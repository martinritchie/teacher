"""`teacher speak` (commands/speak.py): an existing script voiced again, chapters kept."""

import sys
from types import SimpleNamespace

import numpy as np

from typer.testing import CliRunner

import teacher.speech as speech_mod
from teacher.cli import app


def test_speak_voices_each_paragraph_with_the_chosen_voice(tmp_path, monkeypatch):
    """Every paragraph goes to Kokoro with the chosen voice and speed, the accent from the voice's first letter;
    headings are chapters, not speech."""
    made, read = [], []

    class Reader:
        def __init__(self, lang_code, repo_id):
            made.append(lang_code)

        def __call__(self, text, voice, speed, split_pattern):
            read.append((text, voice, speed))
            yield SimpleNamespace(
                audio=SimpleNamespace(
                    cpu=lambda: SimpleNamespace(numpy=lambda: np.zeros(2400))
                )
            )

    monkeypatch.setitem(
        sys.modules, "kokoro", SimpleNamespace(KPipeline=Reader)
    )  # not the real one: it loads torch
    monkeypatch.setattr(speech_mod, "PAUSE_SECONDS", 0.01)
    (tmp_path / "ep.md").write_text(
        "## One\n\nFirst paragraph.\n\n## Two\n\nSecond paragraph."
    )
    args = [
        "speak",
        str(tmp_path / "ep.md"),
        "--out",
        str(tmp_path),
        "--voice",
        "bm_george",
        "--speed",
        "0.9",
    ]
    result = CliRunner().invoke(app, args)
    assert result.exit_code == 0, result.output
    assert made == ["b"] and read == [
        ("First paragraph.", "bm_george", 0.9),
        ("Second paragraph.", "bm_george", 0.9),
    ]
    assert (tmp_path / "ep.mp3").read_bytes()[:3] == b"ID3" and len(
        list((tmp_path / "ep.clips").glob("*.wav"))
    ) == 2
