# Recommender Escalation — Letter Still Missing After T-2

**When to use:** Letter is still missing 24-48 hours before the deadline, and the recommender has not responded to the T-2 follow-up.

**Purpose:** Save the application. This is not a fourth nudge to the recommender — this is contacting program admissions to ask whether the application can still proceed.

---

## Step 1: Contact program admissions (T-1, ~24h before deadline)

**To:** [Program admissions email]
**Subject:** Letter of recommendation status — John Paul L. Gabule, Applicant ID [###]

Dear [Program] Admissions,

I am writing to ask about the status of my application for the Fall 2028 PhD CS cycle. My applicant ID is [###]. The application is otherwise complete: SOP submitted, CV uploaded, transcripts received, application fee paid. Two of three letters of recommendation are uploaded; one remains outstanding.

The third recommender is [Recommender Name, Title, Institution]. I sent them initial materials on [date], a T-21 reminder on [date], a T-7 reminder on [date], and a final T-2 reminder on [date]. As of today, the portal shows the letter has not been received and I have not heard from the recommender.

Could you advise on:
1. Whether the application can be considered with two letters if the third is genuinely unable to submit
2. Whether the program would grant a 1-2 week extension for the third letter
3. Whether you can contact the recommender directly from your side

Either path would let the application move forward. I appreciate any guidance.

Thank you,
John Paul L. Gabule
johnpaullimgabule@gmail.com
[Phone]

---

## Step 2: Final ask to the recommender (in parallel, T-1)

**To:** [Recommender's email]
**Subject:** Final note: [Program] letter — deadline tomorrow

Dear Professor [Last Name],

The [Program] deadline is tomorrow. I haven't heard back about the letter, so I wanted to send one final note in case my earlier emails missed you.

I have also written to [Program] admissions asking whether they would grant an extension or accept the application with two letters. I am not blaming you for anything — I just want to make sure the application has every chance to proceed.

If you can submit at any point in the next 24 hours, the portal link is:
[link]

If you cannot, please tell me — I will withdraw the application from this program rather than have an incomplete file sit there.

Thank you for everything,
John Paul L. Gabule
johnpaullimgabule@gmail.com

---

## Step 3: Decision (T-0)

If the letter does not arrive by the deadline:

**Option A: Withdraw the application from this program**
- Email program admissions: "I am withdrawing my application for the Fall 2028 PhD CS cycle due to an incomplete file. Please refund the application fee if possible. — [Name]"
- Mark in `deadline_tracker_template.csv` as `withdrawn`

**Option B: Submit the incomplete application and ask for an extension**
- Some programs allow the rest of the application to be evaluated while the third letter arrives late
- Status in tracker: `submitted_incomplete_letter_pending`
- Follow up weekly until the letter arrives or the program reaches a decision

**Option C: Use a backup recommender**
- If you have a 4th recommender on standby (highly recommended), have them submit
- Most programs allow recommender swaps before the deadline if you go through the portal's "remove and re-invite" flow
- Status in tracker: `submitted_with_backup`

---

## Lessons-learned log entry

After resolution, log in `journal/decisions.md`:

```markdown
| 2027-XX-XX | Recommender [Name] letter did not arrive for [Program]; resolved via [option] | Outcome: [accepted-as-incomplete / withdrawn / backup-submitted] | Yes (next cycle: have a 4th backup recommender pre-briefed) |
```

---

## How to avoid needing this template

1. **Have 4 recommenders briefed, not 3.** The 4th is your insurance policy. Even if all 3 primary letters arrive, you've cost the 4th person ~30 min of "willing to write, not needed in the end."
2. **Send the T-21 + T-7 reminders religiously.** Most letters that go missing are not from a refusal but from oversight.
3. **Use Interfolio where possible.** Interfolio centralizes letters; if one program loses the letter, you can re-dispatch without bothering the recommender.
4. **Pre-brief recommenders in May 2027 (not Sep).** The 6-month lead time means September requests aren't "out of nowhere" and reminders feel natural.

---

## What NOT to do

- Do not send angry emails. Letters that arrive after an angry email are usually lukewarm.
- Do not publicly criticize the recommender on social media. Academia is small.
- Do not ask another professor to "lean on" the missing recommender. Awkward for everyone.
- Do not give up before T-0. Many last-minute letters arrive within hours of the deadline.
