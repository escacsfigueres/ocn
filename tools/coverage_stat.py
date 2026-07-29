#!/usr/bin/env python3
"""How much of a real PGN corpus does OCN name? (roadmap H2.1)

The reproducible script behind the headline claim. It runs the same
matcher `ocn annotate` runs — deepest position match per game,
transposition-aware, `transposes_to` resolved — over a PGN file and
prints the numbers, without rewriting a byte of the input:

    tools/fetch_lichess.sh                       # or any PGN dump
    python3 tools/coverage_stat.py games.pgn
    python3 tools/coverage_stat.py games.pgn --limit 100000 --json

Reading from stdin lets a compressed corpus stream through without ever
being written to disk:

    zstdcat lichess_db_standard_rated_2025-01.pgn.zst \\
        | python3 tools/coverage_stat.py - --limit 1000000 --progress 50000

No network access and no third-party dependency: the catalogue comes
from `src/ocn` in this checkout, so the number a run prints is the
number this catalogue produces, not the number some published build did.

Read the depth table before quoting the match rate. Every legal first
move is a catalogue row, so any game with one move played is "matched"
and the rate is ~100% by construction — true, and nearly empty. What
the catalogue is actually worth is how deep it keeps naming: the share
of games still named at 8, 12, 16 plies is the honest headline.

Exit codes: 0 on a corpus with at least one game, 2 on an unreadable or
empty input.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
# Unconditionally first: a script's own directory leads sys.path, and this
# one sits next to `tools/ocn.py`, which would otherwise shadow the `ocn`
# package with a same-named module.
sys.path.insert(0, str(REPO_ROOT / "src"))

from ocn.annotate import (  # noqa: E402 - path shim above must run first
    DEFAULT_MAX_PLIES,
    Annotator,
    Stats,
    iter_matches,
)
from ocn.catalog import Catalog  # noqa: E402


DEPTH_MARKS = (2, 4, 8, 12, 16, 20)


def depth_shares(stats: Stats) -> list[tuple[int, int, float]]:
    """How many games are still named at each depth mark."""
    shares = []
    for mark in DEPTH_MARKS:
        deep = sum(1 for depth in stats.depths if depth >= mark)
        shares.append((mark, deep, 100.0 * deep / stats.games if stats.games else 0.0))
    return shares


def fail(message: str, *, code: int = 2) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(code)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="coverage_stat.py",
        description=(
            "Report what share of the games in a PGN corpus OCN-1 classifies, "
            "how deep the match runs, and which openings dominate."
        ),
    )
    parser.add_argument("pgn", help="PGN file to read, or - for stdin")
    parser.add_argument(
        "--catalog",
        metavar="PATH",
        default=None,
        help="catalogue CSV to match against (default: the bundled one)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        metavar="N",
        help="stop after N games (default: read the whole corpus)",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=10,
        metavar="N",
        help="how many openings to list (default: 10)",
    )
    parser.add_argument(
        "--max-plies",
        type=int,
        default=DEFAULT_MAX_PLIES,
        metavar="N",
        help=f"replay at most N plies per game (default: {DEFAULT_MAX_PLIES})",
    )
    parser.add_argument(
        "--progress",
        type=int,
        default=0,
        metavar="N",
        help="print a progress line to stderr every N games (0: never)",
    )
    parser.add_argument("--json", action="store_true", help="emit JSON instead of text")
    return parser


def collect(source, annotator: Annotator, *, limit: int | None, progress: int) -> Stats:
    stats = Stats()
    started = time.perf_counter()
    for _game, match in iter_matches(source, annotator):
        stats.add(match)
        if progress and stats.games % progress == 0:
            elapsed = time.perf_counter() - started
            print(
                f"  {stats.games:,} games, {stats.match_rate:.1f}% matched, "
                f"{stats.games / elapsed:,.0f} games/s",
                file=sys.stderr,
            )
        if limit and stats.games >= limit:
            break
    return stats


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    catalog = Catalog.load(args.catalog)
    annotator = Annotator(catalog, max_plies=args.max_plies)

    if args.pgn == "-":
        source, close = sys.stdin, False
    else:
        path = Path(args.pgn)
        if not path.exists():
            fail(f"PGN not found: {path}")
        source, close = path.open(encoding="utf-8", errors="replace"), True

    started = time.perf_counter()
    try:
        stats = collect(source, annotator, limit=args.limit, progress=args.progress)
    finally:
        if close:
            source.close()
    elapsed = time.perf_counter() - started

    if not stats.games:
        fail(f"no PGN games found in {args.pgn!r}")

    shares = depth_shares(stats)
    if args.json:
        payload = stats.as_dict(args.top)
        payload["depth_shares"] = [
            {"plies": mark, "games": deep, "share": round(share, 2)}
            for mark, deep, share in shares
        ]
        payload["seconds"] = round(elapsed, 3)
        payload["games_per_second"] = round(stats.games / elapsed, 1) if elapsed else None
        payload["catalogue"] = catalog.version()
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(
            f"OCN-1 ({catalog.version()}, {len(catalog):,} rows) classifies "
            f"{stats.match_rate:.1f}% of {stats.games:,} games"
        )
        print()
        print(stats.format_text(args.top))
        print()
        print("still named at")
        width = max(len(f"{deep:,}") for _, deep, _ in shares)
        for mark, deep, share in shares:
            print(f"  {mark:>2} plies  {deep:>{width},}  ({share:.1f}%)")
        print()
        print(f"read in {elapsed:.1f}s ({stats.games / elapsed:,.0f} games/s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
