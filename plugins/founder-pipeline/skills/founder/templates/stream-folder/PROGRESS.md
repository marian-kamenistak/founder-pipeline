# Pipeline progress — [stream slug]

**Current step:** [P<X>.S<Y>-Name]
**Last updated:** [date]
**Track:** [full pipeline / smoke test first]

> Single source of truth for pipeline state (business state lives in `brief.md` — never merge them). Filenames carry NO status; this file does. Statuses: `pending` → `in progress` → `awaiting approval` → `approved`; plus `skipped` (record why) and `killed` (kill gates only). Update the row at every transition, not at end of session. At most ONE step `in progress`/`awaiting approval` at a time, except the `∥` pairs sanctioned in SKILL.md.
>
> **25 steps across 6 phases** (7 + 4 + 1 + 6 + 4 + 3), listed below.
>
> **Conventions used by every step template in this folder.** Set these once at P1.S1 and they hold for the whole run:
> - `{currency}` — the stream's currency. Every money figure in every step file is written `{currency}[X]`; declare the actual currency in `brief.md` at P1.S1.
> - `<owner>` — the person who approves gates and owns queue rows. Named once in `brief.md` at P1.S1.
> - **House stack** — the tools this stream builds on (web framework + host, analytics, CRM, payments, email, automation). Declared once at P1.S1, referenced by P2.S2, P4.S2, P4.S3 and P4.S5. A build outside it needs a recorded override with a reason.
> - **Home market / export market** — the two territories the keyword, naming and indexation steps parameterise on. Declared once at P1.S1.

| Step | Name | Status | Updated | CRITICAL | Def-of-success | Note (one-line "so what") |
|---|---|---|---|---|---|---|
| P1.S1 | Init + portfolio trade | pending | | | | |
| P1.S2 | Problem | pending | | | | |
| P1.S3 | ICP + accounts.md | pending | | | | |
| P1.S4 | Prediction (hypothesis mode) | pending | | | | |
| P1.S5 | Competition | pending | | | | |
| P1.S6 | Offer | pending | | | | |
| P1.S7 | Name | pending | | | | |
| P2.S1 | Economics | pending | | | | |
| P2.S2 | Tooling ∥ | pending | | | | |
| P2.S3 | Pricing | pending | | | | |
| P2.S4 | Validation — PROFIT VERDICT | pending | | | | |
| P3.S1 | Outreach | pending | | | | |
| P4.S0 | Email (deliberate numbering exception — see stage file) | pending | | | | |
| P4.S1 | Keywords | pending | | | | |
| P4.S2 | Copy | pending | | | | |
| P4.S3 | Web | pending | | | | |
| P4.S4 | SourceGap (competitor teardown) | pending | | | | |
| P4.S5 | Deck | pending | | | | |
| P5.S1 | Launch | pending | | | | |
| P5.S2 | Links | pending | | | | |
| P5.S3 | Queues | pending | | | | |
| P5.S4 | PredictionCadence | pending | | | | |
| P6.S1 | GTM | pending | | | | |
| P6.S2 | KPIs | pending | | | | |
| P6.S3 | Execute (90-day plan) | pending | | | | |

## Rewind log

| Date | Step re-opened | Contradiction + evidence | Cascade re-checked (steps, result) |
|---|---|---|---|
| | | | |
