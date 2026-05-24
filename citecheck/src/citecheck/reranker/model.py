"""Cross-encoder reranker with two output heads.

Design choice — shared backbone, two heads
==========================================
We share the entire transformer encoder between the two objectives
(relevance, citation-groundedness) and only diverge at the very top, with two
small linear heads on the pooled [CLS] representation. Reasons:

* The two signals are highly correlated — a passage that is grounded by a
  citation supporting the claim is almost always also relevant. A shared
  backbone exploits that correlation rather than fighting it.
* Halves the parameter count vs. two encoders, so we can fit comfortably with
  4-bit QLoRA on a single 24 GB GPU.
* Matches the standard "multi-head" pattern used in joint NLI/STS models, so
  later swapping in a stronger backbone (DeBERTa-v3, ModernBERT) is one
  ``from_pretrained`` call away.

Both heads are trained jointly under :class:`MultiObjectiveLoss` (see
``loss.py``). At inference, the convenience method :meth:`rerank` exposes the
``lambda`` knob from the lambda sweep in ``RERANKER.lambda_sweep``.
"""
from __future__ import annotations

import logging
from typing import Any

import torch
from torch import nn

from citecheck.config import MODELS
from citecheck.retrieval.bm25 import RetrievalResult

logger = logging.getLogger(__name__)


class CrossEncoderReranker(nn.Module):
    """A two-headed cross-encoder built on a HuggingFace AutoModel backbone.

    Args:
        model_name: HuggingFace model id. Defaults to ``MODELS.reranker_base``.
        dropout: Dropout applied between the pooled vector and each head.
    """

    def __init__(
        self,
        model_name: str | None = None,
        dropout: float = 0.1,
        tokenizer: Any = None,
    ) -> None:
        super().__init__()
        from transformers import AutoModel, AutoTokenizer

        self.model_name = model_name or MODELS.reranker_base
        logger.info("Loading reranker backbone %s", self.model_name)
        self.backbone = AutoModel.from_pretrained(self.model_name)
        hidden = self.backbone.config.hidden_size
        self.dropout = nn.Dropout(dropout)
        self.relevance_head = nn.Linear(hidden, 1)
        self.groundedness_head = nn.Linear(hidden, 1)
        self.tokenizer = tokenizer or AutoTokenizer.from_pretrained(self.model_name)
        self._init_heads()

    def _init_heads(self) -> None:
        for head in (self.relevance_head, self.groundedness_head):
            nn.init.xavier_uniform_(head.weight)
            nn.init.zeros_(head.bias)

    # ----------------------------------------------------------------- forward

    def _pool(self, last_hidden_state: torch.Tensor, attention_mask: torch.Tensor) -> torch.Tensor:
        """Pool [CLS] when available, else mean-pool with attention mask."""
        if self.backbone.config.model_type in {"bert", "roberta", "deberta-v2", "electra"}:
            return last_hidden_state[:, 0]
        # Generic mean pooling fallback (works for any encoder).
        mask = attention_mask.unsqueeze(-1).to(last_hidden_state.dtype)
        return (last_hidden_state * mask).sum(dim=1) / mask.sum(dim=1).clamp(min=1e-6)

    def forward(
        self,
        input_ids: torch.Tensor,
        attention_mask: torch.Tensor,
    ) -> tuple[torch.Tensor, torch.Tensor]:
        """Return ``(relevance_logit, groundedness_logit)`` shape ``[B]`` each."""
        outputs = self.backbone(input_ids=input_ids, attention_mask=attention_mask)
        pooled = self._pool(outputs.last_hidden_state, attention_mask)
        pooled = self.dropout(pooled)
        rel = self.relevance_head(pooled).squeeze(-1)
        gnd = self.groundedness_head(pooled).squeeze(-1)
        return rel, gnd

    # --------------------------------------------------------------- inference

    @torch.inference_mode()
    def score(self, query: str, passage: str, max_length: int = 512) -> tuple[float, float]:
        """Score a single (query, passage) pair.

        Returns:
            ``(relevance_prob, groundedness_score)`` where the relevance head
            is passed through a sigmoid (BCE-trained) and groundedness through
            sigmoid as well (MSE-trained on a [0, 1] target).
        """
        device = next(self.parameters()).device
        enc = self.tokenizer(
            query,
            passage,
            truncation=True,
            padding="max_length",
            max_length=max_length,
            return_tensors="pt",
        ).to(device)
        rel_logit, gnd_logit = self.forward(enc["input_ids"], enc["attention_mask"])
        rel = torch.sigmoid(rel_logit).item()
        gnd = torch.sigmoid(gnd_logit).item()
        return float(rel), float(gnd)

    @torch.inference_mode()
    def score_batch(
        self,
        queries: list[str],
        passages: list[str],
        batch_size: int = 32,
        max_length: int = 512,
    ) -> list[tuple[float, float]]:
        """Batched variant of :meth:`score`."""
        if len(queries) != len(passages):
            raise ValueError("queries and passages must be the same length")
        device = next(self.parameters()).device
        out: list[tuple[float, float]] = []
        for start in range(0, len(queries), batch_size):
            q_batch = queries[start:start + batch_size]
            p_batch = passages[start:start + batch_size]
            enc = self.tokenizer(
                q_batch,
                p_batch,
                truncation=True,
                padding="max_length",
                max_length=max_length,
                return_tensors="pt",
            ).to(device)
            rel, gnd = self.forward(enc["input_ids"], enc["attention_mask"])
            rel_p = torch.sigmoid(rel).tolist()
            gnd_p = torch.sigmoid(gnd).tolist()
            out.extend(zip(rel_p, gnd_p, strict=True))
        return out

    def rerank(
        self,
        query: str,
        candidates: list[RetrievalResult],
        lambda_: float = 0.5,
        batch_size: int = 32,
        max_length: int = 512,
    ) -> list[RetrievalResult]:
        """Re-score and re-sort candidates.

        New score = ``relevance + lambda_ * groundedness``. Candidates without
        a ``passage`` attribute fall back to a neutral score so they aren't
        silently dropped.

        Args:
            query: The query string.
            candidates: First-stage retrieval results.
            lambda_: Weight on the groundedness term — sweep
                ``RERANKER.lambda_sweep`` to choose.
            batch_size: Score-time batch size.
            max_length: Tokenizer truncation length.

        Returns:
            Candidates sorted by descending fused score, with new ``rank``
            assigned. The fused score is written into ``score``; the original
            first-stage score is preserved in ``metadata['first_stage_score']``.
        """
        if not candidates:
            return []
        passages = [c.passage or "" for c in candidates]
        queries = [query] * len(candidates)
        scored = self.score_batch(queries, passages, batch_size=batch_size, max_length=max_length)

        rescored: list[RetrievalResult] = []
        for cand, (rel, gnd) in zip(candidates, scored, strict=True):
            fused = float(rel + lambda_ * gnd)
            meta = dict(cand.metadata)
            meta.setdefault("first_stage_score", cand.score)
            meta["relevance"] = rel
            meta["groundedness"] = gnd
            rescored.append(
                RetrievalResult(
                    doc_id=cand.doc_id,
                    score=fused,
                    rank=cand.rank,  # will be overwritten below
                    passage=cand.passage,
                    metadata=meta,
                )
            )
        rescored.sort(key=lambda r: r.score, reverse=True)
        for new_rank, r in enumerate(rescored, start=1):
            r.rank = new_rank
        return rescored

    # ------------------------------------------------------------ persistence

    def save_pretrained(self, path: Any) -> None:
        """Save backbone, tokenizer, and head weights to ``path``."""
        from pathlib import Path

        path = Path(path)
        path.mkdir(parents=True, exist_ok=True)
        self.backbone.save_pretrained(path)
        self.tokenizer.save_pretrained(path)
        torch.save(
            {
                "relevance_head": self.relevance_head.state_dict(),
                "groundedness_head": self.groundedness_head.state_dict(),
            },
            path / "heads.pt",
        )
        logger.info("Saved CrossEncoderReranker to %s", path)

    @classmethod
    def from_pretrained(cls, path: Any) -> "CrossEncoderReranker":
        """Inverse of :meth:`save_pretrained`."""
        from pathlib import Path

        from transformers import AutoTokenizer

        path = Path(path)
        tokenizer = AutoTokenizer.from_pretrained(path)
        model = cls(model_name=str(path), tokenizer=tokenizer)
        head_state = torch.load(path / "heads.pt", map_location="cpu")
        model.relevance_head.load_state_dict(head_state["relevance_head"])
        model.groundedness_head.load_state_dict(head_state["groundedness_head"])
        return model
