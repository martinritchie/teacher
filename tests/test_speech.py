"""Speech (speech.py): markup removed, one clip per paragraph, and real Kokoro in a functional test."""

import re


import pytest

import teacher.commands.run as run_mod
from teacher.settings import (
    SAMPLE_RATE,
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
def test_voice_model_writes_playable_audio():
    """Real Kokoro, no stub: two paragraphs become two clips of audio, over two seconds in all, and the same text
    takes the same time again (Kokoro has no sampled voice to drift; only its decoder adds a little noise)."""
    from teacher.speech import Voice, speak

    clips = speak(["The authors train an autoencoder.", "Then they predict."], Voice())
    assert len(clips) == 2 and sum(len(c) for c in clips) / SAMPLE_RATE > 2
    assert len(speak(["Then they predict."], Voice())[0]) == len(clips[1])


def test_numbers_are_spelled_as_spoken():
    """Digits become words; digits inside words and symbols are left for the writer to rephrase."""
    from teacher.speech import spell_numbers

    text = "Use 128 dimensions, a floor of 0.5, and 15% masking, as in A.1 with x2 and 1/n."
    assert spell_numbers(text) == (
        "Use one hundred and twenty-eight dimensions, a floor of zero point five, and fifteen percent masking, "
        "as in A.1 with x2 and 1/n."
    )
