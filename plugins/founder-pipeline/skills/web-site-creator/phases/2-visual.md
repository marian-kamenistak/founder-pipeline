# Phase 2 — Visual Enhancement: design system + de-AI polish

Reference: [`references/visual.md`](../references/visual.md). Gates and mobile-layout fixes: [`references/gates.md`](../references/gates.md).

Runs after GATE 1. Sequential with Phase 3 (both touch layout/CSS files). Phase 4 (metadata) may run in parallel — it touches `<head>`/schema components only.

## 2.0 Design system (skip extraction if a brand kit was copied in Phase 1)

- [ ] [S] No kit existed: extract the brand's reference URL or brand PDF with `/founder-pipeline:firecrawl-scrape`, then hand-derive palette, type scale, spacing and radii into `tokens.json` + `DESIGN.md` in `/design/`; save a copy back into your configured brand-kit directory so the next build starts warm
- [ ] [S] When the site's design system evolves, sync changes back to that brand's kit (repo = source of truth; kit = portable copy)
- [ ] [S] Accent as tokens: `--color-accent` AND `--color-accent-dark` (hover) — never per-button hex; harvest palette free via `grep stop-color logo.svg`

## 2.1 Hard rules (audit every one — publish-blockers)

- [ ] [S] **No gradients, anywhere:** no gradient text/bars/numbers/borders/backgrounds. Flat solid brand colors only; depth from color blocks, spacing, imagery
- [ ] [S] **All client/partner logos at the SAME visual height** (fixed `height` + `width:auto`, contain in equal cells)
- [ ] [S] **Generous whitespace:** section padding ~120–160px desktop / 72–96px mobile; large gaps everywhere; when in doubt, add space. Pick a reference site whose spacing you admire, record it in `PLAYBOOK-CASE-NOTES.md`, and hold the build to it
- [ ] [S] **Type scale is GLOBAL** (h1/h2/h3 rules, never per-component) per `references/visual.md` → Default type stack; headings in a font with opinion, never Geist/Inter for h1/h2; fonts self-hosted via fontsource
- [ ] [S] **Every H1 carries 1–2 key words in the display/accent face.** Not just the home hero — every page, every H1. One uniform sans H1 is the single loudest "template" tell a page gives off, and the accent word is what makes a heading look art-directed instead of typed. Pick the words that carry the page's meaning, usually the keyword itself: on a `/mentor` page the H1 might be "An *engineering mentor* who has already done your job", with the serif on the two words the page is actually about. Two words is the ceiling; emphasising half the sentence emphasises nothing.

  Implementation note: pass the heading as a **pre / emphasis / post triple**, never as one interpolated HTML string. A component that takes `h1` as a plain string renders markup as visible text, so retrofitting emphasis means adding `h1Pre` / `h1Emphasis` / `h1Post` props and keeping the plain-string path as the default so existing callers stay byte-identical.
- [ ] [S] Re-audit imagery against Phase 1.3 rules (low-res, distortion) on every image added since
- [ ] [S] **Main cards default:** any primary card grid with photos puts the card **title ON the art**, bottom-left, over a `from-black/85 via-black/35` bottom scrim, in the site's **default heading text color**, semibold weight, plus a **text-shadow outline stroke** (stacked shadows at all 8 offsets, e.g. `-1px -1px`/`1px -1px`/`-1px 1px`/`1px 1px 0 rgba(<bg>,.85)` + a soft `0 2px 8px` drop shadow) — never reverse coloring, never `mix-blend-mode`. (A white + difference-blend treatment matching the homepage H1 was tried first and rejected: use the site's default heading color, at a heavier weight, with an outline for legibility over busy photos — verified in a browser against the actual source images, not assumed.) Plain `text-shadow` blur alone reads fuzzy at card-title sizes — the stroke is what keeps edges crisp; `-webkit-text-stroke` is not a substitute, it thins glyphs on non-Retina displays. When the card set is ordered, its position number renders top-left on the art as a **solid filled circle badge in the site's default neutral color** (e.g. `bg-text-heading`, dark text) — **not the brand accent color** — with a **thin border in the same dark color as the title's outline stroke** (e.g. `border border-[rgba(<title-stroke-rgb>,0.85)]`), so the badge and title read as one system and the badge doesn't wash out over a light patch of photo; never a bare data-point/stat in that corner; if the card set isn't ordered, omit the badge rather than inventing a number. Never a title row above/below the photo on a main card. Document the resulting pattern per-brand in that brand kit's `DESIGN.md` → "Main cards", and keep one reference implementation in the repo (e.g. a `.card-title-outline` utility) so later cards copy rather than re-derive
- [ ] [S] **Main card CTA:** the card's action ("Join the community", "See the dates"…) is the site's **default secondary button** (e.g. `.btn-secondary`), never an accent-colored text link with an arrow. If the whole card is already one `<a href>` to the same destination, render the button as a `<span>`/`<div>` carrying the button's visual classes, NOT a nested `<a>` or `<button>` — an interactive element inside an interactive element is invalid HTML. **Bottom-align the CTA across every card in a row with a two-part pattern, not `mt-auto` on the CTA alone:** an invisible `<div class="flex-1" aria-hidden="true"></div>` spacer as the last-but-one child absorbs all the leftover vertical space (guaranteeing every card's button lands on the same floor along a row), and the CTA itself carries a **fixed** top margin (e.g. `mt-6`) on top of that. `mt-auto` alone on the button, with no spacer, was tried first and failed on a card whose content nearly filled the row height: there was almost no leftover space for the auto margin to distribute, so the button crowded right up against the line above it. The fixed margin on the button is what guarantees a minimum gap regardless of how much (or little) the spacer had to give. Verify by screenshotting a full row with mixed content lengths, not one card in isolation.

## 2.2 De-AI pass (break the AI-built uniform, in impact order)

- [ ] [S] Accent used consistently: CTAs, link underlines, eyebrows, arrows, `::selection`
- [ ] [S] Real artifacts over polished cards — screenshots of the actual spreadsheet/Notion/thread (anonymized)
- [ ] [S] Break symmetry deliberately: alternate image sides, one oversized pull-quote, one bleed, ±1° rotation on collages
- [ ] [S] 2–3 hand-made touches max: marker-highlight on key phrases, handwriting-font mark (**never a scanned signature — forgery risk**), one annotated arrow near the CTA
- [ ] [S] No emoji-as-icons — real SVGs or nothing
- [ ] [S] At least two sections restructured away from the eyebrow → h2 → 3-col-grid skeleton
- [ ] [S] Nav wordmark in the display face; **if the site sits under a parent brand, the parent logo goes top-left** as a parent-brand + product lockup, bundled via `astro:assets`, ~32px, name drops below ~400px. Take the logo variant from the brand kit and match it to the nav background — kits ship a light-bg and a dark-bg variant and they are not interchangeable
- [ ] [S] Display-text lift: H1 + nav wordmark get soft neutral-gray `text-shadow` (~16% alpha, never accent-tinted); dark sections get glow, not shadow
- [ ] [S] Logo wall: grayscale at rest (~0.85 opacity), color on hover, END ON A FULL ROW — hide orphans; verify every harvested logo **visually on the deployed page** (inline SVGs lose `clip-path` defs, "logo-dark" files are white, `fill="#fff"` vanishes on light) — a curl 200 proves nothing; cache-bust repairs with `?v=2`
- [ ] [S] Blog covers audited: no duplicate covers, no confidential screenshots
- [ ] [S] **Footer = brand-dominance block** (`references/visual.md` §4.5): statement row → grouped link columns with mono eyebrows → giant domain wordmark in the display face cropped at the page edge → thin legal strip; exactly ONE signature interaction on the wordmark with touch + reduced-motion fallbacks

## 2.3 Mobile layout pass (`references/gates.md` §9.2 — PageSpeed passing ≠ layout good)

- [ ] [S] H1 in the first 100vh on mobile — reverse hero grid order if a collage sits first
- [ ] [S] Desktop-only decorative placeholders `hidden md:block`, grid rebalanced to full rows
- [ ] [S] Mobile section padding halved (`py-12 md:py-24`); grep for duplicated responsive prefixes (later wins silently)
- [ ] [S] Nav brand fits at 320px; tagline ≤30 chars or `hidden sm:block`; never `whitespace-nowrap` on brand text
- [ ] [S] 3-viewport pass: 320px (no overflow, taps ≥44px), 390px (H1 + CTA above fold), 768px (clean breakpoint) — screenshot top-to-bottom and read every screen

## GATE 2 → Phase 3

Hard-rules audit clean (2.1) · de-AI checklist complete · mobile 3-viewport pass done · design review round 2 run and every P0/P1/P2 finding fixed or skip-reason recorded in `PLAYBOOK-CASE-NOTES.md`, then re-verified. A review whose findings are never applied is theatre.
