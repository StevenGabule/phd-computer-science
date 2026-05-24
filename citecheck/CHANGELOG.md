# Changelog

All notable changes to the CiteCheck codebase will be documented here.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning: [SemVer](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added — Phase 2 scaffold (2026-05-25)

Initial code skeleton for the Phase 2 build phase (Sep 2026 – Apr 2027).
None of the code has been executed end-to-end yet; data, indexes, model
checkpoints, and the constructed eval set are all out of scope for the scaffold.

Foundation:
- `pyproject.toml` — package manifest with pinned dependencies
- `README.md` — quickstart + repo layout
- `LICENSE` — MIT
- `.env.example` — API key template
- `src/citecheck/__init__.py`, `config.py` — package init + central configuration
- `src/citecheck/cli.py` — `citecheck` CLI dispatcher routing to `scripts/`

Module code (written by parallel research agents on the same date):
- `src/citecheck/data/` — CAP loader, CourtListener client, benchmark loaders, eval-set helpers
- `src/citecheck/retrieval/` — BM25 (pyserini), dense (BGE + FAISS), RRF fusion
- `src/citecheck/reranker/` — cross-encoder with multi-objective loss + training loop
- `src/citecheck/agent/` — CitationResolver tool, Bluebook grammar, verify loop
- `src/citecheck/baselines/` — vanilla, naive RAG, Self-RAG, CRAG, EL-RAG reimpl
- `src/citecheck/eval/` — 7 metrics, LLM judge, evaluation runner

Scripts (`scripts/`):
- `download_cap.py`, `build_bm25_index.py`, `build_dense_index.py`
- `train_reranker.py`, `run_baseline.py`, `run_citecheck.py`, `evaluate.py`

Tests (`tests/`):
- pytest suite with mocked external APIs; runnable on a fresh checkout
  without network/GPU/data via `pytest -m "not slow and not gpu and not network"`

### Known limitations of v0.1 scaffold

- LegalBench-RAG schema assumptions may need adjustment when the actual dataset is loaded.
- EL-RAG (Wankhade 2026) reimplementation is from the abstract only; closed-access paper.
- Bluebook grammar regex covers ~80% of common citations; parallel/statute/signal citations are TODO.
- `CitationResolver.verify` requires a downloaded NLI model on first call.
- Reranker training data construction (`build_reranker_training_data`) makes real CourtListener API calls and will be rate-limited at scale.
- All scripts have working CLIs but require local data + API keys + GPU to actually execute meaningful work.

## [0.1.0] — Planned

Phase 2 milestone outputs against the Phase 2 plan:

- M3 (Nov 2026): baseline reproduction complete; LegalBench-RAG numbers match published.
- M4 (Feb 2027): novel contribution (Bluebook-aware reranker + verify loop) prototyped end-to-end.
- M5 (May 2027): full experiments + ablations on 500-item CiteCheck eval set.

Versioning: bump to 0.1.0 when the v0.1 eval set + baselines + CiteCheck pipeline can run end-to-end and produce the headline Resolution Rate / Fabrication Rate metrics.
