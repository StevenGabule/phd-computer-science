"""CiteCheck evaluation layer.

Re-exports the seven metric functions, the :class:`EvaluationReport`
container, the :class:`LLMJudge`, and the :class:`EvaluationRunner` so that
callers can do::

    from citecheck.eval import (
        EvaluationReport,
        EvaluationRunner,
        LLMJudge,
        aggregate_metrics,
        answer_utility,
        citation_resolution_rate,
        citation_support_f1,
        fabrication_rate,
        jurisdictional_validity,
        latency_summary,
        tokens_per_query,
    )

See ``project/citecheck_design.md`` §4 for the rationale behind each metric.
"""
from __future__ import annotations

from citecheck.eval.judge import LLMJudge
from citecheck.eval.metrics import (
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
from citecheck.eval.runner import EvaluationRunner
from citecheck.eval.types import (
    AnswerWithCitations,
    BaselineProtocol,
    CitationStatus,
    CiteCheckExample,
    VerificationResult,
)

__all__ = [
    # Types (re-exported for convenience; canonical sources live in sibling pkgs)
    "AnswerWithCitations",
    "BaselineProtocol",
    "CitationStatus",
    "CiteCheckExample",
    "VerificationResult",
    # Metrics
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
    # Judge + runner
    "LLMJudge",
    "EvaluationRunner",
]
