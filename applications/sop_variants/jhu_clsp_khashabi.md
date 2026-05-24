# Statement of Purpose — Johns Hopkins CS / CLSP (Khashabi fit)

**Program:** Johns Hopkins University, Department of Computer Science (PhD), Center for Language and Speech Processing affiliation
**Advisor targets (primary):** Daniel Khashabi (CS / CLSP, Assistant Professor)
**Secondary advisors of interest:** Benjamin Van Durme (CLSP, faithfulness/semantics)
**Application deadline:** Dec 15, 2027 (typical JHU CS; verify)
**Word count target:** ~1,200 (JHU is flexible; verify)
**Draft version:** 0.1 (2026-05-25; refine during Phase 3 Task 61)

---

In May 2023 a federal judge sanctioned two New York attorneys for filing a brief in *Mata v. Avianca* that cited six judicial opinions ChatGPT had hallucinated. By early 2026 the Charlotin AI Hallucinations tracker had logged roughly fifty subsequent US court orders involving fabricated AI-generated authorities. Magesh, Surani, and Dahl (2025) showed that even commercial legal RAG tools — Lexis+ AI, Westlaw AI-Assisted Research — invent or misattribute citations 17–33% of the time. The unsettling implication is not just that LLMs fabricate; it is that they fabricate in ways the *training data was correct about at the time*. A case that was binding in 2021 may have been overruled in 2023. A reporter abbreviation that was canonical in 1995 may have shifted. The model carries the older world forward into the present without noticing. This is the slice of the citation-faithfulness problem I want to take on first.

Open research on legal RAG has three gaps. End-to-end benchmarks (LegalBench-RAG, MLEB) score retrieval quality but do not separately measure citation faithfulness. The closest open citation-faithfulness work (EL-RAG, Wankhade 2026) evaluates on non-US corpora. And no existing system treats temporal validity — was this citation binding at the time of the question? — as a first-class evaluation axis. Closing these gaps requires both a benchmark that decomposes citation failures into separable axes and a method that does generation-time verification against a live registry rather than post-hoc detection.

I propose **CiteCheck**, an open benchmark and method that scores LLM-generated US case-law citations on three axes — existence, support, and jurisdictional validity — using a CourtListener-backed agentic RAG pipeline with a Bluebook-structure-aware reranker. The benchmark seeds adversarial questions from the Charlotin tracker and from CUAD / LegalBench-RAG; the method emits citations through a constrained-decoding grammar, verifies each one via a `CitationResolver` agent tool, and retracts or re-retrieves on failure within a small iteration budget. The temporal-validity extension I want to develop during the PhD adds a fourth axis: was the cited authority *still good law* at the time of the question's date stamp? This is where Professor Khashabi's research becomes directly relevant. [INSERT SPECIFIC ACCOMPLISHMENTS — see applications/artifacts_strategy.md: planned citation-existence verifier mini-paper on arXiv (Aug 2026), eyecite open-source PRs, master's coursework in NLP / ML / IR, any RA or research-engineering experience demonstrating the independence required for a multi-month build.]

Johns Hopkins CLSP — and Professor **Daniel Khashabi** in particular — is the program whose research most directly anticipates the temporal-validity problem CiteCheck v0.2 will need to solve. Professor Khashabi's COLM 2024 Outstanding Paper "Dated Data: Tracing Knowledge Cutoffs in LLMs" framed exactly the question I will eventually need to answer for legal citations: how does an LLM trained at time *t* reason about facts that have changed between *t* and inference time? In legal AI this is the overruled-precedent problem — a citation that was valid at training but is no longer good law — and Khashabi's methodology for measuring knowledge-cutoff effects ports almost directly onto a temporal-validity axis for CiteCheck. His "TurkingBench" (2025) on web agents speaks to the agent-evaluation methodology I am using for the CiteCheck verify loop. The combination of his evaluation-methodology focus and CLSP's broader strengths in faithfulness (Van Durme's work on self-(in)correctness, the AAAI 2025 paper with Khashabi and Weller on LLM discrimination) make CLSP the right intellectual home for the next stage of this work.

Over the longer arc of a PhD I want to extend CiteCheck along the temporal-validity axis (treating "was this still good law on date X?" as a first-class evaluation question), along state-court coverage (where CourtListener data is uneven), and toward verifier-first training (closing the loop so the generator itself internalizes citation-grounding rather than relying entirely on a post-generation tool). The temporal-validity extension specifically is what makes JHU CLSP the strongest mentorship fit on my list. CiteCheck v0.1 is a starting point; the full research program is what I want to develop at Hopkins under Professor Khashabi's guidance.

---

## Customization done in this version vs. skeleton
- Opening hook adds the temporal-validity framing ("the model carries the older world forward") — connects directly to Khashabi's "Dated Data"
- Proposed approach extended with the v0.2 temporal-validity axis, which the standard skeleton does not have
- Research fit paragraph cites "Dated Data" + "TurkingBench" by name
- Van Durme cross-referenced as a secondary CLSP fit
- Closing emphasizes Khashabi as primary because of the unique temporal-validity intellectual overlap

## Still requires user input before sending
- `[INSERT SPECIFIC ACCOMPLISHMENTS]` paragraph
- Confirm JHU CS 2027 SOP word-count cap when portal opens
- Verify Khashabi still at JHU and accepting students (assistant professors sometimes move)
- Confirm the temporal-validity extension framing isn't already covered by a 2027 publication (search at submission time)
- Decide whether to apply to CS PhD or to a more language-focused track if JHU has one

## Notes
- This is the SOP where the v0.2 temporal-validity hook does the most work. If the user de-prioritizes that extension, the Khashabi fit weakens — consider whether to keep emphasizing it.
- Khashabi was one of Agent E's "top 3 most likely to respond" picks for cold email; that's consistent with the assistant-professor archetype.
