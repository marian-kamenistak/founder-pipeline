# P4.S2 — Content: format + copy sources → `P4-Build.S2-Copy.md`

**Phase: P4-Build**

**Routing:** plain (never fan out copywriting) · format spec MID, psychology pass HIGH, hero/tagline/opener and translation PEAK · gate critic at the step tier

**Earns its keep** always — but format is a derived decision, not a creative one.

**Build rule — there is no pre-sale gate on this step.** Content and web build in every run, including overnight, without waiting for pre-sale evidence. What the removed gate leaves behind, and what still binds: the sell-first RUN ORDER (P3.S1 outreach opened before this step), and honesty about evidence tier — copy claims stay tagged to their evidence level; no fabricated proof (case studies, testimonials, client names) may ever enter the copy to fill the gap that pre-sale evidence would have filled. Record at the top of `P4-Build.S2-Copy.md`: `BUILD RULE: no pre-sale gate — build proceeds; proof elements limited to what actually exists.`

**Hard rule — format follows the live motion.** The only observed channel at this point is P3.S1's outreach (GTM locks the broader channel set later, at P6.S1, from real reply + activation data) — the format derives from that motion mechanically: "warm-intro 1:1 demos to named accounts" → sales deck; "founder-led LinkedIn → landing page" → deck + landing page; "PLG signup → in-product education" → the app itself + onboarding tour. If the format you want doesn't follow from the live motion, the pull is aesthetic, not strategic — name it.

**Ask one at a time:**
1. Restate the live outreach motion from `P3-Clients.S1-Outreach.md` and derive the natural first asset from it in one sentence.
2. Confirm the first asset type (deck / landing page / site / app / hybrid) and what it must accomplish in the funnel.
3. Spec for that first asset:
   - If deck → routes to P4.S5 (HTML→PDF via system Chrome); spec the hero hook + sections here, the build is P4.S5's
   - If web → page list, hero copy direction, CTA flow, which brand kit (build itself happens in P4.S3)
   - If app → MVP feature list, first-user journey
4. Second asset (if needed) — what's the next thing that has to exist?
5. Distribution mechanic — how does the asset get into the ICP's hands?

## Copy sources section (hard rule for any web asset)

Before firing ANY web build pipeline, fill the **Copy sources** section of `P4-Build.S2-Copy.md`. No web build starts until it exists and the owner has approved it. The P4.S3 build then treats it as the single source of truth for words — builders lay out and style, they do not write copy.

The Copy sources section must contain:
1. **Keyword implementation** — pull primary/secondary keywords and AI-search phrasings from the approved `P4-Build.S1-Keywords.md` (the keyword contract) and note per copy section which keyword it serves. **No new keywords are invented here** — if copywriting surfaces a better term, it goes back into `P4-Build.S1-Keywords.md` first (with the owner's re-approval), then into the copy.
2. **Meta block** — page title, meta description, OG title/description, URL path. The meta/SEO spec is OWNED here; P4.S3 implements it, never invents it.
3. **Full page copy, section by section** — hero, problem/outcome, how it works, differentiators, proof, CTA flow. Every field written via `/brand-voice` (mandatory). Include what the page deliberately does NOT say (e.g. no public pricing).
   - **`/marketing-psychology` pass per page (mandatory).** After the draft, run every page through it: proof placement, objection handling, loss aversion, CTA framing, friction points. Apply the findings, then de-AI the result via `/brand-voice` — persuasion principles applied, AI-smooth phrasing removed. Record which principles each page uses in its copy file.
   - **Lead magnet (mandate lives HERE).** If any page converts through email capture, run `/lead-magnets` here for the magnet spec + copy; P4.S3 builds it, P5.S1 distributes it. Its landing section + delivery asset copy are part of this contract, not an afterthought.
4. **Build notes** — brand kit slug, target path/domain, CTA destinations, placeholders for missing assets (photos, tool links) with named owners.

**Language rule:** draft the copy in **English first, even when the home market is not English** — the model works with fuller context in EN and the copy review is sharper. Once the EN version is approved, produce the market-language version and ship *that* as the customer-facing page. The translation is voice-preserving and is bound to the locked terms in `TRANSLATION-GLOSSARY.md` from P4.S1 — a translator (human or model) that "improves" a locked keyword has broken the keyword contract and the page goes back. No translation skill ships in this plugin; if you have one, hand it the glossary as a hard constraint, otherwise brief the translator with it explicitly. Record both versions in the file.

**Style rule (hard — no generic copy).** Every topic line, module name, benefit, and outcome must be at least ONE of:
- **Situational** — names the real scene the reader is in ("the 1:1 where your best engineer says they're bored").
- **Data-driven** — carries a real number or metric ("code review latency doubled after the team hit 9 people").
- **Outcome-based** — states what measurably changes for the reader ("you leave with your Q3 roadmap risk-scored").

Generic category words and topics ("communication skills", "team motivation", "AI use cases", "leadership fundamentals", "best practices") are an automatic FAIL and get rewritten into a situation, a number, or an outcome. Applies to every product/service/offering page.

**No-competition gate (hard — one adversarial score per product/service/offering page).** After the copy passes `/brand-voice` + `/marketing-psychology`, run an adversarial scorer on each page against the competitor research (`P1-Ideation.S5-Competition/` + any P4.S1 research files): *"Could any competitor in the research credibly offer this same thing within a quarter?"* Score 0–10 (10 = structurally impossible to copy given the stream's unique assets; 8 = differentiated on multiple hard-to-copy axes; 5 = better-written sameness; 2 = generic). Anything **under 8 gets revised and re-scored, up to two rounds.** A page still under 8 after two rounds is **FLAGGED to the owner for a judgment call, never silently shipped.** Record each page's final score + its single strongest differentiator in the page copy file. In fan-out runs (many pages), one scorer subagent per page; generic category bullets cap the score at 6 and must be named as gaps with a situational/data/outcome rewrite.

## Deck (if format = deck)

Deck format routes to P4.S5 (HTML→PDF via headless Chrome) — the default deck path, overridable there with a recorded reason.

## App / product surface (if format = app)

Spec the MVP feature list and first-user journey here. For the UI, use `/frontend-design:frontend-design` if you have the `frontend-design` plugin installed (an **optional separate install**, not bundled here) — otherwise brief the build directly on the brand kit's tokens and layout rules. Then run a **review lens** over the result before it ships: does every screen state have a designed empty/loading/error case, is the primary action unambiguous on each screen, does the visual hierarchy match the task hierarchy, and does it hold on a 375px viewport. For product events from day 1, use `/posthog:instrument-product-analytics` if you have the `posthog` plugin installed (also an optional separate install) — otherwise instrument your analytics tool of choice against the same rule: the events exist before launch, not after.

**Write to** `P4-Build.S2-Copy.md`: the BUILD RULE line (build proceeds every run), live motion restated, asset 1 spec + pipeline, asset 2 spec (if any), distribution mechanic, dependencies (brand kit slug, copy approvals, instrumentation events, hosting target), and the Copy sources section if any web asset is in scope. Multi-page sites get the step folder `P4-Build.S2-Copy/` — one copy file per page, named for the page (`hero-copy.md`, `landing-page.md`, `pricing.md`), with the Copy sources section in the step md acting as the INDEX + meta contract.

**Def-of-success — ALL must pass before Owner sign-off (fail → improvement loop per SKILL.md, never advance):**
- `/critical` run recorded; the score is advisory (target ≥ 8/10) — the gate is the PASS/FAIL criteria below, not the number.
- BUILD RULE line recorded at the top; zero fabricated proof elements (the evidence-tier honesty that replaced the removed pre-sale gate).
- Claims-vs-offer fidelity: every capability/outcome claim in the copy maps to a line in approved `P1-Ideation.S6-Offer.md`; zero claims exceed the approved offer scope — exceptions listed and resolved or flagged to the owner.
- Format traceable to the P3.S1 outreach motion in one sentence ("motion X therefore asset Y").
- Copy sources complete: meta block, 100% of copy via `/brand-voice`, EN + market-language versions.
- `/marketing-psychology` pass recorded per page — every page's copy file names the persuasion principles applied; zero pages skipped.
- Keyword traceability: every page section maps to a keyword from the approved `P4-Build.S1-Keywords.md`; the AI-search phrasings are answered verbatim somewhere in the copy; zero keywords invented outside the contract.
- `/lead-magnets` run for every page that converts through email capture — magnet spec + copy present (P4.S3 builds, P5.S1 distributes) — or a "no capture pages" exception carrying a one-line justification tied to the distribution mechanic, FLAGGED to the owner for explicit approval of the omission (recorded in this file) — never a default.
- Zero em dashes in customer-facing copy; ≥ 1 proof element (quote, number, case) per page, each carrying its evidence tag in the page copy file (`[source: ...]` per the SKILL.md cited-assumption rule) — "zero fabricated proof" is verified per element, not asserted per page.
- Style rule held: zero generic category bullets; every topic line is situational, data-driven, or outcome-based.
- No-competition gate: every product/service/offering page scored ≥ 8/10 by the adversarial scorer (after ≤ 2 revise rounds), OR flagged to the owner with its score + open gaps. Zero pages silently shipped under 8.

**Gate out (mandatory — see SKILL.md house rules):**
1. Draft `P4-Build.S2-Copy.md`.
2. Invoke `/critical` on the draft — is the format actually derived from the live motion, or from what's fun to build? Is the evidence-tier honesty held — zero fabricated proof? Does the copy overpromise vs `P1-Ideation.S6-Offer.md`? For the overpromise check, dispatch a subagent that reads `P1-Ideation.S6-Offer.md` and the page copy files and returns the claim-vs-offer exception list — the check is artifact-based, not memory-based, and the main context stays inside the budget rule.
3. Run the **no-competition gate** on every product/service/offering page: adversarial score vs the competitor research, revise + re-score any page under 8/10 up to two rounds, flag survivors under 8 to the owner. Record scores in the page files.
4. Revise; note what changed.
5. Present the draft + the critical findings + the changes to the owner. **Wait for their explicit approval. Never auto-advance.** Approval of the Copy sources section is the explicit precondition for P4.S3.

**Checkpoint:** "First asset: [X]. BUILD RULE: build proceeds every run (no pre-sale gate). Copy sources: [approved/pending]. Copy step complete — if a web asset is in scope, P4.S3 builds it and P4.S4 tears down the competitors' source against it; deck-only goes to P4.S5; otherwise skip to P5.S1 (launch)."

**Next:** `stages/P4-Build.S3-Web.md` (skip to `stages/P4-Build.S5-Deck.md` if deck-only; to `stages/P5-Activation.S1-Launch.md` if neither web nor deck)
