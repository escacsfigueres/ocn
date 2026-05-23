#!/usr/bin/env python3
"""Audit transposition groups in the OCN-1 catalogue.

Groups catalogue rows by their position FEN key (board + side + castling +
en-passant, ignoring move counters) and reports every group with more than
one entry. The audit is informational: transpositions are expected to occur
and this tool helps prepare canonical/alias decisions for them.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable

try:
    from chess_uci import fen_key_after_uci
except ImportError:  # pragma: no cover - only for unusual direct imports.
    from tools.chess_uci import fen_key_after_uci


DEFAULT_CATALOG = Path(__file__).resolve().parent.parent / "catalog" / "ocn-1.csv"
CLASS_ROOTS = ("A", "B", "C", "D", "E")
TSV_FIELDS = [
    "fen_key",
    "group_size",
    "depth_span",
    "classes",
    "ocn1",
    "canonical_name",
    "eco_legacy",
    "parent_ocn1",
    "depth",
    "moves_uci",
]


def fail(message: str, *, code: int = 1) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(code)


def load_catalog(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        fail(f"catalogue not found: {path}")
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _class_of(slug: str) -> str:
    return slug.split(".", 1)[0] if slug else ""


def _depth(row: dict[str, str]) -> int:
    raw = (row.get("depth") or "").strip()
    try:
        return int(raw)
    except ValueError:
        return -1


def build_groups(rows: Iterable[dict[str, str]]) -> list[dict[str, object]]:
    rows = list(rows)
    entries_by_key: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        slug = (row.get("ocn1") or "").strip()
        moves_uci = (row.get("moves_uci") or "").strip()
        if not moves_uci:
            continue
        try:
            key = fen_key_after_uci(moves_uci)
        except ValueError as exc:
            fail(f"catalogue row {slug}: {exc}")
        entries_by_key[key].append(row)

    groups: list[dict[str, object]] = []
    for key, members in entries_by_key.items():
        if len(members) < 2:
            continue
        members_sorted = sorted(members, key=lambda r: (_depth(r), r.get("ocn1") or ""))
        depths = [_depth(r) for r in members_sorted]
        classes = sorted({_class_of((r.get("ocn1") or "").strip()) for r in members_sorted})
        entries = [
            {
                "ocn1": (r.get("ocn1") or "").strip(),
                "canonical_name": r.get("canonical_name") or "",
                "eco_legacy": r.get("eco_legacy") or "",
                "parent_ocn1": r.get("parent_ocn1") or "",
                "depth": _depth(r),
                "moves_uci": (r.get("moves_uci") or "").strip(),
            }
            for r in members_sorted
        ]
        groups.append(
            {
                "fen_key": key,
                "group_size": len(members_sorted),
                "depth_span": max(depths) - min(depths),
                "classes": classes,
                "entries": entries,
            }
        )

    groups.sort(key=lambda g: (-g["group_size"], g["fen_key"]))  # type: ignore[index,arg-type]
    return groups


def filter_groups(
    groups: list[dict[str, object]],
    *,
    min_size: int,
    class_filter: str | None,
) -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    for group in groups:
        if int(group["group_size"]) < min_size:  # type: ignore[arg-type]
            continue
        if class_filter and class_filter not in group["classes"]:  # type: ignore[operator]
            continue
        out.append(group)
    return out


def write_tsv(groups: list[dict[str, object]], out) -> None:
    writer = csv.DictWriter(out, fieldnames=TSV_FIELDS, delimiter="\t", lineterminator="\n")
    writer.writeheader()
    for group in groups:
        classes_str = ",".join(group["classes"])  # type: ignore[arg-type]
        for entry in group["entries"]:  # type: ignore[index]
            writer.writerow(
                {
                    "fen_key": group["fen_key"],
                    "group_size": group["group_size"],
                    "depth_span": group["depth_span"],
                    "classes": classes_str,
                    "ocn1": entry["ocn1"],
                    "canonical_name": entry["canonical_name"],
                    "eco_legacy": entry["eco_legacy"],
                    "parent_ocn1": entry["parent_ocn1"],
                    "depth": entry["depth"],
                    "moves_uci": entry["moves_uci"],
                }
            )


def write_json(groups: list[dict[str, object]], out) -> None:
    print(json.dumps({"groups": groups}, ensure_ascii=False, sort_keys=True), file=out)


def print_summary(groups: list[dict[str, object]]) -> None:
    duplicate_groups = len(groups)
    rows_in_groups = sum(int(g["group_size"]) for g in groups)  # type: ignore[arg-type]
    classes_mixed = sum(1 for g in groups if len(g["classes"]) > 1)  # type: ignore[arg-type]
    depth_varying = sum(1 for g in groups if int(g["depth_span"]) > 0)  # type: ignore[arg-type]
    sizes = Counter(int(g["group_size"]) for g in groups)  # type: ignore[arg-type]
    top_group_size = max(sizes) if sizes else 0
    print(
        "SUMMARY "
        f"duplicate_groups={duplicate_groups} "
        f"rows_in_groups={rows_in_groups} "
        f"classes_mixed_groups={classes_mixed} "
        f"depth_varying_groups={depth_varying} "
        f"top_group_size={top_group_size}",
        file=sys.stderr,
    )


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Audit transposition groups: catalogue rows that share a FEN "
            "position key. Reports every group with two or more entries."
        )
    )
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--summary", action="store_true", help="print a compact summary to stderr")
    parser.add_argument("--json", action="store_true", help="emit structured JSON instead of TSV")
    parser.add_argument(
        "--min-size",
        type=int,
        default=2,
        help="only report groups with at least this many entries (default 2)",
    )
    parser.add_argument(
        "--class",
        dest="class_filter",
        choices=CLASS_ROOTS,
        help="only report groups that include this top-level class",
    )
    return parser.parse_args(argv)


def main() -> int:
    args = parse_args(sys.argv[1:])
    if args.min_size < 2:
        fail("--min-size must be >= 2 (groups need at least two entries)")

    groups = build_groups(load_catalog(args.catalog))
    groups = filter_groups(groups, min_size=args.min_size, class_filter=args.class_filter)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        with args.out.open("w", newline="", encoding="utf-8") as f:
            if args.json:
                write_json(groups, f)
            else:
                write_tsv(groups, f)
    elif args.json:
        write_json(groups, sys.stdout)
    else:
        write_tsv(groups, sys.stdout)

    if args.summary:
        print_summary(groups)
    return 0


if __name__ == "__main__":
    sys.exit(main())
