"""Teacher CLI main entry point."""

import typer

from teacher.dev import dev_app
from teacher.extract import extract_app
from teacher.narrate import narrate_app
from teacher.speak import speak_app

__version__ = "0.1.0"


app = typer.Typer()
app.add_typer(extract_app, name="extract", help="Convert PDF to markdown sections")
app.add_typer(narrate_app, name="narrate", help="Generate audio-optimized narratives")
app.add_typer(speak_app, name="speak", help="Convert narratives to audio")
app.add_typer(dev_app, name="dev", help="Development pipeline commands")

if __name__ == "__main__":
    app()
