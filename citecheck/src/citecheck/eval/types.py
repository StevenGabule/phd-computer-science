"""Shared interface types for the evaluation layer.

The evaluation layer depends on a small set of data contracts that are produced
by the agent, baseline, and data modules (other agents are responsible for
those packages). To keep ``citecheck.eval`` importable on a fresh checkout
where those sibling modules may not yet exist, this module declares minimal
fallback definitions that mirror the documented public interface.

When the sibling modules *do* exist, callers should construct objects of the
real types — this module's definitions are structurally compatible because the
metrics, runner, and judge only access fields via ``getattr`` (with sensible
defaults). The single source of truth at runtime is the object instances passed
to the evaluation functions.

Re-export order
---------------
1. Try to import the real definitions from their canonical sibling modules.
2. On failure (module not yet implemented), fall back to local dataclasses /
   ``Protocol`` definitions defined here.

Tests can monkeypatch ``citecheck.eval.types`` to inject fakes if needed.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Protocol, runtime_checkable

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# CitationStatus
# ---------------------------------------------------------------------------
try:  # pragma: no cover - import-time dispatch
    from citecheck.agent import CitationStatus  # type: ignore[attr-defined]
except Exception:  # noqa: BLE001 - intentional broad except for fallback
    logger.debug("citecheck.agent.CitationStatus unavailable; using eval-local fallback")

    class CitationStatus(str, Enum):
        """Outcome of verifying a single emitted citation against a registry."""

        VERIFIED = "verified"
        """Resolved to a real opinion and the asserted claim is supported."""

        NON_SUPPORTING = "non_supporting"
        """Resolved to a real opinion but the opinion does not entail the claim."""

        UNRESOLVABLE = "unresolvable"
        """Citation string could not be resolved to any real opinion (fabricated)."""

        MALFORMED = "malformed"
        """Citation string does not parse as a Bluebook citation."""


# ---------------------------------------------------------------------------
# VerificationResult
# ---------------------------------------------------------------------------
try:  # pragma: no cover - import-time dispatch
    from citecheck.agent import VerificationResult  # type: ignore[attr-defined]
except Exception:  # noqa: BLE001
    logger.debug("citecheck.agent.VerificationResult unavailable; using fallback")

    @dataclass(slots=True)
    class VerificationResult:
        """Outcome of CitationResolver.verify(citation_str, asserted_claim).

        Attributes:
            citation_str: The Bluebook-style citation string emitted by the model.
            status: :class:`CitationStatus` enum value.
            entailment_score: NLI entailment probability in ``[0.0, 1.0]``. For
                fabricated citations this is set to ``0.0``.
            resolved_opinion_id: CourtListener opinion ID when resolved, else
                ``None``.
            resolved_court_jurisdiction: Court jurisdiction code of the resolved
                opinion (e.g. ``"F"`` for federal). Empty string when unresolved.
            reasoning: Free-form explanation (e.g. NLI judge rationale). Empty
                by default.
        """

        citation_str: str
        status: CitationStatus
        entailment_score: float = 0.0
        resolved_opinion_id: int | None = None
        resolved_court_jurisdiction: str = ""
        reasoning: str = ""


# ---------------------------------------------------------------------------
# AnswerWithCitations
# ---------------------------------------------------------------------------
try:  # pragma: no cover - import-time dispatch
    from citecheck.agent import AnswerWithCitations  # type: ignore[attr-defined]
except Exception:  # noqa: BLE001
    logger.debug("citecheck.agent.AnswerWithCitations unavailable; using fallback")

    @dataclass(slots=True)
    class AnswerWithCitations:
        """A baseline / agent's answer with its emitted citations and verification.

        Attributes:
            question_id: Identifier of the source eval example.
            answer_text: Natural-language answer body.
            citations: Ordered list of emitted citation strings as they appear
                in ``answer_text``.
            verification_results: Per-citation :class:`VerificationResult`,
                aligned 1:1 with ``citations`` when verification has been run;
                empty list before verification.
            latency_ms: End-to-end wall time for ``baseline.answer(question)``
                in milliseconds. ``None`` if not measured.
            tokens_used: Total tokens consumed by the call (prompt + completion).
                ``None`` if not tracked.
            metadata: Free-form per-baseline provenance.
        """

        question_id: str
        answer_text: str
        citations: list[str] = field(default_factory=list)
        verification_results: list[VerificationResult] = field(default_factory=list)
        latency_ms: float | None = None
        tokens_used: int | None = None
        metadata: dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# CiteCheckExample
# ---------------------------------------------------------------------------
try:  # pragma: no cover - import-time dispatch
    from citecheck.data import CiteCheckExample  # type: ignore[attr-defined]
except Exception:  # noqa: BLE001
    logger.debug("citecheck.data.CiteCheckExample unavailable; using fallback")

    @dataclass(slots=True)
    class CiteCheckExample:
        """A single evaluation example.

        Attributes:
            id: Stable identifier.
            question: The natural-language question posed to the LLM.
            gold_citations: List of Bluebook citation strings that a correct
                answer is expected to cite (order-insensitive).
            jurisdiction: The jurisdiction the question is asked under
                (e.g. ``"federal"``, ``"9th_circuit"``, ``"california"``).
            source: Where this example came from (``"charlotin"``, ``"cuad"``,
                ``"legalbench_rag"``, etc.).
            metadata: Free-form, includes optional ``gold_support_labels``
                (mapping citation_str -> bool) for Citation Support F1.
        """

        id: str
        question: str
        gold_citations: list[str] = field(default_factory=list)
        jurisdiction: str = ""
        source: str = ""
        metadata: dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# BaselineProtocol
# ---------------------------------------------------------------------------
@runtime_checkable
class BaselineProtocol(Protocol):
    """Structural protocol that every baseline / system-under-test implements.

    Any class with ``answer(question: str) -> AnswerWithCitations`` satisfies
    this protocol. The ``EvaluationRunner`` accepts any such object.
    """

    def answer(self, question: str) -> "AnswerWithCitations":
        """Produce an answer with citations for ``question``."""
        ...


__all__ = [
    "AnswerWithCitations",
    "BaselineProtocol",
    "CitationStatus",
    "CiteCheckExample",
    "VerificationResult",
]
