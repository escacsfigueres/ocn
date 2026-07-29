#!/usr/bin/env python3
"""Build the ECO class-divergence sidecar `catalog/ocn-1.eco-divergence.tsv`
(roadmap H2.5).

OCN keeps ECO's *idea* of five structural families and does not keep every
one of ECO's letter assignments. The README used to claim otherwise; this
sidecar replaces the claim with a list. A row is **divergent** when its OCN
class letter is not among the letters of its own ECO codes:

    B.Fre  eco_legacy=C00|C01  ->  class B, ECO letters {C}  ->  divergent
    B.Sic  eco_legacy=B20|...  ->  class B, ECO letters {B}  ->  agrees
    E.Ind  eco_legacy=A61|A70  ->  class E, ECO letters {A}  ->  divergent

A row whose class letter appears among *several* ECO letters agrees: the
composite cell already covers OCN's reading, so there is nothing to explain.
Rows with an empty `eco_legacy` are skipped — outside ECO's coverage there is
no assignment to diverge from (the five class roots plus the Lichess
long-tail).

Output columns:

    ocn1<TAB>ocn_class<TAB>eco_codes<TAB>family_head<TAB>rationale_ref

`family_head` is the depth-1 ancestor slug (the first two segments), which is
the level at which OCN's class decisions are actually taken: the whole French
subtree is `B` because `B.Fre` is `B`. `rationale_ref` is a stable key into
the spec's "Borderline rules" section, drawn from a closed set, so a consumer
can ask "why does this row diverge?" and get an answer that is prose in the
spec rather than a shrug.

The mapping is deliberately keyed on `family_head` and not on the row's ECO
letters: the rationale explains why OCN chose *its* letter for that family,
which is one decision, not one decision per transposition tail.

The file is committed like the other sidecars and pinned by a drift test:
change the catalogue without regenerating and CI fails. `tools/validate.py`
independently recomputes the divergent set and refuses a catalogue whose
committed sidecar disagrees, so the headline number cannot rot silently.

Usage:
    python3 tools/build_eco_divergence.py [--catalog catalog/ocn-1.csv]
        [--out catalog/ocn-1.eco-divergence.tsv] [--report]
"""
from __future__ import annotations

import argparse
import csv
import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CATALOG = REPO_ROOT / "catalog" / "ocn-1.csv"
DEFAULT_OUT = REPO_ROOT / "catalog" / "ocn-1.eco-divergence.tsv"

HEADER = "ocn1\tocn_class\teco_codes\tfamily_head\trationale_ref"

MISC_RATIONALE = "misc"

# family_head -> rationale key in spec/OCN-1.md "Borderline rules".
#
#   french-b        the French is semi-open, not an Open Game (the largest
#                   divergence and the one worth arguing about)
#   indians-e       Indian defences ECO files under flank/closed ranges
#   budapest-e      1.d4 Nf6 2.c4 e5, an Indian countergambit (ECO A51-A52)
#   gruenfeld-e     structurally Indian, ECO's D70-D99 notwithstanding
#   catalan-d       Catalan with an early ...d5 is a queen-pawn fight
#   london-colle-a  queen's-pawn *systems*, not Queen's Gambit theory
#
# Anything not listed falls to `misc`: overwhelmingly deep transposition
# tails where an A- or B-class family's move-order runs into another class's
# theory. Those are per-row accidents of tabiya depth, not family-level
# class decisions, and the spec documents them as a bucket.
RATIONALE_BY_FAMILY_HEAD = {
    "B.Fre": "french-b",
    "E.Ben": "indians-e",
    "E.Blf": "indians-e",
    "E.Ind": "indians-e",
    "E.KID": "indians-e",
    "E.OldI": "indians-e",
    "E.Bud": "budapest-e",
    "E.Gru": "gruenfeld-e",
    "D.Cat": "catalan-d",
    "A.Col": "london-colle-a",
    "A.EID": "london-colle-a",
    "A.Hor": "london-colle-a",
    "A.Lon": "london-colle-a",
    "A.QPO": "london-colle-a",
    "A.Ver": "london-colle-a",
}

RATIONALE_REFS = frozenset(RATIONALE_BY_FAMILY_HEAD.values()) | {MISC_RATIONALE}


def split_eco(value: str) -> list[str]:
    """The atomic ECO codes of one `eco_legacy` cell, in declared order."""
    return [part.strip() for part in (value or "").split("|") if part.strip()]


def family_head(slug: str) -> str:
    """The depth-1 ancestor slug: the first two segments, or the slug itself
    when it is shallower (a class root)."""
    return ".".join(slug.split(".")[:2])


def rationale_ref(head: str) -> str:
    return RATIONALE_BY_FAMILY_HEAD.get(head, MISC_RATIONALE)


def is_divergent(slug: str, eco_legacy: str) -> bool:
    """True when the slug's class letter is absent from its own ECO letters.

    False for rows with no ECO code: absence of a code is not a disagreement
    about a code.
    """
    codes = split_eco(eco_legacy)
    if not codes:
        return False
    return slug[:1] not in {code[:1] for code in codes}


def build_divergence_rows(
    rows: list[dict[str, str]],
) -> list[tuple[str, str, str, str, str]]:
    """Every divergent catalogue row as (slug, class, codes, head, rationale).

    Order is catalogue row order — deterministic without sorting, and the
    diff of a regenerated file reads as the diff of the catalogue.
    """
    out: list[tuple[str, str, str, str, str]] = []
    for row in rows:
        slug = row["ocn1"]
        codes = split_eco(row.get("eco_legacy", ""))
        if not is_divergent(slug, row.get("eco_legacy", "")):
            continue
        head = family_head(slug)
        out.append((slug, slug[:1], "|".join(codes), head, rationale_ref(head)))
    return out


def divergent_slugs(rows: list[dict[str, str]]) -> set[str]:
    """The slug set only — what `tools/validate.py` cross-checks against."""
    return {
        row["ocn1"] for row in rows
        if is_divergent(row["ocn1"], row.get("eco_legacy", ""))
    }


def render_tsv(rows: list[tuple[str, str, str, str, str]]) -> str:
    lines = [HEADER]
    lines += ["\t".join(row) for row in rows]
    return "\n".join(lines) + "\n"


def load_catalog(catalog: Path) -> list[dict[str, str]]:
    with catalog.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def build_from_repo(catalog: Path = DEFAULT_CATALOG) -> str:
    return render_tsv(build_divergence_rows(load_catalog(catalog)))


def coverage_report(rows: list[dict[str, str]]) -> str:
    divergent = build_divergence_rows(rows)
    eco_bearing = sum(1 for row in rows if split_eco(row.get("eco_legacy", "")))
    by_rationale = Counter(row[4] for row in divergent)
    by_class = Counter(row[1] for row in divergent)
    lines = [
        f"catalogue rows: {len(rows)}",
        f"ECO-bearing rows: {eco_bearing}",
        f"divergent rows: {len(divergent)} "
        f"({len(divergent) / eco_bearing:.1%} of ECO-bearing)",
        "by rationale_ref:",
    ]
    lines += [
        f"  {ref:<16} {count:>4}"
        for ref, count in sorted(by_rationale.items(), key=lambda kv: (-kv[1], kv[0]))
    ]
    lines.append("by OCN class:")
    lines += [f"  {cls:<16} {count:>4}" for cls, count in sorted(by_class.items())]
    return "\n".join(lines) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build the OCN-1 ECO class-divergence sidecar."
    )
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--report", action="store_true",
                        help="Print a divergence summary to stderr.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(
        sys.argv[1:] if argv is None else argv
    )
    if not args.catalog.exists():
        print(f"ERROR: catalogue not found: {args.catalog}", file=sys.stderr)
        return 1

    rows = load_catalog(args.catalog)
    text = render_tsv(build_divergence_rows(rows))
    args.out.write_text(text, encoding="utf-8")
    print(f"wrote {args.out} ({len(text.splitlines()) - 1} rows)")
    if args.report:
        sys.stderr.write(coverage_report(rows))
    return 0


if __name__ == "__main__":
    sys.exit(main())
