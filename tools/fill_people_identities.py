"""Fill `wikidata_qid`, `born`, `died` and corrected display names in
`catalog/ocn-1.people.tsv` from a verified identity proposal.

Deterministic and re-runnable: reads the current table and a proposal
table, writes the merged result. It does **not** rename `person_id` and
does not touch `events.tsv` or `claims.tsv`, so it cannot ripple. Rows
that resolve to the same QID are left in place and annotated, which makes
duplicates machine-detectable — the later merge then follows from recorded
identity rather than from a judgement call.

Editorial overrides live in DISPLAY_NAME_OVERRIDES, so a naming decision
is visible in the code that applies it rather than buried in the input.

Relation to `resolve_people.py`: that tool searches Wikidata itself and
fills only what survives its championship-year test, refusing the rest —
it is the automated resolver. This one applies a proposal a human has
adjudicated, including the rows the resolver rightly refuses because the
corpus spelling is corrupt (`Kushnir Aleksandr` is Alla Kushnir;
`Marshall Viele, Fabrizio Aaron` is Frank Marshall). The two were
cross-checked on 2026-08-02 and agreed on 57 of 61 rows with no
conflicting QID.

**Hazard both tools share:** `build_chronicle.py` regenerates this table
from the corpus with an empty `wikidata_qid`, and picks display names by
"longest spelling seen wins". Re-running it discards everything either
tool writes here, including the corrected names. Identity is not derivable
from a corpus, so the fix is not to re-run it blindly.

Usage:
    python3 tools/fill_people_identities.py --proposal <tsv> [--apply]
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PEOPLE = ROOT / "catalog" / "ocn-1.people.tsv"
FIELDS = ["person_id", "display_name", "wikidata_qid", "born", "died", "note"]

# Display names where the catalogue keeps its own convention against the
# proposal. Chess practice, not Wikidata label order, decides how a player
# is named here.
DISPLAY_NAME_OVERRIDES = {
    # FIDE, every broadcast and the player's own federation say "Gukesh D";
    # "Dommaraju, Gukesh" is Wikidata's label ordering, not chess usage.
    "gukesh-d": "Gukesh D",
}

UNVERIFIED = "seen in world championship games; identity unverified"


def load(path: Path) -> dict[str, dict]:
    with path.open(encoding="utf-8") as fh:
        return {r["person_id"]: r for r in csv.DictReader(fh, delimiter="\t")}


def build(current: dict[str, dict], proposal: dict[str, dict]) -> list[dict]:
    qid_owners: dict[str, list[str]] = {}
    for pid, row in proposal.items():
        qid = (row.get("wikidata_qid") or "").strip()
        if qid and pid in current:
            qid_owners.setdefault(qid, []).append(pid)

    out = []
    for pid, row in current.items():
        prop = proposal.get(pid)
        new = dict(row)
        if not prop:
            out.append(new)
            continue

        qid = (prop.get("wikidata_qid") or "").strip()
        new["wikidata_qid"] = qid
        new["born"] = (prop.get("born") or "").strip()
        new["died"] = (prop.get("died") or "").strip()
        new["display_name"] = DISPLAY_NAME_OVERRIDES.get(
            pid, (prop.get("display_name") or row["display_name"]).strip())

        note = row.get("note", "")
        if qid:
            note = note.replace(UNVERIFIED, "identity resolved").strip(" |")
            twins = [o for o in qid_owners.get(qid, []) if o != pid]
            if twins:
                note += (f"; duplicate identity: shares {qid} with "
                         f"{', '.join(sorted(twins))} — merge pending")
        else:
            note = (note + "; no Wikidata item found on a fresh search, "
                    "left null deliberately").strip(" |")
        new["note"] = note
        out.append(new)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--proposal", required=True, type=Path)
    ap.add_argument("--people", default=PEOPLE, type=Path)
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    current = load(args.people)
    proposal = load(args.proposal)
    rows = build(current, proposal)

    filled = sum(1 for r in rows if r["wikidata_qid"])
    renamed = sum(1 for r in rows
                  if r["display_name"] != current[r["person_id"]]["display_name"])
    dupes = sum(1 for r in rows if "duplicate identity" in r["note"])
    print(f"rows {len(rows)} | qid filled {filled} | names corrected {renamed} "
          f"| duplicate rows flagged {dupes}")
    for r in rows:
        was = current[r["person_id"]]["display_name"]
        if r["display_name"] != was:
            print(f"  {r['person_id']:<20} {was!r} -> {r['display_name']!r}")

    if not args.apply:
        print("\ndry run: nothing written")
        return 0

    with args.people.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS, delimiter="\t",
                           lineterminator="\n", extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    print(f"\nwrote {args.people}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
