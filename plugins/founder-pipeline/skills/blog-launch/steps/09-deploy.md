# Step 09 — GATE B → deploy → post-publish

## GATE B (blocking — the second and last human gate)

**GATE B is the merged PR, and nothing else.** Not a chat message saying yes, not a verbal go, not an inference from a previous standing instruction. It has two acts, completed at step 08b:

1. **The reviewer sets `Review` = `Approved`** on the post's row on the blog-ideas backlog. They own the copy judgment.
2. **The owner merges the PR.** They own the button.

If either is missing, this step does not run. Verify both before doing anything below: read the row's `Review` field, and confirm the PR is merged (not just approved) — then set `gate_b` in `STATE.md` to the merge date.

The merge is what flips `draft: true` → `false`, so there is no way to deploy an unapproved post without deliberately editing frontmatter by hand.

**If the owner asks to ship without review** (urgency, a post they wrote themselves, a trivial fix): that's their call to make and they can make it, but it is an *override*, not a skip. Record it in `STATE.md` as `gate_b: <date> — override, owner's words: "<literal quote>"`, and say plainly in the checkpoint that the post went out unreviewed. Never let an override become the silent default for the next post.

Only after GATE B:

## Deploy (main loop, bash)

Throughout this step, **the site config** means that site's file under `${CLAUDE_PLUGIN_ROOT}/skills/blog-launch/references/sites/<site-slug>.md` — one per property you publish to, copied from `example-site.md`. It holds the deploy command, the routes, the `llms.txt` location, the IndexNow key and the site's own gotchas.

1. Flip `draft: false` on the primary-language post (and every translated mirror that exists). Re-verify description lengths.
2. Update the curated blog list in the site's `llms.txt` (the site config says where; llms-full regenerates itself).
3. Commit per repo convention — the post, its translated mirrors, AND the step-08 inbound-link edits ship in one commit; `npm run deploy` (or the site config's deploy command).
4. Verify live: curl the post URL in every language, check title + one body string render. Also curl the blog index in each language and confirm the new post's card has an `<img` tag, not the gray placeholder `div` — a correct `heroImage` in frontmatter with a deploy that silently failed (see the site config's env-export gotcha) or got skipped still ships a card with no image, and title/body checks alone won't catch it.

5. **Verify the featured-image contract on the live URL** (clauses 3-4, `${CLAUDE_PLUGIN_ROOT}/skills/blog-launch/steps/05-images.md`). Frontmatter being right is not evidence the deploy produced the right output — run this against every language:

```bash
for u in https://www.example.com/blog/<slug>/ https://www.example.com/<lang>/blog/<translated-slug>/; do
  echo "== $u"
  curl -s "$u" | grep -o '<meta property="og:image" content="[^"]*"'
  curl -s "$u" | grep -o '"@type":"BlogPosting"' | head -1
  curl -s "$u" | python3 -c "import sys,re,json;h=sys.stdin.read();
d=[json.loads(m) for m in re.findall(r'<script type=\"application/ld\+json\">(.*?)</script>',h,re.S)]
b=[x for x in d if x.get('@type')=='BlogPosting'][0]
print('LD image :',b.get('image'));print('LD headline:',b.get('headline'));print('LD datePublished:',b.get('datePublished'))"
done
```

Three failure signals, all blocking:
- og:image or `BlogPosting.image` is the **site-wide default OG image** → the post has no featured image at all; the generic site fallback fired. Go back to step 05. (Know your site's fallback filename before you run this check, or you will read the fallback as a pass.)
- og:image points at something tiny or off-topic (a logo, an avatar, a mid-article diagram) → the body-image fallback grabbed the wrong `![]()`. Go back to step 05.
- No `BlogPosting` script tag → the layout didn't get `extraSchemas`; the post page is missing its schema wiring entirely.

Then confirm uniqueness held after the merge — nothing else on the index may share this post's featured image:

```bash
grep -h "^heroImage:" src/content/blog/*.mdx         | sort | uniq -d   # primary — must print nothing
grep -h "^heroImage:" src/content/blog/<lang>/*.mdx  | sort | uniq -d   # each translation — must print nothing
```

Optional but cheap: paste the live URL into a social-card inspector and Google's Rich Results Test to see the card and the parsed BlogPosting as the platforms see them.

5b. **Count the pictures on the live post** (SKILL.md three-pictures hard rule). Everything above verifies the featured image four different ways and none of it notices a post with no body images at all — which is how a whole blog can ship with exactly one picture per post and nobody spot it. Site chrome (nav logo + footer mark) is commonly ~2 `<img>`, so **hero + 2 body = 5 is a typical floor** and a post sitting at 3 has an empty body:

```bash
for u in https://<domain>/blog/<slug>/ https://<domain>/<lang>/blog/<slug>/; do
  echo "$(curl -s "$u" | grep -o '<img' | wc -l | tr -d ' ')  $u"   # < floor → blocking
done
```

Confirm the chrome count for the target site once (`curl` any text-only route) instead of assuming 2, and set the floor from that. Below the floor is blocking and goes back to `${CLAUDE_PLUGIN_ROOT}/skills/blog-launch/steps/05-images.md` — never ship it as "thin but fine". While you are here, check the index card actually got a thumbnail: a listing template that never reads the featured-image field renders text-only cards no matter how correct every post's frontmatter is.

6. **Verify the technical-SEO contract** (SKILL.md hard rule). These are emitted by the layout and the post template, so they fail silently and site-wide rather than per-post — check them on every deploy, not just new posts:

```bash
U=https://www.example.com/blog/<slug>/
curl -s "$U" | grep -o 'name="robots" content="[^"]*"'          # must include max-image-preview:large
curl -s "$U" | grep -o 'article:modified_time" content="[^"]*"' # must be present
curl -s "$U" | python3 -c "import sys,re,json;h=sys.stdin.read()
b=[json.loads(m) for m in re.findall(r'<script type=\"application/ld\+json\">(.*?)</script>',h,re.S)]
d=[x for x in b if x.get('@type')=='BlogPosting'][0]
need=['datePublished','dateModified','wordCount','timeRequired','isAccessibleForFree','image','publisher','author']
print('missing:', [k for k in need if k not in d] or 'none')
print('author  :', d['author'])          # must be an @id ref to the site's Person/Organization node
print('image   :', d['image'])           # ImageObject; dimensions ONLY if genuinely 1200x630
print('logo    :', d['publisher'].get('logo','MISSING'))"

# Sitemap: honest lastmod or none. Nothing should carry today's date unless it shipped today.
curl -s https://www.example.com/sitemap-0.xml | grep -o '<lastmod>[^<]*' | sort | uniq -c | sort -rn | head -5

# Listing thumbnails must be responsive (grep -o, not grep -c — the HTML is one line).
curl -s https://www.example.com/blog/ | grep -o 'srcset=' | wc -l    # > 0
```

**Date sanity check before and after any bulk content edit** (see `${CLAUDE_PLUGIN_ROOT}/skills/blog-launch/references/dates-and-freshness.md`). Pick two old posts you did NOT revise and confirm their dates did not move. If they did, the generator is lying — fix the lastmod generator, never the template.

## Post-publish checklist (the site config has the exact commands)

- **Purge the CDN/edge cache** for the new/changed URLs (post URL, blog index, every language variant). In the default house stack that is a Cloudflare cache purge; on any other host it is the equivalent invalidation call.
- Run **`/founder-pipeline:web-indexation`** for the new post URLs in every language: IndexNow ping + Google reindex queue. The site config holds that site's IndexNow key and the exact curl commands — never click Request Indexing directly in Search Console.
- **`/founder-pipeline:seo-audit` + `/founder-pipeline:ai-seo`** passes on the live URL. Run both after any content change, and write the findings back to whatever case-notes file the site repo keeps, so the next post starts from what the last one learned.

Update `STATE.md` with the live URLs. **Next:** `${CLAUDE_PLUGIN_ROOT}/skills/blog-launch/steps/10-syndicate.md` ∥ `${CLAUDE_PLUGIN_ROOT}/skills/blog-launch/steps/11-backlinks.md` ∥ `${CLAUDE_PLUGIN_ROOT}/skills/blog-launch/steps/12-announce.md`.
