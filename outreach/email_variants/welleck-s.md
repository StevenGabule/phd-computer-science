# Cold Email Draft — Prof. Sean Welleck (Carnegie Mellon University, LTI)

**Recipient research focus:** Verification, refinement, and self-correction of LLM output; formal-reasoning-adjacent methods (Lean, premise selection).
**Why starred:** His verification/refinement methodology is the closest methodological match for CiteCheck's verifier-in-the-loop design, even though his domain is math/code rather than law.
**Recent paper to cite:** "RefineBench: Evaluating Refinement Capability of Large Language Models" (ICLR 2026) and "Premise Selection for a Lean Hammer" (ICLR 2026 Oral).
**Email address:** wellecks@cmu.edu
**Suggested subject line:** Refinement loops for citation verification — prospective applicant question on RefineBench

---

## Email body

Dear Prof. Welleck,

I'm a Master's-level researcher preparing to apply for PhD CS programs in the Fall 2027 cycle (for Fall 2028 entry). Your RefineBench paper — and especially the distinction it draws between models that revise their output and models that genuinely refine it in response to a verifier signal — directly informs the agent loop I'm trying to design for legal citation verification, where the "verifier" is an actual case-law database rather than a learned reward model.

I'm developing a 1-page problem statement for a project called CiteCheck: an open benchmark and agentic-RAG method that scores LLM legal outputs on three independent axes — (1) existence (does the cited case exist in CourtListener), (2) support (does it stand for the asserted proposition), and (3) jurisdictional validity (binding for the named forum). Each axis produces a hard, machine-checkable signal that the generator can be refined against, in the same spirit as the premise-selection setup in your Lean Hammer work, where the formal kernel is the ground truth.

I would value your honest 60-second reaction — particularly whether the refinement-vs-revision distinction from RefineBench is the right frame for legal citation editing, and whether you would expect a CourtListener-grounded verifier to give a sharp enough training signal to drive meaningful refinement, or whether the signal is too sparse. The draft is attached.

Even a one-line response would be very valuable.

Sincerely,
John Paul L. Gabule
[Current role / affiliation]
johnpaullimgabule@gmail.com
[Link to research log / GitHub]

---

## Customization checklist (before sending)
- [ ] Verify wellecks@cmu.edu is current on CMU LTI directory
- [ ] Re-read RefineBench (and skim Premise Selection for a Lean Hammer) within the last 7 days
- [ ] Update the cited paper if a newer 2026-2027 paper is available at send-time
- [ ] Attach `project/problem_statement.md` as PDF
- [ ] Log the send in `outreach/log.md`

## Notes on this advisor
Methodologically a near-perfect fit (verifier-in-the-loop) but domain-distant (math/code, not law). The honest framing here is that you are pitching a transfer of his methodology to a new domain — that is a feature, not a bug, for an assistant professor building a verification-of-LLMs research line. Likely to respond if the methodological connection lands; risk is that he reads it as "another applied person who wants me to supervise an applied project" and bounces it. Lean into the formal-verifier analogy in any follow-up.
