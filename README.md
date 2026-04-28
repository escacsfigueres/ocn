# OCS — Open Chess Slug

[![Spec license: CC BY 4.0](https://img.shields.io/badge/spec-CC%20BY%204.0-lightgrey.svg)](LICENSE-SPEC)
[![Code license: MIT](https://img.shields.io/badge/code-MIT-blue.svg)](LICENSE-CODE)
[![Status](https://img.shields.io/badge/status-alpha-orange.svg)](#status)

**OCS** is a hierarchical, human-readable naming scheme for chess
openings, designed as a companion to ECO (the *Encyclopaedia of Chess
Openings* code system that has been the de facto standard since 1971).
OCS keeps what is good about ECO — the A/B/C/D/E top-level classification
— and replaces the arbitrary 100-codes-per-letter sub-numbering with
short, parent-aware slugs.

## At a glance

| ECO | OCS-1 | Canonical name |
|---|---|---|
| `B33` | `B.Sic.Sve` | Sicilian Sveshnikov |
| `B90` | `B.Sic.Naj.Eng` | Najdorf English Attack |
| `C67` | `C.RyL.Ber.End` | Ruy López, Berlin Endgame |
| `D47` | `D.Sla.Mer` | Semi-Slav, Mèran |
| `E97` | `E.KID.Cls.Mar` | KID Classical, Mar del Plata |

Read once, remember forever. No lookup table needed.

## Why

ECO has aged remarkably well in one respect: A/B/C/D/E captures the
fundamental structural divide of chess openings (semi-open vs open vs
closed vs Indian vs flank) and any new opening fits cleanly into one of
those five families. **That part of ECO is genuinely good and OCS keeps
it unchanged.**

ECO has aged poorly in another respect: the 00-99 sub-codes within each
letter were assigned in 1971 according to what was fashionable at the
time, distribute coverage unevenly (the Sicilian alone gets 80 codes,
the irregulars share 19), and offer no parent-child hierarchy. Knowing
that "B33 = Sveshnikov" or "C67 = Berlin Endgame" is a feat of
memorisation that benefits no one — neither the player who wants to
study an opening, nor the database designer running queries.

OCS replaces that 50-year-old sub-numbering with hierarchical slugs:

```
B          ← top level (ECO class preserved)
B.Sic      ← family (Sicilian)
B.Sic.Naj  ← variation (Najdorf)
B.Sic.Naj.Eng  ← sub-line (English Attack)
B.Sic.Naj.Eng.Be3.e5  ← specific tabiya (6.Be3 e5 main line)
```

You can read the slug at any depth and immediately know:

- The **structural class** of the position (`B` = semi-open).
- The **family** (`Sic` = Sicilian).
- The **variation** (`Naj` = Najdorf).
- And, if you want the precision, the **exact tabiya** down to the
  signature SAN move that defines it.

## Format

```
<class> "." <family> [ "." <variation> [ "." <subline> [ "." <move> ] ] ]
```

- **`class`**: 1 char from `A B C D E` (preserves ECO classification).
- **`family`**: 3 chars, TitleCase (`Sic`, `RyL`, `KID`).
- **`variation`** / **`subline`**: 3 chars each, TitleCase (`Naj`, `End`).
- **`move`**: SAN-style, capitalised pieces (`Be3`, `e5`, `Bxf6`, `O-O`).
- **Separator**: dot `.`.
- **Maximum depth**: 6 segments (cap recommended at 5 for everyday use).

The full specification is in [`spec/OCS-1.md`](spec/OCS-1.md).

## Status

**Alpha (2026-04-28).** The format is stable; the catalogue covers the
~120 most-frequent opening lines. Comments, corrections and additions
welcome via issues.

## Catalogue

The reference catalogue lives in [`catalog/ocs-1.csv`](catalog/ocs-1.csv)
and contains, for each slug:

- the OCS-1 string (primary key)
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
  depth limits.

Future tools (planned):

- `tools/from_eco.py` — given a PGN with `[ECO "B90"]`, return the most
  specific OCS-1 slug.
- `tools/from_position.py` — given a FEN or Polyglot zobrist, return
  the OCS-1 slug.
- `tools/from_uci.py` — given a UCI move sequence, return the deepest
  matching OCS-1 slug.

## Compatibility with ECO

OCS-1 does not deprecate ECO. The catalogue records, for every entry,
the ECO codes that the slug covers. Tools and consumers SHOULD support
both:

- given an ECO code, look up the OCS-1 slug;
- given an OCS-1 slug, look up the ECO codes.

Books, ChessBase, Lichess Opening Book, FIDE rating reports, and any
other system that uses ECO continues to work unchanged. OCS is the
hierarchical layer on top.

## Borderline classifications

Some openings sit awkwardly between ECO classes. OCS-1 makes explicit
choices, documented in the spec:

- **Catalan** is `D` when Black plays ...d5 within the first five moves.
  Without ...d5, the position is `E` (Indian setup against the Catalan
  bishop).
- **Grünfeld** is `E` (Indian) even though most legacy ECO codes place
  it in the D range (D70-D99). Rationale: Grünfeld is structurally an
  Indian defence, and grouping it with KID, Nimzo, QID, Bogo gives a
  cleaner parent-child hierarchy.
- **Benoni** is `A` (flank) because 2...c5 declines the d5/c4 symmetry.

See [`spec/OCS-1.md`](spec/OCS-1.md) for the full reasoning.

## Roadmap

- **0.1** *(current)* — Core spec, top ~120 entries, validator.
- **0.2** — Tooling: `from_eco`, `from_position`, `from_uci`. Lichess
  Opening Book mapping for the long tail (~3500 entries).
- **0.3** — Internationalised aliases: Catalan, Spanish, French, German
  display names. The English `canonical_name` stays definitive.
- **1.0** — Frozen format and stable catalogue. Public release with an
  open call for feedback from the wider chess data community.

## Acknowledgements

OCS-1 builds on:

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
