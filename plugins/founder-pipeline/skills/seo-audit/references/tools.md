# Tools

This file belongs to the `seo-audit` skill.

**A rank/backlink data provider** — real data over estimates, always. **State the plan cost before
any paid call.** The worked example below is DataForSEO's MCP server (`dfs-mcp`), an **optional
dependency you install separately**; any provider exposing equivalent endpoints substitutes, and
the tool names change with it.

- `on_page_instant_pages` — live on-page crawl per URL. Use instead of reading raw HTML.
- `on_page_lighthouse` — Lighthouse from DataForSEO infra; cross-checks local runs.
- `serp_organic_live_advanced` — actual positions and SERP features per priority keyword.
  Validates "why am I not ranking" against reality.
- `dataforseo_labs_google_ranked_keywords` — the full ranking portfolio. Open every site audit with it.
- `dataforseo_labs_google_domain_intersection` — me-vs-competitor keyword overlap.
- `backlinks_summary` + `backlinks_referring_domains` — authority context.

Every metric carries `[source: <provider> <tool>, <date>]`. If the MCP is down, fall back to the
provider's REST API using credentials from your environment before falling back to estimates.
Never present an estimate as a measurement.

**Free** — Google Search Console, PageSpeed Insights, Bing Webmaster Tools (its AI Performance tab
is the only free view of Copilot grounding queries), Rich Results Test, Schema Validator.
