"""Multi-objective loss combining relevance + citation groundedness.

The CiteCheck reranker is optimized for two coupled objectives:

* **Relevance** (binary, BCE) — does this passage answer the query at all?
* **Citation groundedness** (real in [0, 1], MSE) — what fraction of the
  citations in this passage resolve to an opinion that supports the query?

The combined loss is::

    L = L_relevance + lambda_ * L_groundedness

Lambda sweep
============
Per ``RERANKER.lambda_sweep`` we train a reranker for each
``lambda_ in {0.1, 0.3, 0.5, 1.0}`` and select the best on the validation set
using the agent's downstream Citation Support F1. ``lambda_ = 0.0`` is the
baseline (relevance-only) and is what the cross-encoder backbone was
pretrained on, so we don't repeat it in the sweep.
"""
from __future__ import annotations

import logging

import torch
from torch import nn
from torch.nn import functional as F

logger = logging.getLogger(__name__)

_RELEVANCE_LOSSES = {"bce", "bce_with_logits"}
_GROUNDEDNESS_LOSSES = {"mse", "smooth_l1", "bce", "bce_with_logits"}


class MultiObjectiveLoss(nn.Module):
    """Weighted sum of relevance and groundedness losses.

    Args:
        lambda_: Weight on the groundedness term. Sweep
            ``RERANKER.lambda_sweep`` to choose.
        relevance_loss: One of ``{"bce", "bce_with_logits"}`` (synonyms).
        groundedness_loss: One of ``{"mse", "smooth_l1", "bce",
            "bce_with_logits"}``. ``mse`` is the default because the label is
            a continuous fraction in [0, 1]; ``bce`` is appropriate if you
            binarize the label at some threshold instead.
        reduction: ``"mean"`` (default) or ``"sum"``.
    """

    def __init__(
        self,
        lambda_: float = 0.5,
        relevance_loss: str = "bce",
        groundedness_loss: str = "mse",
        reduction: str = "mean",
    ) -> None:
        super().__init__()
        if lambda_ < 0:
            raise ValueError(f"lambda_ must be >= 0, got {lambda_}")
        if relevance_loss not in _RELEVANCE_LOSSES:
            raise ValueError(
                f"relevance_loss must be one of {_RELEVANCE_LOSSES}, got {relevance_loss!r}"
            )
        if groundedness_loss not in _GROUNDEDNESS_LOSSES:
            raise ValueError(
                f"groundedness_loss must be one of {_GROUNDEDNESS_LOSSES}, "
                f"got {groundedness_loss!r}"
            )
        if reduction not in {"mean", "sum"}:
            raise ValueError(f"reduction must be 'mean' or 'sum', got {reduction!r}")

        self.lambda_ = float(lambda_)
        self.relevance_loss = relevance_loss
        self.groundedness_loss = groundedness_loss
        self.reduction = reduction

    # ----------------------------------------------------------------- forward

    def _relevance(self, logit: torch.Tensor, label: torch.Tensor) -> torch.Tensor:
        return F.binary_cross_entropy_with_logits(
            logit, label.to(logit.dtype), reduction=self.reduction
        )

    def _groundedness(self, logit: torch.Tensor, label: torch.Tensor) -> torch.Tensor:
        target = label.to(logit.dtype)
        if self.groundedness_loss == "mse":
            # Apply sigmoid so logits and target ([0,1]) live on the same scale.
            pred = torch.sigmoid(logit)
            return F.mse_loss(pred, target, reduction=self.reduction)
        if self.groundedness_loss == "smooth_l1":
            pred = torch.sigmoid(logit)
            return F.smooth_l1_loss(pred, target, reduction=self.reduction)
        # bce / bce_with_logits — target should be in [0, 1].
        return F.binary_cross_entropy_with_logits(logit, target, reduction=self.reduction)

    def forward(
        self,
        relevance_logit: torch.Tensor,
        groundedness_logit: torch.Tensor,
        relevance_label: torch.Tensor,
        groundedness_label: torch.Tensor,
    ) -> torch.Tensor:
        """Compute ``L_rel + lambda_ * L_gnd``.

        Shapes are flexible: all four tensors must broadcast together.
        """
        l_rel = self._relevance(relevance_logit, relevance_label)
        l_gnd = self._groundedness(groundedness_logit, groundedness_label)
        return l_rel + self.lambda_ * l_gnd

    def components(
        self,
        relevance_logit: torch.Tensor,
        groundedness_logit: torch.Tensor,
        relevance_label: torch.Tensor,
        groundedness_label: torch.Tensor,
    ) -> dict[str, torch.Tensor]:
        """Return the unweighted components, useful for logging.

        Example:
            >>> loss = MultiObjectiveLoss(lambda_=0.5)
            >>> parts = loss.components(rl, gl, ry, gy)
            >>> wandb.log({"loss/rel": parts["relevance"].item(),
            ...            "loss/gnd": parts["groundedness"].item()})
        """
        return {
            "relevance": self._relevance(relevance_logit, relevance_label),
            "groundedness": self._groundedness(groundedness_logit, groundedness_label),
        }
