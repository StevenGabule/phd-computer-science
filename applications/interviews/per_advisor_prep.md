# Per-Advisor Interview Prep — Top 10 Starred Advisors

**Use when:** Preparing for a specific advisor's interview during Jan-Mar 2028. Pair with `applications/interviews/scenarios.md` for the generic scenarios.

**Update before each interview:** Check Google Scholar 48 hours before the interview for any 2027-2028 papers by the advisor that should replace or supplement the cited ones below.

---

## 1. Daniel E. Ho (Stanford RegLab)

**Title:** Professor (Law / CS courtesy)
**Most recent relevant work to cite:**
- "Hallucinating Legal LLMs" (2025) — the paper that anchors CiteCheck's motivation
- "A Reasoning-Focused Legal Retrieval Benchmark" (2025) — closest published benchmark to CiteCheck

**Interview opening pitch (replace generic with):**
"Your 2025 hallucination paper measured exactly the failure mode CiteCheck is built to drive down. The three-axis decomposition I'm using extends Magesh's framing by separating existence, support, and jurisdictional validity as orthogonal failure modes."

**Specific extensions to propose:**
- Citator-aware support axis (temporal validity using CourtListener treatment data) — builds on the overruled-precedent issue Magesh flagged
- Regulatory-RAG extension — apply verify loop to agency rulemaking, which RegLab works on extensively
- Multi-court coverage (state appellate) — RegLab has connections to multiple state-court data initiatives

**Likely interview questions from him:**
- "How does CiteCheck's three-axis breakdown compare to the failure-mode taxonomy in our 2025 paper?"
- "Have you thought about the agency-rulemaking analog?"
- "What's the IAA on your 50-item gold set?"
- "How are you handling overruled precedents — that's a hard sub-case we haven't fully solved either."

**Questions for him:**
- "RegLab has done both empirical audits and method work — how do you split your students' projects between those?"
- "The hallucination paper named several specific commercial systems. Have any of them engaged with the findings? Would CiteCheck's open release shift that conversation?"
- "What's your view on the v0.2 state-court extension — is the data coverage gap too big right now?"

**Risk:** Ho is senior and busy; the interview may be brief. Have the 60-second pitch dialed.

---

## 2. Julian Nyarko (Stanford RegLab)

**Title:** Associate Professor (Law)
**Most recent relevant work:**
- "A Reasoning-Focused Legal Retrieval Benchmark" (2025) — directly adjacent to CiteCheck
- LegalBench (2023) — the canonical benchmark

**Interview pitch:**
"Your 2025 reasoning-focused retrieval benchmark sits in exactly CiteCheck's evaluation neighborhood. The three-axis decomposition I'm using complements that benchmark by separating *what kind* of retrieval failure happened — existence vs. support vs. jurisdiction."

**Specific extensions:**
- Cross-benchmark study: how do CiteCheck failures correlate with your reasoning-focused benchmark failures?
- Contract-specific extension: your contract-AI line of work suggests a CUAD-focused version of CiteCheck
- Multilingual / non-US extension: Nyarko has interests in comparative legal AI

**Likely questions:**
- "How are you constructing the eval set — fully synthetic, or hand-curated?"
- "What's the cost of your verify loop in practice?"
- "Where do you see the boundary between legal AI for practitioners vs. legal AI for researchers?"

**Questions for him:**
- "LegalBench's tasks are mostly classification. Where do you see open-ended generation evaluation going?"
- "The contract-AI line of work you do — would CiteCheck adapted for contracts (rather than case law) be a useful complement, or is the citation-faithfulness frame less relevant there?"

**Note:** Nyarko is more accessible than Ho per Agent E's analysis; this is the stronger primary-advisor pick for the Stanford application.

---

## 3. Jaromír Šavelka (CMU TEEL Lab)

**Title:** Research Faculty (CS / TEEL Lab)
**Most recent relevant work:**
- "Unreasonable Effectiveness of LLMs in Zero-Shot Semantic Annotation" (2023)
- "Adding Argumentation into Evaluation of Legal Summarization" (2024)
- Empirical legal analysis line of work (2024)

**Interview pitch:**
"Your 2023 paper established that zero-shot LLMs can do legal annotation cleanly, which shifts the bottleneck from extraction to verification — and that's exactly where CiteCheck lives. The argumentation-aware evaluation methodology in your 2024 paper directly parallels CiteCheck's three-axis decomposition."

**Specific extensions:**
- Argumentation-aware support axis: rather than NLI for support, use argumentation-scheme analysis (a Šavelka strength)
- Legal-text annotation pipeline for the CiteCheck v0.1 eval set construction (collaborate with TEEL on annotation methodology)
- Holding-vs-dicta distinction as a fourth axis

**Likely questions:**
- "How does your support metric handle dicta vs. holding distinction?"
- "What's the NLI judge accuracy on legal text vs. general text?"
- "Have you thought about how the verify loop interacts with statutory interpretation as opposed to case law?"

**Questions for him:**
- "TEEL Lab has both CS and JD students — how does that affect project design and timelines?"
- "Your annotation methodology has been a focus — what's the protocol for the cross-disciplinary annotators you typically work with?"
- "What's the qualifier exam structure for LTI vs. SCS PhDs? Which would be a better fit for someone doing legal-NLP?"

**Note:** Šavelka was Agent E's top "most likely to respond" pick; the cold-email response, if it comes, is probably the strongest signal for adjusting the SOP.

---

## 4. Sean Welleck (CMU LTI)

**Title:** Assistant Professor
**Most recent relevant work:**
- "RefineBench: Evaluating Refinement Capability" (ICLR 2026)
- "Premise Selection for a Lean Hammer" (ICLR 2026, Oral)

**Interview pitch:**
"CiteCheck's retract-or-retry loop is structurally close to RefineBench's framing — generation followed by an evaluative step that can trigger another iteration. Your premise-selection work on Lean has a similar evaluate-then-refine structure that legal-citation verification could adapt."

**Specific extensions:**
- Verifier-first training: rather than post-hoc verification, train the generator with verification feedback in the loss (Self-Refine adaptation)
- RefineBench-style evaluation: extend CiteCheck with a refinement-capability axis
- Formal-methods crossover: Lean / Coq for legal reasoning where formal proofs are tractable

**Likely questions:**
- "How does the retract-or-retry budget interact with answer quality? Is there a regime where more iterations make it worse?"
- "What's the failure mode when the generator gets stuck and keeps emitting the same fabricated citation?"
- "Have you considered verifier-first training?"

**Questions for him:**
- "RefineBench established a refinement-quality benchmark; do you see CiteCheck-style verification benchmarks as a complement or a competitor?"
- "Your formal-methods work has been on math/code. Do you see legal reasoning as adjacent or fundamentally different?"

---

## 5. Hamed Zamani (UMass CIIR)

**Title:** Associate Professor (CICS / CIIR Associate Director)
**Most recent relevant work:**
- "Stochastic RAG" (SIGIR 2024)
- "Search-R1" (COLM 2025) — multi-agent RAG
- "Evaluating Retriever in RAG" (SIGIR 2024)
- CIIR@LiveRAG 2025

**Interview pitch:**
"Your Stochastic RAG framing and Evaluating Retriever in RAG paper directly inform how I think about CiteCheck's hybrid retrieval design. The Search-R1 multi-agent setup is the natural next step for CiteCheck v0.2 — splitting the citation-resolver, jurisdiction-reasoner, and precedent-tracer into specialized agents."

**Specific extensions:**
- Multi-agent extension of CiteCheck (Search-R1-flavored)
- Retrieval-evaluation methodology: how do you measure retrieval quality when the right answer is a citation chain rather than a passage?
- CIIR@LiveRAG legal track: position CiteCheck for inclusion in LiveRAG-style evaluation

**Likely questions:**
- "What's the hybrid retrieval recall curve like at top-20?"
- "Have you compared to learned sparse (SPLADE-style) retrievers?"
- "What's your RRF k constant? Why?"

**Questions for him:**
- "CIIR has a long history with TREC-style evaluation. Where do you see retrieval evaluation going as the answer unit shifts from passages to citations or to grounded claims?"
- "How do you structure new students' first-year projects? Single-paper vs. exploratory?"

---

## 6. Daniel Khashabi (JHU CLSP)

**Title:** Assistant Professor
**Most recent relevant work:**
- "Dated Data: Tracing Knowledge Cutoffs in LLMs" (COLM 2024 Outstanding Paper)
- "TurkingBench: Benchmark for Web Agents" (2025)
- "Can LLMs Generate Tabular Summaries?" (2026)

**Interview pitch:**
"Your Dated Data paper frames the exact temporal-validity issue CiteCheck v0.2 needs to address: a citation that was valid at training time but isn't at inference time. The overruled-precedent problem in legal AI is a near-perfect analog of the knowledge-cutoff problem in your work."

**Specific extensions:**
- Temporal-validity axis for CiteCheck (citator-aware "was this still good law on date X?")
- TurkingBench-style evaluation for the agent component: structured eval of CitationResolver as an agent task
- Tabular summarization crossover: legal citation chains *are* tabular structures (court / year / volume / page); summarization-style evaluation may apply

**Likely questions:**
- "How are you handling the overruled-precedent case in v0.1? Just accept it as a known limitation?"
- "What's your latency budget per query for the verify loop?"
- "Have you measured agreement between your support axis and the human-rated subset?"

**Questions for him:**
- "Dated Data's methodology was sophisticated. What would a citator-aware temporal-validity axis look like methodologically?"
- "JHU CLSP has both NLP and speech traditions. Where do you see the overlap going?"
- "What does a typical first-year project look like for your students?"

---

## 7. Mirella Lapata (Edinburgh ILCC)

**Title:** Professor
**Most recent relevant work:**
- "Hierarchical Indexing for Retrieval-Augmented Opinion Summarization" (TACL 2024)
- "Uncertainty Quantification in Retrieval-Augmented QA" (2025)
- "Decomposed Opinion Summarization with Verified Aspect-Aware Modules" (2025)

**Interview pitch:**
"Your 2025 Uncertainty Quantification in RAG-QA paper anticipates exactly the v0.2 direction CiteCheck should take — replacing binary VERIFIED / UNRESOLVABLE / NON_SUPPORTING labels with calibrated probabilities. Your Decomposed Opinion Summarization paper demonstrates verify-aware module architecture, which is what CiteCheck implements at smaller scale."

**Specific extensions:**
- Explicit uncertainty propagation through the verify loop
- Aspect-aware decomposition of the support axis (factual / doctrinal-holding / good-law / persuasiveness as separate aspects)
- UK / EU jurisdiction extension as a joint project (Edinburgh has data access)

**Likely questions:**
- "How do you propose to calibrate the uncertainty estimates?"
- "What's the inter-rater agreement on the support axis right now?"
- "Why US case law first and not UK?"

**Questions for her:**
- "Your verified-aspect-aware modules paper is a structural precedent for CiteCheck. Where do you see that architecture going next?"
- "Edinburgh has a CDT-NLP cohort program separately from the open-call PhD. Which would be a better fit for someone wanting to extend an existing project rather than starting from scratch?"
- "What's the typical 1+3 vs. 4-year structure trade-off in practice?"

---

## 8. Andreas Vlachos (Cambridge CST)

**Title:** Professor
**Most recent relevant work:**
- "Zero-Shot Fact Verification via Natural Logic & LLMs" (EMNLP 2024 Findings)
- "TabVer: Tabular Fact Verification" (TACL 2024)
- "TSVer: Time-Series Evidence Verification" (2025)

**Interview pitch:**
"CiteCheck is methodologically a cousin of your fact-verification work. The CitationResolver's existence check is structurally close to evidence retrieval in fact verification; the support check is structurally close to entailment. The TSVer time-series framing might even apply if we think of overruled-precedent as time-series evidence."

**Specific extensions:**
- Adapt natural-logic methods for support-axis judgments (less noise than NLI on legal text)
- Fact-verification benchmarks crossover: CiteCheck as a domain-specific FEVER variant
- Tabular verification (TabVer) for citation tables in legal briefs

**Likely questions:**
- "How does your support metric compare to FEVER-style entailment?"
- "Have you considered natural-logic for the support axis? It tends to have lower NLI noise."
- "What's the boundary between fact verification and citation verification, in your framing?"

**Questions for him:**
- "Cambridge CST has the Faculty of Law on the same campus. Have your students collaborated with the legal side, or has it stayed CS-internal?"
- "Where do you see fact verification going as the source of evidence shifts from snippets to live API queries?"

---

## 9. Florian Matthes (TUM sebis)

**Title:** Professor
**Most recent relevant work:**
- "AGB-DE: Automated Legal Assessment of German Consumer Contracts" (ACL 2024)
- "AI-Assisted German Employment Contract Review benchmark" (2024)
- "Legal AI Use Case Radar 2024"

**Interview pitch:**
"Your German contract-law work is the closest non-US legal-NLP benchmark family to CiteCheck. The Bluebook-structure-aware approach in CiteCheck would adapt naturally to German citation formats (BGBl, NJW, etc.); the verify-loop architecture is jurisdiction-agnostic."

**Specific extensions:**
- German / EU citation grammar adapted to CiteCheck's verify loop
- Comparative US vs. German legal NLP benchmark
- Industry-academic bridge: TUM sebis has industry connections that could inform deployment-realistic evaluation

**Likely questions:**
- "Why US first? German case law has a cleaner citation grammar than US Bluebook in some ways."
- "How language-portable is your method?"
- "What's the licensing situation on CourtListener for non-US use?"

**Questions for him:**
- "The Legal AI Use Case Radar suggests practitioner deployment is a key focus. Where do you see open-weight tools like CiteCheck fitting?"
- "TUM sebis is industry-connected. What does a typical PhD-industry collaboration look like for your students?"

**Note (per Agent N flag):** the German-contract specialty is the strongest legal-NLP fit at TUM but a weaker connection to US case-law CiteCheck specifically. Consider whether Matthes is the right primary for an SOP focused on US law, or whether to reframe the SOP to emphasize comparative work.

---

## 10. Karthik Narasimhan (Princeton CS / PLI)

**Title:** Associate Professor
**Most recent relevant work:**
- "Cognitive Architectures for Language Agents" (TMLR 2024)
- "SWE-bench" (ICLR 2024)
- "SWE-agent" (2024)
- "Retaining by Doing" (2025)

**Interview pitch:**
"Your Cognitive Architectures for Language Agents paper is the closest published abstraction for CiteCheck's verify loop. SWE-agent's tool-use pattern is the design precedent for CiteCheck's CitationResolver — a specialized agent that mediates between the LLM and an external authoritative source."

**Specific extensions:**
- Cognitive-architecture extension: explicit world-model for legal reasoning (binding-vs-persuasive jurisdiction rules, holding-vs-dicta distinctions)
- SWE-agent-style benchmark for CiteCheck: long-horizon legal-research tasks requiring multi-step verification
- Retaining by Doing as a methodology for learning legal verification through interaction with CourtListener

**Likely questions:**
- "Why a single CitationResolver agent rather than a multi-agent system from the start?"
- "What's the action space — verify, retract, re-retrieve. Is that minimal? Could there be a more expressive action space?"
- "How does CiteCheck handle compound questions that span multiple citations?"

**Questions for him:**
- "Cognitive Architectures was a high-level abstraction. Where do you see it grounding out in specific verticals like legal?"
- "SWE-bench was the canonical evaluation for software-engineering agents. Do you see citation-faithfulness benchmarks playing a similar canonicalizing role for legal AI?"

---

## Cross-advisor pattern: questions that work for any interview

These are useful when an interview is going short and you need a question to keep the conversation going:

1. "What's something you wish more PhD applicants understood about this program / lab?"
2. "Among recent papers from the lab, which one are you most excited about (vs. which one got the most attention)?"
3. "How has [research area] changed in the last 12 months, in your view? What's surprised you?"
4. "What do you wish the broader research community paid more attention to that they don't?"
5. "If a new student wanted to make a contribution in their first year, what kind of project would set them up well?"

## Update protocol

Before each scheduled interview:
- [ ] Check Google Scholar for any 2027-2028 papers by the advisor (replace cited papers if newer)
- [ ] Check the lab page for current PhD students (mention one's work in conversation if relevant)
- [ ] Re-read the cited papers' abstracts at minimum
- [ ] Verify the program's stated PhD program structure (deadlines, qualifier exams, funding model) hasn't changed
