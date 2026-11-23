"""Talking to the model (llm.py): the trace, the per-model caps on calls in flight, and parallel()."""

import json
import re
import threading
import time

import pytest

import teacher.llm as llm_mod
from teacher.testing import (
    PDF,
    SMALL_MODEL,
    TREE,
    cli,
)


def test_every_call_is_traced(episode_run):
    """<name>.trace.jsonl has one line per model call: the prompt template, the message sent and the reply."""
    llm, out = episode_run.llm, episode_run.out
    trace = (out / f"{PDF.stem}.trace.jsonl").read_text().splitlines()
    lines = [json.loads(line) for line in trace if '"call"' in line]
    assert [line["prompt"] for line in lines] == [c.prompt for c in llm]
    assert lines[0]["call"] == "episode/abstract" and "text" in lines[0]["output"]


def test_the_trace_records_tokens_and_the_time_of_each_stage(episode_run):
    """For benchmarking: every call's input and output tokens and its model requests, and the seconds each stage
    of `teacher run` took (read, write, speak), in order."""
    lines = [
        json.loads(line)
        for line in (episode_run.out / f"{PDF.stem}.trace.jsonl")
        .read_text()
        .splitlines()
    ]
    calls = [line for line in lines if "call" in line]
    assert all(
        c["input_tokens"] > 0 and c["output_tokens"] > 0 and c["requests"] == 1
        for c in calls
    )
    assert all(
        len(c["finish_reasons"]) == 1 and "messages" not in c for c in calls
    )  # one request: no history kept
    stages = [line for line in lines if "stage" in line]
    assert [s["stage"] for s in stages] == ["read", "write", "speak"]
    assert all(isinstance(s["seconds"], float) for s in stages)
    assert lines.index(stages[0]) == 0 and lines[-1] == stages[-1]


def test_the_trace_records_each_calls_model_and_time(llm, tmp_path):
    """Each trace line names the model and how long the call took, to see where a run's time goes."""
    (tmp_path / "x.outline.json").write_text(json.dumps(TREE))
    cli("write", tmp_path / "x.outline.json", "--node", "Encoder", "--out", tmp_path)
    line = json.loads((tmp_path / "x.encoder.trace.jsonl").read_text().splitlines()[0])
    assert line["model"] == SMALL_MODEL and isinstance(line["seconds"], float)


def test_calls_in_flight_are_capped_however_parallel_nests(llm, tmp_path, monkeypatch):
    """Every call holds one of its model's slots, so nested `parallel` calls (cases, then notes, then facts) cannot
    exceed the cap; and nesting cannot deadlock."""
    held, most = [0], [0]  # for the narrating model's slots

    class Slots:
        def __init__(self):
            self.inner = threading.BoundedSemaphore(2)

        def __enter__(self):
            self.inner.acquire()
            held[0] += 1
            most[0] = max(most[0], held[0])

        def __exit__(self, *exc):
            held[0] -= 1
            self.inner.release()

    monkeypatch.setattr(llm_mod, "PARALLEL", 4)
    monkeypatch.setattr(llm_mod, "_slots", {SMALL_MODEL: Slots()})
    (tmp_path / "x.outline.json").write_text(json.dumps(TREE))
    cases = [{"tree": str(tmp_path / "x.outline.json"), "node": n, "facts": ["A.", "B."]} for n in ("Method", "Encoder")]  # fmt: skip
    (tmp_path / "cases.json").write_text(json.dumps(cases))
    cli("eval", tmp_path / "cases.json", "--out", tmp_path)
    assert 1 <= most[0] <= 2 and len(llm) > 10


def test_independent_calls_run_in_parallel_in_order(llm, tmp_path, monkeypatch):
    """With several calls in flight, results still come back in order: each case keeps its own narration and verdicts."""
    monkeypatch.setattr(llm_mod, "PARALLEL", 4)
    (tmp_path / "x.outline.json").write_text(json.dumps(TREE))
    cases = [{"tree": str(tmp_path / "x.outline.json"), "node": n, "facts": [f"{n} fact {i}." for i in "ab"]} for n in ("Encoder", "Loss", "Distance term")]  # fmt: skip
    (tmp_path / "cases.json").write_text(json.dumps(cases))
    output = cli("eval", tmp_path / "cases.json", "--note-rounds", 0, "--out", tmp_path)
    assert [line.split()[0] for line in output.splitlines()[2:5]] == [
        "Encoder",
        "Loss",
        "Distance",
    ]
    assert re.search(r"total +6/6", output) and len(llm.of("judge")) == 6
    trace = (
        (tmp_path / next(p.name for p in tmp_path.glob("*.trace.jsonl")))
        .read_text()
        .splitlines()
    )
    assert len(trace) == len(llm)  # every call traced, none lost to a race


def test_parallel_cancels_the_items_not_yet_started_when_one_fails(monkeypatch):
    """A failure (or Ctrl-C) in one item does not wait for every queued item to run first."""
    monkeypatch.setattr(llm_mod, "PARALLEL", 1)
    ran = []

    def work(i):
        ran.append(i)
        if i == 0:
            raise ValueError("first item fails")

    with pytest.raises(ValueError):
        llm_mod.parallel(work, range(20))
    time.sleep(0.02)  # time for a queued item to start, were it not cancelled
    assert ran == [0]
