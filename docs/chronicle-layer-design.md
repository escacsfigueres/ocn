# The chronicle layer: people, places, events, and where names come from

**Status: design, not built.** Adopted 2026-07-30 as the shape of OCN's
cultural layer, the differentiator no other open chess dataset carries.
Sequenced after the announcement (roadmap H4.4); this document exists so
the design is settled before the work starts.

## What it is for

OCN today answers "what is this opening called and where does it sit in
the tree". The chronicle layer answers the questions people actually ask
about openings, in both directions:

- person to openings: what did Steinitz play?
- openings to person: who is this named after, who analysed it first?
- place to openings: what came out of Barcelona 1929?
- event to openings: which openings decided world championship matches?
- chronologically: what did the treatise era of the 1600s bequeath us?

Each of those is the same table read from a different side. That is the
whole architectural insight: **one claims table, many entrances.**

## The schema: three sidecars

Additive, like every other sidecar. `catalog/ocn-1.csv` is untouched.

### `ocn-1.people.tsv`
`person_id, display_name, wikidata_qid, born, died, note`

`wikidata_qid` is the load-bearing column: Steinitz is a public entity
with dates, spellings in every language and a stable identifier that is
not ours to get wrong. We reference; we do not re-litigate biography.

### `ocn-1.events.tsv`
`event_id, display_name, kind, place, year_start, year_end, wikidata_qid`

`kind` from a closed set: `tournament`, `match`, `wch_match`,
`candidates`, `olympiad`, `correspondence`, `publication`.
A treatise is an event of kind `publication` — that is how "Greco
analysed this in his manuscripts" becomes a row rather than prose.

### `ocn-1.claims.tsv` (the join)
`ocn1, relation, subject_type, subject_id, date, source_ref, evidence_grade, note`

`relation` from a closed set:

| relation | reads as |
|---|---|
| `named-after-person` | the opening carries this person's name |
| `named-after-place` | the name is a venue or region |
| `named-at-event` | the name was coined at this event |
| `invented-by` | first to conceive the idea |
| `analysed-in` | published analysis (subject is a `publication` event) |
| `popularised-by` | made it respected through practice |
| `key-game` | the game that fixed the name |
| `played-by` | it is in this player's repertoire |
| `wch-game` | played in a world championship match |
| `renamed` | the line carried a different name before this |
| `known-as` | a source gives this name for the same position |
| `attested-in-print` | this name was on a title page by this year |

`known-as` and `attested-in-print` were added on 2026-08-04, and the reason
is the same in both cases: the `aliases` column had been carrying claims it
cannot support.

An alias is a bare string in a pipe-delimited field. It has no source, no
date and no grade, and it is **directional** — one name is canonical and the
rest are beneath it. That is right for a spelling ("Modern Defense") and
wrong for a name a reference work treats as the head. The Oxford Companion's
entry for 1.e4 g6 2.d4 Bg7 is titled **Robatsch Defence** and gives the
Modern Defence as one of three alternatives; OCN files the position the other
way round. Recording that as an alias would encode one choice as the truth
and lose the only interesting part, which is that two authorities disagree.
`known-as` carries the name with the source that gives it and the grade it
earns, and says nothing about which one wins.

Where a source establishes *which* community uses a name, that belongs in the
note. The relation deliberately does **not** say "in tradition T", because
most sources say "also known as" and naming a tradition they do not name
would assert more than they support. If enough rows accumulate that do carry
a sourced tradition, a column is the next step and not before.

`attested-in-print` dates a **name**, which nothing else here can do. Every
other date in this catalogue is the date of a game, and a game proves when a
move was played, not when anybody called it anything. A book titled *Ruy
Lopez, Breyer system* and printed in 1976 puts the name in circulation by
1976. It is weaker than a first attestation and it is evidence of the right
kind. It is distinct from `analysed-in`, which asserts that a publication
analyses the line: a title page proves the name and says nothing about the
contents, and claiming the stronger relation from the weaker evidence is the
error this catalogue exists to avoid.

`renamed` was added after the fact, on two findings that had nowhere to
go. The Latvian Gambit was the Greco Counter-Gambit until Riga analysts
re-examined it and MCO-7 adopted the new name in 1946; and Lichess's
public history records 263 renamings of catalogue rows since 2019, each
with an author and a date. A name that changed is one of the few
naming facts that can be dated exactly, which makes it worth more than
most, and prose in a notes field cannot carry it.

`evidence_grade` is the H4.4 enum: `verified` (reference-grade book or
encyclopaedia), `attested` (credible published source), `traditional`
(universally repeated, no primary source found), `disputed`. Every claim
carries its grade in public. A hedge stated is scholarship; a hedge
hidden is a lie.

## Source doctrine (this is the part that matters)

Two different questions get confused here, so keep them apart.

**The legal question is settled, and it is permissive.** Chess moves are
facts, not protected works. When the organiser of the 2016 Carlsen
against Karjakin match tried to stop others from transmitting the moves,
a New York court refused: the moves are in the public domain. Nobody
owns a game. A game found in any database may therefore be cited by its
identifying facts — players, event, place, year — with no obligation to
name where the finder happened to see it, because the game is not from
there. It is from history.

**The verifiability question is ours, and it is stricter.** H0.4 says a
published claim cites something a stranger can check. That rules out
aggregates over a private corpus — "N games in Opening Master", "first
appearance per Mega" — not because they are protected but because no
reader can test them. (The practical footnote: EU database law does
protect substantial extraction from a compilation even when the items
are facts, so bulk harvesting stays out of bounds regardless. Citing
individual games does not.)

- **Never publishable**: counts and rankings derived from a commercial
  compilation. The validator already fails these.
- **Always publishable**: a dated game with players and event, however
  it was found. Chess games have been printed in tournament books and
  magazines for two centuries; they belong to everyone.

Which yields the working method:

> **Private corpora are telescopes, not citations.** Search them to find
> leads. Verify each lead against a public source. Cite the public
> source. The telescope never appears in the bibliography.

### Source tiers

| tier | examples | may be cited? |
|---|---|---|
| Reference literature | Oxford Companion, monographs, tournament books | yes, `verified` grade |
| Public game databases | Lichess masters (API), LumbrasGigaBase (free download) | yes, with the game's own identifying data |
| Public entity registries | Wikidata | yes, for entity identity only |
| Commercial compilations | Opening Master, Mega, commercial correspondence sets, Opening Encyclopaedia | **no** — discovery only |

The second tier is what makes the chronicle layer tractable. A freely
downloadable historical database means a claim like "played at the first
world championship, 1886" is checkable by a reader with a browser, not
just by someone holding the same commercial subscription. The
pre-1900 public shard alone carries roughly 19,000 games and over a
hundred world-championship-era events, which is the entire foundation
the treatise-and-first-champions work needs.

Games are identified in a citation the way historians do it: players,
event, place, year — never a row number in a product.

### Women's world championships are first class

`wch_match` covers the women's championship line as it does the open
one, from Menchik onward, with the same evidence bar and the same
completeness expectation. Chess data has a long habit of treating
women's events as a footnote or omitting them; the public bases carry
them (thousands of women's events across the historical shards), so the
only way OCN ends up with a partial chronicle is by choosing to. Any
coverage report that counts championship openings reports both lines
separately, so a gap is visible rather than averaged away.

## Build order (post-announcement)

1. **World championship openings, machine-derived.** Every WCh game is
   exhaustively documented in public sources. Run `ocn annotate` over a
   clean-provenance WCh corpus and the openings-to-championships mapping
   falls out as derived data rather than curated prose. Same for the
   Candidates. Cheapest, most spectacular, zero editorial risk.
2. **The treatise school.** The most-played lines of the catalogue are
   also the oldest: Ruy López (1561), Greco (~1620), Damiano, Polerio,
   Salvio, Philidor. Their sources are reference-grade and public domain,
   which makes them the natural first `verified` lot, and they populate
   `analysed-in` with real publications.
2. **Player repertoires.** Per-player game files are a discovery source
   for `played-by`. Publish the relation with a dated example game,
   never a count from a private database.
3. **Correspondence.** Where deep theory was historically tested; a
   distinct `kind` so a reader can tell OTB practice from postal
   analysis, which are different kinds of evidence about a line.

## What this unlocks in the explorer

Entity routes (`#/person/...`, `#/event/...`), a chronological view of
any family, and the sentence a reader remembers: not "B90" but "this is
the line Kasparov and Kramnik fought over in London, 2000".
