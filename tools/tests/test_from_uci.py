"""Tests for tools/from_uci.py."""
from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent.parent
FROM_UCI = REPO_ROOT / "tools" / "from_uci.py"


def run_from_uci(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(FROM_UCI), *args],
        capture_output=True,
        text=True,
        check=False,
    )


class FromUciTests(unittest.TestCase):
    def test_exact_match_returns_slug(self) -> None:
        result = run_from_uci("c2c4", "c7c5")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(result.stdout.startswith("A.Eng.Sym\t"), result.stdout)

    def test_longer_sequence_returns_deepest_catalogue_prefix(self) -> None:
        result = run_from_uci(
            "e2e4", "c7c5", "g1f3", "d7d6", "d2d4", "c5d4",
            "f3d4", "g8f6", "b1c3", "a7a6", "c1e3", "e7e5",
            "d4b3",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(result.stdout.startswith("B.Sic.Naj.Eng.e5.Nb3\t"), result.stdout)

    def test_json_output(self) -> None:
        result = run_from_uci("--json", "e2e4", "c7c6")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('"ocn1": "B.CaK"', result.stdout)

    def test_illegal_sequence_fails(self) -> None:
        result = run_from_uci("e2e5")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("illegal UCI move", result.stderr)

    def test_unmatched_legal_sequence_fails(self) -> None:
        result = run_from_uci("e2e4")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("no OCN-1 match", result.stderr)


if __name__ == "__main__":
    unittest.main()
