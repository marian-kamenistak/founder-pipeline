# P4.S1 — Keywords & search demand → `P4-Build.S1-Keywords.md`

**Phase: P4-Build** (second step — P4.S0-Email opens the phase; this step no longer needs its own DNS/domain prerequisite since P1.S7 + P4.S0 already cover it)

**Earns its keep when** any content or web asset is planned — which is almost always. Keywords are defined HERE, before a single line of copy exists: the copy step (P4.S2) writes copy *around* this keyword map, and the web step (P4.S3) implements it in meta, headings, and structure. Never the other way round.

**Becomes performative when** the stream is 100% warm-outbound with zero web surface and zero content engine — then record a one-line skip in `brief.md` (skipping P4.S1–S4) and move to P5.S1 (whose own skip rules handle a no-asset stream).

---

## The method lives in `/founder-pipeline:web-keyword`

**Run `/founder-pipeline:web-keyword` in Contract mode (Mode A) for this step.** That skill owns the
keyword contract method end to end — concept seeding, candidate drafting, the localization table, the
live-SERP gate, the no-orphans map, the AI-search question set, and the glossary handoff. It is
the same method this step used to carry inline, extracted so it can also serve existing sites.

Do not re-derive it here. Two copies of a keyword contract drift, and the drift is expensive.

What `/founder-pipeline:web-keyword` covers, so you know what you're getting:
`references/localization.md` (pick the term, don't translate it — candidate drafting, territory
spelling traps, the `[low-volume — brand/AI-search play]` tag), `references/dataforseo-recipes.md`
(endpoints, location table, batching, cost discipline), and `references/audit-mode.md` (not used at
this step — there's no site to audit yet).

**Keyword-data provider.** The recipes are written against the DataForSEO MCP server, which is an
**optional external dependency you configure yourself** — it is not bundled with this plugin. Any
provider that returns real volume, difficulty and trend data works; what the gate below requires is
that every number carries a citation to a real measurement, never an estimate presented as data.
Substitute your provider's endpoint names throughout and record which provider you used.

---

## What is founder-specific and stays here

### Horizon honesty (hard framing)

SEO is a 6-24-month compounder, never the first-revenue engine — only a small minority of newly
published pages reach Google's top-10 inside a year (Ahrefs' two-million-keyword study put it near
6%; treat the 2-6% band as an `[operating assumption]`), and most small consultancy sites produce
zero monthly organic leads (`[operating assumption]` — the working figure here is ~70%; measure your
own market before betting on it). The keyword contract exists so the asset compounds correctly from
day one, NOT because it will bring client #1. Client #1 comes from P3.S1 outreach, which already ran
— this step builds the compounder for clients #5-50.

State this in the step file. A founder reading a keyword contract without it will misread the
timeline and staff against traffic that arrives eighteen months later.

### The seed carry-forward

The contract is SEEDED from P1.S4's carry-forward keyword table (`P1-Ideation.S4-Prediction.md`
names its location) — cite that file; its terms arrive already priced. Feed it to
`/founder-pipeline:web-keyword` as the seed set, along with:

- cited pains from `P1-Ideation.S2-Problem.md` + P1.S4's discourse evidence
- `P1-Ideation.S5-Competition.md` category language
- `P1-Ideation.S6-Offer.md` onliness terms

**Terms already in P1.S4's carry-forward table keep their numbers — cite, don't re-price** — but
only while P1.S4's data is ≤ 90 days old. Older → trigger the SKILL.md loop-back to refresh P1.S4's
table (single ownership preserved), never re-price inline here. Only NEW terms get fresh calls.

### Territory scope — this step owns the locale decision

Name two territories explicitly in the step file before any research runs, and never leave them
implicit:

- **Home market** — the language and country the stream sells in first. Every money page targets
  this locale.
- **Primary export market** — the one additional territory worth building for now. Usually
  English-language, but not always; pick it from where the ICP actually is (P1.S3), not from where
  search volume is largest in the abstract.

Anything beyond those two is a later decision, not this step's. Pass the locked list to
`/founder-pipeline:web-keyword`; it handles the per-territory candidate comparison.

**The non-English trap this exists to catch (worked example: a Czech home market).** Search demand
in a smaller-language market rarely maps onto the English term you started from. Three failure modes
that repeat across such markets:

- **The literal translation nobody types.** The dictionary-correct rendering of the English category
  term often has near-zero volume while a borrowed English word, a colloquialism, or a completely
  different framing carries the demand. Comparing candidates by measured volume is the only way to
  tell — intuition, including a native speaker's, is wrong often enough to matter.
- **A non-Google engine holds real share.** In the Czech market, Seznam.cz still takes a meaningful
  slice of queries, with its own index, its own webmaster tools (and its own submission surface at
  P5.S1) and its own ranking behaviour. Other markets have their own: Naver, Yandex, Baidu, Daum.
  If your home market has one, its volume data and its indexation are a separate workstream, not a
  Google rounding error. Directory-style local surfaces (in the Czech case, Firmy.cz) are the same
  story for local intent.
- **Territory spelling and inflection traps.** Diacritics, case endings and near-identical variants
  across neighbouring markets (Czech vs Slovak is the classic pair) are separate keywords with
  separate volumes. Treat each territory as its own column; never assume a shared term.

If your home market is English and Google-only, the second and third bullets collapse to nothing —
say so in the file rather than leaving the reader to guess whether the check ran.

### Pre-build rankings baseline

This step owns the PRE-BUILD baseline (own domain if it exists, plus each P1.S5 competitor). P5.S1
owns the post-launch day-0 snapshot; P6.S2 owns the recurring reads. Make sure
`/founder-pipeline:web-keyword`'s rankings output gets recorded here as the baseline, not just read
and discarded.

---

**Skills:** `/founder-pipeline:web-keyword` (the method — run this first); `/founder-pipeline:scout` (territory competitor list if P1.S5 needs extending); `/founder-pipeline:seo-audit` only if the stream already has a live site to audit — for a net-new stream that runs at P4.S3, not here. **Page translation is NOT this step's job and no translation skill ships in this plugin:** once terms are locked, the actual page translation happens at P4.S2/S3 by a translator (human or model) working *from* `TRANSLATION-GLOSSARY.md` — voice-preserving, term-for-term against the locked glossary, never re-deciding a term it finds inconvenient. If you have your own translation skill, hand it the glossary as a hard constraint.

**Write to** `P4-Build.S1-Keywords.md` (+ step folder `P4-Build.S1-Keywords/` when the fan-out produces per-cluster SERP/trends notes worth keeping — one file per keyword cluster, INDEX in the step md). Use `/founder-pipeline:web-keyword`'s output format: **localization table first** (one row per concept, the home-market language as the anchor column, one locked-term column pair per additional territory), then the **main keyword table** (Keyword | Language | Volume | Difficulty | Trend | Intent | SERP check | Target page | Verdict | Source), then the AI-search question list per language, the intent-to-page map, the pre-build rankings baseline, and the keyword gap notes. Raw provider JSON lands in the step folder so re-runs read from disk instead of re-paying. This file is the **keyword contract** — P4.S2 copy and P4.S3 meta/headings must trace to it, P6.S2 KPIs track it in your search console(s), and the locked localization table is mirrored into `TRANSLATION-GLOSSARY.md` for whoever translates the pages.

**Def-of-success — ALL must pass before Owner sign-off (fail → improvement loop per SKILL.md, never advance):**
- `/founder-pipeline:critical` run recorded; the score is advisory (target ≥ 8/10) — the gate is the PASS/FAIL criteria below, not the number.
- 3–7 primary keywords, each with volume+difficulty tagged `[source: <keyword-data provider>, <date>]` (or the explicit unavailability flag) — zero bare guesses, zero scraped estimates presented as data. Max 1 primary keyword may carry the unavailability flag; each flagged keyword creates a `queues/manual-queue.md` row "re-price against a real data source" (dated) at contract lock time — a contract with 2+ unpriced primaries does not lock.
- P1.S4's carry-forward table cited as the seed (its terms not re-priced); only NEW terms carry fresh provider calls.
- Home market and primary export market both named explicitly in the file — no implicit locale.
- Every non-anchor territory in scope has a localization table with ≥2 candidate phrasings compared via real measured volume/trend data per concept — never a bare literal translation presented as the term. Losing candidates + their volumes are recorded as evidence for the locked choice.
- If the home market has a non-Google engine with meaningful share, its data and its indexation path are named in the file (or the file states explicitly that the market is Google-only) — never left unexamined.
- Locked localized terms are written to `TRANSLATION-GLOSSARY.md` (created + seeded if it doesn't exist yet) so the translator and P4.S2/S3 reuse them instead of re-translating.
- **Every primary keyword has a recorded live-SERP check** (intent confirmed, top-10 occupants, SERP features, beatability verdict) — an unvalidated keyword fails the contract.
- Google Trends direction recorded per primary keyword, territory-filtered; any declining trend explicitly reconciled with the P1.S2 "why now" (or the keyword dropped).
- Pre-build rankings baseline captured (own domain + competitors) — P5.S1 owns the post-launch day-0 snapshot, P6.S2 the recurring reads.
- Every planned page has ≥ 1 assigned primary keyword and every primary keyword has a target page — no orphans either way.
- The intent-to-page map enumerates the money pages — service/offer, pricing, booking/contact, homepage — sourced from `P1-Ideation.S6-Offer.md` + `P2-Viability.S3-Pricing.md`; each carries ≥ 1 commercial/transactional primary keyword or a recorded exception.
- ≥ 3 AI-search phrasings written the way the ICP would actually ask.
- ≥ 1 territory-uncontested keyword aligned with a locked differentiator from `P1-Ideation.S6-Offer.md`.

**Gate out (mandatory — see SKILL.md house rules):**
1. Draft `P4-Build.S1-Keywords.md`.
2. Invoke `/founder-pipeline:critical` on the draft — attack volume wishful-thinking, intent mismatches, and any keyword chosen because it flatters the offer rather than matching how the ICP searches.
3. Revise; note what changed.
4. Present the draft + the critical findings + the changes to the owner. **Wait for their explicit approval. Never auto-advance.**

**Checkpoint:** "Keyword contract locked: [N primary keywords, trends: X rising / Y flat]. Intent-to-page map covers [pages]. Content next — copy gets written around exactly these terms. Approve the contract, or widen/narrow the set first?"

**Next:** `stages/P4-Build.S2-Copy.md`
