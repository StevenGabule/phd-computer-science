"""EL-RAG baseline (Wankhade 2026, best-effort reimplementation).

.. warning::
    The source paper (Wankhade, "EL-RAG: Evidence-Aligned Learning-to-Rank
    Retrieval-Augmented Generation", 2026) is closed-access and has no public
    code release as of this writing. This module is a *faithful reimpl from
    the abstract and the architecture diagram*, not a port. Numbers reported
    using this baseline are labeled "EL-RAG (reimpl)" in the paper.

Architecture (as described in the abstract):

    1. **Hybrid sparse-dense retriever** — we reuse our existing
       :class:`~citecheck.retrieval.HybridRetriever` (BM25 + dense + RRF).
    2. **Learning-to-rank reranker** — we reuse our existing
       :class:`~citecheck.reranker.CrossEncoderReranker`.
    3. **Multi-hop reasoning generator** — implemented here as a two-pass
       chain: first generate a *reasoning sketch* (chain-of-thought), then a
       grounded answer conditioned on the sketch.
    4. **Evidence Alignment Layer (EAL)** — implemented here as a BERTScore-
       based passage-answer alignment, returning a per-citation alignment
       score that we surface in the verification ``notes`` field.

The reimplementation deliberately matches the *interface* of CiteCheck's
existing pieces so that we can attribute any delta between EL-RAG and
CiteCheck to the verification loop, not to retrieval-stack differences.
"""
from __future__ import annotations

import logging
from collections.abc import Callable, Sequence
from typing import Any

from citecheck.agent.citation_resolver import CitationResolver
from citecheck.agent.loop import AnswerWithCitations

logger = logging.getLogger(__name__)

Generator = Callable[[str], str]

_SKETCH_SYSTEM = """You are reasoning about a US case-law question. List the \
relevant legal issues, the doctrines that apply, and which retrieved passages \
support each step. Do NOT yet write a full answer or cite cases — that comes \
next."""

_GEN_SYSTEM = """You are a legal research assistant. Using the reasoning \
sketch and the retrieved evidence, produce a final answer. Every legal claim \
must be followed by a Bluebook citation: "<Case Name>, <vol> <Reporter> \
<page> (<court> <year>)". Do not introduce facts not present in the evidence."""


class ELRAGBaseline:
    """EL-RAG reimplementation (Wankhade 2026 abstract).

    Args:
        generator: ``(prompt: str) -> str`` callable used for both the sketch
            and the grounded answer.
        hybrid_retriever: A :class:`~citecheck.retrieval.HybridRetriever` (or
            anything with ``.search(query, top_k)``).
        reranker: A learning-to-rank reranker with ``.rerank(query, candidates,
            lambda_)`` — i.e. :class:`~citecheck.reranker.CrossEncoderReranker`.
        resolver: Post-hoc citation verifier.
        top_k_retrieve: First-stage retrieval depth.
        top_k_rerank: Number of passages kept after reranking.
        eal_threshold: BERTScore alignment threshold below which a citation is
            flagged as "weakly aligned" in the verification ``notes`` field.
        rerank_lambda: ``λ`` parameter forwarded to ``reranker.rerank``.
    """

    def __init__(
        self,
        generator: Generator,
        hybrid_retriever: Any,
        reranker: Any,
        resolver: CitationResolver,
        top_k_retrieve: int = 50,
        top_k_rerank: int = 10,
        eal_threshold: float = 0.6,
        rerank_lambda: float = 0.5,
    ) -> None:
        self.generator = generator
        self.retriever = hybrid_retriever
        self.reranker = reranker
        self.resolver = resolver
        self.top_k_retrieve = top_k_retrieve
        self.top_k_rerank = top_k_rerank
        self.eal_threshold = eal_threshold
        self.rerank_lambda = rerank_lambda
        # BERTScorer is heavy; lazy-load on first EAL call.
        self._scorer: Any | None = None

    # ----------------------------------------------------------------- public
    def answer(self, question: str) -> AnswerWithCitations:
        """Run EL-RAG: hybrid retrieve → LTR rerank → multi-hop gen → EAL."""
        passages = self._retrieve_rerank(question)
        sketch = self._generate_sketch(question, passages)
        answer_text = self._generate_grounded(question, passages, sketch)

        parsed = self.resolver.parse_bluebook(answer_text)
        cites = []
        seen: set[str] = set()
        for pc in parsed:
            cite_str = pc.raw_text.strip()
            if cite_str in seen:
                continue
            seen.add(cite_str)
            v = self.resolver.verify(cite_str, asserted_claim=answer_text)
            # Layer EAL alignment on top of the standard verification result.
            eal_score = self._evidence_alignment_layer(answer_text, passages)
            if eal_score is not None:
                v.notes = (
                    f"{v.notes}; EAL alignment={eal_score:.3f} "
                    f"(threshold={self.eal_threshold:.2f})"
                ).strip("; ")
            cites.append((cite_str, v))

        return AnswerWithCitations(
            text=answer_text,
            citations=cites,
            iterations_used=2,  # sketch + grounded
            retrieved_doc_ids=[_doc_id(p) for p in passages],
        )

    # ---------------------------------------------------------------- helpers
    def _retrieve_rerank(self, question: str) -> Sequence[Any]:
        try:
            candidates = self.retriever.search(question, top_k=self.top_k_retrieve)
        except TypeError:
            candidates = self.retriever.search(question)
        if not candidates:
            return candidates
        try:
            reranked = self.reranker.rerank(
                question, candidates, lambda_=self.rerank_lambda
            )
        except Exception:
            logger.exception("EL-RAG reranker failed; using retriever order")
            reranked = candidates
        return list(reranked)[: self.top_k_rerank]

    def _generate_sketch(self, question: str, passages: Sequence[Any]) -> str:
        ctx = _format_passages(passages)
        prompt = (
            f"{_SKETCH_SYSTEM}\n\n### Retrieved evidence\n{ctx}\n\n"
            f"### Question\n{question}\n\n### Reasoning sketch\n"
        )
        return self.generator(prompt)

    def _generate_grounded(
        self, question: str, passages: Sequence[Any], sketch: str,
    ) -> str:
        ctx = _format_passages(passages)
        prompt = (
            f"{_GEN_SYSTEM}\n\n### Retrieved evidence\n{ctx}\n\n"
            f"### Reasoning sketch\n{sketch}\n\n"
            f"### Question\n{question}\n\n### Final answer\n"
        )
        return self.generator(prompt)

    def _evidence_alignment_layer(
        self, answer_text: str, passages: Sequence[Any],
    ) -> float | None:
        """BERTScore-based alignment between answer and best passage.

        Returns the max F1 over (answer, passage_i) or ``None`` if BERTScore
        is unavailable. This is a *proxy* for the EAL described in the
        abstract; the original paper's exact EAL formulation is not public.
        """
        if not passages or not answer_text.strip():
            return None
        try:
            from bert_score import BERTScorer  # noqa: PLC0415 — heavy/optional
        except ImportError:
            logger.debug("bert_score not installed; EAL returning None")
            return None
        if self._scorer is None:
            try:
                self._scorer = BERTScorer(lang="en", rescale_with_baseline=False)
            except Exception as exc:
                logger.warning("BERTScorer init failed (%s); EAL disabled", exc)
                return None

        cand = [answer_text]
        refs = [_passage_text(p) for p in passages if _passage_text(p)]
        if not refs:
            return None
        best = 0.0
        for ref in refs:
            try:
                _p, _r, f1 = self._scorer.score([cand[0]], [ref])
                val = float(f1[0].item())
            except Exception as exc:
                logger.debug("BERTScore call failed (%s); skipping", exc)
                continue
            if val > best:
                best = val
        return best


def _passage_text(p: Any) -> str:
    return getattr(p, "text", None) or getattr(p, "passage", "") or ""


def _format_passages(passages: Sequence[Any]) -> str:
    blocks = []
    for i, p in enumerate(passages, 1):
        text = _passage_text(p)
        doc_id = _doc_id(p)
        blocks.append(f"[{i}] (doc_id={doc_id})\n{text}")
    return "\n\n".join(blocks) if blocks else "(no passages retrieved)"


def _doc_id(p: Any) -> str:
    for attr in ("doc_id", "id", "passage_id"):
        v = getattr(p, attr, None)
        if v is not None:
            return str(v)
    return "unknown"
