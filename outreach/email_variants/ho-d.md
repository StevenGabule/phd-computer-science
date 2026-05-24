# Cold Email Draft — Prof. Daniel E. Ho (Stanford RegLab)

**Recipient research focus:** Empirical legal NLP, regulation, and rigorous evaluation of legal LLMs (LegalBench, hallucination audits).
**Why starred:** Most influential figure in US legal NLP and the senior author of the LegalBench / hallucination work that defines what credible evaluation in this area looks like.
**Recent paper to cite:** "Hallucinating Law: Legal Mistakes with Large Language Models are Pervasive" (2025) and the companion "A Reasoning-Focused Legal Retrieval Benchmark" (2025).
**Email address:** see https://reglab.stanford.edu/ (Stanford faculty directory listing)
**Suggested subject line:** Verifying citations vs. propositions — prospective PhD applicant question on your hallucination audit

---

## Email body

Dear Prof. Ho,

I'm a Master's-level researcher preparing to apply for PhD CS programs in the Fall 2027 cycle (for Fall 2028 entry). Your 2025 paper "Hallucinating Law" — and specifically the finding that even bespoke "legal" tools from LexisNexis and Thomson Reuters still hallucinate on roughly one in six benchmark queries despite RAG grounding — is what convinced me that surface-level retrieval grounding is not enough, and that citation verification has to be evaluated on its own axes.

I'm developing a 1-page problem statement for an open benchmark and agentic-RAG method called CiteCheck, which scores legal-LLM outputs on three independent axes: (1) existence of the cited case in CourtListener, (2) support — whether the case actually stands for the asserted proposition, and (3) jurisdictional validity — whether the cited authority is binding for the stated forum. The method pairs live CourtListener lookups with a Bluebook-structure-aware reranker. The Mata v. Avianca sanctions are the public-facing hook.

I would value your honest 60-second reaction — particularly whether splitting existence / support / jurisdiction as separable evaluation axes is the right decomposition, and whether you see an obvious flaw in benchmarking against CourtListener rather than a curated Westlaw subset (as your reasoning-focused retrieval benchmark uses). The draft is attached.

I understand your time is extremely limited; even a one-line response would be enormously helpful.

Thank you for considering it.

Sincerely,
John Paul L. Gabule
[Current role / affiliation]
johnpaullimgabule@gmail.com
[Link to research log / GitHub]

---

## Customization checklist (before sending)
- [ ] Verify email address from current Stanford Law / RegLab faculty page
- [ ] Re-read "Hallucinating Law" within the last 7 days; double-check the 1-in-6 figure against the paper before claiming it
- [ ] Update the cited paper if a newer 2026-2027 RegLab paper is available at send-time
- [ ] Attach `project/problem_statement.md` as PDF
- [ ] Log the send in `outreach/log.md`

## Notes on this advisor
Highest-prestige, lowest-response-probability target on the list — he is inundated and rarely takes new direct-admit PhD students from cold email. The realistic win condition is not "supervises me" but "responds with a 1-line steer," which is still extremely valuable. If he replies even tersely, that signal is worth more than a long reply from a more available advisor. Sending to him is correct; expecting a reply is not.
