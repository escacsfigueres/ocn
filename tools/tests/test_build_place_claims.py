"""Tests for the place-claim builder.

The load-bearing case is the exclusion: a place name Wikipedia uses and
the catalogue does not must never become a claim, because
`named-after-place` is a fact about a name and we would be asserting it
of a name we do not use.

Run:
    python3 -m unittest tools.tests.test_build_place_claims
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools"))

import build_place_claims as bp  # noqa: E402


def row(ocn1="A.Eng.Agi", name="English Opening, Agincourt Defence",
        place="Agincourt", relation="named-after-place"):
    return {"ocn1": ocn1, "canonical_name": name, "wikipedia_name": name,
            "place": place, "relation": relation, "moves_san": "1.c4 e6",
            "moves_uci": "c2c4 e7e6", "source_tier": "none",
            "evidence_grade": "traditional", "already_attributed": "",
            "citation": ""}


class SlugTests(unittest.TestCase):
    def test_a_place_becomes_a_stable_id(self) -> None:
        self.assertEqual(bp.slugify("Agincourt"), "agincourt")

    def test_accents_are_folded_not_dropped(self) -> None:
        self.assertEqual(bp.slugify("Göteborg"), "goteborg")

    def test_a_two_word_place_keeps_both(self) -> None:
        self.assertEqual(bp.slugify("St. Petersburg"), "st-petersburg")


class BuildTests(unittest.TestCase):
    def test_a_place_our_name_carries_becomes_a_claim(self) -> None:
        claims, _ = bp.build([row()])
        self.assertEqual(len(claims), 1)
        self.assertEqual(claims[0]["relation"], "named-after-place")
        self.assertEqual(claims[0]["subject_type"], "place")
        self.assertEqual(claims[0]["subject_id"], "agincourt")

    def test_an_alias_candidate_is_never_claimed(self) -> None:
        """Wikipedia calls 1.d4 d5 2.c4 the Aleppo Gambit and we call it
        Queen's Gambit; our row is not named after Aleppo."""
        claims, skipped = bp.build([row(relation="alias-candidate")])
        self.assertEqual(claims, [])
        self.assertTrue(skipped)

    def test_the_grade_is_never_better_than_attested(self) -> None:
        claims, _ = bp.build([row()])
        self.assertEqual(claims[0]["evidence_grade"], "attested")

    def test_the_note_records_why_the_claim_holds(self) -> None:
        claims, _ = bp.build([row()])
        self.assertIn("Agincourt", claims[0]["note"])
        self.assertIn("English Opening", claims[0]["note"])

    def test_the_same_opening_and_place_is_not_claimed_twice(self) -> None:
        claims, skipped = bp.build([row(), row()])
        self.assertEqual(len(claims), 1)
        self.assertIn("duplicate", " ".join(skipped))

    def test_one_opening_may_carry_two_different_places(self) -> None:
        claims, _ = bp.build([row(), row(place="Calais")])
        self.assertEqual({c["subject_id"] for c in claims}, {"agincourt", "calais"})

    def test_a_row_with_no_place_is_skipped(self) -> None:
        claims, skipped = bp.build([row(place="  ")])
        self.assertEqual(claims, [])
        self.assertIn("no place", " ".join(skipped))

    def test_claims_carry_every_column_the_table_needs(self) -> None:
        claims, _ = bp.build([row()])
        self.assertEqual(set(claims[0]), set(bp.CLAIM_COLUMNS))


if __name__ == "__main__":
    unittest.main()
