# Viability confirmation + validation gate

**PROFIT VERDICT:** [CLEARS THE BAR at N clients by month M / clears only if assumptions X,Y hold / PROFITABLE BUT MEDIOCRE — KILL / not viable — KILL]  (bar: ≥ 1.5× hurdle rate per founder-hour at 50% scenario AND ≥ absolute floor, from brief.md P1.S1)

**Stream:** [slug]
**Step:** P2.S4-Validation (P2-Viability)
**Last updated:** [date]

---

## Assumptions inventory (Impact × Uncertainty 2×2)

[Full list from a subagent grep of every P1/P2 stream file for `[assumption` tags, with counts per file — the 2×2 must account for every tag. Score each.]

| # | Assumption | Source step | Impact (1–5) | Uncertainty (1–5) | Quadrant |
|---|---|---|---|---|---|
| 1 | [...] | P1.S2 | [X] | [X] | [TR/TL/BR/BL] |
| 2 | [...] | P1.S3 | [X] | [X] | [...] |
| 3 | [...] | P1.S4 | [X] | [X] | [...] |
| 4 | [...] | P1.S6 | [X] | [X] | [...] |
| 5 | [...] | P2.S1 | [X] | [X] | [...] |
| ... | | | | | |

**Top-right quadrant (high impact + high uncertainty) = validation backlog.**

## Validation experiments

[For each top-right assumption, design a binary-outcome experiment.]

### Experiment 1: [assumption]
- **Method:** [LOI / paid pilot / Van Westendorp / smoke landing page / sales meeting — real-world evidence only: named humans, money moved, signatures, or live traffic; internal analysis is not a validation method]
- **Metric:** [what number measures success]
- **Threshold (green):** [value → execute]
- **Threshold (red):** [value → kill or redesign]
- **Timeline:** by [date]
- **Owner:** [name]
- **Status:** [planned / in-flight / resolved]

### Experiment 2: [assumption]
- **Method:**
- **Metric:**
- **Threshold (green):**
- **Threshold (red):**
- **Timeline:**
- **Owner:**
- **Status:**

### Experiment 3: [assumption]
- **Method:**
- **Metric:**
- **Threshold (green):**
- **Threshold (red):**
- **Timeline:**
- **Owner:**
- **Status:**

## Pre-mortem: 3 ways this stream DIES in year one

[Uncomfortable framing required.]

### Death scenario 1
- **What kills it:** [...]
- **Probability:** [low / medium / high]
- **Early warning signal:** [what would you see at month 2 if this was happening?]
- **Mitigation:** [what to do if you see the signal]

### Death scenario 2
- **What kills it:** [...]
- **Probability:** [low / medium / high]
- **Early warning signal:** [...]
- **Mitigation:** [...]

### Death scenario 3
- **What kills it:** [...]
- **Probability:** [low / medium / high]
- **Early warning signal:** [...]
- **Mitigation:** [...]

## Pivot pre-commitment

- **Single most-likely pivot:** [one named pivot]
- **Evidence trigger:** [the named evidence that triggers it]

## Kill criteria (pre-committed)

[Set NOW. Re-reading these at month 6 with the urge to "give it more time" is non-negotiable.]

| Gate | Minimum required | If missed |
|---|---|---|
| Month 3 | [N paying + {currency}X cumulative] | Kill / redesign / extend by N weeks |
| Month 6 | [N paying + {currency}X cumulative] | Kill / redesign / extend |
| Month 12 | [N paying + {currency}X cumulative] | Kill / pivot / continue |

## Minimum evidence to greenlight execute (P6.S3)

[Cannot proceed to the P6.S3 synthesis + 90-day execute plan without this gate's evidence.]

- [ ] At least [N] signed LOIs at {currency}[X] each, OR
- [ ] At least [N] paid pilots delivered at {currency}[Y], OR
- [ ] Pre-sales of {currency}[Z] cumulative, OR
- [ ] Waitlist of [K] qualified ICP members willing to pay

**Date this evidence must exist by:** [date]

---

## Honest-assessment note

This stage earns its keep always. This is the gate that separates streams that ship from streams that die in a planning doc.

## Checkpoint

- [ ] Assumptions inventoried + plotted
- [ ] Validation experiments designed (binary outcomes)
- [ ] Pre-mortem written (uncomfortable)
- [ ] Pivot pre-commitment recorded (one named pivot, one named evidence trigger)
- [ ] Kill criteria pre-committed
- [ ] Minimum evidence gate set
- [ ] TWO `/critical` passes run (profit-refutation + focus-refutation)
- [ ] Ready to synthesize brief

## Validation loop

- [ ] `/critical` profit-refutation pass — PASS/FAIL: [...] — findings: [...] — **CRITICAL SCORE: [X]/10** — advisory; the gate is the def-of-success PASS/FAIL checklist
- [ ] `/critical` focus-refutation pass — PASS/FAIL: [...] — findings: [...] — **CRITICAL SCORE: [X]/10** — advisory; both passes must pass
- [ ] Def-of-success (from the stage file): [each criterion — met/unmet]
- [ ] Improvement loops run (if gate failed): [N — what changed each round]
- [ ] Revised — what changed: [...]
- [ ] **Owner approved** — [date] [overrides, if any]
