"""Read a PDF or blog post, from a path or URL, into Markdown."""

import re
import tempfile
import urllib.request
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Paper:
    name: str
    markdown: str


def read_source(source: str) -> Paper:
    """A PDF path, PDF URL, arXiv abs URL, blog post URL or Markdown file, as Markdown without the references."""
    if source.endswith(".md") and not _is_url(source):
        return Paper(Path(source).stem, _cut_references(Path(source).read_text()))
    data = _fetch(source)
    markdown = _pdf_to_markdown(data) if _is_pdf(data) else _html_to_markdown(data)
    return Paper(_name_from(source), _cut_references(markdown))


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
