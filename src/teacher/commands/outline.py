"""`teacher outline`: a source in, a tree of its headings and subheadings out."""

from pathlib import Path
from typing import Annotated

import typer

from teacher.llm import start_trace
from teacher.servers import serve_script_model
from teacher.settings import SCRIPT_MODEL
from teacher.source import read_source
from teacher.tree import build_tree, render_tree


def outline(
    source: Annotated[
        str,
        typer.Argument(
            help="PDF path or URL, arXiv abs URL, blog post URL, or Markdown file"
        ),
    ],
    model: str = typer.Option(SCRIPT_MODEL, help="Script model served by vLLM"),
    out: Path = typer.Option(Path("out/outline"), help="Output directory"),
    server: str = typer.Option(
        None, help="URL of a running `teacher serve`; skips starting vLLM"
    ),
):
    """Break a source into nested headings, recursively: <name>.outline.md (headings) and .outline.json (with text)."""
    out.mkdir(parents=True, exist_ok=True)
    paper = read_source(source)
    with serve_script_model(model, out / "script-model.log", server) as llm:
        start_trace(out / f"{paper.name}.outline.trace.jsonl")
        tree = build_tree(paper.markdown, llm)
    (out / f"{paper.name}.outline.md").write_text(render_tree(tree))
    (out / f"{paper.name}.outline.json").write_text(
        "[" + ",\n".join(n.model_dump_json(indent=1) for n in tree) + "]"
    )
    typer.echo(f"Wrote {out / paper.name}.outline.md and .outline.json")
