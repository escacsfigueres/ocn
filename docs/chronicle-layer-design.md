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

`evidence_grade` is the H4.4 enum: `verified` (reference-grade book or
encyclopaedia), `attested` (credible published source), `traditional`
(universally repeated, no primary source found), `disputed`. Every claim
carries its grade in public. A hedge stated is scholarship; a hedge
hidden is a lie.

## Source doctrine (this is the part that matters)

The H0.4 rule stands and extends: **a published claim cites a source a
stranger can check.** Commercial databases are compilations; their
contents are licensed and unverifiable to a reader. So:

- **Never publishable**: "N games in Opening Master", "first appearance
  per Mega", "the corpus shows". The validator already fails these.
- **Always publishable**: a dated game with players and event, because
  chess games are historical facts, printed in tournament books,
  magazines and public databases for two centuries. Facts are not
  compilations.

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
