# Pitfalls catalog

Failure modes this skill watches for, with the canonical fix per pitfall. Reach for this when a stage feels off, or when the user is pushing for a shortcut that pattern-matches to a known death spiral.

Money in the examples below is written `{currency}` — substitute the currency declared once at P1.S1. Brand names in the examples are fictional.

---

## Sequencing pitfalls

### Naming before problem-understanding
**Symptom:** user wants to lock the name in P1.S2. "I'm calling it Velocity12, let's go."
**Why it fails:** the name anchors thinking. Every subsequent stage reverse-engineers to fit the label.
**Fix:** force P1.S2–P1.S6 first. Treat the working name as a placeholder. Naming sits at P1.S7 by design.

### Pricing before willingness-to-pay evidence
**Symptom:** "Let's price the Standard tier at `{currency}`4,900." No data behind it.
**Why it fails:** Ramanujam's Minivation (underpricing into bankruptcy) or Feature Shock (priced for features the buyer doesn't value).
**Fix:** require cited willingness-to-pay evidence before pricing locks — reservation-price asks on named accounts (`accounts.md`), anchor benchmarks for the closest alternative, P1.S4 prediction indicators, and 10+ Van Westendorp surveys for volume offers. Flag the launch price as a *hypothesis*, not a decision.

### GTM before ICP
**Symptom:** user wants to talk LinkedIn ad strategy in P1.S3.
**Why it fails:** channels chosen without ICP almost always miss. Series-A SaaS CTOs in your home market are not on TikTok.
**Fix:** ICP locks first. Channels derive from ICP behavior, not channel familiarity.

### Format before GTM
**Symptom:** "I'll build a landing page" decided in P1.S2.
**Why it fails:** if the clients motion is 1:1 demos to named accounts, a landing page is wasted effort. Format follows the motion.
**Fix:** asset spec (P4.S2) derives from the clients motion (P3.S1); GTM (P6.S1) later locks channels from the real reply + activation data.

### Execute before validation
**Symptom:** "Let's just launch and see what happens."
**Why it fails:** the most common stream-death pattern. Burn capital on a hypothesis no one validated.
**Fix:** P2.S4 validation gate. Pre-commit kill criteria. Minimum evidence to execute (N LOIs / pilots / pre-sales).

---

## Evidence pitfalls

### Uncited numbers
**Symptom:** "TAM is `{currency}`50M." Where did that come from?
**Why it fails:** wishful thinking accumulates across the stream. By P2.S4 the financial forecast is fiction.
**Fix:** every number gets `[source: ...]` or `[assumption — validation: ...]`. No exceptions. Skill flags bare numbers and re-prompts.

### Personas instead of evidence
**Symptom:** "Our customer is a 35-45 year old VP Eng at a Series B." Composite, not real.
**Why it fails:** personas are a shortcut for not gathering evidence. They feel rigorous, are wishful.
**Fix:** every ICP claim cites its evidence — named accounts in `accounts.md`, real conversations, P1.S4 prediction indicators, benchmark data. A composite with no cited source behind it is fiction; kick it back to P1.S3.

### "What they say they want" ≠ "what they actually pay for"
**Symptom:** "Customers told me they want X." But none of them paid for X when X existed.
**Why it fails:** stated preference and revealed preference diverge wildly.
**Fix:** weight revealed preference — what they bought, paid, renewed, searched for (cited from accounts, prediction data, benchmarks) — over stated interest. "They said they'd love it" is a `[assumption]`, not evidence.

### Sample size of 1
**Symptom:** "One prospect at a large enterprise said they'd pay `{currency}`6,900 for this." Locks pricing.
**Why it fails:** n=1 is anecdote, not evidence. That one prospect may be an outlier (over- or under-payer), or may simply have been being polite.
**Fix:** multiple independent evidence points — several named-account reactions, anchor benchmarks, prediction indicators — before any pricing hypothesis locks. 10+ for Van Westendorp.

### Metric-definition drift in published numbers
**Symptom:** "120+ attendees per event" in the data registry, the deck and the offer. The figure is real, but it counts approved registrations; the median actually in the room was far lower.
**Why it fails:** the number is true under one definition and false under the one the reader assumes. Once it becomes a guarantee in an offer, the first delivery breaks it.
**Fix:** every published metric names its definition (registered / approved / attended; booked / held). Every guarantee is backtested against history ("held in N of M") before it enters copy — P1.S6 owns the check.

### Productizing internal assets without an audit
**Symptom:** "We already run this, let's just publish/sell it."
**Why it fails:** internal tooling carries real names, IDs and PII in committed files, is single-tenant (hardcoded people, one account), has no analytics, and is load-bearing for live operations.
**Fix:** P1.S1 `ASSET-AUDIT.md` (inventory, publishability, measured numbers, sanitization grep, freeze windows); P5.S1 runs the grep before every publication.

---

## Strategy pitfalls

### "Everyone is the ICP"
**Symptom:** "It's for any tech company that wants to grow." No exclusions.
**Why it fails:** you can't position for everyone. Exclusion is a feature.
**Fix:** P1.S3 forces naming 2–3 adjacent segments you're walking away from.

### Competition is "do nothing"
**Symptom:** "We don't have real competitors."
**Why it fails:** "do nothing" + "internal hack" are competitors. Dunford step 1 forces you to list them.
**Fix:** include status quo, DIY alternatives, and adjacent tools the customer is already using.

### Category miscategorization
**Symptom:** positioning a leadership-coaching offer as a "SaaS platform" because the deck has a dashboard.
**Why it fails:** wrong category = wrong frame of reference = wrong comparison set = lost deals.
**Fix:** Dunford step 5 explicitly. Pick the category that makes you look strongest.

### Differentiator that's table stakes
**Symptom:** "We're differentiated by quality" / "by speed" / "by service."
**Why it fails:** everyone claims these. If your top competitor could claim the same line, it's not a differentiator.
**Fix:** swap labels test. If your positioning works with the competitor's name in it, re-do the unique attributes step.

---

## Naming pitfalls

### Cute name, no ICP comprehension
**Symptom:** user picks a clever name the target buyer can't decode.
**Why it fails:** every sales conversation starts with "what is that?" — wastes the opening 30 seconds.
**Fix:** name candidates tested against "what would a buyer assume this is?" If the answer isn't close to the actual offer, drop the name.

### Name competing with existing brand
**Symptom:** "I'll call it 'Northwind Performance' — close to the parent brand, Northwind."
**Why it fails:** dilutes the parent brand or steals SEO from it.
**Fix:** clear sub-brand convention (e.g., "Northwind Velocity12" — parent brand first, sub-brand second) OR a distinct standalone name. No middle ground.

---

## Pricing pitfalls

### Pricing model copied from a competitor with different unit economics
**Symptom:** "Datadog uses per-host pricing, let's do per-host pricing."
**Why it fails:** copying the model without copying the cost structure = different margins, different scalability.
**Fix:** value metric chosen from the customer's outcome (the enabled value from P1.S6), not competitor lift.

### Tier structure with arbitrary feature gates
**Symptom:** Standard has 5 features, Plus has 7, Premium has 10.
**Why it fails:** customers reverse-engineer to the cheapest tier that has the one feature they need.
**Fix:** tiers gated by *value metric* (seats, usage, outcome) not arbitrary features.

### Anchor price set by gut
**Symptom:** "Feels like `{currency}`4,900."
**Why it fails:** gut is a starting point, not a decision. Van Westendorp catches the gut number being miles off.
**Fix:** gut number = hypothesis. Van Westendorp = validation.

---

## GTM pitfalls

### "We'll do content marketing"
**Symptom:** vague channel commitment.
**Why it fails:** "content marketing" isn't a channel. LinkedIn posts targeting CTOs is. A weekly newsletter to 2,000 members of a community you own is.
**Fix:** specificity gate — every channel gets named distribution, named audience, named cadence, named metric.

### First 10 accounts unnamed
**Symptom:** "We'll target Series A SaaS CTOs."
**Why it fails:** if you can't name 10, the ICP is too vague or you don't have distribution.
**Fix:** list 10 actual companies with the buyer role per account before locking P1.S3.

### Lead with product, not shift
**Symptom:** Raskin narrative starts with "Our product does X."
**Why it fails:** product-first selling lands flat. The shift is what makes the buyer pay attention.
**Fix:** Raskin act 1 = shift, not product. Product appears in act 4.

---

## KPI pitfalls

### Vanity KPIs as success metric
**Symptom:** "Goal: 10,000 newsletter signups."
**Why it fails:** signups don't pay rent. If signups go up but revenue doesn't, what changed?
**Fix:** vanity check — for every metric, "if this moves and revenue doesn't, do I care?" If no, drop it.

### Too many KPIs
**Symptom:** dashboard with 20 metrics.
**Why it fails:** if everything matters, nothing does.
**Fix:** one north-star + 3–5 leading + 2 lagging. No more.

### Leading indicators that don't actually lead
**Symptom:** "social engagement" listed as leading indicator of revenue.
**Why it fails:** social engagement and revenue correlate weakly at best.
**Fix:** every leading indicator passes a "would a 50% move here predict a revenue move in 60 days?" test.

---

## Budget pitfalls

### Forecasts that only model success
**Symptom:** 12-month plan assumes 80% conversion + 95% retention.
**Why it fails:** doesn't survive contact with reality. P2.S1 (economics) specifically asks for 50% / 25% scenarios.
**Fix:** force 3 scenarios (target / 50% / 25%). Define the floor where you shut down.

### CAC ignored
**Symptom:** revenue forecast without acquisition cost line.
**Why it fails:** can't tell if the stream is fundable. `{currency}`100K revenue with `{currency}`200K CAC isn't a stream, it's a charity.
**Fix:** unit economics required: CAC, LTV, payback. Cited or flagged as assumption.

### "Hidden" costs
**Symptom:** budget shows `{currency}`5K/month run-rate but ignores the founder's time at `{currency}`X/hr.
**Why it fails:** undercounts cost; stream looks profitable when it isn't.
**Fix:** include opportunity cost of founder/operator time at market rate.

---

## Validation pitfalls

### Kill criteria set in retrospect
**Symptom:** stream missing targets at month 6, user wants to keep going. "Let's give it more time."
**Why it fails:** moving goalposts. Sunk cost fallacy.
**Fix:** pre-commit kill criteria at P2.S4, before execution. Re-reading at month 6 is non-negotiable.

### Validation experiment that can't fail
**Symptom:** "Run 5 sales calls and see if anyone's interested."
**Why it fails:** "interest" is uncountable. Any answer can be spun as positive.
**Fix:** binary threshold. "If 0/5 sign LOIs at `{currency}`X by [date], kill."

### Pre-mortem that's polite
**Symptom:** "Three ways this might struggle..." — soft language.
**Why it fails:** softness defeats the purpose.
**Fix:** "Three ways this DIES in year one." Uncomfortable framing required.

---

## Brief pitfalls

### Brief as wishlist
**Symptom:** brief lists features that don't exist, metrics not measured, customers not interviewed.
**Why it fails:** fiction that the team will treat as plan.
**Fix:** brief must trace every claim back to a prior stage's evidence. If it doesn't, re-run that stage.

### Brief too long
**Symptom:** 8-page brief.
**Why it fails:** doesn't get re-read. Becomes another dead doc in the wiki.
**Fix:** 1–2 pages max printed. Lean Canvas + Raskin + pricing card + 90-day plan.

### Brief with no kill criteria
**Symptom:** brief has goals, no anti-goals.
**Why it fails:** can't tell when to stop.
**Fix:** validation milestones from P2.S4 are mandatory section in the brief.

---

## Meta pitfalls (using the skill itself)

### Ritualistic stage completion
**Symptom:** filling every template field "because the skill said so."
**Why it fails:** time wasted on stages that don't apply.
**Fix:** honor the honest-assessment frame at each stage. "Performative when X" = skip with one line stating why.

### Skill becomes a task-board replacement
**Symptom:** stream folder used as a project tracker, not a design artifact.
**Why it fails:** scope creep. Skill is for *designing* the stream, not running it.
**Fix:** post-P6.S3, the brief.md gets handed to whatever runs your projects (`queues/` by default, or your task board if you have one); the queues carry the ongoing motion. Stream folder is an archive.

### Re-running the skill instead of running the experiments
**Symptom:** user re-opens skill on the same stream, tinkers with stages instead of doing validation experiments.
**Why it fails:** infinite design loop, zero validation.
**Fix:** if validation experiments are open, the skill blocks re-runs of earlier stages until experiments resolve.
