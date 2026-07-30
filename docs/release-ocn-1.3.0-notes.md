# OCN 1.3.0 — the chronicle layer: openings that carry their history

**Tag:** `ocn-1.3.0`. **Catalogue:** 5,899 rows, **zero slug changes
since 1.2.1** — anything keyed by `ocn1`, `fen_key` or zobrist survives
untouched. Every addition here is a new column value or a new sidecar.

## What changed

Most opening datasets answer *what is this line called*. This release is
the first instalment of a different question: **who is it named after,
and did they invent it?**

Usually they did not, and the catalogue now records which.

| | 1.2.1 | 1.3.0 |
|---|---:|---:|
| Rows with a sourced attribution | 26 | **71** |
| Chronicle claims | 733 | **1,111** |
| Relations in the claims table | 1 | **3** |
| Rows carrying any claim | 733 | **854** |
| Popularity sidecar | — | **5,894 rows** |

### Attributions now carry a role

`attributed_to` no longer says only *who*. It says what they did:
populariser, originator, advocate, first to publish, critic. That
distinction is the point — of the roles recorded, populariser outnumbers
originator three to one.

The clearest case is `C.Dam`, the Damiano Defence, filed as **critic**.
The Oxford Companion's entry reads: "a variation given by Lucena and
rightly condemned by Damiano as leading to a lost game." The opening
carries the name of the man who denounced it.

18 rows record a **rival claimant** in `historical_notes` where the
source names one, rather than quietly picking a winner.

### The claims table now has three entrances

`ocn-1.claims.tsv` is one table read from different sides, and this is
the release where that stops being aspirational:

- `wch-game` (733) — which openings decided world championships
- `named-after-place` (119) — where our own name carries a place
- `renamed` (259) — a line that used to be called something else

The renames come from the public git history of
`lichess-org/chess-openings`, where opening names are maintained by pull
request. 173 of them cite the pull request in which the change was
argued in public, by a named person, on a date. For a name coined after
1992 no reference work can supply that; the repository can.

### Popularity

`ocn-1.popularity.tsv` gives master and Lichess game counts per opening,
from the Lichess explorer API. 5,894 rows, no gaps.

## What we did not do

No claim is graded `verified`. That grade means somebody read the page,
and following a footnote to a book nobody opened is an error this
project has already had to retract once. Everything here is `attested`
or `traditional`, and the grade is on the row.

Rows the sources do not settle are left empty rather than filled
plausibly. Of 208 attribution candidates examined against the Oxford
Companion, 45 were applied and 163 held back.

## Compatibility

Zero slug changes. Zero structural column changes. `ocn-1.csv` keeps its
14 columns; everything new is additive, in sidecars keyed on `ocn1`.

Browse it at **[ocn.vercel.app](https://ocn.vercel.app)**.
