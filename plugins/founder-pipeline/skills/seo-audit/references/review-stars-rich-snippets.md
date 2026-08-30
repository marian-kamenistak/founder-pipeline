# Review stars in search results (rich snippets)

How to earn the ⭐ 4.6 (300) star rating under a search result. This is a *review snippet* Google
generates from `AggregateRating` / `Review` structured data. You earn eligibility; Google decides
whether to render it (days to weeks, never guaranteed).

Run this **after a page with genuine ratings/testimonials is built**
(`/founder-pipeline:web-site-creator` Phase 6), or as a fix when an SEO audit finds a
testimonials/service page with no stars.

---

## The one rule that kills most attempts

Google does **NOT** show self-serving review stars when the rating is attached to
`LocalBusiness`, `Organization`, or their subtypes (`ProfessionalService`, `Consultant`, etc.).
A business rating *itself* on those types is ineligible — the markup validates but stars never appear.

**Fix:** attach the rating to an eligible, self-serving-*allowed* type that represents the *offering*,
not the company:

- `Product` — safest, most widely supported. Use for a service/coaching/mentoring offer.
- `Course` — if it's a structured program.
- `Event`, `Book`, `SoftwareApplication`, `Recipe` — where they genuinely apply.

`Service` / `ProfessionalService` are **not** in Google's review-snippet supported list — don't rely on them.

---

## The four requirements (all must hold)

1. **Eligible type** — `Product` (see above), not `LocalBusiness`/`Organization`/`Service`.
2. **Rating visible on the page** — a user must *see* the stars/score, not just the markup. Render
   visible star icons + a score. Markup-only ratings are ignored and can trigger a manual action.
3. **Honest counts** — use the schema.org distinction:
   - `ratingCount` = *all* ratings (e.g. every survey score you hold).
   - `reviewCount` = *written* reviews actually shown on the page (e.g. the quotes rendered below).
   - Never claim a count the page can't back. A `reviewCount` matching your survey total while the
     page shows a handful of quotes is the "Incorrect number of reviews" manual-action trigger.
4. **Genuine reviews** — real people, real ratings. Invented ratings violate the guidelines.

If the aggregate comes from data not shown individually (surveys, CRM), display a **visible aggregate
stat block** ("<score>/10 from <N> clients") so the markup matches what a visitor sees. Confirm the
underlying data is defensible before publishing the number — it goes public.

---

## Recipe (Astro example, generalizes to any stack)

**a) JSON-LD** — one `Product` per page carrying the aggregate (+ nested `review[]` only where the
written reviews are actually visible on that page):

```js
const productReviewSchema = {
  '@context': 'https://schema.org',
  '@type': 'Product',
  name: '<Offer name> by <Brand>',
  description: '<One-line description of the offering being rated>.',
  url: 'https://www.example.com/offer/',
  brand: { '@type': 'Brand', name: '<Brand>' },
  aggregateRating: {
    '@type': 'AggregateRating',
    ratingValue: String(agg.score), bestRating: '10', worstRating: '1',
    ratingCount: String(agg.total),     // all ratings (surveys + written)
    reviewCount: String(reviews.length) // written reviews shown below
  },
  review: reviews.map(r => ({           // include ONLY where reviews are visible
    '@type': 'Review',
    author: { '@type': 'Person', name: r.name, ...(r.linkedin && { url: r.linkedin }) },
    reviewRating: { '@type': 'Rating', ratingValue: '5', bestRating: '5' },
    reviewBody: r.quote,
  })),
};
// inject via the page's schema slot (Astro: extraSchemas={[..., productReviewSchema]})
```

On pages that show *no* written testimonials (homepage, landing pages): keep `aggregateRating`
(with a visible score badge), **drop the `review[]` array** — don't ship reviews the page doesn't display.

**b) Visible stars** — render actual star icons next to each testimonial AND/OR an aggregate badge:

```jsx
<div role="img" aria-label={`${agg.score} out of 10`}>
  {[0,1,2,3,4].map(() => <StarIcon fill="#F5A623" />)}
</div>
<span><strong>{agg.score}/10</strong> from {agg.total} clients who rated the work.</span>
```

**c) Purge the ineligible rating** — if the site-wide layout has an `aggregateRating` on
`ProfessionalService`/`Organization`, **remove it**. It renders on every page, produces no stars,
and its count (with no reviews present) is a penalty risk.

---

## Validate + submit (do this yourself; needs the user logged into GSC)

1. **Deploy** the page(s).
2. **Google Search Console → URL Inspection** → paste the URL → confirm **"Review snippets: N valid
   items detected"** (N = reviews + 1 aggregate). This is stronger proof than the Rich Results Test
   because it's Google's own live read. Also check Breadcrumbs/HTTPS/indexed.
3. Do NOT click **Request Indexing** directly — the quota is per Google ACCOUNT, so every site you
   own shares one budget and one click can starve the others. Queue each URL (and every locale
   mirror) via `/founder-pipeline:web-indexation` instead, and work the resulting manual-click list
   oldest-first until the quota wall. (Step 2's URL Inspection read is fine to do directly —
   inspection isn't the scarce quota, the Request Indexing click is.)
4. Also ping **IndexNow** if wired (`/founder-pipeline:web-site-creator` Phase 6) — direct and
   immediate, never queued.
5. Track appearance in **GSC → Enhancements → Review snippets** over 1–2 weeks. Stars are eligible,
   not guaranteed — Google renders them algorithmically.

---

## Rollout tip

If persona/landing pages share a component (e.g. a single `PersonaPage` layout), add the `Product`
schema + visible badge **once in the shared component** — every page using it becomes eligible in a
single edit. Request indexing on the top few; Google recrawls the rest.
