"""CLI: run a Phase-2 baseline over the eval set.

Loads a JSONL eval set, instantiates the requested baseline + generator
backend, runs ``baseline.answer(question)`` for every example, and writes
``{question, gold_citations, predicted_text, predicted_citations,
iterations_used, retrieved_doc_ids}`` per line to the output JSONL.

Usage::

    python -m citecheck.scripts.run_baseline \\
        --baseline naive_rag \\
        --eval-jsonl data/eval_v0.1.jsonl \\
        --output-jsonl runs/naive_rag_llama8b.jsonl \\
        --generator llama-3.1-8b-instruct
"""
from __future__ import annotations

import json
import logging
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

import click

from citecheck.agent.citation_resolver import CitationResolver
from citecheck.baselines import (
    BaselineProtocol,
    CRAGBaseline,
    ELRAGBaseline,
    NaiveRAGBaseline,
    SelfRAGBaseline,
    VanillaBaseline,
)
from citecheck.config import API_CFG, MODELS, PATHS, ensure_dirs

logger = logging.getLogger("citecheck.run_baseline")

# CLI choice -> generator-loader function name. The HF id is resolved in
# :func:`_make_generator`.
GENERATOR_CHOICES = ("llama-3.1-8b-instruct", "qwen2.5-7b-instruct", "gpt-4o-mini")
BASELINE_CHOICES = ("vanilla", "naive_rag", "self_rag", "crag", "el_rag")

Generator = Callable[[str], str]


# --------------------------------------------------------------------- backends
def _make_generator(choice: str) -> Generator:
    """Return a ``(prompt) -> str`` callable for the requested model.

    Local HF backends use transformers + chat templating; the hosted choice
    (``gpt-4o-mini``) uses the OpenAI HTTP API via ``httpx``. All three return
    plain strings so the rest of the pipeline is backend-agnostic.
    """
    if choice == "gpt-4o-mini":
        return _make_openai_generator(MODELS.closed_ceiling)
    if choice == "llama-3.1-8b-instruct":
        return _make_hf_generator(MODELS.generator_primary)
    if choice == "qwen2.5-7b-instruct":
        return _make_hf_generator(MODELS.generator_secondary)
    raise click.BadParameter(f"unknown generator {choice!r}")


def _make_hf_generator(hf_id: str) -> Generator:
    """Wrap a local HuggingFace chat model as a ``(prompt) -> str`` callable."""
    import torch  # noqa: PLC0415
    from transformers import AutoModelForCausalLM, AutoTokenizer  # noqa: PLC0415

    logger.info("Loading HF generator %s", hf_id)
    tok = AutoTokenizer.from_pretrained(hf_id, token=API_CFG.hf_token or None)
    if tok.pad_token_id is None:
        tok.pad_token = tok.eos_token
    model = AutoModelForCausalLM.from_pretrained(
        hf_id,
        torch_dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32,
        device_map="auto" if torch.cuda.is_available() else None,
        token=API_CFG.hf_token or None,
    )
    model.eval()

    def generate(prompt: str, max_new_tokens: int = 512) -> str:
        messages = [{"role": "user", "content": prompt}]
        inputs = tok.apply_chat_template(
            messages, return_tensors="pt", add_generation_prompt=True,
        ).to(model.device)
        with torch.no_grad():
            out = model.generate(
                inputs,
                max_new_tokens=max_new_tokens,
                do_sample=False,
                pad_token_id=tok.pad_token_id,
            )
        gen_only = out[0, inputs.shape[1]:]
        return tok.decode(gen_only, skip_special_tokens=True)

    return generate


def _make_openai_generator(model: str) -> Generator:
    """OpenAI Chat Completions wrapper using httpx."""
    import httpx  # noqa: PLC0415

    if not API_CFG.openai_api_key:
        raise click.UsageError("OPENAI_API_KEY not set in environment / .env")
    client = httpx.Client(
        base_url="https://api.openai.com/v1",
        headers={"Authorization": f"Bearer {API_CFG.openai_api_key}"},
        timeout=60.0,
    )

    def generate(prompt: str, max_tokens: int = 512) -> str:
        resp = client.post(
            "/chat/completions",
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens,
                "temperature": 0.0,
            },
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]

    return generate


# ----------------------------------------------------------------- baseline mux
def _instantiate_baseline(
    name: str,
    generator: Generator,
    resolver: CitationResolver,
) -> BaselineProtocol:
    """Build the requested baseline, wiring in retrieval/reranking as needed."""
    if name == "vanilla":
        return VanillaBaseline(generator=generator, resolver=resolver)

    # Lazy imports — these pull heavy deps (Pyserini/FAISS/sentence-transformers).
    from citecheck.retrieval import HybridRetriever  # noqa: PLC0415

    retriever = HybridRetriever()

    if name == "naive_rag":
        return NaiveRAGBaseline(
            generator=generator, retriever=retriever, resolver=resolver,
        )
    if name == "self_rag":
        return SelfRAGBaseline(
            generator=generator, retriever=retriever, resolver=resolver,
        )
    if name == "crag":
        return CRAGBaseline(
            generator=generator, retriever=retriever, resolver=resolver,
        )
    if name == "el_rag":
        from citecheck.reranker.model import CrossEncoderReranker  # noqa: PLC0415

        reranker = CrossEncoderReranker()
        return ELRAGBaseline(
            generator=generator,
            hybrid_retriever=retriever,
            reranker=reranker,
            resolver=resolver,
        )
    raise click.BadParameter(f"unknown baseline {name!r}")


# ------------------------------------------------------------------------- CLI
@click.command()
@click.option(
    "--baseline",
    type=click.Choice(BASELINE_CHOICES, case_sensitive=False),
    required=True,
    help="Which baseline to run.",
)
@click.option(
    "--eval-jsonl",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    required=True,
    help="Path to the CiteCheck eval set (one JSON per line).",
)
@click.option(
    "--output-jsonl",
    type=click.Path(dir_okay=False, path_type=Path),
    required=True,
    help="Where to write per-example predictions.",
)
@click.option(
    "--generator",
    type=click.Choice(GENERATOR_CHOICES, case_sensitive=False),
    default=GENERATOR_CHOICES[0],
    show_default=True,
    help="Which LLM backend to use.",
)
@click.option(
    "--limit",
    type=int,
    default=None,
    help="Stop after N examples (debug).",
)
@click.option(
    "--log-level",
    type=click.Choice(("DEBUG", "INFO", "WARNING", "ERROR")),
    default="INFO",
    show_default=True,
)
def main(
    baseline: str,
    eval_jsonl: Path,
    output_jsonl: Path,
    generator: str,
    limit: int | None,
    log_level: str,
) -> None:
    """Run ``baseline`` over ``eval_jsonl`` and write predictions to ``output_jsonl``."""
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s %(levelname)s %(name)s | %(message)s",
        stream=sys.stderr,
    )
    ensure_dirs()
    output_jsonl.parent.mkdir(parents=True, exist_ok=True)

    # Lazy imports for the agent-side pieces; defer to runtime so --help is fast.
    from citecheck.data import CourtListenerClient, load_eval_set  # noqa: PLC0415

    cl = CourtListenerClient()
    resolver = CitationResolver(cl_client=cl)
    gen = _make_generator(generator.lower())
    system = _instantiate_baseline(baseline.lower(), gen, resolver)
    examples = load_eval_set(eval_jsonl)
    if limit is not None:
        examples = list(examples)[:limit]

    logger.info(
        "Running baseline=%s generator=%s n_examples=%d → %s",
        baseline, generator, len(examples) if hasattr(examples, "__len__") else -1,
        output_jsonl,
    )

    n_done = 0
    with output_jsonl.open("w", encoding="utf-8") as fout:
        for ex in examples:
            try:
                ans = system.answer(ex.question)
            except Exception:
                logger.exception("baseline failed on example id=%s; writing empty row", ex.id)
                row: dict[str, Any] = {
                    "id": ex.id,
                    "question": ex.question,
                    "gold_citations": list(ex.gold_citations),
                    "error": "exception during answer()",
                }
            else:
                row = {
                    "id": ex.id,
                    "question": ex.question,
                    "gold_citations": list(ex.gold_citations),
                    **ans.to_dict(),
                }
            fout.write(json.dumps(row, ensure_ascii=False) + "\n")
            fout.flush()
            n_done += 1
            if n_done % 10 == 0:
                logger.info("  ... %d examples written", n_done)

    logger.info("Done: %d rows in %s", n_done, output_jsonl)


if __name__ == "__main__":  # pragma: no cover
    main()
