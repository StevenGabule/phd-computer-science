"""Tests for ``citecheck.eval.runner`` and ``citecheck.eval.judge``.

The runner is exercised with a mocked baseline that returns canned predictions;
we verify the JSONL trace, the report JSON, and the metrics are correct.
The judge is exercised with a monkeypatched ``_complete`` so no SDK is called.
"""
from __future__ import annotations

import json
import math
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from citecheck.eval import EvaluationRunner, LLMJudge
from citecheck.eval.metrics import EvaluationReport
from citecheck.eval.types import (
    AnswerWithCitations,
    CitationStatus,
    CiteCheckExample,
    VerificationResult,
)


# ---------------------------------------------------------------------------
# Stub baselines
# ---------------------------------------------------------------------------
class _CannedBaseline:
    """A baseline that returns a fixed AnswerWithCitations on each call."""

    model_name = "test-model-0"

    def __init__(self) -> None:
        self.calls = 0

    def answer(self, question: str) -> AnswerWithCitations:
        self.calls += 1
        return AnswerWithCitations(
            question_id="",  # runner overrides with the gold example's id
            answer_text=f"Answer to: {question}",
            citations=["Smith v. Jones, 412 F.3d 567 (9th Cir. 2005)"],
            verification_results=[
                VerificationResult(
                    citation_str="Smith v. Jones, 412 F.3d 567 (9th Cir. 2005)",
                    status=CitationStatus.VERIFIED,
                    entailment_score=0.85,
                    resolved_opinion_id=12345,
                    resolved_court_jurisdiction="F-9",
                )
            ],
            latency_ms=123.0,
            tokens_used=256,
        )


class _FailingBaseline:
    """Always raises — used to verify runner resilience."""

    def answer(self, question: str) -> AnswerWithCitations:  # noqa: ARG002
        raise RuntimeError("simulated baseline crash")


# ---------------------------------------------------------------------------
# Runner — happy path
# ---------------------------------------------------------------------------
def test_evaluation_runner_iterates_examples(
    tmp_path: Path,
    sample_eval_examples: list[CiteCheckExample],
) -> None:
    baseline = _CannedBaseline()
    runner = EvaluationRunner(
        baseline=baseline,
        eval_examples=sample_eval_examples,
        output_dir=tmp_path,
        progress=False,
    )
    report = runner.run()
    assert baseline.calls == len(sample_eval_examples)
    assert isinstance(report, EvaluationReport)
    assert report.sample_size == len(sample_eval_examples)


def test_evaluation_runner_writes_jsonl_and_report(
    tmp_path: Path,
    sample_eval_examples: list[CiteCheckExample],
) -> None:
    baseline = _CannedBaseline()
    runner = EvaluationRunner(
        baseline=baseline,
        eval_examples=sample_eval_examples,
        output_dir=tmp_path,
        progress=False,
    )
    runner.run()

    trace = tmp_path / "predictions.jsonl"
    report_path = tmp_path / "report.json"
    assert trace.exists(), "runner must write predictions.jsonl"
    assert report_path.exists(), "runner must write report.json"

    # JSONL has one row per example with the canonical id.
    lines = trace.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == len(sample_eval_examples)
    rows = [json.loads(line) for line in lines]
    gold_ids = {ex.id for ex in sample_eval_examples}
    assert {r["question_id"] for r in rows} == gold_ids

    # First-row sanity: contains both the gold and prediction shapes we expect.
    first = rows[0]
    assert "gold_citations" in first
    assert "prediction" in first
    assert "verification_results" in first

    # Report JSON parses and has the expected top-level metric keys.
    report_data = json.loads(report_path.read_text(encoding="utf-8"))
    assert report_data["sample_size"] == len(sample_eval_examples)
    for key in (
        "resolution_rate",
        "fabrication_rate",
        "citation_support_f1",
        "jurisdictional_validity",
        "latency_ms",
        "tokens",
        "per_jurisdiction",
    ):
        assert key in report_data


def test_evaluation_runner_uses_baseline_model_name(
    tmp_path: Path,
    sample_eval_examples: list[CiteCheckExample],
) -> None:
    """Runner should pick up ``baseline.model_name`` automatically."""
    baseline = _CannedBaseline()
    runner = EvaluationRunner(
        baseline=baseline,
        eval_examples=sample_eval_examples,
        output_dir=tmp_path,
        progress=False,
    )
    report = runner.run()
    assert report.model_name == "test-model-0"
    assert report.baseline_name == "_CannedBaseline"


def test_evaluation_runner_explicit_names_override(
    tmp_path: Path,
    sample_eval_examples: list[CiteCheckExample],
) -> None:
    runner = EvaluationRunner(
        baseline=_CannedBaseline(),
        eval_examples=sample_eval_examples,
        output_dir=tmp_path,
        baseline_name="override-name",
        model_name="override-model",
        progress=False,
    )
    report = runner.run()
    assert report.baseline_name == "override-name"
    assert report.model_name == "override-model"


def test_evaluation_runner_resolution_rate_is_one_for_canned_baseline(
    tmp_path: Path,
    sample_eval_examples: list[CiteCheckExample],
) -> None:
    """The canned baseline emits only VERIFIED citations."""
    runner = EvaluationRunner(
        baseline=_CannedBaseline(),
        eval_examples=sample_eval_examples,
        output_dir=tmp_path,
        progress=False,
    )
    report = runner.run()
    assert report.resolution_rate == pytest.approx(1.0)
    assert report.fabrication_rate == pytest.approx(0.0)


# ---------------------------------------------------------------------------
# Runner — edge cases
# ---------------------------------------------------------------------------
def test_evaluation_runner_with_empty_examples(tmp_path: Path) -> None:
    runner = EvaluationRunner(
        baseline=_CannedBaseline(),
        eval_examples=[],
        output_dir=tmp_path,
        progress=False,
    )
    report = runner.run()
    assert report.sample_size == 0
    # Empty run still writes the report.
    assert (tmp_path / "report.json").exists()


def test_evaluation_runner_no_output_dir(
    sample_eval_examples: list[CiteCheckExample],
) -> None:
    """No output_dir means no files are written, but the report still returns."""
    runner = EvaluationRunner(
        baseline=_CannedBaseline(),
        eval_examples=sample_eval_examples,
        output_dir=None,
        progress=False,
    )
    report = runner.run()
    assert isinstance(report, EvaluationReport)


def test_evaluation_runner_baseline_exception_is_logged_not_fatal(
    tmp_path: Path,
    sample_eval_examples: list[CiteCheckExample],
) -> None:
    """One bad example should not abort the whole run."""
    runner = EvaluationRunner(
        baseline=_FailingBaseline(),
        eval_examples=sample_eval_examples,
        output_dir=tmp_path,
        progress=False,
    )
    report = runner.run()
    # All examples crashed -> zero citations emitted -> rates default.
    assert report.sample_size == len(sample_eval_examples)
    assert report.resolution_rate == pytest.approx(0.0)
    trace_rows = [
        json.loads(line)
        for line in (tmp_path / "predictions.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    assert all(
        r["prediction"]["metadata"].get("error") == "baseline_exception" for r in trace_rows
    )


def test_evaluation_runner_loads_human_ratings(
    tmp_path: Path,
    sample_eval_examples: list[CiteCheckExample],
) -> None:
    ratings_path = tmp_path / "ratings.json"
    ratings = {ex.id: 4 for ex in sample_eval_examples}
    ratings_path.write_text(json.dumps(ratings), encoding="utf-8")
    runner = EvaluationRunner(
        baseline=_CannedBaseline(),
        eval_examples=sample_eval_examples,
        output_dir=tmp_path,
        human_ratings_path=ratings_path,
        progress=False,
    )
    report = runner.run()
    assert report.answer_utility == pytest.approx(4.0)


def test_evaluation_runner_missing_ratings_file_skips_utility(
    tmp_path: Path,
    sample_eval_examples: list[CiteCheckExample],
) -> None:
    """A missing ratings file should log a warning and leave utility as NaN."""
    runner = EvaluationRunner(
        baseline=_CannedBaseline(),
        eval_examples=sample_eval_examples,
        output_dir=tmp_path,
        human_ratings_path=tmp_path / "does_not_exist.json",
        progress=False,
    )
    report = runner.run()
    assert math.isnan(report.answer_utility)


def test_evaluation_runner_overrides_question_id_on_predictions(
    tmp_path: Path,
    sample_eval_examples: list[CiteCheckExample],
) -> None:
    """Even if the baseline returns the wrong question_id, the runner aligns it."""

    class _MisidentifyingBaseline:
        def answer(self, question: str) -> AnswerWithCitations:  # noqa: ARG002
            return AnswerWithCitations(
                question_id="WRONG_ID",
                answer_text="x",
                citations=[],
                verification_results=[],
                latency_ms=10.0,
                tokens_used=5,
            )

    runner = EvaluationRunner(
        baseline=_MisidentifyingBaseline(),
        eval_examples=sample_eval_examples,
        output_dir=tmp_path,
        progress=False,
    )
    runner.run()
    rows = [
        json.loads(line)
        for line in (tmp_path / "predictions.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    assert {r["question_id"] for r in rows} == {ex.id for ex in sample_eval_examples}


# ---------------------------------------------------------------------------
# LLMJudge — inter-judge kappa
# ---------------------------------------------------------------------------
def test_llm_judge_inter_judge_kappa_perfect_agreement():
    judge = LLMJudge(dual_judge=False)
    kappa = judge.inter_judge_kappa(
        [True, True, False, False],
        [True, True, False, False],
    )
    assert kappa == pytest.approx(1.0)


def test_llm_judge_inter_judge_kappa_total_disagreement():
    judge = LLMJudge(dual_judge=False)
    # All 1 vs all 0 -> kappa = 0.0 (po=0, pe=0).
    kappa = judge.inter_judge_kappa(
        [True, True, True, True],
        [False, False, False, False],
    )
    assert kappa < 0.5


def test_llm_judge_inter_judge_kappa_accepts_dict_shapes():
    """Judgments may be {"supported": bool, ...} dicts."""
    judge = LLMJudge(dual_judge=False)
    a = [{"supported": True}, {"supported": False}]
    b = [{"supported": True}, {"supported": False}]
    assert judge.inter_judge_kappa(a, b) == pytest.approx(1.0)


def test_llm_judge_inter_judge_kappa_length_mismatch_raises():
    judge = LLMJudge(dual_judge=False)
    with pytest.raises(ValueError):
        judge.inter_judge_kappa([True], [True, False])


# ---------------------------------------------------------------------------
# LLMJudge — judge_support
# ---------------------------------------------------------------------------
def test_llm_judge_judge_support_parses_json_response(monkeypatch):
    judge = LLMJudge(dual_judge=False)
    monkeypatch.setattr(
        judge,
        "_complete",
        lambda prompt, model: '{"supported": true, "confidence": 0.91, "reasoning": "matches"}',
    )
    verdict = judge.judge_support(claim="X", evidence="Y")
    assert verdict["supported"] is True
    assert verdict["confidence"] == pytest.approx(0.91)
    assert "matches" in verdict["reasoning"]


def test_llm_judge_judge_support_handles_unparseable(monkeypatch):
    judge = LLMJudge(dual_judge=False)
    monkeypatch.setattr(judge, "_complete", lambda prompt, model: "not json at all")
    verdict = judge.judge_support(claim="X", evidence="Y")
    assert verdict["supported"] is False
    assert "parse error" in verdict["reasoning"].lower()


def test_llm_judge_judge_support_handles_backend_failure(monkeypatch):
    judge = LLMJudge(dual_judge=False)

    def _boom(prompt, model):  # noqa: ARG001
        raise RuntimeError("api down")

    monkeypatch.setattr(judge, "_complete", _boom)
    verdict = judge.judge_support(claim="X", evidence="Y")
    assert verdict["supported"] is False
    assert "backend error" in verdict["reasoning"].lower()


def test_llm_judge_judge_support_extracts_embedded_json(monkeypatch):
    """A judge that emits prose before/after JSON should still parse."""
    judge = LLMJudge(dual_judge=False)
    monkeypatch.setattr(
        judge,
        "_complete",
        lambda prompt, model: 'Sure. {"supported": true, "confidence": 0.5, "reasoning": "ok"}\n',
    )
    verdict = judge.judge_support(claim="X", evidence="Y")
    assert verdict["supported"] is True


# ---------------------------------------------------------------------------
# LLMJudge — dual judge
# ---------------------------------------------------------------------------
def test_llm_judge_dual_judge_constructs_secondary(monkeypatch):
    judge = LLMJudge(model="gpt-4o-mini", dual_judge=True)
    assert judge.secondary is not None
    # Primary is OpenAI -> secondary should be Anthropic-flavored.
    assert judge.secondary.model.startswith("claude")


def test_llm_judge_dual_judge_intersection_logic(monkeypatch):
    judge = LLMJudge(model="gpt-4o-mini", dual_judge=True)
    monkeypatch.setattr(
        judge,
        "_complete",
        lambda prompt, model: '{"supported": true, "confidence": 0.9, "reasoning": ""}',
    )
    monkeypatch.setattr(
        judge.secondary,
        "_complete",
        lambda prompt, model: '{"supported": false, "confidence": 0.6, "reasoning": ""}',
    )
    verdict = judge.judge_support_dual(claim="X", evidence="Y")
    # Conservative intersection -> not supported.
    assert verdict["supported"] is False
    assert verdict["confidence"] == pytest.approx(0.6)
    assert verdict["primary"]["supported"] is True
    assert verdict["secondary"]["supported"] is False


def test_llm_judge_dual_judge_disabled_raises_on_dual_call():
    judge = LLMJudge(dual_judge=False)
    with pytest.raises(RuntimeError):
        judge.judge_support_dual(claim="X", evidence="Y")


def test_llm_judge_default_complete_raises():
    """The default ``_complete`` is a hook; calling it directly must raise."""
    judge = LLMJudge(dual_judge=False)
    with pytest.raises(NotImplementedError):
        judge._complete(prompt="hello", model=judge.model)
