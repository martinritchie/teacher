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
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import jinja2
from pydantic import BaseModel, Field
from pydantic_ai import Agent, NativeOutput
from pydantic_ai.exceptions import UnexpectedModelBehavior
from pydantic_ai.models import Model

from teacher.settings import PARALLEL, PROMPTS, profile


class Problems(BaseModel):
    problems: list[str] = Field(
        description="One concrete problem per item. Empty if there are none."
    )


_templates = jinja2.Environment(
    loader=jinja2.FileSystemLoader(PROMPTS), undefined=jinja2.StrictUndefined
)
_trace: Path  # every call's prompt and output, one JSON line each
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
    settings = family["thinking" if _thinks[agent.name] else "writing"]
    slots = _slots.setdefault(
        llm.model_name, threading.BoundedSemaphore(family["parallel"])
    )
    try:
        with slots:
            start = time.monotonic()
            call = agent.run(prompt, model=llm, model_settings=settings)
            output = asyncio.run_coroutine_threadsafe(call, _loop).result().output
    except UnexpectedModelBehavior as e:
        if fallback is None:
            raise
        output, error = fallback, str(e)
    saved = output.model_dump() if isinstance(output, BaseModel) else output
    seconds = round(time.monotonic() - start, 1)
    line = {"call": agent.name, "model": llm.model_name, "seconds": seconds, "prompt": prompt, "output": saved}  # fmt: skip
    with _trace_lock, _trace.open("a") as f:
        f.write(json.dumps(line | ({"error": error} if error else {})) + "\n")
    return output


def ask_until(
    agent: Agent, llm: Model, check: Callable, tries: int = 2, **values
) -> object:
    """Ask, and while `check(output)` finds problems and tries are left, ask again with the last output
    as `draft` and the problems as `problems`. The last try is not checked."""
    output, problems = None, []
    for attempt in range(tries):
        output = ask(agent, llm, draft=output, problems=problems, **values)
        if attempt == tries - 1 or not (problems := check(output)):
            return output


def parallel(fn: Callable, items: Iterable) -> list:
    """`fn` over `items` on up to PARALLEL threads, results in order. Calls in flight are capped per model in `ask`."""
    with ThreadPoolExecutor(PARALLEL) as pool:
        return list(pool.map(fn, items))


def start_trace(path: Path) -> None:
    """Record every later model call's prompt and output in `path`, one JSON line each."""
    global _trace
    _trace = path
    path.write_text("")


def _render(template: str, **values) -> str:
    return _templates.get_template(template).render(**values)
