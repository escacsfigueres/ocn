# Lot A player-eponym attribution — dry-run record (2026-06-08)

**Status: DRY-RUN ONLY. No catalogue change, no apply.** First real exercise
of the [Attribution Batch Engine](attribution-batch-engine.md)
(`tools/apply_attribution_manifest.py`) against `catalog/ocn-1.csv`.

## Manifest

- Path: [`manifests/lot-a-player-eponyms.manifest.json`](manifests/lot-a-player-eponyms.manifest.json)
- `kind`: `ocn.attribution_manifest.v1`
- `mode`: `attribution_fields_only` (only `attributed_to` / `attribution_source` / `historical_notes` may change)
- `expected_catalog_rows`: 5899
- `expected_changed_rows`: `D.Tar`, `D.Chi`

## Included rows (2)

| slug | name | grade | attributed_to | source (first-hand) |
|---|---|---|---|---|
| `D.Tar` | Tarrasch Defence | CLEAR | Siegbert Tarrasch (advocate) | Avrukh, *GM Repertoire – 1.d4 Vol.1* + *The Power of Pawns* (NotebookLM Q25, orchestrator-reverified) |
| `D.Chi` | Chigorin Defence | CLEAR | Mikhail Chigorin (leading practitioner) | Avrukh, *GM Repertoire – 1.d4* / *The Queen's Gambit* (NotebookLM Q25, orchestrator-reverified) |

Both are **QGD head rows only**. The surnames each span ~150 unrelated rows
(French Tarrasch `B.Fre.Tar`, Semi-Tarrasch `D.STa`, Ruy López Chigorin
`C.RyL.Cha`, Queen's Pawn Chigorin `D.QPG.Chi`, …) — none of which are touched.

## Excluded rows and why

- **`B.Fre.Win` (Winawer) — HELD, not in this manifest.** The naming passage
  is grounded (*The Center Game*: "(3.Nc3 Bb4) named after him"), but the
  exact **author/year of the book was never surfaced** (do not conflate with
  Mario Ziegler, cited for a *different* book in the same paragraph). Per the
  source log's own caveat ("pin exact author/year before applying") and the
  preference for a strict, CLEAR-only manifest, Winawer stays parked until the
  citation is pinned. Including it would have written an incomplete citation.
- **`D.QGD.Exc.Car` (Carlsbad) — separate Lot B.** Non-person place name
  (`attributed_to` stays empty; `historical_notes` only) — a different mode of
  edit, kept out of the person-eponym batch by design.

## Dry-run result

Command:

```bash
python3 tools/apply_attribution_manifest.py \
  --catalog catalog/ocn-1.csv \
  --manifest docs/manifests/lot-a-player-eponyms.manifest.json \
  --dry-run --strict --report markdown
```

- Exit code **0** — accepted under `--strict` (both rows `CLEAR` with sourced `source_refs`).
- Rows changed: **2** (`D.Tar`, `D.Chi`); row count 5899 → 5899.
- `--validate` (runs `validate.py --strict-chess` on the would-be result):
  **PASS** — `OK: 5899 entries validated, 0 warning(s)`.
- SHA-256 **before**: `39df01fdf286c06dd1782bc3803c4ac2eef219e3043b760ad979dcb619959e08`
- SHA-256 **after** (would-be): `014e3fdc5f5340651c4de3e395e8b4865d0a6a45e481d8a4719bba7f6705f5e4`

## Row-level diff summary

Applying to a throwaway copy produces a **4-line diff = exactly 2 rows**
(zero collateral diff on the other 5,897 rows — raw-line preservation):

- `D.Tar`: `attributed_to` `'' → 'Siegbert Tarrasch (advocate)'`;
  `attribution_source` `'' →` Avrukh + *Power of Pawns* citation;
  `historical_notes` `'' →` 1.d4 d5 2.c4 e6 3.Nc3 c5 note (head-only caveat).
- `D.Chi`: `attributed_to` `'' → 'Mikhail Chigorin (leading practitioner)'`;
  `attribution_source` `'' →` Avrukh citation;
  `historical_notes` `'' →` 1.d4 d5 2.c4 Nc6 note (distinct from `C.RyL.Cha`).

## No catalogue mutation

`catalog/ocn-1.csv` is byte-identical before and after this exercise (SHA-256
`39df01f…`, `git status` clean). The dry-run wrote nothing; the `--apply`
verification above wrote only to a temporary file that was discarded.

## Next step (separate GO)

Under an explicit GO, apply with:

```bash
python3 tools/apply_attribution_manifest.py \
  --catalog catalog/ocn-1.csv \
  --manifest docs/manifests/lot-a-player-eponyms.manifest.json \
  --apply --out catalog/ocn-1.csv --strict --validate
# then: git diff --stat catalog/ocn-1.csv && python3 tools/validate.py --strict-chess catalog/ocn-1.csv
```

## See also

- [`parked-attribution-reference-source-log.md`](parked-attribution-reference-source-log.md) — the verified 4-CLEAR / 2-PARTIAL source grades this draws on.
- [`attribution-batch-engine.md`](attribution-batch-engine.md) — the engine and its guardrails.
