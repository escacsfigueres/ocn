#!/usr/bin/env python3
"""Build the popularity sidecar `catalog/ocn-1.popularity.tsv` (roadmap H2.7).

OCN says what a line is *called* and where it sits in the tree. It has
never said how often anyone plays it. This sidecar is that column: for
every concrete catalogue row, how many games reached its position in the
two public Lichess opening-explorer pools.

## The only source, and how its numbers must be quoted

The single source is the **public Lichess opening explorer API**
(<https://explorer.lichess.ovh>). No proprietary database is consulted,
so every number here is checkable by anyone with a browser and a Lichess
account. That imposes a claim discipline the sidecar's consumers must
keep:

- `masters_games` is **games in the Lichess masters database** (~3M OTB
  master games), never "games ever played". `lichess_games` is **games
  in the Lichess games database** restricted to the speeds and rating
  bands this tool queries (see `LICHESS_SPEEDS` / `LICHESS_RATINGS`),
  never "games on Lichess" and never "games in the world".
- `top_game_year_earliest` / `top_game_year_latest` are the earliest and
  latest years **among the sampled top games** -- the handful of
  highest-rated games the API returns for the position
  (`TOP_GAMES`). They are *not* the first or last time the line was
  played. A line played in 1858 whose four highest-rated games are all
  post-2000 will read 2000-something here, and that is correct for what
  the column measures. Label it that way wherever it is displayed.
- `top_player` is the highest-rated player appearing in that same small
  sample, on either colour. It is "the strongest player in the sampled
  top games", not "the greatest exponent of this opening".
- `retrieved` dates the snapshot. The explorer is a living database;
  these numbers drift. The column is what makes a stale figure
  self-evident instead of silently wrong.

## Authentication (changed 3 March 2026)

The explorer API **used to be anonymous and no longer is**. Lichess
disallowed anonymous explorer requests after a sustained DDoS
(<https://lichess.org/@/thibault/blog/the-opening-explorer-now-requires-authentication/FSWh9Zg3>):
"If you use the explorer through the API, you now need to add an oauth
token to each explorer request." Unauthenticated requests get HTTP 401
from nginx before they reach the application.

So this tool needs a Lichess OAuth token. Any personal access token
works -- the explorer needs no particular scope, only a valid Lichess
identity. Mint one at <https://lichess.org/account/oauth/token> and pass
it out of band:

    export LICHESS_TOKEN=lip_xxxxxxxxxxxx
    python3 tools/build_popularity.py

The token is read from `--token` or the `LICHESS_TOKEN` environment
variable, is never written to the cache, the output or any log line, and
must never be committed.

## Rate limit and run time

The same post sets the budget: **25 requests per minute**, which is what
`--rate` defaults to. Two endpoints per distinct position over 5,765
distinct positions is ~11,530 requests, so a cold full run takes roughly
**eight hours**. That is not a mistake in the throttle -- it is the
published limit, and exceeding it risks the token rather than the data.

The run is therefore built to be interrupted. Every response is cached
on disk under `--cache-dir`, keyed by the position, so a re-run costs
nothing for everything already fetched and picks up where it stopped.
Interrupt freely; resume by running the same command again.

Usage:
    python3 tools/build_popularity.py [--positions PATH] [--out PATH]
        [--token TOKEN] [--cache-dir DIR] [--rate PER_MINUTE]
        [--limit N] [--offline]

`--offline` builds the sidecar from the cache alone and reports what is
still missing, which is how a partial run is inspected without spending
requests.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any, Iterable

REPO_ROOT = Path(__file__).resolve().parent.parent

#: The positions sidecar (roadmap H2.8) supplies both the query key
#: (`fen`) and the cache key (`fen_key`), in catalogue order.
DEFAULT_POSITIONS = REPO_ROOT / "src" / "ocn" / "data" / "ocn-1.positions.tsv"
DEFAULT_OUT = REPO_ROOT / "catalog" / "ocn-1.popularity.tsv"

#: Outside the repository on purpose: this is a multi-gigabyte-free but
#: many-thousand-file response cache whose only job is to make a resumed
#: or repeated run cost nothing. It is not an artefact, it is never
#: committed, and deleting it only costs time.
DEFAULT_CACHE_DIR = Path(tempfile.gettempdir()) / "ocn-lichess-explorer-cache"

EXPLORER_BASE = "https://explorer.lichess.ovh"

#: Number of top games requested per masters position. Only used to
#: derive `top_player` and the two sampled-year columns; the totals do
#: not depend on it.
TOP_GAMES = 4

#: The lichess-pool query is deliberately narrowed to real, rated,
#: non-bullet chess in the rating bands where opening choice is a choice.
#: Widening either list changes what `lichess_games` counts, so both are
#: part of the sidecar's documented meaning rather than a tuning knob.
LICHESS_SPEEDS = "blitz,rapid,classical"
LICHESS_RATINGS = "1800,2000,2200,2500"

#: Lichess publishes 25 requests/minute for the explorer (blog post of
#: 3 March 2026). Do not raise this without a reason from upstream.
DEFAULT_RATE_PER_MINUTE = 25

#: Progress cadence, in catalogue rows.
PROGRESS_EVERY = 200

HEADER = (
    "ocn1\tmasters_games\tmasters_white\tmasters_draws\tmasters_black\t"
    "lichess_games\ttop_player\ttop_player_elo\ttop_game_year_earliest\t"
    "top_game_year_latest\tretrieved"
)

FIELDS = HEADER.split("\t")

MAX_RETRIES = 6
BACKOFF_BASE_SECONDS = 5.0
BACKOFF_CAP_SECONDS = 300.0


class ExplorerAuthError(RuntimeError):
    """The explorer rejected the request for want of a valid token."""


# ---------------------------------------------------------------------
# Pure parsing: everything below this line is testable without a network.
# ---------------------------------------------------------------------


@dataclass(frozen=True)
class MastersSummary:
    """The masters-pool facts one position contributes to the sidecar."""

    games: int
    white: int
    draws: int
    black: int
    top_player: str
    top_player_elo: int | None
    year_earliest: int | None
    year_latest: int | None


def _int(value: Any) -> int:
    """A count from a JSON payload, treating absent/null as zero."""
    return int(value) if isinstance(value, (int, float)) else 0


def top_player_of(top_games: Iterable[dict]) -> tuple[str, int | None]:
    """The highest-rated player in a top-games sample, either colour.

    The API returns each game with a `white` and a `black` player, both
    carrying `name` and `rating`; the strongest player in the sample may
    sit on either side, so both are considered. Ties break on the name,
    ascending, purely so that two runs over the same payload agree.

    Returns `("", None)` for an empty or ratingless sample.
    """
    best_name = ""
    best_rating: int | None = None
    for game in top_games or []:
        if not isinstance(game, dict):
            continue
        for colour in ("white", "black"):
            player = game.get(colour)
            if not isinstance(player, dict):
                continue
            rating = player.get("rating")
            name = str(player.get("name") or "").strip()
            if not name or not isinstance(rating, (int, float)):
                continue
            rating = int(rating)
            if best_rating is None or rating > best_rating or (
                rating == best_rating and name < best_name
            ):
                best_name, best_rating = name, rating
    return best_name, best_rating


def sampled_year_range(top_games: Iterable[dict]) -> tuple[int | None, int | None]:
    """Earliest and latest year **among the sampled top games**.

    Emphatically not "when the line was first played": the sample is the
    few highest-rated games the API returns, so both ends are bounded by
    that sample. See the module docstring.
    """
    years = [
        int(game["year"])
        for game in top_games or []
        if isinstance(game, dict) and isinstance(game.get("year"), (int, float))
    ]
    if not years:
        return None, None
    return min(years), max(years)


def summarise_masters(payload: dict) -> MastersSummary:
    """Fold one `/masters` response into the row's masters columns."""
    white = _int(payload.get("white"))
    draws = _int(payload.get("draws"))
    black = _int(payload.get("black"))
    top_games = payload.get("topGames") or []
    name, rating = top_player_of(top_games)
    earliest, latest = sampled_year_range(top_games)
    return MastersSummary(
        games=white + draws + black,
        white=white,
        draws=draws,
        black=black,
        top_player=name,
        top_player_elo=rating,
        year_earliest=earliest,
        year_latest=latest,
    )


def total_games(payload: dict) -> int:
    """Games in a pool response: the explorer reports W/D/B, not a total."""
    return (
        _int(payload.get("white"))
        + _int(payload.get("draws"))
        + _int(payload.get("black"))
    )


def _cell(value: Any) -> str:
    """A TSV cell. `None` is the empty cell; zero is a measured zero."""
    return "" if value is None else str(value)


def popularity_row(
    ocn1: str,
    masters_payload: dict,
    lichess_payload: dict,
    retrieved: str,
) -> list[str]:
    """One output row, as the eleven strings the TSV will carry.

    The four count columns are always numbers, because a zero here is a
    measurement ("no game in this database reached this position") and
    not a gap. The three sample-derived columns -- `top_player`,
    `top_player_elo` and the two years -- are empty when the position has
    no games to sample, since there is nothing they could honestly say.
    """
    masters = summarise_masters(masters_payload)
    return [
        ocn1,
        str(masters.games),
        str(masters.white),
        str(masters.draws),
        str(masters.black),
        str(total_games(lichess_payload)),
        _cell(masters.top_player or None),
        _cell(masters.top_player_elo),
        _cell(masters.year_earliest),
        _cell(masters.year_latest),
        retrieved,
    ]


def render_tsv(rows: Iterable[Iterable[str]]) -> str:
    """The sidecar text: header, then one line per row, in the given order."""
    lines = [HEADER]
    lines += ["\t".join(str(cell) for cell in row) for row in rows]
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------
# Cache
# ---------------------------------------------------------------------


def cache_key(fen_key: str) -> str:
    """A filesystem-safe key for a position.

    `fen_key` contains slashes and spaces, so it cannot be a filename. It
    is hashed, and the original is stored inside the cached document so a
    collision or a stale file is detectable rather than silent.
    """
    return hashlib.sha256(fen_key.encode("utf-8")).hexdigest()[:32]


def cache_file(cache_dir: Path, endpoint: str, fen_key: str) -> Path:
    key = cache_key(fen_key)
    # Sharded on the first two hex characters: 5,765 positions in one
    # flat directory is workable but unpleasant to inspect.
    return cache_dir / endpoint / key[:2] / f"{key}.json"


def read_cache(path: Path, fen_key: str) -> dict | None:
    """The cached payload for a position, or None if absent/unusable."""
    if not path.is_file():
        return None
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(document, dict) or document.get("fen_key") != fen_key:
        return None
    payload = document.get("payload")
    return payload if isinstance(payload, dict) else None


def write_cache(path: Path, fen_key: str, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    document = {"fen_key": fen_key, "payload": payload}
    # Written via a sibling temp file: an eight-hour run will be
    # interrupted, and a half-written JSON file would poison the resume.
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(document, ensure_ascii=False), encoding="utf-8")
    tmp.replace(path)


# ---------------------------------------------------------------------
# Network
# ---------------------------------------------------------------------


def masters_url(fen: str) -> str:
    query = urllib.parse.urlencode({"fen": fen, "topGames": TOP_GAMES})
    return f"{EXPLORER_BASE}/masters?{query}"


def lichess_url(fen: str) -> str:
    query = urllib.parse.urlencode({
        "fen": fen,
        "speeds": LICHESS_SPEEDS,
        "ratings": LICHESS_RATINGS,
        "topGames": 0,
        "recentGames": 0,
    })
    return f"{EXPLORER_BASE}/lichess?{query}"


ENDPOINT_URLS = {"masters": masters_url, "lichess": lichess_url}


def retry_after_seconds(headers: Any, attempt: int) -> float:
    """How long to wait after a throttled response.

    Honours `Retry-After` when the server sends one; otherwise backs off
    exponentially from `BACKOFF_BASE_SECONDS`, capped.
    """
    raw = None
    if headers is not None:
        try:
            raw = headers.get("Retry-After")
        except AttributeError:  # pragma: no cover - non-mapping headers
            raw = None
    if raw:
        try:
            return min(float(str(raw).strip()), BACKOFF_CAP_SECONDS)
        except ValueError:
            pass
    return min(BACKOFF_BASE_SECONDS * (2 ** attempt), BACKOFF_CAP_SECONDS)


class ExplorerClient:
    """A polite, resumable client for the public explorer endpoints."""

    def __init__(
        self,
        token: str,
        rate_per_minute: int = DEFAULT_RATE_PER_MINUTE,
        timeout: float = 60.0,
        sleep=time.sleep,
        clock=time.monotonic,
        opener=urllib.request.urlopen,
    ) -> None:
        self.token = token
        self.min_interval = 60.0 / max(rate_per_minute, 1)
        self.timeout = timeout
        self._sleep = sleep
        self._clock = clock
        self._opener = opener
        self._last_request: float | None = None
        self.requests = 0

    def _throttle(self) -> None:
        if self._last_request is not None:
            wait = self.min_interval - (self._clock() - self._last_request)
            if wait > 0:
                self._sleep(wait)
        self._last_request = self._clock()

    def get(self, url: str) -> dict:
        """One GET, throttled, retried on 429/5xx, decoded as JSON."""
        request = urllib.request.Request(url, headers={
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json",
            "User-Agent": "ocn-build-popularity/1.0 (+https://github.com/escacsfigueres/ocn)",
        })
        last_error: Exception | None = None
        for attempt in range(MAX_RETRIES):
            self._throttle()
            try:
                with self._opener(request, timeout=self.timeout) as response:
                    self.requests += 1
                    return json.loads(response.read().decode("utf-8"))
            except urllib.error.HTTPError as exc:
                if exc.code in (401, 403):
                    # Retrying an auth failure 5,765 times helps nobody.
                    raise ExplorerAuthError(
                        f"HTTP {exc.code} from the explorer: the Lichess "
                        "opening explorer has required an OAuth token since "
                        "2026-03-03. Mint one at "
                        "https://lichess.org/account/oauth/token and pass it "
                        "via --token or LICHESS_TOKEN."
                    ) from exc
                if exc.code == 429 or exc.code >= 500:
                    last_error = exc
                    delay = retry_after_seconds(getattr(exc, "headers", None), attempt)
                    print(
                        f"  HTTP {exc.code}, backing off {delay:.0f}s "
                        f"(attempt {attempt + 1}/{MAX_RETRIES})",
                        file=sys.stderr, flush=True,
                    )
                    self._sleep(delay)
                    continue
                raise
            except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
                last_error = exc
                delay = retry_after_seconds(None, attempt)
                print(
                    f"  {type(exc).__name__}, retrying in {delay:.0f}s "
                    f"(attempt {attempt + 1}/{MAX_RETRIES})",
                    file=sys.stderr, flush=True,
                )
                self._sleep(delay)
        raise RuntimeError(f"giving up after {MAX_RETRIES} attempts: {last_error}")


# ---------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------


def load_positions(path: Path) -> list[dict[str, str]]:
    """Concrete rows from the positions sidecar, in catalogue order."""
    with path.open(newline="", encoding="utf-8") as f:
        return [row for row in csv.DictReader(f, delimiter="\t") if row.get("fen")]


@dataclass
class RunStats:
    rows: int = 0
    positions: int = 0
    cache_hits: int = 0
    fetched: int = 0
    missing: int = 0

    def summary(self, elapsed: float) -> str:
        return (
            f"rows {self.rows}, distinct positions {self.positions}, "
            f"cache hits {self.cache_hits}, fetched {self.fetched}, "
            f"missing {self.missing}, elapsed {elapsed / 60:.1f} min"
        )


def build_rows(
    positions: list[dict[str, str]],
    cache_dir: Path,
    retrieved: str,
    client: ExplorerClient | None,
    stats: RunStats,
    progress_every: int = PROGRESS_EVERY,
    started: float | None = None,
) -> list[list[str]]:
    """Every row's popularity line, in the order the positions arrive.

    Requests are deduplicated by `fen_key`: the explorer indexes
    positions, not move orders, so the 5,894 catalogue rows collapse to
    5,765 distinct positions and the transpositions come for free.
    """
    started = time.monotonic() if started is None else started
    payloads: dict[tuple[str, str], dict] = {}
    rows: list[list[str]] = []
    seen: set[str] = set()

    for index, position in enumerate(positions, start=1):
        fen_key = position["fen_key"]
        fen = position["fen"]
        if fen_key not in seen:
            seen.add(fen_key)
            stats.positions += 1
        row_payloads: dict[str, dict] = {}
        for endpoint in ("masters", "lichess"):
            key = (endpoint, fen_key)
            if key in payloads:
                payload = payloads[key]
            else:
                path = cache_file(cache_dir, endpoint, fen_key)
                payload = read_cache(path, fen_key)
                if payload is not None:
                    stats.cache_hits += 1
                elif client is not None:
                    payload = client.get(ENDPOINT_URLS[endpoint](fen))
                    write_cache(path, fen_key, payload)
                    stats.fetched += 1
                if payload is not None:
                    payloads[key] = payload
            if payload is None:
                break
            row_payloads[endpoint] = payload

        if len(row_payloads) != 2:
            stats.missing += 1
            continue

        rows.append(popularity_row(
            position["ocn1"], row_payloads["masters"], row_payloads["lichess"],
            retrieved,
        ))
        stats.rows += 1

        if progress_every and index % progress_every == 0:
            elapsed = time.monotonic() - started
            done = index / len(positions)
            eta = (elapsed / done - elapsed) / 60 if done else 0.0
            print(
                f"  {index}/{len(positions)} rows ({done:.0%}), "
                f"{stats.cache_hits} cached, {stats.fetched} fetched, "
                f"{elapsed / 60:.1f} min elapsed, ~{eta:.0f} min left",
                file=sys.stderr, flush=True,
            )
    return rows


def resolve_token(explicit: str | None) -> str | None:
    return explicit or os.environ.get("LICHESS_TOKEN") or None


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build the OCN-1 popularity sidecar from the public "
                    "Lichess opening explorer API.",
    )
    parser.add_argument("--positions", type=Path, default=DEFAULT_POSITIONS,
                        help="Positions sidecar to read (default: the "
                             "bundled ocn-1.positions.tsv).")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--token", default=None,
                        help="Lichess OAuth token. Defaults to $LICHESS_TOKEN. "
                             "Required since 2026-03-03 unless --offline.")
    parser.add_argument("--cache-dir", type=Path, default=DEFAULT_CACHE_DIR,
                        help=f"Directory for the resumable response cache "
                             f"(default: {DEFAULT_CACHE_DIR}).")
    parser.add_argument("--rate", type=int, default=DEFAULT_RATE_PER_MINUTE,
                        help=f"Requests per minute (default "
                             f"{DEFAULT_RATE_PER_MINUTE}, the published limit).")
    parser.add_argument("--limit", type=int, default=None,
                        help="Only process the first N catalogue rows.")
    parser.add_argument("--retrieved", default=None,
                        help="Value for the retrieved column (default: today).")
    parser.add_argument("--offline", action="store_true",
                        help="Build from the cache alone; make no request.")
    parser.add_argument("--progress-every", type=int, default=PROGRESS_EVERY)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(sys.argv[1:] if argv is None else argv)

    if not args.positions.exists():
        print(f"ERROR: positions sidecar not found: {args.positions}",
              file=sys.stderr)
        return 1

    token = resolve_token(args.token)
    if not token and not args.offline:
        print(
            "ERROR: no Lichess OAuth token.\n"
            "The opening explorer API stopped accepting anonymous requests on "
            "2026-03-03 (HTTP 401):\n"
            "  https://lichess.org/@/thibault/blog/"
            "the-opening-explorer-now-requires-authentication/FSWh9Zg3\n"
            "Mint a personal access token at "
            "https://lichess.org/account/oauth/token, then:\n"
            "  export LICHESS_TOKEN=lip_...\n"
            "Or pass --offline to build from a cache already on disk.",
            file=sys.stderr,
        )
        return 2

    positions = load_positions(args.positions)
    if args.limit is not None:
        positions = positions[: args.limit]
    retrieved = args.retrieved or date.today().isoformat()

    client = None if args.offline else ExplorerClient(token or "", args.rate)
    stats = RunStats()
    started = time.monotonic()
    print(
        f"{len(positions)} catalogue rows, source {EXPLORER_BASE}, "
        f"{'offline (cache only)' if args.offline else f'{args.rate} req/min'}, "
        f"cache {args.cache_dir}",
        file=sys.stderr, flush=True,
    )

    try:
        rows = build_rows(
            positions, args.cache_dir, retrieved, client, stats,
            args.progress_every, started,
        )
    except ExplorerAuthError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("\ninterrupted: the cache is intact, re-run to resume",
              file=sys.stderr)
        return 130

    elapsed = time.monotonic() - started
    if stats.missing and not rows:
        print("ERROR: nothing cached and nothing fetched; no sidecar written",
              file=sys.stderr)
        print(stats.summary(elapsed), file=sys.stderr)
        return 1

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(render_tsv(rows), encoding="utf-8")
    print(f"wrote {args.out} ({len(rows)} rows, retrieved {retrieved})")
    print(stats.summary(elapsed), file=sys.stderr)
    if stats.missing:
        print(
            f"WARNING: {stats.missing} rows omitted for want of data; "
            "re-run to complete them",
            file=sys.stderr,
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
