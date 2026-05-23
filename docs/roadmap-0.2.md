# OCN 0.2 — roadmap and downstream readiness

**Status as of**: post-commit `432a079` (Add same_as resolved
transpositions).
**Scope**: consolidates the work since OCN 0.1 (catalogue +
validator) and lays out the next phases through public alpha.

## 1. Current state

### Catalogue snapshot

| metric | value |
|---|---|
| rows | 5,966 |
| unique FENs (concrete entries) | 5,765 |
| duplicate FEN groups | 191 |
| — resolved (any kind) | 75 |
| — — single_canonical | 69 |
| — — multiple_canonical | 6 |
| — unresolved | 116 |
| rows in unresolved groups | 233 |
| rows with `transposes_to` set | 73 |
| rows with `same_as` set | 12 |
| FENs with ≥2 canonical OCNs ⭐ | 122 |
| classes_mixed_groups | 0 |
| Tests | 60 / 60 OK |
| Validator (`--strict-chess`) | 0 warnings |
| `audit_chess` (legality + SAN) | 0 illegal, 0 mismatch |
| Lichess parent map | 3,690 / 3,690 matched |

⭐ The "FENs with ≥2 canonical OCNs" count (122) is the metric
that matters most to downstream zobrist joins. It includes both
the 6 declared `multiple_canonical` groups AND the unresolved
groups where ≥2 rows happen to share a FEN without (yet) being
linked by `transposes_to` or `same_as` declarations. **Consumers
joining on zobrist MUST handle multi-row returns regardless of
which kind they encounter.** The 6-vs-122 gap will shrink as the
intra-family audit progresses (Phase 1), but it will never reach
1:1 — the 6 declared cases are intentional preservation, not a
TODO.

### Schema

The catalogue CSV has 14 columns:

```
ocn1, canonical_name, eco_legacy, parent_ocn1, moves_uci, depth,
aliases, flags, notes, attributed_to, attribution_source,
historical_notes, transposes_to, same_as
```

Three slug-level relations are in production:

- `parent_ocn1` — nominal hierarchy (literature lineage).
- `transposes_to` — canonicalisation by position, **asymmetric**
  (non-canonical → canonical).
- `same_as` — co-canonical preservation, **symmetric** (canonical ↔
  canonical).

### Tooling

| tool | role |
|---|---|
| `tools/validate.py` | format + legality + same_as / transposes_to semantics |
| `tools/audit_chess.py` | non-stopping legality and SAN cleanup |
| `tools/audit_transpositions.py` | classifies FEN-duplicate groups as `unresolved`, `single_canonical` or `multiple_canonical`; default report hides resolved groups; `--include-resolved` shows them |
| `tools/export_positions.py` | derived TSV/JSON with `fen_key`, normalised `fen`, `transposition_group_size`, `transposes_to`, `same_as` |
| `tools/from_eco.py`, `from_uci.py`, `from_position.py` | lookup tools, ECO/UCI/FEN entry points |
| `tools/lichess_parent_map.py` | layers Lichess Opening Book on top of OCN |

### What 0.2 already settled

- **Position canonicalisation primitives (`transposes_to` + `same_as`)
  are in production** with validator, audit and export support.
- **Audit reports `resolved_groups` vs `unresolved_groups` cleanly**;
  resolution kinds are first-class (`single_canonical` /
  `multiple_canonical`) and exposed in TSV/JSON output and in
  `--summary`.
- **Arbitration policy is documented in the spec** (7 ordered
  rules + "Do not resolve automatically" carve-outs in
  `spec/OCN-1.md`).
- **6 multiple_canonical groups recorded** (French/Veresov,
  KID Classical Old/e5, Rubinstein/Colle-Zukertort, Nimzo
  Kmoch/Botvinnik, Italian Giuoco/Two Knights × 2 depths).
- **classes_mixed_groups dropped to 0** — no remaining cross-class
  conceptual mixers in the unresolved set.

## 2. What still remains in the unresolved set

The 116 unresolved groups fall into three honest buckets.

### 2.1 Intra-family, both sides with substantive children

Examples from the current top 15:

- `E.KID.Fch.Kav` ⇄ `E.KID.Fch.Kav.Nc3.e5` (rank 1, score 10)
- `D.Sem.Mer.MLn.Old` ⇄ `D.Sem.Mer.MLn.c5.e5` (rank 2)
- `E.Gru.Rus.Hng` ⇄ `E.Gru.Rus.Hng.e4` (rank 3)
- `A.Eng.Mik` ⇄ `A.Eng.Agi.Nc3.Nf6.e4` (rank 4)
- `C.RyL.Mor.Car.MLn` ⇄ `C.RyL.Mor.Ba4.b5.Bb3` and the depth-2
  pair (ranks 5–6)
- `C.PhD.Nim` ⇄ `C.PhD.Lio.MLn.O-O` (ranks 8–9)
- `E.KID.Avk` ⇄ `E.KID.Avk.Cst.Bg5` (rank 7)
- `D.Sem.AMe` ⇄ `D.Sem.AMe.Sto`, `D.Sla.Cze.Kra` ⇄ `Kra.MLn`,
  `D.QGD.Exc.Min.h6.Bh4` etc. (ranks 11–14)

These need per-case judgement — each is either a parent-child
mirror (resolve with TT to the parent or delete) or a sibling
mirror (pick canonical, TT or delete the other). Most are
mechanical once a single decision is made per pair.

### 2.2 Triple groups with unique structure

- `A.Van.ReN.e3.d5` ⇄ `A.Van.d5.e3.e5` ⇄ `A.VtK.e5.Nc3.d5` (rank
  10): three-way Van Geet / Van't Kruijs convergence. All three
  have children. Needs a small structural plan.

### 2.3 Long-tail intra-family residuals

- 100+ groups with score ≤ 5 buried below rank 30. Mostly
  intra-Slav, intra-QGD, intra-Italian deep duplicates similar to
  the patterns the previous batch sprints handled. Mechanical
  cleanup, low information density.

## 3. Roadmap for OCN 0.2

Four phases, ordered by leverage.

### Phase 1 — finish intra-family audit

**Target**: `unresolved_groups < 50` (down from 116). 

Approach:

- Two more multi-agent sweeps over the top 60–80, scoped to
  intra-family pairs (single class). Same pattern as the previous
  successful batch sprints.
- Pair-by-pair TT + delete for the parent/child same-FEN cases.
- Use `same_as` where two real names actually exist (rare at this
  point — the top of the queue is mostly structural mirrors, not
  literary duplicates).
- Honest defer for the Van triple and the Caro/b5 Spanish family
  if they require structural plans.

**Estimated cost**: 3–4 multi-agent sprints. Each removes 15–30
unresolved groups.

**Exit criterion**: top 30 ranked groups are all either deferred
with documented conceptual reasons or below a `score=4` noise
threshold.

### Phase 2 — downstream integration with `chess-parquet`

**Target**: `efcdb-openings` consumes the OCN 0.2 schema and
canonicalises positions correctly.

Required changes in `escacsfigueres/chess-parquet`:

- **Read the 14-column header**. Both `transposes_to` and
  `same_as` must be schema-aware (not just preserved as opaque
  strings).
- **Produce `openings.parquet` with both relations** as
  pass-through columns alongside `ocn1` and the derived
  Polyglot `zobrist`. Schema:

  ```
  ocn1 string
  canonical_name string
  eco_legacy string
  parent_ocn1 string [nullable]
  depth int
  moves_uci string [nullable]
  zobrist int64
  fen_key string
  transposes_to string [nullable]
  same_as string [nullable]
  ```

- **Canonicalisation rules for consumers**:

  ```
  if row.transposes_to is not null:
      canonical_ocn1 = row.transposes_to
  else:
      canonical_ocn1 = row.ocn1

  co_canonicals = [row.ocn1] + parse_pipe(row.same_as)
  ```

  Same FEN may have **multiple canonical rows by design**.
  Consumers MUST NOT assume a single OCN per zobrist when joining
  with position-indexed datasets — there are 6 known
  `multiple_canonical` groups today and more may appear as the
  intra-family audit completes.

- **Zobrist join contract**:

  ```
  positions p
  LEFT JOIN openings o ON p.zobrist = o.zobrist
  ```

  may return multiple rows per `p.zobrist`. The consumer chooses
  how to render the multiple canonicals — typically grouping by
  zobrist and concatenating the `canonical_name` field.

- **Lichess long-tail layering** stays unchanged; the Lichess
  fallback is unaffected by `same_as`.

**Estimated cost**: 1 sprint in the chess-parquet repo. Schema
extension is the bulk of the work; consumer-side query change is
small.

**Exit criterion**: `chess-parquet`'s test suite consumes
`catalog/ocn-1.csv` directly and produces a `openings.parquet`
that round-trips both relations.

### Phase 3 — release artefacts

**Target**: ship the OCN 0.2 release bundle.

Artefacts:

| artefact | source | purpose |
|---|---|---|
| `catalog/ocn-1.csv` | this repo | primary text catalogue, 14 columns |
| `ocn-1.positions.tsv` | `tools/export_positions.py` | derived position index for grep / awk / spreadsheets |
| `ocn-1.transpositions.tsv` (new) | `tools/audit_transpositions.py --ranked --include-resolved --json | jq ...` or a new flag | exported audit state for downstream consumers wanting the resolved/unresolved status per group |
| `openings.parquet` | `chess-parquet`'s `efcdb-openings` | columnar artefact with Polyglot zobrist |

`ocn-1.transpositions.tsv` is the only new artefact. It can be
produced by extending `tools/audit_transpositions.py` with an
`--export-resolution` flag that emits a flat TSV (one row per slug
in any duplicate group, with `resolution_kind`, `canonical_count`
and the slug's own role). Out of scope for this roadmap document
but small.

### Phase 4 — public alpha / beta

**Target**: open call for community feedback.

Pre-release checklist:

- [ ] Phase 1 complete (unresolved_groups < 50).
- [ ] Phase 2 complete (chess-parquet consumes 0.2).
- [ ] Phase 3 artefacts produced and pinned to a release tag.
- [ ] Spec updated with a "Migrating from 0.1" section if any
      consumer of 0.1 exists in the wild.
- [ ] Lichess integration documented end-to-end (parent_map +
      position fallback).
- [ ] Public README has an "open call" link.

## 4. Downstream change list for `chess-parquet`

Concrete changes the `efcdb-openings` crate needs to make for 0.2
support:

1. **CSV reader update**:
   - Expect 14 columns. Currently expects 13.
   - New columns: `same_as` (string nullable, pipe-separated).
   - Reject CSVs with fewer columns (the existing
     "missing-column" guard already does this for `transposes_to`;
     extend to `same_as`).

2. **Parquet schema update**:
   - Add `same_as` field (string, nullable).
   - Keep `transposes_to` as it is.
   - No breaking change to existing zobrist column.

3. **Canonicalisation helper API**:
   - Provide a method `canonical_ocn1(row)` that returns
     `row.transposes_to` if non-null, else `row.ocn1`.
   - Provide a method `co_canonical_ocn1s(row)` that returns
     `[row.ocn1, *parse_pipe(row.same_as)]`.
   - Test that the helpers cover all 6 current
     `multiple_canonical` cases.

4. **Join contract documentation**:
   - State explicitly that `zobrist → ocn1` is **not** a function;
     it is a multi-valued relation. Document this in the
     `chess-parquet` README, not just code comments.

5. **Test data**:
   - Sync `chess-parquet`'s test catalogue copy to the current
     OCN 0.2 head (or remove the local copy and read directly
     from this repo).

## 5. Definition of done for OCN 0.2

The release is done when **all** of the following hold:

- [ ] `tools/audit_transpositions.py --summary` reports
      `unresolved_groups < 50`.
- [ ] All resolved groups in the audit are documented (each one
      either has a `transposes_to`/`same_as` declaration, or sits
      in an explicit deferred list in `docs/transpositions.md`).
- [ ] `chess-parquet` consumes the 0.2 schema and round-trips
      both relations to `openings.parquet`.
- [ ] `ocn-1.positions.tsv` is reproducible from
      `tools/export_positions.py` and pinned to a release tag.
- [ ] A 0.2 git tag exists on this repo's `main`.
- [ ] `docs/transpositions.md` is current as of the tag.
- [ ] `spec/OCN-1.md` is current as of the tag.

When all six boxes are checked, OCN 0.2 ships as a tag and a
pinned bundle. 0.3 (internationalised aliases) is then on deck.

## 6. Recommended next implementation sprint

**The natural next step is `chess-parquet`, not more catalogue
cleanup.**

Reasoning:

- The 116 unresolved groups are mostly low-leverage long-tail
  cleanup (Phase 1 work that grinds down slowly).
- `chess-parquet` is **blocked on the OCN schema being stable**.
  Now that 0.2's schema is in production with all three relations,
  it is the right moment to update downstream **before** more
  catalogue churn could invalidate downstream test fixtures.
- Once `chess-parquet` consumes 0.2 cleanly, future catalogue
  cleanup is automatically reflected downstream; without that
  channel, each cleanup adds drift.

Concrete first sprint in `chess-parquet`:

1. Extend `efcdb-openings` to read 14 columns.
2. Add `same_as` to the Parquet schema.
3. Implement `canonical_ocn1` and `co_canonical_ocn1s` helpers.
4. Update fixture catalogue copy to current OCN 0.2 head.
5. Write a smoke test that joins a sample positions table against
   the current catalogue and confirms multi-canonical FENs return
   multiple rows.

After that, return to this repo for Phase 1 intra-family cleanup,
with the downstream pipeline tracking new commits.
