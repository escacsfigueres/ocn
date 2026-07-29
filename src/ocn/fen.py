"""Position identity for OCN-1 — spec Annex A, normative.

A catalogue row's position is identified by its ``fen_key``: the first
four FEN fields of the position reached by replaying ``moves_uci`` from
the standard initial position.

1. Board — standard FEN piece placement.
2. Side to move — ``w`` or ``b``.
3. Castling rights — the FEN castling field, ``-`` when none remain.
4. En passant — the target square **only if at least one enemy pawn can
   legally capture en passant** (a capture that would leave the
   capturer's own king in check does not count); otherwise ``-``.

Rule 4 is the trap. Many FEN emitters print the en-passant square after
every double pawn push whether or not the capture is legal, so a string
that looks right never matches the catalogue and the lookup silently
returns nothing instead of failing loudly. :func:`fen_key` normalises to
the legal-capture form; :func:`from_board` is the one-call adapter for
anybody holding a board object.
"""
from __future__ import annotations

from ._chess import FILES, Board

__all__ = ["fen_key", "from_board"]

_PIECES = frozenset("PNBRQKpnbrqk")
_CASTLING_ORDER = "KQkq"


def fen_key(fen: str) -> str:
    """Normalise a FEN string to the OCN-1 position key.

    Accepts a 4-field or a full 6-field FEN and returns
    ``"<board> <turn> <castling> <ep>"``: move counters are dropped (they
    are not part of position identity) and the en-passant square is kept
    only when an en-passant capture is actually legal.

    Raises ``ValueError`` when the FEN is malformed.
    """
    parts = fen.split()
    if len(parts) not in (4, 6):
        raise ValueError(
            "expected a FEN with 4 or 6 fields: "
            "<board> <turn> <castling> <en-passant> [halfmove fullmove], "
            f"got {len(parts)}"
        )
    if len(parts) == 6 and (
        not parts[4].isdigit() or not parts[5].isdigit() or int(parts[5]) < 1
    ):
        raise ValueError(f"invalid FEN halfmove/fullmove counters: {parts[4:6]!r}")

    board_field, turn, castling, ep = parts[:4]
    if turn not in ("w", "b"):
        raise ValueError(f"invalid FEN turn field: {turn!r}")

    board = _board_from(_parse_board(board_field), turn, _parse_castling(castling))
    board.ep_square = _parse_ep_square(ep)
    try:
        # Board.fen_key() re-serialises the placement (so an unusual but
        # parseable board field is canonicalised) and resolves rule 4 via
        # full legality, pins included.
        return board.fen_key()
    except ValueError as exc:  # missing king: legality is undefined
        raise ValueError(f"illegal FEN position: {fen!r} ({exc})") from exc


def from_board(board: object) -> str:
    """Return the OCN-1 ``fen_key`` for any board object exposing ``fen()``.

    This is the adapter that saves python-chess users from the
    silent-zero-matches trap. Current python-chess defaults ``fen()`` to
    the legal-capture form and so agrees with OCN, but the always-emit
    form is one keyword away (``board.fen(en_passant="fen")`` on 1.e4 c5
    yields ``... KQkq c6 0 2``), it is what FEN strings arriving from
    PGN headers, UCI engines and other libraries commonly carry, and it
    is what older versions produced. Routing through the adapter makes
    the question moot::

        import chess
        from ocn import Catalog
        from ocn.fen import from_board

        board = chess.Board()
        board.push_san("e4"); board.push_san("c5")
        rows = Catalog.load().by_fen(from_board(board))

    python-chess is **not** imported here and is not a dependency: the
    argument is duck-typed on a callable ``fen()`` attribute, so any
    board implementation with that method works. (``Catalog.by_fen``
    applies the same normalisation to plain strings, so this helper is
    only needed when it reads better at the call site.)
    """
    emit = getattr(board, "fen", None)
    if not callable(emit):
        raise TypeError(
            "from_board() expects a board object with a callable fen() "
            f"method, got {type(board).__name__}"
        )
    return fen_key(emit())


def _parse_board(board_field: str) -> list[str]:
    """Explode a FEN piece-placement field into 64 squares, a1 first."""
    squares = [""] * 64
    ranks = board_field.split("/")
    if len(ranks) != 8:
        raise ValueError(f"invalid FEN board field: {board_field!r}")

    for fen_rank, rank_text in enumerate(ranks):
        file = 0
        board_rank = 7 - fen_rank
        for char in rank_text:
            if char.isdigit():
                if char not in "12345678":
                    raise ValueError(f"invalid FEN board field: {board_field!r}")
                file += int(char)
                continue
            if char not in _PIECES or file >= 8:
                raise ValueError(f"invalid FEN board field: {board_field!r}")
            squares[board_rank * 8 + file] = char
            file += 1
        if file != 8:
            raise ValueError(f"invalid FEN board field: {board_field!r}")
    return squares


def _parse_castling(castling: str) -> set[str]:
    if castling == "-":
        return set()
    rights = set(castling)
    if len(rights) != len(castling) or not rights <= set(_CASTLING_ORDER):
        raise ValueError(f"invalid FEN castling field: {castling!r}")
    return rights


def _parse_ep_square(ep: str) -> int | None:
    if ep == "-":
        return None
    if len(ep) != 2 or ep[0] not in FILES or ep[1] not in "36":
        raise ValueError(f"invalid FEN en-passant field: {ep!r}")
    return (int(ep[1]) - 1) * 8 + FILES.index(ep[0])


def _board_from(squares: list[str], turn: str, castling: set[str]) -> Board:
    """Build a :class:`Board` positioned mid-game, bypassing the opening setup."""
    board = Board.__new__(Board)
    board.squares = squares
    board.white_to_move = turn == "w"
    board.castling = castling
    board.ep_square = None
    return board
