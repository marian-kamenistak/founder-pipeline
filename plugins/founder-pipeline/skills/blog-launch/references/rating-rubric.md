# Rating rubric — the 8/10 gate

Used by step 06. Three blind judges get the identical prompt below with the full post text. Aggregation: **median per dimension; pass = both medians ≥ 8**. Judges never see each other, the writer's context, or previous rounds' scores.

## Verbatim judge prompt

Fill the four placeholders from the site profile before dispatching: `{{AUTHOR_NAME}}`,
`{{AUTHOR_ONE_LINER}}` (what the author does, in six words), `{{SITE_DOMAIN}}`, and
`{{TARGET_READER}}` (the role the post is written for). Everything else is sent verbatim —
do not paraphrase the anchors, they are what makes scores comparable across rounds.

```
You are judging a blog post draft for {{AUTHOR_NAME}} ({{AUTHOR_ONE_LINER}}, {{SITE_DOMAIN}}). Judge ONLY what is on the page. Be harsh; 8 means "publish with pride", not "pretty good". Default skeptical: an unproven claim scores as a missing claim.

Score two dimensions, 0-10 integers:

SIMPLICITY — can a tired {{TARGET_READER}} read this on a phone at 22:40 and get it?
- Sentence and paragraph rhythm: short, breathable, no paragraph over 4 sentences.
- One idea per paragraph; no compound hedged sentences.
- Skimmability: do the H2s + bold lead-ins + table alone deliver ~70% of the value?
- Jargon only where the reader's world uses it.
Anchors: 9-10 = effortless, reads itself, visually inviting; 8 = clean with 1-2 dense spots; 6-7 = needs a second read in places, some walls of text; ≤5 = wordy, abstract, or visually monotone.

VALUE DELIVERED — does the reader walk away with something they will use?
- The tomorrow test: name the concrete thing a reader does differently tomorrow. If you can't, score ≤6.
- Evidence density: numbers, names, dates, linked sources; personal story that only the author could tell.
- Non-obvious: at least 2 insights the top-ranking posts on this topic do NOT contain.
- The generic-AI test: could a general-purpose chatbot have produced this post without the author's life in it? If mostly yes, score ≤5.
Anchors: 9-10 = I would send this to a client unprompted; 8 = clearly useful and personal; 6-7 = solid but exchangeable; ≤5 = restated common knowledge.

Return JSON only:
{
  "simplicity": <0-10>,
  "value": <0-10>,
  "flags": [
    { "quote": "<exact passage>", "problem": "<what is wrong, one sentence>", "fix_hint": "<direction, not rewrite>" }
  ]
}
Flag every passage that cost points. 3-8 flags typical; zero flags with scores <10 is invalid.
```

## Mechanical checks (linkcheck agent, must ALL pass — not scored)

- Every external link resolves (200/301); every internal link exists in the repo.
- Description 50-160 chars (target 120-155). Headline 40-49 chars target, no clickbait smell.
- ≥1 personal story or named lived example. ≥1 counter-voice cited.
- `/founder-pipeline:brand-voice` grep self-check clean (no em dashes, banned words/phrases, smooth transitions).
- Readability design: pull-quote present, no paragraph >4 sentences, **a real sourced number or the core definition within the first 60 words** (not buried in paragraph 3 — AI search engines lift the opening block), **a data table present** (rate/scope/comparison — required by AI-citation structure, not only when the post compares two named things).

## Rules

- **`/founder-pipeline:critical` runs alongside**; CRITICAL SCORE < 7 forces a revise round even if judges pass (it catches wrong-angle problems the copy rubric can't).
- Revise loop: writer receives **flags only, never scores**. Fresh judge panel each round. Max 2 revise rounds.
- Persistent fail → kill / park / override-publish, the owner's literal words required for override, all logged. Never silently publish, never silently kill.
