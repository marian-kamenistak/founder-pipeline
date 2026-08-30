# Step 07 — Secondary-language mirror

Runs after the gate passes, **in parallel with step 09's export prep**. Your top-tier model, high effort — the translated version is copy too.

Skip this step entirely if you publish in one language only.

**Translation method.** If you have a dedicated page-translation skill installed, invoke it on the approved primary-language post and let it own the method. If not, do it inline — the method that works is: a *semantic rewrite* rather than a literal translation, a project translation glossary treated as law for every recurring term, a spellcheck pass with a tool that actually understands the target language's morphology, an automated adequacy score (CometKiwi or equivalent) to catch silent meaning drift, and a final read-through as a native editor rather than a translator. Do not ship machine output unedited.

This step only supplies the blog-specific contract from the site profile in `${CLAUDE_PLUGIN_ROOT}/skills/blog-launch/references/sites/<site-slug>.md`:

- Translated file at the secondary-language content dir (for example `src/content/blog/<lang>/<slug>.mdx`), same slug + `lang: '<lang>'`; if a localized keyword slug is genuinely better, use `pairedSlug` on BOTH files.
- Frontmatter translated (title, description 50-160 chars, faqs); `pubDate` matches the primary-language post; **`draft: true`** — it flips together with the primary at step 09.
- Internal links → `/<lang>/...` variants where the translated page exists, else keep the primary path.
- Image blocks: keep imports/slugs identical, translate alt/captions.
- **Featured image is mandatory on the mirror too** (contract clause 2, `${CLAUDE_PLUGIN_ROOT}/skills/blog-launch/steps/05-images.md`). The translated post resolves its card thumbnail, og:image and `BlogPosting.image` from its *own* file — it inherits nothing from the primary. Two valid ways to satisfy it, in order of preference:
  1. The primary uses a legacy body cover → reuse the same `/images/blog-covers/<primary-slug>.*` file as the translated post's first body image, placed right after the imports, `alt` = the translated title. Same file, same position, translated alt.
  2. The primary uses a gallery `heroImage` → give the mirror its own `heroImage`, unique within the mirror's list (see the per-language grep in step 05). Sharing the primary's slug is permitted but a distinct shot from the same shoot reads better on the index.

  Never let the mirror fall through to whatever diagram or logo happens to sit first in its translated body. This is not hypothetical: on one site a whole back catalogue of mirrored posts — dozens of them — ended up using mid-article screenshots as their social preview, because nobody had checked that the mirror resolves its image independently. Verify before moving on:

  ```bash
  # every mirrored post must have heroImage OR a real first body image
  for f in src/content/blog/<lang>/*.mdx; do
    grep -q "^heroImage:" "$f" || grep -q '!\[' "$f" || echo "NO FEATURED IMAGE: $f"
  done
  ```
- Numbers per the target language's typography conventions, per the glossary. *Worked example — Czech:* decimal comma, thin-space thousands separator. Most languages have at least one such rule and getting it wrong is an instant tell that the page was translated rather than written.

Skip rule: if the brief marked the post primary-language-only (essays aimed at an English-only community often are), record the skip in `STATE.md` and move on — don't translate by inertia.

Build once to confirm the translated file compiles. Update `STATE.md`. **Next:** wait for steps 08 and 10-prep, then GATE B in `${CLAUDE_PLUGIN_ROOT}/skills/blog-launch/steps/09-deploy.md`.
