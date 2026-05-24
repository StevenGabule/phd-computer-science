# Interview Scenarios — Common Questions + Scripted Answers

**Use when:** Preparing for PhD admissions interviews (Jan-Mar 2028). Pair with `applications/interview_prep_template.md` and `applications/interviews/per_advisor_prep.md`.

**Format:** Each scenario has the prompt, a target answer length, key beats to hit, an example answer for the CiteCheck framing, and common pitfalls.

---

## Scenario 1: Opening — "Tell me about your research interests"

**Length:** 60 seconds (memorize, do not script-read)

**Key beats:**
1. Concrete problem (legal-tech failure scenario)
2. The research question you're already working on
3. What you'd extend during the PhD
4. Why this lab / program specifically

**Example answer:**

> "My research focus is verifiable retrieval-augmented generation for legal AI. The motivating problem is *Mata v. Avianca* — the 2023 sanctioning of two attorneys for filing a brief with six ChatGPT-fabricated case citations. Magesh et al. 2025 measured commercial legal RAG tools and found 17-33% hallucination rates. Most of the methodological response has been closed: closed systems, closed evaluation. I've been building CiteCheck, an open benchmark and method that decomposes citation faithfulness into three orthogonal axes — does the cited case exist, does the opinion support the claim, and is it from a binding jurisdiction — combined with an agentic verification loop that calls CourtListener at decode-time. During a PhD I want to extend the framework along [program-specific direction — see per_advisor_prep.md]."

**Pitfalls:**
- Reading from notes. Memorize the rhythm.
- Starting with "I have always been interested in..." Skip the autobiography.
- Going past 90 seconds. The interviewer signals to move on if you do; respect the timing.

---

## Scenario 2: Why a PhD? (vs. industry, MS, work)

**Length:** 60-90 seconds

**Key beats:**
1. What you can do in a PhD that you can't in industry
2. Why now (vs. 5 years from now)
3. Specific things you want a PhD program to give you (not just a credential)

**Example answer:**

> "Three things a PhD would give me that industry roles I've seen wouldn't. First, time horizon: CiteCheck v0.1 is a workshop paper; the research program I want to develop — state-court coverage, multi-jurisdictional precedent reasoning, temporal validity of overruled cases — needs 4-5 years of focused work, which is the PhD time horizon. Second, the research community: industry research groups exist but the iteration loops are tighter and the topic agendas are more constrained. The combination of paper-swap partners, reading-group depth, and qualifier-level breadth that a PhD program provides isn't replicable in industry. Third, the formal advising relationship: I've done meaningful work solo over the past 18 months, but the directions I want to take this require sustained mentorship from someone with deep legal-NLP or NLP-evaluation expertise — not periodic technical reviews. I'm applying now rather than later because the open-weight legal-AI tooling gap is widening rapidly; the academic community needs people working on this problem now, not in 2030."

**Pitfalls:**
- Sounding like the PhD is a credential pursuit ("I need a PhD to get a research role"). Bad.
- Sounding dismissive of industry research ("Industry doesn't do real research"). Naive.
- Failing to connect to time horizon and depth. The interviewer is asking why they should invest 4-5 years in you.

---

## Scenario 3: Walk me through your research project

**Length:** 5-10 minutes (with whiteboard / screen-share)

**Key beats:**
1. The 30-second version of the architecture (high-level pipeline)
2. The 2-minute version that names the key design choices
3. The 5-minute version that walks through Tables 1-2 results
4. Anywhere you intentionally chose against the obvious option, with reasoning

**Visual aid:** Be ready to sketch the 3-stage architecture from `citecheck/docs/architecture.md` on a whiteboard or virtual whiteboard. Practice this 3 times before the first interview.

**Key design choices to explain (the interviewer will likely probe at least one):**
1. **Why shared-backbone two-head reranker, not two separate cross-encoders?** Avoids a Cartesian-product fine-tune cost; the two heads share the citation-grounding feature space.
2. **Why live registry verification, not post-hoc detection?** Eliminates a class of "we noticed but shipped it anyway" failures; reduces the latency cost of human review.
3. **Why constrained-decoding Bluebook grammar?** Makes downstream eyecite parsing deterministic; removes a class of malformed-citation failures.
4. **Why three axes (existence / support / jurisdictional validity), not one?** Single-axis metrics conflate failure modes; per-axis breakdown enables ablation studies that show *which* component fixes which failure.

**Pitfalls:**
- Going into the weeds before establishing the high-level pipeline. Always start at 30,000 feet.
- Dodging "why did you choose X over Y?" questions. Have an honest answer; if you didn't consider Y, say so and discuss it now.
- Pitching results that don't exist yet ("we expect to see..."). Be honest: "this is v0.1; the results I'm showing are from the pilot, not the full eval."

---

## Scenario 4: What are the limitations of your work?

**Length:** 90 seconds

**Key beats:**
1. Name 2-3 honest limitations
2. For each, the workaround you're using or the open problem it raises
3. Connect to PhD-level extensions

**Example answer:**

> "Three big ones. First, NLI judges are noisy on legal language — the entailment models we use weren't trained on legal text, and disagreement with human raters in our 200-item audit is around 15%. The workaround for v0.1 is to report both NLI-only and human-audited support F1; the PhD extension is fine-tuning a legal-NLI judge. Second, the Bluebook grammar in v0.1 covers about 80% of common citations — it misses parallel citations, statute citations like '42 U.S.C. § 1983', and signal phrases like 'see, e.g.'. eyecite handles many of these post-hoc but the constrained-decoding pass is narrower than the parse coverage. Third, latency: the verify loop adds 10-30% p95 overhead, which is fine for batch use cases like contract review but probably wrong for sub-second clinical-style applications. The PhD extension is exploring whether verifier-first training (Self-Refine-like fine-tuning) can move some of the verification cost from inference to training."

**Pitfalls:**
- "I don't see any limitations" or "the main limitation is needing more data." Lazy.
- Naming limitations that aren't actual limitations. Don't humblebrag.
- Listing limitations without proposing how the PhD could address them.

---

## Scenario 5: Describe a technical challenge you've overcome

**Length:** 2-3 minutes

**Key beats:**
1. The specific problem (concrete, not abstract)
2. What you tried that didn't work
3. What you tried that did work
4. What you'd do differently next time

**Example answer (one of many — adapt to your specific experience):**

> "When building CiteCheck's reranker training pipeline, I needed to mine query-passage-relevance triples from the eval set and BM25 hits. The first version pulled the gold-citation set straight from the eval examples and labeled any passage containing one of those citations as positive. This sounded reasonable but produced a reranker that overfit to citation-presence rather than learning anything about relevance: passages with the right citation but wrong topic were ranked above passages with the right topic but no citation. The fix was two changes: (1) require the passage to also entail the asserted claim, scored via the same NLI judge used for evaluation; (2) explicitly mine hard negatives — passages with the right citation but a contradicting claim. After that the reranker behaved like a relevance model with a grounding bias, which is what I wanted. The thing I'd do differently next time: start with explicit failure-mode taxonomy *before* mining training data. I rebuilt the data pipeline three times because I kept finding new failure modes I hadn't anticipated."

**Pitfalls:**
- Choosing a trivial challenge ("I had a bug and I fixed it"). The story should reveal how you think under pressure.
- Choosing a challenge that wasn't actually yours (group projects where you weren't the driver).
- Skipping the "what didn't work" beat. The interviewer learns more from your failures than your successes.

---

## Scenario 6: Why this program / why this lab?

**Length:** 60-90 seconds

**Key beats:**
1. Specific advisor + their specific paper
2. Specific overlap with your direction
3. Specific other things this program offers (course, lab culture, etc.)

**See `applications/interviews/per_advisor_prep.md`** for per-program rehearsed answers.

**Pitfalls:**
- Generic "great department" praise. The interviewer wants to see you've done the research.
- Naming only one advisor with no awareness of the broader department.
- Skipping the program-culture or course-availability dimension.

---

## Scenario 7: What would you want to work on if I admitted you?

**Length:** 60 seconds — short and concrete

**Key beats:**
1. Start with the advisor's recent line of work, NOT yours
2. Propose a specific extension or collaboration
3. Frame as a question, not a demand ("does this seem like a direction you'd want to develop together?")

**Example answer (for Stanford RegLab interview with Daniel Ho):**

> "Two directions I think could be interesting. First, your 2025 hallucinating legal LLMs paper suggests overruled-precedent detection as a hard sub-case. CiteCheck v0.1 handles existence and support but not temporal validity — was this citation still good law on the date the brief was filed? I'd want to develop a citator-aware support axis using the CourtListener treatment data. Second, your work on agency-rulemaking analysis suggests a regulatory-RAG direction: applying CiteCheck's verify loop to regulations rather than just case law. These both seem like 2-3 year sub-projects; I'd want to explore which interests you most. Does either direction seem like a fit?"

**Pitfalls:**
- Telling the advisor what they should be working on. Bad.
- Naming a direction that contradicts their published work without acknowledging it.
- Failing to leave room for them to redirect ("...or whatever direction interests you most").

---

## Scenario 8: What's your 5-year vision?

**Length:** 90 seconds

**Key beats:**
1. PhD-level research goals (concrete, specific to your area)
2. Beyond-PhD aspirations (postdoc / research scientist / faculty)
3. What you want to leave behind even if you don't continue in research

**Example answer:**

> "Five years from now I want to have: CiteCheck as a maintained open benchmark used by other groups working on legal RAG (not just my own); a publication record covering the three-axis decomposition methodology, the multi-jurisdictional precedent extension, and at least one extension to regulatory or international law; and a generation of master's students who've worked through CiteCheck as a teaching artifact in legal-NLP courses. After the PhD I'm most interested in academic research or research-engineering in a public-interest legal-tech context — places like Stanford RegLab, the Caselaw Access Project at Harvard, or a public-defender AI tooling group. Even if my career goes a different direction, the open benchmark and method I want to ship would still be a meaningful artifact for the legal-NLP community."

**Pitfalls:**
- Mapping out a specific job title 5 years out (faculty interviewers are skeptical of that level of certainty).
- Vague aspirations ("be a great researcher"). Concrete artifacts > abstract aspirations.
- Talking only about research output and not about community / mentorship / teaching dimensions.

---

## Scenario 9: What questions do you have for us?

**Length:** Most of the remaining interview time. Prepare 5 questions; ask 3.

**Good questions (real curiosity, hard to fake):**
1. "Your group has [N] PhD students currently — what's the typical mix between solo and collaborative projects? Which mode does CiteCheck-style work tend to follow in your experience?"
2. "How do you balance the publication cadence pressure (annual workshop deadlines, biennial main conference) against the longer-horizon work that PhDs are supposed to enable?"
3. "What's the qualifier exam structure here? What does a typical first-year preparation timeline look like?"
4. "When you've taken students in this area before, what's been the hardest transition for them — coursework-to-research, or research-to-thesis?"
5. "If a student came to you in year 2 wanting to pivot from [the CiteCheck-style work I proposed] to a fairly different direction, how would you handle that?"

**Bad questions (Googleable, signal lack of preparation):**
- "What's the funding situation like?" (research it before)
- "How big is the department?" (research it before)
- "What's the average time to PhD?" (research it before)

**See `applications/interviews/per_advisor_prep.md`** for per-program questions tailored to specific advisors.

---

## Scenario 10: Off-the-record questions for current PhD students

**Length:** Casual conversation; 5-10 minutes per student during open-house days or coffee chats

**What to ask:**
- "How would you describe the advising style here? Hands-on, hands-off, somewhere in between?"
- "How often does the lab meet, and what's the format?"
- "What's the average funding guarantee — first year only, multi-year, or unconditional?"
- "How do you decide when to publish vs. when to keep working on a result?"
- "What's the cost of asking your advisor a 'dumb' question?"
- "What's been the hardest unexpected thing about being a PhD student here?"
- "If you had to do the admissions decision again, would you come here?"

**What NOT to ask current students:**
- "Is [advisor name] a good advisor?" (puts them in an awkward spot)
- "Is this program prestigious enough?" (signals snobbery)

---

## Post-interview ritual

Within 24 hours of every interview:

1. **Send a thank-you email** (1 paragraph; reference one specific thing discussed)
2. **Log in `applications/interviews/log.md`:** date, interviewer, format, vibe, follow-up needed
3. **Update `journal/decisions.md`** if the interview changed how you rank the program
4. **Sleep on it before any decision.** Programs sometimes seem better or worse than they actually are right after a long interview day.

---

## Calibration

If you're getting interview invitations at all, congratulations — that's the hardest single filter in the cycle. From there:
- ~50% acceptance rate is typical for interviews-to-admits at most US PhD programs (varies by program, year, and field).
- Don't read too much into a single interview going well or poorly. Some interviewers are just busy / distracted.
- The most important signal: does the conversation make you want to spend 5 years in this lab? That's the right reverse-question.
