# Statement of Purpose — University of Edinburgh ILCC (Lapata fit)

**Program:** University of Edinburgh, School of Informatics — Institute for Language, Cognition and Computation (PhD)
**Advisor targets (primary):** Mirella Lapata (ILCC, Professor)
**Secondary advisors of interest:** Ivan Titov (interpretability / trustworthiness), Pasquale Minervini (neuro-symbolic / retrieval)
**Application deadline:** Varies; Edinburgh CDT-NLP cohort applications typically Jan-Feb; verify exact 2028 entry deadline
**Word count target:** ~1,200 (UK research proposals are often required as a separate document; verify)
**Co-document:** Research proposal (often 2-3 pages, separate from the personal statement)
**Draft version:** 0.1 (2026-05-25; refine during Phase 3 Task 61)

---

In 2023 a federal judge in the Southern District of New York sanctioned two attorneys for filing a brief in *Mata v. Avianca* that cited six judicial opinions ChatGPT had hallucinated. The UK has its own emerging line of cases — *Harber v. HMRC* (2023) and *Ayinde v. The London Borough of Haringey* (2025) flagged AI-fabricated authorities in tribunal filings, prompting Practice Direction-level guidance from the Bar Standards Board. The problem is jurisdiction-independent: the citation-faithfulness failure mode of retrieval-augmented generation does not respect national borders, and the published methodological responses (Magesh et al. 2025's audit of commercial US tools; EL-RAG, Wankhade 2026, on Indian / COLIEE corpora) remain narrow in geography and shallow in evaluation. A reproducible, transparently-evaluated framework for citation faithfulness — one that decomposes the problem into separable axes and exposes its uncertainty — is the contribution I want to begin in a doctoral program.

Open research on retrieval-augmented legal QA has three gaps that motivate CiteCheck. End-to-end benchmarks (LegalBench-RAG, MLEB) score retrieval quality but not citation faithfulness as a separable axis. Existing citation-faithfulness work either targets non-legal domains (CiteGuard for scientific writing) or non-US corpora (EL-RAG). And almost no open RAG system reports uncertainty alongside its answer — a particular problem in legal AI, where over-confident wrong answers are the failure mode that costs practitioners their licenses. A reproducible, multi-axis benchmark coupled with a verify-aware decomposition and explicit uncertainty quantification is the missing artifact.

I propose **CiteCheck**, an open benchmark and method for verifiable US case-law citations in retrieval-augmented generation. (US case law first because the data is freely accessible via CourtListener and the Caselaw Access Project; UK / EU extensions are explicit future work.) The benchmark scores every emitted citation on three axes — existence, support, and jurisdictional validity. The method is a three-stage agentic pipeline: hybrid BM25 + dense retrieval, a faithfulness-tuned cross-encoder reranker that exploits Bluebook citation structure, and a constrained-decoding citation grammar verified by a `CitationResolver` agent tool with retraction-or-retry. The aspect I am most interested in developing during the PhD is *aspect-aware decomposition of citation faithfulness with explicit uncertainty quantification* — treating "the system is unsure whether this citation supports the claim" as a first-class output rather than a probability swept under the rug. [INSERT SPECIFIC ACCOMPLISHMENTS — see applications/artifacts_strategy.md: planned citation-existence verifier mini-paper on arXiv (Aug 2026), eyecite open-source PRs, master's coursework in NLP / generation / IR, any prior RA or research-engineering experience.]

The University of Edinburgh's ILCC — and Professor **Mirella Lapata**'s group in particular — is the program whose recent work most directly anticipates the uncertainty-and-decomposition direction CiteCheck v0.2 should take. Professor Lapata's TACL 2024 paper "Hierarchical Indexing for Retrieval-Augmented Opinion Summarization" parallels the cross-corpus indexing CiteCheck uses for case-law retrieval. Her 2025 work on "Uncertainty Quantification in Retrieval-Augmented QA" is directly the methodology I want to extend to citation-faithfulness: replacing the binary VERIFIED / UNRESOLVABLE / NON_SUPPORTING labels with calibrated probabilities that downstream legal practitioners can use to triage outputs. And her 2025 "Decomposed Opinion Summarization with Verified Aspect-Aware Modules" demonstrates exactly the verify-aware module architecture CiteCheck implements at a smaller scale — separating retrieval, reranking, and verification into modules each with its own quality signal. The broader Edinburgh ILCC environment adds two more advisors I would value collaborating with: **Ivan Titov**'s 2024-2025 work on interpretability and model editing is directly relevant for understanding *why* CitationResolver verdicts disagree with the generator's surface confidence, and **Pasquale Minervini**'s neuro-symbolic / knowledge-intensive line of work bears on the Bluebook-grammar-as-symbolic-constraint design choice.

Over the longer arc of a PhD I want to extend CiteCheck along three Edinburgh-aware directions: explicit uncertainty propagation through the verify loop (so a low-confidence citation lowers the answer's overall confidence rather than being silently retracted); aspect-aware decomposition of the support axis itself (existence, factual support, doctrinal-holding-vs-dicta distinction, and citator-aware "good law" status as separate aspects); and a UK / EU extension once the US-jurisdiction methodology is validated (most likely as a joint project given Edinburgh's links to UK case-law data). I am applying to Edinburgh because the program's research environment, the ILCC community, and Professor Lapata's specific 2024-2025 work make it the place where this research can go furthest in the directions I most want to develop.

---

## Customization done in this version vs. skeleton
- Opening hook adds UK cases (*Harber v. HMRC* 2023; *Ayinde v. Haringey* 2025) alongside *Mata v. Avianca* — appropriate for a UK program
- Proposed approach acknowledges US-first scoping explicitly with UK/EU as future work — pre-empts the obvious "why not UK case law?" question for an Edinburgh reader
- Research fit cites Lapata's TACL 2024, 2025 Uncertainty QA, and 2025 Decomposed Opinion Summarization by name
- Closing extensions add explicit-uncertainty + aspect-aware-support directions tied to Lapata's recent line
- Titov + Minervini cross-referenced as secondary fits
- Notes the Edinburgh research-proposal-as-separate-document convention (different from US programs)

## Still requires user input before sending
- `[INSERT SPECIFIC ACCOMPLISHMENTS]` paragraph
- Verify UK cases (Harber, Ayinde) citation form and current status — the UK practice direction landscape is evolving
- Edinburgh CDT-NLP usually requires a separate ~2-3 page research proposal; this SOP is the personal statement only — confirm format
- Verify Lapata still at Edinburgh (she is also affiliated with industry through DeepMind / Cohere via consulting; check primary affiliation)
- Confirm Edinburgh ILCC PhD vs. CDT-NLP track — they have different admissions processes
- Funding: Edinburgh PhDs in NLP are often project-specific (advertised positions). Investigate whether 2027 has an advertised position in Lapata's group; if not, the application process is different (general open-call)

## Notes
- UK PhDs are typically 3-4 years and project-specific; this SOP assumes the open-call track. If a project position is advertised, the SOP needs to align to that project's framing more tightly.
- Lapata is senior (per Agent E classified as "least confident" for cold email response). But for a formal application the senior advisor is the right target.
- The uncertainty-quantification angle is the strongest single-PI fit on the list; if user de-prioritizes that, the Edinburgh fit weakens.
