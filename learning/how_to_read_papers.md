# How to Read Papers Efficiently

**The single most important skill in research preparation.** A Master's-level graduate who reads 50 papers carelessly is worse off than one who reads 30 with discipline. This guide is the protocol.

---

## The 3-pass method (Keshav 2007, adapted)

Adapted from S. Keshav, *How to Read a Paper* (ACM Computer Communication Review, 2007). The original is one page and worth reading once before adopting this.

### Pass 1: 5-10 minutes — Should I deep-read this?

**Goal:** decide if this paper is worth your time.

Read in order:
1. **Title.** What is the paper about?
2. **Abstract.** What does it claim?
3. **Introduction.** The first paragraph and the last 1-2 paragraphs (where contributions are stated).
4. **Section headers.** What's the structure?
5. **Figures and tables.** What's the headline result?
6. **Conclusion.** Restated contributions.

After pass 1, write down:
- Category (theory, method, empirical, survey, position)
- Context (what other papers does this build on or argue with?)
- Correctness (do the assumptions seem reasonable?)
- Contributions (in your own words)
- Clarity (is the paper well-written?)

Decision: pass 2 (deep dive), skim only (note 1 paragraph and move on), or drop (mark `dropped` in reading list).

### Pass 2: 60-90 minutes — Understand the contribution

**Goal:** be able to summarize the paper to a peer in 5 minutes.

- Read figures and tables in detail. Are they convincing? What's the comparison?
- Read the method section, not the equations — focus on the design choices and why they were made.
- Skim related work to see what they position against.
- Note the references you should follow up on (top 3-5).

After pass 2, write:
- 1-paragraph summary in your own words
- What surprised you (where the paper went against your intuition)
- What you'd ask the authors if you could
- 3-5 follow-up citations to add to your reading list

### Pass 3: 4-6 hours — Reproduce mentally

**Goal:** be able to write this paper yourself if the authors had not.

Only do pass 3 on papers central to your research direction. For CiteCheck, that's roughly 10-15 papers.

- Re-derive key equations on paper.
- Identify every assumption (stated or implicit).
- Identify limitations the authors did not mention.
- If code is available: clone and run it.
- If a dataset is involved: download a sample and inspect.

After pass 3, write:
- A "method box" (1 page) that captures the algorithm in pseudocode
- A "failure mode" list (3-5 ways the method could fail in practice)
- A position statement: do you build on this paper, depart from it, or contradict it?

---

## Time budget per phase

| Phase | Papers/week (target) | Pass-1 | Pass-2 | Pass-3 |
|---|---|---|---|---|
| Phase 1 (Foundation) | 3-5 | most | 1-2 per week | 0-1 per week |
| Phase 2 (Build) | 1-2 | as needed | new methods only | only directly-built-on |
| Phase 3 (Publish) | 0-1 | only as you cite | only when writing related work | rare |
| Phase 4 (Submit) | 0 | only crisis-reads | none | none |

---

## Note-taking that actually retains

The bottleneck is usually retention, not reading speed.

### The template

Use the template in `docs/superpowers/plans/2026-05-24-phd-prep-phase-1-foundation.md` Task 3 Step 3 for every Tier-1 paper. The key fields:

```markdown
# {Author} {Year} — {Title}

**DOI / arXiv:** ...
**Date read:** YYYY-MM-DD
**Read depth:** {skim | pass-2 | pass-3}
**Relevance to CiteCheck:** {High | Medium | Low}

## 1-line takeaway
[Force yourself to write this. If you can't, you didn't get the paper.]

## Problem
[1-2 sentences in your own words]

## Method
[1 paragraph, no equations — the design choices]

## Results
[Key numerical results + what they prove]

## Limitations
[What the authors acknowledge + what they don't]

## Questions / Ideas for my project
[Specific actionable transfer to CiteCheck]

## Citations to follow up
[2-5 references to add to reading_list.md]
```

### Why this template works

- **1-line takeaway forces compression.** If you can't fit the paper into one line, your understanding is incomplete.
- **"In your own words" prevents copy-paste reading.** A paper you can summarize in your own language is a paper you understand.
- **"Limitations" forces critical reading.** Every paper has limitations; finding them is how you become a peer reviewer.
- **"Citations to follow up" builds a citation graph.** This is how you map a field organically.

### What NOT to put in notes

- Direct quotes (you'll never re-read them; they're just decoration)
- Full equations (re-derive if you need them; copying them in doesn't help understanding)
- A summary of every section (you don't need it — the structured fields above suffice)
- A general impression ("interesting paper") — useless in 6 months

---

## Active reading techniques

### The "I'm explaining this to a colleague" frame
After every section, mentally explain it to a colleague who hasn't read the paper. If you stumble, re-read.

### The "predict the next sentence" exercise
At each paragraph break, pause and predict what the next paragraph will argue. Comparing your prediction to the actual paragraph reveals where your mental model differs from the paper's.

### The "rewrite the abstract" exercise
After pass 2, close the paper and write the abstract from memory. Compare to the actual abstract. The gaps are the parts you didn't internalize.

### The "draw the architecture" exercise
For any method paper, draw the system architecture on paper (or a whiteboard) without looking at the figure. Compare. The differences are what you missed.

---

## Where most people fail

### Failure 1: Reading like a textbook
Textbook = sequential, complete, foundational. Paper = argumentative, partial, derivative. Reading a paper sequentially front-to-back misses the structure that the paper is fundamentally trying to argue something specific.

Fix: always start with the abstract + intro + conclusion. Get the argument first; the technical details serve the argument.

### Failure 2: Reading for memorization
The goal is not to recall the paper later. The goal is to integrate the paper's ideas into your mental model. Memorization is a side effect of integration, not the cause.

Fix: focus on "what does this change about how I think about the problem?" not "what facts can I quote?"

### Failure 3: Reading the wrong papers
You can read 50 papers and learn less than someone who reads 10. The 10 must be the right ones.

Fix: `literature/deep_read_priority.md` lists Tier-1 (must-read), Tier-2 (Phase 2 baselines), Tier-3 (breadth), Tier-4 (skip unless needed). Honor the tiers.

### Failure 4: Reading without writing
Reading alone is consumption. Writing forces synthesis. Without notes, the paper evaporates.

Fix: every paper gets a notes file. If you didn't write a notes file, you didn't read the paper for research purposes — you read it for entertainment.

### Failure 5: Reading without context
A paper is a node in a citation graph. Reading it alone is reading half of it.

Fix: for Tier-1 papers, also read 2-3 of the most-cited references. For breadth: skim, don't deep-read, the related-work section of every paper you encounter to see what landscape it lives in.

---

## Tier-1 paper-specific notes

For the 10 Tier-1 papers in `literature/deep_read_priority.md`:

| Paper | Why deep-read | Time budget | Key questions to answer |
|---|---|---|---|
| Quevedo 2024 (Legal NLP survey) | Foundational context | 6 hours | What clusters does the field decompose into? What is missing? |
| Pipitone & Houir Alami 2024 (LegalBench-RAG) | Phase 2 baseline | 4 hours | What is the eval methodology? What's the SOTA? |
| Magesh 2025 (Hallucination-Free?) | Motivation anchor | 3 hours | What's the failure-mode taxonomy? How is hallucination defined? |
| Wankhade 2026 (EL-RAG) | Closest competitor | 4 hours | How does CAS / FJI differ from CiteCheck's three axes? |
| Guha 2022 (LegalBench) | Foundational benchmark | 4 hours | What tasks are in scope? What's intentionally excluded? |
| Choi 2025 (CiteGuard) | Methodological cousin | 3 hours | How does CiteCheck differ on the agent-loop vs. post-hoc question? |
| Choudhury 2025 (CLAUSE) | Scoop risk | 3 hours | How is CLAUSE different from CiteCheck? Where might they overlap? |
| Reuter 2025 (SAC) | Baseline | 3 hours | What's the chunking strategy? Does it generalize? |
| Asai 2023 (Self-RAG) | Baseline | 4 hours | What are reflection tokens? How does Self-RAG handle low-confidence retrieval? |
| Cheong 2025 (Access to Justice) | SOP narrative | 2 hours | What's the public-defender perspective? Why does open-weight matter? |

After Tier-1 (target: end of June 2026), you should be able to:
- Sketch the field landscape on a whiteboard
- Position CiteCheck in 2 sentences against each Tier-1 paper
- Name the 3-5 most important open questions in citation-faithful legal RAG

---

## Reading rhythms that work (empirically)

From PhD students and active researchers:

- **Morning reading, afternoon writing.** Fresh-brain reading retains more. Writing tolerates fatigue better than reading does.
- **One paper per session.** Don't half-read three papers — fully process one.
- **Active note-taking in the same file as the paper.** Don't switch apps. Keep the notes template open in the same window as the PDF.
- **Weekly summary in your research log.** Sunday: "this week I read X, Y, Z; the headline lesson was W."
- **Monthly synthesis.** End of month: "what have I learned that I didn't know 30 days ago? What changed about my project?"
- **Quarterly re-read.** Pick one Tier-1 paper and re-read your old notes vs. your current understanding. The diff is your growth.

---

## A note on reading-group etiquette

Reading groups are the highest-leverage learning environment for a PhD-prep applicant. Use them well:

- **Listen first.** Weeks 1-3: don't speak unless asked. Watch how experienced researchers discuss papers.
- **Ask questions, don't make statements.** "Did the authors discuss X?" is better than "I think they should have done Y."
- **Volunteer to present.** Once you're comfortable, present a paper. The act of preparing forces deep reading.
- **Don't show off.** The smartest people in the room ask the simplest questions.
- **Stay for the social part.** The 30 minutes after the formal discussion is where collaboration happens.

---

## When you've outgrown this guide

This is a starting protocol. After 6-12 months you'll develop your own rhythm. Signs you're past the starting protocol:

- You can predict the structure of a paper from the abstract alone
- You read in passes without consciously thinking about which pass you're in
- You skim and deep-read in the same paper, interleaving naturally
- You write notes that you actually re-read later
- You catch errors and omissions in papers before the discussion section

When you reach that stage, update this guide for the next person. That's how the protocol evolves.
