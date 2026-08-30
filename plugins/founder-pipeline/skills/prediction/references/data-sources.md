# Data sources — tiered registry

Rule for every tier: record the exact call/URL + date next to the number. A source that can't be re-queried by a future grading run is context, never a leading indicator.

## Tier 1 — keyword / search / AI-search (paid, cache-first)

Your keyword-data provider. Balance check before spending; reuse every cached `raw/*.json` in the output root before paying; respect the run's spend cap. Note that these vendors bill in USD regardless of the currency you report in.

The worked example below is DataForSEO through its MCP server (`dfs-mcp` — an optional dependency you install separately); substitute your own provider's equivalents.
- `kw_data_google_trends_explore` — 5y slope per term
- `kw_data_google_ads_search_volume` / Labs `keyword_overview`, `keyword_ideas` — volume, CPC, difficulty
- `ai_optimization_keyword_data_search_volume` + `ai_opt_llm_ment_*` — AI-prompt volume and LLM mention share (the GEO axis; underused — use it)
- `serp_organic_live_advanced` — live SERP occupancy for the whitespace axis
- Location naming is a live trap on every provider: check the exact string your endpoints expect before trusting a zero. (Worked example: DataForSEO's Labs endpoints want the country name `"Czechia"`, not the code `CZ` — pass the code and you get an empty result set that reads as "no demand".)

## Geographic lag — a larger reference market as leading indicator

When your home market is smaller than, and historically downstream of, a larger market for this category, pull the reference market's locale alongside your target one for every geo-scoped tool (Tier 1 search trends/keyword volume; Tier 2 Wikipedia pageviews on the reference market's language edition). Consumer and B2B tech trends frequently establish in the larger market 6-24 months before matching momentum lands in the smaller one — a term that's flat or thin in the target locale but already rising or mature in the reference market is a **leading indicator**, not evidence of no demand. Log it as one corroborating silo for the Demand axis (`rubric.md`) — never the sole basis for a score — and name the observed lag where a historical comparable pair exists.

Worked example (a Europe-primary idea reading the US as its reference market): "term X hit its US volume plateau in 2024, matching EU volume followed ~14 months later." Set the pairing from the home market + primary export market declared at `/founder-pipeline:founder` P1.S1 — and check the direction before assuming it; not every category flows one way.

## Tier 2 — attention time series (free, scriptable — ideal leading indicators)

- **Wikipedia pageviews** `https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/user/<Article>/monthly/<start>/<end>` — topic attention, ~0.7 correlation with Google Trends; use `user` agent filter; human pageviews decline ~8%/yr — compare against a control article, not raw counts.
- **HN Algolia** `https://hn.algolia.com/api/v1/search_by_date?query=<term>&numericFilters=created_at_i><ts>` — developer/founder mention velocity per rolling window.
- **npm/PyPI downloads** (`api.npmjs.org/downloads`, pypistats) — adoption velocity for tech-stack bets.
- **GitHub** — release cadence, fork counts, dependents (stargazer history is admin-restricted since 2026-07; don't rely on it).

## Tier 3 — papers / reports

arXiv, DORA, Gartner/Forrester press notes, McKinsey/BCG, a16z/Bessemer state-of reports, official vendor research. ≥30% of the registry must come from here or academic sources.

## Tier 4 — labor market

- **Adzuna Jobs API** (free tier ~1k calls/mo) — posting counts + salary per role/skill, EU coverage.
- LinkedIn/Indeed posting searches (manual count, record the query + date).
- Emerging-title scan: the same role under 3+ names is an early-market signal, not three markets.

## Tier 5 — prediction markets (calibration cross-check, free)

- **Polymarket** `gamma-api.polymarket.com/markets` (+ CLOB `/prices-history`) — real-money probabilities on macro/AI/hiring.
- **Manifold** `api.manifold.markets/v0/search-markets?term=` — long-tail niche questions (play-money; weight lower).
- **Metaculus** API — aggregate forecasts + the question-format standard.
Use: find the nearest related question, record its probability in the bet row. >20-point divergence from ours → written justification required.

## Tier 6 — practitioner discourse (context tier — never a sole indicator)

Reddit (official API, OAuth), niche newsletters, conference agendas, podcast episode titles. Feeds the ≥3-silo corroboration test; alone it's Watch-grade.
