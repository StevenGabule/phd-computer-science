# Deep-Read Priority Order

**Purpose:** The 56 papers in `reading_list.md` aren't equal in value. This file gives a specific reading sequence — tier 1 must-reads for M2 lock, tier 2 for Phase 2 baselines, tier 3 for breadth.

**Status:** Generated 2026-05-25 based on `taxonomy.md` clusters and the CiteCheck primary candidate. Revise if the candidate changes at M2.

---

## Tier 1 — Must-read for M2 lock (10 papers, target Jun-Jul 2026)

Read these in this order; each takes ~3-4 hours for deep notes.

| # | Paper | Why now (CiteCheck specifically) | Estimated hours |
|---|---|---|---|
| 1 | **Quevedo et al. 2024 — Legal NLP Survey 2015-2022** (reading_list #28) | Foundational context — fastest path to mental model of where legal NLP has been and where the open problems are. Read first. | 6 (it's a survey) |
| 2 | **Pipitone & Houir Alami 2024 — LegalBench-RAG** (reading_list #32) | Key benchmark Phase 2 M3 reproduces; sets the bar CiteCheck must beat. | 4 |
| 3 | **Magesh et al. 2025 — Hallucination-Free?** (reading_list #30) | Provides the 17-33% fabrication rate that anchors the SOP and motivates the work. | 3 |
| 4 | **Wankhade 2026 — EL-RAG** (reading_list #15) | Closest published competitor; CiteCheck must differentiate from this. CAS/FJI metrics likely inform our evaluation. | 4 |
| 5 | **Guha et al. 2022 — LegalBench** (reading_list #8) | Foundational benchmark; understand its structure and limitations to position our work. | 4 |
| 6 | **Choi et al. 2025 — CiteGuard** (reading_list #24) | Closest methodological cousin (citation attribution validation); we differ by being legal and live-registry-grounded. | 3 |
| 7 | **Choudhury et al. 2025 — CLAUSE** (reading_list #11) | Closest scoop risk — uses CUAD + ContractNLI + RAG for legal-reasoning auditing. Critical to read for differentiation strategy. | 3 |
| 8 | **Reuter et al. 2025 — SAC for legal RAG** (reading_list #10) | Phase 2 baseline (Task 18-22); understand summary-augmented chunking before reproducing. | 3 |
| 9 | **Asai et al. 2023 — Self-RAG** (reading_list #33) | Phase 2 baseline (Task 20); the canonical self-reflective RAG paper. | 4 |
| 10 | **Cheong et al. 2025 — AI for Access to Justice** (reading_list #31) | Provides the public-defender + access-to-justice narrative for the SOP motivation. | 2 |

**Tier 1 total:** ~36 hours. At 4 papers/week (2 per week × 2 evening slots), this is ~3 weeks of deep reading. Schedule June 8 – June 28.

---

## Tier 2 — Phase 2 baselines & comparators (10 papers, target Aug-Oct 2026)

Read in any order; needed before Phase 2 baseline reproduction (M3, Nov 2026).

| # | Paper | Why | Hours |
|---|---|---|---|
| 11 | Jeong et al. 2024 — Adaptive-RAG (#34) | Phase 2 baseline option; adaptive complexity routing | 3 |
| 12 | Gao et al. 2023 — ALCE (citation benchmark) (#35) | Canonical citation eval metrics; CiteCheck adapts these to Bluebook | 4 |
| 13 | Wu et al. 2025 — SourceCheckup (#37) | Medical analog of CiteCheck; near-perfect methodological template | 3 |
| 14 | Šavelka & Ashley 2023 — Zero-shot legal annotation (#13) | Establishes baseline LLM capability on legal text | 3 |
| 15 | Butler et al. 2025 — MLEB (#9) | Largest legal IR benchmark; jurisdictionally diverse — informs scope choice | 4 |
| 16 | Vaddi 2026 — Can small models reason about legal? (#14) | Validates 7B model feasibility on ContractNLI/CASEHOLD/ECTHR | 3 |
| 17 | Khan et al. 2026 — Reason and Verify (#39) | Cross-encoder reranking + rationale grounding; informs Phase 2 reranker design | 3 |
| 18 | Anand et al. 2026 — Self-CRAG (#44) | Comparison to Self-RAG; understand the corrective-RAG line | 3 |
| 19 | Zhang, Šavelka & Ashley 2025 — Overruling benchmark (#46) | Temporally-sensitive case-law reasoning; complements CiteCheck's verification | 3 |
| 20 | Gao et al. 2025 — RAGalyst (#42) | Automated human-aligned RAG eval; informs our judge-plus-spot-check protocol | 3 |

**Tier 2 total:** ~32 hours. Schedule across Aug-Oct 2026 (8 weeks at 4 hr/week of reading).

---

## Tier 3 — Breadth + agentic foundations (15 papers, target Phase 2)

Read selectively as Phase 2 tasks demand. Many are skim-then-deep-if-needed.

### Agent architectures & evaluation
- Shah 2026 — State of LLM agent evaluation (#6) — survey; informs eval-axis design
- Fu et al. 2025 — CATArena (#7) — tournament eval; informs trajectory comparison framing
- Wei et al. 2025 — Beyond ReAct (#21) — DAG planning; potential extension for our agent
- Zhang et al. 2025 — ReCAP (#22) — recursive planning
- Madahar 2025 — Lateral ToT (#23) — search breadth strategy

### Faithfulness & grounding
- Martin et al. 2024 — Semantic verification in RAG (#5) — Swiss-democracy work; methodological precedent
- Guan et al. 2025 — Faithfulness-aware ranking (#25) — multi-objective ranking template
- Clarizia et al. 2025 — Ontology-based RAG (#26) — alternative grounding approach

### Hallucination detection (CiteCheck-relevant)
- HalluGraph 2025 (#51) — post-hoc detector baseline for our evaluation
- UniFact 2025 (#52) — fact verification
- InterpDetect 2025 (#54) — interpretability for detection

### Domain RAG exemplars (for paper-shape reference)
- Low et al. 2025 — Clinical RAG + agentic (#1) — template for "domain RAG with agents"
- Yu et al. 2025 — YpathRAG (#2) — pathology RAG; dual-channel retrieval
- Yang et al. 2025 — Medical dual ranking (#3) — ColBERTv2-based; informs reranker choice
- Wang et al. 2025 — Enterprise LLM benchmark (#4) — multi-task structure

**Tier 3 total:** ~30 hours of skimming + selective deep reading.

---

## Tier 4 — Read only if needed (21 papers)

These are in the reading list for completeness and citation coverage but unlikely to need deep reads unless Phase 2 takes a specific direction. Examples:
- Graph-based RAG (LinearRAG #18, AGRAG #19, G2ConS #20) — only if CiteCheck adds KG-style retrieval
- Specific legal-domain papers outside the chosen scope (e.g., NyayaRAG, COLIEE-specific papers)
- Older foundational work (Sivapiran 2023 #16, Vidler 2023 #17) — useful for related-work section

---

## Reading workflow (per paper)

Use the template from Phase 1 Task 3 Step 3 — save each note to `literature/papers/{lastname}-{year}.md`:

```markdown
# {Author} {Year} — {Title}

**DOI:** {DOI}
**Date read:** YYYY-MM-DD
**Read depth:** {skim | deep-read}
**Relevance to CiteCheck:** {High | Medium | Low}

## Problem
[1-2 sentences]

## Method
[1 paragraph]

## Results
[Key numerical results + what they prove]

## Limitations
[Authors' acknowledged + my own observations]

## Questions / Ideas for CiteCheck
[Specific actionable transfer]

## Citations to follow up
[2-5 references to add to reading_list]
```

After each deep read, update the status in `literature/reading_list.md` from `pending` to `deep-read`.

---

## Calibration

A "deep read" is 3-4 hours for a typical 8-12 page workshop/conference paper, including taking structured notes. A survey paper can be 6-8 hours. Don't compress — the depth is the point.

If you find yourself rushing to "check off" papers, switch to skimming and demote them to Tier 4 status. Quality of 20 deep reads beats quantity of 50 skimmed.
