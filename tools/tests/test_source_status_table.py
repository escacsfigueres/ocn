"""Tests for tools/source_status_table.py.

The source-status table joins, per attribution-candidate head:
  * the catalogue's authoritative attribution state (ATTRIBUTED iff both
    ``attributed_to`` and ``attribution_source`` are non-empty), and
  * a human-maintained machine-readable status registry that carries the
    prose-documented evidence grade (CLEAR / PARTIAL / HOLD) plus its
    citing doc (``source_ref``) and the grade note (``evidence_note``).

Heads with no registry row default to grade ``none`` (untouched). The tool
never invents a grade. These tests build small TSV/CSV fixtures so they do
not depend on the live catalogue.
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
TOOL = REPO_ROOT / "tools" / "source_status_table.py"

# A tiny catalogue mirroring the 14-column schema. Rows:
#   A           class root, no attribution
#   A.Ret       ATTRIBUTED (both fields)           — registry grade CLEAR (applied)
#   B.Fre.Win   UNATTRIBUTED                       — registry grade CLEAR (apply-ready)
#   B.Sic.Alp   UNATTRIBUTED                       — registry grade PARTIAL (held)
#   C.KGm.Dec.Fal UNATTRIBUTED                     — registry grade HOLD
#   D.Mystery   UNATTRIBUTED                       — NOT in registry -> grade none
CATALOG_HEADER = (
    "ocn1,canonical_name,eco_legacy,parent_ocn1,moves_uci,depth,aliases,"
    "flags,notes,attributed_to,attribution_source,historical_notes,"
    "transposes_to,same_as"
)
CATALOG_ROWS = [
    "A,Flank Openings,,,,0,,,Top-level class.,,,,,",
    "A.Ret,Réti Opening,A04,A,g1f3,1,Zukertort,,1.Nf3.,Richard Réti (popularizer),"
    '"Wikipedia, Réti Opening",Named for Réti.,,',
    "B.Fre.Win,\"French, Winawer\",C18,B.Fre,e2e4 e7e6,2,,,5...a6.,,,,,",
    "B.Sic.Alp,Sicilian Alapin,B22,B.Sic,e2e4 c7c5 c2c3,2,,,2.c3.,,,,,",
    "C.KGm.Dec.Fal,\"KGD, Falkbeer\",C31,C.KGm.Dec,e2e4 e7e5 f2f4 d7d5,3,,,2...d5.,,,,,",
    "D.Mystery,Mystery Line,D00,D,d2d4,1,,,A line.,,,,,",
]

# A status registry seeded ONLY with documented grades. Columns:
#   ocn1, grade, source_ref, evidence_note
REGISTRY = [
    ["ocn1", "grade", "source_ref", "evidence_note"],
    ["A.Ret", "CLEAR", "lot-3-eco-a-eponyms-dry-run.md",
     "ECO-A eponym head, applied; Wikipedia + ChessBase sourced."],
    ["B.Fre.Win", "CLEAR", "parked-attribution-reference-source-log.md",
     "The Center Game (nlm Q25): '(3.Nc3 Bb4) named after him' — apply-ready."],
    ["B.Sic.Alp", "PARTIAL", "parked-attribution-reference-source-log.md",
     "nlm negative: no source names the 2.c3 Sicilian after Alapin — held."],
    ["C.KGm.Dec.Fal", "HOLD", "whole-catalogue-attribution-factory-map.md",
     "Lot 2 graded hold; scope head-only, drop invented sub-slug."],
]


def write_catalog(path: Path) -> None:
    path.write_text("\n".join([CATALOG_HEADER, *CATALOG_ROWS]) + "\n", encoding="utf-8")


def write_registry(path: Path, rows=None) -> None:
    rows = REGISTRY if rows is None else rows
    buf = io.StringIO()
    w = csv.writer(buf, delimiter="\t", lineterminator="\n")
    w.writerows(rows)
    path.write_text(buf.getvalue(), encoding="utf-8")


def rows_from_tsv(text: str) -> list[dict]:
    return list(csv.DictReader(io.StringIO(text), delimiter="\t"))


class SourceStatusTableTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)
        self.catalog = self.tmp / "cat.csv"
        self.registry = self.tmp / "reg.tsv"
        write_catalog(self.catalog)
        write_registry(self.registry)

    def run_tool(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(TOOL),
             "--catalog", str(self.catalog),
             "--registry", str(self.registry), *args],
            capture_output=True, text=True, check=False)

    def index(self, rows: list[dict]) -> dict[str, dict]:
        return {r["ocn1"]: r for r in rows}

    # --- catalogue-derived status ---------------------------------------
    def test_attributed_detected_from_catalogue(self) -> None:
        r = self.run_tool()
        self.assertEqual(r.returncode, 0, r.stderr)
        by = self.index(rows_from_tsv(r.stdout))
        self.assertEqual(by["A.Ret"]["catalog_status"], "ATTRIBUTED")
        self.assertEqual(by["A.Ret"]["attributed_to"], "Richard Réti (popularizer)")

    def test_unattributed_catalogue_rows(self) -> None:
        r = self.run_tool()
        by = self.index(rows_from_tsv(r.stdout))
        self.assertEqual(by["B.Fre.Win"]["catalog_status"], "UNATTRIBUTED")
        self.assertEqual(by["B.Sic.Alp"]["catalog_status"], "UNATTRIBUTED")

    # --- registry grades surfaced ---------------------------------------
    def test_registry_grades_surfaced(self) -> None:
        r = self.run_tool()
        by = self.index(rows_from_tsv(r.stdout))
        self.assertEqual(by["B.Fre.Win"]["source_grade"], "CLEAR")
        self.assertEqual(by["B.Sic.Alp"]["source_grade"], "PARTIAL")
        self.assertEqual(by["C.KGm.Dec.Fal"]["source_grade"], "HOLD")

    def test_source_ref_and_note_carried(self) -> None:
        r = self.run_tool()
        by = self.index(rows_from_tsv(r.stdout))
        self.assertEqual(by["B.Fre.Win"]["source_ref"],
                         "parked-attribution-reference-source-log.md")
        self.assertIn("named after him", by["B.Fre.Win"]["evidence_note"])

    # --- none default for undocumented heads ----------------------------
    def test_none_default_for_unregistered_head(self) -> None:
        r = self.run_tool()
        by = self.index(rows_from_tsv(r.stdout))
        # D.Mystery is attribution-empty AND not in the registry; it only
        # appears under --all, but when it does its grade is 'none'.
        r2 = self.run_tool("--all")
        by2 = self.index(rows_from_tsv(r2.stdout))
        self.assertIn("D.Mystery", by2)
        self.assertEqual(by2["D.Mystery"]["source_grade"], "none")
        self.assertEqual(by2["D.Mystery"]["catalog_status"], "UNATTRIBUTED")

    def test_default_rowset_is_registry_union_attributed(self) -> None:
        # Default (no --all): show registry heads + any attributed catalogue
        # row. Plain descriptors with no grade (D.Mystery, class root A) are
        # excluded by default to keep the table to candidate heads.
        r = self.run_tool()
        slugs = {x["ocn1"] for x in rows_from_tsv(r.stdout)}
        self.assertEqual(
            slugs, {"A.Ret", "B.Fre.Win", "B.Sic.Alp", "C.KGm.Dec.Fal"})
        self.assertNotIn("D.Mystery", slugs)
        self.assertNotIn("A", slugs)

    def test_all_includes_every_catalogue_row(self) -> None:
        r = self.run_tool("--all")
        slugs = {x["ocn1"] for x in rows_from_tsv(r.stdout)}
        self.assertEqual(
            slugs,
            {"A", "A.Ret", "B.Fre.Win", "B.Sic.Alp", "C.KGm.Dec.Fal", "D.Mystery"})

    # --- filters --------------------------------------------------------
    def test_status_filter(self) -> None:
        r = self.run_tool("--status", "CLEAR")
        slugs = [x["ocn1"] for x in rows_from_tsv(r.stdout)]
        self.assertEqual(slugs, ["A.Ret", "B.Fre.Win"])

    def test_status_filter_none(self) -> None:
        r = self.run_tool("--all", "--status", "none")
        slugs = [x["ocn1"] for x in rows_from_tsv(r.stdout)]
        self.assertEqual(slugs, ["A", "D.Mystery"])

    def test_unattributed_filter(self) -> None:
        r = self.run_tool("--unattributed")
        slugs = [x["ocn1"] for x in rows_from_tsv(r.stdout)]
        self.assertNotIn("A.Ret", slugs)  # A.Ret is attributed
        self.assertEqual(slugs, ["B.Fre.Win", "B.Sic.Alp", "C.KGm.Dec.Fal"])

    def test_status_and_unattributed_combine_as_and(self) -> None:
        # CLEAR + unattributed => B.Fre.Win only (A.Ret is CLEAR but attributed).
        r = self.run_tool("--status", "CLEAR", "--unattributed")
        slugs = [x["ocn1"] for x in rows_from_tsv(r.stdout)]
        self.assertEqual(slugs, ["B.Fre.Win"])

    # --- output formats parse correctly ---------------------------------
    def test_output_is_catalogue_order(self) -> None:
        r = self.run_tool()
        slugs = [x["ocn1"] for x in rows_from_tsv(r.stdout)]
        self.assertEqual(slugs, ["A.Ret", "B.Fre.Win", "B.Sic.Alp", "C.KGm.Dec.Fal"])

    def test_json_format_parses(self) -> None:
        r = self.run_tool("--format", "json")
        self.assertEqual(r.returncode, 0, r.stderr)
        payload = json.loads(r.stdout)
        by = {row["ocn1"]: row for row in payload}
        self.assertEqual(by["B.Fre.Win"]["source_grade"], "CLEAR")
        self.assertEqual(by["A.Ret"]["catalog_status"], "ATTRIBUTED")

    def test_table_format_human_readable(self) -> None:
        r = self.run_tool("--format", "table")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("B.Fre.Win", r.stdout)
        self.assertIn("CLEAR", r.stdout)
        # header-ish row present
        self.assertIn("ocn1", r.stdout)

    def test_out_file_written(self) -> None:
        out = self.tmp / "table.tsv"
        r = self.run_tool("--out", str(out))
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("B.Fre.Win", out.read_text(encoding="utf-8"))

    # --- consistency invariant ------------------------------------------
    def test_attributed_requires_both_fields(self) -> None:
        # A row with attributed_to but no attribution_source must NOT count as
        # ATTRIBUTED (validator enforces attributed_to => attribution_source).
        rows = [
            CATALOG_HEADER,
            "A,Flank,,,,0,,,c.,,,,,",
            "A.Half,Half Attributed,A00,A,g1f3,1,,,x.,Some Person,,,,",
        ]
        cat = self.tmp / "half.csv"
        cat.write_text("\n".join(rows) + "\n", encoding="utf-8")
        reg = self.tmp / "half_reg.tsv"
        write_registry(reg, [["ocn1", "grade", "source_ref", "evidence_note"],
                             ["A.Half", "PARTIAL", "doc.md", "note"]])
        r = subprocess.run(
            [sys.executable, str(TOOL), "--catalog", str(cat),
             "--registry", str(reg)], capture_output=True, text=True, check=False)
        self.assertEqual(r.returncode, 0, r.stderr)
        by = self.index(rows_from_tsv(r.stdout))
        self.assertEqual(by["A.Half"]["catalog_status"], "UNATTRIBUTED")

    # --- error handling -------------------------------------------------
    def test_registry_slug_not_in_catalogue_is_error(self) -> None:
        reg = self.tmp / "bad_reg.tsv"
        write_registry(reg, [["ocn1", "grade", "source_ref", "evidence_note"],
                             ["Z.Nope", "CLEAR", "doc.md", "note"]])
        r = subprocess.run(
            [sys.executable, str(TOOL), "--catalog", str(self.catalog),
             "--registry", str(reg)], capture_output=True, text=True, check=False)
        self.assertEqual(r.returncode, 1)
        self.assertIn("Z.Nope", r.stderr)

    def test_bad_registry_grade_is_error(self) -> None:
        reg = self.tmp / "badgrade.tsv"
        write_registry(reg, [["ocn1", "grade", "source_ref", "evidence_note"],
                             ["B.Fre.Win", "MAYBE", "doc.md", "note"]])
        r = subprocess.run(
            [sys.executable, str(TOOL), "--catalog", str(self.catalog),
             "--registry", str(reg)], capture_output=True, text=True, check=False)
        self.assertEqual(r.returncode, 1)
        self.assertIn("MAYBE", r.stderr)

    def test_missing_catalogue_is_error(self) -> None:
        r = subprocess.run(
            [sys.executable, str(TOOL), "--catalog", str(self.tmp / "nope.csv"),
             "--registry", str(self.registry)],
            capture_output=True, text=True, check=False)
        self.assertEqual(r.returncode, 1)

    def test_real_registry_validates_against_live_catalogue(self) -> None:
        # The shipped registry must reference only real catalogue slugs and
        # valid grades: running the tool with the defaults must succeed.
        r = subprocess.run([sys.executable, str(TOOL)],
                           capture_output=True, text=True, check=False)
        self.assertEqual(r.returncode, 0, r.stderr)
        # And every default row carries a real grade (never blank).
        for row in rows_from_tsv(r.stdout):
            self.assertIn(row["source_grade"],
                          {"CLEAR", "PARTIAL", "HOLD", "none"})


if __name__ == "__main__":
    unittest.main()
