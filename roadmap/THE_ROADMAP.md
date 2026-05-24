# The Roadmap — May 2026 through April 2028

**Purpose:** Single master document connecting every artifact in this workspace to a calendar date, with explicit guidance on what to start when, what skills to develop, what bottlenecks to anticipate, and what decisions you'll face. Read this first when you return to the project.

**How to use:** This is the navigation layer over the 4 phase plans. Each section here corresponds to a specific calendar window and tells you (a) what to do, (b) what artifacts to consult, (c) what skills to build that month, (d) what to watch for going wrong, (e) what decisions you'll make, and (f) where to get help if stuck.

---

## The arc in one paragraph

You are a Master's-level CS/AI graduate preparing to apply for a PhD in CS for Fall 2028 entry. You have 18 months (May 2026 – Dec 2027) before submission deadlines, plus a 4-month interview/decision window (Jan – Apr 2028). The plan is structured around one focused research project (**CiteCheck** — agentic RAG for verifiable US case-law citations) that anchors a portfolio of evidence proving you can do research. The success metric is not "publish a paper" — it's "give admissions committees enough evidence to advocate for you." Everything else (coursework deepening, recommender cultivation, application materials, interview prep) serves that one signal.

## The four phases at a glance

| Phase | Window | What you're doing | What you're proving |
|---|---|---|---|
| 1. Foundation | May–Aug 2026 (16 wk) | Reading, taxonomy, niche lock, problem statement | You can frame a research direction with rigor |
| 2. Build | Sep 2026 – Apr 2027 (8 mo) | Baseline reproduction → novel contribution → full experiments | You can execute a multi-month research project end-to-end |
| 3. Publish & Apply | May–Sep 2027 (5 mo) | Paper draft, workshop submission, SOPs finalized | You can communicate research to peer review |
| 4. Application Push | Oct–Dec 2027 (3 mo) | Submit 27 applications, recommender wrangling | You can execute logistics under pressure |
| 5. Interview & Decide | Jan–Apr 2028 (4 mo) | Interviews, offer evaluation, accept | You can advocate for yourself in conversation |

---

# Phase 1 — Foundation (May–Aug 2026)

## Week 0 — May 25, 2026 (NOW)

**You start here.** The first 3 days are about setting up so the next 16 weeks run cleanly.

### Day 1 (Monday morning)
- [ ] Install Zotero ([zotero.org](https://www.zotero.org/)) + browser connector — 30 minutes
- [ ] Open [`citecheck/README.md`](../citecheck/README.md) and skim
- [ ] Open [`roadmap/THE_ROADMAP.md`](THE_ROADMAP.md) (this file) and read end-to-end
- [ ] Open [`learning/how_to_read_papers.md`](../learning/how_to_read_papers.md) and skim
- [ ] Read [`docs/superpowers/specs/2026-05-24-phd-cs-study-plan-design.md`](../docs/superpowers/specs/2026-05-24-phd-cs-study-plan-design.md) cover to cover

### Day 2 (Tuesday)
- [ ] Open [`literature/deep_read_priority.md`](../literature/deep_read_priority.md). Schedule the next 4 weeks of Tier-1 reading on your calendar (10 papers, ~36 hours total, 8-9 hours/week of reading)
- [ ] Join one paper-reading group ([ML Collective](https://mlcollective.org/), [Cohere For AI](https://cohere.com/research/cohere-for-ai), or [Eleuther Discord](https://discord.gg/eleutherai)). 10 minutes to sign up.
- [ ] Create a GitHub repo `phd-research-log` (private OK). First post: 100 words on why you're preparing for a CS PhD in agentic RAG for legal applications. Date it 2026-05-31.
- [ ] Open [`project/m2_lock_checklist.md`](../project/m2_lock_checklist.md) and read once — these are the decisions you'll resolve by Aug 31.

### Day 3 (Wednesday)
- [ ] Read Quevedo et al. 2024 Legal NLP survey (Tier-1 paper #1) — start with this. It frames every other paper.
- [ ] Write structured notes in `literature/papers/quevedo-2024.md` following the template in [`docs/superpowers/plans/2026-05-24-phd-prep-phase-1-foundation.md`](../docs/superpowers/plans/2026-05-24-phd-prep-phase-1-foundation.md) Task 3 Step 3
- [ ] First entry in `journal/weekly.md` for the week of May 25 (use the template; 5-10 min)

### Days 4-7
- [ ] Read Tier-1 papers #2 and #3 (Pipitone LegalBench-RAG; Magesh hallucination paper)
- [ ] Set up VS Code or your editor of choice with the project workspace open
- [ ] Configure Zotero with the project's bibliographic style (use the EMNLP / ACL style)

## Weeks 1–4 — June 2026: Build literature map (Milestone M1)

**Skill development this month:** *Reading academic papers efficiently.* See [`learning/how_to_read_papers.md`](../learning/how_to_read_papers.md). Plan for 6-10 papers deeply-read, 15-20 papers skimmed.

**What you're trying to learn:** the landscape of legal NLP + agentic RAG + citation faithfulness. You're NOT trying to memorize methods — you're trying to build a mental map of who is doing what and where the open questions are.

### Daily cadence
- 2 hours of paper reading each weekday morning (~10 hours/week)
- 30 minutes journaling each evening (synthesize what you read; ask yourself "what would I tell a peer about this paper?")
- 1 paper-reading-group meeting per week (1-2 hours, listen first, contribute by week 3)

### Common bottlenecks (and protocols)
- **"This paper makes no sense."** → See [`roadmap/bottlenecks_protocols.md#paper-incomprehensible`](bottlenecks_protocols.md). Short answer: read 3-5 of its cited papers first, then return. If still stuck, post in the reading group.
- **"I keep starting papers and not finishing."** → Switch to the 3-pass method (see `learning/how_to_read_papers.md`). Only deeply read after the first two passes confirm relevance.
- **"I'm reading but not retaining."** → Open the notes file BEFORE you start reading. Write the question "what does this paper claim and how does it support that claim?" at the top. Answer it as you read.

### Decisions to make by end of M1 (Jun 30)
- **Which 3-5 clusters does the field decompose into?** (You'll write these to `literature/taxonomy.md`.)
- **Which 3 candidate gaps could become your project?** (You'll write these to taxonomy.md as well.)
- **Are you still on track for the Aug 31 M2 lock?** If not, why?

### Milestone M1 deliverables (Jun 30, 2026)
- [ ] `literature/reading_list.md` has 50 papers, no `pending` status
- [ ] `literature/papers/` has at least 7 deep-read notes
- [ ] `literature/taxonomy.md` exists with 3-5 clusters and 3 candidate gaps
- [ ] `journal/weekly.md` has 5 weekly entries

## Weeks 5–8 — July 2026: Deepen reading + draft 3 candidate problem statements

**Skill development this month:** *Synthesizing across multiple papers* — moving from "I read papers" to "I see patterns across papers."

This is the month you stop being a reader and start being a researcher with opinions. By end of July you should be able to say in 2 minutes: "the field is doing X, missing Y, and I want to work on Z."

### Daily cadence
- 1 hour reading (less than June — deepening, not breadth)
- 1 hour writing — drafting candidate problem statements, evolving the taxonomy
- 1 hour Phase 2 prep — if you've decided on a candidate, start exploring the dataset access, baseline code availability

### Common bottlenecks
- **"All 3 candidates feel equally good."** → That means you haven't dug deep enough yet. See [`learning/decision_frameworks.md#candidate-selection`](../learning/decision_frameworks.md). The right candidate has a *concrete* dataset and *concrete* baselines you can name in one sentence each.
- **"My candidates all overlap with someone else's recent paper."** → Re-search Scite for any 2026 papers in your area. The field moves quickly. If 3 candidates have all been scooped, you need a 4th. See [`literature/taxonomy.md`](../literature/taxonomy.md) for the gap analysis you can re-do.
- **"I want to pivot to a completely different topic."** → Pause. Re-read your own [`project/candidates.md`](../project/candidates.md) cross-validation analysis. Pivoting once is normal; pivoting twice usually means you're avoiding hard work in the chosen direction. Talk to your reading group first.

### Decisions to make by end of July (~Jul 27)
- **Top candidate selected.** (Write `**Selected for M2: Candidate [X]**` at the top of `project/candidates.md`.)
- **Plan B candidate identified** in case Candidate [X] runs into trouble at M3 in November.

## Weeks 9–13 — August 2026: Lock niche, prepare outreach (Milestone M2)

**Skill development this month:** *Writing precisely.* A 1-page locked problem statement is hard precisely because every sentence has to do work.

This is the month you commit. By Aug 31 you should be able to send your problem statement to an academic and not feel embarrassed. You should be able to defend every design choice for at least 30 seconds each.

### Daily cadence
- 30 min reading (Tier-1 wrap-up, Tier-2 starting)
- 1.5 hours writing — problem statement + advisor outreach
- 1 hour Phase 2 prep — install dependencies, set up the environment, start with the toy notebook
- Weekly: cold-email one academic for feedback (Task 13 in Phase 1)

### Major artifacts to finalize this month
- `project/problem_statement.md` — locked at v1.0
- `outreach/advisors.md` — top 10 starred, papers read for top 10
- `outreach/email_template.md` — customized per recipient before sending
- 2 cold emails sent (Šavelka and Nyarko are the most-likely-to-respond per Agent E's analysis)

### Common bottlenecks
- **"I keep editing the problem statement; it's never done."** → Set a hard deadline of Aug 28. Submit the v1.0 to your reading group for review even if you think it's imperfect. Perfection is the enemy of done. See [`learning/writing_practices.md`](../learning/writing_practices.md).
- **"The cold emails feel awkward to send."** → They are. See [`community/networking_strategy.md#cold-email-archetypes`](../community/networking_strategy.md). Send them anyway. Worst case: silence. Best case: a 5-minute reply that reshapes your project.
- **"I'm not getting any responses."** → 10-20% response rate is normal. Don't take it personally. Send to a different cluster of advisors. If 30+ emails get zero responses, something is wrong with the framing — show your problem statement to a peer for honest feedback.

### M2 lock (Aug 31, 2026)
This is the most important decision of Phase 1. Run through [`project/m2_lock_checklist.md`](../project/m2_lock_checklist.md) end-to-end. Decisions to commit:
1. Final research candidate (CiteCheck is the recommended pick per `project/candidates.md`)
2. Specific subtask scope
3. Annotator strategy (paid Upwork ~$2-3k vs. law student vs. self-only)
4. Plan B niche
5. Geographic program list (US + Europe per current recommendation)
6. Recommender shortlist (3-4 names)

**Why M2 matters:** every Phase 2 task assumes a locked candidate. Reversing this in November (at M3) costs ~3 weeks. Reversing in February costs ~3 months. Don't lock prematurely either — better to delay M2 a week than to lock the wrong candidate.

---

# Phase 2 — Build (Sep 2026 – Apr 2027)

## The macro structure

Phase 2 is 8 months: 4 work-months on the system + 2 months on the eval set + 2 months on the writing prep. The shape is:

```
Sep ───── Oct ───── Nov ───── Dec ───── Jan ───── Feb ───── Mar ───── Apr
infra    baselines  M3     eval set  method    M4     experiments  M5
                  (baselines)         (CitationResolver) (CiteCheck)  (full)
```

## Sep 2026: Infrastructure (Phase 2 Tasks 15-17)

**Skill development this month:** *Production-quality scientific code.* This is when you transition from "code that works in a notebook" to "code that someone else could run." See [`learning/research_skills_curriculum.md#month-1-engineering-discipline`](../learning/research_skills_curriculum.md).

### Week 1 (Sep 1-7)
- [ ] `git pull` the workspace; run `python scripts/verify_scaffold.py` to confirm structural integrity
- [ ] Create your Python venv; `pip install -e ".[dev]"` from `citecheck/`
- [ ] Copy `.env.example` → `.env`; register for a CourtListener API key
- [ ] Run `make test` — should pass on a fresh checkout
- [ ] Open `citecheck/notebooks/quickstart.ipynb` and walk through it
- [ ] Update `journal/weekly.md` with Phase 2 kickoff entry

### Week 2 (Sep 8-14)
- [ ] Start CAP bulk download (`python scripts/download_cap.py --jurisdictions us scotus federal_appellate`)
- [ ] While downloading: review `citecheck/src/citecheck/data/cap_loader.py` and verify the chunking strategy makes sense for your eval set
- [ ] Begin BM25 index build on whatever subset of CAP has downloaded

### Week 3-4 (Sep 15-30)
- [ ] Complete BM25 + dense indexes
- [ ] Load LegalBench-RAG + CUAD into standardized format
- [ ] Smoke test the retrieval pipeline end-to-end

### Bottlenecks
- **CAP download takes longer than expected.** It's ~100GB. Use `--jurisdictions us` subset first; expand if needed.
- **`pyserini` installation fails on Windows.** Requires JDK 21 on PATH. Document the install steps in your `journal/weekly.md` for future reference.
- **`bitsandbytes` doesn't work on Windows.** Known issue. Use Linux for the QLoRA training; Windows is fine for retrieval + inference.

## Oct 2026: Baselines start (Phase 2 Tasks 18-20)

**Skill development this month:** *Reproducibility discipline.* Reproducing other people's results is the single highest-leverage skill you'll develop in Phase 2.

### Cadence
- 3-4 days/week on baseline reproduction
- 1-2 days/week on Phase 2 prep tasks for November (eval set construction starts in Dec)

### Common bottleneck: "I can't reproduce the paper's numbers."
This is normal. See [`roadmap/bottlenecks_protocols.md#cant-reproduce-paper`](bottlenecks_protocols.md). Short answer: (1) confirm you have the exact model checkpoint; (2) confirm you have the exact eval dataset version; (3) confirm hyperparameters match; (4) email the authors politely if discrepancy >5%; (5) if all else fails, document the gap in your paper rather than pretending you reproduced.

## Nov 2026: M3 milestone (baseline reproduction complete)

This is the critical "is my problem still the right problem?" checkpoint. Use [`journal/phase2_milestone_templates.md`](../journal/phase2_milestone_templates.md) M3 template.

**Re-search the field.** Spend a half-day on Scite searching for any 2026 papers in your space. If someone published the CiteCheck paper in October, you need to know now, not in February.

**Lock-or-revise decision.** If baselines reproduce cleanly and no scoop has occurred, commit fully to CiteCheck and move into eval set construction. If something has changed, switch to Plan B per [`project/candidates.md`](../project/candidates.md).

## Dec 2026: Eval set construction (Phase 2 Tasks 24-26)

This is the most labor-intensive month of Phase 2. The 500-item eval set is the heart of the contribution.

### Decisions you must make this month
- **Annotator path locked.** Paid Upwork ($2-3.2k) vs. law-student collaborator (free, slower) vs. self-only adversarial. See [`project/m2_lock_checklist.md`](../project/m2_lock_checklist.md) §3.
- **If paying:** post the Upwork job by Dec 5. Vetting + onboarding takes 2-3 weeks.
- **If collaborating:** identify the law student by Dec 5. Co-authorship discussion (per `journal/decisions.md`).

### Common bottleneck: "Annotation is taking 4x longer than I planned."
Per Agent N: 1 trajectory annotation = ~30-45 min for a JD-level reviewer. 500 items × 30 min = 250 hours. Even at 25 hours/week from a paid annotator, that's 10 weeks. Plan accordingly — if Dec annotation slips, the entire downstream timeline slips.

## Jan–Feb 2027: Method prototyping (Phase 2 Tasks 27-32)

**Skill development this month:** *Reranker training at small scale.* QLoRA + multi-objective loss. See [`learning/research_skills_curriculum.md#months-5-6-deep-learning-discipline`](../learning/research_skills_curriculum.md).

If you have no prior reranker training experience, budget extra time for the first lambda value. Then the subsequent values go fast.

### M4 milestone (Feb 28, 2027)
End-to-end pipeline runs on 50 pilot questions. CiteCheck beats the strongest baseline on Fabrication Rate by ≥5 percentage points OR you re-scope.

## Mar–Apr 2027: Full experiments (Phase 2 Tasks 33-37)

**Skill development this month:** *Ablation discipline.* You'll run dozens of variants. Track everything in wandb. Write up results progressively (don't wait until M5).

### Common bottleneck: "My results are within 1σ of the best baseline."
Per Agent V: this kills the headline. See [`roadmap/bottlenecks_protocols.md#headline-result-not-significant`](bottlenecks_protocols.md). Short answer: pivot the framing from "we beat the baseline" to "we offer a new benchmark + a competitive method" — the benchmark contribution stands even if the method doesn't dominate.

### M5 partial (Apr 30, 2027)
Phase 2 closes. Hand off to Phase 3 with: full results tables, eval set v0.1 ready for release, paper outline ready for LaTeX skeleton population.

---

# Phase 3 — Publish & Apply (May–Sep 2027)

## May 2027: Stability + recommender identification

- Fill in `<TBD>` cells in `docs/papers/latex/main.tex`
- Generate paper figures (Phase 3 Task 42)
- Identify 4 recommenders (3 primary + 1 backup)
- Send recommender ask emails using `applications/recommender_packets/ask_emails/*.md`

## Jun 2027: Paper draft v0

- Convert outline to LaTeX skeleton (Phase 3 Task 44)
- Write Methods + Results + Ablations sections first
- Prepare recommender packets per [`applications/recommender_packets/_template.md`](../applications/recommender_packets/_template.md)

### Bottleneck: "I'm writing slowly."
See [`learning/writing_practices.md`](../learning/writing_practices.md). Short answer: write 250 words of bad prose daily; edit weekly. 250 × 30 days = 7,500 words = a full paper draft.

## Jul 2027: M6 paper draft v1

- Write Intro + Related Work + Discussion + Limitations
- Internal review pass 1 (LLM critique)
- Internal review pass 2 (external reader)
- Refine per-program SOPs (start replacing `[INSERT SPECIFIC ACCOMPLISHMENTS]` with the artifacts you actually shipped)

## Aug 2027: Submission prep + GRE if needed

- Polish paper for workshop submission
- Camera-ready code release prep
- Submit to NLLP @ EMNLP 2027 (verify exact deadline; typically Jun-Jul, may be Aug)
- arXiv preprint (use `applications/submission/arxiv_prep_guide.md`)
- Take GRE if required (most US programs don't; verify)

## Sep 2027: M7 closeout + program list lock

- Workshop reviews may arrive Oct-Nov 2027
- Lock final program list (15-25 from the 27 in `applications/submission/deadline_tracker_template.csv`)
- Complete per-program SOP tailoring for all locked programs
- Final recommender packets + program-by-program tables sent

---

# Phase 4 — Application Push (Oct–Dec 2027)

## Oct 2027: Portal setup + early submissions

Open accounts on all 27 portals. Order transcripts (`applications/submission/transcript_checklist.md`). Apply for fee waivers (`applications/submission/fee_waiver_lookup.md`). Submit NSF GRFP (Oct 15 deadline) for the auto-waiver path.

## Nov 2027: Bulk submission window

Use [`applications/submission/final_week_protocol.md`](../applications/submission/final_week_protocol.md) for each deadline cluster. T-21 reminders to recommenders. Start submitting Dec 1 deadline programs (Stanford, UCLA, NYU).

## Dec 2027: Final push

Bulk of US deadlines fall Dec 1, 8, 15. Submit one application per day. Use the blockers log religiously. Send T-7, T-2, escalation emails to recommenders as needed.

## Closeout (Dec 31, 2027)

Use [`journal/phase4_closeout_template.md`](../journal/phase4_closeout_template.md). Take a hard 5-7 day break Jan 1-7.

---

# Phase 5 — Interview & Decide (Jan–Apr 2028, NEW — not in original plan)

## Jan 5–Feb 15: First wave of interviews

Use [`applications/interviews/scenarios.md`](../applications/interviews/scenarios.md) + [`applications/interviews/per_advisor_prep.md`](../applications/interviews/per_advisor_prep.md). Most interviews are 30-60 min Zoom calls. Some programs run on-site days.

## Feb 15–Mar 15: Second wave + Europe interviews

European programs are often slower; some don't interview at all (Edinburgh, ETH for project-specific positions).

## Mar 15–Apr 15: Decision time

Use [`decisions/offer_evaluation.md`](../decisions/offer_evaluation.md) to compare offers. April 15 is the typical US PhD admit-by-date. After accepting, update [`journal/decisions.md`](../journal/decisions.md) with the final choice and the rationale.

If rejected from everywhere: use [`decisions/rejection_protocol.md`](../decisions/rejection_protocol.md). The next cycle is 12 months out; this is not catastrophic if you have a plan.

---

# Cross-phase skills development

Each phase has a primary skill focus, but several skills develop continuously across phases. See the dedicated docs:

| Skill | Primary file | Phases that develop it |
|---|---|---|
| Reading papers efficiently | [`learning/how_to_read_papers.md`](../learning/how_to_read_papers.md) | All phases |
| Note-taking and synthesis | [`learning/note_taking_system.md`](../learning/note_taking_system.md) | All phases |
| Research methodology + curriculum | [`learning/research_skills_curriculum.md`](../learning/research_skills_curriculum.md) | Phase 1-2 |
| Writing (papers, SOPs, emails) | [`learning/writing_practices.md`](../learning/writing_practices.md) | Phase 1-4 |
| Decision-making under uncertainty | [`learning/decision_frameworks.md`](../learning/decision_frameworks.md) | All phases |
| Networking + community | [`community/networking_strategy.md`](../community/networking_strategy.md) | All phases |
| Sustainable productivity | [`wellness/sustainable_practices.md`](../wellness/sustainable_practices.md) | All phases |
| Financial planning | [`financial/stipend_planning.md`](../financial/stipend_planning.md) | Phase 4-5 |
| Offer evaluation + decisions | [`decisions/offer_evaluation.md`](../decisions/offer_evaluation.md) | Phase 5 |

---

# Quick-start: the next 7 days

If you only have time to absorb one thing from this document, it's this. Here's what to do in the next 7 days:

| Day | What | Where |
|---|---|---|
| Monday | Set up environment: Zotero, reading group, blog | This file, week 0 |
| Tuesday | Read [`learning/how_to_read_papers.md`](../learning/how_to_read_papers.md), schedule the next 4 weeks of reading | learning/ |
| Wednesday | Read Quevedo 2024 survey, write notes | literature/papers/quevedo-2024.md |
| Thursday | Read Magesh 2025 hallucination paper, write notes | literature/papers/magesh-2025.md |
| Friday | Read Pipitone 2024 LegalBench-RAG, write notes | literature/papers/pipitone-2024.md |
| Saturday | Attend first reading group meeting | external |
| Sunday | Weekly retrospective entry; plan week 2 | journal/weekly.md |

That's it. Don't try to do everything in week 0. The 18 months is long; the pace is a marathon, not a sprint. The single most important habit is the weekly retrospective in `journal/weekly.md` — without it, drift is invisible.

---

# When you're stuck

See [`roadmap/bottlenecks_protocols.md`](bottlenecks_protocols.md) for protocols on the common stuck points. For things not in that doc, the general rule is:

1. **Write down the specific question.** "I'm stuck" is too vague to fix.
2. **Sleep on it.** Most "stuck" feels resolved the next morning.
3. **If still stuck after sleeping, talk to someone.** Reading group, paper-swap, Twitter/Bluesky, anyone who can hear you out.
4. **If still stuck after talking, switch context for 1-2 days.** Do something else in the project. Don't push through stuckness — almost always counterproductive.
5. **If still stuck after a week, the framing is probably wrong.** Re-read the problem statement; you may be optimizing the wrong thing.

---

# A final note

This roadmap is a guide, not a contract. Real research is messier than any plan can capture. The phase boundaries will blur. Some weeks will be wasted; some weekends will produce more than entire months. The goal is not to execute this plan perfectly — the goal is to use it as a baseline you can deviate from with reasons.

If at any point this plan stops making sense for your actual situation, update it. Commit the changes. Note in `journal/decisions.md` what changed and why. That commit history is itself evidence of how you think — and PhD admissions committees, eventually, will see exactly the kind of researcher you are by how you respond to a plan meeting reality.

Good luck. The next 18 months are going to be hard and worth it.
