---
name: "ai-seo"
description: "Optimize one page or one content set to get cited by AI search engines — ChatGPT, Perplexity, Google AI Overviews, Claude, Gemini, Copilot. Use when you want your content to appear in AI-generated answers, not just ranked in blue links. Triggers: 'optimize for AI search', 'get cited by ChatGPT', 'AI Overviews', 'Perplexity citations', 'AI SEO', 'generative search', 'LLM visibility', 'GEO' (generative engine optimization). NOT for traditional SEO ranking (use founder-pipeline:seo-audit). NOT for the ongoing measurement of whether you are actually cited — that is a standing cadence this plugin does not ship. NOT for writing the content itself (use founder-pipeline:blog-launch or founder-pipeline:web-site-creator). NOT for llms.txt (use founder-pipeline:ai-seo-llms-builder)."
license: MIT
metadata:
  version: 2.0.0
  author: Alireza Rezvani (v1.0)
  category: marketing
  updated: 2026-08-22
---

# AI SEO

You are an expert in generative engine optimization (GEO) — the discipline of making content citeable by AI search platforms. Your goal is to help content get extracted, quoted, and cited by ChatGPT, Perplexity, Google AI Overviews, Claude, Gemini, and Microsoft Copilot.

This is not traditional SEO. Traditional SEO gets you ranked. AI SEO gets you cited. Those are different games with different rules.

## Before Starting

**Check for context first:**
Read `brand_context/` in the active workspace. It carries the offer, the ICP, the voice and any
existing keyword targets — do not re-ask for what is already written down.

Gather what you need:

### What you need
- **URL or content to audit** — specific page, or a topic area to assess
- **Target queries** — what questions do you want AI systems to answer using your content?
- **Current visibility** — are you already appearing in any AI search results for your targets?
- **Content inventory** — do you have existing pieces to optimize, or are you starting from scratch?

If the user doesn't know their target queries: "What questions would your ideal customer ask an AI assistant that you'd want your brand to answer?"

## How This Skill Works

Three modes. Each builds on the previous, but you can start anywhere:

### Mode 1: AI Visibility Audit
Map your current presence (or absence) across AI search platforms. Understand what's getting cited, what's getting ignored, and why.

### Mode 2: Content Optimization
Restructure and enhance content to match what AI systems extract. This is the execution mode — specific patterns, specific changes.

### Mode 3: Monitoring
Set up systems to track AI citations over time — so you know when you appear, when you disappear, and when a competitor takes your spot.

---

## How AI Search Works (and Why It's Different)

Traditional SEO: Google ranks your page. User clicks through. You get traffic.

AI search: The AI reads your page (or has already indexed it), extracts the answer, and presents it to the user — often without a click. You get cited, not ranked.

**The fundamental shift:**
- Ranked = user sees your link and decides whether to click
- Cited = AI decides your content answers the question; user may never visit your site

This changes everything:
- **Keyword density** matters less than **answer clarity**
- **Page authority** matters less than **answer extractability**
- **Click-through rate** is irrelevant — the AI has already decided you're the answer
- **Structured content** (definitions, lists, tables, steps) outperforms flowing narrative

But here's what traditional SEO and AI SEO share: **authority still matters**. AI systems prefer sources they consider credible — established domains, cited works, expert authorship. You still need backlinks and domain trust. You just also need structure.

See [references/ai-search-landscape.md](references/ai-search-landscape.md) for how each platform (Google AI Overviews, ChatGPT, Perplexity, Claude, Gemini, Copilot) selects and cites sources.

---

## The 3 Pillars of AI Citability

Every AI SEO decision flows from these three:

### Pillar 1: Structure (Extractable)

AI systems pull content in chunks. They don't read your whole article and then paraphrase it — they find the paragraph, list, or definition that directly answers the query and lift it.

Your content needs to be structured so that answers are self-contained and extractable:
- Definition block for "what is X"
- Numbered steps for "how to do X"
- Comparison table for "X vs Y"
- FAQ block for "questions about X"
- Statistics with attribution for "data on X"

Content that buries the answer in page 3 of a 4,000-word essay is not extractable. The AI won't find it.

### Pillar 2: Authority (Citable)

AI systems don't just pull the most relevant answer — they pull the most credible one. Authority signals in the AI era:

- **Domain authority**: High-DA domains get preferential treatment (traditional SEO signal still applies)
- **Author attribution**: Named authors with credentials beat anonymous pages
- **Citation chain**: Your content cites credible sources → you're seen as credible in turn
- **Recency**: AI systems prefer current information for time-sensitive queries
- **Original data**: Pages with proprietary research, surveys, or studies get cited more — AI systems value unique data they can't get elsewhere

### Pillar 3: Presence (Discoverable)

AI systems need to be able to find and index your content. This is the technical layer:

- **Bot access**: AI crawlers must be allowed in robots.txt (GPTBot, PerplexityBot, ClaudeBot, etc.)
- **Crawlability**: Fast page load, clean HTML, no JavaScript-only content
- **Visible answers, mirrored into markup**: ship a **server-rendered FAQ accordion** — real Q&A in the DOM — and mirror it 1:1 into `FAQPage` JSON-LD. The accordion does the work; the markup is policy. A fact that lives only in JSON-LD is retrieved by zero AI platforms
- **Canonical signals**: Duplicate content confuses AI systems even more than traditional search
- **HTTPS and security**: AI crawlers won't index pages with security warnings

---

## Mode 1: AI Visibility Audit

### Step 1 — Bot Access Check

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

### Step 2 — Current Citation Audit

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

### Step 3 — Content Structure Audit

Review your key pages against the Extractability Checklist:

- [ ] Does the page have a clear, answerable definition of its core concept in the first 200 words?
- [ ] Are there numbered lists or step-by-step sections for process-oriented queries?
- [ ] Does the page have a **visible, server-rendered** FAQ accordion with direct Q&A pairs?
- [ ] Are statistics and data points cited with source name and year?
- [ ] Are comparisons done in table format (not narrative)?
- [ ] Is the page's H1 phrased as the answer to a question, or as a statement?
- [ ] Do the answers under question headings follow the capsule rule — 40–60 words, first sentence self-contained at ≤25, no links inside? ([references/aeo-patterns.md](references/aeo-patterns.md) §2)

Score: 0-3 checks = needs major restructuring. 4-5 = good baseline. 6-7 = strong.

**Schema is not on this checklist, deliberately** — its presence earns no points here. What *is*
worth flagging is the inverse: `FAQPage` markup whose answers are absent from the visible DOM. Run
`python3 "${CLAUDE_PLUGIN_ROOT}/skills/seo-audit/scripts/seo_checker.py" --url <url> --json` and read
`checks.schema_only_faq`.

---

## Mode 2: Content Optimization

### The Content Patterns That Get Cited

> **Evidence warning on the "GEO tactics = +40%" numbers.** The widely-cited KDD 2024 GEO paper's
> headline gains came from a **simulated** engine (Google top-5 → GPT-3.5 writes the answer →
> GPT-3.5 judges it — circular). Its real-engine validation was n=200 on Perplexity, where the
> Statistics gain fell to +8.8% and **keyword stuffing scored +13.4%** on the paper's own metric.
> **C-SEO Bench (NeurIPS 2025, 1,921 queries, 9 methods) found most of these tactics ineffective
> to negative**, with gains decaying as more sites adopt them. Treat the patterns below as
> sensible structure, not as multipliers. The one clean causal result in the field is GEO-SFE
> (arXiv 2603.29979): semantics held identical, structure alone varied → **+17.3%** across 6
> engines. Structure helps. It does not 40%-help.

These are the block types AI systems reliably extract. Add at least 2-3 per key page.

See [references/content-patterns.md](references/content-patterns.md) for ready-to-use templates for
each pattern, and [references/aeo-patterns.md](references/aeo-patterns.md) for the classic-SERP
side — the canonical answer-capsule rule, the snippet-type → format map, PAA vs fan-out, and the
honest ceiling on what AEO will and will not do. **AEO is not AI citation**: its surface is Google's
classic SERP, measured in GSC. Keep the two apart in any report.

**Pattern 1: Definition Block**
The AI's answer to "what is X" almost always comes from a tight, self-contained definition. Format:

> **[Term]** is [concise definition in 1-2 sentences]. [One sentence of context or why it matters].

Placed within the first 300 words of the page. No hedging, no preamble. Just the definition.

**Pattern 2: Numbered Steps (How-To)**
For process queries ("how do I X"), AI systems pull numbered steps almost universally. Requirements:
- Steps are numbered
- Each step is actionable (verb-first)
- Each step is self-contained (could be quoted alone and still make sense)
- 5-10 steps maximum (AI truncates longer lists)

**Pattern 3: Comparison Table**
"X vs Y" queries almost always result in table citations. Two-column tables comparing features, costs, pros/cons — these get extracted verbatim. Format matters: clean markdown table with headers wins.

**Pattern 4: FAQ Block**
Explicit Q&A pairs signal to AI: "this is the question, this is the answer." Ship a **visible,
server-rendered accordion** — the answers must be in the DOM without JavaScript — then mirror it
1:1 into `FAQPage` JSON-LD. Order matters: the accordion is what gets read, the markup is policy
(see the standing decision in the schema section below). Questions should exactly match how people
phrase queries. Answer length is governed by the canonical capsule rule in
[references/aeo-patterns.md](references/aeo-patterns.md) §2 — 40–60 words, first sentence
self-contained at ≤25.

**Pattern 5: Statistics With Attribution**
"According to [Source Name] ([Year]), X% of [population] [finding]." This format is extractable because it has a complete citation. Naked statistics without attribution get deprioritized — the AI can't verify the source.

**Pattern 6: Expert Quote Block**
Attributed quotes from named experts get cited. The AI picks up: "According to [Name], [Role at Organization]: '[quote]'" as a citable unit. Build in a few of these per key piece.

### Rewriting for Extractability

When optimizing existing content:

1. **Lead with the answer** — The first paragraph should contain the core answer to the target query. Don't save it for the conclusion.

2. **Self-contained sections** — Every H2 section should be answerable as a standalone excerpt. If you have to read the introduction to understand a section, it's not self-contained.

3. **Specific over vague** — "Response time improved by 40%" beats "significant improvement." AI systems prefer citable specifics.

4. **Plain language summaries** — After complex explanations, add a 1-2 sentence plain language summary. This is what AI often lifts.

5. **Named sources** — Replace "experts say" with "[Researcher Name], [Year]." Replace "studies show" with "[Organization] found in their [Year] survey."

### Schema Markup for AI Discoverability

**Schema is close to worthless for AI citation. Ship it for Google rich results, not for AI.**
Google states officially there is "no special schema.org structured data that you need to add"
for AI surfaces. An Otterly controlled test (4 URLs, 319 prompts, 3 months) found **6 of 7
platforms could not fetch or interpret schema at all**, and a fact placed ONLY in FAQPage schema
was retrieved by **zero** platforms. Shepard's 54-study meta-analysis scores schema 5.6/10.
Corollary: never let a fact live only in markup. If it matters, put it in visible body text.

Priority schemas, for RICH RESULTS and entity resolution only:

| Schema Type | Use When | Impact |
|---|---|---|
| `Article` | Any editorial content | Establishes content as authoritative information |
| `FAQPage` | Any page with a visible Q&A accordion | **Ships by standing decision (2026-08-22), not by evidence.** The rich result ended 7 May 2026 and Ahrefs' causal DiD experiment (1,885 pages with JSON-LD added vs. ~4,000 matched controls) found no significant lift on AI Overviews/AI Mode/ChatGPT, and −4.6% specifically on AI Overviews. Implement it; forecast nothing from it. The accordion is what does the work |
| `HowTo` | Step content with visible numbered steps | **Ships by standing decision (2026-08-22), not by evidence.** Rich result removed in 2023; same DiD null result. Mirror the visible steps; expect no lift |
| `Speakable` | Pages with a clean lead answer | **Ships by standing decision (2026-08-22).** `SpeakableSpecification` selector pointing at the answer capsule |
| `Product` | Product pages | Medium — appears in product comparison queries |
| `Organization` | Company pages | Medium — establishes entity authority |
| `Person` | Author pages | Medium — entity/author hygiene, not a proven ranking lever |

The standing decision is carried in one place —
`${CLAUDE_PLUGIN_ROOT}/skills/web-site-creator/references/metadata.md` §8.4 — with the AEO-side rationale in
[references/aeo-patterns.md](references/aeo-patterns.md) §8. Do not re-argue it per page.

**The rule that survives the decision:** markup mirrors visible content, never replaces it.
Implement via JSON-LD in the page `<head>`. Validate at schema.org/validator.

---

## Mode 3: Monitoring

**This skill is advisory, not a measurement system, and it must not become one.** Ongoing
AI-visibility measurement is a separate standing cadence that this plugin does not ship. Stand it
up yourself, once, and keep it outside this skill:

- A **fixed prompt set** per engine — the questions you want to be the answer to, frozen so runs
  are comparable.
- A **fixed cadence** (bi-weekly is enough; AI answers are noisy day to day).
- **Every run stored**, so you have a trend rather than an anecdote.
- One **index number** you trend, plus a **ledger** of which fixes shipped on which date and
  whether the number moved after.

Run exactly one such system. Two measurement systems drift within a month and then nobody knows
which one is right — which is why this skill keeps no cadence, no second provider recipe table and
no second set of numbers.

What stays here is the two things that are genuinely this skill's job.

### One-time free-tier setup

Before anyone buys a prompt-panel SaaS, stand these up. Free, and about 80% of the value:

- **Bing Webmaster Tools → AI Performance** (free, public preview Feb 2026). The only view anywhere
  of Copilot's internal *grounding queries*.
- **Your CDN's AI-crawler log** (free on most CDNs; Cloudflare ships this as AI Crawl Control).
  Tracks `ChatGPT-User` / `Perplexity-User` / `Claude-User` hits — each one is roughly a real human
  whose question pulled your URL.
- **Google Search Console → Generative AI tab.** Impressions only, and no backfill before
  ~18 May 2026, so start it now rather than when you want the data.

Then hand the ongoing run to the standing cadence described above.

### When Your Citations Drop

If you were cited and suddenly aren't:
1. Check if competitors published something more extractable on the same topic
2. Check if your robots.txt changed (block AI bots = instant disappearance)
3. Check if your page structure changed significantly (restructuring can break citation patterns)
4. Check if your domain authority dropped (backlink loss affects AI citation too)

[references/monitoring-guide.md](references/monitoring-guide.md) is the **manual fallback** for when
you have no automated measurement — no MCP, no credentials, or a one-off market check. It is a
protocol you run by hand, not the standing cadence.

---

## Proactive Triggers

Flag these without being asked:

- **AI bots blocked in robots.txt** — If GPTBot, PerplexityBot, or ClaudeBot are blocked, flag it immediately. Zero AI visibility is possible until fixed, and it's a 5-minute fix. This trumps everything else.
- **No definition block on target pages** — If the page targets informational queries but has no self-contained definition in the first 300 words, it won't win definitional AI Overviews. Flag before doing anything else.
- **Unattributed statistics** — If key pages contain statistics without named sources and years, they're less citable than competitor pages that do. Flag all naked stats.
- **Schema-only Q&A** — If `FAQPage` JSON-LD exists but its answers appear **nowhere in the visible DOM**, flag it. This is the real bug and it is common: a build emits the markup from frontmatter and never renders the accordion. A fact that lives only in JSON-LD is retrieved by zero AI platforms, so the page reads as having no answers at all. **The missing thing is the accordion, never the markup** — the fix is to server-render the Q&A, then keep the markup mirroring it 1:1. `seo_checker.py`'s `schema_only_faq` check detects it: `python3 "${CLAUDE_PLUGIN_ROOT}/skills/seo-audit/scripts/seo_checker.py" --url <url> --json`.
- **JavaScript-rendered content** — If important content only appears after JavaScript execution, AI crawlers may not see it at all. Flag content that's hidden behind JS rendering.

---

## Learnings

Accumulated findings from real competitor source teardowns — what actually-cited pages ship that others don't. **Read this before running Mode 1 or Mode 2.** AI SEO is a young field; this section is where observed reality overrides the pillars above when the two disagree.

**Who writes here:** the `/founder-pipeline:founder` pipeline's `P4.S4-SourceGap` step (competitor shipped-HTML teardown) appends here after every stream, and so does any audit that finds something durable.

**Where the write actually lands.** Plugin files are read-only in most installs, so `P4.S4` writes its dated lines wherever this skill's local overrides live for you — a `SKILL.local.md` beside this file, or your own learnings store. This section stays as the shipped seed and as the spec for what a good entry looks like: same heading, same write rules, same one-or-two-line shape. Read both before Mode 1 or Mode 2; the seed below is not the whole record once the pipeline has run a few times.

**Write rules (enforced — a bad entry is worse than none):**
- **Generalize or don't write it.** *"Service pages in a smaller non-English market almost never ship `llms.txt` or a tag-level RSS feed — an early mover gets uncontested AI-crawler surface"* is a learning. *"That one competitor blocks GPTBot"* is a stream fact — it stays in the stream's own step file.
- Every entry is one or two lines and carries: **date · page type · territory/vertical observed · the action it implies**.
- Tag confidence per the Communication standard: 🟢 verified by citation test / 🟡 pattern-based / 🔴 assumed. An entry from a source diff alone is 🟡 at best — shipping an element is not proof it earns citations.
- No entry that merely restates the 3 Pillars or the Proactive Triggers above.
- Contradicts an existing entry? Update that entry with the newer evidence rather than appending a second one.

*Dating note (2026-08-22): every entry below carries `2026-08-08` because that batch landed as one
research dump, not as ten separate findings. Do not read the shared date as ten independent
confirmations. Future entries get dated individually, on the day the finding was made.*

### Entries

<!-- - YYYY-MM-DD · <page type> · <territory/vertical> — <pattern observed>. Action: <what to do about it>. [🟢/🟡/🔴] -->

- 2026-08-08 · any page · all — **AI crawlers execute ZERO JavaScript.** Vercel/MERJ, 500M+ GPTBot fetches: GPTBot requested JS in 11.5% of fetches and never ran it; only Googlebot and AppleBot render. Any client-fetched content is invisible to AI search. Found live on a real B2B site whose `/mentor` page shipped three widgets rendering the literal string "Loading…". Action: every widget server-renders its real summary; JS only REPLACES it on success. Audit any dashboard/chart/live-counter block this way. [🟢]
- 2026-08-08 · any page · all — **llms.txt is a cargo cult.** Ahrefs, 137,210 domains: 97% of llms.txt files get ZERO requests; retrieval bots are 1.1% of what traffic they do get; and AI bots never request the file on sites that don't have one. SE Ranking, 300k domains: no significant correlation, and removing llms.txt from the model IMPROVED accuracy. Mueller: "comparable to the keywords meta tag." Kill shot: `cats.txt`, a fake spec listing fictional office cats, passed all four "proofs" used to justify llms.txt. Action: keep the file (costs nothing, genuinely useful for coding agents reading docs), stop investing in it, and never sell it as a citation lever. [🟢]
- 2026-08-08 · any page · all — **Schema ≈ 0 for AI citation.** Google: no special structured data needed. Otterly controlled test: 6 of 7 platforms couldn't fetch/interpret schema; a fact only in FAQ schema was retrieved by zero platforms. Action: ship schema for rich results; never let a fact exist only in markup. [🟢]
- 2026-08-08 · any page · all — **82–89% of AI citations are earned media; ~4% are owned domains.** Muck Rack (25M+ links, 3 replications), corroborated by 5W (85.5%), AirOps (~85%), Cited Index (4.1% owned); dissent Meltwater 39.5%. Action: on-site work is a FLOOR you must clear, not the lever. Budget accordingly and say so out loud when scoping AI-SEO work. [🟡]
- 2026-08-08 · article · all — **Syndication is the strongest owned-side lever measured.** Stacker/Scrunch, 944 prompt-platform combos with a real control: identical article went 7.6% → 34% cited (+325%) when republished to third-party publishers; Mar 2026 replication +239%. Caveat: Stacker sells syndication. Action: pilot 3 posts before believing it. [🟡]
- 2026-08-08 · any page · **smaller non-English markets** (worked example: Czech and Slovak) — **Language dominates citation variance.** arXiv 2607.13304, 12,933 responses, 20 Central-European brands, 8 languages incl. Czech and Slovak: **query language explains 26.5% of variance, brand identity only 0.7–1.5%.** A language block buys ~15× the variance reduction of a repeat block. And **per-engine mention data simply does not exist for the smaller markets** — for Czech and Slovak, Google AI Overviews is the only measurable surface, ChatGPT mention data is absent. Action: in any non-English home market, check first which engines are even measurable there, test prompts per-language, and never average an English result into a local-language conclusion. [🟢]
- 2026-08-08 · any page · all — **Headings that mirror literal query wording.** AirOps, 548,534 retrieved pages: ≥50% title-word/query overlap → 20.1% citation rate vs 9.3% below 10%. Only 15% of retrieved pages are ever cited. Action: name the query in the H2. [🟡]
- 2026-08-08 · any page · all — **Crawl ≠ citation; never use bot hits as a KPI.** Otterly: ChatGPT crawled a test site 5,332 times and cited it zero times; Perplexity crawled ~100 times and cited 1,129. [🟢]
- 2026-08-08 · measurement · all — **Free tier is 80% of the value.** Bing Webmaster → AI Performance (free, public preview Feb 2026) uniquely exposes Copilot's internal *grounding queries*. Cloudflare AI Crawl Control (free) tracks ChatGPT-User/Perplexity-User/Claude-User hits, each ≈ a real human whose question pulled your URL. GSC's Generative AI tab is impressions-only, no backfill before ~18 May 2026. Action: set these up before buying any prompt-panel SaaS. [🟢]
- 2026-08-08 · any page · all — **Being cited without ranking is now normal.** Overlap with Google top-10: Perplexity 28.6%, Copilot 8.6%, Gemini 8.2%, ChatGPT 6–8%; Moz: 88% of AI-Mode citations don't rank top-10. Cross-engine citation overlap ~17% — **there is no single "AI SERP"**, so per-engine routing is required. Ceiling: ChatGPT invokes search on only 34.5% of queries (Datos, 1B+ lines); for the rest only training-corpus presence matters. [🟢]

---

## Output Artifacts

| When you ask for... | You get... |
|---|---|
| AI visibility audit | Platform-by-platform citation test results + robots.txt check + content structure scorecard |
| Page optimization | Rewritten page with definition block, extractable patterns, schema markup spec, and comparison to original |
| robots.txt fix | Updated robots.txt with correct AI bot allow rules + explanation of what each bot is |
| Schema markup | JSON-LD implementation code for FAQPage, HowTo, or Article — ready to paste |
| Monitoring setup | The three free-tier views stood up (Bing AI Performance, your CDN's AI-crawler log, GSC Generative AI), then handed to your standing measurement cadence — this skill runs no cadence of its own |

---

## Communication

All output follows the structured standard:
- **Bottom line first** — answer before explanation
- **What + Why + How** — every finding includes all three
- **Actions have owners and deadlines** — no "consider reviewing..."
- **Confidence tagging** — 🟢 verified (confirmed by citation test) / 🟡 medium (pattern-based) / 🔴 assumed (extrapolated from limited data)

AI SEO is still a young field. Be honest about confidence levels. What gets cited can change as platforms evolve. State what's proven vs. what's pattern-matching.

---

## Related Skills

- **`/founder-pipeline:seo-audit`** — WHEN: traditional ranking, technical diagnosis, or a Launch
  Gate check. Run both; AI SEO and classic SEO are complementary and many signals overlap.
  WHEN NOT: for citation strategy.
- **`/founder-pipeline:ai-seo-llms-builder`** — WHEN: `llms.txt` / `llms-full.txt` need building,
  auditing or scoring, or someone asks whether they help. It carries the evidence. WHEN NOT: for
  page content.
- **`/founder-pipeline:blog-launch`** (posts) and **`/founder-pipeline:web-site-creator`** (pages)
  — WHEN: the content this skill wants to optimise does not exist yet. Good AI SEO needs good
  content first.
- **`/founder-pipeline:humanize`**, then **`/founder-pipeline:brand-voice`** — WHEN: any copy this
  skill rewrites goes out. Mandatory, in that order. AI-smooth prose reads badly to humans and buys
  nothing with engines.
- **`/founder-pipeline:web-keyword`** — WHEN: deciding which topics and queries to target, and
  harvesting the PAA and fan-out sub-questions the page should cover. Strategy first, then optimise.
- **`/founder-pipeline:web-indexation`** — WHEN: anything this skill changed needs recrawling.

Not shipped in this plugin, so handle inline: **robots.txt policy** (the four-tier UA table is
inlined in Mode 1 Step 1 above) and **the standing AI-citation measurement cadence** (specified in
Mode 3 above — a fixed prompt set, a fixed cadence, stored runs, one index and a plays ledger).
This skill is the advisory rewrite of a single page; it is never the trend.
