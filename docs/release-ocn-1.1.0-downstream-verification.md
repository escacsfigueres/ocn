# OCN 1.1.0 — downstream verification

**Verified**: 2026-05-27. Records that the **published** `ocn-1.1.0`
release was downloaded and consumed end-to-end by a real downstream
consumer. **Read-only — no catalogue change, no commit/push/tag/
release in the consumer repo.**

## What was verified

A real consumer (`chess-parquet`) downloaded the **published**
release assets (not the local build candidates) and confirmed they
are intact, schema-correct, and usable.

- **Consumer repo**: `/Users/albertpi/Code/chess-parquet` (HEAD
  `eef0989`, synced; pre-existing untracked files left untouched).
- **Account**: `escacsfigueres` (Active).
- **Mode**: read-only — no commit/push/tag/release anywhere.

## Download (private repo)

```bash
gh release download ocn-1.1.0 --repo escacsfigueres/ocn \
  --dir <tmp> --clobber
```

⚠️ `escacsfigueres/ocn` is **private** — bare
`github.com/.../releases/download/…` URLs return **404** to
unauthenticated requests. Consume via `gh release download`
(authenticated), as above.

## Asset integrity (downloaded-from-release sha256 = published)

| asset | size | sha256 | match |
|---|---|---|---|
| `ocn-1.positions.tsv` | 1,475,677 B | `0e78c315c62b1c37a7267b5df3c82f98e1af4e1ae0dbe8e9d47fc68211d89d7d` | ✅ |
| `openings.parquet` | 369,663 B | `a9180bfcd4fee272f0a9a76e866ffbe4ca2311ea68f373b435a5aff75209a5c2` | ✅ |
| `_efcdb_manifest.json` | 328 B | `a8aa50e904328e240290c1f17c56578a3c71875629f953b901ff551ca4ede9f6` | ✅ |

Manifest: `efcdb_version 1.3`, `rows 5899`, `zobrist_variant
polyglot-v1.0`, `source ocn-1.1.0-candidate-e297d36`.

## Smoke-test (on the downloaded `openings.parquet`) — 8/8 OK

| check | result |
|---|---|
| parquet rows | **5,899** ✅ |
| `E.QID.Mil.MLn*` present | **0** ✅ |
| `E.QID.Pet.KPe.*` present | **10** ✅ |
| `E.Nim.Sml.Kmo.canonical_ocn1` | **`E.Nim.Sml.Bot`** ✅ |
| `same_as` non-empty rows | **34** (= 17 multi-canonical × 2) ✅ |
| multi-row zobrist groups | **124** (= duplicate_groups) ✅ |
| `canonical_ocn1` rule violations | **0** (rule: `transposes_to` if set else `ocn1`) ✅ |
| QID `…Qc2` name | "QID Kasparov-Petrosian, Kasparov Attack" — no "Miles" ✅ |

## Producer tests

```
cargo test -p efcdb-openings -p efcdb-core   →   15 + 10 passed
```

## Conclusion

`ocn-1.1.0` is verified **end-to-end from a real consumer's
perspective**: the published assets download intact (sha256 match),
the `openings.parquet` carries the expected schema/counts, the QID
slug-migration is coherent downstream (new slugs present, old absent,
`canonical_ocn1` correct), and the producer tests pass. **No
downstream risk.** The only operational note: the repo is private, so
consume via `gh release download`, not public URLs.
