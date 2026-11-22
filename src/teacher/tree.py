"""The outline tree: a source broken into headings and subheadings the way a reader would by hand, and
narrated leaf by leaf.

Building: the top level is the source's own top-level sections, found from heading numbers. Then, recursively,
a splitter reads each section and lists its subsections (a title and the exact words each starts with, nothing
else); code cuts the text at those words, and each piece is broken down in turn, until it is one idea.

Narrating: each leaf gets notes, checked against its text by a separate verifier and revised until it finds
nothing; then a checked part is written from them (see part.py).
"""

import json
import re
from pathlib import Path

import typer
from pydantic import BaseModel, Field
from pydantic_ai.models import Model

from teacher.llm import Problems, agent, ask, ask_until, parallel
from teacher.part import MAX_PART_WORDS, MAX_SOURCE_CHARS, Brief, component, write_part

MAX_DEPTH = 4  # levels below the top-level sections
MIN_SPLIT_CHARS = 1500  # shorter text is one idea
MIN_OWN_CHARS = (
    300  # a parent's own text longer than this is narrated before its children
)
MAX_SPLIT_CHARS = 28000  # about 7k tokens; longer text is split at its own headings
NOTE_ROUNDS = 3  # verify-and-revise rounds for a leaf's notes
WORDS_PER_NOTE = 30  # a leaf's spoken length follows how much there is to say
_NUMBER = r"(\d+(?:\.\d+)*|[A-Z](?:\.\d+)+|[A-Z](?=\.))"  # 3, 3.3.1, A.1, A.


class Node(BaseModel):
    title: str
    text: str = Field(
        description="Its own text: all of it for a leaf, the part before its first child otherwise."
    )
    children: list["Node"] = []


class Subsection(BaseModel):
    title: str = Field(description="A short title naming the idea, like a heading.")
    starts_with: str = Field(
        description="The first eight or so words of the subsection, copied exactly from the text."
    )


class Split(BaseModel):
    subsections: list[Subsection] = Field(
        description="The subsections in order. Empty if the text is about one idea."
    )


class Notes(BaseModel):
    notes: list[str] = Field(
        description="One fact per item, in the order of the passage, in plain words with numbers in words."
    )


_splitter = agent("tree/splitter", Split, thinks=True)
_note_taker = agent("tree/note_taker", Notes)
_notes_verifier = agent("tree/notes_verifier", Problems, thinks=True)


def build_tree(markdown: str, llm: Model) -> list[Node]:
    return parallel(lambda s: _node(_title(s), s, [], llm), _top_sections(markdown))


def render_tree(nodes: list[Node], depth: int = 0) -> str:
    """The headings alone, as a nested list."""
    return "".join(
        f"{'  ' * depth}- {n.title}\n" + render_tree(n.children, depth + 1)
        for n in nodes
    )


def load_tree(path: Path) -> list[Node]:
    return [Node.model_validate(n) for n in json.loads(path.read_text())]


def find_node(tree: list[Node], title: str) -> Node:
    """The first node, depth first, whose title contains `title` (case ignored)."""
    for node, _ in _walk(tree, tree):
        if title.lower() in node.title.lower():
            return node
    raise typer.BadParameter(f"No node titled like {title!r}")


def narrate(
    node: Node, llm: Model, heard: str = "", rounds: int = NOTE_ROUNDS
) -> list[str]:
    """One checked spoken part per leaf under `node`, in order, and one for any parent whose own text, before its
    first child, is more than a heading or a line. Notes for all parts are taken at once; parts are written in
    order, since each continues from the last."""
    leaves = [(n, siblings) for n, siblings in _walk([node], [node]) if not n.children or len(n.text.strip()) > MIN_OWN_CHARS]  # fmt: skip
    sources = [leaf.text[:MAX_SOURCE_CHARS] for leaf, _ in leaves]
    all_notes = parallel(lambda i: take_notes(leaves[i][0].title, sources[i], llm, rounds), range(len(leaves)))  # fmt: skip
    parts: list[str] = []
    for (leaf, siblings), source, notes in zip(leaves, sources, all_notes):
        words = max(min(WORDS_PER_NOTE * len(notes), MAX_PART_WORDS), 80)
        brief = Brief(
            component=component(leaf.title, notes, words),
            outline=[component(s.title) for s in siblings],
            source=source,
            words=words,
            heard=heard,
        )
        parts.append(write_part(brief, parts, llm))
    return parts


def take_notes(
    title: str, source: str, llm: Model, rounds: int = NOTE_ROUNDS
) -> list[str]:
    """Notes on a passage; then, up to `rounds` times, a separate verifier lists what they miss or get wrong
    against the source and the note-taker revises. Stops early when the verifier finds nothing."""

    def check(notes: Notes) -> list[str]:
        empty = Problems(problems=[])
        return ask(
            _notes_verifier, llm, empty, source=source, notes=notes.notes
        ).problems

    return ask_until(
        _note_taker, llm, check, rounds + 1, title=title, source=source
    ).notes


def _node(title: str, text: str, path: list[str], llm: Model) -> Node:
    if len(path) >= MAX_DEPTH or len(text) < MIN_SPLIT_CHARS:
        return Node(title=title, text=text)
    if len(text) > MAX_SPLIT_CHARS:  # too long for one call: cut at its own headings
        cuts = [(_title(m.group()), m.start()) for m in re.finditer(r"(?m)^#.*$", text) if m.start()]  # fmt: skip
    else:
        empty = Split(subsections=[])
        split = ask(_splitter, llm, empty, path=[*path, title], text=text)
        cuts = [(s.title, _find(text, s.starts_with)) for s in split.subsections]
    cuts = [(t, at) for t, at in cuts if at is not None and t.lower() != title.lower()]
    cuts = [
        c for i, c in enumerate(cuts) if not i or c[1] > cuts[i - 1][1]
    ]  # in order, no overlaps
    if len(cuts) < 2:
        return Node(title=title, text=text)
    ends = [at for _, at in cuts[1:]] + [len(text)]
    pieces = [(t, text[at:end]) for (t, at), end in zip(cuts, ends)]
    children = parallel(lambda p: _node(*p, [*path, title], llm), pieces)
    return Node(title=title, text=text[: cuts[0][1]], children=children)


def _walk(nodes: list[Node], siblings: list[Node]):
    """Every node depth first, with the list it belongs to."""
    for node in nodes:
        yield node, siblings
        yield from _walk(node.children, node.children)


def _top_sections(markdown: str) -> list[str]:
    """Text from each top-level heading (unnumbered, or a number with no dot such as 3 or A.) to the next."""
    sections: list[str] = []
    for part in re.split(r"(?m)^(?=#)", markdown):
        number = re.match(rf"#+\s*{_NUMBER}", part)
        nested = number and "." in number.group(1).rstrip(".")
        if sections and (nested or not part.strip()):
            sections[-1] += part
        elif part.strip():
            sections.append(part)
    return sections


def _title(text: str) -> str:
    return text.strip().splitlines()[0].lstrip("# ").strip() if text.strip() else ""


def _find(text: str, words: str) -> int | None:
    """Where the quoted opening words start, ignoring spacing; snapped to the start of a heading line."""
    for n in (8, 4):
        pattern = r"\s+".join(map(re.escape, words.lstrip("# ").split()[:n]))
        match = pattern and re.search(pattern, text)
        if match:
            line = text.rfind("\n", 0, match.start()) + 1
            return line if not text[line : match.start()].strip("# ") else match.start()
    return None
