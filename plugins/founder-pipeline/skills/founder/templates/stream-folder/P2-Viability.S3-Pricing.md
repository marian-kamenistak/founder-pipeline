# Pricing & business model

**Stream:** [slug]
**Step:** P2.S3-Pricing (P2-Viability)
**Last updated:** [date]

---

## Hard rule

This stage **must** invoke `/founder-pipeline:pricing`. That skill runs the 10-criterion scorecard and won't ship below 95/100. If `/founder-pipeline:pricing` isn't available, fall back to an inline mini-scorecard — score the tier sheet against the 10 /founder-pipeline:pricing criteria by name — and flag this file `FALLBACK — /founder-pipeline:pricing unavailable, scorecard is inline approximation`. The FALLBACK flag is a downstream block: on flag creation add a `queues/manual-queue.md` row "Re-run /founder-pipeline:pricing on <stream>" (dated); P2.S4 verifies no open FALLBACK flag before the PROFIT VERDICT (or the owner's dated override recorded).

- [ ] `/founder-pipeline:pricing` skill invoked and scored ≥95/100
- [ ] Fallback: inline mini-scorecard used — file flagged `FALLBACK — /founder-pipeline:pricing unavailable, scorecard is inline approximation`
- [ ] Fallback only: `queues/manual-queue.md` row "Re-run /founder-pipeline:pricing on <stream>" added — dated [YYYY-MM-DD]

## Value metric

- **Unit of value:** [per seat / per call / per outcome / per quarter / per project]
- **Why this unit:** [tie to the offer's enabled value from P1.S6]
- **Scalability:** [does the unit scale with customer value, your cost, both, neither?]

## Business model

- [ ] Subscription (recurring, retention focus)
- [ ] One-time (transactional)
- [ ] Usage-based (aligns with value, hard to forecast)
- [ ] Hybrid (base + usage)
- [ ] Freemium (acquisition machine, conversion challenge)
- [ ] Enterprise (custom, high-touch, high ACV)
- [ ] Partner-share (% of partner's outcome)

**Picked:** [model]
**Why this model for this stream:** [...]

## Pricing table

| Tier | Value metric | Price | What's included | Key assumption → How to test |
|---|---|---|---|---|
| Starter / Sprint | [unit] | {currency}[X] | [list] | Assumption: [...]. Test: [...] |
| Standard | [unit] | {currency}[Y] | [list] | Assumption: [...]. Test: [...] |
| Plus / Premium | [unit] | {currency}[Z] | [list] | Assumption: [...]. Test: [...] |
| Annual / Enterprise | [unit] | {currency}[A] | [list] | Assumption: [...]. Test: [...] |

## Competitor anchor table

[An anchor without a live URL is deleted, not estimated.]

| Competitor | Price | Live pricing-page URL | Scrape date (this run) |
|---|---|---|---|
| | | | |

## Willingness-to-pay evidence

| Source | Method | Finding | Citation |
|---|---|---|---|
| ICP conversation #1 (accounts.md) | reservation-price ask | [number range] | [name, date] |
| ICP conversation #2 (accounts.md) | reservation-price ask | [number range] | [name, date] |
| ICP conversation #3 (accounts.md) | reservation-price ask | [number range] | [name, date] |
| price-anchoring (Van Westendorp only for low-ticket volume offers) (planned) | 4-question survey, n=10+ | [pending] | `[assumption — validation: run by date X]` |
| Closest alternative benchmark | desk research | {currency}[number] | `[source: ...]` |

## price-anchoring (Van Westendorp only for low-ticket volume offers) plan

- **By when:** [date]
- **n target:** [10+]
- **Channels to reach respondents:** [...]
- **Survey copy:** [4 questions: too cheap / cheap / expensive / too expensive]

## Anti-failure mode check

- [ ] Not Feature Shock — offer is focused, not bloated
- [ ] Not Minivation — price covers cost + sustains the stream
- [ ] Not Hidden Gem — pricing visible in GTM motion
- [ ] Not Undead — pricing aligned with evidenced demand (P1.S4 prediction data + ICP conversations)

---

## Honest-assessment note

This stage earns its keep always. Pricing is the highest-leverage decision in the whole stream.

## Checkpoint

- [ ] Launch hypothesis pricing locked (hypothesis, not decision — validation gate tests it)
- [ ] price-anchoring (Van Westendorp only for low-ticket volume offers) run by [date]
- [ ] Move to the validation gate (P2.S4)

## Validation loop

- [ ] `/founder-pipeline:critical` run — findings: [...] — **CRITICAL SCORE: [X]/10** — advisory; the gate is the def-of-success PASS/FAIL checklist
- [ ] Def-of-success (from the stage file): [each criterion — met/unmet]
- [ ] Improvement loops run (if gate failed): [N — what changed each round]
- [ ] Revised — what changed: [...]
- [ ] **Owner approved** — [date] [overrides, if any]
