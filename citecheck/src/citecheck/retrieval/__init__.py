"""CiteCheck retrieval layer.

Two first-stage retrievers (sparse BM25 via Pyserini/Lucene, dense bi-encoder via
sentence-transformers + FAISS) and a Reciprocal Rank Fusion (RRF) combiner that
together form the ``HybridRetriever`` used by the agentic verifier.

Typical usage::

    from citecheck.retrieval import (
        BM25Retriever,
        DenseRetriever,
        HybridRetriever,
        RetrievalResult,
        rrf_fusion,
    )

    hybrid = HybridRetriever()
    results = hybrid.search("Miranda warning custodial interrogation", top_k=20)
"""
from __future__ import annotations

from citecheck.retrieval.bm25 import (
    BM25Retriever,
    RetrievalResult,
    corpus_to_pyserini_jsonl,
)
from citecheck.retrieval.dense import DenseRetriever
from citecheck.retrieval.fusion import HybridRetriever, rrf_fusion

__all__ = [
    "BM25Retriever",
    "DenseRetriever",
    "HybridRetriever",
    "RetrievalResult",
    "corpus_to_pyserini_jsonl",
    "rrf_fusion",
]
