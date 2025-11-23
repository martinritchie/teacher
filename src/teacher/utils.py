"""Shared utilities: configuration, paths, and section selection."""

from pathlib import Path

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with sensible defaults."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Reader settings
    reader_model: str = Field(
        default="claude-haiku-4-5",
        description="Model to use for PDF reading",
    )

    # Writer settings
    writer_model: str = Field(
        default="claude-sonnet-4-5",
        description="Model to use for narrative generation",
    )
    writer_max_tokens: int = Field(
        default=5000,
        description="Maximum tokens for writer output",
    )
    writer_thinking_budget: int = Field(
        default=1600,
        description="Budget tokens for extended thinking",
    )
    writer_examples_dir: Path | None = Field(
        default=None,
        description="Path to writer examples directory",
    )

    # Speaker settings
    elevenlabs_api_key: SecretStr = Field(
        default="",
        description="ElevenLabs API key (secret)",
    )
    elevenlabs_voice_id: str = Field(
        default="XfNU2rGpBa01ckF309OY",
        description="Default voice ID for TTS",
    )
    elevenlabs_model_id: str = Field(
        default="eleven_turbo_v2_5",
        description="Model ID for TTS generation",
    )
    elevenlabs_output_format: str = Field(
        default="mp3_44100_128",
        description="Audio output format (codec_sample_rate_bitrate)",
    )
    tts_chunk_size: int = Field(
        default=38000,
        description="Maximum characters per TTS request (safety margin below API limit)",
    )

    # API settings
    anthropic_api_key: SecretStr = Field(
        description="Anthropic API key (secret)",
    )

    @property
    def resolved_examples_dir(self) -> Path:
        """Resolve examples directory with fallback to cwd."""
        if self.writer_examples_dir:
            return self.writer_examples_dir
        return Path.cwd() / "prompts" / "teacher-examples"


def get_settings() -> Settings:
    """Get application settings instance."""
    return Settings()


def get_step_dir_from_pdf(pdf_path: Path, step_name: str) -> Path:
    """Get the output directory for a specific step, alongside the PDF.

    Creates the directory if it doesn't exist.

    Args:
        pdf_path: Path to the source PDF file
        step_name: Name of the step ('reader', 'writer', 'speaker')

    Returns:
        Path to the step directory
    """
    step_dir = pdf_path.parent / step_name
    step_dir.mkdir(parents=True, exist_ok=True)
    return step_dir


def find_reader_sections(base_dir: Path) -> Path:
    """Get the reader output directory (where markdown sections are stored).

    Args:
        base_dir: Base directory containing reader/ subdirectory

    Returns:
        Path to the reader directory

    Raises:
        FileNotFoundError: If no markdown sections are found
    """
    reader_dir = base_dir / "reader"
    if not list(reader_dir.glob("[0-9]*.md")):
        raise FileNotFoundError(
            f"No markdown sections found in {reader_dir}. Run 'reader convert' first."
        )
    return reader_dir


def find_writer_output(base_dir: Path) -> Path:
    """Get the writer output file.

    Args:
        base_dir: Base directory containing writer/ subdirectory

    Returns:
        Path to the writer script file

    Raises:
        FileNotFoundError: If script is not found
    """
    writer_file = base_dir / "writer" / "script.md"
    if not writer_file.exists():
        raise FileNotFoundError(
            f"Script not found at {writer_file}. Run 'writer process_sections' first."
        )
    return writer_file


def parse_section_selection(
    sections_str: str | None, available_files: list[Path]
) -> list[Path]:
    """Parse section selection string and return matching files.

    Formats supported:
    - "0-5": Range from 000 to 005
    - "0,3,7": Individual sections 000, 003, 007
    - "0-2,5,8-10": Combined ranges and individuals
    - "abstract,intro": Match by filename stem
    - None: Return all files

    Args:
        sections_str: Section selection string (None = all sections)
        available_files: List of available section files, sorted

    Returns:
        Filtered list of files matching selection, in sorted order

    Raises:
        ValueError: If section selection format is invalid or section not found
    """
    if sections_str is None:
        return available_files

    # Build a map of section indices and stems for easy lookup
    section_map = {}
    for f in available_files:
        # Extract section number from filename (e.g., "000-abstract.md" -> 0)
        stem = f.stem
        try:
            section_num = int(stem.split("-")[0])
            section_map[section_num] = f
            # Also map by name (e.g., "abstract" -> f)
            section_name = "-".join(stem.split("-")[1:])
            section_map[section_name] = f
        except (ValueError, IndexError):
            continue

    selected_indices = set()

    # Parse selection string (e.g., "0-2,5,8-10")
    for part in sections_str.split(","):
        part = part.strip()

        # Check if it's a range (e.g., "0-2")
        if "-" in part and part[0].isdigit():
            try:
                start, end = part.split("-")
                start_idx = int(start.strip())
                end_idx = int(end.strip())
                selected_indices.update(range(start_idx, end_idx + 1))
            except (ValueError, IndexError) as e:
                raise ValueError(f"Invalid range format: {part}") from e
        else:
            # Try as integer index
            try:
                idx = int(part)
                selected_indices.add(idx)
            except ValueError:
                # Try as section name (e.g., "abstract", "introduction")
                if part in section_map:
                    # Find the index of this file
                    for f in available_files:
                        if f.stem == part or f.stem.endswith(f"-{part}"):
                            try:
                                section_num = int(f.stem.split("-")[0])
                                selected_indices.add(section_num)
                            except ValueError:
                                pass
                            break
                else:
                    raise ValueError(f"Section not found: {part}")

    # Filter available files to only selected ones
    result = [
        f for f in available_files if int(f.stem.split("-")[0]) in selected_indices
    ]

    if not result:
        raise ValueError(f"No sections matched selection: {sections_str}")

    return sorted(result)
