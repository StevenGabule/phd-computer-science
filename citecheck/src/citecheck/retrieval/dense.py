"""Dense retriever: sentence-transformers encoder + FAISS inner-product index.

Index-type choice
=================

For CiteCheck we keep two regimes:

* **IndexFlatIP** — exact inner-product search. Fine up to ~100k passages,
  trivially correct, and what we use for the eval-set sanity checks. No
  training step, deterministic, ~O(N·d) per query.
* **IndexIVFFlat** — inverted-file index with ``nlist=4096`` cells. The CAP
  corpus contains ~6.7M opinions; chunked at 512 tokens with 50 token overlap
  the passage count lands around 30M. For that scale we *need* an ANN index,
  and IVFFlat hits the sweet spot of accuracy vs RAM (no PQ compression — we
  have enough memory at this stage and want to keep recall@k high so the
  cross-encoder stage can do its job).

If you later want to push to 100M passages, swap in HNSW or IVFPQ; the
:meth:`DenseRetriever.build_index` helper makes the index type a parameter.
"""
from __future__ import annotations

import json
import logging
from collections.abc import Iterable, Iterator
from pathlib import Path
from typing import Any

import numpy as np

from citecheck.config import MODELS, PATHS, RETRIEVAL
from citecheck.retrieval.bm25 import RetrievalResult, _get_attr

logger = logging.getLogger(__name__)

# Threshold above which we switch from exact (FlatIP) to ANN (IVFFlat).
_IVF_THRESHOLD = 100_000
_IVF_NLIST = 4096
_IVF_NPROBE = 32


class DenseRetriever:
    """Dense bi-encoder retriever (FAISS-backed).

    The encoder is loaded lazily so that constructing the object is cheap and
    does not require a GPU.
    """

    def __init__(
        self,
        model_name: str | None = None,
        index_dir: Path | None = None,
        device: str = "auto",
    ) -> None:
        self.model_name: str = model_name or MODELS.dense_encoder
        self.index_dir: Path = Path(index_dir) if index_dir is not None else PATHS.dense_index
        self.device: str = self._resolve_device(device)
        self._encoder: Any = None
        self._index: Any = None
        self._doc_ids: list[str] | None = None
        self._metadata: list[dict[str, Any]] | None = None

    # ------------------------------------------------------------------ utils

    @staticmethod
    def _resolve_device(device: str) -> str:
        if device != "auto":
            return device
        try:
            import torch  # local import to avoid hard dep at module import time

            return "cuda" if torch.cuda.is_available() else "cpu"
        except ImportError:  # pragma: no cover
            return "cpu"

    @property
    def encoder(self) -> Any:
        if self._encoder is None:
            try:
                from sentence_transformers import SentenceTransformer
            except ImportError as exc:  # pragma: no cover
                raise ImportError(
                    "sentence-transformers is required for DenseRetriever"
                ) from exc
            logger.info("Loading SentenceTransformer %s on %s", self.model_name, self.device)
            self._encoder = SentenceTransformer(self.model_name, device=self.device)
        return self._encoder

    # ----------------------------------------------------------------- build

    def build_index(
        self,
        corpus_iter: Iterable[Any],
        batch_size: int = 32,
        normalize: bool = True,
        force_index_type: str | None = None,
    ) -> None:
        """Embed a corpus and persist a FAISS index + sidecar metadata.

        The corpus is materialized into memory in chunks of ``batch_size``;
        embeddings are streamed into a list before being concatenated. For
        production CAP-scale runs you should call this on a host with enough
        RAM (~120 GB for 30M × 768-dim float32 = ~92 GB embedding tensor)
        *or* shard the corpus and merge FAISS indices afterwards.

        Args:
            corpus_iter: Iterable of items exposing ``id`` and ``contents`` /
                ``plain_text`` (compatible with CAP opinion records).
            batch_size: Sentence-transformer encode batch size.
            normalize: L2-normalize embeddings so that inner product == cosine.
            force_index_type: Either ``"flat"`` or ``"ivf"``. By default we
                pick based on corpus size (``_IVF_THRESHOLD``).
        """
        try:
            import faiss  # noqa: PLC0415
        except ImportError as exc:  # pragma: no cover
            raise ImportError("faiss-cpu (or faiss-gpu) is required") from exc

        self.index_dir.mkdir(parents=True, exist_ok=True)
        doc_ids: list[str] = []
        metadata: list[dict[str, Any]] = []
        texts: list[str] = []

        for item in corpus_iter:
            doc_id = _get_attr(item, ("id", "doc_id", "cluster_id", "opinion_id"))
            text = _get_attr(item, ("plain_text", "contents", "text", "body"))
            if doc_id is None or not text:
                continue
            doc_ids.append(str(doc_id))
            texts.append(str(text))
            meta: dict[str, Any] = {}
            for k in ("court_id", "date_filed", "case_name", "cluster_id"):
                v = _get_attr(item, (k,))
                if v is not None:
                    meta[k] = v if isinstance(v, str | int | float) else str(v)
            metadata.append(meta)

        if not texts:
            raise ValueError("Corpus iterator yielded zero usable records")

        logger.info("Encoding %d passages with %s (batch=%d)", len(texts), self.model_name,
                    batch_size)
        embeddings = self.encoder.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=True,
            convert_to_numpy=True,
            normalize_embeddings=normalize,
        ).astype(np.float32)

        n, dim = embeddings.shape
        use_ivf = force_index_type == "ivf" or (force_index_type is None and n > _IVF_THRESHOLD)
        if use_ivf:
            logger.info("Building IndexIVFFlat (n=%d, dim=%d, nlist=%d)", n, dim, _IVF_NLIST)
            quantizer = faiss.IndexFlatIP(dim)
            index = faiss.IndexIVFFlat(quantizer, dim, _IVF_NLIST, faiss.METRIC_INNER_PRODUCT)
            # IVF requires training; use a random subsample if corpus is huge.
            train_size = min(n, max(_IVF_NLIST * 40, 100_000))
            train_idx = np.random.default_rng(0).choice(n, size=train_size, replace=False)
            index.train(embeddings[train_idx])
            index.add(embeddings)
            index.nprobe = _IVF_NPROBE
        else:
            logger.info("Building IndexFlatIP (n=%d, dim=%d)", n, dim)
            index = faiss.IndexFlatIP(dim)
            index.add(embeddings)

        index_path = self.index_dir / "faiss.index"
        ids_path = self.index_dir / "doc_ids.jsonl"
        meta_path = self.index_dir / "metadata.jsonl"
        cfg_path = self.index_dir / "config.json"

        faiss.write_index(index, str(index_path))
        with ids_path.open("w", encoding="utf-8") as fh:
            for did in doc_ids:
                fh.write(json.dumps(did, ensure_ascii=False) + "\n")
        with meta_path.open("w", encoding="utf-8") as fh:
            for m in metadata:
                fh.write(json.dumps(m, ensure_ascii=False) + "\n")
        cfg_path.write_text(
            json.dumps(
                {
                    "model_name": self.model_name,
                    "dim": int(dim),
                    "n_docs": int(n),
                    "index_type": "ivf" if use_ivf else "flat",
                    "normalize": bool(normalize),
                }
            )
        )
        logger.info("Dense index written to %s", self.index_dir)

        # Cache in-process so search() works immediately after build.
        self._index = index
        self._doc_ids = doc_ids
        self._metadata = metadata

    # ----------------------------------------------------------------- load

    def _load_index(self) -> None:
        try:
            import faiss
        except ImportError as exc:  # pragma: no cover
            raise ImportError("faiss is required to load the dense index") from exc

        index_path = self.index_dir / "faiss.index"
        ids_path = self.index_dir / "doc_ids.jsonl"
        meta_path = self.index_dir / "metadata.jsonl"
        if not index_path.exists():
            raise FileNotFoundError(
                f"Dense index not found at {index_path}. "
                "Run `python scripts/build_dense_index.py` first."
            )
        logger.info("Loading FAISS index from %s", index_path)
        self._index = faiss.read_index(str(index_path))
        self._doc_ids = [json.loads(line) for line in ids_path.read_text().splitlines() if line]
        if meta_path.exists():
            self._metadata = [
                json.loads(line) for line in meta_path.read_text().splitlines() if line
            ]
        else:
            self._metadata = [{} for _ in self._doc_ids]

    def _ensure_loaded(self) -> None:
        if self._index is None or self._doc_ids is None:
            self._load_index()

    # ----------------------------------------------------------------- search

    def _embed_queries(self, queries: list[str], normalize: bool = True) -> np.ndarray:
        emb = self.encoder.encode(
            queries,
            batch_size=min(64, max(1, len(queries))),
            convert_to_numpy=True,
            normalize_embeddings=normalize,
            show_progress_bar=False,
        )
        return np.asarray(emb, dtype=np.float32)

    def search(
        self,
        query: str,
        top_k: int = RETRIEVAL.dense_top_k,
    ) -> list[RetrievalResult]:
        """Embed a single query and return the top-k FAISS neighbors."""
        return self.batch_search([query], top_k=top_k)[0]

    def batch_search(
        self,
        queries: list[str],
        top_k: int = RETRIEVAL.dense_top_k,
        batch_size: int = 64,  # noqa: ARG002 - reserved for future chunking
    ) -> list[list[RetrievalResult]]:
        """Embed and search a batch of queries against the FAISS index."""
        self._ensure_loaded()
        assert self._index is not None and self._doc_ids is not None  # for type checkers
        q_emb = self._embed_queries(queries)
        scores, idxs = self._index.search(q_emb, top_k)
        all_results: list[list[RetrievalResult]] = []
        for q_scores, q_idxs in zip(scores, idxs, strict=True):
            res: list[RetrievalResult] = []
            for rank, (s, i) in enumerate(zip(q_scores, q_idxs, strict=True), start=1):
                if i < 0:
                    continue  # FAISS pads with -1 when fewer than k results
                res.append(
                    RetrievalResult(
                        doc_id=self._doc_ids[i],
                        score=float(s),
                        rank=rank,
                        passage=None,
                        metadata=self._metadata[i] if self._metadata else {},
                    )
                )
            all_results.append(res)
        return all_results


def _iter_jsonl(path: Path) -> Iterator[dict[str, Any]]:
    """Small helper for scripts: stream a JSONL file as dict records."""
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                yield json.loads(line)
