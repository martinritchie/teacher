"""Teacher CLI entry point."""

import typer

from teacher.commands.evaluate import evaluate
from teacher.commands.hear import hear_clips
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

if __name__ == "__main__":
    app()
