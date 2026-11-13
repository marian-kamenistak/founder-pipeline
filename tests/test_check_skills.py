"""The linter is only worth trusting if it fails on the defects it claims to catch.

Each test builds a small broken plugin in a temp dir and asserts the exact error.
Run: python3 -m unittest discover -s tests -p 'test_*.py'
"""
import json
import pathlib
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "scripts"))
import check_skills as cs  # noqa: E402

GOOD_SKILL = '---\nname: demo\ndescription: "Use when testing the linter."\n---\n\n# Demo\n\nBody.\n'
GOOD_AGENT = ('---\nname: scout\ndescription: Narrow research worker. Use one per item with a single question.\n'
              'model: haiku\neffort: low\ntools: Read, Grep\n---\n\n' + 'Gather evidence for one item. ' * 10)


class Fixture(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self._tmp.name)
        self.plugin = self.root / "plugins" / cs.PLUGIN
        (self.plugin / ".claude-plugin").mkdir(parents=True)
        (self.root / ".claude-plugin").mkdir()
        (self.plugin / ".claude-plugin" / "plugin.json").write_text(json.dumps({"name": cs.PLUGIN, "version": "9.9.9"}))
        (self.root / ".claude-plugin" / "marketplace.json").write_text(
            json.dumps({"name": cs.PLUGIN, "description": "d", "plugins": [{"name": cs.PLUGIN}]}))
        (self.root / "CHANGELOG.md").write_text("# Changelog\n\n## 9.9.9\n- x\n")
        self.skill("founder", GOOD_SKILL.replace("demo", "founder"))

    def tearDown(self):
        self._tmp.cleanup()

    def skill(self, name, text):
        d = self.plugin / "skills" / name
        d.mkdir(parents=True, exist_ok=True)
        (d / "SKILL.md").write_text(text)
        return d

    def errors(self):
        out = []
        for d in sorted((self.plugin / "skills").iterdir()):
            e, _ = cs.check_skill(d)
            out += e + cs.check_local_refs(d)
        return out + cs.check_cross_refs(self.plugin) + cs.check_standalone(self.plugin) \
            + cs.check_components(self.plugin) + cs.check_release(self.root, self.plugin)

    def assertError(self, fragment):
        errs = self.errors()
        self.assertTrue(any(fragment in e for e in errs), f"expected an error containing {fragment!r}, got {errs}")


class Frontmatter(Fixture):
    def test_clean_fixture_has_no_errors(self):
        self.skill("demo", GOOD_SKILL)
        self.assertEqual(self.errors(), [])
        self.assertEqual(cs.run(self.root), 0)

    def test_unquoted_colon_in_description_is_invalid_yaml(self):
        self.skill("demo", "---\nname: demo\ndescription: Use when: things happen\n---\nbody\n")
        self.assertError("not valid YAML")

    def test_description_over_spec_limit(self):
        self.skill("demo", f'---\nname: demo\ndescription: "{"x" * 1025}"\n---\nbody\n')
        self.assertError("description is 1025 chars")

    def test_misspelled_key_is_reported_instead_of_silently_ignored(self):
        self.skill("demo", GOOD_SKILL.replace("---\n\n#", "user_invocable: true\n---\n\n#"))
        self.assertError("unknown frontmatter key `user_invocable`")

    def test_unquoted_argument_hint_parses_as_a_list(self):
        self.skill("demo", GOOD_SKILL.replace("---\n\n#", "argument-hint: [topic]\n---\n\n#"))
        self.assertError("argument-hint must be a quoted string")

    def test_metadata_values_must_be_strings(self):
        self.skill("demo", GOOD_SKILL.replace("---\n\n#", "metadata:\n  updated: 2026-08-22\n---\n\n#"))
        self.assertError("metadata.updated must be a string")

    def test_name_must_match_folder(self):
        self.skill("demo", GOOD_SKILL.replace("name: demo", "name: other"))
        self.assertError("does not match folder")


class Budgets(Fixture):
    def test_body_over_token_budget(self):
        self.skill("demo", GOOD_SKILL + "x" * (cs.MAX_BODY_CHARS + 1))
        self.assertError("move detail into references/")

    def test_body_over_line_limit(self):
        self.skill("demo", GOOD_SKILL + "line\n" * (cs.MAX_BODY_LINES + 1))
        self.assertError("lines, limit 500")

    def test_listing_budget_is_enforced_across_skills(self):
        for i in range(11):
            self.skill(f"s{i}", f'---\nname: s{i}\ndescription: "{"y" * 1000}"\n---\nbody\n')
        self.assertEqual(cs.run(self.root), 1)


class References(Fixture):
    def test_dangling_file_reference(self):
        self.skill("demo", GOOD_SKILL + "Read `references/missing.md` when stuck.\n")
        self.assertError("points at `references/missing.md`")

    def test_existing_reference_and_placeholders_pass(self):
        d = self.skill("demo", GOOD_SKILL + "Read `references/ok.md`. Sites live in `references/sites/<slug>.md`.\n")
        (d / "references").mkdir()
        (d / "references" / "ok.md").write_text("ok")
        self.assertEqual(self.errors(), [])

    def test_reference_to_a_skill_that_does_not_ship(self):
        self.skill("demo", GOOD_SKILL + f"Then run `/{cs.PLUGIN}:ghost`.\n")
        self.assertError(f"`{cs.PLUGIN}:ghost` is not a skill, agent or workflow")

    def test_reference_to_an_agent_that_does_not_ship(self):
        self.skill("demo", GOOD_SKILL + f"Dispatch `{cs.PLUGIN}:phantom-critic`.\n")
        self.assertError(f"`{cs.PLUGIN}:phantom-critic`")

    def test_plugin_root_path_breaks_the_standalone_install(self):
        self.skill("founder", GOOD_SKILL.replace("demo", "founder") + "See `${CLAUDE_PLUGIN_ROOT}/skills/founder/x.md`.\n")
        self.assertError("empty in a founder-only install")


class Components(Fixture):
    def agent(self, text, name="scout"):
        (self.plugin / "agents").mkdir(exist_ok=True)
        (self.plugin / "agents" / f"{name}.md").write_text(text)

    def test_good_agent_passes(self):
        self.agent(GOOD_AGENT)
        self.assertEqual(self.errors(), [])

    def test_dated_model_id_is_rejected_in_favour_of_an_alias(self):
        self.agent(GOOD_AGENT.replace("model: haiku", "model: claude-haiku-4-5"))
        self.assertError("an alias survives model releases")

    def test_critic_agents_must_stay_read_only(self):
        self.agent(GOOD_AGENT.replace("tools: Read, Grep", "tools: Read, Edit"))
        self.assertError("read-only")

    def test_workflow_must_not_pin_a_model_or_use_the_clock(self):
        (self.plugin / "workflows").mkdir()
        (self.plugin / "workflows" / "w.js").write_text(
            "export const meta = {\n  name: 'w',\n  description: 'd',\n}\n\nawait agent('x', { model: 'sonnet' })\nlog(Date.now())\n")
        self.assertError("tiers live in agents/")
        self.assertError("breaks workflow resume")

    def test_hook_command_must_point_at_a_file_that_ships(self):
        (self.plugin / "hooks").mkdir()
        (self.plugin / "hooks" / "hooks.json").write_text(json.dumps({"hooks": {"PreToolUse": [
            {"matcher": "Edit", "hooks": [{"type": "command", "command": 'node "${CLAUDE_PLUGIN_ROOT}/hooks/gone.mjs"'}]}]}}))
        self.assertError("points at `hooks/gone.mjs`")


class Release(Fixture):
    def test_version_without_changelog_entry(self):
        (self.root / "CHANGELOG.md").write_text("# Changelog\n\n## 0.0.1\n")
        self.assertError("no `## 9.9.9` section")

    def test_version_declared_twice(self):
        (self.root / ".claude-plugin" / "marketplace.json").write_text(
            json.dumps({"name": cs.PLUGIN, "description": "d", "plugins": [{"name": cs.PLUGIN, "version": "9.9.9"}]}))
        self.assertError("plugin.json is the one source")


if __name__ == "__main__":
    unittest.main()
