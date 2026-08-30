# Step 01 — Brief → GATE A

The owner gives a short description of the post and expectations. Extract a one-screen brief; don't start researching until GATE A passes.

## Extract (ask only what their message didn't answer, one at a time)

1. **Why this post** — the business reason. Which money page / service does it feed? (The site profile lists the money pages.)
2. **Target reader + their moment** — who is reading, and in what situation ("EM three weeks after their first layoff", not "engineering managers").
3. **The contrarian claim** — the one position most people in the room won't say out loud. If the owner hasn't stated one, propose 2-3 candidates and ask which they stand behind. Never invent a position they don't hold.
4. **The personal story available** — which lived scar/win anchors this post? Ask the owner. If a story about someone they mentor or advise: confirm anonymization (virtual first name).
5. **Success definition** — what should a reader do differently tomorrow after reading?
6. **Seed keyword hunch** (optional) — the owner's guess at the search phrase; research validates or replaces it.
7. **Expert co-creation** (optional, pillar posts only) — should 1-3 known figures in the space be asked for a review quote or co-creation before publish? Worth it when: the post is a pillar/GEO play, the figure's audience overlaps the ICP, and there's a real relationship or a credible cold angle. The payoff is distribution (they share what they're quoted in), a likely backlink, and E-E-A-T. The cost is 3-10 days of cycle time and relationship capital — so default NO for regular posts, YES for ~1 pillar post a month. If yes: send the gated draft (post-step-06) with a specific ask ("one 2-3 sentence quote on X"), quote them with name + link in the post, and tag them in the step-12 announcement. Candidates come from the owner, never invented.

## Write

`brief.md` in the workspace: the six answers, ≤1 screen. Propose the working slug (kebab-case, keyword-bearing; final slug locked after research).

Create `STATE.md`:

```markdown
---
slug: <slug>
site: <site-slug>         # matches references/sites/<site-slug>.md
status: active           # active | paused | blocked | done | killed
current_step: "01"
gate_a: pending          # pending | <YYYY-MM-DD>
gate_b: pending          # pending | <YYYY-MM-DD, the PR merge date>
privacy_check: pending   # pending | pass | blocked | legacy (predates the privacy gate)
pr: null                 # PR URL once step 08b opens it
backlog_row: null        # idea-backlog row reference, if backlog-sourced
blocked_on: null         # one line, only when status is blocked/paused
---

# <slug> — pipeline state
- [x] 01 brief
- [ ] 02 research
- [ ] 03 skeleton
- [ ] 04 draft  - [ ] 05 images
- [ ] 06 gate      scores: —
- [ ] 07 translate - [ ] 08 internal links in - [ ] 10-prep exports
- [ ] 08b privacy gate + PR
- [ ] 09 deploy    GATE B: —
- [ ] 10 syndicate - [ ] 11 backlinks - [ ] 12 announce
GATE A: <date, the owner's words>
```

## Branch immediately — the default branch never sees work in progress

Before writing anything, cut the branch the whole post will live on:

```bash
git -C <site-repo> checkout -b post/<slug>
```

Everything from here — the draft MDX, the localised mirror, images, and every `.blog-pipeline/<slug>/` commit (STATE.md ticks, research JSON, gate reports, exports) — lands on that branch. The default branch only ever receives a finished post, as one merge. Record the branch name in the body of `STATE.md`.

`.blog-pipeline/` **is committed** (text only — a few hundred KB of md/json; keep it out of any repo you would not want the research in): the keyword research is paid API data that step 02 caches to avoid re-buying, the gate reports are the audit trail behind each 8/10 call, and the exports are step 10's manual fallback when browser posting hits a login wall. Commit as you go, one commit per step — that's what makes a crashed run resumable on any machine instead of only the one it started on.

**The frontmatter is the machine-readable contract; the checklist below it is the human log.** Any automation that advances the pipeline reads ONLY the frontmatter to decide what to advance, so it must be updated at every transition — a stale `current_step` means the run re-does work or skips it. Keep writing the prose notes in the body as before; they're for humans and for resuming after a long gap.

## Two ways in

**Backlog-sourced (the default for automated runs).** The brief comes from an idea-backlog row already promoted to `Ready` in `queues/` — which means the owner filled `Personal hook` + `Contrarian claim`, and **that promotion IS GATE A**. Compose the brief from the row (angle, hook, contrarian claim, target money page, seed keyword), set `gate_a` to the promotion date and `backlog_row` to the row reference, and continue to step 02 without pausing. Do not re-ask the owner for approval they already gave in the backlog.

> Optional integration: if you have wired an external task board (Notion, Linear, a spreadsheet — see SKILL.md), a promoted row there works exactly the same way and `backlog_row` holds its URL. The local `queues/` files are what ships and what the pipeline assumes by default.

**Conversational (the owner names a topic directly).** Run the extract above and stop at GATE A below.

## GATE A (blocking — conversational route only)

Show the owner: the brief + working slug + one-sentence angle. Wait for their explicit approval. Record their words in `STATE.md` and set `gate_a` to today. Never auto-advance.

**Next:** `steps/02-research.md`
