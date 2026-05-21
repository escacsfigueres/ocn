"""Tests for tools/lichess_parent_map.py."""
from __future__ import annotations

import csv
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TOOL = REPO_ROOT / "tools" / "lichess_parent_map.py"
FIXTURES = REPO_ROOT / "tools" / "tests" / "fixtures"


def run_tool(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(TOOL), *args],
        capture_output=True,
        text=True,
        check=False,
    )


class LichessParentMapTests(unittest.TestCase):
    def test_maps_tsv_rows_to_deepest_ocn_parent(self) -> None:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".tsv") as f:
            f.write("eco\tname\tpgn\n")
            f.write("A30\tEnglish Opening: Symmetrical\t1. c4 c5\n")
            f.write(
                "B90\tNajdorf English e5\t"
                "1. e4 c5 2. Nf3 d6 3. d4 cxd4 4. Nxd4 Nf6 "
                "5. Nc3 a6 6. Be3 e5 7. Nb3\n"
            )
            f.flush()
            result = run_tool(f.name)

        self.assertEqual(result.returncode, 0, result.stderr)
        rows = list(csv.DictReader(result.stdout.splitlines(), delimiter="\t"))
        self.assertEqual(rows[0]["parent_ocn1"], "A.Eng.Sym")
        self.assertEqual(rows[1]["parent_ocn1"], "B.Sic.Naj.Eng.e5.Nb3")

    def test_maps_transposed_positions_to_deeper_parent(self) -> None:
        with (
            tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".csv") as catalog,
            tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".tsv") as lichess,
        ):
            catalog.write("ocn1,canonical_name,eco_legacy,parent_ocn1,moves_uci,depth\n")
            catalog.write("D.Root,Queen Pawn,D00,D,d2d4,1\n")
            catalog.write("D.Root.Deep,QGD Structure,D30,D.Root,d2d4 d7d5 c2c4 e7e6,2\n")
            catalog.flush()
            lichess.write("eco\tname\tpgn\n")
            lichess.write("D30\tQGD transposition\t1. d4 e6 2. c4 d5\n")
            lichess.flush()
            result = run_tool("--catalog", catalog.name, lichess.name)

        self.assertEqual(result.returncode, 0, result.stderr)
        rows = list(csv.DictReader(result.stdout.splitlines(), delimiter="\t"))
        self.assertEqual(rows[0]["parent_ocn1"], "D.Root.Deep")
        self.assertEqual(rows[0]["parent_matched_ply"], "4")

    def test_prefix_match_wins_equivalent_transposition_tie(self) -> None:
        with (
            tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".csv") as catalog,
            tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".tsv") as lichess,
        ):
            catalog.write("ocn1,canonical_name,eco_legacy,parent_ocn1,moves_uci,depth\n")
            catalog.write("A.Trans,A move order,A40,A,d2d4 e7e6 c2c4 d7d5,2\n")
            catalog.write("D.Trans,D move order,D30,D,d2d4 d7d5 c2c4 e7e6,2\n")
            catalog.flush()
            lichess.write("eco\tname\tpgn\n")
            lichess.write("A40\tExplicit A order\t1. d4 e6 2. c4 d5\n")
            lichess.flush()
            result = run_tool("--catalog", catalog.name, lichess.name)

        self.assertEqual(result.returncode, 0, result.stderr)
        rows = list(csv.DictReader(result.stdout.splitlines(), delimiter="\t"))
        self.assertEqual(rows[0]["parent_ocn1"], "A.Trans")

    def test_summary_reports_parse_errors(self) -> None:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".tsv") as f:
            f.write("eco\tname\tpgn\n")
            f.write("A00\tBad row\t1. NotAMove\n")
            f.flush()
            result = run_tool("--summary", f.name)

        self.assertEqual(result.returncode, 1)
        self.assertIn("parse_errors=1", result.stdout)
        self.assertIn("Bad row", result.stderr)

    def test_check_passes_when_all_rows_have_parent(self) -> None:
        result = run_tool("--check", str(FIXTURES / "lichess_sample.tsv"))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("unmatched=0 parse_errors=0", result.stdout)

    def test_check_fails_on_unmatched_rows(self) -> None:
        with (
            tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".csv") as catalog,
            tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".tsv") as lichess,
        ):
            catalog.write("ocn1,canonical_name,eco_legacy,parent_ocn1,moves_uci,depth\n")
            catalog.write("A.Eng,English Opening,A10,A,c2c4,1\n")
            catalog.flush()
            lichess.write("eco\tname\tpgn\n")
            lichess.write("A00\tUnknown first move\t1. a3 h5\n")
            lichess.flush()
            result = run_tool("--check", "--catalog", catalog.name, lichess.name)

        self.assertEqual(result.returncode, 1)
        self.assertIn("unmatched=1", result.stdout)
        self.assertIn("coverage check failed", result.stderr)

    def test_quality_reports_depths_and_top_parents(self) -> None:
        result = run_tool("--quality", "--top", "2", str(FIXTURES / "lichess_sample.tsv"))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("by_parent_depth=", result.stdout)
        self.assertIn("top_parents:", result.stdout)
        self.assertIn("A.Eng.Sym", result.stdout)


if __name__ == "__main__":
    unittest.main()
