# Tooling and costs

What this pipeline actually needs to run, what each thing costs, and what you can skip.

All prices verified from the vendor's own pricing page on **2026-08-27**. Where a figure could not be
verified from a primary source, this document says "not available" and why — it never substitutes a
plausible-looking number. Prices change; re-check before budgeting.

---

## The short answer

| | Monthly | What you get |
|---|---|---|
| **Minimum viable** | **$27 – $37** | The full pipeline, using free tiers everywhere they genuinely suffice |
| **Comfortable** | **$205 – $233** | Paid tiers only where the free tier actually bites |
| **Per research run** | **$0.66 – $2.02** | Metered APIs for one round of keyword, SERP, backlink and social research |

Seven of the thirteen tools below run at **$0** for a solo founder. Only two costs are unavoidable:
a Claude plan (Claude Code is not on the free tier) and custom-domain email (Google Workspace has no
free tier).

If you want the cheapest useful version: **Claude Pro + a $50 DataForSEO deposit + a domain.** That
runs the whole evidence-and-kill half of the pipeline — the part that decides whether to build at
all — for about $20/month plus pennies per run.

---

## Tier 0 — you cannot run the pipeline without these

| What | Why | Cost |
|---|---|---|
| **Claude Pro or higher** | Claude Code is not included in Claude Free | **$17/mo** annual, $20 monthly |
| **A top-tier model** | The adversarial critic passes and reader-facing copy degrade badly on cheaper tiers | included in the plan |
| **You, present, to approve each step** | Every step waits for a human signature. This is not automatable and is not meant to be | free, but it is the real cost |
| **A writable folder** | One folder per idea, one file per step | free |

> **Cost trap worth knowing.** On Claude Pro, the top-tier model is credits-only from the first
> token and does not count toward your plan limits. On Max, up to half the weekly limit covers it.
> This is the sharpest hidden cost in the stack.

---

## Tier 1 — the evidence half (decide whether to build)

This is the part that earns its keep fastest. It runs on one paid API.

### DataForSEO — search demand, competitor traffic, backlinks, WHOIS

The single most load-bearing external service in the pipeline. Without it, the demand-prediction step
and the competitor-research step both fail their evidence criteria, and the keyword contract cannot
lock.

| | |
|---|---|
| Free | **$1 signup credit**, no card, no time limit, plus a free sandbox |
| Paid | Pay-per-call. **No monthly fee.** $50 minimum deposit, spendable across all endpoints |
| Keyword volumes | **$0.06 per task**, up to 1,000 keywords in that one task |
| SERP (Google organic) | $0.0006 standard / $0.002 live, per result page |
| Backlinks | $0.024/request + $0.000036/row |

**One realistic research run** — 200 keyword volumes, 20 SERP checks, 5 backlink summaries:

```
keywords   1 task × $0.06                = $0.060
SERP       20 × $0.0006                  = $0.012
backlinks  5 × ($0.024 + 1 row)          = $0.120
                              standard   = $0.19
                              live mode  = $0.25
                     live, full depth    = $0.61
```

A **$50 deposit buys roughly 200–260 runs of that shape.** Running one every day for a year still
does not exhaust the minimum deposit.

*Source: [dataforseo.com/pricing](https://dataforseo.com/pricing), accessed 2026-08-27.
Per-endpoint backlink rates beyond the two above: not available — the pricing page does not break
them out.*

---

## Tier 2 — the selling half

| Tool | Free tier | First paid | What a founder needs |
|---|---|---|---|
| **A CRM** (Attio used as the worked example) | 3 seats, 50,000 records, **full API access on free** | €39/user/mo monthly, €31 annual | **€0.** Free covers three people with the API |
| **Product analytics** (PostHog) | 1M events, 5K replays, 1M flag requests — **every month**, and ingestion stops rather than billing you | pay-as-you-go, no plan fee, no seat fee | **$0.** Generous enough to skip paid entirely |
| **Lead enrichment** (Apollo) | 900 credits/seat/year (75/mo) | $49/seat/mo annual, $69 monthly | Free is a demo, not a pipeline. $49 if enrichment is load-bearing |

*Sources: [attio.com/pricing](https://attio.com/pricing) · [posthog.com/pricing](https://posthog.com/pricing) ·
[apollo.io/pricing](https://www.apollo.io/pricing), all accessed 2026-08-27.*

> **Two things the vendors do not make obvious.** Attio's pricing page is EUR-locked from Europe with
> no currency switcher — a USD figure is **not available** from the primary source, and third-party
> trackers disagree, so none is quoted here. Apollo's page contradicts itself on whether the API
> works on the free plan: the comparison table ticks it, the FAQ on the same page says it is
> custom-plan only. Treat API-on-free as claimed but unreliable.

---

## Tier 3 — the building and launching half

| Tool | Free tier | First paid | What a founder needs |
|---|---|---|---|
| **Cloudflare** (DNS, Workers, Pages) | 100,000 requests/day, free unlimited egress, free DNS/SSL | Workers Paid **$5/mo** | **$0** until you exceed 100k requests/day or need more than 10 ms CPU per invocation |
| **Domain registration** | — | .com **$10.46/yr**, .io **$50/yr** at Cloudflare | Cloudflare sells at cost with no markup, and renewal equals registration |
| **Google Workspace** | none for custom-domain email | **Business Starter $7/user/mo** annual, $8.40 flexible | Starter, one seat. Up to 20 alias domains ride free — a second brand's email costs nothing extra |
| **Transactional email** (Resend) | 3,000/mo, **100/day cap**, 3 domains | Pro $20/mo — 50,000, no daily cap | **$0.** The daily cap bites before the monthly one |
| **Scraping** (Firecrawl) | 1,000 credits/mo, no card | Hobby $19/mo ($16 annual) — 5,000 | **$0** unless you crawl whole competitor sites |
| **Task board** (Notion) | unlimited blocks **solo**, API included | Plus $12/member/mo, $10 annual | **$0** solo; $10/user the moment a second person joins |

*Sources: [Cloudflare Workers pricing](https://developers.cloudflare.com/workers/platform/pricing/) ·
[Cloudflare Registrar](https://www.cloudflare.com/products/registrar/) ·
[workspace.google.com/pricing](https://workspace.google.com/pricing) ·
[resend.com/pricing](https://resend.com/pricing) ·
[firecrawl.dev/pricing](https://www.firecrawl.dev/pricing) ·
[notion.com/pricing](https://www.notion.com/pricing), all accessed 2026-08-27.*

**Domain price comparison**, because the renewal is what recurs forever:

| Registrar | .com first year | .com renewal | .io first year | .io renewal |
|---|---|---|---|---|
| Cloudflare | $10.46 | **$10.46** | $50.00 | **$50.00** |
| Porkbun | $11.08 | $11.08 | $28.12 | $51.80 |
| Namecheap | $11.08 | $18.48 | $34.98 | $75.98 |

Namecheap's cheap .io first year becomes $75.98 in year two — a $26/yr penalty for the teaser.

---

## Optional — social and web search

Only needed if you want engagement-weighted social research rather than plain web search.

| | Rate | One run of 15 queries |
|---|---|---|
| **OpenAI API** | web search $10 per 1,000 calls, plus model tokens | **$0.20** (small model) – **$0.99** (large) |
| **xAI API** | X search $5 per 1,000 calls, plus model tokens | **$0.27** – **$0.42** |

xAI is roughly half the cost, driven entirely by the $5-vs-$10 search call price.

*Sources: [developers.openai.com/api/docs/pricing](https://developers.openai.com/api/docs/pricing) ·
[docs.x.ai/docs/pricing](https://docs.x.ai/docs/pricing), accessed 2026-08-27.*

> xAI changed search billing to **per invocation** rather than per source. Any per-source figure from
> older documentation no longer applies.

---

## The two rollups in full

### Minimum viable — $27 to $37 per month

| Line | Cost |
|---|---|
| Claude Pro, annual | $17 |
| Google Workspace Business Starter, 1 seat, annual | $7 |
| Domain, amortised (.com $10.46/yr → .io $50/yr) | $0.87 – $4.17 |
| DataForSEO, amortised from the $50 deposit | ~$1 – $5 |
| OpenAI + xAI search, amortised | ~$1 – $3 |
| Firecrawl, PostHog, CRM, Notion, Cloudflare, Resend, Apollo | **$0** |
| **Total** | **$27 – $37** |

### Comfortable — $205 to $233 per month

Paid only where the free tier genuinely stops being enough.

| Line | Cost | Why the free tier bites |
|---|---|---|
| Claude Max 5x | $100 | Pro's weekly limit blocks a working day once you run the pipeline daily |
| Apollo Basic, annual | $49 | 75 credits/month is a demo |
| Firecrawl Hobby | $16 – $19 | 1,000 pages disappear in two competitor crawls |
| Google Workspace Standard | $14 | Starter's 30 GB |
| Notion Plus, second member | $10 – $12 | Free blocks cap once someone joins |
| Cloudflare Workers Paid | $5 | The 10 ms CPU ceiling, not the request count |
| DataForSEO | ~$5 – $15 | metered |
| OpenAI + xAI | ~$5 – $15 | metered |
| Domain | $1 – $4 | — |
| PostHog, CRM, Resend | **$0** | free tiers still hold at this scale |
| **Total** | **$205 – $233** | |

Drop Apollo and stay on Claude Pro: **$75 – $90**. Add a paid CRM and Resend Pro past three seats:
**$265 – $300**.

---

## Before you budget

1. **Roughly $150/month of this stack runs at zero.** PostHog, the CRM free tier, Resend, Cloudflare
   Workers and solo Notion are not trials — they are free plans that hold at founder scale.
2. **The top-tier model on a Pro plan is credits-only from the first token.** Budget for it separately
   or move to Max.
3. **Consumption credits are the new seat price.** Both Attio and Notion moved AI and enrichment onto
   metered credits, so the per-seat number is no longer the whole bill.
4. **Google Workspace list prices rose about 17% in 2025** when Gemini was bundled in. The current
   promotional discount is regional.
5. **The .io floor has climbed to $50/yr** at cost. If the name works as a .com, that is a $40/yr
   saving that recurs forever.

### Could not be verified from a primary source

Listed rather than guessed:

- Claude's numeric per-tier usage caps — Anthropic does not publish them
- Attio pricing in USD — the page is EUR-locked with no switcher
- Apollo API access on the free plan, and its per-tier rate limits — the page contradicts itself
- Cloudflare Pages bandwidth limits — not published on any tier
- Firecrawl's credit multipliers for advanced features — described only as "additional credits"
- DataForSEO's per-endpoint backlink rates beyond the two quoted above
