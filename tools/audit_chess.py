#!/usr/bin/env python3
"""Audit catalogue chess legality without stopping at the first error.

This is the cleanup companion to `tools/validate.py --strict-chess`.
It reports every illegal `moves_uci` sequence and every one-move
parent->child SAN-tail mismatch it can prove from the CSV.
"""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

try:
    from chess_uci import last_move_san, validate_uci_sequence
except ImportError:  # pragma: no cover - only for unusual direct imports.
    from tools.chess_uci import last_move_san, validate_uci_sequence


DEFAULT_CATALOG = Path(__file__).resolve().parent.parent / "catalog" / "ocn-1.csv"
SAN_RE = re.compile(r"^(O-O(?:-O)?|[NBRQK]?[a-h]?[1-8]?x?[a-h][1-8](?:=[NBRQ])?)$")


def normalize_san(san: str) -> str:
    return san.rstrip("+#")


def audit(path: Path) -> int:
    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    by_slug = {row["ocn1"]: row for row in rows}
    illegal: list[str] = []
    san_mismatch: list[str] = []

    for row_no, row in enumerate(rows, start=2):
        slug = row["ocn1"]
        moves = (row.get("moves_uci") or "").strip()
        if not moves:
            continue
        try:
            validate_uci_sequence(moves)
        except ValueError as exc:
            illegal.append(f"row {row_no}: {slug}: {exc}")

    for row_no, row in enumerate(rows, start=2):
        slug = row["ocn1"]
        parent_slug = (row.get("parent_ocn1") or "").strip()
        parent = by_slug.get(parent_slug)
        if not parent:
            continue
        last_segment = slug.rsplit(".", 1)[-1]
        if not SAN_RE.match(last_segment):
            continue
        parent_moves = (parent.get("moves_uci") or "").strip()
        child_moves = (row.get("moves_uci") or "").strip()
        if not child_moves:
            continue
        try:
            san = last_move_san(parent_moves, child_moves)
        except ValueError:
            continue
        if san is not None and normalize_san(san) != last_segment:
            san_mismatch.append(
                f"row {row_no}: {slug}: slug tail {last_segment!r} != "
                f"appended move SAN {normalize_san(san)!r}"
            )

    for item in illegal:
        print(f"ILLEGAL {item}")
    for item in san_mismatch:
        print(f"SAN_MISMATCH {item}")
    print(
        f"SUMMARY rows={len(rows)} illegal={len(illegal)} "
        f"san_mismatch={len(san_mismatch)}"
    )
    return 1 if illegal or san_mismatch else 0


def main() -> int:
    if len(sys.argv) > 2:
        print("usage: python3 tools/audit_chess.py [catalog/ocn-1.csv]", file=sys.stderr)
        return 2
    path = Path(sys.argv[1]) if len(sys.argv) == 2 else DEFAULT_CATALOG
    if not path.exists():
        print(f"ERROR: catalogue not found: {path}", file=sys.stderr)
        return 1
    return audit(path)


if __name__ == "__main__":
    sys.exit(main())
