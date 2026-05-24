# Cold Email Draft — Prof. Mirella Lapata (University of Edinburgh, ILCC)

**Recipient research focus:** Summarization, retrieval-augmented generation, structured/modular generation, uncertainty in QA.
**Why starred:** Senior, highly cited, and her 2024-2025 work on RAG-for-summarization, uncertainty in retrieval-augmented QA, and verified aspect-aware modules is directly relevant to the "support" axis of CiteCheck.
**Recent paper to cite:** "Uncertainty Quantification in Retrieval-Augmented Question Answering" (2025) and "Decomposed Opinion Summarization with Verified Aspect-Aware Modules" (2025).
**Email address:** mlap@inf.ed.ac.uk
**Suggested subject line:** Per-citation uncertainty in legal RAG — prospective applicant question on your 2025 RAG-QA work

---

## Email body

Dear Prof. Lapata,

I'm a Master's-level researcher preparing to apply for PhD CS programs in the Fall 2027 cycle (for Fall 2028 entry). Your 2025 paper on uncertainty quantification in retrieval-augmented QA — particularly the result that aggregate-level confidence calibrates much better than the per-claim confidence that downstream users actually need — is the exact failure mode I'm trying to address for legal citations, where each cited case is its own atomic claim and "the overall answer is 0.8 confident" is operationally useless.

I'm developing a 1-page problem statement for a project called CiteCheck: an open benchmark and agentic-RAG method that scores legal-LLM outputs on three independent axes — (1) existence of the cited case in CourtListener, (2) support (does the case stand for the asserted proposition), and (3) jurisdictional validity (is the cited authority binding for the named forum). The decomposition is in the same spirit as your decomposed opinion-summarization work with verified aspect-aware modules: each axis is verified by a separate module, each producing its own hard signal rather than a fused score. The public-facing hook is the Mata v. Avianca sanctions.

I would value your honest 60-second reaction — particularly whether per-axis verified-module decomposition is a credible substitute for end-to-end uncertainty quantification in a high-stakes domain, and whether you see an obvious risk in equating "verified by CourtListener" with "calibrated." The draft is attached.

Even a one-line response would be very valuable.

Sincerely,
John Paul L. Gabule
[Current role / affiliation]
johnpaullimgabule@gmail.com
[Link to research log / GitHub]

---

## Customization checklist (before sending)
- [ ] Verify mlap@inf.ed.ac.uk is current on Edinburgh ILCC directory
- [ ] Re-read the 2025 uncertainty-in-RAG-QA paper within the last 7 days; double-check the per-claim-vs-aggregate calibration claim before quoting it
- [ ] Update the cited paper if a newer 2026-2027 Lapata-group paper is available at send-time
- [ ] Attach `project/problem_statement.md` as PDF
- [ ] Log the send in `outreach/log.md`

## Notes on this advisor
High-prestige, low-response-probability target similar to Daniel Ho — but the methodological alignment (decomposed verified modules, RAG uncertainty) is unusually clean. If she replies even tersely, that is a strong positive signal. Risk: Edinburgh's PhD admissions are funding-bound and very competitive; a reply is more likely to be a "this is interesting, look at our PhD application page" than an offer to engage. Sending is still correct.
