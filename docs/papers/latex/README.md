# CiteCheck Paper LaTeX Source

**Target venue:** NLLP @ EMNLP 2027 (primary) / TrustNLP @ EMNLP 2027 (backup)
**Status:** v0.1 skeleton (2026-05-25) — compile-safe scaffold with `<TBD>` placeholders for Phase 2 results.

---

## Build

```bash
# install dependencies (one-time)
# Ubuntu/Debian: apt install texlive-full latexmk
# macOS:         brew install --cask mactex && brew install latexmk
# Windows:       install MiKTeX or TeX Live + Strawberry Perl

# build the PDF
make pdf

# rebuild on save
make watch

# word count
make wordcount

# clean build artifacts
make clean
```

Output: `main.pdf`

## ACL style files

The paper uses the official ACL LaTeX style. Download from:
https://github.com/acl-org/acl-style-files

Place `acl.sty` in this directory alongside `main.tex` before building. (NOT included in this repo to avoid bundling third-party code; user fetches at build time.)

## What's in this skeleton

- `main.tex` — full paper structure with draft prose where the literature supports it, `<TBD>` placeholders for numeric results, `\todo{}` markers for writing gaps
- `references.bib` — BibTeX entries for all ~30+ citations from `docs/papers/citecheck_outline.md`
- `figures/.gitkeep` — placeholder; real figures land in Phase 3 Task 42
- `Makefile` — common build targets

## What needs filling in during Phase 3

**Result placeholders (`<TBD>` markers):**
- Table 1 (headline metrics across all systems)
- Table 2 (per-axis breakdown)
- Table 3 (per-jurisdiction breakdown)
- Table 4 (ablations)
- Table 5 (cost analysis: latency + tokens)
- Table 6 (human audit results)

**Writing gaps (`\todo{}` markers):**
- Acknowledgments (Phase 3 Task 53)
- Final paragraph of Discussion (depends on real results)
- Appendix tables (extended versions of Tables 2 and 3)

**Figure placeholders:**
- Figure 1: Architecture diagram (use the data-flow diagram from `citecheck/docs/architecture.md` as the basis)
- Figure 2: Calibration / λ-selection plot
- Figure 3: Per-jurisdiction bars
- Figure 4: Ablation waterfall

## Workflow for Phase 3

1. **May 2027:** Replace each `<TBD>` cell with a real number from Phase 2 results JSONLs (`citecheck/runs/`)
2. **Jun 2027:** Tighten the Methods + Results sections; remove any prose that conflicts with what the results actually show
3. **Jul 2027:** Write the Discussion section based on what actually beat the baselines
4. **Aug 2027:** Final polish per `applications/submission/camera_ready_checklist.md`
5. **Aug-Sep 2027:** Submit via the workshop platform; post arXiv preprint per `applications/submission/arxiv_prep_guide.md`

## Overleaf upload

If preferring Overleaf to local build:
1. Create a new Overleaf project from upload
2. Upload `main.tex`, `references.bib`, the `acl.sty` style file, and the `figures/` directory
3. Set the compiler to pdfLaTeX
4. Set the main document to `main.tex`
5. Compile

Overleaf is recommended for the Phase 3 collaborative review pass (Task 50) — easier to share with paper-swap readers than a local-build flow.
