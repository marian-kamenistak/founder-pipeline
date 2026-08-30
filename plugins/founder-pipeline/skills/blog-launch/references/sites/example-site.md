# Site profile — example.com (template)

> **This is the worked example, not a live site.** Copy it to
> `references/sites/<your-site-slug>.md` and replace every value below with your own.
> One file per site you publish to. The steps only ever refer to "the site profile", so a
> second site needs no changes anywhere else in the pipeline.
>
> The example site here is **Example Advisory** (`example.com`), a fictional one-person
> advisory practice running an Astro blog with an English original and one localized mirror.
> Its stack matches the plugin's default house stack; if yours differs, this file is where
> the difference gets recorded.

Repo: the site's checkout path, from your own config — never hard-code an absolute path into
this file if the profile is shared. Read the repo's own agent instructions (`CLAUDE.md` /
`AGENTS.md`) before editing: its rules bind this pipeline.

## Content locations

- EN posts: `src/content/blog/<slug>.mdx` (slug = filename).
- Localized mirror: `src/content/blog/<lang>/<slug>.mdx`, `lang: '<lang>'`; differing localized
  slug → `pairedSlug` on BOTH files.
- Pipeline workspace: `.blog-pipeline/<slug>/` at repo root (gitignored).

## Frontmatter contract (Zod, `src/content.config.ts`)

```yaml
title: string                 # required
description: string           # 50-160 chars HARD; target 120-155; validates even on drafts
pubDate: 2026-07-21           # bare YAML date
updatedDate:                  # optional, only for real updates
tags: ['leadership']          # first tag sets articleSection + drives ServiceCTA
draft: true                   # until GATE B
lang: 'en'                    # default en; '<lang>' for mirrors
faqs:                         # optional → FAQPage JSON-LD; phrase as real PAA queries
  - q: "..."
    a: "..."
pairedSlug:                   # only when EN/localized slugs differ
```

## Rendering facts the writer must know

- Template (`src/pages/blog/[...slug].astro` + the localized mirror): injects BlogPosting +
  Breadcrumb + FAQPage JSON-LD, renders `faqs` as a visible "Frequently asked" `<details>`
  section, auto-appends `ServiceCTA` and `RelatedPosts`. Rendering the FAQs visibly rather than
  as schema only is deliberate — schema-only FAQs are a real SEO and AI-citation bug.
  **Don't hand-write a CTA card in the body**; one soft closing sentence only.
- **Title tag pattern (hard rule): `{post title} | {service}`, never `{post title} | {site name}`.**
  The `<title>` (and OG/Twitter title, since they read the same prop) is composed as
  `${post.data.title} | ${titleService.eyebrowEn}` (localized: `eyebrow<Lang>`) — see
  `src/pages/blog/[...slug].astro` and its mirror. The service comes from `src/data/services.ts`'s
  `chooseService(tags)`, the SAME shared module `ServiceCTA` uses for its bottom-of-post CTA card —
  one source of truth, don't duplicate the mapping. Pick tags for a new post with this in mind:
  the FIRST tag (in `tagToService` priority order, not array order — read `src/data/services.ts`
  for the current order) decides both the title suffix and which service gets pitched at the end
  of the post. Priority should favour **specific** tags over the one or two generic tags that end
  up on roughly half of all posts; a generic tag makes the post fall through to whatever service
  is last in the order. Tag deliberately so a post doesn't get the wrong offer attached by accident.
  Using `|` (not an em dash) as the separator is also how this satisfies the no-em-dash voice rule
  in the title tag.
- MDX gotchas: HTML comments `<!-- -->` break the build (use `{/* */}`); house posts import
  nothing except the step-05 image convention.
- Gallery: `src/assets/pics/index.ts` — `picBySlug`/`picsByKind`, with whatever `kind` vocabulary
  your gallery uses (this example: hero|portrait|action|talk|speaker|session). Import path from a
  blog MDX file: `../../assets/pics` (EN) / `../../../assets/pics` (localized).

## Internal-link targets (money pages)

List the site's commercial pages here so step 08 can link into them without re-deriving the set.
For the example site:

`/service-a/`, `/service-b/`, `/service-c/`, `/audit/`, `/statistics/`, `/pricing/`
(localized: `/<lang>/pricing-slug/`), `/testimonials/`, `/speaking/`.

Credential anchor: the one-line proof sentence the posts are allowed to cite — for example
`<N>+ sessions / <N>+ clients / <rating> average`. **Verify the current numbers on the live
homepage before citing them**; a stale credential number in a post is a claim you cannot support.

## Build & deploy

- Build check: `npm run build` (Zod validates all frontmatter, including drafts).
- Deploy: the site's own deploy script. If the deploy tool reads credentials from its **own
  process environment** rather than expanding them inline, make sure your secrets are exported
  into that child process, not merely sourced into the shell — a plain `source` silently falls
  back to weaker auth on some CLIs.
- Translation glossary: `TRANSLATION-GLOSSARY.md` at repo root, if the site has a localized
  mirror. It is law for the translation step.

## Post-publish checklist

1. **llms.txt**: add the post to the curated "Blog Posts" list in `public/llms.txt`
   (`llms-full.txt` regenerates itself from non-draft posts).
2. **CDN cache purge** (the edge serves stale HTML): purge the post URL plus both blog index
   URLs through your CDN's API.
3. Run **`/founder-pipeline:web-indexation`** for the post URLs (every language) — the mechanism
   and the rationale live in that skill. This profile only records the site's own identifiers:
   - **IndexNow key**: generate one per property and host the key file at the site root. Record
     *where* it lives here; never write the key value itself into a file that ships or is shared.
   - **Non-Google engines**: if your home market has a search engine with meaningful share
     alongside Google, record its force-reindex endpoint and per-second/per-day limits here.
   - **Search Console property**: record the property identifier (e.g. `sc-domain:example.com`).
     Append URLs to the shared reindex queue; never click Request Indexing directly — the quota
     is per account, so one click starves every other property you own.
4. **`/founder-pipeline:seo-audit` + `/founder-pipeline:ai-seo`** on the live URL; write findings
   back to the site's own case-notes file.

## Backlink register

Point at the site's backlink-target file and record the append convention, so per-post
placements land in a consistent place. For the example site: append per-post placements to the
lowest tier table, and log landed links under `## Progress log` as
`YYYY-MM-DD  <tier>/<ref> <target>  <URL>  <status>`.
