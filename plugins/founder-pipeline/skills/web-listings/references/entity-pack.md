# Entity pack — canonical NAP + identity values for listings

**This file ships as a template. Every value below is a placeholder or a fictional worked example — replace them with your own before the first run.** `scripts/nap_audit.py` parses this file as the single canonical source for Law 6, so keep the heading and field shapes intact when you fill it in.

Every profile listing that asks for name/address/description/logo pulls from here, never from memory and never from a specific site's copy. That is what keeps `sameAs` consistent across Google Business Profile, the company databases, Wikidata and LinkedIn.

**Numbers rule:** any figure (member count, attendee count, years active, session count) used in listing copy comes from your single numbers source of truth at submission time — never hardcoded here, never carried over from a stale site page. Published site figures go stale silently; check the source, not the live page.

## How the parser reads this file

`nap_audit.py` walks `##` and `###` headings and collects, from each block, bullets whose label is
one of **legal name / name / org name**, **registered address / address**, **phone / telephone**, or
**website / official website / url**, written as `- <label>: <value>` — or the same labels as
`| Field | Value |` table rows. It trims an em-dash aside from both the
heading and the value, and treats `not defined`, `unknown`, `unconfirmed`, `n/a`, `tbd`, `none`
and `-` as absent rather than as values to diff against. Run
`/founder-pipeline:web-listings nap-audit --list` after filling this in — it prints which fields
are defined and which are not, so Law 6 never looks more enforced than it is.

---

## Org identity — one block per legal entity, do not conflate them

Larger portfolios routinely run several legal entities. **List each one separately and record which
properties it operates.** Conflating two entities on a listing is the single most common NAP defect,
and it is very hard to unwind once a registry has indexed the wrong pairing.

### Example Collective s.r.o. — canonical entity for the community and conference properties

- Legal name: Example Collective s.r.o.
- Registration number: EXAMPLE-00000000 · VAT: EXAMPLE-VAT-0000
- Registered address: Ulice 1, 110 00 Praha 1, Czech Republic
- Founded: 2024-01-01
- Legal form: private limited company
- Registry status: active
- Website: https://community.example.com
- Phone: not defined — see the NAP completeness note below

### Example Ventures s.r.o. — canonical entity for the personal-brand property

- Legal name: Example Ventures s.r.o.
- Registration number: EXAMPLE-11111111
- Registered address: Ulice 1, 110 00 Praha 1, Czech Republic
- Founded: 2023-01-01
- Website: https://coach.example.com
- Phone: +420 000 000 000
- Note: shares a registered seat with Example Collective s.r.o. Two registered seats at one address
  is normal and lawful; it matters only for Google Business Profile, where **multiple profiles at one
  address is a suspension trigger**. Only one of your entities gets a GBP at a shared address.

**NAP completeness.** Law 6 claims name, address, phone and website are identical everywhere — but a
field the canonical source never defines cannot be checked at all. Record the fields you have, record
the ones you don't as `not defined`, and use `nap-audit --list` to see the real state rather than
assuming the law is fully enforced.

**Founding-date conflicts — pick per entity, hold consistent.** Different entities in a portfolio
have different incorporation dates, and a practice's "operating since" year is a *different claim*
from an incorporation date. Never mix these on one listing — match the date to the specific entity or
claim the field is asking about.

### Google Business Profile eligibility — check before proposing it

GBP is the highest-value local target and the one that can get a business suspended. Google requires
either a physical location customers can visit, or a business that travels to customers. Answer all
three before submitting, and record the answers here:

1. Real, recurring in-person or travel-to-customer service? A practice delivered entirely over video
   meets neither limb and is **ineligible**. A practice that runs in-person sessions on a real cadence
   satisfies the travel-to-customer limb — the rule is about the fact pattern, so establish the fact
   before you close the question either way.
2. A genuine business address, not a P.O. box, virtual office or hot desk?
3. Storefront (public address) or service-area business (address hidden)? A genuinely staffed and
   visitable office qualifies for the storefront model; otherwise it is an SAB and the address is
   hidden. This choice changes the expected verification path — postcard or phone for a storefront,
   usually video for an SAB — so decide it before starting, not halfway through.

Record which Google account owns the profile. Creating it under the wrong account is expensive:
GBP ownership transfer after the fact is manual and slow.

Record the profile name and note the risk if it isn't the legal name. Google's name field must match
how the business is represented offline, and it suspends profiles for keyword-stuffed names. A brand
name matching your domain is usually defensible; have a fallback to the legal or personal name ready.

Bing Places requires a verifiable address. BBB and Yelp are US/Canada only.

## Scope and canonical email per property

Every submission uses one login email per property; there is no per-target routing beyond this table.
Fill it from your own registry — the rows below are the shape, not real addresses.

| Property | Web | Login email |
|---|---|---|
| Community (example) | https://community.example.com | listings@example.com |
| Conference (example) | https://conference.example.com | listings@example.com |
| Personal brand (example) | https://coach.example.com | hello@coach.example.com |
| Marketplace (example) | https://marketplace.example.com | listings@example.com |

Record which legal entity operates each property directly under this table. A property that is a
product of another entity, not an entity itself, still needs that mapping recorded.

## Cross-promotion links

**Any submission form with more than one URL/website/social field should carry links to the other
properties too, not just the one that triggered the submission.** Use this table for those secondary
link fields — pick whichever subset genuinely fits the form's field count and the target's own fit,
don't force every property into a two-link form.

| Property | URL | Fit note |
|---|---|---|
| Community | https://community.example.com | Pairs naturally with any speaker/mentor/founder listing |
| Conference | https://conference.example.com | Pairs with speaker-bureau and event listings |
| Personal brand | https://coach.example.com | Usually the anchor link |
| Personal brand — speaker page | https://coach.example.com/speaker/ | Use instead of the root on speaker-bureau listings |
| Marketplace | https://marketplace.example.com | Product listing |
| LinkedIn (personal) | https://www.linkedin.com/in/example/ | Person entity |
| LinkedIn (company page) | https://www.linkedin.com/company/example/ | Org entity |

## Visual assets

**Use each site's own favicon, apple-touch-icon and `og:image`, fetched live at submission time — no
new design work, no logo commissioning.** A property without a dedicated wordmark does not need one;
its own icon assets are the source. Record the fetched URLs per property in a table like this:

| Property | Favicon / square icon | og:image (wide/banner) |
|---|---|---|
| Community | `https://community.example.com/apple-touch-icon.png` (180×180) | `https://community.example.com/og-default.png` |
| Personal brand | `https://coach.example.com/favicon-192x192.webp` (192×192) | `https://coach.example.com/og-default.jpg` |

**Gotcha:** some directories enforce a **min 400×400** square logo, and 180–192px icons are below
that floor. Keep a production headshot/wordmark set in your brand kit as the fallback, and don't
treat a target as owner-only for asset reasons before you've checked the brand kit.

## Per-property description lengths

Most listing forms cap description length differently. Draft once per property at each tier, run
through `/founder-pipeline:brand-voice` (external-facing copy), then reuse across targets requiring
the same length. Directory-listing register note: most fields (company-database descriptions,
Wikidata label/description, a GBP category blurb) expect a factual "what it is" descriptor, not a
persuasive pitch — keep these numbers-first and factual rather than applying full outcome-over-output
marketing framing.

Draft four tiers per property. This is the shape, with fictional copy:

**Community property (example)**

| Tier | Copy |
|---|---|
| One-liner (≤60) | The region's engineering leadership community. 3,000+ members. |
| Short (≤160) | A peer network of 3,000+ engineering leaders across four cities. 12 meetups a year, 120+ people in the room each time. |
| Medium (≤300) | A peer network connecting 3,000+ engineering leaders across four cities. 12 meetups a year, 120+ people in the room each time, 40+ meetups delivered, 80+ speakers on stage so far. Built for VPEs, CTOs and staff+ engineers who want peers, not a webinar. |
| Long (≤1000) | A peer network for engineering leaders — VPEs, CTOs, staff and principal engineers who want people who have actually run the fire drill, not another framework deck. 3,000+ members across four cities. 12 meetups a year, 120+ people in the room each time, 40+ meetups delivered, 80+ speakers on stage so far. 5 active peer circles for smaller, recurring conversations between meetups. |

Repeat per property, and add a **speaker positioning** set for the personal-brand property if you
pursue the `speaker` category — speaker-bureau copy is a distinct register from mentoring or
consulting copy and should not be reused across the two.

**Home-market language tiers.** Where a target serves a language other than your primary, draft the
tiers in that language too — compiled by a strong model with a native-quality translation pass, never
machine-translated at submission time. Those tiers stay **blocked** until the localize gate below is
satisfied for that property.

## Localize gate status (Law 4)

Re-probe before any submission to a non-primary-language target; this is the gate, not a formality.
Maintain a table like this, dated:

| Property | EN | {lang 2} | {lang 3} | Verdict |
|---|---|---|---|---|
| Community | ✅ | ✅ `/xx/` 200, hreflang correct | ❌ 404 | lang 2 open, lang 3 blocked |
| Conference | ✅ | ❌ `/xx/` 404, no hreflang | ❌ | BLOCKED |

**Important distinction: Law 4 is your own quality policy, not a platform eligibility requirement.**
In practice, nearly every directory hosts the listing copy on *its own* domain — you type a title and
description into their form, and the destination-URL field accepts any URL with no language
validation. Very few targets require a localized landing page as a condition of listing. So a missing
`/xx/` page costs **conversion quality** (the listing reads as foreign to a local audience), not
eligibility.

Read Law 4 accordingly: it is a deliberate standard about not sending local traffic to a page it
can't read, and it should still gate submissions by default. But when a target is high-value and the
copy lives on their domain anyway, an explicit owner override is a reasonable call rather than a rule
violation. What genuinely blocks, in several markets, is a **local company-registration-number gate**
on the generic business-catalog tier — and that tier is low-value anyway.

## Derived data points (computed, re-derive at use time)

Some fields want a derived figure rather than a stored one — "years of experience" from a start year,
for example. Record the derivation, not the answer, and re-derive from the current date at submission
time so it doesn't silently go stale:

- **Years operating**: derived from the start year in your numbers source against the current year.
  Never hardcode the computed number here.

## sameAs canonical set (must resolve identically everywhere)

Once populated, this list becomes the JSON-LD `sameAs` array on each property's site AND the
cross-check list for Phase 1 Audit. **Maintain per-property, not globally** — an org item for one
legal entity is not the same entity as a person item for its founder.

| Property | Wikidata | Company database | LinkedIn | GBP |
|---|---|---|---|---|
| Community | | | | |
| Conference | | | | |
| Personal brand | | | | |

Fill in as each listing goes live; this table is the audit source for Phase 1 on every subsequent run.

**Record status honestly, in three buckets.** The distinction matters more than it looks:

- **ABSENT** — control-tested. You checked a slug you know exists on that platform and got a 200, and
  your own slugs 404. Only then is "absent" a finding.
- **UNCERTAIN — do not record as absent.** A platform that 403s non-browser clients, renders search
  results in JS with no server-side endpoint, or hides profiles behind a login reads as "missing" to a
  plain fetch and is not evidence of anything.
- **DEAD — purge, do not re-propose.** A platform that has shut down should be removed from the
  catalog *and* from bios, decks and one-pagers, which is where a dead affiliation lingers longest.

### Wikidata: an item with zero references is close to worthless

When you audit an existing item, inventory its statements and count references per claim. **Zero
references is the single highest-leverage thing to fix** — an unreferenced item reliably stays out of
Google's Knowledge Graph and is low-trust for LLM grounding. Every claim needs a `P854` reference URL
pointing at the entity's own site for definitional facts (org type, headquarters, founder) and at the
authoritative government registry for legal facts (country, incorporation date).

Two other things worth checking on an existing item: whether the **occupation/instance-of statement
actually matches the positioning** (a wrong statement is worse than a missing one, because it is
confidently wrong), and whether the item cites the **right legal entity** — an org item built against
the wrong registration number and founding date has to be corrected, not extended.

**A common structural leak worth naming:** an old domain still live and ranking alongside the current
one with overlapping positioning splits the same entity across two domains, and undercuts every
listing built on top of it. Redirect or retire it before investing in entity work.

---

*Template version 1.0 — ships unfilled. Replace every placeholder before the first run.*
