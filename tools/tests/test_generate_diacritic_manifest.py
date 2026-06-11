"""Tests for tools/generate_diacritic_manifest.py.

The generator turns the Tier 1 map of docs/diacritic-normalization-map.md
into an `ocn.attribution_manifest.v1` JSON in `naming_strings_only` mode.
It must never hand the engine anything but word-boundary surname
replacements in the six naming columns.

Run:
    python3 -m unittest tools.tests.test_generate_diacritic_manifest
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from generate_diacritic_manifest import (  # noqa: E402
    TIER1_FORMS,
    TIER2_FORMS,
    build_manifest,
    normalize_text,
)


def _row(ocn1: str, **cols: str) -> dict[str, str]:
    base = {
        "ocn1": ocn1,
        "canonical_name": "",
        "eco_legacy": "",
        "parent_ocn1": "",
        "moves_uci": "",
        "depth": "0",
        "aliases": "",
        "flags": "",
        "notes": "",
        "attributed_to": "",
        "attribution_source": "",
        "historical_notes": "",
        "transposes_to": "",
        "same_as": "",
    }
    base.update(cols)
    return base


class NormalizeTextTests(unittest.TestCase):
    def test_replaces_standalone_word_only(self) -> None:
        """Word-boundary: 'Lopez' converts, 'Lopezia' must not."""
        new, targets = normalize_text("Ruy Lopez Defence, Lopezia Line")
        self.assertEqual(new, "Ruy López Defence, Lopezia Line")
        self.assertEqual(targets, {"López"})

    def test_replaces_all_transliteration_variants(self) -> None:
        """Both 'Grunfeld' and 'Gruenfeld' normalize to 'Grünfeld'."""
        new, targets = normalize_text("Gruenfeld beats Grunfeld")
        self.assertEqual(new, "Grünfeld beats Grünfeld")
        self.assertEqual(targets, {"Grünfeld"})

    def test_untouched_text_reports_no_targets(self) -> None:
        new, targets = normalize_text("Sicilian Defence, Najdorf")
        self.assertEqual(new, "Sicilian Defence, Najdorf")
        self.assertEqual(targets, set())


class BuildManifestTests(unittest.TestCase):
    def setUp(self) -> None:
        self.rows = [
            _row("C", canonical_name="Open Games"),
            _row(
                "C.RyL",
                canonical_name="Ruy Lopez Defence",
                notes="The Lopez setup.",
                depth="1",
                parent_ocn1="C",
            ),
            _row(
                "B.Sic",
                canonical_name="Sicilian Defence",
                notes="No surname here.",
                depth="1",
                parent_ocn1="B",
            ),
            _row(
                "A.Ret",
                canonical_name="Reti Opening",
                aliases="Reti System",
                depth="1",
                parent_ocn1="A",
            ),
        ]
        self.manifest = build_manifest(self.rows)

    def test_envelope(self) -> None:
        m = self.manifest
        self.assertEqual(m["kind"], "ocn.attribution_manifest.v1")
        self.assertEqual(m["mode"], "naming_strings_only")
        self.assertEqual(m["expected_catalog_rows"], 4)
        self.assertEqual(m["expected_changed_rows"], ["A.Ret", "C.RyL"])

    def test_changes_carry_only_changed_fields(self) -> None:
        by_slug = {c["ocn1"]: c for c in self.manifest["changes"]}
        self.assertEqual(set(by_slug), {"C.RyL", "A.Ret"})
        self.assertEqual(
            by_slug["C.RyL"]["fields"],
            {
                "canonical_name": "Ruy López Defence",
                "notes": "The López setup.",
            },
        )
        self.assertEqual(
            by_slug["A.Ret"]["fields"],
            {"canonical_name": "Réti Opening", "aliases": "Réti System"},
        )

    def test_changes_are_clear_and_sourced(self) -> None:
        for change in self.manifest["changes"]:
            self.assertEqual(change["evidence_grade"], "CLEAR")
            refs = " ".join(change["source_refs"])
            self.assertIn("diacritic-normalization-map", refs)
            self.assertIn("Wikipedia", refs)


class Tier2Tests(unittest.TestCase):
    def test_tier2_map_matches_the_spec_doc(self) -> None:
        """The Czech/Lithuanian class GO-normalized on 2026-06-11 —
        Sørensen and Würzburger stay parked and must NOT appear."""
        self.assertEqual(
            set(TIER2_FORMS),
            {"Mikėnas", "Krejčík", "Opočenský", "Pelikán"},
        )

    def test_normalize_with_tier2_forms(self) -> None:
        new, targets = normalize_text(
            "English Opening, Mikenas-Carls", forms=TIER2_FORMS
        )
        self.assertEqual(new, "English Opening, Mikėnas-Carls")
        self.assertEqual(targets, {"Mikėnas"})

    def test_tier2_manifest_uses_tier2_map_only(self) -> None:
        rows = [
            _row("A", canonical_name="Flank Openings"),
            _row(
                "A.Mik",
                canonical_name="Mikenas Defence",
                depth="1",
                parent_ocn1="A",
            ),
            _row(
                "C.RyL",
                canonical_name="Ruy Lopez Defence",
                depth="1",
                parent_ocn1="C",
            ),
        ]
        m = build_manifest(rows, tier=2)
        self.assertIn("Tier 2", m["title"])
        self.assertEqual(m["expected_changed_rows"], ["A.Mik"])
        self.assertEqual(
            m["changes"][0]["fields"], {"canonical_name": "Mikėnas Defence"}
        )


class Tier1MapTests(unittest.TestCase):
    def test_map_matches_the_spec_doc(self) -> None:
        """The ten Tier 1 targets of docs/diacritic-normalization-map.md,
        no more, no less — a drift guard between code and spec."""
        self.assertEqual(
            set(TIER1_FORMS),
            {
                "López", "Grünfeld", "Réti", "Sämisch", "Maróczy",
                "Göring", "Hübner", "Löwenthal", "Hromádka", "Møller",
            },
        )


if __name__ == "__main__":
    unittest.main()
