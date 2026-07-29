# The eponym list: what a systematic survey gives that a scholar's notebook cannot

**Status: evidence gathered, nothing applied.** 211 candidate
attributions are sitting in
[`evidence/eponyms/named-after-people.tsv`](evidence/eponyms/named-after-people.tsv),
each joined to a catalogue row by its move sequence and graded by what
its own footnote rests on. No catalogue row has been touched, and no
manifest has been written.

## Why this source, after the last one failed

[`treatise-school-findings.md`](treatise-school-findings.md) records a
negative result worth restating: seventy queries against five libraries
of chess history returned publication facts and almost no attributions.
The reason was structural, not accidental. Edward Winter's *Chess Notes*
is a body of corrections — it writes about the naming questions that are
*contested* and takes the settled ones as read. Asking it who the Adler
Variation is named after is asking a corrections column to state the
uncontroversial.

Wikipedia's `List of chess openings named after people` is the opposite
shape. It exists precisely to state the settled ones, it does so for
about 270 openings at once, and — the part that makes it usable — most
entries carry a footnote saying who says so. It is the systematic survey
the treatise pass went looking for and did not find.

## The join is by position, never by name

Every entry gives its moves. So an entry becomes a catalogue row only
when its move sequence converts to that row's exact `moves_uci`.

This matters more than it sounds. Matching "Alekhine Variation" against
a catalogue row called "Alekhine Variation" would look like it worked
and would be wrong often: there is an Alekhine Variation of the Budapest
Gambit, an Alekhine–Chatard Attack in the French, and Alekhine's Defence
itself, and a name-string match cannot tell them apart. `d2d4 g8f6 c2c4
e7e5 d4e5 f6g4 e2e4` can only be one of them.

Of 265 parsed entries, 228 found a catalogue row that way, and 17 of
those were already attributed by hand — those are left alone, because a
row a human reviewed outranks a footnote. **211 are new.**

The 34 that matched nothing are their own finding: they are positions
the catalogue does not currently hold at that depth, so they are a
coverage worklist rather than a failure.

## Nothing here is `verified`, and that is deliberate

The grade enum reserves `verified` for a reference-grade source. A
footnote is not a reading. This project has already retracted one
citation that sounded right and pointed at the wrong book, so the rule
this lot follows is blunt: **the best grade available from a footnote is
`attested`**, and an entry with no footnote at all is `traditional`.

The tier of the underlying source travels in its own column, so the
reference-grade ones can be promoted by a human who has the book open:

| what the entry cites | rows | grade issued |
|---|---:|---|
| Oxford Companion (Hooper & Whyld) | 19 | `attested` |
| Sunnucks, *Encyclopaedia of Chess* | 30 | `attested` |
| a book or journal | 25 | `attested` |
| a web source | 117 | `attested` |
| nothing at all | 20 | `traditional` |

The 74 reference-backed rows are the promotion queue. They are also the
answer to the question the treatise pass left open — the Oxford
Companion turns out to be reachable entry by entry through the
footnotes, rather than needing the whole book up front.

## Wikipedia is the finding aid, not the citation of record

The catalogue already sets this convention: its Trompowsky row cites
Hooper and Whyld with a page, and adds "via Wikipedia footnote". Same
doctrine as the design's telescope rule — search the aggregator, cite
what it points at, disclose the route.

There is a licensing reason to hold that line as well as an
epistemological one. Wikipedia's text is CC BY-SA 4.0 and this catalogue
is CC BY 4.0, which are not the same licence: share-alike would
propagate. The facts themselves do not carry that problem — that an
opening is named after a person is a fact, and facts are not anyone's
property — but the list's prose and its particular selection are the
encyclopaedia's own work. Recording the fact and its underlying source
stays clear of both hazards. Copying the list would not.

## What the disagreements turned out to be

62 of the 211 attach a person whose surname does **not** appear in the
catalogue's own name for that row. Those looked like conflicts and are
mostly something better: the same position carrying two established
names, which is an alias the catalogue is missing.

| position | OCN calls it | the list calls it |
|---|---|---|
| 1.g3 | Hungarian Opening | Benko's Opening |
| 1.e4 g5 | Borg Defence | Basman Defence |
| 1.Nc3 | Van Geet Opening | Dunst Opening |
| 1.Na3 | Sodium Attack | Durkin Opening |
| 1.Nf3 d5 2.g3 | Réti, King's Indian Attack Setup | Barcza System |

Those are additions, not corrections. A handful of the 62 are real
questions instead — `B.CaK.Adv.Bot` is named for Botvinnik and Carlsen
in the catalogue while the list attributes the same position to Arkell
and Khenkin — and they go to the open-questions pile rather than into a
lot.

## Three errors found in the source

Three entries give moves that do not play out. They are typos in
Wikipedia, and they are worth reporting upstream:

| entry | printed | should almost certainly be |
|---|---|---|
| Moeller Attack of the Italian Game | `5.d4 cxd4` | `exd4` — Black has no c-pawn that can take |
| Morozevich Variation of the Slav | `...Ndb7` | `Nbd7` |
| Rubinstein Variation of the Budapest | `3.dxe4` | `3.dxe5` |

A parser that guessed at these would have manufactured three
attributions for positions nobody plays. Reporting them is the whole
value of converting the moves rather than trusting them.

## A bug this exposed in our own code

One entry, the Wolf Gambit, failed on `5.Nge2` — and that turned out to
be our defect, not Wikipedia's. `tools/chess_uci.py` matched SAN by
generating the notation for each legal move and comparing strings, and
`san()` emits the *shortest* unambiguous form. Where only one knight can
reach e2 it writes `Ne2`, so the perfectly legal `Nge2` matched nothing.

Published PGN disambiguates more than it strictly must, all the time.
The module is what `tools/validate.py` uses, so the bug was quietly
rejecting real games anywhere a source over-disambiguated. Fixed, with
tests for redundant file and rank origins on both quiet moves and
captures — and tests that a *wrong* origin (`Nbe2`, from a knight that
cannot get there) is still an error rather than a shrug.

## What happens next, and what needs a GO

- The 211 are evidence, not a manifest. Turning them into an attribution
  lot means writing an `ocn.attribution_manifest.v1`, running
  `tools/apply_attribution_manifest.py` as a dry run, and applying only
  under an explicit GO — the same gate as every other lot.
- The 74 reference-backed rows are worth splitting into their own lot,
  because they are the ones that can later be promoted to `verified`.
- The alias candidates are a separate lot with a separate shape, and
  should not be smuggled into an attribution manifest.
- `List of chess openings named after places` is parsed differently: it
  names no person and states no "named after" clause, so the place has
  to be read out of the opening's own name. That is an editorial pass,
  not a mechanical one, and it is not started.
