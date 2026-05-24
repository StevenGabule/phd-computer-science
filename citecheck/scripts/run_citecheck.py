"""CLI: run the full CiteCheck verify loop over the eval set.

Same I/O contract as ``run_baseline.py`` so eval scripts can treat its output
identically; the only difference is the system under test is
:class:`~citecheck.agent.VerifyLoop` rather than one of the baseline classes.

Usage::

    python -m citecheck.scripts.run_citecheck \\
        --eval-jsonl data/eval_v0.1.jsonl \\
        --output-jsonl runs/citecheck_llama8b.jsonl \\
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

from citecheck.agent import CitationResolver, VerifyLoop
from citecheck.config import AGENT, API_CFG, MODELS, ensure_dirs

logger = logging.getLogger("citecheck.run_citecheck")

GENERATOR_CHOICES = ("llama-3.1-8b-instruct", "qwen2.5-7b-instruct", "gpt-4o-mini")

Generator = Callable[[str], str]


# --------------------------------------------------------------------- backends
def _make_generator(choice: str) -> Generator:
    """Return a ``(prompt) -> str`` callable for the requested model."""
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


# ------------------------------------------------------------------------- CLI
@click.command()
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
    "--max-iterations",
    type=int,
    default=AGENT.max_iterations,
    show_default=True,
    help="Cap on verify-loop regeneration rounds per question.",
)
@click.option(
    "--no-rerank",
    is_flag=True,
    default=False,
    help="Skip the cross-encoder reranker (use HybridRetriever order as-is).",
)
@click.option(
    "--no-constrained-decoding",
    is_flag=True,
    default=False,
    help="Disable Bluebook regex constraint on generation.",
)
@click.option(
    "--top-k",
    type=int,
    default=10,
    show_default=True,
    help="Passages to retrieve per iteration.",
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
    eval_jsonl: Path,
    output_jsonl: Path,
    generator: str,
    max_iterations: int,
    no_rerank: bool,
    no_constrained_decoding: bool,
    top_k: int,
    limit: int | None,
    log_level: str,
) -> None:
    """Run the full CiteCheck verify loop over ``eval_jsonl``."""
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s %(levelname)s %(name)s | %(message)s",
        stream=sys.stderr,
    )
    ensure_dirs()
    output_jsonl.parent.mkdir(parents=True, exist_ok=True)

    # Lazy imports — these pull heavy retrieval/reranker/data deps.
    from citecheck.data import CourtListenerClient, load_eval_set  # noqa: PLC0415
    from citecheck.retrieval import HybridRetriever  # noqa: PLC0415

    cl = CourtListenerClient()
    resolver = CitationResolver(cl_client=cl)
    retriever = HybridRetriever()
    reranker: Any | None = None
    if not no_rerank:
        from citecheck.reranker.model import CrossEncoderReranker  # noqa: PLC0415

        reranker = CrossEncoderReranker()

    gen = _make_generator(generator.lower())

    loop = VerifyLoop(
        generator=gen,
        retriever=retriever,
        reranker=reranker,
        resolver=resolver,
        max_iterations=max_iterations,
        use_constrained_decoding=not no_constrained_decoding,
        top_k=top_k,
    )

    examples = load_eval_set(eval_jsonl)
    if limit is not None:
        examples = list(examples)[:limit]

    logger.info(
        "Running CiteCheck generator=%s max_iter=%d rerank=%s constrained=%s → %s",
        generator, max_iterations, not no_rerank, not no_constrained_decoding,
        output_jsonl,
    )

    n_done = 0
    with output_jsonl.open("w", encoding="utf-8") as fout:
        for ex in examples:
            try:
                ans = loop.answer(ex.question)
            except Exception:
                logger.exception("verify loop failed on id=%s; writing empty row", ex.id)
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
