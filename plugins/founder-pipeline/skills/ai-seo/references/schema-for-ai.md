# Schema markup for AI discoverability (Mode 2)

This file belongs to the `ai-seo` skill.

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
