# Taxonomy — Agentic RAG and Legal NLP, May 2026

**Status:** Draft v0.1 (assistant-generated from abstracts and Scite excerpts; not from deep reads). Refine after deep-reading the priority papers.
**Corpus:** 29 papers in `reading_list.md`.

---

## Cluster 1: Legal NLP — Datasets & Benchmarks

Papers that define or extend the benchmarks against which legal LLM systems are measured.

- **#8 Guha et al. 2022 — LegalBench** (multi-task legal reasoning benchmark)
- **#9 Butler et al. 2025 — MLEB** (legal embedding benchmark, 10 datasets, 6 jurisdictions)
- **#11 Choudhury et al. 2025 — CLAUSE** (discrepancy benchmark built from CUAD + ContractNLI + RAG-based perturbation pipeline)
- **#14 Vaddi 2026** — comparative model study using ContractNLI, CASEHOLD, ECTHR
- **#27 Nguyen et al. 2024 — CAPTAIN at COLIEE 2024** (system paper at a major legal IR competition)

**Common approach:** Construct or use static benchmarks with held-out test sets; evaluate single-shot or zero-shot LLM performance.
**Strengths:** Standardized, comparable across systems. Highly cited (LegalBench, CUAD).
**Weaknesses:** Static benchmarks saturate quickly; do not evaluate iterative reasoning or agent trajectories. Mostly English/US-jurisdiction biased (MLEB partially addresses this).
**Open questions:** Can a benchmark capture the *quality* of legal reasoning (chain of citations, multi-step reasoning) rather than just final-answer accuracy?

---

## Cluster 2: Legal NLP — Applied Methods (non-agentic)

Papers that propose specific methods (retrieval, classification, extraction) for legal tasks without explicit agentic structure.

- **#10 Reuter et al. 2025** — Summary-Augmented Chunking (SAC) reduces document-level retrieval mismatch in legal RAG
- **#12 Topollai et al. 2025** — modular RAG pipeline for industrial contract revision
- **#13 Šavelka & Ashley 2023** — zero-shot LLM semantic annotation across legal text types
- **#15 Wankhade 2026 — EL-RAG** — explainable RAG with hybrid sparse-dense retrieval, learning-to-rank, multi-hop reasoning + Evidence Alignment Layer for legal
- **#16 Sivapiran et al. 2023** — party extraction from contracts using contextualized spans
- **#17 Vidler et al. 2023** — clause extraction with smaller models (CUAD)
- **#28 Quevedo et al. 2024** — survey of legal NLP 2015–2022 (read first)
- **#29 Gültekin et al. 2024** — energy-aware comparison of SVM vs. BERT vs. LegalBERT on LexGLUE

**Common approach:** Improve a specific retrieval, classification, or extraction step. Often modular pipelines rather than end-to-end agents.
**Strengths:** Practical, reproducible, well-evaluated on standard datasets.
**Weaknesses:** Most do not handle multi-step reasoning or cross-document workflows. Few address the *user* (lawyer) — they address the data.
**Open questions:** What is the right level of integration between LLM-based reasoning and traditional retrieval pipelines for the legal domain?

---

## Cluster 3: Graph-based & Multi-hop RAG (general)

Papers that extend RAG with knowledge-graph structures or multi-step retrieval.

- **#18 Zhuang et al. 2025 — LinearRAG** — relation-free hierarchical graph for large-scale corpora; avoids costly LLM-based relation extraction
- **#19 Wang et al. 2025 — AGRAG** — Minimum Cost Maximum Influence subgraph reasoning; provides explicit reasoning paths
- **#20 Liu et al. 2025 — G2ConS** — graph-guided concept selection (paper mentions law as a target domain)

**Common approach:** Build a graph from the corpus (KG, concept graph, or hierarchical structure); use graph traversal to support multi-hop retrieval.
**Strengths:** Better handling of complex, multi-document queries. Explicit reasoning paths aid interpretability.
**Weaknesses:** Graph construction is expensive and noisy. Most papers evaluate on general QA benchmarks (HotpotQA, MuSiQue), not domain-specific.
**Open questions:** Does graph-based RAG beat strong dense retrievers when the corpus is legal (highly structured, citation-heavy)?

---

## Cluster 4: Agent Architectures & Planning (general-domain)

Papers that improve how LLM agents plan, reason, and reflect — not domain-tied.

- **#21 Wei et al. 2025 — Beyond ReAct** — Planner-centric DAG planning replaces ReAct's local optimization
- **#22 Zhang et al. 2025 — ReCAP** — recursive hierarchical planning with shared context
- **#23 Madahar 2025 — Lateral ToT** — preserves low-utility branches in tree search to improve coverage

**Common approach:** Improve the reasoning/planning loop structure (DAG, recursion, lateral search) over ReAct/CoT baselines.
**Strengths:** Demonstrated gains on long-horizon benchmarks (Robotouille, math, code).
**Weaknesses:** Almost none of this work has been transferred to legal reasoning. Open question whether the gains transfer when the corpus and reasoning style differ.
**Open questions:** Which planning architecture is best suited to legal-document tasks where evidence is spread across multiple documents and citations matter?

---

## Cluster 5: Faithfulness, Citation, Grounding

Papers that focus on ensuring LLM-RAG outputs are grounded in retrieved evidence.

- **#5 Martin et al. 2024** — semantic verification in LLM-RAG (Swiss democracy context)
- **#24 Choi et al. 2025 — CiteGuard** — retrieval-augmented citation attribution validation (scientific writing)
- **#25 Guan et al. 2025** — Faithfulness-aware multi-objective context ranking
- **#26 Clarizia et al. 2025** — Ontology-based RAG grounding via subject-predicate-object triples
- **(#15 EL-RAG also fits here — Citation Alignment Score + Faithful Justification Index)**

**Common approach:** Add a verification, ranking, or grounding layer between retrieval and generation that explicitly checks the output against retrieved evidence.
**Strengths:** Reduces hallucination measurably. Aligns with high-stakes deployment needs.
**Weaknesses:** Most work is on scientific or general QA. Legal citation has unique structure (case names, citations like "X v. Y, 123 U.S. 456 (1985)") that general methods don't exploit.
**Open questions:** Can a citation-faithfulness benchmark designed specifically for legal text catch failure modes that general benchmarks miss?

---

## Cluster 6: Domain-Specific RAG (non-legal exemplars — useful as templates)

Papers that show what domain-specific agentic RAG looks like in mature domains (mostly medical).

- **#1 Low et al. 2025** — clinical RAG + agentic systems; OpenEvidence vs ChatRWD
- **#2 Yu et al. 2025 — YpathRAG** (pathology with dual-channel retrieval + LLM judgment)
- **#3 Yang et al. 2025** — dual retrieving/ranking medical RAG with ColBERTv2
- **#4 Wang et al. 2025** — Enterprise LLM eval framework (CRAG)

**Common approach:** Curate domain vocabulary/corpus, use hybrid retrieval, add domain-specific evaluation.
**Strengths:** Show what "publishable applied RAG paper" looks like — provides architectural template for legal equivalent.
**Weaknesses:** Most are not transferable directly; domain assumptions (medical ontologies, clinical workflows) differ.
**Open questions:** Which medical RAG pattern (e.g., YpathRAG's dual-channel hybrid retrieval) ports best to legal?

---

## Cluster 7: LLM Agent Evaluation Methodology (general)

Papers proposing new ways to evaluate agents, not new agents.

- **#6 Shah 2026** — survey: four-axis taxonomy of evaluation (planning, tool use, self-reflection, memory)
- **#7 Fu et al. 2025 — CATArena** — tournament-style iterative evaluation with open-ended scoring

**Common approach:** Move beyond fixed-test-set accuracy to dynamic, iterative, or relative evaluation.
**Strengths:** Addresses benchmark saturation (a known problem). High citation potential.
**Weaknesses:** No domain-specific application (the survey notes this is an open area). Mostly tested on games/general tasks.
**Open questions:** Can iterative or tournament-style evaluation be applied to legal-reasoning agents, where tasks have semi-objective answers but reasoning quality matters?

---

## Cross-Cluster Observations

1. **Legal RAG ≠ Agentic Legal RAG.** Most legal NLP work (Cluster 2) does retrieval improvements; very little uses agent architectures (Cluster 4). EL-RAG is one of the only papers explicitly multi-hop for legal.

2. **Agent architecture work is domain-generic.** Beyond ReAct, ReCAP, Lateral ToT all test on Robotouille/math/code. None tackle legal. **This is a transfer-learning gap a single applicant could plausibly fill.**

3. **Faithfulness methods are general, not legal.** CiteGuard targets scientific citations. No specific work on legal citation faithfulness despite legal practitioners' zero tolerance for fabricated case citations.

4. **Benchmarks are static.** All legal benchmarks (LegalBench, ContractNLI, CUAD, MLEB) are static-test-set. No tournament-style or iterative evaluation à la CATArena exists for legal.

5. **Efficiency angle is open.** Gültekin 2024 shows efficiency matters for legal NLP (carbon footprint, deployment cost). No work on token/step efficiency of legal *agents*. DEPO-style efficiency work has not been ported to legal.

6. **PEFT/LoRA is missing.** Conspicuously absent from this 29-paper list. Either it's assumed as plumbing, or it's an underexplored angle for legal specifically.

---

## Candidate Gaps for the Research Project

Refining the spec's candidate niches based on this taxonomy. Each is a publishable workshop-paper-scale gap.

### Gap A — Agentic evaluation benchmark for legal reasoning
**One-sentence framing:** Build a benchmark that evaluates legal-reasoning agents on multi-step trajectories (not just final answers), inspired by CATArena (Fu 2025) and Shah's (2026) four-axis taxonomy.
**Builds on:** LegalBench / CUAD / ContractNLI (existing legal tasks) + CATArena / Shah survey (eval methodology).
**Novel angle:** Static legal benchmarks ↔ iterative/agentic eval. No one else has done this combination.
**Feasibility:** High — needs dataset construction + 2-3 baseline agents on small models. Single GPU feasible.
**Workshop fit:** Strong — fits ACL/EMNLP/NeurIPS workshop themes on agent evaluation and applied NLP.

### Gap B — Multi-hop agentic RAG for cross-document legal reasoning
**One-sentence framing:** An agentic RAG that traverses multiple legal documents (case law, statutes, contracts) to answer compound questions, evaluated on a new cross-document benchmark.
**Builds on:** EL-RAG (only existing legal multi-hop work) + AGRAG / LinearRAG (graph methods).
**Novel angle:** Most graph-RAG is general-domain; most legal RAG is single-document. Combine them.
**Feasibility:** Medium — graph construction on legal corpora is non-trivial; compute can spiral.
**Workshop fit:** Strong — combines two hot topics (agents + multi-hop).

### Gap C — Efficiency-focused legal agentic RAG
**One-sentence framing:** Reduce token/step cost of legal RAG agents while maintaining accuracy, using DEPO-style preference optimization on a legal benchmark.
**Builds on:** DEPO (Chen 2025, from design phase) + Gültekin 2024 (efficiency motivation) + LegalBench.
**Novel angle:** No one has applied efficiency-tuned agent training to legal tasks. Practical impact (legal-tech cost concerns).
**Feasibility:** Medium-High — needs reinforcement learning skill (DEPO uses preference optimization).
**Workshop fit:** Good — fits efficiency/practical-deployment workshops.

### Gap D — Legal citation faithfulness benchmark + method
**One-sentence framing:** A benchmark and method for evaluating whether LLM-RAG legal outputs cite actual case law (vs. hallucinated citations), with a faithfulness-tuned ranker.
**Builds on:** CiteGuard (Choi 2025, scientific citations) + Guan 2025 (faithfulness-aware ranking) + CUAD/LegalBench corpora.
**Novel angle:** Legal citation has unique structure (case names, jurisdiction); general citation methods don't exploit this. High real-world impact.
**Feasibility:** Medium — needs careful annotation of correct citations. Could partner with a law student.
**Workshop fit:** Excellent — combines safety/grounding (hot topic) with applied legal NLP.

---

## Recommendation (for your decision at M2, Aug 2026)

Based on the spec's success criteria (workshop submission + arXiv preprint, solo execution, single GPU):

1. **Top pick: Gap A** — best feasibility-to-impact ratio. Dataset construction + agent evaluation methodology has high citation potential and avoids compute-heavy training.

2. **Second pick: Gap D** — strong workshop fit and unique angle. Risk: annotation effort.

3. **Stretch pick: Gap B** — most impressive if it works, but highest compute and complexity risk for solo work.

4. **Skip for now: Gap C** — efficiency work is novel but DEPO-style RL training is high-skill-floor for a solo Master's-level researcher in 12 months.

**Action for July 2026:** Re-evaluate these gaps after deep-reading 15+ papers. Some gaps may close (someone else publishes first). Some new gaps may emerge from the papers you read.

---

## Caveats on This Draft

- Built from abstracts + Scite excerpts, not deep reads. **You may find that Cluster 2 papers actually do agentic work I missed**, or that Cluster 4 papers don't quite fit how I framed them.
- Gap claims about "no one has done X" are based on a 29-paper snapshot. Verify by searching specifically for the gap area before committing to a candidate (e.g., search "legal agent benchmark" before claiming Gap A is open).
- This taxonomy will rot. Update it every month during Phase 1 as papers move between clusters and as new ones (arXiv adds ~10 relevant per week in this space) appear.
