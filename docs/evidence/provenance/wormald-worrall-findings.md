# Wormald and Worrall: an attribution on the wrong row

**Status: applied 2026-08-03.** Companion to
`docs/manifests/wormald-worrall-retraction.manifest.json`. Found 2026-08-03
while building the Ruy López monograph.

## What is wrong

Two lines in the Ruy López carry near-identical names for two different
nineteenth-century players:

| slug | moves | catalogue name | ECO |
|---|---|---|---|
| `C.RyL.Mor.Wor` | 1.e4 e5 2.Nf3 Nc6 3.Bb5 a6 4.Ba4 Nf6 **5.Qe2** | Ruy López Morphy, **Wormald** Attack | C77 |
| `C.RyL.Mor.Ba4.Nf6.O-O.Wor` | … 5.O-O Be7 **6.Qe2** | Ruy López, Closed, **Worrall** Attack | C86 |

The first row carries this attribution:

> Thomas Herbert Worrall (originator)
> Hooper & Whyld, 'The Oxford Companion to Chess' (2nd ed., OUP 1992),
> entry 'Worrall Attack': "Worrall Attack. 757 in the SPANISH OPENING,
> first played in the 1840s. Thomas Herbert Worrall (1807-78), subsequently
> appointed British Commissioner in Mexico, was afterwards transferred to
> New York."

The Companion entry is about the **Worrall Attack**, which is the second
row. It was attached to the first, which is the **Wormald** Attack, named
for Robert Wormald. The two slugs share the fragment `Wor`, and that is
almost certainly how the pass matched them.

The second row, the one the entry actually describes, carries no
attribution at all.

## Why retract rather than move it

Moving the attribution to the correct row would be the obvious repair, and
it is the wrong one. The Companion entry establishes that a line is called
the Worrall Attack and that a man called Worrall existed; it does not say
what he did with the move. `attributed_to` records a person **and a role**,
and this catalogue does not put an eponym in a field that demands a role —
that rule is why 19 other Ruy López proposals are held back unapplied.

So the attribution is retracted and the row keeps a note saying what
happened. The correct place for "this line is called after Worrall" is a
`named-after-person` claim, which is exactly the relation that exists for
it, and the 19 pending proposals are the batch it belongs to.

## Why not simply leave it and print the admission

Four independent reviewers said the same thing on 2026-08-03, and they were
right: a known, diagnosed, fixable error left standing with an apology
attached is not honesty. Under CC-BY it also propagates to redistributors
the errata will never reach. Publishing the retraction is the stronger
demonstration of the grading discipline, because it shows the rule doing
its work rather than being described.

## The open question

The earliest printed use of each name, and for which move order, remains
unanswered. It is put to readers in the monograph's open questions, where
it is worth more than a guess would have been.

## What the same error had also produced

The substring match on `Wor` had left three artefacts, not one. Two were in
proposal files and were corrected alongside the retraction:

- `named-after-person.proposed.tsv` proposed `worrall` for `C.RyL.Mor.Wor`,
  justifying itself with "catalogue name 'Ruy López Morphy, **Wormald**
  Attack' carries this person's name" — which names the wrong man in its own
  sentence. Retargeted to `C.RyL.Mor.Ba4.Nf6.O-O.Wor`, the row the Companion
  entry actually describes.
- `people-proposed-additions.tsv` justified the `worrall` person record as
  "eponym of Ruy López Morphy, Wormald Attack". Corrected to name the Worrall
  Attack.

`C.RyL.Mor.Wor` is therefore left with no proposal at all. A
`named-after-person` claim for Robert Wormald would be correct and needs a
person record that does not yet exist; that is open.

## Applied record

`--validate` and `--dry-run --strict` both exit 0; applied with
`--apply --validate --strict`, 5,899 rows before and after, 1 row changed,
`attributed_to`: `'Thomas Herbert Worrall (originator)'` to `''`. Sidecars
regenerated (`attribution.tsv` loses one row, `name_basis.tsv` one changed),
package copies synced, and all five CI checks exit 0.
