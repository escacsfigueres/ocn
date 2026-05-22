"""Tests for tools/from_eco.py."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent.parent
FROM_ECO = REPO_ROOT / "tools" / "from_eco.py"


def run_from_eco(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(FROM_ECO), *args],
        capture_output=True,
        text=True,
        check=False,
    )


class FromEcoTests(unittest.TestCase):
    def test_unique_deepest_match_returns_slug(self) -> None:
        result = run_from_eco("A04")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(
            result.stdout.startswith("A.Ret.Lis.Nf6.d4.d5\t"),
            result.stdout,
        )

    def test_pgn_file_eco_tag_is_supported(self) -> None:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".pgn") as f:
            f.write('[Event "OCN smoke"]\n[ECO "A11"]\n\n1. c4 *\n')
            f.flush()
            result = run_from_eco(f.name)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(
            result.stdout.startswith("A.KIA.Bg2.c6.O-O.Bf5.d3\t"),
            result.stdout,
        )

    def test_inline_pgn_eco_tag_is_supported(self) -> None:
        result = run_from_eco('[ECO "A11"]', "1.", "c4", "*")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(
            result.stdout.startswith("A.KIA.Bg2.c6.O-O.Bf5.d3\t"),
            result.stdout,
        )

    def test_ambiguous_code_fails_without_all(self) -> None:
        result = run_from_eco("B90")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("ambiguous", result.stderr)
        self.assertIn("tools/from_uci.py", result.stderr)

    def test_all_lists_ambiguous_candidates(self) -> None:
        result = run_from_eco("--all", "B90")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("B.Sic.Naj.Eng.MLn.f3.Nbd7\t", result.stdout)
        self.assertIn("B.Sic.Naj.Eng.e5.Nb3.Be6\t", result.stdout)

    def test_json_output(self) -> None:
        result = run_from_eco("--json", "A11")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload[0]["ocn1"], "A.KIA.Bg2.c6.O-O.Bf5.d3")

    def test_invalid_eco_fails(self) -> None:
        result = run_from_eco("Z99")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("not a valid ECO code", result.stderr)


if __name__ == "__main__":
    unittest.main()
