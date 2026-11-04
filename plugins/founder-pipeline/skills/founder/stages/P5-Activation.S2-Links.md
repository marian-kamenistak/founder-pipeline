# P5.S2 — Links: backlinks + listings + internal mesh → `P5-Activation.S2-Links.md`

**Phase: P5-Activation**

**Earns its keep** in every stream with a web surface — domain authority and internal linking are the two compounding inputs SEO/GEO actually responds to, and both historically fell into queues nobody worked. This stage EXECUTES the first link-building cycle; `queues/backlink-queue.md` then carries the ongoing motion into Adoption. **Performative when** there's no web asset — record the skip.

## What to do

1. **Adopt the gap table into `/web-backlinks`.** P1.S5 produced `_backlink-gap.md` (replicable competitor backlink targets); `references/web-post-launch.md` lists the standing surfaces. Run `/web-backlinks` for the stream's domain: it compiles the playbook, adopts the queue, and executes the agent-executable **earned** tier now — awesome-list PRs, listicle placement outreach, podcast/roster pitches. **It no longer owns directory submissions** (see step 1b).
1b. **Run `/web-listings <domain>` — this is a SEPARATE skill and a separate motion, not a subset of backlinks.** Register-once identity presence: directories, registries, review sites, startup platforms, and your home market's national catalogs. The two are deliberately split, because bundling them buries the listings half. **The dividing test: does it need an ask, or a form?** A human deciding to include you → `/web-backlinks`. Self-serve registration → `/web-listings`. Run `/web-listings audit <domain>` first, then `/web-listings <domain>` to prepare packs, then `/web-listings run <domain>` for the agent-executable ones.
   **Why this is not optional, and why it may outrank step 1:** on current evidence, backlinks are the *weakest* off-page correlate measured — Spearman 0.218, against branded mentions at 0.664 [Ahrefs, n=75,000 brands]. Third-party review-profile presence swung AI citation rate from **1% to 53.5%** [Seer, 804,491 AI responses], and **80.9% of professional-services AI citations point at third-party listicles and roster pages**, not at your own site [Wix Studio, 75,000 AI answers]. A new stream that ships links but no listings is invisible to the surfaces that now do the citing. Full evidence + caveats: `/web-listings` § "Why this skill outranks its reputation".
   **Known failure mode — the queue nobody drains.** `/web-listings` prepares packs but cannot create accounts, give consent, or pay (its Law 5). On one live site, 13 fully-prepared packs sat untouched for months while 4 of 4 agent-ownable ones shipped. So: every human-gated listing leaves this step as a `queues/backlink-queue.md` row — the listing target in `Play`, the owner in `Owner`, the prepared pack's path in `Evidence / artifact` — and the def-of-success below counts them.
2. **Entity SEO pass** — Wikidata item, sameAs JSON-LD, profile consistency. **Owned by `/web-listings`** (entity category; the Wikidata item is `DIR-0001` in its catalog) — run it there rather than hand-rolling, so the ledger and the `sameAs` table stay single-source. One-time work with long-tail citation payoff; agent-executable except final account confirmations.
3. **Internal-links build (explicit, both directions):**
   - **Inbound to the new stream**: from the owner's existing properties where topically honest (other sites they run, existing blog posts) — each new money page gets ≥3 inbound internal links from relevant existing pages. Properties hosted on a platform with no editing API become editor checklists in `queues/manual-queue.md`.
   - **Within the new site**: every page reachable ≤2 clicks from home; money pages linked from every blog post shipped at P5.S1; no orphan pages (crawl check, not vibes).
4. **First outreach wave for links that need a human** — drafts ready-to-send (`/brand-voice`, top-tier model), queued with artifact paths; the 14-day queue rule will re-surface them.
5. **Log the cycle** — what shipped, what's queued, next re-crawl date. Graduated items live in the `/web-backlinks` playbook; `queues/backlink-queue.md` holds only not-yet-adopted candidates (single-owner rule).

**Skills:** `/web-backlinks` (earned links) **and `/web-listings` (register-once presence) — both, always; naming only one is the historical bug this stage carried**, `/brand-voice` (outreach drafts AND any generated listing copy), `/ai-seo` (citation-surface prioritization when choosing targets).

**Write to** `P5-Activation.S2-Links.md`: executed-links table (target | type | status | URL/evidence | → page strengthened), **a separate executed-listings table** (target | category | status | listing URL | queue row), internal-links summary (pages linked, orphans fixed, no-API-host checklists queued), entity-SEO status, queue handoff counts. Status is an enum: `LIVE | SUBMITTED | QUEUED | SKIPPED(reason)` — "identified"/"planned" cannot occupy a row.

**Def-of-success — ALL must pass before owner sign-off (fail → improvement loop per SKILL.md, never advance):**
- `/critical` run recorded; the score is advisory — the gate is the criteria below.
- `/web-backlinks` playbook exists for the domain and the agent-executable tier is EXECUTED (submission URLs/evidence recorded) — not planned.
- **`/web-listings` has run for the domain and its agent-executable tier is EXECUTED, with every human-gated target a `queues/backlink-queue.md` row carrying a filled artifact path.** A listings run that produced zero rows did not happen. Count and report both numbers separately from the backlink counts — never merge them (entity-accounting rule: listings are citation surfaces, never referring domains).
- Zero orphan pages on the new site (crawl evidence); crawl output records per-money-page inbound count; ≥3 must come from LIVE pages — queued no-API-host checklist links never count toward the 3.
- Every executed/queued link row names the money page (or homepage, with recorded reason) it strengthens; the `/ai-seo` prioritization output is cited per target.
- Entity-SEO pass done or queued with artifacts (Wikidata, sameAs JSON-LD).
- Every human-gated link action is a queue row with a ready artifact — none stranded in this step's file.

**Gate out (mandatory — see SKILL.md house rules):**
1. Draft `P5-Activation.S2-Links.md`.
2. Invoke `/critical` — attack execution evidence hardest: how many links are LIVE or genuinely submitted vs "identified"? Are the internal links topically honest or link-stuffing?
3. Revise; note what changed.
4. Present to the owner. **Wait for their explicit approval. Never auto-advance.**

**Checkpoint:** "Links cycle 1: [N] links executed, [M] queued for you. Listings: [P] registered, [Q] packs waiting on your login. Internal mesh complete ([X] links, 0 orphans). Queues formalized next, then prediction cadence."

**Next:** `stages/P5-Activation.S3-Queues.md`
