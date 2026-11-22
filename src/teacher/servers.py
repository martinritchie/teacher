"""The script and voice models: local vLLM servers, each running only while its stage needs the GPU, or Claude
on the Anthropic API for a model named claude-*."""

import os
import signal
import socket
import subprocess
import sys
import time
from collections.abc import Iterator
from contextlib import contextmanager, nullcontext
from pathlib import Path

import httpx
import typer
from pydantic_ai.exceptions import ModelHTTPError
from pydantic_ai.models import Model
from pydantic_ai.models.anthropic import AnthropicModel
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.anthropic import AnthropicProvider
from pydantic_ai.providers.openai import OpenAIProvider

from teacher.settings import CLAUDE_KEY, profile


@contextmanager
def serve_script_model(
    model: str, log: Path, server: str | None = None
) -> Iterator[Model]:
    """The script model for this block: Claude on the Anthropic API for claude-*, otherwise vLLM's
    OpenAI-compatible server, started here unless `server` (a URL from `teacher serve`) is given. A call the
    model's server rejects ends the run."""
    if model.startswith("claude-"):
        yield claude(model)
        return
    cmd = ["vllm", "serve", model, *profile(model)["server"]]
    with nullcontext(server) if server else vllm_server(cmd, log) as url:
        try:
            yield OpenAIChatModel(
                model, provider=OpenAIProvider(base_url=f"{url}/v1", api_key="-")
            )
        except ModelHTTPError as e:
            typer.echo(
                f"vLLM rejected a call: {e.body}\nIf it is too long, lower --chunk."
            )
            raise typer.Exit(1)


def claude(model: str) -> AnthropicModel:
    """Claude on the Anthropic API, with the key from the CLAUDE_API_KEY variable or the repo's .env file."""
    env = Path(__file__).parents[2] / ".env"
    lines = (
        [line.strip().removeprefix("export ") for line in env.read_text().splitlines()]
        if env.exists()
        else []
    )
    found = [
        line.split("=", 1)[1].strip().strip("'\"")
        for line in lines
        if line.startswith(f"{CLAUDE_KEY}=")
    ]
    key = os.environ.get(CLAUDE_KEY) or next(iter(found), None)
    if not key:
        typer.echo(
            f"{model} needs an Anthropic API key: set {CLAUDE_KEY}, or add {CLAUDE_KEY}=... to {env}."
        )
        raise typer.Exit(1)
    return AnthropicModel(model, provider=AnthropicProvider(api_key=key))


@contextmanager
def serve_voice_model(model: str, log: Path) -> Iterator[str]:
    """The TTS model on vLLM-Omni's speech server. Yields its base URL."""
    with vllm_server(["vllm-omni", "serve", model, "--omni"], log) as url:
        yield url


@contextmanager
def vllm_server(cmd: list[str], log: Path, port: int | None = None) -> Iterator[str]:
    """Run `cmd` (a vLLM server) on `port`, or a free one, for the length of the block; yields its URL."""
    port = port or _free_port()
    url = f"http://127.0.0.1:{port}"
    exe = str(Path(sys.executable).with_name(cmd[0]))
    typer.echo(f"Starting {cmd[2]}, log in {log}...")
    proc = subprocess.Popen(
        [exe, *cmd[1:], "--port", str(port)],
        stdout=log.open("w"),
        stderr=subprocess.STDOUT,
        start_new_session=True,  # its own process group, so its engine processes stop with it
    )
    try:
        _wait_until_ready(proc, url, log)
        yield url
    finally:
        _stop(proc)


def _stop(proc: subprocess.Popen) -> None:
    """SIGTERM the server's process group; SIGKILL it if it is still up after a minute."""
    if proc.poll() is not None:  # already exited, e.g. it failed to start
        return
    os.killpg(proc.pid, signal.SIGTERM)
    try:
        proc.wait(timeout=60)
    except subprocess.TimeoutExpired:
        os.killpg(proc.pid, signal.SIGKILL)
        proc.wait()


def _free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def _wait_until_ready(proc: subprocess.Popen, url: str, log: Path) -> None:
    while not _is_ready(url):
        if proc.poll() is not None:
            typer.echo(f"Server exited; see {log}", err=True)
            raise typer.Exit(1)
        time.sleep(2)


def _is_ready(url: str) -> bool:
    try:
        return httpx.get(f"{url}/v1/models").is_success
    except httpx.TransportError:
        return False
