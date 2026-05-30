"""Generate Teacher narratives from academic text using few-shot examples."""

from pathlib import Path
from typing import Annotated

import anthropic
import typer

from teacher.utils import (
    get_settings,
    find_extract_sections,
    get_step_dir_from_pdf,
    parse_section_selection,
)
from teacher.narrate.prompts import (
    get_few_shot_messages,
    narrative_prompt,
    normalizer_prompt,
)

narrate_app = typer.Typer()


def generate_narrative(original_text: str, model: str | None = None) -> str:
    """Generate a Teacher narrative from academic text."""
    settings = get_settings()
    messages = get_few_shot_messages(original_text)

    client = anthropic.Anthropic(api_key=settings.anthropic_api_key.get_secret_value())
    message = client.messages.create(
        model=model or settings.narrate_model,
        max_tokens=settings.narrate_max_tokens,
        thinking={"type": "enabled", "budget_tokens": settings.narrate_thinking_budget},
        system=narrative_prompt(),
        messages=messages,
    )
    narrative = message.content[1].text

    # Second LLM call for ElevenLabs TTS optimization
    processed = client.messages.create(
        model=model or settings.narrate_model,
        max_tokens=settings.narrate_max_tokens,
        system=normalizer_prompt(),
        messages=[{"role": "user", "content": narrative}],
    )
    return processed.content[0].text


@narrate_app.command()
def generate(
    input_file: Annotated[
        Path, typer.Argument(help="Input file containing text to convert to narrative")
    ],
    output: Annotated[
        Path,
        typer.Option(help="Output markdown file path"),
    ],
    model: Annotated[
        str | None,
        typer.Option(help=f"Model name (default: {get_settings().narrate_model})"),
    ] = None,
) -> None:
    """Generate a Teacher narrative from academic text."""
    output.parent.mkdir(parents=True, exist_ok=True)
    text = input_file.read_text()
    narrative = generate_narrative(text, model)
    output.write_text(narrative)
    typer.echo(f"Narrative saved to {output}")


@narrate_app.command()
def process_sections(
    pdf_path: Annotated[Path, typer.Argument(help="Path to PDF file")],
    sections: Annotated[
        str | None,
        typer.Option(
            help='Section selection (e.g., "0-5", "0,3,7", "0-2,5,8-10", or section names). Default: all'
        ),
    ] = None,
    model: Annotated[
        str | None,
        typer.Option(help=f"Model name (default: {get_settings().narrate_model})"),
    ] = None,
) -> None:
    """Process extract sections and save individual narratives alongside PDF.

    Supports section selection formats:
    - "0-5": sections 000 through 005
    - "0,3,7": specific sections 000, 003, 007
    - "0-2,5,8-10": combined ranges and individuals
    - None: all sections
    """
    base_dir = pdf_path.parent
    sections_dir = find_extract_sections(base_dir)
    narrate_dir = get_step_dir_from_pdf(pdf_path, "narrate")
    all_sections = sorted(sections_dir.glob("[0-9]*.md"))

    # Parse section selection
    try:
        selected_sections = parse_section_selection(sections, all_sections)
    except ValueError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)

    for section_file in selected_sections:
        typer.echo(f"Processing {section_file.name}...")
        narrative = generate_narrative(section_file.read_text(), model)
        output_file = narrate_dir / section_file.name
        output_file.write_text(narrative)
        typer.echo(f"  Saved: {output_file.name}")
    typer.echo(f"Processed {len(selected_sections)} section(s) saved to {narrate_dir}")
