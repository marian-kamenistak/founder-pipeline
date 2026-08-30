# Signals & scoring reference — intent signals, lead qualification, intro-call debrief

Used by P3.S1 (outreach) and P6.S1 (GTM input scoring). Adapted from the GTM Engine skill suite (github.com/himanshusaleria/gtm-engine, MIT) — the original's CRM-specific and daily-ritual machinery stripped; the pipeline system of record stays whichever CRM the house stack declared at P1.S1 (Attio, in the worked example) plus the lead log, cadence stays weekly.

**Fit with the house rule:** "Cold outreach without a warm channel doesn't work. Period." A live intent signal IS a warm channel — it's why you're reaching out NOW, and the opener says so. Signal-less volume sends stay banned; this file makes every send signal-justified or warm-path-justified.

---

## 1. Intent signal map — when to reach out, and with what opener

**What:** observable buyer behavior that says the problem is live. Prioritize accounts by signal, time the touch to the signal, open WITH the signal.

**Six signal types** (concrete indicators per stream get defined in P3.S1, question 3):

| Type | Example indicators (eng-leadership flavored) | Where |
|---|---|---|
| Hiring | VP Eng / Head of Eng / first-EM job posts; "we're doubling the team" | LinkedIn Jobs, careers page |
| Org/tech change | New CTO/VPE arrived, reorg announced, replatform, funding round | LinkedIn, news, funding trackers |
| Content consumption | Engaged with your post/newsletter/calculator; attended your talk | LinkedIn, your product-analytics tool, event lists |
| Event/community | Showed up in a leadership community, conference, meetup | Attendee lists, Slack/Discord |
| Competitive | Publicly evaluating coaches/programs, asking peers for recs | LinkedIn threads, communities |
| Pain trigger | Attrition wave, failed release, layoff aftermath, founder posting about scaling pain | LinkedIn, HN, Glassdoor, news |

**Strength tiers:** Strong = directly indicates the live problem (hiring the role, fresh pain trigger, asked for recs). Medium = adjacent (funding, event attendance, competitor content). Weak = generic interest (a like, a follow) — nurture list, never an outreach trigger.

**Rules that make it work:**
- **Combinations beat singles.** Hiring + pain trigger = highest intent. One weak signal = noise.
- **Freshness windows:** hiring signals valid ~30 days, pain triggers ~14 `[operating assumption — tighten or loosen once you have your own reply-rate data by signal age]`. Stale signal = cold send in disguise.
- **Act on strong signals within 48h** — that's when the problem is top-of-mind.
- **ICP check before signal chase.** Strong signal on a non-ICP account is still a waste.
- **Never waste a signal on a generic message.** The signal is the opener: *"Saw you're hiring your first EMs after the Series B — that transition is exactly where I spend my mentoring hours. Worth 15 minutes?"*
- **Detection fits the ≤4h/week budget:** one weekly sweep (LinkedIn saved searches, alerting on named accounts, community skim) feeding the weekly scorecard — not a daily ritual.

**P3.S1 wiring:** a fresh Strong signal bumps an account into Wave 1 regardless of segment; the signal gets logged on the CRM record / lead-log row so the learn gate can test "signal-triggered vs. not" reply rates.

---

## 2. Lead qualification — BANT × words-vs-actions

**What:** two 12-point scores per lead after any real conversation. BANT says whether the deal is real; the commitment scorecard says whether their ACTIONS back their words. Score both in 60 seconds post-call, record on the CRM record (and the lead-log row's stage decision).

**BANT — each factor 1-3:**

| Factor | 3 | 2 | 1 |
|---|---|---|---|
| Budget | Allocated or quantified willingness to pay | Exists in theory; cost of problem understood | "We'd need to figure that out" |
| Authority | Decision-maker engaged, buying process clear | Champion only, DM not yet in | Evaluator with no authority |
| Need | Pain acknowledged AND quantified, actively seeking | Acknowledged, unquantified, "nice to fix" | Mild interest, no articulated problem |
| Timeline | Date + consequence named ("before the reorg lands") | "Next few months", no forcing function | "Sometime" / no urgency |

**Never ask BANT questions directly.** Surface indirectly: "How are you handling this today, what does it cost you?" (B+N) / "If this looked like a fit, who else would weigh in?" (A) / "What's driving the timing?" (T).

**Commitment scorecard — actions over words, each dimension 1-3** (1 = no signal, 2 = said the right things, 3 = demonstrated action):

| Dimension | 3 looks like |
|---|---|
| Engagement | Same-day replies, shows up, brings colleagues |
| Problem acknowledgment | Shares data, states the cost in their own words |
| Timeline | Specific date tied to a business event |
| Resource commitment | Intros the decision-maker, allocates eval time, talks budget |

**Bands (either score):** 10-12 = hot, push next step now. 7-9 = promising — elevate the LOWEST factor next touch, that's the whole follow-up plan. 5-6 = qualify harder. <5 = nurture or drop; below 5 two weeks running = out of the active pipeline.

**Rules:** every 2-3 needs one line of written evidence — no evidence, lower the score. Enthusiasm without action is a 2, never a 3. Rescore weekly (fold it into whatever weekly review your scheduler already runs — cron, CI, or a task queue). A CRM stage ahead of the behavioral score = inflated deal, pull it back.

---

## 3. Intro-call debrief — 10-minute post-call checklist

**When:** after every intro/discovery call with a mentee, partner, or B2B buyer (transcript or memory).

1. **Scores:** BANT /12 + commitment /12, one-line evidence each (Section 2).
2. **Words-vs-actions gaps:** where did polite words outrun behavior? Those claims are `[assumption]`, not evidence — this feeds P6.S1's channel lock.
3. **Buyer readiness type → response mode** (diagnose, then match the move):

| Type | Tell | Your move |
|---|---|---|
| Emotionally ready | Feels the pain, vivid language | Quantify — get THEM to say the number out loud |
| Intellectually ready | Systems-level understanding | Don't educate (condescending) — elevate to business consequences |
| Champion, can't close alone | Convinced, deal stuck internally | Stop selling to them — arm them with the DM-ready narrative |
| Aware, no urgency | "Someday we should" | Tie the gap to a recent, costly, specific consequence |
| Curious, not pained | Interested in the idea, no operational pain | Qualify out gracefully; park as community relationship |

4. **Org selling window:** Unaware → Annoyed → **Hurting (the sweet spot)** → Desperate (bake-off, late) → Solved (rip-and-replace, skip). Sell actively only to Hurting; nurture Annoyed; don't do missionary work on Unaware.
5. **Discovery quality:** did they quantify their own cost? Any "you'd have to ask X for that number" moment = a stakeholder-expansion lever, flag it. Where did I pitch instead of asking the consequence question?
6. **One next action** that raises the lowest-scoring factor — into the lead log / the CRM's `next-action` field, done.

**Pitfall:** happy ears. "They seemed really interested" is not a score. If the debrief produces no 3-with-evidence anywhere, the call was polite, not promising.
