"""Utilities for loading reader prompts."""

from pathlib import Path

PROMPTS_DIR = Path(__file__).parent / "prompts"
SYSTEM_PATH = Path(PROMPTS_DIR, "system")


def get_reader_prompt(pdf_path: str, output_dir: str) -> str:
    """Load and format the PDF-to-markdown reader prompt.

    Args:
        pdf_path: Path to the PDF file to convert
        output_dir: Directory to write markdown files to

    Returns:
        Formatted reader prompt ready for LLM consumption
    """
    prompt_path = Path(SYSTEM_PATH, "reader.md")
    return prompt_path.read_text().format(pdf_path=pdf_path, output_dir=output_dir)
