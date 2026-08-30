# Last-modified dates — policy and rationale

Applies to every site this pipeline publishes to.
Loaded by `steps/05-images.md` (no), `steps/07-translate.md` (no) — this file is loaded by
`steps/09-deploy.md` and by any task that touches dates, sitemaps, or "refresh the old posts".

## The rule

**A last-modified date states that the CONTENT changed. Nothing else may move it.**

Not a rebuild. Not a deploy. Not a git commit. Not a cosmetic sweep across every post
(hero image swaps, typo fixes, component refactors, adding a schema field). Only a human
deciding "I revised this post" moves the date, and they move it by hand.

## Why old dates are safe and fake-fresh dates are not

There is **no ranking penalty for an old `dateModified`.** Evergreen posts rank fine with
old dates. A post from 2020 that has not been revised should keep saying 2020.

The risk runs the other way. Google uses sitemap `<lastmod>` for crawl scheduling **only
while it stays trustworthy** — it states it ignores the value on sites where it has proven
unreliable ([Google Search Central, sitemaps
documentation](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap)).
If lastmod looks noisy — every URL bumping on every deploy — Google stops trusting it and
discounts the signal **across the whole site**. One dishonest fallback poisons every URL on
the domain, not just the pages you touched. Inflated article dates are also a recognised spam
pattern [operating assumption].

So: an honest old date costs nothing. A fake fresh date costs the signal everywhere.

The genuine cost of a stale date is narrow and specific:
- Google may display the date in the SERP, which dents CTR on time-sensitive queries.
- Query-deserves-freshness ranking favours recent content for some queries.

Both are fixed by **actually refreshing the post** and then legitimately bumping
`updatedDate` — never by touching dates alone. Candidates are posts whose value decays:
anything with a year in the title, salary/comp data, tooling and AI posts, market claims.
Evergreen playbooks (1:1s, first 90 days, role definitions) should keep their original dates.

## Date source per page type

| Page type | Source of truth | Moves on a cosmetic sweep? |
|---|---|---|
| Blog post (every language) | frontmatter `updatedDate ?? pubDate` | **No** — manual only |
| Static / landing `.astro` | git last-commit date of that file | No — per-file, shared components don't touch it |
| Blog listing (each locale's index) | newest child post date | Only when a post actually ships |
| Anything unresolved | **omit `<lastmod>` entirely** | n/a — never emit a build date |

Omitting beats guessing. A URL with no lastmod is a URL Google crawls on its own schedule;
a URL with a wrong lastmod is a URL that teaches Google to ignore your sitemap.

## Where this is implemented (the worked example's Astro site)

- `scripts/gen-lastmod.mjs` — builds `src/generated/lastmod.json`. Reads post frontmatter
  for each locale's blog routes, git dates for `.astro` pages, newest-child for listings.
  The policy is repeated at the top of that file. Runs before every build.
- `astro.config.mjs` — sitemap `serialize()` reads that map. Explicitly refuses to emit
  `lastmodMap.__build` as a lastmod value.
- `src/layouts/Layout.astro` — `WebPage.dateModified` and `article:modified_time`.
  `modified_time` is **always** emitted; for a never-revised post it equals
  `published_time`, which is the truthful statement, not a missing field.
- `src/pages/blog/[...slug].astro` + each localized twin — `BlogPosting.dateModified` from
  `modifiedISO = (updatedDate ?? pubDate)`.

## Checks

```bash
# Post dates must survive a content-file sweep. Run before and after any bulk edit:
curl -s https://<your-domain>/blog/<slug>/ | grep -o 'article:modified_time" content="[^"]*"'

# Sitemap: every URL either has an honest lastmod or none. Zero should carry today's date
# unless a post genuinely shipped or was revised today.
curl -s https://<your-domain>/sitemap-0.xml \
  | grep -o '<lastmod>[^<]*' | sort | uniq -c | sort -rn | head
```

If a bulk edit ever does move dates, that is a bug in `gen-lastmod.mjs` — fix the generator,
do not paper over it in the template.

## When someone says "refresh the old posts"

Two different jobs, never conflate them:
1. **Cosmetic/structural** (images, schema, components, links) → dates must NOT move. Ship it.
2. **Content revision** (new sections, updated numbers, re-argued claims) → set `updatedDate`
   on the posts you actually revised, each language independently if only one was rewritten.

Anyone proposing "bump all the dates so Google sees the site as fresh" is proposing the
one thing that reliably makes it worse. Say no and point at this file.
