"""Tests for the Wikipedia eponym reader.

The two things worth pinning down here are the join and the grade. The
join must be by position, because matching "Alekhine Variation" to a row
called "Alekhine Variation" is how two different lines get merged. The
grade must never come out `verified`, because nobody in this pipeline
has read the book the footnote points at.

Run:
    python3 -m unittest tools.tests.test_parse_eponym_lists
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools"))

import parse_eponym_lists as pe  # noqa: E402

OXFORD = ('<ref name="Oxford">{{Citation|surname1=Hooper|title=The Oxford '
          'Companion to Chess|year=1992}}</ref>')


class LinkTests(unittest.TestCase):
    def test_a_plain_link_is_its_own_display(self) -> None:
        self.assertEqual(pe.wiki_links("[[Adolf Albin]]"),
                         [("Adolf Albin", "Adolf Albin")])

    def test_a_piped_link_keeps_both_sides(self) -> None:
        """The target is the Wikipedia article; the display is the name
        a reader sees, and they differ whenever the article is
        disambiguated."""
        self.assertEqual(pe.wiki_links("[[Henry Bird (chess player)|Henry Bird]]"),
                         [("Henry Bird (chess player)", "Henry Bird")])

    def test_two_people_are_both_captured(self) -> None:
        links = pe.wiki_links("[[Armand Blackmar]] and [[Emil Josef Diemer]]")
        self.assertEqual([display for _, display in links],
                         ["Armand Blackmar", "Emil Josef Diemer"])


class RefTests(unittest.TestCase):
    def test_refs_are_lifted_out_of_the_body(self) -> None:
        body, refs = pe.strip_refs(f"*Albin Counter-Gambit{OXFORD}")
        self.assertNotIn("Hooper", body)
        self.assertIn("Hooper", refs)

    def test_a_self_closing_ref_is_lifted_too(self) -> None:
        body, refs = pe.strip_refs('*Bird\'s Opening<ref name="Sunnucks"/>')
        self.assertEqual(body.strip(), "*Bird's Opening")
        self.assertIn("Sunnucks", refs)

    def test_an_sfn_template_counts_as_a_citation(self) -> None:
        """Wikipedia's short-footnote template is a citation even though
        it is not a <ref> tag, and skipping it would grade a cited entry
        as uncited."""
        _, refs = pe.strip_refs("*Amar Opening{{sfn|Hooper|Whyld|1992|p=13}}")
        self.assertIn("Hooper", refs)


class TierTests(unittest.TestCase):
    def test_the_oxford_companion_is_recognised(self) -> None:
        self.assertEqual(pe.source_tier(OXFORD), "oxford-companion")

    def test_an_encyclopaedia_is_recognised(self) -> None:
        self.assertEqual(pe.source_tier("{{citation|last=Sunnucks}}"),
                         "encyclopaedia")

    def test_a_bare_web_citation_is_its_own_tier(self) -> None:
        self.assertEqual(pe.source_tier('<ref>{{cite web|publisher=Chess.com}}</ref>'),
                         "web")

    def test_no_reference_at_all_is_reported_as_such(self) -> None:
        self.assertEqual(pe.source_tier(""), "none")

    def test_nothing_from_this_source_is_ever_verified(self) -> None:
        """`verified` means someone read the page. Following a footnote
        to a book nobody opened is exactly the mistake this project has
        already had to retract once."""
        for tier in ("oxford-companion", "encyclopaedia", "book", "web", "none"):
            with self.subTest(tier=tier):
                self.assertNotEqual(pe.grade_for(tier), "verified")

    def test_an_uncited_entry_is_only_traditional(self) -> None:
        self.assertEqual(pe.grade_for("none"), "traditional")

    def test_a_cited_entry_is_attested(self) -> None:
        self.assertEqual(pe.grade_for("oxford-companion"), "attested")


class EntryTests(unittest.TestCase):
    LINE = ("*[[Albin Countergambit]] – 1.d4 d5 2.c4 e5 – named after "
            f"[[Adolf Albin]]{OXFORD}")

    def test_it_reads_the_name_moves_and_person(self) -> None:
        entry = pe.parse_entry(self.LINE)
        self.assertEqual(entry.people, ["Adolf Albin"])
        self.assertEqual(entry.moves_san, "1.d4 d5 2.c4 e5")
        self.assertIn("Albin Countergambit", entry.wiki_name)

    def test_it_converts_the_moves_to_the_catalogue_s_own_notation(self) -> None:
        self.assertEqual(pe.parse_entry(self.LINE).moves_uci,
                         "d2d4 d7d5 c2c4 e7e5")

    def test_a_line_with_no_moves_is_not_an_entry(self) -> None:
        """Without moves there is no position, and without a position
        there is no join we would trust."""
        self.assertIsNone(pe.parse_entry("*[[Barcza System]] – named after X"))

    def test_an_unparsable_move_is_reported_not_guessed(self) -> None:
        """Wikipedia has typos. A move that is not legal from the
        position means the whole entry is set aside for a human."""
        entry = pe.parse_entry("*Bogus – 1.d4 Nf6 2.c4 e5 3.dxe4 Ng4 – named after [[X]]")
        self.assertIsNotNone(entry)
        self.assertEqual(entry.moves_uci, "")
        self.assertIn("dxe4", entry.problem)

    def test_a_missing_dash_does_not_swallow_the_person(self) -> None:
        """Some entries omit the dash before "named after", which glues
        the clause onto the move list and makes 'named' look like a move."""
        entry = pe.parse_entry("*X – 1.d4 d5 named after [[Someone]]")
        self.assertEqual(entry.moves_san, "1.d4 d5")
        self.assertEqual(entry.people, ["Someone"])

    def test_an_unlinked_person_is_still_a_person(self) -> None:
        entry = pe.parse_entry("*Amar Opening – 1.Nh3 – named after Charles Amar")
        self.assertEqual(entry.people, ["Charles Amar"])

    def test_a_heading_is_not_an_entry(self) -> None:
        self.assertIsNone(pe.parse_entry("==A=="))

    def test_a_maintenance_tag_glued_to_a_move_is_not_a_move(self) -> None:
        """Wikipedia hangs `{{Citation needed}}` off the last move, which
        leaves a stray brace where a move should be."""
        entry = pe.parse_entry("*Wolf Gambit – 1.e4 e6 2.d4 d5 3.Nc3 Nf6 4.Bg5 Bb4 "
                               "5.Nge2{{Citation needed|date=October 2009}}")
        self.assertEqual(entry.problem, "")
        self.assertTrue(entry.moves_uci.endswith("g1e2"))

    def test_a_citation_needed_tag_is_not_a_citation(self) -> None:
        entry = pe.parse_entry("*Wolf Gambit – 1.e4 e5{{Citation needed}}")
        self.assertEqual(entry.tier, "none")
        self.assertEqual(entry.grade, "traditional")

    def test_a_person_appended_with_no_marker_is_still_read(self) -> None:
        """A handful of entries drop the "named after" wording and just
        put the link after the moves."""
        entry = pe.parse_entry("*Soultanbeieff Variation – 1.d4 d5 2.c4 c6 "
                               "[[Victor Soultanbeieff]]")
        self.assertEqual(entry.moves_san, "1.d4 d5 2.c4 c6")
        self.assertEqual(entry.people, ["Victor Soultanbeieff"])


class BulletTests(unittest.TestCase):
    WRAPPED = ("*[[Amar Opening]] – 1.Nh3 – named after Charles Amar<ref>"
               "{{cite web|title=Charles Amar\n|publisher=ChessGames.com}}</ref>")

    def test_a_citation_running_onto_the_next_line_is_rejoined(self) -> None:
        self.assertEqual(len(pe.bullets(self.WRAPPED)), 1)

    def test_a_wrapped_citation_does_not_leak_into_the_person(self) -> None:
        """Read line by line the `<ref>` never closes, and its markup
        ends up inside the person's name."""
        entry = pe.parse_list(self.WRAPPED)[0]
        self.assertEqual(entry.people, ["Charles Amar"])

    def test_a_heading_ends_a_bullet(self) -> None:
        text = "*[[X]] – 1.e4 – named after [[A]]\n==B==\n*[[Y]] – 1.d4 – named after [[B]]"
        self.assertEqual(len(pe.bullets(text)), 2)


class JoinTests(unittest.TestCase):
    CATALOGUE = [
        {"ocn1": "D.Alb", "canonical_name": "Albin Counter-Gambit",
         "moves_uci": "d2d4 d7d5 c2c4 e7e5", "attributed_to": ""},
        {"ocn1": "B.Ale", "canonical_name": "Alekhine Defence",
         "moves_uci": "e2e4 g8f6", "attributed_to": "Alexander Alekhine"},
    ]

    def entry(self, moves="1.d4 d5 2.c4 e5", name="Albin"):
        return pe.parse_entry(f"*{name} – {moves} – named after [[P]]{OXFORD}")

    def test_a_position_match_is_the_join(self) -> None:
        matched, _ = pe.join([self.entry()], self.CATALOGUE)
        self.assertEqual(matched[0].ocn1, "D.Alb")

    def test_a_position_absent_from_the_catalogue_is_reported(self) -> None:
        _, unmatched = pe.join([self.entry(moves="1.g4")], self.CATALOGUE)
        self.assertEqual(len(unmatched), 1)

    def test_an_already_attributed_row_is_flagged_not_overwritten(self) -> None:
        """The catalogue's own attributions were reviewed by a human and
        outrank a footnote."""
        matched, _ = pe.join([self.entry(moves="1.e4 Nf6")], self.CATALOGUE)
        self.assertTrue(matched[0].already_attributed)

    def test_an_entry_that_would_not_convert_never_reaches_the_join(self) -> None:
        broken = pe.parse_entry("*X – 1.d4 Nf6 2.c4 e5 3.dxe4 Ng4 – named after [[P]]")
        matched, unmatched = pe.join([broken], self.CATALOGUE)
        self.assertEqual(matched, [])
        self.assertEqual(len(unmatched), 1)


if __name__ == "__main__":
    unittest.main()
