# Filling the identity column: what was done and what was deliberately not

**Applied 2026-08-03.** Record for
`catalog/ocn-1.people.tsv`, filled by
`tools/fill_people_identities.py` from the verified proposal in the
external identity packet.

## Why identity first and the merge second

The packet proposed both filling the column and merging five duplicate
person rows in one pass. They were separated, and the order reversed.

Merging renames `person_id`, which is referenced by `events.tsv` (in the
`participants` field **and inside the event IDs themselves**, e.g.
`wch-1907-lasker-marshall-viele`) and by every `wch-game` claim whose
`subject_id` is such an event. That is a rippling change across three
tables and 50-plus rows, and it was a judgement call about who is whom.

Filling the identity column first turns it into a mechanical one. Two rows
that resolve to the same QID *are* the same human, by definition:

- `alekhine` and `aljechin` both carry `Q131374`
- `bikova` and `bykova` both carry `Q253772`

Both pairs are annotated in the `note` column with "duplicate identity:
shares Qnnn with X — merge pending", so the duplication is now
machine-detectable and the merge follows from recorded identity rather
than from an argument.

## What was applied

- **60 of 61 rows** carry a Wikidata QID with birth and death years.
- **16 display names corrected.** All were corpus artefacts, not
  editorial preferences: PGN middle initials (`Bronstein, David I`), tag
  corruption (`Hou, Yifan(HLJ)`), missing diacritics (`Capablanca, Jose` →
  `José Raúl`, `Forgacs, Leo` → `Forgács, Leó`), and three corrupted name
  strings that were not the person at all — `Kushnir Aleksandr` is **Alla
  Kushnir**, `Marshall Viele, Fabrizio Aaron` is **Frank Marshall**,
  `Bikova, E.` is Elisaveta Bykova.
- **One row left null on purpose.** `morrison` returned no Wikidata item
  on a fresh search; the note says so. A null here is a visible question,
  not a gap to be papered over.

## The one editorial override

`gukesh-d` stays **"Gukesh D"**, against the proposal's "Dommaraju,
Gukesh". Wikidata's label ordering is not chess practice: FIDE, every
broadcast and the player's own federation use Gukesh D. The override lives
in `DISPLAY_NAME_OVERRIDES` in the tool, so the decision is visible in the
code that applies it. If the catalogue ever adopts surname-first
universally, that should be a stated rule, not an import side-effect.

## Verification before applying

The proposal was cross-checked against the repository's own resolver,
`tools/resolve_people.py`, run in report mode. **57 of 61 rows agreed,
with zero conflicting QIDs.** The four differences were all rows where the
resolver refuses because the corpus spelling is corrupt and a search
returns nothing — which is that tool working as designed, and which
identifies precisely the rows a human had to adjudicate.

One value was spot-checked against the live item and the wider record
because it would be serious to get wrong: `timman`, died 2026. It is
correct — Jan Timman died on 18 February 2026, reported by FIDE and the
European Chess Union.

## Known hazard

`build_chronicle.py` regenerates this table from the corpus with an empty
`wikidata_qid`, and picks display names by "longest spelling seen wins".
Re-running it discards every identity and every corrected name here — it
would restore `Hou, Yifan(HLJ)` and `Kushnir Aleksandr`. The same exposure
applies to `resolve_people.py`. Identity is not derivable from a corpus,
so the answer is not to re-run the generator blindly over a table that now
holds human adjudications.

## Still open

- The five merges (three of which touch the catalogue: `aljechin`,
  `bikova`, `marshall-viele`; the other two exist only in the additions
  file).
- The 182-row additions file, which is a separate and larger editorial
  act, and which contains entities that are not people — Chess.com,
  Frankenstein's monster, Count Dracula.
- `greco` and `harrwitz` date divergences, left as they were.
