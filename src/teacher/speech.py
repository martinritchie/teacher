"""Turn a script into audio with Qwen3-TTS on vLLM-Omni: one request per sentence, one clip per paragraph, saved separately and joined."""

import base64
import io
import re
import struct
from dataclasses import dataclass
from pathlib import Path

import httpx
import numpy as np
import soundfile

from teacher.settings import (
    LANGUAGE,
    CHAPTER_PAUSE_SECONDS,
    PAUSE_SECONDS,
    PROMPTS,
    SAMPLE_RATE,
    SENTENCE_PAUSE_SECONDS,
    WORDS_PER_MINUTE,
)

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
    """The spoken paragraphs, with headings, tags and markdown marks removed, since TTS reads markup aloud."""
    return [b for b in _blocks(script) if not b.startswith("#")]


def chapters(script: str) -> list[tuple[str, int]]:
    """Each `#` heading's title, and the number of the spoken paragraph it starts at."""
    found, spoken = [], 0
    for b in _blocks(script):
        found += [(b.lstrip("# "), spoken)] if b.startswith("#") else []
        spoken += not b.startswith("#")
    return [(title, k) for title, k in found if k < spoken]


def _blocks(script: str) -> list[str]:
    script = re.sub(r"(?m)^(#+ .*)$", r"\n\n\1\n\n", re.sub(r"<[^>]*>", "", script))
    blocks = [b.strip() for b in script.split("\n\n") if b.strip()]
    return [
        b if b.startswith("#") else re.sub(r"[#*<>]", "", b).strip() for b in blocks
    ]


@dataclass(frozen=True)
class Voice:
    """How each paragraph is spoken. `style` sends prompts/voice.md, a short instruction for warm, varied
    intonation, to a preset speaker; without it the delivery is flatter (an earlier, longer instruction made voices
    drift, which even_out now corrects). `clone` is a reference clip (a WAV file, with its transcript in a .txt
    beside it) that every paragraph imitates, which needs a Base (voice clone) model and takes its delivery from
    the clip, so no instruction is sent."""

    speaker: str = "ryan"
    style: bool = True
    clone: Path | None = None
    even_pace: bool = False  # stretch every clip to WORDS_PER_MINUTE
    sentences: bool = True  # one request per sentence, joined with short pauses, not one per paragraph


def speak(paragraphs: list[str], voice: Voice, server: str) -> list[np.ndarray]:
    """One clip per paragraph."""
    request = {"voice": voice.speaker, "language": LANGUAGE, "response_format": "wav"}
    if voice.style and not voice.clone:
        request["instructions"] = (PROMPTS / "voice.md").read_text().strip()
    if voice.clone:
        audio = base64.b64encode(voice.clone.read_bytes()).decode()
        request |= {"task_type": "Base", "ref_audio": f"data:audio/wav;base64,{audio}",
                    "ref_text": voice.clone.with_suffix(".txt").read_text().strip()}  # fmt: skip
    pieces = [split_sentences(p) if voice.sentences else [p] for p in paragraphs]
    spoken = iter(
        clip
        for batch in _batches([s for p in pieces for s in p])
        for clip in _synthesise(batch, request, server)
    )
    gap = np.zeros(int(SENTENCE_PAUSE_SECONDS * SAMPLE_RATE))
    clips = [
        np.concatenate([part for _ in p for part in (next(spoken), gap)][:-1])
        for p in pieces
    ]
    return even_out(clips, paragraphs, pace=voice.even_pace)


def split_sentences(paragraph: str) -> list[str]:
    """The paragraph's sentences, to speak one at a time: Qwen3-TTS reads long inputs less reliably."""
    parts = re.split(r"(?<=[.!?])\s+(?=[\"'(]?[A-Z])", paragraph)
    return [s.strip() for s in parts if s.strip()]


def even_out(
    clips: list[np.ndarray], paragraphs: list[str], pace: bool = True
) -> list[np.ndarray]:
    """The clips made to sound like one take. Each paragraph is synthesised on its own and comes out with its own
    tone, loudness and pace, so a listener hears every boundary: match each clip's tonal balance and loudness to
    the episode's median, then, with `pace`, stretch it to WORDS_PER_MINUTE."""
    if not clips or min(len(c) for c in clips) < SAMPLE_RATE // 2:
        return clips  # too short to measure
    from scipy.signal import fftconvolve, firwin2, welch

    bands = np.geomspace(60, 9000, 25)  # third-octave-ish bands of the voice

    def spectrum(clip: np.ndarray) -> np.ndarray:
        freqs, power = welch(clip, SAMPLE_RATE, nperseg=2048)
        return (
            np.array(
                [
                    power[(freqs >= lo) & (freqs < hi)].mean()
                    for lo, hi in zip(bands, bands[1:])
                ]
            )
            + 1e-12
        )

    def level(clip: np.ndarray) -> float:
        frames = clip[: len(clip) // 480 * 480].reshape(-1, 480)  # 20 ms
        rms = np.sqrt((frames**2).mean(1))
        speech = rms[rms > rms.max() / 30]  # not the pauses
        return float(np.sqrt((speech**2).mean())) if speech.size else 0.0

    reference = np.median([spectrum(c) for c in clips], axis=0)
    out = []
    for clip, text in zip(clips, paragraphs):
        gain_db = np.clip(10 * np.log10(reference / spectrum(clip)), -6, 6)
        centres = np.sqrt(bands[:-1] * bands[1:])
        grid = np.linspace(0, SAMPLE_RATE / 2, 513)
        response = 10 ** (np.interp(grid, centres, gain_db) / 20)
        out.append(
            fftconvolve(clip, firwin2(1025, grid / grid[-1], response), mode="same")
        )
    target = np.median([level(c) for c in out])
    out = [c * target / max(level(c), 1e-9) for c in out]
    if not pace:
        return out
    paces = [
        len(t.split()) / (len(c) / SAMPLE_RATE / 60) for c, t in zip(out, paragraphs)
    ]
    return [
        stretch(c, float(np.clip(WORDS_PER_MINUTE / p, 0.7, 1.4)))
        for c, p in zip(out, paces)
    ]


def stretch(
    audio: np.ndarray, rate: float, frame: int = 1024, tolerance: int = 256
) -> np.ndarray:
    """`audio` played `rate` times as fast, pitch unchanged (WSOLA: overlap-add of input frames, each shifted by up
    to `tolerance` samples to best continue the last, so the waveform stays natural rather than phasey)."""
    from scipy.signal import correlate

    if abs(rate - 1) < 0.01:
        return audio
    hop, window, n_out = frame // 2, np.hanning(frame), int(len(audio) / rate)
    padded = np.pad(audio, (tolerance, frame + tolerance))
    out, weight = np.zeros(n_out + frame), np.zeros(n_out + frame)
    position = tolerance
    for k in range(n_out // hop + 1):
        ideal = int(k * hop * rate) + tolerance
        if ideal + frame + tolerance > len(padded):
            break
        if k:
            natural = padded[position + hop : position + hop + frame]
            search = padded[ideal - tolerance : ideal + tolerance + frame]
            position = (
                ideal
                - tolerance
                + int(np.argmax(correlate(search, natural, mode="valid")))
            )
        else:
            position = ideal
        out[k * hop : k * hop + frame] += padded[position : position + frame] * window
        weight[k * hop : k * hop + frame] += window
    return (out / np.maximum(weight, 1e-8))[:n_out].astype(audio.dtype)


def save(
    out: Path,
    name: str,
    paragraphs: list[str],
    clips: list[np.ndarray] = (),
    marks: list[tuple[str, int]] = (),
) -> None:
    """<out>/<name>.md (the spoken script, with a heading at each of `marks`, from `chapters`) and, with clips,
    <out>/<name>.mp3, with chapter marks podcast apps can skip between, and one WAV per paragraph in
    <out>/<name>.clips/, to check or replace single paragraphs."""
    out.mkdir(parents=True, exist_ok=True)
    titles = dict((k, t) for t, k in marks)
    (out / f"{name}.md").write_text("\n\n".join((f"## {titles[k]}\n\n" if k in titles else "") + p for k, p in enumerate(paragraphs)))  # fmt: skip
    if clips:
        audio, starts = _join(clips, set(titles))
        soundfile.write(out / f"{name}.mp3", audio, SAMPLE_RATE)
        if marks:
            ms = [round(1000 * starts[k] / SAMPLE_RATE) for _, k in marks] + [round(1000 * len(audio) / SAMPLE_RATE)]  # fmt: skip
            mp3 = out / f"{name}.mp3"
            mp3.write_bytes(_chapter_tag([(t, ms[i], ms[i + 1]) for i, (t, _) in enumerate(marks)]) + mp3.read_bytes())  # fmt: skip
        (folder := out / f"{name}.clips").mkdir(exist_ok=True)
        for old in folder.glob("*.wav"):  # a longer earlier version's clips
            old.unlink()
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


def _join(
    clips: list[np.ndarray], new_chapters: set[int] = frozenset()
) -> tuple[np.ndarray, list[int]]:
    """The clips with a pause between paragraphs, a longer one before a new chapter; and where each clip starts."""
    parts, starts, at = [], [], 0
    for k, clip in enumerate(clips):
        if k:
            seconds = CHAPTER_PAUSE_SECONDS if k in new_chapters else PAUSE_SECONDS
            parts.append(np.zeros(int(seconds * SAMPLE_RATE)))
            at += len(parts[-1])
        starts.append(at)
        parts.append(clip)
        at += len(clip)
    return np.concatenate(parts), starts


def _chapter_tag(marks: list[tuple[str, int, int]]) -> bytes:
    """An ID3v2.4 tag holding a table of contents and one chapter frame per (title, start ms, end ms)."""
    size = lambda n: bytes((n >> s) & 0x7F for s in (21, 14, 7, 0))  # noqa: E731 (syncsafe)
    frame = lambda kind, data: kind.encode() + size(len(data)) + b"\0\0" + data  # noqa: E731
    title = lambda text: frame("TIT2", b"\3" + text.encode())  # noqa: E731 (UTF-8)
    ids = [f"ch{k}".encode() for k in range(len(marks))]
    toc = (
        b"toc\0\3"
        + bytes([len(ids)])
        + b"".join(i + b"\0" for i in ids)
        + title("Chapters")
    )
    chaps = [frame("CHAP", i + b"\0" + struct.pack(">4I", start, end, 2**32 - 1, 2**32 - 1) + title(t))
             for i, (t, start, end) in zip(ids, marks)]  # fmt: skip
    body = frame("CTOC", toc) + b"".join(chaps)
    return b"ID3\4\0\0" + size(len(body)) + body
