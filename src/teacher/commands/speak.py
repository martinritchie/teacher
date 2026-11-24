"""`teacher speak`: voice an existing script again, to compare voice settings without rewriting the script."""

from pathlib import Path
from typing import Annotated

import typer

from teacher.servers import serve_voice_model
from teacher.settings import VOICE, VOICE_CLONE_MODEL, VOICE_MODEL
from teacher.speech import Voice, save, speak


def speak_script(
    script: Annotated[
        Path,
        typer.Argument(
            help="A script, one paragraph per blank-line block (e.g. out/run/<name>.md)"
        ),
    ],
    voice: str = typer.Option(VOICE, help="Qwen3-TTS speaker"),
    style: bool = typer.Option(
        True,
        help="Send prompts/voice.md, the speaking-style instruction, to a preset speaker (off: the model's own delivery)",
    ),
    temperature: float = typer.Option(
        None, help="Sampling temperature of the TTS model (vLLM-Omni's default: 0.9)"
    ),
    clone: Path = typer.Option(
        None,
        help="A reference WAV, with its transcript in a .txt beside it, for every paragraph to imitate; uses the Base (voice clone) model",
    ),
    out: Path = typer.Option(Path("out/speak"), help="Output directory"),
    name: str = typer.Option(None, help="Output name; defaults to the script's"),
):
    """Speak <script> into <out>/<name>.mp3, with one WAV per paragraph in <out>/<name>.clips/."""
    paragraphs = [p.strip() for p in script.read_text().split("\n\n") if p.strip()]
    name = name or script.stem
    out.mkdir(parents=True, exist_ok=True)
    model = VOICE_CLONE_MODEL if clone else VOICE_MODEL
    with serve_voice_model(model, out / f"{name}.voice-model.log", temperature) as tts:
        clips = speak(paragraphs, Voice(speaker=voice, style=style, clone=clone), tts)
    save(out, name, paragraphs, clips)
    typer.echo(f"Wrote {out / name}.mp3 and {len(clips)} clips in {out / name}.clips/")
