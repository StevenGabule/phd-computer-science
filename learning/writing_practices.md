# Writing Practices

**Purpose:** Concrete techniques for the kinds of writing you'll do across all 4 phases — research papers, SOPs, emails, problem statements, and journal entries. Each section is short because writing advice is mostly trivial; doing it consistently is the hard part.

---

## The single most important principle

**Write daily.** 250 words a day, every day, for the next 18 months. That's 137,000 words — far more than you need for a paper, 25 SOPs, and a journal combined.

The compound effect of daily writing is enormous. Writers who wait for inspiration produce 1 paper per 18 months; writers who write daily produce 4-5.

**Set up:** open `journal/weekly.md` every morning. Write 1-2 paragraphs of any kind. Even "I'm tired and don't want to write" counts as a warm-up.

---

## Writing for papers (Phase 2-3)

### The Methods section first

Counter-intuitive but consistent advice across senior researchers: write Methods, then Results, then Discussion, then Related Work, then Intro, then Abstract. Last.

**Why:** the Methods section is the most factual; it's easiest when the experiments are freshest. The Intro is the most argumentative; you need to know what the paper actually showed before you can argue for its importance.

### One contribution per paragraph

In the Intro and Discussion: each paragraph makes one argument. If you find yourself writing "additionally" or "furthermore," start a new paragraph.

### The "but" test

Read any sentence that uses "but" or "however." The sentence after the "but" is the actual claim. If the sentence before the "but" is doing work, separate them.

Example:
- Original: "Prior work has addressed retrieval quality, but our work focuses on citation faithfulness."
- Better: "Our work focuses on citation faithfulness — a complement to the retrieval-quality work that dominates prior literature."

### Adverbs you should kill

The following adverbs are almost always weakening:
- "obviously"
- "clearly"
- "simply"
- "merely"
- "essentially"
- "fundamentally" (sometimes OK)
- "actually" (almost always cut)
- "really" (always cut)

If an idea is obvious, you don't need to say so; the reader will see. If it's not obvious, saying "obviously" insults them.

### The 4-pass editing protocol

Each paper section gets 4 editing passes, ideally on different days:

1. **Logic pass.** Does the argument hold? Are claims supported? (Don't fix prose yet.)
2. **Structure pass.** Are paragraphs in the right order? Is each paragraph one argument?
3. **Sentence pass.** Cut weak adverbs. Tighten sentences. Read aloud.
4. **Mechanics pass.** Citations correct. Cross-references work. Formatting consistent.

Don't combine passes. The brain can't simultaneously check logic and sentence rhythm; you'll do both badly.

---

## Writing for SOPs (Phase 3)

### The 60-second test

Read your SOP's opening paragraph aloud. If a friend who knows nothing about CS could understand the central problem in 60 seconds, the opening is working. If not, rewrite.

### The "elevator advisor" test

Imagine the program director is in an elevator with you. You have 30 seconds to convince them you should be in their program. What sentence from your SOP would you use?

That sentence should be in the first 3 sentences of your SOP. If it isn't, restructure.

### The 5-paragraph structure

A standard SOP has 5-6 paragraphs:
1. **Hook + problem framing** (the concrete failure that motivates your research)
2. **What's missing in current work** (the gap)
3. **Your research direction** (what you propose; how it addresses the gap)
4. **Your preparation** (why you can do this work — concrete artifacts, not vibes)
5. **Why this program** (specific advisor + specific paper + connection to your direction)
6. **(Optional) Long-term vision**

Each paragraph: ~200 words. Total: ~1,000-1,200 words.

### Per-program customization without copy-paste

Use the SOP narrative skeleton in `applications/sop_narrative_skeleton.md` as the base. For each program:
- Rewrite the hook if program-appropriate (e.g., UK vs. US legal-tech examples for Edinburgh vs. Stanford)
- Rewrite paragraph 5 entirely (different advisor, different paper, different lab culture)
- Lightly edit paragraph 3 to emphasize the aspect of your research that fits the program's strength (retrieval emphasis at UMass, agents emphasis at CMU)

### Anti-patterns

- Starting with autobiography ("I have always been fascinated by...")
- Using "passion" or "passionate" anywhere
- Listing courses as a CV substitute
- Promising vague extensions ("I want to advance the field")
- Mentioning more than 2 advisors per program (looks like spray-and-pray)
- Including grades, GRE scores, or GPA in the SOP body (those go elsewhere)

---

## Writing for emails (Phases 1, 4)

### Cold emails to academics

**Subject line:** specific, not generic.
- Bad: "PhD inquiry"
- Good: "Question on your 2025 reasoning-focused legal retrieval benchmark"

**Body:** 4 short paragraphs, no more.
1. Why you're writing (who you are, what you're working on, why this specific person)
2. What you want (60-second feedback on your problem statement)
3. What you've attached (PDF of your problem statement)
4. Closing with explicit out ("if you can't respond, no worries")

**Don't:**
- Send the SOP as the email body
- Ask for "advice" (vague; nothing to respond to)
- Ask to "be your student" (premature; you haven't applied yet)
- Use formal salutations like "Dear esteemed Professor" (cringe)
- Include attachments larger than 2MB

### Recommender ask emails

See `applications/recommender_packets/ask_emails/` for templates per archetype. Key principles:
- Send 6 months before earliest deadline (May 2027)
- Include the explicit out ("if you can't write a strong letter, please tell me")
- Specify the time commitment (~20 letters across 3 months)
- Promise the packet (CV, draft SOP, accomplishments list) on confirmation

### Follow-up emails

See `applications/recommender_packets/followup_emails/` for the T-21 / T-7 / T-2 / escalation ladder.

Key principle: each follow-up is shorter and more specific than the last. The T-21 is informative; the T-7 is a reminder; the T-2 is a 5-line emergency; the escalation is a structured plea with extension-request templates.

---

## Writing for problem statements (Phase 1)

The 1-page problem statement is the hardest writing assignment in the entire 18-month plan because every word counts.

### The structure

The template in `docs/superpowers/plans/2026-05-24-phd-prep-phase-1-foundation.md` Task 10:
- Problem (3-4 sentences)
- Why this matters (2-3 sentences)
- Why agentic RAG is the right approach (2 sentences)
- Proposed approach (1 paragraph)
- Evaluation plan (1 paragraph)
- Risks (2-3 bullets)
- Timeline
- References

Total: ~500-600 words.

### The "concrete vs. abstract" test

Read each sentence. Is it concrete (you can point to a specific example) or abstract (could mean many things)?

Concrete examples:
- "Mata v. Avianca (S.D.N.Y. 2023) sanctioned two attorneys for citing six fabricated cases" — concrete
- "Open-weight legal RAG systems hallucinate at deployment-risk rates" — abstract until paired with a number

Abstract sentences are OK as framing; they shouldn't be the central claim of any paragraph.

### The "would I bet on this?" test

For each claim in the problem statement, ask: "would I bet money this is true?" If no, soften or remove.

Example:
- "All existing benchmarks score only final answers" — overstrong. There are exceptions.
- "Most existing benchmarks score only final answers" — accurate, defensible.

### Anti-pattern: framing without committing

A problem statement that lists 5 candidate approaches without picking one is not a problem statement; it's a survey. By M2 (Aug 31), pick one approach. Defend it.

---

## Writing for journal entries (all phases)

### The weekly retrospective

Every Sunday, write to `journal/weekly.md`:

```markdown
## Week of YYYY-MM-DD

### What went well
- ...

### What stalled
- ...

### Adjustment for next week
- ...

### Hours logged
- ...

### Mood / energy (1-10)
- ...
```

Keep it short. 5-10 minutes max. The point is the habit, not the artifact.

### Decision log entries

Every load-bearing decision goes in `journal/decisions.md`:

```markdown
| Date | Decision | Rationale | Reversible? |
|------|----------|-----------|-------------|
| 2026-XX-XX | [What you decided] | [Why; what alternatives you considered] | [Easy / Medium / Hard] |
```

Be verbose in rationale when the decision is hard to reverse. Be terse when it's easy.

---

## Writing under time pressure

Reality: you'll sometimes have to write fast. Tactics for high-quality fast writing:

### The 25-minute Pomodoro

Set a 25-minute timer. Write without editing. After 25 minutes, take a 5-minute break. Do 3-4 cycles.

In 100 focused minutes you can produce 1,500-2,500 words. Most papers are 5,000 words; that's 2-3 mornings of focused writing.

### The "talk it out" technique

If you can't write the section, record yourself talking through it for 5 minutes. Transcribe (Whisper, Otter, etc.). Edit the transcript into prose.

Spoken language is often clearer than written language; the editing-the-transcript approach can produce shockingly good first drafts.

### The "edit yesterday's prose first" warm-up

Open yesterday's writing. Edit it for 15 minutes. By the time you're done, you're warmed up to write today's section.

Don't open a blank page cold; always warm up on existing text first.

---

## Reading like a writer

The most underrated writing-improvement technique: read more, and read deliberately for style.

For each paper you read in Phase 1:
- Note one sentence you wish you had written
- Note one paragraph you found especially clear
- Note one transition that was elegant
- Try to copy the technique in your own writing the next day

After 50 papers, you'll have unconsciously absorbed dozens of stylistic patterns.

Recommended writing models (from a CS / NLP perspective):
- Andrej Karpathy's blog (clarity, vivid examples)
- Patrick Winston, *How to Speak* (MIT lecture; the underlying writing principles transfer)
- Strunk & White, *Elements of Style* (classic; still useful)
- William Zinsser, *On Writing Well* (chapters 1-7)

---

## When to stop writing

The opposite problem from blank-page paralysis: over-writing.

Signs you should stop and edit (or stop entirely):
- You've written >800 words on what should be a 400-word section
- You're explaining things the reader already knows
- You've used the word "moreover" more than twice in a section
- You're qualifying every claim with hedges ("might," "could," "potentially")

Cut ruthlessly. Most first drafts are 30% longer than they should be.

---

## A final note

Writing is the most learnable research skill. It's also the one most affected by daily practice. Skip a week, you regress; write daily, you compound.

If this entire document is too much: write 250 words a day. That's the only rule that matters. The rest is optimization.
