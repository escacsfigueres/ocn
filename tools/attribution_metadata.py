#!/usr/bin/env python3
"""Emit the OCN-1 ``attribution`` sidecar: the richer attribution metadata that
the apply engine strips at write time.

At apply time ``tools/apply_attribution_manifest.py`` writes only the
``attributed_to`` + ``attribution_source`` (+ optionally ``historical_notes``)
fields into ``catalog/ocn-1.csv``. The committed
``ocn.attribution_manifest.v1`` manifests (mode ``attribution_fields_only``)
carry strictly more: a structured ``evidence_grade`` (CLEAR / PARTIAL / HOLD)
and a parenthetical ROLE inside ``attributed_to`` — the
docs/naming-attribution-audit-methodology.md "type-A..I" qualifier that
distinguishes "invented" from "popularised" from "anchored by a game". This
tool recovers that richer data into a machine-readable sidecar WITHOUT touching
the CSV and WITHOUT inventing anything: every non-``unknown`` value traces to a
specific committed manifest.

Two authoritative inputs, never guessed:

  * ``catalog/ocn-1.csv`` — the JOIN KEY. A row is ATTRIBUTED iff BOTH
    ``attributed_to`` and ``attribution_source`` are non-empty (the validator
    enforces ``attributed_to => attribution_source``; a half-filled row is
    UNATTRIBUTED). The sidecar covers EXACTLY the attributed rows.
  * ``docs/manifests/*.manifest.json`` — only the ``attribution_fields_only``
    manifests carry attribution data; all other modes (diacritic / naming /
    alias / eco) are IGNORED. A manifest change contributes role/grade to a row
    ONLY when its ``attributed_to`` EXACTLY equals the catalogue's applied
    value. The CSV is authoritative: if a manifest disagrees with the applied
    CSV, the CSV value wins, the manifest is NOT trusted for role/grade, and
    the discrepancy is flagged in ``manifest_conflict``.

A row with no matching attribution manifest (attributed before the manifest
engine, or via a manifest without those fields) gets the explicit ``unknown``
sentinel for role / evidence_grade / attribution_type — the tool NEVER guesses.

Sidecar columns (one row per ATTRIBUTED catalogue row, catalogue order):

  | column             | source                                              |
  |--------------------|-----------------------------------------------------|
  | ocn1               | catalogue (the attributed row's slug)               |
  | attributed_to      | catalogue (authoritative; the CSV always wins)      |
  | attribution_source | catalogue (authoritative; the CSV always wins)      |
  | role               | the parenthetical in the MATCHING manifest's        |
  |                    | attributed_to (e.g. "popularizer"); else ``unknown``|
  | evidence_grade     | the matching manifest's evidence_grade; else unknown|
  | attribution_type   | A..I letter deterministically mapped from ``role``  |
  |                    | keywords per the methodology doc; else ``unknown``  |
  | source_manifest    | basename of the manifest that supplied role/grade   |
  |                    | (empty when unknown)                                |
  | manifest_conflict  | basename(s) of any same-slug attribution manifest   |
  |                    | whose attributed_to DISAGREES with the CSV (flag)   |

Usage:
    python3 tools/attribution_metadata.py
        [--catalog catalog/ocn-1.csv] [--manifests docs/manifests]
        [--evidence-grade CLEAR|PARTIAL|HOLD|unknown] [--conflicts-only]
        [--ocn1 SLUG ...] [--format tsv|json|table] [--out FILE] [--summary]

    # regenerate the committed sidecar:
    python3 tools/attribution_metadata.py --out catalog/ocn-1.attribution.tsv

Exit codes: 0 success, 1 data error (missing catalogue / manifests dir,
malformed manifest), 2 usage error.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CATALOG = REPO_ROOT / "catalog" / "ocn-1.csv"
DEFAULT_MANIFESTS = REPO_ROOT / "docs" / "manifests"
DEFAULT_OUT = REPO_ROOT / "catalog" / "ocn-1.attribution.tsv"

# Only this manifest mode carries attribution data; every other mode (diacritic,
# naming, alias, eco) is skipped entirely — those are NOT attribution sources.
ATTRIBUTION_MODE = "attribution_fields_only"

# The explicit "not deterministically recoverable" sentinel. Never a guess.
UNKNOWN = "unknown"

# Evidence grades the manifests use (docs/attribution-batch-engine.md). ``unknown``
# is the sentinel for rows with no matching attribution manifest.
DOCUMENTED_GRADES = ("CLEAR", "PARTIAL", "HOLD")
VALID_GRADES = frozenset(DOCUMENTED_GRADES) | {UNKNOWN}

# Deterministic role-keyword -> attribution type (A..I) mapping. Grounded ONLY
# in docs/naming-attribution-audit-methodology.md, which ties role qualifiers to
# types. Conservative: a role whose keyword is not listed here keeps its
# verbatim role string but gets attribution_type == ``unknown`` (we do not
# invent a type). Checked in order; first keyword found in the role wins.
#   C — Popularizer: doc ties "(popularizer)" verbatim to type C; the same
#       practitioner/advocate family (used it repeatedly, made it visible,
#       without necessarily inventing) maps to C.
#   B — First publication / theoretical codification: a "(... namesake)" whose
#       name comes from a codifying source/system.
ROLE_TYPE_KEYWORDS = (
    ("popularizer", "C"),
    ("practitioner", "C"),
    ("advocate", "C"),
    ("namesake", "B"),
)

OUTPUT_COLUMNS = [
    "ocn1",
    "attributed_to",
    "attribution_source",
    "role",
    "evidence_grade",
    "attribution_type",
    "source_manifest",
    "manifest_conflict",
]


def fail(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def load_catalog(path: Path) -> list[dict]:
    if not path.exists():
        fail(f"catalogue not found: {path}")
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def is_attributed(row: dict) -> bool:
    """ATTRIBUTED iff both attribution fields are non-empty (validator rule)."""
    attributed = (row.get("attributed_to") or "").strip()
    source = (row.get("attribution_source") or "").strip()
    return bool(attributed and source)


def role_parenthetical(attributed_to: str) -> str:
    """The role qualifier inside attributed_to, e.g. 'popularizer'.

    The methodology encodes the attribution type as a parenthetical role
    qualifier (e.g. ``"Bent Larsen (popularizer)"``). Returns the inner text of
    the FIRST top-level parenthetical, stripped; empty string if none.
    """
    m = re.search(r"\(([^)]*)\)", attributed_to)
    return m.group(1).strip() if m else ""


def role_to_type(role: str) -> str:
    """Map a role string to an A..I attribution type, or ``unknown``.

    Deterministic keyword scan grounded in the methodology doc. A role with no
    listed keyword keeps ``unknown`` (we never invent a type).
    """
    low = role.lower()
    for keyword, type_code in ROLE_TYPE_KEYWORDS:
        if keyword in low:
            return type_code
    return UNKNOWN


def load_attribution_manifests(manifests_dir: Path) -> list[tuple[str, dict]]:
    """Return ``[(basename, manifest)]`` for every attribution_fields_only file.

    Non-attribution manifests (any other ``mode``) are skipped. A malformed JSON
    file is a hard data error — we do not silently drop attribution evidence.
    """
    if not manifests_dir.exists():
        fail(f"manifests directory not found: {manifests_dir}")
    out: list[tuple[str, dict]] = []
    for path in sorted(manifests_dir.glob("*.manifest.json")):
        try:
            manifest = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            fail(f"malformed manifest {path.name}: {exc}")
        if manifest.get("mode") == ATTRIBUTION_MODE:
            out.append((path.name, manifest))
    return out


def index_manifest_changes(
    manifests: list[tuple[str, dict]],
) -> dict[str, list[tuple[str, dict]]]:
    """Index attribution-manifest changes by ocn1 -> ``[(basename, change)]``."""
    by_slug: dict[str, list[tuple[str, dict]]] = {}
    for basename, manifest in manifests:
        for change in manifest.get("changes", []):
            slug = change.get("ocn1")
            if not slug:
                fail(f"manifest {basename}: change without ocn1")
            by_slug.setdefault(slug, []).append((basename, change))
    return by_slug


def resolve_row(row: dict, manifest_changes: list[tuple[str, dict]]) -> dict:
    """Build one sidecar row for an attributed catalogue row.

    The catalogue ``attributed_to``/``attribution_source`` are authoritative and
    copied verbatim. role/grade/type are lifted ONLY from a manifest change
    whose ``attributed_to`` EXACTLY equals the catalogue value. Any same-slug
    manifest whose value disagrees is recorded in ``manifest_conflict`` (the CSV
    wins). No matching manifest -> ``unknown`` role/grade/type.
    """
    cat_attr = (row.get("attributed_to") or "").strip()
    cat_source = (row.get("attribution_source") or "").strip()

    matching: tuple[str, dict] | None = None
    conflicts: list[str] = []
    for basename, change in manifest_changes:
        mf_attr = (change.get("fields", {}).get("attributed_to") or "").strip()
        if mf_attr == cat_attr:
            # First exact match wins as the role/grade source.
            if matching is None:
                matching = (basename, change)
        else:
            conflicts.append(basename)

    if matching is not None:
        basename, change = matching
        role = role_parenthetical(cat_attr) or UNKNOWN
        grade = (change.get("evidence_grade") or "").strip() or UNKNOWN
        attribution_type = role_to_type(role) if role != UNKNOWN else UNKNOWN
        source_manifest = basename
    else:
        role = UNKNOWN
        grade = UNKNOWN
        attribution_type = UNKNOWN
        source_manifest = ""

    return {
        "ocn1": (row.get("ocn1") or "").strip(),
        "attributed_to": cat_attr,
        "attribution_source": cat_source,
        "role": role,
        "evidence_grade": grade,
        "attribution_type": attribution_type,
        "source_manifest": source_manifest,
        "manifest_conflict": "; ".join(conflicts),
    }


def build_rows(
    catalog: list[dict], manifests: list[tuple[str, dict]]
) -> list[dict]:
    """Sidecar rows for EXACTLY the attributed catalogue rows, catalogue order."""
    by_slug = index_manifest_changes(manifests)
    rows: list[dict] = []
    for row in catalog:
        if not is_attributed(row):
            continue
        slug = (row.get("ocn1") or "").strip()
        rows.append(resolve_row(row, by_slug.get(slug, [])))
    return rows


def build_from_repo(
    catalog: Path = DEFAULT_CATALOG, manifests_dir: Path = DEFAULT_MANIFESTS
) -> str:
    """Deterministic TSV for the live catalogue + manifests — the committed body."""
    return render_tsv(
        build_rows(load_catalog(catalog), load_attribution_manifests(manifests_dir))
    )


def apply_filters(rows: list[dict], args: argparse.Namespace) -> list[dict]:
    out = rows
    if args.evidence_grade:
        out = [r for r in out if r["evidence_grade"] == args.evidence_grade]
    if args.conflicts_only:
        out = [r for r in out if r["manifest_conflict"]]
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
    cols = ["ocn1", "role", "evidence_grade", "attribution_type",
            "source_manifest", "attributed_to"]
    widths = {c: len(c) for c in cols}
    for r in rows:
        for c in cols:
            widths[c] = max(widths[c], len(str(r.get(c, ""))))
    line = "  ".join(c.ljust(widths[c]) for c in cols)
    out = [line, "  ".join("-" * widths[c] for c in cols)]
    for r in rows:
        out.append("  ".join(str(r.get(c, "")).ljust(widths[c]) for c in cols))
    return "\n".join(out) + "\n"


def summary_counts(rows: list[dict]) -> dict[str, int]:
    """Resolution counts: attributed total, resolved (manifest-backed), unknown,
    conflict, plus per-grade and per-type tallies."""
    counts: dict[str, int] = {
        "attributed": len(rows),
        "resolved": sum(1 for r in rows if r["source_manifest"]),
        "unknown": sum(1 for r in rows if not r["source_manifest"]),
        "conflict": sum(1 for r in rows if r["manifest_conflict"]),
    }
    for grade in (*DOCUMENTED_GRADES, UNKNOWN):
        n = sum(1 for r in rows if r["evidence_grade"] == grade)
        if n:
            counts[f"grade_{grade}"] = n
    return counts


def render_summary(rows: list[dict]) -> str:
    counts = summary_counts(rows)
    return "\n".join(f"{k}\t{v}" for k, v in counts.items()) + "\n"


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Emit the OCN-1 attribution-metadata sidecar "
                    "(catalogue join + manifest role/grade lift).")
    p.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    p.add_argument("--manifests", type=Path, default=DEFAULT_MANIFESTS,
                   help="directory of *.manifest.json (default: docs/manifests)")
    p.add_argument("--evidence-grade",
                   choices=tuple(DOCUMENTED_GRADES) + (UNKNOWN,), default=None,
                   help="only rows with this evidence grade")
    p.add_argument("--conflicts-only", action="store_true",
                   help="only rows where a same-slug manifest disagrees with the CSV")
    p.add_argument("--ocn1", action="append", default=[], metavar="SLUG",
                   help="restrict to these slugs (repeatable)")
    p.add_argument("--format", choices=("tsv", "json", "table"), default="tsv")
    p.add_argument("--out", type=Path, default=None,
                   help="write the table here (e.g. catalog/ocn-1.attribution.tsv)")
    p.add_argument("--summary", action="store_true",
                   help="print resolution counts (resolved vs unknown) to stderr")
    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(sys.argv[1:] if argv is None else argv)

    catalog = load_catalog(args.catalog)
    manifests = load_attribution_manifests(args.manifests)
    rows = build_rows(catalog, manifests)

    # Summary is over the FULL attributed set (before --grade/--ocn1 filters).
    if args.summary:
        sys.stderr.write(render_summary(rows))

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
