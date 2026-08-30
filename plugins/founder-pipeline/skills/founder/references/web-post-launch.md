# P5.S1–P5.S2 — post-launch reference tables

Backlink + AI-citation surfaces, the awesome-list PR playbook, and the entity-SEO / Knowledge-Graph procedure. Consumed by P5.S1–P5.S2 (`stages/P5-Activation.S1-Launch.md`, `stages/P5-Activation.S2-Links.md`) — the launch/link subagents read these; they do not belong in the main build context.

**Backlink + AI-citation surfaces — the top-10 beyond the SERP (work alongside the backlink-gap table, not after it).** LLMs answer from UGC, directories, and quote platforms as much as from ranked pages; each surface below is both a backlink and a standing citation source. Rank within a run by ICP fit, not by this default order:

| # | Surface | Play |
|---|---|---|
| 1 | Hacker News | Original-data essay or Show HN per launchable asset; one front-page hit is worth roughly 20-40 referring domains `[operating assumption — measure your own before planning around it]`, and ChatGPT/Perplexity cite HN threads directly |
| 2 | GitHub awesome-lists | PR the stream's citable pages + any open-source repo into the niche's `awesome-*` lists — permanent links inside LLM training data |
| 3 | Niche directories/rosters | Register-once identity/profile listings — owned end-to-end by **`/founder-pipeline:web-listings`** (catalog, submission, ledger); this stage confirms it ran rather than re-deriving a target list |
| 4 | Expert-quote platforms | Featured.com / Qwoted / MentionMatch — do-follow quotes on Forbes-tier domains at scale |
| 5 | Podcasts | Guest spots in the niche's top 5 shows; show-notes backlink + crawled transcript full of brand mentions |
| 6 | YouTube | Talks/demos titled by money query, description linking the money page; Gemini + AI Overviews cite YT, subtitles are crawled text |
| 7 | LinkedIn articles | Native republish of citable pages (data, cost guide) linking back; Bing-indexed → ChatGPT Search |
| 8 | Newsletter/Substack ecosystem | Guest posts + swaps with the niche's editorial newsletters |
| 9 | Stack Exchange | Same play as Reddit/Quora (substance first, ≤1 link) on the niche's SE sites — a second UGC corpus, less saturated |
| 10 | Product Hunt + tool directories | Launch-day campaign (pick the day, line up a hunter, seed the first comments, brief the people who will show up) — run inline, no skill ships for it; MCP registry listings (PulseMCP/mcp.so/Glama) — also inline: assemble the server metadata, submit to each registry, record the listing URL in the backlink register; the standing Product Hunt/tool-directory profile itself → `/founder-pipeline:web-listings` |

Slack/Discord communities are lead channels, not backlink surfaces (not crawled) — route them to P3.S1/P6.S1.

**Awesome-list / repo-directory PR playbook (proven on a niche `awesome-*` list; applies to any list-shaped surface incl. GitLab lists and public wikis):**
1. **Research first, agent-driven**: fan out a read-only agent over `gh search repos` + web search to rank candidate lists by accept-likelihood × authority (alive within ~18 months, has a section the entry genuinely fits, history of merging community PRs). Never mass-target; pick the top 3-5 per cycle and queue the rest in the drip backlog.
2. **Lead with a wedge, not an ask**: scan the target list for a dead link, stale name, or missing obvious resource that WE can fix — the first PR being a correction (ideally to our own moved/renamed property) has near-certain accept odds and buys goodwill for the additions.
3. **One entry per PR**, section-appropriate, description matching the list's own style, canonical `https://www.` URL verified live (curl every URL before committing).
4. **Disclose ownership in every PR body** ("my project, separate PR so you can reject on merits") — maintainers merge transparent self-adds and ban sneaky ones; if the list already cites the founder somewhere, say so.
5. Push branches to a fork, `gh pr create` per branch; log each PR URL in the stream's backlink register and let the drip scheduler track merge status.

**Entity SEO / Knowledge Graph (person or org brand — route to `/founder-pipeline:web-backlinks` Family 7).** Distinct from backlinks: these shape *who Google and LLMs think the brand is*, pass no PageRank, and are tracked on a separate "entity" line — never counted as referring domains. Order: (1) **Wikidata item** — create/extend the Q-item for the founder and the org, each statement cited to an independent source (press, conference pages, Crunchbase); it's the primary Knowledge-Graph feed and the prerequisite for everything below. (2) **`sameAs` consistency** — confirm the on-site entity schema (step 8) lists the Q-item and the identical profile set the brand uses elsewhere. (3) **Google Knowledge Panel** — once the entity is consistent, claim the panel via Google account verification. (4) **Authoritative profiles** — Crunchbase person + org, consistent name spelling on speaker/press pages. Wikipedia is NOT a build step — a compliant article only becomes possible after real independent press exists, and only an independent editor may create it (see `/founder-pipeline:web-backlinks` Law 1).
