# arXiv Prep Guide — CiteCheck Preprint Submission

**Purpose:** Step-by-step guide for posting the CiteCheck preprint to arXiv simultaneously with the workshop submission (Phase 3 Task 56, target Sep 2027).
**Use when:** Paper draft is finalized (Phase 3 Task 53) and the LaTeX source compiles cleanly.

---

## 1. arXiv categories

**Primary:** `cs.CL` (Computation and Language)

**Cross-list (in order of relevance):**
- `cs.LG` (Machine Learning) — for the reranker training + agent loop methodology
- `cs.IR` (Information Retrieval) — for the hybrid BM25 + dense + RRF architecture
- `cs.CY` (Computers and Society) — optional, for the access-to-justice / legal-tech framing

**How to set in submission form:** arXiv asks "Subject" — type `cs.CL` for primary. Then in "Cross-list categories" add the others comma-separated.

## 2. Endorsement (first arXiv submission only)

If this is your first arXiv submission, you need an endorsement from someone with at least one prior `cs.CL` arXiv post.

**Process:**
- Click "Get endorsed" on arXiv after creating the account.
- Generates an endorsement code to share with a potential endorser.
- Email the code to a co-author (if any), advisor, or any cs.CL-active researcher you know personally. Common asks: master's advisor, course professor, collaborator from the citation-verifier mini-paper.
- They click the endorsement link and approve. Takes <5 min on their side.

**If you don't have an endorser:**
- Co-author with someone who does (best path).
- Email a cs.CL author whose paper you cited directly — many will endorse a one-time submission for a polite ask with a paper draft attached.
- Last resort: post on r/MachineLearning or the ACL Slack #arxiv-endorsement channel.

**Lead time:** Plan 1-2 weeks before submission to secure endorsement.

## 3. File requirements

arXiv accepts:
- **Source TeX upload (preferred):** zip the entire `docs/papers/latex/` directory. arXiv re-compiles to PDF on their end, which catches a class of formatting issues.
- **PDF-only upload (fallback):** if TeX source fails to compile on arXiv's processor (common with custom .sty files).

**Required files in the zip (TeX source path):**
```
main.tex
references.bib
acl.sty           (or whatever style file you use — bundle it; do not assume arXiv has it)
figures/*.pdf     (PDF figures embed cleanly; avoid .eps)
```

**Ancillary files:**
- Benchmark dataset card (`citecheck_v0.1_datacard.pdf`) — flag as "ancillary" upload type.
- Code release pointer (URL to Hugging Face Hub + GitHub) — goes in the abstract or a footnote, not as an ancillary file.

**arXiv won't accept:**
- Word documents
- Files >10 MB without explicit reason
- Source files with `\usepackage{minted}` (requires shell-escape — arXiv compile fails)

## 4. License selection

**Recommended:** `CC BY 4.0` (Creative Commons Attribution).

**Trade-offs:**
- `CC BY 4.0` — anyone can copy, modify, redistribute with attribution. Maximum reach; matches the open-source ethos of CiteCheck.
- `CC BY-NC 4.0` — same but no commercial use. Adds friction for legal-tech companies that might want to build on CiteCheck. Probably wrong for this work.
- `arXiv perpetual non-exclusive license` (default) — least restrictive for arXiv but most restrictive for re-use. Avoid; the whole point of CiteCheck is reproducibility.

**Set during the submission form:** "License" dropdown. Confirm before final submit; license cannot be changed retroactively.

## 5. Title, abstract, author formatting

**Title:**
- Max 240 characters.
- Current draft: "CiteCheck: An Open Benchmark and Agentic Method for Verifiable US Case-Law Citations" — 88 characters, well within limit.

**Abstract:**
- Plain text, no LaTeX commands (or arXiv strips them).
- 1,500-1,920 character target (arXiv hard cap ~1,920).
- Lead with the result: "We introduce CiteCheck..."; close with the data/code release line.
- Don't include affiliations or contact info — those go in the author block.

**Authors:**
- First/last name format: "John Paul L. Gabule"
- ORCID: register at https://orcid.org if you don't have one (free, 5 min). Add the ORCID URL in the author metadata.
- Affiliation: if no academic affiliation yet, use the most accurate descriptor. Acceptable: "Independent researcher" or "[Master's institution] (alum)". Avoid leaving blank.
- Email: include in the LaTeX author block (will be redacted on the public arXiv page but visible in source).

## 6. Comments field

arXiv has a "Comments" field that appears at the top of the public listing. Use it for:
- Submission status: "Submitted to NLLP @ EMNLP 2027 (under review)"
- Page count: "12 pages, 4 figures, 6 tables, plus appendices"
- Code/data pointer: "Code: https://github.com/StevenGabule/citecheck; Data: https://huggingface.co/datasets/[user]/citecheck-v0.1"

Update the comments field when:
- The paper is accepted ("Accepted at NLLP @ EMNLP 2027")
- A v2 is posted (camera-ready: "Camera-ready version; minor revisions from v1")

## 7. CLI submission (optional, scripted)

If you prefer scripting:

```bash
pip install arxiv-cli  # community tool; verify exists in 2027
arxiv submit \
  --category cs.CL \
  --cross-list cs.LG,cs.IR \
  --license CC-BY-4.0 \
  --comments "Submitted to NLLP @ EMNLP 2027. Code+data: github.com/StevenGabule/citecheck" \
  --source main.tex.tar.gz
```

If `arxiv-cli` is unavailable or unreliable, use the web form. It is more reliable than the API and the user experience is fine.

## 8. Common rejection reasons (and fixes)

| Reason | Fix |
|---|---|
| Font subsetting missing | Recompile with `pdflatex` + ensure `\usepackage[T1]{fontenc}` and `\usepackage{lmodern}` |
| Bibliography fails to compile | Run `bibtex main` locally first; ensure all `.bbl` and `.bib` are in the upload |
| Missing `.sty` files | Bundle them in the source zip; do not rely on arXiv having ACL/EMNLP style files |
| PDF >5 MB | Compress figures (PDF/X-3 settings) or move some figures to ancillary uploads |
| Encoding errors | Save all source files as UTF-8; avoid stray non-ASCII characters in names |
| Broken `\ref{}` / `\cite{}` | Compile locally, ensure no `??` markers; arXiv compiles once and won't fix mid-document refs |

## 9. Pre-submission checklist

Before clicking "Submit":

- [ ] `main.tex` compiles cleanly with `latexmk -pdf main.tex` (zero errors, zero warnings)
- [ ] All `\todo{}` markers resolved (search the source: `grep -r "\\todo" .`)
- [ ] All `<TBD>` placeholders filled with real numbers (search: `grep -r "<TBD>" .`)
- [ ] References compile (no `[??]` in the rendered PDF)
- [ ] Figures embed cleanly (open the PDF; verify each figure renders)
- [ ] Tables render at intended width (no horizontal overflow)
- [ ] Author block has ORCID
- [ ] Abstract is under 1,920 characters
- [ ] License decided (CC BY 4.0 recommended)
- [ ] Endorsement secured (if first arXiv submission)
- [ ] Comments field text drafted
- [ ] Code repo public + tagged with `v0.1.0-paper` release
- [ ] Dataset card uploaded to Hugging Face Hub with stable DOI (use Zenodo integration)
- [ ] arXiv submission window is open (arXiv has a 5-day moderation period — submit at least 1 week before any deadline)

## 10. Withdrawal / replacement (post-submission)

If the camera-ready version differs from the v1 preprint:

- arXiv supports versioning. Submit camera-ready as v2 via the "Replace" link on your paper's arXiv page.
- v2 should be uploaded within 1-2 weeks of receiving camera-ready notification.
- Update the "Comments" field to "Camera-ready version; accepted at NLLP @ EMNLP 2027" when v2 lands.

If the paper is rejected and you want to withdraw:
- arXiv discourages withdrawal except in cases of error. The paper stays in the archive even if rejected from the conference.
- Update the Comments field to reflect new submission status if you re-submit to a different venue.

---

## Timing relative to workshop submission

Best practice: post arXiv v1 **the same day** as workshop submission. Reasons:
- Establishes priority.
- Lets the reviewing community discover the work.
- Some venues require you to declare any arXiv version in the submission portal — disclose at submission time, not after.

Workshop deadlines for NLLP @ EMNLP 2027: typically Jun-Jul 2027 (verify when CFP publishes). Plan arXiv submission for the same week.

## Documentation

After successful submission, log in `journal/decisions.md`:

```markdown
| 2027-XX-XX | arXiv preprint submitted: https://arxiv.org/abs/XXXX.XXXXX | CiteCheck v0.1 preprint live; matches workshop submission to NLLP @ EMNLP 2027 | Difficult — replacement requires re-upload |
```
