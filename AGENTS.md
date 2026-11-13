# AGENTS.md

Instructions for any coding agent (Claude Code, Codex, Cursor) working in this repository. `CLAUDE.md` imports this file.

## What this repo is

A Claude Code plugin marketplace with one plugin, `plugins/founder-pipeline/`: 23 skills, 4 subagents, 2 workflows, 1 hook and an eval suite. Almost everything is Markdown that a model reads at run time, so a wording change is a behaviour change. Treat it like code: test before and after.

```
.claude-plugin/marketplace.json     the marketplace entry
plugins/founder-pipeline/
  .claude-plugin/plugin.json        the one place the version lives
  skills/<name>/SKILL.md            23 skills; founder/ is the orchestrator
  agents/*.md                       gate-critic, claim-refuter, completeness-critic, evidence-scout
  workflows/*.js                    gather-verify, judge-panel
  hooks/                            approval-guard: asks before a step is marked approved
  evals/<case>/                     behaviour evals for `claude plugin eval`
scripts/                            check_skills.py (linter), verify-release.sh (release scan)
tests/                              unit tests for the linter, the hook and the workflows
docs/ARCHITECTURE.md                how the pieces fit and why
```

## Before you change anything

1. Read `docs/ARCHITECTURE.md`. It explains the decisions the rules below protect.
2. Say what you will change and how you will prove it worked. "Should work" is not proof.

## Checks: run all of them before you call a change done

```bash
python3 scripts/check_skills.py                      # spec limits, budgets, dangling references
python3 -m unittest discover -s tests -p 'test_*.py' # the linter's own tests
node --test "tests/*.test.mjs"                       # hook + workflow logic, mocked runner
bash scripts/verify-release.sh                       # personal data, credentials, machine paths
claude plugin validate . --strict && claude plugin validate plugins/founder-pipeline --strict
```

CI runs the same five on every push. A change to a skill's wording, a description, an agent prompt or a gate also needs the behaviour evals, which call a model and so are not in CI:

```bash
claude plugin eval plugins/founder-pipeline --max-cost-usd 15 --no-publish
```

If an eval fails, fix the plugin. Change a grader only when the grader is wrong, and say why in the commit.

## Rules

- **Test first for behaviour.** A new rule in a skill starts as a failing eval case under `evals/`. Run it, watch it fail, then write the rule. A new check in the linter starts as a failing test in `tests/`.
- **Budgets are enforced, not advised.** Each description is at most 1,024 characters and all 23 together at most 10,500. Each `SKILL.md` body is at most 20,000 characters and 500 lines. Over budget means move detail into `references/` with a pointer that says when to read it. Do not raise a budget to make a change fit.
- **Frontmatter is strict YAML.** Quote any value that contains `: `, `[` or a date. `check_skills.py` parses with a strict loader and rejects unknown keys, so a typo such as `user_invocable` fails the build.
- **The founder skill must work when its folder is copied alone.** No `${CLAUDE_PLUGIN_ROOT}` inside `skills/founder/`. Paths there are relative to the skill folder. Anything the full plugin adds (agents, workflows, the hook) needs a fallback row in `skills/founder/references/capabilities.md`.
- **Tiers, not model names.** Skill text names PEAK, HIGH, MID and CHEAP. Agent files use an alias (`inherit`, `haiku`), never a dated model ID. Workflow scripts set no model; the agent definitions own that. The one dated mapping is the table in `skills/founder/INSTALL.md`.
- **Critics and scouts are read-only.** No `Write`, `Edit` or `Bash` in `agents/*.md`.
- **Gates do not soften.** Do not weaken a def-of-success criterion, the owner sign-off, the profit floor or an honesty rule to make a run smoother. If a gate is wrong, change it in its own commit with the evidence.
- **Nothing private ships.** No real client, prospect or person other than the author, no private paths, no credentials. `verify-release.sh` checks shapes; you check meaning. When unsure, leave it out.
- **Touch only what the change needs.** No drive-by rewrites of neighbouring skills.

## Releasing

1. Bump `version` in `plugins/founder-pipeline/.claude-plugin/plugin.json`. It is the only place the version is declared.
2. Add a `## <version>` section to `CHANGELOG.md`. The linter fails without it.
3. Run every check above, then the evals. Put the eval summary in `docs/eval-results/`.
4. Merge to `main`, then `claude plugin tag plugins/founder-pipeline --push` and create the GitHub release from the changelog section.
