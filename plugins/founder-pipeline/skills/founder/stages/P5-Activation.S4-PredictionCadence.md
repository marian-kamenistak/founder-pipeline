# P5.S4 — Prediction cadence: wire the recurring runs → `P5-Activation.S4-PredictionCadence.md`

**Phase: P5-Activation** (closes the phase)

**Earns its keep** for every stream with an ongoing content/service motion — the P1.S4 hypothesis run made the founding bets; this step makes sure they get GRADED and refreshed on a schedule, not by vibes. **Skip only if** the stream is a one-off engagement or has no content/SEO motion (record the skip in `brief.md`).

## Steps

1. **The ledger already exists** — P1.S4 created `predictions/PREDICTIONS.md` + the founding snapshot. Verify it's intact and the founding bets carry executable indicator commands + check dates (they were written under `/prediction`'s hard rules; if any row is missing its command, fix it NOW — step 0 of the next run depends on it).
2. **Wire the recurring run.** Default: add a dated entry to the stream's `queues/manual-queue.md` — "run `/prediction` live mode for <stream> (quarterly; next: <date ~+3 months>)" — AND register the stream on whatever scheduled surface the owner actually runs:
   - **If you have a scheduler** — cron, a CI schedule (GitHub Actions `schedule`, GitLab pipeline schedule), a hosted task queue, or an OS job runner — register the stream there as a recurring quarterly job, and **verify it is actually loaded** by listing the scheduler's own registry and pasting the matching line into the step file. A job you wrote but never verified is not wired. If your setup keeps a per-stream profile file for recurring runs (competitor set + keyword seeds), create the profile from P1.S5 / P4.S1 — never re-derive those artifacts.
   - **Otherwise** `/prediction` live mode runs on the queue cadence — no new scheduled job needed, but a queue row has no executor: register the run date on an existing scheduled surface (a recurring job that already fires and already reads a checklist file), or require the owner to explicitly accept "manual-fire risk" in the sign-off, recorded in `brief.md`.

   **Bind the dates:** the wired cadence's first run date must be ≤ the earliest founding-bet check date; otherwise add an interim dated grading entry — a cadence that first fires after the bets come due grades nothing.
3. **Mode flip note:** from now on runs use **live mode** — the stream has a site, a competitor set (P1.S5), a keyword contract (P4.S1), and an ACTION-PLAN once P6.S3 ships; the greenfield execution-plan variant retires for this stream.
4. **First graded horizon:** state when the founding bets' earliest check date arrives and what gets graded then — that date goes into the checkpoint summary and `brief.md`.
5. **`/critical` check** on the wiring (not the predictions): does the profile/queue entry reuse the artifacts P1.S5/P4.S1 locked, are the indicator commands executable by someone who wasn't in this conversation, and is any founding indicator a vanity indicator — one that can rise with zero customer contact?

**Write to** `P5-Activation.S4-PredictionCadence.md`: ledger status line, cadence decision (queue-only vs scheduled job, naming the scheduler and the job/profile path), mode-flip note, first grading date.

**Def-of-success — ALL must pass before owner sign-off:**
- `predictions/PREDICTIONS.md` intact; every founding row has an executable indicator command + threshold + check date.
- Every founding bet carries ≥1 DIRECT customer-demand indicator (leads, inbound conversations, replies, booked calls). Leading proxies (rank on a money keyword feeding a CTA page, citations, mentions) are allowed only ALONGSIDE a direct one — a bet whose only indicators can rise with zero customer contact is a FAIL.
- A recurring run is wired (queue entry with date, and/or a scheduled job registered + verified loaded) — **"we'll remember" is a FAIL**; queue-only wiring names its executor (an existing scheduled surface) or carries the owner's recorded "manual-fire risk" acceptance in `brief.md`. That acceptance is valid only when (a) the queue row is bound to a named, verified scheduled surface — paste the evidence: the scheduler's own listing of that job AND the grep of the checklist file the job actually reads — and (b) a missed first fire auto-escalates: register the stream with the recurring runner so the next scheduled run picks it up. Acceptance without that evidence is a FAIL.
- The wired cadence's first run date is ≤ the earliest founding-bet check date — or an interim dated grading entry exists.
- First grading date named and recorded in `brief.md`.
- No re-derived competitor sets or keyword seeds — P1.S5/P4.S1 artifacts cited.

**Gate out (mandatory — see SKILL.md house rules):**
1. Draft `P5-Activation.S4-PredictionCadence.md`.
2. Invoke `/critical` — attack the wiring hardest: are the indicator commands executable by someone who wasn't in this conversation, is the recurring run actually wired (queue entry dated / job verified loaded) or just noted, and vanity indicators — flag any founding indicator that can rise with zero customer contact.
3. Revise; note what changed.
4. Present to the owner. **Wait for their explicit approval. Never auto-advance.**

**Checkpoint:** "Prediction cadence live: [queue / scheduled job], next run [date], first grading [date]. P5-Activation phase complete — P6-Adoption next: GTM locks channels from the outreach + launch data."

**Next:** `stages/P6-Adoption.S1-GTM.md`
