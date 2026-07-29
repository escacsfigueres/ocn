"""Tests for tools/lumbra_chronology_helper.py.

The tool does the two DETERMINISTIC, OFFLINE halves of a Lumbra Gigabase
chronology query: (1) `spec` builds a structured first-appearance query spec
from an OCN row (or explicit move/eponym inputs) for a human to run by hand,
and (2) `summarize` turns a saved results file (TSV/JSON of games) into a
deterministic first-appearance evidence line in the house style. The actual
Lumbra fetch is out-of-band; nothing here touches the network or the live
catalogue. All fixtures are tmp files so the suite stays offline.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TOOLS = REPO_ROOT / "tools"
TOOL = TOOLS / "lumbra_chronology_helper.py"

# A tiny self-contained catalogue slice (same columns as catalog/ocn-1.csv).
SLICE_CSV = (
    "ocn1,canonical_name,eco_legacy,parent_ocn1,moves_uci,depth,aliases,flags,"
    "notes,attributed_to,attribution_source,historical_notes,transposes_to,same_as\n"
    "B,Semi-Open Games,,,,0,,,1.e4 with anything but ...e5.,,,,,\n"
    "B.Fre,French Defence,C00,B,e2e4 e7e6,1,,,1.e4 e6.,,,,,\n"
    'B.Fre.Win,"French, Winawer",C18,B.Fre,e2e4 e7e6 d2d4 d7d5 b1c3 f8b4,2,,,'
    "5...a6.,,,,,\n"
)


def run_tool(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(TOOL), *args],
        capture_output=True, text=True, check=False,
    )


class SpecFromSlugTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)
        self.catalog = self.tmp / "slice.csv"
        self.catalog.write_text(SLICE_CSV, encoding="utf-8")

    def test_spec_from_slug_json_has_position(self) -> None:
        r = run_tool("spec", "--catalog", str(self.catalog),
                     "--ocn1", "B.Fre.Win", "--format", "json")
        self.assertEqual(r.returncode, 0, r.stderr)
        payload = json.loads(r.stdout)
        self.assertEqual(payload["kind"], "ocn.lumbra_chronology_query.v1")
        self.assertEqual(payload["ocn1"], "B.Fre.Win")
        self.assertEqual(payload["name"], "French, Winawer")
        self.assertEqual(payload["moves_uci"],
                         "e2e4 e7e6 d2d4 d7d5 b1c3 f8b4")
        # SAN derived from the UCI line (deterministic, offline).
        self.assertIn("e4", payload["moves_san"])
        self.assertIn("Bb4", payload["moves_san"])
        # FEN derived via tools/ocn.py position key (board, side, castling, ep).
        self.assertTrue(payload["fen"].endswith(" w KQkq -")
                        or payload["fen"].split()[1] in {"w", "b"})

    def test_spec_from_slug_infers_eponym_from_name(self) -> None:
        r = run_tool("spec", "--catalog", str(self.catalog),
                     "--ocn1", "B.Fre.Win", "--format", "json")
        payload = json.loads(r.stdout)
        # "French, Winawer" -> eponym candidate "Winawer".
        self.assertEqual(payload["eponym"], "Winawer")

    def test_spec_explicit_eponym_overrides_inferred(self) -> None:
        r = run_tool("spec", "--catalog", str(self.catalog),
                     "--ocn1", "B.Fre.Win", "--eponym", "Szymon Winawer",
                     "--format", "json")
        payload = json.loads(r.stdout)
        self.assertEqual(payload["eponym"], "Szymon Winawer")

    def test_spec_before_year_recorded(self) -> None:
        r = run_tool("spec", "--catalog", str(self.catalog),
                     "--ocn1", "B.Fre.Win", "--before", "1900",
                     "--format", "json")
        payload = json.loads(r.stdout)
        self.assertEqual(payload["before_year"], 1900)

    def test_spec_text_format_is_human_readable(self) -> None:
        r = run_tool("spec", "--catalog", str(self.catalog),
                     "--ocn1", "B.Fre.Win")
        self.assertEqual(r.returncode, 0, r.stderr)
        # Text output names the slug and flags the manual fetch.
        self.assertIn("B.Fre.Win", r.stdout)
        self.assertRegex(r.stdout.lower(), r"manual|by hand|out-of-band|out of band")

    def test_spec_missing_slug_is_data_error(self) -> None:
        r = run_tool("spec", "--catalog", str(self.catalog), "--ocn1", "Z.Nope")
        self.assertEqual(r.returncode, 1)
        self.assertIn("Z.Nope", r.stderr)

    def test_spec_requires_some_input(self) -> None:
        r = run_tool("spec", "--catalog", str(self.catalog))
        self.assertEqual(r.returncode, 2)


class SpecFromExplicitInputsTests(unittest.TestCase):
    def test_spec_from_explicit_moves(self) -> None:
        r = run_tool("spec", "--moves", "e2e4 c7c5",
                     "--eponym", "Sicilian", "--format", "json")
        self.assertEqual(r.returncode, 0, r.stderr)
        payload = json.loads(r.stdout)
        self.assertEqual(payload["moves_uci"], "e2e4 c7c5")
        self.assertIn("c5", payload["moves_san"])
        self.assertEqual(payload["eponym"], "Sicilian")
        # No slug supplied -> ocn1 absent or null.
        self.assertIsNone(payload.get("ocn1"))

    def test_spec_from_explicit_fen_without_moves(self) -> None:
        fen = "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6"
        r = run_tool("spec", "--fen", fen, "--player", "Morphy",
                     "--format", "json")
        self.assertEqual(r.returncode, 0, r.stderr)
        payload = json.loads(r.stdout)
        # FEN is normalised to the catalogue position key (ep dropped when no
        # legal capture; here a black pawn on c5 makes exd6-style irrelevant,
        # but we only assert the board/side survive).
        self.assertTrue(payload["fen"].startswith(
            "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w"))
        self.assertEqual(payload["player"], "Morphy")
        self.assertIsNone(payload.get("moves_uci"))

    def test_spec_invalid_moves_rejected(self) -> None:
        r = run_tool("spec", "--moves", "e2e4 e2e4", "--eponym", "X")
        self.assertEqual(r.returncode, 1)

    def test_spec_eponym_xor_target_required(self) -> None:
        # Explicit input with no eponym and no player: cannot build a search.
        r = run_tool("spec", "--moves", "e2e4 c7c5")
        self.assertEqual(r.returncode, 2)


class SummarizeTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)

    def write_tsv(self, rows: list[str], header: str =
                  "year\twhite\tblack\tevent") -> Path:
        p = self.tmp / "results.tsv"
        p.write_text("\n".join([header, *rows]) + "\n", encoding="utf-8")
        return p

    def test_first_appearance_earliest_year(self) -> None:
        results = self.write_tsv([
            "1924\tRubinstein\tTartakower\tMeran",
            "1888\tAdams\tBird\tManhattan",
            "1953\tNajdorf\tGligoric\tMar del Plata",
        ])
        r = run_tool("summarize", "--results", str(results))
        self.assertEqual(r.returncode, 0, r.stderr)
        # Earliest year wins; house style: Players en-dashed, comma+event+year.
        self.assertIn("1888", r.stdout)
        self.assertIn("Adams", r.stdout)
        self.assertIn("Bird", r.stdout)
        self.assertIn("Manhattan", r.stdout)
        # The 1924 / 1953 games are NOT the first appearance.
        self.assertNotIn("1924", r.stdout)

    def test_evidence_line_house_style_en_dash(self) -> None:
        results = self.write_tsv(["1888\tAdams\tBird\tManhattan"])
        r = run_tool("summarize", "--results", str(results))
        # en-dash (U+2013) between the two players, never a middle dot.
        self.assertIn("Adams–Bird", r.stdout)
        self.assertNotIn("·", r.stdout)
        # Frames it as a type-A corpus fact, not an attribution.
        self.assertRegex(r.stdout.lower(), r"first")

    def test_tie_break_is_stable_on_year(self) -> None:
        # Two games in the same earliest year -> deterministic pick (input order
        # preserved; the first row of the earliest year wins).
        results = self.write_tsv([
            "1900\tZukertort\tSteinitz\tLondon",
            "1900\tAlpha\tBeta\tParis",
        ])
        r1 = run_tool("summarize", "--results", str(results))
        r2 = run_tool("summarize", "--results", str(results))
        self.assertEqual(r1.stdout, r2.stdout)  # deterministic
        self.assertIn("Zukertort", r1.stdout)
        self.assertNotIn("Alpha", r1.stdout)

    def test_before_filter_excludes_later_games(self) -> None:
        results = self.write_tsv([
            "1888\tAdams\tBird\tManhattan",
            "1850\tStaunton\tHorwitz\tLondon",
        ])
        # --before 1880 drops the 1888 game AND keeps only pre-1880; earliest
        # remaining is 1850.
        r = run_tool("summarize", "--results", str(results), "--before", "1880")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("1850", r.stdout)
        self.assertIn("Staunton", r.stdout)
        self.assertNotIn("Adams", r.stdout)

    def test_before_filter_is_strict_exclusive_boundary(self) -> None:
        # A game in the boundary year itself is excluded by --before YEAR.
        results = self.write_tsv([
            "1880\tA\tB\tX",
            "1875\tC\tD\tY",
        ])
        r = run_tool("summarize", "--results", str(results), "--before", "1880")
        self.assertIn("1875", r.stdout)
        self.assertNotIn("1880", r.stdout)

    def test_empty_results_no_first_appearance(self) -> None:
        results = self.write_tsv([])  # header only
        r = run_tool("summarize", "--results", str(results))
        self.assertEqual(r.returncode, 0, r.stderr)
        # Explicit "no games" sentinel, NOT a fabricated date.
        self.assertRegex(r.stdout.lower(), r"no (games|results|matching)")

    def test_before_filter_emptying_all_rows_is_not_error(self) -> None:
        results = self.write_tsv(["1990\tA\tB\tX"])
        r = run_tool("summarize", "--results", str(results), "--before", "1900")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertRegex(r.stdout.lower(), r"no (games|results|matching)")

    def test_json_output(self) -> None:
        results = self.write_tsv([
            "1924\tRubinstein\tTartakower\tMeran",
            "1888\tAdams\tBird\tManhattan",
        ])
        r = run_tool("summarize", "--results", str(results), "--format", "json")
        self.assertEqual(r.returncode, 0, r.stderr)
        payload = json.loads(r.stdout)
        self.assertEqual(payload["first_year"], 1888)
        self.assertEqual(payload["white"], "Adams")
        self.assertEqual(payload["black"], "Bird")
        self.assertEqual(payload["event"], "Manhattan")
        self.assertEqual(payload["count"], 2)
        self.assertIn("evidence_line", payload)

    def test_json_output_empty_has_null_first_year(self) -> None:
        results = self.write_tsv([])
        r = run_tool("summarize", "--results", str(results), "--format", "json")
        payload = json.loads(r.stdout)
        self.assertIsNone(payload["first_year"])
        self.assertEqual(payload["count"], 0)

    def test_json_results_file_accepted(self) -> None:
        # The results file may itself be JSON (list of game objects).
        p = self.tmp / "results.json"
        p.write_text(json.dumps([
            {"year": 1924, "white": "Rubinstein", "black": "Tartakower",
             "event": "Meran"},
            {"year": 1888, "white": "Adams", "black": "Bird",
             "event": "Manhattan"},
        ]), encoding="utf-8")
        r = run_tool("summarize", "--results", str(p), "--format", "json")
        self.assertEqual(r.returncode, 0, r.stderr)
        payload = json.loads(r.stdout)
        self.assertEqual(payload["first_year"], 1888)

    def test_malformed_year_is_error(self) -> None:
        results = self.write_tsv(["not-a-year\tA\tB\tX"])
        r = run_tool("summarize", "--results", str(results))
        self.assertEqual(r.returncode, 1)
        self.assertIn("ERROR", r.stderr)

    def test_missing_required_column_is_error(self) -> None:
        # Header lacks "year".
        p = self.tmp / "bad.tsv"
        p.write_text("white\tblack\tevent\nA\tB\tX\n", encoding="utf-8")
        r = run_tool("summarize", "--results", str(p))
        self.assertEqual(r.returncode, 1)
        self.assertIn("year", r.stderr.lower())

    def test_missing_results_file_is_error(self) -> None:
        r = run_tool("summarize", "--results", str(self.tmp / "nope.tsv"))
        self.assertEqual(r.returncode, 1)

    def test_results_required(self) -> None:
        r = run_tool("summarize")
        self.assertEqual(r.returncode, 2)


class NoSubcommandTests(unittest.TestCase):
    def test_no_subcommand_is_usage_error(self) -> None:
        r = run_tool()
        self.assertEqual(r.returncode, 2)

    def test_help_mentions_manual_fetch(self) -> None:
        r = run_tool("--help")
        self.assertEqual(r.returncode, 0)
        self.assertRegex(r.stdout.lower(), r"lumbra")
        self.assertRegex(r.stdout.lower(), r"manual|by hand|out-of-band|out of band")


if __name__ == "__main__":
    unittest.main()
