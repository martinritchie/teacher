"""Teacher CLI entry point."""

import typer

from teacher.commands.evaluate import evaluate
from teacher.commands.outline import outline
from teacher.commands.run import run
from teacher.commands.serve import serve
from teacher.commands.write import write

app = typer.Typer()
app.callback()(lambda: None)
app.command()(run)
app.command()(outline)
app.command()(write)
app.command(name="eval")(evaluate)
app.command()(serve)

if __name__ == "__main__":
    app()
