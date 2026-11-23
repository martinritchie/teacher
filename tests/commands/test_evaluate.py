"""`teacher eval` (commands/evaluate.py): narrate fixed cases and judge them fact by fact."""

import json
import re

from teacher.settings import (
    JUDGE_MODEL,
)
from teacher.testing import (
    SMALL_MODEL,
    TREE,
    block,
    cli,
)


def test_eval_scores_each_case_against_its_facts(llm, tmp_path):
    """`teacher eval` narrates each case's node and judges it one fact per call; the table counts the verdicts and the report keeps the narration."""
    (tmp_path / "x.outline.json").write_text(json.dumps(TREE))
    cases = [{"tree": str(tmp_path / "x.outline.json"), "node": "Encoder", "facts": ["It maps tokens.", "It is small."]},
             {"tree": str(tmp_path / "x.outline.json"), "node": "Loss", "facts": ["Two terms."]}]  # fmt: skip
    (tmp_path / "cases.json").write_text(json.dumps(cases))
    llm.verdict = "missing"
    output = cli("eval", tmp_path / "cases.json", "--note-rounds", 0, "--out", tmp_path)
    assert re.search(r"Encoder +0/2 +0.0 +0 +0 +2 +0", output) and re.search(
        r"total +0/3", output
    )
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
    cli(
        "eval",
        tmp_path / "cases.json",
        "--only",
        "loss",
        "--note-rounds",
        0,
        "--out",
        tmp_path,
    )
    assert len(llm.of("judge")) == 2  # the final narration and the first drafts


def test_eval_judges_with_the_fixed_judge_whatever_narrates(llm, tmp_path):
    """The narration comes from --model; every judge call goes to settings.JUDGE_MODEL, served after the narration
    is done, and the report says which is which."""
    (tmp_path / "x.outline.json").write_text(json.dumps(TREE))
    cases = [{"tree": str(tmp_path / "x.outline.json"), "node": "Encoder", "facts": ["It maps tokens."]}]  # fmt: skip
    (tmp_path / "cases.json").write_text(json.dumps(cases))
    output = cli("eval", tmp_path / "cases.json", "--note-rounds", 0, "--out", tmp_path)
    assert {c.model for c in llm.of("judge")} == {JUDGE_MODEL} and llm.started == 2
    assert {c.model for c in llm if c.phase != "judge"} == {SMALL_MODEL}
    assert max(llm.index(c) for c in llm if c.phase != "judge") < llm.index(
        llm.of("judge")[0]
    )
    assert f"narrated by {SMALL_MODEL}, judged by {JUDGE_MODEL}" in output


def test_a_judge_that_is_the_narrator_uses_its_server(llm, tmp_path):
    """When --judge names the narrating model, the eval starts one server for both; Claude stays available."""
    (tmp_path / "x.outline.json").write_text(json.dumps(TREE))
    cases = [{"tree": str(tmp_path / "x.outline.json"), "node": "Encoder", "facts": ["It maps tokens."]}]  # fmt: skip
    (tmp_path / "cases.json").write_text(json.dumps(cases))
    cli(
        "eval",
        tmp_path / "cases.json",
        "--note-rounds",
        0,
        "--out",
        tmp_path,
        "--judge",
        SMALL_MODEL,
    )
    assert llm.started == 1 and {c.model for c in llm} == {SMALL_MODEL}
    llm.clear()
    cli(
        "eval",
        tmp_path / "cases.json",
        "--out",
        tmp_path,
        "--judge",
        "claude-sonnet-5-5",
    )
    assert {c.model for c in llm.of("judge")} == {"claude-sonnet-5-5"}


def test_repeat_runs_every_case_several_times_at_once(llm, tmp_path):
    """--repeat N narrates and judges every case N times in one go; the table shows each run's score and the mean."""
    (tmp_path / "x.outline.json").write_text(json.dumps(TREE))
    cases = [{"tree": str(tmp_path / "x.outline.json"), "node": n, "facts": ["A.", "B."]} for n in ("Encoder", "Loss")]  # fmt: skip
    (tmp_path / "cases.json").write_text(json.dumps(cases))
    output = cli(
        "eval",
        tmp_path / "cases.json",
        "--note-rounds",
        0,
        "--out",
        tmp_path,
        "--repeat",
        2,
    )
    assert len(llm.of("judge")) == 2 * 2 * 2 * 2  # cases, facts, runs, final and draft
    assert re.search(r"Encoder +2/2 2/2", output) and re.search(
        r"total +4/4 4/4  mean 4.0", output
    )
    assert (
        "2 run(s)" in output
        and "## Loss (run 2)" in next(tmp_path.glob("*.md")).read_text()
    )


def test_eval_scores_the_first_drafts_and_reports_the_checks_and_their_cost(
    llm, tmp_path
):
    """To see what the loop adds: the parts as first drafted are judged on the same facts, the table counts the
    parts the check sent back and its problems, the report lists them, and each agent's calls and time are shown."""
    (tmp_path / "x.outline.json").write_text(json.dumps(TREE))
    cases = [{"tree": str(tmp_path / "x.outline.json"), "node": "Encoder", "facts": ["It maps tokens."]}]  # fmt: skip
    (tmp_path / "cases.json").write_text(json.dumps(cases))
    llm.verdicts = [["The listener could not tell what is encoded."]]
    output = cli("eval", tmp_path / "cases.json", "--note-rounds", 0, "--out", tmp_path)
    drafts = [block(c.prompt, "narration") for c in llm.of("judge")]
    assert drafts == ["Part two.", "Part one."]  # the rewrite, then the first draft
    assert (
        re.search(r"Encoder +1/1 +1.0 +0 +0 +0 +0 +0 +1/1 +1 +0", output)
        and "drafts 1.0" in output
    )
    assert re.search(r"part/checker +1 ", output) and re.search(
        r"part/writer +2 ", output
    )
    report = next(tmp_path.glob("*.md")).read_text()
    assert "Checker, part 1: The listener could not tell what is encoded." in report
