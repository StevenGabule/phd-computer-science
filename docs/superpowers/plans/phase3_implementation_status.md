# Phase 3 Implementation Status (v0.1 scaffold)

**Date:** 2026-05-25
**Status:** v0.1 scaffold complete — paper outline + LaTeX skeleton + per-program SOP drafts + recommender packets + submission infrastructure all in place. Nothing has been *executed* yet (no paper writing on real numbers, no recommender asks sent, no applications submitted) — those activities belong to Phase 3 (May–Sep 2027).

This document maps the 24 tasks in `docs/superpowers/plans/2026-05-24-phd-prep-phase-3-publish-apply.md` to the scaffold artifacts that have been created.

---

## Coverage matrix

| Phase 3 Task | Plan section | Scaffold status | Files |
|---|---|---|---|
| **Task 40** Remaining stability / robustness experiments | May 2027 | ⏳ DEPENDS ON PHASE 2 | (Phase 2 Task 36 prerequisite) |
| **Task 41** Finalize results tables | May 2027 | 🟡 STRUCTURE READY | `docs/papers/latex/main.tex` Tables 1-6 with `<TBD>` cells (Phase 3 fills in real numbers) |
| **Task 42** Generate paper figures | May 2027 | 🟡 PLACEHOLDER | `docs/papers/latex/figures/.gitkeep`; Phase 3 generates from wandb + matplotlib |
| **Task 43** Identify 3-4 recommenders + draft ask emails | May 2027 | 🟢 TEMPLATES READY | `applications/recommender_packets/ask_emails/{4 archetype emails}.md` |
| **Task 44** Convert outline to LaTeX skeleton | Jun 2027 | 🟢 DONE | `docs/papers/latex/main.tex`, `references.bib`, `Makefile`, `README.md` |
| **Task 45** Write Methods + Results + Ablations | Jun 2027 | 🟡 STRUCTURE READY | Sections defined in LaTeX; awaiting real numbers from Phase 2 |
| **Task 46** Prepare recommender packets | Jun 2027 | 🟢 TEMPLATE READY | `applications/recommender_packets/_template.md` |
| **Task 47** Send recommender asks | Jun 2027 | 🟢 EMAILS READY | 4 ask-email variants in `applications/recommender_packets/ask_emails/` |
| **Task 48** Write Introduction + Related Work + Discussion + Limitations | Jul 2027 | 🟡 STRUCTURE READY | LaTeX has draft prose for Intro and Related Work from outline; Discussion/Limitations awaiting real results |
| **Task 49** Internal review pass 1 (LLM critique) | Jul 2027 | ⏳ FUTURE | (Phase 3 user task; paste draft into Claude/GPT) |
| **Task 50** Internal review pass 2 (external reader) | Jul 2027 | ⏳ FUTURE | (Phase 3 user task; share with reading group / paper-swap) |
| **Task 51** Refine SOP narrative core | Jul 2027 | 🟢 5 DRAFTS READY | `applications/sop_variants/{5 programs}.md` |
| **Task 52** M6 milestone retrospective | Jul 2027 | 🟢 TEMPLATE READY | `journal/phase2_milestone_templates.md` (M3/M4/M5 templates; Phase 3 will add M6/M7) |
| **Task 53** Polish paper for workshop submission | Aug 2027 | 🟢 CHECKLIST READY | `applications/submission/camera_ready_checklist.md` |
| **Task 54** Camera-ready code release prep | Aug 2027 | 🟡 STRUCTURE READY | `citecheck/` has README, LICENSE, CHANGELOG; Phase 3 tags v0.1.0-paper release |
| **Task 55** Submit paper to workshop | Aug-Sep 2027 | ⏳ FUTURE | (Phase 3 user task; verify NLLP @ EMNLP 2027 deadline) |
| **Task 56** arXiv preprint | Aug-Sep 2027 | 🟢 GUIDE READY | `applications/submission/arxiv_prep_guide.md` |
| **Task 57** Take GRE if needed | Aug 2027 | ⏳ FUTURE | (Phase 3 user task; verify per-program requirements first) |
| **Task 58** Start per-program SOP customization (top 5) | Aug 2027 | 🟢 DONE | 5 SOPs already drafted in `applications/sop_variants/` |
| **Task 59** Respond to workshop reviews | Sep 2027 | ⏳ FUTURE | (Phase 3 user task; covered by `camera_ready_checklist.md` Phase 2) |
| **Task 60** Lock final program list (15-25) | Sep 2027 | 🟢 STARTING POINT | `outreach/programs.md` has 22+ programs categorized |
| **Task 61** Complete per-program SOP tailoring | Sep 2027 | 🟡 5 DONE / ~15+ TO GO | Top 5 done; ~15-20 remaining programs need shorter customizations |
| **Task 62** Send follow-ups to recommenders | Sep 2027 | 🟢 PATTERN READY | Reminder schedule documented in `applications/recommender_packets/_template.md` |
| **Task 63** Phase 3 closeout retrospective | Sep 2027 | ⏳ FUTURE | (Phase 3 user task) |

**Legend:**
- 🟢 DONE / READY = AI-completable scaffold in place
- 🟡 STRUCTURE READY = Skeleton in place; needs real content from Phase 2 results or user judgment
- ⏳ FUTURE = User task during Phase 3 execution
- ⏳ DEPENDS ON PHASE 2 = Requires Phase 2 execution to complete first

---

## File inventory (this Phase 3 scaffold session)

| Artifact | Files | Word/Line counts |
|---|---|---|
| LaTeX paper project | `docs/papers/latex/{main.tex, references.bib, Makefile, README.md, figures/.gitkeep}` | TBD on commit |
| Per-program SOP variants | `applications/sop_variants/{stanford, cmu, jhu, umass, edinburgh}.md` | ~6,160 total words across 5 SOPs |
| Recommender packet | `applications/recommender_packets/_template.md` | ~1,400 words |
| Recommender ask emails | `applications/recommender_packets/ask_emails/{4 archetypes}.md` | ~1,300 words total |
| arXiv prep guide | `applications/submission/arxiv_prep_guide.md` | ~1,800 words |
| Camera-ready checklist | `applications/submission/camera_ready_checklist.md` | ~2,200 words |
| Portal navigation guide | `applications/submission/portal_navigation_guide.md` | ~3,000 words |
| Phase 3 status doc | `docs/superpowers/plans/phase3_implementation_status.md` (this file) | ~1,500 words |
| Limits documentation | `PHASE3_LIMITS.md` | ~1,300 words |

Total Phase 3 scaffold: ~18,700 words across 16+ files.

---

## Known limitations (v0.1 scaffold)

1. **Per-program SOPs cover only 5 of ~22 target programs.** The other 15-20 need similar treatment in Phase 3 Task 61, using the 5 existing as templates.
2. **LaTeX `<TBD>` cells everywhere results belong.** All result tables and figures are placeholders pending Phase 2 execution.
3. **Recommender names are not in the packet template.** User must identify the actual recommenders and customize the packet per-person.
4. **Portal navigation guide covers only top 10 programs.** Phase 3 Task 60 finalizes the program list; navigation for the remaining 12+ programs should be added as those applications open.
5. **arXiv endorser unspecified.** The arXiv guide notes endorsement is required for first submission; user must arrange an endorser by ~Aug 2027.
6. **GRE strategy unsettled.** Status doc notes "if required" — most US top programs no longer require, but user must verify each one.
7. **Citation-existence verifier mini-paper assumed.** The artifacts strategy commits the user to shipping this by Aug 2027; if it slips, the `[INSERT SPECIFIC ACCOMPLISHMENTS]` paragraph in every SOP becomes much harder to fill.
8. **NLLP @ EMNLP 2027 deadline unconfirmed.** Typical window is Jun-Jul; verify when CFP publishes (usually Apr-May 2027).
9. **UK/EU portal navigation thin.** ETH and Edinburgh covered; Cambridge, EPFL, UCL, Imperial, KU Leuven, TUM, Heidelberg, U. Amsterdam need additional portal walkthroughs in Phase 3.

---

## What's next (when Phase 3 actually starts, May 2027)

1. Pre-Phase-3 (May 1, 2027): User runs `git pull`, reviews scaffolded SOPs, drafts personal accomplishments to replace `[INSERT SPECIFIC ACCOMPLISHMENTS]` placeholders.
2. **Phase 3 kickoff:** User executes Task 40 (any remaining Phase 2 stability work) and begins Task 41 (filling LaTeX result tables with real numbers from Phase 2 outputs).
3. **Task 43-47 (May-Jun 2027):** Identify recommenders, customize packets, send ask emails (use the 4 archetype templates).
4. **Task 44-48 (Jun-Jul 2027):** Paper-writing crunch — convert outline to full LaTeX, write Methods/Results/Ablations sections.
5. **Task 53-56 (Aug-Sep 2027):** Submit paper to NLLP @ EMNLP 2027, post arXiv preprint, prepare camera-ready.

---

## How this status doc gets updated

When new code or content lands during Phase 3 execution, update this file alongside `citecheck/CHANGELOG.md` and `journal/decisions.md`. Phase 3 tasks transition from 🟢 READY → ✅ DONE → ⏳ EXECUTED as they actually happen.
