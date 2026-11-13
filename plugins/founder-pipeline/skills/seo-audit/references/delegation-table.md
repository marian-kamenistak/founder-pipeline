# Delegation table

This file belongs to the `seo-audit` skill.

This skill owns diagnosis. Everything else has an owner, and reaching past these boundaries forks
a source of truth.

| Concern | Owner |
|---|---|
| Building a new site, and its build-time SEO rules | `/founder-pipeline:web-site-creator` (`phases/5-seo.md` is the canonical build rule set) |
| Building or rewriting one page | `/founder-pipeline:web-site-creator` (its page phases), or whatever page builder you use |
| Structured data spec and the standing schema decision | `${CLAUDE_PLUGIN_ROOT}/skills/web-site-creator/references/metadata.md` §8.4 |
| Site architecture, internal-link topology, URL design | `${CLAUDE_PLUGIN_ROOT}/skills/web-site-creator/references/seo.md` |
| Keyword research, SERP features, PAA and fan-out harvesting | `/founder-pipeline:web-keyword` |
| Writing the content the audit says is missing | `/founder-pipeline:blog-launch` (posts) · `/founder-pipeline:web-site-creator` (pages) |
| De-AI pass on any copy this audit causes to be rewritten | `/founder-pipeline:humanize`, then `/founder-pipeline:brand-voice` |
| Getting a fixed page recrawled | `/founder-pipeline:web-indexation` — never click Request Indexing in GSC |
| Whether ChatGPT / Perplexity actually cite us | Not shipped here. Stand up the ongoing measurement loop yourself: a fixed prompt set per engine, re-run on a fixed cadence, every run stored, with a ledger of which fixes shipped and whether the citation rate moved. Do not fold it into this audit |
| Advisory rewrite of one page for AI citation | `/founder-pipeline:ai-seo` |
| `llms.txt` / `llms-full.txt` | `/founder-pipeline:ai-seo-llms-builder` |
| Place-in-the-query, map pack, business profile, service×city | Not shipped here. Local search is its own discipline: `LocalBusiness` schema, name/address/phone consistency across directories, a claimed and complete business profile, and one page per service×city that is genuinely distinct. Grade a location page here only on the generic on-page layer |
| Crawler allowlist, robots.txt policy | `/founder-pipeline:ai-seo` carries the AI-crawler tier list; the site's own robots.txt policy is yours to own |
| Rank, volume, backlink and competitor data | A rank/backlink data provider MCP or API (this skill's worked example is DataForSEO's `dfs-mcp`, an optional dependency you install separately) |
| Business context, ICP, offer, voice | `brand_context/` in the active workspace |
