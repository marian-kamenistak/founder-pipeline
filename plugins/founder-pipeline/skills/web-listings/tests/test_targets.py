#!/usr/bin/env python3
"""Invariants for web-listings/config/targets.json and the NAP audit. No network.

  python3 ${CLAUDE_PLUGIN_ROOT}/skills/web-listings/tests/test_targets.py

Design note: `local_tier` is ADDITIVE and does not change a row's `category`.
`category` drives Phase 2 selection, so retagging twenty existing rows to a new
"local" class would silently change which targets get selected for every property.
"Is this a local citation surface?" is therefore `local_tier is not None`, and a row
can be both `catalog` and tier 2.
"""

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGETS = json.load(open(os.path.join(ROOT, "config", "targets.json"),
                        encoding="utf-8"))["targets"]

VALID_TIERS = {1, 2, 3, 4, 5, 6}


def test_ids_are_unique():
    ids = [t["id"] for t in TARGETS]
    assert len(ids) == len(set(ids)), "duplicate target ids"


def test_local_tier_values_are_valid():
    for t in TARGETS:
        if "local_tier" in t:
            assert t["local_tier"] in VALID_TIERS, f"{t['id']} has local_tier {t['local_tier']!r}"


def test_tier1_local_targets_are_worldwide():
    """Tier 1 is core-universal by definition — a country-scoped tier 1 is a mistag."""
    for t in TARGETS:
        if t.get("local_tier") == 1:
            assert t.get("territory") == "worldwide", \
                f"{t['id']} is tier 1 but scoped to {t.get('territory')}"


def test_country_general_directories_are_tier2():
    """Tier 2 is 'country-specific general directory'. A worldwide tier 2 is a mistag."""
    for t in TARGETS:
        if t.get("local_tier") == 2:
            assert t.get("territory") != "worldwide", \
                f"{t['id']} is tier 2 but scoped worldwide"


def test_local_targets_exist_for_the_portfolio_territories():
    terr = {t.get("territory") for t in TARGETS if t.get("local_tier")}
    for expected in ("cz", "sk", "pl"):
        assert expected in terr, f"no local-tier targets for {expected}"


def test_google_business_profile_is_tier1_and_carries_its_eligibility_block():
    """GBP is the highest-value local target and the one that can get a business
    suspended. A row that doesn't state the gate invites someone to just submit it."""
    gbp = [t for t in TARGETS if "google business profile" in t["name"].lower()]
    assert gbp, "no Google Business Profile row"
    assert gbp[0].get("local_tier") == 1
    notes = (gbp[0].get("notes") or "").lower()
    assert "eligib" in notes, "GBP row does not mention the eligibility gate"


def test_no_target_duplicates_a_canonical_nap_value():
    """NAP lives in entity-pack.md and nowhere else. A canonical value copied into
    this file is a second source of truth waiting to drift.

    Checks canonical values specifically, not any phone-shaped string: several rows
    legitimately record the TARGET's own sales line in their notes, which is vendor
    contact detail, not the owner's NAP.
    """
    STRUCTURED = ("name", "url", "submit_url", "territory", "category")
    packs = na.load_packs()
    leaked = []
    for entity, fields in packs.items():
        for field, value in fields.items():
            if field == "website" or not value or len(value) <= 8:
                continue  # a row may legitimately cite the property URL
            for t in TARGETS:
                for key in STRUCTURED:
                    if value in str(t.get(key) or ""):
                        leaked.append(f"{entity}.{field} in {t['id']}.{key}")
    assert not leaked, "canonical NAP values duplicated into targets.json: " + "; ".join(leaked)
    # `notes` is deliberately excluded: a row may name an entity inside a sentence
    # explaining who qualifies for membership. That is commentary, not a NAP field.


def test_entity_pack_defines_the_fields_the_audit_needs_to_run():
    """nap_audit cannot diff a field the canonical source never defines.

    name + address are required — without them there is nothing to compare. phone and
    website are NOT asserted here because entity-pack.md genuinely defines neither in
    a per-entity form today; `nap_audit --list` prints that gap explicitly rather than
    letting Law 6 look fully enforced when it is not.
    """
    packs = na.load_packs()
    defined = {f for v in packs.values() for f in v}
    for required in ("name", "address"):
        assert required in defined, f"entity-pack.md defines no canonical {required}"


# ---------- nap_audit ----------

sys.path.insert(0, os.path.join(ROOT, "scripts"))
import nap_audit as na  # noqa: E402


def test_normalise_phone_strips_formatting():
    assert na.normalise_phone("+420 000 000 000") == "+420000000000"
    assert na.normalise_phone("00420-000-000-000") == "00420000000000"


def test_normalise_name_is_case_and_space_insensitive():
    assert na.normalise_name("  Acme   Holdings ") == na.normalise_name("acme holdings")


def test_normalise_name_folds_diacritics():
    """A name written with diacritics on one listing and without them on another must
    compare equal, or every local listing reads as drift."""
    assert na.normalise_name("Nováková") == na.normalise_name("Novakova")


def test_diff_nap_reports_exact_match():
    canon = {"name": "Acme Holdings", "phone": "+420 000 000 000",
             "website": "https://example.com"}
    found = {"name": "acme holdings", "phone": "+420000000000",
             "website": "https://example.com"}
    out = {d["field"]: d["status"] for d in na.diff_nap(canon, found)}
    assert set(out.values()) == {"exact"}, out


def test_diff_nap_reports_drift_not_missing_when_a_value_differs():
    canon = {"name": "Acme Holdings", "phone": "+420 000 000 000"}
    found = {"name": "Acme Holdings s.r.o.", "phone": "+420 000 000 000"}
    out = {d["field"]: d["status"] for d in na.diff_nap(canon, found)}
    assert out["name"] == "drift"
    assert out["phone"] == "exact"


def test_diff_nap_reports_missing_when_a_field_is_absent():
    canon = {"name": "Acme Holdings", "phone": "+420 000 000 000"}
    out = {d["field"]: d["status"] for d in na.diff_nap(canon, {"name": "Acme Holdings"})}
    assert out["phone"] == "missing"


def test_parse_entity_pack_reads_a_property_block():
    md = """
## coach.example.com

- Name: Acme Holdings
- Phone: +420 000 000 000
- Website: https://coach.example.com

## community.example.com

- Name: Acme Collective
- Website: https://community.example.com
"""
    packs = na.parse_entity_pack(md)
    assert packs["coach.example.com"]["phone"] == "+420 000 000 000"
    assert packs["community.example.com"]["name"] == "Acme Collective"
    assert "phone" not in packs["community.example.com"]


def test_parse_entity_pack_trims_inline_commentary_from_a_value():
    """entity-pack.md annotates values with an em-dash aside. Without trimming, a
    phone number comes back as the number plus three sentences of caveat and every
    comparison against it fails."""
    md = ("## x\n\n- Phone: +420 000 000 000 — UNCONFIRMED, sourced from the live site.\n"
          "- Name: Acme Holdings s.r.o.\n")
    packs = na.parse_entity_pack(md)
    assert packs["x"]["phone"] == "+420 000 000 000"
    assert packs["x"]["name"] == "Acme Holdings s.r.o."


def test_parse_entity_pack_drops_an_aside_left_open_by_the_dash_cut():
    """A renamed company is the common case that breaks the em-dash cut: it leaves the
    parenthetical open, so the canonical name came back as
    'Acme Holdings s.r.o. (renamed from "Old Name, s.r.o."'."""
    md = ('## x\n\n- Legal name: Acme Holdings s.r.o. (renamed from '
          '"Old Name, s.r.o." — same registration number, some catalogs still show the old name)\n')
    assert na.parse_entity_pack(md)["x"]["name"] == "Acme Holdings s.r.o."


def test_parse_entity_pack_treats_placeholders_as_absent():
    """'not defined' is a note to a human, not a value to diff a listing against."""
    md = "## x\n\n- Phone: not defined — see the completeness note\n- Name: Acme s.r.o.\n"
    packs = na.parse_entity_pack(md)
    assert "phone" not in packs["x"]
    assert packs["x"]["name"] == "Acme s.r.o."


def test_parse_entity_pack_reads_a_markdown_table_block():
    """entity-pack.md may use a table rather than a bullet list. Adapt the parser to
    the file — the file is the source of truth and other work depends on its shape."""
    md = """
## coach.example.com

| Field | Value |
|---|---|
| Name | Acme Holdings |
| Phone | +420 000 000 000 |
"""
    packs = na.parse_entity_pack(md)
    assert packs["coach.example.com"]["name"] == "Acme Holdings"
    assert packs["coach.example.com"]["phone"] == "+420 000 000 000"


if __name__ == "__main__":
    fns = [(n, f) for n, f in sorted(globals().items())
           if n.startswith("test_") and callable(f)]
    failed = 0
    for name, fn in fns:
        try:
            fn()
            print(f"  ok   {name}")
        except Exception as e:
            failed += 1
            print(f"  FAIL {name}: {type(e).__name__}: {e}")
    print(f"\n{len(fns) - failed}/{len(fns)} passed")
    sys.exit(1 if failed else 0)
