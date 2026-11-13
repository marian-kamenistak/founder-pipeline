# P2.S2 — Tooling + operating stack → `P2-Viability.S2-Tooling.md`

**Phase: P2-Viability**

**Routing:** plain (drafts ∥ with P2.S1) · draft MID, stage judge MID · gate critic on the session model

**∥ note:** this step may draft in parallel with P2.S1 (economics) — its costs feed back into P2.S1's model before P2.S1's gate closes — but it gates separately, with its own `/critical` pass and its own owner sign-off.

**Earns its keep when** the stream needs new infrastructure (a site, an app, payments, scheduling, CRM). **Becomes performative when** the stream runs entirely on tools already paid for and wired up — then this is a 10-line inventory, not a project.

## The house stack is an input, not a decision made here

The **house stack was declared once at P1.S1** and recorded in `brief.md`: the default framework, host, analytics platform, form/anti-spam pair, transactional email sender, CRM, and automation platform this operator builds on. This step does **not** re-litigate it. It does three things:

1. Maps each delivery and build need onto a house-stack row.
2. Names the **gaps** — needs the house stack does not cover.
3. For each gap, picks a tool here and **writes it back into `brief.md`**, so every later stage inherits one stack instead of re-choosing per step.

Re-opening a house-stack row is allowed, but it is an **override**: record the row, the replacement, and the reason in this file. Silent per-stream tool drift is what turns one operator into six half-configured stacks.

**If no house stack was declared at P1.S1** (skipped, or this is the first stream), declare it now and write it into `brief.md` before answering anything below — later stages read it from there, not from this file.

### The recommended default stack (worked example)

Use this if you have no opinion yet. It is one operator's working stack, shipped because it is cheap, fast, and boring — not because it is the only correct answer. Every row is replaceable; the *reason* column is what should survive the replacement.

| Need | Recommended default | Why this shape |
|---|---|---|
| Web | A static-first framework on an edge host, scaffolded via `/web-site-creator` (the reference implementation targets Astro on Cloudflare Workers) | Ships fast, near-zero run-rate, no server to maintain |
| Decks | HTML → PDF through a headless system browser (P4.S5) | Version-controlled, diffable, no export dance; see P4.S5 for the override path |
| Analytics | A product-analytics platform with event tracking and funnels (PostHog in the reference stack) | Events, not just pageviews — P6.S2's KPIs need behaviour |
| Forms | A bot-challenge widget + a transactional email sender (Turnstile + Resend in the reference stack) | Spam control and deliverability are two jobs; one tool rarely does both well |
| CRM | Your CRM, whatever it is (Attio in the reference stack) | P3.S1 needs a system of record with an API, not a spreadsheet |
| Automation | A no-code automation platform, a scheduler, or an MCP integration (Make.com in the reference stack) | Whatever protects the weekly hour budget without new code to own |

**Ask one at a time:**
1. Delivery tooling — what does fulfilling one client require? (calendar/scheduling, docs, video, community platform, LMS, etc.) Name what exists vs what's missing. Then map the full client motion — form, booking, payment, contract, email deliverability (DNS/SPF owner named) — each touch to a stack row; an uncovered touch is a gap, not a footnote.
2. Build tooling — what does the asset build need? Answer from the house stack above; name only the **gaps** and the **overrides**, with reasons.
3. Payments + contracts — how does money actually arrive? (invoice, card processor, bank transfer) What legal/contract template is needed?
4. New subscriptions or one-off costs this stream adds — feed them back into `P2-Viability.S1-Economics.md` run-rate if not already there.
5. Automation opportunities — what recurring work can the automation row of the stack absorb (automation platform, scheduled job, or an MCP integration) so the weekly hour budget from P2.S1 holds?

**Skills:** `/web-site-creator` Phase 1.0 preflight — it runs a **brand-kit availability check** against your configured brand kit for this brand (does a kit exist, is it current, what is missing). Record its result here rather than discovering it mid-build in P4.S3. For the automation requirement below, **design** the automation — trigger, steps, failure path, owner, and where it runs — rather than naming a tool; if your automation platform ships a Claude Code plugin, install it separately and use it here. A named tool is not an automation.

**Write to** `P2-Viability.S2-Tooling.md`. Table: Need | Tool | Status (have / configure / buy) | Cost/month | Owner. Plus the client-motion coverage map (Touch | Stack row | Owner), the house-stack gap + override list (Row | House default | This stream | Reason), and the brand-kit check result (kit exists yes/no + action taken). Flag anything that adds to `P2-Viability.S1-Economics.md`. Costs use the currency declared at P1.S1.

**Def-of-success — ALL must pass before owner sign-off (fail → improvement loop per SKILL.md, never advance):**
- `/critical` run recorded; the score is advisory (target ≥ 8/10) — the gate is the PASS/FAIL criteria below, not the number.
- Minimum Ship stack identified — every tool on it traces to a named delivery or build need; zero "nice to have" in the Ship column.
- Every new cost fed back into `P2-Viability.S1-Economics.md` run-rate (cross-checked, not assumed).
- **House stack honoured:** every build need maps to a declared house-stack row, or to a recorded override naming the row, the replacement, and the reason. An undeclared new tool is a FAIL, not a footnote — and the web surface goes through `/web-site-creator` unless the override is recorded here.
- ≥ 1 automation identified that protects the P2.S1 weekly hour budget, specified as a design (trigger, steps, failure path, owner) — not as a tool name.
- Every table row complete: named tool, Cost/month cited to a live pricing-page URL or invoice, named owner; zero TBD/decide-later rows — any unresolved gap becomes a `queues/manual-queue.md` row before the gate.
- Brand-kit check result recorded in the output file: kit exists yes/no + action taken.
- Client-motion coverage map complete — form, booking, payment, contract, email deliverability (DNS/SPF owner named) each mapped to a stack row; any uncovered touch = FAIL.

**Gate out (mandatory — see SKILL.md house rules):**
1. Draft `P2-Viability.S2-Tooling.md`.
2. Invoke `/critical` on the draft — hunt for tool-shopping disguised as necessity: which "needed" tools are actually procrastination? Which overrides are preference dressed as requirement? What's the minimum stack for Ship phase?
3. Revise; note what changed.
4. Present the draft + the critical findings + the changes to the owner. **Wait for their explicit approval. Never auto-advance.**

**Checkpoint:** "Stack locked: [X new tools, Y/month added to run-rate], [Z] house-stack overrides recorded. Pricing next (P2.S3)."

**Next:** `stages/P2-Viability.S3-Pricing.md`
