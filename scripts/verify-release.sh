#!/usr/bin/env bash
# verify-release.sh — pre-push gate for this public repo. Runs locally and in CI.
#
# Checks FILES, never agent claims. Written because during the port one agent
# reported progress on a file it had made zero edits to, and four others died
# mid-run. Nothing ships on the strength of a report.
#
# Exit 0 = clean. Exit 1 = at least one BLOCKER. Warnings never fail the build.
#
# Usage:  bash scripts/verify-release.sh [path-to-repo]
#
# The identity check scans for private names (people, companies, internal folder
# codes) that must never reach a public repo. That list is itself private, so it
# is not in this file: put it in `.release-identity` at the repo root (gitignored)
# as two shell variables, IDENT='name1|name2' and PRIVATE_PATHS='pattern1|pattern2'.
# Without that file (for example in CI) the identity check is skipped and says so;
# every other check still runs.

set -uo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="${1:-$(cd "$HERE/.." && pwd)}"
BLOCKERS=0
WARNINGS=0

red()  { printf "\033[31m%s\033[0m\n" "$*"; }
yel()  { printf "\033[33m%s\033[0m\n" "$*"; }
grn()  { printf "\033[32m%s\033[0m\n" "$*"; }
hdr()  { printf "\n\033[1m── %s\033[0m\n" "$*"; }

block() { red   "  BLOCKER: $*"; BLOCKERS=$((BLOCKERS+1)); }
warn()  { yel   "  warning: $*"; WARNINGS=$((WARNINGS+1)); }

[ -d "$REPO" ] || { red "No repo at $REPO"; exit 1; }
cd "$REPO" || exit 1

# Scan what SHIPS, not the working folder: tracked files plus untracked files
# that are not gitignored. Git internals (.git/) and ignored agent state
# (.memsearch/) never reach GitHub, so flagging them is noise that trains
# people to ignore the scanner. Added 2026-11-04.
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  SHIP="$(mktemp -d)"
  trap 'rm -rf "$SHIP"' EXIT
  git ls-files -co --exclude-standard -z | (cd "$REPO" && xargs -0 -I{} rsync -R "{}" "$SHIP/") 2>/dev/null
  cd "$SHIP" || exit 1
fi

# Reviewed-and-cleared allowlist. One string per line, `string  # why`.
# A scanner that cries wolf gets ignored, so false positives are retired
# deliberately and with a recorded reason — never by loosening a pattern.
ALLOW="$HERE/release-allowlist.txt"
allowed() {
  [ -f "$ALLOW" ] || return 1
  grep -v '^\s*#' "$ALLOW" 2>/dev/null | sed 's/[[:space:]]*#.*//' | grep -v '^\s*$' \
    | grep -qxF "$1"
}
# Filter a newline-separated list through the allowlist.
sieve() { while IFS= read -r l; do [ -n "$l" ] && ! allowed "$l" && printf '%s\n' "$l"; done; }
# Files fully cleared via `file:` entries — used to exempt specific files from
# a whole check (e.g. the licence is SUPPOSED to carry the author's name).
allowed_file() {
  [ -f "$ALLOW" ] || return 1
  local f="${1#./}"
  grep '^file:' "$ALLOW" 2>/dev/null | sed 's/^file:[[:space:]]*//;s/[[:space:]]*#.*//' | grep -v '^\s*$' \
    | grep -qxF "$f"
}
filter_allowed_files() { while IFS= read -r f; do [ -n "$f" ] && ! allowed_file "$f" && printf '%s\n' "$f"; done; }

echo "Scanning $(pwd)"
echo "Files: $(find . -type f | wc -l | tr -d ' ')   Size: $(du -sh . | cut -f1)"

# ---------------------------------------------------------------- 1. identity
hdr "1. Owner and business identity"

# Names are checked case-insensitively and as substrings, because they hide
# inside filenames, JSON keys, schema @ids and heredocs.
IDENT=""; PRIVATE_PATHS=""
[ -f "$REPO/.release-identity" ] && . "$REPO/.release-identity"
if [ -z "$IDENT" ]; then
  yel "  skipped: no .release-identity file (private name list not available here)"
else
  hits=$(grep -rEil "$IDENT" . 2>/dev/null | filter_allowed_files)
  if [ -n "$hits" ]; then
    block "owner/business identity in $(echo "$hits" | wc -l | tr -d ' ') file(s):"
    echo "$hits" | sed 's|^\./|    |' | head -25
  else
    grn "  clean"
  fi
  if [ -n "$PRIVATE_PATHS" ]; then
    hits=$(grep -rEl "$PRIVATE_PATHS" . 2>/dev/null | filter_allowed_files)
    if [ -n "$hits" ]; then
      block "private workspace paths in:"; echo "$hits" | sed 's|^\./|    |' | head -15
    else
      grn "  no private workspace paths"
    fi
  fi
fi

# ------------------------------------------------------------------- 2. PII
hdr "2. Personal data (own and third-party)"

phones=$(grep -rEoh '\+4[0-9]{1,2}[ ]?[0-9]{3}[ ]?[0-9]{3}[ ]?[0-9]{3}' . 2>/dev/null \
  | sort -u | sieve)
if [ -n "$phones" ]; then
  block "phone numbers not on the reviewed allowlist:"; echo "$phones" | sed 's|^|    |'
else
  grn "  no unreviewed phone numbers"
fi

emails=$(grep -rEoh '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}' . 2>/dev/null \
  | grep -Eiv 'example\.(com|org)|@[a-z-]+\.local|noreply@|user@|you@|name@' | sort -u | sieve)
if [ -n "$emails" ]; then
  block "email addresses not on the reviewed allowlist:"; echo "$emails" | sed 's|^|    |' | head -20
else
  grn "  no unreviewed email addresses"
fi

# ------------------------------------------------------------ 3. credentials
hdr "3. Credentials and secrets"

# Shapes, not names: long hex, sk-/fc-/phc-/phx- prefixes, bearer tokens.
hits=$(grep -rEn '[a-f0-9]{32,}|\b(sk|fc|phc|phx|rk)_[A-Za-z0-9_-]{16,}|Bearer [A-Za-z0-9._-]{20,}' . 2>/dev/null \
  | grep -Eiv 'example|placeholder|your-|xxxx|<|\$\{' | head -12)
if [ -n "$hits" ]; then
  block "credential-shaped strings:"; echo "$hits" | sed 's|^\./|    |' | cut -c1-130
else
  grn "  no credential-shaped strings"
fi

hits=$(grep -rEl 'API_TOKEN|API_KEY|_SECRET|_TOKEN' . 2>/dev/null | head -10)
if [ -n "$hits" ]; then
  warn "files naming credential variables — confirm each is the user's own to set, not a read of the author's:"
  echo "$hits" | sed 's|^\./|    |'
fi

# ------------------------------------------------------------------ 4. paths
hdr "4. Paths that break on another machine"

hits=$(grep -rn '/Users/\|/home/[a-z]\|~/\.claude\|~/\.env\|My Drive\|Google Drive' . 2>/dev/null \
  | grep -vE '^\./(plugins/founder-pipeline/skills/founder/INSTALL\.md|README\.md):[0-9]+:.*~/\.claude/skills' \
  | grep -vFf <(grep '^file:' "$ALLOW" 2>/dev/null | sed 's/^file:[[:space:]]*//;s/[[:space:]]*#.*//' | grep -v '^$' || true) 2>/dev/null | head -12)
if [ -n "$hits" ]; then
  block "absolute or home-relative paths:"; echo "$hits" | sed 's|^\./|    |' | cut -c1-130
else
  grn "  no machine-local paths"
fi

# Every ${CLAUDE_PLUGIN_ROOT} pointer must resolve to a file that exists.
broken=0
while IFS= read -r ref; do
  rel="${ref#*CLAUDE_PLUGIN_ROOT\}/}"; rel="${rel%%[\`\ \)\"]*}"
  [ -n "$rel" ] && [ ! -e "plugins/founder-pipeline/$rel" ] && { echo "    missing: $rel"; broken=$((broken+1)); }
done < <(grep -rhoE '\$\{CLAUDE_PLUGIN_ROOT\}/[A-Za-z0-9._/-]+' plugins 2>/dev/null | sort -u)   # plugins/ only: tests/ holds deliberately broken fixtures
[ "$broken" -gt 0 ] && block "$broken dangling \${CLAUDE_PLUGIN_ROOT} pointer(s)" || grn "  all plugin-root pointers resolve"

# -------------------------------------------------------------- 5. structure
hdr "5. Plugin structure"

[ -f ".claude-plugin/marketplace.json" ] || block "missing .claude-plugin/marketplace.json"
[ -f "plugins/founder-pipeline/.claude-plugin/plugin.json" ] || block "missing plugin.json"
[ -f "LICENSE" ] || block "missing LICENSE"
[ -f "README.md" ] || block "missing README.md"

for j in .claude-plugin/marketplace.json plugins/founder-pipeline/.claude-plugin/plugin.json; do
  [ -f "$j" ] && { python3 -c "import json,sys; json.load(open('$j'))" 2>/dev/null \
    || block "$j is not valid JSON"; }
done

hits=$(grep -rl 'REPLACE_WITH_YOUR' . 2>/dev/null | filter_allowed_files)
[ -n "$hits" ] && { block "unfilled placeholders in:"; echo "$hits" | sed 's|^\./|    |'; } \
                || grn "  no unfilled placeholders"

sk="plugins/founder-pipeline/skills"
if [ -d "$sk" ]; then
  for d in "$sk"/*/; do
    [ -f "$d/SKILL.md" ] || block "skill without SKILL.md: $(basename "$d")"
  done
  echo "  $(ls -d "$sk"/*/ 2>/dev/null | wc -l | tr -d ' ') skills present"
fi

links=$(find . -type l 2>/dev/null)
[ -n "$links" ] && { block "symlinks will ship broken:"; echo "$links" | sed 's|^\./|    |'; } \
                 || grn "  no symlinks"

# ---------------------------------------------------------------- 6. junk
hdr "6. Artifacts that must not ship"

junk=$(find . \( -name "*.pyc" -o -name "__pycache__" -o -name ".DS_Store" \
  -o -name ".memsearch" -o -name "AUDIT-*.md" -o -name "*.bak" -o -name ".env" \) 2>/dev/null)
[ -n "$junk" ] && { block "build/junk artifacts:"; echo "$junk" | sed 's|^\./|    |'; } \
                || grn "  clean"

# --------------------------------------------------- 7. dangling skill refs
hdr "7. Skill references"

# Any /skill invocation must be namespaced to this plugin or be a known public plugin.
PUBLIC='posthog:|Notion:|cloudflare:|frontend-design:|founder-pipeline:'
# Plain /<name> refs to a skill bundled in this plugin are intended since v0.2:
# founder resolves them bundled -> user's own -> inline fallback
# (skills/founder/references/capabilities.md), so they are not dangling.
BUNDLED=$(ls plugins/*/skills 2>/dev/null | grep -v ':' | grep -v '^$' | sed 's|^|/|;s|$|$|' | paste -sd'|' -)
dangling=$(grep -rhoE '(^|[^a-z/])/[a-z][a-z0-9-]{2,}(:[a-z0-9-]+)?' . 2>/dev/null \
  | grep -oE '/[a-z][a-z0-9:-]+' | grep -Ev "$PUBLIC" | grep -Ev "${BUNDLED:-^$}" | sort | uniq -c | sort -rn | head -15)
if [ -n "$dangling" ]; then
  warn "possible un-namespaced skill refs (review — many will be URL paths, not skills):"
  echo "$dangling" | sed 's|^|    |'
else
  grn "  no dangling skill references"
fi

# ------------------------------------------------------------------ verdict
hdr "Verdict"
if [ "$BLOCKERS" -gt 0 ]; then
  red "  $BLOCKERS blocker(s), $WARNINGS warning(s) — DO NOT PUSH"
  exit 1
else
  grn "  0 blockers, $WARNINGS warning(s) — safe to push"
  echo "  Warnings still need a human read. This script catches shapes, not judgment:"
  echo "  it cannot see a client anecdote, a testimonial quote, or a named company."
  exit 0
fi
