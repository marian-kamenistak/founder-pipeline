# Audit mode — scoring a live site against measured demand

Mode B. The pages already exist. The question is whether they target anything real, and if a
non-English page set is involved, whether it was localized or merely translated.

## Build the inventory first

Before any judgment, capture for every page in scope: URL, file path, `<title>`, meta description,
and H1 — **verbatim**. Not summarised, not paraphrased. The audit is a string-level comparison and
a paraphrase destroys the evidence.

Two traps that make an inventory wrong in ways that look right:

- **Redirects.** A page can still build while a redirect rule sends its URL elsewhere. Auditing the
  build alone invents pages that aren't reachable; auditing live URLs alone misses files that are
  quietly shipping stale content. Check both, and flag any page that exists in one view and not the
  other — those are usually real defects (duplicate pricing pages with divergent numbers, orphaned
  files with old prices, redirects pointing at files that don't exist).
- **Drafts.** Pages marked draft may or may not build depending on the framework's config. Confirm
  which state applies rather than assuming.

## The no-orphans check, both directions

**Every page → at least one primary keyword with measured demand.** A page targeting nothing
measurable is either serving a purpose that isn't search (fine — record the exception explicitly)
or it's invisible by accident (not fine).

**Every primary keyword → a target page.** Demand you measured and then didn't build for is the
easier half of the gap to fix and the easier half to forget.

**Money pages carry commercial intent.** Offer, pricing, booking, homepage — each needs at least
one commercial or transactional primary, or a recorded exception. A pricing page targeting an
informational query is a quiet, common failure: it ranks, gets traffic, and converts nothing.

**Watch for cannibalisation.** Two pages targeting the same term split the signal, and a blog post
frequently outranks the money page it was meant to feed. Check the live SERP for which of your own
URLs actually appears — the answer is often not the intended one.

**Watch for cross-domain cannibalisation** when an organisation runs several sites. Two of your own
domains competing for one term is worse than either competing alone, and it's invisible unless you
run ranked-keywords on both.

## The translation layer

Two failure modes. They need separate judgments because a page can fail one and pass the other,
and the fixes are different.

### Keyword-level — renderings nobody searches

The output is the localization table from `localization.md`: locked term per concept per territory,
with rejected candidates and their volumes as the evidence trail.

Then find where the site contradicts its own contract. Both directions occur, often on the same
site:

- **Over-translated** — a term rendered natively where the market types English. Common on role
  titles and technical concepts.
- **Under-translated** — an English term left raw where the market has a real, higher-volume native
  word. Common on service nouns, which is where buying intent lives.
- **Inconsistently declined** — English nouns given local inflection on some pages and left bare on
  others. Pick one rule and apply it everywhere; the inconsistency itself reads as machine output.
- **Contract violations** — a glossary exists and pages ignore it. Check the glossary's own status
  too: unratified decisions sitting in a file are not a contract, and treating them as one hides
  the fact that nobody ever agreed.

### Naturalness — grammatical, but not how a native writes

Separate from keywords. A page can target the right term and still read as translated. What to look
for:

- **Calques.** Word-for-word renderings of English idioms that are grammatical and slightly wrong.
  Compound English concepts are the usual source — the parts translate individually and the result
  isn't a phrase anyone says.
- **Dictionary-first word choice.** The first dictionary result for an abstract noun is often not
  the natural one in context.
- **Register drift.** Formal/informal address, honorifics, and tone must be consistent sitewide.
  A single page switching register is jarring in a way native readers notice immediately even when
  they can't name it.
- **Structural tells.** Sentence rhythm carried over from the source language, uniform paragraph
  shapes, absent contractions where the language uses them.

Score each page and produce a **string-level fix table**: exact current string → exact proposed
string → the reason. Not "improve the H1" — the literal replacement text.

**Every proposed string must satisfy both constraints: natural in the language, and targeting a
measured keyword.** A beautifully idiomatic sentence built on a zero-volume term is not a fix, and
a keyword-stuffed one that no native would write trades one problem for another.

## Separating defects from findings

An audit surfaces things that aren't keyword problems — broken redirects, duplicate pages,
conflicting prices, missing files. Report them, clearly separated from the keyword findings.
They matter (they leak the traffic the keywords earn) but merging them muddies both.

## Output

- **Page-keyword map** — page, assigned primary, measured demand, verdict, gap
- **Coverage holes** — measured demand with no page, sized by volume
- **Localization table** — locked terms with rejected candidates and volumes
- **Fix table** — per page, exact string → exact replacement → reason
- **Defects** — structural problems found along the way, listed separately

Rank recommendations by measured demand, not by how easy they are to write. And when the answer to
"are we using the right keywords" is no, say no — with the numbers, and with what people type
instead. An audit that validates whatever already exists wasn't an audit.

## Scope boundary

Audit mode proposes; it doesn't edit. The fix table is reviewed and approved before any page
changes, because keyword and copy decisions have owners and a silent rewrite removes their say.
Where target pages live on a platform without an editing API, the fixes ship as a manual checklist
for a human to apply. That checklist needs a home or it evaporates: write the rows to the project's
`queues/manual-queue.md`, which is the shipped default. If you run an external task board instead,
mirror them there — but write the file either way, so the record survives independently of any
integration.
