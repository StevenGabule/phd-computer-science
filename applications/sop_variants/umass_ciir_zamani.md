# Statement of Purpose — UMass Amherst CICS / CIIR (Zamani fit)

**Program:** University of Massachusetts Amherst, Manning College of Information and Computer Sciences (PhD), Center for Intelligent Information Retrieval affiliation
**Advisor targets (primary):** Hamed Zamani (CICS / CIIR Associate Director, Associate Professor)
**Secondary advisors of interest:** James Allan (CIIR Director, Distinguished Professor)
**Application deadline:** Dec 15, 2027 (typical UMass CICS; verify)
**Word count target:** ~1,200 (UMass is flexible)
**Draft version:** 0.1 (2026-05-25; refine during Phase 3 Task 61)

---

In May 2023 a federal judge sanctioned two attorneys in *Mata v. Avianca* for filing a brief containing six citations ChatGPT had fabricated. By early 2026 the Charlotin AI Hallucinations tracker had logged roughly fifty similar US court orders. Magesh, Surani, and Dahl (2025) measured 17–33% citation-hallucination rates on commercial legal AI tools (Lexis+, Westlaw). The proximate cause of these failures is almost always the retrieval-and-generation seam: the retriever returns plausible but irrelevant passages, the generator stitches together a citation-shaped string from those passages, and no component checks whether the resulting citation refers to a real opinion. The deeper failure is that we evaluate end-to-end RAG systems with single-axis metrics (token-F1, exact match) that conflate retrieval quality, generation quality, and verification — when in legal practice these are three distinct failure modes with three distinct mitigations. Disentangling them is the work I want to do.

Open research on legal RAG has three concrete gaps. Existing benchmarks (LegalBench-RAG, MLEB) score retrieval quality at the passage level but cannot tell us whether the *citations* the generator emits resolve to real opinions, support the asserted claims, or come from binding jurisdictions. Open methodological work (EL-RAG, Wankhade 2026) targets non-US corpora and uses static alignment rather than live-registry verification. And the retrieval-side techniques that would most help — hybrid sparse-dense fusion, faithfulness-aware reranking, multi-hop retrieval over cross-corpus indexes — have been developed mostly outside the legal domain. A reproducible, US-grounded, retrieval-aware benchmark plus a method that puts the retrieval improvements at the center is the missing artifact.

I propose **CiteCheck**, an open benchmark and method that scores LLM-generated US case-law citations on three axes — existence (does it resolve in CourtListener?), support (does the resolved opinion entail the claim?), and jurisdictional validity (binding for the forum?). The method is a three-stage pipeline: hybrid BM25 + dense retrieval over a Caselaw Access Project index fused with Reciprocal Rank Fusion; a cross-encoder reranker fine-tuned with a multi-objective loss that combines query-passage relevance with a citation-grounding signal (Bluebook fields parsed via `eyecite` and resolved through the CourtListener API); and a constrained-decoding citation grammar verified by a `CitationResolver` agent tool with retraction-or-retry. The retrieval architecture is the part of the system I find most interesting from an IR perspective, and the multi-objective reranker loss is the methodological contribution where I expect the most insight from working in CIIR. [INSERT SPECIFIC ACCOMPLISHMENTS — see applications/artifacts_strategy.md: planned citation-existence verifier mini-paper on arXiv (Aug 2026), eyecite open-source PRs, master's coursework in IR / NLP / ML, any prior RA experience with retrieval systems or large-scale indexing.]

UMass CICS — and the Center for Intelligent Information Retrieval (CIIR) under Professor **Hamed Zamani**'s leadership — is the program whose research most closely aligns with CiteCheck's retrieval-architecture choices. Professor Zamani's SIGIR 2024 paper "Stochastic RAG" and the 2024 work on "Evaluating Retriever in RAG" both directly inform how I think about the BM25-plus-dense-fusion design in CiteCheck. His more recent COLM 2025 work on "Search-R1" and the CIIR@LiveRAG 2025 multi-agent RAG paper extend exactly along the trajectory CiteCheck will follow as it grows from a single-agent verify loop into a more sophisticated multi-agent system (one agent for retrieval, one for verification, one for jurisdiction reasoning). I would value the chance to develop CiteCheck under Professor Zamani's guidance with the broader CIIR community as a sounding board for the retrieval-evaluation questions that emerge from a citation-centric benchmark (how should we measure retrieval quality when the right answer is not a passage but a citation chain?). CIIR's history under Professor James Allan as the canonical home of TREC-style evaluation methodology adds a layer of evaluation discipline that few other groups can match.

Over the PhD I want to extend CiteCheck along three directions that all sit squarely in CIIR's research neighborhood. First, multi-agent retrieval (Zamani's CIIR@LiveRAG line of work) — separating the citation-resolver, the jurisdiction-reasoner, and the precedent-tracer into specialized agents that share a retrieval substrate. Second, retrieval-evaluation methodology for citation-centric benchmarks: TREC-style benchmark construction, but the relevance unit is a cited authority chain, not a passage. Third, query-side analysis: which question types most reliably surface citation hallucinations, and can we route them to a stronger retrieval path? These are all questions CIIR is uniquely positioned to ask. UMass is the program where I can take CiteCheck the furthest along the retrieval-architecture axis.

---

## Customization done in this version vs. skeleton
- Problem framing pivots from "fabricated citations" to "the retrieval-and-generation seam" — more retrieval-flavored
- Proposed approach emphasizes the BM25 + dense + RRF + multi-objective reranker over the agent loop (Stanford SOP does the opposite weighting)
- Research fit cites Zamani's Stochastic RAG (SIGIR 2024), Evaluating Retriever in RAG (SIGIR 2024), Search-R1 (COLM 2025), and CIIR@LiveRAG 2025 by name
- Closing extensions are retrieval-evaluation flavored: TREC-style methodology, query-side analysis, multi-agent retrieval
- Allan cross-referenced as CIIR Director with evaluation-discipline pedigree

## Still requires user input before sending
- `[INSERT SPECIFIC ACCOMPLISHMENTS]` paragraph (especially the IR coursework / RA experience)
- Confirm UMass CICS 2027 SOP word-count cap
- Verify Zamani still at UMass and accepting students
- Confirm whether to apply to CICS PhD directly or to a CIIR-specific track if one exists

## Notes
- UMass CIIR is the retrieval-focused alternative to a more general NLP program. If the user pivots toward seeing CiteCheck as fundamentally an IR system rather than an agent system, this SOP becomes the strongest fit on the list.
- Zamani is the strongest pure-retrieval mentorship fit per Agent E's top-10 starred analysis. The framing here leans into that.
