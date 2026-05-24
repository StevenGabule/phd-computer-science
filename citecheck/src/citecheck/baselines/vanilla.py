"""Vanilla parametric-only baseline.

Hits the LLM with the question and a strict citation-format instruction, with
*no* retrieval. This is the "how much does the model know on its own, and how
often does it hallucinate citations?" floor. Any RAG variant that does not
beat this on Citation Support F1 has not earned its complexity.
"""
from __future__ import annotations

import logging
from collections.abc import Callable

from citecheck.agent.citation_resolver import CitationResolver
from citecheck.agent.loop import AnswerWithCitations

logger = logging.getLogger(__name__)

Generator = Callable[[str], str]

_VANILLA_SYSTEM = """You are a legal research assistant. Answer the user's \
question using your own knowledge of US case law. Every legal claim must be \
followed by a Bluebook citation: "<Case Name>, <vol> <Reporter> <page> \
(<court> <year>)". If you are not confident a citation exists, say "I do not \
have a verified citation" and do not invent one."""


class VanillaBaseline:
    """Parametric-knowledge-only baseline (no retrieval, no verification).

    Args:
        generator: ``(prompt: str) -> str`` callable.
        resolver: A :class:`CitationResolver` used *only* to populate the
            ``citations`` field of the returned :class:`AnswerWithCitations`
            so the eval harness can score the same way it does for RAG systems.
            The generator itself sees no resolver feedback.
    """

    def __init__(self, generator: Generator, resolver: CitationResolver) -> None:
        self.generator = generator
        self.resolver = resolver

    def answer(self, question: str) -> AnswerWithCitations:
        """Generate a one-shot answer and post-hoc verify any citations."""
        prompt = f"{_VANILLA_SYSTEM}\n\n### Question\n{question}\n\n### Answer\n"
        logger.debug("VanillaBaseline: prompting (%d chars)", len(prompt))
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
            retrieved_doc_ids=[],
        )
