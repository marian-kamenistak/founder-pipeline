# P5.S3 — Activation: route the stream's execution work onto the task queues → `P5-Activation.S3-Queues.md`

**Phase: P5-Activation**

**Routing:** fan-out (one agent per step file/folder, synthesis plain on main thread) · sweep CHEAP · gate critic at the step tier

**Earns its keep** whenever the stream has a live web surface or any launched asset — the moment work stops being "build" and becomes "keep shipping into the world," it needs a tracked queue or the follow-through rots. **Performative** only for deck-only streams with zero ongoing distribution motion — record the skip in `brief.md` (skips still get the owner's sign-off).

**Why this step exists:** launches produce three streams of ongoing work — actions only the owner can perform, backlink acquisition, and media/content publishing — and every one of them historically died in "drafted, awaiting" limbo because no artifact tracked it. Activation converts launch outputs into tracked, owned tasks BEFORE Adoption (P6.S1–S3) starts burning the calendar.

**Where tasks live.** The shipped default is the stream's own `queues/` folder — three files, created from `templates/stream-folder/queues/` on first use:

| File | Holds |
|---|---|
| `queues/manual-queue.md` | Actions only the owner can do that serve neither link acquisition nor publishing: payments, filings, legal/admin, tool access, approvals of non-publish decisions. |
| `queues/backlink-queue.md` | Backlink and listing acquisition candidates for the stream's domain. |
| `queues/media-queue.md` | Content and coverage: posts, blogs, syndication, newsletters, podcast appearances, press, talks. |

Purpose decides the file, not the action type: a directory sign-up whose point is a backlink is a `backlink-queue.md` row owned by the owner; a platform login needed to publish is a `media-queue.md` row owned by the owner. Each file carries its own row format and status vocabulary at the top — follow it exactly rather than inventing columns.

**If you already run an external task board** (Notion, Linear, Jira, Asana, a Kanban board, an issue tracker), it is a supported substitute for all three files — one board, filtered by a `Stream` field and a `Type` field covering the three work streams. Pick one destination and use it for the whole stream; do not split rows across a board and the local files. Everything below applies unchanged; substitute "board row" for "queue row" and keep the same required fields. **Whatever escalation that board already has — a daily digest, a stale-item report, an SLA rule — is the re-surfacing mechanism; do not hand-build a second one beside it.** With the local `queues/` default there is no automation: re-surfacing happens at every checkpoint, which is why the checkpoint format below is mandatory.

## What to do

1. **Sweep P3.S1 through P5.S2 (Outreach, Keywords, Copy, Web, Deck, Launch, Links) for stranded work.** Grep the stream folder (step files, step output folders, build logs, STATE files) for anything "awaiting", "pending", "blocked", "owner must", "handed to". Record the sweep as a TABLE in the output file — one row per step, P3.S1 through P5.S2, columns `files checked | hits | routed to`; a 0-hit row still lists the files checked, so "swept" is provable, not claimed.
2. **Create one queue row per hit,** in the queue file whose purpose matches (table above). Every row carries, whatever the destination's column names: an **imperative task title** with estimated minutes · the **work type** (Backlink / Listing / Social / Content / Podcast / Newsletter / PR / Event / Outreach / Web-SEO) · the **stream** (this stream's domain) · a **status** (ready when an artifact exists, else backlog; blocked with the blocker named) · an **owner** (`<owner>`, a named collaborator, or `agent`) · the **date added** · a **ready-artifact path** to the prepared draft — reference by path, never copy content into the row · a **source** stamp `founder P<X>.S<Y> {stream}`. One item, one row — an owner-blocked backlink item is one row owned by the owner, not two.
3. **Seed backlink work:** top rows from P1.S5's `_backlink-gap.md` + P5.S1–S2 leftovers (`references/web-post-launch.md` surfaces not yet executed) that fit this stream — candidates only, effort-tagged, type Backlink/Listing; the full gap table stays where it is. `/web-backlinks` Phase 1 adoption reads `queues/backlink-queue.md`; graduated items move into the stream's `backlinks/PLAYBOOK.md` blocks and their queue rows get a `→ BL-NNN` note in Notes.
4. **Seed media/content work:** P5.S1's launch set (announcements, syndication of any shipped blog asset) + first-cycle posts from P4.S2's asset specs, and 3–5 podcast/press targets if in scope, into `queues/media-queue.md`. (Channel-driven rows get added later at P6.S1 — GTM runs in Adoption.)
5. **Hygiene contract:** every row carries added-date + owner + status + artifact path; the boundary rule holds (a podcast appearance is one `media-queue.md` row; chasing its show-notes link afterwards is a separate `backlink-queue.md` row referencing it); "ready / drafted, awaiting the owner" is an OPEN state, never a done state. Any row open ≥ 14 days gets a do / delegate / kill decision at the next checkpoint — that rule is the only thing standing between a queue and a graveyard. If the destination board automates it, verify the automation covers this stream rather than rebuilding it.

**Skills:** `/web-backlinks` (adopts `Backlink` rows when its playbook compiles), **`/web-listings` (adopts `Listing` rows — same queue, different skill; its Phase 1 audit reads them)**, `/blog-launch` (blog/syndication rows), `/brand-voice` (any queued copy is external-facing).

**Write to** `P5-Activation.S3-Queues.md`: the sweep table (one row per step P3.S1–P5.S2: `files checked | hits | routed to`), the list of created row titles with their queue file (or board URL), documented seeds, and any "empty because" notes.

**Def-of-success — ALL must pass:**
- Zero stranded "awaiting the owner" items remain outside the queues (sweep evidence recorded — files checked, hits routed).
- Sweep table has all 7 step rows, no empty files-checked cell.
- Every created row has task title + type + stream + status + owner + added date + artifact path (or a recorded "no artifact yet" reason).
- No item appears twice across the three queues (search the destination for the target before creating).
- ≥ 1 seeded row per work stream (backlink, media) OR a recorded "empty because" line.

**Gate out (mandatory — see SKILL.md house rules):**
1. Draft `P5-Activation.S3-Queues.md`.
2. Invoke `/critical` — attack the sweep hardest: did it actually catch every stranded item across P3.S1–P5.S2, and does every queue row have a real owner + artifact path, or are the queues just a new place for work to rot? `/critical` must spot-check that every referenced artifact path resolves (Read each, or ls the set) — a dead path is a blocking finding.
3. Revise; note what changed.
4. Present to the owner. **Wait for their explicit approval. Never auto-advance.**

**Checkpoint:** "Queue rows created: [N] ([N] backlink, [N] media, [N] manual). Oldest stranded item was [X, from step P<X>.S<Y>]. Pick the first batch to execute — or name what's missing."

**Next:** `stages/P5-Activation.S4-PredictionCadence.md`
