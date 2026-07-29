#!/usr/bin/env python3
"""Export derived position rows from the OCN-1 catalogue.

One row per concrete catalogue entry carrying every per-row field that can
be *derived* from `moves_uci`, so that no consumer has to own a chess
engine to use OCN by position. This is the artefact the `ocn-chess`
package bundles as its O(1) position index, and the one a release
publishes as `ocn-1.positions.tsv`.

Per row, all from a single replay of the line:

- `fen_key`   the position identity of spec Annex A: board, turn,
              castling, and the en-passant square only when a capture is
              actually legal. The join key.
- `fen`       the same position as a complete FEN, with the true halfmove
              clock and fullmove number of the replay, so it can be handed
              to a board library unchanged. Never a join key: the counters
              are not part of position identity.
- `san`       the line as numbered SAN movetext (`1.e4 c5 2.Nf3`), derived
              exactly as `tools/build_json_export.py` derives `moves_san`.
- `epd`       the position as EPD: the same four fields as `fen_key`, in
              standard EPD form and with no operations. OCN already
              normalises en passant the way EPD wants it, so the string
              coincides with `fen_key` by construction — the column exists
              so EPD-consuming tooling finds the field under the name it
              expects, while `fen_key` stays the documented join key.
- `zobrist`   the Polyglot book hash of Annex A as unsigned decimal,
              computed in-repo by `tools/polyglot_zobrist.py` (roadmap
              H2.8: the key OCN documents is now computable from this
              checkout, with no private repo and no runtime dependency).

Class roots (`A` through `E`) carry no `moves_uci` and therefore no
position: they are excluded unless `--include-roots` asks for them, and
then every derived column is blank.

Not here yet: a `mainline` SAN continuation for leaf rows. It needs the
popularity data that arrives with roadmap H2.7, and inventing one from
nothing would be worse than not shipping it.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

try:
    from chess_uci import Board, parse_uci
except ImportError:  # pragma: no cover - only for unusual direct imports.
    from tools.chess_uci import Board, parse_uci

try:
    from polyglot_zobrist import polyglot_hash
except ImportError:  # pragma: no cover - only for unusual direct imports.
    from tools.polyglot_zobrist import polyglot_hash


DEFAULT_CATALOG = Path(__file__).resolve().parent.parent / "catalog" / "ocn-1.csv"

#: Column order is part of the artefact's contract: existing columns keep
#: their positions, new ones are appended, so a consumer reading by index
#: (awk, cut, a spreadsheet) survives the upgrade.
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
    "san",
    "epd",
    "zobrist",
]

#: The derived columns, blank for a class root.
DERIVED_FIELDS = ("fen_key", "fen", "san", "epd", "zobrist")


def fail(message: str, *, code: int = 1) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(code)


def load_catalog(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        fail(f"catalogue not found: {path}")
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


@dataclass(frozen=True)
class Position:
    """Everything one UCI line yields, from a single pass over the board."""

    fen_key: str
    fen: str
    san: str
    epd: str
    zobrist: str


def replay(moves_uci: str) -> Position:
    """Replay a UCI line and return every field derived from it.

    One pass, because each derived column wants the same walk: the SAN
    token comes back from every push, the halfmove clock and ply count
    accumulate on the way, and the board at the end answers `fen_key`,
    the EPD and the Polyglot hash.

    `fen` is `fen_key` plus the *true* counters observed during the
    replay: the halfmove clock counts plies since the last capture or
    pawn move, the fullmove number is `plies // 2 + 1`. Earlier versions
    emitted a placeholder `0 1`, which made the column unusable for
    anything that parses a real FEN.
    """
    board = Board()
    halfmove = 0
    plies = 0
    san_tokens: list[str] = []
    for token in moves_uci.split():
        try:
            move = parse_uci(token)
            piece = board.piece_at(move.src)
            capture = bool(board.piece_at(move.dst))
            san = board.push_uci(token)
        except (ValueError, IndexError) as exc:
            raise ValueError(f"illegal UCI move '{token}': {exc}") from exc
        # Numbered movetext: White's move carries the move number, Black's
        # follows bare. Same rendering as build_json_export's `moves_san`.
        san_tokens.append(f"{plies // 2 + 1}.{san}" if plies % 2 == 0 else san)
        # Pawn moves cover en-passant captures and promotions, so the two
        # tests below are the whole halfmove-clock rule.
        halfmove = 0 if piece.lower() == "p" or capture else halfmove + 1
        plies += 1

    key = board.fen_key()
    return Position(
        fen_key=key,
        fen=f"{key} {halfmove} {plies // 2 + 1}",
        san=" ".join(san_tokens),
        # EPD's four fields are `fen_key`'s four fields, en passant
        # included: Annex A normalises to the legal-capture form, which is
        # the form EPD wants.
        epd=key,
        zobrist=str(polyglot_hash(board)),
    )


def derive_rows(rows: Iterable[dict[str, str]], *, include_roots: bool) -> list[dict[str, str]]:
    rows = list(rows)
    position_by_slug: dict[str, Position] = {}
    for row in rows:
        slug = (row.get("ocn1") or "").strip()
        moves_uci = (row.get("moves_uci") or "").strip()
        if not moves_uci:
            continue
        try:
            position_by_slug[slug] = replay(moves_uci)
        except ValueError as exc:
            fail(f"catalogue row {slug}: {exc}")

    group_sizes = Counter(position.fen_key for position in position_by_slug.values())
    derived: list[dict[str, str]] = []
    for row in rows:
        moves_uci = (row.get("moves_uci") or "").strip()
        if not moves_uci and not include_roots:
            continue
        slug = (row.get("ocn1") or "").strip()
        position = position_by_slug.get(slug)
        fen_key = position.fen_key if position else ""
        derived.append(
            {
                "ocn1": slug,
                "canonical_name": row.get("canonical_name") or "",
                "eco_legacy": row.get("eco_legacy") or "",
                "parent_ocn1": row.get("parent_ocn1") or "",
                "depth": row.get("depth") or "",
                "moves_uci": moves_uci,
                "fen_key": fen_key,
                "fen": position.fen if position else "",
                "transposition_group_size": str(group_sizes[fen_key]) if fen_key else "",
                "transposes_to": (row.get("transposes_to") or "").strip(),
                "same_as": (row.get("same_as") or "").strip(),
                "san": position.san if position else "",
                "epd": position.epd if position else "",
                "zobrist": position.zobrist if position else "",
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
        description=(
            "Export OCN-1 catalogue rows with every derived position field: "
            "fen_key, full FEN, SAN movetext, EPD and the Polyglot zobrist."
        )
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
