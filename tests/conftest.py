"""Fixtures shared by every test: the PDF converted once per session, a stub script model, and stub speech.

No model server starts: the script model is a pydantic-ai FunctionModel whose replies follow each agent's phase,
and speech returns silence. Helpers the tests call directly are in teacher.testing.
"""

import functools
import json
import re
from contextlib import contextmanager
from types import SimpleNamespace

import numpy as np
import pytest
from pydantic_ai.messages import ModelResponse, TextPart
from pydantic_ai.models.function import AgentInfo, FunctionModel
from pydantic_ai.profiles import ModelProfile

import teacher.commands.evaluate as eval_mod
import teacher.commands.run as run_mod
import teacher.llm as llm_mod
import teacher.servers as servers
import teacher.source as source
from teacher.settings import (
    SAMPLE_RATE,
)
from teacher.testing import (
    CONTRIBUTIONS,
    PHASES,
    Calls,
    block,
    component,
    method,
    spelled,
)

_pdf_to_markdown = functools.cache(source._pdf_to_markdown)


@pytest.fixture(autouse=True)
def pdf_once(monkeypatch):
    """MinerU (vLLM, real GPU) converts each PDF once per session."""
    monkeypatch.setattr(source, "_pdf_to_markdown", _pdf_to_markdown)


@pytest.fixture
def llm(monkeypatch):
    """No server process; the script model is a FunctionModel. Each agent's instructions identify its phase."""
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
        components = calls.components or [component(j, [j]) for j in range(1, n + 1)]
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

    def model(name, provider):
        calls.served = name
        return stub(name)

    monkeypatch.setattr(servers, "vllm_server", no_server)
    monkeypatch.setattr(servers, "OpenAIChatModel", model)
    monkeypatch.setattr(servers, "claude", stub)  # no Anthropic API calls in tests
    monkeypatch.setattr(eval_mod, "claude", stub)
    monkeypatch.setattr(
        llm_mod, "PARALLEL", 1
    )  # stub replies are numbered in call order
    return calls


@pytest.fixture
def tts(monkeypatch):
    """Stub speech: record the paragraphs and the voice, and return a short silence."""
    calls = []

    def speak(paragraphs, voice, server):
        calls.append(
            SimpleNamespace(script="\n\n".join(paragraphs), voice=voice.speaker)
        )
        return [np.zeros(SAMPLE_RATE // 2) for _ in paragraphs]

    monkeypatch.setattr(run_mod, "speak", speak)
    return calls
