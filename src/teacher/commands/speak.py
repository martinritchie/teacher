"""`teacher speak`: voice an existing script again, to compare voice settings without rewriting the script."""

from pathlib import Path
from typing import Annotated

import typer

from teacher.servers import serve_voice_model
from teacher.settings import VOICE, VOICE_CLONE_MODEL, VOICE_MODEL, VOICE_SAMPLING
from teacher.speech import Voice, chapters, make_speakable, save, speak


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
        VOICE_SAMPLING["temperature"],
        help="Sampling temperature of the TTS model (vLLM-Omni's default: 0.9)",
    ),
    top_p: float = typer.Option(
        VOICE_SAMPLING["top_p"],
        help="Nucleus sampling of the TTS model's first stage (vLLM-Omni's default: 1.0)",
    ),
    top_k: int = typer.Option(
        VOICE_SAMPLING["top_k"],
        help="Top-k sampling of the TTS model's first stage (vLLM-Omni's default: 50)",
    ),
    sentences: bool = typer.Option(
        True,
        help="One TTS request per sentence, joined with short pauses (off: one per paragraph)",
    ),
    group_chars: int = typer.Option(
        0,
        help="With --sentences, pack neighbouring sentences into requests of up to this many characters",
    ),
    seed: int = typer.Option(
        None, help="Sampling seed for every TTS request (default: random)"
    ),
    clone: Path = typer.Option(
        None,
        help="A reference WAV, with its transcript in a .txt beside it, for every paragraph to imitate; uses the Base (voice clone) model",
    ),
    even_pace: bool = typer.Option(
        False,
        help="Stretch every paragraph to WORDS_PER_MINUTE (off: the model's own pace)",
    ),
    out: Path = typer.Option(Path("out/speak"), help="Output directory"),
    name: str = typer.Option(None, help="Output name; defaults to the script's"),
):
    """Speak <script> into <out>/<name>.mp3, with one WAV per paragraph in <out>/<name>.clips/."""
    text = script.read_text()
    paragraphs = make_speakable(text)
    name = name or script.stem
    out.mkdir(parents=True, exist_ok=True)
    model = VOICE_CLONE_MODEL if clone else VOICE_MODEL
    sampling = dict(temperature=temperature, top_p=top_p, top_k=top_k) | (
        {"seed": seed} if seed is not None else {}
    )
    with serve_voice_model(model, out / f"{name}.voice-model.log", sampling) as tts:
        clips = speak(
            paragraphs,
            Voice(
                speaker=voice,
                style=style,
                clone=clone,
                even_pace=even_pace,
                sentences=sentences,
                group_chars=group_chars,
            ),
            tts,
        )
    save(out, name, paragraphs, clips, chapters(text))
    typer.echo(f"Wrote {out / name}.mp3 and {len(clips)} clips in {out / name}.clips/")
