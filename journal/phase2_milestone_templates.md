# Phase 2 Milestone Retrospective Templates

**Use:** Copy the relevant section to `journal/weekly.md` (or a dedicated milestone file) when each milestone closes. Templates exist for M3 (Nov 2026), M4 (Feb 2027), and M5 partial (Apr 2027). Phase 2 also closes with a phase-level retrospective.

Templates correspond to Phase 2 plan tasks: 23 (M3), 32 (M4), 39 (M5 partial).

---

## M3 Retrospective Template — End of November 2026

**Use after Phase 2 Task 23 closes the baseline-reproduction milestone.**

```markdown
## M3 Milestone Retrospective — 2026-11-30

### Status
- Milestone: M3 (Baseline reproduction)
- On track for M4? [Y / N + reason]
- Decision: lock or revise problem statement based on baseline numbers

### Baselines reproduced
| Baseline | Reproduction status | Numbers vs. published |
|---|---|---|
| Vanilla Llama-3.1-8B | [REPRODUCED / FAILED] | LegalBench-RAG: ? (vs paper: ?) |
| Naive RAG (BM25 + BGE) | [REPRODUCED / FAILED] | LegalBench-RAG: ? (vs paper: ?) |
| Self-RAG | [REPRODUCED / FAILED / SKIPPED] | LegalBench-RAG: ? (vs Asai 2023: ?) |
| CRAG | [REPRODUCED / FAILED / SKIPPED] | LegalBench-RAG: ? (vs Yan 2024: ?) |
| EL-RAG (reimpl) | [REPRODUCED / FAILED / SKIPPED] | LegalBench-RAG: ? (vs Wankhade 2026: ?) |

### GPU-hours actually used
- Plan estimate (Months 1-3): ~85 GPU-hours
- Actual: ?
- Variance reason: ?

### What went well
- ...

### What stalled
- ...

### Adjustments for Phase 2 Months 4-5
- ...

### Lock-or-revise decision (the one that matters)
- **Problem statement still locks at CiteCheck v1.0?** [Y / N]
- **If N**: trigger Plan B niche per `project/candidates.md`. The fallback is Candidate A (ContractTraj-Bench). The cost of switching now is ~3 weeks of re-scoping; the cost of switching later is much higher.
- **If Y**: write the M3 entry in `journal/decisions.md` confirming the lock and proceed to Task 24 (eval-set construction).

### New papers from arXiv since M2 lock (re-search)
- ?

### Recommended changes to citecheck/ codebase based on Month 1-3 learnings
- ?
```

---

## M4 Retrospective Template — End of February 2027

**Use after Phase 2 Task 32 closes the novel-contribution-prototyped milestone.**

```markdown
## M4 Milestone Retrospective — 2027-02-28

### Status
- Milestone: M4 (Novel contribution prototyped + pilot eval)
- On track for M5? [Y / N + reason]

### Novel contribution: Bluebook-aware reranker + agent verify loop
- Reranker fine-tuned across λ ∈ {0.1, 0.3, 0.5, 1.0}: [DONE / IN_PROGRESS]
- Best-λ ablation results (pilot 50 questions):
  | λ | Citation Resolution Rate | Citation Support F1 | Latency p95 |
  |---|---|---|---|
  | 0.1 | ? | ? | ? |
  | 0.3 | ? | ? | ? |
  | 0.5 | ? | ? | ? |
  | 1.0 | ? | ? | ? |
- Selected λ for full experiments: ?
- VerifyLoop integration: [DONE / IN_PROGRESS / BLOCKED]

### Eval set construction (Task 24-26)
- v0.1 eval set size: ? / 500 target
- Annotator path actually taken: [PAID UPWORK JD / LAW STUDENT COLLABORATOR / SELF-ONLY ADVERSARIAL]
- Annotator cost actually spent: $?
- Inter-annotator kappa on 50-item gold subset: ?

### Pilot evaluation on 50 questions
- CiteCheck vs. best baseline:
  - Fabrication rate improvement: ?
  - Citation Support F1 improvement: ?
  - Latency overhead: ?

### What went well
- ...

### What stalled
- ...

### Adjustments for Phase 2 Months 6-8
- ...

### Risk check
- Is anyone else publishing a competing benchmark (Butler & Butler follow-up, Magesh extension, new arXiv)?
- Did the eval-set construction balloon beyond 500 items (scope creep)?
- Is the reranker training within budget?

### Decision: continue to full experiments (Task 33) or re-scope?
- **Continue if:** pilot shows CiteCheck beats best baseline by ≥5 percentage points on Fabrication Rate AND the eval set is at ≥300 items.
- **Re-scope if:** pilot improvement is within noise OR eval set is below 200 items.
```

---

## M5 Partial Retrospective Template — End of April 2027

**Use at end of Phase 2 (full M5 closes in Phase 3 Month 1).**

```markdown
## M5 Partial Retrospective — 2027-04-30 (Phase 2 Closeout)

### Status
- Milestone: M5 (Full experiments + ablations + stability checks) — PARTIAL
- Phase 3 kickoff date: 2027-05-03

### Full experiments completed (Task 33)
- All baselines × CiteCheck × full eval set: [DONE / IN_PROGRESS]
- GPU-hours consumed for experiments: ?
- Cash spent for closed-API ceiling (GPT-4o-mini): $?

### Headline results (Table 1 draft)
| System | Citation Resolution Rate | Fabrication Rate | Citation Support F1 | Jurisdictional Validity | Latency p95 (s) | Tokens/query |
|---|---|---|---|---|---|---|
| Vanilla Llama-3.1-8B | ? | ? | ? | ? | ? | ? |
| Naive RAG | ? | ? | ? | ? | ? | ? |
| Self-RAG | ? | ? | ? | ? | ? | ? |
| CRAG | ? | ? | ? | ? | ? | ? |
| EL-RAG (reimpl) | ? | ? | ? | ? | ? | ? |
| GPT-4o-mini + web | ? | ? | ? | ? | ? | ? |
| **CiteCheck (ours)** | ? | ? | ? | ? | ? | ? |

### Ablations (Task 34)
- Without reranker: [ran / pending]
- Without CitationResolver tool: [ran / pending]
- Without constrained decoding: [ran / pending]
- Per-jurisdiction breakdown: [ran / pending]

### Human audit (Task 35)
- 200-item Citation Support F1 (human-rated): ?
- 100-item Answer Utility (Likert 1-5 mean): ?
- Inter-judge kappa (LLM judge vs. human): ?

### Stability (Task 36)
- 3 seeds run: [Y / N]
- Std dev on headline metrics: ?
- Is CiteCheck advantage outside 1σ of best baseline? [Y / N — critical]

### What's left for Phase 3 (Month 1 of Phase 3 = May 2027)
- Final result tables
- Paper draft v0 (build on `docs/papers/citecheck_outline.md`)
- arXiv preprint preparation
- Internal review cycle

### Energy level / confidence (1-10): ?

### Anything to roll back or re-scope before Phase 3? [Y / N + details]
```

---

## Phase 2 Closeout Template (overall)

**Use at end of Phase 2 (2027-04-30) for the full phase retrospective.**

```markdown
## Phase 2 Closeout — End of April 2027

### Status
- Phase 2 status: COMPLETE
- Total months elapsed: 8 (Sep 2026 – Apr 2027)
- Phase 3 kickoff: 2027-05-03

### Total resources actually spent
- GPU-hours: ? (vs. Phase 2 plan estimate ~310)
- Cash: $? (vs. Phase 2 plan estimate ~$2,180-$3,380)
- Hours of focused work: ?

### What worked
- ...

### What didn't work
- ...

### Lessons that change Phase 3 plan
- ...

### Key artifacts produced
- CiteCheck v0.1 benchmark: ? questions, public on Hugging Face Hub: [URL]
- Trained reranker checkpoint: best λ = ?, on Hugging Face: [URL]
- Experiment results JSONLs in `citecheck/runs/`
- Paper outline → draft v0 (in Phase 3 Month 1)

### Confidence in submission for NLLP @ EMNLP 2027
- Expected workshop deadline: Jun/Jul 2027
- Days of paper-writing time available in Phase 3 Months 1-2: ?
- Confidence: [HIGH / MEDIUM / LOW + reason]

### Anything to flag for advisors at this point
- ...
```
