#!/usr/bin/env python3
"""Diff the NAP on every claimed local listing against the canonical one.

Law 6 says name, address, phone and website are identical everywhere. Nothing has
ever checked it. This does, and it reads the canonical values from exactly one place:
references/entity-pack.md.

  python3 nap_audit.py --list                 # what entity blocks exist
  python3 nap_audit.py "<entity or property>" # diff every local-tier listing
  python3 nap_audit.py "<...>" --json

Two honesty rules baked in:
  - CHK rows are CANDIDATES, not verdicts. A listing behind a login or rendered by JS
    reads as "missing" to a plain fetch. Confirm before editing anything.
  - If a property cannot be resolved to an entity block, this refuses to guess.
    A portfolio with several legal entities will have properties whose operating
    entity is genuinely unconfirmed, and inventing that mapping is exactly the
    drift Law 6 exists to prevent.
"""

import argparse
import json
import os
import re
import sys
import unicodedata
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = "Mozilla/5.0 (compatible; web-listings-nap-audit/1.0)"
FIELDS = ("name", "address", "phone", "website")

# entity-pack.md writes these labels; map them onto the four NAP fields.
ALIASES = {
    "legal name": "name", "name": "name", "org name": "name",
    "registered address": "address", "address": "address",
    "phone": "phone", "telephone": "phone",
    "website": "website", "official website": "website", "url": "website",
}


def normalise_phone(s):
    return re.sub(r"[^\d+]", "", s or "")


def normalise_name(s):
    """Casefold, collapse whitespace, strip diacritics.

    Diacritic folding is not optional in any market whose language carries them:
    a name written with diacritics on one listing and without them on another must
    compare equal, or every local listing reads as drift.
    """
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", s).strip().casefold()


def _norm(field, value):
    return normalise_phone(value) if field == "phone" else normalise_name(value)


PLACEHOLDERS = {"not defined", "none", "n/a", "na", "tbd", "unknown", "unconfirmed", "-"}


def clean_value(raw):
    """Strip entity-pack.md's inline commentary and reject placeholders.

    The file annotates values with an em-dash aside ("+420 ... — UNCONFIRMED, sourced
    from..."). Kept whole, that value never matches anything on a listing, so every
    row reads as drift. A placeholder like "not defined" is a note to a human, not
    something to diff against.
    """
    v = re.split(r"\s+[—–]\s+", (raw or "").strip())[0]
    v = re.sub(r"\s*\(.*?\)\s*$", "", v)
    # The em-dash cut can leave a parenthetical open:
    #   'Engineering Leaders Hub s.r.o. (renamed from "Augment Lab, s.r.o."'
    # An unbalanced '(' means the aside started here and its close was trimmed away.
    if v.count("(") > v.count(")"):
        v = v[:v.rindex("(")]
    v = v.strip().strip("*").strip()
    return "" if v.lower() in PLACEHOLDERS else v


def parse_entity_pack(md):
    """{block heading: {field: value}} from `##`/`###` blocks.

    Handles both shapes the file uses: `- Field: value` bullets and
    `| Field | Value |` table rows. The heading key is trimmed at the em-dash the
    file uses for its inline commentary.
    """
    packs, current = {}, None
    for line in md.splitlines():
        h = re.match(r"^#{2,3}\s+(.+?)\s*$", line)
        if h:
            current = re.split(r"\s+[—–]\s+", h.group(1))[0].strip()
            packs.setdefault(current, {})
            continue
        if current is None:
            continue

        m = re.match(r"^\s*-\s*\*{0,2}([A-Za-zÀ-ž /]+?)\*{0,2}\s*:\s*(.+?)\s*$", line)
        if not m:
            m = re.match(r"^\s*\|\s*([A-Za-zÀ-ž /]+?)\s*\|\s*(.+?)\s*\|\s*$", line)
        if not m:
            continue
        label = ALIASES.get(m.group(1).strip().lower())
        if not label or label in packs[current]:
            continue
        value = clean_value(m.group(2))
        if value:
            packs[current][label] = value
    return packs


def resolve(packs, wanted):
    """Exact heading match, else a single unambiguous substring match, else None."""
    if wanted in packs:
        return wanted, packs[wanted]
    hits = [k for k in packs if normalise_name(wanted) in normalise_name(k)]
    return (hits[0], packs[hits[0]]) if len(hits) == 1 else (None, None)


def diff_nap(canonical, found):
    out = []
    for field in FIELDS:
        expected = canonical.get(field)
        if not expected:
            continue
        actual = found.get(field)
        if not actual:
            status = "missing"
        elif _norm(field, expected) == _norm(field, actual):
            status = "exact"
        else:
            status = "drift"
        out.append({"field": field, "expected": expected, "found": actual, "status": status})
    return out


def fetch(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=45) as r:
            return r.read().decode("utf-8", "replace")
    except (urllib.error.URLError, urllib.error.HTTPError, OSError):
        return ""


def scan(html, canonical):
    """Best-effort presence scan. 'Not found by this scan' is not 'absent' — see the
    CHK caveat printed by the CLI."""
    text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html))
    return {f: canonical[f] for f in FIELDS
            if canonical.get(f) and _norm(f, canonical[f]) in _norm(f, text)}


def load_packs():
    with open(os.path.join(ROOT, "references", "entity-pack.md"), encoding="utf-8") as fh:
        return parse_entity_pack(fh.read())


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("entity", nargs="?")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    packs = load_packs()
    usable = {k: v for k, v in packs.items() if v}

    if args.list or not args.entity:
        print("Entity blocks carrying NAP fields in entity-pack.md:\n")
        for k, v in usable.items():
            print(f"  {k}\n      {', '.join(f'{f}={v[f]!r}' for f in FIELDS if f in v)}")
        missing = [f for f in FIELDS if not any(f in v for v in usable.values())]
        if missing:
            print(f"\n  NOT PRESENT ANYWHERE in entity-pack.md: {', '.join(missing)}")
            print("  Law 6 cannot be checked for a field the canonical source does not define.")
        return 0

    key, canonical = resolve(usable, args.entity)
    if not canonical:
        print(f"Cannot resolve {args.entity!r} to a single entity block.")
        print(f"Blocks: {sorted(usable)}")
        print("\nRefusing to guess. Where entity-pack.md leaves a property's operating "
              "entity unconfirmed, inventing that mapping is the drift Law 6 exists "
              "to prevent. Ask the owner, then pass the entity name directly.")
        return 2

    with open(os.path.join(ROOT, "config", "targets.json"), encoding="utf-8") as fh:
        targets = json.load(fh)["targets"]

    rows, unrecorded = [], []
    for t in targets:
        if not t.get("local_tier"):
            continue
        # `url` is the DIRECTORY's homepage, not our listing on it. Scanning that
        # would report seventeen meaningless "missing" rows and look like a finding.
        # A listing can only be checked once its own URL has been recorded.
        listing = t.get("listing_url")
        if not listing:
            unrecorded.append(t)
            continue
        rows.append({"id": t["id"], "name": t["name"], "url": listing,
                     "local_tier": t["local_tier"],
                     "diff": diff_nap(canonical, scan(fetch(listing), canonical))})

    if args.json:
        print(json.dumps({"entity": key, "canonical": canonical, "rows": rows,
                          "unrecorded": [t["id"] for t in unrecorded]},
                         indent=2, ensure_ascii=False))
        return 0

    print(f"Canonical entity: {key}")
    print("  " + " · ".join(f"{f}={canonical[f]!r}" for f in FIELDS if f in canonical) + "\n")
    for r in sorted(rows, key=lambda x: x["local_tier"]):
        bad = [d for d in r["diff"] if d["status"] != "exact"]
        print(f"{'OK  ' if not bad else 'CHK '}T{r['local_tier']} {r['id']} {r['name']}")
        for d in bad:
            print(f"       {d['status']:8} {d['field']}: expected {d['expected']!r}, found {d['found']!r}")
    if not rows:
        print("  (nothing checkable yet)")
    if unrecorded:
        print(f"\n{len(unrecorded)} local-tier target(s) have no `listing_url` recorded, so "
              f"they cannot be checked:")
        for t in sorted(unrecorded, key=lambda x: x["local_tier"]):
            print(f"  T{t['local_tier']} {t['id']} {t['name']}")
        print("  Fix: record `listing_url` on the row when a listing is created "
              "(/founder-pipeline:web-listings Phase 4). Until then this is UNMEASURED, "
              "not clean.")
    if rows:
        print("\nCHK rows are CANDIDATES, not verdicts. A listing behind a login or "
              "rendered by JavaScript reads as missing to a plain fetch. Confirm first.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
