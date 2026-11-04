# Content: format + copy sources

**Stream:** [slug]
**Step:** P4.S2-Copy (P4-Build)
**Last updated:** [date]

---

## Hard rule

Format **follows** GTM. Don't pick format from creative preference — derive it from how the ICP buys.

| GTM motion | Natural primary asset |
|---|---|
| 1:1 demos to named accounts | Sales deck |
| Founder-led LinkedIn → landing | Deck + landing page |
| PLG signup → in-product education | App MVP + onboarding |
| Partner-led referral | Partner one-pager + sell sheet |
| Community-led | Community space + first asset |

## Primary asset

**Type:** [deck / web / app / hybrid]

### If deck
- Deck type from your configured brand kit: [VC / partnership / coaching / workshop / media / talent / role]
- Hero hook (one-line): [...]
- Section list: [hero / problem / solution / proof / pricing / CTA / footer]
- CTA: [what action]
- Personalization: [recipient name in URL? per-deck customization?]
- Tracking: page view + click autocapture + session replay in your analytics tool

### If web
- Page list: [/landing / /pricing / /about / /faq / /apply]
- Hero copy: [...]
- CTA flow: [primary CTA → form → confirmation → next step]
- Conversion goal: [signup / form fill / payment]
- Tech stack: [your declared house stack (P1.S1). Builds outside it need a recorded override + reason]
- Tracking: analytics events for each CTA + funnel steps

### If app
- MVP feature list (3–5 max):
  1. [...]
  2. [...]
  3. [...]
- First-user journey: [signup → first value moment → retention hook]
- Retention hook: [what brings them back day 2]
- Tech stack: [your declared house stack (P1.S1), or a recorded override + reason]
- Tracking: product analytics from day 1

## Secondary asset (if needed)

[What's the next asset that has to exist for the GTM motion to work?]

- Type: [...]
- Spec: [...]
- Sequencing: [primary first, then secondary by date X]

## Distribution mechanic

- How does the asset get into the ICP's hands? [...]
- Gating: [none / email gate / referral / paid]
- Follow-up sequence: [post-consumption nurture]

## Dependencies

- Brand assets: [logo, photos, CDN hosting]
- Tech stack: [confirmed or to-decide]
- Tracking: [analytics setup. If you use PostHog, its own plugin ships `/posthog:instrument-integration` — an optional dependency you install separately]
- Skills to invoke: `/frontend-design:frontend-design` for distinctive UI (optional dependency — the `frontend-design` plugin, installed separately). After the deck deploys, run a deck health check inline: every link clicks through to a 200, prices and claims match the live site, no placeholder text, the PDF opens under 5 MB, and slide count matches the build log.

---

## Honest-assessment note

This stage earns its keep always. Format is a derived decision — get it right or waste the GTM motion.

## Checkpoint

- [ ] First asset spec locked: [X]
- [ ] Second asset spec locked (if needed): [Y]
- [ ] Web build (P4.S3) next

---

# Copy sources section (single source of truth for words — precondition for the P4.S3 web build)
## Keyword map

| Keyword | Type (primary/secondary/AI-search phrasing) | Source |
|---|---|---|
| | | `[source: ...]` or `[assumption — validation: Search Console after launch]` |

## Meta block

- Page title: [...]
- Meta description: [...]
- OG title / description: [...]
- URL path: [...]

## Page copy (section by section, every field via `/brand-voice`)

### Hero
[...]

### Problem / outcome
[...]

### How it works
[...]

### Differentiators
[...]

### Proof
[...]

### CTA flow
[...]

### Deliberately NOT said
[e.g. no public pricing — and why]

## Language versions

- EN draft (approved first): [above / link]
- Market-language version: [...] — translate only after the EN draft is approved, and work from `TRANSLATION-GLOSSARY.md` (P4.S1) so every locked keyword survives verbatim. A native speaker or a translation pass reviews it before it ships; a literal translation of a headline is a draft, not a headline.

## Build notes

- Brand kit slug: [...]
- Target path/domain: [...]
- CTA destinations: [...]
- Placeholders + owners: [...]

---

## Validation loop

- [ ] `/critical` run — findings: [...] — **CRITICAL SCORE: [X]/10** — advisory; the gate is the def-of-success PASS/FAIL checklist
- [ ] Def-of-success (from the stage file): [each criterion — met/unmet]
- [ ] Improvement loops run (if gate failed): [N — what changed each round]
- [ ] Revised — what changed: [...]
- [ ] **Owner approved** — [date] [overrides, if any]
