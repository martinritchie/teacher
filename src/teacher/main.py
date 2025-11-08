"""Main orchestrator for the Teacher multi-agent research paper system.

This system converts research papers into high-quality, audio-optimized transcripts
using a multi-agent collaborative approach:

1. Phase 1: Individual Analysis - Each agent analyzes the paper from their perspective
2. Phase 2: Collaborative Refinement - Agents discuss and refine their understanding
3. Phase 3: Audio Transcript Generation - Create speech-optimized output
"""

import os
from pathlib import Path
from typing import Optional

import anyio
from claude_agent_sdk import query
from claude_agent_sdk.types import AssistantMessage, TextBlock

from teacher.agents import create_default_personas, TranscriptGenerator, Phase0Agent


class TeacherSystem:
    """Main system for orchestrating multi-agent paper analysis."""

    def __init__(self, work_dir: str = "/tmp/teacher_work"):
        """Initialize the Teacher system.

        Args:
            work_dir: Working directory for tarball extraction and processing
        """
        self.personas = create_default_personas()
        self.transcript_generator = TranscriptGenerator()
        self.phase0_agent = Phase0Agent(work_dir=work_dir)
        self.paper_text: Optional[str] = None
        self.markdown_output_path: Optional[Path] = None

    @staticmethod
    def _extract_text_from_response(message) -> str:
        """Extract text content from SDK message.

        Args:
            message: Message from query() response

        Returns:
            Extracted text content
        """
        text_content = ""
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    text_content += block.text
        return text_content

    async def load_paper(self, tarball_path: str) -> str:
        """Load and extract a research paper from an arXiv tarball.

        Args:
            tarball_path: Path to the .tar.gz file

        Returns:
            Paper text content
        """
        tarball_file = Path(tarball_path)
        if not tarball_file.exists():
            raise FileNotFoundError(f"Tarball not found: {tarball_path}")

        print(f"📦 Processing tarball: {tarball_path}")
        self.paper_text, self.markdown_output_path = await self.phase0_agent.process_tarball(tarball_path)

        print(f"✓ Successfully extracted and processed paper")
        print(f"  Document size: {len(self.paper_text)} characters")
        print(f"  Markdown files saved to: {self.markdown_output_path}")
        return self.paper_text

    async def phase_1_individual_analysis(self) -> dict:
        """Phase 1: Each agent independently analyzes the paper.

        Returns:
            Dictionary mapping agent names to their analyses
        """
        if not self.paper_text:
            raise ValueError("No paper loaded. Call load_paper() first.")

        print("\n📖 Phase 1: Individual Analysis")
        print("=" * 50)
        analyses = {}

        for persona in self.personas:
            print(f"\nAnalyzing with {persona.name}...")

            prompt = f"""You are {persona.name}, a {persona.role}.

{persona.perspective}

Please analyze the following research paper and provide your key insights:

{self.paper_text}

Focus on:
1. Key concepts from your perspective
2. Important findings and implications
3. Potential applications or limitations
4. Connections to related work in your field"""

            analysis_text = ""
            async for message in query(prompt=prompt):
                analysis_text += self._extract_text_from_response(message)

            analyses[persona.name] = analysis_text
            print(f"✓ Analysis complete from {persona.name}")

        return analyses

    async def phase_2_collaborative_refinement(self, analyses: dict) -> str:
        """Phase 2: Agents collaborate to refine and synthesize understanding.

        Args:
            analyses: Individual analyses from Phase 1

        Returns:
            Refined understanding from collaboration
        """
        print("\n💬 Phase 2: Collaborative Refinement")
        print("=" * 50)

        combined_analyses = "\n\n".join(
            f"{name}'s Perspective:\n{analysis}"
            for name, analysis in analyses.items()
        )

        prompt = f"""You are facilitating a discussion between research experts with different perspectives.

Here are their individual analyses:

{combined_analyses}

Please synthesize these perspectives to:
1. Identify agreements and areas of consensus
2. Resolve any apparent conflicts or misunderstandings
3. Build a comprehensive, accurate understanding
4. Highlight the most important takeaways

Produce a refined, unified understanding that captures all perspectives."""

        refined_understanding = ""
        async for message in query(prompt=prompt):
            refined_understanding += self._extract_text_from_response(message)

        print("✓ Collaborative refinement complete")
        return refined_understanding

    async def phase_3_generate_transcript(self, refined_understanding: str) -> str:
        """Phase 3: Generate audio-optimized transcript.

        Args:
            refined_understanding: Output from Phase 2

        Returns:
            Audio-optimized transcript
        """
        print("\n🎙️ Phase 3: Audio Transcript Generation")
        print("=" * 50)

        prompt = f"""You are creating a transcript optimized for text-to-speech conversion.

Based on this research paper analysis:

{refined_understanding}

Generate a transcript that:
1. Uses clear, natural language suitable for audio narration
2. Maintains logical flow and pacing for listening
3. Explains technical jargon clearly without omitting it
4. Maximizes educational value for audio format
5. Includes natural section breaks for narration
6. Avoids complex formatting or symbols

The transcript should sound like a knowledgeable expert explaining the research to an intelligent audience."""

        transcript = ""
        async for message in query(prompt=prompt):
            transcript += self._extract_text_from_response(message)

        print("✓ Audio transcript generated")
        return transcript

    async def process_paper(self, tarball_path: str) -> str:
        """Run the complete multi-phase paper processing pipeline.

        Args:
            tarball_path: Path to the .tar.gz arXiv paper archive

        Returns:
            Final audio-optimized transcript
        """
        print("\n🚀 Starting Teacher Paper Processing Pipeline")
        print("=" * 50)

        await self.load_paper(tarball_path)

        # Phases 1-3: Audio transcription pipeline
        analyses = await self.phase_1_individual_analysis()
        refined_understanding = await self.phase_2_collaborative_refinement(analyses)
        final_transcript = await self.phase_3_generate_transcript(refined_understanding)

        print("\n" + "=" * 50)
        print("✅ Pipeline Complete!")
        print("=" * 50)
        print(f"\n📁 Markdown files saved to: {self.markdown_output_path}")

        return final_transcript


async def main():
    """Main entry point for the Teacher system."""

    if not os.getenv("ANTHROPIC_API_KEY"):
        print("⚠️  Warning: ANTHROPIC_API_KEY not set")
        print("   Set your API key to enable Claude analysis:")
        print("   export ANTHROPIC_API_KEY='your-key-here'")
        print("   Get your key from: https://console.anthropic.com/")

    system = TeacherSystem()
    sample_tarball = "papers/sample_paper.tar.gz"

    if Path(sample_tarball).exists():
        transcript = await system.process_paper(sample_tarball)
        print("\n📝 Final Transcript:")
        print("-" * 50)
        print(transcript)
    else:
        print(f"Sample tarball not found at {sample_tarball}")
        print("\nTo test the system:")
        print(f"1. Place an arXiv tarball at {sample_tarball}")
        print("2. Set your ANTHROPIC_API_KEY")
        print("3. Run: python -m teacher.main")
        print("\nSystem is ready to process papers!")


if __name__ == "__main__":
    anyio.run(main)
