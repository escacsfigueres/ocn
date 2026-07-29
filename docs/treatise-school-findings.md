# What the library could and could not answer

**Status: findings, nothing applied.** The first nine of the fifteen
treatise heads have been put to five source libraries (Edward Winter's
*Chess Notes* in three parts, two Spanish chess history collections),
45 queries in all, through `tools/ask_treatise_sources.py`. The raw
answers with their citations are in
[`evidence/treatise/`](evidence/treatise/).

The result splits cleanly in two, and the split is the finding.

## What the library confirms: the bibliography

Publication facts came back cited and consistent. These are enough to
populate `events` rows of kind `publication`, which the chronicle design
already provides for -- a treatise is an event, which is how "analysed
in his book" becomes a queryable relation rather than prose.

| person | work | where and when | source |
|---|---|---|---|
| Ruy López de Segura | *Libro de la invención liberal y arte del juego del axedrez* | Alcalá, 1561 | Winter, *Chess Notes* |
| Philidor | *L'Analyze des Echecs* | London, 1749; English as *Chess Analysed*, London 1750; revised 1752, 1754, 1790 | Winter, *Chess Notes* |
| Pedro Damiano | *Questo libro e da imparare giocare a scachi et de le partite* | Rome, 1512 (an earlier lost edition is mentioned) | Winter, *Chess Notes* |
| Lucena | his treatise | 1497 "or a little earlier"; died c. 1530 | Winter, *Chess Notes* |
| Ponziani | first edition | 1769, title not stated in these sources | Winter, *Chess Notes* |
| Jaenisch | a St Petersburg publication | 1837, title not stated in these sources | Winter, *Chess Notes* |

## What it does not confirm: the attributions themselves

For every one of the nine heads, the library could not say **which
reference work states that the opening is named after the person**, nor
**what the person's role was** -- invented, first published, or
popularised. That is not a failure of the library; it is what the
library is. *Chess Notes* is a body of corrections and controversies,
not a dictionary of eponyms: Winter writes about the naming questions
that are contested, and takes the settled ones as read.

So the attribution layer needs a different source class: an
encyclopaedia of openings, the *Oxford Companion to Chess*, or the
treatises themselves. Knowing that before spending a week is the point
of having asked.

## Two heads that should not be attributed as planned

The negatives were more informative than the confirmations.

**`C.RyL.Luc`, the Lucena Variation.** Winter records that the famous
Lucena Position in rook endings is not Lucena's at all -- it comes from
Salvio -- and that Lucena's book does not contain the position that
bears his name. A man whose most famous eponym is misattributed is not a
man whose second eponym should be taken on trust. The sources say
nothing about which Ruy López line is his, or on whose authority. This
head moves from candidate to **open question**.

**`C.Sco.Nxd4`, the Scotch Lolli Variation.** Across three parts of
*Chess Notes*, Lolli appears only in connection with the "Lolli
position" in rook and bishop against rook. There is no mention of a
Lolli line in the Scotch, and no source attaching his name to one. Also
**open**, and more doubtful than the Lucena: at least Lucena has a
documented connection to the Ruy López era.

## One dispute worth keeping

**`C.RyL`.** Von der Lasa argued in the *Deutsche Schachzeitung* of 1873
(p. 163) that the opening should be called the *Deutsche Partie*,
because almost all of its development was the work of German
researchers; Cordel adopted the name in *Theorie und Praxis des
Schachspiels*. The Handbuch's eighth edition (Berlin and Leipzig, 1922,
p. 423) reports both. This is a `disputed` note on the row, not a
reason to rename anything -- but it is exactly the kind of fact the
chronicle exists to carry, and no other open chess dataset has it.

## What happens next

- The publication facts can become `events` of kind `publication` now:
  they are cited, and they claim only what they say.
- The attribution claims wait for a source that answers them. The
  library offered web research on every query; that is a lead generator,
  not a citation, and would need the same verification afterwards.
- Two heads leave the worksheet's candidate list and join the open
  questions, which is a better outcome than fifteen thin attributions.

Six heads remain to query. The pattern is unlikely to change, but the
negatives are cheap and the occasional von der Lasa is worth the wait.
