"""`teacher serve`: keep the script model running, so other commands can skip starting it (--server)."""

import signal
import sys
import time
from pathlib import Path

import typer

from teacher.servers import vllm_server
from teacher.settings import SCRIPT_MODEL, profile


def serve(
    model: str = typer.Option(SCRIPT_MODEL, help="Script model served by vLLM"),
    port: int = typer.Option(8000, help="Port to serve on"),
    log: Path = typer.Option(Path("out/serve.log"), help="Server log"),
):
    """Serve the script model until Ctrl-C. Pass the printed URL to other commands as --server."""
    log.parent.mkdir(parents=True, exist_ok=True)
    # Stop vLLM (its own process group) on Ctrl-C or `pkill -f "teacher serve"`, even when started in the background.
    signal.signal(signal.SIGINT, signal.default_int_handler)
    signal.signal(signal.SIGTERM, lambda *_: sys.exit(0))
    with vllm_server(
        ["vllm", "serve", model, *profile(model)["server"]], log, port
    ) as url:
        typer.echo(f"Ready. Use --server {url}")
        try:
            while True:
                time.sleep(3600)
        except (KeyboardInterrupt, SystemExit):
            typer.echo("Stopping.")
