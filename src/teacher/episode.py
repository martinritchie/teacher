"""The script of a `teacher run` episode, in three parts, each told everything the listener has already heard:
1. the abstract, transcribed for the ear;
2. the contributions, for a listener who knows ML but not this subfield;
3. how it works: notes on every section, one planner call that outlines the method as components, then for
   each component a detail pass over the full text of its sections and a checked part (see part.py).
"""

import re
from pathlib import Path

import semchunk
from pydantic import BaseModel, Field
from pydantic_ai.models import Model

from teacher.llm import agent, ask, ask_until, parallel, start_trace
from teacher.part import (
    MAX_PART_WORDS,
    MAX_SOURCE_CHARS,
    Brief,
    Component,
    Detail,
    Term,
    write_part,
)
from teacher.settings import THINKING, WORDS_PER_MINUTE
from teacher.speech import unspoken

MAX_SECTION_CHARS = 12000  # about 3k tokens of abstract, introduction or conclusion
MIN_OVERLAP = 0.8  # share of the abstract's words the transcription must keep
SPOKEN = "Plain spoken English: no symbols, LaTeX or markup; numbers and acronyms as they are said."


class Abstract(BaseModel):
    text: str = Field(
        description=f"The abstract, sentence for sentence. Change only what cannot be spoken. {SPOKEN}"
    )


class Contribution(BaseModel):
    problem: str = Field(
        description=f"The problem this contribution addresses, in one or two sentences. {SPOKEN}"
    )
    before: str = Field(
        description=f"What people did before, and where it fell short. {SPOKEN}"
    )
    new: str = Field(
        description=f"What the authors do differently, and why that helps. {SPOKEN}"
    )


class Contributions(BaseModel):
    context: str = Field(
        description=f"The background the abstract takes for granted, for someone who knows ML broadly but not this area. Do not restate the abstract. {SPOKEN}"
    )
    items: list[Contribution] = Field(
        description="One to four contributions, in the order the paper gives them."
    )

    def spoken(self) -> list[str]:
        return [self.context, *(f"{i.problem} {i.before} {i.new}" for i in self.items)]


class Method(BaseModel):
    glossary: list[Term] = Field(
        description="Every quantity, module or procedure the method names. All later parts use these names only."
    )
    components: list[Component] = Field(
        description="Two to seven, in the order someone implementing the method would build them."
    )
    key_numbers: list[str] = Field(
        description="Only values a first implementation needs, each written in words with what it controls, e.g. 'four tokens per vector'."
    )


_abstract_reader = agent("episode/abstract", Abstract)
_contributions_writer = agent("episode/contributions", Contributions)
_section_notes = agent("plan/section_notes")
_planner = agent("plan/planner", Method, THINKING)
_detailer = agent("plan/detailer", Detail, THINKING)


def split_into_chunks(markdown: str, model: str, max_tokens: int) -> list[str]:
    """The source's sections, each starting with its heading, split further only where one is over
    `max_tokens` (counted with the script model's tokenizer)."""
    sections: list[str] = []
    for s in re.split(r"(?m)^(?=#)", markdown):
        heading_only = sections and "\n" not in sections[-1].strip()
        sections[-1:] = [sections[-1] + s] if heading_only else [*sections[-1:], s]
    split = semchunk.chunkerify(model, max_tokens)
    return [c for s in sections if s.strip() for c in split(s.strip())]


def write_episode(
    markdown: str, chunks: list[str], llm: Model, minutes: int, trace: Path
) -> str:
    """The script; every call's prompt and output go to `trace`, for tuning the prompts."""
    start_trace(trace)
    abstract = _read_abstract(_section(markdown, "abstract"), llm)
    contributions = ask_until(
        _contributions_writer,
        llm,
        lambda c: unspoken(" ".join(c.spoken())),
        heard=abstract,
        introduction=_section(markdown, "introduction") or chunks[0],
        conclusion=_section(markdown, "conclusions?"),
    )
    heard = "\n\n".join(filter(None, [abstract, *contributions.spoken()]))
    notes = parallel(lambda c: ask(_section_notes, llm, chunk=c), chunks)
    headings = [_headings(c) for c in chunks]
    method = ask(_planner, llm, notes=notes, headings=headings, heard=heard)
    budget = minutes * WORDS_PER_MINUTE - len(heard.split())
    parts = _how_it_works(method, chunks, heard, budget, llm)
    return "\n\n".join([heard, _overview(method), *parts])


def _read_abstract(abstract: str, llm: Model) -> str:
    """The abstract for the ear, read again once if the transcription strays from the original words or
    keeps symbols."""
    if not abstract:
        return ""

    def check(a: Abstract) -> list[str]:
        strays = _overlap(abstract, a.text) < MIN_OVERLAP
        return unspoken(a.text) + strays * [
            "Keep every sentence, in the authors' words."
        ]

    return ask_until(_abstract_reader, llm, check, abstract=abstract).text


def _how_it_works(
    method: Method, chunks: list[str], heard: str, budget: int, llm: Model
) -> list[str]:
    """One checked part per component, its mechanism first rewritten from its sections. Word targets are
    the planner's, shrunk to fit `budget` and capped."""
    scale = min(1, max(budget, 0) / max(sum(c.words for c in method.components), 1))
    parts: list[str] = []
    for c in method.components:
        source = _source(c.chunks, chunks)
        fallback = Detail(**c.model_dump(include=set(Detail.model_fields)))
        detail = ask(_detailer, llm, fallback, glossary=method.glossary, outline=method.components, component=c, source=source)  # fmt: skip
        brief = Brief(
            component=c.model_copy(update=detail.model_dump()),
            outline=method.components,
            source=source,
            words=max(min(round(c.words * scale), MAX_PART_WORDS), 80),
            heard=heard,
            glossary=method.glossary,
            key_numbers=method.key_numbers,
        )
        parts.append(write_part(brief, parts, llm))
    return parts


def _source(numbers: list[int], chunks: list[str]) -> str:
    """The sections a component names, in its order, while they fit in MAX_SOURCE_CHARS. Invented numbers
    are dropped."""
    picked: list[str] = []
    for n in dict.fromkeys(n for n in numbers if 1 <= n <= len(chunks)):
        if picked and sum(map(len, picked)) + len(chunks[n - 1]) > MAX_SOURCE_CHARS:
            break
        picked.append(chunks[n - 1])
    return "\n\n".join(picked)[:MAX_SOURCE_CHARS]


def _headings(chunk: str) -> str:
    """Every heading in a section, e.g. "3.3 ENERGY TRANSFORMER / 3.3.1 SCORING RULES"; a split section's
    later pieces have none."""
    found = [line.lstrip("# ") for line in chunk.splitlines() if line.startswith("#")]
    return " / ".join(found) or "(continued)"


def _overview(method: Method) -> str:
    names = [c.name for c in method.components]
    listed = f"{', '.join(names[:-1])} and {names[-1]}" if len(names) > 1 else names[0]
    return (
        f"Here is how it works. The method has {_number(len(names))} pieces: {listed}."
    )


def _section(markdown: str, name: str) -> str:
    """The text under the heading `name` (a regex; numbering and case ignored), up to the next heading."""
    match = re.search(rf"(?ims)^#+\s*[\d.]*\s*{name}\b[^\n]*$(.*?)(?=^#|\Z)", markdown)
    return match.group(1).strip()[:MAX_SECTION_CHARS] if match else ""


def _overlap(original: str, spoken: str) -> float:
    words = lambda s: set(re.findall(r"[a-z]{3,}", s.lower()))  # noqa: E731
    return len(words(original) & words(spoken)) / max(len(words(original)), 1)


def _number(n: int) -> str:
    return "one two three four five six seven eight nine ten".split()[n - 1] if 0 < n <= 10 else str(n)  # fmt: skip
