# Rubric — base rates, scoring, ensemble, probabilities, grading

## 1. Outside view first (mandatory, before any inside-view reasoning)

For each bet, find a **reference class** and its base rate before looking at the bet's specifics:
- "What % of niche B2B service categories 2× search demand within 24 months?"
- "What % of new consulting SKUs in this vertical reach 10 paying clients in year 1?"
- Sources: industry reports, the ledger's own history (from cycle 3 on), comparable search-trend curves for analogous terms 2-5 years older, and — where your home market historically lags a larger reference market for this category — that reference market's mature curve for the same term, with the observed lag noted (`data-sources.md`; the worked example there is a Europe-primary idea reading the US curve as its leading indicator).

Record: reference class, base rate `[source]`, and the anchor probability. The final probability (step 4 below) must state how far it moved from the anchor and why. No reference class findable → base rate = INSUFFICIENT DATA → confidence capped at Watch.

## 2. Four axes, multiplicative (a zero kills the bet — that's the point)

Score 0-5 per axis; final score = product. INSUFFICIENT DATA on an axis ≠ zero — it means the bet can't be fully scored: cap at Watch, emit a manual-verification item naming exactly what evidence would resolve it.

| Axis | 0 | 3 | 5 |
|------|---|---|---|
| **Demand evidence** | no volume anywhere, discourse only | volume OR trend slope OR AI-prompt presence, single silo | corroborated across ≥3 unrelated silos (search + jobs + papers/discourse), rising slope |
| **Competitive whitespace** | ≥3 players own the SERP/positioning/registry space | 1-2 present but beatable (validated live SERP + LLM-citation scan) | nobody credible covers it |
| **Founder-fit** | needs assets the owner doesn't have | adjacent to existing assets, some new build | direct reuse of existing assets (see the asset list the caller passed in, the run's `brief.md`, or ask) |
| **Channel runway** | the channel is hardened (SERP locked, AI Overview locked, event circuit saturated) | contestable within 6-12 months of work | space so new it's unformed — first-mover window |

Channel runway generalizes rank-runway: for search bets it's the SERP/AI-citation window; for event/community/marketplace bets it's speaker-slot/category-page availability — low search volume alone never kills a non-search bet. Where your home market lags a larger reference market, that reference market's mature trend for the same term counts as one corroborating silo toward Demand evidence (never the sole basis for a score) when paired with a lag rationale (`data-sources.md`).

## 3. Ensemble verdict

Dispatch **3 parallel fresh-context subagents**, each given the registry evidence + this rubric + ONE framing — (a) optimist: strongest honest case FOR, (b) skeptic: strongest honest case AGAINST, must engage the step-3D contrarian sources, (c) base-rate-anchored: outside view dominates. Each is blind to the others (independence is the point — sequential role-play in one context anchors and defeats it). The orchestrator takes the **median** per axis. Record all three passes — a >2-point spread on any axis is itself a finding (the evidence is ambiguous; say so).

**Survival**: a bet survives iff it clears the step-2 pre-registered cutoff (default: every axis ≥ 2 AND product ≥ 24 AND confidence ≥ Medium). Surviving bets get probabilities, money ranges, and execution-plan slots. Non-surviving bets split two ways: **DEAD** (any axis scored 0, or a pre-registered kill rule fired) — recorded in the report's Drop list with the killing evidence, no ledger row; **WATCH** (missed the cutoff on thin evidence / INSUFFICIENT DATA) — unscored ledger row with graduation criteria.

## 4. Probability + confidence

- **Probability**: one number per bet, 5% granularity (never "likely"), anchored on the base rate, adjusted with named reasons. This is what gets Brier-scored later.
- **Resolution check**: a ledger where every probability sits in 45-55% is safe but useless — hedging has no information value. If >half the bets land there, re-examine before shipping: either the evidence genuinely can't discriminate (say so) or the scoring is dodging commitment.
- **Confidence bands** (orthogonal to probability): **High** = ≥2 independent source *types* agree; **Medium** = one strong type, others silent; **Watch** = discourse only or any INSUFFICIENT DATA axis. Contradicting evidence anywhere → cap at Medium and state the contradiction. Watch items enter the ledger UNSCORED (no probability, no Brier — graduation criteria only) and get no execution-plan slot and no money block.

## 5. Grading (step 0 of the next run)

Per matured row: execute the recorded indicator call → outcome o ∈ {hit=1, miss=0, partial=0.5} against the pre-registered threshold → **Brier = (p − o)²**.
- Ledger header carries: rolling mean Brier, the naive base-rate forecaster's Brier on the same rows, and the delta. Beating 0.25 (coin flip) is trivial; **the test is beating the base rate**.
- From cycle 3: calibration buckets (55-65%, 65-75%, ...) — do 70% claims hit ~70%?
- A prediction may be revised mid-period with a timestamp; grade both initial and final (two Brier entries, marked).
- Backtest warning: never "validate" the rubric by retro-predicting past quarters — retrieval leaks future information into the research; backtests flatter.

## 6. Wild-card + cross-impact (per surviving bet)

- One sentence: "It's <close date> and this bet failed because ___" — plus one watchable indicator for that failure path.
- Cross-impact: name which other bets move together with this one. Correlated bets are ONE bet wearing two names — merge them or mark the correlation in both rows; a ledger of five correlated bets has one bet's worth of diversification.
