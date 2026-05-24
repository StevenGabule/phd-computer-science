# Candidate Problem Statements — May 2026

**Status:** v0.1 — 4 candidates developed in parallel by background research agents, each with independent Scite validation searches (May 25, 2026). Re-validate before locking at M2 (Aug 2026).

**Reading order:** Skim all 4 candidates → read the **Cross-Candidate Validation** section at the end → bring to your reading group / paper-swap for feedback → decide at M2.

---

## Candidate A: ContractTraj-Bench — A Step-Level Trajectory Benchmark for Agentic Contract Reasoning

### Problem
Existing legal-NLP benchmarks (LegalBench, ContractNLI, CUAD, MLEB, LegalBench-RAG) score only final answers, so an agent that arrives at the right NDA-clause classification through hallucinated retrieval and unverified reasoning is rewarded equally to one that grounds every step in cited clauses. Junior M&A lawyers and contract reviewers using agentic copilots cannot debug *where* an agent went wrong on a 60-page Share Purchase Agreement when only end-to-end accuracy is reported. No public benchmark instruments the four-axis agent rubric (planning, tool-use, self-reflection, memory; cf. Shah 2026) on contract-reasoning trajectories with clause-level provenance ground truth.

### Motivation
In contract review, a wrong "Termination for Convenience" answer that cites the wrong clause is a malpractice risk; the same wrong answer with the *right* clause cited is a recoverable judgment call. Step-level diagnosis is therefore the operational requirement, not a research luxury. Without it, the field will keep saturating LegalBench-RAG (already >85% on top systems) while real failures (missed cross-references, defeasible-rule violations) stay invisible.

### Specific subtask
Build a benchmark of 200-300 multi-step contract-reasoning trajectories spanning clause cross-referencing, defined-term resolution, defeasible-condition application, and conflicting-provision detection over CUAD + ContractNLI documents, where each trajectory is annotated with step-level labels for retrieval correctness, citation faithfulness, reflection triggers, and final-answer correctness.

### Novel angle (post-validation)
Validation found three close-but-different works: EU-Agent-Bench (Lichkovski et al., 2025) evaluates agent *compliance with EU law*, not legal-reasoning trajectory quality; LegalWiz (Mantravadi et al., 2025) is a multi-agent contradiction-generation framework; LOGicalThought (Nananukul et al., 2025) hits ContractNLI but scores only final answers. The gap is open but narrower than originally framed: the novel contribution is **a legal-domain step-level rubric** (clause provenance, defined-term traceability, defeasibility) layered on a CATArena-style trajectory protocol, not the trajectory-evaluation idea itself.

### Proposed method
A four-layer benchmark: (1) a *task generator* that converts CUAD/ContractNLI items into multi-step queries requiring 2-5 retrieval-reasoning hops (e.g., "does Section 7.3's indemnity cap survive termination given Section 12.1's carve-outs?"); (2) a *reference agent harness* using LangGraph + Llama-3.1-8B / Qwen2.5-7B QLoRA-tuned, with retriever/reflector/synthesizer tools; (3) a *trajectory-annotation protocol* labelling each step on retrieval-precision, citation-faithfulness, reflection-validity, and memory-coherence (Shah's 4-axis taxonomy adapted to legal); (4) an *LLM-judge-plus-spot-check* evaluation following CATArena's tournament pairing for relative ranking. Novel contribution sits in layers (1) and (3): the legal-specific step rubric and the cross-reference fidelity metric.

### Datasets
- **CUAD** (Hendrycks et al., 2021) — Public on HuggingFace, 510 contracts, 13k+ clause annotations
- **ContractNLI** (Koreeda & Manning, 2021) — Public on GitHub, 607 NDAs
- **LegalBench-RAG** (Pipitone et al., 2024) — Public on HuggingFace, used as a final-answer comparator
- **MAUD subset** — Public, M&A deal points for cross-reference subtask
- **New trajectory annotations** — Must construct (~200-300 trajectories × 4-axis labels; estimated 4-6 weeks solo with LLM-assisted pre-labelling + manual verification on 50-item gold subset)

### Baselines to compare against
- **Vanilla RAG** with Llama-3.1-8B-Instruct + BGE-large retriever
- **Self-RAG** (Asai et al., 2023)
- **ReAct** (Yao et al., 2023) on Qwen2.5-7B
- **LegalBench-RAG reference pipeline** (Pipitone et al., 2024)
- **GPT-4o-mini ReAct** as a closed-model upper bound

### Evaluation metrics
- **Final-answer F1/EM** on ContractNLI labels — comparability to prior work
- **Retrieval Precision@k per step** — measures tool-use quality
- **Citation Faithfulness** (Min et al. FactScore-style) — adapted for clause IDs
- **Cross-Reference Recall** — new: fraction of relied-on clauses correctly traced
- **Reflection Validity rate** — does a triggered reflection step change a wrong intermediate state to a right one
- **Trajectory Efficiency** — tokens/steps to correct answer (penalises wandering)

### Risks and contingencies
- *Annotation cost balloons beyond solo capacity* — mitigation: cap at 200 trajectories, use LLM pre-labelling with 50-item human-gold calibration set; release smaller v0.1
- *LLM-judge bias inflates trajectory scores* — mitigation: dual-judge (GPT-4o + Claude Sonnet) with disagreement-flagged manual review; report inter-judge kappa
- *7B base models too weak to produce non-trivial trajectories* — mitigation: include Qwen2.5-14B-Instruct via 4-bit QLoRA; fall back to Colab Pro A100 spot for harder runs
- *EU-Agent-Bench or a concurrent ACL submission scoops the niche* — mitigation: differentiate explicitly on contract-clause-provenance metrics, target a workshop earlier (NLLP @ EMNLP 2026 deadline ~Jul 2026)
- *Cross-reference subtask depends on clean clause segmentation in CUAD* — mitigation: restrict v1 to the 25 CUAD contract types with cleanest annotation

### Feasibility assessment
- Data accessible: **H** — all primary sources are public HuggingFace; only the trajectory annotations need construction
- Compute (single GPU, 7-13B QLoRA): **H** — inference + QLoRA fits in 24GB VRAM; no training of new base models required
- 12-month scope: **M** — annotation is the choke point; achievable if scoped to 200 trajectories, ContractNLI + CUAD only
- Solo execution: **M** — feasible but the LLM-judge calibration and 50-item gold annotation will be the longest single task

### Publishability
- Workshop fit: **H** — fits NLLP, LegalAI, RegNLP, and LLM-agent workshops squarely
- Novelty post-validation: **M** — trajectory-evaluation idea exists in general agent work; the legal-specific rubric is the defensible novel contribution

### Recommended target venues (workshop, in priority order)
1. **NLLP @ EMNLP 2026** — natural-language legal-processing community, exact fit for benchmark contributions
2. **RegNLP @ COLING 2026** — regulatory NLP, growing interest in trajectory-grounded compliance evaluation
3. **LLM Agents workshop @ ICLR 2027 / NeurIPS 2026** — broader agent-eval audience; cite CATArena, Shah, EU-Agent-Bench

### Most relevant prior works (3-5)
- Lichkovski et al. (2025) *EU-Agent-Bench*, arxiv:2510.21524 — evaluates agent *compliance with EU law* via function-call rubric; mine evaluates *trajectory quality of contract-reasoning agents* on private-law documents
- Mantravadi et al. (2025) *LegalWiz*, arxiv:2510.03418 — multi-agent generation of contradictions for legal RAG; mine evaluates rather than generates, and uses real contracts not synthetic
- Pipitone et al. (2024) *LegalBench-RAG*, arxiv:2408.10343 — retrieval-grounded legal QA benchmark with final-answer scoring; mine adds step-level trajectory rubric on the same document set
- Lan et al. (2025) *DeepWideSearch*, arxiv:2510.20168 — general agentic-search benchmark with failure-mode taxonomy; mine adapts the failure-mode framing to contract-specific axes
- Yang et al. (2026) *HippoCamp*, arxiv:2604.01221 — dense step-wise trajectory annotations for personal-file agents; mine borrows the annotation protocol and applies it to legal documents

---

## Candidate B: AgentLex-RAG — Agentic Multi-Hop RAG for Cross-Corpus Legal Compliance Reasoning

### Problem
In-house counsel and compliance officers routinely answer questions whose evidence is scattered across three corpora: a contract clause, the controlling statute or regulation it invokes, and the case law interpreting that statute. Current legal RAG systems (Reuter et al. 2025; Pipitone & Houir Alami 2024 — LegalBench-RAG) retrieve top-k chunks from a single corpus and let the LLM stitch the answer, which fails when the answer requires *chained* lookups (e.g., "Does clause 7.2 of this NDA survive termination under New York law as interpreted in *Ashland Mgmt*?"). EL-RAG (Wankhade 2026) added a multi-hop reasoning generator but uses a static hybrid retriever rather than an agent that *decides* which corpus to query next. The concrete deficiency: no published system frames cross-corpus legal QA as an explicit agentic decision process with corpus-routing actions.

### Motivation
Compliance errors from missing one hop (e.g., relying on a contract clause whose enforceability was narrowed by a 2023 ruling) carry real liability — Magesh et al. 2025 found 17%+ hallucination rates on legal RAG even with strong retrievers. Failure looks like a confidently wrong memo that cites a statute but misses the controlling precedent, which is the dominant failure mode flagged by LegalWiz (Mantravadi et al. 2025).

### Specific subtask
Build an agent that, given a compliance question and a contract, plans and executes a sequence of retrieval actions over three indexed corpora — {contract, US statute (USC/CFR), federal case law (Caselaw Access Project)} — and produces an answer with a typed citation chain (clause → statute → case). Evaluation set: 500 hand-curated compound questions where ground-truth evidence demonstrably spans ≥2 corpora.

### Novel angle (post-validation)
Validation searches turned up multi-hop legal RAG (EL-RAG), graph-RAG on legal KGs (Jia et al. 2025), and cross-document contradiction benchmarks (LegalWiz), but **no agentic system that explicitly routes between contract/statute/case-law corpora with learned tool-selection policy and is evaluated on compound questions requiring corpus-crossing**. The novel contribution is (1) the corpus-routing agent formulation, (2) a small curated cross-corpus benchmark (no existing one isolates this skill — LegalBench-RAG queries are mostly intra-corpus), and (3) ablation showing when agentic routing beats flat hybrid retrieval.

### Proposed method
Three-corpus indexed RAG with a 7B agent (Qwen2.5-7B or Llama-3.1-8B, QLoRA fine-tuned) using a ReAct-style loop. Tools: `search_contract`, `search_statute`, `search_caselaw`, each backed by BM25 + bge-small-en hybrid retrievers. The agent emits a typed action plan (corpus, query rewrite), inspects top-3 results, and decides next hop or terminates with a cited answer. Novel components: (a) corpus-router fine-tuned via DPO on synthetic (question → correct-corpus-sequence) trajectories generated from LegalBench-RAG by GPT-4o-mini; (b) hop-budget controller to prevent runaway loops; (c) typed citation chain in the output.

### Datasets
- **LegalBench-RAG** (Pipitone & Houir Alami 2024, arxiv 2408.10343) — Public on HuggingFace; provides contract clause queries.
- **Caselaw Access Project** (case.law) — Public bulk download; US federal case law.
- **USC + CFR** from govinfo.gov — Public XML dumps.
- **Custom cross-corpus eval set** — Need to construct: ~500 questions, ~2 weeks effort (LLM-generated candidates + 1 legal-domain reviewer hired on Upwork for ~$800).
- **NyayaRAG 2025** and **COLIEE 2025** — Public on registration; secondary eval for generalization.

### Baselines to compare against
- Flat hybrid RAG with all three corpora pooled (BM25 + bge-small + RRF)
- EL-RAG (Wankhade 2026) re-implemented (multi-hop reasoning generator, no agentic routing)
- LegalBench-RAG SOTA pipeline (Pipitone & Houir Alami 2024)
- HDRR (Cheng et al. 2026, arxiv 2603.26815) — document-routed hybrid, adapted to legal
- Naive ReAct agent with single pooled corpus (no typed routing)

### Evaluation metrics
- **Citation-chain F1** — precision/recall of (corpus, document_id) pairs in answer vs. gold chain; measures whether all hops are recovered
- **Answer EM / token-F1** — standard QA correctness
- **Hop efficiency** — avg tool calls per correct answer (cost proxy)
- **Faithfulness (LLM-judge)** — does each answer claim trace to a retrieved chunk? (Magesh-style)
- **Wall-clock latency p50/p95** — practical deployability

### Risks and contingencies
1. **Multi-hop compute blowup at 7-13B with 3+ tool calls per query.** Mitigation: cap hop budget at 4, batch retrievals, use bge-small (384d) not bge-large; pre-cache embeddings for the eval corpus.
2. **Custom eval set is the bottleneck and may not be defensible without a real lawyer in the loop.** Mitigation: budget $800 for one paralegal/JD reviewer; release set publicly with the paper as a contribution itself.
3. **Agent fails to learn corpus routing from synthetic trajectories** (well-known DPO-on-synthetic problem). Mitigation: fall back to prompt-engineered ReAct with few-shot exemplars; report both fine-tuned and prompted variants.
4. **EL-RAG re-implementation may not match published numbers** (closed-access paper; no code). Mitigation: implement faithfully from the abstract and cite the gap; compare to a generic multi-hop baseline (IRCoT) instead.
5. **Scope creep into legal-judgment-prediction.** Mitigation: hard constraint — answers are extractive citation chains, not predictions.

### Feasibility assessment
- Data accessible: **H** — LegalBench-RAG, Caselaw Access Project, and USC/CFR are all open; custom eval set is small enough to build solo.
- Compute (single GPU, 7-13B QLoRA): **M** — QLoRA on 7B is fine; the risk is *inference-time* multi-hop (3-4 LLM calls per query × 500 eval examples × N baselines). Manageable with caching and small reranker.
- 12-month scope: **M** — Months 1-3 infra + indexes, 4-6 baselines, 7-9 agent + DPO, 10-11 eval set + experiments, 12 paper. Tight but achievable if eval set construction starts in parallel month 1.
- Solo execution: **M** — Single biggest risk is the legal annotation; mitigated by paid reviewer + LLM pre-filtering.

### Publishability
- Workshop fit: **H** — Cross-corpus agentic RAG + a new benchmark = standard workshop contribution shape.
- Novelty post-validation: **M** — Multi-hop legal RAG is no longer untouched (EL-RAG), but the *agentic corpus-routing* framing and the cross-corpus benchmark are new. Honest framing: "first agentic system for cross-corpus legal compliance QA with typed citation chains."

### Recommended target venues (workshop, in priority order)
1. **NLLP @ EMNLP 2026/2027** — Natural Legal Language Processing workshop is the exact fit; benchmarks + RAG are in-scope.
2. **KaLLM / Knowledgeable LMs @ ACL 2027** — retrieval-augmented and tool-using LMs, agentic angle lands well.
3. **AAAI 2027 Student Abstract** — short version of the cross-corpus benchmark contribution; lower-risk fallback.

### Most relevant prior works (3-5)
1. Wankhade (2026), EL-RAG, DOI 10.21203/rs.3.rs-8947587/v1 — multi-hop legal RAG with hybrid retriever; mine adds *agentic corpus routing* and a cross-corpus benchmark rather than a static reasoning generator.
2. Pipitone & Houir Alami (2024), LegalBench-RAG, arxiv 2408.10343 — single-corpus benchmark; mine extends to cross-corpus compound questions.
3. Reuter, Lingenberg & Liepiņa (2025), arxiv 2510.06999 — addresses Document-Level Retrieval Mismatch via summary-augmented chunking; complementary, I cite as an orthogonal retrieval-side improvement, not a routing one.
4. Mantravadi, Dalmia & Mukherji (2025), LegalWiz, arxiv 2510.03418 — explicitly calls cross-document contradiction the open gap; mine answers their "needs retrieval-aware prompting or multi-hop reasoning" call.
5. Jia, Zhu & Chen (2025), DOI 10.1117/12.3076253 — KG + RAG for labor law contract review; single-jurisdiction, no agent; mine differs by being agentic and US-federal cross-corpus.

---

## Candidate C: LexEcoRAG — Dual-Efficiency Preference Optimization for Agentic Legal RAG

### Problem
Agentic RAG systems for legal/contract analysis (e.g., clause review, CUAD-style extraction, LegalBench reasoning) typically issue many redundant tool calls and consume tens of thousands of tokens per query, making them economically and environmentally costly for routine deployment in mid-sized law firms and in-house counsel teams. Gultekin et al. (2024) showed classical models were 40-75× cheaper than BERT-family models on LexGLUE for comparable accuracy, yet no published work has targeted token and step efficiency of *agentic* legal RAG pipelines as a first-class training objective. The closest analogue, GRAPH-GRPO-LEX (Dechtiar et al., 2025), applies GRPO to contract *graph extraction* with structural rewards, not to agent action budgets. The problem is that practitioners deploying open-weight 7-13B legal agents have no training recipe that explicitly trades accuracy against agent cost.

### Motivation
Legal-tech vendors and solo practitioners running self-hosted models cannot absorb the per-query token cost of long-context, multi-hop agent loops; failure looks like agents abandoned in favor of cheaper SVM/BM25 pipelines that lose the reasoning benefits. Reducing per-query tokens and tool steps by even 30-50% at iso-accuracy directly translates to lower GPU-hours, lower latency for clause-review workflows, and feasibility on a single consumer GPU at inference time.

### Specific subtask
Reduce average tokens-per-query and average tool-call steps-per-query of a 7B agentic RAG system on LegalBench-RAG and CUAD clause-extraction tasks by at least 30% (tokens) and 20% (steps) while keeping macro-F1 within 2 absolute points of an SFT baseline.

### Novel angle (post-validation)
Validation searches confirm: (a) DEPO-style dual-efficiency PO has not been applied in the legal domain; (b) GRAPH-GRPO-LEX uses GRPO but optimizes *graph fidelity*, not action-budget; (c) RECON and HSEQ pursue efficient RAG but target general QA, not legal corpora or legal tool schemas. Novelty sits in (i) constructing a legal-specific dual-efficiency reward (token + step + clause-grounding faithfulness) and (ii) demonstrating that efficiency-targeted PO transfers to a domain where tool schemas are narrow (statute lookup, clause retriever, citation checker) but documents are long.

### Proposed method
LexEcoRAG is a 3-tool agent (sparse retriever, dense clause retriever, citation verifier) over a 7B Qwen2.5/Llama-3 base with QLoRA. Stage 1: SFT on synthetic ReAct trajectories generated from CUAD and LegalBench-RAG gold answers. Stage 2: collect rollouts and train with a dual-efficiency reward `r = accuracy - lambda_tok * tokens - lambda_step * steps`. Novel contribution sits in stage 2 reward design and a *Plan B* simpler-method comparison. If GRPO proves too heavy to tune, the same reward is applied via offline DPO over rejection-sampled trajectory pairs (preferred = short+correct, dispreferred = long+correct or short+wrong), which is far more stable for a solo researcher. This explicitly does require preference optimization but degrades gracefully to DPO, which is well-documented in TRL.

### Datasets
- LegalBench-RAG (Pipitone & Alami, 2024): Public on HuggingFace, ready to use.
- CUAD v1 (Hendrycks et al., 2021): Public, CC-BY, 510 contracts, 41 clause types.
- ContractNLI (Koreeda & Manning, 2021): Public on HuggingFace.
- Synthetic ReAct trajectories: construct (est. 2-3 weeks of compute + prompt engineering using Llama-3-70B via OpenRouter or a hosted teacher).

### Baselines to compare against
- Vanilla ReAct + RAG on Llama-3-8B / Qwen2.5-7B (no efficiency training).
- SFT-only baseline (trained on same trajectories, no efficiency reward).
- RECON-style learned context compression (Xu et al., 2025, arxiv:2510.10448) ported to legal.
- BLADE (Li et al., AAAI 2025, doi:10.1609/aaai.v39i23.34620): black-box LLM + small domain model.
- Topollai et al. (2025, arxiv:2511.14671) industrial-contract RAG (where comparable).

### Evaluation metrics
- **Macro-F1 / Exact-Match** on LegalBench-RAG and CUAD (primary accuracy).
- **Avg tokens per query** (input + output): direct deployment cost proxy.
- **Avg tool-call steps per query**: latency and orchestration cost proxy.
- **End-to-end wall-clock latency on single RTX 4090** (or Colab L4): practitioner-relevant.
- **Citation faithfulness** (clause-span overlap with gold): guards against efficiency-by-shortcutting.

### Risks and contingencies
1. **Primary risk — RL/PO skill floor (HIGH).** User's preference-optimization skill is unknown; GRPO tuning is notoriously sensitive. *Mitigation:* commit upfront to a DPO-first path using TRL's well-documented `DPOTrainer`, treating GRPO as a stretch goal. If even DPO is unstable, fall back to **Plan B: training-free efficiency** via (a) retrieval pruning with a small reranker, (b) early-exit heuristics, (c) prompt-cache + chain-of-thought truncation. This still yields a workshop-worthy ablation paper on "how far you get without PO."
2. **Reward hacking** — agent learns to skip steps and lose accuracy. *Mitigation:* hard constraint `r = -inf` if F1 drops below threshold; keep faithfulness term.
3. **Single-GPU memory for trajectory storage and rollouts.** *Mitigation:* offline DPO needs only inference; rollouts can be batched overnight.
4. **Concurrent publication** — gap is closing fast (RECON, HERA appeared in Oct 2025). *Mitigation:* commit to legal-specific framing and a public LexEcoRAG-bench artifact; even if scooped on method, the legal benchmark + ablations are publishable.
5. **LegalBench-RAG label noise.** *Mitigation:* report per-task breakdown.

### Feasibility assessment
- Data accessible: **H** — LegalBench-RAG, CUAD, ContractNLI all public on HF.
- Compute (single GPU, 7-13B QLoRA): **M** — QLoRA SFT and DPO on 7B are fine; full GRPO with 16 rollouts on 13B is borderline on a single 24GB card and may need 7B + Colab Pro bursts.
- 12-month scope: **M** — feasible only if DPO path is committed early; full GRPO ablation could blow the budget.
- Solo execution: **M-L** — the RL component is the single biggest risk. Rating is **M** if the user can demonstrate prior DPO experience, **L** if not, in which case Plan B is mandatory.

### Publishability
- Workshop fit: **H** — efficient-ML and legal-NLP workshops are actively soliciting this kind of work.
- Novelty post-validation: **M** — domain transfer of efficiency PO is novel but adjacent work (GRAPH-GRPO-LEX, RECON, HERA) is publishing rapidly. Tight framing on tokens+steps+faithfulness in legal is still defensible through 2026.

### Recommended target venues (workshop, in priority order)
1. **EMNLP 2027 NLLP workshop (Natural Legal Language Processing)** — direct fit; values legal-domain efficiency work.
2. **NeurIPS 2027 Efficient Natural Language and Speech Processing (ENLSP) workshop** — values token/latency results across domains.
3. **ICLR 2027 Tiny Papers** — if Plan B (training-free) ends up being the contribution, the 4-page format is ideal.

### Most relevant prior works (3-5)
- Dechtiar et al. (2025), *GRAPH-GRPO-LEX*, arxiv:2511.06618 — uses GRPO on contracts but for graph extraction; my work targets agent action-budget, not graph fidelity.
- Xu et al. (2025), *RECON*, arxiv:2510.10448 — efficient RAG via context condensation, general QA; I apply preference-optimization to legal *agent steps*, not summarization.
- Li & Ramakrishnan (2026), *HERA*, arxiv:2604.00901 — token-efficient multi-agent RAG via gradient-free evolution on general benchmarks; I use gradient-based PO and target a single-agent legal setting deployable on one GPU.
- Topollai et al. (2025), arxiv:2511.14671 — industrial contract RAG with reward-based alignment for *acceptability*, not efficiency; I add token/step terms to the reward.
- Vaddi (2026), arxiv:2603.25944 — small-model efficiency comparison on CONTRACTNLI/CASEHOLD via prompting only; I train for efficiency rather than compare static models.

---

## Candidate D: CiteCheck — An Open Benchmark and Agentic-RAG Method for Verifiable US Case-Law Citations

### Problem
Open-weight legal RAG systems routinely emit case citations that look syntactically correct in Bluebook form ("Smith v. Jones, 412 F.3d 567 (9th Cir. 2005)") but refer to cases that do not exist, do not stand for the proposition cited, or come from the wrong jurisdiction. Mata v. Avianca (S.D.N.Y. 2023) sanctioned attorneys for filing a brief containing six such fabricated citations from ChatGPT. While Magesh et al. (2025) showed that even proprietary RAG tools (Lexis+ AI, Westlaw AI-Assisted Research) hallucinate 17-33% of the time, they release no open benchmark, no open-weight baseline, and no method — and existing open frameworks like EL-RAG (Wankhade 2026) evaluate on Indian/COLIEE corpora, not US case law resolvable against public registries.

### Motivation
The Mata sanction has been followed by ~50 documented US court orders citing AI-generated fake authorities (per the Damien Charlotin tracker), with judges now adding standing orders requiring AI-use disclosure. Open-weight 7-13B models will not be auditable by law-firm IT or used responsibly in pro-bono / public-defender contexts (Cheong et al., 2025) without an open, reproducible measurement of how often they fabricate citations and an open method to drive that rate down.

### Specific subtask
Given a legal question and a US-jurisdiction RAG corpus, generate a grounded answer with citations such that every cited authority (i) resolves to a real opinion in the CourtListener / Caselaw Access Project API, (ii) covers the proposition asserted (entailment check), and (iii) is jurisdictionally appropriate. The benchmark scores each citation on these three axes; the method is an agentic RAG pipeline that calls a CitationResolver tool at decode-time and reranks/retracts unverifiable claims.

### Novel angle (post-validation)
Magesh et al. measures closed systems; EL-RAG focuses on non-US corpora with self-reported alignment scores; HalluGraph (Noël et al., 2025) does post-hoc KG audit. None offers an open, open-weight, US-case-law benchmark where citation existence is checked against a live public registry, nor an agentic method that uses Bluebook-structure parsing plus a CourtListener lookup as a verification tool inside the generation loop. The novelty is the combination: (open benchmark) + (structure-aware faithfulness-tuned reranker exploiting Bluebook regex fields) + (agent-callable citation-resolver tool) under a single-GPU budget.

### Proposed method
A three-stage agentic RAG pipeline over a Llama-3.1-8B / Qwen2.5-7B base with QLoRA. Stage 1 — Retrieve: hybrid BM25 + dense (BGE-legal) over a CAP/CourtListener-indexed corpus. Stage 2 — Faithfulness-tuned rerank: a cross-encoder fine-tuned with a multi-objective loss combining standard relevance and a structure-aware citation-grounding signal (Bluebook fields parsed via eyecite); positive pairs require the candidate passage to contain a citation whose resolved opinion text supports the claim. Stage 3 — Agent verify: at generation time the model emits citations through a constrained-decoding grammar; a CitationResolver agent tool queries the CourtListener API and a local CAP mirror; unresolvable or non-entailing citations trigger retraction or re-retrieval (max k iterations). The novel contribution sits at the rerank loss (structure-aware) and the agent tool-loop (live verification).

### Datasets
- Caselaw Access Project bulk data — public, free, ~6.7M US opinions (https://case.law).
- CourtListener API — public, free with rate-limited key, covers PACER + opinions.
- LegalBench-RAG (Pipitone & Alami, 2024) — public on HuggingFace, used as one task source.
- CUAD (Hendrycks et al., 2021) — public on HuggingFace, for contract-citation subset.
- Need to construct: ~500-1000 question / gold-citation pairs (effort: ~6-8 weeks solo, or 4 weeks with one annotator). Seed from briefs cited in the Charlotin AI-hallucination tracker for adversarial cases.

### Baselines to compare against
- Vanilla Llama-3.1-8B-Instruct (no retrieval)
- Llama-3.1-8B + naive RAG (BM25 + top-k stuff)
- Llama-3.1-8B + Self-RAG (Asai et al., 2024)
- Llama-3.1-8B + CRAG (Yan et al., 2024)
- EL-RAG (Wankhade, 2026) reimplementation if released
- HalluGraph (Noël et al., 2025) as post-hoc detector baseline
- GPT-4o-mini with web-search tool (closed-API ceiling reference)

### Evaluation metrics
- **Citation Resolution Rate:** % of emitted citations that resolve to a real CourtListener opinion (existence is binary, machine-checkable).
- **Citation Support F1:** does the resolved opinion entail the asserted proposition (NLI-judged + 200-item human audit).
- **Jurisdictional Validity:** % of citations from a binding/persuasive jurisdiction for the question.
- **Fabrication Rate:** 1 − resolution rate; primary headline metric tied to Mata-type harm.
- **Answer Utility (Likert 1-5, 100-item human audit)** to detect over-retraction.
- **Latency and tokens-per-query** — feasibility on a single GPU.

### Risks and contingencies
- Annotation effort balloons: mitigate by seeding from existing Charlotin tracker briefs and using LLM-assisted pre-labels with spot-check (Gray et al., 2024 methodology).
- CourtListener API rate limits break agent loop: mirror the CAP bulk dump locally (~100 GB) and cache resolver calls.
- Entailment NLI is noisy on legal language: report both NLI score and human-audited subset; do not headline NLI-only numbers.
- Scoop risk — EL-RAG-v2 or a Magesh follow-up may release first: differentiate by being open-weight + open-data + reproducible-on-one-GPU; emphasize the agent-tool-loop contribution even if the benchmark is partially scooped.
- No law-student annotator available: fall back to the Charlotin tracker + appellate-brief mining for gold citations (lower coverage but zero-partner risk).

### Feasibility assessment
- Data accessible: **H** — CAP and CourtListener are fully open with documented APIs.
- Compute (single GPU, 7-13B QLoRA): **H** — reranker fine-tune and 7-8B QLoRA fit on 24 GB; agent loop is inference-only.
- 12-month scope: **M** — benchmark construction (3-4 months) + method (4 months) + eval (2 months) + writing is tight but achievable if scope is held to ~500 questions.
- Solo execution: **M** — annotation is the binding constraint; lower to **H** if a law-student collaborator joins for 8 weeks of validation.

### Publishability
- Workshop fit: **H** — NLLP (Natural Legal Language Processing) at EMNLP is a near-perfect home; safety/trustworthy-ML workshops are a strong second.
- Novelty post-validation: **M** — the benchmark-only angle is partly covered by Magesh and Butler & Butler (2026); the open-weight + agentic-verifier + structure-aware reranker combination is the defensible novel contribution.

### Recommended target venues (workshop, in priority order)
1. NLLP @ EMNLP 2026/2027 — the canonical legal NLP workshop; citation faithfulness is squarely in scope.
2. TrustNLP @ NAACL 2027 — frames the work as trustworthy-NLP with a high-stakes deployment story.
3. ICLR 2027 Tiny Papers or AAAI 2027 Student Abstract — a 2-4 page distillation as a backup low-risk venue.

### Most relevant prior works (3-5)
- Magesh, V., Surani, F., & Dahl, M. (2025). Hallucination-Free? Assessing the Reliability of Leading AI Legal Research Tools. *Journal of Empirical Legal Studies*, 22(2), 216-242. https://doi.org/10.1111/jels.12413 — Closed-system audit; this work provides the open, reproducible counterpart with a method, not just measurement.
- Wankhade, N. W. (2026). EL-RAG. https://doi.org/10.21203/rs.3.rs-8947587/v1 — Introduces CAS/FJI on Indian/COLIEE corpora; this work targets US case law with live registry resolution and an agentic verifier instead of a static alignment score.
- Noël, V., Seidou, E. Y., & Capo-Chichi, C. K. (2025). HalluGraph. https://doi.org/10.48550/arxiv.2512.01659 — Post-hoc KG audit; this work integrates verification into the generation loop and resolves to a live public registry rather than a derived KG.
- Butler, A.-R., & Butler, U. (2026). Legal RAG Bench. https://doi.org/10.48550/arxiv.2603.01710 — End-to-end legal RAG benchmark; this work narrows scope to citation existence/support, releasing a focused open-weight method targeting Mata-type fabrication.
- Cheong, I., Liu, P., & Stammbach, D. (2025). How Can AI Augment Access to Justice? https://doi.org/10.48550/arxiv.2510.22933 — Motivates the open-weight constraint and verification emphasis from a deployment-needs perspective.

---

# Cross-Candidate Validation (assistant analysis, May 25, 2026)

After all 4 candidates were developed in parallel, here is a head-to-head comparison and a culling recommendation.

## Scorecard

| Criterion | A: ContractTraj | B: AgentLex | C: LexEcoRAG | D: CiteCheck |
|---|---|---|---|---|
| Data accessibility | H | H | H | H |
| Compute (single GPU) | H | M | M | H |
| 12-month scope | M | M | M | M |
| Solo execution | M | M | **M-L** | M (→H with partner) |
| Workshop fit | H | H | H | H |
| Novelty post-validation | M | M | M | M |
| Real-world impact / SOP hook | M | H | M | **H (Mata v. Avianca)** |
| Scoop risk (next 12 months) | H (EU-Agent-Bench fresh) | M (EL-RAG closest) | **H (3 fresh threats: RECON/HERA/GRAPH-GRPO-LEX)** | M (Butler 2026 closest) |
| Skill/expertise risk | Low | Low-M | **HIGH (GRPO/DPO)** | Low |
| Cost (annotation/compute beyond GPU) | $0 | **~$800 reviewer** | $0 | $0 (or partner) |
| Earliest viable workshop deadline | NLLP EMNLP 2026 (Jul) | NLLP EMNLP 2026 (Jul) | EMNLP 2027 NLLP | NLLP EMNLP 2026 (Jul) |

## Overlap analysis

- **A and B both use LegalBench-RAG + CUAD as core data** — sharing infrastructure investment is realistic.
- **A and D both produce a new open benchmark** — could be unified ("open benchmark for agentic legal RAG evaluating trajectory quality AND citation faithfulness"), but **risk: scope creep beyond a single workshop paper**.
- **B and D both involve agent tool-loops over case law / statute corpora** — sharing the CourtListener/CAP index infrastructure is realistic.
- **C is method-only and somewhat orthogonal** to the others. Could be combined with B as "agentic cross-corpus RAG with efficiency-targeted training" but that doubles the scope risk.

## Recommendation: keep 2, defer 1, drop 1

### KEEP — Candidate D (CiteCheck) as **primary**

Reasons:
- **Highest real-world impact + SOP narrative.** Mata v. Avianca is concrete, ongoing, and easy to explain to admissions committees and to non-CS reviewers.
- **Lowest skill floor risk** — the technical components (cross-encoder reranker + agent tool loop) are well-trodden territory.
- **Highest data accessibility** — both CAP and CourtListener are fully open and documented.
- **Highest compute feasibility** — reranker fine-tune + 7-8B QLoRA fits comfortably on a single 24GB card.
- **Strong workshop fit** — NLLP and TrustNLP are both natural homes; the safety angle is timely.
- Honest weakness: Butler & Butler 2026 (Legal RAG Bench) is a partial scoop. Mitigate by narrowing scope to **citation existence/support specifically** rather than general legal RAG.

### KEEP — Candidate A (ContractTraj-Bench) as **secondary / Plan B**

Reasons:
- **Lowest compute risk** — no training of base models, all QLoRA + inference.
- **Different paper shape** from D (trajectory eval vs. citation faithfulness), so the two don't compete for the same workshop slot.
- The 4-axis rubric is a strong methodological contribution even if EU-Agent-Bench publishes a competing benchmark first.
- Caveat: scope is annotation-heavy; if D's annotation also balloons, doing both simultaneously may be impossible. Pick D first, fall back to A if D blocks.

### DEFER — Candidate B (AgentLex-RAG) — strong but expensive

Reasons to defer:
- **$800 paid reviewer is a real out-of-pocket cost** — flag this to user before committing.
- **Compute risk is highest among the four** (multi-hop inference × 500 examples × N baselines).
- 12-month scope is tightest because three corpora must be indexed and integrated.
- However, the framing ("first agentic cross-corpus legal compliance system") is the most impressive if successfully executed.

Decision rule: revisit B at M2 (Aug 2026) **only if** the user has either (a) confirmed budget for the reviewer, (b) access to an advisor who can sponsor the project, or (c) made significant progress on D and wants to extend.

### DROP — Candidate C (LexEcoRAG)

Reasons:
- **Single biggest disqualifier: solo feasibility is M-L without confirmed RL/PO skills.** The user's preference-optimization experience was flagged as unknown. The Plan B (training-free efficiency) is real but reduces novelty to "engineering ablation paper" rather than a methods paper.
- **Scoop risk is highest** — three fresh (Oct/Nov 2025 → 2026) competing papers (RECON, HERA, GRAPH-GRPO-LEX) are publishing rapidly in adjacent space.
- Other candidates do not have this skill-floor problem.
- If the user later wants to do efficiency work, the better strategy is to first publish D or A, then add an efficiency follow-up paper in the PhD itself.

## Suggested action sequence (for M2 lock decision)

1. **By mid-Jul 2026:** revisit this candidates.md after deep-reading 5+ papers from `literature/papers/`. Verify gap claims independently.
2. **Before Aug 31 (M2 lock):** if D's data construction looks tractable in your first ~2 weeks of prototyping (Aug 1-15), commit to D. If you stall on data construction, switch to A.
3. **Stretch path (only if D is going very well by Mar 2027):** add A's trajectory-evaluation axis as a *second contribution* in the D paper, framing the benchmark as evaluating both citation faithfulness AND trajectory quality. This is a workshop-paper stretch; do not commit to it upfront.

## Caveats on this analysis

- **All 4 validations were run in May 2026.** Re-search before M2 — arXiv adds ~10 relevant papers/week in this space, and new entrants could close any of these gaps.
- The scoop-risk ratings are based on a 2-3 search snapshot per candidate. Validate specifically against arXiv preprints from Jul-Sep 2026 before locking.
- Real workshop deadlines: NLLP @ EMNLP 2026 is ~Jul 2026 (already past for Sep 2026 target submission, so realistic earliest is NLLP @ EMNLP 2027 with Jun/Jul 2027 deadline). Adjust expectations.
