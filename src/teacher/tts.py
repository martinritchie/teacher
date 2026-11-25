"""Turn a script into audio with Kokoro, in-process: one clip per paragraph, saved separately and joined into an MP3 with chapter marks."""

import re
import struct
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import soundfile

from teacher.settings import (
    CHAPTER_PAUSE_SECONDS,
    PAUSE_SECONDS,
    SAMPLE_RATE,
    VOICE,
    VOICE_MODEL,
)

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
    """Who reads, and how fast: a Kokoro voice, whose first letter picks the accent (`am_michael`: a for American,
    b for British), and a speed (1 is the voice's own)."""

    name: str = VOICE
    speed: float = 1.0


def synthesize(paragraphs: list[str], voice: Voice = Voice()) -> list[np.ndarray]:
    """One clip per paragraph, from Kokoro on the GPU, or the CPU without one. Kokoro splits a long paragraph into
    pieces it can read itself. Nothing about the voice is sampled, so it cannot drift between paragraphs."""
    from kokoro import KPipeline

    reader = KPipeline(
        lang_code=voice.name[0], repo_id=VOICE_MODEL
    )  # on the GPU if there is one
    return [np.concatenate([r.audio.cpu().numpy() for r in reader(p, voice=voice.name, speed=voice.speed, split_pattern=None) if r.audio is not None])
            for p in paragraphs]  # fmt: skip


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
