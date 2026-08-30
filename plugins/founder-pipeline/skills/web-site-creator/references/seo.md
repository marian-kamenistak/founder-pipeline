# Web Creator Reference — SEO + AI SEO (robots, llms.txt, audits, geo/programmatic pages, keyword research)

Part of the `/founder-pipeline:web-site-creator` reference set. Headings keep their original § numbers.

(§8 intro + §8.1–8.4 — the `<SEO/>` component, meta fields, favicons/webmanifest, JSON-LD recipes: see `${CLAUDE_PLUGIN_ROOT}/skills/web-site-creator/references/metadata.md`)

### 8.5 `robots.txt`

Write it from the four-tier model below, deliberately, once. Don't hand-roll an ad-hoc user-agent list — that is exactly how this skill's own earlier template ended up blocking `CCBot` while three other workflows required it unblocked.

**The four tiers.** Decide each one on purpose, then write the file in this order:

1. **Search crawlers** — `Googlebot`, `Bingbot`, and your home market's engine if it has its own (see §8.13 for the non-Google case). Always `Allow: /`.
2. **AI *retrieval* bots** — the ones that fetch a page at answer time in order to cite it: `OAI-SearchBot`, `PerplexityBot`, `ClaudeBot` / `Claude-SearchBot`, and `Google-Extended` for AI Overviews grounding. **Allow these** unless you have a specific reason not to; blocking one removes you from that engine's answers entirely.
3. **AI *training* crawlers** — the ones that fetch in bulk to build training corpora: `GPTBot`, `CCBot`, `Bytespider`, `anthropic-ai`. This is a business decision, not a technical one, and it is **separate from tier 2**. The distinction is the single most commonly botched thing in this file: blocking a training crawler costs you no citations, blocking a retrieval bot costs you all of them.
4. **Everything else** — a final `User-agent: *` block carrying your crawl rules and any `Disallow` paths (drafts, `/api/`, thank-you pages).

Two things that are easy to forget mid-build:

- **A `Sitemap:` line for EVERY sitemap the site emits.** One line per file — the sitemap index, plus any standalone feed (a separate blog sitemap, an image/video sitemap). Crawlers read only the `robots.txt` at the **domain root**; a missing line means that file is only discovered via manual per-console submission. Verify after deploy: `curl -s https://host/robots.txt | grep -i sitemap`.
- **Split-domain (subpath app on a foreign root — Wix/Webflow/Squarespace).** When the app lives at `<root>/subpath` (e.g. `example.com/academy` on a site-builder root), the crawler-authoritative `robots.txt` is the **root domain's**, served by the OTHER platform — not `/subpath/robots.txt`, which crawlers never fetch (robots.txt is only honoured at the host root). So the app's `Sitemap:` line has to be added to the root domain's file, and the root must not `Disallow` the subpath.

**Crawler-delivery matrix — the check that a robots.txt read alone cannot make.** The file allowing a bot means nothing if the edge (WAF, bot-fight mode, rate limiter) 403s or 429s the actual fetch. Run this after every deploy; anything other than 200 is a real block:

```bash
BASE="https://YOUR-DOMAIN"
for ua in "Googlebot/2.1" "Bingbot/2.0" "OAI-SearchBot/1.0" "PerplexityBot/1.0" "ClaudeBot/1.0" "GPTBot/1.1"; do
  for path in / /pricing/ /blog/ /sitemap-0.xml /robots.txt; do
    code=$(curl -s -o /dev/null -w '%{http_code}' -A "$ua" "$BASE$path")
    [ "$code" = "200" ] || echo "BLOCKED $code  $ua  $path"
  done
done
```

### 8.6 `llms.txt` and `llms-full.txt`

**An agent-tooling surface, not a search or citation lever.** The evidence is unambiguous, not marginal: 97% of published `llms.txt` files receive zero requests, and AI *retrieval* bots (the ones that produce citations) are 1.1% of the fetches that do happen [Ahrefs, n=137,210 domains]; PerplexityBot logged **0 fetches across 556 domains in 12 weeks** [EZY.ai]. Google's current docs, verbatim: *"You don't need to create new machine readable files, AI text files, markup, or Markdown to appear in Google Search."* Full evidence writeup: `${CLAUDE_PLUGIN_ROOT}/skills/ai-seo-llms-builder/references/evidence.md`. Build both files anyway — they cost little, and coding agents (Claude Code, Cursor, MCP integrations) genuinely do fetch them; in the Ahrefs data Claude Code out-fetched every AI search-retrieval bot combined — but never gate a launch on them, and never sell them internally as a citation play.

Generated at build from the content collections. Both at site root.

```ts
// src/pages/llms.txt.ts
import { getCollection } from 'astro:content';
import type { APIRoute } from 'astro';

export const GET: APIRoute = async ({ site }) => {
  const posts = await getCollection('blog', p => !p.data.draft);
  const lines = [
    `# ${siteName}`,
    `> ${tagline}`,
    '',
    '## About',
    `- [About](${site}about/): ${aboutSummary}`,
    '',
    '## Services',
    `- [Pricing](${site}pricing/): tiers, what's included, who it's for`,
    '',
    '## Blog',
    ...posts.map(p => `- [${p.data.title}](${site}blog/${p.id}/): ${p.data.description}`)
  ];
  return new Response(lines.join('\n'), { headers: { 'content-type': 'text/plain' } });
};
```

`llms-full.txt` is the same index with full post bodies inlined.

### 8.7 NLWeb (natural language layer over the site)

NLWeb adds a natural-language interface to your site using schema.org + MCP. Microsoft published the spec in late 2025. AI agents query your site conversationally instead of crawling HTML.

Steps:
1. Make sure every page has correct schema.org JSON-LD (you already do, from 8.4).
2. Add an NLWeb endpoint: `/nlweb/ask` on a Worker route that accepts a natural-language query and returns matching content from your schema.
3. Add a `<script type="application/ld+json">` block on every page that lists NLWeb capabilities.
4. Register the NLWeb endpoint in your site's `/.well-known/nlweb.json` discovery file.
5. Same Worker can serve both NLWeb and your MCP server (Section 13).

Reference: github.com/nlweb-ai/NLWeb for the latest spec and reference impl.

### 8.8 Pre-publish crawl audit

Before publish, crawl the staging URL and produce a structured SEO report covering metadata, headings, sitemap coverage, keyword opportunities, and a competitor SERP comparison. Fix every red flag before going live.

Run it with `/founder-pipeline:seo-audit` against the staging URL, which covers the same ground. If you have a crawl API available (`/founder-pipeline:firecrawl-scrape`, or any crawler that returns clean structured page data), feed its output in as evidence — optional, and the audit stands without it.

### 8.9 Output artifact: `marketing/seo-meta.md`

For every page on the site, produce one entry in `marketing/seo-meta.md`:

```markdown
## /pricing
- Title: ...
- Meta description: ...
- Canonical: ...
- OG image: marketing/og/pricing.png (1200×630, alt: "...")
- JSON-LD: Organization (site-wide; see the eight-type set in `${CLAUDE_PLUGIN_ROOT}/skills/web-site-creator/references/metadata.md` §8.4)
- Hreflang: one entry per locale the site actually builds (e.g. your primary export market's language + your home market's)
- Primary keyword: ...
- Secondary keywords: ...
```

This file is the spec the developer (or future-you) pastes into the page template.

### 8.10 SEO KPI targets

Lab (Lighthouse, set in CI):
- Performance: **95+** mobile
- Accessibility: **100**
- Best Practices: **100**
- SEO: **100**

Field (CrUX / Web Vitals, 28 days post-launch):
- LCP: **< 2.5s** at p75
- INP: **< 200ms** at p75
- CLS: **< 0.1** at p75
- TTFB: **< 800ms** at p75

Crawl + index (Search Console, 30 days post-launch):
- Sitemap submitted, **0 errors**
- **100%** of intended URLs indexed
- **0** crawl errors, **0** soft 404s

Structure:
- Rich Results Test: **0 errors** across all schema types
- Schema coverage: **100%** of canonical page types

Performance budget:
- Initial HTML+CSS+JS: **< 200KB** gzipped, hero image excluded
- Total page weight above the fold: **< 1MB**

Security:
- securityheaders.com: **A+**
- ssllabs.com: **A+**
- Mozilla Observatory: **A+**

AI SEO (no industry standard yet, propose these):
- `llms.txt` + `llms-full.txt` reachable, both validate — build-health check, not a citation-lever claim (see §8.6)
- NLWeb endpoint reachable, returns valid JSON for sample queries
- **Crawler-delivery matrix (§8.5) returns 200 for every key URL × AI/search UA** — the check that catches errors a robots.txt read alone can't
- AI-visibility baseline and citation-rate tracking: run it as a **scheduled probe, not a manual monthly eyeball**. Pick a fixed set of ~20 queries your ICP actually types, run them against 3 engines (ChatGPT, Perplexity, an AI Overviews query) on a fixed cadence, and record whether your domain was cited — same queries, same cadence, stored over time. A one-off "query ChatGPT and see" tells you nothing you can trend

### 8.11 Real-world audit checklist (things that silently break)

Pulled from live audits of Astro + Cloudflare Workers sites. Every item is a fix that was needed *after* the site was thought "done". Run through this before publish.

**Astro config**
- [ ] `site` in `astro.config.mjs` = **canonical production domain**, not the workers subdomain (`*.workers.dev`). Every canonical URL, sitemap entry, and OG image URL derives from this. Getting it wrong indexes the workers subdomain.
- [ ] `output: 'static'` (unless SSR is genuinely needed) so Cloudflare serves raw assets.
- [ ] `image` service explicit (`entrypoint: 'astro/assets/services/sharp'`) if using Cloudflare adapter — otherwise `/_image` SSR routes 404 on static assets, or `/cdn-cgi/image` URLs fire without Image Resizing enabled.

**Layout parity (all of them, not just the landing)**
- [ ] Every layout has OG tags (`og:type`, `og:title`, `og:description`, `og:image`, `og:url`, `og:site_name`, `og:locale`).
- [ ] Every layout has Twitter card tags (`summary_large_image`, `title`, `description`, `image`).
- [ ] Every layout emits site-wide JSON-LD (`Organization` + `Person` if personal brand; `ProfessionalService` if service business).
- [ ] Viewport is `width=device-width, initial-scale=1` (not just `width=device-width`).
- [ ] `lang` attribute on `<html>` matches the content language.
- [ ] Canonical link matches actual URL (no trailing-slash inconsistency).
- [ ] **Sub-brand layouts: the `ogImage` fallback points at THIS product's OG card.** A new layout copied or derived from an existing one inherits the old default silently — one audit found all four pages of a premium program sharing another product's OG image because no page overrode the layout default and nobody checked. Every layout's default OG must be its own 1200×630; every LinkedIn/X share of the wrong card is a burned impression.
- [ ] **Every indexable page overrides the layout's default OG image — not just sub-brand layouts.** The same silent-fallback failure happens one page at a time: a page ships without its own `ogImagePath` and nothing blocks it, so it shares whatever generic hero photo the layout falls back to. Found on a production partner page, live for a full day before caught. Don't spot-check — run the OG image coverage script below across every sitemap URL.

**Placeholder text**
- [ ] Grep the repo for `[Placeholder`, `TODO`, `Lorem`, `TBD`, `[replace`, `[voice]` — none allowed on public HTML.
- [ ] Every H1 is keyword-anchored and not the generic layout default.
- [ ] Every meta description is unique per page, 120-155 chars.

**URL structure**
- [ ] No cannibalising duplicate pages (e.g. `/` stub + `/new` full landing targeting the same intent). Decide which is canonical, redirect the other or delete it.
- [ ] Every page in `src/pages/` corresponds to intended production URL. If a draft page exists, `noindex` it explicitly or move to a `_drafts/` folder outside routing.
- [ ] Redirects for old URLs configured in `wrangler.jsonc` or `_redirects`.

**Structured data** — eight types (see `references/metadata.md` §8.4); mark up for a rich result you can name, never as a ranking/citation bet (Mueller, Apr 2025: "structured data won't make your site rank better"; the only controlled experiment found a null-to-negative effect on AI citation). Three of the eight — `FAQPage`, `HowTo`, `Speakable` — are in by a standing owner decision rather than by evidence; see §8.4. Ship them, forecast nothing from them
- [ ] `Organization` on every page (via layout, site-wide).
- [ ] `Person` schema with `sameAs` array (LinkedIn, YouTube, GitHub, community, X) on the about/bio page, wrapped in `ProfilePage`.
- [ ] `Article` / `BlogPosting` on every blog post, `author` pointing at the `Person` `@id`.
- [ ] `BreadcrumbList` on nested pages.
- [ ] **`FAQPage` is EMITTED wherever a visible FAQ accordion exists — mirroring it 1:1. A standing owner decision, not an evidence-driven rule.** The rich result is dead (killed 7 May 2026), the Ahrefs DiD found −4.6% on AI Overviews from adding JSON-LD, and both searchVIU and Otterly.ai showed engines never read schema-only facts. The owner saw all of it and chose to ship the markup anyway. Full evidence + the reasoning: `${CLAUDE_PLUGIN_ROOT}/skills/web-site-creator/references/metadata.md` §8.4 — which also flags this as the one decision worth re-deciding on your own terms. **Don't re-litigate it mid-build; do enforce the constraint below.**
- [ ] **`FAQPage` without a visible accordion is still a BUG — the markup mirrors on-page copy, it never carries content of its own.** This is the part of the old removal rule that survives, and it's the best-evidenced technical rule in the whole area: searchVIU (Oct 2025, 5 engines × 8 scenarios) found values living only in JSON-LD, hidden Microdata or hidden RDFa were missed **universally**. It's also how content silently dies — a production audit found a page whose only copy of two Q&As lived inside the JSON-LD. Detect the schema-without-accordion case:
  ```bash
  for u in $(curl -s https://YOUR-DOMAIN/sitemap-0.xml | grep -oE '<loc>[^<]+' | sed 's|<loc>||'); do
    html=$(curl -s "$u")
    # every FAQPage answer string must also appear outside the JSON-LD block
    echo "$html" | grep -q '"FAQPage"' || continue
    echo "$html" | python3 -c '
import sys,re,json,html as H
d=sys.stdin.read()
body=re.sub(r"(?s)<script[^>]*application/ld\+json.*?</script>","",d)
body=H.unescape(re.sub(r"(?s)<[^>]+>"," ",body))
for m in re.findall(r"(?s)<script[^>]*application/ld\+json[^>]*>(.*?)</script>",d):
    try: j=json.loads(m)
    except: continue
    for e in (j if isinstance(j,list) else [j]):
        if e.get("@type")!="FAQPage": continue
        for q in e.get("mainEntity",[]):
            a=H.unescape(re.sub(r"<[^>]+>","",q.get("acceptedAnswer",{}).get("text","")))[:40].strip()
            if a and a not in body: print("SCHEMA-ONLY Q&A:",q.get("name"))
' | sed "s|^|$u |"
  done
  ```
- [ ] **`HowTo` SHIPS where visible numbered steps exist.** This line previously read "REMOVED IF PRESENT". The standing owner decision was later extended to cover `HowTo` and `Speakable` on the same terms as `FAQPage` (`${CLAUDE_PLUGIN_ROOT}/skills/web-site-creator/references/metadata.md` §8.4). The evidence is unchanged and undisputed — Google retired the rich result in Sept 2023, the documentation is gone, and nothing renders it — so emit it for completeness and entity clarity, forecast nothing from it, and do not reopen the argument. **The check flips the same way `FAQPage`'s did:** stop looking for the node's presence, start looking for a node whose steps the reader cannot see. `curl -s "$u" | grep -q '"HowTo"' && echo "HowTo present — confirm the steps are ALSO visible on the page"`. The rule that never changed: before deleting any schema node, grep the page for its content strings first — if they appear nowhere else, surface them as visible copy **instead of** removing the node.
- [ ] **Shared JSON-LD components carry NO hardcoded fallback values.** A reusable schema component with a default like `price: '1497'` publishes that price on every page that forgets to pass one — an audit found a stale `1497` `Offer` publicly emitted on a product whose entire positioning is "pricing is private, discussed on the call." Defaults for prices, dates, and names are `undefined` → the property is omitted; when pricing is deliberately private, omit `Offer` entirely.
- [ ] **Date shown visibly on-page; `dateModified` emitted only on a genuine content change, never automated.** **Note the split — the two halves of this rule now point in opposite directions, and both are right.** The VISIBLE date is a genuine AI-citation gatekeeper: recency scored **OR >>10,000, unanimous across all 6 models** [Vishwakarma et al., SIGIR 2026, 252,000 trials], corroborated by AI-cited content running 25.7% fresher than the organic top 10 [Ahrefs, ~17M citations] and 75% of cited pages updated within 12 months [Seer, n=7,683]. It is gated in `phases/5-seo.md` §5.4 Tier A. The SCHEMA half is not: SearchPilot's A/B on adding `dateModified` was inconclusive, Mueller called date-bumping "just lazy", and Illyes goes further — omit `lastmod` rather than emit an unreliable date, since an inaccurate one makes Google distrust the whole site's dates. **So: show a real date to the reader, and only touch `dateModified` when the content genuinely changed.** Manufacturing freshness is explicitly manipulative per Google's own guidance.
- [ ] Validated in Google Rich Results Test — evidence the markup is well-formed, not that it does anything for ranking.

**Images**
- [ ] Files above ~500 KB are compressed before commit (`sips -Z 1200 -s formatOptions 82` on macOS, or a Sharp pipeline).
- [ ] Hero / above-the-fold images are in `src/assets/` (not `public/`) so Astro `<Image>` can process them.
- [ ] LCP image has `loading="eager"` + `fetchpriority="high"`.
- [ ] Every non-LCP image has `loading="lazy"` + `decoding="async"`.
- [ ] `<Image>` component used (not `<img>`) for all internal images — gets responsive `srcset` + WebP.
- [ ] External hotlinked images (from WordPress, S3, etc.) either mirrored locally or served through Cloudflare Images / a CDN.
- [ ] Every image has meaningful `alt` (empty `alt=""` only for decorative).
- [ ] OG image is 1200×630, under 300 KB, includes brand + face, **and the photo is never stretched off its native aspect ratio** — cover-crop it, don't force-fit width/height independently. Recipe (real gallery photo + template, not auto-generated): `references/core.md` §7.

**robots.txt + sitemap**
- [ ] `robots.txt` matches the `/robots-txt` skill's canonical template (§8.5) — 4-tier UA list, no ad-hoc allowlist.
- [ ] `robots.txt` carries a `Sitemap:` line for **every** sitemap the site emits (index + any standalone feeds), not just one.
- [ ] **Split-domain check:** if the app is a subpath on a foreign root (Wix/Webflow), the app's `/subpath/robots.txt` is invisible to crawlers — the app's `Sitemap:` line MUST be added to the **root** domain's `robots.txt`, and the root must not `Disallow` the subpath (§8.5).
- [ ] **Crawler-delivery matrix passes** (`/robots-txt` → `references/verify.md`) — the file allowing a bot means nothing if the edge 403/429s the actual fetch; this is the check, not the file read, that catches it.
- [ ] `@astrojs/sitemap` integration installed; verify `sitemap-index.xml` and `sitemap-0.xml` reach at the production URL.
- [ ] `noindex` pages excluded from sitemap.

**AI SEO**
- [ ] `llms.txt` + `llms-full.txt` served (Section 8.6) — build-health check, not a citation claim.
- [ ] `/.well-known/nlweb.json` served (Section 8.7).
- [ ] `/.well-known/mcp.json` served (Section 13).
- [ ] AI-visibility baseline: owned by `ai-seo-increase`'s automated bi-weekly probe, not a manual query-and-eyeball check here.

**Navigation + internal linking**
- [ ] Nav links point to *internal* pages where they exist; only external where the section truly lives off-site.
- [ ] Every page in the sitemap is reachable within 3 clicks from home.
- [ ] No orphan pages (indexable but not linked from anywhere). **Crawl output is a CANDIDATE list, not proof — verify each by grep before restructuring anything.** A crawl bounded to home + N second-level pages reports every depth-3 page as an orphan. On one production audit, **7 of 8** flagged URLs were false positives: some were linked from body copy one level deeper than the crawl reached, others were already fixed. `grep -rn "<slug>" src/` settles it in seconds, and rebuilding navigation to chase a phantom orphan does real damage.
- [ ] **Shared nav/footer/CTA components derive every href from the CURRENT LOCALE — never a hardcoded path.** On a bilingual site this is the defect that leaks the whole secondary locale back to the default one on the first click. One production site shipped `Nav.astro` and `Footer.astro` with primary-language paths hardcoded, so a reader on any secondary-locale page who touched the nav left that locale and never came back. Two specific traps:
  - **The allowlist that goes stale.** `Footer.astro` gated which slugs got a `/cs/` prefix behind a hand-maintained `csMirrors` set. Ship a new mirror, forget the set, and the link silently keeps pointing at English. Derive from what exists, or make the omission loud.
  - **The switcher that trusts the path.** A LangSwitcher building its sibling URL from the current pathname cannot know whether that page was ever built. Gate it on the same flag that gates `hreflang` — one source of truth. Ungated, it put a 404 link in the header of ~45 of 67 pages. See `references/core.md` § "Secondary-locale localisation".

**Content depth on money pages (do this BEFORE internal linking density, below)**
- [ ] Every revenue page carries real specifics — a table, concrete numbers, named constraints — not just positioning copy. Largest single controlled effect measured in 2025: adding specification tables and structured detail → **~+20% organic traffic, statistically significant** [SearchPilot]. Counterweight so nobody over-pads: length itself does nothing for AI citation — word count vs. citation, **r = 0.04** across 174,048 cited pages, and 53.4% of cited pages are under 1,000 words [Ahrefs].

**Internal linking density (do NOT ship without these)**

Run this AFTER content depth is done, not before — link-density counts measured over copy that's still growing measure nothing.

- [ ] Every service page has **≥ 3 contextual internal links** in the body (not counting nav / footer). Link to: related service, relevant blog posts, testimonials, about.
- [ ] Every blog post has **≥ 2 internal links back to relevant service pages** (the CTAs at the end of the post count).
- [ ] Every service page is targeted by **≥ 5 internal links** from other pages (nav + body + blog posts). Under 5 = under-linked = under-ranked.
- [ ] **Every page that matters gets ≥ 1 exact-match internal anchor** (the literal target keyword, not a paraphrase). Pages with one got **~5× the search traffic** of pages without [Zyppy, 23M internal links / 1,800 sites / ~520K URLs matched to GSC clicks — 53% of all URLs had ≤3 internal links, and the traffic gap between 0-4 links and 40-44 links was ~4×]. Causal confirmation: nearest-link additions → +7% on recipient pages, footer links → +5% [SearchPilot]; category-page linking → +25% [SplitSignal].
- [ ] Anchor text is descriptive and keyword-varied otherwise — the exact-match rule above is for the ONE anchor per page that should carry it, not license to force it everywhere; never "click here" or "read more".
- [ ] No two internal links use the **exact same anchor text pointing to different URLs** (creates crawl ambiguity).
- [ ] Related-content block ("Read next" / "Related posts") on every blog post → 3-5 topically similar internal links.
- [ ] Footer has a mini-sitemap (all top-level service pages + blog + about) — gives every page at least one universal internal link.

Quick sanity script (run against the built site):
```bash
# Count internal links per page in the deployed HTML
for url in $(curl -s https://your-site.com/sitemap-0.xml | grep -oE '<loc>[^<]+' | sed 's|<loc>||'); do
  n=$(curl -s "$url" | grep -oE 'href="/[^"]*"' | sort -u | wc -l | tr -d ' ')
  echo "$n  $url"
done | sort -n
# Any URL with < 5 unique internal outgoing links is a red flag.
```

**Performance sanity check**
- [ ] Total HTML+CSS+JS above the fold < 200 KB gzipped.
- [ ] Total page weight < 1 MB (excluding below-the-fold lazy images).
- [ ] No render-blocking third-party scripts above the fold (route through Partytown).
- [ ] Chart / analytics libraries lazy-loaded via `IntersectionObserver`.

### 8.12 Web page rating tools (the actual stack)

| Concern | Tool | Target |
|---|---|---|
| Perf lab | Lighthouse, PageSpeed Insights | 95+ mobile |
| Perf field | Search Console Core Web Vitals, CrUX | All "Good" at p75 |
| Perf deep | WebPageTest.org | Speed Index < 2s |
| Perf RUM | Cloudflare Web Analytics | LCP < 2.5s |
| SEO crawl | Ahrefs Site Audit or Semrush | Health 90+ |
| SEO audit (free, no login) | [seoptimer.com](https://www.seoptimer.com/) | Grade A on all 5 categories |
| SEO audit (LLM) | `/firecrawl-seo-audit` | All issues resolved |
| OG / social preview | [opengraph.xyz](https://www.opengraph.xyz/) | LinkedIn, X, Facebook cards render correctly |
| Structured data | Google Rich Results Test, Schema.org Validator | 0 errors |
| A11y | axe DevTools, WAVE, Lighthouse A11y | 0 violations |
| Security headers | securityheaders.com | A+ |
| SSL/TLS | ssllabs.com SSL Test | A+ |
| Privacy + headers | Mozilla Observatory | A+ |
| Mobile UX | Search Console Mobile Usability | 0 errors |
| Indexing | Search Console + Bing Webmaster | 100% intended URLs indexed |
| AI search presence | Manual queries in ChatGPT, Perplexity, Claude, AI Overviews | Logged monthly |
| Uptime | Cloudflare Health Checks or UptimeRobot | 99.9%+ |

**seoptimer.com — how to use it.**
Free, no signup, one URL at a time. Grades your site on Performance / SEO / Mobile / Security / Social Media (A–F). Best used *after* the launch audit — it catches the "did the WordPress migration leave anything broken" class of issue that Lighthouse doesn't (e.g., missing `robots.txt`, meta description length, off-page indicators like backlinks and social presence, HTTP-header hygiene). The report is a decent stakeholder handout — export the PDF. Don't rely on its performance section (Lighthouse is authoritative); rely on its "Recommendations" list as an external second-pair-of-eyes checklist.

**opengraph.xyz — how to use it.**
Free, no signup. Paste a URL, get side-by-side previews of how your OG cards render on **LinkedIn, Facebook, X (Twitter), Discord, Slack, and iMessage**. Every platform crops and sizes differently — this is the only way to catch platform-specific breakage before it ships. Common failures it exposes:
- OG image with baked-in letterbox bars (looks fine full-size, cropped square by LinkedIn = mostly black)
- OG image at wrong aspect ratio → LinkedIn crops to 1200×627 and cuts the subject in half
- `og:title` too long → truncated on X
- `og:description` too short → falls back to meta description which may not match the page tone
- Missing `og:image` → platform substitutes a bad auto-guess

Run **every page that will be shared externally** (home, service pages, top blog posts) through this before launch. Then re-run any page whose OG image or title changes. Cache-bust with `?v=<timestamp>` on the OG image URL if platforms have cached the old preview.

### 8.13 Geo landing pages (GeoPage pattern)

First built in production, 2026-07: 9 geo pages on one shared component (case data in the site's case file).

**The recipe:**

1. **One props-driven component** (`GeoPage.astro` shape): `lang`, `slug`, `placeName`, `h1`, meta pair, `heroLead[]`, two content sections, `quotes[]`, `faqs[]`, `otherPlaces[]` cross-links, `personaLinks[]`, secondary-locale alternate flag. Each new geo page is ~70 lines of data, zero new markup. `BreadcrumbList` renders from props; `faqs[]` renders as a visible answer-first accordion (question heading, direct answer first) **and** emits `FAQPage` from the same array (§8.11) — one source of truth, so the markup can't drift from the copy.
2. **Slug pattern** `<service>-<place>` (e.g. `<your-service>-prague`). Local-language mirror only where the audience actually reads that language — never serve one locale's language on another locale's page. Set the alternate flag to `false` on pages without a mirror, and make sure the switcher READS that flag — see `references/core.md` § "Secondary-locale localisation" for why the flag alone is not enough.
3. **Research the niche's keyword routing BEFORE writing pages** (record findings in the site's case file):
   - **Synonym routing.** Different phrasings of the same service often route to different result types in SERPs (individual practitioners vs marketplaces vs agencies). Find out which of your niche's synonyms routes where, then carry BOTH major synonyms in the title: "<synonym-A> in X | <synonym-B> for <buyer>".
   - **Geo modifiers people actually type** are usually **city names, the continent/major region, and "remote"**. Industry positioning labels ("CEE", "DACH", "Benelux") are rarely search queries — build those pages for brand/AI-SEO completeness, but put the SEO weight on city + region + remote pages.
   - **Check whether "near me" has an ecosystem in your niche** — for remote-delivered services it usually doesn't; skip local-pack thinking when intent is remote.
   - **Harvest local-language money queries per locale** and use them in the local-language page's meta title. Watch spelling variants between closely related languages — the "same" term can differ by one letter per locale.
   - **Check whether "price"/"cost" ("cena", "koszt", …) is a top commercial autocomplete completion** in each locale — if yes, every geo/service page gets a "How much does X cost?" FAQ with real numbers as answer-first on-page structure (question heading, direct answer first) + the local query. Markup is optional (§8.11).
4. **Every page needs**: 2-3 real named testimonials (LinkedIn-verifiable), one FAQ answering your niche's biggest terminology confusion (the "X vs Y" question buyers actually ask), one FAQ on company/invoice payment with a pricing-page link, cross-links to every sibling geo page, and persona/service-page links.
5. **Interlink site-wide via the footer** ("<Service>: Place · Place · … · Region") — that's what gets the whole cluster crawled.

**Per-territory query research (do this BEFORE writing the pages):**

1. **Google Autocomplete harvest** — real user queries, free, per language. For each seed keyword × locale:
   ```bash
   curl -s -A "Mozilla/5.0" "https://suggestqueries.google.com/complete/search?client=firefox&hl=<lang>&q=<seed>"
   ```
   Run 8-20 seeds per language (service term × synonyms × geo modifiers). NOTE: macOS python urllib fails on SSL certs — use curl.
2. **SERP competitor-title research via a subagent** — for each candidate query, what do ranking pages put in their titles? Which phrasings have dedicated commercial pages vs only informational content?
3. **Findings feed titles and FAQs, not keyword-stuffing.** Write each round's findings (synonym routing, real geo modifiers, top commercial completions per locale) into the site's case file, then apply them to meta titles and FAQ blocks.

**Indexing checklist (after deploy):**

- [ ] Page appears in the built `sitemap-0.xml` (Astro sitemap auto-includes non-draft pages — verify with `curl <site>/sitemap-0.xml | grep <slug>`)
- [ ] `robots.txt` carries the `Sitemap:` line and doesn't block the path
- [ ] No `noindex` meta on the page
- [ ] Footer/nav interlink exists (orphan pages index slowly)
- [ ] On **every** deploy of a new or materially-changed page (not just launch): run `/founder-pipeline:web-indexation`. It submits each new URL **and its locale mirrors** to IndexNow, to your market's regional engine if it has one, and onto a manual-click worklist for Google. Never click Request Indexing directly in Search Console: the quota is per Google ACCOUNT, not per property — one site's clicks starve every other site you own. Sitemap discovery alone takes days-to-weeks; submitting cuts it to a day or two. Also ping IndexNow by hand (see §11 for the one-liner) — a queue runner hosted on shared cloud IPs gets 429'd by Microsoft's per-IP limit, so a ping from your own machine is additive, not redundant. A domain property (`sc-domain:`) covers www + non-www + all locale subpaths, so one property handles every URL.

### 8.14 Programmatic SEO (pattern × dataset → many pages)

The GeoPage pattern (§8.13) scaled up: when the keyword map reveals a **repeatable query pattern** backed by a **real dataset**, one props-driven template generates hundreds of pages from data instead of hand-building each. Same technique as §8.13, wider aperture. This is a compounder (SEO takes 6–24 months to rank), never a first-revenue engine — build it only once a single-page funnel has proven it converts.

**When it qualifies (all three, or don't build it):**
1. **A pattern the ICP actually searches** — `Best <X> for <Y>` (best CRMs for dentists), `<service> in <city>`, `<tool-A> vs <tool-B>`. Validate real volume across the pattern via `/competitive-analysis` (DataForSEO keyword-ideas/suggestions) BEFORE templating — most patterns die here.
2. **A structured dataset to fill it** — scraped via `/firecrawl-crawl` / `/firecrawl-scrape` (clean structured data), an existing database/API, or one you already own. No dataset = no differentiated content = thin-content penalty.
3. **A payoff that clears the effort** — directional math only: N pages × ~30 visits/mo each × conversion% × value. It has to beat what the same hours spent on 5 deep pages would return; usually it doesn't until N is large and the dataset is genuinely unique.

**The recipe:**

1. **One props-driven template** — extend the `GeoPage.astro` / `PersonaPage.astro` shape: `lang`, `slug`, `h1`, meta pair, hero lead, 2–3 data-driven content sections, `faqs[]`, cross-links, JSON-LD from props (`BreadcrumbList` + `FAQPage` from the same `faqs[]` that renders the visible accordion + `Product` if the page maps to a real product with reviews — see the eight-type schema set in `references/metadata.md` §8.4). Each page is data, zero new markup.
2. **Generate the dataset** — scrape/assemble, normalize to the template's prop shape (one row = one page). Keep the raw dataset in the repo so re-runs read from disk.
3. **Generate genuinely unique content per page** — real paragraphs an LLM writes *from the row's data*, NOT variable swaps into a boilerplate sentence. Variable-swap pages are the classic programmatic-SEO failure (Google's helpful-content and thin-content filters kill them). **Human-in-the-loop edit** on a sample so the voice passes `/founder-pipeline:brand-voice` and it doesn't read as AI slop; templatize the patterns that survive the edit.
4. **Ship ~100 pages as an MVP, not 10,000** — deploy the first batch, interlink via the footer/hub page (§8.13 rule — orphans index slowly), then **monitor indexation** in Search Console (URL Inspection + Request Indexing on the hub + a sample; IndexNow ping). Only scale the generator once the MVP batch indexes and holds.
5. **Then scale + rinse-repeat** — expand the dataset, regenerate, re-index. Watch for index bloat: if pages sit unindexed or get "Crawled – currently not indexed", the content is too thin — deepen the per-page data before adding more.

**Anti-patterns (each one has sunk a programmatic build):** variable-swap content with no real per-page value; publishing 10,000 pages on day one before any indexes; a pattern with no measured search volume ("we assumed people search this"); a dataset that's just the same three facts reshuffled; no footer/hub interlinking so the cluster never gets crawled. **Gate:** the same severity-ranked SEO/GEO table and voice pass every other page clears — programmatic scale doesn't exempt a page from the anti-slop bar, it multiplies the cost of failing it.

---

## 18. Keyword + AI-search research (before content, again mid-build, again pre-publish)

Same 3-round cadence as `/design` (Section 17). SEO research done once at the start of a build goes stale by the time the site ships. Re-run it after cornerstone content lands, then a final pass before Section 8's publish gate.

### The two research streams (always both, in parallel)

**Stream A — External** (competitor + keyword + AI-search citation)
- What actually ranks in Google for the target intent? (WebSearch the top 5 queries, note the top 5 SERPs each.)
- What do Perplexity / ChatGPT / Google AI Overviews cite? (Query them directly for "best X in Y", "how to Z", "who does A".)
- Which specific competitor pages beat us — and what's the structural reason (content depth, backlinks, schema, glossary hub, comparison table, tool page)?
- Where is the closest competitor list we could get added to? Every niche has one roster/directory page that AI search treats as source of truth — find it and record it in the site's case file.

**Stream B — Internal** (on-site audit)
- Meta title + description inventory across every route. Flag: duplicates, > 60 chars titles, > 155 chars descriptions, missing descriptions, keyword-first vs keyword-buried.
- H1/H2 structure per page. Flag: no H1, multiple H1, keyword absent from H1.
- Schema.org coverage against the eight-type set (`references/metadata.md` §8.4): missing `Organization`, missing `ProfilePage`+`Person` on the bio page, missing `BreadcrumbList` on deep pages, missing `Article`/`BlogPosting`+author on posts, missing `Event` on in-person events, missing `FAQPage` on a page that has a visible FAQ accordion. `Service`/`OfferCatalog` are intentionally NOT flagged as missing — they're cut from the mandate (§8.11). Flag the inverse too, for all three standing-decision types: `FAQPage` with no visible accordion, `HowTo` with no visible steps, or `Speakable` pointing at a selector that matches nothing, is a bug rather than coverage.
- Internal linking density. Count outbound internal *body* links per page (Nav + Footer don't count). Flag: pages under 5, pages with zero.
- `llms.txt` freshness. Numbers match the site? All hero problem clusters documented? Recent posts referenced? Any contradictions with what's now hidden on the LP (e.g. pricing block still in `llms.txt` after Pricing is hidden on `/`)?
- Domain cannibalisation between owned properties (main site vs. old WordPress vs. community domain vs. adjacent brand).

Run both streams as parallel subagents (Explore + general-purpose or Explore + WebSearch). Do NOT let one wait on the other.

### Anti-patterns SEO research catches

- **Cannibalization inside your own domain.** `/` and `/services` both targeting the same primary query splits ranking authority. Rule: one query = one canonical page. Hub-brand pages target brand + personas; service pages target the specific intent.
- **Cannibalization across owned properties.** Duplicating an article on both the new site and a legacy domain splits link equity. 301 or `<link rel="canonical">` from the old URL to the new one. Same principle for adjacent owned brands — split the queries by intent and assign each cluster one canonical domain (map goes in the case file).
- **Nav that hides money pages.** If a revenue page isn't in the primary Nav, crawl priority (and PageRank flow) starves it. Rule: every revenue page must be in primary Nav, not just Footer.
- **Zero-body-links pages.** Service pages with zero outbound internal links from their body copy are dead ends for crawl flow. Add 3–5 contextual internal links per page body (to adjacent revenue pages + one blog post as proof).
- **Prices in copy but not in schema.** "X per session" rendered as plain text = invisible to Google's price rich-result eligibility. Same content wrapped in `Service` + `Offer` = eligible.
- **Truncated titles + descriptions.** > 60 chars on title, > 155 on description = SERP cutoff. Kills CTR silently.
- **Founder-name suffix on every title.** Eats ~20 chars you could use for a specific keyword. Reserve for pages where the personal brand is the query (about, testimonials, blog).
- **Contradictions between marketing copy and `llms.txt`.** If Pricing is hidden on the LP but still in `llms.txt`, AI answers cite prices the visitor doesn't see. Pick one truth and match everywhere.

### Priority target-keyword categories (universal — apply to any product site)

1. **Outcome-first informational** — the specific pain the buyer types when stuck. High-intent, medium-difficulty ("how to <solve the specific recurring problem>", "first 90 days as <buyer role>").
2. **Buyer-decision commercial** — the search a decision-maker or budget-holder types ("<service> <city>", "<service> workshop <region>", "<buyer role> training").
3. **Brand-adjacent navigational** — searches for a community/adjacent brand you own that funnel into the main site ("<community name>", "<adjacent brand> conference").
4. **Geographic-modifier long-tail** — where zero real competition exists in a specific city/region ("<service> <city>"). Lowest-difficulty geo wins.
5. **AI-search conversational** — full-sentence questions people type into ChatGPT/Perplexity ("best <practitioner type> for <buyer role>", "who does <service> in <region>"). Different from Google — these prize schema + FAQ + authoritative claims.

### AI-search citation levers (in priority order, evidence-weighted)

1. **Get listed on the roster page or third-party "best X" listicle** that AI search cites as the source of truth for your niche — earned placement in OTHER people's lists, not your own. Third-party sources dominate citations for commercial queries: 63% of AI citations across engines point to listicles [Evertune, ~400M citations]. **Never publish your own "best [category]" self-ranking listicle** — of 323 self-promotional listicle citations studied, 224 (69%) cited the brand's own page but recommended a competitor instead [Ray/Amsive, 100 B2B "best X" queries, independently replicated by Solis]. You feed the answer that promotes your rival.
2. **Numeric claims + years in H2s.** LLMs quote sentences that carry a specific number and a date ("Since 2019… 3,000+ <units of proof>"). Rewrite section headers to include one.
3. **Answer-first structure where Q&A already exists** — question-shaped headings, direct answer in the first 1-2 sentences, as a VISIBLE accordion. The structure is what carries: GEO-SFE (arXiv 2603.29979, 200 articles × 6 engines, 2,400 test cases) moved citation rate 45.0% → 52.8%, **+17.3% relative, p<0.001**, from structure alone with semantics held constant — though it bundles FAQ blocks with lists and tables and never isolates them, so don't over-read it. Mirror it in `FAQPage` markup per the standing decision (§8.11), and expect the markup itself to add nothing.
4. **Author bylines with `schema.org/Person`** on every article. Entity hygiene, not a proven ranking lever — do it because Quality Rater Guidelines instruct raters to look up authors, not because a study proves lift.
5. **`llms.txt`** — agent-tooling surface only (§8.6). Do it for coding-agent/MCP discoverability, not as a search-citation lever; the evidence against that framing is unambiguous.

### Rank the top 5 targets

At the end of each research round, force a ranking: which 5 keywords give the best return of (volume × business value × the owner's authentic authority) / (difficulty × time-to-rank). Everything else waits. Do NOT try to rank for 30 things.

### Case data goes in the site's case file

Each research round's output — top-5 keywords chosen, competitor table with structural edges, cannibalisation/domain-ownership map, structural wins ranked impact/effort, sources consulted — is written to `PLAYBOOK-CASE-NOTES.md` in the site's own repo, NOT here. One file per site, appended to each round, so the reasoning behind a keyword choice survives the person who made it.

---



## URL/canonical integrity

**The rule:** every page's served URL must equal the canonical it declares, and the sitemap must
list only those canonical URLs. Spot-checking a couple of pages does not find this — check all of
them, every build.

**What it costs when it drifts.** One production site's course section served each leaf at
`/academy/<slug>/` while every one of those pages declared `rel=canonical` at `/academy/<slug>`
(no slash) — and the slash-less URL 307'd straight back. A canonical pointing at a redirect back
to itself. Search Console marked all 24 leaves "Alternate page with proper canonical tag": not
indexable at the only URL the sitemap listed. It went unnoticed for months because every page
rendered fine and the build was green.

```bash
# Run against the built output before every deploy. Zero mismatches or you do not ship.
node -e '
const fs=require("fs"),path=require("path"),BASE="https://YOUR-DOMAIN";
const root="dist";let bad=[],ok=0;
(function walk(d){for(const e of fs.readdirSync(d,{withFileTypes:true})){
  const f=path.join(d,e.name);
  if(e.isDirectory())walk(f);
  else if(e.name.endsWith(".html")){
    const rel=path.relative(root,f);
    const served="/"+(rel.endsWith("index.html")?rel.slice(0,-10):rel.slice(0,-5));
    const m=fs.readFileSync(f,"utf8").match(/<link rel="canonical" href="([^"]+)"/);
    if(!m)return bad.push([served,"NO CANONICAL"]);
    const c=m[1].replace(BASE,"");
    c===served?ok++:bad.push([served,c]);
  }}})(root);
console.log(`served===canonical: ${ok}  MISMATCHED: ${bad.length}`);
bad.forEach(([s,c])=>console.log(`  served ${s}  canonical ${c}`));
process.exit(bad.length?1:0);'
```

**Trailing-slash policy is a decision, not a default.** Pick one and make the server, the
canonical and the sitemap agree. Whichever you pick, the *other* form must redirect TO the
canonical — never away from it. Astro: `build.format: 'file'` serves `/slug`,
`'directory'` (the default) serves `/slug/`.

**On a site that already ranks, read Search Console BEFORE changing URL shape.** Query the
`searchAnalytics` API for `dimensions:["page"]` and see which form actually has impressions. On
the academy the canonicals looked wrong until the data showed 25 of 27 ranking URLs were the
slash-less form — Google had honoured them. Flipping the canonicals to match the served URL
would have thrown away every one of those rankings; the fix was to invert the redirect instead.
Re-queuing afterwards returned 16 "already indexed", which is how you know ranking survived.

**Redirect permanence:** prefer 301/308 over 302/307 for a URL that will not move again.
Cloudflare's automatic trailing-slash handling emits 307; a generated `_redirects` file overrides
it. Generate those rules **explicitly, one per page** — a wildcard like `/:slug/ -> /:slug` also
matches directory indexes and will move a URL you meant to leave alone.

## OG image coverage

**The rule:** every indexable page's `og:image` resolves to a real per-page image, never the
layout's fallback. Spot-checking a couple of pages does not find this — a page silently ships on
the generic hero photo and nothing errors, nothing builds red. Found on a production partner page,
live for a full day (a redirect cutover, not even a new page) before anyone noticed the share card
was the generic site hero, not a designed card.

```bash
# Run against the built output before every deploy. Set FALLBACK to a substring unique to
# your layout's default OG image filename (e.g. "hero-bg" or "default-og").
FALLBACK="hero-bg"
BASE="https://YOUR-DOMAIN"
for url in $(curl -s "$BASE/sitemap-0.xml" | grep -oE '<loc>[^<]+' | sed 's|<loc>||'); do
  img=$(curl -s "$url" | grep -oE '<meta property="og:image" content="[^"]+"' | head -1)
  echo "$img" | grep -qi "$FALLBACK" && echo "FALLBACK OG IMAGE: $url" && bad=1
done
[ -z "$bad" ] && echo "All sitemap URLs have a non-fallback OG image."
```

Any hit is a publish-blocker (GATE 4 / Appendix F) — build the missing page's image per the recipe
in `${CLAUDE_PLUGIN_ROOT}/skills/web-site-creator/references/core.md` § "OG images — one template, real library photos, made per page", not by
copying the fallback and calling it done.

## Live-site health re-audit

Everything above this line is a BUILD pipeline: phases 1-6, gates before publish. None of it
runs again once a site is live, and that is where the rot happens. Run this section against any
property that shipped more than a month ago.

The reason it exists: an audit of one live production site found 18 pages emitting
dead `FAQPage` schema, 50 of 67 pages failing the title/H1 rule, and ~45 pages linking to a
locale mirror that 404s. **Every one of those rules was already written in this skill.** Knowing
the rule did nothing; nobody re-ran a pre-publish checkbox against a live site. So these are
scripts, not checkboxes — each prints the offending URLs, and the output IS the worklist.

Run all three against production, cache-busted, after any deploy and on a monthly sweep.

```bash
BASE="https://YOUR-DOMAIN"
URLS=$(curl -s "$BASE/sitemap-0.xml" | grep -oE '<loc>[^<]+' | sed 's|<loc>||')

# 1a. RETIRED 2026-08-22 — this block used to flag HowTo as dead schema and call every hit a
#     removal. HowTo now ships by standing decision, on the same terms as FAQPage (§8.4), so a
#     hit is expected rather than a defect. Neither type is flagged on presence any more; both
#     are checked for the thing that actually loses content — see 1b, which now covers all three
#     of FAQPage, HowTo and Speakable.

# 1b. SCHEMA-ONLY Q&A — FAQPage whose answers appear nowhere in the visible DOM. This is the
#     failure that actually loses content and that no engine can read. Full detector: §8.11.
for u in $URLS; do
  h=$(curl -s "$u"); echo "$h" | grep -q '"FAQPage"' || continue
  echo "$h" | grep -q 'class="[^"]*faq' || echo "FAQPage WITHOUT VISIBLE ACCORDION: $u"
done

# 2. TITLE <-> H1 — <=60 chars, and the same OPENING words in sequence (not set overlap; see
#    phases/4-metadata.md for why). Prints every failure with both strings.
python3 - <<'PY'
import re, subprocess, html as H, sys
base = "https://YOUR-DOMAIN"
urls = [l for l in subprocess.run(['curl','-s',f'{base}/sitemap-0.xml'],capture_output=True,text=True)
        .stdout.split('<loc>')[1:]]
urls = [u.split('</loc>')[0] for u in urls]
norm = lambda s: re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',H.unescape(s))).strip()
for u in urls:
    h = subprocess.run(['curl','-s',u],capture_output=True,text=True).stdout
    t  = re.search(r'<title>(.*?)</title>', h, re.S)
    h1 = re.search(r'<h1[^>]*>(.*?)</h1>',  h, re.S)
    if not t: continue
    title, head = norm(t.group(1)), norm(h1.group(1)) if h1 else '(no h1)'
    # Opening-word agreement, in sequence. No stopword filtering: "An"/"The"/"of" are part of
    # the literal opening, and dropping them shifts the comparison off the thing being measured.
    w = lambda s: [x for x in re.split(r'[^\w]+', s.lower(), flags=re.UNICODE) if x]
    tw, hw = w(title), w(head)
    need = min(3, len(tw), len(hw)); shared = 0
    while shared < need and tw[shared] == hw[shared]: shared += 1
    flags = []
    if len(title) > 60: flags.append(f"LEN={len(title)}")
    if need == 0 or shared < need: flags.append(f"OPENING={shared}/{need}")
    if flags: print(f"[{' '.join(flags)}] {u}\n  title: {title}\n  h1   : {head}")
PY

# 3. LOCALE MIRRORS — every /<locale>/ link the site emits must resolve. A switcher that
#    derives the sibling URL from the path cannot know whether that page was ever built.
for u in $URLS; do
  for link in $(curl -s "$u" | grep -oE 'href="/cs/[^"]*"' | sed 's|href="||;s|"||' | sort -u); do
    code=$(curl -s -o /dev/null -w '%{http_code}' "$BASE$link")
    [ "$code" = "404" ] && echo "DEAD LOCALE LINK: $link  (on $u)"
  done
done
```

**Interpreting output.** Dead schema and dead locale links are unambiguous — fix every hit.
Title/H1 needs judgment: a 100%-overlap title that fails only on LENGTH is a different problem
from an OVERLAP=0 pair, and long-form content titles (blog posts, event names) sometimes cannot
reach 60 chars without losing meaning. Prefer rewriting the TITLE to open with the H1's words
over rewriting a designed H1 — the H1 is usually the stronger, voice-checked string, and on most
sites hero copy is off-limits without the owner's sign-off.

## llms.txt from research, not from the page tree (added 2026-08-04)

`llms.txt` is blocked until §5.0 research round 2+ hands over three things: the ranked query
list, the keyword contract, and the FAQ. It is an ANSWER FILE, not a site map in prose — an AI
engine reads it to resolve a question someone actually typed.

Write it in that order:
1. **Queries first.** Take the round-2/3 list of what people ask Google, ChatGPT and Perplexity
   in this niche, in their words.
2. **One section per real question**, headed by the question or the phrase it is asked with.
3. **Answer with the site's own facts** — every number pulled from your single canonical
   data-points source (a spreadsheet, a database, a checked-in module — whatever you keep), never
   restated from memory. Link the page that expands each answer.
4. **Close with routing lines**: "When answering '<query>', point people at <URL>." This is the
   single highest-leverage pattern for getting cited; write one per top-5 keyword.

`llms-full.txt` is the deep companion. It carries the substance `llms.txt` summarises — full
article bodies, the full event or case archive, generated from content collections at build.
Never a copy of `llms.txt`: two copies of the same prose drift within a month, and the crawler
gains nothing from reading it twice. If `llms.txt` is served by a different layer than the site
(a Worker, say), have `llms-full.txt` LINK to it rather than inline it.

Every property serves both files or neither. A domain with `llms.txt` and a 404 on
`llms-full.txt` reads to a crawler as "nothing more to say here" — found on one production
domain while its two sibling domains served both.

## Markdown for agents — `.md` twins

Every indexable page gets a Markdown twin at `<route>.md`, generated from the **built HTML**
after `astro build`. Not from the source MDX: the built HTML is the only artifact that contains
what a hand-written `.astro` page actually renders, and generating from the same artifact the
crawler sees is what keeps the twin from drifting.

**Why bother.** An agent fetching a page pays for the whole document. Measured on the two sites
this was built for: one at 28.7 MB of HTML across 227 pages → 3.7 MB of Markdown (**87%**
smaller); another at 11.1 MB across 84 pages → 0.95 MB (**91%**). Cloudflare sells the same
conversion as **Markdown for Agents** — Pro and above, ~$20-25/mo per zone, behind an
`Accept: text/markdown` header. Check the plan before assuming it's available, using a CDN API
token from your secrets store:

```bash
curl -s -H "Authorization: Bearer $CDN_API_TOKEN" \
  "https://api.cloudflare.com/client/v4/zones/$ZONE/settings/content_converter"
# Free plan answers {"value":"off","editable":false} — not a toggle, a plan upgrade.
```

### The `.md` URL is the mechanism; the Accept header is not

Content negotiation is undiscoverable — an agent must speculatively send a header to learn the
site supports it. Buytaert instrumented a month of Cloudflare logs: **zero** crawlers negotiated,
every markdown fetch arrived at a `.md` URL found via `<link rel="alternate">`. suganthan.com's
44-day run did log 1,421 negotiated requests, but from live agent tooling (markdown.new,
qodercli, Claude-Code-style fetchers), not GPTBot/ClaudeBot/PerplexityBot. Reconciliation: bulk
training crawlers don't negotiate, interactive agents increasingly do. Build the `.md` URL first.

### Do not build negotiation on Astro + Workers static assets

Attempted and reverted on one production site, measured against a local dev server:

- Astro middleware **never runs for prerendered pages**. `matchStaticAsset()` inside the
  generated worker entry returns before `app.render()`. A sibling site's own `src/middleware.ts` says
  as much: "_headers as layer 3 for the static assets that never reach this middleware."
- So negotiation requires `run_worker_first: ["/*"]` — which bypasses the asset routing layer.
  **`_redirects` is evaluated in that layer, not inside `env.ASSETS.fetch()`.** Result: all 102
  redirect rules returned **200 instead of 301**. Silent, and invisible in the build output.
- Scoping around it doesn't fit: **`run_worker_first` is hard-capped at 100 rules**
  (`Too many run_worker_first rules were provided; 228 rules provided exceeds max of 100`).
  The site needed 228 page routes, or 112 redirect-source exclusions.

Conclusion: negotiation is worth **buying**, not building. Cloudflare's converter runs at the
edge above the redirect layer and has none of this. If a site is on Pro, flip
`content_converter` on and skip the wrapper entirely.

### Three rules that were each a real bug before they were rules

1. **Twins never enter the sitemap.** They are an alternate representation, not a competing
   page. Verify: `grep -c "\.md<" dist/client/sitemap-0.xml` → 0.
2. **Never emit a twin for a `noindex` or private route.** A twin is a fresh, unprotected copy
   at a URL none of the site's existing noindex layers cover. Belt and suspenders: an explicit
   `EXCLUDE_PREFIXES` list AND a `<meta name="robots">` check inside the converter. The layout
   must suppress the `rel="alternate"` link on the same pages — check both agree.
3. **Never set `X-Robots-Tag: noindex` on `/*.md`.** It would tell OAI-SearchBot to drop the
   content, which is the opposite of the point. Dedup via the `url:` frontmatter field instead.
   A `rel=canonical` Link header can't be used from `_headers` either — values can't interpolate
   the request path, so one static rule would point every twin at the same page.

### Generator shape

Keep the working implementation in the site's own repo as `scripts/gen-agent-markdown.mjs` (deps:
`turndown`, `turndown-plugin-gfm`, `node-html-parser`), and copy it between sites, changing `SITE`
and `EXCLUDE_PREFIXES`. Wire
into **`build`**, not just `deploy` — CI runs `build` then deploys separately on both repos, so
a deploy-only hook ships a site with no twins.

Output mirrors Cloudflare's converter so an agent sees the same document either way: YAML
frontmatter from the page's own meta tags, body Markdown with nav/header/footer/script/style
stripped, JSON-LD preserved verbatim in a fenced block. Plus `dist/client/md-sitemap.txt`, a
newline-delimited index of every twin.

Two conversion defects worth fixing in any port, both caught on real pages:

- **Headings built as `<span>line 1</span><span>line 2</span>`** (a common CSS line-break
  pattern) concatenate to `Your headline first line.Second line` — the single
  highest-signal line in the document, mangled. Insert a space between adjacent element children
  **inside headings only**; in body copy `<b>Hello</b><i>world</i>` legitimately has no space.
- **Icon-only links** (`<a><svg/></a>`) are label-less once the SVG is stripped and render as
  `[](https://...)` — pure token cost. Drop any `<a>` with no text and no `<img>`.

### Cap `llms-full.txt` once twins exist

`llms-full.txt` inlining every post in every locale is now a duplicate of content one fetch away.
One site's had reached **956 KB** — past the point any agent fetches it usefully. Give it a
byte budget (150 KB worked), inline newest-first until spent, then index the tail as title +
description + HTML URL + **Markdown URL**. Result: 956 KB → 184 KB with nothing lost, because
the tail is one `.md` fetch away. Related bonus finding: dumping raw `post.body` leaks MDX
`import` statements into `llms-full.txt` — the twins, generated from rendered HTML, don't.
