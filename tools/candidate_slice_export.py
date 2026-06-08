#!/usr/bin/env python3
"""Export a review slice of the OCN-1 catalogue for an attribution sprint.

Select rows by explicit slug (`--ocn1` / `--ocn1-file`) and/or by filter
(`--eco-prefix`, `--empty-attribution`), and emit the review-relevant columns in
deterministic catalogue order. This feeds the factory loop: a human reviews the
slice, fills in sources, and the result is scaffolded into a manifest.

Selection model: the base set is the explicit slugs (or ALL rows if none given);
`--eco-prefix` and `--empty-attribution` then narrow it (logical AND).

Usage:
    python3 tools/candidate_slice_export.py [--catalog catalog/ocn-1.csv]
        [--ocn1 SLUG ...] [--ocn1-file FILE] [--eco-prefix A|B|C|D|E]
        [--empty-attribution] [--columns C1,C2,...] [--format csv|json]
        [--out FILE] [--allow-missing]

Exit codes: 0 success (an empty slice is success), 1 data error (missing slug
without --allow-missing, unreadable catalogue/slug file), 2 usage error.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

try:
    from validate import REQUIRED_COLUMNS
except ImportError:  # pragma: no cover
    from tools.validate import REQUIRED_COLUMNS

DEFAULT_CATALOG = Path(__file__).resolve().parent.parent / "catalog" / "ocn-1.csv"
DEFAULT_COLUMNS = (
    "ocn1,canonical_name,aliases,notes,attributed_to,"
    "attribution_source,historical_notes,moves_uci,parent_ocn1"
)


def fail(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def warn(msg: str) -> None:
    print(f"WARN:  {msg}", file=sys.stderr)


def read_slug_file(path: Path) -> list[str]:
    if not path.exists():
        fail(f"--ocn1-file not found: {path}")
    slugs = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            slugs.append(line)
    return slugs


def load_rows(catalog: Path) -> list[dict]:
    if not catalog.exists():
        fail(f"catalogue not found: {catalog}")
    with catalog.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Export a catalogue review slice.")
    p.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    p.add_argument("--ocn1", action="append", default=[], metavar="SLUG")
    p.add_argument("--ocn1-file", type=Path, default=None)
    p.add_argument("--eco-prefix", choices=("A", "B", "C", "D", "E"), default=None)
    p.add_argument("--empty-attribution", action="store_true")
    p.add_argument("--columns", default=DEFAULT_COLUMNS)
    p.add_argument("--format", choices=("csv", "json"), default="csv")
    p.add_argument("--out", type=Path, default=None)
    p.add_argument("--allow-missing", action="store_true")
    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(sys.argv[1:] if argv is None else argv)

    columns = [c.strip() for c in args.columns.split(",") if c.strip()]
    unknown = [c for c in columns if c not in REQUIRED_COLUMNS]
    if unknown:
        parser.error(f"unknown column(s): {', '.join(unknown)}")

    rows = load_rows(args.catalog)
    by_slug = {r["ocn1"]: r for r in rows}

    explicit: list[str] = list(args.ocn1)
    if args.ocn1_file:
        explicit += read_slug_file(args.ocn1_file)

    if explicit:
        missing = [s for s in dict.fromkeys(explicit) if s not in by_slug]
        if missing:
            if args.allow_missing:
                for s in missing:
                    warn(f"slug not in catalogue, skipped: {s}")
            else:
                fail(f"slug not in catalogue: {missing[0]}")
        base = {s for s in explicit if s in by_slug}
    else:
        base = set(by_slug)

    selected = []
    for row in rows:  # catalogue order, deterministic
        slug = row["ocn1"]
        if slug not in base:
            continue
        if args.eco_prefix and not (slug == args.eco_prefix
                                    or slug.startswith(args.eco_prefix + ".")):
            continue
        if args.empty_attribution and (row.get("attributed_to") or "").strip():
            continue
        selected.append({c: row.get(c, "") for c in columns})

    if args.format == "json":
        text = json.dumps(selected, ensure_ascii=False, indent=2)
        out = text + "\n"
    else:
        import io
        buf = io.StringIO()
        writer = csv.DictWriter(buf, fieldnames=columns, lineterminator="\n")
        writer.writeheader()
        writer.writerows(selected)
        out = buf.getvalue()

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(out, encoding="utf-8")
    else:
        sys.stdout.write(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
