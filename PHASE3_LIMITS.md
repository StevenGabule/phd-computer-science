# What Cannot Be Done by AI Alone for Phase 3

**Why this file exists:** Phase 3 (May–Sep 2027) is the Publish & Apply phase of the 18-month plan. The scaffold (LaTeX paper, per-program SOP drafts, recommender packet templates, submission guides) was created in a single chat session, but the *execution* of Phase 3 requires resources outside any AI assistant's capability.

This document makes those limits explicit, mirroring `PHASE2_LIMITS.md`.

---

## What was done by AI in the Phase 3 scaffold session (2026-05-25)

- **LaTeX paper project** (`docs/papers/latex/`): main.tex skeleton, references.bib, Makefile, figures placeholder. ~8 pages of compile-safe structure with real prose where the outline already supported it and `<TBD>` markers where Phase 2 results belong.
- **5 per-program SOP variants** (`applications/sop_variants/`): Stanford, CMU, JHU, UMass, Edinburgh — each ~1,100-1,300 words, tailored to a specific advisor's recent paper, keeping `[INSERT SPECIFIC ACCOMPLISHMENTS]` as the user-fill placeholder.
- **Recommender packet template + 4 ask-email variants** (`applications/recommender_packets/`): reusable packet structure + targeted asks for master's-thesis-advisor, coursework professor, industry research supervisor, and collaborator/PI archetypes.
- **Submission infrastructure** (`applications/submission/`): arXiv prep guide, camera-ready checklist, per-program portal navigation guide for the top ~10 target programs.
- **Phase 3 status doc** (`docs/superpowers/plans/phase3_implementation_status.md`) mapping each of the 24 Phase 3 plan tasks to scaffolded artifacts.

## What CANNOT be done by AI for Phase 3 execution

| Task | Why it requires non-AI resources |
|---|---|
| **Fill in real experiment numbers in the paper** | Requires Phase 2 execution to actually run (CAP download, GPU training, eval set, baselines). All `<TBD>` cells in tables 1-6 remain until then. |
| **Generate paper figures** | Architecture diagram needs a real drawing tool; calibration plot needs real wandb data from Phase 2 Task 36 stability runs. |
| **Write recommender letters** | Letters must come from real humans who can speak to your work. AI cannot ghostwrite a letter and pretend it came from a professor. |
| **Take the GRE** | If any target program still requires it (verify per program — most no longer do), you must register and sit the exam. ETS testing requires biometric verification. |
| **Get advisor sign-off on SOPs** | Many strong applicants have their master's advisor read the SOP before submission. AI feedback is not a substitute. |
| **Submit to workshops** | OpenReview / SoftConf require human authentication. The Submit button is yours alone. |
| **Negotiate with the workshop chair** | If a paper is borderline and chairs reach out, the conversation requires you, not a model. |
| **Make program-list final decisions** | Drop / keep / add programs based on real-time signals from outreach, advisor responses, and your own preferences — these are judgment calls. |
| **Confirm portal-specific quirks** | Portals change between application cycles. Test each one yourself the day you create your account. |
| **Pay application fees / fee waivers** | Requires real payment instruments or eligibility-verified accounts; many waivers have submission windows that close before the application deadline. |
| **Pre-empt-style reviewer rebuttals** | If the paper gets reviews requesting changes, the rebuttal needs your judgment and your authority over the experiments. |

## What the scaffold lets the user do TODAY

- Read the LaTeX project + references and verify it compiles when Phase 2 data is ready (`cd docs/papers/latex && make pdf` once `latexmk` is installed)
- Review the 5 per-program SOP variants and refine the openings + advisor-specific paragraphs based on personal voice
- Adapt the recommender ask-emails to specific named recommenders (the `[FILL IN]` placeholders mark exactly what changes per-person)
- Walk through the portal navigation guide to identify which programs need account setup in advance of deadlines (some require transcript orders 4-6 weeks ahead)
- Begin the artifacts-by-Aug-2027 commitments from `applications/artifacts_strategy.md` so the `[INSERT SPECIFIC ACCOMPLISHMENTS]` placeholder has content to fill in
- Cross-check the Phase 3 status doc against the Phase 3 plan to see which tasks are scaffold-complete vs. require execution

## When Phase 3 actually begins (May 2027)

Per `docs/superpowers/plans/2026-05-24-phd-prep-phase-3-publish-apply.md`, Phase 3 sequences 24 tasks across 5 months. The transition trigger is Phase 2 closing (M5, end of Apr 2027). On May 1, 2027:

1. **Task 40 (May week 1):** Run any stability checks carried from Phase 2 Task 36 that were abbreviated. Update result tables.
2. **Task 41 (May week 2):** Finalize all results tables in `docs/papers/latex/main.tex` — replace every `<TBD>` with a real number.
3. **Task 42 (May week 3):** Generate paper figures (architecture, calibration, ablation bars) using matplotlib + wandb plot exports.
4. **Task 43 (May week 4):** Identify the 3-4 specific recommenders by name, customize the packets in `applications/recommender_packets/`, send the ask emails.

After that point, you're executing Phase 3 in real terms. The scaffold's job is done.

## The phrase "complete Phase 3"

Same nuance as `PHASE2_LIMITS.md`: "Phase 3 complete" in the chat-session sense means **the scaffold and all preparatory work are done** so the user can hit the ground running in May 2027. It does NOT mean the 5 months of paper-finishing, workshop submission, and application material finalization can be compressed into a chat session — that's not physically possible because the paper writing depends on Phase 2 results that don't exist yet.

The most a chat-session AI can do is what was done here: LaTeX skeleton with all known prose, BibTeX entries for all references, per-program SOP variants with advisor-specific paragraphs, recommender packet structure, submission infrastructure documentation. The remaining 5 months of execution belongs to the user, with AI assistance available throughout (e.g., editing paper sections after real results come in, drafting reviewer responses, refining SOPs based on advisor feedback).
