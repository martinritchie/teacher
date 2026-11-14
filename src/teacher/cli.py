"""Teacher CLI entry point."""

import typer

from teacher.run import run

app = typer.Typer()
app.callback()(lambda: None)
app.command()(run)

if __name__ == "__main__":
    app()
