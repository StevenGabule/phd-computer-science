"""Tests for citecheck.baselines.* — protocol + 5 baseline implementations."""
from __future__ import annotations

import pytest


def test_baseline_protocol_is_runtime_checkable():
    from citecheck.baselines import BaselineProtocol

    class DummyBaseline:
        def answer(self, question: str):
            return None

    assert isinstance(DummyBaseline(), BaselineProtocol)


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
def test_baseline_class_importable(import_path, class_name):
    """Each baseline class should be importable from its module."""
    import importlib

    mod = importlib.import_module(import_path)
    assert hasattr(mod, class_name)
    cls = getattr(mod, class_name)
    assert callable(cls)


def test_vanilla_baseline_answer(mock_generator):
    """VanillaBaseline.answer should return AnswerWithCitations with no retrieved context."""
    from citecheck.baselines import VanillaBaseline
    from citecheck.eval.types import AnswerWithCitations

    baseline = VanillaBaseline(generator=mock_generator)
    result = baseline.answer("Test question?")
    assert isinstance(result, AnswerWithCitations)
    mock_generator.assert_called_once()


def test_naive_rag_baseline_uses_retriever(mock_generator, mock_retriever):
    """NaiveRAGBaseline.answer should call the retriever and the generator."""
    from citecheck.baselines import NaiveRAGBaseline
    from citecheck.eval.types import AnswerWithCitations

    baseline = NaiveRAGBaseline(generator=mock_generator, retriever=mock_retriever)
    result = baseline.answer("Test question?")
    assert isinstance(result, AnswerWithCitations)
    mock_retriever.search.assert_called()
    mock_generator.assert_called()


def test_all_baselines_satisfy_protocol():
    """Spot-check that the 5 baseline classes have an answer() method."""
    import importlib

    for mod_name, cls_name in [
        ("citecheck.baselines.vanilla", "VanillaBaseline"),
        ("citecheck.baselines.naive_rag", "NaiveRAGBaseline"),
        ("citecheck.baselines.self_rag", "SelfRAGBaseline"),
        ("citecheck.baselines.crag", "CRAGBaseline"),
        ("citecheck.baselines.el_rag", "ELRAGBaseline"),
    ]:
        mod = importlib.import_module(mod_name)
        cls = getattr(mod, cls_name)
        assert hasattr(cls, "answer"), f"{cls_name} is missing answer()"
