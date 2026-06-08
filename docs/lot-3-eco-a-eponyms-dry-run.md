# Lot 3 ECO-A eponym attribution — evidence + dry-run record (2026-06-08)

**Status: DRY-RUN ONLY. No catalogue change, no apply.** Produced via the factory
tooling: `candidate_slice_export` → evidence sprint (4 read-only agents, one per
head) → orchestrator re-verification → `scaffold_attribution_manifest` → human
fill → engine `--dry-run --strict --validate`.

## Manifest

- Path: [`manifests/lot-3-eco-a-eponyms.manifest.json`](manifests/lot-3-eco-a-eponyms.manifest.json)
- `mode`: `attribution_fields_only`, `expected_catalog_rows`: 5899
- `expected_changed_rows`: `A.Bir`, `A.Lar`, `A.Ret`, `A.Gro` (catalogue order)

## Included rows — all 4 CLEAR, head-only

| slug | opening | attributed_to | role | source (re-verified) |
|---|---|---|---|---|
| `A.Bir` | Bird's Opening (1.f4) | Henry Edward Bird | popularizer | Wikipedia 'Bird's Opening' / 'Henry Bird' |
| `A.Lar` | Larsen Attack (1.b3) | Bent Larsen | popularizer | Wikipedia 'Nimzowitsch–Larsen Attack'; ChessBase |
| `A.Ret` | Réti Opening (1.Nf3) | Richard Réti | popularizer | Wikipedia 'Réti Opening' |
| `A.Gro` | Grob Opening (1.g4) | Henri Grob | analyst and popularizer | Wikipedia 'Grob's Attack' / 'Henri Grob' |

**Evidence discipline.** Each head was researched by a dedicated agent, then the
orchestrator **independently re-fetched the cited Wikipedia article** to confirm
the agent quoted it faithfully (the re-verify-before-trusting rule that caught
the earlier "Paris 1878" fabrication). All four claims checked out. Every eponym
is recorded as a **champion / popularizer (or analyst), not an inventor** — each
first move predates its namesake (Bird: Lucena c. 1497; Réti: 1.Nf3 ancient,
catalogued separately as Zukertort; Larsen: John Owen 1870s + Nimzowitsch;
Grob: Carl Ahlhausen) — stated conservatively in `historical_notes`. No
"first played by / invented by" claim is made.

**Sourcing note.** Citations are Wikipedia (re-verified first-hand by the
orchestrator), corroborated by ChessBase for Larsen. These are bedrock,
uncontested eponyms (single unambiguous person per opening, no multi-head
surname risk in ECO A), so secondary-but-verified sourcing meets the CLEAR bar
here — consistent with the prior `B.Ale` (Alekhine) attribution precedent.

## Held / excluded

None — all four cleared. (Lot 3 was scoped as exactly these four ECO-A heads.)

## Dry-run result

```bash
python3 tools/apply_attribution_manifest.py \
  --catalog catalog/ocn-1.csv \
  --manifest docs/manifests/lot-3-eco-a-eponyms.manifest.json \
  --dry-run --strict --validate --report markdown
```

- Exit **0** — accepted under `--strict` (all `CLEAR`, all with `source_refs`).
- Rows changed: **4** (`A.Bir`, `A.Lar`, `A.Ret`, `A.Gro`); row count 5899 → 5899.
- `--validate` (`validate.py --strict-chess` on the would-be result): **PASS** —
  `OK: 5899 entries validated, 0 warning(s)`.
- SHA-256 **before**: `014e3fdc5f5340651c4de3e395e8b4865d0a6a45e481d8a4719bba7f6705f5e4`
- SHA-256 **after** (would-be): `3e62cb065068728ebcebdfd91a567e49169995afbc2fff2f5a3e3d654f99ef42`
- Applying to a throwaway copy gives an **8-line diff = exactly 4 rows** (zero
  collateral diff on the other 5,895 rows); only `attributed_to` /
  `attribution_source` / `historical_notes` change.

## No catalogue mutation

`catalog/ocn-1.csv` is byte-identical before and after this exercise (SHA-256
`014e3fd…`, `git status` clean). The dry-run wrote nothing.

## Next step (separate GO)

```bash
python3 tools/apply_attribution_manifest.py \
  --catalog catalog/ocn-1.csv \
  --manifest docs/manifests/lot-3-eco-a-eponyms.manifest.json \
  --apply --out catalog/ocn-1.csv --strict --validate
# then: git diff --stat catalog/ocn-1.csv && python3 tools/validate.py --strict-chess catalog/ocn-1.csv
```

## See also

- [`attribution-factory-tooling.md`](attribution-factory-tooling.md) — the slice → scaffold → dry-run pipeline used here.
- [`whole-catalogue-attribution-factory-map.md`](whole-catalogue-attribution-factory-map.md) — Lot 3 is the factory map's recommended first batch.
- [`lot-a-player-eponyms-dry-run.md`](lot-a-player-eponyms-dry-run.md) — the prior applied batch (Tarrasch, Chigorin).
