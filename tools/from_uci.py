#!/usr/bin/env python3
"""Resolve a UCI move sequence to the deepest matching OCN-1 slug.

The match is prefix-based: if the input continues beyond a catalogue
tabiya, the deepest catalogue row whose `moves_uci` is a prefix wins.
"""
from __future__ import annotations

import csv
import json
import sys
from dataclasses import dataclass
from pathlib import Path

try:
    from chess_uci import validate_uci_sequence
except ImportError:  # pragma: no cover - only for unusual direct imports.
    from tools.chess_uci import validate_uci_sequence


DEFAULT_CATALOG = Path(__file__).resolve().parent.parent / "catalog" / "ocn-1.csv"


@dataclass(frozen=True)
class Match:
    ocn1: str
    canonical_name: str
    eco_legacy: str
    depth: int
    matched_ply: int
    moves_uci: str


def fail(message: str, *, code: int = 1) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(code)


def load_catalog(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        fail(f"catalogue not found: {path}")
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def normalize_moves(parts: list[str]) -> str:
    moves = " ".join(part.strip() for part in parts if part.strip())
    if not moves:
        fail("missing UCI moves")
    try:
        validate_uci_sequence(moves)
    except ValueError as exc:
        fail(str(exc))
    return moves


def is_prefix(candidate: list[str], query: list[str]) -> bool:
    return bool(candidate) and len(candidate) <= len(query) and query[: len(candidate)] == candidate


def find_match(rows: list[dict[str, str]], moves: str) -> Match | None:
    query = moves.split()
    best: Match | None = None
    for row in rows:
        row_moves = (row.get("moves_uci") or "").strip()
        candidate = row_moves.split()
        if not is_prefix(candidate, query):
            continue
        depth = int(row["depth"])
        match = Match(
            ocn1=row["ocn1"],
            canonical_name=row["canonical_name"],
            eco_legacy=row["eco_legacy"],
            depth=depth,
            matched_ply=len(candidate),
            moves_uci=row_moves,
        )
        if best is None:
            best = match
            continue
        if (match.matched_ply, match.depth, match.ocn1) > (best.matched_ply, best.depth, best.ocn1):
            best = match
    return best


def print_match(match: Match, *, json_output: bool) -> None:
    if json_output:
        print(json.dumps(match.__dict__, ensure_ascii=False, sort_keys=True))
        return
    print(
        "\t".join(
            [
                match.ocn1,
                match.canonical_name,
                match.eco_legacy,
                str(match.depth),
                str(match.matched_ply),
            ]
        )
    )


def main() -> int:
    args = sys.argv[1:]
    json_output = False
    if "--json" in args:
        json_output = True
        args.remove("--json")

    catalog = DEFAULT_CATALOG
    if "--catalog" in args:
        index = args.index("--catalog")
        try:
            catalog = Path(args[index + 1])
        except IndexError:
            fail("--catalog requires a path", code=2)
        del args[index:index + 2]

    if not args:
        fail("usage: python3 tools/from_uci.py [--json] [--catalog path] <uci moves...>", code=2)

    moves = normalize_moves(args)
    match = find_match(load_catalog(catalog), moves)
    if match is None:
        fail("no OCN-1 match for UCI sequence")
    print_match(match, json_output=json_output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
