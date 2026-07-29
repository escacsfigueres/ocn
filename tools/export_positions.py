#!/usr/bin/env python3
"""Export derived position rows from the OCN-1 catalogue.

One row per concrete catalogue entry with the `fen_key` of spec Annex A
(board, turn, castling, legal en-passant), the same position as a
complete `fen` with true halfmove/fullmove counters, and the size of its
transposition group. This is the artefact the `ocn-chess` package bundles
as its O(1) position index.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Iterable

try:
    from chess_uci import Board, parse_uci
except ImportError:  # pragma: no cover - only for unusual direct imports.
    from tools.chess_uci import Board, parse_uci


DEFAULT_CATALOG = Path(__file__).resolve().parent.parent / "catalog" / "ocn-1.csv"
FIELDS = [
    "ocn1",
    "canonical_name",
    "eco_legacy",
    "parent_ocn1",
    "depth",
    "moves_uci",
    "fen_key",
    "fen",
    "transposition_group_size",
    "transposes_to",
    "same_as",
]


def fail(message: str, *, code: int = 1) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(code)


def load_catalog(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        fail(f"catalogue not found: {path}")
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def replay(moves_uci: str) -> tuple[str, str]:
    """Replay a UCI line and return its `(fen_key, fen)` pair.

    `fen_key` is the position identity of spec Annex A (board, turn,
    castling, legal en-passant). `fen` is that key plus the *true*
    counters observed during the replay: the halfmove clock counts plies
    since the last capture or pawn move, the fullmove number is
    `plies // 2 + 1`. Earlier versions emitted a placeholder `0 1`, which
    made the column unusable for anything that parses a real FEN.
    """
    board = Board()
    halfmove = 0
    plies = 0
    for token in moves_uci.split():
        try:
            move = parse_uci(token)
            piece = board.piece_at(move.src)
            capture = bool(board.piece_at(move.dst))
            board.push_uci(token)
        except (ValueError, IndexError) as exc:
            raise ValueError(f"illegal UCI move '{token}': {exc}") from exc
        # Pawn moves cover en-passant captures and promotions, so the two
        # tests below are the whole halfmove-clock rule.
        halfmove = 0 if piece.lower() == "p" or capture else halfmove + 1
        plies += 1
    key = board.fen_key()
    return key, f"{key} {halfmove} {plies // 2 + 1}"


def derive_rows(rows: Iterable[dict[str, str]], *, include_roots: bool) -> list[dict[str, str]]:
    rows = list(rows)
    fen_by_slug: dict[str, str] = {}
    full_fen_by_slug: dict[str, str] = {}
    for row in rows:
        slug = (row.get("ocn1") or "").strip()
        moves_uci = (row.get("moves_uci") or "").strip()
        if not moves_uci:
            continue
        try:
            fen_by_slug[slug], full_fen_by_slug[slug] = replay(moves_uci)
        except ValueError as exc:
            fail(f"catalogue row {slug}: {exc}")

    group_sizes = Counter(fen_by_slug.values())
    derived: list[dict[str, str]] = []
    for row in rows:
        moves_uci = (row.get("moves_uci") or "").strip()
        if not moves_uci and not include_roots:
            continue
        slug = (row.get("ocn1") or "").strip()
        fen_key = fen_by_slug.get(slug, "")
        derived.append(
            {
                "ocn1": slug,
                "canonical_name": row.get("canonical_name") or "",
                "eco_legacy": row.get("eco_legacy") or "",
                "parent_ocn1": row.get("parent_ocn1") or "",
                "depth": row.get("depth") or "",
                "moves_uci": moves_uci,
                "fen_key": fen_key,
                "fen": full_fen_by_slug.get(slug, ""),
                "transposition_group_size": str(group_sizes[fen_key]) if fen_key else "",
                "transposes_to": (row.get("transposes_to") or "").strip(),
                "same_as": (row.get("same_as") or "").strip(),
            }
        )
    return derived


def write_tsv(rows: list[dict[str, str]], out) -> None:
    writer = csv.DictWriter(out, fieldnames=FIELDS, delimiter="\t", lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)


def write_json(rows: list[dict[str, str]], out) -> None:
    print(json.dumps(rows, ensure_ascii=False, sort_keys=True), file=out)


def print_stats(rows: list[dict[str, str]]) -> None:
    concrete = [row for row in rows if row["fen_key"]]
    group_counts = Counter(row["fen_key"] for row in concrete)
    duplicate_groups = sum(1 for count in group_counts.values() if count > 1)
    duplicate_rows = sum(count for count in group_counts.values() if count > 1)
    print(
        "SUMMARY "
        f"rows={len(rows)} "
        f"concrete={len(concrete)} "
        f"unique_fen={len(group_counts)} "
        f"duplicate_groups={duplicate_groups} "
        f"duplicate_rows={duplicate_rows}",
        file=sys.stderr,
    )


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export OCN-1 catalogue rows with derived FEN position keys."
    )
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--format", choices=("tsv", "json"), default="tsv")
    parser.add_argument(
        "--include-roots",
        action="store_true",
        help="include class-root rows with blank FEN fields",
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="print a compact derivation summary to stderr",
    )
    return parser.parse_args(argv)


def main() -> int:
    args = parse_args(sys.argv[1:])
    rows = derive_rows(load_catalog(args.catalog), include_roots=args.include_roots)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        with args.out.open("w", newline="", encoding="utf-8") as f:
            if args.format == "json":
                write_json(rows, f)
            else:
                write_tsv(rows, f)
    elif args.format == "json":
        write_json(rows, sys.stdout)
    else:
        write_tsv(rows, sys.stdout)

    if args.stats:
        print_stats(rows)
    return 0


if __name__ == "__main__":
    sys.exit(main())
