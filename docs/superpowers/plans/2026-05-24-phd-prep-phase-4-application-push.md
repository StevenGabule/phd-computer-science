# PhD Prep — Phase 4 (Application Push) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Submit all 15-25 PhD applications by their stated deadlines (predominantly Dec 1 – Jan 15 2028) with strong, program-tailored materials, complete recommender delivery, fee handling, and post-submission follow-through (workshop-paper handling + interview preparation).

**Architecture:** Phase 4 is execution-heavy rather than research-heavy. Nineteen tasks across three months: (a) October stands up the master deadline tracker, opens all portals, kicks off transcripts, secures fee waivers, and submits any Oct/Nov-deadline programs/fellowships; (b) November is the polish-and-bulk-submit window where SOPs are read-aloud-finalized and recommender follow-ups go out 3 weeks before each deadline; (c) December is the high-stakes final push for the Dec 1/8/15 US clusters, plus daily letter-delivery monitoring, late-deadline Europe programs, closeout retrospective, interview prep, and handling of workshop-paper acceptance updates. Two milestone reviews: M-Submit (after Dec 15 deadline cluster passes) and M-Closeout (end of December, full Phase 1–4 retrospective).

**Tools & Resources:**
- Google Sheets OR Notion for the master deadline tracker (single source of truth — pick one and stick with it)
- Interfolio Dossier (https://www.interfolio.com/) for managing recommender letters where supported
- Each program's individual portal (CMU SCS, Stanford Graduate Admissions, MIT Apply, Berkeley CalCentral, etc.)
- Calendar (Google Calendar) with alerts at T-21, T-7, T-2, T-0 for every deadline
- LaTeX or Word for any program-specific essay/form
- pandoc for converting markdown SOP drafts to PDF when portal requires PDF
- Email (Gmail) for recommender follow-ups and admissions-office contact
- Payment method (credit card with $3K+ headroom) for application fees
- PDF reader with annotation (for last-pass SOP read-throughs)

---

## File Structure

All paths relative to `C:\Users\John Paul L. Gabule\Desktop\phd-computer-science`. Builds on directories established in Phases 1–3.

```
applications/
  deadline_tracker.md          # mirror of Sheets/Notion master tracker (markdown copy)
  fee_budget.md                # fee budget + waiver tracking
  blockers.md                  # portal bugs / surprises log
  per_program/
    {program-slug}/
      sop.pdf                  # final SOP submitted (copy)
      cv.pdf                   # CV submitted (copy)
      transcripts/             # transcripts uploaded
      essays/                  # any extra essays (diversity, research interests)
      confirmation.md          # submission confirmation details
      portal_notes.md          # idiosyncrasies of this portal
  submitted/                   # consolidated archive after submission
    {program-slug}/
  fellowships/
    nsf_grfp/
    hertz/
    openai_fellows/
    {other}/
outreach/
  recommenders.md              # 3-5 recommenders, contact, status per program
  recommender_followups.md     # log of every recommender ping
journal/
  weekly.md                    # weekly entries continue from Phases 1-3
  decisions.md                 # decision log continues
  phase4_retro.md              # M-Closeout 18-month retrospective
interviews/
  prep.md                      # interview prep workbook (Task 80)
  per_program_qa.md            # advisor-specific Q&A prep
publications/
  citecheck_workshop/
    review_response.md         # rebuttal / camera-ready notes (Task 68)
    final_camera_ready.pdf     # if accepted (Task 81)
```

---

## Pre-work — Last week of September 2027

### Task 63: Phase 4 kickoff + import Phase 3 outputs

**Artifacts:**
- Create: `applications/`, `applications/per_program/`, `applications/submitted/`, `applications/fellowships/`, `interviews/`, `publications/citecheck_workshop/` directories
- Create: `applications/deadline_tracker.md`, `applications/fee_budget.md`, `applications/blockers.md`
- Create: `outreach/recommender_followups.md`, `interviews/prep.md`

- [ ] **Step 1: Create directory structure**

```powershell
New-Item -ItemType Directory -Force applications\per_program, applications\submitted, applications\fellowships\nsf_grfp, applications\fellowships\hertz, applications\fellowships\openai_fellows, interviews, publications\citecheck_workshop | Out-Null
```

Verify: `Test-Path applications\per_program, applications\submitted, interviews, publications\citecheck_workshop` returns `True True True True`.

- [ ] **Step 2: Confirm Phase 3 outputs are present**

Verify these exist (from Phase 3):
- `outreach/programs.md` — locked program list of 15-25 programs (Task 60)
- `applications/sop_variants/` — per-program SOP variants (Task 61)
- `outreach/recommenders.md` — recommenders briefed (Tasks 47, 62)
- `applications/artifacts_strategy.md` — artifact inventory complete
- `publications/citecheck_workshop_submission.pdf` — workshop submission (Task 55)
- `publications/citecheck_arxiv.pdf` — arXiv preprint (Task 56)

If any of these are missing, STOP and fix in Phase 3 before continuing. The deadline pressure will only compound missing inputs.

- [ ] **Step 3: Log Phase 4 kickoff**

Append to `journal/decisions.md`:

```markdown
| 2027-09-28 | Phase 4 kickoff: application push begins | Phase 3 outputs verified; transitioning from build/write phase to submit/execute phase | No — applications begin Oct 1 |
```

---

## Month 1 — October 2027: Portal setup + early submissions

### Task 64: Build/update the master deadline tracker

**Artifacts:**
- Create: `applications/deadline_tracker.md` (markdown mirror)
- Create: a Google Sheets or Notion master tracker (working copy)

- [ ] **Step 1: Pick one tool — Sheets OR Notion. Not both. Not a third.**

Recommendation: Google Sheets for simplicity, conditional formatting on due dates, and easy sharing if you need to give a recommender visibility. Notion is fine if you already live in it. Whatever you pick, every program belongs in exactly one place.

- [ ] **Step 2: Create the master tracker with these columns (one row per program)**

| Column | Notes |
|---|---|
| Program | "CMU MLD", "Stanford CS PhD", etc. |
| Deadline (UTC) | Convert local deadline to UTC; many portals close at 11:59 pm at a specific timezone |
| Deadline (local) | The program's stated deadline + timezone |
| Days until deadline | Sheets formula: `=A2 - TODAY()` (update daily) |
| Application URL | Direct link to the portal |
| Application fee (USD) | Typical $75–130 |
| Fee waiver eligible? | Y/N + program (FreeApp, GEM, NSF, departmental) |
| Fee waiver status | not-applied / applied / granted / denied |
| GRE required? | Y/N (most top US CS programs dropped GRE — verify per program) |
| GRE waived if not required? | Some programs accept GRE if you have it; flag if optional |
| SOP word/page limit | Verify in the application instructions, not from external blog posts |
| Extra essays | Diversity, research interest, personal background — list each |
| Recommender method | Interfolio / portal form / email |
| # recommenders | Usually 3, occasionally 2 or 4 |
| Recommenders assigned | Names of your 3-5 LoR writers used for this program |
| Recommender request sent? | Date sent to recommenders via the portal |
| Transcripts | "official-required" / "self-uploaded-OK" / "deferred-on-admit" |
| Transcript request sent? | Date you ordered official transcripts |
| Test scores | TOEFL/IELTS required? GRE? Subject? |
| CV/Resume | Required? Page limit? |
| Writing sample | Required? Length? |
| Submission status | not-started / drafting / submitted / confirmed |
| Submitted date | After submit |
| Confirmation number | After submit |
| Notes | Quirks (e.g., "portal crashes in Safari", "fee is $0 if you log in via .edu") |

- [ ] **Step 3: Mirror the tracker as a markdown table in `applications/deadline_tracker.md`**

The markdown copy is for git/version-control visibility. Update it weekly (full overwrite is fine).

- [ ] **Step 4: Populate every row from `outreach/programs.md`**

For each of the 15-25 programs:
1. Visit the program's PhD admissions page (search: "[program name] CS PhD admissions")
2. Find the application instructions for Fall 2028 entry (page should be live by Oct 2027)
3. Fill in all columns
4. Bookmark the portal URL

Time budget: ~30 min per program × 20 programs = ~10 hours. Spread over 3 days.

- [ ] **Step 5: Calendar alerts**

For every program, create 4 Google Calendar reminders:
- T-21 days before deadline: "[Program] — recommender follow-up due"
- T-7 days: "[Program] — final SOP read-aloud + submit"
- T-2 days: "[Program] — confirm letters delivered + submit if not done"
- T-0 (8 hours before deadline): "[Program] — HARD STOP final check"

- [ ] **Step 6: Identify your three deadline clusters**

US top-30 cluster around three dates. Highlight them in the tracker:
- **Dec 1 cluster** (varies year, but commonly includes some of: CMU, MIT, Princeton, Berkeley)
- **Dec 8 cluster** (commonly: UW, UCLA, UMD)
- **Dec 15 cluster** (commonly: Stanford, Cornell, Yale)
- **Jan 1, Jan 5, Jan 15** scattered (some Europe programs, Caltech, GA Tech)

Verify each by visiting the actual admissions page for Fall 2028 cycle — dates shift year to year.

- [ ] **Step 7: Log Task 64 in weekly journal (week of 2027-10-04)**

### Task 65: Open application accounts on all program portals

**Artifacts:**
- Modify: `applications/deadline_tracker.md` (mark portal-created status)
- Create: `applications/per_program/{slug}/portal_notes.md` (per program)

- [ ] **Step 1: For each program, create an account on its portal**

Each portal is a separate registration. Use the SAME email address across all of them (your primary, professional Gmail). Use a password manager — you'll have 15-25 portal logins.

- [ ] **Step 2: Complete the fixed/biographical fields in every portal**

Fields that are identical across applications:
- Name, date of birth, contact info
- Citizenship + visa status
- Demographic information (optional — fill in per personal preference)
- Educational history (institutions, dates, GPA, degree)
- CV upload (use latest from `applications/artifacts_strategy.md`)
- Self-uploaded transcripts (most portals accept unofficial at application time)

Time budget: ~20 min per portal × 20 portals = ~7 hours. Spread over 2-3 days.

- [ ] **Step 3: Note per-program portal quirks in `applications/per_program/{slug}/portal_notes.md`**

Common quirks to record:
- "Portal does not auto-save — save manually every 5 min"
- "File upload limited to 5 MB; SOP must be PDF only"
- "Recommender invitation is sent only after you submit the application"
- "Save button is hidden at the bottom of a long form"
- "Logout after 30 min of inactivity"

- [ ] **Step 4: Mark portal-opened status in tracker**

For every row, set a "portal opened" flag = Yes. If any portal isn't live yet for Fall 2028, set a calendar alert to check weekly until it opens.

- [ ] **Step 5: Log Task 65 in weekly journal (week of 2027-10-04)**

### Task 66: Order official transcripts from every institution attended

**Artifacts:**
- Modify: `applications/deadline_tracker.md` (transcript request column updated)
- Create: receipts in `applications/per_program/{slug}/transcripts/` after delivery

- [ ] **Step 1: List every institution where you took college-level coursework**

For most users this is: undergraduate, Master's, and any community college / dual-enrollment.

- [ ] **Step 2: For each institution, find the transcript request portal**

Most use Parchment (https://www.parchment.com/), National Student Clearinghouse, or the registrar's own page. Order an OFFICIAL ELECTRONIC transcript sent to:
- Yourself (one copy you keep) — for unofficial use
- Each program that requires official transcripts at application time

Important: some programs only require official transcripts on admission. Most accept unofficial (self-uploaded) at application time. Check the per-program rules in your tracker (Column: Transcripts) before ordering.

- [ ] **Step 3: Pay attention to lead time**

Electronic transcripts: usually 1-3 business days. Paper transcripts: 1-3 weeks. Order at least 3 weeks before your earliest deadline. If you have any pending grade changes or degree certifications, allow 4 weeks.

Total transcript cost: typically $10-25 per request × number of programs. Add this to `applications/fee_budget.md`.

- [ ] **Step 4: Track delivery in tracker**

For each program requiring official transcripts, set "transcript request sent" = date. Check delivery confirmation 5 business days later.

- [ ] **Step 5: Risk flag — transcript with degree-conferral pending**

If your most recent transcript is missing the conferral date for your Master's degree, contact your registrar IMMEDIATELY. Many programs will reject a transcript that doesn't show the degree was awarded. The fix can take 2-4 weeks.

- [ ] **Step 6: Log Task 66 in weekly journal (week of 2027-10-04)**

### Task 67: Application fee strategy + budget

**Artifacts:**
- Create: `applications/fee_budget.md`
- Modify: `applications/deadline_tracker.md` (fee waiver status column)

- [ ] **Step 1: Compute the worst-case fee total**

Open `applications/fee_budget.md`:

```markdown
# Application Fee Budget — Fall 2027 cycle

## Worst-case fees (no waivers granted)
| Program | Fee (USD) | Notes |
|---|---|---|
| ... | $... | |
| **TOTAL (worst case)** | **$X,XXX** | |

## Likely-case after waivers
| Program | Original fee | Waiver type | Final |
|---|---|---|---|
| ... | | | |
| **TOTAL (likely)** | **$X,XXX** | | |

## Transcripts
| Institution | # copies | Per-copy cost | Subtotal |
|---|---|---|---|
| | | | |
| **Transcript subtotal** | | | |

## Other (e.g., GRE if still required, score-send fees)
| Item | Cost |
|---|---|
| | |

## GRAND TOTAL | $X,XXX |
```

For 20 programs at $80-130 each, worst-case fee total is **$1,600–$2,600**. Including transcripts ($200-400) and any GRE score-sends ($30 each), realistic budget headroom: **$2,500–$3,500**.

- [ ] **Step 2: Apply for fee waivers everywhere eligible**

Common waiver sources:
- **FreeApp / Council of Graduate Schools** — many top programs participate; income-based
- **GEM Consortium** — for underrepresented groups in STEM (https://www.gemfellowship.org/)
- **NSF GRFP applicants** — some programs waive fees for GRFP applicants
- **Departmental waivers** — many CS departments have their own form (search: "[program] application fee waiver CS")
- **First-gen, low-income, military veteran, peace corps** — program-specific
- **Conference fee waivers** — if you attended a recruiting event (CRA-WP, SIGCSE), often a waiver code

Each waiver application: 15-30 minutes. Apply as early in October as possible; some have submission windows that close before the application deadline.

- [ ] **Step 3: Update tracker with waiver status per program**

After applying for waivers, set the "Fee waiver status" column = applied. Re-check weekly. If granted, update final fee in budget.

- [ ] **Step 4: Confirm payment method**

Ensure your credit card has $3K+ headroom across November-December. Some portals charge at submission, some pre-authorize and charge later. Don't get blocked at the submit step.

- [ ] **Step 5: Log Task 67 in weekly journal (week of 2027-10-11)**

### Task 68: Workshop paper status check + reviewer response prep

**Artifacts:**
- Create: `publications/citecheck_workshop/review_response.md`

- [ ] **Step 1: Check the NLLP @ EMNLP 2027 workshop timeline**

Workshop notifications typically land 4-8 weeks after submission. Phase 3 submitted in Sept 2027, so expect notifications in October-November 2027. Verify the actual dates on the workshop website (https://nllpw.org/ or the EMNLP 2027 colocated workshops page) and set a calendar reminder.

- [ ] **Step 2: If reviews arrive in October — respond promptly**

Workshop reviews are typically less formal than main-conference reviews. Three scenarios:

**Scenario A: Accept** — prepare camera-ready by the deadline (usually 2-3 weeks after notification). Apply reviewer suggestions; finalize bibtex; convert to ACL/EMNLP template if not already. Save final PDF to `publications/citecheck_workshop/final_camera_ready.pdf`. See Task 81.

**Scenario B: Conditional accept / minor revisions** — same as accept but with revision tracking. Document changes in `review_response.md`.

**Scenario C: Reject** — your workshop submission was a stretch goal. Don't panic. Re-target a Spring workshop (e.g., NAACL workshops, ACL workshops). The arXiv preprint (Task 56) is your citable artifact regardless.

- [ ] **Step 3: Whatever the outcome, update SOPs**

If accepted: add "Accepted at NLLP @ EMNLP 2027" to your CV and the publications section of every SOP variant in Task 70. If rejected: keep the arXiv reference; do not mention rejection. Either way, this updates the materials you submit later.

- [ ] **Step 4: Log Task 68 in weekly journal**

Track decision arrival date and your response timeline. This is the rare task where the trigger is external — do not let it slip if it arrives mid-Oct.

### Task 69: Submit any October/November-deadline applications + fellowships

**Artifacts:**
- Modify: `applications/deadline_tracker.md`
- Create: `applications/per_program/{slug}/confirmation.md` for each submission
- Create: `applications/fellowships/{name}/` submission records

- [ ] **Step 1: Identify October/November deadlines from the tracker**

Common early-window targets:
- **Some Europe programs** — ETH (rolling), Oxford (early Jan but verify), Cambridge (some programs early Dec)
- **NSF GRFP** — usually mid-to-late October for Fall 2028 cohort (deadline by field; CS typically mid-Oct)
- **Hertz Fellowship** — usually end of October / early November
- **OpenAI Residency / Fellows** — varies; check website
- **Google PhD Fellowship** — varies; check website
- **Microsoft Research PhD Fellowship** — varies
- **Apple Scholars in AI/ML** — varies

- [ ] **Step 2: Submit NSF GRFP first if eligible**

GRFP requires:
- Research proposal (~2 pages)
- Personal statement (~3 pages)
- 3 reference letters via the GRFP portal (separate from PhD program letters — coordinate carefully with recommenders)
- Transcripts from all institutions

GRFP is high-leverage: a successful application provides 3 years of funding portable to any US program; many programs prioritize GRFP recipients in admissions.

- [ ] **Step 3: For each fellowship submitted, archive a copy to `applications/fellowships/{name}/`**

Include: final essay PDFs, submission confirmation, recommender list, fee receipt (if any).

- [ ] **Step 4: For each Oct/Nov-deadline PhD program, complete the per-program submission protocol (see Task 76 protocol, applied early)**

- [ ] **Step 5: Log Task 69 in weekly journal**

Each submission gets a separate entry. Note: hours spent, any portal issues encountered (add to `blockers.md`).

---

## Month 2 — November 2027: Bulk submission window opens

### Task 70: Final SOP polish per program

**Artifacts:**
- Modify: `applications/sop_variants/{program-slug}.md` for each program
- Create: `applications/per_program/{slug}/sop.pdf` for each program

- [ ] **Step 1: For each program, run a 4-pass polish on the SOP variant**

Pass 1 — **Read aloud**. The brain skips errors when reading silently; the mouth does not. Read every SOP aloud. Flag every awkward phrase and rewrite it. Time per program: 30-45 min.

Pass 2 — **Per-program fact-check**. Verify:
- Advisor names are spelled correctly and current at the program (faculty move — confirm via the program's current faculty page in November 2027)
- Specific paper titles you reference are quoted exactly
- Any quoted statistic or claim is sourced (have a citation handy if asked)
- The program name and department are correct (do not send "I'm excited to apply to MIT" to a CMU portal — this happens)

Pass 3 — **Word/page limit**. Verify against the program's stated limit (NOT a blog post; check the actual application instructions). Cut to fit. If the program says 1000 words, 1001 words is over the limit.

Pass 4 — **Copy-edit**. Run through Grammarly or similar. Eyes-on for sentence-level issues. Have one other human (a friend, family member with college English, or a writing-tutor service) read at least 3 of your SOPs — they will catch what you can't.

- [ ] **Step 2: Convert each finalized SOP to PDF**

```powershell
pandoc applications\sop_variants\stanford-cs.md -o applications\per_program\stanford-cs\sop.pdf
```

Or use Word's Save As PDF. Verify font, margins, page count in the PDF (some markdown-to-PDF flows expand content unexpectedly).

- [ ] **Step 3: Verify the PDF on a different machine/device**

PDFs can render differently. Open on phone or a different OS to confirm formatting holds.

- [ ] **Step 4: Save the final PDF to the program's per_program folder**

This is your archived submission record. Do not modify after submitting.

- [ ] **Step 5: Log Task 70 in weekly journal**

Track hours per SOP. Budget: 1.5-2 hours per program × 20 programs = ~30-40 hours total. Spread across the first 2 weeks of November.

### Task 71: Recommender follow-ups — 3-week pre-deadline ping

**Artifacts:**
- Create: `outreach/recommender_followups.md`
- Modify: `outreach/recommenders.md` (status per program)

- [ ] **Step 1: Open `outreach/recommender_followups.md` with this template**

```markdown
# Recommender Follow-up Log

| Date sent | Recommender | Program | Deadline | Method | Status | Response |
|-----------|-------------|---------|----------|--------|--------|----------|
```

- [ ] **Step 2: 21 days before each program's deadline, send a personalized ping**

Template:

```
Subject: Quick reminder — [Program] LoR due [date]

Dear Prof. [Last name],

A friendly reminder that my [Program] application is due [date]. The recommendation portal should have sent you an invitation around [date you submitted in portal]. Submission method: [Interfolio / portal direct / email].

I've attached an updated CV and the SOP for this program for context, in case it's helpful. Happy to send my full program list as well.

Many thanks again for your support.

Best,
John Paul L. Gabule
```

- [ ] **Step 3: Send a full program list to each recommender once (early November)**

Some recommenders prefer to write one strong letter and submit it everywhere via Interfolio; some want to tailor per program. Match each recommender's preference.

Format the program list as a single document:

```markdown
# John Paul L. Gabule — PhD Program List, Fall 2027 cycle

| # | Program | Deadline | Submission method | Notes |
|---|---------|----------|-------------------|-------|
| 1 | Stanford CS | 2027-12-15 | Stanford portal | "Submit by email or via portal" |
...
```

Send via email; attach. Easier to action than a wall of text.

- [ ] **Step 4: Check Interfolio / portal status weekly**

For Interfolio: log in, view "deliveries" tab, check each program shows "delivered". For portal-direct: most portals show recommender status on your application dashboard.

If a recommender hasn't submitted with 14 days remaining, send a softer ping ("just confirming you got the invitation"). If 7 days remaining: send a more direct ping and CC their assistant if known.

- [ ] **Step 5: Update tracker with letter-delivery status per program**

Add a sub-column: "Letters delivered = X of N". Many trackers turn this red when X < N and < 7 days remain.

- [ ] **Step 6: Log Task 71 in weekly journal (week of 2027-11-01)**

### Task 72: Submit December 1 deadline programs

**Artifacts:**
- Modify: `applications/deadline_tracker.md` (submitted status + confirmation)
- Create: `applications/per_program/{slug}/confirmation.md` per program

- [ ] **Step 1: For each Dec 1 deadline program, complete the submission protocol 5-7 days early**

Submission protocol (apply to each program):
1. Log into the portal in Chrome (preferred — most portals are Chrome-tested). Try Firefox as backup.
2. Open every section. Verify every required field is complete.
3. Upload the final PDF SOP from `applications/per_program/{slug}/sop.pdf`. Verify it opens correctly in the portal's preview.
4. Upload CV, transcripts, any additional materials.
5. Confirm recommender slots are filled (recommender will get the invitation when you submit OR when you add them — varies by portal).
6. Pay the application fee (or apply fee waiver code).
7. Review the "ready to submit" summary page carefully — does it have your correct name? Correct program? Correct concentration?
8. Submit.
9. Screenshot the confirmation page.
10. Save the confirmation email to `applications/per_program/{slug}/confirmation.md`:

```markdown
# Submission Confirmation — [Program]

**Submitted:** 2027-11-XX HH:MM [Timezone]
**Confirmation number:** [from email]
**Fee paid:** [amount + method]
**Letters status:** [X of N delivered as of submission]
**Portal URL:** [...]

## Confirmation email
[paste full email here]

## Notes
[anything weird that happened]
```

- [ ] **Step 2: Submit early in the day (not at midnight)**

Portal failures spike near deadlines. Aim to submit by 4 PM the day before the actual deadline. If the portal fails, you have time to email admissions.

- [ ] **Step 3: Update tracker for each submitted program**

Set status = submitted; fill submitted-date and confirmation-number columns. Move row to a "submitted" section at the bottom of the tracker.

- [ ] **Step 4: Log Task 72 in weekly journal (week of 2027-11-22)**

### Task 73: One application per day target

- [ ] **Step 1: Pace submissions across November**

Goal: submit one application per business day from the second week of November onward. This:
- Spreads the cognitive load (each portal has different friction)
- Catches portal bugs earlier (if one program's portal is broken, you don't discover it on Dec 14)
- Creates a sustainable working rhythm during a high-stress month

- [ ] **Step 2: Block 2-3 hour calendar slots for submission days**

Each submission takes 90-120 minutes the first time through that particular portal. Block it. Don't try to submit between other meetings.

- [ ] **Step 3: Treat submission as a discrete deliverable**

A submitted application is the finished work product. Once it's submitted, move the row in the tracker, file the confirmation, and stop touching that application. No "let me re-read the SOP after submitting" — only invites regret.

- [ ] **Step 4: Log Task 73 in weekly journal (week of 2027-11-08, 11-15, 11-22)**

### Task 74: Track per-program submission status

**Artifacts:**
- Modify: `applications/deadline_tracker.md`

- [ ] **Step 1: Per submitted program, track these post-submit fields**

Add or verify these columns are populated in the tracker:
- Submission confirmation email received? (Y/N + date)
- Letters delivered? (X of N, with names of any not-yet-delivered)
- Fee paid / waiver applied? (Y/N + receipt #)
- Any "additional materials requested" follow-up from program? (Y/N + status)

- [ ] **Step 2: Daily 15-minute check during November**

Open each submitted program's portal once a day during the bulk submission window. Verify:
- All required fields show green / complete
- Letter delivery status hasn't regressed (sometimes Interfolio mis-syncs)
- No new emails from the admissions office

- [ ] **Step 3: Log Task 74 in weekly journal**

### Task 75: Maintain a portal-bugs / blockers log

**Artifacts:**
- Create: `applications/blockers.md`

- [ ] **Step 1: Open `applications/blockers.md`**

```markdown
# Portal & Application Blockers Log

| Date | Program | Issue | Severity | Action taken | Resolved? |
|------|---------|-------|----------|--------------|-----------|
```

- [ ] **Step 2: Log every issue as you hit it**

Common issues:
- SOP file rejected for "invalid format" despite being a valid PDF → try different PDF export, or re-save with a different tool
- File size limit hit (10 MB cap; your PDF is 12 MB) → recompress images, regenerate from source
- Recommender invitation not delivered → check spam; resend from portal; if still failing, contact admissions
- Transcript verification stuck on "pending" for >5 days → contact registrar to re-send; CC admissions
- Portal session times out mid-edit → save more frequently; some portals let you save drafts of essays separately
- Two-factor auth on portal locked out → wait 24 hr or contact program IT
- Demographic question with no opt-out → leave blank if optional; contact admissions if required and inapplicable
- Browser-specific bug (works in Chrome, not Safari) → switch browsers; test on the supported browser only

- [ ] **Step 3: For each high-severity issue, escalate quickly**

Email the program's admissions office directly. Most programs are responsive within 1-2 business days. Keep the email short, specific, factual:

```
Subject: [Program] portal issue — file upload failing

Dear [Program] Graduate Admissions,

I'm submitting an application for the PhD CS program (Fall 2028 entry).
When attempting to upload my Statement of Purpose, the portal returns:
[exact error message].

I have attempted: [browsers tried, file formats tried]. The PDF is [file size, no obvious encoding issues].

Could you advise on next steps or accept the document by email?

Best,
John Paul L. Gabule
Applicant ID: [from portal]
```

- [ ] **Step 4: Log Task 75 in weekly journal**

---

## Month 3 — December 2027: Final push + post-submission

### Task 76: Submit all December-deadline programs

**Artifacts:**
- Modify: `applications/deadline_tracker.md`
- Create: confirmation files in `applications/per_program/{slug}/`

- [ ] **Step 1: Treat each of Dec 1, Dec 8, Dec 15 as a hard mini-deadline cluster**

Three sub-pushes within December. Plan each like a separate deliverable.

- [ ] **Step 2: For the Dec 1 cluster — final submissions 2-3 days early**

For every Dec 1 deadline program not already submitted in November:
1. Apply the submission protocol from Task 72 Step 1.
2. Submit by Nov 28 at latest.
3. Triple-check the deadline timezone — some programs say "Dec 1" but mean "Dec 1 by 11:59 PM Eastern" which means Nov 30 if you're west of that zone.

- [ ] **Step 3: For the Dec 8 cluster — submit by Dec 6**

Same protocol.

- [ ] **Step 4: For the Dec 15 cluster — submit by Dec 13**

Same protocol. By this point you'll have done 12-15 submissions; the protocol should be muscle memory.

- [ ] **Step 5: M-Submit milestone retrospective**

After the Dec 15 cluster passes, append to `journal/weekly.md`:

```markdown
## M-Submit Retrospective — Dec 16, 2027
- Submitted programs: X of N total
- Remaining: list any not-yet-submitted (e.g., Jan 1 / Jan 15 deadlines)
- Recommender status: X letters delivered across all programs
- Major issues encountered: [paraphrase from blockers.md]
- Fee total to date: $X
- On track for M-Closeout (Dec 31)? [Y/N]
```

- [ ] **Step 6: Log Task 76 in weekly journal**

### Task 77: Recommender final-week monitoring

**Artifacts:**
- Modify: `outreach/recommender_followups.md`

- [ ] **Step 1: Starting 7 days before each deadline, check letter delivery DAILY**

This is the highest-leverage daily task in December. A missing letter blocks the entire application even if the rest is perfect.

- [ ] **Step 2: 48-hour rule**

If a recommender has not submitted within 48 hours of a deadline, take these steps in order:
1. Send the recommender a direct text/email ("just a quick check — the [Program] letter is due in 48 hr, please confirm submission when you can")
2. If no response in 12 hr, call the recommender's office
3. If still nothing 24 hr before deadline, email the program admissions office: "My recommender [Name, affiliation] is finalizing their letter; they expect to submit within 24 hours of the deadline. Could you confirm the program accepts letters within a 48-hour window past the deadline if needed?"
4. Most top programs allow 1-3 days of grace for letters as long as the applicant submitted on time.

- [ ] **Step 3: Backup plan — have a 4th recommender on call**

Pre-Phase 4, you should have an emergency 4th recommender briefed (Phase 3 Task 47/62). If a primary recommender goes silent, this backup can write a letter in 48 hours — not ideal, but better than missing a deadline.

- [ ] **Step 4: Log every contact in `outreach/recommender_followups.md`**

Each ping logged: date, recommender, channel, response (or no-response).

- [ ] **Step 5: Log Task 77 in weekly journal**

### Task 78: Submit any late-deadline (Jan / Feb) programs

**Artifacts:**
- Modify: `applications/deadline_tracker.md`
- Create: confirmation files for late submissions

- [ ] **Step 1: Identify Jan 1, Jan 5, Jan 15, Feb 1, Feb 15 deadline programs**

Common late-deadline targets:
- Some Europe programs (Edinburgh, Cambridge specific programs)
- Caltech (often Dec 15 actually; verify)
- A few US programs with later cycles

- [ ] **Step 2: Don't lose focus on these — but don't submit them last**

Schedule each late-deadline submission for 7+ days before its deadline. Spread them through mid-to-late December.

- [ ] **Step 3: Log late submissions in tracker + per_program folder**

### Task 79: Phase 4 closeout — archive all submitted materials

**Artifacts:**
- Move all `applications/per_program/{slug}/` to `applications/submitted/{slug}/` once submitted
- Create: `applications/submitted/_INDEX.md`

- [ ] **Step 1: After every program is submitted, archive its folder**

```powershell
Move-Item applications\per_program\* applications\submitted\
```

Verify: `applications/per_program/` is empty after archiving.

- [ ] **Step 2: Create `applications/submitted/_INDEX.md`**

```markdown
# Submitted Applications — Fall 2027 Cycle

| # | Program | Submitted | Confirmation | Letters delivered | Fee | Notes |
|---|---------|-----------|--------------|-------------------|-----|-------|
| 1 | Stanford CS | 2027-12-13 | STN-12345 | 3 of 3 | $125 | clean submit |
| ... |
```

This index becomes your single source of truth for "what did I submit, when".

- [ ] **Step 3: Verify each per-program folder has the required files**

Per program, confirm:
- `sop.pdf` (the exact PDF submitted)
- `cv.pdf` (the exact CV submitted)
- `confirmation.md` (submission record)
- `portal_notes.md` (any quirks worth remembering)

- [ ] **Step 4: Log Task 79 in weekly journal**

### Task 80: Prepare for interview season (Jan-Mar 2028)

**Artifacts:**
- Create: `interviews/prep.md`
- Create: `interviews/per_program_qa.md`

- [ ] **Step 1: Build the interview prep workbook in `interviews/prep.md`**

```markdown
# PhD Interview Preparation

## Universal questions
For each, draft a 60-90 second spoken answer. Practice aloud.

1. "Walk me through your research so far."
2. "Why do you want to do a PhD?"
3. "Why this program specifically?"
4. "Who would you want to work with here, and why?"
5. "Tell me about a research setback and what you learned."
6. "Where do you see your research in 5 years?"
7. "Do you have questions for me?" (have 3-5 substantive questions ready)

## Research-vision pitch (2 minutes)
[Draft a 2-minute spoken version of your problem statement. Memorize the structure, not the words.]

## CiteCheck pitch (90 seconds)
[Specifically how to talk about the workshop paper, what worked, what's next.]

## Technical drill list
- Be able to explain your method end-to-end at the whiteboard / over Zoom screen-share
- Be ready to defend choices: dataset, baseline, metric
- Be ready to take a critique: "what if your evaluation has X bias?"

## Logistics
- Test Zoom + webcam + microphone + lighting + background
- Test screen-share with your slides if applicable
- Quiet room, stable internet
```

- [ ] **Step 2: Build per-program Q&A in `interviews/per_program_qa.md`**

For each of your top-8 programs (the ones most likely to interview), draft:
- 3 questions specific to that program
- 2 questions specific to the advisor(s) you'd want to work with
- A short paragraph: "why this program over the others I applied to" (do not say "ranking")

- [ ] **Step 3: Mock interview**

Find a friend, mentor, or current PhD student. Do at least one 30-minute mock interview before the end of December. Audio-record it; listen back the next day.

- [ ] **Step 4: Calendar — block interview windows**

Mark Jan 15 – Mar 15 2028 as high-availability. Top US programs interview in this window; some give 3-7 days notice. Don't be on vacation without internet during this window.

- [ ] **Step 5: Log Task 80 in weekly journal**

### Task 81: Handle workshop paper acceptance + applications update

**Artifacts:**
- Update: SOPs and CV (mid-cycle update) if workshop accepted
- Create: `publications/citecheck_workshop/final_camera_ready.pdf` (if accepted)

- [ ] **Step 1: If NLLP @ EMNLP 2027 accepts the paper (notification typically Oct-Nov)**

Camera-ready deadline is typically 2-3 weeks after notification. Tasks:
- Address reviewer feedback in the paper
- Update to the workshop's camera-ready template
- Submit camera-ready by deadline
- Register for the workshop (separate fee, usually $50-200; budget for this)
- Prepare poster or short talk (workshop format varies)

- [ ] **Step 2: Mid-cycle SOP update — if there's still time**

If acceptance is received before any program's deadline, you may add a 1-2 sentence reference to the acceptance in the SOPs not yet submitted. Be honest about timeline — "accepted at NLLP @ EMNLP 2027" is fine; "published" is not (camera-ready usually means in proceedings, but check the workshop's terminology).

For applications already submitted before notification: most programs allow a brief update email to the admissions office or via the portal ("update materials" or "supplemental" form). Send a 2-3 sentence update with the acceptance noted; do not resubmit the entire SOP unless invited.

- [ ] **Step 3: Update CV permanently**

Add the workshop paper acceptance to your CV in the Publications section. This is the standing version for interviews.

- [ ] **Step 4: Update arXiv preprint to the camera-ready version**

If you have time, update the arXiv preprint to match the camera-ready (with a note that this version was published at NLLP @ EMNLP 2027).

- [ ] **Step 5: Log Task 81 in weekly journal**

### Task 82: M-Closeout — 18-month plan retrospective

**Artifacts:**
- Create: `journal/phase4_retro.md`
- Modify: `journal/weekly.md` (final Phase 4 entry)
- Modify: `journal/decisions.md` (closeout entry)

- [ ] **Step 1: Write the 18-month retrospective in `journal/phase4_retro.md`**

```markdown
# 18-Month PhD Prep — Retrospective
**Period:** Jun 2026 – Dec 2027
**Author:** John Paul L. Gabule
**Date:** 2027-12-31

## Outcomes
- Programs applied to: X
- Fellowships applied to: X (NSF GRFP, Hertz, OpenAI Fellows, Google PhD, ...)
- Workshop paper outcome: [accepted / rejected / pending]
- arXiv preprints live: [count + titles]
- Total artifacts produced: [reading list, problem statement, baseline reproductions, SOPs, ...]

## What worked
- [3-5 bullets — concrete things that paid off]

## What didn't work
- [3-5 bullets — honest. Did you over-invest in any phase? Under-invest in any?]

## Per-phase reflection
### Phase 1 (Foundation, Jun-Aug 2026)
- What I'd do differently:
### Phase 2 (Build, Sep 2026 – Apr 2027)
- What I'd do differently:
### Phase 3 (Submit research / prep apps, May-Sep 2027)
- What I'd do differently:
### Phase 4 (Application push, Oct-Dec 2027)
- What I'd do differently:

## Hours invested
- Phase 1: [hours]
- Phase 2: [hours]
- Phase 3: [hours]
- Phase 4: [hours]
- TOTAL: [hours]

## Cost of preparation
- Software/services: $...
- Conferences/travel: $...
- Application fees + transcripts + GRE: $...
- TOTAL: $...

## If admissions asks about my prep process
[2-3 paragraphs you could use as a polished answer in an interview: "I spent 18 months systematically preparing — here's the structure and what I learned."]

## Open questions going into interview season
- [Things you're genuinely unsure about — what will you ask interviewers?]

## Next session — Spring 2028
- Interview prep continues (Task 80)
- Visit days (March-April)
- Decision-making (by April 15 in US per the CGS deal)
- If admitted: secure funding, choose advisor, begin onboarding
- If not admitted: re-apply plan or alternative-path plan
```

- [ ] **Step 2: Log closeout in `journal/decisions.md`**

```markdown
| 2027-12-31 | Phase 4 complete: all applications submitted, 18-month plan retrospective written | Plan execution finished; transition to interview/decision phase | N/A — end of planned period |
```

- [ ] **Step 3: Final weekly journal entry**

```markdown
## Phase 4 Closeout — Week of 2027-12-27
- Phase 4 status: COMPLETE
- Total applications submitted: X
- Total weeks elapsed across all phases: 84
- Energy / confidence: [1-10]
- Now waiting for: interview invitations (Jan-Mar 2028), decisions (Feb-Apr 2028)
```

- [ ] **Step 4: Take a real break before interview season**

Genuinely: 5-7 days completely off after Dec 31. Interview season is its own marathon. You need the reset.

---

## Verification Checklist (run at end of Phase 4)

Before declaring Phase 4 complete, confirm the following exist with content:

- [ ] `applications/deadline_tracker.md` has rows for all 15-25 programs with submitted status
- [ ] `applications/submitted/_INDEX.md` lists every submitted application with confirmation numbers
- [ ] Every program in the index has: `sop.pdf`, `cv.pdf`, `confirmation.md` in its folder
- [ ] `applications/fee_budget.md` shows actual final spend (within $3,500 budget)
- [ ] `applications/blockers.md` documents every portal issue encountered (and resolution)
- [ ] `outreach/recommender_followups.md` shows letter delivery for every program
- [ ] `outreach/recommenders.md` shows each recommender's coverage of programs
- [ ] `publications/citecheck_workshop/` has either camera-ready PDF (if accepted) or review-response notes (if rejected)
- [ ] `interviews/prep.md` is filled out with universal questions + practiced research pitch
- [ ] `interviews/per_program_qa.md` has top-8 programs covered
- [ ] `journal/phase4_retro.md` exists and is filled in (no placeholders)
- [ ] `journal/weekly.md` has weekly entries for all 13 weeks of Phase 4
- [ ] `journal/decisions.md` has Phase 4 entries
- [ ] At least one mock interview completed
- [ ] Calendar blocked for Jan 15 – Mar 15 2028 interview availability
- [ ] All NSF GRFP / Hertz / industry fellowship submissions archived under `applications/fellowships/`

---

## Phase 4 Risk Register

These are the known risks to the application push. Each has a mitigation; track in `applications/blockers.md` if any materialize.

| Risk | Severity | Mitigation |
|---|---|---|
| Recommender misses deadline | High | T-21/T-7/T-2 reminders + backup recommender on call + 48hr admissions escalation |
| Portal browser/file-format bug at submit | High | Submit 3+ days early; have Chrome + Firefox tested; PDFs validated on second device |
| Official transcript stuck at registrar | Medium | Order by mid-October; confirm degree-conferral date is visible |
| Fee waiver window closes before applied | Medium | Apply for all waivers in first week of October |
| Workshop paper rejected near deadline | Low-Medium | arXiv preprint provides citable artifact; don't lean on workshop acceptance |
| Workshop paper accepted but camera-ready conflicts with app deadlines | Medium | Reserve a buffer week in late Nov for camera-ready work |
| Calendar/timezone confusion on deadline | High | All tracker deadlines stored in UTC + local; submit 24+ hours early |
| Credit card declined at submit | Low | Confirm $3K+ headroom; have backup card |
| Last-minute SOP edit introduces error | Medium | Submit and stop editing; no post-submission re-reads |
| Interview invitation arrives during submission rush | Medium | Quick-reply same day; schedule for after final submission |

---
