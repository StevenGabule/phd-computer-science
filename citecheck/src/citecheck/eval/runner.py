"""End-to-end evaluation runner.

The :class:`EvaluationRunner` iterates an eval set, invokes a baseline /
system-under-test, captures predictions (with wall-clock latency), computes the
seven metrics, and writes both a per-question JSONL trace and a top-level
:class:`citecheck.eval.metrics.EvaluationReport`.

Typical usage::

    from citecheck.eval import EvaluationRunner
    from citecheck.baselines import VanillaBaseline

    runner = EvaluationRunner(
        baseline=VanillaBaseline(),
        eval_examples=load_eval_set(PATHS.eval_set),
        output_dir=PATHS.runs_dir / "vanilla-2026-05-24",
    )
    report = runner.run()
    print(report.to_json())
"""
from __future__ import annotations

import json
import logging
import time
from dataclasses import asdict, is_dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from tqdm import tqdm

from citecheck.eval.metrics import EvaluationReport, aggregate_metrics
from citecheck.eval.types import (
    AnswerWithCitations,
    BaselineProtocol,
    CiteCheckExample,
)

logger = logging.getLogger(__name__)


class EvaluationRunner:
    """Runs a baseline against an eval set and produces an :class:`EvaluationReport`.

    Args:
        baseline: Any object implementing :class:`BaselineProtocol` (i.e. has
            ``answer(question: str) -> AnswerWithCitations``).
        eval_examples: List of :class:`CiteCheckExample` to evaluate against.
        output_dir: Where to write the per-question JSONL trace and the
            top-level report JSON. If ``None``, nothing is written to disk.
        human_ratings_path: Optional path to a JSON file containing
            ``{"<question_id>": <Likert 1-5>, ...}`` for answer utility.
        baseline_name: Human-readable label for the run (defaults to the
            baseline's class name).
        model_name: Model identifier; pulled from ``baseline.model`` or
            ``baseline.model_name`` if present, otherwise ``"unknown"``.
        progress: Show tqdm progress bar. Disable for non-TTY logs.
    """

    def __init__(
        self,
        baseline: BaselineProtocol,
        eval_examples: list[CiteCheckExample],
        output_dir: Path | None = None,
        human_ratings_path: Path | None = None,
        baseline_name: str | None = None,
        model_name: str | None = None,
        progress: bool = True,
    ) -> None:
        self.baseline = baseline
        self.eval_examples = list(eval_examples)
        self.output_dir = Path(output_dir) if output_dir is not None else None
        self.human_ratings_path = (
            Path(human_ratings_path) if human_ratings_path is not None else None
        )
        self.baseline_name = baseline_name or type(baseline).__name__
        self.model_name = model_name or _infer_model_name(baseline)
        self.progress = progress

        if self.output_dir is not None:
            self.output_dir.mkdir(parents=True, exist_ok=True)

    # ---- main entry point ------------------------------------------------
    def run(self) -> EvaluationReport:
        """Iterate the eval set, score it, persist outputs, and return the report."""
        if not self.eval_examples:
            raise ValueError("EvaluationRunner.run called with no eval examples.")

        logger.info(
            "Starting evaluation: baseline=%s model=%s n=%d output=%s",
            self.baseline_name,
            self.model_name,
            len(self.eval_examples),
            self.output_dir,
        )

        predictions: list[AnswerWithCitations] = []
        trace_path = (
            self.output_dir / "predictions.jsonl" if self.output_dir is not None else None
        )

        # Open the trace once so we stream rows even on long runs.
        trace_fh = trace_path.open("w", encoding="utf-8") if trace_path else None
        try:
            iterator = self.eval_examples
            if self.progress:
                iterator = tqdm(iterator, desc=f"eval[{self.baseline_name}]")
            for ex in iterator:
                pred = self._answer_one(ex)
                predictions.append(pred)
                if trace_fh is not None:
                    trace_fh.write(json.dumps(_serialize_trace_row(ex, pred)) + "\n")
                    trace_fh.flush()
        finally:
            if trace_fh is not None:
                trace_fh.close()

        human_ratings = self._load_human_ratings_aligned()

        report = aggregate_metrics(
            predictions=predictions,
            gold=self.eval_examples,
            human_ratings=human_ratings,
            baseline_name=self.baseline_name,
            model_name=self.model_name,
            run_id=_make_run_id(self.baseline_name),
            extra={
                "n_examples": len(self.eval_examples),
                "trace_path": str(trace_path) if trace_path else None,
                "human_ratings_path": (
                    str(self.human_ratings_path) if self.human_ratings_path else None
                ),
            },
        )

        if self.output_dir is not None:
            report_path = self.output_dir / "report.json"
            report_path.write_text(report.to_json(), encoding="utf-8")
            logger.info("Wrote report to %s", report_path)

        logger.info(
            "Evaluation complete: resolution=%.3f fabrication=%.3f "
            "jurisdictional=%.3f support_f1=%.3f",
            report.resolution_rate,
            report.fabrication_rate,
            report.jurisdictional_validity,
            report.citation_support_f1.get("f1", float("nan")),
        )
        return report

    # ---- per-example mechanics ------------------------------------------
    def _answer_one(self, ex: CiteCheckExample) -> AnswerWithCitations:
        """Invoke the baseline once, capturing latency if the baseline did not."""
        start = time.perf_counter()
        try:
            pred = self.baseline.answer(ex.question)
        except Exception:  # noqa: BLE001 - we never want one bad example to abort a run
            logger.exception("Baseline failed on example id=%s; recording empty answer.", ex.id)
            elapsed_ms = (time.perf_counter() - start) * 1000.0
            pred = AnswerWithCitations(
                question_id=ex.id,
                answer_text="",
                citations=[],
                verification_results=[],
                latency_ms=elapsed_ms,
                metadata={"error": "baseline_exception"},
            )
            return pred

        elapsed_ms = (time.perf_counter() - start) * 1000.0
        # Force question_id and latency onto the prediction (the baseline may not).
        if getattr(pred, "question_id", None) in (None, ""):
            pred = _with_field(pred, question_id=ex.id)
        if getattr(pred, "latency_ms", None) is None:
            pred = _with_field(pred, latency_ms=elapsed_ms)
        return pred

    # ---- human ratings ---------------------------------------------------
    def _load_human_ratings_aligned(self) -> list[int] | None:
        """Read ``human_ratings_path`` and align it to ``self.eval_examples``.

        Returns ``None`` if no path was given. Missing IDs become ``None`` in
        the returned list so :func:`answer_utility` ignores them.
        """
        if self.human_ratings_path is None:
            return None
        if not self.human_ratings_path.exists():
            logger.warning(
                "human_ratings_path %s not found; skipping utility metric.",
                self.human_ratings_path,
            )
            return None
        try:
            raw = json.loads(self.human_ratings_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            logger.warning("Could not read human ratings (%s); skipping.", exc)
            return None
        if not isinstance(raw, dict):
            logger.warning("human_ratings JSON must be {question_id: rating}; got %s", type(raw))
            return None
        aligned: list[int] = []
        for ex in self.eval_examples:
            val = raw.get(ex.id)
            aligned.append(int(val) if isinstance(val, (int, float)) else None)  # type: ignore[arg-type]
        return aligned  # type: ignore[return-value]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _infer_model_name(baseline: Any) -> str:
    for attr in ("model_name", "model", "_model_name"):
        v = getattr(baseline, attr, None)
        if isinstance(v, str) and v:
            return v
    return "unknown"


def _make_run_id(baseline_name: str) -> str:
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    return f"{baseline_name}-{stamp}"


def _with_field(obj: Any, **updates: Any) -> Any:
    """Return a copy of ``obj`` with the named fields updated.

    Works on dataclasses; falls back to setattr for non-dataclass objects
    (best-effort — if the object is frozen and not a dataclass we re-raise).
    """
    if is_dataclass(obj) and not isinstance(obj, type):
        from dataclasses import replace

        try:
            return replace(obj, **updates)
        except TypeError:
            # frozen-but-not-replace-compatible: build a new dict and re-construct.
            pass
    # Best-effort mutation:
    for k, v in updates.items():
        try:
            setattr(obj, k, v)
        except (AttributeError, TypeError):
            logger.debug("Could not set %s on %s; leaving original value.", k, type(obj))
    return obj


def _serialize_trace_row(ex: CiteCheckExample, pred: AnswerWithCitations) -> dict[str, Any]:
    """Pack one (gold, prediction, verification) tuple into a JSON-serializable dict."""
    return {
        "question_id": ex.id,
        "question": ex.question,
        "jurisdiction": ex.jurisdiction,
        "gold_citations": list(ex.gold_citations),
        "gold_metadata": _maybe_asdict(ex.metadata),
        "prediction": {
            "answer_text": pred.answer_text,
            "citations": list(pred.citations or []),
            "latency_ms": pred.latency_ms,
            "tokens_used": pred.tokens_used,
            "metadata": _maybe_asdict(pred.metadata),
        },
        "verification_results": [
            _verification_to_dict(vr) for vr in (pred.verification_results or [])
        ],
    }


def _verification_to_dict(vr: Any) -> dict[str, Any]:
    """Serialize a VerificationResult-like object into plain JSON types."""
    if is_dataclass(vr) and not isinstance(vr, type):
        d = asdict(vr)
        # Coerce enum -> str for JSON.
        status = d.get("status")
        if hasattr(status, "value"):
            d["status"] = status.value
        elif status is not None:
            d["status"] = str(status)
        return d
    # Fallback: pull known attributes if present.
    status = getattr(vr, "status", None)
    return {
        "citation_str": getattr(vr, "citation_str", ""),
        "status": getattr(status, "value", str(status) if status is not None else ""),
        "entailment_score": getattr(vr, "entailment_score", 0.0),
        "resolved_opinion_id": getattr(vr, "resolved_opinion_id", None),
        "resolved_court_jurisdiction": getattr(vr, "resolved_court_jurisdiction", ""),
        "reasoning": getattr(vr, "reasoning", ""),
    }


def _maybe_asdict(value: Any) -> Any:
    """Convert dataclasses and unknowns to plain JSON types defensively."""
    if value is None:
        return None
    if is_dataclass(value) and not isinstance(value, type):
        return asdict(value)
    if isinstance(value, dict):
        return {k: _maybe_asdict(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_maybe_asdict(v) for v in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return str(value)


__all__ = ["EvaluationRunner"]
