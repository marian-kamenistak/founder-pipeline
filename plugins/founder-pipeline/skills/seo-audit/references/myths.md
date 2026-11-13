# Myths this skill does not chase

This file belongs to the `seo-audit` skill.

Stated once so no audit re-litigates them, and so a client asking "shouldn't we add more words"
gets the same answer twice.

| Myth | What this skill does |
|---|---|
| Longer content ranks better | No word-count target, ever. Word count is reported as context and survives only as the 150-word thin-content Gate floor |
| Outbound links leak authority | Outbound links to named sources are a **positive**. The old `link_ratio` penalty was deleted from the checker on 2026-08-22 |
| Schema drives rankings or AI citations | Schema is reported, never scored. It ships for Google rich results and entity resolution. See `${CLAUDE_PLUGIN_ROOT}/skills/web-site-creator/references/metadata.md` §8.4 for the standing decision on which types ship |
| Google penalises AI-written content | Google penalises thin and unhelpful content. Authorship method is not the axis. Run `/founder-pipeline:humanize` because AI-smooth copy reads badly, not because of a penalty |
| The model that wrote it is a ranking factor | It is not |
| URL slug word order matters | It does not. Consistency across the site does |
| Keyword density is a target | Answer clarity is. Density is a symptom, not a lever |
