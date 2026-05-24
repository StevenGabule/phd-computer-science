# What Cannot Be Done by AI Alone for Phase 4

**Why this file exists:** Phase 4 (Oct–Dec 2027) is the Application Push phase of the 18-month plan. The scaffold (deadline tracker, blockers log, transcript checklist, fee-waiver lookup, recommender follow-up emails, final-week submission protocol, interview prep) was created in a single chat session, but the *execution* of Phase 4 requires resources outside any AI assistant's capability.

This document makes those limits explicit, mirroring `PHASE2_LIMITS.md` and `PHASE3_LIMITS.md`.

---

## What was done by AI in the Phase 4 scaffold session (2026-05-25)

- **Master deadline tracker** (`applications/submission/deadline_tracker_template.csv`): 27 programs pre-populated with portal URLs, deadlines, fees, waiver paths, SOP word limits, recommender methods, status columns.
- **Blockers log** (`applications/submission/blockers.md`): live-issue tracker template with eight common-blocker types pre-templated.
- **Transcript checklist** (`applications/submission/transcript_checklist.md`): 5-phase plan for ordering transcripts from every institution attended.
- **Fee-waiver lookup** (`applications/submission/fee_waiver_lookup.md`): per-program waiver paths + total fee budget ($1,600-3,200).
- **Recommender follow-up email sequence** (`applications/recommender_packets/followup_emails/{T-21, T-7, T-2, T-escalation}.md`): timed reminder ladder from 3-weeks-out through deadline-missed escalation.
- **Final-week submission protocol** (`applications/submission/final_week_protocol.md`): day-by-day Sunday-through-Saturday playbook for each deadline cluster.
- **Interview scenarios** (`applications/interviews/scenarios.md`): 10 common interview questions with example answers, length targets, pitfalls.
- **Per-advisor interview prep** (`applications/interviews/per_advisor_prep.md`): rehearsed openings + likely-questions + questions-to-ask for the top 10 starred advisors.
- **Phase 4 closeout retrospective template** (`journal/phase4_closeout_template.md`).
- **Phase 4 status doc** (`docs/superpowers/plans/phase4_implementation_status.md`) mapping each of the 20 Phase 4 plan tasks to scaffold artifacts.

## What CANNOT be done by AI for Phase 4 execution

| Task | Why it requires non-AI resources |
|---|---|
| **Submit applications** | Each program portal requires human authentication (sometimes 2FA), file uploads, and a Submit button click. There is no API-driven submission for PhD applications. |
| **Pay application fees** | Requires real payment instruments (credit card, PayPal). Some programs only accept institutional payment systems. |
| **Apply for fee waivers** | Requires income documentation, FAFSA verification, GRFP fellowship applicant status, or other personal-info inputs that AI cannot supply. |
| **Order official transcripts** | Each registrar requires the student's authenticated request, often with payment, sometimes with a signed FERPA release. |
| **Get recommenders to write letters** | Letters must come from real humans. AI cannot ghost-write a letter and pretend it came from a professor. |
| **Sit the GRE** | If any target program still requires GRE (verify per program — most US top programs no longer do), the user must register and sit the exam. ETS testing requires biometric verification. |
| **Field-call interviews** | Most interviews are 30-60 minutes of real-time conversation. AI can prep but cannot answer in your voice. |
| **Make decision calls** | Drop / keep / add programs based on real-time signals from advisor responses, partner's geographic constraints, financial aid offers — all judgment calls. |
| **Negotiate with admissions** | If a deadline extension is needed (recommender delay, transcript delay, technical issue), the conversation requires you, not a model. |
| **Maintain emotional regulation through the application crunch** | Dec 2027 will be the highest-stress month of the 18-month plan. AI can suggest sleep / caffeine / one-social-commitment-per-week protocols (in `final_week_protocol.md`) but cannot enforce them. |

## What the scaffold lets the user do TODAY

- Customize `deadline_tracker_template.csv` with personal program list (e.g., drop Oxford if user follows the Phase 2 recommendation)
- Verify portal URLs and deadlines in the tracker against the programs' 2027-2028 admissions pages
- Order transcripts in October 2027 per `transcript_checklist.md`
- Apply for fee waivers in October-November 2027 per `fee_waiver_lookup.md`
- Customize per-recommender follow-up emails from the T-21 / T-7 / T-2 / escalation templates
- Walk through the final-week protocol mentally; identify gaps before the actual deadline crunch
- Rehearse interview scenarios out loud (literally read `scenarios.md` aloud, time the answers)
- Prepare per-advisor questions from `per_advisor_prep.md` so the user can pull them up quickly when an interview is scheduled with <72 hours notice

## When Phase 4 actually begins (October 2027)

Per `docs/superpowers/plans/2026-05-24-phd-prep-phase-4-application-push.md`, Phase 4 sequences 20 tasks across 3 months. The transition trigger is Phase 3 closing (workshop submission complete, application materials finalized, recommenders briefed). On Oct 1, 2027:

1. **Task 64 (Oct week 1):** Open each program's deadline-tracker row; verify URLs and deadlines for the 2027-2028 cycle.
2. **Task 65 (Oct week 1-2):** Create accounts on every program portal; complete fixed fields.
3. **Task 66 (Oct week 2):** Order transcripts per `transcript_checklist.md`.
4. **Task 67 (Oct week 2-3):** Apply for fee waivers per `fee_waiver_lookup.md`.
5. **Task 68 (Oct week 3):** Workshop paper status check (NLLP @ EMNLP 2027 review window).
6. **Task 69 (Oct week 4):** Submit any Oct/Nov-deadline programs + fellowships (NSF GRFP, Hertz, OpenAI).

After that, you're executing Phase 4 in real terms.

## The phrase "complete Phase 4"

Same nuance as PHASE2_LIMITS and PHASE3_LIMITS: "Phase 4 complete" in the chat-session sense means **the scaffold and all preparatory work are done** so the user can execute cleanly in Oct-Dec 2027. It does NOT mean the 3 months of submission, recommender wrangling, and interview prep have been compressed into a chat session — that's not physically possible because:

- Applications require human authentication on 27 separate portals.
- Recommender letters require real humans willing to spend 2-4 hours per letter.
- Interviews require real-time conversation skill that AI cannot exercise on the user's behalf.

The most a chat-session AI can do is what was done here: the deadline tracker pre-populated with 27 programs, the recommender follow-up email sequence templated, the per-advisor interview prep with rehearsed openings for the top 10 starred advisors, the day-by-day submission protocol, the blockers-logging mechanism, and the explicit documentation of what AI cannot do. The remaining 3 months of execution belongs to the user, with AI assistance available throughout (e.g., debugging a portal upload that's failing at midnight, drafting a custom extension-request email to a specific program, rehearsing an interview answer the user wants tightened).
