"""Tests for tools/ocn.py — the consumer reader.

The audit's consumer simulation found that every consumer rewrites the
same four loops; this reader kills that friction with zero schema
impact: by_slug, by_fen, family walk, transposition resolve.

Run:
    python3 -m unittest tools.tests.test_ocn
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools"))

from ocn import Catalog  # noqa: E402

# Stable anchors: slugs are identity (zero slug changes since 1.1.0 and
# the spec freezes them); names are deliberately NOT asserted here.
SICILIAN_FEN = "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2"


class CatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.cat = Catalog.load()

    def test_by_slug_returns_the_row(self) -> None:
        row = self.cat.by_slug("B.Sic")
        self.assertEqual(row["ocn1"], "B.Sic")
        self.assertEqual(row["moves_uci"], "e2e4 c7c5")

    def test_by_slug_unknown_raises(self) -> None:
        with self.assertRaises(KeyError):
            self.cat.by_slug("Z.Nope")

    def test_by_fen_finds_the_position(self) -> None:
        rows = self.cat.by_fen(SICILIAN_FEN)
        self.assertIn("B.Sic", [r["ocn1"] for r in rows])

    def test_fen_key_drops_illegal_ep_square(self) -> None:
        """Board libraries emit the ep square after any double push;
        the catalogue key keeps it only when a capture is legal."""
        from ocn import fen_key

        self.assertEqual(
            fen_key(SICILIAN_FEN),
            "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq -",
        )
        # 1.e4 a6 2.e5 d5: exd6 is a legal ep capture — d6 must survive.
        legal = "rnbqkbnr/1pp1pppp/p7/3pP3/8/8/PPPP1PPP/RNBQKBNR w KQkq d6 0 3"
        self.assertTrue(fen_key(legal).endswith(" d6"))

    def test_by_fen_ignores_move_counters(self) -> None:
        crazy_counters = SICILIAN_FEN.rsplit(" ", 2)[0] + " 41 99"
        self.assertEqual(
            [r["ocn1"] for r in self.cat.by_fen(crazy_counters)],
            [r["ocn1"] for r in self.cat.by_fen(SICILIAN_FEN)],
        )

    def test_children_are_direct_only(self) -> None:
        kids = self.cat.children("B.Sic")
        self.assertTrue(kids)
        self.assertTrue(all(k["parent_ocn1"] == "B.Sic" for k in kids))

    def test_walk_returns_the_whole_subtree(self) -> None:
        subtree = list(self.cat.walk("B.Sic"))
        self.assertEqual(subtree[0]["ocn1"], "B.Sic")
        self.assertTrue(
            all(r["ocn1"] == "B.Sic" or r["ocn1"].startswith("B.Sic.")
                for r in subtree)
        )
        self.assertGreater(len(subtree), len(self.cat.children("B.Sic")))

    def test_resolve_follows_transposes_to_once(self) -> None:
        # E.Nim.Sml.Kmo -> E.Nim.Sml.Bot is the 1.1.0 release's own
        # worked example of a transposition row.
        self.assertEqual(self.cat.resolve("E.Nim.Sml.Kmo"), "E.Nim.Sml.Bot")

    def test_resolve_is_identity_for_canonicals(self) -> None:
        self.assertEqual(self.cat.resolve("B.Sic"), "B.Sic")

    def test_co_canonicals_come_back_as_slugs(self) -> None:
        # 17 same_as groups exist; every declared partner must resolve.
        found = 0
        for row in self.cat.rows:
            for partner in self.cat.co_canonicals(row["ocn1"]):
                self.cat.by_slug(partner)
                found += 1
        self.assertEqual(found, 34)  # 17 bilateral pairs


if __name__ == "__main__":
    unittest.main()
