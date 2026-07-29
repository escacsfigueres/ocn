# Consuming OCN

*(Current as of `ocn-1.2.0`, 5,899 rows. Renamed 2026-07-29 — the
filename previously carried a `-0.2` release suffix; the guide tracks
the catalogue, not one release.)*

A short, practical guide for someone joining FEN / zobrist / game
positions to OCN openings. If you have already implemented an
opening-book join against another catalogue (Lichess, ChessBase,
SCID), **OCN looks similar but has one crucial difference**: a
single position can map to multiple canonical rows by design.
Read the [Quick start](#0-quick-start) and the
[Common mistakes](#8-common-mistakes) before writing the join.

For background and full normative definitions, see
[`spec/OCN-1.md`](../spec/OCN-1.md). For the project roadmap, see
[`traction-roadmap.md`](traction-roadmap.md). For the release with
shipped artefacts, see
[ocn-1.2.0](https://github.com/escacsfigueres/ocn/releases/tag/ocn-1.2.0).

## 0. Quick start

If you have a chess position and want OCN names:

1. Install the package (`pip install ocn-chess`) and call `Catalog.by_fen(fen)` —
   the en-passant normalisation and the O(1) positions index are built
   in. Without Python, match your position's `fen_key` against the
   release artefact `ocn-1.positions.tsv` (spec Annex A defines the key).
2. **Keep all rows returned** — do not deduplicate on position.
3. For each row, derive `canonical_ocn1 = COALESCE(NULLIF(transposes_to, ''), ocn1)`.
4. Group / display per your UI: see
   [Handling transpositions](#5-handling-transpositions) for
   non-canonical → canonical, and
   [Handling co-canonicals](#6-handling-co-canonicals) for the
   "two real names" case.

That's the whole loop. Sections below explain why the contract is
shaped this way and what each column means.

## 1. Core contract

OCN rows are **not one-to-one with FEN / zobrist**. A single
position can return multiple OCN rows because two distinct
literary opening names can describe the same final position (e.g.
Rubinstein Opening ⇄ Colle System Zukertort, French Classical
Main Line ⇄ Veresov Classical Main Line). These coexistences are
recorded in the `same_as` column and are intentional, not
duplicate-cleanup work.

The consequence for consumers:

- **Do not** dedupe by `zobrist` at the storage layer.
- **Do not** treat a multi-row return as an error.
- **Do** decide what to display **after** collecting all matching
  rows. The display choice (single canonical, both names side by
  side, name-with-aka, etc.) is your product decision; OCN gives
  you the data to make it correctly.

The current catalogue has **124 positions with ≥2 OCN rows**
(out of 5,765 unique FENs), all of them classified: every group is
resolved by `transposes_to` or declared co-canonical via `same_as`
(**17 declared groups, 34 rows**). Consumers who collapse on
zobrist silently lose up to 124 distinct labels in real chess-game
queries.

## 2. Three relations

OCN encodes three different kinds of relationship between slugs.
They are orthogonal and serve different consumer needs.

| column | type | semantics | when set |
|---|---|---|---|
| `parent_ocn1` | string nullable | **Human / nominal hierarchy.** Walk up to render breadcrumb navigation ("Sicilian → Najdorf → English Attack"). Not for position canonicalisation. | Every non-class-root row. |
| `transposes_to` | string nullable | **Position canonicalisation, asymmetric.** Non-canonical row → canonical row that owns the same FEN. Used when a move-order alias exists alongside the canonical literary name. | Only on non-canonical rows. Mutually exclusive with `same_as`. |
| `same_as` | string nullable (pipe-separated) | **Co-canonical preservation, symmetric.** Both rows are canonical literary identities of the same position. Neither is "the alias" — both are real names. | Only on co-canonical rows (both sides usually carry it). Mutually exclusive with `transposes_to`. |

Class roots (`A`, `B`, `C`, `D`, `E`) carry none of these — they
are filters, not positions, and have no `moves_uci`, no
`transposes_to`, no `same_as`.

## 3. Canonical display rule

The single most important derivation:

```
canonical_ocn1 = transposes_to if transposes_to is not empty
                                  else ocn1
```

No artefact ships `canonical_ocn1` as a column: derive it on read.
The `ocn-chess` package does it for you (`Catalog.resolve`), and
section 7 has the one-line SQL view.

`same_as` does **not** replace `canonical_ocn1`. A row with
`same_as` set is itself canonical (its own `canonical_ocn1` equals
its `ocn1`); `same_as` is the list of *other* canonicals that
share its FEN. To enumerate every canonical for a position:

```
co_canonicals(row) = [row.ocn1] + split_pipe(row.same_as)
```

But the right join pattern is usually simpler: just `GROUP BY zobrist`
on the joined rows, then list their `canonical_ocn1` values
distinct. `same_as` is informative for display, not for join keys.

## 4. Lookup by position

Pick the right artefact for your input:

| have | use | join key |
|---|---|---|
| FEN string or board object | the `ocn-chess` package (`Catalog.by_fen`), `ocn-1.positions.tsv`, or `tools/ocn.py` | `fen_key` (board + side + castling + ep, ignoring counters) |
| Polyglot zobrist hash (INT64) | `ocn-1.positions.tsv`, the `zobrist` column | `zobrist` |
| EPD record | `ocn-1.positions.tsv`, the `epd` column | `epd` |
| OCN slug | the package, or `catalog/ocn-1.csv` directly | `ocn1` |
| Lichess opening name / line | `catalog/ocn-1.lichess-xref.tsv` | exact SAN sequence → `ocn1` (every Lichess line on a position OCN covers resolves to a slug) |
| how often a line is played | `catalog/ocn-1.popularity.tsv`, [section 15](#15-the-popularity-sidecar) | `ocn1` |

### What the positions sidecar carries

One row per concrete slug (the five class roots have no position and are
not in the file), fourteen columns:

| column | what it is |
|---|---|
| `ocn1`, `canonical_name`, `eco_legacy`, `parent_ocn1`, `depth`, `moves_uci` | copied from the catalogue, so the sidecar answers on its own |
| `fen_key` | the position identity of spec Annex A. **The join key.** |
| `fen` | the same position as a complete FEN, with the true halfmove clock and fullmove number of the line. Hand it to a board library; never join on it |
| `transposition_group_size` | how many catalogue rows share this `fen_key` |
| `transposes_to`, `same_as` | the two catalogue relations, sections 5 and 6 |
| `san` | the line as numbered movetext, `1.e4 c5 2.Nf3` |
| `epd` | the position as a bare EPD record (four fields, no operations) |
| `zobrist` | the Polyglot book hash, unsigned decimal |

Sample row (`B.Sic.Naj.Eng`, trimmed to the derived columns):

```
san      1.e4 c5 2.Nf3 d6 3.d4 cxd4 4.Nxd4 Nf6 5.Nc3 a6 6.Be3
epd      rnbqkb1r/1p2pppp/p2p1n2/8/3NP3/2N1B3/PPP2PPP/R2QKB1R b KQkq -
fen      rnbqkb1r/1p2pppp/p2p1n2/8/3NP3/2N1B3/PPP2PPP/R2QKB1R b KQkq - 1 6
zobrist  8839051919898350604
```

**Polyglot remains the recommended canonical 64-bit hash**, and as of
roadmap H2.8 the sidecar carries it: `zobrist` is the hash spec Annex A
defines, computed in this repository by
[`tools/polyglot_zobrist.py`](../tools/polyglot_zobrist.py) in stdlib
Python, with no runtime dependency and no private repo in the chain. It
is emitted as **unsigned decimal**; if your column is a signed INT64
(DuckDB, Postgres `bigint`, Parquet), reinterpret rather than clamp —
subtract 2^64 from anything above 2^63-1. The values are pinned in CI
against the public test vectors published with the Polyglot book format,
so a join against any conforming book or database matches exactly.

`epd` is the four EPD fields with no operations. Because OCN already
normalises en passant the way EPD wants it (see the trap below), that
string is the same string as `fen_key`; the column exists so EPD-driven
tooling finds the field under the name it expects. Join on `fen_key`.

`fen_key` in `ocn-1.positions.tsv` is the same FEN with halfmove
and fullmove counters stripped — match on that, not on the full
FEN, since OCN doesn't record counters. **En passant trap:** most
board libraries emit the ep square after *any* double push; the
catalogue keys keep it only when an ep capture is actually legal.
Normalise before matching (`tools/ocn.py`'s `fen_key()` does this
for you) or positions like 1.e4 c5 will silently miss.

Aliases (pipe-separated) now carry both systematic American
spellings ("Sicilian Defense" alongside the British canonical) and
1,300+ position-anchored Lichess labels, so name-based search
covers the vocabulary your users actually type.

Example (one position, two canonical rows by design):

```
zobrist 7092856595585369542
  → row 1: ocn1=D.Rub, canonical_ocn1=D.Rub, same_as=A.Col.Zuk
  → row 2: ocn1=A.Col.Zuk, canonical_ocn1=A.Col.Zuk, same_as=D.Rub
```

Both rows should be returned by the JOIN. Both are canonical.

## 5. Handling transpositions

A row with `transposes_to` set is a documented move-order
alias of the canonical it points to. Common case: a position
reached by two move orders, one of which is the literary name and
the other a structural descriptor.

Example:

```
ocn1            : C.Pet.Thr.Fou
canonical_name  : "Petrov Three Knights, Four Knights Transposition"
transposes_to   : C.Fou
canonical_ocn1  : C.Fou
```

UI display options (your product decides which fits):

```
A) Display canonical only:
   "Four Knights Game"

B) Display canonical with breadcrumb back to user's path:
   "Petrov Three Knights, Four Knights Transposition → Four Knights Game"

C) Display canonical with parenthetical aka:
   "Four Knights Game (via Petrov Three Knights transposition)"
```

The recommended default for most consumers is **A**: collapse to
the canonical name for the user-facing label. Show the
transposition path only if you have a "show source move order"
UI affordance.

## 6. Handling co-canonicals

A row with `same_as` set is canonical AND so is the row it points
to. Both should appear in the joined result, and your UI decides
how to present the dual identity.

Example:

```
row 1
  ocn1            : D.Rub
  canonical_name  : "Rubinstein Opening"
  transposes_to   : (null)
  same_as         : "A.Col.Zuk"

row 2
  ocn1            : A.Col.Zuk
  canonical_name  : "Colle System, Zukertort"
  transposes_to   : (null)
  same_as         : "D.Rub"
```

UI display options:

```
A) Both names with slash:
   "Rubinstein Opening / Colle System, Zukertort"

B) Primary name with aka:
   "Rubinstein Opening (also: Colle System, Zukertort)"

C) Pick one by product policy (locale, recency, etc.):
   "Colle System, Zukertort"
```

**Do not** silently drop one of the rows. The reason OCN keeps
both is exactly that the literature uses both names; collapsing
loses information your users may rely on.

The current catalogue has **17 declared co-canonical groups**
(34 rows carrying `same_as`). Enumerate them live with
`tools/audit_transpositions.py --include-resolved` or, in Python,
`Catalog.load().co_canonicals(slug)` from `tools/ocn.py`. More may
be added in future releases without schema changes.

## 7. Recommended SQL / pseudocode

### Python, zero dependencies (the `ocn-chess` package)

The package carries the catalogue and the position index inside the
wheel, so it works offline and needs nothing else installed. It is
built in this repository under [`src/ocn/`](../src/ocn/) — install it
with `pip install .` from a checkout; the PyPI release lands with the
next tagged release.

```python
from ocn import Catalog

cat = Catalog.load()                          # bundled ocn-1.csv
row = cat.by_slug("B.Sic.Naj.Eng")            # typed Row, KeyError if absent
row.eco                                       # ('B90',) — pipes already split
cat.by_eco("B90")                             # deepest first
cat.by_name("Grunfeld")                       # diacritic- and case-folded
cat.search("najdorf", limit=5)                # substring, broadest first
cat.parents("B.Sic.Naj.Eng")                  # breadcrumb, root to parent
for hit in cat.by_fen(fen):                   # O(1); handles the ep trap
    canonical = cat.by_slug(cat.resolve(hit.ocn1))
    others = cat.co_canonicals(canonical.ocn1)
```

Holding a board object rather than a FEN string:

```python
from ocn.fen import from_board

rows = cat.by_fen(from_board(board))   # python-chess is never imported
```

The same lookups from a shell, with `--json` on every subcommand:

```
ocn lookup B90
ocn lookup B.Sic.Naj.Eng
ocn lookup "najdorf"
ocn fen "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2"
ocn uci "e2e4 c7c5 g1f3 d7d6"
ocn version
```

`ocn.__version__` is the reader; `Catalog.load().version()` is the
catalogue release the bundled data came from. They move independently.

### Python from a checkout (`tools/ocn.py`)

If you have the repo and would rather not install anything, the
in-repo reader covers the same four loops over plain dicts:

```python
import sys; sys.path.insert(0, "tools")
from ocn import Catalog

cat = Catalog.load()                       # catalog/ocn-1.csv
row = cat.by_slug("B.Sic")                 # KeyError if absent
hits = cat.by_fen(fen)                     # handles the ep trap for you
for hit in hits:                           # ≥1 row per position by design
    canonical = cat.by_slug(cat.resolve(hit["ocn1"]))
    label = canonical["canonical_name"]
    others = cat.co_canonicals(canonical["ocn1"])   # same_as partners
tree = list(cat.walk("B.Sic"))             # whole subtree, breadcrumbs
```

### Canonical OCN per row (SQL)

The sidecar is a plain TSV, so every engine reads it directly. In DuckDB:

```sql
CREATE VIEW ocn AS
SELECT
  CAST(zobrist AS UBIGINT) AS zobrist,
  fen_key,
  ocn1,
  canonical_name,
  COALESCE(NULLIF(transposes_to, ''), ocn1) AS canonical_ocn1,
  same_as
FROM read_csv('ocn-1.positions.tsv', delim='\t', header=true,
              types={'zobrist': 'UBIGINT'});
```

`canonical_ocn1` is not a column in the file: it is `transposes_to`
when set, otherwise the row's own slug, which is the COALESCE above.
Materialise it once in a view and the rest of the queries stay short.

**Cast `zobrist` deliberately.** The column is unsigned decimal, so
about half the catalogue exceeds `2^63-1` and a bare `BIGINT` either
overflows or silently truncates. Read it as `UBIGINT` (DuckDB), or as
`numeric` / `text` in Postgres, and reinterpret if your own positions
table stores the hash signed.

### Joining a positions table to OCN (DuckDB style)

```sql
SELECT
  p.game_id,
  p.ply,
  o.ocn1,
  o.canonical_ocn1,
  o.canonical_name,
  o.same_as
FROM positions p
LEFT JOIN ocn o
  ON p.zobrist = o.zobrist;
```

Note: **this returns one row per `(p, o)` match**, so a position
with two co-canonical OCN rows produces two output rows per
position. Aggregate after collecting:

```sql
WITH joined AS (
  SELECT
    p.game_id, p.ply, p.zobrist,
    o.canonical_ocn1, o.canonical_name, o.same_as
  FROM positions p
  LEFT JOIN ocn o
    ON p.zobrist = o.zobrist
)
SELECT
  game_id, ply, zobrist,
  string_agg(DISTINCT canonical_name, ' / ' ORDER BY canonical_name)
    AS display_label
FROM joined
GROUP BY game_id, ply, zobrist;
```

If you have FENs rather than hashes, the same join works on `fen_key`
— normalise your en-passant field first (see the trap in section 4).

### Worked example

Input: `zobrist = 7092856595585369542` (Rubinstein / Colle-Zukertort tabiya).

Returns:

| ocn1 | canonical_name | transposes_to | same_as | canonical_ocn1 |
|---|---|---|---|---|
| `D.Rub` | Rubinstein Opening | (null) | `A.Col.Zuk` | `D.Rub` |
| `A.Col.Zuk` | Colle System, Zukertort | (null) | `D.Rub` | `A.Col.Zuk` |

Expected display output after `GROUP BY zobrist` with
`string_agg(canonical_name, ' / ')`:

```
"Colle System, Zukertort / Rubinstein Opening"
```

(Alphabetical because of the `ORDER BY canonical_name`; pick your
preferred ordering rule.)

### Pseudocode

```python
def display_name_for_zobrist(z, openings_table):
    rows = openings_table.lookup_all(z)        # may return ≥0 rows
    if not rows:
        return None                            # outside the catalogue
    canonicals = {r.canonical_ocn1 for r in rows}
    names = sorted({r.canonical_name for r in rows
                    if not r.transposes_to})    # filter to canonical rows
    if len(names) == 1:
        return names[0]
    return " / ".join(names)                   # co-canonical → both
```

## 8. Common mistakes

1. **Assuming one OCN per zobrist.** The most frequent and
   highest-impact mistake. OCN's contract explicitly allows
   multi-row returns; consumers that join with `INNER JOIN ...
   LIMIT 1` will silently mislabel 124 positions today and more
   in future releases.

2. **Treating multiple-canonical groups as data errors to
   deduplicate.** A `same_as` row is *not* a duplicate to be
   cleaned. It is OCN's primitive for "this FEN has two real
   names" and removing one row erases real literary information.

3. **Using ECO as primary key.** ECO codes are coarse (`B90`
   covers many distinct Najdorf lines) and frozen since 1971.
   OCN exposes ECO as `eco_legacy` for reference, but the
   primary key for joining is `ocn1` (for slug-keyed access) or
   `zobrist` (for position-keyed access). When you do need to
   filter by ECO, join the scalar table rather than pattern-match
   the packed cell — see [Joining by ECO](#9-joining-by-eco).

4. **Replacing `same_as` with `transposes_to`.** They mean
   different things. `transposes_to` says "this row is not
   canonical, the target is." `same_as` says "this row is
   canonical AND so is the target." If you map one to the other
   you corrupt OCN's relation.

5. **Deleting non-canonical rows before display.** Sometimes a
   user *wants* to see "Petrov Three Knights, Four Knights
   Transposition" specifically — it tells them how the position
   was reached. Drop non-canonical rows only when your UI
   explicitly chooses to collapse to a single canonical label.

6. **Ignoring class roots.** Rows `A`, `B`, `C`, `D`, `E` have
   no `moves_uci`, no `fen_key`, no `zobrist`. They will not
   join against your positions table and that is correct — they
   are family-level filters, not positions. Do not write a join
   that fails noisily on them.

## 9. Joining by ECO

`eco_legacy` is a *pipe-packed* cell: a slug covering several ECO
codes stores them as `A87|A88|A89`. That is honest storage and
hostile SQL — `LIKE '%B90%'` is not a join key, and it happily
matches nothing useful in one direction and too much in the other.
The sidecar
[`catalog/ocn-1.eco.tsv`](../catalog/ocn-1.eco.tsv) is the scalar
view of exactly the same data, one row per (slug, atomic code):

```
ocn1	eco	seq
A.Eng	A10	0
A.Eng	A11	1
A.Eng	A12	2
...
B.Sic.Naj.Eng	B90	0
```

`seq` is the code's 0-based position inside that slug's original
pipe list, so ordering by it reconstructs the `eco_legacy` cell
exactly. Every OCN slug carrying `B90`, stdlib only:

```python
import csv

with open("catalog/ocn-1.eco.tsv", newline="", encoding="utf-8") as f:
    b90 = [r["ocn1"] for r in csv.DictReader(f, delimiter="\t")
           if r["eco"] == "B90"]
```

The SQL shape is the obvious one — no `LIKE`, no string splitting:

```sql
SELECT c.*
FROM ocn_eco e
JOIN ocn_catalog c USING (ocn1)
WHERE e.eco = 'B90';
```

A code usually returns several rows (`B90` covers the Najdorf
family root and its deeper lines). To collapse to one, apply the
spec's **deepest-match** rule: keep the highest `depth` consistent
with your context, and report ties rather than picking silently.

Scale: **7,234 (slug, code) pairs** over **500 distinct ECO codes**
and **5,600 slugs** — more pairs than catalogue rows, because 526
slugs carry a composite cell.

Two things not to misread:

- **`eco_legacy` stays.** The table is additive, not a migration;
  consumers already splitting pipes keep working unchanged.
- **Absence is a statement, not a gap.** 299 rows (5.1%) carry no
  ECO code at all: the five class roots, which are filters rather
  than lines, and 294 Lichess long-tail lines that lie beyond
  ECO's 500-code resolution. They are simply not in the table. Do
  not left-join them onto a placeholder code.

Regenerate with `python3 tools/build_eco_table.py --report`; a
drift test fails CI if the committed file and the catalogue
disagree.

## 10. Consuming OCN from an ECO-keyed system

If your data is already keyed by ECO — a games table with an `eco`
column, a book keyed by code, a UI that groups by A/B/C/D/E — there
are exactly two safe ways to attach OCN, and one tempting shortcut
that is wrong.

**Path 1: join by code.** Use
[`catalog/ocn-1.eco.tsv`](../catalog/ocn-1.eco.tsv) (section 9). One
row per (slug, atomic code), so the join is an equality join, and a
code returning several slugs is normal — apply the deepest-match rule
to collapse. This is the right path when your rows carry a code and
nothing else.

**Path 2: join by position.** Replay the moves and compare `fen_key`
or the Polyglot `zobrist`, both defined normatively in
[Annex A](../spec/OCN-1.md#annex-a--position-identity-normative) and
covered in section 4 above. Slower to set up, strictly better
answers: it finds the OCN row for a position your ECO code only
approximates, and it survives transpositions that a code-keyed join
cannot see. Use it when you have real games or real boards.

**The shortcut that is wrong: joining by letter.** OCN's class letter
is *not* ECO's letter. It keeps ECO's five structural families as an
idea, and reassigns some of the members.

Worked example. Take `C00` — in ECO, "French Defence, general". A
consumer that reads ECO's letter as OCN's letter reasons:

```
row.eco = "C00"  ->  ECO letter C  ->  bucket "Open Games (1.e4 e5)"
```

and then produces a rendering that shows the French next to the Ruy
López and the Italian. What OCN actually says:

```python
import csv

with open("catalog/ocn-1.eco.tsv", newline="", encoding="utf-8") as f:
    slugs = [r["ocn1"] for r in csv.DictReader(f, delimiter="\t")
             if r["eco"] == "C00"]

slugs[:3]            # ['B.Fre', 'B.Fre.RPa', 'B.Fre.Kor']
slugs[0][0]          # 'B'  — not 'C'
len(slugs)           # 43
```

Every one of those 43 rows is class `B`. OCN reads `C` as the
symmetric king-pawn openings (1.e4 e5) and the French as a semi-open
answer to 1.e4, beside the Sicilian and Caro-Kann; the full argument
is in the spec's [Borderline
rules](../spec/OCN-1.md#borderline-rules). Bucket by OCN's letter and
label the bucket with ECO's meaning and you misfile the entire French
— 252 rows, one of the five most-played defences in chess.

The relation on this case is exactly stateable: OCN's `B` is ECO's B
*plus* the French, OCN's `C` is ECO's C *minus* the French. Every
other letter difference is enumerated in the divergence sidecar
[`catalog/ocn-1.eco-divergence.tsv`](../catalog/ocn-1.eco-divergence.tsv):

```
ocn1	ocn_class	eco_codes	family_head	rationale_ref
B.Fre	B	C00|C01|C02|...	B.Fre	french-b
A.Lon	A	D02	A.Lon	london-colle-a
E.Gru	E	D70|D71|...	E.Gru	gruenfeld-e
```

770 rows, 13.8% of the 5,600 rows that carry an ECO code.
`rationale_ref` is a closed set — `french-b`, `indians-e`,
`gruenfeld-e`, `catalan-d`, `london-colle-a`, `budapest-e`, `misc` —
and each key resolves to a written rationale in the spec's Borderline
rules. If you must map by letter (a legacy UI, a fixed schema), load
this file first and treat the listed slugs as the exception table;
absence from it means the letters agree.

Regenerate with `python3 tools/build_eco_divergence.py --report`. The
committed file is pinned twice: a drift test rebuilds it, and
`tools/validate.py` independently recomputes the divergent set and
fails on any disagreement — the count cannot grow without the list
growing with it.

## 11. The whole-catalogue JSON export

`ocn-1.json` is a release artefact: the entire catalogue in one
file, with no CSV parser, no pipe splitting and no chess engine
required at the consumer end. It is built by
[`tools/build_json_export.py`](../tools/build_json_export.py) and
attached to releases. It is deliberately **not** committed — the
canonical source is `catalog/ocn-1.csv`, and a checked-in
derivative would drift from it. The shape, with one row shown and
its emptier catalogue columns elided so the sample stays readable:

```json
{
  "schema": "ocn.catalog.v1",
  "catalog_version": "ocn-1.2.0",
  "generated_note": "derived artefact, canonical source is catalog/ocn-1.csv",
  "rows": [
    {
      "ocn1": "B.Sic.Naj.Eng",
      "canonical_name": "Sicilian Najdorf, English Attack",
      "eco_legacy": "B90",
      "parent_ocn1": "B.Sic.Naj",
      "moves_uci": "e2e4 c7c5 g1f3 d7d6 d2d4 c5d4 f3d4 g8f6 b1c3 a7a6 c1e3",
      "depth": "3",
      "moves_san": "1.e4 c5 2.Nf3 d6 3.d4 cxd4 4.Nxd4 Nf6 5.Nc3 a6 6.Be3",
      "eco": ["B90"],
      "aliases_list": [],
      "same_as_list": [],
      "flags_list": ["sharp", "theoretical"]
    }
  ]
}
```

Each row object carries **every catalogue column verbatim, in
header order** (values are strings, exactly as in the CSV), then
five derived fields:

| field | type | derivation |
|---|---|---|
| `moves_san` | string | `moves_uci` replayed offline to numbered SAN (`1.e4 c5 2.Nf3`). `""` for the five class roots, which have no position. |
| `eco` | array | `eco_legacy` split on `\|`; `[]` when empty, never `[""]`. |
| `aliases_list` | array | `aliases` split on `\|`. |
| `same_as_list` | array | `same_as` split on `\|`. |
| `flags_list` | array | `flags` split on `\|`. |

Guarantees worth relying on:

- **Rows follow catalogue order** and every row object uses the
  same fixed key order, so two builds of the same catalogue are
  byte-identical and a diff is a real change.
- **Nothing is invented.** The derived fields are conveniences
  computed from columns already present; the JSON adds no fact the
  CSV does not carry.
- `catalog_version` is the release tag the export was built from,
  so a downstream cache can be invalidated on it.

Build it yourself with
`python3 tools/build_json_export.py --out ocn-1.json --pretty`
(drop `--pretty` for the compact form: about 3.3 MB against 4.5 MB
indented).

## 12. Links

- Spec: [`spec/OCN-1.md`](../spec/OCN-1.md)
- Roadmap: [`traction-roadmap.md`](traction-roadmap.md)
- Release: [ocn-1.2.0](https://github.com/escacsfigueres/ocn/releases/tag/ocn-1.2.0)
- Lichess cross-reference (in-repo sidecar):
  [`catalog/ocn-1.lichess-xref.tsv`](../catalog/ocn-1.lichess-xref.tsv)
- Scalar ECO join table (in-repo sidecar):
  [`catalog/ocn-1.eco.tsv`](../catalog/ocn-1.eco.tsv)
- ECO class-divergence list (in-repo sidecar):
  [`catalog/ocn-1.eco-divergence.tsv`](../catalog/ocn-1.eco-divergence.tsv),
  built by
  [`tools/build_eco_divergence.py`](../tools/build_eco_divergence.py)
- Popularity snapshot (in-repo sidecar, section 15):
  `catalog/ocn-1.popularity.tsv`, built by
  [`tools/build_popularity.py`](../tools/build_popularity.py) from the
  public Lichess opening explorer API
- Python package (catalogue bundled): `pip install ocn-chess` —
  source at [`src/ocn/`](../src/ocn/), data refreshed by
  [`tools/sync_package_data.py`](../tools/sync_package_data.py)
- In-repo Python reader: [`tools/ocn.py`](../tools/ocn.py)
- JSON export builder:
  [`tools/build_json_export.py`](../tools/build_json_export.py)

## 13. Release artefacts

Every `ocn-*` tag is built and published by
[`.github/workflows/release.yml`](../.github/workflows/release.yml),
which reruns the full CI gate, rebuilds the derived files from
`catalog/ocn-1.csv` and attaches exactly these eight assets:

| asset | what it is |
|---|---|
| `ocn-1.csv` | the canonical catalogue, 14 columns |
| `ocn-1.json` | the whole catalogue as one JSON document (schema `ocn.catalog.v1`), section 11 |
| `ocn-1.positions.tsv` | one row per concrete slug: `fen_key`, full FEN, transposition-group size, SAN movetext, EPD and the Polyglot `zobrist`, section 4 |
| `ocn-1.lichess-xref.tsv` | Lichess opening lines mapped to OCN slugs |
| `ocn-1.eco.tsv` | scalar join table, one row per (slug, ECO code), section 9 |
| `ocn-1.eco-divergence.tsv` | rows whose OCN class letter is absent from their ECO codes, section 10 |
| `ocn_chess-*.whl`, `ocn_chess-*.tar.gz` | the `ocn-chess` Python package, catalogue bundled |
| `SHA256SUMS` | sha256 of every asset above |

Pin by sha256 from `SHA256SUMS` if you need reproducibility
(`escacsfigueres/ocn` is private — download via an authenticated
`gh release download`, not raw URLs).

The published `ocn-1.positions.tsv` is byte-identical to the copy
inside the wheel: the workflow builds it with the same options
`tools/sync_package_data.py` uses and fails if the two differ.

**No parquet.** Releases up to 1.2.0 carried `openings.parquet` and
`_efcdb_manifest.json`, generated from the private `chess-parquet`
repo. They are gone by decision (roadmap decision 8): everything OCN
publishes is now buildable from `catalog/` alone. The one thing that
made those files load-bearing — the Polyglot zobrist — moved into the
positions sidecar in roadmap H2.8 and is computed here in stdlib Python.
The hashes are unchanged by the move: the same positions produce the
same 64-bit keys the parquet carried, so a join written against 1.2.0
keeps working.

## 14. Naming games: `ocn annotate`

If what you have is games rather than positions, the whole join is one
command. It reads a multi-game PGN (or `-` for stdin) and writes the
same PGN back with two tags added per game:

```
ocn annotate games.pgn --stats > named.pgn
```

```
[ECO "B90"]
[OCN "B.Sic.Naj.Eng"]
[OCNName "Sicilian Najdorf, English Attack"]
```

The tags go after `ECO` if the game has one, else after `Round`.
Everything else survives untouched: movetext is never reflowed,
comments, NAGs, variations, unknown tags and line endings all come
through as written. Re-annotating a file rewrites its OCN tags in place
rather than stacking duplicates, so the command is idempotent.

**The matching rule.** Every position the mainline passes through is
looked up in the catalogue's `fen_key` index and the *last* hit wins —
then `transposes_to` is followed once. Two consequences worth knowing
before you compare notes with an ECO-keyed tool:

- Move order does not matter. A game that reaches the Najdorf English
  Attack via 1.Nf3 gets `B.Sic.Naj.Eng`, the same as one that plays
  1.e4. Prefix matching over `moves_uci` cannot do this; position
  matching gets it for free.
- Variations are ignored. The annotation describes the game that was
  played, not the analysis attached to it.

Games are replayed to a ply cap (`--max-plies`, default 40, the deepest
catalogue line plus slack); the rest of the movetext is never parsed,
which is what keeps a million-game file to minutes rather than hours.

The same matcher is available as a library, one catalogue load for a
whole corpus:

```python
from ocn.annotate import Annotator, annotate_text, iter_matches

text, stats = annotate_text(open("games.pgn").read())
print(stats.match_rate, stats.median_ply, stats.top(10))

annotator = Annotator()                       # loads the bundled catalogue
for game, match in iter_matches(open("huge.pgn"), annotator):
    ...                                       # match.slug, match.name, match.ply
```

**Reading the numbers.** `--stats`, and the fuller report from
[`tools/coverage_stat.py`](../tools/coverage_stat.py), print a match
rate — but every legal first move is a catalogue row, so any game with
one move played counts as matched and the rate sits at ~100% on real
corpora. The informative figures are the median match depth and the
share of games still named at 8, 12 and 16 plies, which is why
`coverage_stat.py` prints that table. Quote those.

## 15. The popularity sidecar

`catalog/ocn-1.popularity.tsv` (roadmap H2.7) answers the one question
the catalogue never could: how often is this line actually played. One
row per concrete slug, eleven columns, built by
[`tools/build_popularity.py`](../tools/build_popularity.py) from the
public **Lichess opening explorer API** and nothing else.

| column | what it is |
|---|---|
| `ocn1` | the slug, the join key |
| `masters_games` | games in the **Lichess masters database** that reached this position (`masters_white + masters_draws + masters_black`) |
| `masters_white`, `masters_draws`, `masters_black` | the outcome split of that same total |
| `lichess_games` | games in the **Lichess games database** that reached it, restricted to rated blitz, rapid and classical in the 1800/2000/2200/2500 rating bands |
| `top_player`, `top_player_elo` | the highest-rated player, either colour, **among the sampled top games** the API returns for the position |
| `top_game_year_earliest`, `top_game_year_latest` | the year range **of that same small sample** |
| `retrieved` | ISO date of the snapshot, identical for every row of a run |

### Scoped claims, or the numbers become lies

Every figure belongs to the database it came from, and the column names
are short for readability, not for quotation. When you display or
publish these numbers:

- `masters_games` is **"games in the Lichess masters database"** — an
  OTB master collection of roughly three million games. It is never
  "games ever played" and never "how popular this opening is".
- `lichess_games` is **"games in the Lichess games database"** in the
  speeds and rating bands above. It is not "games on Lichess" (bullet
  and sub-1800 play are excluded by the query) and certainly not a
  world total.
- The two are **not addable**. They count different populations of
  players. The web explorer sums them internally to rank rows and never
  shows the sum, which is the right pattern to copy.
- `top_game_year_earliest` is **the earliest year among the sampled top
  games**, not the first time anyone played the line. The sample is the
  handful of highest-rated games the API returns, so a line played
  continuously since 1858 can easily report a 21st-century range.
  Labelling it as a first-played date would be false.
- `top_player` is **the strongest player in that sample**, not the
  opening's leading practitioner.

Rows the databases have never seen carry `0` in the five count columns —
a measured zero, not a gap — and empty `top_player`, `top_player_elo`
and year cells, because a sample of nothing supports no claim.

### Refreshing it

This is the one sidecar that is **not derived from the catalogue**, so
it has no drift test and regenerating it is not expected to be a no-op:
it is a dated snapshot of a database that grows every day. Regenerate it
whenever you like; the `retrieved` column is what dates the figures, and
a consumer comparing two releases should read it before comparing
counts.

Two operational facts before you run it:

- **The explorer API requires a Lichess OAuth token.** Anonymous
  requests have returned HTTP 401 since 3 March 2026, when Lichess
  disallowed them to stop a DDoS
  ([announcement](https://lichess.org/@/thibault/blog/the-opening-explorer-now-requires-authentication/FSWh9Zg3)).
  Mint a personal token at <https://lichess.org/account/oauth/token> —
  no particular scope is needed — and export it as `LICHESS_TOKEN`.
- **The published budget is 25 requests per minute.** The tool throttles
  to exactly that by default, which puts a full cold run at roughly
  eight hours for the ~11,500 requests the catalogue needs. Every
  response is cached on disk, so the run is resumable and a re-run is
  free; interrupt it whenever and start it again.

```
export LICHESS_TOKEN=lip_...
python3 tools/build_popularity.py                 # full run, resumable
python3 tools/build_popularity.py --limit 50      # a quick smoke test
python3 tools/build_popularity.py --offline       # rebuild from the cache
```

Requests are deduplicated by position, so the transpositions in the
catalogue cost nothing extra: 5,894 rows collapse to 5,765 distinct
positions.
