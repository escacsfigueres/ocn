"""Tests for `ocn annotate` and the `ocn.annotate` module.

The PGNs are built here from the catalogue's own `moves_uci`, converted
to SAN by the vendored move generator, so a fixture can never drift away
from the row it is supposed to reach: if the Najdorf English Attack line
changes, the fixture changes with it and the assertion still means what
it says.

Run from a checkout without installing anything:

    python3 -m unittest discover -s tests
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from ocn import Catalog  # noqa: E402
from ocn._chess import validate_uci_sequence  # noqa: E402
from ocn.annotate import (  # noqa: E402
    Annotator,
    Stats,
    annotate_text,
    iter_games,
    mainline_tokens,
)

SRC = REPO_ROOT / "src"
NAJDORF_ENGLISH = "B.Sic.Naj.Eng"


def san_line(catalog: Catalog, slug: str) -> list[str]:
    """The catalogue row's own moves, as SAN."""
    return validate_uci_sequence(" ".join(catalog.by_slug(slug).moves_uci))


def movetext(sans: list[str], result: str = "1-0") -> str:
    """SAN moves as numbered movetext, the way a PGN writes them."""
    parts: list[str] = []
    for index, san in enumerate(sans):
        if index % 2 == 0:
            parts.append(f"{index // 2 + 1}.")
        parts.append(san)
    parts.append(result)
    return " ".join(parts)


def game(movetext_body: str, *, headers: dict[str, str] | None = None) -> str:
    tags = {
        "Event": "Test",
        "Site": "?",
        "Date": "2026.07.29",
        "Round": "1",
        "White": "White Player",
        "Black": "Black Player",
        "Result": "1-0",
    }
    tags.update(headers or {})
    header_block = "".join(f'[{name} "{value}"]\n' for name, value in tags.items())
    return f"{header_block}\n{movetext_body}\n\n"


def run_cli(*args: str, stdin: str | None = None) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ, PYTHONPATH=str(SRC))
    return subprocess.run(
        [sys.executable, "-m", "ocn.cli", *args],
        cwd=REPO_ROOT,
        env=env,
        input=stdin,
        text=True,
        capture_output=True,
        check=False,
    )


class SharedCatalog(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.catalog = Catalog.load()
        cls.annotator = Annotator(cls.catalog)


class MovetextParsingTests(SharedCatalog):
    def test_variations_are_skipped(self) -> None:
        tokens = mainline_tokens("1. e4 e5 (1... c5 2. Nf3 (2. c3) d6) 2. Nf3 Nc6 *")
        self.assertEqual(tokens, ["e4", "e5", "Nf3", "Nc6"])

    def test_comments_nags_and_suffixes_are_dropped(self) -> None:
        tokens = mainline_tokens(
            "1. e4 {a comment (with a paren)} e5 $1 2. Nf3!? ; trailing\n Nc6 1/2-1/2"
        )
        self.assertEqual(tokens, ["e4", "e5", "Nf3!?", "Nc6"])

    def test_lichess_clock_comments_and_repeated_numbers(self) -> None:
        """The shape a Lichess export actually has."""
        tokens = mainline_tokens(
            "1. e4 { [%clk 0:03:00] } 1... c5 { [%clk 0:03:00] } "
            "2. Nf3 { [%eval 0.21] } 2... d6?! { [%clk 0:02:55] } 1-0"
        )
        self.assertEqual(tokens, ["e4", "c5", "Nf3", "d6?!"])

    def test_black_first_move_numbers_are_stripped(self) -> None:
        self.assertEqual(mainline_tokens("15... Nf6 16. Bg5"), ["Nf6", "Bg5"])

    def test_games_split_on_the_tag_section(self) -> None:
        text = game("1. e4 e5 1-0") + game("1. d4 d5 0-1", headers={"Round": "2"})
        games = list(iter_games(text.splitlines(keepends=True)))
        self.assertEqual(len(games), 2)
        self.assertEqual(games[1].header("Round"), "2")
        self.assertEqual("".join(one.text for one in games), text)

    def test_a_bracket_inside_a_comment_does_not_start_a_game(self) -> None:
        text = game('1. e4 {see [Event "elsewhere"]\nstill the comment} e5 1-0')
        games = list(iter_games(text.splitlines(keepends=True)))
        self.assertEqual(len(games), 1)


class MatchingTests(SharedCatalog):
    def test_najdorf_english_attack_is_named(self) -> None:
        pgn = game(movetext(san_line(self.catalog, NAJDORF_ENGLISH)), headers={"ECO": "B90"})
        out, stats = annotate_text(pgn, annotator=self.annotator)
        self.assertIn(f'[OCN "{NAJDORF_ENGLISH}"]', out)
        self.assertIn('[OCNName "Sicilian Najdorf, English Attack"]', out)
        self.assertEqual(stats.matched, 1)

    def test_tags_land_after_the_eco_header(self) -> None:
        pgn = game(movetext(san_line(self.catalog, NAJDORF_ENGLISH)), headers={"ECO": "B90"})
        out, _ = annotate_text(pgn, annotator=self.annotator)
        lines = [line for line in out.splitlines() if line.startswith("[")]
        self.assertEqual(
            lines[lines.index('[ECO "B90"]') + 1], f'[OCN "{NAJDORF_ENGLISH}"]'
        )
        self.assertEqual(
            lines[lines.index('[ECO "B90"]') + 2],
            '[OCNName "Sicilian Najdorf, English Attack"]',
        )

    def test_tags_land_after_round_when_there_is_no_eco(self) -> None:
        pgn = game(movetext(san_line(self.catalog, NAJDORF_ENGLISH)))
        out, _ = annotate_text(pgn, annotator=self.annotator)
        lines = [line for line in out.splitlines() if line.startswith("[")]
        self.assertEqual(lines[lines.index('[Round "1"]') + 1], f'[OCN "{NAJDORF_ENGLISH}"]')

    def test_transposed_move_order_reaches_the_same_slug(self) -> None:
        """1.Nf3 into the Najdorf: prefix matching would miss this."""
        direct = game(movetext(san_line(self.catalog, NAJDORF_ENGLISH)))
        transposed = game(
            "1. Nf3 c5 2. e4 d6 3. d4 cxd4 4. Nxd4 Nf6 5. Nc3 a6 6. Be3 1-0"
        )
        direct_out, _ = annotate_text(direct, annotator=self.annotator)
        transposed_out, stats = annotate_text(transposed, annotator=self.annotator)
        self.assertIn(f'[OCN "{NAJDORF_ENGLISH}"]', transposed_out)
        self.assertEqual(stats.matched, 1)
        self.assertEqual(
            [line for line in direct_out.splitlines() if line.startswith("[OCN")],
            [line for line in transposed_out.splitlines() if line.startswith("[OCN")],
        )

    def test_deepest_position_along_the_way_wins(self) -> None:
        """The Sicilian is passed through; the Najdorf is where it ends."""
        tokens = san_line(self.catalog, NAJDORF_ENGLISH)
        match = self.annotator.match_tokens(tokens)
        self.assertEqual(match.slug, NAJDORF_ENGLISH)
        self.assertEqual(match.ply, len(tokens))
        self.assertEqual(self.annotator.match_tokens(tokens[:2]).slug, "B.Sic")

    def test_transposes_to_is_resolved_to_the_canonical_slug(self) -> None:
        row = self._transposing_row()
        out, _ = annotate_text(
            game(movetext(validate_uci_sequence(" ".join(row.moves_uci)))),
            annotator=self.annotator,
        )
        canonical = self.catalog.resolve(row.ocn1)
        self.assertNotEqual(canonical, row.ocn1)
        self.assertIn(f'[OCN "{canonical}"]', out)
        self.assertNotIn(f'[OCN "{row.ocn1}"]', out)

    def _transposing_row(self):
        """A row that transposes into a target with no co-canonical twin.

        `same_as` partners are both canonical at one position, so the
        pick between them is a display choice rather than a resolution;
        this test is about resolution.
        """
        for row in self.catalog:
            target = self.catalog.get(row.transposes_to or "")
            if row.moves_uci and target and not target.same_as:
                return row
        self.skipTest("no transposing row in the catalogue")

    def test_comments_nags_and_variations_do_not_change_the_result(self) -> None:
        plain = game("1. e4 c5 2. Nf3 d6 3. d4 cxd4 4. Nxd4 Nf6 5. Nc3 a6 1-0")
        noisy = game(
            "1. e4 {best by test} c5 $1 2. Nf3 (2. Nc3 Nc6 (2... d6 3. f4)) d6\n"
            "3. d4 cxd4 4. Nxd4 Nf6 ; a trailing comment\n"
            "5. Nc3 a6!? {the Najdorf} 1-0"
        )
        plain_out, _ = annotate_text(plain, annotator=self.annotator)
        noisy_out, stats = annotate_text(noisy, annotator=self.annotator)
        self.assertEqual(stats.errors, 0)
        self.assertIn('[OCN "B.Sic.Naj"]', noisy_out)
        self.assertEqual(
            [line for line in plain_out.splitlines() if line.startswith("[OCN")],
            [line for line in noisy_out.splitlines() if line.startswith("[OCN")],
        )

    def test_an_unmatched_game_is_left_alone(self) -> None:
        """Every legal first move is a catalogue row, so the only
        unmatched game is one with no moves at all — the abandoned game
        every real dump carries."""
        pgn = game("*", headers={"Result": "*"})
        out, stats = annotate_text(pgn, annotator=self.annotator)
        self.assertEqual(out, pgn)
        self.assertEqual((stats.games, stats.matched), (1, 0))

    def test_a_stale_ocn_tag_is_dropped_from_an_unmatched_game(self) -> None:
        pgn = game("*", headers={"Result": "*", "OCN": "B.Sic", "OCNName": "wrong"})
        out, _ = annotate_text(pgn, annotator=self.annotator)
        self.assertNotIn("[OCN ", out)

    def test_an_illegal_move_stops_the_game_without_stopping_the_file(self) -> None:
        """A broken game keeps what it reached; the file keeps the game."""
        broken = game("1. e4 c5 2. Nf3 Qxh8 1-0", headers={"Round": "2"})
        pgn = game(movetext(san_line(self.catalog, NAJDORF_ENGLISH))) + broken
        out, stats = annotate_text(pgn, annotator=self.annotator)
        self.assertEqual((stats.games, stats.matched, stats.errors), (2, 2, 1))
        self.assertIn(f'[OCN "{NAJDORF_ENGLISH}"]', out)
        self.assertEqual(out.count("[OCN "), 2)
        self.assertIn("2. Nf3 Qxh8 1-0", out)

    def test_max_plies_bounds_the_replay(self) -> None:
        tokens = san_line(self.catalog, NAJDORF_ENGLISH)
        shallow = Annotator(self.catalog, max_plies=2).match_tokens(tokens)
        self.assertEqual((shallow.slug, shallow.ply), ("B.Sic", 2))


class FidelityTests(SharedCatalog):
    def test_movetext_is_not_reflowed(self) -> None:
        body = "1. e4 c5\n2. Nf3    d6 {kept}\n3. d4 cxd4 1-0"
        out, _ = annotate_text(game(body), annotator=self.annotator)
        self.assertIn(body, out)

    def test_unknown_headers_and_order_survive(self) -> None:
        pgn = game("1. e4 c5 1-0", headers={"WhiteElo": "2700", "Variant": "Standard"})
        out, _ = annotate_text(pgn, annotator=self.annotator)
        kept = [line for line in out.splitlines() if line.startswith("[")]
        self.assertEqual(
            [line for line in kept if not line.startswith("[OCN")],
            [line for line in pgn.splitlines() if line.startswith("[")],
        )

    def test_annotating_twice_is_idempotent(self) -> None:
        pgn = game(movetext(san_line(self.catalog, NAJDORF_ENGLISH)), headers={"ECO": "B90"})
        once, _ = annotate_text(pgn, annotator=self.annotator)
        twice, _ = annotate_text(once, annotator=self.annotator)
        self.assertEqual(once, twice)

    def test_carriage_returns_survive(self) -> None:
        pgn = game("1. e4 c5 1-0").replace("\n", "\r\n")
        out, _ = annotate_text(pgn, annotator=self.annotator)
        self.assertIn('[OCN "B.Sic"]\r\n', out)
        self.assertEqual(out.count("\n"), out.count("\r\n"))  # no bare newline added


class StatsTests(SharedCatalog):
    def _stats(self) -> Stats:
        pgn = (
            game(movetext(san_line(self.catalog, NAJDORF_ENGLISH)))
            + game("1. e4 c5 1-0", headers={"Round": "2"})
            + game("*", headers={"Round": "3", "Result": "*"})
        )
        return annotate_text(pgn, annotator=self.annotator)[1]

    def test_totals_and_rate(self) -> None:
        stats = self._stats()
        self.assertEqual((stats.games, stats.matched, stats.errors), (3, 2, 0))
        self.assertAlmostEqual(stats.match_rate, 200 / 3, places=6)

    def test_median_depth_in_plies(self) -> None:
        stats = self._stats()
        self.assertAlmostEqual(stats.median_ply, (11 + 2) / 2)

    def test_top_openings_are_ranked(self) -> None:
        stats = self._stats()
        top = stats.top(10)
        self.assertEqual(len(top), 2)
        self.assertEqual({slug for slug, _, _ in top}, {NAJDORF_ENGLISH, "B.Sic"})
        self.assertTrue(all(count == 1 for _, _, count in top))

    def test_top_is_capped(self) -> None:
        self.assertLessEqual(len(self._stats().top(1)), 1)

    def test_text_summary_shape(self) -> None:
        text = self._stats().format_text()
        self.assertRegex(text, r"games\s+3")
        self.assertRegex(text, r"matched\s+2\s+\(66\.7%\)")
        self.assertRegex(text, r"median depth\s+6\.5 plies")
        self.assertIn("top 2 openings", text)

    def test_json_summary_shape(self) -> None:
        payload = self._stats().as_dict()
        self.assertEqual(payload["games"], 3)
        self.assertEqual(payload["matched"], 2)
        self.assertEqual(payload["median_ply"], 6.5)
        self.assertEqual(
            sorted(entry["ocn1"] for entry in payload["top"]),
            sorted([NAJDORF_ENGLISH, "B.Sic"]),
        )


class CommandLineTests(SharedCatalog):
    def setUp(self) -> None:
        self.pgn = game(
            movetext(san_line(self.catalog, NAJDORF_ENGLISH)), headers={"ECO": "B90"}
        )

    def test_annotate_a_file_to_stdout(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "games.pgn"
            path.write_text(self.pgn, encoding="utf-8")
            result = run_cli("annotate", str(path))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(f'[OCN "{NAJDORF_ENGLISH}"]', result.stdout)

    def test_annotate_from_stdin(self) -> None:
        result = run_cli("annotate", "-", stdin=self.pgn)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(f'[OCN "{NAJDORF_ENGLISH}"]', result.stdout)
        self.assertIn("1. e4 c5", result.stdout)

    def test_out_file_and_stats_on_stderr(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory) / "annotated.pgn"
            result = run_cli("annotate", "-", "--out", str(out), "--stats", stdin=self.pgn)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, "")
            self.assertIn(f'[OCN "{NAJDORF_ENGLISH}"]', out.read_text(encoding="utf-8"))
        self.assertIn("matched", result.stderr)
        self.assertIn("top 1 openings", result.stderr)

    def test_stats_json(self) -> None:
        result = run_cli("annotate", "-", "--stats", "--json", stdin=self.pgn)
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stderr)
        self.assertEqual(payload["games"], 1)
        self.assertEqual(payload["matched"], 1)
        self.assertEqual(payload["match_rate"], 100.0)
        self.assertEqual(payload["top"][0]["ocn1"], NAJDORF_ENGLISH)

    def test_garbage_input_exits_two(self) -> None:
        result = run_cli("annotate", "-", stdin="this is not a PGN file at all\n")
        self.assertEqual(result.returncode, 2)
        self.assertIn("no PGN games found", result.stderr)

    def test_empty_input_exits_two(self) -> None:
        result = run_cli("annotate", "-", stdin="")
        self.assertEqual(result.returncode, 2)
        self.assertIn("ERROR", result.stderr)

    def test_missing_file_exits_two(self) -> None:
        result = run_cli("annotate", "/nonexistent/does-not-exist.pgn")
        self.assertEqual(result.returncode, 2)
        self.assertIn("ERROR", result.stderr)

    def test_a_file_with_no_match_exits_one_and_still_writes(self) -> None:
        result = run_cli("annotate", "-", stdin=game("*", headers={"Result": "*"}))
        self.assertEqual(result.returncode, 1)
        self.assertIn('[Event "Test"]', result.stdout)

    def test_help(self) -> None:
        result = run_cli("annotate", "--help")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("usage:", result.stdout)


if __name__ == "__main__":
    unittest.main()
