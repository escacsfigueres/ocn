#!/usr/bin/env python3
"""Build the scalar ECO join table `catalog/ocn-1.eco.tsv` (roadmap H1.5).

`eco_legacy` packs a slug's ECO codes into one pipe-separated cell
(`A87|A88|A89`), which is honest storage and hostile SQL: joining by ECO
means `LIKE '%B90%'`, which also matches nothing useful and everything
wrong. This sidecar normalises that cell into one row per (slug, code):

    ocn1<TAB>eco<TAB>seq

`seq` is the 0-based position of the code inside that slug's pipe list, so
the original cell is reconstructible by ordering on it. Rows with an empty
`eco_legacy` are skipped entirely — the five class roots, plus the Lichess
long-tail lines that lie beyond ECO's 500-code resolution. Absence from
this table is the honest statement "ECO does not name this line"; it is
never a null code.

`eco_legacy` itself stays in the catalogue unchanged: this is an additive
convenience, not a migration, and existing consumers keep working.

The file is committed like the other sidecars and pinned by a drift test:
change the catalogue without regenerating and CI fails.

Usage:
    python3 tools/build_eco_table.py [--catalog catalog/ocn-1.csv]
        [--out catalog/ocn-1.eco.tsv] [--report]
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CATALOG = REPO_ROOT / "catalog" / "ocn-1.csv"
DEFAULT_OUT = REPO_ROOT / "catalog" / "ocn-1.eco.tsv"

HEADER = "ocn1\teco\tseq"


def split_eco(value: str) -> list[str]:
    """The atomic ECO codes of one `eco_legacy` cell, in declared order."""
    return [part.strip() for part in (value or "").split("|") if part.strip()]


def build_eco_rows(rows: list[dict[str, str]]) -> list[tuple[str, str, int]]:
    """Expand every row's `eco_legacy` cell into (slug, code, seq) triples.

    Order is catalogue row order, then `seq` within a row — deterministic
    without sorting, and it keeps a slug's codes contiguous.
    """
    out: list[tuple[str, str, int]] = []
    for row in rows:
        for seq, code in enumerate(split_eco(row.get("eco_legacy", ""))):
            out.append((row["ocn1"], code, seq))
    return out


def render_tsv(rows: list[tuple[str, str, int]]) -> str:
    lines = [HEADER]
    lines += [f"{ocn1}\t{eco}\t{seq}" for ocn1, eco, seq in rows]
    return "\n".join(lines) + "\n"


def load_catalog(catalog: Path) -> list[dict[str, str]]:
    with catalog.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def build_from_repo(catalog: Path = DEFAULT_CATALOG) -> str:
    return render_tsv(build_eco_rows(load_catalog(catalog)))


def coverage_report(rows: list[dict[str, str]]) -> str:
    pairs = build_eco_rows(rows)
    slugs = {ocn1 for ocn1, _, _ in pairs}
    codes = {eco for _, eco, _ in pairs}
    composites = sum(1 for _, _, seq in pairs if seq == 1)
    return "\n".join([
        f"catalogue rows: {len(rows)}",
        f"eco table rows: {len(pairs)}",
        f"slugs with at least one ECO code: {len(slugs)} "
        f"({len(slugs) / len(rows):.1%})",
        f"slugs with no ECO code: {len(rows) - len(slugs)} "
        f"({(len(rows) - len(slugs)) / len(rows):.1%})",
        f"distinct ECO codes: {len(codes)}",
        f"slugs with a pipe-composite cell: {composites}",
    ]) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build the scalar OCN-1 to ECO join table."
    )
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--report", action="store_true",
                        help="Print a coverage summary to stderr.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(
        sys.argv[1:] if argv is None else argv
    )
    if not args.catalog.exists():
        print(f"ERROR: catalogue not found: {args.catalog}", file=sys.stderr)
        return 1

    rows = load_catalog(args.catalog)
    text = render_tsv(build_eco_rows(rows))
    args.out.write_text(text, encoding="utf-8")
    print(f"wrote {args.out} ({len(text.splitlines()) - 1} rows)")
    if args.report:
        sys.stderr.write(coverage_report(rows))
    return 0


if __name__ == "__main__":
    sys.exit(main())
