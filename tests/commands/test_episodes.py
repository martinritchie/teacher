"""`teacher episodes` (commands/episodes.py): a BibTeX file in, an episode for each new citation out."""

from teacher.commands.episodes import citations
from teacher.testing import PDF, cli

BIB = """@misc{shao2025calm,
      title={Continuous Autoregressive Language Models},
      eprint={2510.27688},
      url={https://example.com/elsewhere},
}

@article{blog2026,
  title = {Weight space programming},
  url = {https://example.com/post/},
}

@book{nothing2020,
  title = {No source},
}
"""


def test_each_citation_is_read_from_its_eprint_else_its_url():
    assert citations(BIB) == [
        ("shao2025calm", "https://arxiv.org/abs/2510.27688"),
        ("blog2026", "https://example.com/post/"),
        ("nothing2020", ""),
    ]


def test_a_new_citation_becomes_an_episode_named_after_its_key(llm, tts, tmp_path):
    """Only entries with no MP3 yet are made; the script and MP3 are copied in under the citation's key."""
    (tmp_path / "show.bib").write_text(f"@misc{{old,\n  url={{{PDF}}},\n}}\n\n@misc{{new,\n  url={{{PDF}}},\n}}\n")  # fmt: skip
    (tmp_path / "old.mp3").write_bytes(b"made before")
    cli("episodes", "--bib", tmp_path / "show.bib", "--out", tmp_path, "--work", tmp_path / "work")  # fmt: skip
    assert len(tts) == 1 and (tmp_path / "new.mp3").read_bytes()[:3] == b"ID3"
    assert (tmp_path / "new.md").read_text().startswith("## Introduction")
