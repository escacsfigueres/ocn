# Winter Chess Notes, batch 2: verification record

**Status: verified, un-applied.** Companion to
`docs/manifests/winter-batch-02.manifest.json`. Drafted 2026-08-02 from the
complete local Winter harvest (2,692 C.N. items). Every item below was
re-read first-hand at chesshistory.com before drafting; where the harvest
text and the live page were compared they matched verbatim.

## `E.Nim.Sml` — the Sämisch Variation, disclaimed by Sämisch

The batch's centrepiece, and the kind of case the catalogue exists for: a
variation universally named after a player who published a denial that it
was his.

**C.N. 4981** (winter34.html), reporting Peter Anderberg. In his column in
the *Berliner illustrierte Nachtausgabe* of 23 February 1934, written after
the death of the Silesian master Adolf Kramer, Sämisch introduced a game
with: "Die vorliegende Partie ist die Prioritätspartie der bekannten
Variante 1 d4 Sf6 2 c4 e6 3 Sc3 Lb4 4 a3!?, **die fälschlich als meine
Erfindung ausgegeben wurde**. Die erstmalige Anwendung dieser Spielweise
geschah aber durch A. Kramer, nur ist diese Partie vergessen worden, weil
sie in einem Provinzturnier gespielt wurde." The game is Kramer v Machate,
Silesian championship, Bad Altheide 1926 — a tournament Sämisch himself
won as an unofficial competitor.

Priority is nonetheless not settled in Kramer's favour either. **C.N. 5682**
gives an earlier occurrence by transposition: Voellmy v Procházka,
correspondence 1918-19, *Schweizerische Schachzeitung*,
September-October 1919, pp. 120-122. C.N. 4981 also notes Ferrari v Stalda,
Trieste 1923 (MegaBase 2007), and that Sämisch was evidently unaware of
Norman v Michell.

Hence the recorded attribution names both, with the disclaimer attached to
the eponym rather than hidden in a note: Sämisch as system namesake who
disclaimed the invention, Kramer as first application *per Sämisch*. The
qualifier "per Sämisch" is load-bearing — the transposition evidence means
the catalogue must not assert Kramer as originator flatly.

## `A.Eng` — English Opening

- **C.N. 10066** (winter145.html): Potter and Steinitz on 1 c4, *The Field*,
  18 April 1874, p. 375, and *City of London Chess Magazine*, May 1874,
  p. 89: "This move, when made by the first player, constitutes what is
  called the 'English Opening'." And G. Reichhelm, *American Chess
  Journal*, June 1879, p. 362 (from *Hartford Weekly Times*, 19 June 1879,
  p. 4): "Now justly called 'the English opening', it having been
  introduced by the great English champion, Staunton."
- **C.N. 9166** (winter128.html): Winter's still-open request for instances
  during Staunton's lifetime of the name being used on the basis of his
  espousal.

The distinction matters and is preserved in the drafted wording: the 1874
citations *name* the opening without crediting anyone, while the 1879
citation *credits Staunton* and postdates his death. `attributed_to` takes
Staunton as populariser on the strength of the 1879 primary; the name
itself is national, and the catalogue does not claim he coined it.

## `B.Nim` — Nimzowitsch Defence

Attribution (Nimzowitsch, populariser) came from the Companion round-2 lot
and is unchanged; the Companion's bare "rival claimant: Fischer" line is
now backed by substance.

- **C.N. 9484** (winter134.html): the German name Fischer-Nimzowitsch after
  Eduard Fischer; Hugh Myers, *The Nimzovich Defense to 1. e4* (Yorklyn,
  1995), p. i: Nimzowitsch "was by no means its originator or inventor",
  but "there's no doubt that he was the first to play it with frequent
  success in major international competition. That is an acceptable reason
  for naming it The Nimzovich Defense" — direct corroboration of the
  populariser role already recorded. On Fischer, Myers: "I have never seen
  the score of a single game in which he played it." *Modern Chess
  Openings* introduced Fischer's name in the 11th edition (1972, ed. Korn),
  p. 192.
- **C.N. 12175** (winter195.html): the name was already in British use in
  1903 — *Alderley & Wilmslow Advertiser*, 11 September 1903, p. 3, a
  column probably by Carslake Winter-Wood, calling 1 e4 Nc6 "the Fischer
  defence", printed with Schories v Allcock, Plymouth, 31 August 1903.

## `E.Nim` — Nimzo-Indian Defence

- **C.N. 11441** (winter181.html): Edward Lasker's footnote in *The Game of
  Chess* (New York, 1972), p. 447, on the term: "A horrible abbreviation of
  Nimzovich-Indian. The mutilation of the name of the greatest chess
  theorist ... is as unnecessary as it is undignified." Dropped from the
  1997 algebraic edition by Nunn and Burgess.

Terminology history rather than attribution; `attributed_to` unchanged.

## What the harvest does not yet support

- **Budapest (`E.Bud`)**: C.N. 5988 concerns only a monograph by
  "St. Schwartz" (Antwerp, c. 1927) and a request for information about its
  author; C.N. 6571 came through the harvest as a title-only stub. The
  Jakobetz/Gyuricza/Bottlik chapter on the disputed origin (pp. 37-48)
  remains an offline task. No claim drafted.
- **Harvest gaps to report upstream**: several nomenclature-tier items
  arrived as titles with no body (C.N. 3712, 3713, 4974, 6571, 7639, 4603
  among them) — the extractor missed the body on those pages. Separately,
  roughly a third of the "nomenclature" tier is about the term *world
  chess champion*, not opening names; a tier split would sharpen the queue.

## Dry-run record

`--validate` and `--dry-run --strict` both exit 0 on 2026-08-02;
5,899 rows before and after, 4 rows changed.
