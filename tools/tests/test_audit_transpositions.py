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
    "aliases,flags,notes,attributed_to,attribution_source,historical_notes,"
    "transposes_to,same_as\n"
)


def catalog_row(*fields: str) -> str:
    return ",".join(fields + ("",) * (14 - len(fields))) + "\n"


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


class RankedAuditTests(unittest.TestCase):
    def _write_catalog(self, tmp: str, rows: str) -> Path:
        catalog = Path(tmp) / "catalog.csv"
        catalog.write_text(HEADER + rows, encoding="utf-8")
        return catalog

    def _mixed_and_intra_class_catalog(self, tmp: str) -> Path:
        # Mixed-class group: A.Tr1 (eco D02) and D.Tr2 (eco D02) reach the
        # same FEN via different move orders.
        # Intra-class group: two E rows that reach a shared FEN via the
        # same move order would not be a duplicate; instead we use two
        # genuine E openings that arrive at the same KID FEN.
        return self._write_catalog(
            tmp,
            catalog_row("A", "Flank Openings", "A", "", "", "0")
            + catalog_row("D", "Closed Queen's Pawn", "D", "", "", "0")
            + catalog_row("E", "Indian Defences", "E", "", "", "0")
            + catalog_row(
                "A.Tr1", "AD Trans One", "D02", "A", "d2d4 g8f6 c2c4 e7e6", "1"
            )
            + catalog_row(
                "D.Tr2", "AD Trans Two", "D02", "D", "c2c4 g8f6 d2d4 e7e6", "1"
            )
            + catalog_row(
                "E.Tr1", "E Trans One", "E60", "E", "d2d4 g8f6 c2c4 g7g6", "1"
            )
            + catalog_row(
                "E.Tr2", "E Trans Two", "E60", "E", "c2c4 g8f6 d2d4 g7g6", "1"
            ),
        )

    def test_ranked_places_class_mixed_group_first(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            catalog = self._mixed_and_intra_class_catalog(tmp)
            result = run_audit("--catalog", str(catalog), "--ranked")

        self.assertEqual(result.returncode, 0, result.stderr)
        rows = list(csv.DictReader(result.stdout.splitlines(), delimiter="\t"))
        self.assertEqual(
            [
                "rank",
                "score",
                "fen_key",
                "group_size",
                "depth_span",
                "classes",
                "eco_set",
                "resolved",
                "resolution_kind",
                "canonical_count",
                "ocn1",
                "canonical_name",
                "parent_ocn1",
                "depth",
                "moves_uci",
                "transposes_to",
                "same_as",
            ],
            list(rows[0].keys()),
        )
        first_rank_rows = [row for row in rows if row["rank"] == "1"]
        first_classes = {row["classes"] for row in first_rank_rows}
        self.assertEqual(first_classes, {"A,D"})
        self.assertTrue(int(first_rank_rows[0]["score"]) > 0)

    def test_limit_truncates_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            catalog = self._mixed_and_intra_class_catalog(tmp)
            result = run_audit(
                "--catalog", str(catalog), "--ranked", "--limit", "1"
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        rows = list(csv.DictReader(result.stdout.splitlines(), delimiter="\t"))
        self.assertEqual({row["rank"] for row in rows}, {"1"})
        slugs = sorted(row["ocn1"] for row in rows)
        self.assertEqual(slugs, ["A.Tr1", "D.Tr2"])

    def test_json_still_works_alongside_ranking(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            catalog = self._mixed_and_intra_class_catalog(tmp)
            result = run_audit("--catalog", str(catalog), "--json")

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(len(payload["groups"]), 2)
        sizes = sorted(g["group_size"] for g in payload["groups"])
        self.assertEqual(sizes, [2, 2])

    def test_ranked_and_json_are_mutually_exclusive(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            catalog = self._mixed_and_intra_class_catalog(tmp)
            result = run_audit(
                "--catalog", str(catalog), "--ranked", "--json"
            )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("mutually exclusive", result.stderr)

    def test_limit_validates_positive(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            catalog = self._mixed_and_intra_class_catalog(tmp)
            result = run_audit(
                "--catalog", str(catalog), "--ranked", "--limit", "0"
            )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("ERROR", result.stderr)


class ResolutionKindTests(unittest.TestCase):
    def _write_catalog(self, tmp: str, rows: str) -> Path:
        catalog = Path(tmp) / "catalog.csv"
        catalog.write_text(HEADER + rows, encoding="utf-8")
        return catalog

    def test_single_canonical_group_is_resolved(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            catalog = self._write_catalog(
                tmp,
                catalog_row("A", "Flank Openings", "A", "", "", "0")
                + catalog_row("D", "Closed Queen's Pawn", "D", "", "", "0")
                + catalog_row(
                    "A.Tr1", "AD Trans One", "D02", "A", "d2d4 g8f6 c2c4 e7e6",
                    "1", "", "", "", "", "", "", "D.Tr2",
                )
                + catalog_row(
                    "D.Tr2", "AD Trans Two", "D02", "D", "c2c4 g8f6 d2d4 e7e6",
                    "1",
                ),
            )

            result = run_audit("--catalog", str(catalog), "--json", "--include-resolved")

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(len(payload["groups"]), 1)
        group = payload["groups"][0]
        self.assertEqual(group["resolution_kind"], "single_canonical")
        self.assertEqual(group["canonical_count"], 1)
        self.assertTrue(group["resolved"])

    def test_multiple_canonical_group_is_resolved_with_kind(self) -> None:
        # Two canonical rows (empty transposes_to) coexist by design,
        # and a third row points into the group.
        with tempfile.TemporaryDirectory() as tmp:
            catalog = self._write_catalog(
                tmp,
                catalog_row("A", "Flank Openings", "A", "", "", "0")
                + catalog_row("B", "Semi-Open Games", "B", "", "", "0")
                + catalog_row("D", "Closed Queen's Pawn", "D", "", "", "0")
                + catalog_row(
                    "A.Can", "A Canonical", "A45", "A",
                    "d2d4 g8f6 b1c3 d7d5 c1g5 e7e6 e2e4 f8e7",
                    "1",
                )
                + catalog_row(
                    "B.Can", "B Canonical", "C14", "B",
                    "e2e4 e7e6 d2d4 d7d5 b1c3 g8f6 c1g5 f8e7",
                    "1",
                )
                + catalog_row(
                    "D.Pnt", "D Pointer", "D01", "D",
                    "d2d4 d7d5 b1c3 g8f6 c1g5 e7e6 e2e4 f8e7",
                    "1", "", "", "", "", "", "", "A.Can",
                ),
            )

            result = run_audit("--catalog", str(catalog), "--json", "--include-resolved")

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(len(payload["groups"]), 1)
        group = payload["groups"][0]
        self.assertEqual(group["resolution_kind"], "multiple_canonical")
        self.assertEqual(group["canonical_count"], 2)
        self.assertTrue(group["resolved"])

    def test_multiple_canonicals_without_pointer_remain_unresolved(self) -> None:
        # Same FEN reached by three rows but no transposes_to declared
        # anywhere: the group is not catalogued, it must stay visible.
        with tempfile.TemporaryDirectory() as tmp:
            catalog = self._write_catalog(
                tmp,
                catalog_row("A", "Flank Openings", "A", "", "", "0")
                + catalog_row("B", "Semi-Open Games", "B", "", "", "0")
                + catalog_row(
                    "A.Can", "A Canonical", "A45", "A",
                    "d2d4 g8f6 b1c3 d7d5 c1g5 e7e6 e2e4 f8e7",
                    "1",
                )
                + catalog_row(
                    "B.Can", "B Canonical", "C14", "B",
                    "e2e4 e7e6 d2d4 d7d5 b1c3 g8f6 c1g5 f8e7",
                    "1",
                ),
            )

            result = run_audit("--catalog", str(catalog), "--summary")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("unresolved_groups=1", result.stderr)
        self.assertIn("multiple_canonical_groups=0", result.stderr)

    def test_external_pointer_remains_unresolved(self) -> None:
        # A non-canonical pointer that targets a slug outside the group
        # must not count as resolved.
        with tempfile.TemporaryDirectory() as tmp:
            catalog = self._write_catalog(
                tmp,
                catalog_row("A", "Flank Openings", "A", "", "", "0")
                + catalog_row("D", "Closed Queen's Pawn", "D", "", "", "0")
                + catalog_row(
                    "D.Other", "D Other", "D02", "D",
                    "d2d4 g8f6 c2c4 e7e6 b1c3", "1",
                )
                + catalog_row(
                    "A.Tr1", "AD Trans One", "D02", "A",
                    "d2d4 g8f6 c2c4 e7e6", "1",
                    "", "", "", "", "", "", "D.Other",
                )
                + catalog_row(
                    "D.Tr2", "AD Trans Two", "D02", "D",
                    "c2c4 g8f6 d2d4 e7e6", "1",
                ),
            )

            result = run_audit("--catalog", str(catalog), "--summary")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("unresolved_groups=1", result.stderr)
        self.assertIn("resolved_groups=0", result.stderr)


class SameAsResolutionTests(unittest.TestCase):
    def _write_catalog(self, tmp: str, rows: str) -> Path:
        catalog = Path(tmp) / "catalog.csv"
        catalog.write_text(HEADER + rows, encoding="utf-8")
        return catalog

    def test_two_canonicals_with_bilateral_same_as_resolve_multiple(self) -> None:
        # Two slugs reach the same FEN, both canonical, declared
        # co-canonical via bilateral same_as. No third slug, no
        # transposes_to. Must resolve as multiple_canonical.
        with tempfile.TemporaryDirectory() as tmp:
            catalog = self._write_catalog(
                tmp,
                catalog_row("A", "Flank Openings", "A", "", "", "0")
                + catalog_row("D", "Closed Queen's Pawn", "D", "", "", "0")
                + catalog_row(
                    "A.Can", "A Canonical", "D05", "A",
                    "d2d4 g8f6 g1f3 e7e6 e2e3", "1",
                    "", "", "", "", "", "", "", "D.Can",
                )
                + catalog_row(
                    "D.Can", "D Canonical", "D05", "D",
                    "d2d4 g8f6 g1f3 e7e6 e2e3", "1",
                    "", "", "", "", "", "", "", "A.Can",
                ),
            )

            result = run_audit("--catalog", str(catalog), "--json", "--include-resolved")

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(len(payload["groups"]), 1)
        group = payload["groups"][0]
        self.assertEqual(group["resolution_kind"], "multiple_canonical")
        self.assertEqual(group["canonical_count"], 2)
        self.assertTrue(group["resolved"])

    def test_one_way_same_as_also_resolves(self) -> None:
        # The contract says same_as is conceptually symmetric — a
        # one-way declaration in the CSV still resolves the group.
        with tempfile.TemporaryDirectory() as tmp:
            catalog = self._write_catalog(
                tmp,
                catalog_row("A", "Flank Openings", "A", "", "", "0")
                + catalog_row("D", "Closed Queen's Pawn", "D", "", "", "0")
                + catalog_row(
                    "A.Can", "A Canonical", "D05", "A",
                    "d2d4 g8f6 g1f3 e7e6 e2e3", "1",
                    "", "", "", "", "", "", "", "D.Can",
                )
                + catalog_row(
                    "D.Can", "D Canonical", "D05", "D",
                    "d2d4 g8f6 g1f3 e7e6 e2e3", "1",
                ),
            )

            result = run_audit("--catalog", str(catalog), "--summary")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("resolved_groups=1", result.stderr)
        self.assertIn("multiple_canonical_groups=1", result.stderr)

    def test_same_as_combined_with_transposes_to_pointer(self) -> None:
        # Mixed group: two canonicals linked by same_as plus one
        # non-canonical row with transposes_to into the group.
        # Should resolve as multiple_canonical with canonical_count=2.
        with tempfile.TemporaryDirectory() as tmp:
            catalog = self._write_catalog(
                tmp,
                catalog_row("A", "Flank Openings", "A", "", "", "0")
                + catalog_row("D", "Closed Queen's Pawn", "D", "", "", "0")
                + catalog_row("E", "Indian Defences", "E", "", "", "0")
                + catalog_row(
                    "A.Can", "A Canonical", "D05", "A",
                    "d2d4 g8f6 g1f3 e7e6 e2e3", "1",
                    "", "", "", "", "", "", "", "D.Can",
                )
                + catalog_row(
                    "D.Can", "D Canonical", "D05", "D",
                    "d2d4 g8f6 g1f3 e7e6 e2e3", "1",
                    "", "", "", "", "", "", "", "A.Can",
                )
                + catalog_row(
                    "E.Pnt", "E Pointer", "E40", "E",
                    "d2d4 e7e6 g1f3 g8f6 e2e3", "1",
                    "", "", "", "", "", "", "A.Can",
                ),
            )

            result = run_audit("--catalog", str(catalog), "--json", "--include-resolved")

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(len(payload["groups"]), 1)
        group = payload["groups"][0]
        self.assertEqual(group["resolution_kind"], "multiple_canonical")
        self.assertEqual(group["canonical_count"], 2)


if __name__ == "__main__":
    unittest.main()
