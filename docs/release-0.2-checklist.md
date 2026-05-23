# OCN 0.2 — pre-release checklist

**State**: pushed; ready for the internal OCN 0.2 tag at the maintainer's discretion.
**Last updated**: against commit `094c616` (this checklist + post-push re-verification).

## Coordinates

| field | value |
|---|---|
| OCN repo HEAD | `094c616` (Add OCN 0.2 release checklist) |
| OCN branch | `main`, synced with `origin/main` |
| chess-parquet compatible commit | `a56bd569d190734193136f16bf229033cbaa8b80` (`docs(corpus): record Reckless timeout investigation`) |
| chess-parquet key commit (downstream support) | `71c14fc` (producer(openings): support OCN 0.2 identity columns) — unchanged since 0.2 emission landed |
| OCN local commits ahead of `origin/main` | 0 (pushed) |

The two newer chess-parquet commits (`94a43d0` Batch 3 risky weapon
depth jobs, `a56bd56` Reckless timeout investigation doc) do **not**
modify the downstream openings producer or the 14-column contract;
they consume the catalogue and the runner. The 0.2 schema is stable
for both.

## Catalogue snapshot

| metric | value |
|---|---|
| schema columns | **14** (fixed order, regression test guards drift) |
| rows | **5,966** |
| unique FENs (concrete entries) | 5,765 |
| rows with `transposes_to` set | **73** |
| rows with `same_as` set | **12** |
| duplicate FEN groups | **191** |
| — resolved | **75** (69 single_canonical + 6 multiple_canonical) |
| — unresolved | **116** |
| rows in unresolved groups | 233 |
| FENs with ≥2 canonical OCNs (downstream join arity) | **122** |
| classes_mixed_groups | 0 |

### Schema (in CSV column order)

```
ocn1, canonical_name, eco_legacy, parent_ocn1, moves_uci, depth,
aliases, flags, notes, attributed_to, attribution_source,
historical_notes, transposes_to, same_as
```

This order is the **downstream contract** with
`chess-parquet`'s `efcdb-openings`. Reordering or adding a 15th
column without a coordinated chess-parquet release is a
breaking change. A regression test
(`test_canonical_catalogue_header_matches_downstream_contract`)
guards the order.

## Tests and validators executed

All run against commit `094c616` (re-verified post-push; identical
metrics to the original `ecf7193` run — no catalogue drift):

| command | result |
|---|---|
| `python3 tools/validate.py --strict-chess catalog/ocn-1.csv` | `OK: 5966 entries validated, 0 warning(s)` |
| `python3 tools/audit_chess.py catalog/ocn-1.csv` | `rows=5966 illegal=0 san_mismatch=0` |
| `python3 -m unittest discover tools/tests` | **60 / 60 OK** |
| `python3 tools/lichess_parent_map.py --check external/lichess-openings` | `rows=3690 matched=3690 unmatched=0 parse_errors=0` |
| `python3 tools/audit_transpositions.py --summary` | `duplicate_groups=191 resolved=75 unresolved=116 multiple_canonical=6` |
| `python3 tools/export_positions.py --include-roots --stats --out /tmp/ocn-1.positions.tsv` | `rows=5966 concrete=5961 unique_fen=5765 duplicate_groups=191 duplicate_rows=387` |
| `git diff --check` | clean |
| ad-hoc contract verification (header, mutex, FEN match) | 0 errors |

## Release artefacts

To be produced once the tag lands:

| artefact | source | size approx | purpose |
|---|---|---|---|
| `catalog/ocn-1.csv` | this repo | ~700 KB | primary text catalogue, 14 columns |
| `ocn-1.positions.tsv` | `tools/export_positions.py --include-roots` | ~1 MB | derived position index with `fen_key`, `fen`, `transposition_group_size`, `transposes_to`, `same_as` |
| `openings.parquet` | `chess-parquet`'s `efcdb-openings` | TBD | columnar artefact with Polyglot zobrist, both identity columns |
| `ocn-1.transpositions.tsv` (optional) | `tools/audit_transpositions.py --ranked --include-resolved` piped to TSV | ~50 KB | audit state per group, useful for downstream consumers wanting `resolution_kind` per slug |

The first three are required for OCN 0.2. The transpositions audit
TSV is nice-to-have; consumers can run the audit themselves
against the CSV.

## Known limitations

1. **116 unresolved duplicate groups** remain in the catalogue.
   Most are intra-family parent/child or sibling mirrors with both
   sides carrying substantive subtrees. Phase 1 of
   [`docs/roadmap-0.2.md`](roadmap-0.2.md) targets reducing this
   to <50 after a couple more multi-agent cleanup sprints. **Not
   a blocker for the 0.2 tag** — the audit reports them
   transparently and consumers handle multi-row zobrist returns
   regardless of declared resolution status.

2. **122 FENs map to ≥2 canonical OCNs**, but only 6 are
   declared multi_canonical via `same_as`. The remaining 116 are
   pending Phase 1 cleanup. Downstream contract handles both
   cases identically (preserve all rows on zobrist join), so
   this gap is informational, not functional. See
   [`docs/roadmap-0.2.md`](roadmap-0.2.md) §1 for the
   "6-vs-122 gap" note.

3. **No public release tag yet.** Internally ready; pending the
   `git push` + tag decision.

4. **No `same_as` schema change is forward-incompatible.** The
   14-column header is stable for 0.2 — additions (Phase 3
   internationalised aliases) come in 0.3.

5. **Conceptual residue documented**: Van Geet / Van't Kruijs
   3-way (`A.Van.ReN.e3.d5 ⇄ A.Van.d5.e3.e5 ⇄ A.VtK.e5.Nc3.d5`)
   and the Caro/b5 Spanish family remain as documented deferred
   cases in `docs/transpositions.md`. Not blockers.

## Release decision

**Pushed; ready for the internal OCN 0.2 tag at the maintainer's discretion.**

The catalogue, schema, validator, audit, export and downstream
producer are all aligned at commit `094c616`. No outstanding
contract issues. Test suite green. Downstream `chess-parquet`
already consumes the 0.2 schema and has since landed two consumer-side
commits (Batch 3 risky weapon depth jobs, Reckless timeout
investigation doc) that do not change the producer contract.
Phase 1 cleanup work is incremental, not gating.

### Recommended sequence (updated)

1. ~~`git push origin main`~~ — done; HEAD is on `origin/main`.
2. Tag `ocn-1.0.2` (or similar) on `094c616`. Not yet applied.
3. Regenerate `ocn-1.positions.tsv` from the tag and attach to the
   release.
4. Coordinate with `chess-parquet` to pin its `openings.parquet`
   producer to the same tag and publish the Parquet artefact.

### Alternative: one more Phase 1 sprint before tag

If you prefer to enter 0.2 with `unresolved_groups < 100`, run
one more multi-agent intra-family sweep targeting the long-tail
score-≤5 groups. Expected drop: ~20-30 groups. Not technically
required; purely a cosmetic improvement to the audit report at
release time.
