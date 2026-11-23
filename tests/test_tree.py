"""The outline tree (tree.py): top-level sections, recursive splitting, the notes loop, and narrating a node."""

import json

from teacher.testing import (
    LONG,
    TREE,
    block,
    cli,
    outline,
    source_of,
)


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


def test_subsections_are_found_in_order_so_no_text_is_cut_twice(llm, tmp_path):
    """Each subsection is looked for after the one before: a repeated opening phrase finds its next occurrence, and
    a subsection listed out of order is dropped rather than cutting text that another child already holds."""
    doc = f"## 1 Method\n\nStep begins here. {LONG}\n\nStep begins here. {LONG}"
    llm.splits = {
        "1 Method": [("First", "Step begins here."), ("Second", "Step begins here.")]
    }
    _, tree = outline(llm, tmp_path, doc)
    first, second = tree[0]["children"]
    assert first["text"].startswith("Step begins") and second["text"].startswith(
        "Step begins"
    )
    assert tree[0]["text"] + first["text"] + second["text"] == doc
    llm.clear()
    doc = (
        f"## 1 Method\n\nBeta part. {LONG}\n\nGamma part. {LONG}\n\nAlpha part. {LONG}"
    )
    llm.splits = {
        "1 Method": [("A", "Alpha part."), ("B", "Beta part."), ("C", "Gamma part.")]
    }
    _, tree = outline(llm, tmp_path, doc)
    assert not tree[0][
        "children"
    ]  # B and C come before A in the text, so only A is found: one piece, a leaf


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
    tree[0]["text"] = "## 5.3 Batch\n"
    (tmp_path / "x.outline.json").write_text(json.dumps(tree))
    llm.clear()
    cli("write", tmp_path / "x.outline.json", "--node", "5.3", "--out", tmp_path)
    assert len(llm.of("leaf notes")) == 2  # a bare heading is not narrated
