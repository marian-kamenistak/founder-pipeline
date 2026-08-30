# Step 06 — Rating gate: 8/10 or it doesn't ship

Load `references/rating-rubric.md` (the verbatim judge prompt + anchors live there).

## W2 — judge panel via the Workflow tool

`parallel(judge1, judge2, judge3, linkcheck)`:

- **3 blind judges** — fresh contexts, **session model**, `effort: 'medium'`, identical prompt from the rubric file + the full post text. No access to the writer's context, the brief's history, or each other. JSON schema output: `{ simplicity: 0-10, value: 0-10, flags: [{quote, problem}] }`.
- **linkcheck** — cheap-model agent: curl every external link (expect 200/301), verify internal links exist in the site repo, description char count, headline rules, ≥1 personal story present, ≥1 counter-voice cited, readability-design checks (no >4-sentence paragraphs, pull-quote present, no uniform text wall), **exactly one `<h1>` in the built page and no skipped heading level** (build the post, then `grep -oi '<h[1-6]' dist/client/blog/<slug>/index.html` — a body `#` producing a second `<h1>` is a gate failure, not a style nit; see `steps/04-draft.md`).

## Alongside: /founder-pipeline:critical (main loop)

Run `/founder-pipeline:critical` on the draft + brief: is the angle actually contrarian or better-written sameness? Is the value real? It ends with `CRITICAL SCORE: X/10`.

## Verdict (computed, not felt)

- **PASS** = median(simplicity) ≥ 8 AND median(value) ≥ 8 AND all mechanical checks green AND CRITICAL SCORE ≥ 7.
- CRITICAL SCORE < 7 forces a revise round even if the judges pass.

## Revise loop (max 2 rounds)

Writer (original step-04 context) receives **flags only, never the scores** — prevents writing-to-the-number. Revise, re-run the `/founder-pipeline:brand-voice` self-check, then a **fresh** W2 panel. Each round's scores append to `gate-report.md` and `STATE.md`.

## On persistent fail after 2 rounds

Hard stop. Write `gate-report.md` (all rounds, all flags, all scores) and present the owner exactly three options:
1. **Kill** — delete the MDX, keep the workspace for post-mortem.
2. **Park** — draft stays `draft: true` in the repo + workspace intact.
3. **Override-publish** — requires their literal words; logged verbatim in `STATE.md`.

Never silently publish, never silently delete.

On PASS: post the gate report to the owner as FYI, update `STATE.md`. **Next:** `steps/07-translate.md` ∥ `steps/08-internal-links.md` ∥ step 10's export prep.
