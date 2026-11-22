"""`teacher eval`: narrate a fixed set of nodes and judge each narration against facts it must state, to
compare prompt changes in minutes."""

import json
import time
from pathlib import Path
from typing import Annotated

import typer
from pydantic_ai.models import Model

from teacher.judge import judge
from teacher.llm import parallel, start_trace
from teacher.servers import claude, serve_script_model
from teacher.settings import JUDGE_MODEL, SCRIPT_MODEL
from teacher.speech import UNSPOKEN
from teacher.tree import NOTE_ROUNDS, find_node, load_tree, narrate


def evaluate(
    cases: Annotated[
        Path, typer.Argument(help="JSON list of {tree, node, facts}")
    ] = Path("evals/cases.json"),
    only: str = typer.Option(None, help="Run only cases whose node contains this"),
    model: str = typer.Option(
        SCRIPT_MODEL,
        help="Model that narrates: served by vLLM, or claude-* on the Anthropic API",
    ),
    server: str = typer.Option(
        None, help="URL of a running `teacher serve`; skips starting vLLM"
    ),
    note_rounds: int = typer.Option(
        NOTE_ROUNDS,
        help="Verify-and-revise rounds for each leaf's notes; 0 for one draft",
    ),
    repeat: int = typer.Option(
        1,
        help="Runs of every case, all at once; the table shows each run's score and the mean",
    ),
    out: Path = typer.Option(
        Path("out/eval"), help="Output directory; each run gets a timestamped report"
    ),
):
    """Narrate each case's node and judge it fact by fact with the fixed judge (settings.JUDGE_MODEL), whatever
    model narrates; print a score table, with details in <out>/<time>.md."""
    todo = [
        c
        for c in json.loads(cases.read_text())
        if not only or only.lower() in c["node"].lower()
    ]
    out.mkdir(parents=True, exist_ok=True)
    stamp, began = time.strftime("%Y%m%d-%H%M%S"), time.monotonic()
    judge_llm = claude(
        JUDGE_MODEL
    )  # first, so a missing key stops the run before any narration
    with serve_script_model(model, out / "script-model.log", server) as llm:
        start_trace(out / f"{stamp}.trace.jsonl")
        runs = parallel(
            lambda case: _run_case(case, llm, judge_llm, note_rounds), todo * repeat
        )
    by_case = [
        runs[i :: len(todo)] for i in range(len(todo))
    ]  # each case's runs, in order
    table = [
        f"narrated by {model}, judged by {JUDGE_MODEL}, {repeat} run(s) in {time.monotonic() - began:.0f}s"
    ]
    table.append(f"{'node':40} stated  missing  contra  unverified  symbols  words")
    for case, results in zip(todo, by_case):
        verdicts = [j for _, judged in results for j in judged]
        count = lambda v: sum(j[0] == v for j in verdicts)  # noqa: E731
        stated = " ".join(
            f"{sum(j[0] == 'stated' for j in judged)}/{len(judged)}"
            for _, judged in results
        )
        words = sum(len(narration.split()) for narration, _ in results) // repeat
        symbols = sum(len(_symbols(narration)) for narration, _ in results)
        table.append(f"{case['node'][:40]:40} {stated:>7} {count('missing'):>6} {count('contradicted'):>7} {sum(bool(j[2]) for j in verdicts):>11} {symbols:>8} {words:>6}")  # fmt: skip
    totals = [
        sum(sum(j[0] == "stated" for j in by_case[c][r][1]) for c in range(len(todo)))
        for r in range(repeat)
    ]
    of = sum(len(c["facts"]) for c in todo)
    mean = f"  mean {sum(totals) / repeat:.1f}" if repeat > 1 else ""
    table.append(f"{'total':40} {' '.join(f'{t}/{of}' for t in totals):>7}{mean}")
    report = ["```", *table, "```"]
    for case, results in zip(todo, by_case):
        for r, (narration, judged) in enumerate(results, start=1):
            run = f" (run {r})" if repeat > 1 else ""
            report += [f"## {case['node']}{run}", narration, *(f"- **{v}**: {fact} — _{quote}_{' **(' + flag + ')**' if flag else ''}" for fact, (v, quote, flag) in zip(case["facts"], judged)), f"Symbols: {', '.join(_symbols(narration)) or 'none'}"]  # fmt: skip
    (out / f"{stamp}.md").write_text("\n\n".join(report) + "\n")
    typer.echo("\n".join(table) + f"\n\nDetails in {out / stamp}.md")


def _run_case(
    case: dict, llm: Model, judge_llm: Model, rounds: int
) -> tuple[str, list[tuple[str, str, str]]]:
    node = find_node(load_tree(Path(case["tree"])), case["node"])
    narration = "\n\n".join(narrate(node, llm, rounds=rounds))
    return narration, parallel(
        lambda fact: judge(fact, narration, judge_llm), case["facts"]
    )


def _symbols(narration: str) -> list[str]:
    return sorted(set(UNSPOKEN.findall(narration)))
