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

You get the founder skill plus 21 specialist skills it calls when they are present (critic, prediction,
pricing, offers, voice, SEO, launch…).

```bash
claude plugin marketplace add marian-kamenistak/founder-pipeline
claude plugin install founder-pipeline@founder-pipeline
claude plugin list            # founder-pipeline should be listed and enabled
```

Start it with `/founder-pipeline:founder`, or `/founder-pipeline:founder <idea> smoke` for the 48-hour
smoke test.

### B. Only the founder skill

Use this if you already have your own critic, voice or SEO skills, or want the smallest footprint.

```bash
git clone https://github.com/marian-kamenistak/founder-pipeline.git
cp -r founder-pipeline/plugins/founder-pipeline/skills/founder ~/.claude/skills/founder
```

Start it with `/founder`. Each skill call in the pipeline resolves in this order: a bundled skill, then
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

**If you connect only one thing, connect DataForSEO.** It is the one tool whose absence marks the most
criteria `BLOCKED`, because nothing else gives the early steps measured demand. The skill never makes up
a search volume to fill the gap.

What happens without each tool is listed in the **Tools** table of
`references/capabilities.md`. The rule is always the same: MCP, then the vendor's REST
API with your credentials, then `BLOCKED` with a backfill row in `queues/manual-queue.md`.

---

## 3. Models

The skill names **tiers**, never model names, so it doesn't go stale when new models ship. Each step
and subagent runs at one of four tiers (full map in `references/engine-routing.md`). As of
November 2026, the Claude mapping is:

| Tier | Used for | Claude model (Nov 2026) |
|---|---|---|
| **PEAK** | the main loop, both kill passes, every final verify and refutation critic, prediction synthesis, every customer-facing word | Fable 5.1 |
| **HIGH** | critical passes on money gates (P1.S6, P2.S1), pricing judgment, the persuasion pass | Opus 5.5 |
| **MID** | drafting over provided context, routine judges, launch subagents, the deck build | Sonnet 5.5 |
| **CHEAP** | research gathering fan-outs: sizing, competitor scouts, enrichment, SERP checks, queue sweeps | Haiku 5.5 |

On a smaller plan you can run everything at MID, except for one rule: **critics and customer-facing copy
never drop below HIGH.** A weak critic approves things it should reject, and that costs more than the
tokens you saved.

---

## 4. Check it works

```bash
mkdir -p ~/ideas && cd ~/ideas && claude
> /founder-pipeline:founder        # or /founder for install B
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
