# Writing style — essay architecture

Structure lives here. Sentences live in `/founder-pipeline:brand-voice` (banned AI words/phrases, no em dashes, no smooth transitions, grep self-check) — run it after drafting, don't duplicate it. Sources: your own accumulated house style, your three style north stars, and the posts on your site that already work.

## The three north stars

Name three writers whose posts you want yours to read like. They have to be specific people whose
archive you can go and read, because the whole pipeline calibrates against them — "authoritative but
approachable" is not a north star, it is a mood. Replace the three below with your own; they are
kept here because the *three roles* are what matters, not these particular authors.

- **A personal-story essayist** (worked example: Justin Welsh, justinwelsh.me/essays): the post is a personal story. "It happened to me." When protecting someone, give them a virtual first name ("Let's call him Tomas"). The lesson emerges from the story; it is never announced first.
- **A dense, zero-filler practitioner** (worked example: Jade Rubick, rubick.com/posts): straight to the point, insight-dense. Every paragraph earns its place or dies. If a paragraph could open any post on the topic, it's filler.
- **A say-the-thing writer** (worked example: John Cutler, cutlefish.substack.com): direct. No throat-clearing, no "let's explore".

## Spine

Practice, not theory. How-tos, not concepts. The default outline (order may bend to serve the story):

1. **Problem** — the reader's situation, named concretely.
2. **Solution** — the position. Contrarian where the author actually is, never contrarian as a pose.
3. **How to get there** — steps the reader can run tomorrow.
4. **Lessons learned** — the scars, what they'd do differently.

Definitional-keyword posts additionally: definition of the concept inside the **first 60 words** — AI search engines lift the opening block as the citable unit, not whatever shows up in paragraph 3 — one data table, FAQ candidates for the `faqs` frontmatter. The two shapes that reliably win AI citations:

- **The price post** — "what does X cost": the rate in sentence one, a full rate table segmented by the two or three variables that actually move the price, and a 4-question FAQ.
- **The distinction post** — "X vs Y vs Z": the definition in sentence one, a comparison table with one row per option, and a 5-question FAQ.

Keep your own best-performing post of each shape listed in the site profile as the local exemplar to copy from.

## Openings

- Cold open. Start in the middle. **First paragraph carries a real, sourced number or the core definition within the first 60 words — not optional, this is the block AI search engines quote verbatim.** The two shapes, in the abstract: a price sentence ("<service> costs <low> to <high> per <unit> in <market>.") or a definition sentence ("A <role> is a <category> who <the one distinguishing thing>, usually while still <the thing people assume they stopped doing>."). No number exists naturally yet? That's what step 04's number-finding subagent is for — never ship a vague-quantifier opening.
- No "In this post I will". No context-setting paragraph. The reader's problem or the claim, sentence one.

## Evidence density

- A number, name, or date roughly **every 150 words**. All from real sources (inline link) or your own verified data-points store. Never invented.
- Counter-voices: cite the strongest opposing take fairly (named, linked), then rebut with evidence. One per post minimum.
- Internal links: 2-4 money pages + 1-3 previous posts, woven into prose with meaningful anchors.

## Headlines

- Target 40-49 characters. Forms that work: number-led, "How to…", "Why you should…", question + "can" ("How Can <audience> Gain <outcome>?"). High-share words when honest: mistakes, habits, successful, and whatever your field's word for "practitioner" is.
- Numbers create intrigue; big specific numbers more so ("a 300k rollercoaster", "8 to 80 teams"). Use your own reporting currency and write the symbol out consistently across the post.
- Title + subtitle in title case; subtitle doubles as the meta-description seed.
- The clickbait test from `/founder-pipeline:brand-voice` applies: if it could headline a content-mill listicle, rewrite.

## Design for readability (house rule: great design, easily readable)

The post must look inviting at arm's length. Concretely:

- Short sentences. Short paragraphs: 1-3 sentences, never more than 4. Breathable; white space carries rhythm.
- **Skimmability test**: a reader scanning only H2s + bold lead-ins + the table gets ~70% of the value.
- H2s are opinionated sentences, not labels ("'One person can't own all that' was true. Was." not "Ownership Models").
- One **pull-quote** (blockquote) carrying the post's sharpest sentence — the line someone screenshots.
- **Bold lead-ins** on list items ("**Been in the seat.** I helped build…").
- One data table, always — a rate table, a scope table (segments × ranges × sources), a signals/checklist table, or a straight comparison (this vs alternatives vs doing nothing). AI search engines extract clean tables near-verbatim; the same numbers said in prose don't get lifted the same way. Every cell sourced or original data, never invented.
- Vary block shapes: no screen-height of uniform paragraphs. Paragraph → list → table → quote → paragraph.
- Images: **featured + at least 2 in the body** — the count is a hard rule in `SKILL.md` and is verified in the built output at step 09, not judged here. Centered, captioned with source, placed after a section's first paragraph, never immediately before an H2. Decoration still fails: if you cannot say why a picture sits in that particular section, the section is not the problem, the picture is.
- Highlight sparingly: bold for the load-bearing phrase, never whole sentences shouting.

## Endings

- No summary, no recap, no optimistic bow (per `/founder-pipeline:brand-voice`). End on the lesson's edge or a wedge question.
- One soft CTA sentence linking a money page — name the service as the natural next step rather than pitching it. The site template appends the CTA card; don't hard-sell in the body.

## Length

Whatever the value requires: HN-style essays 1,200-1,800 words; definitional guides can run longer. Cutting 30% in revision is normal and expected — density beats length.
