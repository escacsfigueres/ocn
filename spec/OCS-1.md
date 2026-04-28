# OCS-1 — Open Chess Slug, version 1

**Status**: Draft v0.1 · 2026-04-28
**Author**: Club d'Escacs Figueres
**License**: CC-BY-4.0 (this document and the catalogue)
**Repository**: https://github.com/escacsfigueres/ocs

## Why OCS

The Encyclopaedia of Chess Openings (ECO), introduced by Šahovski Informator
in 1971, has been the de facto naming standard for chess openings for
50+ years. ECO has aged remarkably well in one respect: the **A/B/C/D/E**
top-level classification captures the fundamental structural divide of
chess openings, and any new opening fits cleanly into one of those five
families.

ECO has aged poorly in another respect: the 100 sub-codes within each
letter (`A00`–`E99`) are arbitrary, frozen in 1971, distributed by what was
fashionable then, and offer no parent-child hierarchy. Knowing that "B33"
is the Sveshnikov, "E97" is the King's Indian Classical, and "C67" is the
Ruy López Berlin Endgame is a feat of memorisation that does not benefit
the player learning openings or the database designer running queries.

OCS-1 is **a hierarchical companion to ECO**, not a replacement. It keeps
the A/B/C/D/E top-level classification — that is the part of ECO that
deserves to live another 50 years — and replaces the arbitrary 00-99
sub-code with a small, human-readable, hierarchical slug.

## Goals

1. **Memorable**. A player should be able to read `B.Sic.Naj.Eng` once
   and never need to look it up.
2. **Hierarchical**. Parent-child relationships are explicit. All Sicilian
   lines start with `B.Sic`.
3. **Compatible**. Every OCS-1 slug carries a back-reference to its ECO
   code(s). ECO is preserved in the catalogue as `eco_legacy`.
4. **Open**. The specification and the catalogue are CC-BY-4.0. Anyone may
   adopt OCS-1 in their own database, book or product.
5. **Stable**. Once a slug is published in a tagged release, it MUST NOT
   change meaning. New openings extend the catalogue; existing entries are
   amended only via aliases or deprecation, never by re-pointing.

## Format

```
<class> "." <family> [ "." <variation> [ "." <subline> [ "." <move> [ "." <move> ] ] ] ]
```

| Position | Length | Case | Examples |
|---|---|---|---|
| `class` | 1 char | uppercase A/B/C/D/E | `A`, `B`, `C`, `D`, `E` |
| `family` | 3 chars | TitleCase or known ALLCAPS abbreviation | `Sic`, `Fre`, `RyL`, `KID`, `QGD` |
| `variation` | 3 chars | TitleCase | `Naj`, `Sve`, `Mar`, `Tar`, `Sml` |
| `subline` | 3 chars | TitleCase | `Eng`, `End`, `Ope`, `Cls` |
| `move` | 2-4 chars | SAN-style, capitalised pieces | `Be3`, `e5`, `Bxf6`, `O-O` |

Total length is bounded: maximum 4 segments after the class give 1 + 3×4 = 13 characters.
Adding two `move` segments brings the practical maximum to ~20 characters.

### Class assignment

The class is derived from the position **after the principal opening
moves of the variation**, not from a single rigid rule. The intent is:

- **A** — Flank openings: any line that does not start with 1.e4 or with
  1.d4 followed by an early 2.c4. Includes Réti, English, Bird, Larsen,
  the Dutch family, Trompowsky, Benoni, and other "non-classical" centre
  treatments.
- **B** — Semi-Open: 1.e4 followed by **any reply other than 1...e5**.
  Includes Sicilian, Caro-Kann, French, Pirc, Modern, Alekhine,
  Scandinavian.
- **C** — Open: 1.e4 e5 (symmetric king-pawn). Includes Ruy López, Italian,
  Petrov, Scotch, Vienna, King's Gambit and the rest of the Open Games.
- **D** — Closed Queen's Pawn: 1.d4 d5 (symmetric queen-pawn) or any line
  in which Black plays an early ...d5. Includes Queen's Gambit (declined,
  accepted), Slav, Semi-Slav, Catalan (Black plays ...d5; otherwise see
  below), Tarrasch, Albin.
- **E** — Indian: 1.d4 Nf6 with Black declining ...d5 in the early
  middlegame. Includes King's Indian Defence, Nimzo-Indian, Queen's
  Indian, Bogo-Indian, Old Indian, Grünfeld, Catalan-without-d5.

The class is a property of the **OCS-1 slug**, not of the literal
move-order that produced it. Two transposing move-orders that converge to
the same canonical position therefore share the same OCS-1 slug.

#### Borderline rules

- **Catalan**: classified `D` only when Black plays ...d5 within the first
  five moves. Without ...d5 (e.g. King's Indian setup against the Catalan
  bishop) the position is classified `E`. Spec rationale: Catalan is
  defined by the structural fight for d5; without that fight, the position
  belongs in the Indian family.
- **Grünfeld**: classified `E` even though some legacy ECO codes place it
  in the D range. Spec rationale: Grünfeld is structurally an Indian
  defence (1.d4 Nf6 first), and grouping it with the Indian family makes
  the parent-child hierarchy clean.
- **Queen's Gambit Accepted**: `D.QGA`. Black plays ...d5 then ...dxc4.
  Stays in D.
- **Benoni**: `A.Ben`. The 2...c5 reply against 1.d4 declines the d5/c4
  symmetry; it is a flank treatment of the centre.

### Family abbreviation rules

When abbreviating a family or variation name to 3 characters:

1. **Preserve a vowel** if possible. Prefer `Naj` over `Njd`,
   `Sve` over `Svs`, `Tar` over `Trt`.
2. **Use the first three pronounceable characters** of the name, accents
   dropped (`Sml` for Sämisch, `Gru` for Grünfeld).
3. **Honour established acronyms**: `KID`, `QGD`, `QGA`, `QID`, `NID`,
   `OID`, `RyL` (Ruy López — the y is preserved because the
   pronunciation collapses into "Roo-Ee-Lo-Pez").
4. **Avoid collisions within the same parent**. If two children of the
   same parent both want `Cla`, the second uses a different abbreviation
   (`Clo`, `Csc`, …) and the choice is documented in the catalogue.

Display names (`canonical_name`) keep the original spelling, including
accents, punctuation and full words: `Sicilian Defence: Sämisch
Variation`. The 3-letter slug is purely for compact reference.

### `move` segments — the depth tail

For lines that are routinely identified by a specific tabiya beyond the
named variation, append literal SAN moves (capitalised pieces, no
file/rank disambiguation) separated by dots:

```
B.Sic.Naj.Eng.Be3.e5     6.Be3 e5 main line of the English Attack
B.Sic.Naj.Eng.Be3.e6     6.Be3 e6 Scheveningen-style
B.Sic.Sve.Nd5            11.Nd5 main Sveshnikov tabiya
B.Sic.Sve.Nd5.Nb8        Nb8 retreat under 11.Nd5
C.RyL.Ber.End.dxe5       After ...dxe5 in the Berlin Endgame
```

Castling is `O-O` (kingside) or `O-O-O` (queenside). Captures use `x`.
Promotions: `=Q`. Check (`+`) and mate (`#`) are not part of the slug —
they describe the move, not the variation.

The depth tail is appended only when the SAN move is **the canonical tabiya
that opening literature attaches a name to**. Random middlegame moves do
not become OCS-1 slugs.

### Maximum depth

The catalogue MUST NOT contain entries with more than 6 dots (i.e. 7
segments). The recommended cap is 5 segments for everyday lines, and 7
only for legendary tabiyas. Beyond that, identify the position by Zobrist
hash, not by slug.

## Catalogue

The reference catalogue is `catalog/ocs-1.csv`. Each row has the columns:

| Column | Type | Description |
|---|---|---|
| `ocs1` | string | The slug (primary key). |
| `canonical_name` | string | Full human-readable name with accents and punctuation. |
| `eco_legacy` | string | Pipe-separated ECO codes that this slug covers (`B90`, or `B90\|B91`). |
| `parent_ocs1` | string null | Parent slug. NULL for class roots like `A`. |
| `depth` | int | 0 for class roots, increments by 1 per dot. |
| `aliases` | string null | Pipe-separated alternative names (Lasker–Pelikan, etc.). |
| `flags` | string null | Comma-separated tags: `gambit`, `sharp`, `closed`, `endgame`, `theoretical`. |
| `notes` | string null | Free text explaining edge cases or borderline classification. |

The catalogue is normative for the slugs it contains. Tools and consumers
SHOULD look up unknown ECO codes by querying the catalogue with
`eco_legacy LIKE '%<code>%'`.

## Versioning

OCS-1 follows semantic versioning at the catalogue level:

- **Patch** (1.0.x): clarifications, typo fixes, alias additions.
- **Minor** (1.x): new entries that do not change the meaning of existing
  slugs. New `flags` values. Breaking format changes in the spec are NOT
  allowed in a minor version.
- **Major** (2.x): changes to the slug format itself.

Once a release is tagged, an entry's `ocs1` MUST NOT be re-pointed to a
different position. If a slug is found to be wrong, mark it `deprecated`
in `flags` and add the correct slug as a new entry.

## Examples

The full canonical example set lives in `catalog/ocs-1.csv`. A few
illustrative ones:

| OCS-1 | ECO | Canonical name |
|---|---|---|
| `A.Eng.Sym` | A30–A39 | English Opening, Symmetrical Variation |
| `A.Hol.Lng` | A87–A89 | Dutch Defence, Leningrad Variation |
| `A.Tro` | A45 | Trompowsky Attack |
| `B.Sic` | B20–B99 | Sicilian Defence |
| `B.Sic.Naj` | B90–B99 | Sicilian Defence, Najdorf Variation |
| `B.Sic.Naj.Eng` | B90 | Sicilian Najdorf, English Attack |
| `B.Sic.Naj.Eng.Be3.e5` | B90 | Najdorf English Attack, 6.Be3 e5 |
| `B.Sic.Sve` | B33 | Sicilian Sveshnikov (Lasker–Pelikan) |
| `B.CaK.Adv` | B12 | Caro-Kann, Advance Variation |
| `B.Fre.Win` | C15–C19 | French Defence, Winawer Variation |
| `C.RyL.Ber.End` | C67 | Ruy López, Berlin Defence, Endgame |
| `C.Ita.Evn` | C51 | Italian, Evans Gambit |
| `C.Pet` | C42 | Petrov Defence |
| `D.QGD.Tar` | D58–D59 | Queen's Gambit Declined, Tartakower |
| `D.Sla.Mer` | D47 | Slav, Semi-Slav, Mèran Variation |
| `D.Cat.Ope` | E04–E05 | Catalan, Open Variation |
| `E.KID.Sml` | E80–E89 | King's Indian Defence, Sämisch Variation |
| `E.Nim.Cls` | E32–E33 | Nimzo-Indian, Classical Variation |
| `E.Gru.Exc` | D85 | Grünfeld, Exchange Variation |

## Acknowledgements

OCS-1 builds on the work of:

- Šahovski Informator (1971) for the A/B/C/D/E classification.
- Lichess Chess Openings (CC0) for canonical English names.
- Hooper & Whyld, *Oxford Companion to Chess* (1984) for canonical name
  conventions.
- The community of chess players, coaches and database authors who have
  pointed out the limits of ECO for half a century.
