# P2.S1 — Economics: time + money in one model → `P2-Viability.S1-Economics.md`

**Phase: P2-Viability**

**Earns its keep** always. Hours and money are one model — profit per founder-hour is the number the whole pipeline gates on, and it needs both sides in one place. This step prices the stream in hours AND in money before P2.S3–S4 stress-test it. (P2.S2 tooling may draft in parallel; its costs feed back into this model before this gate closes.)

**Currency:** every money cell in this file uses the stream's currency, declared once at P1.S1 and recorded in `brief.md`. This file writes `{currency}` wherever the symbol goes; substitute the declared one. Mixed-currency inputs (a tool priced in USD, a client paying in EUR) are converted at a stated rate with the rate cited in the cell.

**Part A — time budget (hard numbers):**
1. Re-open the P1.S1 portfolio trade — which stream gives up hours, how many per week. Still true now that the offer is concrete?
2. Weekly hours this stream gets: design/build vs delivery vs marketing. Three numbers, verified against the founder's actual calendar (a calendar scan, or the P1.S1 portfolio-trade hours cited as the source); an unsourced self-reported hour budget fails the tagging criterion.
3. Capacity check — cite the delivery-capacity block from `P1-Ideation.S6-Offer.md` (hours/client/month × realistic client count): does it fit the weekly budget? If not, what gives?

**Part B — roadmap.** Ship (1 friendly customer end-to-end) / Pilot (paid cohort, no public marketing) / Public (full marketing) / Scale. Table: Phase | Milestone | Owner | Due | Done-when. Every milestone a named owner + binary done criterion.

**Part C — money:**
4. Upfront cost to launch (Ship + Pilot) and run-rate per month — itemized (tooling rows arrive from P2.S2).
5. 12-month revenue forecast + unit economics (CAC, LTV, gross margin, payback) — every number `[source: ...]` or `[assumption — validation: ...]`. First pass; P2.S3–S4 stress-test it against pricing. Where the P1.S4 money model produced a range, cite it as the forecast's starting envelope.
6. **Scenarios + the bar (this step OWNS both — P2.S4 cites them):** 100% / 50% / 25% scenario table — the base is defined, not vibed: 100/50/25% of forecast client volume at the cited P1.S4 price envelope; break-even month + unit volume; **profit per founder-hour** at 100% and 50% (12-month profit ÷ total founder-hours from Part A), placed next to the P1.S1 hurdle rate and absolute floor. The verdict block carries one mandatory row naming the single assumption that carries the forecast.

**Where the model lives:** a spreadsheet, so the scenarios recalculate instead of being retyped. Degradation ladder: a connected spreadsheet tool (via its MCP connector, if you have one) → a file in whatever cloud drive you use → markdown-only tables in this file plus a flag saying the scenarios are hand-computed. The md file always carries the verdict numbers and a link to wherever the live model sits.

**Skills:** `/founder-pipeline:plan` for milestone sequencing.

**Write to** `P2-Viability.S1-Economics.md`. Time-budget block + roadmap table + money tables (upfront / run-rate / forecast / unit economics / scenarios), every cell sourced or flagged; profit-per-founder-hour verdict block at the top.

**Def-of-success — ALL must pass before owner sign-off (fail → improvement loop per SKILL.md, never advance):**
- `/founder-pipeline:critical` run recorded; the score is advisory — the gate is the criteria below.
- **Zero negative slack:** summed milestone effort per week ≤ the stated weekly budget. **Not everything on the owner:** overflow is carried by a named person, tool, or automation — "the owner works more" is not a resource plan.
- Delivery capacity (from P1.S6) fits inside delivery hours; Ship/Pilot/Public/Scale all dated, every milestone owned with a binary done criterion.
- **Positive RoI:** 12-month profit > 0 at 100%, AND the 50% scenario at worst break-even-adjacent with a named floor decision.
- **Profit bar (from P1.S1):** profit per founder-hour at the 50% scenario ≥ 1.5× the hurdle rate AND 12-month profit ≥ the absolute floor. Below either bar, say it NOW in bold — don't let P2.S4 be the first place mediocrity is named.
- 100% of numbers tagged; break-even inside the P1.S1 horizon; gross margin ≥ 50% for productized service/consulting (justify explicitly if lower).
- Every cost row cites a live price-page URL or written quote, OR carries an explicit `[assumption — validation: <check>]` tag — bounded: assumption-tagged cost rows ≤ 20% of total monthly cost (in the declared currency) and never the top-3 rows by amount; each carries a due-by check date — real quotes are the rule, the tag is the bounded exception. P2.S2 tooling rows imported before this gate closes.

**Gate out (mandatory — see SKILL.md house rules):**
1. Draft `P2-Viability.S1-Economics.md`.
2. Invoke `/founder-pipeline:critical` — attack both halves: does the milestone list fit the hour budget or is this a 60-hour week in a 10-hour costume? And every number: where did it come from, which single assumption carries the forecast?
3. Revise; note what changed.
4. Present to the owner. **Wait for their explicit approval. Never auto-advance.**

**Checkpoint:** "Weekly budget [X]h, roadmap locked. Break-even month [Y], profit/founder-hour at 50% = [Z] vs hurdle [H]. Tooling gate next (parallel draft may already be open) — then pricing."

**Next:** `stages/P2-Viability.S2-Tooling.md` (∥ — may already be drafted; close its gate, then `stages/P2-Viability.S3-Pricing.md`)
