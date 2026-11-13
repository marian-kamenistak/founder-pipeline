# P1.S5 — Competition + differentiators → `P1-Ideation.S5-Competition.md`

**Phase: P1-Ideation**

**Routing:** fan-out (one agent per competitor, then adversarial verification of each weakness) · scouts CHEAP, verify PEAK · gate critic on the session model

**Earns its keep when** the market has incumbents or substitutes the user must position against. Almost always.

**Becomes performative when** the user is genuinely first-mover in a brand-new category (rare — verify by listing alternatives anyway).

**Input first:** open with P1.S2's RAW alternatives list (`P1-Ideation.S2-Problem.md` — this step researches and validates it) and P1.S4's niche verdict (`niche-verdict.md` in the stream's `predictions/` folder). The competitor set is scoped to the verdict's Pick; angles the verdict marked DEAD are not relitigated here. Pains come cited from `P1-Ideation.S2-Problem.md` and P1.S4's discourse evidence.

Use April Dunford's positioning frame:
1. **Competitive alternatives** — what would they do if your offer didn't exist? (often "do nothing" or "internal hack" — name these too)
2. **Unique attributes** — what does only you have? (capabilities, relationships, IP, distribution)
3. **Enabled value** — what does that uniqueness allow the customer to do that alternatives don't?
4. **Who-cares segment** — who values this enabled benefit the most?
5. **Market category** — what frame of reference do you want the buyer to use to evaluate you?

**Grill pass first** (`references/grilling.md`): map this step's decisions and what depends on what, look up every fact in the intake, `brief.md` and approved step files instead of asking, then ask only the open decisions, each with a recommended answer. Play the answers back and get a yes before drafting.

**Ask one at a time:**
1. Name 3 competitive alternatives — seed from P1.S2's raw list, including "do nothing" and "internal build".
2. For each, one-line on what they do well and where they fail this ICP.
3. Your unique attributes — what only you have. Be specific (not "experience" — the shape to aim for is "412 onboarding audits shipped, 9 named enterprise logos under contract, a monthly practitioner call running since 2021": countable, dated, checkable).
4. Enabled value — what does that uniqueness let the customer DO that alternatives don't?
5. Category — pick the box you want to play in.

**Skills:** `/scout` when the landscape is still fuzzy and competitors aren't named yet. The rest of this stage's research has **no skill shipped with this plugin** — run it inline (and if your install happens to have a dedicated research or enrichment skill, use that instead; the gate is the same either way):

- **Competitive brief** — the default once 1-3 specific rivals are named. Per rival, pull positioning and messaging from their own surfaces: homepage promise, the category words they use, who they say it's for, pricing if visible, proof assets. Write it up as positioning / messaging / gap analysis in the shape the Dunford frame above needs.
- **Deep profile of the top 3 alternatives** — offer, delivery model, named customers or case studies, review-site sentiment, and the specific place they fail THIS ICP, each line carrying a source URL.
- **Primary research** — only if positioning genuinely needs it: analyst reports, customer-review aggregation, community threads where this ICP complains out loud.

**Hard data (optional keyword + backlink data provider — recipes in `references/dataforseo-playbook.md`, Jobs 1 + 3):** for every competitor with a web surface, the qualitative profile gets a quant backbone. The playbook is written against **DataForSEO** (via its MCP server or REST API — an optional dependency you configure separately); any provider returning the same figures works, because the gate below is the citation, not the vendor. The endpoint names here are DataForSEO's, as the worked example:
1. **Discovery check** — competitor-domain and SERP-competitor lookups (`/v3/dataforseo_labs/google/competitors_domain/live`, `/v3/dataforseo_labs/google/serp_competitors/live`) on the named rivals: does the data surface a competitor the owner hasn't named? If yes, it gets a file too.
2. **Quant block per competitor** (format in the playbook): domain rank, est. organic traffic, keyword count, referring domains — via `/v3/dataforseo_labs/google/domain_rank_overview/live` + `/v3/backlinks/summary/live`; their top pages via `/v3/dataforseo_labs/google/relevant_pages/live` (their highest-traffic pages ARE their strategy, use them for the "what they do well" line).
3. **Backlink capture** — `/v3/backlinks/referring_domains/live` per competitor + `/v3/backlinks/domain_intersection/live` across 2+ competitors → the **backlink-gap table** (domains linking to multiple rivals but not to us, with link type + how-to-replicate per row). Saved into the step folder as `_backlink-gap.md`; P5.S2 (links) executes it.
Follow the playbook's full profiling sequence for the profile shape — it persists the raw provider responses next to the written profile, so a later step can re-read the numbers instead of trusting a summary.

**Write to** `P1-Ideation.S5-Competition.md` + the step folder `P1-Ideation.S5-Competition/` — one researched file per competitor/alternative (offer, pricing if visible, positioning language, strengths, where they fail this ICP, sources), fanned out one subagent per competitor. The step md carries the Dunford synthesis + an INDEX table (competitor | file | one-line verdict). "Do nothing" and "internal build" get files too — they're competitors.

**Def-of-success — ALL must pass before owner sign-off (fail → improvement loop per SKILL.md, never advance):**
- `/critical` run recorded; the score is advisory (target ≥ 8/10) — the gate is the PASS/FAIL criteria below, not the number.
- ≥ 3 alternatives including "do nothing" / "internal build", each with a source link.
- Every "where they fail this ICP" line carries a source (review aggregation, pricing page, their top-pages data, or a named-human quote) or is tagged `[hypothesis — validation: <how>]`.
- Step folder holds one researched file per INDEX row, including dedicated files for BOTH "do nothing" AND "internal build".
- Every web-surface competitor file carries the quant block with a per-figure source tag naming the provider and call (e.g. `[source: DataForSEO /v3/dataforseo_labs/google/domain_rank_overview/live, <date>]`) — never scraped guesses presented as data. A `BLOCKED: keyword-data provider unavailable` note passes ONLY if (a) a REST-fallback attempt is recorded (credentials read from your environment, per the engine-routing degradation rule) AND (b) a `queues/manual-queue.md` row is added to backfill the quant block before P5.S2 executes `_backlink-gap.md`. A bare BLOCKED with neither is a FAIL.
- Backlink-gap table exists in the step folder with ≥ 5 replicable targets (or a recorded reason why the territory has none); each row tagged with its data source (e.g. `[source: DataForSEO /v3/backlinks/*]`) — same never-scraped-guesses rule as the quant block.
- ≥ 2 unique attributes that survive the test "could a competitor's sales deck claim the same sentence?" — if yes, it's not unique.
- Enabled value stated as something the customer DOES, not something you have.
- One market category picked (not two hedged ones).

**Gate out (mandatory — see SKILL.md house rules):**
1. Draft `P1-Ideation.S5-Competition.md`.
2. Invoke `/critical` on the draft — attack the uniqueness claims hardest: would a competitor's sales deck refute them? Is "do nothing" being underestimated as the real competitor? Attack the weakness claims ("where they fail this ICP") as hard as the uniqueness claims — an unsourced failure line is wishful thinking about the competition.
3. Revise; note what changed.
4. Present the draft + the critical findings + the changes to the owner. **Wait for their explicit approval. Never auto-advance.**

**Checkpoint:** "Category: [X]. Position vs alternatives: [Y]. Lock this, or run a deeper competitive scout first? Next we distill what actually makes us stand out in this territory."

**Next:** `stages/P1-Ideation.S6-Offer.md`
