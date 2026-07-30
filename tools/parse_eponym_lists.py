#!/usr/bin/env python3
"""Read Wikipedia's eponym lists into reviewable evidence, joined by position.

`List of chess openings named after people` is the systematic survey of
the naming question that the treatise pass went looking for and did not
find: roughly 270 entries, each giving the opening, its move sequence,
the person, and -- the part that matters -- a footnote saying who says
so. `docs/treatise-school-findings.md` records that Winter's *Chess
Notes* answers bibliography and not attribution, because it corrects
contested names and takes settled ones as read. This list is the
opposite shape: it states the settled ones and cites them.

Three rules make it usable rather than merely tempting.

**The join is by position, never by name.** Every entry carries its
moves, so an entry becomes a catalogue row only when the move sequence
converts to the exact `moves_uci` of that row. Matching "Alekhine
Variation" against a row called "Alekhine Variation" is how two
unrelated lines get silently merged; matching `d2d4 g8f6 c2c4 e7e5 ...`
cannot do that. Entries whose moves do not convert, or convert to a
position the catalogue does not hold, are reported and dropped.

**Nothing here is `verified`.** That grade means somebody read the page.
Following a footnote to a book nobody opened is precisely the error this
project has already retracted once, so the best grade this tool will
issue is `attested`, and an entry with no footnote at all gets
`traditional`. The tier of the underlying source travels in its own
column, so the reference-grade ones can be promoted later by a human
with the book actually in hand.

**Wikipedia is the finding aid, not the citation of record.** The
catalogue's own convention is already this: the Trompowsky row cites
Hooper and Whyld with a page and adds "via Wikipedia footnote". Same
doctrine as the design's telescope rule -- search the aggregator, cite
what it points at, disclose the route.

The output is evidence for review. This tool writes no catalogue row and
no manifest; turning its TSV into an attribution lot is a separate,
gated step.

Usage:
    python3 tools/parse_eponym_lists.py --wiki people.wiki --out evidence.tsv
    python3 tools/parse_eponym_lists.py --wiki people.wiki --unmatched
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path
from typing import NamedTuple

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools"))

from chess_uci import uci_sequence_from_pgn  # noqa: E402

DEFAULT_CATALOGUE = REPO_ROOT / "catalog" / "ocn-1.csv"

#: Wikipedia separates the parts of an entry with a *spaced* en dash. The
#: spacing is load-bearing: plenty of openings carry an unspaced en dash
#: inside their own name -- Blackmar-Diemer, Caro-Kann, Alekhine-Chatard
#: -- and splitting on the bare character truncates them mid-name.
DASH = " – "

MOVES_RE = re.compile(r"^1\.\s*[A-Za-z]")
LINK_RE = re.compile(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]")
REF_RE = re.compile(r"<ref[^>]*/>|<ref.*?</ref>|\{\{sfn[^}]*\}\}", re.S | re.I)
TEMPLATE_RE = re.compile(r"\{\{[^{}]*\}\}")

PLACE_COLUMNS = (
    "ocn1", "canonical_name", "wikipedia_name", "place", "relation",
    "moves_san", "moves_uci", "source_tier", "evidence_grade",
    "already_attributed", "citation",
)

#: Words that name the kind of opening rather than the place itself.
GENERIC = {"gambit", "defense", "defence", "variation", "attack", "opening",
           "system", "countergambit", "counter-gambit", "game", "line",
           "trap", "in", "the", "of"}

OUTPUT_COLUMNS = (
    "ocn1", "canonical_name", "wikipedia_name", "person", "people_raw",
    "wikipedia_article", "moves_san", "moves_uci", "source_tier",
    "evidence_grade", "already_attributed", "citation",
)


class Entry(NamedTuple):
    wiki_name: str
    moves_san: str
    moves_uci: str
    people: list[str]
    people_raw: str
    articles: list[str]
    refs: str
    tier: str
    grade: str
    problem: str


class Match(NamedTuple):
    entry: Entry
    ocn1: str
    canonical_name: str
    already_attributed: bool


def wiki_links(text: str) -> list[tuple[str, str]]:
    """Every `[[target|display]]` in a fragment, as (target, display)."""
    return [(target.strip(), (display or target).strip())
            for target, display in LINK_RE.findall(text)]


def strip_refs(line: str) -> tuple[str, str]:
    """The line without its citations, and the citations on their own.

    Short-footnote templates (`{{sfn|...}}`) count: they are citations
    that happen not to be `<ref>` tags, and treating them as prose would
    grade a cited entry as uncited.
    """
    refs = " ".join(REF_RE.findall(line))
    return REF_RE.sub("", line), refs


def source_tier(refs: str) -> str:
    """What class of source the entry rests on."""
    lowered = refs.lower()
    if not lowered.strip():
        return "none"
    if "oxford companion" in lowered or "hooper" in lowered:
        return "oxford-companion"
    if "sunnucks" in lowered or "encyclopaedia of chess" in lowered:
        return "encyclopaedia"
    if "cite book" in lowered or "cite journal" in lowered:
        return "book"
    return "web"


def grade_for(tier: str) -> str:
    """The honest grade for a claim sourced this way.

    Never `verified`: that grade is reserved for a source someone in
    this project has actually read, and a footnote is not a reading.
    """
    return "traditional" if tier == "none" else "attested"


def _clean(text: str) -> str:
    text = TEMPLATE_RE.sub("", text)
    text = LINK_RE.sub(lambda m: (m.group(2) or m.group(1)), text)
    return re.sub(r"\s+", " ", text.replace("'''", "").replace("''", "")).strip()


def _split_trailing_link(text: str) -> tuple[str, str]:
    """Peel a person off the end of a move list.

    A few entries drop the "named after" wording entirely and simply put
    the linked name after the moves, which otherwise parses as a move.
    """
    match = re.search(r"(\[\[[^\]]+\]\](?:\s*(?:and|,)\s*\[\[[^\]]+\]\])*)\s*$", text)
    if match is None:
        return text, ""
    return text[:match.start()], match.group(1)


def parse_entry(line: str) -> Entry | None:
    """One list bullet, or None when the line is not a usable entry."""
    if not line.lstrip().startswith("*"):
        return None

    body, refs = strip_refs(line)
    parts = [part.strip() for part in body.lstrip().lstrip("*").split(DASH)]

    moves_san, person_clause = "", ""
    for part in parts:
        if not MOVES_RE.match(part):
            continue
        #: A maintenance tag hung off the last move leaves a stray brace
        #: sitting where a move should be.
        part = TEMPLATE_RE.sub("", part).strip()
        #: Some entries omit the dash before "named after", which glues
        #: the clause onto the moves and makes "named" parse as a move.
        head, _, tail = part.partition("named after")
        if not tail:
            head, tail = _split_trailing_link(head)
        moves_san, person_clause = head.strip(), tail.strip()
        break
    if not moves_san:
        return None

    if not person_clause:
        person_clause = next(
            (part[len("named after"):].strip() for part in parts
             if part.lower().startswith("named after")), "")

    links = wiki_links(person_clause)
    people = [display for _, display in links] or (
        [_clean(person_clause)] if _clean(person_clause) else [])

    try:
        moves_uci, problem = uci_sequence_from_pgn(moves_san), ""
    except Exception as error:  # the module raises plain ValueErrors
        moves_uci, problem = "", str(error)

    tier = source_tier(refs)
    return Entry(
        wiki_name=_clean(parts[0]) if parts else "",
        moves_san=moves_san,
        moves_uci=moves_uci,
        people=people,
        people_raw=_clean(person_clause),
        articles=[target for target, _ in links],
        refs=re.sub(r"\s+", " ", refs).strip(),
        tier=tier,
        grade=grade_for(tier),
        problem=problem,
    )


def bullets(wikitext: str) -> list[str]:
    """The list's bullets, each reassembled onto one line.

    A citation frequently runs onto the following line, and a `<ref>`
    read line by line never closes -- so its markup survives into the
    person's name.
    """
    found: list[str] = []
    for line in wikitext.splitlines():
        if line.lstrip().startswith("*"):
            found.append(line)
        elif found and line.strip() and not line.startswith("="):
            found[-1] += " " + line.strip()
    return found


def parse_list(wikitext: str) -> list[Entry]:
    entries = []
    for bullet in bullets(wikitext):
        entry = parse_entry(bullet)
        if entry is not None:
            entries.append(entry)
    return entries


def join(entries: list[Entry],
         catalogue: list[dict[str, str]]) -> tuple[list[Match], list[Entry]]:
    """Attach each entry to the catalogue row holding the same position."""
    by_uci: dict[str, dict[str, str]] = {}
    for row in catalogue:
        moves = row.get("moves_uci", "").strip()
        if moves:
            by_uci.setdefault(moves, row)

    matched: list[Match] = []
    unmatched: list[Entry] = []
    for entry in entries:
        row = by_uci.get(entry.moves_uci) if entry.moves_uci else None
        if row is None:
            unmatched.append(entry)
            continue
        matched.append(Match(
            entry=entry,
            ocn1=row["ocn1"],
            canonical_name=row.get("canonical_name", ""),
            already_attributed=bool(row.get("attributed_to", "").strip()),
        ))
    return matched, unmatched


def place_in(name: str) -> str:
    """The place a Wikipedia opening name is built on, without the kind word."""
    head = name.split(" of ")[0].split(",")[0].split("(")[0]
    words = [w for w in head.split() if w.lower().strip(".") not in GENERIC]
    return " ".join(words).strip()


def names_the_place(place: str, canonical: str) -> bool:
    """Does OUR name carry the place, or do we call the line something else?

    This is the whole distinction for a place lot. `named-after-place`
    is a fact about a *name*, not about a position: Wikipedia calls
    1.d4 d5 2.c4 the Aleppo Gambit, and if the catalogue calls it
    "Queen's Gambit, c4" then our row is not named after Aleppo. That is
    an alias we may be missing, not an attribution we can make.
    """
    def key(text: str) -> str:
        stripped = "".join(c for c in unicodedata.normalize("NFKD", text)
                           if not unicodedata.combining(c))
        return re.sub(r"[^a-z]", "", stripped.lower())
    return bool(key(place)) and key(place) in key(canonical)


def citation_for(entry: Entry) -> str:
    """How the row should read if it ever becomes an attribution.

    The underlying source is named and the route is disclosed, which is
    the convention the catalogue's existing Trompowsky row already sets.
    """
    if entry.tier == "none":
        return ("no source cited in Wikipedia's list of chess openings named "
                "after people; recorded as traditional usage only")
    return (f"{entry.refs[:300]} -- cited by Wikipedia, 'List of chess openings "
            f"named after people'; not independently checked")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--wiki", type=Path, required=True,
                        help="wikitext of the eponym list")
    parser.add_argument("--catalogue", type=Path, default=DEFAULT_CATALOGUE)
    parser.add_argument("--out", type=Path, default=None,
                        help="write the joined evidence here")
    parser.add_argument("--unmatched", action="store_true",
                        help="list the entries that found no catalogue row")
    parser.add_argument("--places", action="store_true",
                        help="read the list as place names rather than people")
    args = parser.parse_args(sys.argv[1:] if argv is None else argv)

    for path in (args.wiki, args.catalogue):
        if not path.is_file():
            print(f"ERROR: no such file: {path}", file=sys.stderr)
            return 1

    entries = parse_list(args.wiki.read_text(encoding="utf-8"))
    with args.catalogue.open(newline="", encoding="utf-8") as handle:
        catalogue = list(csv.DictReader(handle))
    matched, unmatched = join(entries, catalogue)

    broken = [e for e in entries if e.problem]
    fresh = [m for m in matched if not m.already_attributed]

    print(f"entries parsed      {len(entries):5d}")
    print(f"  moves unparsable  {len(broken):5d}  (Wikipedia typos, reported below)")
    print(f"matched to a slug   {len(matched):5d}")
    print(f"  already attributed{len([m for m in matched if m.already_attributed]):5d}"
          f"  (left alone; a reviewed row outranks a footnote)")
    print(f"  NEW attributions  {len(fresh):5d}")
    print(f"no catalogue row    {len(unmatched) - len(broken):5d}")

    tiers = Counter(m.entry.tier for m in fresh)
    print("\nsource tier of the new ones:")
    for tier, count in tiers.most_common():
        print(f"  {count:4d}  {tier} -> {grade_for(tier)}")

    if broken:
        print("\nmoves that do not play out (Wikipedia errata):")
        for entry in broken:
            print(f"  {entry.wiki_name[:44]:<44} {entry.moves_san[:40]}")
            print(f"      {entry.problem}")

    if args.unmatched:
        print("\nno catalogue row holds this position:")
        for entry in unmatched:
            if entry.problem:
                continue
            print(f"  {entry.wiki_name[:48]:<48} {entry.moves_san[:44]}")

    if args.out and args.places:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        kept = 0
        with args.out.open("w", encoding="utf-8", newline="") as handle:
            handle.write("\t".join(PLACE_COLUMNS) + "\n")
            for match in matched:
                entry = match.entry
                place = place_in(entry.wiki_name)
                ours = names_the_place(place, match.canonical_name)
                kept += ours
                handle.write("\t".join([
                    match.ocn1, match.canonical_name, entry.wiki_name, place,
                    "named-after-place" if ours else "alias-candidate",
                    entry.moves_san, entry.moves_uci, entry.tier, entry.grade,
                    "yes" if match.already_attributed else "", citation_for(entry),
                ]) + "\n")
        print(f"\nwrote {args.out}")
        print(f"  named-after-place (our own name carries it): {kept}")
        print(f"  alias-candidate (we call it otherwise)     : {len(matched) - kept}")
        print("\nevidence only: no catalogue row and no manifest was written")
        return 0

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        with args.out.open("w", encoding="utf-8", newline="") as handle:
            handle.write("\t".join(OUTPUT_COLUMNS) + "\n")
            for match in matched:
                entry = match.entry
                handle.write("\t".join([
                    match.ocn1, match.canonical_name, entry.wiki_name,
                    "; ".join(entry.people), entry.people_raw,
                    "; ".join(entry.articles), entry.moves_san, entry.moves_uci,
                    entry.tier, entry.grade,
                    "yes" if match.already_attributed else "",
                    citation_for(entry),
                ]) + "\n")
        print(f"\nwrote {args.out}")

    print("\nevidence only: no catalogue row and no manifest was written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
