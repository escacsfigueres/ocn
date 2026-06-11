#!/usr/bin/env python3
"""Consumer reader for the OCN-1 catalogue (audit P2 item 15).

Every consumer the audit simulated rewrote the same four loops; this
module is those loops, once, with zero schema impact:

    from ocn import Catalog
    cat = Catalog.load()                      # catalog/ocn-1.csv
    cat.by_slug("B.Sic")                      # row dict, KeyError if absent
    cat.by_fen(fen)                           # rows at this position
    cat.children("B.Sic"); cat.walk("B.Sic")  # direct kids / whole subtree
    cat.resolve("E.Nim.Sml.Kmo")              # canonical slug (transposes_to)
    cat.co_canonicals("D.QGD.Exc")            # same_as partners, as slugs

FEN matching uses the catalogue's own key: board + side to move +
castling + en passant, move counters ignored (same convention as
`ocn-1.positions.tsv`). Position lookups derive FENs from `moves_uci`
on first use and are cached for the Catalog's lifetime.
"""
from __future__ import annotations

import csv
from pathlib import Path

try:
    from chess_uci import fen_key_after_uci
except ImportError:  # pragma: no cover - only for unusual direct imports.
    from tools.chess_uci import fen_key_after_uci

DEFAULT_CATALOG = Path(__file__).resolve().parent.parent / "catalog" / "ocn-1.csv"


def fen_key(fen: str) -> str:
    """Normalise a full FEN to the catalogue's position key: board, side,
    castling, en passant — counters dropped, and the ep square kept only
    when an ep capture is actually legal (board libraries emit it after
    any double push; the catalogue does not)."""
    board, side, castling, ep = (fen.split() + ["-"] * 4)[:4]
    if ep != "-" and not _ep_capture_possible(board, side, ep):
        ep = "-"
    return f"{board} {side} {castling} {ep}"


def _ep_capture_possible(board: str, side: str, ep: str) -> bool:
    """True when a pawn of `side` stands beside the ep target square."""
    file_idx = "abcdefgh".index(ep[0])
    # White captures onto rank 6 from rank 5; black onto rank 3 from rank 4.
    pawn, from_rank = ("P", 5) if side == "w" else ("p", 4)
    cells: list[str] = []
    for ch in board.split("/")[8 - from_rank]:
        cells.extend([""] * int(ch) if ch.isdigit() else [ch])
    return any(
        0 <= file_idx + d < 8 and cells[file_idx + d] == pawn
        for d in (-1, 1)
    )


class Catalog:
    def __init__(self, rows: list[dict[str, str]]):
        self.rows = rows
        self._by_slug = {r["ocn1"]: r for r in rows}
        self._by_fen: dict[str, list[dict[str, str]]] | None = None

    @classmethod
    def load(cls, path: Path | str = DEFAULT_CATALOG) -> "Catalog":
        with Path(path).open(newline="", encoding="utf-8") as f:
            return cls(list(csv.DictReader(f)))

    def by_slug(self, slug: str) -> dict[str, str]:
        return self._by_slug[slug]

    def by_fen(self, fen: str) -> list[dict[str, str]]:
        if self._by_fen is None:
            self._by_fen = {}
            for row in self.rows:
                moves = (row.get("moves_uci") or "").strip()
                if not moves:
                    continue
                self._by_fen.setdefault(
                    fen_key_after_uci(moves), []
                ).append(row)
        return list(self._by_fen.get(fen_key(fen), []))

    def children(self, slug: str) -> list[dict[str, str]]:
        return [r for r in self.rows if r["parent_ocn1"] == slug]

    def walk(self, slug: str):
        """Yield the row at `slug`, then its whole subtree, depth-first
        in catalogue order."""
        yield self.by_slug(slug)
        prefix = slug + "."
        for row in self.rows:
            if row["ocn1"].startswith(prefix):
                yield row

    def resolve(self, slug: str) -> str:
        """The canonical slug for a position: follow `transposes_to`
        once (the catalogue contract — links never chain)."""
        target = (self.by_slug(slug).get("transposes_to") or "").strip()
        return target or slug

    def co_canonicals(self, slug: str) -> list[str]:
        """The row's `same_as` partners (co-canonical slugs), if any."""
        raw = (self.by_slug(slug).get("same_as") or "").strip()
        return [t.strip() for t in raw.split("|") if t.strip()]
