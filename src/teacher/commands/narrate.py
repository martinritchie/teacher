"""`teacher narrate`: narrate one node of an outline tree (every leaf under it), to iterate on the writing prompts."""

import re
from pathlib import Path
from typing import Annotated

import typer

from teacher.llm import start_trace
from teacher.servers import serve_script_model
from teacher.settings import SCRIPT_MODEL
from teacher.tree import NOTE_ROUNDS, find_node, load_tree, narrate


def narrate_node(
    tree: Annotated[
        Path, typer.Argument(help="<name>.outline.json from `teacher outline`")
    ],
    node: str = typer.Option(..., help="Title of the node to narrate, or part of it"),
    model: str = typer.Option(
        SCRIPT_MODEL,
        help="Script model: served by vLLM, or claude-* on the Anthropic API",
    ),
    server: str = typer.Option(
        None, help="URL of a running `teacher serve`; skips starting vLLM"
    ),
    note_rounds: int = typer.Option(
        NOTE_ROUNDS,
        help="Verify-and-revise rounds for each leaf's notes; 0 for one draft",
    ),
    out: Path = typer.Option(Path("out/narrate"), help="Output directory"),
):
    """Narrate one node: <out>/<name>.<node>.md, with every model call in .trace.jsonl."""
    out.mkdir(parents=True, exist_ok=True)
    found = find_node(load_tree(tree), node)
    slug = re.sub(r"\W+", "-", found.title).strip("-").lower()
    name = f"{tree.name.removesuffix('.outline.json')}.{slug}"
    with serve_script_model(model, out / "script-model.log", server) as llm:
        start_trace(out / f"{name}.trace.jsonl")
        parts = narrate(found, llm, rounds=note_rounds)
    (out / f"{name}.md").write_text("\n\n".join(parts) + "\n")
    typer.echo(f"Wrote {out / name}.md")
