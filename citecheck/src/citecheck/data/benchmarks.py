"""Loaders for downstream legal-NLP benchmarks (LegalBench-RAG, CUAD).

Both datasets ship on the Hugging Face Hub; we standardize them into a common
:class:`BenchmarkExample` so the rest of CiteCheck (retrieval, reranker, eval)
can iterate over a single shape.

Schema assumptions are documented inline; see TODOs where the public release
schema is ambiguous and should be re-verified against the live dataset card
before Phase 2 task "benchmark integration".
"""
from __future__ import annotations

import json
import logging
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class BenchmarkExample:
    """Common shape for downstream RAG/QA benchmarks.

    Attributes:
        id: Globally-unique ID (prefixed by ``source`` to avoid collisions).
        source: ``"legalbench-rag"`` or ``"cuad"``.
        question: Natural-language query or instruction.
        gold_passages: List of gold-relevant passages (verbatim text spans).
        gold_answer: Reference answer string (may be empty for retrieval-only).
        metadata: Free-form extra fields (e.g. contract type, jurisdiction).
    """

    id: str
    source: str
    question: str
    gold_passages: list[str]
    gold_answer: str
    metadata: dict[str, Any] = field(default_factory=dict)


def _load_hf_dataset(
    name: str,
    split: str,
    cache_dir: Path | None = None,
    **load_kwargs: Any,
) -> Any:
    """Thin wrapper around ``datasets.load_dataset`` with a uniform import path.

    Imported lazily so that callers who only need the BenchmarkExample dataclass
    don't pay the ~500ms ``datasets`` import cost.
    """
    from datasets import load_dataset  # type: ignore[import-untyped]

    logger.info("Loading HF dataset %s split=%s", name, split)
    return load_dataset(
        name,
        split=split,
        cache_dir=str(cache_dir) if cache_dir is not None else None,
        **load_kwargs,
    )


def load_legalbench_rag(
    split: str = "test",
    cache_dir: Path | None = None,
) -> list[BenchmarkExample]:
    """Load LegalBench-RAG examples and normalize to :class:`BenchmarkExample`.

    Uses the ``zeroentropy/legalbenchrag`` dataset on the HF Hub. The published
    card describes records with at least ``query``, ``snippets`` (list of
    {text, file_path, span}), and ``corpus`` identifiers. We map:

    * ``question``  <- ``query``
    * ``gold_passages`` <- the ``text`` of each snippet
    * ``gold_answer`` <- empty (retrieval-only benchmark)
    * ``metadata`` <- snippets' file_path/span + corpus name

    TODO(Phase 2 benchmark integration): re-verify exact field names against
    the live dataset card; the project has shipped at least one schema rev.
    """
    ds = _load_hf_dataset("zeroentropy/legalbenchrag", split=split, cache_dir=cache_dir)
    out: list[BenchmarkExample] = []
    for i, row in enumerate(ds):
        if not isinstance(row, dict):
            row = dict(row)
        query = row.get("query") or row.get("question") or ""
        snippets = row.get("snippets") or row.get("contexts") or []
        if isinstance(snippets, dict):
            # Some HF releases store snippets as parallel lists under a dict.
            snippets = [
                {"text": t, "file_path": fp, "span": sp}
                for t, fp, sp in zip(
                    snippets.get("text", []),
                    snippets.get("file_path", []),
                    snippets.get("span", [None] * len(snippets.get("text", []))),
                    strict=False,
                )
            ]
        gold_passages = [
            (s.get("text") if isinstance(s, dict) else str(s)) or "" for s in snippets
        ]
        meta = {
            "corpus": row.get("corpus") or row.get("corpus_name") or "",
            "snippet_locations": [
                {
                    "file_path": s.get("file_path") if isinstance(s, dict) else None,
                    "span": s.get("span") if isinstance(s, dict) else None,
                }
                for s in snippets
            ],
        }
        ex_id = row.get("id") or row.get("qid") or f"lbr-{split}-{i}"
        out.append(
            BenchmarkExample(
                id=f"legalbench-rag::{ex_id}",
                source="legalbench-rag",
                question=str(query),
                gold_passages=gold_passages,
                gold_answer="",
                metadata=meta,
            )
        )
    logger.info("Loaded %d LegalBench-RAG examples", len(out))
    return out


def load_cuad(
    version: str = "v1",
    cache_dir: Path | None = None,
) -> list[BenchmarkExample]:
    """Load CUAD (Contract Understanding Atticus Dataset) and normalize.

    Uses ``theatticusproject/cuad-qa`` (SQuAD-style). Records have:
    ``id``, ``title``, ``context``, ``question``, ``answers`` (dict with
    ``text`` and ``answer_start`` lists). We map answer texts to
    ``gold_passages`` (since each answer is a span lifted from the contract)
    and use the first answer as ``gold_answer``.

    Args:
        version: Dataset version tag (kept for future-proofing; ignored if the
            HF release does not expose configurations).
        cache_dir: HF cache directory override.
    """
    # CUAD on HF is a single config; version is forwarded as metadata only.
    ds = _load_hf_dataset("theatticusproject/cuad-qa", split="train", cache_dir=cache_dir)
    out: list[BenchmarkExample] = []
    for i, row in enumerate(ds):
        if not isinstance(row, dict):
            row = dict(row)
        answers = row.get("answers") or {}
        if isinstance(answers, dict):
            texts = list(answers.get("text") or [])
        else:
            texts = [str(a.get("text", "")) for a in answers if isinstance(a, dict)]
        gold_answer = texts[0] if texts else ""
        ex_id = row.get("id") or f"cuad-{i}"
        out.append(
            BenchmarkExample(
                id=f"cuad::{ex_id}",
                source="cuad",
                question=str(row.get("question") or ""),
                gold_passages=texts,
                gold_answer=gold_answer,
                metadata={
                    "title": row.get("title", ""),
                    "context": row.get("context", ""),
                    "version": version,
                },
            )
        )
    logger.info("Loaded %d CUAD examples", len(out))
    return out


def to_jsonl(examples: list[BenchmarkExample], dest: Path) -> None:
    """Write :class:`BenchmarkExample` records to a newline-delimited JSON file.

    Creates parent directories as needed. Each line is a single JSON object
    produced by :func:`dataclasses.asdict` (preserves field order).
    """
    dest.parent.mkdir(parents=True, exist_ok=True)
    with dest.open("w", encoding="utf-8") as fh:
        for ex in examples:
            fh.write(json.dumps(asdict(ex), ensure_ascii=False) + "\n")
    logger.info("Wrote %d examples to %s", len(examples), dest)


__all__ = ["BenchmarkExample", "load_legalbench_rag", "load_cuad", "to_jsonl"]
