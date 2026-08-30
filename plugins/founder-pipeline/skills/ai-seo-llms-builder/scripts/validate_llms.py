#!/usr/bin/env python3
"""
Validate an llms.txt / llms-full.txt against the spec plus the house rules in
../references/spec.md.

    validate_llms.py <url-or-path> --strict            # llms.txt profile
    validate_llms.py <url-or-path> --archive           # llms-full.txt profile
    validate_llms.py <url> --strict --check-links      # HEAD every routed URL
    validate_llms.py <url> --strict --data-points <p>  # cross-check numbers vs the registry
    validate_llms.py <url> --strict --catalog <p>      # diff prices vs the offer catalog

--data-points expects a JSON snapshot in the shape
    {"streams": {"<stream>": {"data_points": {"<key>": {"display": "...", ...}}}}}
Wherever your data-points registry actually lives (a database, a spreadsheet, a YAML file),
export it to that shape and pass the snapshot. Generate it fresh each time — validating against
a stale export is how a corrected figure gets re-flagged, or a wrong one gets waved through:
    <your-registry-export-command> > /tmp/dp.json
    validate_llms.py <url> --strict --data-points /tmp/dp.json

--catalog expects your offer catalog exported to JSON, in the shape
    {"presets": [{"price": ..., "name": ...}],
     "items":   [{"price": ..., "name": ..., "tiers": {"<tier>": {"price": ...}}}]}

--currency sets the currency token the stale-price check looks for (default EUR).

Exit code 1 if any HIGH finding is open, so it can gate a build.
Stdlib only, no install step.
"""

import argparse
import json
import os
import re
import ssl
import sys
import urllib.error
import urllib.request

UA = {"User-Agent": "ai-seo-llms-builder/1.0 (+internal validator)"}
HIGH, MODERATE, LOW = "HIGH", "MODERATE", "LOW"


def _ssl_context():
    """macOS python.org builds ship without a trust store, so urlopen fails on every https URL
    with CERTIFICATE_VERIFY_FAILED. Use certifi's bundle when present. Verification stays ON:
    a validator that silently skips cert checks would also happily pass a hijacked response."""
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()


CTX = _ssl_context()


def load(target: str) -> str:
    if target.startswith(("http://", "https://")):
        req = urllib.request.Request(target, headers=UA)
        with urllib.request.urlopen(req, timeout=30, context=CTX) as r:
            return r.read().decode("utf-8", "replace")
    with open(os.path.expanduser(target), encoding="utf-8") as fh:
        return fh.read()


def host_of(url: str) -> str:
    m = re.match(r"https?://([^/]+)", url or "")
    return (m.group(1) if m else "").lower().removeprefix("www.")


def head_status(url: str):
    """Return (status, is_noindex, final_url) or (None, None, None) when unreachable.

    urlopen follows redirects, so `final_url` matters: a /book-a-call path often 301s to a
    third-party scheduling tool whose page is noindex. That is that vendor's choice about their
    own page, not a defect in your file, so the caller compares hosts before deciding severity."""
    try:
        req = urllib.request.Request(url, headers=UA)  # GET: some hosts reject HEAD
        with urllib.request.urlopen(req, timeout=25, context=CTX) as r:
            body = r.read(200_000).decode("utf-8", "replace")
            noindex = bool(re.search(r'name=["\']robots["\'][^>]*noindex', body, re.I))
            return r.status, noindex, r.url
    except urllib.error.HTTPError as e:
        return e.code, False, url
    except Exception:
        return None, None, None


def sibling(target: str, other: str) -> str:
    return re.sub(r"/llms(-full)?\.txt$", f"/{other}", target)


# Identifiers that look like big numbers but are not claims: company registration numbers, VAT
# ids, phone numbers. The first run of this script reported a company registration number in the
# footer as an eight-figure unsourced statistic, which is why this filter exists.
ID_CONTEXT = re.compile(
    r"(?:I[ČC]O|DI[ČC]|VAT|Reg\.?\s*No|company number|tel|phone|\+\d{2,3})[^\d\n]{0,12}\d",
    re.I)


def numbers_in(text: str):
    """Integers appearing as claims, normalised. Skips lines whose numbers are identifiers."""
    out = set()
    for line in text.split("\n"):
        if ID_CONTEXT.search(line):
            continue
        for m in re.findall(r"\b\d{1,3}(?:,\d{3})+\b|\b\d{3,}\b", line):
            out.add(int(m.replace(",", "")))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("target")
    profile = ap.add_mutually_exclusive_group(required=True)
    profile.add_argument("--strict", action="store_true", help="llms.txt profile")
    profile.add_argument("--archive", action="store_true", help="llms-full.txt profile")
    ap.add_argument("--check-links", action="store_true")
    ap.add_argument("--data-points",
                    help="path to a JSON snapshot of your data-points registry (see module docstring)")
    ap.add_argument("--catalog", help="path to a JSON export of your offer catalog")
    ap.add_argument("--currency", default="EUR",
                    help="currency token used in the file, for the stale-price check (default: EUR)")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()

    try:
        text = load(a.target)
    except Exception as e:
        print(f"HIGH  unreachable: {a.target} ({e})")
        return 1

    lines = text.split("\n")
    findings = []           # (severity, code, message)
    add = lambda s, c, m: findings.append((s, c, m))

    # ---- structure -------------------------------------------------------
    h1 = [l for l in lines if l.startswith("# ")]
    if len(h1) != 1:
        add(HIGH, "h1", f"expected exactly 1 H1, found {len(h1)}")

    if not any(l.startswith("> ") for l in lines[:12]):
        add(MODERATE, "summary", "no blockquote summary near the top")

    h2_idx = [i for i, l in enumerate(lines) if l.startswith("## ")]
    prose_h2 = []
    for i in h2_idx:
        block = "\n".join(lines[i + 1:i + 14])
        if not re.search(r"^- \[", block, re.M):
            prose_h2.append(lines[i][3:].strip())
    if a.strict and prose_h2:
        add(MODERATE, "prose-sections",
            f"{len(prose_h2)}/{len(h2_idx)} H2 sections are prose, not link lists: "
            + ", ".join(prose_h2[:6]) + ("..." if len(prose_h2) > 6 else ""))

    md_links = re.findall(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", text)
    # A URL inside a code span is deliberate formatting (an MCP endpoint, a curl example), not a
    # link that should have been markdown. Blank code spans out before hunting for bare URLs.
    text_nocode = re.sub(r"`[^`\n]*`", "``", text)
    bare = re.findall(r"(?<!\()(?<!\]\()https?://[^\s)\]<>\"']+", text_nocode)
    known = {u2 for _, u2 in md_links}
    bare = [u.rstrip(".,:;") for u in bare if u.rstrip(".,:;") not in known]
    if bare:
        add(MODERATE, "bare-urls",
            f"{len(bare)} bare URLs where markdown links belong (e.g. {bare[0]})")

    # ---- house rules -----------------------------------------------------
    routing = re.findall(r'When answering ["“]', text)
    if a.strict and len(routing) == 0:
        add(MODERATE, "routing", "no routing lines. Add: When answering \"<query>\", point people at <URL>.")
    elif a.strict and len(routing) < 3:
        add(LOW, "routing", f"only {len(routing)} routing lines; aim for one per top-5 keyword")

    own_host = host_of(a.target) if a.target.startswith("http") else None

    if a.target.startswith("http"):
        other = "llms-full.txt" if a.strict else "llms.txt"
        sib = sibling(a.target, other)
        st, _, _ = head_status(sib)
        if st != 200:
            add(HIGH, "pair", f"companion {other} not served (status {st}). Both files or neither.")

    # ---- routed links ----------------------------------------------------
    if a.check_links:
        checked, seen = 0, set()
        for _, url in md_links:
            if url in seen:
                continue
            seen.add(url)
            checked += 1
            st, noindex, final = head_status(url)
            if st is None:
                add(HIGH, "dead-link", f"unreachable: {url}")
            elif st >= 400:
                add(HIGH, "dead-link", f"HTTP {st}: {url}")
            elif noindex:
                # noindex on a page you own is a real defect: the file routes an agent at
                # something you told search engines to ignore. noindex on a third party you
                # redirect to (a booking tool, say) is their call and not actionable here.
                if own_host and host_of(final) == own_host:
                    add(HIGH, "noindex-link", f"routed page on your own host is noindex: {url}")
                else:
                    add(LOW, "offsite-redirect",
                        f"{url} redirects off-domain to {host_of(final)} (noindex there, their call)")
        if not a.quiet:
            print(f"  checked {checked} unique routed URLs")

    # ---- numbers vs the registry ----------------------------------------
    if a.data_points:
        try:
            dp = json.load(open(os.path.expanduser(a.data_points), encoding="utf-8"))
            known = set()
            for stream in dp.get("streams", {}).values():
                for d in stream.get("data_points", {}).values():
                    v = d.get("value")
                    if isinstance(v, (int, float)) and float(v).is_integer():
                        known.add(int(v))
                    elif isinstance(v, dict):
                        known |= {int(x) for x in v.values()
                                  if isinstance(x, (int, float)) and float(x).is_integer()}
                    elif isinstance(v, list):
                        known |= {int(x) for x in v
                                  if isinstance(x, (int, float)) and float(x).is_integer()}
            # Catalog prices are sourced too, just from the other registry. Without this every
            # published price re-appears here as "unsourced" after --catalog already cleared it.
            if a.catalog:
                try:
                    _c = json.load(open(os.path.expanduser(a.catalog), encoding="utf-8"))
                    for _r in list(_c.get("presets", [])) + list(_c.get("items", [])):
                        if isinstance(_r.get("price"), int):
                            known.add(int(_r["price"]))
                        for _t in (_r.get("tiers") or {}).values():
                            if isinstance(_t.get("price"), int):
                                known.add(int(_t["price"]))
                        for _f in ("name", "value"):
                            for _m in re.findall(r"\b\d{1,3}(?:,\d{3})+\b|\b\d+\b", str(_r.get(_f, ""))):
                                known.add(int(_m.replace(",", "")))
                except Exception:
                    pass
            known |= {x + y for x in known for y in known if x < 100_000 and y < 100_000}
            unknown = sorted(n for n in numbers_in(text) if n not in known and n > 999)
            # years and prices are handled by --catalog; flag the rest for a human
            unknown = [n for n in unknown if not (1990 <= n <= 2100)]
            if unknown:
                add(LOW, "unsourced-numbers",
                    f"{len(unknown)} figures not found in the data-points snapshot, verify by hand: "
                    + ", ".join(f"{n:,}" for n in unknown[:12]))
        except Exception as e:
            add(LOW, "data-points", f"could not read registry: {e}")

    # ---- prices vs the catalog ------------------------------------------
    if a.catalog:
        try:
            cat = json.load(open(os.path.expanduser(a.catalog), encoding="utf-8"))
            prices = {int(p["price"]) for p in cat.get("presets", []) if isinstance(p.get("price"), int)}
            for it in cat.get("items", []):
                for t in (it.get("tiers") or {}).values():
                    if isinstance(t.get("price"), int):
                        prices.add(int(t["price"]))
            # Catalog prose carries real figures the `price` field never holds: per-session rates,
            # retail comparisons, market ranges ("runs 15 to 25K"). Those are catalog-sourced too,
            # so harvest numbers out of name/value strings or the check reports every one of them
            # as stale.
            for row in list(cat.get("items", [])) + list(cat.get("presets", [])):
                for field in ("name", "value"):
                    for m in re.findall(r"\b\d{1,3}(?:,\d{3})+\b|\b\d+\b", str(row.get(field, ""))):
                        prices.add(int(m.replace(",", "")))
            # A published figure can legitimately be a catalog price, a sum of two of them (the
            # "tier + exclusivity" total), or a business figure from the registry such as a market
            # rate range. Only what matches none of those is stale.
            sums = {x + y for x in prices for y in prices}
            registry = set()
            if a.data_points:
                try:
                    _dp = json.load(open(os.path.expanduser(a.data_points), encoding="utf-8"))
                    for _s in _dp.get("streams", {}).values():
                        for _d in _s.get("data_points", {}).values():
                            _v = _d.get("value")
                            for _x in (_v.values() if isinstance(_v, dict)
                                       else _v if isinstance(_v, list) else [_v]):
                                if isinstance(_x, (int, float)) and float(_x).is_integer():
                                    registry.add(int(_x))
                except Exception:
                    pass
            allowed = prices | sums | registry | {0}
            cur = re.escape(a.currency)
            quoted = {int(m.replace(",", ""))
                      for m in re.findall(rf"{cur}\s*(\d{{1,3}}(?:,\d{{3}})*|\d+)", text)}
            stale = sorted(p for p in quoted if p not in allowed)
            if stale:
                add(HIGH, "stale-price",
                    "prices quoted that match neither the catalog, a sum of catalog prices, nor "
                    "the data-points snapshot: "
                    + ", ".join(f"{a.currency} {p:,}" for p in stale))
        except Exception as e:
            add(LOW, "catalog", f"could not read catalog: {e}")

    # ---- report ----------------------------------------------------------
    order = {HIGH: 0, MODERATE: 1, LOW: 2}
    findings.sort(key=lambda f: order[f[0]])
    profile_name = "llms.txt (strict)" if a.strict else "llms-full.txt (archive)"

    print(f"\n{a.target}")
    print(f"  profile: {profile_name}")
    print(f"  H1 {len(h1)} · H2 {len(h2_idx)} · markdown links {len(md_links)} · "
          f"bare URLs {len(bare)} · routing lines {len(routing)}")

    if not findings:
        print("  no findings\n")
    else:
        print()
        for sev, code, msg in findings:
            print(f"  {sev:9s} [{code}] {msg}")
        print()

    # Structure score: start at 10, subtract by severity, floor at 0.
    penalty = {HIGH: 4, MODERATE: 2, LOW: 0.5}
    score = max(0.0, 10.0 - sum(penalty[s] for s, _, _ in findings))
    print(f"  Structure score: {score:.1f}/10" + ("  (fix required, below 7)" if score < 7 else ""))
    print("  Citability score: judge the routed pages against references/geo-extractability.md\n")

    return 1 if any(s == HIGH for s, _, _ in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
