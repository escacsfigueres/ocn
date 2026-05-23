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
    "aliases,flags,notes,attributed_to,attribution_source,historical_notes\n"
)


def catalog_row(*fields: str) -> str:
    return ",".join(fields + ("",) * (12 - len(fields))) + "\n"


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
        self.assertEqual(
            rows[0]["fen"],
            "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 1",
        )
        self.assertEqual(rows[0]["transposition_group_size"], "1")

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
