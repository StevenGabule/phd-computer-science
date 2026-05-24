# Cold Email Draft — Prof. Karthik Narasimhan (Princeton, PLI)

**Recipient research focus:** Language agents, agent architectures, tool-use, and benchmarks for autonomous LLM systems (SWE-agent, Cognitive Architectures for Language Agents).
**Why starred:** SWE-agent and Cognitive Architectures for Language Agents are the closest published analog to "agentic RAG over case law" — same pattern of LLM + structured external environment + verifier loop.
**Recent paper to cite:** "SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering" and "Cognitive Architectures for Language Agents."
**Email address:** see Princeton CS / PLI faculty directory
**Suggested subject line:** Agent-environment interface for case-law verification — prospective applicant question on SWE-agent

---

## Email body

Dear Prof. Narasimhan,

I'm a Master's-level researcher preparing to apply for PhD CS programs in the Fall 2027 cycle (for Fall 2028 entry). Your SWE-agent paper — specifically the argument that the *interface* between the LLM and its environment, not the LLM itself, is often the bottleneck for agent performance — is the design principle I'm trying to take seriously for an agent that has to interact with a real case-law database rather than a code repository.

I'm developing a 1-page problem statement for a project called CiteCheck: an open benchmark and agentic-RAG method that scores legal-LLM outputs on three independent axes — (1) existence of the cited case in CourtListener, (2) support (does the case stand for the asserted proposition), and (3) jurisdictional validity (binding for the named forum). The agent's "environment" is a live CourtListener instance plus a Bluebook-aware structural parser; the SWE-agent insight pushes me to treat the design of that interface (what fields the agent sees, what actions it can take, what feedback it receives) as a first-class research artifact rather than an implementation detail. The public-facing failure mode is Mata v. Avianca.

I would value your honest 60-second reaction — particularly whether the agent-environment-interface frame from SWE-agent transfers cleanly to a database-as-environment setting, and whether you see an obvious flaw in evaluating the agent on three orthogonal axes rather than on a single end-to-end task-completion metric of the kind your benchmarks favor. The draft is attached.

Even a one-line response would be very valuable.

Sincerely,
John Paul L. Gabule
[Current role / affiliation]
johnpaullimgabule@gmail.com
[Link to research log / GitHub]

---

## Customization checklist (before sending)
- [ ] Verify current email from Princeton CS / PLI faculty directory
- [ ] Re-read SWE-agent (and skim Cognitive Architectures for Language Agents) within the last 7 days
- [ ] Update the cited paper if a newer 2026-2027 PLI paper is available at send-time
- [ ] Attach `project/problem_statement.md` as PDF
- [ ] Log the send in `outreach/log.md`

## Notes on this advisor
Methodological fit is strong on the agent-architecture side and Princeton PLI is an obvious fit for a "language agents in a verified environment" framing. Risk: he is a very high-profile assistant prof with substantial industry pull (now also affiliated with Sierra), so inbound is heavy; the email has to differentiate from generic "I want to do agents" applicants within the first sentence, which the agent-environment-interface angle does. Likely to skim, possible to reply.
