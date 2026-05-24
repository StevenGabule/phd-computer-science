"""Centralized configuration for CiteCheck.

All paths, model names, hyperparameters, and API endpoints live here so modules
import them rather than hard-coding values. Environment variables override
defaults; see ``.env.example`` for the full list.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

# Load .env from the citecheck/ directory (two levels up from this file)
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
load_dotenv(_PROJECT_ROOT / ".env")


@dataclass(frozen=True)
class Paths:
    """Local filesystem paths. Override via CITECHECK_*_DIR env vars."""

    project_root: Path = _PROJECT_ROOT
    data_dir: Path = field(
        default_factory=lambda: Path(
            os.environ.get("CITECHECK_DATA_DIR", _PROJECT_ROOT / "data")
        )
    )
    models_dir: Path = field(
        default_factory=lambda: Path(
            os.environ.get("CITECHECK_MODELS_DIR", _PROJECT_ROOT / "models")
        )
    )
    indexes_dir: Path = field(
        default_factory=lambda: Path(
            os.environ.get("CITECHECK_INDEXES_DIR", _PROJECT_ROOT / "indexes")
        )
    )
    runs_dir: Path = field(
        default_factory=lambda: Path(_PROJECT_ROOT / "runs")
    )

    @property
    def cap_raw(self) -> Path:
        return self.data_dir / "cap_raw"

    @property
    def cap_parquet(self) -> Path:
        return self.data_dir / "cap_parquet"

    @property
    def cl_cache(self) -> Path:
        return self.data_dir / "cl_cache"

    @property
    def eval_set(self) -> Path:
        return self.data_dir / "eval_v0.1.jsonl"

    @property
    def bm25_index(self) -> Path:
        return self.indexes_dir / "bm25"

    @property
    def dense_index(self) -> Path:
        return self.indexes_dir / "dense"


@dataclass(frozen=True)
class Models:
    """Model identifiers. Use HuggingFace Hub names."""

    # Generator (the LLM that emits citations)
    generator_primary: str = "meta-llama/Llama-3.1-8B-Instruct"
    generator_secondary: str = "Qwen/Qwen2.5-7B-Instruct"
    generator_stretch: str = "meta-llama/Llama-3.1-13B-Instruct"

    # Dense retriever (passage embedder)
    dense_encoder: str = "BAAI/bge-base-en-v1.5"
    dense_encoder_legal: str = "nlpaueb/legal-bert-base-uncased"

    # Cross-encoder reranker base (fine-tuned on legal data in Phase 2)
    reranker_base: str = "cross-encoder/ms-marco-MiniLM-L-12-v2"

    # NLI judge (for Citation Support F1)
    nli_judge: str = "MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli"

    # Hosted closed-API ceiling reference (uses OPENAI_API_KEY)
    closed_ceiling: str = "gpt-4o-mini"


@dataclass(frozen=True)
class Retrieval:
    """Retrieval hyperparameters."""

    bm25_top_k: int = 50
    dense_top_k: int = 50
    rrf_top_k: int = 20
    rrf_k_constant: int = 60   # standard RRF constant
    chunk_tokens: int = 512    # token chunk size for indexing
    chunk_overlap: int = 50


@dataclass(frozen=True)
class Reranker:
    """Reranker training hyperparameters."""

    max_length: int = 512
    batch_size: int = 16
    learning_rate: float = 2e-5
    epochs: int = 3
    lambda_sweep: tuple[float, ...] = (0.1, 0.3, 0.5, 1.0)
    warmup_ratio: float = 0.1
    hard_negative_ratio: float = 0.5  # fraction of hard negatives per positive
    train_triples_target: int = 20000


@dataclass(frozen=True)
class Agent:
    """Agent verification loop hyperparameters."""

    max_iterations: int = 3
    constrained_decoding: bool = True
    nli_entailment_threshold: float = 0.7
    cache_resolver_calls: bool = True


@dataclass(frozen=True)
class API:
    """External API configuration. Reads keys from environment via dotenv."""

    courtlistener_base: str = "https://www.courtlistener.com/api/rest/v4"
    courtlistener_rate_limit_per_hour: int = 5000
    cl_api_key: str = field(default_factory=lambda: os.environ.get("CL_API_KEY", ""))

    hf_token: str = field(default_factory=lambda: os.environ.get("HF_TOKEN", ""))
    openai_api_key: str = field(default_factory=lambda: os.environ.get("OPENAI_API_KEY", ""))
    openrouter_api_key: str = field(default_factory=lambda: os.environ.get("OPENROUTER_API_KEY", ""))
    anthropic_api_key: str = field(default_factory=lambda: os.environ.get("ANTHROPIC_API_KEY", ""))

    wandb_api_key: str = field(default_factory=lambda: os.environ.get("WANDB_API_KEY", ""))
    wandb_project: str = field(default_factory=lambda: os.environ.get("WANDB_PROJECT", "citecheck"))
    wandb_entity: str = field(default_factory=lambda: os.environ.get("WANDB_ENTITY", ""))


# Singleton-style accessors so callers can `from citecheck.config import PATHS`
PATHS = Paths()
MODELS = Models()
RETRIEVAL = Retrieval()
RERANKER = Reranker()
AGENT = Agent()
API_CFG = API()


def ensure_dirs() -> None:
    """Create local data/model/index directories if missing.

    Safe to call multiple times. Intended for use at script entry points.
    """
    for d in (PATHS.data_dir, PATHS.models_dir, PATHS.indexes_dir, PATHS.runs_dir):
        d.mkdir(parents=True, exist_ok=True)
