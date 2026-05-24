"""CourtListener REST v4 client with rate limiting, retry, and disk cache.

Wraps the two endpoints CiteCheck uses most often:

* ``POST /api/rest/v4/citation-lookup/`` — resolves a Bluebook-style citation
  string to an opinion (used by the agent loop's CitationResolver tool).
* ``GET /api/rest/v4/opinions/{id}/`` — fetches a resolved opinion by ID.

Rate limiting: CourtListener authenticated tier is 5,000 req/hr. We enforce a
soft 4,500/hr ceiling via a sliding-window token bucket and raise
:class:`RateLimitedError` past that. Retries on 5xx and timeouts (3 attempts,
exponential backoff); 4xx errors propagate immediately.

Disk cache: resolved citations are written to ``cache_dir/{sha1}.json`` so the
agent's verify loop never re-resolves the same string.
"""
from __future__ import annotations

import hashlib
import json
import logging
import threading
import time
from collections import deque
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

import httpx
from tenacity import (
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
)

from citecheck.config import API_CFG, PATHS

logger = logging.getLogger(__name__)

# Soft cap below the documented 5,000/hr to leave headroom for concurrent agents.
_SOFT_RATE_LIMIT = 4500
_RATE_WINDOW_SECONDS = 3600
_REQUEST_TIMEOUT_SECONDS = 15.0


class RateLimitedError(Exception):
    """Raised when the client's soft rate limit would be exceeded.

    Carries the number of requests already made in the current sliding window
    so callers can decide whether to back off or surface the error.
    """

    def __init__(self, calls_in_window: int, window_seconds: int = _RATE_WINDOW_SECONDS):
        self.calls_in_window = calls_in_window
        self.window_seconds = window_seconds
        super().__init__(
            f"CourtListener soft rate limit reached: {calls_in_window} calls "
            f"in last {window_seconds}s (limit {_SOFT_RATE_LIMIT})."
        )


@dataclass(frozen=True)
class CLOpinion:
    """Normalized CourtListener opinion record.

    Attributes:
        id: CourtListener opinion ID (integer, stable).
        case_name: Case caption (e.g. "Brown v. Board of Education").
        court: Human-readable court name.
        court_jurisdiction: Court's jurisdiction code ("F" federal, "S" state, etc.).
        year: Year of the decision (int).
        citation_strings: List of Bluebook citations associated with this opinion.
        body_text: Plain-text opinion body (may be empty if CL has only HTML).
        url: Absolute URL on courtlistener.com.
    """

    id: int
    case_name: str
    court: str
    court_jurisdiction: str
    year: int
    citation_strings: list[str] = field(default_factory=list)
    body_text: str = ""
    url: str = ""


def _is_retryable(exc: BaseException) -> bool:
    """Tenacity predicate: retry on transport/timeout and 5xx, but not 4xx."""
    if isinstance(exc, httpx.TransportError | httpx.TimeoutException):
        return True
    if isinstance(exc, httpx.HTTPStatusError):
        return 500 <= exc.response.status_code < 600
    return False


class CourtListenerClient:
    """REST v4 client with rate limiting, retry, and disk-backed read-through cache."""

    def __init__(
        self,
        api_key: str | None = None,
        cache_dir: Path | None = None,
        base_url: str | None = None,
    ) -> None:
        """Create a client.

        Args:
            api_key: CourtListener API token. Falls back to ``API_CFG.cl_api_key``.
            cache_dir: Directory for the JSON disk cache. Defaults to ``PATHS.cl_cache``.
            base_url: Override the API base URL (useful for tests).
        """
        self._api_key = api_key if api_key is not None else API_CFG.cl_api_key
        self._cache_dir = cache_dir if cache_dir is not None else PATHS.cl_cache
        self._cache_dir.mkdir(parents=True, exist_ok=True)
        self._base_url = base_url or API_CFG.courtlistener_base
        self._lock = threading.Lock()
        # Sliding-window timestamps of recent request starts (monotonic seconds).
        self._calls: deque[float] = deque()

        headers = {"User-Agent": "citecheck/0.1"}
        if self._api_key:
            headers["Authorization"] = f"Token {self._api_key}"
        else:
            logger.warning(
                "CourtListenerClient created without an API key; unauthenticated "
                "tier is capped at 100 req/hr."
            )
        self._client = httpx.Client(
            base_url=self._base_url,
            headers=headers,
            timeout=_REQUEST_TIMEOUT_SECONDS,
        )

    # ---- context manager -------------------------------------------------
    def __enter__(self) -> CourtListenerClient:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()

    def close(self) -> None:
        """Close the underlying HTTP connection pool."""
        self._client.close()

    # ---- rate limiting ---------------------------------------------------
    def _check_rate_limit(self) -> None:
        """Drop timestamps older than the window; raise if at/above soft cap."""
        now = time.monotonic()
        cutoff = now - _RATE_WINDOW_SECONDS
        with self._lock:
            while self._calls and self._calls[0] < cutoff:
                self._calls.popleft()
            if len(self._calls) >= _SOFT_RATE_LIMIT:
                raise RateLimitedError(len(self._calls))
            self._calls.append(now)

    # ---- disk cache ------------------------------------------------------
    def _cache_path(self, key: str) -> Path:
        digest = hashlib.sha1(key.encode("utf-8")).hexdigest()
        return self._cache_dir / f"{digest}.json"

    def _cache_get(self, key: str) -> dict[str, Any] | None:
        p = self._cache_path(key)
        if not p.exists():
            return None
        try:
            with p.open("r", encoding="utf-8") as fh:
                return json.load(fh)
        except (OSError, json.JSONDecodeError) as exc:
            logger.warning("Corrupt cache entry %s (%s); ignoring", p, exc)
            return None

    def _cache_put(self, key: str, value: dict[str, Any]) -> None:
        p = self._cache_path(key)
        try:
            with p.open("w", encoding="utf-8") as fh:
                json.dump(value, fh)
        except OSError as exc:
            logger.warning("Failed to write cache entry %s: %s", p, exc)

    # ---- HTTP ------------------------------------------------------------
    @retry(
        retry=retry_if_exception(_is_retryable),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=2, min=2, max=30),
        reraise=True,
    )
    def _request(self, method: str, path: str, **kwargs: Any) -> httpx.Response:
        self._check_rate_limit()
        logger.debug("CL %s %s", method, path)
        resp = self._client.request(method, path, **kwargs)
        # raise_for_status so retry-on-5xx works; tenacity inspects the exception.
        resp.raise_for_status()
        return resp

    # ---- public API ------------------------------------------------------
    def resolve_citation(self, citation_str: str) -> CLOpinion | None:
        """Resolve a Bluebook citation string to a :class:`CLOpinion`.

        Returns ``None`` if CourtListener does not find a match. Read-through
        cached: identical citation strings hit disk after the first call.
        """
        cache_key = f"resolve::{citation_str}"
        cached = self._cache_get(cache_key)
        if cached is not None:
            if cached.get("__miss__"):
                return None
            return _from_cl_dict(cached)

        try:
            resp = self._request(
                "POST",
                "/citation-lookup/",
                data={"text": citation_str},
            )
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code in (400, 404):
                # CL signals "no match" via 4xx in v4 citation-lookup.
                self._cache_put(cache_key, {"__miss__": True})
                return None
            raise

        payload = resp.json()
        # The endpoint returns a list of match dicts; an empty list means no hit.
        matches = payload if isinstance(payload, list) else payload.get("results", [])
        if not matches:
            self._cache_put(cache_key, {"__miss__": True})
            return None

        first = matches[0]
        # The v4 lookup response contains nested cluster/opinion objects; we
        # canonicalize via the dedicated opinion fetch when an ID is present.
        opinion_id = first.get("opinion_id") or first.get("id")
        if opinion_id is None:
            logger.warning("CL citation-lookup response missing opinion id: %s", first)
            return None
        opinion = self.get_opinion(int(opinion_id))
        if opinion is not None:
            self._cache_put(cache_key, asdict(opinion))
        return opinion

    def get_opinion(self, opinion_id: int) -> CLOpinion | None:
        """Fetch a single opinion by CourtListener ID.

        Returns ``None`` on 404. Cached in the same disk store as resolutions.
        """
        cache_key = f"opinion::{opinion_id}"
        cached = self._cache_get(cache_key)
        if cached is not None:
            if cached.get("__miss__"):
                return None
            return _from_cl_dict(cached)

        try:
            resp = self._request("GET", f"/opinions/{opinion_id}/")
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 404:
                self._cache_put(cache_key, {"__miss__": True})
                return None
            raise

        opinion = _from_cl_dict(resp.json())
        self._cache_put(cache_key, asdict(opinion))
        return opinion


def _from_cl_dict(d: dict[str, Any]) -> CLOpinion:
    """Coerce a CourtListener response (or cached blob) into :class:`CLOpinion`."""
    cluster = d.get("cluster") if isinstance(d.get("cluster"), dict) else {}
    court_obj = cluster.get("court") if isinstance(cluster.get("court"), dict) else {}
    date_filed = cluster.get("date_filed") or d.get("date_filed") or ""
    year = int(date_filed[:4]) if date_filed[:4].isdigit() else int(d.get("year") or 0)

    citation_strings = d.get("citation_strings") or [
        c.get("cite", "") if isinstance(c, dict) else str(c)
        for c in (cluster.get("citations") or [])
    ]

    return CLOpinion(
        id=int(d.get("id", 0)),
        case_name=str(cluster.get("case_name") or d.get("case_name") or ""),
        court=str(court_obj.get("full_name") or d.get("court") or ""),
        court_jurisdiction=str(
            court_obj.get("jurisdiction") or d.get("court_jurisdiction") or ""
        ),
        year=year,
        citation_strings=[s for s in citation_strings if s],
        body_text=str(
            d.get("plain_text") or d.get("body_text") or d.get("html_with_citations") or ""
        ),
        url=str(d.get("absolute_url") or d.get("url") or ""),
    )


__all__ = ["CLOpinion", "CourtListenerClient", "RateLimitedError"]
