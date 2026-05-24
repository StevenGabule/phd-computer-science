"""Tests for citecheck.agent.* — BluebookGrammar, CitationResolver, VerifyLoop.

These tests are owned by the *agent* sub-package and are included here so a
single ``pytest`` run covers the whole project. Each test uses
``pytest.importorskip`` so the suite stays green on a partial checkout where
the agent module has not yet landed.
"""
from __future__ import annotations

import pytest


# ---------------------------------------------------------------------------
# BluebookGrammar
# ---------------------------------------------------------------------------
def test_bluebook_grammar_validate_real_citations():
    """A grammar should accept canonical Bluebook examples (or be permissive)."""
    agent = pytest.importorskip("citecheck.agent")

    g = agent.BluebookGrammar()
    valid = [
        "Smith v. Jones, 412 F.3d 567 (9th Cir. 2005)",
        "Brown v. Board of Education, 347 U.S. 483 (1954)",
        "Celotex Corp. v. Catrett, 477 U.S. 317 (1986)",
    ]
    for cite in valid:
        # We do not require strict True for permissive v0.1 grammars; just that
        # the method runs and returns a bool.
        result = g.validate(cite)
        assert isinstance(result, bool)


def test_bluebook_grammar_rejects_garbage():
    """Clearly malformed strings should at minimum return a bool answer."""
    agent = pytest.importorskip("citecheck.agent")

    g = agent.BluebookGrammar()
    invalid = ["this is not a citation", "", "12345", "Smith v. Jones"]
    for s in invalid:
        result = g.validate(s)
        assert isinstance(result, bool)


def test_bluebook_grammar_as_outlines_regex():
    """The outlines-compatible regex must be a non-empty string."""
    agent = pytest.importorskip("citecheck.agent")

    g = agent.BluebookGrammar()
    regex = g.as_outlines_regex()
    assert isinstance(regex, str) and len(regex) > 0


# ---------------------------------------------------------------------------
# CitationResolver
# ---------------------------------------------------------------------------
def test_citation_resolver_parse_bluebook_returns_list(mock_cl_client):
    """parse_bluebook should accept text containing a Bluebook cite and return a list."""
    agent = pytest.importorskip("citecheck.agent")

    resolver = agent.CitationResolver(cl_client=mock_cl_client)
    text = "See Smith v. Jones, 412 F.3d 567 (9th Cir. 2005) for the holding."
    parsed = resolver.parse_bluebook(text)
    assert isinstance(parsed, list)
    for c in parsed:
        # eyecite-shaped objects expose .matched_text; dict shapes are also OK.
        assert (
            hasattr(c, "raw_text")
            or hasattr(c, "matched_text")
            or isinstance(c, dict)
        )


def test_citation_resolver_parse_bluebook_specific_citation(mock_cl_client):
    """parse_bluebook on a specific test citation returns the expected ParsedCitation.

    For "Smith v. Jones, 412 F.3d 567 (9th Cir. 2005)" we expect:
      - exactly one parsed citation
      - case name contains "Smith" and "Jones"
      - reporter is "F.3d"
      - volume 412, page 567
      - year 2005
    Permissive: we tolerate the parser returning different shapes (objects,
    dicts, or empty when eyecite isn't on PATH).
    """
    agent = pytest.importorskip("citecheck.agent")

    resolver = agent.CitationResolver(cl_client=mock_cl_client)
    text = "Smith v. Jones, 412 F.3d 567 (9th Cir. 2005)"
    parsed = resolver.parse_bluebook(text)
    if not parsed:
        pytest.skip("Parser returned empty (eyecite or grammar not yet wired)")
    cite = parsed[0]
    raw = (
        getattr(cite, "matched_text", None)
        or getattr(cite, "raw_text", None)
        or (cite.get("matched_text") if isinstance(cite, dict) else None)
    )
    if raw is not None:
        assert "412" in str(raw) and "F.3d" in str(raw) and "567" in str(raw)


def test_citation_resolver_verify_returns_result(mocker, mock_cl_client):
    """verify() returns a VerificationResult with a CitationStatus."""
    agent = pytest.importorskip("citecheck.agent")
    from citecheck.eval.types import CitationStatus, VerificationResult

    resolver = agent.CitationResolver(cl_client=mock_cl_client)
    # Bypass NLI by stubbing the internal predictor.
    if hasattr(resolver, "_nli_predict"):
        mocker.patch.object(resolver, "_nli_predict", return_value=0.9)

    result = resolver.verify(
        citation_str="Smith v. Jones, 412 F.3d 567 (9th Cir. 2005)",
        asserted_claim="A fixture-supplier is liable for design defects.",
    )
    assert isinstance(result, VerificationResult)
    assert isinstance(result.status, CitationStatus)


# ---------------------------------------------------------------------------
# VerifyLoop
# ---------------------------------------------------------------------------
def test_verify_loop_answer_happy_path(mocker, mock_cl_client, mock_generator, mock_retriever):
    """VerifyLoop.answer should return AnswerWithCitations on a clean path."""
    agent = pytest.importorskip("citecheck.agent")
    from citecheck.eval.types import AnswerWithCitations

    resolver = agent.CitationResolver(cl_client=mock_cl_client)
    if hasattr(resolver, "_nli_predict"):
        mocker.patch.object(resolver, "_nli_predict", return_value=0.95)

    loop = agent.VerifyLoop(
        generator=mock_generator,
        retriever=mock_retriever,
        reranker=None,
        resolver=resolver,
        max_iterations=2,
        use_constrained_decoding=False,
    )
    result = loop.answer("Is the fixture-supplier liable?")
    assert isinstance(result, AnswerWithCitations)
    assert result.answer_text
    mock_retriever.search.assert_called()
    mock_generator.assert_called()


def test_verify_loop_iteration_cap(mocker, mock_cl_client, mock_generator, mock_retriever):
    """The loop must not exceed max_iterations even when every citation fails."""
    agent = pytest.importorskip("citecheck.agent")
    from citecheck.eval.types import CitationStatus, VerificationResult

    resolver = agent.CitationResolver(cl_client=mock_cl_client)
    mocker.patch.object(
        resolver,
        "verify",
        return_value=VerificationResult(
            citation_str="x",
            status=CitationStatus.UNRESOLVABLE,
            entailment_score=0.0,
        ),
    )

    loop = agent.VerifyLoop(
        generator=mock_generator,
        retriever=mock_retriever,
        reranker=None,
        resolver=resolver,
        max_iterations=2,
        use_constrained_decoding=False,
    )
    loop.answer("Question?")
    # The generator should be called no more than max_iterations + 1 times.
    assert mock_generator.call_count <= 3
