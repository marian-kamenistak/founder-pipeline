#!/usr/bin/env python3
"""select_targets.py — read config/targets.json without loading it into the conversation.

The registry is about 155 KB (roughly 39,000 tokens). Reading it whole to pick a dozen rows
wastes the context the rest of the run needs, so this prints only what a step asks for.

  python3 select_targets.py --class community            # rows that apply to a brand class
  python3 select_targets.py --class services --territory worldwide cz --priority 1
  python3 select_targets.py --unassigned                  # rows with applies_to: []
  python3 select_targets.py --id DIR-0001                 # one full row, notes included

List output is one compact line per target, without notes:
  id | priority | territory | category | cost | name | submit_url
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

DEFAULT = pathlib.Path(__file__).resolve().parent.parent / "config" / "targets.json"


def select(targets, brand_class=None, territories=None, priority=None, unassigned=False):
    rows = []
    for t in targets:
        applies = t.get("applies_to") or []
        if unassigned:
            if applies:
                continue
        elif brand_class and brand_class not in applies:
            continue
        if territories and t.get("territory") not in territories:
            continue
        if priority is not None and t.get("priority") != priority:
            continue
        rows.append(t)
    return sorted(rows, key=lambda t: (t.get("priority") or 99, t.get("id", "")))


def line(t):
    return " | ".join(str(t.get(k, "")) for k in ("id", "priority", "territory", "category", "cost", "name")) \
        + " | " + str(t.get("submit_url") or t.get("url") or "")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", default=str(DEFAULT))
    ap.add_argument("--class", dest="brand_class")
    ap.add_argument("--territory", nargs="+")
    ap.add_argument("--priority", type=int)
    ap.add_argument("--unassigned", action="store_true")
    ap.add_argument("--id")
    a = ap.parse_args(argv)
    targets = json.loads(pathlib.Path(a.file).read_text())["targets"]
    if a.id:
        hit = [t for t in targets if t.get("id") == a.id]
        if not hit:
            print(f"no target with id {a.id}", file=sys.stderr)
            return 1
        print(json.dumps(hit[0], indent=2, ensure_ascii=False))
        return 0
    if not (a.brand_class or a.unassigned):
        ap.error("give --class <brand_class>, --unassigned or --id <ID>; printing all rows defeats the purpose")
    rows = select(targets, a.brand_class, a.territory, a.priority, a.unassigned)
    for t in rows:
        print(line(t))
    print(f"{len(rows)} of {len(targets)} targets", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
