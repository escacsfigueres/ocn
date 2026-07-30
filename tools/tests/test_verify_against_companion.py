"""Tests for the Companion verifier's parsing.

The network is never touched here. What matters is that a reply is
matched back to the row it answers -- a reply attached to the wrong row
would put one opening's citation on another's attribution, which is the
same silent error the position join exists to prevent.

Run:
    python3 -m unittest tools.tests.test_verify_against_companion
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools"))

import verify_against_companion as vc  # noqa: E402


def row(ocn1="A.Ama", name="Amar Opening", moves="1.Nh3"):
    return {"ocn1": ocn1, "canonical_name": name, "wikipedia_name": name,
            "moves_san": moves, "person": "Charles Amar", "source_tier": "web",
            "already_attributed": ""}


class LabelTests(unittest.TestCase):
    def test_the_parent_clause_is_dropped(self) -> None:
        r = row(name="Adams Attack of the Sicilian Defence")
        self.assertEqual(vc.label_for(r), "Adams Attack")

    def test_a_pipe_never_survives_into_a_label(self) -> None:
        """The reply format is pipe-delimited, so a pipe in a label
        would split one answer into two fields."""
        self.assertNotIn("|", vc.label_for(row(name="Odd | Name")))

    def test_an_empty_name_falls_back_to_the_slug(self) -> None:
        self.assertEqual(vc.label_for(row(name="")), "A.Ama")


class PromptTests(unittest.TestCase):
    def test_every_opening_is_numbered_with_its_moves(self) -> None:
        prompt = vc.build_prompt([row(), row("A.Bar", "Barnes Opening", "1.f3")])
        self.assertIn("1) Amar Opening = 1.Nh3", prompt)
        self.assertIn("2) Barnes Opening = 1.f3", prompt)

    def test_the_prompt_forbids_guessing(self) -> None:
        self.assertIn("Do not guess", vc.build_prompt([row()]))


class ParseTests(unittest.TestCase):
    BATCH = [row(), row("A.Bar", "Barnes Opening", "1.f3"),
             row("A.Clm", "Clemenz Opening", "1.h3")]

    def test_a_numbered_reply_goes_to_the_row_at_that_position(self) -> None:
        answer = "2) Barnes Opening | 1282 | Barnes Opening, 1282, of little merit. | unclear | none"
        got = vc.parse_answer(answer, self.BATCH)
        self.assertIn("A.Bar", got)
        self.assertEqual(got["A.Bar"]["companion_index"], "1282")
        self.assertEqual(got["A.Bar"]["role"], "unclear")

    def test_none_is_recorded_as_no_entry(self) -> None:
        got = vc.parse_answer("1) Amar Opening | NONE", self.BATCH)
        self.assertEqual(got["A.Ama"]["verdict"], "no-entry")

    def test_an_unnumbered_reply_is_matched_by_its_label(self) -> None:
        got = vc.parse_answer("Clemenz Opening | 1323 | named after Hermann Clemenz. "
                              "| originated | none", self.BATCH)
        self.assertEqual(got["A.Clm"]["companion_index"], "1323")

    def test_a_reply_naming_no_row_is_discarded(self) -> None:
        """Better to lose an answer than to file it under the wrong
        opening."""
        self.assertEqual(vc.parse_answer("Sicilian Najdorf | 500 | x | y | z",
                                         self.BATCH), {})

    def test_prose_around_the_table_is_ignored(self) -> None:
        answer = ("Here are the entries you asked about:\n\n"
                  "1) Amar Opening | 1324 | Amar Opening, 1324. | unclear | none\n\n"
                  "Would you like me to check anything else?")
        got = vc.parse_answer(answer, self.BATCH)
        self.assertEqual(set(got), {"A.Ama"})

    def test_a_bulleted_reply_still_parses(self) -> None:
        got = vc.parse_answer("* 1) Amar Opening | 1324 | q | unclear | none", self.BATCH)
        self.assertEqual(got["A.Ama"]["companion_index"], "1324")

    def test_a_position_outside_the_batch_is_not_forced(self) -> None:
        self.assertEqual(vc.parse_answer("9) Something | 1 | q | r | s", self.BATCH), {})

    def test_a_quote_containing_no_role_still_records_the_quote(self) -> None:
        got = vc.parse_answer("1) Amar Opening | 1324 | Amar Opening, 1324.", self.BATCH)
        self.assertEqual(got["A.Ama"]["quote"], "Amar Opening, 1324.")
        self.assertEqual(got["A.Ama"]["role"], "")


class SelectionTests(unittest.TestCase):
    def test_an_already_attributed_row_is_never_asked_about(self) -> None:
        import csv
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "in.tsv"
            cols = ["ocn1", "canonical_name", "wikipedia_name", "moves_san",
                    "person", "source_tier", "already_attributed"]
            with path.open("w", newline="", encoding="utf-8") as handle:
                w = csv.DictWriter(handle, cols, delimiter="\t")
                w.writeheader()
                w.writerow({**{c: "" for c in cols}, "ocn1": "A.One",
                            "source_tier": "web"})
                w.writerow({**{c: "" for c in cols}, "ocn1": "A.Two",
                            "source_tier": "web", "already_attributed": "yes"})
            got = vc.rows_to_ask(path, None, None, set())
            self.assertEqual([r["ocn1"] for r in got], ["A.One"])


if __name__ == "__main__":
    unittest.main()
