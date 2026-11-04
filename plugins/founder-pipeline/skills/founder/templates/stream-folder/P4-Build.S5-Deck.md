# Deck — sales deck PDF build log

**Stream:** [slug]
**Step:** P4.S5-Deck (P4-Build)
**Last updated:** [date]

> HTML→PDF via system Chrome is the default deck path (owner: this step), because the deck is then the same HTML the site already serves: one source of words, real clickable links in the PDF, and no re-typing of prices into a design tool. A different path (a design tool, a slide app) needs a recorded override with the reason — the reason has to answer how copy stays in sync with the live site.
>
> Copy, prices, links, and photos are SOURCED from the live site (P4.S3) — never re-written here.
>
> Generator shape: a small folder next to the web build holding one HTML file per slide (or one long HTML with page breaks), a print stylesheet at the deck's page size, a data file the slides read prices and links from — the same data file the site reads — and a one-command script that renders it to PDF with headless Chrome. The plugin ships a minimal reference version; point `Generator location` at yours.

---

## Build log

| Item | Value |
|---|---|
| Generator location | [path] |
| Live deck URL | [<site>/deck] |
| PDF location | [the site's static-asset dir, e.g. `public/deck.pdf`] |
| Slide count | [N] |
| Link count (all verified clickable) | [N] |
| Rebuild command | [`...`] |

## Footer-link diff (site vs deck)

| Link on site footer | In deck? | Note |
|---|---|---|
| | | |

## Offering-URL diff (site data file vs sorted PDF URI list — any missing URL = FAIL)

| Offering URL (from site data file) | In PDF URI list? | Note |
|---|---|---|
| | | |

## Open placeholders

| Placeholder | Where | Blocking? | Queue row |
|---|---|---|---|
| | | | |

---

## Honest-assessment note

- [ ] Earns its keep — stream has a client-send motion
- [ ] Performative — no deck motion: skip recorded in brief.md + PROGRESS.md

## Checkpoint

- [ ] Deck live at [URL], PDF downloadable, ICP click test passed (P1.S3 persona)
- [ ] Launch (P5.S1) next

## Validation loop

- [ ] `/critical` run — findings: [...] — **CRITICAL SCORE: [X]/10** — advisory; the gate is the def-of-success PASS/FAIL checklist
- [ ] Def-of-success (from the stage file): [each criterion — met/unmet]
- [ ] Improvement loops run (if gate failed): [N — what changed each round]
- [ ] Revised — what changed: [...]
- [ ] **Owner approved** — [date] [overrides, if any]
