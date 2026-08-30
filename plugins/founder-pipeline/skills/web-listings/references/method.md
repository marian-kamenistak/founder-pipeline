# Method — how to submit, by category

`config/targets.json` says *where*. This file says *how*. Do not add target names here — if a target isn't in `targets.json`, it doesn't exist for this skill; add it there first.

## Category playbooks

**entity** (Wikidata, the company databases, LinkedIn, Google Business Profile, Bing Places, Apple Business Connect)
Highest leverage, do first. Wikidata requires notability — do not attempt for a property with no independent press coverage; check what press mentions actually exist first. Person and org entities are separate items — never conflate the founder with the legal entity. GBP: most specific category, service area (not a fake storefront address for remote services), every offer as a Product with a link, 10+ photos, seed Q&A, weekly posts thereafter.

**startup-platform / ai-tools** (Product Hunt, BetaList, AlternativeTo, and the long tail of launch-discovery sites)
Profile/listing existence is this skill's job. Coordinated **launch-day** campaigns (hunter selection, timed comments, the launch playbook) are NOT this skill's job — if a property is doing a launch, pre-stage the profile here and run the campaign separately.

**Register every active property here, not only the marketplace-shaped ones.** A community, a conference, a course product and a personal practice can all be registered as products on the **general** launch-discovery platforms. Two limits on that: it does not extend to category-specific platforms (an AI-tool directory still wants an actual AI tool), and it does not extend to the `review` category — software-review sites are still the wrong shelf for a community or a coaching practice regardless of the "register as a product" framing.

**review / b2b-services** (the B2B software-review sites, the agency-rating platforms, the consumer-review platform)
Only submit where the fit is real — a review site for SaaS products is the wrong target for a 1:1 practice or a community. Check the fit note in the target's `notes` before submitting; don't submit everywhere reflexively. Some require a minimum review count before a public profile activates — flag as `blocked` with reason, not `rejected`.

**vertical** (practitioner directories, fractional-exec platforms, dev-community platforms)
Where most of the real leverage sits for a personal-brand or community property. If you have already measured which of these get cited by AI engines for your queries, prioritise from that measurement rather than from directory size.

**event / talent / media**
Event listings (the conference-data repos, developer-event calendars, CFP platforms) belong to a conference property primarily; also list a community property's recurring meetups where the platform accepts recurring events. Media/PR pitches that need a human angle (journalist pipelines, guest posts) are NOT this skill — hand to `/founder-pipeline:web-backlinks` Family 4 (Digital PR & citations). This skill only handles listing/profile surfaces, not pitched placements.

**institution / catalog** (chambers of commerce, home-market business catalogs)
**The localize-before-register gate applies to every row in this category** — verify the property has live, properly-translated pages in the catalog's language with correct `hreflang` before submitting. If not, mark `blocked`, note what's missing, and stop — do not submit an English-only site to a non-English directory. Catalogs that auto-populate from a company-registration number are a **claim/correct** action, not a submission — check current listing accuracy first, correct only what's wrong. Note also that "auto-populated" is a claim to verify per catalog: some national catalogs that look ID-driven are in fact operator-built, so no stub exists to claim and you create the record from scratch.

## Submission mechanics

The agent submits genuine anonymous forms and never authenticates (`SKILL.md` Law 5). Full browser mechanics live in `references/automation-execution.md`; this is the short version.

1. Check `references/entity-pack.md` for NAP, bio, logo/favicon/og:image, the description at the required length, and the canonical login email for the property.
2. Load the page and find out what the target actually is. Any sign-in, sign-up or SSO gate → OWNER-ONLY; prepare the pack as paste-ready content and stop there.
3. No login required and the form is a one-shot submit → ask in chat for a clear yes on this specific submission, then submit. Log the outcome immediately to `<property>/listings/runs.jsonl` (`submitted`, with the confirmation URL) — the ledger row is the human-facing status, the jsonl is the machine execution history, log both.
4. Never accept a required link-back as a condition — Law 1. If a target's terms require one, mark `rejected`, reason = "requires followed link-back, violates Law 1", and remove it from future runs (don't re-propose).
5. **Hard stop, screenshot, queue OWNER-ONLY** on an account/password field, a payment field, a CAPTCHA, or a phone/SMS/ID verification step — do not attempt to push past these regardless of how close the submission is to done.
6. After any submission, log the ledger row and the jsonl entry. After any `live` confirmation (spot-checked, not assumed), record `listing_url` on the `targets.json` row and update `references/entity-pack.md`'s `sameAs` table.

## Staleness

Any `targets.json` row with `verified_on` older than 90 days gets re-verified (one fetch, confirm still live and submission mechanics unchanged) before it's used in a new run — don't submit against a stale URL. Pay particular attention to `cost` and `login_required`: those are the two fields that change under you, and a stale "free, no login" is what sends a run into a hard stop.
