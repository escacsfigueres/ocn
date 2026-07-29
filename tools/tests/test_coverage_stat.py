"""Tests for tools/coverage_stat.py.

The tool is the reproducible script behind the "OCN names X% of real
games" claim, so what is tested here is that the numbers it prints are
the numbers the corpus supports — including the depth table, which is
the part of the report that carries information once the headline rate
saturates near 100%.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent.parent
COVERAGE_STAT = REPO_ROOT / "tools" / "coverage_stat.py"

NAJDORF = (
    '[Event "Deep"]\n[Site "?"]\n[Round "1"]\n[Result "1-0"]\n[ECO "B90"]\n\n'
    "1. e4 c5 2. Nf3 d6 3. d4 cxd4 4. Nxd4 Nf6 5. Nc3 a6 6. Be3 1-0\n\n"
)
SHORT = (
    '[Event "Shallow"]\n[Site "?"]\n[Round "2"]\n[Result "0-1"]\n\n'
    "1. e4 c5 0-1\n\n"
)
NO_MOVES = '[Event "Abandoned"]\n[Site "?"]\n[Round "3"]\n[Result "*"]\n\n*\n\n'


def run_coverage_stat(pgn: str, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(COVERAGE_STAT), *args],
        input=pgn,
        capture_output=True,
        text=True,
        check=False,
    )


class CoverageStatTests(unittest.TestCase):
    def test_json_headline_numbers(self) -> None:
        result = run_coverage_stat(NAJDORF + SHORT + NO_MOVES, "-", "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["games"], 3)
        self.assertEqual(payload["matched"], 2)
        self.assertAlmostEqual(payload["match_rate"], 66.67, places=2)
        self.assertEqual(payload["median_ply"], 6.5)
        self.assertEqual(payload["errors"], 0)
        self.assertEqual(
            sorted(entry["ocn1"] for entry in payload["top"]),
            ["B.Sic", "B.Sic.Naj.Eng"],
        )

    def test_depth_table_counts_deep_matches_only(self) -> None:
        payload = json.loads(run_coverage_stat(NAJDORF + SHORT, "-", "--json").stdout)
        shares = {entry["plies"]: entry["games"] for entry in payload["depth_shares"]}
        self.assertEqual(shares[2], 2)
        self.assertEqual(shares[8], 1)
        self.assertEqual(shares[12], 0)

    def test_text_report_leads_with_the_claim(self) -> None:
        result = run_coverage_stat(NAJDORF + SHORT, "-")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertRegex(result.stdout, r"OCN-1 \(.*rows\) classifies 100\.0% of 2 games")
        self.assertIn("still named at", result.stdout)

    def test_limit_stops_early(self) -> None:
        payload = json.loads(
            run_coverage_stat(NAJDORF * 5, "-", "--json", "--limit", "2").stdout
        )
        self.assertEqual(payload["games"], 2)

    def test_reads_a_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "games.pgn"
            path.write_text(NAJDORF, encoding="utf-8")
            result = run_coverage_stat("", str(path), "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["games"], 1)

    def test_empty_corpus_exits_two(self) -> None:
        result = run_coverage_stat("nothing resembling a game here\n", "-")
        self.assertEqual(result.returncode, 2)
        self.assertIn("no PGN games found", result.stderr)

    def test_missing_file_exits_two(self) -> None:
        result = run_coverage_stat("", "/nonexistent/none.pgn")
        self.assertEqual(result.returncode, 2)
        self.assertIn("ERROR", result.stderr)


if __name__ == "__main__":
    unittest.main()
