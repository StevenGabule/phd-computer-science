"""Tests for citecheck.baselines.* — protocol + the five baseline implementations.

These tests are owned by the *baselines* sub-package and are included here so
``pytest`` covers the whole project. Each test ``pytest.importorskip``-s the
relevant module so the suite stays green on a partial checkout.
"""
from __future__ import annotations

import importlib

import pytest


# ---------------------------------------------------------------------------
# BaselineProtocol
# ---------------------------------------------------------------------------
def test_baseline_protocol_is_runtime_checkable():
    """Any object with ``answer(self, question)`` should satisfy the protocol."""
    # Prefer the canonical home in citecheck.baselines, but fall back to the
    # eval-layer re-export (which mirrors the same Protocol).
    try:
        from citecheck.baselines import BaselineProtocol
    except (ImportError, ModuleNotFoundError):
        from citecheck.eval.types import BaselineProtocol  # type: ignore[assignment]

    class DummyBaseline:
        def answer(self, question: str):  # noqa: ARG002
            return None

    assert isinstance(DummyBaseline(), BaselineProtocol)


# ---------------------------------------------------------------------------
# Class-level imports
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    "import_path,class_name",
    [
        ("citecheck.baselines.vanilla", "VanillaBaseline"),
        ("citecheck.baselines.naive_rag", "NaiveRAGBaseline"),
        ("citecheck.baselines.self_rag", "SelfRAGBaseline"),
        ("citecheck.baselines.crag", "CRAGBaseline"),
        ("citecheck.baselines.el_rag", "ELRAGBaseline"),
    ],
)
def test_baseline_class_importable(import_path: str, class_name: str):
    """Each baseline class should be importable from its module."""
    mod = pytest.importorskip(import_path)
    assert hasattr(mod, class_name), f"{import_path} missing {class_name}"
    cls = getattr(mod, class_name)
    assert callable(cls)


def test_all_baselines_satisfy_protocol():
    """Each baseline must expose ``answer(question)``."""
    for mod_name, cls_name in [
        ("citecheck.baselines.vanilla", "VanillaBaseline"),
        ("citecheck.baselines.naive_rag", "NaiveRAGBaseline"),
        ("citecheck.baselines.self_rag", "SelfRAGBaseline"),
        ("citecheck.baselines.crag", "CRAGBaseline"),
        ("citecheck.baselines.el_rag", "ELRAGBaseline"),
    ]:
        try:
            mod = importlib.import_module(mod_name)
        except (ImportError, ModuleNotFoundError):
            pytest.skip(f"{mod_name} not implemented yet")
        cls = getattr(mod, cls_name)
        assert hasattr(cls, "answer"), f"{cls_name} is missing answer()"


# ---------------------------------------------------------------------------
# Shared resolver fixture
# ---------------------------------------------------------------------------
@pytest.fixture
def stub_resolver(mocker, mock_cl_client):
    """A CitationResolver with parse_bluebook + verify stubbed (no eyecite needed)."""
    pytest.importorskip("citecheck.agent")
    from citecheck.agent import CitationResolver
    from citecheck.eval.types import CitationStatus, VerificationResult

    resolver = mocker.MagicMock(spec=CitationResolver)
    resolver.parse_bluebook.return_value = []
    resolver.verify.return_value = VerificationResult(
        citation_str="",
        status=CitationStatus.VERIFIED,
        entailment_score=0.9,
    )
    return resolver


# ---------------------------------------------------------------------------
# VanillaBaseline
# ---------------------------------------------------------------------------
def test_vanilla_baseline_answer(mock_generator, stub_resolver):
    """VanillaBaseline.answer returns an answer object with no retrieval context."""
    vanilla = pytest.importorskip("citecheck.baselines.vanilla")

    baseline = vanilla.VanillaBaseline(generator=mock_generator, resolver=stub_resolver)
    result = baseline.answer("Test question?")
    # Vanilla baseline must call the generator exactly once and never retrieve.
    mock_generator.assert_called_once()
    # The returned object should at minimum carry the generated text.
    text = getattr(result, "text", None) or getattr(result, "answer_text", "")
    assert text  # non-empty


# ---------------------------------------------------------------------------
# NaiveRAGBaseline
# ---------------------------------------------------------------------------
def test_naive_rag_baseline_uses_retriever(mock_generator, mock_retriever, stub_resolver):
    """NaiveRAGBaseline.answer calls retriever and feeds context into the prompt."""
    naive_rag = pytest.importorskip("citecheck.baselines.naive_rag")

    baseline = naive_rag.NaiveRAGBaseline(
        generator=mock_generator,
        retriever=mock_retriever,
        resolver=stub_resolver,
    )
    baseline.answer("Test question?")
    mock_retriever.search.assert_called()
    mock_generator.assert_called()
    # The generator must have been called with a prompt that includes at
    # least one retrieved passage substring.
    call_args = mock_generator.call_args
    assert call_args is not None
    prompt = (
        call_args.args[0]
        if call_args.args
        else call_args.kwargs.get("prompt", "")
    )
    assert isinstance(prompt, str) and prompt
    # mock_retriever's canned passages mention "fixture-supplier" / "Strict liability".
    assert (
        "fixture-supplier" in prompt
        or "Strict liability" in prompt
        or "Smith v. Jones" in prompt
        or "Doe v. Roe" in prompt
    )
