"""Helpers for the test suite: stub-model controls, prompt parsing, CLI shortcuts and sample inputs.

They live in the package rather than under tests/ because tests run with pytest's importlib import mode, where test
modules cannot import each other; pytest's docs recommend keeping such utilities with the library code. Fixtures are
in tests/conftest.py.
"""

import json
import re
import time
from pathlib import Path
from types import SimpleNamespace

from typer.testing import CliRunner

from teacher.cli import app

PDF = next((Path(__file__).parents[2] / "papers").glob("CALM*/*.pdf"))
DATA = Path(__file__).parents[2] / "tests/data"
PDF_MARKDOWN = DATA / "calm.md"  # MinerU's Markdown of PDF
SHORT_MARKDOWN = (
    DATA / "calm-short.md"
)  # the sections the unit tests name, two paragraphs each: what PDF reads as in them


SMALL_MODEL = "Qwen/Qwen3-0.6B"  # only its tokenizer is downloaded


PHASES = {"# Introduction Writer": "introduction", "# Credits Reader": "credits", "# Contributions Writer": "contributions", "# Notes Writer": "notes", "# Method Planner": "outline", "# Component Detailer": "detail", "# Method Writer": "method", "# Listener": "reconstruct", "# Method Checker": "check", "# Section Splitter": "split", "# Fact Judge": "judge", "# Leaf Note Taker": "leaf notes", "# Notes Verifier": "notes check", "# Grounding Checker": "grounding"}  # fmt: skip


DIGITS = "zero one two three four five six seven eight nine".split()


def spelled(k):
    """A number in words, digit by digit, since the symbol check rejects digits."""
    return " ".join(DIGITS[int(d)] for d in str(k))


INTRODUCTION = "An introduction in other words."
CREDITS = {"affiliations": [{"institution": "WeChat AI, at Tencent", "authors": ["Chenze Shao", "Darren Li"]},
                            {"institution": "Tsinghua University", "authors": ["Darren Li"]}], "thanks": ""}  # fmt: skip
AUTHORS = "Chenze Shao and Darren Li are at WeChat AI, at Tencent. Darren Li is also at Tsinghua University."
CONTRIBUTIONS = {"context": "Context.", "items": [{"problem": "Problem.", "before": "Before.", "new": "New."}]}  # fmt: skip


BLOG = """<html><head><title>Tracing features</title></head><body>
<nav><a href="/">Home</a> <a href="/subscribe">Subscribe to our newsletter</a></nav>
<article><h1>Tracing features through a transformer</h1>
{body}
</article>
<footer>Copyright notice. Cookie settings.</footer></body></html>"""


PARAGRAPH = "<p>We build an attribution graph for each prompt, and we then study how the features interact across the layers of the model.</p>"


class Calls(list):
    """Recorded model calls, plus controls for the stub."""

    verdicts: list[list[str]] = []  # problems for the check calls, in order
    introductions: list[str] = []  # introduction replies; default INTRODUCTION
    credits: list[dict] = []  # credits replies; default CREDITS
    contributions: list[dict] = []  # contributions replies; default CONTRIBUTIONS
    details: list = []  # detail replies (a string is invalid output); default "Detailed step k."
    splits: dict = {}  # section title -> [(title, starts_with)]; "*" for every section; default none
    verdict: str = "stated"  # the judge's verdict on every fact
    quote: str | None = None  # the judge's quote; default the narration's first line
    gaps: list[list[str]] = []  # the notes verifier's problems, in order; default none
    started: int = 0  # vLLM servers started
    error: Exception | None = None  # raised by every call when set
    components: list[dict] | None = None  # the outline's; default is one per chunk
    parts: list[str] = []  # replies to the method calls; default "Part k."
    unsupported: list[
        list[str]
    ] = []  # the grounding checker's statements, in order; default none
    served: str = ""  # the model the script server was started with
    server: list = []  # the vLLM command it was started with
    settings: dict = {}  # model settings of each phase

    def of(self, phase):
        return [c for c in self if c.phase == phase]


def invoke(*args):
    return CliRunner().invoke(app, ["run", *map(str, args)])


def run(*args):
    result = invoke(*args, "--model", SMALL_MODEL)
    assert result.exit_code == 0, result.output
    return result


def serve(monkeypatch, body: bytes):
    monkeypatch.setattr(
        "urllib.request.urlopen", lambda *a, **k: SimpleNamespace(read=lambda: body)
    )


def block(prompt, tag):
    return re.findall(rf"<{tag}>\n(.*?)\n</{tag}>", prompt, re.S)[0]


def chunk(call):
    return block(call.prompt, "chunk")


def source_of(call):
    return block(call.prompt, "source")


def component(k, chunks, words=150):
    return {"name": f"piece {k}", "purpose": f"Purpose {k}.", "inputs": "x", "steps": [f"Step {k}."], "outputs": "y", "chunks": chunks, "words": words}  # fmt: skip


def method(components):
    glossary = [{"name": "the encoder", "symbol": "E", "meaning": "Encodes."}]
    return {"glossary": glossary, "components": components, "key_numbers": ["Size four."]}  # fmt: skip


def targets(llm):
    return [int(re.findall(r"about (\d+) words", c.prompt)[0]) for c in llm.of("method")]  # fmt: skip


def paragraphs(tts):
    return tts[0].script.split("\n\n")


LONG = (
    "The method works in stages. " * 70
)  # over the length below which text is one idea


DOC = f"""# A Paper

## Abstract

Short abstract.

## 1 Introduction

{LONG}

## 2 Method

Some preamble.

## 2.1 Encoder

The encoder maps tokens to vectors. {LONG}

The decoder maps vectors back to tokens. {LONG}

## 2.2 Loss

The loss compares samples. {LONG}
"""


def outline(llm, tmp_path, doc=DOC):
    (tmp_path / "paper.md").write_text(doc)
    args = ["outline", tmp_path / "paper.md", "--out", tmp_path, "--model", SMALL_MODEL]
    result = CliRunner().invoke(app, list(map(str, args)))
    assert result.exit_code == 0, result.output
    tree = json.loads((tmp_path / "paper.outline.json").read_text())
    return (tmp_path / "paper.outline.md").read_text(), tree


TREE = [
    {"title": "1 Intro", "text": "Intro text.", "children": []},
    {"title": "2 Method", "text": "Preamble.", "children": [
        {"title": "Encoder", "text": "The encoder maps tokens to vectors.", "children": []},
        {"title": "Loss", "text": "", "children": [
            {"title": "Distance term", "text": "The distance term compares samples.", "children": []},
            {"title": "Diversity term", "text": "The diversity term spreads samples.", "children": []},
        ]},
    ]},
]  # fmt: skip


def cli(*args):
    result = CliRunner().invoke(app, [*map(str, args), "--model", SMALL_MODEL])
    assert result.exit_code == 0, result.output
    return result.output


FAKE_SERVER = """
import http.server, os, subprocess, sys
port = int(sys.argv[sys.argv.index("--port") + 1])
engine = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(600)"])
open(sys.argv[1], "w").write(f"{os.getpid()} {engine.pid}")
class Models(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200); self.end_headers(); self.wfile.write(b'{"data": []}')
    def log_message(self, *args):
        pass
http.server.HTTPServer(("127.0.0.1", port), Models).serve_forever()
"""


def fake_server(tmp_path):
    """A stand-in for `vllm serve`: answers /v1/models, with an 'engine' child in its process group."""
    (tmp_path / "fake_server.py").write_text(FAKE_SERVER)
    return ["python", str(tmp_path / "fake_server.py"), str(tmp_path / "pids")]


def alive(pid: int) -> bool:
    try:
        return Path(f"/proc/{pid}/stat").read_text().split(") ")[1][0] != "Z"
    except FileNotFoundError:
        return False


def gone(*pids: int) -> bool:
    for _ in range(50):
        if not any(alive(p) for p in pids):
            return True
        time.sleep(0.1)
    return False


def typer_exit():
    import typer

    return typer.Exit
