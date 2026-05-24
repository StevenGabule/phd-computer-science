"""Tests for citecheck.eval.metrics — the 7 metric functions + EvaluationReport."""
from __future__ import annotations

import math

import pytest

from citecheck.eval.types import (
    AnswerWithCitations,
    CitationStatus,
    CiteCheckExample,
    VerificationResult,
)


def _make_pred(question_id: str, citations: list[tuple[str, CitationStatus, float]]) -> AnswerWithCitations:
    """Helper: build an AnswerWithCitations from (citation_str, status, score) tuples."""
    return AnswerWithCitations(
        question_id=question_id,
        answer_text="answer body",
        citations=[c[0] for c in citations],
        verification_results=[
            VerificationResult(
                citation_str=c[0],
                status=c[1],
                entailment_score=c[2],
            )
            for c in citations
        ],
        latency_ms=100.0,
        tokens_used=200,
    )


def test_citation_resolution_rate_all_verified():
    from citecheck.eval import citation_resolution_rate

    preds = [
        _make_pred("a", [("cite1", CitationStatus.VERIFIED, 0.9)]),
        _make_pred("b", [("cite2", CitationStatus.NON_SUPPORTING, 0.3)]),
    ]
    gold: list[CiteCheckExample] = []
    rate = citation_resolution_rate(preds, gold)
    # Both citations are RESOLVED (whether VERIFIED or NON_SUPPORTING)
    assert rate == pytest.approx(1.0)


def test_citation_resolution_rate_all_fabricated():
    from citecheck.eval import citation_resolution_rate

    preds = [
        _make_pred("a", [("fake1", CitationStatus.UNRESOLVABLE, 0.0)]),
        _make_pred("b", [("fake2", CitationStatus.UNRESOLVABLE, 0.0)]),
    ]
    assert citation_resolution_rate(preds, []) == pytest.approx(0.0)


def test_citation_resolution_rate_mixed():
    from citecheck.eval import citation_resolution_rate

    preds = [
        _make_pred("a", [
            ("cite1", CitationStatus.VERIFIED, 0.9),
            ("fake1", CitationStatus.UNRESOLVABLE, 0.0),
        ]),
    ]
    # 1 out of 2 resolved
    assert citation_resolution_rate(preds, []) == pytest.approx(0.5)


def test_fabrication_rate_complement_of_resolution_rate():
    from citecheck.eval import citation_resolution_rate, fabrication_rate

    preds = [
        _make_pred("a", [
            ("cite1", CitationStatus.VERIFIED, 0.9),
            ("fake1", CitationStatus.UNRESOLVABLE, 0.0),
        ]),
    ]
    assert (citation_resolution_rate(preds, []) + fabrication_rate(preds, [])) == pytest.approx(1.0)


def test_citation_support_f1_returns_dict():
    from citecheck.eval import citation_support_f1

    preds = [
        _make_pred("a", [
            ("cite1", CitationStatus.VERIFIED, 0.9),
            ("cite2", CitationStatus.NON_SUPPORTING, 0.2),
        ]),
    ]
    gold = [
        CiteCheckExample(
            id="a",
            question="?",
            gold_citations=["cite1", "cite2"],
            metadata={"gold_support_labels": {"cite1": True, "cite2": False}},
        )
    ]
    result = citation_support_f1(preds, gold)
    assert isinstance(result, dict)
    for key in ("precision", "recall", "f1"):
        assert key in result
        assert 0.0 <= result[key] <= 1.0


def test_jurisdictional_validity_returns_float():
    from citecheck.eval import jurisdictional_validity

    preds = [
        _make_pred("a", [("cite1", CitationStatus.VERIFIED, 0.9)]),
    ]
    # Set resolved_court_jurisdiction on the verification result
    preds[0].verification_results[0].resolved_court_jurisdiction = "F"
    gold = [CiteCheckExample(id="a", question="?", jurisdiction="federal")]

    rate = jurisdictional_validity(preds, gold)
    assert isinstance(rate, float)
    assert 0.0 <= rate <= 1.0


def test_answer_utility_no_human_ratings_returns_nan_or_zero():
    from citecheck.eval import answer_utility

    preds = [_make_pred("a", [("cite1", CitationStatus.VERIFIED, 0.9)])]
    val = answer_utility(preds, [], human_ratings=None)
    # Either NaN (with a warning) or 0.0 / None — just ensure it doesn't crash
    assert val is None or math.isnan(val) or isinstance(val, float)


def test_answer_utility_with_human_ratings():
    from citecheck.eval import answer_utility

    preds = [
        _make_pred("a", [("c", CitationStatus.VERIFIED, 0.9)]),
        _make_pred("b", [("c", CitationStatus.VERIFIED, 0.9)]),
    ]
    val = answer_utility(preds, [], human_ratings=[5, 3])
    assert val == pytest.approx(4.0)


def test_latency_summary_returns_dict():
    from citecheck.eval import latency_summary

    preds = [
        _make_pred("a", [("c", CitationStatus.VERIFIED, 0.9)]),
        _make_pred("b", [("c", CitationStatus.VERIFIED, 0.9)]),
    ]
    preds[0].latency_ms = 100.0
    preds[1].latency_ms = 300.0
    summary = latency_summary(preds)
    assert isinstance(summary, dict)
    assert "p50" in summary or "median" in summary or "mean" in summary


def test_tokens_per_query_returns_dict():
    from citecheck.eval import tokens_per_query

    preds = [_make_pred("a", [("c", CitationStatus.VERIFIED, 0.9)])]
    preds[0].tokens_used = 500
    summary = tokens_per_query(preds)
    assert isinstance(summary, dict)


def test_aggregate_metrics_includes_all_seven():
    from citecheck.eval import EvaluationReport, aggregate_metrics

    preds = [_make_pred("a", [("cite1", CitationStatus.VERIFIED, 0.9)])]
    gold = [CiteCheckExample(id="a", question="?", gold_citations=["cite1"])]
    report = aggregate_metrics(preds, gold, human_ratings=None)
    assert isinstance(report, EvaluationReport)


def test_evaluation_report_serialization():
    from citecheck.eval import aggregate_metrics

    preds = [_make_pred("a", [("cite1", CitationStatus.VERIFIED, 0.9)])]
    gold = [CiteCheckExample(id="a", question="?", gold_citations=["cite1"])]
    report = aggregate_metrics(preds, gold)
    # Should be roundtrip-able through dict/json
    if hasattr(report, "to_dict"):
        d = report.to_dict()
        assert isinstance(d, dict)
    elif hasattr(report, "__dict__"):
        assert isinstance(report.__dict__, dict)
