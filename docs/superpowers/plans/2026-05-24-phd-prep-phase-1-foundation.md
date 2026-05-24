# PhD Prep — Phase 1 (Foundation) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Lay the research foundation by Aug 2026 — produce a 50-paper literature map, lock the specific agentic-RAG legal subtask, and have outreach + tracking infrastructure ready for the Build phase.

**Architecture:** Sixteen weekly tasks across four months. Each task produces a concrete artifact (markdown file, paper notes, decision log entry) checked into the project directory. Two milestone reviews (M1 end of June, M2 end of August) consolidate progress. Plan is for solo execution with cold-email feedback from 1–2 external academics in the final month.

**Tools & Resources:**
- Scite MCP server for literature search
- Reference manager: Zotero (recommended; free, BibTeX export) or Obsidian + Citations plugin
- Markdown editor for notes (VS Code, Obsidian, or plain editor)
- Email (Gmail) for cold outreach
- Spreadsheet (Google Sheets / Excel) for advisor + program tracking

---

## File Structure

All paths relative to `C:\Users\John Paul L. Gabule\Desktop\phd-computer-science`.

```
literature/
  reading_list.md            # master list of 50 papers, status per paper
  taxonomy.md                # clustering of papers by approach/subtask
  papers/
    {short-id}.md            # one note file per deep-read paper
project/
  problem_statement.md       # 1-page locked problem statement (M2 deliverable)
  candidates.md              # 3 candidate subtasks with evaluation
  baselines.md               # list of existing methods to reproduce
outreach/
  programs.md                # 15-25 target programs
  advisors.md                # 30-50 advisor profiles
  email_template.md          # base cold-email template
  log.md                     # outreach log (sent date, recipient, status)
journal/
  weekly.md                  # weekly retrospective entries
  decisions.md               # decision log (date + decision + rationale)
```

---

## Pre-work — Week 0 (last week of May 2026)

### Task 0: Set up project directory and tracking infrastructure

**Artifacts:**
- Create: `literature/`, `literature/papers/`, `project/`, `outreach/`, `journal/` directories
- Create: `literature/reading_list.md`
- Create: `journal/weekly.md`
- Create: `journal/decisions.md`

- [ ] **Step 1: Create directory structure**

In PowerShell, from the project root:

```powershell
New-Item -ItemType Directory -Force literature\papers, project, outreach, journal | Out-Null
```

Verify: `Test-Path literature\papers, project, outreach, journal` returns `True True True True`.

- [ ] **Step 2: Create `literature/reading_list.md` with header**

```markdown
# Reading List — Agentic RAG for Legal/Contracts

Target: 50 papers by end of June 2026. Status: pending | skimmed | deep-read.

| # | Status | Year | Authors | Title | DOI / arXiv | Note file |
|---|--------|------|---------|-------|-------------|-----------|
```

- [ ] **Step 3: Create `journal/weekly.md`**

```markdown
# Weekly Retrospective

Format per week: What went well | What stalled | Adjustment for next week | Hours logged

## Week of YYYY-MM-DD
- Went well:
- Stalled:
- Adjustment:
- Hours: 0
```

- [ ] **Step 4: Create `journal/decisions.md`**

```markdown
# Decision Log

| Date | Decision | Rationale | Reversible? |
|------|----------|-----------|-------------|
```

- [ ] **Step 5: Choose and install reference manager**

Recommendation: Zotero (https://www.zotero.org/). Install Zotero Desktop + browser connector.
Verify install: open Zotero, create a collection named "PhD Prep — Legal RAG".

- [ ] **Step 6: Join one online paper-reading group (Track M activity)**

Pick one and apply/join:
- ML Collective Reading Group (https://mlcollective.org/)
- Cohere For AI Open Science Community (https://cohere.com/research/cohere-for-ai)
- EleutherAI Discord (#research channels)
- A local university journal club (search "[your nearest university] CS journal club")

Save your chosen group name + meeting cadence in `journal/decisions.md` as a decision entry.

- [ ] **Step 7: Set up a public research log (Track M activity)**

Pick one and create:
- GitHub repo `phd-research-log` with a README that you update monthly, OR
- A free blog (https://hashnode.com, https://medium.com, or GitHub Pages with Jekyll/Hugo)

First post (placeholder, 100 words): "Why I'm preparing for a CS PhD in agentic RAG for legal applications" — date 2026-05-31.

Add the URL to `journal/decisions.md` and to your cold email template (Task 13, Step 1) when you build it.

- [ ] **Step 8: Log Week 0 completion**

Append to `journal/weekly.md`:

```markdown
## Week of 2026-05-25
- Went well: Project infrastructure set up. Reference manager chosen and installed. Reading group joined. Research blog seeded.
- Stalled: (nothing yet)
- Adjustment: (none)
- Hours: 3
```

---

## Month 1 — June 2026: Build literature map (Milestone M1)

### Task 1: Seed reading list with 7 foundational papers

**Artifacts:**
- Modify: `literature/reading_list.md` (add 7 entries)

- [ ] **Step 1: Add the 7 foundational papers found during plan design**

Open `literature/reading_list.md` and append these entries (status: pending):

| # | Status | Year | Authors | Title | DOI / arXiv | Note file |
|---|--------|------|---------|-------|-------------|-----------|
| 1 | pending | 2025 | Low et al. | Answering real-world clinical questions using LLM, RAG, and agentic systems | 10.1177/20552076251348850 | `papers/low-2025.md` |
| 2 | pending | 2025 | Yu et al. | YpathRAG: RAG framework and benchmark for pathology | arxiv:2510.08603 | `papers/yu-2025.md` |
| 3 | pending | 2025 | Yang et al. | Dual retrieving and ranking medical LLM with RAG | 10.1038/s41598-025-00724-w | `papers/yang-2025.md` |
| 4 | pending | 2025 | Wang et al. | Enterprise LLM evaluation benchmark | 10.5121/csit.2025.152001 | `papers/wang-2025.md` |
| 5 | pending | 2024 | Martin et al. | Semantic verification in LLM-based RAG | 10.1609/aaaiss.v3i1.31199 | `papers/martin-2024.md` |
| 6 | pending | 2026 | Shah | The state of evaluating LLM agents | 10.2139/ssrn.6172280 | `papers/shah-2026.md` |
| 7 | pending | 2025 | Fu et al. | CATArena: Tournament-style LLM agent evaluation | arxiv:2510.26852 | `papers/fu-2025.md` |

- [ ] **Step 2: Verify entries render correctly**

Open `literature/reading_list.md` in your markdown editor. Confirm: table renders with 7 rows.

- [ ] **Step 3: Log Task 1 completion**

Append to `journal/decisions.md`:

```markdown
| 2026-06-01 | Seeded reading list with 7 papers from plan design | These are the strongest hits from the May 2026 Scite search; safer than re-searching | Yes |
```

### Task 2: Add 10 legal-NLP-specific papers via Scite search

**Artifacts:**
- Modify: `literature/reading_list.md` (add 10 entries, items 8–17)

- [ ] **Step 1: Run Scite search for legal NLP + LLM**

In Claude Code, ask Claude (or run yourself in Scite web UI):

> Search Scite: `"legal" AND ("language model" OR "NLP") AND ("contract" OR "case law" OR "statute")`, date_from 2023, limit 20.

- [ ] **Step 2: Pick 10 papers most relevant to agentic RAG for legal tasks**

Selection criteria (prioritize):
1. Uses RAG, agents, or retrieval explicitly
2. Has open-access PDF
3. Includes evaluation methodology (not just method description)
4. Published 2024 or later

- [ ] **Step 3: Add the 10 selected papers to `literature/reading_list.md`**

Append rows 8–17 with status `pending` following the same column structure.

- [ ] **Step 4: Run Scite search for LegalBench and ContractNLI specifically**

Search for these benchmark papers (cited as baselines in the spec):

> Search Scite: `term="LegalBench"` and `term="ContractNLI"` separately, fetch top 3 each.

- [ ] **Step 5: Add 5 benchmark-related entries to reading list (rows 18–22)**

These will be your reproduction targets in M3.

- [ ] **Step 6: Log Task 2 completion in `journal/weekly.md` for week of 2026-06-01**

### Task 3: Deep-read papers 1–3 (foundational RAG)

**Artifacts:**
- Create: `literature/papers/low-2025.md`
- Create: `literature/papers/yu-2025.md`
- Create: `literature/papers/yang-2025.md`

- [ ] **Step 1: Open paper 1 (Low et al., 2025) and read abstract + introduction**

Use the access URL from your Scite search or `https://doi.org/10.1177/20552076251348850`.

- [ ] **Step 2: Read methods, results, discussion sections**

Skim related work; read the rest carefully.

- [ ] **Step 3: Create `literature/papers/low-2025.md` with the structured note template**

```markdown
# Low et al. 2025 — Answering real-world clinical questions using LLM, RAG, and agentic systems

**DOI:** 10.1177/20552076251348850
**Date read:** 2026-06-XX
**Read depth:** deep
**Relevance to legal RAG:** [High | Medium | Low]

## Problem
[1-2 sentences: what gap does this address?]

## Method
[1 paragraph: what did they build?]

## Results
[Key numerical results + what they prove]

## Limitations
[What the authors acknowledge + what you noticed]

## Questions / Ideas for my project
[What is unanswered? What could you do differently for legal domain?]

## Citations to follow up
[2-5 specific references from this paper to add to reading list]
```

- [ ] **Step 4: Mark paper 1 as deep-read in `literature/reading_list.md`**

Change status from `pending` to `deep-read`.

- [ ] **Step 5: Repeat Steps 1–4 for papers 2 and 3 (Yu 2025, Yang 2025)**

Each gets its own note file using the same template.

- [ ] **Step 6: Add new entries to reading_list from citations followed up**

If the three papers point to 5 new high-relevance papers, add rows 23–27.

- [ ] **Step 7: Log Task 3 in weekly journal (week of 2026-06-08)**

Hours expected: ~12 (4 hrs/paper × 3).

### Task 4: Deep-read papers 4–7 (agents + evaluation)

**Artifacts:**
- Create: `literature/papers/wang-2025.md`, `martin-2024.md`, `shah-2026.md`, `fu-2025.md`

- [ ] **Step 1: Deep-read Wang et al. 2025 (Enterprise LLM benchmark)**

Use the structured note template from Task 3. Save to `literature/papers/wang-2025.md`.

- [ ] **Step 2: Deep-read Martin et al. 2024 (Semantic verification in RAG)**

Save to `literature/papers/martin-2024.md`. Pay attention to their evaluation approach — this is directly relevant for legal fact-checking.

- [ ] **Step 3: Deep-read Shah 2026 (State of LLM agent evaluation)**

Save to `literature/papers/shah-2026.md`. This is a survey — extract the taxonomy of evaluation methodologies.

- [ ] **Step 4: Deep-read Fu et al. 2025 (CATArena)**

Save to `literature/papers/fu-2025.md`. Note tournament-style evaluation as a potential evaluation lens for your project.

- [ ] **Step 5: Mark all 4 as deep-read in reading_list.md**

- [ ] **Step 6: Log Task 4 in weekly journal (week of 2026-06-15)**

### Task 5: Skim remaining papers in reading list (~15 papers)

**Artifacts:**
- Modify: `literature/reading_list.md` (update statuses)
- Create: short notes for 5 highest-relevance skimmed papers (1 paragraph each)

- [ ] **Step 1: Skim each remaining paper — abstract, intro, conclusion only**

Per paper: ~15 minutes. For each, decide:
- High relevance → deep-read in July (mark `pending-deep`)
- Medium relevance → 1-paragraph note now (mark `skimmed`)
- Low relevance → drop from list (mark `dropped`)

- [ ] **Step 2: Write 1-paragraph note for each medium-relevance paper**

Format (in a single `literature/skim_notes.md` file):

```markdown
## {paper-id} — {title}
**DOI:** ...
**One-line takeaway:** ...
**Why kept in list:** ...
```

- [ ] **Step 3: Update reading_list.md with new statuses**

Confirm: every row has a status that is not `pending`.

- [ ] **Step 4: Top-up reading list to 50 entries**

If after dropping papers you have fewer than 50 entries, run additional Scite searches:
- `"agentic RAG" AND legal`
- `"contract" AND "language model" AND retrieval`
- `"case law" AND "neural"`

Add new entries until reading list has 50 unique papers.

- [ ] **Step 5: Log Task 5 in weekly journal (week of 2026-06-22)**

### Task 6: Build taxonomy and M1 review

**Artifacts:**
- Create: `literature/taxonomy.md`

- [ ] **Step 1: Cluster the deep-read papers by approach**

Open Zotero collection, look at your 7 deep-read papers and 5 skim notes. Identify 3–5 clusters. Example clusters:
- Domain-specific RAG with hybrid retrieval
- Agentic RAG with tool use
- Evaluation methodology (benchmarks)
- Semantic verification / fact-checking
- Fine-tuned retrieval models

- [ ] **Step 2: Write `literature/taxonomy.md`**

```markdown
# Taxonomy — Agentic RAG and Legal NLP, May 2026

## Cluster 1: [Name]
- Papers: [paper ids]
- Common approach: [1-2 sentences]
- Strengths: [...]
- Weaknesses: [...]
- Open questions: [...]

## Cluster 2: [Name]
...

## Cross-cluster observations
- What is everyone doing similarly?
- What is no one doing?
- Where is legal-domain coverage thinnest?
```

- [ ] **Step 3: Identify 3 candidate gaps that could become your research project**

Add to taxonomy.md a section "Candidate gaps for my project" listing 3 specific gaps (e.g., "no agentic RAG benchmark for contract-clause classification", "no efficiency-focused work on legal retrieval", "no multi-document reasoning evaluation on case law").

- [ ] **Step 4: M1 retrospective entry in `journal/weekly.md` (week of 2026-06-29)**

```markdown
## M1 Retrospective — End of June 2026
- Reading list: 50 papers
- Deep-read: 7 papers
- Skimmed: ~15 papers
- Taxonomy: 3-5 clusters identified
- Candidate gaps: 3 documented in taxonomy.md
- On track for M2 (Aug 2026)? [Y/N + reason]
```

- [ ] **Step 5: Log M1 completion in `journal/decisions.md`**

```markdown
| 2026-06-30 | M1 milestone reached: literature map + taxonomy + 3 candidate gaps | Foundation for niche-locking in M2 | Yes |
```

---

## Month 2 — July 2026: Deepen reading + draft 3 candidate problem statements

### Task 7: Deep-read 8 additional papers (4 per fortnight)

**Artifacts:**
- Create: 8 new note files in `literature/papers/`

- [ ] **Step 1: From `pending-deep` papers in reading_list, pick 8 for July**

Prioritize those that directly touch your 3 candidate gaps.

- [ ] **Step 2: Deep-read papers 8–11 in the first fortnight (week of Jul 6 + Jul 13)**

2 papers/week. Each gets a note file using the structured template from Task 3.

- [ ] **Step 3: Deep-read papers 12–15 in the second fortnight (Jul 20 + Jul 27)**

Same cadence.

- [ ] **Step 4: Update reading_list statuses + log weekly journal entries for each week**

### Task 8: Draft 3 candidate problem statements

**Artifacts:**
- Create: `project/candidates.md`

- [ ] **Step 1: Pick the 3 candidate gaps from taxonomy.md and turn each into a problem statement skeleton**

Open `project/candidates.md` and create three sections:

```markdown
# Candidate Problem Statements — July 2026

## Candidate A: [Working title]
- Problem: [2 sentences]
- Proposed method: [2 sentences — what's the agentic RAG twist?]
- Evaluation: [How will you measure success?]
- Datasets: [Are they public? What are they?]
- Baselines: [Which existing methods will you compare against?]
- Compute: [Will this run on 1 GPU with QLoRA on 7B models?]
- Estimated effort: [low/medium/high]

## Candidate B: ...
## Candidate C: ...
```

- [ ] **Step 2: Fill in each candidate from your taxonomy gaps**

Be specific. "Agentic RAG for contracts" is not a problem statement. "Multi-hop agentic RAG for cross-document obligation extraction in M&A contracts, evaluated on a 200-document test set" is.

- [ ] **Step 3: Identify which candidates have public data**

For each candidate, name a specific dataset:
- LegalBench tasks (specify which)
- ContractNLI
- CUAD (Contract Understanding Atticus Dataset)
- ECtHR cases (European Court of Human Rights)
- Caselaw Access Project

If none of your candidates has a public dataset, that candidate is a high-risk pick — flag it.

- [ ] **Step 4: Evaluate each candidate against criteria**

Add a table to `project/candidates.md`:

| Criterion | A | B | C |
|---|---|---|---|
| Data accessible | | | |
| Novel angle (vs reading list) | | | |
| Single-GPU feasible | | | |
| Reproducible baseline exists | | | |
| Publishable in 12 months | | | |

Score each Y/N or H/M/L.

- [ ] **Step 5: Log Task 8 in weekly journal (week of 2026-07-27)**

### Task 9: Pick top candidate (M2 preparation)

**Artifacts:**
- Modify: `project/candidates.md` (mark top pick)
- Create: `journal/decisions.md` entry

- [ ] **Step 1: Compare candidates against the evaluation table**

The winner is the one that scores Y/H on data accessibility AND publishability AND single-GPU feasibility. Novelty is the tiebreaker.

- [ ] **Step 2: Mark the winner in `project/candidates.md`**

Add at the top: `**Selected for M2: Candidate [X]** — locked 2026-07-31`.

- [ ] **Step 3: Log the decision in `journal/decisions.md`**

```markdown
| 2026-07-31 | Selected Candidate [X] as the research problem | [1-sentence rationale referencing the evaluation table] | Yes, but reversal cost rises after baseline reproduction in M3 |
```

---

## Month 3 — August 2026: Lock niche, prepare outreach (Milestone M2)

### Task 10: Write the 1-page locked problem statement

**Artifacts:**
- Create: `project/problem_statement.md`

- [ ] **Step 1: Create `project/problem_statement.md` with this structure**

```markdown
# Problem Statement — [Working title]

**Version:** 1.0
**Locked:** 2026-08-XX

## Problem (2-3 sentences)
[Specific, concrete problem in legal NLP. Reference real users / use case.]

## Why this matters (2-3 sentences)
[Why is solving this useful? What does failure look like?]

## Why agentic RAG is the right approach (2-3 sentences)
[What makes this not solvable with a single LLM call or pure RAG?]

## Proposed approach (1 paragraph)
[High-level: what components, what data flow, what novel element]

## Evaluation plan (1 paragraph)
[Dataset, baselines, metrics, ablations]

## Risks and contingencies (2-3 bullets)
[What could kill this project, and what would you do?]

## Timeline alignment
- M3 (Nov 2026): Baseline reproduction on [specific dataset + 2-3 methods]
- M4 (Feb 2027): Novel contribution scoped and prototyped
- M5 (May 2027): Full experiments complete
- M6 (Jul 2027): Paper draft v1
- M7 (Sep 2027): Submission to [target venue]

## References
[5-10 most important citations]
```

- [ ] **Step 2: Fill in every section. No placeholders.**

If any section feels weak, that's signal the candidate selection needs revisiting — but only revisit if you can't honestly fill in "Why this matters" with a real use case.

- [ ] **Step 3: Word count check**

A 1-page problem statement is ~500 words. Aim for 400–600. If over 800, cut.

- [ ] **Step 4: Log in weekly journal (week of 2026-08-03)**

### Task 11: Identify 30-50 candidate advisors

**Artifacts:**
- Create: `outreach/advisors.md`
- Create: `outreach/programs.md`

- [ ] **Step 1: Create initial program list of 15-25 programs**

Open `outreach/programs.md`:

```markdown
# Target Programs — Draft (Aug 2026)

Categorization: reach (top-10), match (top-30), safety (top-100).

## Reach (top-10 US CS PhD programs)
- [ ] Stanford
- [ ] MIT
- [ ] CMU
- [ ] UC Berkeley
- [ ] University of Washington

## Match (top-30)
- [ ] [program]
- [ ] ...

## Safety (top-100 / regional fit)
- [ ] [program]
- [ ] ...

## International (if applicable)
- [ ] [program]
- [ ] ...
```

Fill in real program names from CSRankings (https://csrankings.org/ → AI subfield).

- [ ] **Step 2: For each program, identify 2-4 faculty whose research touches NLP/RAG/agents/legal NLP**

Use the program's "Faculty" or "People" page; cross-reference with Google Scholar for recent (2024-2026) papers.

- [ ] **Step 3: Create `outreach/advisors.md`**

```markdown
# Candidate Advisors

| # | Name | Program | Title | Research area | Last 3 papers (titles) | Email | Reading status |
|---|------|---------|-------|---------------|------------------------|-------|----------------|
| 1 | | | | | | | not-read |
```

- [ ] **Step 4: Populate 30 entries minimum, 50 ideal**

Spend ~1 hour total per 10 advisors filled. Status options: `not-read` | `papers-read` | `email-drafted` | `email-sent` | `responded` | `dead-end`.

- [ ] **Step 5: Log in weekly journal (week of 2026-08-10)**

### Task 12: Read 2-3 papers per priority advisor (top 10)

**Artifacts:**
- Modify: `outreach/advisors.md` (update reading status)

- [ ] **Step 1: Pick the 10 advisors whose work most closely overlaps with your problem statement**

Star them in advisors.md.

- [ ] **Step 2: For each starred advisor, read 2-3 recent papers (abstract + intro + conclusion is enough)**

Per advisor: ~30-45 minutes. Note one concrete observation about their research direction in advisors.md.

- [ ] **Step 3: Update reading status to `papers-read` for the 10 advisors**

- [ ] **Step 4: Log in weekly journal (week of 2026-08-17)**

### Task 13: Draft cold email template and send to 2 academics for feedback

**Artifacts:**
- Create: `outreach/email_template.md`
- Modify: `outreach/log.md`

- [ ] **Step 1: Create `outreach/email_template.md`**

```markdown
# Cold Email Template (v1, Aug 2026)

## Subject lines (test both)
- "Question on your [paper title] from a prospective PhD applicant"
- "[Your problem statement keyword] — feedback request from a prospective applicant"

## Body

Dear Prof. [Last name],

I'm a Master's-level researcher preparing to apply for PhD CS programs in Fall 2027. Your recent paper, "[exact title]," particularly the [specific observation, 1 sentence — prove you read it], directly informs work I'm planning on [your problem statement in 1 sentence].

I'm writing a 1-page problem statement on [your topic] and would value your honest 60-second reaction — particularly whether the framing is sound and whether you see obvious issues with [specific decision in your problem statement, e.g., dataset choice]. The draft is attached.

I understand your time is limited; even a one-line response would be valuable.

Thank you for considering it.

Sincerely,
John Paul L. Gabule
[Affiliation / current role]
[Email]
[Link to public research blog or GitHub, if you have one — set one up in Track M]
```

- [ ] **Step 2: Create `outreach/log.md`**

```markdown
# Outreach Log

| Date sent | Recipient | Program | Subject | Status | Response date | Notes |
|-----------|-----------|---------|---------|--------|---------------|-------|
```

- [ ] **Step 3: Pick 2 advisors from your top-10 starred list whose work is closest to your problem statement**

These are not your top-choice advisors; these are "feedback advisors." If they respond, great. If not, you've lost nothing.

- [ ] **Step 4: Customize the template for each advisor — specifically the [exact title] and [specific observation]**

Re-read one of their papers before sending. The specificity is what gets a reply.

- [ ] **Step 5: Attach `project/problem_statement.md` as PDF**

Convert via pandoc or Word: `pandoc project/problem_statement.md -o problem_statement.pdf`.

- [ ] **Step 6: Send both emails**

- [ ] **Step 7: Log in `outreach/log.md`**

Add a row per email with status `sent`.

- [ ] **Step 8: Log in weekly journal (week of 2026-08-24)**

### Task 14: M2 milestone review and Phase 1 closeout

**Artifacts:**
- Modify: `journal/weekly.md` (M2 retrospective)
- Modify: `journal/decisions.md`

- [ ] **Step 1: M2 retrospective in `journal/weekly.md`**

```markdown
## M2 Retrospective — End of August 2026
- Problem statement: Locked at version 1.0
- Reading list: 50 papers, 15 deep-read
- Taxonomy: complete with 3-5 clusters
- Candidates: 3 evaluated, 1 selected
- Outreach: 2 cold emails sent for feedback, [N] advisors in pipeline
- On track for M3 (Nov 2026 — baseline reproduction)? [Y/N + reason]
- Any cold email responses? [paraphrase]
- Adjustments for Phase 2: [...]
```

- [ ] **Step 2: Log M2 completion in `journal/decisions.md`**

```markdown
| 2026-08-31 | M2 milestone reached: problem statement locked, outreach pipeline live | Foundation complete; ready for Build phase | Yes, problem statement can be revised before M3 |
```

- [ ] **Step 3: Schedule Phase 2 kickoff for week of 2026-09-07**

Phase 2 kickoff is its own planning session — produce a new implementation plan for Sep 2026 – Apr 2027 (M3–M5: baseline reproduction → novel contribution → full experiments). Don't try to write it now; the literature map and problem statement should inform that plan.

- [ ] **Step 4: Final Phase 1 weekly journal entry (week of 2026-08-31)**

```markdown
## Phase 1 Closeout — Week of 2026-08-31
- Phase 1 status: COMPLETE
- Total weeks elapsed: 16
- Total artifacts produced: 50-paper reading list, taxonomy, candidates doc, locked problem statement, 30-50 advisor list, 2 cold emails sent
- Phase 2 kickoff: 2026-09-07
- Energy level / confidence: [1-10 scale]
```

---

## Verification Checklist (run at end of Phase 1)

Before declaring Phase 1 complete, confirm the following exist with content:

- [ ] `literature/reading_list.md` has 50 entries, all with status (no `pending`)
- [ ] `literature/papers/` has at least 15 note files
- [ ] `literature/taxonomy.md` exists with 3–5 clusters and a "candidate gaps" section
- [ ] `project/candidates.md` has 3 candidates with evaluation table
- [ ] `project/problem_statement.md` exists at v1.0, ~400–600 words, no placeholders
- [ ] `outreach/programs.md` has 15–25 programs categorized reach/match/safety
- [ ] `outreach/advisors.md` has 30+ rows with `papers-read` status for top-10
- [ ] `outreach/email_template.md` exists in working form
- [ ] `outreach/log.md` has at least 2 `sent` rows
- [ ] `journal/weekly.md` has weekly entries for all 16 weeks
- [ ] `journal/decisions.md` has at least 5 logged decisions
- [ ] Active membership in a paper-reading group (attended at least 4 meetings)
- [ ] Research blog/log live with at least 4 posts (one per month)
