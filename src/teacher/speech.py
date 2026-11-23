"""Turn a script into audio with Qwen3-TTS on vLLM-Omni: one clip per paragraph, saved separately and joined."""

import base64
import io
import re
from dataclasses import dataclass
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


def spell_numbers(text: str) -> str:
    """Numbers written in digits, in words, as a reader would say them: "0.5" is "zero point five", "15%" is
    "fifteen percent". Digits inside a word or a symbol ("A.1", "x2", "1/n") are left for the writer."""
    from decimal import Decimal

    from num2words import num2words

    text = re.sub(r"(?<![\w.])(\d+(?:\.\d+)?)\s?%", r"\1 percent", text)
    return re.sub(
        r"(?<![\w./])\d+(?:\.\d+)?(?![\w/]|\.\d)",
        lambda m: num2words(Decimal(m.group())),
        text,
    )


def make_speakable(script: str) -> list[str]:
    """Paragraphs with tags and markdown marks removed, since TTS reads markup aloud."""
    plain = re.sub(r"[#*<>]", "", re.sub(r"<[^>]*>", "", script))
    return [p.strip() for p in plain.split("\n\n") if p.strip()]


@dataclass(frozen=True)
class Voice:
    """How each paragraph is spoken. By default, the speaker as Qwen3-TTS speaks with no instruction: an instruction
    made voices and tone drift between paragraphs. `style` sends prompts/voice.md as the instruction; `clone` is a
    reference clip (a WAV file, with its transcript in a .txt beside it) that every paragraph imitates, which
    needs a Base (voice clone) model."""

    speaker: str = "ryan"
    style: bool = False
    clone: Path | None = None


def speak(paragraphs: list[str], voice: Voice, server: str) -> list[np.ndarray]:
    """One clip per paragraph."""
    request = {"voice": voice.speaker, "language": LANGUAGE, "response_format": "wav"}
    if voice.style:
        request["instructions"] = (PROMPTS / "voice.md").read_text().strip()
    if voice.clone:
        audio = base64.b64encode(voice.clone.read_bytes()).decode()
        request |= {"task_type": "Base", "ref_audio": f"data:audio/wav;base64,{audio}",
                    "ref_text": voice.clone.with_suffix(".txt").read_text().strip()}  # fmt: skip
    return [
        clip
        for batch in _batches(paragraphs)
        for clip in _synthesise(batch, request, server)
    ]


def save(
    out: Path, name: str, paragraphs: list[str], clips: list[np.ndarray] = ()
) -> None:
    """<out>/<name>.md (the spoken script) and, with clips, <out>/<name>.mp3 and one WAV per paragraph in
    <out>/<name>.clips/, to check or replace single paragraphs."""
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{name}.md").write_text("\n\n".join(paragraphs))
    if clips:
        soundfile.write(out / f"{name}.mp3", _join(clips), SAMPLE_RATE)
        (folder := out / f"{name}.clips").mkdir(exist_ok=True)
        for i, clip in enumerate(clips, start=1):
            soundfile.write(folder / f"{i:03d}.wav", clip, SAMPLE_RATE)


def _batches(paragraphs: list[str]) -> list[list[str]]:
    return [paragraphs[i : i + _BATCH] for i in range(0, len(paragraphs), _BATCH)]


def _synthesise(batch: list[str], request: dict, server: str) -> list[np.ndarray]:
    body = request | {"items": [{"input": paragraph} for paragraph in batch]}
    reply = httpx.post(f"{server}/v1/audio/speech/batch", json=body, timeout=None)
    return [_decode(result) for result in reply.raise_for_status().json()["results"]]


def _decode(result: dict) -> np.ndarray:
    if result["status"] != "success":
        raise RuntimeError(f"TTS failed: {result['error']}")
    audio, _ = soundfile.read(io.BytesIO(base64.b64decode(result["audio_data"])))
    return audio


def _join(clips: list[np.ndarray]) -> np.ndarray:
    pause = np.zeros(int(PAUSE_SECONDS * SAMPLE_RATE))
    return np.concatenate([part for clip in clips for part in (clip, pause)][:-1])
