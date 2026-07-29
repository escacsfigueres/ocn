"""Tests for the people resolver.

Almost every case here is about refusing to answer. Attaching a wrong
Wikidata identifier to a person silently attaches every opening they
played to the wrong human, and nothing downstream can detect it -- so
the resolver has to prefer an empty column to a plausible guess, and
these tests are what hold it to that.

Run:
    python3 -m unittest tools.tests.test_resolve_people
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools"))

import resolve_people as rp  # noqa: E402


def candidate(qid="Q1", label="Wilhelm Steinitz", description="chess player",
              born=1836, died=1900, is_player=True):
    return rp.Candidate(qid=qid, label=label, description=description,
                        born=born, died=died, is_player=is_player)


class WindowTests(unittest.TestCase):
    """The years a person was actually seen playing, from the championship map."""

    def rows(self):
        return [
            {"white": "Steinitz, Wilhelm", "black": "Zukertort, Johannes", "year": "1886"},
            {"white": "Lasker, Emanuel", "black": "Steinitz, Wilhelm", "year": "1894"},
            {"white": "Steinitz, Wilhelm", "black": "Lasker, Emanuel", "year": "1896"},
        ]

    def test_it_spans_first_to_last_appearance(self) -> None:
        window = rp.activity_window(self.rows())
        self.assertEqual(window["steinitz"], (1886, 1896))

    def test_it_counts_a_person_playing_either_colour(self) -> None:
        window = rp.activity_window(self.rows())
        self.assertEqual(window["lasker"], (1894, 1896))

    def test_an_undated_game_does_not_widen_the_window(self) -> None:
        rows = self.rows() + [{"white": "Steinitz, Wilhelm",
                               "black": "Lasker, Emanuel", "year": ""}]
        self.assertEqual(rp.activity_window(rows)["steinitz"], (1886, 1896))


class PlausibilityTests(unittest.TestCase):
    """The years are the verification. A surname is not."""

    def test_a_contemporary_is_plausible(self) -> None:
        self.assertTrue(rp.plausible(candidate(), 1886, 1896))

    def test_someone_born_after_the_games_is_not_the_player(self) -> None:
        """The failure this whole tool exists to prevent: a modern
        namesake collected for a nineteenth-century champion."""
        modern = candidate(qid="Q2", label="Steinitz", born=1963, died=None)
        self.assertFalse(rp.plausible(modern, 1886, 1896))

    def test_someone_dead_before_the_last_game_is_not_the_player(self) -> None:
        self.assertFalse(rp.plausible(candidate(died=1890), 1886, 1896))

    def test_dying_in_the_year_of_the_last_game_is_allowed(self) -> None:
        """Players do die in the year they last played."""
        self.assertTrue(rp.plausible(candidate(died=1896), 1886, 1896))

    def test_a_child_could_not_have_played_it(self) -> None:
        self.assertFalse(rp.plausible(candidate(born=1884, died=1960), 1886, 1896))

    def test_an_implausibly_old_player_is_rejected(self) -> None:
        self.assertFalse(rp.plausible(candidate(born=1700, died=1900), 1886, 1896))

    def test_a_living_player_needs_no_death_date(self) -> None:
        carlsen = candidate(qid="Q106807", label="Magnus Carlsen", born=1990, died=None)
        self.assertTrue(rp.plausible(carlsen, 2013, 2023))

    def test_an_undated_candidate_cannot_be_verified(self) -> None:
        """No birth year means no way to test the match, and an
        unverifiable match is exactly what the empty column is for."""
        self.assertFalse(rp.plausible(candidate(born=None), 1886, 1896))


class ResolutionTests(unittest.TestCase):
    def test_one_surviving_candidate_is_the_answer(self) -> None:
        qid, reason = rp.resolve([candidate()], (1886, 1896))
        self.assertEqual(qid, "Q1")
        self.assertIn("Steinitz", reason)

    def test_no_survivor_leaves_the_column_empty(self) -> None:
        qid, reason = rp.resolve([candidate(born=1963, died=None)], (1886, 1896))
        self.assertEqual(qid, "")
        self.assertIn("no candidate", reason)

    def test_two_survivors_leave_the_column_empty(self) -> None:
        """Ambiguity is reported, never broken by picking the first."""
        pair = [candidate(qid="Q1"), candidate(qid="Q2", label="W. Steinitz")]
        qid, reason = rp.resolve(pair, (1886, 1896))
        self.assertEqual(qid, "")
        self.assertIn("Q1", reason)
        self.assertIn("Q2", reason)

    def test_a_non_player_is_discarded_before_the_dates_are_read(self) -> None:
        """A violinist born in the right decade still is not the champion."""
        violinist = candidate(qid="Q9", label="Steinitz", description="violinist",
                              is_player=False)
        qid, _ = rp.resolve([violinist, candidate()], (1886, 1896))
        self.assertEqual(qid, "Q1")

    def test_a_person_with_no_window_is_not_resolved(self) -> None:
        qid, reason = rp.resolve([candidate()], None)
        self.assertEqual(qid, "")
        self.assertIn("no games", reason)


class EntityParsingTests(unittest.TestCase):
    """Reading Wikidata's JSON without trusting it to be complete."""

    def entity(self, claims):
        return {"id": "Q1", "labels": {"en": {"value": "Wilhelm Steinitz"}},
                "descriptions": {"en": {"value": "Austrian chess player"}},
                "claims": claims}

    def dated(self, prop, iso):
        return {prop: [{"mainsnak": {"datavalue": {"value": {"time": iso}}}}]}

    def item(self, prop, qid):
        return {prop: [{"mainsnak": {"datavalue": {"value": {"id": qid}}}}]}

    def test_it_reads_a_year_from_a_wikidata_timestamp(self) -> None:
        parsed = rp.parse_entity(self.entity(self.dated("P569", "+1836-05-14T00:00:00Z")))
        self.assertEqual(parsed.born, 1836)

    def test_it_reads_a_year_before_the_common_era(self) -> None:
        """Negative timestamps must not be parsed as a positive year."""
        parsed = rp.parse_entity(self.entity(self.dated("P569", "-0500-01-01T00:00:00Z")))
        self.assertEqual(parsed.born, -500)

    def test_occupation_chess_player_marks_a_player(self) -> None:
        parsed = rp.parse_entity(self.entity(self.item("P106", rp.Q_CHESS_PLAYER)))
        self.assertTrue(parsed.is_player)

    def test_a_fide_identifier_also_marks_a_player(self) -> None:
        """Plenty of players carry a FIDE id and some other occupation."""
        claims = {"P1440": [{"mainsnak": {"datavalue": {"value": "1503014"}}}]}
        self.assertTrue(rp.parse_entity(self.entity(claims)).is_player)

    def test_someone_with_neither_is_not_a_player(self) -> None:
        parsed = rp.parse_entity(self.entity(self.item("P106", "Q1259917")))
        self.assertFalse(parsed.is_player)

    def test_a_missing_claim_does_not_raise(self) -> None:
        parsed = rp.parse_entity({"id": "Q1", "labels": {}, "descriptions": {},
                                  "claims": {}})
        self.assertIsNone(parsed.born)
        self.assertEqual(parsed.label, "")

    def test_a_snak_with_no_value_is_skipped(self) -> None:
        """Wikidata records 'unknown value' as a snak without a datavalue."""
        claims = {"P569": [{"mainsnak": {"snaktype": "somevalue"}}]}
        self.assertIsNone(rp.parse_entity(self.entity(claims)).born)


class SearchTermTests(unittest.TestCase):
    def test_a_corpus_name_is_turned_around_for_searching(self) -> None:
        self.assertIn("Wilhelm Steinitz", rp.search_terms("Steinitz, Wilhelm"))

    def test_the_bare_surname_is_tried_too(self) -> None:
        """Transliterated given names miss; the surname alone often hits."""
        self.assertIn("Steinitz", rp.search_terms("Steinitz, Wilhelm"))

    def test_an_initial_is_not_searched_as_a_given_name(self) -> None:
        terms = rp.search_terms("Bikova, E.")
        self.assertNotIn("E. Bikova", terms)
        self.assertIn("Bikova", terms)

    def test_a_middle_initial_gets_a_second_chance_without_it(self) -> None:
        """"Jan H Timman" finds nothing; "Jan Timman" is the article."""
        self.assertIn("Jan Timman", rp.search_terms("Timman, Jan H"))

    def test_the_corpus_spelling_is_searched_verbatim_too(self) -> None:
        """Dropping the initial is not always the improvement it looks
        like: Bobby Fischer answers to "Robert J Fischer", which is a
        recorded alias, and not to "Robert Fischer", which is not."""
        self.assertIn("Robert J Fischer", rp.search_terms("Fischer, Robert J"))

    def test_the_surname_first_order_is_tried(self) -> None:
        """Wikidata titles Chinese players surname first, and "Yifan
        Hou" is not an article while "Hou Yifan" is."""
        self.assertIn("Hou Yifan", rp.search_terms("Hou, Yifan"))

    def test_a_corpus_tag_never_reaches_the_search(self) -> None:
        terms = rp.search_terms("Hou, Yifan(HLJ)")
        self.assertIn("Hou Yifan", terms)
        self.assertFalse([t for t in terms if "(" in t])

    def test_terms_are_not_repeated(self) -> None:
        """A single given name makes two of the four forms identical."""
        self.assertEqual(len(rp.search_terms("Steinitz, Wilhelm")),
                         len(set(rp.search_terms("Steinitz, Wilhelm"))))


class GivenNameTests(unittest.TestCase):
    def test_it_reads_the_first_given_name(self) -> None:
        self.assertEqual(rp.given_name("Timman, Jan H"), "Jan")

    def test_an_initial_only_yields_nothing(self) -> None:
        self.assertEqual(rp.given_name("Bikova, E."), "")

    def test_the_given_name_breaks_a_tie_between_relatives(self) -> None:
        """Three Polgárs were alive and playing at once, so the dates
        cannot separate them, but the corpus says which one it means."""
        polgars = [
            candidate(qid="Q12823", label="Susan Polgar", born=1969, died=None),
            candidate(qid="Q183250", label="Judit Polgár", born=1976, died=None),
            candidate(qid="Q923742", label="László Polgár", born=1946, died=None),
        ]
        self.assertEqual(rp.resolve(polgars, (1996, 1996), "Susan")[0], "Q12823")

    def test_a_given_name_matching_two_of_them_still_refuses(self) -> None:
        pair = [candidate(qid="Q1", label="Susan Polgar", born=1969, died=None),
                candidate(qid="Q2", label="Susan Polgar-Smith", born=1970, died=None)]
        self.assertEqual(rp.resolve(pair, (1996, 1996), "Susan")[0], "")


if __name__ == "__main__":
    unittest.main()
