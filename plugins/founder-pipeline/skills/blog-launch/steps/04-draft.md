# Step 04 — Draft: content + citations + voice pass

**One writer, one context, session model, high effort. Per-section fan-out is forbidden** — parallel sections produce seams, repeated setups, and a dead narrative arc. This is the "don't go cheap on copy" rule made structural. The story has to talk to the reader.

Keep `references/writing-style.md` loaded (structure) and invoke `/founder-pipeline:brand-voice` (sentences). Both are mandatory, in that order of concern.

## 1. Write the draft

Follow the skeleton. While writing:

- **The owner's raw material is the spine.** The drafter does NOT start from the brief alone. First run a raw-material intake: interview the owner for the story, the scar, the numbers and the contrarian line, and write the transcript to `.blog-pipeline/<slug>/raw-material.md` with an explicit **KEEP VERBATIM** zone. Load that file before writing a word, and keep everything in the KEEP VERBATIM zone as SENTENCES — non-native quirks, odd rhythms and all. The pipeline arranges the owner's sentences, it does not replace them. Their phrasing is the one thing no detector or skeptical reader can call AI. If the intake produces no story or no data, the post does not get written yet; report that instead of drafting around the hole. (The evidence for this rule: a detector audit of one blog estate found pipeline-written posts scoring 52-75% AI-likely against 7-25% for the same author's hand-written posts, and the skeletons with an unfilled "the owner's specific scars" slot were the worst of all.)
- **Citations are written IN, not bolted on.** Every number/name/date gets its inline Markdown link the moment it's written. Counter-voices: state the opposing view fairly with a link, then rebut it with evidence. If a claim can't be sourced — from an external link, or from your own internal data-points store if you keep one — cut it or ask the owner.
- **No vague quantity words.** Don't write "many engineers", "often", "a few teams", "rarely" — AI search engines quote numbers, not hedges. When the draft wants a vague quantifier, dispatch a subagent to find a real, citable source for that specific claim (industry report, survey, study, official stat). Cite the result inline as `[the number itself](source URL)` — the house convention (e.g. `[3,360 survey submissions as of March 2026](url)` inside the sentence that uses the figure) — or, if it doesn't sit naturally in the sentence, list it under a "Sources" section at the bottom of the post. If the subagent finds nothing solid, cut the claim rather than reach for the vague word.
- **Personal story** placed where the skeleton planned it, told as lived experience ("It happened to me in..."), names of private individuals virtualized.
- **Design for readability while drafting:** paragraphs 1-3 sentences; a number/name/date roughly every 150 words; bold lead-ins on list items; ONE pull-quote (blockquote) carrying the post's sharpest sentence; the comparison table where planned; vary block shapes so no screen of the post is a uniform text wall.
- **Internal links** woven into prose per skeleton; CTA is one soft sentence at the end linking a money page — where the site template auto-appends a service-CTA card (the site profile says whether yours does), keep the hard sell out of the body.

## 2. Voice pass (same context, mandatory)

Invoke `/founder-pipeline:brand-voice` on the full draft: banned AI words/phrases, no em dashes, no smooth transitions, no optimistic bow, outputs→outcomes, then run its grep self-check until clean. Also load the voice fingerprint that `/founder-pipeline:humanize` ships for your language and check the draft against it — especially the second-order tells (epigram density, fragment-contrasts, uncontracted register) and the corpus-level checks: grep the site's published posts for the draft's coinages and best lines (zero reuse allowed), and confirm the scaffold differs from sibling posts. Optionally run `/founder-pipeline:marketing-psychology` on the closing CTA framing only.

## 3. Assemble the MDX

Per the site profile's frontmatter contract:

- `title`, `description` (write to 120-155 chars; hard schema limit 50-160 — validates even on drafts), `pubDate` (today, bare YAML date), `tags` (drive BOTH the auto-CTA and the `<title>` tag suffix — choose deliberately, see the site profile's title-tag pattern), `faqs` (the PAA Q&As), **`draft: true`**.
- **FAQ answers must render as visible page content, not schema-only (hard rule).** The `faqs` frontmatter feeds both the FAQPage JSON-LD AND a visible "Frequently asked" `<details>` section on the page (the site profile confirms the template renders it — verify before relying on it for a new site). Schema-only FAQ answers violate Google's structured-data guidelines (markup must match visible content) and can't be lifted as AI-search citations. This is a real bug worth checking for: a post template that emits the schema but never the text passes every frontmatter check and still fails the guideline.
- Body: pure Markdown + the image imports from step 05 when it lands. No HTML comments (`<!-- -->` breaks MDX builds; use `{/* */}`).
- **Heading levels start at `##` (hard rule).** The page's `<h1>` is the frontmatter `title`, rendered once by the template — a body `#` compiles to a *second* `<h1>`. A single site-health audit found this on 12 published posts at once, one of them carrying 12 `<h1>`s because every section header used `#`. Section headers from the skeleton are `##`; anything nested inside one is `###`, then `####` — one level down at a time, never skipped, never a body `#`.
- **Provenance footer.** Close the post with a plain last line like `[Writing time: 9h]` — the number must be REAL (ask the owner how long the post actually took them end-to-end, including the raw-material dump and review; never invent it — a fake provenance signal is worse than none). When a post is later revised because of real reader feedback, append a messy dated note in place ("Update 2026-08: a reader pushed back on §3, they're right") instead of silently editing — a visible correction trail is stronger provenance than any metatag. Honest `updatedDate` per `references/dates-and-freshness.md` accompanies any such revision.
- File at the site profile's primary-language content dir under the locked slug.

Run the site build once (`npm run build` in the repo) to catch schema/MDX errors now, not at deploy.

Update `STATE.md`. **Next:** `steps/06-gate.md` (once step 05 has merged its images).
