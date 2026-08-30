# P1.S3 — ICP + territory → `P1-Ideation.S3-ICP.md`

**Phase: P1-Ideation**

**Earns its keep when** segmentation is non-obvious (CTO vs VP Eng vs Eng Director have different jobs), or geography matters (CEE willingness-to-pay ≠ US).

**Becomes performative when** there is one clear buyer ("Series A-C SaaS CTO in EU, 50–300 engineers"). Lock it fast.

**Ask one at a time:**
1. Primary ICP firmographic — stage, size, vertical, geography. Force specificity.
2. Buyer role — title, reporting line, budget authority, how they decide.
3. Who this is explicitly NOT for — name 2–3 adjacent segments you're walking away from.
4. TAM / SAM / SOM napkin numbers — cite each.
5. Why this segment first? (concentration of pain, ease of reach, willingness-to-pay)
6. Name 10 specific companies/accounts that match. If you can't, your ICP is too vague. Write them to `accounts.md` in the stream folder root — the CANONICAL named-accounts list (single-owner rule): the smoke test, P2.S3's price anchoring, and P3.S1's outreach all read this file, never a new list.

**Skills:** `/founder-pipeline:scout` for segmentation + sizing. Two further passes have no skill shipped with this plugin — run them inline unless your install has a dedicated one:

- **Deep segment mapping** (optional, when a segment is genuinely new to you): a research fan-out that reads industry directories and registries, community threads where the segment talks, and analyst or trade-press write-ups, and returns a per-segment brief with source URLs.
- **Account enrichment** (needed for the named-accounts gate): for each candidate account, find the company page, a named human with their title, and a profile URL that proves both existence and ICP fit.

Fan-out rule for either pass: each research subagent gets ONE distinct source class (industry directories/registries, communities, competitor customer pages/case studies) and must return source URLs per segment and per account; unsourced accounts are rejected at the gate.

**Write to** `P1-Ideation.S3-ICP.md`, plus the 10 named accounts to `accounts.md` in the stream folder root. TAM numbers cited or flagged. If the scout run and the segment-mapping fan-out produce substantive per-segment research, keep it in the step folder `P1-Ideation.S3-ICP/` (one file per segment, INDEX in the step md) instead of pasting walls of research into the step file.

**Def-of-success — ALL must pass before owner sign-off (fail → improvement loop per SKILL.md, never advance):**
- `/founder-pipeline:critical` run recorded; the score is advisory (target ≥ 8/10) — the gate is the PASS/FAIL criteria below, not the number.
- 10–20 real named accounts, each row = company + named human (title) + profile/source URL proving existence and ICP fit — a row without a human and a URL doesn't count. Written to `accounts.md` in the stream folder root.
- Every account tagged with a reach path (1st-degree / warm intro via named person / community / cold); ≥ 5 of the first 10 reachable warm — 0 warm paths fails the step here, not at P3.S1.
- TAM / SAM / SOM: SAM and SOM each carry ≥1 real cited source (registry/directory count, a search-volume figure from your keyword-data provider, scout output file path); `[assumption]` tag permitted for TAM only; the SOM ≥ 10× sanity ratio may be computed ONLY on a cited SOM — an assumption-tagged SOM fails the ratio automatically.
- ≥ 2 named exclusion segments with the reason for walking away.
- Sanity ratio: SOM ≥ 10× the 12-month revenue target — otherwise the segment can't carry the stream.

**Gate out (mandatory — see SKILL.md house rules):**
1. Draft `P1-Ideation.S3-ICP.md`.
2. Invoke `/founder-pipeline:critical` on the draft — attack the TAM/SAM/SOM math and the "why this segment first" logic hardest; hunt for "everyone is the ICP" drift.
3. Revise; note what changed.
4. Present the draft + the critical findings + the changes to the owner. **Wait for their explicit approval. Never auto-advance.**

**Checkpoint:** "Primary ICP: [X]. Exclusions: [Y, Z]. Lock this, or split into two ICPs we carry forward for one more stage?"

**Next:** `stages/P1-Ideation.S4-Prediction.md`
