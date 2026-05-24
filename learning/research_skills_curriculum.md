# Research Skills Curriculum — Month by Month

**Purpose:** What to deliberately practice each month of the 18-month plan. The phase plans tell you *what to do*; this file tells you *what to learn while doing it*.

**Principle:** A PhD is fundamentally about learning to do research, not about producing research. Treat every month as a deliberate-practice opportunity, not just an output-production sprint.

---

## Month 1 (June 2026) — Reading academic papers with discipline

**Primary skill:** the 3-pass method (see `how_to_read_papers.md`).

**Secondary skill:** structured note-taking.

**Deliberate practice:**
- Read 10 papers using the template strictly. Do not skip the "1-line takeaway" or "questions for project" fields, even when tired.
- After each paper, do the "rewrite the abstract from memory" exercise once.
- Weekly: pick the paper that surprised you most; explain it to a non-CS friend in 5 minutes. If they don't get it, your understanding is incomplete.

**Self-assessment at end of month:**
- Can you recall the central claim of every paper you read this month? (If <70%, your notes need work.)
- Can you place each paper on a 2D map of (research direction × method type)?
- Can you identify 3-5 open questions the field hasn't addressed?

**Resources:**
- Keshav, *How to Read a Paper* (ACM CCR 2007, 1 page) — read this first
- Sanjeev Arora, *How to Read a Research Paper* (Princeton CS blog post)

---

## Month 2 (July 2026) — Synthesizing across papers

**Primary skill:** seeing patterns, not facts. Moving from "papers as units" to "fields as graphs."

**Deliberate practice:**
- Build the `literature/taxonomy.md` file iteratively, not in one sitting. Add 1-2 papers per week; restructure clusters when needed.
- For every pair of papers in your reading list, ask: "do these agree, disagree, or talk past each other?"
- Write 1-paragraph mini-essays on questions like "what are the 3 most-cited evaluation metrics in legal RAG, and where do they disagree?" — even if no one will read them.

**Self-assessment:**
- Can you draw the citation graph of your top 20 papers from memory? (Approximately — exact edges aren't the point.)
- Can you identify the 3-5 conceptual disagreements in the field (e.g., "the citation-faithfulness camp vs. the retrieval-quality camp")?
- Can you state 3 candidate gaps in a way that a researcher 5 years senior to you would think were sensible (even if they'd push back on prioritization)?

**Resources:**
- Hennessy & Patterson, *How to Write a Survey Paper* — the inverse of reading a survey is doing one mentally for a field
- Read 1-2 actual NLP / IR survey papers (Quevedo 2024 is on your list; complement with one from another subfield to see survey style variation)

---

## Month 3 (August 2026) — Writing a problem statement that survives criticism

**Primary skill:** precision in prose. Every sentence does work or is cut.

**Deliberate practice:**
- Draft your problem statement. Show to 2 people (paper-swap, advisor, reading-group member). Cut anything that doesn't survive their feedback.
- Practice writing the same idea three different ways. Pick the shortest.
- Read 5 SOPs / problem statements from people who got into PhD programs in your area (search Twitter / Reddit; many are public). What patterns do you notice?

**Self-assessment:**
- Can you state the problem in 1 sentence (~25 words)? In 3 sentences? In a paragraph?
- For every claim in your problem statement, can you name the evidence?
- If a senior researcher asks "why do you care about this?" can you answer in 30 seconds without notes?

**Resources:**
- Strunk & White, *Elements of Style* — short, classic, still useful
- William Zinsser, *On Writing Well* — chapters 1-7 specifically (clarity, simplicity, brevity)

---

## Months 4-5 (September-October 2026) — Engineering discipline

**Primary skill:** writing production-quality scientific code.

**This is the month most CS PhD applicants discover their notebook code doesn't survive contact with a real eval harness.**

**Deliberate practice:**
- For every function you write, write a unit test. Yes, every function. Yes, even small ones.
- Use type hints aggressively. `mypy --strict` is the aspirational baseline.
- Write docstrings before you write the function body. The docstring is the contract.
- Use `logging` instead of `print` from day one.
- Set up wandb (or alternative) for every experiment from day one.

**Self-assessment:**
- Can a stranger run your code from a clean checkout? (Run `make test` on a fresh clone to verify.)
- Can you reproduce a result from 2 weeks ago? (If not, you have a reproducibility bug.)
- Is your code organized so that swapping one component (e.g., the retriever) is a single-file change?

**Resources:**
- Hilary Mason, *On Being a Research Engineer* — short essay on the mindset
- Joel Grus, *I Don't Like Notebooks* (JupyterCon 2018 talk) — controversial but worth watching
- The `citecheck/` codebase itself — read every module before you modify it

---

## Months 5-6 (October-November 2026) — Reproducing other people's work

**Primary skill:** the patience and rigor to make someone else's results emerge from your machine.

**The cliché:** "the first 80% of reproduction takes 20% of the time; the last 20% takes the other 80%." This is true. Plan accordingly.

**Deliberate practice:**
- Reproduce Self-RAG end-to-end. Document every discrepancy.
- Reproduce CRAG end-to-end. Document every discrepancy.
- For each, write a 1-page "what we found" report. These become Section 5.1 of your paper.
- Email at least one paper's authors with a polite, specific question. They almost always reply.

**Self-assessment:**
- Can you match the paper's headline numbers within 2%? Within 5%? Within 10%?
- If not, do you know *why*?
- Have you isolated whether the gap is a code issue, a hyperparameter issue, a data issue, or an environment issue?

**Resources:**
- The ACL Reproducibility Checklist (for the rigor language)
- Joelle Pineau, *Reproducibility in Machine Learning* (NeurIPS keynote) — for the philosophy
- The `citecheck/src/citecheck/baselines/` modules — read every line of the baseline you're reproducing

---

## Months 7-8 (December 2026 - January 2027) — Eval set construction discipline

**Primary skill:** dataset craftsmanship. The benchmark is half your contribution.

**Deliberate practice:**
- Hand-annotate 50 items yourself before recruiting any annotator. You will see the failure modes only by doing the work.
- Write annotator instructions iteratively. Test on yourself. Test on a peer who knows nothing about legal NLP. Revise until both succeed.
- Compute inter-annotator agreement at 25, 50, 100 items. Don't wait until 500 to discover the protocol is broken.
- Adversarial seeding: deliberately include cases you predict will be hard. They reveal what the metric actually measures.

**Self-assessment:**
- Can you defend each annotation decision under a hostile question? (E.g., "why is *this* cite labeled VERIFIED?")
- Is your annotation protocol short enough to fit on 2 pages? (If not, it's too complex; simplify.)
- Have you considered who will use your benchmark in 2 years, and what they'd need from the documentation?

**Resources:**
- Bender & Friedman, *Data Statements for NLP* — the standard documentation framework
- Gebru et al., *Datasheets for Datasets* — the broader practice
- Read the README + datacard of CUAD, LegalBench-RAG before designing your own

---

## Months 8-9 (February-March 2027) — Reranker training, the ML-engineering core

**Primary skill:** the hyperparameter-search and ablation discipline.

**This is the month you stop running scripts and start designing experiments.**

**Deliberate practice:**
- For every experiment: hypothesis, prediction, prediction-falsifying outcome. Write all three BEFORE you run the experiment.
- After every experiment: actual result, comparison to prediction, what you learned, what to try next.
- Run lambda sweep with a clear stopping rule (e.g., "if no value improves over lambda=0.5 by >1%, stop").
- Treat compute as expensive. A 12-hour run that doesn't change your plan is wasted compute.

**Self-assessment:**
- Can you sketch a single result figure without looking? (If not, your tracking is broken.)
- Do you have a 1-sentence intuition for *why* each hyperparameter matters?
- When a result surprises you, do you investigate immediately, or do you let it slide?

**Resources:**
- Andrej Karpathy, *A Recipe for Training Neural Networks* (blog post, 2019) — gold standard
- The DEPO paper (cited in your reading list) for the multi-objective optimization mindset
- Your own wandb dashboard — review it weekly

---

## Month 10 (April 2027) — Ablations and analysis

**Primary skill:** the discipline of explaining *why* something works.

**Deliberate practice:**
- For each component of CiteCheck, run the without-it experiment.
- Write a 1-paragraph explanation of each result. The explanation should not be "the metric went up" — it should be a hypothesis about the underlying mechanism.
- Run a "stupid baseline" check: what's the simplest possible system that gets close to CiteCheck's score? If it's close, your contribution is weaker than you think; if it's far, you've validated the design.

**Self-assessment:**
- Can you predict, before running, what the "without-X" ablation will give?
- For the ablations that surprise you, do you have a hypothesis explaining the surprise?
- Have you stress-tested your method on out-of-distribution examples?

---

## Month 11 (May 2027) — Stability + writing prep

**Primary skill:** experimental rigor in writing-up.

**Deliberate practice:**
- Run every headline result with 3 seeds. Report mean ± std.
- For each result, ask: "what would convince a skeptic this isn't noise?"
- Begin a "limitations" file in your paper repo. Add to it as you discover limitations during writing.

**Self-assessment:**
- If a hostile reviewer asks "could this just be noise?", can you point to specific evidence (multiple seeds, statistical significance test, per-jurisdiction stability)?

---

## Month 12 (June 2027) — Paper drafting

**Primary skill:** technical writing.

**Deliberate practice:**
- 250-500 words/day of paper-draft prose. No backspace in the first hour.
- Write methods + results first (data is freshest). Intro + related work last (positioning is most fluid).
- Read your prose aloud daily. The ear catches what the eye misses.

**Self-assessment:**
- Can you state the paper's contribution in 1 sentence at any moment?
- Does every figure / table tell a complete story on its own?
- Have you killed every "obvious" or "clearly" — adverbs that signal weak argument?

**Resources:**
- Higham, *Handbook of Writing for the Mathematical Sciences* — chapters 2-3 (sentence-level discipline)
- Pinker, *The Sense of Style* — the only "popular" writing book that's actually about writing
- Pasanau & Pasanau, *How to Write a Lot* — for the productivity-of-writing question

---

## Month 13 (July 2027) — Writing under review

**Primary skill:** internalizing peer-review feedback.

**Deliberate practice:**
- Submit drafts to paper-swap partners. Read their feedback non-defensively.
- For each piece of feedback, write a 1-line response: accept (change made), partial (compromise), reject (with reason).
- After the response, take 24 hours before sending. You'll soften 30% of your "rejects."

---

## Month 14 (August 2027) — Submission engineering

**Primary skill:** the discipline of finishing.

**Deliberate practice:**
- Submit *early*. T-2 submissions degrade quality and add stress.
- Use the camera-ready checklist (`applications/submission/camera_ready_checklist.md`) ruthlessly.
- After submission, take 1 week off the paper.

---

## Months 15-16 (September-October 2027) — Application craftsmanship

**Primary skill:** matching what you want to what you're offering.

**Deliberate practice:**
- For every program, write down "what does this program want in a student?" before customizing the SOP.
- Read the lab's most recent paper before writing the per-program fit paragraph.
- For your top 3 programs, do "deep fit research": read every PhD student's bio, identify the lab culture.

---

## Months 17-18 (November-December 2027) — Operational excellence under pressure

**Primary skill:** the discipline of executing logistics without dropping balls.

**Deliberate practice:**
- Run every submission through the `final_week_protocol.md` whether or not you feel you need it.
- Use the deadline tracker as your single source of truth.
- After every submission, document what could be improved for the next.

---

## Months 19-22 (January-April 2028) — Interview poise

**Primary skill:** real-time communication of technical work.

**Deliberate practice:**
- Practice your 60-second pitch 20+ times before the first interview.
- Record yourself answering interview questions; watch the videos. The first 2 are painful; you'll find recurring tics.
- After every interview, journal what went well and what didn't. Patterns emerge by interview #3.

---

## Cross-cutting skills (develop continuously)

| Skill | How to develop | Where to check progress |
|---|---|---|
| Decision-making under uncertainty | `learning/decision_frameworks.md` — apply at every fork | `journal/decisions.md` |
| Productive solitude | Weekly: 4-hour blocks with no internet | `journal/weekly.md` |
| Talking about your work | Reading group + paper-swap + one talk per quarter | Recorded talks |
| Writing about your work | This entire curriculum | `journal/decisions.md` mini-essays |
| Reading critically | The 3-pass method, lifetime practice | Notes files |
| Recovering from failure | `wellness/sustainable_practices.md` | Self-assessment |

---

## What this curriculum will NOT teach you

These are real skills you'll need; they require different resources:

- **Statistics and probability beyond intro level.** Take a class or read Wasserman, *All of Statistics*, before Phase 2 if your stats foundation is weak.
- **Linear algebra and optimization for ML.** Strang's *Introduction to Linear Algebra* is the gentle path; Boyd & Vandenberghe's *Convex Optimization* is the deep path.
- **Programming language theory.** Some background in PL helps for grammar-based work like the Bluebook grammar. SICP if you have time; otherwise, focus on the constrained-decoding literature.
- **Legal doctrine.** You don't need a JD, but you should be able to distinguish holding from dicta. Read 2-3 chapters of a 1L civil procedure casebook (Friedenthal or Cound). Skim, don't memorize.

If you find a gap during Phase 2 execution, name it in `journal/decisions.md` and budget 1-2 weeks of explicit study before continuing.

---

## Closing note

This curriculum is intense. Doing it perfectly is impossible. The point is not perfection — the point is to know what you're trying to develop each month so that the deliberate practice happens, even if imperfectly.

Most people who try this plan will skip 40% of the deliberate-practice exercises. Those who do most of them will go into their PhD with a 6-12 month head start over their cohort.

The single most important habit: weekly retrospective in `journal/weekly.md`. Without it, you can't tell if the curriculum is working.
