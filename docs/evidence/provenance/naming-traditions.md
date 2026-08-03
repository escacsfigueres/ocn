# Two traditions, one position: the case for a naming-tradition relation

**Status: proposal, nothing applied.** Written 2026-08-04 from a question
Albert asked about the Modern and the Robatsch.

## The catalogue contradicts itself in four places

1.e4 g6 is the **Modern Defence** in English-language literature and the
**Robatsch Defence** in the continental tradition, after the Austrian
grandmaster Karl Robatsch. OCN records that as follows:

| where | what it says |
|---|---|
| `B.Mod`, B06, 1.e4 g6, **96 lines beneath it** | canonical name `Modern Defence`; the only alias is `Modern Defense`, the American spelling. **`Robatsch` does not appear.** No attribution. |
| `A.Mod`, A42, the setup against 1.d4 | canonical `Modern Defence against d4`; alias **`Robatsch Defence`**; note "Modern/Robatsch setup against queen-pawn openings". No attribution. |
| `docs/evidence/provenance/people-proposed-additions.tsv` | `robatsch → Robatsch, Karl`, note: **"eponym of Modern Defence, Standard Setup"** |
| `docs/companion-attributions-dry-run.md`, quoting Hooper & Whyld | "Robatsch merely popularised a line known since the sixteenth century" |

So the alias points at the queen-pawn row, the person record points at the
Modern Defence, the row with ninety-six descendants points at nothing, and the
one sourced sentence we hold about the man is filed in a dry-run report. Every
one of those four artefacts was produced by a different pass, and no two of
them agree.

## Why the alias column cannot fix it

The obvious repair is to add `Robatsch Defence` to `B.Mod`'s aliases. That
would make the catalogue findable and would still be wrong, for three reasons.

**An alias is directional.** The column exists to say "this string also denotes
this row", with the canonical name above and the rest below. `Modern Defense`
belongs there: it is the same name, spelled for a different market. `Robatsch
Defence` is not a lesser spelling of `Modern Defence`. It is what a whole body
of literature calls the thing, and demoting it encodes one tradition as the
truth and the other as a variant.

**An alias carries no evidence.** It is a bare string in a pipe-delimited
column: no source, no date, no person, no place. We hold a person record for
Karl Robatsch and a sourced sentence about what he did, and neither can attach
to an alias. Everything else in this catalogue that asserts something carries
its evidence with it; the alias column is the one place where a claim is made
and nothing backs it.

**An alias deletes the interesting fact.** That two communities give the same
position different names, and when, and on whose authority, is precisely what a
catalogue of names is for. Flattening it into a synonym list throws away the
only part worth recording.

## The proposed relation

`catalog/ocn-1.claims.tsv` already has the right shape —
`ocn1, relation, subject_type, subject_id, date, games, source_ref,
evidence_grade, note` — and this fits it:

- `ocn1` = `B.Mod`
- `relation` = `known-as-in-tradition`
- `subject_type` = `name`, `subject_id` = `Robatsch Defence`
- `date` = earliest attestation of the name in that tradition
- `source_ref` = the citation that establishes it
- `evidence_grade` = as everywhere else

**The open design question, and it is not free.** There is no column for the
tradition itself. Either `claims.tsv` grows one, which touches every consumer
of the file and the published packages, or the tradition is encoded inside
`subject_id`, which puts structure in a string and will be regretted. That
choice is Albert's and it is the whole cost of the proposal; the rest is
already built.

## Why this matters beyond one opening

`B.Mod` is not an anomaly, it is the visible case. **109 of the Ruy López's 328
lines carry no alternative name at all; across the catalogue it is 2,144 of
5,899.** The Ruy López monograph argues that this is OCN's most consequential
weakness, worse than being wrong, because a reader who searches the name their
own source uses does not find us. The named examples there are the same
phenomenon as the Robatsch: a 2026 course teaches a line as the **Modern
Archangel** and a recent book teaches another as the **Neo-Møller**, and
neither string is anywhere in the catalogue.

A tradition relation closes that gap **without OCN having to pick winners**,
which is the only way it can honestly be closed. It also gives the letter to
chessgames.com a question their community can actually answer: not "is our name
right" but "what do you call this, and since when".

## There is no policy, and that is the actual finding

Section C of the decisions sheet had already parked **48 `named-after-person`
claims** for being "the eponym of a different name for the same opening", and
named five pairs. Checking what the catalogue does with each of them turns up
four different answers to one question:

| pair | what OCN does |
|---|---|
| Pirc / **Ufimtsev** | the second name appears on **no row at all**, anywhere in 5,899 |
| Modern / **Robatsch** | the second name sits on a **neighbouring row**, `A.Mod`, not on `B.Mod` |
| **Richter**-Veresov | both names **compounded into one canonical name**, `A.Ver` |
| Van Geet / **Dunst** | both on the **same row**, one demoted to an alias |
| Sodium / **Durkin** | the eponym is a **child row**, `A.Sod.Dur`, under a descriptive parent |

Five instances of one phenomenon, four incompatible treatments, and a fifth
name simply missing. No pass did anything wrong; there was nothing to be
consistent with. That is what a relation buys — not a better place to put
Robatsch, but the first answer to the question that applies to all of them.

It also puts a number on the proposal: those **48 parked claims** are true
statements the catalogue currently cannot make, and this is the relation that
would let it make them.

## Two neighbouring problems, found while checking, that this does not solve

Stated separately so the proposal is not credited with more than it does.

**Five aliases are another row's canonical name.** `Lion Defence`, `London
System` (twice), `Richter-Veresov Attack` and `Colle System` each appear as an
alias on one row and as the name of another. That is not two traditions naming
one position; it is one name reaching two positions by different move orders,
and it wants transposition machinery, not this.

**A person split out of a compound surname.** The proposed people file carries
`lopez → López, Juan`, "eponym of English King's English, Bellon Gambit". There
is no Juan López. The row's own `attributed_to` reads **Juan Manuel Bellón
López (populariser)**, and a splitter took the last word of a Spanish compound
surname for a person. This is the fourth place tonight where a surname was
treated as an identity; see
[[ocn-person-identity-is-qid-not-surname]] and
`wch-participant-integrity.md`.
