"""`teacher judge-bench`: how well a judge agrees with recorded Claude verdicts, to choose a local eval judge.

evals/judge-reference.jsonl holds narrations from earlier evals, each with its facts and Claude's verdict and quote.
The candidate judges every (narration, fact) pair through the same `judge()` as `teacher eval`, quote check
included. Agreement is reported overall and per verdict, since "stated" is most of the set and a judge that
always says it would agree often while being useless.
"""

import json
from collections import Counter
from pathlib import Path

import typer

from teacher.judge import judge
from teacher.llm import parallel, start_trace
from teacher.servers import serve_script_model
from teacher.settings import JUDGE_MODEL

VERDICTS = ("stated", "missing", "contradicted")


def judge_bench(
    model: str = typer.Option(
        JUDGE_MODEL,
        help="Candidate judge: served by vLLM, or claude-* on the Anthropic API",
    ),
    reference: Path = typer.Option(
        Path("evals/judge-reference.jsonl"), help="Narrations with Claude's verdicts"
    ),
    server: str = typer.Option(
        None, help="URL of a running `teacher serve`; skips starting vLLM"
    ),
    limit: int = typer.Option(0, help="Judge only the first N facts; 0 for all"),
    out: Path = typer.Option(Path("out/judge-bench"), help="Output directory"),
):
    """Judge every recorded (narration, fact) pair with --model; print agreement with Claude, and write the
    disagreements to <out>/<model>.md."""
    groups = [json.loads(line) for line in reference.read_text().splitlines()]
    cases = [(g["narration"], f) for g in groups for f in g["facts"]][: limit or None]
    out.mkdir(parents=True, exist_ok=True)
    name = model.replace("/", "_")
    with serve_script_model(model, out / f"{name}.model.log", server) as llm:
        start_trace(out / f"{name}.trace.jsonl")
        got = parallel(lambda c: judge(c[1]["fact"], c[0], llm), cases)
    gold, pred = [f["verdict"] for _, f in cases], [v for v, _, _ in got]
    lines = [f"{model}: {len(cases)} facts", *agreement(gold, pred)]
    report = ["```", *lines, "```"]
    for (narration, f), (verdict, quote, flag) in zip(cases, got):
        if verdict != f["verdict"]:
            report += [f"## Claude: {f['verdict']}, {model}: {verdict}", f"**Fact:** {f['fact']}", f"**Claude quote:** {f['quote'] or '-'}",
                       f"**Candidate quote:** {quote or '-'}{f' ({flag})' if flag else ''}", narration]  # fmt: skip
    (out / f"{name}.md").write_text("\n\n".join(report) + "\n")
    typer.echo("\n".join(lines) + f"\n\nDisagreements in {out / name}.md")


def agreement(gold: list[str], pred: list[str]) -> list[str]:
    """Agreement, Cohen's kappa (agreement beyond what the two verdict mixes give by chance), and per verdict the
    recall (of Claude's, how many the candidate gave too) and precision (of the candidate's, how many Claude gave)."""
    n, both = len(gold), Counter(zip(gold, pred))
    observed = sum(both[v, v] for v in VERDICTS) / n
    g, p = Counter(gold), Counter(pred)
    chance = sum(g[v] * p[v] for v in VERDICTS) / n**2
    kappa = (observed - chance) / (1 - chance) if chance < 1 else 0.0
    rows = [f"agreement {observed:.3f}, kappa {kappa:.3f}"]
    for v in VERDICTS:
        rows.append(
            f"{v:13} Claude {g[v]:4}  candidate {p[v]:4}  recall {both[v, v]}/{g[v]}  precision {both[v, v]}/{p[v]}"
        )
    return rows
