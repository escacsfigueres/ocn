#!/usr/bin/env python3
"""Resolve a FEN position to OCN-1 catalogue rows."""
from __future__ import annotations

import csv
import json
import sys
from dataclasses import dataclass
from pathlib import Path

try:
    from chess_uci import fen_key_after_uci
except ImportError:  # pragma: no cover - only for unusual direct imports.
    from tools.chess_uci import fen_key_after_uci


DEFAULT_CATALOG = Path(__file__).resolve().parent.parent / "catalog" / "ocn-1.csv"
PIECES = set("PNBRQKpnbrqk")


@dataclass(frozen=True)
class Match:
    ocn1: str
    canonical_name: str
    eco_legacy: str
    depth: int
    moves_uci: str
    fen_key: str


def fail(message: str, *, code: int = 1) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(code)


def load_catalog(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        fail(f"catalogue not found: {path}")
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def normalize_castling(text: str) -> str:
    if text == "-":
        return text
    seen: set[str] = set()
    ordered = ""
    for right in "KQkq":
        if right in text:
            ordered += right
            seen.add(right)
    if len(seen) != len(text) or any(ch not in "KQkq" for ch in text):
        fail(f"invalid FEN castling field: {text!r}", code=2)
    return ordered or "-"


def parse_square(text: str) -> int:
    file = "abcdefgh".index(text[0])
    rank = int(text[1]) - 1
    return rank * 8 + file


def parse_board(board: str) -> list[str]:
    squares = [""] * 64
    ranks = board.split("/")
    if len(ranks) != 8:
        fail(f"invalid FEN board field: {board!r}", code=2)

    for fen_rank, rank_text in enumerate(ranks):
        file = 0
        board_rank = 7 - fen_rank
        for ch in rank_text:
            if ch.isdigit():
                if ch not in "12345678":
                    fail(f"invalid FEN board field: {board!r}", code=2)
                file += int(ch)
                continue
            if ch not in PIECES:
                fail(f"invalid FEN board field: {board!r}", code=2)
            if file >= 8:
                fail(f"invalid FEN board field: {board!r}", code=2)
            squares[board_rank * 8 + file] = ch
            file += 1
        if file != 8:
            fail(f"invalid FEN board field: {board!r}", code=2)
    return squares


def normalize_ep(squares: list[str], turn: str, ep: str) -> str:
    if ep == "-":
        return ep
    if len(ep) != 2 or ep[0] not in "abcdefgh" or ep[1] not in "36":
        fail(f"invalid FEN en-passant field: {ep!r}", code=2)

    target = parse_square(ep)
    pawn = "P" if turn == "w" else "p"
    source_offsets = (-9, -7) if turn == "w" else (7, 9)
    for offset in source_offsets:
        src = target + offset
        if 0 <= src < 64 and abs((src % 8) - (target % 8)) == 1:
            if squares[src] == pawn:
                return ep
    return "-"


def normalize_fen_key(text: str) -> str:
    parts = text.split()
    if len(parts) not in {4, 6}:
        fail(
            "expected FEN with 4 or 6 fields: "
            "<board> <turn> <castling> <en-passant> [halfmove fullmove]",
            code=2,
        )
    if len(parts) == 6 and (
        not parts[4].isdigit() or not parts[5].isdigit() or int(parts[5]) < 1
    ):
        fail("invalid FEN halfmove/fullmove counters", code=2)
    board, turn, castling, ep = parts[:4]
    squares = parse_board(board)
    if turn not in {"w", "b"}:
        fail(f"invalid FEN turn field: {turn!r}", code=2)
    ep = normalize_ep(squares, turn, ep)
    return f"{board} {turn} {normalize_castling(castling)} {ep}"


def catalog_matches(rows: list[dict[str, str]], fen_key: str) -> list[Match]:
    matches: list[Match] = []
    for row in rows:
        moves_uci = (row.get("moves_uci") or "").strip()
        if not moves_uci:
            continue
        try:
            row_fen = fen_key_after_uci(moves_uci)
        except ValueError as exc:
            fail(f"catalogue row {row.get('ocn1')}: {exc}")
        if row_fen != fen_key:
            continue
        matches.append(
            Match(
                ocn1=row["ocn1"],
                canonical_name=row["canonical_name"],
                eco_legacy=row["eco_legacy"],
                depth=int(row["depth"]),
                moves_uci=moves_uci,
                fen_key=row_fen,
            )
        )
    return sorted(matches, key=lambda match: (-match.depth, match.ocn1))


def print_matches(matches: list[Match], *, json_output: bool) -> None:
    if json_output:
        print(
            json.dumps(
                [match.__dict__ for match in matches],
                ensure_ascii=False,
                sort_keys=True,
            )
        )
        return

    for match in matches:
        print(
            "\t".join(
                [
                    match.ocn1,
                    match.canonical_name,
                    match.eco_legacy,
                    str(match.depth),
                    match.moves_uci,
                ]
            )
        )


def main() -> int:
    args = sys.argv[1:]
    json_output = False
    if "--json" in args:
        json_output = True
        args.remove("--json")

    all_matches = False
    if "--all" in args:
        all_matches = True
        args.remove("--all")

    catalog = DEFAULT_CATALOG
    if "--catalog" in args:
        index = args.index("--catalog")
        try:
            catalog = Path(args[index + 1])
        except IndexError:
            fail("--catalog requires a path", code=2)
        del args[index:index + 2]

    if not args:
        fail(
            "usage: python3 tools/from_position.py [--all] [--json] "
            "[--catalog path] <fen>",
            code=2,
        )

    fen_key = normalize_fen_key(" ".join(args))
    rows = load_catalog(catalog)
    matches = catalog_matches(rows, fen_key)
    if not matches:
        fail("no OCN-1 match for FEN position")

    if all_matches:
        print_matches(matches, json_output=json_output)
        return 0

    # same_as co-canonicals are all canonical and are returned together
    # (README, "Three relations per slug") — they are not ambiguity.
    # Build the bidirectional same_as map once.
    same_map: dict[str, set[str]] = {}
    for row in rows:
        for target in (t.strip() for t in (row.get("same_as") or "").split("|")):
            if not target:
                continue
            same_map.setdefault(row["ocn1"], set()).add(target)
            same_map.setdefault(target, set()).add(row["ocn1"])

    top_depth = matches[0].depth
    top = [match for match in matches if match.depth == top_depth]

    # Expand from the first deepest match across same_as links (transitive,
    # any depth). Co-canonical partners join the result; only deepest rows
    # NOT linked this way make the position genuinely ambiguous.
    linked = {top[0].ocn1}
    changed = True
    while changed:
        changed = False
        for match in matches:
            if match.ocn1 in linked:
                continue
            if same_map.get(match.ocn1, set()) & linked:
                linked.add(match.ocn1)
                changed = True

    if any(match.ocn1 not in linked for match in top):
        candidates = ", ".join(match.ocn1 for match in top[:8])
        suffix = "" if len(top) <= 8 else f", ... ({len(top)} total)"
        fail(
            f"FEN position is ambiguous at depth {top_depth}: "
            f"{candidates}{suffix}. Use --all to list matches."
        )

    selected = [match for match in matches if match.ocn1 in linked]
    print_matches(selected, json_output=json_output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
