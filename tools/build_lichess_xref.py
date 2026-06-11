#!/usr/bin/env python3
"""Build the OCN-1 ↔ Lichess cross-reference sidecar.

Maps every OCN-1 row to its Lichess label (audit P2 item 12) by SAN
sequence against the snapshot vendored in `external/lichess-openings/`
(never a live download — the sidecar must be reproducible offline, and
refreshing the vendor is its own decision). Match semantics:

- `exact`: the row's full SAN sequence is a Lichess line.
- `prefix`: the longest Lichess line that prefixes the row's sequence —
  the row is deeper than the Lichess book; the match is its family label.
- `none`: no Lichess line prefixes the sequence (rare first moves).
- `root`: the five class roots, which have no position.

The sidecar lives at `catalog/ocn-1.lichess-xref.tsv` and is pinned by a
drift test: changing the catalogue or the snapshot without regenerating
fails CI. `--report` adds a coverage summary, including the Lichess names
that OCN does not know under canonical_name or aliases (exact and
spelling-folded counts) — the feed for the alias lots.

Usage:
    python3 tools/build_lichess_xref.py [--catalog catalog/ocn-1.csv]
        [--lichess-dir external/lichess-openings]
        [--out catalog/ocn-1.lichess-xref.tsv] [--report]
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

try:
    from chess_uci import last_move_san
except ImportError:  # pragma: no cover - only for unusual direct imports.
    from tools.chess_uci import last_move_san

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CATALOG = REPO_ROOT / "catalog" / "ocn-1.csv"
DEFAULT_LICHESS_DIR = REPO_ROOT / "external" / "lichess-openings"
DEFAULT_OUT = REPO_ROOT / "catalog" / "ocn-1.lichess-xref.tsv"

HEADER = "ocn1\tmatch_kind\tmatched_plies\ttotal_plies\tlichess_eco\tlichess_name"


def san_sequence(moves_uci: str) -> list[str]:
    """Derive the SAN token list for a UCI move string, check/mate
    suffixes stripped (Lichess pgn tokens carry them inconsistently
    relative to our derivation)."""
    toks = moves_uci.split()
    sans: list[str] = []
    for i in range(1, len(toks) + 1):
        san = last_move_san(" ".join(toks[: i - 1]), " ".join(toks[:i]))
        sans.append(san.rstrip("+#"))
    return sans


def load_lichess_index(
    lichess_dir: Path,
) -> dict[tuple[str, ...], tuple[str, str]]:
    """SAN-token tuple -> (eco, name) for every line of the snapshot."""
    index: dict[tuple[str, ...], tuple[str, str]] = {}
    for tsv in sorted(lichess_dir.glob("*.tsv")):
        with tsv.open(newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f, delimiter="\t"):
                sans = tuple(
                    t.rstrip("+#")
                    for t in row["pgn"].split()
                    if not t.endswith(".")
                )
                index[sans] = (row["eco"], row["name"])
    return index


def match_sans(
    sans: list[str],
    index: dict[tuple[str, ...], tuple[str, str]],
) -> tuple[str, int, str, str]:
    """Longest-prefix match of a SAN sequence against the Lichess index."""
    for k in range(len(sans), 0, -1):
        hit = index.get(tuple(sans[:k]))
        if hit:
            kind = "exact" if k == len(sans) else "prefix"
            return kind, k, hit[0], hit[1]
    return "none", 0, "", ""


def build_xref_rows(
    rows: list[dict[str, str]],
    index: dict[tuple[str, ...], tuple[str, str]],
) -> list[tuple[str, str, int, int, str, str]]:
    out: list[tuple[str, str, int, int, str, str]] = []
    for row in rows:
        moves = (row.get("moves_uci") or "").strip()
        if not moves:
            out.append((row["ocn1"], "root", 0, 0, "", ""))
            continue
        sans = san_sequence(moves)
        kind, plies, eco, name = match_sans(sans, index)
        out.append((row["ocn1"], kind, plies, len(sans), eco, name))
    return out


def render_tsv(rows: list[tuple[str, str, int, int, str, str]]) -> str:
    lines = [HEADER]
    for ocn1, kind, plies, total, eco, name in rows:
        lines.append(f"{ocn1}\t{kind}\t{plies}\t{total}\t{eco}\t{name}")
    return "\n".join(lines) + "\n"


def build_from_repo(
    catalog: Path = DEFAULT_CATALOG,
    lichess_dir: Path = DEFAULT_LICHESS_DIR,
) -> str:
    with catalog.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    return render_tsv(build_xref_rows(rows, load_lichess_index(lichess_dir)))


def _fold(name: str) -> str:
    """Spelling-fold for coverage comparison: case plus the systematic
    British/American differences."""
    return (
        name.lower()
        .replace("defence", "defense")
        .replace("centre", "center")
    )


def alias_candidates(
    rows: list[dict[str, str]],
    index: dict[tuple[str, ...], tuple[str, str]],
) -> tuple[list[tuple[str, str, str]], list[tuple[str, str]]]:
    """Position-keyed alias feed.

    Returns (candidates, position_uncovered): a candidate is a Lichess
    line whose exact SAN sequence has an OCN row but whose name is
    absent (after spelling fold) from that row's canonical+aliases —
    i.e. a label OCN could adopt as an alias with Lichess as evidence.
    Position-uncovered lines have no OCN row at their sequence at all.
    Name comparison across the two naming grammars is only meaningful
    position-by-position; whole-vocabulary string membership is not.
    """
    by_sans: dict[tuple[str, ...], dict[str, str]] = {}
    for r in rows:
        moves = (r.get("moves_uci") or "").strip()
        if not moves:
            continue
        key = tuple(san_sequence(moves))
        cur = by_sans.get(key)
        # Phantom path-markers share their parent's sequence; the alias
        # belongs on the shallowest (parent) row.
        if cur is None or int(r["depth"]) < int(cur["depth"]):
            by_sans[key] = r
    candidates: list[tuple[str, str, str]] = []
    uncovered: list[tuple[str, str]] = []
    for sans, (eco, name) in index.items():
        row = by_sans.get(sans)
        if row is None:
            uncovered.append((eco, name))
            continue
        names = {row["canonical_name"]} | {
            a.strip() for a in (row["aliases"] or "").split("|") if a.strip()
        }
        if name in names or _fold(name) in {_fold(n) for n in names}:
            continue
        candidates.append((row["ocn1"], eco, name))
    return candidates, uncovered


def coverage_report(catalog: Path, lichess_dir: Path, xref_text: str) -> str:
    with catalog.open(newline="", encoding="utf-8") as f:
        cat_rows = list(csv.DictReader(f))
    index = load_lichess_index(lichess_dir)
    candidates, uncovered = alias_candidates(cat_rows, index)

    kinds: dict[str, int] = {}
    for line in xref_text.splitlines()[1:]:
        kinds[line.split("\t")[1]] = kinds.get(line.split("\t")[1], 0) + 1
    concrete = sum(v for k, v in kinds.items() if k != "root")
    covered = len(index) - len(uncovered)

    lines = [
        f"xref rows: {sum(kinds.values())} (concrete {concrete})",
        "match_kind: "
        + ", ".join(f"{k}={v}" for k, v in sorted(kinds.items())),
        f"ocn->lichess matched: {kinds.get('exact', 0) + kinds.get('prefix', 0)}"
        f"/{concrete}",
        f"lichess lines: {len(index)}; position-covered by OCN: {covered} "
        f"({covered / len(index):.1%}); position-uncovered: {len(uncovered)}",
        f"alias candidates (covered position, label OCN lacks): "
        f"{len(candidates)}",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build the OCN-1 <-> Lichess cross-reference sidecar."
    )
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    parser.add_argument("--lichess-dir", type=Path, default=DEFAULT_LICHESS_DIR)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--report", action="store_true",
                        help="Print a position-keyed coverage summary to "
                             "stderr.")
    parser.add_argument("--alias-candidates", type=Path, default=None,
                        help="Also write the alias-candidate feed (slug, "
                             "lichess_eco, lichess_name TSV) to this path.")
    args = parser.parse_args()

    text = build_from_repo(args.catalog, args.lichess_dir)
    args.out.write_text(text, encoding="utf-8")
    print(f"wrote {args.out} ({len(text.splitlines()) - 1} rows)")
    if args.report:
        sys.stderr.write(
            coverage_report(args.catalog, args.lichess_dir, text)
        )
    if args.alias_candidates:
        with args.catalog.open(newline="", encoding="utf-8") as f:
            cat_rows = list(csv.DictReader(f))
        cands, _ = alias_candidates(
            cat_rows, load_lichess_index(args.lichess_dir)
        )
        out_lines = ["ocn1\tlichess_eco\tlichess_name"]
        out_lines += [f"{s}\t{e}\t{n}" for s, e, n in cands]
        args.alias_candidates.write_text(
            "\n".join(out_lines) + "\n", encoding="utf-8"
        )
        print(f"wrote {args.alias_candidates} ({len(cands)} candidates)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
