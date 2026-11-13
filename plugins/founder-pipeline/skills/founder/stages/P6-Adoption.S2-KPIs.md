# P6.S2 — KPIs → `P6-Adoption.S2-KPIs.md`

**Phase: P6-Adoption**

**Routing:** plain (may run ∥ with P6.S1) · draft MID, stage judge MID · gate critic at the step tier

**Earns its keep** always.

**Hard rule:** One north-star **behavioral** metric tied to revenue. Plus 3–5 leading indicators + 2 lagging. **Vanity metrics rejected** — every metric scored against the "would someone change behavior based on this?" test. If no, it's vanity.

**Ask one at a time:**
1. North-star metric — what one number, if it moves, signals the stream is working? Tied to revenue.
2. Leading indicators (3–5) — what predicts the north-star moving? Tie them to the P3.S1 conversion path and read them **per segment × wave**: CRM stage-conversion rates (contacted→replied→call→signal) and product-analytics interaction events (teaser visits, quiz completions, bookings by UTM). A metric that can't be split by segment/wave can't tell you WHICH outreach works.
3. Lagging indicators — revenue, retention, CAC payback, NPS.
4. Vanity check — for each metric, "if this goes up but revenue doesn't, do I care?" If yes, drop it.
5. Instrumentation — the plan CITES P4.S3's analytics wiring (`P4-Build.S3-Web.md`): the events are already instrumented; this step defines the metrics read from them, never re-instruments. Beyond that, name the source system for every remaining metric — payments/billing for revenue, the CRM for pipeline stages, whatever automation layer carries the webhooks, and the search console for organic. The P1.S1 house stack is the worked example (PostHog for product analytics, Stripe for payments, Attio for CRM, a webhook automation tool); any equivalent works as long as the metric names a real, readable source.
   If a web asset shipped: the search console tracks the `P4-Build.S1-Keywords.md` primary keywords (impressions, position) as leading indicators.

**Skills:** the PostHog plugin's `/posthog:instrument-product-analytics` ONLY for genuinely new events not wired at P4.S3, and `/posthog:managing-subscriptions` for weekly digest delivery — **an optional dependency you install separately**; skip both if your analytics stack is something else and do the equivalent in that tool. For the recurring rank read, a rank API's `ranked_keywords` (own domain) plus a competitor `domain_intersection` call (vs the P1.S5 competitors) is the automatable rank leading-indicator — the recurring reads are OWNED here, and P5.S1's day-0 snapshot is the baseline they compare against. `references/dataforseo-playbook.md` Jobs 4/6 give the DataForSEO version; DataForSEO is a paid third-party API and an optional dependency. The search console stays the owned-impressions complement.

**The CITATION half of that read is an AI-visibility probe, not a rank API.** P5.S1 item 5 takes an AI-mention probe as part of the day-0 baseline, and this step declares itself owner of the recurring reads — but rank tooling cannot re-read a citation, so without this the AI-visibility loop opens at launch and never closes: everything P4.S3 spent on `/ai-seo` and `/ai-seo-llms-builder` (gated at Structure ≥7 / Citability ≥7) is never checked against whether an engine actually cites the site. Register the domain with whatever recurring AI-visibility measurement you run — a scheduled multi-engine probe (ChatGPT / Perplexity / AI Overviews) on a bi-weekly cadence is the shape to aim for — and let it be the automated read behind any citation or AI-visibility metric on the table. *(A dedicated recurring AI-visibility skill does not ship in this plugin; wire the probe yourself, or use your own if you have one installed.)* Whatever you use should also keep a ledger of which plays shipped and whether they worked, which is the part a rank tool has no equivalent for. Two things to respect when reading any such index: it renormalises over measured layers, so **a high score on low coverage is not a good score** — always read `coverage` beside the total; and engine data is not uniform by market (in Czech/Slovak, for instance, ChatGPT mention data does not exist, so measure AI Overviews and say so rather than reporting a zero as a finding).

**Advisory, not a gate.** A stream with no citation ambition does not need this — if the GTM never expected AI citations, say so in one line and move on. What is not acceptable is carrying a citation metric on the table with no instrument behind it.

**Write to** `P6-Adoption.S2-KPIs.md`. Metric table with north-star at top, leading + lagging beneath, a `Baseline (date)` column on every metric row, instrumentation plan (citing P4.S3's wiring), vanity-check column.

**Def-of-success — ALL must pass before owner sign-off (fail → improvement loop per SKILL.md, never advance):**
- `/critical` run recorded; the score is advisory (target ≥ 8/10) — the gate is the PASS/FAIL criteria below, not the number.
- Exactly ONE north-star, behavioral and revenue-tied ("if this moves, money moves").
- 3–5 leading indicators, each predicting the north-star, each measurable weekly.
- 100% of metrics pass the vanity check ("if this rises but revenue doesn't, do I care?").
- Every metric has a named instrumentation source (an analytics event from P4.S3's wiring, the payments system, a CRM stage, ...) — zero re-instrumentation of already-wired events.
- Every metric row carries a recorded baseline value + date (P5.S1 day-0 snapshot for rank/citation; a live read from the analytics/CRM/payments source for the rest) — a metric without a baseline is FAIL.
- Each leading indicator names its automated read (rank API call, search console, an analytics subscription, a CRM stage report) AND the first read is executed with output recorded in the file — hand-countable-weekly does not pass.
- Weekly digest/rank read actually scheduled on your scheduler (cron, CI, or a task queue) or as a queue row, per the P5.S4 standard, with evidence path recorded.

**Gate out (mandatory — see SKILL.md house rules):**
1. Draft `P6-Adoption.S2-KPIs.md`.
2. Invoke `/critical` on the draft — hunt vanity metrics that survived; is the north-star genuinely behavioral and revenue-tied, or a feel-good proxy?
3. Revise; note what changed.
4. Present the draft + the critical findings + the changes to the owner. **Wait for their explicit approval. Never auto-advance.**

**Checkpoint:** "North-star: [X]. Leading: [Y, Z, W]. Lagging: [revenue, retention]. Final synthesis next — the brief and the 90-day plan."

**Next:** `stages/P6-Adoption.S3-Execute.md`
