# P4.S5 — Sales deck PDF → `P4-Build.S5-Deck.md` + project `deck/` folder

**Phase: P4-Build** (closes the phase)

**Earns its keep when** P4.S3 shipped a web surface with more than one offering to showcase (a catalog: workshops, products, tiers, services) — the deck is the thing the owner emails a warm lead to pull them onto the site. **Skip entirely** (one line in `brief.md` saying why) when: the stream is deck-only already, has a single offer with nothing to page through, or has no client-send motion (pure self-serve). A deck for a one-SKU self-serve product is performative — skip it.

**The job of this deck (do not forget it):** the PDF is bait, not the destination. Its one goal is to get the reader to open a page. Details live on the web; the deck teases and links. Short beats complete. Every offering slide and every CTA is a live clickable link into the site built in P4.S3.

**Hard gates:**
- **P4.S3 web is live and approved.** The deck sources its copy, prices, links, and photos from the shipped site — never invents its own. New connective copy (cover framer, section labels, CTA) routes through `/brand-voice` first (for a regulated-industry audience, take that skill's channel-flex override toward the more conservative register).
- **Reuse the site's real design tokens + real photography.** Brand-exact or it undercuts the site. Real event/product/people photos are the proof the thing exists — use many; no stock filler.

## Default build — HTML → PDF via headless Chrome. Always.

**A self-contained HTML/CSS deck rendered to PDF with headless Chrome (`puppeteer-core` driving the Chrome already installed on the machine), NOT a design tool.** This is the only path that gives pixel-exact brand match, real clickable link annotations, and one-command regeneration when prices or offerings change. A design tool gives you none of the three: the brand match drifts from the site, the links become flat text, and every price change is a manual re-export. **No Canva, no Figma export**, unless the owner explicitly overrides — and the override is recorded in `P2-Viability.S2-Tooling.md` with its reason.

**The generator's shape (build this; no reference implementation ships with the plugin).** One folder, `<project>/deck/`, holding four things:

1. **`build.mjs`** — the whole generator, one file. It (a) reads the *site's own* data files for the offering catalog — names, one-line promises, prices, page URLs — so the deck cannot drift from the site; (b) stages the chosen photos into a working directory; (c) renders an HTML string from a template plus that data; (d) drives Puppeteer to print it to `deck.pdf`; (e) copies the result into the site's static-assets directory so the next site deploy publishes it.
2. **A template** — the slide markup and all the CSS, inline in the generator or beside it. Self-contained: no build step, no framework, no external stylesheet.
3. **`assets/`** — the real photography and the brand SVGs, copied in (not linked out to a shared library that may move).
4. **`README.md`** — the one-command rebuild, where the data comes from, and any open placeholders.

The property that matters: **the offering catalog is read, never retyped.** A generator that hardcodes prices is a generator that ships a wrong price the first time you change one.

**Deck spine (scale slide count to the catalog):**
1. Cover — tagline + subhead reused from the site hero, one framer line, a premium photo, a few proof numbers.
2. Differentiators — the brand's "why us", led by the strongest one.
3. Trust — the client/logo wall exactly as the site shows it.
4..N. **One slide per offering** — name, one-line promise, program/contents as titles only (drive the click), format + price, a real photo, a clickable "see the full page →" into the live site.
N+1. Free/entry tier (if any) → its page.
N+2. The community/ecosystem slide (if any) → its URL.
N+3. Close — CTA: the real booking address + buy paths, one wedge line.

**Delegate the build (context-budget hard rule — see SKILL.md House rules).** Spawn ONE build subagent that reads the site's data/copy files, the brand tokens, and the photo library ITSELF on its own context, builds the generator, renders the PDF, and returns ONLY a compact summary — output path, slide count, embedded-link count (verify > 0 via `grep -a /URI`), file size, and any open placeholders. The main context never holds the slide copy or the photo set — only the summary and the gate verdict.

## Design recipe (what separates a premium deck from brand-exact slides)

Brand-exact colours and fonts are the floor, not the result. These are the moves that do the rest. Reproduce them.

**Canvas.** 16:9 landscape, exactly `1280×720` per `.slide` (`overflow:hidden; page-break-after:always`). `@page { size:1280px 720px; margin:0 }`. A dark-themed deck needs `-webkit-print-color-adjust:exact; print-color-adjust:exact` on `body` AND Puppeteer `printBackground:true`, or every dark background drops out white.

**Background photography — the core move.** Photos are the proof and the premium feel. Full-bleed them, but always keep text on a dark scrim so it stays high-contrast. Three patterns, pick by the photo's aspect ratio (check it first — `sips -g pixelWidth -g pixelHeight <file>` on macOS, `identify` or `ffprobe` elsewhere):

1. **Full-bleed hero / close / community-text slide** (photo aspect near 16:9, 4:3, or portrait). Two stacked layers under the text:
   - Photo layer: `position:absolute; inset:0; background-size:cover; background-position:center right` (bias the crop so faces/subject sit on the photo side, away from the text).
   - Directional scrim on top: `linear-gradient(90deg, rgba(3,6,9,.97) 0%, rgba(3,6,9,.9) ~46%, rgba(3,6,9,.4) 100%)` — substitute your own near-black. Text lives in a `position:relative` box above the scrim, width-capped to ~55–60% so it never collides with the subject.
2. **Split slide (one per offering).** Text column ~57% on solid dark (left); photo absolutely positioned on the right ~43%, full height, `background-size:cover`. Kill the hard seam with an `::after` on the photo that fades its inner edge into the page: `linear-gradient(90deg, var(--bg) 0%, rgba(3,6,9,.15) 22%, transparent 55%)`.
3. **Wide banner / collage (aspect wider than ~2:1, e.g. a group photo at 3.5:1).** DO NOT full-bleed cover-crop it — cover throws away ~half the width and centres on whatever is in the middle, killing the "full of people" point. Instead render it as a **full-width band at ~its natural height** (e.g. `1280×~320`) pinned to the top of the slide, with a bottom fade into the page (`::after { height:88px; background:linear-gradient(180deg, transparent, var(--bg)) }`), and put the slide's heading/stats/CTA on solid dark BELOW the band. This shows every face instead of a cropped sliver.

**Legibility guarantees.** Any small text that can cross a photo (per-slide footer: brand · site URL · page number) gets `text-shadow: 0 1px 5px rgba(3,6,9,.9)`. Keep the H1/H2 sitting on the darkest part of the scrim, never over the bright side.

**Photo selection rules.** (a) **No image used twice** — audit before render; pick the single best/most-premium shot for the cover and give each offering its own. (b) Real event/workshop/people photography only — it proves the program exists. (c) Match the photo's scene to the slide's theme. (d) **No off-brand artifacts, especially on the cover** — a predecessor brand's logo on a t-shirt, a rival's branded apparel in the crowd, a competitor's product on a laptop screen in shot. These survive review astonishingly often because nobody is looking at the shirts. Zoom in on the cover before you ship it, and swap the photo rather than crop around the problem.

**Rendering (puppeteer-core + the installed Chrome).** `executablePath` = the installed Chrome binary; `headless:true`; args `--no-sandbox --allow-file-access-from-files --font-render-hinting=none`. `page.goto('file://…deck.html', {waitUntil:'networkidle0'})`, then `await page.evaluateHandle('document.fonts.ready')` before `page.pdf({ width:'1280px', height:'720px', printBackground:true, margin:{top:0,right:0,bottom:0,left:0} })`.

**Fonts.** `@import` the site's own faces from a web font host (or embed them locally) so the render is self-contained and matches the site exactly. **If the deck carries accented or non-Latin glyphs — Czech and Slovak diacritics, Polish ogonek, Turkish dotless i, Greek, Cyrillic — verify the display face actually ships them before you commit to it.** Display and editorial faces frequently do not, and the failure is silent: the browser substitutes a fallback for the missing glyph only, so one word in a headline renders in a different typeface and nobody notices until the PDF is in a client's inbox. Name an explicit fallback face that does carry the range. `webp` photos load fine.

**Polish that reads as premium.** Chips for tier/level (filled accent for the flagship line, outline for the lighter one); a per-slide footer strip; accent-numbered lists for multi-part programs. **Delivery-language flags: inline SVG, never emoji** — Chromium's regional-indicator flag emoji render inconsistently in print. Hand-draw each flag you need as a small SVG, ~18×12, with a hairline `box-shadow` so a white field does not dissolve into a light card.

**Standing brand chrome on EVERY slide.** Source these from the site's own brand SVGs, in whichever light variant reads on dark:
- **Top-right:** the full brand lockup (mark + wordmark) at ~26px tall, sitting on a soft dark **radial scrim** (`radial-gradient(130% 130% at 65% 35%, rgba(3,6,9,.62), transparent 100%)`) plus a drop-shadow, so it stays legible over bright photo corners as well as dark panels. Without the scrim it washes out on light photos — this is a real fix, not a precaution.
- **Bottom-left footer:** the **mark only** (no wordmark), ~17px, immediately before the brand wordmark in the footer strip.
- **Third-party logos** (a chat platform, a video platform, a marketplace) appear wherever a slide names them. Use the official brand SVGs, keep them small, and keep the treatment consistent with the website's.

**Signature emphasis.** When the brand has one or two hero promises (a guarantee, a measured-outcome pledge), pull those cards hard to the front: accent border + glow + a filled accent number chip + a brighter card wash + a lit title, while the rest stay muted. "Highlighted" should be unmistakable, not a tint.

**Verify the render, don't trust it.** Clickable links: extract the sorted URI list via `grep -a -o 'https\?://[^)]*' deck.pdf | sort -u` and diff it against the offering manifest (every offering URL from the site's data file) — any missing URL = FAIL. A bare `/URI` count > 0 proves links exist, not that the RIGHT links exist; the diff is the gate. Screenshot the key slides (drive the HTML in headless Chrome, screenshot each `.slide`) and actually look — fonts loaded, backgrounds present, no text over the bright side of a photo, no duplicate image.

## Deploy + link (always — the deck is worthless unwired)

- **Serve it as a public asset on the SAME hosting surface as the P4.S3 site**, at a clean, no-extension URL — `<site>/deck` (or `<site>/<path>/deck`). Ship the file as `…/deck.pdf` in the site's static-assets directory, and front it with a route (or redirect) that serves `/deck` with `Content-Type: application/pdf` and `Content-Disposition: inline`. On an edge-worker host this is a path handler reading the asset and setting those two headers, with the worker taking the request ahead of static-asset serving for that route.
- **Link it from the site footer** ("Overview deck" / "Sales deck (PDF)") so it's discoverable, not just email-only.
- Rebuild is one command; document it in `deck/README.md`.

**Write to** `P4-Build.S5-Deck.md`: build log — generator location, live deck URL, slide count + link count, footer-link diff, offering-URL diff (site data file vs PDF URI list), rebuild command, open placeholders.

**Def-of-success — ALL must pass before Owner sign-off (fail → improvement loop per SKILL.md, never advance):**
- `/critical` run recorded on the rendered deck; score advisory (target ≥ 8/10) — the gate is the criteria below.
- Brand-exact: colors, fonts, and photo treatment match the P4.S3 site 1:1.
- Backgrounds follow the design recipe: full-bleed photos carry a dark text-side scrim (heading never on the bright side), wide banners render as bands not cover-crops, no image is used twice, and the cover has no off-brand artifact.
- Every offering slide + every CTA is a live clickable link into the site; the sorted URI list from the PDF contains every offering URL from the site's data file (diff against the offering manifest; any missing URL = FAIL).
- All copy traces to the approved site copy or a `/brand-voice`-passed new line — zero deck-invented claims, and honesty guardrails (unproven scores/logos labeled) preserved from source.
- Deck live at `<site>/deck` returning `200` + `application/pdf` inline; footer link shipped and resolving.
- Short enough to bait, not replace, the site — reviewer can name each slide's single job.
- ICP click test: `/critical`, roleplaying the P1.S3 persona, names the specific slide it would click and why; no named click = FAIL.

**Gate out (mandatory — see SKILL.md house rules):**
1. Deck rendered + deployed + footer-linked; link count and live headers verified. Re-read the site's data files at verification time and diff prices/URLs against the rendered deck — any mismatch = re-render before presenting. Add a `queues/manual-queue.md` row for a 90-day drift re-check (deck prices/URLs vs site data).
2. Invoke `/critical` on the deck — does it pull the reader to the site or try to be the site? Does any slide overpromise vs the live page? Would the P1.S3 ICP click at least one offering?
3. Fix; note what changed.
4. Present the live deck URL + link/headers proof + critical findings to the owner. **Wait for their explicit approval. Never auto-advance.**

**Checkpoint:** "Deck live at [URL], linked from footer, [N] slides, [M] clickable links. P4-Build phase complete — P5-Activation next: the launch actually executes (posts, registries, links)."

**Next:** `stages/P5-Activation.S1-Launch.md`
