# Queues — stand up the execution queues

**Stream:** [slug]
**Step:** P5.S3-Queues (P5-Activation)
**Last updated:** [date]

> Sweeps P3.S1 through P5.S2 for every "awaiting / pending / blocked / the owner must / handed to" item and lands each in exactly one queue. "Drafted, awaiting the owner" is an OPEN queue item, not a done state.

---

## Queue status

| Queue | Path | Rows | Oldest open | Highest-value next |
|---|---|---|---|---|
| manual-queue | `queues/manual-queue.md` | [N] | [date] | [...] |
| backlink-queue | `queues/backlink-queue.md` | [N] | [date] | [...] |
| media-queue | `queues/media-queue.md` | [N] | [date] | [...] |

## Sweep log

One row per step, P3.S1 through P5.S2 — a 0-hit row still lists the files checked (no empty files-checked cell).

| Step | Files checked (step file, output folder, STATE/build logs) | Hits | Routed to |
|---|---|---|---|
| P3.S1-Outreach | | | |
| P4.S1-Keywords | | | |
| P4.S2-Copy | | | |
| P4.S3-Web | | | |
| P4.S4-SourceGap | | | |
| P4.S5-Deck | | | |
| P5.S1-Launch | | | |
| P5.S2-Links | | | |

## Hygiene contract

- [ ] Every row in all three queues carries four fields: `added: YYYY-MM-DD | owner | status | artifact/evidence path` (manual-queue rows additionally: `- [ ] added YYYY-MM-DD | action (est. min) | ready artifact: <path> | unblocks: <outcome>`)
- [ ] No duplicate items across queues (single-owner rule)
- [ ] backlink-queue holds only not-yet-adopted candidates (graduated items live in the /founder-pipeline:web-backlinks playbook)
- [ ] ≥14-day-old items flagged for do / delegate / kill

---

## Honest-assessment note

- [ ] Earns its keep — open owner-actions exist across P3-P5
- [ ] Performative — zero open items after sweep (rare): skip recorded in brief.md + PROGRESS.md

## Checkpoint

- [ ] Three queues standing, sweep complete, counts above verified
- [ ] PredictionCadence (P5.S4) next — may draft in parallel (∥)

## Validation loop

- [ ] `/founder-pipeline:critical` run — findings: [...] — **CRITICAL SCORE: [X]/10** — advisory; the gate is the def-of-success PASS/FAIL checklist
- [ ] Def-of-success (from the stage file): [each criterion — met/unmet]
- [ ] Improvement loops run (if gate failed): [N — what changed each round]
- [ ] Revised — what changed: [...]
- [ ] **Owner approved** — [date] [overrides, if any]
