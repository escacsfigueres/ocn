# Dating a name instead of a move

**Status: verified, un-applied.** Companion to
`printed-name-attestations.proposed.tsv`. Built 2026-08-03 while assembling
the Ruy López monograph.

## What this is for

Every date the catalogue currently holds is the date of a *game*. A game
proves when a move was played and says nothing about when anybody called
the move anything. For a catalogue whose subject is names, that is the
wrong measurement, and it is the reason the monograph has to print the
warning that its dates are floors.

A title page is a different kind of evidence. A book called *Ruy Lopez,
Breyer system*, printed in 1976, establishes that the name was in
circulation by 1976. It is weaker than a first attestation — an earlier use
almost certainly exists — but it is evidence of the right kind, and the
catalogue held none of it.

## Method

All 328 Ruy López lines were queried against Open Library's public search
API by the distinctive part of each canonical name, then filtered:

| stage | records |
|---|---|
| returned by Open Library | 234 |
| a book about a line, not about a person or an event | 52 |
| after removing books whose subject is a rival opening | 32 |
| after requiring the opening be named wherever a name is shared | 16 |

The last filter is the one that matters and it comes straight from
[[ocn-person-identity-is-qid-not-surname]]: the same word names lines in
different openings. This catalogue holds a Panov System and a Rossolimo
Defence under the Chigorin, while a book titled *Panov Attack* is about the
Caro-Kann and one titled *Rossolimo's Opening* is about the Sicilian. A
title cannot say which is meant, so a name that appears in any canonical
name outside `C.RyL` was accepted only when the title also named the Ruy
López or the Spanish. The rival list is derived from the catalogue itself
rather than hand-written.

Those sixteen books name nine slugs between them, and two titles name a
line this opening holds twice under different parents. Resolving those by
what each title actually says leaves **seven lines**. Every stage above is
code; the last step is a judgement, recorded as one in the `note` column
rather than folded into the filter.

Scripts are in the monograph workspace, not in the repository: they are a
one-off harvest against a third-party API, not a maintained tool.

## Result

Seven of 328, which is two per cent. The shortfall is a finding rather than
a failure. Most opening books are titled for the opening and not the line —
the shelf is full of volumes called *The Ruy Lopez* that treat forty of
these names inside and announce none of them on the cover. Open Library
indexes titles, so a book that discusses the Breyer for thirty pages under
a general title is invisible to this method, and no amount of filter work
recovers it.

What would populate this properly is the survey literature, where every
*Informant* and *New in Chess Yearbook* article names its line explicitly,
and the publishers' and course catalogues. None of that is open data. It is
also exactly the kind of thing a reading community knows offhand and no
index holds, which is why the monograph puts the question to its readers
instead of answering it.

## Proposed relation

No schema change is needed. `catalog/ocn-1.claims.tsv` already carries
`ocn1, relation, subject_type, subject_id, date, games, source_ref,
evidence_grade, note`. The proposal adds one relation value and one
subject type:

- `relation` = `attested-in-print`
- `subject_type` = `work`, `subject_id` = the Open Library work identifier

`date` is the year of publication, `games` is empty, `source_ref` is the
full citation, `evidence_grade` is `attested`. Open Library identifiers are
stable, resolvable and open, which is why they are preferred here over
ISBNs.

**Held for a decision.** The relation name asserts something specific — that
the work attests the *name*, not that it is *about* the line — and the
distinction is the reason the claim is worth having at all. That is Albert's
call, and until it is made the seven rows sit in the proposed TSV.

## Why this is worth seven rows

Because it is the only evidence in the catalogue that dates a name rather
than a position, and because it is the one gap a reader can close for us.
See [[evidence-sustains-less-than-triage]]: the discipline is to assert what
the source proves and no more, and a title page proves a year.
