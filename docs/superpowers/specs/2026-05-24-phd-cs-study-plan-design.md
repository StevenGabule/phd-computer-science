# PhD CS Application Strengthening Plan — Design Spec

**Date:** 2026-05-24
**Author:** John Paul L. Gabule (with Claude)
**Status:** Approved draft, awaiting user review
**Time horizon:** May 2026 – December 2027 (18 months)
**Target:** PhD CS applications for Fall 2028 entry (deadlines Dec 2027 – Jan 2028)

---

## 1. Context

- Applicant: Master's-level graduate in CS / AI / related field.
- Goal: maximize competitiveness for PhD CS admission with an applied AI/NLP focus.
- Methods bias: agentic systems, RAG, fine-tuning. Domain selected opportunistically.
- Chosen research domain: **Legal / contracts** (agentic RAG application).
- Approach selected: **Research Portfolio Sprint** — invest the majority of available time in producing one publishable research artifact rather than spreading thin across coursework or many small projects.

## 2. Why this approach

For applied-track CS PhD applicants with a master's already in hand, the marginal value of additional coursework is low. Admissions committees read SOPs for evidence the applicant can *do research*. A single focused research project — even an unpublished or workshop-only output — is the strongest demonstrable evidence. Literature search (Scite, May 2026) confirms two facts that shape this plan:

1. **LLM agents and agentic RAG** are among the most active publishable subfields for 2025–2026, with multiple new evaluation benchmarks and methodology papers (Shen et al., 2026; Shah, 2026; Fu et al., 2025; Cheng et al., 2025; Low et al., 2025; Gonzalez-Pumariega et al., 2025).
2. **Legal-domain agentic RAG** is comparatively underserved versus medical, financial, and general-purpose RAG, leaving clear publishable niches.

## 3. Architecture

Four parallel tracks over four phases.

### Tracks

| Track | Name | Weight |
|---|---|---|
| R | Research Project | 70% |
| C | Curriculum Depth | 15% |
| A | Application Materials | 10% |
| M | Methodology & Metacognition | 5% |

### Phases

| Phase | Months | Focus |
|---|---|---|
| 1. Foundation | May–Aug 2026 | Literature map; lock niche; learn methods stack |
| 2. Build | Sep 2026 – Apr 2027 | Execute research project; experiments + writing |
| 3. Publish & Apply | May–Sep 2027 | Workshop submission; finalize application materials |
| 4. Application Push | Oct–Dec 2027 | SOPs, recommenders, submissions |

## 4. Track R — Research Project (the centerpiece)

**Topic:** Agentic Retrieval-Augmented Generation for legal/contract tasks.
**Form of output:** Workshop paper + arXiv preprint + open-source code release.
**Target venues:** NeurIPS workshops, ACL/EMNLP/NAACL workshops, AAAI student abstract, ICLR Tiny Papers / Blogposts track.

### Specific subtask candidates (to lock in M2)

- Contract clause review and risk flagging
- Case law retrieval with citation reasoning
- Statute interpretation and cross-referencing
- M&A due diligence document review
- Compliance question answering across regulatory corpora

Baselines to reproduce: **LegalBench** and **ContractNLI** family.

### Milestones

| ID | Date | Deliverable |
|---|---|---|
| M1 | Jun 2026 | Literature map: 50-paper reading list, taxonomy of legal NLP + agentic RAG approaches |
| M2 | Aug 2026 | Niche locked; 1-page problem statement; 1–2 academics consulted via cold email |
| M3 | Nov 2026 | Baseline reproduction: 2–3 existing methods replicated on a small legal task |
| M4 | Feb 2027 | Novel contribution scoped, prototyped, and validated on small data |
| M5 | May 2027 | Full experiments complete; ablations and stability checks done |
| M6 | Jul 2027 | Paper draft v1; internal review (advisor, online community, paper-swap) |
| M7 | Sep 2027 | Workshop submission; arXiv preprint |

### Compute and tools

- Models: 7B–13B open-weight models (Llama, Qwen, Mistral) usable via QLoRA on consumer GPU or Colab Pro.
- Frameworks: PyTorch, Hugging Face Transformers + PEFT, LangChain or LlamaIndex (or direct implementations), Weights & Biases for experiment tracking.
- Storage: GitHub for code; Hugging Face Hub for model/dataset artifacts.

## 5. Track C — Curriculum Depth

Selective deepening only where it enables the research project. Master's-level foundation is assumed.

| Subject | Treatment | Rationale |
|---|---|---|
| ML & Deep Learning | Refresh + advanced (RLHF, instruction tuning, retrieval models) | Foundation for agentic systems |
| Natural Language Processing | Deep dive (information retrieval, transformers, evaluation methodology) | Directly serves the project |
| Advanced Software Engineering | Light touch (patterns for ML systems and experiment infrastructure) | Enables clean reproducible experiments |
| Intelligent Systems | Light touch (planning, search, multi-agent fundamentals) | Background for agent reasoning |
| Advanced Algorithm Design | Skip unless target program qual exam requires | Master's-level coverage assumed |
| Advanced Computer Architecture | Skip | Not load-bearing for AI/NLP applied research |
| HCI | Skip unless target program requires | Optional add-on |
| Research Methods | Embedded in Track M | Avoid double-counting |
| Data Science & Big Data | Light, as project pipeline needs | Just-in-time |
| Graduate Seminar | Replicate via paper-reading group | Track M activity |

### Concrete resources

- **NLP:** Stanford CS224N; Jurafsky & Martin, *Speech and Language Processing*, 3rd edition draft
- **Deep Learning:** Goodfellow, *Deep Learning*; Zhang et al., *Dive into Deep Learning* (d2l.ai)
- **LLMs / Agents / RAG:** Stanford CS336 (LLMs from scratch); ACL 2024–2025 tutorials on RAG and agents
- **Legal NLP:** Stanford CodeX seminars; ACL Natural Legal Language Processing workshop proceedings

## 6. Track A — Application Materials

| Month | Deliverable |
|---|---|
| Jun 2026 | Target program list: 15–25 programs, mix of reach/match/safety |
| Jul–Aug 2026 | Identify 30–50 candidate advisors; read 2–3 recent papers per advisor |
| Sep 2026 onward | Begin advisor cold-email outreach (1 paragraph showing engagement with their work) |
| Mar 2027 | SOP draft v1; shared narrative core, per-program tailoring later |
| Jun–Jul 2027 | Identify 3–4 recommenders; prepare "rec packet" (CV + draft SOP + accomplishment list) |
| Aug 2027 | GRE if any target program requires (most top US CS programs no longer require it; verify per program) |
| Sep 2027 | Lock final program list; produce tailored SOP per program |
| Oct–Dec 2027 | Submit applications (most deadlines Dec 1 – Jan 15) |

### Outreach guidance

- Target younger faculty (assistant professors) — they reply at higher rates and have more capacity to take students.
- Email length: short. One paragraph identifying a specific paper of theirs, one paragraph on your project relevance, one paragraph on your ask (a brief call, advice on direction).
- Send 30+ emails. Expect a 10–20% response rate.

## 7. Track M — Methodology & Metacognition

- **Weekly literature workflow:** 3 papers skimmed per week, 1 deeply read with structured notes (problem / method / results / limitations / questions).
- **Monthly retrospective (30–60 min):** what's working, what's blocked, what to change for next month.
- **Paper-reading group:** join one (ML Collective, Cohere For AI, Eleuther, local university journal club). Replaces the "Graduate Seminar" course in the curriculum.
- **Public writing:** monthly blog post or GitHub README log on research progress. Demonstrates research thinking to admissions reviewers.

## 8. Weekly cadence (reference target, ~40 hrs/week)

| Day | Block | Hours |
|---|---|---|
| Mon–Fri AM (2h each) | Research project deep work (Track R) | 10 |
| Mon–Fri PM (2h each) | Curriculum + coding implementation (Track R + C) | 10 |
| Tue + Thu evening | Literature reading (Track R + M) | 4 |
| Wed evening | Application work (Track A) | 4 |
| Fri evening | Writing — blog post, paper draft, notes (Track M + R) | 4 |
| Sat AM | Paper-reading group / seminar (Track M) | 2 |
| Sat PM | Buffer / catch-up | 3 |
| Sun | Rest + weekly retrospective (30 min) | 3 |

Scale to real availability. If working full-time or in school, halve block sizes and extend the calendar accordingly.

## 9. Risks and mitigations

| Risk | Likelihood | Mitigation |
|---|---|---|
| Research project stalls at M3 (baseline reproduction) | High | Scope to small public datasets; have a Plan B niche identified at M2 |
| No GPU access | Medium | Colab Pro / Lambda / Kaggle; restrict to 7B–13B with QLoRA |
| Cold-email outreach gets no responses | Medium | Send 30+; one good response is enough; target assistant professors |
| Workshop submission rejected | Medium | arXiv preprint and "submitted to X" both count on CV |
| Solo burnout | Medium | Reading group + monthly retrospective enforce accountability |
| Domain rabbit hole — legal NLP requires legal expertise | Medium | Partner with a law student or legal professional for domain validation by M2 |

## 10. Success criteria

- **Minimum:** Workshop submission (regardless of outcome) + arXiv preprint + 4–6 tailored SOPs + 3 strong recommendation letters. Competitive at mid-tier programs.
- **Target:** Above + accepted workshop paper + clear advisor interest from 1–2 target programs. Competitive at top-30 programs.
- **Stretch:** Above + main-conference submission + co-authorship on a second paper through collaboration. Competitive at top-10 programs.

## 11. Open items (to resolve in Phase 1)

- Lock the specific legal subtask in M2 (Aug 2026).
- Identify Plan B niche for the research project in case M3 reproduction fails.
- Decide whether to formally enroll in any MOOC certificates (optional; not load-bearing for admissions).
- Confirm GRE requirements for each target program.
- Identify the 3–4 specific recommenders by Mar 2027 at the latest.

---

## References

Cheng, Y., Soltani Moakhar, A., Fan, C., et al. (2025). Temporal blindness in multi-turn LLM agents: Misaligned tool use vs. human time perception. *arXiv*. https://doi.org/10.48550/arxiv.2510.23853

Chen, S., Zhao, M., Xu, L., et al. (2025). DEPO: Dual-efficiency preference optimization for LLM agents. *arXiv*. https://doi.org/10.48550/arxiv.2511.15392

Chen, Y., Yao, Z., Liu, Y., et al. (2025). StockBench: Can LLM agents trade stocks profitably in real-world markets? *arXiv*. https://doi.org/10.48550/arxiv.2510.02209

Fu, L., Ding, X., Zhu, Y., et al. (2025). CATArena: Evaluation of LLM agents through iterative tournament competitions. *arXiv*. https://doi.org/10.48550/arxiv.2510.26852

Gonzalez-Pumariega, G., Su Yean, L., Sunkara, N., et al. (2025). Robotouille: An asynchronous planning benchmark for LLM agents. *arXiv*. https://doi.org/10.48550/arxiv.2502.05227

Haider, S. A., Prabha, S., Gomez Cabello, C. A., et al. (2025). The development and evaluation of a retrieval-augmented generation large language model virtual assistant for postoperative instructions. *Bioengineering*, 12(11), 1219. https://doi.org/10.3390/bioengineering12111219

Lei, Y., Xie, H., Zhao, J., et al. (2025). MSCoRe: A benchmark for multi-stage collaborative reasoning in LLM agents. *arXiv*. https://doi.org/10.48550/arxiv.2509.17628

Low, Y., Jackson, M. L., Hyde, R. J., et al. (2025). Answering real-world clinical questions using large language model, retrieval-augmented generation, and agentic systems. *Digital Health*, 11. https://doi.org/10.1177/20552076251348850

Martin, A., Witschel, H. F., & Mandl, M. M. (2024). Semantic verification in large language model-based retrieval augmented generation. *Proceedings of the AAAI Symposium Series*, 3(1), 188–192. https://doi.org/10.1609/aaaiss.v3i1.31199

Shah, E. (2026). The state of evaluating LLM agents. *SSRN*. https://doi.org/10.2139/ssrn.6172280

Shen, Y., Yang, Y., Xi, Z., et al. (2026). SciAgentGym: Benchmarking multi-step scientific tool-use in LLM agents. *arXiv*. https://doi.org/10.48550/arxiv.2602.12984

Sledzieski, S., Kshirsagar, M., Baek, M., et al. (2024). Democratizing protein language models with parameter-efficient fine-tuning. *Proceedings of the National Academy of Sciences*, 121. https://doi.org/10.1073/pnas.2405840121

Superbi, J., Pinto, H. S., & Santos, E. (2024). Enhancing large language model performance on ENEM math questions using retrieval-augmented generation. *SBC Brazilian Symposium on Computing Science*, 56–63. https://doi.org/10.5753/bresci.2024.243977

Wang, L., Yi, D., Jose, D., et al. (2025). Enterprise large language model evaluation benchmark. *CSIT*, 01–19. https://doi.org/10.5121/csit.2025.152001

Yang, Q., Zuo, H., Su, R., et al. (2025). Dual retrieving and ranking medical large language model with retrieval augmented generation. *Scientific Reports*, 15(1). https://doi.org/10.1038/s41598-025-00724-w

Yu, D., Wang, Y., Jin, S., et al. (2025). YpathRAG: A retrieval-augmented generation framework and benchmark for pathology. *arXiv*. https://doi.org/10.48550/arxiv.2510.08603
