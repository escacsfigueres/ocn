#!/usr/bin/env python3
"""Scaffold an ocn.attribution_manifest.v1 SKELETON from reviewed slugs.

Produces a structurally valid manifest whose field values are EMPTY strings — so
`tools/apply_attribution_manifest.py` accepts it structurally but rejects it in
dry-run as a no-op ("expected to change but did not") until a human fills real
values. This makes "fill before apply" an enforced contract, not a convention.

It never invents field values, and refuses by default to scaffold an
already-attributed slug (whose empty-field skeleton would CLEAR the attribution
on apply) — pass --allow-attributed to override with a loud warning.

Usage:
    python3 tools/scaffold_attribution_manifest.py --title "..." \\
        --mode attribution_fields_only|naming_strings_only \\
        (--ocn1 SLUG ... | --ocn1-file FILE) [--evidence-grade CLEAR|PARTIAL|INSUFFICIENT] \\
        [--source-ref TEXT ...] [--catalog catalog/ocn-1.csv] [--out manifest.json]
        [--allow-attributed]

Exit codes: 0 success, 1 data error (missing/duplicate slug, already-attributed
without override), 2 usage error.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

DEFAULT_CATALOG = Path(__file__).resolve().parent.parent / "catalog" / "ocn-1.csv"
MANIFEST_KIND = "ocn.attribution_manifest.v1"
SKELETON_DESCRIPTION = (
    "NOT-APPLY-READY skeleton from scaffold_attribution_manifest.py: fill every "
    "field value (and, under --strict, set evidence_grade=CLEAR + source_refs) "
    "before --apply. The apply engine rejects the unfilled skeleton as a no-op."
)
# Ordered field skeletons per mode (frozenset iteration order is undefined).
FIELDS_ORDER = {
    "attribution_fields_only": ["attributed_to", "attribution_source", "historical_notes"],
    "naming_strings_only": ["canonical_name", "aliases", "notes",
                            "attributed_to", "attribution_source", "historical_notes"],
}


def fail(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def warn(msg: str) -> None:
    print(f"WARN:  {msg}", file=sys.stderr)


def read_slug_file(path: Path) -> list[str]:
    if not path.exists():
        fail(f"--ocn1-file not found: {path}")
    return [ln.strip() for ln in path.read_text(encoding="utf-8").splitlines()
            if ln.strip() and not ln.strip().startswith("#")]


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Scaffold an attribution manifest skeleton.")
    p.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    p.add_argument("--title", required=True)
    p.add_argument("--mode", required=True, choices=tuple(FIELDS_ORDER))
    p.add_argument("--ocn1", action="append", default=[], metavar="SLUG")
    p.add_argument("--ocn1-file", type=Path, default=None)
    p.add_argument("--evidence-grade", choices=("CLEAR", "PARTIAL", "INSUFFICIENT"),
                   default="CLEAR")
    p.add_argument("--source-ref", action="append", default=[], metavar="TEXT")
    p.add_argument("--out", type=Path, default=None)
    p.add_argument("--allow-attributed", action="store_true",
                   help="Scaffold even already-attributed slugs (warns; risks clearing).")
    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(sys.argv[1:] if argv is None else argv)

    slugs: list[str] = list(args.ocn1)
    if args.ocn1_file:
        slugs += read_slug_file(args.ocn1_file)
    if not slugs:
        parser.error("at least one --ocn1 or a non-empty --ocn1-file is required")

    dupes = sorted({s for s in slugs if slugs.count(s) > 1})
    if dupes:
        fail(f"duplicate slug(s) in input: {', '.join(dupes)}")

    if not args.catalog.exists():
        fail(f"catalogue not found: {args.catalog}")
    with args.catalog.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    index = {r["ocn1"]: i for i, r in enumerate(rows)}

    missing = [s for s in slugs if s not in index]
    if missing:
        fail(f"slug not in catalogue: {missing[0]}")

    attributed = [s for s in slugs
                  if (rows[index[s]].get("attributed_to") or "").strip()
                  or (rows[index[s]].get("attribution_source") or "").strip()]
    if attributed:
        if args.allow_attributed:
            for s in attributed:
                warn(f"slug {s} is already attributed; an empty-field skeleton would "
                     f"CLEAR it on apply — fill deliberately")
        else:
            fail(f"slug already attributed (use --allow-attributed to override): "
                 f"{', '.join(attributed)}")

    ordered = sorted(set(slugs), key=lambda s: index[s])  # catalogue order
    fields_keys = FIELDS_ORDER[args.mode]
    changes = [{
        "ocn1": slug,
        "evidence_grade": args.evidence_grade,
        "source_refs": list(args.source_ref),
        "fields": {k: "" for k in fields_keys},
    } for slug in ordered]

    manifest = {
        "kind": MANIFEST_KIND,
        "title": args.title,
        "description": SKELETON_DESCRIPTION,
        "mode": args.mode,
        "expected_catalog_rows": len(rows),
        "expected_changed_rows": ordered,
        "changes": changes,
    }

    text = json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
