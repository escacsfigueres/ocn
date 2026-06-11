"""Tests for tools/from_position.py."""
from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent.parent
FROM_POSITION = REPO_ROOT / "tools" / "from_position.py"


def run_from_position(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(FROM_POSITION), *args],
        capture_output=True,
        text=True,
        check=False,
    )


class FromPositionTests(unittest.TestCase):
    def test_exact_fen_returns_slug(self) -> None:
        result = run_from_position(
            "rnbqkbnr/pp1ppppp/8/2p5/2P5/8/PP1PPPPP/RNBQKBNR w KQkq c6 0 2"
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(result.stdout.startswith("A.Eng.Sym\t"), result.stdout)

    def test_four_field_fen_is_supported(self) -> None:
        result = run_from_position(
            "rnbqkbnr/pp2pppp/2p5/3p4/2PP4/8/PP2PPPP/RNBQKBNR w KQkq -"
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(result.stdout.startswith("D.Sla\t"), result.stdout)

    def test_json_output(self) -> None:
        result = run_from_position(
            "--json",
            "rnbqkbnr/pp2pppp/2p5/3p4/2PP4/8/PP2PPPP/RNBQKBNR w KQkq -",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload[0]["ocn1"], "D.Sla")

    def test_unmatched_position_fails(self) -> None:
        result = run_from_position(
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("no OCN-1 match", result.stderr)

    def test_invalid_fen_fails(self) -> None:
        result = run_from_position("not-a-fen")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("expected FEN", result.stderr)


class CoCanonicalTests(unittest.TestCase):
    """same_as partners are all canonical and must be returned together."""

    def fen_of(self, slug: str) -> str:
        import csv
        sys.path.insert(0, str(REPO_ROOT / "tools"))
        from chess_uci import fen_key_after_uci  # noqa: E402
        with (REPO_ROOT / "catalog" / "ocn-1.csv").open(
            newline="", encoding="utf-8"
        ) as f:
            rows = {r["ocn1"]: r for r in csv.DictReader(f)}
        return fen_key_after_uci(rows[slug]["moves_uci"])

    def test_depth_mismatched_co_canonical_pair_returned_together(self) -> None:
        # D.Rub (depth 1) and A.Col.Zuk (depth 2) are bilateral same_as
        # co-canonicals; the shallower one must not be silently dropped.
        result = run_from_position(self.fen_of("D.Rub"))
        self.assertEqual(result.returncode, 0, result.stderr)
        slugs = [line.split("\t")[0] for line in result.stdout.splitlines()]
        self.assertIn("A.Col.Zuk", slugs)
        self.assertIn("D.Rub", slugs)

    def test_same_depth_co_canonical_pair_is_not_ambiguous(self) -> None:
        # E.KID.Fch.Uhl and E.KID.Fch.Sim share depth and FEN via same_as;
        # the co-canonical contract says return both, not "ambiguous".
        result = run_from_position(self.fen_of("E.KID.Fch.Uhl"))
        self.assertEqual(result.returncode, 0, result.stderr)
        slugs = [line.split("\t")[0] for line in result.stdout.splitlines()]
        self.assertEqual(sorted(slugs), ["E.KID.Fch.Sim", "E.KID.Fch.Uhl"])


if __name__ == "__main__":
    unittest.main()
