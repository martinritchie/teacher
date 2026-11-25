"""Checking spoken clips by machine, so a voice setting can be compared without listening to every run: what
Whisper hears in each clip and in which language, how far that is from the script, how much each clip sounds like
the episode's speaker, and how its delivery (pitch, pitch range, pace) compares with the episode's other clips."""

import re
from collections import Counter
from pathlib import Path

import numpy as np
import soundfile

ASR_MODEL = "openai/whisper-small"
SPEAKER_MODEL = "microsoft/wavlm-base-plus-sv"
SAME_SPEAKER = 0.86  # the speaker model's suggested threshold for "same speaker"
RATE = 16000  # both models take 16 kHz audio
WINDOW = (
    20 * RATE
)  # the speaker model scores long clips in windows of this many samples, then averages
OUTLIER = (
    3.0  # robust z-score beyond which a clip's delivery stands out from the episode
)


def check_clips(
    clips: list[Path], texts: list[str], reference: Path | None = None
) -> list[dict]:
    """One row per clip: seconds, Whisper's transcript, its language, word error rate against the script, and
    speaker similarity to the reference clip or, without one, to the average of the other clips."""
    import torch
    from transformers import AutoFeatureExtractor, WavLMForXVector, pipeline

    device = 0 if torch.cuda.is_available() else -1
    audio = [_load(c) for c in clips]
    asr = pipeline("automatic-speech-recognition", model=ASR_MODEL, device=device)

    # Whisper's long-form transcription, and its timestamp mode, can loop on a clip, repeating text until the WER is
    # meaningless. Each clip is heard as independent 15-second windows without timestamps; the language is read
    # once, from the first window.
    def transcribe(a: np.ndarray) -> dict:
        step = 15 * RATE
        text = [asr({"raw": a[i : i + step], "sampling_rate": RATE}, generate_kwargs={"task": "transcribe"})["text"].strip()
                for i in range(0, len(a), step)]  # fmt: skip
        first = asr({"raw": a[:step], "sampling_rate": RATE}, return_timestamps=True, return_language=True,
                    generate_kwargs={"task": "transcribe"})  # fmt: skip
        return {"text": " ".join(text), "chunks": first.get("chunks", [])}

    heard = [transcribe(a) for a in audio]
    extract = AutoFeatureExtractor.from_pretrained(SPEAKER_MODEL)
    model = (
        WavLMForXVector.from_pretrained(SPEAKER_MODEL)
        .to("cuda" if device == 0 else "cpu")
        .eval()
    )

    def embed(a: np.ndarray) -> np.ndarray:
        windows = [
            a[i : i + WINDOW]
            for i in range(0, len(a), WINDOW)
            if len(a[i : i + WINDOW]) > RATE
        ]
        vectors = []
        for w in windows or [a]:
            inputs = extract(w, sampling_rate=RATE, return_tensors="pt").to(
                model.device
            )
            with torch.no_grad():
                e = model(**inputs).embeddings[0].cpu().numpy()
            vectors.append(e / np.linalg.norm(e))
        mean = np.mean(vectors, axis=0)
        return mean / np.linalg.norm(mean)

    voices = np.stack([embed(a) for a in audio])
    others = (
        voices.sum(0) - voices
    )  # each clip compared with the rest, so it cannot match itself
    targets = (
        np.repeat(embed(_load(reference))[None], len(clips), 0) if reference else others
    )
    similarity = (voices * targets).sum(1) / np.linalg.norm(targets, axis=1)
    rows = []
    for clip, a, h, text, sim in zip(clips, audio, heard, texts, similarity):
        languages = Counter(c.get("language") or "?" for c in h.get("chunks", []))
        pitch, spread = _pitch(a)
        rows.append({"clip": clip.name, "seconds": round(len(a) / RATE, 1), "language": languages.most_common(1)[0][0] if languages else "?",
                     "wer": round(word_error_rate(text, h["text"]), 3), "speaker": round(float(sim), 3),
                     "pitch": pitch, "range": spread, "pace": round(len(text.split()) / (len(a) / RATE), 2), "heard": h["text"].strip()})  # fmt: skip
    for key in (
        "pitch",
        "range",
        "pace",
    ):  # mark delivery that stands out from the rest of the episode
        values = np.array([r[key] for r in rows])
        mad = np.median(np.abs(values - np.median(values)))
        for r, v in zip(
            rows, values
        ):  # no spread (every clip evened to one pace): nothing stands out
            r[f"{key}_z"] = (
                round(float(0.6745 * (v - np.median(values)) / mad), 1)
                if mad > 1e-3 * abs(np.median(values))
                else 0.0
            )
    return rows


def _pitch(audio: np.ndarray) -> tuple[float, float]:
    """Median pitch in Hz, and the spread of pitch (interquartile range) in semitones, over voiced frames."""
    import torch
    import torchaudio

    f0 = torchaudio.functional.detect_pitch_frequency(
        torch.from_numpy(audio)[None], RATE, freq_low=65, freq_high=400
    )
    f0 = f0[0].numpy()
    f0 = f0[(f0 > 65) & (f0 < 400)]
    if len(f0) < 10:
        return 0.0, 0.0
    q1, med, q3 = np.percentile(f0, [25, 50, 75])
    return round(float(med), 1), round(float(12 * np.log2(q3 / q1)), 2)


def summary(rows: list[dict]) -> str:
    off_language = [r["clip"] for r in rows if r["language"] not in ("english", "en")]
    off_voice = [r["clip"] for r in rows if r["speaker"] < SAME_SPEAKER]
    misread = [r["clip"] for r in rows if r["wer"] > 0.25]
    delivery = [
        r["clip"]
        for r in rows
        if max(abs(r["pitch_z"]), abs(r["range_z"]), abs(r["pace_z"])) > OUTLIER
    ]
    wers, sims = [r["wer"] for r in rows], [r["speaker"] for r in rows]
    minutes = sum(r["seconds"] for r in rows) / 60
    return (f"{len(rows)} clips, {minutes:.1f} min | misread (WER > 0.25): {len(misread)} {misread} | "
            f"delivery outliers (|z| > {OUTLIER}): {len(delivery)} {delivery} | not English: {len(off_language)} | "
            f"voice below {SAME_SPEAKER}: {len(off_voice)} | WER median {np.median(wers):.3f}, max {max(wers):.3f} | "
            f"speaker median {np.median(sims):.3f}, min {min(sims):.3f}")  # fmt: skip


def word_error_rate(reference: str, hypothesis: str) -> float:
    """Word-level edit distance over the reference length, ignoring case and punctuation."""
    ref, hyp = _words(reference), _words(hypothesis)
    row = list(range(len(hyp) + 1))
    for i, r in enumerate(ref, start=1):
        prev, row[0] = row[0], i
        for j, h in enumerate(hyp, start=1):
            prev, row[j] = row[j], min(row[j] + 1, row[j - 1] + 1, prev + (r != h))
    return row[-1] / max(len(ref), 1)


def _words(text: str) -> list[str]:
    return re.findall(r"[a-z0-9']+", text.lower().replace("-", " "))


def _load(path: Path) -> np.ndarray:
    from scipy.signal import resample_poly

    audio, rate = soundfile.read(path, dtype="float32")
    audio = audio.mean(1) if audio.ndim > 1 else audio
    return (
        resample_poly(audio, RATE, rate).astype(np.float32) if rate != RATE else audio
    )
