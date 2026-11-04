# Launch — ship the distribution assets

**Stream:** [slug]
**Step:** P5.S1-Launch (P5-Activation)
**Last updated:** [date]

> Launch is EXECUTION — assets published, servers registered, posts live — not planning. Items fan out in parallel (one delegated subagent each); this file is the gate-carrier. Item 6 routes to `/web-indexation` directly. Items 4, 5 and 7 have no shipped skill — run them inline as described in the table.

---

## Launch-item table

| # | Item | How it runs | Status (DONE / QUEUED / SKIPPED + reason) | Evidence URL | First-signal metric |
|---|---|---|---|---|---|
| 1 | First blog posts (2–3, from P4.S1 intent-to-page map) | `/blog-launch` | | | |
| 2 | MCP server publication | Inline (optional): if the stream answers a repeatable question an ICP would ask an AI, wrap that as an MCP server, publish the repo, and list it in the public MCP registries you use. | [SKIPPED needs "no real question the ICP asks an AI" reason] | | |
| 3 | Agent skill publication | Inline (optional): if the stream encodes a repeatable procedure, package it as a skill/plugin, publish the repo with a README and licence, and announce it where your ICP already looks for tooling. | [SKIPPED needs "no recurring use" reason] | | |
| 4 | Lead-magnet distribution (magnet from P4.S3) | Inline: publish the magnet on the site behind the capture form, verify the form fires a capture event end-to-end, then post the announce post on the channel P6.S1 names and link it. | | [announce-post URL] | [≥1 capture event in your analytics tool — event name + timestamp logged in step folder] |
| 5 | Day-0 baseline snapshot (ranks + AI citations, ONCE) | Inline: record today's position for each primary keyword and whether each target AI engine cites the site, with the date and the tool used. Whatever source you use, use the same one for every later read. | | [path in step folder] | (recurring reads belong to P6.S2) |
| 6 | Indexation + engines (sitemap/robots, IndexNow, reindex queue, plus any non-Google engine that matters in your home market) | `/web-indexation` | | | |
| 7 | Local Business identity (map/business profile + NAP consistency across every listing + ≥1 local directory citation) | Inline: claim the business profile, make name/address/phone byte-identical everywhere, and add at least one local directory citation. | [SKIPPED needs "no local/service-area component" reason] | | |

> A worked example of the non-Google half of item 6: in the Czech and Slovak market, Seznam runs its own index with its own webmaster tools and its own submission flow, and a site indexed by Google can be invisible there. Whatever your home market's equivalent is, it belongs in item 6 alongside Google.

**DONE means verifiably live** — URL returning 200, registry listing, event in analytics. Never "written". At gate time every evidence URL (posts, registries, repos) is re-fetched by the gate-carrier itself and must return 200 — fetch log stored in the step folder.

**Blog floor (item 1):** ≥1 post LIVE is a hard floor; between 1 and 2, only via the SKILL.md override mechanism recorded here with the owner's explicit sign-off; 0 live posts = FAIL, no override path. **Item 4:** announce-post URL (fetched, 200) + ≥1 capture event are UNCONDITIONAL — they never queue; only shares that must go out under the owner's personal identity may land as queue rows.

## Day-0 baseline

**Location:** [path in `P5-Activation.S1-Launch/` — the single day-0 snapshot; P6.S2 owns all recurring reads]

## Owner-gated items → queues

[Community posts under the owner's personal identity, account sign-ups, syndication approvals — queue rows with ready artifact paths. Zero "drafted, awaiting" items outside the queues.]

| Queue | Rows added | Ready artifact paths |
|---|---|---|
| media-queue | [N] | [...] |
| manual-queue | [N] | [...] |

## INDEX — step folder `P5-Activation.S1-Launch/`

| File | So what |
|---|---|
| [submission log / published URL list] | [...] |

---

## Honest-assessment note

- [ ] Earns its keep — stream has a web surface or content motion
- [ ] Performative — deck-only stream, no web/content motion: skip recorded in brief.md

## Checkpoint

- [ ] Launched: [N] posts, MCP [shipped/skipped], skill [shipped/skipped], magnet distributed, local identity [shipped/skipped]
- [ ] [M] items in queues for the owner
- [ ] Links (P5.S2) next — backlinks + internal mesh

## Validation loop

- [ ] `/critical` run — findings: [...] — **CRITICAL SCORE: [X]/10** — advisory; the gate is the def-of-success PASS/FAIL checklist
- [ ] Def-of-success (from the stage file): [each criterion — met/unmet]
- [ ] Improvement loops run (if gate failed): [N — what changed each round]
- [ ] Revised — what changed: [...]
- [ ] **Owner approved** — [date] [overrides, if any]
