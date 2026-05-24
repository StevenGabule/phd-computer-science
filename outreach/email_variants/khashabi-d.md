# Cold Email Draft — Prof. Daniel Khashabi (Johns Hopkins, CLSP)

**Recipient research focus:** Evaluation of LLMs, temporal/contextual robustness, agents, and crowdsourcing-style benchmarks.
**Why starred:** Assistant professor whose "Dated Data" and TurkingBench work signal serious interest in evaluation and agent settings; outstanding-paper track record suggests rigor that would sharpen CiteCheck's benchmark design.
**Recent paper to cite:** "Dated Data: Tracing Knowledge Cutoffs in Large Language Models" and "TurkingBench: A Challenge Benchmark for Web Agents."
**Email address:** see https://danielkhashabi.com/
**Suggested subject line:** Temporal validity in legal RAG benchmarks — prospective applicant question on Dated Data

---

## Email body

Dear Prof. Khashabi,

I'm a Master's-level researcher preparing to apply for PhD CS programs in the Fall 2027 cycle (for Fall 2028 entry). Your "Dated Data" paper — the finding that effective knowledge cutoffs are systematically earlier than the nominal cutoffs vendors report, and that this distortion is largest for slow-changing reference material — is directly relevant to the benchmark I'm designing, where the "ground truth" (US case law) keeps changing after the model's cutoff and the cost of a stale answer is a sanctioned attorney rather than a wrong trivia answer.

I'm developing a 1-page problem statement for a project called CiteCheck: an open benchmark and agentic-RAG method that scores legal-LLM outputs on three axes — (1) existence (does the cited case exist in CourtListener), (2) support (does it stand for the asserted proposition), and (3) jurisdictional validity (binding for the named forum). The verification loop queries a live CourtListener instance, which means the temporal-cutoff confound you characterized in "Dated Data" shows up explicitly as one of the metrics the benchmark has to be robust to. The Mata v. Avianca sanctions are the public failure mode.

I would value your honest 60-second reaction — particularly whether the three-axis decomposition is a sensible way to disentangle parametric-knowledge staleness from retrieval failure, and whether you see an obvious issue with treating "jurisdictional validity" as a separable axis rather than folding it into "support." The draft is attached.

Even a one-line response would be very valuable.

Sincerely,
John Paul L. Gabule
[Current role / affiliation]
johnpaullimgabule@gmail.com
[Link to research log / GitHub]

---

## Customization checklist (before sending)
- [ ] Pull current email from https://danielkhashabi.com/
- [ ] Re-read "Dated Data" within the last 7 days
- [ ] Update the cited paper if a newer 2026-2027 paper is available at send-time
- [ ] Attach `project/problem_statement.md` as PDF
- [ ] Log the send in `outreach/log.md`

## Notes on this advisor
Promising and probably responsive — assistant prof, active on evaluation/agents, and JHU CLSP is one of the more accessible top NLP groups for cold outreach. The "Dated Data" angle is genuinely sharp here because legal case law is the canonical "slow-changing reference material" his paper warned about. Risk: he is not a legal-NLP person specifically, so the email has to make the methodological transfer obvious in the opening line, not bury it in paragraph two.
