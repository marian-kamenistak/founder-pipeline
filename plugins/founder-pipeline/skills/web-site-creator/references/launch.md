# Web Creator Reference — Launch (deploy, indexing machinery, KPIs, analytics stack)

Part of the `/founder-pipeline:web-site-creator` reference set. Headings keep their original § numbers.

> **This file is written against the house stack declared at the start of the build** (see the skill's
> house-stack section). The recommended default — and the stack every worked example below uses — is
> Astro on Cloudflare Workers, with an edge CDN, a product-analytics SDK, and a CRM. If your declared
> house stack differs, the *rules* still hold; the specific commands and dashboard paths are the
> example, not the mandate.

## 10. Deploy

```bash
pnpm build
wrangler deploy
```

Custom domain: add via your platform's dashboard as a route on the deployed Worker. SSL automatic.

---

## 11. Post-launch checklist (in order)

Day of launch:

- [ ] Cloudflare Web Analytics enabled
- [ ] PostHog instrumented + verified (page view, CTA click, form submit events firing)
- [ ] `robots.txt` reachable and validated
- [ ] `llms.txt` + `llms-full.txt` reachable and validated
- [ ] NLWeb endpoint reachable, `/.well-known/nlweb.json` resolves
- [ ] Sitemap reachable, validates against XML schema
- [ ] All OG cards rendered correctly (test in opengraph.xyz)

Within 48 hours:

- [ ] Run **`/founder-pipeline:web-indexation`** (one-time per-property setup: GSC verified + sitemap submitted + robots.txt re-fetched, Bing Webmaster verified + sitemap manually submitted, IndexNow key live at root) — this is where GSC/Bing/IndexNow wiring lives, not inline here
- [ ] Any **regional search engine** that matters for your home market (see `/founder-pipeline:web-indexation`) — skip if your traffic is Google/Bing-only
- [ ] **Edge/CDN analytics** verified receiving page views
- [ ] Send the first newsletter to your list, and run a week-0 AI-search probe (ask ChatGPT/Perplexity the three queries the site is built to answer, record whether it is cited — this is your baseline; re-run monthly)

Within 2 weeks:

- [ ] Claim the business listing on the major map/local surfaces if the business serves a place; seed the first external backlinks (`/founder-pipeline:web-backlinks`, `/founder-pipeline:web-listings`); register the site's MCP server if it exposes one
- [ ] First Lighthouse CI run in production passes all thresholds

### 11.1 Every new page after launch — reindex + where else to submit

**Standing loop, not launch-only — owned by `/founder-pipeline:web-indexation`.** Every time a new page (or a materially-changed one) is deployed to a live site, invoke that skill the same day: it covers the IndexNow ping (instant, across the engines that accept it), the Google reindex queue (never click Request Indexing directly — the quota is per Google *account*, so one click can starve every other site you own), sitemap/llms.txt confirmation, and the AI-crawler findability levers (robots.txt allowlist, llms.txt, Bing index, citations, internal interlinking). Full recipes (curl commands, queue schema, one-time setup) live in that skill — don't re-derive them here.

---

## 14. KPIs + instrumentation

Pulled from `/founder-pipeline:founder` Stage 19 (KPIs). The site is the conversion surface for the stream's north-star.

### North-star (behavioral, tied to revenue)
One metric. Example: **completed intro calls per month** if you sell consulting; **paid pilot signups per month** if you sell pilots; **trial-to-paid conversions per month** if SaaS.

### Leading indicators (3-5)
- Homepage → pricing page CTR
- Pricing page → contact form submit rate
- Blog reader → newsletter signup rate
- Cold visitor → return visitor rate (7-day)
- LinkedIn click-through to site

### Lagging (revenue side)
- Monthly recurring or one-time revenue from site-sourced leads
- CAC: spend per acquired customer from site channel
- Payback period
- 6-month retention (if recurring)

### Vanity-check filter
For every metric, ask: "if this number goes up but revenue doesn't, do I care?" If no, drop it.

### Instrumentation
Wire from day 1, before launch. If you use PostHog, the `posthog` plugin ships an
`/posthog:instrument-product-analytics` skill that does this end-to-end — it is an **optional
dependency you install separately**, not part of this plugin. Otherwise instrument your own SDK by
hand against the event list below.

Minimum events:
- `page_view` (auto)
- `cta_click` with `cta_location` + `cta_label`
- `form_submit` with `form_type` (contact / newsletter / lead magnet)
- `pricing_tier_clicked` with `tier`
- `blog_post_read` with `slug` + scroll depth
- `outbound_click` with destination

---

## 14.5 Web analytics stack (four layers)

§14 defines *which* metrics matter; this section is *how the tracking is physically wired* so those metrics exist, agree with each other, and land in the CRM. Wire the whole stack BEFORE launch (Phase 7 gate) — retrofitting attribution after traffic starts loses the baseline permanently.

**The stack has four layers, each with one job; do not collapse them.** The tools named below are the house-stack default and the worked example the rest of this section is written against — substitute your own per layer, but keep the four-layer split.

| Layer | Tool (default) | Job | Don't use it for |
|---|---|---|---|
| Product analytics | **PostHog** | funnels, session replay, event-level behaviour, feature flags, A/B | ad-platform conversion import (its client events are ad-blocked ~30%) |
| Web/marketing analytics | **GA4 via Google Tag (gtag/GTM)** | channel/source attribution, Google Ads conversion import, Search Console join | deep behavioural funnels (GA4's UI is worse than PostHog's) |
| Privacy-light traffic | **Your edge/CDN's built-in analytics** | server-side, cookieless pageview + Core Web Vitals truth (no ad-block gap) | events / conversions |
| CRM + revenue truth | **Your CRM** (worked example below: Attio) | lead → opportunity → revenue; closes the loop back to ad platforms | anonymous traffic |

**Consent — reject-only is the default.** All of GA4, GTM, and PostHog autocapture set cookies / process PII, so every build ships a consent bar. The default model is **opt-out**: two buttons (Reject + Accept), no Settings panel, everyone treated as accepted until they click Reject. Full recipe in **§14.5.8** — build from it, don't improvise, and read §14.5.8's "What breaks silently" list before writing the Reject handler. Edge/CDN analytics is cookieless and runs regardless (it is injected above your origin and the bar cannot govern it — say so in the privacy policy rather than implying otherwise).

> **Opt-out diverges from EU law, and shipping it is a deliberate commercial call the owner has to make, not a default you inherit.** Most EU member states require opt-in, and "by continuing you agree" is explicitly not valid consent anywhere in the EEA. *Worked example of how specific this gets:* Czech law has required opt-in since 1 Jan 2022 (zákon č. 374/2021 Sb., amending §89(3) of 127/2005 Sb.). **For a client build, an EU-regulated site, or any site running Google Ads to EEA/UK traffic, switch to strict opt-in** — Google's EU User Consent Policy requires a `granted` signal to reflect real consent, and Google can disable personalised ads or suspend the account, which is a live enforcer where the regulator is theoretical. §14.5.8 exposes the two constants that flip the posture. **Check your own jurisdiction before adopting the default; this file is not legal advice.**

### 14.5.1 Google Tag / GTM + GA4

- **Load pattern.** Prefer **GTM** as the single container (GA4 + LinkedIn Insight Tag + Google Ads tag all live inside it → no per-tag code edits later). Route it through **Partytown** or lazy-inject after consent so it stays off the LCP critical path (§9.1 — third-party JS is the #1 mobile-perf killer). GA4 config tag fires `page_view` on route change (SPA-safe: hook Astro `astro:page-load`).
- **Consent Mode v2** installed with all six of `ad_storage`, `ad_user_data`, `ad_personalization`, `analytics_storage`, `functionality_storage`, `personalization_storage` **`granted` by default** under the reject-only model, and a `denied` default emitted instead when the stored state is already `rejected`. `security_storage` stays `granted` in BOTH payloads — it covers anti-fraud and authentication, and denying it is Google's own documented anti-pattern. **Delete the `region: [...]` array and `wait_for_update` rather than flipping them**: leaving `region` in place after flipping the signals grants the rest of the world and denies Europe, the exact inverse of the intent, and `wait_for_update: 500` adds 500ms to every hit waiting for an update that never comes. Payloads and the branch in §14.5.8. Under strict opt-in (client/EU builds) the original `default: denied` → `update: granted` shape is correct instead.
- **Server-side option:** for the money conversions, prefer **GA4 Measurement Protocol** (or GTM server-side on a Cloudflare Worker) fired from the same `/api/*` route that already handles the form — server events survive ad-blockers and Safari ITP, and carry the same dedup ID as the client event.
- **Mirror the §14 events into GA4** with the same names so the two tools tell the same story. Mark `form_submit` (contact / pilot / call-booked) and `pricing_tier_clicked` as GA4 **key events (conversions)** — those are what Google Ads optimizes toward, and they are the events your paid-ads setup will bid against.
- **Join Search Console** to GA4 and to the property so organic query data lands in one place (feeds §18 keyword rounds).

### 14.5.2 PostHog dashboards (ship these, not raw event lists)

A pile of events nobody looks at is not analytics. Build these dashboards day 1 so the numbers have a home:

1. **Acquisition** — pageviews & uniques by `utm_source`/`utm_medium`/`utm_campaign` and referrer; new vs returning; top landing pages. (This is where paid traffic shows up — tag every ad URL with UTMs.)
2. **Conversion funnel** — `page_view` (landing) → `cta_click` → `form_submit` → (from the CRM) `booking_confirmed`, as a Funnel insight, sliced by source so you see which channel converts, not just which delivers clicks.
3. **Content** — `blog_post_read` by slug + scroll-depth, newsletter-signup rate per post → feeds the §20 blog-scaffold decisions.
4. **Money-page health** — pricing-page views, `pricing_tier_clicked` distribution, contact-form start-vs-submit (drop-off = friction), session replays filtered to `form_submit` abandoners.
- Set the **north-star (§14) as an Insight pinned to the top dashboard**; wire an alert (chat/email) when weekly conversions drop below a floor.
- Enable **session replay**, but sample it and mask inputs — replay of form abandoners is the highest-value qualitative signal.

### 14.5.3 Edge / CDN analytics

- Turn it on in your CDN's dashboard for the deployed Worker/zone (part of the `/deploy` step). Cookieless, server-side beacon — it's the ground-truth pageview count when ad-blockers dent GA4/PostHog, and it reports real Core Web Vitals (CrUX-style) from actual visitors, which validates the §9.1 lab scores.

### 14.5.4 Connect the CRM (close the loop)

The point of analytics is revenue attribution, and revenue lives in the CRM. Two directions. The API shape below is a worked example against the default CRM named in §14.5; the pattern is the same for any CRM with an upsert endpoint.

- **Site → CRM (lead capture).** The same `/api/contact` | `/api/email-capture` Worker route that sends the transactional email also upserts a **Person** (and **Company** by email domain) in the CRM via its API — carrying `utm_*`, `referrer`, `landing_page`, the analytics `distinct_id`, and the session-replay URL as attributes, so a sales conversation opens with full context. Read the CRM API token from your secrets store at deploy time and bind it as a Worker secret; never commit it and never read it from a file the repo can see. Idempotent upsert keyed on email; never block the user's success response on the CRM call (fire-and-forget with retry; the email + 200 path is independent — §16.4).
  ```
  POST https://api.<your-crm>/v2/objects/people/records   (assert = upsert on email_addresses)
  Authorization: Bearer <token from your secrets store>
  body: { data: { values: { email_addresses:[{email_address}], name, ... custom attrs: utm_source, utm_campaign, landing_page, replay_url } } }
  ```
  Create the custom attributes (`utm_source`, `utm_campaign`, `landing_page`, `lead_source_detail`, `replay_url`) on the Person object once, before wiring the route.
- **CRM → ad platforms (offline conversion feedback).** When a lead becomes a booked call / pilot / customer in the CRM, that status change is the signal Google Ads and LinkedIn actually need to optimize on (clicks are noise; qualified pipeline is signal). Export won/qualified records — with the click IDs captured at capture time (`gclid` for Google, `li_fat_id` for LinkedIn, stored as CRM attributes) — back as **offline conversions** (Google Ads Offline Conversion Import / Enhanced Conversions for Leads; LinkedIn Conversions API). That export belongs to your paid-ads setup, not to the web build; **the web build's only job here is to capture and persist `gclid`/`li_fat_id`/`utm_*` at form submit** so they exist when the deal closes weeks later. Grab them from the URL on landing, stash in a first-party cookie, include in the CRM upsert.

### 14.5.5 Zone hardening

Your CDN does **not** default a new zone to secure. A live-zone audit of one site launched months earlier found `always_use_https` off, no HSTS, `min_tls_version` at the 1.0 floor, and Early Hints off — none of it caught, because nothing in the pipeline checked it. Apply these four via the API at launch, not from the dashboard by hand (scriptable, repeatable per zone).

The commands below are the worked example for the default house stack. Export your CDN API token from your secrets store into the shell first — never inline the token, never commit it:

```bash
API_TOKEN=<your CDN API token, from your secrets store>
ZONE_ID=<zone id — GET /zones?name=<domain>>

curl -s -X PATCH -H "Authorization: Bearer $API_TOKEN" -H "Content-Type: application/json" \
  "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/settings/always_use_https" -d '{"value":"on"}'

curl -s -X PATCH -H "Authorization: Bearer $API_TOKEN" -H "Content-Type: application/json" \
  "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/settings/min_tls_version" -d '{"value":"1.2"}'

curl -s -X PATCH -H "Authorization: Bearer $API_TOKEN" -H "Content-Type: application/json" \
  "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/settings/early_hints" -d '{"value":"on"}'

curl -s -X PATCH -H "Authorization: Bearer $API_TOKEN" -H "Content-Type: application/json" \
  "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/settings/security_header" \
  -d '{"value":{"strict_transport_security":{"enabled":true,"max_age":15552000,"include_subdomains":true,"preload":false,"nosniff":true}}}'
```

- **`preload: false` is deliberate — never flip it without the owner's explicit sign-off.** HSTS preload submits the domain to the browser-vendor-maintained preload list baked into Chrome/Firefox/Safari; getting a domain OFF that list again takes months and a browser release cycle, and it hard-breaks every subdomain that ever runs plain HTTP. Ship 6 months at `max_age: 15552000` first, confirm nothing on the domain (or a subdomain) depends on unencrypted HTTP, then reconsider.
- **DNSSEC and WAF managed rules are separate asks — not part of this default four.** Both are one-way commitments (DNSSEC needs a DS record at the registrar; a WAF managed ruleset can false-positive against a launch's own forms) and neither is a Phase-6 blocker. Raise them with the owner per-domain if the audit surfaces them.
- **Don't enable Bot Fight Mode or any AI-bot-blocking toggle (`ai_bots_protection`, `ai_training`, `ai_search`, `ai_user`) on a domain whose strategy depends on AI-search visibility.** That strategy needs GPTBot/PerplexityBot/ClaudeBot to reach the site, and a bot-fight false-positive is invisible until the next citation-rate check comes back down. If Bot Fight Mode is ever turned on, re-run the crawler-delivery matrix (`phases/5-seo.md` §5.3) immediately after, and re-check AI-crawler access with `/founder-pipeline:ai-seo`.
- Verify after applying: `curl -I http://<domain>/` should 301 to `https://`; `curl -sI https://<domain>/ | grep -i strict-transport` should show the `max-age`.

**Publish-gate additions (Appendix F):** consent bar shipped per §14.5.8 (Reject verified to delete the analytics and `_ga*` cookies on ALL THREE domain forms, pageviews still firing after Reject, `gcs=G100` on the GA hit, no recorder.js request, CLS identical with and without the bar); privacy page carries a cookie table + `#cookie-settings` + a bumped date + every processor named; Consent Mode v2 granted-by-default with `region`/`wait_for_update` deleted and `security_storage` granted in both payloads; GA4 key events marked; the 4 analytics dashboards built + north-star pinned; edge/CDN analytics on; zone hardening applied (always_use_https, HSTS, TLS min 1.2, Early Hints) and verified live; CRM upsert tested end-to-end (submit form → record appears with UTMs); `gclid`/`li_fat_id` capture verified in the stored record; WebMCP enabled (§14.5.6); Crawler Hints enabled (§14.5.7).

### 14.5.6 WebMCP (Beta) — Agent Readiness

Cloudflare dashboard toggle, zone-level: **Agent Readiness → WebMCP**. Injects a lightweight bridge (`HTMLRewriter`-based, one `<script>` tag) into every HTML response so browser-based AI agents can read and interact with the page — no origin code change, no redeploy. Enable the main toggle plus both tool packs (**Content Credentials / C2PA** and **Site MCP server** — both default on when the main toggle flips).

**Dashboard-only — no Zone Settings API existed for it at the time of writing** (not in the documented `/zones/{zone_id}/settings/{setting_id}` list, no JSON body published; re-check, this is a moving target). Unlike §14.5.5's hardening four, this cannot be scripted with curl right now — do it by hand per zone: Cloudflare dashboard → zone → **Agent Readiness → WebMCP** → enable + confirm both tool-pack sub-toggles are on. Re-check periodically; Cloudflare tends to backfill Settings API support for dashboard betas once they exit preview — if it appears, add the PATCH recipe here next to §14.5.5.

Do this at launch alongside the other zone-level toggles in §14.5.5, on the same domain.

### 14.5.7 Crawler Hints

Cloudflare dashboard toggle, zone-level: **Caching → Configuration → Crawler Hints** (Beta). Sends search engines a signal when cached content changes, so they time recrawls instead of polling blind — no origin change, no redeploy.

**Dashboard-only — no Zone Settings API existed for it at the time of writing** (not in the `/zones/{zone_id}/settings` list, no documented setting ID). Same as §14.5.6's WebMCP: do it by hand, one click, per zone — dashboard → zone → **Caching → Configuration** → scroll to **Crawler Hints** → enable. Enabling implicitly agrees to the vendor's Supplemental Terms for the feature (shown inline on the toggle).

Do this at launch alongside the other zone-level toggles in §14.5.5/§14.5.6, on the same domain. Worth applying retroactively across every zone you already run, not just new ones.

### 14.5.8 Consent bar — the reject-only recipe

Built and verified in production on two live sites. Two buttons, **Reject** and **Accept**, no Settings panel. Everyone is treated as accepted until they click Reject.

#### The contract — copy this verbatim into every build

| | |
|---|---|
| **Cookie** | `consent_v1`, values `accepted` \| `rejected`, anything else treated as absent |
| **Attributes** | `path=/; max-age=15552000; SameSite=Lax; Secure` (180 days), **no `Domain`** (host-only) |
| **Absent** | → effective state `accepted`, **and** the bar shows |
| **Signal** | `<html data-consent="ask\|accepted\|rejected">`, set by an inline `<head>` reader before first paint |
| **Global** | `window.__consent` → `{ stored, state, hasChosen(), isRejected(), set(v), reopen() }` |
| **DOM** | `<aside id="consent-bar" data-consent-bar role="region">`, buttons `<button type="button" data-consent-action="accept\|reject\|reopen">` |
| **Event** | `window.dispatchEvent(new CustomEvent('consent:change', { detail: { state, previous, hadChoice } }))` |
| **Anchor** | `#cookie-settings` on the privacy page |

**Version the cookie name.** The `_v1` suffix is the whole point: when the policy changes, ship `consent_v2` and every stored answer on the internet is invalidated in one line, with no migration and no stale consent honoured under new terms.

**Cookie, not localStorage.** `localStorage` throws in private-mode Safari and in partitioned contexts; `document.cookie` never throws, and this is the one script that must not fail — if the reader throws, the `<head>` block dies and every gate downstream fails open. A cookie is also readable at the Worker edge and expires without hand-rolled timestamp logic.

**Safari ITP will silently expire the answer in 7 days. Handle it or the bar is broken by design.** Since ITP 2.3 every cookie written via `document.cookie` is capped at **7 days** no matter what `max-age` says. Under an opt-out model that means an explicit Reject decays back to "no stored choice" = accepted, on a weekly cycle, forever. **This is a bigger exposure than the opt-in/opt-out question itself** — it turns a recorded "no" into a fresh "yes" without the visitor doing anything.

A `localStorage` mirror does **not** fix it: WebKit applies the same 7-day cap to all script-writable storage (localStorage, sessionStorage, IndexedDB, Cache API, service workers) and wipes the lot together. The one real difference is that the storage clock resets on interaction with the site while the cookie's expiry is absolute from write time.

**The fix is four lines: rewrite the cookie on every pageload when a stored choice exists.** That refreshes the 7-day window each visit, so the answer only lapses after 7 days of not visiting at all, which is defensible.

```js
var v = readCookie('consent_v1') || lsGet('consent_v1');
if (v === 'accepted' || v === 'rejected') { writeCookie('consent_v1', v); lsSet('consent_v1', v); }
```

Keep the localStorage mirror as a second source anyway — it survives a cookie-jar clear that leaves storage intact, and vice versa — just don't let it carry the ITP argument.

**The real escape hatch, if the site needs one:** cookies set by a `Set-Cookie` response header are exempt from the JS cap and get the general 400-day limit. On this stack that is a `POST /api/consent` route returning `204` plus the header, about 15 lines. It does **not** compromise cacheability, because no HTML response varies — the mandatory `purge_everything` deploy model stays intact. Worth doing on any site where a lapsed consent decision is a real problem.

#### The static-site constraint that dictates the design

Both the HTML and the CDN cache are shared by every visitor (`purge_everything` zones), so **the markup cannot vary on the cookie** and you must not add a Worker that makes it vary — that makes every page uncacheable. Therefore: the bar is always in the HTML, `display: none` by default, and revealed by CSS only for `html[data-consent="ask"]`. Reserve its height with `html[data-consent="ask"] body { padding-bottom: … }` so the space exists in the **first** layout, not as a shift.

Side effect worth having: the attribute is only ever set by JS, so **no-JS visitors and non-executing crawlers never see the bar.** Googlebot, GPTBot, ClaudeBot and PerplexityBot read a clean page, and the bar cannot pollute an LLM's reading of it.

#### Pull for init, push for live changes

Not a compromise, two different questions. **Init-time config must pull** (`window.__consent.isRejected()`) — an analytics boot inside `requestIdleCallback` may run before or after the bar's script, and an event that already fired is invisible to a listener registered later. **Live changes must push** via the CustomEvent, because a bundled analytics module and an `is:inline` bar script share nothing but `window`.

#### What breaks silently — read this before writing the Reject handler

1. **`opt_out_capturing()` stops ALL capture, pageviews included.** If the spec is "downgrade but keep counting", this is the opposite, and the button *looks* like it works. `cookieless_mode: 'on_reject'` at init is documented to fix that — **it did not, when measured**; see the table below before relying on it.
2. **Cookies are cross-subdomain, and only PostHog cleans up after itself.** `cross_subdomain_cookie` defaults true, so `ph_<token>_posthog` lives on `.example.com` and GA's `_ga`/`_ga_*`/`_gcl_*` likewise. PostHog's `set_config({persistence:'memory'})` internally calls `update_config → clear() → remove()`, which deletes with **both** cross-subdomain flags — so its own cookie is handled. **gtag deletes nothing**: a Consent Mode downgrade stops it *writing* `_ga*` and never removes what is already there. Sweep GA by hand against `''`, `'.'+hostname` and `'.'+registrable domain`. Any hand-rolled delete (including PostHog's on a stack where you can't trust the library version) needs all three forms — a host-only delete passes every other check and leaves the cookie in place.
3. **`reset()` is required, and it must come AFTER the persistence swap.** Swapping persistence does *not* break the identifier: `update_config` saves `props` before `clear()` and restores them into the new store, so the same `distinct_id` keeps going out on the wire for the rest of the pageload. `reset(true)` is what actually breaks it. Called *before* the swap it writes a fresh id straight back into the cookie store, which is worse than not calling it. **Expect three side effects:** a new session id (so pageviews either side of the Reject land in two PostHog sessions — session counts inflate), super properties wiped (any registered attribution props drop and re-register from their cookies on the next pageload, so it self-heals on navigation), and one extra `reloadFeatureFlags()` call.
4. **Check whether `disable_session_recording: true` is already set at init.** Where recording is started by hand for perf reasons, "set `disable_session_recording: true` on reject" is a no-op — the real levers are skipping `startSessionRecording()` and calling `stopSessionRecording()` live.
5. **`pointerdown` fires before `click`.** On any site that boots analytics from an interaction listener, clicking Reject boots analytics, `await`s the import, and inits at full config *after* the rejection. Two fixes, both needed: early-return on `ev.target.closest('[data-consent-bar]')`, and read the consent state **after** the `await`, never before.
6. **Guard on `posthog.__loaded`, not `window.posthog`** — the CDN snippet leaves a stub array on `window` long before the real library lands, and calling `set_config` on the stub queues a call replayed with the wrong intent.

#### The Reject handler — do not try to make PostHog cookieless at runtime

**Measured against a reverse-proxied `array.js` (1.417.1) in a real browser on a live site. Every configuration-based approach failed to stop `ph_<token>_posthog` being written:**

| Attempt | Result |
|---|---|
| `persistence: 'memory'` at init | Cookie written anyway |
| `set_config({persistence: 'memory'})` | Cookie reappears within seconds of deletion — the storage backend is fixed at construction |
| `opt_out_capturing()` | Capture stops, cookie **still** written |
| `cookieless_mode: 'on_reject'` + `opt_out_capturing()` | `is_capturing()` returned **false**, i.e. it killed pageviews too |
| Sweeping cookies + storage at 0s / 3s / 8s / `pagehide` | Re-created every time |

**So: if Reject must mean "nothing stored", do not load the library at all.**

```js
window.addEventListener('load', () => {
  if (window.__consent && window.__consent.isRejected()) return;   // the whole mechanism
  requestIdleCallback(() => initPostHog(), { timeout: 2000 });
});
```

Verified clean: `window.posthog` undefined, no `ph_*` cookie or storage key, nothing reappears, page fully functional. It also cannot break when the vendor ships a new bundle, which a config-based approach can.

**The cost is real and must be agreed up front: rejecting visitors are not counted at all.** "Reject keeps anonymous pageviews" is not achievable this way. Decide which the site wants *before* writing the privacy copy, because the copy has to match. Claiming "stores no analytics identifier" while the library quietly writes one is the worst of the three outcomes.

A **live** Reject (clicked mid-session, library already constructed) needs `location.reload()` after sweeping — the backend cannot be swapped in place. Sweep, then reload into a page that never loads it. Accept the duplicate `$pageview`.

Still sweep on reject for **everything else**: `__ph_opt_in_out_*`, `ph_<token>_window_id` / `_primary_window_exists` in sessionStorage, and all of GA's `_ga*` / `_gcl_*`, which gtag never deletes on a consent downgrade.

> **Measurement trap that will waste an hour.** Clearing storage on a page where PostHog is still live is useless — it rewrites the cookie before you navigate, and the leftover looks like proof that your fix failed. Several readings during this build were wrong for exactly this reason. **Always clear on a page where the library cannot run**, then observe.

Where the library is npm-pinned (not a reverse-proxied `array.js`), `cookieless_mode: 'on_reject'` may behave as documented — but verify it in a browser against the pinned version before believing it, and check `is_capturing()` specifically.

Also clear from localStorage/sessionStorage: `ph_<token>_posthog`, `ph_<token>_window_id`, `ph_<token>_primary_window_exists`, `__ph_opt_in_out_<token>`.

Set `person_profiles: 'never'` on the rejected path. With `identified_only` + memory persistence, any `identify()` from a form mints a profile keyed to a random per-pageload id — junk rows, and a person record for someone who said no.

**Reject is always live and never reloads** (a reload after Reject reads as punitive and re-fires a pageview). **Accept reloads only when upgrading from a stored `rejected`**, which by construction only happens on the privacy page, where a reload is an expected outcome of a settings action. Accept from the bar is a pure state write — the default was already accepted, so there is nothing to upgrade.

#### Never forward a device identifier after a Reject

Where the build decorates outbound links with a `distinct_id` for cross-domain attribution, gate that on `!rejected` **unconditionally**, regardless of any flag that retains attribution cookies. Forwarding an identifier to a third-party origin is the one thing a Reject must always stop — and under memory persistence the forwarded value is a per-pageload random that corrupts the receiving site's funnel anyway.

#### The two constants that flip the posture

Name them, comment them, put them at the top of their block so a future switch to opt-in is one edit:

```js
var ATTR_COOKIES_SURVIVE_REJECT = true;   // false => Reject also stops writing + clears ad-click cookies
var CONSENT_DEFAULT             = 'accepted';  // 'rejected' => strict opt-in, load nothing before Accept
```

#### The privacy page is the enforceable half

Art. 13 GDPR makes the policy the enforceable artefact; the bar is merely the visible one. **If time is short, ship the policy fixes first.** Required on every build:

- A **cookie table**: name / purpose / duration / party. Include the strictly-necessary Cloudflare cookies (`__cf_bm`, `cf_clearance`) — without them, the first person to open DevTools after clicking Reject sees cookies and reports the bar as broken.
- A `#cookie-settings` section with the current state rendered from `window.__consent.state` and a `data-consent-action="reopen"` button.
- Name **every** processor, including the analytics vendor and the host. A policy that promises a cookie bar it does not have, or names a host that was retired, is the first thing an auditor finds.
- Name Cloudflare Web Analytics explicitly as out of the bar's scope if it is on.
- **Bump the "last updated" date.** A cookie policy that changed materially and did not move its date is the single easiest thing to point at.

#### The visual default

A consent bar is a notice nobody came to read. Build it to disappear, not to be noticed.

- **A thin stripe, ~50px desktop.** One line of copy, 13px. Not a card, not a panel.
- **Actions are underlined text links, not buttons.** No background, no border, no pill. **Keep them `<button>` elements** — they perform an action rather than navigating, so a screen reader has to announce "button" and Space has to fire them. Only the paint changes. Do not reach for the design system's primary/secondary button classes: a pill is heavier than the whole stripe should be.
- **Mostly transparent, blurred.** ~50% background plus `backdrop-filter: blur(14px)` on a `::before` so the page shows through instead of being boxed off. Keep the blur on the pseudo-element — an element with `backdrop-filter` becomes the containing block for any `position: fixed` descendant.
- **The policy link is body text colour, not the brand accent.** At 13px an accent-coloured link is the loudest thing on the page, which is backwards.
- **Dismiss on scroll** past ~240px. It must record **nothing** — scrolling is not a choice, and treating it as one is the "by continuing you agree" pattern that is explicitly not valid consent. Scope the dismissal to the tab (`sessionStorage`) so it stops nagging across pages in one visit but asks again later.
- **Tap targets:** text-link actions are ~19px tall, under the 24×24 CSS px minimum in **WCAG 2.5.8 (Target Size, AA)**. Add ~6px vertical padding.
- **Reserve the height with a ResizeObserver**, not per-breakpoint literals: `--consent-bar-h` on `documentElement`, with a CSS fallback for the first frame. The copy wraps to a different number of lines by viewport *and* language, so any fixed number is wrong somewhere — a hardcoded guess ran 18px short on a 402px phone, leaving that much content under the bar.

#### If the bar is hidden on mobile, the privacy page must carry REAL controls

Hiding the stripe below `md` is a reasonable call on a phone. It creates a trap that is easy to miss: **a "Change your choice" control that merely re-shows the bar does nothing at all**, because the bar is `display: none` at that width. The result is a site where a phone visitor cannot reject by any route.

Put actual accept and reject controls on `#cookie-settings`, and delegate the click handler from `document` rather than from the bar so the same controls work in both places. Then the "reopen the bar" concept is unnecessary — drop it.

Whenever the bar is suppressed anywhere, the privacy page is load-bearing: do not remove `#cookie-settings` and do not unlink Privacy from the footer.

#### Accessibility and perf

`role="region"` with an `aria-label`, **not** `role="dialog"` — no scrim, no `aria-modal`, no focus trap, no `inert` on the page. No `aria-live` (the bar is present at load, not injected; on `reopen()` move focus to the first button instead). Escape does nothing, deliberately: it is not a dialog, and dismissing without choosing would itself be a choice. Last in DOM ⇒ last in tab order, and it must never take focus on load. Slide-in goes inside `@media (prefers-reduced-motion: no-preference)`. No image, no icon, no extra font, font-size ≤ 15px — on a sparse page the bar's own text can otherwise become LCP.

---



### 14.5.9 Canonical host — exactly one host serves, the other 301s

**The rule: pick ONE canonical host per zone and make every other host 301 to it, permanently, preserving path and query.** Whether you pick apex or `www` does not matter. Serving both does.

This is not an SEO nicety. A zone that answers 200 on both hosts is broken in three ways at once, and none of them raise an error:

1. **Analytics splits.** Cookies are per-host, so the same person browsing `example.com` and then `www.example.com` is two people in two sessions, and the second one arrives "self-referred" — the site as its own referring domain. Measured on two live sites: several hundred people on the wrong host on one, and a three-figure block of self-referred people on the other.
2. **Link equity splits.** Every backlink to the non-canonical host points at a URL that search engines must reconcile via `rel=canonical` rather than a redirect — weaker, slower, and silently ignored some of the time.
3. **It looks fine.** Both hosts render. The canonical tag is usually correct. Nothing 404s, nothing logs, no build fails. It is invisible until somebody reads a referrer table and wonders why the site refers to itself.

**Audit — run this on every zone, not just the one being launched.** Cheap, and on the estate it was written for it found live bugs on roughly one zone in ten:

```bash
for d in <domain> ...; do
  a=$(curl -s -m 12 -o /dev/null -w "%{http_code}" "https://$d/")
  w=$(curl -s -m 12 -o /dev/null -w "%{http_code}" "https://www.$d/")
  [ "$a-$w" = "200-200" ] && echo "SPLIT: $d serves both hosts"
done
```

**Which host is canonical is not a guess** — read it off the site itself before writing any rule:

```bash
curl -s https://<domain>/ | grep -o '<link rel="canonical"[^>]*>'
```

Redirect *towards* whatever that says. Getting the direction wrong 301s your canonical host into a loop or into a page that does not exist.

**The fix is a zone Redirect Rule, not `_redirects` and not app code.** `_redirects` lives in the assets layer, which a Worker-first route or an edge cache can skip; a Redirect Rule runs in the `http_request_dynamic_redirect` phase, above both, and applies to every request the zone sees. If the zone has no such ruleset yet, `PUT` the phase entrypoint; if it has one, `POST` a single rule so existing rules survive.

```bash
API_TOKEN=<your CDN API token, from your secrets store>
ZONE_ID=<zone id>

# Append to an existing ruleset (get its id from GET /zones/$ZONE_ID/rulesets, phase http_request_dynamic_redirect):
curl -s -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/rulesets/$RULESET_ID/rules" \
  -H "Authorization: Bearer $API_TOKEN" -H "Content-Type: application/json" --data '{
    "action": "redirect",
    "description": "apex -> www (canonical host)",
    "expression": "(http.host eq \"example.com\" and not starts_with(http.request.uri.path, \"/mcp\") and not starts_with(http.request.uri.path, \"/api/\") and not ends_with(http.request.uri.path, \".txt\"))",
    "action_parameters": { "from_value": {
      "status_code": 301,
      "preserve_query_string": true,
      "target_url": { "expression": "concat(\"https://www.example.com\", http.request.uri.path)" }
    }}
  }'

# No ruleset on the zone yet — create the phase entrypoint with the same rule inside {"rules":[ ... ]}:
#   PUT /zones/$ZONE_ID/rulesets/phases/http_request_dynamic_redirect/entrypoint
```

**Three carve-outs, all learned the hard way:**

- **`/mcp*` and any other JSON-RPC or webhook endpoint.** A 301 on a POST is not reliably followed, and many clients downgrade it to GET. MCP servers registered against the non-canonical host would break.
- **`/api/`** — same reason, for the site's own form endpoints.
- **`*.txt` verification files** — the site-verification files for every search console you are registered with (Google, Bing, and any regional engine), plus the IndexNow key. Verification fetchers do not all follow redirects; a 301 can un-verify a property that was working.

**Order matters if the zone already has path-specific redirects.** Append the host rule *last* so narrower rules (short vanity paths, legacy query-string backlinks) still resolve in one hop instead of two.

**Verify — and wait before you believe a negative result.** Rules take up to ~30s to reach every POP. A deep path answering 200 immediately after the API call is propagation, not a broken carve-out; re-test after half a minute before debugging the expression:

```bash
curl -sI "https://<non-canonical>/some/deep/path/?q=1" | grep -iE '^HTTP|^location'   # expect 301 + path AND query preserved
curl -sI "https://<non-canonical>/mcp"                | grep -iE '^HTTP'              # expect 200 — carve-out holds
curl -sI "https://<canonical>/"                       | grep -iE '^HTTP'              # expect 200 — untouched
```

**Evidence:** a single audit pass across a whole estate of live zones found three sites serving both hosts. Two of them canonicalised to `www` and one to the **apex** — so its rule ran `www` → apex, the opposite direction to the others. That is the whole reason the direction is read off the canonical tag rather than assumed: on any estate of more than a couple of domains, they will not all agree. Always read the canonical tag; never assume `www`.

### 14.5.10 Analytics load timing — the entry pageview is the one you cannot lose

A perf pass will eventually push analytics behind `requestIdleCallback` or a first-interaction listener. **Do that to the marketing tags, never to the product-analytics SDK**, and understand what the deferral costs before you agree to it.

`pointerdown` is the event that *precedes* a click on a link. Defer PostHog behind it and, on a landing page, `import('posthog-js')` races the navigation and usually loses: the **entry pageview is never sent**, and the SDK's first sight of the visitor is page two — whose referrer is the site itself.

The failure has a signature you can query, and it is the only way to tell it apart from an ordinary expired session:

```sql
SELECT count() AS self_referred,
       countIf(first_self_ts = first_any_ts) AS never_seen_before   -- lost entry hit
FROM (
  SELECT person_id,
         minIf(timestamp, properties.$referring_domain IN ('www.example.com','example.com')) AS first_self_ts,
         min(timestamp) AS first_any_ts
  FROM events WHERE event = '$pageview' AND timestamp >= now() - INTERVAL 90 DAY
  GROUP BY person_id HAVING first_self_ts > toDateTime('2000-01-01')
)
```

Measured on a site with the bug: 675 self-referred people, **666 of them (98.7%) with no earlier tracked pageview at all** — roughly a third of all visitors whose real source (Google, LinkedIn, ChatGPT) was discarded and relabelled Referral. The same query on a healthy site in the same estate came back 123 / 18 (15%) — ordinary returning visitors. **The ratio is the diagnosis, not the raw count**: near-100% means lost entry hits, a low share means real returning traffic.

**The split to ship:**

- **PostHog (or whatever owns attribution): eager.** Initialise as soon as the module script runs. Keep `disable_session_recording: true` at init and start the recorder one idle beat later — recorder.js is the heavy part, and deferring *it* costs nothing but replays of sub-3s bounces.
- **gtag / GTM / ad pixels: lazy**, on the existing interaction-or-idle trigger. This is where the measured cost actually was (~13s of throttled main-thread time on a cold load), and none of it carries attribution you cannot rebuild.
- Leave a comment at the call site saying why, or the next perf pass silently undoes it.

**Dev traffic never reaches the production project.** Guard on the *hostname*, not `import.meta.env.DEV` — `astro preview` and `wrangler dev` both serve a production build and would otherwise report:

```js
const LOCAL = /^(localhost|127\.0\.0\.1|0\.0\.0\.0|\[::1\]|.+\.local)$/i.test(location.hostname);
```

Belt-and-braces it at the project level too, so data already collected drops out of every filtered query: analytics project settings → internal/test filters → `$host` `not_regex` `^(localhost|127\.0\.0\.1|\[::1\])(:\d+)?$` plus your platform's preview domains, and default those filters to on. Measured on one live site: `localhost:4321` was the **6th-largest referring domain** — 26 people / 292 pageviews in 90 days, sitting inside every number the weekly reports quoted.

**Launch verification, 20 seconds:** open a page from an external link and click through to a second page *immediately*. Both pageviews must appear, and the first one must carry the real referrer. If only the second shows up, the SDK is still deferred.

### 14.5.11 First-touch attribution must outlive the 7-day ITP window

§14.5.8 solves Safari ITP for the **consent** cookie by rewriting it on every pageload, which
refreshes the 7-day window each visit. Do not reach for the same fix here. It works for consent
because a lapsed answer just re-asks the question — visibly, and the visitor decides again. Applied
to attribution, the identical trick fails silently and destructively.

An attribution cookie written with `document.cookie` and rewritten each pageload does not expire 7
days after the first touch; it expires after **7 days of not visiting**. So the cookie survives
exactly the visitor who was never in doubt — the one browsing this week — and is gone for the one
whose source you actually needed:

> reads a blog post from a Google result → thinks about it for three weeks → comes back and books

That visit writes a **brand-new `first`** pointing at whatever page they landed on, with no source.
The conversion is filed as `direct`. Nothing errors, no gap appears in any dashboard, and the
number that gets quieter is organic search — the channel that did the work. On a considered
purchase (consulting, coaching, B2B, anything with a multi-week decision) that is the majority
case, not an edge case.

**The fix: mirror the first touch into a cookie the SERVER sets.** The 7-day cap applies to cookies
created through `document.cookie`, not to `Set-Cookie` from a first-party origin.

```
POST /api/attr   { first: TouchData }
  → Set-Cookie: <name>_f=…; Max-Age=7776000; Path=/; SameSite=Lax; Secure; HttpOnly
```

Four rules, each of which is a bug if you skip it:

1. **First touch only.** `last` and the click IDs describe the conversion happening right now, so
   the live cookie always has them fresh. Mirroring the whole object doubles the header weight on
   every request for nothing.
2. **Write-once, enforced on the server.** The client cannot read an HttpOnly cookie, so it cannot
   know whether one exists and cannot police itself. The endpoint keeps whatever it already stored
   and returns `{ok:true, kept:true}`. That also makes it idempotent — a retry or a second tab is
   free, so the client can just fire once per session behind a `sessionStorage` flag.
3. **The reader prefers the durable copy.** Merge on read: durable `first` outranks live `first`,
   `last` stays live. A live cookie that lapsed and re-registered is *wrong*, not merely stale, so
   "use whichever exists" is not good enough — the durable one has to win when both are present.
4. **It must be a POST to an uncached path, and this is the one that bites.** A cached response
   carrying `Set-Cookie` hands one visitor's attribution to every later visitor: wrong data for
   everyone and a privacy incident in the same header. Verify BOTH guards before shipping —
   your CDN must not cache POST, *and* the zone cache rule must exclude the API prefix. If a later
   refactor moves this into middleware or a GET on an HTML route, it becomes live on a page with a
   24h edge TTL. Say so in a comment at the call site.

**Consent still gates it.** A rejecting visitor writes no cookie at all, so there is nothing to
mirror and the call never fires.

**Verify on the deployed site, not locally** — a curl chain proves all four properties in one go:

```bash
curl -s -c jar -D - -o /dev/null -X POST https://<host>/api/attr \
  -H 'content-type: application/json' \
  -d '{"first":{"at":"2026-06-01T10:00:00.000Z","url":"/blog/x/","src":"google.com","med":"organic"}}' \
  | grep -iE '^set-cookie|^cache-control'
# expect: HttpOnly, Secure, Max-Age=7776000, and cache-control: no-store

curl -s -b jar -X POST https://<host>/api/attr -H 'content-type: application/json' \
  -d '{"first":{"at":"2026-08-21T13:39:00.000Z","url":"/about/"}}'
# expect: {"ok":true,"kept":true}   <- write-once held; the original survived
```

Regression-test the decay itself, not just the happy path: assert that a live cookie whose `first`
has been overwritten by a later visit still resolves to the original source once the durable cookie
is present. That test is the whole point of the mechanism.

## Stale sitemap submission after a cutover

Search Console keeps crawling the sitemap URL that was **submitted**, not the one `robots.txt`
declares. The two drift apart at every re-platform, and nothing warns you.

Worked example, from a site replatformed off a hosted site builder onto the house stack: GSC still
had `/sitemap.xml` on file — by then a 404 carrying 1 error, last fetched 8 days earlier — while the
live `/sitemap-index.xml` with all 51 URLs had **never been submitted**. Every new page reported
"URL is unknown to Google / No referring sitemaps detected", and it looked like a sitemap-*content*
bug until somebody actually read the submission list.

Unlike Request Indexing, sitemap submit/delete IS scriptable:

```bash
# needs the webmasters (write) scope, and the caller as a Full user on the property
PUT    https://searchconsole.googleapis.com/webmasters/v3/sites/{site}/sitemaps/{feedpath}
DELETE https://searchconsole.googleapis.com/webmasters/v3/sites/{site}/sitemaps/{feedpath}
GET    https://searchconsole.googleapis.com/webmasters/v3/sites/{site}/sitemaps   # audit
```

Add to every cutover checklist: submit the new sitemap, delete the dead one, then re-read the
list. While you are there, audit for duplicates — one site had three overlapping submissions
(`/sitemap-index.xml`, `/sitemap_index.xml`, and a non-canonical apex-host variant carrying a
warning) all listing the same 177 URLs. Keep exactly one: the one the generator emits, on the
canonical host, that `robots.txt` declares.

**Declared sitemap URLs must be on the canonical host.** A second site in the same estate declared
a sitemap on the apex while the apex 301s to `www` — a sitemap line pointing at a redirect. Cross-
check this against §14.5.9 whenever you add a canonical-host redirect rule: the rule and the
sitemap declaration are edited in different places and drift silently.
