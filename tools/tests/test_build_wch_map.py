"""Tests for the world championship mapper.

No network, no external corpus: the fixtures are inline PGN, and every
case here is one the real 10-million-game corpus actually produced. The
event filter went through three drafts before the structural rule
replaced it, and each draft's leak has a test so it cannot come back.

Run:
    python3 -m unittest tools.tests.test_build_wch_map
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def _load_mapper():
    """Import the mapper without leaving its path behind.

    `tools/ocn.py` and the installable `ocn` package share a name, and
    the mapper needs the package. Importing it here would otherwise pin
    `src/` at the front of sys.path and hand the package to
    `test_ocn.py`, whose subject is the other module entirely -- a
    failure that only appears when the whole suite runs, which is the
    worst kind. So the path is restored and the `ocn` modules are
    dropped from the cache, leaving the next importer to resolve its own.
    """
    import importlib

    saved_path = list(sys.path)
    saved_modules = {name: mod for name, mod in sys.modules.items()
                     if name == "ocn" or name.startswith("ocn.")}
    sys.path.insert(0, str(REPO_ROOT / "tools"))
    try:
        module = importlib.import_module("build_wch_map")
    finally:
        sys.path[:] = saved_path
        for name in [n for n in sys.modules if n == "ocn" or n.startswith("ocn.")]:
            del sys.modules[name]
        sys.modules.update(saved_modules)
    return module


_mapper = _load_mapper()
MATCH_MAX = _mapper.MATCH_MAX
MATCH_MIN = _mapper.MATCH_MIN
classify_event = _mapper.classify_event
surname_of = _mapper.surname_of
year_of = _mapper.year_of


class EventNameTests(unittest.TestCase):
    """The name filter narrows the field; it does not decide."""

    def test_it_admits_the_title_events(self) -> None:
        for event in (
            "World Championship 1st",
            "World Championship 31th-KK1",
            "Wch",
            "WCh 2024",
            "Steinitz - Zukertort World Championship Match",
            "PCA-World Championship",
            "FIDE-Wch",
        ):
            with self.subTest(event=event):
                self.assertIsNotNone(classify_event(event), event)

    def test_the_womens_title_is_its_own_kind(self) -> None:
        for event in ("Wch women", "WCh Women 2020", "Wch (Women) Pitsunda/Tbilisi"):
            with self.subTest(event=event):
                verdict = classify_event(event)
                self.assertIsNotNone(verdict)
                self.assertEqual(verdict[0], "women")

    def test_the_open_title_is_not_labelled_women(self) -> None:
        self.assertEqual(classify_event("World Championship 20th")[0], "open")

    def test_knockout_editions_are_a_separate_format(self) -> None:
        self.assertEqual(classify_event("FIDE WCh KO")[1], "knockout")
        self.assertEqual(classify_event("FIDE-Wch k.o.")[1], "knockout")
        self.assertEqual(classify_event("World Championship 20th")[1], "match")

    def test_it_rejects_what_only_wears_the_name(self) -> None:
        """Every entry here leaked through an earlier draft of the filter.

        The first let in 33,000 games; the second still carried the
        physically-disabled association, two email federations and a
        university championship.
        """
        for event in (
            "Wch U20 final-A",          # age-restricted
            "Duisburg Wch U12m",        # the gendered suffix beat \\bu\\d+\\b
            "Halle wch-jr",             # the abbreviation beat \\bjunior\\b
            "World Championship Amateur",
            "WchT U26 11. fin-A",       # team
            "XI WCh-Blind",
            "Wch Silent",               # deaf chess
            "24. IPCA WCh 2025",        # physically disabled
            "15. IECG WCH-F-00004",     # email chess federation
            "2. LSS WCH F-00005",       # server chess federation
            "2. CC World Ch Final",     # correspondence
            "World Ch corres",
            "10. WCh-University",
            "Lyon wch stud tt",
            "Wch candidates qf",        # its own event kind
            "Wch Blitz",
        ):
            with self.subTest(event=event):
                self.assertIsNone(classify_event(event), event)

    def test_an_unrelated_event_is_not_a_championship(self) -> None:
        for event in ("Hastings", "Linares", "Corus Wijk aan Zee", ""):
            with self.subTest(event=event):
                self.assertIsNone(classify_event(event))


class PlayerIdentityTests(unittest.TestCase):
    """One man, several spellings."""

    def test_a_surname_survives_the_variants(self) -> None:
        self.assertEqual(surname_of("Botvinnik, Mikhail"), "botvinnik")
        self.assertEqual(surname_of("Botvinnik, M"), "botvinnik")
        self.assertEqual(surname_of("Botvinnik"), "botvinnik")
        self.assertEqual(surname_of("BOTVINNIK, Mikhail M"), "botvinnik")

    def test_a_missing_name_is_empty_rather_than_a_player(self) -> None:
        self.assertEqual(surname_of(None), "")
        self.assertEqual(surname_of(""), "")


class ShapeTests(unittest.TestCase):
    """What a title match is, structurally."""

    def test_the_bounds_hold_the_real_matches(self) -> None:
        #: The longest title match ever played, Karpov against Kasparov
        #: in 1984, was abandoned after 48 games; the shortest run in the
        #: corpus is a handful.
        self.assertLessEqual(MATCH_MIN, 4)
        self.assertGreaterEqual(MATCH_MAX, 48)

    def test_the_bounds_exclude_a_knockout_field(self) -> None:
        #: A knockout edition brings 128 players and several hundred
        #: games, which is what the shape rule is for.
        self.assertLess(MATCH_MAX, 300)


class DateTests(unittest.TestCase):
    def test_a_year_is_read_or_left_empty(self) -> None:
        self.assertEqual(year_of("1886.01.11"), "1886")
        self.assertEqual(year_of("2024.??.??"), "2024")
        self.assertEqual(year_of("????.??.??"), "")
        self.assertEqual(year_of(None), "")


class SidecarTests(unittest.TestCase):
    """The committed map, when it is there."""

    SIDECAR = REPO_ROOT / "catalog" / "ocn-1.wch.tsv"

    def setUp(self) -> None:
        if not self.SIDECAR.exists():
            self.skipTest("championship map not built")

    def test_the_columns_are_the_documented_ones(self) -> None:
        header = self.SIDECAR.read_text(encoding="utf-8").splitlines()[0]
        self.assertEqual(header.split("\t")[:5], ["ocn1", "kind", "format", "event", "year"])

    def test_every_row_names_a_catalogue_slug(self) -> None:
        #: The catalogue is read from the CSV rather than through either
        #: `ocn` module: the package and `tools/ocn.py` share a name, and
        #: importing one here puts the other's tests on the wrong path.
        import csv

        with (REPO_ROOT / "catalog" / "ocn-1.csv").open(newline="", encoding="utf-8") as f:
            slugs = {row["ocn1"] for row in csv.DictReader(f)}
        with self.SIDECAR.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle, delimiter="\t"))
        self.assertTrue(rows)
        missing = sorted({r["ocn1"] for r in rows if r["ocn1"] not in slugs})
        self.assertEqual(missing[:5], [], "rows point at slugs the catalogue does not have")

    def test_both_championship_lines_are_present(self) -> None:
        import csv

        with self.SIDECAR.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle, delimiter="\t"))
        kinds = {r["kind"] for r in rows}
        self.assertIn("open", kinds)
        self.assertIn("women", kinds, "the women's championship is first class here")

    def test_it_reaches_back_to_the_first_championship(self) -> None:
        import csv

        with self.SIDECAR.open(newline="", encoding="utf-8") as handle:
            years = [r["year"] for r in csv.DictReader(handle, delimiter="\t") if r["year"]]
        self.assertLessEqual(int(min(years)), 1886, "Steinitz against Zukertort is the floor")


if __name__ == "__main__":
    unittest.main()
