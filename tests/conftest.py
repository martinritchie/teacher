"""Fixtures shared by every test: airplane mode, the PDF's saved Markdown, a stub script model, and stub speech.

Unit tests (everything not marked `functional`) touch no network, GPU or model: the PDF reads as MinerU's saved
Markdown of it, the script model is a pydantic-ai FunctionModel whose replies follow each agent's phase, and speech
returns silence. Helpers the tests call directly are in teacher.testing.
"""

import json
import os
import socket
import re
from contextlib import contextmanager
from types import SimpleNamespace

import numpy as np
import pytest
from pydantic_ai.messages import ModelResponse, TextPart
from pydantic_ai.models.function import AgentInfo, FunctionModel
from pydantic_ai.profiles import ModelProfile

import teacher.commands.evaluate as eval_mod
import semchunk

import teacher.commands.run as run_mod
import teacher.episode as episode
import teacher.llm as llm_mod
import teacher.servers as servers
import teacher.source as source
import teacher.speech as speech
from teacher.settings import (
    SAMPLE_RATE,
)
from teacher.testing import (
    CONTRIBUTIONS,
    SHORT_MARKDOWN,
    PDF,
    PHASES,
    Calls,
    block,
    component,
    method,
    run,
    spelled,
)

os.environ |= {
    "HF_HUB_OFFLINE": "1",
    "TRANSFORMERS_OFFLINE": "1",
}  # tokenizers from the local cache only
LOOPBACK = {"127.0.0.1", "::1", "localhost"}
CHUNKERIFY = semchunk.chunkerify


@pytest.fixture(autouse=True)
def unit(request, monkeypatch):
    """Airplane mode for unit tests: sockets reach loopback only. The PDF reads as a short version of its saved
    Markdown (MinerU on the GPU is in a functional test), and tokens are counted as words (loading a real
    tokenizer takes seconds). `tokenizers` records whose tokenizer chunking asked for."""
    if not request.node.get_closest_marker("functional"):
        return _unit(monkeypatch)


@pytest.fixture
def llm(monkeypatch):
    """No server process; the script model is a FunctionModel. Each agent's instructions identify its phase."""
    return _llm(monkeypatch)


@pytest.fixture
def tts(monkeypatch):
    """Stub speech: record the paragraphs and the voice, and return a short silence."""
    return _tts(monkeypatch)


@pytest.fixture(scope="session")
def episode_run(tmp_path_factory):
    """One `teacher run` of the paper with the stubs' default replies, shared by the tests that only read what it
    did (each run costs a dozen stub calls). Its `llm` and `tts` are the calls made, `out` the output folder."""
    with pytest.MonkeyPatch.context() as mp:
        _unit(mp)
        llm, tts, out = _llm(mp), _tts(mp), tmp_path_factory.mktemp("episode")
        run(PDF, "--out", out)
    return SimpleNamespace(llm=llm, tts=tts, out=out)


def _unit(monkeypatch):
    connect = socket.socket.connect

    def offline(sock, address):
        if sock.family != socket.AF_UNIX and address[0] not in LOOPBACK:
            raise OSError(
                f"Unit tests are offline: {address}. Mark the test functional, or stub the call."
            )
        return connect(sock, address)

    monkeypatch.setattr(socket.socket, "connect", offline)
    monkeypatch.setattr(
        source, "_pdf_to_markdown", lambda data: SHORT_MARKDOWN.read_text()
    )
    tokenizers = []

    def chunkerify(tokenizer, max_tokens):
        tokenizers.append(tokenizer)
        return CHUNKERIFY(lambda text: len(text.split()), max_tokens)

    monkeypatch.setattr(episode.semchunk, "chunkerify", chunkerify)
    return tokenizers


def _llm(monkeypatch):
    calls = Calls()
    calls.verdicts, calls.abstracts, calls.parts, calls.contributions = [], [], [], []
    calls.details, calls.splits, calls.verdict, calls.started = [], {}, "stated", 0
    calls.gaps, calls.quote = [], None
    calls.settings, calls.components = {}, None

    def reply(messages, info: AgentInfo, model: str):
        if calls.error:
            raise calls.error
        phase = PHASES[info.instructions.splitlines()[0]]
        prompt = str(messages[-1].parts[-1].content)  # a retry's content is a list
        calls.settings[phase] = info.model_settings
        calls.append(SimpleNamespace(phase=phase, prompt=prompt, model=model))
        k = len(calls.of(phase))
        problems = calls.verdicts.pop(0) if phase == "check" and calls.verdicts else []
        n = len(re.findall(r'<chunk number="', prompt))
        components = calls.components or [
            component(1, list(range(1, n + 1)))
        ]  # one, to keep the calls few
        text = {
            "abstract": lambda: json.dumps({"text": calls.abstracts.pop(0) if calls.abstracts else block(prompt, "abstract")}),
            "contributions": lambda: json.dumps(calls.contributions.pop(0) if calls.contributions else CONTRIBUTIONS),
            "notes": lambda: f"Notes {k}.",
            "outline": lambda: json.dumps(method(components)),
            "judge": lambda: json.dumps({"verdict": calls.verdict, "quote": calls.quote if calls.quote is not None else block(prompt, "narration").split("\n")[0]}),
            "leaf notes": lambda: json.dumps({"notes": [f"Note {spelled(k)} a.", f"Note {spelled(k)} b."]}),
            "notes check": lambda: json.dumps({"problems": calls.gaps.pop(0) if calls.gaps else []}),
            "split": lambda: json.dumps({"subsections": [{"title": t, "starts_with": w} for t, w in calls.splits.get(block(prompt, "path").split(" > ")[-1], calls.splits.get("*", []))]}),
            "detail": lambda: (lambda d: d if isinstance(d, str) else json.dumps(d))(calls.details.pop(0) if calls.details else {"purpose": f"Purpose {k}.", "inputs": "x", "steps": [f"Detailed step {k}."], "outputs": "y"}),
            "method": lambda: calls.parts.pop(0) if calls.parts else f"Part {spelled(k)}.",
            "reconstruct": lambda: json.dumps({"pseudocode": f"Code {k}."}),
            "check": lambda: problems if isinstance(problems, str) else json.dumps({"problems": problems}),
        }[phase]()  # fmt: skip
        return ModelResponse(parts=[TextPart(text)])

    @contextmanager
    def no_server(cmd, log, port=None):
        calls.started += 1
        yield "http://server"

    def stub(
        name,
    ):  # named like the real model, since its settings are looked up by name
        return FunctionModel(lambda m, i: reply(m, i, name), model_name=name, profile=ModelProfile(supports_json_schema_output=True))  # fmt: skip

    def served(name, url):
        calls.served = name
        return stub(name)

    monkeypatch.setattr(servers, "vllm_server", no_server)
    monkeypatch.setattr(servers, "served", served)
    monkeypatch.setattr(servers, "claude", stub)  # no Anthropic API calls in tests
    monkeypatch.setattr(eval_mod, "claude", stub)
    monkeypatch.setattr(
        llm_mod, "PARALLEL", 1
    )  # stub replies are numbered in call order
    return calls


def _tts(monkeypatch):
    calls = []

    def speak(paragraphs, voice, server):
        calls.append(
            SimpleNamespace(script="\n\n".join(paragraphs), voice=voice.speaker)
        )
        return [
            np.zeros(SAMPLE_RATE // 100) for _ in paragraphs
        ]  # a short MP3 encodes quickly

    monkeypatch.setattr(run_mod, "speak", speak)
    monkeypatch.setattr(speech, "PAUSE_SECONDS", 0.01)
    return calls
