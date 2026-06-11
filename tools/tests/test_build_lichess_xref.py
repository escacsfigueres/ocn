"""Tests for tools/build_lichess_xref.py.

The xref builder maps every OCN-1 row to its Lichess label by SAN
sequence (exact match, else longest prefix) against the snapshot
vendored in external/lichess-openings/, and emits the committed sidecar
catalog/ocn-1.lichess-xref.tsv. A drift test pins the committed sidecar
to a fresh rebuild; coverage thresholds ratchet so regressions fail CI.

Run:
    python3 -m unittest tools.tests.test_build_lichess_xref
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools"))

from build_lichess_xref import (  # noqa: E402
    build_xref_rows,
    match_sans,
    render_tsv,
    san_sequence,
)

TINY_INDEX = {
    ("e4",): ("B00", "King's Pawn Game"),
    ("e4", "c5"): ("B20", "Sicilian Defense"),
    ("e4", "c5", "Nf3"): ("B27", "Sicilian Defense: Old Sicilian"),
}


def _row(ocn1: str, moves: str, depth: str) -> dict[str, str]:
    return {"ocn1": ocn1, "moves_uci": moves, "depth": depth}


class MatchTests(unittest.TestCase):
    def test_exact_match(self) -> None:
        kind, plies, eco, name = match_sans(["e4", "c5"], TINY_INDEX)
        self.assertEqual(
            (kind, plies, eco, name),
            ("exact", 2, "B20", "Sicilian Defense"),
        )

    def test_longest_prefix_match(self) -> None:
        kind, plies, eco, name = match_sans(
            ["e4", "c5", "Nf3", "d6", "d4"], TINY_INDEX
        )
        self.assertEqual(kind, "prefix")
        self.assertEqual(plies, 3)
        self.assertEqual(eco, "B27")

    def test_no_match(self) -> None:
        kind, plies, eco, name = match_sans(["d4"], TINY_INDEX)
        self.assertEqual((kind, plies, eco, name), ("none", 0, "", ""))


class SanSequenceTests(unittest.TestCase):
    def test_uci_to_san(self) -> None:
        self.assertEqual(
            san_sequence("e2e4 c7c5 g1f3"), ["e4", "c5", "Nf3"]
        )

    def test_checks_are_stripped(self) -> None:
        # 1.d4 e5 2.dxe5 Bb4+ — SAN check suffix must not break matching
        # against Lichess pgn tokens (which carry them inconsistently
        # relative to our derivation).
        sans = san_sequence("d2d4 e7e5 d4e5 f8b4")
        self.assertEqual(sans[-1], "Bb4")


class BuildRowsTests(unittest.TestCase):
    def test_class_roots_marked_root(self) -> None:
        rows = build_xref_rows([_row("A", "", "0")], TINY_INDEX)
        self.assertEqual(rows[0], ("A", "root", 0, 0, "", ""))

    def test_concrete_rows_matched_in_catalog_order(self) -> None:
        rows = build_xref_rows(
            [
                _row("B", "", "0"),
                _row("B.Sic", "e2e4 c7c5", "1"),
                _row("D.QPG", "d2d4 d7d5", "1"),
            ],
            TINY_INDEX,
        )
        self.assertEqual([r[0] for r in rows], ["B", "B.Sic", "D.QPG"])
        self.assertEqual(rows[1][1], "exact")
        self.assertEqual(rows[2][1], "none")  # no d4 line in the tiny index
        self.assertEqual(rows[2][2], 0)


class AliasCandidateTests(unittest.TestCase):
    def test_candidates_are_position_keyed(self) -> None:
        """A Lichess line whose exact sequence exists in OCN but whose
        name is absent from that row's canonical+aliases is an alias
        candidate ON that row; name-present lines are not; lines with no
        OCN row at the sequence are position-uncovered, not candidates."""
        from build_lichess_xref import alias_candidates

        catalog = [
            {"ocn1": "B.Sic", "moves_uci": "e2e4 c7c5", "depth": "1",
             "canonical_name": "Sicilian Defence", "aliases": ""},
            {"ocn1": "C.KPO", "moves_uci": "e2e4 e7e5", "depth": "1",
             "canonical_name": "King's Pawn Game", "aliases": ""},
        ]
        index = {
            ("e4", "c5"): ("B20", "Sicilian Defense"),
            ("e4", "e5"): ("C20", "King's Pawn Game"),
            ("d4", "d5"): ("D00", "Queen's Pawn Game"),
        }
        cands, uncovered = alias_candidates(catalog, index)
        # Sicilian Defense differs only by spelling fold -> NOT a candidate.
        # King's Pawn Game is already the canonical -> NOT a candidate.
        self.assertEqual(cands, [])
        self.assertEqual(uncovered, [("D00", "Queen's Pawn Game")])

    def test_genuinely_new_label_is_a_candidate(self) -> None:
        from build_lichess_xref import alias_candidates

        catalog = [
            {"ocn1": "B.Sic", "moves_uci": "e2e4 c7c5", "depth": "1",
             "canonical_name": "Sicilian Defence", "aliases": ""},
        ]
        index = {("e4", "c5"): ("B20", "Sicilian Defense: Old Sicilian")}
        cands, uncovered = alias_candidates(catalog, index)
        self.assertEqual(
            cands,
            [("B.Sic", "B20", "Sicilian Defense: Old Sicilian")],
        )
        self.assertEqual(uncovered, [])

    def test_phantom_collision_prefers_shallowest_row(self) -> None:
        from build_lichess_xref import alias_candidates

        catalog = [
            {"ocn1": "A.Tro.Bxf6", "moves_uci": "d2d4 g8f6 c1g5",
             "depth": "2", "canonical_name": "Tromp Bxf6", "aliases": ""},
            {"ocn1": "A.Tro", "moves_uci": "d2d4 g8f6 c1g5", "depth": "1",
             "canonical_name": "Trompowsky Attack", "aliases": ""},
        ]
        index = {("d4", "Nf6", "Bg5"): ("A45", "Trompowsky Niche Line")}
        cands, _ = alias_candidates(catalog, index)
        self.assertEqual(cands, [("A.Tro", "A45", "Trompowsky Niche Line")])


class RenderTests(unittest.TestCase):
    def test_tsv_shape(self) -> None:
        text = render_tsv([("B.Sic", "exact", 2, 2, "B20", "Sicilian Defense")])
        lines = text.splitlines()
        self.assertEqual(
            lines[0],
            "ocn1\tmatch_kind\tmatched_plies\ttotal_plies\tlichess_eco\tlichess_name",
        )
        self.assertEqual(
            lines[1], "B.Sic\texact\t2\t2\tB20\tSicilian Defense"
        )


class SidecarDriftTests(unittest.TestCase):
    SIDECAR = REPO_ROOT / "catalog" / "ocn-1.lichess-xref.tsv"

    def test_committed_sidecar_is_current(self) -> None:
        """The committed sidecar must equal a fresh rebuild from the
        vendored snapshot — catalogue or snapshot changes without a
        sidecar regen fail here."""
        from build_lichess_xref import build_from_repo

        self.assertTrue(self.SIDECAR.exists(), "sidecar not committed")
        fresh = build_from_repo()
        self.assertEqual(
            self.SIDECAR.read_text(encoding="utf-8"), fresh,
            "catalog/ocn-1.lichess-xref.tsv is stale — regenerate with "
            "tools/build_lichess_xref.py",
        )

    def test_coverage_thresholds(self) -> None:
        """Ratchet: exact+prefix coverage of concrete rows must not
        regress below the level measured at introduction."""
        import csv

        with self.SIDECAR.open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f, delimiter="\t"))
        concrete = [r for r in rows if r["match_kind"] != "root"]
        self.assertEqual(len(rows), 5899)
        matched = sum(
            1 for r in concrete if r["match_kind"] in ("exact", "prefix")
        )
        exact = sum(1 for r in concrete if r["match_kind"] == "exact")
        self.assertGreaterEqual(matched / len(concrete), 0.999)
        self.assertGreaterEqual(exact / len(concrete), 0.50)

    def test_lichess_position_coverage_ratchet(self) -> None:
        """Lichess→OCN position coverage measured 89.8% (375 uncovered)
        at introduction — it must not regress."""
        import csv as _csv

        from build_lichess_xref import (
            DEFAULT_CATALOG,
            DEFAULT_LICHESS_DIR,
            alias_candidates,
            load_lichess_index,
        )

        with DEFAULT_CATALOG.open(newline="", encoding="utf-8") as f:
            rows = list(_csv.DictReader(f))
        _, uncovered = alias_candidates(
            rows, load_lichess_index(DEFAULT_LICHESS_DIR)
        )
        self.assertLessEqual(len(uncovered), 375)


if __name__ == "__main__":
    unittest.main()
