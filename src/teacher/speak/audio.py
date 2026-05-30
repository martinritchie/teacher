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

    # Hard-split any single sentence that alone exceeds the limit, so the
    # grouping loop below only ever sees sentences that can fit in a chunk.
    bounded = []
    for sentence in sentences:
        if len(sentence) > max_chars:
            bounded.extend(
                sentence[i : i + max_chars] for i in range(0, len(sentence), max_chars)
            )
        else:
            bounded.append(sentence)
    sentences = bounded

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


def get_audio_duration(file: Path) -> int:
    """Get duration of an audio file in milliseconds using ffprobe."""
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "quiet",
            "-show_entries",
            "format=duration",
            "-of",
            "csv=p=0",
            str(file),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return int(float(result.stdout.strip()) * 1000)


def write_ffmpeg_chapters(
    sections: list[tuple[str, list[Path]]], metadata_file: Path
) -> None:
    """Write ffmpeg metadata file with chapter markers derived from section durations."""
    lines = [";FFMETADATA1"]
    offset_ms = 0
    for title, files in sections:
        chapter_duration = sum(get_audio_duration(f) for f in files)
        lines.append("[CHAPTER]")
        lines.append("TIMEBASE=1/1000")
        lines.append(f"START={offset_ms}")
        lines.append(f"END={offset_ms + chapter_duration}")
        lines.append(f"title={title}")
        offset_ms += chapter_duration
    metadata_file.write_text("\n".join(lines) + "\n")


def concatenate_audio_files(
    sections: list[tuple[str, list[Path]]], output_file: Path
) -> None:
    """Concatenate audio files into an M4B with chapter markers.

    Args:
        sections: List of (chapter_title, audio_files) tuples
        output_file: Path to write the output file (should be .m4b)
    """
    all_files = [f for _, files in sections for f in files]
    for input_file in all_files:
        if not input_file.exists():
            raise FileNotFoundError(f"Input file not found: {input_file}")

    parent = output_file.parent
    concat_file = parent / "concat_list.txt"
    metadata_file = parent / "metadata.txt"

    concat_file.write_text("".join(f"file '{f.absolute()}'\n" for f in all_files))
    write_ffmpeg_chapters(sections, metadata_file)

    try:
        subprocess.run(
            [
                "ffmpeg",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                str(concat_file),
                "-i",
                str(metadata_file),
                "-map_metadata",
                "1",
                "-c:a",
                "aac",
                "-b:a",
                "128k",
                "-y",
                str(output_file),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
    finally:
        concat_file.unlink(missing_ok=True)
        metadata_file.unlink(missing_ok=True)
