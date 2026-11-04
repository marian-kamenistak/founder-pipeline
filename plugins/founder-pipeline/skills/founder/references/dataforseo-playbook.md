# Search-data playbook — tool recipes for founder stages P1.S5 / P4.S1 / P4.S3 / P4.S4

**Purpose:** one place that maps each research job to the exact API calls, so stages P1.S5 (competition), P4.S1 (keywords), P4.S3 (web hardening), and P4.S4 (competitor source teardown) pull REAL data instead of scraped guesses. Referenced by `/seo-audit` and `/ai-seo`.

**The recipes are written against DataForSEO** — a paid third-party search-data API, and an **optional dependency you configure separately** (its MCP server, or its REST endpoints). It is the worked example, not a requirement: any provider that returns the same figures works, because the gate is the citation, not the vendor. Substitute your provider's endpoint names throughout.

**Endpoints are written as REST paths** (`/v3/...`), because the path is the one name that works on every access route: the REST API takes it directly, and an MCP server that exposes a single generic request tool takes it as the `path` argument (`method: POST`, `data` as an array of task objects). If your MCP server instead exposes one tool per endpoint, its tool names are derived from these paths.

**Availability rule (from SKILL.md cross-cutting):** if the provider's MCP server is connected, these endpoints OVERRIDE any scraped or estimated number — and if the server has a no-AI / raw-response mode, use it whenever you need the `cost` or `check_url` fields (DataForSEO's MCP takes `noAiMode: true`; its default summarised response drops both, so you can neither log spend nor cite the source). If not connected, fall back to the provider's REST API (`https://api.dataforseo.com` + the same path, for this one) with credentials read from your secrets store — same endpoints, same data. Never silently substitute weaker data (fetch-and-guess, training-data estimates) and present it as equal; tag the criterion `BLOCKED` instead and add a queue row to backfill.

**Every number cited from these endpoints gets the inline tag** `[source: <provider> <path>, <date>]`.

---

## Location & language parameters

Set these from the **home market and primary export market declared at P1.S1** — nothing in this playbook assumes a single market, and nothing assumes Google is the dominant engine in yours. Look up your markets' exact `location_name` strings in the provider's location list before the first call; the strings are literal and unforgiving.

| Territory | location_name | language_code |
|---|---|---|
| Your home market | the provider's exact string for it | the market's own language code |
| Your primary export market | e.g. `United States` (largest EN corpus) or `United Kingdom` | `en` |

**Worked example (a Czech-language home market with an English export market):**

| Territory | location_name | language_code |
|---|---|---|
| Czechia | `Czechia` — **not** "Czech Republic"; the API rejects the long form | `cs` (or `en` for EN-language queries) |
| Slovakia | `Slovakia` | `sk` |
| Global / EN | `United States` or `United Kingdom` | `en` |
| Poland | `Poland` | `pl` |

Run each market's keyword set as a SEPARATE call — volumes and SERPs differ completely between markets, and a merged call silently averages two different realities. The default pair for any stream is `<home market>` + `<primary export market>`.

---

## Job 1 — Discover competitors + describe them (P1.S5)

| Step | Tool | What it gives |
|---|---|---|
| 1. Discover unnamed competitors | `/v3/dataforseo_labs/google/competitors_domain/live` (seed: own domain or the best-known rival) | closest organic competitors by keyword overlap — surfaces rivals the owner hasn't named |
| 2. Cross-check via SERP | `/v3/dataforseo_labs/google/serp_competitors/live` (seed: 3-5 primary keywords) | who actually occupies the SERPs for the money terms |
| 3. Quant block per competitor | `/v3/dataforseo_labs/google/domain_rank_overview/live` + `/v3/backlinks/summary/live` | est. organic traffic, keyword count, traffic value, domain rank, referring domains, spam score |
| 4. Their content strategy | `/v3/dataforseo_labs/google/relevant_pages/live` | their highest-traffic pages = what actually works for them |
| 5. Their tech stack | `/v3/domain_analytics/technologies/domain_technologies/live` | CMS, analytics, marketing stack |
| 6. Compare all at once | `/v3/backlinks/bulk_ranks/live` (array of domains) | one call, domain rank for every competitor — feeds the INDEX table |

**Quant block format (goes in each competitor file):**

```
| Metric | Value | Source |
|---|---|---|
| Domain rank | NN | [source: <provider> /v3/backlinks/summary/live, YYYY-MM-DD] |
| Est. organic traffic /mo | NN | [source: <provider> /v3/dataforseo_labs/google/domain_rank_overview/live, ...] |
| Organic keywords | NN | ... |
| Referring domains | NN | ... |
| Top page by traffic | URL — keyword | [source: /v3/dataforseo_labs/google/relevant_pages/live, ...] |
```

## Job 2 — Keyword research for the product (P4.S1)

| Step | Tool | What it gives |
|---|---|---|
| 1. Expand seeds | `/v3/dataforseo_labs/google/keyword_ideas/live` + `/v3/dataforseo_labs/google/keyword_suggestions/live` + `/v3/dataforseo_labs/google/related_keywords/live` | candidate keywords around the seed terms with volume/CPC/competition |
| 2. Volume + CPC (exact) | `/v3/keywords_data/google_ads/search_volume/live` (batch up to 1000 keywords/call) | Google Ads volumes — the canonical numbers |
| 3. Difficulty (batch) | `/v3/dataforseo_labs/google/bulk_keyword_difficulty/live` | 0-100 difficulty per keyword, one call for the whole set |
| 4. Intent | `/v3/dataforseo_labs/google/search_intent/live` | informational / commercial / transactional / navigational per keyword — feeds the intent-to-page map |
| 5. Trends | Google Trends explore (`/v3/keywords_data/google_trends/explore/live`, territory-filtered) — call parameters in `${CLAUDE_PLUGIN_ROOT}/skills/web-keyword/references/dataforseo-recipes.md` → Trends; direction per the rule below this table | rising/flat/declining/sparse — replaces manual WebFetch of Google Trends |
| 6. What competitors rank for | `/v3/dataforseo_labs/google/ranked_keywords/live` (per competitor domain) | their keyword portfolio with positions and volumes |
| 7. Keyword gap | `/v3/dataforseo_labs/google/domain_intersection/live` (own domain vs each competitor) | keywords they rank for and you don't (and vice versa) — the uncontested-territory finder |
| 8. AI-search volume | `/v3/ai_optimization/ai_keyword_data/keywords_search_volume/live` | how often the phrasings are asked to LLMs — validates the AI-search question list |

**Trends direction rule (the `Trend` label in Jobs 2 and 2b).** Call with `time_range: past_5_years` (weekly points), in the raw-response mode so `check_url` survives — cite each figure with it, since it opens the same query in the Google Trends UI. Take the last 104 weeks, dropping the partial week flagged `missing_data`. A `null` week means "below Google's data threshold", never zero; small markets are full of them.
1. If under 80% of those weeks carry a value, the label is **`sparse — direction not measurable`**. Stop there: a half-empty series fakes big swings. `sparse` is an instrument finding, not a demand finding — decide on Ads volume and note that Trends could not see the term.
2. Otherwise compare the mean of the last 52 weeks with the mean of the prior 52, counting `null` as 0. Above **+10%** is `rising`, below **−10%** is `declining`, anything between is `flat`. Record the change beside the label, e.g. `rising (+19%)`.

Values are 0-100 relative to the highest point in the call, so numbers compare only *within* one call (max 5 terms). Comparing candidates therefore means ONE call: two single-term calls each rescale to their own peak and look equally strong whatever the real demand. For an ambiguous term (also a film title, a sport), set `category_code`, or the related queries fill with the wrong meaning. An empty `rising` list in a small market means the movement is below Google's threshold, not that nothing is rising — fall back to the `top` list.

## Job 2b — Localize the term, don't translate it (P4.S1 step 2, every non-EN territory)

**Purpose:** pick each territory's keyword by measured demand, not by translating the English term. A literal translation is a hypothesis to test, never the default answer — Job 7 item 2's 88× synonym gap and item 3 (English loanwords beating literal local renders in technical categories) are both instances of this same failure mode.

| Step | Tool | What it gives |
|---|---|---|
| 1. Draft candidates (no tool — ICP-language step) | — | per seed concept: the literal translation, the industry/job-title term locals actually use, any buyer-language synonym (Job 7 item 2's pattern), and — if the brand deliberately keeps English terms — the kept-English option |
| 2. Volume per candidate | `/v3/keywords_data/google_ads/search_volume/live` (batched, one call per territory `location_name`+`language_code`) | real monthly volume per candidate, side by side |
| 3. Trend per candidate | Google Trends explore, all candidates for one concept in ONE call (≤5) — direction rule under Job 2 | rising/flat/declining/sparse per candidate — a candidate can have volume but be fading; `sparse` = judge on volume alone |
| 4. Lock | — | highest real volume+trend wins the concept for that territory. Near-zero volume across ALL candidates (Job 7 item 3 — common for smaller-language B2B service terms) still locks a term, tagged `[low-volume — brand/AI-search play]`, never left as an untested literal guess |
| 5. Persist | — | write the locked term + rejected candidates (with their volumes, as the evidence trail) into the project's `TRANSLATION-GLOSSARY.md`. **No translation skill ships in this plugin** — hand this file to whoever translates the pages (human or model) as a hard constraint, so the SEO-validated term is what ships instead of a fresh re-translation |

**Output format (localization table, one row per concept):**
`Concept (EN canonical) | EN term [vol, source] | <Territory> term — locked [vol, source] | rejected <Territory> candidates + volumes [source]` — one locked-term column pair per non-EN territory in scope (playbook location table above).

## Job 3 — Backlink gap: what links competitors have, to copy the approach (P1.S5 capture → P5.S2 execution)

| Step | Tool | What it gives |
|---|---|---|
| 1. Their referring domains | `/v3/backlinks/referring_domains/live` (per competitor, sorted by rank) | where their link equity comes from |
| 2. **The gap** | `/v3/backlinks/domain_intersection/live` (targets: 2+ competitor domains; exclude: own domain) | domains linking to MULTIPLE competitors but NOT to you — the highest-probability outreach targets (they demonstrably link to sites like yours) |
| 3. Individual links + anchors | `/v3/backlinks/backlinks/live` + `/v3/backlinks/anchors/live` (per priority referring domain) | the exact pages and anchor texts — reveals HOW they earned it (directory listing, guest post, podcast, review) |
| 4. Filter junk | `/v3/backlinks/bulk_spam_score/live` | drop spam-score > 30 targets before they enter the outreach list |

**Output format (backlink-gap table, one row per target domain):**
`Referring domain | Rank | Links to (which competitors) | Link type (directory / guest post / podcast / listicle / review) | How to replicate | Priority`

The "How to replicate" column is the deliverable — a listable action (submit to directory X, pitch podcast Y, request inclusion in listicle Z), not a metric.

## Job 4 — Rankings: how competitors and me rank on Google (P4.S1 pre-build baseline → P5.S1 day-0 snapshot, once → P6.S2 recurring KPI read)

| Step | Tool | What it gives |
|---|---|---|
| 1. My rankings | `/v3/dataforseo_labs/google/ranked_keywords/live` (own domain) | every keyword the site ranks for, with position + URL |
| 2. Head-to-head | `/v3/dataforseo_labs/google/domain_intersection/live` (me vs competitor) | shared keywords with BOTH positions side by side |
| 3. Trajectory | `/v3/dataforseo_labs/google/historical_rank_overview/live` | rank history — is a competitor rising or fading |
| 4. Live position check | `/v3/serp/google/organic/live/advanced` (per primary keyword, territory-set) | the actual SERP right now — where each domain sits today |

## Job 5 — SERP validation (P4.S1 gate — every primary keyword)

Labs data is a database snapshot; the live SERP is the truth. For EVERY primary keyword in the keyword contract, run `/v3/serp/google/organic/live/advanced` (correct location + language) and record:

1. **Intent confirmed?** Do the top-10 results match the intent you assigned (a keyword you called "transactional" whose SERP is all blog guides = intent misread → fix the intent-to-page map)?
2. **Who actually ranks** — domains in top 10 (competitors from P1.S5 there? someone new?)
3. **SERP features** — AI Overview present? Featured snippet? People-also-ask? Local pack? Video? These change what "ranking" is worth and what format wins.
4. **Beatable?** Top-10 all DR-80 giants = keyword is mispriced for a new site regardless of "difficulty" score — flag it.

A primary keyword without a recorded live-SERP check is an unvalidated guess and fails the def-of-success.

## Job 6 — SEO + AI SEO hardening (P4.S3 / `/seo-audit` / `/ai-seo`)

| Concern | Tool | What it gives |
|---|---|---|
| On-page audit (live) | `/v3/on_page/instant_pages` (per URL) | meta, headings, canonical, schema presence, internal links — real crawl, not guesses |
| Performance | `/v3/on_page/lighthouse/live/json` | Lighthouse run on the provider's infrastructure — a cross-check against your own local or CI Lighthouse run |
| Content parse | `/v3/on_page/content_parsing/live` | how a crawler actually reads the page content |
| LLM mentions — am I cited? | `/v3/ai_optimization/llm_mentions/search_mentions/live` (brand/domain query) | where the brand appears in LLM answers — automated, replaces manual-only testing |
| Who wins AI answers in the niche | `/v3/ai_optimization/llm_mentions/top_mentioned_domains/live` + `/v3/ai_optimization/llm_mentions/top_mentioned_pages/live` | which domains/pages LLMs cite for the topic — the AI-SEO competitor set |
| Live LLM answer probe | `/v3/ai_optimization/<model>/llm_responses/live` (`<model>`: `chat_gpt`, `claude`, `gemini`, `perplexity`) / `/v3/ai_optimization/chat_gpt/llm_scraper/live/advanced` | what ChatGPT actually answers for the target query, with sources |
| Rank baseline day-0 snapshot (owned by P5.S1, run once; P6.S2 owns the recurring read) | `/v3/dataforseo_labs/google/ranked_keywords/live` (own domain, day of launch) | the day-0 snapshot the search console's later readings are compared against |

---

## Job 7 — Home-market boost + new-site launch checklist

**Worked example: a market where Google is not the only engine that matters.** The lessons below come from one stream launching a Czech-language site alongside an English one. Read them as the *shape* of what happens in any market with its own dominant search engine and its own directories — then re-run the measurements for yours. Do not carry the Czech numbers into your own money model.

1. **Indexation before diagnosis.** On a new or cut-over domain, money pages can sit unindexed for WEEKS — in this run, a money page still read "URL is not on Google" nine days after cutover, which fully explained its missing rankings. Before blaming keywords or authority, run a URL inspection on every money page in the search console. Fixing it (queueing pages, IndexNow, the local engine) is **`/web-indexation`**'s job, not this playbook's — run it on day 1 post-launch for every money page.
2. **Name pages after what buyers type, not what the brand says.** Check the synonym pair volumes before locking any page title. In this run the role-title pair split 880/mo against 10/mo — an **88× gap** that the brand's preferred word was hiding. One `/v3/keywords_data/google_ads/search_volume/live` batch call answers it for every page title at once. This is the English instance of the general Job 2b method — run the same candidate comparison for every non-English territory too, not just English synonym pairs.
3. **In a smaller language, organic volume for niche B2B services is near-zero.** Most literal-translation service terms returned `None` volume; the few real terms were generic (a broad career term at 40/mo). So those pages are a brand + AI-search + local-engine play, not a volume play: target the 1-2 real-volume terms, write the titles in the actual local language (never English titles sitting on a `/<lang>/` path), and do not project export-market traffic in the money model — cite the measured local volumes. Job 2b's low-volume tag exists for exactly this case.
4. **The local engine's webmaster tools.** Where a national search engine holds real share, Google's console is not enough — verification, per-property API-key scoping, force-reindex and IndexNow coverage for that engine are all **`/web-indexation`**'s job; see that skill for the mechanism. One mechanism fact worth keeping here: these engines usually scope their API key **per verified property**, so every domain needs its own key — a key issued for one site will silently return that site's data if you point it at another.
5. **Search-engine registration ≠ ranking. Registering with more engines only affects DISCOVERY, never position** (ranking is content + authority + backlinks). So register where the ICP actually searches, and ignore the long tail:
   - **Google Search Console** — always. Roughly 90% share in most markets.
   - **Bing Webmaster Tools** — do it, but the reason is NOT Bing's own traffic: **Bing's index powers ChatGPT Search, Copilot and DuckDuckGo**, so it is an AI-SEO lever. Fastest setup is its "import from Google Search Console" path (auto-verifies and pulls the sitemap in about two clicks, no separate domain verification).
   - **Your home market's national engine**, if it has one with meaningful share (see item 4).
   - **Regional engines outside your markets — skip.** Near-zero traffic, and IndexNow already pings several of them, so discovery is covered passively with no manual account.
   - **Engines requiring in-country hosting or licensing** — irrelevant unless you are actually targeting that market.
   - The registrations that ACTUALLY move modern SEO and AI visibility are authority and citation surfaces, not second-tier search engines: company databases, professional networks, Wikidata, the local business-profile product, and niche directories that rank in the money SERP (next item).
6. **Directories and listicles that rank IN your money SERP are double-value placements** — a backlink AND a presence on the SERP itself. In this run, an industry newsletter's listicle held position #1 for the head term and a niche directory held #10 for a second money term; being listed on either put the brand on the SERP without ranking for it. When a live-SERP check (Job 5) surfaces one, it goes to the TOP of the backlink-gap outreach table.
7. **Per-money-page AI-extractability kit** (implemented once, reused): definition block in the first 300 words, FAQ section with FAQPage JSON-LD, one comparison table (this vs alternatives vs doing nothing), synonym-first title. This is the P4.S3 hardening default for every persona/service page.

## Cost discipline (pay-per-call, no subscription)

| Tier | Calls | ~Cost |
|---|---|---|
| **Cheap** (default, run freely) | all `/v3/dataforseo_labs/*` (incl. `search_intent`, `bulk_keyword_difficulty`), `/v3/keywords_data/*` | ~$0.01-0.05/call |
| **Moderate** | `/v3/serp/google/organic/live/advanced` (live), `/v3/on_page/*`, `/v3/ai_optimization/llm_mentions/*` | ~$0.002-0.02/result set, live SERP ~$0.002/SERP but per-keyword |
| **Heavier** | `/v3/backlinks/backlinks/live`, `/v3/backlinks/referring_domains/live`, `/v3/backlinks/domain_intersection/live` at high limits | scale with `limit` — set `limit: 100-300`, not 1000+ |

Costs are the provider's own pay-per-call pricing in USD, quoted at the time of writing — check current rates before budgeting.

Rules: (1) batch keywords into single calls wherever the tool takes arrays; (2) set an explicit `limit` on backlink calls; (3) check the account balance before a full multi-competitor + backlink sweep — a 14-competitor deep pass needs roughly $10-20 on the account, while per-page keyword research runs on about $1; (4) save every raw response to disk inside the step's own output folder (`<step-folder>/raw/<competitor-slug>/<date>/*.json`) so a re-run reads the file instead of re-paying.
