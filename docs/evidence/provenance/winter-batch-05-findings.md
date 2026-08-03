# Winter Chess Notes, batch 5: verification record

**Status: verified, un-applied.** Companion to
`docs/manifests/winter-batch-05.manifest.json`. Drafted 2026-08-02.

## One row, not five

The dossier presents a Marshall cluster spanning `C.RyL`, `D.Sem.Mar`,
`D.Tar.Mar` and `B.Fre.Nrm.d5.Nc3.c5`, with the same items repeated under
each. They are not the same opening. The Semi-Slav, Tarrasch and French
Marshall Gambits are distinct lines that happen to share an eponym; every
routed item here is about the **Ruy López** Marshall Attack. Writing notes
on the other three from this evidence would attach a Ruy López history to
openings it does not describe.

This is the routing behaviour the harvest side has already diagnosed and
supplemented: matching by name token pulls in every opening carrying the
same person's name. The supplement helps, but the drafting step still has
to check the moves, not the label.

## `C.RyL.Mar` — what Marshall did not keep secret

The row already records that the idea predates 1918 (Walbrodt, Havana
1893). What the batch adds is evidence bearing on the *legend* — that
Marshall hoarded the gambit for years to spring on Capablanca:

- **C.N. 6980** (winter80.html): Jaffe and Cleland v Marshall and
  Padelford, New York, circa 15 February 1918, a consultation game
  published in the **Brooklyn Daily Eagle of 7 March 1918, p. 6** — score
  located by Eduardo Bauzá Mercére, who notes Marshall was playing the
  gambit "many months before his encounter with Capablanca (which was
  played on 23 October 1918)", and even played the 16...h5 later debated
  in analysis. Eight months, in print, in a New York daily.
- **C.N. 6777** (winter74.html): the supporting citation usually offered
  for the secrecy story — that Marshall had seen a Frere v Marshall game
  published in 1917 — traces to A. Soltis, Chess Life, January 1983,
  p. 11, whose account Winter describes as "devoid of any sources". Winter
  reports finding that game nowhere before Marshall's own *Comparative
  Chess* (Philadelphia, 1932), which printed it **undated**.

The note is worded to record what the sources show — public play in
February 1918, and an unsourced 1917 claim — without asserting the
opposite legend in its place. Whether Marshall regarded it as a surprise
is not something these documents settle; whether it was unpublished is.

## Considered and not drafted

- **C.N. 3980**: Kasparov's *My Great Predecessors* says Capablanca was
  "not reckoning on" 15...h5, whereas Capablanca's own notes in the New
  York 1918 tournament book, p. 12, suggested it ("15...h5 was perhaps the
  best way to keep up the pressure") before dropping it from *My Chess
  Career*. A genuine annotation-history correction, but about a game's
  analysis rather than a name, so it belongs to a games layer the
  catalogue does not yet have.
- **C.N. 11754**: Shipley's column in the Philadelphia Inquirer, 6 March
  1938, p. 8A, carries a comment on the Marshall Gambit pre-1918 that
  Winter calls noteworthy — but it is reproduced as a facsimile image and
  its text is not in the extract, so nothing was drafted from it. Worth a
  look by eye if the Marshall question is revisited.
- **C.N. 5664**: concerns the Walbrodt consultation game already cited in
  the existing note; it corrects the venue and the spelling of Ostolaza's
  name, which the catalogue does not record either way.

## Dry-run record

`--validate` and `--dry-run --strict` both exit 0 on 2026-08-02;
5,899 rows before and after, 1 row changed.
