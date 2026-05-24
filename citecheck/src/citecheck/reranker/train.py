"""Reranker training loop with QLoRA (PEFT) + W&B logging.

Notes
-----
* QLoRA: 4-bit NF4 quantization on the backbone + LoRA adapters on the
  attention QKV projections (and FFN where present). The two regression
  heads stay full-precision (they are tiny, ~hidden_size+1 params each).
* Schedule: AdamW with linear warmup + cosine decay over total training
  steps (``epochs * steps_per_epoch / grad_accum``).
* Logging: per-step total loss + each component, validation loss at every
  epoch, plus checkpoint name in W&B summary.

The function is structurally complete and calls real APIs; we degrade
gracefully when CUDA is unavailable (QLoRA requires a CUDA bitsandbytes
build) by falling back to full-precision fine-tuning on CPU.
"""
from __future__ import annotations

import logging
import math
import os
from pathlib import Path
from typing import TYPE_CHECKING, Any

import torch
from torch.optim import AdamW
from torch.utils.data import DataLoader

from citecheck.config import MODELS, PATHS, RERANKER
from citecheck.reranker.dataset import RerankerDataset, RerankerExample
from citecheck.reranker.loss import MultiObjectiveLoss
from citecheck.reranker.model import CrossEncoderReranker

if TYPE_CHECKING:
    import wandb as wandb_t  # noqa: F401 — type alias

logger = logging.getLogger(__name__)


def _build_qlora_model(model_name: str) -> CrossEncoderReranker:
    """Construct a 4-bit quantized cross-encoder wrapped with LoRA adapters."""
    from peft import LoraConfig, get_peft_model
    from transformers import AutoModel, AutoTokenizer, BitsAndBytesConfig

    bnb_cfg = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True,
        bnb_4bit_compute_dtype=torch.bfloat16,
    )
    logger.info("Loading 4-bit quantized backbone %s", model_name)
    backbone = AutoModel.from_pretrained(model_name, quantization_config=bnb_cfg)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    lora_cfg = LoraConfig(
        r=16,
        lora_alpha=32,
        lora_dropout=0.05,
        bias="none",
        task_type="FEATURE_EXTRACTION",
        # Most encoder models expose "query", "key", "value", "dense" — peft
        # auto-resolves substrings.
        target_modules=["query", "key", "value", "dense"],
    )
    peft_backbone = get_peft_model(backbone, lora_cfg)

    # Build the wrapper without re-loading the backbone.
    model = CrossEncoderReranker.__new__(CrossEncoderReranker)
    torch.nn.Module.__init__(model)
    model.model_name = model_name
    model.backbone = peft_backbone
    hidden = peft_backbone.config.hidden_size
    model.dropout = torch.nn.Dropout(0.1)
    model.relevance_head = torch.nn.Linear(hidden, 1)
    model.groundedness_head = torch.nn.Linear(hidden, 1)
    model.tokenizer = tokenizer
    model._init_heads()  # type: ignore[attr-defined]
    return model


def _collate(batch: list[dict[str, torch.Tensor]]) -> dict[str, torch.Tensor]:
    return {k: torch.stack([b[k] for b in batch]) for k in batch[0]}


def _evaluate(
    model: CrossEncoderReranker,
    loader: DataLoader,
    loss_fn: MultiObjectiveLoss,
    device: torch.device,
) -> dict[str, float]:
    model.eval()
    totals = {"loss": 0.0, "relevance": 0.0, "groundedness": 0.0}
    n_batches = 0
    with torch.inference_mode():
        for batch in loader:
            input_ids = batch["input_ids"].to(device)
            attn = batch["attention_mask"].to(device)
            rel_y = batch["relevance_label"].to(device)
            gnd_y = batch["groundedness_label"].to(device)
            rel_logit, gnd_logit = model(input_ids, attn)
            loss = loss_fn(rel_logit, gnd_logit, rel_y, gnd_y)
            parts = loss_fn.components(rel_logit, gnd_logit, rel_y, gnd_y)
            totals["loss"] += float(loss.item())
            totals["relevance"] += float(parts["relevance"].item())
            totals["groundedness"] += float(parts["groundedness"].item())
            n_batches += 1
    return {k: v / max(1, n_batches) for k, v in totals.items()}


def train_reranker(
    train_examples: list[RerankerExample],
    val_examples: list[RerankerExample],
    model_name: str | None = None,
    output_dir: Path | None = None,
    lambda_: float = 0.5,
    epochs: int = RERANKER.epochs,
    batch_size: int = RERANKER.batch_size,
    learning_rate: float = RERANKER.learning_rate,
    use_qlora: bool = True,
    grad_accum_steps: int = 1,
    warmup_ratio: float = RERANKER.warmup_ratio,
    wandb_run: Any = None,
    log_every: int = 20,
    seed: int = 0,
) -> Path:
    """Train the two-head cross-encoder reranker with QLoRA.

    Args:
        train_examples: Training :class:`RerankerExample` list.
        val_examples: Validation list.
        model_name: HF backbone id; defaults to ``MODELS.reranker_base``.
        output_dir: Where checkpoints are written. A sub-folder
            ``reranker_lambda{lambda_}`` is created under it. Defaults to
            ``PATHS.models_dir / "reranker"``.
        lambda_: Weight on the groundedness loss term.
        epochs, batch_size, learning_rate: Standard hyperparameters.
        use_qlora: If True (default), load the backbone in 4-bit and attach
            LoRA adapters. Requires CUDA + bitsandbytes; falls back to
            full-precision training on CPU.
        grad_accum_steps: Number of micro-batches per optimizer step.
        warmup_ratio: Linear warmup fraction of total steps.
        wandb_run: Optional ``wandb.Run`` to log into; if ``None`` we log to
            stdout only.
        log_every: Steps between training-loss logs.
        seed: RNG seed.

    Returns:
        Path to the saved checkpoint directory.
    """
    torch.manual_seed(seed)
    model_name = model_name or MODELS.reranker_base
    base_dir = Path(output_dir) if output_dir is not None else PATHS.models_dir / "reranker"
    ckpt_dir = base_dir / f"reranker_lambda{lambda_}"
    ckpt_dir.mkdir(parents=True, exist_ok=True)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    if use_qlora and not torch.cuda.is_available():
        logger.warning(
            "QLoRA requested but CUDA is unavailable; falling back to "
            "full-precision training on CPU. Use a GPU for real runs."
        )
        use_qlora = False

    if use_qlora:
        model = _build_qlora_model(model_name)
    else:
        model = CrossEncoderReranker(model_name=model_name)
    model.to(device)

    train_ds = RerankerDataset(train_examples, tokenizer=model.tokenizer)
    val_ds = RerankerDataset(val_examples, tokenizer=model.tokenizer)
    train_loader = DataLoader(
        train_ds, batch_size=batch_size, shuffle=True, collate_fn=_collate, drop_last=True
    )
    val_loader = DataLoader(
        val_ds, batch_size=batch_size, shuffle=False, collate_fn=_collate
    )

    loss_fn = MultiObjectiveLoss(lambda_=lambda_)
    optimizer = AdamW(
        (p for p in model.parameters() if p.requires_grad),
        lr=learning_rate,
        weight_decay=0.01,
    )
    total_micro = max(1, len(train_loader)) * epochs
    total_steps = max(1, total_micro // grad_accum_steps)
    warmup_steps = int(warmup_ratio * total_steps)

    def lr_lambda(step: int) -> float:
        if step < warmup_steps:
            return step / max(1, warmup_steps)
        progress = (step - warmup_steps) / max(1, total_steps - warmup_steps)
        return 0.5 * (1.0 + math.cos(math.pi * progress))

    scheduler = torch.optim.lr_scheduler.LambdaLR(optimizer, lr_lambda)

    if wandb_run is not None:
        wandb_run.config.update(
            {
                "lambda": lambda_,
                "epochs": epochs,
                "batch_size": batch_size,
                "learning_rate": learning_rate,
                "warmup_ratio": warmup_ratio,
                "grad_accum_steps": grad_accum_steps,
                "use_qlora": use_qlora,
                "model_name": model_name,
                "n_train": len(train_examples),
                "n_val": len(val_examples),
            },
            allow_val_change=True,
        )

    global_step = 0
    best_val_loss = math.inf
    for epoch in range(epochs):
        model.train()
        optimizer.zero_grad(set_to_none=True)
        for micro_idx, batch in enumerate(train_loader):
            input_ids = batch["input_ids"].to(device)
            attn = batch["attention_mask"].to(device)
            rel_y = batch["relevance_label"].to(device)
            gnd_y = batch["groundedness_label"].to(device)
            rel_logit, gnd_logit = model(input_ids, attn)
            loss = loss_fn(rel_logit, gnd_logit, rel_y, gnd_y) / grad_accum_steps
            loss.backward()

            if (micro_idx + 1) % grad_accum_steps == 0:
                torch.nn.utils.clip_grad_norm_(
                    (p for p in model.parameters() if p.requires_grad), max_norm=1.0
                )
                optimizer.step()
                scheduler.step()
                optimizer.zero_grad(set_to_none=True)
                global_step += 1

                if global_step % log_every == 0:
                    parts = loss_fn.components(rel_logit, gnd_logit, rel_y, gnd_y)
                    msg = (
                        f"epoch={epoch} step={global_step} "
                        f"loss={loss.item() * grad_accum_steps:.4f} "
                        f"rel={parts['relevance'].item():.4f} "
                        f"gnd={parts['groundedness'].item():.4f} "
                        f"lr={scheduler.get_last_lr()[0]:.2e}"
                    )
                    logger.info(msg)
                    if wandb_run is not None:
                        wandb_run.log(
                            {
                                "train/loss": loss.item() * grad_accum_steps,
                                "train/relevance": parts["relevance"].item(),
                                "train/groundedness": parts["groundedness"].item(),
                                "train/lr": scheduler.get_last_lr()[0],
                                "epoch": epoch,
                            },
                            step=global_step,
                        )

        val_metrics = _evaluate(model, val_loader, loss_fn, device)
        logger.info("Validation epoch=%d: %s", epoch, val_metrics)
        if wandb_run is not None:
            wandb_run.log({f"val/{k}": v for k, v in val_metrics.items()}, step=global_step)

        if val_metrics["loss"] < best_val_loss:
            best_val_loss = val_metrics["loss"]
            model.save_pretrained(ckpt_dir)
            logger.info("New best val_loss=%.4f; saved to %s", best_val_loss, ckpt_dir)

    if wandb_run is not None:
        wandb_run.summary["best_val_loss"] = best_val_loss
        wandb_run.summary["checkpoint_dir"] = str(ckpt_dir)

    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
    return ckpt_dir
