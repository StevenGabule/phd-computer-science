"""Unit tests for ``citecheck.eval.metrics``.

Every metric is exercised with hand-crafted inputs whose expected output is
computable by hand so failures point directly at the metric definition. The
EvaluationReport JSON round-trip is also covered here.
"""
from __future__ import annotations

import json
import math

import pytest

from citecheck.eval import (
    EvaluationReport,
    aggregate_metrics,
    answer_utility,
    citation_resolution_rate,
    citation_support_f1,
    fabrication_rate,
    jurisdictional_validity,
    latency_summary,
    per_jurisdiction_breakdown,
    tokens_per_query,
)
from citecheck.eval.types import (
    AnswerWithCitations,
    CitationStatus,
    CiteCheckExample,
    VerificationResult,
)


def _make_gold(
    id: str,  # noqa: A002 - mirrors the dataclass field name
    *,
    question: str = "?",
    gold_citations: list | None = None,
    jurisdiction: str = "",
    source: str = "manual",
    metadata: dict | None = None,
) -> CiteCheckExample:
    """Helper that handles both real and fallback CiteCheckExample shapes.

    The canonical (data.eval_set) variant is a frozen dataclass with no
    defaults; the eval-layer fallback (citecheck.eval.types) has defaults
    for everything but id/question. Try the kwargs-only form first.
    """
    return CiteCheckExample(
        id=id,
        question=question,
        gold_citations=gold_citations if gold_citations is not None else [],
        jurisdiction=jurisdiction,
        source=source,
        metadata=metadata if metadata is not None else {},
    )


def _make_pred(
    question_id: str,
    citations: list[tuple[str, CitationStatus, float]],
    *,
    court_jur: str = "F",
    latency_ms: float | None = 100.0,
    tokens_used: int | None = 200,
) -> AnswerWithCitations:
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
                resolved_opinion_id=(
                    None if c[1] == CitationStatus.UNRESOLVABLE else 1
                ),
                resolved_court_jurisdiction=(
                    "" if c[1] == CitationStatus.UNRESOLVABLE else court_jur
                ),
            )
            for c in citations
        ],
        latency_ms=latency_ms,
        tokens_used=tokens_used,
    )


# ---------------------------------------------------------------------------
# Metric 1: citation_resolution_rate
# ---------------------------------------------------------------------------
def test_citation_resolution_rate_all_verified():
    preds = [
        _make_pred("a", [("c1", CitationStatus.VERIFIED, 0.9)]),
        _make_pred("b", [("c2", CitationStatus.NON_SUPPORTING, 0.3)]),
    ]
    # Both VERIFIED and NON_SUPPORTING count as resolved.
    assert citation_resolution_rate(preds, []) == pytest.approx(1.0)


def test_citation_resolution_rate_all_fabricated():
    preds = [
        _make_pred("a", [("fake1", CitationStatus.UNRESOLVABLE, 0.0)]),
        _make_pred("b", [("fake2", CitationStatus.UNRESOLVABLE, 0.0)]),
    ]
    assert citation_resolution_rate(preds, []) == pytest.approx(0.0)


def test_citation_resolution_rate_mixed():
    preds = [
        _make_pred(
            "a",
            [
                ("c1", CitationStatus.VERIFIED, 0.9),
                ("fake1", CitationStatus.UNRESOLVABLE, 0.0),
                ("c2", CitationStatus.NON_SUPPORTING, 0.2),
                ("bad", CitationStatus.MALFORMED, 0.0),
            ],
        ),
    ]
    # 2 of 4 resolved -> 0.5.
    assert citation_resolution_rate(preds, []) == pytest.approx(0.5)


def test_citation_resolution_rate_zero_citations_returns_zero():
    preds = [_make_pred("a", [])]
    assert citation_resolution_rate(preds, []) == pytest.approx(0.0)


# ---------------------------------------------------------------------------
# Metric 2: fabrication_rate
# ---------------------------------------------------------------------------
def test_fabrication_rate_complement_of_resolution_rate():
    preds = [
        _make_pred(
            "a",
            [
                ("c1", CitationStatus.VERIFIED, 0.9),
                ("fake1", CitationStatus.UNRESOLVABLE, 0.0),
            ],
        ),
    ]
    assert (
        citation_resolution_rate(preds, []) + fabrication_rate(preds, [])
        == pytest.approx(1.0)
    )


def test_fabrication_rate_pure_garbage_is_one():
    preds = [_make_pred("a", [("fake", CitationStatus.UNRESOLVABLE, 0.0)])]
    assert fabrication_rate(preds, []) == pytest.approx(1.0)


# ---------------------------------------------------------------------------
# Metric 3: citation_support_f1
# ---------------------------------------------------------------------------
def test_citation_support_f1_perfect_score():
    preds = [
        _make_pred(
            "a",
            [
                ("c1", CitationStatus.VERIFIED, 0.95),  # >= 0.7 -> supports
                ("c2", CitationStatus.VERIFIED, 0.95),
            ],
        ),
    ]
    gold = [
        _make_gold(
            id="a",
            metadata={"gold_support_labels": {"c1": True, "c2": True}},
        )
    ]
    result = citation_support_f1(preds, gold)
    assert result["precision"] == pytest.approx(1.0)
    assert result["recall"] == pytest.approx(1.0)
    assert result["f1"] == pytest.approx(1.0)
    assert result["support"] == pytest.approx(2.0)


def test_citation_support_f1_hand_computed_pr():
    """Two preds: TP=1, FP=1, FN=1 -> precision 0.5, recall 0.5, f1 0.5."""
    preds = [
        _make_pred(
            "a",
            [
                ("c1", CitationStatus.VERIFIED, 0.9),  # predicts support
                ("c2", CitationStatus.VERIFIED, 0.9),  # predicts support
            ],
        )
    ]
    gold = [
        _make_gold(
            id="a",
            metadata={
                "gold_support_labels": {
                    "c1": True,   # TP
                    "c2": False,  # FP
                    "c3": True,   # FN (gold says support, model never emitted)
                }
            },
        )
    ]
    result = citation_support_f1(preds, gold)
    assert result["precision"] == pytest.approx(0.5)
    assert result["recall"] == pytest.approx(0.5)
    assert result["f1"] == pytest.approx(0.5)
    assert result["support"] == pytest.approx(3.0)


def test_citation_support_f1_threshold_gating():
    """A VERIFIED citation below the threshold is treated as non-supporting."""
    preds = [
        _make_pred(
            "a",
            [
                ("c1", CitationStatus.VERIFIED, 0.5),  # below default 0.7 -> NOT supports
            ],
        )
    ]
    gold = [_make_gold(id="a", metadata={"gold_support_labels": {"c1": True}})]
    result = citation_support_f1(preds, gold, threshold=0.7)
    # pred_supports=False, gold=True -> FN; precision=0, recall=0, f1=0
    assert result["recall"] == pytest.approx(0.0)
    assert result["precision"] == pytest.approx(0.0)
    assert result["f1"] == pytest.approx(0.0)


def test_citation_support_f1_returns_zero_on_empty_labels():
    preds = [_make_pred("a", [("c1", CitationStatus.VERIFIED, 0.9)])]
    gold = [_make_gold(id="a")]  # no gold_support_labels
    result = citation_support_f1(preds, gold)
    assert result["support"] == pytest.approx(0.0)
    assert result["f1"] == pytest.approx(0.0)


# ---------------------------------------------------------------------------
# Metric 4: jurisdictional_validity
# ---------------------------------------------------------------------------
def test_jurisdictional_validity_federal_binding():
    preds = [_make_pred("a", [("c1", CitationStatus.VERIFIED, 0.9)], court_jur="F")]
    gold = [_make_gold(id="a", jurisdiction="federal")]
    assert jurisdictional_validity(preds, gold) == pytest.approx(1.0)


def test_jurisdictional_validity_sister_circuit_persuasive():
    """For a 9th-Cir question, a 2d-Cir opinion is persuasive (counts as valid)."""
    preds = [_make_pred("a", [("c1", CitationStatus.VERIFIED, 0.9)], court_jur="F-2")]
    gold = [_make_gold(id="a", jurisdiction="9th_circuit")]
    assert jurisdictional_validity(preds, gold) == pytest.approx(1.0)


def test_jurisdictional_validity_wrong_court_fails():
    """A California-state opinion is not binding/persuasive for a 9th-Cir federal question."""
    preds = [_make_pred("a", [("c1", CitationStatus.VERIFIED, 0.9)], court_jur="S-NY")]
    gold = [_make_gold(id="a", jurisdiction="9th_circuit")]
    assert jurisdictional_validity(preds, gold) == pytest.approx(0.0)


def test_jurisdictional_validity_ignores_unresolvable():
    """Unresolvable citations should NOT enter the denominator."""
    preds = [
        _make_pred(
            "a",
            [
                ("c1", CitationStatus.VERIFIED, 0.9),
                ("fake", CitationStatus.UNRESOLVABLE, 0.0),
            ],
            court_jur="F",
        )
    ]
    gold = [_make_gold(id="a", jurisdiction="federal")]
    # 1/1 resolved + valid; the fake is excluded.
    assert jurisdictional_validity(preds, gold) == pytest.approx(1.0)


def test_jurisdictional_validity_no_resolved_returns_zero():
    preds = [_make_pred("a", [("fake", CitationStatus.UNRESOLVABLE, 0.0)])]
    gold = [_make_gold(id="a", jurisdiction="federal")]
    assert jurisdictional_validity(preds, gold) == pytest.approx(0.0)


# ---------------------------------------------------------------------------
# Metric 5: answer_utility
# ---------------------------------------------------------------------------
def test_answer_utility_no_human_ratings_returns_nan():
    preds = [_make_pred("a", [("c1", CitationStatus.VERIFIED, 0.9)])]
    val = answer_utility(preds, [], human_ratings=None)
    assert math.isnan(val)


def test_answer_utility_with_human_ratings():
    preds = [
        _make_pred("a", [("c", CitationStatus.VERIFIED, 0.9)]),
        _make_pred("b", [("c", CitationStatus.VERIFIED, 0.9)]),
    ]
    assert answer_utility(preds, [], human_ratings=[5, 3]) == pytest.approx(4.0)


def test_answer_utility_skips_none_ratings():
    preds = [
        _make_pred("a", [("c", CitationStatus.VERIFIED, 0.9)]),
        _make_pred("b", [("c", CitationStatus.VERIFIED, 0.9)]),
    ]
    # type ignore: function accepts None entries
    assert answer_utility(preds, [], human_ratings=[5, None]) == pytest.approx(5.0)


def test_answer_utility_rejects_out_of_range():
    preds = [_make_pred("a", [("c", CitationStatus.VERIFIED, 0.9)])]
    with pytest.raises(ValueError):
        answer_utility(preds, [], human_ratings=[7])


def test_answer_utility_length_mismatch_raises():
    preds = [_make_pred("a", [("c", CitationStatus.VERIFIED, 0.9)])]
    with pytest.raises(ValueError):
        answer_utility(preds, [], human_ratings=[5, 4])


# ---------------------------------------------------------------------------
# Metric 6: latency_summary
# ---------------------------------------------------------------------------
def test_latency_summary_basic_percentiles():
    preds = [
        _make_pred(f"q{i}", [("c", CitationStatus.VERIFIED, 0.9)], latency_ms=float(i))
        for i in range(1, 101)
    ]
    summary = latency_summary(preds)
    assert summary["mean"] == pytest.approx(50.5)
    assert summary["p50"] == pytest.approx(50.5)
    assert summary["p95"] == pytest.approx(95.05, rel=1e-2)


def test_latency_summary_returns_nan_when_no_latency():
    preds = [_make_pred("a", [("c", CitationStatus.VERIFIED, 0.9)], latency_ms=None)]
    summary = latency_summary(preds)
    assert math.isnan(summary["p50"])
    assert math.isnan(summary["p95"])
    assert math.isnan(summary["mean"])


# ---------------------------------------------------------------------------
# Metric 7: tokens_per_query
# ---------------------------------------------------------------------------
def test_tokens_per_query_basic():
    preds = [
        _make_pred("a", [("c", CitationStatus.VERIFIED, 0.9)], tokens_used=100),
        _make_pred("b", [("c", CitationStatus.VERIFIED, 0.9)], tokens_used=300),
    ]
    summary = tokens_per_query(preds)
    assert summary["mean"] == pytest.approx(200.0)
    assert summary["p50"] == pytest.approx(200.0)


def test_tokens_per_query_returns_nan_when_unset():
    preds = [_make_pred("a", [("c", CitationStatus.VERIFIED, 0.9)], tokens_used=None)]
    summary = tokens_per_query(preds)
    assert math.isnan(summary["mean"])


# ---------------------------------------------------------------------------
# per_jurisdiction_breakdown
# ---------------------------------------------------------------------------
def test_per_jurisdiction_breakdown_groups_correctly():
    preds = [
        _make_pred("a", [("c", CitationStatus.VERIFIED, 0.9)], court_jur="F"),
        _make_pred("b", [("c", CitationStatus.UNRESOLVABLE, 0.0)], court_jur="F"),
        _make_pred("c", [("c", CitationStatus.VERIFIED, 0.9)], court_jur="F-9"),
    ]
    gold = [
        _make_gold(id="a", jurisdiction="federal"),
        _make_gold(id="b", jurisdiction="federal"),
        _make_gold(id="c", jurisdiction="9th_circuit"),
    ]
    breakdown = per_jurisdiction_breakdown(preds, gold)
    assert set(breakdown.keys()) == {"federal", "9th_circuit"}
    assert breakdown["federal"]["resolution_rate"] == pytest.approx(0.5)
    assert breakdown["9th_circuit"]["resolution_rate"] == pytest.approx(1.0)
    assert breakdown["federal"]["n_questions"] == pytest.approx(2.0)


# ---------------------------------------------------------------------------
# aggregate_metrics
# ---------------------------------------------------------------------------
def test_aggregate_metrics_includes_all_seven_fields():
    preds = [_make_pred("a", [("c1", CitationStatus.VERIFIED, 0.9)], court_jur="F")]
    gold = [
        _make_gold(
            id="a",
            jurisdiction="federal",
            metadata={"gold_support_labels": {"c1": True}},
        )
    ]
    report = aggregate_metrics(preds, gold, baseline_name="test", model_name="m")
    assert isinstance(report, EvaluationReport)
    assert report.sample_size == 1
    assert report.baseline_name == "test"
    assert report.model_name == "m"
    assert report.resolution_rate == pytest.approx(1.0)
    assert report.fabrication_rate == pytest.approx(0.0)
    assert "f1" in report.citation_support_f1
    assert report.jurisdictional_validity == pytest.approx(1.0)
    assert math.isnan(report.answer_utility)
    assert set(report.latency_ms.keys()) == {"p50", "p95", "mean"}
    assert set(report.tokens.keys()) == {"p50", "p95", "mean"}
    assert "federal" in report.per_jurisdiction


def test_aggregate_metrics_with_human_ratings():
    preds = [
        _make_pred("a", [("c1", CitationStatus.VERIFIED, 0.9)]),
        _make_pred("b", [("c2", CitationStatus.VERIFIED, 0.9)]),
    ]
    gold = [_make_gold(id="a"), _make_gold(id="b")]
    report = aggregate_metrics(preds, gold, human_ratings=[5, 3])
    assert report.answer_utility == pytest.approx(4.0)


def test_aggregate_metrics_mismatched_ids_raises():
    preds = [_make_pred("a", [("c1", CitationStatus.VERIFIED, 0.9)])]
    gold = [_make_gold(id="b")]
    with pytest.raises(ValueError):
        aggregate_metrics(preds, gold)


# ---------------------------------------------------------------------------
# EvaluationReport serialization
# ---------------------------------------------------------------------------
def test_evaluation_report_to_dict_is_json_serializable():
    preds = [_make_pred("a", [("c1", CitationStatus.VERIFIED, 0.9)])]
    gold = [_make_gold(id="a")]
    report = aggregate_metrics(preds, gold)
    # answer_utility is NaN here; to_dict must replace NaN with the sentinel.
    d = report.to_dict()
    json_str = json.dumps(d)
    assert "NaN" in json_str
    # Reload back into a dict and an EvaluationReport.
    reloaded = json.loads(json_str)
    assert reloaded["sample_size"] == 1
    restored = EvaluationReport.from_dict(reloaded)
    assert restored.sample_size == 1
    assert math.isnan(restored.answer_utility)


def test_evaluation_report_to_json_is_indented_by_default():
    preds = [_make_pred("a", [("c1", CitationStatus.VERIFIED, 0.9)])]
    gold = [_make_gold(id="a")]
    report = aggregate_metrics(preds, gold)
    s = report.to_json()
    assert "\n" in s  # default indent=2 produces multi-line JSON


def test_evaluation_report_from_dict_round_trips_extras():
    """Unknown keys are routed into ``extra`` rather than raising."""
    preds = [_make_pred("a", [("c1", CitationStatus.VERIFIED, 0.9)])]
    gold = [_make_gold(id="a")]
    report = aggregate_metrics(preds, gold, extra={"git_sha": "deadbeef"})
    d = report.to_dict()
    d["unknown_key"] = "stuff"
    restored = EvaluationReport.from_dict(d)
    assert restored.extra.get("git_sha") == "deadbeef"
    assert restored.extra.get("unknown_key") == "stuff"
