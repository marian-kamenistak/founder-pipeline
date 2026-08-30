# Reading layout: post body, tables, index cards

Presentation contract for the site's posts. Written after an audit found
the post template carrying its typography as one inline arbitrary-variant string with
**no rules at all for tables, lists, blockquotes or images** — every markdown table on
the site was rendering at bare browser defaults (no borders, no padding, no header
band, overflowing on mobile).

Everything here is CSS and template level. It applies to all posts at once and needs
no per-post edits. **Never paste table markup or typography classes into an `.mdx`
file** — a post that needs custom styling to read properly means this contract has a
gap; fix the contract.

## 1. Post body: `.post-body`

The body of every post is a single `<div class="post-body">`. All typography lives in
`src/styles/global.css` under the `.post-body` block. Do not reintroduce inline
`[&_h2]:…` variant strings on the template: they cannot express table, list, or
`::marker` rules, which is exactly how the tables got missed.

| Property | Value | Why |
|---|---|---|
| Measure | `max-width: 44rem` | The 48rem container runs ~85 chars per line at this size. 44rem lands at ~74, inside the 60-75 comfortable range. Left-aligned, so it stays flush with the h1. |
| Font size | `1.0625rem`, `1.1875rem` at `md` | 17px mobile / 19px desktop. Long-form needs a bigger step than UI text. |
| Line height | `1.75` | |
| Block rhythm | `> * + * { margin-top: 1.4em }` | One rule, in `em`, so spacing scales with the font-size step instead of being restated per breakpoint. |
| Heading attachment | `h2`/`h3` get large `margin-top`, **negative `margin-bottom`** | A heading must sit closer to the text it introduces than to the section above it. Without this, headings float equidistant and the page loses its structure. |

Also covered, and previously unstyled: `ul`/`ol` markers and indentation, `li` spacing,
`blockquote` (accent left rule), `img` (rounded, generous vertical margin), `hr`, `pre`.

## 2. Tables

Two pieces, both automatic:

1. **`rehypeWrapTables`** in `astro.config.mjs` wraps every markdown `<table>` in
   `<div class="table-scroll">` at build time, both locales. Markdown emits a bare
   `<table>` with nowhere to hang a scroll container; without the wrapper a 4-column
   table either overflows the phone viewport or crushes its columns. The wrapper also
   lets the table keep `border-collapse: collapse` and still show rounded corners —
   a collapsed table clips its own radius.
2. **`.post-body .table-scroll` / `table`** in `global.css` owns the look.

Design intent, since a table is *scanned in columns*, not read in lines:

- Header band in `--color-accent-soft` with `--color-accent-dark` text. This is the
  one place colour is used structurally in the body; it marks where a table begins
  without a heavy border.
- Zebra rows (`tbody tr:nth-child(even)` → `neutral-50`) so a wide row stays trackable
  across its full width, plus an accent-tinted hover row.
- First cell of each row is the label (criterion, option, role) in every table on this
  site, so it carries `font-weight: 500` and the darker text colour.
- Generous cell padding (`~0.8em 1em`), `vertical-align: top`, and a slightly smaller
  font than body copy (`0.9375em`) because table text is dense.
- Tables share the 44rem body measure. The wrapper is a child of `.post-body`, so a
  wider `max-width` on it is silently clamped — don't add one and assume it works.

## 3. Blog index cards (each locale's `/blog/` route)

One post per row, full width. Not a multi-column grid: at the 48rem container a
3-column grid gave each card ~240px, too narrow for a title plus an abstract.

- Layout `grid-cols-1 sm:grid-cols-[13rem_minmax(0,1fr)]` — featured image left,
  content right; stacks on mobile.
- The image is a **direct grid child** with `sm:aspect-auto sm:h-full object-cover`,
  so it stretches to whatever height the content column sets. Wrapping it in a div
  breaks the stretch.
- **Card title is 24px (`text-2xl`).** Fixed size, not a responsive step.
- Then the abstract (`description`, unclamped — the schema caps it at 160 chars).
- Then a row of up to 3 tags as pills, with the date pushed right via `ml-auto`.
- Tags render as `<span>`, never `<a>`: the card is already one big anchor and there
  are no tag archive pages to link to.

## Verification

After any change here, check the built output rather than the source:

```bash
# every table wrapped? both numbers must match
# (pass every locale's built blog directory, not just the default one)
grep -rho '<div class="table-scroll">' dist/client/blog/ dist/client/<lang>/blog/ | wc -l
grep -rho '<table' dist/client/blog/ dist/client/<lang>/blog/ | wc -l

# body class applied to every post
grep -rl 'class="post-body"' dist/client/blog/ dist/client/<lang>/blog/ | wc -l
```

`grep -rl 'table-scroll'` over `dist/` counts far more files than have tables —
`inlineStylesheets: 'always'` puts the CSS into every page. Match on the element
`<div class="table-scroll">`, not the bare string.

In the browser, confirm the measure landed: `charsPerLine` should be 60-75.

```js
const b = document.querySelector('.post-body'), c = getComputedStyle(b.querySelector('p'));
Math.round(b.getBoundingClientRect().width / (parseFloat(c.fontSize) * 0.5))
```
