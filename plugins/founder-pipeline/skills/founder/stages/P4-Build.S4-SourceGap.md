# P4.S4 — Competitor source teardown → `P4-Build.S4-SourceGap.md` + `P4-Build.S4-SourceGap/`

**Phase: P4-Build**

**Routing:** fan-out + delegated (one agent per competitor, then one fix subagent) · research CHEAP, fix MID · gate critic on the session model

**Earns its keep when** P4.S3 shipped a live web surface. The site just passed its own hardening pass — but hardening checks the site against a *checklist*. This step checks it against the *competitors who actually rank*, by reading their shipped HTML. Checklists tell you what's broken; rivals' source tells you what's missing. **Skip entirely** (one line in `brief.md`) only when P4.S3 was skipped — no site, nothing to diff. That skip is common and legitimate: a stream with no web surface has nothing to compare.

**Partial skip:** if the stream ships no blog/article surface, run the landing-page half only and record the skip + why. Never skip the landing half.

**Hard gates:**
- **P4.S3 web is live and approved.** This step diffs against a real deployed URL set, never a local build.
- **Top 3 competitors are the named ones from `P1-Ideation.S5-Competition.md`** — selected by ranking evidence (organic keyword overlap / rank), not by who feels biggest. Paste the selection evidence with `[source: <tool>, <date>]`. If P1.S5's set is stale or its top 3 don't rank for the `P4-Build.S1-Keywords.md` primary keywords, re-pick from live SERP data and note the swap.

## What to do

**1. Lock the 6 URLs (2 per competitor).** For each of the 3 competitors:
- **Landing / money page** — the one that ranks for their version of your primary keyword, not their homepage-by-default.
- **Blog / article page** — their single best-performing post, picked from data: a keyword-data provider's "top ranking pages" or "pages by referring domains" report (DataForSEO's `/v3/dataforseo_labs/google/relevant_pages/live` / `/v3/backlinks/domain_pages/live` are the worked example). Never eyeball "looks popular".

Record the 6 URLs + why each was picked in the step file before pulling anything.

**2. Pull the RAW source — markdown is not enough.** `/firecrawl-scrape` with **raw HTML** requested (`formats: ['rawHtml']`), because the markdown pipeline strips exactly what this step exists to read: `<head>` tags and `<script type="application/ld+json">` blocks. Cross-check the parsed view with an on-page crawl API (meta, headings, canonical, schema presence, internal links — DataForSEO's `/v3/on_page/instant_pages` is the worked example; any crawler reporting the rendered head works). Also fetch each competitor's `robots.txt`, `sitemap.xml`, `llms.txt`, and `/rss.xml` — presence/absence is a finding.

**3. Extract into a four-layer comparison matrix.** One column per competitor URL, one column for OUR equivalent page. Four layers, all mandatory:

| Layer | What to inventory |
|---|---|
| **Head meta** | title pattern (formula, not just the string), meta description, canonical, robots/max-snippet/max-image-preview, full OG set, Twitter card set, hreflang cluster, `article:published_time` / `modified_time`, author, geo/locale, theme-color, preconnect/preload hints |
| **JSON-LD** | every `@type` present, `@graph` nesting shape, `sameAs` arrays, `BreadcrumbList`, `Article`/`BlogPosting` field completeness (`author` as `Person` vs bare string, `dateModified`, `publisher`, `image`), `FAQPage`, `HowTo`, `Product`, `Organization`/`Person`, `AggregateRating`, `Service`, `Course`, `Event`, `VideoObject`, `SpeakableSpecification` |
| **Body elements** | breadcrumb nav, TOC, definition block in first 300 words, FAQ block, comparison table, author bio + credentials, last-updated stamp, reading time, related-posts, inline newsletter/capture, sticky or repeated CTA, review/testimonial widget, jump-links, `<time>` semantics, image `alt` discipline, heading hierarchy shape |
| **AI-extractability surfaces** | `llms.txt` / `llms-full.txt`, RSS + autodiscovery `<link>`, sitemap segmentation (posts vs pages vs images), robots.txt rules for GPTBot / PerplexityBot / ClaudeBot / Google-Extended, NLWeb or MCP endpoint, feed-per-tag |

**4. Diff and verdict every gap.** For each row where ≥1 competitor ships something our page doesn't, write a verdict — **Adopt / Adapt / Reject** — plus one line of reason and a severity:
- **High** = they can win a SERP feature or an AI citation we structurally cannot (missing `Article`/`FAQPage` JSON-LD, no canonical, no `dateModified`, AI bots blocked, no definition block on an informational page, missing hreflang on a mirrored page).
- **Moderate** = weakens us (thinner OG set, no breadcrumbs or `BreadcrumbList`, no author entity, no TOC on long posts, no comparison table, no last-updated stamp).
- **Low** = polish.

**A `Reject` verdict is a first-class outcome and must be used.** Copying a rival's `@type` inventory wholesale is cargo-culting, and two rejections are mandatory to consider:
- **Never adopt schema the stream cannot truthfully populate.** `AggregateRating` without real collected ratings, invented `reviewCount`, or a fabricated author credential is spam markup — it risks a manual action and it's dishonest. If the underlying data doesn't exist, the row is `Reject — no truthful source` (or becomes a P6 action to *collect* the data first). Cross-ref `/seo-audit` → its `references/review-stars-rich-snippets.md`.
- **Never adopt an element that contradicts the approved artifacts.** Anything that changes reader-facing words routes back through `P4-Build.S2-Copy.md` + `/brand-voice` first — this step ships structure, not new copy. Anything that contradicts `P1-Ideation.S6-Offer.md` is `Reject`.

**5. Fix High + Moderate on the live site, in this step.** Delegate ONE fix subagent: it reads the gap table, the `web/` sources, the keyword contract, and the approved Copy sources on its own context, applies the `Adopt`/`Adapt` rows, redeploys, and returns ONLY a compact diff summary — files touched, per-row `fixed / carried / rejected`, and the re-crawl evidence. The main context holds the gap table and the gate verdict, never the HTML.

**6. Re-verify by artifact, not by claim.** After the fix pass: re-crawl each of our changed pages with the on-page crawl API, schema-validate every added JSON-LD block, and **re-run P4.S3's severity-ranked SEO/GEO error table** so that file stays true (append the re-run + date to `P4-Build.S3-Web.md`; the project's own post-change rule applies). Paste the evidence.

**7. Write the durable learning back into the two SEO skills.** Append a dated bullet to the `## Learnings` section of BOTH the bundled `seo-audit` skill's `SKILL.md` (full plugin install only) and the bundled `ai-seo` skill's `SKILL.md` (full plugin install only) (SEO/on-page/schema findings → `/seo-audit`; AI-citability and extractability-surface findings → `/ai-seo`; a finding that is genuinely both goes in both). If your plugin directory is not writable in your install, the learning goes wherever those skills' local overrides live for you — the requirement is that it lands where the NEXT site's run will read it, never that it sits in this step's file.

**The learning filter — generalize or don't write it.** Only patterns that will hold for the NEXT site go into those skills: *"B2B service pages in a smaller non-English market consistently ship `Service` + `BreadcrumbList` but never `FAQPage` — the FAQ block is free whitespace there"* is a learning. *"Competitor X's pricing page has no canonical"* is a stream fact and stays in this step's file. Every entry: dated, one or two lines, names the page type and territory it was observed in, and states the action it implies. No entry that just restates the skill's existing checklist.

**Step folder** `P4-Build.S4-SourceGap/`: one raw-extract file per competitor (`<competitor>-landing.md`, `<competitor>-blog.md`) holding the head-meta dump, the JSON-LD blocks verbatim, and the element inventory — so a re-run reads from disk instead of re-scraping. Plus `INDEX.md`.

**Skills:** `/firecrawl-scrape` (raw HTML — the primary tool here) + `/seo-audit` (the diff's severity framing + review-stars honesty rules) + `/ai-seo` (Pillar 1 extractability + bot-access checks) + `/critical`. Use `/firecrawl-scrape`, not a plain fetch — competitor sites are JS-heavy and a naive fetch will silently lose the schema blocks.

**Optional external dependency — a keyword/backlink data provider.** The page-selection and gap-sizing recipes in `references/dataforseo-playbook.md` (Jobs 1/6) are written against the **DataForSEO MCP server**, which you configure yourself; it is not bundled with this plugin. The endpoints named throughout (`/v3/on_page/instant_pages`, `/v3/dataforseo_labs/google/relevant_pages/live`, `/v3/backlinks/domain_pages/live`, `/v3/dataforseo_labs/google/domain_intersection/live`) are that provider's names for four capabilities — crawl a live URL's rendered head, list a domain's ranking pages, list its most-linked pages, and intersect two domains' keyword sets. Substitute your provider's equivalents. Without any such provider you can still run this step, but URL selection falls back to whatever ranking evidence you can gather by hand — record which, because the def-of-success below requires the selection to be evidence-backed either way.

**Map their structure too.** Their sitemap plus their navigation is their content strategy, stated out loud. Pull `sitemap.xml` (and any nested sitemaps) for each competitor and note the shape: which sections exist, how many URLs each holds, what they publish under and what they never publish at all. A section you have no equivalent of is a gap row like any other.

**Engine mode: fan-out** — one research subagent per competitor (2 URLs each), each returning only its filled matrix column; then plain synthesis + verdicts on the main thread; then ONE delegated fix subagent. Never let the raw HTML of 6 pages into the main context.

**Write to** `P4-Build.S4-SourceGap.md`: the 3 competitors + selection evidence, the 6 URLs + why each, the four-layer comparison matrix, the gap table (`Layer | Gap | Competitors shipping it | Our page | Severity | Verdict + reason | Status`), the fix diff summary, re-crawl + schema-validation evidence, the P4.S3 table re-run result, and the exact learning lines written to `/seo-audit` and `/ai-seo` (quoted, so it's auditable).

**Def-of-success — ALL must pass before Owner sign-off (fail → improvement loop per SKILL.md, never advance):**
- 3 competitors named with ranking evidence + `[source, date]`; 6 real URLs locked, each with its selection reason (blog half skipped only with a recorded no-article-surface reason).
- Raw HTML actually pulled for all 6 (markdown-only extraction = FAIL — the `<head>` and JSON-LD blocks must be quoted verbatim in the step folder).
- Comparison matrix covers all four layers for every URL; no layer left blank.
- Every gap row carries a severity AND an `Adopt`/`Adapt`/`Reject` verdict with a one-line reason — zero blank verdicts.
- **Zero High rows open on our site at sign-off**, each closed by re-crawl evidence pasted in — not by a claim that it was fixed.
- Every Moderate row is fixed OR carried into `P6-Adoption.S2-KPIs.md` with an owner + date — never silently dropped.
- Every adopted JSON-LD `@type` names its real data source; zero markup the stream cannot truthfully populate.
- Zero reader-facing words changed outside `P4-Build.S2-Copy.md` + `/brand-voice`.
- P4.S3's severity table re-run after the fixes and still zero High; the re-run is appended to `P4-Build.S3-Web.md` with a date.
- Dated learning lines written to the `## Learnings` section of BOTH `/seo-audit` and `/ai-seo`, each generalized (page type + territory + implied action) — a stream-specific fact in those skills = FAIL.
- `/critical` run recorded; score advisory (target ≥ 8/10) — the gate is the criteria above.

**Gate out (mandatory — see SKILL.md house rules):**
1. Matrix + gap table complete; High rows closed with re-crawl evidence; Moderate rows fixed or carried with owners.
2. Invoke `/critical` on the gap table — is any `Adopt` row cargo-culting a rival's choice that doesn't fit this stream? Is any `Reject` row actually laziness dressed as judgment? Would any adopted schema be untruthful for this business? Is the learning written to the two SEO skills genuinely generalizable, or a stream fact smuggled into a shared skill?
3. Fix; note what changed.
4. Present the gap table + the fix diff + re-crawl evidence + the two learning lines to the owner. **Wait for their explicit approval. Never auto-advance.**

**Checkpoint:** "Teardown of [3 competitors] across 6 pages: [N] gaps found — [H] High / [M] Moderate. Fixed [X] live, carried [Y] to P6.S2, rejected [Z] with reasons. Learnings written to the seo-audit + ai-seo skills. Next: the sales deck PDF."

**Next:** `stages/P4-Build.S5-Deck.md` (skip to `stages/P5-Activation.S1-Launch.md` only if the deck genuinely does not apply — see P4.S5's skip rule)
