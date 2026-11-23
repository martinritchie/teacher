"""The script of a `teacher run` episode (episode.py). No server is started: the script model is a pydantic-ai FunctionModel, and speech is a stub (see tests/conftest.py); the real tokenizer is in a functional test.

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
7. Join abstract, contributions, an overview sentence and the parts; remove markup, split into paragraphs, and speak."""

import pytest

import teacher.episode as episode

from teacher.settings import SCRIPT_MODEL, WORDS_PER_MINUTE
from teacher.testing import (
    CONTRIBUTIONS,
    PDF,
    PDF_MARKDOWN,
    SMALL_MODEL,
    block,
    chunk,
    component,
    invoke,
    paragraphs,
    run,
    source_of,
    targets,
)


def test_chunk_sets_the_source_tokens_for_each_call(
    llm, tts, tmp_path, unit, episode_run
):
    """--chunk is the quality limit, counted with the model's tokenizer (here, a word count). Sections over it are split, so a smaller value gives more chunks than the default."""
    run(PDF, "--out", tmp_path, "--chunk", 150)
    small = llm.of("notes")
    assert all(len(chunk(c).split()) <= 150 for c in small) and unit == [SMALL_MODEL]
    assert 1 < len(episode_run.llm.of("notes")) < len(small)


@pytest.mark.functional
def test_chunks_fit_the_real_tokenizer():
    """The script model's real tokenizer, from the Hugging Face cache, keeps every chunk of the paper within --chunk."""
    from transformers import AutoTokenizer

    from teacher.episode import split_into_chunks

    tokens = AutoTokenizer.from_pretrained(SMALL_MODEL)
    chunks = split_into_chunks(PDF_MARKDOWN.read_text(), SMALL_MODEL, 500)
    assert len(chunks) > 30 and all(len(tokens.encode(c)) <= 500 for c in chunks)


def test_chunks_are_the_sources_sections(episode_run):
    """Each chunk is one section of the source, starting with its heading; a heading with no text of its own joins the next. The outline sees every heading."""
    llm = episode_run.llm
    notes, outline = llm.of("notes"), llm.of("outline")[0].prompt
    assert chunk(notes[0]).startswith(
        "# CONTINUOUS AUTOREGRESSIVE LANGUAGE MODELS\n\n## ABSTRACT"
    )  # a bare title
    assert "## 1 INTRODUCTION" not in chunk(notes[0])
    assert chunk(notes[1]).startswith("## 1 INTRODUCTION")
    assert 'heading="CONTINUOUS AUTOREGRESSIVE LANGUAGE MODELS / ABSTRACT"' in outline
    assert 'heading="2 AUTOENCODER / 2.1 HIGH-FIDELITY RECONSTRUCTION"' in outline


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


def test_abstract_is_transcribed_from_the_abstract_alone(episode_run):
    """The abstract reader sees only the text under the abstract heading, and its transcription opens the script."""
    llm, tts = episode_run.llm, episode_run.tts
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
    assert "<problems>" not in first.prompt and "<draft>" not in first.prompt
    assert "99.9%" in block(second.prompt, "problems")
    assert block(second.prompt, "draft") == block(
        first.prompt, "abstract"
    )  # the version to fix


def test_contributions_see_the_abstract_introduction_and_conclusion(episode_run):
    """The contributions writer hears the abstract as spoken and reads the introduction and the conclusion."""
    llm, tts = episode_run.llm, episode_run.tts
    prompt = llm.of("contributions")[0].prompt
    assert paragraphs(tts)[0] in block(prompt, "heard")
    assert block(prompt, "introduction") and block(prompt, "conclusion")


def test_contributions_with_symbols_are_written_again(llm, tts, tmp_path):
    """Words with digits or symbols in the contributions go back as a problem, once."""
    llm.contributions = [{**CONTRIBUTIONS, "context": "Over 99.9% of it."}]
    run(PDF, "--out", tmp_path)
    first, second = llm.of("contributions")
    assert "<problems>" not in first.prompt and "99.9%" in block(
        second.prompt, "problems"
    )
    assert "Over 99.9% of it." not in tts[0].script


def test_outline_sees_every_note_and_what_was_heard(episode_run):
    """All notes come before the outline, which sees every note and the abstract and contributions."""
    llm = episode_run.llm
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
    """Before the parts are written, every component's mechanism is rewritten from its sections, all at once; the writer and checker get the rewrite. Name, sections and words stay the outline's."""
    llm.components = [component(1, [3]), component(2, [2])]
    run(PDF, "--out", tmp_path)
    notes, details, parts = llm.of("notes"), llm.of("detail"), llm.of("method")
    assert [source_of(d) for d in details] == [chunk(notes[2]), chunk(notes[1])]
    assert (
        "1. Step 2." in details[1].prompt
        and "- piece 1: Purpose 1." in details[1].prompt
    )
    assert llm.index(details[-1]) < llm.index(
        parts[0]
    )  # every rewrite at once, before the first part
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


def test_part_sources_stop_at_the_size_limit(llm, tts, tmp_path, monkeypatch):
    """A component that names many sections gets them in order, up to MAX_SOURCE_CHARS (about four thousand tokens), so the writer and checker stay inside their window."""
    monkeypatch.setattr(
        episode, "MAX_SOURCE_CHARS", 3000
    )  # the short paper is under the real limit
    llm.components = [component(1, list(range(1, 30)))]
    run(PDF, "--out", tmp_path)
    source = source_of(llm.of("method")[0])
    assert source.startswith(chunk(llm.of("notes")[0])) and 1500 < len(source) <= 3000


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


def test_only_the_outline_and_check_think(episode_run):
    """Thinking is on for the outline and the check and off for everything else, each with Qwen3's sampling for its mode."""
    llm = episode_run.llm
    thinks = {p: s["extra_body"]["chat_template_kwargs"]["enable_thinking"] for p, s in llm.settings.items()}  # fmt: skip
    assert thinks == {"abstract": False, "contributions": False, "notes": False, "outline": True, "detail": True, "method": False, "reconstruct": False, "check": True}  # fmt: skip


def test_run_with_a_claude_model_chunks_with_the_local_tokenizer(
    llm, tts, tmp_path, unit
):
    """An API model has no local tokenizer: chunking for a Claude run counts tokens with the local script model's."""
    result = invoke(
        PDF, "--out", tmp_path, "--model", "claude-sonnet-5-5", "--no-audio"
    )
    assert result.exit_code == 0, result.output
    assert llm.started == 0 and {c.model for c in llm} == {
        "claude-sonnet-5-5"
    }  # no vLLM server was started
    assert unit == [SCRIPT_MODEL]
