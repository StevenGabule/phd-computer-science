# Application Blockers Log

**Purpose:** Live log of portal bugs, transcript delays, recommender hiccups, and any other obstacle hit during Phase 4 submission (Oct-Dec 2027). The single most valuable document during the application crunch — share it with anyone helping you apply.

**Usage:** Add a row the moment a blocker appears. Don't wait until you've fixed it. The act of writing it down forces you to be specific and often suggests the fix.

---

## Active blockers

| Date | Program | Issue (1 line) | What I tried | Status | Owner | ETA |
|------|---------|----------------|--------------|--------|-------|-----|

## Resolved blockers (move from active when closed)

| Date opened | Date closed | Program | Issue | Resolution | Hours spent |
|-------------|-------------|---------|-------|------------|-------------|

---

## Templates for common blocker types

### Portal upload rejected

```
| 2027-XX-XX | [Program] | PDF upload rejected — "file too large (>5MB)" | Compressed via `gs -dPDFSETTINGS=/ebook` to 1.8MB | resolved | self | done |
```

### Recommender invitation not received

```
| 2027-XX-XX | [Program] | Recommender [Name] reports no portal invitation in inbox or spam | Asked them to whitelist `*.applyweb.com`; re-sent invitation via portal | active | self | 24h |
```

### Transcript order delay

```
| 2027-XX-XX | All US programs | Master's institution registrar says transcript request will take 10 business days vs. expected 5 | Followed up with registrar; verified expedited option ($25 extra) is available | active | registrar | 5 days |
```

### Fee waiver rejected

```
| 2027-XX-XX | [Program] | Fee waiver application rejected ("submitted after waiver deadline") | Submitted full fee; logged for "lessons learned" doc | resolved | self | done |
```

### GRE score-send failed

```
| 2027-XX-XX | [Program] | ETS score-send failed — institution code mismatch | Verified correct GRE institution code at gradadmissions.[program].edu; re-sent score | active | ETS | 7-10 days |
```

### Recommender silence

```
| 2027-XX-XX | All | Recommender [Name] not responding to T-21 reminder | Sent T-14 follow-up; if no response by T-7, escalate (see escalation_emails/) | active | recommender | T-7 |
```

### Portal session timeout / data loss

```
| 2027-XX-XX | [Program] | Portal timed out after 30 min and lost in-progress SOP edits | Restored from local backup; switched to drafting in Google Docs and pasting in | resolved | self | done |
```

### Unexpected required document

```
| 2027-XX-XX | [Program] | Portal asks for "diversity statement" not listed on admissions page | Wrote 1-page diversity statement; saved template for similar programs | resolved | self | 2 hours |
```

---

## Weekly review protocol

Every Sunday during Oct-Dec 2027:
1. Read every active blocker; if status hasn't changed in 7 days, escalate.
2. Move resolved blockers to the resolved table; log total hours.
3. Cross-check `deadline_tracker_template.csv` for any program approaching deadline with an open blocker.
4. If 3+ blockers are active simultaneously, consider triage: which programs are highest-priority?

## Escalation thresholds

- **Open >5 days, deadline >2 weeks away:** Continue monitoring; nudge external party.
- **Open >2 days, deadline <2 weeks away:** Daily check-ins; escalate to program admissions office.
- **Open >24 hours, deadline <72 hours away:** Email program admissions directly; request extension or workaround.
- **Open at T-12 hours to deadline:** Phone the program; some admissions offices respond to emergencies that don't reach email.

## What goes in here vs. what doesn't

**Goes here:**
- Anything blocking a specific application from being completed on time
- Issues that recurred across programs (worth tracking as a pattern)
- Unexpected requirements you only discovered mid-submission

**Doesn't go here:**
- Routine submission steps (those are in `final_week_protocol.md`)
- General anxieties or impostor-syndrome moments (those are personal; a separate journal is better)
- Issues with the LaTeX paper or research code (those go in the citecheck CHANGELOG)
