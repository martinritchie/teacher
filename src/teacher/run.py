"""`teacher run`: paper or blog post in, script and audio out."""

import re
import urllib.request
from pathlib import Path
from typing import Annotated

import ollama
import typer

PROMPTS = Path(__file__).parent / "prompts"
NOTES_TOKENS = 3000  # budget for the combined notes in every script call


def load(source: str) -> tuple[str, str]:
    """Return (name, markdown) with the references cut."""
    if source.startswith("http"):
        data = urllib.request.urlopen(
            source.replace("arxiv.org/abs/", "arxiv.org/pdf/")
        ).read()
        name = re.sub(
            r"\.(pdf|html?)$", "", source.split("?")[0].rstrip("/").split("/")[-1]
        )
    else:
        data, name = Path(source).read_bytes(), Path(source).stem
    if data[:4] == b"%PDF":
        import pymupdf
        import pymupdf4llm

        md = pymupdf4llm.to_markdown(pymupdf.open(stream=data, filetype="pdf"))
    else:
        import trafilatura

        md = (
            trafilatura.extract(
                data.decode(errors="replace"),
                output_format="markdown",
                deduplicate=True,
            )
            or ""
        )
    return name, re.split(r"(?im)^#+ \W*references\b", md)[0]


def split(md: str, limit: int) -> list[str]:
    """Pack markdown sections into chunks of at most `limit` tokens (len // 4)."""
    chunks = [""]
    for sec in re.split(r"(?m)^(?=#+ )", md):
        for i in range(0, len(sec), limit * 4) if len(sec) > limit * 4 else [0]:
            piece = sec[i : i + limit * 4]
            if chunks[-1] and len(chunks[-1] + piece) > limit * 4:
                chunks.append("")
            chunks[-1] += piece
    return [c for c in chunks if c.strip()]


def write_script(chunks: list[str], model: str, minutes: int) -> str:
    system = (
        (PROMPTS / "script.md").read_text()
        + "\n\n"
        + "\n\n".join(
            f.read_text() for f in sorted((PROMPTS / "examples").glob("*.md"))
        )
    )
    words = minutes * 150
    n, total = len(chunks), sum(map(len, chunks))
    targets = [round(words * len(c) / total) for c in chunks]
    share = NOTES_TOKENS * 4 // n
    # largest prompt: system + chunk + notes budget + previous + draft + problems + instructions
    prompt = (
        len(system) // 4
        + max(map(len, chunks)) // 4
        + NOTES_TOKENS
        + max(targets) * 2
        + 1500
    )
    num_ctx = (prompt + 1000) // 1024 * 1024 + 1024

    def chat(system, *user):
        msgs = [{"role": "system", "content": system}] + [
            {"role": "user", "content": u} for u in user
        ]
        r = ollama.chat(model=model, messages=msgs, options={"num_ctx": num_ctx})
        if r.prompt_eval_count + r.eval_count >= num_ctx:
            typer.echo(
                f"Prompt filled the {num_ctx} token window and was cut; lower --chunk.",
                err=True,
            )
            raise typer.Exit(1)
        return r.message.content

    typer.echo(f"Notes for {n} chunks...")
    notes = [
        chat((PROMPTS / "notes.md").read_text(), c, "Write the notes for this chunk.")
        for c in chunks
    ]
    cut = [x[:share] for x in notes]
    all_notes, parts = "\n".join(cut), []
    for k, (chunk, note, target) in enumerate(zip(chunks, notes, targets), 1):
        typer.echo(f"Part {k}/{n}...")
        prev = parts[-1].split("\n\n")[-1][-1500:] if parts else ""
        ask = f"<notes>\n{all_notes}\n</notes>\n<previous>\n{prev}\n</previous>\nWrite this part in about {target} words."
        part = chat(system, chunk, ask)
        verdict = chat(
            (PROMPTS / "check.md").read_text(),
            f"<notes>\n{note[: NOTES_TOKENS * 4]}\n</notes>\n<part>\n{part}\n</part>",
        )
        if verdict.strip() != "OK":
            part = chat(
                system,
                chunk,
                f"{ask}\n<draft>\n{part[: target * 8]}\n</draft>\n<problems>\n{verdict[:2000]}\n</problems>",
            )
        parts.append(part.strip())
    return "\n\n".join(parts)


def clean(text: str) -> str:
    return re.sub(r"[#*<>]", "", re.sub(r"<[^>]*>", "", text))


def speak(script: str, voice: str, out: Path) -> None:
    import numpy as np
    import soundfile
    from kokoro import KPipeline

    audio = [
        r.audio.numpy()
        for r in KPipeline(lang_code=voice[0])(script, voice=voice)
        if r.audio is not None
    ]
    soundfile.write(out, np.concatenate(audio), 24000)


def run(
    source: Annotated[
        str, typer.Argument(help="PDF path, PDF URL, arXiv abs URL, or blog post URL")
    ],
    model: str = typer.Option("gemma3:12b", help="Ollama model tag"),
    voice: str = typer.Option("af_heart", help="Kokoro voice"),
    minutes: int = typer.Option(25, help="Target length of the audio"),
    chunk: int = typer.Option(4000, help="Max source tokens per call"),
    out: Path = typer.Option(Path("out"), help="Output directory"),
):
    """Turn a paper or blog post into <name>.md (script) and <name>.mp3 in --out."""
    name, md = load(source)
    script = clean(write_script(split(md, chunk), model, minutes))
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{name}.md").write_text(script)
    speak(script, voice, out / f"{name}.mp3")
    typer.echo(f"Wrote {out / name}.md and .mp3")
