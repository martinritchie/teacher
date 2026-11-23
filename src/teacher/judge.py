"""Judging a narration fact by fact, for `teacher eval`.

The judge gets one fact per call and must quote the narration's words that decide its verdict. A stated or
contradicted verdict whose quote is not in the narration counts as missing, so a judge that misreads cannot
score a fact.
"""

import re
from difflib import SequenceMatcher
from typing import Literal

from pydantic import BaseModel, Field
from pydantic_ai.models import Model

from teacher.llm import agent, ask


class Verdict(BaseModel):
    verdict: Literal["stated", "missing", "contradicted"]
    quote: str = Field(
        description="The words of the narration that decide the verdict, copied exactly; '...' between two separate passages. Empty only if the fact is missing."
    )


_judge = agent("eval/judge", Verdict, thinks=True)


def judge(fact: str, narration: str, llm: Model) -> tuple[str, str, str]:
    """(verdict, quote, flag); the flag says why a verdict was overruled, or is empty."""
    fallback = Verdict(verdict="missing", quote="")
    v = ask(_judge, llm, fallback, narration=narration, fact=fact)
    if v.verdict != "missing" and not _quoted(v.quote, narration):
        return (
            "missing",
            v.quote,
            f"judged {v.verdict}, but the quote is not in the narration",
        )
    return v.verdict, v.quote, ""


def _quoted(quote: str, narration: str) -> bool:
    """Every passage of the quote (split at '...' and between sentences, since judges join sentences from
    different places) is in the narration: at least 90% of its words appear, in order, in a window of the
    narration as long as the passage. Case and punctuation are ignored."""
    words = lambda s: re.findall(r"[a-z0-9]+", s.lower())  # noqa: E731
    text = words(narration)
    passages = [
        w for p in re.split(r"\.\.\.|…|(?<=[.!?])\s+", quote) if (w := words(p))
    ]
    return bool(passages) and all(_in_order(p, text) for p in passages)


def _in_order(passage: list[str], text: list[str]) -> bool:
    n = len(passage)
    for start in range(max(len(text) - n + 1, 1)):
        matcher = SequenceMatcher(
            None, passage, text[start : start + n + 2], autojunk=False
        )
        if sum(b.size for b in matcher.get_matching_blocks()) >= 0.9 * n:
            return True
    return False
