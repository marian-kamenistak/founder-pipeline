# Current citation audit (Mode 1, Step 2)

This file belongs to the `ai-seo` skill.

**Automated first, if you have a rank-data provider connected.** The worked example below is
DataForSEO's MCP server (`dfs-mcp`), an **optional dependency you install separately**; any
provider exposing equivalent LLM-mention endpoints substitutes, and the tool names change with it.
Without one, skip straight to the manual spot-check table underneath.

| Question | Tool |
|---|---|
| Where is my brand/domain mentioned in LLM answers? | `ai_opt_llm_ment_search` (query: brand or domain) |
| Which domains win AI answers in my niche? | `ai_opt_llm_ment_top_domains` (topic query) |
| Which specific pages get cited? | `ai_opt_llm_ment_top_pages` |
| What does ChatGPT actually answer for my target query, with sources? | `ai_optimization_llm_response` / `ai_optimization_chat_gpt_scraper` |
| How often are my target phrasings asked to LLMs? | `ai_optimization_keyword_data_search_volume` |

Tag results `[source: <provider> <tool>, <date>]`. Then spot-verify manually:

| Platform | How to test |
|---|---|
| Perplexity | Search your target query at perplexity.ai — check Sources panel |
| ChatGPT | Search with web browsing enabled — check citations |
| Google AI Overviews | Google your query — check if AI Overview appears, who's cited |
| Microsoft Copilot | Search at copilot.microsoft.com — check source cards |

For each query, document:
- Are you cited? (yes/no)
- Which competitors are cited?
- What content type gets cited? (definition? list? stats?)
- How is the answer structured?

This tells you the pattern that's currently winning. Build toward it.
