"""Utilities for loading extract prompts."""

from pathlib import Path

PROMPTS_DIR = Path(__file__).parent / "prompts"
SYSTEM_PATH = Path(PROMPTS_DIR, "system")


def get_extract_prompt(pdf_path: str, output_dir: str) -> str:
    """Load and format the PDF-to-markdown extract prompt.

    Args:
        pdf_path: Path to the PDF file to convert
        output_dir: Directory to write markdown files to

    Returns:
        Formatted extract prompt ready for LLM consumption
    """
    prompt_path = Path(SYSTEM_PATH, "extract.md")
    return prompt_path.read_text().format(pdf_path=pdf_path, output_dir=output_dir)
