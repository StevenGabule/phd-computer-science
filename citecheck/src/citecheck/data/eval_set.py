"""CiteCheck evaluation set: schema, IO, and seeding utilities.

The eval set is a JSONL file at :attr:`PATHS.eval_set` (default
``data/eval_v0.1.jsonl``). Each record is a :class:`CiteCheckExample` carrying
a legal question plus its gold citations (Bluebook strings + the matching
CourtListener opinion IDs).

Seeding pipeline:

1. :func:`seed_from_charlotin` — parse the Damien Charlotin AI-hallucination
   tracker into raw candidates.
2. :func:`llm_prelabel` — use a teacher LLM to draft question/citation pairs
   from underlying briefs/opinions.
3. :func:`human_verify_subset` — present a sample for manual audit.

Steps 2 and 3 are scaffolded (stubbed where they need external resources);
step 1 expects a CSV the user has to download manually because the tracker is
not redistributed.
"""
from __future__ import annotations

import csv
import json
import logging
from collections.abc import Iterator
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Protocol

from citecheck.config import PATHS

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class GoldCitation:
    """A single gold citation: Bluebook string plus its CourtListener opinion ID."""

    citation: str
    cl_opinion_id: int | None = None


@dataclass(frozen=True)
class CiteCheckExample:
    """One CiteCheck eval-set record.

    Attributes:
        id: Stable example ID (e.g. ``"charlotin-0042"``).
        question: Legal question or brief excerpt requiring a citation.
        gold_citations: List of :class:`GoldCitation` -- canonical answers.
        jurisdiction: Bluebook jurisdiction tag (e.g. ``"us"``, ``"ny"``, ``"2dcir"``).
        source: Where this example came from
            (``"charlotin"`` | ``"synthetic"`` | ``"manual"``).
        metadata: Free-form (annotator, brief URL, original docket, etc.).
    """

    id: str
    question: str
    gold_citations: list[GoldCitation]
    jurisdiction: str
    source: str
    metadata: dict[str, Any] = field(default_factory=dict)


class _LLMClient(Protocol):
    """Minimal LLM-client interface used by :func:`llm_prelabel`."""

    def complete(self, prompt: str) -> str:
        """Run a single completion and return the model's text output."""
        ...


def load_eval_set(path: Path | None = None) -> list[CiteCheckExample]:
    """Load the CiteCheck eval set from JSONL.

    Args:
        path: Override the default ``PATHS.eval_set`` location.

    Returns:
        Parsed list of :class:`CiteCheckExample`.

    Raises:
        FileNotFoundError: if ``path`` does not exist.
    """
    p = path if path is not None else PATHS.eval_set
    if not p.exists():
        raise FileNotFoundError(
            f"Eval set not found at {p}. Build it first via seed_from_charlotin + "
            "llm_prelabel + human_verify_subset (Phase 2 task: 'build eval set')."
        )

    out: list[CiteCheckExample] = []
    with p.open("r", encoding="utf-8") as fh:
        for i, line in enumerate(fh):
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Bad JSON at {p}:{i + 1}: {exc}") from exc
            raw_cites = row.get("gold_citations") or []
            cites = [
                GoldCitation(
                    citation=str(c.get("citation", "")),
                    cl_opinion_id=(int(c["cl_opinion_id"]) if c.get("cl_opinion_id") else None),
                )
                for c in raw_cites
            ]
            out.append(
                CiteCheckExample(
                    id=str(row["id"]),
                    question=str(row["question"]),
                    gold_citations=cites,
                    jurisdiction=str(row.get("jurisdiction", "")),
                    source=str(row.get("source", "manual")),
                    metadata=dict(row.get("metadata", {})),
                )
            )
    logger.info("Loaded %d eval examples from %s", len(out), p)
    return out


def save_eval_set(examples: list[CiteCheckExample], path: Path) -> None:
    """Serialize examples to JSONL at ``path`` (creates parent dirs)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        for ex in examples:
            fh.write(json.dumps(asdict(ex), ensure_ascii=False) + "\n")
    logger.info("Wrote %d examples to %s", len(examples), path)


def seed_from_charlotin(
    tracker_csv: Path,
    max_examples: int = 100,
) -> list[CiteCheckExample]:
    """Seed eval-set candidates from the Damien Charlotin AI-hallucination tracker.

    The tracker is a manually curated CSV of court orders sanctioning attorneys
    for AI-fabricated citations. CiteCheck uses it as the seed for "hard" eval
    examples (questions where an LLM previously hallucinated). Expected columns::

        case_id, jurisdiction, fabricated_citations, brief_url

    ``fabricated_citations`` is a ``|``-separated list of Bluebook strings.

    Args:
        tracker_csv: Path to the manually-downloaded tracker CSV.
        max_examples: Stop after parsing this many rows (default 100).

    Returns:
        List of :class:`CiteCheckExample` with ``source="charlotin"``. Note
        that ``cl_opinion_id`` is ``None`` for every gold citation here -- the
        whole point is that these strings are *fabricated*; downstream code
        treats a ``None`` cl_opinion_id as "should not resolve".

    Raises:
        NotImplementedError: if ``tracker_csv`` does not exist. The tracker is
            not redistributed; the user must download it manually. See:
            https://www.damiencharlotin.com/hallucinations/ (TODO: confirm
            canonical URL during Phase 2 task 'build eval set').
    """
    if not tracker_csv.exists():
        raise NotImplementedError(
            "Manual download of tracker CSV required; see TODO in docstring. "
            f"Expected file at {tracker_csv}. Phase 2 task: 'build eval set / "
            "seed from Charlotin tracker'."
        )

    out: list[CiteCheckExample] = []
    with tracker_csv.open("r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        for i, row in enumerate(reader):
            if i >= max_examples:
                break
            cite_strs = [
                s.strip() for s in (row.get("fabricated_citations") or "").split("|") if s.strip()
            ]
            gold = [GoldCitation(citation=s, cl_opinion_id=None) for s in cite_strs]
            out.append(
                CiteCheckExample(
                    id=f"charlotin-{row.get('case_id', i):0>4}",
                    question="",  # filled in by llm_prelabel from the brief
                    gold_citations=gold,
                    jurisdiction=str(row.get("jurisdiction", "")),
                    source="charlotin",
                    metadata={"brief_url": row.get("brief_url", "")},
                )
            )
    logger.info("Seeded %d candidates from Charlotin tracker at %s", len(out), tracker_csv)
    return out


def llm_prelabel(
    examples: list[CiteCheckExample],
    llm_client: _LLMClient,
    n: int = 500,
) -> list[CiteCheckExample]:
    """LLM-draft question/citation pairs for up to ``n`` examples.

    Expected prompt (one paragraph, sketched here for the implementer): given
    the brief URL or excerpt in ``ex.metadata["brief_url"]`` (or
    ``metadata["brief_text"]`` if pre-fetched) and the list of citation strings
    in ``ex.gold_citations``, ask the teacher LLM to (a) extract the legal
    proposition each citation supports, (b) restate it as a self-contained
    natural-language question, and (c) return JSON of the form
    ``{"question": "...", "rationale": "..."}``. The function fills the
    returned ``question`` into ``ex.question`` and threads ``rationale`` into
    ``ex.metadata``.

    Args:
        examples: Candidates (typically from :func:`seed_from_charlotin`).
        llm_client: Any object with a ``complete(prompt: str) -> str`` method.
        n: Maximum number of examples to pre-label.

    Returns:
        Updated copies of the input examples (input list is not mutated).
    """
    # TODO(Phase 2, task: 'build eval set / LLM prelabel'): wire this to the
    # OpenRouter/Anthropic/OpenAI client of choice, validate the JSON shape,
    # and back off on rate limits. The current stub raises so callers cannot
    # accidentally treat unlabeled examples as labeled.
    raise NotImplementedError(
        "llm_prelabel is a Phase 2 stub. Implement the teacher prompt + "
        f"JSON-shape validation before running on examples (received {len(examples)}, "
        f"would process {min(n, len(examples))}). See docstring for the expected "
        "prompt contract."
    )


def human_verify_subset(
    examples: list[CiteCheckExample],
    n: int = 50,
) -> Iterator[CiteCheckExample]:
    """Yield ``n`` examples for human verification via a CLI loop.

    Intended CLI flow (consumer's responsibility, not implemented here):

    1. For each yielded example, print ``ex.question`` and each
       ``ex.gold_citations[i].citation`` on its own line.
    2. Prompt the annotator with ``[k]eep / [e]dit citation / [d]rop`` per
       citation. ``edit`` re-reads stdin to capture the corrected Bluebook
       string; ``drop`` removes the citation from the example.
    3. Persist the annotator's verdict (e.g. ``verified=True``,
       ``annotator="JPG"``, ``timestamp=...``) into ``ex.metadata``.

    For Jupyter use, the consumer can wrap each yielded example with ipywidgets
    instead of stdin. This generator deliberately doesn't do IO so it can be
    reused from either context.

    Args:
        examples: Examples to sample from.
        n: How many to yield. If ``n > len(examples)``, yields everything.
    """
    # Deterministic head-slice; callers who want randomness should shuffle first.
    yield from examples[: max(0, n)]


__all__ = [
    "CiteCheckExample",
    "GoldCitation",
    "human_verify_subset",
    "llm_prelabel",
    "load_eval_set",
    "save_eval_set",
    "seed_from_charlotin",
]
