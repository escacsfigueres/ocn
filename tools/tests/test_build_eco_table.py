"""Tests for tools/build_eco_table.py.

The ECO join table is the scalar view of `eco_legacy`: one row per (slug,
atomic ECO code), `seq` recording the code's 0-based position in the
original pipe list. It is a committed sidecar, so the contract is both
"the expansion is correct" and "the checked-in file is current".

Pinned here:

  * expansion semantics on tiny fixtures — single code, pipe composite,
    empty cell (skipped, never emitted as a blank code);
  * order is catalogue order then `seq`, so the original cell is
    reconstructible and the file diffs meaningfully;
  * round-trip: re-joining the table by slug rebuilds every `eco_legacy`
    cell in the live catalogue exactly, including the composites;
  * the drift guard — the committed `catalog/ocn-1.eco.tsv` must equal a
    fresh rebuild (same pattern as the attribution sidecar);
  * the live scale, so a silent collapse of the expansion is caught.

Run:
    python3 -m unittest tools.tests.test_build_eco_table
"""
from __future__ import annotations

import csv
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools"))

from build_eco_table import (  # noqa: E402
    HEADER,
    build_eco_rows,
    build_from_repo,
    coverage_report,
    load_catalog,
    render_tsv,
    split_eco,
)

CATALOG = REPO_ROOT / "catalog" / "ocn-1.csv"
SIDECAR = REPO_ROOT / "catalog" / "ocn-1.eco.tsv"

EXPECTED_TABLE_ROWS = 7234
EXPECTED_DISTINCT_CODES = 500
EXPECTED_SLUGS_WITH_ECO = 5600
EXPECTED_CATALOGUE_ROWS = 5899


def _row(ocn1: str, eco: str) -> dict[str, str]:
    return {"ocn1": ocn1, "eco_legacy": eco}


class SplitEcoTests(unittest.TestCase):
    def test_single_code(self) -> None:
        self.assertEqual(split_eco("B90"), ["B90"])

    def test_composite_keeps_declared_order(self) -> None:
        self.assertEqual(split_eco("A87|A88|A89"), ["A87", "A88", "A89"])

    def test_empty_cell_yields_nothing(self) -> None:
        self.assertEqual(split_eco(""), [])
        self.assertEqual(split_eco("   "), [])
        self.assertEqual(split_eco("||"), [])


class BuildEcoRowsTests(unittest.TestCase):
    def test_composite_expands_with_zero_based_seq(self) -> None:
        self.assertEqual(
            build_eco_rows([_row("A.Hol", "A80|A81|A82")]),
            [("A.Hol", "A80", 0), ("A.Hol", "A81", 1), ("A.Hol", "A82", 2)])

    def test_rows_without_eco_are_skipped(self) -> None:
        rows = [_row("A", ""), _row("A.Eng", "A10"), _row("B", "")]
        self.assertEqual(build_eco_rows(rows), [("A.Eng", "A10", 0)])

    def test_order_is_catalogue_order_then_seq(self) -> None:
        rows = [_row("Z.Last", "C00|C01"), _row("A.First", "A10")]
        self.assertEqual(
            [r[0] for r in build_eco_rows(rows)],
            ["Z.Last", "Z.Last", "A.First"])

    def test_render_tsv_shape(self) -> None:
        text = render_tsv(build_eco_rows([_row("A.Eng", "A10|A11")]))
        self.assertEqual(
            text, HEADER + "\nA.Eng\tA10\t0\nA.Eng\tA11\t1\n")


class LiveCatalogueTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.catalog = load_catalog(CATALOG)
        cls.pairs = build_eco_rows(cls.catalog)

    def test_expected_scale(self) -> None:
        self.assertEqual(len(self.catalog), EXPECTED_CATALOGUE_ROWS)
        self.assertEqual(len(self.pairs), EXPECTED_TABLE_ROWS)
        self.assertEqual(
            len({eco for _, eco, _ in self.pairs}), EXPECTED_DISTINCT_CODES)
        self.assertEqual(
            len({ocn1 for ocn1, _, _ in self.pairs}), EXPECTED_SLUGS_WITH_ECO)

    def test_composites_make_the_table_longer_than_the_catalogue(self) -> None:
        self.assertGreater(len(self.pairs), len(self.catalog))

    def test_every_slug_exists_in_the_catalogue(self) -> None:
        slugs = {row["ocn1"] for row in self.catalog}
        for ocn1, _, _ in self.pairs:
            self.assertIn(ocn1, slugs)

    def test_codes_are_well_formed(self) -> None:
        for _, eco, _ in self.pairs:
            self.assertRegex(eco, r"^[A-E][0-9]{2}$")

    def test_seq_is_contiguous_from_zero_per_slug(self) -> None:
        seen: dict[str, list[int]] = {}
        for ocn1, _, seq in self.pairs:
            seen.setdefault(ocn1, []).append(seq)
        for ocn1, seqs in seen.items():
            self.assertEqual(seqs, list(range(len(seqs))), ocn1)

    def test_round_trip_rebuilds_every_eco_legacy_cell(self) -> None:
        rebuilt: dict[str, list[str]] = {}
        for ocn1, eco, _ in self.pairs:
            rebuilt.setdefault(ocn1, []).append(eco)
        for row in self.catalog:
            cell = row["eco_legacy"].strip()
            if cell:
                self.assertEqual("|".join(rebuilt[row["ocn1"]]), cell,
                                 row["ocn1"])
            else:
                self.assertNotIn(row["ocn1"], rebuilt, row["ocn1"])

    def test_class_roots_are_absent(self) -> None:
        slugs = {ocn1 for ocn1, _, _ in self.pairs}
        for root in ("A", "B", "C", "D", "E"):
            self.assertNotIn(root, slugs)

    def test_coverage_report_mentions_the_headline_counts(self) -> None:
        report = coverage_report(self.catalog)
        self.assertIn(f"eco table rows: {EXPECTED_TABLE_ROWS}", report)
        self.assertIn(f"distinct ECO codes: {EXPECTED_DISTINCT_CODES}", report)


class SidecarDriftTests(unittest.TestCase):
    def test_committed_sidecar_is_current(self) -> None:
        """The committed sidecar must equal a fresh rebuild from the live
        catalogue. Editing `eco_legacy` without regenerating fails here.
        Stable because the expansion is deterministic."""
        self.assertTrue(SIDECAR.exists(), "sidecar not committed")
        self.assertEqual(
            SIDECAR.read_text(encoding="utf-8"), build_from_repo(CATALOG),
            "catalog/ocn-1.eco.tsv is stale — regenerate with "
            "python3 tools/build_eco_table.py")

    def test_committed_sidecar_header_and_shape(self) -> None:
        lines = SIDECAR.read_text(encoding="utf-8").splitlines()
        self.assertEqual(lines[0], HEADER)
        self.assertEqual(len(lines) - 1, EXPECTED_TABLE_ROWS)
        with SIDECAR.open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f, delimiter="\t"))
        self.assertEqual(len(rows), EXPECTED_TABLE_ROWS)
        self.assertEqual(list(rows[0]), ["ocn1", "eco", "seq"])


if __name__ == "__main__":
    unittest.main()
