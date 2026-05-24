# Cold Email Draft — Prof. Andreas Vlachos (University of Cambridge, CST)

**Recipient research focus:** Automated fact verification, claim decomposition, evidence retrieval, and dialogue.
**Why starred:** Fact verification is the direct methodological cousin of citation verification — a claim, an evidence corpus, and a structured verdict — and his 2024-2025 work has continued to push the evidence-retrieval-plus-verdict pipeline that CiteCheck specializes to law.
**Recent paper to cite:** His 2024-2025 line of work on automated fact verification with explicit evidence retrieval and structured verdicts (FEVER / AVeriTeC continuation).
**Email address:** see https://www.cst.cam.ac.uk/people/av308
**Suggested subject line:** Legal citation verification as structured fact verification — prospective applicant question

---

## Email body

Dear Prof. Vlachos,

I'm a Master's-level researcher preparing to apply for PhD CS programs in the Fall 2027 cycle (for Fall 2028 entry). Your sustained work on automated fact verification — particularly the framing of verification as evidence-retrieval-plus-structured-verdict, rather than a single fused entailment judgment — is the methodological template I want to specialize to legal citations, where the "claim" is a cited case + a proposition and the "evidence" is the opinion text itself.

I'm developing a 1-page problem statement for a project called CiteCheck: an open benchmark and agentic-RAG method that scores legal-LLM outputs on three independent axes — (1) existence (does the cited case exist in CourtListener), (2) support (does the case stand for the asserted proposition — essentially a claim-verification step over the opinion text), and (3) jurisdictional validity (is the cited authority binding for the named forum, which is a structured deductive check rather than an NLI one). The Mata v. Avianca sanctions are the public-facing failure mode.

I would value your honest 60-second reaction — particularly whether splitting "existence" and "support" as separate axes is the right call (in fact-verification benchmarks they often collapse into NEI vs SUPPORTS), and whether you see jurisdictional validity as a legitimate third axis or as a domain-specific filter that should sit outside the verification pipeline entirely. The draft is attached.

Even a one-line response would be very valuable.

Sincerely,
John Paul L. Gabule
[Current role / affiliation]
johnpaullimgabule@gmail.com
[Link to research log / GitHub]

---

## Customization checklist (before sending)
- [ ] Pull current email from https://www.cst.cam.ac.uk/people/av308
- [ ] Identify the specific 2024-2025 Vlachos-group paper to cite by exact title before sending; do not send with the generic "your sustained work" phrasing
- [ ] Re-read that paper within the last 7 days
- [ ] Attach `project/problem_statement.md` as PDF
- [ ] Log the send in `outreach/log.md`

## Notes on this advisor
Methodologically one of the cleanest fits on the list: legal citation verification is almost a special case of his research program. The framing question he is most likely to push back on — whether existence and support should be separate axes — is exactly the right question to invite, because his answer materially improves the benchmark design. Risk: Cambridge PhD admissions are heavily funding-bound and his group is competitive. Before sending, I (the user) should swap the placeholder paper reference for a specific 2024-2025 title; this is the only email in the set where I did not lock the exact title in advance.
