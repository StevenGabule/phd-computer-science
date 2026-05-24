"""Reciprocal Rank Fusion + the ``HybridRetriever`` that composes BM25 + dense.

RRF (Cormack, Clarke & Buettcher, 2009) is the simplest fusion rule that is
both score-agnostic (no need to normalize BM25 scores against cosine
similarities) and remarkably hard to beat in practice.

.. math::

    \\text{score}(d) = \\sum_{r \\in R} \\frac{1}{k + \\text{rank}_r(d)}

where ``k`` is a smoothing constant (we use ``RETRIEVAL.rrf_k_constant = 60``,
the value from the original paper) and ``R`` is the set of input rankings.
"""
from __future__ import annotations

import logging
from collections import defaultdict
from pathlib import Path
from typing import Any

from citecheck.config import RETRIEVAL
from citecheck.retrieval.bm25 import BM25Retriever, RetrievalResult
from citecheck.retrieval.dense import DenseRetriever

logger = logging.getLogger(__name__)


def rrf_fusion(
    rankings: list[list[RetrievalResult]],
    k: int = RETRIEVAL.rrf_k_constant,
    top_k: int | None = None,
) -> list[RetrievalResult]:
    """Reciprocal Rank Fusion of N ranked lists of :class:`RetrievalResult`.

    Args:
        rankings: A list of rankings. Each ranking is a list of
            :class:`RetrievalResult` ordered best-first; ranks are taken from
            the ``rank`` attribute when present, otherwise from list index.
        k: Smoothing constant (60 is the original RRF default; CiteCheck
            inherits it via :data:`RETRIEVAL.rrf_k_constant`).
        top_k: Optional truncation. ``None`` returns all fused documents.

    Returns:
        A single ranked list sorted by descending RRF score. The returned
        :class:`RetrievalResult` objects carry the *fused* score in ``score``
        and a fresh 1-based ``rank``; ``passage`` and ``metadata`` are taken
        from the first occurrence of that ``doc_id`` across input rankings.
    """
    if k <= 0:
        raise ValueError(f"RRF constant k must be positive, got {k}")
    if not rankings:
        return []

    fused_scores: dict[str, float] = defaultdict(float)
    first_seen: dict[str, RetrievalResult] = {}

    for ranking in rankings:
        for idx, result in enumerate(ranking):
            rank = result.rank if result.rank and result.rank > 0 else idx + 1
            fused_scores[result.doc_id] += 1.0 / (k + rank)
            if result.doc_id not in first_seen:
                first_seen[result.doc_id] = result
            elif result.passage and not first_seen[result.doc_id].passage:
                # Prefer the variant that carries a passage payload.
                first_seen[result.doc_id] = result

    ordered = sorted(fused_scores.items(), key=lambda kv: kv[1], reverse=True)
    if top_k is not None:
        ordered = ordered[:top_k]

    out: list[RetrievalResult] = []
    for new_rank, (doc_id, score) in enumerate(ordered, start=1):
        proto = first_seen[doc_id]
        out.append(
            RetrievalResult(
                doc_id=doc_id,
                score=float(score),
                rank=new_rank,
                passage=proto.passage,
                metadata=dict(proto.metadata),
            )
        )
    return out


class HybridRetriever:
    """Composes BM25 + dense retrieval and fuses with RRF.

    The two underlying retrievers are constructed lazily so callers can
    instantiate ``HybridRetriever`` even when only one backend is available.

    Example::

        hybrid = HybridRetriever()
        results = hybrid.search("statute of frauds writing requirement", top_k=20)
    """

    def __init__(
        self,
        bm25: BM25Retriever | None = None,
        dense: DenseRetriever | None = None,
        bm25_index_dir: Path | None = None,
        dense_index_dir: Path | None = None,
        dense_model_name: str | None = None,
        device: str = "auto",
        rrf_k: int = RETRIEVAL.rrf_k_constant,
    ) -> None:
        self.bm25: BM25Retriever = bm25 or BM25Retriever(index_dir=bm25_index_dir)
        self.dense: DenseRetriever = dense or DenseRetriever(
            model_name=dense_model_name, index_dir=dense_index_dir, device=device
        )
        self.rrf_k: int = rrf_k

    def search(
        self,
        query: str,
        top_k: int = RETRIEVAL.rrf_top_k,
        bm25_top_k: int = RETRIEVAL.bm25_top_k,
        dense_top_k: int = RETRIEVAL.dense_top_k,
    ) -> list[RetrievalResult]:
        """Run BM25 + dense in sequence and RRF-fuse the rankings."""
        bm25_hits = self.bm25.search(query, top_k=bm25_top_k)
        dense_hits = self.dense.search(query, top_k=dense_top_k)
        return rrf_fusion([bm25_hits, dense_hits], k=self.rrf_k, top_k=top_k)

    def batch_search(
        self,
        queries: list[str],
        top_k: int = RETRIEVAL.rrf_top_k,
        bm25_top_k: int = RETRIEVAL.bm25_top_k,
        dense_top_k: int = RETRIEVAL.dense_top_k,
        bm25_threads: int = 4,
    ) -> list[list[RetrievalResult]]:
        """Batch variant of :meth:`search` — fuses per-query."""
        bm25_batches = self.bm25.batch_search(queries, top_k=bm25_top_k, threads=bm25_threads)
        dense_batches = self.dense.batch_search(queries, top_k=dense_top_k)
        out: list[list[RetrievalResult]] = []
        for bm25_hits, dense_hits in zip(bm25_batches, dense_batches, strict=True):
            out.append(rrf_fusion([bm25_hits, dense_hits], k=self.rrf_k, top_k=top_k))
        return out

    # --------------------------------------------------------------- helpers

    def __repr__(self) -> str:  # pragma: no cover - cosmetic
        return (
            f"HybridRetriever(bm25_index={self.bm25.index_dir}, "
            f"dense_index={self.dense.index_dir}, rrf_k={self.rrf_k})"
        )

    def warm_up(self) -> None:
        """Force lazy loaders to instantiate (useful in long-running services)."""
        _ = self.bm25.searcher  # type: ignore[attr-defined]
        _ = self.dense.encoder
        self.dense._ensure_loaded()  # type: ignore[attr-defined]
        logger.info("HybridRetriever warmed up.")


def _maybe_to_dict(r: RetrievalResult) -> dict[str, Any]:  # pragma: no cover - helper
    """Cheap (de)serializer for debugging / scripts."""
    return {
        "doc_id": r.doc_id,
        "score": r.score,
        "rank": r.rank,
        "passage": r.passage,
        "metadata": r.metadata,
    }
