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
from teacher.servers import serve_script_model
from teacher.settings import SCRIPT_MODEL
from teacher.speech import UNSPOKEN
from teacher.tree import NOTE_ROUNDS, find_node, load_tree, narrate


def evaluate(
    cases: Annotated[
        Path, typer.Argument(help="JSON list of {tree, node, facts}")
    ] = Path("evals/cases.json"),
    only: str = typer.Option(None, help="Run only cases whose node contains this"),
    model: str = typer.Option(SCRIPT_MODEL, help="Script model served by vLLM"),
    server: str = typer.Option(
        None, help="URL of a running `teacher serve`; skips starting vLLM"
    ),
    note_rounds: int = typer.Option(
        NOTE_ROUNDS,
        help="Verify-and-revise rounds for each leaf's notes; 0 for one draft",
    ),
    out: Path = typer.Option(
        Path("out/eval"), help="Output directory; each run gets a timestamped report"
    ),
):
    """Narrate each case's node and judge it fact by fact; print a score table, with details in <out>/<time>.md."""
    todo = [
        c
        for c in json.loads(cases.read_text())
        if not only or only.lower() in c["node"].lower()
    ]
    out.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%d-%H%M%S")
    with serve_script_model(model, out / "script-model.log", server) as llm:
        start_trace(out / f"{stamp}.trace.jsonl")
        results = parallel(lambda case: _run_case(case, llm, note_rounds), todo)
    table = [f"{'node':40} stated  missing  contra  unverified  symbols  words"]
    for case, (narration, judged) in zip(todo, results):
        n = {
            v: sum(j[0] == v for j in judged)
            for v in ("stated", "missing", "contradicted")
        }
        table.append(f"{case['node'][:40]:40} {n['stated']:>3}/{len(judged):<3} {n['missing']:>6} {n['contradicted']:>7} {sum(bool(j[2]) for j in judged):>11} {len(_symbols(narration)):>8} {len(narration.split()):>6}")  # fmt: skip
    total = (
        sum(j[0] == "stated" for _, judged in results for j in judged),
        sum(len(c["facts"]) for c in todo),
    )
    table.append(f"{'total':40} {total[0]:>3}/{total[1]}")
    report = ["```", *table, "```"]
    for case, (narration, judged) in zip(todo, results):
        report += [f"## {case['node']}", narration, *(f"- **{v}**: {fact} — _{quote}_{' **(' + flag + ')**' if flag else ''}" for fact, (v, quote, flag) in zip(case["facts"], judged)), f"Symbols: {', '.join(_symbols(narration)) or 'none'}"]  # fmt: skip
    (out / f"{stamp}.md").write_text("\n\n".join(report) + "\n")
    typer.echo("\n".join(table) + f"\n\nDetails in {out / stamp}.md")


def _run_case(
    case: dict, llm: Model, rounds: int
) -> tuple[str, list[tuple[str, str, str]]]:
    node = find_node(load_tree(Path(case["tree"])), case["node"])
    narration = "\n\n".join(narrate(node, llm, rounds=rounds))
    return narration, parallel(lambda fact: judge(fact, narration, llm), case["facts"])


def _symbols(narration: str) -> list[str]:
    return sorted(set(UNSPOKEN.findall(narration)))
