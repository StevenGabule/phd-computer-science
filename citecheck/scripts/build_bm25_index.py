"""Build a Pyserini/Lucene BM25 index over the CAP corpus.

Usage::

    python scripts/build_bm25_index.py \\
        --corpus-parquet data/cap_parquet \\
        --output-dir indexes/bm25 \\
        --threads 8
"""
from __future__ import annotations

import logging
import tempfile
from pathlib import Path

import click

from citecheck.config import PATHS, ensure_dirs
from citecheck.retrieval.bm25 import BM25Retriever, corpus_to_pyserini_jsonl

logger = logging.getLogger(__name__)


@click.command()
@click.option(
    "--corpus-parquet",
    type=click.Path(exists=True, path_type=Path),
    default=lambda: PATHS.cap_parquet,
    show_default=True,
    help="Path to the CAP parquet directory produced by data.cap_loader.",
)
@click.option(
    "--output-dir",
    type=click.Path(path_type=Path),
    default=lambda: PATHS.bm25_index,
    show_default=True,
    help="Where the Lucene index will live.",
)
@click.option(
    "--threads",
    type=int,
    default=4,
    show_default=True,
    help="Pyserini indexer threads (scales near-linearly up to ~16).",
)
@click.option(
    "--jsonl-out",
    type=click.Path(path_type=Path),
    default=None,
    help="Optional path to keep the intermediate Pyserini JSONL. "
    "If omitted, a temp dir is used and cleaned up automatically.",
)
@click.option("-v", "--verbose", is_flag=True, help="Enable DEBUG logging.")
def main(
    corpus_parquet: Path,
    output_dir: Path,
    threads: int,
    jsonl_out: Path | None,
    verbose: bool,
) -> None:
    """Convert CAP parquet -> Pyserini JSONL -> Lucene index."""
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    ensure_dirs()
    output_dir.mkdir(parents=True, exist_ok=True)

    from citecheck.data import iter_cap_opinions  # imported lazily

    retriever = BM25Retriever(index_dir=output_dir)

    if jsonl_out is not None:
        jsonl_out.parent.mkdir(parents=True, exist_ok=True)
        target_jsonl = jsonl_out
        cleanup_dir = None
    else:
        cleanup_dir = tempfile.mkdtemp(prefix="citecheck_bm25_")
        target_jsonl = Path(cleanup_dir) / "corpus.jsonl"

    try:
        logger.info("Streaming CAP opinions -> %s", target_jsonl)
        n = corpus_to_pyserini_jsonl(iter_cap_opinions(corpus_parquet), target_jsonl)
        logger.info("Wrote %d records; invoking Pyserini indexer", n)
        retriever.build_index(target_jsonl, threads=threads)
        logger.info("BM25 index ready at %s", output_dir)
    finally:
        if cleanup_dir is not None and Path(cleanup_dir).exists():
            import shutil

            shutil.rmtree(cleanup_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
