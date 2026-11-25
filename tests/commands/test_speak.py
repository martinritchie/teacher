"""`teacher speak` (commands/speak.py): voice an existing script with chosen voice settings."""

import base64
import io
from contextlib import contextmanager
from types import SimpleNamespace

import numpy as np
import soundfile
from typer.testing import CliRunner

from teacher.cli import app
from teacher.settings import (
    SAMPLE_RATE,
    VOICE_CLONE_MODEL,
)


def test_speak_sends_the_chosen_voice_settings(tmp_path, monkeypatch):
    """`teacher speak` voices an existing script with the style instruction; --clone sends no instruction but the
    reference clip and its transcript to the Base model, and --temperature reaches the server's deploy config."""
    import teacher.commands.speak as speak_mod
    import teacher.speech as speech_mod

    sent, served = [], []

    @contextmanager
    def server(model, log, sampling=None):
        served.append((model, sampling))
        yield "http://tts"

    def post(url, json, timeout):
        sent.append(json)
        wav = io.BytesIO()
        soundfile.write(wav, np.zeros(2400), SAMPLE_RATE, format="WAV")
        result = {
            "status": "success",
            "audio_data": base64.b64encode(wav.getvalue()).decode(),
        }
        return SimpleNamespace(raise_for_status=lambda: SimpleNamespace(json=lambda: {"results": [result] * len(json["items"])}))  # fmt: skip

    monkeypatch.setattr(speak_mod, "serve_voice_model", server)
    monkeypatch.setattr(speech_mod.httpx, "post", post)
    (tmp_path / "ep.md").write_text("First paragraph.\n\nSecond paragraph.")
    (tmp_path / "ref.wav").write_bytes(b"RIFF")
    (tmp_path / "ref.txt").write_text("The reference words.")
    result = CliRunner().invoke(app, ["speak", str(tmp_path / "ep.md"), "--out", str(tmp_path), "--temperature", "0.5", "--top-k", "30", "--clone", str(tmp_path / "ref.wav")])  # fmt: skip
    assert result.exit_code == 0, result.output
    assert served == [
        (VOICE_CLONE_MODEL, {"temperature": 0.5, "top_p": 0.85, "top_k": 30})
    ]
    body = sent[0]
    assert [i["input"] for i in body["items"]] == [
        "First paragraph.",
        "Second paragraph.",
    ]
    assert (
        "instructions" not in body
        and body["task_type"] == "Base"
        and body["ref_text"] == "The reference words."
    )
    assert len(list((tmp_path / "ep.clips").glob("*.wav"))) == 2
    sent.clear()
    result = CliRunner().invoke(
        app, ["speak", str(tmp_path / "ep.md"), "--out", str(tmp_path)]
    )
    assert result.exit_code == 0, result.output
    assert (
        sent[0]["instructions"].startswith("Explaining an idea")
        and sent[0]["voice"] == "ryan"
    )
