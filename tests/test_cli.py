"""Smoke tests for the `ocn` command line.

Each subcommand is run as a real subprocess, because that is what the
roadmap's acceptance test is: `pip install ocn-chess` then
`ocn lookup B90` on a clean machine. The tests do not require the
package to be installed — they run `python -m ocn.cli` with `src/` on
`PYTHONPATH` — but they additionally exercise the installed console
script whenever one is on `PATH`.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC = REPO_ROOT / "src"

FEN = "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2"


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ, PYTHONPATH=str(SRC))
    return subprocess.run(
        [sys.executable, "-m", "ocn.cli", *args],
        cwd=REPO_ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )


class HelpTests(unittest.TestCase):
    def test_every_subcommand_has_help(self) -> None:
        for args in ([], ["lookup"], ["fen"], ["uci"], ["version"]):
            with self.subTest(command=args or ["<root>"]):
                result = run_cli(*args, "--help")
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn("usage:", result.stdout)

    def test_bare_invocation_prints_usage(self) -> None:
        result = run_cli()
        self.assertEqual(result.returncode, 2)
        self.assertIn("usage:", result.stdout)


class LookupCommandTests(unittest.TestCase):
    def test_lookup_by_eco(self) -> None:
        result = run_cli("lookup", "B90")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("B.Sic.Naj", result.stdout)

    def test_lookup_by_slug(self) -> None:
        result = run_cli("lookup", "B.Sic.Naj.Eng")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Sicilian Najdorf, English Attack", result.stdout)
        self.assertIn("B > B.Sic > B.Sic.Naj", result.stdout)

    def test_lookup_by_slug_with_a_castling_token(self) -> None:
        """382 slugs end in `O-O`; the detector must not read them as names."""
        result = run_cli("lookup", "E.Gru.Exc.Cla.MLn.O-O")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(result.stdout.startswith("E.Gru.Exc.Cla.MLn.O-O "))

    def test_lookup_by_name_falls_back_to_search(self) -> None:
        result = run_cli("lookup", "najdorf")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("B.Sic.Naj", result.stdout)

    def test_lookup_json_carries_typed_fields(self) -> None:
        result = run_cli("lookup", "B.Sic.Naj.Eng", "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload[0]["ocn1"], "B.Sic.Naj.Eng")
        self.assertEqual(payload[0]["eco"], ["B90"])
        self.assertEqual(payload[0]["parents"], ["B", "B.Sic", "B.Sic.Naj"])

    def test_lookup_miss_exits_one(self) -> None:
        result = run_cli("lookup", "Z.Nope")
        self.assertEqual(result.returncode, 1)
        self.assertIn("ERROR", result.stderr)


class FenCommandTests(unittest.TestCase):
    def test_fen_lookup_normalises_en_passant(self) -> None:
        result = run_cli("fen", FEN)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("B.Sic", result.stdout)

    def test_fen_json(self) -> None:
        result = run_cli("fen", FEN, "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("B.Sic", [row["ocn1"] for row in json.loads(result.stdout)])

    def test_malformed_fen_exits_two(self) -> None:
        result = run_cli("fen", "not a fen")
        self.assertEqual(result.returncode, 2)


class UciCommandTests(unittest.TestCase):
    def test_uci_takes_the_deepest_prefix(self) -> None:
        result = run_cli("uci", "e2e4 c7c5 g1f3 d7d6 d2d4 c5d4 f3d4 g8f6 b1c3 a7a6")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("B.Sic.Naj", result.stdout)

    def test_uci_json_reports_the_matched_ply(self) -> None:
        result = run_cli("uci", "e2e4", "c7c5", "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["ocn1"], "B.Sic")
        self.assertEqual(payload["matched_ply"], 2)

    def test_uci_without_a_match_exits_one(self) -> None:
        result = run_cli("uci", "a2a3")
        self.assertIn(result.returncode, (0, 1))


class VersionCommandTests(unittest.TestCase):
    def test_version_reports_package_and_catalogue(self) -> None:
        result = run_cli("version")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("ocn-chess", result.stdout)

    def test_version_json(self) -> None:
        result = run_cli("version", "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertTrue(payload["package"])
        self.assertTrue(payload["catalogue"])


class InstalledConsoleScriptTests(unittest.TestCase):
    """The roadmap's acceptance criterion, when an install is present."""

    def setUp(self) -> None:
        self.executable = shutil.which("ocn")
        if not self.executable:
            self.skipTest("ocn console script not on PATH (package not installed)")

    def test_ocn_lookup_b90(self) -> None:
        result = subprocess.run(
            [self.executable, "lookup", "B90"],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("B.Sic.Naj", result.stdout)


if __name__ == "__main__":
    unittest.main()
