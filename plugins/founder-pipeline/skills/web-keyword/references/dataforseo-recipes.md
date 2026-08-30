# Keyword-data provider recipes

Endpoints, parameters, batching and cost discipline.

**This file is written against DataForSEO**, the default provider for this pipeline and the source
of every endpoint name below. It is one worked example of a *capability*, not a requirement: the
skill needs a provider that returns search volume, CPC, keyword difficulty, search intent, trend
history and live SERP results for a named location and language, and any provider covering those
substitutes. If you swap providers, the method is unchanged — the endpoint names, the batching
limits and the cost tiers are what you re-derive from your own vendor's documentation.

If your provider is missing a layer (live SERP, related queries, a non-Google engine), that layer
is **unmeasured** and is reported as unmeasured. It is never reported as zero.

Tool names below are the DataForSEO MCP server's; REST paths are given where the two differ
meaningfully.

## Access

Prefer the provider's MCP server if it has one — for DataForSEO that is `dfs-mcp`. Otherwise call
the REST API, reading credentials from your environment or secrets store rather than hard-coding
them. If you load them from a dotenv-style file, note that in most shells a plain source makes a
variable available to the current shell only; a child process reading `process.env` needs the
variables actually exported.

DataForSEO's docs are fetchable in-session: `mcp__dfs-mcp__docs_search` with a path like
`keywords_data/google_trends/explore/live`.

## Location and language

Every call is scoped to one **territory** — a location plus a language code — as decided by the
locale decision in `SKILL.md`. There is no global default and you should not invent one.

**Run every territory as a separate call.** Volumes and SERPs differ completely between markets;
a combined call averages two markets into a number describing neither.

Pull the canonical location name from the endpoint's own locations list rather than guessing.
Mismatched location names fail loudly on some endpoints and silently return global data on others,
and the silent case is the one that poisons a report. The common name is often not the API's name —
DataForSEO, for instance, takes `Czechia` and rejects `Czech Republic`.

Worked example, for a business whose home market is Czechia and whose export market is English:

| Territory | `location_name` | `language_code` |
|---|---|---|
| Home — Czechia | `Czechia` — **the API rejects "Czech Republic"** | `cs` |
| Neighbouring market — Slovakia | `Slovakia` | `sk` |
| Export — global English | `United States` (largest EN corpus) or `United Kingdom` | `en` |

Substitute your own pair. Note that `sk` is listed separately rather than folded into `cs`: closely
related languages are separate markets with separate volumes, and merging them is the single most
common way a territory table goes wrong.

## Core recipes

### Volume, CPC, competition — the canonical numbers

`kw_data_google_ads_search_volume` — batches up to ~1000 keywords per call. This is the number
everything else is judged against. Batch aggressively; the cost is per call, not per keyword.

### Expansion — catching phrasings nobody guessed

`dataforseo_labs_google_keyword_suggestions` (phrase-match expansions),
`dataforseo_labs_google_related_keywords` (semantic neighbours),
`dataforseo_labs_google_keyword_ideas` (category-based).

Run these on a *small* number of head seeds, not the whole set — they fan out fast. Filter results
to a volume floor before doing anything with them.

Note on `keyword_ideas`: its category algorithm can return off-topic noise in niche B2B verticals.
If the output is visibly unrelated to the seed, discard it and say so rather than filtering it into
something that looks plausible.

### Difficulty and intent — survivors only

`dataforseo_labs_bulk_keyword_difficulty` — 0-100, batched.
`dataforseo_labs_search_intent` — informational / commercial / transactional / navigational.

Run both only on keywords that survived the volume cut. Intent is the one that decides page type:
it separates people buying a course from people hiring a person, which look identical in a keyword
list and convert completely differently.

### Trends — direction and, more importantly, real phrasing

`kw_data_google_trends_explore` (REST: `keywords_data/google_trends/explore/live`).

- Max **5 keywords** per call; values are relative to the highest term in the call, so a call's
  numbers are only comparable *within* that call.
- `type`: `web` (default), `news`, `youtube`, `images`, `froogle`.
- Time: `date_from`/`date_to`, or `time_range` presets (`past_12_months`, `past_5_years`,
  `2004_present`). Explicit dates override `time_range`.
- Historical data starts 2004-01-01 for `web`, 2008-01-01 for other types.

**`item_types` is the setting that matters most:**

- `google_trends_graph` (default) — the trend line
- `google_trends_map` — regional breakdown
- `google_trends_topics_list` / `google_trends_queries_list` — **top and rising related queries**

The related-queries lists require **one keyword per call**. Spend the extra calls. This is the
closest thing available to hearing the market speak in its own words, as opposed to confirming or
denying the words you thought to ask about. Rising queries in particular surface phrasing that
hasn't reached anyone's keyword list yet.

Trends is capacity-limited globally by Google, so spread large jobs and expect occasional
collection errors rather than treating a failure as a zero.

### Live SERP — the validation gate

`serp_organic_live_advanced` (REST: `serp/google/organic/live/advanced`), correct location and
language, depth 20 is usually enough.

Per keyword record: does the top 10 match the intent you assigned; who ranks; which SERP features
are present (AI Overview, featured snippet, People-also-ask, local pack, video); and whether it's
beatable or a wall of high-authority domains.

Directories and listicles that rank *in* a money SERP are double-value: a backlink and a presence
on the SERP itself. When one appears, it belongs at the top of any outreach list.

### Rankings and gap

`dataforseo_labs_google_ranked_keywords` — every keyword a domain ranks for, with position and URL.
Run on your own domain and on each competitor.

`dataforseo_labs_google_domain_intersection` — shared keywords with both positions side by side.
The uncontested-territory finder.

`dataforseo_labs_google_historical_rank_overview` — trajectory, for telling a rising competitor
from a fading one.

**Labs index artifacts:** a domain can show zero ranked keywords in a small-market Labs index while
demonstrably ranking on the live SERP. The Labs index is a sample, not the truth. When Labs says
zero and the live SERP says position 1, the live SERP wins — record it as an index artifact rather
than a ranking finding.

### AI search

`ai_optimization_keyword_data_search_volume` — how often phrasings are asked of models.
`ai_opt_llm_ment_search` — where a brand or domain appears in LLM answers.
`ai_opt_llm_ment_top_domains` / `ai_opt_llm_ment_top_pages` — who wins the answers in a topic.
`ai_optimization_llm_response` — the live answer, with sources.

Model answers are non-deterministic. A single probe is an anecdote; re-run anything you intend to
report as a finding, and flag disagreement between runs rather than picking the convenient one.

## Cost discipline

Figures are DataForSEO's published list prices in USD at the time of writing, given as orders of
magnitude rather than a quote. Check your own provider's current pricing; the *relative* tiers are
the part that transfers.

| Tier | Calls | Rough cost |
|---|---|---|
| Cheap — run freely | all `dataforseo_labs_*`, `search_intent`, `bulk_keyword_difficulty`, `kw_data_*` | ~$0.01-0.05/call |
| Moderate | `serp_organic_live_advanced`, `on_page_*`, `ai_opt_llm_ment_*` | ~$0.002/SERP, but per keyword |
| Heavier | `backlinks_*` at high limits | scales with `limit` — set 100-300, not 1000+ |

Rules:

1. **Batch wherever the endpoint takes an array.** Cost is per call.
2. **Save every raw response to disk**, dated, so a re-run reads the file instead of re-paying.
   Convention: a `raw/` folder beside the report, named `<endpoint>_<territory>_<date>.json`.
3. **Log the cost reported by each response** and report the total. DataForSEO returns it in a
   `cost` field on every response; most providers expose an equivalent.
4. **Check the balance** before a large multi-competitor sweep. Keyword research for a single page
   runs on roughly one unit of currency; a deep competitor-plus-backlink pass wants ten to twenty
   available. Running out mid-sweep leaves a half-measured report, which is worse than not starting.

## Reporting rules

Every number carries `[source: <endpoint>, YYYY-MM-DD]`. A figure with no source is a guess wearing
a number's clothes.

A failed call is reported as a failed call. If an endpoint errored, a market has no API coverage,
or a limit was hit, say which and why. **Unmeasured is never reported as zero** — a zero is a
finding about the market, an unmeasured layer is a finding about the instrument, and merging them
manufactures conclusions.
