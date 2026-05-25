"""Reranker training data construction + ``torch.utils.data.Dataset``.

We build (query, passage, relevance, groundedness) tuples from the CiteCheck
eval set + BM25 negatives, then tokenize them on the fly.

Groundedness label
==================
For each (query, passage) pair we run ``eyecite.get_citations`` on the
passage to extract Bluebook citations, resolve each through CourtListener,
and check whether any resolved opinion appears in the eval example's gold
``support_opinion_ids``. The label is the fraction of in-passage citations
that successfully resolve to a supporting opinion — a soft real-valued
[0, 1] signal that the cross-encoder can learn to predict.

Calls to ``CourtListenerClient.resolve_citation`` are *not* batched and are
the main cost of this routine; in practice we cache them on disk under
``PATHS.cl_cache`` (managed by the client itself) so re-runs are cheap.
"""
from __future__ import annotations

import logging
import random
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

import torch
from torch.utils.data import Dataset

from citecheck.config import RERANKER

if TYPE_CHECKING:  # imports kept out of runtime cycles
    from citecheck.data import CiteCheckExample, CourtListenerClient
    from citecheck.retrieval.bm25 import BM25Retriever

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class RerankerExample:
    """A single training example for the multi-objective reranker.

    Attributes:
        query: The textual claim or query.
        passage: Candidate passage text.
        relevance_label: 1 if the passage is on-topic for the query, else 0.
        citation_grounding_label: Fraction in [0, 1] of citations in the
            passage that resolve to an opinion supporting the query. 0 when no
            citations are present.
        citation_metadata: Free-form dict — e.g., the list of parsed eyecite
            citation dicts, the resolved CourtListener cluster IDs, etc.
    """

    query: str
    passage: str
    relevance_label: int
    citation_grounding_label: float = 0.0
    citation_metadata: dict[str, Any] = field(default_factory=dict)


class RerankerDataset(Dataset[dict[str, torch.Tensor]]):
    """PyTorch dataset that tokenizes (query, passage) pairs on demand.

    Returned batch items use the keys ``input_ids``, ``attention_mask``,
    ``relevance_label`` (long, 0/1), and ``groundedness_label`` (float).
    """

    def __init__(
        self,
        examples: list[RerankerExample],
        tokenizer: Any,
        max_length: int = RERANKER.max_length,
    ) -> None:
        if not examples:
            raise ValueError("RerankerDataset received zero examples")
        self.examples = examples
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self) -> int:
        return len(self.examples)

    def __getitem__(self, idx: int) -> dict[str, torch.Tensor]:
        ex = self.examples[idx]
        enc = self.tokenizer(
            ex.query,
            ex.passage,
            truncation=True,
            padding="max_length",
            max_length=self.max_length,
            return_tensors="pt",
        )
        return {
            "input_ids": enc["input_ids"].squeeze(0),
            "attention_mask": enc["attention_mask"].squeeze(0),
            "relevance_label": torch.tensor(ex.relevance_label, dtype=torch.float32),
            "groundedness_label": torch.tensor(
                ex.citation_grounding_label, dtype=torch.float32
            ),
        }


# ---------------------------------------------------------------- builders


def _extract_citations(passage: str) -> list[Any]:
    """Run ``eyecite.get_citations`` on a passage, swallowing parser hiccups."""
    try:
        from eyecite import get_citations  # local import keeps top-level light
    except ImportError as exc:  # pragma: no cover
        raise ImportError(
            "eyecite is required to label citation groundedness"
        ) from exc
    try:
        return list(get_citations(passage))
    except Exception as exc:  # noqa: BLE001 — eyecite occasionally throws on odd text
        logger.debug("eyecite.get_citations failed on a passage (%s); returning []", exc)
        return []


def _gold_opinion_ids(ex: CiteCheckExample) -> set[str]:
    """Pull supporting opinion IDs out of a CiteCheckExample regardless of attr name."""
    for attr in (
        "support_opinion_ids",
        "gold_opinion_ids",
        "supporting_opinion_ids",
        "support_ids",
    ):
        if hasattr(ex, attr):
            val = getattr(ex, attr)
            if val:
                return {str(v) for v in val}
    return set()


def _grounding_score(
    passage: str,
    gold_ids: set[str],
    cl_client: CourtListenerClient,
) -> tuple[float, dict[str, Any]]:
    """Compute the soft grounding label for a single passage."""
    citations = _extract_citations(passage)
    if not citations:
        return 0.0, {"n_citations": 0, "resolved": []}

    resolved_records: list[dict[str, Any]] = []
    supporting = 0
    for cit in citations:
        cite_str = getattr(cit, "matched_text", None)
        if cite_str is None and hasattr(cit, "corrected_citation"):
            cite_str = cit.corrected_citation()
        if not cite_str:
            continue
        try:
            # NOTE: CourtListener is rate-limited to 5,000 req/hour (see
            # `API_CFG.courtlistener_rate_limit_per_hour`). The client itself
            # is expected to handle backoff + on-disk caching (PATHS.cl_cache);
            # we just call it.
            resolved = cl_client.resolve_citation(cite_str)
        except Exception as exc:  # noqa: BLE001
            logger.debug("resolve_citation(%r) failed: %s", cite_str, exc)
            resolved = None
        record: dict[str, Any] = {"citation": cite_str, "resolved_id": None}
        if resolved is not None:
            resolved_id = (
                getattr(resolved, "opinion_id", None)
                or getattr(resolved, "cluster_id", None)
                or getattr(resolved, "id", None)
            )
            record["resolved_id"] = str(resolved_id) if resolved_id is not None else None
            if record["resolved_id"] and record["resolved_id"] in gold_ids:
                supporting += 1
        resolved_records.append(record)

    score = supporting / max(1, len(resolved_records))
    return score, {"n_citations": len(citations), "resolved": resolved_records}


def build_reranker_training_data(
    eval_examples: list[CiteCheckExample],
    bm25_retriever: BM25Retriever,
    cl_client: CourtListenerClient,
    n_pos: int = 1,
    n_hard_neg: int = 2,
    n_easy_neg: int = 1,
    bm25_top_k: int = 50,
    seed: int = 0,
) -> list[RerankerExample]:
    """Mine (positive, hard-negative, easy-negative) triples from eval examples.

    For each eval example:

    1. Run BM25 with the query/claim text. The retrieved set is our candidate
       pool for both positives and hard negatives.
    2. Positives = top-ranked passages whose ``doc_id`` is in the example's
       gold ``support_opinion_ids``.
    3. Hard negatives = top-ranked passages whose ``doc_id`` is *not* in gold
       (BM25 thought they were relevant; they aren't).
    4. Easy negatives = sampled from much further down the ranking
       (rank > ``bm25_top_k``) as random pool of unrelated text.

    Each (query, passage) pair is then annotated with a soft citation
    groundedness label via :func:`_grounding_score`.

    Args:
        eval_examples: List of ``CiteCheckExample`` from the eval set.
        bm25_retriever: A built :class:`~citecheck.retrieval.bm25.BM25Retriever`.
        cl_client: A :class:`~citecheck.data.CourtListenerClient` for
            resolving in-passage citations.
        n_pos: Positives to keep per example.
        n_hard_neg: Hard negatives per example.
        n_easy_neg: Easy negatives per example.
        bm25_top_k: How deep into the BM25 ranking to draw negatives.
        seed: RNG seed for easy-negative sampling reproducibility.

    Returns:
        A flat list of :class:`RerankerExample` ready to feed to
        :class:`RerankerDataset`.
    """
    rng = random.Random(seed)
    out: list[RerankerExample] = []

    for ex in eval_examples:
        query = getattr(ex, "claim", None) or getattr(ex, "query", None) or getattr(ex, "text", "")
        if not query:
            logger.warning("Skipping eval example with no query/claim text")
            continue
        gold_ids = _gold_opinion_ids(ex)
        hits = bm25_retriever.search(query, top_k=bm25_top_k * 2)

        pos_hits = [h for h in hits if h.doc_id in gold_ids][:n_pos]
        hard_neg_pool = [h for h in hits[:bm25_top_k] if h.doc_id not in gold_ids]
        rng.shuffle(hard_neg_pool)
        hard_negs = hard_neg_pool[:n_hard_neg]

        easy_pool = [h for h in hits[bm25_top_k:] if h.doc_id not in gold_ids]
        rng.shuffle(easy_pool)
        easy_negs = easy_pool[:n_easy_neg]

        for hit, rel in [
            *[(h, 1) for h in pos_hits],
            *[(h, 0) for h in hard_negs],
            *[(h, 0) for h in easy_negs],
        ]:
            passage = hit.passage or ""
            grounding, meta = _grounding_score(passage, gold_ids, cl_client) if passage else (
                0.0,
                {"n_citations": 0, "resolved": []},
            )
            out.append(
                RerankerExample(
                    query=query,
                    passage=passage,
                    relevance_label=rel,
                    citation_grounding_label=grounding,
                    citation_metadata=meta,
                )
            )

    logger.info("Built %d reranker examples from %d eval examples", len(out), len(eval_examples))
    return out
