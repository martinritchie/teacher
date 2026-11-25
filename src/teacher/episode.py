"""The script of a `teacher run` episode, in chapters, each told everything the listener has already heard:
1. an introduction: what the work is about, in the episode's own words (the abstract is the authors' text, so it
   is paraphrased, never read out);
2. the authors, grouped by institution, and anyone the front page thanks;
3. the contributions, for a listener who knows ML but not this subfield;
4. how it works: notes on every section, one planner call that outlines the method as components, then for
   each component a detail pass over the full text of its sections and a checked part (see part.py), one
   chapter each.
The script is Markdown: a `## ` heading starts each chapter, and every other block is a spoken paragraph.
"""

import re
from typing import Any

import semchunk
from pydantic import BaseModel, Field
from pydantic_ai.models import Model

from teacher.llm import agent, ask, ask_until, parallel
from teacher.part import (
    MAX_PART_WORDS,
    MAX_SOURCE_CHARS,
    Brief,
    Component,
    Detail,
    Term,
    write_part,
)
from teacher.settings import SCRIPT_MODEL, WORDS_PER_MINUTE
from teacher.tts import unspoken

MAX_SECTION_CHARS = 12000  # about 3k tokens of abstract, introduction or conclusion
COPIED_WORDS = 8  # a run of this many words taken from the abstract is a quotation, not a paraphrase
MAX_NAMED = 10  # authors named per institution; the rest are counted
SPOKEN = "Plain spoken English: no symbols, LaTeX or markup; numbers and acronyms as they are said."


class Introduction(BaseModel):
    text: str = Field(
        description=f"What the work is about and why it matters, in your own words, about as long as the abstract. {SPOKEN}"
    )


class Affiliation(BaseModel):
    institution: str = Field(
        description=f"The institution as it would be said aloud, e.g. 'WeChat AI, at Tencent'. {SPOKEN}"
    )
    authors: list[str] = Field(
        description="Full names exactly as printed, in the paper's order."
    )


class Credits(BaseModel):
    affiliations: list[Affiliation] = Field(
        description="Every institution on the front page, in the order of its first author. An author with several appears under each."
    )
    thanks: str = Field(
        description=f"If the front page explicitly thanks people or organisations, one or two sentences saying whom and for what. Empty if it thanks no one. {SPOKEN}"
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
        min_length=1,
        description="Two to seven, in the order someone implementing the method would build them.",
    )
    key_numbers: list[str] = Field(
        description="Only values a first implementation needs, each written in words with what it controls, e.g. 'four tokens per vector'."
    )


_introducer = agent("episode/introduction", Introduction)
_credits_reader = agent("episode/credits", Credits)
_contributions_writer = agent("episode/contributions", Contributions)
_section_notes = agent("episode/section_notes")
_planner = agent("episode/planner", Method, thinks=True)
_detailer = agent("episode/detailer", Detail, thinks=True)


def split_into_chunks(markdown: str, model: str, max_tokens: int) -> list[str]:
    """The source's sections, each starting with its heading, split further only where one is over
    `max_tokens` (counted with the script model's tokenizer)."""
    sections: list[str] = []
    for s in re.split(r"(?m)^(?=#)", markdown):
        heading_only = sections and "\n" not in sections[-1].strip()
        sections[-1:] = [sections[-1] + s] if heading_only else [*sections[-1:], s]
    tokenizer = (
        SCRIPT_MODEL if model.startswith("claude-") else model
    )  # an API model has no local tokenizer
    split: Any = semchunk.chunkerify(tokenizer, max_tokens)
    return [c for s in sections if s.strip() for c in split(s.strip())]


def write_episode(
    markdown: str, front: str, chunks: list[str], llm: Model, minutes: int
) -> str:
    """The script, as Markdown chapters; every call goes to the trace, if one is open (llm.start_trace). The
    section notes are written while the opening is, since they do not depend on what was heard."""

    def opening() -> list[tuple[str, str]]:
        abstract = _section(markdown, "abstract") or chunks[0][:MAX_SECTION_CHARS]
        introduction = _introduce(abstract, llm)
        contributions = ask_until(
            _contributions_writer,
            llm,
            lambda c: unspoken(" ".join(c.spoken())),
            heard=introduction,
            introduction=_section(markdown, "introduction") or chunks[0],
            conclusion=_section(markdown, "conclusions?"),
        )
        return [("Introduction", introduction), ("Authors", _credits(front, llm)),
                ("Contributions", "\n\n".join(contributions.spoken()))]  # fmt: skip

    def all_notes() -> list[str]:
        return parallel(lambda c: ask(_section_notes, llm, chunk=c), chunks)

    chapters, notes = parallel(lambda job: job(), [opening, all_notes])
    heard = "\n\n".join(text for _, text in chapters)
    headings = [_headings(c) for c in chunks]
    method = ask(_planner, llm, notes=notes, headings=headings, heard=heard)
    budget = minutes * WORDS_PER_MINUTE - len(heard.split())
    parts = _how_it_works(method, chunks, heard, budget, llm)
    parts[0] = f"{_overview(method)}\n\n{parts[0]}"
    chapters += [(c.name[:1].upper() + c.name[1:], p) for c, p in zip(method.components, parts)]  # fmt: skip
    return "\n\n".join(f"## {title}\n\n{text}" for title, text in chapters if text)


def _introduce(abstract: str, llm: Model) -> str:
    """What the work is about, from its abstract but in other words: written again once if it copies a run of
    the abstract's words or keeps symbols."""

    def check(i: Introduction) -> list[str]:
        copied, announced = (
            _copied(abstract, i.text),
            re.match(r"[^.\n]*:\s*\n", i.text),
        )
        return (
            unspoken(i.text)
            + bool(announced)
            * [
                f'Start with the content itself: "{announced and announced.group().strip()}" would be read aloud.'
            ]
            + bool(copied)
            * [
                f'These words are copied from the abstract: "{copied}". Say it in your own words.'
            ]
        )

    return ask_until(_introducer, llm, check, abstract=abstract).text


def _credits(front: str, llm: Model) -> str:
    """The authors, grouped by institution, then whom the front page thanks. Asked again once if it names
    someone not on the page."""
    if not front.strip():
        return ""
    page = re.sub(r"\W+", " ", front.lower())

    def check(c: Credits) -> list[str]:
        names = [n for a in c.affiliations for n in a.authors]
        absent = [
            n for n in names if re.sub(r"\W+", " ", n.lower()).strip() not in page
        ]
        return absent and [f"Not on the front page: {', '.join(absent)}. Copy names exactly as printed."]  # fmt: skip

    credits = ask_until(_credits_reader, llm, check, front=front)
    everyone = list(dict.fromkeys(n for a in credits.affiliations for n in a.authors))
    # an author's own name or a web address is not an institution (a blog post often names none)
    places = [a for a in credits.affiliations if a.authors and a.institution.strip() and a.institution not in everyone and not re.search(r"\.\w", a.institution)]  # fmt: skip
    named: set[str] = set()
    lines = [] if places or not everyone else [f"The authors are {_listed(_capped(everyone))}." if len(everyone) > 1 else f"The author is {everyone[0]}."]  # fmt: skip
    for a in places:
        names = _capped(a.authors)
        also = " also" if set(a.authors) <= named else ""
        lines.append(
            f"{_listed(names)} {'are' if len(names) > 1 else 'is'}{also} at {a.institution}."
        )
        named |= set(a.authors)
    thanks = (
        credits.thanks if re.search(r"thank|grateful|acknowledg", front, re.I) else ""
    )
    return "\n\n".join(filter(None, [" ".join(lines), thanks]))


def _how_it_works(
    method: Method, chunks: list[str], heard: str, budget: int, llm: Model
) -> list[str]:
    """One checked part per component, its mechanism first rewritten from its sections. The rewrites run at
    once, as none depends on another or on a part; the parts are written in order, each continuing the last.
    Word targets are the planner's, shrunk to fit `budget` and capped."""
    scale = min(1, max(budget, 0) / max(sum(c.words for c in method.components), 1))

    def detailed(c: Component) -> Detail:
        fallback = Detail(**c.model_dump(include=set(Detail.model_fields)))
        return ask(_detailer, llm, fallback, glossary=method.glossary, outline=method.components, component=c, source=_source(c.chunks, chunks))  # fmt: skip

    parts: list[str] = []
    for c, detail in zip(method.components, parallel(detailed, method.components)):
        source = _source(c.chunks, chunks)
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
    return f"Here is how it works. The method has {_number(len(names))} piece{'s' * (len(names) > 1)}: {_listed(names)}."


def _capped(names: list[str]) -> list[str]:
    return names[:MAX_NAMED] + [f"{_number(len(names) - MAX_NAMED)} others"] * (len(names) > MAX_NAMED)  # fmt: skip


def _listed(items: list[str]) -> str:
    return f"{', '.join(items[:-1])} and {items[-1]}" if len(items) > 1 else items[0]


def _section(markdown: str, name: str) -> str:
    """The text under the heading `name` (a regex; numbering and case ignored), up to the next heading."""
    match = re.search(rf"(?ims)^#+\s*[\d.]*\s*{name}\b[^\n]*$(.*?)(?=^#|\Z)", markdown)
    return match.group(1).strip()[:MAX_SECTION_CHARS] if match else ""


def _copied(original: str, spoken: str) -> str:
    """The first run of COPIED_WORDS words of `spoken` that is also in `original`, or ""."""
    words = lambda s: re.findall(r"[a-z0-9]+", s.lower())  # noqa: E731
    source, said = " " + " ".join(words(original)) + " ", words(spoken)
    runs = (
        " ".join(said[i : i + COPIED_WORDS])
        for i in range(len(said) - COPIED_WORDS + 1)
    )
    return next((r for r in runs if f" {r} " in source), "")


def _number(n: int) -> str:
    return "one two three four five six seven eight nine ten".split()[n - 1] if 0 < n <= 10 else str(n)  # fmt: skip
