"""Tests for citecheck.retrieval.* — BM25, dense, RRF fusion."""
from __future__ import annotations

import pytest


def test_retrieval_result_dataclass():
    from citecheck.retrieval import RetrievalResult

    r = RetrievalResult(doc_id="d1", score=0.9, rank=1, passage="text")
    assert r.doc_id == "d1"
    assert r.score == 0.9
    assert r.rank == 1
    assert r.passage == "text"


def test_rrf_fusion_basic():
    """RRF should rank documents that appear high in multiple lists above
    documents that appear high in only one."""
    from citecheck.retrieval import RetrievalResult, rrf_fusion

    list_a = [
        RetrievalResult(doc_id="A", score=0.9, rank=1, passage=""),
        RetrievalResult(doc_id="B", score=0.8, rank=2, passage=""),
        RetrievalResult(doc_id="C", score=0.7, rank=3, passage=""),
    ]
    list_b = [
        RetrievalResult(doc_id="B", score=0.95, rank=1, passage=""),
        RetrievalResult(doc_id="A", score=0.85, rank=2, passage=""),
        RetrievalResult(doc_id="D", score=0.6, rank=3, passage=""),
    ]
    fused = rrf_fusion([list_a, list_b], k=60)
    doc_ids = [r.doc_id for r in fused]
    # A and B appear in both → should be top-2
    assert set(doc_ids[:2]) == {"A", "B"}
    # C and D appear in only one each → ranked below
    assert set(doc_ids[2:]) == {"C", "D"}


def test_rrf_fusion_top_k_truncation():
    from citecheck.retrieval import RetrievalResult, rrf_fusion

    docs_a = [RetrievalResult(doc_id=f"d{i}", score=0.9 - i * 0.1, rank=i + 1, passage="") for i in range(5)]
    docs_b = [RetrievalResult(doc_id=f"d{i}", score=0.95 - i * 0.1, rank=i + 1, passage="") for i in range(5)]
    fused = rrf_fusion([docs_a, docs_b], k=60, top_k=3)
    assert len(fused) == 3


def test_rrf_fusion_empty_input():
    from citecheck.retrieval import rrf_fusion

    assert rrf_fusion([], k=60) == []
    assert rrf_fusion([[], []], k=60) == []


def test_rrf_fusion_single_list():
    """Fusing a single list should preserve its order."""
    from citecheck.retrieval import RetrievalResult, rrf_fusion

    single = [
        RetrievalResult(doc_id="x", score=0.9, rank=1, passage=""),
        RetrievalResult(doc_id="y", score=0.7, rank=2, passage=""),
    ]
    fused = rrf_fusion([single], k=60)
    assert [r.doc_id for r in fused] == ["x", "y"]


@pytest.mark.slow
def test_bm25_retriever_build_index_and_search(tmp_path):
    """Integration test — requires pyserini + JDK 21 on PATH."""
    from citecheck.retrieval import BM25Retriever

    # Skip if pyserini unavailable
    pytest.importorskip("pyserini")

    corpus_jsonl = tmp_path / "corpus.jsonl"
    corpus_jsonl.write_text(
        '{"id": "1", "contents": "fixture supplier liability design defect"}\n'
        '{"id": "2", "contents": "summary judgment standard federal rule"}\n',
        encoding="utf-8",
    )
    index_dir = tmp_path / "index"
    retriever = BM25Retriever(index_dir=index_dir)
    retriever.build_index(corpus_jsonl)
    results = retriever.search("design defect", top_k=5)
    assert len(results) >= 1
    assert results[0].doc_id == "1"


@pytest.mark.gpu
def test_dense_retriever_build_and_search_smoke(tmp_path):
    """Smoke test — requires GPU and the dense encoder model."""
    pytest.importorskip("sentence_transformers")
    pytest.importorskip("faiss")
    from citecheck.retrieval import DenseRetriever

    retriever = DenseRetriever(index_dir=tmp_path / "dense")
    # Don't actually run; just confirm constructible
    assert retriever is not None
