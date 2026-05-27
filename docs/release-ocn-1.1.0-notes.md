# OCN 1.1.0 — fully resolved transposition catalogue

**Release notes (draft — tag not yet created).** Docs-only record;
no tag/release/upload accompanies this document.

- **Proposed release**: `OCN 1.1.0 — fully resolved transposition catalogue`
- **Proposed tag**: `ocn-1.1.0` (minor bump — first slug-rename; slug
  identity is not guaranteed stable across this boundary)
- **Target commit**: current `main` (the release-cycle head; this
  notes commit or its successor)
- **Previous release**: `ocn-1.0.3` (`dd2abd3`)

## Summary

The transposition layer is **fully resolved**: every duplicate-FEN
group in the catalogue is now classified.

- **0 unresolved duplicate-FEN groups** (was 116 at the start of the
  post-0.2 cleanup; 31 at the start of this push series).
- **QID Miles/Petrosian slug-migration applied** — the mislabelled
  a3/Nc3 Kasparov-Petrosian subtree was re-homed under
  `E.QID.Pet.KPe` (OCN's first slug-rename).
- **Nimzo Bot/Kmo naming fixed** — `E.Nim.Sml.Kmo` (spurious
  "Kmoch") → `transposes_to E.Nim.Sml.Bot`, relabelled "a3 Move
  Order"; "Kmoch" stays at 4.f3 (`E.Nim.Fou`), per Lichess E20.
- **`same_as` / `transposes_to` contract unchanged** — same two
  resolution channels, same semantics.
- **Schema unchanged** — 14-column catalogue, 13-column
  `openings.parquet` (incl. `canonical_ocn1`, `zobrist`).

## Metrics (at the release head)

| metric | value | vs `ocn-1.0.3` |
|---|---|---|
| catalogue rows | 5,899 | (1.0.3 baseline) |
| duplicate_groups | 124 | — |
| resolved_groups | 124 | — |
| **unresolved_groups** | **0** | down from the long-tail |
| multiple_canonical_groups | 17 | grew via the `same_as` programme |
| schema columns | 14 (catalogue) / 13 (parquet) | unchanged |

## Compatibility / breaking note

⚠️ **This is OCN's first slug-rename.** Slug identity is **not**
guaranteed stable across release tags — `ocn-1.1.0` establishes that
precedent.

- **10 canonical OCN slugs changed**: `E.QID.Mil.MLn.* →
  E.QID.Pet.KPe.*` (the QID Kasparov-Petrosian subtree), and the
  duplicate `E.QID.Mil.MLn` was deleted.
- **No FEN / moves_uci / zobrist / schema change** for those
  positions — only the slug identity (and `canonical_name`
  "Miles" → "Kasparov-Petrosian") moved.
- **Consumers pinning `E.QID.Mil.MLn*` slugs must update** to the
  `E.QID.Pet.KPe.*` names. Position-lookup consumers joining on
  FEN/zobrist are unaffected.

## Assets (candidate — sha256)

Regenerated against the migrated catalogue; local candidates pending
upload at tag time.

| asset | size | sha256 |
|---|---|---|
| `ocn-1.positions.tsv` | 1,475,677 B | `0e78c315c62b1c37a7267b5df3c82f98e1af4e1ae0dbe8e9d47fc68211d89d7d` |
| `openings.parquet` | 369,663 B | `a9180bfcd4fee272f0a9a76e866ffbe4ca2311ea68f373b435a5aff75209a5c2` |
| `_efcdb_manifest.json` | 328 B | `a8aa50e904328e240290c1f17c56578a3c71875629f953b901ff551ca4ede9f6` |

`_efcdb_manifest.json`: `efcdb_version 1.3`, `rows 5899`,
`zobrist_variant polyglot-v1.0`, `source
ocn-1.1.0-candidate-<commit>`. **Regenerate fresh at tag time** if
the head moves; do not reuse `ocn-1.0.3` checksums.

## Downstream (chess-parquet)

> **Post-release downstream verification (2026-05-27):** the
> published release was downloaded by a real consumer and verified
> end-to-end (sha256 match, 8/8 smoke-test, producer tests green).
> See
> [`release-ocn-1.1.0-downstream-verification.md`](release-ocn-1.1.0-downstream-verification.md).

The `efcdb-cli openings` producer was run against the migrated
catalogue and **smoke-tested**:

- `openings.parquet` rows **5,899**; schema **unchanged** (13 cols);
  `canonical_ocn1` rule **0 violations**; `transposes_to` 112,
  `same_as` 34; distinct zobrist 5,765, **124 multi-row zobrist
  groups** (= duplicate_groups).
- QID migration absorbed cleanly: **0** `E.QID.Mil.MLn*`, **10**
  `E.QID.Pet.KPe.*` in the parquet — **no producer code change**.
- `cargo test -p efcdb-openings -p efcdb-core` → 15 + 10 passed.

## Upgrade guidance (from `ocn-1.0.3`)

- If you pinned `ocn-1.0.3`, expect the **QID slug names to change**
  on upgrade (`E.QID.Mil.MLn.* → E.QID.Pet.KPe.*`); update any
  hard-coded slug references.
- `canonical_ocn1` is still computed by the **`transposes_to` rule**
  (canonical_ocn1 = `transposes_to` if set, else `ocn1`).
- **`same_as` semantics are unchanged** — symmetric co-canonical
  pairs (17 groups), still joined many-to-one on zobrist downstream.
- Nimzo: the depth-3 Sämisch `E.Nim.Sml.Kmo` is now "a3 Move Order"
  (transposes to `E.Nim.Sml.Bot`); "Kmoch" is `E.Nim.Fou` (4.f3).

## Open follow-ups (NOT in this release)

- `E.Nim.Rub.Kmo`'s "Kmoch" is the same artifact as the fixed Nimzo
  case — a cosmetic relabel for a future pass (does not affect
  resolution counts).
- `E.Nim.Sml.Kmo.MLn` parent-chain quirk (cosmetic).

Both are documented in
[`nimzo-botvinnik-kmoch-apply-preflight.md`](nimzo-botvinnik-kmoch-apply-preflight.md);
neither blocks the release.
