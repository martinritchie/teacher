"""Reading a source (source.py): PDF path or URL, arXiv abs URL, blog post, Markdown file; references cut."""

import re
from types import SimpleNamespace

import pytest
from typer.testing import CliRunner

import teacher.source as source

from teacher.cli import app
from teacher.testing import (
    BLOG,
    PARAGRAPH,
    PDF,
    PDF_MARKDOWN,
    chunk,
    run,
    serve,
)


def test_arxiv_abs_url_is_read_as_pdf(llm, tts, tmp_path, monkeypatch):
    """An arXiv abstract URL downloads the PDF. The arXiv id names the output."""
    seen = []

    def urlopen(req, *a, **k):
        seen.append(getattr(req, "full_url", req))
        return SimpleNamespace(read=PDF.read_bytes)

    monkeypatch.setattr("urllib.request.urlopen", urlopen)
    run("https://arxiv.org/abs/2510.27688v1", "--out", tmp_path)
    assert seen == ["https://arxiv.org/pdf/2510.27688v1"]
    assert (tmp_path / "2510.27688v1.mp3").exists()


def test_blog_post_url_is_read_as_article(llm, tts, tmp_path, monkeypatch):
    """An HTML URL gives the model the article text only. The last URL segment names the output."""
    serve(monkeypatch, BLOG.format(body=PARAGRAPH * 8).encode())
    run(
        "https://transformer-circuits.pub/2025/attribution-graphs/biology.html",
        "--out",
        tmp_path,
    )
    source = chunk(llm.of("notes")[0])
    assert "attribution graph" in source
    assert "newsletter" not in source and "Cookie" not in source
    assert (tmp_path / "biology.mp3").exists()


def test_whole_source_is_covered_without_references(episode_run):
    """The chunks cover the source from the abstract to the conclusion. The reference list and all after it are cut."""
    llm = episode_run.llm
    source = "".join(chunk(c) for c in llm.of("notes"))
    assert "ABSTRACT" in source and "CONCLUSION" in source
    assert not re.search(r"\n#+ \W*References", source, re.I)
    assert "PROOF OF THEOREM" not in source


def test_a_source_with_no_text_stops_before_any_model_starts(llm, tmp_path):
    """An empty source (a blank file, or a page with no article text) is an error up front."""
    (tmp_path / "empty.md").write_text("\n\n")
    result = CliRunner().invoke(
        app, ["outline", str(tmp_path / "empty.md"), "--out", str(tmp_path)]
    )
    assert (
        result.exit_code != 0 and "No text found" in result.output and llm.started == 0
    )


@pytest.mark.functional
def test_mineru_converts_the_pdf_as_the_unit_tests_assume():
    """Real MinerU on the GPU. The unit tests read tests/data/calm.md in its place; this keeps that file honest.
    If MinerU's output changes, save the new output there."""
    headings = lambda md: re.findall(r"(?m)^#+ .*", md)  # noqa: E731
    assert headings(source._pdf_to_markdown(PDF.read_bytes())) == headings(
        PDF_MARKDOWN.read_text()
    )
