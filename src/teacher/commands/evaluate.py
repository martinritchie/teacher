"""`teacher eval`: narrate a fixed set of nodes and judge each narration against facts it must state, to
compare prompt changes in minutes."""

import json
import time
from pathlib import Path
from typing import Annotated

import typer
from pydantic_ai.models import Model

from teacher.judge import judge, unsupported
from teacher.llm import parallel, start_trace
from teacher.servers import claude, serve_script_model
from teacher.settings import JUDGE_MODEL, SCRIPT_MODEL
from teacher.tts import UNSPOKEN
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
    judge_model: str = typer.Option(
        JUDGE_MODEL,
        "--judge",
        help="Model that judges; keep it fixed so scores stay comparable. The narrator's server is reused when they match",
    ),
    out: Path = typer.Option(
        Path("out/eval"), help="Output directory; each run gets a timestamped report"
    ),
):
    """Narrate each case's node, then judge it fact by fact with the fixed judge (settings.JUDGE_MODEL), whatever
    model narrates; print a score table, with details in <out>/<time>.md."""
    todo = [
        c
        for c in json.loads(cases.read_text())
        if not only or only.lower() in c["node"].lower()
    ]
    out.mkdir(parents=True, exist_ok=True)
    stamp, began = time.strftime("%Y%m%d-%H%M%S"), time.monotonic()
    if judge_model.startswith("claude-"):
        claude(
            judge_model
        )  # first, so a missing key stops the run before any narration
    trace = out / f"{stamp}.trace.jsonl"
    start_trace(trace)
    work = todo * repeat
    with serve_script_model(model, out / "script-model.log", server) as llm:
        narrated = parallel(lambda case: _narrate(case, llm, note_rounds), work)
        # the final narration, and the same parts as first drafted, judged on the same facts
        texts = [n for n, _ in narrated] + [
            "\n\n".join(d["draft"] for d in log) for _, log in narrated
        ]
        sources = [_source(case) for case in work * 2]
        if judge_model == model:
            judged, grounded = (
                _judge_all(work * 2, texts, llm),
                _ground_all(texts, sources, llm),
            )
    if judge_model != model:
        with serve_script_model(judge_model, out / "judge-model.log") as judge_llm:
            judged, grounded = (
                _judge_all(work * 2, texts, judge_llm),
                _ground_all(texts, sources, judge_llm),
            )
    n = len(work)
    runs = [(text, log, final, draft, bad, bad_draft) for (text, log), final, draft, bad, bad_draft in zip(narrated, judged[:n], judged[n:], grounded[:n], grounded[n:])]  # fmt: skip
    by_case = [
        runs[i :: len(todo)] for i in range(len(todo))
    ]  # each case's runs, in order
    stated = lambda verdicts: sum(v[0] == "stated" for v in verdicts)  # noqa: E731
    table = [
        f"narrated by {model}, judged by {judge_model}, {repeat} run(s) in {time.monotonic() - began:.0f}s"
    ]
    table.append(
        f"{'node':34} stated  draft  +  -  missing  contra  unverified  unsup  draft  rewritten  checker  symbols  words  /100w"
    )
    for case, results in zip(todo, by_case):
        verdicts = [v for r in results for v in r[2]]
        count = lambda v: sum(j[0] == v for j in verdicts)  # noqa: E731
        finals = " ".join(f"{stated(r[2])}/{len(r[2])}" for r in results)
        draft = sum(stated(r[3]) for r in results) / repeat
        gained = sum(
            f[0] == "stated" != d[0] for r in results for f, d in zip(r[2], r[3])
        )
        lost = sum(
            d[0] == "stated" != f[0] for r in results for f, d in zip(r[2], r[3])
        )
        logs = [d for r in results for d in r[1]]
        rewritten = (
            f"{sum(bool(d['checker'] or d['symbols']) for d in logs)}/{len(logs)}"
        )
        words = sum(len(r[0].split()) for r in results) / repeat
        density = 100 * sum(stated(r[2]) for r in results) / max(repeat * words, 1)
        bad, bad_draft = (sum(len(r[k]) for r in results) / repeat for k in (4, 5))
        table.append(f"{case['node'][:34]:34} {finals:>6} {draft:>6.1f} {gained:>2} {lost:>2} {count('missing'):>8} {count('contradicted'):>7} {sum(bool(j[2]) for j in verdicts):>11} {bad:>6.1f} {bad_draft:>6.1f} {rewritten:>10} {sum(len(d['checker']) for d in logs):>8} "
                     f"{sum(len(d['symbols']) for d in logs):>8} {words:>6.0f} {density:>6.2f}")  # fmt: skip
    totals = [
        sum(stated(by_case[c][r][2]) for c in range(len(todo))) for r in range(repeat)
    ]
    drafts = sum(stated(r[3]) for r in runs) / repeat
    of = sum(len(c["facts"]) for c in todo)
    mean = f"  mean {sum(totals) / repeat:.1f}" if repeat > 1 else ""
    table.append(
        f"{'total':34} {' '.join(f'{t}/{of}' for t in totals):>6}{mean}  drafts {drafts:.1f}  "
        f"unsupported {sum(len(r[4]) for r in runs) / repeat:.1f} (drafts {sum(len(r[5]) for r in runs) / repeat:.1f})"
    )
    table += ["", *_costs(trace)]
    report = ["```", *table, "```"]
    for case, results in zip(todo, by_case):
        for r, (narration, log, final, draft, bad, _) in enumerate(results, start=1):
            run = f" (run {r})" if repeat > 1 else ""
            report += [f"## {case['node']}{run}", narration, *(f"- **{v}**: {fact} — _{quote}_{' **(' + flag + ')**' if flag else ''}{f' (draft: {d[0]})' if d[0] != v else ''}" for fact, (v, quote, flag), d in zip(case["facts"], final, draft)),
                       *(f"Checker, part {k}: " + "; ".join(d["checker"] + d["symbols"]) for k, d in enumerate(log, start=1) if d["checker"] or d["symbols"]),
                       *(f"Unsupported: {b}" for b in bad), f"Symbols: {', '.join(_symbols(narration)) or 'none'}"]  # fmt: skip
    (out / f"{stamp}.md").write_text("\n\n".join(report) + "\n")
    typer.echo("\n".join(table) + f"\n\nDetails in {out / stamp}.md")


def _narrate(case: dict, llm: Model, rounds: int) -> tuple[str, list[dict]]:
    """The node's narration, and each part's first draft with the problems the check found in it."""
    node = find_node(load_tree(Path(case["tree"])), case["node"])
    log: list[dict] = []
    return "\n\n".join(narrate(node, llm, rounds=rounds, log=log)), log


def _source(case: dict) -> str:
    """The text the node's narration is written from: its own text and every descendant's, in order."""
    todo, texts = [find_node(load_tree(Path(case["tree"])), case["node"])], []
    while todo:
        node, todo = todo[0], [*todo[0].children, *todo[1:]]
        texts.append(node.text)
    return "\n\n".join(t for t in texts if t.strip())


def _ground_all(
    narrations: list[str], sources: list[str], llm: Model
) -> list[list[str]]:
    """Each narration's statements that its source does not support."""
    return parallel(
        lambda k: unsupported(narrations[k], sources[k], llm), range(len(narrations))
    )


def _costs(trace: Path) -> list[str]:
    """Calls, seconds and output tokens per agent, from the trace: what each round of the loop costs."""
    calls = [
        json.loads(line) for line in trace.read_text().splitlines() if '"call"' in line
    ]
    rows = [f"{'agent':24} calls  seconds  output tokens"]
    for name in dict.fromkeys(c["call"] for c in calls):
        mine = [c for c in calls if c["call"] == name]
        rows.append(
            f"{name:24} {len(mine):5} {sum(c['seconds'] for c in mine):8.0f} {sum(c.get('output_tokens', 0) for c in mine):14}"
        )
    return rows


def _judge_all(
    cases: list[dict], narrations: list[str], llm: Model
) -> list[list[tuple[str, str, str]]]:
    """Every fact of every case against its narration, all at once; one list of verdicts per case."""
    pairs = [(i, fact) for i, case in enumerate(cases) for fact in case["facts"]]
    verdicts = parallel(lambda p: judge(p[1], narrations[p[0]], llm), pairs)
    return [
        [v for (i, _), v in zip(pairs, verdicts) if i == k] for k in range(len(cases))
    ]


def _symbols(narration: str) -> list[str]:
    return sorted(set(UNSPOKEN.findall(narration)))
