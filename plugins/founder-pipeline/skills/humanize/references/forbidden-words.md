# Forbidden words — the baseline list

Canonical source of truth for this skill. It exists because of a repeatable failure: a word ban set
by the owner, agreed by everyone, and enforced by nobody. One site audit found a ban set months
earlier broken **219 times across 84 live pages**. A rule with no automated check decays quietly,
and the copy drifts back to machine vocabulary one page at a time.

Two tiers, because they need different enforcement:

- **Tier 1 — BANNED. Zero tolerance.** No instance survives on a published page. These have no
  legitimate use in the register this skill is protecting; every occurrence is either machine
  vocabulary or a content-mill reflex. A single hit is a defect.
- **Tier 2 — BUDGETED. Justify or cut.** Real words with real uses that AI overproduces. These warn
  rather than fail, and the writer must be able to say why each one earned its place.

**Make this list executable.** Keep a machine-readable mirror (one JSON array per tier plus an
exception map) wherever your site-health or CI check runs, scoped to page content a reader actually
sees — inside `<main>`, chrome and code stripped. This file is the source; the mirror is a mirror.
Change both or neither.

---

## Tier 1 — BANNED (zero on any page)

### The owner's own bans

Owner-specific bans go here, each with a reason and the date it was set, so a future writer can tell
a considered rule from a stale one. Worked example of the row format:

| word | why |
|---|---|
| actually | Filler in ~90% of its uses and a hedge in the rest. Banned outright. Ban the equivalent in every language the brand publishes in, or it walks straight back in through the translation. |

### AI vocabulary

delve · tapestry · testament to · pivotal · meticulous / meticulously · realm · underscore(s) ·
showcase · vibrant · transformative · game-changer · synergy · multifaceted · holistic · unleash ·
foster (verb) · garner · boasts · commendable · paradigm · myriad · plethora · utilize · facilitate ·
streamline

### Openers and closers

"In today's…" · "In an era where…" · "Have you ever wondered" · "Picture this" · "Let me share" ·
"I'm excited to announce" · "It's no secret that" · "In conclusion" · "At the end of the day" ·
"the key takeaway" · "I'd love to hear your thoughts" · "What strategies have worked for you?"

### Performed candour

"Here's the thing" · "The truth is" · "I'll be honest" · "Let's be honest" · "Look," (as an opener)

### Copula dodge

serves as · stands as · functions as · boasts

### Stock collocations

vibrant community · invaluable insights · actionable takeaways · meaningful impact · fast-paced ·
ever-evolving · cutting-edge · best-in-class · world-class · state-of-the-art · move the needle ·
low-hanging fruit · seamless experience

### Pipeline tics

"not vibes" / "not a vibe" — `SKILL.md` names "Specifics, not vibes" as a known generator tic. It
turned up on five pages of a single site in one audit, which is what a generator tic looks like from
the outside: never once, always a handful.

Add your own as you find them. The signal is repetition across pieces that no human would sustain.

---

## Tier 2 — BUDGETED (warn; justify each)

### Categorical absolutes

never · always · every · nobody · everyone · none

The rule bans these **with one exception: an absolute survives when it is literally verifiable — a
cap, a contract term, a seat count.** That exception is why they sit in Tier 2 and not Tier 1. A
regex cannot tell "I cap my 1:1s at 14" (verifiable, keep) from "every leader knows" (slop, cut).
One site audit had 437 live instances, and a large share were load-bearing voice — a repeated
"Nobody handed you the team. Nobody handed you the mandate." is doing rhetorical work, not padding.
Enforcing zero would flatten the writing the list exists to protect.

**Use probability words instead when the absolute is not verifiable:** most, usually, rarely, tends
to, hard to.

### Soft AI vocabulary

crucial · robust · leverage (as a verb) · harness · elevate · empower · unlock · navigate
(metaphorical) · comprehensive · nuanced · landscape (abstract) · underscore · in order to ·
prior to · commence · approximately

---

## NOT forbidden — do not "fix" these

- **Words the author's own corpus attests.** If a flagged word appears repeatedly in the author's
  verified hand-written writing, it is voice, not machine vocabulary — record it in
  `voice-fingerprint.md` and exempt it here. The shipped worked example is *seamlessly*: attested
  several times in one author's hand-written corpus, so it stays on its own, while the collocation
  "seamless experience" remains Tier 1.
- **Rule of three, aphorism ladders, cleft contrasts** — genuine style for many authors. Check the
  fingerprint before treating them as tells.
- **Third-party quotes.** Testimonials are somebody else's words. If a customer wrote "actually", it
  stays. The automated check must scope around quoted blocks, and a human fixing a page must never
  edit inside a quoted value.
- **Code comments, structured data, alt text, meta titles.** The rule is about page content a reader
  sees.
- **Factual records.** The title of a talk that was delivered, an event name, a company name, a book
  title. These record what happened; editing them falsifies the record. Worked example: a speaker
  page listing a real past talk called "Product & Engineering Synergy" keeps that title even though
  *synergy* is Tier 1. Rewrite the copy *around* a record, never the record.

  Enforce this with a scoped exception map in the mirror (`"/speaker/": ["synergy"]`). Use it ONLY
  for a documented non-target like that one, never for copy you simply do not want to fix — a check
  that can never go green is a check people stop reading.
- **A banned phrase used literally rather than rhetorically.** "At the end of the day" is banned as a
  closer; "work you can put down at the end of the day" is a time of day. The automated check cannot
  tell these apart and will flag the literal use. Reword yours rather than weakening the list, but do
  not read the flag as proof the sentence was bad.

---

## How to fix a hit

Never delete the flagged word and ship the same sentence — `SKILL.md` is explicit that word swaps on
an unchanged sentence read worse than the original. Rewrite the sentence around the idea. Most
"actually" hits are pure filler and the sentence is stronger with it simply gone ("what the role
actually owns" → "what the role owns"); where it was carrying emphasis, rebuild the emphasis with
structure instead.
