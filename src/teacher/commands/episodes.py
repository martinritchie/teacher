"""`teacher episodes`: make an episode for every citation in a BibTeX file that has none yet.

The file is the show's list: merging a citation into it requests an episode, named after its key.
"""

import re
import shutil
from pathlib import Path

import typer

from teacher.settings import MIN_FREE_GPU_GIB, SCRIPT_MODEL
from teacher.source import _name_from

GPU_BUSY = 75  # exit code: nothing wrong, try again later (EX_TEMPFAIL)


def episodes(
    bib: Path = typer.Option(
        Path("episodes/episodes.bib"), help="BibTeX file of the show's papers"
    ),
    out: Path = typer.Option(Path("episodes"), help="Where <key>.md and <key>.mp3 go"),
    work: Path = typer.Option(
        Path("out/run"), help="Where each run writes its logs, trace and clips"
    ),
    model: str = typer.Option(SCRIPT_MODEL, help="Script model, as for `teacher run`"),
    dry_run: bool = typer.Option(False, help="List what would be made, and stop"),
):
    """Run `teacher run` on the source of every entry without <out>/<key>.mp3 (its arXiv eprint, else its url,
    else its DOI), then copy the script and MP3 to <out>/<key>.md and .mp3."""
    from teacher.cli import app

    todo = [(k, s) for k, s in citations(bib.read_text()) if not (out / f"{k}.mp3").exists()]  # fmt: skip
    free = gpu_free_gib()
    if todo and not dry_run and free < MIN_FREE_GPU_GIB:
        typer.echo(f"{len(todo)} to make, but the GPU has {free:.1f} GiB free and a run needs {MIN_FREE_GPU_GIB}: "
                   "close games and log out of the desktop, then try again.")  # fmt: skip
        raise typer.Exit(GPU_BUSY)
    for key, source in todo:
        typer.echo(f"{key}: {source or 'no eprint, url or doi; skipped'}")
        if dry_run or not source:
            continue
        app(
            ["run", source, "--out", str(work), "--model", model], standalone_mode=False
        )
        for ext in ("md", "mp3"):
            shutil.copy(work / f"{_name_from(source)}.{ext}", out / f"{key}.{ext}")
    typer.echo(f"{len(todo)} to make" if dry_run else f"Made {len(todo)} episode(s)")


def gpu_free_gib() -> float:
    """Free memory on the GPU now; desktops and games hold some."""
    import subprocess

    query = ["nvidia-smi", "--query-gpu=memory.free", "--format=csv,noheader,nounits"]
    return (
        int(
            subprocess.run(
                query, capture_output=True, text=True, check=True
            ).stdout.split()[0]
        )
        / 1024
    )


def citations(text: str) -> list[tuple[str, str]]:
    """Each entry's key, and the source to read it from ("" if it names none)."""
    found = []
    for key, body in re.findall(r"@\w+\s*\{\s*([^,\s]+)\s*,(.*?)\n\s*\}", text, re.S):
        fields = {k.lower(): v.strip() for k, v in re.findall(r"(?m)^\s*(\w+)\s*=\s*[{\"](.*)[}\"]\s*,?\s*$", body)}  # fmt: skip
        eprint, url, doi = (fields.get(f, "") for f in ("eprint", "url", "doi"))
        found.append((key, eprint and f"https://arxiv.org/abs/{eprint}" or url or doi and f"https://doi.org/{doi}"))  # fmt: skip
    return found
