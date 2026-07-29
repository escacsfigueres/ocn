# OCN — Open Chess Naming

[![CI](https://github.com/escacsfigueres/ocn/actions/workflows/ci.yml/badge.svg)](https://github.com/escacsfigueres/ocn/actions/workflows/ci.yml)
[![Spec license: CC BY 4.0](https://img.shields.io/badge/spec-CC%20BY%204.0-lightgrey.svg)](LICENSE-SPEC)
[![Code license: MIT](https://img.shields.io/badge/code-MIT-blue.svg)](LICENSE-CODE)
[![Release](https://img.shields.io/badge/release-ocn--1.2.0-blue.svg)](#status)

**OCN** is a hierarchical, human-readable naming scheme for chess
openings, designed as a companion to ECO (the *Encyclopaedia of Chess
Openings* code system that has been the de facto standard since 1971).
OCN keeps the best idea in ECO — the five structural families A/B/C/D/E —
and replaces the arbitrary 100-codes-per-letter sub-numbering with short,
parent-aware slugs.

## At a glance

| ECO | OCN-1 | Canonical name |
|---|---|---|
| `B33` | `B.Sic.Sve` | Sicilian Sveshnikov |
| `B90` | `B.Sic.Naj.Eng` | Najdorf English Attack |
| `C67` | `C.RyL.Ber.Wal.End` | Ruy López, Berlin Wall Endgame |
| `D47` | `D.Sem.Mer` | Semi-Slav, Meran |
| `E97` | `E.KID.Cls.Mar` | KID Classical, Mar del Plata |

Read once, remember forever. No lookup table needed.

## Why

ECO has aged remarkably well in one respect: A/B/C/D/E captures the
fundamental structural divide of chess openings (semi-open vs open vs
closed vs Indian vs flank) and any new opening fits cleanly into one of
those five families. **OCN keeps that idea. It does not keep every one of
ECO's letter assignments.** 770 rows — 13.8% of the rows that carry an ECO
code — sit in an OCN class that is not among their own ECO letters, always
for a structural reason: the French is `B`, the London and Colle systems
are `A`, the Grünfeld and Benoni are `E`. The full breakdown is in
[`docs/ocn-audit-2026-07.md`](docs/ocn-audit-2026-07.md#5-classification-honesty)
(section 5) until the derived divergence sidecar ships (roadmap H2.5); the
main cases are argued under "Borderline classifications" below.

ECO has aged poorly in another respect: the 00-99 sub-codes within each
letter were assigned in 1971 according to what was fashionable at the
time, distribute coverage unevenly (the Sicilian alone gets 80 codes,
the irregulars share 19), and offer no parent-child hierarchy. Knowing
that "B33 = Sveshnikov" or "C67 = Berlin Endgame" is a feat of
memorisation that benefits no one — neither the player who wants to
study an opening, nor the database designer running queries.

OCN replaces that 50-year-old sub-numbering with hierarchical slugs:

```
B              ← top level (structural family)
B.Sic          ← family (Sicilian)
B.Sic.Naj      ← variation (Najdorf)
B.Sic.Naj.Eng  ← sub-line (English Attack, 6.Be3)
```

For specific named tabiyas the slug may carry one or two trailing SAN
moves (`B.Sic.Sve.Nd5` for the 11.Nd5 main line). See the spec for the
full grammar; for everyday use the four levels above are enough.

You can read the slug at any depth and immediately know:

- The **structural class** of the position (`B` = semi-open).
- The **family** (`Sic` = Sicilian).
- The **variation** (`Naj` = Najdorf).
- And, if you want the precision, the **exact tabiya** down to the
  signature SAN move that defines it.

## Format

```
<class> "." <family> [ "." <variation> [ "." <subline> [ "." <move> [ "." <move> ] ] ] ]
```

- **`class`**: 1 char from `A B C D E` (ECO's five families; see
  "Borderline classifications" for where OCN's letter differs from ECO's).
- **`family`**: 3 chars, TitleCase (`Sic`, `RyL`, `KID`).
- **`variation`** / **`subline`**: 3 chars each, TitleCase (`Naj`, `End`).
- **`move`**: SAN-style, capitalised pieces (`Be3`, `e5`, `Bxf6`, `O-O`).
  Up to two trailing move segments are allowed.
- **Separator**: dot `.`.
- **Maximum depth**: 6 dots / 7 segments. Recommended cap is 5 segments
  for everyday use; deeper slugs are reserved for legendary tabiyas.

The full specification is in [`spec/OCN-1.md`](spec/OCN-1.md).

## Status

**Released — `ocn-1.2.0` (2026-06-11).** The format is stable; the reference
catalogue has 5,899 entries, every duplicate-FEN group is resolved
(`unresolved_groups=0`), canonical names carry their true diacritics, the
ECO legacy codes are audited, and CI runs strict legal-move/SAN validation
plus the full tool test suite under an unconditional gate. Release notes:
[`docs/release-ocn-1.2.0-notes.md`](docs/release-ocn-1.2.0-notes.md). Post-1.2
work adds internationalised alias sidecars and consumer tooling, planned in
[`docs/traction-roadmap.md`](docs/traction-roadmap.md). Comments,
corrections and additions welcome via issues.

> Naming history: previously drafted as **OCS — Open Chess Slug** during
> alpha. Renamed to OCN before public release because "slug" carries
> different connotations outside web-development circles. The format
> itself is unchanged.

## Catalogue

The reference catalogue lives in [`catalog/ocn-1.csv`](catalog/ocn-1.csv)
— 14 columns per row:

- `ocn1` — the OCN-1 string (primary key)
- `canonical_name` — the canonical English name
- `eco_legacy` — the ECO codes it covers
- `parent_ocn1` — the parent slug (nominal hierarchy)
- `moves_uci` — the defining move sequence in UCI notation
- `depth` — the depth in the hierarchy
- `aliases` — known aliases (Sveshnikov a.k.a. Lasker–Pelikan)
- `flags` — tags from the closed set `gambit`, `sharp`, `closed`,
  `endgame`, `theoretical`, `deprecated`
- `notes` — free-text notes for borderline classifications
- `attributed_to`, `attribution_source`, `historical_notes` — sourced
  naming attributions (who an opening is named for, with the citation;
  every non-empty `attributed_to` must carry a source)
- `transposes_to`, `same_as` — position-identity relations (see
  "Three relations per slug" below)

The catalogue is licensed under **CC-BY-4.0**: you may use, share and
adapt it for any purpose, including commercial, provided you cite "Club
d'Escacs Figueres" and link to this repository.

## Tools

Everything is Python 3 standard library — no third-party dependency, no
build step (chess legality is checked by the in-repo move generator,
[`tools/chess_uci.py`](tools/chess_uci.py)). Recipes
and join patterns for consumers are in
[`docs/consuming-ocn-0.2.md`](docs/consuming-ocn-0.2.md).

### Consumer tools

- [`tools/ocn.py`](tools/ocn.py) — the reader: load the catalogue, look up a
  slug or a FEN, walk parents and children, resolve `transposes_to` and
  `same_as`. Start here if you are writing code against OCN.
- [`tools/from_uci.py`](tools/from_uci.py) — a legal UCI move sequence in, the
  deepest OCN-1 row whose moves are a prefix of it out (TSV, or `--json`).
- [`tools/from_eco.py`](tools/from_eco.py) — an ECO code, a PGN file, or inline
  PGN with an `[ECO "..."]` tag in, the unique deepest match out; `--all` lists
  candidates for ambiguous codes.
- [`tools/from_position.py`](tools/from_position.py) — a FEN in, matching rows
  out; board, side to move, castling and en passant are matched, the move
  counters ignored.
- [`tools/export_positions.py`](tools/export_positions.py) — writes the derived
  position-indexed TSV/JSON view (`fen_key`, counter-normalised `fen`,
  transposition group size). A fuller positions sidecar — SAN movetext, EPD and
  Polyglot zobrist, all computed here in Python — is planned (roadmap H2.8).

### Maintainer tools

[`tools/validate.py`](tools/validate.py) is the gate CI runs: format, slug
collisions, parent references, depth limits, plus a `--strict-chess` mode for
legal UCI sequences and SAN tail consistency.
[`tools/audit_chess.py`](tools/audit_chess.py) and
[`tools/audit_transpositions.py`](tools/audit_transpositions.py) are its batch
counterparts, reporting every issue — or every duplicate-FEN group, ranked by
how likely it is to need a structural decision — instead of stopping at the
first; the resolution workflow is in
[`docs/archive/transpositions.md`](docs/archive/transpositions.md). The
attribution factory ([`audit_naming_attribution.py`](tools/audit_naming_attribution.py),
[`candidate_slice_export.py`](tools/candidate_slice_export.py),
[`scaffold_attribution_manifest.py`](tools/scaffold_attribution_manifest.py),
[`apply_attribution_manifest.py`](tools/apply_attribution_manifest.py)) triages
rows, exports review slices and applies evidence-backed JSON manifests under
strict guardrails — the catalogue is never hand-edited (see
[`docs/attribution-batch-engine.md`](docs/attribution-batch-engine.md)).
[`tools/fetch_lichess.sh`](tools/fetch_lichess.sh) pulls the upstream Lichess
Opening Book TSVs (CC0) into `external/`. The remaining scripts — the Lichess
parent map, the doc slug gate, and the test suite CI runs on every push
([`tools/tests/`](tools/tests/),
[`.github/workflows/ci.yml`](.github/workflows/ci.yml)) — are listed with the
documents that use them in [`docs/INDEX.md`](docs/INDEX.md).

## Three relations per slug

Each catalogue row carries **three** relations to other slugs:

- `parent_ocn1` — nominal hierarchy. Groups slugs by literature
  lineage and lets a reader navigate from a family root down to a
  specific tabiya. The parent chain is what produces a readable slug
  (`E.Nim.Rub.O-O.Nf3` is a child of `E.Nim.Rub.O-O`).
- `transposes_to` — canonicalisation by position, **asymmetric**.
  Points from a slug whose FEN coincides with another slug's FEN
  to the FEN-canonical one. Set when this row is a move-order
  transposition of another. NULL when this row is itself canonical.
- `same_as` — co-canonical preservation, **symmetric**. Pipe-separated
  list of slugs that share this row's FEN and are preserved as
  co-canonicals (both / all are real literary names — e.g.
  Rubinstein Opening ⇄ Colle-Zukertort). Mutually exclusive with
  `transposes_to` on a single row.

A position-indexed consumer (e.g. `chess-parquet`) should follow
`transposes_to` once to canonicalise an OCN-1 result; rows linked
by `same_as` are all canonical and may be returned together. A
literature-oriented consumer (a book, a teaching tool) should follow
`parent_ocn1` to render the human hierarchy. The validator and
`audit_transpositions.py` enforce that both `transposes_to` and
`same_as` only point to rows whose FEN matches.

## Compatibility with ECO

OCN-1 does not deprecate ECO. The catalogue records, for every entry,
the ECO codes that the slug covers. Tools and consumers SHOULD support
both:

- given an ECO code, look up the OCN-1 slug;
- given an OCN-1 slug, look up the ECO codes.

Books, ChessBase, Lichess Opening Book, FIDE rating reports, and any
other system that uses ECO continues to work unchanged. OCN is the
hierarchical layer on top.

## Borderline classifications

Some openings sit awkwardly between ECO classes. OCN-1 makes explicit
choices, and these are where its class letter differs from ECO's:

- **French** (`B.Fre` and its subtree) is `B`, the semi-open class, although
  ECO codes it C00-C19. Rationale: OCN reads `C` as the symmetric king-pawn
  openings (1.e4 e5); the French answers 1.e4 asymmetrically, like the
  Sicilian and the Caro-Kann. At 252 rows this is the largest single
  divergence, and the one most worth arguing about.
- **London / Colle family** (`A.Lon`, `A.Col` and neighbours) is `A`
  although ECO codes them in the D range (D02-D05). Rationale: they are
  queen's-pawn *systems*, played largely regardless of Black's reply,
  rather than Queen's Gambit theory (82 rows).
- **Catalan** is `D` when Black plays ...d5 within the first five moves.
  Without ...d5, the position is `E` (Indian setup against the Catalan
  bishop).
- **Grünfeld** is `E` (Indian) even though most legacy ECO codes place
  it in the D range (D70-D99). Rationale: Grünfeld is structurally an
  Indian defence, and grouping it with KID, Nimzo, QID, Bogo gives a
  cleaner parent-child hierarchy.
- **Benoni / Benko** is `E` (Indian) even though legacy ECO places it in
  the A range. Rationale: the main Benoni and Benko families are Indian
  defences by structure and move-order (`1.d4 Nf6 2.c4 c5`), so they
  belong beside KID and Grünfeld rather than under flank openings.

See [`spec/OCN-1.md`](spec/OCN-1.md) for the full reasoning.

## Roadmap

The living plan is [`docs/traction-roadmap.md`](docs/traction-roadmap.md):
five horizons — a public-ready gate, exist and install, prove it, announce,
grow — taking OCN from a released catalogue to a standard people can find,
install and cite. Two long-running tracks continue under it: naming
attribution (are the eponyms *true*, and is the *kind* of attribution
explicit — invented, published, popularised, event anchor? Methodology:
[`docs/naming-attribution-audit-methodology.md`](docs/naming-attribution-audit-methodology.md))
and the internationalised alias sidecars, where the English `canonical_name`
stays definitive. Release records, decision logs and the rest of the
documentation are indexed in [`docs/INDEX.md`](docs/INDEX.md).

## Acknowledgements

OCN-1 builds on:

- **Šahovski Informator** (1971) for the A/B/C/D/E classification.
- **[lichess-org/chess-openings](https://github.com/lichess-org/chess-openings)**
  (CC0) for canonical English names of the long tail.
- **Hooper & Whyld**, *Oxford Companion to Chess* (1984), for naming
  conventions.

## License

Dual-licensed:

- **Specification documents** (in `spec/`) and **catalogues** (in
  `catalog/`): [CC-BY-4.0](LICENSE-SPEC).
- **Code** (in `tools/`): [MIT](LICENSE-CODE).

Copyright © 2026 Club d'Escacs Figueres.
