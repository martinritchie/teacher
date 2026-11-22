"""Functional spec for `teacher run`. No server is started: the script model is a pydantic-ai FunctionModel, and speech is a stub, except in the slow test.

Flow under test:
1. Load the source (PDF path, PDF URL, arXiv URL, or blog post URL).
2. Split it into chunks of at most --chunk tokens.
3. Abstract: the text under the abstract heading, transcribed for the ear (prompts/episode/abstract.md). A transcription that keeps too few of the original words is made again, once.
4. Contributions: from the abstract as heard, the introduction and the conclusion (prompts/episode/contributions.md).
5. Notes on each chunk (prompts/plan/section_notes.md), then an outline of the method, with thinking on, from every note and what was heard (prompts/plan/planner.md).
6. For each component of the outline:
   a. A detailer, with thinking on, rewrites the component's purpose, inputs, steps and outputs from the full text of its sections (prompts/plan/detailer.md).
   b. Write one spoken part from the outline, the detailed component, its sections, what was heard and the last sentences of the previous part (prompts/part/writer.md).
   c. A listener writes pseudocode from the narration alone (prompts/part/listener.md).
   d. A checker, with thinking on, compares the pseudocode with the component and its source (prompts/part/checker.md). If there are problems, write the part again with them. One rewrite at most.
7. Join abstract, contributions, an overview sentence and the parts; remove markup, split into paragraphs, and speak.
"""

import functools
import json
import re
import threading
from contextlib import contextmanager
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest
from pydantic_ai.exceptions import ModelHTTPError
from pydantic_ai.messages import ModelResponse, TextPart
from pydantic_ai.models.function import AgentInfo, FunctionModel
from pydantic_ai.profiles import ModelProfile
from typer.testing import CliRunner

import teacher.commands.evaluate as eval_mod
import teacher.commands.run as run_mod
import teacher.llm as llm_mod
import teacher.servers as servers
import teacher.source as source
from teacher.cli import app
from teacher.settings import (
    JUDGE_MODEL,
    SAMPLE_RATE,
    VOICE_MODEL,
    WORDS_PER_MINUTE,
    profile,
)

PDF = next((Path(__file__).parents[1] / "papers").glob("CALM*/*.pdf"))
SMALL_MODEL = "Qwen/Qwen3-0.6B"  # only its tokenizer is downloaded
PHASES = {"# Abstract Reader": "abstract", "# Contributions Writer": "contributions", "# Notes Writer": "notes", "# Method Planner": "outline", "# Component Detailer": "detail", "# Method Writer": "method", "# Listener": "reconstruct", "# Method Checker": "check", "# Section Splitter": "split", "# Fact Judge": "judge", "# Leaf Note Taker": "leaf notes", "# Notes Verifier": "notes check"}  # fmt: skip
DIGITS = "zero one two three four five six seven eight nine".split()


def spelled(k):
    """A number in words, digit by digit, since the symbol check rejects digits."""
    return " ".join(DIGITS[int(d)] for d in str(k))


CONTRIBUTIONS = {"context": "Context.", "items": [{"problem": "Problem.", "before": "Before.", "new": "New."}]}  # fmt: skip

BLOG = """<html><head><title>Tracing features</title></head><body>
<nav><a href="/">Home</a> <a href="/subscribe">Subscribe to our newsletter</a></nav>
<article><h1>Tracing features through a transformer</h1>
{body}
</article>
<footer>Copyright notice. Cookie settings.</footer></body></html>"""
PARAGRAPH = "<p>We build an attribution graph for each prompt, and we then study how the features interact across the layers of the model.</p>"

_pdf_to_markdown = functools.cache(source._pdf_to_markdown)


@pytest.fixture(autouse=True)
def pdf_once(monkeypatch):
    """MinerU (vLLM, real GPU) converts each PDF once per session."""
    monkeypatch.setattr(source, "_pdf_to_markdown", _pdf_to_markdown)


class Calls(list):
    """Recorded model calls, plus controls for the stub."""

    verdicts: list[list[str]] = []  # problems for the check calls, in order
    abstracts: list[str] = []  # abstract replies; default echoes the abstract
    contributions: list[dict] = []  # contributions replies; default CONTRIBUTIONS
    details: list = []  # detail replies (a string is invalid output); default "Detailed step k."
    splits: dict = {}  # section title -> [(title, starts_with)]; "*" for every section; default none
    verdict: str = "stated"  # the judge's verdict on every fact
    quote: str | None = None  # the judge's quote; default the narration's first line
    gaps: list[list[str]] = []  # the notes verifier's problems, in order; default none
    started: int = 0  # vLLM servers started
    error: Exception | None = None  # raised by every call when set
    components: list[dict] | None = None  # the outline's; default is one per chunk
    parts: list[str] = []  # replies to the method calls; default "Part k."
    served: str = ""  # the model the script server was started with
    settings: dict = {}  # model settings of each phase

    def of(self, phase):
        return [c for c in self if c.phase == phase]


@pytest.fixture
def llm(monkeypatch):
    """No server process; the script model is a FunctionModel. Each agent's instructions identify its phase."""
    calls = Calls()
    calls.verdicts, calls.abstracts, calls.parts, calls.contributions = [], [], [], []
    calls.details, calls.splits, calls.verdict, calls.started = [], {}, "stated", 0
    calls.gaps, calls.quote = [], None
    calls.settings, calls.components = {}, None

    def reply(messages, info: AgentInfo, model: str):
        if calls.error:
            raise calls.error
        phase = PHASES[info.instructions.splitlines()[0]]
        prompt = str(messages[-1].parts[-1].content)  # a retry's content is a list
        calls.settings[phase] = info.model_settings
        calls.append(SimpleNamespace(phase=phase, prompt=prompt, model=model))
        k = len(calls.of(phase))
        problems = calls.verdicts.pop(0) if phase == "check" and calls.verdicts else []
        n = len(re.findall(r'<chunk number="', prompt))
        components = calls.components or [component(j, [j]) for j in range(1, n + 1)]
        text = {
            "abstract": lambda: json.dumps({"text": calls.abstracts.pop(0) if calls.abstracts else block(prompt, "abstract")}),
            "contributions": lambda: json.dumps(calls.contributions.pop(0) if calls.contributions else CONTRIBUTIONS),
            "notes": lambda: f"Notes {k}.",
            "outline": lambda: json.dumps(method(components)),
            "judge": lambda: json.dumps({"verdict": calls.verdict, "quote": calls.quote if calls.quote is not None else block(prompt, "narration").split("\n")[0]}),
            "leaf notes": lambda: json.dumps({"notes": [f"Note {spelled(k)} a.", f"Note {spelled(k)} b."]}),
            "notes check": lambda: json.dumps({"problems": calls.gaps.pop(0) if calls.gaps else []}),
            "split": lambda: json.dumps({"subsections": [{"title": t, "starts_with": w} for t, w in calls.splits.get(block(prompt, "path").split(" > ")[-1], calls.splits.get("*", []))]}),
            "detail": lambda: (lambda d: d if isinstance(d, str) else json.dumps(d))(calls.details.pop(0) if calls.details else {"purpose": f"Purpose {k}.", "inputs": "x", "steps": [f"Detailed step {k}."], "outputs": "y"}),
            "method": lambda: calls.parts.pop(0) if calls.parts else f"Part {spelled(k)}.",
            "reconstruct": lambda: json.dumps({"pseudocode": f"Code {k}."}),
            "check": lambda: problems if isinstance(problems, str) else json.dumps({"problems": problems}),
        }[phase]()  # fmt: skip
        return ModelResponse(parts=[TextPart(text)])

    @contextmanager
    def no_server(cmd, log, port=None):
        calls.started += 1
        yield "http://server"

    def stub(
        name,
    ):  # named like the real model, since its settings are looked up by name
        return FunctionModel(lambda m, i: reply(m, i, name), model_name=name, profile=ModelProfile(supports_json_schema_output=True))  # fmt: skip

    def model(name, provider):
        calls.served = name
        return stub(name)

    monkeypatch.setattr(servers, "vllm_server", no_server)
    monkeypatch.setattr(servers, "OpenAIChatModel", model)
    monkeypatch.setattr(servers, "claude", stub)  # no Anthropic API calls in tests
    monkeypatch.setattr(eval_mod, "claude", stub)
    monkeypatch.setattr(
        llm_mod, "PARALLEL", 1
    )  # stub replies are numbered in call order
    return calls


@pytest.fixture
def tts(monkeypatch):
    """Stub speech: record the paragraphs and the voice, and return a short silence."""
    calls = []

    def speak(paragraphs, voice, server):
        calls.append(SimpleNamespace(script="\n\n".join(paragraphs), voice=voice))
        return np.zeros(SAMPLE_RATE)

    monkeypatch.setattr(run_mod, "speak", speak)
    return calls


def invoke(*args):
    return CliRunner().invoke(app, ["run", *map(str, args)])


def run(*args):
    result = invoke(*args, "--model", SMALL_MODEL)
    assert result.exit_code == 0, result.output
    return result


def serve(monkeypatch, body: bytes):
    monkeypatch.setattr(
        "urllib.request.urlopen", lambda *a, **k: SimpleNamespace(read=lambda: body)
    )


def block(prompt, tag):
    return re.search(rf"<{tag}>\n(.*?)\n</{tag}>", prompt, re.S).group(1)


def chunk(call):
    return block(call.prompt, "chunk")


def source_of(call):
    return block(call.prompt, "source")


def component(k, chunks, words=150):
    return {"name": f"piece {k}", "purpose": f"Purpose {k}.", "inputs": "x", "steps": [f"Step {k}."], "outputs": "y", "chunks": chunks, "words": words}  # fmt: skip


def method(components):
    glossary = [{"name": "the encoder", "symbol": "E", "meaning": "Encodes."}]
    return {"glossary": glossary, "components": components, "key_numbers": ["Size four."]}  # fmt: skip


def targets(llm):
    return [int(re.search(r"about (\d+) words", c.prompt).group(1)) for c in llm.of("method")]  # fmt: skip


def paragraphs(tts):
    return tts[0].script.split("\n\n")


# --- Inputs ---


def test_no_audio_writes_the_script_only(llm, tts, tmp_path):
    """--no-audio stops after the script: <name>.md is written, and no TTS is started."""
    run(PDF, "--out", tmp_path, "--no-audio")
    assert (tmp_path / f"{PDF.stem}.md").read_text().startswith("The efficiency")
    assert not tts and not (tmp_path / f"{PDF.stem}.mp3").exists()


def test_pdf_in_script_and_audio_out(llm, tts, tmp_path):
    """One command turns a local PDF into <name>.md and <name>.mp3."""
    run(PDF, "--out", tmp_path)
    assert (tmp_path / f"{PDF.stem}.mp3").exists()
    assert (tmp_path / f"{PDF.stem}.md").read_text() == tts[0].script


def test_arxiv_abs_url_is_read_as_pdf(llm, tts, tmp_path, monkeypatch):
    """An arXiv abstract URL downloads the PDF. The arXiv id names the output."""
    seen = []

    def urlopen(req, *a, **k):
        seen.append(getattr(req, "full_url", req))
        return SimpleNamespace(read=PDF.read_bytes)

    monkeypatch.setattr("urllib.request.urlopen", urlopen)
    run("https://arxiv.org/abs/2510.27688v1", "--out", tmp_path)
    assert seen == ["https://arxiv.org/pdf/2510.27688v1"]
    assert (tmp_path / "2510.27688v1.mp3").exists()


def test_blog_post_url_is_read_as_article(llm, tts, tmp_path, monkeypatch):
    """An HTML URL gives the model the article text only. The last URL segment names the output."""
    serve(monkeypatch, BLOG.format(body=PARAGRAPH * 8).encode())
    run(
        "https://transformer-circuits.pub/2025/attribution-graphs/biology.html",
        "--out",
        tmp_path,
    )
    source = chunk(llm.of("notes")[0])
    assert "attribution graph" in source
    assert "newsletter" not in source and "Cookie" not in source
    assert (tmp_path / "biology.mp3").exists()


# --- Context: a long source is the normal case ---


def test_chunk_sets_the_source_tokens_for_each_call(llm, tts, tmp_path):
    """--chunk is the quality limit, counted with the model's tokenizer. Sections over it are split, so a smaller value gives more chunks."""
    from transformers import AutoTokenizer

    tokens = AutoTokenizer.from_pretrained(SMALL_MODEL)
    run(PDF, "--out", tmp_path, "--chunk", 500)
    small = llm.of("notes")
    assert all(len(tokens.encode(chunk(c))) <= 500 for c in small)
    llm.clear()
    run(PDF, "--out", tmp_path, "--chunk", 6000)
    assert 1 < len(llm.of("notes")) < len(small)


def test_chunks_are_the_sources_sections(llm, tts, tmp_path):
    """Each chunk is one section of the source, starting with its heading; a heading with no text of its own joins the next. The outline sees every heading."""
    run(PDF, "--out", tmp_path)
    notes, outline = llm.of("notes"), llm.of("outline")[0].prompt
    assert chunk(notes[1]).startswith(
        "## ABSTRACT"
    ) and "## 1 INTRODUCTION" not in chunk(notes[1])
    assert chunk(notes[2]).startswith("## 1 INTRODUCTION")
    assert 'heading="ABSTRACT"' in outline
    assert 'heading="2 AUTOENCODER / 2.1 HIGH-FIDELITY RECONSTRUCTION"' in outline


def test_rejected_call_is_an_error(llm, tts, tmp_path):
    """If vLLM rejects a call (for example, a prompt longer than its window), stop, point at --chunk, and write no audio."""
    llm.error = ModelHTTPError(400, SMALL_MODEL, body="maximum context length")
    result = invoke(PDF, "--out", tmp_path, "--model", SMALL_MODEL)
    assert result.exit_code != 0
    assert "--chunk" in result.output and "maximum context length" in result.output
    assert not tts


def test_whole_source_is_covered_without_references(llm, tts, tmp_path):
    """The chunks cover the source from the abstract to the conclusion. The reference list and all after it are cut."""
    run(PDF, "--out", tmp_path)
    source = "".join(chunk(c) for c in llm.of("notes"))
    assert "ABSTRACT" in source and "CONCLUSION" in source
    assert not re.search(r"\n#+ \W*References", source, re.I)
    assert "PROOF OF THEOREM" not in source


# --- Script ---


def test_abstract_then_contributions_then_how_it_works(llm, tts, tmp_path):
    """The script is the abstract, the contributions, a sentence naming the method's pieces, then one part per piece."""
    llm.components = [component(1, [1]), component(2, [3])]
    run(PDF, "--out", tmp_path)
    script = paragraphs(tts)
    overview = "Here is how it works. The method has two pieces: piece 1 and piece 2."
    tail = [
        "Context.",
        "Problem. Before. New.",
        overview,
        "Part one.",
        "Part two.",
    ]
    assert script[-5:] == tail and len(script) > 5


def test_abstract_is_transcribed_from_the_abstract_alone(llm, tts, tmp_path):
    """The abstract reader sees only the text under the abstract heading, and its transcription opens the script."""
    run(PDF, "--out", tmp_path)
    abstract = block(llm.of("abstract")[0].prompt, "abstract")
    assert "continuous" in abstract.lower() and "introduction" not in abstract.lower()
    assert paragraphs(tts)[0].split()[:5] == abstract.split()[:5]


def test_abstract_that_strays_is_transcribed_again(llm, tts, tmp_path):
    """A transcription that keeps too few of the abstract's words is made again, once, told why."""
    llm.abstracts = ["Something else entirely."]
    run(PDF, "--out", tmp_path)
    assert len(llm.of("abstract")) == 2
    assert "Keep every sentence" in block(llm.of("abstract")[1].prompt, "problems")
    assert "Something else" not in tts[0].script


def test_abstract_with_symbols_is_transcribed_again(llm, tts, tmp_path):
    """Words with digits or symbols left in the transcription go back as a problem."""
    run(PDF, "--out", tmp_path)  # the stub echoes the abstract, which says 99.9%
    first, second = llm.of("abstract")
    assert "<problems>" not in first.prompt
    assert "99.9%" in block(second.prompt, "problems")


def test_contributions_see_the_abstract_introduction_and_conclusion(llm, tts, tmp_path):
    """The contributions writer hears the abstract as spoken and reads the introduction and the conclusion."""
    run(PDF, "--out", tmp_path)
    prompt = llm.of("contributions")[0].prompt
    assert paragraphs(tts)[0] in block(prompt, "heard")
    assert block(prompt, "introduction") and block(prompt, "conclusion")


def test_outline_sees_every_note_and_what_was_heard(llm, tts, tmp_path):
    """All notes come before the outline, which sees every note and the abstract and contributions."""
    run(PDF, "--out", tmp_path)
    notes, outline = llm.of("notes"), llm.of("outline")[0]
    assert llm.index(outline) == llm.index(notes[-1]) + 1
    assert all(f"Notes {k}." in outline.prompt for k in range(1, len(notes) + 1))
    assert "Problem. Before. New." in block(outline.prompt, "heard")


def test_each_part_gets_its_component_and_its_chunks(llm, tts, tmp_path):
    """Each part gets the sections its component names, in that order, invented numbers dropped."""
    llm.components = [component(1, [3, 1, 2]), component(2, [99, 0, 3])]
    run(PDF, "--out", tmp_path)
    notes, parts = llm.of("notes"), llm.of("method")
    joined = "\n\n".join(chunk(notes[k]) for k in (2, 0, 1))
    assert source_of(parts[0]) == joined
    assert source_of(parts[1]) == chunk(notes[2])
    assert 'part on "piece 2"' in parts[1].prompt and len(parts) == 2


def test_each_component_is_detailed_from_its_sections(llm, tts, tmp_path):
    """Before its part is written, each component's mechanism is rewritten from its sections; the writer and checker get the rewrite. Name, sections and words stay the outline's."""
    llm.components = [component(1, [3]), component(2, [2])]
    run(PDF, "--out", tmp_path)
    notes, details, parts = llm.of("notes"), llm.of("detail"), llm.of("method")
    assert [source_of(d) for d in details] == [chunk(notes[2]), chunk(notes[1])]
    assert (
        "1. Step 2." in details[1].prompt
        and "- piece 1: Purpose 1." in details[1].prompt
    )
    assert llm.index(details[1]) < llm.index(parts[1])
    assert (
        "1. Detailed step 2." in parts[1].prompt and "1. Step 2." not in parts[1].prompt
    )
    assert 'part on "piece 2"' in parts[1].prompt
    assert "1. Detailed step 1." in llm.of("check")[0].prompt


def test_a_detail_with_no_valid_answer_keeps_the_outline(llm, tts, tmp_path):
    """A detailer reply that is not a component does not end the run: the outline's draft is used."""
    llm.components = [component(1, [1])]
    llm.details = [
        "not a component",
        "still not a component",
    ]  # the reply and its retry
    run(PDF, "--out", tmp_path)
    assert "1. Step 1." in llm.of("method")[0].prompt


def test_part_sources_stop_at_the_size_limit(llm, tts, tmp_path):
    """A component that names many sections gets them in order, up to about four thousand tokens, so the writer and checker stay inside their window."""
    llm.components = [component(1, list(range(1, 30)))]
    run(PDF, "--out", tmp_path)
    source = source_of(llm.of("method")[0])
    assert source.startswith(chunk(llm.of("notes")[0])) and 8000 < len(source) <= 16000


def test_contributions_with_symbols_are_written_again(llm, tts, tmp_path):
    """Words with digits or symbols in the contributions go back as a problem, once."""
    llm.contributions = [{**CONTRIBUTIONS, "context": "Over 99.9% of it."}]
    run(PDF, "--out", tmp_path)
    first, second = llm.of("contributions")
    assert "<problems>" not in first.prompt and "99.9%" in block(
        second.prompt, "problems"
    )
    assert "Over 99.9% of it." not in tts[0].script


def test_each_part_gets_the_glossary_what_was_heard_and_the_previous_part(
    llm, tts, tmp_path
):
    """Every part uses the same names, knows what the listener heard, and continues from the last sentences."""
    run(PDF, "--out", tmp_path)
    parts = llm.of("method")
    assert all("- the encoder (the paper's E): Encodes." in c.prompt for c in parts)
    assert all("Problem. Before. New." in block(c.prompt, "heard") for c in parts)
    assert block(parts[0].prompt, "previous") == ""
    for k, call in enumerate(parts[1:], start=1):
        assert block(call.prompt, "previous") == f"Part {spelled(k)}."


def test_listener_hears_only_the_narration(llm, tts, tmp_path):
    """The listener gets the earlier parts and this part, never the source or the outline."""
    llm.components = [component(1, [1]), component(2, [2])]
    run(PDF, "--out", tmp_path)
    notes, listens = llm.of("notes"), llm.of("reconstruct")
    assert [block(c.prompt, "part") for c in listens] == ["Part one.", "Part two."]
    assert block(listens[1].prompt, "heard") == "Part one."
    assert not any(
        chunk(notes[0])[:200] in c.prompt or "Purpose" in c.prompt for c in listens
    )


def test_check_compares_the_pseudocode_with_the_component_and_source(
    llm, tts, tmp_path
):
    """One check per part: it sees the component's steps, its source, the part and the listener's pseudocode."""
    llm.components = [component(1, [2])]
    run(PDF, "--out", tmp_path)
    check = llm.of("check")[0].prompt
    assert len(llm.of("check")) == len(llm.of("method"))
    assert "1. Detailed step 1." in check and block(check, "pseudocode") == "Code 1."
    assert source_of(llm.of("check")[0]) == chunk(llm.of("notes")[1])


def test_a_check_with_no_valid_answer_counts_as_no_problems(llm, tts, tmp_path):
    """A checker reply that is not a verdict (thinking ran out of tokens) does not end the run: no problems, and the error is in the trace."""
    llm.components = [component(1, [1])]
    llm.verdicts = ["not a verdict", "still not a verdict"]  # the reply and its retry
    run(PDF, "--out", tmp_path)
    assert len(llm.of("method")) == 1
    trace = (tmp_path / f"{PDF.stem}.trace.jsonl").read_text().splitlines()
    checks = [json.loads(t) for t in trace if '"part/checker"' in t]
    assert "error" in checks[0] and checks[0]["output"] == {"problems": []}


def test_failed_check_gives_one_rewrite(llm, tts, tmp_path):
    """Problems from the check go back to the writer. The rewrite replaces the part and gets no second check."""
    llm.components = [component(1, [1])]
    llm.verdicts = [["The size of the latent vector is unclear."]]
    run(PDF, "--out", tmp_path)
    parts = llm.of("method")
    assert len(parts) == 2 and len(llm.of("check")) == 1
    assert "- The size of the latent vector is unclear." in parts[1].prompt
    assert block(parts[1].prompt, "draft") == "Part one."
    assert paragraphs(tts)[-1] == "Part two."


def test_word_targets_come_from_the_outline_capped(llm, tts, tmp_path):
    """Each part's word target is the outline's, capped at three hundred words; a long --minutes does not pad them."""
    llm.components = [component(1, [1], 100), component(2, [2], 500)]
    run(PDF, "--out", tmp_path, "--minutes", 60)
    assert targets(llm) == [100, 300]


def test_minutes_shrinks_the_targets_to_fit(llm, tts, tmp_path):
    """If the outline's targets do not fit in what is left of --minutes after the abstract and contributions, they shrink in proportion."""
    llm.components = [component(1, [1], 200), component(2, [2], 400)]
    run(PDF, "--out", tmp_path, "--minutes", 4)
    heard = " ".join(paragraphs(tts)[:-3])
    left = 4 * WORDS_PER_MINUTE - len(heard.split())
    assert sum(targets(llm)) == pytest.approx(left, abs=3)
    assert targets(llm)[1] == pytest.approx(2 * targets(llm)[0], abs=1)


def test_symbols_in_a_part_are_problems(llm, tts, tmp_path):
    """Words with digits or symbols in a part go to the rewrite as a problem, even when the checker finds none."""
    llm.components = [component(1, [1])]
    llm.parts = ["Set K=4 for 99.9% accuracy."]
    run(PDF, "--out", tmp_path)
    assert "K=4, 99.9%" in block(llm.of("method")[1].prompt, "problems")


def test_every_call_is_traced(llm, tts, tmp_path):
    """<name>.trace.jsonl has one line per model call: the prompt template, the message sent and the reply."""
    run(PDF, "--out", tmp_path)
    trace = (tmp_path / f"{PDF.stem}.trace.jsonl").read_text().splitlines()
    lines = [json.loads(line) for line in trace]
    assert [line["prompt"] for line in lines] == [c.prompt for c in llm]
    assert lines[0]["call"] == "episode/abstract" and "text" in lines[0]["output"]


def test_markup_never_reaches_tts(llm, tts, tmp_path, monkeypatch):
    """TTS reads markup aloud. Remove break tags and markdown marks even if the model writes them."""
    dirty = '# Intro\n\nThe **loss** falls. <break time="1.0s" /> Then it stops.'
    monkeypatch.setattr(run_mod, "write_episode", lambda *a, **k: dirty)
    run(PDF, "--out", tmp_path)
    assert not re.search(r"[#*<>]", tts[0].script)
    assert "The loss falls." in tts[0].script


# --- Models ---


def test_models_are_cli_arguments(llm, tts, tmp_path):
    """--model is the model vLLM serves. --voice reaches the TTS."""
    run(PDF, "--out", tmp_path, "--voice", "aiden")
    assert llm.served == SMALL_MODEL
    assert tts[0].voice == "aiden"


def test_only_the_outline_and_check_think(llm, tts, tmp_path):
    """Thinking is on for the outline and the check and off for everything else, each with Qwen3's sampling for its mode."""
    run(PDF, "--out", tmp_path)
    thinks = {p: s["extra_body"]["chat_template_kwargs"]["enable_thinking"] for p, s in llm.settings.items()}  # fmt: skip
    assert thinks == {"abstract": False, "contributions": False, "notes": False, "outline": True, "detail": True, "method": False, "reconstruct": False, "check": True}  # fmt: skip


@pytest.mark.slow
def test_voice_model_writes_playable_audio(tmp_path):
    """Real Qwen3-TTS on vLLM-Omni, no stub: two paragraphs become audio of more than two seconds."""
    from teacher.servers import serve_voice_model
    from teacher.speech import speak

    with serve_voice_model(VOICE_MODEL, tmp_path / "voice.log") as server:
        audio = speak(
            ["The authors train an autoencoder.", "Then they predict."], "ryan", server
        )
    assert len(audio) / SAMPLE_RATE > 2


# --- Outline: a tree of headings and subheadings ---

LONG = (
    "The method works in stages. " * 70
)  # over the length below which text is one idea
DOC = f"""# A Paper

## Abstract

Short abstract.

## 1 Introduction

{LONG}

## 2 Method

Some preamble.

## 2.1 Encoder

The encoder maps tokens to vectors. {LONG}

The decoder maps vectors back to tokens. {LONG}

## 2.2 Loss

The loss compares samples. {LONG}
"""


def outline(llm, tmp_path, doc=DOC):
    (tmp_path / "paper.md").write_text(doc)
    args = ["outline", tmp_path / "paper.md", "--out", tmp_path, "--model", SMALL_MODEL]
    result = CliRunner().invoke(app, list(map(str, args)))
    assert result.exit_code == 0, result.output
    tree = json.loads((tmp_path / "paper.outline.json").read_text())
    return (tmp_path / "paper.outline.md").read_text(), tree


def test_outline_top_level_is_the_sources_top_level_sections(llm, tmp_path):
    """The top level is the source's top-level headings; numbered subheadings stay inside their section. Each long section is offered to the splitter whole."""
    headings, tree = outline(llm, tmp_path)
    assert headings == "- A Paper\n- Abstract\n- 1 Introduction\n- 2 Method\n"
    splits = {block(c.prompt, "path"): block(c.prompt, "text") for c in llm.of("split")}
    assert set(splits) == {"1 Introduction", "2 Method"}
    assert (
        "## 2.1 Encoder" in splits["2 Method"] and "## 2.2 Loss" in splits["2 Method"]
    )


def test_outline_breaks_each_section_down_recursively(llm, tmp_path):
    """Listed subsections become children, cut where their quoted opening words are, and each is broken down in turn. A leaf keeps its text."""
    llm.splits = {
        "2 Method": [("Encoder", "## 2.1 Encoder"), ("Loss", "2.2 Loss")],
        "Encoder": [
            ("Encoding", "The encoder maps tokens"),
            ("Decoding", "The decoder maps vectors back"),
        ],
    }
    headings, tree = outline(llm, tmp_path)
    assert headings.endswith(
        "- 2 Method\n  - Encoder\n    - Encoding\n    - Decoding\n  - Loss\n"
    )
    method = tree[3]
    assert method["text"].strip().endswith("Some preamble.")
    encoder, loss = method["children"]
    assert encoder["children"][1]["text"].startswith("The decoder maps vectors back")
    assert loss["text"].startswith("## 2.2 Loss") and not loss["children"]
    assert "2 Method > Encoder" in [block(c.prompt, "path") for c in llm.of("split")]


def test_outline_ignores_quotes_that_are_not_in_the_text(llm, tmp_path):
    """A subsection whose opening words are not in the text is merged into the one before; with fewer than two left, the section is a leaf."""
    llm.splits = {
        "2 Method": [
            ("Encoder", "## 2.1 Encoder"),
            ("Invented", "words that appear nowhere"),
        ]
    }
    headings, tree = outline(llm, tmp_path)
    assert headings.endswith("- 2 Method\n") and not tree[3]["children"]


def test_outline_stops_at_four_levels(llm, tmp_path):
    """However deep the text nests, the tree goes at most four levels below the top-level sections."""
    nested = ""
    for d in range(8, 0, -1):  # level d: "Lead d." then level d + 1, then "Mid d."
        nested = f"Lead {d}. {LONG[:900]}{nested} Mid {d}. {LONG[:900]}"
    llm.splits = {"1 Method": [("L1", "Lead 1."), ("M1", "Mid 1.")]}
    llm.splits |= {
        f"L{d}": [(f"L{d + 1}", f"Lead {d + 1}."), (f"M{d + 1}", f"Mid {d + 1}.")]
        for d in range(1, 8)
    }
    headings, _ = outline(llm, tmp_path, f"## 1 Method\n\n{nested}")
    assert "        - L4" in headings and "L5" not in headings


# --- Fast iteration: one node at a time, a fixed set of cases, a server kept running ---

TREE = [
    {"title": "1 Intro", "text": "Intro text.", "children": []},
    {"title": "2 Method", "text": "Preamble.", "children": [
        {"title": "Encoder", "text": "The encoder maps tokens to vectors.", "children": []},
        {"title": "Loss", "text": "", "children": [
            {"title": "Distance term", "text": "The distance term compares samples.", "children": []},
            {"title": "Diversity term", "text": "The diversity term spreads samples.", "children": []},
        ]},
    ]},
]  # fmt: skip


def cli(*args):
    result = CliRunner().invoke(app, [*map(str, args), "--model", SMALL_MODEL])
    assert result.exit_code == 0, result.output
    return result.output


def test_write_narrates_every_leaf_under_a_node(llm, tmp_path):
    """`teacher write` narrates the leaves under the named node, in order: notes on each leaf's own text, then a part written from them with its siblings as the outline, listened to and checked."""
    (tmp_path / "x.outline.json").write_text(json.dumps(TREE))
    cli("write", tmp_path / "x.outline.json", "--node", "method", "--out", tmp_path)
    notes, parts = llm.of("leaf notes"), llm.of("method")
    assert [source_of(c) for c in notes] == ["The encoder maps tokens to vectors.", "The distance term compares samples.", "The diversity term spreads samples."]  # fmt: skip
    assert not llm.of("detail")
    assert (
        "1. Note one a.\n2. Note one b." in parts[0].prompt
        and "about 80 words" in parts[0].prompt
    )
    assert "1. Note two a." in llm.of("check")[1].prompt
    assert "- Encoder\n- Loss\n</outline>" in parts[0].prompt
    assert (
        "- Diversity term\n" in parts[1].prompt
        and 'part on "Distance term"' in parts[1].prompt
    )
    assert len(llm.of("check")) == 3
    assert (
        tmp_path / "x.2-method.md"
    ).read_text() == "Part one.\n\nPart two.\n\nPart three.\n"


def test_eval_scores_each_case_against_its_facts(llm, tmp_path):
    """`teacher eval` narrates each case's node and judges it one fact per call; the table counts the verdicts and the report keeps the narration."""
    (tmp_path / "x.outline.json").write_text(json.dumps(TREE))
    cases = [{"tree": str(tmp_path / "x.outline.json"), "node": "Encoder", "facts": ["It maps tokens.", "It is small."]},
             {"tree": str(tmp_path / "x.outline.json"), "node": "Loss", "facts": ["Two terms."]}]  # fmt: skip
    (tmp_path / "cases.json").write_text(json.dumps(cases))
    llm.verdict = "missing"
    output = cli("eval", tmp_path / "cases.json", "--out", tmp_path)
    assert re.search(r"Encoder +0/2 +2 +0", output) and re.search(r"total +0/3", output)
    judged = {
        block(c.prompt, "fact"): block(c.prompt, "narration") for c in llm.of("judge")
    }
    assert judged == {"It maps tokens.": "Part one.", "It is small.": "Part one.", "Two terms.": "Part two.\n\nPart three."}  # fmt: skip
    report = next(tmp_path.glob("*.md")).read_text()
    assert "- **missing**: It is small." in report and "Part one." in report


def test_eval_runs_only_the_cases_asked_for(llm, tmp_path):
    """--only picks cases by node title."""
    (tmp_path / "x.outline.json").write_text(json.dumps(TREE))
    cases = [{"tree": str(tmp_path / "x.outline.json"), "node": n, "facts": ["A fact."]} for n in ("Encoder", "Loss")]  # fmt: skip
    (tmp_path / "cases.json").write_text(json.dumps(cases))
    cli("eval", tmp_path / "cases.json", "--only", "loss", "--out", tmp_path)
    assert len(llm.of("judge")) == 1


def test_server_option_uses_a_running_server(llm, tmp_path):
    """With --server, commands use that server instead of starting vLLM."""
    (tmp_path / "x.outline.json").write_text(json.dumps(TREE))
    cli(
        "write",
        tmp_path / "x.outline.json",
        "--node",
        "Encoder",
        "--out",
        tmp_path,
        "--server",
        "http://127.0.0.1:8000",
    )
    assert llm.started == 0
    cli("write", tmp_path / "x.outline.json", "--node", "Encoder", "--out", tmp_path)
    assert llm.started == 1


def test_notes_are_verified_and_revised_until_nothing_is_missing(llm, tmp_path):
    """A separate verifier checks each leaf's notes against its text; the note-taker revises with the problems, and the loop stops when the verifier finds none."""
    (tmp_path / "x.outline.json").write_text(json.dumps(TREE))
    llm.gaps = [["The notes miss the vector size."], []]
    cli("write", tmp_path / "x.outline.json", "--node", "Encoder", "--out", tmp_path)
    takes, checks = llm.of("leaf notes"), llm.of("notes check")
    assert len(takes) == 2 and len(checks) == 2
    assert block(checks[0].prompt, "notes") == "- Note one a.\n- Note one b."
    assert source_of(checks[0]) == "The encoder maps tokens to vectors."
    assert "- The notes miss the vector size." in block(takes[1].prompt, "problems")
    assert block(takes[1].prompt, "draft") == "- Note one a.\n- Note one b."
    assert "1. Note two a." in llm.of("method")[0].prompt


def test_note_rounds_caps_the_loop(llm, tmp_path):
    """--note-rounds caps the verify-and-revise rounds; 0 keeps the first draft unchecked."""
    (tmp_path / "x.outline.json").write_text(json.dumps(TREE))
    llm.gaps = [["Missing one."], ["Missing two."], ["Missing three."]]
    cli(
        "write",
        tmp_path / "x.outline.json",
        "--node",
        "Encoder",
        "--out",
        tmp_path,
        "--note-rounds",
        2,
    )
    assert len(llm.of("notes check")) == 2 and len(llm.of("leaf notes")) == 3
    llm.clear()
    cli(
        "write",
        tmp_path / "x.outline.json",
        "--node",
        "Encoder",
        "--out",
        tmp_path,
        "--note-rounds",
        0,
    )
    assert not llm.of("notes check") and len(llm.of("leaf notes")) == 1


def test_a_verdict_whose_quote_is_not_in_the_narration_counts_as_missing(llm, tmp_path):
    """A stated or contradicted verdict must quote the narration; if its quote is not there, the fact counts as missing and is flagged."""
    (tmp_path / "x.outline.json").write_text(json.dumps(TREE))
    cases = [{"tree": str(tmp_path / "x.outline.json"), "node": "Encoder", "facts": ["It maps tokens."]}]  # fmt: skip
    (tmp_path / "cases.json").write_text(json.dumps(cases))
    llm.quote = "Words the narration never says."
    output = cli("eval", tmp_path / "cases.json", "--out", tmp_path)
    assert re.search(r"Encoder +0/1 +1 +0 +1", output)
    assert (
        "judged stated, but the quote is not in the narration"
        in next(tmp_path.glob("*.md")).read_text()
    )
    llm.clear()
    llm.quote = "part ONE"  # case and edge punctuation do not matter
    assert re.search(
        r"Encoder +1/1", cli("eval", tmp_path / "cases.json", "--out", tmp_path)
    )


def test_independent_calls_run_in_parallel_in_order(llm, tmp_path, monkeypatch):
    """With several calls in flight, results still come back in order: each case keeps its own narration and verdicts."""
    monkeypatch.setattr(llm_mod, "PARALLEL", 4)
    (tmp_path / "x.outline.json").write_text(json.dumps(TREE))
    cases = [{"tree": str(tmp_path / "x.outline.json"), "node": n, "facts": [f"{n} fact {i}." for i in "ab"]} for n in ("Encoder", "Loss", "Distance term")]  # fmt: skip
    (tmp_path / "cases.json").write_text(json.dumps(cases))
    output = cli("eval", tmp_path / "cases.json", "--out", tmp_path)
    assert [line.split()[0] for line in output.splitlines()[2:5]] == [
        "Encoder",
        "Loss",
        "Distance",
    ]
    assert re.search(r"total +6/6", output) and len(llm.of("judge")) == 6
    trace = (
        (tmp_path / next(p.name for p in tmp_path.glob("*.trace.jsonl")))
        .read_text()
        .splitlines()
    )
    assert len(trace) == len(llm)  # every call traced, none lost to a race


# --- Models: settings by family, Claude on the API, a fixed judge, one cap on calls in flight ---


def test_eval_judges_with_the_fixed_judge_whatever_narrates(llm, tmp_path):
    """The narration comes from --model; every judge call goes to settings.JUDGE_MODEL, and the report says which is which."""
    (tmp_path / "x.outline.json").write_text(json.dumps(TREE))
    cases = [{"tree": str(tmp_path / "x.outline.json"), "node": "Encoder", "facts": ["It maps tokens."]}]  # fmt: skip
    (tmp_path / "cases.json").write_text(json.dumps(cases))
    output = cli("eval", tmp_path / "cases.json", "--out", tmp_path)
    assert {c.model for c in llm.of("judge")} == {JUDGE_MODEL}
    assert {c.model for c in llm if c.phase != "judge"} == {SMALL_MODEL}
    assert f"narrated by {SMALL_MODEL}, judged by {JUDGE_MODEL}" in output


def test_a_claude_model_runs_on_the_api_with_its_own_settings(llm, tmp_path):
    """--model claude-* starts no vLLM server. Its calls get Claude's settings: effort by role, no sampling settings."""
    (tmp_path / "x.outline.json").write_text(json.dumps(TREE))
    args = ["write", tmp_path / "x.outline.json", "--node", "Encoder", "--out", tmp_path, "--model", "claude-sonnet-5-5"]  # fmt: skip
    result = CliRunner().invoke(app, list(map(str, args)))
    assert result.exit_code == 0, result.output
    assert llm.started == 0 and {c.model for c in llm} == {"claude-sonnet-5-5"}
    assert llm.settings["method"]["anthropic_effort"] == "low"
    assert llm.settings["check"]["anthropic_effort"] == "high"
    assert not any("temperature" in s or "top_p" in s for s in llm.settings.values())


def test_a_model_with_no_profile_is_an_error():
    """Settings are looked up by model family; an unknown family says where to add one."""
    with pytest.raises(ValueError, match="PROFILES"):
        profile("gemma-4-12b")


def test_calls_in_flight_are_capped_however_parallel_nests(llm, tmp_path, monkeypatch):
    """Every model call holds one of PARALLEL slots, so nested `parallel` calls (cases, then notes, then facts) cannot
    exceed it; and nesting cannot deadlock."""
    held, most = [0], [0]

    class Slots:
        def __init__(self):
            self.inner = threading.BoundedSemaphore(2)

        def __enter__(self):
            self.inner.acquire()
            held[0] += 1
            most[0] = max(most[0], held[0])

        def __exit__(self, *exc):
            held[0] -= 1
            self.inner.release()

    monkeypatch.setattr(llm_mod, "PARALLEL", 4)
    monkeypatch.setattr(llm_mod, "_slots", Slots())
    (tmp_path / "x.outline.json").write_text(json.dumps(TREE))
    cases = [{"tree": str(tmp_path / "x.outline.json"), "node": n, "facts": ["A.", "B."]} for n in ("Method", "Loss", "Encoder")]  # fmt: skip
    (tmp_path / "cases.json").write_text(json.dumps(cases))
    cli("eval", tmp_path / "cases.json", "--out", tmp_path)
    assert 1 <= most[0] <= 2 and len(llm) > 20


def test_a_parents_own_text_is_narrated_before_its_children(llm, tmp_path):
    """Text a section has before its first subsection is narrated too, as the first part, unless it is only a
    heading or a line."""
    long_intro = "The batch method draws many samples at once and counts repeats. " * 8
    tree = [{"title": "5.3 Batch", "text": long_intro, "children": [
        {"title": "Algorithm", "text": "The algorithm counts.", "children": []},
        {"title": "Theorem", "text": "The bias vanishes.", "children": []}]}]  # fmt: skip
    (tmp_path / "x.outline.json").write_text(json.dumps(tree))
    cli("write", tmp_path / "x.outline.json", "--node", "5.3", "--out", tmp_path)
    assert [source_of(c) for c in llm.of("leaf notes")] == [long_intro, "The algorithm counts.", "The bias vanishes."]  # fmt: skip
    llm.clear()
    cli("write", tmp_path / "x.outline.json", "--node", "Batch", "--out", tmp_path)
    tree[0]["text"] = "## 5.3 Batch\n"
    (tmp_path / "x.outline.json").write_text(json.dumps(tree))
    llm.clear()
    cli("write", tmp_path / "x.outline.json", "--node", "5.3", "--out", tmp_path)
    assert len(llm.of("leaf notes")) == 2  # a bare heading is not narrated
