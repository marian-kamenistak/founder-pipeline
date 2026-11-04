# P2.S3 — Pricing & business model → `P2-Viability.S3-Pricing.md`

**Phase: P2-Viability**

**Earns its keep** always. Pricing is the highest-leverage decision in the whole stream.

**Hard rule — execution order is load-bearing. Do these in sequence, do not improvise:**

1. **FIRST, invoke `/pricing` immediately.** Don't ask any P2.S3 questions yet. Pass it the existing pain/demand context so it skips its own Step 1 discovery:
   > "Pricing the [name] offer. The job/pain context is already captured in `<parent>/<slug>/P1-Ideation.S2-Problem.md` (cited pains) + `P1-Ideation.S4-Prediction.md` (discourse evidence). Read them and treat Step 1 as satisfied — go straight to Step 2 (alternatives & value anchors). Also load `P1-Ideation.S6-Offer.md` for the offer spec and `P1-Ideation.S5-Competition.md` for alternative pricing anchors."

   `/pricing` will run its 7-step flow with the 10-criterion scorecard. It won't return "ready" below 95/100.

2. **THEN, capture business-model context** that the pricing skill doesn't cover. One question at a time:
   - **Business model shape** — subscription / one-time / usage / hybrid / freemium / enterprise / partner-share. Pick the model AND state why this ICP buys this way.
   - **Validation plan** — beyond the pricing scorecard, what's the live WTP test? **Default for high-ticket B2B services: direct price anchoring** — state the REAL price in 10+ live discovery/pre-sale conversations and count reactions (buying question / negotiation / silence / walk-away). Surveys measure price perception, not purchase intent; Van Westendorp is explicitly criticized for high-ticket B2B and is only the fallback for lower-ticket, higher-volume offers. Pre-sales / paid pilots remain the actual gate.

3. **THEN, write `P2-Viability.S3-Pricing.md`.** All money cells use the currency declared at P1.S1 (`{currency}` below). Structure:
   - **Pricing-skill output** — the filled-in template from `/pricing`'s "What good pricing looks like" block, including the explicit `SCORE: __/100  ✅ Ship` line.
   - **Business model + rationale** — from question above.
   - **Tier table with validation column:**

     | Tier | Value metric | Price | What's included | Key assumption → How to test |
     |---|---|---|---|---|

     Example row: `| Standard | Per quarter | {currency}4,900 | X, Y, Z | Assumption: the buyer role will pay {currency}4,900/quarter for KPI-guaranteed performance coaching. Test: 5 paid pilots next quarter at this price; if >2 reject on price, run Van Westendorp on the next 10 prospects. |`
   - **Competitor anchor table** — each anchor = competitor, price, live pricing-page URL, scrape date (this run). An anchor without a URL is deleted, not estimated.
   - **Price-anchoring plan** — 10+ named prospects from `accounts.md` (the P1.S3 canonical list — never a new list), the exact price sentence to be said out loud, what counts as accept/reject signal, threshold for kill/pivot. (Van Westendorp only if the offer is low-ticket/volume — note why.)

**If `/pricing` is unavailable** (skill not installed): fall back to an inline mini-scorecard — score the tier sheet against the 10 pricing criteria by name — and flag the file `FALLBACK — pricing skill unavailable, scorecard is inline approximation`. Re-run with the skill before public launch. Don't skip the stage. The FALLBACK flag is a downstream block — on flag creation add a `queues/manual-queue.md` row "Re-run pricing on <stream>" (dated), and P2.S4's gate-out MUST verify no FALLBACK flag is present before the PROFIT VERDICT (or the owner's dated override recorded).

**Def-of-success — ALL must pass before owner sign-off (fail → improvement loop per SKILL.md, never advance):**
- Pricing scorecard **≥ 95/100** (existing hard gate — the skill won't return "ready" below it); fallback runs carry the queue row + flag (`queues/manual-queue.md` "Re-run pricing on <stream>" dated + the `FALLBACK` file flag) — a fallback without both is a FAIL.
- `/critical` run recorded on the price-ceiling assumption and model choice; the score is advisory (target ≥ 8/10) — the gate is the PASS/FAIL criteria below, not the number.
- Price floor sanity: each tier's price ≥ 3× its unit delivery cost (cite `P1-Ideation.S6-Offer.md`'s delivery-capacity block) — value-based pricing dies below that.
- **RoI price floor (hard gate): each tier's price ≥ unit delivery cost + (P1.S1 bar rate × founder-hours consumed per unit).** The marginal client must clear the founder-hour bar at list price — a price below this floor makes every sale a donation of founder time, and no volume fixes it.
- **Full-cost margin floor (hard gate): each tier's price ≥ 1.2 × (unit cash costs + ALL expert time priced — founder hours at ≥ the P1.S1 bar rate, contractor/concierge hours at their market rate).** The business must be profitable AFTER paying everyone, founders included, with ≥20% margin on the fully-loaded cost. **Package discounts may never drop a tier below this floor** — a discount that violates the margin dies, not the margin. Show the computation per tier: `1.2 × (cash + Σ hours × rates) = floor vs price, margin %`.
- **Floor inputs cited:** in every floor computation above, unit cash costs and hours×rates must be cited line-items from `P2-Viability.S1-Economics.md` — a floor computation without a P2.S1 citation is a FAIL of this criterion.
- Competitor anchor table required: each anchor = competitor, price, live pricing-page URL, scrape date (this run). An anchor without a URL is deleted, not estimated.
- Every tier has a key assumption + a named test with a threshold.
- WTP test is intent-based, not perception-based: real price anchored in 10+ live conversations with named prospects from `accounts.md`, timeline, kill/pivot threshold. (A survey-only plan fails this criterion for high-ticket services.)

**Gate out (mandatory — see SKILL.md house rules):**
1. Draft `P2-Viability.S3-Pricing.md` (only AFTER the pricing scorecard reaches ≥95/100).
2. Invoke `/critical` on the draft — adversarial pass on the price-ceiling assumption and the business-model choice: what evidence says this ICP buys this way at this number?
3. Revise; note what changed.
4. Present the draft + the pricing score + the critical findings to the owner. **Wait for their explicit approval. Never auto-advance.**

**Checkpoint:** "Pricing locked: [tier table]. Pricing scorecard: [X/100]. Business model: [Y]. WTP validation plan: [Z]. This is a launch hypothesis — the Viability gate next tests whether the whole stream clears profit."

**Next:** `stages/P2-Viability.S4-Validation.md`
