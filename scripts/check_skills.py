#!/usr/bin/env python3
"""check_skills.py — lint the plugin against the Agent Skills spec and this repo's own budgets.

`claude plugin validate` checks the manifests. It does not check what costs context or what
breaks an install, so this does:

  frontmatter   strict YAML, known keys only, name == folder, string types
  description   <= 1024 chars each (agentskills.io spec), and a total budget for the listing
  body          <= 500 lines and <= 20,000 chars (about 5,000 tokens at 4 chars per token)
  references    every file a skill points at exists; every /founder-pipeline:<name> and
                founder-pipeline:<agent> resolves to something that ships
  standalone    the founder skill folder works when copied alone (no plugin-root paths)
  components    agents, workflows and hooks are well formed
  release       plugin.json version has a CHANGELOG entry; the marketplace entry does not
                repeat the version

Usage:  python3 scripts/check_skills.py [--report] [repo-root]
Exit 0 = clean, 1 = at least one error.
"""
from __future__ import annotations

import json
import pathlib
import re
import sys

import yaml

PLUGIN = "founder-pipeline"
MAX_DESC = 1024            # agentskills.io/specification
MAX_TOTAL_DESC = 10_500    # this repo's budget for the always-loaded skill listing
MAX_BODY_LINES = 500       # code.claude.com/docs/en/skills
MAX_BODY_CHARS = 20_000    # ~5,000 tokens, the spec's recommended ceiling
CHARS_PER_TOKEN = 4        # estimate, used only for the report

SKILL_KEYS = {
    "name", "description", "when_to_use", "argument-hint", "arguments", "allowed-tools",
    "disallowed-tools", "model", "effort", "context", "agent", "background", "hooks", "paths",
    "shell", "metadata", "license", "compatibility", "disable-model-invocation", "user-invocable",
}
AGENT_MODELS = {"inherit", "haiku", "sonnet", "opus", "fable"}  # aliases only, never a dated id
EFFORTS = {"low", "medium", "high", "xhigh", "max"}
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n(.*)\Z", re.S)
# `references/x.md`, `stages/x.md` ... in backticks, relative to the skill folder
LOCAL_REF_RE = re.compile(r"`((?:references|stages|steps|phases|templates|scripts|config|tests)/[A-Za-z0-9._/-]+\.[a-z0-9]+)`")
# Paths the skills tell the user to keep in THEIR site repo. They are not plugin files.
SITE_REPO_FILES = {"scripts/gen-lastmod.mjs", "scripts/gen-agent-markdown.mjs"}
SLASH_REF_RE = re.compile(rf"/{PLUGIN}:([a-z0-9-]+)")
AGENT_REF_RE = re.compile(rf"(?<![/\w]){PLUGIN}:([a-z0-9-]+)")


def split_frontmatter(text: str):
    m = FRONTMATTER_RE.match(text)
    if not m:
        raise ValueError("no frontmatter block")
    return yaml.safe_load(m.group(1)), m.group(2)


def check_skill(skill_dir: pathlib.Path) -> tuple[list[str], dict]:
    """Return (errors, stats) for one skill folder."""
    errors: list[str] = []
    stats = {"name": skill_dir.name, "desc": 0, "body_chars": 0, "body_lines": 0}
    path = skill_dir / "SKILL.md"
    try:
        fm, body = split_frontmatter(path.read_text())
    except (ValueError, yaml.YAMLError) as e:
        return [f"{path}: frontmatter is not valid YAML ({str(e).splitlines()[0]})"], stats
    if not isinstance(fm, dict):
        return [f"{path}: frontmatter is not a mapping"], stats

    for key in sorted(set(fm) - SKILL_KEYS):
        errors.append(f"{path}: unknown frontmatter key `{key}`")
    name = fm.get("name")
    if name != skill_dir.name:
        errors.append(f"{path}: name `{name}` does not match folder `{skill_dir.name}`")
    if not isinstance(name, str) or not NAME_RE.match(name) or len(name) > 64:
        errors.append(f"{path}: name must be lowercase kebab-case, at most 64 chars")
    desc = fm.get("description")
    if not isinstance(desc, str) or not desc.strip():
        errors.append(f"{path}: description must be a non-empty string")
        desc = ""
    if len(desc) > MAX_DESC:
        errors.append(f"{path}: description is {len(desc)} chars, limit {MAX_DESC}")
    if "argument-hint" in fm and not isinstance(fm["argument-hint"], str):
        errors.append(f"{path}: argument-hint must be a quoted string (an unquoted [..] parses as a list)")
    for k, v in (fm.get("metadata") or {}).items():
        if not isinstance(v, str):
            errors.append(f"{path}: metadata.{k} must be a string, got {type(v).__name__}")

    lines = body.count("\n")
    if lines > MAX_BODY_LINES:
        errors.append(f"{path}: body is {lines} lines, limit {MAX_BODY_LINES}")
    if len(body) > MAX_BODY_CHARS:
        errors.append(f"{path}: body is {len(body)} chars, limit {MAX_BODY_CHARS} — move detail into references/")

    stats.update(desc=len(desc), body_chars=len(body), body_lines=lines)
    return errors, stats


def check_local_refs(skill_dir: pathlib.Path) -> list[str]:
    errors = []
    for md in sorted(skill_dir.rglob("*.md")):
        for ref in sorted(set(LOCAL_REF_RE.findall(md.read_text()))):
            if any(c in ref for c in "<>*{}") or ref in SITE_REPO_FILES:
                continue
            # A reference resolves from the skill root, from the file's own folder, or, when the
            # sentence names another bundled skill, from that sibling skill's root.
            homes = [skill_dir, md.parent] + [d for d in skill_dir.parent.iterdir() if d.is_dir()]
            if not any((h / ref).exists() for h in homes):
                errors.append(f"{md}: points at `{ref}`, which does not exist")
    return errors


def check_cross_refs(plugin_dir: pathlib.Path) -> list[str]:
    skills = {p.name for p in (plugin_dir / "skills").iterdir() if (p / "SKILL.md").exists()}
    agents = {p.stem for p in (plugin_dir / "agents").glob("*.md")} if (plugin_dir / "agents").exists() else set()
    workflows = {p.stem for p in (plugin_dir / "workflows").glob("*.js")} if (plugin_dir / "workflows").exists() else set()
    known = skills | agents | workflows
    errors = []
    for f in sorted(list(plugin_dir.rglob("*.md")) + list(plugin_dir.rglob("*.js"))):
        if "evals" in f.relative_to(plugin_dir).parts[:1]:
            continue
        text = f.read_text()
        for ref in sorted(set(SLASH_REF_RE.findall(text)) | set(AGENT_REF_RE.findall(text))):
            if ref not in known:
                errors.append(f"{f}: `{PLUGIN}:{ref}` is not a skill, agent or workflow in this plugin")
    return errors


def check_standalone(plugin_dir: pathlib.Path) -> list[str]:
    """The founder skill is documented as installable by copying its folder alone."""
    errors = []
    for f in sorted((plugin_dir / "skills" / "founder").rglob("*.md")):
        if "CLAUDE_PLUGIN_ROOT" in f.read_text():
            errors.append(f"{f}: uses ${{CLAUDE_PLUGIN_ROOT}}, which is empty in a founder-only install")
    return errors


def check_components(plugin_dir: pathlib.Path) -> list[str]:
    errors = []
    for a in sorted((plugin_dir / "agents").glob("*.md")) if (plugin_dir / "agents").exists() else []:
        try:
            fm, body = split_frontmatter(a.read_text())
        except (ValueError, yaml.YAMLError) as e:
            errors.append(f"{a}: frontmatter is not valid YAML ({str(e).splitlines()[0]})")
            continue
        if fm.get("name") != a.stem:
            errors.append(f"{a}: name `{fm.get('name')}` does not match file `{a.stem}`")
        if not isinstance(fm.get("description"), str) or len(fm["description"]) < 40:
            errors.append(f"{a}: description must say when to use the agent")
        if fm.get("model") not in AGENT_MODELS:
            errors.append(f"{a}: model must be one of {sorted(AGENT_MODELS)} (an alias survives model releases)")
        if fm.get("effort") not in EFFORTS:
            errors.append(f"{a}: effort must be one of {sorted(EFFORTS)}")
        if not fm.get("tools"):
            errors.append(f"{a}: declare `tools` so the agent gets least privilege")
        elif re.search(r"\b(Write|Edit|Bash)\b", str(fm["tools"])):
            errors.append(f"{a}: research and critic agents are read-only; remove Write/Edit/Bash")
        if len(body.strip()) < 200:
            errors.append(f"{a}: system prompt is too short to be a contract")
    for w in sorted((plugin_dir / "workflows").glob("*.js")) if (plugin_dir / "workflows").exists() else []:
        text = w.read_text()
        if not text.startswith("export const meta = {"):
            errors.append(f"{w}: must begin with `export const meta = {{`")
        if f"name: '{w.stem}'" not in text:
            errors.append(f"{w}: meta.name must equal the file name `{w.stem}`")
        if re.search(r"\bmodel\s*:", text.split("\n}\n", 1)[-1]):
            errors.append(f"{w}: do not set a model in the script; tiers live in agents/*.md")
        for banned in ("Date.now(", "Math.random(", "new Date()"):
            if banned in text:
                errors.append(f"{w}: `{banned}` breaks workflow resume")
    hooks = plugin_dir / "hooks" / "hooks.json"
    if hooks.exists():
        try:
            cfg = json.loads(hooks.read_text())
        except json.JSONDecodeError as e:
            return errors + [f"{hooks}: not valid JSON ({e})"]
        for groups in cfg.get("hooks", {}).values():
            for group in groups:
                for h in group.get("hooks", []):
                    for ref in re.findall(r"\$\{CLAUDE_PLUGIN_ROOT\}/([A-Za-z0-9._/-]+)", h.get("command", "")):
                        if not (plugin_dir / ref).exists():
                            errors.append(f"{hooks}: command points at `{ref}`, which does not exist")
    return errors


def check_release(root: pathlib.Path, plugin_dir: pathlib.Path) -> list[str]:
    errors = []
    manifest = json.loads((plugin_dir / ".claude-plugin" / "plugin.json").read_text())
    version = manifest.get("version")
    if not version:
        errors.append("plugin.json: version is missing")
    market = json.loads((root / ".claude-plugin" / "marketplace.json").read_text())
    if not market.get("description") and not market.get("metadata", {}).get("description"):
        errors.append("marketplace.json: description is missing")
    for entry in market.get("plugins", []):
        if "version" in entry:
            errors.append("marketplace.json: drop `version` from the plugin entry; plugin.json is the one source")
    changelog = root / "CHANGELOG.md"
    if not changelog.exists() or f"## {version}" not in changelog.read_text():
        errors.append(f"CHANGELOG.md: no `## {version}` section for the version in plugin.json")
    return errors


def run(root: pathlib.Path, report: bool = False) -> int:
    plugin_dir = root / "plugins" / PLUGIN
    errors: list[str] = []
    stats = []
    for skill_dir in sorted(p for p in (plugin_dir / "skills").iterdir() if p.is_dir()):
        if not (skill_dir / "SKILL.md").exists():
            errors.append(f"{skill_dir}: no SKILL.md")
            continue
        e, s = check_skill(skill_dir)
        errors += e + check_local_refs(skill_dir)
        stats.append(s)
    total_desc = sum(s["desc"] for s in stats)
    if total_desc > MAX_TOTAL_DESC:
        errors.append(f"skill listing: descriptions total {total_desc} chars, budget {MAX_TOTAL_DESC}")
    errors += check_cross_refs(plugin_dir) + check_standalone(plugin_dir)
    errors += check_components(plugin_dir) + check_release(root, plugin_dir)

    if report:
        print("| Skill | Description (chars) | SKILL.md body (chars) | Body (est. tokens) |")
        print("|---|---:|---:|---:|")
        for s in stats:
            print(f"| `{s['name']}` | {s['desc']} | {s['body_chars']:,} | {s['body_chars'] // CHARS_PER_TOKEN:,} |")
        print(f"| **Total, {len(stats)} skills** | **{total_desc:,}** | | |")
        print(f"\nAlways-loaded listing: {total_desc:,} chars, about {total_desc // CHARS_PER_TOKEN:,} tokens "
              f"(estimate at {CHARS_PER_TOKEN} chars per token; budget {MAX_TOTAL_DESC:,}).")
    for e in errors:
        print(f"ERROR {e}".replace(str(root) + "/", ""))
    print(f"{len(stats)} skills checked, {len(errors)} error(s).")
    return 1 if errors else 0


if __name__ == "__main__":
    argv = [a for a in sys.argv[1:] if a != "--report"]
    repo = pathlib.Path(argv[0]).resolve() if argv else pathlib.Path(__file__).resolve().parent.parent
    sys.exit(run(repo, report="--report" in sys.argv))
