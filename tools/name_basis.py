#!/usr/bin/env python3
"""Emit the OCN-1 ``name_basis`` sidecar: WHY each opening name exists.

A ``name_basis`` classifies the naming *basis* of every catalogue row against
the taxonomy in ``docs/non-person-opening-name-taxonomy.md`` (person, geography,
structure, move, metaphor, gambit, tactic, descriptor). This makes the
do-not-attribute map machine readable.

THE HONEST CONSTRAINT: most rows need human judgment to classify, so this
deterministic first pass classifies ONLY unambiguous rows and marks everything
else ``review`` — it NEVER guesses a category. The value is (a) a reusable,
tested tool, and (b) a sidecar capturing the unambiguous classifications plus an
honest review queue, every classification traceable to a deterministic rule.

Deterministic rules (checked in order; first match wins):

  1. ``person`` (rule ``attributed_to``) — fires iff ``attributed_to`` is
     non-empty AND ``attribution_source`` is non-empty (the validator enforces
     ``attributed_to => attribution_source``; a half-filled row is treated as
     unclassified). An already-asserted, sourced person attribution is the
     safest deterministic signal. Taxonomy: the player-eponym track; the audit's
     whole point is that the do-not-attribute map keys off this asserted state.

  2. ``descriptor`` (rule ``editorial_leaf_token``) — fires iff the LEAF (last
     comma-segment) of ``canonical_name`` is one of a small curated set of pure
     editorial-bookkeeping tokens that the taxonomy doc's category 8
     ("Database / editorial descriptor") and bucket D ("the never-attribute
     descriptor map") enumerate as PERMANENTLY unattributed: Main Line,
     Accepted, Declined, Move Order. These name a catalogue relationship, not a
     place/person/structure/metaphor, so the basis of that distinguishing leaf
     segment is unambiguous. Deliberately conservative: more contestable tokens
     the doc also lists (Exchange, System, Classical, Modern, Open, Closed,
     Advance, Fianchetto, Normal) are LEFT as ``review`` because they can denote
     a structure/strategic concept (category 4), not pure bookkeeping.

Every row not matched by a rule → ``name_basis = review``, ``basis_rule =
review``. The tool BIASES HARD toward ``review``: a small, correct deterministic
core plus a large honest review queue is the goal, not broad coverage.

Usage:
    python3 tools/name_basis.py
        [--catalog catalog/ocn-1.csv] [--name-basis CATEGORY]
        [--format tsv|json|table] [--out FILE] [--summary]

    # regenerate the committed sidecar:
    python3 tools/name_basis.py --out catalog/ocn-1.name_basis.tsv

Exit codes: 0 success, 1 data error (missing catalogue), 2 usage error.
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
DEFAULT_OUT = REPO_ROOT / "catalog" / "ocn-1.name_basis.tsv"

# The full taxonomy vocabulary (docs/non-person-opening-name-taxonomy.md). Only
# ``person`` and ``descriptor`` currently have a deterministic rule; the rest are
# documented so the sidecar's category space is explicit, but a row only ever
# receives one of them through a HUMAN review pass, never this tool. ``review``
# is the honest "not deterministically classifiable" bucket.
TAXONOMY_CATEGORIES = (
    "person",      # player eponym (asserted via attributed_to)
    "geography",   # place names the line/family or event anchor (cat 1-3)
    "structure",   # pawn structure / setup / plan (cat 4)
    "move",        # move-shape / piece arrangement (cat 5)
    "metaphor",    # nickname / animal / evocative label (cat 6)
    "gambit",      # material offer (cat 7)
    "tactic",      # tactical motif / evaluation (cat 7)
    "descriptor",  # editorial / DB bookkeeping token (cat 8)
)
REVIEW = "review"
VALID_BASES = frozenset(TAXONOMY_CATEGORIES) | {REVIEW}

# Rule 2's curated editorial-leaf tokens. EXACT, conservative subset of the
# taxonomy doc's category 8 + bucket D: only tokens that name a catalogue
# relationship with no place/person/structure/metaphor meaning. See module
# docstring for why the more contestable descriptor tokens are excluded.
EDITORIAL_LEAF_TOKENS = frozenset({
    "Main Line",
    "Accepted",
    "Declined",
    "Move Order",
})

OUTPUT_COLUMNS = ["ocn1", "canonical_name", "name_basis", "basis_rule"]

RULE_ATTRIBUTED = "attributed_to"
RULE_EDITORIAL = "editorial_leaf_token"


def fail(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def load_catalog(path: Path) -> list[dict]:
    if not path.exists():
        fail(f"catalogue not found: {path}")
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def leaf_segment(canonical_name: str) -> str:
    """The last comma-segment of a canonical name — the distinguishing leaf."""
    return canonical_name.split(",")[-1].strip()


def classify(row: dict) -> tuple[str, str]:
    """Return ``(name_basis, basis_rule)`` for a catalogue row.

    Rules are checked highest-confidence first; the first match wins. No rule
    match → ``(review, review)``. A category is NEVER returned without its rule.
    """
    attributed = (row.get("attributed_to") or "").strip()
    source = (row.get("attribution_source") or "").strip()
    if attributed and source:
        return "person", RULE_ATTRIBUTED

    leaf = leaf_segment(row.get("canonical_name") or "")
    if leaf in EDITORIAL_LEAF_TOKENS:
        return "descriptor", RULE_EDITORIAL

    return REVIEW, REVIEW


def build_rows(catalog: list[dict]) -> list[dict]:
    """Classify every catalogue row, preserving catalogue order."""
    rows: list[dict] = []
    for row in catalog:
        name_basis, basis_rule = classify(row)
        rows.append({
            "ocn1": (row.get("ocn1") or "").strip(),
            "canonical_name": row.get("canonical_name") or "",
            "name_basis": name_basis,
            "basis_rule": basis_rule,
        })
    return rows


def render_tsv(rows: list[dict]) -> str:
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=OUTPUT_COLUMNS, delimiter="\t",
                       lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
    return buf.getvalue()


def build_from_repo(catalog: Path = DEFAULT_CATALOG) -> str:
    """Deterministic TSV for the live catalogue — the committed-sidecar body."""
    return render_tsv(build_rows(load_catalog(catalog)))


def render_json(rows: list[dict]) -> str:
    return json.dumps(rows, ensure_ascii=False, indent=2) + "\n"


def render_table(rows: list[dict]) -> str:
    cols = OUTPUT_COLUMNS
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
    """Counts per name_basis over ALL rows (auto-classified vs review)."""
    counts = {cat: 0 for cat in (*TAXONOMY_CATEGORIES, REVIEW)}
    for r in rows:
        counts[r["name_basis"]] = counts.get(r["name_basis"], 0) + 1
    # Drop never-emitted categories for a tight summary, but always keep review.
    return {k: v for k, v in counts.items() if v or k == REVIEW}


def render_summary(rows: list[dict]) -> str:
    counts = summary_counts(rows)
    total = sum(counts.values())
    auto = total - counts.get(REVIEW, 0)
    lines = [f"{cat}\t{counts[cat]}" for cat in counts]
    lines.append(f"auto_classified\t{auto}")
    lines.append(f"total\t{total}")
    return "\n".join(lines) + "\n"


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Emit the OCN-1 name_basis sidecar (deterministic + review queue).")
    p.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    p.add_argument("--name-basis", choices=tuple(TAXONOMY_CATEGORIES) + (REVIEW,),
                   default=None, help="only rows with this name_basis")
    p.add_argument("--format", choices=("tsv", "json", "table"), default="tsv")
    p.add_argument("--out", type=Path, default=None,
                   help="write the table here (e.g. catalog/ocn-1.name_basis.tsv)")
    p.add_argument("--summary", action="store_true",
                   help="print per-category counts (auto vs review) to stderr")
    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(sys.argv[1:] if argv is None else argv)

    catalog = load_catalog(args.catalog)
    rows = build_rows(catalog)

    # Summary is over the FULL classification (always all rows), to stderr.
    if args.summary:
        sys.stderr.write(render_summary(rows))

    if args.name_basis:
        rows = [r for r in rows if r["name_basis"] == args.name_basis]

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
