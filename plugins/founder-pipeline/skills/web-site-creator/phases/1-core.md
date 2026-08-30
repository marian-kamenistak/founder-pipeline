# Phase 1 — Web Core: skeleton, content, pictures

Reference: [`references/core.md`](../references/core.md). Site-specific findings go in the repo's `PLAYBOOK-CASE-NOTES.md`, never here.

Steps marked **[P]** dispatch as parallel subagents the moment their inputs exist; **[S]** steps run in order in the main context.

## 1.0 Preflight (all must pass before scaffolding)

- [ ] [S] Positioning locked. Founder streams: Stages 00–12 approved — offer (`04_offer_ideation.md`), keyword contract (`11_keywords_content.md`), copy sources (`12_copy_content.md`); copy ships VERBATIM from the approved Copy sources section, new copy routes through `/founder-pipeline:brand-voice` and back into that file first. Standalone builds: a written brief with promise + audience + offer
- [ ] [S] Buying signal: founder streams — the pre-sale gate does NOT apply here; the web builds in every run. Standalone builds: confirm buying signal exists (discovery calls / LOI / pilot) or record the skip with the owner's sign-off
- [ ] [S] North star: one-sentence promise + primary CTA + secondary CTA — through `/founder-pipeline:brand-voice`; sanity-check with `/founder-pipeline:critical` before hero copy locks
- [ ] [S] Infra provisioned per the declared house stack. On the default stack that means: a paid CDN/edge account, the domain on that CDN's DNS, a private git repo, Node 22 + pnpm, `wrangler login`; register the Astro docs MCP (`claude mcp add --transport http astro-docs https://mcp.docs.astro.build/mcp`)
- [ ] [S] Brand kit: check your configured brand-kit directory FIRST — the path is a config value, recorded once in the repo's `PLAYBOOK-CASE-NOTES.md` (one subfolder per brand you build for, each holding `tokens.json`, `DESIGN.md` and type packages). Kit exists → copy those into the repo, done. No kit → extraction is a Phase 2 entry step; get the brand PDF or reference URL now
- [ ] [S] Newsletter tool chosen (e.g. Buttondown / Beehiiv / MailerLite / your email provider's broadcast product / a DB table + your transactional email provider) — before scaffolding
- [ ] [S] Image library located: point at your configured photo library and record the path in `PLAYBOOK-CASE-NOTES.md`. It needs a `catalog.json` (or equivalent index) carrying category/tags per image so a subagent can grep it — organise categories by the *subject* a page will need (events, community, one-to-one work, workshops, portraits). A brand with no photos at all = **blocker**, not a licence to ship an all-text design
- [ ] [P] **Research round 1:** founder streams — adopt the P4.S1 keyword contract (`11_keywords_content.md`) as round 1, don't re-derive. Standalone builds — **run `/founder-pipeline:web-keyword` Mode A (Contract)**; it owns the method, the localization table and the intent classification, and a generic research subagent produces none of those. Protocol and the rounds 2–3 sequence: [`phases/5-seo.md`](5-seo.md) → Research protocol. Also collect competitor pages and AI-citation sources. Build continues; results must land before page copy locks
- [ ] [P] **The page set in §1.2 is keyed to that contract, so round 1 gates it, not Phase 5.** Phase 5 is where ranking work is *finished*; it is far too late to be where the target terms are first *chosen* — by then §1.2 has fixed the routes and Phase 4 has written the titles against them. What round 1 must return before page copy locks: one primary keyword per planned page, no two pages sharing one (cannibalisation splits your own authority), and each term carrying real volume + difficulty + source. **Advisory, not a gate:** if the contract is thin or the site is brand new with no demand data, note the assumption in `PLAYBOOK-CASE-NOTES.md` and proceed — a missing number is a known risk to revisit in round 2, never a reason to stall the build
- [ ] [P] **Dispatch image curation** (subagent): grep the image library's `catalog.json` for the categories each planned page needs; copy matches into the repo — never hotlink across deployments

## 1.1 Scaffold

- [ ] [S] `pnpm create astro@latest` (minimal, strict TS); integrations via `npx astro add cloudflare partytown sitemap` — never manual config edits
- [ ] [S] `astro.config.mjs`: `site` = canonical production domain (never `*.workers.dev`); `output: 'static'`; `build.inlineStylesheets: 'always'`; explicit sharp image service with the Cloudflare adapter
- [ ] [S] `wrangler.toml` with ASSETS binding; secrets via `wrangler secret put`, never in the file
- [ ] [S] `public/_headers`: security headers only on `/*` (rules combine — a `Cache-Control` there defeats every per-path rule); never `no-store` on HTML (kills bfcache — use `public, max-age=0, must-revalidate` or omit); `immutable` on `/_astro/*`; `"run_worker_first": ["/api/*"]` or API GETs 404. Verify with the curl loop (`references/gates.md` §9.0) after every deploy
- [ ] [S] GitHub Actions deploy + Lighthouse CI + axe on every PR
- [ ] [S] Map `tokens.json` → `src/styles/tokens.css` `@theme` block; install the house type stack (fonts, global h1/h2/h3 scale — spec in `references/visual.md` → Default type stack)
- [ ] [S] Bilingual? Set up Astro i18n NOW (`prefixDefaultLocale: false`, secondary-locale tree, `lang` in content schema, hreflang in layout). Retrofitting is much harder. Locale URLs are prefix-style: `/<locale>/<slug>` (e.g. `/cs/<slug>`), never `/<slug>/<locale>/` (rule in `references/core.md` → Secondary-locale localisation)
- [ ] [S] Layout primitives, one file each, no abstraction until used twice: Section, Container, Heading, Prose, Button, Card, Nav, Footer, SEO, NewsletterForm, ContactForm

## 1.2 Pages + content (copy first, layout second)

**Every public string routes through `/founder-pipeline:brand-voice`.** If the brand has contested terminology — two words that mean nearly the same thing where picking the wrong one changes what you're selling (e.g. "partnership" vs "membership") — settle it ONCE in a wording file committed to the repo and load it here, rather than deciding ad hoc per page.

- [ ] [S] **No vague quantity words (hard rule).** "Many", "few", "often", "rarely", "most", "some" don't get quoted by AI search — LLMs and Google AI Overviews lift specific numbers, not qualitative hedges. Every quantity claim on the page gets a real, sourced number instead: dispatch a subagent to find a valid source (industry report, study, survey, official stat), then cite it as a numbered inline link at first use, or in an "Appendix: Sources" section below the content if it can't sit naturally in the copy. No source found → cut the claim; don't fall back to the vague word.
- [ ] [S] **DRY (hard rule):** anything on 2+ pages becomes ONE component in `src/components/`, driven by props/data (`src/data/`). Never copy-paste a section across pages
- [ ] [S] Home: hero promise → social proof → problem → solution → 3–6 outcome-first features → pricing teaser → real FAQ → final CTA
- [ ] [S] **Hero must-haves, all four (hard rule):**
  1. Hero content renders on first paint — NEVER behind a scroll-reveal; verify with a hard refresh, text present in the first frame
  2. At least one accent-colored word directly inside the H1
  3. Real social/brand icon row near the hero CTA when accounts exist
  4. The single strongest real number restated compactly beside the primary CTA
- [ ] [S] **Imagery floor (publish-blocker):** every page ≥2 real images; money page's hero (or next section) shows a photo or real artifact; social-proof imagery before the first CTA repeat; never monogram/`?` placeholder avatars
- [ ] [S] **Pre-testimonial fallback:** zero customer quotes yet ≠ exemption — fill the proof slot with real event/community/stage photos from the image library instead
- [ ] [S] Lead capture beyond the calendar link: primary CTA + one lower-commitment capture (newsletter / lead magnet / contact form); a "coming soon" magnet is a placeholder — cut it
- [ ] [S] Pricing page: run `/founder-pipeline:pricing` FIRST — no pricing copy below a 95/100 JTBD scorecard
- [ ] [S] About: outcome-based — what the owner did for people like the reader (numbers), why you, why now, who it's for, **who it's NOT for**
- [ ] [S] Persona/service pages: sticky-content pattern (`references/core.md` §20) — 90% reader problem / 10% credential, diary-entry blocks, "You've probably tried ✕", `Target:` lines, problem-anxiety FAQs
- [ ] [S] Each persona page pairs with 3–5 tightly-scoped blog scaffolds (`draft: true`, one per search query) with reciprocal links
- [ ] [S] Blog: Content Collection with zod schema (description 50–160 chars, `lang` field), MDX layout with author, dates, related posts, newsletter CTA
- [ ] [S] Testimonials: quotes carry an OUTCOME or number, verbatim excerpts, LinkedIn-verifiable, one per buyer tier; LP features 3 + links to /testimonials
- [ ] [P] **Dispatch translations** per finished default-locale page: translate the page into the secondary locale, run the result back through `/founder-pipeline:brand-voice`, and keep a `TRANSLATION-GLOSSARY.md` at repo root so recurring terms stay identical across pages. Line up a spellchecker that actually covers your target language before you start — coverage is uneven and the gaps are silent (worked example: LanguageTool has no Czech, so a Czech mirror needs a Czech-specific checker instead)

## 1.3 Pictures (rules apply to every image, every phase)

- [ ] [S] **Never low-res (hard rule):** source ≥2× largest CSS display size, never upscaled; blurry hero is worse than no hero — swap the photo. Measure before committing (`sips -g pixelWidth <file>`), don't eyeball. Images pasted into chat arrive downscaled (~900px is typical) — hunt the original in the image library first; if none exists, cap the CSS display width so the file never renders above native (a 900px photo is fine at ≤560px in a split hero, wrong as a full-bleed background)
- [ ] [S] **Never distorted (hard rule)** — check the ASSET and the CSS: (a) CSS: `object-fit: cover` + `aspect-ratio` (logos: `contain`); (b) pipeline: resize LONG EDGE only (`cwebp -resize 1600 0`, ImageMagick `-resize 1600x1600>` never `!`). After batch optimize: width == height on a photo ⇒ almost certainly squashed
- [ ] [S] Source images ≤2× display size, nothing over 500 KB committed; hero via `<Image>` `fetchpriority="high"`, everything else lazy; every `<img>` has explicit `width`+`height`
- [ ] [S] **Every image gets a real, descriptive `alt` (hard rule)** — never `alt=""` except a genuinely decorative image (background texture, divider) with zero content value. Write it from the section the image sits in, never from the filename: name what's actually depicted, then work in that page's or section's real target keyword/topic ONLY where it's true of the image — never stuffed, never a keyword bolted onto a generic description. A hero on a pricing page names the offer ("1:1 engineering leadership coaching session"), not "photo of people talking"; a speaker photo inside a case-study section names the event/topic it illustrates, not "founder speaking". A generic string (`"image"`, `"photo1"`) or a keyword crammed in with no real description fails this exactly like a missing attribute — same bar as `references/seo.md` §8.11's audit checklist, enforced here at build time instead of after the fact.

## GATE 1 → Phase 2

`npm run build` passes · all pages exist with real copy (grep dist for `[Placeholder|TODO|Lorem|TBD]` = zero) · imagery floor met on every page · hero must-haves ×4 present · every image has a real, descriptive `alt` (grep dist for `alt=""` and hand-check each hit is genuinely decorative; grep for `<img` / `<Image` without an `alt=` attribute at all = zero) · research round 1 results in `PLAYBOOK-CASE-NOTES.md`. Then run design review round 1 (structural — see SKILL.md review cadence) and start Phase 2. Phase 4 (metadata) may start in parallel from here.
