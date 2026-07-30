#!/usr/bin/env python3
"""The strongest master games played in each opening, with a link to each.

Albert asked whether chessgames.com could give OCN the best games per
variation. It could, but it is not needed and its terms make bulk use
awkward: the games are already on this machine.

`tools/build_popularity.py` asked the Lichess masters explorer for four
top games per position and kept only a summary of them -- the highest
rated player, and the span of years. The full responses stayed in its
cache, and each game in them carries a Lichess id, which is a permanent
public URL anyone can open. So roughly 19,000 games can be recovered
with no new API call at all.

What the relation is, precisely
------------------------------
These are the **highest-rated** master games in a position, which is not
the same as the historically important ones. The design reserves
`key-game` for "the game that fixed the name", and calling these that
would be a claim the data cannot support -- the top game in a line is
often a strong modern one that had nothing to do with its naming.

So this emits an enrichment sidecar rather than claims: for each
opening, its strongest recorded games with players, year and link. That
is directly useful to a reader ("show me this line played well"), it is
honest about what it is, and the rows that *do* turn out to be naming
games can be promoted into `key-game` by review afterwards.

The cache is the source, so this is offline and repeatable. A position
absent from the cache is reported, never fetched silently.

Usage:
    python3 tools/build_notable_games.py --dry-run
    python3 tools/build_notable_games.py --out catalog/ocn-1.games.tsv
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools"))

DEFAULT_CACHE = Path.home() / ".cache" / "ocn-lichess-explorer" / "masters"
DEFAULT_CATALOGUE = REPO_ROOT / "catalog" / "ocn-1.csv"

COLUMNS = ("ocn1", "white", "white_elo", "black", "black_elo", "year",
           "result", "lichess_id", "url")

GAME_URL = "https://lichess.org/{id}"

#: The explorer reports the winner as a colour, or null for a draw.
RESULT = {"white": "1-0", "black": "0-1", None: "1/2-1/2"}


def cached_payloads(cache: Path) -> dict[str, dict]:
    """Every cached masters response, keyed by the position it answers."""
    found: dict[str, dict] = {}
    for path in cache.rglob("*.json"):
        try:
            document = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        key = document.get("fen_key")
        payload = document.get("payload", document)
        if key and isinstance(payload, dict):
            found[key] = payload
    return found


def games_for(payload: dict) -> list[dict]:
    out = []
    for game in payload.get("topGames") or []:
        identifier = game.get("id")
        if not identifier:
            continue
        white, black = game.get("white") or {}, game.get("black") or {}
        out.append({
            "white": white.get("name", ""), "white_elo": white.get("rating", ""),
            "black": black.get("name", ""), "black_elo": black.get("rating", ""),
            "year": game.get("year", ""),
            "result": RESULT.get(game.get("winner"), ""),
            "lichess_id": identifier, "url": GAME_URL.format(id=identifier),
        })
    return out


def main(argv: list[str] | None = None) -> int:
    from chess_uci import fen_key_after_uci

    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--cache", type=Path, default=DEFAULT_CACHE)
    parser.add_argument("--catalogue", type=Path, default=DEFAULT_CATALOGUE)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(sys.argv[1:] if argv is None else argv)

    if not args.cache.is_dir():
        print(f"ERROR: no cache at {args.cache}. Run tools/build_popularity.py "
              f"first, or point --cache at its cache directory.", file=sys.stderr)
        return 1

    payloads = cached_payloads(args.cache)
    print(f"cached positions   {len(payloads):6d}")

    with args.catalogue.open(newline="", encoding="utf-8") as handle:
        catalogue = [r for r in csv.DictReader(handle) if r["moves_uci"].strip()]

    rows: list[dict] = []
    missing = 0
    for row in catalogue:
        payload = payloads.get(fen_key_after_uci(row["moves_uci"].strip()))
        if payload is None:
            missing += 1
            continue
        for game in games_for(payload):
            rows.append({"ocn1": row["ocn1"], **game})

    #: A transposition means two slugs share a position and therefore
    #: share its games; that is correct, and worth reporting so nobody
    #: reads the row count as a game count.
    distinct = len({r["lichess_id"] for r in rows})
    print(f"catalogue rows     {len(catalogue):6d}  (no cached position: {missing})")
    print(f"game rows          {len(rows):6d}")
    print(f"distinct games     {distinct:6d}  (the rest are transpositions "
          f"sharing a position)")

    years = [int(r["year"]) for r in rows if str(r["year"]).isdigit()]
    if years:
        print(f"years              {min(years)}-{max(years)}")
    top = Counter(r["white"] for r in rows if r["white"]).most_common(5)
    print("most frequent as White:", ", ".join(f"{n} ({c})" for n, c in top))

    if args.out and not args.dry_run:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        with args.out.open("w", encoding="utf-8", newline="") as handle:
            handle.write("\t".join(COLUMNS) + "\n")
            for row in rows:
                handle.write("\t".join(str(row.get(c, "")) for c in COLUMNS) + "\n")
        print(f"\nwrote {args.out}")
    else:
        print("\ndry run: nothing written")

    print("derived from cache; no request was made to any service")
    return 0


if __name__ == "__main__":
    sys.exit(main())
