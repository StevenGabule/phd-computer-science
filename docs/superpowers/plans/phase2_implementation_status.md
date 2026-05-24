# Phase 2 Implementation Status (v0.1 scaffold)

**Date:** 2026-05-25
**Status:** v0.1 scaffold complete — code structure in place, ready for Phase 2 (Sep 2026 – Apr 2027) execution. Nothing has been run end-to-end yet.

This document maps the 26 tasks in `docs/superpowers/plans/2026-05-24-phd-prep-phase-2-build.md` to the code that has been written.

---

## Coverage matrix

| Phase 2 Task | Plan section | Scaffold status | Files |
|---|---|---|---|
| **Task 15** Set up project repo / env / deps | Month 1: Sep 2026 | ✅ DONE | `pyproject.toml`, `Makefile`, `.env.example`, `LICENSE`, `CHANGELOG.md`, `CONTRIBUTING.md`, `src/citecheck/__init__.py`, `src/citecheck/config.py`, `src/citecheck/cli.py` |
| **Task 16** Index CAP bulk download (~100GB) | Month 1 | 🟡 SCRIPTS WRITTEN | `src/citecheck/data/cap_loader.py`, `scripts/download_cap.py`, `scripts/build_bm25_index.py`, `scripts/build_dense_index.py` (must download data and run) |
| **Task 17** Load LegalBench-RAG + CUAD into standardized format | Month 1 | ✅ DONE | `src/citecheck/data/benchmarks.py` |
| **Task 18** Reproduce vanilla Llama-3.1-8B-Instruct baseline | Month 2: Oct 2026 | 🟡 SCAFFOLD | `src/citecheck/baselines/vanilla.py`, `scripts/run_baseline.py` (must run with model) |
| **Task 19** Implement BM25 + bge-small naive RAG baseline | Month 2 | 🟡 SCAFFOLD | `src/citecheck/retrieval/bm25.py`, `src/citecheck/retrieval/dense.py`, `src/citecheck/retrieval/fusion.py`, `src/citecheck/baselines/naive_rag.py` |
| **Task 20** Implement Self-RAG baseline | Month 2 | 🟡 SCAFFOLD | `src/citecheck/baselines/self_rag.py` |
| **Task 21** Implement CRAG baseline | Month 3: Nov 2026 | 🟡 SCAFFOLD | `src/citecheck/baselines/crag.py` |
| **Task 22** Reimplement EL-RAG (Wankhade 2026) | Month 3 | 🟡 BEST-EFFORT SKELETON | `src/citecheck/baselines/el_rag.py` (closed-access paper; reimpl from abstract) |
| **Task 23** M3 milestone retrospective + lock decision | Month 3 | ⏳ FUTURE | (user task at M3) |
| **Task 24** Mine Charlotin AI-hallucination tracker | Month 4: Dec 2026 | 🟡 PARSE FUNCTION | `src/citecheck/data/eval_set.py::seed_from_charlotin` (raises if CSV missing; parses if present) |
| **Task 25** LLM-pre-label 500 candidate question / gold-citation pairs | Month 4 | 🟡 INTERFACE ONLY | `src/citecheck/data/eval_set.py::llm_prelabel` (stub — wire to OpenAI/OpenRouter/Anthropic) |
| **Task 26** Recruit + onboard annotator | Month 4 | ⏳ FUTURE | (user task; budget decision in `project/m2_lock_checklist.md`) |
| **Task 27** Implement Bluebook citation parser via eyecite | Month 5: Jan 2027 | ✅ DONE | `src/citecheck/agent/citation_resolver.py::CitationResolver.parse_bluebook` |
| **Task 28** Prototype CitationResolver agent tool | Month 5 | ✅ DONE | `src/citecheck/agent/citation_resolver.py::CitationResolver`, `src/citecheck/data/cl_client.py::CourtListenerClient` |
| **Task 29** Build constrained-decoding grammar for citation emission | Month 5 | ✅ DONE | `src/citecheck/agent/grammar.py::BluebookGrammar` |
| **Task 30** Fine-tune cross-encoder reranker with multi-objective loss | Month 6: Feb 2027 | 🟡 SCAFFOLD | `src/citecheck/reranker/dataset.py`, `model.py`, `loss.py`, `train.py`, `scripts/train_reranker.py` (must run on GPU with training data) |
| **Task 31** Integrate stages 1-2-3 into end-to-end CiteCheck agent | Month 6 | ✅ DONE | `src/citecheck/agent/loop.py::VerifyLoop`, `scripts/run_citecheck.py` |
| **Task 32** Pilot evaluation on 50 hand-picked questions | Month 6 | 🟡 SCAFFOLD | `src/citecheck/eval/runner.py`, `scripts/evaluate.py` |
| **Task 33** Run all baselines + CiteCheck on full eval set | Month 7: Mar 2027 | ⏳ FUTURE | (needs constructed eval set + GPU time) |
| **Task 34** Ablation studies | Month 7 | ⏳ FUTURE | (configurable via VerifyLoop init args; user runs) |
| **Task 35** Human audit of 200-item subset | Month 7 | 🟡 INTERFACE | `src/citecheck/eval/metrics.py::answer_utility` accepts `human_ratings` arg |
| **Task 36** Stability checks (multiple seeds) | Month 8: Apr 2027 | ⏳ FUTURE | (run scripts multiple times with --seed flag) |
| **Task 37** Per-task and per-jurisdiction breakdown | Month 8 | 🟡 PARTIAL | `src/citecheck/eval/metrics.py::EvaluationReport` supports breakdown dicts |
| **Task 38** Draft paper outline | Month 8 | ⏳ FUTURE | (user task; Phase 3 plan handles full paper) |
| **Task 39** M5 partial milestone retrospective | Month 8 | ⏳ FUTURE | (user task) |

**Legend:**
- ✅ DONE = Real, runnable code in the scaffold
- 🟡 SCAFFOLD / INTERFACE = Code structure in place; needs data, GPU, or wiring to run
- ⏳ FUTURE = User task during Phase 2 execution

---

## File inventory (TO BE UPDATED after all agents return)

| Module | Files | Total lines |
|---|---|---|
| Foundation | 9 | ~700 |
| `data/` | 5 | 1,186 (Agent I) |
| `retrieval/` | 4 | TBD (Agent J) |
| `reranker/` | 5 | TBD (Agent J) |
| `agent/` | 4 | TBD (Agent K) |
| `baselines/` | 6 | TBD (Agent K) |
| `eval/` | 4 | TBD (Agent L) |
| `scripts/` | 7 | TBD |
| `tests/` | 8 | TBD (Agent L) |

---

## Known limitations (v0.1 scaffold)

These are documented in `citecheck/CHANGELOG.md` and individual file docstrings:

1. **LegalBench-RAG schema assumptions** may need adjustment when the actual dataset is loaded (Agent I flag).
2. **CourtListener v4 citation-lookup response shape** assumed; verify on first live call (Agent I flag).
3. **`download_cap_bulk` full-corpus mode** requires URL scraping not yet implemented; jurisdiction-filtered mode works.
4. **`seed_from_charlotin`** requires the tracker CSV (not redistributed) on disk.
5. **`llm_prelabel`** is a stub — needs an OpenRouter/OpenAI/Anthropic client wired in.
6. **EL-RAG reimplementation** is from the abstract only; closed-access paper, no public code.
7. **Bluebook grammar** covers ~80% of common citations; parallel citations, statute citations, and signal phrases are TODO.
8. **`pyarrow`** dependency added post-scaffold per Agent I flag (parquet IO backend for pandas).

---

## What's next (when Phase 2 actually starts, Sep 2026)

1. Pre-Phase-2 (Jun-Aug 2026): user reads Tier 1 papers, locks problem statement at M2, makes annotator decision.
2. **Phase 2 kickoff (Sep 2026):** clone repo, install deps, configure `.env`, run `python scripts/verify_scaffold.py` to confirm structural integrity, then start executing Phase 2 tasks 15-39 in order.

---

## How this status doc gets updated

When new code lands or a task transitions from 🟡 SCAFFOLD → ✅ DONE → ⏳ RAN, update this file alongside `citecheck/CHANGELOG.md`. Log the change in `journal/decisions.md` as well.
