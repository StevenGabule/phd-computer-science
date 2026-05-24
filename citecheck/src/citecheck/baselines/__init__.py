"""CiteCheck baseline systems for Phase 2 comparison.

Five reference systems implementing :class:`~citecheck.baselines.protocol.BaselineProtocol`:

    * :class:`VanillaBaseline` — parametric LLM, no retrieval.
    * :class:`NaiveRAGBaseline` — retrieve top-k, stuff, generate.
    * :class:`SelfRAGBaseline` — Asai et al. 2023 reflection tokens.
    * :class:`CRAGBaseline` — Yan et al. 2024 retrieval evaluator.
    * :class:`ELRAGBaseline` — Wankhade 2026 reimplementation.

All five expose the same :meth:`answer` signature as :class:`citecheck.agent.VerifyLoop`,
so the eval harness can swap them transparently.
"""
from __future__ import annotations

from citecheck.baselines.crag import CRAGBaseline
from citecheck.baselines.el_rag import ELRAGBaseline
from citecheck.baselines.naive_rag import NaiveRAGBaseline
from citecheck.baselines.protocol import BaselineProtocol
from citecheck.baselines.self_rag import SelfRAGBaseline
from citecheck.baselines.vanilla import VanillaBaseline

__all__ = [
    "BaselineProtocol",
    "CRAGBaseline",
    "ELRAGBaseline",
    "NaiveRAGBaseline",
    "SelfRAGBaseline",
    "VanillaBaseline",
]
