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

    def test_redundant_origin_file_is_accepted(self) -> None:
        """Published PGN disambiguates more than it must. Here only the
        g1 knight can reach e2, so `san()` emits "Ne2" -- but "Nge2" is
        legal notation and rejecting it drops a real game."""
        self.assertEqual(
            uci_sequence_from_pgn("1. e4 e6 2. d4 d5 3. Nc3 Nf6 4. Bg5 Bb4 5. Nge2"),
            "e2e4 e7e6 d2d4 d7d5 b1c3 g8f6 c1g5 f8b4 g1e2",
        )

    def test_redundant_origin_rank_is_accepted(self) -> None:
        self.assertEqual(
            uci_sequence_from_pgn("1. e4 e6 2. d4 d5 3. Nc3 Nf6 4. Bg5 Bb4 5. N1e2"),
            "e2e4 e7e6 d2d4 d7d5 b1c3 g8f6 c1g5 f8b4 g1e2",
        )

    def test_a_redundant_origin_on_a_capture_is_accepted(self) -> None:
        """Only the f3 knight can take on e5, so "Nxe5" is what `san()`
        emits, but "Nfxe5" is what plenty of sources print."""
        self.assertEqual(
            uci_sequence_from_pgn("1. Nf3 e5 2. Nfxe5"),
            "g1f3 e7e5 f3e5",
        )

    def test_a_wrong_origin_file_is_still_rejected(self) -> None:
        """The fallback must not turn into a shrug: "Nbe2" names a
        knight that cannot get there, and that is an error in the source,
        not a notation style."""
        with self.assertRaises(ValueError):
            uci_sequence_from_pgn("1. e4 e6 2. d4 d5 3. Nc3 Nf6 4. Bg5 Bb4 5. Nbe2")

    def test_a_genuinely_ambiguous_token_is_still_rejected(self) -> None:
        """Both knights reach d2 here, so a bare "Nd2" names neither."""
        with self.assertRaises(ValueError):
            uci_sequence_from_pgn("1. Nf3 e5 2. Nc3 e4 3. Nd2")

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
