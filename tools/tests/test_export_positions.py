"""Tests for tools/export_positions.py."""
from __future__ import annotations

import csv
import json
import subprocess
import tempfile
import unittest
from pathlib import Path


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
        self.assertEqual(rows[0]["fen_key"], "")
        self.assertEqual(rows[0]["fen"], "")

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


if __name__ == "__main__":
    unittest.main()
