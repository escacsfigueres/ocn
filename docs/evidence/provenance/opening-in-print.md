# The position is seventy years older than the name

**Status: proposal, blocked, nothing applied.** Companions:
`opening-in-print.proposed.tsv` and `opening-in-print.events.proposed.tsv`.
Written 2026-08-04 from a question Albert asked while reading the monograph.

## The question

The Ruy López monograph's span chart anchored its axis on Lucena's book of
about 1497, labelled "the earliest book this catalogue cites". Albert asked
whether Lucena actually discusses this opening.

## The answer, and why it changed the chart

**Lucena cannot be sustained.** Wikipedia's article on him says his
*Repetición de Amores y Arte de Ajedrez* (Salamanca, c. 1497) "includes
analysis of eleven chess openings" and **does not say which eleven**. The
sources that do name the Ruy López among them are a chess.com blog post and
Grokipedia, which is below the standard this catalogue applies to everything
else. The claim circulates widely and is not citable here.

**Something older and better exists.** Wikipedia's article on the opening
states it directly:

> "Although it bears his name, this particular opening was included in the
> Göttingen manuscript, which dates from c. 1490."

That is seven years earlier than Lucena and, more to the point, it is about
*this opening* rather than about the beginnings of chess printing. The
monograph's axis now starts there.

The distinction matters more than the seven years. Lucena was "the oldest
book we cite"; the Göttingen manuscript is "the oldest document that contains
this opening". Only the second is a fact about the Ruy López.

## What that exposes

**The position predates the name by about seventy years.** The moves were
written down around 1490; Ruy López de Segura, who the opening is named
after, published his *Libro de la invención liberal y arte del juego del
axedrez* at Alcalá de Henares in 1561. For a catalogue whose subject is names
rather than moves, that gap is the single most useful fact on the axis, and
1561 is the only date on it that is about a name at all.

## The proposal

Two `analysed-in` claims on `C.RyL`, using a relation that is **already in the
closed set** in `docs/chronicle-layer-design.md` and has never been used:
"published analysis, subject is a `publication` event". It would be the first
time the catalogue records that a *document contains an opening*, as against
recording that a *game plays* one.

## Why it is blocked

`catalog/ocn-1.events.tsv` is generated. `tools/build_chronicle.py` derives it
wholesale from `catalog/ocn-1.wch.tsv`, emits only `wch_match` and
`wch_match_women`, and **does not preserve rows it did not create**. A
publication event added by hand would survive exactly until the next
regeneration — which is not hypothetical, because correcting the participant
names on 2026-08-03 required one.

The fix is small and belongs before this proposal, not after it: the builder
should read any existing `events.tsv`, keep every row whose `kind` is not one
it generates, and merge rather than overwrite. The same argument applies to
`claims.tsv`, where the splice is currently done by hand for the same reason
(see `wch-participant-integrity.md`), and to `people.tsv`, where regenerating
would erase the curated Wikidata identities.

Until then the two claims and their two event rows sit here.

## A caveat to keep with the date

The Göttingen manuscript's date is not settled: the literature places it
somewhere between 1471 and 1505, and it is not known whether it or Lucena's
book came first. The claim carries `attested` and the note carries the range.
Related: [[evidence-sustains-less-than-triage]].
