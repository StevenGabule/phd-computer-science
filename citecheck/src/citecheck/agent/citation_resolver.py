"""Citation parsing, resolution, and entailment judging.

The :class:`CitationResolver` is the core trust boundary of CiteCheck. It is the
only component that decides whether a citation is real and whether it actually
supports the claim it is attached to. Everything upstream (retrieval, ranking,
generation) is best-effort; everything downstream (loop control, eval metrics)
trusts these verdicts.

Pipeline (per citation):
    1. ``eyecite.get_citations`` lifts Bluebook spans out of free text.
    2. :class:`~citecheck.data.cl_client.CourtListenerClient` resolves to a
       canonical :class:`~citecheck.data.cl_client.CLOpinion` (or fails).
    3. An NLI judge (DeBERTa-v3-large MNLI-FEVER-ANLI by default) scores the
       claim against the opinion body; ``entail >= threshold`` → VERIFIED.

The NLI model is loaded lazily and cached on the instance so cheap callers
(e.g. just wanting to parse) pay no startup cost.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING, Any

from citecheck.config import AGENT, MODELS

if TYPE_CHECKING:
    from citecheck.data.cl_client import CLOpinion, CourtListenerClient

logger = logging.getLogger(__name__)

# Cap how much opinion body we feed to the NLI judge per call. DeBERTa-v3-large
# has a 512-token context window; we chunk and take the max-entailment chunk
# rather than truncating blindly, but each chunk still respects this cap.
_NLI_CHUNK_CHARS = 1800
_NLI_CHUNK_OVERLAP = 200


class CitationStatus(str, Enum):
    """Verdict produced by :meth:`CitationResolver.verify`.

    Values are strings so they JSON-serialize cleanly into eval outputs.
    """

    VERIFIED = "verified"           # parsed, resolved, NLI entailment >= threshold
    UNRESOLVABLE = "unresolvable"   # parsed but CourtListener returned no opinion
    NON_SUPPORTING = "non_supporting"  # resolved but NLI says claim not entailed
    UNKNOWN = "unknown"             # parse failed or judge errored


@dataclass(frozen=True)
class ParsedCitation:
    """A single Bluebook citation lifted from text by eyecite.

    Fields mirror the ``volume reporter page`` triple plus court/year metadata,
    falling back to empty string / ``None`` when eyecite cannot extract a piece.
    """

    raw_text: str
    reporter: str = ""
    volume: str = ""
    page: str = ""
    court: str | None = None
    year: int | None = None
    eyecite_obj: Any = field(default=None, repr=False, compare=False)


@dataclass
class VerificationResult:
    """Per-citation verdict returned by :meth:`CitationResolver.verify`."""

    citation_str: str
    status: CitationStatus
    resolved_opinion: CLOpinion | None = None
    entailment_score: float | None = None
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        """JSON-safe projection (drops the heavy ``CLOpinion`` payload)."""
        return {
            "citation_str": self.citation_str,
            "status": self.status.value,
            "entailment_score": self.entailment_score,
            "notes": self.notes,
            "resolved_opinion_id": (
                getattr(self.resolved_opinion, "id", None) if self.resolved_opinion else None
            ),
        }


class CitationResolver:
    """Parse, resolve, and entailment-judge Bluebook citations.

    Args:
        cl_client: CourtListener client used to look up parsed citations.
        nli_model_name: HuggingFace model id for the entailment judge. Defaults
            to :attr:`citecheck.config.Models.nli_judge`.
        entailment_threshold: NLI ``entailment`` probability at or above which
            a citation is marked :attr:`CitationStatus.VERIFIED`. Defaults to
            :attr:`citecheck.config.Agent.nli_entailment_threshold`.
    """

    def __init__(
        self,
        cl_client: CourtListenerClient,
        nli_model_name: str | None = None,
        entailment_threshold: float = AGENT.nli_entailment_threshold,
    ) -> None:
        self.cl_client = cl_client
        self.nli_model_name = nli_model_name or MODELS.nli_judge
        self.entailment_threshold = entailment_threshold
        # Lazy NLI handles
        self._nli_tokenizer: Any | None = None
        self._nli_model: Any | None = None
        self._nli_entailment_label_id: int | None = None

    # ------------------------------------------------------------------ parse
    def parse_bluebook(self, text: str) -> list[ParsedCitation]:
        """Lift Bluebook citations out of ``text`` via eyecite.

        Returns ``[]`` if eyecite is unavailable or finds nothing. Only
        full-form case citations are returned; short-form ``Id.`` / supra
        references are skipped because they have no standalone resolution.
        """
        try:
            from eyecite import get_citations  # noqa: PLC0415 — lazy import
            from eyecite.models import CaseCitation  # noqa: PLC0415
        except ImportError:  # pragma: no cover — dep listed in pyproject
            logger.warning("eyecite not installed; parse_bluebook returning []")
            return []

        out: list[ParsedCitation] = []
        try:
            citations = get_citations(text)
        except Exception:  # eyecite occasionally raises on malformed input
            logger.exception("eyecite.get_citations failed on %d-char input", len(text))
            return []

        for cit in citations:
            if not isinstance(cit, CaseCitation):
                continue
            groups = getattr(cit, "groups", {}) or {}
            meta = getattr(cit, "metadata", None)
            year_raw = getattr(meta, "year", None) if meta is not None else None
            try:
                year_val = int(year_raw) if year_raw else None
            except (TypeError, ValueError):
                year_val = None
            out.append(
                ParsedCitation(
                    raw_text=getattr(cit, "matched_text", lambda: str(cit))()
                    if callable(getattr(cit, "matched_text", None))
                    else str(cit),
                    reporter=groups.get("reporter", "") or "",
                    volume=groups.get("volume", "") or "",
                    page=groups.get("page", "") or "",
                    court=getattr(meta, "court", None) if meta is not None else None,
                    year=year_val,
                    eyecite_obj=cit,
                )
            )
        logger.debug("parse_bluebook: found %d case citations", len(out))
        return out

    # ------------------------------------------------------------------ verify
    def verify(self, citation_str: str, asserted_claim: str) -> VerificationResult:
        """Run the full parse→resolve→entail pipeline on one citation.

        Args:
            citation_str: Raw citation string as emitted by the LLM, e.g.
                ``"Brown v. Board of Education, 347 U.S. 483 (1954)"``.
            asserted_claim: The natural-language sentence the LLM attached the
                citation to. Used as the NLI ``hypothesis``.

        Returns:
            A :class:`VerificationResult` whose ``status`` is one of the four
            :class:`CitationStatus` values. The result is always returned (no
            exceptions for parse/resolve/judge failures — those surface as
            ``UNRESOLVABLE`` / ``UNKNOWN`` with an explanatory ``notes`` field).
        """
        parsed_list = self.parse_bluebook(citation_str)
        if not parsed_list:
            return VerificationResult(
                citation_str=citation_str,
                status=CitationStatus.UNKNOWN,
                notes="eyecite parse returned no CaseCitation",
            )
        parsed = parsed_list[0]

        # 2) Resolve via CourtListener.
        try:
            opinion = self.cl_client.resolve_citation(citation_str)
        except Exception as exc:
            logger.warning("CL resolve_citation raised on %r: %s", citation_str, exc)
            return VerificationResult(
                citation_str=citation_str,
                status=CitationStatus.UNRESOLVABLE,
                notes=f"CL client error: {exc}",
            )

        if opinion is None:
            return VerificationResult(
                citation_str=citation_str,
                status=CitationStatus.UNRESOLVABLE,
                notes=f"CourtListener returned no opinion for {parsed.raw_text!r}",
            )

        # 3) NLI entailment of the asserted claim against the opinion body.
        body = getattr(opinion, "body_text", None) or getattr(opinion, "plain_text", "") or ""
        if not body.strip():
            return VerificationResult(
                citation_str=citation_str,
                status=CitationStatus.UNKNOWN,
                resolved_opinion=opinion,
                notes="resolved opinion has empty body_text; cannot judge entailment",
            )

        try:
            score = self._score_entailment(asserted_claim, body)
        except Exception as exc:
            logger.exception("NLI judge failed for citation %r", citation_str)
            return VerificationResult(
                citation_str=citation_str,
                status=CitationStatus.UNKNOWN,
                resolved_opinion=opinion,
                notes=f"NLI judge error: {exc}",
            )

        status = (
            CitationStatus.VERIFIED
            if score >= self.entailment_threshold
            else CitationStatus.NON_SUPPORTING
        )
        return VerificationResult(
            citation_str=citation_str,
            status=status,
            resolved_opinion=opinion,
            entailment_score=score,
            notes=f"NLI entail={score:.3f} threshold={self.entailment_threshold:.2f}",
        )

    # ---------------------------------------------------------- NLI internals
    def _ensure_nli_loaded(self) -> None:
        """Lazy-load the NLI tokenizer/model + cache entailment label id."""
        if self._nli_model is not None:
            return
        from transformers import (  # noqa: PLC0415 — heavy, defer
            AutoModelForSequenceClassification,
            AutoTokenizer,
        )

        logger.info("Loading NLI judge %s (first call)", self.nli_model_name)
        self._nli_tokenizer = AutoTokenizer.from_pretrained(self.nli_model_name)
        self._nli_model = AutoModelForSequenceClassification.from_pretrained(
            self.nli_model_name
        )
        self._nli_model.eval()
        # Resolve label id robustly: MNLI-style configs label entailment as
        # "ENTAILMENT" / "entailment" / id2label index 0 depending on checkpoint.
        id2label = getattr(self._nli_model.config, "id2label", {}) or {}
        for idx, name in id2label.items():
            if str(name).lower().startswith("entail"):
                self._nli_entailment_label_id = int(idx)
                break
        if self._nli_entailment_label_id is None:
            self._nli_entailment_label_id = 0  # safe MNLI default
            logger.warning(
                "Could not find entailment label in id2label=%r; defaulting to 0",
                id2label,
            )

    def _score_entailment(self, claim: str, body: str) -> float:
        """Return the max P(entailment | claim, chunk) over body chunks.

        Chunking is character-based with overlap; sufficient for v0.1. A
        token-aware chunker should replace this in v0.2 if we adopt judges
        with non-trivial tokenization (sentencepiece vs. wordpiece behave
        differently on long opinion bodies).
        """
        import torch  # noqa: PLC0415

        self._ensure_nli_loaded()
        assert self._nli_tokenizer is not None
        assert self._nli_model is not None
        assert self._nli_entailment_label_id is not None

        chunks = _chunk_text(body, _NLI_CHUNK_CHARS, _NLI_CHUNK_OVERLAP)
        best = 0.0
        with torch.no_grad():
            for chunk in chunks:
                inputs = self._nli_tokenizer(
                    chunk,
                    claim,
                    truncation=True,
                    max_length=512,
                    return_tensors="pt",
                )
                logits = self._nli_model(**inputs).logits[0]
                probs = torch.softmax(logits, dim=-1)
                entail_p = float(probs[self._nli_entailment_label_id].item())
                if entail_p > best:
                    best = entail_p
        return best


def _chunk_text(text: str, size: int, overlap: int) -> list[str]:
    """Greedy character chunker with overlap; never returns an empty list."""
    if size <= 0:
        raise ValueError("size must be positive")
    if overlap < 0 or overlap >= size:
        raise ValueError("overlap must satisfy 0 <= overlap < size")
    if len(text) <= size:
        return [text]
    out: list[str] = []
    step = size - overlap
    for start in range(0, len(text), step):
        out.append(text[start : start + size])
        if start + size >= len(text):
            break
    return out
