# Decision Frameworks

**Purpose:** Pre-committed criteria for the major decisions in the 18-month plan. The point is to decide *how* to decide before you face the decision under pressure. Otherwise you'll regret in November the decision you made in panic in October.

---

## Meta-framework: how to make good decisions

Before any specific framework, the meta-questions to ask:

1. **Is this decision reversible?** Reversible decisions deserve speed (act, learn, adjust). Irreversible decisions deserve deliberation.
2. **What's the cost of waiting one week?** If small, wait — more information is almost always better.
3. **What information would change my decision?** Go get that information before deciding.
4. **What does my future self want?** Imagine yourself in 6 months looking back. Which decision will you regret less?
5. **Am I deciding under emotion?** Anger, fear, excitement all degrade decision quality. Sleep on emotional decisions.

The single most useful question: **"What's the worst case if I'm wrong about this?"** If the worst case is "I lose a week of work," decide fast. If it's "I waste a year of the plan," deliberate hard.

---

## Decision 1: Which candidate to lock at M2 (Aug 31, 2026)

**Default per `project/candidates.md`:** Candidate D (CiteCheck).

**When to override the default:**
- During deep reads in June-July, you discovered Candidate D's gap has been closed by 2026 papers.
- A specific advisor (Ho, Nyarko, Šavelka) responded to a cold email saying CiteCheck is being done elsewhere.
- Your independent skill assessment concludes Candidate C (LexEcoRAG, RL/PO-heavy) is more tractable for you than originally estimated.

**Criteria (apply in order):**

1. **Data accessibility** (binary gate). If the candidate's gold data requires a non-existent dataset or a JD-level annotator you can't afford, the candidate is dead. Drop.
2. **Single-GPU feasibility** (binary gate). If the candidate requires multi-GPU training you don't have access to, the candidate is dead. Drop.
3. **Scoop risk** (high signal). Re-search Scite the week of M2. Any paper that exactly matches your candidate kills it. A paper that partially overlaps reshapes it (acceptable).
4. **Workshop-publishability in 12 months** (high signal). Can you imagine the 8-page write-up landing at NLLP / TrustNLP given known compute + annotation budget?
5. **Personal interest** (low signal but real). You will work harder on something you actually want to read about. If two candidates tie on the above, pick the one you'd read about for fun.

**Anti-pattern:** picking the candidate that sounds most impressive to admissions committees. Committees evaluate execution, not ambition. A well-executed Candidate D > a badly-executed Candidate B.

**Reversibility:** medium-to-low. Reversing at M3 (Nov 2026) costs ~3 weeks of work. Reversing at M4 (Feb 2027) costs ~3 months. So this decision deserves real deliberation.

---

## Decision 2: Annotator strategy (resolve by Dec 2026)

**Options (per `project/m2_lock_checklist.md`):**
A) Paid Upwork JD reviewer (~$2,000–$3,200; 4-week turnaround)
B) Law-student collaborator (free; 8-week turnaround; co-authorship discussion)
C) Self-only with adversarial seeding (zero cost; lower coverage; v0.1 release)

**Criteria:**

| Criterion | A (paid) | B (collaborator) | C (self) |
|---|---|---|---|
| Cash cost | $2,000-3,200 | $0 | $0 |
| Time cost | low (parallel) | medium | high |
| Quality | high | high (if law student is good) | medium |
| Annotator availability risk | low (Upwork has many) | high (one person, can drop out) | n/a |
| Co-authorship complexity | none | real | none |
| Plan-stability impact | high (locked in) | medium | high |

**Decision rule:**

- **If you can afford $2-3k and don't have a law-student collaborator already lined up by Aug 2026:** Option A. Don't try to "find a collaborator" mid-Phase-2; you'll waste 2 months.
- **If you have a specific named law student or paralegal who has agreed to ~8 weeks of work:** Option B. Lock the co-authorship terms in writing before they start.
- **If both A and B are off the table:** Option C, but reduce the eval set to ~200 items. Plan to expand in v0.2.

**Anti-pattern:** delaying this decision past Dec 2026. Annotator recruitment takes 2-4 weeks; if you decide in Dec and recruit in January, you've cost yourself a month of the eval-set window.

**Reversibility:** medium. You can switch from C to A mid-construction (mine 100 items yourself, then hire an Upworker for the next 400) but you can't easily reverse a co-authorship promise.

---

## Decision 3: Workshop venue selection (Aug 2027)

**Default:** NLLP @ EMNLP 2027 (primary), TrustNLP @ EMNLP 2027 (backup), NeurIPS workshops (fallback for Aug-Sep deadlines).

**Criteria:**

1. **Audience fit.** NLLP is the most direct legal-NLP audience. TrustNLP draws a safety/faithfulness crowd. Pick the venue where your contribution lands obviously.
2. **Review quality + supportiveness.** Workshops vary. Ask 2-3 people in your network which venues they've had good experiences with.
3. **Timing.** If you're aiming for fall PhD admissions, the paper needs to be public by November. NLLP @ EMNLP typically notifies in October — works. NeurIPS workshops sometimes notify in November — borderline.
4. **Co-located conference.** Submitting to a workshop co-located with a main conference you'd attend anyway is a force multiplier (you'll go regardless; the workshop visibility is a freebie).
5. **Submission deadline.** Workshops in your timeline that have deadlines before you're ready (Jun-Jul 2027 with insufficient Phase 2 buffer) are stress-inducing. NLLP @ EMNLP 2027 typically has Jul-Aug deadlines — OK.

**Anti-pattern:** holding out for a main-conference submission (ACL / EMNLP main). The acceptance rate is 4-5x lower for a Master's-level applicant; the time spent on rebuttal cycles competes with application materials. Workshop first.

**Reversibility:** high. If rejected, the next venue is 1-3 months away. Don't agonize.

---

## Decision 4: Per-program SOP customization scope (Sep 2027)

**Default:** customize for top 5 programs (`applications/sop_variants/` already drafted).

**The decision:** customize for which other ~15-20 programs?

**Criteria:**

1. **Program tier × admission probability.** Reach programs with strong fit deserve deep customization; safety programs deserve light customization.
2. **Word count per program.** A program with a 1,000-word limit and a unique cultural fit (e.g., Edinburgh's CDT-NLP) deserves a full rewrite. A program with a 1,500-word limit and weak fit can use a lightly-customized version of the closest SOP variant.
3. **Time budget.** ~3 hours per deep customization × 5 programs = 15 hours. ~1 hour per light customization × 15 programs = 15 hours. 30 hours total in September.

**Recommendation:**
- Top 5 programs: deep customization (5 hours each)
- Next 10 programs: medium customization (1.5 hours each)
- Remaining ~5-7 programs: light customization (30 min each)
- Total: 25 + 15 + 3 = ~45 hours, spread over 3-4 weeks

**Anti-pattern:** treating all programs equally. You'll burn out and the strongest SOPs will suffer.

---

## Decision 5: Which programs to apply to (Sep 2027)

**Default:** the 22+ programs in `outreach/programs.md` minus NYU/Oxford caveats.

**Criteria for adding a program:**

1. **A specific advisor whose recent work is directly relevant.** (Not "this program is prestigious" — there must be a *named* advisor.)
2. **The program's PhD structure fits you.** US 5-6 year vs. UK 3-4 year vs. ETH project-specific 4-year are different commitments.
3. **You can imagine living there for 4-6 years.** This is real.
4. **The application cost is bearable.** $80-150 per program adds up. 25 programs × $100 = $2,500.

**Criteria for removing a program:**

1. **Advisor doesn't respond to cold email.** Not definitive, but a signal.
2. **The fit paragraph is forced.** If you can't write a genuine 3-sentence per-advisor connection, the application is wasted.
3. **The geographic location is genuinely off the table** (visa, partner constraints, family). Don't waste fee money on a program you won't accept if admitted.
4. **The program's most-recent papers don't align with your direction.** Faculty pivot; lab agendas drift.

**Recommendation:** 18-22 programs is the sweet spot. <15 is too few (interview rate is highly variable); >25 has diminishing returns (you can't customize 25 SOPs well).

---

## Decision 6: Which recommenders to ask (May 2027)

**Default per `applications/recommender_packets/_template.md`:** 3 primary + 1 backup.

**Criteria for each recommender slot:**

| Slot | Ideal profile | Acceptable substitute |
|---|---|---|
| Slot 1 (must) | Master's thesis advisor | Senior research collaborator |
| Slot 2 | NLP / ML / IR professor from key course | Industry research supervisor with strong PhD |
| Slot 3 | Recent research collaborator (specific project) | Coursework professor with notable engagement |
| Backup | Anyone who can write within 48 hours notice | A PhD student you've co-authored with |

**Anti-criteria (avoid these):**
- Famous names you don't actually know
- People who saw you do well in 1 course but nothing else
- People you haven't communicated with in 2+ years
- Industry supervisors who can't speak to research

**Decision rule:** when in doubt, ask the person with the *closer* relationship over the *more prestigious* name. A warm letter from a postdoc beats a tepid letter from a famous full professor.

---

## Decision 7: Which offer to accept (April 2028)

This is the largest decision in the entire 18-month plan. **Use `decisions/offer_evaluation.md`** (separate file) for the full framework. Summary criteria:

1. **Advisor fit** (40% weight). Does the advisor's research direction excite you? Will you want to work with them daily for 4-6 years?
2. **Funding stability** (20% weight). Multi-year guarantee > single-year. RA-funded > TA-funded > unfunded.
3. **Cohort and lab culture** (15% weight). Do current students seem happy? Is the lab collaborative or competitive?
4. **Program structure** (10% weight). Qualifier exam, time-to-degree, breadth requirements — all affect your year-1-2 experience.
5. **Geographic / personal fit** (10% weight). Cost of living, partner / family considerations, weather, community.
6. **Brand / network** (5% weight). Lower than people think. Real but smaller than the others.

**Anti-pattern:** picking based on US News ranking. Rankings are aggregate; your experience is individual. A "lower-ranked" program with a perfect advisor fit > a "higher-ranked" program with a mediocre fit.

---

## Decision 8: When to switch direction

The hardest decision class. Use these guardrails:

**Conditions that justify a switch:**
- A fundamental assumption of your direction has been shown wrong (e.g., the dataset you needed doesn't exist; a paper proved the approach can't work).
- Your direction has been published by someone else and you have no differentiator.
- You've worked 3+ months without measurable progress despite genuine effort.
- An advisor or peer you respect has independently suggested you reconsider.

**Conditions that look like "I should switch" but aren't:**
- You're tired (sleep, then re-evaluate).
- You're frustrated with one specific bug (it's a bug, not a problem).
- A different topic seems more exciting (the grass is always greener; PhD topics get hard in month 4 regardless).
- You're behind schedule (catch up before switching).

**Process if you decide to switch:**
1. Document the decision and reasoning in `journal/decisions.md` (verbose entry).
2. Notify any collaborators / advisors immediately.
3. Take 1 week before re-committing — sometimes the rest re-energizes the original direction.
4. If you do switch, sunk-cost the old work (don't try to "save" it) and start the new direction fresh.

---

## Decision 9: When to ask for help

**Default:** ask earlier than feels comfortable.

**Specific triggers to ask immediately:**
- You've been stuck on a coding problem for >4 hours.
- You've been stuck on a writing problem for >2 days.
- You're not sure whether to switch directions.
- You've received conflicting advice from two sources.

**Where to ask:**
- Reading group (best for paper / methodology questions)
- Paper-swap partner (best for writing questions)
- Twitter / Bluesky academic community (best for "is this idea novel?" questions)
- StackOverflow / GitHub Issues (best for engineering questions)
- An advisor or former mentor (best for direction-level questions)
- A peer in the program (best for application logistics)

**How to ask:**
- Write your specific question in 2-3 sentences before approaching anyone.
- State what you've already tried.
- State what answer would be useful (a yes/no? a pointer to a paper? a code snippet?).
- Acknowledge the asker's time ("if this isn't useful to think about, no worries").

**Anti-pattern:** asking a vague "what should I do?" question. The asker doesn't know your context; they'll give generic advice that doesn't help.

---

## Decision 10: When the plan is wrong

**The hardest meta-decision.** Sometimes the 18-month plan itself, not a specific tactical choice, is wrong for your situation.

**Triggers to reconsider the plan:**
- You've consistently missed milestones for 2+ months.
- Your life circumstances have changed materially (health, family, financial).
- The PhD path no longer feels right when you imagine it 5 years out.
- A genuinely better opportunity has appeared (different research role, different career direction).

**Process:**
1. Re-read the master design spec (`docs/superpowers/specs/2026-05-24-phd-cs-study-plan-design.md`).
2. Write a 1-page assessment: what's working, what's not, what's changed since May 2026.
3. Talk to 2-3 people: a former advisor, a peer who's been through it, your partner / family.
4. Sit with the assessment for 1 week.
5. If you decide to deviate from the plan substantially, document the new plan in a new spec file. Don't abandon the old plan silently — replace it formally.

**Anti-pattern:** quietly drifting away from the plan without acknowledging it. Drift becomes confusion which becomes burnout.

---

## Decision-making hygiene

Across all the above:

1. **Write decisions down.** Use `journal/decisions.md`. Include the alternatives considered, the criteria used, and the reasoning.
2. **Pre-commit to criteria.** Decide *how* to decide before you face the decision. Otherwise emotion / recency bias / fatigue contaminate the call.
3. **Set deadlines on decisions.** Open decisions consume background cognitive bandwidth. "I'll decide by Friday" frees you to think about other things until Friday.
4. **Distinguish two-way doors from one-way doors.** Two-way (reversible) — decide fast. One-way (committing) — decide slow.
5. **Honor the decision.** Once made, commit. Re-evaluating every decision daily is its own kind of failure.

---

## A final note on judgment

The decision frameworks here are starting points. After 12 months in the plan, your judgment will exceed these guardrails for your specific situation. When that happens, override the framework with reasons, and document the override in `journal/decisions.md`.

The frameworks exist to prevent the worst version of you — the tired, anxious, deadline-pressed version — from making a decision the rested, thoughtful version of you would reverse. They are not the ceiling on your judgment; they are the floor.
