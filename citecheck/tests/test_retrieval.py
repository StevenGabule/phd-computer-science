"""Tests for citecheck.retrieval.* — BM25, dense, RRF fusion.

Only the RRF fusion + ``RetrievalResult`` tests run by default. The BM25 and
dense smoke tests are marked ``@pytest.mark.slow`` / ``@pytest.mark.gpu`` and
skipped on a vanilla ``pytest`` invocation (no indexes / models / JVM).
"""
from __future__ import annotations

import pytest

from citecheck.retrieval import RetrievalResult, rrf_fusion


# ---------------------------------------------------------------------------
# RetrievalResult dataclass
# ---------------------------------------------------------------------------
def test_retrieval_result_dataclass():
    r = RetrievalResult(doc_id="d1", score=0.9, rank=1, passage="text")
    assert r.doc_id == "d1"
    assert r.score == pytest.approx(0.9)
    assert r.rank == 1
    assert r.passage == "text"
    assert r.metadata == {}


def test_retrieval_result_default_metadata_is_independent():
    """Two RetrievalResult instances must not share the default metadata dict."""
    a = RetrievalResult(doc_id="a", score=1.0, rank=1)
    b = RetrievalResult(doc_id="b", score=0.5, rank=2)
    a.metadata["k"] = "v"
    assert "k" not in b.metadata


# ---------------------------------------------------------------------------
# rrf_fusion — known-output tests
# ---------------------------------------------------------------------------
def test_rrf_fusion_basic():
    """Documents appearing high in BOTH rankings rank above singletons."""
    list_a = [
        RetrievalResult(doc_id="A", score=0.9, rank=1),
        RetrievalResult(doc_id="B", score=0.8, rank=2),
        RetrievalResult(doc_id="C", score=0.7, rank=3),
    ]
    list_b = [
        RetrievalResult(doc_id="B", score=0.95, rank=1),
        RetrievalResult(doc_id="A", score=0.85, rank=2),
        RetrievalResult(doc_id="D", score=0.6, rank=3),
    ]
    fused = rrf_fusion([list_a, list_b], k=60)
    doc_ids = [r.doc_id for r in fused]
    # A and B appear in both -> should rank above C and D (singletons).
    assert set(doc_ids[:2]) == {"A", "B"}
    assert set(doc_ids[2:]) == {"C", "D"}


def test_rrf_fusion_known_scores_match_formula():
    """For a tiny input, the fused scores must equal the RRF formula by hand.

    RRF score = sum_r 1 / (k + rank). With k=60:
      A: 1/(60+1) + 1/(60+2)  = 1/61 + 1/62
      B: 1/(60+2) + 1/(60+1)  = 1/62 + 1/61  (same as A)
      C: 1/(60+3)             = 1/63
      D: 1/(60+3)             = 1/63
    So {A, B} > {C, D}, and A's score == B's score, C's == D's.
    """
    list_a = [
        RetrievalResult(doc_id="A", score=0.9, rank=1),
        RetrievalResult(doc_id="B", score=0.8, rank=2),
        RetrievalResult(doc_id="C", score=0.7, rank=3),
    ]
    list_b = [
        RetrievalResult(doc_id="B", score=0.95, rank=1),
        RetrievalResult(doc_id="A", score=0.85, rank=2),
        RetrievalResult(doc_id="D", score=0.6, rank=3),
    ]
    fused = rrf_fusion([list_a, list_b], k=60)
    score_by_id = {r.doc_id: r.score for r in fused}
    expected_ab = 1 / 61 + 1 / 62
    expected_cd = 1 / 63
    assert score_by_id["A"] == pytest.approx(expected_ab)
    assert score_by_id["B"] == pytest.approx(expected_ab)
    assert score_by_id["C"] == pytest.approx(expected_cd)
    assert score_by_id["D"] == pytest.approx(expected_cd)


def test_rrf_fusion_top_k_truncation():
    docs_a = [RetrievalResult(doc_id=f"d{i}", score=0.9 - 0.1 * i, rank=i + 1) for i in range(5)]
    docs_b = [RetrievalResult(doc_id=f"d{i}", score=0.95 - 0.1 * i, rank=i + 1) for i in range(5)]
    fused = rrf_fusion([docs_a, docs_b], k=60, top_k=3)
    assert len(fused) == 3


def test_rrf_fusion_empty_input():
    assert rrf_fusion([], k=60) == []
    assert rrf_fusion([[], []], k=60) == []


def test_rrf_fusion_single_list_preserves_order():
    single = [
        RetrievalResult(doc_id="x", score=0.9, rank=1),
        RetrievalResult(doc_id="y", score=0.7, rank=2),
    ]
    fused = rrf_fusion([single], k=60)
    assert [r.doc_id for r in fused] == ["x", "y"]


def test_rrf_fusion_assigns_fresh_ranks():
    """Output ranks must be a 1-based contiguous sequence by descending score."""
    fused = rrf_fusion(
        [
            [RetrievalResult("a", 0, 1), RetrievalResult("b", 0, 2)],
            [RetrievalResult("b", 0, 1), RetrievalResult("a", 0, 2)],
        ],
        k=60,
    )
    assert [r.rank for r in fused] == list(range(1, len(fused) + 1))


def test_rrf_fusion_passage_preferred_from_richer_input():
    """When a doc_id appears with a passage and without, the passage wins."""
    list_a = [RetrievalResult(doc_id="A", score=1.0, rank=1, passage=None)]
    list_b = [RetrievalResult(doc_id="A", score=1.0, rank=1, passage="text")]
    fused = rrf_fusion([list_a, list_b], k=60)
    assert fused[0].passage == "text"


def test_rrf_fusion_negative_k_rejected():
    """RRF's smoothing constant must be positive."""
    with pytest.raises(ValueError):
        rrf_fusion([[RetrievalResult("a", 1, 1)]], k=0)


# ---------------------------------------------------------------------------
# Slow / GPU smoke tests — skipped by default
# ---------------------------------------------------------------------------
@pytest.mark.slow
def test_bm25_retriever_build_index_and_search(tmp_path):
    """Integration smoke test — requires pyserini + JDK 21."""
    pytest.importorskip("pyserini")
    from citecheck.retrieval import BM25Retriever

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
def test_dense_retriever_constructible(tmp_path):
    """Smoke test — DenseRetriever must be constructible without a GPU."""
    pytest.importorskip("sentence_transformers")
    pytest.importorskip("faiss")
    from citecheck.retrieval import DenseRetriever

    retriever = DenseRetriever(index_dir=tmp_path / "dense")
    assert retriever is not None
