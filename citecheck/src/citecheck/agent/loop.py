"""CiteCheck verify-then-emit loop.

This is the orchestrator that ties retrieval, reranking, generation, and
citation verification into one pipeline. It is the *thing* whose behavior is
being measured against the five baselines in Phase 2.

Algorithm (one iteration)::

    1. retrieve top-k passages
    2. (optional) rerank with cross-encoder + λ-weighted MMR
    3. build prompt (system + context + question + verification feedback)
    4. generate answer (constrained-decoded for citation slots if enabled)
    5. parse Bluebook citations from the answer
    6. verify each citation: parse → CL resolve → NLI judge
    7. if all VERIFIED or budget exhausted → return
       else → record feedback (which cites failed and why), goto step 3

The loop's contract is the same as the baselines' contract
(:class:`~citecheck.baselines.protocol.BaselineProtocol`), so it can be plugged
into the same eval harness.
"""
from __future__ import annotations

import logging
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from citecheck.agent.citation_resolver import (
    CitationResolver,
    CitationStatus,
    VerificationResult,
)
from citecheck.agent.grammar import BluebookGrammar
from citecheck.config import AGENT

if TYPE_CHECKING:
    from citecheck.retrieval import RetrievalResult

logger = logging.getLogger(__name__)

Generator = Callable[[str], str]


@dataclass
class AnswerWithCitations:
    """Top-level result returned by :meth:`VerifyLoop.answer` and baselines.

    Attributes:
        text: Final answer string emitted by the generator.
        citations: List of ``(citation_str, VerificationResult)`` pairs. Empty
            list means the answer contained no recognized citations (which is
            itself a failure mode for legal QA, but the loop will not synthesize
            them).
        iterations_used: Number of generation passes consumed; useful for both
            cost accounting and for diagnosing loop instability.
        retrieved_doc_ids: IDs of passages fed into the prompt on the final
            iteration (for traceability and eval).
    """

    text: str
    citations: list[tuple[str, VerificationResult]] = field(default_factory=list)
    iterations_used: int = 0
    retrieved_doc_ids: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "text": self.text,
            "citations": [
                {"citation_str": c, "verification": v.to_dict()} for c, v in self.citations
            ],
            "iterations_used": self.iterations_used,
            "retrieved_doc_ids": self.retrieved_doc_ids,
        }


_SYSTEM_PROMPT = """You are a careful legal research assistant. Answer the \
user's question using only the provided case-law excerpts. Every factual or \
legal claim MUST be followed by a Bluebook citation in the form \
"<Case Name>, <vol> <Reporter> <page> (<court> <year>)". If the excerpts do \
not support an answer, say so and cite no cases. Do not invent citations."""


class VerifyLoop:
    """Iterative retrieval-augmented generation with citation verification.

    Args:
        generator: Any callable ``(prompt: str) -> str``. This lets the loop
            wrap a local ``transformers`` pipeline, an OpenRouter HTTP client,
            an ``outlines`` constrained sampler, etc. without coupling to any
            specific LLM backend.
        retriever: Object with ``.search(query: str, top_k: int) ->
            Sequence[RetrievalResult]``. Typically a
            :class:`~citecheck.retrieval.HybridRetriever`.
        reranker: Optional cross-encoder with ``.rerank(query, candidates,
            lambda_) -> Sequence[RetrievalResult]``. If ``None``, the
            retriever's order is used as-is.
        resolver: :class:`CitationResolver` used to verify each emitted cite.
        max_iterations: Hard cap on regeneration rounds. Default
            :attr:`Agent.max_iterations`.
        use_constrained_decoding: If True, the grammar is exposed in the prompt
            (and, when the generator backend supports it, used to constrain
            generation). The generator callable is responsible for actually
            wiring up Outlines if it wants hard constraints; the loop merely
            advertises the regex.
        top_k: Number of passages to retrieve per iteration.
        rerank_lambda: ``λ`` for MMR-style reranking; passed straight to
            ``reranker.rerank``.
    """

    def __init__(
        self,
        generator: Generator,
        retriever: Any,
        reranker: Any | None,
        resolver: CitationResolver,
        max_iterations: int = AGENT.max_iterations,
        use_constrained_decoding: bool = AGENT.constrained_decoding,
        top_k: int = 10,
        rerank_lambda: float = 0.5,
    ) -> None:
        if max_iterations < 1:
            raise ValueError("max_iterations must be >= 1")
        self.generator = generator
        self.retriever = retriever
        self.reranker = reranker
        self.resolver = resolver
        self.max_iterations = max_iterations
        self.use_constrained_decoding = use_constrained_decoding
        self.top_k = top_k
        self.rerank_lambda = rerank_lambda
        self.grammar = BluebookGrammar() if use_constrained_decoding else None

    # ----------------------------------------------------------------- public
    def answer(self, question: str) -> AnswerWithCitations:
        """Run the full verify loop and return a citation-checked answer."""
        passages = self._retrieve_and_rerank(question)
        feedback: list[str] = []
        last_text = ""
        last_cites: list[tuple[str, VerificationResult]] = []

        for iteration in range(1, self.max_iterations + 1):
            prompt = self._build_prompt(question, passages, feedback)
            logger.debug("Iter %d: prompting generator (%d chars)", iteration, len(prompt))
            text = self.generator(prompt)
            cites = self._verify_all(text)
            last_text, last_cites = text, cites

            if not cites:
                logger.info("Iter %d: no citations emitted; stopping", iteration)
                break

            bad = [(c, v) for c, v in cites
                   if v.status in (CitationStatus.UNRESOLVABLE, CitationStatus.NON_SUPPORTING)]
            if not bad:
                logger.info("Iter %d: all %d citations VERIFIED", iteration, len(cites))
                break

            if iteration == self.max_iterations:
                logger.info(
                    "Iter %d: %d/%d citations failed; budget exhausted",
                    iteration, len(bad), len(cites),
                )
                break

            feedback = self._format_feedback(bad)
            logger.info(
                "Iter %d: %d/%d citations failed; regenerating with feedback",
                iteration, len(bad), len(cites),
            )

        return AnswerWithCitations(
            text=last_text,
            citations=last_cites,
            iterations_used=iteration,
            retrieved_doc_ids=[_doc_id(p) for p in passages],
        )

    # ---------------------------------------------------------------- helpers
    def _retrieve_and_rerank(self, question: str) -> Sequence[RetrievalResult]:
        """Run first-stage retrieval, then (optionally) reranking."""
        try:
            candidates = self.retriever.search(question, top_k=self.top_k)
        except TypeError:
            # Some retrievers use positional-only signatures.
            candidates = self.retriever.search(question)
        if self.reranker is None or not candidates:
            return candidates
        try:
            return self.reranker.rerank(question, candidates, lambda_=self.rerank_lambda)
        except Exception:
            logger.exception("reranker.rerank failed; falling back to retriever order")
            return candidates

    def _build_prompt(
        self,
        question: str,
        passages: Sequence[RetrievalResult],
        feedback: list[str],
    ) -> str:
        """Assemble the generator prompt for one iteration."""
        ctx_blocks = []
        for i, p in enumerate(passages, 1):
            text = getattr(p, "text", None) or getattr(p, "passage", "") or ""
            doc_id = _doc_id(p)
            ctx_blocks.append(f"[{i}] (doc_id={doc_id})\n{text}")
        context = "\n\n".join(ctx_blocks) if ctx_blocks else "(no passages retrieved)"

        sections = [_SYSTEM_PROMPT, "", "### Context", context, "", "### Question", question]
        if self.grammar is not None:
            sections.extend([
                "",
                "### Citation format",
                "Citations must match this regex (Bluebook full form):",
                self.grammar.bluebook_regex,
            ])
        if feedback:
            sections.extend(["", "### Verification feedback from previous attempt"])
            sections.extend(f"- {line}" for line in feedback)
            sections.append(
                "Revise the answer. Remove or replace any citation flagged above. "
                "If you cannot find a supporting citation in the context, omit the claim."
            )
        sections.extend(["", "### Answer"])
        return "\n".join(sections)

    def _verify_all(self, text: str) -> list[tuple[str, VerificationResult]]:
        """Parse every citation in ``text`` and verify each one.

        We pass the full answer text as the ``asserted_claim`` rather than
        trying to surgically split sentences — this is a deliberate over-approx
        for v0.1: it makes verification *harder* (NLI has to entail more
        material from less specific evidence) but it avoids brittle sentence
        segmentation that misattributes claims to citations.
        """
        parsed = self.resolver.parse_bluebook(text)
        out: list[tuple[str, VerificationResult]] = []
        seen: set[str] = set()
        for pc in parsed:
            cite_str = pc.raw_text.strip()
            if cite_str in seen:
                continue
            seen.add(cite_str)
            result = self.resolver.verify(cite_str, asserted_claim=text)
            out.append((cite_str, result))
        return out

    @staticmethod
    def _format_feedback(
        bad: list[tuple[str, VerificationResult]],
    ) -> list[str]:
        """Convert failed verifications into actionable bullets for the prompt."""
        lines: list[str] = []
        for cite, v in bad:
            if v.status is CitationStatus.UNRESOLVABLE:
                lines.append(
                    f"{cite!r}: not found in CourtListener — citation appears fabricated."
                )
            elif v.status is CitationStatus.NON_SUPPORTING:
                score = v.entailment_score if v.entailment_score is not None else float("nan")
                lines.append(
                    f"{cite!r}: real case, but NLI judge says it does NOT support the claim "
                    f"(entailment={score:.2f})."
                )
            else:
                lines.append(f"{cite!r}: could not verify ({v.notes})")
        return lines


def _doc_id(p: Any) -> str:
    """Best-effort extraction of a passage's stable identifier."""
    for attr in ("doc_id", "id", "passage_id"):
        v = getattr(p, attr, None)
        if v is not None:
            return str(v)
    return "unknown"
