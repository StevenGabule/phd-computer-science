# PhD Prep — Phase 3 (Publish & Apply) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Across May 2027 – Sep 2027, finish remaining CiteCheck experiments, draft and submit the CiteCheck workshop paper (NLLP @ EMNLP 2027 primary, TrustNLP @ EMNLP 2027 backup) with an arXiv preprint, and bring application materials from "v1 SOP draft + advisor longlist" to "locked program list + per-program tailored SOPs + briefed recommenders" ready to fire in the Oct–Dec 2027 application push (Phase 4).

**Architecture:** Phase 3 runs two parallel tracks over five months. **Track R (Research)** closes out M5 (May), drafts the paper (M6, Jul), and submits + preprints (M7, Sep). **Track A (Applications)** identifies recommenders (May), prepares and sends rec packets (Jun–Jul), refines the SOP narrative core with actual CiteCheck artifacts (Jul), locks the final program list and tailors per-program SOP variants (Aug–Sep), and sends reconfirmation packets to recommenders 4 weeks before the earliest deadline. Each month ends with a journal entry that scores both tracks against the milestone, and Month 5 ends with a Phase 3 closeout retrospective that hands Phase 4 a clean run-list of 15–25 programs with dates, fees, and submission methods.

**Tech Stack:**
- *Research:* LaTeX via Overleaf (ACL/EMNLP 2027 template — `acl2023.sty` family, updated for the 2027 cycle), BibTeX (export from Zotero), `wandb` plot exports + `matplotlib` polish for camera-ready figures, `git tag` + GitHub Releases for code release, Hugging Face Hub for model + dataset cards, arXiv (cs.CL primary, cs.IR secondary) for the preprint, OpenReview / Softconf for workshop submission portal.
- *Applications:* Google Docs (per-program SOP variants — one Doc per program, suffix `_v{N}.docx`) or Notion (database view if preferred), Google Sheets for the program/deadline tracker (columns: program, deadline, fee, fee-waiver eligibility, GRE required, submission method, recommender method, status), Interfolio Dossier ($48/yr) for letters that need to be sent to multiple programs from the same letter, ETS GRE registration if any program requires (~$220 fee, allow 4-week scheduling lead time), Gmail templates / Boomerang for recommender follow-ups, Adobe Acrobat or pandoc for SOP PDF conversion.

---

## File Structure

All paths relative to `C:\Users\John Paul L. Gabule\Desktop\phd-computer-science`. Phase 3 extends the Phase 2 tree:

```
citecheck/
  paper/
    outline.md                      # carried in from Phase 2
    citecheck.tex                   # main paper file (Task 44)
    sections/
      00_abstract.tex
      01_introduction.tex
      02_related.tex
      03_benchmark.tex
      04_method.tex
      05_experiments.tex
      06_discussion.tex
      07_conclusion.tex
      appendix.tex
    figures/                        # carried in from Phase 2; finalized in Task 42
      fig01_system_diagram.pdf
      fig02_reranker_loss.pdf
      fig03_calibration.pdf
      fig04_per_jurisdiction.pdf
      fig05_ablation_bars.pdf
      fig06_qualitative_retraction.pdf
    tables/
      tab01_benchmark_stats.tex
      tab02_main_results.tex
      tab03_ablations.tex
      tab04_human_audit.tex
      tab05_seed_stability.tex
      tab06_per_task.tex
      tab07_per_jurisdiction.tex
      tab08_error_modes.tex
    references.bib
    reviews/
      internal_pass1_claude.md      # Task 49
      internal_pass2_external.md    # Task 50
      reviewer_responses.md         # Task 59
  release/
    README_release.md               # camera-ready repo README
    LICENSE                         # MIT or Apache-2.0
    requirements.txt                # frozen deps
    reproduce.sh / reproduce.ps1    # one-shot reproduction script
    model_card.md                   # HF model card
    dataset_card.md                 # HF dataset card
applications/
  sop_narrative_skeleton.md         # Phase 2 artifact; refined in Task 51
  artifacts_strategy.md             # NEW — Task 43 step 0 backfills this
  programs_final.md                 # locked Sep 2027 list (Task 60)
  deadlines_tracker.xlsx            # Google Sheets export (Task 60)
  sops/
    {program-slug}.md               # one per locked program (Task 61)
    {program-slug}.pdf              # PDF export per program (Task 61)
  recommenders/
    recommender_shortlist.md        # Task 43
    rec_packet_template.md          # Task 46
    packets/
      {recommender-slug}.pdf        # one per recommender (Task 46)
    asks/
      {recommender-slug}_ask.md     # email draft per recommender (Task 43)
    followups/
      {recommender-slug}_followup_sep.md  # Task 62
    log.md                          # one row per recommender per event
  gre/
    program_gre_requirements.md     # per-program GRE policy as of 2027 cycle
    score_report.pdf                # if Task 57 fires
journal/
  weekly.md                         # continues from Phase 2
  decisions.md                      # continues from Phase 2
  phase3_retros.md                  # M5-final, M6, M7 retrospectives + Phase 3 closeout
```

---

## Pre-work — Week 0 (week of 2027-05-03)

This is a half-week kickoff: confirm Phase 2 closeout, read the M5-partial retrospective, and stand up the Phase 3 directory tree.

- [ ] **Step 1: Confirm Phase 2 verification checklist is fully ticked**

Re-read `docs/superpowers/plans/2026-05-24-phd-prep-phase-2-build.md` Verification Checklist. Any unticked item that blocks Phase 3 must be resolved in Task 40 (it's the catch-up task).

- [ ] **Step 2: Create the Phase 3 directory extensions**

```powershell
New-Item -ItemType Directory -Force `
  citecheck\paper\sections, citecheck\paper\tables, citecheck\paper\reviews, `
  citecheck\release, `
  applications\sops, applications\recommenders\packets, `
  applications\recommenders\asks, applications\recommenders\followups, `
  applications\gre | Out-Null
```

Verify: `Test-Path citecheck\paper\sections, citecheck\release, applications\sops` all return `True`.

- [ ] **Step 3: Create `journal/phase3_retros.md` with section headers**

Headers: `## M5-Final Retrospective — End of May 2027`, `## M6 Retrospective — End of Jul 2027`, `## M7 Retrospective — End of Sep 2027`, `## Phase 3 Closeout — Week of 2027-09-27`.

- [ ] **Step 4: Log Week 0 in `journal/weekly.md` (week of 2027-05-03)**

```markdown
## Week of 2027-05-03 — Phase 3 kickoff
- Went well: Phase 2 closed; Phase 3 tree provisioned.
- Stalled:
- Adjustment:
- Hours: 3
```

---

## Month 1 — May 2027: M5 finish (Research) + recommender identification (Applications)

### Task 40: Run remaining stability / robustness experiments carried over from Phase 2 Task 36

**Artifacts:**
- Modify: `citecheck/experiments/seeds/2027-04/results.json` (extend with any missing seeds / backbone)
- Create: `citecheck/experiments/seeds/2027-05-stability/results.json`

- [ ] **Step 1: Open the Phase 2 M5-partial retrospective and list what stability checks were deferred**

Phase 2 Task 36 explicitly flagged that if the 72 GPU-hour seed sweep blew the April budget, seeds 2 and 3 could be downsampled to 200 items, and the secondary-backbone swap (Qwen2.5-7B-Instruct) could be skipped. List everything skipped here.

- [ ] **Step 2: Restore the deferred work in priority order**

Priority order: (a) full-eval-set seeds for CiteCheck and the 2 strongest baselines (≥3 seeds × ≥500 items each), (b) Qwen2.5-7B-Instruct backbone swap for CiteCheck only, (c) constrained-decoding-grammar robustness check (vary the grammar permissiveness ±10%, confirm CRR / FabR move monotonically).

Compute: budget ~30 GPU-hours for this task. If (a) alone consumes the budget, log (b) and (c) as Phase 4 wishlist items rather than dragging Phase 3.

- [ ] **Step 3: Re-run NLI judge over any new outputs**

Use the same DeBERTa-v3-large-mnli judge from Phase 2 Task 35 so Citation Support F1 numbers are comparable.

- [ ] **Step 4: Update the master results table (`citecheck/experiments/runs/2027-03-full-eval/results.json`) with the augmented numbers**

If headline numbers shift by more than 1 percentage point on CRR or FabR after the full seed sweep, this is a *finding*: report mean ± std prominently and de-emphasize point estimates in the abstract.

- [ ] **Step 5: Risk check — if a seed run reveals CiteCheck's lead over the best baseline is within 1 std**

This is the riskiest finding of Phase 3: a method that looked decisive in March 2027 may look noisy in May. If it happens, do not hide it. Log the finding in `journal/decisions.md` and re-frame the paper contribution toward the *benchmark and analysis* (which stands on its own) rather than the *method as state-of-the-art* (which would need more work).

- [ ] **Step 6: Log Task 40 in `journal/weekly.md` (week of 2027-05-10)**

### Task 41: Finalize all results tables, ablation tables, error-mode tables

**Artifacts:**
- Create: `citecheck/paper/tables/tab01_benchmark_stats.tex` through `tab08_error_modes.tex`
- Create: `citecheck/experiments/runs/2027-05-error-modes/results.json`

- [ ] **Step 1: Build the 8 LaTeX tables**

Source data is the JSON in `citecheck/experiments/runs/` and `citecheck/experiments/ablations/`. Use a small Python script (`scripts/build_tables.py`) that reads each JSON and emits a `\begin{tabular}` block with booktabs styling. One file per table.

- [ ] **Step 2: Implement the error-mode analysis (was a Phase 2 plan item, deferred to here)**

For every (method, question) pair where CiteCheck outperforms baseline, classify the baseline's failure: (i) cite-does-not-exist (FabR), (ii) cite-exists-but-no-support, (iii) cite-from-wrong-jurisdiction, (iv) refused-to-answer-but-was-answerable. Build `tab08_error_modes.tex` as a stacked bar / matrix table showing the distribution per baseline.

- [ ] **Step 3: Sanity-check each table renders standalone**

Compile a one-page `.tex` per table: `pdflatex tab02_main_results.tex` (after wrapping in `\documentclass{standalone}` plus booktabs preamble). Confirm rows align and decimals are consistent (3 dp for percentages, 2 dp for kappa).

- [ ] **Step 4: Compute statistical-significance markers**

For Table 2 (main results), run paired bootstrap (10,000 resamples) between CiteCheck and each baseline on the headline metric (CSF1 via human audit). Mark cells with `^{\dagger}` (p<0.05) or `^{\ddagger}` (p<0.01). Bootstrapping code goes in `citecheck/eval/significance.py`.

- [ ] **Step 5: Log Task 41 in `journal/weekly.md` (week of 2027-05-17)**

### Task 42: Generate final paper figures

**Artifacts:**
- Create / Modify: `citecheck/paper/figures/fig01` through `fig06` (PDF, vector)

- [ ] **Step 1: Figure 1 — System diagram (3 stages)**

Draw in `draw.io` (free) or `tikz` directly. Three boxes: hybrid retrieval → faithfulness-tuned rerank → constrained generation + verify loop. Export to PDF.

- [ ] **Step 2: Figure 2 — Reranker loss curves**

From `wandb` runs of Phase 2 Task 30 (the λ sweep over {0.1, 0.3, 0.5, 1.0}). Use `wandb` API to download per-step loss arrays, replot in matplotlib with consistent academic styling (`seaborn-paper`, font_scale=1.2). Export PDF.

- [ ] **Step 3: Figure 3 — Calibration plot**

For CiteCheck and best baseline, plot predicted confidence (mean token probability of cited spans) vs. realized Citation Support rate, binned in deciles. Calibration is a common reviewer ask; producing it now pre-empts a major revision.

- [ ] **Step 4: Figure 4 — Per-jurisdiction breakdown bar chart**

Bars per (jurisdiction = SCOTUS / federal circuits / state) × (CiteCheck vs best baseline) showing CSF1. Use the slices from Phase 2 Task 37.

- [ ] **Step 5: Figure 5 — Ablation bar chart**

One bar per ablation config (A0–A7 from Phase 2 Task 34), height = headline metric, colored by component category (retrieval / rerank / agent / decoding).

- [ ] **Step 6: Figure 6 — Qualitative retraction example**

One annotated screenshot/table showing: question → baseline output (fabricated cite, highlighted red) → CiteCheck iteration 1 (bad cite retracted, highlighted yellow) → CiteCheck iteration 2 (valid cite resolved, highlighted green). Build as a TikZ figure for crisp rendering.

- [ ] **Step 7: All figures must be vector PDF (no rasters) and pass colorblind check**

Run each through `oklch-color-blindness` check or use `colorbrewer` palettes (Tol's "muted" 6-color scheme is safest). Avoid red/green pairs — use red/blue or orange/blue.

- [ ] **Step 8: Log Task 42 in `journal/weekly.md` (week of 2027-05-24)**

### Task 43: Application — identify 3-4 specific recommenders; draft "ask" emails

**Artifacts:**
- Create: `applications/artifacts_strategy.md` (gap backfill — referenced by `sop_narrative_skeleton.md` but never created in Phase 2)
- Create: `applications/recommenders/recommender_shortlist.md`
- Create: `applications/recommenders/asks/{recommender-slug}_ask.md` (3–4 files)

- [ ] **Step 0: Backfill `applications/artifacts_strategy.md`**

The SOP skeleton (`applications/sop_narrative_skeleton.md`, paragraph 4) references `[INSERT SPECIFIC ACCOMPLISHMENTS]` and cross-references an `artifacts_strategy.md` that Phase 2 never produced. Create it now:

```markdown
# Artifacts Strategy — Application-Ready Evidence (May 2027)

| Artifact | Source (Phase 1/2 task) | SOP paragraph | LinkedIn / blog post slot | GitHub release |
|----------|-------------------------|---------------|---------------------------|----------------|
| 500-item CiteCheck benchmark | Phase 2 Tasks 24-26 | P3 | yes — dataset card link | yes (Task 54) |
| Faithfulness-tuned reranker | Phase 2 Task 30 | P3 | yes — model card link | yes (Task 54) |
| End-to-end agentic pipeline | Phase 2 Task 31 | P3 | yes — short demo video | yes (Task 54) |
| Per-jurisdiction analysis | Phase 2 Task 37 / Phase 3 Task 41 | P3 | yes — blog post | repo notebook |
| arXiv preprint | Phase 3 Task 56 | P4 + P3 | yes — main link | n/a |
| Workshop acceptance (if it lands) | Phase 3 Task 59 | P4 | yes — announcement | n/a |
```

- [ ] **Step 1: Draw the recommender shortlist from Phase 1 outreach**

Open `outreach/advisors.md` and `outreach/log.md`. Candidates fall in three buckets:
1. **Academic recommenders who already engaged** — anyone who responded to the Phase 1 Task 13 cold emails or Phase 2 outreach. These are gold.
2. **Master's program supervisors** — your thesis advisor and one other Master's professor who saw your work closely.
3. **Industry / open-source collaborators** — only if they hold a PhD and can speak to research aptitude (e.g., a research scientist mentor at an internship).

Target: 4 recommenders (most US programs require 3; having 4 lets you tailor — e.g., a law-tech recommender for Stanford RegLab, an NLP recommender for CMU LTI).

- [ ] **Step 2: Score each candidate against criteria**

Criteria: (a) holds a PhD or equivalent research credential, (b) has worked with you in the last 4 years, (c) can write specifics (not just "John is hardworking"), (d) responds to email reliably. Reject anyone failing (a), (b), or (d). Tolerate (c) only if you can compensate by providing an extremely detailed rec packet.

- [ ] **Step 3: Write `applications/recommenders/recommender_shortlist.md`**

```markdown
# Recommender Shortlist — Phase 3

| Slug | Name | Affiliation | Relationship | Holds PhD? | Last contact | Status |
|------|------|-------------|--------------|------------|--------------|--------|
| smith-jane | Prof. Jane Smith | XYZ Univ | Master's thesis advisor | Y | 2027-04 | confirmed willing |
| ...
```

- [ ] **Step 4: Draft an "ask" email per recommender**

Template:

```
Subject: Letter of recommendation for PhD applications, Fall 2027

Dear Prof. [Last name],

I'm applying to ~15–20 US PhD programs in CS / NLP for Fall 2028 entry, with
deadlines clustered Dec 1, 2027 – Jan 8, 2028. I'm writing to ask whether you
would be willing to write a letter of recommendation for me.

Quick context: my research direction is CiteCheck — an open benchmark and
agentic-RAG method for verifiable US case-law citations. I'll have an arXiv
preprint by ~Aug 2027 and a workshop submission to NLLP @ EMNLP 2027.

If you're willing, I'll send a rec packet (CV, current SOP draft, list of
programs with deadlines and submission methods, your 1-page accomplishments
summary that you can pull from) by [date 6 weeks before earliest deadline].

I understand if you'd prefer to decline — I'd rather know now than find out
in November. A one-line response is plenty.

Thank you for considering it.

Sincerely,
John Paul L. Gabule
```

Per-recommender customization: 1–2 sentences referencing specific work you did together.

- [ ] **Step 5: Send all 3–4 ask emails by 2027-05-31**

Log in `applications/recommenders/log.md` (one row per email: date, recipient, subject, status).

RISK: a recommender declines. Mitigation: have a 5th candidate ready in `recommender_shortlist.md` marked `backup`.

- [ ] **Step 6: M5-final journal entry (week of 2027-05-31)**

```markdown
## M5-Final Retrospective — End of May 2027

- Stability checks: [completed list]
- Tables: 8 of 8 built and rendering
- Figures: 6 of 6 vector PDFs in `citecheck/paper/figures/`
- Recommenders: [N] asked, [N] confirmed, [N] declined, [N] pending
- Headline numbers (post-stability):
  - CRR (CiteCheck vs best baseline): X% vs Y%
  - FabR: X% vs Y%
  - CSF1 (human): X vs Y
- Total GPU-hours in May: [N]
- Phase 3 confidence (1–10): [N]
- Anything that should slip into Jun: [...]
```

Append a decision-log entry: `| 2027-05-31 | M5 finalized; CiteCheck results locked for paper drafting | Stability and error-mode analysis complete; results table frozen | Reversible only via re-running experiments |`.

---

## Month 2 — June 2027: Paper outline → draft v0 + rec packet prep

### Task 44: Convert Phase 2 paper outline into a full LaTeX skeleton

**Artifacts:**
- Create: `citecheck/paper/citecheck.tex`
- Create: `citecheck/paper/sections/*.tex` (8 stub files)
- Create: `citecheck/paper/references.bib`

- [ ] **Step 1: Create the Overleaf project (or local LaTeX project)**

Open https://www.overleaf.com/ → New Project → Templates → search "ACL 2023" or "EMNLP". Use the most recent ACL template (the 2023 template family is the basis for 2026/2027 — `acl2023.sty`). If the 2027 venue posts a venue-specific template before submission, swap to it then.

If you prefer local: clone `git clone https://github.com/acl-org/acl-style-files.git` into `citecheck/paper/style/`.

- [ ] **Step 2: Set up `citecheck.tex` with the section includes**

```latex
\documentclass[11pt]{article}
\usepackage[]{acl}
\usepackage{times}
\usepackage{latexsym}
\usepackage{booktabs}
\usepackage{graphicx}
\usepackage{microtype}
\usepackage{inconsolata}

\title{CiteCheck: An Open Benchmark and Agentic-RAG Method for Verifiable US Case-Law Citations}
\author{John Paul L. Gabule \\ [affiliation] \\ \texttt{johnpaullimgabule@gmail.com}}

\begin{document}
\maketitle
\input{sections/00_abstract}
\input{sections/01_introduction}
\input{sections/02_related}
\input{sections/03_benchmark}
\input{sections/04_method}
\input{sections/05_experiments}
\input{sections/06_discussion}
\input{sections/07_conclusion}
\bibliographystyle{acl_natbib}
\bibliography{references}
\appendix
\input{sections/appendix}
\end{document}
```

- [ ] **Step 3: Stub each `sections/*.tex` with the outline bullets from Phase 2 Task 38**

Each section file gets a `\section{...}` header plus 3–6 bullet comments that capture the outline points. No prose yet.

- [ ] **Step 4: Build `references.bib` by exporting from Zotero**

In Zotero, select the "PhD Prep — Legal RAG" collection → right-click → Export Collection → Format: BibTeX → save as `references.bib`. Quick-check that key entries (Magesh 2025, Pipitone & Houir Alami 2024, Wankhade 2026, Asai 2024, Yan 2024, Maynez 2020, the Charlotin tracker note) exist. Add any missing ones by hand.

- [ ] **Step 5: Compile the skeleton to confirm it renders**

`pdflatex citecheck.tex && bibtex citecheck && pdflatex citecheck.tex && pdflatex citecheck.tex`. The PDF should produce a near-empty document with section headings only.

- [ ] **Step 6: Log Task 44 in `journal/weekly.md` (week of 2027-06-07)**

### Task 45: Write Methods + Results + Ablations sections first

**Artifacts:**
- Modify: `citecheck/paper/sections/04_method.tex`
- Modify: `citecheck/paper/sections/05_experiments.tex`
- Modify: `citecheck/paper/sections/03_benchmark.tex` (partial — the construction subsection)

- [ ] **Step 1: Methods section (~1500 words)**

Cover: the 3-stage pipeline architecture (with a forward-reference to Figure 1); the faithfulness-tuned reranker objective $L = L_{\text{rel}} + \lambda L_{\text{ground}}$ with the 5 structure features from Phase 2 Task 27; the citation grammar; the verify loop with $k=3$ iterations. Every method claim must cite an artifact (a script, a config file, a hyperparameter) that someone could reproduce.

- [ ] **Step 2: Experiments section (~1800 words)**

Subsections: setup (baselines list, hardware, training cost), main results (Table 2 narrative), ablations (Table 3 narrative — *one paragraph per ablation row*, highlighting which removal hurts most), human audit (Table 4), stability (Table 5), per-task and per-jurisdiction (Tables 6 + 7), error modes (Table 8).

For each table, write a "what this number means" paragraph rather than just describing the number. Reviewers reward analysis over description.

- [ ] **Step 3: Benchmark construction subsection of Section 3 (~600 words)**

Cover: source distribution (200 CAP / 150 CUAD / 100 LegalBench-RAG / 50 adversarial — defer the rest of Section 3 to Task 48 once Intro frames it). Include the inter-annotator agreement number (Cohen's kappa from Phase 2 Task 26 Step 4).

- [ ] **Step 4: Cross-link figures and tables**

Every table and figure must be `\ref`d at least once in body text. Use `\autoref{tab:main_results}` etc. (requires `hyperref` preamble — add if not already).

- [ ] **Step 5: Pass 1 self-review — read aloud**

Reading aloud surfaces clunky sentences. Spend 1 hour reading Sections 4 + 5 aloud. Tag every sentence you stumble over with `% TODO: rephrase`.

- [ ] **Step 6: Log Task 45 in `journal/weekly.md` (week of 2027-06-14 + 2027-06-21 — this is 2 weeks of focused writing)**

RISK: writing Methods + Results often surfaces missing experiments or unclear definitions. Allocate ≥3 GPU-hours of slack for "I need one more number" runs. If you find a real gap (e.g., no significance test), pull it into Task 41.

### Task 46: Application — prepare the rec packet for each recommender

**Artifacts:**
- Create: `applications/recommenders/rec_packet_template.md`
- Create: `applications/recommenders/packets/{recommender-slug}.pdf` (one per confirmed recommender)
- Create: `applications/programs_draft.md` (interim file; finalized in Task 60)

- [ ] **Step 1: Build the rec packet template**

```markdown
# Recommendation Packet — John Paul L. Gabule, Fall 2027 PhD applications

## 1. About me (1 paragraph)
[3–5 sentences capturing your research direction, current role, and what you'd like the letter to emphasize.]

## 2. CV (attached, 2 pages)
[PDF attachment]

## 3. Current SOP draft (attached)
[`applications/sop_narrative_skeleton.md` exported to PDF; per-program tailoring is later, but the recommender benefits from the v1 narrative core.]

## 4. Programs (table)
| Program | Deadline | Submission method | Portal URL |
|---------|----------|-------------------|------------|
| Stanford CS | 2027-12-08 | School portal — they email you | https://... |
| ...

## 5. Accomplishments and specifics to draw on (1 page)
- Master's thesis: [title + 2-sentence summary + 1 specific technical result]
- CiteCheck project (2026–): [list 3–4 concrete artifacts — arXiv preprint, benchmark release, etc.]
- Coursework relevant: [list 4–6 advanced courses with specific projects]
- Open-source / community: [contributions, reading-group participation, blog]
- Things you've directly observed me do (one paragraph the recommender can adapt verbatim)

## 6. Logistics
- Deadlines I want letters submitted by: [first deadline minus 5 business days]
- If a program uses Interfolio: my Dossier ID is [...]
- For programs that email a link directly: please reply to me when you've submitted, even one-word "done" is enough
```

- [ ] **Step 2: Fill the template per recommender — personalization is paragraph 1 and section 5**

For each confirmed recommender, produce a customized version. Don't send identical packets — the section-5 specifics should reflect what *that* recommender saw of your work.

- [ ] **Step 3: Convert each packet to PDF**

`pandoc applications/recommenders/packets/{slug}.md -o applications/recommenders/packets/{slug}.pdf --pdf-engine=xelatex`. Verify the table renders.

- [ ] **Step 4: Build `applications/programs_draft.md`**

Start from `outreach/programs.md` (Phase 1 Task 11). For each program, fill: deadline (verify by visiting the program's PhD admissions page — never trust last year's date), application fee, fee-waiver eligibility, GRE policy ("not required" / "optional" / "required"), submission method for letters (Interfolio, direct email, school portal). One row per program. ~15–25 rows.

If a program's PhD admissions page is not yet updated for the 2027–28 cycle (common in June), mark `deadline: TBD (from 2026 cycle: <date>)` and revisit in August.

- [ ] **Step 5: Log Task 46 in `journal/weekly.md` (week of 2027-06-28)**

### Task 47: Send recommender asks and rec packets with 6-week lead time

**Artifacts:**
- Modify: `applications/recommenders/log.md`
- Send: emails (3–4)

- [ ] **Step 1: Confirm timing math**

Target: rec packet in recommenders' hands by Aug 1, 2027 — about 4 months before Dec 1 deadlines. The spec says 6 weeks lead time; we err generous because (a) summer travel, (b) some recommenders work multiple cycles and queue letters. If your earliest deadline is Nov 15 (a few US programs and some UK programs), pull this to Jul 1.

- [ ] **Step 2: Write the cover email**

```
Subject: Your rec letter packet for my Fall 2027 PhD applications

Dear Prof. [Last name],

Thank you again for agreeing to write. Attached is the full packet:
- 2-page CV
- Current SOP draft (~1100 words; per-program tailoring is in progress, but
  the research narrative is stable)
- Table of 17 programs I am targeting, with deadlines and how the letter
  reaches each one (most use a school portal that will email you a link
  in November)
- A one-page "specifics to draw on" sheet — concrete things you've seen me
  do, that you can use, edit, or ignore

Most deadlines cluster Dec 1, 2027 – Jan 8, 2028. The earliest is [date].
I'll send a reminder ~4 weeks before that with the final program list and
any portal links I've received by then.

If anything is missing or unclear, please tell me — I'd rather fix it now.

Sincerely,
John Paul L. Gabule
```

- [ ] **Step 3: Send all packets**

Log in `applications/recommenders/log.md` (one row per send: date, recipient, packet version, status).

- [ ] **Step 4: Set a calendar reminder for the 4-week follow-up**

Use Google Calendar (or `mcp__claude_ai_Google_Calendar__create_event`): event titled "Recommender follow-up wave 1" on the date that is earliest-deadline minus 4 weeks (around Nov 1, 2027 for Dec 1 deadlines).

- [ ] **Step 5: Risk register**

| Risk | Mitigation |
|------|------------|
| Recommender goes silent in summer | The Aug 1 send leaves 4 months; send a polite June nudge if no response by Jun 30 |
| Recommender wants to write a single letter to be uploaded everywhere | Confirm Interfolio Dossier ID is in section 6 of the packet |
| Program adds a 4th letter requirement | This is rare; if discovered in August (Task 60), add a 5th recommender from the `backup` slot |

- [ ] **Step 6: Log Task 47 + Jun weekly reflection in `journal/weekly.md` (week of 2027-06-28)**

End-of-June journal entry: M6 is mid-July; how much paper drafting got done in Jun vs. how much carries to Jul; recommender response rate so far.

---

## Month 3 — July 2027: M6 paper draft v1 + SOP refinement

### Task 48: Write Introduction + Related Work + Discussion + Limitations sections

**Artifacts:**
- Modify: `citecheck/paper/sections/01_introduction.tex`
- Modify: `citecheck/paper/sections/02_related.tex`
- Modify: `citecheck/paper/sections/03_benchmark.tex` (fill remaining subsections)
- Modify: `citecheck/paper/sections/06_discussion.tex`
- Modify: `citecheck/paper/sections/07_conclusion.tex`
- Modify: `citecheck/paper/sections/00_abstract.tex`

- [ ] **Step 1: Introduction (~700 words)**

Lead with the Mata v. Avianca opener (already in the SOP, paragraph 1 — adapt, do not copy verbatim). Three-paragraph structure: (i) the problem in concrete terms, (ii) what's been tried (one sentence per major prior approach: Self-RAG, CRAG, EL-RAG, HalluGraph), (iii) our contribution (1 benchmark + 1 method + 3 empirical findings). End with a 1-sentence statement of the headline result.

- [ ] **Step 2: Related Work (~900 words)**

Three subsections: (i) Retrieval-augmented generation variants for faithfulness, (ii) Legal NLP benchmarks and evaluation, (iii) Structured generation and citation grounding. Per subsection: 3–6 papers, with each paper getting 1–2 sentences that say what they did and how CiteCheck differs. Do NOT just list — *position*.

- [ ] **Step 3: Section 3 Benchmark — fill subsections beyond construction**

Subsections to add to Section 3 from the outline: dataset statistics (1 table — Tab. 1), task taxonomy, jurisdictional coverage, comparison with LegalBench-RAG and CUAD (1 paragraph), licensing and access (1 paragraph — confirm CUAD's CC-BY-4.0, CAP's public domain, LegalBench-RAG's terms).

- [ ] **Step 4: Discussion (~800 words)**

Three parts: (i) where CiteCheck wins and why (point at the ablation evidence); (ii) where CiteCheck loses or under-performs (the per-jurisdiction breakdown's worst slice is your honest report — *do not hide it*); (iii) what generalizes and what doesn't (the 3-axis evaluation framework generalizes to medical, statutory, regulatory citation; the agentic retraction loop generalizes less because it requires a domain-specific resolver).

- [ ] **Step 5: Limitations (~300 words, often a top-level section in EMNLP/NAACL papers)**

Cover: English-only, US-only, federal-and-appellate-heavy corpus; NLI proxy for legal "stands for the proposition" is imperfect; reranker fine-tuned on Llama-3.1-8B specifically; cost / latency of the verify loop. Be honest. Reviewers reward limitation-honesty.

- [ ] **Step 6: Conclusion (~250 words)**

Restate the headline finding, point at one future-work direction that genuinely matters (e.g., temporal validity — citations to laws that have been amended), and end without flourish.

- [ ] **Step 7: Abstract (~200 words, written last)**

Structure: (i) problem in 1 sentence with a number, (ii) what we did in 2 sentences, (iii) headline result in 2 sentences with a number, (iv) what this enables in 1 sentence.

- [ ] **Step 8: Word-count check**

ACL/EMNLP long papers cap at 8 pages of body (excluding references and limitations); EMNLP workshops typically cap at 8 pages also. Run `texcount` and confirm body ≤ 8 pages compiled. Trim if over.

- [ ] **Step 9: Log Task 48 in `journal/weekly.md` (week of 2027-07-05)**

### Task 49: Internal review pass 1 — paste full draft into Claude/GPT for critique

**Artifacts:**
- Create: `citecheck/paper/reviews/internal_pass1_claude.md`
- Modify: paper sections to address critique

- [ ] **Step 1: Compile the current draft to a single PDF**

`pdflatex citecheck.tex && bibtex citecheck && pdflatex citecheck.tex && pdflatex citecheck.tex`. Verify PDF compiles without errors.

- [ ] **Step 2: Paste the full text into Claude (this CLI) with a structured critique prompt**

```
You are a senior NLP reviewer for EMNLP. Critique this paper draft on:
1. Clarity of the contribution claim (is it specific and falsifiable?)
2. Soundness of the evaluation (are baselines fair, metrics defensible?)
3. Coverage of related work (any obvious omission from 2024–2026?)
4. Statistical evidence (significance tests present? error bars?)
5. Limitations honesty (are there hidden weaknesses?)
6. Writing — top 5 unclear sentences with rewrite suggestions

Return your critique as markdown headings, with paste-able rewrite blocks where applicable.
```

- [ ] **Step 3: Save the critique to `citecheck/paper/reviews/internal_pass1_claude.md`**

- [ ] **Step 4: Address each critique item with one of {ACCEPT and edit, DEFER to pass 2, REJECT with note}**

Maintain a `% REVIEW-PASS-1:` comment block in each section file that lists the items addressed and how.

- [ ] **Step 5: Re-compile after edits; verify 8-page limit still holds**

- [ ] **Step 6: Log Task 49 in `journal/weekly.md` (week of 2027-07-12)**

### Task 50: Internal review pass 2 — share with reading group / paper-swap

**Artifacts:**
- Create: `citecheck/paper/reviews/internal_pass2_external.md`
- Modify: paper sections to address external critique

- [ ] **Step 1: Identify 1–2 external readers**

Sources (in priority order): (a) anyone from the Phase 1 paper-reading group who works on RAG / legal NLP; (b) advisors who responded to the Phase 1 Task 13 cold emails — even a 1-hour read in exchange for thanks is fair to ask; (c) a paper-swap thread on EleutherAI Discord or ML Collective Slack — explicit quid-pro-quo, you'll review their draft in return.

- [ ] **Step 2: Send the draft with a structured ask**

```
Subject: 1-hour read swap — CiteCheck draft (8 pp, NLLP 2027 target)

Hi [name],

Would you be open to swapping reads? Mine is attached — 8 pages on an open
benchmark + agentic-RAG method for verifying US case-law citations, target
NLLP @ EMNLP 2027. I'd value your reaction to:

1. Is the contribution claim clear in the abstract and intro?
2. Are the baselines fair / are obvious comparisons missing?
3. Anywhere I'm hand-waving where a number is expected?

A page of notes is plenty. Happy to do the same for any draft of yours.

Sincerely,
JP
```

- [ ] **Step 3: Collect responses; consolidate to `internal_pass2_external.md`**

Even if you only get one substantive response, that's enough. Two is luxurious.

- [ ] **Step 4: Address each external critique**

Same {ACCEPT/DEFER/REJECT} discipline as Task 49. Mark each in the paper sections.

- [ ] **Step 5: Re-compile; declare the draft "v1.0 ready for camera-ready polish"**

Tag the Overleaf project / git repo: `git tag paper-v1.0`.

- [ ] **Step 6: Log Task 50 in `journal/weekly.md` (week of 2027-07-19)**

RISK: external readers do not respond. Mitigation: do not block on them past 2 weeks; if no response by Jul 22, proceed to Task 51 + 52 and treat the external pass as a Phase 4 follow-up.

### Task 51: Application — refine the SOP narrative core with CiteCheck results

**Artifacts:**
- Modify: `applications/sop_narrative_skeleton.md` (replace placeholders)

- [ ] **Step 1: Open `applications/sop_narrative_skeleton.md` and locate `[INSERT SPECIFIC ACCOMPLISHMENTS]` in paragraph 4**

Cross-reference `applications/artifacts_strategy.md` (built in Task 43 step 0). Replace the placeholder with 3–4 concrete sentences:

```
For example: "Over the past 18 months I have built CiteCheck, an open
benchmark and agentic-RAG method for verifiable US case-law citations.
The benchmark comprises 500 human-verified question/gold-citation pairs
across federal and state jurisdictions (Cohen's kappa = X.XX between
annotators). The method — a hybrid retriever, a Bluebook-structure-aware
reranker fine-tuned with a multi-objective loss, and a CitationResolver
tool that retracts unresolvable citations — reduces fabrication rate by
X percentage points relative to the strongest open baseline on the
benchmark's adversarial split. The full system is released under
[license] with model and dataset cards on Hugging Face Hub. A workshop
paper is under submission at NLLP @ EMNLP 2027, with an arXiv preprint
available."
```

The exact numbers come from Task 41's results tables. If the workshop submission has not yet landed by the time per-program SOPs are sent (Sep 2027), phrase it as "under submission" — *do not claim acceptance you do not have*.

- [ ] **Step 2: Verify all in-text citations in the SOP still hold**

The SOP cites Magesh 2025, Pipitone & Houir Alami 2024, Wankhade 2026, Maynez 2020, Mata v. Avianca, Charlotin tracker. Confirm DOIs / URLs are still live. Re-check via `mcp__claude_ai_Scite__search_literature` if any look stale.

- [ ] **Step 3: Bump version to 0.2 and date-stamp**

In the SOP file header: `**Version:** 0.2 (post-experiments refinement)` and `**Last updated:** 2027-07-XX`.

- [ ] **Step 4: Re-export to PDF for use in recommender follow-up packets (Task 62)**

`pandoc applications/sop_narrative_skeleton.md -o applications/sop_narrative_skeleton.pdf`.

- [ ] **Step 5: Log Task 51 in `journal/weekly.md` (week of 2027-07-26)**

### Task 52: M6 milestone retrospective

**Artifacts:**
- Modify: `journal/phase3_retros.md` (M6 section)
- Modify: `journal/decisions.md`

- [ ] **Step 1: M6 retrospective entry**

```markdown
## M6 Retrospective — End of July 2027

- Paper draft v1.0: √ (tag `paper-v1.0`)
- Sections written: abstract, intro, related, benchmark, method, experiments, discussion, limitations, conclusion
- Internal review pass 1 (LLM critique): √, [N] items addressed
- Internal review pass 2 (external reader): [√ / partial / skipped] — [N] readers responded
- SOP narrative core refined to v0.2: √
- Recommenders: [N] confirmed and packet-sent, [N] silent (follow up in Aug)
- Total writing hours in Jun + Jul: [N]
- Compute hours in Jun + Jul: [N] (any one-more-number runs?)
- On track for M7 (Sep submission)? Y/N + reason

### Risks for Aug–Sep
- Workshop CFP deadline may shift — verify via OpenReview / venue website weekly
- A reviewer demand discovered late could force a partial re-run
- Per-program SOP customization is 15-25 documents, each taking 60–90 min
```

- [ ] **Step 2: Decision-log entry**

`| 2027-07-31 | Paper draft v1.0 locked for submission polish; SOP narrative core refined with CiteCheck results | All sections drafted; internal critique addressed | Reversible only at cost of re-drafting |`

- [ ] **Step 3: Log Task 52 in `journal/weekly.md` (week of 2027-07-26 — same week as Task 51 closure)**

---

## Month 4 — August 2027: Submission prep + GRE if needed + per-program SOP variants begin

### Task 53: Polish paper for workshop submission

**Artifacts:**
- Modify: `citecheck/paper/citecheck.tex` (and all section files)

- [ ] **Step 1: Anonymization for double-blind submission**

NLLP and TrustNLP typically use double-blind review. Strip:
- Author name and email from `\author{...}` — replace with `\author{Anonymous}`
- Acknowledgments section — wrap in `\iffalse ... \fi` so it doesn't compile
- GitHub repo URLs — replace with `https://anonymous.4open.science/...` (use the free anonymous-code service)
- Hugging Face model/dataset URLs — replace with placeholder text "[Anonymized for review]"
- Self-citations — if you cite your own prior work, use third-person framing

Verify: `grep -i "gabule\|johnpaul\|github.com/jpgabule"` returns nothing.

- [ ] **Step 2: Proofreading pass**

Tools: `chktex citecheck.tex` for LaTeX warnings; `aspell --mode=tex check sections/*.tex` for spelling; manual read for grammar. Fix every warning.

- [ ] **Step 3: Format check against the venue's submission requirements**

Open the NLLP 2027 CFP (https://nllpw.org/ or equivalent — verify the actual URL at submission time). Confirm: page limit, format (single-column or two-column), reference page count, supplementary material policy.

- [ ] **Step 4: Final compile and PDF check**

`pdflatex citecheck.tex && bibtex citecheck && pdflatex citecheck.tex && pdflatex citecheck.tex`. Open the PDF and visually scan every page for: (a) figures rendered correctly, (b) tables not overflowing margins, (c) URLs not breaking awkwardly, (d) reference list complete with all in-text citations resolved.

- [ ] **Step 5: Diff the anonymized version against the named version**

Keep two branches in your local git: `main` (named, for arXiv) and `submission` (anonymized). Verify the diff is *only* anonymization, not accidental content changes.

- [ ] **Step 6: Log Task 53 in `journal/weekly.md` (week of 2027-08-02)**

### Task 54: Camera-ready code release prep

**Artifacts:**
- Create: `citecheck/release/README_release.md`
- Create: `citecheck/release/LICENSE`
- Create: `citecheck/release/requirements.txt`
- Create: `citecheck/release/reproduce.ps1` + `reproduce.sh`
- Create: `citecheck/release/model_card.md`
- Create: `citecheck/release/dataset_card.md`

- [ ] **Step 1: Choose license — MIT or Apache-2.0**

MIT is shorter and more permissive (acceptable for code only). Apache-2.0 includes patent-grant language (better for tool-using systems with potential patent risk). Recommendation: **Apache-2.0** for code; **CC-BY-4.0** for the dataset (matches LegalBench-RAG and CUAD conventions).

Save to `citecheck/release/LICENSE` (the canonical Apache 2.0 text from https://www.apache.org/licenses/LICENSE-2.0.txt) and `citecheck/release/LICENSE_DATA` (CC-BY-4.0 text).

- [ ] **Step 2: Freeze requirements**

`pip freeze > citecheck/release/requirements.txt` from the `citecheck-py311` environment. Pin every dep to the exact version that produced the results.

- [ ] **Step 3: Write `reproduce.sh` and `reproduce.ps1`**

A one-shot script that: (a) builds the conda env, (b) downloads the CAP subset + CourtListener-cached responses needed for eval, (c) downloads the released reranker LoRA weights from HF Hub, (d) runs the eval over `data/eval/eval_set_v1.jsonl`, (e) prints the headline numbers.

Goal: a fresh reviewer can produce Table 2 in <2 wall-clock hours on a 24GB GPU.

- [ ] **Step 4: Write `model_card.md`**

Use the Hugging Face model card template (https://huggingface.co/docs/hub/model-cards). Sections: intended use, training data, evaluation, limitations, ethical considerations (legal AI in particular — flag "this model is not a substitute for legal counsel" prominently).

- [ ] **Step 5: Write `dataset_card.md`**

Use the Hugging Face dataset card template. Sections: dataset summary, supported tasks, languages (en), data instances (1 example record), data fields (the Pydantic schema from Phase 2 Task 17), data splits, source data, annotation process (cite Phase 2 Task 26 guidelines), inter-annotator agreement number, licensing.

- [ ] **Step 6: Write `README_release.md`**

The release-time root README. Sections: what is CiteCheck, how to install, how to reproduce, how to cite, license, acknowledgments (annotator, advisors, communities).

- [ ] **Step 7: Stage but do not publish yet**

The HF Hub upload and the GitHub release happen on the same day as workshop submission + arXiv (Task 55, Task 56). Until then, keep the release branch local.

- [ ] **Step 8: Log Task 54 in `journal/weekly.md` (week of 2027-08-09)**

### Task 55: Submit paper to chosen workshop

**Artifacts:**
- Submission: OpenReview / Softconf entry
- Modify: `journal/decisions.md` (log submission)

- [ ] **Step 1: Verify the actual 2027 deadlines**

Re-check via the venue's CFP page within 1 week of submission. The Phase 2 plan flagged "NLLP @ EMNLP 2027 submission Jun/Jul" and "TrustNLP @ EMNLP 2027 similar window" — both windows can shift; confirm.

Likely scenarios:
- NLLP @ EMNLP 2027 — submission deadline ~Jun-Jul 2027 (a typical pattern is paper submissions for EMNLP workshops are due 6–8 weeks before the main conference, which is usually Nov)
- TrustNLP @ EMNLP 2027 — similar window
- NeurIPS 2027 workshops — submission deadlines typically Aug-Sep 2027 (with the conference itself in Dec)

If by Aug 1 both NLLP and TrustNLP deadlines have *passed*, the fallback is a NeurIPS 2027 workshop (e.g., a Trustworthy ML or Foundation-Model workshop). Confirm the actual NeurIPS workshop list as published, and pick one whose scope covers legal-domain RAG or faithfulness.

- [ ] **Step 2: Create the submission portal entry**

NLLP and TrustNLP typically use OpenReview. Create account / log in. Start a new submission. Fill: title, authors (anonymized + add yourself privately), abstract, keywords, primary subject area, ethics statement.

- [ ] **Step 3: Upload the anonymized PDF**

Confirm: PDF is the anonymized version (Task 53 Step 5), the supplementary material is *not* required at this stage (workshop convention varies; check CFP), and the anonymous code link points to a working repo on https://anonymous.4open.science/.

- [ ] **Step 4: Submit**

Capture a screenshot of the confirmation page. Save to `citecheck/paper/submission_confirmation.png`.

- [ ] **Step 5: Decision-log entry**

`| 2027-08-XX | Submitted CiteCheck to NLLP @ EMNLP 2027 (backup: TrustNLP) | Workshop reach, with arXiv preprint as parallel distribution | Reversible: can withdraw before reviewing starts |`

- [ ] **Step 6: Log Task 55 in `journal/weekly.md` (week of 2027-08-16)**

RISK: workshop deadline already past at the time you check. Mitigation: NeurIPS workshops typically open submission in Aug with deadlines around late Aug / early Sep. If both EMNLP workshop windows are gone by Aug, target a NeurIPS workshop; if those are also gone, fall back to ACL Rolling Review (ARR) for the Oct 2027 cycle (deadline ~Oct 15, decisions Feb 2028 — *this misses the application cycle's value*, so it's a true last resort).

### Task 56: arXiv preprint of paper

**Artifacts:**
- arXiv submission
- Modify: `journal/decisions.md`

- [ ] **Step 1: Use the NON-anonymized version**

Switch back to `main` branch (named authors, acknowledgments included, real GitHub and HF URLs).

- [ ] **Step 2: Add the venue note**

Add to the abstract footnote: "Under submission at NLLP @ EMNLP 2027." Do *not* claim acceptance you do not have. If the workshop has a no-preprint policy (rare for workshops), respect it — verify before posting.

- [ ] **Step 3: Submit to arXiv**

https://arxiv.org/submit (or `arxiv-sanity submit` if you use the CLI tool). Primary category: `cs.CL`. Secondary: `cs.IR`. Allow ~12 hours for moderation (typically posted next business day).

- [ ] **Step 4: Once live, simultaneously**

- Push the GitHub repo public; `git tag v1.0`; create a GitHub Release with the tag and link to the arXiv ID.
- Publish the model and dataset cards to Hugging Face Hub (use `huggingface-cli upload`).
- Post a short announcement on your research blog (Phase 1 Task 0 Step 7) and on the recommended community channels (ML Collective, EleutherAI, Twitter / Bluesky if you use those).
- Add the arXiv URL to `applications/sop_narrative_skeleton.md` paragraph 4 (replace "under submission" with "arXiv:YYMM.XXXXX").

- [ ] **Step 5: Decision-log entry**

`| 2027-08-XX | arXiv preprint live (arXiv:YYMM.XXXXX); GitHub + HF Hub release public | Preprint amplifies the workshop submission and gives recommenders/admissions readers a stable URL | Irreversible (arXiv versions are permanent; can post new versions but not delete) |`

- [ ] **Step 6: Log Task 56 in `journal/weekly.md` (week of 2027-08-16)**

### Task 57: Take GRE if any target program still requires (verify per program first)

**Artifacts:**
- Create: `applications/gre/program_gre_requirements.md`
- Create: `applications/gre/score_report.pdf` (if test taken)

- [ ] **Step 1: Per-program GRE policy audit**

By 2027, most top-tier US CS PhD programs have dropped the GRE permanently. Verify each program on your `programs_draft.md` (Task 46) individually — go to their PhD admissions FAQ. Categorize:
- **not accepted** (e.g., Stanford CS has not accepted GRE since 2021) — do *not* take.
- **optional / not required** — do not take unless you would dramatically over-perform (≥330 combined) and want a credential signal.
- **required** — must take.

Build `applications/gre/program_gre_requirements.md` with one row per program.

- [ ] **Step 2: If zero programs require GRE — skip this task; log the skip**

`| 2027-08-XX | GRE waived for all target programs in cycle 2027–28 | Audited each program's PhD admissions page; none require GRE | Reversible if a late-added program does require it |`

- [ ] **Step 3: If ≥1 program requires GRE — register and schedule**

Register at https://www.ets.org/gre/ — fee ~$220 USD. Test centers fill up; schedule by Aug 1 for an Aug-late or early-Sep test date. Allow 10–15 business days for official score reporting to programs (ETS sends 4 free score reports at test time; additional reports are $35 each).

- [ ] **Step 4: Preparation budget**

Two-week intensive prep is typical for someone with a CS Master's: Magoosh / Manhattan Prep / ETS official PowerPrep. Budget ~40 hours. Target score for top CS programs that still require: Q ≥ 168, V ≥ 158.

- [ ] **Step 5: After taking the test, log the score**

Save the ETS score report to `applications/gre/score_report.pdf`. Update `program_gre_requirements.md` with the actual score.

- [ ] **Step 6: Log Task 57 in `journal/weekly.md` (week of 2027-08-23)**

RISK: GRE-required program lowers cap because of bad score. Mitigation: if score is below target by >5 points on Quant, retake within 21 days (ETS allows up to 5 retakes per 365-day rolling window). If retake risk is high, drop that program from the list.

### Task 58: Application — start per-program SOP customization for the top 5 programs first

**Artifacts:**
- Create: `applications/sops/{program-slug}.md` (5 files in Aug; remaining 10–20 in Sep — Task 61)

- [ ] **Step 1: Identify the top 5 priority programs**

Highest-priority criteria: (a) advisor fit (one or two named advisors whose work directly informs CiteCheck — examples: Daniel Ho / Julian Nyarko at Stanford RegLab; advisors at CMU LTI working on faithful RAG; advisors at UW or Edinburgh working on factuality), (b) deadline (earlier deadlines get drafted first), (c) likelihood of admission.

- [ ] **Step 2: For each of the 5, copy the skeleton and customize**

```powershell
foreach ($p in @("stanford-cs", "cmu-lti", "uw-cs", "ucb-eecs", "edinburgh-ilcc")) {
  Copy-Item applications\sop_narrative_skeleton.md applications\sops\$p.md
}
```

For each file, fill in:
- `[CUSTOMIZE-ADVISOR]` — 2–3 sentences citing ONE specific advisor's paper (by title and year) and connecting it to a piece of CiteCheck. The Edinburgh and Stanford worked examples in the skeleton are *reference templates only* — remove the second example in each per-program file.
- `[PROGRAM-SPECIFIC HOOK]` — 1–2 sentences on the program's environment (lab affiliation, named center, location-relevant courts, compute resources, industry partnerships).
- Opening hook customization (Mata v. Avianca for US programs; for UK programs like Cambridge or Oxford, swap to *Ayinde v. The London Borough of Haringey* (2025) or *Harber v. HMRC* (2023)).

- [ ] **Step 3: Word-count check per SOP**

Target: 1000–1200 words per the skeleton. Most programs cap at 1000–1500 words; verify each program's exact cap on its admissions page and trim.

- [ ] **Step 4: Cross-read pass**

Pick any 2 of the 5 SOPs and read them back-to-back. They should be ~80% identical (the research-vision paragraphs 1–4 and 6) and ~20% distinct (the research-fit paragraph 5). If they read as 100% identical, paragraph 5 needs more customization. If they read as <50% identical, you've over-customized — pull back; the narrative core is stable.

- [ ] **Step 5: Log Task 58 + Aug weekly reflection in `journal/weekly.md` (week of 2027-08-30)**

End-of-August journal entry: paper submitted (where?), arXiv live (ID?), GRE status (taken / skipped / scheduled), SOPs drafted (5/N), recommender response rate.

---

## Month 5 — September 2027: M7 closeout + lock final program list + finish SOPs

### Task 59: Workshop reviews — respond to reviewer comments if camera-ready required

**Artifacts:**
- Create: `citecheck/paper/reviews/reviewer_responses.md`
- Possibly modify: paper sections for camera-ready

- [ ] **Step 1: Monitor OpenReview / venue email for reviews**

NLLP and TrustNLP typically return reviews 3–6 weeks after submission. If you submitted Aug 16, expect reviews mid- to late-September. NeurIPS workshops (if you fell back) may not return until October — in which case this task slips to Phase 4 (acceptable; the arXiv preprint is what serves the application cycle).

- [ ] **Step 2: If reviews arrive — read all and triage**

Categorize each reviewer comment: {accept-as-is, clarification, additional-experiment, fundamental-rejection-of-claim}. Most workshop reviews land in the first two categories.

- [ ] **Step 3: Write a structured response (if rebuttal is allowed)**

```markdown
# Reviewer Responses — NLLP @ EMNLP 2027

## Reviewer 1
- Comment R1.1: [paste]
- Response: [your reply]
- Paper change: [reference to specific edit]

## Reviewer 2
...
```

Workshops often skip formal rebuttals; in that case, you address comments directly in camera-ready.

- [ ] **Step 4: If accepted — prepare camera-ready**

Add author names back, restore acknowledgments, replace anonymized code URL with the real one. Re-compile. Submit by camera-ready deadline (typically 2–4 weeks after notification).

If rejected at the primary venue and the TrustNLP backup is still open, re-submit there. If both are closed, target a NeurIPS workshop in Oct or hold for ACL Rolling Review (next cycle, value already extracted from the preprint).

- [ ] **Step 5: Update SOP language**

If accepted: change `applications/sop_narrative_skeleton.md` paragraph 4 from "under submission" to "accepted at NLLP @ EMNLP 2027". Re-export to PDF; propagate to all per-program SOPs.

If rejected: leave the language as "arXiv preprint" — the preprint is the durable artifact and is what matters for admissions readers.

- [ ] **Step 6: Decision-log entry**

`| 2027-09-XX | Workshop decision received: [accepted / rejected] | [1-sentence rationale] | [Reversible: can submit to other venues] |`

- [ ] **Step 7: Log Task 59 in `journal/weekly.md` (week of 2027-09-06)**

RISK: rejection at the primary venue right before application deadlines. Mitigation: arXiv preprint already exists and is the load-bearing artifact for admissions. Rejection is genuinely tolerable for the application cycle; you can resubmit in early 2028.

### Task 60: Application — lock the final program list

**Artifacts:**
- Create: `applications/programs_final.md`
- Create / Modify: `applications/deadlines_tracker.xlsx` (export from Google Sheets)

- [ ] **Step 1: Review `applications/programs_draft.md` (Task 46) line-by-line**

For each program, re-verify (the 2027–28 application cycle's admissions page is now fully published):
- Deadline (down to hour and timezone)
- Application fee
- Fee-waiver eligibility (financial-need waivers, GRFP-recipient waivers, conference-affiliated waivers — apply by Sep 30 for most programs)
- GRE policy (cross-check with Task 57)
- Letter submission method (Interfolio, school portal, direct email)
- Number of letters required (3 standard; some programs accept 4)
- Statement word/page cap
- Transcript requirements (official sealed vs. uploaded copy)
- English-proficiency test requirements (TOEFL/IELTS — typically waived if your degree was English-medium, but verify per program)

- [ ] **Step 2: Cut and add as needed**

Cuts: a program that quietly added a research-statement requirement you don't have the bandwidth for, a program whose only advisor of interest left, a program whose deadline conflicts unrecoverably. Adds: any newly-discovered fit (a faculty hire announced in 2027 whose work aligns with CiteCheck).

Final list size: 15–25 programs. Smaller-is-better for SOP quality.

- [ ] **Step 3: Build `applications/programs_final.md`**

```markdown
# Locked Program List — Fall 2027 PhD Applications (Cycle 2027–28)

**Locked:** 2027-09-XX
**Total programs:** [N]
**Reach / Match / Safety:** [a/b/c]

| Program | Deadline | Time zone | Fee | Waiver eligible? | GRE? | Letters | Submission method | SOP status | Notes |
|---------|----------|-----------|-----|------------------|------|---------|-------------------|------------|-------|
| Stanford CS | 2027-12-08 | PT 23:59 | $125 | conf-waiver | no | 3 | school portal — emails letter-writers | ready | Adv: Daniel Ho |
| ...
```

- [ ] **Step 4: Build `deadlines_tracker.xlsx`**

Export the above table to Google Sheets and pin a chronological view sorted by deadline. Add conditional formatting that highlights deadlines within 14 days.

- [ ] **Step 5: Submit any fee-waiver applications**

Most need to be in by Sep 30 – Oct 15. Use `mcp__claude_ai_Google_Calendar__create_event` to set reminders for each.

- [ ] **Step 6: Decision-log entry**

`| 2027-09-XX | Final program list locked at [N] programs | Verified deadlines, fees, letter requirements, GRE policies for each | Costly to revise: requires updating recommender packets |`

- [ ] **Step 7: Log Task 60 in `journal/weekly.md` (week of 2027-09-13)**

### Task 61: Application — complete per-program SOP tailoring for ALL locked programs

**Artifacts:**
- Modify: `applications/sops/{program-slug}.md` (5 from Task 58)
- Create: `applications/sops/{program-slug}.md` (the remaining 10–20)
- Create: `applications/sops/{program-slug}.pdf` (PDF export per program)

- [ ] **Step 1: For each remaining program — instantiate from the skeleton**

```powershell
$remaining = Get-Content applications\programs_final_slugs.txt
foreach ($p in $remaining) {
  if (-not (Test-Path "applications\sops\$p.md")) {
    Copy-Item applications\sop_narrative_skeleton.md "applications\sops\$p.md"
  }
}
```

- [ ] **Step 2: Per program, fill the 3 customization slots**

The skeleton's customization checklist is the cheat sheet:
- `[CUSTOMIZE-ADVISOR]` block (from `outreach/advisors.md` papers-read row for that program's top advisor)
- `[PROGRAM-SPECIFIC HOOK]` block
- Opening hook variant (US vs. UK case)

For UK programs (Cambridge, Oxford, Edinburgh, UCL): swap *Mata v. Avianca* for *Ayinde v. Haringey* or *Harber v. HMRC*. For Canadian programs (Toronto, McGill, Waterloo): keep US framing but acknowledge the cross-jurisdictional relevance in paragraph 6.

- [ ] **Step 3: Per-program word-count enforcement**

Each program's cap is in `programs_final.md`. Trim each SOP to its specific cap.

- [ ] **Step 4: PDF export**

`pandoc applications/sops/{slug}.md -o applications/sops/{slug}.pdf --pdf-engine=xelatex -V geometry:margin=1in`

- [ ] **Step 5: Final cross-read**

Sample 3 of the 15–25 SOPs at random. Read them back-to-back. Confirm:
- Same opening hook (or correctly-localized variant)
- Same research direction in paragraphs 2–4
- Distinct paragraph-5 research-fit content per program
- No leftover `[PLACEHOLDER]` markers (use `grep -l "\[CUSTOMIZE\|\[INSERT\|\[PROGRAM" applications/sops/*.md` — should return zero hits)

- [ ] **Step 6: Update `programs_final.md` SOP status column**

Mark each row's SOP status as `draft-final` (ready for the Phase 4 submission push, but not yet uploaded to any portal).

- [ ] **Step 7: Log Task 61 in `journal/weekly.md` (week of 2027-09-20)**

This is the highest-volume task of Phase 3. Budget 60–90 minutes per SOP × ~17 SOPs (assuming 5 done in Task 58, 12 more in Task 61) = ~15–25 hours. Block out a dedicated week.

### Task 62: Application — send personalized follow-ups to recommenders

**Artifacts:**
- Create: `applications/recommenders/followups/{recommender-slug}_followup_sep.md`
- Send: emails (3–4)
- Modify: `applications/recommenders/log.md`

- [ ] **Step 1: Trigger date is earliest-deadline minus 4 weeks**

For Dec 1 deadlines, send around Nov 1. For Nov 15 deadlines (rare), send mid-Oct. Some programs accept letters early — call out which in the follow-up.

NOTE: Phase 3 ends Sep 30. The literal send may slip into early October. Plan: pre-write the follow-up text in late Sep so Phase 4 just hits "send".

- [ ] **Step 2: Per recommender, draft a follow-up email**

```
Subject: PhD application update — final program list + reminder

Dear Prof. [Last name],

A short update as deadlines approach. The CiteCheck workshop submission
[was accepted at / is under review at / appears as arXiv:YYMM.XXXXX at]
NLLP @ EMNLP 2027 and the preprint is at [link]. I've updated my SOP
paragraph 4 to reflect this; the latest version is attached.

The final program list is now locked at [N] programs (table attached).
The earliest deadline is [date]. Most programs will email you a portal
link by [month]; a few use Interfolio, where my Dossier ID is [...].

If anything is missing or unclear — especially if a portal link hasn't
arrived for any of the programs listed — please let me know.

Thank you again,
JP
```

Attach the *updated* `sop_narrative_skeleton.pdf` (v0.2 or v0.3 with arXiv URL) and the deadline tracker as PDF.

- [ ] **Step 3: Save each follow-up draft**

`applications/recommenders/followups/{recommender-slug}_followup_sep.md`. These are pre-drafted; the actual send happens in Phase 4 (week of 2027-11-01 typically).

- [ ] **Step 4: Calendar reminder for the send**

`mcp__claude_ai_Google_Calendar__create_event` titled "Send recommender follow-up wave 1" on the date that is earliest-deadline minus 4 weeks.

- [ ] **Step 5: Log Task 62 in `journal/weekly.md` (week of 2027-09-27)**

### Task 63: Phase 3 closeout retrospective; M7 milestone reached; hand-off to Phase 4

**Artifacts:**
- Modify: `journal/phase3_retros.md` (M7 + closeout sections)
- Modify: `journal/decisions.md`
- Create: `docs/superpowers/plans/phase4_kickoff_notes.md` (a brief — not the full plan; that's Phase 4's first task)

- [ ] **Step 1: M7 retrospective**

```markdown
## M7 Retrospective — End of September 2027

- Workshop submission: √ (NLLP @ EMNLP 2027 / TrustNLP / NeurIPS workshop — name actual venue)
- arXiv preprint: √ (arXiv:YYMM.XXXXX)
- Code + model + dataset release: √ (GitHub / HF Hub URLs)
- Workshop reviews status: [received / pending]
- Workshop acceptance status: [accepted / rejected / pending]
- Final program list locked: √ ([N] programs)
- Per-program SOPs drafted: √ ([N] / [N])
- Recommenders briefed, packets sent, follow-ups pre-drafted: √
- Total writing hours in Phase 3: [N]
- Total compute hours in Phase 3: [N]
```

- [ ] **Step 2: Phase 3 closeout retrospective**

```markdown
## Phase 3 Closeout — Week of 2027-09-27

- Phase 3 status: COMPLETE
- Total weeks elapsed: 22 (May 1 – Sep 30)
- Total artifacts produced:
  - Research: paper draft v1, paper submission, arXiv preprint, GitHub release, HF model + dataset cards
  - Applications: SOP narrative core refined to v0.2/v0.3, 15-25 per-program SOPs, locked program list, deadline tracker, recommender packets sent, recommender follow-ups pre-drafted, GRE status resolved
- Phase 4 kickoff: 2027-10-04 (week of)
- Energy / confidence (1-10): [N]
- Biggest learning of Phase 3: [...]

### What carries into Phase 4
- The November application submission push (15-25 portals)
- Recommender follow-up wave 1 (Nov 1, pre-drafted)
- Workshop review responses if reviews still pending
- Interview-prep for programs that interview applicants (Dec-Feb)
- Decision-management in Mar-Apr 2028

### Risks for Phase 4
- A recommender goes silent in November despite follow-ups
- A portal-side bug delays submission (have one screen-recording of the upload process per portal type for support tickets)
- An invited interview lands during a high-load research week
```

- [ ] **Step 3: Phase 4 kickoff brief (not a full plan)**

```markdown
# Phase 4 Kickoff Brief — Oct-Dec 2027 + Jan-Apr 2028

## Tasks Phase 4 must produce (full plan written week of 2027-10-04)
- Submit applications to 15-25 programs by their deadlines
- Manage recommender follow-ups: wave 1 (Nov 1), wave 2 (Dec 1) for late deadlines
- Track portal-side confirmations
- Respond to interview requests (typical: Jan-Feb)
- Manage decision deadlines (typical: Apr 15)
- Visit days (in-person or virtual, Mar-Apr)
- Decision and accept (by Apr 15)

## Inputs Phase 4 inherits from Phase 3
- `applications/programs_final.md` (locked)
- `applications/sops/*.md` and `*.pdf` (drafted)
- `applications/deadlines_tracker.xlsx` (live)
- `applications/recommenders/followups/*.md` (pre-drafted)
- `citecheck/paper/citecheck.pdf` (preprint live)
- All Phase 1+2+3 outreach + journal artifacts

## Constraints for Phase 4
- November and early December are the highest-load weeks of the cycle
- A separate budget item: $500–1000 for application fees (15-25 × ~$95 average)
```

- [ ] **Step 4: Final Phase 3 weekly journal entry (week of 2027-09-27)**

```markdown
## Phase 3 Closeout — Week of 2027-09-27
- Phase 3 status: COMPLETE
- Total weeks elapsed: 22
- Phase 4 kickoff: 2027-10-04
- Energy / confidence: [N]
- One-sentence summary of Phase 3: "[built and shipped CiteCheck the paper and the application materials in parallel]"
```

- [ ] **Step 5: Decision-log final entry of Phase 3**

`| 2027-09-30 | Phase 3 complete: paper submitted + preprint live; application materials ready to submit | All Phase 3 milestones achieved; clean hand-off to Phase 4 | Yes — Phase 4 can still adjust program list at the margin |`

- [ ] **Step 6: Log Task 63 in `journal/weekly.md` (week of 2027-09-27 — final Phase 3 entry)**

---

## Verification Checklist (run at end of Phase 3)

Before declaring Phase 3 complete, confirm the following exist with content:

- [ ] `citecheck/paper/citecheck.tex` compiles to a complete PDF (≤8 pp body)
- [ ] All `citecheck/paper/sections/*.tex` populated; no `% TODO` markers
- [ ] `citecheck/paper/tables/` has 8 tables; all referenced in body text
- [ ] `citecheck/paper/figures/` has 6 vector-PDF figures; all referenced in body text
- [ ] `citecheck/paper/references.bib` has ≥30 entries; every in-text citation resolves
- [ ] `citecheck/paper/reviews/internal_pass1_claude.md` exists with critique addressed
- [ ] `citecheck/paper/reviews/internal_pass2_external.md` exists (or marked "skipped — no responses")
- [ ] Workshop submission confirmed (screenshot in `citecheck/paper/submission_confirmation.png`)
- [ ] arXiv preprint live with arXiv ID logged in `journal/decisions.md`
- [ ] `citecheck/release/` populated: README, LICENSE, requirements.txt, reproduce.sh/.ps1, model_card.md, dataset_card.md
- [ ] GitHub repo public; `git tag v1.0` exists; GitHub Release created
- [ ] HF Hub model + dataset uploaded with cards
- [ ] `applications/artifacts_strategy.md` exists (gap backfill from Task 43)
- [ ] `applications/sop_narrative_skeleton.md` at v0.2+, all placeholders replaced where stable
- [ ] `applications/sops/` has 15–25 per-program drafts (md + pdf each); zero `[PLACEHOLDER]` markers remain
- [ ] `applications/programs_final.md` locked with deadlines, fees, GRE policy, letter method per program
- [ ] `applications/deadlines_tracker.xlsx` (or Google Sheets equivalent) live and sorted by deadline
- [ ] `applications/recommenders/recommender_shortlist.md` has 3–4 confirmed entries (+ 1 backup)
- [ ] `applications/recommenders/packets/` has one PDF per confirmed recommender, all sent
- [ ] `applications/recommenders/followups/` has pre-drafted follow-ups per recommender
- [ ] `applications/gre/program_gre_requirements.md` exists; GRE taken or correctly skipped
- [ ] `journal/phase3_retros.md` has M5-final, M6, M7, and Phase 3 closeout sections filled
- [ ] `journal/weekly.md` has weekly entries for all 22 weeks of Phase 3
- [ ] `journal/decisions.md` has at least 8 new Phase 3 decisions logged
- [ ] `docs/superpowers/plans/phase4_kickoff_notes.md` exists for the Oct 2027 transition

---

## Compute & Cash Budget Summary (Phase 3)

| Month | Task block | Est. GPU-hours | Cash items |
|-------|------------|----------------|------------|
| May  | Stability + error-mode runs | 30 | (none) |
| Jun  | One-more-number runs during writing | ~5 | (none) |
| Jul  | (none — pure writing) | 0 | (none) |
| Aug  | (none — pure submission prep) | 0 | GRE registration ~$220 if needed; arXiv free |
| Sep  | (none — pure application work) | 0 | Interfolio Dossier $48; fee-waiver applications free |
| **Total** | | **~35 GPU-hours** | ~$270 (GRE optional) + $50 contingency API |

Phase 3 is light on compute and heavy on writing and coordination. Almost all GPU usage is in May for stability-check completion. Cash is dominated by GRE (if any program requires) and Interfolio.

Application-fee cash budget is deferred to Phase 4: ~15–25 programs × ~$95 average = ~$1,400–2,400. Apply for fee waivers in early September (Task 60 Step 5) to reduce this materially.
