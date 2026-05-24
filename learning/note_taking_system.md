# Note-Taking System

**Purpose:** A simple, durable note-taking system you can maintain for 18 months without it becoming a burden. The system should be invisible — you spend time on the content, not on the tooling.

---

## The principle: durability > sophistication

The best note-taking system is the one you actually use 12 months from now. Most elaborate systems (Roam, Obsidian-with-50-plugins, Notion with relational databases) fail this test for solo PhD-prep applicants because the setup overhead exceeds the marginal benefit over plain markdown files in git.

**Recommendation:** plain markdown files in this git repo. That's the system.

If you want enhancement, add Obsidian or VS Code as a viewer (both read markdown natively). Don't migrate to a proprietary system.

---

## File organization

The directory structure is already laid out. Notes live in:

| Note type | Where | Format |
|---|---|---|
| Paper notes | `literature/papers/{lastname}-{year}.md` | Template per `phase-1-foundation.md` Task 3 |
| Weekly retrospectives | `journal/weekly.md` | Append one entry per week |
| Decisions | `journal/decisions.md` | Append one row per decision |
| Research ideas | `journal/ideas.md` (create as needed) | Bullet list with dates |
| Open questions | `journal/questions.md` (create as needed) | Bullet list with date asked, date resolved |
| Code experiments | `citecheck/runs/{date}-{experiment-name}.md` | Per-experiment notes |
| Interview notes | `applications/interviews/{program}.md` | Per-program prep + post-interview log |

Do not create new directory schemes. The existing ones are sufficient.

---

## Active reading notes

The single most-used note format. Template (from `how_to_read_papers.md`):

```markdown
# {Author} {Year} — {Title}

**DOI / arXiv:** ...
**Date read:** YYYY-MM-DD
**Read depth:** {skim | pass-2 | pass-3}
**Relevance to CiteCheck:** {High | Medium | Low}

## 1-line takeaway
[ONE sentence. Force yourself to write it.]

## Problem
[1-2 sentences in your own words]

## Method
[1 paragraph, no equations]

## Results
[Key numbers + what they prove]

## Limitations
[Authors' + your own]

## Questions / Ideas for my project
[Specific actionable transfer]

## Citations to follow up
[2-5 references]
```

### Anti-patterns

- **Copying the abstract.** You can re-read it any time. Notes are for *your* synthesis.
- **Writing in third person** ("the paper argues that..."). Use first person ("I found this convincing because..."); it's a research log, not an academic citation.
- **Notes that are longer than the paper.** Suggests you didn't synthesize.
- **Notes without a 1-line takeaway.** Suggests you didn't really finish the read.

---

## Linking notes

Plain markdown supports simple wiki-style links: `[[paper-id]]` or relative paths `[Quevedo 2024](quevedo-2024.md)`.

**When to link:**
- When a paper directly cites another paper you've read
- When two papers contradict each other
- When a paper's method inspired a CiteCheck design choice

**When NOT to link:**
- Don't try to build a comprehensive knowledge graph. The graph maintenance becomes the bottleneck.
- Links are useful for navigation, not for "completeness."

---

## Spaced-repetition (optional, high-leverage)

For vocabulary and concepts you need to retain across months:

**Setup:** Anki ([apps.ankiweb.net](https://apps.ankiweb.net/)) — free, syncs across devices.

**What to flashcard:**
- Acronyms: BM25, BGE, RRF, NLI, FAISS, ECTHR, SCOTUS, etc.
- Method names: Self-RAG, CRAG, EL-RAG, ALCE, RAGAS, etc.
- Statistical concepts: Cohen's kappa, F1 vs. precision vs. recall, t-test thresholds
- Legal concepts: holding vs. dicta, binding vs. persuasive, FRCP key sections

**What NOT to flashcard:**
- Code syntax (you'll look it up in context)
- Specific results (they change)
- Theoretical proofs (re-derive when needed)

**Cadence:** add 5-10 cards per week of Phase 1. Review 10 minutes daily. By end of Phase 1 you'll have ~150 cards; by Phase 2 you'll have automated knowledge of the field's vocabulary.

**Recommended deck structure:**
- Deck 1: Legal NLP vocabulary
- Deck 2: Retrieval / RAG methods
- Deck 3: Agent architectures
- Deck 4: Evaluation metrics
- Deck 5: Legal doctrine (holding, dicta, binding, persuasive, etc.)

---

## Concept maps

For visual learners (or anyone trying to see the field's structure):

**Tool:** Excalidraw ([excalidraw.com](https://excalidraw.com/)) — free, exports to PNG/SVG, can save .excalidraw files in git.

**When useful:**
- After reading 10+ papers, draw the relationships between them (who cites whom; who agrees with whom)
- Before locking the M2 candidate, draw the candidate-decision tree
- Before writing the paper's related work section, draw the field's clusters and where CiteCheck sits

**Save concept maps to:** `literature/concept_maps/` (create the directory).

Update once per month, not more. The concept map is a snapshot, not a living document.

---

## The "second brain" anti-pattern

Many productivity systems advertise themselves as a "second brain" — a comprehensive external system that holds everything you've ever read. Resist this.

Reasons:
1. **Maintenance cost outweighs benefit for a solo applicant on an 18-month timeline.** You're not building a 30-year knowledge base; you're preparing for one application cycle.
2. **The act of forgetting is part of synthesis.** What you forget after a week probably wasn't important; what stays with you is the residue worth keeping.
3. **The git repo IS your second brain.** It's already there, version-controlled, searchable with `grep`. Use it.

**If you must have a second brain:** use Obsidian as a viewer over this repo. Don't migrate the notes to Obsidian's vault format; just point Obsidian at the existing markdown files.

---

## Daily writing log (the highest-leverage note-taking practice)

This is the only "every day" note-taking commitment:

**File:** `journal/daily.md` (create as needed; daily entries can compress into weekly entries after a month)

**Format:** 2-5 minutes, free-form:

```markdown
## 2026-05-26

What I did today:
- Read Quevedo 2024 sections 1-3
- Took notes on cluster taxonomy

What I learned:
- Legal NLP has a clear pre-2020 / post-2020 split around transformer adoption
- Quevedo flags evaluation methodology as the biggest open issue — interesting for CiteCheck

What I'm stuck on:
- Section 4 (datasets) is dense — need to come back tomorrow

Plan for tomorrow:
- Finish Quevedo sections 4-5
- Start Pipitone 2024 LegalBench-RAG pass-1
```

This log is for *you*. No one else will read it. But it's the artifact that lets you (3 weeks from now) remember what you were thinking.

**Anti-pattern:** writing in a polished style for the daily log. Write fast, write rough, write honestly.

---

## Sunday review

Once a week, do a 30-minute review:

1. Read this week's daily entries (15 min)
2. Synthesize into `journal/weekly.md` weekly entry (10 min)
3. Plan the coming week against the phase plan (5 min)

The Sunday review is the meta-activity that keeps the plan on track. Without it, you drift; with it, drift is visible early.

---

## What to do when notes get out of hand

After 6+ months, your `literature/papers/` directory will have 30+ files. Some will be duplicates of insight; some will be outdated.

**Quarterly cleanup (15 minutes):**
- Delete notes for `dropped` papers (the paper is in `reading_list.md` as `dropped`; the notes file is dead weight)
- Merge notes where two papers say the same thing
- Update the `taxonomy.md` if cluster boundaries have shifted

Don't do this more often than quarterly. The instinct to "tidy notes" is procrastination.

---

## Final note: notes are private

These notes are for you. They are NOT public artifacts. Do not be afraid to write in shorthand, in your native language, in profanity, or in unfinished sentences. The audience is you-in-3-weeks; that audience is forgiving.

The polished version of your understanding goes into papers, SOPs, and emails. The rough version lives in notes. Don't conflate the two.
