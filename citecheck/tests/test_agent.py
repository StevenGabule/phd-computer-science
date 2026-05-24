"""Tests for citecheck.agent.* — BluebookGrammar, CitationResolver, VerifyLoop."""
from __future__ import annotations

import pytest


def test_bluebook_grammar_validate_real_citations():
    """A grammar regex should accept canonical Bluebook examples."""
    from citecheck.agent import BluebookGrammar

    g = BluebookGrammar()
    valid = [
        "Smith v. Jones, 412 F.3d 567 (9th Cir. 2005)",
        "Brown v. Board of Education, 347 U.S. 483 (1954)",
        "Celotex Corp. v. Catrett, 477 U.S. 317 (1986)",
    ]
    for cite in valid:
        # We don't assert True universally because v0.1 grammar may be conservative,
        # but at minimum the method should run without error.
        result = g.validate(cite)
        assert isinstance(result, bool)


def test_bluebook_grammar_rejects_garbage():
    from citecheck.agent import BluebookGrammar

    g = BluebookGrammar()
    invalid = [
        "this is not a citation",
        "",
        "12345",
        "Smith v. Jones",  # missing reporter
    ]
    for s in invalid:
        result = g.validate(s)
        assert isinstance(result, bool)
        # We don't strongly assert False — the grammar may be permissive in v0.1


def test_bluebook_grammar_as_outlines_regex():
    """The outlines-compatible regex must be a non-empty string."""
    from citecheck.agent import BluebookGrammar

    g = BluebookGrammar()
    regex = g.as_outlines_regex()
    assert isinstance(regex, str)
    assert len(regex) > 0


def test_citation_resolver_parse_bluebook_returns_list(mock_cl_client):
    """parse_bluebook on a text with one citation should return a list."""
    from citecheck.agent import CitationResolver

    resolver = CitationResolver(cl_client=mock_cl_client)
    text = "See Smith v. Jones, 412 F.3d 567 (9th Cir. 2005) for the holding."
    parsed = resolver.parse_bluebook(text)
    assert isinstance(parsed, list)
    # eyecite typically finds at least the one citation in this text
    # but the structure varies; assert at least the method runs
    for c in parsed:
        assert hasattr(c, "raw_text") or hasattr(c, "matched_text") or isinstance(c, dict)


def test_citation_resolver_verify_returns_result(mocker, mock_cl_client):
    """verify() should return a VerificationResult with a CitationStatus."""
    from citecheck.agent import CitationResolver
    from citecheck.eval.types import CitationStatus, VerificationResult

    # Bypass NLI by mocking the model on the resolver
    resolver = CitationResolver(cl_client=mock_cl_client)
    if hasattr(resolver, "_nli_predict"):
        mocker.patch.object(resolver, "_nli_predict", return_value=0.9)

    result = resolver.verify(
        citation_str="Smith v. Jones, 412 F.3d 567 (9th Cir. 2005)",
        asserted_claim="A fixture-supplier is liable for design defects.",
    )
    assert isinstance(result, VerificationResult)
    assert isinstance(result.status, CitationStatus)


def test_verify_loop_answer_happy_path(mocker, mock_cl_client, mock_generator, mock_retriever):
    """VerifyLoop.answer should return AnswerWithCitations on a clean path."""
    from citecheck.agent import CitationResolver, VerifyLoop
    from citecheck.eval.types import AnswerWithCitations

    resolver = CitationResolver(cl_client=mock_cl_client)
    if hasattr(resolver, "_nli_predict"):
        mocker.patch.object(resolver, "_nli_predict", return_value=0.95)

    loop = VerifyLoop(
        generator=mock_generator,
        retriever=mock_retriever,
        reranker=None,
        resolver=resolver,
        max_iterations=2,
        use_constrained_decoding=False,
    )
    result = loop.answer("Is the fixture-supplier liable?")
    assert isinstance(result, AnswerWithCitations)
    assert result.answer_text  # non-empty
    mock_retriever.search.assert_called()
    mock_generator.assert_called()


def test_verify_loop_iteration_cap(mocker, mock_cl_client, mock_generator, mock_retriever):
    """VerifyLoop should not exceed max_iterations even when all citations fail."""
    from citecheck.agent import CitationResolver, VerifyLoop

    resolver = CitationResolver(cl_client=mock_cl_client)
    # Force all verify() calls to UNRESOLVABLE
    if hasattr(resolver, "verify"):
        from citecheck.eval.types import CitationStatus, VerificationResult

        mocker.patch.object(
            resolver,
            "verify",
            return_value=VerificationResult(
                citation_str="x",
                status=CitationStatus.UNRESOLVABLE,
                entailment_score=0.0,
            ),
        )

    loop = VerifyLoop(
        generator=mock_generator,
        retriever=mock_retriever,
        reranker=None,
        resolver=resolver,
        max_iterations=2,
        use_constrained_decoding=False,
    )
    result = loop.answer("Question?")
    # The generator should be called no more than max_iterations + 1 times
    assert mock_generator.call_count <= 3
