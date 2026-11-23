"""The model servers (servers.py): a running server, Claude on the API, and stopping vLLM however a command ends."""

import json
import os
import signal
import subprocess
import sys
import time

import pytest
from typer.testing import CliRunner

import teacher.llm as llm_mod
import teacher.servers as servers
from teacher.cli import app
from teacher.testing import (
    TREE,
    alive,
    cli,
    fake_server,
    gone,
    typer_exit,
)


def test_server_option_uses_a_running_server(llm, tmp_path):
    """With --server, commands use that server instead of starting vLLM."""
    (tmp_path / "x.outline.json").write_text(json.dumps(TREE))
    cli(
        "write",
        tmp_path / "x.outline.json",
        "--node",
        "Encoder",
        "--out",
        tmp_path,
        "--server",
        "http://127.0.0.1:8000",
    )
    assert llm.started == 0
    cli("write", tmp_path / "x.outline.json", "--node", "Encoder", "--out", tmp_path)
    assert llm.started == 1


def test_a_claude_model_runs_on_the_api_with_its_own_settings(llm, tmp_path):
    """--model claude-* starts no vLLM server. Its calls get Claude's settings: effort by role, no sampling settings."""
    (tmp_path / "x.outline.json").write_text(json.dumps(TREE))
    args = ["write", tmp_path / "x.outline.json", "--node", "Encoder", "--out", tmp_path, "--model", "claude-sonnet-5-5"]  # fmt: skip
    result = CliRunner().invoke(app, list(map(str, args)))
    assert result.exit_code == 0, result.output
    assert llm.started == 0 and {c.model for c in llm} == {"claude-sonnet-5-5"}
    assert llm.settings["method"]["anthropic_effort"] == "low"
    assert llm.settings["check"]["anthropic_effort"] == "high"
    assert not any("temperature" in s or "top_p" in s for s in llm.settings.values())


@pytest.mark.functional  # real processes and signals
def test_sigterm_stops_the_server_and_its_engine(tmp_path):
    """A SIGTERM (a `pkill`, a timeout) unwinds the block, so the server and its engine process are stopped and do
    not keep the GPU; the previous signal handler is put back afterwards."""
    before = signal.getsignal(signal.SIGTERM)
    with pytest.raises(SystemExit):
        with servers.vllm_server(fake_server(tmp_path), tmp_path / "server.log"):
            os.kill(os.getpid(), signal.SIGTERM)
            time.sleep(5)
    server, engine = map(int, (tmp_path / "pids").read_text().split())
    assert gone(server, engine)
    assert signal.getsignal(signal.SIGTERM) is before


@pytest.mark.functional  # real processes and signals
def test_stopping_reaches_an_engine_whose_server_already_exited(tmp_path):
    """If the server process has died but left its engine running, stopping still signals the whole group."""
    script = "import subprocess, sys; e = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(600)']); print(e.pid, flush=True)"  # fmt: skip
    proc = subprocess.Popen([sys.executable, "-c", script], stdout=subprocess.PIPE, text=True, start_new_session=True)  # fmt: skip
    engine = int(proc.stdout.readline())
    proc.wait()
    assert alive(engine)
    servers._stop(proc)
    assert gone(engine)


@pytest.mark.functional  # real processes and signals
def test_a_port_already_serving_a_model_is_refused(tmp_path):
    """On a fixed port where another server answers, starting a second would talk to the wrong one: stop instead."""
    with servers.vllm_server(fake_server(tmp_path), tmp_path / "first.log") as url:
        port = int(url.rsplit(":", 1)[1])
        with pytest.raises(typer_exit()):
            with servers.vllm_server(
                fake_server(tmp_path), tmp_path / "second.log", port
            ):
                pass


@pytest.mark.functional  # a real process
def test_a_server_records_its_startup_time_in_the_trace(tmp_path, monkeypatch):
    """The time from starting a server to its first answer goes in the trace: an engine's startup is part of its cost."""
    monkeypatch.setattr(llm_mod, "_trace", None)
    llm_mod.start_trace(tmp_path / "t.trace.jsonl")
    with servers.vllm_server(fake_server(tmp_path), tmp_path / "server.log"):
        pass
    line = json.loads((tmp_path / "t.trace.jsonl").read_text())
    assert isinstance(line["startup_seconds"], float) and "server" in line
