"""Build a FAISS dense index over the CAP corpus.

Usage::

    python scripts/build_dense_index.py \\
        --corpus-parquet data/cap_parquet \\
        --output-dir indexes/dense \\
        --model BAAI/bge-base-en-v1.5 \\
        --batch-size 64 \\
        --device auto
"""
from __future__ import annotations

import logging
from pathlib import Path

import click

from citecheck.config import MODELS, PATHS, ensure_dirs
from citecheck.retrieval.dense import DenseRetriever

logger = logging.getLogger(__name__)


@click.command()
@click.option(
    "--corpus-parquet",
    type=click.Path(exists=True, path_type=Path),
    default=lambda: PATHS.cap_parquet,
    show_default=True,
    help="CAP parquet directory.",
)
@click.option(
    "--output-dir",
    type=click.Path(path_type=Path),
    default=lambda: PATHS.dense_index,
    show_default=True,
    help="Where the FAISS index + sidecar metadata will be written.",
)
@click.option(
    "--model",
    type=str,
    default=lambda: MODELS.dense_encoder,
    show_default=True,
    help="HuggingFace sentence-transformers model id.",
)
@click.option("--batch-size", type=int, default=32, show_default=True)
@click.option(
    "--device",
    type=click.Choice(["auto", "cpu", "cuda", "mps"]),
    default="auto",
    show_default=True,
)
@click.option(
    "--index-type",
    type=click.Choice(["auto", "flat", "ivf"]),
    default="auto",
    show_default=True,
    help="Force FAISS index type. 'auto' picks IVFFlat above 100k passages.",
)
@click.option(
    "--no-normalize",
    is_flag=True,
    help="Disable L2 normalization (use raw inner product).",
)
@click.option("-v", "--verbose", is_flag=True)
def main(
    corpus_parquet: Path,
    output_dir: Path,
    model: str,
    batch_size: int,
    device: str,
    index_type: str,
    no_normalize: bool,
    verbose: bool,
) -> None:
    """Embed the CAP corpus with a bi-encoder and persist a FAISS index."""
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    ensure_dirs()
    output_dir.mkdir(parents=True, exist_ok=True)

    from citecheck.data import iter_cap_opinions  # imported lazily

    retriever = DenseRetriever(model_name=model, index_dir=output_dir, device=device)
    force = None if index_type == "auto" else index_type
    retriever.build_index(
        iter_cap_opinions(corpus_parquet),
        batch_size=batch_size,
        normalize=not no_normalize,
        force_index_type=force,
    )
    logger.info("Dense index written to %s", output_dir)


if __name__ == "__main__":
    main()
