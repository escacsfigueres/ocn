"""Tests for SAN/PGN helpers in tools/chess_uci.py."""
from __future__ import annotations

import unittest

from tools.chess_uci import fen_key_after_uci, fen_keys_after_uci, pgn_tokens, uci_sequence_from_pgn


class ChessUciTests(unittest.TestCase):
    def test_pgn_tokens_strip_move_numbers_and_results(self) -> None:
        self.assertEqual(
            pgn_tokens("1. e4 c5 2. Nf3 d6 1/2-1/2"),
            ["e4", "c5", "Nf3", "d6"],
        )

    def test_san_pgn_to_uci_sequence(self) -> None:
        self.assertEqual(
            uci_sequence_from_pgn("1. e4 c5 2. Nf3 d6 3. d4 cxd4"),
            "e2e4 c7c5 g1f3 d7d6 d2d4 c5d4",
        )

    def test_castling_and_capture_san(self) -> None:
        self.assertEqual(
            uci_sequence_from_pgn("1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 4. O-O"),
            "e2e4 e7e5 g1f3 b8c6 f1b5 a7a6 e1g1",
        )

    def test_fen_key_normalizes_non_capturable_ep(self) -> None:
        self.assertEqual(
            fen_key_after_uci("c2c4 c7c5"),
            "rnbqkbnr/pp1ppppp/8/2p5/2P5/8/PP1PPPPP/RNBQKBNR w KQkq -",
        )

    def test_fen_keys_after_each_uci_ply(self) -> None:
        keys = fen_keys_after_uci("d2d4 d7d5 c2c4")
        self.assertEqual(len(keys), 3)
        self.assertEqual(
            keys[-1],
            "rnbqkbnr/ppp1pppp/8/3p4/2PP4/8/PP2PPPP/RNBQKBNR b KQkq -",
        )


if __name__ == "__main__":
    unittest.main()
