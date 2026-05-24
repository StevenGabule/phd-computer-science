"""Naive retrieval-augmented baseline.

Standard "retrieve top-k, stuff into a prompt, generate once" RAG. No
reranker, no constrained decoding, no verification loop. This isolates the
contribution of *just* having retrieved evidence vs. parametric memory
(:class:`~citecheck.baselines.vanilla.VanillaBaseline`).
"""
from __future__ import annotations

import logging
from collections.abc import Callable, Sequence
from typing import Any

from citecheck.agent.citation_resolver import CitationResolver
from citecheck.agent.loop import AnswerWithCitations

logger = logging.getLogger(__name__)

Generator = Callable[[str], str]

_NAIVE_SYSTEM = """You are a legal research assistant. Answer the user's \
question using only the provided case-law excerpts. Every legal claim must be \
followed by a Bluebook citation: "<Case Name>, <vol> <Reporter> <page> \
(<court> <year>)". If the excerpts do not support an answer, say so and cite \
no cases."""


class NaiveRAGBaseline:
    """Retrieve → stuff → generate, then verify citations post-hoc.

    Args:
        generator: ``(prompt: str) -> str`` callable.
        retriever: Object with ``.search(query, top_k)`` returning passages.
        resolver: :class:`CitationResolver` used post-hoc to populate the
            ``citations`` field. The generator never sees verification output;
            that's what makes this "naive".
        top_k: Number of passages to retrieve and stuff into the prompt.
    """

    def __init__(
        self,
        generator: Generator,
        retriever: Any,
        resolver: CitationResolver,
        top_k: int = 10,
    ) -> None:
        self.generator = generator
        self.retriever = retriever
        self.resolver = resolver
        self.top_k = top_k

    def answer(self, question: str) -> AnswerWithCitations:
        """Run one retrieve-stuff-generate pass."""
        passages = self._retrieve(question)
        prompt = self._build_prompt(question, passages)
        logger.debug("NaiveRAGBaseline: prompting (%d chars)", len(prompt))
        text = self.generator(prompt)

        parsed = self.resolver.parse_bluebook(text)
        cites = []
        seen: set[str] = set()
        for pc in parsed:
            cite_str = pc.raw_text.strip()
            if cite_str in seen:
                continue
            seen.add(cite_str)
            cites.append((cite_str, self.resolver.verify(cite_str, asserted_claim=text)))

        return AnswerWithCitations(
            text=text,
            citations=cites,
            iterations_used=1,
            retrieved_doc_ids=[_doc_id(p) for p in passages],
        )

    # ---------------------------------------------------------------- helpers
    def _retrieve(self, question: str) -> Sequence[Any]:
        try:
            return self.retriever.search(question, top_k=self.top_k)
        except TypeError:
            return self.retriever.search(question)

    @staticmethod
    def _build_prompt(question: str, passages: Sequence[Any]) -> str:
        blocks = []
        for i, p in enumerate(passages, 1):
            text = getattr(p, "text", None) or getattr(p, "passage", "") or ""
            doc_id = _doc_id(p)
            blocks.append(f"[{i}] (doc_id={doc_id})\n{text}")
        context = "\n\n".join(blocks) if blocks else "(no passages retrieved)"
        return (
            f"{_NAIVE_SYSTEM}\n\n### Context\n{context}\n\n"
            f"### Question\n{question}\n\n### Answer\n"
        )


def _doc_id(p: Any) -> str:
    for attr in ("doc_id", "id", "passage_id"):
        v = getattr(p, attr, None)
        if v is not None:
            return str(v)
    return "unknown"
