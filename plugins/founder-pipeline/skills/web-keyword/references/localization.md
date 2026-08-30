# Localization — pick the term, don't translate it

The method for choosing a keyword in a language that isn't English. Read this before drafting
candidates for any non-English territory.

## The core failure

A literal translation looks correct. It is grammatical, a native speaker would understand it, and
it survives every review that isn't a measurement. It can still be a word nobody types.

This is different from a bad translation. Bad translations get caught. *Correct* translations of
the wrong term ship, sit at position 1 for a phrase with zero searches, and get read as evidence
that the market doesn't exist.

So: the literal translation is a hypothesis. It enters the comparison as one candidate among
several, and it wins only if it measures best.

## Drafting candidates

For each concept, in each territory, draft at least two — usually three or four:

**1. The literal translation.** The dictionary answer. Include it; sometimes it wins.

**2. The industry or job-title term locals actually use.** Often not the literal one. Check how
job boards in that market phrase the role, how people describe it on LinkedIn, how a job ad for it
reads. Recruiters have already solved this problem — their phrasing is field-tested against people
who search for exactly this.

**3. The buyer-language synonym.** Where the brand uses its own word, the buyer often uses a
different one for the same thing. Adjacent professional categories are the usual source: coach vs
mentor vs advisor vs consultant, training vs course vs workshop vs programme. These are not
synonyms to a search engine and frequently differ by an order of magnitude.

**4. The kept-English option.** Many markets borrow English terms wholesale, especially in
technical and business fields, because the English term is what appears on the contract, the
business card and the LinkedIn headline. In several measured cases the English term beat its native
translation by 5-40× *within* the local market. Always include it as a candidate for role titles,
technology names, and recently-imported business concepts.

## Spelling and morphology traps

These silently measure the wrong word — the call succeeds, returns a number, and the number
describes a term nobody typed.

**Closely-related languages are not variants of each other.** Worked example, Czech and Slovak:
`manažer` (cs) and `manažér` (sk) are different words in different markets, as are `kariérní` (cs)
and `kariérny` (sk). Measuring the Czech spelling against a Slovak location returns near-zero and
reads as "no demand in Slovakia", which is a conclusion about the query, not the market. The same
trap exists across any closely-related pair — Spanish and Portuguese, Danish and Norwegian, Serbian
and Croatian — and across national variants of one language, where the shared spelling can still
sit on completely different volumes. Never reuse one territory's keyword list for its neighbour
without re-measuring it there.

**Where a loanword has competing spellings, measure all of them.** Borrowed terms often arrive in
more than one form before one wins, and the split can be even. Measuring one arbitrarily halves
the apparent demand.

**Inflected languages: pick the form people type.** In languages with cases, the nominative is
usually the search form, but not always — the phrase-embedded form can dominate for multi-word
queries. When a concept has a natural phrase form, measure both the bare noun and the phrase.

**Diacritics.** Measure the correctly-accented form. Users type both, and search engines fold them,
but the correct form is what the tooling and the eventual page copy need to agree on. Writing
keywords without diacritics into a report guarantees someone later pastes them into a page.

## Locking

Highest real volume plus trend direction wins the concept for that territory. A candidate with
volume but a declining trend loses to a slightly smaller rising one, because the page will be
alive for years.

**Record the losing candidates with their volumes.** This is the deliverable, not the paperwork.
It's what makes the choice checkable later, and when a literal translation loses, the comparison is
the finding. A locked term with no visible alternatives looks like an opinion.

## When everything measures near zero

Common for B2B and professional-service terms in smaller language markets. The honest reading is
usually not "no demand" but "demand exists and does not express itself as native-language search"
— because the buyers search in English, or ask a model, or arrive via referral.

Still lock a term. Tag it `[low-volume — brand/AI-search play]`. Two reasons this matters more
than it looks:

- **It's a strategy signal, not a footnote.** It says that language's pages are a brand, AI-search
  and secondary-engine play, and that projecting English-style traffic onto them will produce a
  business model built on a number that was never measured.
- **It stops the untested literal from surviving by default.** The alternative to locking is
  leaving whatever the translator wrote, which is the exact failure this whole method exists to
  prevent.

Then check the English terms *within that territory*. When native-language service terms measure
zero, the English ones often don't — that's the market telling you which language its buyers search
in, and it's frequently the most actionable finding of the whole run.

## Secondary search engines

Some markets have a meaningful non-Google engine, and API coverage for those is usually poor or
absent. Worked example: in Czechia, Seznam holds a share large enough that a keyword set validated
only on Google describes part of the market — its results, its snippet formats and the sites that
win them differ from Google's for the same query. Yandex in its markets, Naver in Korea and Baidu
in China are the same problem in different clothes. Find out early whether your territory has one,
because the answer changes what "we rank" means.

Where the engine has no usable API — which is common — check the live results manually for the head
terms and record what you see as **observations, not metrics**, clearly separated from the measured
numbers so nobody later averages an eyeball into a dataset. Note the engine's own indexing route
too; several of them need a separate submission and will not pick a site up from Google's sitemap.

If an engine can't be measured, say it can't be measured. Reporting it as zero invents a finding.

## Feeding the glossary

Locked terms and their rejected candidates belong in the project's `TRANSLATION-GLOSSARY.md`.
Whatever translates pages next reads it first and treats the locked column as fixed, which is what
stops the next page from being re-translated straight back into the term you measured and rejected.
Without this step the localization work decays with every new page.
