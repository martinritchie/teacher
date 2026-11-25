"""`teacher hear`: check an episode's clips by machine: language, word error rate, and voice consistency."""

from pathlib import Path
from typing import Annotated

import typer

from teacher.hearing import hear, summary
from teacher.speech import make_speakable


def hear_clips(
    clips: Annotated[
        Path,
        typer.Argument(
            help="A <name>.clips folder from `teacher run` or `teacher speak`"
        ),
    ],
    reference: Path = typer.Option(
        None, help="A WAV of the intended voice; defaults to the episode's own average"
    ),
):
    """Score every clip; print a table and a summary, and write them to <name>.hear.md beside the folder."""
    script = clips.with_name(clips.name.removesuffix(".clips") + ".md")
    texts = make_speakable(script.read_text())
    files = sorted(clips.glob("*.wav"))
    if len(files) != len(texts):
        raise typer.BadParameter(
            f"{len(files)} clips but {len(texts)} paragraphs in {script}"
        )
    rows = hear(files, texts, reference)
    table = [f"{'clip':8} {'secs':>5} {'lang':7} {'WER':>6} {'voice':>6} {'pitch Hz':>9} {'z':>5} {'range st':>9} {'z':>5} {'w/s':>5} {'z':>5}  heard"]  # fmt: skip
    table += [f"{r['clip']:8} {r['seconds']:>5} {r['language'][:7]:7} {r['wer']:>6.3f} {r['speaker']:>6.3f} {r['pitch']:>9} {r['pitch_z']:>5} {r['range']:>9} {r['range_z']:>5} {r['pace']:>5} {r['pace_z']:>5}  {r['heard'][:50]}" for r in rows]  # fmt: skip
    report = "\n".join(table) + "\n\n" + summary(rows)
    heard = "\n\n".join(f"{r['clip']}: {r['heard']}" for r in rows)
    clips.with_name(clips.name.removesuffix(".clips") + ".hear.md").write_text(
        f"```\n{report}\n```\n\n## What Whisper heard\n\n{heard}\n"
    )
    typer.echo(report)
