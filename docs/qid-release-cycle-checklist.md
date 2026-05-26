# QID slug-migration — release-cycle checklist (Option C)

**Decision**: **Option C selected** (from
[`qid-migration-decision-record.md`](qid-migration-decision-record.md)).
The QID slug-migration is **not** an out-of-band apply; it rides a
release cycle whose end state is **`unresolved_groups=0`**, with
regenerated artefacts and a new tag.

**Status**: PLAN ONLY. **Nothing is applied or executed here, and
`catalog/ocn-1.csv` is not touched.** This is the ordered runbook
for when the release cycle is GO'd.

## Goal of the cycle

Apply the QID slug-migration (re-slug the mislabelled
Kasparov-Petrosian subtree under `E.QID.Pet.KPe`), reach a clean
**0-unresolved** catalogue, regenerate downstream artefacts, and cut
a new tagged release with assets.

## Ordered steps

> Each step is GO-gated; do not chain them without checking the
> previous one. Steps 2 and 5 are the only ones that mutate state
> (catalogue / downstream artefacts).

1. **Pre-apply safety snapshot** — record the baseline before
   touching anything:
   - `git status -sb` (clean, on `main`, synced)
   - `python3 tools/validate.py --strict-chess catalog/ocn-1.csv` → 0 warnings
   - `python3 tools/audit_transpositions.py --summary` → `unresolved_groups=1`, rows=5,900
   - `python3 -m unittest discover tools/tests` → 60/60
   - grep tests for `E.QID.Mil.MLn` (update any pinned assertion as part of step 2)

2. **Apply the QID slug-migration** per
   [`qid-miles-petrosian-migration-preflight.md`](qid-miles-petrosian-migration-preflight.md):
   delete `E.QID.Mil.MLn`, re-slug its 10 descendants
   `E.QID.Mil.MLn.* → E.QID.Pet.KPe.*` (fix `parent_ocn1`), relabel
   `canonical_name` to drop "Miles" → "Kasparov-Petrosian". No
   `moves_uci`/FEN change; no schema change.

3. **Validate the migrated catalogue** — expected after step 2:
   - rows **5,899** (−1: `E.QID.Mil.MLn` deleted)
   - duplicate_groups **124** (−1)
   - resolved_groups **124** (the group collapses; not counted resolved)
   - **unresolved_groups 0** ✅
   - multiple_canonical_groups **17** (unchanged)
   - `validate.py --strict-chess` 0 warnings · `audit_chess.py` 0/0 · tests 60/60 · `lichess_parent_map.py --check` 3690/3690
   - run the preflight's 14-point verification checklist (no old
     `E.QID.Mil.MLn*` left, all new parents resolve, no "Miles" in
     any `E.QID.Pet.KPe.*` canonical_name)

4. **Export the position index** —
   `python3 tools/export_positions.py --include-roots --stats --out /tmp/ocn-1.positions.tsv`
   (record the new row/group counts).

5. **Regenerate `openings.parquet`** via `chess-parquet`'s
   `efcdb-openings` producer against the migrated catalogue
   (coordinate in that repo).

6. **Downstream smoke test** — confirm the producer:
   - absorbs the 10 renamed `canonical_ocn1` values
     (`E.QID.Mil.MLn.* → E.QID.Pet.KPe.*`) without error,
   - emits the same schema (no column change),
   - the parquet's zobrist/identity columns are unchanged for all
     unaffected positions (only the QID rows' slug identity moves).

7. **Update docs / changelog** —
   - mark this checklist's steps done,
   - update `docs/transpositions.md` Current state to
     `unresolved_groups=0` / `resolved_groups=124`,
   - update `docs/transposition-cleanup-closure.md` to "0 holds —
     fully resolved",
   - write a changelog/consumer note: "slug-migration: 10
     `E.QID.Mil.MLn*` → `E.QID.Pet.KPe*`, 1 delete; no FEN/schema
     change; canonical_ocn1 identity changed for 11 rows".

8. **Tag the release** — proposed tag below (decide patch vs minor):
   - `git tag -a <tag> -m "OCN 0.2 — 0 unresolved; QID slug-migration"`
   - `git push origin <tag>` (separate explicit GO)

9. **Upload release assets + checksums** —
   - `shasum -a 256 /tmp/ocn-1.positions.tsv /tmp/openings.parquet /tmp/_efcdb_manifest.json`
   - `gh release create <tag> --title … --notes-file … <assets>`
   - record the new sha256s in `docs/release-0.2-checklist.md`-style note.

## Tag-name decision (confirm at release)

This is **OCN's first slug-rename** — 11 rows change `ocn1`
identity (no positions change). Options:

- **`ocn-1.1.0`** (minor bump) — **recommended**: signals to
  downstream that slug identity is **not** guaranteed stable across
  this boundary (10 `canonical_ocn1` renamed). Aligns with the
  decision-record's "minor bump" note.
- `ocn-1.0.4` (patch) — only if treating the migration as a routine
  fix; weaker signal, not preferred for an identity change.

Whichever is chosen, the release notes must carry an explicit
**"slug-migration"** label so consumers pinning `E.QID.Mil.MLn*`
slugs know to update.

## Risk controls

- **Exact `old_slug → new_slug` map** lives in
  [`qid-miles-petrosian-migration-preflight.md`](qid-miles-petrosian-migration-preflight.md)
  (10 renames + 1 delete) — apply from there, do not improvise.
- **No schema change** — 14 columns, same downstream contract.
- **No `moves_uci`/FEN change** — every migrated row keeps its line;
  positions identical (only the duplicate node is deleted).
- **`canonical_ocn1` changes for 10 rows** — the one downstream-
  visible effect; covered by the regen (step 5) + smoke test (6) +
  changelog (7) + minor version signal (8).
- **No consumer should assume slug stability across release tags** —
  state this explicitly in the release notes; it is the precedent
  this migration sets.
- Each mutating step (2, 5) and the tag/upload (8, 9) is its own
  explicit GO.

## Gating

No catalogue apply, artefact regen, tag, or upload happens without
an explicit GO for that step. This checklist commit changes nothing
in `catalog/ocn-1.csv`.
