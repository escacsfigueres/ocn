#!/usr/bin/env python3
"""Map world championship games to OCN slugs, machine-derived.

The first step of the chronicle layer (`docs/chronicle-layer-design.md`):
which openings decided world championships. It is derived rather than
curated, so it carries no editorial risk -- the tool replays each game
against the catalogue with the same matcher `ocn annotate` uses, and
every claim it emits names a game by its identifying facts (players,
event, year), which is how a game is cited.

Both championship lines are first class. The women's world championship
has run since 1927 and is reported separately rather than folded into a
total, because a gap you cannot see is a gap nobody fixes.

Events are identified by structure, not by name. Filtering on the words
"world championship" is an arms race nobody wins: the first draft let in
33,000 games from junior, age-group, blind and deaf championships, and
the second still carried the physically-disabled association, two email
chess federations and a university championship. Every organisation that
runs a world championship of something says so in the event name.

What a title match *is*, on the other hand, is structural and stable:
two players, one event, between four and sixty games. Knockout editions
have a hundred and twenty-eight players; team events have dozens; postal
finals have fifteen. So the name filter only narrows the field, and the
shape of the event decides. Both are reported: --events lists what was
kept and why, --rejected what the name filter dropped.

Sources: any PGN whose games are public record. The default corpus is
LumbrasGigaBase, which is freely downloadable, so a reader can check any
claim without a subscription. Commercial compilations may be searched
for leads but are never cited -- see the source doctrine in the design
document.

Usage:
    python3 tools/build_wch_map.py PGN [PGN ...] --out catalog/ocn-1.wch.tsv
    python3 tools/build_wch_map.py PGN --rejected      # audit the filter
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from ocn import Catalog  # noqa: E402
from ocn.annotate import Annotator, iter_games  # noqa: E402

#: An event is a world championship if it matches one of these and none
#: of the exclusions below. Case-insensitive.
WCH_INCLUDE = re.compile(
    r"""(?ix)
    \b(
        world \s* ch(ampionship)?      # World Championship, World Ch
      | wch                            # Wch, the short form public bases use
      | world \s* title
    )\b
    """
)

#: What wears the name without being the thing. Every entry is here
#: because a real corpus put it in front of the include pattern -- the
#: first draft of this list let in 33,000 games from junior, age-group,
#: blind and deaf championships, so the list is written from the audit
#: rather than from imagination. Run with --events to check it again.
WCH_EXCLUDE = re.compile(
    r"""(?ix)
    (
        \b(wcht | team | teams)\b            # team world championships
      | \bu\d+\w*                            # U12m, U14w, U20 ...
      | \b(jr|jun|junior|juniors|youth|cadet|girls?|boys?|school\w*)\b
      | \b(senior|seniors|veterans?)\b
      | \b(amateur|student|students)\b
      | \b(blind|blindfold|silent|deaf|disab\w*|ibca|icsc|ipca)\b
      | \b(univ|university|academic)\b
      | \b(iecg|lss|ficgs|iccf)\b          # server and email federations
      | \b(cc|corr|corres\w*|correspondence|iccf)\b   # postal play: different evidence
      | \b(stud|stud\w*|tt)\b                  # student and team tournaments
      | \b(blitz|rapid|active|bullet)\b
      | \b(computer|engine|program)\b
      | \b(960|fischer\s*random|chess960)\b
      | \b(problem|composition|solving)\b
      | \b(cup|olympiad|zonal|interzonal)\b
      | \bcandidates?\b                       # its own event kind
      | \b(qualifier|prelim\w*|simul)\b
    )
    """
)

#: The knockout era (1998-2004, plus the women's knockouts) produced a
#: thousand games per edition against a title match's thirty, so it is
#: reported as its own format rather than averaged into the same figure.
#: It was a world championship; it was not a title match.
#: A title match runs from a handful of games to the 48 of Karpov
#: against Kasparov in 1984. Anything outside that is a tournament, a
#: knockout or a federation's own championship of something.
MATCH_MIN = 4
MATCH_MAX = 60

KNOCKOUT = re.compile(r"(?ix)\b(k\.?o\.?|knock\s*-?\s*out)\b")

#: The women's championship, which is a world championship and is
#: reported as its own line rather than folded into a total.
WOMEN = re.compile(r"(?ix)\b(women|women's|womens|ladies|female)\b")


def classify_event(event: str) -> tuple[str, str] | None:
    """`(kind, format)` for a world championship event, else None.

    kind is `open` or `women`; format is `match` for a title match and
    `knockout` for the FIDE knockout editions.
    """
    if not event:
        return None
    if not WCH_INCLUDE.search(event):
        return None
    if WCH_EXCLUDE.search(event):
        return None
    kind = "women" if WOMEN.search(event) else "open"
    fmt = "knockout" if KNOCKOUT.search(event) else "match"
    return kind, fmt


def year_of(date: str | None) -> str:
    """The year from a PGN date, or an empty string when unknown."""
    if not date:
        return ""
    head = date.split(".")[0]
    return head if head.isdigit() and len(head) == 4 else ""


def surname_of(name: str | None) -> str:
    """The comparable part of a player's name.

    Corpora spell the same person several ways; the surname is what
    survives, so grouping uses it and nothing else.
    """
    if not name:
        return ""
    head = name.split(",")[0].strip()
    return head.casefold()


def game_citation(game) -> str:
    """A game named the way a game is cited: players, event, year."""
    white = (game.header("White") or "?").strip()
    black = (game.header("Black") or "?").strip()
    event = (game.header("Event") or "?").strip()
    site = (game.header("Site") or "").strip()
    year = year_of(game.header("Date"))
    where = ", ".join(part for part in (event, site, year) if part and part != "?")
    return f"{white}-{black}, {where}" if where else f"{white}-{black}"


COLUMNS = (
    "ocn1", "kind", "format", "event", "year", "white", "black", "result", "ply",
    "citation",
)


def rows_from_pgn(paths: list[Path], annotator: Annotator, *, progress_every: int = 0):
    """Yield one record per title-match game, plus a summary.

    Two passes over the candidates: collect every game whose event name
    survives the name filter, group them by event and year, then keep
    only the groups shaped like a title match. A group's shape is what
    identifies it -- two players and a match-length run of games -- so
    an organisation inventing a new championship name cannot walk in.
    """
    seen = 0
    rejected: Counter = Counter()
    groups: dict[tuple[str, str], list] = {}

    for path in paths:
        with path.open(encoding="utf-8", errors="replace") as handle:
            for game in iter_games(handle):
                seen += 1
                if progress_every and seen % progress_every == 0:
                    print(f"  {seen:,} games read, {len(groups):,} candidate events",
                          file=sys.stderr)
                event = (game.header("Event") or "").strip()
                verdict = classify_event(event)
                if verdict is None:
                    if event and WCH_INCLUDE.search(event):
                        rejected[event] += 1
                    continue
                kind, fmt = verdict
                year = year_of(game.header("Date"))
                groups.setdefault((event, year), []).append((kind, fmt, game))

    kept_events: Counter = Counter()
    dropped_shape: Counter = Counter()
    matched = kept = 0
    for (event, year), entries in groups.items():
        #: Names vary across a corpus -- "Botvinnik, Mikhail" and
        #: "Botvinnik, M" are one man -- so players are counted by
        #: surname, and the pair only has to account for most of the
        #: seats rather than all of them, which absorbs the odd typo.
        appearances: Counter = Counter()
        for _, _, g in entries:
            for side in ("White", "Black"):
                name = surname_of(g.header(side))
                if name:
                    appearances[name] += 1
        pair = appearances.most_common(2)
        seats = sum(appearances.values())
        dominant = sum(count for _, count in pair) / seats if seats else 0

        #: A title match is two players and a match-length run of games.
        if len(pair) != 2 or dominant < 0.9 or not (MATCH_MIN <= len(entries) <= MATCH_MAX):
            dropped_shape[f"{event} ({year or 'no year'})"] = len(entries)
            continue
        kept_events[f"{event} ({year or 'no year'})"] = len(entries)
        for kind, fmt, game in entries:
            kept += 1
            match = annotator.match_game(game)
            if not match.matched:
                continue
            matched += 1
            yield {
                "ocn1": match.slug,
                "kind": kind,
                "format": fmt,
                "event": event,
                "year": year,
                "white": (game.header("White") or "").strip(),
                "black": (game.header("Black") or "").strip(),
                "result": (game.header("Result") or "").strip(),
                "ply": str(match.ply),
                "citation": game_citation(game),
            }

    yield {"__summary__": {"seen": seen, "kept": kept, "matched": matched,
                           "rejected": rejected, "kept_events": kept_events,
                           "dropped_shape": dropped_shape}}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("pgn", nargs="+", type=Path)
    parser.add_argument("--out", type=Path,
                        help="write the TSV here; omit to print the summary only")
    parser.add_argument("--rejected", action="store_true",
                        help="list events the filter rejected, most frequent first")
    parser.add_argument("--events", action="store_true",
                        help="list the events the filter kept, most frequent first")
    parser.add_argument("--progress-every", type=int, default=20000)
    args = parser.parse_args(sys.argv[1:] if argv is None else argv)

    missing = [path for path in args.pgn if not path.is_file()]
    if missing:
        print("ERROR: no such file: " + ", ".join(str(p) for p in missing), file=sys.stderr)
        return 1

    annotator = Annotator(Catalog.load())
    records: list[dict] = []
    summary: dict = {}
    for item in rows_from_pgn(args.pgn, annotator, progress_every=args.progress_every):
        if "__summary__" in item:
            summary = item["__summary__"]
        else:
            records.append(item)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        with args.out.open("w", encoding="utf-8", newline="") as handle:
            handle.write("\t".join(COLUMNS) + "\n")
            for record in records:
                handle.write("\t".join(record[column] for column in COLUMNS) + "\n")
        print(f"wrote {args.out} ({len(records)} rows)")

    open_rows = [r for r in records if r["kind"] == "open"]
    women_rows = [r for r in records if r["kind"] == "women"]
    matches = [r for r in records if r["format"] == "match"]
    knockouts = [r for r in records if r["format"] == "knockout"]
    print(f"games read          {summary.get('seen', 0):,}")
    print(f"championship games  {summary.get('kept', 0):,}")
    print(f"  matched to a slug {summary.get('matched', 0):,}")
    print(f"  open title        {len(open_rows):,}")
    print(f"  women's title     {len(women_rows):,}")
    print(f"  title matches     {len(matches):,}")
    print(f"  knockout editions {len(knockouts):,}")
    if records:
        years = sorted({r["year"] for r in records if r["year"]})
        print(f"years               {years[0]} to {years[-1]}" if years else "")
        for label, subset in (("open", open_rows), ("women", women_rows)):
            if not subset:
                continue
            top = Counter(r["ocn1"] for r in subset).most_common(5)
            print(f"  most played, {label}:")
            for slug, count in top:
                row = annotator.catalog.get(slug)
                print(f"    {count:4d}  {slug:26s} {row.canonical_name if row else ''}")

    if args.events and summary.get("dropped_shape"):
        print("\nname matched but the shape did not (players, or game count):")
        for event, count in summary["dropped_shape"].most_common(15):
            print(f"  {count:5d}  {event}")

    if args.events and summary.get("kept_events"):
        print("\ntitle matches kept:")
        for event, count in summary["kept_events"].most_common(40):
            print(f"  {count:5d}  {event}")

    if args.rejected and summary.get("rejected"):
        print("\nrejected by the filter (name matched, event did not):")
        for event, count in summary["rejected"].most_common(30):
            print(f"  {count:5d}  {event}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
