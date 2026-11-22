"""Turn a script into audio with Qwen3-TTS on vLLM-Omni."""

import base64
import io
import re
from pathlib import Path

import httpx
import numpy as np
import soundfile

from teacher.settings import LANGUAGE, PAUSE_SECONDS, PROMPTS, SAMPLE_RATE

_BATCH = 8  # paragraphs per request
UNSPOKEN = re.compile(
    r"\S*(?:[=%_\[\]{}^\\|~<>²³]|\d|[α-ωΑ-Ω])\S*"
)  # words TTS reads badly


def unspoken(text: str) -> list[str]:
    """A problem naming each word with a symbol or digit in it, or none."""
    found = list(dict.fromkeys(UNSPOKEN.findall(text)))[:12]
    return [f"Write these as they are spoken, with no symbols or digits: {', '.join(found)}"] if found else []  # fmt: skip


def make_speakable(script: str) -> list[str]:
    """Paragraphs with tags and markdown marks removed, since TTS reads markup aloud."""
    plain = re.sub(r"[#*<>]", "", re.sub(r"<[^>]*>", "", script))
    return [p.strip() for p in plain.split("\n\n") if p.strip()]


def speak(paragraphs: list[str], voice: str, server: str) -> np.ndarray:
    """One clip per paragraph, joined with short pauses."""
    style = (PROMPTS / "voice.md").read_text().strip()
    clips = [
        clip
        for batch in _batches(paragraphs)
        for clip in _synthesise(batch, voice, style, server)
    ]
    return _join(clips)


def save(out: Path, name: str, paragraphs: list[str], audio: np.ndarray | bool) -> None:
    """<out>/<name>.md (the spoken script) and, unless audio is False, <out>/<name>.mp3."""
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{name}.md").write_text("\n\n".join(paragraphs))
    if audio is not False:
        soundfile.write(out / f"{name}.mp3", audio, SAMPLE_RATE)


def _batches(paragraphs: list[str]) -> list[list[str]]:
    return [paragraphs[i : i + _BATCH] for i in range(0, len(paragraphs), _BATCH)]


def _synthesise(
    batch: list[str], voice: str, style: str, server: str
) -> list[np.ndarray]:
    request = {
        "items": [{"input": paragraph} for paragraph in batch],
        "voice": voice,
        "language": LANGUAGE,
        "instructions": style,
        "response_format": "wav",
    }
    reply = httpx.post(f"{server}/v1/audio/speech/batch", json=request, timeout=None)
    return [_decode(result) for result in reply.raise_for_status().json()["results"]]


def _decode(result: dict) -> np.ndarray:
    if result["status"] != "success":
        raise RuntimeError(f"TTS failed: {result['error']}")
    audio, _ = soundfile.read(io.BytesIO(base64.b64decode(result["audio_data"])))
    return audio


def _join(clips: list[np.ndarray]) -> np.ndarray:
    pause = np.zeros(int(PAUSE_SECONDS * SAMPLE_RATE))
    return np.concatenate([part for clip in clips for part in (clip, pause)][:-1])
