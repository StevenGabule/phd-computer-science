"""Constrained-decoding grammar for Bluebook case citations.

The generator emits a free-form answer, but every span we want to recognize as
a "citation" must match this grammar. When :attr:`Agent.constrained_decoding`
is on, the loop wraps citation slots with ``outlines.generate.regex(model,
pattern)`` so the LLM can never emit a syntactically-broken citation.

Coverage (v0.1):
    * Standard full case citations: ``<Name>, <vol> <Reporter> <page> (<court> <year>)``
    * Court parenthetical is *optional* (some U.S. Supreme Court cites omit it).
    * Reporter list is drawn from ``reporters_db`` and supplemented with the
      most common federal/regional reporters as a hard fallback so the regex
      is non-empty even if ``reporters_db`` is unavailable.

Out of scope for v0.1 (planned v0.2):
    * Parallel citations (``...; 99 S. Ct. 2456; 60 L. Ed. 2d 1056``)
    * Pin cites (``347 U.S. 483, 495``)
    * Statute citations (``42 U.S.C. § 1983``)
    * Signal phrases (``See, e.g.,`` / ``Cf.`` / ``But see``)
    * Short-form / ``id.`` / ``supra``

These all parse cleanly via :mod:`eyecite` post-hoc; the grammar is purely a
generation-side guard rail, not a parser.
"""
from __future__ import annotations

import logging
import re
from typing import Any

logger = logging.getLogger(__name__)

# Fallback reporter set, used if reporters_db is not importable. Keep deliberately
# narrow — the goal is high precision on the federal/regional reporters that
# dominate the eval set, not exhaustive coverage.
_FALLBACK_REPORTERS: tuple[str, ...] = (
    "U.S.",
    "S. Ct.", "S.Ct.",
    "L. Ed.", "L.Ed.", "L. Ed. 2d", "L.Ed.2d",
    "F.", "F.2d", "F.3d", "F.4th",
    "F. Supp.", "F.Supp.", "F. Supp. 2d", "F.Supp.2d", "F. Supp. 3d", "F.Supp.3d",
    "F.R.D.",
    "B.R.",
    "A.", "A.2d", "A.3d",
    "P.", "P.2d", "P.3d",
    "N.E.", "N.E.2d", "N.E.3d",
    "N.W.", "N.W.2d",
    "S.E.", "S.E.2d",
    "S.W.", "S.W.2d", "S.W.3d",
    "So.", "So. 2d", "So.2d", "So. 3d", "So.3d",
    "Cal.", "Cal. 2d", "Cal. 3d", "Cal. 4th", "Cal. 5th",
    "Cal. Rptr.", "Cal. Rptr. 2d", "Cal. Rptr. 3d",
    "N.Y.", "N.Y.2d", "N.Y.3d",
    "N.Y.S.", "N.Y.S.2d", "N.Y.S.3d",
)


def _load_reporters() -> list[str]:
    """Return reporter abbreviations, preferring reporters_db, falling back."""
    try:
        from reporters_db import REPORTERS  # noqa: PLC0415
    except ImportError:
        logger.info("reporters_db unavailable; using %d fallback reporters",
                    len(_FALLBACK_REPORTERS))
        return list(_FALLBACK_REPORTERS)

    out: set[str] = set()
    for _canon, entries in REPORTERS.items():
        for entry in entries:
            for edition in entry.get("editions", {}):
                out.add(edition)
            for variation in entry.get("variations", {}):
                out.add(variation)
    if not out:
        return list(_FALLBACK_REPORTERS)
    # Sort by length descending so the regex alternation matches "F. Supp. 2d"
    # before "F." — without this, "F." would greedily win and corrupt parses.
    return sorted(out, key=len, reverse=True)


def _escape_alternation(items: list[str]) -> str:
    """Build a non-capturing regex alternation from a list of literals."""
    if not items:
        raise ValueError("cannot build alternation from empty list")
    return "(?:" + "|".join(re.escape(s) for s in items) + ")"


class BluebookGrammar:
    """Grammar + regex for full-form Bluebook case citations.

    Components::

        case_name    : One or more capitalized words, allows v./vs., apostrophes,
                       hyphens, commas inside corporate names.
        volume       : 1–4 digits.
        reporter     : alternation built from reporters_db (or fallback).
        page         : 1–6 digits, optional pin cite suffix (e.g. ", 495").
        court_year   : Optional parenthetical "(<court abbrev> <4-digit year>)"
                       or "(<4-digit year>)" — court is omitted when the reporter
                       uniquely identifies the court (e.g. U.S. ⇒ SCOTUS).
    """

    # -------- token-level pieces -------------------------------------------
    # Case names: at least one capitalized word, then v./vs., then more capitalized
    # words. Allow internal commas (e.g. "Smith, Inc. v. Jones, LLC") and
    # lowercase connectors (e.g. "Brown v. Board of Education", "In re Foo").
    # _NAME_TOKEN matches either a capitalized word OR a small set of legal
    # connectors that frequently appear unaltered in case names.
    _NAME_TOKEN = (
        r"(?:[A-Z][A-Za-z0-9'\-&.]*"            # capitalized word
        r"|of|the|and|for|in|on|de|du|la|le|von|van|el)"
    )
    _CASE_NAME = (
        r"(?:[A-Z][A-Za-z0-9'\-&.]*"            # first token MUST be capitalized
        r"(?:(?:,?\s+)" + _NAME_TOKEN + r"){0,10})"
        r"\s+v\.?\s+"                            # v. separator
        r"(?:[A-Z][A-Za-z0-9'\-&.]*"
        r"(?:(?:,?\s+)" + _NAME_TOKEN + r"){0,10})"
    )
    _VOLUME = r"\d{1,4}"
    _PAGE = r"\d{1,6}(?:,\s*\d{1,6})?"  # allow optional pin cite
    _YEAR = r"(?:1[6-9]\d{2}|20\d{2})"  # 1600–2099
    # Court abbreviation: letters, digits, dots, spaces, "th", "Cir.", "App.", etc.
    _COURT_ABBR = r"[A-Z][A-Za-z0-9.\- ]{1,30}"

    def __init__(self) -> None:
        reporters = _load_reporters()
        self._reporter_alt = _escape_alternation(reporters)
        self.bluebook_regex: str = self._build_regex()
        self._compiled = re.compile(self.bluebook_regex)
        logger.debug("BluebookGrammar built with %d reporters", len(reporters))

    # ------------------------------------------------------------------ build
    def _build_regex(self) -> str:
        # Court parenthetical is optional and itself made of (court? year):
        court_year = (
            r"\((?:" + self._COURT_ABBR + r"\s+)?" + self._YEAR + r"\)"
        )
        # Whole citation; no anchors so it can be embedded in larger text.
        return (
            r"(?P<case_name>" + self._CASE_NAME + r"),\s+"
            r"(?P<volume>" + self._VOLUME + r")\s+"
            r"(?P<reporter>" + self._reporter_alt + r")\s+"
            r"(?P<page>" + self._PAGE + r")"
            r"(?:\s+(?P<court_year>" + court_year + r"))?"
        )

    # ----------------------------------------------------------------- output
    def as_outlines_regex(self) -> str:
        """Return the regex string suitable for ``outlines.generate.regex``.

        Outlines compiles the pattern into a DFA and constrains the LM's
        next-token distribution to tokens that keep the DFA accepting. The
        pattern is the *same* as :attr:`bluebook_regex` but stripped of named
        groups (Outlines tolerates them on recent versions but older builds
        choke, and the names carry no information for constrained decoding).
        """
        # Strip ?P<name> annotations: (?P<x>...) -> (?:...)
        return re.sub(r"\?P<[a-zA-Z_]+>", "?:", self.bluebook_regex)

    def validate(self, text: str) -> bool:
        """``True`` iff ``text`` contains at least one matching citation span.

        Use this for cheap sanity checks (e.g. "did the LLM emit anything
        citation-shaped?"). Authoritative parsing still goes through eyecite.
        """
        return self._compiled.search(text) is not None

    def find_all(self, text: str) -> list[str]:
        """Return every matching citation span in ``text``.

        Useful for fishing citations out of free-form generations when the
        constrained-decoding path is disabled.
        """
        return [m.group(0) for m in self._compiled.finditer(text)]

    # ---------------------------------------------------- optional Lark export
    def as_lark_grammar(self) -> str:
        """Return a Lark grammar string approximating the regex.

        This is provided for callers that prefer Lark over regex-DFA backends
        (e.g. ``transformers-cfg``). The grammar is intentionally a superset of
        :attr:`bluebook_regex` — Lark's token language can't express all of the
        character-class subtleties — so use eyecite for the authoritative parse.
        """
        # Build reporter alternation as Lark-quoted strings.
        reporters = _load_reporters()
        reporter_alt = " | ".join(f'"{r}"' for r in reporters)
        return (
            "start: citation\n"
            'citation: case_name "," WS volume WS reporter WS page (WS court_year)?\n'
            "case_name: /[A-Z][A-Za-z0-9'\\-&.]+(?:[ ,][A-Z][A-Za-z0-9'\\-&.]+)*"
            " v\\.? [A-Z][A-Za-z0-9'\\-&.]+(?:[ ,][A-Z][A-Za-z0-9'\\-&.]+)*/\n"
            "volume: /\\d{1,4}/\n"
            f"reporter: {reporter_alt}\n"
            "page: /\\d{1,6}(?:, ?\\d{1,6})?/\n"
            "court_year: /\\([A-Z][A-Za-z0-9.\\- ]{0,30}\\s+\\d{4}\\)|\\(\\d{4}\\)/\n"
            "WS: /[ \\t]+/\n"
        )

    # ------------------------------------------------------ outlines binding
    def bind_outlines(self, model: Any) -> Any:  # pragma: no cover — needs LLM
        """Return an Outlines callable that constrains generation to the grammar.

        Args:
            model: an ``outlines.models.transformers`` model handle.

        Returns:
            A callable ``f(prompt: str, **kw) -> str`` that, when invoked, will
            sample tokens from ``model`` constrained to the Bluebook regex.

        Raises:
            ImportError: if ``outlines`` is not installed.
        """
        try:
            import outlines  # noqa: PLC0415
        except ImportError as exc:
            raise ImportError(
                "outlines is required for constrained decoding; "
                "install with `pip install outlines`"
            ) from exc
        return outlines.generate.regex(model, self.as_outlines_regex())
