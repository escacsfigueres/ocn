"""Tests for tools/export_positions.py.

The positions sidecar is the artefact that lets a consumer use OCN by
position without owning a chess engine, so what is pinned here is the
whole derived contract: the column list *and its order* (H2.8 appended
`san`, `epd` and `zobrist` rather than reshuffling, because awk and
spreadsheet consumers read by index), the true halfmove/fullmove
counters, and the values of each derived column on lines small enough to
verify by hand.

The Polyglot hash itself is gated in `test_polyglot_zobrist.py` against
the published book-format vectors; here it is only checked that the
column carries that number, as unsigned decimal, for the right row.
"""
from __future__ import annotations

import csv
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from tools.export_positions import FIELDS, replay
from tools.polyglot_zobrist import polyglot_hash_after_uci


REPO_ROOT = Path(__file__).resolve().parents[2]
EXPORT_POSITIONS = REPO_ROOT / "tools" / "export_positions.py"


HEADER = (
    "ocn1,canonical_name,eco_legacy,parent_ocn1,moves_uci,depth,"
    "aliases,flags,notes,attributed_to,attribution_source,historical_notes,"
    "transposes_to,same_as\n"
)


def catalog_row(*fields: str) -> str:
    return ",".join(fields + ("",) * (14 - len(fields))) + "\n"


def run_export(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["python3", str(EXPORT_POSITIONS), *args],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


class ExportPositionsTests(unittest.TestCase):
    def test_exports_fen_for_concrete_rows(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            catalog = Path(tmp) / "catalog.csv"
            catalog.write_text(
                HEADER
                + catalog_row("A", "Other Openings", "A", "", "", "0")
                + catalog_row("B.Sic", "Sicilian Defence", "B20", "B", "e2e4 c7c5", "1"),
                encoding="utf-8",
            )

            result = run_export("--catalog", str(catalog))

        self.assertEqual(result.returncode, 0, result.stderr)
        rows = list(csv.DictReader(result.stdout.splitlines(), delimiter="\t"))
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["ocn1"], "B.Sic")
        self.assertEqual(
            rows[0]["fen_key"],
            "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq -",
        )
        # Two plies, both pawn moves: halfmove clock 0, fullmove 2. The
        # column used to emit a placeholder `0 1` for every row.
        self.assertEqual(
            rows[0]["fen"],
            "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2",
        )
        self.assertEqual(rows[0]["transposition_group_size"], "1")

    def test_counters_track_captures_and_quiet_moves(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            catalog = Path(tmp) / "catalog.csv"
            catalog.write_text(
                HEADER
                + catalog_row("A", "Other Openings", "A", "", "", "0")
                # 1.e4 c5 2.Nf3 d6 3.d4 cxd4 4.Nxd4 Nf6 5.Nc3 a6 6.Be3:
                # eleven plies, last capture on ply 7, last pawn move on
                # ply 10 -> halfmove 1, fullmove 11 // 2 + 1 = 6.
                + catalog_row(
                    "B.Sic.Naj.Eng",
                    "Sicilian Najdorf English Attack",
                    "B90",
                    "A",
                    "e2e4 c7c5 g1f3 d7d6 d2d4 c5d4 f3d4 g8f6 b1c3 a7a6 c1e3",
                    "1",
                ),
                encoding="utf-8",
            )

            result = run_export("--catalog", str(catalog))

        self.assertEqual(result.returncode, 0, result.stderr)
        row = list(csv.DictReader(result.stdout.splitlines(), delimiter="\t"))[0]
        self.assertEqual(row["fen"], f"{row['fen_key']} 1 6")

    def test_quiet_moves_accumulate_the_halfmove_clock(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            catalog = Path(tmp) / "catalog.csv"
            catalog.write_text(
                HEADER
                + catalog_row("A", "Other Openings", "A", "", "", "0")
                # 1.Nf3 Nf6 2.Ng1 Ng8: four quiet moves, no pawn moved.
                + catalog_row(
                    "A.Zzz", "Shuffle", "A00", "A", "g1f3 g8f6 f3g1 f6g8", "1"
                ),
                encoding="utf-8",
            )

            result = run_export("--catalog", str(catalog))

        self.assertEqual(result.returncode, 0, result.stderr)
        row = list(csv.DictReader(result.stdout.splitlines(), delimiter="\t"))[0]
        self.assertEqual(row["fen"], f"{row['fen_key']} 4 3")

    def test_include_roots_keeps_blank_position_fields(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            catalog = Path(tmp) / "catalog.csv"
            catalog.write_text(
                HEADER
                + catalog_row("A", "Other Openings", "A", "", "", "0")
                + catalog_row("B.Sic", "Sicilian Defence", "B20", "B", "e2e4 c7c5", "1"),
                encoding="utf-8",
            )

            result = run_export("--catalog", str(catalog), "--include-roots")

        self.assertEqual(result.returncode, 0, result.stderr)
        rows = list(csv.DictReader(result.stdout.splitlines(), delimiter="\t"))
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["ocn1"], "A")
        # A class root is a filter, not a position: every derived column is
        # blank, including the three H2.8 added.
        for field in ("fen_key", "fen", "san", "epd", "zobrist"):
            self.assertEqual(rows[0][field], "", field)

    def test_marks_transposition_group_size(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            catalog = Path(tmp) / "catalog.csv"
            catalog.write_text(
                HEADER
                + catalog_row("A", "Other Openings", "A", "", "", "0")
                + catalog_row("A.Tr1", "Transposition One", "A", "A", "d2d4 g8f6 c2c4 e7e6", "1")
                + catalog_row("A.Tr2", "Transposition Two", "A", "A", "c2c4 g8f6 d2d4 e7e6", "1"),
                encoding="utf-8",
            )

            result = run_export("--catalog", str(catalog), "--format", "json")

        self.assertEqual(result.returncode, 0, result.stderr)
        rows = json.loads(result.stdout)
        self.assertEqual({row["transposition_group_size"] for row in rows}, {"2"})


class ColumnContractTests(unittest.TestCase):
    """The header is a contract: old columns keep their index, new ones append."""

    #: The 1.2.0 sidecar, verbatim. Nothing in this tuple may move.
    LEGACY_FIELDS = (
        "ocn1",
        "canonical_name",
        "eco_legacy",
        "parent_ocn1",
        "depth",
        "moves_uci",
        "fen_key",
        "fen",
        "transposition_group_size",
        "transposes_to",
        "same_as",
    )

    def test_legacy_columns_keep_their_positions(self) -> None:
        self.assertEqual(tuple(FIELDS[: len(self.LEGACY_FIELDS)]), self.LEGACY_FIELDS)

    def test_h28_columns_are_appended_in_order(self) -> None:
        self.assertEqual(FIELDS[len(self.LEGACY_FIELDS):], ["san", "epd", "zobrist"])

    def test_emitted_header_matches_the_declared_fields(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            catalog = Path(tmp) / "catalog.csv"
            catalog.write_text(
                HEADER
                + catalog_row("A", "Other Openings", "A", "", "", "0")
                + catalog_row("B.Sic", "Sicilian Defence", "B20", "B", "e2e4 c7c5", "1"),
                encoding="utf-8",
            )

            result = run_export("--catalog", str(catalog))

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.splitlines()[0].split("\t"), FIELDS)


class DerivedColumnTests(unittest.TestCase):
    """`san`, `epd` and `zobrist` on lines small enough to check by hand."""

    NAJDORF_ENGLISH = "e2e4 c7c5 g1f3 d7d6 d2d4 c5d4 f3d4 g8f6 b1c3 a7a6 c1e3"

    def test_san_is_numbered_movetext(self) -> None:
        self.assertEqual(replay("e2e4 c7c5 g1f3").san, "1.e4 c5 2.Nf3")

    def test_san_renders_captures_castling_and_promotion(self) -> None:
        # 1.e4 e5 2.Nf3 Nc6 3.Bb5 a6 4.O-O: the SAN forms most likely to
        # be mangled by a naive renderer.
        self.assertEqual(
            replay("e2e4 e7e5 g1f3 b8c6 f1b5 a7a6 e1g1").san,
            "1.e4 e5 2.Nf3 Nc6 3.Bb5 a6 4.O-O",
        )

    def test_san_is_empty_for_an_empty_line(self) -> None:
        self.assertEqual(replay("").san, "")

    def test_epd_is_the_four_field_position(self) -> None:
        position = replay("e2e4 c7c5")
        self.assertEqual(
            position.epd,
            "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq -",
        )
        self.assertEqual(len(position.epd.split()), 4)
        # No counters, and no EPD operations: a bare four-field record.
        self.assertNotIn(";", position.epd)

    def test_epd_and_fen_key_coincide_by_construction(self) -> None:
        # Annex A normalises en passant to the legal-capture form, which is
        # the form EPD wants, so the two strings are the same string. The
        # column exists for tools that expect the name, not because the
        # value differs -- pinned so a future divergence is deliberate.
        for moves_uci in ("e2e4 c7c5", "e2e4 d7d5 e4e5 f7f5", "d2d4 g8f6 c2c4"):
            with self.subTest(moves=moves_uci):
                position = replay(moves_uci)
                self.assertEqual(position.epd, position.fen_key)

    def test_zobrist_is_the_polyglot_hash_as_unsigned_decimal(self) -> None:
        position = replay(self.NAJDORF_ENGLISH)
        self.assertEqual(
            position.zobrist, str(polyglot_hash_after_uci(self.NAJDORF_ENGLISH))
        )
        self.assertTrue(position.zobrist.isdigit())
        self.assertLess(int(position.zobrist), 1 << 64)

    def test_zobrist_matches_the_published_initial_position_key(self) -> None:
        # The one value any reader can check against the book format.
        self.assertEqual(replay("").zobrist, "5060803636482931868")

    def test_transpositions_share_fen_key_and_zobrist(self) -> None:
        # Two move orders, one position: both derived keys must agree, or
        # the sidecar would report a transposition group the hash denies.
        first = replay("d2d4 g8f6 c2c4 e7e6")
        second = replay("c2c4 g8f6 d2d4 e7e6")
        self.assertEqual(first.fen_key, second.fen_key)
        self.assertEqual(first.zobrist, second.zobrist)
        self.assertNotEqual(first.san, second.san)

    def test_columns_reach_the_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            catalog = Path(tmp) / "catalog.csv"
            catalog.write_text(
                HEADER
                + catalog_row("A", "Other Openings", "A", "", "", "0")
                + catalog_row(
                    # `catalog_row` joins on commas, so no comma in the name.
                    "B.Sic.Naj.Eng",
                    "Sicilian Najdorf English Attack",
                    "B90",
                    "A",
                    self.NAJDORF_ENGLISH,
                    "3",
                ),
                encoding="utf-8",
            )

            result = run_export("--catalog", str(catalog))

        self.assertEqual(result.returncode, 0, result.stderr)
        row = list(csv.DictReader(result.stdout.splitlines(), delimiter="\t"))[0]
        self.assertEqual(
            row["san"], "1.e4 c5 2.Nf3 d6 3.d4 cxd4 4.Nxd4 Nf6 5.Nc3 a6 6.Be3"
        )
        self.assertEqual(
            row["epd"],
            "rnbqkb1r/1p2pppp/p2p1n2/8/3NP3/2N1B3/PPP2PPP/R2QKB1R b KQkq -",
        )
        self.assertEqual(row["zobrist"], "8839051919898350604")


if __name__ == "__main__":
    unittest.main()
