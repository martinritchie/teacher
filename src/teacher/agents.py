"""Multi-agent system for research paper analysis."""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
from claude_agent_sdk.types import AssistantMessage, TextBlock


class Phase0Agent:
    """Autonomous agent for LaTeX paper extraction and markdown transcription.

    Uses ClaudeSDKClient with file and bash tools to:
    - Extract and explore tarball structure
    - Find and read the main LaTeX paper
    - Handle included files (\input, \include)
    - Reconstruct complete paper
    - Transcribe to markdown with proper formatting preservation
    """

    def __init__(self, work_dir: str = "/tmp/teacher_work"):
        """Initialize Phase 0 agent.

        Args:
            work_dir: Working directory for extraction and processing
        """
        self.work_dir = Path(work_dir)
        self.work_dir.mkdir(parents=True, exist_ok=True)

    async def process_tarball(self, tarball_path: str) -> tuple[str, Path]:
        """Process a tarball, extract, explore, and generate markdown.

        Args:
            tarball_path: Path to the .tar.gz file

        Returns:
            Tuple of (reconstructed_paper_text, markdown_output_path)
        """
        system_prompt = f"""You are an expert at extracting and processing academic papers from compressed archives.

Your task is to:
1. Extract the tarball at: {tarball_path}
2. Explore the extracted directory structure
3. Identify the main LaTeX paper file (typically main.tex, paper.tex, or the largest .tex file)
4. Read and reconstruct the complete paper, resolving any \\input{{}} or \\include{{}} statements
5. Create a "markdown" folder within the extracted directory (sibling to the original files)
6. Transcribe the paper to well-structured markdown, preserving:
   - All mathematical equations (keep LaTeX notation in $ $ or $$ $$ or \\begin{{equation}}...\\end{{equation}})
   - Pseudocode and algorithm blocks (as code blocks)
   - Tables (as markdown tables or formatted blocks)
   - Figures/diagrams (with descriptions)
   - All citations and technical content
   - Lists, emphasis, and formatting
7. For each section, save it as a separate markdown file in the markdown/ folder

Filename format: Use section names converted to lowercase with underscores (e.g., "Introduction" → "introduction.md", "Related Work" → "related_work.md")

After saving all markdown files, provide the FULL RECONSTRUCTED PAPER TEXT in a code block marked:
```
RECONSTRUCTED_PAPER_START
<complete paper text here>
RECONSTRUCTED_PAPER_END
```

Important: Save each markdown section as its own file in the markdown/ subfolder. Do not output sections in text format - use the Write tool to save them directly."""

        options = ClaudeAgentOptions(
            allowed_tools=["Bash", "Read", "Write", "Glob"],
            permission_mode="acceptEdits"
        )

        markdown_output = ""
        paper_text = ""

        async with ClaudeSDKClient(options=options) as client:
            await client.query(system_prompt)

            async for message in client.receive_response():
                # Collect all output
                if isinstance(message, AssistantMessage):
                    for block in message.content:
                        if isinstance(block, TextBlock):
                            content = block.text

                            # Extract reconstructed paper if present
                            if "RECONSTRUCTED_PAPER_START" in content:
                                start = content.find("RECONSTRUCTED_PAPER_START") + len("RECONSTRUCTED_PAPER_START")
                                end = content.find("RECONSTRUCTED_PAPER_END")
                                if start != -1 and end != -1:
                                    paper_text = content[start:end].strip()

        # Find the markdown folder created by the agent within the extracted directory
        output_path = await self._find_markdown_folder()

        return paper_text, output_path

    async def _find_markdown_folder(self) -> Path:
        """Find and return the markdown folder created by the agent in the extracted directory.

        Returns:
            Path to the markdown folder
        """
        # The tarball will be extracted to work_dir by the agent
        # Search for the first markdown folder found
        for path in self.work_dir.rglob("markdown"):
            if path.is_dir():
                return path

        # Fallback: return path to work_dir/markdown if not found
        fallback = self.work_dir / "markdown"
        return fallback


@dataclass
class AgentPersona:
    """Defines an agent's role and perspective for paper analysis."""

    name: str
    role: str
    expertise: str
    perspective: str

    def get_system_prompt(self) -> str:
        """Generate system prompt for this agent persona.

        Returns:
            Formatted system prompt for the agent
        """
        return f"""You are {self.name}, a {self.role} with expertise in {self.expertise}.

Your perspective: {self.perspective}

Your task is to analyze research papers from your unique viewpoint, capturing:
- Key concepts relevant to your field
- Practical implications and applications
- Connections to related work
- Potential limitations or gaps in the research

Be thorough but concise, focusing on clarity and accuracy."""


class ResearchAnalysisAgent:
    """Agent for analyzing research papers from a specific perspective."""

    def __init__(self, persona: AgentPersona):
        """Initialize analysis agent with a persona.

        Args:
            persona: AgentPersona defining the agent's role
        """
        self.persona = persona
        self.notes: Optional[str] = None

    async def analyze_paper(self, paper_text: str) -> str:
        """Analyze paper from agent's perspective.

        Args:
            paper_text: Full text of the research paper

        Returns:
            Agent's analysis and notes
        """
        self.notes = f"{self.persona.name}'s Analysis:\n\n[Analysis to be generated by Claude API]"
        return self.notes


class TranscriptGenerator:
    """Generates audio-optimized transcripts from research paper analysis."""

    def __init__(self):
        """Initialize transcript generator."""
        self.transcript: Optional[str] = None
        self.technical_glossary: dict = {}

    async def generate_transcript(self, analyses: dict, paper_text: str) -> str:
        """Generate audio-optimized transcript from agent analyses.

        Args:
            analyses: Dictionary of {agent_name: analysis_text}
            paper_text: Original paper text for reference

        Returns:
            Audio-optimized transcript
        """
        self.transcript = "Generated audio transcript would appear here..."
        return self.transcript

    def add_glossary_term(self, term: str, definition: str) -> None:
        """Add technical term to glossary for audio narration.

        Args:
            term: Technical term
            definition: Clear explanation suitable for audio
        """
        self.technical_glossary[term] = definition


class MarkdownTranscriber:
    """Orchestrates Claude to manually transcribe LaTeX papers to markdown."""

    def __init__(self, output_dir: str = "paper_output"):
        """Initialize markdown transcriber.

        Args:
            output_dir: Directory to save markdown files
        """
        self.output_dir = Path(output_dir)

    async def save_markdown_sections(self, sections: dict[str, str]) -> Path:
        """Save transcribed markdown sections to individual files.

        Args:
            sections: Dictionary mapping section names to markdown content

        Returns:
            Path to output directory
        """
        self.output_dir.mkdir(parents=True, exist_ok=True)

        for section_name, content in sections.items():
            # Convert section name to filename
            filename = section_name.lower().replace(" ", "_").replace(":", "")
            filename = "".join(c if c.isalnum() or c == "_" else "" for c in filename)
            if not filename:
                filename = "content"

            filepath = self.output_dir / f"{filename}.md"
            filepath.write_text(content)

        return self.output_dir


def create_default_personas() -> list[AgentPersona]:
    """Create a set of default agent personas for research analysis.

    Returns:
        List of AgentPersona objects with different perspectives
    """
    return [
        AgentPersona(
            name="Dr. Researcher",
            role="Research Scientist",
            expertise="academic research methodology",
            perspective="Focus on scientific rigor, methodology, and reproducibility"
        ),
        AgentPersona(
            name="Prof. Practitioner",
            role="Industry Practitioner",
            expertise="real-world applications and implementation",
            perspective="Emphasize practical applications, scalability, and business impact"
        ),
        AgentPersona(
            name="Dr. Communicator",
            role="Science Communicator",
            expertise="making complex topics accessible",
            perspective="Translate technical concepts into clear explanations for general audiences"
        ),
    ]
