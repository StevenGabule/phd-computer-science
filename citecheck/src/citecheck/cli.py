"""CiteCheck top-level CLI dispatcher.

Provides a single ``citecheck`` entry point (registered in pyproject.toml) that
routes to the per-task scripts in ``citecheck/scripts/``. Each subcommand here
is a thin wrapper around a corresponding script; for now most call the script
as a subprocess so the CLI works even before the scripts are imported as
modules.

Usage::

    citecheck --help
    citecheck download-cap --dest data/cap_raw --jurisdictions us
    citecheck build-bm25 --corpus-parquet data/cap_parquet
    citecheck train-reranker --train-jsonl data/reranker_train.jsonl
    citecheck run-baseline --baseline naive_rag --eval-jsonl data/eval_v0.1.jsonl
    citecheck run-citecheck --eval-jsonl data/eval_v0.1.jsonl
    citecheck evaluate --predictions runs/preds.jsonl --gold data/eval_v0.1.jsonl
"""
from __future__ import annotations

import logging
import subprocess
import sys

import click

from citecheck import __version__
from citecheck.config import PATHS, ensure_dirs

logger = logging.getLogger("citecheck.cli")
_SCRIPTS_DIR = PATHS.project_root / "scripts"


def _run_script(script_name: str, args: tuple[str, ...]) -> int:
    """Execute a script in citecheck/scripts/ as a subprocess.

    Returns the script's exit code. Logs but does not raise on non-zero exit.
    """
    script_path = _SCRIPTS_DIR / script_name
    if not script_path.exists():
        logger.error("Script not found: %s", script_path)
        click.echo(f"Error: {script_path} does not exist yet. Has it been written?", err=True)
        return 2
    cmd = [sys.executable, str(script_path), *args]
    logger.info("Running: %s", " ".join(cmd))
    return subprocess.run(cmd, check=False).returncode


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(__version__, prog_name="citecheck")
@click.option("--verbose", "-v", is_flag=True, help="Enable debug logging.")
def main(verbose: bool) -> None:
    """CiteCheck — verifiable US case-law citations via agentic RAG."""
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(asctime)s %(name)s %(levelname)s %(message)s",
    )
    ensure_dirs()


@main.command("download-cap", context_settings={"ignore_unknown_options": True})
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
def download_cap(args: tuple[str, ...]) -> None:
    """Download the Caselaw Access Project bulk dump (large; ~100GB)."""
    sys.exit(_run_script("download_cap.py", args))


@main.command("build-bm25", context_settings={"ignore_unknown_options": True})
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
def build_bm25(args: tuple[str, ...]) -> None:
    """Build the BM25 (pyserini/Lucene) index over the corpus."""
    sys.exit(_run_script("build_bm25_index.py", args))


@main.command("build-dense", context_settings={"ignore_unknown_options": True})
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
def build_dense(args: tuple[str, ...]) -> None:
    """Build the dense FAISS index over the corpus."""
    sys.exit(_run_script("build_dense_index.py", args))


@main.command("train-reranker", context_settings={"ignore_unknown_options": True})
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
def train_reranker(args: tuple[str, ...]) -> None:
    """Fine-tune the cross-encoder reranker with the multi-objective loss."""
    sys.exit(_run_script("train_reranker.py", args))


@main.command("run-baseline", context_settings={"ignore_unknown_options": True})
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
def run_baseline(args: tuple[str, ...]) -> None:
    """Run one of the published baselines on the eval set."""
    sys.exit(_run_script("run_baseline.py", args))


@main.command("run-citecheck", context_settings={"ignore_unknown_options": True})
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
def run_citecheck(args: tuple[str, ...]) -> None:
    """Run the full CiteCheck agentic pipeline on the eval set."""
    sys.exit(_run_script("run_citecheck.py", args))


@main.command("evaluate", context_settings={"ignore_unknown_options": True})
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
def evaluate(args: tuple[str, ...]) -> None:
    """Compute all 7 CiteCheck metrics on a predictions file."""
    sys.exit(_run_script("evaluate.py", args))


@main.command("info")
def info() -> None:
    """Print configured paths and environment-variable status."""
    click.echo(f"CiteCheck v{__version__}")
    click.echo(f"Project root:  {PATHS.project_root}")
    click.echo(f"Data dir:      {PATHS.data_dir}")
    click.echo(f"Models dir:    {PATHS.models_dir}")
    click.echo(f"Indexes dir:   {PATHS.indexes_dir}")
    click.echo(f"Scripts dir:   {_SCRIPTS_DIR}")
    click.echo(f"Scripts found: {sorted(p.name for p in _SCRIPTS_DIR.glob('*.py'))}")


if __name__ == "__main__":
    main()
