# CiteCheck Architecture (v0.1 scaffold)

> Companion to `../project/citecheck_design.md` (research framing) and
> `../docs/superpowers/plans/2026-05-24-phd-prep-phase-2-build.md` (execution plan).

This document describes the code structure: how the modules in
`citecheck/src/citecheck/` fit together, what the data flow looks like at
inference time, and which classes own which responsibilities.

---

## Module map

```
src/citecheck/
├── config.py          # PATHS, MODELS, RETRIEVAL, RERANKER, AGENT, API_CFG
├── cli.py             # `citecheck` CLI dispatcher → scripts/
├── data/              # Datasets and external clients
│   ├── cap_loader.py        # Caselaw Access Project bulk loader → parquet
│   ├── cl_client.py         # CourtListener REST API v4 client (cached)
│   ├── benchmarks.py        # LegalBench-RAG + CUAD loaders → BenchmarkExample
│   └── eval_set.py          # CiteCheckExample + seed/prelabel/audit helpers
├── retrieval/         # First-stage retrieval
│   ├── bm25.py              # pyserini + Lucene
│   ├── dense.py             # sentence-transformers + FAISS
│   └── fusion.py            # Reciprocal Rank Fusion + HybridRetriever
├── reranker/          # Second-stage reranker (Bluebook-structure-aware)
│   ├── dataset.py           # RerankerDataset + training-data construction
│   ├── model.py             # CrossEncoderReranker (shared backbone, two heads)
│   ├── loss.py              # MultiObjectiveLoss (relevance + groundedness)
│   └── train.py             # Training loop with QLoRA
├── agent/             # Third-stage verify loop (THE novel contribution)
│   ├── citation_resolver.py # CitationResolver (eyecite + CL + NLI)
│   ├── grammar.py           # BluebookGrammar (constrained decoding)
│   └── loop.py              # VerifyLoop (orchestrator)
├── baselines/         # Comparison systems
│   ├── protocol.py          # BaselineProtocol (typing.Protocol)
│   ├── vanilla.py           # No retrieval
│   ├── naive_rag.py         # BM25 + stuff context
│   ├── self_rag.py          # Asai et al. 2023
│   ├── crag.py              # Yan et al. 2024
│   └── el_rag.py            # Wankhade 2026 reimpl (closed-access — best effort)
└── eval/              # Metrics + judge + runner
    ├── metrics.py           # 7 metrics (Resolution, Fabrication, Support F1, etc.)
    ├── judge.py             # LLMJudge (dual-judge with kappa)
    └── runner.py            # EvaluationRunner (iter + measure + report)
```

## Inference data flow

```
                ┌──────────────────────────────────────────────────────┐
                │   question: "Did the court hold X under NY law?"      │
                └─────────────────────────┬────────────────────────────┘
                                          │
                              ┌───────────▼────────────┐
                              │  HybridRetriever       │
                              │  BM25 ⊕ Dense ⊕ RRF    │  (retrieval/)
                              └───────────┬────────────┘
                                          │ top-20 passages
                              ┌───────────▼────────────┐
                              │ CrossEncoderReranker   │  (reranker/)
                              │ score = rel + λ·ground │
                              └───────────┬────────────┘
                                          │ top-5 reranked
                              ┌───────────▼────────────┐
                              │  Generator + Grammar   │  (agent/grammar.py)
                              │  Llama-3.1-8B QLoRA    │
                              │  constrained-decoded   │
                              │  Bluebook citations    │
                              └───────────┬────────────┘
                                          │ answer with cited authorities
                              ┌───────────▼────────────┐
                              │   CitationResolver     │  (agent/citation_resolver.py)
                              │   eyecite → CL → NLI   │
                              └───────────┬────────────┘
                                          │ per-citation VerificationResult
                                          │ (VERIFIED / UNRESOLVABLE /
                                          │  NON_SUPPORTING / UNKNOWN)
                                          │
                              ┌───────────▼────────────┐
                              │  Any failures and      │
                              │  iterations remain?    │
                              │  → re-retrieve         │ (agent/loop.py)
                              │  Otherwise → return    │
                              └───────────┬────────────┘
                                          │
                                          ▼
                              ┌────────────────────────┐
                              │ AnswerWithCitations    │
                              │ {answer, [citations    │
                              │  with statuses],       │
                              │  iterations_used}      │
                              └────────────────────────┘
```

## Training data flow

The reranker is the only component fine-tuned in Phase 2 (QLoRA on a cross-encoder).
Training data is mined from the eval set + BM25 hits:

```
   eval examples ─── BM25 top-k ──── eyecite parse ─── CL resolve
                                                            │
                                                            ▼
                                  positive: gold-citation match
                                  hard-neg: similar passage, wrong cite
                                  easy-neg: random unrelated passage
                                                            │
                                                            ▼
                                  RerankerExample(query, passage,
                                                  relevance_label,
                                                  groundedness_label)
                                                            │
                                                            ▼
                                  train_reranker(λ ∈ {0.1, 0.3, 0.5, 1.0})
                                                            │
                                                            ▼
                                  best λ on val → use for inference
```

## Key design choices

### Shared-backbone, two-head reranker

`CrossEncoderReranker` has a single transformer backbone and two regression
heads (relevance, groundedness). The combined score is `relevance + λ * groundedness`.
This avoids a Cartesian product of fine-tunes (one per λ) at scoring time
while still letting us sweep λ in training.

### Live-registry verification vs. post-hoc detection

The novel design choice (vs. HalluGraph and similar): verification happens
**inside the generation loop**, not as a post-hoc audit. Unresolvable
citations trigger a retraction-or-retry rather than just being flagged. This
is more expensive per query but eliminates an entire class of "we noticed but
shipped it anyway" failures.

### Constrained Bluebook decoding

Citations are emitted via an `outlines`-regex constraint that forces
well-formed Bluebook structure (`{vol} {reporter} {page} ({court} {year})`).
This makes downstream `eyecite` parsing 100% reliable and eliminates a class
of failures where the generator emits a citation-shaped string that's
syntactically invalid.

### Provider-agnostic generator

The `generator` argument in `VerifyLoop` and baselines is a callable
`(prompt: str) -> str`. This lets us swap between local transformers (Llama,
Qwen via QLoRA), OpenRouter, OpenAI direct, or Anthropic without changing
pipeline code.

## What's NOT in v0.1

- Multi-jurisdiction grammar (US Supreme Court + federal appellate only)
- Statute citations (only case-law citations)
- Parallel citations ("X v. Y, 1 F.3d 1, 2 F. Supp. 3d 3 (...)")
- Signal phrases ("see", "but see", "cf.", etc.)
- State court coverage beyond what CourtListener provides
- Real-time updates to the CAP index
- Multi-language legal corpora

These are all tracked in the Phase 2 plan's M5/M6 "future work" notes.
