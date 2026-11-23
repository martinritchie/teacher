"""One checked spoken part about one component of a method, shared by `teacher run` and the outline tree.

The writer narrates the component from its brief; a listener, who hears only the narration, writes pseudocode
from it; a checker compares that with the component and its source. Problems, and any word TTS would read
badly, go back to the writer once.
"""

import re

from pydantic import BaseModel, Field
from pydantic_ai.models import Model

from teacher.llm import Problems, agent, ask, ask_until
from teacher.speech import spell_numbers, unspoken

MAX_PART_WORDS = 300  # a longer part pads; --minutes only ever shortens
# About 4k tokens of source per part; keeps the checker inside its window.
MAX_SOURCE_CHARS = 16000
# Whether a listener and a checker review each part before a rewrite. With CHECK_PARTS False only symbols that code
# cannot spell (1/n, Greek letters) send a part back. Set by evals: see README, "The part loop".
CHECK_PARTS = False


class Term(BaseModel):
    name: str = Field(
        description="The plain name used for this thing everywhere in the episode, e.g. 'the noise level'."
    )
    symbol: str | None = Field(
        description="How the paper writes it, as it is spoken, e.g. 'sigma'. Null if the paper uses no symbol."
    )
    meaning: str


class Detail(BaseModel):
    purpose: str = Field(description="One sentence: why this piece exists.")
    inputs: str = Field(
        description="What comes in, in words, with its rough shape if it has one, e.g. 'one vector per token' or 'the observed data and a prior'. No symbols."
    )
    steps: list[str] = Field(
        description="What it does, one operation per item, in plain words. An equation becomes the operations it performs. No symbols, subscripts or formulas."
    )
    outputs: str = Field(
        description="What comes out, and which other component uses it."
    )


class Component(Detail):
    name: str = Field(description="A name from the glossary.")
    chunks: list[int] = Field(
        description="Numbers of the sections that describe this component, most important first."
    )
    words: int = Field(
        description="Spoken length in words, by how much explaining it needs: about 120 for a simple piece, up to 300 for the most novel one."
    )


class Brief(BaseModel):
    """Everything the writer and checker see for one part."""

    component: Component
    outline: list[Component]  # every component, so the writer knows what not to cover
    source: str
    words: int
    # What the listener heard before the method: the abstract and the contributions.
    heard: str = ""
    glossary: list[Term] = []
    key_numbers: list[str] = []


class Reconstruction(BaseModel):
    pseudocode: str = Field(
        description="Pseudocode for the last part, written from the narration alone."
    )


_writer = agent("part/writer")
_listener = agent("part/listener", Reconstruction)
_checker = agent("part/checker", Problems, thinks=True)


def component(
    name: str, steps: tuple[str, ...] | list[str] = (), words: int = 0
) -> Component:
    """A component known only by name and steps, such as a leaf of the outline tree."""
    return Component(
        name=name,
        purpose="",
        inputs="",
        steps=list(steps),
        outputs="",
        chunks=[],
        words=words,
    )


def write_part(
    brief: Brief, parts: list[str], llm: Model, log: list | None = None
) -> str:
    """The part for `brief`, continuing from `parts`, the parts the listener has heard so far. With `log`, each
    checked draft is added to it with its problems, split into the checker's and the symbol check's."""
    values = dict(brief) | {"previous": _previous(parts)}

    def check(part: str) -> list[str]:
        if not CHECK_PARTS:
            symbols = unspoken(part)
            if log is not None:
                log.append({"draft": part, "checker": [], "symbols": symbols})
            return symbols
        fallback = Reconstruction(pseudocode="UNCLEAR: the listener wrote nothing.")
        heard = "\n\n".join(parts)
        pseudocode = ask(_listener, llm, fallback, heard=heard, part=part).pseudocode
        verdict = ask(
            _checker,
            llm,
            Problems(problems=[]),
            part=part,
            pseudocode=pseudocode,
            **values,
        )
        symbols = unspoken(part)
        if log is not None:
            log.append({"draft": part, "checker": verdict.problems, "symbols": symbols})
        return symbols + verdict.problems

    return ask_until(
        _writer, llm, check, clean=spell_numbers, **values
    ).strip()  # numbers in words without a rewrite


def _previous(parts: list[str]) -> str:
    """The last two sentences the listener heard: enough to continue from, too little to copy."""
    return " ".join(re.split(r"(?<=[.!?])\s+", parts[-1].strip())[-2:]) if parts else ""
