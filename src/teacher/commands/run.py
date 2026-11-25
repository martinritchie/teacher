"""`teacher run`: a paper or blog post in, a narrated MP3 out.

Start here. Each line is one stage of the data flow, and each stage lives in its own module:
source (read and convert), episode (introduction, authors, contributions, method), tts (Kokoro), servers (local vLLM).
Only one model holds the GPU at a time.
"""

import time
from pathlib import Path
from typing import Annotated

import typer

from teacher.episode import split_into_chunks, write_episode
from teacher.llm import record, stage, start_trace
from teacher.servers import serve_script_model
from teacher.settings import SCRIPT_MODEL, VOICE, VOICE_MODEL
from teacher.source import read_source
from teacher.tts import Voice, chapters, make_speakable, save, synthesize


def run(
    source: Annotated[
        str, typer.Argument(help="PDF path, PDF URL, arXiv abs URL, or blog post URL")
    ],
    model: str = typer.Option(
        SCRIPT_MODEL,
        help="Script model: served by vLLM, or claude-* on the Anthropic API",
    ),
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
    """Turn a paper or blog post into <name>.md (script) and <name>.mp3 in --out. <name>.trace.jsonl has every
    model call (prompt, output, tokens, seconds), each server's startup time, and the time of each stage."""
    out.mkdir(parents=True, exist_ok=True)

    start = time.monotonic()
    paper = read_source(source)
    chunks = split_into_chunks(paper.markdown, model, chunk)
    start_trace(
        out / f"{paper.name}.trace.jsonl"
    )  # named after the source, so opened once it is read
    record(stage="read", seconds=round(time.monotonic() - start, 1))

    with (
        stage("narrate"),
        serve_script_model(model, out / "script-model.log", server) as llm,
    ):
        script = write_episode(paper.markdown, paper.front, chunks, llm, minutes)

    paragraphs, marks = make_speakable(script), chapters(script)
    save(
        out, paper.name, paragraphs, marks=marks
    )  # before speech, so a failure there keeps the script
    typer.echo(f"Wrote {out / paper.name}.md")

    if audio:
        with stage("tts"):
            clips = synthesize(paragraphs, Voice(voice))
        save(out, paper.name, paragraphs, clips, marks)
        typer.echo(f"Wrote {out / paper.name}.mp3")
