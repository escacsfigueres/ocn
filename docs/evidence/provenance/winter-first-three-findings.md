# Winter Chess Notes, first three: verification record

**Status: verified, un-applied.** Companion to
`docs/manifests/winter-first-three.manifest.json`. Batch drafted 2026-08-02.

## Provenance chain

Leads were surfaced by the external harvest pipeline (Chess Notes pass of
2026-08-02, grade `lead-only` at harvest time). Every C.N. item below was
then **re-read first-hand at chesshistory.com on 2026-08-02** before
drafting; the quotes in this file are from that first-hand reading, not
from the harvest. The sources cited in the manifest are the published
primaries and Winter's numbered items. Edward Winter's Chess Notes is an
established source for this catalogue (precedent: the Maróczy Bind
attributions, applied 2026-05-31, "verified first-hand").

## `B.CaK` — Caro-Kann Defence

- **C.N. 7249** (winter86.html): Chess Monthly, September 1888, pp. 25-26,
  annotation to Bird & Blackburne v von Bardeleben & Weiss (Bradford):
  "This move was introduced by the late Herr Kann, of Pest, and adopted in
  practice by Herr Caro, of Berlin. It gives a safe but dull game."
  BCM, October 1888, pp. 411-412 (W.H.K. Pollock): "The Field observes
  that it was introduced by Herr Kann, of Pesth, and practised by Herr
  Caro, of Berlin."
- **C.N. 8423** (winter113.html): A. Csánk, Wiener Schachzeitung,
  1 September 1887 (pp. 49-52) and 1 October 1887 (pp. 73-75); per
  Thomas Niessen's summary, Csánk reports Marcus Kann "was the first to
  apply the defence", and that Csánk, Ja[c]ques Schwarz and M. Weiss
  analysed it before Weiss played it at Nuremberg, 1883.
- **C.N. 7017** (winter80.html): earliest 1...c6 found so far, unnamed
  players, Chess Player's Chronicle, 1845 (not 1846), pp. 336-337.
- **C.N. 9431** (winter133.html): earlier Kann specimen, A. Csánk v
  M. Kann, Vienna, 13 February 1884, published in Allgemeine
  Sport-Zeitung, 7 August 1884.

Roles chosen from the catalogue's existing vocabulary: Kann `originator`
(the primaries say "introduced by" and "first to apply"), Caro `leading
practitioner` ("adopted in practice by", "practised by").

**What this batch does not claim:** who coined the compound name
"Caro-Kann" or when it first appeared in print; the 1888 annotations
attribute the *move*, not the label. C.N. 7249's later paragraphs on the
name's first occurrences are left for a follow-up once read in full.

## `E.Ben` — Benoni Defence

- **C.N. 4435, reproducing C.N. 2250** (winter23.html): the name comes
  from Hebrew ben-oni, "child/son of (my) sorrow/sadness"; Staunton's
  Chess-Player's Companion p. 318 note cites "Benoni, oder [die]
  Vertheidigungen [gegen] die Gambitzüge im Schache, etc. Von Aaron
  Reinganum, Frankfort, 1825". Documented confusions: Rey Ardid, Cien
  nuevas partidas de ajedrez (Saragossa, 1940), p. 22 ("the English
  player Benoni"); O'Kelly, L'intuition à l'affût (two 1830s brothers).
  C.N. 4435 adds Avital Pilpel's note that by Hebrew stress the reading
  "son of my strength" also exists (Taharut Amanim be'Sachmat, 1952).

`attributed_to` stays empty: the name's basis is a book title, not a
person (precedent: `D.QGD.Exc.Car`, Carlsbad, non-person basis with
historical_notes only). Note for the vocabulary backlog: `name_basis`
currently knows `review / descriptor / person`; the Benoni suggests a
fourth basis class (work or phrase). Not introduced unilaterally here.

## `C.PhD` — Philidor Defence

- **C.N. 9220** (winter129.html): Chernev, Curious Chess Facts (New York,
  1937), p. 14: "Philidor never played Philidor's Defence!"; D.J. Morgan,
  BCM, May 1954, p. 157 ("Philidor, it is said, never played the Philidor
  Defence"); W.S. Mackie's letter, BCM, August 1954, p. 257, asking when
  the name was first attached to 1 e4 e5 2 Nf3 d6.

`attributed_to` stays empty: the evidence documents an open question about
the name's attachment, not an attribution act. Writing "Philidor (eponym)"
here would assert more than the quotes prove.

## Adversarial re-test, round 1 (2026-08-02 afternoon)

Run against the external re-test brief (retest-brief-01). Verdicts on this
batch's pieces:

- **Benoni = Reinganum title: survives, strengthened and corrected.** A
  contemporary 1825 review located in a Jena journal (JPortal,
  jparticle_00195775) fixes the exact title: "Ben-Oni oder die
  Vertheidigungen gegen die Gambitzüge im Schache ... Frankfurt am Main:
  Hermann 1825" — hyphenated Ben-Oni; Staunton's rendering was loose. The
  manifest was corrected accordingly. The treatise covers defences to the
  King's and Queen's Gambits generally plus the then-unknown 1.d4 c5, so
  "the treatise = Old Benoni" would overstate; this batch never claimed
  it. No pre-1825 chess use of "Benoni" surfaced. Reinganum's identity
  (Frankfurt Jewish community figure) remains a people-candidate task: no
  QID located yet.
- **Kann identity: resolved.** Marcus Kann, Wikidata Q86090, Vienna 1820 -
  Vienna 3 Feb 1886. The Chess Monthly's "of Pest" is a discrepancy of
  that primary (Steinitz's "de Vienne" was right); noted in the manifest's
  historical_notes. The quote itself stands as a quote.
- **Compound name "Caro-Kann": verified at Winter first-hand.** C.N. 7249's
  later paragraphs: the joint title first appears in Curt von Bardeleben's
  article, Deutsche Schachzeitung, July 1890, pp. 193-195; Brüderschaft
  1886 headed Caro's games "Caro's Eröffnung" / "Unregelmässige
  Eröffnung". Winter also documents the Brace 1977 and Oxford Companion
  errors. Added to the manifest's historical_notes. An independent
  pre-July-1890 sweep (ANNO, Google Books) stays open before upgrading to
  "verified at primary".
- **Philidor: survives as drafted.** This batch asserts only the Chernev
  quote and the open question. The name itself is plainly older than 1937
  (a dated earliest-attachment via Staunton's Handbook 1847 is an open
  Internet Archive task); no recorded Philidor game with 2...d6 surfaced
  to falsify Chernev.
- **E.Bud's two existing claims** (named-after-place, renamed): both
  survive; they assert the name-carries-place and a documented Lichess
  rename, neither of which the Budapest-origin primaries touch.

## Dry-run record

`--validate` and `--dry-run --strict` both exit 0 on 2026-08-02;
5,899 rows before and after, 3 rows changed, catalogue sha256
`711da9c5...` -> `bd17984d...`.
