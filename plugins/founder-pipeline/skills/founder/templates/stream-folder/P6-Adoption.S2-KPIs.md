# KPIs

**Stream:** [slug]
**Step:** P6.S2-KPIs (P6-Adoption)
**Last updated:** [date]

---

## North-star metric

**Metric:** [one number]

**Definition:** [precise — including window, denominator, exclusions]

**Why this:** [tied to revenue, not awareness; behavioral, not stated]

**Baseline (date):** [value @ YYYY-MM-DD — P5.S1 day-0 snapshot for rank/citation; a live read from your analytics tool, CRM, and payment processor for the rest]
**Target by month 6:** [number]
**Target by month 12:** [number]

## Leading indicators (3–5)

| # | Metric | Definition | Baseline (date) | Predicts north-star how | Vanity check (passes?) |
|---|---|---|---|---|---|
| 1 | [metric] | [...] | [value @ YYYY-MM-DD] | [50% move → ___ predicted in __ days] | [yes/no — drop if no] |
| 2 | [metric] | [...] | [value @ YYYY-MM-DD] | [...] | [yes/no] |
| 3 | [metric] | [...] | [value @ YYYY-MM-DD] | [...] | [yes/no] |
| 4 | [metric] | [...] | [value @ YYYY-MM-DD] | [...] | [yes/no] |
| 5 | [metric] | [...] | [value @ YYYY-MM-DD] | [...] | [yes/no] |

## Lagging indicators

| # | Metric | Definition | Baseline (date) | Target |
|---|---|---|---|---|
| 1 | Revenue (MRR / ARR / per-deal) | [...] | [value @ YYYY-MM-DD] | {currency}[X] by month [N] |
| 2 | Retention (renewal rate / churn) | [...] | [value @ YYYY-MM-DD] | [X]% by month [N] |
| 3 (optional) | CAC payback | [...] | [value @ YYYY-MM-DD] | [N] months |
| 4 (optional) | NPS | [...] | [value @ YYYY-MM-DD] | [score] |

## Vanity-check rejection list

[Metrics that came up but didn't pass the "if this moves and revenue doesn't, do I care?" test. Listed here as evidence of rigor — not tracked.]

- [metric]: rejected because [reason]
- [metric]: rejected because [reason]

## Instrumentation

| Tool | Events tracked | Owner | Date live |
|---|---|---|---|
| Product analytics | [page views, autocaptured clicks, custom events] | [owner] | [date] |
| Payment processor | [payment, refund, churn] | [owner] | [date] |
| CRM / task board | [pipeline stage transitions] | [owner] | [date] |
| Automation tool (if used) | [automation hooks] | [owner] | [date] |
| Rank / AI-citation read | [recurring read this step owns — same source as the P5.S1 day-0 baseline, which lives in P5.S1's folder] | [owner] | [date] |

If your analytics tool is PostHog, its own plugin is an **optional dependency you install separately**; once installed it covers this step's setup work:
- `/posthog:instrument-product-analytics` — for event setup
- `/posthog:instrument-integration` — for SDK install
- `/posthog:managing-subscriptions` — for weekly digest delivery
- `/posthog:querying-posthog-data` — for ad-hoc KPI pulls

Without it, do the same four things by hand: define the event schema before writing any code, install the SDK on every page, schedule one recurring digest to a place you actually read, and keep the KPI queries in a file in this stream folder so the numbers are reproducible.

---

## Honest-assessment note

This stage earns its keep always. The vanity-check column is the difference between a dashboard that gets used and one that gets ignored.

## Checkpoint

- [ ] North-star locked
- [ ] Leading indicators (3–5) selected, all pass vanity check
- [ ] Lagging indicators defined
- [ ] Instrumentation plan in place
- [ ] Execute plan (P6.S3) next

## Validation loop

- [ ] `/critical` run — findings: [...] — **CRITICAL SCORE: [X]/10** — advisory; the gate is the def-of-success PASS/FAIL checklist
- [ ] Def-of-success (from the stage file): [each criterion — met/unmet]
- [ ] Improvement loops run (if gate failed): [N — what changed each round]
- [ ] Revised — what changed: [...]
- [ ] **Owner approved** — [date] [overrides, if any]
