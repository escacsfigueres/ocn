# Where modern opening names come from: Lichess's git history

**Status: evidence gathered, nothing applied.** 263 substantive renaming
events affecting catalogue rows, each with a date, a named author and a
public commit URL, in
[`evidence/provenance/lichess-renames.tsv`](evidence/provenance/lichess-renames.tsv).

## The gap this fills

The Oxford Companion is dated 1992 and is silent on every name coined
since. For those the usual answer is that nobody knows who named them —
and for a large part of the vocabulary in daily use, that is simply
false. Somebody does, and it is written down in public.

Lichess names openings from `lichess-org/chess-openings`, a repository
maintained by pull request: 876 commits, 51 contributors, February 2016
to July 2026. Every name in it was added or changed by a person, on a
date, in a commit that frequently says why. That is a citable public
record of exactly the kind the chronicle design asks for, and no other
open chess dataset carries it.

It is also the answer to a question worth stating plainly: **there is no
naming authority.** FIDE tried in 1932 and 1965 and was ignored. ECO is
a publisher's classification, not a registry. So for a modern name, the
commit that introduced it into the database everyone reads is not merely
evidence of the name — it is frequently the origin of the name's
currency.

## Two kinds of event, and only one is interesting

**First naming** — the commit where a position first acquired any name.
14,321 of them, and almost all land in two bulk imports (2019 and 2021)
that say nothing beyond "this came from the initial data". Reported, not
claimed.

**Rename** — a commit that changed the name of a position it already
named. 1,114 of them, 361 landing on a catalogue row. These are
editorial decisions with an author and a date.

Filtering matters as much as finding. 98 of the 361 are a restored
diacritic or a missing comma, and calling those naming decisions would
bury the ones that are under the ones that are not.

## What the 263 contain

| when | row | from | to |
|---|---|---|---|
| 2024-06-12 | `C.Pet` and four children | Russian Game | **Petrov's Defense** |
| 2022-07-14 | `C.KGm.Acc.MKe` | Van Geet Opening: Nowokunski Gambit | **King's Gambit Accepted: Mason-Keres Gambit** |
| 2022-12-11 | `A.QPO.Nf6.Nc3.d5.e4` | Blackmar-Diemer Gambit | **Queen's Pawn Game: Hübsch Gambit** |
| 2022-10-12 | `A.QPO.Nf6.g4` | Bronstein Gambit | **Indian Defense: Gibbins-Weidenhagen Gambit** |
| 2022-08-26 | `C.Ita.Nd4` | Italian Game: Schilling-Kostic Gambit | **Italian Game: Blackburne-Kostić Gambit** |
| 2022-05-28 | `B.Nim.Col` | Nimzowitsch Defense: Lean Variation | **Nimzowitsch Defense: Colorado Countergambit** |
| 2022-06-26 | `D.Bgm` | Blackmar Gambit | **Blackmar-Diemer Gambit** |

Several are attribution changes rather than cosmetic ones — the
Schilling-Kostić line was reassigned to Blackburne, the Bronstein Gambit
to Gibbins and Weidenhagen. And the last is a reversal: the same
position had gone the other way in January 2020, so the repository
records the naming being argued both ways with two years between.

## The join, and what it drops

By position, never by name: Lichess stores a SAN move sequence, which is
converted and matched against `moves_uci`. 701 rename events carried a
sequence our converter could not read and were dropped rather than
guessed at — those are worth a look, because a systematic conversion
failure would be a defect on our side, as one already turned out to be.

## What this is not

A commit is a primary record of the decision it made. It is not evidence
that the decision was right, and it says nothing about who first used
the name away from this repository. So every row is `attested`: the
naming event is documented, the naming history behind it is not.

## What needs a decision

`renamed` is **not in the closed relation set** in
[`chronicle-layer-design.md`](chronicle-layer-design.md), though
[`treatise-school-findings.md`](treatise-school-findings.md) already
called the Latvian Gambit's renaming "the first candidate for a
`renamed` relation". Admitting it to the set is a design decision, and
these 263 rows plus the Latvian are the case for making it.
