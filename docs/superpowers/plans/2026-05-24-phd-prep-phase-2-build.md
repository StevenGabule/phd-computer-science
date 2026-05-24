# PhD Prep — Phase 2 (Build) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the CiteCheck system (hybrid retrieve → faithfulness-tuned rerank → agent verify) end-to-end across Sep 2026 – Apr 2027, reproduce 3–5 baselines (M3, Nov 2026), prototype and validate the novel reranker + CitationResolver (M4, Feb 2027), and complete full evaluation on a ~500-item legal QA set with ablations and stability checks (early M5, May 2027 — partial in Apr).

**Architecture:** CiteCheck is a 3-stage agentic-RAG pipeline over US case-law: (1) hybrid BM25 + dense (BGE-legal) retrieval over a local Caselaw Access Project (CAP) index, augmented by live CourtListener API lookups; (2) a cross-encoder reranker fine-tuned with a multi-objective loss combining standard relevance with a Bluebook-structure-aware citation-grounding signal (parsed via `eyecite`); (3) a constrained-decoding citation grammar paired with a `CitationResolver` tool — the LLM emits well-formed citations, the tool resolves them against CAP + CourtListener, and unresolvable / non-entailing citations trigger retraction or re-retrieval up to `k` iterations. Implementation is solo, single 24GB GPU, Colab Pro for bursts, with QLoRA fine-tuning only (no base-model pre-training).

**Tech Stack:**
- Python 3.11, PyTorch 2.4+, CUDA 12.x
- `transformers` 4.45+, `peft` 0.12+, `trl` 0.11+, `bitsandbytes` 0.43+
- `sentence-transformers` 3.0+, `BAAI/bge-base-en-v1.5` (and `nlpaueb/legal-bert-base-uncased` for legal-tuned encoders)
- `pyserini` 0.24+ for BM25 indexing (Anserini Lucene backend)
- `eyecite` 2.6+ for Bluebook citation parsing (CourtListener team)
- `langchain-core` 0.3+ or direct orchestration (no LangChain agents — too heavy)
- `outlines` 0.1+ or `guidance` 0.2+ for constrained decoding
- `datasets` 3.0+, `huggingface-hub`, `wandb` (free tier) for run tracking
- Llama-3.1-8B-Instruct as primary backbone; Qwen2.5-7B-Instruct as secondary
- CourtListener REST API (free, rate-limited 5,000 req/hr with token)
- CAP bulk download (~100GB, public domain, S3-hosted)

---

## File Structure

All paths relative to `C:\Users\John Paul L. Gabule\Desktop\phd-computer-science`.

```
citecheck/
  README.md
  pyproject.toml                  # dependencies, version pins
  .env.example                    # CL_API_KEY, WANDB_API_KEY, HF_TOKEN
  src/citecheck/
    __init__.py
    config.py                     # paths, model names, hyperparameters
    data/
      cap_loader.py               # CAP bulk download + parquet conversion
      cl_client.py                # CourtListener API client + disk cache
      benchmarks.py               # LegalBench-RAG, CUAD loaders
      eval_set.py                 # the 500-item question/gold-citation set
    retrieval/
      bm25_index.py               # Pyserini wrapper
      dense_index.py              # BGE-legal FAISS index
      hybrid.py                   # reciprocal rank fusion
    rerank/
      cross_encoder.py            # base cross-encoder eval harness
      train_reranker.py           # QLoRA fine-tune with multi-objective loss
      grounding_signal.py         # eyecite-derived structure signal
    agent/
      citation_grammar.py         # outlines/guidance grammar for citations
      citation_resolver.py        # tool: resolve citation → CAP/CL
      verify_loop.py              # k-iteration retract / re-retrieve loop
      citecheck.py                # end-to-end orchestration
    eval/
      metrics.py                  # CRR, CSF1, JV, FabR, Likert harness
      nli_judge.py                # NLI-based support scoring
      run_eval.py                 # batch evaluation runner
  baselines/
    vanilla_llama.py
    naive_rag.py
    self_rag.py                   # Asai et al. 2024 reimpl
    crag.py                       # Yan et al. 2024 reimpl
    el_rag.py                     # Wankhade 2026 reimpl (or stub)
    hallugraph_posthoc.py         # post-hoc detector
    gpt4o_websearch.py            # ceiling baseline (API)
  scripts/
    download_cap.sh / .ps1
    build_bm25_index.py
    build_dense_index.py
    prelabel_eval_set.py          # LLM pre-labeling pass
    run_all_baselines.py
    run_citecheck.py
    run_ablations.py
  data/                           # gitignored; large artifacts
    cap_raw/                      # ~100GB
    cap_parquet/                  # processed
    cl_cache/                     # CourtListener response cache
    indices/
      bm25/
      dense/
    eval/
      eval_set_v1.jsonl           # 500-item set (M4 deliverable)
      audit_subset_v1.jsonl       # 200-item human-audit subset (M5)
  experiments/
    runs/                         # per-run output dirs (results.json, log.txt)
    ablations/
    seeds/
  notebooks/
    01_cap_exploration.ipynb
    02_eyecite_smoke.ipynb
    03_pilot_50q.ipynb
  paper/
    outline.md                    # M5 partial deliverable
    figures/
journal/                          # extends Phase 1 journal
  weekly.md                       # continue weekly entries
  decisions.md                    # continue decision log
  phase2_retros.md                # M3, M4, M5-partial retrospectives
```

---

## Pre-work — Week 0 (last week of Aug 2026, immediately after M2)

This is a small kickoff block run during the gap between Phase 1 closeout and Sep 1 — it sets up only the directory tree and pulls down the locked problem statement for reference. Heavy lifting starts at Task 15.

- [ ] **Step 1: Create the `citecheck/` directory tree**

```powershell
New-Item -ItemType Directory -Force `
  citecheck\src\citecheck\data, `
  citecheck\src\citecheck\retrieval, `
  citecheck\src\citecheck\rerank, `
  citecheck\src\citecheck\agent, `
  citecheck\src\citecheck\eval, `
  citecheck\baselines, citecheck\scripts, `
  citecheck\data\cap_raw, citecheck\data\cap_parquet, citecheck\data\cl_cache, `
  citecheck\data\indices\bm25, citecheck\data\indices\dense, citecheck\data\eval, `
  citecheck\experiments\runs, citecheck\experiments\ablations, citecheck\experiments\seeds, `
  citecheck\notebooks, citecheck\paper\figures | Out-Null
```

Verify: `Test-Path citecheck\src\citecheck\agent` returns `True`.

- [ ] **Step 2: Copy the locked problem statement into the project as a reference**

```powershell
Copy-Item project\problem_statement.md citecheck\paper\problem_statement_v1.md
```

- [ ] **Step 3: Create `journal/phase2_retros.md` with section headers for M3, M4, M5-partial**

- [ ] **Step 4: Log Week 0 in `journal/weekly.md` (week of 2026-08-31)**

---

## Month 1 — September 2026: Infrastructure

Compute budget for the month: ~10 GPU-hours (mostly smoke tests on small slices). Bandwidth: ~120GB download (CAP + model weights). Storage: provision ≥250GB free disk before starting Task 16.

### Task 15: Set up project repo, Python environment, and dependencies

**Artifacts:**
- Create: `citecheck/pyproject.toml`
- Create: `citecheck/README.md`
- Create: `citecheck/.env.example`
- Create: `citecheck/src/citecheck/config.py`
- Create: a working conda/venv environment, `citecheck-py311`

- [ ] **Step 1: Install Miniconda (if not already) and create environment**

```powershell
conda create -n citecheck-py311 python=3.11 -y
conda activate citecheck-py311
```

- [ ] **Step 2: Write `citecheck/pyproject.toml`**

Minimum content:

```toml
[project]
name = "citecheck"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
  "torch>=2.4.0",
  "transformers>=4.45.0",
  "peft>=0.12.0",
  "trl>=0.11.0",
  "bitsandbytes>=0.43.0",
  "accelerate>=0.34.0",
  "sentence-transformers>=3.0.0",
  "datasets>=3.0.0",
  "huggingface-hub>=0.25.0",
  "pyserini>=0.24.0",
  "faiss-cpu>=1.8.0",           # use faiss-gpu if CUDA build available
  "eyecite>=2.6.0",
  "outlines>=0.1.0",
  "wandb",
  "python-dotenv",
  "tqdm",
  "rich",
  "pydantic>=2.0",
  "requests",
  "tenacity",
  "pandas",
  "pyarrow",
]
```

Install: `pip install -e citecheck/`.

- [ ] **Step 3: Install PyTorch + CUDA wheels matching your GPU**

For CUDA 12.1: `pip install torch --index-url https://download.pytorch.org/whl/cu121`. Verify: `python -c "import torch; print(torch.cuda.is_available(), torch.cuda.get_device_name(0))"` returns `True` and your GPU name.

- [ ] **Step 4: Install Java 21 (required by Pyserini's Anserini backend)**

`winget install Microsoft.OpenJDK.21` or download from Adoptium. Set `JAVA_HOME` env var. Verify: `java --version` reports 21.

- [ ] **Step 5: Create `citecheck/.env.example`**

```
HF_TOKEN=
COURTLISTENER_API_KEY=
WANDB_API_KEY=
OPENAI_API_KEY=        # only used for GPT-4o ceiling baseline
```

Copy to `.env` and fill values. Register for CourtListener API at https://www.courtlistener.com/help/api/ (free, instant).

- [ ] **Step 6: Write `citecheck/src/citecheck/config.py`**

Centralize all paths, model IDs, hyperparameters:

```python
from pathlib import Path
from pydantic import BaseModel

ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / "data"

class Config(BaseModel):
    backbone: str = "meta-llama/Llama-3.1-8B-Instruct"
    secondary_backbone: str = "Qwen/Qwen2.5-7B-Instruct"
    dense_encoder: str = "BAAI/bge-base-en-v1.5"
    legal_encoder: str = "nlpaueb/legal-bert-base-uncased"
    cross_encoder: str = "BAAI/bge-reranker-base"
    nli_judge: str = "MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli"
    max_retrieve_k: int = 50
    rerank_top_k: int = 10
    verify_max_iters: int = 3
    seeds: list[int] = [13, 42, 1337]
```

- [ ] **Step 7: Smoke-test imports**

```powershell
python -c "import transformers, peft, trl, bitsandbytes, sentence_transformers, pyserini, eyecite, outlines, faiss; print('ok')"
```

Risk: `pyserini` on Windows can be flaky — if you hit `JNI` errors, fall back to WSL2 Ubuntu for indexing steps only.

- [ ] **Step 8: Smoke-test GPU inference with a 7B model in 4-bit**

```python
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
bnb = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_compute_dtype="bfloat16")
m = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-7B-Instruct", quantization_config=bnb, device_map="auto")
print(m.get_memory_footprint() / 1e9, "GB")
```

Should report ~5–6 GB. Compute: ~10 minutes wall time.

- [ ] **Step 9: Log Task 15 in `journal/weekly.md` (week of 2026-09-07)**

### Task 16: Download and index CAP locally; set up CourtListener client with disk cache

**Artifacts:**
- Create: `citecheck/scripts/download_cap.ps1`
- Create: `citecheck/src/citecheck/data/cap_loader.py`
- Create: `citecheck/src/citecheck/data/cl_client.py`
- Create: `citecheck/data/cap_parquet/` (populated with ~6.7M opinions)
- Create: `citecheck/data/indices/bm25/` (Lucene index)

- [ ] **Step 1: Download CAP bulk data (RISK: ~100GB, multi-day download)**

CAP is hosted at https://case.law/ and mirrored on the LIL S3 bucket. The full corpus is ~100GB compressed. Use the per-jurisdiction tarballs to chunk the download — start with the 10 largest reporters (US Supreme Court, Federal Reporter, California, NY, Texas) to unblock indexing while remaining downloads run in the background.

```powershell
# scripts/download_cap.ps1
$jurisdictions = @("us", "f", "f2d", "f3d", "cal", "ny", "tex", "mass", "ill", "fla")
foreach ($j in $jurisdictions) {
    $url = "https://static.case.law/$j/"
    # Use aria2c for resumable, parallel downloads
    aria2c -d data/cap_raw/$j -i "$url" --continue=true --max-connection-per-server=4
}
```

Verify: `(Get-ChildItem data\cap_raw -Recurse -File | Measure-Object -Property Length -Sum).Sum / 1GB` should grow steadily. Run in background; check daily.

- [ ] **Step 2: Write `cap_loader.py` to stream JSON → parquet with metadata schema**

Key fields to retain per opinion: `id`, `name_abbreviation`, `decision_date`, `jurisdiction`, `court`, `citations` (list of strings), `casebody.opinions[].text`. Use `pyarrow` for streaming writes; one parquet file per jurisdiction.

Verify after first jurisdiction completes: `import pyarrow.parquet as pq; t = pq.read_table("data/cap_parquet/us.parquet"); print(t.num_rows)` — expect ~30,000 for US Supreme Court.

- [ ] **Step 3: Write `cl_client.py` — a thin requests wrapper with disk cache and retry**

```python
import requests, json, hashlib
from pathlib import Path
from tenacity import retry, wait_exponential, stop_after_attempt

CACHE = Path("data/cl_cache")

class CourtListenerClient:
    BASE = "https://www.courtlistener.com/api/rest/v4"
    def __init__(self, token: str):
        self.s = requests.Session()
        self.s.headers["Authorization"] = f"Token {token}"

    @retry(wait=wait_exponential(min=1, max=30), stop=stop_after_attempt(5))
    def get(self, path: str, **params):
        key = hashlib.sha256(f"{path}{sorted(params.items())}".encode()).hexdigest()[:16]
        cached = CACHE / f"{key}.json"
        if cached.exists():
            return json.loads(cached.read_text())
        r = self.s.get(f"{self.BASE}{path}", params=params, timeout=30)
        r.raise_for_status()
        CACHE.mkdir(parents=True, exist_ok=True)
        cached.write_text(r.text)
        return r.json()
```

Smoke-test: fetch the `/clusters/?cite=410 U.S. 113` (Roe v. Wade) endpoint, verify response is cached on second call.

- [ ] **Step 4: Build BM25 index over CAP opinions using Pyserini**

```python
# scripts/build_bm25_index.py
# Convert parquet → Pyserini-compatible JSONL (id, contents)
# Then: python -m pyserini.index.lucene -collection JsonCollection \
#   -input data/cap_jsonl -index data/indices/bm25 -generator DefaultLuceneDocumentGenerator \
#   -threads 8 -storePositions -storeDocvectors -storeRaw
```

Compute: indexing 6.7M opinions takes ~6–8 hours single-threaded on SSD, ~2 hours with 8 threads. Start this overnight.

Verify: `from pyserini.search.lucene import LuceneSearcher; s = LuceneSearcher("data/indices/bm25"); hits = s.search("Miranda warning custodial interrogation", k=5); print([h.docid for h in hits])` returns 5 hits.

- [ ] **Step 5: Build dense FAISS index over a 500K subset for early prototyping**

Full-corpus dense indexing (6.7M × 768d = ~20GB FP32, ~10GB FP16) is unnecessary for M3. Start with the 500K most-cited opinions (use a citation-count cutoff). Full index built later in Task 31.

```python
from sentence_transformers import SentenceTransformer
import faiss, numpy as np
model = SentenceTransformer("BAAI/bge-base-en-v1.5", device="cuda")
# Chunk each opinion into 512-token windows, embed, store doc_id mapping
```

Compute: ~6 GPU-hours for 500K chunks at batch size 64.

- [ ] **Step 6: Document the index sizes and a sample retrieval in `notebooks/01_cap_exploration.ipynb`**

- [ ] **Step 7: Log Task 16 in `journal/weekly.md` (weeks of 2026-09-14 and 2026-09-21)**

This task spans 2 weeks because of the download time. Note in journal which subset of CAP is indexed and any download failures encountered.

### Task 17: Load LegalBench-RAG + CUAD into standardized format

**Artifacts:**
- Create: `citecheck/src/citecheck/data/benchmarks.py`
- Create: `citecheck/data/eval/legalbench_rag_standardized.jsonl`
- Create: `citecheck/data/eval/cuad_standardized.jsonl`

- [ ] **Step 1: Download LegalBench-RAG**

LegalBench-RAG is the 2024 retrieval-augmented extension of LegalBench (Guha et al. 2024, arXiv:2308.11462; LegalBench-RAG by Pipitone & Alami 2024, arXiv:2408.10343).

```python
from datasets import load_dataset
ds = load_dataset("ZeroEntropy/legalbench-rag")
# Tasks: contract_nli, cuad, maud, privacy_qa
```

If the HF dataset is renamed/unavailable, fall back to the GitHub release at https://github.com/ZeroEntropyAI/legalbench-rag.

- [ ] **Step 2: Download CUAD v1 (Hendrycks et al. 2021, arXiv:2103.06268)**

```python
ds_cuad = load_dataset("theatticusproject/cuad-qa")
# 510 commercial contracts, 41 legal clause types
```

- [ ] **Step 3: Define a standardized record schema**

```python
# benchmarks.py
from pydantic import BaseModel
class EvalRecord(BaseModel):
    qid: str
    source: str                # "legalbench_rag" | "cuad" | "citecheck_v1"
    task: str                  # e.g., "contract_nli", "obligation_extraction"
    question: str
    context_docs: list[dict]   # optional pre-supplied context
    gold_answer: str | None
    gold_citations: list[str]  # Bluebook-form citations; empty for non-citation tasks
    jurisdiction: str | None
    difficulty: str | None     # "easy" | "medium" | "hard"
```

- [ ] **Step 4: Write loaders that emit JSONL files in this schema**

Verify: `wc -l data/eval/legalbench_rag_standardized.jsonl` reports the expected record count (sanity-check against the dataset's published size). For CUAD: expect 22,000+ QA pairs collapsed to ~4,000 unique questions if grouping by question template.

- [ ] **Step 5: Spot-check 20 records manually**

Open the JSONL, pick 20 random rows, confirm `question` and `gold_answer` look coherent and `gold_citations` either populated (citation task) or correctly empty (non-citation task). Document any schema mismatches in `notebooks/02_eyecite_smoke.ipynb`.

- [ ] **Step 6: Log Task 17 + September weekly reflection in `journal/weekly.md`**

Include: (a) total GPU-hours consumed in Sep, (b) any blocker (e.g., CAP download still in progress), (c) on-track-for-M3? Y/N.

---

## Month 2 — October 2026: Baseline reproduction begins (M3 work)

Compute budget for the month: ~40 GPU-hours (mostly inference; vanilla-LLM eval, naive RAG sweep, Self-RAG training).

### Task 18: Reproduce vanilla Llama-3.1-8B-Instruct baseline on LegalBench-RAG (no retrieval)

**Artifacts:**
- Create: `citecheck/baselines/vanilla_llama.py`
- Create: `citecheck/experiments/runs/2026-10-vanilla-llama/results.json`

- [ ] **Step 1: Write the inference script**

Load Llama-3.1-8B-Instruct in 4-bit (fits in ~6GB), iterate the standardized eval set, generate answers with a simple system prompt: "Answer the legal question. If citing a case, use Bluebook format."

```python
# baselines/vanilla_llama.py
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import json, time
from citecheck.config import Config
cfg = Config()
bnb = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_compute_dtype="bfloat16")
tok = AutoTokenizer.from_pretrained(cfg.backbone)
m = AutoModelForCausalLM.from_pretrained(cfg.backbone, quantization_config=bnb, device_map="auto")
# ... iterate eval set, generate, write results.json
```

- [ ] **Step 2: Run on the LegalBench-RAG subset (no context provided)**

Compute: ~4 GPU-hours for ~4,000 questions at ~3s/question.

- [ ] **Step 3: Compute placeholder metrics (Exact Match, ROUGE-L)**

Full CiteCheck metrics (CRR, CSF1, etc.) come online in Task 35. For now: confirm the model produces plausible output, store raw generations + per-question latency.

- [ ] **Step 4: Sanity-check 20 outputs manually**

Confirm that (a) the model attempts citations in Bluebook form, (b) you can identify obvious hallucinations (cites that don't exist) — these become your first qualitative evidence of the problem CiteCheck addresses.

- [ ] **Step 5: Log Task 18 in `journal/weekly.md` (week of 2026-10-05)**

### Task 19: Implement BM25 + bge-base naive RAG baseline

**Artifacts:**
- Create: `citecheck/baselines/naive_rag.py`
- Create: `citecheck/src/citecheck/retrieval/bm25_index.py`
- Create: `citecheck/src/citecheck/retrieval/dense_index.py`
- Create: `citecheck/src/citecheck/retrieval/hybrid.py`
- Create: `citecheck/experiments/runs/2026-10-naive-rag/results.json`

- [ ] **Step 1: Wrap Pyserini in `bm25_index.py` with a `search(query, k)` interface**

- [ ] **Step 2: Wrap FAISS in `dense_index.py` with `search(query, k)` and `embed(text)`**

- [ ] **Step 3: Implement reciprocal rank fusion in `hybrid.py`**

```python
def rrf(bm25_hits: list, dense_hits: list, k: int = 60) -> list:
    scores = {}
    for rank, h in enumerate(bm25_hits): scores[h.docid] = scores.get(h.docid, 0) + 1/(k+rank)
    for rank, h in enumerate(dense_hits): scores[h.docid] = scores.get(h.docid, 0) + 1/(k+rank)
    return sorted(scores.items(), key=lambda x: -x[1])
```

- [ ] **Step 4: Wire into a naive RAG baseline (retrieve top-10, stuff into prompt, generate)**

- [ ] **Step 5: Run on the same LegalBench-RAG slice as Task 18**

Compute: ~6 GPU-hours (retrieval is CPU-bound; generation dominates).

- [ ] **Step 6: Verify naive RAG beats vanilla on at least one metric**

If it doesn't, debug retrieval — likely cause is poor index coverage of the specific corpus the benchmark was built from. CUAD specifically references contracts not in CAP; for CUAD queries the "retrieval corpus" must be the contract collection itself.

- [ ] **Step 7: Log Task 19 in `journal/weekly.md` (week of 2026-10-12)**

### Task 20: Implement Self-RAG (Asai et al. 2024) baseline

**Artifacts:**
- Create: `citecheck/baselines/self_rag.py`
- Create: `citecheck/experiments/runs/2026-10-self-rag/results.json`

- [ ] **Step 1: Pull the published Self-RAG model and code**

Asai et al. 2024 "Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection" (arXiv:2310.11511). Authors released `selfrag/selfrag_llama2_7b` on HF Hub plus training code at https://github.com/AkariAsai/self-rag.

Risk: Self-RAG was trained on Llama-2-7B; running it as-is is the cleanest reproduction. Adapting to Llama-3.1-8B is a research project of its own — out of scope. Use the original checkpoint.

- [ ] **Step 2: Implement the inference loop with reflection tokens**

Self-RAG uses special tokens (`[Retrieve]`, `[IsRel]`, `[IsSup]`, `[IsUse]`) — decode these and branch retrieval/generation accordingly. The released `selfrag` package handles this; use it as a starting point.

- [ ] **Step 3: Plug in your CAP BM25 retriever as the retrieval backend (replace their default Contriever)**

- [ ] **Step 4: Run on the same eval slice**

Compute: ~12 GPU-hours (multi-pass generation is slow).

- [ ] **Step 5: Record per-question reflection-token usage**

Track how often `[Retrieve]` fires — this is a useful comparator for CiteCheck's k-iteration verify loop.

- [ ] **Step 6: Verification: confirm Self-RAG numbers are within 10–20% of the original paper's reported scores on a comparable task**

If the gap is huge, the most likely cause is tokenizer / template mismatch. Document the gap rather than chase it for 2 weeks.

- [ ] **Step 7: Log Task 20 + October weekly reflection (week of 2026-10-26)**

Include hours spent debugging Self-RAG specifically (commonly underestimated). October retrospective: any task slipping into November?

---

## Month 3 — November 2026: M3 milestone

Compute budget for the month: ~35 GPU-hours.

### Task 21: Implement CRAG (Yan et al. 2024) baseline

**Artifacts:**
- Create: `citecheck/baselines/crag.py`
- Create: `citecheck/experiments/runs/2026-11-crag/results.json`

- [ ] **Step 1: Pull CRAG paper and reference impl**

Yan et al. 2024 "Corrective Retrieval Augmented Generation" (arXiv:2401.15884). Code: https://github.com/HuskyInSalt/CRAG. Core idea: a lightweight retrieval evaluator (T5-large) scores retrieved docs as Correct / Incorrect / Ambiguous; Incorrect triggers a web search; Ambiguous merges both.

- [ ] **Step 2: Train or load the retrieval evaluator**

Authors released a fine-tuned T5-large evaluator. Use it directly. If unavailable, fine-tune T5-large on PopQA/Bio (~6 GPU-hours QLoRA) — but only as fallback.

- [ ] **Step 3: Adapt the "web search" branch for legal domain**

Replace web search with a CourtListener API query (you already have the client from Task 16). This is a legitimate adaptation — document it clearly so the baseline is reproducible.

- [ ] **Step 4: Run on the eval slice**

Compute: ~8 GPU-hours.

- [ ] **Step 5: Verify CRAG behavior changes vs naive RAG**

Inspect 10 cases where CRAG triggered re-retrieval. Confirm the re-retrieval pulled different docs than the initial pass. If it never re-retrieves, the evaluator is too lenient — adjust threshold.

- [ ] **Step 6: Log Task 21 in `journal/weekly.md` (week of 2026-11-02)**

### Task 22: Reimplement EL-RAG (Wankhade 2026) — RISK FLAG

**Artifacts:**
- Create: `citecheck/baselines/el_rag.py` OR a stub `el_rag_NOT_REPRODUCED.md`
- Create: `journal/decisions.md` entry on reproducibility

- [ ] **Step 1: Locate EL-RAG paper and any released artifacts**

Wankhade 2026 — verify the exact DOI/arXiv ID from the Phase 1 reading list and confirm whether code, model, or data is publicly released.

- [ ] **Step 2: If code is released → reimplement following the published method**

Likely components: an entity-linking module (e.g., BLINK or ReFinED) bolted onto a RAG pipeline. Estimate: 1 week + ~6 GPU-hours.

- [ ] **Step 3: If code is NOT released and the paper underspecifies — write `el_rag_NOT_REPRODUCED.md` and stop**

Document what's missing (e.g., entity-linker checkpoint not released, no training hyperparameters, ambiguous loss formulation). Add a decision-log entry. Do not spend more than 3 days on a stub reimplementation.

Risk: this is a foreseeable stall point. The safer fallback is replacing EL-RAG in the baseline table with **a stronger off-the-shelf method you can run** — candidates: ARES retrieval evaluator (Saad-Falcon et al. 2024, arXiv:2311.09476), or RaLLe (Hoshi et al. 2023, arXiv:2308.10633).

- [ ] **Step 4: Run EL-RAG (or its replacement) on the eval slice**

Compute: ~8 GPU-hours.

- [ ] **Step 5: Log Task 22 in `journal/weekly.md` (week of 2026-11-09)**

### Task 23: M3 milestone retrospective + decision

**Artifacts:**
- Create / Modify: `journal/phase2_retros.md` (M3 section)
- Modify: `project/problem_statement.md` (only if numbers force a revision)
- Create / Modify: `project/baselines.md` (lock the final baseline lineup)

- [ ] **Step 1: Assemble a baseline-comparison table**

Pull `results.json` from each baseline run, build a markdown table with rows = methods, columns = (latency, EM, ROUGE-L, retrieval recall@10). Even without the final CiteCheck metrics, this exposes the rough landscape.

- [ ] **Step 2: Inspect 20 high-citation-density questions across baselines**

Look for the hallucination pattern: when does a baseline cite a case that doesn't exist? Document 3–5 concrete failure modes — these become the motivating examples in your paper.

- [ ] **Step 3: M3 retrospective in `journal/phase2_retros.md`**

```markdown
## M3 Retrospective — End of November 2026

- Baselines reproduced: [list with √ or × per method]
- Baseline-comparison table: [link or paste]
- Hallucination failure modes observed: [3–5 bullets]
- Total GPU-hours consumed in Sep–Nov: [N]
- Total wall-clock weeks: [N]

### Decision: lock or revise problem statement?
- [ ] LOCK — baselines confirm the citation-fabrication problem is real and unsolved
- [ ] REVISE — baselines already solve it (unlikely given pre-work) OR baselines reveal a different, more interesting problem

### Adjustments for Dec–Feb
- [...]
```

- [ ] **Step 4: If REVISE, update `project/problem_statement.md` to v1.1 and log in `journal/decisions.md`**

Revision should not change the project scope significantly — it should sharpen the contribution claim (e.g., "we focus on Bluebook-structured citation grounding because we observe baselines hallucinate volume numbers more than case names").

- [ ] **Step 5: Lock the final baseline lineup in `project/baselines.md`**

5 methods to evaluate against in M5: vanilla Llama-3.1-8B, naive RAG, Self-RAG, CRAG, EL-RAG (or replacement), HalluGraph post-hoc detector (added in Task 33), GPT-4o-mini-web (ceiling, added in Task 33).

- [ ] **Step 6: Log Task 23 + November weekly reflection (week of 2026-11-30)**

---

## Month 4 — December 2026: Eval set construction begins

Compute budget for the month: ~20 GPU-hours (LLM pre-labeling pass). Human effort: ~30–40 hours of your time on annotation review; ramping up an annotator (Task 26) is a parallel track.

### Task 24: Mine the Charlotin AI-hallucination tracker for adversarial citation examples

**Artifacts:**
- Create: `citecheck/data/eval/adversarial_seed.jsonl` (~50 examples)
- Create: `notebooks/03_pilot_50q.ipynb` (early scaffolding)

- [ ] **Step 1: Pull the Charlotin tracker dataset**

Damien Charlotin maintains a public DB of legal AI-hallucination cases at https://www.damiencharlotin.com/hallucinations/. Scrape the table (respecting robots.txt) or use a published CSV if available. Each row is a real-world incident of an LLM fabricating a citation in a court filing.

- [ ] **Step 2: For each incident, extract: (question or task posed to LLM, fabricated citation, evidence of fabrication)**

Many entries link to court orders (PDFs); use those as ground-truth attestation that the citation is fake.

- [ ] **Step 3: Construct ~50 adversarial questions**

Format: "Find a case supporting [legal proposition that was wrongly cited in a real incident]". Gold answer = "No supporting case exists in the corpus" + the actual cases (if any) on the topic. These are the negative-class questions for measuring Fabrication Rate.

- [ ] **Step 4: Save to `adversarial_seed.jsonl` in the standardized schema**

- [ ] **Step 5: Spot-check 10 adversarial questions against your BM25 index — confirm they return plausible-looking but wrong candidates**

- [ ] **Step 6: Log Task 24 in `journal/weekly.md` (week of 2026-12-07)**

### Task 25: LLM pre-label 500 candidate question/gold-citation pairs

**Artifacts:**
- Create: `citecheck/scripts/prelabel_eval_set.py`
- Create: `citecheck/data/eval/eval_set_v0_unverified.jsonl` (500 candidates, NOT yet human-verified)

- [ ] **Step 1: Sample candidate source contexts from CAP + CUAD + LegalBench-RAG**

Target distribution: 200 from CAP opinions (case-law citation tasks), 150 from CUAD (contract-clause QA), 100 from LegalBench-RAG existing tasks, 50 adversarial (from Task 24).

- [ ] **Step 2: For each context, prompt a strong model (GPT-4o or Claude 3.5 Sonnet) to generate (a) a realistic legal question, (b) the gold answer, (c) the supporting citation in Bluebook form**

```
You are constructing a legal-QA benchmark. Given this case opinion: <text>
Generate ONE question a junior attorney might realistically ask, the answer
grounded in the opinion, and the Bluebook citation. Output JSON:
{"question": "...", "gold_answer": "...", "gold_citations": ["..."]}
```

Cost: ~$30–60 in API calls for 500 candidates.

- [ ] **Step 3: Run `eyecite` over each generated citation to confirm it parses to a valid structure**

Reject any candidate where the citation doesn't parse. Re-prompt the model to regenerate. Track rejection rate; expect 5–10%.

- [ ] **Step 4: Output `eval_set_v0_unverified.jsonl`**

These are CANDIDATES; they are not yet usable. Human verification (Task 26) is required.

- [ ] **Step 5: You-as-annotator: spot-check 30 candidates personally**

Verify question is well-formed, answer is grounded, citation resolves in CourtListener. If your own spot-check rejection rate is >30%, regenerate with a stronger prompt before handing off to the annotator.

- [ ] **Step 6: Log Task 25 in `journal/weekly.md` (week of 2026-12-14)**

### Task 26: Recruit + onboard annotator — RISK FLAG, EXTERNAL DEPENDENCY

**Artifacts:**
- Create: `citecheck/data/eval/annotation_guidelines.md`
- Create: `outreach/annotator_recruitment_log.md`

- [ ] **Step 1: Decide annotator track**

Two paths:
- **Paid (Upwork)**: paralegal or JD with US case-law experience. Budget: $25–40/hr × ~80 hrs = $2,000–3,200 for 500 items.
- **Collaborator (law school)**: cold-email 5–10 US law school faculty (esp. legal tech / legal-NLP folks) asking if a JD student would co-annotate for co-authorship on the paper. Lower cash cost; higher coordination cost; higher upside (potential co-author).

Recommended: try collaborator path for 2 weeks (Dec 1–14); if no firm yes by Dec 21, fall back to Upwork.

- [ ] **Step 2: Write `annotation_guidelines.md`**

Cover: (a) what "gold citation" means in Bluebook form, (b) acceptable Shepardization-equivalent verification steps (CourtListener check), (c) inter-annotator agreement protocol — you will dual-annotate 50 items to compute Cohen's kappa, target ≥0.7, (d) UI: if no budget for Label Studio, a Google Sheet with a prescribed schema is fine.

- [ ] **Step 3: Post job / send emails (in parallel with Task 25)**

Log every contact in `outreach/annotator_recruitment_log.md` with date, channel, status.

- [ ] **Step 4: Onboarding session (synchronous 60-min call) once an annotator agrees**

Walk through the guidelines with 5 example items. Have them annotate 10 items as a tryout; if kappa with your own annotation is <0.5, either retrain or hire someone else.

- [ ] **Step 5: Begin annotation in parallel with Task 27 (you keep coding; annotator processes ~50 items/week)**

500 items ÷ 50/week = 10 weeks. With Dec start, finishes mid-Feb — JUST in time for M4 pilot eval. THIS IS THE SINGLE TIGHTEST DEPENDENCY IN PHASE 2. If recruitment slips past Dec 21, the pilot eval (Task 32) will run on a partial set.

- [ ] **Step 6: Log Task 26 + December weekly reflection (week of 2026-12-28)**

End-of-year retro: hours-vs-plan delta, annotator pipeline status, any course-correction needed for Q1 2027.

---

## Month 5 — January 2027: Method prototyping

Compute budget for the month: ~25 GPU-hours.

### Task 27: Implement Bluebook citation parser via eyecite + custom regex

**Artifacts:**
- Create: `citecheck/src/citecheck/rerank/grounding_signal.py`
- Create: `citecheck/notebooks/02_eyecite_smoke.ipynb` (extend with citation-parsing tests)

- [ ] **Step 1: Skim eyecite docs (https://eyecite.readthedocs.io/) — confirm coverage of US federal + state reporter formats**

- [ ] **Step 2: Write a wrapper that returns structured fields per citation**

```python
# grounding_signal.py
from eyecite import get_citations
from eyecite.models import FullCaseCitation

def parse_citation(text: str) -> list[dict]:
    """Parse text and return [{volume, reporter, page, year, court, parties, raw}]."""
    out = []
    for c in get_citations(text):
        if isinstance(c, FullCaseCitation):
            md = c.metadata
            out.append({
                "volume": c.groups.get("volume"),
                "reporter": c.groups.get("reporter"),
                "page": c.groups.get("page"),
                "year": md.year,
                "court": md.court,
                "plaintiff": md.plaintiff,
                "defendant": md.defendant,
                "raw": c.matched_text(),
            })
    return out
```

- [ ] **Step 3: Add custom regex fallbacks for Bluebook patterns eyecite misses**

Examples: parallel citations (multiple reporters), supplements ("(Supp. 2019)"), short forms ("Roe, 410 U.S. at 153"). Add tests for each.

- [ ] **Step 4: Run parser over the gold citations in `eval_set_v0_unverified.jsonl` and confirm ≥95% parse rate**

If parse rate <95%, either improve regex or filter unparseable citations from the eval set (and log the filter rate as a known limitation in the paper).

- [ ] **Step 5: Define the structure-aware grounding signal**

For a (question, retrieved opinion, candidate citation) triple, compute features:
- citation parses (binary)
- parsed reporter matches opinion's known reporter (binary)
- parsed volume/page within ±2 of opinion's volume/page (binary)
- parsed year matches decision_date year (binary)
- parsed court matches opinion's court (binary)

These features become the structure-aware signal in the reranker training loss (Task 30).

- [ ] **Step 6: Log Task 27 in `journal/weekly.md` (week of 2027-01-04)**

### Task 28: Prototype the CitationResolver agent tool

**Artifacts:**
- Create: `citecheck/src/citecheck/agent/citation_resolver.py`

- [ ] **Step 1: Define the tool interface**

```python
# citation_resolver.py
from pydantic import BaseModel

class ResolveResult(BaseModel):
    citation_raw: str
    resolved: bool
    source: str | None        # "cap" | "courtlistener" | None
    opinion_id: str | None
    excerpt: str | None       # snippet supporting the cite, if applicable
    error: str | None         # e.g., "volume not found", "fabricated"

def resolve_citation(citation_raw: str) -> ResolveResult:
    parsed = parse_citation(citation_raw)
    if not parsed: return ResolveResult(citation_raw=citation_raw, resolved=False, error="unparseable")
    # 1. Try CAP local parquet by (volume, reporter, page)
    # 2. Fall back to CourtListener API
    # 3. Return resolved=False with error if neither hits
    ...
```

- [ ] **Step 2: Implement CAP lookup**

Build a small lookup index (parquet → pandas in-memory df keyed by (volume, reporter, page)) — ~6.7M rows × 5 cols = ~500MB RAM, acceptable.

- [ ] **Step 3: Implement CourtListener fallback using `CourtListenerClient.get("/clusters/", cite=...)`**

Risk: CL rate-limits at ~5,000 req/hr. Mitigation: aggressive disk cache (already in Task 16), batched resolution where possible.

- [ ] **Step 4: Write 30 unit tests covering: real cite (resolves), real cite with typo (one digit off — should fail or fuzzy-match — your choice, document), fabricated cite (should not resolve)**

- [ ] **Step 5: Measure resolver latency**

Target: <200ms cached, <2s uncached (network-bound). Profile and add an in-memory LRU on top of the disk cache if needed.

- [ ] **Step 6: Log Task 28 in `journal/weekly.md` (week of 2027-01-11)**

### Task 29: Build constrained-decoding grammar for citation emission

**Artifacts:**
- Create: `citecheck/src/citecheck/agent/citation_grammar.py`

- [ ] **Step 1: Define a Lark/CFG grammar for Bluebook full case citations**

`outlines` (Willard & Louf 2023, arXiv:2307.09702) supports CFG-constrained generation. Define a grammar covering: full case cite, short cite, id., supra, parallel cites.

```
case_cite: parties "," WS volume WS reporter WS page paren_year
parties: WORD ("v." WS WORD)?
volume: INT
reporter: REPORTER_TOKEN
page: INT
paren_year: "(" YEAR ")"
REPORTER_TOKEN: "U.S." | "F." | "F.2d" | "F.3d" | "S.Ct." | ...
```

- [ ] **Step 2: Wrap with outlines or guidance to enforce grammar during generation**

```python
from outlines import generate, models
m = models.transformers("meta-llama/Llama-3.1-8B-Instruct")
gen = generate.cfg(m, citation_grammar)
output = gen("Cite the controlling Supreme Court case on Miranda warnings.")
```

- [ ] **Step 3: Compare constrained vs unconstrained generation on 50 questions**

Measure: % of outputs that contain at least one citation; % of citations that pass eyecite parsing; % that resolve via CitationResolver.

- [ ] **Step 4: Tune the grammar — common failure: too restrictive grammar blocks valid citations the model wants to emit**

Iterate until ≥98% of constrained outputs parse via eyecite. Compute: ~6 GPU-hours of iteration.

- [ ] **Step 5: Log Task 29 + January weekly reflection (week of 2027-01-25)**

January is the gear-up month for M4. By end of Jan you should have: parser working, resolver working, grammar working — three independent components. M4 is the integration + reranker training.

---

## Month 6 — February 2027: M4 milestone (novel contribution prototyped)

Compute budget for the month: ~60 GPU-hours (reranker fine-tuning dominates).

### Task 30: Fine-tune cross-encoder reranker with multi-objective loss

**Artifacts:**
- Create: `citecheck/src/citecheck/rerank/cross_encoder.py`
- Create: `citecheck/src/citecheck/rerank/train_reranker.py`
- Create: `citecheck/experiments/runs/2027-02-reranker-v1/`

- [ ] **Step 1: Define training data**

GAP: the original spec doesn't say where (query, doc, label) triples for reranker training come from. Resolution: construct from (question, gold-citation-opinion, retrieved-but-wrong-opinion) triples mined from your eval-set candidates + Task 19's BM25 hits. Target: 10,000–30,000 triples. Positives = retrieved opinions whose ID matches gold_citation's CAP id. Hard negatives = retrieved opinions same jurisdiction + similar topic but wrong cite. Easy negatives = random sample from CAP.

- [ ] **Step 2: Define the multi-objective loss**

`L = L_relevance + λ · L_grounding`

- `L_relevance`: standard pairwise margin loss (positives vs negatives), as in `BAAI/bge-reranker-base` training.
- `L_grounding`: BCE over the structure-aware features from Task 27 — model predicts "would the citation parsed from this passage match the question's citation context?". Treat the 5 binary structure features as auxiliary supervision; sum BCE losses.
- λ tuned over {0.1, 0.3, 0.5, 1.0} on a 500-triple validation split.

- [ ] **Step 3: Fine-tune via QLoRA on `BAAI/bge-reranker-base` (568M params)**

Reranker is small enough that full fine-tuning fits in 24GB — QLoRA is still recommended for speed + reproducibility. Hyperparameters: lr 2e-5, batch 16, epochs 3, LoRA rank 16.

```python
# train_reranker.py — outline only
from peft import LoraConfig, get_peft_model
from trl import RewardTrainer
# build dataset of (question, pos_doc, neg_doc, structure_features)
# wrap base CE in custom model with two heads (relevance, grounding)
# train with weighted sum of losses
```

Compute: ~12 GPU-hours per λ value × 4 = 48 GPU-hours. This is the biggest single compute block in Phase 2.

- [ ] **Step 4: Evaluate reranker on held-out 500 triples**

Metric: NDCG@10 on relevance; AUC on grounding-feature prediction. Pick the best λ for downstream integration.

- [ ] **Step 5: Log Task 30 in `journal/weekly.md` (week of 2027-02-01) — note 2 weeks elapsed because of training queue**

### Task 31: Integrate stages 1-2-3 into end-to-end CiteCheck agent

**Artifacts:**
- Create: `citecheck/src/citecheck/agent/verify_loop.py`
- Create: `citecheck/src/citecheck/agent/citecheck.py`
- Create: `citecheck/scripts/run_citecheck.py`

- [ ] **Step 1: Wire the components**

```
question
  → hybrid retrieve (BM25 + dense) top-50
  → fine-tuned reranker top-10
  → backbone LLM with constrained-citation grammar generates answer with cites
  → CitationResolver checks every cite
  → if all resolve AND NLI judge supports → return
  → if not, retract bad cites, re-retrieve with augmented query, regenerate (max k=3)
```

- [ ] **Step 2: Implement the verify loop**

```python
# verify_loop.py
def verify_and_iterate(question, generate_fn, retrieve_fn, max_iters=3):
    for i in range(max_iters):
        answer, cites = generate_fn(question, retrieve_fn(question))
        resolutions = [resolve_citation(c) for c in cites]
        if all(r.resolved for r in resolutions): return answer, cites, resolutions
        # augment query with failed citations' context, retry
        question = augment(question, resolutions)
    return answer, cites, resolutions   # return last attempt with failures noted
```

- [ ] **Step 3: Build full dense FAISS index over the FULL 6.7M CAP corpus**

Postponed from Task 16 — needed now for full evaluation. Compute: ~40 GPU-hours embedding pass. Run on Colab Pro A100 burst if your local GPU is too slow.

- [ ] **Step 4: Smoke-test end-to-end on 20 hand-picked questions**

Confirm the loop terminates, citations resolve, answers are non-empty.

- [ ] **Step 5: Log Task 31 in `journal/weekly.md` (week of 2027-02-15)**

### Task 32: Pilot evaluation on 50 hand-picked questions + M4 milestone retrospective

**Artifacts:**
- Create: `citecheck/experiments/runs/2027-02-pilot/results.json`
- Create / Modify: `journal/phase2_retros.md` (M4 section)

- [ ] **Step 1: Curate 50 questions covering: 20 easy (citation in retrieval top-3), 20 medium (top-10 but not top-3), 10 hard (adversarial)**

Use the human-verified eval set; if annotator hasn't finished, use your own spot-checked subset.

- [ ] **Step 2: Run all baselines + CiteCheck on the 50-item pilot**

Compute: ~4 GPU-hours.

- [ ] **Step 3: Compute pilot metrics**

Citation Resolution Rate (CRR), simple binary Citation Support (does the cited opinion contain a sentence entailing the answer? — manual judgment for 50 items is fine), Fabrication Rate.

- [ ] **Step 4: M4 retrospective in `journal/phase2_retros.md`**

```markdown
## M4 Retrospective — End of February 2027

- Novel components built: parser √, resolver √, grammar √, reranker √, agent loop √
- Pilot results (50 items): [paste table]
- CiteCheck CRR vs best baseline CRR: [+/- X pp]
- CiteCheck FabR vs best baseline FabR: [+/- X pp]
- Total GPU-hours consumed in Sep–Feb: [N]
- Annotator status: [N items completed of 500]

### Decision: proceed to full eval (Task 33) or iterate on method?
- [ ] PROCEED — pilot results show clear directional improvement
- [ ] ITERATE — pilot is inconclusive, give 2 more weeks to debug
- [ ] PIVOT — pilot is negative, revisit reranker loss design

### Risks carried forward
- Annotator completion rate
- CourtListener rate-limit during full eval
- [...]
```

- [ ] **Step 5: Log Task 32 + February weekly reflection (week of 2027-02-22)**

---

## Month 7 — March 2027: Full experiments

Compute budget for the month: ~80 GPU-hours (full eval runs across multiple baselines + CiteCheck + ablations).

### Task 33: Run all baselines + CiteCheck on the full eval set

**Artifacts:**
- Create: `citecheck/scripts/run_all_baselines.py`
- Create: `citecheck/experiments/runs/2027-03-full-eval/results.json`
- Create: `citecheck/baselines/hallugraph_posthoc.py`
- Create: `citecheck/baselines/gpt4o_websearch.py`

- [ ] **Step 1: Implement the two remaining baselines**

- **HalluGraph post-hoc detector**: take any baseline's output, run HalluGraph's claim-graph extraction over it, flag unverifiable claims. Treat as a post-hoc baseline — does not change the underlying generation. Use whichever public impl is closest to the original paper; if none exists, document as "skipped" rather than reimplement.
- **GPT-4o-mini with web search**: OpenAI's `gpt-4o-mini` with the `web_search` tool. This is the API-cost ceiling baseline. Budget: ~$50 for ~500 questions.

- [ ] **Step 2: Build `run_all_baselines.py` with a CLI flag per baseline**

`python scripts/run_all_baselines.py --baseline self_rag --eval data/eval/eval_set_v1.jsonl --out experiments/runs/...`

- [ ] **Step 3: Run each baseline on the full 500-item human-verified eval set**

Compute estimates:
- vanilla Llama: 2 GPU-hours
- naive RAG: 3 GPU-hours
- Self-RAG: 8 GPU-hours
- CRAG: 6 GPU-hours
- EL-RAG (or replacement): 6 GPU-hours
- CiteCheck: 8 GPU-hours
- HalluGraph: 2 GPU-hours (post-hoc, fast)
- GPT-4o-mini-web: ~$50 API + 0 GPU-hours

Total: ~35 GPU-hours.

- [ ] **Step 4: Compute all CiteCheck metrics**

Citation Resolution Rate, Citation Support F1 (via NLI judge — DeBERTa-v3-large-mnli; human audit comes in Task 35), Jurisdictional Validity (does the cited court bind the asked jurisdiction? — derived from eyecite court field + a small lookup table), Fabrication Rate.

- [ ] **Step 5: Verify CiteCheck beats best baseline on FabR and CRR — RISK FLAG**

If CiteCheck is not strictly better on at least one of (FabR, CRR), debug before moving to ablations. Common cause: reranker's grounding signal collapsed because of bad training data; refit with cleaner triples.

- [ ] **Step 6: Log Task 33 in `journal/weekly.md` (week of 2027-03-08)**

### Task 34: Ablation studies

**Artifacts:**
- Create: `citecheck/scripts/run_ablations.py`
- Create: `citecheck/experiments/ablations/2027-03/results.json`

- [ ] **Step 1: Define ablation configurations**

- A0: full CiteCheck (control)
- A1: − reranker (use raw hybrid retrieval, skip stage 2)
- A2: − CitationResolver (skip verify loop, accept LLM output as-is)
- A3: − constrained decoding (allow free-form generation, parse cites post-hoc)
- A4: − grounding-signal loss (relevance-only reranker)
- A5: − multi-iteration (k=1)
- A6: hybrid retrieval → BM25-only
- A7: hybrid retrieval → dense-only

- [ ] **Step 2: Run each ablation on the full eval set**

Compute: 8 GPU-hours × 7 ablations = 56 GPU-hours. This is the biggest single compute block of the month. Consider running 2–3 in parallel on Colab Pro burst.

- [ ] **Step 3: Build the ablation table (rows = configs, columns = metrics)**

Identify which removal hurts the most — this is your paper's central evidence for why each component matters.

- [ ] **Step 4: Spot-check 10 questions per ablation to confirm the metric drop is real (not a bug)**

- [ ] **Step 5: Log Task 34 in `journal/weekly.md` (week of 2027-03-15)**

### Task 35: Human audit of 200-item subset for Citation Support F1 and Answer Utility

**Artifacts:**
- Create: `citecheck/data/eval/audit_subset_v1.jsonl` (200 items, stratified sample)
- Create: `citecheck/experiments/runs/2027-03-human-audit/results.json`

- [ ] **Step 1: Sample 200 items stratified by (task type, difficulty, baseline-vs-CiteCheck disagreement)**

Disagreement-weighted sampling surfaces the most informative items.

- [ ] **Step 2: For each item × each method, present (question, generated answer, cited opinion text) to the human auditor**

Auditor judges: (a) does the cited opinion text support the answer? (Y/N/Partial), (b) Answer Utility Likert 1–5.

This is the SECOND major human-effort block. Annotator from Task 26 is ideal if available; otherwise budget 1–2 weeks of your own time (200 × 5 methods × 2 min = ~33 hrs solo).

- [ ] **Step 3: Compute Citation Support F1 from human Y/N judgments**

Replace the NLI-judge proxy with human labels for this 200-item subset; use the NLI judge on the full 500 set, reporting both numbers.

- [ ] **Step 4: Inter-rater check — you re-annotate 30 items the annotator did; compute Cohen's kappa, expect ≥0.7**

If kappa <0.7, retrain or discount results from divergent items.

- [ ] **Step 5: Log Task 35 + March weekly reflection (week of 2027-03-29)**

---

## Month 8 — April 2027: Wrap-up + paper outline

Compute budget for the month: ~40 GPU-hours (seed reps + secondary backbone).

### Task 36: Stability checks — multiple seeds and (compute permitting) a secondary base model

**Artifacts:**
- Create: `citecheck/experiments/seeds/2027-04/results.json`

- [ ] **Step 1: Re-run CiteCheck + the 2 strongest baselines under 3 random seeds (13, 42, 1337 from `Config`)**

Report mean ± std per metric. NLP reviewers increasingly demand this; it's cheap insurance.

Compute: 3 seeds × 3 methods × 8 GPU-hours = 72 GPU-hours. RISK: blows the monthly budget. Mitigation: if over budget, downsample eval set to 200 for seeds 2 and 3 — report this clearly.

- [ ] **Step 2: If compute permits, swap backbone to Qwen2.5-7B-Instruct and re-run CiteCheck only**

This establishes whether the method generalizes across base models. Compute: ~8 GPU-hours. Skip if Step 1 already consumed the budget.

- [ ] **Step 3: Log Task 36 in `journal/weekly.md` (week of 2027-04-05)**

### Task 37: Per-task and per-jurisdiction breakdown

**Artifacts:**
- Create: `citecheck/experiments/runs/2027-04-breakdown/results.json`

- [ ] **Step 1: Slice the full eval results by (task = contract_nli | cuad | case_law_qa | adversarial)**

Each slice should have ≥50 items for the comparison to be informative.

- [ ] **Step 2: Slice by jurisdiction (US Supreme Court vs federal circuits vs state)**

This is where the method's strength might vary — case-law citation density and Bluebook adherence differ across courts.

- [ ] **Step 3: Build two breakdown tables; identify any slice where CiteCheck UNDER-performs**

Honest reporting of failure slices strengthens the paper. Speculate on causes in 2–3 sentences per slice.

- [ ] **Step 4: Log Task 37 in `journal/weekly.md` (week of 2027-04-12)**

### Task 38: Draft paper outline

**Artifacts:**
- Create: `citecheck/paper/outline.md`

- [ ] **Step 1: Pick target venue v1 + v2**

Primary: NLLP @ EMNLP 2027 (submission window typically Jun/Jul 2027). Secondary: TrustNLP @ NAACL 2027 (Mar 2027 — likely missed; track 2027 NAACL main if Feb cycle is alive; otherwise TrustNLP @ EMNLP 2027 if separately co-located). Confirm dates before committing.

- [ ] **Step 2: Write a paper outline**

```markdown
# CiteCheck — Paper Outline

## 1. Introduction
- Problem: LLMs fabricate legal citations in real-world filings (cite Charlotin examples)
- Gap: no benchmark + method targets Bluebook-structured citation grounding
- Contribution: (1) 500-item benchmark, (2) faithfulness-tuned reranker, (3) agent-verify loop

## 2. Related Work
- RAG variants (Self-RAG, CRAG, EL-RAG)
- Legal NLP benchmarks (LegalBench, LegalBench-RAG, CUAD)
- Citation grounding + structured generation

## 3. The CiteCheck Benchmark
- Construction process (Tasks 24-26)
- Statistics, jurisdictional coverage
- Annotation protocol + inter-annotator agreement

## 4. Method
- Hybrid retrieval (BM25 + BGE-legal)
- Faithfulness-tuned reranker with structure-aware loss
- Constrained-decoding citation grammar
- CitationResolver agent tool + k-iteration verify loop

## 5. Experiments
- Baselines and setup
- Main results (Task 33)
- Ablations (Task 34)
- Human audit (Task 35)
- Stability (Task 36)
- Per-task and per-jurisdiction breakdown (Task 37)

## 6. Discussion
- Where CiteCheck wins and loses
- Limitations: corpus coverage, single backbone family, English-only US case-law
- Ethics: should LLMs draft legal documents at all?

## 7. Conclusion + Future Work

## Appendix
- Annotation guidelines
- Full grammar definition
- Hyperparameters
- Failure cases
```

- [ ] **Step 2: Block out the figures and tables you'll need**

- Figure 1: System diagram (3 stages)
- Figure 2: Reranker loss curves (per λ)
- Table 1: Benchmark statistics
- Table 2: Main results (all baselines × all metrics)
- Table 3: Ablations
- Table 4: Per-jurisdiction breakdown
- Figure 3: Qualitative example (a fabricated citation that CiteCheck retracts)

Start collecting raw data into `citecheck/paper/figures/` now; final rendering happens in Phase 3.

- [ ] **Step 3: Log Task 38 in `journal/weekly.md` (week of 2027-04-19)**

### Task 39: M5 partial milestone retrospective + Phase 3 hand-off

**Artifacts:**
- Modify: `journal/phase2_retros.md` (M5-partial section)
- Modify: `journal/decisions.md`

- [ ] **Step 1: M5-partial retrospective**

```markdown
## M5 (Partial) Retrospective — End of April 2027

- Full eval complete: √
- Ablations complete: √
- Human audit complete: √ (200 items)
- Stability checks: [seeds done? secondary backbone done?]
- Per-task / per-jurisdiction breakdown: √
- Paper outline drafted: √
- Total GPU-hours consumed Sep 2026 – Apr 2027: [N]
- Total annotator hours: [N]
- Annotator co-authorship status: [if collaborator path was taken]

### Headline numbers
- CiteCheck Citation Resolution Rate: X% (vs best baseline Y%)
- CiteCheck Fabrication Rate: X% (vs best baseline Y%)
- Citation Support F1 (human): X (vs best baseline Y)

### What is unfinished and goes into Phase 3
- Final M5 polish (week of May 2027)
- Paper writing (M6, Jun 2027)
- Submission to [venue] (M7, Jul 2027)
- Outreach: convert advisor feedback contacts into PhD application materials

### Risks for Phase 3
- Venue acceptance is uncertain even with strong numbers
- Backup venues: [list]
- If reviewers demand more experiments, do we have compute budget for Phase 3 to address them? [Y/N + plan]
```

- [ ] **Step 2: Decision log entry**

```markdown
| 2027-04-30 | Phase 2 complete; results support a submission-worthy paper | Headline metrics on FabR and CRR show clear improvement; ablations support each component; human audit aligns with NLI proxy | Yes — could still pivot scope based on Phase 3 writing |
```

- [ ] **Step 3: Schedule Phase 3 kickoff for week of 2027-05-03**

Phase 3 = M5 final polish + M6 paper drafting + M7 submission. Plan it as a separate document.

- [ ] **Step 4: Final Phase 2 weekly journal entry (week of 2027-04-26)**

```markdown
## Phase 2 Closeout — Week of 2027-04-26
- Phase 2 status: COMPLETE
- Total weeks elapsed: 34
- Total artifacts produced: 500-item benchmark, 5 baselines, full CiteCheck system, ablation suite, human audit, paper outline
- Phase 3 kickoff: 2027-05-03
- Energy / confidence: [1–10]
- Biggest learning of Phase 2: [...]
```

---

## Verification Checklist (run at end of Phase 2)

Before declaring Phase 2 complete, confirm the following exist with content:

- [ ] `citecheck/` directory tree fully populated; `pip install -e citecheck/` succeeds
- [ ] CAP indexed: `data/indices/bm25/` and `data/indices/dense/` non-empty; sample queries return hits
- [ ] CourtListener client works (cached responses present in `data/cl_cache/`)
- [ ] `data/eval/eval_set_v1.jsonl` has 500 records, all human-verified
- [ ] `data/eval/audit_subset_v1.jsonl` has 200 records with human Citation-Support + Likert labels
- [ ] Each baseline has a `results.json` under `experiments/runs/`
- [ ] CiteCheck full results, ablations (≥7 configs), seeds (≥3) all present
- [ ] `journal/phase2_retros.md` has M3, M4, M5-partial sections filled
- [ ] `journal/weekly.md` has weekly entries for all 34 weeks of Phase 2
- [ ] `journal/decisions.md` has at least 10 new decisions logged
- [ ] `citecheck/paper/outline.md` exists with all 7 sections drafted and figure/table list
- [ ] Annotator co-authorship decision logged (yes / no / who)

---

## Compute Budget Summary (Phase 2)

| Month | Task block | Est. GPU-hours |
|-------|------------|----------------|
| Sep   | infra + indexing + smoke | 10 |
| Oct   | vanilla + naive-RAG + Self-RAG | 40 |
| Nov   | CRAG + EL-RAG + M3 review | 35 |
| Dec   | LLM pre-labeling | 20 |
| Jan   | parser, resolver, grammar prototyping | 25 |
| Feb   | reranker QLoRA + agent integration | 60 |
| Mar   | full eval + ablations | 80 |
| Apr   | seeds + secondary backbone | 40 |
| **Total** | | **~310 GPU-hours** |

On a single RTX 4090 / A6000 (24GB) at ~22 hr/day usable, this is ~14 wall-clock days of pure compute spread over 34 weeks — comfortable margin. Colab Pro A100 burst recommended for the full-corpus dense embedding pass (Task 31) and the reranker λ-sweep (Task 30).

Cash budget estimate: $2,000–3,200 annotator + $80 API calls + $10/mo Colab Pro × 8 = ~$2,180–3,380.
