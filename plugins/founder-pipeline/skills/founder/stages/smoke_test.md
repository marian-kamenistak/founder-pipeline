# Smoke-test track (48h to send, 7-day read) → `smoke.md`

For "should I even build X?" hunches. The full pipeline costs days of thinking — it must be earned by signal, not enthusiasm. This track produces a go/no-go from 10 real outreaches sent inside 48h and read at 7 days, with 5 questions up front.

It is self-contained: nothing here depends on a prior step of the pipeline having run. Everything is written into the **stream folder** — one directory per idea, named after the idea, holding `smoke.md`, `accounts.md`, and the `queues/` folder.

**Day 1 — answer 5 questions** (one at a time, write to a single `smoke.md` in the stream folder):
1. Customer pain in one sentence — no jargon.
2. Primary ICP guess — one segment, one buyer role, one geography.
3. Offer in one sentence — what they get, what it roughly costs.
4. 10 named accounts that match the ICP — read `accounts.md` in the stream folder if P1.S3 already produced it; else collect them now and WRITE them to `accounts.md` (it's the canonical list either way). Real companies, real names. Can't name 10? That's the first signal. For each account, note in one line who the buyer role is, why this company plausibly has the pain, and the reachable route in (a person, a form, a mutual connection) — a name with no route in is not an account.
5. The outreach message — 3 sentences max, `/founder-pipeline:brand-voice` mandatory, asks for a 20-minute problem conversation (not a pitch). `P3-Clients.S1-Outreach.md` owns the outreach message across the pipeline; if you have already run P3.S1, reuse its template verbatim. If you have not, write the message here to that shape and P3.S1 adopts it later.

**Day 1–2 — send all 10.** Real sends, not drafts. LinkedIn DM, email, or warm intro — whatever reaches that ICP fastest. Log every send in a send-log table in `smoke.md` — one row per account: datetime, channel, recipient handle/URL — filled at send time, not reconstructed later. A row without that evidence counts as a draft. **Upon the 10th send:** append a dated day-7 read item to `queues/manual-queue.md` (per SKILL.md's queue rule — create `queues/` from `${CLAUDE_PLUGIN_ROOT}/skills/founder/templates/stream-folder/queues/` on first use), read date computed from the first send's logged timestamp. Outcome recording is blocked until that row exists — a 7-day read nobody scheduled never happens.

**"Conversation booked" =** a calendar entry with date and attendee recorded in `smoke.md`. A verbal "sure, sometime next week" is interest, not a booking — unrecorded bookings don't count toward the 3+ threshold.

**Decision rule (pre-committed, written in `smoke.md` before sending):**
- **3+ conversations booked within 7 days** → signal. Enter the full pipeline at P1.S2, carrying `smoke.md` as evidence.
- **1–2 booked** → weak signal. Rework the pain statement or ICP (once), re-run with 10 fresh accounts.
- **0 booked** → no-go. Park the idea, write one paragraph on why it died. Do not enter the full pipeline "anyway."

**Skills:** `/founder-pipeline:brand-voice` (outreach message, mandatory), `/founder-pipeline:brainstorm` (message angle). Account profiling is inline: for each of the 10, pull the company's own site and public profile pages, and record size, sector, the named buyer role, the evidence they have the pain, and the route in. *(If you have a dedicated enrichment skill installed, use it — none ships in this plugin.)*

**Def-of-success — ALL must pass before owner sign-off (fail → improvement loop per SKILL.md, never advance):**
- `/founder-pipeline:critical` run recorded on `smoke.md` BEFORE any send; the score is advisory (target ≥ 8/10) — the gate is the PASS/FAIL criteria below, not the number.
- 10/10 named accounts are real and reachable; pain statement ≤ 25 words.
- Decision rule written and pre-committed BEFORE the first send.
- 10 real sends within 48h — drafts don't count.
- `smoke.md` contains a send-log table (one row per account: datetime, channel, recipient handle/URL) filled at send time; any row without that evidence counts as a draft and fails the gate.
- Day-7 read item exists in `queues/manual-queue.md`, appended upon the 10th send, read date computed from the first send's logged timestamp — outcome recording is blocked until it does.
- Every conversation counted toward the 3+ threshold has a calendar entry with date and attendee recorded in `smoke.md` — unrecorded bookings don't count.
- Outcome recorded against the pre-committed rule; a "no-go anyway we continue" is an automatic fail.

**Validation loop:** before sending, invoke `/founder-pipeline:critical` on `smoke.md` — is the pain statement sharp, are the 10 accounts real, would the message get answered? The owner approves the message and the list before anything is sent (real outreach is outward-facing — never send without explicit approval).

The smoke test replaces nothing — it gates. Every stage of the full pipeline still runs if the signal is there.
