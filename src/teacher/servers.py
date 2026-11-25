"""The script and voice models: local vLLM servers, each running only while its stage needs the GPU, or Claude
on the Anthropic API for a model named claude-*."""

import os
import signal
import socket
import subprocess
import sys
import threading
import time
from collections.abc import Iterator
from contextlib import contextmanager, nullcontext
from pathlib import Path

import httpx
import typer
from pydantic_ai.exceptions import ModelHTTPError
from pydantic_ai.models import Model

from teacher.llm import record
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
            yield served(model, url)
        except ModelHTTPError as e:
            hint = (
                "\nIf it is too long, lower --chunk." if e.model_name == model else ""
            )
            typer.echo(
                f"{e.model_name} rejected a call ({e.status_code}): {e.body}{hint}"
            )
            raise typer.Exit(1)


def served(model: str, url: str) -> Model:
    """A model on a vLLM server's OpenAI-compatible API. The client libraries are imported here, as they are slow to import."""
    from pydantic_ai.models.openai import OpenAIChatModel
    from pydantic_ai.providers.openai import OpenAIProvider

    return OpenAIChatModel(
        model, provider=OpenAIProvider(base_url=f"{url}/v1", api_key="-")
    )


def claude(model: str) -> Model:
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
    from pydantic_ai.models.anthropic import AnthropicModel
    from pydantic_ai.providers.anthropic import AnthropicProvider

    return AnthropicModel(model, provider=AnthropicProvider(api_key=key))


@contextmanager
def serve_voice_model(
    model: str, log: Path, sampling: dict | None = None
) -> Iterator[str]:
    """The TTS model on vLLM-Omni's speech server. Yields its base URL. `sampling` (temperature, top_p, top_k,
    repetition_penalty) replaces those settings of the first token stage, through a copy of its deploy config
    written next to the log; a temperature applies to both token stages (vLLM-Omni's default for Qwen3-TTS: 0.9)."""
    cmd = ["vllm-omni", "serve", model, "--omni"]
    if sampling:
        cmd += [
            "--deploy-config",
            str(_tts_config(sampling, log.with_suffix(".deploy.yaml"))),
        ]
    with vllm_server(cmd, log) as url:
        yield url


def _tts_config(sampling: dict, path: Path) -> Path:
    import vllm_omni
    import yaml

    config = yaml.safe_load(
        (Path(vllm_omni.__file__).parent / "deploy" / "qwen3_tts.yaml").read_text()
    )
    talker = config["stages"][0]
    talker["default_sampling_params"] |= sampling
    if "temperature" in sampling:
        talker["subtalker_sampling_params"]["temperature"] = sampling["temperature"]
    path.write_text(yaml.safe_dump(config, sort_keys=False))
    return path


@contextmanager
def vllm_server(cmd: list[str], log: Path, port: int | None = None) -> Iterator[str]:
    """Run `cmd` (a vLLM server) on `port`, or a free one, for the length of
    the block; yields its URL. The server is stopped however the block ends, including on SIGTERM or SIGHUP (a
    `pkill`, a closed terminal). Its command and startup time go in the trace."""
    port = port or _free_port()
    url = f"http://127.0.0.1:{port}"
    if _is_ready(
        url
    ):  # a server already answers there; ours could not bind, and we would talk to the wrong one
        typer.echo(
            f"Port {port} is already serving a model; stop it or choose another port.",
            err=True,
        )
        raise typer.Exit(1)
    exe = str(Path(sys.executable).with_name(cmd[0]))
    typer.echo(f"Starting {cmd[2]}, log in {log}...")
    main = (
        threading.current_thread() is threading.main_thread()
    )  # signal handlers can only be set there
    handlers = (
        {s: signal.signal(s, _exit_on_signal) for s in (signal.SIGTERM, signal.SIGHUP)}
        if main
        else {}
    )
    with log.open("w") as out:
        proc = subprocess.Popen(
            [exe, *cmd[1:], "--port", str(port)],
            stdout=out,
            stderr=subprocess.STDOUT,
            start_new_session=True,  # its own process group, so its engine processes stop with it
        )
    try:
        start = time.monotonic()
        _wait_until_ready(proc, url, log)
        record(
            server=cmd[2],
            args=cmd[3:],
            startup_seconds=round(time.monotonic() - start, 1),
        )
        yield url
    finally:
        _stop(proc)
        for s, handler in handlers.items():
            signal.signal(s, handler)


def _exit_on_signal(signum, frame) -> None:
    raise SystemExit(
        128 + signum
    )  # unwinds the `with` blocks, so every server started is stopped


def _stop(proc: subprocess.Popen) -> None:
    """SIGTERM the server's whole process group and wait until every process in it has gone, SIGKILL whatever is
    left after a minute. The group is signalled even if its leader has already exited: an engine process left
    behind would keep the GPU."""
    for sig, seconds in ((signal.SIGTERM, 60), (signal.SIGKILL, 10)):
        try:
            os.killpg(proc.pid, sig)
        except ProcessLookupError:
            return
        deadline = time.monotonic() + seconds
        while time.monotonic() < deadline:
            proc.poll()  # reap the leader, so it does not linger as a zombie in the group
            try:
                os.killpg(proc.pid, 0)  # is anyone left in the group?
            except ProcessLookupError:
                return
            time.sleep(0.2)


def _free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def _wait_until_ready(proc: subprocess.Popen, url: str, log: Path) -> None:
    while proc.poll() is None:
        if _is_ready(url):
            return
        time.sleep(2)
    typer.echo(f"Server exited; see {log}", err=True)
    raise typer.Exit(1)


def _is_ready(url: str) -> bool:
    try:
        return httpx.get(f"{url}/v1/models").is_success
    except httpx.TransportError:
        return False
