# Install and connect

The founder skill runs on **Claude Code alone**. Everything else on this page is an upgrade: each
connection you add swaps an inline fallback for a measured source or a specialist skill. You can start
with nothing connected and add things as the run reaches the steps that need them. The skill tells you
when that is: its first step writes a `CAPABILITIES.md` into your idea's folder, listing what it found
and the one missing item that costs you the most evidence.

What each thing costs is in **[TOOLING-AND-COSTS.md](https://github.com/marian-kamenistak/founder-pipeline/blob/main/docs/TOOLING-AND-COSTS.md)**. This page covers how to
connect them.

---

## 1. Pick an install

### A. The whole plugin (recommended)

You get the founder skill plus 22 specialist skills it calls when they are present (critic, prediction,
pricing, offers, voice, SEO, launch…), and the parts a skill folder cannot carry: four subagents (gate
critic, claim refuter, completeness critic, evidence scout), two workflows (`gather-verify`,
`judge-panel`) and one hook that asks you before any step is marked `approved`.

```bash
claude plugin marketplace add marian-kamenistak/founder-pipeline
claude plugin install founder-pipeline@founder-pipeline
claude plugin list            # founder-pipeline should be listed and enabled
```

Start it with `/founder-pipeline:founder <your idea in one sentence>`. For the 48-hour smoke test, the
recommended first run, type `/founder-pipeline:founder <idea> smoke`.

### B. Only the founder skill

Use this if you already have your own critic, voice or SEO skills, or want the smallest footprint.

```bash
git clone https://github.com/marian-kamenistak/founder-pipeline.git
mkdir -p ~/.claude/skills
cp -r founder-pipeline/plugins/founder-pipeline/skills/founder ~/.claude/skills/founder
```

Start it with `/founder`. This install has no subagents, workflows or hook; the skill runs the same
roles as generic subagents and the gates do not change. Each skill call in the pipeline resolves in this order: a bundled skill, then
any skill of yours with the same name, then the inline fallback card in
`references/capabilities.md`. Your own `/critical` or voice skill is picked up automatically.

If you want only some of the specialist skills, copy just those folders:

```bash
cp -r founder-pipeline/plugins/founder-pipeline/skills/{critical,pricing,prediction} ~/.claude/skills/
```

### C. Another agent harness (Codex, Cursor, others)

Point the harness's rules or skills file at this folder's `SKILL.md`. The skill reads one stage file
at a time from `stages/`, so keep the folder structure intact. Subagent fan-out and the model-tier
routing assume a harness that can spawn subagents. Without that, run fan-outs serially; the gates
don't change.

---

## 2. Connect tools (all optional)

Each tool below takes one command. Credentials go in environment variables, never in a file you commit.
After connecting, run `claude mcp list` to check it shows as connected, then tell the skill to re-run
its preflight. It updates `CAPABILITIES.md` and lists the `BLOCKED` criteria it can now backfill.

| Connect | Unlocks | Command |
|---|---|---|
| **DataForSEO** (keyword volume, SERP, rankings, backlinks, WHOIS) | P1.S4 demand data, P1.S5 competitor quant + backlink gap, P1.S7 domain check, P4.S1 keyword contract, P4.S4, P5.S1 day-0 baseline, P6.S2 rank reads | `claude mcp add dataforseo -e DATAFORSEO_USERNAME=$DATAFORSEO_USERNAME -e DATAFORSEO_PASSWORD=$DATAFORSEO_PASSWORD -- npx -y dataforseo-mcp-server` |
| **Firecrawl** (clean page content, raw HTML) | faster research in P1–P3, the P4.S4 competitor HTML teardown | `claude mcp add firecrawl -e FIRECRAWL_API_KEY=$FIRECRAWL_API_KEY -- npx -y firecrawl-mcp` |
| **A CRM** (Attio as the example) | P3.S1 accounts, waves and stages in a real system of record | `claude mcp add --transport http attio https://mcp.attio.com/mcp` (OAuth on first use). Any CRM with an MCP server or REST API works. |
| **Product analytics** (PostHog as the example) | P3.S1 UTMs, P4.S3 event wiring, P6.S2 KPI reads | `claude mcp add --transport http posthog https://mcp.posthog.com/mcp` (OAuth). Optional: PostHog's Claude Code plugin for its `posthog:*` skills. |
| **Task board** (Notion as the example) | P5.S3 and P6.S3 mirror the owner-action queue onto a board | `claude mcp add --transport http notion https://mcp.notion.com/mcp` (OAuth) |
| **Gmail, Google Calendar, Google Sheets** | P3.S1 messages staged as drafts, P1.S6/P2.S1 real calendar capacity, P2.S1 live scenario model | Connect them as connectors in your claude.ai settings. Claude Code picks them up when you're signed in with the same account. |
| **Cloudflare** (DNS, deploys) | P4.S0 mail DNS records, P4.S3 deploy | `npm i -g wrangler && wrangler login`. Optional: Cloudflare's own Claude Code plugin. |

Prefer a file to five commands? Copy [`examples/mcp.json`](https://github.com/marian-kamenistak/founder-pipeline/blob/main/examples/mcp.json)
into your project as `.mcp.json`, delete the servers you don't use, and export the two environment
variables it names. The plugin does not ship an `.mcp.json` of its own on purpose: a bundled server
would start for every user, including the ones with no account for it.

**If you connect only one thing, connect DataForSEO.** It is the one tool whose absence marks the most
criteria `BLOCKED`, because nothing else gives the early steps measured demand. The skill never makes up
a search volume to fill the gap.

What happens without each tool is listed in the **Tools** table of
`references/capabilities.md`. The rule is always the same: MCP, then the vendor's REST
API with your credentials, then `BLOCKED` with a backfill row in `queues/manual-queue.md`.

---

## 3. Models

The skill's own files name **tiers**, never models, so they don't go stale when a model ships. This
page is the one place that maps tiers to model names. Each stage file states its tiers on its
`Routing:` line (full map in `references/engine-routing.md`). As of November 2026, the Claude mapping
is:

| Tier | Used for | Claude model (Nov 2026) |
|---|---|---|
| **PEAK** | the main loop, both kill passes, every final verify and refutation critic, prediction synthesis, every customer-facing word | Fable 5.2 |
| **HIGH** | critical passes on money gates (P1.S6, P2.S1), pricing judgment, the persuasion pass | Opus 5.5 |
| **MID** | drafting over provided context, routine judges, launch subagents, the deck build | Sonnet 5.5 |
| **CHEAP** | research gathering fan-outs: sizing, competitor scouts, enrichment, SERP checks, queue sweeps | Haiku 5.5 |

With the full plugin the tiers are enforced by the agent definitions, not by a prompt: the evidence
scout is pinned to the small model (`model: haiku`), and the three critics inherit the model your
session runs on (`model: inherit`), so they are always as strong as the main loop. The aliases survive
model releases; no file names a dated model ID.

On a smaller plan, PEAK means the best model you have. You can run MID and CHEAP work on something
cheaper. Two things never move: **the main loop does not drop below HIGH, and critics, refuters and
customer-facing copy run on your best model.** A weak critic approves things it should reject, and
that costs more than the tokens you saved. On Claude Pro the top-tier model is billed in credits;
see [TOOLING-AND-COSTS.md](https://github.com/marian-kamenistak/founder-pipeline/blob/main/docs/TOOLING-AND-COSTS.md).

---

## 4. Check it works

```bash
mkdir -p ~/ideas && cd ~/ideas && claude
> /founder-pipeline:founder a paid onboarding checklist for small agencies smoke     # /founder … for install B
```

The first step asks for a parent folder and an idea slug, then runs the capability preflight. You should
see `~/ideas/<slug>/CAPABILITIES.md` with every skill marked `bundled`, `own:<name>` or `fallback`, and
every tool marked `connected`, `REST` or `missing`. Seeing `fallback` and `missing` here is fine; the run
carries on and tells you which gates are waiting on what.

## Update and remove

```bash
claude plugin marketplace update founder-pipeline && claude plugin update founder-pipeline@founder-pipeline
claude plugin uninstall founder-pipeline@founder-pipeline
```

For install B, pull the repo again and re-copy the folder. Your idea folders are yours and are never
touched by an update.

## What the plugin adds to a session

- **Context.** The 23 skill descriptions are the only part that is always loaded: 9,820 characters,
  about 2,455 tokens (estimate at 4 characters per token; measured by `scripts/check_skills.py --report`).
  Everything else loads when a skill runs, one stage file at a time.
- **One hook.** A `PreToolUse` hook on `Write` and `Edit` looks only at files named `PROGRESS.md` that
  carry the pipeline's column header. When an edit adds an `approved` row it asks you to confirm. It never
  blocks, and on any error it lets the edit through. Source: `hooks/approval-guard.mjs`. It needs Node.js
  on the `PATH`; without Node it does nothing and the rule rests on the skill's own instruction.
- **Nothing else runs in the background.** No MCP server, no monitor, no telemetry.
