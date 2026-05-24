# SOP Narrative Skeleton — CiteCheck Research Vision

**Version:** 0.1 (draft for per-program tailoring)
**Last updated:** 2026-05-25
**Status:** Reusable narrative core; customize sections marked `[CUSTOMIZE]` per program

---

## Opening hook (paragraph 1, ~150 words)

In May 2023, a federal judge in the Southern District of New York sanctioned two attorneys for filing a brief in *Mata v. Avianca* that cited six judicial opinions that did not exist. The citations were syntactically flawless — proper Bluebook form, plausible reporters, real-looking docket numbers — but they had been hallucinated by ChatGPT, and neither the attorneys nor opposing counsel could verify them until the court did. By early 2026, the Charlotin AI Hallucinations tracker has logged roughly fifty US court orders involving fabricated AI-generated authorities, and Magesh et al. (2025) showed that even commercial legal RAG systems — Lexis+ AI, Westlaw AI-Assisted Research, marketed as hallucination-free — invent or misattribute case law between 17% and 33% of the time. The legal profession is encountering an AI verifiability crisis with real consequences for sanctions, malpractice, and access to justice, and the research community has so far ceded the problem to closed proprietary vendors. That is the gap I want my doctoral work to close.

## Problem framing (paragraph 2, ~200 words)

The state of open research on legal RAG is unsatisfying in three specific ways. First, the most widely cited evaluation of commercial legal AI — Magesh et al. (2025) — was conducted on closed systems with closed prompts, so no one outside the vendors can reproduce, ablate, or improve on those numbers. Second, the leading open legal-RAG benchmarks either evaluate retrieval quality without separately scoring citation existence and propositional support (LegalBench-RAG, Pipitone & Houir Alami, 2024), or they focus on European corpora and entity linking rather than US case-law citation verification (EL-RAG, Wankhade et al., 2026). Third, the existing evaluation framing treats a hallucinated citation as a single failure mode, when in practice it decomposes into at least three distinct errors: the cited case does not exist; it exists but does not stand for the asserted proposition; or it exists and supports the proposition but comes from a non-binding jurisdiction. Conflating these three has masked which failure mode dominates in different generator families. A reproducible, US-grounded, three-axis benchmark with an open-weight baseline method is the missing artifact, and building it is a tractable, fundable doctoral program — not a single paper.

## Proposed research direction (paragraph 3, ~250 words)

I propose **CiteCheck**, an open benchmark and method for verifiable US case-law citations in retrieval-augmented generation. The benchmark scores every emitted citation on three axes: **existence** (does the citation resolve to a real opinion in CourtListener?), **support** (does the cited passage entail the proposition the model asserts it stands for?), and **jurisdictional validity** (is the cited authority binding or merely persuasive for the forum the brief addresses?). The method is an agentic RAG pipeline that, at decode-time, calls a CitationResolver tool against a live CourtListener mirror, retracts citations that fail existence, and reranks the remainder with a faithfulness-tuned reranker that exploits Bluebook structure (reporter, volume, page, court, year) as a hard constraint rather than treating the citation as opaque text. I want to be honest about scope: CiteCheck v1 will cover federal appellate and Supreme Court opinions, not the long tail of state trial courts where coverage in CourtListener is uneven; the support axis will rely on natural-language inference over headnotes, which is a known weak proxy for the legal notion of "standing for a proposition"; and the agentic retraction step trades latency for reliability in a way that some downstream uses cannot afford. These limitations are themselves a research agenda. Target venues for the first two papers are NLLP@EMNLP 2027 and TrustNLP@NAACL 2027, with an arXiv pre-release of the benchmark earlier to invite community contribution before the conference cycle.

## Background and preparation (paragraph 4, ~200 words)

My preparation for this work is Master's-level applied AI rather than core ML theory, and I think that orientation is the right one for the problem. CiteCheck is fundamentally a systems-and-evaluation contribution — corpus construction, tool-augmented inference, careful three-axis scoring — and it rewards the kind of engineering-disciplined empirical research my training emphasized. `[INSERT SPECIFIC ACCOMPLISHMENTS — list 3-4 concrete items here, drawn from: (a) Master's thesis or capstone topic and one specific technical result; (b) NLP / IR / RAG coursework with the actual project you built, not just course numbers; (c) any open-source contributions to libraries the legal-NLP community uses (HuggingFace datasets, LangChain, LlamaIndex, sentence-transformers); (d) research assistantships, industry internships, or kaggle/shared-task placements where you did the work end-to-end; (e) any publication, even workshop or non-archival — name it]`. The skills that transfer most directly to CiteCheck are: building reproducible evaluation harnesses, working with messy legal-domain text (citation parsers, court-name normalization, jurisdictional taxonomies), fine-tuning rerankers on faithfulness signals, and the patience to do careful annotation rather than rely on synthetic labels. I do not yet have a publication in a top-tier venue; that is exactly what the PhD is for.

## Research fit (paragraph 5, ~200 words)

I am applying to programs that combine strong NLP / IR foundations with serious applied-AI infrastructure and, where possible, an active law-and-technology presence. CiteCheck specifically benefits from three things a PhD environment provides that an independent researcher cannot easily assemble: sustained access to a faculty advisor who can push back on benchmark-design choices before they bake in, a cohort of NLP peers working on adjacent faithfulness and tool-use problems, and the institutional credibility to engage with law-school clinics, public defenders, and court-data providers who will not otherwise share data with an unaffiliated person.

`[CUSTOMIZE-ADVISOR — write 2-3 sentences here. Name one advisor (occasionally two if their work is genuinely complementary). Cite one specific recent paper of theirs by title and year. State concretely how a piece of CiteCheck connects to that line of work.]`

> **Worked example, Stanford (RegLab):** Professor Daniel Ho's and Professor Julian Nyarko's work on auditing legal AI (Magesh et al., 2025, *Hallucination-Free? Assessing the Reliability of Leading AI Legal Research Tools*) is the direct empirical precursor to CiteCheck, and RegLab's combination of CS, law, and policy makes it the natural environment to extend that evaluation from closed commercial systems to open, reproducible benchmarks with a method attached. I would hope to discuss the support-axis design with Professor Nyarko in particular, given his work on legal-language entailment.

> **Worked example, University of Edinburgh (ILCC):** The Institute for Language, Cognition and Computation has a long line of work on grounded and faithful generation, and Professor Mirella Lapata's work on factuality in summarization (e.g., Maynez et al., 2020, on faithfulness in abstractive summarization) maps cleanly onto the support-axis problem in CiteCheck: a hallucinated case citation is a faithfulness failure of a particular structured kind. Edinburgh's strength in evaluation methodology and its proximity to the UK legal-tech ecosystem would let CiteCheck extend to the EWCA/UKSC corpus as a natural second-year project.

`[PROGRAM-SPECIFIC HOOK — 1-2 additional sentences on the program's environment: lab affiliation, relevant centers, location-relevant courts or case law, compute resources, or named industry partnerships.]`

## Long-term vision and closing (paragraph 6, ~150 words)

CiteCheck is the first project, not the program. The same three-axis evaluation framework — existence, support, validity — generalizes to other high-stakes citation domains: medical literature in clinical decision support, statutory and regulatory citations beyond case law, and (the harder problem) real-time citation to legislation that has been amended or repealed since a model's training cutoff. By year three I would expect to extend the work to multi-jurisdictional legal systems where the binding-vs-persuasive distinction is genuinely difficult (UK Supreme Court vs. devolved courts, EU vs. member-state law), and by year five to the harder question of *temporal* citation validity in a world of continuously updated legal databases. The through-line is verifiable generation in domains where being plausibly wrong is worse than being clearly uncertain, and I would like to do that work in a program that takes both the NLP and the public-interest sides of it seriously.

---

## Per-program customization checklist

For each application, replace:
- [ ] `[INSERT SPECIFIC ACCOMPLISHMENTS]` — your concrete background bullets (3-4 specific items)
- [ ] `[CUSTOMIZE-ADVISOR]` — 2-3 sentences citing a specific advisor's paper and connecting to CiteCheck
- [ ] `[PROGRAM-SPECIFIC HOOK]` — 1-2 sentences on the program's environment (lab, resources, location-relevant courts/case law)
- [ ] Opening hook: keep the *Mata v. Avianca* framing OR switch to a program-locally-relevant case if known (e.g., a UK case for Cambridge/Oxford applications such as *Ayinde v. The London Borough of Haringey* (2025) or *Harber v. HMRC* (2023), where fabricated AI authorities were flagged)
- [ ] Trim or expand the worked-example advisor block — the final SOP should have ONE advisor section, not two; the second example above is for reference only and must be removed in the per-program version

## Notes on tone

- Specific, not flowery
- Cites real papers in-text (the SOP reviewer is a working academic)
- ~1000-1200 words for the final per-program version
- No "I have always been fascinated by..."
- No "passion" language
- First-person but research-forward, not autobiographical-forward
- Acknowledge limitations of CiteCheck honestly in the vision section (gives credibility)

## Anti-patterns to avoid

- Starting with childhood interest in computers
- "My journey into AI began when..."
- Listing courses as a CV substitute
- Claiming to want to "advance the field" without specifying which gap
- Mentioning more than 1-2 advisors per program (looks like spray-and-pray)
- Discussing GRE / GPA in the SOP body (those go in the application form)
- Citing only the same 2-3 papers as everyone else (LegalBench, RAG original) — show range

## References cited in the skeleton (verify and keep in your reading list)

- Magesh, V., Surani, F., Dahl, M., Suzgun, M., Manning, C. D., & Ho, D. E. (2025). *Hallucination-Free? Assessing the Reliability of Leading AI Legal Research Tools*. (RegLab / Stanford HAI working paper, cited in the opening and worked-example sections.)
- Pipitone, N., & Houir Alami, G. (2024). *LegalBench-RAG: A Benchmark for Retrieval-Augmented Generation in the Legal Domain*. arXiv.
- Wankhade, M., et al. (2026). *EL-RAG: Entity-Linking-Augmented RAG for European Legal Texts*. (Confirm exact author list and venue before citing in the per-program SOP.)
- Cheong, I., et al. (2025). *Access-to-justice implications of generative AI in legal services*. (Confirm exact citation; used to anchor the public-interest framing if you choose to expand paragraph 1 in a program that emphasizes law-and-policy work.)
- *Mata v. Avianca, Inc.*, 22-cv-1461 (S.D.N.Y. June 22, 2023) (Castel, J.).
- Charlotin, D. *AI Hallucinations Tracker* (https://www.damiencharlotin.com/hallucinations/). Running tally referenced for the ~50-case figure; cite as accessed-on date in the per-program SOP.
- Maynez, J., Narayan, S., Bohnet, B., & McDonald, R. (2020). *On Faithfulness and Factuality in Abstractive Summarization*. ACL. (Used only in the Edinburgh worked example; swap out for the actual advisor's paper at other programs.)
