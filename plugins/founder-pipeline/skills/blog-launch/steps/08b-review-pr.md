# Step 08b — Privacy gate → PR + preview → copy review

Two jobs, in this order and never reversed: **prove the post is safe to publish**, then **hand it to the reviewer in a surface they actually use**.

Where a named collaborator does the copy review, assume they do not work in GitHub — a copy reviewer is usually not a developer, and may review in a different language than the one you drafted in. The PR exists as plumbing — it produces the preview URL, holds the diff, and is the thing that eventually merges — but it is not the review surface. **The reviewer needs no repo access**, which is why briefs and raw research never leave the owner's account.

Pick one review surface and keep it: a task board, a shared doc, or a CMS with commenting. The worked example below uses a task board with per-block comments, which is what makes sentence-level feedback possible. If you use Notion for this, the `Notion:*` plugin is an optional dependency you install separately.

---

## Part 1 — Privacy gate (BLOCKING, runs first)

Where the owner's material comes from live client, mentoring or prospect relationships, a published post can out a real person's employer, their situation, or the mere fact that they are working with you at all. This gate is the only thing standing between a private conversation and a permanent public URL.

**It blocks. It never flags-and-continues.**

### Check A — scan the rendered text

Read the primary-language post, every translated mirror, and the FAQ block. Flag every instance of:

- A company name that isn't a public example (a named case study, a public talk, a company the owner has written about before with consent).
- A real first or last name attached to a story. Client stories use a changed first name — verify the change actually happened rather than trusting the draft's word for it.
- A **role + company** combination ("the VP of Engineering at a fintech in a mid-size European capital") — this identifies one person in a small market even with no name.
- A **tenure + size + industry** combination specific enough to narrow to one person ("10 years at the same 200-person healthtech").
- Anything that reveals someone is *currently* being coached, mentored, or performance-managed. This is the most damaging category and the least obvious.

Judge against the reader in your smallest market, not your largest. A detail that is anonymous in a market of 300 million identifies exactly one person in a market of 10 million — and your smaller market is usually your home one, where you are most likely to be read by people who know the subject. If you publish in more than one language, judge against the reader of the smaller-market translation, not the primary-language original.

### Check B — declared guardrails

If the draft, the brief, or the source idea carries a `⚠️ Guardrail` block, **read it and resolve it explicitly**. These are the owner's own warnings, written at capture time, when they still remembered the real situation.

What such a block looks like: a draft built on a live client engagement records which parties it describes — the person being written about, and whoever else was in the room — and states exactly which details may not be published. Write the guardrail at capture time, because by drafting time nobody remembers which detail was the sensitive one.

Resolution means ONE of:
- **Generalized** — the archetype survives, every identifying detail is gone.
- **Composited** — merged with other cases so no single real person is described.
- **Consented** — the owner confirms they have explicit sign-off. Their word, in this session, recorded in `STATE.md`. Never infer consent from the fact that they wrote the draft.

A `Guardrail` flag set on the backlog row means Check B is mandatory even if the draft carries no inline block.

### Outcome

- **Clean** → set `privacy_check: pass` in `STATE.md`, continue to Part 2.
- **Any hit** → set `privacy_check: blocked` and `status: blocked`, write the specific finding into `blocked_on`, raise it on whatever alerting channel you use, and **stop**. Do not open the PR. Do not "note it for later". The finding goes to the owner as: what was found, where, and the two or three ways to resolve it.

**This gate runs again before step 10.** Syndicated copies on third-party publishing platforms can't be quietly edited the way a post on your own site can, and the syndicated version is a *different artifact* — re-verify rather than trusting the earlier pass.

---

## Part 2 — Branch, PR, preview

The branch already exists from step 01. Finish it:

1. Commit remaining work — the primary-language source, every translated mirror, images, and the `.blog-pipeline/<slug>/` state.
2. Push `post/<slug>`.
3. Open the PR against the site's default branch. Body carries: gate scores from step 06, the target keyword, the money page it feeds, the personal hook, and **the privacy-check result**. Title: `post: <slug>`.
4. CI builds the preview and comments the URL. Wait for it — the preview URL is the deliverable of this part, not the PR itself.
5. Verify the preview actually renders the post: the page loads at its real route, the featured image resolves (not the site fallback), and the FAQ block is visible. A broken preview wastes the reviewer's time and they have no way to diagnose it.

---

## Part 3 — Hand it to the reviewer

Update the post's row on your blog-ideas backlog:

| Field | Value |
|---|---|
| `Status` | `In review` |
| `Preview URL` | the CI preview link — **this is what the reviewer reads** |
| `PR` | the PR URL (for the owner's merge, not for the reviewer) |
| `Review` | `Pending` |
| `Sent for review` | today |

Then **paste the post body into the review surface itself** — every language, as normal rich-text blocks, not a code block. Per-block comments are the whole point: they let the reviewer comment on a specific sentence instead of describing where the problem is. Above it, a short header block: the angle in one line, the target reader, and what the post is trying to get them to do.

Notify the reviewer on whatever channel you already use with them. Set `STATE.md` `status: paused`, `blocked_on: "awaiting copy review"`.

### What the reviewer does

- Reads the rendered preview.
- Comments inline on the pasted body for anything specific.
- Sets `Review` = `Approved` or `Changes requested`, with a one-line summary in `Reviewer notes`.

### Changes requested

Pull their comments, apply them, push to the same branch (the preview updates automatically), set `Review` back to `Pending`, and tell them. Do not merge, and do not argue with the feedback in the row — if something can't be applied, that's a conversation with the owner, not a note on the board.

**Copy changes are still copy.** Anything reader-facing goes through `/founder-pipeline:brand-voice` before it lands, and the Copy sources record gets updated — a reviewer's edits do not bypass the voice rules.

---

## GATE B

**`Review` = `Approved` on the board, then the owner merges the PR.** Two acts, one gate: the reviewer owns the judgment, the owner owns the button. Where the owner is also the only reviewer, the two acts still happen separately — approve the copy in one pass, merge in another.

The merge itself flips `draft: true` → `false`, so an unapproved or abandoned post stays invisible on the live site by construction. Set `gate_b` to the merge date and `privacy_check` stays `pass`.

Nothing downstream — deploy, indexation, syndication, identity posts — may run before the merge exists. If you run a scheduled tick job over the pipeline it should enforce this; don't bypass it by hand either.

**Next:** `${CLAUDE_PLUGIN_ROOT}/skills/blog-launch/steps/09-deploy.md`
