# What actually earns a citation

The llms file routes an agent to a page. Whether that page gets quoted is decided on the page. This is
the half that moves the number.

## The measured levers

From the GEO paper (Aggarwal, Murahari, Rajpurohit, Kalyan, Narasimhan, Deshpande — KDD '24,
Princeton / Georgia Tech / Allen Institute / IIT Delhi), benchmarked on GEO-bench, 10,000 queries
across nine domains:

| Lever | What it means on the page |
|---|---|
| **Quotation addition** | A named person saying something, in quotes. Not a paraphrase. |
| **Statistics addition** | A number where a vague claim was. "1,400 members as of August 2026", not "a large community". Your own real figure, carrying its own date. |
| **Cite sources** | Link the origin of a claim, including outbound to credible third parties. |
| Authoritative tone, fluency, technical terms | Worth doing, not worth a sprint. |
| **Keyword stuffing** | Backfires. It is the one tactic that measurably hurts. |

**The percentage column was struck on 2026-08-22, deliberately.** The figures that used to sit here
(+27.8% / +25.9% / +24.9%) came from a **simulated** engine — Google top-5 retrieved, GPT-3.5 wrote
the answer, GPT-3.5 judged it, which is circular. The paper's own real-engine validation was n=200
on Perplexity, where the Statistics gain fell to +8.8% and **keyword stuffing scored +13.4%** on the
same metric. C-SEO Bench (NeurIPS 2025, 1,921 queries, 9 methods) then found most of these tactics
ineffective to negative, decaying further as adoption rises. **Keep the levers; they are sensible
structure. Never quote a number against them** — every vendor figure circulating in 2026 traces back
to that one 2024 study.

A meta-review of 45 GEO studies (July 2026) found content structure, topical depth and context
placement produced more consistent results than any single trick.

## The extractability kit, per money page

This is the same kit `${CLAUDE_PLUGIN_ROOT}/skills/founder/stages/P4-Build.S3-Web.md` already requires. Score one point each:

1. **Definition block in the first 300 words.** A self-contained paragraph that answers "what is X"
   without needing the rest of the page. AI engines lift blocks, not narratives.
2. **A statistic or named source every 150–200 words.** Fact density is what makes a passage worth
   quoting instead of summarising.
3. **Paragraphs of 2–3 lines.** Long flowing prose does not survive extraction.
4. **At least one comparison table.** Among the most citable formats there is.
5. **A visible, server-rendered FAQ accordion**, using the question phrasing people actually type,
   mirrored 1:1 into `FAQPage` JSON-LD. Order matters and the point is scored on the **accordion**:
   a fact living only in the markup was retrieved by zero platforms in every test run. Answer length
   follows the canonical capsule rule — `${CLAUDE_PLUGIN_ROOT}/skills/ai-seo/references/aeo-patterns.md` §2.
6. **Synonym-first title**, covering the phrasing variants people use for the same thing.
7. **Named author with a byline** where the page carries opinion.
8. **Outbound citations** to credible sources. Counter-intuitive for SEO instincts; it is one of the
   three measured levers.

Citability score = kit items present, normalised to 10, averaged across the routed money pages.

## Off-site, which usually outweighs everything above

Worth knowing so this skill does not oversell what a page edit can do:

- Roughly **82% of AI citations come from earned media** rather than owned or paid content
  [Muck Rack, 25M+ links, 3 replications; corroborated by 5W at 85.5% and AirOps at ~85%; Meltwater
  dissents at 39.5%].
- **Brand mentions correlate more strongly with AI visibility than backlinks do** — reported around
  0.664 vs 0.218. [operating assumption: the correlation is widely reported by vendors and matches
  what we see, but we have not found a study with a public method behind those two coefficients.]
- Publishing across many outlets rather than only your own site is reported to increase AI citations
  substantially. The one measured figure (Stacker/Scrunch, 944 prompt-platform combos with a control:
  7.6% → 34% cited) comes from a vendor that sells syndication — pilot it before believing it.
- **ChatGPT's retrieval leans on Bing**, with a high overlap between its citations and Bing's top
  results. That is why `/founder-pipeline:web-indexation`'s IndexNow ping matters more than any llms file edit.
- The overlap between Google's top-10 and AI citations has fallen sharply, so ranking and being cited
  are drifting apart. Do not assume one buys the other.

When a stream asks "how do we get cited", the honest ranking is: earn mentions elsewhere, be in Bing's
index, make the page quotable. The llms file is somewhere below all three, and is mostly about serving
agents well.

**llms.txt's own ceiling, stated so this skill never oversells its primary artifact:** a perfect
`llms.txt` earns zero citations on its own. 97% of published files receive no requests at all
[Ahrefs, n=137,210 domains], retrieval bots are 1.1% of the traffic the rest do get, and Google lists
the file under myths. Its entire measurable value is agent tooling — a coding agent or agentic
browser reading the real prices instead of scraping a nav. Score it, ship it, keep it accurate, and
never put it on a slide as a visibility lever.
