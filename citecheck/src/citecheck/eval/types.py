"""Eval-layer data contracts.

The evaluation layer needs a slightly different ``AnswerWithCitations`` /
``VerificationResult`` shape than the agent's internal types: eval needs
per-question latency, token counts, and a verification list keyed by
``VerificationResult`` (not a tuple), and a single ``question_id`` to align
predictions with gold examples.

Design decision (intentional): we define these types HERE rather than
importing the agent's variants because

1. The agent's ``AnswerWithCitations`` carries ``iterations_used`` and a
   ``list[tuple[str, VerificationResult]]`` for citations — useful for the
   *agent's* introspection but awkward for the *eval* layer (no easy
   ``predictions[i].verification_results`` access).
2. The agent's ``VerificationResult`` carries the heavy ``CLOpinion`` payload
   inline; eval-time results only need IDs and the court jurisdiction code.
3. ``CitationStatus`` here adds a ``MALFORMED`` value (citation that does not
   parse as a Bluebook cite) which the agent currently subsumes under
   ``UNKNOWN``. Keeping them separate lets the metrics distinguish
   "fabricated" from "garbled".

Adapters: ``EvaluationRunner._answer_one`` accepts the agent's output and
either uses it directly (when it matches this shape) or wraps it; this
single boundary is the only place that needs to know about both forms.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any, Protocol, runtime_checkable

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# CitationStatus
# ---------------------------------------------------------------------------
class CitationStatus(StrEnum):
    """Outcome of verifying a single emitted citation against a registry.

    Values are strings so they serialize cleanly into JSON eval traces.
    """

    VERIFIED = "verified"
    """Resolved to a real opinion and the asserted claim is supported."""

    NON_SUPPORTING = "non_supporting"
    """Resolved to a real opinion but the opinion does not entail the claim."""

    UNRESOLVABLE = "unresolvable"
    """Citation string could not be resolved to any real opinion (fabricated)."""

    MALFORMED = "malformed"
    """Citation string does not parse as a Bluebook citation."""

    UNKNOWN = "unknown"
    """Parse / resolver / judge returned an error; status is indeterminate."""


# ---------------------------------------------------------------------------
# VerificationResult
# ---------------------------------------------------------------------------
@dataclass(slots=True)
class VerificationResult:
    """Per-citation verdict consumed by the eval metrics.

    Attributes:
        citation_str: The Bluebook-style citation string emitted by the model.
        status: :class:`CitationStatus` enum value.
        entailment_score: NLI entailment probability in ``[0.0, 1.0]``. Set to
            ``0.0`` for fabricated / malformed citations.
        resolved_opinion_id: CourtListener opinion ID when resolved, else
            ``None``.
        resolved_court_jurisdiction: Court jurisdiction code of the resolved
            opinion (e.g. ``"F-9"`` for the Ninth Circuit). Empty string when
            unresolved.
        reasoning: Free-form explanation (e.g. NLI judge rationale).
    """

    citation_str: str
    status: CitationStatus
    entailment_score: float = 0.0
    resolved_opinion_id: int | None = None
    resolved_court_jurisdiction: str = ""
    reasoning: str = ""

    @classmethod
    def from_agent_result(
        cls, agent_result: Any, citation_str: str | None = None
    ) -> VerificationResult:
        """Build an eval :class:`VerificationResult` from the agent's variant.

        The agent's ``citecheck.agent.VerificationResult`` carries
        ``resolved_opinion`` (a heavy ``CLOpinion``) plus ``notes`` instead of
        ``reasoning``; this adapter projects to the eval shape and tolerates
        either source.
        """
        status = getattr(agent_result, "status", None)
        if isinstance(status, str):
            try:
                status = CitationStatus(status)
            except ValueError:
                status = CitationStatus.UNKNOWN
        elif not isinstance(status, CitationStatus):
            # Try to map by name from the agent's enum to ours.
            name = getattr(status, "value", None) or getattr(status, "name", "")
            try:
                status = CitationStatus(str(name).lower())
            except ValueError:
                status = CitationStatus.UNKNOWN

        opinion = getattr(agent_result, "resolved_opinion", None)
        opinion_id = getattr(opinion, "id", None) if opinion is not None else (
            getattr(agent_result, "resolved_opinion_id", None)
        )
        jurisdiction = (
            getattr(opinion, "court_jurisdiction", "")
            if opinion is not None
            else getattr(agent_result, "resolved_court_jurisdiction", "")
        )
        score = getattr(agent_result, "entailment_score", None)
        return cls(
            citation_str=citation_str or getattr(agent_result, "citation_str", ""),
            status=status if isinstance(status, CitationStatus) else CitationStatus.UNKNOWN,
            entailment_score=float(score) if score is not None else 0.0,
            resolved_opinion_id=int(opinion_id) if opinion_id is not None else None,
            resolved_court_jurisdiction=str(jurisdiction or ""),
            reasoning=str(
                getattr(agent_result, "notes", "")
                or getattr(agent_result, "reasoning", "")
            ),
        )


# ---------------------------------------------------------------------------
# AnswerWithCitations
# ---------------------------------------------------------------------------
@dataclass(slots=True)
class AnswerWithCitations:
    """A baseline / agent's answer with its emitted citations and verification.

    This is the eval-layer's canonical answer shape. The agent's internal
    ``AnswerWithCitations`` (``citecheck.agent.loop.AnswerWithCitations``)
    has a slightly different field set; use :meth:`from_agent_answer` to
    bridge between the two at the runner / baseline boundary.

    Attributes:
        question_id: Identifier of the source eval example. Always set by the
            runner before metrics are computed.
        answer_text: Natural-language answer body.
        citations: Ordered list of emitted citation strings as they appear
            in ``answer_text``.
        verification_results: Per-citation :class:`VerificationResult`,
            aligned 1:1 with ``citations`` when verification has been run;
            empty list before verification.
        latency_ms: End-to-end wall time for ``baseline.answer(question)`` in
            milliseconds. ``None`` if not measured.
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

    @classmethod
    def from_agent_answer(
        cls,
        agent_answer: Any,
        *,
        question_id: str = "",
        latency_ms: float | None = None,
        tokens_used: int | None = None,
    ) -> AnswerWithCitations:
        """Wrap an agent ``AnswerWithCitations`` into the eval-layer shape.

        Handles both the eval shape (pass-through) and the agent's
        ``citations: list[tuple[str, VerificationResult]]`` shape.
        """
        # Already eval-shaped? Just copy / inject missing fields.
        _eval_shape_fields = ("question_id", "answer_text", "verification_results")
        if all(hasattr(agent_answer, f) for f in _eval_shape_fields):
            _latency = (
                latency_ms
                if latency_ms is not None
                else getattr(agent_answer, "latency_ms", None)
            )
            _tokens = (
                tokens_used
                if tokens_used is not None
                else getattr(agent_answer, "tokens_used", None)
            )
            return cls(
                question_id=question_id or agent_answer.question_id,
                answer_text=agent_answer.answer_text,
                citations=list(agent_answer.citations or []),
                verification_results=list(agent_answer.verification_results or []),
                latency_ms=_latency,
                tokens_used=_tokens,
                metadata=dict(getattr(agent_answer, "metadata", {}) or {}),
            )

        # Agent shape: text + citations=list[(str, VR)]
        text = getattr(agent_answer, "text", "") or getattr(agent_answer, "answer_text", "")
        raw_citations = getattr(agent_answer, "citations", []) or []
        citation_strings: list[str] = []
        verification_results: list[VerificationResult] = []
        for entry in raw_citations:
            if isinstance(entry, tuple) and len(entry) == 2:
                cite_str, vr = entry
                citation_strings.append(str(cite_str))
                verification_results.append(
                    VerificationResult.from_agent_result(vr, citation_str=str(cite_str))
                )
            elif isinstance(entry, str):
                citation_strings.append(entry)
            else:
                # Object with .citation_str / .status fields -- treat as a VR.
                citation_strings.append(getattr(entry, "citation_str", str(entry)))
                verification_results.append(VerificationResult.from_agent_result(entry))

        metadata: dict[str, Any] = {}
        iterations_used = getattr(agent_answer, "iterations_used", None)
        if iterations_used is not None:
            metadata["iterations_used"] = iterations_used
        retrieved = getattr(agent_answer, "retrieved_doc_ids", None)
        if retrieved is not None:
            metadata["retrieved_doc_ids"] = list(retrieved)

        return cls(
            question_id=question_id,
            answer_text=text,
            citations=citation_strings,
            verification_results=verification_results,
            latency_ms=latency_ms,
            tokens_used=tokens_used,
            metadata=metadata,
        )


# ---------------------------------------------------------------------------
# CiteCheckExample
# ---------------------------------------------------------------------------
# Try the canonical home in citecheck.data.eval_set; fall back to a local
# dataclass when that module hasn't shipped yet. The fallback shape mirrors
# the documented interface exactly so swapping at import-time is transparent.
try:  # pragma: no cover - import-time dispatch
    from citecheck.data.eval_set import CiteCheckExample  # type: ignore[no-redef]
except Exception:  # noqa: BLE001 - intentional broad except for partial-checkout
    logger.debug("citecheck.data.eval_set.CiteCheckExample unavailable; using fallback")

    @dataclass(slots=True)
    class CiteCheckExample:  # type: ignore[no-redef]
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
    """Structural protocol every baseline / system-under-test implements.

    Any class with ``answer(question: str) -> AnswerWithCitations`` satisfies
    this protocol. The :class:`citecheck.eval.EvaluationRunner` accepts any
    such object. Returned answers may be either eval-shaped or agent-shaped;
    the runner converts via :meth:`AnswerWithCitations.from_agent_answer`.
    """

    def answer(self, question: str) -> AnswerWithCitations:
        """Produce an answer with citations for ``question``."""
        ...


__all__ = [
    "AnswerWithCitations",
    "BaselineProtocol",
    "CitationStatus",
    "CiteCheckExample",
    "VerificationResult",
]
