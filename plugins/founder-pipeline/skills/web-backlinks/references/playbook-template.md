# PLAYBOOK.md template

Copy this skeleton to `<property>/backlinks/PLAYBOOK.md`, fill every `{slot}`. **The header = everything above `## Plan tracker`.** It travels verbatim to every executor — keep it under 500 words. Nothing below the tracker line is ever sent to executors.

```markdown
# Backlink Playbook — {domain}
updated: {YYYY-MM-DD} · property: {property id from the registry} · brand class: {community/conference/personal/marketplace}
baseline ({date}): rank {N or unranked}, referring domains {N}
adopted from: {every prior file path, or "fresh"}
sending: {dedicated address user@domain, SPF/DKIM/DMARC verified {date} | primary inbox per owner OK {date}, cap 8/day}
second-language markets under the one-cold-email-ever rule: {list, or "none"}

## EXECUTOR CONTRACT (read fully before your block)

AUTONOMY: Templates marked GRADUATED you send yourself — no draft-for-approval
(the owner's standing decision, recorded above). Templates marked CANARY: return
the filled draft to the orchestrator for the owner's review — do NOT send. Also
return (never send): Owner-only queue items, replies with any question/humor/
negotiation or mention of payment.

THE FOUR LAWS:
1. White-hat only. Never edit Wikipedia to add our links. Never drop bare links
   on Reddit/forums. Never pay for links. Block seems to ask for this → BLOCKED, log why.
2. Honest framing. Send only emails stating what the recipient gets (for fix
   requests AND unlinked-mention asks, an accurate page IS their benefit —
   these are legitimate as written). Offer feels false → BLOCKED.
3. Stay inside the block. No improvised targets, recipients, or template edits
   beyond filling {slots}.
4. Never require, promise, or trade a followed link. Badge/embed snippets keep
   their rel="nofollow" exactly as written. Anchor for any link you place or
   request: the brand name or the bare URL — never a keyword phrase, including
   form anchor fields.

VELOCITY: {15 (all dedicated aliases) / 8 (any primary-inbox sending)} sends/day
TOTAL across all properties. Your dispatch message states today's remaining budget.
Would exceed it → DEFERRED.

SMALL-MARKET RECIPIENTS (person/org located in a market listed in the header, or
a contact on that market's country TLD, incl. org inboxes): one cold email ever,
across all properties. In-thread follow-up only for fix-request/housekeeping mail,
never for pitches.

EVERY COLD EMAIL ends with the identification + opt-out line:
"{sender name}, {legal entity}, {city}. Writing because {one clause: why them}.
Reply 'no thanks' and I won't write again." (Translate the opt-out phrase into
the recipient's language where the template is non-English.)

VOICE:
- Context first, ask within 2 sentences. 4-6 lines, ONE ask.
- No em dashes. No exclamation marks. Sign off as configured in the voice rules.
- Real numbers only, from CONTEXT — never invent numbers, names, stories.
- Banned words: leverage, unlock, empower, delve, robust, holistic, streamline,
  utilize, comprehensive, foster, resonate, landscape.
- Non-primary languages: fill {slots} only — never compose the text yourself.
  Formal register, full diacritics.

SUPPRESSION (orchestrator pre-checks; if you still spot one, BLOCK): recipient
in do-not-contact.md, prior mail thread, known member/speaker/sponsor
(lists: {pointers}), client/partner in the CRM, ledger cooldown.

RESULT FORMAT — you write NO files. Return exactly:
`BL-NNN | sent/blocked/deferred/canary-draft | {recipient} | {one-line note or draft attached}`
The orchestrator writes PLAYBOOK.md, outreach-log.md, the ledger, **and any adopted task-board row** (Phase 4.8b — a block going terminal flips its `board_row` to `Done`/`Parked`/`Killed`). Executors never touch the board.

## Plan tracker
| metric | value |
|---|---|
| blocks total / terminal (won+parked+dead) | {N} / {N} |
| completion | {N}% |
| in flight (sent, awaiting reply) | {N} |
| stalled (follow-up exhausted, >14 days) | {BL-NNN list → auto-park next run} |
| blocked/deferred needing attention | {list + reason} |
| next gates | {dates / block IDs} |
| Owner-only + decisions + build queues open | {N} |

Updated by EVERY run and by /founder-pipeline:web-backlinks status. Plan COMPLETE
= all blocks terminal AND all queues empty. Every non-terminal block gets advanced,
gate-waited, or parked each run — none rots silently.

## Migrated state (from adopted files — history, do not re-pitch)
| target | contact | channel | last action + date | status | follow-up gate |
|---|---|---|---|---|---|

## Owner-only queue
{Signups, payments, posts/PRs/answers from the owner's identity (Reddit, Quora,
GitHub, X, LinkedIn), warm contacts found by suppression — paste-ready content inline.}

## Owner decisions
{Choices blocking blocks, e.g. "marketplace profile X may outrank our own site
for the owner's own name — yes/no?" One line each + what unblocks.}

## Build blocks
{model: build — assets/pages needed before outreach (badge SVG + page, directory
MVP, stat page). Routed to /founder-pipeline:web-site-creator. Outreach blocks
depending on them carry gate: BL-NNN.}

## Blocks
{sorted impact/effort; cheap wins first}
```

## Block format

```markdown
### BL-{NNN} · {verb-first title}
status: pending | model: cheap|mid|build | gate: {date | BL-NNN | none} | est: {min} | impact: {H/M/L, DR if known} | risk: {low/med}
board_row: {task-board row URL if this block was adopted from a board row, else `none`}
TOOLS: {mail send | browser form | web fetch}
CONTEXT: {everything inline: recipient name + email + HOW it was verified (live
  site / CFP thread / prior thread), page URLs, why this target, allowed numbers,
  asset URLs with "verify 200 before send" where relevant, language.}
TEMPLATE: {CANARY (canary_remaining: 3) | GRADUATED {date}}
  Subject: {…}
  {full text with {slots}; recipient benefit in the text; identification +
  opt-out line at the end}
TASK:
  1. {exact steps incl. gate check and any verify-before-send}
  2. Send (GRADUATED) or return draft (CANARY).
  3. Return result line per contract.
DONE WHEN: {verifiable: result line returned; orchestrator confirms logs written}
```

Status values: `pending → canary (draft with the owner) → sent → replied → won | parked | dead | blocked | deferred`.
Lifecycle: one follow-up ever (gate = last send + 21 days); no reply 21 days after the follow-up → `parked`; explicit no / opt-out / bounce → `dead`. Small-market recipients: follow-up only for fix-request/housekeeping class; pitch blocks go straight to `parked` if silent.

## Compile-time checklist (Phase 3, before saving)

- [ ] Header < 500 words; sending decision recorded; suppression pointers present; velocity default set (run passes the daily remainder)
- [ ] Every cold-email TEMPLATE: recipient benefit in text + identification/opt-out line
- [ ] Law-4 sweep: no required/traded followed links anywhere; badges carry rel="nofollow"; anchors brand-only
- [ ] Law-3 spot check: 2 random blocks executable by a fresh cheap-model session with only block + header
- [ ] Non-primary-language templates compiled (never composed), formal register, diacritics, CANARY
- [ ] Nothing needing the owner's accounts/identity/payment sits in executor blocks (→ the three queues)
- [ ] Migrated state complete; ledger backfilled; no migrated target reappears as a new block; one gated follow-up block compiled per in-flight migrated row (small-market: fix-request class only)
- [ ] Gates set: follow-up = last send + 21 days, one follow-up ever (small-market: fix-request/housekeeping class only, never pitches); dependency gates point at build blocks
- [ ] Every number in TEMPLATE and CONTEXT verified against your numbers source of truth this run
- [ ] **Every block adopted from a task-board row carries its row URL in `board_row:`** (blocks originated here carry `board_row: none`). Without it, Phase 4.8b has nothing to write terminal state back to and the row rots on `Ready`

## Delta report format (end of every `/founder-pipeline:web-backlinks run`)

```
{domain} — run {date}: {N} executed ({sent}/{blocked}/{deferred}/{canary-drafts})
Per-template: {name}: {sends} sent / {replies} replies {⚠ if 20+/0}
Replies since last run: {N} ({summary; escalations to the owner listed})
Links won: {N} · Referring domains: {N} (baseline {N}, {+N}) · Plan completion: {N}%
AI-citation line (never merged into referring domains): brand mentions {N} · third-party listicle placements {N} · entity-surface changes {N}
Board sync: {N} rows flipped ({Done}/{Parked}/{Killed}/{Blocked}) · drift found: {N or none}
Deliverability: {bounces/complaints this run; monthly postmaster check due {date}}
Next gates: {dates/IDs} · Owner queues: {N open} · Blockers: {list or none}
```
