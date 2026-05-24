"""LLM-as-judge for Citation Support entailment + inter-judge agreement.

The CiteCheck design (`project/citecheck_design.md` §4) reports Citation Support
F1 by both NLI (machine) and human audit. The :class:`LLMJudge` here is the
*third* judge: a free-text reasoner that gives the dual-judge fallback when
NLI is too uncertain, and a sanity check on the 200-item human audit.

Design notes
------------
* Backend dispatch is by model-name prefix: ``gpt-*`` -> OpenAI, ``claude-*``
  -> Anthropic, ``llama-*`` / ``qwen-*`` -> a generic local interface.
* The actual SDK call is left as :meth:`_complete`, which raises
  :class:`NotImplementedError` by default. Wire it to your preferred SDK at
  call sites (the test suite mocks it directly).
* Dual-judge mode instantiates a *second* judge (default: Claude) and reports
  inter-judge Cohen's kappa via :meth:`inter_judge_kappa`.
"""
from __future__ import annotations

import json
import logging
import re
from typing import Any

from sklearn.metrics import cohen_kappa_score

from citecheck.config import MODELS

logger = logging.getLogger(__name__)


# Default judge prompt — keep terse to control token cost. The judge must
# return a JSON object on a single line so we can robustly parse it.
_JUDGE_PROMPT = """You are an expert legal-research auditor. You will be given
a CLAIM that a legal citation supposedly supports, and the EVIDENCE text from
the cited opinion. Decide whether the EVIDENCE textually entails the CLAIM
under standard Bluebook reasoning.

Respond with a single JSON object on one line and nothing else:
{{"supported": <true|false>, "confidence": <float in [0.0, 1.0]>, "reasoning": "<one sentence>"}}

CLAIM: {claim}

EVIDENCE: {evidence}

JSON:"""


def _model_backend(model_name: str) -> str:
    """Pick a backend hint from the model name prefix.

    Returns one of ``"openai"``, ``"anthropic"``, ``"local"``. Used for
    logging and to let callers dispatch their own SDK; this module does not
    import any SDKs directly.
    """
    name = model_name.lower()
    if name.startswith(("gpt-", "o1-", "o3-", "text-davinci")):
        return "openai"
    if name.startswith("claude"):
        return "anthropic"
    return "local"


class LLMJudge:
    """LLM-as-judge for claim-vs-evidence entailment.

    Args:
        model: Primary judge model name. Defaults to
            :data:`citecheck.config.MODELS.closed_ceiling`.
        dual_judge: When ``True`` (default), instantiates a second judge from
            ``secondary_model`` to support :meth:`inter_judge_kappa`.
        secondary_model: Override for the second judge. If ``None``, picks a
            backend different from ``model`` (e.g. Claude if primary is GPT,
            and vice versa).

    Example::

        judge = LLMJudge(model="gpt-4o-mini", dual_judge=True)
        verdict = judge.judge_support(claim="...", evidence="...")
        # {"supported": True, "confidence": 0.9, "reasoning": "..."}
    """

    def __init__(
        self,
        model: str = MODELS.closed_ceiling,
        dual_judge: bool = True,
        secondary_model: str | None = None,
    ) -> None:
        self.model = model
        self.backend = _model_backend(model)
        self.dual_judge = dual_judge
        self.secondary: LLMJudge | None = None
        if dual_judge:
            if secondary_model is None:
                secondary_model = (
                    "claude-3-5-sonnet-latest"
                    if self.backend == "openai"
                    else "gpt-4o-mini"
                )
            # Construct without recursing into dual_judge to avoid infinite loops.
            self.secondary = LLMJudge(model=secondary_model, dual_judge=False)
        logger.debug(
            "LLMJudge(model=%s, backend=%s, dual=%s, secondary=%s)",
            self.model,
            self.backend,
            self.dual_judge,
            getattr(self.secondary, "model", None),
        )

    # ---- main API --------------------------------------------------------
    def judge_support(self, claim: str, evidence: str) -> dict[str, Any]:
        """Single-judge support verdict.

        Returns a dict with keys ``supported`` (bool), ``confidence`` (float
        in ``[0, 1]``), ``reasoning`` (str). If parsing fails the verdict
        defaults to ``{"supported": False, "confidence": 0.0,
        "reasoning": "judge parse error: <raw>"}``.
        """
        prompt = _JUDGE_PROMPT.format(claim=claim.strip(), evidence=evidence.strip())
        try:
            raw = self._complete(prompt=prompt, model=self.model)
        except Exception as exc:  # noqa: BLE001 - external SDK failures
            logger.warning("LLMJudge backend failure (%s): %s", self.model, exc)
            return {
                "supported": False,
                "confidence": 0.0,
                "reasoning": f"judge backend error: {exc!s}",
            }
        return _parse_judge_response(raw)

    def judge_support_dual(self, claim: str, evidence: str) -> dict[str, Any]:
        """Dual-judge verdict.

        Calls both the primary and secondary judges. Returns a dict with both
        verdicts plus a top-level ``"supported"`` that is ``True`` iff both
        judges agree it is supported (intersection — conservative for safety
        metrics).
        """
        if not self.dual_judge or self.secondary is None:
            raise RuntimeError(
                "judge_support_dual requires dual_judge=True at construction."
            )
        primary = self.judge_support(claim, evidence)
        secondary = self.secondary.judge_support(claim, evidence)
        return {
            "supported": bool(primary["supported"]) and bool(secondary["supported"]),
            "confidence": min(
                float(primary["confidence"]),
                float(secondary["confidence"]),
            ),
            "primary": primary,
            "secondary": secondary,
        }

    # ---- agreement metric -----------------------------------------------
    @staticmethod
    def inter_judge_kappa(
        judgments_a: list[Any],
        judgments_b: list[Any],
    ) -> float:
        """Cohen's kappa between two label sequences.

        Both arguments must be aligned and the same length. Each element is
        coerced to ``int(bool(x))`` so booleans, 0/1, and dict-with-``supported``
        all work.
        """
        if len(judgments_a) != len(judgments_b):
            raise ValueError(
                f"length mismatch: {len(judgments_a)} vs {len(judgments_b)}"
            )
        if not judgments_a:
            return float("nan")
        a = [int(bool(_extract_label(x))) for x in judgments_a]
        b = [int(bool(_extract_label(x))) for x in judgments_b]
        # sklearn returns nan when there is only one class in both; coerce to 1.0
        # for the special case "both judges agree on everything" because kappa is
        # undefined but the practical interpretation is perfect agreement.
        if set(a) | set(b) == {0} or set(a) | set(b) == {1}:
            return 1.0
        return float(cohen_kappa_score(a, b))

    # ---- backend hook ----------------------------------------------------
    def _complete(self, prompt: str, model: str) -> str:  # noqa: ARG002 - subclass hook
        """Generate a completion. **Override or monkeypatch in production.**

        The default implementation raises ``NotImplementedError`` because we
        do not import vendor SDKs in this module. Wiring options:

        * Subclass :class:`LLMJudge` and override ``_complete``.
        * Or monkeypatch the instance in tests / glue scripts.
        """
        raise NotImplementedError(
            f"LLMJudge._complete is a hook; wire it to your {self.backend} SDK. "
            "See module docstring for guidance."
        )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _parse_judge_response(raw: str) -> dict[str, Any]:
    """Best-effort JSON extraction from a judge response.

    Strategy:
    1. Strip whitespace and try ``json.loads`` directly.
    2. If that fails, scan for the first ``{...}`` block (greedy match).
    3. If that fails, return a sentinel "parse error" verdict.
    """
    raw = (raw or "").strip()
    candidates = [raw]
    match = re.search(r"\{.*\}", raw, flags=re.DOTALL)
    if match:
        candidates.append(match.group(0))

    for candidate in candidates:
        try:
            parsed = json.loads(candidate)
        except (json.JSONDecodeError, TypeError):
            continue
        if not isinstance(parsed, dict):
            continue
        return {
            "supported": bool(parsed.get("supported", False)),
            "confidence": float(parsed.get("confidence", 0.0)),
            "reasoning": str(parsed.get("reasoning", "")),
        }

    logger.warning("LLMJudge could not parse response: %r", raw[:200])
    return {
        "supported": False,
        "confidence": 0.0,
        "reasoning": f"judge parse error: {raw[:120]}",
    }


def _extract_label(x: Any) -> bool:
    """Pull a boolean ``supported`` label out of any of the shapes we accept."""
    if isinstance(x, dict):
        return bool(x.get("supported", False))
    return bool(x)


__all__ = ["LLMJudge"]
