"""Caselaw Access Project (CAP) bulk loader.

The CAP exports per-jurisdiction ``.tar.gz`` archives at https://case.law/exports/
containing JSONL.gz files with one opinion per line. This module:

1. Downloads the bulk dump (resumable, with progress) via :func:`download_cap_bulk`.
2. Normalizes the JSONL into a column-oriented Parquet store
   (:func:`parse_cap_jsonl_to_parquet`).
3. Streams normalized opinions back out via :func:`iter_cap_opinions`.

The full bulk dump is ~100 GB and multi-day to download. Default behavior
restricts to ``["us"]`` (U.S. Supreme Court) for testing; pass
``only_jurisdictions=None`` to download everything.
"""
from __future__ import annotations

import gzip
import json
import logging
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path

import httpx
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential
from tqdm import tqdm

from citecheck.config import PATHS

logger = logging.getLogger(__name__)

CAP_EXPORTS_BASE = "https://case.law/exports"
CAP_DEFAULT_JURISDICTIONS: list[str] = ["us"]  # U.S. Supreme Court only by default
# Streaming download chunk size (1 MiB)
_CHUNK_BYTES = 1024 * 1024


@dataclass(frozen=True)
class CAPOpinion:
    """Normalized CAP opinion record.

    Attributes:
        id: CAP case ID (string; CAP uses opaque IDs, not all numeric).
        case_name: Human-readable case name (e.g. "Brown v. Board of Education").
        court: Court name as it appears in CAP metadata.
        year: Decision year (int).
        jurisdiction: CAP jurisdiction slug (e.g. "us", "ny", "cal").
        headnotes: Editor-prepared summary text, if present (may be empty).
        body_text: Full opinion text (concatenated majority + concurrences).
    """

    id: str
    case_name: str
    court: str
    year: int
    jurisdiction: str
    headnotes: str
    body_text: str


@retry(
    retry=retry_if_exception_type((httpx.TransportError, httpx.HTTPStatusError)),
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=2, min=4, max=60),
    reraise=True,
)
def _download_one(url: str, dest: Path, client: httpx.Client) -> None:
    """Stream-download a single URL to ``dest`` with resume support.

    If ``dest`` already exists, sends a Range header to resume from its size.
    Raises ``httpx.HTTPStatusError`` on non-2xx, non-206 responses.
    """
    dest.parent.mkdir(parents=True, exist_ok=True)
    existing = dest.stat().st_size if dest.exists() else 0
    headers = {"Range": f"bytes={existing}-"} if existing else {}

    with client.stream("GET", url, headers=headers, timeout=60.0) as resp:
        if resp.status_code == 416:
            # Range not satisfiable -- file is already complete on disk.
            logger.info("Already complete: %s", dest)
            return
        if resp.status_code not in (200, 206):
            resp.raise_for_status()

        total_header = resp.headers.get("Content-Length")
        total = int(total_header) + existing if total_header else None
        mode = "ab" if resp.status_code == 206 else "wb"

        with open(dest, mode) as fh, tqdm(
            total=total,
            initial=existing,
            unit="B",
            unit_scale=True,
            desc=dest.name,
        ) as bar:
            for chunk in resp.iter_bytes(chunk_size=_CHUNK_BYTES):
                fh.write(chunk)
                bar.update(len(chunk))


def download_cap_bulk(
    dest: Path,
    only_jurisdictions: list[str] | None = None,
) -> None:
    """Download the CAP bulk dump to ``dest`` (one ``.tar.gz`` per jurisdiction).

    Args:
        dest: Output directory. Created if missing.
        only_jurisdictions: List of CAP jurisdiction slugs (e.g. ``["us", "ny"]``).
            If ``None``, downloads every jurisdiction (~100 GB, multi-day).
            Defaults to :data:`CAP_DEFAULT_JURISDICTIONS` (``["us"]``) when callers
            pass an empty list.

    Downloads are resumable: re-running the function continues from the last
    byte written on disk. Files are saved as ``{dest}/{jurisdiction}.tar.gz``.
    """
    dest.mkdir(parents=True, exist_ok=True)

    if only_jurisdictions is None:
        logger.warning(
            "No jurisdiction filter set: CAP bulk dump is ~100 GB and multi-day. "
            "Pass only_jurisdictions=['us'] for a small test download."
        )
        # Caller explicitly opted into the full dump; resolve the list lazily by
        # asking the exports index page (deferred -- see TODO below).
        # TODO(Phase 2, task: download CAP): scrape https://case.law/exports/ for
        # the canonical list of per-jurisdiction tar.gz URLs. For now require an
        # explicit list.
        raise NotImplementedError(
            "Full-corpus download requires scraping https://case.law/exports/ for "
            "the per-jurisdiction file list. Pass only_jurisdictions=[...] "
            "explicitly until that scrape is implemented (Phase 2 task: 'download "
            "CAP bulk')."
        )

    targets = only_jurisdictions or CAP_DEFAULT_JURISDICTIONS
    logger.info("Downloading %d CAP jurisdiction(s) to %s", len(targets), dest)

    with httpx.Client(follow_redirects=True) as client:
        for jur in targets:
            url = f"{CAP_EXPORTS_BASE}/{jur}_text.tar.gz"
            out = dest / f"{jur}_text.tar.gz"
            logger.info("Fetching %s -> %s", url, out)
            _download_one(url, out, client)


def _normalize_record(raw: dict) -> CAPOpinion | None:
    """Map a CAP JSONL record to :class:`CAPOpinion`.

    Returns ``None`` if the record is missing required fields. CAP's schema is
    nested: ``casebody.data.opinions[*].text`` holds the actual opinion text.
    """
    try:
        cap_id = str(raw["id"])
        case_name = raw.get("name_abbreviation") or raw.get("name") or ""
        decision_date = raw.get("decision_date") or ""
        year = int(decision_date[:4]) if decision_date[:4].isdigit() else 0
        court = (raw.get("court") or {}).get("name", "")
        jurisdiction = (raw.get("jurisdiction") or {}).get("slug", "")
        casebody = (raw.get("casebody") or {}).get("data") or {}
        headnotes = "\n".join(casebody.get("head_matter", "") or [])
        opinions = casebody.get("opinions") or []
        body_text = "\n\n".join(o.get("text", "") for o in opinions if o.get("text"))
    except (KeyError, TypeError, ValueError) as exc:
        logger.debug("Skipping malformed CAP record: %s", exc)
        return None

    if not cap_id or not body_text:
        return None

    return CAPOpinion(
        id=cap_id,
        case_name=case_name,
        court=court,
        year=year,
        jurisdiction=jurisdiction,
        headnotes=headnotes,
        body_text=body_text,
    )


def parse_cap_jsonl_to_parquet(
    src: Path,
    dest: Path,
    batch_size: int = 10000,
) -> int:
    """Convert CAP JSONL.gz files under ``src`` into row-grouped Parquet at ``dest``.

    Each input ``.jsonl.gz`` becomes a sibling ``.parquet`` under ``dest`` (with
    the same stem). Returns the total number of opinions written. Records that
    fail normalization are logged and skipped.

    Args:
        src: Directory containing ``*.jsonl.gz`` (or the path to a single file).
        dest: Output directory for ``.parquet`` files.
        batch_size: Number of records to accumulate before flushing a row group.
    """
    # Import pandas lazily so importing this module doesn't pay the pandas cost.
    import pandas as pd

    dest.mkdir(parents=True, exist_ok=True)
    paths = [src] if src.is_file() else sorted(src.rglob("*.jsonl.gz"))
    if not paths:
        raise FileNotFoundError(f"No .jsonl.gz files found under {src}")

    total_written = 0
    for p in paths:
        out_path = dest / (p.stem.replace(".jsonl", "") + ".parquet")
        logger.info("Parsing %s -> %s", p, out_path)
        batch: list[CAPOpinion] = []
        frames: list[pd.DataFrame] = []
        with gzip.open(p, "rt", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    raw = json.loads(line)
                except json.JSONDecodeError:
                    logger.debug("Bad JSON line in %s; skipping", p.name)
                    continue
                rec = _normalize_record(raw)
                if rec is None:
                    continue
                batch.append(rec)
                if len(batch) >= batch_size:
                    frames.append(pd.DataFrame([r.__dict__ for r in batch]))
                    total_written += len(batch)
                    batch.clear()
        if batch:
            frames.append(pd.DataFrame([r.__dict__ for r in batch]))
            total_written += len(batch)
        if frames:
            pd.concat(frames, ignore_index=True).to_parquet(out_path, index=False)
        else:
            logger.warning("No valid records in %s", p)
    logger.info("Wrote %d opinions across %d parquet files", total_written, len(paths))
    return total_written


def iter_cap_opinions(parquet_dir: Path) -> Iterator[CAPOpinion]:
    """Stream :class:`CAPOpinion` instances from every ``*.parquet`` under ``parquet_dir``.

    Reads one file at a time to keep memory bounded; yields per-row dataclasses.
    """
    import pandas as pd

    files = sorted(parquet_dir.glob("*.parquet"))
    if not files:
        raise FileNotFoundError(f"No .parquet files under {parquet_dir}")
    for fp in files:
        logger.debug("Streaming %s", fp)
        df = pd.read_parquet(fp)
        for row in df.itertuples(index=False):
            yield CAPOpinion(
                id=str(row.id),
                case_name=str(row.case_name),
                court=str(row.court),
                year=int(row.year),
                jurisdiction=str(row.jurisdiction),
                headnotes=str(row.headnotes),
                body_text=str(row.body_text),
            )


# Re-export PATHS for symmetry with other data modules; callers commonly do
# ``from citecheck.data.cap_loader import PATHS``.
__all__ = [
    "CAPOpinion",
    "CAP_DEFAULT_JURISDICTIONS",
    "CAP_EXPORTS_BASE",
    "PATHS",
    "download_cap_bulk",
    "iter_cap_opinions",
    "parse_cap_jsonl_to_parquet",
]
