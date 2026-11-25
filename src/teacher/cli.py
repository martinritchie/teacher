"""Teacher CLI entry point."""

import os
import signal
import sys

import typer

from teacher.commands.episodes import episodes
from teacher.commands.evaluate import evaluate
from teacher.commands.hear import hear_clips
from teacher.commands.judge_bench import judge_bench
from teacher.commands.outline import outline
from teacher.commands.run import run
from teacher.commands.serve import serve
from teacher.commands.speak import speak_script
from teacher.commands.write import write

app = typer.Typer()
app.callback()(lambda: None)
app.command()(run)
app.command()(outline)
app.command()(write)
app.command(name="eval")(evaluate)
app.command()(serve)
app.command(name="speak")(speak_script)
app.command(name="hear")(hear_clips)
app.command(name="judge-bench")(judge_bench)
app.command()(episodes)


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
