# Winter Chess Notes, batch 4: verification record

**Status: verified, un-applied.** Companion to
`docs/manifests/winter-batch-04.manifest.json`. Drafted 2026-08-02 from the
complete dossier (62 slugs, 207 strong items with full text). Every item
was re-read first-hand at chesshistory.com before drafting.

## Where the material actually belongs

The dossier files its strongest clusters under the parent heads — 22 items
on `B.Sic` and 18 on `B.Fre`, the two most-played defences, both with empty
attribution and notes. Almost none of that material is about the parent
name. It is about **sub-variations**: the Dragon, the Kalashnikov, the
Löwenthal, the Rossolimo, the Maróczy Bind, Fort Knox. Filing by mention
rather than by subject is a reasonable harvest heuristic; drafting has to
undo it, or the notes land on the wrong row.

## `B.Sic.Dra` — the Dragon

A metaphor with a receding earliest date, which is why the note records a
chain rather than a single citation:

- Tartakower, 'Die hypermoderne Schachpartie' (instalments, 1924-25),
  p. 270, annotating Alekhine v Sämisch, Vienna 1922: "Die
  Drachenvariante" (C.N. 7826).
- Heinrich Wolf, Wiener Schachzeitung, June 1924, p. 164, annotating
  Tartakower v Lasker, New York 1924: "die sogenannte **Paulsensche**
  Drachenvariante" — a form of the name attaching Paulsen to it that has
  not survived.
- H. Weenink, Tijdschrift van den Nederlandschen Schaakbond,
  February-March 1925, p. 43: 'De "drakevariant" van den Siciliaan'
  (C.N. 5135).
- Winter reports an earlier occurrence at Wiener Schachzeitung,
  January-February 1914, p. 30. **It is reproduced there as a facsimile
  image, not as text**, so the note cites Winter's report of it rather
  than quoting it.
- Aristide Gromer, 'Les échecs par la joie' (Brussels, 1939), pp. 52-53,
  used "la variante dite du 'Dragon'" for **White's g2-g4 advance** — the
  term meaning something other than Black's setup, worth recording because
  it shows the name was not yet fixed.

## `B.Sic.Kal` — the Kalashnikov

The clearest case in the batch, and a useful one for the catalogue's
purpose: **the name honours a rifle, not a chess player.** Dirk Jan ten
Geuzendam, New in Chess 2/1990, p. 18: "the Kalashnikov — the
semi-automatic, fast-firing version of the Sveshnikov". BCM, October 1991,
p. 479: "known jocosely as 'Kalashnikov'". Earliest printed uses located:
Ian Rogers in CHESS, April 1991, p. 25, and a note by John van der Wiel in
New in Chess 1/1989, p. 35. Winter asked when and why the name attached,
after Mikhail Kalashnikov's death on 23 December 2013, and reports nothing
conclusive (C.N.s 8450, 8456, 8493).

Note for the identity work: **Mikhail Kalashnikov must never be added to
`people.tsv` as a chess eponym.** The name is a pun on the weapon's
reputation, not an attribution to a person, and an entity resolver would
match him confidently and wrongly — the same trap as Frankenstein's
monster and Chess.com.

## `B.Sic.Loe` — the Löwenthal

Winter's own verdict is that "the whole matter seems murky", and the note
says so. No Löwenthal game with 4...e5 5 Nb5 a6 is known; his connection is
editorial, via the 1865 six-part article 'The Sicilian Opening' in the
Chess Player's Magazine, which he edited, where 5 Nb5 appears in two
different move orders and his name is attached with a wrong reference to
the ninth rather than eleventh game of his match with Morphy. Modern Chess
Openings then printed a wrong origin date across three editions: 1839 in
the 10th (1965) — impossible, McDonnell having died in 1835 — 1934 in the
11th (1972), and the correct 1834 only in the 12th (1982). Winter's
standing request is for early uses of the term applied separately to
4...e5 and to 4...e5 5 Nb5 a6 (C.N. 6580).

**A catalogue observation this raises.** `B.Sic.Kal` (4...e5 5 Nb5 **d6**)
carries "Sicilian Defense: Löwenthal Variation" among its aliases, while
`B.Sic.Loe` (4...e5 5 Nb5 **a6**) is the Löwenthal proper. That is exactly
the confusion Winter documents, now encoded in the alias table. Whether
the alias should stay is an editorial question, not something this batch
should settle; but it should be looked at.

## Dropped from this batch

`B.Fre.FKn` (Fort Knox) was drafted and then removed. Its only evidence is
that Winter asked who gave the line that name and when (C.N. 7330) and got
no answer. `--dry-run --strict` refused it at grade PARTIAL, which is the
guardrail behaving correctly; the response was to drop the row rather than
relabel it CLEAR. A note saying only "nobody knows" tells a reader nothing
the absence of a note does not already tell them.

## Dry-run record

`--validate` and `--dry-run --strict` both exit 0 on 2026-08-02 after the
Fort Knox row was removed; 5,899 rows before and after, 3 rows changed.
