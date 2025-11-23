"""Convert narrative text to audio using text-to-speech service."""

from pathlib import Path
from typing import Annotated

import typer
from elevenlabs import ElevenLabs, VoiceSettings

from teacher.speaker.audio import chunk_text, concatenate_audio_files
from teacher.utils import get_settings, get_step_dir_from_pdf, parse_section_selection

speaker_app = typer.Typer()


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


@speaker_app.command()
def generate(
    pdf_path: Annotated[Path, typer.Argument(help="Path to PDF file")],
    sections: Annotated[
        str | None,
        typer.Option(
            help='Section selection (e.g., "0-5", "0,3,7", "0-2,5,8-10"). Default: all'
        ),
    ] = None,
    voice_id: Annotated[
        str | None,
        typer.Option(
            help=f"Voice ID to use (default: {get_settings().elevenlabs_voice_id})"
        ),
    ] = None,
) -> None:
    """Convert narrative sections to audio using ElevenLabs TTS alongside PDF.

    Supports section selection formats:
    - "0-5": sections 000 through 005
    - "0,3,7": specific sections 000, 003, 007
    - "0-2,5,8-10": combined ranges and individuals
    - None: all sections
    """
    settings = get_settings()
    base_dir = pdf_path.parent
    speaker_dir = get_step_dir_from_pdf(pdf_path, "speaker")
    writer_dir = base_dir / "writer"
    voice_id = voice_id or settings.elevenlabs_voice_id

    # Find all writer section files
    if not writer_dir.exists():
        raise FileNotFoundError(
            f"Writer directory not found at {writer_dir}. Run 'writer process_sections' first."
        )

    all_section_files = sorted(writer_dir.glob("[0-9]*.md"))
    if not all_section_files:
        raise FileNotFoundError(
            f"No section files found in {writer_dir}. Run 'writer process_sections' first."
        )

    # Parse section selection
    try:
        section_files = parse_section_selection(sections, all_section_files)
    except ValueError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)

    audio_files = []
    total_chars = 0

    for section_file in section_files:
        text = section_file.read_text()
        text_len = len(text)
        total_chars += text_len

        # Check if text needs chunking
        if text_len > settings.tts_chunk_size:
            typer.echo(
                f"Processing {section_file.stem}... ({text_len} chars - splitting into chunks)"
            )
            chunks = chunk_text(text, settings.tts_chunk_size)
            for i, chunk in enumerate(chunks):
                chunk_len = len(chunk)
                chunk_num = i + 1
                audio_file = (
                    speaker_dir / f"{section_file.stem}-part-{chunk_num:03d}.mp3"
                )
                typer.echo(
                    f"  Chunk {chunk_num}: {chunk_len} chars → {audio_file.name}"
                )
                _generate_audio_chunk(chunk, audio_file, voice_id, settings)
                audio_files.append(audio_file)
        else:
            typer.echo(f"Processing {section_file.stem}... ({text_len} chars)")
            audio_file = speaker_dir / f"{section_file.stem}.mp3"
            _generate_audio_chunk(text, audio_file, voice_id, settings)
            audio_files.append(audio_file)

    # Concatenate all audio files
    if audio_files:
        output = speaker_dir / "output.mp3"
        typer.echo(
            f"\nConcatenating {len(audio_files)} audio files ({len(section_files)} sections) → {output.name}"
        )
        concatenate_audio_files(audio_files, output)
        typer.echo(f"✓ Audio saved to: {output} (total: {total_chars} chars)")


@speaker_app.command()
def list_voices() -> None:
    """List available voices from ElevenLabs."""
    settings = get_settings()
    client = ElevenLabs(api_key=settings.elevenlabs_api_key.get_secret_value())
    voices = client.voices.get_all()

    for voice in voices.voices:
        typer.echo(f"{voice.voice_id}: {voice.name}")
