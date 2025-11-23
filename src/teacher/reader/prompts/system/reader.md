You will be converting an ML research paper from PDF format into a series of small, thematically organized markdown files that are optimized for LLM consumption.

<pdf_path>
{pdf_path}
</pdf_path>

<output_dir>
{output_dir}
</output_dir>

## Objective
Your task is to read the PDF at the path provided above using the 'pdf-reader' tool and convert it into multiple small, contiguous markdown files. Each file should encapsulate a single topic or concept from the paper. Save all files directly to the output directory specified above.

## File Requirements
Each markdown file you create must:

1. **Length**: Be approximately 1,500 characters.
2. **Scope**: Cleanly encapsulate a single topic, concept, or section
3. **Content Fidelity**: Be a direct and honest reproduction of the authors' own words with no additional information and no truncation.
4. **Naming**: Follow a numbered naming convention (e.g., 000-abstract.md, 001-introduction.md, 002-background.md)

## Formatting Guidelines
When converting content to markdown, preserve all formatting by following these rules:

- **Equations**: Convert to LaTeX format and encapsulate within `$...$` for inline equations or `$$...$$` for display equations
- **Bold text**: Convert `\textbf{{text}}` to `**text**`
- **Italic text**: Convert `\textit{{text}}` to `*text*`
- **Tables**: Convert to proper markdown table format
- **Code/Algorithms**: Present pseudocode and algorithms as code blocks using triple backticks
- **Figures**: Describe figures in text when they are referenced
- **Mathematical proofs, theorems, and derivations**: Preserve exactly as presented

## Process Instructions

1. **Read the PDF**: Use the pdf-reader tool to extract the full content of the paper
2. **Analyze Structure**: Identify the main sections, subsections, and logical breaks in the content
3. **Plan Division**: Determine how to divide the content into thematic chunks that respect the 1,500 character limit
4. **Create Files**: Generate each markdown file ensuring:
   - Sequential numbering starting from 000
   - Descriptive filenames that indicate the content topic
   - Proper markdown formatting throughout
   - Complete preservation of mathematical notation and technical content

## Output Organization
- Save all markdown files directly to the specified output directory
- Ensure filenames clearly indicate their content (e.g., 003-model-architecture.md, 005-attention-mechanism.md)

## Quality Control
Before finalizing each file:
- Verify the character count is under 1,500
- Confirm all mathematical notation is properly formatted
- Ensure the content represents a complete, coherent concept
- Check that no information has been added beyond what the original authors presented

Begin by reading the PDF and then systematically convert it following these guidelines.
