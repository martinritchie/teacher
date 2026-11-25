"""One checked spoken part (part.py): writer, listener, checker, and one rewrite."""

import json

from teacher.testing import (
    PDF,
    block,
    chunk,
    component,
    paragraphs,
    run,
    source_of,
    spelled,
)


def test_each_part_gets_the_glossary_what_was_heard_and_the_previous_part(
    llm, tts, tmp_path
):
    """Every part uses the same names, knows what the listener heard, and continues from the last sentences."""
    llm.components = [component(1, [1]), component(2, [2])]
    run(PDF, "--out", tmp_path, "--no-audio")
    parts = llm.of("method")
    assert all("- the encoder (the paper's E): Encodes." in c.prompt for c in parts)
    assert all("Problem. Before. New." in block(c.prompt, "heard") for c in parts)
    assert block(parts[0].prompt, "previous") == ""
    for k, call in enumerate(parts[1:], start=1):
        assert block(call.prompt, "previous") == f"Part {spelled(k)}."


def test_listener_hears_only_the_narration(llm, tts, tmp_path, checked):
    """The listener gets the earlier parts and this part, never the source or the outline."""
    llm.components = [component(1, [1]), component(2, [2])]
    run(PDF, "--out", tmp_path, "--no-audio")
    notes, listens = llm.of("notes"), llm.of("reconstruct")
    assert [block(c.prompt, "part") for c in listens] == ["Part one.", "Part two."]
    assert block(listens[1].prompt, "heard") == "Part one."
    assert not any(
        chunk(notes[0])[:200] in c.prompt or "Purpose" in c.prompt for c in listens
    )


def test_check_compares_the_pseudocode_with_the_component_and_source(
    llm, tts, tmp_path, checked
):
    """One check per part: it sees the component's steps, its source, the part and the listener's pseudocode."""
    llm.components = [component(1, [2])]
    run(PDF, "--out", tmp_path, "--no-audio")
    check = llm.of("check")[0].prompt
    assert len(llm.of("check")) == len(llm.of("method"))
    assert "1. Detailed step 1." in check and block(check, "pseudocode") == "Code 1."
    assert source_of(llm.of("check")[0]) == chunk(llm.of("notes")[1])
    thinking = {
        p: s["extra_body"]["chat_template_kwargs"]["enable_thinking"]
        for p, s in llm.settings.items()
    }
    assert (
        thinking["check"] and not thinking["reconstruct"]
    )  # the checker thinks; the listener does not


def test_a_check_with_no_valid_answer_counts_as_no_problems(
    llm, tts, tmp_path, checked
):
    """A checker reply that is not a verdict (thinking ran out of tokens) does not end the run: no problems, and the error is in the trace."""
    llm.components = [component(1, [1])]
    llm.verdicts = ["not a verdict", "still not a verdict"]  # the reply and its retry
    run(PDF, "--out", tmp_path, "--no-audio")
    assert len(llm.of("method")) == 1
    trace = (tmp_path / f"{PDF.stem}.trace.jsonl").read_text().splitlines()
    checks = [json.loads(t) for t in trace if '"part/checker"' in t]
    assert "error" in checks[0] and checks[0]["output"] == {"problems": []}
    replies = [
        m for m in checks[0]["messages"] if m["kind"] == "response"
    ]  # the failed attempts are kept
    assert (
        len(replies) == checks[0]["requests"] == len(checks[0]["finish_reasons"]) == 2
    )
    assert "not a verdict" in json.dumps(replies[0])


def test_failed_check_gives_one_rewrite(llm, tts, tmp_path, checked):
    """Problems from the check go back to the writer. The rewrite replaces the part and gets no second check."""
    llm.components = [component(1, [1])]
    llm.verdicts = [["The size of the latent vector is unclear."]]
    run(PDF, "--out", tmp_path)
    parts = llm.of("method")
    assert len(parts) == 2 and len(llm.of("check")) == 1
    assert "- The size of the latent vector is unclear." in parts[1].prompt
    assert block(parts[1].prompt, "draft") == "Part one."
    assert paragraphs(tts)[-1] == "Part two."


def test_symbols_in_a_part_are_problems(llm, tts, tmp_path):
    """Numbers are spelled out in code, with no rewrite; words with symbols left in a part go to the rewrite as a
    problem, with or without the listener and checker."""
    llm.components = [component(1, [1])]
    llm.parts = ["Set K=4 for 99.9% accuracy."]
    run(PDF, "--out", tmp_path, "--no-audio")
    rewrite = llm.of("method")[1].prompt
    assert "K=four" in block(rewrite, "problems")
    assert "ninety-nine point nine percent" in block(rewrite, "draft")
    assert not llm.of("check")  # no listener or checker by default (part.CHECK_PARTS)
