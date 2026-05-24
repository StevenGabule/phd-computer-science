"""Verify the CiteCheck v0.1 scaffold is structurally complete.

Run this after a fresh checkout to confirm every expected file exists and
every public module imports without error. Does NOT exercise external APIs,
GPU code, or actual model loading — just structural integrity.

Usage::

    python scripts/verify_scaffold.py
    # exits 0 on success, 1 on missing files or import failures
"""
from __future__ import annotations

import importlib
import sys
from pathlib import Path

EXPECTED_FILES = [
    # Foundation
    "pyproject.toml",
    "README.md",
    "LICENSE",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "Makefile",
    ".env.example",
    "src/citecheck/__init__.py",
    "src/citecheck/cli.py",
    "src/citecheck/config.py",
    # Data layer
    "src/citecheck/data/__init__.py",
    "src/citecheck/data/cap_loader.py",
    "src/citecheck/data/cl_client.py",
    "src/citecheck/data/benchmarks.py",
    "src/citecheck/data/eval_set.py",
    # Retrieval
    "src/citecheck/retrieval/__init__.py",
    "src/citecheck/retrieval/bm25.py",
    "src/citecheck/retrieval/dense.py",
    "src/citecheck/retrieval/fusion.py",
    # Reranker
    "src/citecheck/reranker/__init__.py",
    "src/citecheck/reranker/dataset.py",
    "src/citecheck/reranker/model.py",
    "src/citecheck/reranker/loss.py",
    "src/citecheck/reranker/train.py",
    # Agent
    "src/citecheck/agent/__init__.py",
    "src/citecheck/agent/citation_resolver.py",
    "src/citecheck/agent/grammar.py",
    "src/citecheck/agent/loop.py",
    # Baselines
    "src/citecheck/baselines/__init__.py",
    "src/citecheck/baselines/protocol.py",
    "src/citecheck/baselines/vanilla.py",
    "src/citecheck/baselines/naive_rag.py",
    "src/citecheck/baselines/self_rag.py",
    "src/citecheck/baselines/crag.py",
    "src/citecheck/baselines/el_rag.py",
    # Eval
    "src/citecheck/eval/__init__.py",
    "src/citecheck/eval/metrics.py",
    "src/citecheck/eval/judge.py",
    "src/citecheck/eval/runner.py",
    # Scripts
    "scripts/download_cap.py",
    "scripts/build_bm25_index.py",
    "scripts/build_dense_index.py",
    "scripts/train_reranker.py",
    "scripts/run_baseline.py",
    "scripts/run_citecheck.py",
    "scripts/evaluate.py",
    # Tests
    "tests/conftest.py",
    "tests/test_config.py",
    "tests/test_data.py",
    "tests/test_retrieval.py",
    "tests/test_agent.py",
    "tests/test_baselines.py",
    "tests/test_metrics.py",
    "tests/test_eval_runner.py",
]

EXPECTED_IMPORTS = [
    "citecheck",
    "citecheck.config",
    "citecheck.cli",
    "citecheck.data",
    "citecheck.retrieval",
    "citecheck.reranker",
    "citecheck.agent",
    "citecheck.baselines",
    "citecheck.eval",
]


def main() -> int:
    citecheck_root = Path(__file__).resolve().parent.parent
    missing_files: list[str] = []
    for rel in EXPECTED_FILES:
        if not (citecheck_root / rel).exists():
            missing_files.append(rel)

    print(f"Checking {len(EXPECTED_FILES)} expected files...")
    if missing_files:
        print(f"  MISSING ({len(missing_files)}):")
        for m in missing_files:
            print(f"    - {m}")
    else:
        print(f"  All {len(EXPECTED_FILES)} files present.")

    print(f"\nChecking {len(EXPECTED_IMPORTS)} module imports...")
    failed_imports: list[tuple[str, str]] = []
    for mod in EXPECTED_IMPORTS:
        try:
            importlib.import_module(mod)
            print(f"  OK   {mod}")
        except Exception as e:
            failed_imports.append((mod, repr(e)))
            print(f"  FAIL {mod}: {e!r}")

    print()
    if missing_files or failed_imports:
        print(f"FAILED: {len(missing_files)} missing files, {len(failed_imports)} failed imports")
        return 1
    print("All structural checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
