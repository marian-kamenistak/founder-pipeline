# Web Creator Reference — Interactivity (animations, forms, contact Worker, motion recipes)

Part of the /web-site-creator reference set. Split from build-product-site-reference.md v16 (2026-07). Headings keep their original § numbers.

## 5. Animations + transitions

**Sticky card stacks (method/steps sections):** each card `position: sticky` with `top: calc(var(--header-h) + N*10px)`. Two hard-won rules: (a) measure the sticky header's real height into a CSS var with a ResizeObserver — hardcoded offsets break when the title wraps; (b) the LAST card has no scroll range of its own and will slide up under the sticky header unless the card list gets bottom runway (`md:pb-[22vh]` on the `<ul>`, compensated out of the section padding).

### Act HUD (scrollytelling chapter indicator)

A fixed pill in the bottom-RIGHT corner that names the chapter of the page the visitor is in — "ACT I · HOOK", "ACT V · PROOF" — turning a long landing page into a narrative. Reference implementation: `src/components/ActHud.astro`.

- Sections opt in with a `data-act="ACT II · METHOD"` attribute on the `<section>`; the HUD shows the last section whose top crossed the viewport midline, so unlabeled sections inherit the current act.
- Pill styling: `fixed bottom-[18px] right-5 z-40 rounded-full border border-neutral-900/10 bg-white/80 backdrop-blur-sm px-3.5 py-1.5 font-mono text-[11px] font-semibold uppercase tracking-[0.14em] text-accent` + the standard soft shadow. Bottom-right, one z-layer below the nav (nav is z-50).
- Decorative only: `aria-hidden="true"`, ships with `hidden` and is revealed by the script — no JS, no HUD, no layout shift.
- Scroll handler is rAF-throttled (`ticking` flag), listeners `{ passive: true }`, re-runs on resize.
- The component takes an `initial` prop (the first act's label) so the pill isn't empty before the first scroll event.
- Localize the act labels per language ("ACT IV · FREE TOOL" / "AKT IV · KALKULAČKA") — they're reader-facing copy.

### Hide-on-scroll-down nav (reappear on scroll-up)

The sticky header (`sticky top-0 z-50 transition-transform duration-300 motion-reduce:transition-none`) hides on scroll-down and reappears the moment the user scrolls up, desktop and mobile. Reference implementation: `src/components/Nav.astro`. Rules: never hide within the first header-height of the page, while the mobile drawer (`<details>`) is open, or while keyboard focus is inside the nav; toggle `-translate-y-full` from a rAF-throttled scroll listener. Pair with `html { scroll-padding-top: 5rem; }` so anchor jumps don't land headings under the reappeared nav.


### Page transitions

```astro
---
import { ViewTransitions } from 'astro:transitions';
---
<head>
  <ViewTransitions />
</head>
```

Add `transition:animate="fade"` on main content blocks. Override per-page if a section needs to persist.

### Entrance + scroll reveals

Use Motion One, lazy-loaded.

```ts
// src/scripts/reveal.ts
import { animate, inView } from 'motion';

inView('[data-reveal]', (el) => {
  animate(el, { opacity: [0, 1], y: [16, 0] }, {
    duration: 0.4,
    easing: [0.16, 1, 0.3, 1]
  });
});
```

Markup: `<div data-reveal>...</div>`.

### Stagger

```ts
animate('[data-stagger] > *', { opacity: [0, 1], y: [12, 0] }, {
  delay: stagger(0.06),
  duration: 0.35
});
```

### Micro-interactions

Tailwind for hover/focus. Buttons get `transition-all duration-200 ease-out hover:-translate-y-0.5`. Cards get `transition-shadow hover:shadow-lg`.

### Button interaction baseline — NON-NEGOTIABLE, define once, never per component

A button with no states is a rectangle. Every button ships with FOUR states or it is not done,
and they are defined ONCE on the canonical class in global CSS, never per section.

Why this is a hard rule and not advice: an audit of one production site found
**183 button instances across 47 files and not one `:hover`, `:active`, `:focus-visible` or
`transition` on either canonical class**. Every button on a whole production estate was inert,
including under keyboard focus. It passed every other gate. Nothing catches this unless it is
checked explicitly, because an inert button looks completely correct in a screenshot.

```css
.btn-primary, .btn-secondary {
  cursor: pointer;
  -webkit-user-select: none; user-select: none;  /* double-tap selecting the label reads as broken */
  transition:
    transform 180ms cubic-bezier(0.34, 1.4, 0.64, 1),   /* slight overshoot = "attached to the pointer" */
    background-color 220ms ease, border-color 220ms ease, color 220ms ease, box-shadow 220ms ease;
}

/* GUARD hover behind (hover: hover). Without it a tap leaves a touch device stuck in the hover
   state until the user taps elsewhere — the single most common mobile button bug. */
@media (hover: hover) {
  .btn-primary:hover  { transform: translateY(-2px); background: <one step brighter>;
                        box-shadow: 0 10px 22px -12px <fill colour at ~55%>; }
  .btn-secondary:hover{ transform: translateY(-2px); border-color: <text colour>;
                        background: <text colour at 7%>; }
}

/* :active is not optional — on touch it is the ONLY feedback, since :hover never fires. */
.btn-primary:active, .btn-secondary:active { transform: translateY(0) scale(0.97); transition-duration: 90ms; }

/* focus-visible, NOT focus: a mouse click must not leave a ring behind. Missing entirely is an
   accessibility failure, not a polish gap — a keyboard user cannot see where they are. */
.btn-primary:focus-visible, .btn-secondary:focus-visible { outline: 2px solid <accent>; outline-offset: 3px; }

.btn-primary[disabled], .btn-secondary[disabled],
.btn-primary[aria-disabled='true'], .btn-secondary[aria-disabled='true'] {
  opacity: 0.45; cursor: not-allowed; transform: none; box-shadow: none;
}

/* Drop the MOVEMENT only. Colour, ring and press feedback stay — a reduced-motion user still
   needs full affordance. Killing every state here is the common over-correction. */
@media (prefers-reduced-motion: reduce) {
  .btn-primary, .btn-secondary { transition: background-color 220ms ease, border-color 220ms ease, color 220ms ease; }
  .btn-primary:hover, .btn-secondary:hover,
  .btn-primary:active, .btn-secondary:active { transform: none; }
}
```

Define this on the canonical class and all N instances get it in one edit; per-component hover
classes guarantee drift and guarantee some component gets missed. If a section genuinely needs a
different size, override `font-size`/`padding` in that component and inherit every state.

**Verify before shipping — an inert button is invisible in review:**

```bash
# Against the BUILT html/css, not the source: catches states lost to a scoped-style mistake.
for s in ':hover' ':active' 'focus-visible' 'aria-disabled' 'hover: hover' 'prefers-reduced-motion'; do
  printf '%-24s %s\n' "$s" "$(grep -c -- "$s" dist/**/index.html 2>/dev/null | head -1)"
done
# Then tab to a button in a real browser. If you cannot see where focus is, it is not shipped.
```


### Scroll-reveal recipe library (source: veebilehed24.ee/en/blog/css-scroll-animations-html-css-javascript-examples/)

Fifteen catalogued scroll effects, adopted after an upcoming-events card build.
Pick ONE per surface — the motion budget above still applies. All the
class-toggle effects ride the same IntersectionObserver + `.active`/`.is-in` pattern this file
already documents; the scroll-linked ones set a `--scroll` custom property from a scroll listener.

| # | Effect | Technique (condensed) |
|---|--------|----------------------|
| 1 | Scroll-timeline animation | CSS `animation-timeline` + keyframes (scale/rotate/hue) |
| 2 | Parallax depth layers | `translateY(calc(var(--scroll) * 0.15/0.35/0.65))` per layer |
| 3 | Horizontal scroll section | `translateX(calc(var(--scroll) * -1))` |
| 4 | Scroll zoom hero | `scale(calc(0.6 + var(--zoom) * 1.6))` |
| 5 | Scroll text reveal | `clip-path: inset(0 calc(100% - var(--reveal) * 100%) 0 0)` |
| 6 | Layered card stack | JS per-card translateY/scale/rotate by scroll index |
| 7 | SVG path draw | `strokeDasharray`/`strokeDashoffset` from scroll progress |
| 8 | 3D perspective panels | `translateZ/rotateX/rotateY` under `perspective: 1000px` |
| 9 | Fade-in + slide-up | `opacity:0; translateY(70px)` -> `.active` resolves |
| 10 | **Blur -> Sharp reveal** | full recipe below — the house favourite |
| 11 | Scale-in by viewport proximity | JS distance-from-center drives scale/opacity |
| 12 | Scroll progress bar | width = scrollTop / (scrollHeight - clientHeight) |
| 13 | Section colour transitions | JS RGB interpolation between section colours |
| 14 | Hover simulation on scroll | `.is-hovered` toggled within 150px of viewport centre |
| 15 | Floating elements | IO threshold 0.4 toggles a 3s `float` keyframe loop |

**Blur -> Sharp reveal — the full recipe as shipped in a production events card (`UpcomingEvents.astro`):**

```css
/* Pre-state ONLY under a JS-set class, so a JS failure leaves content visible. */
.js-fx .card         { opacity: .2; filter: blur(14px); transform: scale(.96) translateY(40px); }
.js-fx .card .row    { opacity: .2; filter: blur(10px); transform: translateY(14px); }

.card.is-in          { opacity: 1; filter: blur(0); transform: none;
                       transition: opacity .75s ease, filter .75s ease,
                                   transform .75s cubic-bezier(0.22, 1, 0.36, 1); }
.card.is-in .row     { /* same end state + transitions, each row delayed by var(--d) —
                          set --d: 180ms + i*70ms from JS for a stagger */ }
```

Wrap the whole thing in `@media (prefers-reduced-motion: no-preference)` — with reduced motion
the content is simply visible, unanimated. Blur is compositor-expensive: keep it ONE-SHOT on
entry (never scroll-linked continuous blur), and at most a handful of elements per viewport.

Debugging note that cost an hour in production: **an occluded/background Chrome tab freezes CSS
transitions at t=0** (`document.getAnimations()` shows them `running` with `currentTime: 0`,
`document.visibilityState === "hidden"`). If a reveal "doesn't fire" in remote-driven or
backgrounded testing, check visibility before debugging the CSS — and verify end states with
`document.getAnimations().forEach(a => a.finish())`.


### Mobile horizontal overflow: the page scrolls sideways into empty space

The hardest class of layout bug in this stack, because **it does not reproduce in Chrome** —
not desktop Chrome, not headless Chrome at a real device viewport. Only on an actual iOS device.
Budget for that up front: you cannot fix this from the dev machine, so build a device-side
measurement tool FIRST instead of shipping guesses.

**What it looks like:** on an iPhone the page can be swiped right into black emptiness.
`documentElement.scrollWidth` far exceeds `clientWidth` while `body.scrollWidth` is correct.

**Things that are NOT the answer, each proven wrong the expensive way in production:**

- **`overflow-x: hidden` on `html`/`body` — the web's most-recommended fix — MAKES IT WORSE ON
  iOS.** Safari responds by resizing the LAYOUT VIEWPORT to the overflow width: the whole site
  renders squeezed into the left ~40% of the screen. Shipped it, broke the site, reverted.
- **`overflow-x: clip`** computes correctly and still scrolls: Chrome does not propagate `clip`
  from the root element to the viewport. Only `hidden` propagates, and see above.
- **Walking the DOM for elements wider than the viewport finds NOTHING**, because on Chrome
  there genuinely is no such element. Two separate `getBoundingClientRect` audits (DevTools AI
  and an agent) both correctly returned zero unclipped elements while the phone was clearly
  broken.
- **Grid-vs-flex in the scroll container** looked like a perfect theory (the guilty rail was the
  only `grid grid-flow-col` among three rails; the two flex ones were innocent). Converting it to
  flex changed NOTHING — the rail was still the culprit. Do not let an elegant theory substitute
  for a device re-test.

**What the culprit actually looks like when you find it:** the offending container's own box
FITS (`width 402, right 402` at a 402 viewport) and no single child explains the overflow. It is
the container failing to CONTAIN its scrollable content, caused by something every child shares.

**The method that works — bisect on the device.** Ship a param-gated tool, inert without its
param, and let whoever holds the phone run it:

```js
// ?diag=1    on-screen badge: viewport / document / overflow delta, red when > 1
// ?nofx=all  hide every horizontally-scrolling block; then name the OTHERS to isolate one
// ?bisect=1  AUTOMATIC: hide each child in turn, re-measure, walk into whichever kills the
//            overflow, and print the CULPRIT PATH down to the deepest responsible node
```

The on-screen `scrollWidth - clientWidth` readout matters as much as the hiding: it turns "does
it still feel wrong?" into a number a non-developer can read out from a phone with no devtools.
`?bisect=1` is the highest-value part — it replaces six manual round-trips with one URL.

Once a container is named, narrow WITHIN it with further toggles (hide its absolutely-positioned
children, disable `scroll-snap-type`, zero the negative margins, force `overflow-x: scroll` +
`contain: paint`) rather than guessing at a fix.

**THE FIX, confirmed on device: `contain: paint` on the scroll container.**

```css
.rail {
  overflow-x: auto;
  contain: paint;   /* forces real containment — without it iOS lets the scrollable
                       content expand the DOCUMENT even though the rail's own box fits */
}
```

Put it on EVERY swipeable rail, marquee and carousel viewport as a default, not only on the one
that got caught. On the site where this was found, three other rails were "innocent" purely because of their content;
structurally they were one card away from the same bug.

**Why it is the right fix and the others were not:** the container's box already fits the
viewport — nothing needs resizing, hiding or clipping at the page level. The only thing wrong is
that iOS does not treat the scroll container as a containment boundary. `contain: paint` says
exactly that and nothing else, so it has no layout side effects, no effect on `position: sticky`,
and no visual change on any browser that was already behaving.

Costs nothing, and on a long rail it is a small paint win.

### Motion budget (enforce in code review)

- No single animation over 400ms
- No autoplay video over 6 seconds
- No parallax on mobile
- `prefers-reduced-motion: reduce` kills all motion except essential state changes

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

### Form success state

After submit succeeds, animate the form into a success card in place. No page reload, no toast.

---

## 6. Forms

**Every conversion surface keeps an on-page capture path.** An outbound calendar link as the ONLY conversion path is a single point of failure that also filters out everyone not ready for a call — one audit found four pages where every CTA was the same external booking link, no form, no email capture, and the advertised lead magnet was a "coming in August" stub. Minimum per product surface: the primary CTA (call/booking) PLUS one lower-commitment capture (newsletter, lead magnet, contact form) that lands an email address you own. A promised-but-unbuilt lead magnet is a placeholder — cut it until it's live (§1.9).

### Newsletter tool: choose per product

Options:
- **Buttondown**: dev-friendly API, RSS-to-email, cheap
- **Resend Broadcasts**: same vendor as transactional, single dashboard
- **Beehiiv**: growth tooling, referral program built in
- **MailerLite**: cheapest, decent API
- **Self-hosted via D1 + Resend**: maximum control, more work

Pick before scaffolding. Store API key in Worker secret as `NEWSLETTER_API_KEY`.

### Newsletter signup component

`NewsletterForm.astro`:
- Email input + button
- Inline error states (Zod validation server-side)
- Success state replaces form in place
- Double opt-in default
- Privacy line below input, links to privacy policy

### Contact form

`ContactForm.astro`:
- Name, email, message, optional company
- Honeypot field
- Cloudflare Turnstile widget
- Server-side validation with Zod
- Sends via Resend to your inbox
- Auto-reply with reasonable response time and what happens next

### Server handler (Astro action or Worker route)

```ts
// src/pages/api/contact.ts
import type { APIRoute } from 'astro';
import { z } from 'zod';

const schema = z.object({
  name: z.string().min(2).max(120),
  email: z.string().email(),
  message: z.string().min(10).max(5000),
  company: z.string().max(120).optional(),
  honey: z.string().max(0),
  turnstileToken: z.string()
});

export const POST: APIRoute = async ({ request, locals }) => {
  const body = await request.json();
  const parsed = schema.safeParse(body);
  if (!parsed.success) return json({ ok: false, errors: parsed.error.flatten() }, 400);

  const env = locals.runtime.env;
  const verify = await fetch('https://challenges.cloudflare.com/turnstile/v0/siteverify', {
    method: 'POST',
    body: new URLSearchParams({ secret: env.TURNSTILE_SECRET, response: parsed.data.turnstileToken })
  }).then(r => r.json());
  if (!verify.success) return json({ ok: false, error: 'captcha' }, 400);

  await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: { Authorization: `Bearer ${env.RESEND_API_KEY}`, 'content-type': 'application/json' },
    body: JSON.stringify({
      from: 'site@your-product.com',
      to: 'you@your-product.com',
      subject: `New contact: ${parsed.data.name}`,
      reply_to: parsed.data.email,
      text: parsed.data.message
    })
  });

  return json({ ok: true });
};

const json = (data: unknown, status = 200) =>
  new Response(JSON.stringify(data), { status, headers: { 'content-type': 'application/json' } });
```

---

## 16. Contact form on a static site (Cloudflare Worker + Resend pattern)

Static sites can't POST. The Astro Cloudflare adapter supports per-route SSR — one API route in an otherwise-static build.

### 16.1 Endpoint

`src/pages/api/email-capture.ts`:
```typescript
import type { APIRoute } from 'astro';

export const prerender = false;  // this route runs on the Worker, not at build

const json = (data, status = 200) =>
  new Response(JSON.stringify(data), {
    status,
    headers: { 'content-type': 'application/json; charset=utf-8' },
  });

export const POST: APIRoute = async ({ request, locals }) => {
  let body = {};
  try { body = await request.json(); } catch { return json({ ok: false, error: 'invalid_json' }, 400); }
  const email = (body.email ?? '').trim().toLowerCase();
  const source = (body.source ?? 'unknown').slice(0, 80);
  if (!/^\S+@\S+\.\S+$/.test(email) || email.length > 200) {
    return json({ ok: false, error: 'invalid_email' }, 400);
  }

  // env access safely (may be undefined during local dev)
  let resendKey; let notifyTo = 'you@brand.com'; let notifyFrom = 'leads@brand.com';
  try {
    const env = locals?.runtime?.env ?? {};
    resendKey = env.RESEND_API_KEY;
    notifyTo = env.LEAD_NOTIFY_TO ?? notifyTo;
    notifyFrom = env.LEAD_NOTIFY_FROM ?? notifyFrom;
  } catch {}

  if (!resendKey) {
    console.log('[EMAIL_LOG]', { email, source });
    return json({ ok: true });
  }

  try {
    const r = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: { Authorization: `Bearer ${resendKey}`, 'content-type': 'application/json' },
      body: JSON.stringify({
        from: notifyFrom,
        to: notifyTo,
        subject: `New lead: ${email} (from ${source})`,
        text: `Reply to ${email}.\nSource: ${source}\nUA: ${request.headers.get('user-agent')}`,
        reply_to: email,
      }),
    });
    if (!r.ok) {
      console.error('resend failed', r.status, await r.text().catch(() => ''));
      return json({ ok: false, error: 'send_failed' }, 502);
    }
    return json({ ok: true });
  } catch (e) {
    console.error('resend exception', e);
    return json({ ok: false, error: 'send_exception' }, 502);
  }
};
```

### 16.2 Secrets

Store the API key as a Worker secret (not in the repo):
```bash
cd path/to/project
echo "$RESEND_API_KEY" | wrangler secret put RESEND_API_KEY
```

Optionally also `LEAD_NOTIFY_TO` and `LEAD_NOTIFY_FROM` to override the defaults without a redeploy.

### 16.3 Domain verification with Resend

Before any send works, Resend requires you to verify the sending domain:

1. Resend dashboard → **Domains** → **Add Domain** → `brand.com` → pick EU region if EU data matters.
2. Resend gives you: 1 TXT (SPF), 3 CNAME (DKIM).
3. Add all 4 records to Cloudflare DNS.
4. Resend polls DNS. Verification usually within 60 seconds.
5. Test send from local:
   ```bash
   curl -X POST -H "Authorization: Bearer $RESEND_API_KEY" -H "Content-Type: application/json" \
     -d '{"from":"leads@brand.com","to":"you@brand.com","subject":"Test","text":"Hello."}' \
     https://api.resend.com/emails
   ```
   If unverified: `{"statusCode":403,"message":"...domain is not verified..."}`.

### 16.4 Client-side component pattern

Single email input, honeypot field, client validation, graceful error surface. Show a success card in place of the form on 200, an error message on 5xx.

**Never return `ok: true` when the send failed.** Users see success but no email delivers, and you don't know until leads complain.

### 16.5 Email provider comparison (2026 pricing)

Reviewed for a "contact form on a personal / small-business site" use case (< 1000 emails/mo):

| Provider | HQ | Free tier | Best for |
|---|---|---|---|
| **Resend** | 🇺🇸 | 3,000/mo | Best DX; Claude one-shots the code |
| **Brevo** | 🇫🇷 | 9,000/mo | EU sovereignty + generous free |
| **MailerSend** | 🇱🇹 | 3,000/mo | Pure transactional, EU-native |
| **Maileroo** | 🇦🇺 | 3,000/mo + free dedicated IP | Modern DX, adequacy-decision EU-legal |
| Mailgun | 🇸🇪/🇺🇸 | trial only | Enterprise features, expensive |
| Postmark | 🇺🇸 | none | Elite deliverability, no free tier |
| SES EU | 🇩🇪/🇮🇪 | 62k/mo from EC2 | Cheapest at scale, more setup |
| Scaleway TEM | 🇫🇷 | none | Pure EU sovereignty + cheap |

Skip: Loops (SaaS-priced $49/mo), Mailchimp (marketing bloat), Mailmodo (AMP-focused), Customer.io (enterprise).

**Default recommendation:** Resend for DX, or Brevo / MailerSend if EU data residency is a hard requirement.

### 16.6 Email authentication DNS — SPF · DKIM · DMARC (Cloudflare) — EXPLICIT STEP, never skip

**Why this is its own step.** The moment the site sends *any* mail — Resend transactional/contact-form replies, plus human mail if the domain is on Google Workspace — the domain needs SPF + DKIM + DMARC or (a) mail lands in spam and (b) anyone can spoof `@brand.com`. §16.3 only verifies the Resend sender; this step authenticates the **whole domain across every sender** and is the prerequisite for enforcement (and later BIMI). Assumes the domain's DNS is on Cloudflare.

**Golden rules (memorize — every one has bitten a real send):**
- **Exactly ONE `SPF` TXT at the root** (`@`) and **exactly ONE `_dmarc` TXT**. Two SPF records = `permerror` = every check fails. Merge senders into one string; never stack.
- **Each sender has its OWN DKIM selector** — they don't conflict. Resend = `resend._domainkey`, Google Workspace = `google._domainkey`. Add all of them.
- **DKIM/MX/CNAME mail records must be "DNS only" (grey cloud) in Cloudflare** — never proxied (orange). Proxying a DKIM CNAME or a mail MX breaks it silently.
- **Resend's SPF lives on the `send.` SUBDOMAIN, not the root.** Do NOT cram `include:amazonses.com` into the root SPF. Resend mail still passes DMARC via DKIM alignment (`d=brand.com`) + relaxed SPF alignment on the `send.brand.com` Return-Path. The root SPF is only for mail sent *directly* as `@brand.com` (i.e. Google Workspace SMTP).
- **Never jump straight to `p=reject`.** Stage it. Enforcing before all legit senders are aligned quarantines a real newsletter/receipt blast.

**Step 1 — Inventory every sender first (do this before touching DNS).** List everything that will send as `@brand.com`: Resend (always, for forms), Google Workspace / mailbox host (if human mail on the domain), any newsletter tool (§6), booking (Calendly etc.), your CRM, e-sign, invoicing. Each one needs its SPF include + DKIM selector accounted for below. A sender you forget is a sender that breaks when you enforce.

**Step 2 — SPF (one root TXT).** Build a single record for the direct-`@brand.com` senders only:
- Google Workspace mailbox: `v=spf1 include:_spf.google.com ~all`
- No Google Workspace, Resend-only site (forms send from `@brand.com` but via Resend's DKIM/subdomain): a root SPF is optional for deliverability but publish a neutral one anyway so a bare `@brand.com` never softfails: `v=spf1 ~all` (DKIM carries DMARC alignment).
- Keep `~all` (softfail) until DMARC is at enforcement; only then consider tightening to `-all`.

**Step 3 — DKIM (one selector per sender, all added).**
- **Resend**: add exactly what the Resend dashboard lists (§16.3) — typically MX + SPF TXT on `send.brand.com` and a `resend._domainkey` DKIM record. DNS-only.
- **Google Workspace**: Admin console → Apps → Google Workspace → Gmail → Authenticate email → generate 2048-bit key → publish the `google._domainkey` TXT in Cloudflare → back in Admin, click **Start authentication**. (Missing this = Google mail is SPF-only and fails DMARC on any forward.)
- Any other sender: add its selector per its docs.

**Step 4 — DMARC. Default path = Cloudflare DMARC Management (free, native, no external analyzer).**
1. Cloudflare dash → the zone → **Email → DMARC Management → Enable**. It auto-creates the `_dmarc` TXT at `p=none` with `rua=` pointing at `…@dmarc-reports.cloudflare.net` and parses aggregate reports in-dashboard for free.
2. If setting it manually instead, publish one `_dmarc` TXT:
   `v=DMARC1; p=none; rua=mailto:dmarc@brand.com; fo=1; adkim=r; aspf=r`
3. **Monitor 1–2 weeks.** In the DMARC report view, confirm EVERY legitimate source shows **aligned pass** (DKIM and/or SPF). Any legit source failing = fix its DKIM/SPF before moving on. Unknown IPs failing = spoofers; that's exactly what enforcement will kill.
4. **Ramp only once reports are clean:** `p=none` → `p=quarantine; pct=100` → (after another clean week) `p=reject`. Edit the single `_dmarc` record each time. Quarantine is reversible (spam-folder, not bounce); use it as the safe first enforcement.

**Step 5 — Verify (paste-ready):**
```bash
D=brand.com
echo "SPF:";   dig +short TXT $D | grep -i spf1
echo "DMARC:"; dig +short TXT _dmarc.$D
echo "Resend DKIM:"; dig +short TXT resend._domainkey.$D | head -c 80; echo
echo "Google DKIM:"; dig +short TXT google._domainkey.$D | head -c 80; echo
# Then send a live test through each sender and read the raw headers:
# Authentication-Results: ... spf=pass ... dkim=pass ... dmarc=pass (p=...)
```
A green `dig` proves the record exists; only `dmarc=pass` in a **real received message's headers**, from **each** sender, proves alignment. Don't enforce on `dig` alone.

**Optional hardening (add after DMARC is at enforcement):** MTA-STS (`_mta-sts` TXT + policy file) + TLS-RPT (`_smtp._tls` TXT) for enforced TLS; BIMI (`default._bimi` TXT → SVG Tiny P/S logo) — but BIMI's inbox logo needs `p=quarantine`/`reject` first AND, for Gmail/Apple display, a paid VMC (~$1–1.5k/yr + registered trademark), so treat BIMI as a separate brand decision, not part of the default build.

**Write to the build log:** senders inventoried, records added (with selectors), DMARC path (Cloudflare Management vs manual), current DMARC policy stage, and the date to revisit for the next ramp.

---

## Appendix C. Motion recipes

### Fade-up reveal
```ts
animate(el, { opacity: [0, 1], y: [16, 0] }, { duration: 0.4, easing: [0.16, 1, 0.3, 1] });
```

### Stagger children
```ts
animate('[data-stagger] > *', { opacity: [0, 1], y: [12, 0] }, { delay: stagger(0.06), duration: 0.35 });
```

### House effect kit — the CSS+JS that makes a new build render identical to your existing sites
Canonical source: **your configured brand kit's `kit/` directory** (a `global.css` effect layer plus portable components — the reference kit ships `NeuralNet.astro` and `GalleryGlitch.astro`). **Copy verbatim — do not re-type.** Keep a parity checklist in the kit's README. The pieces below are the reference kit's; substitute your own equivalents:

- **Marker highlight** — the skewed brush stroke (NOT a flat band). One class, applied to `<span class="mark-hl">` on 2–3 phrases:
  ```css
  .mark-hl { background: linear-gradient(104deg, rgba(250,220,80,0) 1%, rgba(250,220,80,.85) 3%, rgba(250,220,80,.55) 96%, rgba(250,220,80,0) 99%);
    padding: 0 .15em; margin: 0 -.05em; border-radius: .2em; -webkit-box-decoration-break: clone; box-decoration-break: clone; }
  ```
- **Staggered scroll reveal** — `[data-reveal]` fades a container's direct children; `[data-reveal-children]` staggers a grid's items; one IntersectionObserver toggles `.is-visible`. Prefer a **transition-based** end-state (robust: `.is-visible` sets `opacity:1` directly, so content is never stuck hidden if the timeline is paused), stagger via `transition-delay`:
  ```css
  [data-reveal] > *, [data-reveal-children] > * { opacity:0; transform:translateY(12px);
    transition: opacity 400ms cubic-bezier(.22,1,.36,1), transform 400ms cubic-bezier(.22,1,.36,1); }
  [data-reveal].is-visible > *, [data-reveal-children].is-visible > * { opacity:1; transform:none; }
  [data-reveal-children].is-visible > *:nth-child(2){ transition-delay:70ms } /* …3→140ms, 4→210ms … */
  @media (prefers-reduced-motion: reduce){ [data-reveal] > *, [data-reveal-children] > * { opacity:1!important; transform:none!important; transition:none!important } }
  ```
  IO: `{ threshold: 0.05, rootMargin: '0px 0px 120px 0px' }`, unobserve after reveal, and reveal anything already scrolled above the fold (`entry.boundingClientRect.top < 0`) so anchor/restore-scroll landings aren't blank (§9.2 Fix 6).
- **NeuralNet hero** — `<NeuralNet class="hero__neural" />` inside a `position:relative; overflow:hidden` hero, content at `z-index:1`, canvas `position:absolute; inset:0; display:none; @media(min-width:768px){display:block}`.
- **Pixel glitch** — drop `<GalleryGlitch />` once per layout; tag photo clusters `data-glitch` (one random visible photo glitches every ~5–12s) and standalone photos `data-glitch-solo`. Needs the `.glitch-slice`/`.glitching` CSS from `global.css`. Never on logos or the hero-first photo if it hurts legibility.

**Two gotchas that cost real time:**
1. **Never put `var(--x)` in an `animation` shorthand** (`animation: name 400ms var(--ease) forwards`) — if the custom prop fails to resolve, the whole shorthand is invalid, `animation-name` → `none`, and the element sits at its static `opacity:0` **invisible**. Use a literal `cubic-bezier(…)`, or transitions (above).
2. **Test effects in a FOREGROUND tab.** Reveals, glitch, and NeuralNet all depend on the document animation timeline, which the browser **freezes in a hidden/backgrounded tab** — a screenshot taken while another tab is active shows blank/frozen effects (false failure). To check a reveal end-state independent of the timeline, inject `[data-reveal] > * { transition:none !important }` and confirm `.is-visible > *` computes to `opacity:1`.

### Button press
```css
.btn:active { transform: scale(0.97); transition: transform 100ms; }
```

### Accent-button edge + lift (retrofit pattern)
When the primary CTA color is a flat background fill (Tailwind `bg-accent` or an arbitrary hex like `bg-[#D02E7C]`), it reads as a color block, not a button, until it gets a defined edge and a lift. Add a border one shade darker than the fill plus a soft color-matched shadow:
```css
a.bg-accent, button.bg-accent, a.bg-\[#HEXVALUE\], button.bg-\[#HEXVALUE\] {
  border: 1px solid var(--color-accent-dark);
  box-shadow: 0 4px 14px 0 rgb(from var(--color-accent) r g b / 0.35);
}
```
Ship this as **one global CSS rule** targeting the class(es) the CTA already uses, rather than editing every page/component that has a copy of the button markup. It retrofits every instance (nav, hero, pricing, FAQ toggle, email capture) in one pass and stays correct when new pages reuse the same class. Scope the selector to `a`/`button` tags specifically — a bare `.bg-accent` selector will also catch decorative non-clickable elements (icon badges, chips) that may intentionally set their own border/hover-state logic; don't blanket-override those.

### Display-text lift (H1 + wordmark text-shadow)
Give the H1 and the nav wordmark a soft neutral-gray `text-shadow` so the display type feels raised off the page, family-related to the button shadows but much quieter:
```css
h1, .text-lift {
  text-shadow: 0 3px 16px rgba(23, 23, 23, 0.16);
}
```
Two rules learned the hard way: (1) **text takes shadow much harder than a solid block** — reusing the buttons' 35% alpha reads as a gray smudge under the letters; text needs roughly half or less (10–18%), slightly wider blur, smaller offset. (2) **Neutral gray only, never accent-tinted** — an accent-colored text-shadow on dark-on-light headings reads as a print misregistration, not a lift. Ship as one global rule (`h1` + a `.text-lift` utility for the wordmark and any other display-face text). On dark sections, don't reuse this; light-on-dark wants a glow (white halo + accent-tinted bloom) instead, and if the text animates opacity, a plain `text-shadow` rides the animation for free — never `filter: drop-shadow()` on animating text (forces compositing layers). Cost: ~0 — paint-time only, invisible to PageSpeed.

### Nav scroll-shrink
On scroll past 80px, reduce nav padding from `py-4` to `py-2`, add `backdrop-blur` and `bg-white/80`.

### Form success
Slide form up + fade out 200ms, fade success card in 200ms. Use View Transitions if both elements share `view-transition-name`.

---

## Appendix D. Form patterns

### Contact form (default)
Name, email, message, Turnstile. Honeypot. Inline errors. Success card replaces form.

### Newsletter signup
Email only. Privacy line. Double opt-in. Success: "Check your inbox for confirmation."

### Lead magnet
Email + first name. After submit, email the asset via Resend. Success: "Sent. Check your inbox."

### Gated download
Same as lead magnet, but mark the contact as a warm lead in your CRM via webhook.

---

## Scroll-linked horizontal card shelf (junto.eu pattern, pinned — full spec)

**Main services/products as cards → scroll-linked horizontal track (hard rule).** The signature interaction for the primary offer cards: **as the page scrolls DOWN, the card track translates right → left** (scrolling up reverses it). junto's DOM is the reference: `<div class="list" style="will-change: transform; transform: translate(-2.5314px, 0px); transform-style: preserve-3d;">` — scroll progress is bound to `translateX`. Implement it exactly:
- **Structure (PINNED — house default):** an outer `.shelf` scroll-driver whose height is `100vh + travel`, containing a `position:sticky; top:0; height:100vh; overflow:hidden` pin wrapper, containing the flex track. The section **pins** and the page does NOT advance vertically until the cards have travelled fully right→left. (junto itself only drifts ~2.5px and never pins; the house default is the stronger Apple/Stripe pinned pattern.)
- **Travel = maxX:** set the driver height from the MEASURED overflow so 1px of vertical scroll ≈ 1px of horizontal travel: `shelf.style.setProperty('--shelf-travel', maxX + 'px')` after measuring; recompute on resize + after images decode. Never hardcode the height.
- **Progress (pinned):** `p = clamp(-sectionTop / (sectionHeight - vh), 0, 1)` where `sectionTop = shelf.getBoundingClientRect().top` (goes negative as it scrolls past). `p=0` at pin start, `p=1` when the last card is flush.
- **Un-pin escape hatch (hard):** pinning is scroll-hijack, so it must never trap. Under `prefers-reduced-motion: reduce` AND on touch/narrow viewports, drop the pin entirely (`height:auto`, no sticky, no transform) and leave a plain horizontally-scrollable shelf. Never stack more than ~2 pinned shelves in a page: each one holds the reader hostage for its full travel, and the cost compounds.
- **Range, always MEASURED, never hardcoded:** `maxX = track.scrollWidth - track.clientWidth`; `x = -p * maxX`. This guarantees the first card is flush left at `p=0` and the **last card is fully reachable** at `p=1` — a hardcoded px range strands cards offscreen at some viewport and is the #1 way this effect ships broken.
- **Apply:** `transform: translate3d(x,0,0)` (GPU compositing). Never animate `left`/`margin`/`width`.
- **Drive:** a passive scroll listener that only sets a flag + a `requestAnimationFrame` loop that writes the transform — never write layout-reading transforms inside the scroll handler. Gate the rAF with an `IntersectionObserver` so it only runs while the section is in view; add `will-change: transform` on enter and REMOVE it on exit (no `will-change` on idle elements).
- **Recompute** `maxX` on `ResizeObserver` and after images load (otherwise the range is wrong on first paint).
- **Accessibility (non-negotiable):** the track keeps `overflow-x: auto` + real focusable cards + scroll-snap, so it is fully usable by keyboard/touch/trackpad without the effect. Under `prefers-reduced-motion: reduce`, **disable the scroll-linked transform entirely** and leave it as a plain horizontally-scrollable shelf.
- **Verify:** `document.documentElement.scrollWidth === clientWidth` (no page-level horizontal overflow) at 360px and desktop, and the last card is reachable at both.
- Modern progressive enhancement is allowed via CSS `animation-timeline: view()` behind `@supports (animation-timeline: view())`, with the rAF path as fallback.
