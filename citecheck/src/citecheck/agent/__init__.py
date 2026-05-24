"""CiteCheck agent layer.

Implements the verify-then-emit loop that distinguishes CiteCheck from naive
RAG: every citation produced by the generator is parsed (eyecite), resolved
against CourtListener, and judged for entailment against the cited opinion
before being returned to the caller.

Public surface:
    :class:`CitationResolver` — eyecite parse + CL resolve + NLI judge.
    :class:`BluebookGrammar` — regex/grammar for constrained decoding.
    :class:`VerifyLoop` — full pipeline orchestrator (retrieve→rerank→generate→verify).
    :class:`VerificationResult` — per-citation verdict dataclass.
    :class:`CitationStatus` — enum of verdicts.
    :class:`AnswerWithCitations` — top-level answer object.

Typical usage::

    from citecheck.agent import VerifyLoop, CitationResolver
    from citecheck.data import CourtListenerClient
    from citecheck.retrieval import HybridRetriever

    cl = CourtListenerClient()
    resolver = CitationResolver(cl_client=cl)
    loop = VerifyLoop(generator=my_llm, retriever=HybridRetriever(),
                       reranker=None, resolver=resolver)
    answer = loop.answer("What case established Miranda warnings?")
"""
from __future__ import annotations

from citecheck.agent.citation_resolver import (
    CitationResolver,
    CitationStatus,
    ParsedCitation,
    VerificationResult,
)
from citecheck.agent.grammar import BluebookGrammar
from citecheck.agent.loop import AnswerWithCitations, VerifyLoop

__all__ = [
    "AnswerWithCitations",
    "BluebookGrammar",
    "CitationResolver",
    "CitationStatus",
    "ParsedCitation",
    "VerificationResult",
    "VerifyLoop",
]
