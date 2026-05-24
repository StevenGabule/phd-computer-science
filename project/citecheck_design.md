# CiteCheck — Detailed Design Reference

**Companion to:** `project/problem_statement.md` (the tight ~500-word version)
**Purpose:** Full implementation detail — method components, dataset notes, baseline citations, complete metric justifications, risk register with mitigations, and open scoping items for M2 lock.
**Version:** 0.1 (draft — refine during Phase 1 deep reads; lock at M2, 2026-08-31)
**Source:** Selected as primary candidate from `project/candidates.md` (vs. ContractTraj-Bench secondary; AgentLex-RAG deferred; LexEcoRAG dropped)

---

## 1. Architecture (3-stage pipeline)

### Stage 1 — Hybrid retrieve

- **Sparse:** BM25 via `pyserini` over a local Caselaw Access Project (CAP) bulk download (~100 GB; ~6.7M US opinions).
- **Dense:** `BAAI/bge-base-en-v1.5` (or `nlpaueb/legal-bert-base-uncased` for legal-tuned encoder, A/B compared).
- **Fusion:** Reciprocal Rank Fusion (RRF) on top-50 from each, return top-20.

### Stage 2 — Faithfulness-tuned rerank

- **Architecture:** Cross-encoder fine-tuned with a multi-objective loss:
  - L_relevance (standard query-doc relevance)
  - L_groundedness (does the candidate passage CONTAIN a citation whose resolved opinion text supports the claim, parsed via `eyecite`)
  - Combined: `L = L_relevance + λ * L_groundedness` (sweep λ ∈ {0.1, 0.3, 0.5, 1.0})
- **Training data:** Mine (query, doc, label) triples from eval-set candidates + Stage 1 BM25 hits, targeting 10k–30k triples with hard/easy negatives.
- **Output:** Top-5 reranked passages with their parsed Bluebook citation metadata.

### Stage 3 — Agent verify

- **Decoding:** Constrained-decoding grammar via `outlines` or `guidance` to force well-formed Bluebook citation emission.
- **Tool: `CitationResolver`** — queries the CourtListener API (with local CAP mirror as fallback for rate-limited scenarios). Returns: (exists ∈ {Y, N}, opinion_text if Y, court + year).
- **Verification logic:**
  - If `exists = N` → mark citation as unresolvable; agent loop re-retrieves (max k = 3 iterations) and re-generates with the unresolvable citation marked.
  - If `exists = Y` → run NLI entailment between the asserted proposition and the resolved opinion text; if non-entailment, mark as "exists but doesn't support" and re-retrieve.
- **Output:** Answer with citations annotated by verification status (verified / unresolvable / non-supporting).

### Novel contributions

The rerank loss (Bluebook-structure-aware) and the agent tool-loop (live registry verification) are the two novel contributions. All other components (BM25, BGE, cross-encoder, constrained decoding) are standard.

---

## 2. Datasets

| Dataset | Source | Size | Access | Use |
|---|---|---|---|---|
| Caselaw Access Project | https://case.law (bulk download) | ~6.7M US opinions | Public domain | Primary retrieval corpus |
| CourtListener API | https://www.courtlistener.com/api/ | PACER + opinions | Free; rate-limited (5,000 req/hr with API key) | Live verification + secondary index |
| LegalBench-RAG | HuggingFace (Pipitone & Alami 2024) | ~700 contract clauses, ~7k QA pairs | CC-BY | Task source for contract subset |
| CUAD | HuggingFace (Hendrycks et al. 2021) | 510 contracts, 13k clause annotations | CC-BY | Contract-citation subset |
| **Custom CiteCheck eval set** | Construct | ~500-1000 question / gold-citation pairs | To release CC-BY | Primary evaluation |

**Eval-set construction (~6-8 weeks solo, or 4 weeks with one annotator):**
- Seed adversarial examples from the Damien Charlotin AI-hallucination tracker (briefs cited in court orders with fabricated AI citations).
- LLM-pre-label 1,500 candidates using GPT-4o-mini, human-verify 500 to gold (Gray et al. 2024 methodology).
- Annotation budget options: paid Upwork JD ($2,000–$3,200), law-student collaborator (free, slower), or self-only with adversarial seeding (zero cost, lower coverage).

---

## 3. Baselines (named systems with citations)

| Baseline | Why include | Citation |
|---|---|---|
| Vanilla Llama-3.1-8B-Instruct (no retrieval) | Floor — what an LLM does with no grounding | Meta AI 2024 |
| Llama-3.1-8B + naive RAG (BM25 + top-k stuff) | The "obvious" first thing one tries | Lewis et al. 2020 |
| Self-RAG (Llama-3.1-8B) | Best-known self-reflective RAG | Asai et al. 2023 (arxiv:2310.11511) |
| CRAG | Corrective RAG with retrieval-then-evaluate | Yan et al. 2024 |
| EL-RAG reimplementation | Closest published legal RAG with multi-hop + alignment scoring | Wankhade 2026 (10.21203/rs.3.rs-8947587/v1) |
| HalluGraph (as post-hoc detector) | Tests whether post-hoc detection beats in-loop verification | Noël et al. 2025 |
| GPT-4o-mini with web search | Closed-API upper-bound reference | OpenAI |

EL-RAG re-implementation flagged as risky (closed-access paper; no public code). Fallback: implement faithfully from abstract; if not reproducible, document the gap and substitute a generic multi-hop baseline (IRCoT) for comparison.

---

## 4. Evaluation metrics (with justification)

| Metric | Justification |
|---|---|
| **Citation Resolution Rate** | % of emitted citations that resolve to a real CourtListener opinion. Machine-checkable, binary, primary safety metric tied directly to Mata-type harm. |
| **Fabrication Rate** | 1 − Resolution Rate; the headline number for press, SOPs, and adoption decisions. |
| **Citation Support F1** | Does the resolved opinion entail the asserted proposition. NLI-judged + 200-item human audit (NLI alone is too noisy on legal language). |
| **Jurisdictional Validity** | % of citations from a binding/persuasive jurisdiction for the question. Captures the "wrong-court" failure mode that Resolution Rate misses. |
| **Answer Utility** | Likert 1-5 from 100-item human audit. Detects over-retraction (system that refuses everything has perfect Resolution Rate but zero utility). |
| **Latency (p50, p95)** | Practical deployability on a single GPU. |
| **Tokens-per-query** | Deployment cost proxy; relevant to public-defender / pro-bono use cases. |

**Ablations to run (M5):**
- Without Stage 2 reranker (baseline retrieval + Stage 3 only)
- Without Stage 3 CitationResolver (retrieval + reranker only, post-hoc citation check)
- Without constrained decoding (free-form citation emission, post-hoc parse)
- Per-jurisdiction breakdown (federal appellate vs. Supreme Court vs. state if included)
- Multiple base models if compute allows (Qwen2.5-7B as secondary; Llama-3.1-13B as stretch)

---

## 5. Risk register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Annotation effort balloons past solo capacity | High | High | Cap at 500 items for v0.1; LLM pre-label + 50-item gold calibration; seed from Charlotin tracker (zero-cost adversarial); release v0.1 publicly |
| LLM-judge bias inflates NLI scores | Medium | Medium | Dual-judge (GPT-4o + Claude); disagreement-flagged manual review; report inter-judge kappa |
| 7B base too weak for non-trivial citation reasoning | Medium | Medium | Include Qwen2.5-14B-Instruct (4-bit QLoRA); Colab Pro A100 spot for harder runs |
| EL-RAG re-impl fails to match published numbers | High | Low | Document the gap; substitute IRCoT as a generic multi-hop baseline |
| Scoop by Butler & Butler 2026 "Legal RAG Bench" follow-up or Magesh extension | Medium | High | Differentiate on open-weight + open-data + reproducible-on-one-GPU + agentic-verifier combination; emphasize live-registry verification as the methodological contribution; target NLLP @ EMNLP 2026 if a sub-scope can ship early |
| CourtListener API rate limits | High | Medium | Mirror CAP bulk dump locally; cache resolver calls; batch where possible |
| Entailment NLI noisy on legal language | High | Medium | Report both NLI and human-audited subset; do not headline NLI-only numbers |
| No law-student annotator available | Medium | Medium | Fall back to Charlotin tracker mining (lower coverage but zero-partner risk); allocate paid budget |
| Cross-reference subtask depends on clean clause segmentation in CUAD | Medium | Low | Restrict v1 to 25 CUAD contract types with cleanest annotation |
| Project requires legal expertise the user lacks | Medium | High | Partner with a law student or legal professional for domain validation by M2; cite Šavelka/Ashley/Ho work for methodology grounding |

---

## 6. Open scoping items (resolve before M2 lock — see `project/m2_lock_checklist.md`)

- **Coverage cap:** federal appellate + Supreme Court only (recommended for v1) vs. include state appellate (doubles annotation effort).
- **Plan B niche** if M3 baseline reproduction reveals the gap has narrowed too far (e.g., Butler 2026 releases a competing benchmark in Aug/Sep 2026).
- **Annotator decision:** paid Upwork JD vs. law-student collaborator vs. self-only.
- **Workshop venue final pick:** confirm NLLP @ EMNLP 2027 deadline date when CFP publishes (typically May/Jun 2027).
- **Co-authorship policy with annotator** (decision Phase 2 plan flagged).
- **State courts:** confirm whether CourtListener has reliable coverage for the state-court tier if we expand scope.

---

## 7. Full references

1. Asai, A., Wu, Z., Wang, Y., et al. (2023). Self-RAG: Learning to retrieve, generate, and critique through self-reflection. *arXiv*. https://doi.org/10.48550/arxiv.2310.11511
2. Butler, A.-R., & Butler, U. (2026). Legal RAG Bench: an end-to-end benchmark for legal RAG. *arXiv*. https://doi.org/10.48550/arxiv.2603.01710
3. Cheong, I., Liu, P., & Stammbach, D. (2025). How Can AI Augment Access to Justice? Public Defenders' Perspectives on AI Adoption. *arXiv*. https://doi.org/10.48550/arxiv.2510.22933
4. Choi, Y. M., Guo, X., & Fung, Y. R. (2025). CiteGuard: Faithful Citation Attribution for LLMs via Retrieval-Augmented Validation. *arXiv*. https://doi.org/10.48550/arxiv.2510.17853
5. Choudhury, M. R., Chandramouli, A., & Anand, M. (2025). Better Call CLAUSE: A Discrepancy Benchmark for Auditing LLM Legal Reasoning Capabilities. *arXiv*. https://doi.org/10.48550/arxiv.2511.00340
6. Gao, T., Yen, H., Yu, J., & Chen, D. (2023). Enabling Large Language Models to Generate Text with Citations (ALCE). *EMNLP*. https://doi.org/10.18653/v1/2023.emnlp-main.398
7. Guan, T., Sun, S., & Chen, B. (2025). Faithfulness-Aware Multi-Objective Context Ranking for RAG. *Preprints*. https://doi.org/10.20944/preprints202512.1983.v1
8. Guha, N., Ho, D. E., Nyarko, J., et al. (2022). LegalBench: Prototyping a Collaborative Benchmark for Legal Reasoning. *arXiv*. https://doi.org/10.48550/arxiv.2209.06120
9. Hendrycks, D., Burns, C., Chen, A., & Ball, S. (2021). CUAD: An Expert-Annotated NLP Dataset for Legal Contract Review. *NeurIPS Datasets and Benchmarks*. https://doi.org/10.48550/arxiv.2103.06268
10. Magesh, V., Surani, F., & Dahl, M. (2025). Hallucination-Free? Assessing the Reliability of Leading AI Legal Research Tools. *J. Empirical Legal Studies*, 22(2), 216-242. https://doi.org/10.1111/jels.12413
11. *Mata v. Avianca, Inc.*, 22-cv-1461 (S.D.N.Y. June 22, 2023) — sanction order for ChatGPT-fabricated case citations.
12. Noël, V., Seidou, E. Y., & Capo-Chichi, C. K. (2025). HalluGraph: Auditable Hallucination Detection for Legal RAG Systems via Knowledge Graph Alignment. *arXiv*. https://doi.org/10.48550/arxiv.2512.01659
13. Pipitone, N., & Houir Alami, G. (2024). LegalBench-RAG: A Benchmark for Retrieval-Augmented Generation in the Legal Domain. *arXiv*. https://doi.org/10.48550/arxiv.2408.10343
14. Reuter, M., Lingenberg, T., & Liepiņa, R. (2025). Towards Reliable Retrieval in RAG Systems for Large Legal Datasets. *arXiv*. https://doi.org/10.48550/arxiv.2510.06999
15. Wankhade, N. W. (2026). EL-RAG: Explainable Retrieval-Augmented Generation Framework for Evidence-Aligned and Faithful Legal Reasoning. https://doi.org/10.21203/rs.3.rs-8947587/v1
16. Yan, S., Gu, J.-C., Zhu, Y., & Ling, Z.-H. (2024). Corrective Retrieval Augmented Generation. *arXiv*.
