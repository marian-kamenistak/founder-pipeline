# Capabilities — what this skill uses, and what it does when something is missing

This skill runs on **Claude Code alone**. Every other skill, plugin, MCP server and API it mentions is an
*upgrade*, never a requirement. This file is the single place that says, for each one: which steps use it,
what it adds, and the **inline fallback** the step runs when it is not installed.

Two rules hold for everything below:

1. **A missing capability never removes a gate.** It changes *how* the step does its work, never *whether*
   the def-of-success is checked. The per-step critical pass, the owner's sign-off, the pricing ≥95/100
   scorecard and the P2.S4 profit verdict all run in full on the fallback path.
2. **A missing data source is never filled with a guess.** If a step needs measured data (search volume,
   rankings, backlinks, a CRM read) and no source is reachable, the criterion is marked `BLOCKED` with the
   exact missing input named, and a backfill row goes into `queues/manual-queue.md`. A web-fetch guess or a
   training-data estimate presented as measured data is a FAIL, not a fallback.

---

## Skill resolution (how a `/name` in a stage file is resolved)

Stage files call skills by plain name: `/critical`, `/pricing`, `/brand-voice`. Resolve each one in this
order, once per run, and record the result in the stream's `CAPABILITIES.md`:

1. **Bundled** — the skill ships in the same plugin as this one (`/founder-pipeline:<name>`). Use it.
2. **Your own** — any installed skill with the same name or the same job (your own `/critical`, a voice
   skill under another name, a house SEO skill). Use it, and note the substitution.
3. **Inline fallback** — the card for that skill below. Run it in the main loop (or a subagent at the tier
   the step names) and record `fallback` in `CAPABILITIES.md` and in the step's Validation loop block.

Never stop a run because a skill is missing. Never silently skip the work a skill would have done.

## Agents, workflows and the approval hook (full plugin only)

The full plugin ships the pipeline's roles as real components. The founder-only install has none of them and runs the same roles from the cards below; the gates are identical.

| Component | What it is | Founder-only fallback |
|---|---|---|
| `founder-pipeline:gate-critic` | Read-only critic on the session model, fresh context, fixed verdict block | A generic subagent given the **Critic card** below |
| `founder-pipeline:evidence-scout` | Read-only research worker pinned to the small model, one question, fixed fields | A generic subagent on your smallest model, given the scaffolding in `references/engine-routing.md` |
| `founder-pipeline:claim-refuter` | Skeptic on the session model, one claim, answers REFUTED when unsure | A generic subagent told to refute one claim and to default to refuted |
| `founder-pipeline:completeness-critic` | Asks only "what is missing" before a sweep is called done | A generic subagent given the question, the coverage and the findings |
| `/founder-pipeline:gather-verify` | Workflow: scout per item, skeptic per claim, completeness critic. Background, resumable | The same three roles dispatched by hand, in that order |
| `/founder-pipeline:judge-panel` | Workflow: one blind gate critic per framing; one FAIL fails the gate | Parallel critic subagents, one per framing, never in one response |
| Approval hook | Turns any edit that adds an `approved` row to `PROGRESS.md` into a permission prompt | The rule in `SKILL.md`: only the owner's explicit sign-off flips a row |

A workflow starts many agents at once. Offer it, say roughly how many agents it will run, and start it only on the owner's yes. Record in the step's Validation loop block which path ran: agent, workflow or fallback.

## Capability preflight (runs once, at P1.S1, before any questions)

1. List the skills available in this session. For each name in the **Skills** table below, record
   `bundled` / `own:<name>` / `fallback`.
2. List the MCP tools available in this session. For each row in the **Tools** table below, record
   `connected` / `REST` (credentials found in the environment or secrets store) / `missing`.
3. Write the result to `<stream>/CAPABILITIES.md` (template: `templates/stream-folder/CAPABILITIES.md`).
4. Tell the owner, in three lines max: what is connected, what runs on fallback, and the **one** missing
   item that costs the most evidence (usually the keyword/backlink data provider). Offer the matching
   `INSTALL.md` (in this skill folder) section. Do not block on it.
5. Every later step reads `CAPABILITIES.md` instead of re-probing. If the owner connects something mid-run,
   update the row and say which earlier `BLOCKED` criteria can now be backfilled.

---

## Skills

| Skill | Used at | What it adds | Inline fallback |
|---|---|---|---|
| `/critical` | every step (gate), P1.S1 + P2.S4 kill passes | A tested adversarial reviewer with a stable output contract | **Critic card** below. Mandatory, never skipped. |
| `/brand-voice` (+ `/humanize`) | every reader-facing string: P1.S7, P3.S1, P4.S2, P4.S3, P4.S5, P5.S1–S2, smoke test | Your own voice profile + AI-pattern removal | **Voice card** below. |
| `/prediction` | P1.S4 (hypothesis mode), P5.S4 (cadence) | Demand data, niche verdict, carry-forward keyword table, a dated prediction ledger | **Prediction card** below. |
| `/pricing` | P2.S3 | 7-step JTBD + value-based method, 10-criterion scorecard | **Pricing card** below (same scorecard, inline). |
| `/offers` | P1.S6 | Offer packaging: scope, risk reversal, guarantee, bonuses | Inline: write scope IN / scope OUT, one risk-reversal mechanism with its exact trigger, the guarantee's measurable condition, and the payment structure. Every element must answer one named objection from P1.S5 or P3.S1. |
| `/scout` | P1.S2, P1.S3, P1.S5, P1.S6, P3.S1 | Systematic landscape research with segmentation questions first | Inline: ask 2 segmentation questions, then fan out one subagent per segment with a fixed field schema, a source URL + access date per field, `VERIFIED` / `ASSUMED` labels, and "not found" as a valid answer. |
| `/brainstorm` | P1.S2, P1.S6, P1.S7, P2.S4, P3.S1, P6.S1, smoke test | Structured divergent thinking, questions one at a time | Inline: ask up to 3 focused questions one at a time, then produce 5–8 distinct options, each with one line of upside, one of risk, and what evidence would pick it. Recommend one. |
| `/plan` | P2.S1, P6.S1, P6.S3 | A structured plan with owners and done-criteria | Inline: milestones, each with owner, binary done-criterion, date, and the dependency it waits on. Weeks 1–2 customer-facing only. |
| `/health` | P1.S1 | Project config hygiene before a long run | Inline: confirm the stream's parent folder is writable and under version control, and that no other stream there is mid-flight (the focus guard does the rest). |
| `/firecrawl-scrape` | P1.S2, P1.S3, P1.S5, P2.S3, P3.S1, P4.S4 | Verbatim page content and **raw HTML** (head, JSON-LD) | Web fetch for page *text*. For P4.S4, which needs raw HTML, use `curl -sL <url>`; markdown converters drop `<head>` and JSON-LD, so never use them there. |
| `/web-keyword` | P4.S1 | Keyword contract method, locale decision, translation glossary | Inline: 3–7 primaries, each with measured volume + difficulty + intent from your data provider (else `BLOCKED`), ≥2 candidate phrasings per market checked against the live SERP, an intent-to-page map with no orphan keyword, and a `TRANSLATION-GLOSSARY.md`. |
| `/marketing-psychology` | P4.S2 | Per-page persuasion pass | Inline per page: where is proof placed relative to the claim, which objection does each section answer, is the CTA framed as the next small step. Apply, then re-run the voice card. |
| `/lead-magnets` | P4.S2, P6.S1 | Lead-magnet spec + copy | Inline: one magnet that solves one narrow job for the ICP in under 15 minutes, a delivery mechanism, the capture event, and the follow-up it unlocks. |
| `/web-site-creator` | P2.S2 (preflight), P4.S3 | Scaffold + deploy on your house stack with SEO/AI-SEO hardening | Build on your declared house stack by hand or with your own scaffold. Keep the P4.S3 gates: copy matches P4.S2 1:1, forms with anti-spam, analytics wired, Lighthouse mobile ≥95, `llms.txt` written last from P4.S1's query list. |
| `/seo-audit` | P4.S1, P4.S3, P4.S4, P6.S1 | Technical + on-page audit with severity framing | Inline: title/meta length, one H1, canonical, hreflang, sitemap, robots, JSON-LD validity, internal links, Core Web Vitals. One severity table (High / Moderate / Low). |
| `/ai-seo` | P4.S1, P4.S3, P4.S4, P6.S1 | AI-search extractability and citation readiness | Inline: answer-first paragraphs under question headings, a FAQ block, named entities and dated facts, AI crawlers allowed in `robots.txt`, a markdown twin or `llms.txt`. |
| `/ai-seo-llms-builder` | P4.S3 | `llms.txt` built from real queries | Inline: write `llms.txt` from P4.S1's query list (one line per question → the page that answers it), never from the page tree. |
| `/blog-launch` | P5.S1 | Post pipeline with an 8/10 rating gate | Inline: brief → draft from a real experience → critic card against "would the ICP forward this?" (≥8/10 to ship) → voice card → publish → 3 inbound internal links. |
| `/web-indexation` | P5.S1 | Search-engine and AI-engine discovery | Inline: submit the sitemap in each search engine's webmaster console, ping IndexNow for the changed URLs, and record what was submitted. Never batch-click "request indexing". |
| `/web-backlinks` | P5.S2, P5.S3 | Earned-link execution from the backlink-gap table | Inline: work `_backlink-gap.md` top-down; one tailored pitch per target through the voice card; log target, ask, status. |
| `/web-listings` | P5.S1, P5.S2 | Directories, registries, entity presence | Inline: list 10–20 directories and registries your ICP actually browses (verify each by finding one competitor listed there), submit with consistent name/address/description, log each URL. |

### Critic card (fallback for `/critical`)

With the full plugin, this card is the `founder-pipeline:gate-critic` agent; dispatch that. Otherwise run it as a
**fresh subagent** that has not seen the drafting conversation (PEAK tier for kill passes and final
verifies, HIGH for money gates, otherwise the step's tier). Give it the step file, the stage file's
def-of-success list pasted in, and, if the step names one, the framing to adopt (e.g. "refute the profit
case"). It must:

1. State the framing it was given (or "unframed").
2. Name the 3 weakest load-bearing claims and why each fails if its assumption collapses.
3. Name what is being avoided and what it costs.
4. Give a prioritised fix list, each fix with a rating delta `(+X.X)`.
5. Output, immediately before the last line:
   ```
   DEF-OF-SUCCESS VERDICT
   - <criterion>: PASS/FAIL — one line of evidence
   BLOCKING FINDINGS: <none / list>
   GATE: PASS / FAIL
   ```
6. End with exactly one line: `CRITICAL SCORE: X/10`.

A criterion without evidence in the document is FAIL. Opposing framings run as separate, independent
subagents, never in one response.

### Voice card (fallback for `/brand-voice` + `/humanize`)

Before the first reader-facing string, ask the owner for 3 samples of their own writing (a post, an email,
a page) and write a 10-line voice profile into `brief.md`: sentence length, person, formality, words they
use, words they never use. Then for every string:

- Specific over general: a number, a name, a date, or a concrete scene in every paragraph.
- Cut: em dashes, "not X but Y" reversals, rule-of-three lists, "delve / leverage / seamless / unlock /
  game-changer", rhetorical questions as openers, summary closers.
- Read it aloud against the voice profile; rewrite any sentence the owner would not say.
- Runs at the top tier (PEAK). Cheaper tiers produce rule-compliant but AI-smooth copy.

### Prediction card (fallback for `/prediction`)

Run as ONE delegated subagent (synthesis at PEAK). Inputs: idea, P1.S2 alternatives list, P1.S3 ICP, the
profit bar. It returns `predictions/niche-verdict.md`:

1. 3–5 candidate niches/framings. For each: measured search demand from your data provider (else
   `BLOCKED`), the number of competitors already answering it, and one direct customer-demand indicator
   (a named account's stated pain, a job post, a forum thread with a date).
2. `PICK`, `NEAR-MISS`, `DEAD` per candidate, with the reason.
3. A carry-forward keyword table for P4.S1.
4. `predictions/PREDICTIONS.md`: 3 dated, falsifiable bets ("by <date>, <metric> ≥ <value>"), each with a
   check date. P5.S4 schedules the re-check.

### Pricing card (fallback for `/pricing`)

Inline, in order: (1) the one job the buyer hires this for, in their words; (2) the exact decision-maker;
(3) the alternative they'd use instead, quantified in time or money; (4) value math the buyer can do in 30
seconds; (5) a value-based price, then the tier structure (pure ladder or pure menu); (6) score the
10-criterion scorecard 0/5/10 each: JTBD clarity, buyer profile, alternative anchor, value math, price
logic, tier coherence, voice fit, decoy/anchor, friction removal, differentiation; (7) iterate until
**≥95/100**. The P2.S3 floors (≥3× unit cost, RoI floor, full-cost margin floor) apply on top.

---

## Tools (MCP servers, APIs, connectors)

Each degrades in one direction only: **MCP → the vendor's REST API with credentials from your environment →
`BLOCKED` + a backfill queue row.** Setup commands are in `INSTALL.md` (in this skill folder).

| Tool | Used at | What it adds | Without it |
|---|---|---|---|
| Keyword / SERP / backlink data provider (DataForSEO is the worked example; see `dataforseo-playbook.md`) | P1.S4, P1.S5, P1.S7, P4.S1, P4.S4, P5.S1, P6.S2 | Measured volume, difficulty, rankings, backlink gaps, WHOIS | Volume and ranking criteria are `BLOCKED`. Use your search console's owned impressions where they exist, labelled as such. WHOIS via a registrar's lookup. |
| Web scraping (Firecrawl, via `/firecrawl-scrape`) | P1.S2–P4.S4 | Clean page content at volume, raw HTML | Built-in web fetch + `curl` for raw HTML. Slower, same evidence. |
| Web search (built in to Claude Code) | most research steps | Cited why-now shifts, competitor discovery | Every unsourced claim drops to `[assumption — validation: …]`. |
| CRM (Attio is the worked example; any CRM with an MCP or REST API) | P3.S1, P6.S1, P6.S2 | System of record for accounts, waves, stages | `accounts.md` + the queue files are the system of record. |
| Mail client connector (Gmail or similar) | P3.S1, smoke test | Messages staged as drafts, draft IDs recorded | Messages sit ready-to-send in the step folder as a `Ready` queue row. Sends are always the owner's click. |
| Calendar connector | P1.S6, P2.S1 | Real delivery capacity from the calendar | Ask the owner for their weekly free hours; tag `[assumption — validation: calendar check]`. |
| Spreadsheet connector (Google Sheets or similar) | P2.S1 | A live scenario model with formulas | Markdown tables only; say so in the file. |
| Product analytics (PostHog is the worked example; `posthog:*` plugin optional) | P3.S1, P4.S3, P6.S2 | UTM + event instrumentation, KPI reads | Instrument the same events in whatever analytics you run; read KPIs from its UI and record the numbers with the date. |
| Task board (Notion or similar; `Notion:*` plugin optional) | P5.S3, P6.S3 | A board mirror of the owner-action queue | `queues/*.md` are the system of record. |
| Hosting / DNS (Cloudflare is the worked example; `cloudflare:*` plugin optional) | P4.S0, P4.S3 | Deploy, DNS, anti-spam, transactional mail bindings | Your host's own console and CLI. |
| Scheduler (cron, CI, or your harness's scheduled tasks) | P5.S4, P6.S3, smoke test | Recurring prediction re-checks and standing checks | A dated queue row; the owner explicitly accepts the manual-fire risk at sign-off. |
| Headless browser (system Chrome) | P4.S5 | HTML→PDF deck | Print the deck HTML to PDF from a normal browser; same source-of-truth rule. |
