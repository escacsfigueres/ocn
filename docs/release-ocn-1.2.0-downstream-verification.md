# OCN 1.2.0 — downstream verification

**Verified**: 2026-06-11, same day as the release. Records that the
**published** `ocn-1.2.0` release assets are intact, schema-correct and
byte-identical to the gate-verified candidates, and that the producer
pipeline consumed the 1.2.0 catalogue cleanly.

## Build provenance

- **Producer**: `efcdb-openings 0.1.0` (`chess-parquet`), run from an
  isolated worktree at `origin/main` = `f5e3b40` — the main worktree was on
  a foreign feature branch with uncommitted work and was not touched.
- **Input**: `catalog/ocn-1.csv` at `feb1098` (= tag `ocn-1.2.0`), sha256
  `255ab28006ed…`.
- **Manifest**: `efcdb_version 1.3`, `rows 5899`, `zobrist_variant
  polyglot-v1.0`, `source ocn-1.2.0-candidate-feb1098`.
- **Positions export**: `tools/export_positions.py --include-roots`
  (stats: rows 5,899, concrete 5,894, unique_fen 5,765,
  duplicate_groups 124).

## Asset integrity (downloaded-from-release sha256 = staged candidates)

| asset | size | sha256 | byte-identical |
|---|---|---|---|
| `ocn-1.positions.tsv` | 1,476,314 B | `b57380b874d59fd3d11205ba7e1bfbdc6c55d06866f73db2ac7db26a633b466c` | ✅ |
| `openings.parquet` | 369,453 B | `e1292c4c32bf7ffa4b624890c59318ad09684b63b0cdd185468506e7dd06638f` | ✅ |
| `_efcdb_manifest.json` | 328 B | `c9d1d7f22ec6ce17584465d13af3c30bdd67676bbe013fd1c05a3fa4d8d3d573` | ✅ |

Download path (private repo): `gh release download ocn-1.2.0 --repo
escacsfigueres/ocn` — unauthenticated asset URLs return 404.

## Candidate gate (run pre-tag on the staged parquet)

| check | result |
|---|---|
| parquet rows / columns | **5,899 / 13** (1.1.0 schema) ✅ |
| unmatched slugs, both directions | **0** ✅ |
| drift vs catalogue across all 11 shared columns | **0 cells** ✅ |
| `canonical_ocn1` rule violations (`transposes_to` else `ocn1`) | **0** ✅ |
| multi-row zobrist groups (nulls excluded) | **124** (= 1.1.0 = transposition audit) ✅ |
| null-zobrist rows | 5 (= the A–E class roots, by design) ✅ |
| `same_as` non-empty rows | **34** (= 17 co-canonical pairs × 2) ✅ |
| 1.2.0 spot checks: `A.Ret.d5.c4` "Réti Opening, 2.c4", `B.KPG` "King's Pawn Opening", `A.Ret.d5.g3` rename, `C.RyL` "Ruy López" | all ✅ |
| "López" canonicals 307, residual ASCII "Lopez" | **0** ✅ |
| `A.Lon` eco `D02`, `E.QID.Nim` eco `E15` in parquet | ✅ |
| downloaded parquet re-read | 5,899 rows ✅ |

## Producer tests

```
cargo test -p efcdb-openings -p efcdb-core   →   15 + 10 passed
```

## Join-key contract

Zero `ocn1` changes vs `ocn-1.1.0`: consumers keyed by slug, FEN or
zobrist are unaffected. Only name-string joins see the 683
`canonical_name` updates — which is the point of the release.
