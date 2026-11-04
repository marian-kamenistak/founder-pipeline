---
name: founder
description: Design a new revenue stream, service, product, or business idea end-to-end in founder mode — 25 steps across 6 phases run prediction-informed and sell-first (P1-Ideation with an early /prediction run, P2-Viability closing on the profit kill gate, P3-Clients outreach, P4-Build for content+web, P5-Activation executing the launch, P6-Adoption with GTM, KPIs and the 90-day plan), from problem to first 90-day execute plan. Use whenever the owner wants to launch a new service, productize an offer, build a new SKU, design a new community tier or partnership package, monetize a side project, stand up a new brand, or work through any "should I build X?" decision — even if they don't use the words "revenue stream" or "founder". Every step is challenged with /critical and manually validated by the owner before the next one runs. Forces evidence over assumption, cites every revenue number, names what's NOT included, and refuses to greenlight execution without LOIs, pre-sales, or paid pilots. Includes a 48-hour smoke-test track (5 questions + 10 real outreaches) for "should I even build X?" hunches, and a portfolio-trade gate (which existing stream gives up hours) before any design work. Runs standalone on Claude Code alone: specialist skills (/critical, /prediction, /pricing, /offers, /web-site-creator, …) and tools (keyword data, CRM, analytics) are used when installed and replaced by inline fallbacks when not.
---

# Founder — design a new revenue stream end-to-end

Design a new revenue stream the way the best operators do it: problem first, evidence over wishful thinking, demand data before design lock-in, pricing tied to willingness-to-pay, and execution gated by validation. Walks 25 steps grouped into 6 phases, one step at a time, producing one `.md` file per step in a stream folder.

The skill refuses to let you name a service before you know the problem. Refuses to lock a niche before the demand data is on the table. Refuses to set pricing without willingness-to-pay evidence. Refuses to greenlight execution without LOIs, pre-sales, or paid pilots. These are not bureaucracy. These are the gates that separate streams that ship from streams that die in a doc nobody re-opens.

## Step IDs

Every step has one canonical ID: `P<X>-<PhaseName>.S<Y>-<StepName>` (e.g. `P1-Ideation.S5-Competition`). Short form in prose: `P1.S5`. Step numbering restarts at S1 in each phase. There are NO letter-suffixed steps (no `02b`/`13b`) — every step is first-class. Stage instruction files, template files, and stream output files all carry the same ID, so the step→phase mapping is deterministic from any filename alone.

**One documented exception: `P4-Build.S0-Email`.** Email provisioning had to slot before P4.S1-Keywords and P4.S3-Web, but inserting it as a proper S1 and shifting Keywords→S2/Copy→S3/Web→S4/SourceGap→S5/Deck→S6 would have renumbered every cross-reference to those steps AND retroactively broken any in-flight stream that already held approved P4.S2/S3 rows under the old numbers. S0 was chosen over a renumber for that reason. This is the only S0 in the skill and the only time this rule bends — do not use it as precedent for future insertions without asking first; check every active stream's `PROGRESS.md` for in-flight collisions before ever renumbering a phase after streams exist under the old numbers.

## How to run this skill

**One stage file at a time.** Each step's full instructions live in its own file under `stages/`. At each step:

1. Read ONLY the current stage file (e.g. `stages/P1-Ideation.S2-Problem.md`) — never load all stage files at once.
2. Run the step exactly as the file says: questions one at a time, write the output file.
3. Run the **per-step validation loop** (below). No step is complete without it.
4. Update `brief.md` (business state) and `PROGRESS.md` (pipeline state) after the step.
5. Move to the file named under **Next:** at the bottom of the stage file.

**Serial gates, parallel work.** The step SEQUENCE stays serial and human-gated — every step depends on the approved output of the previous one plus the owner's judgment. But inside that sequence, three kinds of parallelism are explicitly sanctioned:
- **Research fan-out inside a step** (subagents for `/scout`, `/prediction`, account enrichment, or a deep-research pass) — always fine.
- **Paired steps flagged `∥` in the phases table** — draft the second while the first awaits the owner's sign-off; both still gate individually. The pairs, each justified by a verified no-dependency check: **P2.S1∥P2.S2** (tooling needs only the hour budget draft, feeds cost rows back), **P4.S1 prep during P3.S1's send-waves** (keyword research needs no outreach output), **P5.S1's launch items fan out internally**, **P5.S2 alongside P5.S1** (link building starts as soon as the site is live), **P5.S3∥P5.S4** (the prediction-cadence step only appends one row to the manual queue), **P6.S1∥P6.S2** (KPIs read P3.S1/P4.S3/P5.S1 instrumentation, not the GTM file — both feed P6.S3).
- **Background builds**: the web build (P4.S3) runs as one delegated subagent while the main thread works outreach follow-ups (P3.S1) — build zone rules still apply.
Never parallelize across a kill gate (P2.S4) or an unapproved upstream artifact.

## The 6 phases and their steps

25 steps: 7 + 4 + 1 + 6 + 4 + 3.

| Phase | Steps (stage files) | Notes |
|---|---|---|
| **P1-Ideation** (7) | `S1-Init`, `S2-Problem`, `S3-ICP`, `S4-Prediction`, `S5-Competition`, `S6-Offer`, `S7-Name` | S1 creates the folder + `brief.md` + `PROGRESS.md` + intake digest, declares the house stack and currency, and carries the portfolio-trade kill gate. **S4 runs `/prediction` in hypothesis mode** — demand data, niche verdict, keyword/query whitespace — taking S2's raw alternatives list as an explicit input (whitespace and keyword gaps are probed against those domains), so competition scoping (S5), the offer (S6), and the name (S7) are steered by data, not taste. S5 then researches the landscape deeply, scoped BY the niche verdict. S6 merges differentiators + solution (onliness statement → value prop → delivery capacity, in one gate). |
| **P2-Viability** (4) | `S1-Economics`, `S2-Tooling` (∥), `S3-Pricing`, `S4-Validation` | Everything that feeds the kill decision, in one phase. S1 merges time + money: hour budget, roadmap, forecast, unit economics, scenarios, profit-per-founder-hour — one model, one gate. S2 drafts in parallel, feeds cost rows back into S1. S3 = `/pricing` ≥95/100 + WTP plan + price floors. S4 = the `PROFIT VERDICT` kill gate. |
| **P3-Clients** (1, sell first) | `S1-Outreach` | Opens immediately after the verdict — named accounts (from P1.S3's `accounts.md`) + first touches. The first-revenue engine. Deliberately its own phase: nothing in P4 may be used as a reason to delay it. |
| **P4-Build** (6) | `S0-Email` (numbering exception, see Step IDs — skip if the stream inherits an existing inbox), `S1-Keywords`, `S2-Copy`, `S3-Web` (skip if no web asset), `S4-SourceGap` (skip if no web asset), `S5-Deck` (skip if no client-send motion) | The compounders. **S0 = domain-alias email provisioning** on the domain P1.S7 locked (a hosted business-mail suite is the worked example) — MX/SPF/DKIM, role-address aliases, DMARC at `p=none`; must precede S1 (feeds real addresses into copy) and S3 (its transactional-sending SPF must merge with, never duplicate, S0's root SPF). S1 = keyword contract (seeded by P1.S4's carry-forward table, run via `/web-keyword`) **and the locale decision: which languages this stream serves, decided HERE and never retrofitted** — `/web-site-creator` Phase 1.0 needs it before it scaffolds, and adding a second locale after launch means re-cutting every URL. S2 = Copy sources incl. meta/SEO spec + lead-magnet copy (via `/lead-magnets`). S3 = the declared house stack via `/web-site-creator`, always — S1's keyword contract and FAQ are a **hard input** to its `llms.txt`, which is written last, not scaffolded early. S4 = reads the top 3 competitors' shipped HTML (landing + blog post) for head-meta / JSON-LD / element / AI-surface gaps, fixes High+Moderate on the live site, and writes the generalizable pattern back into `/seo-audit` + `/ai-seo`. S5 = HTML→PDF deck via a headless system browser, always (see the deck rule below). |
| **P5-Activation** (4, launch — execution, not planning) | `S1-Launch`, `S2-Links`, `S3-Queues`, `S4-PredictionCadence` | **S1 launches**: first blog posts (`/blog-launch`), publication of any packaged artifact the stream ships (MCP server, agent skill, CLI — see the inline publication checklist in the stage file), lead-magnet distribution — items fan out in parallel. **S2 builds links**: `/web-backlinks` execution + internal-links pass. S3 stands up the three queues. S4 wires the stream into `/prediction`'s recurring cadence. |
| **P6-Adoption** (3, ongoing motion, runs off the queues) | `S1-GTM`, `S2-KPIs`, `S3-Execute` | GTM locks channels from REAL data — outreach replies (P3.S1) + activation metrics (P5.S1-S2) — killing the old theory-only GTM. Adoption's engine is the queues: media-queue = the blog-post/appearance cadence, backlink-queue = `/web-backlinks` continuation. S2 = north-star + instrumentation readout. S3 = the 90-day execute plan. |

Smoke-test track (48h go/no-go before committing to the pipeline): `stages/smoke_test.md` → `smoke.md`. It is a pre-pipeline gate, not one of the 25 steps.

**Prediction-informed, sell-first sequencing:** the run order enforces what the data says — roughly 60% of first consulting clients come from warm network `[operating assumption]`, around 70% of consultant sites produce zero monthly leads `[operating assumption]`, SEO is a 6-24-month compounder, and a niche locked before demand data is a guess wearing a plan's clothes. So **prediction runs at P1.S4** (steering the idea while it's still cheap to change), **outreach (P3.S1) runs immediately after the viability verdict**, content/web (P4) build as compounders in the same run, and GTM (P6.S1) locks channels only after outreach and activation have produced observable data. (An earlier version of this pipeline gated the build on a pre-sale; that gate is REMOVED — the run order still sells first.)

## What this skill produces

One folder per stream at `<parent>/<slug>/` — where `<parent>` is whichever directory the user names at P1.S1. The skill never assumes a default — it asks. Templates for the output files live in `templates/stream-folder/`.

**File naming (hard rule).** Each step is represented by exactly ONE md file in the stream folder, named exactly after its step ID: `P<X>-<PhaseName>.S<Y>-<StepName>.md` (e.g. `P1-Ideation.S6-Offer.md`). Filenames NEVER carry status — no `_in_progress` or any other suffix. Status lives exclusively in `PROGRESS.md` (below). The only unnumbered items in the stream folder: `brief.md`, `PROGRESS.md`, `CAPABILITIES.md` (P1.S1 preflight), `smoke.md`, `accounts.md` (created at P1.S3, the canonical named-accounts list), the `queues/` folder (created at P5.S3, or earlier on the first owner-blocked item), the `predictions/` folder (created at P1.S4), and the designated intake folder.

**PROGRESS.md — the pipeline state file (hard rule).** Created at P1.S1 from `templates/stream-folder/PROGRESS.md`. It is the single source of truth for where the pipeline stands; `brief.md` holds the business state, `PROGRESS.md` holds the pipeline state — never merge them.
- One row per step: `Step | Name | Status | Updated | CRITICAL | Def-of-success | Note` — the Note is a one-line "so what" summary of the step's outcome, so the file doubles as a step-by-step run summary the owner can read top to bottom.
- Statuses: `pending` → `in progress` → `awaiting approval` → `approved`; plus `skipped` (with the why) and `killed` (stream-ending gates only). A step's file existing means nothing — only an `approved` row means approved and locked.
- At any moment at most ONE step is `in progress`/`awaiting approval` EXCEPT the `∥`-flagged pairs above — a flagged pair may hold two.
- A **Rewind log** section records every loop-back: date, step re-opened, contradiction + evidence, cascade re-check result.
- Update the row at every transition, not at end of session — a crash must never lose pipeline state.

**Artifact ownership (dedupe rule — hard).** Every recurring artifact has exactly ONE owning step; later steps CITE the owner's file, they never re-ask or re-produce it. The owners:
- Alternatives/competitor analysis → **P1.S5** (P1.S2 collects the owner's raw list; P1.S5 researches it)
- Named accounts (10-20 real names) → **P1.S3** writes `accounts.md`; smoke test, P2.S3's price anchoring, and P3.S1's outreach all read it
- Demand/keyword/niche data → **P1.S4** (prediction run); P1.S5 scopes competitors with it, P4.S1 seeds the keyword contract from its carry-forward table
- Unique attributes + differentiators + onliness → **P1.S6**
- Delivery-capacity math → **P1.S6**; P2.S1, P2.S3, P2.S4 cite it
- Scenarios (100/50/25%) + profit-per-founder-hour → **P2.S1**; P2.S4 cites
- Outreach message / first touch → **P3.S1**; smoke test uses the same template; P6.S1 cites
- Email/DNS mail records (MX, SPF, DKIM, DMARC) → **P4.S0**; P4.S3's transactional sending domain must merge into P4.S0's root SPF, never write a second one
- SERP/rank baselines → **P4.S1** (pre-build) and **P5.S1** (day-0 snapshot, once); P6.S2 owns the recurring read
- Backlink gap table → **P1.S5** produces `_backlink-gap.md`; **P5.S2** executes it; P5.S3's backlink-queue holds only not-yet-adopted candidates
- Meta/SEO spec → **P4.S2**; P4.S3 implements
- Lead magnet → spec+copy **P4.S2**, build **P4.S3**, distribution **P5.S1**
- Raskin narrative → **P6.S1**; P6.S3 cites
- Analytics instrumentation → **P4.S3** (event wiring, once); P6.S2 owns the metric definitions read from it
- Competitor shipped-HTML teardown (head meta, JSON-LD `@type` inventory, body elements, AI-extractability surfaces) → **P4.S4**; it fixes High+Moderate gaps on the live site, re-runs P4.S3's severity table, and writes the generalizable learning into `/seo-audit` + `/ai-seo`
- Deck pipeline → **P4.S5** is the only deck path
If a later step finds the owner's artifact inadequate, that's a loop-back (below), not a rewrite-in-place elsewhere.

**Step output folders (for high-value multi-file outputs).** When a step produces more than one substantive artifact, it creates a sibling folder named exactly like its file: `P<X>-<PhaseName>.S<Y>-<StepName>/` (e.g. `P1-Ideation.S5-Competition/` with one researched file per competitor; `P6-Adoption.S1-GTM/` with channel briefs). Rules:
- The step's **md file stays the single gate-carrier**: verdict, def-of-success, validation loop, and an INDEX table listing every file in the folder with a one-line "so what". The folder holds data; the file holds judgment.
- Default folder-producing steps: P1.S3 (segment research), P1.S5 (per-competitor files + INDEX), P3.S1 (per-account profiles + ready-to-send messages), P4.S1 (SERP/trends notes per cluster), P4.S2 (per-page copy files), P4.S4 (one raw-extract file per competitor page + INDEX), P5.S1 (launch assets + registry submissions log), P6.S1 (channel briefs, audits). Other steps stay single-file unless the output genuinely warrants more.

## House rules (apply to every step)

**House stack + currency — declared once at P1.S1, referenced everywhere after.** Before any design work, record in `brief.md`:
- **House stack** — the web framework and host, the analytics tool, the form/anti-spam/transactional-email pair, the CRM, and the automation runner this business builds on. The shipped worked example and recommended default: Astro on Cloudflare Workers, PostHog for product analytics, Turnstile + Resend for forms and transactional mail, Attio for CRM, Make.com for cross-app automation. Substitute your own — but declare it once, and then every later step builds on the declared stack rather than re-litigating the choice.
- **Currency** — money figures throughout this skill are written `<CUR>` (e.g. `<CUR>4,900`). Set yours at P1.S1 and substitute it in every output file.
- **Home market + primary export market** — the two locale/market pairs the stream targets by default (language + country for each). Keyword research, SERP checks and search-engine registration are all run per market; nothing in this skill assumes a single market.

**Runs standalone — every other skill and tool is optional (hard rule).** This skill needs nothing but Claude Code. The skills it calls (`/critical`, `/prediction`, `/pricing`, `/brand-voice`, …) and the tools it uses (a keyword data provider, a CRM, analytics, mail, a task board) are upgrades: each is resolved bundled → your own → inline fallback, and every fallback lives in ONE file, `references/capabilities.md`. P1.S1 opens with a **capability preflight** that records what this session has in `<stream>/CAPABILITIES.md`; every later step reads that file instead of re-probing. A missing capability changes *how* a step works, never *whether* its gate runs — and a missing data source marks the criterion `BLOCKED`, it is never filled with an estimate. Install and connection steps per tool: `INSTALL.md` (in this skill folder) in the repo.

**Model floor for reader-facing copy (hard rule):** every `/brand-voice` invocation, every translation pass, and every blog draft (`/blog-launch`) runs on **your top-tier model** — in-session, or by setting the dispatched agent to that tier. Cheaper tiers produce rule-compliant but AI-smooth output. Name a tier, never a specific model codename: codenames age out and the floor must survive them. The full per-step tier matrix lives in `references/engine-routing.md`.

**Honesty rules for every number (hard rule).** A stream is designed on its evidence, so a fabricated figure does more damage here than anywhere else — it survives into the viability gate, the pricing, and the 90-day plan.

1. **Every number comes from a call or a named source.** Never estimate, never round a figure you did not receive, never reconstruct one from memory. Derived figures state what they were derived from.
2. **An unavailable metric prints "not available" and says why** — not blank, not zero, not a plausible placeholder. Blank reads as "nothing here"; zero reads as a measurement. Both misrepresent coverage. (The same rule a site-health monitor enforces as `unmeasured`: a metric that could not be read is never a zero.)
3. **Low confidence is labelled, with the specific missing input** that would raise it. A recommendation whose confidence you cannot state is one you should not be making.
4. **No padding, and name what you did not cover.** A short accurate answer beats a long one. A silent top-25 sample of 400 rows reads as complete — state the cap and the total.
5. **Analysis steps run at high or max effort.** These are verification tasks, not generation tasks.

Rule 2 is the one that pays. In one real run, a keyword check returned no data for five home-market terms and no data in any market for the category's own head term. Dropping those rows, or filling them with a small plausible number, would have hidden the most consequential finding of the run: the category the whole business was built around had no measurable search demand.

**Per-step validation loop (hard rule — no exceptions, no auto-advance).** Every step ends the same way:
1. Copy the step's template from `templates/stream-folder/` to the step's canonical filename (if no template exists for the step, start from the stage file's output spec) and flip its `PROGRESS.md` row to `in progress`. Draft the output in it.
2. Invoke **`/critical`** on the draft — challenge assumptions, evidence, and numbers. Each stage file names what to attack hardest. It natively ends every response with a `CRITICAL SCORE: X/10` line — read it from there and record the findings + score in the file's Validation loop block.
3. **Check the step's def-of-success** — the criteria list in the stage file. **The verdict is computed, not felt:** the critical pass must judge each def-of-success criterion **PASS/FAIL with one line of evidence**, plus list any blocking findings. The step passes only when every criterion is PASS and no blocking finding is unresolved. The numeric CRITICAL SCORE is advisory context, never the pass mechanism — numeric self-scores are unstable across runs; binary criteria carry the gate. At the two kill-decision steps (P1.S1 = focus/portfolio kill, P2.S4 = profit kill), run independent critical passes with opposing framings — at P2.S4 both a profit-refutation and a focus-refutation pass; at P1.S1 a focus/portfolio-refutation pass. Each must pass.
4. **If the gate fails → improvement loop, not advance.** Revise using every relevant tool: re-invoke the stage's specialist skills, fan out research subagents, rewrite via `/brand-voice`, re-run the critical pass. Token spend is not a reason to stop — a weak step compounds through every step after it. After 3 loops with no movement, the missing ingredient is real-world evidence (data, outreach, prediction indicators), not better prose — name exactly what evidence is missing and go get it. Never pad the score by softening the critical pass.
5. When the def-of-success passes, flip the `PROGRESS.md` row to `awaiting approval` and present to the owner: the draft + the critical findings + the score + the def-of-success checklist. **Wait for their explicit approval.** A step without the owner's manual sign-off is not done. (The owner can consciously override a failed criterion — record the override in the file.)
6. On approval: tick the Validation loop checkboxes and flip the `PROGRESS.md` row to `approved` with the date, CRITICAL score, def-of-success result, and the one-line Note.

**Context budget (hard rule).** At any step, the main conversation holds ONLY: the current stage file + `brief.md` + at most ONE prior artifact the step explicitly needs. Everything else is delegated to a subagent that reads/researches/writes on its own context and returns ONLY its conclusion — never raw dumps. If a step would pull more than ~15KB of prior artifacts into the main context, delegate.

**Profit floor + opportunity cost (hard rule).** Captured at P1.S1 and enforced at P2.S1 and P2.S4: the owner's **hurdle rate** = profit per founder-hour of their best current stream, and an **absolute floor** = minimum 12-month profit that justifies the focus cost. A new stream must project **≥ 1.5× the hurdle rate per founder-hour at the 50% scenario** AND clear the absolute floor — otherwise it dies at P2.S4. The P1.S1 bar is also passed into P1.S4 as the prediction run's pre-registered money floor, so the demand data arrives already compared against it. **"Profitable but mediocre" is a KILL, not a maybe.**

**Focus guard (hard rule).** ONE stream in design/build at a time. P1.S1 scans candidate parents for any other stream whose `PROGRESS.md` has rows that are neither `approved` nor `skipped`/`killed`; if one exists, the skill stops and forces a decision: FINISH it, PARK it (dated re-entry note in its `brief.md` + a `parked` note in its `PROGRESS.md`), or KILL it. Every plan must also name the people/tools that carry what the owner can't — a plan where everything lands on the founder's calendar is a fail at P2.S1.

**Golden Rule, adapted (two zones).**
- **Documents zone (P1.S1 through P2.S4):** apply the SPIRIT — resolve every intake/inter-step contradiction by asking the owner follow-up questions before drafting on top of it. Never demand 95% *market* confidence from documents — that comes from evidence gates, and pretending otherwise is analysis paralysis.
- **Build zone (P4.S2 through P4.S5, decks, apps):** apply the LETTER — nothing gets built below 95% confidence in WHAT to build, with named artifact sources: approved Copy sources, locked keyword contract. A self-reported confidence number with no artifact behind it is 0%.

**Loop-back rule (rework preceding steps when quality demands it).** Later steps routinely reveal an earlier output wasn't good enough — outreach replies contradict the differentiators, prediction indicators contradict the niche, price anchoring contradicts the forecast. DON'T patch forward:
1. Name the target step and the specific contradiction (with the new evidence).
2. Get the owner's approval to rewind (overnight mode: allowed autonomously, max once per target step, logged in `MORNING-REVIEW.md`).
3. Re-open the target step — flip its `PROGRESS.md` row back to `in progress` and add a Rewind log entry — re-run its full validation loop.
4. **Cascade check** after re-approval: list every later approved step that cites the changed file; re-validate each, re-open any whose conclusions no longer hold. Record the cascade result in the Rewind log entry.

**Cited assumption chain.** Every revenue figure, conversion rate, market size, or growth assumption gets tagged inline: `[source: <citation>]` or `[assumption — validation: <how we'll test>]`. If you can't say where a number came from or how you'd test it, don't write it.

**"Would I bet money?" gate per deliverable.** Every step's output must reference real names, real numbers, measurable outcomes. Reject generic outputs and re-run the step.

**Honest-assessment frame per step.** Each stage file opens with one line on *when it earns its keep* and *when it becomes performative*. Skip steps confidently when they don't apply — record the skip + why in `brief.md` and mark the `PROGRESS.md` row `skipped`; skips still get the owner's sign-off.

**Active checkpoints between steps.** Never a passive "continue?" — always an active commitment question.

**Owner-action queue (hard rule; queue mechanics at P5.S3).** The moment any step produces an action only the owner (or a named delegate) can perform, write a row into the stream's `queues/manual-queue.md` — created at P5.S3, or earlier on the first owner-blocked item, from `templates/stream-folder/queues/`. Row fields: Task (imperative, with est. minutes) · Type (Backlink / Listing / Social / Content / Podcast / Newsletter / PR / Event / Outreach / Web-SEO / Strategy-Ops) · Stream · Status (`Ready` when an artifact exists, else `Backlog`) · Owner · Added · `Ready artifact` path · `Unblocks` · `Source` = `founder P<X>.S<Y> {stream}`. "Drafted, awaiting the owner" is an OPEN row (`Ready`), not a done state. Every checkpoint restates the stream's open rows: count, oldest item's age, single highest-value next.
**Optional integration:** if you run an external task board, mirror the same fields onto it and let the board be the source of truth for open rows — the schema above is designed to map onto a board's columns one-for-one. The ≥14-day do/delegate/kill rule on stale rows is then enforced by whatever escalation your board or scheduler provides; checkpoints reference that escalation, they don't rebuild it. With no board, the queue files are the system of record and the checkpoint restatement is the escalation.

**One step at a time.** Cap questions at 6 per step. Ask them one at a time.

**Brief updates after every step.** `brief.md` reflects the current state after each step. Always actionable.

**Skill routing.** Each stage file names the specialist skills to invoke; the full per-step routing map — which skills, in which order, at which engine mode and model tier — is the table in `references/engine-routing.md`. Resolve every `/name` through `references/capabilities.md` (bundled → your own → inline fallback card) and record which path ran in the step's Validation loop block.

## Anti-patterns this skill refuses

- **Advancing without the owner's sign-off.** "Looks good, moving on" from the model is not approval.
- **Advancing on a failed def-of-success.** Any FAIL criterion means improvement loop. Also refused: grade inflation — re-running the critical pass softer to fish for a pass.
- **A funnel that never kills is a tunnel.** If early gates kill under ~20-30% of ideas, the gates are ritual. A killed stream is a WIN (avoided opportunity cost); the Camuffo RCTs (759 firms, Camuffo/Gambardella et al., large-scale replication of the "scientific approach to entrepreneurial decision-making" trials) show trained founders terminate MORE and earn more.
- **Locking a niche before the demand data.** P1.S4 exists so the niche, keywords, and content angles are picked FROM evidence — skipping it to "save time" re-creates the guess-first pipeline this version killed.
- **SEO/content as the first-revenue engine.** New pages have roughly 2-6% odds of top-10 within a year `[operating assumption]`; roughly 60% of first consulting clients come from warm network `[operating assumption]`. Keywords/web are 6-24-month compounders — never the plan for client #1.
- **Name before problem.** Force the name to fall out of ideation (and P1.S4's reframe data), not precede it.
- **Pricing from "psychological mechanisms"** instead of value × willingness-to-pay.
- **Business Model Canvas as deliverable.** Thinking tool, not output.
- **Polished brief from zero evidence.** A problem/ICP/offer claim with no cited data behind it — no prediction indicator, no named account, no real conversation, no benchmark — is fiction, however well-written.
- **Vanity KPIs.** Force one north-star *behavioral* metric.
- **"Everyone is the ICP."** Exclusion is a feature.
- **20-question intakes.** Cap at 6 per step, one at a time.
- **30-page outputs.** Produce the 1-pager that gets acted on.
- **Execution without validation gate.** No LOIs, no pre-sales, no pilots = no execute.
- **Building web/content and calling it launched.** A deployed site with unexecuted launch work (no posts, no registry submissions, no links) is inventory, not distribution — P5-Activation is execution, and skipping it re-creates the "drafted, awaiting" graveyard.
- **Web builds outside your declared house stack.** Every web surface goes through `/web-site-creator` on the stack declared at P1.S1, unless the owner explicitly overrides with a recorded reason. The point is not the specific framework — it is that one stack, chosen once, is what makes the build, the SEO hardening and the post-launch work repeatable.
- **Decks built outside the deck path.** P4.S5's default is HTML→PDF through a headless system browser, because the deck then shares the site's components, copy and prices instead of drifting from them, and regenerates from source on every change. A design-tool export (Canva, Figma, slides) breaks that link. Overriding the default is allowed; doing it without recording the reason in the step file is not.
- **Deciding the language late.** Which locales a stream serves is a P4.S1 decision, not a P5 afterthought. Retrofitting a second language means re-cutting every URL, 301ing the originals and re-earning their rankings. Locale is always a URL PREFIX (`/<lang>/<slug>`), never a suffix.
- **Writing `llms.txt` before the research.** An llms file assembled from the page tree describes the site; one assembled from P4.S1's query list answers what people actually ask Google and the AI engines. Only the second gets cited. `/ai-seo-llms-builder` enforces this: its `build` mode refuses to run without a query list, and its `audit` mode flags a file written from the page tree.
- **Accepting mediocre profit.** Under the hurdle rate or under the absolute floor at P2.S4 = KILL, not "kept small on the side".
- **Two streams in design at once.** Finish, park, or kill first.
- **Adding a stream without killing anything.** P1.S1 forces the portfolio trade before any design work.
- **Teaching frameworks instead of running them.**

**Overnight / autonomous mode:** loaded on demand — see `references/overnight.md`. Read it ONLY when the invocation carries the `overnight` flag.

## Resume mode

If the user re-invokes the skill on an existing stream (folder already exists), `PROGRESS.md` tells you where things stand: the row marked `in progress`/`awaiting approval` is the current step; otherwise the last `approved` row is the last done. Ask: "Resume at the next step (or finish the current one), rewind to [step], or restart fresh?"

**Legacy streams (created before this skill introduced `PROGRESS.md`):** an `*_in_progress.md` filename marks the current step; otherwise the highest-numbered approved file is the last done. Resume such a stream under its OWN numbering map — don't renumber a stream mid-flight. New streams always use the P/S map.

## Express mode

If the user flagged express mode at P1.S1, skip the "earns its keep / performative" intros and go straight to the questions.

**Hard gates survive express mode. No exceptions.** Express skips explanations, never evidence: the per-step critical + owner sign-off loop, the P1.S4 prediction gate, the `/pricing` ≥95/100 gate, the **RoI price floor (P2.S3)**, the profit verdict (P2.S4), and the portfolio trade (P1.S1) all apply in full. If express mode is being requested to get around a gate, name that and refuse.

## References

- `stages/*.md` — one file per step; the only stage content loaded during a run
- `templates/stream-folder/` — output templates, including `CAPABILITIES.md` and the three queue files
- `references/capabilities.md` — skill resolution, the P1.S1 capability preflight, and the inline fallback for every optional skill and tool
- `references/engine-routing.md` — the full per-step routing map: specialist skills, engine mode, and model tier, plus the orchestration rules
- `references/frameworks.md` — Value Proposition Canvas / Lean Canvas / Dunford positioning / Monetizing Innovation / Raskin narrative cheat sheets
- `references/pitfalls.md` — failure modes catalogued, with the canonical fix per pitfall
- `references/question-bank.md` — full question bank per step when you need to go deeper
- `references/signals-and-scoring.md` — intent signals, BANT × commitment scoring, intro-call debrief (P3.S1, P6.S1)
- `references/dataforseo-playbook.md` — search-data tool recipes per job (P1.S5, P4.S1, P4.S3, P4.S4)
- `references/web-post-launch.md` — backlink/AI-citation surfaces + awesome-list + entity-SEO playbook (consumed by P5.S1-S2)
- `references/overnight.md` — autonomous overnight mode; read only when the `overnight` flag is set
