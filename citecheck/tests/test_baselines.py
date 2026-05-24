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
# VanillaBaseline
# ---------------------------------------------------------------------------
def test_vanilla_baseline_answer(mock_generator):
    """VanillaBaseline.answer returns AnswerWithCitations with no retrieved context."""
    vanilla = pytest.importorskip("citecheck.baselines.vanilla")
    from citecheck.eval.types import AnswerWithCitations

    baseline = vanilla.VanillaBaseline(generator=mock_generator)
    result = baseline.answer("Test question?")
    assert isinstance(result, AnswerWithCitations)
    mock_generator.assert_called_once()
    # No retrieval means no retrieved-doc identifiers in metadata.
    retrieved = (result.metadata or {}).get("retrieved_doc_ids", [])
    assert retrieved == [] or retrieved is None


# ---------------------------------------------------------------------------
# NaiveRAGBaseline
# ---------------------------------------------------------------------------
def test_naive_rag_baseline_uses_retriever(mock_generator, mock_retriever):
    """NaiveRAGBaseline.answer calls retriever and feeds context into the prompt."""
    naive_rag = pytest.importorskip("citecheck.baselines.naive_rag")
    from citecheck.eval.types import AnswerWithCitations

    baseline = naive_rag.NaiveRAGBaseline(
        generator=mock_generator,
        retriever=mock_retriever,
    )
    result = baseline.answer("Test question?")
    assert isinstance(result, AnswerWithCitations)
    mock_retriever.search.assert_called()
    mock_generator.assert_called()
    # The generator must have been called with a prompt that includes
    # at least one retrieved passage substring.
    call_args = mock_generator.call_args
    if call_args is not None:
        prompt = (
            call_args.args[0]
            if call_args.args
            else call_args.kwargs.get("prompt", "")
        )
        if isinstance(prompt, str) and prompt:
            # mock_retriever returns passages containing "fixture-supplier" or
            # "Strict liability"; one of them should appear in the prompt.
            assert (
                "fixture-supplier" in prompt
                or "Strict liability" in prompt
                or "Smith v. Jones" in prompt
                or "Doe v. Roe" in prompt
            )
