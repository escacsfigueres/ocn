"""Tests for tools/candidate_slice_export.py.

Exports a review slice of catalogue rows for an evidence sprint: explicit slugs
(or all rows) narrowed by --eco-prefix / --empty-attribution filters, in
deterministic catalogue order.
"""
from __future__ import annotations

import csv
import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TOOLS = REPO_ROOT / "tools"
TOOL = TOOLS / "candidate_slice_export.py"
FIXTURES = Path(__file__).resolve().parent / "fixtures"
BASE = FIXTURES / "apply_manifest_base.csv"  # rows: A, A.Tro(attr), B, B.Fre, B.Fre.Win


def run_tool(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, str(TOOL), "--catalog", str(BASE), *args],
                          capture_output=True, text=True, check=False)


def rows_from_csv(text: str) -> list[dict]:
    return list(csv.DictReader(io.StringIO(text)))


class SliceTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)

    def test_single_slug(self) -> None:
        r = run_tool("--ocn1", "A.Tro")
        self.assertEqual(r.returncode, 0, r.stderr)
        rows = rows_from_csv(r.stdout)
        self.assertEqual([x["ocn1"] for x in rows], ["A.Tro"])
        self.assertEqual(len(rows[0]), 9)  # default 9 columns

    def test_repeated_slug_deduplicated(self) -> None:
        r = run_tool("--ocn1", "A.Tro", "--ocn1", "A.Tro")
        self.assertEqual([x["ocn1"] for x in rows_from_csv(r.stdout)], ["A.Tro"])

    def test_output_is_catalogue_order_not_input_order(self) -> None:
        r = run_tool("--ocn1", "B.Fre.Win", "--ocn1", "A.Tro", "--ocn1", "A")
        self.assertEqual([x["ocn1"] for x in rows_from_csv(r.stdout)],
                         ["A", "A.Tro", "B.Fre.Win"])

    def test_ocn1_file_skips_blanks_and_comments(self) -> None:
        f = self.tmp / "slugs.txt"
        f.write_text("# a comment\nA.Tro\n\n  \nB.Fre\n", encoding="utf-8")
        r = run_tool("--ocn1-file", str(f))
        self.assertEqual([x["ocn1"] for x in rows_from_csv(r.stdout)], ["A.Tro", "B.Fre"])

    def test_empty_attribution_filter(self) -> None:
        r = run_tool("--empty-attribution")
        slugs = [x["ocn1"] for x in rows_from_csv(r.stdout)]
        self.assertNotIn("A.Tro", slugs)        # A.Tro is attributed
        self.assertEqual(slugs, ["A", "B", "B.Fre", "B.Fre.Win"])

    def test_eco_prefix_filter(self) -> None:
        r = run_tool("--eco-prefix", "A")
        self.assertEqual([x["ocn1"] for x in rows_from_csv(r.stdout)], ["A", "A.Tro"])

    def test_eco_prefix_and_empty_attribution_combine_as_and(self) -> None:
        r = run_tool("--eco-prefix", "A", "--empty-attribution")
        self.assertEqual([x["ocn1"] for x in rows_from_csv(r.stdout)], ["A"])

    def test_missing_slug_rejected(self) -> None:
        r = run_tool("--ocn1", "Z.Nope")
        self.assertEqual(r.returncode, 1)
        self.assertIn("ERROR", r.stderr)
        self.assertIn("Z.Nope", r.stderr)

    def test_missing_slug_allowed_warns(self) -> None:
        r = run_tool("--ocn1", "A.Tro", "--ocn1", "Z.Nope", "--allow-missing")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("WARN", r.stderr)
        self.assertEqual([x["ocn1"] for x in rows_from_csv(r.stdout)], ["A.Tro"])

    def test_unknown_column_is_usage_error(self) -> None:
        r = run_tool("--ocn1", "A.Tro", "--columns", "ocn1,bogus_col")
        self.assertEqual(r.returncode, 2)

    def test_custom_columns_order(self) -> None:
        r = run_tool("--ocn1", "A.Tro", "--columns", "canonical_name,ocn1")
        self.assertEqual(r.stdout.splitlines()[0], "canonical_name,ocn1")

    def test_json_format(self) -> None:
        r = run_tool("--ocn1", "A.Tro", "--format", "json")
        payload = json.loads(r.stdout)
        self.assertEqual(payload[0]["ocn1"], "A.Tro")

    def test_empty_selection_is_not_an_error(self) -> None:
        # A.Tro is attributed; --empty-attribution drops it -> 0 rows, still exit 0.
        r = run_tool("--ocn1", "A.Tro", "--empty-attribution")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(rows_from_csv(r.stdout), [])

    def test_out_file_written(self) -> None:
        out = self.tmp / "slice.csv"
        r = run_tool("--ocn1", "A.Tro", "--out", str(out))
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("A.Tro", out.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
