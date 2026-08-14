#!/usr/bin/env python3
"""Turn the championship map into the chronicle layer's three sidecars.

`docs/chronicle-layer-design.md` specifies people, events and claims as
separate tables joined by one claims row per fact, so that "which
openings decided championships" and "what did this player play" are the
same table read from different sides. This builds the first population
of all three from `catalog/ocn-1.wch.tsv`, which is itself derived from
public record.

Nothing here is curated. Every row traces to a game the mapper found,
and every claim names its games the way a game is cited: players, event,
year. What the tool deliberately does NOT do is guess: a person's
Wikidata identifier, dates and full name are left empty rather than
inferred from a corpus spelling, because a wrong identifier is worse
than a missing one -- it silently attaches an opening to the wrong human.
Those columns are filled by review, one person at a time.

It **merges** into the three tables rather than replacing them. The map
is one source of rows and no longer the only one: the files now carry 59
Wikidata identities filled in by review, 119 place claims, seven print
attestations and the publication events a manuscript needs, none of which
the map can produce. A row the builder does not generate is kept, an
empty cell takes the generated value, and a cell that already says
something keeps saying it and prints the disagreement.

Usage:
    python3 tools/build_chronicle.py --out-dir catalog
    python3 tools/build_chronicle.py --dry-run          # counts only
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_WCH = REPO_ROOT / "catalog" / "ocn-1.wch.tsv"

PEOPLE_COLUMNS = ("person_id", "display_name", "wikidata_qid", "born", "died", "note")
EVENT_COLUMNS = ("event_id", "display_name", "kind", "format", "year", "participants",
                 "games", "source")
CLAIM_COLUMNS = ("ocn1", "relation", "subject_type", "subject_id", "date",
                 "games", "source_ref", "evidence_grade", "note")

#: The championship map is machine-derived from public game records, so
#: its claims carry the grade that describes exactly that: attested by a
#: public corpus, not read out of a reference work. Nothing here claims
#: `verified`; that grade is for a source someone has read.
GRADE = "attested"

SOURCE = ("LumbrasGigaBase (freely downloadable), via tools/build_wch_map.py; "
          "each game identified by players, event and year")

#: Regrouping the map by player pair exposes contamination the map could
#: not see: a corpus files the odd club game under a championship event
#: tag, and inside a legitimate group of fourteen it rides along
#: unnoticed. A title match is a run of games between one pair, so a pair
#: with fewer than this many games inside a championship event is a
#: mislabelled game rather than a match. They are dropped and reported,
#: never silently kept.
MIN_MATCH_GAMES = 4

#: A corpus writes an unknown player as "?" or leaves the field empty.
#: Neither is a person.
UNKNOWN = {"", "?", "??", "N.N.", "NN", "unknown"}


def slugify(text: str) -> str:
    """A stable id from a name: ascii, lowercase, hyphens."""
    folded = (text.replace("ø", "o").replace("æ", "ae").replace("ß", "ss"))
    import unicodedata
    stripped = "".join(
        ch for ch in unicodedata.normalize("NFKD", folded)
        if not unicodedata.combining(ch)
    )
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", stripped.lower())).strip("-")


def person_id(name: str) -> str:
    """A person's id from the corpus spelling of their name.

    The surname carries it: a corpus writes the same player several ways,
    and the surname is the part that survives.
    """
    surname = name.split(",")[0].strip()
    return slugify(surname)


def read_wch(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def read_tsv(path: Path) -> list[dict[str, str]]:
    """The table as it stands, or nothing if this is the first run."""
    if not path.is_file():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def identity(row: dict[str, str], key: str | tuple[str, ...]) -> str | tuple[str, ...]:
    """What makes this row this row. Events and people have an id column;
    claims are identified by opening, relation and subject together."""
    if isinstance(key, str):
        return row[key]
    return tuple(row[column] for column in key)


def merge_rows(
    existing: list[dict[str, str]],
    generated: list[dict[str, str]],
    key: str | tuple[str, ...],
) -> tuple[list[dict[str, str]], dict]:
    """Fold a regeneration into the table on disk without losing anything.

    The championship map is one source of rows, not the only one. The
    files have since accumulated Wikidata identities filled in one person
    at a time, thirteen corrected participant spellings, 119 place claims
    and the publication events a manuscript needs. Overwriting is how all
    of that disappears, so:

    - a row the builder does not generate is kept;
    - a row it generates that is not on disk is added;
    - an empty cell takes the generated value;
    - a cell that already says something keeps saying it, and the
      disagreement is reported rather than resolved.

    The last rule is the one that matters. A regeneration cannot know
    whether a value on disk is a correction or staleness, and guessing
    either way is worse than printing it and letting a human look.
    """
    generated_by_key = {identity(row, key): row for row in generated}
    report: dict = {"kept": 0, "added": 0, "filled": 0,
                    "diverged": 0, "divergences": []}
    merged: list[dict[str, str]] = []

    for row in existing:
        fresh = generated_by_key.get(identity(row, key))
        if fresh is None:
            report["kept"] += 1
            merged.append(dict(row))
            continue
        out = dict(row)
        for column, value in fresh.items():
            current = out.get(column, "")
            if not current:
                if value:
                    report["filled"] += 1
                out[column] = value
            elif value and value != current:
                report["diverged"] += 1
                report["divergences"].append(
                    (identity(row, key), column, current, value)
                )
        merged.append(out)

    on_disk = {identity(row, key) for row in existing}
    for row in generated:
        if identity(row, key) not in on_disk:
            report["added"] += 1
            merged.append(dict(row))

    return merged, report


def build(rows: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    """The three tables, from the championship map."""
    people: dict[str, dict[str, str]] = {}
    events: dict[str, dict] = {}
    claims: dict[tuple[str, str], dict] = {}

    dropped: Counter = Counter()

    #: First pass: group by year and player pair, so a mislabelled game
    #: can be told from a match before anything is written.
    pairs: dict[tuple, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        names = [row["white"].strip(), row["black"].strip()]
        if any(name in UNKNOWN for name in names):
            dropped[f"unnamed player in {row['event']} ({row['year']})"] += 1
            continue
        key = (row["year"], tuple(sorted(person_id(name) for name in names)))
        pairs[key].append(row)

    for key, group in list(pairs.items()):
        if len(group) < MIN_MATCH_GAMES:
            year, ids = key
            dropped[f"{' vs '.join(ids)} ({year}): {len(group)} game(s), "
                    f"too few for a title match"] += len(group)
            del pairs[key]

    for row in [row for group in pairs.values() for row in group]:
        year = row["year"]
        players = [row["white"], row["black"]]
        ids = []
        for name in players:
            if not name:
                continue
            pid = person_id(name)
            ids.append(pid)
            #: The longest spelling seen wins as the display name: a
            #: corpus that has both "Botvinnik, M" and "Botvinnik,
            #: Mikhail" knows the fuller one.
            existing = people.get(pid)
            if existing is None or len(name) > len(existing["display_name"]):
                people[pid] = {
                    "person_id": pid, "display_name": name, "wikidata_qid": "",
                    "born": "", "died": "",
                    "note": "seen in world championship games; identity unverified",
                }

        event_id = f"wch-{year or 'undated'}-{'-'.join(sorted(set(ids)))}"
        event = events.get(event_id)
        if event is None:
            event = events[event_id] = {
                "event_id": event_id,
                "display_name": row["event"],
                "kind": "wch_match" if row["kind"] == "open" else "wch_match_women",
                "format": row["format"],
                "year": year,
                "participants": set(),
                "games": 0,
                "source": SOURCE,
            }
        event["participants"].update(ids)
        event["games"] += 1

        key = (row["ocn1"], event_id)
        claim = claims.get(key)
        if claim is None:
            claim = claims[key] = {
                "ocn1": row["ocn1"], "relation": "wch-game",
                "subject_type": "event", "subject_id": event_id, "date": year,
                "games": 0,
                #: One example citation per claim. A reader checks a claim
                #: by looking up a game, so the claim carries one.
                "source_ref": row["citation"],
                "evidence_grade": GRADE, "note": "",
            }
        claim["games"] += 1

    event_rows = []
    for event in events.values():
        event_rows.append({
            **event,
            "participants": "|".join(sorted(event["participants"])),
            "games": str(event["games"]),
        })
    claim_rows = [{**claim, "games": str(claim["games"])} for claim in claims.values()]

    return {
        "dropped": dropped,
        "people": sorted(people.values(), key=lambda r: r["person_id"]),
        "events": sorted(event_rows, key=lambda r: (r["year"], r["event_id"])),
        "claims": sorted(claim_rows, key=lambda r: (r["subject_id"], r["ocn1"])),
    }


def write_tsv(path: Path, columns: tuple[str, ...], rows: list[dict[str, str]]) -> None:
    """Written the way `csv.DictReader` reads it.

    Joining on tabs was enough while every row came from the map. It
    stopped being enough once curated rows arrived: a source_ref quotes
    the sentence it rests on, and a value that *begins* with a quote is
    silently truncated when the reader takes it back.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(columns)
        for row in rows:
            writer.writerow([str(row.get(column, "")) for column in columns])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--wch", type=Path, default=DEFAULT_WCH)
    parser.add_argument("--out-dir", type=Path, default=REPO_ROOT / "catalog")
    parser.add_argument("--dry-run", action="store_true",
                        help="report the counts and write nothing")
    args = parser.parse_args(sys.argv[1:] if argv is None else argv)

    if not args.wch.is_file():
        print(f"ERROR: no championship map at {args.wch}. Build it first with "
              f"tools/build_wch_map.py.", file=sys.stderr)
        return 1

    tables = build(read_wch(args.wch))
    people, events, claims = tables["people"], tables["events"], tables["claims"]
    dropped = tables["dropped"]

    print(f"people  {len(people):5d}  (identities unverified: "
          f"{sum(1 for p in people if not p['wikidata_qid'])})")
    kinds = Counter(e["kind"] for e in events)
    print(f"events  {len(events):5d}  " + ", ".join(f"{k}={v}" for k, v in sorted(kinds.items())))
    print(f"claims  {len(claims):5d}  openings named: "
          f"{len({c['ocn1'] for c in claims})}")

    per_opening = Counter()
    for claim in claims:
        per_opening[claim["ocn1"]] += int(claim["games"])
    print("\nmost championship games, by opening:")
    for slug, games in per_opening.most_common(5):
        print(f"  {games:4d}  {slug}")

    if dropped:
        total = sum(dropped.values())
        print(f"\ndropped {total} game(s) that a corpus filed under a championship "
              f"but no title match played:")
        for reason, count in dropped.most_common(10):
            print(f"  {count:4d}  {reason}")

    tables = [
        ("ocn-1.people.tsv", PEOPLE_COLUMNS, people, "person_id"),
        ("ocn-1.events.tsv", EVENT_COLUMNS, events, "event_id"),
        ("ocn-1.claims.tsv", CLAIM_COLUMNS, claims,
         ("ocn1", "relation", "subject_id")),
    ]
    merged = []
    print()
    for name, columns, rows, key in tables:
        path = args.out_dir / name
        result, report = merge_rows(read_tsv(path), rows, key)
        merged.append((path, columns, result))
        print(f"{name:20s} {len(result):5d} rows  "
              f"kept {report['kept']}, added {report['added']}, "
              f"filled {report['filled']}, diverged {report['diverged']}")
        for row_id, column, on_disk, generated_value in report["divergences"][:20]:
            print(f"    {row_id} {column}: on disk '{on_disk}', "
                  f"generated '{generated_value}' — kept the file's")
        if report["diverged"] > 20:
            print(f"    ... and {report['diverged'] - 20} more")

    if args.dry_run:
        print("\ndry run: nothing written")
        return 0

    for path, columns, rows in merged:
        write_tsv(path, columns, rows)
    print(f"\nwrote {args.out_dir}/ocn-1.{{people,events,claims}}.tsv")
    return 0


if __name__ == "__main__":
    sys.exit(main())
