# Changelog

## 0.3.0 (2026-11-13)

The pipeline and its gates are the same. This release makes the plugin checkable: the roles it describes ship as components, the rules a machine can check are checked by one, and behaviour is covered by evals.

### Added

- **Four subagents** in `agents/`: `gate-critic`, `claim-refuter`, `completeness-critic` and `evidence-scout`. All four are read-only. The scout is pinned to the small model; the three critics inherit the session model, so they are as strong as the main loop.
- **Two workflows** in `workflows/`: `gather-verify` (a scout per item, a skeptic per claim, then a completeness critic) and `judge-panel` (one blind critic per framing; one FAIL fails the gate). Both are unit-tested against a mocked runner.
- **An approval hook.** Any edit that adds an `approved` row to a pipeline `PROGRESS.md` becomes a permission prompt. It asks, it does not block, and it lets the edit through on any error.
- **A grill pass for the ideation steps** (`references/grilling.md`), adapted from the `grilling` skill in mattpocock/skills (MIT): map the decisions and their dependencies, look facts up, ask only decisions, give a recommended answer with each, play the answers back before drafting. The cap of 6 questions per step stays.
- **A `Routing:` line in every stage file** with the execution mode and the model tier per role, so a step no longer needs the 28 KB routing map.
- **Behaviour evals** in `plugins/founder-pipeline/evals/` for `claude plugin eval`: 7 cases. Results for this release are in `docs/eval-results/`.
- **A linter**, `scripts/check_skills.py`, with 22 tests of its own: strict YAML, spec limits, context budgets, dangling references, the standalone install, agents, workflows, hooks, release metadata.
- **The release scan** (`scripts/verify-release.sh`) now lives in the repo. The private name list it scans for stays in a gitignored file.
- **CI** on every push and pull request: linter, unit tests, release scan, `claude plugin validate --strict`.
- `AGENTS.md` and `CLAUDE.md` for coding agents working on this repo, `docs/ARCHITECTURE.md`, `examples/mcp.json`, a plugin icon.

### Changed

- **Always-loaded context is 37% smaller.** The 23 skill descriptions went from 15,647 to 9,820 characters and now say when to use the skill. Three were over the 1,024-character spec limit; none is now.
- **`founder/SKILL.md` is 48% smaller**, 32,803 to 17,025 characters. The step-ID contract, the artifact-ownership list, the full anti-pattern list and the queue mechanics moved word for word into `references/`, each behind a pointer that says when to read it.
- `ai-seo`, `web-backlinks`, `seo-audit` and `marketing-psychology` bodies are under 17,500 characters, with the detail moved word for word into `references/`. The version notes in `web-site-creator/SKILL.md` moved to its changelog.
- **Unattended mode deploys to a preview URL by default.** Production needs `deploy: production` in the kickoff. The run has a time limit (`max hours`, default 8) and stops when a `STOP` file appears in the stream folder. This changes behaviour: 0.2.0 deployed live.
- **The P1.S1 health check asks before it writes.** 0.2.0 applied fixes and could create a `CLAUDE.md` in your project unasked.
- The model table names Fable 5.2 for the top tier and explains how tiers are enforced. The install guide counts 22 specialist skills (it said 21).
- Cost docs agree with each other: the top-tier model's credits on a Pro plan are stated as not included, DataForSEO is optional, email on your domain is a cost from phase 4.
- The version is declared once, in `plugin.json`.

### Fixed

- 7 skills had frontmatter that strict YAML parsers reject (an unquoted colon in the description).
- `user_invocable` in `health` and `scout` was a misspelling that Claude Code ignores silently. It is `user-invocable`.
- `argument-hint` parsed as a list in 9 skills, and one `metadata` value parsed as a date.
- The founder-only install was broken in 7 files that pointed at `${CLAUDE_PLUGIN_ROOT}`, which is empty outside a plugin install.
- A cold request to "just estimate" a search volume for a stream already in the pipeline did not load the founder skill, and the model answered with a number. 0.2.0 had the same gap. The eval caught it (0 of 3 runs passed on both versions); one sentence in the skill description fixed it (3 of 3).
- `web-site-creator/references/seo.md` pointed at a `/robots-txt` skill that does not ship.
- `blog-launch` hard-coded `model: 'sonnet'` for its research agents. It names a tier now.
- The cost doc said a $50 deposit buys 200 to 260 runs and also that a run a day for a year would not use it up.

## 0.2.0 (2026-11-04)

- The founder skill runs standalone. Every skill and tool it mentions is optional, resolved at run time, with one fallback card per item in `references/capabilities.md`.
- Step 1 opens with a capability preflight that writes `CAPABILITIES.md`.
- New `INSTALL.md`: three ways to install, one command per tool, and the model tiers mapped to current Claude models.
- Ported two months of fixes from the source pipeline: an asset audit for ideas that productize something you already run, a promise backtest in the offer step, a sanitization check before launch, and search-data calls rewritten for the REST API.

## 0.1.0 (2026-08-30)

First public release.
