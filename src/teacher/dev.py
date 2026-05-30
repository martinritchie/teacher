"""Development commands for quick pipeline iteration."""

from pathlib import Path
from typing import Annotated

import typer
from elevenlabs import ElevenLabs, VoiceSettings

from teacher.speak.audio import chunk_text, concatenate_audio_files
from teacher.narrate import generate_narrative
from teacher.utils import get_settings, get_step_dir_from_pdf

dev_app = typer.Typer()


def _generate_audio_chunk(
    text: str, output_file: Path, voice_id: str, settings
) -> None:
    """Generate audio for a single text chunk."""
    client = ElevenLabs(api_key=settings.elevenlabs_api_key.get_secret_value())
    audio = client.text_to_speech.convert(
        voice_id=voice_id,
        text=text,
        model_id=settings.elevenlabs_model_id,
        output_format=settings.elevenlabs_output_format,
        voice_settings=VoiceSettings(stability=0.0),
    )

    with open(output_file, "wb") as f:
        for chunk in audio:
            f.write(chunk)


@dev_app.command()
def subsection(
    pdf_path: Annotated[
        Path,
        typer.Argument(help="Path to PDF file"),
    ],
    section: Annotated[
        Path,
        typer.Argument(help="Path to subsection markdown file"),
    ],
    model: Annotated[
        str | None,
        typer.Option(help=f"Model name (default: {get_settings().narrate_model})"),
    ] = None,
    voice_id: Annotated[
        str | None,
        typer.Option(
            help=f"Voice ID to use (default: {get_settings().elevenlabs_voice_id})"
        ),
    ] = None,
) -> None:
    """Chain narrate → speak: markdown → narrative → mp3."""
    settings = get_settings()
    speak_dir = get_step_dir_from_pdf(pdf_path, "speak")
    voice_id = voice_id or settings.elevenlabs_voice_id

    text = section.read_text()
    typer.echo(f"Generating narrative from {section.name}...")
    narrative = generate_narrative(text, model)
    narrative_len = len(narrative)

    narrative_path = speak_dir / "narrative.md"
    narrative_path.write_text(narrative)
    typer.echo(f"Narrative saved to: {narrative_path} ({narrative_len} chars)")

    typer.echo("Converting to audio...")
    audio_files = []

    # Check if narrative needs chunking
    if narrative_len > settings.tts_chunk_size:
        typer.echo(
            f"Narrative exceeds {settings.tts_chunk_size} chars - splitting into chunks"
        )
        chunks = chunk_text(narrative, settings.tts_chunk_size)
        for i, chunk in enumerate(chunks):
            chunk_len = len(chunk)
            chunk_num = i + 1
            chunk_file = speak_dir / f"chunk-{chunk_num:03d}.mp3"
            typer.echo(f"  Chunk {chunk_num}: {chunk_len} chars → {chunk_file.name}")
            _generate_audio_chunk(chunk, chunk_file, voice_id, settings)
            audio_files.append(chunk_file)

        output = speak_dir / "output.mp3"
        typer.echo(f"Concatenating {len(audio_files)} chunks → {output.name}")
        concatenate_audio_files(audio_files, output)
        typer.echo(f"✓ Audio saved to: {output}")
    else:
        output = speak_dir / "output.mp3"
        _generate_audio_chunk(narrative, output, voice_id, settings)
        typer.echo(f"✓ Audio saved to: {output} ({narrative_len} chars)")
