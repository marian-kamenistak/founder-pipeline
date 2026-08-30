# Phase 6 — Launch: final gate, deploy, indexing

Reference: [`references/launch.md`](../references/launch.md). Full publish gate: [`references/gates.md`](../references/gates.md) → Appendix F.

Runs after GATES 1–5 all pass. Analytics is **wired** in Phase 5's Z2 lane (same `<head>` files as titles/JSON-LD — one pass, not two); this phase **verifies** it fired. Ends with handoff to post-launch growth (GATE 6).

## 6.1 Final publish gate (all blockers)

Reads the same **BARRIER 2** staging-verification wave `5-seo.md` runs for GATE 5 — one deploy candidate, one check pass, two gates evaluated against their own subset. Don't redeploy staging a second time for these.

- [ ] Lighthouse 95/100/100/100 mobile · axe 0 violations · securityheaders + ssllabs + Mozilla Observatory A+
- [ ] Forms re-tested end-to-end in the deploy candidate: POST 200 AND the email arrives
- [ ] `/founder-pipeline:brand-voice` final pass on every public string — this already happened at BARRIER 1 in Phase 5; confirm it, don't redo it
- [ ] Every P0 from all design-review rounds fixed and verified — publish is blocked until then

## 6.2 Analytics verification (wiring already done in Phase 5 Z2)

- [ ] Product-analytics events firing in staging: `page_view`, `cta_click`, `form_submit`, `pricing_tier_clicked`, `blog_post_read`, `outbound_click`; 4 dashboards (acquisition / funnel / content / money-page) + north-star pinned + drop alert
- [ ] GTM/GA4 via Google Tag confirmed wired to Consent Mode v2 (granted-by-default per §14.5.8, `region` + `wait_for_update` deleted, `security_storage` granted in both payloads), key events marked, routed through Partytown/lazy — off the LCP path
- [ ] **Consent bar verified live, not just present** (`references/launch.md` §14.5.8). The four checks that catch the silent failures: (1) after Reject, **every** analytics cookie is gone including the `.registrable-domain` one — a host-only delete passes every other check and fails this; (2) pageview requests **still fire** after Reject and the distinct-id differs across reloads — if capture stopped, someone reached for the SDK's opt-out call without also enabling its cookieless mode; (3) no session-recorder request and zero autocapture events after Reject; (4) the GA hit carries `gcs=G100`. Plus: Lighthouse CLS identical with and without the bar, and no Layout Shift record naming `#consent-bar` or `body`
- [ ] CDN-level web analytics on — on the default stack this is a one-click dashboard setting with zero code, since the domain is already proxied; a manual beacon embed is only needed for a DNS-only (unproxied) domain
- [ ] **Zone hardening (one-time per domain, do it at launch, not later):** `always_use_https = on` · `min_tls_version = 1.2` · `early_hints = on` (free LCP win — preloads critical assets while the origin computes the response) · HSTS (`strict_transport_security`: `enabled: true`, `max_age: 15552000` i.e. 6 months, `include_subdomains: true`, `preload: false` — never enable `preload` without the owner's explicit sign-off, it's a hard-to-reverse browser-list submission) + `nosniff: true`. Recipe + curl verification: `references/launch.md` § "Zone hardening". Found all four missing on a live-zone audit of an already-shipped site running a free CDN plan — don't assume your CDN defaults to secure
- [ ] **Cloudflare WebMCP (Beta) enabled:** dashboard → zone → **Agent Readiness → WebMCP** → enable main toggle + both tool packs (Content Credentials/C2PA, Site MCP server). Dashboard-only, no API yet — do it by hand, same launch pass as zone hardening above. Recipe: `references/launch.md` § 14.5.6
- [ ] **Cloudflare Crawler Hints enabled:** dashboard → zone → **Caching → Configuration → Crawler Hints** → enable. Dashboard-only, no API — same launch pass as the two toggles above. Recipe: `references/launch.md` § 14.5.7
- [ ] **CRM connected:** the form route upserts a contact record carrying `utm_*` + `referrer` + `landing_page` + the session-replay URL, authenticating with the CRM's API token read from your environment — never hardcoded, never committed. Test submit→record end to end. Also capture and persist the ad-click identifiers (`gclid`, `li_fat_id`, `fbclid`) so offline conversions can be fed back to the ad platforms later
- [ ] **Entry pageview survives a fast click** (`references/launch.md` § 14.5.10). Land on a page from an external link and click through immediately: BOTH pageviews must appear and the first must carry the real referrer. Product analytics loads **eagerly**; only gtag/GTM/ad pixels stay on the idle-or-interaction trigger. On one real site, deferring the SDK cost ~34% of its visitors' true source for months, and the only symptom was the site appearing as its own top referring domain
- [ ] **First touch survives 7 days of absence** (`references/launch.md` § 14.5.11). If the build writes an attribution cookie with `document.cookie`, Safari expires it after a week away — so the visitor who reads a post, waits three weeks and then converts is filed as `direct`, and organic search quietly loses the credit it earned. Mirror `first` into a server-set `HttpOnly` cookie via `POST /api/attr`, write-once on the server, durable copy wins on read. **That endpoint must stay a POST on a path the zone cache rule excludes** — a cached `Set-Cookie` hands one visitor's attribution to everyone. Verify with the two-curl chain in §14.5.11: expect `HttpOnly … Max-Age=7776000` on the first, `{"ok":true,"kept":true}` on the second
- [ ] **No analytics on local hostnames**, guarded on `location.hostname` (not `import.meta.env.DEV` — `astro preview` and `wrangler dev` serve production builds), plus host exclusions in the analytics project's internal/test filters, with those filters defaulted ON for the whole team
- [ ] KPIs wired to the north-star metric; vanity filter: "if this goes up but revenue doesn't, do I care?"

## 6.3 Deploy — BARRIER 3

- [ ] `pnpm build && wrangler deploy`; custom domain via Workers route. **Always rebuild after editing `wrangler.jsonc` — deploy without build ignores route changes**
- [ ] **[P] after deploy** — production reachability curl set: `robots.txt`, `llms.txt`, `llms-full.txt`, sitemap, `/rss.xml`, `/.well-known/nlweb.json`, IndexNow `<key>.txt`
- [ ] **[P] after deploy** — crawler-delivery matrix (`5-seo.md` §5.3), run again against **production**, not just staging. This catches a different failure class than the staging run: staging catches app-level 404s, production catches **edge-level** failures — WAF rules, bot-fight mode, rate limits — that don't exist on staging and are invisible locally. This is exactly the class of bug behind the site in §5.3 that was serving errors to 54% of AI-crawler requests while every local and staging check looked clean
- [ ] **[P] after deploy** — product analytics + CDN analytics verified in production
- [ ] **[S] after the above** — zone cache `purge_everything` (confirmed necessary on every zone tested; a URL-scoped purge does not reliably clear edge-cached HTML or `robots.txt`)

## 6.3a Canonical host — BLOCKER, and re-check it on every existing zone

- [ ] **Exactly one host serves the site; every other host 301s to it, preserving path and query.** Apex or `www` is a free choice — serving both is not. Recipe, carve-outs and the propagation gotcha: `references/launch.md` § 14.5.9

Do not skip this because the site "looks fine on both". That is the symptom, not the absence of the bug: both hosts render, the canonical tag is usually right, nothing 404s, and meanwhile cookies split per host so the same person counts twice and arrives **self-referred** — the site showing up as its own top referring domain. It is invisible until somebody reads a referrer table.

- [ ] Read the canonical host off the page (`curl -s https://<domain>/ | grep -o '<link rel="canonical"[^>]*>'`) — **never assume `www`.** Of three zones found broken in one sweep, one was canonical on the **apex**, so its redirect ran the other way
- [ ] Fix with a zone **Redirect Rule**, not `_redirects` (assets layer — skipped by Worker-first routes and edge cache) and not app code
- [ ] Carve out `/mcp*`, `/api/`, and `*.txt` verification files — a 301 on POST is not reliably followed, and verification fetchers do not all follow redirects
- [ ] Verify path AND query survive the redirect, the carve-outs still return 200, and the canonical host is untouched. **Wait ~30s before believing a negative** — rules take that long to reach every POP, and a deep path still answering 200 straight after the API call is propagation, not a broken expression
- [ ] **[S] once per account, not per launch** — run the all-zones audit in § 14.5.9 across every domain, not only the one being launched. One such sweep found this live on 3 of 23 zones in a single account, all launched months apart, none of them caught by any existing check

## 6.4 Indexing — BARRIER 4, gated on 6.3's production crawler-delivery matrix returning all-200

Applies to EVERY deploy of a new/materially-changed page, not launch-only. Owned by **`/founder-pipeline:web-indexation`** — invoke it here for launch, and again after every future deploy that adds or changes a page (don't re-derive the mechanism in this file).

**Hard gate: never enqueue a URL that didn't return 200 in 6.3's production crawler-delivery matrix.** `/founder-pipeline:web-indexation` already refuses to ping noindex/404/redirect URLs — this closes the gap where a URL looks fine in a human browser but errors for every bot, which is invisible unless the matrix actually ran.

- [ ] **Bing Webmaster Tools verified + sitemap manually submitted + AI Performance report checked** — treat this as a named blocker, not an optional nicety. **87% of SearchGPT/Copilot citations match Bing's top organic results** [Seer Interactive]; a natural experiment where a site was algorithmically deindexed by Bing lost 90K+ AI citations while its Google rankings were untouched [Gabe, Jun 2026] — Bing is the index ChatGPT/Copilot actually draw from, not Google. Bing's AI Performance report (citation-share metric added Jun 2026) is the only first-party AI-citation data available anywhere in this stack
- [ ] `/founder-pipeline:web-indexation` one-time per-property setup done: IndexNow key generated + live at root, GSC property verified + sitemap submitted + robots.txt re-fetched
- [ ] **Re-platform or domain cutover? Re-point the GSC sitemap submission and DELETE the old one.** `robots.txt` naming the new sitemap does not update Search Console — it keeps fetching whatever was submitted, even after that URL starts 404ing (recipe in `references/launch.md` → Stale sitemap submission)
- [ ] `/founder-pipeline:web-indexation` every-deploy steps run for this launch: IndexNow pinged (this is a Bing/Yandex protocol, and is also how several regional engines take submissions — **Google does not support it**; its value here is specifically the Bing→ChatGPT/Copilot pipeline above), homepage + `/llms.txt` + `/llms-full.txt` (+ locale mirrors) appended to the reindex queue

- [ ] **Add the new domain to your recurring health monitor.** A launched site decays silently:
  page speed, backlink authority and AI-crawler access all drift with nobody watching. Whatever
  monitor you run, add a row for this domain carrying its URL, label, CDN zone, analytics project,
  a few deep paths, the repo, and **thresholds seeded from THIS launch's real numbers**. Floors
  must come from the launch measurements, never a flat 90 — a site-builder-era site and a
  statically-generated one do not share a bar. Keep the per-metric fix guidance next to the
  monitor's config so an alert arrives with its remedy attached. If you run no monitor yet, the
  minimum viable version is a fortnightly scheduled job that records Lighthouse mobile, the
  crawler-delivery matrix from §5.3, and the sitemap-wide scripts from 6.5.

## GATE 6 → done

All 6.1–6.4 checked. **Hand off to post-launch growth**, which this skill does not own: `/founder-pipeline:web-backlinks` (link acquisition), `/founder-pipeline:blog-launch` (publishing cadence), `/founder-pipeline:lead-magnets` (capture assets), and `/founder-pipeline:web-listings` (register-once directory/registry/catalog presence — Product Hunt, Crunchbase, Wikidata, plus the business catalogs that matter in your home market). The remaining activation work has no skill in this plugin — run it from your own plan: a local business profile if the site targets a place, an MCP server if the product has an API, AI-visibility probes on a fixed cadence, and a 90-day loop reviewing all of it. Record launch date + week-0 state in `PLAYBOOK-CASE-NOTES.md`.

## 6.5 Schedule the re-audit

Everything above runs once. Sites rot afterwards, and the rot is invisible because nothing errors
and nothing builds red: dead schema types keep being maintained, titles drift out of the 30-60
band as pages get edited, and a new page ships without the locale mirror its switcher assumes.

Put `references/seo.md` § "Live-site health re-audit" on a monthly sweep from launch day, and run
it after any deploy that adds pages. It is three scripts against the production sitemap and the
output is the worklist. The reason this step exists at all: an audit found a live site failing
three rules that were already written in this skill — the knowledge was never the gap, the re-run
was.
