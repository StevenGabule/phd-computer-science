# Bottlenecks and Protocols

**Purpose:** A catalog of the common stuck points across the 18-month plan, with a specific protocol for each. When you hit a wall, find your situation here.

**Meta-principle:** Most stuckness is about lack of specificity. "I'm stuck on the paper" is not actionable; "I don't know how to phrase the contribution claim in the abstract" is. Before consulting this file, write down your stuckness in one specific sentence.

---

## Reading bottlenecks

### Paper-incomprehensible
**You opened a paper and after 30 minutes you don't understand the central claim.**

Protocol:
1. Stop. Don't push through.
2. Read the abstract again. Write the central claim in one sentence in your own words. If you can't, you've identified the gap.
3. Look at the introduction's last paragraph. It usually states contributions in plain English. Compare to your abstract reading.
4. Identify the 3-5 references the paper relies on most. Read at least one of them first.
5. Return to the paper. If still impenetrable, it may genuinely be over your current head — that's data, not failure.
6. Post in the reading group: "Has anyone read X? Section Y of the introduction lost me at [specific sentence]."

When to drop a paper entirely: if after the above protocol you still don't get the central claim and the paper is not Tier-1 priority, drop it. Mark `dropped` in `literature/reading_list.md`. Not every paper rewards effort.

### Reading without retention
**You read papers but a week later cannot summarize them.**

Protocol:
1. You're probably reading passively. Switch to active reading.
2. Before opening the paper, write the question at the top of your notes: "What does this paper claim and how does it support that claim?"
3. Make yourself answer that question in your notes before closing the paper.
4. Add a "1-line takeaway" to the top of every notes file. If you can't write the 1-liner, you didn't understand the paper.
5. Weekly: re-read your 1-line takeaways aloud. Concepts you can't recall become flashcards.

### Reading too slowly
**You're behind on the deep-read schedule.**

Protocol:
1. Verify you're using the 3-pass method (see `learning/how_to_read_papers.md`). Most "slow" readers are doing a single deep pass when they should be doing a fast first pass, then deciding.
2. Cap deep reads at 4 hours per paper. If you blow past 4 hours, the paper is either much more important than you thought (good — but adjust schedule) or you're getting stuck on unimportant details (bad — fast-forward to results and discussion).
3. Drop low-priority papers ruthlessly. 50 deeply-read is better than 100 half-read.
4. Reading group is your forcing function. If the group meets weekly and you must contribute, you'll read.

---

## Writing bottlenecks

### Blank-page paralysis
**You open `main.tex` (or the SOP, or the email) and write nothing for an hour.**

Protocol:
1. Stop trying to write the section. Write the section's outline instead — bullet points are fine.
2. Or: write the section's *worst possible* version. Genuinely bad. Then edit upward.
3. Or: write a 1-paragraph email to a friend explaining what the section is supposed to say. Then convert the email into the section.
4. Or: walk for 20 minutes without your phone. Most blank-page paralysis dissolves when you stop trying.
5. Or: switch to a different section that feels easier. Return to the hard one when momentum exists.

### Editing-instead-of-writing
**You write 50 words, edit them, rewrite, edit, end the day with the same 50 words.**

Protocol:
1. Set a timer for 30 minutes. Goal: 300 words. No backspace. No editing.
2. After 30 min, take a 10-min break, then edit if needed.
3. Repeat 2-3x per writing session.
4. Most writers should average 250-500 words/day on a paper for 4 weeks; perfectionism cuts that to 50 words/day for 6 months.

### Section feels wrong but I can't say why
**You finished a section but rereading it makes you uncomfortable.**

Protocol:
1. Read it aloud. The ear catches what the eye misses.
2. Show it to someone outside your area. Ask "what did you understand?" If their summary differs from your intent, the section isn't doing its job.
3. Identify the *one* sentence that feels weakest. Often the whole section is wrong because of that one sentence. Fix it; the rest may resolve.
4. If still wrong: leave the section and write the next one. Return with fresh eyes in 2-3 days.

---

## Code bottlenecks

### Can't reproduce paper
**You implemented a baseline from a paper and your numbers are off by >5%.**

Protocol:
1. Confirm you have the exact model checkpoint (HuggingFace revision hash, not just model name).
2. Confirm you have the exact eval dataset version (HuggingFace dataset commit, not just dataset name).
3. Confirm hyperparameters match — every single one. Most reproduction failures are silent hyperparameter drift.
4. Confirm preprocessing matches (tokenization, truncation strategy, batch ordering). A surprising fraction of "reproduction" failures are preprocessing bugs.
5. Run the official code repo (if it exists) on the same eval. If your numbers differ from their code, the issue is your code; if they match their code but differ from the paper, the issue is upstream.
6. Email the authors politely with a specific question. They almost always respond.
7. If still off after all the above, document the discrepancy in your paper. "We were unable to reproduce X et al.'s reported Y of 87.2; our reimplementation achieves 84.1." Honesty is better than fakery.

### Code works in notebook but fails in script
**The same code that ran in `jupyter notebook` fails in `python script.py`.**

Protocol:
1. 90% of the time: a path issue or an environment-variable issue. Run `os.getcwd()` and `os.environ` in both contexts; diff.
2. 5% of the time: import-time side effects. Check whether your module has top-level code that depends on a notebook's interactive state.
3. 5% of the time: random seed not set. Notebooks share a global RNG state across cells; scripts get a fresh one. Set seeds explicitly.

### Training loss goes NaN
**The training loop ran for 200 steps then loss became NaN.**

Protocol:
1. Reduce learning rate by 10x. Usually fixes it.
2. Add gradient clipping (`torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)`).
3. Check the data — a single corrupted example can cause NaN. Validate inputs are not all-zero or all-NaN.
4. Use mixed precision carefully — `fp16` is more numerically fragile than `bf16`. Switch if you can.
5. If using QLoRA, verify the base model loaded successfully (sometimes `bitsandbytes` silently corrupts).
6. Print loss every 10 steps and look at where it spiked. Often gives a clue about which batch caused it.

### Out of memory (CUDA OOM)
**Training crashes with `CUDA out of memory`.**

Protocol:
1. Reduce batch size by half. Usually first thing to try.
2. Enable gradient checkpointing (`model.gradient_checkpointing_enable()`).
3. Reduce sequence length if possible.
4. Use QLoRA (4-bit) instead of 8-bit or full precision.
5. Switch to a smaller base model (Llama-3.1-8B → Qwen-7B → smaller).
6. Use `accelerate` to spread across multiple GPUs (Colab Pro: A100 40GB).
7. As a last resort: use CPU offloading (`device_map="auto"` with `offload_folder`).

---

## Research-direction bottlenecks

### Candidate gap has been closed
**You went to write the abstract and discovered someone published your idea last month.**

Protocol:
1. Read their paper end-to-end. Verify it actually does what you were going to do (titles can be misleading).
2. If they did the exact same thing: your contribution is now a "concurrent and independent" replication. Still publishable, but weaker.
3. If they did it differently: emphasize the difference in your framing. Most "scoops" leave room for related work.
4. If they did it better: pivot to a sub-problem they didn't address. They've validated the problem; you can dig deeper.
5. Email the authors. Often they're happy to compare notes and may have follow-up directions they don't have bandwidth to pursue.
6. Use this as a forcing function for clarity: what's the smallest viable contribution that still feels novel?

### Headline result not significant
**Your method beats baselines by 2-3 percentage points but the std dev is 4 percentage points.**

Protocol:
1. Verify the comparison is fair (same data, same hyperparameter search budget, same compute).
2. Run more seeds. 3 is the minimum; 5-10 if compute allows.
3. Use a more sensitive metric. If F1 is noisy, try per-class breakdown or learned-evaluator scores.
4. Pivot the framing: "we introduce a benchmark + a competitive method" stands even if the method doesn't dominate. The benchmark contribution is hard for reviewers to argue against.
5. Add an analysis-heavy section: even a "not-quite-best" method becomes interesting if you can characterize *when* it wins vs. loses.

### I want to change my project
**You're 3 months into Phase 2 and want to switch to a different topic.**

Protocol:
1. **Pause for 1 week.** Don't make this decision in a moment of frustration.
2. Write the case for switching: what's not working, what's broken about the current direction, what's better about the new one. Be specific.
3. Write the case for staying: what would you lose by switching, what's the sunk cost, what's the time cost to ramp on a new topic.
4. Talk to 2-3 people: your reading group, a former advisor, a paper-swap partner.
5. Most "want to switch" feelings are about pace, not topic. If the new topic also has the same pace problems in 3 months, you'll want to switch again.
6. Switching once is normal. Switching twice means there's a pattern; investigate that before switching a third time.

---

## Recommender bottlenecks

### Recommender not responding to ask email
**You sent the ask in May; it's now July and no response.**

Protocol:
1. Send a polite 1-paragraph follow-up. "Following up in case my earlier note got buried."
2. If no response in another 2 weeks: send a direct ask in a different channel (Twitter DM, LinkedIn, an email to a colleague who could nudge them).
3. After 4 weeks of silence: assume no. Move to your backup recommender.
4. Don't hold a grudge — silence often means overload, not rejection. They may write a fine letter for the next student you don't know about.

### Recommender accepts but seems lukewarm
**They said yes but the response was short and unenthusiastic.**

Protocol:
1. Send the recommender packet immediately. If they were lukewarm because they were unsure how much work it was, the packet may reassure them.
2. Schedule a 15-min check-in call in October. Brief them on the program list verbally; gauge enthusiasm.
3. If still lukewarm: they may write a "supportive but not strong" letter. Acceptable for ⅓ slot but not ideal for the primary letter. Adjust your other letter strategy accordingly.
4. Honest assessment: do you really want them as a recommender, or are you settling? Sometimes lukewarm recommenders write better letters than enthusiastic ones; sometimes worse. Read the personality.

### Recommender missing the deadline
**T-2 emails sent; T-0 approaching; portal still shows no letter.**

Protocol: use `applications/recommender_packets/followup_emails/T-escalation.md`. The short version:
- Contact program admissions yourself. Ask for a 1-2 week extension.
- Send the recommender one final note with phone number.
- Activate your backup recommender if available.
- Worst case: withdraw the application from that program. Better than a 2-letter incomplete file in some cases (but verify — some programs DO consider incomplete files).

---

## Application bottlenecks

### Portal won't accept my upload
**The portal returns an error on file upload.**

Protocol:
1. Check the file format (PDF, not Word; some portals only accept PDF/A).
2. Check the file size (most portals: 5 MB max; compress if over).
3. Check the filename (some portals reject spaces, special characters, very long names). Rename to `lastname_firstname_sop.pdf`.
4. Try a different browser. Chrome works; Edge and Safari sometimes fail silently.
5. Try a different device. Some portal upload widgets break on specific OS combinations.
6. If still failing: log in `applications/submission/blockers.md`, email program admissions (they often have a manual upload workflow for edge cases).

### Transcript hasn't arrived
**You ordered transcripts in October; the program portal still shows "not received."**

Protocol:
1. Verify the order shipped from the source institution (call the registrar).
2. Verify the destination address on the order matches the program's requirement (they sometimes differ for "official" vs. "applicant" transcripts).
3. Some programs take 5-10 business days to mark transcripts as received even after they arrive. Wait one more week before escalating.
4. If still missing after 3 weeks: order a duplicate transcript. The first may genuinely have been lost in transit.
5. Document in `blockers.md`.

### I missed a deadline
**You realized at 2am that today was the deadline; you submitted at 3am, 3 hours late.**

Protocol:
1. Don't panic. Most programs have a 24-hour grace period for technical issues.
2. Email program admissions within the next 8 hours: brief explanation, your applicant ID, and request to confirm the application is being reviewed.
3. If they reject the late submission: it's done. Don't beg, don't argue. Mark as `withdrawn_late` in the tracker and move on.
4. If they accept: thank them sincerely. Add a buffer day for the next deadline.
5. After this happens once, you'll never miss another deadline.

---

## Interview bottlenecks

### Interview is happening in <72 hours and I'm not prepared
**Email arrived this morning; interview is Thursday.**

Protocol:
1. Pull up `applications/interviews/per_advisor_prep.md` and find the row for this advisor.
2. If they're not in the top-10 starred list: spend 90 minutes today on Google Scholar reading their 3 most recent papers.
3. Read your SOP for this program (the per-program one in `applications/sop_variants/`).
4. Practice your 60-second research pitch from `applications/interviews/scenarios.md` Scenario 1 — 5 times out loud.
5. Prepare 3 questions for them (from `per_advisor_prep.md` or invent).
6. Sleep 8 hours the night before. Tired interviewees underperform substantially.

### Interview question I didn't expect
**They asked something completely off-script.**

Protocol:
1. Pause. "That's a great question — let me think for a moment" is fine.
2. If you don't know: say so, then propose how you'd find out. "I don't know off the top of my head, but my first move would be X."
3. If you partially know: state the part you know, flag the part you don't, propose how you'd extend. Most interviewers reward this more than false confidence.
4. Never bluff. Interviewers can tell, and a bluff caught is worse than an honest "I don't know."

### Interview went badly
**You left the interview feeling you bombed it.**

Protocol:
1. Send the thank-you email anyway, within 24 hours.
2. Take 1 day off the application stuff. Don't try to "process."
3. In 48 hours, journal what specifically went wrong. Most "I bombed it" feelings turn out to be 1-2 specific moments magnified.
4. Use the lesson for the next interview. Often the second interview at the same program (with a different faculty member) reverses the verdict.
5. Don't drop the program from your ranking based on one bad interview unless something genuinely fundamental was wrong (e.g., advisor said they're not taking students).

---

## Project-management bottlenecks

### I have too many open threads
**You're context-switching between 5 things and finishing nothing.**

Protocol:
1. List every active thread. Be honest — usually 7-10 things, not 5.
2. Pick the top 3. Commit to them for the next week.
3. Park the rest in a `parked/` file with a date you'll revisit them.
4. Tell collaborators you're parking their thing temporarily. Most won't mind; some will appreciate the honesty.
5. Re-evaluate Sunday during the weekly retrospective.

### I'm working but not progressing
**You're putting in hours but the milestones aren't moving.**

Protocol:
1. Look at the last 2 weeks of `journal/weekly.md`. Identify what you've actually completed (not started).
2. Compare to what you planned. The delta is your "lost time" — characterize it.
3. Common patterns: too much reading (reading without writing), perfectionism on one section, switching too often, social-media drift.
4. Set a "hard problem of the week" — one specific thing that must complete by Sunday. Cut other commitments to make room.
5. If 2 weeks pass without milestone progress, the milestone might be wrong. Reconsider whether you've over-scoped.

### I'm burning out
**You can't get up for the morning reading. Each day feels like dread.**

Protocol:
1. See [`wellness/sustainable_practices.md`](../wellness/sustainable_practices.md) for the full protocol.
2. Short answer: take a real break. Not "I'll work on something easier" — a full 5-7 days off.
3. Don't try to "push through" — burnout that's pushed through becomes recovery measured in months, not days.
4. The PhD-prep cycle is a marathon. You need pace, not heroics.
5. If breaks aren't helping, talk to someone. Therapist, partner, peer who's been through it. Don't isolate.

---

## Meta-bottleneck: I don't know what to do

**It's Wednesday morning and you don't know what to work on.**

Protocol:
1. Open [`THE_ROADMAP.md`](THE_ROADMAP.md). Find the current week. Look at the cadence.
2. If the roadmap says "read paper X" — read paper X.
3. If the roadmap says "write section Y" — write section Y.
4. If you've already done all of this week's roadmap items — do next week's. (Treat as a gift; you're ahead.)
5. If the roadmap doesn't cover your situation — write down your specific question. Open this file. Find the closest match. Apply the protocol.
6. If no protocol fits — your situation is new. Write it down for the next time. Update this file.

---

## Last-resort: nothing in this document is working

If you've genuinely tried multiple protocols and you're still stuck for >1 week:

1. The problem may not be tactical — it may be structural. Re-read the spec (`docs/superpowers/specs/2026-05-24-phd-cs-study-plan-design.md`) and ask: is this still the right plan for me?
2. Talk to a former advisor or a PhD student who's 2-3 years ahead of you. Buy them coffee.
3. Consider whether the PhD path is what you actually want. Genuine question, asked seriously every 6 months. The plan only works if the underlying motivation is real.

If the answer is "yes, this is still what I want, and the plan is still right" — keep going. The 18 months has slack built in. Most "I'm too far behind" moments resolve themselves within 4-6 weeks of steady effort.
