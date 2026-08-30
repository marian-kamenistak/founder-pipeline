# Step 11 — Per-post backlinks

Consumes `research/backlinks.json` (R3: where the top competing posts get their links) + the R3 list parked in `research/SYNTHESIS.md`. Runs ∥ steps 10 and 12.

## Filter (mid-tier model in a subagent)

From R3's referring domains/pages, keep only placements realistically reachable for THIS post:

- **Quora**: existing questions matching the post's FAQ phrasings (genuine answer, 1 link max, ~30 min/answer quality bar).
- **Reddit**: the subreddits in your niche where competitor posts actually earned links — a real contribution referencing the post, never a bare link drop.
- **Hacker News**: submit only if the post reads as an essay, not marketing (the gate report tells you); best Tue-Sat mornings.
- **Directories/newsletters/listicles** that link to competing posts — each with the contact/submit path found in R3 data.
- Drop: spam-score >30 domains, link farms, anything violating the four laws below.

Output: ≤10 placements, each with target URL, why it links to competitors, the concrete action, and effort estimate.

## Register + hand off (main loop)

1. Append the placements to that site's backlink register (the register file is named in `${CLAUDE_PLUGIN_ROOT}/skills/blog-launch/references/sites/<site-slug>.md`), tagged with the per-post placement tier and matching the register's table format, and note them for the Progress log (format: `YYYY-MM-DD  <tier>/<ref> <target>  <URL>  <status>`).
2. Route execution through `/founder-pipeline:web-backlinks` (it owns outreach drafting, the ledger, the velocity budget, and the owner-only queue for identity posts — Reddit/Quora answers published under the owner's own name are theirs to paste, prepared but not posted).
3. Its four laws bind this step too: white-hat only, no bare-link drops, honest framing, never trade a followed link.

Report to the owner: placements registered, what's queued in `/founder-pipeline:web-backlinks`, and what awaits their paste. Update `STATE.md` (step 12 marks the pipeline complete).
