#!/usr/bin/env python3
"""When each opening was taken up, and by whom, from a public game corpus.

`docs/practitioner-chronology-design.md` argues that the interesting
fact about a player and an opening is usually chronological. Vaisser was
first to play the Sveshnikov at a high level; Kramnik, Dubov and Carlsen
made it theirs afterwards. The London runs Kamsky, then Kramnik, then
Carlsen. Without the ordering Vaisser does not register at all -- he was
never a top-ten player, and his claim rests entirely on being early.

The Lichess masters explorer cannot answer this on its own. Its top
games are sorted by rating, so early adopters are invisible behind
whoever is strongest, and its `top_player` column turns out to be the
rating list wearing a disguise.

A corpus can. This walks LumbrasGigaBase -- freely downloadable, and the
tier the design already sanctions -- annotating every game to a
catalogue slug and recording who played it and when. From that, for any
opening: the first year it appears, the players in that first window,
and how the line spreads afterwards.

What comes out is an observation, not a verdict. "Earliest in this
corpus" is not "first ever", and the note says so on every row. A game
is cited the way historians cite one, by players, event and year, so a
reader can check it without holding the corpus.

The run is long -- roughly nine hours over nine gigabytes -- so it
writes incrementally and can be resumed: a shard already recorded in the
output is skipped.

Usage:
    python3 tools/build_adoption_chronology.py --pgn-dir DIR --out games.tsv
    python3 tools/build_adoption_chronology.py --pgn-dir DIR --out g.tsv --resume
"""
from __future__ import annotations

import argparse
import csv
import sys
import time
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
#: `src` only. `tools/ocn.py` is the consumer reader and shadows the
#: `ocn` package if tools/ is on the path, which fails obscurely.
sys.path.insert(0, str(REPO_ROOT / "src"))

COLUMNS = ("ocn1", "year", "white", "white_elo", "black", "black_elo",
           "result", "event", "shard", "corpus")

#: Ratings are the difference between "somebody played this" and "a
#: strong player played this", which is the whole question when asking
#: who took a line up. The first pass over Lumbras omitted them and had
#: to be redone; they are not optional.
ELO_HEADERS = ("WhiteElo", "BlackElo")

#: Below this the game is a fragment or a scoresheet stub, not evidence
#: that anyone played the opening deliberately.
MIN_PLIES = 12


def year_of(date: str | None) -> str:
    head = (date or "")[:4]
    return head if head.isdigit() else ""


def shards(directory: Path) -> list[Path]:
    return sorted(p for p in directory.glob("*.pgn") if p.is_file())


def already_done(out: Path) -> set[str]:
    """Shards whose rows are already in the output."""
    if not out.is_file():
        return set()
    done: set[str] = set()
    with out.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            done.add(row["shard"])
    return done


def main(argv: list[str] | None = None) -> int:
    from ocn.annotate import Annotator, iter_games
    from ocn.catalog import Catalog

    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--pgn-dir", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--limit-per-shard", type=int, default=0,
                        help="stop after this many games per shard (for a trial)")
    parser.add_argument("--progress-every", type=int, default=50000)
    parser.add_argument("--corpus", default="",
                        help="name recorded on every row, so passes over "
                             "different bases stay distinguishable when merged")
    parser.add_argument("--min-elo", type=int, default=0,
                        help="keep a game only if either player is at least this")
    args = parser.parse_args(sys.argv[1:] if argv is None else argv)

    if not args.pgn_dir.is_dir():
        print(f"ERROR: no such directory: {args.pgn_dir}", file=sys.stderr)
        return 1

    files = shards(args.pgn_dir)
    if not files:
        print(f"ERROR: no .pgn files in {args.pgn_dir}", file=sys.stderr)
        return 1

    done = already_done(args.out) if args.resume else set()
    if done:
        print(f"resuming: {len(done)} shard(s) already recorded", file=sys.stderr)

    annotator = Annotator(Catalog.load())
    fresh = not args.out.is_file() or not args.resume
    handle = args.out.open("w" if fresh else "a", encoding="utf-8", newline="")
    if fresh:
        handle.write("\t".join(COLUMNS) + "\n")

    totals: Counter = Counter()
    began = time.monotonic()
    try:
        for shard in files:
            if shard.name in done:
                print(f"skip {shard.name} (already recorded)", file=sys.stderr)
                continue
            seen = kept = 0
            started = time.monotonic()
            print(f"reading {shard.name} ({shard.stat().st_size / 1e6:.0f} MB)",
                  file=sys.stderr, flush=True)
            with shard.open(encoding="utf-8", errors="replace") as source:
                for game in iter_games(source):
                    seen += 1
                    if args.limit_per_shard and seen > args.limit_per_shard:
                        break
                    if args.progress_every and seen % args.progress_every == 0:
                        rate = seen / max(time.monotonic() - started, 1)
                        print(f"  {seen:,} read, {kept:,} kept, {rate:.0f}/s",
                              file=sys.stderr, flush=True)
                    year = year_of(game.header("Date"))
                    if not year:
                        continue
                    try:
                        match = annotator.match_game(game)
                    except Exception:
                        continue
                    slug = getattr(match, "slug", None)
                    if not slug or getattr(match, "plies", 0) < MIN_PLIES:
                        continue
                    def elo(header: str) -> str:
                        raw = (game.header(header) or "").strip()
                        return raw if raw.isdigit() else ""
                    white_elo, black_elo = elo("WhiteElo"), elo("BlackElo")
                    if args.min_elo:
                        best = max((int(e) for e in (white_elo, black_elo) if e),
                                   default=0)
                        if best < args.min_elo:
                            continue
                    handle.write("\t".join([
                        slug, year,
                        (game.header("White") or "?").replace("\t", " "),
                        white_elo,
                        (game.header("Black") or "?").replace("\t", " "),
                        black_elo,
                        (game.header("Result") or "").replace("\t", " "),
                        (game.header("Event") or "").replace("\t", " ")[:80],
                        shard.name, args.corpus,
                    ]) + "\n")
                    kept += 1
            handle.flush()
            totals[shard.name] = kept
            print(f"  done {shard.name}: {seen:,} read, {kept:,} kept, "
                  f"{time.monotonic() - started:.0f}s", file=sys.stderr, flush=True)
    finally:
        handle.close()

    print(f"\nkept {sum(totals.values()):,} game rows in "
          f"{(time.monotonic() - began) / 60:.0f} min")
    print(f"wrote {args.out}")
    print("a game row is an observation of play, not a claim about naming")
    return 0


if __name__ == "__main__":
    sys.exit(main())
