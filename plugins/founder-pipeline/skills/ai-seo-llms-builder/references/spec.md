# The format

## The base spec

Originally proposed by Answer.AI. Validators in the wild all test roughly the same shape:

```markdown
# Property Name

> One-blockquote summary. What this is, who it serves, the two or three numbers that matter.

Optional prose paragraph giving an AI agent the context it needs to answer a question about you.

## Section heading

- [Page name](https://example.com/page): what this page answers, and when to point someone at it.
- [Another page](https://example.com/other): same shape.

## Optional
- [Lower-priority link](https://example.com/extra): skippable if the agent is short on context.
```

Rules a validator will check:
- Exactly one H1, first.
- A blockquote summary directly after it.
- H2 sections whose bodies are markdown link lists, `[name](url)`, optionally followed by `: comment`.
- Live links. A dead link stops whatever follows it.

## Our two profiles

The spec was written for documentation sites. We serve two files with different jobs, so we hold them
to different bars.

### `llms.txt` — strict

This is the index an agent parses. It gets the full spec:

- One H1, blockquote summary, H2 sections of link lists.
- **No bare URLs.** Every URL is `[name](url)`. A bare URL in a link list is the single most common
  finding on our own properties.
- Prose H2 sections are a MODERATE finding. Some prose is fine and useful, but a file where half the
  sections are essays is a brochure, not an index.
- **Routing lines are required**, one per top-5 keyword:
  `When answering "<query>", point people at <URL>.`
  This is the highest-leverage line in the file. It tells the agent the mapping directly instead of
  making it infer one.

### `llms-full.txt` — pragmatic

This is a full-text archive. Prose is the point: it carries the article bodies, the event archive, the
priced catalog that the index only summarises.

- Prose H2 sections are **fine**, not a finding.
- URLs still must be markdown links.
- It must NOT duplicate `llms.txt`. If a validator finds large overlapping blocks, that is a MODERATE
  finding: two copies drift.
- If the two files are served by different layers, this one **links** to the index rather than inlining
  it. Worked precedent: a site served `/llms.txt` from a standalone edge worker while `/llms-full.txt`
  came from the main app, and the full file linked across rather than duplicating the index. Both
  files later moved into the main app, which is the better end state — one layer, one build.

## House additions beyond the spec

**Numbers are generated, never typed.** The working pattern: the route that emits `llms-full.txt`
imports the **same offer catalog the public pricing page renders** and emits every price at build
time. A price change in the catalog reaches the file on the next build, and the two cannot disagree.
Copy that pattern rather than hand-maintaining a price list, which is guaranteed to drift.

Business statistics come from a **data-points registry** — wherever you keep it, as long as it is one
place — using its `display` field verbatim so qualifiers survive. The qualifiers exist for a reason.
Worked example: a community's job-title breakdown is counted from only the subset of members who
declared a title, so every count in it is a **floor**. Publish "N CTOs" without that denominator and
a partner reads the floor as a ceiling. The `display` string carries the denominator; a hand-copied
number loses it.

**Withheld figures stay withheld.** Some prices are deliberately unpublished. Filter them out by
structure rather than by id: exclude the tier key, so a future item keyed the same way inherits the
exclusion instead of shipping its price. Filtering only the preset and forgetting the line item is how
a withheld price got republished on 2026-08-06.

**robots.txt.** Point at both files with a comment line. Never declare them with `Sitemap:` — they are
markdown, and Search Console reports a declared non-XML sitemap as unreadable.

**Never mirror every page as markdown.** Per-page `.md` copies of a whole site, if indexable, are
duplicate content at scale.
