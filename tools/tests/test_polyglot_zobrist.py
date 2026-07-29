"""Tests for tools/polyglot_zobrist.py.

The Polyglot book hash is normative in spec Annex A, which means OCN does
not get to have an opinion about its value: a hash that disagrees with the
public book format is simply wrong, and every `.bin` opening book and every
consumer joining on the number would silently miss.

So the gate here is the **published test vectors** of the book format, not
a self-consistency check. They are pinned exactly, in hex, with the line
that produces each one; the last two are the pathological cases the format
documentation ships precisely because implementations get them wrong (an
en-passant file key that must appear, then the capture that removes a
castling right).

Beyond the vectors:

  * the key table's shape (781 entries, all distinct, all unsigned 64-bit)
    — a truncated or duplicated paste would fail here rather than corrupt
    a release;
  * the en-passant rule of Annex A, isolated: the file key is taken only
    when a capture is actually legal, not after every double push, checked
    against a deliberately weaker second implementation;
  * a 200-row cross-check over the live catalogue, hashing each position
    twice by two independent paths — replay-then-hash through
    `chess_uci.Board`, and a from-FEN recomputation written here that
    shares nothing with the board code but the key table.

Run:
    python3 -m unittest tools.tests.test_polyglot_zobrist
"""
from __future__ import annotations

import csv
import unittest
from pathlib import Path

from tools.chess_uci import Board, parse_square
from tools.polyglot_zobrist import (
    CASTLING_BASE,
    CASTLING_ORDER,
    EN_PASSANT_BASE,
    PIECE_KIND,
    RANDOM_KEYS,
    TURN_INDEX,
    polyglot_hash,
    polyglot_hash_after_uci,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
CATALOG = REPO_ROOT / "catalog" / "ocn-1.csv"

UINT64_MAX = (1 << 64) - 1

#: The public Polyglot test vectors, as published with the book format:
#: `(description, moves_uci, expected key)`.
PUBLIC_VECTORS = (
    ("initial position", "", 0x463B96181691FC9C),
    ("1.e4", "e2e4", 0x823C9B50FD114196),
    ("1.e4 d5", "e2e4 d7d5", 0x0756B94461C50FB0),
    ("1.e4 d5 2.e5", "e2e4 d7d5 e4e5", 0x662FAFB965DB29D4),
    # The famous one: 2...f5 is a double push with a white pawn beside it,
    # so the en-passant file key must be part of the hash.
    ("1.e4 d5 2.e5 f5", "e2e4 d7d5 e4e5 f7f5", 0x22A48B5A8E47FF78),
    # 3.c4 offers en passant to the b4 pawn ...
    ("1.a4 b5 2.h4 b4 3.c4", "a2a4 b7b5 h2h4 b5b4 c2c4", 0x3C8123EA7B067637),
    # ... 3...bxc3 takes it, and 4.Ra3 loses White's queen-side castling.
    (
        "1.a4 b5 2.h4 b4 3.c4 bxc3 4.Ra3",
        "a2a4 b7b5 h2h4 b5b4 c2c4 b4c3 a1a3",
        0x5C3F9B829B279560,
    ),
)


def board_after(moves_uci: str) -> Board:
    board = Board()
    for token in moves_uci.split():
        board.push_uci(token)
    return board


def hash_with_ep_after_any_double_push(board: Board) -> int:
    """The *weaker* en-passant rule, for contrast only.

    Classical Polyglot implementations take the en-passant file key
    whenever a double push just happened and an enemy pawn stands beside
    it, without checking that the capture is legal. Annex A requires the
    legal-capture test (the same one `fen_key` applies). This helper
    exists so a test can show the two rules parting company; it is never
    the answer OCN publishes.
    """
    key = 0
    for square, piece in enumerate(board.squares):
        if piece:
            key ^= RANDOM_KEYS[PIECE_KIND[piece] * 64 + square]
    for offset, right in enumerate(CASTLING_ORDER):
        if right in board.castling:
            key ^= RANDOM_KEYS[CASTLING_BASE + offset]
    if board.ep_square is not None:
        key ^= RANDOM_KEYS[EN_PASSANT_BASE + board.ep_square % 8]
    if board.white_to_move:
        key ^= RANDOM_KEYS[TURN_INDEX]
    return key


def hash_from_fen_key(fen_key: str) -> int:
    """Hash a four-field FEN directly, without touching the board code.

    The independent second path used by the catalogue cross-check: it
    parses the exported `fen_key` string and XORs the key table itself,
    sharing no move generation, no legality test and no state machine with
    `chess_uci.Board`. `fen_key` already carries Annex A's normalised
    en-passant field, so its square is taken at face value here.
    """
    placement, turn, castling, ep = fen_key.split()

    key = 0
    for offset, rank_text in enumerate(placement.split("/")):
        rank = 7 - offset  # FEN prints rank 8 first; squares count from rank 1.
        file = 0
        for char in rank_text:
            if char.isdigit():
                file += int(char)
                continue
            key ^= RANDOM_KEYS[PIECE_KIND[char] * 64 + rank * 8 + file]
            file += 1
        if file != 8:
            raise ValueError(f"malformed FEN rank '{rank_text}'")

    if castling != "-":
        for offset, right in enumerate(CASTLING_ORDER):
            if right in castling:
                key ^= RANDOM_KEYS[CASTLING_BASE + offset]
    if ep != "-":
        key ^= RANDOM_KEYS[EN_PASSANT_BASE + parse_square(ep) % 8]
    if turn == "w":
        key ^= RANDOM_KEYS[TURN_INDEX]
    return key


class PublicVectorTests(unittest.TestCase):
    """The gate: the published keys, matched exactly."""

    def test_every_published_vector_matches(self) -> None:
        for description, moves_uci, expected in PUBLIC_VECTORS:
            with self.subTest(position=description):
                self.assertEqual(
                    polyglot_hash_after_uci(moves_uci),
                    expected,
                    f"{description}: Polyglot key mismatch",
                )

    def test_initial_position_unsigned_decimal(self) -> None:
        # The column ships as unsigned decimal, so the documented value of
        # the one position everybody can check is pinned in that form too.
        self.assertEqual(polyglot_hash(Board()), 5060803636482931868)

    def test_hash_is_unsigned_64_bit(self) -> None:
        for _, moves_uci, _ in PUBLIC_VECTORS:
            with self.subTest(moves=moves_uci):
                value = polyglot_hash_after_uci(moves_uci)
                self.assertGreaterEqual(value, 0)
                self.assertLessEqual(value, UINT64_MAX)


class KeyTableTests(unittest.TestCase):
    """Shape guards on the vendored table (a bad paste must not ship)."""

    def test_table_has_781_distinct_unsigned_64_bit_keys(self) -> None:
        self.assertEqual(len(RANDOM_KEYS), 781)
        self.assertEqual(len(set(RANDOM_KEYS)), 781)
        self.assertTrue(all(0 <= key <= UINT64_MAX for key in RANDOM_KEYS))

    def test_offsets_partition_the_table(self) -> None:
        self.assertEqual(CASTLING_BASE, 768)          # 12 kinds * 64 squares
        self.assertEqual(EN_PASSANT_BASE, 772)        # + 4 castling rights
        self.assertEqual(TURN_INDEX, 780)             # + 8 en-passant files
        self.assertEqual(TURN_INDEX + 1, len(RANDOM_KEYS))

    def test_piece_kinds_cover_both_colours(self) -> None:
        self.assertEqual(sorted(PIECE_KIND.values()), list(range(12)))
        self.assertEqual(set(PIECE_KIND), set("pPnNbBrRqQkK"))


class EnPassantRuleTests(unittest.TestCase):
    """Annex A's en-passant rule, isolated from everything else."""

    def test_file_key_is_taken_when_a_capture_is_legal(self) -> None:
        # 3.c4 with a black pawn on b4: the capture is legal, so both the
        # strict and the weak rule agree, and both hit the published key.
        board = board_after("a2a4 b7b5 h2h4 b5b4 c2c4")
        self.assertIsNotNone(board.legal_ep_square())
        self.assertEqual(polyglot_hash(board), 0x3C8123EA7B067637)
        self.assertEqual(polyglot_hash(board), hash_with_ep_after_any_double_push(board))

    def test_file_key_is_omitted_after_a_double_push_nobody_can_answer(self) -> None:
        # 2.c4 is a double push, but no black pawn stands beside it.
        board = board_after("d2d4 g8f6 c2c4")
        self.assertEqual(board.ep_square, parse_square("c3"))
        self.assertIsNone(board.legal_ep_square())

        weak = hash_with_ep_after_any_double_push(board)
        self.assertNotEqual(polyglot_hash(board), weak)
        # Exactly one term apart, and it is the c-file en-passant key.
        self.assertEqual(
            polyglot_hash(board) ^ weak,
            RANDOM_KEYS[EN_PASSANT_BASE + parse_square("c3") % 8],
        )

    def test_hash_matches_the_fen_key_normalisation(self) -> None:
        # The two encodings of Annex A must never disagree about en
        # passant: same rule, same position, one identity.
        for moves_uci in ("d2d4 g8f6 c2c4", "e2e4 d7d5 e4e5 f7f5"):
            with self.subTest(moves=moves_uci):
                board = board_after(moves_uci)
                self.assertEqual(polyglot_hash(board), hash_from_fen_key(board.fen_key()))


class ConvenienceTests(unittest.TestCase):
    def test_empty_line_is_the_initial_position(self) -> None:
        self.assertEqual(polyglot_hash_after_uci(""), 0x463B96181691FC9C)
        self.assertEqual(polyglot_hash_after_uci("   "), 0x463B96181691FC9C)

    def test_illegal_move_is_rejected_with_the_offending_token(self) -> None:
        with self.assertRaises(ValueError) as caught:
            polyglot_hash_after_uci("e2e4 e2e4")
        self.assertIn("e2e4", str(caught.exception))


class CatalogueCrossCheckTests(unittest.TestCase):
    """200 real catalogue lines, hashed twice by two independent paths."""

    SAMPLE = 200

    @classmethod
    def setUpClass(cls) -> None:
        with CATALOG.open(newline="", encoding="utf-8") as f:
            lines = [
                (row["ocn1"], row["moves_uci"].strip())
                for row in csv.DictReader(f)
                if row.get("moves_uci", "").strip()
            ]
        # Spread the sample across the whole file rather than taking the
        # first 200 rows, which would all be class A and shallow.
        stride = max(1, len(lines) // cls.SAMPLE)
        cls.sample = lines[::stride][: cls.SAMPLE]

    def test_sample_is_the_expected_size(self) -> None:
        self.assertEqual(len(self.sample), self.SAMPLE)

    def test_replay_path_and_fen_path_agree(self) -> None:
        for slug, moves_uci in self.sample:
            with self.subTest(ocn1=slug):
                board = board_after(moves_uci)
                self.assertEqual(polyglot_hash(board), hash_from_fen_key(board.fen_key()))

    def test_hashing_is_deterministic(self) -> None:
        first = [polyglot_hash_after_uci(moves) for _, moves in self.sample]
        second = [polyglot_hash_after_uci(moves) for _, moves in self.sample]
        self.assertEqual(first, second)

    def test_transpositions_hash_together_and_others_apart(self) -> None:
        # The hash must be a function of the position, not of the move
        # order that reached it: same fen_key iff same key.
        by_fen: dict[str, set[int]] = {}
        for _, moves_uci in self.sample:
            board = board_after(moves_uci)
            by_fen.setdefault(board.fen_key(), set()).add(polyglot_hash(board))
        for fen_key, keys in by_fen.items():
            with self.subTest(fen_key=fen_key):
                self.assertEqual(len(keys), 1)
        self.assertEqual(len({next(iter(k)) for k in by_fen.values()}), len(by_fen))


if __name__ == "__main__":
    unittest.main()
