# Web Creator Reference — Gates (performance + a11y publish-blockers, design review, publish gate)

Part of the `/founder-pipeline:web-site-creator` reference set. Headings keep their original § numbers.

## 9. Performance + accessibility gates (publish-blockers)

**Why 95+ mobile is a hard gate, precisely stated:** the *ranking* evidence for Core Web Vitals is weak — Mueller: "not giant factors in ranking, and I doubt you'd see a big drop just because of that." The *conversion* evidence is strong and causal — true server-side A/B tests (not correlational) found 31% better LCP → +8% sales [Vodafone Italy], and passing all three CWV → +33% conversion, +53% revenue/visitor [Rakuten 24]. Chase this number for revenue, not rank. One practical note: INP is nearly free on a static Astro build (most sites already pass it) — LCP is the metric that actually differentiates, so that's where remediation effort (§9.1) belongs.

Don't deploy if any of these fail:

- All Lighthouse and field targets in 8.10 met
- `axe-core` clean on every page
- Every interactive element reachable by keyboard, focus rings visible
- Color contrast WCAG AA minimum
- All images served via Cloudflare Images with srcset, `width` + `height` set
- Total CLS under 0.05 on hero + above-the-fold
- Voice final pass: `/founder-pipeline:brand-voice` re-run on every public string

Add CI checks for Lighthouse + axe on every PR.

### 9.0 Cache-Control headers (`_headers`) — get these right on day one

Two rules that cost one production site real performance for months. Both are silent: nothing errors, the site just caches badly.

**Rule 1 — never put `Cache-Control` on `/*`.**
Cloudflare `_headers` **combines** matching rules, it does not override them. Two rules that both match a URL and both set `Cache-Control` emit a single joined header, and the browser honours the **first** directive it sees:

```
/*
  Cache-Control: no-store          ← don't
/_astro/*
  Cache-Control: public, max-age=31536000, immutable
```
```
GET /_astro/app.abc123.js
cache-control: no-store, public, max-age=31536000, immutable   ← no-store wins; nothing is cached
```

Leave `/*` for security headers only (HSTS, `X-Content-Type-Options`, `Referrer-Policy`) and declare `Cache-Control` per path.

**Rule 2 — never use `no-store` on HTML.** It's the intuitive way to stop the edge serving stale HTML after a deploy, and it is the one value that disables the **back/forward cache**: Chrome and Safari refuse to bfcache any document served `no-store`, so every Back click becomes a full reload. Lighthouse reports it under `bf-cache` as "Not actionable", which is misleading — it's your header.

Use `public, max-age=0, must-revalidate` instead. Same freshness guarantee (the browser and edge must revalidate before reuse, so a deploy is live immediately), but the document is *storable*, so bfcache works. Revalidation is answered with a 304 off the ETag — a header round trip, not a re-download. This is also the Workers Assets default, so on Cloudflare the correct move is simply to **write no HTML rule at all**.

Working baseline:

```
/*
  Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin

# HTML: no rule — inherits the Workers Assets default,
# `public, max-age=0, must-revalidate` (revalidated, storable, bfcache-safe).

/_astro/*
  Cache-Control: public, max-age=31536000, immutable   # content-hashed

/images/*
  Cache-Control: public, max-age=604800                # not hashed — a week, then revalidate
```

**Verify after every deploy** (edge caching means the first read can be stale — send `Cache-Control: no-cache` to bypass):

```bash
for u in / /_astro/<hashed-file>.js /images/<file>.jpg; do
  echo -n "$u → "
  curl -s -D- -o /dev/null -H "Cache-Control: no-cache" "https://<domain>$u" \
    | grep -i '^cache-control'
done
```
A comma-joined `Cache-Control` in that output means two rules overlapped — go back to Rule 1.

**Related gotcha — GET requests to API routes 404.** On Workers Assets the static-asset layer is matched *before* the Worker runs, so a `GET /api/whatever` with no matching file returns the assets 404 and your endpoint never executes. POST routes are unaffected, which makes this look like a routing bug in only half your API. Fix in `wrangler.jsonc`:

```jsonc
"assets": {
  "directory": "./dist/client",
  "run_worker_first": ["/api/*"]
}
```

### 9.1 Mobile PageSpeed remediation loop (68 → 99 in one session)

The recipe that moved a real Astro + Cloudflare Worker site from mobile Performance **68 → 99** in two deploy cycles. Every item is a fix that actually shipped, not theory. Do them in this order — the biggest wins are at the top.

**Measurement — iterate on LOCAL Lighthouse, confirm once with PSI.**

Do not run the remediation loop against PSI. Its quota will strand you mid-loop, and it gives you a score without the raw trace you need to find the cause. Iterate locally, then spend one PSI run to confirm.

```bash
npx -y lighthouse@12 "<url>" \
  --only-categories=performance --form-factor=mobile --screenEmulation.mobile \
  --throttling-method=simulate --output=json --output-path=./lh.json \
  --chrome-flags="--headless=new --no-sandbox" --quiet
```

Same engine, same audits, same Lantern simulation as PSI, no quota, and you keep the full JSON. Needs only Node + Chrome.

- **Local numbers are for RELATIVE comparison, never for quoting.** Local TTFB includes your real latency to the edge (measured 663 ms from Prague where PSI reported 10 ms), and a 4×-throttled M-series Mac still outruns PSI's reference box. So local scores read high. Trust the *deltas* and the *shape* (which phase owns the time, which audits fire); quote only PSI.
- **Neither is "true" performance.** Both are lab. The real number is CrUX field data from actual visitors — Cloudflare Web Analytics (§14.5.3) reports it.
- **Use a PageSpeed Insights API key**, held in your secrets store. Anonymous callers share a ~25/day pool that strangers exhaust — that cost a full day of blocked measurement once. A key gives 25,000/day.
  ```bash
  curl -s "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=$(python3 -c 'import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1],safe=""))' "$URL")&strategy=mobile&category=performance&key=$PSI_API_KEY"
  ```
  If the key is ever missing, recreate it: Google Cloud → enable PageSpeed Insights API → Credentials → API key (~2 min). Note PSI appears to serve a cached result for repeat calls on the same URL within a short window — three back-to-back runs returned byte-identical metrics, so don't mistake that for stability. Vary the URL (`?x=1`) or wait if you need genuinely independent samples.
- Expect ±5–8 points of run-to-run variance. Sample 3 runs and take the median before declaring a win. One run proves nothing.

**Diagnosis — read the trace, don't guess at the audit list.**

Lighthouse's "Opportunities" list is often silent about the actual bottleneck. Two techniques that find it in minutes:

- **Filmstrip byte-size = blank-screen detector.** Decode `audits["screenshot-thumbnails"].details.items[]` and print each frame's byte length. Identical tiny sizes (~1 KB) mean a literally blank white screen. A real case: frames at 641/1282/1922/2563 ms were all exactly 1,182 bytes — the page painted *nothing* for 2.9 s while every byte had arrived by 536 ms. That instantly reframes the problem from "slow network" to "paint is being withheld."
- **`--blocked-url-patterns` = A/B culprit isolation.** Re-run with a suspect origin blocked and diff the score. This turns "third-party JS is probably hurting" into a number you can act on: blocking one analytics origin moved a real site 78 → 92 and simulated FCP 3,082 → 1,606 ms. Blocking something and getting a *worse* score also rules it out (blocking a hero video dropped the score to 84, because LCP then waited on a failed resource).
- **Read the LCP phase table** (`largest-contentful-paint-element`): TTFB / Load Delay / Load Time / Render Delay. Huge Render Delay with tiny TTFB and Load Time means nothing is slow to *fetch* — something is slow to *paint*. Caveat: for a `<video>` LCP element Lighthouse often fails to attribute the poster resource and dumps everything into Render Delay, so cross-check against the filmstrip.
- **Compare `observed*` vs simulated metrics** in `audits.metrics.details.items[0]`. `observedLoad` / `observedDomContentLoaded` vs `observedFirstContentfulPaint` is the tell for the trap below.

**Fix 1 — Lazy-load third-party embeds. (Biggest single lever.)**
Any embed that pulls a third-party JS bundle at page load (calendar widgets, chat widgets, `<object>` embeds, YouTube iframes without `loading="lazy"`) will torch your TBT. On one real build, a calendar-widget `<object>` embed was eating **~1,000 ms of TBT and ~3.9 s of JS execution**.

Pattern — placeholder + IntersectionObserver swap:
```html
<div data-embed="https://third-party.example.com/embed/xyz" style="height:700px;">
  <a href="https://third-party.example.com/direct" target="_blank" class="cta-button">
    Loading… tap to open in a new tab →
  </a>
</div>
<script is:inline>
  (function () {
    const el = document.querySelector('[data-embed]');
    if (!el || !('IntersectionObserver' in window)) return;
    const io = new IntersectionObserver((entries) => {
      entries.forEach(e => {
        if (e.isIntersecting && !el.dataset.loaded) {
          el.dataset.loaded = '1';
          el.innerHTML = '';
          const iframe = document.createElement('iframe');
          iframe.src = el.dataset.embed;
          iframe.loading = 'lazy';
          iframe.style.cssText = 'border:0;width:100%;height:700px;';
          el.appendChild(iframe);
          io.disconnect();
        }
      });
    }, { rootMargin: '400px 0px' });
    io.observe(el);
  })();
</script>
```
The `rootMargin: '400px 0px'` means the embed starts loading before it enters the viewport, so scrolling users don't see the placeholder. The `<a>` fallback keeps users with JS disabled or slow networks bookable.

**Fix 2 — Non-blocking Google Fonts.**
`<link rel="stylesheet" href="fonts.googleapis.com/...">` is render-blocking (~400–500 ms of critical-path time on mobile). Swap to async preload:
```html
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link
  rel="preload"
  as="style"
  href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap"
  onload="this.onload=null;this.rel='stylesheet'"
/>
<noscript>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" />
</noscript>
```
The `preload` starts the fetch immediately without blocking render; the `onload` swap upgrades it to a stylesheet the moment CSS arrives. `<noscript>` fallback covers no-JS clients. Do this in every layout that references Google Fonts.

**Fix 3 — `build.inlineStylesheets: 'always'` in Astro.**
Astro's default (`'auto'`) emits component-scoped CSS as separate hashed files (e.g. `/_astro/Footer.abc123.css`). Each of those becomes a render-blocking request. On one real build a single `Footer.*.css` chunk was **8 KB and 209 ms on the LCP critical path** — for a small footer. Kill the whole class of problem:
```js
// astro.config.mjs
export default defineConfig({
  site: 'https://www.example.com',
  build: {
    inlineStylesheets: 'always',  // <-- inlines every CSS chunk into <head>
  },
  // ...
});
```
Tradeoff: HTML pages get slightly larger. For a site under ~20 pages, this is a pure win — no extra network round-trips, no cache-miss on first paint. Watch total HTML size only if you're rendering huge component trees.

**Fix 4 — Every `<img>` gets explicit `width` and `height`.**
Not just for CLS — Lighthouse actively docks you for images without dimensions even when CLS is fine. This includes:
- Client logo walls (a 36-logo wall on a real build — every one needed dimensions)
- Nav / footer logos (external SVGs count)
- FromTheBlog card covers
- Testimonial photos
- Any raw `<img>` you didn't pass through Astro's `<Image>` component

The Astro `<Image>` component handles this for you. Raw `<img>` tags do not.

**Fix 5 — Source images must not be larger than their displayed size.**
Lighthouse flags any image where source > display as "Improve image delivery." A 400×400 file rendered at 200×200 wastes ~75% of the bytes. Batch resize:
```bash
# WebP files (macOS `sips` can't resize webp — use ImageMagick)
magick "photo.webp" -resize 200x200 "photo.webp"

# Bulk client-logo resize (max width 200px for a max-h-12 = 48px display)
cd public/images/clients
for f in *.png *.webp; do
  [ -f "$f" ] || continue
  w=$(magick identify -format "%w" "$f" 2>/dev/null)
  if [ -n "$w" ] && [ "$w" -gt 200 ]; then
    magick "$f" -resize 200x "$f"
  fi
done
```
Rule of thumb: source ≤ **2×** display size (retina headroom). Anything more is waste.

**Fix 6 — Remove `will-change` from elements that aren't animating.**
`will-change: opacity, transform` on `[data-reveal] > *` (or any pre-visible element) creates a composite layer *before* animation starts. Mobile GPUs pay for those layers in memory, and Lighthouse counts them against you. Only apply `will-change` inside the animation itself, or drop it entirely — Astro's fade-up reveal works fine without it because the browser promotes the element to a layer automatically once the `transform` animation is in flight.

**Fix 7 — Analytics SDKs: `load` is NOT deferred. Use `requestIdleCallback` + lazy session recording.**

Wrapping an analytics snippet in `window.addEventListener('load', …)` reads like deferral and is the pattern every vendor ships. It is not enough. On a well-optimised page `load` fires *early* — measured at 539 ms on a real build — while first paint did not happen until 2,851 ms. So the SDK downloaded and executed squarely inside the paint window. Blocking that one origin was worth **14 Lighthouse points**.

Check for it: if `observedLoad` is much smaller than `observedFirstContentfulPaint`, everything you hung off `load` is on the paint path.

```js
window.addEventListener('load', () => {
  var idle = window.requestIdleCallback || function (fn) { return setTimeout(fn, 1); };
  idle(function () { initAnalytics(); }, { timeout: 2000 });
});
```

Then kill session recording at init and start it in a *second*, separate idle callback — the recorder bundle (rrweb ~57 KiB) is typically the heaviest single asset on the page and nothing needs it in the first seconds:

```js
posthog.init(TOKEN, { /* … */ disable_session_recording: true });
// separate callback, so a busy main thread delays the recorder, not $pageview
idle2(function () { posthog.startSessionRecording(); }, { timeout: 5000 });
```

`$pageview` still fires at init, so short visits are still counted — you only lose the replay of a sub-3s bounce. Real result, **confirmed on PSI: 78 → 96 mobile** (FCP 1.5 s, LCP 2.4 s, TBT 20 ms, CLS 0). Local Lighthouse had put it at a 94 median across a 90/94/98 spread — so local was directionally right and slightly *pessimistic* here, but the 8-point spread is exactly why the median rule above exists. Never quote a single local run.

**Traps that look like fixes but aren't:**
- `content-visibility: auto` on below-fold sections — sounds like a free win, but if `contain-intrinsic-size` is wrong you get CLS regressions on scroll. Only apply when you can precisely measure the section's rendered height.
- Assuming a CSS `filter` / `mix-blend-mode` is your LCP problem because a *previous* PSI run blamed render delay. Verify the rule actually applies at the tested viewport first — Lightning CSS minifies `min-width: 768px` to `width>=768px`, so a naive grep for the media query in the built output finds nothing and you "confirm" a bug that isn't there.
- Deferring analytics to `load` (see Fix 7). Looks deferred, measures as blocking.
- Client-side JS to defer *your own* CSS — this is what `inlineStylesheets: 'always'` already solves, without the JS cost.
- Preconnecting to more than 4 origins — each `<link rel="preconnect">` warms a TCP+TLS handshake; overuse burns mobile radio budget with nothing to show for it.
- Removing entire sections to "save weight" — Lighthouse scores what's above the fold most heavily. Below-fold content rarely costs perf points if the images are lazy-loaded.

**Verification loop — 3-run stability check.**
Sample 3 consecutive *local* Lighthouse runs and take the median, then spend one PSI run to confirm the real number. If any run falls below your target, one of these is usually the culprit:
1. An image without `width`/`height` (variance in reflow timing)
2. A third-party embed that occasionally hits its slow path (calendar widget cold cache)
3. Font loading racing render (double-check the `preload` swap ships correctly)

Targets: **95+ mobile Performance**, all Core Web Vitals green (FCP/LCP < 1.2s, TBT = 0, CLS < 0.05).

### 9.2 Mobile responsiveness fix loop (layout, ordering, overlaps)

PageSpeed passing (9.1) says the page *loads* fast on mobile. It doesn't say the *layout* is any good. This is the parallel loop that fixes: photo grids appearing before the H1, empty design placeholders that look broken, excessive padding that pushes content below the fold, orphaned grid items, horizontal overflow, illegible text.

**Measurement — the real thing, not DevTools emulation.**
- Drive the actual mobile viewport in Claude-in-Chrome (or on a real device). DevTools mobile emulation misses touch targets, scroll behavior, and iOS-specific bugs.
- Test at **two widths**: 390px (iPhone 14 baseline) and 320px (iPhone SE / narrow Android — the floor).
- **Chrome on macOS won't resize a window below ~606px wide**, so a true phone viewport is unreachable by resizing. Workaround (field-proven in production): load the page into a same-origin `<iframe width="390">` — vw units resolve against the iframe, and `contentDocument` stays scriptable for measuring rects. Reverse trick for checking desktop from a small window: a 1440px iframe with `transform: scale(0.41)`.
- Scroll top → bottom on every page. Screenshot every ~600px. Photos-of-photos catches what "does it look OK?" misses.
- Assert no horizontal scroll: `document.documentElement.scrollWidth <= window.innerWidth`. Any diff means something is spilling.

**Fix 1 — Reverse hero grid order so the H1 is above the fold on mobile. (Biggest single lever.)**
Desktop hero often uses `md:grid-cols-[1fr_460px]` with a hero image / photo collage as the second column. Sensible on desktop. On mobile the grid collapses to one column, and if the image div has `order-first md:order-last`, the visitor sees a decorative photo grid *before* they see who you are and what you do — H1 pushed hundreds of pixels below the fold. Bounce rate looks like the copy failed. The copy never got a chance.

```diff
- <div class="order-first md:order-last">   <!-- photo grid -->
+ <div class="md:order-last">               <!-- photo grid: DOM order on mobile, right column on desktop -->
```
Rule: **on mobile, the H1 must be in the first 100vh of scroll, period.** Everything decorative goes below.

**Fix 2 — Hide desktop-only decorative placeholders on mobile.**
Design compositions that use empty circles / negative-space blocks (`aspect-square rounded-full bg-neutral-300`) as balance elements on a 3-column desktop grid look like broken images on mobile. The visitor doesn't know the gray disc is intentional — they think it failed to load.

```diff
- <div class="aspect-square rounded-full bg-neutral-300"></div>
+ <div class="hidden md:block aspect-square rounded-full bg-neutral-300"></div>
```

**Fix 3 — Rebalance the mobile grid after hiding items.**
Hiding decorative items breaks the grid's row math. Hiding 2 of 9 items in a 3-col grid leaves 7 → `3+3+1` with an orphan on the last row. Fix by hiding one more (usually another decorative image) to land on **6 items = 2 clean rows of 3**, or switch the mobile column count so the remainder divides evenly.

Concrete: a 9-item collage of `[photo, quote, circle, quote, photo, photo, circle, photo, quote]` becomes `[photo, quote, quote, photo, photo, quote]` on mobile (hide both circles + one photo), giving a clean `photos + quotes` proof grid at 3×2.

**Fix 4 — Cut oversized mobile section padding.**
`py-24 md:py-32` = 96px top *and* bottom on mobile. Combined across 8 sections that's ~1,500px of pure dead space on the scroll length, most of it above the first visible content in each section. Mobile users pay for scroll time in attention. Halve the mobile padding:

```diff
- <div class="mx-auto w-full max-w-6xl px-6 py-24 md:py-32">
+ <div class="mx-auto w-full max-w-6xl px-6 py-12 md:py-24">
```

Also grep for **duplicated Tailwind classes** — real bugs that hide in long class strings:
```bash
# Duplicated responsive prefix — the later one wins silently
grep -nE '(py-[0-9]+ md:py-[0-9]+ md:py-[0-9]+)|(px-[0-9]+ md:px-[0-9]+ md:px-[0-9]+)' src/**/*.astro
```
Real example: `py-24 md:py-32 md:py-24` — the trailing `md:py-24` overrode the `md:py-32`, so the value the designer thought they set was never actually applied.

**Fix 5 — Nav header: verify the brand block fits at 320px.**
Logo + wordmark + tagline + hamburger has to fit in ~320px of usable width (`px-6` eats 48px). Two common failures:
- Tagline is too long (a 50+-character positioning sentence) → wraps under the logo or clips.
- `whitespace-nowrap` on the brand block forces horizontal overflow.

Rules: keep the mobile tagline ≤ 30 characters, or `hidden sm:block` it entirely. Never `whitespace-nowrap` on the brand text — let it wrap.

**Fix 5b — Never hide nav links on mobile without a menu behind them.**
`display:none` on the link list below a breakpoint is only half a pattern — the other half is the hamburger (a no-JS `<details>` disclosure is enough — keep a reference `Nav.astro` in your own component library). One audit found the nav below 680px reduced to brand + one CTA button, leaving three primary sections unreachable from the header on every phone. If a link matters enough for desktop nav, mobile visitors get a way to reach it too.

**Fix 6 — Reveal animations must handle "user lands mid-page."**
Anchor links, browser restore-scroll, and hash navigation all drop the user past the top. If you have an `IntersectionObserver` reveal (`[data-reveal-children]` starts at `opacity: 0`), sections above the current scroll position never intersect — the visitor sees blank white space where content should be.

Two-line fix in the IO callback: on page load, force-reveal anything already past the fold before wiring the observer.
```js
const io = new IntersectionObserver(/* ... */);
els.forEach((el) => {
  // If already in or above the viewport at load, reveal immediately.
  if (el.getBoundingClientRect().top < window.innerHeight) {
    el.classList.add('is-visible');
  } else {
    io.observe(el);
  }
});
```

**Fix 7 — Scroll-snap rails: snap area ignores container padding.**
Card stacks converted to horizontal snap rails (`-mx-6 px-6 overflow-x-auto snap-x snap-mandatory`) immediately snap to `scrollLeft: 24` and swallow the left gutter — `snap-start` aligns to the container's snap area, which does NOT include padding, so the first card sits flush against the screen edge while every other card keeps its inset. Fix: `scroll-px-6` (scroll-padding) on the container. Catch it by measuring `scrollLeft` at rest (must be 0), not by eye.

**Fix 8 — `backdrop-filter` on an ancestor clips `position: fixed` children.**
A `backdrop-blur` on `<header>` makes the header the CSS containing block for its own fixed-position mobile-menu panel (spec behavior for `backdrop-filter`, same as `transform`) — the open menu clips to the header's height instead of spanning the viewport. Fix: move the blur to a `::before` pseudo-element (a sibling layer, not an ancestor of the panel); visual effect identical.

**Traps that look like fixes but aren't:**
- Adding `overflow-x: hidden` on `<body>` to "kill" horizontal scroll — hides the symptom, not the cause. Find the element that's overflowing (`document.querySelectorAll('*')` + `getBoundingClientRect().right > window.innerWidth`) and fix its width.
- Wrapping every section in `overflow-hidden` — kills sticky headers and any intentional overflow (tooltips, dropdowns).
- Using `min-w-0` / `flex-shrink` as a blanket fix — sometimes needed, but if the fix is "make text smaller until it fits" the real answer is usually "let it wrap."
- Testing only in Chrome DevTools mobile emulation — miss Safari-specific bugs (100vh, safe-area, `-webkit-` prefixes on gradients).

**Verification loop — 3-viewport pass before deploy.**
1. **320px** — nothing overflows, no horizontal scroll, all tap targets ≥ 44px.
2. **390px** — the H1 is fully visible above the fold; the first CTA is above the fold or one thumb-scroll away.
3. **768px** — the desktop-preview breakpoint kicks in cleanly, no layout jump between `md:` states.

Then screenshot top-to-bottom at 390px and read every screen the way a visitor would. If any screen shows a blank block, an unlabeled gray shape, or a text/photo overlap — that's a fix, not a feature.

---

## 17. Design review loop

Run a **structured design review three times** during the build. Not once at the end. Iterate on the findings each time.

This plugin ships no design-review skill. If you have one, or if you install the optional
`frontend-design` plugin separately, route these rounds to it. Otherwise run each round yourself
against the prompt given for it below — the prompts are the substance, and the review works read
from a checklist. Ask for findings as **P0 / P1 / P2 with concrete class-level changes** either way.

**Round 1 — at GATE 1 (pages scaffolded with real content), before any polish.**
- Point it at the dev server (`http://localhost:4321/`). Ask: *"Structural review. Density, hierarchy, section pacing, first impression. Ignore copy — voice-review comes later."*
- What you're catching: sections that don't earn their space, cards without air, monotone typographic hierarchy, dark/light bands that flatten rather than pace.
- Output format to ask for: **P0 / P1 / P2 with Tailwind class changes**.

**Round 2 — at GATE 2 (voice pass + logo/gallery/testimonials in).**
- Ask for a "compression check": am I trying to fit too much? Which sections could be dropped or merged? What would a Linear/Cal.com/Framer marketer cut?
- Then a re-run of density + hierarchy on the sections that changed.

**Round 3 — at GATE 3, pre-publish, alongside `/founder-pipeline:seo-audit`.**
- Full P0/P1/P2 sweep including the mobile viewport.
- Any P0 finding blocks publish. P1 backlog for post-launch. P2 optional.

### Anti-patterns the design review catches (from real builds)

- **Padding didn't scale with the type.** You bumped H2 to `text-6xl` but left `py-16` on sections → cramped. Rule: whenever type size goes up, vertical section padding must too. Match `py-24 md:py-32` to a `text-5xl+` H2.
- **Dark-band clustering.** Alternating dark/light is a rhythm. 4-5 dark sections in a row is a wall. Reserve dark for revenue-critical acts (hero, pricing, CTA). No more than 2 dark sections adjacent.
- **Card padding stuck at p-6 while cards got taller.** Linear/Cal.com run `p-10 md:p-12` on marketing cards. `p-6` is dashboard-density.
- **No eyebrow labels.** A small uppercase tag above each H2 (`text-xs uppercase tracking-[0.2em] text-neutral-500 mb-4`) creates a landing pad for the reader's eye. It's the single most-copied Linear pattern.
- **Long line lengths on paragraph blocks.** `max-w-6xl` on a container is fine; paragraphs inside must be capped at `max-w-3xl` (68ch equivalent) or reading falls apart on wide monitors.
- **Same 1rem for hero body + section body + card body.** Rescale: hero copy `text-lg md:text-xl`, section body `text-lg`, card body default. Three distinct sizes create hierarchy without shouting.
- **H2 leading not set on giant type.** At `text-5xl+` the browser default leading is loose; set `leading-[1.05]` or `leading-tight` explicitly.

### How to phrase the prompt

The `/design` skill responds best to:
1. **Live URL** (dev server), not screenshots — it can access `browser` tools and see the real state.
2. **Explicit scope**: "Focus on density and section pacing, skip a11y and copy" beats "review my landing page".
3. **Output format request**: "P0/P1/P2 with Tailwind class changes" turns the review into a diff you can apply.

### Do NOT use the design review for

- Generating new components — that is the optional, separately-installed `frontend-design` plugin's territory.
- Copy review — that is `/founder-pipeline:brand-voice`, plus a plain read-through against your own copy standards.
- SEO/perf issues — that is `/founder-pipeline:seo-audit`, and the optional, separately-installed `cloudflare` plugin's `web-perf` skill for performance profiling.

---

## Appendix F. The publish gate

Before flipping DNS or hitting "publish", every item below is green:

- [ ] `/founder-pipeline:founder` Stages 00-12 complete for this stream (founder streams only)
- [ ] `/founder-pipeline:pricing` scorecard ≥ 95/100
- [ ] `/founder-pipeline:brand-voice` final pass on every public string
- [ ] Every button has hover + active + focus-visible + disabled states, defined once on the canonical class (see interactivity.md "Button interaction baseline"). Tab to one and confirm the focus ring is visible.
- [ ] All meta from 8.2 present on every page
- [ ] Favicon set + `site.webmanifest` shipped (8.3)
- [ ] JSON-LD validated per page type (8.4)
- [ ] `robots.txt` matches your single canonical template (four-tier spec in `phases/5-seo.md` §Z1); `llms.txt`, `llms-full.txt`, sitemap.xml all reachable (`llms.txt` is a build-health check, not a citation claim — §8.6)
- [ ] **Crawler-delivery matrix** returns 200 for every key URL × AI/search UA, run once on staging and again on production (5-seo.md §5.3, 6-launch.md §6.3) — a robots.txt read alone does not catch edge-level blocks
- [ ] **Bing Webmaster Tools verified + sitemap submitted + AI Performance report checked** (6-launch.md §6.4) — the large majority of ChatGPT/Copilot citations match Bing's top organic results [operating assumption], and this is the only first-party AI-citation data available in this stack
- [ ] NLWeb endpoint live and discoverable
- [ ] `/founder-pipeline:seo-audit` ran, all issues resolved
- [ ] **Section 8.11 real-world audit checklist run — every item green**
- [ ] `site` in `astro.config.mjs` = canonical production domain (not `*.workers.dev`)
- [ ] **One canonical host. Every other host 301s to it** (apex↔`www`), path and query preserved, via a zone **Redirect Rule** — not `_redirects`, not app code (6-launch.md §6.3a, `references/launch.md` §14.5.9). Verify with `curl -sI` on BOTH hosts: a 200 from each is the bug. Read the direction off `<link rel="canonical">`, never assume `www`. Carve out `/mcp*`, `/api/`, `*.txt` verification files. One sweep found this live on three separate zones, all launched months apart
- [ ] Every layout has OG + Twitter + JSON-LD parity (not just the landing layout)
- [ ] No `[Placeholder]` / `TODO` / `Lorem` text in any public HTML
- [ ] No cannibalising duplicate pages (`/` vs `/new` etc.)
- [ ] Schema is the eight-type set (`references/metadata.md` §8.4) — `Organization`, `BreadcrumbList`, `Article`/`BlogPosting`+author, `ProfilePage`+`Person`, in-person `Event`, `FAQPage` wherever a **visible** FAQ accordion exists, `HowTo` wherever **visible** numbered steps exist, and `Speakable` on a clean spoken-answer section. `Service`/`OfferCatalog` remain out (no live rich result). **`HowTo` is no longer removed on sight** — the REMOVE-IF-PRESENT rule this line used to carry was retired when the standing decision was extended to cover it and `Speakable`; a gate that strips what the owner sanctioned is worse than no gate. What IS still a blocker: any of the three carrying content the reader cannot see (detection script in `references/seo.md` §8.11)
- [ ] **Zero `FAQPage` nodes whose answers appear nowhere in the visible DOM** — schema-only Q&A is a bug in both directions: unreadable to every engine tested [searchVIU, 5 engines, 0 of 5], and the way content silently disappears. Detector in `references/seo.md` §8.11
- [ ] On a multi-locale site: one flag governs `hreflang`, the language switcher AND the sitemap entry, and every shared nav/footer/CTA href derives from the current locale (`references/core.md` § "Secondary-locale localisation"). An ungated switcher puts a 404 in the header of every unmirrored page
- [ ] `Person` schema + `sameAs` (LinkedIn, YouTube, GitHub, community) on personal-brand sites, wrapped in `ProfilePage`
- [ ] Hero images in `src/assets/` (not `public/`), served via `<Image>` with `fetchpriority="high"`
- [ ] No image over 500 KB committed to `public/` or `src/assets/`
- [ ] **Imagery floor (§1.9):** no all-text public page (≥2 real images each); money-page hero shows a photo or real artifact; zero monogram/`?` placeholder avatars; no hotlinked cross-deployment images
- [ ] **Attributed social proof** (face, logo, or named outcome quote) on every money page before the first CTA repeat (§1.9)
- [ ] Every clickable card / tier / person row has a hover state (§1.5 #10, §1.8)
- [ ] On-page lead capture exists beyond the calendar link; no "coming soon" lead-magnet stubs (§6)
- [ ] Sub-brand layouts: `ogImage` default is THIS product's card, not inherited from another product (§8.11)
- [ ] **Every indexable page has its own OG image, not the layout fallback** — OG image coverage script reports zero hits (§8.11 / `references/core.md` § OG images)
- [ ] Shared JSON-LD components have no hardcoded fallback prices/dates — `Offer` omitted when pricing is private (§8.11)
- [ ] Date shown visibly on-page; `dateModified` emitted only on genuine content change, never automated (§8.11) — not the AI-citation lever it was once framed as
- [ ] Mobile nav keeps a menu at 320px — no link-hiding without a hamburger/`<details>` fallback (§9.2 Fix 5b)
- [ ] Lighthouse CI passes (95/100/100/100)
- [ ] axe-core: 0 violations
- [ ] securityheaders.com A+, ssllabs.com A+, Mozilla Observatory A+
- [ ] PostHog events firing in staging
- [ ] **Consent bar (§14.5.8):** shipped, reject-only model; Reject deletes `ph_*`/`_ga*` on host AND `.host` AND `.registrable-domain`; pageviews still fire after Reject (`gcs=G100`); no `recorder.js` request after Reject; CLS identical with and without the bar; privacy page has a cookie table, `#cookie-settings`, every processor named, and a bumped date
- [ ] **Analytics stack (§14.5):** GTM/GA4 wired with Consent Mode v2 granted-by-default (`region` + `wait_for_update` deleted, `security_storage` granted in both payloads); GA4 key events marked; product analytics with 4 dashboards + north-star pinned + drop alert; edge web analytics on; your CRM's upsert tested (submit → record with UTMs + replay URL); `gclid`/`li_fat_id` captured + persisted at submit
- [ ] MCP server deployed and `/.well-known/mcp.json` resolves
- [ ] OG cards tested in opengraph.xyz
- [ ] Contact + newsletter forms tested end to end
- [ ] **Internal linking density** (Section 8.11): every service page ≥3 outgoing internal links, every service page ≥5 incoming internal links, every blog post ≥2 links back to relevant service pages, every page that matters has ≥1 exact-match internal anchor (~5× traffic effect, Zyppy)
- [ ] **Content depth on money pages** (§8.11): real specifics — tables, numbers, named constraints — not just positioning copy (largest single 2025 SearchPilot effect, ~+20%)
- [ ] **External backlinks tracker** started (Ahrefs Webmaster Tools account + tracking sheet from Section 12.2)
- [ ] **If i18n site:** hreflang tags on every page, sitemap contains xhtml:link alternates for every language, /cs/ (or equivalent) routes reachable
- [ ] **If migrating from WP:** every URL from the old sitemap either returns 200 or 301s to a valid destination; 0 unresolved 404s from the top 100 backlinks
- [ ] **If using API route:** wrangler secrets set (`RESEND_API_KEY` etc), test POST returns 200 AND email actually delivers, failure path returns 502 not 200
- [ ] **Email auth DNS live before first send (§16.6):** ONE root SPF TXT + each sender's DKIM selector + a `_dmarc` TXT (at least `p=none` via Cloudflare DMARC Management) all published; a real received test message from each sender shows `dmarc=pass` in its headers. (Ramp `none→quarantine→reject` continues post-launch — record the revisit date in the build log.)
- [ ] **Article meta** on every blog post (`og:type=article`, `article:published_time`, `article:section`, `article:tag`); NOT `og:type=website`
- [ ] **BlogPosting JSON-LD** on every blog post with `inLanguage`, `articleSection`, `author.sameAs`
- [ ] **BreadcrumbList JSON-LD** on every deep page

---

