"""Text chunking and audio concatenation utilities for TTS processing."""

import subprocess
from pathlib import Path


def chunk_text(text: str, max_chars: int = 38000) -> list[str]:
    """Split text into chunks at sentence boundaries.

    Splits at sentence boundaries (`. `, `! `, `? `) to maintain readability.
    Each chunk stays under max_chars limit.

    Args:
        text: Text to split
        max_chars: Maximum characters per chunk (default: 38000, safe margin below 40k limit)

    Returns:
        List of text chunks
    """
    if len(text) <= max_chars:
        return [text]

    chunks = []
    current_chunk = ""

    # Split by sentences (periods, exclamation marks, question marks followed by space)
    sentences = []
    current_sentence = ""
    for i, char in enumerate(text):
        current_sentence += char
        if char in ".!?" and i + 1 < len(text) and text[i + 1] == " ":
            sentences.append(current_sentence)
            current_sentence = ""

    if current_sentence:
        sentences.append(current_sentence)

    # Group sentences into chunks
    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= max_chars:
            current_chunk += sentence
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


def concatenate_audio_files(input_files: list[Path], output_file: Path) -> None:
    """Concatenate multiple MP3 files using ffmpeg.

    Args:
        input_files: List of paths to MP3 files to concatenate (in order)
        output_file: Path to write the concatenated MP3 file

    Raises:
        subprocess.CalledProcessError: If ffmpeg command fails
        FileNotFoundError: If any input file is not found
    """
    # Verify all input files exist
    for input_file in input_files:
        if not input_file.exists():
            raise FileNotFoundError(f"Input file not found: {input_file}")

    # Create concat demuxer file
    concat_file = output_file.parent / "concat_list.txt"
    with open(concat_file, "w") as f:
        for input_file in input_files:
            f.write(f"file '{input_file.absolute()}'\n")

    try:
        # Use ffmpeg concat demuxer
        subprocess.run(
            [
                "ffmpeg",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                str(concat_file),
                "-c",
                "copy",
                "-y",
                str(output_file),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
    finally:
        # Clean up temp file
        concat_file.unlink(missing_ok=True)
