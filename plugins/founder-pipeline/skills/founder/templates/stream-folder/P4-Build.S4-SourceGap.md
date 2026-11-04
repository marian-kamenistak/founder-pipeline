# Competitor source teardown — gap table + fixes

**Stream:** [slug]
**Step:** P4.S4-SourceGap (P4-Build)
**Last updated:** [date]

> Reads the SHIPPED HTML of the top 3 competitors (landing page + best blog post each) and diffs it against our live pages. Raw HTML only — markdown extraction loses `<head>` and JSON-LD, which is the whole point. High + Moderate gaps get fixed on the live site in this step. Generalizable findings are written back into `/seo-audit` + `/ai-seo`.

---

## Competitor selection (evidence, not vibes)

| # | Competitor | Why top 3 (rank / keyword overlap) | Source + date |
|---|---|---|---|
| 1 | | | |
| 2 | | | |
| 3 | | | |

Swapped out of P1.S5's set? [no / yes — who, and the live-SERP reason]

## The 6 URLs

| Competitor | Page type | URL | Why this page (data, not eyeball) |
|---|---|---|---|
| 1 | landing / money | | |
| 1 | blog post | | |
| 2 | landing / money | | |
| 2 | blog post | | |
| 3 | landing / money | | |
| 3 | blog post | | |

Our equivalent pages: landing = [URL], blog post = [URL]
Blog half skipped? [no / yes — no article surface because ...]
Raw HTML pulled for all 6: [yes/no — verbatim `<head>` + JSON-LD blocks live in `P4-Build.S4-SourceGap/`]

## Comparison matrix — four layers

### Layer 1 — Head meta

| Element | C1 landing | C1 blog | C2 landing | C2 blog | C3 landing | C3 blog | OURS |
|---|---|---|---|---|---|---|---|
| title pattern (formula) | | | | | | | |
| meta description | | | | | | | |
| canonical | | | | | | | |
| robots / max-snippet / max-image-preview | | | | | | | |
| OG set (full?) | | | | | | | |
| Twitter card set | | | | | | | |
| hreflang cluster | | | | | | | |
| `article:published_time` / `modified_time` | | | | | | | |
| author | | | | | | | |
| geo / locale / theme-color | | | | | | | |
| preconnect / preload | | | | | | | |

### Layer 2 — JSON-LD `@type` inventory

| `@type` | C1 landing | C1 blog | C2 landing | C2 blog | C3 landing | C3 blog | OURS |
|---|---|---|---|---|---|---|---|
| | | | | | | | |

Notes on `@graph` nesting shape, `sameAs` arrays, and `Article`/`BlogPosting` field completeness (`author` as `Person` vs bare string, `dateModified`, `publisher`, `image`): [...]

### Layer 3 — Body elements

| Element | C1 landing | C1 blog | C2 landing | C2 blog | C3 landing | C3 blog | OURS |
|---|---|---|---|---|---|---|---|
| breadcrumb nav | | | | | | | |
| TOC | | | | | | | |
| definition block in first 300 words | | | | | | | |
| FAQ block | | | | | | | |
| comparison table | | | | | | | |
| author bio + credentials | | | | | | | |
| last-updated stamp | | | | | | | |
| reading time | | | | | | | |
| related posts | | | | | | | |
| inline newsletter / capture | | | | | | | |
| sticky / repeated CTA | | | | | | | |
| review / testimonial widget | | | | | | | |
| heading hierarchy shape | | | | | | | |
| image `alt` discipline | | | | | | | |

### Layer 4 — AI-extractability surfaces

| Surface | C1 | C2 | C3 | OURS |
|---|---|---|---|---|
| `llms.txt` / `llms-full.txt` | | | | |
| RSS + autodiscovery `<link>` | | | | |
| sitemap segmentation | | | | |
| robots.txt: GPTBot / PerplexityBot / ClaudeBot / Google-Extended | | | | |
| NLWeb / MCP endpoint | | | | |
| feed-per-tag | | | | |

## Gap table — every row gets a verdict

> `Reject` is a first-class verdict and must be used where it applies. Two mandatory rejections: schema the stream cannot truthfully populate (no invented `AggregateRating` / `reviewCount` / credentials — see `${CLAUDE_PLUGIN_ROOT}/skills/seo-audit/references/review-stars-rich-snippets.md`), and anything contradicting `P1-Ideation.S6-Offer.md`. Reader-facing words route back through P4.S2 + `/brand-voice` — this step ships structure, not copy.

| Layer | Gap | Competitors shipping it | Our page | Severity | Verdict + one-line reason | Status |
|---|---|---|---|---|---|---|
| | | | | High / Moderate / Low | Adopt / Adapt / Reject — [reason] | fixed / carried / rejected |

- High rows open at sign-off: **[must be 0]**
- Moderate rows carried to P6-Adoption.S2-KPIs.md (owner + date): [...]

## Fix pass (delegated subagent — diff summary only)

- Files touched: [...]
- Per-row outcome: [fixed N / carried M / rejected Z]
- Redeployed: [yes — URL + time]
- Adopted `@type` → real data source: [`@type` = source, one per adopted schema — zero untruthful markup]
- Reader-facing words changed outside P4.S2 + `/brand-voice`: [must be none]

## Re-verification (artifact, not claim)

- Live re-crawl of each changed page (a crawler API, or a re-fetch of the raw HTML): [pasted evidence]
- Schema validation on every added JSON-LD block: [result]
- **P4.S3 severity table re-run** — result + date appended to `P4-Build.S3-Web.md`: [zero High? yes/no]

## Learnings written back (quoted, so it's auditable)

Only generalizable patterns — page type + territory + implied action. A stream-specific fact stays in THIS file. Plugin skill files are read-only for installers, so the lines go into your own learnings store (a `## Learnings` section in your agent's learnings file, one heading per skill) — never edited into the shipped skill.

- Learnings for `/seo-audit`: "[exact line written]"
- Learnings for `/ai-seo`: "[exact line written]"

---

## Validation loop

- [ ] `/critical` run — findings: [...] — **CRITICAL SCORE: [X]/10** — advisory; the gate is the def-of-success PASS/FAIL checklist
- [ ] Def-of-success (from the stage file): [each criterion — met/unmet]
- [ ] Improvement loops run (if gate failed): [N — what changed each round]
- [ ] Revised — what changed: [...]
- [ ] **Owner approved** — [date] [overrides, if any]
