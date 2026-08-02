# Winter Chess Notes, batch 3: verification record

**Status: verified, un-applied.** Companion to
`docs/manifests/winter-batch-03.manifest.json`. Drafted 2026-08-02 from the
**repaired** harvest: the first extraction had truncated 829 of 2,696 items
at a duplicate anchor (Chess Notes emits each C.N. number twice, once in a
heading and once as an empty anchor before the body), so those items
arrived as titles only. Six of the items used here were among them. Every
item below was re-read first-hand at chesshistory.com before drafting.

## Closures the repair made possible

Three heads already in the catalogue could be finished rather than left
hanging:

- **`E.Nim.Sml` — Norman v Michell, the gap batch 2 recorded as open.**
  C.N. 4974 (winter34.html) supplies it: G.M. Norman played 4 a3 against
  R.P. Michell at Hastings, **usually dated 1923 but played on 3 January
  1924** (BCM, February 1924, p. 43; Michell won and annotated it on
  pp. 77-78). Bruce Hayden's account of the transfer, BCM, July 1965,
  p. 207: "The idea caught the eye of the German master Fritz Sämisch and
  he adopted it thereon. And thereon, as is the way of chess fashion, his
  name was bestowed on the variation." So the sequence is now legible:
  Norman plays it in 1924, Sämisch adopts it and the name follows him, and
  in 1934 Sämisch publishes a denial crediting Kramer's 1926 game — while
  a 1918-19 transposition predates them all.
- **`E.Nim` — who advocated the term 'Nimzo-Indian'.** C.N. 3712
  (winter09.html): Nimzowitsch himself called it simply 'Indisch' when
  annotating in the Wiener Schachzeitung of January 1925 (pp. 3-5, 17-18);
  Tartakower used 'La "Variante de Nimzowitch"' in L'Echiquier, January
  1930, pp. 579-581; and the earliest located advocacy of the compound is
  Hans Kmoch's footnote to the heading 'Nimzoindisch', Wiener Schachzeitung,
  May 1931, p. 132: "Diese Bezeichnung scheint mir für die folgende
  Variante sehr empfehlenswert."
- **`B.Nim` — when Nimzowitsch's name attached to 1 e4 Nc6.** C.N. 3713
  (winter09.html): the Ostend 1907 tournament book headed his game against
  Duras 'Königsläufer Eröffnung' (p. 153) but indexed it 'Verteidigung
  Niemzowitsch' (p. 334); by Tidskrift för Schack, November-December 1920,
  pp. 181-183, Nimzowitsch was annotating his own 1 e4 Nc6 game under
  'Niemzowitsch's spelöppning'.

## New heads

- **`C.Ita.Evn` — Evans Gambit.** C.N. 9332: Purdy, Chess World, 1 April
  1950, pp. 90-91, on the first known game being inventor v McDonnell, and
  the pointer to Tim Harding, 'Eminent Victorian Chess Players'
  (Jefferson, 2012), pp. 9-34, as the fullest account. C.N. 6941: the
  Chess Amateur, September 1915, p. 348, "The Evans should be called the
  German Game" — a wartime renaming proposal from a German magazine, and
  the Yorkshire Observer Budget's reply. C.N.s 9113 and 11255: the famous
  "a gift of the gods to a languishing chess world" has **no established
  author**; Reitstein raised the question in BCM, July 1965, p. 197, and
  the only source offered was MCO 9th ed. (1957), p. 6. A separate German
  remark to similar effect is ascribed to Tartakower on German-language
  sites; Winter lists three Tartakower books where it appears but the
  ascription is not settled, so the catalogue records the English phrase's
  authorship as open and does not repeat the Tartakower attribution.
- **`E.Bog` — Bogo-Indian.** C.N. 7677: Golombek called 'Bogo-Indian' a
  "hideous name" in The Encyclopedia of Chess (1977), p. 34, was caught by
  W.H. Cozens in BCM, September 1978, p. 401, for allowing "the exactly
  analogous Nimzo-Indian to pass without stricture", and the 1981 paperback
  dropped it. He had conceded the parallel in The Times, 5 February 1977.
- **`E.Bud` — Budapest.** C.N.s 5988 and 6571: the origin is disputed; the
  standard treatment is the Gyuricza and Bottlik chapter (pp. 37-48) in
  Jakobetz's bilingual booklet (Budapest, 2010), which sets Gyula Breyer
  against István Abonyi. **The chapter has not been read for this entry**,
  so the note records the dispute and points at the source without
  asserting an origin. The early monograph 'De Budapester Verdediging' by
  "St. Schwartz" (Antwerp, c. 1927) is recorded; its author is
  unidentified.

## Deliberate omissions and open questions

- **No attribution is added by this batch.** Every item documents naming
  history, an editorial quarrel, or an open dispute. Adding
  `attributed_to` for E.Bog or E.Bud on this evidence would assert an
  origin the sources explicitly leave unsettled.
- **Bottlik's forename** is given as "Iván" in the extracted C.N. 6571 text
  and as "István" in one summarising read of the same page; because
  "István Abonyi" appears in the same sentence, contamination is likely in
  one direction or the other. The note therefore uses the surname alone.
- **An editorial question for the catalogue, not a claim.** Golombek's
  Times column (C.N. 7677) records that the Reynolds variation of the
  Semi-Slav is called the Klaus Junge line by the Germans, and the Abrahams
  variation the Noteboom line by the Dutch. OCN currently carries Noteboom
  as the head with Abrahams and Junge as sub-variations
  (`D.Sla.Not.Abr`, `D.Sla.Not.Jun`), which encodes one national tradition
  as the parent of the others. Whether that hierarchy is right is a naming
  decision, not something a source batch should settle.

## Dry-run record

`--validate` and `--dry-run --strict` both exit 0 on 2026-08-02;
5,899 rows before and after, 6 rows changed.
