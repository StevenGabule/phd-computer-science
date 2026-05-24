"""Corrective RAG baseline (Yan et al., 2024).

Paper: "Corrective Retrieval Augmented Generation." Yan et al. add a
lightweight *retrieval evaluator* (originally a fine-tuned T5-large) between
the retriever and the generator. The evaluator scores each retrieved doc and
the result is routed:

    * ``Correct``  → use as-is (with internal knowledge stripping refinement).
    * ``Incorrect`` → discard, fall back to web search.
    * ``Ambiguous`` → use both retrieved docs AND web search.

This reimplementation:

    * Implements the **prompted-LLM-judge** variant of the evaluator (cheap,
      no extra fine-tuning required). A note in the docstring points at the
      original T5 checkpoint for callers who want the faithful version.
    * **Skips the web-search fallback by design**: CiteCheck's whole point is
      that adding ungrounded web results to legal QA is a hallucination
      amplifier. We replace the fallback with *abstain-or-warn* and document
      this divergence loudly. An implementer who *does* want web search can
      pass a ``web_search`` callable.
    * Implements the "knowledge refinement" pass (decompose doc into strips,
      keep only strips relevant to the query) as a separate prompted step.
"""
from __future__ import annotations

import logging
from collections.abc import Callable, Sequence
from enum import Enum
from typing import Any

from citecheck.agent.citation_resolver import CitationResolver
from citecheck.agent.loop import AnswerWithCitations

logger = logging.getLogger(__name__)

Generator = Callable[[str], str]
WebSearch = Callable[[str], Sequence[str]]


class CRAGVerdict(str, Enum):
    """Output of the retrieval evaluator on a single (query, doc) pair."""

    CORRECT = "correct"
    INCORRECT = "incorrect"
    AMBIGUOUS = "ambiguous"


_EVAL_PROMPT = """You are a retrieval quality grader. Decide whether the \
passage answers the query.

Reply with EXACTLY one word: "Correct" if the passage clearly contains the \
answer; "Incorrect" if it does not; "Ambiguous" if it is partially relevant \
but missing key information.

Query: {query}
Passage: {passage}
Verdict:"""

_REFINE_PROMPT = """Extract only the sentences from the passage that \
directly answer the query. Drop everything else. Output the kept sentences \
verbatim, one per line.

Query: {query}
Passage: {passage}
Kept sentences:"""

_GEN_SYSTEM = """You are a legal research assistant. Answer the question \
using only the provided refined evidence. Every legal claim must be followed \
by a Bluebook citation: "<Case Name>, <vol> <Reporter> <page> (<court> \
<year>)". If the evidence is insufficient, say so explicitly."""


class CRAGBaseline:
    """Corrective RAG (Yan et al. 2024) baseline.

    Args:
        generator: ``(prompt: str) -> str`` callable used for *both* the final
            answer and (by default) the retrieval evaluator. Pass a separate
            ``judge_generator`` if you want to use a cheaper model for grading.
        retriever: First-stage retriever.
        resolver: Citation verifier for post-hoc grading.
        judge_generator: Optional separate callable for the evaluator. Defaults
            to ``generator``.
        web_search: Optional fallback callable ``(query) -> Sequence[str]``.
            If ``None`` (the default — see module docstring), the ``Incorrect``
            branch is replaced with an abstain-and-warn pattern.
        top_k: First-stage retrieval depth.
        refine: If True (default), run the per-doc knowledge-refinement pass.
    """

    def __init__(
        self,
        generator: Generator,
        retriever: Any,
        resolver: CitationResolver,
        judge_generator: Generator | None = None,
        web_search: WebSearch | None = None,
        top_k: int = 10,
        refine: bool = True,
    ) -> None:
        self.generator = generator
        self.retriever = retriever
        self.resolver = resolver
        self.judge_generator = judge_generator or generator
        self.web_search = web_search
        self.top_k = top_k
        self.refine = refine
        if web_search is None:
            logger.info(
                "CRAGBaseline running with NO web-search fallback (CiteCheck "
                "default). 'Incorrect' branch will abstain instead."
            )

    # ----------------------------------------------------------------- public
    def answer(self, question: str) -> AnswerWithCitations:
        """Run CRAG: retrieve → evaluate → refine/route → generate."""
        try:
            candidates = self.retriever.search(question, top_k=self.top_k)
        except TypeError:
            candidates = self.retriever.search(question)

        verdicts = [self._evaluate(question, p) for p in candidates]
        evidence_blocks: list[str] = []
        used_docs: list[str] = []

        corrects = [
            (p, v) for p, v in zip(candidates, verdicts, strict=True)
            if v is CRAGVerdict.CORRECT
        ]
        ambiguous = [
            (p, v) for p, v in zip(candidates, verdicts, strict=True)
            if v is CRAGVerdict.AMBIGUOUS
        ]

        # Route 1: at least one Correct doc → use only those (with optional refine).
        if corrects:
            for p, _ in corrects:
                text = self._passage_text(p)
                refined = self._refine(question, text) if self.refine else text
                evidence_blocks.append(refined)
                used_docs.append(_doc_id(p))
        elif ambiguous:
            # Route 2: only Ambiguous → use them + (optionally) web search.
            for p, _ in ambiguous:
                text = self._passage_text(p)
                refined = self._refine(question, text) if self.refine else text
                evidence_blocks.append(refined)
                used_docs.append(_doc_id(p))
            if self.web_search is not None:
                evidence_blocks.extend(self.web_search(question))
        # Route 3: everything Incorrect → fall back (web search or abstain).
        elif self.web_search is not None:
            evidence_blocks.extend(self.web_search(question))
        else:
            # CiteCheck default: refuse to fabricate.
            text = (
                "I cannot answer with sufficient confidence: no retrieved "
                "passage was judged a correct match for this question, and no "
                "web-search fallback is configured."
            )
            return AnswerWithCitations(
                text=text, citations=[], iterations_used=1, retrieved_doc_ids=used_docs,
            )

        prompt = self._build_prompt(question, evidence_blocks)
        out = self.generator(prompt)

        parsed = self.resolver.parse_bluebook(out)
        cites = []
        seen: set[str] = set()
        for pc in parsed:
            cite_str = pc.raw_text.strip()
            if cite_str in seen:
                continue
            seen.add(cite_str)
            cites.append((cite_str, self.resolver.verify(cite_str, asserted_claim=out)))

        return AnswerWithCitations(
            text=out, citations=cites, iterations_used=1, retrieved_doc_ids=used_docs,
        )

    # ---------------------------------------------------------------- helpers
    def _evaluate(self, query: str, passage: Any) -> CRAGVerdict:
        """Prompted-LLM retrieval evaluator (one of three verdicts)."""
        text = self._passage_text(passage)
        prompt = _EVAL_PROMPT.format(query=query, passage=text[:1200])
        out = self.judge_generator(prompt).strip().lower()
        if out.startswith("correct"):
            return CRAGVerdict.CORRECT
        if out.startswith("incorrect"):
            return CRAGVerdict.INCORRECT
        if out.startswith("ambiguous"):
            return CRAGVerdict.AMBIGUOUS
        logger.warning("CRAG evaluator returned unparseable verdict %r; treating as Ambiguous", out)
        return CRAGVerdict.AMBIGUOUS

    def _refine(self, query: str, passage_text: str) -> str:
        """Drop irrelevant sentences via prompted strip selection."""
        if not passage_text.strip():
            return passage_text
        prompt = _REFINE_PROMPT.format(query=query, passage=passage_text[:2000])
        out = self.generator(prompt).strip()
        # Guard against the model erroneously emitting nothing or just refusing.
        if not out or out.lower().startswith("none"):
            return passage_text
        return out

    @staticmethod
    def _passage_text(p: Any) -> str:
        return getattr(p, "text", None) or getattr(p, "passage", "") or ""

    @staticmethod
    def _build_prompt(question: str, evidence_blocks: list[str]) -> str:
        blocks = [f"[{i}] {b}" for i, b in enumerate(evidence_blocks, 1)]
        context = "\n\n".join(blocks) if blocks else "(no refined evidence)"
        return (
            f"{_GEN_SYSTEM}\n\n### Refined evidence\n{context}\n\n"
            f"### Question\n{question}\n\n### Answer\n"
        )


def _doc_id(p: Any) -> str:
    for attr in ("doc_id", "id", "passage_id"):
        v = getattr(p, attr, None)
        if v is not None:
            return str(v)
    return "unknown"
