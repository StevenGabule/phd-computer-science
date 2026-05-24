# CiteCheck

> Open benchmark and agentic-RAG method for verifiable US case-law citations.

This is the **code subproject** of a broader 18-month PhD CS application prep workspace. See the parent project's [`/README.md`](../README.md) for the full context. For research framing, see [`../project/problem_statement.md`](../project/problem_statement.md) (tight) and [`../project/citecheck_design.md`](../project/citecheck_design.md) (full implementation detail).

---

## What this is

CiteCheck is a three-stage agentic RAG pipeline that scores LLM-generated US case-law citations on three axes:

1. **Existence** — does the cited case resolve to a real opinion in CourtListener?
2. **Support** — does the resolved opinion entail the asserted proposition (NLI + human audit)?
3. **Jurisdictional validity** — is the citation from a binding or persuasive jurisdiction?

The method: hybrid BM25 + dense retrieval → Bluebook-structure-aware cross-encoder reranker → constrained-decoded citation emission verified against the CourtListener API in an agent tool loop with retraction-or-retry.

Real-world motivation: *Mata v. Avianca* (S.D.N.Y. 2023) sanctioned attorneys for ChatGPT-fabricated case citations; ~50 similar court orders followed (Charlotin tracker). Magesh et al. (2025) showed even proprietary tools hallucinate 17–33%. CiteCheck provides the open, reproducible counterpart.

## Status

**Phase 2 (Build) scaffold — May 2026.** Code structure is in place; data, indexes, models, and the eval set are not yet built. See [`../docs/superpowers/plans/2026-05-24-phd-prep-phase-2-build.md`](../docs/superpowers/plans/2026-05-24-phd-prep-phase-2-build.md) for the 26-task execution plan (Sep 2026 – Apr 2027).

## Quick start

```bash
# 1. Clone the parent workspace
git clone https://github.com/StevenGabule/phd-computer-science.git
cd phd-computer-science/citecheck

# 2. Set up Python environment (Python 3.11+)
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\Activate.ps1
pip install -e ".[dev]"

# 3. Configure API keys
cp .env.example .env
# Edit .env with your CourtListener key, HF token, wandb key, etc.

# 4. Run tests (none require network/GPU by default)
pytest

# 5. (When ready) Download data and build indexes
python scripts/download_cap.py              # ~100GB, multi-day
python scripts/build_bm25_index.py
python scripts/build_dense_index.py

# 6. Run a baseline
python scripts/run_baseline.py --baseline naive_rag --questions data/eval_v0.1.jsonl
```

## Repo layout

```
citecheck/
├── pyproject.toml          # build + dependencies + dev tools
├── .env.example            # API key template (copy to .env)
├── README.md               # this file
├── src/citecheck/
│   ├── __init__.py
│   ├── config.py           # paths, model names, hyperparameters
│   ├── data/               # data loaders (CAP, CourtListener, LegalBench-RAG, CUAD)
│   ├── retrieval/          # BM25, dense, fusion (RRF)
│   ├── reranker/           # cross-encoder + multi-objective loss + training
│   ├── agent/              # CitationResolver tool + constrained-decoding + verify loop
│   ├── baselines/          # vanilla, naive RAG, Self-RAG, CRAG, EL-RAG (reimpl)
│   └── eval/               # 7 metrics + LLM judge + experiment runner
├── scripts/                # one-off CLIs (download, indexing, train, run, evaluate)
└── tests/                  # pytest test suite (none require network/GPU by default)
```

## Compute and storage budget

| Resource | Estimate | Notes |
|---|---|---|
| GPU | 1 × 24GB consumer (RTX 4090 / A5000) | Phase 2 plan total: ~310 GPU-hours over 8 months |
| Storage | ~150 GB | CAP bulk (~100 GB) + indexes (~30 GB) + checkpoints (~20 GB) |
| Cloud bursts | Colab Pro A100 for reranker lambda sweep + full-corpus dense embedding | Optional but recommended |
| Cash | ~$2,180–$3,380 total | Annotator (~$2k-$3.2k) + APIs ($80) + Colab Pro ($80) |

## Citing this work

Not published yet. Target venue: NLLP @ EMNLP 2027. arXiv preprint planned Sep 2027.

## License

MIT. See [LICENSE](LICENSE) once added.
