"""Tests for tools/audit_transpositions.py."""
from __future__ import annotations

import csv
import json
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
AUDIT_TOOL = REPO_ROOT / "tools" / "audit_transpositions.py"


HEADER = (
    "ocn1,canonical_name,eco_legacy,parent_ocn1,moves_uci,depth,"
    "aliases,flags,notes,attributed_to,attribution_source,historical_notes\n"
)


def catalog_row(*fields: str) -> str:
    return ",".join(fields + ("",) * (12 - len(fields))) + "\n"


def run_audit(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["python3", str(AUDIT_TOOL), *args],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


class AuditTranspositionsTests(unittest.TestCase):
    def _write_catalog(self, tmp: str, rows: str) -> Path:
        catalog = Path(tmp) / "catalog.csv"
        catalog.write_text(HEADER + rows, encoding="utf-8")
        return catalog

    def test_no_duplicates_returns_empty_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            catalog = self._write_catalog(
                tmp,
                catalog_row("A", "Flank Openings", "A", "", "", "0")
                + catalog_row("B", "Semi-Open Games", "B", "", "", "0")
                + catalog_row("B.Sic", "Sicilian Defence", "B20", "B", "e2e4 c7c5", "1"),
            )

            result = run_audit("--catalog", str(catalog), "--summary")

        self.assertEqual(result.returncode, 0, result.stderr)
        rows = list(csv.DictReader(result.stdout.splitlines(), delimiter="\t"))
        self.assertEqual(rows, [])
        self.assertIn("duplicate_groups=0", result.stderr)

    def test_reports_transposition_group(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            catalog = self._write_catalog(
                tmp,
                catalog_row("A", "Flank Openings", "A", "", "", "0")
                + catalog_row("D", "Closed Queen's Pawn", "D", "", "", "0")
                + catalog_row("A.Tr1", "Transposition One", "A", "A", "d2d4 g8f6 c2c4 e7e6", "1")
                + catalog_row("D.Tr2", "Transposition Two", "D", "D", "c2c4 g8f6 d2d4 e7e6", "1"),
            )

            result = run_audit("--catalog", str(catalog))

        self.assertEqual(result.returncode, 0, result.stderr)
        rows = list(csv.DictReader(result.stdout.splitlines(), delimiter="\t"))
        self.assertEqual(len(rows), 2)
        slugs = sorted(row["ocn1"] for row in rows)
        self.assertEqual(slugs, ["A.Tr1", "D.Tr2"])
        self.assertEqual({row["group_size"] for row in rows}, {"2"})
        self.assertEqual({row["classes"] for row in rows}, {"A,D"})
        self.assertEqual({row["fen_key"] for row in rows}, {rows[0]["fen_key"]})

    def test_json_output_is_structured_groups(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            catalog = self._write_catalog(
                tmp,
                catalog_row("A", "Flank Openings", "A", "", "", "0")
                + catalog_row("D", "Closed Queen's Pawn", "D", "", "", "0")
                + catalog_row("A.Tr1", "Transposition One", "A", "A", "d2d4 g8f6 c2c4 e7e6", "1")
                + catalog_row("D.Tr2", "Transposition Two", "D", "D", "c2c4 g8f6 d2d4 e7e6", "1"),
            )

            result = run_audit("--catalog", str(catalog), "--json")

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertIn("groups", payload)
        self.assertEqual(len(payload["groups"]), 1)
        group = payload["groups"][0]
        self.assertEqual(group["group_size"], 2)
        self.assertEqual(group["classes"], ["A", "D"])
        self.assertEqual(len(group["entries"]), 2)
        self.assertEqual(
            sorted(entry["ocn1"] for entry in group["entries"]),
            ["A.Tr1", "D.Tr2"],
        )

    def test_min_size_filters_out_small_groups(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            catalog = self._write_catalog(
                tmp,
                catalog_row("A", "Flank Openings", "A", "", "", "0")
                + catalog_row("D", "Closed Queen's Pawn", "D", "", "", "0")
                + catalog_row("A.Tr1", "Transposition One", "A", "A", "d2d4 g8f6 c2c4 e7e6", "1")
                + catalog_row("D.Tr2", "Transposition Two", "D", "D", "c2c4 g8f6 d2d4 e7e6", "1"),
            )

            result = run_audit("--catalog", str(catalog), "--min-size", "3", "--summary")

        self.assertEqual(result.returncode, 0, result.stderr)
        rows = list(csv.DictReader(result.stdout.splitlines(), delimiter="\t"))
        self.assertEqual(rows, [])
        self.assertIn("duplicate_groups=0", result.stderr)

    def test_class_filter_keeps_matching_groups(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            catalog = self._write_catalog(
                tmp,
                catalog_row("A", "Flank Openings", "A", "", "", "0")
                + catalog_row("D", "Closed Queen's Pawn", "D", "", "", "0")
                + catalog_row("E", "Indian Defences", "E", "", "", "0")
                + catalog_row("A.Tr1", "AD Trans One", "A", "A", "d2d4 g8f6 c2c4 e7e6", "1")
                + catalog_row("D.Tr2", "AD Trans Two", "D", "D", "c2c4 g8f6 d2d4 e7e6", "1")
                + catalog_row("E.Tr1", "E Trans One", "E", "E", "d2d4 g8f6 c2c4 g7g6", "1")
                + catalog_row(
                    "E.Tr2", "E Trans Two", "E", "E", "c2c4 g8f6 d2d4 g7g6", "1"
                ),
            )

            result = run_audit("--catalog", str(catalog), "--class", "E", "--summary")

        self.assertEqual(result.returncode, 0, result.stderr)
        rows = list(csv.DictReader(result.stdout.splitlines(), delimiter="\t"))
        self.assertEqual(sorted(row["ocn1"] for row in rows), ["E.Tr1", "E.Tr2"])
        self.assertIn("duplicate_groups=1", result.stderr)

    def test_invalid_min_size_errors(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            catalog = self._write_catalog(tmp, "")
            result = run_audit("--catalog", str(catalog), "--min-size", "1")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("ERROR", result.stderr)


if __name__ == "__main__":
    unittest.main()
