"""Utilities for loading narrate prompts and few-shot examples."""

from pathlib import Path
from typing import Any

from pydantic import BaseModel, model_serializer, model_validator

PROMPTS_DIR = Path(__file__).parent / "prompts"
SYSTEM_PATH = Path(PROMPTS_DIR, "system")


class FewShotExample(BaseModel):
    """Structure for a few-shot example."""

    original: str
    teacher: str
    title: str

    @model_validator(mode="before")
    @classmethod
    def parse_markdown(cls, data: Any) -> dict[str, str]:
        """Parse markdown format into structured fields."""
        if isinstance(data, str):
            parts = data.split("## Original Text")
            orig_teacher = parts[1].split("## Teacher")
            return {
                "title": parts[0].strip().lstrip("# ").strip(),
                "original": orig_teacher[0].strip(),
                "teacher": orig_teacher[1].strip(),
            }
        return data

    @model_serializer
    def serialize_model(self) -> list[dict[str, str]]:
        """Serialize to conversation message format for LLM consumption."""
        return [
            {"role": "user", "content": self.original},
            {"role": "assistant", "content": self.teacher},
        ]


def narrative_prompt() -> str:
    """Load the narrate system prompt.

    Returns:
        Narrate system prompt for converting academic text to audio narratives
    """
    return Path(SYSTEM_PATH, "narrative.md").read_text()


def normalizer_prompt() -> str:
    """Load the ElevenLabs technical narrator prompt.

    Returns:
        Narrator configuration prompt for TTS
    """
    return Path(SYSTEM_PATH, "elevenlabs.md").read_text()


def get_few_shot_examples() -> list[FewShotExample]:
    """Load few-shot examples.

    Returns:
        List of few-shot examples with original text and teacher narrative
    """
    examples_dir = Path(PROMPTS_DIR, "few-shot-examples")
    return [
        FewShotExample.model_validate(md_file.read_text())
        for md_file in sorted(examples_dir.glob("**/*.md"))
    ]


def get_few_shot_messages(user_text: str) -> list[dict[str, str]]:
    """Get few-shot examples formatted as conversation messages for API calls.

    Args:
        user_text: Final user text to append

    Returns:
        List of message dicts with role and content
    """
    examples = get_few_shot_examples()
    return [item for example in examples for item in example.model_dump()] + [
        {"role": "user", "content": user_text}
    ]
