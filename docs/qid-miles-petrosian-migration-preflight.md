# QID Miles/Petrosian — migration preflight checklist

**Status**: PREFLIGHT (no catalogue change). Companion to
[`qid-miles-petrosian-structural-proposal.md`](qid-miles-petrosian-structural-proposal.md)
(Option A recommended). This document fully specifies the future
slug migration so the apply is mechanical and verifiable.

**Do not apply from this document.** The migration is OCN's first
slug-rename and changes `canonical_ocn1` downstream — it needs a
dedicated, GO'd, `chess-parquet`-coordinated commit. The **go/no-go
decision** (whether/when to apply) is recorded separately in
[`qid-migration-decision-record.md`](qid-migration-decision-record.md)
(recommendation: bundle with the next release/tag, not an immediate
out-of-band apply).

## Preflight finding (important)

The slug rename alone is **not sufficient**. The 10 descendants'
`canonical_name` fields still read **"QID Miles, …"** (e.g. "QID
Miles, Kasparov Attack"). Re-slugging to `E.QID.Pet.KPe.*` without
relabelling would leave the slug `E.QID.Pet.KPe.d5.cxd5.Qc2` named
"QID Miles, Kasparov Attack" — the naming lie would persist in the
`canonical_name` column. **The migration must relabel
`canonical_name` on all 10 descendants too** (proposed names below).

Aliases do **not** need changing (they are leaf descriptors — "d5
Line", "Kasparov Attack", "Romanishin Attack", etc. — none contains
"Miles"). Only `canonical_name` carries "Miles".

## Row to delete (1)

| slug | why | moves (after `…Nf3 b6`) |
|---|---|---|
| `E.QID.Mil.MLn` | duplicate of `E.QID.Pet.KPe` (identical moves + FEN); the correctly-named KPe survives | `a3 Bb7 Nc3` |

Its alias "Main Line" and name "QID Miles Variation, Main Line" are
discarded (KPe keeps its own correct name "QID Petrosian,
Kasparov-Petrosian").

## Rows to re-slug + relabel (10 descendants)

`moves_uci` is **unchanged** on every row — only `ocn1`,
`parent_ocn1`, and `canonical_name` change. All share the prefix
`d2d4 g8f6 c2c4 e7e6 g1f3 b7b6` (shown below as `…`).

| # | old_slug | new_slug | old_parent → new_parent | new canonical_name (proposed) | moves (after `…`) |
|---|---|---|---|---|---|
| 1 | `E.QID.Mil.MLn.Be7` | `E.QID.Pet.KPe.Be7` | `E.QID.Mil.MLn` → `E.QID.Pet.KPe` | QID Kasparov-Petrosian, Be7 | `a3 Bb7 Nc3 Be7` |
| 2 | `E.QID.Mil.MLn.d5` | `E.QID.Pet.KPe.d5` | `E.QID.Mil.MLn` → `E.QID.Pet.KPe` | QID Kasparov-Petrosian, d5 | `a3 Bb7 Nc3 d5` |
| 3 | `E.QID.Mil.MLn.d5.cxd5` | `E.QID.Pet.KPe.d5.cxd5` | `E.QID.Mil.MLn.d5` → `E.QID.Pet.KPe.d5` | QID Kasparov-Petrosian d5, cxd5 | `a3 Bb7 Nc3 d5 cxd5` |
| 4 | `E.QID.Mil.MLn.d5.cxd5.Nxd5` | `E.QID.Pet.KPe.d5.cxd5.Nxd5` | `…Mil.MLn.d5.cxd5` → `…Pet.KPe.d5.cxd5` | QID Kasparov-Petrosian cxd5, Nxd5 | `a3 Bb7 Nc3 d5 cxd5 Nxd5` |
| 5 | `E.QID.Mil.MLn.d5.cxd5.exd5` | `E.QID.Pet.KPe.d5.cxd5.exd5` | `…Mil.MLn.d5.cxd5` → `…Pet.KPe.d5.cxd5` | QID Kasparov-Petrosian cxd5, exd5 | `a3 Bb7 Nc3 d5 cxd5 exd5` |
| 6 | `E.QID.Mil.MLn.d5.cxd5.Qc2` | `E.QID.Pet.KPe.d5.cxd5.Qc2` | `…Mil.MLn.d5.cxd5` → `…Pet.KPe.d5.cxd5` | QID Kasparov-Petrosian, Kasparov Attack | `a3 Bb7 Nc3 d5 cxd5 Nxd5 Qc2` |
| 7 | `E.QID.Mil.MLn.d5.cxd5.e3` | `E.QID.Pet.KPe.d5.cxd5.e3` | `…Mil.MLn.d5.cxd5` → `…Pet.KPe.d5.cxd5` | QID Kasparov-Petrosian, Petrosian Attack | `a3 Bb7 Nc3 d5 cxd5 Nxd5 e3` |
| 8 | `E.QID.Mil.MLn.d5.cxd5.Qa4` | `E.QID.Pet.KPe.d5.cxd5.Qa4` | `…Mil.MLn.d5.cxd5` → `…Pet.KPe.d5.cxd5` | QID Kasparov-Petrosian, Rashkovsky Attack | `a3 Bb7 Nc3 d5 cxd5 Nxd5 Qa4` |
| 9 | `E.QID.Mil.MLn.d5.cxd5.e4` | `E.QID.Pet.KPe.d5.cxd5.e4` | `…Mil.MLn.d5.cxd5` → `…Pet.KPe.d5.cxd5` | QID Kasparov-Petrosian, Polovodin Gambit | `a3 Bb7 Nc3 d5 cxd5 Nxd5 e4` |
| 10 | `E.QID.Mil.MLn.d5.cxd5.Bd2` | `E.QID.Pet.KPe.d5.cxd5.Bd2` | `…Mil.MLn.d5.cxd5` → `…Pet.KPe.d5.cxd5` | QID Kasparov-Petrosian, Romanishin Attack | `a3 Bb7 Nc3 d5 cxd5 Nxd5 Bd2` |

(Order above is by tree depth for clarity; rows 4-10 all share the
new parent `E.QID.Pet.KPe.d5.cxd5`.)

## Slugs that do NOT change

| slug | role after migration |
|---|---|
| `E.QID.Mil` | **unchanged** — the real Miles Variation (`4.Bf4`), now a childless depth-2 leaf. Accurate: no catalogued 4.Bf4 sub-theory. |
| `E.QID.Pet.KPe` | **unchanged slug + name** — "QID Petrosian, Kasparov-Petrosian" (`4.a3 Bb7 5.Nc3`). Gains the migrated subtree as children. |
| `E.QID.Pet` | unchanged (the `4.a3` Petrosian root). |
| `E.QID.Pet.And`, `E.QID.Pet.Hdg`, `E.QID.Pet.Ba6*`, `E.QID.Pet.Kas*` | unchanged Petrosian siblings — none collide with the migrated slugs. |

## Downstream impact

| dimension | effect |
|---|---|
| schema | **no change** (14 columns, same contract) |
| catalogue rows | **5,900 → 5,899** (−1; `E.QID.Mil.MLn` deleted, subtree merges under existing KPe) |
| `unresolved_groups` | **2 → 1** (only Nimzo Bot/Kmo would remain) |
| `duplicate_groups` | **125 → 124** |
| `resolved_groups` | 123 (the group collapses; not counted as "resolved") |
| `multiple_canonical_groups` | 17 (unchanged) |
| FEN/positions | **none change** — moves_uci identical on all migrated rows |
| `canonical_ocn1` downstream | **10 slugs renamed** + 1 deleted → `chess-parquet` must **regenerate** `openings.parquet`, but **no code change** (schema identical) |
| version semantics | 11 rows change identity, 0 positions change → decide patch vs minor bump for the downstream contract |

## Verification checklist (for the future apply)

After applying the migration, confirm ALL of:

- [ ] No `E.QID.Mil.MLn` row remains (deleted).
- [ ] No `E.QID.Mil.MLn.*` slug remains (all 10 re-slugged).
- [ ] All 10 new slugs `E.QID.Pet.KPe.*` exist.
- [ ] Every new `parent_ocn1` resolves to an existing row
      (`E.QID.Pet.KPe`, `E.QID.Pet.KPe.d5`, `E.QID.Pet.KPe.d5.cxd5`).
- [ ] `E.QID.Pet.KPe` now has children; its own name/moves unchanged.
- [ ] `E.QID.Mil` still exists as a childless leaf (4.Bf4).
- [ ] `moves_uci` byte-identical on all 10 migrated rows (FEN unchanged).
- [ ] No `canonical_name` on any `E.QID.Pet.KPe.*` row still contains
      "Miles" (relabel complete).
- [ ] No `transposes_to`/`same_as` anywhere points at a deleted/old
      `E.QID.Mil.MLn*` slug.
- [ ] `validate.py --strict-chess` → 0 warnings; `audit_chess.py` →
      0 illegal/0 san_mismatch.
- [ ] `unittest discover tools/tests` → all green (update any test
      that references `E.QID.Mil.MLn*`).
- [ ] `audit_transpositions.py --summary` → `unresolved_groups=1`,
      `duplicate_groups=124`, rows=5,899.
- [ ] `lichess_parent_map.py --check` → still 3690/3690.
- [ ] `export_positions.py --include-roots --stats` → regenerates;
      note the new positions.tsv checksum for any downstream pin.
- [ ] `git diff --check` clean.

## Test-suite note

Grep the test suite for `E.QID.Mil.MLn` before applying — if any
test pins one of these slugs (e.g. an ambiguous-candidate assertion),
update it to the new `E.QID.Pet.KPe.*` slug as part of the migration
commit (precedent: the Najdorf slug update during an earlier batch).

## Apply gating (recap from the proposal)

1. Confirm `chess-parquet` absorbs the `canonical_ocn1` rename (or
   accept the regenerated `openings.parquet`).
2. Decide version semantics (patch vs minor).
3. Apply in a dedicated commit with explicit GO. Not folded into
   any other work.
