# P2.S4 — Viability confirmation + validation gate → `P2-Viability.S4-Validation.md`

**Phase: P2-Viability** (closes the phase)

**Routing:** plain (two kill-passes as parallel subagents, opposing framings) · kill passes PEAK · gate critic PEAK

**Earns its keep** always. This stage answers ONE question with evidence: **will this stream generate profit?** It is the difference between streams that ship and streams that die in a planning doc. Nothing downstream (content, web, marketing, client outreach at scale) runs until this stage produces a defensible YES or a provisional-yes with named experiments.

**Part A — profit verdict.** Reconcile `P2-Viability.S3-Pricing.md` × `P2-Viability.S1-Economics.md`:
1. At the locked pricing and the P2.S1 cost base, how many paying clients does break-even need — and does that number fit the delivery capacity? CITE `P1-Ideation.S6-Offer.md`'s capacity block + `P2-Viability.S1-Economics.md`'s hour budget — don't recompute either.
2. 12-month profit at forecast / at 50% / at 25% — the scenarios and profit-per-founder-hour are CITED from `P2-Viability.S1-Economics.md`, never recomputed here. If 50% of forecast is a loss, say so in bold.
3. Verdict line at the top of `P2-Viability.S4-Validation.md`: `PROFIT VERDICT: [CLEARS THE BAR at N clients by month M] / [clears only if assumptions X,Y hold — experiments named] / [PROFITABLE BUT MEDIOCRE — KILL] / [not viable — KILL]`. The bar = P1.S1 profit bar: ≥ 1.5× hurdle rate per founder-hour at the 50% scenario AND ≥ the absolute floor. **Mediocre is an explicit kill verdict, not a "keep it small" option** — a surviving mediocre stream eats the focus that a better stream needs.

**Part B — Impact × Uncertainty 2×2** on every key assumption surfaced across all prior stages:
1. List every `[assumption — validation: ...]` tag written so far — dispatch a subagent to grep every P1/P2 stream file for `[assumption` tags and return the full list with counts per file; the 2×2 must account for every tag. Group into a 2×2:
   - X-axis: Uncertainty (low → high)
   - Y-axis: Impact if wrong (low → high)
   - Top-right quadrant (high impact + high uncertainty) = the validation backlog
2. For each top-right assumption, design a validation experiment:
   - **Method**: how you'll test (5 paid pilots / 10 Van Westendorp surveys / LOI signatures / smoke landing page). Method must be a real-world evidence type — named humans, money moved, signatures, or live traffic; internal analysis is not a validation method.
   - **Metric**: what number measures success
   - **Threshold**: what value = green light, what value = red
   - **Timeline**: by when
   - **Kill or go**: what evidence kills the stream vs greenlights public launch
3. Pre-mortem — 3 ways this stream dies in year one. Be uncomfortable. Include the P1.S1 portfolio trade (sacrificed stream drops more than this one produces = kill evidence).
4. **Pivot discipline** — evidence from randomised controlled trials of scientific decision-making in entrepreneurship (Camuffo et al.; pooled across the RCT programme, n ≈ 759 firms): the winning pattern is ONE or TWO focused pivots; zero pivots (attachment) and 3+ pivots (thrashing) both correlate with worse outcomes. Pre-commit: what single most-likely pivot would the evidence trigger, and what evidence triggers it?
5. Kill criteria — what evidence at month 3 / month 6 / month 12 shuts this down. Pre-commit.
6. Minimum evidence required for build + launch — N signed LOIs / paid pilots / pre-sales / waitlist of K. Be specific. This is the minimum-evidence record, not a pre-sale gate: the build does not wait on it.

**Skills:** `/brainstorm` for kill criteria. **Run a split test only if** the validation gate IS a testable hypothesis on an existing landing page or pricing surface with enough live traffic to reach significance — in that case specify variant, primary metric, minimum detectable effect, required sample size and run length *before* the test ships, and treat an underpowered test as no evidence. (A dedicated A/B-test-setup skill would do that arithmetic for you; none ships with this plugin — do it inline, or install one separately.) Otherwise the gate is LOIs / pre-sales / paid pilots, not a statistical test.

**Write to** `P2-Viability.S4-Validation.md`. Profit verdict at top, 2×2 in markdown table form, validation experiment table, pre-mortem narrative, single most-likely pivot + triggering evidence, kill criteria, minimum-evidence gate.

**Def-of-success — ALL must pass before owner sign-off (fail → improvement loop per SKILL.md, never advance):**
- TWO independent `/critical` passes run — profit-refutation and focus-refutation framings (per SKILL.md) — each recorded with its own PASS/FAIL and findings; both must pass. Scores are advisory (target ≥ 8/10) — the gate is the PASS/FAIL criteria below, not the numbers. These are the most important critical passes in the pipeline; do not soften them.
- **PROFIT VERDICT is "CLEARS THE BAR"** — ≥ 1.5× hurdle rate per founder-hour at the 50% scenario AND ≥ the absolute floor, restated (cited, not recomputed) from `P2-Viability.S1-Economics.md` × `P2-Viability.S3-Pricing.md`. "Profitable but mediocre" = kill; no downstream phase (build/marketing/outreach) runs on a mediocre verdict.
- Unit economics floor: LTV:CAC ≥ 3 and payback ≤ 12 months (justify explicitly if either is off). CAC and LTV inputs tagged `[source]` or `[assumption — validation]`; any justified off-floor exception becomes a row in the validation experiment table with its own threshold and date — a justification without an experiment row is a FAIL.
- Every top-right 2×2 assumption has an experiment with method, metric, threshold, and date; the method is a real-world evidence type — named humans, money moved, signatures, or live traffic; internal analysis is not a validation method.
- Pivot pre-commitment recorded: one named pivot, one named evidence trigger.
- Kill criteria pre-committed for months 3 / 6 / 12; minimum-evidence gate specific (N LOIs / pilots / pre-sales).

**Gate out (mandatory — see SKILL.md house rules):**
1. Verify `P2-Viability.S3-Pricing.md` carries no open `FALLBACK` flag before issuing the PROFIT VERDICT — an open flag blocks the verdict until the pricing skill re-runs or the owner's dated override is recorded.
2. Draft `P2-Viability.S4-Validation.md`.
3. Run TWO independent `/critical` passes on the draft — profit-refutation and focus-refutation framings (per SKILL.md) — each recorded with its own PASS/FAIL and findings; both must pass. These are the most important critical passes in the whole pipeline: attack the profit verdict, the pre-mortem's honesty, and whether the kill criteria have teeth or are theater.
4. Revise; note what changed.
5. Present the draft + the critical findings + the changes to the owner. **Wait for their explicit approval. Never auto-advance.**

**Checkpoint:** "PROFIT VERDICT: [X]. Validation backlog: [N experiments]. Pre-commit kill criteria: [Y]. Min evidence to build/launch: [Z]. P2-Viability phase complete — proceed to P3-Clients (P3.S1 outreach opens immediately), or run the validation experiments first?"

**Next:** `stages/P3-Clients.S1-Outreach.md`
