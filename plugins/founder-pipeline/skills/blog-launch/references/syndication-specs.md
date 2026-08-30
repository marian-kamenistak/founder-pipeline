# Syndication specs — Medium, Substack, Hackernoon

Purpose: distribution + high-DA backlinks, never SEO cannibalization. The original on your own domain is always canonical. Standing rule: if a platform's publication process strips or overrides the canonical tag, switch it back to your domain once the submission is accepted.

## Common export rules (all three files)

- All internal links rewritten to absolute `https://<your-domain>/...` URLs.
- Footer attribution: one line — "Originally published at [\<your-domain>](<post URL>)." followed by a single credential sentence naming what you do and one verifiable number. Pull that number from your verified data-points store and **re-check it before every use** — a syndicated copy cannot be quietly corrected later the way a post on your own site can.
- Images: list local file paths (from the repo gallery) at the top of the export for manual/automated upload; captions preserved.
- Strip site-specific MDX (imports, components) → plain Markdown.
- Title may vary ±20% per platform norms; the claim stays identical.
- Export header block (not pasted): `platform, canonical: {{CANONICAL}}, tags, publish_mode: draft`.

## Medium (`exports/medium.md`)

- **Canonical:** best path is the import tool — `medium.com/p/import` with the live URL sets `rel=canonical` automatically. Fallback: new story → paste → Story settings → Advanced → canonical URL.
- Tags (5 max): keep a standing set of your four or five evergreen topic tags in the site profile and swap ≤2 for post-specific ones each time.
- Consider a publication submission (The Startup, Entrepreneur's Handbook, or whichever publication owns your topic) AFTER the post proves itself on your own domain.
- Best publish windows: Tue or Sat mornings [operating assumption — worth re-testing against your own analytics].
- Mode: create as **draft**; the owner pushes publish.

## Hackernoon (`exports/hackernoon.md`)

- Editor has an explicit canonical field ("Originally published at") — fill it.
- Goes through human editorial review; expect days of delay. Draft only.
- High DA; this one matters most for backlinks.

## Substack (`exports/substack.md`)

- **No canonical support.** Mitigations, both mandatory:
  1. Publish **7-14 days after** the original (Google has indexed the canonical by then). Create the draft now with a scheduled date; never same-day.
  2. First line of the body: "*Originally published at [\<your-domain>](<post URL>).*"
- Substack doubles as the newsletter send — sending emails to subscribers is a bigger action than a web draft: **never send without the owner's explicit word**; scheduled draft is the ceiling of autonomy.

## Automation notes (step 09 phase 2)

Browser automation running in the owner's own logged-in session. Per platform: 2 attempts max, then hand the export file to the owner with the exact click-path for the canonical setting. Screenshot every created draft. Drafts only, publishes are the owner's.
