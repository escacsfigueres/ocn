# OCN — Open Chess Naming

[![CI](https://github.com/escacsfigueres/ocn/actions/workflows/ci.yml/badge.svg)](https://github.com/escacsfigueres/ocn/actions/workflows/ci.yml)
[![Spec license: CC BY 4.0](https://img.shields.io/badge/spec-CC%20BY%204.0-lightgrey.svg)](LICENSE-SPEC)
[![Code license: MIT](https://img.shields.io/badge/code-MIT-blue.svg)](LICENSE-CODE)
[![Status](https://img.shields.io/badge/status-alpha-orange.svg)](#status)

**OCN** is a hierarchical, human-readable naming scheme for chess
openings, designed as a companion to ECO (the *Encyclopaedia of Chess
Openings* code system that has been the de facto standard since 1971).
OCN keeps what is good about ECO — the A/B/C/D/E top-level classification
— and replaces the arbitrary 100-codes-per-letter sub-numbering with
short, parent-aware slugs.

## At a glance

| ECO | OCN-1 | Canonical name |
|---|---|---|
| `B33` | `B.Sic.Sve` | Sicilian Sveshnikov |
| `B90` | `B.Sic.Naj.Eng` | Najdorf English Attack |
| `C67` | `C.RyL.Ber.End` | Ruy López, Berlin Endgame |
| `D47` | `D.Sla.Sem.Mer` | Semi-Slav, Mèran |
| `E97` | `E.KID.Cls.Mar` | KID Classical, Mar del Plata |

Read once, remember forever. No lookup table needed.

## Why

ECO has aged remarkably well in one respect: A/B/C/D/E captures the
fundamental structural divide of chess openings (semi-open vs open vs
closed vs Indian vs flank) and any new opening fits cleanly into one of
those five families. **That part of ECO is genuinely good and OCN keeps
it unchanged.**

ECO has aged poorly in another respect: the 00-99 sub-codes within each
letter were assigned in 1971 according to what was fashionable at the
time, distribute coverage unevenly (the Sicilian alone gets 80 codes,
the irregulars share 19), and offer no parent-child hierarchy. Knowing
that "B33 = Sveshnikov" or "C67 = Berlin Endgame" is a feat of
memorisation that benefits no one — neither the player who wants to
study an opening, nor the database designer running queries.

OCN replaces that 50-year-old sub-numbering with hierarchical slugs:

```
B              ← top level (ECO class preserved)
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

- **`class`**: 1 char from `A B C D E` (preserves ECO classification).
- **`family`**: 3 chars, TitleCase (`Sic`, `RyL`, `KID`).
- **`variation`** / **`subline`**: 3 chars each, TitleCase (`Naj`, `End`).
- **`move`**: SAN-style, capitalised pieces (`Be3`, `e5`, `Bxf6`, `O-O`).
  Up to two trailing move segments are allowed.
- **Separator**: dot `.`.
- **Maximum depth**: 6 dots / 7 segments. Recommended cap is 5 segments
  for everyday use; deeper slugs are reserved for legendary tabiyas.

The full specification is in [`spec/OCN-1.md`](spec/OCN-1.md).

## Status

**Alpha (2026-05-22).** The format is stable; the reference catalogue has
6,099 entries and passes strict legal-move/SAN validation in CI. Comments,
corrections and additions welcome via issues.

> Naming history: previously drafted as **OCS — Open Chess Slug** during
> alpha. Renamed to OCN before public release because "slug" carries
> different connotations outside web-development circles. The format
> itself is unchanged.

## Catalogue

The reference catalogue lives in [`catalog/ocn-1.csv`](catalog/ocn-1.csv)
and contains, for each slug:

- the OCN-1 string (primary key)
- the canonical English name
- the ECO codes it covers (`eco_legacy`)
- the parent slug
- the depth in the hierarchy
- known aliases (Sveshnikov a.k.a. Lasker–Pelikan)
- tags (`gambit`, `sharp`, `closed`, `endgame`, `theoretical`)
- free-text notes for borderline classifications

The catalogue is licensed under **CC-BY-4.0**: you may use, share and
adapt it for any purpose, including commercial, provided you cite "Club
d'Escacs Figueres" and link to this repository.

## Tools

- [`tools/validate.py`](tools/validate.py) — checks the catalogue for
  format errors, slug collisions, broken parent references, profile
  depth limits. CI also runs its `--strict-chess` mode, which checks
  legal UCI move sequences and one-move SAN tail consistency.
- [`tools/audit_chess.py`](tools/audit_chess.py) — runs the strict chess
  legality/SAN checks across the full catalogue and reports every issue
  instead of stopping at the first one. Use it as a batch cleanup report
  if strict validation ever fails.
- [`tools/from_uci.py`](tools/from_uci.py) — given a legal UCI move
  sequence, returns the deepest OCN-1 catalogue row whose moves are a
  prefix of that sequence. Supports TSV output by default and JSON with
  `--json`.
- [`tools/from_eco.py`](tools/from_eco.py) — given an ECO code, PGN file,
  or inline PGN text with an `[ECO "..."]` tag, returns the unique deepest
  OCN-1 match. Ambiguous codes report candidates with `--all`.
- [`tools/from_position.py`](tools/from_position.py) — given a FEN
  position, returns matching OCN-1 catalogue rows. It matches on board,
  side to move, castling rights, and en-passant square, ignoring halfmove
  and fullmove counters.
- [`tools/export_positions.py`](tools/export_positions.py) — exports a
  derived position-indexed TSV/JSON view with `fen_key`, canonical
  counter-normalised `fen`, and transposition group size for each concrete
  catalogue row. Polyglot Zobrist materialisation is handled by the
  `efcdb openings` producer in `escacsfigueres/chess-parquet`.
- [`tools/audit_transpositions.py`](tools/audit_transpositions.py) — groups
  catalogue rows by FEN position key and reports every group with two or
  more entries (TSV by default, structured JSON with `--json`). Useful for
  preparing canonical/alias decisions across move orders. Supports
  `--summary`, `--min-size N`, `--class A/B/C/D/E`, and a scoring mode
  `--ranked [--limit N]` that surfaces the groups most likely to require
  a structural decision (class mixing, depth span, ECO/name/parent
  divergence, A/D, A/E and D/E family bonuses). Groups already resolved
  by the catalogue's `transposes_to` link (see below) are **hidden by
  default**; pass `--include-resolved` to see them. See
  [`docs/transpositions.md`](docs/transpositions.md) for the resolution
  workflow and the current top families to decide. Typical usage:

  ```
  python3 tools/audit_transpositions.py --ranked --limit 20
  python3 tools/audit_transpositions.py --ranked --include-resolved --limit 20
  ```

  The audit is informational: transpositions are expected, not errors.
- [`tools/lichess_parent_map.py`](tools/lichess_parent_map.py) — reads
  Lichess Opening Book TSV rows, converts their SAN PGN lines to UCI, and
  emits the deepest matching OCN-1 parent for each row. Use `--check` to
  fail if any row cannot be parsed or assigned to an OCN-1 parent, and
  `--quality` to inspect depth distribution and the most common parents.
- [`tools/tests/`](tools/tests/) — tool test suite covering validation,
  strict chess checks, lookup behaviour, and positive/negative fixtures
  (`tools/tests/fixtures/`). CI runs it
  on every push and pull request via [`.github/workflows/ci.yml`](.github/workflows/ci.yml).
- [`tools/fetch_lichess.sh`](tools/fetch_lichess.sh) — pulls the
  upstream Lichess Opening Book TSVs (CC0) into `external/`, used by
  `escacsfigueres/chess-parquet`'s Lichess companion-table builder.

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
choices, documented in the spec:

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

- **0.1** — Core spec, ~6,100-entry catalogue, strict validator,
  lookup tools, and a derived FEN position export.
- **0.2** *(tagged · `ocn-1.0.2` baseline at `415f1df`,
  `ocn-1.0.3` post-cleanup release at `dd2abd3` with downloadable
  artefacts)* — Position canonicalisation and downstream
  artefacts. 14-column catalogue with `transposes_to`
  (asymmetric) and `same_as` (symmetric) relations;
  `audit_transpositions.py` classifies duplicate FEN groups as
  `single_canonical` or `multiple_canonical`. Downstream
  `chess-parquet` already consumes the 0.2 schema. Post-tag main
  has reduced unresolved duplicate groups from 116 → **1** (only the
  QID Miles/Petrosian slug-migration hold remains; transposition
  cleanup phase closed — see
  [`docs/transposition-cleanup-closure.md`](docs/transposition-cleanup-closure.md)).
  **Consumer guide:**
  [`docs/consuming-ocn-0.2.md`](docs/consuming-ocn-0.2.md).
  Other docs: [`docs/roadmap-0.2.md`](docs/roadmap-0.2.md) for the
  original phased plan,
  [`docs/release-0.2-checklist.md`](docs/release-0.2-checklist.md)
  for the `ocn-1.0.3` release decision record,
  [`docs/release-0.2-post-transposition-cleanup-checklist.md`](docs/release-0.2-post-transposition-cleanup-checklist.md)
  for the current post-cleanup release candidate (`ad25527`,
  not yet tagged), and
  [`docs/post-0.2-next-steps.md`](docs/post-0.2-next-steps.md)
  for what's next.
- **0.3** — Internationalised aliases: Catalan, Spanish, French,
  German display names. The English `canonical_name` stays
  definitive.
- **1.0** — Frozen format and stable catalogue. Public release with
  an open call for feedback from the wider chess data community.

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
