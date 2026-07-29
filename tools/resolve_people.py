#!/usr/bin/env python3
"""Give the chronicle's people a public identity, or leave them anonymous.

`docs/chronicle-layer-design.md` calls `wikidata_qid` the load-bearing
column of `ocn-1.people.tsv`: a champion is a public entity with dates
and spellings in every language, and referencing that entity is cheaper
and more honest than re-litigating a biography in our own columns.
`build_chronicle.py` leaves the column empty on purpose, because it
derives people from corpus spellings and a corpus spelling is not an
identity.

This fills the column, and refuses to fill it when it cannot be sure.

The refusal is the design. Matching a surname to a Wikidata item is easy
and wrong: the search for "Steinitz" returns a footballer and a physicist
alongside the champion. So a candidate has to survive the years we
actually watched the person play, taken from the championship map:

  * born early enough to have played their first game;
  * not dead before their last one;
  * not implausibly old by the end of it.

Someone the corpus saw playing in 1886 and a Wikidata item born in 1963
are not the same human, whatever the surname says. Where more than one
candidate survives, or none does, the column stays empty and the person
is reported for review. A wrong identifier silently attaches every
opening that person played to the wrong human, and no downstream check
can catch it; an empty column is a question anyone can see.

Wikidata is cited here for entity identity only, which is the use the
design's source tiers permit. No count, ranking or claim is taken from
it.

Usage:
    python3 tools/resolve_people.py                     # dry run, report only
    python3 tools/resolve_people.py --apply --out catalog/ocn-1.people.tsv
    python3 tools/resolve_people.py --person steinitz --person lasker
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Callable, NamedTuple

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PEOPLE = REPO_ROOT / "catalog" / "ocn-1.people.tsv"
DEFAULT_WCH = REPO_ROOT / "catalog" / "ocn-1.wch.tsv"

PEOPLE_COLUMNS = ("person_id", "display_name", "wikidata_qid", "born", "died", "note")

WIKIDATA_API = "https://www.wikidata.org/w/api.php"

#: A courteous agent is the price of the public endpoint, and the docs
#: ask for a way to be contacted if a script misbehaves.
USER_AGENT = ("OCN-chess-catalogue/1.2 (https://github.com/escacsfigueres/ocn; "
              "albertpi@gmail.com) python-urllib")

Q_CHESS_PLAYER = "Q10873124"
P_OCCUPATION = "P106"
P_FIDE_ID = "P1440"
P_BORN = "P569"
P_DIED = "P570"

#: Nobody plays a world championship game at nine, and nobody plays one
#: at a hundred and eleven. Both bounds are deliberately far outside the
#: real range: they exist to reject a different human, not to referee an
#: unusual career. Carlsen was 13 at his first title-cycle appearance.
MIN_PLAYING_AGE = 10
MAX_PLAYING_AGE = 110

#: The search is fuzzy on purpose -- corpora transliterate -- so it
#: returns a wide net that the date check then cuts down.
SEARCH_LIMIT = 20

DEFAULT_RATE_PER_MINUTE = 60


class Candidate(NamedTuple):
    qid: str
    label: str
    description: str
    born: int | None
    died: int | None
    is_player: bool

    def describe(self) -> str:
        lived = f"{self.born or '?'}-{self.died or ''}"
        return f"{self.qid} ({self.label}, {lived}; {self.description})"


def year_of(timestamp: str) -> int | None:
    """The year in a Wikidata timestamp, negative years included.

    Wikidata writes `+1836-05-14T00:00:00Z`, and years before the common
    era with a leading minus. Splitting on the hyphen without minding the
    sign turns 500 BCE into the year 500.
    """
    if not timestamp:
        return None
    sign = -1 if timestamp[0] == "-" else 1
    digits = timestamp.lstrip("+-").split("-", 1)[0]
    return sign * int(digits) if digits.isdigit() else None


def _claim_values(entity: dict, prop: str) -> list:
    """Every present value for a property.

    Wikidata records "unknown value" as a snak with no `datavalue` at
    all, so a claim existing does not mean a value exists.
    """
    values = []
    for statement in entity.get("claims", {}).get(prop, []):
        datavalue = statement.get("mainsnak", {}).get("datavalue")
        if datavalue is not None:
            values.append(datavalue.get("value"))
    return values


def parse_entity(entity: dict) -> Candidate:
    """A candidate from Wikidata's entity JSON, tolerant of what is absent."""
    def first_year(prop: str) -> int | None:
        for value in _claim_values(entity, prop):
            if isinstance(value, dict) and (year := year_of(value.get("time", ""))) is not None:
                return year
        return None

    occupations = {v.get("id") for v in _claim_values(entity, P_OCCUPATION)
                   if isinstance(v, dict)}
    is_player = Q_CHESS_PLAYER in occupations or bool(_claim_values(entity, P_FIDE_ID))

    return Candidate(
        qid=entity.get("id", ""),
        label=entity.get("labels", {}).get("en", {}).get("value", ""),
        description=entity.get("descriptions", {}).get("en", {}).get("value", ""),
        born=first_year(P_BORN),
        died=first_year(P_DIED),
        is_player=is_player,
    )


def search_terms(display_name: str) -> list[str]:
    """What to ask the search for, given a corpus spelling.

    A corpus writes "Steinitz, Wilhelm"; Wikidata is titled "Wilhelm
    Steinitz". Four forms, because each rescues a different failure seen
    in the championship table:

      * the whole given name reversed, which is the ordinary case;
      * the *first* given name only -- "Timman, Jan H" finds nothing as
        "Jan H Timman" and resolves instantly as "Jan Timman";
      * surname first, which is how Wikidata titles Chinese players --
        "Hou Yifan" is an article and "Yifan Hou" is not;
      * the bare surname, for transliterations none of the above catch.

    Widening the net is safe because the date check narrows it again,
    and an ambiguity that survives leaves the column empty by design.
    """
    surname, _, given = display_name.partition(",")
    #: Corpora tag players with a club or region -- "Hou, Yifan(HLJ)" --
    #: and the tag defeats every search that carries it.
    surname = re.sub(r"\([^)]*\)", "", surname).strip()
    given = re.sub(r"\([^)]*\)", "", given).strip()

    #: An initial ("E.") is not a given name, and searching "E. Bikova"
    #: finds nothing that searching "Bikova" would not.
    parts = [word for word in given.split() if len(word.rstrip(".")) > 1]

    terms: list[str] = []
    if parts:
        #: The corpus spelling verbatim, initials and all. It is not
        #: redundant with the stripped form: "Fischer, Robert J" finds
        #: Bobby Fischer as "Robert J Fischer", matching his recorded
        #: alias, and finds nothing at all as "Robert Fischer".
        terms.append(f"{given} {surname}")
        terms.append(f"{' '.join(parts)} {surname}")
        terms.append(f"{parts[0]} {surname}")
        terms.append(f"{surname} {parts[0]}")
    if surname:
        terms.append(surname)
    return list(dict.fromkeys(term for term in terms if term.strip()))


def given_name(display_name: str) -> str:
    """The corpus's first given name, or empty when it gives only an initial."""
    _, _, given = display_name.partition(",")
    given = re.sub(r"\([^)]*\)", "", given).strip()
    parts = [word for word in given.split() if len(word.rstrip(".")) > 1]
    return parts[0] if parts else ""


def activity_window(rows: list[dict[str, str]]) -> dict[str, tuple[int, int]]:
    """First and last year each person was seen playing, by person id."""
    from build_chronicle import person_id

    seen: dict[str, list[int]] = {}
    for row in rows:
        year = row.get("year", "").strip()
        if not year.isdigit():
            continue
        for name in (row.get("white", ""), row.get("black", "")):
            if name.strip():
                seen.setdefault(person_id(name), []).append(int(year))
    return {pid: (min(years), max(years)) for pid, years in seen.items()}


def plausible(candidate: Candidate, first_year: int, last_year: int) -> bool:
    """Could this Wikidata person have played those games?"""
    if candidate.born is None:
        #: Undated, so unverifiable -- and unverifiable is what the empty
        #: column means.
        return False
    if candidate.born + MIN_PLAYING_AGE > first_year:
        return False
    if candidate.born + MAX_PLAYING_AGE < last_year:
        return False
    if candidate.died is not None and candidate.died < last_year:
        return False
    return True


def resolve(candidates: list[Candidate], window: tuple[int, int] | None,
            given: str = "") -> tuple[str, str]:
    """The one identifier the evidence supports, or an empty column and why."""
    if window is None:
        return "", "no games in the championship map, so nothing to verify against"

    first_year, last_year = window
    players = [c for c in candidates if c.is_player]
    survivors = [c for c in players if plausible(c, first_year, last_year)]

    if len(survivors) == 1:
        return survivors[0].qid, f"matched {survivors[0].describe()}"
    if not survivors:
        near = ", ".join(c.describe() for c in players[:3]) or "none"
        return "", (f"no candidate survived {first_year}-{last_year} "
                    f"(considered: {near})")

    #: A chess family puts several contemporaries under one surname. The
    #: corpus's own given name separates them when it names exactly one.
    if given:
        named = [c for c in survivors if given.lower() in c.label.lower()]
        if len(named) == 1:
            return named[0].qid, f"matched on given name {given!r}: {named[0].describe()}"

    listed = ", ".join(c.describe() for c in survivors[:4])
    return "", f"{len(survivors)} candidates survived {first_year}-{last_year}: {listed}"


class Wikidata:
    """The public API, rate-limited and injectable for tests."""

    def __init__(self, *, rate_per_minute: int = DEFAULT_RATE_PER_MINUTE,
                 opener: Callable = urllib.request.urlopen,
                 sleep: Callable[[float], None] = time.sleep) -> None:
        self._interval = 60.0 / max(rate_per_minute, 1)
        self._opener = opener
        self._sleep = sleep
        self._last = 0.0

    def _get(self, params: dict) -> dict:
        wait = self._interval - (time.monotonic() - self._last)
        if wait > 0:
            self._sleep(wait)
        url = WIKIDATA_API + "?" + urllib.parse.urlencode({**params, "format": "json"})
        request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with self._opener(request, timeout=60) as handle:
                payload = json.load(handle)
        finally:
            self._last = time.monotonic()
        return payload

    def search(self, term: str) -> list[str]:
        payload = self._get({"action": "wbsearchentities", "search": term,
                             "language": "en", "uselang": "en", "type": "item",
                             "limit": SEARCH_LIMIT})
        return [hit["id"] for hit in payload.get("search", []) if hit.get("id")]

    def entities(self, qids: list[str]) -> list[Candidate]:
        found: list[Candidate] = []
        #: The API takes fifty ids per call and rejects more.
        for start in range(0, len(qids), 50):
            batch = qids[start:start + 50]
            payload = self._get({"action": "wbgetentities", "ids": "|".join(batch),
                                 "props": "labels|descriptions|claims",
                                 "languages": "en"})
            for entity in payload.get("entities", {}).values():
                if "missing" not in entity:
                    found.append(parse_entity(entity))
        return found

    def candidates_for(self, display_name: str) -> list[Candidate]:
        qids: list[str] = []
        for term in search_terms(display_name):
            for qid in self.search(term):
                if qid not in qids:
                    qids.append(qid)
        return self.entities(qids)


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, columns: tuple[str, ...], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        handle.write("\t".join(columns) + "\n")
        for row in rows:
            handle.write("\t".join(str(row.get(c, "")) for c in columns) + "\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--people", type=Path, default=DEFAULT_PEOPLE)
    parser.add_argument("--wch", type=Path, default=DEFAULT_WCH)
    parser.add_argument("--out", type=Path, default=None,
                        help="where to write; required with --apply")
    parser.add_argument("--person", action="append",
                        help="only this person id; repeatable")
    parser.add_argument("--rate", type=int, default=DEFAULT_RATE_PER_MINUTE)
    parser.add_argument("--report", type=Path, default=None,
                        help="write the per-person reasoning here")
    parser.add_argument("--apply", action="store_true",
                        help="write the resolved table (dry run otherwise)")
    args = parser.parse_args(sys.argv[1:] if argv is None else argv)

    for path in (args.people, args.wch):
        if not path.is_file():
            print(f"ERROR: no such file: {path}", file=sys.stderr)
            return 1
    if args.apply and args.out is None:
        print("ERROR: --apply needs --out", file=sys.stderr)
        return 1

    people = read_tsv(args.people)
    windows = activity_window(read_tsv(args.wch))
    wanted = [p for p in people if not args.person or p["person_id"] in args.person]

    api = Wikidata(rate_per_minute=args.rate)
    resolved, lines = 0, []

    for index, person in enumerate(wanted, 1):
        pid, name = person["person_id"], person["display_name"]
        print(f"[{index}/{len(wanted)}] {pid}", file=sys.stderr, flush=True)
        try:
            candidates = api.candidates_for(name)
        except (urllib.error.URLError, json.JSONDecodeError, TimeoutError) as error:
            lines.append(f"{pid}\tERROR\t{error}")
            continue

        qid, reason = resolve(candidates, windows.get(pid), given_name(name))
        lines.append(f"{pid}\t{qid or '-'}\t{reason}")
        if not qid:
            continue

        resolved += 1
        match = next(c for c in candidates if c.qid == qid)
        person["wikidata_qid"] = qid
        person["born"] = str(match.born) if match.born is not None else ""
        person["died"] = str(match.died) if match.died is not None else ""
        person["note"] = ("seen in world championship games; identity confirmed "
                          "against Wikidata by playing dates")

    print(f"\nresolved {resolved}/{len(wanted)}; "
          f"{len(wanted) - resolved} left unverified")
    for line in lines:
        if "\t-\t" in line or "\tERROR\t" in line:
            print("  " + line.replace("\t", "  "))

    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text("person_id\twikidata_qid\treason\n" + "\n".join(lines)
                               + "\n", encoding="utf-8")
        print(f"\nreport: {args.report}")

    if not args.apply:
        print("\ndry run: nothing written")
        return 0

    write_tsv(args.out, PEOPLE_COLUMNS, people)
    print(f"\nwrote {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
