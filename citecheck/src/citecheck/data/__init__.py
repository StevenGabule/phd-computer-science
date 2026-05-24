"""CiteCheck data layer.

Re-exports the main loader functions and client classes for case-law corpora
(CAP), the CourtListener API, downstream evaluation benchmarks (LegalBench-RAG,
CUAD), and the CiteCheck eval set itself.

Typical usage::

    from citecheck.data import (
        CourtListenerClient,
        download_cap_bulk,
        load_cuad,
        load_eval_set,
        load_legalbench_rag,
    )
"""
from __future__ import annotations

from citecheck.data.benchmarks import (
    BenchmarkExample,
    load_cuad,
    load_legalbench_rag,
    to_jsonl,
)
from citecheck.data.cap_loader import (
    CAPOpinion,
    download_cap_bulk,
    iter_cap_opinions,
    parse_cap_jsonl_to_parquet,
)
from citecheck.data.cl_client import (
    CLOpinion,
    CourtListenerClient,
    RateLimitedError,
)
from citecheck.data.eval_set import (
    CiteCheckExample,
    human_verify_subset,
    llm_prelabel,
    load_eval_set,
    save_eval_set,
    seed_from_charlotin,
)

__all__ = [
    # benchmarks
    "BenchmarkExample",
    "load_legalbench_rag",
    "load_cuad",
    "to_jsonl",
    # cap_loader
    "CAPOpinion",
    "download_cap_bulk",
    "parse_cap_jsonl_to_parquet",
    "iter_cap_opinions",
    # cl_client
    "CLOpinion",
    "CourtListenerClient",
    "RateLimitedError",
    # eval_set
    "CiteCheckExample",
    "load_eval_set",
    "save_eval_set",
    "seed_from_charlotin",
    "llm_prelabel",
    "human_verify_subset",
]
