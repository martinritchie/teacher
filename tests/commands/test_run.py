"""`teacher run` (commands/run.py): a source in, a script and an MP3 out."""

from pydantic_ai.exceptions import ModelHTTPError

import teacher.commands.run as run_mod
from teacher.speech import chapters, make_speakable
from teacher.testing import (
    PDF,
    SMALL_MODEL,
    invoke,
    run,
)


def test_no_audio_writes_the_script_only(llm, tts, tmp_path):
    """--no-audio stops after the script: <name>.md is written, and no TTS is started."""
    run(PDF, "--out", tmp_path, "--no-audio")
    assert (
        (tmp_path / f"{PDF.stem}.md")
        .read_text()
        .startswith("## Introduction\n\nAn introduction")
    )
    assert not tts and not (tmp_path / f"{PDF.stem}.mp3").exists()


def test_pdf_in_script_and_audio_out(episode_run):
    """One command turns a local PDF into <name>.md, the script in chapters, and <name>.mp3, which marks them."""
    tts, out = episode_run.tts, episode_run.out
    script = (out / f"{PDF.stem}.md").read_text()
    assert make_speakable(script) == tts[0].script.split("\n\n")
    assert [t for t, _ in chapters(script)] == [
        "Introduction",
        "Authors",
        "Contributions",
        "Piece 1",
    ]
    assert (out / f"{PDF.stem}.mp3").read_bytes()[:3] == b"ID3"


def test_rejected_call_is_an_error(llm, tts, tmp_path):
    """If vLLM rejects a call (for example, a prompt longer than its window), stop, point at --chunk, and write no audio."""
    llm.error = ModelHTTPError(400, SMALL_MODEL, body="maximum context length")
    result = invoke(PDF, "--out", tmp_path, "--model", SMALL_MODEL)
    assert result.exit_code != 0
    assert "--chunk" in result.output and "maximum context length" in result.output
    assert not tts


def test_a_call_rejected_by_another_model_names_it(llm, tts, tmp_path):
    """A rejection from a model other than the script model (the eval judge, out of API credit) names that model,
    with no hint about --chunk."""
    llm.error = ModelHTTPError(
        400, "claude-sonnet-5-5", body="credit balance is too low"
    )
    result = invoke(PDF, "--out", tmp_path, "--model", SMALL_MODEL)
    assert (
        result.exit_code != 0
        and "claude-sonnet-5-5 rejected a call (400)" in result.output
    )
    assert "--chunk" not in result.output


def test_models_are_cli_arguments(llm, tts, tmp_path):
    """--model is the model vLLM serves, with its profile's arguments. --voice reaches the TTS."""
    run(PDF, "--out", tmp_path, "--voice", "aiden")
    assert (
        llm.server[:3] == ["vllm", "serve", SMALL_MODEL] and llm.served == SMALL_MODEL
    )
    assert "--structured-outputs-config" in llm.server  # JSON with no free whitespace
    assert tts[0].voice == "aiden"


def test_the_script_is_saved_even_if_speech_fails(llm, tmp_path, monkeypatch):
    """The script is written before the voice model starts, so a speech failure does not lose it."""

    def broken_speak(paragraphs, voice, server):
        raise RuntimeError("TTS failed")

    monkeypatch.setattr(run_mod, "speak", broken_speak)
    result = invoke(PDF, "--out", tmp_path, "--model", SMALL_MODEL)
    assert result.exit_code != 0
    assert (tmp_path / f"{PDF.stem}.md").read_text().strip()
    assert not (tmp_path / f"{PDF.stem}.mp3").exists()
