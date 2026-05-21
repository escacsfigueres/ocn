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

    def test_summary_reports_parse_errors(self) -> None:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".tsv") as f:
            f.write("eco\tname\tpgn\n")
            f.write("A00\tBad row\t1. NotAMove\n")
            f.flush()
            result = run_tool("--summary", f.name)

        self.assertEqual(result.returncode, 1)
        self.assertIn("parse_errors=1", result.stdout)
        self.assertIn("Bad row", result.stderr)


if __name__ == "__main__":
    unittest.main()
