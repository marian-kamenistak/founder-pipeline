# Web Creator Reference — Metadata (meta tags, favicons, JSON-LD, OG)

Part of the `/founder-pipeline:web-site-creator` reference set. Headings keep their original § numbers.

## 8. SEO + AI SEO

This section is the heart of the playbook. Most consultant sites skip 80% of it.

### 8.1 The `<SEO/>` component

Sets per page: `<title>`, meta description, canonical, Open Graph, Twitter card, JSON-LD.

### 8.2 Meta fields, all of them

```html
<!-- Core -->
<title>{title} · {siteName}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">

<!-- Open Graph -->
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="{ogImage}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{ogImageAlt}">
<meta property="og:site_name" content="{siteName}">
<!-- {primaryLocale} = your primary export market; one :alternate line per additional locale you ship -->
<meta property="og:locale" content="{primaryLocale}">
<meta property="og:locale:alternate" content="{homeMarketLocale}">
<meta property="og:url" content="{canonical}">

<!-- Twitter / X -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{ogImage}">
<meta name="twitter:image:alt" content="{ogImageAlt}">
<meta name="twitter:site" content="@your_handle">

<!-- Geo — only if the business genuinely serves a place; omit entirely for a remote/global product.
     {geoRegion} is an ISO 3166-2 subdivision code, {geoPosition} is "lat;lon". -->
<meta name="geo.region" content="{geoRegion}">
<meta name="geo.placename" content="{geoPlacename}">
<meta name="geo.position" content="{geoLat};{geoLon}">
<meta name="ICBM" content="{geoLat}, {geoLon}">

<!-- Mobile / app meta -->
<meta name="theme-color" content="#0a0a0a" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#ffffff" media="(prefers-color-scheme: dark)">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="{siteName}">
<meta name="format-detection" content="telephone=no">
<link rel="manifest" href="/site.webmanifest">

<!-- Hreflang — one line per locale you actually ship, plus x-default.
     Worked example below: primary export market at the root, home market under a path prefix. -->
<link rel="alternate" hreflang="en" href="https://example.com{path}">
<link rel="alternate" hreflang="{homeMarketLang}" href="https://example.com/{homeMarketLang}{path}">
<link rel="alternate" hreflang="x-default" href="https://example.com{path}">
```

### 8.3 Favicon set (no shortcuts)

`/public/`:
```
favicon.svg            # scalable, theme-aware via prefers-color-scheme inside the SVG
favicon-16.png
favicon-32.png
apple-touch-icon.png   # 180x180
icon-192.png
icon-512.png
site.webmanifest
```

`site.webmanifest`:
```json
{
  "name": "Your Product",
  "short_name": "Product",
  "icons": [
    { "src": "/icon-192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable" }
  ],
  "theme_color": "#0a0a0a",
  "background_color": "#ffffff",
  "display": "standalone",
  "start_url": "/"
}
```

**Take the icon from your configured brand kit, not from the scaffold.** Where a family of sites shares a parent brand, the mark in that brand kit (192×192 minimum) is the default favicon for every site in the family. Copy it into the repo under `src/assets/brand/` rather than referencing the kit path at build time. Two failure modes to check for explicitly: shipping the scaffold's placeholder icon, and shipping a leftover icon from a *different* product in the same estate — both survive review for weeks because nobody looks at a 32px square. Serve modern formats (`favicon-32x32.webp` + `favicon-192x192.webp`) alongside the PNG fallbacks in §8.3.

**Proxying gotcha on split domains (hosted site builder at the root, your build on subpaths).** This bites on any domain where a Worker proxies only *specific* prefixes to your build (`/assets/*`, your product paths, sitemaps, the IndexNow key) and a hosted site builder still serves everything else. A root-level `/favicon.svg` or `/favicon.png` falls outside the proxied prefixes, so `<link rel="icon" href="/favicon.svg">` silently resolves to the *builder's* icon, not yours. Fix: import the favicon through `astro:assets` (`import favicon from '../assets/brand/favicon.png'`) and reference the emitted hashed URL (`href={favicon.src}` → `/assets/…png`, since `astro.config` sets `build.assets: 'assets'`). Same rule for the nav logo. Verify with `curl -sI` that the icon URL returns your platform's response headers (e.g. the CSP from your `_headers` file), not the site builder's CDN (`x-served-by`, Fastly and similar). A single-root domain with no split has no such problem — `/public/` root icons are fine there.

### 8.4 JSON-LD recipes per surface

**Schema earns rich results and entity resolution, never rankings or AI citations.** [Mueller, Apr 2025: *"Structured data won't make your site rank better."*] The only controlled experiment on record (Ahrefs, 1,885 pages with JSON-LD added vs ~4,000 matched controls, DiD) found no significant lift on AIO/AI Mode/ChatGPT and a −4.6% move on AI Overviews; a 5-engine live-retrieval test ignored JSON-LD entirely. Mark up for a rich result you can name, never as a ranking or citation bet — which is why this table is six types, not ten.

| Surface | Schemas to include |
|---|---|
| Site-wide (root layout) | `Organization` (with `logo` + `sameAs`) — standalone `WebSite`-as-type dropped, SiteLinks Searchbox was retired and it has no other rich result |
| About / bio page | `ProfilePage` + `Person`, reference `Organization` |
| Blog post | `Article` (or `BlogPosting`) + `author` → `Person` `@id` + `BreadcrumbList` |
| Deep / nested pages | `BreadcrumbList` |
| In-person events only | `Event` — online-only events don't qualify for the rich result (Google's own restriction) |
| Any page carrying a **visible** FAQ accordion | `FAQPage`, mirroring the accordion 1:1 — see the standing-decision note below |
| Any page carrying **visible** numbered steps | `HowTo`, mirroring the visible steps 1:1 — same standing decision, extended 2026-08-22 |
| Any page with a clean lead answer capsule | `Speakable` (`SpeakableSpecification`), selector pointing at the capsule — same standing decision, added 2026-08-22 |

**`FAQPage` — standing decision: emit it, with eyes open.** This type is in the mandate by explicit policy call, NOT because the evidence supports it. What the evidence actually says: the Google rich result was killed **7 May 2026** (SC reporting removed Jun 2026, API removed Aug 2026), so it renders nothing in Search; the Ahrefs DiD above found **−4.6% on AI Overviews** from adding JSON-LD; searchVIU (Oct 2025, 5 engines × 8 scenarios) found a fact living **only** in JSON-LD was picked up by **0 of 5** systems; Otterly.ai planted a fact that existed nowhere on the web except inside FAQ schema and tracked 319 prompts Dec 2025–Mar 2026 — **no platform ever used it**. The owner was shown all of this and chose to ship it anyway. Do not "fix" this back to a removal rule on evidence grounds — that argument has already been had and settled. It only reopens if Google or an engine documents active harm.

If you are adopting this playbook for your own estate, this is the one standing decision worth re-deciding on your own terms: the honest reading of the evidence supports dropping all three types, and the owner's call to keep them is a bet on future engine behaviour, not on measured return.

**Extended to `HowTo` and `Speakable`.** The same standing decision now covers both. `HowTo`'s rich result was retired by Google in Sept 2023 and the previous rule here read **"REMOVE IF PRESENT"**; that rule is retired, because keeping it would have this file contradicting the owner's decision and would leave sanctioned `HowTo` nodes on already-live sites flagged as defects. `Speakable` has no rich result in this market either. Both ship on the same terms as `FAQPage`: implement them, forecast nothing from them, and do not reopen the evidence argument — it has been had and settled. It reopens only if Google or an engine documents active harm. AEO-side rationale: `${CLAUDE_PLUGIN_ROOT}/skills/ai-seo/references/aeo-patterns.md` §8.

**The one hard constraint that survives from the old removal rule, and it now governs all three types:** each is emitted **only** where the corresponding thing is visible on the page — a rendered FAQ accordion, rendered numbered steps, a rendered answer capsule — mirroring it 1:1. Schema-only Q&A (and schema-only steps) is still banned outright — it is unreadable to every engine tested and it is how content goes missing (one audit found a live page whose only copy of two Q&As lived inside the JSON-LD). Visible content first; markup mirrors it, never replaces it, never adds a question or a step the reader can't see.

**Still cut from the mandate:** `Service`+`OfferCatalog` (no live rich result), `Product`+`AggregateRating` (only when the product genuinely has third-party reviews — never self-serving; full eligibility rules in `${CLAUDE_PLUGIN_ROOT}/skills/seo-audit/references/review-stars-rich-snippets.md`).

Validate every type with Google Rich Results Test before publish — it's evidence the markup is well-formed, not that it does anything for ranking.

(other §8 subsections — §8.5 robots.txt through §8.14 programmatic SEO, incl. the §8.11 audit checklist and §8.12 rating/OG-preview tools: see seo.md)
