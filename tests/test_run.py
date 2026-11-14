"""Functional spec for `teacher run`. The LLM (ollama.chat) and Kokoro are stubs, except in the slow test.

Flow under test:
1. Load the source (PDF path, PDF URL, arXiv URL, or blog post URL).
2. Split it into chunks of at most --chunk tokens.
3. Notes pass: one call for each chunk (system prompt: prompts/notes.md).
4. For each chunk, in order:
   a. Write one spoken part from the chunk, all the notes, and the end of the previous part (prompts/script.md).
   b. Check the part against the notes of its chunk (prompts/check.md). The reply is "OK" or a list of problems.
   c. If the reply is not "OK", write the part again with the problems. One rewrite at most.
5. Join the parts, remove markup, and speak.
"""

import re
from pathlib import Path
from types import SimpleNamespace

import pytest
from typer.testing import CliRunner

import teacher.run as run_mod
from teacher.cli import app

PDF = next((Path(__file__).parents[1] / "papers").glob("CALM*/*.pdf"))
WORDS_PER_MINUTE = 150
REPLY_RESERVE = 1000  # tokens that each call must leave free for the reply

BLOG = """<html><head><title>Tracing features</title></head><body>
<nav><a href="/">Home</a> <a href="/subscribe">Subscribe to our newsletter</a></nav>
<article><h1>Tracing features through a transformer</h1>
{body}
</article>
<footer>Copyright notice. Cookie settings.</footer></body></html>"""
PARAGRAPH = "<p>We build an attribution graph for each prompt, and we then study how the features interact across the layers of the model.</p>"


class Calls(list):
    """Recorded ollama.chat calls, plus controls for the stub."""

    verdicts: list[str] = []  # replies for the check calls, in order; "OK" when empty
    notes_pad = ""  # extra text on each notes reply, to make the notes large
    prompt_tokens = 10  # the prompt_eval_count that the stub reports

    def of(self, phase):
        return [c for c in self if c.phase == phase]


@pytest.fixture
def llm(monkeypatch):
    """Stub ollama.chat. The system prompt file identifies the phase: notes, script, or check."""
    calls = Calls()
    calls.verdicts = []

    def chat(model, messages, options=None, **_):
        system = messages[0]["content"]
        phase = next(
            p.stem
            for p in run_mod.PROMPTS.glob("*.md")
            if system.startswith(p.read_text())
        )
        calls.append(
            SimpleNamespace(
                phase=phase, model=model, messages=messages, options=options
            )
        )
        k = len(calls.of(phase))
        text = {
            "notes": f"Notes {k}.{calls.notes_pad}",
            "script": f"Part {k}.",
            "check": "OK",
        }[phase]
        if phase == "check" and calls.verdicts:
            text = calls.verdicts.pop(0)
        return SimpleNamespace(
            message=SimpleNamespace(content=text),
            prompt_eval_count=calls.prompt_tokens,
            eval_count=5,
        )

    monkeypatch.setattr("ollama.chat", chat)
    return calls


@pytest.fixture
def tts(monkeypatch):
    """Stub Kokoro: record the text and the voice, and write a placeholder file."""
    calls = []

    def speak(script, voice, out):
        calls.append(SimpleNamespace(script=script, voice=voice))
        out.write_bytes(b"mp3")

    monkeypatch.setattr(run_mod, "speak", speak)
    return calls


def invoke(*args):
    return CliRunner().invoke(app, ["run", *map(str, args)])


def run(*args):
    result = invoke(*args)
    assert result.exit_code == 0, result.output
    return result


def serve(monkeypatch, body: bytes):
    monkeypatch.setattr(
        "urllib.request.urlopen", lambda *a, **k: SimpleNamespace(read=lambda: body)
    )


def tokens(call):
    return sum(len(m["content"]) for m in call.messages) // 4


# --- Inputs ---


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
    source = llm[0].messages[1]["content"]
    assert "attribution graph" in source
    assert "newsletter" not in source and "Cookie" not in source
    assert (tmp_path / "biology.mp3").exists()


# --- Context: a long source is the normal case ---


def test_chunk_sets_the_source_tokens_for_each_call(llm, tts, tmp_path):
    """--chunk is the quality limit. No chunk is larger, and a smaller value gives more chunks."""
    run(PDF, "--out", tmp_path, "--chunk", 2000)
    small = llm.of("notes")
    assert all(len(c.messages[1]["content"]) // 4 <= 2000 for c in small)
    llm.clear()
    run(PDF, "--out", tmp_path, "--chunk", 6000)
    assert 1 < len(llm.of("notes")) < len(small)


def test_window_holds_every_call_and_its_reply(llm, tts, tmp_path, monkeypatch):
    """The code sets num_ctx itself. Each prompt fits with a reserve for the reply, even when the notes are large."""
    serve(monkeypatch, BLOG.format(body=PARAGRAPH * 400).encode())
    llm.notes_pad = " fact" * 2000
    run("https://example.com/long-post", "--out", tmp_path, "--chunk", 2000)
    assert len(llm.of("notes")) > 4
    assert all(tokens(c) + REPLY_RESERVE <= c.options["num_ctx"] for c in llm)
    assert (
        len({c.options["num_ctx"] for c in llm}) == 1
    )  # one value, so Ollama loads the model once
    assert (tmp_path / "long-post.mp3").exists()


def test_full_window_is_an_error(llm, tts, tmp_path):
    """If Ollama reports a prompt that fills the window, the prompt was cut. Stop, and write no audio."""
    llm.prompt_tokens = 10**6
    result = invoke(PDF, "--out", tmp_path)
    assert result.exit_code != 0
    assert "--chunk" in result.output
    assert not tts


def test_whole_source_is_covered_without_references(llm, tts, tmp_path):
    """The chunks cover the source from the abstract to the conclusion. The reference list and all after it are cut."""
    run(PDF, "--out", tmp_path)
    source = "".join(c.messages[1]["content"] for c in llm.of("notes"))
    assert "ABSTRACT" in source and "CONCLUSION" in source
    assert not re.search(r"\n#+ \W*References", source, re.I)
    assert "PROOF OF THEOREM" not in source


# --- Script ---


def test_notes_pass_then_one_part_for_each_chunk(llm, tts, tmp_path):
    """All notes come first. Each part call then gets its chunk and the notes of all chunks."""
    run(PDF, "--out", tmp_path)
    notes, parts = llm.of("notes"), llm.of("script")
    n = len(notes)
    assert [c.phase for c in llm[:n]] == ["notes"] * n
    assert len(parts) == n
    for note_call, part_call in zip(notes, parts):
        assert note_call.messages[1]["content"] == part_call.messages[1]["content"]
        assert all(
            f"Notes {k}." in part_call.messages[-1]["content"] for k in range(1, n + 1)
        )
    assert tts[0].script.split("\n\n") == [f"Part {k}." for k in range(1, n + 1)]


def test_each_part_continues_from_the_previous_part(llm, tts, tmp_path):
    """A part call contains the end of the previous part, so a chunk boundary is not audible."""
    run(PDF, "--out", tmp_path)
    parts = llm.of("script")
    for k, call in enumerate(parts[1:], start=1):
        assert f"Part {k}." in call.messages[-1]["content"]


def test_each_part_is_checked_against_its_notes(llm, tts, tmp_path):
    """One check call follows each part. It gets the notes of that chunk and the part, not the source."""
    run(PDF, "--out", tmp_path)
    checks = llm.of("check")
    assert len(checks) == len(llm.of("script"))
    for k, call in enumerate(checks, start=1):
        text = call.messages[-1]["content"]
        assert f"Notes {k}." in text and f"Part {k}." in text
        assert f"Notes {k + 1}." not in text


def test_failed_check_gives_one_rewrite(llm, tts, tmp_path):
    """Problems from the check go back to the writer. The rewrite replaces the part and gets no second check."""
    llm.verdicts = ["- The value of beta is absent."]
    run(PDF, "--out", tmp_path)
    n = len(llm.of("notes"))
    parts = llm.of("script")
    assert len(parts) == n + 1
    assert "The value of beta is absent." in parts[1].messages[-1]["content"]
    assert "Part 1." in parts[1].messages[-1]["content"]
    script = tts[0].script.split("\n\n")
    assert script[0] == "Part 2." and len(script) == n


def test_minutes_sets_the_length_target(llm, tts, tmp_path):
    """The word targets of the parts add up to --minutes of speech."""
    run(PDF, "--out", tmp_path, "--minutes", 12)
    targets = [
        int(re.search(r"(\d+) words", c.messages[-1]["content"]).group(1))
        for c in llm.of("script")
    ]
    assert sum(targets) == pytest.approx(12 * WORDS_PER_MINUTE, rel=0.1)


def test_markup_never_reaches_tts(tts, tmp_path, monkeypatch):
    """Kokoro reads markup aloud. Remove break tags and markdown marks even if the model writes them."""
    dirty = '# Intro\n\nThe **loss** falls. <break time="1.0s" /> Then it stops.'
    monkeypatch.setattr(run_mod, "write_script", lambda *a, **k: dirty)
    run(PDF, "--out", tmp_path)
    assert not re.search(r"[#*<>]", tts[0].script)
    assert "The loss falls." in tts[0].script


# --- Models ---


def test_models_are_cli_arguments(llm, tts, tmp_path):
    """--model reaches Ollama. --voice reaches Kokoro."""
    run(PDF, "--out", tmp_path, "--model", "qwen3:14b", "--voice", "bm_george")
    assert {c.model for c in llm} == {"qwen3:14b"}
    assert tts[0].voice == "bm_george"


@pytest.mark.slow
def test_kokoro_writes_playable_audio(tmp_path):
    """Real Kokoro, no stub: a short sentence becomes an MP3 of more than one second."""
    sf = pytest.importorskip("soundfile")
    pytest.importorskip("kokoro")
    out = tmp_path / "hello.mp3"
    run_mod.speak("The authors train an autoencoder on text chunks.", "af_heart", out)
    assert sf.info(out).duration > 1
