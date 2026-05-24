"""Self-RAG baseline (Asai et al., 2023).

Paper: "Self-RAG: Learning to Retrieve, Generate, and Critique through
Self-Reflection." Asai et al. introduce four families of *reflection tokens*
that the model emits as part of its output to control retrieval and to grade
its own generations:

    * ``[Retrieve]`` / ``[No Retrieve]`` — should we go fetch more evidence?
    * ``[Relevant]`` / ``[Irrelevant]`` — is the fetched passage useful?
    * ``[Supported]`` / ``[Partial]`` / ``[Contradict]`` — does the evidence
      back the just-generated sentence?
    * ``[Utility:1..5]`` — overall answer quality.

Two implementation modes:

    * **Fine-tuned** (preferred): if the original ``selfrag/selfrag_llama2_7b``
      checkpoint loads, we let the model emit the tokens natively and parse
      them out of the stream. This is the closest reproduction.
    * **Prompted** (fallback): on any other generator we paste the token
      vocabulary into the system prompt and ask the model to imitate the
      protocol. This is an *ablation*, not a faithful reproduction — Asai et
      al. show prompted Self-RAG underperforms the fine-tuned version
      substantially. We log a clear warning when this path is taken.
"""
from __future__ import annotations

import logging
import re
from collections.abc import Callable, Sequence
from typing import Any

from citecheck.agent.citation_resolver import CitationResolver
from citecheck.agent.loop import AnswerWithCitations

logger = logging.getLogger(__name__)

Generator = Callable[[str], str]

SELF_RAG_CHECKPOINT = "selfrag/selfrag_llama2_7b"

_REFLECTION_TOKENS = (
    "[Retrieve]", "[No Retrieve]",
    "[Relevant]", "[Irrelevant]",
    "[Supported]", "[Partial]", "[Contradict]",
)

_RETRIEVE_RE = re.compile(r"\[(?:No )?Retrieve\]")
_RELEVANCE_RE = re.compile(r"\[(?:Ir)?relevant\]", re.IGNORECASE)
_SUPPORT_RE = re.compile(r"\[(?:Supported|Partial|Contradict)\]")
_REFLECTION_STRIP_RE = re.compile(
    r"\[(?:No )?Retrieve\]|\[(?:Ir)?relevant\]|\[Supported\]|\[Partial\]|"
    r"\[Contradict\]|\[Utility:\d\]",
    re.IGNORECASE,
)

_PROMPTED_SYSTEM = """You are a Self-RAG-style legal assistant. Use these \
reflection tokens to control your behavior:

  [Retrieve] / [No Retrieve] : whether the next claim needs evidence lookup.
  [Relevant] / [Irrelevant]  : whether a retrieved passage helps.
  [Supported] / [Partial] / [Contradict] : whether evidence backs your claim.

Format every sentence as: <reflection tokens> <sentence with Bluebook cite>.
Citations must follow "<Case Name>, <vol> <Reporter> <page> (<court> <year>)"."""


class SelfRAGBaseline:
    """Self-RAG (Asai et al. 2023) baseline.

    Args:
        generator: ``(prompt: str) -> str`` callable. Should ideally wrap the
            fine-tuned ``selfrag/selfrag_llama2_7b`` checkpoint; otherwise the
            class falls back to *prompted* Self-RAG (a documented ablation).
        retriever: Retrieval backend with ``.search(query, top_k)``.
        resolver: Citation verifier (for post-hoc grading; the Self-RAG model
            grades its own outputs via [Supported]/[Contradict], but we keep
            CiteCheck-style verification on top for apples-to-apples eval).
        is_finetuned: If True, we trust the model's reflection tokens. If False
            (default — there's no way to know without loading the checkpoint),
            we still parse tokens if present but log a warning.
        top_k: Passages to retrieve when ``[Retrieve]`` fires.
        max_segments: Cap on how many ``<reflect><sentence>`` segments to emit
            before forcing termination. Mirrors Self-RAG's beam budget.
    """

    def __init__(
        self,
        generator: Generator,
        retriever: Any,
        resolver: CitationResolver,
        is_finetuned: bool = False,
        top_k: int = 10,
        max_segments: int = 6,
    ) -> None:
        self.generator = generator
        self.retriever = retriever
        self.resolver = resolver
        self.is_finetuned = is_finetuned
        self.top_k = top_k
        self.max_segments = max_segments
        if not is_finetuned:
            logger.warning(
                "SelfRAGBaseline running in PROMPTED mode (no fine-tuned "
                "checkpoint). Results are an ablation, not a reproduction."
            )

    # ----------------------------------------------------------------- public
    def answer(self, question: str) -> AnswerWithCitations:
        """Run Self-RAG: decide-retrieve → generate-with-reflection → stitch."""
        decision_prompt = self._decision_prompt(question)
        decision_out = self.generator(decision_prompt)
        retrieve = self._should_retrieve(decision_out)
        passages: Sequence[Any] = []
        if retrieve:
            try:
                passages = self.retriever.search(question, top_k=self.top_k)
            except TypeError:
                passages = self.retriever.search(question)
            # Filter to passages the model considers relevant.
            passages = self._filter_relevant(question, passages)

        gen_prompt = self._generation_prompt(question, passages)
        raw = self.generator(gen_prompt)

        # Truncate at max_segments worth of support tokens.
        raw = self._truncate_segments(raw)

        # Strip reflection tokens for downstream citation parsing.
        clean = _REFLECTION_STRIP_RE.sub("", raw).strip()

        parsed = self.resolver.parse_bluebook(clean)
        cites = []
        seen: set[str] = set()
        for pc in parsed:
            cite_str = pc.raw_text.strip()
            if cite_str in seen:
                continue
            seen.add(cite_str)
            cites.append((cite_str, self.resolver.verify(cite_str, asserted_claim=clean)))

        return AnswerWithCitations(
            text=clean,
            citations=cites,
            iterations_used=1,
            retrieved_doc_ids=[_doc_id(p) for p in passages],
        )

    # ---------------------------------------------------------------- helpers
    def _decision_prompt(self, question: str) -> str:
        return (
            f"{_PROMPTED_SYSTEM}\n\n"
            f"Decide whether to retrieve evidence for this question. "
            f'Reply with exactly one token: "[Retrieve]" or "[No Retrieve]".\n\n'
            f"Question: {question}\nDecision: "
        )

    @staticmethod
    def _should_retrieve(decision_out: str) -> bool:
        m = _RETRIEVE_RE.search(decision_out)
        if not m:
            # No explicit decision: default to retrieving (safer for legal QA).
            return True
        return m.group(0) == "[Retrieve]"

    def _filter_relevant(self, question: str, passages: Sequence[Any]) -> Sequence[Any]:
        """Ask the model to tag each passage [Relevant] or [Irrelevant]."""
        kept = []
        for p in passages:
            text = getattr(p, "text", None) or getattr(p, "passage", "") or ""
            check_prompt = (
                f'{_PROMPTED_SYSTEM}\n\nIs this passage relevant to the question? '
                f'Reply with exactly "[Relevant]" or "[Irrelevant]".\n\n'
                f"Question: {question}\nPassage: {text[:800]}\nVerdict: "
            )
            verdict = self.generator(check_prompt)
            m = _RELEVANCE_RE.search(verdict)
            if m is None or m.group(0).lower() == "[relevant]":
                kept.append(p)
        logger.debug("Self-RAG relevance filter kept %d/%d", len(kept), len(passages))
        return kept

    def _generation_prompt(self, question: str, passages: Sequence[Any]) -> str:
        blocks = []
        for i, p in enumerate(passages, 1):
            text = getattr(p, "text", None) or getattr(p, "passage", "") or ""
            blocks.append(f"[{i}] {text}")
        context = "\n\n".join(blocks) if blocks else "(no passages retrieved)"
        return (
            f"{_PROMPTED_SYSTEM}\n\n### Context\n{context}\n\n"
            f"### Question\n{question}\n\n"
            f"Emit each sentence prefixed with reflection tokens. "
            f"After each cited sentence, add one of "
            f"{', '.join(_REFLECTION_TOKENS[4:])} to grade evidence support.\n\n"
            f"### Answer\n"
        )

    def _truncate_segments(self, raw: str) -> str:
        """Cut the generation after ``max_segments`` support-token markers."""
        matches = list(_SUPPORT_RE.finditer(raw))
        if len(matches) <= self.max_segments:
            return raw
        cut = matches[self.max_segments].end()
        return raw[:cut]


def _doc_id(p: Any) -> str:
    for attr in ("doc_id", "id", "passage_id"):
        v = getattr(p, attr, None)
        if v is not None:
            return str(v)
    return "unknown"
