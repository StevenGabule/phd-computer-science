# PhD CS Application Prep — Project Workspace

**Owner:** John Paul L. Gabule
**Goal:** Strengthen application for PhD CS, Fall 2028 entry (deadlines Dec 2027 – Jan 2028)
**Research direction:** Agentic RAG for legal/contracts (primary candidate: **CiteCheck**)
**Timeline:** 18 months, May 2026 – December 2027

---

## Quick navigation

### Strategy & planning

- [`docs/superpowers/specs/2026-05-24-phd-cs-study-plan-design.md`](docs/superpowers/specs/2026-05-24-phd-cs-study-plan-design.md) — Master design spec (Tracks R/C/A/M × 4 phases)
- [`docs/superpowers/plans/2026-05-24-phd-prep-phase-1-foundation.md`](docs/superpowers/plans/2026-05-24-phd-prep-phase-1-foundation.md) — Phase 1: Foundation (May–Aug 2026)
- [`docs/superpowers/plans/2026-05-24-phd-prep-phase-2-build.md`](docs/superpowers/plans/2026-05-24-phd-prep-phase-2-build.md) — Phase 2: Build (Sep 2026 – Apr 2027)
- [`docs/superpowers/plans/2026-05-24-phd-prep-phase-3-publish-apply.md`](docs/superpowers/plans/2026-05-24-phd-prep-phase-3-publish-apply.md) — Phase 3: Publish & Apply (May–Sep 2027)
- [`docs/superpowers/plans/2026-05-24-phd-prep-phase-4-application-push.md`](docs/superpowers/plans/2026-05-24-phd-prep-phase-4-application-push.md) — Phase 4: Application Push (Oct–Dec 2027)

### Research project

- [`project/candidates.md`](project/candidates.md) — 4 candidate problem statements (A, B, C, D) with cross-candidate validation
- [`project/problem_statement.md`](project/problem_statement.md) — CiteCheck tight ~500-word problem statement (v0.1; awaiting M2 lock 2026-08-31)
- [`project/citecheck_design.md`](project/citecheck_design.md) — Full implementation detail (method, datasets, baselines, metrics, risks, references)
- [`project/m2_lock_checklist.md`](project/m2_lock_checklist.md) — All decisions due by Aug 31, 2026
- [`literature/reading_list.md`](literature/reading_list.md) — 56-paper reading list
- [`literature/taxonomy.md`](literature/taxonomy.md) — Cluster taxonomy + candidate gap analysis
- [`literature/deep_read_priority.md`](literature/deep_read_priority.md) — Sequenced read order (Tier 1-4) with rationale per paper
- [`literature/papers/`](literature/papers/) — Per-paper structured notes (deep reads go here)

### Applications & outreach

- [`outreach/programs.md`](outreach/programs.md) — Target programs (US + Europe top tier, 22 + NYU)
- [`outreach/advisors.md`](outreach/advisors.md) — 59 candidate advisors; top 10 starred (★)
- [`outreach/email_template.md`](outreach/email_template.md) — Base cold-email template
- [`outreach/email_variants/`](outreach/email_variants/) — Per-advisor customized email drafts (top 10)
- [`outreach/log.md`](outreach/log.md) — Outreach send log
- [`applications/sop_narrative_skeleton.md`](applications/sop_narrative_skeleton.md) — Reusable SOP narrative core for CiteCheck
- [`applications/artifacts_strategy.md`](applications/artifacts_strategy.md) — Pre-PhD artifact commitments to fill SOP track-record gap
- [`applications/interview_prep_template.md`](applications/interview_prep_template.md) — Per-program interview prep + master interview log (for Jan-Mar 2028)

### Journals

- [`journal/weekly.md`](journal/weekly.md) — Weekly retrospectives (every Sunday)
- [`journal/decisions.md`](journal/decisions.md) — Decision log (every load-bearing decision)

---

## Where am I in the plan?

The plan is structured as **4 phases × 4 tracks**:

| Phase | Months | Focus | Status |
|---|---|---|---|
| 1. Foundation | May–Aug 2026 | Literature map, niche lock, infrastructure | **Active** — pre-work + parts of M1 done by assistant; user executing M1-M2 |
| 2. Build | Sep 2026 – Apr 2027 | Baseline reproduction → novel contribution → full experiments | Plan written |
| 3. Publish & Apply | May–Sep 2027 | Paper draft, workshop submission, finalize application materials | Plan written |
| 4. Application Push | Oct–Dec 2027 | Submit all PhD applications | Plan written |

| Track | Weight | Description |
|---|---|---|
| R — Research Project | 70% | CiteCheck end-to-end |
| C — Curriculum Depth | 15% | Selective deepening of NLP/ML/RAG/agents |
| A — Application Materials | 10% | SOP, recommenders, program list, submissions |
| M — Methodology & Metacognition | 5% | Reading group, blog, weekly retrospectives |

---

## Key decisions locked

- **Approach:** Research Portfolio Sprint (70/15/10/5 across R/C/A/M)
- **Research direction:** Agentic RAG for legal/contracts, primary candidate CiteCheck (citation faithfulness)
- **Geographic application focus:** US + Europe top tier
- **Reference manager:** Zotero
- **Target entry:** Fall 2028 (apply Dec 2027 – Jan 2028)
- **Target venue (first paper):** NLLP @ EMNLP 2027 (primary), TrustNLP @ EMNLP 2027 (backup)

See [`journal/decisions.md`](journal/decisions.md) for the full chronological log.

---

## Outstanding decisions (resolve at M2 lock, 2026-08-31)

- Specific subtask scope for CiteCheck (federal appellate + Supreme Court only vs. include state appellate)
- Annotator strategy: paid Upwork JD (~$2k–$3.2k) vs. law-student collaborator vs. self-only
- Plan B research niche if M3 baseline reproduction reveals gap has closed
- Whether to add Asia (NUS, KAIST, Tsinghua, Toronto, McGill) to program list
- Final GRE strategy per program

---

## How to use this workspace

**If you're picking up after a break:**
1. Read [`journal/weekly.md`](journal/weekly.md) for the latest entry
2. Check current phase plan for the next pending task
3. Reference [`project/problem_statement.md`](project/problem_statement.md) to re-anchor on the research direction
4. Skim [`literature/taxonomy.md`](literature/taxonomy.md) if you've been away >4 weeks (the field moves fast)

**If you're updating after deep-reading papers:**
1. Add structured notes to `literature/papers/{lastname}-{year}.md`
2. Update status in `literature/reading_list.md` (`pending` → `deep-read`)
3. Revise `literature/taxonomy.md` if cluster boundaries or candidate gaps shift
4. Log meaningful judgment changes in `journal/decisions.md`

**If you're ready to outreach an advisor:**
1. Star them in `outreach/advisors.md` if not already
2. Customize from `outreach/email_variants/{lastname}.md` (top 10 pre-drafted) or `outreach/email_template.md`
3. Attach current `project/problem_statement.md` as PDF
4. Log the send in `outreach/log.md` immediately
