**Status: APPLIED 2026-06-11** under the approved decision record.

# Attribution manifest — Duplicate-name renames: four pairs made unique

- kind: `ocn.attribution_manifest.v1`
- mode: `naming_strings_only`
- catalogue: `/Users/albertpi/Code/ocn/catalog/ocn-1.csv`
- rows: 5899 -> 5899
- sha256 before: `26d506cd77afc4f2438d8cf69523c853907efe18a57f1d96f91605ed4b956ffd`
- sha256 after:  `f201a39a8faa5dc01bf53368bf65183f23f600fe97bf3e2bd7efae16f76596c9`
- rows changed: 5

## Changes

### `A.Eng.Rev.Nc3.Nf6.g3.d5` (evidence: CLEAR)
- sources: docs/phantom-and-duplicate-name-decision.md (GO 2026-06-11): different position (A22, via Nc3) than its A29 namesake; path-compositional rename.
- `canonical_name`: 'English Reversed Sicilian g3, d5' -> 'English Reversed Sicilian Nc3 g3, d5'

### `A.Ret.d5.g3` (evidence: CLEAR)
- sources: docs/phantom-and-duplicate-name-decision.md (GO 2026-06-11): the family head A.KIA keeps the plain name; this is the 1.Nf3 d5 2.g3 path.
- `canonical_name`: "King's Indian Attack" -> "Réti, King's Indian Attack Setup"

### `B.KPG` (evidence: CLEAR)
- sources: docs/phantom-and-duplicate-name-decision.md (GO 2026-06-11): bare 1.e4 takes its own existing alias as canonical; identity alias drops.
- `canonical_name`: "King's Pawn Game" -> "King's Pawn Opening"
- `aliases`: "King's Pawn Opening" -> ''

### `C.KPO` (evidence: CLEAR)
- sources: docs/phantom-and-duplicate-name-decision.md (GO 2026-06-11): drops the alias that is now B.KPG's canonical, removing search ambiguity.
- `aliases`: "King's Pawn Opening" -> ''

### `A.Ret.d5.c4` (evidence: CLEAR)
- sources: docs/phantom-and-duplicate-name-decision.md (GO 2026-06-11): the Réti proper (A09); the family head A.Ret keeps the plain name.
- `canonical_name`: 'Réti Opening' -> 'Réti Opening, 2.c4'

## Validation: PASS

```
OK: 5899 entries validated, 0 warning(s)
```
