# Problem Statement — CiteCheck

**Working title:** CiteCheck — An Open Benchmark and Agentic-RAG Method for Verifiable US Case-Law Citations
**Version:** 0.1 (draft — for refinement during deep reads Jun-Jul 2026)
**Status:** **AWAITING M2 LOCK** (target lock date: 2026-08-31)
**Source:** Primary candidate from `project/candidates.md`. Full implementation detail in `project/citecheck_design.md`.

---

## Problem

Open-weight legal RAG systems routinely emit case citations that look syntactically correct in Bluebook form ("Smith v. Jones, 412 F.3d 567 (9th Cir. 2005)") but refer to cases that do not exist or do not support the claim. In *Mata v. Avianca* (S.D.N.Y. 2023), two attorneys were sanctioned for filing a brief containing six fabricated ChatGPT-generated citations; the Charlotin tracker has since logged ~50 similar US court orders. Magesh et al. (2025) showed proprietary tools (Lexis+, Westlaw) hallucinate 17–33% of the time but release no open benchmark, baseline, or method.

## Why this matters

Junior associates, public defenders, and pro-bono attorneys are the populations most exposed to fabricated citations and least able to afford proprietary tooling (Cheong et al., 2025). Without an open, reproducible US-case-law-grounded benchmark and an open method to drive the fabrication rate down, the field cedes the problem to closed vendors whose error rates remain unverifiable.

## Why agentic RAG is the right approach

Static RAG retrieves passages but cannot verify whether emitted citations correspond to real opinions — the generator may invent a plausible Bluebook citation from retrieved cases without matching any of them. Agentic RAG adds a `CitationResolver` tool that queries CourtListener at decode-time, plus a retraction-or-re-retrieval loop, turning citation faithfulness into a generation-time constraint rather than a post-hoc check.

## Proposed approach

A three-stage pipeline over Llama-3.1-8B / Qwen2.5-7B with QLoRA: (1) hybrid BM25 + dense retrieval over a Caselaw Access Project corpus; (2) a cross-encoder reranker fine-tuned with a Bluebook-structure-aware citation-grounding loss (`eyecite` parses); (3) at generation, citations emitted via a constrained-decoding grammar and verified via a `CitationResolver` tool against the CourtListener API plus a local CAP mirror. Novel contributions: the Bluebook-aware rerank loss + live-registry verification loop.

## Evaluation plan

Datasets: Caselaw Access Project, CourtListener API, LegalBench-RAG, CUAD, plus ~500 constructed question/gold-citation pairs (seeded from Charlotin tracker). Baselines: Vanilla 8B, naive RAG, Self-RAG, CRAG, EL-RAG (reimpl), GPT-4o-mini with web search. Primary metrics: Citation Resolution Rate, Citation Support F1 (NLI + 200-item human audit), Jurisdictional Validity, Fabrication Rate.

## Risks and contingencies

- **Annotation balloon** → seed adversarial cases from Charlotin tracker; release v0.1 with 500 items rather than 1000.
- **Scoop risk (Butler & Butler 2026)** → differentiate on open-weight + open-data + agent-tool-loop combination.
- **CourtListener rate limits** → mirror CAP locally (~100GB), cache resolver calls.

## Timeline alignment

| Milestone | Date | Deliverable |
|---|---|---|
| M3 | Nov 2026 | Baseline reproduction (2-3 methods) |
| M4 | Feb 2027 | Novel contribution prototyped |
| M5 | May 2027 | Full experiments + ablations |
| M6 | Jul 2027 | Paper draft v1 |
| M7 | Sep 2027 | NLLP @ EMNLP 2027 submission + arXiv |

## References (most load-bearing)

1. Magesh et al. (2025). *J. Empirical Legal Studies*, 22(2), 216-242. https://doi.org/10.1111/jels.12413
2. Wankhade (2026). EL-RAG. https://doi.org/10.21203/rs.3.rs-8947587/v1
3. Pipitone & Houir Alami (2024). LegalBench-RAG. https://doi.org/10.48550/arxiv.2408.10343
4. Guha et al. (2022). LegalBench. https://doi.org/10.48550/arxiv.2209.06120
5. Cheong et al. (2025). AI + Access to Justice. https://doi.org/10.48550/arxiv.2510.22933
6. *Mata v. Avianca, Inc.*, 22-cv-1461 (S.D.N.Y. June 22, 2023).

**See `project/citecheck_design.md` for full method details, dataset notes, baseline citations, complete metric justifications, and detailed risk register.**
