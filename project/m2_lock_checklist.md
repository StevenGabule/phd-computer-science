# M2 Lock Checklist — Decisions Due by 2026-08-31

All decisions consolidated from `project/candidates.md`, `project/problem_statement.md`, Phase 1 plan, and Phase 2 plan. Resolve each before M2 (end of Foundation phase). Each decision blocks something in Phase 2.

---

## Hard locks (cannot start Phase 2 without)

### 1. Final research candidate
- [ ] Confirm **CiteCheck** as primary research project (recommended in candidates.md), OR
- [ ] Switch to **Candidate A: ContractTraj-Bench**, OR
- [ ] Switch to **Candidate B: AgentLex-RAG** (note: $800+ paid reviewer flag), OR
- [ ] Combine A + D as unified benchmark (stretch — risk of scope creep)
- **Why this matters:** Every subsequent decision and Phase 2 task assumes a specific candidate.
- **Inputs to weigh:** Updated Scite searches (re-run gap validation in late Aug); deep reads of taxonomy clusters 1 + 5 + 7; gut check after talking to ≥1 academic (Task 13 of Phase 1).

### 2. Specific subtask scope (if CiteCheck)
- [ ] Federal appellate + Supreme Court only (recommended for v1), OR
- [ ] Include state appellate courts (doubles annotation effort, broadens claim)
- **Why this matters:** Determines corpus size, annotation budget, and eval-set difficulty.

### 3. Annotator strategy
- [ ] Paid Upwork JD reviewer (~$2,000–$3,200 cash; 4-week turnaround on 500-item validation)
- [ ] Law-student collaborator (free; 8-week turnaround; risk of attrition; potential co-authorship)
- [ ] Self-only with adversarial seeding from Charlotin tracker (zero cost; lower coverage; v0.1 release)
- **Why this matters:** Phase 2 Task 26 forces this decision by Dec 21, 2026 at the latest; better to decide at M2 to allow recruitment lead time.

### 4. Plan B niche
- [ ] Identify a fallback project to swap in if M3 (Nov 2026) baseline reproduction reveals CiteCheck's gap has closed
- **Candidates to consider as Plan B:** ContractTraj-Bench (least overlap with CiteCheck infrastructure), a tighter subscope of CiteCheck (e.g., contract-citation-only, dropping case-law), or a niche found during July deep reads
- **Why this matters:** Without a Plan B, you may waste 2-3 months pivoting under pressure mid-Phase 2.

---

## Soft locks (can be deferred but should be decided)

### 5. Workshop venue priority
- [ ] Primary: NLLP @ EMNLP 2027 (recommended; Jun/Jul 2027 deadline)
- [ ] Backup: TrustNLP @ EMNLP 2027
- [ ] Alternative: AAAI 2028 (Aug 2027 deadline), ICLR 2028 Tiny Papers, ACL 2028 main/workshop
- **Why this matters:** Submission timing affects Phase 3 schedule. Pre-confirm dates as soon as CFPs publish.

### 6. Geographic program list final
- [ ] Lock at US + Europe top tier (current, 23 programs including NYU)
- [ ] Add Asia tier (NUS, KAIST, Tsinghua, Toronto, McGill) — adds 5+ programs and ~$500-700 in fees
- [ ] Drop Europe to focus on US only (smaller list, simpler logistics)
- **Why this matters:** Affects Phase 3 SOP customization workload (each program = ~3 hours of tailoring) and Phase 4 fee budget.

### 7. Specific recommenders
- [ ] Identify 4 specific recommenders by name (Phase 3 Task 43 due May 2027 — but ideally identified at M2)
- **Typical mix:** master's advisor (mandatory if available), research collaborator/PI, professor from key course, professional reference (only if research-leaning)
- **Why this matters:** Earlier identification = earlier conversations = stronger letters. 6-week lead time before earliest submission is the minimum.

### 8. Artifact commitments (from `applications/artifacts_strategy.md`)
- [ ] Confirm Option 2: Citation-existence verifier mini-paper (Jun-Sep 2026 — START NOW if confirming)
- [ ] Confirm Option 1: eyecite open-source PRs (Jun 2026 – Mar 2027)
- [ ] Decide on Option 4: Blog series (conditional on Phase 2 schedule)
- **Why this matters:** Option 2 specifically starts BEFORE Phase 2 — committing later loses the pre-Phase-2 window.

### 9. GRE strategy
- [ ] Verify per-program GRE requirements (most US top programs no longer require; Europe doesn't use)
- [ ] If required by ≥3 target programs: schedule GRE for Aug 2027 (budget $220 + ~80 hr prep)
- [ ] If only required by 1-2: drop those programs from list
- **Why this matters:** Avoid scrambling to take GRE in Phase 4 with applications already due.

---

## Information-gathering (do before deciding above)

- [ ] Re-run Scite gap validation searches in late August 2026 for each candidate niche (papers come out weekly)
- [ ] Email 2 academics (from `outreach/email_variants/` — Šavelka or Nyarko recommended) with problem statement for feedback
- [ ] Read Quevedo 2024 Legal NLP survey end-to-end (Task 3 of Phase 1)
- [ ] Deep-read 5 most relevant papers from Cluster 5 (Faithfulness/Citation) and Cluster 7 (Agent Evaluation) of `literature/taxonomy.md`
- [ ] Verify CourtListener API rate limits in current 2026 form (5,000 req/hr per Phase 2 plan — confirm)
- [ ] Check 2027 EMNLP / NAACL workshop CFPs as they publish (typically Feb-Apr 2027) — note exact deadlines

---

## How to use this checklist

1. **Today (May 25, 2026):** scan; verify nothing is already decided that needs updating.
2. **End of June 2026 (M1):** revisit; preliminary positions should be forming.
3. **Mid August 2026:** make first-pass commitments; share with reading group for sanity check.
4. **August 31, 2026 (M2 lock):** all hard locks resolved; write decisions to `journal/decisions.md`; commit to `project/problem_statement.md` v1.0; begin Phase 2 on Sep 1.
5. **Soft locks** can shift through Sep 2026 but ideally stable by end of September.
