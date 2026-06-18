#!/usr/bin/env python3
"""Per-head attribution source-status table for the OCN-1 catalogue.

Joins, for every attribution-candidate head, the catalogue's AUTHORITATIVE
attribution state with a small human-maintained status registry, so picking
the next evidence sprint target is a query, not a hand-scan of prose docs.

Two authoritative inputs, never guessed:

  * ``catalog/ocn-1.csv`` — a row is ATTRIBUTED iff BOTH ``attributed_to`` and
    ``attribution_source`` are non-empty (the validator enforces
    ``attributed_to => attribution_source``; a half-filled row is UNATTRIBUTED).
  * ``docs/attribution-source-status.tsv`` — a machine-readable registry of the
    evidence grades that currently live in prose docs (CLEAR / PARTIAL / HOLD),
    each row citing the documenting doc (``source_ref``) and the grade note
    (``evidence_note``). A head absent from the registry has grade ``none``
    (untouched) — the tool never invents a grade.

By default the table is the set of *candidate heads*: every registry head plus
every attributed catalogue row (the interesting subset). ``--all`` emits one row
per catalogue row instead.

Usage:
    python3 tools/source_status_table.py
        [--catalog catalog/ocn-1.csv] [--registry docs/attribution-source-status.tsv]
        [--all] [--status CLEAR|PARTIAL|HOLD|none] [--unattributed]
        [--catalog-status ATTRIBUTED|UNATTRIBUTED] [--ocn1 SLUG ...]
        [--format tsv|json|table] [--out FILE]

Exit codes: 0 success, 1 data error (missing catalogue/registry, registry slug
not in catalogue, bad grade, malformed registry), 2 usage error.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CATALOG = REPO_ROOT / "catalog" / "ocn-1.csv"
DEFAULT_REGISTRY = REPO_ROOT / "docs" / "attribution-source-status.tsv"

# Grades documented in the source-log / sweep / factory-map docs. ``none`` is
# the default for any head the registry does not mention (untouched).
DOCUMENTED_GRADES = ("CLEAR", "PARTIAL", "HOLD")
GRADE_NONE = "none"
VALID_GRADES = frozenset(DOCUMENTED_GRADES) | {GRADE_NONE}

REGISTRY_COLUMNS = ("ocn1", "grade", "source_ref", "evidence_note")

OUTPUT_COLUMNS = [
    "ocn1",
    "canonical_name",
    "catalog_status",
    "source_grade",
    "attributed_to",
    "attribution_source",
    "source_ref",
    "evidence_note",
]

STATUS_ATTRIBUTED = "ATTRIBUTED"
STATUS_UNATTRIBUTED = "UNATTRIBUTED"


def fail(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def load_catalog(path: Path) -> list[dict]:
    if not path.exists():
        fail(f"catalogue not found: {path}")
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_registry(path: Path, valid_slugs: set[str]) -> dict[str, dict]:
    """Parse the status registry; validate slugs and grades. Returns by-slug."""
    if not path.exists():
        fail(f"status registry not found: {path}")
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        fields = reader.fieldnames or []
        missing_cols = [c for c in REGISTRY_COLUMNS if c not in fields]
        if missing_cols:
            fail(f"registry missing column(s): {', '.join(missing_cols)}")
        by_slug: dict[str, dict] = {}
        for line_no, raw in enumerate(reader, start=2):
            slug = (raw.get("ocn1") or "").strip()
            if not slug:
                fail(f"registry line {line_no}: empty ocn1")
            if slug in by_slug:
                fail(f"registry: duplicate slug {slug}")
            if slug not in valid_slugs:
                fail(f"registry slug not in catalogue: {slug} (line {line_no})")
            grade = (raw.get("grade") or "").strip()
            if grade not in DOCUMENTED_GRADES:
                fail(f"registry slug {slug}: invalid grade {grade!r} "
                     f"(expected one of {', '.join(DOCUMENTED_GRADES)})")
            by_slug[slug] = {
                "grade": grade,
                "source_ref": (raw.get("source_ref") or "").strip(),
                "evidence_note": (raw.get("evidence_note") or "").strip(),
            }
        return by_slug


def catalog_status(row: dict) -> str:
    """ATTRIBUTED iff both attribution fields are non-empty (validator rule)."""
    attributed = (row.get("attributed_to") or "").strip()
    source = (row.get("attribution_source") or "").strip()
    return STATUS_ATTRIBUTED if attributed and source else STATUS_UNATTRIBUTED


def build_rows(catalog: list[dict], registry: dict[str, dict],
               *, include_all: bool) -> list[dict]:
    """Join catalogue + registry into per-head status rows, catalogue order."""
    rows: list[dict] = []
    for row in catalog:
        slug = (row.get("ocn1") or "").strip()
        status = catalog_status(row)
        reg = registry.get(slug)
        in_default = reg is not None or status == STATUS_ATTRIBUTED
        if not include_all and not in_default:
            continue
        rows.append({
            "ocn1": slug,
            "canonical_name": row.get("canonical_name") or "",
            "catalog_status": status,
            "source_grade": reg["grade"] if reg else GRADE_NONE,
            "attributed_to": (row.get("attributed_to") or "").strip(),
            "attribution_source": (row.get("attribution_source") or "").strip(),
            "source_ref": reg["source_ref"] if reg else "",
            "evidence_note": reg["evidence_note"] if reg else "",
        })
    return rows


def apply_filters(rows: list[dict], args: argparse.Namespace) -> list[dict]:
    out = rows
    if args.status:
        out = [r for r in out if r["source_grade"] == args.status]
    if args.catalog_status:
        out = [r for r in out if r["catalog_status"] == args.catalog_status]
    if args.unattributed:
        out = [r for r in out if r["catalog_status"] == STATUS_UNATTRIBUTED]
    if args.ocn1:
        wanted = set(args.ocn1)
        out = [r for r in out if r["ocn1"] in wanted]
    return out


def render_tsv(rows: list[dict]) -> str:
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=OUTPUT_COLUMNS, delimiter="\t",
                       lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
    return buf.getvalue()


def render_json(rows: list[dict]) -> str:
    return json.dumps(rows, ensure_ascii=False, indent=2) + "\n"


def render_table(rows: list[dict]) -> str:
    cols = ["ocn1", "catalog_status", "source_grade", "source_ref", "canonical_name"]
    widths = {c: len(c) for c in cols}
    for r in rows:
        for c in cols:
            widths[c] = max(widths[c], len(str(r.get(c, ""))))
    line = "  ".join(c.ljust(widths[c]) for c in cols)
    out = [line, "  ".join("-" * widths[c] for c in cols)]
    for r in rows:
        out.append("  ".join(str(r.get(c, "")).ljust(widths[c]) for c in cols))
    return "\n".join(out) + "\n"


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Per-head attribution source-status table (catalogue + registry).")
    p.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    p.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    p.add_argument("--all", action="store_true",
                   help="emit every catalogue row (default: registry heads + attributed rows)")
    p.add_argument("--status", choices=tuple(DOCUMENTED_GRADES) + (GRADE_NONE,),
                   default=None, help="only rows with this source grade")
    p.add_argument("--catalog-status",
                   choices=(STATUS_ATTRIBUTED, STATUS_UNATTRIBUTED), default=None,
                   help="only rows with this catalogue attribution status")
    p.add_argument("--unattributed", action="store_true",
                   help="only catalogue-UNATTRIBUTED rows (next-target view)")
    p.add_argument("--ocn1", action="append", default=[], metavar="SLUG",
                   help="restrict to these slugs (repeatable)")
    p.add_argument("--format", choices=("tsv", "json", "table"), default="tsv")
    p.add_argument("--out", type=Path, default=None)
    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(sys.argv[1:] if argv is None else argv)

    catalog = load_catalog(args.catalog)
    valid_slugs = {(r.get("ocn1") or "").strip() for r in catalog}
    registry = load_registry(args.registry, valid_slugs)

    rows = build_rows(catalog, registry, include_all=args.all)
    rows = apply_filters(rows, args)

    if args.format == "json":
        out = render_json(rows)
    elif args.format == "table":
        out = render_table(rows)
    else:
        out = render_tsv(rows)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(out, encoding="utf-8")
    else:
        sys.stdout.write(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
