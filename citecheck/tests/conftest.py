"""Shared pytest fixtures for the CiteCheck test suite.

All fixtures here mock external dependencies (CourtListener API, real
filesystem corpora, GPU models). Tests that need real network / GPU / large
data should be marked ``@pytest.mark.slow``, ``@pytest.mark.gpu``, or
``@pytest.mark.network`` and are excluded by default via ``make test``.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pytest

from citecheck.eval.types import (
    AnswerWithCitations,
    CitationStatus,
    CiteCheckExample,
    VerificationResult,
)

# Canonical test citation referenced across multiple fixtures.
_TEST_CITE = "Smith v. Jones, 412 F.3d 567 (9th Cir. 2005)"


@dataclass(slots=True)
class FakeCLOpinion:
    """Minimal fake of citecheck.data.cl_client.CLOpinion."""

    id: int
    case_name: str
    court: str
    court_jurisdiction: str
    year: int
    citation_strings: list[str]
    body_text: str
    url: str


@pytest.fixture
def sample_eval_examples() -> list[CiteCheckExample]:
    """Three hand-crafted CiteCheckExample instances spanning common cases."""
    return [
        CiteCheckExample(
            id="ex001",
            question="Is a fixture-supplier liable for design defects under NY law?",
            gold_citations=[_TEST_CITE],
            jurisdiction="ny",
            source="manual",
            metadata={"gold_support_labels": {_TEST_CITE: True}},
        ),
        CiteCheckExample(
            id="ex002",
            question="Does a non-compete survive termination under Delaware law?",
            gold_citations=[
                "Ashland Mgmt., Inc. v. Janien, 82 N.Y.2d 395 (1993)",
                "Smith v. Jones, 412 F.3d 567 (9th Cir. 2005)",
            ],
            jurisdiction="delaware",
            source="charlotin",
            metadata={},
        ),
        CiteCheckExample(
            id="ex003",
            question="What is the standard for summary judgment in federal court?",
            gold_citations=["Celotex Corp. v. Catrett, 477 U.S. 317 (1986)"],
            jurisdiction="federal",
            source="legalbench_rag",
            metadata={},
        ),
    ]


@pytest.fixture
def sample_cl_opinion() -> FakeCLOpinion:
    return FakeCLOpinion(
        id=1234567,
        case_name="Smith v. Jones",
        court="ca9",
        court_jurisdiction="F",
        year=2005,
        citation_strings=["412 F.3d 567"],
        body_text="A fixture-supplier is liable when the design defect was foreseeable.",
        url="https://www.courtlistener.com/opinion/1234567/smith-v-jones/",
    )


@pytest.fixture
def mock_cl_client(mocker, sample_cl_opinion):
    """A pytest-mock'd CourtListenerClient.

    ``resolve_citation`` returns the sample CLOpinion for the canonical test
    citation, ``None`` for anything else.
    """
    client = mocker.MagicMock(name="CourtListenerClient")

    def _resolve(citation_str: str):
        if "412 F.3d 567" in citation_str or "Smith v. Jones" in citation_str:
            return sample_cl_opinion
        return None

    client.resolve_citation.side_effect = _resolve
    client.get_opinion.return_value = sample_cl_opinion
    return client


@pytest.fixture
def tmp_data_dir(tmp_path: Path) -> Path:
    """Empty temp directory with the standard CiteCheck subdir layout."""
    for sub in ("cap_raw", "cap_parquet", "cl_cache", "indexes/bm25", "indexes/dense"):
        (tmp_path / sub).mkdir(parents=True, exist_ok=True)
    return tmp_path


@pytest.fixture
def sample_answer_verified(sample_cl_opinion) -> AnswerWithCitations:
    """An AnswerWithCitations where the single citation is VERIFIED."""
    return AnswerWithCitations(
        question_id="ex001",
        answer_text=f"Yes, the fixture-supplier is liable. See {_TEST_CITE}.",
        citations=[_TEST_CITE],
        verification_results=[
            VerificationResult(
                citation_str=_TEST_CITE,
                status=CitationStatus.VERIFIED,
                entailment_score=0.92,
                resolved_opinion_id=sample_cl_opinion.id,
                resolved_court_jurisdiction=sample_cl_opinion.court_jurisdiction,
                reasoning="opinion body entails the asserted claim",
            ),
        ],
        latency_ms=1234.5,
        tokens_used=512,
    )


@pytest.fixture
def sample_answer_fabricated() -> AnswerWithCitations:
    """An AnswerWithCitations where the single citation is UNRESOLVABLE."""
    return AnswerWithCitations(
        question_id="ex002",
        answer_text="See Doe v. Roe, 999 F.4th 1 (12th Cir. 9999).",
        citations=["Doe v. Roe, 999 F.4th 1 (12th Cir. 9999)"],
        verification_results=[
            VerificationResult(
                citation_str="Doe v. Roe, 999 F.4th 1 (12th Cir. 9999)",
                status=CitationStatus.UNRESOLVABLE,
                entailment_score=0.0,
            ),
        ],
        latency_ms=842.1,
        tokens_used=384,
    )


@pytest.fixture
def mock_generator(mocker):
    """A mock LLM callable: (prompt: str) -> str. Returns a canned response."""
    gen = mocker.MagicMock(name="generator")
    gen.return_value = (
        "Yes. The fixture-supplier is liable for design defects. "
        "See Smith v. Jones, 412 F.3d 567 (9th Cir. 2005)."
    )
    return gen


@pytest.fixture
def mock_retriever(mocker):
    """A mock retriever exposing ``.search(query, top_k)`` returning RetrievalResults."""
    from citecheck.retrieval import RetrievalResult

    retriever = mocker.MagicMock(name="HybridRetriever")
    retriever.search.return_value = [
        RetrievalResult(
            doc_id="cap_001",
            score=0.85,
            rank=1,
            passage="A fixture-supplier is liable when the design defect was foreseeable.",
            metadata={"case_name": "Smith v. Jones"},
        ),
        RetrievalResult(
            doc_id="cap_002",
            score=0.72,
            rank=2,
            passage="Strict liability does not apply to component suppliers in California.",
            metadata={"case_name": "Doe v. Roe"},
        ),
    ]
    return retriever
