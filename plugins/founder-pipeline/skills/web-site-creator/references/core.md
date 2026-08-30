# Web Creator Reference — Core (prereqs, scaffold, pages, content, migration)

Part of the /founder-pipeline:web-site-creator reference set. Headings keep their original § numbers.

# Build a Product Site

A repeatable guide for shipping a marketing site for a new product, in a given design system, on your declared house stack.

**You finish with:** a fast, SEO-ready, AI-crawlable, animated marketing site (home + 3-5 pages + blog) deployed to a custom domain, with working contact and newsletter forms, off-site presence wired, and an MCP server exposing the site to AI agents. Roughly 3-5 focused days.

**This file is product-independent.** Rules and recipes live here; site-specific facts (keyword picks, competitor tables, backlink targets, niche SERP findings) live in a `PLAYBOOK-CASE-NOTES.md` file inside each site's own repo. When a research round or audit produces site data, write it to the case file, not here.

---

## Status: the web stage of the founder pipeline

This playbook is the default for any web asset built through `/founder-pipeline:founder` at its Web stage. When that stage is reached and the asset type is web, route to the `/founder-pipeline:web-site-creator` skill (this reference set).

**Scope includes sub-brand sections inside an existing repo.** A new product landing built as a page set + own layout inside an already-deployed site (e.g. a `/new-offer/` section inside an existing `example.com` repo) skips the scaffold phase but NOT the quality bars: imagery floor (§1.9), social proof, hover affordance (§1.5 #10), forms/lead capture (§6), per-product OG default (§8.11), mobile nav menu (§9.2), and the three design rounds (§17) all apply. This rule exists because a real section build silently bypassed all of them — "it's just a few pages in an existing repo" is how text-wall pages with the wrong OG image ship.

---

## Stack

**Declare your house stack once, at the start of the pipeline, then reference it everywhere.** The stack below is the recommended default and the worked example this whole reference set is written against. If you declare a different one, substitute consistently — but declare it explicitly and record the decision, so "which framework are we on" is never an open question mid-build.

Recommended default house stack:

- **Astro 5** with MDX and Content Collections
- **Cloudflare Workers** with Static Assets for hosting
- **Tailwind CSS** with tokens driven by your design source
- **Motion One** for animations, Astro **View Transitions** for page nav
- **Pagefind** for on-site search
- A **bot-protection service** for form spam (Cloudflare Turnstile in the default stack)
- A **transactional email service** (Resend in the default stack)
- A **product analytics platform**, instrumented before launch (PostHog in the default stack)
- **MCP server** exposing the site's content to AI agents
- Newsletter tool: **per-product choice** (see Section 6)

The rest of this file gives concrete commands and config for the default stack. Treat them as the worked example for whatever you declared.

---

## 0. Prereqs

- Cloudflare paid account, domain in Cloudflare DNS
- GitHub repo (private until launch)
- Node 22, pnpm
- Wrangler CLI authenticated: `wrangler login`
- Astro docs MCP registered in Claude Code (so the agent can pull live docs while building):

  ```bash
  claude mcp add --transport http astro-docs https://mcp.docs.astro.build/mcp
  ```
- Design source: brand book PDF, or a reference website URL
- Product north star: one sentence promise + one primary CTA + one secondary CTA. Run through `/founder-pipeline:brand-voice` before anything else.
- A product brief from the earlier `/founder-pipeline:founder` stages (ideation through approved copy sources). The site reflects positioning already locked there.

---

## 1.9 Imagery floor + default image library

This section exists because of a real audit: 3 of a section's 4 pages shipped with **zero images** — an entire premium-priced section running on one 120px circular photo — while dozens of catalogued brand photos sat unused one import away. A high-ticket offer page with no photos reads as a doc, not a product. This section makes imagery a hard floor, not a taste call.

**The floor (publish-blockers):**

- **No all-text public page.** Every page carries ≥ 2 real images: people, real artifacts (screenshots of the actual spreadsheet/board/thread), venue, or product. Color blocks, borders, and typography are seasoning, not the meal.
- **The money page's hero (or the section immediately after it) shows a photo or real artifact.** If the visitor can scroll the full first viewport without seeing a human or a receipt, the page fails.
- **Social-proof imagery on every money page:** at least one of {client logo wall, named testimonial with headshot, attributed outcome quote} above the first CTA repeat. A bare self-claim ("N+ sessions delivered") without a face or logo next to it reads as unverified.
- **Never ship monogram placeholder avatars.** An initials tile or a "?" circle where a face should be looks unfinished and erodes exactly the trust the page exists to build. Real photo, or restructure the section so no avatar is implied (describe anonymous experts in prose — don't render a fake person chip).
- **Circular avatar in a flex row → put the fixed size + `flex-shrink:0` on the flex ITEM, not the `<img>`.** When a `border-radius:50%` portrait is wrapped (e.g. an `<a>` linking to LinkedIn) and sits in a `display:flex` row, the wrapper is the flex item. If only the `<img>` carries `width/height/flex-shrink:0`, the wrapper still collapses, and the near-universal global reset `img{max-width:100%;height:auto}` then clamps the photo to the collapsed wrapper width → it renders as a **thin ellipse**. Fix: `.photo-wrapper{display:block;width:120px;height:120px;flex-shrink:0}`. This only bites in the bundled build (a shared/global stylesheet supplies the reset), not in `astro dev` — so verify avatars on the built output, not just dev.
- **A promised interactive asset ("take the self-assessment — opens in August") is a placeholder.** Cut the section until the thing is live; a dead soft-CTA trains visitors that the page over-promises.

**Default image library — builds pull from your configured brand kit:**

Maintain one shared asset library per brand you build for, and point this skill at it in your configuration. Any new site or section under that brand starts from the library instead of shipping text-only or hunting for new photos. The library is worth building once at the shape below — the categories are what a marketing site actually consumes:

| Need | Suggested location | Contents |
|---|---|---|
| Portraits / hero shots | `src/assets/pics/` (registry `src/assets/pics/index.ts`) | Typed photos — portraits, event/talk shots, 1:1 session shots, conference shots; each with a real `alt` |
| Hero / about | `src/assets/hero/` | Primary hero and about images, plus any location or credential badge |
| Testimonial headshots | `src/assets/testimonials/` | One headshot per named testimonial |
| Avatar mosaic faces | `src/assets/customers/` | Small avatars for social-proof mosaics |
| Real-artifact screenshots | `src/assets/artifacts/` | Product-proof shots — the actual dashboard, board, audit, or report |
| Company logos | `public/images/clients/` | Client or customer logos, webp + png, some svg |
| Stage/gallery | `public/images/gallery/` | Event and stage photography |
| Brand marks | `src/assets/brand/` | Logo and footer mark SVGs |

**Usage rules:**

- **Copy the files into the new repo's `src/assets/`** — never hotlink across deployments (a real audited page hotlinked its single photo from an unrelated preview deployment, which breaks the moment that deployment rotates) and never deep-import across repos. `public/` stays for verbatim-served files (logos, favicons, OG).
- **Reuse the registry pattern:** a `src/assets/pics/index.ts` that imports each photo once, tags it with a kind (`hero|portrait|action|talk|speaker|session`) and a human `alt`, and exposes `picsByKind()` — pages then *cycle real photos* through card lists instead of defaulting to text-only cards.
- **A brand with no library yet:** build the equivalent library in Phase 1.0 preflight (client-supplied shoot, harvested artifacts, licensed photos) BEFORE copy is written. If the photos don't exist yet, that's a preflight blocker to schedule — not a reason to design an all-text page.
- Optimization discipline unchanged (§8.11 Images): `<Image>` with explicit `width`/`height`, webp q80–85, LCP eager + `fetchpriority="high"`, everything else lazy.

---

## 2. Scaffold

```bash
pnpm create astro@latest my-product-site -- --template minimal --typescript strict
cd my-product-site
pnpm add @astrojs/mdx @astrojs/sitemap @astrojs/rss @astrojs/cloudflare
pnpm add -D tailwindcss @tailwindcss/vite @tailwindcss/typography pagefind
pnpm add motion zod posthog-js
```

### Wire integrations with `astro add`

Prefer `astro add` over manual `pnpm add` + config editing — it installs the package, updates `astro.config.mjs`, and runs any required setup prompts in one step.

```bash
npx astro add cloudflare    # SSR/static adapter for Cloudflare Workers
npx astro add partytown     # offload 3rd-party scripts (GA, PostHog loader, Turnstile) to a web worker
npx astro add sitemap       # generate sitemap-index.xml at build
```

If pnpm is the project manager: `pnpm dlx astro add <integration>`.

### `astro.config.mjs`

```ts
import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
import cloudflare from '@astrojs/cloudflare';
import tailwind from '@tailwindcss/vite';

export default defineConfig({
  site: 'https://your-product.com',
  output: 'static',
  adapter: cloudflare({ platformProxy: { enabled: true } }),
  // Locales: your primary language plus your home market's. The example below is a
  // worked case for an English-primary site with a Czech/Slovak home market — substitute
  // your own home market + primary export market.
  integrations: [mdx(), sitemap({ i18n: { defaultLocale: 'en', locales: { en: 'en-US', cs: 'cs-CZ', sk: 'sk-SK' } } })],
  vite: { plugins: [tailwind()] },
  experimental: { viewTransitions: true }
});
```

### `wrangler.toml`

```toml
name = "my-product-site"
compatibility_date = "2026-06-01"
main = "./dist/_worker.js/index.js"
assets = { directory = "./dist", binding = "ASSETS" }

[vars]
# One entry per service your house stack needs a credential for:
# transactional email, bot protection, newsletter, product analytics.
```

Secrets are pushed through your host's secret store (`wrangler secret put` on the default stack), never committed in this file.

### GitHub Actions deploy

`.github/workflows/deploy.yml`:

```yaml
on: { push: { branches: [main] } }
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with: { node-version: 22, cache: pnpm }
      - run: pnpm install --frozen-lockfile
      - run: pnpm build
      - run: pnpm dlx @lhci/cli autorun --upload.target=temporary-public-storage
      - run: pnpm dlx axe-cli http://localhost:4321
      - uses: cloudflare/wrangler-action@v3
        with:
          # Repository secrets you create in your own repo settings,
          # scoped to your own account. Never commit their values.
          apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          accountId: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
```

### Map tokens to Tailwind

`src/styles/tokens.css`:

```css
@import "tailwindcss";

@theme {
  --color-brand-50: ...;
  --color-brand-500: ...;
  --font-sans: ...;
  --radius-md: ...;
  --duration-base: 250ms;
  --ease-out: cubic-bezier(0.16, 1, 0.3, 1);
}
```

---

## 3. Layout primitives

Build these once, use everywhere. One file per primitive. No abstractions until you use a thing twice.

```
src/components/
  Section.astro     # vertical rhythm + max-width
  Container.astro   # horizontal padding
  Heading.astro     # h1/h2/h3 with type scale
  Prose.astro       # MDX body wrapper
  Button.astro      # primary/secondary/ghost, with loading state
  Card.astro
  Nav.astro         # sticky, scroll-shrink, mobile drawer
  Footer.astro
  SEO.astro         # canonical, OG, Twitter, JSON-LD
  NewsletterForm.astro
  ContactForm.astro
```

---

## 4. Pages

Each page starts with copy. Route every word through `/founder-pipeline:brand-voice`.

### Home (`src/pages/index.astro`)

1. Hero: one-sentence promise, sub-line, primary CTA, secondary CTA, hero visual
2. Social proof: logos or specific numbers
3. Problem: the moment your reader recognises themselves
4. Solution: how the product changes that moment
5. Features: 3-6, each with outcome-first headline
6. Pricing teaser: anchor + link to pricing page
7. FAQ: 5-8 questions, real ones
8. Final CTA

### Product / Features (`src/pages/product.astro`)
Deeper feature explanations, screenshots, short demo video or loom embed.

### Pricing (`src/pages/pricing.astro`)
Run through the `/founder-pipeline:pricing` skill first. Don't ship pricing copy without the JTBD pass.

### About (`src/pages/about.astro`)
**Outcome-based, not just factual.** The About section is about the reader, not a résumé. Lead with what the owner *did for people like them and can do for them* — the change they create — backed by specific outcomes and numbers, before any credential or bio timeline. Facts (roles, years, logos) exist to make the outcome believable, not to stand alone. Then: why you, why now, who it's for, who it's not for. The "not for" line is the one that makes the rest believable.

Test each sentence: does it tell the reader what *they* get, or just what the owner *is*? Rewrite the second kind into the first ("20 years in the industry" → "I've helped 40+ leaders move from stuck to promoted — and I've been in the seat myself for 20 years").

### Blog index (`src/pages/blog/index.astro`)
List from Content Collection, filter by tag, paginate at 20.

### Blog post (`src/pages/blog/[slug].astro`)
MDX layout, author bio, published + updated dates, related posts, share buttons, newsletter CTA at end.

### Contact (`src/pages/contact.astro`)
ContactForm component, alternate channels listed (email, LinkedIn, Calendly link if you offer calls).

(§4.5 Footer — brand-dominance pattern: see visual.md)

---

## 7. Content + blog

### Content Collections

`src/content.config.ts`:

```ts
import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const blog = defineCollection({
  loader: glob({ pattern: '**/*.mdx', base: './src/content/blog' }),
  schema: z.object({
    title: z.string(),
    description: z.string().min(50).max(160),
    pubDate: z.date(),
    updatedDate: z.date().optional(),
    author: z.string(),
    tags: z.array(z.string()).default([]),
    ogImage: z.string().optional(),
    draft: z.boolean().default(false),
    // Your primary language plus your home/export market languages.
    lang: z.enum(['en', 'cs', 'sk']).default('en')
  })
});

export const collections = { blog };
```

### OG images — one template, real library photos, made per page (not auto-generated)

Every indexable page needs its own OG image before it ships, or it silently inherits the layout's generic hero photo — the same failure mode as the sub-brand `ogImage` leak in §8.11, just on a single page instead of a whole section. A real page shipped for a full day on the generic hero because nothing forced the per-page image or caught the fallback (root cause + fix: `${CLAUDE_PLUGIN_ROOT}/skills/web-site-creator/references/seo.md` → OG image coverage).

**A Satori/`astro-og-canvas` build-time generator is the theoretical option but not what ships in practice** — these are hand-designed static assets, because the template leans on a real event/community photo (not a title-on-gradient card a generator produces) and a human still has to crop the right photo to the right subject. Don't scaffold a generator unless a site genuinely has too many pages to hand-design (100+, e.g. programmatic SEO §8.14) — for the normal 5–35 page site, design them.

**The template (dark background, 1200×630):**
- Brand logo, top-left
- Small uppercase eyebrow/category label (e.g. `CALL FOR SPEAKERS`)
- Large bold headline, 2 lines max — the page's actual locked H1 or hero line, not a generic restatement
- One-sentence subtitle below it
- Short gradient divider line
- Location / tag text, bottom-left (e.g. a city list, if the offer is geographically anchored)
- A real photo occupying the right ~40% of the canvas — pulled from this project's own brand-kit image library (§1.9), never a stock photo. Crop to the subject, not a random frame.

**Build once in a design tool as a reusable template** — duplicate it per page, swap the photo and the two text blocks, export. Don't hand-code a new template each time; the whole point is one shared layout with two swappable slots. If you have the Figma or Canva MCP plugins installed (each an optional dependency you install separately), they can generate and export these directly.

**Never stretch the photo — crop it, always preserving its native aspect ratio.** Resizing the photo panel's container to a non-native aspect ratio (e.g. via a `preserve_aspect_ratio: false` resize call, or any resize that doesn't also recompute the image's internal crop box) squashes people and objects into visibly wrong proportions — caught on a first production card, where the container was resized to the panel's target box but the image fill inside it kept its old crop mapping, stretching the photo vertically. The fix is a cover-style crop, computed from the source's real aspect ratio: scale the image so it fully covers the panel on the constraining dimension (usually height), then center-crop the overflow on the other dimension — never scale width and height independently to force-fit the box.

**Export + wiring:**
- Export at exactly 1200×630, `.webp`, under 300 KB (§8.11 Images).
- Save to `public/gallery/<page-slug>/og-<page-slug>.webp` — one directory per page slug, so the card sits next to the page it belongs to.
- Pass the path via the layout's `ogImagePath` prop (or equivalent) on that page — never rely on the layout default.
- Always emit `og:image:width=1200`, `og:image:height=630`, `og:image:alt` alongside it.

**Sequencing — don't build this at GATE 1.** The headline and subtitle are baked into the exported image, so building it before copy is voice-passed and locked means redesigning it every time copy changes. Phase 4 rule + GATE dependency: `${CLAUDE_PLUGIN_ROOT}/skills/web-site-creator/phases/4-metadata.md`.

---

## 20. Sticky content style — the operator-newsletter playbook

Every persona / service / role landing page follows this pattern. Extracted from a `/founder-pipeline:critical` review of production persona pages that surfaced a 50/50 me/reader ratio and consultant-marketing tone. (Examples below are from one worked build in a single niche — swap the specifics for your niche; the moves are universal.)

### The 6 mandatory moves per persona / service page

**1. 90/10 rule.** Hero and body are 90% reader problem, 10% your credential. Credentials move to a slim "Why me" strip near the bottom of the page. Kill the repeating headline stat (a cumulative-volume number, e.g. "N+ sessions delivered") from the hero of every page. State it **once**, at the bottom.

**2. Diary-entry situation body.** The situation description is the reader's own first-person internal monologue, quoted, italic, indented:

```html
<blockquote class="mt-5 border-l-2 border-neutral-300 pl-5 text-neutral-700 italic leading-relaxed">
  It is Sunday, 9pm. I spent 40 minutes in a 1:1 with an engineer who is not shipping. 
  I have another 4 direct reports and I still owe my CTO a hiring plan.
</blockquote>
```

Never write "You inherited an org that runs on autopilot the wrong way." Write it as if the reader is journalling: `It is Tuesday. The prior CTO left three months ago and I still cannot answer "what do we own on the platform" without a caveat.`

**3. "You've probably tried" bullets.** Under each situation title, list 3-5 things the reader has already attempted and why each failed. This is the single highest-stickiness move because it proves recognition. The reader thinks "wait, do they know me?"

```
✕ Reading The Manager's Path on the weekend
✕ Copying 1:1 templates from LinkedIn
✕ Asking your peer EM what she does (she is drowning too)
✕ Blocking Fridays for "strategy" that gets eaten by meetings
```

**4. Tackle block with measurable outcome.** Every situation gets a "how we tackle it" that ends with a specific `Target:` line. Never abstract "we design a plan." Always: `Target: 80%+ sprint completion by week 12` or `Within 4 weeks: the specific conversation delivered, a number in writing, a documented fallback plan.`

**5. Problem-anxiety FAQs, not credential-anxiety FAQs.** Kill these: "NDA?", "what company size?", "how are you different from a business school?". Replace with:
- "What if my situation is weird and does not fit anything on this page?"
- "What if I only have 3 or 4 sessions to figure something out?"
- "Will you actually tell me to fire the guy, or will you just ask me questions?"
- "What if the real problem is my director, not my team?"

Credential-anxiety questions are what a prospect who ALREADY trusts you asks. Someone landing from Google search has problem-anxiety, not credential-anxiety.

**6. Varied hero opener per persona.** Never the same "You are the person the board asks…" pattern six times. Each persona page gets a unique diary-fragment hook. Reader fatigue triggers when they realize the pages share the same template voice.

### The blog-scaffold pattern

Landing pages are **landing zones**, not primary content. Each persona / service page pairs with 3-5 tightly-scoped blog posts:

- One blog post per specific search query the reader would type. E.g. "How to handle a chronic underperformer as a first-time EM" beats "Engineering Manager tips."
- Scaffold shipped as `draft: true` MDX with title + description (50-160 chars per content.config.ts schema) + intro fragment + H2 outline + TODO markers + related-blog links + a link back to the persona page.
- The reciprocal link on the persona page is a "Related reads" pill row per situation, deep-linked to the exact blog post that goes deeper on that situation's tackle.

### The persona-page component structure (Astro)

```
PersonaPage.astro
├── Hero (varied opener, 90% reader problem, 10% credential)
├── Situations (per-situation card)
│   ├── Title
│   ├── Diary-entry body (italic, border-left, quoted)
│   ├── You've probably tried (✕ bullets)
│   ├── Tackle block (bg-neutral-50, teal label) + Target: line
│   └── Related reads (pill row of blog links, hover states)
├── Topics (10 questions the reader would type)
├── Method (3 steps: intro → session 1 → cadence)
├── FAQs (problem-anxiety, not credential-anxiety)
├── Other personas (SEO internal linking)
├── Why me (SINGLE strip at bottom, portrait + 2 short paragraphs)
└── CTA (calendar + email)
```

### Anti-patterns this section catches

- Hero opens with credentials. Should open with reader's inner monologue.
- Every persona page repeats the same credential stat. Move to Why-me strip. Say it once.
- Situations described in third person ("You inherited…"). Should be first-person quoted diary.
- Tackle blocks that end with "we design a plan." Add measurable `Target:` line.
- FAQ list about the seller's process. Should be about the reader's problem-anxieties.
- Six persona pages with identical hero opener. Vary the diary fragment per role.
- Persona page as primary content. Should be landing zone with 3-5 tightly-scoped blog scaffolds per persona.
- Blog posts written before persona pages exist. Persona page first, then scaffold the 3-5 blog posts that go deeper into the tackle.

### When NOT to use this pattern

- Non-persona service pages (audit, workshop, event registration). Those have different intent shapes.
- Landing pages driven by paid ads (LP for a specific campaign). Those need a different scaffold (see `/founder-pipeline:pricing` and Section 8).
- Utility pages (privacy, terms, sitemap). Not content pages, don't over-engineer.

### Reference implementation

The build that first shipped this pattern used one shared persona-page component, 6 persona pages, and 19 paired blog scaffolds. Record your own equivalent in your site's case file.

---

## Appendix A. Copy prompts per page

Every prompt routes through `/founder-pipeline:brand-voice` first.

### Hero
> Write a one-sentence promise for [product]. Reader is [audience]. Their specific moment of need is [moment]. Outcome they get is [outcome]. No corporate words. No "we help you". Lead with the outcome.

### Problem section
> Describe the moment my reader recognises themselves. Make it specific enough that the wrong reader bounces. 60-100 words.

### Features
> For each feature, write a headline that names the outcome, not the capability. Then a 1-sentence proof.

### FAQ
> Write 6 real questions a [persona] asks before buying. Answer each in 2-4 sentences. Include the uncomfortable ones.

### Pricing
> Run the `/founder-pipeline:pricing` skill first. Don't write pricing copy until JTBD scorecard is 95+.

### Secondary-locale localisation
> Produce local-language variants of every public string. If you have a dedicated translation skill installed, use it; otherwise translate inline, then re-run `/founder-pipeline:brand-voice` on the translated output so it sounds like the brand, not machine translation. (A page-level translation skill is an optional extra — the inline path is sufficient.)
>
> **URL scheme rule: locale is a PREFIX, never a suffix.** `/cs/<slug>` (e.g. `/cs/services/`), NOT `/<slug>/cs/`. Same for every other locale. Every new site follows this from day 1. Existing suffix-style URLs are legacy and migrate wholesale with 301s at cutover, not piecemeal — record the decision in your own decision log.
>
> **One flag governs hreflang AND the language switcher.** A page either has a real mirror or it does not, and that single fact decides three things: whether to emit the `hreflang` pair, whether to render the switcher, and whether the mirror belongs in the sitemap. Wire them to the same prop (`hasAltLocale` or equivalent). Google's own guidance is to omit `hreflang` rather than point it at an untranslated page, and the switcher deserves the same discipline for a harder reason: **it derives the sibling URL from the current pathname, so it cannot know whether that page was ever built.** Rendered unconditionally it ships a 404 in the site header. One production site did exactly that on roughly two thirds of its pages — every event page plus `/blog`, `/privacy`, `/code-of-conduct` and a pricing sub-page — while every one of those pages had the flag set correctly. The flag existed; the switcher just never read it. (This warning previously lived only in the geo/programmatic-pages section, where nobody building an ordinary bilingual site would ever find it.)
>
> **Every shared component derives hrefs from the current locale.** Nav, footer, CTAs, cards — anything rendered on both locales. A hardcoded `/pricing` in a shared footer sends every Czech reader back to English on their first click, and it will not show up in any build error. Two failure shapes seen in production: hardcoded default-locale paths in `Nav.astro`/`Footer.astro`, and a hand-maintained allowlist of "slugs that have a mirror" that silently went stale the moment a new mirror shipped. Prefer deriving from the routes that actually exist; if you must keep a list, make a miss loud rather than silent.

---

## Appendix E. Skills to invoke during the build

Skills prefixed `/founder-pipeline:` ship with this plugin. Skills prefixed with another namespace (`posthog:`, `cloudflare:`, `frontend-design:`) come from public plugins you install separately — each is an **optional dependency**; if it isn't installed, do the inline fallback in the Notes column and flag that you did.

| Stage | Skill | Notes |
|---|---|---|
| Copy (every page) | `/founder-pipeline:brand-voice` | Mandatory, non-negotiable |
| Design extract from URL | `/founder-pipeline:firecrawl-scrape` | Scrape the reference site, then read its colours, type scale and spacing off the returned markup |
| Design extract from PDF | — | No skill ships for this. Read the brand book directly and transcribe tokens by hand |
| Pricing copy + tiers | `/founder-pipeline:pricing` | Won't ship below 95/100 |
| Page-level review | `frontend-design:frontend-design` (optional) | 3× during build — see Section 17. Without it, run the §17 checklist by hand |
| Positioning sanity check | `/founder-pipeline:critical` | Before hero copy is locked |
| SEO audit | `/founder-pipeline:seo-audit` | Pre-publish |
| Web perf | `cloudflare:web-perf` (optional) | Pre-publish. Without it, run Lighthouse and read Core Web Vitals directly |
| AI SEO | `/founder-pipeline:ai-seo` | Pre-publish |
| Keyword + AI-search research | `/founder-pipeline:web-keyword`, plus general-purpose subagents for open-ended research | 3× during build — see Section 18 |
| Backlink target discovery | `/founder-pipeline:web-backlinks` | Once at build, then every 90 days — see Section 19 |
| Translation | — | No skill ships for this. Translate inline, then re-run brand voice on the output |
| Long-form review | `/founder-pipeline:critical` | For blog posts and pricing copy |
| Final voice pass | `/founder-pipeline:brand-voice` | Last gate before publish |
| Instrumentation | `posthog:instrument-product-analytics` (optional) | Before launch, not after. Without it, wire your analytics SDK by hand against its own docs |
| MCP server scaffold | `cloudflare:build-mcp` (optional) | Section 13. Without it, scaffold from your host's MCP template |

---

---

## 15. Migrating from an existing WordPress site (real playbook, not theory)

If you're replacing an existing WP site (not a green-field build), follow this exact order. Skipping steps causes multi-hour outages — every warning below was hit in production during a real bilingual migration of a mid-sized site.

### 15.1 Never point new-site DNS at production before content parity

- Keep the old WP site alive on its current domain.
- Build the new Astro site on a `*.workers.dev` subdomain first.
- Only switch DNS once you have ≥ 90% content parity (see 15.4).

### 15.2 Archive the old WP to a separate domain

If the old site was `brand.com`, decide the archive hostname before touching anything: e.g. `old.brand.com` OR a totally separate domain like `brand-archive.tld`.

Order of operations:
1. **Add new DNS zone** for the archive domain at your DNS provider.
2. **Add A + AAAA records** for the archive domain pointing at the current WP host's origin IP.
3. **CRITICAL: add a `mysql.<archive-domain>` A record** pointing at your host's MySQL server IP. WordPress cannot boot without DB, and on many shared hosts the MySQL hostname it uses is a subdomain of the site itself. Set it DNS-only (unproxied) — an HTTP proxy blocks port 3306.
4. **In your host's control panel: add the archive hostname as an alias** to the same WP install. Otherwise the web server serves the default vhost and PHP returns empty 500s.
5. **Update `wp-config.php`** on the origin server: set `WP_HOME` and `WP_SITEURL` to the archive domain OR update the DB rows.
6. **Also check `.htaccess` for `php_value` directives** — these require `mod_php`. Hosts running PHP-FPM return 500 on every PHP request when a `php_value` directive is present. Move settings to `.user.ini` instead.
7. **Check `.user.ini` for `auto_prepend_file`** — Wordfence and similar plugins hard-code the old site's path. If the path is stale (points at old domain's directory that no longer exists), every PHP request 500s empty. Update the path or comment out the line.

Verify the archive site works fully before touching the primary domain:
```bash
curl -I https://archive-domain.com/
curl -I https://archive-domain.com/blog/
curl -I https://archive-domain.com/services/
```
All must return 200. If not, do NOT proceed to 15.3.

### 15.3 Attach primary domain to the new Astro Worker

Once archive is stable at 200:

1. **Delete existing A + AAAA records** for the primary domain in Cloudflare. Cloudflare's Worker Custom Domain API refuses to auto-manage a hostname that already has "externally managed DNS records" — you must delete them first.

   Via API. Note the permission trap: **DNS-record editing is a narrower scope than general zone editing**, and a token that can deploy the Worker very often cannot delete the record blocking it. Check the scope before you assume the call failed for another reason. Use a token from your secrets store with DNS-edit scope on the zone:
   ```bash
   ZONE_ID="..."
   # List records
   curl -H "Authorization: Bearer $DNS_EDIT_TOKEN" \
     "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records"
   # Delete each A + AAAA for primary and www
   curl -X DELETE -H "Authorization: Bearer $DNS_EDIT_TOKEN" \
     "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records/<record_id>"
   ```

2. **Add routes to `wrangler.jsonc`:**
   ```jsonc
   "routes": [
     { "pattern": "brand.com", "custom_domain": true },
     { "pattern": "www.brand.com", "custom_domain": true }
   ]
   ```

3. **Rebuild and deploy.** The `@astrojs/cloudflare` adapter regenerates `dist/client/wrangler.json` at build time — if you edit `wrangler.jsonc` and deploy without rebuilding, the routes are NOT picked up. Always `npx astro build` before `wrangler deploy`.

4. **Cloudflare auto-creates the DNS records** for the Worker on the primary hostname. Verify at 200.

### 15.4 Content migration (WP → Astro MDX)

For every URL on the old WP site indexed by Google, you need one of:
- Native replacement on new site
- 301 redirect to new location
- 301 redirect to archive domain

Do NOT rely on WP → Astro auto-migration tools. They break on custom fields, Gutenberg blocks, embedded shortcodes, and image references. Manual is more reliable.

**Scrape all old URLs:**
```
# Enumerate every URL first — from the old site's sitemap.xml, or by crawling it.
/founder-pipeline:firecrawl-scrape <url>   # per-page content
```

**Batch-scrape 30+ posts in one invocation** — the scraper is rate-limited but handles concurrent URLs. Store scraped markdown in a gitignored working directory.

**Convert to MDX with frontmatter — Python script pattern:**
```python
# Extract title, description, pubDate from live page's og: meta tags
# Not from firecrawl markdown — WP theme cruft breaks the extraction
html = requests.get(url).text
title = re.search(r'article:published_time"[^>]*content="([^"]+)"', html).group(1)
```
- Strip WP-specific noise: "Skip to content" links, related-post footers, WP nav breadcrumbs, share-widget markup.
- Clamp `description` to ≤160 chars (content-collection schema requirement).
- Decode HTML entities (`&#039;` → `'`, `&nbsp;` → space).
- Strip trailing brand-name suffixes (" — Founder Name" or similar) from titles.

**MDX-specific pitfalls that will break your build:**
- **Curly braces in prose.** MDX parses `{...}` as JSX expression. WP posts often include stray JSON in image alt text (breadcrumb schema leaks). Escape all `{` → `\{` and `}` → `\}` in body content before writing MDX. Only outside code fences.
- **YAML quote escaping.** If a `description:` value contains an unescaped `"`, YAML frontmatter blows up. Replace inner `"` with `'` or use single-quoted YAML strings.
- **Blog post frontmatter `description` too long.** Content-collection schema in `src/content.config.ts` requires `description: z.string().min(50).max(160)`. Post-process descriptions to fit.

**Redirect map:**
- Put a `public/_redirects` file at repo root.
- Cloudflare Workers Static Assets format: one rule per line, `<source> <destination> <status>`.
- **CRITICAL: no `/*` catch-all rules.** Cloudflare Workers evaluates `_redirects` BEFORE serving static assets. A `/*` rule at the bottom will 301 EVERY page — including your live home page — to the destination. This is a production outage. Use only explicit-path rules.
- No wildcards on Static Assets. Format:
  ```
  /old-slug/               /blog/new-slug/           301
  /contact/                /                          301
  /courses/                https://archive.com/courses/   301
  ```

### 15.5 Bilingual (i18n) setup

If the old WP site had a `/cs/` (or other language) prefix, you need Astro i18n from day 1 — retrofitting it later is much harder.

**Locale URLs are prefix-style, always:** `/cs/<slug>`, not `/<slug>/cs/` (see the URL scheme rule in "Secondary-locale localisation" above). The trees and code below already follow this; do not invent a suffix variant even when mirroring a single standalone page.

**Config:**
```javascript
// astro.config.mjs
i18n: {
  defaultLocale: 'en',
  locales: ['en', 'cs'],
  routing: {
    prefixDefaultLocale: false,       // EN pages at /, not /en/
    redirectToDefaultLocale: false,
  },
},
integrations: [
  sitemap({
    i18n: {
      defaultLocale: 'en',
      locales: { en: 'en-US', cs: 'cs-CZ' },
    },
  }),
],
```

**Directory structure:**
```
src/pages/
  index.astro             # EN home
  services.astro          # EN /services/
  cs/
    index.astro           # CS home at /cs/
    services.astro        # CS /cs/services/
  blog/[...slug].astro    # EN blog posts
  cs/blog/
    index.astro           # CS blog index at /cs/blog/
    [...slug].astro       # CS blog posts at /cs/blog/<slug>/
src/content/blog/
  learn-or-die.mdx        # EN post
  cs/
    learn-or-die.mdx      # CS post (same slug, different lang)
```

**Content collection schema — add lang field:**
```typescript
schema: z.object({
  title: z.string(),
  description: z.string().min(50).max(160),
  pubDate: z.date(),
  updatedDate: z.date().optional(),
  tags: z.array(z.string()).default([]),
  draft: z.boolean().default(false),
  lang: z.enum(['en', 'cs']).default('en'),  // <-- add this
}),
```

**Blog routing that filters by lang:**
```typescript
// src/pages/blog/[...slug].astro (EN)
export async function getStaticPaths() {
  const posts = await getCollection('blog', ({ data, id }) =>
    !data.draft && !id.startsWith('cs/')
  );
  return posts.map(post => ({ params: { slug: post.id }, props: { post } }));
}

// src/pages/cs/blog/[...slug].astro (CS)
export async function getStaticPaths() {
  const posts = await getCollection('blog', ({ data, id }) =>
    !data.draft && id.startsWith('cs/')
  );
  return posts.map(post => ({
    params: { slug: post.id.replace(/^cs\//, '') },  // strip cs/ prefix
    props: { post },
  }));
}
```

**Layout must emit lang attr + hreflang alternates:**
```astro
---
const pathname = Astro.url.pathname;
const isCs = pathname.startsWith('/cs/') || pathname === '/cs';
const htmlLang = isCs ? 'cs' : 'en';
const enPath = isCs ? (pathname.replace(/^\/cs\/?/, '/') || '/') : pathname;
const csPath = isCs ? pathname : (pathname === '/' ? '/cs/' : `/cs${pathname}`);
---
<html lang={htmlLang}>
  <head>
    <link rel="alternate" hreflang="en" href={new URL(enPath, Astro.site)} />
    <link rel="alternate" hreflang="cs" href={new URL(csPath, Astro.site)} />
    <link rel="alternate" hreflang="x-default" href={new URL(enPath, Astro.site)} />
  </head>
</html>
```

**Language switcher component:** small nav-embedded EN · CS toggle. Anchor tags with `lang="en"` / `hreflang="en"` for accessibility.

**Translating pages to a native secondary locale.** No translation skill ships with this plugin, so run the recipe inline (if you have a dedicated page-translation skill installed, use it — it's an optional extra). Don't hand-roll a fresh prompt per page; hold the whole recipe in one place and reuse it: semantic rewrite (not word-by-word), **formal web register** — every language has one, and it is usually not the register a casual-translation prompt produces — locale-correct typography, source-language technical terms deliberately kept untranslated where practitioners use them, locale link rewriting, meta + JSON-LD translation, and a fresh-context "native editor" pass that reads ONLY the target language.

*Worked example — Czech.* Web register means vykání and full diacritics. Typography means thin-space thousands separators, decimal commas and low-high „quotes" (`2 166 EUR` · `9,17/10` · `16 %`). Terms practitioners say in English stay in English (session, roadmap, sparring, hire). This is the level of specificity your own locale needs, written down once.

Three assets that make it scale past ~5 pages:
1. **`TRANSLATION-GLOSSARY.md` at repo root** — canonical target-language renderings of CTAs, nav labels, taglines, tier names. Read it first and treat entries as law. Prevents the same button being translated three ways.
2. **Corrections log inside the glossary** — every human correction recorded as `source | rejected | approved`; future runs never repeat a fixed mistake.
3. **A deterministic spellcheck/diacritics layer** for the target language, run after the semantic pass. Check what actually supports your locale before committing: the obvious mainstream grammar checkers have real coverage gaps (LanguageTool, for instance, does not support Czech at all — it was dropped from both the distribution and the cloud API). For Czech specifically, the UFAL Korektor public REST API (`lindat.mff.cuni.cz/services/korektor/api/correct`, model `czech-spellchecker`) fills the gap.

**Batch-translating 20+ pages:** seed the glossary from already-approved pages FIRST, then one subagent per batch of 5-6 pages each following the same recipe, then an independent fresh-context reviewer per page reading only the target language. Present in batches of ~5 with `draft: true` on blog posts; first-batch corrections go into the glossary before the remaining batches run.

### 15.6 Blog image migration (archive domain → local)

WP posts embed images from `wp-content/uploads/YYYY/MM/*`. After migration, these still point at the archive domain — brittle if archive ever goes down.

**Batch-download + path-rewrite pattern:**
```python
# Enumerate all image URLs across MDX files
import re
IMG_PATTERN = re.compile(r'https?://(?:www\.)?archive-domain\.com/wp-content/uploads/[^)"\'\s\]]+')
urls = set()
for path in Path("src/content/blog").rglob("*.mdx"):
    urls.update(IMG_PATTERN.findall(path.read_text()))

# Parallel download preserving year/month structure
# Then rewrite <domain>/wp-content/uploads/<path> → /images/blog-archive/<path>
```

Preserve the `YYYY/MM/` structure to avoid filename collisions (WP recycles filenames).

### 15.7 Article meta + JSON-LD for migrated blog posts

Existing blog schema often defaults to `og:type=website` — wrong for blog posts. Add per-post article meta:

```typescript
// pass to Layout as article prop
article={{
  publishedTime: post.data.pubDate.toISOString(),
  modifiedTime: post.data.updatedDate?.toISOString(),
  section: post.data.tags?.[0] ?? 'Your Default Category',
  tags: post.data.tags,
  authorName: 'Author Name',
  authorUrl: 'https://your-product.com/',
  locale: 'en_GB',  // or 'cs_CZ' for CS posts
}}
```

Layout renders:
```html
<meta property="og:type" content="article" />
<meta property="og:locale" content="en_GB" />
<meta property="article:published_time" content="..." />
<meta property="article:modified_time" content="..." />
<meta property="article:section" content="..." />
<meta property="article:author" content="https://your-product.com/" />
<meta property="article:tag" content="tag-1" />
<meta property="article:tag" content="tag-2" />
```

**BlogPosting JSON-LD** on every post with `inLanguage`, `articleSection`, `datePublished`, `dateModified`, `author` (Person + sameAs), `publisher`, `image`, `mainEntityOfPage`, `keywords`.

**BreadcrumbList JSON-LD** on every deep page (blog posts, service pages nested one below root).

---

