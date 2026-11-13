# Bot access check (Mode 1, Step 1)

This file belongs to the `ai-seo` skill.

First: confirm AI crawlers can access your site. This plugin does not ship a robots.txt policy
skill, so the working bot taxonomy is inlined here. Sort every user-agent into one of four tiers
and decide the tier, not the individual bot:

| Tier | What it is | Default |
|---|---|---|
| 1 — classic search | `Googlebot`, `Bingbot`, `Seznambot` and your market's equivalents | Always allow. Blocking one of these is never the right answer |
| 2 — **AI retrieval** | `OAI-SearchBot`, `ChatGPT-User`, `Claude-SearchBot`, `Claude-User`, `PerplexityBot`, `Perplexity-User`, `Google-Extended`, `Applebot-Extended`, `DuckAssistBot`, `MistralAI-User`, `Meta-ExternalFetcher` | Always allow. **These are the crawlers that produce citations** |
| 3 — AI training | `GPTBot`, `ClaudeBot`, `anthropic-ai`, `CCBot`, `Bytespider` | Allow by default; blocking is a deliberate business trade, not a fix |
| 4 — scrapers and SEO tools | commercial crawlers with no user-facing surface | Operator's call. Nothing in this skill depends on them |

**The fact that trips up most audits: training bots ≠ search bots.** Blocking `GPTBot` (training) does **nothing** to `OAI-SearchBot` (retrieval — the crawler that actually produces ChatGPT citations). They're different crawlers with different jobs, not "often the same crawl." Same split on Anthropic: `ClaudeBot` (training) vs `Claude-SearchBot` / `Claude-User` (retrieval). Field data: 79% of publishers block a training bot, and 71% *also* block a retrieval bot by mistake [Zhao & Berman, Rutgers/Wharton].

**Check robots.txt** at `yourdomain.com/robots.txt`. If any Tier 2 agent is blocked, flag it immediately — that's an immediate visibility killer for that platform.

Don't flag Tier 3 as a fix unless the operator has deliberately decided to trade training exposure for a traffic cost (Zhao & Berman: blocking AI crawlers costs ~−7% weekly human-only traffic within 6 weeks, without reliably preventing citation).

**A robots.txt read is not enough on its own.** It misses edge-level blocks — WAF rules, bot-fight
modes, CDN challenges — that return 403 to a crawler the file explicitly allows. Verify delivery by
fetching the URL *as* each Tier 2 user-agent and asserting a 200 with real content in the body.
`seo_checker.py`'s `crawler_fetch` check does exactly this for GPTBot and Googlebot:
`python3 "${CLAUDE_PLUGIN_ROOT}/skills/seo-audit/scripts/seo_checker.py" --url <url> --json`.
