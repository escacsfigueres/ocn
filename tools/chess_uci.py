"""Small self-contained chess legality helper for OCN validation.

It intentionally covers only what the catalogue needs: validating legal
UCI move sequences from the initial chess position and deriving basic SAN
for one-move parent -> child extensions. It has no third-party runtime
dependency, so CI can run it anywhere Python runs.
"""
from __future__ import annotations

from dataclasses import dataclass


FILES = "abcdefgh"
PROMOTIONS = {"q", "r", "b", "n"}


@dataclass(frozen=True)
class Move:
    src: int
    dst: int
    promotion: str = ""


def square_name(square: int) -> str:
    return FILES[square % 8] + str(square // 8 + 1)


def parse_square(text: str) -> int:
    file = FILES.index(text[0])
    rank = int(text[1]) - 1
    return rank * 8 + file


def parse_uci(text: str) -> Move:
    if len(text) not in {4, 5}:
        raise ValueError(f"invalid UCI move '{text}'")
    return Move(parse_square(text[:2]), parse_square(text[2:4]), text[4:] or "")


def piece_color(piece: str) -> bool:
    return piece.isupper()


class Board:
    def __init__(self) -> None:
        self.squares = [""] * 64
        self.white_to_move = True
        self.castling = {"K", "Q", "k", "q"}
        self.ep_square: int | None = None
        self._setup()

    def _setup(self) -> None:
        back = "RNBQKBNR"
        for file, piece in enumerate(back):
            self.squares[file] = piece
            self.squares[8 + file] = "P"
            self.squares[48 + file] = "p"
            self.squares[56 + file] = piece.lower()

    def clone(self) -> "Board":
        board = Board.__new__(Board)
        board.squares = self.squares[:]
        board.white_to_move = self.white_to_move
        board.castling = set(self.castling)
        board.ep_square = self.ep_square
        return board

    def piece_at(self, square: int) -> str:
        return self.squares[square]

    def king_square(self, white: bool) -> int:
        king = "K" if white else "k"
        return self.squares.index(king)

    def is_attacked(self, square: int, by_white: bool) -> bool:
        file = square % 8
        rank = square // 8

        pawn_rank = rank - 1 if by_white else rank + 1
        if 0 <= pawn_rank < 8:
            pawn = "P" if by_white else "p"
            for pawn_file in (file - 1, file + 1):
                if 0 <= pawn_file < 8 and self.squares[pawn_rank * 8 + pawn_file] == pawn:
                    return True

        knight = "N" if by_white else "n"
        for df, dr in ((1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)):
            nf, nr = file + df, rank + dr
            if 0 <= nf < 8 and 0 <= nr < 8 and self.squares[nr * 8 + nf] == knight:
                return True

        king = "K" if by_white else "k"
        for df in (-1, 0, 1):
            for dr in (-1, 0, 1):
                if df == 0 and dr == 0:
                    continue
                nf, nr = file + df, rank + dr
                if 0 <= nf < 8 and 0 <= nr < 8 and self.squares[nr * 8 + nf] == king:
                    return True

        if self._ray_attacked(file, rank, by_white, ((1, 0), (-1, 0), (0, 1), (0, -1)), "RQ"):
            return True
        return self._ray_attacked(file, rank, by_white, ((1, 1), (1, -1), (-1, 1), (-1, -1)), "BQ")

    def _ray_attacked(
        self,
        file: int,
        rank: int,
        by_white: bool,
        directions: tuple[tuple[int, int], ...],
        attackers: str,
    ) -> bool:
        wanted = attackers if by_white else attackers.lower()
        for df, dr in directions:
            nf, nr = file + df, rank + dr
            while 0 <= nf < 8 and 0 <= nr < 8:
                piece = self.squares[nr * 8 + nf]
                if piece:
                    if piece in wanted:
                        return True
                    break
                nf += df
                nr += dr
        return False

    def is_legal(self, move: Move) -> bool:
        if not self._is_pseudo_legal(move):
            return False
        moving_white = self.white_to_move
        board = self.clone()
        board._push_unchecked(move)
        return not board.is_attacked(board.king_square(moving_white), not moving_white)

    def san(self, move: Move) -> str:
        if not self.is_legal(move):
            raise ValueError(f"illegal move {self.move_name(move)}")
        piece = self.piece_at(move.src)
        dest_piece = self.piece_at(move.dst)
        is_ep = piece.lower() == "p" and move.dst == self.ep_square and not dest_piece
        capture = bool(dest_piece) or is_ep

        if piece.lower() == "k" and abs((move.dst % 8) - (move.src % 8)) == 2:
            text = "O-O" if move.dst % 8 == 6 else "O-O-O"
        elif piece.lower() == "p":
            text = ""
            if capture:
                text += FILES[move.src % 8] + "x"
            text += square_name(move.dst)
            if move.promotion:
                text += "=" + move.promotion.upper()
        else:
            text = piece.upper()
            text += self._disambiguation(move, piece)
            if capture:
                text += "x"
            text += square_name(move.dst)

        board = self.clone()
        board._push_unchecked(move)
        opponent_king = board.king_square(board.white_to_move)
        if board.is_attacked(opponent_king, not board.white_to_move):
            text += "+"
        return text

    def push_uci(self, text: str) -> str:
        move = parse_uci(text)
        san = self.san(move)
        self._push_unchecked(move)
        return san

    def move_name(self, move: Move) -> str:
        return square_name(move.src) + square_name(move.dst) + move.promotion

    def _disambiguation(self, move: Move, piece: str) -> str:
        has_other = False
        same_file = False
        same_rank = False
        for src, candidate in enumerate(self.squares):
            if src == move.src or candidate != piece:
                continue
            other = Move(src, move.dst, move.promotion)
            if self.is_legal(other):
                has_other = True
                if src % 8 == move.src % 8:
                    same_file = True
                if src // 8 == move.src // 8:
                    same_rank = True
        if not has_other:
            return ""
        if not same_file:
            return FILES[move.src % 8]
        if not same_rank:
            return str(move.src // 8 + 1)
        return square_name(move.src)

    def _is_pseudo_legal(self, move: Move) -> bool:
        if not (0 <= move.src < 64 and 0 <= move.dst < 64):
            return False
        piece = self.piece_at(move.src)
        if not piece or piece_color(piece) != self.white_to_move:
            return False
        target = self.piece_at(move.dst)
        if target and piece_color(target) == self.white_to_move:
            return False
        if move.promotion and move.promotion not in PROMOTIONS:
            return False

        df = move.dst % 8 - move.src % 8
        dr = move.dst // 8 - move.src // 8
        kind = piece.lower()

        if kind == "p":
            return self._pawn_pseudo_legal(move, piece, df, dr, target)
        if move.promotion:
            return False
        if kind == "n":
            return (abs(df), abs(dr)) in {(1, 2), (2, 1)}
        if kind == "b":
            return abs(df) == abs(dr) and self._path_clear(move.src, move.dst)
        if kind == "r":
            return (df == 0 or dr == 0) and self._path_clear(move.src, move.dst)
        if kind == "q":
            return (df == 0 or dr == 0 or abs(df) == abs(dr)) and self._path_clear(move.src, move.dst)
        if kind == "k":
            return self._king_pseudo_legal(move, piece, df, dr)
        return False

    def _pawn_pseudo_legal(self, move: Move, piece: str, df: int, dr: int, target: str) -> bool:
        white = piece.isupper()
        direction = 1 if white else -1
        start_rank = 1 if white else 6
        promotion_rank = 7 if white else 0
        src_rank = move.src // 8
        dst_rank = move.dst // 8
        reaches_promotion = dst_rank == promotion_rank
        if reaches_promotion != bool(move.promotion):
            return False
        if df == 0 and dr == direction and not target:
            return True
        if df == 0 and dr == 2 * direction and src_rank == start_rank and not target:
            between = move.src + 8 * direction
            return not self.piece_at(between)
        if abs(df) == 1 and dr == direction:
            return bool(target) or move.dst == self.ep_square
        return False

    def _king_pseudo_legal(self, move: Move, piece: str, df: int, dr: int) -> bool:
        if max(abs(df), abs(dr)) == 1:
            return True
        if dr != 0 or abs(df) != 2:
            return False
        white = piece.isupper()
        rank = 0 if white else 7
        if move.src != rank * 8 + 4:
            return False
        kingside = df == 2
        right = "K" if white and kingside else "Q" if white else "k" if kingside else "q"
        if right not in self.castling:
            return False
        rook_square = rank * 8 + (7 if kingside else 0)
        rook = "R" if white else "r"
        if self.piece_at(rook_square) != rook:
            return False
        path_files = (5, 6) if kingside else (1, 2, 3)
        if any(self.piece_at(rank * 8 + file) for file in path_files):
            return False
        attacked_files = (4, 5, 6) if kingside else (4, 3, 2)
        return not any(self.is_attacked(rank * 8 + file, not white) for file in attacked_files)

    def _path_clear(self, src: int, dst: int) -> bool:
        sf, sr = src % 8, src // 8
        df, dr = dst % 8, dst // 8
        step_f = (df > sf) - (df < sf)
        step_r = (dr > sr) - (dr < sr)
        f, r = sf + step_f, sr + step_r
        while (f, r) != (df, dr):
            if self.squares[r * 8 + f]:
                return False
            f += step_f
            r += step_r
        return True

    def _push_unchecked(self, move: Move) -> None:
        piece = self.piece_at(move.src)
        target = self.piece_at(move.dst)
        old_ep = self.ep_square
        self.ep_square = None

        if piece.lower() == "p" and move.dst == old_ep and not target and move.src % 8 != move.dst % 8:
            captured = move.dst - (8 if piece.isupper() else -8)
            self.squares[captured] = ""

        self.squares[move.src] = ""
        self.squares[move.dst] = move.promotion.upper() if piece.isupper() and move.promotion else (
            move.promotion if move.promotion else piece
        )

        if piece.lower() == "k" and abs((move.dst % 8) - (move.src % 8)) == 2:
            rank = move.src // 8
            if move.dst % 8 == 6:
                rook_src, rook_dst = rank * 8 + 7, rank * 8 + 5
            else:
                rook_src, rook_dst = rank * 8, rank * 8 + 3
            self.squares[rook_dst] = self.squares[rook_src]
            self.squares[rook_src] = ""

        self._update_castling_rights(move, piece, target)

        if piece.lower() == "p" and abs((move.dst // 8) - (move.src // 8)) == 2:
            self.ep_square = (move.src + move.dst) // 2
        self.white_to_move = not self.white_to_move

    def _update_castling_rights(self, move: Move, piece: str, target: str) -> None:
        if piece == "K":
            self.castling.discard("K")
            self.castling.discard("Q")
        elif piece == "k":
            self.castling.discard("k")
            self.castling.discard("q")
        for square, right in ((0, "Q"), (7, "K"), (56, "q"), (63, "k")):
            if move.src == square or (move.dst == square and target):
                self.castling.discard(right)


def validate_uci_sequence(moves: str) -> list[str]:
    board = Board()
    sans: list[str] = []
    for token in moves.split():
        try:
            sans.append(board.push_uci(token))
        except (ValueError, IndexError) as exc:
            raise ValueError(f"illegal UCI move '{token}': {exc}") from exc
    return sans


def last_move_san(parent_moves: str, child_moves: str) -> str | None:
    parent = parent_moves.split()
    child = child_moves.split()
    if len(child) != len(parent) + 1 or child[: len(parent)] != parent:
        return None
    board = Board()
    for token in parent:
        board.push_uci(token)
    return board.push_uci(child[-1])
