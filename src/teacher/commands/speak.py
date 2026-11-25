"""`teacher speak`: voice an existing script again, to compare voices without rewriting the script."""

from pathlib import Path
from typing import Annotated

import typer

from teacher.settings import VOICE, VOICE_MODEL
from teacher.speech import Voice, chapters, make_speakable, save, speak


def speak_script(
    script: Annotated[
        Path,
        typer.Argument(
            help="A script, one paragraph per blank-line block, with `## ` chapter headings (e.g. out/run/<name>.md)"
        ),
    ],
    voice: str = typer.Option(
        VOICE, help=f"{VOICE_MODEL} voice, e.g. am_michael, bm_george"
    ),
    speed: float = typer.Option(1.0, help="Speaking speed; 1 is the voice's own"),
    out: Path = typer.Option(Path("out/speak"), help="Output directory"),
    name: str = typer.Option(None, help="Output name; defaults to the script's"),
):
    """Speak <script> into <out>/<name>.mp3, with one WAV per paragraph in <out>/<name>.clips/."""
    text = script.read_text()
    paragraphs = make_speakable(text)
    clips = speak(paragraphs, Voice(voice, speed))
    save(out, name or script.stem, paragraphs, clips, chapters(text))
    typer.echo(f"Wrote {out / (name or script.stem)}.mp3 and {len(clips)} clips")
