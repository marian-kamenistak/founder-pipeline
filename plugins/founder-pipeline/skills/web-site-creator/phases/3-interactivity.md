# Phase 3 — Interactivity: motion, signature effects, forms

Reference: [`references/interactivity.md`](../references/interactivity.md). Perf gate: [`references/gates.md`](../references/gates.md) §9.1.

Runs after GATE 2 (sequential with Phase 2 — same files).

## 3.1 Effect layer

- [ ] [S] **If your brand kit ships an effect kit, copy it verbatim** — a `kit/` folder holding `global.css` plus one component per signature effect. Never hand-reimplement; rewrites drift every time. A kit of this shape typically carries: a generative hero canvas, a pixel-glitch treatment on a photo cluster (`data-glitch`), a `.mark-hl` skewed marker for 2–3 phrases, staggered reveals (`[data-reveal]`/`[data-reveal-children]` + `.is-visible`), and a `.logo-wall` grayscale→color pass. Keep the kit's gotchas in its README next to the code (two that bite on this stack: no `var()` inside an `animation` shorthand, and verify every effect in a FOREGROUND tab)
- [ ] [S] Brand with no effect kit: ONE signature animation of equal ambition — designed via `/frontend-design:frontend-design` (optional dependency; if that plugin isn't installed, design it yourself against the Phase 2 tokens and the "one signature move" bar in SKILL.md), then promote it back into that brand's kit so the next build inherits it
- [ ] [S] Animations: reveals on 1–2 sections max, nothing over 400ms, `prefers-reduced-motion` kills all motion (the calm variant is a first-class design, not a fallback)
- [ ] [S] Reveal animations force-show content already past the fold on load (anchor/restore-scroll landings); hero content NEVER behind a reveal (Phase 1 hard rule)
- [ ] [S] **Main offer cards → pinned scroll-linked horizontal track** — full spec in `references/interactivity.md` → Scroll-linked horizontal card shelf. Non-negotiables: measured travel (never hardcoded), un-pin escape hatch on reduced-motion + touch/narrow, keyboard/touch usable without the effect, rAF-driven `translate3d`, last card reachable at every viewport
- [ ] [S] Sticky card stacks: measure header height into a CSS var via ResizeObserver + bottom runway on the last card
- [ ] [S] **No interaction-dead cards:** every clickable card, pricing tier, person row has a hover state (lift + accent border); card grids reuse ONE persona-card design site-wide (white card, accent ↗ chip, hover lift, first card default-highlighted via `:has()`)
- [ ] [S] **Mobile nav keeps a menu:** never `display:none` nav links below a breakpoint without a hamburger/`<details>` fallback

## 3.2 Forms

- [ ] [S] **Consent bar** — build the component here (it is UI; the analytics gating it drives is wired in Phase 5 Z2). Full recipe: `references/launch.md` §14.5.8. Non-negotiables: two buttons (Reject + Accept), no Settings panel, `consent_v1` cookie, `html[data-consent]` set by an inline `<head>` reader before first paint, markup always present and revealed by CSS (the HTML is CDN-cached and cannot vary per visitor), body padding reserved so it costs zero CLS, `role="region"` not `dialog`, no scrim, no focus trap, last in tab order
- [ ] [S] Contact: honeypot + CAPTCHA widget + schema validation (Zod) + transactional send + auto-reply; success card replaces form in place
- [ ] [S] Newsletter: double opt-in + privacy line, wired to the tool chosen in Phase 1.0
- [ ] [S] **Never return `ok: true` when the send failed** — failure path returns 502, not 200
- [ ] [S] Sending domain verified with your transactional email provider (its SPF TXT + DKIM CNAME records live in your DNS) BEFORE testing sends
- [ ] [S] **Email auth DNS — SPF + DKIM + DMARC, never skip:** inventory every `@yourdomain` sender; ONE root SPF TXT + ONE `_dmarc` TXT; per-sender DKIM selectors, all DNS-only (never proxied through a CDN); DMARC `p=none` → monitor 1–2 wks → ramp `none → quarantine → reject`, never jump. Verify with real received-message headers (`dmarc=pass`), not just `dig`

## 3.3 Performance pass (`references/gates.md` §9.1 — the 68→99 recipe, in order)

- [ ] [S] Lazy-load every third-party embed via IntersectionObserver placeholder swap (biggest lever)
- [ ] [S] Fonts non-blocking (`preload as=style` + onload swap + noscript)
- [ ] [S] No `will-change` on idle/pre-animation elements
- [ ] [S] Measure at pagespeed.web.dev (web UI, not the quota-limited API), mobile, 3-run stability

## GATE 3 → Phase 4/5

Effect parity: grep `dist/` for your kit's own effect markers (on the kit shape above: `grep -roE 'mark-hl|data-neural|data-glitch|is-visible|data-reveal-children|logo-wall' dist/`) — missing markers = drift · effects verified in a FOREGROUND tab (hidden tabs freeze the animation timeline; a background screenshot is a false failure) · forms tested end-to-end: POST 200 AND the email arrives · reduced-motion pass · `document.documentElement.scrollWidth === clientWidth` at 360px and desktop · **Lighthouse 95+ mobile, TBT 0, CLS < 0.05** · design review round 3 (full P0/P1/P2 sweep incl. mobile) run, findings fixed and re-verified — any P0 blocks publish.
