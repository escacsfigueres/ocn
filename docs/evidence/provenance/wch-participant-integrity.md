# Who actually played in the world-championship claims

**Status: applied 2026-08-03.** Companion to
`wch-participant-integrity.proposed.tsv`. Found 2026-08-03 while checking a
single suspicious name printed in the Ruy López monograph.

## How it started

The monograph printed the earliest game on one line as *Gaprindashvili, Nona
v Kushnir Aleksandr, Wch women Riga LAT, 1965*. The 1965, 1969 and 1972
women's title matches were played against **Alla** Kushnir. The catalogue
holds both `Kushnir, Alla` and `Kushnir Aleksandr` — the second with no
comma, a masculine given name, and 26 rows inside the women's championship.

That is the same defect the Wormald retraction just closed: a surname treated
as an identity.

And it was already known. The Wikidata resolution pass of 2026-07-31 found
exactly these people — `alekhine`/`aljechin`, `bykova`/`bikova` and
`marshall`/`marshall-viele` resolving to one human each, and wrong forenames
shipped for Karpov and Smyslov. That pass corrected `people.tsv`. **Nobody
went back to the game records**, so the same wrong names are still sitting in
the chronicle's most-cited file, and the monograph printed one of them.

## The test

No outside knowledge is needed. **A title match is two players**, so inside
one event the participant pair should be constant. Every row whose pair
differs from its event's modal pair is suspect, and the suspects then split
by a second question: does the row share *both surnames* with the modal pair?

- Both surnames present: the same match, with one player spelled two ways.
- A surname missing: a different game, filed here because a surname matched.

## What it found

`catalog/ocn-1.wch.tsv` holds **1,040 rows over 85 events**. 988 agree with
their own event's participant pair. **52 do not**, and they are not one
problem:

| | rows |
|---|---|
| the same match, one player spelled two ways | 42 |
| a different game filed into a championship match | 10 |

Of those 10, seven are genuinely foreign games — two Spanish amateurs filed
into Steinitz–Zukertort 1886, three games into Alekhine–Capablanca 1927,
`Botvinnik, Alexander v Al Tal, Ammar` filed into Botvinnik–Tal 1961, and
`Hanvitha Koneru` filed into Hou Yifan's 2011 defence against **Humpy**
Koneru.

**Three of the ten are the correctly spelled rows.** They were flagged
because the majority spelling in their event is the wrong one: the two rows
reading `Bogoljubow, Efim v Alekhine, Alexander` are right and the twenty-one
reading `Aljechin, Yuri` are wrong; the one row reading `Kushnir, Alla` is
right and the twenty-six reading `Kushnir Aleksandr` are wrong. A modal vote
is a consistency check and not a truth procedure, and this file is a clean
demonstration of the difference.

## What the test cannot see

Where **every** row of an event carries the wrong name there is no minority
to flag. The 6th championship of 1907 was Emanuel Lasker against Frank James
Marshall; all fifteen rows name `Marshall Viele, Fabrizio Aaron`, and the
consistency test passes them without comment. It took the July resolution
file, not this test, to know that. Any similar case elsewhere in
the file is equally invisible to this method, so the renames proposed here
are a floor and not a complete list.

Forty-nine rows name the player `?`, in women's championships between 1975
and 1988. They are not errors, they are absences, and nothing here fixes
them.

## Effect on the monograph

Small, and worth stating because the volume is public. Of the **155**
Ruy López rows exactly **one** is foreign — the 1886 intruder. The six other
1886 Ruy López rows are genuinely Steinitz against Zukertort, so the
volume's claim that the world-championship record runs from 1886 stands.

## What is proposed

The sibling TSV, un-applied, in three parts:

- **drop**, 7 rows: games by people who did not play the match they are filed
  under. Each is evidenced by the file itself.
- **rename**, 13 spellings covering **334 rows**, of which **12 carry a
  Wikidata identity** taken from `docs/evidence/people/wikidata-resolved.tsv`.
  Each therefore points at a person and not at a preferred spelling, which is
  the whole argument of that pass. Two of them change a form the file uses
  everywhere: the resolved name is `Spassky, Boris`, and the file holds only
  `Spassky, Boris V.` and `Spassky, Boris Vasily`; the resolved name is
  `Bykova, Elisaveta`, and the file holds `Bikova, E.` and `Bykova,
  Elizaveta`. In both cases the catalogue is wrong twice over and the
  consistency test could only see it because it was wrong in two different
  ways.
- **unresolved**, the 49 rows naming `?`. Alla Kushnir turned out to have a
  record after all — resolved to Q269098 with her dates on 31 July — filed
  under the slug `kushnir-aleksandr`, built from the misspelling. The identity
  work had been right and only the handle carried the error.

## Two couplings that made this more than a two-column rename

`tools/apply_sidecar_manifest.py` now exists, with twenty tests, and all four
chronicle sidecars round-trip through it byte for byte. The manifest at
`docs/manifests/wch-participant-integrity.manifest.json` dry-runs clean:
1,040 rows to 1,033, every operation matching its declared count exactly.
It was **not enough to apply on its own**, for two reasons found while
checking, and both are now handled.

**The names are in the citation column as well.** Every row of `wch.tsv`
carries `citation` in the form `White-Black, Event, Place, Year`, so the
Aljechin row reads `Aljechin, Yuri-Bogoljubow, World Championship 14th,
Deutschland/Niederlande, 1929`. Correcting `white` and `black` and leaving
`citation` would fix the display and leave the evidence wrong.

Substring replacement cannot do this safely, and no boundary rule saves it:
the corrected `Bogoljubow, Efim` *contains* `Bogoljubow,`, so any rule that
matches the wrong rows matches the right ones too. The engine gained a
`sync_prefix` operation instead, anchored rather than searched — it rebuilds
the citation's opening from the row's own corrected pair, having first checked
that the citation begins with the pair it used to carry. That holds on all
1,040 rows, and the operation refuses to run if it ever stops holding.

**Regenerating the chronicle would destroy the identity work.**
`tools/build_chronicle.py` derives `people.tsv`, `events.tsv` and
`claims.tsv` from `wch.tsv`, and `source_ref` is a verbatim copy of
`citation`. Regenerating is therefore the way to propagate this fix to the 733 wch-game
claims, and it is also a trap twice over. It writes `people.tsv` with
`wikidata_qid` empty by design, which would have erased the **60 curated
identities** resolved on 2026-07-31. And its `claims.tsv` holds *only* the
wch-game relation, so copying it would have deleted the 259 `renamed` and 119
`named-after-place` claims built by other passes.

What was done instead: regenerate into a scratch directory, take `events.tsv`
whole because it is entirely derived, splice the regenerated wch-game block
into the existing `claims.tsv` keeping the other 378 claims in place, and
leave `people.tsv` alone.

## What the rename then forced

Renaming the participants renamed the event identifiers derived from them, and
that broke the chronicle's own joins: `events.tsv` began naming `kushnir` and
`marshall`, which `people.tsv` did not hold, while `aljechin`, `bikova`,
`kushnir-aleksandr` and `marshall-viele` sat referenced by nothing. The July
pass had marked two of those pairs **merge pending** and the merge had never
happened; this forced it. Applied through the same engine
(`docs/manifests/people-identity-merge.manifest.json`): two duplicates dropped,
two slugs renamed onto the identity they already carried.

One thing the regeneration healed by itself. The 1929 match had been split
into two events, `wch-1929-alekhine-bogoljubow` with six games and
`wch-1929-aljechin-bogoljubow` with twenty-one, because one man was spelled two
ways. It is now one event with twenty-seven.

**After: 59 people, 59 referenced, nothing dangling in either direction, no
`merge pending` note left, and 58 of the 59 carrying a Wikidata identity.**

See [[attribution-working-pattern]]: automate the triage, never the truth.
