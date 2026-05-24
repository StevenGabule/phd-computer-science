# Artifacts Strategy — Closing the SOP Track-Record Gap

**Date:** 2026-05-25
**Why this exists:** The SOP narrative skeleton at `applications/sop_narrative_skeleton.md` contains an `[INSERT SPECIFIC ACCOMPLISHMENTS]` placeholder in paragraph 4 ("Background and preparation"). The agent who drafted that skeleton flagged honestly that without at least one concrete transferable artifact — a faithfulness-eval repo, an annotated legal corpus, a workshop paper, or a substantial open-source contribution — visible by August 2027, the gap between the ambitious CiteCheck vision and the demonstrated track record will be visible to top-tier admissions committees. The CiteCheck workshop paper is the *primary* artifact but, on the current Phase 2/3 timeline, will not be accepted (and may not even be submitted) before SOPs are written in September–November 2027. This document picks the bridging artifacts.

## The gap, concretely

Top-tier PhD admissions committees (Stanford, MIT, CMU, Princeton, UW, Edinburgh, ETH, Cambridge ILCC, Oxford) read SOPs for *evidence the applicant has done research*, not for promises that they will. The proof-of-research signals committees weigh are, roughly in order: (1) first-author publications at recognized venues; (2) co-authored publications; (3) preprints with serious empirical content; (4) substantial open-source contributions that other researchers depend on; (5) reproducible benchmarks or datasets with usage signals; (6) competition placements; (7) technical writing that demonstrates depth. Coursework, grades, and Master's thesis sit *below* this stack — they are admission-gating but not differentiating.

By SOP-writing time (September–November 2027), the user's research timeline says: Phase 2 (Sep 2026 – Apr 2027) builds the CiteCheck system; Phase 3 (May–Sep 2027) writes the workshop paper. NLLP@EMNLP 2027 review notifications historically land in October — *after* most US program deadlines (Dec 1 / Dec 15). TrustNLP@NAACL 2027 has a similar mid-fall cycle. Realistically, by the time SOPs are submitted, the user can claim: "I have built CiteCheck, released the benchmark on Hugging Face, posted a preprint on arXiv, and submitted to [venue]." That is good — but it is *one* artifact, all built in the year before applying, and the committee has no signal from before mid-2026 that the user was already doing research-quality work.

The bridging artifacts therefore need to do three jobs: (a) demonstrate the user was producing research output *before* the CiteCheck push, so the timeline reads as a sustained research trajectory rather than a one-year sprint; (b) prove specific transferable skills the CiteCheck pitch claims (reproducible evaluation, legal-NLP engineering, faithfulness measurement); (c) be discoverable by a committee member who Googles the applicant's name. Each artifact needs a public URL.

## Options surveyed

### Option 1: Open-source contribution to `eyecite` (or BlackstoneNLP / LexNLP)
- **One-line:** Submit 2–4 substantive PRs to the Free Law Project's `eyecite` citation parser, ideally adding a feature (e.g., a `verify_exists` mode that resolves parsed citations against CourtListener).
- **Effort:** 4–8 weeks of evenings/weekends; first PR within 3 weeks.
- **Visibility/CV-value:** **H** for the CiteCheck pitch specifically — `eyecite` is the legal-NLP community's default citation parser, RegLab uses it, and a maintainer co-sign on a PR is a discoverable third-party validation of the user's competence in the exact subdomain.
- **Risk of failure:** Low-medium. Free Law Project is responsive but PRs can sit. Mitigation: open an issue first, get maintainer buy-in on direction before coding.
- **Parallel with CiteCheck?** Yes — and better than parallel: it directly seeds CiteCheck's existence-axis tooling. Work done here is *not* extra work, it is Phase 2 prep.
- **First-week action:** Fork `freelawproject/eyecite`, read the contributing guide, file one well-scoped issue ("Add optional CourtListener-resolution mode for parsed citations") to test responsiveness before investing further.

### Option 2: Pre-CiteCheck mini-paper / standalone artifact: "Does this citation exist?" verifier
- **One-line:** Build and release a small standalone tool (Python package + HF Space demo) that takes a block of text, extracts case citations via `eyecite`, resolves each against the CourtListener API, and returns an existence verdict. Write it up as a 4–6 page tech report on arXiv.
- **Effort:** 8–12 weeks part-time (June–August 2026).
- **Visibility/CV-value:** **H**. An arXiv preprint with a working demo and a clean repo is the highest-bandwidth signal short of a peer-reviewed paper. It also de-risks CiteCheck's existence-axis: by the time Phase 2 starts, this component already works.
- **Risk of failure:** Medium. The honest risk is that the artifact is *too small* to be a "paper" and reads as a blog post in arXiv clothing. Mitigation: pair the tool with a small empirical study — e.g., run it on the outputs of GPT-4o, Claude, Llama 3.1, Mistral when asked to brief a US legal question, and report existence-failure rates by model. That makes it an empirical contribution, not just an engineering one.
- **Parallel with CiteCheck?** No — must be done *before* Phase 2 (Jun–Aug 2026) so it does not compete with the main system build.
- **First-week action:** Sketch the empirical study design in a one-page doc — exactly which models, exactly which prompts, exactly what counts as a citation, exactly what the eval metric is. The artifact succeeds or fails on the rigor of that one page.

### Option 3: Reproducibility report on a recent legal RAG paper
- **One-line:** Pick one recent legal-RAG paper (e.g., Reuter et al. 2025 on structured-aware chunking, or Pipitone & Houir Alami 2024 on LegalBench-RAG), reproduce its main results on a different model or a different jurisdictional subset, write a 6–8 page report, submit to ML Reproducibility Challenge or post to arXiv.
- **Effort:** 6–10 weeks part-time.
- **Visibility/CV-value:** **M**. The ML Reproducibility Challenge is a recognized venue but its prestige varies by committee member. Stronger signal: the report demonstrates the user can read a paper critically and execute someone else's experimental design — exactly the competence committees worry about in applied-AI applicants.
- **Risk of failure:** Medium-high. Reproducibility studies often fail to reproduce (which is interesting but harder to write up well), and dependency on the original authors' code/data can stall the project.
- **Parallel with CiteCheck?** Partially — overlaps in legal-NLP infrastructure but is a distinct empirical question. Could run in Sep–Dec 2026 alongside Phase 2's first months when system-building is in scaffolding mode.
- **First-week action:** Read three candidate target papers; pick the one whose code is most actually-runnable from a fresh clone. If none are, that itself is the project (and a harder paper to write).

### Option 4: Technical blog series on legal RAG (5–7 posts)
- **One-line:** Publish a substantive, code-backed blog series on Hugging Face Blog or a personal site: e.g., "What's actually hard about legal RAG, in seven parts" — each post ~2k words with a runnable notebook.
- **Effort:** 10–14 weeks at one post every 2 weeks.
- **Visibility/CV-value:** **M**. Blogs do not count as publications but the *right* blog series (technical depth, real code, real numbers) gets cited by other researchers and indexed on Twitter/Bluesky/HN, which a committee member may notice. The Hugging Face Blog is the highest-signal venue because it is editorially curated.
- **Risk of failure:** Low for completion, medium for impact. Blog posts that no one reads have near-zero CV value.
- **Parallel with CiteCheck?** Yes — and the posts can serially document the CiteCheck build itself, turning Phase 2 work into a public-facing artifact stream.
- **First-week action:** Pitch the series to the HuggingFace Blog editorial team with a one-paragraph proposal and a draft of post #1; do not start writing until they accept (or reject — in which case publish on a personal site).

### Option 5: Contribution to RAGAS or ARES adding legal-domain test cases
- **One-line:** Submit a PR to RAGAS or ARES (open-source RAG eval frameworks) adding a legal-domain test suite — faithfulness/context-precision metrics evaluated on a small legal QA set the user constructs.
- **Effort:** 4–6 weeks part-time.
- **Visibility/CV-value:** **M-H**. RAGAS in particular has serious adoption; a merged PR with a named contributor entry is a discoverable signal. Less specific to *legal* NLP than Option 1, but more specific to *evaluation methodology*, which is the part of CiteCheck the SOP foregrounds.
- **Risk of failure:** Medium. Maintainer responsiveness on busy OSS projects is unpredictable.
- **Parallel with CiteCheck?** Yes, and the test suite work is directly reusable in CiteCheck.
- **First-week action:** Open a discussion issue in the RAGAS repo proposing the legal test suite; gauge maintainer interest before building.

### Option 6: Workshop paper at a non-CiteCheck venue from existing Master's work
- **One-line:** If any Master's coursework or thesis-adjacent project has a publishable sub-result, write it up as a 4-page workshop paper and submit to a venue with a *spring 2027* deadline (so acceptance lands before SOP-writing).
- **Effort:** 6–10 weeks depending on how much novel work is needed on top of existing material.
- **Visibility/CV-value:** **H** if accepted; **M** if posted as preprint only. An accepted workshop paper is the single highest-signal artifact on this list.
- **Risk of failure:** High — depends entirely on whether the existing Master's work has a publishable result. The user knows this better than I do.
- **Parallel with CiteCheck?** Yes, ideally written in Sep–Dec 2026 for a spring deadline.
- **First-week action:** Spend two hours writing a one-page "is there a paper here?" memo on the strongest piece of existing Master's work. If the answer is no, skip this option. Do not force it.

### Option 7: Kaggle / shared-task placement in a legal-NLP competition
- **One-line:** Enter a legal-NLP shared task (COLIEE, SemEval legal tracks, or a Kaggle competition if one runs in the window) and aim for a top-10 placement.
- **Effort:** 6–8 weeks during the competition window.
- **Visibility/CV-value:** **M**. A top-3 placement is high-signal; a top-30 placement is decorative. The committee reads "placed 27th of 412" as approximately equivalent to "competed".
- **Risk of failure:** High — placement is by definition not under the user's control, and no qualifying competition may run in the Jun 2026 – Aug 2027 window.
- **Parallel with CiteCheck?** Only at gaps; shared tasks are 6–8 weeks of evening intensity.
- **First-week action:** Check COLIEE 2027 dates (typically announced summer 2026) and Kaggle's legal-AI listings; defer commitment until a competition with a winnable structure exists.

## Recommended commitments

The user should commit to **Option 2** (pre-CiteCheck mini-paper) and **Option 1** (eyecite contributions), with **Option 4** (blog series) as an opportunistic third if Phase 2 has slack. Calendar:

- **Option 2: Citation-existence verifier + empirical study + arXiv tech report.** Start June 1, 2026; arXiv post by September 15, 2026. Two months of build (Jun–Jul), one month of write-up (Aug), buffer week. This is the single most leveraged artifact: it is high-visibility, it directly de-risks CiteCheck's existence axis, it produces a citable preprint, and it is finishable in the pre-Phase-2 window without competing with the main research.

- **Option 1: `eyecite` contributions (2–4 merged PRs).** Start June 15, 2026 (issue-filing) in parallel with Option 2; aim for first PR merged by August 1, 2026 and 3–4 PRs merged by March 2027. The work is naturally interleaved with Option 2 (the verifier *uses* `eyecite`) and with Phase 2 (CiteCheck *uses* `eyecite`), so marginal cost is near zero. Maintainer recognition is the rare CV signal that comes from real community engagement rather than self-published work.

- **Option 4 (conditional): HuggingFace blog series, 3 posts not 7.** Start January 2027 if Phase 2 is on schedule; skip if not. Three posts at ~2k words each is finishable in 6 weeks of evenings and turns Phase 2 work into a public-facing stream. Drop this immediately if Phase 2 slips — the workshop paper takes priority over blog visibility.

Why these and not the others: Option 3 (reproducibility report) is good work but its CV-value is moderate and it does not specifically build CiteCheck infrastructure. Option 5 (RAGAS PR) is similar — useful, but Option 1 dominates it for this specific SOP because `eyecite` is *the* legal-NLP citation library and the recognition is more domain-targeted. Option 6 (workshop paper from existing work) should be pursued *only if* the user has an existing result with a clear paper in it; otherwise it is wishful thinking and forced retrofitting hurts the work. Option 7 (Kaggle) is too risk-bound on external timing.

Total effort: ~16 weeks of evenings/weekends for Options 1+2, fully contained in Jun–Sep 2026 before Phase 2 starts. Marginal load during Phase 2 is small (PR follow-ups, optional blog posts).

## Template: "[INSERT SPECIFIC ACCOMPLISHMENTS]" replacement

The following paragraph fits in paragraph 4 of the SOP skeleton. Fill bracketed slots based on which artifacts complete by Aug 2027:

> "My recent work has focused on the engineering primitives that CiteCheck depends on. In `[summer/fall 2026]`, I released `[name of citation-verifier tool]` — a Python package and Hugging Face Space that resolves AI-generated case citations against CourtListener, paired with an empirical study showing that `[N]`% of citations produced by `[model family]` when prompted for US legal briefs fail existence verification. The tech report is on arXiv (`[arXiv ID]`) and the tool has `[N stars / N downloads]` as of `[date]`. I have also contributed `[N]` merged pull requests to `eyecite`, the Free Law Project's open-source citation parser used by the Stanford RegLab evaluations referenced above, including `[one specific feature, e.g., 'an extension that returns structured CourtListener-resolution metadata alongside parsed citations']`. `[Optional third sentence: If blog series completed: 'I have documented the design decisions in a three-part technical series on the Hugging Face Blog (links in CV).' If workshop paper accepted/submitted by SOP date: 'A workshop submission extending this benchmark to the full three-axis CiteCheck evaluation is under review at NLLP@EMNLP 2027.']` This thread of work — citation parsing, resolution infrastructure, faithfulness measurement on legal text — is precisely what CiteCheck scales up, and it is what I would continue with a doctoral advisor."

Variants for partial completion:

- **If only Option 2 completes:** Drop the eyecite sentence; expand the empirical-study sentence with one additional specific finding.
- **If only Option 1 completes:** Lead with eyecite contributions; describe the citation-verifier as "a prototype I built in summer 2026, now folded into the broader CiteCheck system."
- **If neither completes:** Lean harder on Master's thesis + one specific course project, and accept that the SOP will be weaker. Do not fabricate.

## How much does this matter?

Honestly: less than the user's anxiety probably suggests, but more than zero. Admissions outcomes at top-10 programs are dominated by (a) strong letters from researchers the admissions committee knows or trusts, (b) a research vision that is *specific and tractable* rather than ambitious-and-vague, and (c) signals that the applicant can actually execute. The CiteCheck pitch already does (b) well. The artifacts in this document address (c). They cannot manufacture (a) — that is what the user's existing advisor relationships and the CiteCheck collaborations during Phase 2 are for.

Quantitatively, my honest estimate: a candidate with the CiteCheck vision, two strong letters, a Master's degree, and *zero* bridging artifacts has a non-trivial but uncertain shot at top-10 programs — they read as someone with a plan but no evidence they can execute it, and admissions committees discount plans. The same candidate with Options 1+2 completed reads as someone who has *already started* the doctoral research and just wants institutional support to scale it — a meaningfully different and stronger position. The marginal value of the third artifact (Option 4 blog series) is small and probably not worth the time if Phase 2 is under pressure. The marginal value of Options 1+2 is, in my estimate, the difference between "interesting candidate the committee debates" and "obvious admit the committee fights for." That estimate is not a guarantee — admissions is stochastic and committee composition varies — but it is the honest framing of why this investment is worth ~16 weeks of pre-Phase-2 time.
