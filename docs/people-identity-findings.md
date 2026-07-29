# Giving the chronicle's people a public identity

**Status: resolved and proposed, nothing applied.** 55 of the 61 people
in `catalog/ocn-1.people.tsv` now have a verified Wikidata identifier
with birth and death years, in
[`evidence/people/people-proposed.tsv`](evidence/people/people-proposed.tsv).
The reasoning for every one of the 61, including the six refusals, is in
[`evidence/people/wikidata-resolution.tsv`](evidence/people/wikidata-resolution.tsv).
The catalogue itself is untouched and the apply is waiting on a GO.

## Why this column and not another

[`chronicle-layer-design.md`](chronicle-layer-design.md) calls
`wikidata_qid` the load-bearing column of the people table, and the
reason is that we should not be in the biography business: a champion is
a public entity with dates and spellings in every language, and
referencing that entity is both cheaper and more honest than
re-litigating it in our own columns. `build_chronicle.py` leaves the
column empty on purpose, because it derives people from corpus spellings
and a corpus spelling is not an identity.

## The dates are the verification

Matching a surname to a Wikidata item is easy and wrong. Searching
"Karpov" returns an asteroid, a railway station and eight unrelated
people before it returns a chess player.

So a candidate has to survive the years we actually watched the person
play, taken from the championship map: born early enough to have played
their first game, not dead before their last, not implausibly old by the
end. That single test does almost all the work — someone the corpus saw
playing in 1886 and a Wikidata item born in 1963 are not the same human,
whatever the surname says. Where more than one candidate survives, the
corpus's own given name breaks the tie if it names exactly one of them,
and where it does not, the column stays empty.

It never guesses. A wrong identifier silently attaches every opening a
person played to the wrong human, and nothing downstream can detect it.

## Two things the identifiers exposed

**`alekhine` and `aljechin` are the same man.** The corpus spells
Alexander Alekhine's name two ways, and the surname-based person id
split him into two people — one with 82 championship games, one with 21.
Both resolved to Q131374. The QID is doing here exactly what an external
identifier is for: it is the only column in the table that can prove two
rows are one person. `bikova` and `bykova` are the same case (Elizaveta
Bykova, women's champion), visible in the spellings but not yet joined
by a QID because the abbreviated row did not resolve.

**Three person ids merge two different humans each.** Because the id is
the surname alone, distinct players collapse together, and
`build_chronicle.py` then picks the longest spelling as the display
name — which can pick the wrong man:

| person id | corpus spellings | games |
|---|---|---:|
| `karpov` | Karpov, Anatoly / Karpov, **Aleksandr** | 139 / 44 |
| `botvinnik` | Botvinnik, Mikhail / Botvinnik, Alexander | 148 / 1 |
| `smyslov` | Smyslov, Vladimir / Smyslov, Vasily | 65 / 4 |

`karpov` is the damaging one: the display name reads "Karpov,
Aleksandr", so the row for the world champion is labelled with another
player's given name, and 44 games that are not Anatoly's hang off it.
This is why `karpov` is one of the six refusals — the resolver could not
find a chess player named Aleksandr Karpov who fits 1978-1996, which is
the correct answer to a question that should not have been asked.

Smyslov is the reassuring case: the corpus's majority spelling
("Vladimir") is simply wrong, the champion is Vasily, and the date check
found Q104148 Vasily Smyslov anyway because the bare surname search plus
the playing window is stronger than the misspelling.

## The six it would not answer

`bikova` (a duplicate of `bykova`), `karpov` (two humans in one row),
`kushnir-aleksandr`, `marshall-viele`, `morrison`, `zvorykina`. Four of
those are genuinely obscure or corrupted corpus rows; two are the
structural problems above. None should be resolved by hand until the
person table's own duplicates are settled, because resolving a row that
represents two people just encodes the error with an identifier.

## One date worth a second pair of eyes

Wikidata records Jan Timman as having died on 18 February 2026, with
references attached. That is recent enough to be worth confirming before
it goes into a published table, though nothing about the claim looks
irregular.

## What needs a GO

1. Apply the 55 resolved identities to `catalog/ocn-1.people.tsv`
   (`--apply --out`), leaving the six refusals empty as they are.
2. Separately, decide the merges: `aljechin` into `alekhine`, `bikova`
   into `bykova`. These change `events.participants` and so are a
   chronicle rebuild, not a column fill.
3. Separately again, decide what to do about surname-only person ids.
   The honest fix is to key people by QID once they have one, which is
   the argument the design was already making.
