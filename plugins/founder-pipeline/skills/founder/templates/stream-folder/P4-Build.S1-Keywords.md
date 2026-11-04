# Keywords & search demand — the keyword contract

**Stream:** [slug]
**Step:** P4.S1-Keywords (P4-Build)
**Last updated:** [date]

> Seeded by P1.S4's carry-forward keyword table (reference it, don't re-derive). Copy (P4.S2) is written around this map; web meta/headings (P4.S3) implement it; KPIs (P6.S2) track it in Search Console. Change it here first, everywhere else second.

---

## Localization table

> One row per concept, EN as the default/anchor column, one locked-term column pair per non-EN target territory (location table in `${CLAUDE_PLUGIN_ROOT}/skills/founder/references/dataforseo-playbook.md`). Each locked term beat ≥2 candidate phrasings on real search-volume/trend data — literal translation is a candidate, not the default winner (Job 2b). Locked terms get mirrored into `TRANSLATION-GLOSSARY.md`, which whoever translates the pages works from: hand it to your translator, or to the agent doing the translation pass, and require every locked term to survive verbatim.

| Concept (EN canonical) | EN term [vol, source] | `<Territory>` term — locked [vol, source] | Rejected `<Territory>` candidates + volumes [source] |
|---|---|---|---|
| | | | |

## Primary keywords

| Keyword | Lang | Volume/mo | Difficulty | Trend 12m / 5y (territory) | Intent | Target page | Source |
|---|---|---|---|---|---|---|---|
| | | | | | | | `[source: ...]` |

> Max 1 primary may carry the unavailability flag; each flagged keyword gets a dated `queues/manual-queue.md` row "re-price via the keyword-volume source" at contract lock time. A contract with 2+ unpriced primaries does not lock.

## Google Trends notes

- [keyword] — [rising/flat/declining], territory: [home market / export market / regional / global], seasonality: [...]
- Reconciliation with P1.S2 "why now": [any declining trend explained or keyword dropped]

## AI-search phrasings (feeds llms.txt + FAQ)

1. [How the ICP would ask ChatGPT/Perplexity — verbatim natural language]
2. [...]
3. [...]

## Intent-to-page map

> Must enumerate the money pages — service/offer, pricing, booking/contact, homepage — sourced from P1-Ideation.S6-Offer.md + P2-Viability.S3-Pricing.md; each carries ≥ 1 commercial/transactional primary keyword or a recorded exception.

| Page | Primary keyword | Intent | Secondary keywords |
|---|---|---|---|
| | | | |

## Territory keyword gap

- Uncontested + differentiator-aligned (priority): [...]
- Contested, worth fighting: [...]
- Ceded (competitors own it, we don't fight): [...]

---

## Validation loop

- [ ] `/critical` run — findings: [...] — **CRITICAL SCORE: [X]/10** — advisory; the gate is the def-of-success PASS/FAIL checklist
- [ ] Def-of-success (from the stage file): [each criterion — met/unmet]
- [ ] Localization table complete for every target territory; locked terms mirrored into `TRANSLATION-GLOSSARY.md`: [done / N/A — EN-only stream]
- [ ] Improvement loops run (if gate failed): [N — what changed each round]
- [ ] Revised — what changed: [...]
- [ ] **Owner approved** — [date] [overrides, if any]
