# QID release-cycle — pre-apply safety snapshot (step 1)

**Step 1 of [`qid-release-cycle-checklist.md`](qid-release-cycle-checklist.md).**
This is the clean baseline recorded **before** any catalogue
mutation. **Step 2 (the apply) is NOT executed** — no catalogue
change accompanies this snapshot.

## Snapshot

- **Date**: 2026-05-26
- **Base**: `origin/main` = `a60b7ae` (local synced, `0 0`)
- **Worktree**: clean, on `main`

## Validations (all green)

| check | result |
|---|---|
| `git status -sb` | `## main...origin/main` (synced) |
| `git rev-list --left-right --count origin/main...HEAD` | `0 0` |
| `validate.py --strict-chess` | **OK: 5900 entries, 0 warnings** |
| `audit_chess.py` | **rows=5900 illegal=0 san_mismatch=0** |
| `unittest discover tools/tests` | **60/60 OK** |
| `lichess_parent_map.py --check` | **A:721 B:972 C:1026 D:461 E:510** (3690 matched) |
| `audit_transpositions.py --summary` | `duplicate_groups=125 resolved_groups=124 unresolved_groups=1 multiple_canonical_groups=17` |
| `export_positions.py --include-roots --stats` | `rows=5900 concrete=5895 unique_fen=5765 duplicate_groups=125 duplicate_rows=255` |
| `git diff --check` | clean |

## Baseline metrics (pre-apply)

| metric | value |
|---|---|
| catalogue rows | 5,900 |
| duplicate_groups | 125 |
| resolved_groups | 124 |
| unresolved_groups | **1** (QID only) |
| multiple_canonical_groups | 17 |

## QID preconditions (verified — safe to migrate at step 2)

| precondition | result |
|---|---|
| `E.QID.Mil.MLn` exists (row to delete) | ✅ YES |
| migrating slugs = `Mil.MLn` + 10 descendants | ✅ **11** (exact list below) |
| `E.QID.Pet.KPe` exists (target anchor) | ✅ YES — **empty leaf** (0 children) |
| inbound `transposes_to`/`same_as` to any migrating slug | ✅ **NONE** (self-contained) |
| `E.QID.Mil` (stays as real 4.Bf4) current child | `E.QID.Mil.MLn` (migrates away → Mil becomes childless leaf) |

The 11 migrating slugs (re-slug `E.QID.Mil.MLn.* → E.QID.Pet.KPe.*`,
delete `E.QID.Mil.MLn`):

```
E.QID.Mil.MLn                       (DELETE — merges into E.QID.Pet.KPe)
E.QID.Mil.MLn.Be7
E.QID.Mil.MLn.d5
E.QID.Mil.MLn.d5.cxd5
E.QID.Mil.MLn.d5.cxd5.Bd2
E.QID.Mil.MLn.d5.cxd5.Nxd5
E.QID.Mil.MLn.d5.cxd5.Qa4
E.QID.Mil.MLn.d5.cxd5.Qc2
E.QID.Mil.MLn.d5.cxd5.e3
E.QID.Mil.MLn.d5.cxd5.e4
E.QID.Mil.MLn.d5.cxd5.exd5
```

(Exact old→new map + new `canonical_name`s in
[`qid-miles-petrosian-migration-preflight.md`](qid-miles-petrosian-migration-preflight.md).)

## **PAS 1 COMPLETE**

Baseline is clean and the QID preconditions hold. **Step 2 (apply
the migration) is GO-gated and NOT executed here.** When step 2 is
GO'd, the expected post-apply state is: rows 5,899,
duplicate_groups 124, resolved_groups 124, **unresolved_groups 0**,
multiple_canonical_groups 17.
