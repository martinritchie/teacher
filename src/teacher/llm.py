"""Talking to the script model: agents built from prompt files, traced calls, a retry loop, and parallel calls.

An agent named "part/writer" has prompts/part/writer.md as its instructions and renders
prompts/part/writer_task.md, with the values passed to `ask`, as the message of each call. Its model settings
come from the profile of whichever model runs it (settings.PROFILES): writing or thinking.
"""

import asyncio
import json
import threading
import time
from collections.abc import Callable, Iterable
from typing import Any
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from pathlib import Path

import jinja2
from pydantic import BaseModel, Field
from pydantic_ai import Agent, NativeOutput, capture_run_messages
from pydantic_ai.exceptions import UnexpectedModelBehavior
from pydantic_ai.messages import ModelMessagesTypeAdapter, ModelResponse
from pydantic_ai.models import Model
from pydantic_ai.settings import ModelSettings

from teacher.settings import PARALLEL, PROMPTS, profile


class Problems(BaseModel):
    problems: list[str] = Field(
        description="One concrete problem per item. Empty if there are none."
    )


_templates = jinja2.Environment(
    loader=jinja2.FileSystemLoader(PROMPTS), undefined=jinja2.StrictUndefined
)
_trace: Path | None = (
    None  # every call's prompt, output and tokens, and each stage's time: one JSON line each
)
_trace_lock = threading.Lock()
_thinks: dict[
    str, bool
] = {}  # agent name -> whether it plans or checks (thinking settings)
# Calls in flight per model, however deeply `parallel` nests: the GPU's cap does not hold back API calls.
_slots: dict[str, threading.BoundedSemaphore] = {}

# Every model call runs on this one event loop, whichever thread asks: the HTTP client's connection
# pool belongs to the loop that first used it, so calls from `parallel` threads must not bring their own.
_loop = asyncio.new_event_loop()
threading.Thread(target=_loop.run_forever, daemon=True).start()


def agent(name: str, output=str, thinks: bool = False) -> Agent:
    _thinks[name] = thinks
    output = output if output is str else NativeOutput(output)
    return Agent(name=name, instructions=_render(f"{name}.md"), output_type=output)


def ask(agent: Agent, llm: Model, fallback=None, **values):
    """One call, traced. With a `fallback`, a reply that is not valid output (e.g. thinking that ran out of
    tokens) gives the fallback instead of ending the run."""
    prompt, error = _render(f"{agent.name}_task.md", **values), None
    family = profile(llm.model_name)
    settings = family["thinking" if _thinks[str(agent.name)] else "writing"]
    slots = _slots.setdefault(
        llm.model_name, threading.BoundedSemaphore(family["parallel"])
    )
    try:
        with slots:
            start, messages = time.monotonic(), []
            call = _run(agent, prompt, llm, settings, messages)
            output = asyncio.run_coroutine_threadsafe(call, _loop).result().output
    except UnexpectedModelBehavior as e:
        if fallback is None:
            raise
        output, error = fallback, str(e)
    saved = output.model_dump() if isinstance(output, BaseModel) else output
    replies = [m for m in messages if isinstance(m, ModelResponse)]
    line = {"call": agent.name, "model": llm.model_name, "seconds": round(time.monotonic() - start, 1),
            "input_tokens": sum(r.usage.input_tokens for r in replies), "output_tokens": sum(r.usage.output_tokens for r in replies),
            "requests": len(replies), "finish_reasons": [r.finish_reason for r in replies], "prompt": prompt, "output": saved}  # fmt: skip
    if (
        error or len(replies) > 1
    ):  # keep the failed attempts, reasoning included, and what was sent after them
        line |= {"error": error} if error else {}
        line["messages"] = ModelMessagesTypeAdapter.dump_python(messages, mode="json")
    record(**line)
    return output


async def _run(
    agent: Agent, prompt: str, llm: Model, settings: ModelSettings, messages: list
):
    """agent.run, with every request and reply of the run added to `messages`, even when it fails."""
    with capture_run_messages() as captured:
        try:
            return await agent.run(prompt, model=llm, model_settings=settings)
        finally:
            messages.extend(captured)


def ask_until(
    agent: Agent,
    llm: Model,
    check: Callable,
    tries: int = 2,
    clean: Callable = lambda output: output,
    **values: Any,
) -> Any:
    """Ask, and while `check(output)` finds problems and tries are left, ask again with the last output
    as `draft` and the problems as `problems`. The last try is not checked. `clean` is applied to every
    output first, for fixes code can make without a model."""
    output, problems = None, []
    for attempt in range(tries):
        output = clean(ask(agent, llm, draft=output, problems=problems, **values))
        if attempt == tries - 1 or not (problems := check(output)):
            return output


def parallel(fn: Callable, items: Iterable) -> list:
    """`fn` over `items` on up to PARALLEL threads, results in order. Calls in flight are capped per model in `ask`.
    If one fails, or Ctrl-C is pressed, the items not yet started are cancelled rather than run."""
    pool = ThreadPoolExecutor(PARALLEL)
    try:
        return list(pool.map(fn, items))
    finally:
        pool.shutdown(wait=False, cancel_futures=True)


def start_trace(path: Path) -> None:
    """Record every later model call (prompt, output, tokens, seconds) and stage time in `path`, one JSON line each."""
    global _trace
    _trace = path
    path.write_text("")


def record(**line) -> None:
    """One line in the trace, if one is open."""
    if _trace:
        with _trace_lock, _trace.open("a") as f:
            f.write(json.dumps(line) + "\n")


@contextmanager
def stage(name: str):
    """Record how long the block took, as {"stage": name, "seconds": ...}."""
    start = time.monotonic()
    yield
    record(stage=name, seconds=round(time.monotonic() - start, 1))


def _render(template: str, **values) -> str:
    return _templates.get_template(template).render(**values)
