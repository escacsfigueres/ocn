#!/usr/bin/env python3
"""Generate the Tier 1 diacritic-normalization manifest.

Turns the Tier 1 map of `docs/diacritic-normalization-map.md` into an
`ocn.attribution_manifest.v1` JSON in `naming_strings_only` mode, ready for
`tools/apply_attribution_manifest.py`. The replacement is word-boundary per
ASCII variant across the six naming columns; rows without a hit are not
mentioned in the manifest at all, so the engine's exact-change and
zero-collateral guardrails do the final policing.

The map constants here MIRROR the spec doc — the doc is the human source of
truth, `test_generate_diacritic_manifest.py` pins the two together. When the
lot is applied, `validate.py`'s `BANNED_ASCII_NAME_FORMS` is populated from
the same pairs so the guard activates atomically with the data.

Usage:
    python3 tools/generate_diacritic_manifest.py [--catalog catalog/ocn-1.csv]
        --out docs/manifests/diacritic-tier1-normalization.manifest.json
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

DEFAULT_CATALOG = Path(__file__).resolve().parent.parent / "catalog" / "ocn-1.csv"
MAP_DOC = "docs/diacritic-normalization-map.md"

# Tier 1: normalized form -> ASCII variants found in the catalogue.
TIER1_FORMS: dict[str, tuple[str, ...]] = {
    "López": ("Lopez",),
    "Grünfeld": ("Grunfeld", "Gruenfeld"),
    "Réti": ("Reti",),
    "Sämisch": ("Saemisch", "Samisch"),
    "Maróczy": ("Maroczy",),
    "Göring": ("Goring", "Goering"),
    "Hübner": ("Hubner", "Huebner"),
    "Löwenthal": ("Lowenthal", "Loewenthal"),
    "Hromádka": ("Hromadka",),
    "Møller": ("Moller", "Moeller"),
}

# The person each normalized surname refers to (evidence column of the map).
TIER1_PERSONS: dict[str, str] = {
    "López": "Ruy López de Segura",
    "Grünfeld": "Ernst Grünfeld",
    "Réti": "Richard Réti",
    "Sämisch": "Friedrich Sämisch",
    "Maróczy": "Géza Maróczy",
    "Göring": "Carl Theodor Göring",
    "Hübner": "Robert Hübner",
    "Löwenthal": "Johann Löwenthal",
    "Hromádka": "Karel Hromádka",
    "Møller": "Jørgen Møller",
}

# Tier 2: the Czech/Lithuanian class, GO-normalized 2026-06-11 (map doc,
# "Tier 2 — parked, one batched decision"). Sørensen and Würzburger remain
# parked pending per-row referent evidence and must NOT be added here.
TIER2_FORMS: dict[str, tuple[str, ...]] = {
    "Mikėnas": ("Mikenas",),
    "Krejčík": ("Krejcik",),
    "Opočenský": ("Opocensky",),
    "Pelikán": ("Pelikan",),
}

TIER2_PERSONS: dict[str, str] = {
    "Mikėnas": "Vladas Mikėnas",
    "Krejčík": "Josef Krejčík",
    "Opočenský": "Karel Opočenský",
    "Pelikán": "Jiří Pelikán",
}

# Tier 3: divergences surfaced by the Lichess xref triage (2026-06-11) —
# rows whose position-anchored Lichess label restores a diacritic the
# OCN text dropped. Sørensen stays parked (per-row referents; Lichess
# itself splits ö/ø by line) and must NOT be added here.
TIER3_FORMS: dict[str, tuple[str, ...]] = {
    "Kádas": ("Kadas",),
    "Bücker": ("Bucker",),
    "Kostić": ("Kostic",),
    "Szén": ("Szen",),
    "Süchting": ("Suchting",),
    "Hübsch": ("Hubsch",),
    "Döry": ("Dory",),
    "Löhn": ("Lohn",),
    "Schönemann": ("Schonemann",),
    "Düsseldorf": ("Dusseldorf",),
    "Tübingen": ("Tubingen",),
}

TIER3_PERSONS: dict[str, str] = {
    "Kádas": "Gábor Kádas",
    "Bücker": "Stefan Bücker",
    "Kostić": "Borislav Kostić",
    "Szén": "József Szén",
    "Süchting": "Hugo Süchting",
    "Hübsch": "Hübsch (Hübsch Gambit; Lichess + German orthography)",
    "Döry": "Ladislaus Döry",
    "Löhn": "Löhn (Lichess + German orthography; no encyclopedia entry found)",
    "Schönemann": "Schönemann (Lichess + German orthography; no encyclopedia entry found)",
    "Düsseldorf": "Düsseldorf (place name)",
    "Tübingen": "Tübingen (place name)",
}

TIER_SPECS: dict[int, tuple[dict[str, tuple[str, ...]], dict[str, str], str]] = {
    1: (TIER1_FORMS, TIER1_PERSONS, "Tier 1 (10 surnames)"),
    2: (TIER2_FORMS, TIER2_PERSONS, "Tier 2 (Czech/Lithuanian class)"),
    3: (TIER3_FORMS, TIER3_PERSONS, "Tier 3 (Lichess xref discoveries)"),
}

# Columns the manifest may rewrite (the naming_strings_only field scope).
NAMING_COLUMNS = (
    "canonical_name",
    "aliases",
    "notes",
    "attributed_to",
    "attribution_source",
    "historical_notes",
)

def _variant_res(
    forms: dict[str, tuple[str, ...]],
) -> dict[str, re.Pattern[str]]:
    return {
        target: re.compile(r"\b(" + "|".join(map(re.escape, variants)) + r")\b")
        for target, variants in forms.items()
    }


def normalize_text(
    value: str, forms: dict[str, tuple[str, ...]] | None = None
) -> tuple[str, set[str]]:
    """Replace every ASCII variant of `forms` (default Tier 1) in `value`,
    word-boundary.

    Returns the new text and the set of normalized targets that matched.
    """
    matched: set[str] = set()
    for target, pattern in _variant_res(forms or TIER1_FORMS).items():
        value, n = pattern.subn(target, value)
        if n:
            matched.add(target)
    return value, matched


def build_changes(rows: list[dict[str, str]], tier: int = 1) -> list[dict]:
    forms, persons, label = TIER_SPECS[tier]
    changes: list[dict] = []
    for row in rows:
        fields: dict[str, str] = {}
        row_targets: set[str] = set()
        for col in NAMING_COLUMNS:
            old = row.get(col) or ""
            new, targets = normalize_text(old, forms)
            if new != old:
                fields[col] = new
                row_targets |= targets
        if not fields:
            continue
        refs = [f"{MAP_DOC} — {label}, survey 2026-06-11"]
        refs.extend(f"Wikipedia: {persons[t]}" for t in sorted(row_targets))
        changes.append(
            {
                "ocn1": row["ocn1"],
                "evidence_grade": "CLEAR",
                "source_refs": refs,
                "fields": fields,
            }
        )
    return changes


def build_manifest(rows: list[dict[str, str]], tier: int = 1) -> dict:
    _, _, label = TIER_SPECS[tier]
    changes = build_changes(rows, tier)
    return {
        "kind": "ocn.attribution_manifest.v1",
        "title": f"Diacritic normalization — {label}",
        "description": (
            "Audit P1 item 7, generated by tools/generate_diacritic_manifest.py "
            f"from the {label} map in {MAP_DOC}. Word-boundary respelling of "
            "eponym surnames to the person's orthography across the naming "
            "columns; no alias additions, no structural changes."
        ),
        "mode": "naming_strings_only",
        "expected_catalog_rows": len(rows),
        "expected_changed_rows": sorted(c["ocn1"] for c in changes),
        "changes": changes,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate the Tier 1 diacritic-normalization manifest."
    )
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    parser.add_argument("--out", type=Path, required=True,
                        help="Path for the manifest JSON.")
    parser.add_argument("--tier", type=int, choices=sorted(TIER_SPECS),
                        default=1, help="Which map tier to generate (default 1).")
    args = parser.parse_args()

    with args.catalog.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    manifest = build_manifest(rows, tier=args.tier)
    args.out.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    changed = manifest["expected_changed_rows"]
    canonical = sum(
        1 for c in manifest["changes"] if "canonical_name" in c["fields"]
    )
    print(f"manifest: {args.out}")
    print(f"rows changed: {len(changed)} (canonical_name: {canonical})")
    per_target: dict[str, int] = {}
    for c in manifest["changes"]:
        for ref in c["source_refs"][1:]:
            per_target[ref] = per_target.get(ref, 0) + 1
    for ref, n in sorted(per_target.items(), key=lambda kv: -kv[1]):
        print(f"  {n:4d}  {ref.removeprefix('Wikipedia: ')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
