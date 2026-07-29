"""Tests for tools/build_eco_divergence.py and the validator check that
pins it (roadmap H2.5).

The divergence sidecar is OCN's honesty instrument: it lists every row whose
OCN class letter is not among its own ECO letters, with a rationale key that
resolves to prose in the spec. Its value is entirely in being complete and
current, so the contract is three-sided:

  * the divergence predicate is right — "class absent from the row's ECO
    letters", agreeing when a composite cell contains the class letter, and
    silent on rows with no ECO code at all;
  * `rationale_ref` is a closed set assigned by `family_head`, so no row can
    acquire an unexplained key;
  * the drift guard — the committed `catalog/ocn-1.eco-divergence.tsv` must
    equal a fresh rebuild (same pattern as the ECO and attribution sidecars);
  * `tools/validate.py` reaches the same set by an independent inline
    recomputation. Two implementations agreeing is the point: the validator
    does not import the builder, so a bug in the builder cannot hide itself.

The live counts are pinned. They are quoted in the spec, the consumer guide
and the README, and a silent drift in any of them is exactly the failure this
whole work item exists to prevent.

Run:
    python3 -m unittest tools.tests.test_build_eco_divergence
"""
from __future__ import annotations

import csv
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools"))

from build_eco_divergence import (  # noqa: E402
    HEADER,
    RATIONALE_BY_FAMILY_HEAD,
    RATIONALE_REFS,
    build_divergence_rows,
    build_from_repo,
    coverage_report,
    divergent_slugs,
    family_head,
    is_divergent,
    load_catalog,
    main,
    rationale_ref,
    render_tsv,
)
from validate import (  # noqa: E402
    DIVERGENCE_SIDECAR,
    divergence_sidecar_problem,
    recompute_divergent_slugs,
)

CATALOG = REPO_ROOT / "catalog" / "ocn-1.csv"
SIDECAR = REPO_ROOT / "catalog" / "ocn-1.eco-divergence.tsv"

EXPECTED_DIVERGENT_ROWS = 770
EXPECTED_ECO_BEARING_ROWS = 5600
EXPECTED_CATALOGUE_ROWS = 5899
EXPECTED_BY_RATIONALE = {
    "french-b": 252,
    "indians-e": 195,
    "gruenfeld-e": 117,
    "london-colle-a": 82,
    "catalan-d": 49,
    "misc": 44,
    "budapest-e": 31,
}


def _row(ocn1: str, eco: str) -> dict[str, str]:
    return {"ocn1": ocn1, "eco_legacy": eco}


class DivergencePredicateTests(unittest.TestCase):
    def test_class_absent_from_eco_letters_diverges(self) -> None:
        self.assertTrue(is_divergent("B.Fre", "C00|C01"))
        self.assertTrue(is_divergent("E.Gru", "D70|D71"))

    def test_class_present_among_eco_letters_agrees(self) -> None:
        self.assertFalse(is_divergent("B.Sic.Naj", "B90"))

    def test_composite_cell_agrees_when_any_code_carries_the_class(self) -> None:
        """`A.Owe` style cells: one matching letter is enough. The catalogue
        has already conceded OCN's reading in that cell, so there is nothing
        to explain."""
        self.assertFalse(is_divergent("A.Mix", "A40|B00"))
        self.assertTrue(is_divergent("A.Mix", "D40|B00"))

    def test_rows_without_eco_are_never_divergent(self) -> None:
        """Absence of a code is not a disagreement about a code — the five
        class roots and the Lichess long-tail."""
        self.assertFalse(is_divergent("A", ""))
        self.assertFalse(is_divergent("B.Sic.Naj.Xyz", "   "))
        self.assertFalse(is_divergent("C.RyL", "||"))


class FamilyHeadAndRationaleTests(unittest.TestCase):
    def test_family_head_is_the_first_two_segments(self) -> None:
        self.assertEqual(family_head("B.Fre.Win.Nc3.Bb4.e5.c5"), "B.Fre")
        self.assertEqual(family_head("A.Lon"), "A.Lon")

    def test_family_head_of_a_class_root_is_the_root(self) -> None:
        self.assertEqual(family_head("A"), "A")

    def test_known_heads_map_to_their_documented_rationale(self) -> None:
        self.assertEqual(rationale_ref("B.Fre"), "french-b")
        self.assertEqual(rationale_ref("A.Lon"), "london-colle-a")
        self.assertEqual(rationale_ref("A.Col"), "london-colle-a")
        self.assertEqual(rationale_ref("D.Cat"), "catalan-d")
        self.assertEqual(rationale_ref("E.Gru"), "gruenfeld-e")
        self.assertEqual(rationale_ref("E.Bud"), "budapest-e")
        self.assertEqual(rationale_ref("E.Ben"), "indians-e")

    def test_unmapped_head_falls_to_misc(self) -> None:
        self.assertEqual(rationale_ref("A.Zzz"), "misc")

    def test_rationale_set_is_closed_and_matches_the_spec_keys(self) -> None:
        self.assertEqual(RATIONALE_REFS, {
            "french-b", "indians-e", "gruenfeld-e", "catalan-d",
            "london-colle-a", "budapest-e", "misc",
        })

    def test_every_mapped_head_is_a_real_catalogue_slug(self) -> None:
        slugs = {row["ocn1"] for row in load_catalog(CATALOG)}
        for head in RATIONALE_BY_FAMILY_HEAD:
            self.assertIn(head, slugs, head)


class BuildDivergenceRowsTests(unittest.TestCase):
    def test_row_shape(self) -> None:
        self.assertEqual(
            build_divergence_rows([_row("B.Fre.Adv", "C02")]),
            [("B.Fre.Adv", "B", "C02", "B.Fre", "french-b")])

    def test_agreeing_rows_are_skipped(self) -> None:
        rows = [_row("B.Sic", "B20"), _row("B.Fre", "C00"), _row("A", "")]
        self.assertEqual([r[0] for r in build_divergence_rows(rows)], ["B.Fre"])

    def test_order_is_catalogue_order(self) -> None:
        rows = [_row("E.Gru", "D70"), _row("B.Fre", "C00")]
        self.assertEqual([r[0] for r in build_divergence_rows(rows)],
                         ["E.Gru", "B.Fre"])

    def test_eco_codes_column_is_the_normalised_pipe_list(self) -> None:
        built = build_divergence_rows([_row("E.Bud", " A51 | A52 ")])
        self.assertEqual(built[0][2], "A51|A52")

    def test_render_tsv_shape(self) -> None:
        text = render_tsv(build_divergence_rows([_row("A.Lon", "D02")]))
        self.assertEqual(text, HEADER + "\nA.Lon\tA\tD02\tA.Lon\tlondon-colle-a\n")

    def test_divergent_slugs_matches_the_built_rows(self) -> None:
        rows = [_row("B.Fre", "C00"), _row("B.Sic", "B20"), _row("D.Cat", "E01")]
        self.assertEqual(divergent_slugs(rows), {"B.Fre", "D.Cat"})


class LiveCatalogueTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.catalog = load_catalog(CATALOG)
        cls.divergent = build_divergence_rows(cls.catalog)

    def test_expected_scale(self) -> None:
        self.assertEqual(len(self.catalog), EXPECTED_CATALOGUE_ROWS)
        self.assertEqual(len(self.divergent), EXPECTED_DIVERGENT_ROWS)

    def test_headline_share_of_eco_bearing_rows(self) -> None:
        """13.8% — the number the README and the spec both quote."""
        eco_bearing = sum(
            1 for row in self.catalog if row["eco_legacy"].strip())
        self.assertEqual(eco_bearing, EXPECTED_ECO_BEARING_ROWS)
        self.assertEqual(
            round(100 * len(self.divergent) / eco_bearing, 1), 13.8)

    def test_rationale_breakdown_is_pinned(self) -> None:
        counts: dict[str, int] = {}
        for row in self.divergent:
            counts[row[4]] = counts.get(row[4], 0) + 1
        self.assertEqual(counts, EXPECTED_BY_RATIONALE)

    def test_french_is_the_largest_single_rationale(self) -> None:
        counts: dict[str, int] = {}
        for row in self.divergent:
            counts[row[4]] = counts.get(row[4], 0) + 1
        self.assertEqual(max(counts, key=lambda k: counts[k]), "french-b")

    def test_every_divergent_row_carries_a_closed_set_rationale(self) -> None:
        for row in self.divergent:
            self.assertIn(row[4], RATIONALE_REFS, row[0])

    def test_class_letter_column_matches_the_slug(self) -> None:
        for slug, cls, _, _, _ in self.divergent:
            self.assertEqual(cls, slug[0], slug)
            self.assertIn(cls, "ABCDE", slug)

    def test_class_letter_is_absent_from_the_listed_codes(self) -> None:
        """The defining property, re-asserted on the built file rather than
        on the predicate that built it."""
        for slug, cls, codes, _, _ in self.divergent:
            self.assertTrue(codes, slug)
            self.assertNotIn(cls, {code[0] for code in codes.split("|")}, slug)

    def test_family_head_is_an_ancestor_of_every_row(self) -> None:
        for slug, _, _, head, _ in self.divergent:
            self.assertTrue(slug == head or slug.startswith(head + "."), slug)

    def test_family_head_maps_to_exactly_one_rationale(self) -> None:
        seen: dict[str, str] = {}
        for _, _, _, head, ref in self.divergent:
            self.assertEqual(seen.setdefault(head, ref), ref, head)

    def test_no_class_root_appears(self) -> None:
        slugs = {row[0] for row in self.divergent}
        for root in ("A", "B", "C", "D", "E"):
            self.assertNotIn(root, slugs)

    def test_class_c_never_diverges(self) -> None:
        """OCN's `C` is the strict subset "1.e4 e5" of ECO's C, so no row
        can be OCN-C while its ECO codes are not C. The French moving out is
        the whole divergence; nothing moves in."""
        self.assertNotIn("C", {row[1] for row in self.divergent})

    def test_coverage_report_mentions_the_headline_counts(self) -> None:
        report = coverage_report(self.catalog)
        self.assertIn(f"divergent rows: {EXPECTED_DIVERGENT_ROWS}", report)
        self.assertIn("french-b", report)


class SidecarDriftTests(unittest.TestCase):
    def test_committed_sidecar_is_current(self) -> None:
        """The committed sidecar must equal a fresh rebuild from the live
        catalogue. Reclassifying a row or editing `eco_legacy` without
        regenerating fails here. Stable because the build is deterministic."""
        self.assertTrue(SIDECAR.exists(), "sidecar not committed")
        self.assertEqual(
            SIDECAR.read_text(encoding="utf-8"), build_from_repo(CATALOG),
            "catalog/ocn-1.eco-divergence.tsv is stale — regenerate with "
            "python3 tools/build_eco_divergence.py")

    def test_committed_sidecar_header_and_shape(self) -> None:
        lines = SIDECAR.read_text(encoding="utf-8").splitlines()
        self.assertEqual(lines[0], HEADER)
        self.assertEqual(len(lines) - 1, EXPECTED_DIVERGENT_ROWS)
        with SIDECAR.open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f, delimiter="\t"))
        self.assertEqual(len(rows), EXPECTED_DIVERGENT_ROWS)
        self.assertEqual(
            list(rows[0]),
            ["ocn1", "ocn_class", "eco_codes", "family_head", "rationale_ref"])

    def test_every_sidecar_slug_exists_in_the_catalogue(self) -> None:
        slugs = {row["ocn1"] for row in load_catalog(CATALOG)}
        with SIDECAR.open(newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f, delimiter="\t"):
                self.assertIn(row["ocn1"], slugs)

    def test_cli_writes_the_same_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "out.tsv"
            self.assertEqual(main(["--out", str(out)]), 0)
            self.assertEqual(out.read_text(encoding="utf-8"),
                             SIDECAR.read_text(encoding="utf-8"))

    def test_cli_reports_a_missing_catalogue(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(
                main(["--catalog", str(Path(tmp) / "nope.csv"),
                      "--out", str(Path(tmp) / "out.tsv")]), 1)


class ValidatorCrossCheckTests(unittest.TestCase):
    """The validator's inline recomputation is a second implementation. It
    must agree with the builder on the live catalogue, and must complain
    loudly (and legibly) when the committed file drifts."""

    def test_validator_points_at_the_committed_sidecar(self) -> None:
        self.assertEqual(DIVERGENCE_SIDECAR, SIDECAR)

    def test_validator_recomputation_agrees_with_the_builder(self) -> None:
        rows = load_catalog(CATALOG)
        self.assertEqual(recompute_divergent_slugs(rows), divergent_slugs(rows))
        self.assertEqual(len(recompute_divergent_slugs(rows)),
                         EXPECTED_DIVERGENT_ROWS)

    def test_live_catalogue_and_sidecar_agree(self) -> None:
        self.assertIsNone(divergence_sidecar_problem(load_catalog(CATALOG)))

    def test_missing_sidecar_is_a_problem(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            problem = divergence_sidecar_problem(
                [_row("B.Fre", "C00")], sidecar=Path(tmp) / "absent.tsv")
        self.assertIn("not found", problem or "")

    def test_extra_slug_in_the_sidecar_is_reported(self) -> None:
        """Sidecar lists a row the catalogue no longer diverges on."""
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "d.tsv"
            path.write_text(
                HEADER + "\nB.Fre\tB\tC00\tB.Fre\tfrench-b\n", encoding="utf-8")
            problem = divergence_sidecar_problem(
                [_row("B.Fre", "B00")], sidecar=path)
        self.assertIn("1 stale", problem or "")
        self.assertIn("B.Fre", problem or "")

    def test_missing_slug_in_the_sidecar_is_reported(self) -> None:
        """Catalogue diverges on a row the sidecar does not list — the
        failure mode that would let the headline number rot."""
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "d.tsv"
            path.write_text(HEADER + "\n", encoding="utf-8")
            problem = divergence_sidecar_problem(
                [_row("B.Fre", "C00")], sidecar=path)
        self.assertIn("1 unlisted", problem or "")
        self.assertIn("B.Fre", problem or "")
        self.assertIn("build_eco_divergence.py", problem or "")

    def test_examples_are_capped_at_ten(self) -> None:
        rows = [_row(f"B.Fr{i:02d}", "C00") for i in range(25)]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "d.tsv"
            path.write_text(HEADER + "\n", encoding="utf-8")
            problem = divergence_sidecar_problem(rows, sidecar=path) or ""
        self.assertIn("25 unlisted", problem)
        self.assertIn("...", problem)
        self.assertEqual(
            sum(1 for slug in (r["ocn1"] for r in rows) if slug in problem), 10)

    def test_full_validator_run_is_clean_on_the_live_catalogue(self) -> None:
        proc = subprocess.run(
            [sys.executable, str(REPO_ROOT / "tools" / "validate.py")],
            capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("OK:", proc.stdout)

    def test_fixture_catalogues_do_not_trip_the_check(self) -> None:
        """The check is scoped to the canonical catalogue: the tiny
        validator fixtures carry no sidecar of their own and must keep
        validating cleanly."""
        fixture = REPO_ROOT / "tools" / "tests" / "fixtures" / "valid_minimal.csv"
        proc = subprocess.run(
            [sys.executable, str(REPO_ROOT / "tools" / "validate.py"),
             str(fixture)],
            capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertNotIn("divergence", proc.stderr)


if __name__ == "__main__":
    unittest.main()
