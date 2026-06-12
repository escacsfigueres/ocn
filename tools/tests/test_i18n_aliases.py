"""Integrity tests for the i18n alias sidecars (Track 2).

One TSV per locale at catalog/ocn-1.aliases.<locale>.tsv with columns
ocn1, name. Partial coverage is by design (display falls back to the
English canonical); what IS in a sidecar must be sound.

Run:
    python3 -m unittest tools.tests.test_i18n_aliases
"""
from __future__ import annotations

import csv
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools"))

from validate import BANNED_CHAR_RE  # noqa: E402

CATALOG = REPO_ROOT / "catalog" / "ocn-1.csv"
SIDECARS = sorted((REPO_ROOT / "catalog").glob("ocn-1.aliases.*.tsv"))


class I18nAliasTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        with CATALOG.open(newline="", encoding="utf-8") as f:
            cls.slugs = {r["ocn1"] for r in csv.DictReader(f)}

    def test_pilot_locales_exist(self) -> None:
        locales = {p.name.split(".")[2] for p in SIDECARS}
        self.assertTrue({"ca", "es"} <= locales, f"found: {locales}")

    def test_sidecars_are_sound(self) -> None:
        for path in SIDECARS:
            with self.subTest(sidecar=path.name):
                with path.open(newline="", encoding="utf-8") as f:
                    reader = csv.DictReader(f, delimiter="\t")
                    self.assertEqual(reader.fieldnames, ["ocn1", "name"])
                    rows = list(reader)
                self.assertTrue(rows)
                seen = set()
                for r in rows:
                    slug, name = r["ocn1"], r["name"]
                    self.assertIn(slug, self.slugs, f"unknown slug {slug}")
                    self.assertNotIn(slug, seen, f"duplicate {slug}")
                    seen.add(slug)
                    self.assertTrue(name.strip(), f"empty name for {slug}")
                    self.assertEqual(name, name.strip())
                    self.assertNotIn("  ", name)
                    self.assertIsNone(BANNED_CHAR_RE.search(name))


if __name__ == "__main__":
    unittest.main()
