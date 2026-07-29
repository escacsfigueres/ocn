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

1. Compute the Polyglot zobrist hash of the position.
2. JOIN against `openings.parquet` on `zobrist`.
3. **Keep all rows returned** — do not deduplicate on zobrist.
4. For each row, derive `canonical_ocn1 = COALESCE(NULLIF(transposes_to, ''), ocn1)`.
5. Group / display per your UI: see
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

`openings.parquet` already materialises this in the `canonical_ocn1`
column (non-null for every row). For TSV consumers, derive it on
read.

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
| Polyglot zobrist hash (INT64) | `openings.parquet` | `zobrist` |
| Position object that can produce a Polyglot zobrist | `openings.parquet` | derive zobrist, then `zobrist` |
| FEN string | `ocn-1.positions.tsv`, or `tools/ocn.py` | `fen_key` (board + side + castling + ep, ignoring counters) |
| OCN slug | either, or `catalog/ocn-1.csv` directly | `ocn1` |
| Lichess opening name / line | `catalog/ocn-1.lichess-xref.tsv` | exact SAN sequence → `ocn1` (every Lichess line on a position OCN covers resolves to a slug) |

**Polyglot is the recommended canonical hash.** OCN's
`openings.parquet` is generated with `polyglot-v1.0` (see
`_efcdb_manifest.json` → `zobrist_variant`).

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

### Python, zero dependencies (`tools/ocn.py`)

If you are in Python and have the repo, the reader is the loop
library — no parquet stack needed:

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

```sql
SELECT
  zobrist,
  ocn1,
  canonical_name,
  COALESCE(NULLIF(transposes_to, ''), ocn1) AS canonical_ocn1,
  same_as
FROM read_parquet('openings.parquet');
```

`openings.parquet` already exposes `canonical_ocn1` as a
materialised column, so the COALESCE is only needed for TSV /
CSV consumers.

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
LEFT JOIN read_parquet('openings.parquet') o
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
  LEFT JOIN read_parquet('openings.parquet') o
    ON p.zobrist = o.zobrist
)
SELECT
  game_id, ply, zobrist,
  string_agg(DISTINCT canonical_name, ' / ' ORDER BY canonical_name)
    AS display_label
FROM joined
GROUP BY game_id, ply, zobrist;
```

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

## 10. The whole-catalogue JSON export

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

## 11. Links

- Spec: [`spec/OCN-1.md`](../spec/OCN-1.md)
- Roadmap: [`traction-roadmap.md`](traction-roadmap.md)
- Release: [ocn-1.2.0](https://github.com/escacsfigueres/ocn/releases/tag/ocn-1.2.0)
- Lichess cross-reference (in-repo sidecar):
  [`catalog/ocn-1.lichess-xref.tsv`](../catalog/ocn-1.lichess-xref.tsv)
- Scalar ECO join table (in-repo sidecar):
  [`catalog/ocn-1.eco.tsv`](../catalog/ocn-1.eco.tsv)
- Python reader: [`tools/ocn.py`](../tools/ocn.py)
- JSON export builder:
  [`tools/build_json_export.py`](../tools/build_json_export.py)

The release page hosts three downloadable artefacts:
`ocn-1.positions.tsv`, `openings.parquet`, and
`_efcdb_manifest.json`. Pin them by sha256 if you need
reproducibility (`escacsfigueres/ocn` is private — download via an
authenticated `gh release download`, not raw URLs).
