# Phase 5 — SEO + AI-SEO: research, on-page, AI-crawler surfaces, crawler delivery

Reference: [`references/seo.md`](../references/seo.md).

Runs after GATE 1 content exists; finalizes after GATE 4. Research rounds are **[P]** subagent lanes dispatched at fixed points (round 1 from Phase 1.0, round 2 mid-build, round 3 pre-publish).

## Execution order — zones, not topics

Sequence by **which files an item writes**, not by which topic it belongs to — matching the rule Phases 2–3 already use ("both touch layout/CSS and are never parallelized against each other") applied properly to this phase. Two items run in parallel iff they write to different zones; a zone's own items are serial with each other when order matters.

| Zone | Writes | Covers |
|---|---|---|
| **Z1** standalone routes + `public/` | `public/*`, `src/pages/rss.xml.ts`, `llms.txt.ts`, `nlweb.json`, `<key>.txt`, `scripts/gen-agent-markdown.mjs` | robots.txt, IndexNow key, RSS route, NLWeb route, llms files, Markdown twins |
| **Z2** layout `<head>` | `src/layouts/*`, `<SEO/>` | titles/descriptions, JSON-LD, RSS autodiscovery link, analytics wiring (pulled forward from 6.2 — same files, one pass) |
| **Z3** page bodies | `src/pages/**`, `src/content/**` | content depth, AI-citation must-haves (§5.4), internal links, `/founder-pipeline:brand-voice` pass — **serial within itself**: depth and §5.4 before link-density scoring, or the count measures copy that's still growing |
| **Z4** nav + footer | nav/footer components | revenue pages into nav, footer mini-sitemap |
| **Z5** new pages | new files only | geo landing pages |

Z1/Z2/Z4/Z5 run **[P]** against each other from phase-open. Z3 is **[S]** internally (depth → links) and runs alongside the others since it touches none of their files. `llms.txt`/`llms-full.txt` (Z1) wait on research round 3.

**BARRIER 1 — content freeze.** `/founder-pipeline:brand-voice` final pass on every public string, then a **[P]** wave of read-only local-build checks against the frozen `dist/`.

**BARRIER 2 — staging deploy.** One deploy candidate serves both GATE 5 (below) and GATE 6.1 — merge the verification wave, evaluate each gate against its own subset, so the deploy-and-check loop runs once instead of twice. Any fix re-triggers the whole wave.

## 5.0 Research protocol (the one definition — all three rounds use it)

- [ ] **Every number in a research round obeys the honesty rules** (the same house rules `/founder-pipeline:founder` applies), which are, in full:
  1. **Sourced, never estimated.** Every figure comes from an actual API call, tool run or named published study. If you did not fetch it, you do not have it.
  2. **"Not available" beats a blank or a zero.** An unavailable metric prints `not available` *with the reason* — no quota, no coverage for this market, tool returned nothing. A zero means measured-and-zero and nothing else.
  3. **Low confidence is labelled with what would raise it.** Say what the number would need to become trustworthy (a bigger sample, a paid tier, a second source), so the reader knows the cost of certainty.
  4. **Sampling caps are stated, never silent.** "Top 100 of 3,400 URLs" — never present a capped run as if it were exhaustive.

  "No data" is frequently the most valuable answer a keyword round returns — a term with no measurable demand is a finding about the market, not a gap to paper over.

Two parallel subagent streams per round:
- **Stream A (external):** what ranks in Google for the target intent, what Perplexity/ChatGPT/AI Overviews cite, which competitor pages win and why, which roster/list page is the AI-citation source of truth in the niche
- **Stream B (internal, round 2 onward):** meta title/description inventory, H1 structure, schema coverage, internal-link density, `llms.txt` freshness, cross-domain cannibalisation

Rules:
- [ ] Rank the top 5 target keywords by (volume × business value × authentic authority) / (difficulty × time-to-rank). Everything else waits
- [ ] One query = one canonical page; check nothing you own already targets the same query
- [ ] **Cover the head term's sub-query cluster, not just the head term itself.** Pages ranking across a fan-out of related queries were **161% more likely to be cited**, Spearman **0.77** [Surfer/Hardwick, 7,000+ queries] — the strongest content-side correlate found in the research behind this rule, and mechanistically consistent with Google's own confirmed query fan-out in both AI Overviews and AI Mode
- [ ] Every round's findings → the site's `PLAYBOOK-CASE-NOTES.md` (keywords, competitor table, cannibalisation map, synonym routing)

## 5.1 On-page — Z2/Z3/Z4/Z5

- [ ] [Z2] **Titles 50–60 chars, dash separators not pipes, no brackets, the key term mirrored in the H1.** Google rewrites titles at scale and length is the single biggest predictor: 51–60 chars = the lowest rewrite band (39–42%); >60 chars = >76%; >70 chars = 99.9% [Zyppy, n=80,959 titles / 2,370 sites]. Brackets `[]` → 77.6% rewritten; pipes removed/replaced in 41%; dashes survive at 19.7%. A number present in both title and H1 is retained 97.3% of the time vs 74.2% when only in the title. Google's overall rewrite rate reached **76% by Q1 2025** — short and literal beats clever. Causal backup: moving the strongest term to the front of the title → **+8.5% organic traffic @95% confidence** [SearchPilot]; all-caps A/B → **+7% @99%** [SplitSignal, n=3,908 pages]
- [ ] [Z2] Descriptions 120–155 chars, unique per page, keyword-first; drop the brand-name suffix except on brand pages. Google rewrites the majority of these regardless (~63–71% across studies) — write them once, then leave them alone. **Never `data-nosnippet` on body content**: a causal A/B showed **−3%, significant negative within 2 weeks** [SearchPilot]
- [ ] [Z3/Z4] **Money page shape — check this before any metadata work, because a wrong offer shape cannot be recovered by clean tags** (offer anatomy, added 2026-08-22; no effect sizes claimed, this is craft):
  1. **One service per page, never two combined.** The most common failure on a service site: a combined page has no primary keyword to win and competes with itself
  2. **Two-second rule** — what you do, where, and what to do next are all visible without scrolling and without reading a paragraph. Plain headline naming the service; wordplay goes in the sub-head or nowhere
  3. **Price answered on the page** — a number, a band, or a stated reason there isn't one. Same rule as §5.4 Tier A, restated here because it is an offer decision before it is an SEO one
  4. **CTA above the fold, mid-page and at the end** — one action, three chances
  5. **Real photos, and FAQ capped at 5 questions** on a transactional page. Stock imagery reads as a page about a service rather than a page from a business; more than 5 questions turns a money page into a content page
- [ ] [Z4] Every revenue page in primary Nav — footer-only starves crawl priority
- [ ] [Z3] **Serial, in this order — content depth first, then internal linking (link-density counts measured over copy that's still growing measure nothing):**
  1. Every revenue page carries real specifics — a table, concrete numbers, named constraints — not just positioning copy. The largest single controlled effect measured in 2025: adding specification tables and structured detail → **~+20% organic traffic, statistically significant** [SearchPilot]. Counterweight so nobody over-corrects into padding: length itself does nothing — word count vs. AI citation, **r = 0.04** across 174,048 cited pages, and 53.4% of cited pages are under 1,000 words [Ahrefs]
  2. Internal linking density: service pages ≥3 outgoing body links and ≥5 incoming; blog posts ≥2 links back to service pages; related-posts block everywhere; footer mini-sitemap; no duplicate anchor text → different URLs (sanity script in `references/seo.md`). **Plus: ≥1 exact-match internal anchor pointing at every page that matters** — pages with one got **~5× the search traffic** of pages without [Zyppy, 23M internal links / 1,800 sites / ~520K URLs matched to GSC clicks; 53% of all URLs had ≤3 internal links]. Causal confirmation: nearest-link additions → **+7%** on recipient pages, footer links → **+5%** [SearchPilot]; category-page linking → **+25%** [SplitSignal]
  3. **Answer-first extractability:** question-shaped H2s with the direct answer in the first 1–2 sentences underneath, per `${CLAUDE_PLUGIN_ROOT}/skills/ai-seo/references/content-patterns.md`. Frame honestly, this is the most over-sold area in the field — the Princeton GEO paper's headline lifts (+41% statistics, +115% cited sources) don't survive realistic multi-actor competition [C-SEO Bench, NeurIPS 2025: most of the same tactics "not only largely ineffective but also frequently have a negative impact," context position alone beat the best tactic 7.6×], and a 45-study survey found **no technique with a stable cross-platform causal effect** [Martinez, arXiv Jul 2026]. Do it because it's free and good writing — never quote a multiplier
- [ ] [Z5] Geo landing pages: one props-driven GeoPage component; research the geo modifiers people actually type (city + region + "remote", NOT industry labels); both niche synonyms in titles; footer interlinking
- [ ] [Z5] **If the site targets a PLACE, a local-SEO layer applies on top of everything here.** No local-SEO skill ships with this plugin, so run these three inline — they are the ones that bite at build time: (a) **no service×city page ships without a real search-volume figure**; building unvalidated cells is how a geo section becomes the thin content Google sweeps; (b) the `LocalBusiness`-family node carries `geo`, `openingHoursSpecification` and `priceRange`, not just address and telephone — those three are the most commonly missing; (c) score every pair of sibling geo pages for text similarity **before deploy** (Jaccard over the page's own body tokens is enough) — pairs over 0.60 are a mail-merge, not a page set. Locality matching must fold diacritics wherever your market uses them ("Kraków" ≠ "Krakow" to a raw comparison)
- [ ] [Z5] Programmatic SEO ONLY when the keyword map has a repeatable pattern + a real dataset: template × dataset, genuinely unique per-page content (human-in-the-loop edit), ~100-page MVP, monitor indexation, THEN scale. A 6–24-month compounder, never a launch-day task
- [ ] [Z2] **Every page's served URL === its declared canonical, checked mechanically across ALL pages, not spot-checked.** Trailing slash is the usual mismatch. Script in `references/seo.md` → URL/canonical integrity
- [ ] [Z1] **Sitemap lists only canonical, indexable, 200-returning URLs** — never a redirect, never a `noindex` page. If a page is excluded from the sitemap, it must also be excluded from any reindex queue
- [ ] [Z3] `marketing/seo-meta.md` written: one entry per page (title, description, OG, schema, keywords)

## 5.2 AI-crawler surfaces — Z1

- [ ] [Z1] `robots.txt` — write it from a **single canonical source** and never keep a second copy. Four tiers, in this order: (1) `User-agent: *` with the site's own disallows and the `Sitemap:` line; (2) search crawlers you explicitly welcome; (3) AI *retrieval* bots that fetch a page to answer a live query (OAI-SearchBot, PerplexityBot, ClaudeBot, Google-Extended) — allow these, they are how you get cited; (4) AI *training* scrapers (GPTBot, CCBot, Bytespider…) — allow or deny as a deliberate policy decision, recorded once in `PLAYBOOK-CASE-NOTES.md`. Two traps: keeping the same UA list in more than one skill or file guarantees they drift out of agreement, and a `public/robots.txt` shadowed by a generated route means the file you edited is not the file that ships. **Reading policy is not verifying delivery** — the tiers are only real once §5.3's matrix confirms each UA actually gets a 200
- [ ] [Z1] **`llms.txt`/`llms-full.txt` are an agent-tooling surface (Claude Code, Cursor, MCP integrations), not a search or citation lever — build them, don't gate publish on them.** The evidence is unambiguous: 97% of published files receive zero requests, and AI *retrieval* bots are 1.1% of the fetches that do happen [Ahrefs, n=137,210 domains]; PerplexityBot logged 0 fetches across 556 domains in 12 weeks [EZY.ai]. Google, current docs: *"You don't need to create new machine readable files, AI text files, markup, or Markdown to appear in Google Search."* Full evidence: `${CLAUDE_PLUGIN_ROOT}/skills/ai-seo-llms-builder/references/evidence.md`. **Still written LAST**, after research round 2+ has produced the real query list, keyword contract and FAQ — never scaffolded early from the page tree; when built, `/founder-pipeline:ai-seo-llms-builder` is the quality bar (rule + template in `references/seo.md` → llms.txt from research)
- [ ] [Z1] `llms.txt` + `llms-full.txt` generated at build from content collections. `llms-full.txt` is the DEEP companion, never a copy of `llms.txt`: it carries the full text `llms.txt` only summarises. Two copies of the same content drift within a month. Both files exist on every property or neither does
- [ ] [Z1] RSS at `/rss.xml` via `@astrojs/rss` from the same collections (published, default-locale, newest first); autodiscovery `<link>` in every layout (Z2); feed listed in `llms.txt` Key Pages. Skip only if the site has no dated content — record the skip
- [ ] [Z1] **Markdown twin of every indexable page, emitted post-build at `<route>.md`, advertised with `<link rel="alternate" type="text/markdown">` in the layout `<head>` and a stanza in `llms.txt`.** Recipe + generator in `references/seo.md` → Markdown for agents. Three non-negotiables, each of which was a real failure in the 2026-08-14 build: the twin is **absent from the sitemap** (it is an alternate representation, not a competing page), it is **never emitted for a `noindex` or private route** (that would be a fresh unprotected copy at a URL the site's existing noindex layers don't cover), and it carries **no `X-Robots-Tag: noindex`** (that would tell OAI-SearchBot to drop the content, which is the opposite of the point — the `url:` frontmatter field is the dedup signal). Measured on two real builds: 87% fewer bytes across 227 pages, 91% across 84 pages
- [ ] [Z1] **Do NOT try to serve the twin on `Accept: text/markdown` on this stack. Cost-benefit is inverted and it has a measured production failure mode.** Astro middleware never sees prerendered pages, so negotiation needs `run_worker_first: ["/*"]` — which bypasses the asset routing layer, where `_redirects` is evaluated. Verified with `wrangler dev` on a real build: all 102 of its redirect rules silently returned 200 instead of 301. Scoping around it doesn't fit either: `run_worker_first` is **capped at 100 rules** and that site needed 228. Negotiation is worth buying, not building — Cloudflare's own Markdown for Agents (Pro tier) runs at the edge *above* the redirect layer. Evidence on whether it's worth even that: Buytaert logged a month of Cloudflare data and saw **zero** crawlers negotiate, all markdown fetches arriving at `.md` URLs; suganthan.com's 44-day run logged 1,421 negotiated requests, all from live agent tooling rather than GPTBot/ClaudeBot/PerplexityBot. **Ship the `.md` URL; treat the header as optional.**
- [ ] [Z1] NLWeb endpoint + `/.well-known/nlweb.json`
- [ ] [Z1] **IndexNow key wired at build, every site, no exceptions:** 8–128 char hex key, `public/<key>.txt` at root, `.indexnow-key` in repo root for scripts. The key is public by design — NOT a secret, never in `.env`

## 5.3 Crawler delivery — the check no phase file previously required

**This is the biggest gap the evidence sweep found.** First-party run data from a live site: it was serving an error to **54% of AI-crawler requests** (953×499 + 134×429 + 499×404, concentrated on `/event/*` — the most question-shaped content the site owns had never once been successfully delivered to a crawler) while its `robots.txt` allowed every one of those bots the whole time. Reading policy is not the same as verifying delivery.

- [ ] **[P, after BARRIER 2] Fetch every key URL as each AI + search user-agent and assert 200**, against the staging deploy candidate. Build the matrix inline — it is a nested loop over your key URLs × the UA strings from §5.2's four tiers, asserting `200` on each and printing every cell that isn't. Crawl is rarely the bottleneck — an established domain sees thousands of AI-crawler hits per week — **delivery and selection** are

  ```bash
  UAS=("Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
       "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)"
       "Mozilla/5.0 (compatible; OAI-SearchBot/1.0; +https://openai.com/searchbot)"
       "Mozilla/5.0 (compatible; PerplexityBot/1.0; +https://perplexity.ai/perplexitybot)"
       "Mozilla/5.0 (compatible; ClaudeBot/1.0; +claudebot@anthropic.com)"
       "Mozilla/5.0 (compatible; GPTBot/1.0; +https://openai.com/gptbot)")
  for u in $(curl -s "$BASE/sitemap-0.xml" | grep -oE '<loc>[^<]+' | sed 's|<loc>||'); do
    for ua in "${UAS[@]}"; do
      code=$(curl -s -o /dev/null -w '%{http_code}' -A "$ua" "$u")
      [ "$code" = "200" ] || echo "FAIL $code  ${ua%% *}  $u"
    done
  done
  ```
- [ ] **[P, after BARRIER 1] Main content exists in raw HTML with JS disabled** — `curl` the page and grep for the H1 + first body paragraph. AI crawlers execute **zero JavaScript** in the overwhelming majority of fetches [Vercel/MERJ, >500M GPTBot fetches: JS fetched but not executed in 11.5–23.8% of requests depending on bot; independently replicated]. Binary outcome, no partial credit — Astro passes by default, this check exists to catch a client-rendered island holding real content. Gemini is the one exception (uses Googlebot's Web Rendering Service)
- [ ] **[P, after BARRIER 1] Grep the crawler-view HTML for PLACEHOLDER strings, not just for the H1.** Checking the H1 and first paragraph is not sufficient and will hand you a false pass: one real page passed that check while three widgets in its live-data section shipped the literal string `Loading…` to GPTBot, so the entire section — counters, role distribution, capacity chart — was invisible to AI search. Every client-hydrated island must **server-render its real summary**, with the script REPLACING it on success, and its error branch must leave the server-rendered text standing rather than overwriting it with "unavailable".
  ```bash
  curl -s -A "Mozilla/5.0 (compatible; GPTBot/1.0)" "$URL" \
    | grep -oiE "loading[.…]*|please wait|fetching|--|placeholder|lorem" | sort | uniq -c
  # any hit inside a content region is a fail
  ```

## 5.4 AI-citation content must-haves — Z3

**Read this framing before you use the checklist, or you will over-invest.** Every large measured effect in 2025–26 AI-citation research is **off-page**: Trustpilot presence swung citation rate from 1% to 53.5% [Seer, 804,491 AI responses, 4 platforms, 1,926 brands, 15,783 prompts]; branded web mentions correlate at Spearman **0.664** vs backlinks 0.218 [Ahrefs, 75,000 brands]. **No published correlation coefficient exists for any on-page formatting element.** That asymmetry is the finding. The items below are cheap and defensible; none of them is a lever that beats ranking for the query in the first place.

**The counter-rule that governs the whole section — optimising the body for citability can cost you retrieval.** Body-only GEO rewrites cut average top-20 presence ~9%, post-rerank top-10 presence **16%**, and final citation 6% [SAGEO Arena, via Martinez survey arXiv 2607.14035]. And retrieval position dominates everything here by orders of magnitude: moving a document to context position 1 = **+2.77** ranking positions vs **+0.36** for the best content rewrite, a ~7.7× gap [C-SEO Bench, NeurIPS 2025 D&B, 1,921 queries, 4 LLMs]; list position scored **OR >>10,000** vs OR ~1 for formatting [Vishwakarma et al., SIGIR 2026, 252,000 counterbalanced trials, 6 LLMs, 18 factors]. **Never trade content depth or query-cluster coverage (§5.0) for any tactic below.**

### Tier A — gated (strong evidence, unanimous across models)

The three factors below come from the only large controlled experiment in the field [Vishwakarma et al., SIGIR 2026, 252,000 trials, 6 LLMs — Gemini 2.5, GPT-5.x, Claude 3.5 Sonnet, Kimi K2; one factor varied per trial, brand-anonymised, counterbalanced, GLMM]. Each scored **OR >>10,000 and was unanimous across all six models** — the same tier as topic match and retrieval position, and three to four orders of magnitude above formatting.

- [ ] [Z3] **A visible, accurate last-updated (or published) date on every page.** [Recency was a unanimous gatekeeper, OR >>10,000, in the 252k-trial study. Corroborated observationally: AI-cited content runs 25.7% fresher than the organic top 10, and ChatGPT cites URLs 393–458 days newer [Ahrefs, ~17M citations]; 75% of cited pages were updated within 12 months, and of 4,124 pages carrying both dates, 72% look fresh by *update* date vs only 42% by *publish* date [Seer, n=7,683 pages / 47,097 citations, Mar–Jun 2026 — explicitly correlational]. Google AI Overviews is the least recency-biased surface.] **Hard limit, unchanged from §8.11:** the date must reflect a genuine content change. Bumping `dateModified` without substantive edits is manipulative per Google's own guidance, and Illyes' position is to omit an unreliable date rather than emit one — an inaccurate date makes Google distrust every date on the site.
- [ ] [Z3] **If the page concerns something paid, the price or cost is stated explicitly on the page — a number, not "contact us".** [Price-not-mentioned scored OR >>10,000, unanimous across all 6 models — one of only four gatekeeper factors found. Honest caveat the authors state: the corpus was product-review documents, so "price" may generalise to *concrete commercial specifics* rather than literally a price tag.] Where pricing is deliberately private, that is a positioning decision that costs citations — make it knowingly, and give the page a different concrete number (duration, cohort size, scope) instead. Never let this rule resurrect a stale hardcoded price: `Offer` defaults stay `undefined` (§8.11).
- [ ] [Z3] **Concrete named specifics — figures, durations, constraints, specs — present in the body.** [Missing-specifications scored OR 8.63–243 across the same 252k trials. Reinforced correlationally: Zyppy's meta-analysis of 54 experiments/patents/case studies scores "Factually Specific" **8.3/10, 10th of 23 factors** — "0.8 g/kg of bodyweight" beats "adults need protein".] Note this is about specificity, **not** placement and **not** methodology disclosure — see Tier B.

### Tier B — checklist (weak, contested, or folklore; do them for the reader)

- [ ] [Z3] **Open with the real number.** Put at least one concrete, true figure in the first ~60 words, and the direct answer in the first paragraph. **Do this for readers — there is no measured citation multiplier behind it and you must not claim one.** [No study has ever manipulated within-page placement of statistics. The "44.2% of citations come from the first 30% of the page" figure is real but observational — it measures where cited text was *found*, not that moving text earlier causes citation [Indig/Growth Memo via Search Engine Land, Feb 2026, 18,012 verified ChatGPT citations, p≈0.0] — and the same study found **53% of citations came from mid-paragraph**, not the opening sentence. On statistics-anywhere the benchmarks split in sign: Princeton GEO +34% PAWC [KDD 2024, 10K queries, *simulated* GPT-3.5 engine] vs **−0.53 ranking positions, significantly negative** [C-SEO Bench] vs +2.4% with trustworthiness falling [CC-GSEO-Bench, 1,030 articles].]
- [ ] [Z3] **Build a table when the data is genuinely tabular — and never convert prose to a table expecting AI citations.** The justification is organic, not AI: adding specification tables and structured detail is the largest single controlled effect measured in 2025, **~+20% organic traffic, statistically significant** [SearchPilot]. [For AI citation it is folklore at the table level: content structure scored **OR 0.79–1.68 — null**, and the authors' conclusion was verbatim *"formatting choices had no impact"* [252k trials, 6 LLMs]. The circulating table multipliers — 2.5×, 4.2×, 25.7%, 47% — come from vendor posts with no published methodology, disagree by a factor of ten, and none controls for ranking position. The one supportive controlled study bundles tables with lists and code blocks and never isolates them [GEO-SFE, arXiv 2603.29979].]
- [ ] [Z3] **A visible FAQ accordion wherever the page has real repeat questions — question-shaped heading, direct answer in the first 1–2 sentences — mirrored 1:1 into `FAQPage` markup (§8.11).** [Structure-level support is real but bundled: +17.3% relative citation rate from structure alone with semantics held constant, p<0.001 [GEO-SFE, 200 articles × 6 engines, 2,400 test cases]. The markup layer is measured and null — see §8.4; it ships by standing decision, not evidence.] The accordion is the part that does the work; every answer must be in the DOM, server-rendered, never JS-only.
- [ ] [Z3] **State claims confidently — cut "may", "could", "in some cases" where you actually know the answer.** [Hedged language scored OR 2.67–754 against citation across 4+ of 6 models; claims-with-evidence OR 2.09–>>10,000 [252k trials]. Weaker than Tier A and not unanimous, but it costs nothing and it matches the `/founder-pipeline:brand-voice` and `/founder-pipeline:humanize` bar already applied to every string.] Hedge where you're genuinely uncertain — a false confident claim is a worse failure than a lost citation.
- [ ] [Z3] **Answer capsule under every question-shaped heading: 40–60 words total, first sentence self-contained at ≤25 words, no hyperlinks inside it.** Sentence 1 is the unit an engine lifts; sentences 2–3 carry the qualifier that makes the block featured-snippet eligible; paragraph snippets truncate near 320 characters, which is where the hard cap of 60 comes from. Source links live in the detail *below* the capsule, never inside it. **Canonical statement of this rule, and the reconciliation of the two conflicting source figures (20–25w vs 40–60w), lives in `${CLAUDE_PLUGIN_ROOT}/skills/ai-seo/references/aeo-patterns.md` §2** — every other file points there rather than restating a number. [Tier B for the same reason as the accordion above: structure-level support is real but bundled (GEO-SFE +17.3% from structure alone), and no study has isolated capsule length. Do it because it serves both a reader and a snippet extractor — claim no multiplier.]
- [ ] [Z3] **Write every section so it survives being read alone — no "this", "it", or "as described above" pointing at an earlier section.** [Sound theory transferred from RAG architecture, with **zero publisher-side tests**. Anthropic Contextual Retrieval (248-query eval) cut top-20 retrieval failure 5.7% → 2.9%, a **49% reduction** — but the *retriever* prepended the context, not the author, and a system doing contextual retrieval or late chunking makes the author's effort redundant. Follow it because it costs nothing and the mechanism is sound, never because there's a number behind it.]
- [ ] [Z3] **Attribute non-obvious factual claims to a named, linkable source.** [Correlational only: Zyppy scores "Cites Sources" **8.0/10, 12th of 23** across 54 studies. **Do not quote the Princeton "+115% for cited sources"** — that figure is the 5th-ranked site in an all-optimised 5-source pool on a simulated engine, where the top-ranked site simultaneously *lost* 30.3%; it is a zero-sum redistribution effect, not a general lift, and C-SEO Bench failed to replicate the family of tactics it belongs to.]

**Rejected — do not add these and do not let them back in:**
- **"State sample size, collection date and method next to every statistic to get cited."** No study anywhere tests this. Zero measured evidence. Keep methodology disclosure as an editorial/trust practice if you want it; never justify it as a visibility lever.
- **Author-schema multipliers** — "1.9× for named bylines", "2.3× with credentials", "1.8× for complete `Person` schema", "40% penalty for no named author". Every one is vendor-sourced with no published n, method or control. Google Search Liaison has stated bylines are not a direct ranking factor.
- **Three fabricated statistics now circulating in GEO content**, checked to primary source and not found: a *"Princeton + Moz, 500,000 URLs, WWW 2026, FAQ schema = 3.2× citations"* study that **does not exist** (no Princeton release, no Moz publication, no WWW 2026 proceedings entry; the same 3.2× is credited elsewhere to "200+ domains" and to "73 websites"); *"SE Ranking: data-rich pages get 93% more citations, expert quotes 71% more"* — **not present** in the SE Ranking primary (n=2.33M pages, XGBoost+SHAP, Dec 2025); and *"schema markup → 2.1× more citations"*. If any of these appear in a draft, cut them.

## GATE 5 → Phase 6

Research round 3 done (findings in `PLAYBOOK-CASE-NOTES.md`) · SEO crawl audit on staging (`/founder-pipeline:seo-audit`, plus a third-party crawler for the crawl layer) — every red flag fixed · grep public HTML for `[Placeholder|TODO|Lorem|TBD]` = zero · all 5.2 surfaces build and render locally · **URL/canonical integrity script passes on every page (zero mismatches)** · **every sitemap URL returns 200 and is not `noindex`** · **crawler-delivery matrix (5.3) returns 200 for every checked URL × UA on staging** · **Markdown twins: count matches the indexable page count, zero twins for `noindex`/private routes, zero twins in the sitemap, `.md` serves as `text/markdown` and `_redirects` still 301 (both checked against `wrangler dev`, not just the built files)**.

**Tier-A AI-citation items (§5.4) — gated, all three:** every page carries a **visible, accurate** date · every page about something paid states a real **price/cost number** (or the private-pricing decision is recorded and a different concrete number stands in its place) · every page carries **concrete named specifics**, not positioning copy alone. Tier B is a checklist, never a blocker — the evidence doesn't support gating on it.

```bash
# Tier-A sweep, as a crawler sees it (zero-JS, server-rendered HTML only).
# Output is a WORKLIST OF CANDIDATES, not a pass/fail — same convention as the orphan check.
# The date line is a real failure on any page. The price line only matters on pages that sell
# something, so triage its hits by hand rather than chasing them to zero.
#
# Set these two ONCE per site, to your own currencies and locales, and reuse them everywhere:
CURRENCY='EUR|USD|GBP|\$|£|€'                    # add every currency the site quotes in
DATEWORDS='updated|published|last reviewed'      # + the same words in each secondary locale
                                                 # (worked example, CZ mirror: aktualizováno|publikováno)

for u in $(curl -s "$BASE/sitemap-0.xml" | grep -oE '<loc>[^<]+' | sed 's|<loc>||'); do
  h=$(curl -s -A "Mozilla/5.0 (compatible; GPTBot/1.0)" "$u")
  echo "$h" | grep -qiE "($DATEWORDS)[^<]{0,40}[0-9]{4}" \
    || echo "NO VISIBLE DATE: $u"
  echo "$h" | grep -qE "[0-9][0-9,. ]*\s*($CURRENCY)|($CURRENCY)\s*[0-9]" \
    || echo "  no price number (only a failure if this page sells): $u"
done
```
