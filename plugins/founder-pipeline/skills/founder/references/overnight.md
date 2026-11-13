## Unattended mode (autonomous run, review packet)

For "kick it off, review the result later." Invoked explicitly with the `overnight` flag: `/founder-pipeline:founder <stream> overnight`. It changes **WHO approves, never WHAT passes**. Nothing below softens a gate; it substitutes a fresh-context judge for a human signature and defers the signature to the review session.

**Operator mandate (read this first — it governs everything below):**
- **Never ask the owner anything. Nobody is watching.** There is no one to answer a question, so a question is a dead end. Every question you would have asked, you answer yourself with research and reasoning, then log three things — in the step's build log and in `MORNING-REVIEW.md`: the question, your answer, and the evidence or reasoning behind it, tagged `[assumption — owner review]`. The owner reviews the answers later; they never get asked the question.
- **A failed tool is not a blocked step.** An honest `BLOCKED: needs [exactly what]` for missing real-world evidence is a valid outcome and never breaks this mandate; a tool error is not. If a tool errors, an API is down, a connector is missing, a page will not load, a search returns nothing — find another route. Fall back to REST, to a different source, to a different method, to a manual reconstruction. Retry after failures; gather the missing information yourself. "I couldn't because X failed" is not an acceptable outcome unless you have exhausted every alternative route and logged each one you tried.
- **If a phase stalls, ship the strong 80% and keep moving.** Don't burn the whole run on one step chasing the last 20%. Produce the best version the available evidence supports, note explicitly in the step file and in `MORNING-REVIEW.md` what got cut and why, mark any evidence-dependent gap `BLOCKED: needs [exactly what]`, and advance to the next step that does not depend on the cut part. A shipped 80% that names its gaps beats a perfect step that never finished.
- **Stop only at the definition of done, a run limit, or the stop file.** The run limits are in the next section. The run ends when every step has reached its def-of-success (or an honestly-logged `BLOCKED` naming the exact missing evidence), the web is built and deployed (or P4.S3 is skipped with a recorded reason), and `MORNING-REVIEW.md` is written — not when the context is long, not when a step got hard, not when you would normally check in. Push through to done.

These four override any instinct to pause, hedge, or defer. They never override the run limits or the hard limits below. The hard limits below still stand — never fabricate evidence, never send outreach, and the two P1.S1 preconditions (a non-empty intake folder and a supplied profit bar) legitimately halt the run before it starts. "Blocked is not an option" and "do not stop until done" apply once the run is past P1.S1.

**What replaces the owner's per-step approval:**
1. Def-of-success verdicts come from a **fresh-context `/critical` subagent** per step, spawned with only the draft and the criteria — never the chat history, so it cannot inherit this session's sympathy. Its GATE line decides.
2. The improvement loop runs up to **3 rounds per step** with full skill and subagent fan-out. If the gate still fails, the step is marked `BLOCKED` in the file, the reason is logged, and the run CONTINUES to whatever downstream steps do not depend on it — it never fakes a pass to keep moving.
3. Every auto-advanced step is left at `awaiting approval` in `PROGRESS.md`, with its CRITICAL score, def-of-success result and one-line Note filled in. **Only the owner's review approval flips a row to `approved`.** `PROGRESS.md` itself is what shows which conclusions are still provisional.

**What unattended mode may NEVER do (hard limits):**
- **Fabricate evidence.** Interview quotes, discovery calls, LOIs, pilots and price-anchoring reactions are human facts. Evidence-dependent criteria pass ONLY from pre-existing recorded evidence — the stream's intake-folder assets, prior stream files, version-control history, meeting notes the owner pointed at. Otherwise the criterion is `BLOCKED: needs real-world evidence — [exactly what]`. An unattended run without a non-empty intake folder stops at P1.S1: raw idea assets are its fuel.
- **Send anything.** No outreach messages, no emails, no posts. P3.S1 prepares the accounts table and the messages ready-to-send; sending is the owner's click. Staging a draft in the mail client is permitted — a draft is not a send.
- **Skip the profit bar.** The hurdle rate and the absolute floor must be supplied in the kickoff prompt or already present in the stream's `brief.md`. Without them the run stops at P1.S1 and says so.
- **Deploy to production without being told to.** P4.S3's web build is a must-have unattended step: the run builds the site and deploys it to a **preview or staging URL** on the declared host. It goes to the production domain only when the kickoff carries `deploy: production`. Either way the review packet lists the URL, a diff summary and a one-line rollback path.

**Run limits (checked before every step starts, never mid-step):**
- **Time.** The kickoff's `max hours` (default 8). When the limit is reached the run finishes the current step, writes `MORNING-REVIEW.md` and stops.
- **Rounds.** 3 improvement rounds per step, then `BLOCKED` and move on (rule 2 above). One autonomous rewind per target step.
- **Stop file.** If `<stream>/STOP` exists, the run writes `MORNING-REVIEW.md` and ends. Creating that file is how the owner halts a run from another terminal or a phone.
- **Spend.** Token and money caps belong to the harness, not to a prompt: set them where you launch the run (your plan's limits, `claude -p --max-budget-usd <amount>` for a headless run, or your scheduler's timeout). The run records what it was launched with in `MORNING-REVIEW.md`.

**Sub-skill autonomy rule:** routed skills (`/pricing`, `/brainstorm`, `/scout`, …) are conversational by design — unattended, NEVER let one wait for a human. Answer its questions yourself from the intake folder, prior stream files and version-control history, and tag every self-answered question `[assumption — owner review]` in the step file. If a sub-skill's question genuinely cannot be answered from the available material, record the best-guess answer AND the open question in `MORNING-REVIEW.md`, and continue.

**Review packet (the run's last act):** write `MORNING-REVIEW.md` in the stream folder — a table of steps with GATE verdict, rounds used, what changed, `BLOCKED` items with the exact evidence each needs, and any overrides proposed; links to the preview URL and the key drafts; and the 3 decisions the owner must make, ranked. The review conversation starts from this file, and each approval flips that step's `PROGRESS.md` row to `approved`, step by step.

**Kickoff template (paste with the launch — the run stops at P1.S1 without these):**
```
/founder-pipeline:founder <stream> overnight
parent: <path to the folder streams live in>     slug: <kebab-case>
horizon: <90d/6m/12m>       type: <SKU of an existing brand / new brand / productized consulting>
portfolio trade: <stream> gives up <N> h/week; people: <who carries what>
hurdle rate: <CUR X per founder-hour>            absolute floor: <CUR Y 12-month profit>
intake folder: <path>       brand kit: <kit> — only needed to OVERRIDE your configured default
max hours: <N, default 8>   deploy: <preview (default) / production>
prior evidence: <files or version-control history to inherit>
```

**Launch mechanics:**
- Start in a normal session with the kickoff template above.
- **Pre-grant the permissions the run needs** through your agent's allowlist or project settings before starting: a single interactive permission prompt stalls the entire run until someone answers it. Grant the specific tools the pipeline uses; do not disable the permission system wholesale.
- **Keep the machine awake** for the duration — an unattended run dies with the session when the host sleeps.
- **The run is resumable.** If it dies mid-pipeline, re-invoking resumes from the `PROGRESS.md` row marked `in progress` or `awaiting approval`.
