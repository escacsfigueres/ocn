# Who made a line theirs: a design, and why the obvious signal is wrong

**Status: design, not built.** Blocked on a Lichess API token; the
method is specified here so it can run the moment one is available.

## The question

Openings acquire people who are not their inventors. Vaisser was the
first to play the Sveshnikov at a high level; Kramnik, Dubov and Carlsen
later made it theirs, Carlsen to the point of using it as a regular
weapon in the 2018 world championship. The London System runs Kamsky,
then Kramnik, then Carlsen. Avrukh did not popularise the Catalan by
playing it; he wrote the book that everyone else uses.

None of that is `invented-by`, and lumping it under a single
`popularised-by` loses what makes it interesting. **The chronology is
the content.** Without it Vaisser does not register at all — he is not a
top-ten player and never was, and his claim rests entirely on being
early.

## The obvious signal is the rating list, measured

`catalog/ocn-1.popularity.tsv` carries a `top_player` per opening, and
it is tempting to read it as "the player associated with this line". It
is not. The six players holding the most rows are exactly the six with
the highest peak rating in the data:

| player | rows | peak Elo in data |
|---|---:|---:|
| Carlsen | 1,629 | 2882 |
| Kasparov | 250 | 2851 |
| Caruana | 218 | 2844 |
| Aronian | 147 | 2830 |
| Nakamura | 126 | 2816 |
| Anand | 123 | 2817 |

The column records the highest-rated player who appears in the
explorer's top games for a position. Carlsen holds 1,629 openings
because he is the highest-rated player in the database, not because
those lines are his. Building an association relation on it would
produce a table that says Carlsen owns a third of chess.

The stored year range fails the same way: `B.Sic.Sve` reads 2018–2018,
because those are the years of the *highest-rated* games, which are
Carlsen's championship ones. The Sveshnikov dates from the 1970s.

Two spelling defects also have to be fixed before any of this is
joined: 125 of 853 surnames appear under more than one spelling, and
`Carlsen` conflates Magnus with Torben Erik — the same failure the
chronicle's people table had, from the same cause.

## Three relations, not one

| relation | what it says | evidence |
|---|---|---|
| `first-elite-adopter` | earliest master-level games in this line, and by whom | earliest window in which the position appears at all |
| `popularised-by` | took it up later and made it associated with them | a share of the line's games far above that player's base rate, dated |
| `analysed-in` | contributed to the line through literature rather than play | a published monograph, cited by author, title, publisher, year |

The third is the one no game database can see. Avrukh, Kotronias and
Gawain Jones belong to their openings through books, and that
attachment is a bibliographic fact — verifiable from a catalogue record
without owning the book, which also keeps it clear of the
commercial-source gate: what is cited is that the work exists and what
it covers, never its contents.

## How to collect the first two

The Lichess masters explorer accepts `since` and `until`. Querying one
position across successive windows gives the shape of its adoption:

    GET https://explorer.lichess.ovh/masters?fen=…&since=1980&until=1989&topGames=8

- **First adopter**: walk windows forward from the earliest until the
  position first returns games; the players in that window are the
  candidates.
- **Popularisers**: a player's share of a line's games against their
  share of all master games in the same window. Lift, not count —
  otherwise the answer is Carlsen everywhere, for the same reason as
  above.

Cost: roughly six windows per opening. Restricted to lines carrying a
person's name, or to those with enough master games to be worth asking
about, this is a few thousand requests rather than the 11,000 the
popularity run made.

**Requires `LICHESS_TOKEN`.** The explorer returns 401 without one, as
`tools/build_popularity.py` documents.

## Grades

`first-elite-adopter` and `popularised-by` derived this way are
`attested`: the games are public and each claim names one, but "first"
is only ever first *in this database*, and that limit must be stated in
the note rather than hidden by the grade.

`analysed-in` from a catalogue record is `attested` too — the book's
existence is verifiable, its influence is not.

## What this is not

A measure of who played a line *best*, or of who deserves credit. It
records who was early and who was associated, both of which are facts,
and leaves the judgement out.
