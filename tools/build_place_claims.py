#!/usr/bin/env python3
"""Turn the place-named openings into chronicle claims.

`docs/non-person-opening-name-taxonomy.md` settled that a non-person
descriptor never receives `attributed_to`: the catalogue's attribution
columns are for people, and filling them with "Vienna" or "Abbazia"
would misuse a column whose whole meaning is a human being credited.

That decision is about the CSV. It is not a decision that the fact has
nowhere to live. `docs/chronicle-layer-design.md` puts
`named-after-place` in the claims table's closed relation set precisely
for this, and the claims sidecar is additive and typed -- so a place
name becomes a row with a subject type, a source and a grade, instead of
prose in a notes field nobody can query.

This reads the evidence produced by `parse_eponym_lists.py --places` and
emits claims for the rows where **our own canonical name carries the
place**. Rows where Wikipedia uses a place name and the catalogue does
not are excluded upstream: `named-after-place` is a fact about a name,
and asserting it for a name we do not use would be false.

Every claim is `attested` at best. The source is Wikipedia's list, which
is a finding aid; the grade says so.

Usage:
    python3 tools/build_place_claims.py --dry-run
    python3 tools/build_place_claims.py --out docs/evidence/eponyms/place-claims.tsv
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_IN = REPO_ROOT / "docs" / "evidence" / "eponyms" / "named-after-places.tsv"
DEFAULT_CLAIMS = REPO_ROOT / "catalog" / "ocn-1.claims.tsv"

CLAIM_COLUMNS = ("ocn1", "relation", "subject_type", "subject_id", "date",
                 "games", "source_ref", "evidence_grade", "note")

RELATION = "named-after-place"
SUBJECT_TYPE = "place"

#: Names Wikipedia files under places that are not places. There is no
#: mechanical test for this -- "Amazon" is a river and also a fairy
#: piece -- so the exclusions are listed with their reason and reviewed
#: as a list rather than inferred one row at a time.
NOT_A_PLACE = {
    "amazon": "the amazon is a fairy piece (queen + knight); D.QPG.Ama is "
              "1.d4 d5 2.Qd3, an early queen sortie, not a claim about Brazil",
    "kahiko-hula": "kahiko and hula are Hawaiian dances, not places",
}

SOURCE = ("Wikipedia, 'List of chess openings named after places'; the opening "
          "was tied to this catalogue row by move sequence, and the catalogue's "
          "own name carries the place")


def slugify(text: str) -> str:
    """A stable place id: ascii, lowercase, hyphens."""
    folded = text.replace("ø", "o").replace("æ", "ae").replace("ß", "ss")
    stripped = "".join(c for c in unicodedata.normalize("NFKD", folded)
                       if not unicodedata.combining(c))
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", stripped.lower())).strip("-")


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def build(rows: list[dict[str, str]]) -> tuple[list[dict[str, str]], Counter]:
    """Claims for the rows whose own name carries the place."""
    claims: list[dict[str, str]] = []
    skipped: Counter = Counter()
    seen: set[tuple[str, str]] = set()

    for row in rows:
        if row["relation"] != RELATION:
            skipped["catalogue names the line something else (alias candidate)"] += 1
            continue
        place = row["place"].strip()
        if not place:
            skipped["no place could be read from the name"] += 1
            continue
        subject = slugify(place)
        if subject in NOT_A_PLACE:
            skipped[f"not a place: {NOT_A_PLACE[subject]}"] += 1
            continue
        key = (row["ocn1"], subject)
        if key in seen:
            skipped["duplicate opening/place pair"] += 1
            continue
        seen.add(key)
        claims.append({
            "ocn1": row["ocn1"],
            "relation": RELATION,
            "subject_type": SUBJECT_TYPE,
            "subject_id": subject,
            "date": "",
            "games": "",
            "source_ref": SOURCE,
            #: Never better than attested: the source is a finding aid,
            #: not a reference work someone has read on this point.
            "evidence_grade": "attested",
            "note": f"catalogue name '{row['canonical_name']}' carries '{place}'",
        })

    claims.sort(key=lambda c: (c["ocn1"], c["subject_id"]))
    return claims, skipped


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--in", dest="source", type=Path, default=DEFAULT_IN)
    parser.add_argument("--claims", type=Path, default=DEFAULT_CLAIMS,
                        help="the live claims table, to report what would be added")
    parser.add_argument("--out", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(sys.argv[1:] if argv is None else argv)

    if not args.source.is_file():
        print(f"ERROR: no such file: {args.source}", file=sys.stderr)
        return 1

    claims, skipped = build(read_tsv(args.source))
    places = Counter(c["subject_id"] for c in claims)

    print(f"claims built    {len(claims)}")
    print(f"distinct places {len(places)}")
    for reason, count in skipped.most_common():
        print(f"  skipped {count:4d}  {reason}")

    if args.claims.is_file():
        live = read_tsv(args.claims)
        kinds = Counter(r["relation"] for r in live)
        print(f"\nlive claims table: {len(live)} rows, "
              f"relations {dict(kinds)}")
        print(f"this lot would make it {len(live) + len(claims)} rows "
              f"across {len(kinds) + 1} relations")

    print("\nplaces named most often:")
    for place, count in places.most_common(8):
        print(f"  {count:3d}  {place}")

    if args.out and not args.dry_run:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        with args.out.open("w", encoding="utf-8", newline="") as handle:
            handle.write("\t".join(CLAIM_COLUMNS) + "\n")
            for claim in claims:
                handle.write("\t".join(claim[c] for c in CLAIM_COLUMNS) + "\n")
        print(f"\nwrote {args.out}")
    else:
        print("\ndry run: nothing written")

    print("proposal only: the live claims table is untouched")
    return 0


if __name__ == "__main__":
    sys.exit(main())
