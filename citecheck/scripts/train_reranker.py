"""Sweep lambda values and train the multi-objective reranker for each.

Usage::

    python scripts/train_reranker.py \\
        --train-jsonl data/reranker_train.jsonl \\
        --val-jsonl data/reranker_val.jsonl \\
        --output-dir models/reranker \\
        --lambda-values 0.1 0.3 0.5 1.0 \\
        --epochs 3 \\
        --batch-size 16
"""
from __future__ import annotations

import json
import logging
from pathlib import Path

import click

from citecheck.config import API_CFG, MODELS, PATHS, RERANKER, ensure_dirs
from citecheck.reranker.dataset import RerankerExample
from citecheck.reranker.train import train_reranker

logger = logging.getLogger(__name__)


def _load_jsonl(path: Path) -> list[RerankerExample]:
    """Load reranker examples from a JSONL file."""
    out: list[RerankerExample] = []
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            out.append(
                RerankerExample(
                    query=obj["query"],
                    passage=obj["passage"],
                    relevance_label=int(obj.get("relevance_label", 0)),
                    citation_grounding_label=float(obj.get("citation_grounding_label", 0.0)),
                    citation_metadata=obj.get("citation_metadata", {}),
                )
            )
    return out


@click.command()
@click.option(
    "--train-jsonl",
    type=click.Path(exists=True, path_type=Path),
    required=True,
    help="JSONL of training RerankerExamples.",
)
@click.option(
    "--val-jsonl",
    type=click.Path(exists=True, path_type=Path),
    required=True,
    help="JSONL of validation RerankerExamples.",
)
@click.option(
    "--output-dir",
    type=click.Path(path_type=Path),
    default=lambda: PATHS.models_dir / "reranker",
    show_default=True,
)
@click.option(
    "--lambda-values",
    type=float,
    multiple=True,
    default=RERANKER.lambda_sweep,
    show_default=True,
    help="Lambda values to sweep (one ckpt per value).",
)
@click.option(
    "--model-name",
    type=str,
    default=lambda: MODELS.reranker_base,
    show_default=True,
)
@click.option("--epochs", type=int, default=RERANKER.epochs, show_default=True)
@click.option("--batch-size", type=int, default=RERANKER.batch_size, show_default=True)
@click.option(
    "--learning-rate", type=float, default=RERANKER.learning_rate, show_default=True
)
@click.option("--grad-accum-steps", type=int, default=1, show_default=True)
@click.option(
    "--no-qlora", is_flag=True, help="Disable QLoRA (full-precision fine-tune)."
)
@click.option("--no-wandb", is_flag=True, help="Disable W&B logging.")
@click.option("--wandb-project", type=str, default=None)
@click.option("--wandb-entity", type=str, default=None)
@click.option("-v", "--verbose", is_flag=True)
def main(
    train_jsonl: Path,
    val_jsonl: Path,
    output_dir: Path,
    lambda_values: tuple[float, ...],
    model_name: str,
    epochs: int,
    batch_size: int,
    learning_rate: float,
    grad_accum_steps: int,
    no_qlora: bool,
    no_wandb: bool,
    wandb_project: str | None,
    wandb_entity: str | None,
    verbose: bool,
) -> None:
    """Run one training job per lambda; checkpoints land under ``output-dir``."""
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    ensure_dirs()

    train = _load_jsonl(train_jsonl)
    val = _load_jsonl(val_jsonl)
    logger.info("Loaded %d train / %d val examples", len(train), len(val))

    use_wandb = not no_wandb and bool(API_CFG.wandb_api_key)
    if not no_wandb and not API_CFG.wandb_api_key:
        logger.warning("WANDB_API_KEY not set; disabling W&B logging.")

    checkpoints: list[Path] = []
    for lam in lambda_values:
        logger.info("=== Training with lambda=%s ===", lam)
        run = None
        if use_wandb:
            import wandb

            run = wandb.init(
                project=wandb_project or API_CFG.wandb_project,
                entity=wandb_entity or (API_CFG.wandb_entity or None),
                name=f"reranker-lambda{lam}",
                config={"lambda": lam},
                reinit=True,
            )
        try:
            ckpt = train_reranker(
                train_examples=train,
                val_examples=val,
                model_name=model_name,
                output_dir=output_dir,
                lambda_=lam,
                epochs=epochs,
                batch_size=batch_size,
                learning_rate=learning_rate,
                use_qlora=not no_qlora,
                grad_accum_steps=grad_accum_steps,
                wandb_run=run,
            )
            checkpoints.append(ckpt)
            logger.info("Checkpoint for lambda=%s -> %s", lam, ckpt)
        finally:
            if run is not None:
                run.finish()

    logger.info("Sweep complete. Checkpoints:")
    for c in checkpoints:
        logger.info("  %s", c)


if __name__ == "__main__":
    main()
