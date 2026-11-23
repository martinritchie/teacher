"""Speech (speech.py): markup removed, one clip per paragraph, and real Qwen3-TTS in a functional test."""

import re

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
