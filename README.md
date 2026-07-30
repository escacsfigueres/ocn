# OCN — Open Chess Naming

[![CI](https://github.com/escacsfigueres/ocn/actions/workflows/ci.yml/badge.svg)](https://github.com/escacsfigueres/ocn/actions/workflows/ci.yml)
[![Spec license: CC BY 4.0](https://img.shields.io/badge/spec-CC%20BY%204.0-lightgrey.svg)](LICENSE-SPEC)
[![Code license: MIT](https://img.shields.io/badge/code-MIT-blue.svg)](LICENSE-CODE)
[![Release](https://img.shields.io/badge/release-ocn--1.2.1-blue.svg)](https://github.com/escacsfigueres/ocn/releases/tag/ocn-1.2.1)
[![PyPI](https://img.shields.io/pypi/v/ocn-chess.svg)](https://pypi.org/project/ocn-chess/)
[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.21670207-1f6feb.svg)](https://doi.org/10.5281/zenodo.21670207)
[![Explorer](https://img.shields.io/badge/explorer-ocn.vercel.app-brightgreen.svg)](https://ocn.vercel.app)

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

**Browse the whole catalogue at [ocn.vercel.app](https://ocn.vercel.app)** —
every slug, its moves, its ECO codes, its aliases, how often it is played,
and who it is named after.

## Five-minute quickstart

```bash
pip install ocn-chess
```

The catalogue travels inside the package: no download, no database, no
third-party dependency, and the lookups work on a plane.

```python
from ocn import Catalog

cat = Catalog.load()                                 # the bundled catalogue, offline
cat.by_slug("B.Sic.Naj.Eng").canonical_name          # -> 'Sicilian Najdorf, English Attack'
[row.ocn1 for row in cat.parents("B.Sic.Naj.Eng")]   # -> ['B', 'B.Sic', 'B.Sic.Naj']
len(cat.by_eco("B90"))                               # -> 20
fen = "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2"   # 1.e4 c5
cat.by_fen(fen)[0].ocn1                              # -> 'B.Sic'
```

Twenty OCN rows share the single ECO code `B90`, and the breadcrumb
reads the hierarchy back out — that is the whole pitch, in four lines.
The FEN above ends in an en-passant square no pawn can legally capture
on, which is what most board libraries print and what silently returns
zero rows everywhere else; `by_fen` normalises it (see
[`ocn/fen.py`](src/ocn/fen.py)).

Then name your own games:

```bash
ocn annotate games.pgn --stats > named.pgn
```

Every game gains `[OCN "..."]` and `[OCNName "..."]` headers, matched by
position at every ply — so a Najdorf reached through 1.Nf3 is named a
Najdorf — and `--stats` prints the coverage summary to stderr. Nothing
else in the file is touched.

The Python block above is executed and checked against its own `# ->`
comments by [`tests/test_quickstart.py`](tests/test_quickstart.py) on
every push: copy-paste works verbatim, or CI goes red.

## Why

ECO has aged remarkably well in one respect: A/B/C/D/E captures the
fundamental structural divide of chess openings (semi-open vs open vs
closed vs Indian vs flank) and any new opening fits cleanly into one of
those five families. **OCN keeps that idea. It does not keep every one of
ECO's letter assignments.** 770 rows — 13.8% of the rows that carry an ECO
code — sit in an OCN class that is not among their own ECO letters, always
for a structural reason: the French is `B`, the London and Colle systems
are `A`, the Grünfeld and Benoni are `E`. The complete machine-readable
list is [`catalog/ocn-1.eco-divergence.tsv`](catalog/ocn-1.eco-divergence.tsv)
(derived, validator-enforced); the main cases are argued under
"Borderline classifications" below and in the spec's Borderline rules.

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

For specific named tabiyas the slug may carry trailing SAN moves
(`B.Sic.Sve.Nd5` for the 11.Nd5 main line). See the spec for the
full grammar; for everyday use the four levels above are enough.

You can read the slug at any depth and immediately know:

- The **structural class** of the position (`B` = semi-open).
- The **family** (`Sic` = Sicilian).
- The **variation** (`Naj` = Najdorf).
- And, if you want the precision, the **exact tabiya** down to the
  signature SAN move that defines it.

## Format

```
<class> ( "." <named> )+ ( "." <move> )*
```

- **`class`**: 1 char from `A B C D E` (ECO's five families; see
  "Borderline classifications" for where OCN's letter differs from ECO's).
- **`named`**: one or more 3-char TitleCase tokens — family (`Sic`,
  `RyL`, `KID`), variation (`Naj`), subline (`Eng`) and deeper levels.
- **`move`**: zero or more trailing SAN-style segments, capitalised
  pieces, check/mate stripped (`Be3`, `e5`, `Bxf6`, `O-O`).
- **Separator**: dot `.`.
- **Maximum depth**: 7 segments total (6 dots) — a hard cap; deeper
  theory is identified by position, not by longer slugs.

The full specification is in [`spec/OCN-1.md`](spec/OCN-1.md).

## Status

**Released — `ocn-1.2.1` (2026-07-30).** Citable as [doi:10.5281/zenodo.21670207](https://doi.org/10.5281/zenodo.21670207).
Previous release: `ocn-1.2.0` (2026-06-11). The format is stable; the reference
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

### Sidecars: what else ships beside the names

Additive tables keyed on `ocn1`. `catalog/ocn-1.csv` never changes shape
to accommodate them, so a consumer takes only what it needs.

| file | rows | what it holds |
|---|---:|---|
| `ocn-1.popularity.tsv` | 5,894 | master and Lichess game counts per opening, plus the strongest game's year range |
| `ocn-1.claims.tsv` | 852 | the chronicle: typed, sourced, graded assertions about openings |
| `ocn-1.people.tsv` / `ocn-1.events.tsv` | 61 / 71 | the entities those claims point at |
| `ocn-1.wch.tsv` | 1,040 | every world championship game mapped to a slug |
| `ocn-1.eco.tsv`, `ocn-1.eco-divergence.tsv` | — | ECO mapping, and where we knowingly differ |
| `ocn-1.lichess-xref.tsv` | 5,899 | position-keyed cross-reference to Lichess's names |
| `ocn-1.aliases.{ca,es}.tsv` | — | locale aliases (Catalan, Spanish) |

### The chronicle layer

Most opening datasets answer "what is this line called". The chronicle
answers the questions people actually ask: *who is it named after, and
did they invent it?*

Usually not. Of the attributions carrying a role, the majority say the
person **popularised** a line rather than originating it — and the
catalogue records which. Damiano is filed as the **critic** of the
defence that bears his name, on the Oxford Companion's words: "a
variation given by Lucena and rightly condemned by Damiano". Where a
source names a rival claimant, that goes in `historical_notes` rather
than being quietly resolved.

`ocn-1.claims.tsv` is one table with many entrances — the same rows
answer "which openings decided world championships" and "which openings
are named after places", because a claim carries its subject's type.
Every claim states its source and its evidence grade, and no grade is
better than the evidence for it.

The design, the sources it admits, and the reasoning behind each lot are
in [`docs/`](docs/INDEX.md).

## Tools

Everything is Python 3 standard library — no third-party dependency, no
build step (chess legality is checked by the in-repo move generator,
[`tools/chess_uci.py`](tools/chess_uci.py)). Recipes
and join patterns for consumers are in
[`docs/consuming-ocn.md`](docs/consuming-ocn.md).

### The `ocn-chess` package

The installable form of everything below, with the catalogue bundled
inside the wheel — no checkout, no network, no dependency. Built here
under [`src/ocn/`](src/ocn/); on PyPI as
[`ocn-chess`](https://pypi.org/project/ocn-chess/).

```python
from ocn import Catalog

cat = Catalog.load()
cat.by_slug("B.Sic.Naj.Eng").canonical_name   # 'Sicilian Najdorf, English Attack'
cat.by_eco("B90")                             # deepest first
cat.by_name("Grunfeld")                       # case- and diacritic-folded
cat.parents("B.Sic.Naj.Eng")                  # breadcrumb, root to parent
cat.by_fen(fen)                               # O(1); en-passant trap handled
```

```
ocn lookup B90
ocn lookup B.Sic.Naj
ocn fen "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2"
ocn uci "e2e4 c7c5 g1f3 d7d6"
ocn annotate games.pgn --stats > named.pgn
```

`annotate` reads a multi-game PGN (`-` for stdin), tags every game with
`[OCN]` and `[OCNName]`, and leaves the rest of the file byte for byte
as it found it. The match is by **position at every ply, deepest hit
wins**, so transpositions land on the same name as the move order they
transpose into, and `transposes_to` is resolved to the canonical slug.
`--stats` prints games, match rate, median depth in plies and the top
openings to stderr; a thousand games annotate in well under a second.

Every subcommand takes `--json`. Details and join patterns:
[`docs/consuming-ocn.md`](docs/consuming-ocn.md).

### The `ocn` Rust crate

The same catalogue, the same API shape, embedded in the binary with zero
runtime dependencies. Built here under [`rust/`](rust/); on crates.io as
[`ocn`](https://crates.io/crates/ocn).

```bash
cargo add ocn
```

```rust
let cat = ocn::Catalog::load();                        // embedded, parsed once
cat.by_slug("B.Sic.Naj.Eng").unwrap().canonical_name;  // "Sicilian Najdorf, English Attack"
cat.by_fen(fen).unwrap();                              // en-passant trap handled
```

The crate carries no move generator: position lookup reads the embedded
index, and `fen_key` needs only Annex A's legal-capture test. Its suite
recomputes `fen_key` and the Polyglot hash for all 5,894 concrete rows
and demands the Python-derived columns back, so the two readers cannot
drift apart. Details: [`rust/README.md`](rust/README.md).

### Consumer tools

- [`tools/ocn.py`](tools/ocn.py) — the in-repo reader: load the catalogue, look
  up a slug or a FEN, walk parents and children, resolve `transposes_to` and
  `same_as`. Use the package above unless you want a checkout-only script.
- [`tools/from_uci.py`](tools/from_uci.py) — a legal UCI move sequence in, the
  deepest OCN-1 row whose moves are a prefix of it out (TSV, or `--json`).
- [`tools/from_eco.py`](tools/from_eco.py) — an ECO code, a PGN file, or inline
  PGN with an `[ECO "..."]` tag in, the unique deepest match out; `--all` lists
  candidates for ambiguous codes.
- [`tools/from_position.py`](tools/from_position.py) — a FEN in, matching rows
  out; board, side to move, castling and en passant are matched, the move
  counters ignored.
- [`tools/coverage_stat.py`](tools/coverage_stat.py) — runs the `ocn annotate`
  matcher over a PGN corpus and reports only the numbers: match rate, median
  depth, the depth table and the top openings, as text or JSON. The
  reproducible script behind any published "OCN names X% of real games"
  figure; it streams, so a compressed dump can be piped straight into it.
- [`tools/export_positions.py`](tools/export_positions.py) — writes the derived
  position-indexed TSV/JSON view: `fen_key`, a complete `fen` with true
  halfmove/fullmove counters, transposition group size, SAN movetext, EPD and
  the Polyglot `zobrist`, all computed here in Python (roadmap H2.8). This is
  the index the package bundles.
- [`tools/polyglot_zobrist.py`](tools/polyglot_zobrist.py) — the Polyglot book
  hash of spec Annex A in stdlib Python: the public 781-key table vendored with
  its provenance, pinned in CI against the book format's published test
  vectors. No runtime dependency, no private repo in the chain.

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
