# AEO patterns — answer engine optimization

*Reference for `/founder-pipeline:ai-seo`. Written 2026-08-22. In-skill paths are bare; cross-skill paths are rooted at `${CLAUDE_PLUGIN_ROOT}`.*

---

## 1. What AEO is, and what it is not

**AEO's surface is Google's classic SERP** — position 0 (the featured snippet), People Also Asked,
and voice results. It is measured in Google Search Console and in SERP-feature data. That is a real
surface with real traffic and a real measurement path.

**AEO is not AI citation.** Being quoted by ChatGPT, Perplexity or Claude is a different
mechanism with different evidence, and this skill's own evidence base says so out loud: cross-engine
citation overlap is about 17%, and Moz found 88% of AI-Mode citations do not rank in Google's top
10. Optimising for a snippet does not buy you a citation, and the two should never be reported as
one number.

**The one real bridge, and it is worth stating:** pages that already held featured snippets before
AI Overviews rolled out tend to appear in AI Overviews. Google is drawing from a surface it already
built. So snippet work is not wasted on the AI side — it is just not the same work, and it does not
get sold as an AI-citation lever.

Practical consequence: AEO findings go in the classic-SERP section of a report, measured in GSC.
AI-citation findings go in the AI section, measured on your standing AI-visibility cadence (see
`/founder-pipeline:ai-seo` Mode 3 — this plugin does not ship one). Never average them.

---

## 2. The canonical answer capsule rule

**This is the single definition. Every other file in this plugin points here rather than restating
it.** Two sources conflicted — 20–25 words for AI liftability, 40–60 words for featured-snippet
eligibility — and this is the reconciliation, not a compromise:

> The answer capsule is **40–60 words total**, and its **first sentence is self-contained at ≤25
> words**. Sentence 1 is the AI-liftable unit; sentences 2–3 carry the qualifier that makes it
> featured-snippet eligible. Hard cap 60 (paragraph snippets truncate near 320 characters). No
> hyperlinks inside the capsule — source links live in the detail below it.

Why it works as one rule: the two sources were not disagreeing about length, they were describing
two different consumers of the same block. An engine lifting a sentence takes sentence 1. Google's
snippet extractor takes the paragraph. Write one block that serves both.

Placement and shape:

- Directly under the question-shaped heading. Nothing between them — no image, no callout, no
  "before we get into it".
- Answer immediately. No warm-up clause, no restating the question.
- Self-contained. If it needs the paragraph above it to make sense, it is not a capsule.
- The detail, the nuance and the links go **below** it, not inside it.

Grading a page: count words in the block under each question heading, count words in its first
sentence, check for `<a>` inside it. Three mechanical checks.

---

## 3. Snippet type → format map

Google picks the snippet format from the query. Match the format or you are not eligible, however
good the answer is.

| Query shape | Snippet Google returns | What the page must contain |
|---|---|---|
| "what is X", "why does X", "how does X work" | **Paragraph** (~40–60 words, truncates near 320 chars) | The capsule, under a question heading |
| "how to X", "steps to X", "best X", "types of X" | **List** (ordered for process, unordered for sets) | A real `<ol>`/`<ul>`, 5–8 items, each item self-contained and verb-first for process |
| "X vs Y", "X price", "X comparison", "X specifications" | **Table** | A real `<table>` with a header row. 2–4 columns; more gets truncated |
| "X near me", "X hours", "X address" | Local pack, not a snippet | Route to `/founder-pipeline:web-listings` and to a local-SEO pass (not shipped here: `LocalBusiness` schema, NAP consistency, business profile) — nothing on the page wins this |

Two rules that follow:

- **Markup the format, don't fake it.** A list drawn with hyphens in a paragraph is a paragraph. A
  table drawn with CSS grid is not a table.
- **One format per heading.** A capsule followed immediately by a list under the same H2 makes the
  extractor choose, and it often chooses neither.

---

## 4. Question-phrased headings

- **60–70% of H2/H3 on an informational page are question-shaped.** Not 100% — a page that is
  nothing but questions reads as an FAQ dump and loses the narrative that keeps a human on it.
- **Phrase the heading the way the query is typed**, not the way an editor would write it. "How
  much does engineering leadership coaching cost?" beats "Investment". AirOps, 548,534 retrieved
  pages: ≥50% title-word/query overlap gave a 20.1% citation rate against 9.3% below 10% overlap.
- **Answer immediately underneath.** The capsule is the first thing after the heading.
- **No links inside the capsule.** They pull the extractor's attention and they make the block
  non-self-contained.
- Harvest the actual phrasings from `/founder-pipeline:web-keyword`, not from intuition.

---

## 5. Definition pattern

The "what is X" capsule has its own shape. It is fully specified as **Pattern 1** in
`content-patterns.md` — read it there and do not restate it here. The AEO-specific additions:

- The definition must appear **within the first 300 words** for the paragraph snippet, and be
  under a question-shaped or term-shaped heading for PAA.
- Term first, in bold, then "is". `**X** is …` — the extractor keys on the copula.
- Define the page's core term exactly once. A second definition of the same term elsewhere on the
  page competes with the first.

---

## 6. PAA versus fan-out queries

These get conflated constantly, and they are not the same kind of object.

| | People Also Asked | Fan-out queries |
|---|---|---|
| What it is | Questions Google **actually shows** on the SERP | Sub-questions an engine **infers and asks itself** before synthesising an answer |
| Status | Observed data | Inferred. Not directly observable |
| Source | SERP scrape, a rank-data provider's SERP endpoints, the live SERP | Fan-out tooling, or reasoning about what the answer needs |
| Confidence | 🟢 It is on the page | 🟡 At best. It is a model of a model |
| Tooling limit | Works in every market | **US / English only** today. Smaller non-English markets have no fan-out data at all — Czech and Slovak are the worked example |

**Route all harvesting to `/founder-pipeline:web-keyword`.** It owns SERP-feature research including PAA
extraction, and naming fan-out as a research artifact is its job, not this file's. This file only
says what the two things are so a report never labels one as the other.

In a smaller non-English market (Czech and Slovak are the worked example): PAA is available,
fan-out is not. Say so rather than substituting an English fan-out list and calling it research.

---

## 7. Voice and conversational queries

- Voice queries are **long-tail and question-shaped** — who / what / when / where / why / how.
  They map onto the same question headings and capsules, which is why voice does not need its own
  content strategy.
- **The capsule is the voice answer.** Assistants read back roughly a sentence. That is sentence 1
  of the capsule, which is exactly why the ≤25-word constraint is on sentence 1 and not on the block.
- Conversational phrasing beats keyword phrasing here: people speak in full sentences.
- **Anything with a place, an address, opening hours or a phone number is NAP work, not page work.**
  Route it: `/founder-pipeline:web-listings` owns directories and the canonical NAP values; the
  business profile, `LocalBusiness` schema and service×city pages belong to a local-SEO pass this
  plugin does not ship. Nothing in this file wins a "near me" query.

---

## 8. Schema for AEO

**Standing decision, 2026-08-22: FAQPage, HowTo and Speakable ship.** Implement them. This is a
policy call by the site owner, recorded here so no future session re-argues it, and it is carried
in one place — `${CLAUDE_PLUGIN_ROOT}/skills/web-site-creator/references/metadata.md` §8.4 — with
this file and `/founder-pipeline:ai-seo` pointing at it.

| Type | Ship on | How |
|---|---|---|
| `FAQPage` | Any page with a real Q&A block | Mirror the **visible accordion** 1:1. Never a question that isn't on the page |
| `HowTo` | Step-by-step content | Mirror the visible numbered steps |
| `Speakable` | Pages with a clean lead answer | `SpeakableSpecification` with a CSS selector pointing at the capsule |

**The one hard rule that survives the decision:** the markup mirrors visible content, never
replaces it. A visible, server-rendered accordion first; the JSON-LD second. A fact that lives only
in JSON-LD is retrieved by **zero** AI platforms — that is the schema-only-Q&A bug, and it is the
thing to flag on an audit, not the absent markup.

**Dated evidence note, kept for honesty about the tradeoff.** FAQPage rich results ended 7 May
2026; HowTo rich results were removed in 2023. Ahrefs' causal DiD experiment (1,885 pages with
JSON-LD added against ~4,000 matched controls) found no significant lift on AI Overviews, AI Mode
or ChatGPT, and −4.6% specifically on AI Overviews. Google states there is no special structured
data needed for its AI surfaces. So these types are shipped for entity resolution, validator
cleanliness and future-proofing — **not** because a rich result or a citation lift is expected.
Implement them; do not forecast a gain from them.

---

## 9. Fan-out queries, defined

Stated once so the term is usable in a report without ambiguity:

> A **fan-out query** is a sub-question an engine generates and answers internally before
> synthesising the response it shows a user. Ask "which CRM for a 5-person agency" and the engine
> may internally resolve "what CRMs exist", "which are priced for small teams", "which integrate
> with X" before writing one answer.

Consequences for a page:

- The page competes on the **sub-questions**, not only on the query the user typed. A page that
  answers exactly one question loses to a page that resolves three of the engine's five.
- Question headings are how you cover them cheaply: one heading and one capsule per sub-question.
- **Tooling limit: US and English only.** Smaller non-English markets have no fan-out data at all
  — Czech and Slovak are the worked example. In those markets, derive sub-questions from PAA and
  from real customer questions, label them 🟡, and never present an English fan-out list as market
  research.

---

## 10. What AEO will not do

The honest ceiling. State it when scoping, not after.

- **It will not get you cited by an AI engine.** Different surface, different selection mechanism.
  The 17% cross-engine overlap figure is the reason.
- **A featured snippet often costs you the click.** Winning position 0 can reduce clicks for the
  query it wins. Worth it for brand-defining terms, not automatically worth it for everything.
- **It will not beat authority.** Snippets get pulled from pages already ranking on page one for
  the query. Structure is how you win among eligible pages, not how you become eligible.
- **It will not fix an offer problem.** A perfectly capsuled page for a service nobody searches for
  is a well-formatted zero. Validate the query volume first — `/founder-pipeline:web-keyword`.
- **It will not survive a JS-rendered answer.** Extractors and AI crawlers both work on
  server-rendered HTML. If the capsule is injected client-side, it does not exist.
- **It is not measurable per-answer.** GSC shows impressions and position; it does not tell you
  which block Google lifted. Report the input you changed and the position movement, not a causal
  claim about the snippet.

---

## Related

- `content-patterns.md` — the six extractable block templates, including the definition block
- `ai-search-landscape.md` — how each AI platform selects and cites sources
- `${CLAUDE_PLUGIN_ROOT}/skills/web-keyword/SKILL.md` — PAA and fan-out harvesting, keyword validation
- `${CLAUDE_PLUGIN_ROOT}/skills/seo-audit/SKILL.md` — grading a page against these patterns
- `${CLAUDE_PLUGIN_ROOT}/skills/web-site-creator/references/metadata.md` §8.4 — the standing schema decision
