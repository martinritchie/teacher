"""Speech (speech.py): markup removed, one clip per paragraph, and real Qwen3-TTS in a functional test."""

import re

import numpy as np

import pytest

import teacher.commands.run as run_mod
from teacher.settings import (
    SAMPLE_RATE,
    VOICE_MODEL,
)
from teacher.testing import (
    PDF,
    run,
)


def test_markup_never_reaches_tts(llm, tts, tmp_path, monkeypatch):
    """TTS reads markup aloud. Remove break tags and markdown marks even if the model writes them."""
    dirty = '# Intro\n\nThe **loss** falls. <break time="1.0s" /> Then it stops.'
    monkeypatch.setattr(run_mod, "write_episode", lambda *a, **k: dirty)
    run(PDF, "--out", tmp_path)
    assert not re.search(r"[#*<>]", tts[0].script)
    assert "The loss falls." in tts[0].script


def test_run_saves_one_clip_per_paragraph(episode_run):
    """Besides the MP3, every paragraph is saved as its own WAV, to check or redo single paragraphs."""
    tts, out = episode_run.tts, episode_run.out
    paragraphs = tts[0].script.split("\n\n")
    clips = sorted((out / f"{PDF.stem}.clips").glob("*.wav"))
    assert [c.name for c in clips[:2]] == ["001.wav", "002.wav"] and len(clips) == len(
        paragraphs
    )


@pytest.mark.functional
def test_voice_model_writes_playable_audio(tmp_path):
    """Real Qwen3-TTS on vLLM-Omni, no stub: two paragraphs become audio of more than two seconds."""
    from teacher.servers import serve_voice_model
    from teacher.speech import Voice, speak

    with serve_voice_model(VOICE_MODEL, tmp_path / "voice.log") as server:
        clips = speak(
            ["The authors train an autoencoder.", "Then they predict."], Voice(), server
        )
    assert len(clips) == 2 and sum(len(c) for c in clips) / SAMPLE_RATE > 2


def test_numbers_are_spelled_as_spoken():
    """Digits become words; digits inside words and symbols are left for the writer to rephrase."""
    from teacher.speech import spell_numbers

    text = "Use 128 dimensions, a floor of 0.5, and 15% masking, as in A.1 with x2 and 1/n."
    assert spell_numbers(text) == (
        "Use one hundred and twenty-eight dimensions, a floor of zero point five, and fifteen percent masking, "
        "as in A.1 with x2 and 1/n."
    )


def test_stretch_slows_speech_without_changing_its_pitch():
    """WSOLA: the same tone, a quarter longer at rate 0.8."""
    from teacher.speech import stretch

    t = np.arange(SAMPLE_RATE) / SAMPLE_RATE
    tone = np.sin(2 * np.pi * 220 * t).astype(np.float32)
    slow = stretch(tone, 0.8)

    def peak(a):
        return np.argmax(np.abs(np.fft.rfft(a))) * SAMPLE_RATE / len(a)

    assert len(slow) == int(SAMPLE_RATE / 0.8) and abs(peak(slow) - 220) < 2


def test_clips_are_evened_out_to_one_loudness_and_pace():
    """Each paragraph is synthesised on its own; afterwards every clip has the episode's median loudness and
    speaks at WORDS_PER_MINUTE, so the boundaries between paragraphs cannot be heard."""
    from teacher.settings import WORDS_PER_MINUTE
    from teacher.speech import even_out

    rng = np.random.default_rng(0)

    def noise(seconds, level):
        return (level * rng.standard_normal(int(seconds * SAMPLE_RATE))).astype(
            np.float32
        )

    clips, texts = (
        [noise(10, 0.05), noise(10, 0.2)],
        ["word " * 25, "word " * 15],
    )  # 150 and 90 words a minute
    even = even_out(clips, texts)
    rms = [float(np.sqrt(np.mean(c**2))) for c in even]
    assert abs(rms[0] - rms[1]) / rms[0] < 0.1
    paces = [len(t.split()) / (len(c) / SAMPLE_RATE / 60) for c, t in zip(even, texts)]
    assert all(abs(p - WORDS_PER_MINUTE) < 2 for p in paces)
