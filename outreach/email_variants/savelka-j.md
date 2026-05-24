# Cold Email Draft — Dr. Jaromír Šavelka (Carnegie Mellon University)

**Recipient research focus:** Applying LLMs to legal text — annotation, case-law analysis, summarization evaluation — with a combined CS + JD background.
**Why starred:** Research faculty at CMU with the rare CS+JD profile; his work on zero-shot legal annotation and argumentation-aware summarization evaluation is methodologically adjacent to CiteCheck's structure-aware verification.
**Recent paper to cite:** "Unreasonable Effectiveness of Large Language Models for Low-Resource and Domain-Specific Legal Text Annotation" (2023) and "Adding argumentation into the evaluation of legal summarization" (2024).
**Email address:** jsavelka@cs.cmu.edu
**Suggested subject line:** Structure-aware evaluation of legal LLM outputs — prospective applicant seeking 60s of feedback

---

## Email body

Dear Dr. Šavelka,

I'm a Master's-level researcher preparing to apply for PhD CS programs in the Fall 2027 cycle (for Fall 2028 entry). Your 2024 paper on adding argumentation into the evaluation of legal summarization — specifically the move away from purely surface-level summary metrics toward evaluating whether the argumentative structure of a judicial opinion is preserved — is the kind of structure-aware evaluation I'm trying to apply to citation verification rather than summarization.

I'm developing a 1-page problem statement for a project called CiteCheck: an open benchmark and agentic-RAG method that scores legal-LLM outputs on three independent axes — (1) existence of the cited case in CourtListener, (2) support (does the case stand for the asserted proposition), and (3) jurisdictional validity (is the cited authority binding for the named forum). The reranker is Bluebook-citation-structure-aware in the same spirit your evaluator is argumentation-structure-aware, and the public hook is the Mata v. Avianca sanctions.

I would value your honest 60-second reaction — particularly whether the Bluebook-aware reranker is a productive specialization or whether a general-purpose dense retriever fine-tuned on case-law would dominate it, and whether you see an obvious annotation bottleneck given the experience reported in your zero-shot annotation work. The draft is attached.

Even a one-line response would be very valuable.

Sincerely,
John Paul L. Gabule
[Current role / affiliation]
johnpaullimgabule@gmail.com
[Link to research log / GitHub]

---

## Customization checklist (before sending)
- [ ] Verify jsavelka@cs.cmu.edu is current on CMU CS directory
- [ ] Re-read the 2024 argumentation-evaluation paper within the last 7 days
- [ ] Update the cited paper if a newer 2026-2027 paper is available at send-time
- [ ] Attach `project/problem_statement.md` as PDF
- [ ] Log the send in `outreach/log.md`

## Notes on this advisor
Probably the single most likely advisor on this list to write back substantively: research-track faculty (so less inundated than tenure-track stars), specialized in exactly this area, and known for being responsive to applied legal-NLP work. Risk: as research faculty his ability to admit/fund a primary PhD student varies by year, so any reply that opens a conversation should be followed up by asking who the natural CS-tenure-track co-advisor would be at CMU.
