#!/usr/bin/env python3
"""Turn the Companion verdicts into an attribution manifest.

`docs/evidence/eponyms/companion-verdicts.tsv` holds what the Oxford
Companion says about each candidate attribution: the entry, its index
number, a verbatim quote, the role the book gives the person, and any
rival claimant it names. This turns the usable subset into an
`ocn.attribution_manifest.v1` for `tools/apply_attribution_manifest.py`,
which is the only thing allowed to touch the catalogue.

What makes a row usable, and why each test exists
-------------------------------------------------
* **The Companion has an entry.** No entry, no citation.
* **The quote names the person.** A retrieval that returns the right
  entry can still return one that never mentions the person the row is
  about, and an attribution whose own quote does not support it is the
  failure this whole pipeline exists to prevent.
* **The role is determined.** `unclear` rows are held back rather than
  attributed blandly. The role is the point: every other open dataset
  can say "Sicilian Defence"; almost none can say who *popularised* it
  as distinct from who invented it.

The role travels inside `attributed_to` in parentheses, which is the
convention the catalogue already uses ("Pal Benko (systematiser)"). A
rival claimant goes to `historical_notes`, because a contested name
recorded with its rival is scholarship and the same name recorded bare
is a claim the book itself would not make.

Nothing here writes the catalogue. It writes a manifest, which then gets
a dry run, and an apply only under an explicit GO.

Usage:
    python3 tools/generate_companion_manifest.py --out docs/manifests/x.json
    python3 tools/generate_companion_manifest.py --summary
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import unicodedata
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_VERDICTS = REPO_ROOT / "docs" / "evidence" / "eponyms" / "companion-verdicts.tsv"
DEFAULT_CATALOGUE = REPO_ROOT / "catalog" / "ocn-1.csv"

#: No opening number in the citation. The Companion's index numbers are
#: reliable in the book and unreliable coming back from retrieval: more
#: than half these entries cover several openings at once, and the
#: number returned is often a sibling's. `E.KID.Cls.Pet` came back as
#: 339, which the entry's own words assign to the Queen's Indian; the
#: King's Indian line is 399. An entry name is a complete citation for
#: an alphabetical reference work, and the verbatim quote travels with
#: it, so nothing is lost by dropping a number that cannot be trusted.
CITATION = ("Hooper & Whyld, 'The Oxford Companion to Chess' (2nd ed., OUP 1992), "
            "entry '{entry}'")

#: How the Companion introduces each line an entry covers: a number,
#: then "in the" and the parent opening in small capitals. Counting bare
#: numbers instead does not work -- quotes are full of move numbers, and
#: "Pd7-d6" alone would make a single-line entry look like three.
OPENING_REF = re.compile(r"in the\s+[A-Z][A-Z'\-\. >:\"]{2,}")

#: The Companion's characterisation, as a noun the catalogue can carry.
#: `unclear` is absent on purpose -- it is the reason a row is excluded.
ROLE_NOUN = {
    "originated": "originator",
    "first-published": "first to publish",
    "popularised": "populariser",
    "recommended": "advocate",
    "condemned": "critic",
}


def fold(text: str) -> str:
    stripped = "".join(c for c in unicodedata.normalize("NFKD", text)
                       if not unicodedata.combining(c))
    return re.sub(r"[^a-z]", "", stripped.lower())


#: Verbs the Companion uses, mapped to the role each supports. The
#: quote has to agree with the role before the role is written down.
ROLE_EVIDENCE = {
    "originated": r"\bintroduc|\boriginat|\bdevis|\bevolved\b|\binvent|\bpioneer|\bthe idea of\b",
    "first-published": r"\bgiven by\b|\bpublished\b|\bgiven in\b|\bfirst to publish\b|\bmonograph\b",
    "popularised": r"\bplayed\b|\bpractis|\bused by\b|\bspeciality\b|\bmade it\b|\bfavour|\badvanced by\b",
    "recommended": r"\brecommend|\badvocat|\bpreferred\b",
    "condemned": r"\bcondemn|\brejected\b",
}


def body_of(quote: str) -> str:
    """The entry with its headword removed.

    A person's name is always in the title of their own entry, so
    checking the whole quote proves nothing: "Keres Defence, 244. Known
    since the 1840s... played by HUCKLE" passes a naive test while
    crediting Keres with nothing at all.
    """
    return re.sub(r"^[^,.]{0,60}[,.]", "", quote.strip(), count=1)


def role_supported(quote: str, role: str) -> bool:
    """Do the entry's own words carry the verb the role claims?"""
    pattern = ROLE_EVIDENCE.get(role)
    return bool(pattern and re.search(pattern, quote, re.I))


def quote_names(quote: str, people: str) -> bool:
    """Does the Companion's own words mention the person being credited?

    Matched on a folded prefix of each name part, because the OCR
    mangles capitals and because Spanish and Slavic names carry more
    parts than the catalogue records.
    """
    folded = fold(body_of(quote))
    for person in people.split(";"):
        for part in person.split():
            key = fold(part)
            if len(key) >= 5 and key[:5] in folded:
                return True
    return False


def openings_in_quote(quote: str) -> int:
    """How many distinct opening lines the quoted entry covers.

    An entry naming one line states one attribution. An entry naming
    four -- "91 in the SLAV... 168 in the QUEEN'S GAMBIT Declined... 299
    and 396 in the NIMZO-INDIAN and KING'S INDIAN" -- states four, and
    the role that came back may belong to a sibling rather than to our
    row. Those are held for review instead of guessed at.

    Zero is not a gap: a top-level entry ("Clemenz Opening, 1323, named
    after the Estonian player...") names no parent because it has none.
    """
    return len(OPENING_REF.findall(quote))


def usable(row: dict[str, str]) -> bool:
    return (row["verdict"] == "entry"
            and row["role"] in ROLE_NOUN
            and bool(row["quote"].strip())
            and quote_names(row["quote"], row["person"])
            and role_supported(row["quote"], row["role"]))


def attribution_for(row: dict[str, str]) -> str:
    noun = ROLE_NOUN[row["role"]]
    people = [p.strip() for p in row["person"].split(";") if p.strip()]
    return "; ".join(f"{p} ({noun})" for p in people)


def rival_note(row: dict[str, str]) -> str:
    rival = row["rival"].strip()
    if not rival or rival.lower() in {"none", "-", "n/a"}:
        return ""
    return (f"The Oxford Companion names a rival claimant: {rival}. "
            f"Recorded as disputed rather than resolved.")


def build(rows: list[dict[str, str]], catalogue_rows: int) -> dict:
    changes = []
    for row in rows:
        source = CITATION.format(entry=row["asked_as"])
        quote = re.sub(r"\s+", " ", row["quote"]).strip().strip('"')
        fields = {
            "attributed_to": attribution_for(row),
            "attribution_source": f"{source}: \"{quote}\"",
        }
        note = rival_note(row)
        if note:
            fields["historical_notes"] = note
        changes.append({
            "ocn1": row["ocn1"],
            "evidence_grade": "CLEAR",
            "source_refs": [source],
            "fields": fields,
        })
    changes.sort(key=lambda c: c["ocn1"])

    return {
        "kind": "ocn.attribution_manifest.v1",
        "title": "Oxford Companion attributions, with the role the book gives",
        "description": (
            "DRY-RUN PROPOSAL, un-applied. Attributions for rows where Hooper & "
            "Whyld's Oxford Companion (2nd ed., 1992) has an entry for the exact "
            "line, the entry's own words name the person, and the book states a "
            "role. Each row was tied to its catalogue slug by MOVE SEQUENCE, not "
            "by name, via Wikipedia's list of openings named after people; the "
            "Companion was then asked about that exact line and its answer is "
            "quoted verbatim in attribution_source, so any row can be checked "
            "against the book. Rows the Companion does not cover, does not name "
            "the person in, or gives no role for are excluded rather than "
            "attributed blandly. The role is carried in attributed_to in "
            "parentheses, per the convention already in the catalogue. Where the "
            "Companion names a rival claimant that goes to historical_notes: a "
            "contested name recorded with its rival is scholarship, the same name "
            "recorded bare is a claim the book would not make. "
            "Passages were retrieved by notebook query over the book and are "
            "reproduced verbatim; a sample was checked against the PDF directly "
            "and matched word for word. Apply only under an explicit GO."
        ),
        "mode": "attribution_fields_only",
        "expected_catalog_rows": catalogue_rows,
        "expected_changed_rows": [c["ocn1"] for c in changes],
        "changes": changes,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--verdicts", type=Path, default=DEFAULT_VERDICTS)
    parser.add_argument("--catalogue", type=Path, default=DEFAULT_CATALOGUE)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--summary", action="store_true",
                        help="report what would be included and excluded")
    args = parser.parse_args(sys.argv[1:] if argv is None else argv)

    with args.verdicts.open(newline="", encoding="utf-8") as handle:
        verdicts = list(csv.DictReader(handle, delimiter="\t"))
    with args.catalogue.open(newline="", encoding="utf-8") as handle:
        catalogue = list(csv.DictReader(handle))
    known = {r["ocn1"] for r in catalogue}
    attributed = {r["ocn1"] for r in catalogue if r["attributed_to"].strip()}

    kept, dropped = [], {}
    for row in verdicts:
        if row["ocn1"] not in known:
            dropped[row["ocn1"]] = "not a catalogue slug"
        elif row["ocn1"] in attributed:
            dropped[row["ocn1"]] = "already attributed by hand"
        elif row["verdict"] != "entry":
            dropped[row["ocn1"]] = f"Companion verdict: {row['verdict']}"
        elif not row["quote"].strip():
            dropped[row["ocn1"]] = "no quote returned"
        elif not quote_names(row["quote"], row["person"]):
            dropped[row["ocn1"]] = "the entry's body never names the person"
        elif row["role"] not in ROLE_NOUN:
            dropped[row["ocn1"]] = f"role not determined ({row['role'] or 'blank'})"
        elif openings_in_quote(row["quote"]) > 1:
            dropped[row["ocn1"]] = "entry covers several openings; role may be a sibling's"
        elif not role_supported(row["quote"], row["role"]):
            dropped[row["ocn1"]] = f"the quote carries no verb supporting '{row['role']}'"
        else:
            kept.append(row)

    print(f"verdicts read   {len(verdicts)}")
    print(f"included        {len(kept)}")
    print(f"excluded        {len(dropped)}")
    reasons: dict[str, int] = {}
    for reason in dropped.values():
        reasons[reason] = reasons.get(reason, 0) + 1
    for reason, count in sorted(reasons.items(), key=lambda kv: -kv[1]):
        print(f"  {count:4d}  {reason}")

    roles: dict[str, int] = {}
    for row in kept:
        roles[row["role"]] = roles.get(row["role"], 0) + 1
    print("\nroles carried:", ", ".join(f"{v} {k}" for k, v in
                                        sorted(roles.items(), key=lambda kv: -kv[1])))
    print("rival claimants recorded:", sum(1 for r in kept if rival_note(r)))

    if args.summary or not args.out:
        print("\nno manifest written (use --out)")
        return 0

    manifest = build(kept, len(catalogue))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(manifest, indent=1, ensure_ascii=False) + "\n",
                        encoding="utf-8")
    print(f"\nwrote {args.out} ({len(manifest['changes'])} changes)")
    print("next: dry-run it with tools/apply_attribution_manifest.py, then GO")
    return 0


if __name__ == "__main__":
    sys.exit(main())
