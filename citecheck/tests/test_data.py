"""Tests for citecheck.data.* — CourtListenerClient, benchmarks, eval_set.

These tests are owned by the *data* agent's deliverables; the eval agent
includes them here so a single ``pytest`` run covers the whole package once
all modules land. Each test ``pytest.importorskip``-s the module it needs so
the suite stays green on a partial checkout.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest


# ---------------------------------------------------------------------------
# CiteCheckExample (data.eval_set)
# ---------------------------------------------------------------------------
def test_cite_check_example_roundtrip(tmp_path: Path):
    """JSONL round-trip through save_eval_set / load_eval_set preserves fields.

    Uses the real ``data.eval_set`` types (with ``GoldCitation`` records) so the
    on-disk schema matches what ``load_eval_set`` expects.
    """
    eval_set = pytest.importorskip("citecheck.data.eval_set")

    examples = [
        eval_set.CiteCheckExample(
            id="rt001",
            question="Round-trip test question 1",
            gold_citations=[
                eval_set.GoldCitation(citation="Smith v. Jones, 412 F.3d 567", cl_opinion_id=12345),
            ],
            jurisdiction="us",
            source="manual",
            metadata={"note": "fixture"},
        ),
        eval_set.CiteCheckExample(
            id="rt002",
            question="Round-trip test question 2",
            gold_citations=[
                eval_set.GoldCitation(citation="Brown v. Board, 347 U.S. 483", cl_opinion_id=None),
            ],
            jurisdiction="us",
            source="charlotin",
        ),
    ]

    out = tmp_path / "eval.jsonl"
    eval_set.save_eval_set(examples, out)
    loaded = eval_set.load_eval_set(out)

    assert len(loaded) == len(examples)
    for orig, back in zip(examples, loaded, strict=True):
        assert orig.id == back.id
        assert orig.question == back.question
        assert orig.jurisdiction == back.jurisdiction
        assert orig.source == back.source
        assert len(orig.gold_citations) == len(back.gold_citations)
        for a, b in zip(orig.gold_citations, back.gold_citations, strict=True):
            assert a.citation == b.citation
            assert a.cl_opinion_id == b.cl_opinion_id


def test_load_eval_set_handles_empty(tmp_path: Path):
    eval_set = pytest.importorskip("citecheck.data.eval_set")

    empty = tmp_path / "empty.jsonl"
    empty.write_text("", encoding="utf-8")
    assert eval_set.load_eval_set(empty) == []


def test_load_eval_set_missing_file_raises(tmp_path: Path):
    eval_set = pytest.importorskip("citecheck.data.eval_set")

    with pytest.raises(FileNotFoundError):
        eval_set.load_eval_set(tmp_path / "nope.jsonl")


def test_cite_check_example_default_metadata():
    """metadata defaults to an empty dict; the other fields are required."""
    eval_set = pytest.importorskip("citecheck.data.eval_set")

    ex = eval_set.CiteCheckExample(
        id="x",
        question="q?",
        gold_citations=[],
        jurisdiction="us",
        source="manual",
    )
    assert isinstance(ex.metadata, dict) and ex.metadata == {}


def test_seed_from_charlotin_missing_csv_raises(tmp_path: Path):
    """``seed_from_charlotin`` must raise when the tracker CSV isn't present."""
    eval_set = pytest.importorskip("citecheck.data.eval_set")

    missing = tmp_path / "absent.csv"
    with pytest.raises((NotImplementedError, FileNotFoundError)):
        eval_set.seed_from_charlotin(missing)


# ---------------------------------------------------------------------------
# Benchmarks (data.benchmarks)
# ---------------------------------------------------------------------------
def test_benchmark_example_jsonl_roundtrip(tmp_path: Path):
    """BenchmarkExample JSONL serialization must round-trip cleanly."""
    benchmarks = pytest.importorskip("citecheck.data.benchmarks")

    example_cls = benchmarks.BenchmarkExample
    to_jsonl = benchmarks.to_jsonl

    examples = [
        example_cls(
            id="b1",
            source="cuad",
            question="Q1?",
            gold_passages=["passage A"],
            gold_answer="A1",
            metadata={"category": "termination"},
        ),
        example_cls(
            id="b2",
            source="legalbench-rag",
            question="Q2?",
            gold_passages=[],
            gold_answer="A2",
            metadata={},
        ),
    ]
    out = tmp_path / "bench.jsonl"
    to_jsonl(examples, out)

    lines = out.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == len(examples)
    parsed = [json.loads(line) for line in lines]
    assert parsed[0]["id"] == "b1"
    assert parsed[0]["source"] == "cuad"
    assert parsed[1]["question"] == "Q2?"


@pytest.mark.network
def test_legalbench_rag_loader_smoke():
    """``load_legalbench_rag`` exists and is callable (won't hit HF in CI)."""
    benchmarks = pytest.importorskip("citecheck.data.benchmarks")
    assert callable(benchmarks.load_legalbench_rag)


@pytest.mark.network
def test_cuad_loader_smoke():
    """``load_cuad`` exists and is callable (won't hit HF in CI)."""
    benchmarks = pytest.importorskip("citecheck.data.benchmarks")
    assert callable(benchmarks.load_cuad)


# ---------------------------------------------------------------------------
# CourtListener client (data.cl_client) — depends on httpx
# ---------------------------------------------------------------------------
def test_cl_client_construct_no_key_warns(tmp_path: Path, caplog):
    """Constructing without an API key should log a warning, not raise."""
    pytest.importorskip("httpx")
    pytest.importorskip("tenacity")
    from citecheck.data.cl_client import CourtListenerClient

    with caplog.at_level("WARNING"):
        client = CourtListenerClient(api_key="", cache_dir=tmp_path / "cl_cache")
    assert client is not None
    # The warning text mentions the 100 req/hr unauthenticated tier.
    assert any("unauthenticated" in rec.message.lower() for rec in caplog.records)
    client.close()


def test_cl_client_resolve_returns_opinion_when_found(mocker, tmp_path: Path):
    """resolve_citation returns CLOpinion when CL's response includes a hit."""
    pytest.importorskip("httpx")
    pytest.importorskip("tenacity")
    from citecheck.data.cl_client import CourtListenerClient

    # Two-step fetch: citation-lookup returns a match with an opinion_id, then
    # get_opinion(id) returns the full opinion.
    lookup_resp = mocker.MagicMock(status_code=200)
    lookup_resp.json.return_value = [{"opinion_id": 12345}]
    lookup_resp.raise_for_status.return_value = None

    opinion_resp = mocker.MagicMock(status_code=200)
    opinion_resp.json.return_value = {
        "id": 12345,
        "case_name": "Smith v. Jones",
        "court": "ca9",
        "court_jurisdiction": "F-9",
        "date_filed": "2005-06-15",
        "citation_strings": ["412 F.3d 567"],
        "plain_text": "Holding ...",
        "absolute_url": "https://courtlistener.com/12345/",
    }
    opinion_resp.raise_for_status.return_value = None

    # Route by URL path: /citation-lookup/ -> lookup_resp, /opinions/ -> opinion_resp.
    def _request(method, path, **kwargs):  # noqa: ARG001
        if "citation-lookup" in path:
            return lookup_resp
        return opinion_resp

    mocker.patch("httpx.Client.request", side_effect=_request)
    client = CourtListenerClient(api_key="fake-key", cache_dir=tmp_path / "cl_cache")
    result = client.resolve_citation("Smith v. Jones, 412 F.3d 567 (9th Cir. 2005)")
    assert result is not None
    assert result.id == 12345
    assert "Smith" in result.case_name
    client.close()


def test_cl_client_resolve_returns_none_on_404(mocker, tmp_path: Path):
    """A 404 on /citation-lookup/ must surface as None, not an exception."""
    pytest.importorskip("httpx")
    pytest.importorskip("tenacity")
    import httpx

    from citecheck.data.cl_client import CourtListenerClient

    response = mocker.MagicMock(status_code=404)
    err = httpx.HTTPStatusError("404", request=mocker.MagicMock(), response=response)
    response.raise_for_status.side_effect = err

    mocker.patch("httpx.Client.request", return_value=response)
    client = CourtListenerClient(api_key="fake-key", cache_dir=tmp_path / "cl_cache")
    result = client.resolve_citation("FAKE v. FAKE, 999 F.3d 999 (9th Cir. 2099)")
    assert result is None
    client.close()


def test_cl_client_rate_limit_raises(tmp_path: Path):
    """Saturating the soft rate-limit window should raise RateLimitedError."""
    pytest.importorskip("httpx")
    pytest.importorskip("tenacity")
    from citecheck.data.cl_client import CourtListenerClient, RateLimitedError

    client = CourtListenerClient(api_key="fake-key", cache_dir=tmp_path / "cl_cache")
    # Directly fill the sliding window with synthetic timestamps.
    import time as _time

    now = _time.monotonic()
    # Implementation detail: _calls is a deque of monotonic timestamps and
    # _SOFT_RATE_LIMIT is module-level; introspect both to avoid hard-coding.
    from citecheck.data.cl_client import _SOFT_RATE_LIMIT  # type: ignore[attr-defined]

    for _ in range(_SOFT_RATE_LIMIT):
        client._calls.append(now)  # type: ignore[attr-defined]
    with pytest.raises(RateLimitedError):
        client._check_rate_limit()  # type: ignore[attr-defined]
    client.close()
