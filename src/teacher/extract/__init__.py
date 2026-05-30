"""Convert PDF to markdown sections using Claude Agent SDK with pdf-reader-mcp."""

from pathlib import Path
from typing import Annotated

import anyio
import typer
from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ClaudeSDKClient,
    ResultMessage,
    TextBlock,
)
from claude_agent_sdk.types import McpStdioServerConfig

from teacher.extract.prompts import get_extract_prompt
from teacher.utils import get_settings, get_step_dir_from_pdf

extract_app = typer.Typer()


async def convert_async(pdf_path: Path, model: str | None = None) -> None:
    """Async conversion logic using ClaudeSDKClient."""
    settings = get_settings()
    output_dir = get_step_dir_from_pdf(pdf_path, "extract")
    mcp_config = McpStdioServerConfig(
        command="npx",
        args=["-y", "@sylphxai/pdf-reader-mcp"],
    )

    options = ClaudeAgentOptions(
        mcp_servers={"pdf-reader": mcp_config},
        model=model or settings.extract_model,
        permission_mode="acceptEdits",
        max_buffer_size=1024 * 1024 * 50,
        env={"ANTHROPIC_API_KEY": settings.anthropic_api_key.get_secret_value()},
    )

    async with ClaudeSDKClient(options=options) as client:
        prompt = get_extract_prompt(
            str(pdf_path.absolute()), str(output_dir.absolute())
        )
        await client.query(prompt)

        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        typer.echo(block.text)
            elif isinstance(message, ResultMessage):
                if message.is_error:
                    typer.echo(f"✗ Error: {message.result}", err=True)
                    raise typer.Exit(1)
                typer.echo(f"✓ Conversion complete (${message.total_cost_usd:.4f})")


@extract_app.command()
def convert(
    pdf_path: Annotated[Path, typer.Argument(help="Path to PDF file")],
    model: Annotated[
        str | None,
        typer.Option(help=f"Model name (default: {get_settings().extract_model})"),
    ] = None,
) -> None:
    """Convert PDF to markdown sections alongside the PDF."""
    anyio.run(convert_async, pdf_path, model)
