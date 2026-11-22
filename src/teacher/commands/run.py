"""`teacher run`: a paper or blog post in, a narrated MP3 out.

Start here. Each line is one stage of the data flow, and each stage lives in its own module:
source (read and convert), episode (abstract, contributions, method), speech (TTS), servers (local vLLM).
Only one model holds the GPU at a time.
"""

from pathlib import Path
from typing import Annotated

import typer

from teacher.episode import split_into_chunks, write_episode
from teacher.servers import serve_script_model, serve_voice_model
from teacher.settings import SCRIPT_MODEL, VOICE, VOICE_MODEL
from teacher.source import read_source
from teacher.speech import make_speakable, save, speak


def run(
    source: Annotated[
        str, typer.Argument(help="PDF path, PDF URL, arXiv abs URL, or blog post URL")
    ],
    model: str = typer.Option(SCRIPT_MODEL, help="Script model served by vLLM"),
    voice: str = typer.Option(VOICE, help=f"{VOICE_MODEL} speaker"),
    minutes: int = typer.Option(25, help="Upper limit on the length of the audio"),
    chunk: int = typer.Option(4000, help="Max source tokens per chunk"),
    out: Path = typer.Option(Path("out/run"), help="Output directory"),
    server: str = typer.Option(
        None, help="URL of a running `teacher serve`; skips starting vLLM"
    ),
    audio: bool = typer.Option(
        True, help="Speak the script; --no-audio writes the script only"
    ),
):
    """Turn a paper or blog post into <name>.md (script) and <name>.mp3 in --out."""
    out.mkdir(parents=True, exist_ok=True)

    paper = read_source(source)
    chunks = split_into_chunks(paper.markdown, model, chunk)

    with serve_script_model(model, out / "script-model.log", server) as llm:
        script = write_episode(
            paper.markdown, chunks, llm, minutes, out / f"{paper.name}.trace.jsonl"
        )

    paragraphs = make_speakable(script)

    if audio:
        with serve_voice_model(VOICE_MODEL, out / "voice-model.log") as tts:
            audio = speak(paragraphs, voice, tts)

    save(out, paper.name, paragraphs, audio)
    typer.echo(
        f"Wrote {out / paper.name}.md{' and .mp3' if audio is not False else ''}"
    )
