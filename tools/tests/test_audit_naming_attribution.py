"""Tests for tools/audit_naming_attribution.py."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TOOLS = REPO_ROOT / "tools"
TOOL = TOOLS / "audit_naming_attribution.py"
CATALOG = REPO_ROOT / "catalog" / "ocn-1.csv"

sys.path.insert(0, str(TOOLS))
import audit_naming_attribution as ana  # noqa: E402


def make_row(name: str, *, aliases: str = "", depth: str = "1", ocn1: str = "X.Y",
             parent: str = "", attributed_to: str = "", attribution_source: str = "",
             historical_notes: str = "") -> dict[str, str]:
    return {
        "ocn1": ocn1,
        "canonical_name": name,
        "eco_legacy": "",
        "parent_ocn1": parent,
        "moves_uci": "",
        "depth": depth,
        "aliases": aliases,
        "flags": "",
        "notes": "",
        "attributed_to": attributed_to,
        "attribution_source": attribution_source,
        "historical_notes": historical_notes,
        "transposes_to": "",
        "same_as": "",
    }


def classify(row, parent_row=None, has_children=False, family_has_template=False):
    return ana.classify_row(
        row,
        parent_row=parent_row,
        has_children=has_children,
        family_has_template=family_has_template,
    )


def run_tool(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(TOOL), *args],
        capture_output=True,
        text=True,
        check=False,
    )


class ClassificationUnitTests(unittest.TestCase):
    def test_descriptor_row_is_ignore(self) -> None:
        r = classify(make_row("Some Variation, Main Line"))
        self.assertEqual(r["category"], ana.CAT_DESCRIPTOR)
        self.assertEqual(r["recommended_next_action"], ana.ACT_IGNORE)
        self.assertEqual(r["risk_level"], ana.RISK_LOW)

    def test_gambit_row_is_ignore(self) -> None:
        r = classify(make_row("Queen's Gambit Accepted"))
        self.assertEqual(r["category"], ana.CAT_GAMBIT)
        self.assertEqual(r["recommended_next_action"], ana.ACT_IGNORE)

    def test_metaphor_row_is_ignore(self) -> None:
        r = classify(make_row("Sicilian Dragon Variation"))
        # 'sicilian' is geo but a surname/metaphor takes precedence over geo
        self.assertEqual(r["category"], ana.CAT_METAPHOR)
        self.assertEqual(r["recommended_next_action"], ana.ACT_IGNORE)

    def test_already_attributed_row(self) -> None:
        r = classify(make_row("Whatever Defence", attributed_to="Some Person"))
        self.assertEqual(r["category"], ana.CAT_ALREADY)
        self.assertEqual(r["recommended_next_action"], ana.ACT_ALREADY)

    def test_dangerous_surname_is_individual_proposal(self) -> None:
        r = classify(make_row("Tarrasch Defence", ocn1="D.Tar"))
        self.assertEqual(r["category"], ana.CAT_PERSON)
        self.assertEqual(r["risk_level"], ana.RISK_HIGH)
        self.assertEqual(r["recommended_next_action"], ana.ACT_INDIVIDUAL)

    def test_moderate_surname_no_template_is_source_sprint(self) -> None:
        r = classify(make_row("French, Winawer", ocn1="B.Fre.Win"))
        self.assertEqual(r["category"], ana.CAT_PERSON)
        self.assertEqual(r["risk_level"], ana.RISK_MEDIUM)
        self.assertEqual(r["recommended_next_action"], ana.ACT_SOURCE)

    def test_eponym_with_family_template_is_batch_candidate(self) -> None:
        r = classify(make_row("French, Winawer", ocn1="B.Fre.Win"),
                     family_has_template=True)
        self.assertEqual(r["recommended_next_action"], ana.ACT_BATCH)

    def test_inheriting_child_is_ignored(self) -> None:
        parent = make_row("Tarrasch Defence", ocn1="D.Tar")
        child = classify(
            make_row("Tarrasch Defence, Main Line", ocn1="D.Tar.MLn", parent="D.Tar"),
            parent_row=parent,
        )
        self.assertEqual(child["recommended_next_action"], ana.ACT_IGNORE)
        self.assertFalse(child["head_candidate"])

    def test_geo_family_is_ignore_low(self) -> None:
        r = classify(make_row("Sicilian Defence", ocn1="B.Sic"))
        self.assertEqual(r["category"], ana.CAT_PLACE)
        self.assertEqual(r["recommended_next_action"], ana.ACT_IGNORE)
        self.assertEqual(r["risk_level"], ana.RISK_LOW)

    def test_event_token_is_source_sprint(self) -> None:
        r = classify(make_row("QGD, Carlsbad Variation", ocn1="D.QGD.Exc.Car"))
        self.assertEqual(r["category"], ana.CAT_PLACE)
        self.assertEqual(r["recommended_next_action"], ana.ACT_SOURCE)


class CatalogIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        result = run_tool("--format", "json")
        assert result.returncode == 0, result.stderr
        payload = json.loads(result.stdout)
        cls.by_slug = {r["ocn1"]: r for r in payload["rows"]}
        cls.groups = payload["eponym_head_groups"]

    def test_known_applied_rows_are_already_attributed(self) -> None:
        for slug in ("B.Sic.Naj", "D.QGD.Cmb", "A.Tro", "B.Sic.Acc.Mar"):
            with self.subTest(slug=slug):
                self.assertIn(slug, self.by_slug)
                self.assertEqual(self.by_slug[slug]["category"], ana.CAT_ALREADY)
                self.assertEqual(
                    self.by_slug[slug]["recommended_next_action"], ana.ACT_ALREADY
                )

    def test_winawer_is_source_sprint_or_batch(self) -> None:
        row = self.by_slug["B.Fre.Win"]
        self.assertEqual(row["category"], ana.CAT_PERSON)
        self.assertEqual(row["risk_level"], ana.RISK_MEDIUM)
        self.assertIn(
            row["recommended_next_action"], (ana.ACT_SOURCE, ana.ACT_BATCH)
        )

    def test_descriptor_category_invariant(self) -> None:
        # Every descriptor / gambit / metaphor row must be ignore_descriptor.
        for slug, r in self.by_slug.items():
            if r["category"] in (ana.CAT_DESCRIPTOR, ana.CAT_GAMBIT, ana.CAT_METAPHOR):
                self.assertEqual(
                    r["recommended_next_action"], ana.ACT_IGNORE, msg=slug
                )

    def test_dangerous_surname_groups_are_high_risk(self) -> None:
        for g in self.groups:
            if g["surname"] in ana.DANGEROUS_SURNAMES:
                self.assertEqual(g["risk_level"], ana.RISK_HIGH)

    def test_tool_does_not_mutate_catalog(self) -> None:
        before = hashlib.sha256(CATALOG.read_bytes()).hexdigest()
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "report.tsv"
            result = run_tool("--out", str(out), "--summary")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(out.exists())
        after = hashlib.sha256(CATALOG.read_bytes()).hexdigest()
        self.assertEqual(before, after)

    def test_summary_line_shape(self) -> None:
        result = run_tool("--summary")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("SUMMARY ", result.stderr)
        self.assertIn("rows=", result.stderr)
        self.assertIn("person_eponym=", result.stderr)


class DangerousSeedSyncTests(unittest.TestCase):
    """The dangerous multi-head surname seed must match the factory map."""

    def test_nimzowitsch_is_dangerous_multihead(self) -> None:
        # ~126 rows across unrelated openings (B.Nim, E.Nim, A.Lar alias...):
        # never blanket-attributable, must be individual_proposal.
        r = classify(make_row("Nimzowitsch Defence", ocn1="B.Nim"))
        self.assertEqual(r["risk_level"], ana.RISK_HIGH)
        self.assertEqual(r["recommended_next_action"], ana.ACT_INDIVIDUAL)

    def test_factory_map_dangerous_surnames_present(self) -> None:
        # docs/whole-catalogue-attribution-factory-map.md verified counts.
        expected = {
            "tarrasch", "chigorin", "rubinstein", "steinitz", "marshall",
            "bogoljubow", "nimzowitsch", "botvinnik", "keres", "lasker",
            "paulsen",
        }
        self.assertTrue(expected <= ana.DANGEROUS_SURNAMES,
                        expected - ana.DANGEROUS_SURNAMES)
        self.assertFalse(expected & ana.MODERATE_SURNAMES,
                         expected & ana.MODERATE_SURNAMES)


if __name__ == "__main__":
    unittest.main()
