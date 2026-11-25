"""Read a PDF or blog post, from a path or URL, into Markdown."""

import re
import tempfile
import urllib.request
from dataclasses import dataclass
from pathlib import Path

import typer

FRONT_CHARS = 5000  # enough for a long author list and the first page's footnotes


@dataclass(frozen=True)
class Paper:
    name: str
    markdown: str
    front: str = ""  # the first page (title, authors, affiliations, first-page footnotes), or a post's byline and start


def read_source(source: str) -> Paper:
    """A PDF path, PDF URL, arXiv abs URL, blog post URL or Markdown file, as Markdown without the references."""
    if source.endswith(".md") and not _is_url(source):
        markdown = Path(source).read_text()
        front = markdown[:FRONT_CHARS]
    else:
        data = _fetch(source)
        markdown = _pdf_to_markdown(data) if _is_pdf(data) else _html_to_markdown(data)
        front = (
            _first_page(data)
            if _is_pdf(data)
            else _byline(data) + markdown[:FRONT_CHARS]
        )
    if not markdown.strip():
        raise typer.BadParameter(f"No text found in {source}")
    return Paper(_name_from(source), _cut_references(markdown), front[:FRONT_CHARS])


def _first_page(data: bytes) -> str:
    """The first page's text layer, footnotes included, which MinerU's Markdown may move or drop."""
    import pypdfium2

    return (
        pypdfium2.PdfDocument(data)[0]
        .get_textpage()
        .get_text_range()
        .replace("\r\n", "\n")
    )


def _byline(data: bytes) -> str:
    import trafilatura

    meta = trafilatura.extract_metadata(data.decode(errors="replace"))
    fields = {
        "Title": meta and meta.title,
        "Author": meta and meta.author,
        "Site": meta and meta.sitename,
    }
    return "".join(f"{k}: {v}\n" for k, v in fields.items() if v) + "\n"


def _fetch(source: str) -> bytes:
    if _is_url(source):
        return urllib.request.urlopen(_arxiv_pdf_url(source)).read()
    return Path(source).read_bytes()


def _is_url(source: str) -> bool:
    return source.startswith("http")


def _arxiv_pdf_url(url: str) -> str:
    return url.replace("arxiv.org/abs/", "arxiv.org/pdf/")


def _name_from(source: str) -> str:
    if not _is_url(source):
        return Path(source).stem
    last = source.split("?")[0].rstrip("/").split("/")[-1]
    return re.sub(r"\.(pdf|html?)$", "", last)


def _is_pdf(data: bytes) -> bool:
    return data[:4] == b"%PDF"


def _pdf_to_markdown(data: bytes) -> str:
    """MinerU's vision model on an in-process vLLM engine. Frees the GPU when done."""
    import torch
    from mineru import parse
    from mineru.config import VlmConfig
    from mineru.model.vlm.runtime import shutdown_cached_models

    with tempfile.NamedTemporaryFile(suffix=".pdf") as f:
        f.write(data)
        f.flush()
        markdown = parse(f.name, vlm_config=VlmConfig(engine="vllm")).markdown()
    shutdown_cached_models()
    torch.cuda.empty_cache()
    return _drop_figures(markdown)


def _drop_figures(markdown: str) -> str:
    return re.sub(r"!\[[^\]]*\]\(data:image[^)]*\)\n*", "", markdown)


def _html_to_markdown(data: bytes) -> str:
    import trafilatura

    html = data.decode(errors="replace")
    return trafilatura.extract(html, output_format="markdown", deduplicate=True) or ""


def _cut_references(markdown: str) -> str:
    return re.split(r"(?im)^#+ \W*references\b", markdown)[0]
