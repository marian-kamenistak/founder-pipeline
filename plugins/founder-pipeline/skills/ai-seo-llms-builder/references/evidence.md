# The evidence base

Researched 2026-08-06. Kept here so the "does llms.txt help us rank" question is settled from data
rather than re-argued from vibes every few months. If you update this, date the change.

## Does llms.txt drive AI citations? No.

| Source | Finding |
|---|---|
| Google, generative-AI search guide (published 15 May 2026, updated 15 Jun 2026) | You do not need machine-readable files, AI text files or Markdown to appear in Search including its generative features. Has a "Mythbusting generative AI search" section that names llms.txt and content chunking. |
| SE Ranking, ~300,000 domains | ~10% adoption. Neither a statistical model nor an XGBoost classifier found correlation with AI citations. **Removing the variable improved model accuracy.** Adoption was flat across traffic tiers (9.88% low, 10.54% mid, 8.27% high), so it is not something high performers pioneered. |
| Ahrefs, 137,210 domains | **97% saw zero requests** for the file in May 2026. Of the 3% fetched, only 19.5% of requests came from named AI tools. |
| Provider commitments | As of Q1 2026 no major provider (OpenAI, Google, Anthropic, Meta, Mistral) had publicly committed to reading or acting on it in production. GPTBot fetches it occasionally; that is not evidence it influences sourcing or ranking. |
| Controlled studies | None showing a citation lift. In the case studies that claim one, the file shipped alongside content restructuring, technical fixes or link acquisition, any of which explains the result. |

## Where it does pay off

Agentic and developer tooling. The two named fetchers in Ahrefs' data are GPTBot and **Claude Code**.
Stripe, Vercel, Cloudflare, Anthropic and Mastercard ship the file for coding agents and agentic
browsers. For anything with programmatic consumers, an `llms-full.txt` measurably improves token
efficiency: one clean markdown file instead of scraping HTML.

The concrete return: an agent asked "what does a partnership with you cost" reads your real per-item
prices out of the file instead of guessing from a nav. That is what the work buys.

## What the community skills concluded independently

Neither is installed. Both worth learning from.

| Skill | Position on llms.txt |
|---|---|
| [claude-seo](https://github.com/AgricIDaniel/claude-seo) (25 sub-skills, 18 agents) | Explicitly rejects "llms.txt as a citation lever" as one of three influencer myths. Scores passage citability, question-based heading hierarchy, attribution density and entity presence instead. |
| [claude-seo-ai](https://github.com/Hainrixz/claude-seo-ai) | Generates it but **scores it 0**, labelled low/uncertain impact. Best safety rails of the group: dry-run default, unified-diff preview, git-aware, refuses a dirty tree. |
| A third group generate llms.txt and apply GEO tactics from the KDD 2024 study | Useful patterns, but check the plumbing before trusting the headline: several ship an "AI visibility score" that calls a vendor backend rather than actually querying ChatGPT, Claude, Gemini or Perplexity. **Any visibility number you did not watch being measured is a marketing number** — verify what a tool queries before you report its score to anyone. |

Browser validators ([llms-txt.io](https://llms-txt.io/validator), [Spindora](https://www.spindorai.com/en/llms-txt-kontrol-araci),
[RankRay](https://rankray.com/free-seo-tools/llms-txt-checker/), [Rankability](https://www.rankability.com/tools/llms-txt-generator/))
all test spec compliance only, no CI. Fine as a 60-second second opinion; `scripts/validate_llms.py`
does the same checks plus our house rules and runs in a pipeline.

## What to do instead, ranked

1. **Earn mentions elsewhere.** ~82% of AI citations come from earned media [Muck Rack, 25M+ links];
   brand mentions correlate more strongly with AI visibility than backlinks do [operating assumption
   — see the caveat in `geo-extractability.md`].
2. **Be in Bing's index.** ChatGPT's retrieval leans on it heavily. `/founder-pipeline:web-indexation` owns this.
3. **Make the page quotable.** Quotes, statistics, cited sources. See `geo-extractability.md`.
4. **Then** ship a good llms file, for the agents.

## Sources

- https://baselinelabs.ai/blog/llms-txt-google-search
- https://ariashaw.com/does-llms-txt-actually-work
- https://organikpi.com/blog/distribution/llms-txt-adoption-impact/
- https://livegodigital.com/the-great-llms-txt-confusion-of-2026/
- GEO: Generative Engine Optimization, KDD '24 — https://arxiv.org/pdf/2311.09735
- https://www.omnibound.ai/blog/generative-engine-optimization-statistics
