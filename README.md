# Founder Pipeline

**A business-idea pipeline that argues with you.**

Most tools help you write a plan. This one keeps refusing to let you move on until you've proved
the last thing you said. It walks a new business idea through 25 steps, and at each step it attacks
your own work, checks it against a written list of pass-or-fail rules, and stops dead until you
personally sign it off.

It is allowed to tell you the idea is bad. Three of the steps can kill it outright. That's the point.

---

## Read this first, in plain English

Imagine you want to start something — a service, a product, a side business. The normal thing that
happens is this: you get excited, you write a nice document, the document sounds great, and then
nothing happens. Or worse, you spend six months building it and *then* find out nobody wanted it.

This pipeline is built to stop both of those.

It works like a series of locked doors. Behind door one is "what problem am I solving?" You can't get
to door two until you've answered door one **with evidence** — not a feeling, not a guess, an actual
source you can point at. Then a critic reads your answer and tries to tear it apart. Then *you* have
to look at it and say "yes, this is good enough" out loud.

Only then does door two open.

There are 25 doors. Three of them can be locked forever, meaning: this idea is dead, stop working on
it, go do something else. That sounds harsh. It's the most valuable thing here. Killing a bad idea in
week one saves you the six months.

---

## What actually happens when you run it

You'll type one command, and then have a long conversation. Here's the shape of it:

| Phase | What it does | Steps |
|---|---|---|
| **1. Ideation** | Works out the problem, who has it, whether anyone's searching for a fix, who they'd use instead, and what you'd sell. The **name comes last**, on purpose. | 7 |
| **2. Viability** | Counts the money and the hours. Ends with a verdict: is this worth your time, yes or no? | 4 |
| **3. Clients** | Talk to 10–20 real people. Before you build anything. | 1 |
| **4. Build** | Email, keywords, copy, website, competitor teardown, deck. The slow stuff that pays off later. | 6 |
| **5. Activation** | Actually publish it. A finished website nobody has seen is not a launch. | 4 |
| **6. Adoption** | Pick your channels from real data, pick your numbers, write the 90-day plan. | 3 |

Each step writes one file into a folder for your idea. At the end you have a complete, evidenced
paper trail of every decision and why you made it.

**In a hurry?** There's a 48-hour version. Answer five questions, message ten real people, and see if
three of them will talk to you. If nobody replies, you just saved yourself weeks. That's the
`smoke test`, and it's the recommended way to start.

---

## Installation

### Step 1 — Get Claude Code

If you don't have it, install it first:

```bash
npm install -g @anthropic-ai/claude-code
```

You'll need a **Claude Pro plan or higher** ($17/month billed annually). Claude Code isn't included
in the free tier. [Sign up here.](https://claude.com/pricing)

### Step 2 — Add this repo

In your terminal, run:

```bash
claude plugin marketplace add marian-kamenistak/founder-pipeline
```

This tells Claude Code where to find the plugin. You only do this once.

### Step 3 — Install the plugin

```bash
claude plugin install founder-pipeline@founder-pipeline
```

### Step 4 — Check it worked

```bash
claude plugin list
```

You should see `founder-pipeline` in the list, with a version number and `enabled`.

### Step 5 — Start it

Open Claude Code in whatever folder you want your work saved in, and type:

```
/founder-pipeline:founder
```

It will start asking you questions. Answer them honestly — it's checking your answers against real
data, so a flattering answer just gets caught two steps later.

### Only want the founder skill, or already have your own critic?

The founder skill runs on its own. Copy one folder and it uses whatever you already have installed,
falling back to built-in instructions for anything you don't:

```bash
git clone https://github.com/marian-kamenistak/founder-pipeline.git
cp -r founder-pipeline/plugins/founder-pipeline/skills/founder ~/.claude/skills/founder
```

Then type `/founder`. Its first step writes a `CAPABILITIES.md` into your idea's folder, listing
what it found and the one missing connection that costs you the most evidence.

**Connecting tools** (search data, CRM, analytics, mail, task board) is optional and takes one command
each: **[plugins/founder-pipeline/skills/founder/INSTALL.md](plugins/founder-pipeline/skills/founder/INSTALL.md)**.

---

## Updating it later

```bash
claude plugin marketplace update founder-pipeline
claude plugin update founder-pipeline@founder-pipeline
```

## Removing it

```bash
claude plugin uninstall founder-pipeline@founder-pipeline
```

Nothing you've written is deleted. Your idea folders are yours and stay where they are.

---

## What it costs to run

**Short answer: about $27–37 a month**, most of which is your Claude plan.

Seven of the thirteen tools involved are genuinely free at the scale one person works at — not
trials, actual free plans. Two costs are unavoidable: a Claude plan, and email on your own domain.

| | Per month |
|---|---|
| Bare minimum | **$27 – $37** |
| Comfortable | **$205 – $233** |
| One research run | **$0.66 – $2.02** |

You do **not** need to buy everything before you start. Phases 1 and 2 — the half that decides
whether to build at all — need a Claude plan and one pay-as-you-go API with a $50 deposit that lasts
roughly 200 runs.

Full breakdown, with every price sourced and dated: **[docs/TOOLING-AND-COSTS.md](docs/TOOLING-AND-COSTS.md)**

---

## What you need before you start

**Required:**

- Claude Code, and a Claude Pro plan or higher
- A folder to work in
- About an hour where nobody will interrupt you, for the first session

**Required for the research steps (phase 1 onward):**

- A [DataForSEO](https://dataforseo.com/) account. Pay-as-you-go, $50 minimum deposit, no monthly
  fee. This is what turns "I think people want this" into an actual number. It's the one paid thing
  the early phases genuinely can't fake.

**Only needed if you get as far as building a website (phase 4+):**

- A domain name (~$10/year for a .com)
- A [Cloudflare](https://www.cloudflare.com/) account — free
- [Google Workspace](https://workspace.google.com/) if you want email on your domain — $7/user/month
- [Firecrawl](https://www.firecrawl.dev/), [PostHog](https://posthog.com/),
  [Resend](https://resend.com/) — all have free tiers that are enough

**Optional, and it works fine without them:**

- The [PostHog](https://posthog.com/docs/ai/claude-code) and Notion plugins for Claude Code, if you
  want analytics and task tracking wired in automatically

---

## The rules it won't break

These are the things that make it different from asking a chatbot to write you a business plan.

**Every number has a source.** It will not estimate, round, or invent a figure. If something can't be
measured, it writes "not available" and says why — never a zero, never a blank, because both of those
read like an answer when they aren't.

**It stops for you, every single time.** No step is finished because the AI thinks it looks good. It
finishes when *you* say so. There is no auto-advance and no skipping ahead.

**"Profitable but mediocre" counts as a failure.** If a new idea won't clearly beat the thing you're
already doing, it gets killed rather than kept as a small side project. Small side projects are how
focus dies.

**A funnel that never kills anything is just a tunnel.** If your ideas keep sailing through the early
gates, the gates aren't working. A killed idea is a win — it's months you didn't waste.

**It won't let you name it first.** The name comes at step seven, after you know what the thing
actually is. Naming first is how people fall in love with an idea before checking if it's real.

---

## Frequently asked

**Do I need to be technical?**
No. You need to be able to open a terminal and copy-paste four commands. Everything after that is a
conversation in plain English.

**How long does a full run take?**
It's not one sitting. Expect several sessions over a few weeks, because some steps require you to go
and talk to actual humans and wait for replies. The 48-hour smoke test is a single afternoon plus a
week of waiting.

**Can I skip steps?**
Some, yes — and it tells you which. If you're not building a website, four of the six build steps
skip cleanly. The gates and kill steps never skip.

**What if I disagree with it?**
You can override any failed check. It records that you did, and why. It's a pipeline, not a boss.

**Do I need all the other skills and tools?**
No. Version 0.2 made every one of them optional. Each step uses a bundled skill if it's there, then
your own skill with the same name, then a fallback card that ships inside the founder skill. Missing
search data is the one gap you'll feel: those checks show as `BLOCKED` rather than being filled with
a guess. See [plugins/founder-pipeline/skills/founder/INSTALL.md](plugins/founder-pipeline/skills/founder/INSTALL.md).

**Will it just tell me my idea is great?**
No. It's specifically built not to. If that's what you want, ask a normal chatbot.

---

## What changed

**0.2.0 (2026-11-04)**
- The founder skill runs standalone. Every skill and tool it mentions is optional, resolved at run
  time, with one fallback card per item in `references/capabilities.md`.
- Step 1 opens with a capability preflight that writes `CAPABILITIES.md`.
- New [plugins/founder-pipeline/skills/founder/INSTALL.md](plugins/founder-pipeline/skills/founder/INSTALL.md): three ways to install, one command per tool, and the
  model tiers mapped to current Claude models.
- Ported two months of fixes from the source pipeline: an asset audit for ideas that productize
  something you already run, a promise backtest in the offer step, a sanitization check before
  launch, and search-data calls rewritten for the REST API.

**0.1.0 (2026-08-30)**: first public release.

---

## Licence

MIT. Do what you like with it.

Portions of `signals-and-scoring` are adapted from
[gtm-engine](https://github.com/himanshusaleria/gtm-engine), also MIT.

The frameworks it uses — Lean Canvas, the Value Proposition Canvas, Dunford positioning, the Raskin
narrative, Van Westendorp pricing — belong to their authors and are cited where used.
