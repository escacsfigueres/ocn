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
    "resolved",
    "resolution_kind",
    "canonical_count",
    "ocn1",
    "canonical_name",
    "eco_legacy",
    "parent_ocn1",
    "depth",
    "moves_uci",
    "transposes_to",
    "same_as",
]
RANKED_TSV_FIELDS = [
    "rank",
    "score",
    "fen_key",
    "group_size",
    "depth_span",
    "classes",
    "eco_set",
    "resolved",
    "resolution_kind",
    "canonical_count",
    "ocn1",
    "canonical_name",
    "parent_ocn1",
    "depth",
    "moves_uci",
    "transposes_to",
    "same_as",
]

# Scoring weights for --ranked. Intent: surface the groups most likely to
# require a structural decision (canonical vs alias) before pure
# move-order duplicates of the same family.
SCORE_CLASS_MIXING = 5   # per extra class beyond the first
SCORE_DEPTH_SPAN = 2     # per depth level of spread
SCORE_ECO_DIVERGENCE = 3 # per extra distinct eco_legacy beyond the first
SCORE_NAME_DIVERGENCE = 1
SCORE_PARENT_DIVERGENCE = 1
SCORE_FAMILY_BONUS_CROSS = 3  # A/D, A/E or D/E present
SCORE_FAMILY_BONUS_DE = 1     # D or E present (but not crossed)
SCORE_SIZE_BONUS = 1  # per entry beyond the second


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
                "transposes_to": (r.get("transposes_to") or "").strip(),
                "same_as": (r.get("same_as") or "").strip(),
            }
            for r in members_sorted
        ]
        kind, canonical_count = _resolution_kind(entries)
        groups.append(
            {
                "fen_key": key,
                "group_size": len(members_sorted),
                "depth_span": max(depths) - min(depths),
                "classes": classes,
                "entries": entries,
                "resolution_kind": kind,
                "canonical_count": canonical_count,
                "resolved": kind != "unresolved",
            }
        )

    groups.sort(key=lambda g: (-g["group_size"], g["fen_key"]))  # type: ignore[index,arg-type]
    return groups


RESOLUTION_UNRESOLVED = "unresolved"
RESOLUTION_SINGLE_CANONICAL = "single_canonical"
RESOLUTION_MULTIPLE_CANONICAL = "multiple_canonical"


def _resolution_kind(entries: list[dict[str, object]]) -> tuple[str, int]:
    """Classify a duplicate group's resolution state.

    A group is "resolved" iff:
      - every non-canonical entry (with ``transposes_to``) points at
        another entry within the same group, AND
      - at least one declaration exists — either a non-canonical
        ``transposes_to`` pointer into the group, or an in-group
        ``same_as`` edge between two canonical entries.

    A group with no declarations of any kind is still unresolved:
    the FEN duplication has not been catalogued.

    Two resolved sub-kinds are distinguished:
      - ``single_canonical`` — exactly one canonical entry, every
        other entry points to it. The common case: one literary
        name owns the FEN, the rest are documented move-order
        transpositions.
      - ``multiple_canonical`` — two or more canonical entries
        coexist by design. Declared either by an in-group
        non-canonical pointer (the original mechanism, French /
        Veresov and KID Classical precedents) or by ``same_as``
        edges between the canonicals (the OCN 0.3 mechanism, used
        when there is no third descriptor slug to act as pointer,
        e.g. Rubinstein Opening ⇄ Colle-Zukertort).

    Returns ``(kind, canonical_count)``.
    """
    slugs_in_group = {str(e["ocn1"]) for e in entries}
    canonicals = [e for e in entries if not (e.get("transposes_to") or "")]
    canonical_count = len(canonicals)
    pointers_into_group = [
        e for e in entries
        if (e.get("transposes_to") or "") in slugs_in_group
    ]

    # Detect in-group same_as edges between canonical entries.
    # The relation is treated as undirected: an edge from A to B
    # also resolves the pair regardless of B's same_as field.
    same_as_edges_into_group = []
    for e in canonicals:
        targets = [
            t.strip()
            for t in (e.get("same_as") or "").split("|")
            if t.strip()
        ]
        if any(t in slugs_in_group and t != e["ocn1"] for t in targets):
            same_as_edges_into_group.append(e)

    # No declarations at all → the group's FEN equivalence has not
    # been catalogued yet; treat as unresolved.
    has_declaration = bool(pointers_into_group) or bool(same_as_edges_into_group)
    if not has_declaration:
        return RESOLUTION_UNRESOLVED, canonical_count

    # Any transposes_to pointing outside the group is escape; the
    # group is not internally resolved.
    if canonical_count + len(pointers_into_group) != len(entries):
        return RESOLUTION_UNRESOLVED, canonical_count

    if canonical_count == 1:
        return RESOLUTION_SINGLE_CANONICAL, 1
    return RESOLUTION_MULTIPLE_CANONICAL, canonical_count


def filter_groups(
    groups: list[dict[str, object]],
    *,
    min_size: int,
    class_filter: str | None,
    include_resolved: bool = True,
) -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    for group in groups:
        if int(group["group_size"]) < min_size:  # type: ignore[arg-type]
            continue
        if class_filter and class_filter not in group["classes"]:  # type: ignore[operator]
            continue
        if not include_resolved and group.get("resolved"):
            continue
        out.append(group)
    return out


def _eco_set(group: dict[str, object]) -> list[str]:
    eco_values = {
        (entry["eco_legacy"] or "").strip()
        for entry in group["entries"]  # type: ignore[index]
    }
    return sorted(value for value in eco_values if value)


def score_group(group: dict[str, object]) -> int:
    classes: list[str] = group["classes"]  # type: ignore[assignment]
    entries: list[dict[str, object]] = group["entries"]  # type: ignore[assignment]
    eco = _eco_set(group)
    names = {(e["canonical_name"] or "").strip() for e in entries}
    parents = {(e["parent_ocn1"] or "").strip() for e in entries}

    class_set = set(classes)
    family_bonus = 0
    if {"A", "D"} <= class_set or {"A", "E"} <= class_set or {"D", "E"} <= class_set:
        family_bonus = SCORE_FAMILY_BONUS_CROSS
    elif "D" in class_set or "E" in class_set:
        family_bonus = SCORE_FAMILY_BONUS_DE

    return (
        max(len(classes) - 1, 0) * SCORE_CLASS_MIXING
        + int(group["depth_span"]) * SCORE_DEPTH_SPAN  # type: ignore[arg-type]
        + max(len(eco) - 1, 0) * SCORE_ECO_DIVERGENCE
        + max(len(names) - 1, 0) * SCORE_NAME_DIVERGENCE
        + max(len(parents) - 1, 0) * SCORE_PARENT_DIVERGENCE
        + family_bonus
        + max(int(group["group_size"]) - 2, 0) * SCORE_SIZE_BONUS  # type: ignore[arg-type]
    )


def rank_groups(groups: list[dict[str, object]]) -> list[dict[str, object]]:
    annotated: list[dict[str, object]] = []
    for group in groups:
        enriched = dict(group)
        enriched["score"] = score_group(group)
        enriched["eco_set"] = _eco_set(group)
        annotated.append(enriched)
    annotated.sort(
        key=lambda g: (-int(g["score"]), -int(g["group_size"]), str(g["fen_key"]))
    )
    for index, group in enumerate(annotated, start=1):
        group["rank"] = index
    return annotated


def apply_limit(groups: list[dict[str, object]], limit: int | None) -> list[dict[str, object]]:
    if limit is None:
        return groups
    return groups[:limit]


def write_tsv(groups: list[dict[str, object]], out) -> None:
    writer = csv.DictWriter(out, fieldnames=TSV_FIELDS, delimiter="\t", lineterminator="\n")
    writer.writeheader()
    for group in groups:
        classes_str = ",".join(group["classes"])  # type: ignore[arg-type]
        resolved_str = "1" if group.get("resolved") else "0"
        for entry in group["entries"]:  # type: ignore[index]
            writer.writerow(
                {
                    "fen_key": group["fen_key"],
                    "group_size": group["group_size"],
                    "depth_span": group["depth_span"],
                    "classes": classes_str,
                    "resolved": resolved_str,
                    "resolution_kind": group.get("resolution_kind", RESOLUTION_UNRESOLVED),
                    "canonical_count": group.get("canonical_count", 0),
                    "ocn1": entry["ocn1"],
                    "canonical_name": entry["canonical_name"],
                    "eco_legacy": entry["eco_legacy"],
                    "parent_ocn1": entry["parent_ocn1"],
                    "depth": entry["depth"],
                    "moves_uci": entry["moves_uci"],
                    "transposes_to": entry.get("transposes_to", ""),
                    "same_as": entry.get("same_as", ""),
                }
            )


def write_ranked_tsv(groups: list[dict[str, object]], out) -> None:
    writer = csv.DictWriter(
        out, fieldnames=RANKED_TSV_FIELDS, delimiter="\t", lineterminator="\n"
    )
    writer.writeheader()
    for group in groups:
        classes_str = ",".join(group["classes"])  # type: ignore[arg-type]
        eco_str = "/".join(group["eco_set"])  # type: ignore[arg-type]
        resolved_str = "1" if group.get("resolved") else "0"
        for entry in group["entries"]:  # type: ignore[index]
            writer.writerow(
                {
                    "rank": group["rank"],
                    "score": group["score"],
                    "fen_key": group["fen_key"],
                    "group_size": group["group_size"],
                    "depth_span": group["depth_span"],
                    "classes": classes_str,
                    "eco_set": eco_str,
                    "resolved": resolved_str,
                    "resolution_kind": group.get("resolution_kind", RESOLUTION_UNRESOLVED),
                    "canonical_count": group.get("canonical_count", 0),
                    "ocn1": entry["ocn1"],
                    "canonical_name": entry["canonical_name"],
                    "parent_ocn1": entry["parent_ocn1"],
                    "depth": entry["depth"],
                    "moves_uci": entry["moves_uci"],
                    "transposes_to": entry.get("transposes_to", ""),
                    "same_as": entry.get("same_as", ""),
                }
            )


def write_json(groups: list[dict[str, object]], out) -> None:
    print(json.dumps({"groups": groups}, ensure_ascii=False, sort_keys=True), file=out)


def print_summary(groups: list[dict[str, object]]) -> None:
    duplicate_groups = len(groups)
    rows_in_groups = sum(int(g["group_size"]) for g in groups)  # type: ignore[arg-type]
    resolved = [g for g in groups if g.get("resolved")]
    unresolved = [g for g in groups if not g.get("resolved")]
    multiple_canonical = [
        g for g in groups
        if g.get("resolution_kind") == RESOLUTION_MULTIPLE_CANONICAL
    ]
    rows_in_unresolved = sum(int(g["group_size"]) for g in unresolved)  # type: ignore[arg-type]
    classes_mixed = sum(1 for g in unresolved if len(g["classes"]) > 1)  # type: ignore[arg-type]
    depth_varying = sum(1 for g in unresolved if int(g["depth_span"]) > 0)  # type: ignore[arg-type]
    sizes = Counter(int(g["group_size"]) for g in unresolved)  # type: ignore[arg-type]
    top_group_size = max(sizes) if sizes else 0
    print(
        "SUMMARY "
        f"duplicate_groups={duplicate_groups} "
        f"resolved_groups={len(resolved)} "
        f"unresolved_groups={len(unresolved)} "
        f"multiple_canonical_groups={len(multiple_canonical)} "
        f"rows_in_groups={rows_in_groups} "
        f"rows_in_unresolved_groups={rows_in_unresolved} "
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
    parser.add_argument(
        "--ranked",
        action="store_true",
        help=(
            "score groups by class mixing, depth span, ECO/name/parent "
            "divergence and family bonuses, then emit ranked TSV with "
            "rank/score/eco_set columns"
        ),
    )
    parser.add_argument(
        "--limit",
        type=int,
        help="truncate output to the first N groups (after sorting)",
    )
    parser.add_argument(
        "--include-resolved",
        action="store_true",
        help=(
            "include groups already resolved by transposes_to. By default "
            "the audit hides resolved groups (one canonical entry + every "
            "other entry pointing to a slug within the group) so the "
            "report focuses on duplicates that still need a decision"
        ),
    )
    return parser.parse_args(argv)


def main() -> int:
    args = parse_args(sys.argv[1:])
    if args.min_size < 2:
        fail("--min-size must be >= 2 (groups need at least two entries)")
    if args.ranked and args.json:
        fail("--ranked and --json are mutually exclusive")
    if args.limit is not None and args.limit < 1:
        fail("--limit must be >= 1")

    groups = build_groups(load_catalog(args.catalog))
    summary_groups = filter_groups(
        groups,
        min_size=args.min_size,
        class_filter=args.class_filter,
        include_resolved=True,
    )
    groups = filter_groups(
        groups,
        min_size=args.min_size,
        class_filter=args.class_filter,
        include_resolved=args.include_resolved,
    )
    if args.ranked:
        groups = rank_groups(groups)
    groups = apply_limit(groups, args.limit)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        with args.out.open("w", newline="", encoding="utf-8") as f:
            if args.json:
                write_json(groups, f)
            elif args.ranked:
                write_ranked_tsv(groups, f)
            else:
                write_tsv(groups, f)
    elif args.json:
        write_json(groups, sys.stdout)
    elif args.ranked:
        write_ranked_tsv(groups, sys.stdout)
    else:
        write_tsv(groups, sys.stdout)

    if args.summary:
        print_summary(summary_groups)
    return 0


if __name__ == "__main__":
    sys.exit(main())
