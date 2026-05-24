# What Cannot Be Done by AI Alone for Phase 2

**Why this file exists:** Phase 2 of the 18-month PhD-prep plan (Sep 2026 – Apr 2027) is an 8-month execution phase. The scaffold (full `citecheck/` Python codebase) was created in a single chat session, but the actual *execution* of Phase 2 requires resources outside any AI assistant's capability.

This document makes those limits explicit so future contributors (including the user) know exactly what's scaffolded vs. what still requires human time, hardware, money, or network access.

---

## What was done by AI in the scaffold session

- `citecheck/` Python package: 49 files, ~7,000 lines, all syntax-valid
- 9 test files mocking all external dependencies (runnable on `make test` from a fresh checkout)
- 7 CLI scripts (download, indexing, training, evaluation, verification)
- pyproject.toml with pinned dependencies + CI workflow + Makefile + pre-commit
- Architecture and design docs
- 3 commits pushed to `origin/main` for the scaffold

## What CANNOT be done by AI for Phase 2 execution

| Task | Why it requires non-AI resources |
|---|---|
| **Download Caselaw Access Project bulk corpus (~100 GB)** | Multi-day network transfer; not feasible in a chat session |
| **Build BM25 + dense indexes** | Requires the downloaded corpus + multi-hour CPU/GPU time |
| **Construct the 500-question CiteCheck eval set** | Requires human legal annotation (or a paid annotator at ~$2k-$3.2k per Phase 2 plan estimate); a chat-session AI cannot ethically substitute for a JD-level legal reviewer |
| **Train the cross-encoder reranker** | Requires the training data + ~48 GPU-hours per λ value × 4 values = ~190 GPU-hours; physical GPU required |
| **Reproduce Self-RAG, CRAG, EL-RAG baselines** | Requires loading 7-13B parameter models + GPU time; ~30 GPU-hours total |
| **Run the full eval set through all baselines + CiteCheck** | Requires constructed eval set + all baselines + GPU + ~$50-100 in API costs for GPT-4o-mini ceiling baseline |
| **Human audit of 200-item subset** | Requires a human reviewer's actual judgments; cannot be synthesized |
| **Stability checks across 3 seeds** | Requires re-running the full eval set 3× = ~72 additional GPU-hours |
| **CourtListener API key + live queries** | Requires the user to register at courtlistener.com; rate limits apply |
| **Hire / coordinate an annotator** | Requires a real human partnership decision (Upwork hire, law-school collaborator, or self-only) |

## What the scaffold lets the user do TODAY (without execution)

- Read the code and understand the architecture (`citecheck/docs/architecture.md`)
- Run unit tests against mocked components (`cd citecheck && make test`)
- Walk through the demo notebook (`citecheck/notebooks/quickstart.ipynb`) with smoke fixtures
- Review milestone templates for M3/M4/M5 retrospectives
- Reference the paper outline draft (`docs/papers/citecheck_outline.md`) while doing deep reads
- Make the M2 lock decisions (`project/m2_lock_checklist.md`)
- Star advisors and customize cold emails (`outreach/email_variants/`)
- Begin the artifacts-by-Aug-2027 commitments (`applications/artifacts_strategy.md`)

## When Phase 2 actually begins (Sep 2026)

The Phase 2 plan (`docs/superpowers/plans/2026-05-24-phd-prep-phase-2-build.md`) sequences 26 tasks across 8 months. The first three tasks (15, 16, 17) are infrastructure setup that triggers the real-execution chain. Run them in order:

1. **Task 15 (Sep week 1):** `cd citecheck && pip install -e ".[dev]" && cp .env.example .env && python scripts/verify_scaffold.py` — confirms the scaffold survived dependency installation
2. **Task 16 (Sep weeks 2-4):** `python scripts/download_cap.py --jurisdictions us scotus federal_appellate` — starts the multi-day CAP download
3. **Task 17 (Sep week 4):** `python scripts/build_bm25_index.py --corpus-parquet data/cap_parquet --output-dir indexes/bm25`

After that point, you're executing Phase 2 in real terms. The scaffold's job is done.

## The phrase "complete Phase 2"

In the context of this codebase, "Phase 2 complete" means **the scaffold and all preparatory work are done** so the user can begin execution on Sep 1, 2026. It does NOT mean the 8 months of experiments, training, and writing have been compressed into a chat session — that's not physically possible.

The most a chat-session AI can do is what was done here: the scaffold, the docs, the templates, the test suite, the smoke fixtures, the paper outline, the milestone templates. The remaining 8 months of execution is the user's work, with AI assistance available throughout (e.g., debugging a failing baseline reproduction, drafting paper sections, brainstorming experiment designs).
