"""Teacher CLI entry point."""

import os
import signal
import sys

import typer

from teacher.commands.batch import batch
from teacher.commands.evaluate import evaluate
from teacher.commands.audio_check import audio_check
from teacher.commands.judge_bench import judge_bench
from teacher.commands.outline import outline
from teacher.commands.run import run
from teacher.commands.serve import serve
from teacher.commands.tts import tts
from teacher.commands.narrate import narrate_node

app = typer.Typer()
app.callback()(lambda: None)
EPISODES, SCRIPT, VOICE, SERVER = "Episodes", "Script prompts", "Voice", "Server"
app.command(rich_help_panel=EPISODES)(run)
app.command(rich_help_panel=EPISODES)(batch)
app.command(rich_help_panel=SCRIPT)(outline)
app.command(name="narrate", rich_help_panel=SCRIPT)(narrate_node)
app.command(name="eval", rich_help_panel=SCRIPT)(evaluate)
app.command(name="judge-bench", rich_help_panel=SCRIPT)(judge_bench)
app.command(rich_help_panel=VOICE)(tts)
app.command(name="audio-check", rich_help_panel=VOICE)(audio_check)
app.command(rich_help_panel=SERVER)(serve)


def main() -> None:
    """The `teacher` command. After a SIGTERM or SIGHUP, once the `with` blocks have stopped every server, exit at
    once: worker threads may still be retrying calls to a stopped server, and Python would wait for them."""
    try:
        app()
    except SystemExit as stop:
        if stop.code not in (128 + signal.SIGTERM, 128 + signal.SIGHUP):
            raise
        sys.stdout.flush(), sys.stderr.flush()
        os._exit(stop.code)


if __name__ == "__main__":
    main()
