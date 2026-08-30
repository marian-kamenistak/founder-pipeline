# P3.S1 — Clients attraction: named accounts + outreach → `P3-Clients.S1-Outreach.md`

**Phase: P3-Clients** (sell first)

**Earns its keep** always, and it runs BEFORE marketing, content, and web on purpose: most first consulting clients come from the warm network — roughly 60% on this pipeline's operating assumption `[operating assumption]` — and conversations, not artifacts, are the validation instrument. This step turns the P1.S3 named accounts (`accounts.md`) and the P2.S4 minimum-evidence momentum into a working pipeline of real companies and real first touches, armed with nothing more than the teaser asset. What these 10-20 conversations teach about channels and objections becomes the INPUT to P6.S1 GTM (Adoption — runs after activation). The outreach message is OWNED here — the smoke test shares it, P6.S1 only adds per-channel variants.

**Ask one at a time:**
1. First 10-20 named accounts — actual companies, with the buyer role identified per account. (Seed from `accounts.md` — the P1.S3 canonical list, never a new one; upgrade guesses to researched entries in that file.) If 10 can't be named, the ICP is too vague — loop back.
2. **Client segments** — split the accounts into 2-4 segments with a stated rationale (ICP variant, warmth, industry, seniority — whatever predicts a different message or conversion). Each segment gets its own message angle via `/founder-pipeline:brand-voice`. One undifferentiated blast is an auto-fail.
3. Per account: warmest path in — existing relationship / mutual intro / community touchpoint / cold. Name the connector where one exists. Plus any **live intent signal** (hiring the role, org change, fresh pain trigger — signal map, strength tiers, and freshness windows in `references/signals-and-scoring.md`): a fresh Strong signal bumps the account into Wave 1, and the opener references the signal — a signal IS a warm channel; signal-less cold stays banned.
4. **Waves** — sequence the outreach: Wave 1 = the warmest, highest-signal segment (5-10 accounts, dated); a **learn gate** between waves (what reply rate / objections / buying signals from Wave N adjust the message, segment, or offer before Wave N+1 fires). Waves must fit the `P2-Viability.S1-Economics.md` weekly marketing hours.
5. Conversion path — first touch → discovery call → pilot/LOI. What's the ask at each step, and what counts as a buying signal (pricing question, start date, scope)? After every discovery/intro call: run the 10-minute debrief + BANT × words-vs-actions scoring (`references/signals-and-scoring.md`) — both /12 scores and the one lowest-factor next action land on the account's record in the system of record; below-5 two weeks running leaves the active pipeline.
6. **Tracking spec** — system-of-record + analytics wiring (below): which pipeline/list per wave, which UTM convention per segment×wave, which analytics events count as interaction.

## System of record + interaction measurement

**Your CRM is the pipeline system of record.** The pipeline is CRM-agnostic — use whatever the P1.S1 house stack declared (Attio, HubSpot, Pipedrive, Airtable, a database in your notes tool — any of them work). Connect it through its MCP connector if one exists, otherwise its REST API with a token from your secrets store, otherwise by hand. What the pipeline requires is the *shape*, not the vendor:

- One list (or pipeline view) per stream; every account a company record with attributes: `segment`, `wave`, `path-in`, `connector`, `stage` (identified → contacted → replied → call booked → buying signal → pilot/LOI → won/lost), `last-touch`, `next-action`.
- Wave launch = batch stage update; replies and call outcomes logged as notes on the record, so `P6-Adoption.S1-GTM.md` can read the conversation data straight out of the CRM instead of reconstructing it from memory.
- **If no CRM is connected**, the shipped fallback is a lead log in this step's folder — same attributes, one row per account — plus a `queues/manual-queue.md` row to get a real CRM wired. The fallback is an interim record, not a pass: see the def-of-success gate below.

**Analytics measures what recipients DO** (not just what they answer) — your product-analytics platform, whichever one the P1.S1 house stack declared:
- Every link sent (teaser page, quiz, calendar) carries `utm_source=outreach&utm_campaign=<stream>-w<wave>&utm_content=<segment>` — one convention, no exceptions, or per-wave attribution dies.
- Track as interaction events: teaser page visit, scroll/dwell, quiz started/completed, calendar page viewed, booking made. Instrument BEFORE Wave 1 fires.
- The learn gate between waves reads BOTH: the CRM (reply/call/signal counts per segment) and the analytics (who clicked but didn't reply — silent interest is re-targeting material for the follow-up, not a dead end).

**Skills:** `/founder-pipeline:scout` to expand the named-accounts list; `/founder-pipeline:firecrawl-scrape` to pull each account's site, careers page and news for the enrichment profile. **Account enrichment runs inline** — no enrichment skill ships with this plugin, so for each account gather it yourself: who the buyer is, the warm path, recent signals, and 2+ personalization hooks, each with a source URL and access date. A prospect database (Apollo, Clay, or similar, via MCP where connected) speeds up contact discovery — verify anything it returns outside its strong coverage regions by hand, since most of them are thin outside North America. `/founder-pipeline:brand-voice` for every outreach message; `/founder-pipeline:brainstorm` for the message angle. For interaction tracking, `/posthog:instrument-product-analytics` if you run PostHog — the PostHog plugin is an **optional dependency you install separately**; otherwise instrument the equivalent events in your own analytics platform. Stage each email-channel message as a **draft in your email client** (via an email MCP connector if you have one — record the draft ID; LinkedIn/DM stay in the md table) and log booked discovery calls to your calendar once confirmed (a complement — most bookings flow through the external scheduler). If the teaser is a deployed deck, check before sending that it renders, its links resolve, and it is reachable at the URL you are about to paste.

**Write to** `P3-Clients.S1-Outreach.md` + the step folder `P3-Clients.S1-Outreach/` — one enrichment profile per named account (who the buyer is, warm path, recent signals, personalization hooks) and the ready-to-send message per account. The step md carries the accounts table (Company | Buyer role | Path in | Connector | Status), cadence, conversion path, and the INDEX.

**Def-of-success — ALL must pass before owner sign-off (fail → improvement loop per SKILL.md, never advance):**
- `/founder-pipeline:critical` run recorded; the score is advisory (target ≥ 8/10) — the gate is the PASS/FAIL criteria below, not the number.
- 10/10 accounts are real, reachable companies with a named buyer role.
- ≥ 30% of accounts have a warm path (relationship, intro, community touchpoint) — all-cold lists fail for a solo operator.
- One enrichment profile per account in `P3-Clients.S1-Outreach/`, each citing ≥2 live sources with URL + access date (personal profile, company page, signal source) — uncited profiles fail.
- Opening message ≤ 3 sentences, via `/founder-pipeline:brand-voice`, asks for a problem conversation not a pitch.
- Every Wave 1 account has a staged ready-to-send artifact: a saved draft (ID recorded) for the email channel, an md-table row for LinkedIn/DM.
- Cadence arithmetic fits the weekly marketing hours; conversion path defines what counts as a buying signal.
- **Segments + waves defined:** 2-4 segments with rationale, Wave 1 scheduled with dates, a learn gate specified between waves (what evidence changes what).
- **System of record live:** the CRM list/pipeline exists with segment/wave/stage attributes and all accounts loaded. If the CRM is unreachable (no connector, no token, no account): write `BLOCKED: CRM` + a `queues/manual-queue.md` row (owner: `<owner>`, ready artifact: account CSV export path, dated) AND Wave 1 does NOT launch until the pipeline is live, or the owner overrides in writing (recorded in this file) naming the interim record — the lead log — and the date the real CRM lands. Never sign off with sends scheduled and no system of record.
- **Interaction tracking live BEFORE Wave 1:** UTM convention per segment×wave applied to every link; teaser/quiz/calendar events instrumented and verified firing.

**Gate out (mandatory — see SKILL.md house rules):**
1. Draft `P3-Clients.S1-Outreach.md`.
2. Invoke `/founder-pipeline:critical` on the draft — are these 10 real, reachable accounts or a wish list? Is the opening message something this ICP would actually answer? Is the cadence honest against the hour budget?
3. Revise; note what changed.
4. Present the draft + the critical findings + the changes to the owner. **Wait for their explicit approval. Never auto-advance.**

**Checkpoint:** "[N] accounts in [K] segments, Wave 1 = [segment] on [date], CRM pipeline live, interaction tracking verified. Messages approved — sends are the owner's click. P4-Build next — the keyword contract (P4.S1) preps while the waves run (∥); GTM waits until P6.S1, when the waves have produced real channel data."

**Next:** `stages/P4-Build.S0-Email.md`
