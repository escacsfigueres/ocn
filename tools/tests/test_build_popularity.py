"""Tests for tools/build_popularity.py — the popularity sidecar (H2.7).

**No test here touches the network.** Every API response is canned, shaped
after the official examples published in `lichess-org/api`
(`doc/specs/examples/openingExplorer-*.json.yaml`) and validated against
the schemas in the same repo, so the parsing contract is pinned without
depending on a live service, a token, or today's game counts.

There is deliberately **no drift test**. The other sidecars are derived
from the catalogue, so regenerating them must be a no-op and CI can pin
the bytes. This one is a *snapshot of a moving external database*: the
numbers change whenever Lichess indexes another game, and a byte-pinning
test would fail on every honest refresh. What is pinned instead is the
shape — header, field count, column types, the ISO `retrieved` date —
which is what a consumer actually depends on, plus a row count that
tracks the catalogue.

Run:
    python3 -m unittest tools.tests.test_build_popularity
"""
from __future__ import annotations

import importlib.util
import json
import re
import sys
import tempfile
import unittest
import urllib.error
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TOOLS = REPO_ROOT / "tools"

_SPEC = importlib.util.spec_from_file_location(
    "ocn_build_popularity", TOOLS / "build_popularity.py")
assert _SPEC and _SPEC.loader
build_popularity = importlib.util.module_from_spec(_SPEC)
# Registered before execution: the module defines dataclasses, and
# @dataclass resolves annotations through sys.modules[cls.__module__].
sys.modules["ocn_build_popularity"] = build_popularity
_SPEC.loader.exec_module(build_popularity)

bp = build_popularity

POPULARITY_TSV = REPO_ROOT / "catalog" / "ocn-1.popularity.tsv"
POSITIONS_TSV = bp.DEFAULT_POSITIONS

#: A `/masters` response in the shape the API documents: W/D/B totals and
#: a `topGames` sample whose players sit on both colours. Carlsen at 2881
#: is the strongest here and he is playing *white* in one game and
#: *black* in another, which is exactly the case a colour-blind top-player
#: pick has to get right.
MASTERS_PAYLOAD = {
    "opening": {"eco": "D06", "name": "Queen's Gambit Declined"},
    "white": 1927,
    "draws": 5215,
    "black": 1469,
    "moves": [],
    "topGames": [
        {"uci": "c6d5", "id": "kN6d9l2i", "winner": "black",
         "black": {"name": "Anand, V.", "rating": 2785},
         "white": {"name": "Carlsen, M.", "rating": 2881},
         "year": 2014, "month": "2014-06"},
        {"uci": "c6d5", "id": "qeYPJL2y", "winner": "white",
         "black": {"name": "Carlsen, M.", "rating": 2843},
         "white": {"name": "So, W.", "rating": 2778},
         "year": 2018, "month": "2018-06"},
        {"uci": "c6d5", "id": "VpWYyv3g", "winner": None,
         "black": {"name": "Kramnik, V.", "rating": 2770},
         "white": {"name": "Karjakin, S.", "rating": 2760},
         "year": 2009, "month": "2009-11"},
    ],
}

LICHESS_PAYLOAD = {
    "opening": None,
    "white": 5061745,
    "draws": 492487,
    "black": 4458129,
    "moves": [],
    "topGames": [],
    "recentGames": [],
}

#: A position no game in either database has reached. The explorer
#: answers with zeroes and empty samples rather than a 404.
EMPTY_PAYLOAD = {
    "opening": None, "white": 0, "draws": 0, "black": 0,
    "moves": [], "topGames": [],
}


class TopPlayerTests(unittest.TestCase):
    def test_picks_the_highest_rating_across_both_colours(self) -> None:
        name, rating = bp.top_player_of(MASTERS_PAYLOAD["topGames"])
        self.assertEqual((name, rating), ("Carlsen, M.", 2881))

    def test_finds_a_leader_who_only_ever_plays_black(self) -> None:
        games = [{"white": {"name": "Weak, A.", "rating": 2100},
                  "black": {"name": "Strong, B.", "rating": 2800}, "year": 2001}]
        self.assertEqual(bp.top_player_of(games), ("Strong, B.", 2800))

    def test_empty_sample_yields_no_player(self) -> None:
        self.assertEqual(bp.top_player_of([]), ("", None))
        self.assertEqual(bp.top_player_of(None), ("", None))

    def test_ties_break_deterministically_on_the_name(self) -> None:
        games = [{"white": {"name": "Zukertort, J.", "rating": 2600},
                  "black": {"name": "Anderssen, A.", "rating": 2600}, "year": 1878}]
        self.assertEqual(bp.top_player_of(games), ("Anderssen, A.", 2600))

    def test_players_without_a_rating_are_skipped(self) -> None:
        games = [{"white": {"name": "Unrated, U."},
                  "black": {"name": "Rated, R.", "rating": 2400}, "year": 1950}]
        self.assertEqual(bp.top_player_of(games), ("Rated, R.", 2400))

    def test_malformed_entries_do_not_crash(self) -> None:
        self.assertEqual(bp.top_player_of([None, {}, {"white": "nope"}]), ("", None))


class SampledYearTests(unittest.TestCase):
    def test_range_spans_the_sample(self) -> None:
        self.assertEqual(
            bp.sampled_year_range(MASTERS_PAYLOAD["topGames"]), (2009, 2018))

    def test_single_game_gives_an_identical_pair(self) -> None:
        self.assertEqual(bp.sampled_year_range([{"year": 1999}]), (1999, 1999))

    def test_no_sample_gives_no_years(self) -> None:
        self.assertEqual(bp.sampled_year_range([]), (None, None))

    def test_entries_without_a_year_are_ignored(self) -> None:
        self.assertEqual(
            bp.sampled_year_range([{"year": 2000}, {}, {"year": None}]),
            (2000, 2000))


class SummaryTests(unittest.TestCase):
    def test_masters_totals_are_the_sum_of_the_three_outcomes(self) -> None:
        summary = bp.summarise_masters(MASTERS_PAYLOAD)
        self.assertEqual(summary.games, 1927 + 5215 + 1469)
        self.assertEqual(
            (summary.white, summary.draws, summary.black), (1927, 5215, 1469))
        self.assertEqual(summary.top_player, "Carlsen, M.")
        self.assertEqual(summary.top_player_elo, 2881)
        self.assertEqual((summary.year_earliest, summary.year_latest), (2009, 2018))

    def test_empty_position_summarises_to_zero_and_nothing(self) -> None:
        summary = bp.summarise_masters(EMPTY_PAYLOAD)
        self.assertEqual(summary.games, 0)
        self.assertEqual(summary.top_player, "")
        self.assertIsNone(summary.top_player_elo)
        self.assertIsNone(summary.year_earliest)
        self.assertIsNone(summary.year_latest)

    def test_total_games_of_the_lichess_pool(self) -> None:
        self.assertEqual(
            bp.total_games(LICHESS_PAYLOAD), 5061745 + 492487 + 4458129)

    def test_missing_keys_count_as_zero(self) -> None:
        self.assertEqual(bp.total_games({}), 0)


class RowTests(unittest.TestCase):
    def test_row_has_every_column_in_order(self) -> None:
        row = bp.popularity_row(
            "A.Eng", MASTERS_PAYLOAD, LICHESS_PAYLOAD, "2026-07-29")
        self.assertEqual(len(row), len(bp.FIELDS))
        self.assertEqual(row, [
            "A.Eng", "8611", "1927", "5215", "1469", "10012361",
            "Carlsen, M.", "2881", "2009", "2018", "2026-07-29",
        ])

    def test_unplayed_position_keeps_zeroes_but_empties_the_samples(self) -> None:
        # A zero is a measurement -- "no game in this database reached
        # this position" -- so the count columns stay numeric. The
        # sample-derived columns have nothing to say and stay empty.
        row = bp.popularity_row("X.Y", EMPTY_PAYLOAD, EMPTY_PAYLOAD, "2026-07-29")
        self.assertEqual(row, ["X.Y", "0", "0", "0", "0", "0", "", "", "", "",
                               "2026-07-29"])

    def test_row_never_contains_a_tab_or_newline(self) -> None:
        row = bp.popularity_row(
            "A.Eng", MASTERS_PAYLOAD, LICHESS_PAYLOAD, "2026-07-29")
        for cell in row:
            with self.subTest(cell=cell):
                self.assertNotIn("\t", cell)
                self.assertNotIn("\n", cell)


class RenderTests(unittest.TestCase):
    def test_header_matches_the_documented_columns(self) -> None:
        self.assertEqual(bp.HEADER.split("\t"), [
            "ocn1", "masters_games", "masters_white", "masters_draws",
            "masters_black", "lichess_games", "top_player", "top_player_elo",
            "top_game_year_earliest", "top_game_year_latest", "retrieved",
        ])

    def test_render_emits_header_then_rows(self) -> None:
        text = bp.render_tsv([
            bp.popularity_row("A.Eng", MASTERS_PAYLOAD, LICHESS_PAYLOAD, "2026-07-29"),
            bp.popularity_row("X.Y", EMPTY_PAYLOAD, EMPTY_PAYLOAD, "2026-07-29"),
        ])
        lines = text.splitlines()
        self.assertEqual(lines[0], bp.HEADER)
        self.assertEqual(len(lines), 3)
        self.assertTrue(text.endswith("\n"))
        for line in lines:
            with self.subTest(line=line):
                self.assertEqual(len(line.split("\t")), 11)

    def test_empty_input_still_renders_a_header(self) -> None:
        self.assertEqual(bp.render_tsv([]), bp.HEADER + "\n")


class CacheTests(unittest.TestCase):
    def test_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = bp.cache_file(Path(tmp), "masters", "some fen/key w KQkq -")
            bp.write_cache(path, "some fen/key w KQkq -", MASTERS_PAYLOAD)
            self.assertEqual(
                bp.read_cache(path, "some fen/key w KQkq -"), MASTERS_PAYLOAD)

    def test_filename_is_safe_for_a_fen_full_of_slashes(self) -> None:
        fen_key = "rnbqkbnr/pppppppp/8/8/2P5/8/PP1PPPPP/RNBQKBNR b KQkq -"
        path = bp.cache_file(Path("/tmp/x"), "masters", fen_key)
        self.assertNotIn("/", path.name)
        self.assertNotIn(" ", path.name)
        self.assertTrue(path.name.endswith(".json"))

    def test_a_different_position_is_a_miss_not_a_wrong_answer(self) -> None:
        # The filename is a hash; the payload must still prove which
        # position it belongs to, so a collision cannot go unnoticed.
        with tempfile.TemporaryDirectory() as tmp:
            path = bp.cache_file(Path(tmp), "masters", "key-a")
            bp.write_cache(path, "key-a", MASTERS_PAYLOAD)
            self.assertIsNone(bp.read_cache(path, "key-b"))

    def test_absent_and_corrupt_files_are_misses(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            missing = Path(tmp) / "nope.json"
            self.assertIsNone(bp.read_cache(missing, "k"))
            corrupt = Path(tmp) / "bad.json"
            corrupt.write_text("{not json", encoding="utf-8")
            self.assertIsNone(bp.read_cache(corrupt, "k"))

    def test_no_temp_file_survives_a_write(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = bp.cache_file(Path(tmp), "masters", "k")
            bp.write_cache(path, "k", EMPTY_PAYLOAD)
            self.assertEqual(
                sorted(p.name for p in path.parent.iterdir()), [path.name])


class UrlTests(unittest.TestCase):
    FEN = "rnbqkbnr/pppppppp/8/8/2P5/8/PP1PPPPP/RNBQKBNR b KQkq - 0 1"

    def test_masters_url_carries_the_fen_and_a_top_games_sample(self) -> None:
        url = bp.masters_url(self.FEN)
        self.assertTrue(url.startswith(bp.EXPLORER_BASE + "/masters?"))
        self.assertIn("topGames=4", url)
        self.assertIn("2P5", url)
        self.assertNotIn(" ", url)

    def test_lichess_url_pins_the_speeds_and_rating_bands(self) -> None:
        url = bp.lichess_url(self.FEN)
        self.assertTrue(url.startswith(bp.EXPLORER_BASE + "/lichess?"))
        # These two define what `lichess_games` counts, so they are part
        # of the artefact's meaning, not a tuning knob.
        self.assertIn("speeds=blitz%2Crapid%2Cclassical", url)
        self.assertIn("ratings=1800%2C2000%2C2200%2C2500", url)
        self.assertIn("topGames=0", url)
        self.assertIn("recentGames=0", url)

    def test_the_source_is_the_public_explorer_and_nothing_else(self) -> None:
        self.assertEqual(bp.EXPLORER_BASE, "https://explorer.lichess.ovh")


class BackoffTests(unittest.TestCase):
    class Headers:
        def __init__(self, value): self._value = value
        def get(self, _name): return self._value

    def test_retry_after_header_wins(self) -> None:
        self.assertEqual(bp.retry_after_seconds(self.Headers("17"), 0), 17.0)

    def test_backoff_is_exponential_without_a_header(self) -> None:
        delays = [bp.retry_after_seconds(None, n) for n in range(4)]
        self.assertEqual(delays, [5.0, 10.0, 20.0, 40.0])

    def test_backoff_is_capped(self) -> None:
        self.assertEqual(
            bp.retry_after_seconds(None, 99), bp.BACKOFF_CAP_SECONDS)

    def test_absurd_retry_after_is_capped_too(self) -> None:
        self.assertEqual(
            bp.retry_after_seconds(self.Headers("99999"), 0),
            bp.BACKOFF_CAP_SECONDS)

    def test_unparseable_retry_after_falls_back_to_backoff(self) -> None:
        self.assertEqual(bp.retry_after_seconds(self.Headers("soon"), 1), 10.0)


class FakeResponse:
    def __init__(self, payload): self._payload = payload
    def __enter__(self): return self
    def __exit__(self, *_): return False
    def read(self): return json.dumps(self._payload).encode("utf-8")


class ClientTests(unittest.TestCase):
    """The client is exercised with an injected opener: still no network."""

    def http_error(self, code: str | int, reason: str, headers=None):
        """An HTTPError that closes itself when the test ends.

        `HTTPError` is a file-like object; one that is never closed emits
        a ResourceWarning during interpreter shutdown and turns an
        otherwise clean CI log into noise.
        """
        error = urllib.error.HTTPError("https://x", code, reason, headers, None)
        self.addCleanup(error.close)
        return error

    def make_client(self, responses, **kwargs):
        self.slept: list[float] = []
        self.now = [0.0]
        calls: list[str] = []

        def opener(request, timeout=None):
            calls.append(request.full_url)
            result = responses.pop(0)
            if isinstance(result, Exception):
                raise result
            return FakeResponse(result)

        def sleep(seconds):
            self.slept.append(seconds)
            self.now[0] += seconds

        client = bp.ExplorerClient(
            "tok", sleep=sleep, clock=lambda: self.now[0], opener=opener,
            **kwargs)
        return client, calls

    def test_sends_a_bearer_token(self) -> None:
        captured = {}

        def opener(request, timeout=None):
            captured.update(request.headers)
            return FakeResponse(MASTERS_PAYLOAD)

        client = bp.ExplorerClient(
            "secret-token", sleep=lambda _: None, clock=lambda: 0.0,
            opener=opener)
        client.get("https://explorer.lichess.ovh/masters?fen=x")
        # urllib title-cases header names.
        self.assertEqual(captured.get("Authorization"), "Bearer secret-token")

    def test_returns_the_decoded_payload(self) -> None:
        client, _ = self.make_client([MASTERS_PAYLOAD])
        self.assertEqual(client.get("https://x/masters"), MASTERS_PAYLOAD)
        self.assertEqual(client.requests, 1)

    def test_throttles_to_the_configured_rate(self) -> None:
        client, _ = self.make_client(
            [MASTERS_PAYLOAD, MASTERS_PAYLOAD], rate_per_minute=25)
        client.get("https://x/1")
        client.get("https://x/2")
        # 25/minute is one request every 2.4 seconds.
        self.assertEqual(self.slept, [2.4])

    def test_429_is_retried_after_the_servers_own_delay(self) -> None:
        error = self.http_error(429, "Too Many Requests", BackoffTests.Headers("3"))
        client, calls = self.make_client([error, MASTERS_PAYLOAD])
        self.assertEqual(client.get("https://x/masters"), MASTERS_PAYLOAD)
        self.assertIn(3.0, self.slept)
        self.assertEqual(len(calls), 2)

    def test_server_errors_are_retried(self) -> None:
        error = self.http_error(503, "nope")
        client, calls = self.make_client([error, MASTERS_PAYLOAD])
        self.assertEqual(client.get("https://x/masters"), MASTERS_PAYLOAD)
        self.assertEqual(len(calls), 2)

    def test_401_fails_fast_with_an_actionable_message(self) -> None:
        # The explorer has required a token since 2026-03-03. Retrying an
        # auth failure thousands of times would waste hours and say
        # nothing useful, so it must raise on the first response.
        error = self.http_error(401, "Unauthorized")
        client, calls = self.make_client([error, MASTERS_PAYLOAD])
        with self.assertRaises(bp.ExplorerAuthError) as caught:
            client.get("https://x/masters")
        self.assertEqual(len(calls), 1)
        self.assertIn("oauth/token", str(caught.exception).lower())

    def test_it_outlasts_an_outage_longer_than_the_old_attempt_budget(self) -> None:
        """The behaviour the run needed and did not have.

        Six attempts was about five minutes, which a sleeping laptop or
        a changed network outruns easily -- and a collection that dies at
        48% has spent hours for nothing. Time is the honest budget: the
        client keeps trying while the patience lasts, and a request that
        comes back after twenty failures still counts.
        """
        #: Ten failures spend about twenty-five minutes of backoff, well
        #: inside the hour, and comfortably past the old six-attempt bound.
        errors = [urllib.error.URLError("network is down") for _ in range(10)]
        client, calls = self.make_client([*errors, {"white": 1, "draws": 0, "black": 0}],
                                         patience=3600.0)
        result = client.get("https://x/masters")
        self.assertEqual(result["white"], 1)
        self.assertGreater(len(calls), bp.MAX_RETRIES,
                           "gave up within the old attempt bound")

    def test_gives_up_once_the_patience_is_spent(self) -> None:
        errors = [urllib.error.URLError("still down") for _ in range(200)]
        client, calls = self.make_client(errors, patience=120.0)
        with self.assertRaises(RuntimeError) as caught:
            client.get("https://x/masters")
        self.assertIn("resumes where this stopped", str(caught.exception))
        self.assertLess(len(calls), 200, "kept trying past the budget")


class BuildRowsTests(unittest.TestCase):
    """`build_rows` against a cache only — `client=None`, so no network."""

    POSITIONS = [
        {"ocn1": "A.One", "fen_key": "K1", "fen": "K1 w - - 0 1"},
        {"ocn1": "A.Two", "fen_key": "K2", "fen": "K2 b - - 0 2"},
        # Same position as A.One by a different move order: the explorer
        # indexes positions, so this must not cost a second request.
        {"ocn1": "A.Three", "fen_key": "K1", "fen": "K1 w - - 0 3"},
    ]

    def seed(self, tmp: Path) -> None:
        for key, masters in (("K1", MASTERS_PAYLOAD), ("K2", EMPTY_PAYLOAD)):
            bp.write_cache(bp.cache_file(tmp, "masters", key), key, masters)
            bp.write_cache(bp.cache_file(tmp, "lichess", key), key,
                           LICHESS_PAYLOAD if key == "K1" else EMPTY_PAYLOAD)

    def test_builds_every_row_in_catalogue_order(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            self.seed(Path(tmp))
            stats = bp.RunStats()
            rows = bp.build_rows(
                self.POSITIONS, Path(tmp), "2026-07-29", None, stats,
                progress_every=0)
        self.assertEqual([row[0] for row in rows], ["A.One", "A.Two", "A.Three"])
        self.assertEqual(stats.rows, 3)
        self.assertEqual(stats.missing, 0)

    def test_transpositions_share_one_lookup(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            self.seed(Path(tmp))
            stats = bp.RunStats()
            rows = bp.build_rows(
                self.POSITIONS, Path(tmp), "2026-07-29", None, stats,
                progress_every=0)
        # Three rows, two distinct positions, four cache reads (two
        # endpoints each) -- the third row is served from memory.
        self.assertEqual(stats.positions, 2)
        self.assertEqual(stats.cache_hits, 4)
        self.assertEqual(rows[0][1:6], rows[2][1:6])

    def test_rows_without_data_are_reported_not_invented(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            stats = bp.RunStats()
            rows = bp.build_rows(
                self.POSITIONS, Path(tmp), "2026-07-29", None, stats,
                progress_every=0)
        self.assertEqual(rows, [])
        self.assertEqual(stats.missing, 3)

    def test_output_is_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            self.seed(Path(tmp))
            stats_a, stats_b = bp.RunStats(), bp.RunStats()
            first = bp.build_rows(self.POSITIONS, Path(tmp), "2026-07-29",
                                  None, stats_a, progress_every=0)
            second = bp.build_rows(self.POSITIONS, Path(tmp), "2026-07-29",
                                   None, stats_b, progress_every=0)
        self.assertEqual(bp.render_tsv(first), bp.render_tsv(second))


@unittest.skipUnless(POPULARITY_TSV.exists(),
                     f"{POPULARITY_TSV.name} not built yet (needs a Lichess "
                     f"OAuth token; see tools/build_popularity.py)")
class CommittedSidecarTests(unittest.TestCase):
    """Shape checks on the committed snapshot, tolerant of a refresh.

    Deliberately not a drift test: the numbers move whenever Lichess
    indexes another game. Only the contract is pinned.
    """

    ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

    @classmethod
    def setUpClass(cls) -> None:
        text = POPULARITY_TSV.read_text(encoding="utf-8")
        cls.lines = text.splitlines()
        cls.rows = [line.split("\t") for line in cls.lines[1:]]

    def test_header_is_the_documented_one(self) -> None:
        self.assertEqual(self.lines[0], bp.HEADER)

    def test_every_row_has_every_column(self) -> None:
        bad = [row[0] for row in self.rows if len(row) != len(bp.FIELDS)]
        self.assertEqual(bad, [])

    def test_counts_are_integers_and_never_negative(self) -> None:
        for row in self.rows:
            with self.subTest(ocn1=row[0]):
                for index in (1, 2, 3, 4, 5):
                    self.assertRegex(row[index], r"^\d+$")

    def test_white_draws_black_sum_to_the_masters_total(self) -> None:
        for row in self.rows:
            with self.subTest(ocn1=row[0]):
                self.assertEqual(
                    int(row[1]), int(row[2]) + int(row[3]) + int(row[4]))

    def test_sampled_years_are_plausible_and_ordered(self) -> None:
        for row in self.rows:
            earliest, latest = row[8], row[9]
            if not earliest or not latest:
                continue
            with self.subTest(ocn1=row[0]):
                self.assertLessEqual(int(earliest), int(latest))
                self.assertGreater(int(earliest), 1400)

    def test_retrieved_is_one_iso_date_for_the_whole_snapshot(self) -> None:
        dates = {row[-1] for row in self.rows}
        self.assertEqual(len(dates), 1, f"mixed retrieval dates: {dates}")
        self.assertRegex(dates.pop(), self.ISO_DATE)

    def test_slugs_are_unique(self) -> None:
        slugs = [row[0] for row in self.rows]
        self.assertEqual(len(slugs), len(set(slugs)))

    @unittest.skipUnless(POSITIONS_TSV.exists(), "positions sidecar missing")
    def test_slugs_all_exist_in_the_catalogue(self) -> None:
        known = {row["ocn1"] for row in bp.load_positions(POSITIONS_TSV)}
        unknown = [row[0] for row in self.rows if row[0] not in known]
        self.assertEqual(unknown, [])


if __name__ == "__main__":
    unittest.main()
