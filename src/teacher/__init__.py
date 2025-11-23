"""Teacher CLI main entry point."""

import typer

from teacher.dev import dev_app
from teacher.reader import reader_app
from teacher.speaker import speaker_app
from teacher.writer import writer_app

__version__ = "0.1.0"


app = typer.Typer()
app.add_typer(reader_app, name="reader", help="Convert PDF to markdown sections")
app.add_typer(writer_app, name="writer", help="Generate audio-optimized narratives")
app.add_typer(speaker_app, name="speaker", help="Convert narratives to audio")
app.add_typer(dev_app, name="dev", help="Development pipeline commands")

if __name__ == "__main__":
    app()
