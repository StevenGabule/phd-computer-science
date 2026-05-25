"""Tests for citecheck.config."""
from __future__ import annotations

from pathlib import Path


def test_imports_cleanly():
    from citecheck.config import (
        AGENT,
        API_CFG,
        MODELS,
        PATHS,
        RERANKER,
        RETRIEVAL,
        ensure_dirs,
    )

    assert PATHS is not None
    assert MODELS is not None
    assert RETRIEVAL is not None
    assert RERANKER is not None
    assert AGENT is not None
    assert API_CFG is not None
    assert callable(ensure_dirs)


def test_paths_are_pathlib():
    from citecheck.config import PATHS

    assert isinstance(PATHS.project_root, Path)
    assert isinstance(PATHS.data_dir, Path)
    assert isinstance(PATHS.models_dir, Path)
    assert isinstance(PATHS.indexes_dir, Path)
    assert isinstance(PATHS.runs_dir, Path)


def test_paths_derived_properties():
    from citecheck.config import PATHS

    assert PATHS.cap_raw.name == "cap_raw"
    assert PATHS.cap_parquet.name == "cap_parquet"
    assert PATHS.cl_cache.name == "cl_cache"
    assert PATHS.eval_set.suffix == ".jsonl"
    assert PATHS.bm25_index.parent == PATHS.indexes_dir
    assert PATHS.dense_index.parent == PATHS.indexes_dir


def test_models_have_expected_attributes():
    from citecheck.config import MODELS

    for attr in (
        "generator_primary",
        "generator_secondary",
        "dense_encoder",
        "reranker_base",
        "nli_judge",
        "closed_ceiling",
    ):
        assert hasattr(MODELS, attr), f"MODELS missing {attr}"
        value = getattr(MODELS, attr)
        assert isinstance(value, str) and value, f"MODELS.{attr} is empty"


def test_retrieval_hyperparameters():
    from citecheck.config import RETRIEVAL

    assert RETRIEVAL.bm25_top_k > 0
    assert RETRIEVAL.dense_top_k > 0
    assert RETRIEVAL.rrf_top_k > 0
    assert RETRIEVAL.rrf_k_constant > 0
    assert RETRIEVAL.chunk_tokens > 0


def test_reranker_lambda_sweep_is_tuple():
    from citecheck.config import RERANKER

    assert isinstance(RERANKER.lambda_sweep, tuple)
    assert len(RERANKER.lambda_sweep) > 0
    assert all(0 <= x <= 10 for x in RERANKER.lambda_sweep)


def test_agent_iteration_cap():
    from citecheck.config import AGENT

    assert AGENT.max_iterations >= 1
    assert 0.0 <= AGENT.nli_entailment_threshold <= 1.0


def test_ensure_dirs_creates(tmp_path, monkeypatch):

    # Replace PATHS with a temp version
    monkeypatch.setenv("CITECHECK_DATA_DIR", str(tmp_path / "data"))
    monkeypatch.setenv("CITECHECK_MODELS_DIR", str(tmp_path / "models"))
    monkeypatch.setenv("CITECHECK_INDEXES_DIR", str(tmp_path / "indexes"))
    # Re-construct Paths after env mutation
    from citecheck.config import Paths

    new_paths = Paths()
    for d in (new_paths.data_dir, new_paths.models_dir, new_paths.indexes_dir):
        d.mkdir(parents=True, exist_ok=True)
        assert d.exists()


def test_api_cfg_endpoints():
    from citecheck.config import API_CFG

    assert API_CFG.courtlistener_base.startswith("https://")
    assert API_CFG.courtlistener_rate_limit_per_hour > 0
