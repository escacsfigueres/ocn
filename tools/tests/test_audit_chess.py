"""Tests for tools/audit_chess.py."""
from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TOOL = REPO_ROOT / "tools" / "audit_chess.py"
FIXTURES = Path(__file__).resolve().parent / "fixtures"


def run_tool(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(TOOL), *args],
        capture_output=True,
        text=True,
        check=False,
    )


class AuditChessTests(unittest.TestCase):
    def test_missing_catalogue_fails_cleanly(self) -> None:
        result = run_tool("/nonexistent/path/ocn-1.csv")
        self.assertEqual(result.returncode, 1)
        self.assertIn("ERROR", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_valid_fixture_passes(self) -> None:
        result = run_tool(str(FIXTURES / "valid_minimal.csv"))
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
