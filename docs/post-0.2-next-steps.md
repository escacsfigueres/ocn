# Post-0.2 next steps

**Last updated**: against commit `b582e6f`.
**Companion**: builds on
[`roadmap-0.2.md`](roadmap-0.2.md) (the four-phase plan) and
[`release-0.2-checklist.md`](release-0.2-checklist.md) (the
release decision record). This document narrows the focus to the
operational next steps now that Phase 1's `unresolved_groups < 50`
target has already been crossed.

## Current state — main vs tag

| ref | hash | role |
|---|---|---|
| tag `ocn-1.0.2` | `415f1df` | **release baseline**. Frozen, pinnable by downstream consumers that want exactly what the 0.2 release shipped. |
| `origin/main` HEAD | `b582e6f` | **post-tag Phase 1 cleanup**. Two doc-and-data commits beyond the tag that remove descriptor duplicates and add 18 `transposes_to` arrows. Schema and contract unchanged. |

### Metric delta tag → main

|                            | tag (`415f1df`) | main (`b582e6f`) | Δ |
|----------------------------|---|---|---|
| rows                       | 5,966 | 5,905 | −61 (clean-up deletes) |
| duplicate_groups           | 191 | 130 | −61 |
| resolved_groups            | 75 | 93 | +18 |
| unresolved_groups          | 116 | **37** | **−79** |
| multiple_canonical_groups  | 6 | 6 | — |
| rows_in_unresolved_groups  | 233 | 75 | −158 |
| schema                     | 14 columns | 14 columns | unchanged |

**Phase 1 roadmap target was `unresolved_groups < 50`.** Result is
**37**, which puts the catalogue past Phase 1's exit criterion
without any further intra-family cleanup required.

## Recommendation for consumers

Downstream consumers fall into two camps:

- **Stability-oriented** (citation, reproducibility, locked
  release): pin tag `ocn-1.0.2` (commit `415f1df`). Everything
  documented in `docs/release-0.2-checklist.md` describes this
  state exactly. New cleanup commits do not affect them.
- **Currency-oriented** (cleaner audit, fewer Lichess-imported
  descriptor leaves, additional `transposes_to` declarations):
  pin `origin/main` HEAD (commit `b582e6f` at the time of this
  document). Schema is identical to the tag; the 14-column
  contract holds; only the row set is reduced and some
  `transposes_to` cells are populated.

Both pins are valid OCN 0.2 catalogues. The schema, validator,
audit and downstream `chess-parquet` producer behave identically
against both.

## Artefacts to generate

Now that main is stable and Phase 1 cleanup has landed, the
release artefact bundle becomes worth producing.

### Required

| artefact | source | purpose |
|---|---|---|
| `ocn-1.positions.tsv` | `tools/export_positions.py --include-roots --out ocn-1.positions.tsv` against `main` | derived position index with `fen_key`, normalised `fen`, `transposition_group_size`, `transposes_to`, `same_as` |
| `openings.parquet` | `chess-parquet`'s `efcdb-openings` producer against `main` | columnar artefact with Polyglot zobrist, both identity columns |

### Optional

| artefact | source | purpose |
|---|---|---|
| `ocn-1.transpositions.tsv` | `tools/audit_transpositions.py --ranked --include-resolved --json` piped to TSV via small helper, or a new `--export-resolution` flag added to the audit tool | exported audit state per group, useful for consumers wanting `resolution_kind` and `canonical_count` per slug without re-running the audit themselves |

The `transpositions.tsv` artefact is nice-to-have for OCN 0.2; not
required. Consumers can run `audit_transpositions.py` against the
catalogue themselves.

## Pending decisions — 37 unresolved groups

The 37 remaining unresolved groups split into two kinds:

### Top deferred conceptuals (require proposal before any change)

These are the "two real names, no descriptor side" cases. Each
needs a per-family arbitration decision (multiple_canonical via
`same_as`, single_canonical, or genuine defer). All have working
documentation in [`docs/transpositions.md`](transpositions.md)
under "Deferred conceptual families".

| group | classes | character |
|---|---|---|
| `A.Van.ReN.e3.d5 ⇄ A.Van.d5.e3.e5 ⇄ A.VtK.e5.Nc3.d5` | A | three-way Van Geet / Van't Kruijs |
| `B.Mod.Std.Nf3.C5S ⇄ B.Sic.HAc.d4.Bg7` | A,B | cross-family Modern / Sicilian Hyperaccelerated |
| `E.Nim.Sml.Bot ⇄ E.Nim.Sml.Kmo` | E | Botvinnik vs Kmoch — `same_as` candidate |
| `A.Lar.Cls.MLn ⇄ A.Ret.Nim.MLn` | A | Larsen vs Reti Nimzowitsch-Larsen — `same_as` candidate |
| `A.QPO.Nf6.Nf3.c6 ⇄ A.QPO.c6.Nf3.Nf6` | A | Czech-Indian move-order mirror |
| `A.Eng.Sym.Nc3.Nf6.Nf3 ⇄ A.Eng.Sym.Nf3.Nf6.Nc3` | A | English Symmetrical Three Knights, both real |
| `D.QGA.Flo.MLn ⇄ D.QGA.Jan.e3.b5` | D | Flohr vs Haberditz — `same_as` candidate |
| `A.Lon.Cls.MLn (+.c4) ⇄ A.Lon.Msn.MLn.Nbd2 (+.c4)` | A | Classical vs Mason London — 2 paired groups, `same_as` candidate |
| `A.PQI.e3 ⇄ A.PQI.e3.Bb7` | A | parent-child same-FEN, structural review |

### Long-tail structural residuals (mechanical, low priority)

The remaining ~27 groups are deeper intra-family duplicates with
score=4 or lower. Same pattern as the previous cleanup batches
but progressively diminishing returns (each removal touches a
single row that few consumers will ever query). Cleanup is
optional; the catalogue functions correctly with them in place.

## Proposed Phase 2

A small operational plan, ordered by leverage:

1. **Generate `ocn-1.positions.tsv` from `main` and ship it as a
   release asset.** Tiny script run; reproducible from any
   commit; gives stability-oriented consumers a derived
   position-indexed artefact alongside the tag.
2. **Run `chess-parquet`'s `efcdb-openings` producer against
   `main`, validate the resulting `openings.parquet` against the
   downstream contract (helpers `canonical_ocn1`,
   `co_canonical_ocn1s`), and pin it.** Smoke test that
   multi-canonical FENs return multiple rows on zobrist join.
3. **Decide one deferred conceptual case for the next proposal
   sprint.** Recommended starting point: `D.QGA.Flo.MLn ⇄
   D.QGA.Jan.e3.b5` — clean `same_as` candidate, mechanical
   resolution, no schema work, low risk. Or `A.Lon.Cls vs Msn`
   pair (two real London System families, sets a precedent for
   "intra-A two-family `same_as`").
4. **Long-tail mechanical residuals** stay deferred unless a
   consumer specifically requests further cleanup. Diminishing
   returns make them low priority.

After step 2 the OCN 0.2 release bundle is complete:
`catalog/ocn-1.csv` (in repo and at tag), `ocn-1.positions.tsv`
(generated from main), `openings.parquet` (generated from
`chess-parquet` against main). Step 3 is the first proposal
sprint of the post-Phase-1 era.

## Recommended next operational action

**Generate `ocn-1.positions.tsv` from `main` and attach it as a
GitHub release asset on the `ocn-1.0.2` tag** (or on a separate
`ocn-1.0.2-cleanup` tag if you prefer to keep the release
artefacts pinned to the same baseline as `b582e6f`).

This is a single command (`python3 tools/export_positions.py
--include-roots --out /tmp/ocn-1.positions.tsv`) plus an upload
step. No catalogue change, no schema change, no proposal needed.
Closes the artefact gap in the release bundle.

Step 2 (run `chess-parquet` against `main`) is the natural
follow-up but lives in the other repo.
