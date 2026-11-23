"""`teacher write` (commands/write.py): narrate one node of an outline tree."""

import json

from teacher.testing import (
    TREE,
    cli,
    source_of,
)


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
