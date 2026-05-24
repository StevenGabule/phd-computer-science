# Transcript Order Checklist

**Purpose:** Order all institutional transcripts well before the Phase 4 deadline rush. Most US registrars take 5-10 business days; some take 2-4 weeks. Do this in early October 2027 at the latest.

---

## Phase A — Inventory (do this once, in early October 2027)

- [ ] List every post-secondary institution attended (undergraduate, master's, any non-degree coursework, summer programs that issued transcripts)
- [ ] For each, note:
  - Institution name and full mailing address
  - Registrar email + phone
  - Transcript ordering URL (most use Parchment, Credentials Solutions, or National Student Clearinghouse; some have in-house systems)
  - Whether they support electronic delivery (PDF to email) or paper-only
  - Typical processing time (call the registrar if not documented)
  - Cost per copy

## Phase B — Per-Program Requirements

Most US programs accept unofficial transcripts (PDF upload) at the time of application, then require official transcripts only if admitted. But some require official at submission. Verify per program:

- [ ] For each program, check what's required at the application stage:
  - "Unofficial PDF upload" → upload a scan or downloaded student-portal PDF
  - "Official transcript via institution-to-institution electronic delivery" → order through Parchment / NSC and select the program's registrar as recipient
  - "Official paper transcript mailed" → least common; budget extra time and cost
- [ ] Note any program with non-standard requirements (some want a separate "academic record" form filled by the registrar)

## Phase C — Place Orders

For each (institution, program) pair where official transcripts are required:

- [ ] Order through the institution's transcript provider
- [ ] Verify the destination address / email matches the program's stated requirement
- [ ] Pay the per-copy fee (typically $5-25 per copy)
- [ ] Note the order tracking number
- [ ] Add a row to `deadline_tracker_template.csv` `notes` column

## Phase D — Track Delivery

- [ ] Verify each transcript was received by the program (most portals show transcript status under "documents received")
- [ ] If not received within 10 business days of order:
  - Contact the source institution's registrar to confirm the order shipped
  - Contact the destination program's admissions office to verify the address / email
  - Log in `blockers.md`

## Phase E — Have Backup Copies

- [ ] Keep digital copies (PDF) of every transcript for your own records — in case a program portal loses your upload mid-process
- [ ] Keep at least one official paper copy at home — some programs only ask for paper after admission

---

## Cost estimate

20 programs × ~$15/transcript × 2-3 institutions = **~$600-900** in transcript fees.

If institutional fees seem prohibitive:
- Many institutions allow you to order one transcript to yourself (self-as-recipient) and then upload as "unofficial" — saves $$ if the program accepts unofficial
- Some institutions offer free transcripts to alumni who have donated within the last year (worth asking)

---

## Common gotchas

1. **Degree-conferral date not yet recorded.** If you finish your master's in spring 2027, the conferral may not show on the transcript until summer 2027. Some programs reject transcripts that say "in progress" — verify conferral date before ordering.
2. **Course name mismatches across transcripts.** If you took a cross-listed course (e.g., "CS 489 / EE 489"), some programs flag the discrepancy. Have an explanation ready in the application notes field.
3. **Non-English transcripts.** International institutions usually issue transcripts in the local language. For US/UK applications, need either (a) official translation or (b) WES evaluation. WES takes 4-6 weeks; budget accordingly.
4. **Final grades may not appear on a transcript ordered before the final grade-posting date.** If applying mid-semester (Dec 2027), order transcripts after the final grade-posting date for that semester (typically late December for fall semester).
5. **Registrar holiday closures.** Many US registrars close Dec 20-Jan 2. Order before Dec 15 to avoid holiday delays.

---

## Pre-application timeline

| When | Action |
|------|--------|
| Early Oct 2027 | Inventory institutions; identify per-program requirements |
| Mid Oct 2027 | Place orders for institution-to-institution delivery |
| Late Oct 2027 | Verify delivery; chase any non-delivered orders |
| Nov 2027 | Re-order if anything is still missing |
| Dec 2027 | Spot-check before each submission that the program has received the transcript |
