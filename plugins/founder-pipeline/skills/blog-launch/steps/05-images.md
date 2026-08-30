# Step 05 — Images from the gallery

Runs as a **cheap-model subagent, in parallel with step 04** (depends only on the skeleton's image slots).

> **Imagery rules are shared between posts and pages.** If your install has a dedicated imagery skill,
> it owns the sourcing ladder (real photographs before anything generated, and never a generated photo
> of a person, room or event), the three-picture floor, the featured-image contract, the optimisation
> criteria and the alt-text rule — read it first and let it win where it is newer. Otherwise this file
> is the whole contract: it states those rules inline below, plus the blog-specific application (the
> frontmatter field, the MDX block, the uniqueness check against live posts).

## Source

The site profile names the gallery registry — the shipped worked example uses an Astro image registry at `src/assets/pics/index.ts` holding ~77 images typed `Pic { slug, src, alt, kind: hero|portrait|action|talk|speaker|mentoring }`, with helpers `picBySlug`/`picsByKind`.

**Allowed image sources** (this list replaces any older gallery-only rule):
1. **Gallery photos** — the registry above; still the default for hero/personal shots.
2. **Screenshots** — real product/tool/result screenshots (a PageSpeed score, a before/after of
   a site, a dashboard). These are often MORE relevant than a photo on evidence-driven posts;
   label them honestly (what + when captured). Still **never client-confidential screenshots**.
3. **AI-generated images — for infographic-style pictures ONLY** (a numbers card, a diagram, a
   process visual). Never AI-generated "photos" of people, places, or fake product shots.
4. **Stock photos: never.**

Post-specific screenshots/infographics live in `public/images/blog/<slug>/` and are referenced
with plain markdown (they're pre-optimized; they don't join the gallery registry). If the post
needs a data CHART from real data, that is a charting job for step 04 — render the chart from the
underlying figures there and treat it as a body image, not a gallery pick.

## The featured-image contract (all four clauses are blocking)

One field feeds four surfaces. Get `heroImage` wrong and all four break together — this is why they're one checklist, not four:

```
heroImage: '<gallery-slug>'        → picBySlug()
  ├─ blog index card thumbnail     (<img>, aspect-[16/9])
  ├─ og:image                      (getImage 1200×630 jpg, absolute URL)
  └─ BlogPosting JSON-LD `image`   (same absolute URL)

fallback if no heroImage → first inline body image (legacy /images/blog-covers/<slug>.*)
fallback if neither     → the site-wide default og image  ← generic. Means the post FAILED this contract.
```

1. **Unique** — the featured image must not repeat any other live post's featured image in the same language.
2. **Present in the primary language _and_ every localisation** — a localised mirror with no featured image of its own is a failed post, not a partial one.
3. **Resolves to a real og:image + a real card thumbnail** — verified live, not assumed from frontmatter.
4. **Carries BlogPosting JSON-LD** — the layout emits it automatically; your job is to confirm it emitted with a real `image`, not the generic fallback.

Steps 05 and 07 satisfy clauses 1-2. Step 09 verifies clauses 3-4 on the live URL.

## Select

**Every post ships with a featured image, mandatory — no zero-image posts, ever. And the pipeline
DECIDES the featured picture itself — it never ships without one and never punts the choice back to
the owner.** When a post is evidence-driven, an infographic or screenshot cover (via the body-image
fallback below) may beat a gallery photo — decide by what best represents the post on a social share
card. The hero doubles as og:image (social share preview) and the blog-listing thumbnail, so a post without one is invisible on social shares and looks broken in the index grid. Pick the single most representative shot (kind `hero`/`portrait` for personal-story posts, `talk`/`mentoring`/`speaker` for practice or event-tied posts) and set it as `heroImage` in frontmatter — this is a gallery slug string, not an MDX block:

```yaml
---
title: "..."
heroImage: 'mentoring-04'
---
```

## The body-image floor (blocking)

**≥2 inline images in the body, on top of the hero. Three pictures per post is the floor, not the target.**

This rule exists because the older wording said "add 1-2 inline images" and was the only mention of body imagery anywhere in the pipeline. Nothing counted them, so an entire six-post site shipped with exactly one picture each — the hero — and passed every gate on the way. The count is now verified in the built output at `steps/09-deploy.md`.

- **The hero never counts toward the two.** It renders as the card thumbnail and the og:image; a reader scrolling the article has already passed it. Don't reuse the hero as an inline pick.
- **Every localisation carries its own two.** A localised mirror inherits the body structure, so it inherits the slots — but the alt text is written in the mirror's language, not copied from the source. Step 07 owns that.
- **Placement is per skeleton section, not decorative.** One image per major section it actually illustrates: a talk/mentoring shot for practice sections, a workshop/breakout shot for method sections, a portrait only if the post is personal-story-heavy. After the section's first paragraph, never immediately before an H2.
- **Alt text is a description, not a caption or a keyword slot.** Say what is in the frame, specifically enough that someone who cannot see it knows what they missed. Where the gallery catalog carries a `description` field per image, that is the right register and the right starting point — the site profile names the catalog file.
- **Nowhere to put a second one means the skeleton is thin.** Fix it in step 03; never waive the clause here.

Total pictures per post: **3+** (1 hero + 2 or more inline).

**Hard rule: `heroImage` must be unique across every live (non-draft) post in the same language — not just the last 3.** The blog index shows every post's card at once, so any repeat is visible in the same grid, and on an estate with roughly as many posts as gallery images, "check the last 3" silently produces the same photo on 10+ cards over time (a confirmed regression on a real site). Before picking, check what's actually taken:

```bash
grep -h "^heroImage:" src/content/blog/*.mdx | sort | uniq -c | sort -rn        # primary language
grep -h "^heroImage:" src/content/blog/<lang>/*.mdx | sort | uniq -c | sort -rn # localisation
```

Pick a slug with count 0 (or the lowest count) in the target language's list. Languages are checked separately — a post and its own localised mirror may share an image, that's not a repeat.

**Never set `heroImage` on a post whose body already embeds a legacy per-post cover** (`![...](/images/blog-covers/<slug>.*)` or a similar archive path — these are unique, pre-existing images from a previous CMS's archive, one per post, not from this gallery). `heroImage` frontmatter always wins over that body image on both the listing card and the og:image, so adding it silently hides the post's original unique cover behind a generic reused gallery photo. Check first: `grep -l "!\[.*\](/images/blog-covers/" src/content/blog/<slug>.mdx` — if it matches, leave `heroImage` unset entirely and let the listing/post-page fallback pick up the body image automatically.

**The body-image fallback only counts if the first image is an actual cover.** The fallback regex grabs the *first* `![](...)` in the body, whatever it is — on legacy imports that's sometimes a 96px avatar, a logo strip, or a mid-article diagram, which then becomes the card thumbnail and the og:image at 1200×630 (another confirmed regression). Look at what the fallback will actually pick before trusting it:

```bash
grep -m1 -o '!\[[^]]*\]([^) ]*' src/content/blog/<slug>.mdx    # what the card will show
```

If it's not a real cover, either place the proper `/images/blog-covers/<slug>.*` file as the first body image (alt = post title, right after the imports), or set a gallery `heroImage`.

## MDX convention (inline images — this file defines it)

```mdx
import { Image } from 'astro:assets';
import { picBySlug } from '../../assets/pics';

<figure style="text-align:center">
  <Image src={picBySlug('talk-08').src} alt={picBySlug('talk-08').alt} width={720} />
  <figcaption>Community meetup #37. Photo: the event organiser.</figcaption>
</figure>
```

- Import path is relative to the MDX file (the site profile confirms depth).
- Alt comes from the registry (already descriptive); caption is short + sourced, centered.
- Place after the section's first paragraph, never before an H2.
- The hero image needs no import/figure — it's a plain `heroImage: '<slug>'` frontmatter field; the post page and listing page resolve it via `picBySlug` automatically and generate the og:image at build time.

## Output

Return to the main loop: chosen `heroImage` slug + inline slugs + ready-to-paste MDX blocks + placement notes. The step-04 writer merges them. Verify the build still passes after merge.

Update `STATE.md`. **Next:** `steps/06-gate.md`
