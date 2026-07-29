"""Tests for tools/build_json_export.py.

The JSON export is a *derived* release artefact: it must be reproducible
from `catalog/ocn-1.csv` alone, byte-identical across builds, and honest
about the fields it adds. What is pinned here:

  * the envelope (`schema`, `catalog_version`, `generated_note`, `rows`)
    and the fact that a real build parses as JSON;
  * every CSV column survives verbatim, in header order, with the derived
    fields appended in a fixed order — no reordering, no dropped column,
    no silent rewrite of catalogue text;
  * `moves_san` is the UCI line replayed, not a stored field: the Najdorf
    English Attack must render `1.e4 c5 ...`, and the class roots (which
    have no position) must render the empty string rather than a
    plausible-looking guess;
  * the four pipe-split arrays behave on the three cases that matter — a
    single-code cell, a pipe composite, and an empty cell (`[]`, never
    `[""]`);
  * two builds of the same catalogue are byte-identical.

Run:
    python3 -m unittest tools.tests.test_build_json_export
"""
from __future__ import annotations

import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools"))

from build_json_export import (  # noqa: E402
    GENERATED_NOTE,
    LIST_FIELDS,
    SCHEMA,
    build_document,
    build_row,
    moves_san,
    render_json,
    split_pipe,
)

CATALOG = REPO_ROOT / "catalog" / "ocn-1.csv"
EXPECTED_ROWS = 5899
TEST_VERSION = "ocn-1.2.0-test"


class MovesSanTests(unittest.TestCase):
    def test_numbered_san_rendering(self) -> None:
        self.assertEqual(
            moves_san("e2e4 c7c5 g1f3"), "1.e4 c5 2.Nf3")

    def test_empty_and_blank_are_empty_string(self) -> None:
        self.assertEqual(moves_san(""), "")
        self.assertEqual(moves_san("   "), "")

    def test_capture_and_castling_tokens(self) -> None:
        san = moves_san("e2e4 e7e5 g1f3 b8c6 f1c4 g8f6 e1g1")
        self.assertTrue(san.endswith("4.O-O"), san)

    def test_illegal_uci_raises(self) -> None:
        with self.assertRaises(ValueError):
            moves_san("e2e5")


class SplitPipeTests(unittest.TestCase):
    def test_empty_gives_empty_list(self) -> None:
        self.assertEqual(split_pipe(""), [])
        self.assertEqual(split_pipe("|"), [])

    def test_single_and_composite(self) -> None:
        self.assertEqual(split_pipe("B90"), ["B90"])
        self.assertEqual(split_pipe("B90|B91"), ["B90", "B91"])

    def test_whitespace_is_trimmed(self) -> None:
        self.assertEqual(split_pipe("a | b"), ["a", "b"])


class BuildRowTests(unittest.TestCase):
    def test_derived_fields_appended_after_csv_columns(self) -> None:
        row = build_row({
            "ocn1": "X.Y",
            "eco_legacy": "B90|B91",
            "moves_uci": "e2e4",
            "aliases": "One|Two",
            "flags": "sharp",
            "same_as": "",
        })
        self.assertEqual(row["eco_legacy"], "B90|B91")  # source untouched
        self.assertEqual(row["eco"], ["B90", "B91"])
        self.assertEqual(row["aliases_list"], ["One", "Two"])
        self.assertEqual(row["flags_list"], ["sharp"])
        self.assertEqual(row["same_as_list"], [])
        self.assertEqual(row["moves_san"], "1.e4")
        self.assertEqual(
            list(row)[-5:],
            ["moves_san", "eco", "aliases_list", "same_as_list", "flags_list"])


class WholeCatalogueExportTests(unittest.TestCase):
    """Build the real export once into a temp dir and inspect it."""

    @classmethod
    def setUpClass(cls) -> None:
        cls._tmp = tempfile.TemporaryDirectory()
        out = Path(cls._tmp.name) / "ocn-1.json"
        out.write_text(
            render_json(build_document(CATALOG, TEST_VERSION), pretty=True),
            encoding="utf-8")
        cls.out = out
        cls.doc = json.loads(out.read_text(encoding="utf-8"))
        cls.by_slug = {r["ocn1"]: r for r in cls.doc["rows"]}

    @classmethod
    def tearDownClass(cls) -> None:
        cls._tmp.cleanup()

    def test_envelope_fields(self) -> None:
        self.assertEqual(self.doc["schema"], SCHEMA)
        self.assertEqual(self.doc["catalog_version"], TEST_VERSION)
        self.assertEqual(self.doc["generated_note"], GENERATED_NOTE)
        self.assertIn("canonical source", self.doc["generated_note"])

    def test_row_count_matches_catalogue(self) -> None:
        self.assertEqual(len(self.doc["rows"]), EXPECTED_ROWS)

    def test_rows_follow_catalogue_order(self) -> None:
        with CATALOG.open(newline="", encoding="utf-8") as f:
            catalog = list(csv.DictReader(f))
        self.assertEqual(
            [r["ocn1"] for r in self.doc["rows"]],
            [r["ocn1"] for r in catalog])

    def test_every_csv_column_survives_verbatim(self) -> None:
        with CATALOG.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            columns = list(reader.fieldnames or [])
            catalog = list(reader)
        derived = ["moves_san", "eco"] + [d for _, d in LIST_FIELDS]
        for exported, source in zip(self.doc["rows"], catalog):
            self.assertEqual(list(exported), columns + derived)
            for column in columns:
                self.assertEqual(exported[column], source[column])

    def test_najdorf_english_attack_san(self) -> None:
        row = self.by_slug["B.Sic.Naj.Eng"]
        self.assertTrue(
            row["moves_san"].startswith("1.e4 c5"), row["moves_san"])
        self.assertEqual(
            row["moves_san"],
            "1.e4 c5 2.Nf3 d6 3.d4 cxd4 4.Nxd4 Nf6 5.Nc3 a6 6.Be3")
        self.assertEqual(row["eco"], ["B90"])

    def test_class_roots_have_no_san_and_no_eco(self) -> None:
        for root in ("A", "B", "C", "D", "E"):
            row = self.by_slug[root]
            self.assertEqual(row["moves_san"], "", root)
            self.assertEqual(row["eco"], [], root)
            self.assertEqual(row["moves_uci"], "", root)

    def test_pipe_composite_eco_row(self) -> None:
        row = self.by_slug["A.Hol.Lng"]
        self.assertEqual(row["eco_legacy"], "A87|A88|A89")
        self.assertEqual(row["eco"], ["A87", "A88", "A89"])
        self.assertEqual(row["flags_list"], ["sharp"])

    def test_null_eco_row_gets_empty_array_not_empty_string(self) -> None:
        row = self.by_slug["A.Ret.Ang.g3.Nf6"]
        self.assertEqual(row["eco_legacy"], "")
        self.assertEqual(row["eco"], [])
        self.assertNotEqual(row["eco"], [""])
        self.assertTrue(row["moves_san"].startswith("1.Nf3 d5"))

    def test_same_as_list_on_a_co_canonical_row(self) -> None:
        self.assertEqual(self.by_slug["D.Rub"]["same_as_list"], ["A.Col.Zuk"])

    def test_every_row_derives_all_four_arrays(self) -> None:
        for row in self.doc["rows"]:
            for field in ["eco"] + [d for _, d in LIST_FIELDS]:
                self.assertIsInstance(row[field], list, f"{row['ocn1']}.{field}")
            self.assertIsInstance(row["moves_san"], str)

    def test_san_present_for_every_row_with_moves(self) -> None:
        for row in self.doc["rows"]:
            if row["moves_uci"].strip():
                self.assertTrue(row["moves_san"], row["ocn1"])
                self.assertTrue(row["moves_san"].startswith("1."), row["ocn1"])


class DeterminismTests(unittest.TestCase):
    def test_two_builds_are_byte_identical(self) -> None:
        first = render_json(build_document(CATALOG, TEST_VERSION))
        second = render_json(build_document(CATALOG, TEST_VERSION))
        self.assertEqual(first, second)

    def test_pretty_and_compact_carry_the_same_data(self) -> None:
        document = build_document(CATALOG, TEST_VERSION)
        self.assertEqual(
            json.loads(render_json(document, pretty=True)),
            json.loads(render_json(document, pretty=False)))

    def test_output_ends_with_newline(self) -> None:
        self.assertTrue(
            render_json({"rows": []}, pretty=False).endswith("\n"))


if __name__ == "__main__":
    unittest.main()
