"""Choosing a local judge (commands/judge_bench.py): agreement with recorded Claude verdicts, per verdict."""

import json

from teacher.commands.judge_bench import agreement
from teacher.testing import SMALL_MODEL, cli


def test_agreement_is_reported_per_verdict():
    """A judge that always says "stated" agrees with most of a stated-heavy set, and kappa shows it is no better than chance."""
    rows = agreement(["stated"] * 8 + ["missing", "contradicted"], ["stated"] * 10)
    assert rows[0] == "agreement 0.800, kappa 0.000"
    assert (
        "recall 8/8" in rows[1] and "recall 0/1" in rows[2] and "recall 0/1" in rows[3]
    )


def test_judge_bench_judges_every_recorded_fact_and_lists_disagreements(llm, tmp_path):
    """Every (narration, fact) pair goes through the eval's judge; disagreements are written with both quotes."""
    group = {"narration": "The encoder compresses four tokens.\n\nThe decoder rebuilds them.", "facts": [
        {"fact": "Four tokens are compressed.", "verdict": "stated", "quote": "compresses four tokens"},
        {"fact": "The decoder is a Transformer.", "verdict": "missing", "quote": ""}]}  # fmt: skip
    (tmp_path / "ref.jsonl").write_text(json.dumps(group) + "\n")
    output = cli(
        "judge-bench",
        "--reference",
        tmp_path / "ref.jsonl",
        "--out",
        tmp_path,
    )
    assert (
        len(llm.of("judge")) == 2
    )  # the stub judge says "stated", quoting the narration's first line
    assert (
        "agreement 0.500" in output
        and "missing       Claude    1  candidate    0" in output
    )
    report = (tmp_path / f"{SMALL_MODEL.replace('/', '_')}.md").read_text()
    assert (
        f"## Claude: missing, {SMALL_MODEL}: stated" in report
        and "The decoder is a Transformer." in report
    )
