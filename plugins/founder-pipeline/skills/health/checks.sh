#!/usr/bin/env bash
# Deterministic health sweep. Usage: checks.sh [project-dir]   (default: cwd)
# Prints machine-readable findings; judgment + fixes stay in SKILL.md.
PROJ="${1:-$PWD}"
cd "$PROJ" || exit 1
CDIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"

# ---------------------------------------------------------------------------
# Configuration. These are the only project-specific knobs in this script —
# adapt them to your own conventions rather than ignoring the findings.
# ---------------------------------------------------------------------------
# L1 — line limits: per CLAUDE.md file, and for the whole auto-loaded chain.
L1_FILE_LIMIT=${L1_FILE_LIMIT:-200}
L1_CHAIN_LIMIT=${L1_CHAIN_LIMIT:-400}
# L2 — invariant rules that must appear exactly ONCE in any loaded chain.
# Format: "LABEL:distinctive substring of the rule". Two shipped defaults;
# replace them with whatever standing instructions your projects declare.
L2_RULES=(
  "GR:95% confidence"
  "WD:State your assumptions out loud"
)

echo "### PROJECT: $PROJ"
echo

echo "## L0 HARNESS"
command -v claude >/dev/null && claude doctor 2>&1 | grep -Ev '^$|^For a full' | sed 's/^/  doctor: /'
for f in "$CDIR/settings.json" "$CDIR/settings.local.json" ".claude/settings.json" ".claude/settings.local.json"; do
  [ -f "$f" ] || continue
  python3 -c "import json,sys; json.load(open(sys.argv[1]))" "$f" 2>/dev/null \
    && echo "  json OK: $f" || echo "  json BROKEN: $f"
done
python3 - "$CDIR" <<'PY'
import json, os, shlex, sys
cdir = sys.argv[1]
for name in ("settings.json", "settings.local.json"):
    p = os.path.join(cdir, name)
    if not os.path.exists(p): continue
    try: s = json.load(open(p))
    except Exception: continue
    for ev, arr in s.get("hooks", {}).items():
        for m in arr:
            for h in m.get("hooks", []):
                for tok in shlex.split(h.get("command", "")):
                    if "/" in tok and tok.rsplit(".", 1)[-1] in ("js", "sh", "py"):
                        if not os.path.exists(tok):
                            print(f"  hook MISSING: {ev} -> {tok}")
    sl = s.get("statusLine", {}).get("command", "")
    for tok in shlex.split(sl):
        if "/" in tok and not os.path.exists(tok):
            print(f"  statusLine MISSING: {tok}")
    env = s.get("env", {})
    if env.get("DISABLE_TELEMETRY") == "1":
        print("  env NOTE: DISABLE_TELEMETRY=1 also disables feature-flag eval "
              "(any feature gated behind a flag stays off)")
PY
echo

echo "## L0b RUNTIME (hook processes, self-exec wrappers, machine pressure)"
python3 - <<'PY'
import subprocess, os, re, glob, collections

def secs(t):
    """Parse ps etime/time: [[dd-]hh:]mm:ss[.ff]"""
    t = t.strip(); d = 0
    if "-" in t:
        head, t = t.split("-", 1); d = int(head)
    try: p = [float(x) for x in t.split(":")]
    except ValueError: return 0.0
    while len(p) < 3: p.insert(0, 0.0)
    return d*86400 + p[0]*3600 + p[1]*60 + p[2]

# --- runaway hook / plugin / skill processes -------------------------------
# Hooks are meant to be sub-second. Seconds of CPU or an hour of wall time is a defect.
try:
    raw = subprocess.run(["ps", "-Ao", "pid=,etime=,time=,command="],
                         capture_output=True, text=True, timeout=15).stdout
except Exception:
    raw = ""
HOOKISH = re.compile(r'/\.claude/(hooks|plugins|skills|jobs)/')
runaway, byscript = [], collections.Counter()
for line in raw.splitlines():
    parts = line.split(None, 3)
    if len(parts) < 4: continue
    pid, et, ct, cmd = parts
    if not HOOKISH.search(cmd) or "checks.sh" in cmd: continue
    cpu, wall = secs(ct), secs(et)
    script = next((tok for tok in cmd.split() if HOOKISH.search(tok)), cmd[:60])
    byscript[script] += 1
    if cpu > 60 or wall > 1800:
        runaway.append((int(cpu), int(wall), pid, script))
for cpu, wall, pid, script in sorted(runaway, reverse=True)[:15]:
    print(f"  hook RUNAWAY: pid {pid}  cpu={cpu}s wall={wall}s  {script}")
for script, n in byscript.most_common():
    if n >= 4:
        print(f"  hook PILEUP: {n} concurrent instances of {script}")
if not runaway and not any(n >= 4 for n in byscript.values()):
    print(f"  hook processes OK ({sum(byscript.values())} live, none runaway)")

# --- self-referential exec wrappers ---------------------------------------
# A wrapper that execs its own path spins forever, silently. See the documented
# case in SKILL.md L0b: one core pegged per session-stop, wired memory to 12 GB,
# machine unusable. Patterns that don't exist on this machine are simply skipped;
# add your own script directories here if you keep them elsewhere.
home = os.path.expanduser("~")
seen = set()
# Override with WRAPPER_SCAN_DIRS (colon-separated globs) to match your layout.
_default = "~/.local/bin/*:~/.local/share/*/bin/*:~/.claude/scripts/*"
for pat in os.environ.get("WRAPPER_SCAN_DIRS", _default).split(":"):
    for f in glob.glob(os.path.expanduser(pat)):
        if f in seen or not os.path.isfile(f) or not os.access(f, os.X_OK): continue
        seen.add(f)
        try: txt = open(f, errors="ignore").read(8000)
        except Exception: continue
        if not txt.startswith("#!"): continue
        real = os.path.realpath(f)
        for line in txt.splitlines():
            s = line.strip()
            if not s.startswith("exec "): continue
            for a, b in re.findall(r'"([^"]+)"|(\S+)', s):
                tok = (a or b).replace("$HOME", home).replace("${HOME}", home)
                if not tok.startswith("/"): continue
                if os.path.realpath(tok) == real:
                    print(f"  self-exec LOOP: {f}")
                    print(f"                  {s}")

# --- machine pressure ------------------------------------------------------
def sysctl(k):
    try: return subprocess.run(["sysctl","-n",k],capture_output=True,text=True,timeout=5).stdout.strip()
    except Exception: return ""
ncpu = int(sysctl("hw.ncpu") or 0)
ram  = int(sysctl("hw.memsize") or 0)
load = os.getloadavg()[0]
vm = subprocess.run(["vm_stat"], capture_output=True, text=True).stdout
pg = int(re.search(r'page size of (\d+)', vm).group(1)) if "page size of" in vm else 16384
wired = int(re.search(r'wired down:\s+(\d+)', vm).group(1)) * pg if "wired down" in vm else 0
swap = sysctl("vm.swapusage")
swap_used = float(re.search(r'used = ([\d.]+)M', swap).group(1)) if "used =" in swap else 0.0
flags = []
if ncpu and load > ncpu * 1.5: flags.append(f"load {load:.1f} on {ncpu} cores")
if ram and wired > ram * 0.5:  flags.append(f"wired {wired/2**30:.1f} GB of {ram/2**30:.0f} GB")
if swap_used > 4096:           flags.append(f"swap {swap_used/1024:.1f} GB used")
print(f"  machine: load {load:.1f}/{ncpu}c, wired {wired/2**30:.1f}GB/{ram/2**30:.0f}GB, swap {swap_used/1024:.1f}GB"
      + ("  <-- PRESSURE: " + "; ".join(flags) if flags else ""))
PY
echo

echo "## L1 CLAUDE.md INVENTORY (limit $L1_FILE_LIMIT lines each)"
find . -name CLAUDE.md -not -path "*/node_modules/*" -not -path "*/.git/*" 2>/dev/null \
  | while read -r f; do printf "  %4s  %s\n" "$(wc -l < "$f" | tr -d ' ')" "$f"; done | sort -rn
echo "  --- auto-loaded chain for this project (limit $L1_CHAIN_LIMIT) ---"
CHAIN=$(wc -l "$CDIR"/CLAUDE.md "$CDIR"/*.md ./CLAUDE.md 2>/dev/null | tail -1 | awk '{print $1}')
echo "  chain total: ${CHAIN:-?} lines (~$(( ${CHAIN:-0} * 5 )) tokens)"
echo

echo "## L2 INVARIANT RULES (each must appear ONCE per loaded chain)"
for rule in "${L2_RULES[@]}"; do
  label="${rule%%:*}"; needle="${rule#*:}"
  if grep -q "$needle" "$CDIR/CLAUDE.md" 2>/dev/null; then
    echo "  global: HAS $label"
  else
    echo "  global: no $label (project roots must carry it)"
  fi
done
find . -name CLAUDE.md -not -path "*/node_modules/*" 2>/dev/null | sort | while read -r f; do
  hits=""; any=0
  for rule in "${L2_RULES[@]}"; do
    label="${rule%%:*}"; needle="${rule#*:}"
    if grep -q "$needle" "$f"; then hits="$hits $label"; any=1
    else hits="$hits $(printf '%*s' ${#label} '')"; fi
  done
  [ "$any" = 0 ] || echo "  $hits  $f"
done
echo "  (repeats in nested files = duplication, not compliance — the chain loads all of them)"
echo

echo "## L3 UNRESOLVED PATH REFERENCES"
python3 - <<'PY'
import os, re
root = os.getcwd()
parent = os.path.dirname(root)
# Only real filesystem pointers. Deliberately NOT checked (not file refs):
#   URL routes (/cfp, /api/add), bare filenames named as concepts (Layout.astro),
#   globs/placeholders (*, {a,b}, <account>, ...), hostnames.
for dirpath, dirs, files in os.walk(root):
    dirs[:] = [d for d in dirs if d not in (".git", "node_modules", ".claude", "dist")]
    if "CLAUDE.md" not in files: continue
    md = os.path.join(dirpath, "CLAUDE.md")
    txt = open(md, errors="ignore").read()
    # historical annotations are intentional, not broken pointers
    txt = re.sub(r'\((?:was|formerly|renamed from)\s+`[^`]+`\)', '', txt, flags=re.I)
    bad = []
    for c in set(re.findall(r'`([^`\n]+)`', txt)):
        c = c.strip().rstrip(',;')
        if "/" not in c: continue                                  # bare name, not a path
        if re.search(r'[*{}<>?…]|\.\.\.', c): continue             # glob / placeholder
        if re.search(r'''["'=&|:;]''', c): continue                # code snippet, not a path
        if " " in c and not c.startswith(("/", "~")): continue     # prose/command, not a rel path
        if c.count("/") == 1 and c.endswith("/"): continue         # shorthand for a dir named nearby
        if re.match(r'^(https?:|www\.|@|\$)', c): continue
        if re.search(r'\.(io|com|cz|sk|net|org|dev)(/|$)', c): continue   # hostname
        if c.startswith("~"):
            cands = [os.path.expanduser(c)]
        elif c.startswith("/"):
            # absolute only if it names a real filesystem root; else it's a URL route
            if not os.path.isdir("/" + c.lstrip("/").split("/")[0]): continue
            cands = [c]
        else:
            cands = [os.path.join(b, c) for b in (dirpath, root, parent)]
        if not any(os.path.exists(os.path.normpath(p)) for p in cands):
            bad.append(c)
    for b in sorted(bad):
        print(f"  MISSING: {b}   <- {os.path.relpath(md, root)}")
PY
echo

echo "## L4 MEMORY INDEX"
python3 - "$PROJ" "$CDIR" <<'PY'
import os, re, sys
slug = re.sub(r'[/ _]', '-', sys.argv[1])
d = os.path.join(sys.argv[2], "projects", slug, "memory")
if not os.path.isdir(d):
    print("  no memory dir"); raise SystemExit
idx = os.path.join(d, "MEMORY.md")
linked = set(re.findall(r'\]\(([^)]+\.md)\)', open(idx).read())) if os.path.exists(idx) else set()
files = {f for f in os.listdir(d) if f.endswith(".md") and f != "MEMORY.md"}
print("  orphan files (not indexed):", ", ".join(sorted(files - linked)) or "none")
print("  dead index entries:", ", ".join(sorted(linked - files)) or "none")
print(f"  {len(files)} memories (~{sum(os.path.getsize(os.path.join(d,f)) for f in files)//4} tokens if all loaded)")
PY
echo

echo "## L5 SYSTEMIC (same broken ref across sibling projects?)"
echo "  run: grep -rl '<broken-ref>' \"\$(dirname \"$PROJ\")\" --include=CLAUDE.md"
echo "  >1 hit = fix at the source, report once, do not re-file per project"
