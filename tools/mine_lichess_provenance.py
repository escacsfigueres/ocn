#!/usr/bin/env python3
"""Recover where modern opening names came from, out of Lichess's git history.

The Oxford Companion is dated 1992 and answers nothing about a name
coined since. For those the usual answer is that nobody knows -- but for
a large part of the vocabulary in daily use, somebody does, and it is
written down.

Lichess names openings from `lichess-org/chess-openings`, a public
repository maintained by pull request. Every name in it was added by a
person, on a date, in a commit that often says why. That makes the
provenance of a modern name a citable public fact of exactly the kind
`docs/chronicle-layer-design.md` asks for, and one no other open chess
dataset carries.

Two kinds of event come out of the history, and the second is the
valuable one:

**First naming.** The commit where a position first acquired any name.
Most of these land in two bulk imports (2019 and 2021) and say little
beyond "this came from the initial data", so they are reported but not
claimed.

**Rename.** A commit that changed the name of a position it already
named. These are editorial decisions with an author and a date, and some
are substantive: "Schilling-Kostic Gambit" became "Blackburne-Kostić
Gambit", "Lean Variation" became "Colorado Countergambit", and
"Blackmar Gambit" became "Blackmar-Diemer Gambit", undoing a rename made
two years earlier.

Trivial changes are filtered out. Restoring a diacritic or adding a
missing comma is not a naming decision, and treating it as one would
bury the twenty that are under two hundred that are not.

The join is by position: Lichess stores a SAN move sequence, which is
converted and matched against `moves_uci`. Names are never matched to
names.

Requires a clone of the repository; nothing is vendored, since what is
worth keeping is the finding and its commit URL.

Usage:
    git clone https://github.com/lichess-org/chess-openings.git /tmp/co
    python3 tools/mine_lichess_provenance.py --repo /tmp/co --out evidence.tsv
"""
from __future__ import annotations

import argparse
import csv
import difflib
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools"))

from chess_uci import uci_sequence_from_pgn  # noqa: E402

DEFAULT_CATALOGUE = REPO_ROOT / "catalog" / "ocn-1.csv"

COLUMNS = ("ocn1", "canonical_name", "relation", "renamed_from", "renamed_to",
           "date", "author", "commit", "commit_subject", "source_ref",
           "evidence_grade")

ROW = re.compile(r"^([A-E]\d\d)\t([^\t]+)\t(.+)$")
COMMIT_URL = "https://github.com/lichess-org/chess-openings/commit/{sha}"

#: A rename below this similarity is an editorial decision; at or above
#: it the change is punctuation, a diacritic or a typo. Both matter, but
#: only one is a fact about naming.
SUBSTANTIVE_BELOW = 0.93


def history(repo: Path) -> str:
    return subprocess.run(
        ["git", "log", "--reverse", "--date=short",
         "--format=@@@|%H|%ad|%an|%s", "-p", "--", "*.tsv"],
        capture_output=True, text=True, cwd=repo, check=True).stdout


def events(diff: str) -> tuple[dict[str, dict], list[dict]]:
    """First-naming events by position, and every rename."""
    named: dict[str, dict] = {}
    renames: list[dict] = []
    for chunk in diff.split("@@@|")[1:]:
        head, _, body = chunk.partition("\n")
        bits = head.split("|", 3)
        if len(bits) < 4:
            continue
        commit = {"sha": bits[0][:9], "date": bits[1], "author": bits[2],
                  "subject": bits[3].strip()}
        added: dict[str, str] = {}
        removed: dict[str, str] = {}
        for line in body.splitlines():
            if line.startswith(("+++", "---")):
                continue
            if line.startswith("+"):
                match = ROW.match(line[1:])
                if match:
                    added[match.group(3).strip()] = match.group(2).strip()
            elif line.startswith("-"):
                match = ROW.match(line[1:])
                if match:
                    removed[match.group(3).strip()] = match.group(2).strip()
        for pgn, name in added.items():
            if pgn in removed and removed[pgn] != name:
                renames.append({**commit, "pgn": pgn,
                                "from": removed[pgn], "to": name})
            elif pgn not in named:
                named[pgn] = {**commit, "name": name}
    return named, renames


def substantive(before: str, after: str) -> bool:
    """Is this a naming decision, or a diacritic and a comma?"""
    plain = lambda text: re.sub(r"[^a-z0-9]", "", text.lower())  # noqa: E731
    if plain(before) == plain(after):
        return False
    return difflib.SequenceMatcher(None, before, after).ratio() < SUBSTANTIVE_BELOW


def catalogue_by_position(path: Path) -> dict[str, dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return {r["moves_uci"].strip(): r for r in csv.DictReader(handle)
                if r["moves_uci"].strip()}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--repo", type=Path, required=True,
                        help="clone of lichess-org/chess-openings")
    parser.add_argument("--catalogue", type=Path, default=DEFAULT_CATALOGUE)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args(sys.argv[1:] if argv is None else argv)

    if not (args.repo / ".git").is_dir():
        print(f"ERROR: not a git clone: {args.repo}", file=sys.stderr)
        return 1

    named, renames = events(history(args.repo))
    print(f"positions first named  {len(named):6d}")
    print(f"rename events          {len(renames):6d}")

    catalogue = catalogue_by_position(args.catalogue)
    rows: list[dict[str, str]] = []
    seen: set[tuple[str, str, str]] = set()
    unconvertible = trivial = 0

    for event in renames:
        try:
            moves = uci_sequence_from_pgn(event["pgn"])
        except Exception:
            unconvertible += 1
            continue
        row = catalogue.get(moves)
        if row is None:
            continue
        if not substantive(event["from"], event["to"]):
            trivial += 1
            continue
        key = (row["ocn1"], event["from"], event["to"])
        if key in seen:
            continue
        seen.add(key)
        rows.append({
            "ocn1": row["ocn1"], "canonical_name": row["canonical_name"],
            "relation": "renamed", "renamed_from": event["from"],
            "renamed_to": event["to"], "date": event["date"],
            "author": event["author"], "commit": event["sha"],
            "commit_subject": event["subject"][:160].replace("\t", " "),
            "source_ref": COMMIT_URL.format(sha=event["sha"]),
            #: A commit is a primary record of the decision it made, but
            #: it records the decision and not the scholarship behind it.
            "evidence_grade": "attested",
        })

    rows.sort(key=lambda r: (r["date"], r["ocn1"]))
    print(f"\nlanding on an OCN row  {len(rows) + trivial:6d}")
    print(f"  substantive renames  {len(rows):6d}")
    print(f"  punctuation or typo  {trivial:6d}")
    print(f"  unconvertible pgn    {unconvertible:6d}")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        with args.out.open("w", encoding="utf-8", newline="") as handle:
            handle.write("\t".join(COLUMNS) + "\n")
            for row in rows:
                handle.write("\t".join(row[c] for c in COLUMNS) + "\n")
        print(f"\nwrote {args.out}")

    print("\nNOTE: `renamed` is not yet in the chronicle design's closed "
          "relation set. Adding it is a design decision, not this tool's.")
    print("evidence only: no catalogue row, no claims row")
    return 0


if __name__ == "__main__":
    sys.exit(main())
