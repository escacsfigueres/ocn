# The Oxford Companion, read entry by entry

**Status: eleven findings read and citable, nothing applied.** These come
from Hooper and Whyld, *The Oxford Companion to Chess*, second edition
(Oxford University Press, 1992), consulted directly. Each row below names
the entry and the printed page, so anyone holding the book can check it.

This is the source [`treatise-school-findings.md`](treatise-school-findings.md)
concluded was missing. It answers what *Chess Notes* structurally could
not, and in three places it overturns what the earlier pass concluded.

## The method, and a negative result about method

The first thing tried was the obvious thing: index all ~950 named
opening entries mechanically and join them to the catalogue in bulk.
**That does not work, and it cannot work.** Two reasons, and the second
is the interesting one.

The practical reason is that one headword routinely covers several
unrelated openings — "Alekhine Variation" alone spans the Slav, the
Queen's Pawn, the Dutch and the Staunton Gambit, each with its own
number — so a name match lands on the wrong line unless the parent
opening is checked too. Fuzzy-matching the parent against OCR of this
quality produced confident false positives: "Hanham Variation" scored a
clean match against parent "FRENCH DEFENCE" because both strings contain
the word *Defence*. Hanham is a Philidor line. Two rounds of automation
produced two rounds of subtle errors.

The deeper reason is that **`verified` means somebody read the page**. A
bulk fuzzy join cannot produce that grade no matter how good it gets,
because the thing the grade certifies is the reading. Automating it is
self-defeating: it would manufacture exactly the false confidence the
grade exists to prevent. So the Companion is used the way a reference
work is meant to be used — one entry at a time, read.

The mechanical index is still worth having as a *finding aid* (it says
which page to turn to), and that is all it is used for here.

## What the entries say

| catalogue row | Companion entry | p. | what it establishes |
|---|---|---:|---|
| `C.Dam` | Damiano Defence, 1051 | 101 | "a variation **given by Lucena** and rightly **condemned by Damiano** as leading to a lost game" |
| `C.PhD` | Philidor Defence, 1015 | 305 | "**noted by Lucena and recommended by Ruy López**. Its strongest advocate was Philidor" |
| `C.Pon` | Ponziani Opening, 813 | 314 | "**mentioned by Lucena**, it was liked by Staunton, and for that reason sometimes called the **English Knight's, or Staunton Opening**" |
| `C.RyL.Coz` | Cozio Defence, 783 | 97 | in the Spanish, "a variation **first given by Carrera**", also the **Lucena-Cozio** or **Steinitz Variation** |
| `A.Hol.Sta` | Staunton Gambit, 258 | 393 | "**played by Staunton against Horwitz in 1847**" |
| `C.Sco.Nxd4` | Lolli Variation, 1007 | 232 | "**Lolli's response to the Scotch Game**. He considered this safer than 3...exd4" |
| `C.LtO` | Greco Counter-gambit, 1044 | 158 | "later called the **Latvian Counter-gambit, or Riga Gambit**, said by **Polerio to have been the idea of his friend Leonardo di Bona**. It was given in **Greco's book, published in Paris, 1669**. Advocated by Deschapelles" |
| `C.Bsh.Ber.f4` | Greco Gambit, 658 | 158 | in the Bishop's Opening, "**given by Greco** and still played" |
| (King's Gambit) | Greco Gambit, 1146 | 158 | "**given by Polerio**, and sometimes called the **Greco-Polerio Variation, or the Calabrian Gambit**, after Greco's homeland" |
| `C.KGm.Acc.All` | Allgaier Gambit, 1166 | 12 | "played around 1780 by the Englishman **Cotter**, after whom it is sometimes named... **Allgaier was the first to publish a detailed analysis**, which appeared in the fourth edition of his book, **1819**" |
| `D.Alb` | Albin Counter-gambit, 110 | 6 | "**introduced by Cavallotti** (after whom it is sometimes named) in a game against Salvioli at **Milan 1881**, and re-introduced in the game **Lasker-Albin, New York 1893**" |

## Three conclusions the earlier pass got wrong

**The Scotch Lolli is real.** `treatise-school-findings.md` moved
`C.Sco.Nxd4` from candidate to open question, and called it "more
doubtful than the Lucena", because across three parts of *Chess Notes*
Lolli appeared only in connection with the rook-and-bishop ending. The
Companion has the entry, with a number and a rationale. The negative was
an artefact of asking a corrections column about an uncontested name.

**The Latvian Gambit's history is older and stranger than recovered.**
The earlier pass established the twentieth-century renaming (Greco
Counter-Gambit becomes Latvian, via Riga analysts and MCO-7). The
Companion adds the other end: Polerio attributed the *idea* to Leonardo
di Bona, and Greco's book of 1669 is where it was given. So the line
carries the name of the man who published it, over an idea credited to
someone else entirely — and then got renamed after a country three
centuries later.

**The Cozio attribution is disputed at the source.** The head was on the
worksheet as a question about which edition to cite. The real question
is whether it is his at all: the Companion says the Spanish line 783 was
*first given by Carrera*.

## The pattern in all of this

Six of the eleven say the same kind of thing: **the person on the label
is not the person who invented the line.** Damiano condemned his.
Philidor advocated a line Lucena had noted and Ruy López recommended.
Allgaier published the first real analysis of something Cotter played.
Cavallotti introduced Albin's gambit. Polerio credited di Bona.

That is precisely the distinction `docs/treatise-school-questions.md`
insisted on — `analysed-in` is not `invented-by` — and it turns out to be
the majority case, not an edge case. Any attribution lot built from this
must carry the role, not just the name.

## What needs a GO

1. These eleven can become an attribution lot at grade **`verified`**,
   each citing the entry and page above. They are the first `verified`
   rows the catalogue would have.
2. Several aliases fall out for free and belong in a separate lot:
   English Knight's Opening and Staunton Opening for `C.Pon`; Riga
   Gambit and Greco Counter-Gambit for `C.LtO`; Calabrian Gambit for the
   King's Gambit Greco; Lucena-Cozio and Steinitz Variation for
   `C.RyL.Coz`.
3. `D.Alb`, `C.RyL.Coz` and `C.KGm.Acc.All` should carry a `disputed`
   note recording the rival claimant the Companion names.
4. The remaining treatise heads (Lucena, Jaenisch, Stamma, Salvio,
   Bilguer, the Ruy López head itself) are not yet read. They are
   lookups, not research, now that the book is to hand.

**The book is not in the repository and must not be.** It is a
copyrighted reference work; what is recorded here is the fact and the
page, which is what a citation is.
