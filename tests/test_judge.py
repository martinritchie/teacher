"""The fact judge for `teacher eval` (judge.py)."""

import json
import re

from teacher.testing import (
    TREE,
    cli,
)


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
