# OCN-1 — Open Chess Naming, version 1

**Status**: Draft v0.1 · 2026-04-28
**Author**: Club d'Escacs Figueres
**License**: CC-BY-4.0 (this document and the catalogue)
**Repository**: https://github.com/escacsfigueres/ocn

## Why OCN

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

OCN-1 is **a hierarchical companion to ECO**, not a replacement. It keeps
the A/B/C/D/E top-level classification — that is the part of ECO that
deserves to live another 50 years — and replaces the arbitrary 00-99
sub-code with a small, human-readable, hierarchical slug.

## Goals

1. **Memorable**. A player should be able to read `B.Sic.Naj.Eng` once
   and never need to look it up.
2. **Hierarchical**. Parent-child relationships are explicit. All Sicilian
   lines start with `B.Sic`.
3. **Compatible**. Every OCN-1 slug carries a back-reference to its ECO
   code(s). ECO is preserved in the catalogue as `eco_legacy`.
4. **Open**. The specification and the catalogue are CC-BY-4.0. Anyone may
   adopt OCN-1 in their own database, book or product.
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
| `move` | 1-6 chars | SAN-style, check/mate stripped | `Be3`, `e5`, `Bxf6`, `O-O`, `O-O-O` |

Total depth is bounded at 6 dots / 7 segments. Named segments are normally
3-character tokens; up to two trailing SAN move segments may extend the
slug when a named tabiya needs move-level precision.

### Class assignment

The class is derived from the position **after the principal opening
moves of the variation**, not from a single rigid rule. The intent is:

- **A** — Flank openings: lines outside 1.e4 and outside the main
  1.d4/2.c4 Indian-defence complex. Includes Réti, English, Bird,
  Larsen, the Dutch family, Trompowsky, and other "non-classical" centre
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
- **E** — Indian: 1.d4 Nf6 with Black defining the game by an Indian
  piece setup or hypermodern central strike rather than by the classical
  1...d5 queen-pawn symmetry. Includes King's Indian Defence,
  Nimzo-Indian, Queen's Indian, Bogo-Indian, Old Indian, Grünfeld,
  Benoni/Benko, and Catalan-without-d5.

The class is a property of the **OCN-1 slug**, not of the literal
move-order that produced it. Two transposing move-orders that converge to
the same canonical position therefore share the same OCN-1 slug.

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
- **Budapest / Fajarowicz**: `E.Bud`. The legacy ECO codes are `A51` and
  `A52`, but `1.d4 Nf6 2.c4 e5` is an Indian countergambit against the
  d4/c4 complex, so it belongs with the Indian defences rather than with
  flank openings.
- **Queen's Gambit Accepted**: `D.QGA`. Black plays ...d5 then ...dxc4.
  Stays in D.
- **Benoni / Benko**: `E.Ben`. Even though the legacy ECO range is `A43`
  and `A56`-`A79`, the main Benoni and Benko families arise from
  `1.d4 Nf6 2.c4 c5` Indian move-orders and should live beside King's
  Indian and Grünfeld structures. Immediate Old Benoni move-orders
  without ...Nf6 stay in the same family to avoid splitting a single
  named opening across classes.

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
named variation, append literal SAN moves separated by dots. Check (`+`)
and mate (`#`) are stripped. File/rank disambiguation is allowed when SAN
requires it. The grammar permits up to two trailing move segments:

```
B.Sic.Sve.Nd5            11.Nd5 main Sveshnikov tabiya  (one move)
B.Sic.Sve.Bxf6           9.Bxf6 line                    (one move)
B.Sic.Naj.Eng.Be3.e5     6.Be3 e5 main line of the English Attack  (two moves)
B.Sic.Naj.Eng.Be3.e6     6.Be3 e6 Scheveningen-style                (two moves)
C.RyL.Ber.End.dxe5       After ...dxe5 in the Berlin Endgame        (one move)
```

Examples like `B.Sic.Naj.Eng.Be3.e5` are illustrative of the grammar. The
0.1 reference catalogue does not yet enumerate every depth-5 tabiya; the
catalogue grows as the community contributes lines that meet the
"named-tabiya" bar (see below).

Castling is `O-O` (kingside) or `O-O-O` (queenside). Captures use `x`.
Promotions: `=Q`. Check (`+`) and mate (`#`) are not part of the slug —
they describe the move, not the variation.

The depth tail is appended only when the SAN move is **the canonical tabiya
that opening literature attaches a name to**. Random middlegame moves do
not become OCN-1 slugs.

### Maximum depth

The catalogue MUST NOT contain entries with more than 6 dots (i.e. 7
segments). The recommended cap is 5 segments for everyday lines, and 7
only for legendary tabiyas. Beyond that, identify the position by Zobrist
hash, not by slug.

## Catalogue

The reference catalogue is `catalog/ocn-1.csv`. Each row has the columns:

| Column | Type | Description |
|---|---|---|
| `ocn1` | string | The slug (primary key). |
| `canonical_name` | string | Full human-readable name with accents and punctuation. |
| `eco_legacy` | string | Pipe-separated ECO codes that this slug covers (`B90`, or `B90\|B91`). |
| `parent_ocn1` | string null | Parent slug. NULL for class roots like `A`. |
| `moves_uci` | string null | Canonical UCI move sequence reaching the slug's reference position (space-separated, e.g. `e2e4 c7c5 g1f3 d7d6 d2d4 c5d4 f3d4 g8f6 b1c3 a7a6`). NULL for class roots, which are filters, not positions. |
| `depth` | int | 0 for class roots, increments by 1 per dot. |
| `aliases` | string null | Pipe-separated alternative names (Lasker–Pelikan, etc.). |
| `flags` | string null | Pipe-separated tags from the closed set `{gambit, sharp, closed, endgame, theoretical, deprecated}`. |
| `notes` | string null | Free text explaining edge cases or borderline classification. |
| `attributed_to` | string null | Player(s), school, or event the opening is associated with. Free text. |
| `attribution_source` | string null | Citation supporting `attributed_to`. **Required** when `attributed_to` is non-empty — the validator rejects unsourced claims. Free text but should reference a book, an article, a tournament game, or a corpus signal. |
| `historical_notes` | string null | Longer-form context (transmission history, popularisation, calibration against the corpus). |
| `transposes_to` | string null | Slug of the FEN-canonical OCN-1 entry that owns this position. Set when this row is a move-order transposition of another. NULL when this row is itself canonical. See "Canonicalisation by position" below. |

The three attribution columns form the catalogue's "Layer 2" — curated,
human-asserted history. They sit alongside the corpus-derived `Layer 1`
table `opening_provenance` (EFCDB-v1 Table 8), which stores
machine-recomputable signals (first/last game, top players, total
games). Joining the two by `ocn1` lets a reader see what the literature
claims AND what the corpus shows, and notice when they disagree.

Producers MAY emit a derived `zobrist` (INT64) column alongside the
catalogue when serialising to a position-indexed format. The reference
toolchain (`escacsfigueres/chess-parquet`'s `efcdb-openings` crate)
replays `moves_uci` from the standard initial position and writes the
Polyglot Zobrist hash into `openings.parquet`. Consumers can then JOIN
`openings.zobrist` against any position-indexed dataset directly.

The OCN repository also provides a lightweight derived export:
`tools/export_positions.py` emits one row per concrete catalogue entry
with `fen_key` (board, turn, castling, legal en-passant), canonical
counter-normalised `fen` (`fen_key 0 1`), and
`transposition_group_size`. This export is for audit and text workflows;
the Polyglot `zobrist` contract remains the EFCDB/openings artefact.

### Canonicalisation by position (`transposes_to`)

OCN-1 has two distinct relations between slugs:

- **`parent_ocn1`** is the **nominal hierarchy**. It groups slugs by
  literature lineage and lets a human reader navigate from a family
  root (`A.Kan`, `E.Nim`) down to a specific tabiya. The parent chain
  is what produces a readable slug.
- **`transposes_to`** is **canonicalisation by position**. It points
  from a slug whose FEN coincides with another slug's FEN to that
  other slug — the FEN-canonical one. It does not change the
  parent-child tree.

Many openings are reached by more than one move order. OCN-1 keeps
each named move order alive (so a reader following the Kangaroo
literature can still find the Kangaroo entries) but records on each
non-canonical entry that the position **is** another OCN-1 slug by
FEN. Consumers building a position index SHOULD treat
`transposes_to` as the canonicalisation arrow: when resolving a FEN
to OCN-1, follow `transposes_to` once and report the target slug.

Contract:

- `transposes_to` is a single `ocn1` value or NULL.
- It MUST differ from `ocn1`.
- The target MUST exist in the catalogue.
- The target MUST NOT be a class root (class roots are filters, not
  positions).
- Class roots themselves MUST NOT carry `transposes_to`.
- When both rows have `moves_uci`, their FEN keys (board + side to
  move + castling + en-passant) MUST match. The validator rejects
  rows whose declared transposition does not hold by FEN.
- `transposes_to` does not replace `aliases` or `notes`. Aliases
  preserve human-readable alternate names; notes capture move-order
  context. `transposes_to` makes the relation computable.

A duplicate FEN group is "resolved" when exactly one entry has empty
`transposes_to` (the canonical) and every other entry points into
the group with `transposes_to`. `tools/audit_transpositions.py`
hides resolved groups by default and surfaces them with
`--include-resolved`.

### Looking up a slug from an ECO code

A single ECO code can map to several OCN-1 slugs (e.g. `B90` covers the
Najdorf family root and several depth-3 lines). Tools resolving "ECO →
OCN-1" SHOULD apply the **deepest-match** rule:

1. Filter rows whose `eco_legacy` contains the queried code.
2. Among those, pick the row with the highest `depth` whose path is
   consistent with the available context (e.g. the move list).
3. If multiple rows tie at the same depth, the consumer SHOULD report
   the ambiguity rather than silently picking one.

When precise matching matters (preparation, novelty hunting,
move-order-aware analysis) consumers SHOULD JOIN by `zobrist` against a
position-indexed dataset rather than rely on ECO at all. ECO is a coarse
filter; the canonical zobrist is the unambiguous identifier.

## Versioning

OCN-1 follows semantic versioning at the catalogue level:

- **Patch** (1.0.x): clarifications, typo fixes, alias additions.
- **Minor** (1.x): new entries that do not change the meaning of existing
  slugs. New `flags` values. Breaking format changes in the spec are NOT
  allowed in a minor version.
- **Major** (2.x): changes to the slug format itself.

Once a release is tagged, an entry's `ocn1` MUST NOT be re-pointed to a
different position. If a slug is found to be wrong, mark it `deprecated`
in `flags` and add the correct slug as a new entry.

## Examples

The full canonical example set lives in `catalog/ocn-1.csv`. A few
illustrative ones:

| OCN-1 | ECO | Canonical name |
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
| `D.Sla.Sem.Mer` | D47 | Slav, Semi-Slav, Mèran Variation |
| `D.Cat.Ope` | E04–E05 | Catalan, Open Variation |
| `E.KID.Sml` | E80–E89 | King's Indian Defence, Sämisch Variation |
| `E.Nim.Cls` | E32–E33 | Nimzo-Indian, Classical Variation |
| `E.Gru.Exc` | D85 | Grünfeld, Exchange Variation |

## Lichess long-tail integration

OCN-1 is intentionally curated and compact — it names 2,025 important
opening families, variations, and tabiyas that humans can memorise. It
does NOT attempt to name every line that ever appeared in a game.

For the long tail (Bird's Australian Variation, Polish Sokolsky
Defended, Englund Gambit Complex…), consumers SHOULD layer the Lichess
Opening Book (`lichess-org/chess-openings`, CC0) on top of OCN-1:

1. Resolve a position to OCN-1 first via `positions.zobrist =
   openings.zobrist`.
2. If no OCN-1 match, fall back to the Lichess catalogue keyed by the
   same Polyglot Zobrist.
3. Lichess entries carry a `parent_ocn1` field — the deepest OCN-1
   ancestor of that line — so even unnamed-by-OCN positions can be
   shown grouped under a familiar OCN-1 family.

The reference EFCDB toolchain provides this layering as Table 6
(`lichess_openings`); see the EFCDB-v1 spec for the schema and the
join recipe. With both tables loaded, every position in a real game
database can be resolved to a name: curated OCN-1 names first, and then
Lichess's CC0 names with an OCN-1 family as breadcrumb.

The repository includes `tools/lichess_parent_map.py` as a lightweight
CSV/TSV bridge: it converts Lichess SAN PGN lines to UCI and assigns the
deepest OCN-1 parent by move-prefix match.

## Acknowledgements

OCN-1 builds on the work of:

- Šahovski Informator (1971) for the A/B/C/D/E classification.
- Lichess Chess Openings (CC0) for canonical English names.
- Hooper & Whyld, *Oxford Companion to Chess* (1984) for canonical name
  conventions.
- The community of chess players, coaches and database authors who have
  pointed out the limits of ECO for half a century.
