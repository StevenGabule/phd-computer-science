"""Tests for citecheck.eval.runner — EvaluationRunner."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from citecheck.eval.types import (
    AnswerWithCitations,
    CitationStatus,
    CiteCheckExample,
    VerificationResult,
)


class _CannedBaseline:
    """A baseline that returns a fixed AnswerWithCitations per question."""

    def __init__(self):
        self.calls = 0

    def answer(self, question: str) -> AnswerWithCitations:
        self.calls += 1
        return AnswerWithCitations(
            question_id=f"q{self.calls}",
            answer_text=f"Answer to: {question}",
            citations=["Smith v. Jones, 412 F.3d 567 (9th Cir. 2005)"],
            verification_results=[
                VerificationResult(
                    citation_str="Smith v. Jones, 412 F.3d 567 (9th Cir. 2005)",
                    status=CitationStatus.VERIFIED,
                    entailment_score=0.85,
                ),
            ],
            latency_ms=123.0,
            tokens_used=256,
        )


def test_evaluation_runner_iterates_examples(tmp_path: Path, sample_eval_examples):
    from citecheck.eval import EvaluationRunner

    baseline = _CannedBaseline()
    runner = EvaluationRunner(
        baseline=baseline,
        eval_examples=sample_eval_examples,
        output_dir=tmp_path,
    )
    report = runner.run()
    assert baseline.calls == len(sample_eval_examples)
    assert report is not None


def test_evaluation_runner_writes_output(tmp_path: Path, sample_eval_examples):
    from citecheck.eval import EvaluationRunner

    baseline = _CannedBaseline()
    runner = EvaluationRunner(
        baseline=baseline,
        eval_examples=sample_eval_examples,
        output_dir=tmp_path,
    )
    runner.run()
    # At minimum, the output directory should contain at least one file
    written = list(tmp_path.glob("*"))
    assert len(written) >= 1


def test_evaluation_runner_with_empty_examples(tmp_path: Path):
    from citecheck.eval import EvaluationRunner

    baseline = _CannedBaseline()
    runner = EvaluationRunner(
        baseline=baseline,
        eval_examples=[],
        output_dir=tmp_path,
    )
    report = runner.run()
    assert baseline.calls == 0
    assert report is not None


def test_llm_judge_inter_judge_kappa():
    """Inter-judge kappa should compute correctly for matching judgments."""
    from citecheck.eval import LLMJudge

    judge = LLMJudge(dual_judge=False)
    # Perfect agreement → kappa should be 1.0
    kappa = judge.inter_judge_kappa([True, True, False, False], [True, True, False, False])
    assert kappa == pytest.approx(1.0)


def test_llm_judge_kappa_disagreement():
    from citecheck.eval import LLMJudge

    judge = LLMJudge(dual_judge=False)
    # Total disagreement → kappa near -1.0
    kappa = judge.inter_judge_kappa([True, True, True, True], [False, False, False, False])
    assert kappa < 0.5
