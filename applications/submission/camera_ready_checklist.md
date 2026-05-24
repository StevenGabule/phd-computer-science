# Camera-Ready Checklist — CiteCheck Workshop Paper

**Purpose:** What to do between workshop acceptance notification (~late Oct 2027 for NLLP @ EMNLP) and camera-ready deadline (~mid Nov 2027).
**Lead time:** ~3 weeks. Don't leave to the last weekend.

---

## Phase 1 — Triage (within 48 hours of acceptance)

- [ ] Read the acceptance email end-to-end, including any conditional acceptance notes
- [ ] Note the camera-ready deadline (exact date, time, timezone)
- [ ] Note the page-limit policy for camera-ready (usually 1 extra page over submission limit, e.g., 8+1 → 9 pages of content + unlimited refs/appendix)
- [ ] Note any required additional sections (e.g., NLLP usually requires an Ethics Statement; some workshops require a Reproducibility Checklist)
- [ ] Check whether the workshop uses OpenReview, SoftConf, or another submission platform
- [ ] Note the format requirements (single-blind, double-blind for the camera-ready, whatever the workshop specifies)

## Phase 2 — Reviewer Response Integration (week 1)

- [ ] Read all reviews carefully; categorize comments:
  - **Must-fix** (factual errors, missing experiments the reviewer flagged as required)
  - **Should-address** (clarifications, additional context the reviewer requested)
  - **Acknowledge but won't fix** (out-of-scope, defer to future work)
- [ ] For each must-fix: integrate the change in `main.tex`. Mark each change with a comment so it's traceable: `% R1.3: addressed reviewer 1 comment 3`
- [ ] For each should-address: integrate or write a 1-paragraph justification for the rebuttal (some workshops have a discussion phase between acceptance and camera-ready)
- [ ] If a reviewer flagged a missing experiment that you cannot run in the camera-ready window: write a 1-paragraph "limitations" note explicitly acknowledging it and committing to follow-up work
- [ ] Write the response document if the workshop requires one (3-page max for most)

## Phase 3 — De-anonymization (week 1)

If the original submission was anonymous (most are):

- [ ] Add author block to title: name, ORCID, email, affiliation
- [ ] Restore acknowledgments section (advisors, collaborators, funders, reviewers — many drafts omit this entirely during anonymous review)
- [ ] Restore self-citations: change all "Anonymous (under review)" or "[redacted]" to actual citations
- [ ] Restore code/data links in the abstract, intro, conclusion
- [ ] Restore footnotes that pointed to author institution, dataset URL, etc.
- [ ] Search the source for leftover anonymization markers: `grep -rn "anonymous\|redacted\|XXX\|\\todo" *.tex`
- [ ] Search PDF metadata: anonymization sometimes leaves identifying info in PDF properties. After final PDF compile, run `pdfinfo main.pdf` and verify Author / Producer fields are correct

## Phase 4 — Acknowledgments Section (week 2)

Include thanks to:
- Advisor(s) — if applicable
- Funders — if any (e.g., NSF GRFP, university research credits, cloud credits from a vendor program)
- Anonymous reviewers ("We thank the anonymous reviewers for their constructive feedback...")
- Specific people who helped: paper-swap partners, annotators, anyone who reviewed drafts
- Open-source projects relied on: pyserini, eyecite, transformers, etc. (one sentence covering them all)

Format: standard `\section*{Acknowledgments}` (or `\section*{Acknowledgements}` — match what the conference style file uses).

Length: 1 paragraph, ~80-150 words. Don't pad.

## Phase 5 — Page Limit (week 2)

NLLP @ EMNLP workshop typically: 8 pages main + unlimited refs + appendix. Camera-ready may extend to 9 pages.

- [ ] Compile and check page count
- [ ] If over limit: tighten before cutting content. Common wins:
  - Remove redundant sentences in intro/conclusion
  - Tighten table captions
  - Move 1-2 ablations to appendix
  - Reduce inter-sentence spacing in tight paragraphs (carefully — don't break formatting)
- [ ] If under limit: don't artificially pad; use the space for clearer figures or more discussion only if it improves the paper

## Phase 6 — BibTeX Cleanup (week 2)

- [ ] Verify every cited paper has a DOI or arXiv URL in the `.bib` entry
- [ ] No `\bibitem` placeholders or `??` markers
- [ ] Author names rendered correctly (especially non-ASCII characters — `\v{S}avelka` for Šavelka)
- [ ] Conference / journal names consistent (e.g., "EMNLP" not "Empirical Methods in Natural Language Processing" — match the conference convention)
- [ ] Year format consistent
- [ ] Verify all hyperref links in the PDF resolve (click-test each)

## Phase 7 — Figures & Tables (week 2)

- [ ] Figures embedded as PDF (vector) where possible, not PNG (raster)
- [ ] Every figure resolves at 300 DPI when printed
- [ ] Figure captions tell a complete story (so the figure is interpretable without reading the surrounding text)
- [ ] Tables have horizontal rules in standard ACL/EMNLP style (top, mid, bottom — use `\toprule`, `\midrule`, `\bottomrule` from `booktabs`)
- [ ] Table cells aligned (decimal alignment for numbers via `siunitx` or manual `\phantom{.}` if needed)
- [ ] No table overflows the column / page width

## Phase 8 — Ethics & Reproducibility (week 2)

NLLP / TrustNLP / most legal-AI venues require an explicit Ethics Statement. Cover:
- Potential dual-use of the benchmark (could be used to train better fabricators)
- License terms (CC BY 4.0 for code, CC BY-NC for the benchmark if you went that direction)
- Annotator compensation and IRB status (if you hired an annotator: "annotators were paid at $X/hour above [city] minimum wage; no IRB review required because annotation was not on human subjects")
- Data sourcing (CAP and CourtListener are both public domain / public APIs; no consent issues)

Reproducibility Checklist (use the ACL standard if available):
- Code released? Y, with URL
- Data released? Y, with URL and DOI (via Zenodo)
- Environment / dependencies pinned? Y, in `pyproject.toml`
- Hyperparameters in paper or appendix? Y
- Random seeds documented? Y
- Expected runtime + hardware? Y

## Phase 9 — arXiv v2 (week 3)

If a v1 was posted simultaneously with submission (see `arxiv_prep_guide.md`):

- [ ] After camera-ready PDF is finalized, replace the v1 on arXiv with v2
- [ ] Update arXiv "Comments" field: "Camera-ready version; accepted at NLLP @ EMNLP 2027"
- [ ] Verify v2 is the camera-ready PDF (not the submission version)

## Phase 10 — Code + Dataset Release (week 3)

- [ ] Tag a GitHub release: `git tag v0.1.0-paper && git push --tags`
- [ ] Update `citecheck/README.md` with the paper citation (BibTeX entry) at the top
- [ ] Mirror dataset to Hugging Face Hub with a complete data card (Description, Source, Intended Use, Limitations, License, Citation)
- [ ] Get a Zenodo DOI for the dataset (Hugging Face → Zenodo integration is one-click)
- [ ] Update the paper's data/code URL to use the released versioned URLs (not master branch links)

## Phase 11 — Submission Upload (week 3, day of deadline -2)

- [ ] Log in to the workshop submission platform 24+ hours before the deadline
- [ ] Upload the camera-ready PDF
- [ ] Upload the response document (if required)
- [ ] Verify the system says "Submitted" — screenshot the confirmation
- [ ] Email the program chairs if anything is unclear (don't wait until the last minute)
- [ ] If a co-author is on the submission, confirm they have access to the platform

## Phase 12 — Post-submission (rest of week 3)

- [ ] Update `journal/decisions.md` with the submission confirmation
- [ ] Update CV with the accepted paper
- [ ] Update `outreach/log.md` if any recommender or advisor should be informed
- [ ] Update applications already in flight: if SOPs reference the workshop submission, update to "accepted at NLLP @ EMNLP 2027"
- [ ] Plan for the conference itself (poster vs. talk, travel, slides)

---

## Common gotchas

- **PDF anonymization residue.** Even after removing names from the text, the PDF metadata can still have your name. Run `pdfinfo main.pdf` and verify.
- **Style-file version mismatches.** The submission version's `acl.sty` may have changed by camera-ready time. Re-download the latest from https://github.com/acl-org/acl-style-files.
- **Footnote on first page.** Some workshops require an "authors contributed equally" or affiliation footnote — these have specific format requirements.
- **Hyperref color.** Default `\hypersetup{colorlinks=true}` makes links blue; the conference style may prefer black `colorlinks=false, hidelinks`. Verify.
- **Bibliography style.** EMNLP uses `acl_natbib`; ACL uses `acl_natbib`; check the style file's `.bst` and match.
- **Page numbers.** Some venues require page numbers for camera-ready submission (even if the published version drops them). Verify.

## Documentation

After camera-ready submission, log in `journal/decisions.md`:

```markdown
| 2027-XX-XX | Camera-ready submitted to NLLP @ EMNLP 2027 | All R1/R2/R3 must-fixes addressed; v2 also on arXiv | No — published version is final |
```
