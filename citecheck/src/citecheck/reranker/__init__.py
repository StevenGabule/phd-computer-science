"""CiteCheck reranker package.

A cross-encoder with two output heads — relevance and citation-groundedness —
trained jointly under a weighted multi-objective loss. See ``model.py``,
``loss.py``, and ``train.py`` for the moving parts, and ``dataset.py`` for the
training-data construction routine.
"""
from __future__ import annotations

from citecheck.reranker.dataset import (
    RerankerDataset,
    RerankerExample,
    build_reranker_training_data,
)
from citecheck.reranker.loss import MultiObjectiveLoss
from citecheck.reranker.model import CrossEncoderReranker
from citecheck.reranker.train import train_reranker

__all__ = [
    "CrossEncoderReranker",
    "MultiObjectiveLoss",
    "RerankerDataset",
    "RerankerExample",
    "build_reranker_training_data",
    "train_reranker",
]
