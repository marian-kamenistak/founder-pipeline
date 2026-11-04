# P6.S1 — Adoption: GTM strategy → `P6-Adoption.S1-GTM.md`

**Phase: P6-Adoption**

**Earns its keep** always — most streams die in GTM, not product.

**Input first:** channels get locked here from OBSERVED data, not theory — and by the time GTM runs, TWO real datasets exist (this fixes the old circular dependency where GTM had to guess before anything shipped): (1) the live pipeline in `P3-Clients.S1-Outreach.md` — reply rates, which paths-in worked, what objections and buying questions came up; (2) the activation metrics from P5.S1–S2 — post reads, registry traffic, magnet captures, link placements. Read both before answering anything. If the data is too thin to support a channel claim, that's a `[assumption — validation: ...]` tag, not a fact. Weigh the evidence with the words-vs-actions rubric (`references/signals-and-scoring.md`): a channel claim backed only by polite words ("they loved it") is an `[assumption]`; only demonstrated action (call scores ≥7/12, intros made, budget discussed) counts as conversation data.

**Ask one at a time:**
1. First 3 channels — for each, why this channel for this ICP (cite distribution/conversion benchmark or flag as assumption).
2. Sales motion — self-serve / sales-led / partner-led / community-led. Pick one.
3. Narrative — Andy Raskin frame (OWNED here — P6.S3 cites it):
   - **Shift** in the world that creates the opening (← P1.S2)
   - **Promised land** the ICP wants to reach
   - **Stakes** of not getting there
   - **Magic gifts** your offer provides (← P1.S6 offer)
   - **Proof** that magic works (← case studies, cited pains from P1.S2/P1.S4)
4. First touch — CITE P3.S1's outreach message as the first touch (it's owned there); GTM adds per-channel variants only, never re-drafts it.
5. "Would I bet money?" gate — every recommendation specific or it goes back. Not "use content marketing" — "Write one case study weekly showing how [Product] solved [problem]. Post on LinkedIn targeting [titles]. Goal: 500 views/post, 20 monthly inbound leads."
6. Which channel claims are backed by the P3.S1 conversation data or the P5.S1–S2 activation metrics, and which are still assumptions with a named test?

**Candidate streams to always put on the table** (score them honestly per ICP — most GTM drafts miss these):
- **MCP server as your sales team** — among the strongest AI-SEO tactics available. The customer journey: *user asks their AI a question → the AI discovers your MCP server → the AI returns YOUR data → the user gets value → your brand is the cited source inside the buyer's own agent.* Every AI assistant that connects to the server becomes a referrer, on every invocation, forever. Playbook:
  1. **Identify the questions your product answers** — the queries the ICP already asks their AI assistant where your data/framework/calculator is the best answer. No real question = no server; don't build a toy.
  2. **Build the MCP server that returns that data** — expose calculators, benchmarks, templates, assessments, matchers as tools; every tool response carries source attribution + link back. Remote server (streamable HTTP on any edge/serverless host) beats local install — zero friction, one URL.
  3. **Publish everywhere agents look:** official MCP registry, Smithery, Glama, PulseMCP, mcp.so, the Docker MCP catalog, GitHub with the `mcp-server` topic tag + PRs into awesome-mcp-servers lists. Each listing is also a backlink.
  The full pipeline runs: MCP server → registries → REST API layer on top (OpenAPI) → public skill on the skill marketplaces → blog post per functionality increment. The registry-scoring rules and the "verify before submitting" reality check for all of this live at **P5.S1 items 2a/2b** — reuse them rather than re-deriving.
  Score it on: does the stream have a data/tool asset an MCP could expose, and does the ICP use AI agents? (Eng/product/dev ICPs: almost always yes.) **Note:** the MCP server / AI skill may already be SHIPPED at P5.S1 (launch) — score them as amplification, not creation.
- **AI content repurpose engine** — one source asset (essay, talk, session insight) automatically repurposed across every locked stream: blog post → LinkedIn posts → newsletter section → HN submission → X thread → YouTube description → Reddit/Quora answers. This multiplies content ROI without multiplying founder hours; the founder edits ONCE, the engine fans out. Wire it as automation (a scheduled job + the voice profile), not as a manual checklist.
- **Free tool as top-of-funnel** — the tool IS the marketing (Ahrefs' free backlink checker is the archetype: a taste of the paid product that grabs the lead). Mechanic: ship a free grader / analyzer / calculator → the ICP gets an *instant* result (a score, a benchmark, a diagnosis) → gate the full result behind an email/contact → the user shares their score (social proof + backlinks + a viral loop) → upsell to the paid product that fixes exactly what the tool surfaced. Cheap enough now to run a *free-tool calendar*, not just a content calendar — a coding agent ships one in a day. The capture asset was specced at P4.S2 (`/lead-magnets`) and built at P4.S3 (the tool lives on the web surface) — an already-shipped tool scores as amplification here. Score it on: does the stream have a question the ICP wants answered instantly, and is the output worth bragging about?
- **Shareable viral artifact** — make the product's OUTPUT the distribution channel. Ask "what does my user want to brag about?", then make that thing beautiful, branded (logo subtle but present — nobody shares someone else's billboard), and one-tap shareable with a pre-filled post. Canon: Spotify Wrapped, Duolingo streak, GitHub contribution graph, Stripe Atlas incorporation milestone. Every share = free impressions to the exact target audience, and it works in B2B too (the artifact gets pasted into Slack/Teams, not just X). Score it on: does the product create a moment / milestone / result the ICP would screenshot unprompted?

**Skills:**
- **Campaign brief — the default for any GTM with a concrete conversion event** (LOIs, pre-sales, signups, applications). Produce a week-by-week brief with channel mix, asset list, per-channel KPIs, and a budget split shaped for solo-operator execution. *(The original pipeline routed this to a dedicated campaign-planning skill that does not ship in this plugin — write the brief inline to that shape, or use your own equivalent if you have one installed.)*
- **Standing marketing plan** — the structure around the campaign: positioning, channel priorities, and cadence beyond the single conversion push. Do this when the stream needs an ongoing motion, not just one campaign; campaign briefs then slot into it. *(Also inline — no dedicated skill ships here.)*
- **Channel playbooks** — for each locked channel, write down its own mechanics (posting cadence, format, targeting, what a good week looks like) before writing its brief. Inline, per locked channel.
- Lead magnets: the `/lead-magnets` mandate moved to P4.S2 (spec + copy; P4.S3 builds, P5.S1 distributes) — this step only amplifies existing magnets per locked channel.
- `/plan` — fall back to this only if the GTM is exploratory and the conversion event isn't pinned yet.
- `/brainstorm` — for the opening message angle when cold outreach is the lead channel.
- `/seo-audit` — if the GTM relies on an existing site the owner already runs; run BEFORE driving traffic so the funnel isn't leaking.
- **Local-territory boost (home-market organic)** — when the GTM includes a local presence in a market with its own dominant search engine and directories, apply `references/dataforseo-playbook.md` Job 7: measured local-language volumes only in channel projections; that market's webmaster tools and national directory as named checklist items; and the double-value placement rule — a directory/listicle that ranks IN a money SERP beats every other backlink target. **Worked example (Czech/Slovak):** most literal-translation service terms have ZERO measured volume, so the CZ organic channel is a brand + AI-search + Seznam play, not a traffic engine — register with Seznam Webmaster and Firmy.cz and project accordingly. Re-run the same test for whatever your home market is before assuming Google-market economics carry over.
- `/ai-seo` — if the GTM has a content engine that needs to be citation-ready (ChatGPT / Perplexity / AI Overviews). Only worth it if content production is in the 90-day plan.
- **Paid ads — only if both conditions hold**: (1) paid budget is named and (2) CAC math works (target CAC < gross margin × payback period). For a solo-operator reality, paid is rarely the right first GTM lever — push back if these conditions aren't met. *(No paid-ads or ad-creative skill ships in this plugin; design the tactics inline against those two gates.)* When paid clears the CAC gate, a design MCP (e.g. the Canva plugin's `generate-design` / `export-design`, an optional dependency you install separately) can export the static ad creative — same scope: ad visuals only, not decks.
- **Closed-loop paid engine** — when paid IS a locked channel and the offer is proven: wire ad-click → landing → analytics → **your CRM** → revenue → offline-conversion feedback across LinkedIn / Google Search + PMax + Demand Gen / YouTube. Runs AFTER the web asset + analytics stack ship (`/web-site-creator` Phase 6.2 analytics stack). The same CAC gate applies before spend. *(Inline — no ads-system skill ships here.)*

**Write to** `P6-Adoption.S1-GTM.md`. The file OPENS with a mandatory **Observed-data readout** block — P3.S1 reply rate, top 3 objections, P5.S1–S2 metrics, all with real numbers (a line with no data yet says `no data yet — <why>` explicitly) — so gate-time verification of the Input-first mandate is mechanical, not a judgment call. Then: three channels with cited evidence, sales motion, Raskin narrative one-pager (owned here — P6.S3 cites it), per-channel first-touch variants (the first touch itself is P3.S1's message, cited). Supporting artifacts (per-channel briefs, `/seo-audit` output, positioning notes) go in the step folder `P6-Adoption.S1-GTM/`, INDEX in the step md. (Named accounts live in `accounts.md` — P1.S3; outreach messages are P3.S1's.)

**Def-of-success — ALL must pass before owner sign-off (fail → improvement loop per SKILL.md, never advance):**
- `/critical` run recorded; the score is advisory (target ≥ 8/10) — the gate is the PASS/FAIL criteria below, not the number.
- 3 channels, each with a cited benchmark or a flagged assumption + test — zero "everyone does LinkedIn" picks.
- At least ONE of the 3 locked channels is backed by observed numbers from the readout (P3.S1 reply rate or a P5.S1–S2 metric). If all three rest on external benchmarks or flagged assumptions, the step does NOT lock channels — it outputs a dated channel-test plan instead, and the gate is FAIL until at least one test has produced observed numbers.
- Observed-data readout present at the top of the file with real numbers (P3.S1 reply rate, top 3 objections, P5.S1–S2 metrics) or explicit `no data yet — <why>` lines — a missing or vibes-only readout is FAIL. Every `no data yet — <why>` line carries a dated backfill action as a `queues/manual-queue.md` row — missing observation data is an open item, never a permanent exemption.
- Raskin narrative: Shift, Stakes, and Proof lines each carry a source citation (P1.S2 / P1.S4 / named case study) or `[assumption — validation: ...]`; any bare narrative claim = FAIL.
- Plan fits the P2.S1 marketing hour budget (sends, posts, follow-ups counted).
- If paid is in the mix: target CAC < gross margin × payback period, shown numerically.
- First touch cites P3.S1's message verbatim; per-channel variants are actual messages/assets, not categories ("this exact 3-sentence DM", not "cold outreach").

**Gate out (mandatory — see SKILL.md house rules):**
1. Draft `P6-Adoption.S1-GTM.md`.
2. Invoke `/critical` on the draft — attack the channel choices hardest: is channel #1 chosen because the data says the ICP is there, or because it's comfortable? Does the weekly hour budget from `P2-Viability.S1-Economics.md` actually cover this plan?
3. Revise; note what changed.
4. Present the draft + the critical findings + the changes to the owner. **Wait for their explicit approval. Never auto-advance.**

**Checkpoint:** "Locked from observed data: [X]. Provisional pending test (dated, queue row): [Y, Z]. Narrative: [one-liner]. KPIs next — the measurement readout on the locked channels." Never announce a provisional channel as data-locked — the checkpoint claims exactly what the gate verified.

**Next:** `stages/P6-Adoption.S2-KPIs.md`
