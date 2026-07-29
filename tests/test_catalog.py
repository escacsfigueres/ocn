"""Round-trip tests for the `ocn` package reader against the bundled data.

Run from a checkout without installing anything:

    python3 -m unittest discover -s tests

Slugs are the stable anchors (zero `ocn1` changes since 1.1.0, and the
spec freezes them); canonical names are asserted only where a name is
itself the thing under test, such as the diacritic fold.
"""
from __future__ import annotations

import sys
import time
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

import ocn  # noqa: E402
from ocn import Catalog, Row, fen_key  # noqa: E402
from ocn.fen import from_board  # noqa: E402

# 1.e4 c5 as a board library prints it: the en-passant square is emitted
# after the double push even though no white pawn can take on c6.
SICILIAN_FEN_WITH_EP = "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2"
SICILIAN_FEN_KEY = "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq -"


class CatalogLoadTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.cat = Catalog.load()

    def test_bundled_catalogue_loads(self) -> None:
        self.assertGreater(len(self.cat), 5000)
        self.assertEqual(len(list(self.cat)), len(self.cat))

    def test_versions_are_distinct_and_present(self) -> None:
        self.assertTrue(ocn.__version__)
        self.assertTrue(self.cat.version())
        self.assertNotEqual(self.cat.version(), "unknown")

    def test_rows_are_typed(self) -> None:
        row = self.cat.by_slug("B.Sic.Naj.Eng")
        self.assertIsInstance(row, Row)
        self.assertEqual(row.canonical_name, "Sicilian Najdorf, English Attack")
        self.assertEqual(row.eco, ("B90",))
        self.assertEqual(row.parent, "B.Sic.Naj")
        self.assertEqual(row.depth, 3)
        self.assertEqual(row.moves_uci[:2], ("e2e4", "c7c5"))
        self.assertIn("sharp", row.flags)
        self.assertIsNone(row.transposes_to)
        self.assertEqual(row.same_as, ())

    def test_class_roots_carry_no_position(self) -> None:
        root = self.cat.by_slug("B")
        self.assertTrue(root.is_class_root)
        self.assertEqual(root.moves_uci, ())
        self.assertIsNone(root.parent)

    def test_eco_pipes_are_split(self) -> None:
        self.assertGreater(len(self.cat.by_slug("B.Sic").eco), 1)

    def test_by_slug_unknown_raises_and_get_returns_none(self) -> None:
        with self.assertRaises(KeyError):
            self.cat.by_slug("Z.Nope")
        self.assertIsNone(self.cat.get("Z.Nope"))


class LookupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.cat = Catalog.load()

    def test_by_eco_is_non_empty_and_deepest_first(self) -> None:
        rows = self.cat.by_eco("B90")
        self.assertTrue(rows)
        depths = [row.depth for row in rows]
        self.assertEqual(depths, sorted(depths, reverse=True))
        self.assertTrue(all("B90" in row.eco for row in rows))

    def test_by_eco_is_case_insensitive(self) -> None:
        self.assertEqual(
            [row.ocn1 for row in self.cat.by_eco("b90")],
            [row.ocn1 for row in self.cat.by_eco("B90")],
        )

    def test_by_name_matches_an_alias_case_insensitively(self) -> None:
        # `by_name` is an exact match over canonical names and aliases:
        # "Najdorf Variation" is an alias of B.Sic.Naj, plain "najdorf"
        # is not a name anybody carries — that is what `search` is for.
        self.assertIn(
            "B.Sic.Naj", [row.ocn1 for row in self.cat.by_name("najdorf variation")]
        )

    def test_by_name_folds_diacritics(self) -> None:
        """"Grunfeld" must find the Grünfeld rows — the fold contract."""
        rows = self.cat.by_name("Grunfeld")
        self.assertTrue(rows)
        self.assertIn("E.Gru", [row.ocn1 for row in rows])
        self.assertTrue(
            any("ü" in row.canonical_name or "ü" in "|".join(row.aliases) for row in rows)
        )

    def test_by_name_unknown_is_empty(self) -> None:
        self.assertEqual(self.cat.by_name("no such opening at all"), [])

    def test_search_is_substring_broadest_first(self) -> None:
        rows = self.cat.search("najdorf", limit=5)
        self.assertTrue(rows)
        self.assertLessEqual(len(rows), 5)
        self.assertEqual("B.Sic.Naj", rows[0].ocn1)
        depths = [row.depth for row in rows]
        self.assertEqual(depths, sorted(depths))

    def test_search_folds_diacritics_too(self) -> None:
        self.assertTrue(self.cat.search("grunfeld"))

    def test_search_of_empty_text_is_empty(self) -> None:
        self.assertEqual(self.cat.search("   "), [])


class PositionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.cat = Catalog.load()

    def test_fen_key_drops_an_illegal_ep_square(self) -> None:
        self.assertEqual(fen_key(SICILIAN_FEN_WITH_EP), SICILIAN_FEN_KEY)

    def test_fen_key_keeps_a_legal_ep_square(self) -> None:
        # 1.e4 a6 2.e5 d5: exd6 is legal, so d6 belongs in the key.
        legal = "rnbqkbnr/1pp1pppp/p7/3pP3/8/8/PPPP1PPP/RNBQKBNR w KQkq d6 0 3"
        self.assertTrue(fen_key(legal).endswith(" d6"))

    def test_fen_key_accepts_four_field_fens(self) -> None:
        self.assertEqual(fen_key(SICILIAN_FEN_KEY), SICILIAN_FEN_KEY)

    def test_fen_key_rejects_malformed_input(self) -> None:
        for bad in ("", "not a fen", SICILIAN_FEN_KEY.replace(" w ", " x ")):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                fen_key(bad)

    def test_by_fen_survives_the_always_ep_trap(self) -> None:
        """The headline consumer bug: a board library's FEN must match.

        python-chess prints `c6` after 1...c5 whether or not the capture
        is legal. Without normalisation the lookup returns nothing and
        the consumer concludes the catalogue has no Sicilian.
        """
        trapped = [row.ocn1 for row in self.cat.by_fen(SICILIAN_FEN_WITH_EP)]
        normalised = [row.ocn1 for row in self.cat.by_fen(SICILIAN_FEN_KEY)]
        self.assertIn("B.Sic", trapped)
        self.assertEqual(trapped, normalised)

    def test_by_fen_ignores_move_counters(self) -> None:
        weird = SICILIAN_FEN_WITH_EP.rsplit(" ", 2)[0] + " 41 99"
        self.assertEqual(
            [row.ocn1 for row in self.cat.by_fen(weird)],
            [row.ocn1 for row in self.cat.by_fen(SICILIAN_FEN_WITH_EP)],
        )

    def test_by_fen_unknown_position_is_empty(self) -> None:
        self.assertEqual(self.cat.by_fen("8/8/8/8/8/8/8/K6k w - -"), [])

    def test_from_board_adapts_any_board_with_a_fen_method(self) -> None:
        """python-chess is never imported; the adapter is duck-typed."""

        class FakeBoard:
            def fen(self) -> str:
                return SICILIAN_FEN_WITH_EP

        self.assertEqual(from_board(FakeBoard()), SICILIAN_FEN_KEY)
        self.assertIn("B.Sic", [row.ocn1 for row in self.cat.by_fen(from_board(FakeBoard()))])

    def test_from_board_rejects_non_boards(self) -> None:
        with self.assertRaises(TypeError):
            from_board(object())

    def test_python_chess_is_never_imported(self) -> None:
        self.assertNotIn("chess", sys.modules)


class HierarchyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.cat = Catalog.load()

    def test_parents_is_a_root_to_parent_breadcrumb(self) -> None:
        self.assertEqual(
            [row.ocn1 for row in self.cat.parents("B.Sic.Naj.Eng")],
            ["B", "B.Sic", "B.Sic.Naj"],
        )

    def test_parents_of_a_class_root_is_empty(self) -> None:
        self.assertEqual(self.cat.parents("B"), [])

    def test_children_are_direct_only(self) -> None:
        kids = self.cat.children("B.Sic")
        self.assertTrue(kids)
        self.assertTrue(all(kid.parent == "B.Sic" for kid in kids))

    def test_walk_returns_the_whole_subtree(self) -> None:
        subtree = list(self.cat.walk("B.Sic"))
        self.assertEqual(subtree[0].ocn1, "B.Sic")
        self.assertTrue(
            all(row.ocn1 == "B.Sic" or row.ocn1.startswith("B.Sic.") for row in subtree)
        )
        self.assertGreater(len(subtree), len(self.cat.children("B.Sic")))


class CanonicalisationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.cat = Catalog.load()

    def test_resolve_follows_transposes_to_once(self) -> None:
        self.assertEqual(self.cat.resolve("E.Nim.Sml.Kmo"), "E.Nim.Sml.Bot")

    def test_resolve_is_identity_for_canonicals(self) -> None:
        self.assertEqual(self.cat.resolve("B.Sic"), "B.Sic")

    def test_transposition_links_never_chain(self) -> None:
        """The catalogue contract: one hop resolves, always."""
        for row in self.cat:
            if row.transposes_to:
                target = self.cat.by_slug(row.transposes_to)
                self.assertIsNone(target.transposes_to, row.ocn1)

    def test_co_canonicals_come_back_as_resolvable_slugs(self) -> None:
        found = 0
        for row in self.cat:
            for partner in self.cat.co_canonicals(row.ocn1):
                self.assertIsNotNone(self.cat.get(partner), partner)
                found += 1
        self.assertGreater(found, 0)

    def test_co_canonicals_are_symmetric(self) -> None:
        for row in self.cat:
            for partner in self.cat.co_canonicals(row.ocn1):
                self.assertIn(row.ocn1, self.cat.co_canonicals(partner))


class PositionIndexPerformanceTests(unittest.TestCase):
    """Guard the O(1) promise: lookups read the bundled index, never replay.

    Deriving the index by replaying every `moves_uci` takes roughly half
    a second; the sidecar makes the first lookup a parse and every later
    one a dict hit. The timing bound is deliberately loose (CI machines
    vary wildly); the structural assertion below is the real guard.
    """

    def test_bundled_positions_index_is_used(self) -> None:
        cat = Catalog.load()
        self.assertIsNotNone(
            cat._positions_tsv,
            "bundled ocn-1.positions.tsv missing — run tools/sync_package_data.py",
        )

    def test_lookup_is_fast_after_a_warm_load(self) -> None:
        cat = Catalog.load()
        cat.by_fen(SICILIAN_FEN_KEY)  # warm the index

        start = time.perf_counter()
        for _ in range(100):
            cat.by_fen(SICILIAN_FEN_WITH_EP)
        elapsed = time.perf_counter() - start

        self.assertLess(elapsed, 0.5, f"100 warm by_fen calls took {elapsed:.3f}s")


if __name__ == "__main__":
    unittest.main()
