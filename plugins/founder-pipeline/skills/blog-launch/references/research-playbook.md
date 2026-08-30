# Per-post research playbook (R1-R4)

Slimmed from `${CLAUDE_PLUGIN_ROOT}/skills/founder/references/dataforseo-playbook.md` — go there for territory tables and REST fallbacks. Budget: **~1 USD per post total** (the keyword-data vendor bills in USD regardless of your own reporting currency). Every number cited downstream carries `[source: <vendor> <tool>, <date>]`. Save every raw JSON response under the workspace `research/` folder so re-runs read disk instead of re-paying.

**Territory defaults: your home market + your primary export market** — separate calls, never mixed. Set them once in the site profile and read them from there.

> **Worked example.** A practice selling into the US in English while publishing locally in Czech runs `United States`/`en` and `Czechia`/`cs`. Note the exact location string: the API's name is `Czechia`, **not** "Czech Republic" — a wrong location name returns an empty result set rather than an error, which reads as "no search volume for this topic" and silently kills a good post idea. Check your own market's exact location string the same way before trusting a zero.

## R1 — Keywords & trends (~$0.10)

1. Seeds: from the brief + how the ICP words the problem.
2. Expand: `dataforseo_labs_google_keyword_ideas` + `_keyword_suggestions` + `_related_keywords`.
3. Volumes: `kw_data_google_ads_search_volume` (ONE batched call, all candidates).
4. Difficulty: `dataforseo_labs_bulk_keyword_difficulty` (ONE batched call).
5. Intent: `dataforseo_labs_search_intent` — a blog post wants informational/commercial; flag mismatches.
6. Trend: `kw_data_google_trends_explore` on the top 2-3 candidates (12m + 5y, territory-filtered); a declining trend is reported, not hidden.

Output schema: `{ primary: {kw, volume, difficulty, intent, trend}, secondaries: [...], rejected: [{kw, why}] }`

## R2 — SERP angles (~$0.15)

1. `serp_organic_live_advanced` for the primary keyword (correct territory/language). Record top 10 + SERP features (AI Overview, snippet, PAA).
2. `on_page_content_parsing` on the top 3 ranking posts: what they cover, their structure, their proof.
3. The deliverable is **the gap**: what do ALL of them miss that the author can say from their own first-hand track record? Also: are the top 10 beatable (DR mix) or giants?

Output: `{ top10: [...], features: [...], covered: [...], gap: [3-5 ideas], beatable: verdict, paa_questions: [...] }`

## R3 — Backlink mining (~$0.40, the heaviest — cap limits)

For the top 3 competing POSTS (URLs from R2, not domains):
1. `backlinks_backlinks` per URL, `limit: 100`, order by rank.
2. `backlinks_referring_domains` per URL, `limit: 100`.
3. Filter: spam_score ≤ 30, real pages (drop scrapers/mirrors). Classify each source: directory / listicle / newsletter / Reddit / Quora / HN / blogroll / editorial.

Output: `{ placements: [{source_url, type, links_to, why_reachable, action}], skipped_spam: n }` — this feeds step 10 directly.

## R4 — AI-search (~$0.20)

1. `ai_optimization_llm_response` (or `ai_optimization_chat_gpt_scraper`): ask the 2-3 money questions the post targets; record answers + cited sources.
2. `ai_opt_llm_ment_top_domains` + `_top_pages` for the topic: who wins LLM citations today.
3. `ai_optimization_keyword_data_search_volume` on the natural-language phrasings.

Output: `{ questions_to_answer_verbatim: [3-5], current_winners: [...], we_are_cited: bool, phrasing_volumes: [...] }` — feeds `faqs` frontmatter + the `/founder-pipeline:ai-seo` pass.

## Fallbacks

MCP server down → call the vendor's REST API directly with credentials from your secrets store, same endpoints. Both down → mark outputs `[assumption — validate in Search Console]`, continue; never invent numbers. R3 can also fall back to the raw exports of your most recent competitor audit for this site, if one is recent enough to still be true and the topic overlaps it.
