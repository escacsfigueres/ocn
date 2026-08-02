# Evidence backlog — triage of what is collected but not applied

Result of a pass over every gathered-but-unconverted evidence file in
`docs/evidence/`. **Nothing was applied to the catalogue.** Each source is
recorded with what it actually supports, which is not always what its own
columns claim.

## The pattern worth knowing before reading the rest

Every file's triage columns assert more than its own evidence sustains. This is
the single recurring finding, and it explains why `attributed_to` sits at 1.2%
after months of collection: the evidence largely proves **eponyms**, while the
field demands **roles**. Each source must be converted to the claim type it can
carry, not to the field that happens to be empty.

## 1. `eponyms/companion-verdicts.tsv` — 52 ready

208 rows. Funnel: 115 have an Oxford Companion entry, 70 of those have no
`attributed_to` yet, 63 state a definite role.

Of those 63, **11 do not survive their own quote**:

- 9 where the entry names the person only as the opening's eponym and says
  nothing about what they did (`"Kevitz Defence, 42 in the ENGLISH OPENING."`)
- 2 where the entry credits someone else, or names the person as the one the
  opening was named *after* (From's Gambit is "first given by GRECO")

→ `docs/manifests/companion-attributions-round2.manifest.json`, 52 changes,
`--validate` clean, `--strict` dry-run clean, 5899 rows unchanged.
Excluded rows are in the `.review.json` / `.parked.json` sidecars with a reason
each. **Pending GO.**

Note: `B.CaK` (Caro-Kann, 82.8M games, no attribution) lands in PARKED. The
Companion entry establishes only the eponym, so this source cannot fill that gap.

## 2. `eponyms/named-after-people.tsv` — 240 claims proposed

228 rows, **no `role` column**, 202 of 228 citations are Wikipedia `<ref>`
blobs pointing at chessgames.com / chess.com / 365chess.com. Supports the
eponym, not a role. Belongs in `named-after-person`, which is already in the
chronicle's closed relation set and has zero rows.

→ `provenance/named-after-person.proposed.tsv` (240 claims, 224 slugs) and
`provenance/people-proposed-additions.tsv` (182 entities). Findings and the
four identity rulings are in `provenance/named-after-person-findings.md`,
including two wrong forenames in the released `catalog/ocn-1.people.tsv`
(`karpov`, `smyslov`) and the fact that all 61 person entities are orphans.

## 3. `eponyms/named-after-places.tsv` — done, nothing to add

186 rows → 119 claims, already applied. The gate was **"the catalogue's own
name carries the place"**, which is self-evidencing and independent of
Wikipedia's frequently absent sourcing — a sound rule, and the reason
`source_tier: none` rows were still acceptable.

The two rows that carry a place name but were excluded are correctly excluded:
"Amazon Attack" is the fairy piece, "Kahiko-Hula" is a dance form. Neither is a
place. Two cosmetic defects in the source file, neither costing anything:
one row has a UCI sequence in its `source_tier` column (`E.KID.Cls.Oth.Na6`),
and five slugs appear twice because they carry two place names each
(`D.Sla` is both Czech and Slav).

## 4. `eponyms/companion-sublines.tsv` — absorbed, nothing to add

33 rows: 21 already covered by a prior manifest, 10 already attributed, 1 with
an unmappable role, and 1 (`C.RyL.Coz`) that fails quote verification for the
same reason it failed in source 1 — the clause says "first given by CARRERA"
and names Cozio only as the eponym.

## 5. `provenance/notable-games.tsv` — recommend a sidecar, not claims

The best-quality evidence in the backlog: 19,860 games over 5,196 slugs, 1964–2026,
**100% with Elo on both sides and 100% with a permanent lichess.org URL**, capped
at four games per opening. 4,372 slugs would gain history.

**But no relation in the closed set fits it honestly.** `key-game` reads as
"the game that fixed the name" — these were selected by Elo and fixed no names.
`played-by` reads as "it is in this player's repertoire" — two to four games do
not establish a repertoire. Forcing either would put 19,860 false claims into a
layer whose subject is naming history.

Recommendation: land it as its own sidecar, `catalog/ocn-1.games.tsv`, sibling
to `ocn-1.popularity.tsv`. It gives every opening page four exemplar games with
permanent links, it is honest about being an Elo-ranked roster rather than a
naming fact, and it keeps the chronicle about names. This is a decision, not a
conversion, and it is Albert's.
