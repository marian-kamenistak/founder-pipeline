# Pipeline contract — step IDs, parallel pairs, phases, files and artifact ownership

Reference for the `founder` skill. Read it when you create or resume a stream folder, when a step needs to know which step owns an artifact, or before drafting two steps in parallel. The text below is the pipeline's standing contract; `SKILL.md` carries the short form.

## Step IDs

Every step has one canonical ID: `P<X>-<PhaseName>.S<Y>-<StepName>` (e.g. `P1-Ideation.S5-Competition`). Short form in prose: `P1.S5`. Step numbering restarts at S1 in each phase. There are NO letter-suffixed steps (no `02b`/`13b`) — every step is first-class. Stage instruction files, template files, and stream output files all carry the same ID, so the step→phase mapping is deterministic from any filename alone.

**One documented exception: `P4-Build.S0-Email`.** Email provisioning had to slot before P4.S1-Keywords and P4.S3-Web, but inserting it as a proper S1 and shifting Keywords→S2/Copy→S3/Web→S4/SourceGap→S5/Deck→S6 would have renumbered every cross-reference to those steps AND retroactively broken any in-flight stream that already held approved P4.S2/S3 rows under the old numbers. S0 was chosen over a renumber for that reason. This is the only S0 in the skill and the only time this rule bends — do not use it as precedent for future insertions without asking first; check every active stream's `PROGRESS.md` for in-flight collisions before ever renumbering a phase after streams exist under the old numbers.

## Serial gates, parallel work

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

## Legacy streams

**Legacy streams (created before this skill introduced `PROGRESS.md`):** an `*_in_progress.md` filename marks the current step; otherwise the highest-numbered approved file is the last done. Resume such a stream under its OWN numbering map — don't renumber a stream mid-flight. New streams always use the P/S map.
