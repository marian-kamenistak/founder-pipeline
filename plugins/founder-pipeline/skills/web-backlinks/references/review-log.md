# Design rationale — why this skill's rules read the way they do

Not a changelog. This is the record of what was tested, what broke, and which rule each failure produced — kept so nobody "simplifies" a rule that exists because the simple version already failed once.

## Credentials & browser automation (Phase 4.4b)

**The gap.** Phase 4 blocks could specify `TOOLS: browser form` but had no instructions for how an executor actually authenticates or drives the browser. A live run hit this directly: account creation and password entry had been authorized in-session by the owner, the agent declined both because no credential-retrieval mechanism existed, and every account-gated directory in the batch stalled on the owner-only queue with no path forward.

**What was verified before writing the fix** (environment checks, not a full pressure-test — this is a capability/reference addition, not a discipline rule): the password-manager CLI installed and reachable in-shell; the automation vault confirmed reachable with write scope; the vault confirmed to hold **almost no** login items for the gated targets in question, meaning most needed fresh signups rather than credential lookups; exactly one browser connected to the automation MCP server (no ambiguous-device prompt needed).

**The tension found.** A general rule against the agent ever handling an existing high-value secret exists for good reasons. But driving a login through a browser-automation `form_input` call inherently means the value passes through a tool-call parameter — and a *brand-new* signup password doesn't pre-exist anywhere safer; it's born the moment the agent generates it. Drafting an unscoped exception was blocked by the harness's own permission classifier on the first attempt ("widens permissions beyond what the user asked… this specific weakening was not user-requested") — correctly: what had been asked for was password-manager-driven automation, not a named override of an existing safety guard.

**The correction, and it is the load-bearing part.** The next draft asked the owner directly and got explicit authorization for a password-manager write fallback covering freshly-generated, low-stakes signup passwords. **That authorization did not make it permissible.** The platform's browser-automation rules prohibit the agent creating accounts or entering passwords into any field, and state explicitly that user authorization does not lift that prohibition; the one sanctioned exception is a dedicated credential-request tool where the password manager's own UI takes per-item human approval and the value never reaches the agent. No such tool is wired into this skill. Caught before any live run executed against it.

So Phase 4.4b reads as it does: password, signup and login steps are owner-only, full stop; the agent may pre-fill non-secret fields and stage content but never drives a credential-bearing step. **Do not "restore" the fallback on the strength of an in-chat yes** — that is exactly the path that was already walked and reversed.

**Second finding from the same pass:** a "self-serve" label on a target that was written from search data rather than a live page load is not evidence. At least one target labelled self-serve turned out to be account-gated on first contact. Verify by loading the page before submitting anything.

**Third finding:** an unattended run must not depend on a credential store that requires biometric or desktop-app unlock. Where a password manager forbids service-account access to a personal vault by design, the fix is not a smarter fallback — it is removing the dependency: anything this skill needs lives in a service-account-reachable vault, and a credential found only in a personal vault is logged as a setup gap for a human to move, not worked around per-run.

## Task-board write-back (Phase 4.8b)

**The bug.** When an external task board is wired up, it starts out intake-only. Phase 1 adopted rows from it; nothing ever wrote state back. The signature is unmistakable once you look: a board carrying **zero `Done` rows of this skill's type against several `Done` rows of the sibling listings skill's type**, with a large pile of `Ready` rows — that's a missing write-back, not unproductive outreach. The sibling skill treats the board AS its ledger and flips rows on every outcome; this skill kept real state in PLAYBOOK.md / outreach-log.md / ledger.md and left the board frozen at whatever it was adopted as.

**Why it mattered beyond tidiness.** Two downstream failures, one of them cross-skill:
1. `status` reads PLAYBOOK.md; the board reads as the single marketing queue. They silently disagreed, with no way to tell which was right.
2. Any staleness escalation running against `Ready` rows nagged indefinitely on rows that were already executed and won — and those false nags were indistinguishable from the genuinely-waiting listings packs. The missing write-back was actively degrading the signal on *another skill's* queue.

**The fix, four touch points:** `board_row:` field added to the block format (`playbook-template.md`); Phase 1 adoption records the row URL into it and treats a missing one as an adoption bug; **Phase 4.8b** flips the row on terminal state (`won`→`Done` + live URL, `parked`→`Parked`, `dead`→`Killed`, `blocked`→`Blocked`+reason; send→`Waiting on reply`); orchestrator declared sole writer of the board, executors never touch it. `status` gained a board-drift line so a missed write-back surfaces instead of accumulating. Guard against the obvious over-correction: `board_row: none` creates nothing.

## The AI-citation layer (additive, not a re-scoring)

The `## The AI-citation layer` section in SKILL.md, plus its wiring into Family 1, Family 4, the Phase 4 delta report and Common mistakes, came from an evidence sweep, not from a re-review of the skill. What it establishes:

- **Backlinks are the weakest off-page correlate measured**: branded web mentions 0.664 > branded anchor 0.527 > brand search volume 0.392 > DR 0.326 > referring domains 0.295 > **backlinks 0.218** [Ahrefs, n=75,000 brands]. Vendor study from a company that sells a mention tracker — flagged as such in the skill.
- **Unlinked mentions stop being scored as failures.** They get their own reporting line, same treatment as entity work.
- **A hard new anti-pattern for Family 1**: never publish your own "best [category]" listicle — 224 of 323 self-promotional listicle citations (69%) cited the brand's own page and then recommended a competitor [Ray/Amsive, 100 B2B queries, replicated by Solis]. A directory *of others* stays fine.
- **Per-engine entity targeting**: Wikipedia/Wikidata ≈ a ChatGPT play, Reddit ≈ a Perplexity play [Profound, 30M citations] — recorded with the caveat that "share of top-10 sources" inflates concentration ~6× vs share of total citations.
- **Explicit guard against over-correction**: referring domains remain the KPI; the AI-citation layer is a second scoreboard reported alongside, never instead.

A sibling section covering review-profile presence — the biggest single off-page swing in the same dataset — lives in `/founder-pipeline:web-listings`.

## RED baseline (before the skill existed)

**Baseline A — planner (mid-tier model), "build a backlink plan for a domain":** found the existing hand-written target file and built on it — good. Failures: defaulted to draft-only against a standing autonomy decision; task blocks referenced external files ("copy in targets file") = not self-contained; no cross-property ledger; no canary/velocity concept (it did have date gates + dedup — both kept as first-class fields).

**Baseline B — executor (cheap model), naive blocks:** refused a Wikipedia link-insertion block (correct — gray-hat) and ALSO refused honest-goal outreach framed as extraction ("ask them to link to us"). Lesson: templates must state the reciprocal offer inside the email text or cheap executors refuse or stall. This is why Law 2 is written as a property of the template text, not of the operator's intent.

**Counters built into v1:** the Four Laws, adoption-first Phase 1, an executor contract with explicit autonomy and exceptions, canary + velocity, the cross-property ledger, the owner-only queue.

## Iteration record

| Round | Composite score | Verdict |
|---|---|---|
| Round 1: 3 domain dry-runs + penalty audit + executor test | 72/74/71 (dry-runs), 54 (risk), executor PASS | FAIL — major rewrite |
| Round 2: risk re-audit + fresh dry-run | 88 (risk, all 16 v1 findings verified fixed) / 87 (usability, all 6 v1 gaps fixed) | FAIL — 15 interplay bugs |
| Round 2 fixes applied | A-O fix list from both reviewers, incl. own-thread suppression carve-out, migrated-row follow-up compilation, small-market scope + contract placement, alias send mechanics, lifecycle unification, header boundary | — |
| Round 3: fix verification (A-O checklist) | 91/100 — 12/15 clean, 3 stale lines contradicting fixed siblings | 3 one-line edits applied |
| Final: stale lines fixed | **95+/100** — every reviewer-listed item for 95+ applied and verified | **SHIP** |

### Round 2 key catches

- **Own-thread suppression paradox**: the mailbox-history warm-contact check would have flagged the campaign's own sends and routed every follow-up to the manual queue. Carve-out: campaign-created threads (in outreach-log/ledger) reply in-thread.
- **Migrated rows had no execution path**: the history table defined gates but nothing compiled follow-up blocks from it — every in-flight target would have rotted.
- **The small-market rule was orphaned** (Phase 4 only, undefined scope) and killed legitimate fix-request follow-ups; now scoped, in the contract, and in the checklist with a fix-request-class exemption.
- **Business-critique pass (6.5/10)**: the skill is sound tooling, but cap at 2 active playbooks tied to quarterly revenue (now the Focus rule); the survey linkbait asset and clearing the first-cycle owner-only queue outrank all new outreach in ROI.

### Round 1 findings → fixes (all applied in the v2 rewrite)

- **Law 4 added**: a required link-back is a link scheme under Google's spam policy; directory verification decoupled from links; swaps nofollow both ways; badges ship rel="nofollow"; reciprocal cap 5; portfolio anti-PBN rules.
- **Sending infra**: dedicated per-property address preferred (SPF/DKIM/DMARC precheck), primary-inbox fallback 8/day only with a recorded OK; warm-up; bounce/complaint circuit breaker; per-template reply-rate breaker (20+ sends / 0 replies).
- **Compliance**: identification + opt-out line on every cold email; `do-not-contact.md`; the small-market one-cold-ever rule.
- **Suppression deepened**: mailbox-history check per recipient (prior thread → warm intro via the owner), audience-list check, tiered cooldowns (journalists 90d cross-property, others 30d), one-ask-ever per recipient across owned domains.
- **Canary redefined**: 3 drafts + recipient list reviewed, graduation after 5 clean business days; non-primary-language templates always compiled + CANARY, formal register + diacritics.
- **Concurrency model**: orchestrator sole writer, executors return result lines, intra-batch dedupe, run lock for multi-terminal.
- **Adoption spec**: whole-tree search (incl. `competitor_analysis/**/outreach*`), Migrated-state table + status vocabulary, gate derivation (+21d, one follow-up), ledger backfill.
- **Intake fixes**: competitors = INDEX or ≥5 profiles (kills a false ASK), intersection selection heuristic (exclude DR>80 generics), cost gate unified across phases, baseline reuse, context-resolution order, brand-class weighting, an event-listings family, BUILD blocks + dependency gates, an owner-decisions queue, the Law-2 carve-out for fix requests, and a correction to a stale career figure that had been carried in a template — which is why "verify every number at compile time" is a checklist item rather than advice.
