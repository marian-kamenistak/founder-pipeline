# The AI-citation layer

This file belongs to the `web-backlinks` skill.

**The headline: off-page is where the measured AI-citation effects actually are.** On-page formatting has *no published correlation coefficient at all*; off-page signals have several, and they beat backlinks:

| Signal | Correlation with AI visibility |
|---|---|
| **Branded web mentions (linked OR unlinked)** | **Spearman 0.664** |
| Branded anchor text | 0.527 |
| Brand search volume | 0.392 |
| Domain Rating | 0.326 |
| Referring domains | 0.295 |
| **Backlinks** | **0.218** |

[Ahrefs, n=75,000 brands, DR>40, keyword volume ≥800.] Vendor study — Ahrefs sells a brand-mention tracker, so treat 0.664 with more caution than their negative results. Correlational throughout; big brands get both mentions and citations for shared reasons.

**Four consequences for how this skill runs — none of them changes the Four Laws:**

- [ ] **A mention is a win even when it never becomes a link.** Family 4 tells you to reclaim unlinked mentions FIRST; keep doing that for ranking, but stop scoring an un-converted mention as a failure — on this evidence the mention was already carrying ~3× the correlation of the link you were chasing. Log mentions on their own line, like entity work; never merge them into referring domains.
- [ ] **Third-party listicles are the single highest-value placement target, and your own listicle is a trap.** 63% of AI citations point to listicle pages [Evertune, ~400M citations]; in professional services, **third-party listicles take 80.9% of citations vs 19.1% for self-promotional ones** [Wix Studio, 75,000 AI answers / 1M+ citations — platform vendor, reported via Semrush-owned Search Engine Land, two layers of interest]. **Never publish your own "best [category]" self-ranking listicle:** of 323 self-promotional listicle citations studied, **224 (69%) cited the brand's own page and then recommended a competitor** [Ray/Amsive, 100 B2B "best X" queries, independently replicated by Solis]. You'd be funding the answer that promotes a rival. This is a live risk for the Family 1 directory play — a niche *directory* of other people is fine; a ranked "best X" list with you on it is not.
- [ ] **Entity work has a per-engine shape.** Ship the Wikidata item early (already Family 7 policy) — but know which engine it buys: ChatGPT leans Wikipedia (47.9% of its top-10 sources), Perplexity leans Reddit (46.7%), AI Overviews lean Reddit + YouTube (~21% / 18.8%) [Profound, 30M citations, Aug 2024–Jun 2025]. On a total-volume basis these shares are far smaller (Wikipedia is 7.8% of ChatGPT citations) — Profound's "share of top-10 sources" framing inflates apparent concentration ~6×. A Wikipedia/Wikidata play is disproportionately a **ChatGPT** play; a Reddit play is disproportionately a **Perplexity** play. Law 1 is unchanged: notability-first, never COI link insertion, never bare-link drops.
- [ ] **Being named matters more than being linked.** Citation rate was 53.1% when a brand was mentioned in the answer vs 10.6% when it wasn't — a 5× gap, with "ghost citations" where the source is cited but the brand never named [Seer, 541,213 responses, 20 brands, 6 platforms — the vendor's own client portfolio, not a random sample]. Reinforces Law 4's existing framing: badge and swap links are worth having for brand and AI surface, never for PageRank.

**What this does NOT license.** Don't retarget the playbook away from links on the strength of a correlation table. Referring domains stay the KPI this skill is measured on; the AI-citation layer is a second scoreboard reported alongside it, never instead of it.
