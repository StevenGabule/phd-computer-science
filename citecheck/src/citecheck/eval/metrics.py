"""The seven CiteCheck evaluation metrics + the :class:`EvaluationReport` container.

Every metric function takes ``predictions: list[AnswerWithCitations]`` and (most)
take ``gold: list[CiteCheckExample]``. The two lists are aligned by ``question_id``;
metrics raise ``ValueError`` if the IDs do not match.

Metrics defined here (see ``project/citecheck_design.md`` §4 for justification):

1. :func:`citation_resolution_rate` -- % of emitted citations that resolve to a real
   opinion (status in {VERIFIED, NON_SUPPORTING}).
2. :func:`fabrication_rate` -- ``1 - resolution_rate``; headline safety metric.
3. :func:`citation_support_f1` -- precision / recall / F1 of (citation, supports)
   tuples vs. gold support labels.
4. :func:`jurisdictional_validity` -- % of citations from a binding or persuasive
   jurisdiction for the question's stated jurisdiction.
5. :func:`answer_utility` -- mean Likert 1-5 from human ratings (NaN if none supplied).
6. :func:`latency_summary` -- p50 / p95 / mean from ``AnswerWithCitations.latency_ms``.
7. :func:`tokens_per_query` -- p50 / p95 / mean from ``AnswerWithCitations.tokens_used``.

Plus:

* :func:`aggregate_metrics` -- runs all seven and returns an :class:`EvaluationReport`.
* :func:`per_jurisdiction_breakdown` -- helper that produces per-jurisdiction
  resolution_rate / fabrication_rate slices.
"""
from __future__ import annotations

import logging
import math
from collections import defaultdict
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from typing import Any

import numpy as np

from citecheck.config import AGENT
from citecheck.eval.types import (
    AnswerWithCitations,
    CitationStatus,
    CiteCheckExample,
    VerificationResult,
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Jurisdiction validity lookup
# ---------------------------------------------------------------------------
# Maps the question's stated jurisdiction (normalized) -> set of court
# jurisdiction codes that are BINDING for that question.
_BINDING: dict[str, set[str]] = {
    "federal": {"F", "FS", "FB", "FD", "SCOTUS"},
    "scotus": {"SCOTUS"},
    "supreme_court": {"SCOTUS"},
    "1st_circuit": {"SCOTUS", "F-1"},
    "2d_circuit": {"SCOTUS", "F-2"},
    "3d_circuit": {"SCOTUS", "F-3"},
    "4th_circuit": {"SCOTUS", "F-4"},
    "5th_circuit": {"SCOTUS", "F-5"},
    "6th_circuit": {"SCOTUS", "F-6"},
    "7th_circuit": {"SCOTUS", "F-7"},
    "8th_circuit": {"SCOTUS", "F-8"},
    "9th_circuit": {"SCOTUS", "F-9"},
    "10th_circuit": {"SCOTUS", "F-10"},
    "11th_circuit": {"SCOTUS", "F-11"},
    "dc_circuit": {"SCOTUS", "F-DC"},
    "federal_circuit": {"SCOTUS", "F-FED"},
    # State jurisdictions: binding = own state highest court + SCOTUS on federal questions.
    "california": {"SCOTUS", "S-CA"},
    "new_york": {"SCOTUS", "S-NY"},
    "texas": {"SCOTUS", "S-TX"},
}

# Persuasive (but not binding) jurisdictions. Anything in either binding or
# persuasive counts toward jurisdictional_validity; only "neither" fails.
_PERSUASIVE: dict[str, set[str]] = {
    "federal": {"S-CA", "S-NY", "S-TX"},  # sister-sovereign state cases
    "1st_circuit": {f"F-{i}" for i in range(2, 12)} | {"F-DC", "F-FED"},
    "2d_circuit": {f"F-{i}" for i in [1, 3, 4, 5, 6, 7, 8, 9, 10, 11]} | {"F-DC", "F-FED"},
    "3d_circuit": {f"F-{i}" for i in [1, 2, 4, 5, 6, 7, 8, 9, 10, 11]} | {"F-DC", "F-FED"},
    "4th_circuit": {f"F-{i}" for i in [1, 2, 3, 5, 6, 7, 8, 9, 10, 11]} | {"F-DC", "F-FED"},
    "5th_circuit": {f"F-{i}" for i in [1, 2, 3, 4, 6, 7, 8, 9, 10, 11]} | {"F-DC", "F-FED"},
    "6th_circuit": {f"F-{i}" for i in [1, 2, 3, 4, 5, 7, 8, 9, 10, 11]} | {"F-DC", "F-FED"},
    "7th_circuit": {f"F-{i}" for i in [1, 2, 3, 4, 5, 6, 8, 9, 10, 11]} | {"F-DC", "F-FED"},
    "8th_circuit": {f"F-{i}" for i in [1, 2, 3, 4, 5, 6, 7, 9, 10, 11]} | {"F-DC", "F-FED"},
    "9th_circuit": {f"F-{i}" for i in [1, 2, 3, 4, 5, 6, 7, 8, 10, 11]} | {"F-DC", "F-FED"},
    "10th_circuit": {f"F-{i}" for i in [1, 2, 3, 4, 5, 6, 7, 8, 9, 11]} | {"F-DC", "F-FED"},
    "11th_circuit": {f"F-{i}" for i in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]} | {"F-DC", "F-FED"},
    "california": {"F", "FS", "FB", "FD", "F-9"} | {"S-NY", "S-TX"},
    "new_york": {"F", "FS", "FB", "FD", "F-2"} | {"S-CA", "S-TX"},
    "texas": {"F", "FS", "FB", "FD", "F-5"} | {"S-CA", "S-NY"},
}


def _normalize_jurisdiction(j: str) -> str:
    return j.strip().lower().replace(" ", "_").replace("-", "_")


def _is_binding_or_persuasive(question_jur: str, court_jur: str) -> bool:
    """Return True iff ``court_jur`` is binding or persuasive for ``question_jur``."""
    q = _normalize_jurisdiction(question_jur)
    if not q or not court_jur:
        return False
    binding = _BINDING.get(q, set())
    persuasive = _PERSUASIVE.get(q, set())
    return court_jur in binding or court_jur in persuasive


# ---------------------------------------------------------------------------
# Alignment helper
# ---------------------------------------------------------------------------
def _align(
    predictions: list[AnswerWithCitations],
    gold: list[CiteCheckExample],
) -> list[tuple[AnswerWithCitations, CiteCheckExample]]:
    """Pair each prediction with its gold example by ``question_id`` / ``id``.

    Raises ``ValueError`` if the two sets of IDs do not match exactly.
    """
    gold_by_id = {ex.id: ex for ex in gold}
    pred_ids = {p.question_id for p in predictions}
    if pred_ids != set(gold_by_id):
        missing_in_gold = pred_ids - set(gold_by_id)
        missing_in_pred = set(gold_by_id) - pred_ids
        raise ValueError(
            f"Prediction / gold ID mismatch. "
            f"Missing in gold: {sorted(missing_in_gold)[:5]} ... "
            f"Missing in predictions: {sorted(missing_in_pred)[:5]} ..."
        )
    return [(p, gold_by_id[p.question_id]) for p in predictions]


def _iter_verification_results(
    predictions: list[AnswerWithCitations],
) -> list[VerificationResult]:
    """Flatten all per-citation verification results across predictions."""
    out: list[VerificationResult] = []
    for p in predictions:
        out.extend(getattr(p, "verification_results", []) or [])
    return out


# ---------------------------------------------------------------------------
# Metric 1: citation_resolution_rate
# ---------------------------------------------------------------------------
def citation_resolution_rate(
    predictions: list[AnswerWithCitations],
    gold: list[CiteCheckExample] | None = None,  # noqa: ARG001 - kept for signature symmetry
) -> float:
    """Fraction of emitted citations that resolved to a real opinion.

    A citation counts as "resolved" if its
    :class:`citecheck.eval.types.CitationStatus` is one of
    ``VERIFIED`` or ``NON_SUPPORTING`` (both mean the registry returned an
    opinion; the difference is only whether it entails the claim).

    Returns ``0.0`` when no citations were emitted (vacuously zero — a system
    that emits nothing cannot be safe).
    """
    results = _iter_verification_results(predictions)
    if not results:
        return 0.0
    resolved = sum(
        1
        for r in results
        if r.status in (CitationStatus.VERIFIED, CitationStatus.NON_SUPPORTING)
    )
    return resolved / len(results)


# ---------------------------------------------------------------------------
# Metric 2: fabrication_rate
# ---------------------------------------------------------------------------
def fabrication_rate(
    predictions: list[AnswerWithCitations],
    gold: list[CiteCheckExample] | None = None,
) -> float:
    """The headline metric: ``1.0 - citation_resolution_rate``.

    Counts the fraction of emitted citations that are either unresolvable
    (fabricated) or malformed (syntactically broken).
    """
    return 1.0 - citation_resolution_rate(predictions, gold)


# ---------------------------------------------------------------------------
# Metric 3: citation_support_f1
# ---------------------------------------------------------------------------
def citation_support_f1(
    predictions: list[AnswerWithCitations],
    gold: list[CiteCheckExample],
    threshold: float = AGENT.nli_entailment_threshold,
) -> dict[str, float]:
    """Precision / recall / F1 of (citation_str, supports_claim) tuples vs. gold.

    Args:
        predictions: Per-question predictions.
        gold: Aligned gold examples. Each must carry
            ``metadata["gold_support_labels"]: dict[citation_str -> bool]``
            for the (citation, supports) tuples to be scored. Citations absent
            from the gold labels are ignored (i.e. partial coverage is OK).
        threshold: Entailment-score cutoff. A citation is predicted as
            supporting iff ``status == VERIFIED`` AND
            ``entailment_score >= threshold``.

    Returns:
        Dict with keys ``"precision"``, ``"recall"``, ``"f1"``,
        ``"support"`` (the number of (pred, gold) tuples that contributed).
        All values are floats; F1 / precision / recall fall back to ``0.0`` if
        the corresponding denominator is zero (rather than NaN, so callers can
        always serialize the result).
    """
    paired = _align(predictions, gold)
    tp = fp = fn = support = 0
    for pred, ex in paired:
        gold_labels: dict[str, bool] = ex.metadata.get("gold_support_labels", {}) or {}
        # Map citation_str -> predicted supports flag.
        pred_labels: dict[str, bool] = {}
        for vr in pred.verification_results or []:
            pred_labels[vr.citation_str] = (
                vr.status == CitationStatus.VERIFIED and vr.entailment_score >= threshold
            )
        for citation_str, gold_supports in gold_labels.items():
            support += 1
            pred_supports = pred_labels.get(citation_str, False)
            if pred_supports and gold_supports:
                tp += 1
            elif pred_supports and not gold_supports:
                fp += 1
            elif (not pred_supports) and gold_supports:
                fn += 1
            # (not pred_supports) and (not gold_supports) is a true negative; no contribution.
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0
    return {
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "support": float(support),
    }


# ---------------------------------------------------------------------------
# Metric 4: jurisdictional_validity
# ---------------------------------------------------------------------------
def jurisdictional_validity(
    predictions: list[AnswerWithCitations],
    gold: list[CiteCheckExample],
) -> float:
    """Fraction of resolved citations from a binding or persuasive jurisdiction.

    Only **resolved** citations (status VERIFIED or NON_SUPPORTING) contribute
    to the denominator — unresolvable citations cannot have a jurisdiction
    and are handled by :func:`fabrication_rate` instead.

    Returns ``0.0`` if no resolved citations exist.
    """
    paired = _align(predictions, gold)
    total = good = 0
    for pred, ex in paired:
        q_jur = ex.jurisdiction
        for vr in pred.verification_results or []:
            if vr.status not in (CitationStatus.VERIFIED, CitationStatus.NON_SUPPORTING):
                continue
            total += 1
            if _is_binding_or_persuasive(q_jur, vr.resolved_court_jurisdiction):
                good += 1
    if total == 0:
        return 0.0
    return good / total


# ---------------------------------------------------------------------------
# Metric 5: answer_utility
# ---------------------------------------------------------------------------
def answer_utility(
    predictions: list[AnswerWithCitations],
    gold: list[CiteCheckExample] | None = None,  # noqa: ARG001
    human_ratings: list[int] | None = None,
) -> float:
    """Mean Likert 1-5 utility rating.

    Falls back to ``NaN`` (with a logged warning) when no ratings are provided,
    because there is no defensible automated proxy for "is this answer useful
    to a lawyer". The CiteCheck design calls for a 100-item human audit.

    Args:
        predictions: Used only to validate ``len(human_ratings) ==
            len(predictions)`` when ratings are present.
        gold: Unused; accepted for signature symmetry.
        human_ratings: One integer in ``[1, 5]`` per prediction, in the same
            order. May contain ``None`` for skipped items; those are ignored.
    """
    if human_ratings is None:
        logger.warning(
            "answer_utility requires human audit; returning NaN. "
            "Pass human_ratings (one Likert 1-5 per prediction)."
        )
        return float("nan")
    if len(human_ratings) != len(predictions):
        raise ValueError(
            f"human_ratings length ({len(human_ratings)}) must equal "
            f"predictions length ({len(predictions)})."
        )
    valid = [int(r) for r in human_ratings if r is not None]
    for r in valid:
        if not 1 <= r <= 5:
            raise ValueError(f"Likert rating out of [1,5]: {r}")
    if not valid:
        return float("nan")
    return float(np.mean(valid))


# ---------------------------------------------------------------------------
# Metric 6: latency_summary
# ---------------------------------------------------------------------------
def latency_summary(
    predictions: list[AnswerWithCitations],
) -> dict[str, float]:
    """Return p50 / p95 / mean of per-query latency in milliseconds.

    Returns NaN for all stats if no prediction reports ``latency_ms``.
    """
    latencies = [
        p.latency_ms for p in predictions if getattr(p, "latency_ms", None) is not None
    ]
    if not latencies:
        return {"p50": float("nan"), "p95": float("nan"), "mean": float("nan")}
    arr = np.asarray(latencies, dtype=float)
    return {
        "p50": float(np.percentile(arr, 50)),
        "p95": float(np.percentile(arr, 95)),
        "mean": float(np.mean(arr)),
    }


# ---------------------------------------------------------------------------
# Metric 7: tokens_per_query
# ---------------------------------------------------------------------------
def tokens_per_query(
    predictions: list[AnswerWithCitations],
) -> dict[str, float]:
    """Return p50 / p95 / mean of per-query token usage.

    Returns NaN for all stats if no prediction reports ``tokens_used``.
    """
    tokens = [
        p.tokens_used for p in predictions if getattr(p, "tokens_used", None) is not None
    ]
    if not tokens:
        return {"p50": float("nan"), "p95": float("nan"), "mean": float("nan")}
    arr = np.asarray(tokens, dtype=float)
    return {
        "p50": float(np.percentile(arr, 50)),
        "p95": float(np.percentile(arr, 95)),
        "mean": float(np.mean(arr)),
    }


# ---------------------------------------------------------------------------
# Per-jurisdiction breakdown
# ---------------------------------------------------------------------------
def per_jurisdiction_breakdown(
    predictions: list[AnswerWithCitations],
    gold: list[CiteCheckExample],
) -> dict[str, dict[str, float]]:
    """Group predictions by question jurisdiction and compute per-slice stats.

    Returns a dict mapping jurisdiction -> {resolution_rate, fabrication_rate,
    jurisdictional_validity, n_questions, n_citations}.
    """
    paired = _align(predictions, gold)
    by_jur: dict[str, list[tuple[AnswerWithCitations, CiteCheckExample]]] = defaultdict(list)
    for pred, ex in paired:
        by_jur[ex.jurisdiction or "unknown"].append((pred, ex))

    out: dict[str, dict[str, float]] = {}
    for jur, pairs in by_jur.items():
        slice_preds = [p for p, _ in pairs]
        slice_gold = [g for _, g in pairs]
        n_citations = sum(len(p.verification_results or []) for p in slice_preds)
        out[jur] = {
            "resolution_rate": citation_resolution_rate(slice_preds),
            "fabrication_rate": fabrication_rate(slice_preds),
            "jurisdictional_validity": jurisdictional_validity(slice_preds, slice_gold),
            "n_questions": float(len(slice_preds)),
            "n_citations": float(n_citations),
        }
    return out


# ---------------------------------------------------------------------------
# EvaluationReport
# ---------------------------------------------------------------------------
@dataclass(slots=True)
class EvaluationReport:
    """Frozen result of an evaluation run.

    Attributes:
        run_id: Caller-supplied run identifier (timestamp by default).
        timestamp: ISO-8601 UTC timestamp when the report was produced.
        baseline_name: Human-readable name of the system-under-test.
        model_name: Model identifier (e.g. ``"meta-llama/Llama-3.1-8B-Instruct"``).
        sample_size: Number of predictions scored.
        resolution_rate: See :func:`citation_resolution_rate`.
        fabrication_rate: See :func:`fabrication_rate`.
        citation_support_f1: Dict {precision, recall, f1, support}.
        jurisdictional_validity: See :func:`jurisdictional_validity`.
        answer_utility: Mean Likert; NaN if no human ratings.
        latency_ms: Dict {p50, p95, mean}.
        tokens: Dict {p50, p95, mean}.
        per_jurisdiction: Per-slice breakdown.
        extra: Free-form additional fields a caller wants to record.
    """

    run_id: str
    timestamp: str
    baseline_name: str
    model_name: str
    sample_size: int

    resolution_rate: float
    fabrication_rate: float
    citation_support_f1: dict[str, float]
    jurisdictional_validity: float
    answer_utility: float
    latency_ms: dict[str, float]
    tokens: dict[str, float]
    per_jurisdiction: dict[str, dict[str, float]]
    extra: dict[str, Any] = field(default_factory=dict)

    # ---- (de)serialization ------------------------------------------------
    def to_dict(self) -> dict[str, Any]:
        """Return a plain-dict view (NaN values become the string ``"NaN"``).

        JSON itself cannot represent ``NaN`` cross-platform, so we substitute
        the literal string. Use :meth:`from_dict` to round-trip.
        """
        return _replace_nans(asdict(self), sentinel="NaN")

    def to_json(self, indent: int | None = 2) -> str:
        import json

        return json.dumps(self.to_dict(), indent=indent)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> EvaluationReport:
        """Inverse of :meth:`to_dict`. ``"NaN"`` strings are restored to floats."""
        restored = _replace_nans(d, sentinel="NaN", restore=True)
        # Pop unknown keys into ``extra`` rather than crashing — protects against
        # forward-compatible report schemas.
        fields = {f for f in cls.__dataclass_fields__}  # noqa: C416
        known = {k: v for k, v in restored.items() if k in fields}
        extras = {k: v for k, v in restored.items() if k not in fields}
        if extras:
            known.setdefault("extra", {}).update(extras)
        return cls(**known)


def _replace_nans(
    obj: Any,
    sentinel: str = "NaN",
    restore: bool = False,
) -> Any:
    """Walk ``obj`` swapping floats(NaN) <-> ``sentinel`` string for JSON safety."""
    if isinstance(obj, dict):
        return {k: _replace_nans(v, sentinel, restore) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_replace_nans(v, sentinel, restore) for v in obj]
    if isinstance(obj, tuple):
        return tuple(_replace_nans(v, sentinel, restore) for v in obj)
    if not restore and isinstance(obj, float) and math.isnan(obj):
        return sentinel
    if restore and obj == sentinel:
        return float("nan")
    return obj


# ---------------------------------------------------------------------------
# aggregate_metrics
# ---------------------------------------------------------------------------
def aggregate_metrics(
    predictions: list[AnswerWithCitations],
    gold: list[CiteCheckExample],
    human_ratings: list[int] | None = None,
    *,
    baseline_name: str = "unknown",
    model_name: str = "unknown",
    run_id: str | None = None,
    extra: dict[str, Any] | None = None,
) -> EvaluationReport:
    """Compute all seven metrics + jurisdiction breakdown and pack into an
    :class:`EvaluationReport`.

    This is the canonical way to evaluate a run. Equivalent to calling the
    individual metric functions and assembling a report by hand.
    """
    timestamp = datetime.now(UTC).isoformat()
    if run_id is None:
        run_id = f"run-{timestamp.replace(':', '').replace('-', '').split('.')[0]}"

    return EvaluationReport(
        run_id=run_id,
        timestamp=timestamp,
        baseline_name=baseline_name,
        model_name=model_name,
        sample_size=len(predictions),
        resolution_rate=citation_resolution_rate(predictions),
        fabrication_rate=fabrication_rate(predictions),
        citation_support_f1=citation_support_f1(predictions, gold),
        jurisdictional_validity=jurisdictional_validity(predictions, gold),
        answer_utility=answer_utility(predictions, gold, human_ratings),
        latency_ms=latency_summary(predictions),
        tokens=tokens_per_query(predictions),
        per_jurisdiction=per_jurisdiction_breakdown(predictions, gold),
        extra=dict(extra or {}),
    )


__all__ = [
    "EvaluationReport",
    "aggregate_metrics",
    "answer_utility",
    "citation_resolution_rate",
    "citation_support_f1",
    "fabrication_rate",
    "jurisdictional_validity",
    "latency_summary",
    "per_jurisdiction_breakdown",
    "tokens_per_query",
]
