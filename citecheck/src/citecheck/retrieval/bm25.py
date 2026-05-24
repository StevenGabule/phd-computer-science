"""BM25 retriever backed by Pyserini / Lucene.

Why Pyserini?
    * It is the de-facto research baseline for BM25 over large corpora.
    * It supports both an in-process Java-backed ``LuceneSearcher`` and an
      out-of-process indexer (``python -m pyserini.index.lucene``), giving us a
      single artifact we can ship to the cluster.
    * Tunable ``k1`` / ``b`` parameters — we leave them at Pyserini's defaults
      (0.9 / 0.4) because legal text behaves similarly to MS MARCO passages.

Corpus contract
    Pyserini expects JSONL records with at least the keys ``id`` and
    ``contents``. We obtain them by streaming our CAP parquet via
    ``citecheck.data.cap_loader.iter_cap_opinions`` (written by the data agent)
    through :func:`corpus_to_pyserini_jsonl`.
"""
from __future__ import annotations

import json
import logging
import subprocess
import sys
from collections.abc import Iterable, Iterator
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from citecheck.config import PATHS, RETRIEVAL

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class RetrievalResult:
    """A single result returned by any retriever (BM25, dense, hybrid).

    Attributes:
        doc_id: Stable string identifier of the retrieved passage / opinion.
        score: Retriever-native score (BM25, inner product, RRF, etc.). Higher
            means more relevant. The numeric scale is **not** comparable across
            retrievers; only the ranking is.
        rank: 1-based rank within the ranked list this result came from.
        passage: Optional passage text (populated when the retriever has it).
        metadata: Free-form provenance — ``court_id``, ``date_filed``,
            ``cluster_id`` etc., as available.
    """

    doc_id: str
    score: float
    rank: int
    passage: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


def corpus_to_pyserini_jsonl(opinions: Iterator[Any], dest: Path) -> int:
    """Convert a stream of CAP opinions into Pyserini JSONL format.

    Pyserini's Lucene indexer expects one JSON object per line with the schema::

        {"id": "<doc_id>", "contents": "<text>"}

    Optional extra fields (we include ``court_id`` and ``date_filed`` when
    available) are stored as ``StoredField`` and round-trip through search.

    Args:
        opinions: Iterator yielding objects with at minimum ``id`` (or
            ``cluster_id``) and ``plain_text`` / ``contents`` attributes —
            matches the contract of ``data.cap_loader.iter_cap_opinions``.
        dest: Output JSONL path. Parent dirs are created if missing.

    Returns:
        Number of records written.
    """
    dest.parent.mkdir(parents=True, exist_ok=True)
    n = 0
    with dest.open("w", encoding="utf-8") as fh:
        for op in opinions:
            doc_id = _get_attr(op, ("id", "doc_id", "cluster_id", "opinion_id"))
            contents = _get_attr(op, ("plain_text", "contents", "text", "body"))
            if doc_id is None or not contents:
                continue
            record: dict[str, Any] = {"id": str(doc_id), "contents": str(contents)}
            for extra in ("court_id", "date_filed", "case_name", "cluster_id"):
                val = _get_attr(op, (extra,))
                if val is not None:
                    record[extra] = val if isinstance(val, str | int | float) else str(val)
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")
            n += 1
            if n % 100_000 == 0:
                logger.info("corpus_to_pyserini_jsonl: wrote %d records", n)
    logger.info("corpus_to_pyserini_jsonl: total %d records -> %s", n, dest)
    return n


def _get_attr(obj: Any, names: Iterable[str]) -> Any:
    """Return the first attribute/key in ``names`` that exists on ``obj``."""
    for name in names:
        if hasattr(obj, name):
            value = getattr(obj, name)
            if value is not None:
                return value
        if isinstance(obj, dict) and name in obj and obj[name] is not None:
            return obj[name]
    return None


class BM25Retriever:
    """Pyserini-backed BM25 retriever.

    Lazy-loads the Java-backed ``LuceneSearcher`` so that constructing the
    object does not pay JVM startup cost (important for tests / CLIs that only
    want to call :meth:`build_index`).
    """

    def __init__(self, index_dir: Path | None = None) -> None:
        self.index_dir: Path = Path(index_dir) if index_dir is not None else PATHS.bm25_index
        self._searcher: Any = None

    @property
    def searcher(self) -> Any:
        """Lazily-instantiated ``pyserini.search.lucene.LuceneSearcher``."""
        if self._searcher is None:
            if not self.index_dir.exists():
                raise FileNotFoundError(
                    f"BM25 index not found at {self.index_dir}. "
                    "Run `python scripts/build_bm25_index.py` first."
                )
            try:
                from pyserini.search.lucene import LuceneSearcher
            except ImportError as exc:  # pragma: no cover - import-time guard
                raise ImportError(
                    "pyserini is required for BM25Retriever. "
                    "Install with `pip install pyserini` and ensure a JDK 21 is on PATH."
                ) from exc
            logger.info("Loading LuceneSearcher from %s", self.index_dir)
            self._searcher = LuceneSearcher(str(self.index_dir))
        return self._searcher

    def build_index(self, corpus_jsonl: Path, threads: int = 4) -> None:
        """Build a Lucene BM25 index from a Pyserini-format JSONL corpus.

        Shells out to ``python -m pyserini.index.lucene`` so that indexing
        happens in a fresh JVM with its own heap (Pyserini's recommended
        approach for large corpora). Works on both CPU and GPU machines.

        Args:
            corpus_jsonl: Path to the input JSONL file. May also be a directory
                of shards; Pyserini handles both.
            threads: Number of indexer threads. Pyserini scales near-linearly
                up to ~16 on modern CPUs.
        """
        corpus_jsonl = Path(corpus_jsonl)
        if not corpus_jsonl.exists():
            raise FileNotFoundError(f"Corpus path does not exist: {corpus_jsonl}")
        self.index_dir.mkdir(parents=True, exist_ok=True)

        # Pyserini takes a *directory* of JSONL files as -input. If we were
        # given a single file, pass its parent.
        input_dir = corpus_jsonl if corpus_jsonl.is_dir() else corpus_jsonl.parent

        cmd = [
            sys.executable,
            "-m",
            "pyserini.index.lucene",
            "--collection", "JsonCollection",
            "--input", str(input_dir),
            "--index", str(self.index_dir),
            "--generator", "DefaultLuceneDocumentGenerator",
            "--threads", str(threads),
            "--storePositions",
            "--storeDocvectors",
            "--storeRaw",
        ]
        logger.info("Running Pyserini indexer: %s", " ".join(cmd))
        result = subprocess.run(cmd, check=False, capture_output=True, text=True)
        if result.returncode != 0:
            logger.error("Pyserini indexer failed:\nSTDOUT:\n%s\nSTDERR:\n%s",
                         result.stdout, result.stderr)
            raise RuntimeError(
                f"Pyserini indexer exited with code {result.returncode}. "
                "Check that a JDK 21 is installed and on PATH."
            )
        logger.info("BM25 index built at %s", self.index_dir)

    def search(
        self,
        query: str,
        top_k: int = RETRIEVAL.bm25_top_k,
    ) -> list[RetrievalResult]:
        """Run a single BM25 query.

        Args:
            query: Natural-language query string.
            top_k: Maximum number of results to return.

        Returns:
            List of :class:`RetrievalResult` sorted by descending BM25 score.
        """
        hits = self.searcher.search(query, k=top_k)
        results: list[RetrievalResult] = []
        for rank, hit in enumerate(hits, start=1):
            passage = self._extract_contents(hit)
            results.append(
                RetrievalResult(
                    doc_id=str(hit.docid),
                    score=float(hit.score),
                    rank=rank,
                    passage=passage,
                    metadata={"raw": getattr(hit, "raw", None)},
                )
            )
        return results

    def batch_search(
        self,
        queries: list[str],
        top_k: int = RETRIEVAL.bm25_top_k,
        threads: int = 4,
    ) -> list[list[RetrievalResult]]:
        """Run a batch of BM25 queries in parallel.

        Wraps ``LuceneSearcher.batch_search`` which uses a thread pool inside
        the JVM. Returns results in the same order as ``queries``.
        """
        qids = [f"q{i}" for i in range(len(queries))]
        batch = self.searcher.batch_search(queries, qids=qids, k=top_k, threads=threads)
        all_results: list[list[RetrievalResult]] = []
        for qid in qids:
            hits = batch[qid]
            res_list: list[RetrievalResult] = []
            for rank, hit in enumerate(hits, start=1):
                res_list.append(
                    RetrievalResult(
                        doc_id=str(hit.docid),
                        score=float(hit.score),
                        rank=rank,
                        passage=self._extract_contents(hit),
                        metadata={"raw": getattr(hit, "raw", None)},
                    )
                )
            all_results.append(res_list)
        return all_results

    @staticmethod
    def _extract_contents(hit: Any) -> str | None:
        """Pull ``contents`` out of a Pyserini hit if ``--storeRaw`` was used."""
        raw = getattr(hit, "raw", None)
        if not raw:
            return None
        try:
            parsed = json.loads(raw)
            return parsed.get("contents")
        except (json.JSONDecodeError, TypeError):
            return raw if isinstance(raw, str) else None
