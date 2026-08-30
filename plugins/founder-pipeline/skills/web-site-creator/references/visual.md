# Web Creator Reference — Visual (design system, anti-slop, testimonials, cards, footer, type)

Part of the `/founder-pipeline:web-site-creator` reference set. Headings keep their original § numbers.


## Section anchors — every section gets a real `#name`

Every `<section>` on every page ships with a descriptive `id`. No exceptions, including legal
pages, thank-you screens and detail templates. Audited on one production site: 227 sections across
the whole site, and the pages built earliest were the ones missing them entirely (three whole
templates had zero) — the anchors get added when a page is designed, then never retrofitted unless
someone checks.

Why it earns its keep beyond deep-linking:
- **Support and sales.** "It's at example.com/partner#start-here" beats "scroll about
  halfway down".
- **Google jump-to-section links.** Google generates them from in-page anchors; no anchors, no
  chance of one.
- **Nav and in-page CTAs** stop being fragile — an anchor survives a section reorder, a scroll
  offset does not.
- **Analytics and bug reports** get a stable name to point at.

Rules:
- **Descriptive, kebab-case, stable**: `#what-you-get`, `#speaker-wall`, `#start-here`. NEVER
  auto-numbered (`#section-2` is useless to link to and breaks the moment the order changes).
- **Name it for what the section IS**, not where it sits. `#pricing`, not `#third-block`.
- **Locale mirrors reuse the SAME anchor**, so `/cs/join#what-you-get` resolves exactly like
  `/join#what-you-get`. A translated anchor is a broken link waiting to happen.
- **Add `scroll-mt-*`** on any anchor sitting under a sticky header, or the heading lands behind it.

Verify (run against the BUILT html, so component-generated sections are included):

```bash
python3 - <<'EOF'
import re, os
tot = miss = 0
for root, _, files in os.walk('dist/client'):
    for f in files:
        if f != 'index.html': continue
        h = open(os.path.join(root, f), encoding='utf-8').read()
        i, j = h.find('<main'), h.find('</main>')
        if i < 0: continue
        secs = re.findall(r'<section([^>]*)>', h[i:j])
        tot += len(secs); miss += sum(1 for s in secs if 'id="' not in s)
print(f'{tot} sections, {miss} without an anchor')   # miss must be 0
EOF
```


## 1. Extract the design system

**Goal:** produce `tokens.json` + `DESIGN.md` you can drop into the Astro project.

### From a reference website

Scrape the reference site (`/founder-pipeline:firecrawl-scrape <url>`, or any scraper you have),
then ask the agent to derive the system from what came back:

> *"From this page's markup and CSS, produce a `DESIGN.md` documenting colors, type scale, spacing,
> radii, shadows, component patterns and motion patterns. Report the values actually used, not an
> idealised system."*

### From a brand book PDF

Read the brand book (any PDF-to-text step; `Read` handles PDFs directly), then prompt the agent:

> *"Extract design tokens from this brand book. Output `tokens.json` with `colors`, `typography`,
> `spacing`, `radii`, `shadows`, `motion`. Use CSS variable names like `--color-brand-500`."*

### Tokens schema

```json
{
  "colors": {
    "brand": { "50": "#...", "500": "#...", "900": "#..." },
    "neutral": { "50": "#...", "900": "#..." },
    "accent": { "500": "#..." },
    "semantic": { "success": "#...", "warning": "#...", "danger": "#..." }
  },
  "typography": {
    "fontFamily": { "sans": "...", "serif": "...", "mono": "..." },
    "fontSize": { "xs": "0.75rem", "...": "..." }
  },
  "spacing": { "1": "0.25rem", "...": "..." },
  "radii": { "sm": "...", "md": "...", "lg": "...", "full": "9999px" },
  "shadows": { "sm": "...", "md": "...", "lg": "..." },
  "motion": {
    "duration": { "fast": "150ms", "base": "250ms", "slow": "400ms" },
    "easing": { "out": "cubic-bezier(0.16, 1, 0.3, 1)" }
  }
}
```

Check `DESIGN.md` and `tokens.json` into `/design/` in the repo.

---

## 1.5 De-AI the design (anti-slop pass)

AI-built sites converge on the same uniform: Geist/Inter everywhere, gray-and-white Tailwind palette, identical `rounded-2xl` cards in symmetric grids, every section shaped eyebrow → big heading → paragraph → card grid, everything fade-up animated the same way. Each choice is fine alone; together they read "generated" — especially to a tech audience that sees this uniform daily. Run this pass on every site BEFORE launch. First applied in production 2026-07.

**Checklist (in impact order):**

1. **Signature accent color, committed.** One brand color used consistently: CTA buttons, link underlines, eyebrow labels, "Read more →" arrows, `::selection`. All-black/gray chrome is the #1 tell. Pull the color from the brand's existing assets — `grep stop-color logo.svg` gives you the gradient palette for free. Define `--color-accent` AND `--color-accent-dark` (the hover) as tokens once; hardcoded per-button hover hexes WILL drift apart when the accent changes.
2. **Headings in a font with opinion.** Never Geist, Inter, or system sans for h1/h2 — those are the AI-era defaults. Keep a clean sans for body, but set headings in a characterful face (serif like Fraunces, or a display grotesque). Self-host via fontsource. A serif headline over a geometric body instantly reads "designed."
   - **Declare a house type stack once, in your configured brand kit, and reuse it across every property in your estate** unless an individual brand mandates its own type. A worked example of such a stack: `Geist Variable` body + `Geist Mono Variable` data + a characterful serif display face on **h1+h2 only**, with a `:root:lang(xx)` override for any locale the display face cannot render (see the glyph-coverage rule below). Keep it in one `global.css` you copy verbatim between sites — the imports, the subset selection and the per-locale swap are all load-bearing, and re-deriving them per site is how they drift.
   - This is a *house* style, not a generated default: it exists so the properties in one estate read as one family. It does NOT license reaching for it on a client brand that has its own type — that would be the exact convergence this section exists to prevent. Where a house stack overrides a parent brand's own spec, that must be a recorded, deliberate call by the owner, not a default.
   - **Verify glyph coverage for every non-English locale before committing to a display face.** Check the font's actual cmap (fontTools on the woff), not the fontsource subset list. *Worked example:* Shippori Mincho ships a "latin-ext" file that exists but holds only 10 non-letter glyphs, so Czech `č ď ě ň ř š ť ů ž` fell back per-character to Georgia and read as random bold letters *inside* H1 words. Fix pattern: keep the face for the primary locale, override `--font-display` via `:root:lang(xx)` with a covered look-alike (Playfair Display for a Didone) — `unicode-range` keeps the extra font off other locales' pages.
3. **Real artifacts over polished cards.** Screenshots of the actual spreadsheet, the actual Notion page, the actual message thread (anonymized). AI pages describe; humans show receipts. This is the most persuasive item and the only one needing client-supplied material.
4. **Break the symmetry deliberately.** Alternate image sides in repeating card lists. Make one testimonial an oversized pull-quote instead of N equal cards. Let one element bleed off the container edge. Add slight rotation (±1deg) to card collages — sticky-note energy.
5. **Hand-made touches, sparingly.** Marker-highlight effect (skewed yellow gradient background) on 2-3 key phrases. A handwritten-style mark under the About section, but NEVER a real scanned signature: a genuine signature on a public page is a forgery risk. Use a first-name-only doodle or a handwriting font instead. One handwritten-style annotation with an arrow near the main CTA. Two or three of these per site, not ten.
6. **One signature animation, not ten defaults.** Uniform scroll-fade-up on every section reads as a template setting. Keep reveals on 1-2 sections max. Replace decoration-animations with meaning-animations: logo walls grayscale→color on hover, live counters, a marquee.
7. **Never emoji-as-icons** on a professional site. Real SVGs or nothing.
8. **Set the nav wordmark in the display face.** The brand name in the header should use the same font as the headlines (same size as before) — ties the whole page into one system for one line of CSS.
   - **Where a site belongs to a parent brand: parent mark top-left, then the product name.** Open the nav with the parent brand's mark, then the product name in the display face — parent-brand mark + product name as one lockup, the whole `<a>` linking home. Take the mark from your configured brand kit, and **pick the variant cut for your nav's background**: kits typically ship a dark-ink cut for light backgrounds and a light/inverse cut for dark ones, and shipping the inverse cut on a white nav renders an invisible logo. Recipe: make `.nav__brand` an `inline-flex` with `gap` and `align-items:center`; logo `height:32px; width:auto; flex-shrink:0`; optional thin `1px` divider (`::before`, `height:20px`, `var(--n-200)`) between mark and product name; below ~400px `display:none` the product-name span but keep the logo. Bundle the SVG via `astro:assets` (`import brandLogo from '../assets/brand/logo.svg'` → `src={brandLogo.src}`) so it emits under the proxied `/assets/*` prefix (see §8.3 in metadata.md for why a root-level path breaks on split domains).
9. **Vary the section skeleton.** If every section is eyebrow → h2 → paragraph → 3-col grid, restructure at least two sections into a different shape (two-lane, full-bleed, pull-quote, timeline).
10. **No interaction-dead cards.** Every clickable card, pricing tier, and person row gets a hover state (lift + accent border + 150–200ms transition — the §1.8 recipe). A page where only the two buttons respond to the mouse feels static and templated; one production audit found zero hover affordance on any card across four pages and it read exactly like that. Non-clickable cards can stay quiet — but then nothing about them (cursor, arrow chip) should *suggest* clickability.

**CSS snippets that carry most of this:**

```css
/* marker highlight — apply to <span class="mark-hl"> */
.mark-hl {
  background: linear-gradient(104deg, rgba(250,220,80,0) 1%, rgba(250,220,80,.85) 3%, rgba(250,220,80,.55) 96%, rgba(250,220,80,0) 99%);
  padding: 0 .15em; margin: 0 -.05em; border-radius: .2em;
  -webkit-box-decoration-break: clone; box-decoration-break: clone;
}
::selection { background: var(--accent); color: #fff; }
/* logo wall: human hover */
.logo-wall img { filter: grayscale(1); opacity: .7; transition: filter .2s, opacity .2s; }
.logo-wall li:hover img { filter: none; opacity: 1; }
```

---

## 1.6 Harvested assets: logo walls + covers (gotchas that bit us)

Learned in production, 2026-07. When pulling client logos and images from company sites:

- **Inline-SVG extraction breaks silently.** An extracted `<svg>` that references `clip-path="url(#…)"` without carrying the `<defs>` renders as NOTHING in an `<img>` tag (invalid reference = element not rendered). Strip the clip-path or copy the defs. Also add explicit `width`/`height` to the root.
- **"logo-dark" means FOR dark backgrounds** — i.e. it's white and invisible on a light wall. Never trust filenames; check actual `fill` values (SVG) or sample opaque pixels (PNG) before shipping.
- **White fills hide on light walls.** `fill="#fff"` paths in a wordmark → replace with a dark neutral. The wall is grayscale anyway.
- **Cache-bust fixed assets.** After repairing a broken file at the same public URL, bump `?v=2` in the src — browsers and the CDN keep serving the broken one.
- **Logo wall spec:** grayscale at rest at ~0.85 opacity (0.65 reads "disabled"), color on hover, tight grid (6-7 cols desktop), and END ON A FULL ROW — hide orphan logos (comment them out) rather than leaving a one-logo row.
- **Verify every logo visually on the deployed page.** Three different invisible-logo failure modes in one afternoon; a curl 200 proves nothing about rendering.
- **Audit "first image = cover" blogs for two things:** duplicate covers across posts, and screenshots leaking confidential data — an unblurred client issue-tracker board once shipped as a featured image, publicly, for months. Real dashboards need a blur pass before they become covers, and a cover that came from a client's screen needs their sign-off as well.

---

## 1.7 Testimonials: selection, design, and the avatar mosaic

Distilled from production LP work, 2026-07.

**Selection (matters more than design):**

- Feature quotes that carry an OUTCOME or a number — a team size that changed, a hard decision the person can now name, a number they can point at — never attendance records ("provided guidance during my transition"). If the page promises money or promotions, the quotes must show money or promotions.
- One featured quote per buyer tier (CEO view, manager, C-level) so every visitor sees someone like themselves.
- Quotes are VERBATIM excerpts — trim with an ellipsis, never rewrite. Names, roles, companies must be LinkedIn-verifiable; link the profile.
- Full list lives on a /testimonials subpage grouped by seniority, with Review/ItemList JSON-LD schema. The LP features 3 and links down.

**Design:**

- Featured cards in a quiet neutral (cream/paper) with hand-made details (corner pins, ±1° rotation). Color belongs at ACCENT scale only — small quote tiles in a hero collage work; the same colors on poster-size cards read as a circus. Pull tile colors from the logo's gradient stops.
- Micro-quotes can live inside other sections: small colored note tiles in the hero collage, persona-matched quotes inside "who this is for" lanes.

**Avatar mosaic (the "wall of faces" pattern several SaaS homepages use) — high-delight, cheap to build:**

- ~100 small rounded avatar tiles (`w-8 rounded-lg`), grayscale + reduced opacity at rest, arranged in an organic shape via pattern strings (`'#'` = tile, `' '` = gap) — a world-map silhouette works. Rows are `flex justify-center`.
- Hover: tile pops to color, and a white tooltip card (photo, name, role, verbatim excerpt) appears via `group-hover` — pure CSS, no JS.
- Cycle people through tiles when tiles > people (`people[seed % people.length]`); every tile must resolve to a REAL person and quote.
- Edge-aware tooltip alignment (first cols `left-0`, last cols `right-0`, else centered) so cards don't run off-screen. `hidden md:block` — hover doesn't exist on touch.
- Close the section with the "See all N testimonials →" link BELOW the mosaic: cards argue, the mosaic shows scale, the link converts.

---

## 1.8 Clickable card grids: one persona-card design, reused site-wide

First built for an LP "pick your persona" grid, then reused for an About-page portfolio grid (2026-07). Any grid of clickable cards on the site uses THIS design — don't invent a second card language per page; two card designs on one site is an AI tell.

**The recipe (`ul.persona-cards > li > a.persona-card`):**

- Card: `rounded-2xl border border-neutral-200 bg-white p-6 pr-16` (the `pr-16` reserves space for the icon chip), `h-full` inside a `grid md:grid-cols-2 lg:grid-cols-3 gap-4`.
- Hover: `hover:border-accent hover:shadow-md hover:-translate-y-1 transition duration-200` — the whole card is the link; lift + accent border is the affordance.
- Icon chip: absolute top-right (`top-5 right-5`) circle `h-9 w-9 rounded-full bg-accent text-white` holding a diagonal ↗ arrow SVG; on hover it darkens (`group-hover:bg-accent-dark`) and nudges up-right (`group-hover:translate-x-0.5 group-hover:-translate-y-0.5`).
- Title `text-lg font-semibold group-hover:text-accent transition`; body `mt-2 text-sm text-neutral-600 leading-relaxed`. Optional CTA line at the bottom (`mt-4 text-sm font-medium text-accent`) when cards go to different properties and need scent — make the anchor `flex flex-col` with `flex-1` on the body so CTAs bottom-align.
- **First-card default highlight:** the primary card gets `.persona-card-first` — CSS paints it in the hovered state by default (accent border, shadow, lifted, darkened chip), and a `.persona-cards:has(.persona-card:not(.persona-card-first):hover)` rule drops it back to normal the moment the user hovers any OTHER card. Guides the eye to the primary action AND breaks the identical-tiles uniform without a differently-designed "featured" card. Ship the ~15-line `<style>` block alongside the grid — it's Astro-scoped, so each page carries its own copy.

---

(§4.5 below was extracted from "## 4. Pages" — the rest of §4 lives in core.md)

### 4.5 Footer — brand-dominance pattern

The footer is not a legal afterthought; it's the last brand impression and the page's confidence statement. Build three static HTML explorations of the variants below before committing one to the site — the pattern is cheap to prototype and expensive to retrofit.

**Anatomy, top to bottom:**
1. **Statement row** — one of: a grounded tagline in the display face (the brand's real sign-off, not invented), a "scoreboard" of 3 giant stats in the mono face (numbers do the dominance talking — **every stat must come from your verified metrics store or documented case notes**, never from a round number someone liked), or an outcome-led headline + CTA button (reader's problem, never "we" copy). All strings through `/founder-pipeline:brand-voice`.
2. **Grouped link columns** — 3–4 columns, mono-face uppercase eyebrows (11px, `letter-spacing: 0.14em`), links grouped by buyer intent (per-persona services / for-companies / explore / contact), the money link (`Pricing`, email) tinted accent.
3. **Giant wordmark** — the domain in the display face, spanning the full container width, **cropped at the bottom page edge**. This is the signature move.
4. **Thin legal strip** — legal entity, company registration number, address, socials. Dominance doesn't drop compliance.

**Wordmark recipe:**

```css
.wordmark-wrap { overflow: hidden; margin-bottom: -0.15em; /* crops descender zone at page edge */ }
.wordmark {
  font-family: var(--font-display); font-weight: 800;
  font-size: clamp(48px, 14.2vw, 240px);       /* ~14vw spans a 12-char domain edge to edge */
  letter-spacing: -0.03em; line-height: 0.9; white-space: nowrap;
}
```

Links home, gets an `aria-label="<domain> — home"`. Wrap the TLD in a `.tld` span so it can carry the accent color.

**ONE signature interaction — pick exactly one** (motion-budget rule from §5 applies):
- **Rise-in on scroll** (Monument): wordmark starts `translateY(105%)` inside the overflow-hidden wrap, IntersectionObserver adds `.is-visible` → `translateY(0)` over 1s `cubic-bezier(0.22,1,0.36,1)` (same easing family as the site reveals). Optional per-letter hover lift via JS-wrapped `<span class="ch">` letters.
- **Outline → fill** (Scoreboard): `color: transparent; -webkit-text-stroke: 2px <ink>` + accent gradient via `background-clip: text` with `background-size: 0% 100%` sweeping to `100%` on hover. Drop stroke to ~1.2px below 640px or it clogs.
- **Cursor spotlight** (Signature): two stacked copies — dim base (`#2c2c44`-class on dark) + gradient-clipped lit clone revealed through a `radial-gradient` `mask-image` positioned by `--mx`/`--my` CSS vars updated on `pointermove` (rAF-throttled). Park the spotlight off-canvas on `pointerleave`.

**Mandatory fallbacks:** no-hover devices (`(hover: hover)` false) get the finished state (fill/lit) via IntersectionObserver when the footer scrolls into view; `prefers-reduced-motion` gets the static end-state, no animation. The calm variant is a first-class design (skill bar, non-negotiable).

**Gotchas:**
- The crop margin is font-metric-dependent: -0.14em to -0.155em worked for Shippori Mincho 800; re-tune per display face so descenders clip, baselines don't.
- Footer links never replace primary Nav for revenue pages (§18 — footer-only starves crawl priority). The footer link grid is a mini-sitemap bonus, not the canonical path.
- Bilingual sites: the statement row and column eyebrows translate; the wordmark (domain) never does.

---

## Appendix B. Component patterns

### Hero
Grid: copy left 60%, visual right 40% on desktop, stacked on mobile. Primary CTA above the fold on mobile.

### Feature grid
3 columns desktop, 1 mobile. Icon, headline, 1-2 sentence body. Stagger entrance on scroll.

### Pricing table
3 tiers max. Middle tier highlighted. Annual toggle if applicable. CTA per column. FAQ directly below.

### FAQ
Accordion. First item open by default. Use `<details>` for free a11y.

### Blog card
Title, description, date, read time, tag chips. Hover lifts card 2px and adds shadow.

### CTA section
Full-bleed band, contrasting bg. One sentence + one button. Place before footer on every page.

---

## Default type stack + scale (house style)

**Source of truth is a `tokens.css` in your configured brand kit** — define the type scale there once and copy the block verbatim into each site, rather than re-deriving it per project.

Worked example of such a stack: body/UI `Geist Variable`, data/code `Geist Mono Variable`, display `Shippori Mincho` on **h1+h2 only** (h3–h6 stay sans — a Mincho at H4 sizes turns to mud). Scale, set as **GLOBAL h1/h2/h3 rules, never per-component**: `h1 clamp(48px,5vw,72px)/700/lh 1.05/ls -0.025em`, `h2 clamp(36px,4.5vw,60px)/700/lh 1.1/ls -0.025em`, `h3 clamp(24px,2.5vw,30px)/600/ls -0.025em`.

Three traps, all paid for in production:
(a) **Never size headings per-component** — one site had `.sec-title` redefined in NINE scoped blocks, so one section silently rendered at the browser default and they could never be kept in sync. Global rules + let genuinely-different scoped sizes win on specificity.
(b) **`ch` units move when the face does** — `ch` is the width of the font's `0` glyph, so a `max-width: 15ch` headline silently narrowed by 10% on a face swap (33.37px→30.00px per ch) and squeezed the hero into six short lines. Use `%`/`px`/column width for heading measure.
(c) **Do NOT reuse an oversized mission-headline clamp as the `h1` rule.** A `clamp(60px,5vw,92px)` intended for a one-off mission statement renders a 10-word `h1` at ~83px and pushes the hero CTA below the fold.

Per-locale display override, worked example: pages in a second locale override `--font-display` to `Playfair Display` via `:root:lang(xx)`, because Shippori Mincho carries no Czech glyphs (§1.5 item 2). Packages for the example stack: `@fontsource-variable/geist`, `@fontsource-variable/geist-mono`, `@fontsource/shippori-mincho` (latin+latin-ext 700/800 subsets ONLY — the full files ship ~265 KB of Japanese subsets), `@fontsource/playfair-display` (same subsets). Geist is body-only; headings carry an opinionated face (serif like Fraunces or a display grotesque) — never Geist/Inter for h1/h2.
