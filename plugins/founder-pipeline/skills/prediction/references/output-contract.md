# Output contract (step 7)

All outputs live under `<output root>/predictions/`: living ledger `PREDICTIONS.md` (never deleted rows), dated snapshot `<YYYY-MM-DD>/` (same-day re-run: `<YYYY-MM-DD>-2/`) with `workspace.md` (config + framed questions + pre-registered rules, created at step 1), `research-notes/`, `raw/` (cached API JSON), `prediction-report.md`, `execution-plan.md`, and in hypothesis mode `niche-verdict.md`.

## Ledger row (PREDICTIONS.md)

```
| id | question (background · resolution criterion · close date) | probability | base rate [source, frozen] | confidence | indicator command (curl URL, or your keyword-data provider's call written out — e.g. `dfs-mcp: <tool> {params}`) | threshold | check date | market x-check | wild-card (fails because → watch indicator) | status | brier |
```

- The **indicator command cell is executable verbatim** — step 0 runs it, no interpretation. `raw/` caches responses; the command itself lives in the row.
- **Watch rows**: probability, base rate, and brier cells hold `—`; threshold = graduation criterion; status = `watch`. They graduate to scored rows (new id, cross-referenced) when a later run finds the missing evidence.
- Header block above the table: rolling mean Brier · base-rate forecaster Brier on the same rows (each row's frozen base-rate value IS that forecaster's prediction) · delta · calibration buckets (from cycle 3). First run writes this header with "cycle 1 — no calibration data yet". Status vocab: `pending → hit / miss / partial` (+ `revised@date` — both entries graded).

## prediction-report.md

1. **Verdict paragraph first** — the 3-sentence "so what" the owner reads if they read nothing else.
2. Bets table (surviving + Watch), each with the 3-pass ensemble spread where it exceeded 2 points.
3. Contrarian section — the ≥2 against-sources per bet and how the verdict answers them.
4. INSUFFICIENT DATA register — every gap + its named manual-verification item (these route to the caller's manual queue if one exists).
5. Money block — per-bet range + dominant-uncertainty factor + floor comparison.
6. Calibration note — Brier trend, and from cycle 3 the honest line: "beating base rates: yes/no".

## execution-plan.md

**Live variant** (existing stream): 4 sections — keywords & renames (extend-existing beats new; cannibalization check) · pages & posts (≥3 inbound internal links each) · event/podcast/conference topics · packaged artifacts the stream could ship (MCP server, agent skill, CLI) plus `llms.txt`. For that last section, list per candidate: what it does, the registries or directories it would be listed in, and who maintains it after launch — an artifact with no named maintainer is not a plan. `/founder-pipeline:ai-seo-llms-builder` owns the `llms.txt` itself. Sequenced 90-day view + one stop-doing line. Every item cites its bet id.

**Greenfield variant** (hypothesis mode): everything is a NEW asset — no rename/cannibalization sections. Sections: keyword contract seed (3-7 primaries with volumes, feeds founder P4.S1 Keywords) · first-pages list (feeds P4.S2 Copy and P4.S3 Web) · first-posts list (feeds P5.S1 Launch) · event/community angles · packaged-artifact candidates (only if a real question-the-ICP-asks exists — no toy servers). Every item cites its bet id.

## niche-verdict.md (hypothesis mode only — the ideation steering doc)

- **Pick**: surviving bets ranked by ensemble probability, ties broken by conservative-end money range vs the pre-registered floor (no score×money arithmetic — the two aren't multipliable). The Pick must clear the money floor at the conservative end; if it doesn't, label it honestly: "content angle, not a stream".
- **Drop**: two distinct lists — **DEAD** (axis 0 / kill rule fired, with the killing evidence; this text stops the founder run from relitigating them at P1.S5) and **NEAR-MISS** (Watch rows with graduation criteria + re-check date — these are worth a second look, dead angles aren't).
- **Reframe**: queries/phrasings where demand exists under a different name than the owner's framing (the most common hypothesis-mode finding — e.g. head term with volume vs invented niche phrase with zero).
- **Carry-forward table**: keyword/query/content-angle shortlist with volumes `[source]` → consumed by founder P1.S5 (competition scoping), P1.S7 (name), P4.S1 (keyword contract).

Reader-facing titles/copy suggestions pass `/founder-pipeline:brand-voice` conventions. The owner reviews before any downstream step consumes the plan (hard gate — in founder runs this is the P1.S4 sign-off).
