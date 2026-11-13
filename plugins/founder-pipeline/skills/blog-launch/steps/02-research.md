# Step 02 — Research (W1 fan-out + synthesis)

Four research agents in parallel, then a main-loop synthesis. Recipes + budgets: `references/research-playbook.md` (load it now). Raw JSON goes to `research/` on disk; only conclusions enter the main window. Budget roughly one currency unit of keyword-API spend per post.

## W1 — launch via the Workflow tool

With the owner's yes, run one workflow: `parallel(R1, R2, R3, R4)`, each an agent at the MID tier (your default general-purpose model), `effort: 'medium'`, and a JSON output schema. When the four questions are plain evidence gathering, `/founder-pipeline:gather-verify` runs the same shape with a skeptic and a completeness critic behind it. Without the Workflow tool, dispatch the four as parallel subagents. Each agent prompt includes: the brief (paste `brief.md`), the site profile's territory defaults, the recipe from the research playbook, and the instruction to save raw API responses under `research/`.

| Agent | Question it answers | Recipe |
|---|---|---|
| R1 keywords | What phrase do we target, what volume/difficulty/trend/intent? | playbook R1 |
| R2 SERP angles | Who ranks today, what do they say, what do they ALL miss? | playbook R2 |
| R3 backlink mining | Where do the top competing posts get their links from? | playbook R3 |
| R4 AI-search | What do ChatGPT/Perplexity answer today, who gets cited, which phrasings to answer verbatim? | playbook R4 |

If your keyword-data MCP server is unavailable to subagents, fall back to the provider's REST API, reading credentials from your environment or secrets store per the playbook; if both fail, mark the affected outputs `[assumption — validate in Search Console]` and continue. Never fabricate volumes.

## Synthesis (main loop, session model)

From the four JSON outputs produce `research/SYNTHESIS.md`:

1. **Primary keyword + intent** (one; secondaries ≤3). Locked slug.
2. **3 headline candidates** per `references/writing-style.md` headline rules (number / How-to / question form, 40-49 chars target, no content-mill smell).
3. **The gap** — 3-5 valuable ideas the ranking posts all miss (this is where the post wins; from R2).
4. **AI-answer targets** — 3-5 natural-language questions to answer verbatim (feeds `faqs` frontmatter; from R4).
5. **Backlink source list** — R3's placements worth reusing, parked verbatim for step 11.
6. **Kill check** — if R1 shows near-zero volume AND R4 shows no AI-search demand AND the post has no strategic purpose beyond search (per brief), say so to the owner now instead of writing into a void. A post can still proceed as a positioning/HN piece; that's their call, one question, then continue.

Update `STATE.md`. **Next:** `steps/03-skeleton.md`
