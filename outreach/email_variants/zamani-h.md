# Cold Email Draft — Prof. Hamed Zamani (UMass Amherst, CIIR)

**Recipient research focus:** Retrieval-augmented generation, conversational/agentic IR, RAG evaluation (Search-R1, LiveRAG).
**Why starred:** Leading academic on the retrieval and evaluation side of RAG; LiveRAG 2025 and multi-agent RAG work make him the best retrieval-systems fit on this list.
**Recent paper to cite:** Search-R1 / LiveRAG 2025 line of work on multi-agent and live-corpus RAG evaluation.
**Email address:** see https://groups.cs.umass.edu/zamani/
**Suggested subject line:** Live-corpus RAG evaluation for legal citation verification — prospective applicant question

---

## Email body

Dear Prof. Zamani,

I'm a Master's-level researcher preparing to apply for PhD CS programs in the Fall 2027 cycle (for Fall 2028 entry). Your work on LiveRAG and Search-R1 — particularly the insistence on evaluating RAG against a live, growing corpus rather than a frozen snapshot — is the design principle I want to inherit for a domain where the corpus (US case law) genuinely grows every day and where stale snapshots silently invalidate jurisdictional reasoning.

I'm developing a 1-page problem statement for a project called CiteCheck: an open benchmark and agentic-RAG method that scores legal-LLM outputs on three axes — (1) existence (does the cited case exist in CourtListener), (2) support (does the case stand for the asserted proposition), and (3) jurisdictional validity (is the cited authority binding for the named forum). The benchmark queries a live CourtListener instance rather than a frozen index, and the agent loop is structured around a Bluebook-aware reranker plus verifier feedback. Mata v. Avianca is the public-facing failure mode.

I would value your honest 60-second reaction — particularly whether a live-corpus, three-axis benchmark is a legitimate evaluation contribution in its own right (versus just a domain-specialized RAG paper), and whether you see an obvious confounder in measuring retrieval quality against a corpus that updates between train and test. The draft is attached.

Even a one-line response would be very valuable.

Sincerely,
John Paul L. Gabule
[Current role / affiliation]
johnpaullimgabule@gmail.com
[Link to research log / GitHub]

---

## Customization checklist (before sending)
- [ ] Pull current email address from https://groups.cs.umass.edu/zamani/ faculty page
- [ ] Re-read the Search-R1 / LiveRAG 2025 paper within the last 7 days
- [ ] Update the cited paper if a newer 2026-2027 Zamani-group paper is available at send-time
- [ ] Attach `project/problem_statement.md` as PDF
- [ ] Log the send in `outreach/log.md`

## Notes on this advisor
Strong methodological fit on the retrieval side and one of the more responsive RAG-research PIs in the US. His group is a natural home for a "legal-domain instantiation of live multi-agent RAG" framing — that framing will land better than "I want to do legal NLP." Risk: he gets a high volume of RAG-applicant email; the live-corpus angle is the differentiator that has to land in the first paragraph.
