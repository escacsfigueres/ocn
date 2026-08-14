"""Tests for the chronicle sidecar builder.

The cases that matter here are the ones about *not* asserting things:
an unverified person keeps an empty identifier, a mislabelled game is
dropped and reported rather than promoted to a title match, and the
grade says machine-attested rather than verified.

Run:
    python3 -m unittest tools.tests.test_build_chronicle
"""
from __future__ import annotations

import csv
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools"))

import build_chronicle as bc  # noqa: E402


def game(ocn1="C.RyL", white="Steinitz, Wilhelm", black="Zukertort, Johannes",
         year="1886", kind="open", fmt="match", event="World Championship 1st"):
    return {
        "ocn1": ocn1, "kind": kind, "format": fmt, "event": event, "year": year,
        "white": white, "black": black, "result": "1-0", "ply": "8",
        "citation": f"{white}-{black}, {event}, {year}",
    }


class IdentityTests(unittest.TestCase):
    def test_a_person_id_is_the_surname(self) -> None:
        self.assertEqual(bc.person_id("Botvinnik, Mikhail"), "botvinnik")
        self.assertEqual(bc.person_id("Botvinnik, M"), "botvinnik")

    def test_it_folds_accents_rather_than_dropping_them(self) -> None:
        self.assertEqual(bc.person_id("Gligorić, Svetozar"), "gligoric")
        self.assertEqual(bc.person_id("Réti, Richard"), "reti")

    def test_a_two_word_surname_survives_whole(self) -> None:
        self.assertEqual(bc.person_id("Loureda Garcia, Jose"), "loureda-garcia")


class BuildTests(unittest.TestCase):
    def rows(self, n=6, **kwargs):
        return [game(**kwargs) for _ in range(n)]

    def test_a_match_becomes_an_event_with_its_players(self) -> None:
        tables = bc.build(self.rows())
        self.assertEqual(len(tables["events"]), 1)
        event = tables["events"][0]
        self.assertEqual(event["participants"], "steinitz|zukertort")
        self.assertEqual(event["games"], "6")
        self.assertEqual(event["kind"], "wch_match")

    def test_the_womens_title_gets_its_own_event_kind(self) -> None:
        tables = bc.build(self.rows(kind="women", white="Menchik, Vera",
                                    black="Graf, Sonja", event="Wch women"))
        self.assertEqual(tables["events"][0]["kind"], "wch_match_women")

    def test_an_unverified_person_carries_no_identifier(self) -> None:
        """A wrong Wikidata id attaches an opening to the wrong human,
        which is worse than an empty column."""
        tables = bc.build(self.rows())
        for person in tables["people"]:
            with self.subTest(person=person["person_id"]):
                self.assertEqual(person["wikidata_qid"], "")
                self.assertIn("unverified", person["note"])

    def test_the_fuller_spelling_wins_as_the_display_name(self) -> None:
        rows = self.rows(3) + [game(white="Botvinnik, M") for _ in range(3)]
        rows += [game(white="Botvinnik, Mikhail") for _ in range(3)]
        people = {p["person_id"]: p for p in bc.build(rows)["people"]}
        self.assertEqual(people["botvinnik"]["display_name"], "Botvinnik, Mikhail")

    def test_a_claim_carries_a_citation_and_an_honest_grade(self) -> None:
        claim = bc.build(self.rows())["claims"][0]
        self.assertEqual(claim["relation"], "wch-game")
        self.assertEqual(claim["evidence_grade"], "attested")
        self.assertIn("Steinitz", claim["source_ref"])

    def test_games_of_one_opening_are_counted_not_repeated(self) -> None:
        claims = bc.build(self.rows(6))["claims"]
        self.assertEqual(len(claims), 1)
        self.assertEqual(claims[0]["games"], "6")


class ContaminationTests(unittest.TestCase):
    """What a corpus files under a championship and a championship did not play."""

    def test_a_stray_game_is_dropped_and_reported(self) -> None:
        """Two club players inside a legitimate championship group.

        The map cannot see this -- the group as a whole is a real match --
        but regrouping by player pair exposes it.
        """
        rows = [game() for _ in range(6)]
        rows.append(game(white="Garcia Camina, Belarmino",
                         black="Loureda Garcia, Jose Antonio"))
        tables = bc.build(rows)
        pairs = {e["participants"] for e in tables["events"]}
        self.assertEqual(pairs, {"steinitz|zukertort"})
        self.assertTrue(tables["dropped"], "the stray game vanished without a word")
        self.assertIn("too few for a title match", " ".join(tables["dropped"]))

    def test_an_unnamed_player_is_not_a_person(self) -> None:
        rows = [game() for _ in range(6)] + [game(white="?", black="?")]
        tables = bc.build(rows)
        self.assertNotIn("", {p["person_id"] for p in tables["people"]})
        self.assertIn("unnamed player", " ".join(tables["dropped"]))

    def test_a_real_short_match_is_not_mistaken_for_contamination(self) -> None:
        tables = bc.build([game() for _ in range(bc.MIN_MATCH_GAMES)])
        self.assertEqual(len(tables["events"]), 1)
        self.assertFalse(tables["dropped"])


class SidecarTests(unittest.TestCase):
    """The committed tables, when they are there."""

    DIR = REPO_ROOT / "catalog"

    def setUp(self) -> None:
        if not (self.DIR / "ocn-1.claims.tsv").exists():
            self.skipTest("chronicle not built")

    def read(self, name):
        with (self.DIR / name).open(newline="", encoding="utf-8") as handle:
            return list(csv.DictReader(handle, delimiter="\t"))

    def test_every_claim_points_at_a_catalogue_slug(self) -> None:
        with (self.DIR / "ocn-1.csv").open(newline="", encoding="utf-8") as handle:
            slugs = {row["ocn1"] for row in csv.DictReader(handle)}
        missing = sorted({c["ocn1"] for c in self.read("ocn-1.claims.tsv")
                          if c["ocn1"] not in slugs})
        self.assertEqual(missing[:5], [])

    def test_every_event_claim_points_at_a_real_event(self) -> None:
        """Scoped to `subject_type == "event"`. The claims table is one
        table with many entrances, so a place claim's subject is a place
        and looking for it among the events would fail by design."""
        events = {e["event_id"] for e in self.read("ocn-1.events.tsv")}
        missing = sorted({c["subject_id"] for c in self.read("ocn-1.claims.tsv")
                          if c["subject_type"] == "event"
                          and c["subject_id"] not in events})
        self.assertEqual(missing[:5], [])

    def test_every_claim_declares_a_subject_type_we_know(self) -> None:
        """The guard the previous test was silently doing: a subject type
        nobody handles would slip past every check that scopes by it."""
        kinds = {c["subject_type"] for c in self.read("ocn-1.claims.tsv")}
        self.assertLessEqual(kinds, {"event", "place", "person", "publication",
                                     #: A rename's subject is the name the
                                     #: line carried before, not a thing in
                                     #: the world -- so `name` is its own
                                     #: subject type rather than a stand-in.
                                     "name"})

    def test_a_place_claim_names_a_place(self) -> None:
        places = [c for c in self.read("ocn-1.claims.tsv")
                  if c["subject_type"] == "place"]
        if not places:
            self.skipTest("no place claims applied")
        for claim in places:
            with self.subTest(ocn1=claim["ocn1"]):
                self.assertTrue(claim["subject_id"].strip())
                self.assertEqual(claim["relation"], "named-after-place")

    def test_every_event_names_people_the_table_knows(self) -> None:
        people = {p["person_id"] for p in self.read("ocn-1.people.tsv")}
        for event in self.read("ocn-1.events.tsv"):
            for pid in event["participants"].split("|"):
                with self.subTest(event=event["event_id"], person=pid):
                    self.assertIn(pid, people)

    def test_both_championship_lines_are_present(self) -> None:
        kinds = {e["kind"] for e in self.read("ocn-1.events.tsv")}
        self.assertIn("wch_match", kinds)
        self.assertIn("wch_match_women", kinds)


class MergeTests(unittest.TestCase):
    """A regeneration must not be able to destroy a reviewed fact.

    The builder derives its three tables from the championship map, but
    the files it writes have since accumulated things the map cannot
    know: Wikidata identities filled in one person at a time, corrected
    participant spellings, place claims, publication events. Overwriting
    is how all of that disappears.
    """

    def test_a_row_the_builder_does_not_generate_survives(self) -> None:
        existing = [{"event_id": "pub-1561-segura", "kind": "publication",
                     "display_name": "Libro del axedrez"}]
        merged, _ = bc.merge_rows(existing, [], "event_id")
        self.assertEqual(merged, existing)

    def test_a_generated_row_is_added(self) -> None:
        generated = [{"event_id": "wch-1886-steinitz-zukertort", "kind": "wch_match"}]
        merged, report = bc.merge_rows([], generated, "event_id")
        self.assertEqual(merged, generated)
        self.assertEqual(report["added"], 1)

    def test_a_reviewed_identity_is_not_erased_by_an_empty_cell(self) -> None:
        existing = [{"person_id": "steinitz", "display_name": "Steinitz, Wilhelm",
                     "wikidata_qid": "Q106648"}]
        generated = [{"person_id": "steinitz", "display_name": "Steinitz, Wilhelm",
                      "wikidata_qid": ""}]
        merged, _ = bc.merge_rows(existing, generated, "person_id")
        self.assertEqual(merged[0]["wikidata_qid"], "Q106648")

    def test_an_empty_cell_takes_the_generated_value(self) -> None:
        existing = [{"person_id": "steinitz", "display_name": ""}]
        generated = [{"person_id": "steinitz", "display_name": "Steinitz, Wilhelm"}]
        merged, report = bc.merge_rows(existing, generated, "person_id")
        self.assertEqual(merged[0]["display_name"], "Steinitz, Wilhelm")
        self.assertEqual(report["filled"], 1)

    def test_a_correction_wins_over_the_generated_value_and_is_reported(self) -> None:
        """The 13 misspelled participants were corrected in the file, not
        in the map. Regenerating must not put them back."""
        existing = [{"event_id": "wch-2011", "participants": "hou|koneru-humpy"}]
        generated = [{"event_id": "wch-2011", "participants": "hou|koneru"}]
        merged, report = bc.merge_rows(existing, generated, "event_id")
        self.assertEqual(merged[0]["participants"], "hou|koneru-humpy")
        self.assertEqual(report["diverged"], 1)
        self.assertIn(("wch-2011", "participants", "hou|koneru-humpy", "hou|koneru"),
                      report["divergences"])

    def test_a_quoted_source_survives_a_round_trip(self) -> None:
        """Source refs quote the sentence they rest on, so they contain
        quote characters — and a claim's note can begin with one. Merging
        reads the file and writes it back, so a writer that does not quote
        what the reader unquotes corrupts the value on the next rebuild,
        and rewrites four curated claims even when it does not.
        """
        rows = [
            {"ocn1": "B.Mod.Std", "relation": "known-as",
             "subject_id": 'Hooper & Whyld: "Robatsch Defence. 1276"'},
            {"ocn1": "B.Sic.Naj.Rg1", "relation": "renamed",
             "subject_id": '"Freak Attack" is what it was called'},
        ]
        columns = ("ocn1", "relation", "subject_id")
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "claims.tsv"
            bc.write_tsv(path, columns, rows)
            first = path.read_bytes()
            read_back = bc.read_tsv(path)
            self.assertEqual(read_back, rows)

            bc.write_tsv(path, columns, read_back)
            self.assertEqual(path.read_bytes(), first,
                             "a rebuild rewrote the file it just read")

    def test_a_claim_is_identified_by_more_than_one_column(self) -> None:
        """Claims have no id column: the same opening carries a wch-game
        claim and a named-after-place claim, and only the three columns
        together tell them apart."""
        existing = [{"ocn1": "C.RyL", "relation": "named-after-person",
                     "subject_id": "lopez-de-segura", "note": "reviewed"}]
        generated = [{"ocn1": "C.RyL", "relation": "wch-game",
                      "subject_id": "wch-1886", "note": ""}]
        merged, report = bc.merge_rows(
            existing, generated, ("ocn1", "relation", "subject_id")
        )
        self.assertEqual(len(merged), 2)
        self.assertEqual(report["kept"], 1)
        self.assertEqual(report["added"], 1)

    def test_the_curated_rows_keep_their_place_and_new_ones_follow(self) -> None:
        existing = [{"event_id": "pub-1561-segura"}, {"event_id": "wch-1886"}]
        generated = [{"event_id": "wch-1886"}, {"event_id": "wch-1890"}]
        merged, _ = bc.merge_rows(existing, generated, "event_id")
        self.assertEqual([r["event_id"] for r in merged],
                         ["pub-1561-segura", "wch-1886", "wch-1890"])


if __name__ == "__main__":
    unittest.main()
