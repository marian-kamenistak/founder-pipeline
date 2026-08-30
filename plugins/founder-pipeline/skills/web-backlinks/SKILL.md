---
name: web-backlinks
description: Use when you want to build backlinks, raise domain authority, grow referring domains, run link-building outreach, create a link-magnet directory, or execute/refresh a backlink playbook for any property in your portfolio. Triggers: "backlinks", "link building", "domain authority", "DR", "referring domains", "link exchange", "backlink playbook", "/founder-pipeline:web-backlinks".
argument-hint: <domain> | run <property> [N] | status
---

# Backlinks — plan once, execute with cheap models

Turn competitor backlink data plus your unfair assets (an owned audience, an event, unique datasets) into a durable `PLAYBOOK.md` — a domain-specific execution plan that tracks its own completion — then execute its blocks with parallel cheap-model subagents. The playbook IS the deliverable; executors read nothing but their block plus the playbook header.

## Commands

| Command | What happens |
|---|---|
| `/founder-pipeline:web-backlinks <domain>` | Phases 1-3: prereqs → tactic fan-out → compile/refresh PLAYBOOK.md |
| `/founder-pipeline:web-backlinks run <property> [N]` | Phase 4: execute next N eligible blocks (default 5) with parallel subagents |
| `/founder-pipeline:web-backlinks status` | One table across all properties: plan completion %, pending/sent/replied/won, stalled blocks, next gates, baseline delta. **Plus a board-drift line:** any block terminal in PLAYBOOK.md whose `board_row` is still open (or vice versa) — drift means a 4.8b write-back was missed; report the count and fix it in the same run |

## Property registry (configure once)

This skill does not hard-code any domain. Domains map to properties through the registry at
`${CLAUDE_PLUGIN_ROOT}/skills/web-listings/config/properties.json` — the same registry
`/founder-pipeline:web-listings` reads. Fill it with your own properties before the first run;
it ships with example rows only. A domain that isn't in the registry: ask.

**Focus rule:** max 2 ACTIVE playbooks at a time — the properties tied to this quarter's revenue. Asked for a third → point at the rule, ask which one to pause. (The daily send budget is shared; seven parallel playbooks just starve each other.) **Boundary rule:** every target, asset, and play belongs to exactly ONE property playbook (event speakers/badges/media → the event property; audience members/survey → the community property). If two playbooks could claim it, the more specific property wins.

## The Four Laws (violating the letter = violating the spirit)

1. **White-hat only.** No Wikipedia link insertion (COI; links get reverted, domains blacklisted — the path is notability-first: linkbait assets earn press citations, independent editors cite you). No bare-link drops on Reddit/forums. No paid links, no PBNs, no comment spam.
2. **Honest framing, stated in the template.** Cheap executors refuse blocks that read as extraction — correctly. Every outreach template states the recipient's benefit in its own text. Carve-out: for fix requests and unlinked mentions, an accurate page IS the recipient's benefit — that satisfies this law.
3. **Self-contained blocks.** Target, verified contact, URLs, template text, gates, logging — ALL inline. Test: could a fresh cheap-model session with only this block plus the playbook header complete it?
4. **Never require, promise, or trade a followed link.** A required link-back (e.g. "link to get listed/verified") is a link scheme under Google's spam policy. Directory verification = identity confirmation only; a link-back may be *invited* as optional, and the invite must say so. Any link that IS part of an agreed swap carries `rel="nofollow"` (or `sponsored`) — both directions. Badge/widget snippets ship with `rel="nofollow"` baked in, brand-name alt text; their value is brand, referral traffic, and AI-citation surface — never PageRank. Max 5 live reciprocal arrangements per domain; no three-way swaps (that's a link network); no "partners/resources" pages built for reciprocation.

**Portfolio rules (a portfolio of owned domains = accidental-PBN risk):** own-domain interlinks are contextual, editorial, sparing — never sitewide/footer, never counted in the referring-domains KPI. Own domains never appear in each other's directories or resources pages. **One LINK ask per recipient across the whole portfolio, ever** (ledger enforces). The 30/90-day cooldowns in Phase 4 govern non-link contact only — commentary pitches, journalist queries on a different topic, referral/business conversations.

**Entity work is not backlink work (Family 7).** Wikidata items, Google Knowledge Panel, `sameAs` audits, and authoritative-profile listings are `nofollow`/SERP features — they shape how Google and LLMs identify the person and the organisation, not PageRank. Track them in a separate "entity" line; **never count them as referring domains or report them as backlinks.** Ship the Wikidata item early for personal/org brand: it feeds the Knowledge Graph and is the prerequisite for the Knowledge Panel and any future (editor-created) Wikipedia article.

## The AI-citation layer — why off-page work is worth more than the referring-domains KPI shows

**The headline: off-page is where the measured AI-citation effects actually are.** On-page formatting has *no published correlation coefficient at all*; off-page signals have several, and they beat backlinks:

| Signal | Correlation with AI visibility |
|---|---|
| **Branded web mentions (linked OR unlinked)** | **Spearman 0.664** |
| Branded anchor text | 0.527 |
| Brand search volume | 0.392 |
| Domain Rating | 0.326 |
| Referring domains | 0.295 |
| **Backlinks** | **0.218** |

[Ahrefs, n=75,000 brands, DR>40, keyword volume ≥800.] Vendor study — Ahrefs sells a brand-mention tracker, so treat 0.664 with more caution than their negative results. Correlational throughout; big brands get both mentions and citations for shared reasons.

**Four consequences for how this skill runs — none of them changes the Four Laws:**

- [ ] **A mention is a win even when it never becomes a link.** Family 4 tells you to reclaim unlinked mentions FIRST; keep doing that for ranking, but stop scoring an un-converted mention as a failure — on this evidence the mention was already carrying ~3× the correlation of the link you were chasing. Log mentions on their own line, like entity work; never merge them into referring domains.
- [ ] **Third-party listicles are the single highest-value placement target, and your own listicle is a trap.** 63% of AI citations point to listicle pages [Evertune, ~400M citations]; in professional services, **third-party listicles take 80.9% of citations vs 19.1% for self-promotional ones** [Wix Studio, 75,000 AI answers / 1M+ citations — platform vendor, reported via Semrush-owned Search Engine Land, two layers of interest]. **Never publish your own "best [category]" self-ranking listicle:** of 323 self-promotional listicle citations studied, **224 (69%) cited the brand's own page and then recommended a competitor** [Ray/Amsive, 100 B2B "best X" queries, independently replicated by Solis]. You'd be funding the answer that promotes a rival. This is a live risk for the Family 1 directory play — a niche *directory* of other people is fine; a ranked "best X" list with you on it is not.
- [ ] **Entity work has a per-engine shape.** Ship the Wikidata item early (already Family 7 policy) — but know which engine it buys: ChatGPT leans Wikipedia (47.9% of its top-10 sources), Perplexity leans Reddit (46.7%), AI Overviews lean Reddit + YouTube (~21% / 18.8%) [Profound, 30M citations, Aug 2024–Jun 2025]. On a total-volume basis these shares are far smaller (Wikipedia is 7.8% of ChatGPT citations) — Profound's "share of top-10 sources" framing inflates apparent concentration ~6×. A Wikipedia/Wikidata play is disproportionately a **ChatGPT** play; a Reddit play is disproportionately a **Perplexity** play. Law 1 is unchanged: notability-first, never COI link insertion, never bare-link drops.
- [ ] **Being named matters more than being linked.** Citation rate was 53.1% when a brand was mentioned in the answer vs 10.6% when it wasn't — a 5× gap, with "ghost citations" where the source is cited but the brand never named [Seer, 541,213 responses, 20 brands, 6 platforms — the vendor's own client portfolio, not a random sample]. Reinforces Law 4's existing framing: badge and swap links are worth having for brand and AI surface, never for PageRank.

**What this does NOT license.** Don't retarget the playbook away from links on the strength of a correlation table. Referring domains stay the KPI this skill is measured on; the AI-citation layer is a second scoreboard reported alongside it, never instead of it.

## Phase 1 — Intake & prereqs (sequential, cheap)

0. **Bootstrap.** Create if missing, under the property's working folder: `backlinks/` with `outreach-log.md` (same schema as the ledger), a portfolio-wide `backlinks/ledger.md` (header: `date | recipient email/domain | category (journalist/podcast/editor/peer/vendor/other) | property | block | status (sent/blocked/deferred/parked/dead)`), and `backlinks/do-not-contact.md`. The ledger and do-not-contact list are shared across every property — put them one level above the per-property folders and record the path in the playbook header. Velocity counts only `sent` rows.
1. **Adopt existing work FIRST.** Intake sources, in order: (a) `queues/backlink-queue.md` — the shipped default queue — plus, if you have wired one up, your external task board's open rows for this property with Type ∈ {Backlink, Listing}. An external board is an optional integration, not a requirement; when one is in use, adopted rows get a `→ BL-NNN` note on the board, don't delete them — **and the row's URL is recorded in the block's `board_row:` field, which is what Phase 4.8b writes terminal state back to; an adopted row with no `board_row:` on its block is an adoption bug**. (b) the WHOLE property tree for prior campaign state: `backlink*`, `backlinks/`, `competitor_analysis/**/outreach*`, `competitor_analysis/ACTION-PLAN.md` (often carries outreach state), placement/outreach logs. Every adopted file gets a pointer header to the new playbook. Build a `## Migrated state` table: target | contact | channel | last action + date | status. Status vocabulary: prose maps to `sent` (email/DM/PR sent, connect pending), `blocked`, `parked`, `dead`. **Lifecycle (one rule everywhere):** follow-up gate = last send + 21 days; ONE follow-up ever; no reply 21 days after the follow-up → `parked` (silent targets may be revisited after 6+ months with a genuinely new angle); explicit no, opt-out, or invalid address → `dead` (never resurrect). **Backfill the portfolio ledger from migrated contacts.** Never re-pitch a contacted target.
2. **Competitors.** Accept `competitors/INDEX.md` OR ≥5 profile files in `competitors/` (generate a lightweight INDEX from them, note it). Only if NEITHER exists, ASK: build competitor profiles first (`/founder-pipeline:founder` step 04 produces them), or proceed with discovered competitors — discovery = a backlink-competitors pull plus a SERP-competitors pull from your rank-data provider, spam ≤30, same-audience only. Batch run with no human available → discovered-only, note it in the header.
3. **Backlink-gap data.** Needs step 2's list. `competitor_analysis/` snapshot <30 days old → reuse it (freshness is the criterion; method drift is fine, note it). Otherwise run the cheap tier yourself: for each competitor pull referring domains, intersect the sets, subtract your own referring domains, and rank the remainder by referring-domain count and topical fit. Intersection input: 3-6 competitors of comparable size/geo — exclude DR>80 generic platforms (large developer-content networks and Q&A sites), their gap tables are noise.
4. **Baseline snapshot.** Reuse any <30-day `me.md`/snapshot numbers before paying for a fresh pull. Otherwise pull bulk ranks and bulk referring domains for the property. Young domain with no data → record `baseline: unranked, 0 referring domains`. Baseline → header; every run reports the delta.
5. **Context resolution (binding everywhere).** Property context = the property's own agent-instructions file if present, else its entry in your portfolio context file — never scratch/notes files. Shared numbers (audience size, attendees, sessions, career-history figures) come from your single numbers source of truth and ALWAYS beat property-folder drafts. No positioning in either place → ask the owner for 3 lines before Phase 2; in a batch run with nobody available, STOP after Phase 1 and leave the ask in the run summary — never fan out without positioning (this outranks step 2's discovered-only fallback).
6. **Sending infrastructure.** Cold outreach must NOT default to the primary community/client mailbox. Check the playbook header for a recorded sending decision; if absent, ask the owner once: dedicated address on the property domain (preferred) or explicit OK to use the main inbox at reduced cap (8/day). Record the answer in the header. **Mechanics for a dedicated address:** it must exist as a verified send-as alias in the sending account — confirm it appears in the account's from-options AND that SPF+DKIM+DMARC pass for the property domain before block one; log both checks. Replies land in the primary inbox and feed the Phase 4 triage as normal. Alias not configured → that's an owner-only setup item; until it's done, the property runs at the 8/day fallback only with the owner's recorded OK.

**Cost gate (all phases, all paid calls):** stating the estimated cost in-chat is sufficient below the equivalent of 5 units of your reporting currency per run; above that, ask first. Cache every raw JSON response under `competitor_analysis/<date>/raw/`.

## Phase 2 — Tactic fan-out (parallel: one research subagent per family, one message)

**Pre-step: classify the brand** — community / conference / personal brand / marketplace / SaaS — and tag 1-2 priority families for it (community → badges + survey; conference → event listings + speaker badges + media partners; personal brand → directories + podcasts + PR; marketplace/SaaS → linkbait tools + reviews). Priority families get the instruction "go deep"; others "go wide, top 5 only".

Each agent receives: the domain, brand class, property context per Phase 1.5 (resolved paths — no bare filenames), competitor INDEX, backlink-gap table, **the exclusion list from the Migrated-state table (sent/in-flight, parked, dead — do not re-propose)**, and its family brief from `${CLAUDE_PLUGIN_ROOT}/skills/web-backlinks/references/platform-matrix.md`. Toolset: Read, WebSearch, WebFetch or `/founder-pipeline:firecrawl-scrape` — NO paid rank-data calls inside fan-out agents; if a family needs one (e.g. a content-mention search for unlinked mentions), the orchestrator runs it under the cost gate and passes results in. Internal spreadsheets (e.g. speaker lists) are permitted contact sources; emails from them must be confirmed against the CFP or mail thread they came from, not the live site.

Families 2-6 return the scored table (`target | contact route | effort S/M/L | impact H/M/L (+DR if known) | cost | risk | evidence URL`). Family 1 (directory play) returns a design doc instead: niche, listing schema, submission + verification mechanics (Law 4 compliant), seed list, invite template. Merge, dedupe (also against Migrated state), write to `<property>/backlinks/opportunities.md`.

| Family | One-line brief |
|---|---|
| Directory play | Link-magnet directory on the property domain; listing free, verification = identity, link-back optional invite. Build → `/founder-pipeline:web-site-creator`. **A directory OF OTHERS is the play; a ranked "best X" list with you on it is not** — 69% of self-promotional listicle citations ended up recommending a competitor (see the AI-citation layer above). |
| Partners & exchanges | Adjacent players worth ONE-WAY plays first; reciprocal only within Law 4 caps. |
| Platform placements | **Earned** placements needing a pitch: awesome-lists, speaker DBs, podcast guest slots, roster pages that require an ask. Register-once identity/profile listings — coach directories, event-listing self-serve forms, business/startup registries — are owned by **`/founder-pipeline:web-listings`**, not this family; don't re-propose a target that skill already tracks. **Portfolio rule (still applies wherever this family DOES apply): on any registry/directory that hosts multiple orgs or products, list EVERY owned property in your registry, not just the one that triggered the run.** Each stays a separate entity pointing to its own domain. These are identity listings, not swaps, so the anti-PBN "own domains never appear in each other's directories" rule does not apply to third-party registries. |
| Digital PR & citations | Unlinked-mention reclamation (do FIRST), wrong/dead-link fixes, journalist pipelines, regional media pitches, broken-link building. **Score mentions separately from links** — an unconverted mention is still a win (r=0.664 vs 0.218 for backlinks). Also hunt EARNED placement on third-party "best X" listicles: 63% of AI citations point at listicles, 80.9% of them third-party. |
| Linkbait assets | Original data (survey), citation-engineered stat pages, free tools. Highest ceiling, slowest fuse. |
| Non-standard | Badge embeds (nofollow — brand/traffic/AI-surface value), awards, .edu lectures, testimonials (owner-approved), newsletter swaps. |

## Phase 3 — Compile the playbook

Write `<property>/backlinks/PLAYBOOK.md` from `${CLAUDE_PLUGIN_ROOT}/skills/web-backlinks/references/playbook-template.md`. Non-negotiables:

- The playbook is the domain-specific execution plan and tracks its own completion: the **Plan tracker** section counts blocks by status, % complete, stalled and blocked items, next gates. Complete = every block terminal (won/parked/dead) AND both queues empty.
- Header carries (template has slots for all): baseline, sending decision, autonomy contract, velocity budget (15 sends/day TOTAL across all properties — compile writes the constant into the header slot; the orchestrator computes and passes the day's remaining budget at run time), SUPPRESSION rules, do-not-contact pointer, the Four Laws digest, anchor rule, voice rules (top 8 + banned words, distilled from `/founder-pipeline:brand-voice` and your own style guide if you have one).
- Blocks sorted impact/effort, IDs `BL-NNN` (migrated state keeps history in its own table, new blocks number from BL-001). `gate:` takes a date OR a block ID (`gate: BL-002` = dependency).
- **Compile one gated follow-up block per in-flight Migrated-state row** (gate = last send + 21 days, reply-in-thread, one ever). Without this the history table rots — "none rots silently" covers migrated rows too. Second-language rows: follow-up only if the mail is fix-request/housekeeping class; pitch rows go terminal at gate + 21 unanswered.
- **Non-primary-language templates are compiled, never composed.** Template text in any language other than the executor's primary is written at compile time by a strong model, with `/founder-pipeline:brand-voice` applied and a native-quality translation pass (formal register and full diacritics where the language has them — e.g. Czech "Díky", not "Diky"). Executors only fill {slots}. Every such template starts as CANARY regardless of its English sibling.
- Three queues besides executor blocks: **Owner-only** (signups, payments, posts/PRs/answers from the owner's identity — Reddit, Quora, GitHub, X, LinkedIn — with executor-drafted content attached), **Owner decisions** (e.g. a marketplace profile that may outrank the owner's own name), **Build blocks** (`model: build` — badge SVGs, directory pages, stat pages → routed to `/founder-pipeline:web-site-creator`, and gating their dependent outreach via `gate: BL-NNN`).
- Every number in TEMPLATE **and CONTEXT** verified against your numbers source of truth this run. Compile checklist in the template — run it before saving.

## Phase 4 — Execute (`/founder-pipeline:web-backlinks run <property> [N]`)

**Concurrency:** the orchestrator is the SOLE writer of PLAYBOOK.md, ledger.md, outreach-log.md, **and of any adopted task-board row** (executors never touch the board). Executors return structured results; the orchestrator serializes all writes. Take a run lock (`backlinks/.run-lock` with timestamp + property; stale >2h = ignorable); another live run → wait or tell the owner.

1. Read PLAYBOOK.md. Eligible = `pending` + gate satisfied (date passed / gated block terminal-successful). Take next N.
2. **Suppression, per recipient, in order:** (a) search the sending mailbox for any prior thread with the address AND the domain — any hit → NOT a cold target; route to the Owner-only queue with the thread link (warm intro beats cold template). **Carve-out: threads THIS campaign created (recorded in outreach-log/ledger) are not warm hits — follow-up blocks reply in that thread as designed;** (b) known-audience check against the member/speaker/sponsor list pointers in the header; (c) `do-not-contact.md` — hard stop; (d) your CRM's client/partner records → Owner-only; (e) ledger cooldowns: journalists/editors/podcast hosts 90 days across ALL properties, everyone else 30 days, recipient + any owned domain = one ask ever. **Dedupe within the batch too** (two blocks, same recipient → keep one).
3. Velocity: orchestrator computes today's remaining send budget — 15/day TOTAL across all properties when all senders are verified dedicated aliases; 8/day TOTAL whenever any property sends from the primary inbox; warm-up 8/day for a dedicated address's first 4 weeks. Won-link pace: cap = max(3/week, 4% of baseline referring domains/week) per domain; red flag = 2× cap → pause outreach, let pitches cook. **Small-market rule** (any market where your name is one of a few hundred rather than a few million — recipient person/org located there, or a country-TLD contact, including org inboxes): ONE cold email ever across all properties; the single in-thread follow-up is allowed only for fix-request/housekeeping mail, never for pitches. Declare which markets this covers in the playbook header.
4. Dispatch eligible blocks to parallel subagents at their tagged model (cheap model default, mid-tier for long-form). Executors get: block verbatim + playbook header verbatim + today's send budget. Nothing else.
4b. **Credentials & browser automation.** For any block whose TOOLS line is `browser form`, `browser login`, or `account creation`, drive navigation and non-secret field-fill with a browser-automation tool if one is available in your environment (e.g. the `claude-in-chrome` MCP server, an optional dependency you install separately) — most directory/marketplace submission flows are JS-rendered and session-gated, not plain HTML forms a scripted client can fill.
   - **Hard platform boundary — this is not a skill-level choice and no in-chat authorization lifts it:** the agent may never create an account or enter a password into any field, typed or sourced from a password-manager CLI, full stop. An earlier draft of this section proposed a password-manager write fallback for freshly-generated signup passwords; that was authorized in-session and it was still wrong — the platform's browser-automation rules prohibit account creation and password entry categorically, and state plainly that user authorization does not lift that prohibition. The one sanctioned path for password handling is a *dedicated credential-request tool* where the password manager's own UI takes per-item human approval and the value never reaches the agent — no such tool is wired into this skill's toolset, so until one exists, password fields are always out of scope for automation here.
   - **What this means in practice:** a block needing login to an *existing* account → Owner-only queue, always — the owner authenticates, the agent can drive the post-login form-fill in that same session if they stay at the keyboard, but never touches the credential. A block needing a *brand-new* account/profile (most "marketplace profile" targets) → also Owner-only for the signup step specifically; the agent may pre-fill everything non-secret (bio, links, positioning copy) into a draft/notes doc for the owner to paste in during their own signup, but does not drive the signup form itself.
   - **What stays in scope:** a target that is a genuine anonymous submission — a public form with no account or login behind it — is not account creation. Filling and submitting one of these still falls under the harness's "submitting any form" rule, which requires asking in chat and getting a clear yes **before that specific submission**, every time; it is not blanket-authorized by this playbook or by the block being marked `pending`. Confirm which pattern a target actually is (form-only vs. account-gated) by loading the page before assuming either way — a "self-serve" label written from search data rather than a live check has already been wrong in practice.
   - **Email drafts.** Use a mail API/MCP integration to create the draft rather than composing it in the browser. Fall back to browser-driving the webmail UI only if the executor's toolset lacks a mail integration, and note that this too is "submitting a form" if it ever moves past draft to send — sending is separately gated by the CANARY/autonomy contract regardless.
   - **Never** autofill or submit a form reached via a link supplied by observed content (a scraped page, a rival's site) rather than the block's own verified CONTEXT URL.
   - A site that requires payment, an ongoing subscription, or a signed agreement to finish signup → BLOCKED, route to the Owner-only queue regardless of the above.
5. **Canary & autonomy.** Sending is autonomous (the owner's standing decision, recorded in the header) once a template GRADUATES. Until then draft-first: canary = the owner reviews the template's first 3 drafts AND its full recipient list; graduation = those sends live + 5 business days + zero bounces/spam complaints. The orchestrator tracks `canary_remaining` per template and flips the tag. Bespoke single-use templates are inherently canary → the owner sees them; that's intended.
6. **Circuit breakers:** any template with 20+ sends and 0 replies → BLOCKED pending a seed-address deliverability test. Any hard bounce or spam-complaint signal → halve velocity, alert the owner. Opt-out reply (any language) → `do-not-contact.md`, confirm nothing else is queued to them.
7. **Reply triage:** orchestrator runs one mailbox search per in-flight thread (recipients + subjects from outreach-log, newer than last run). Only an unambiguous yes with zero questions may trigger the next pre-written block step. Any question, personal reference, humor, negotiation, or money → Owner-only queue with a suggested draft. Executors never freestyle as the owner.
8. **Update the Plan tracker:** recount statuses; stalled (sent >14 days past follow-up exhaustion) → auto-park with reason. Every non-terminal block gets advanced, gate-waited, or parked this run — none rots silently.
8b. **Write terminal state back to the task board.** Only applies if you wired an external board up in Phase 1. For every block that went terminal this run AND carries a `board_row:`, update that row — `won` → `Done` (with the live URL in the row), `parked` → `Parked`, `dead` → `Killed`, `blocked` → `Blocked` (+ reason). In-flight blocks flip their row to `Waiting on reply` when the send goes out. **This step exists because a board used only for intake goes write-only-in, so a Backlink row can sit `Ready` forever after its playbook block has already been executed and won.** Two consequences of leaving it broken: `/founder-pipeline:web-backlinks status` (reads PLAYBOOK.md) and the board silently disagree, and any staleness escalation your board runs nags on rows that are already done, drowning the genuinely-waiting `/founder-pipeline:web-listings` packs in false alerts. **Never invent a row** — if `board_row: none`, this block was never adopted from the board and gets no row created here (Phase 1 adoption owns row↔block mapping; seeding new rows is `/founder-pipeline:founder` P5.S3's job).
9. **Delta report:** sent/blocked/deferred per template (send AND reply counts), links won, referring domains vs baseline (reuse <7-day data; refresh at most monthly under the cost gate), plan completion %, next gates, blockers for the owner, monthly deliverability note. **Plus a separate AI-citation line — never merged into referring domains:** brand mentions earned (linked and unlinked), third-party listicle placements won, entity-surface changes. Trend only — this is a directional count you keep yourself, not a measured citation rate; if you run a dedicated AI-visibility probe elsewhere, that owns the actual measurement and this line just points at it.

## Red flags — STOP the run

- A block requires/trades a followed link → Law 4 rewrite
- A block references a file for its content → Law 3 rewrite
- Cold email without recipient benefit + identification/opt-out line → rewrite
- Executor improvised a target, recipient, or non-template second-language text → discard, log
- Links landing faster than 2× the velocity cap → pause property outreach
- Reply mentions payment for a link → decline template, log, tell the owner

## Common mistakes

| Mistake | Fix |
|---|---|
| Re-pitching a contacted/dead target | Adoption + ledger backfill are mandatory; Phase 2 agents get the exclusion list |
| Requiring a link-back "to verify" a listing | Law 4: verification = identity; link invite is optional and says so |
| Followed badge links at scale | Badges ship `rel="nofollow"`; value is brand + AI surface, not PageRank |
| Cold mail from the community mailbox | Phase 1.6 sending decision; dedicated address preferred |
| Executor defaults to draft-only on graduated templates | Autonomy contract is in the header; graduated = send |
| Keyword anchors | Anchor = brand/name or bare URL, in the executor contract |
| Cold-templating someone the owner already knows | Mailbox-history suppression check is per-send and mandatory |
| Counting DA daily | Referring domains monthly; judge quarterly |
| Executing a block and leaving its board row on `Ready` | Phase 4.8b write-back — terminal block flips its `board_row`; stale `Ready` rows drown the real `/founder-pipeline:web-listings` queue in false alerts |
| Creating a fresh board row for a block that was never adopted from one | `board_row: none` means no row; Phase 1 owns the mapping, `/founder-pipeline:founder` P5.S3 owns seeding |
| Writing off an unlinked mention that won't convert | It's a win on its own line — mentions correlate 0.664 vs 0.218 for backlinks |
| Proposing your own "best [category]" listicle as a linkbait asset | 69% of self-promotional listicle citations recommend a competitor — pitch for placement on OTHER people's lists |
| Reporting AI-citation wins inside the referring-domains KPI | Separate line, same rule as entity work |

## Optional dependencies

None of these gate the skill; each has a stated fallback.

- **A rank/backlink data provider** (the family of commercial SEO APIs — bulk referring domains, competitor discovery, content mention search). Without one, Phase 1.3 and 1.4 run off free web search and the baseline is recorded as `unranked, unmeasured`.
- **A browser-automation MCP server** for Phase 4.4b form-fill. Without one, every `browser form` block routes to the Owner-only queue.
- **A mail API/MCP integration** for draft creation. Without one, drafts are written into the playbook for the owner to paste.
- **An external task board.** Without one, `queues/backlink-queue.md` is the queue and Phase 4.8b is a no-op.

## References

- `references/platform-matrix.md` — family briefs + brand-class weighting for Phase 2 agents
- `references/playbook-template.md` — playbook skeleton, block format, executor contract
- `references/review-log.md` — design rationale: what was tested, what failed, and why the rules read as they do
