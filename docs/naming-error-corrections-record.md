# Naming-error corrections — applied record (2026-06-11)

**Status: APPLIED** via the batch engine (`naming_strings_only`, 16 rows),
under the 360-audit P0 GO. Manifest:
[`manifests/naming-error-corrections.manifest.json`](manifests/naming-error-corrections.manifest.json).

## What was wrong and what the evidence said

- **"Meadow Hay Trap" was on the wrong row.** Lichess (CC0 corpus,
  `external/lichess-openings`): the trap is `1.a4 e5 2.Ra3` — our
  `A.War.e5.Ra3`, which already carried the name. `A.War.Mad`
  (`1.a4 e5 2.a5 d5`, the Ware Gambit precursor) and its `MLn` child were
  renamed to descriptive `a5 d5` names; the gambit names deeper in the
  subtree (`A.War.Mad.MLn.f5.a6` = "Ware Opening, Ware Gambit") match
  Lichess and were untouched.
- **"Greco Variation" was duplicated across two different positions** —
  and the audit agent's first reading ("Greco is the Qf6 line") was
  **backwards**: Lichess puts *Greco Variation* on `3.Nxe5 Qe7`
  (`C.LtO.Nxe5.Qe7`, kept), and Wikipedia confirms `3...Qf6` is simply
  *the main line* ("Greco Countergambit" is the historical name of the
  whole opening, not of either queen move). The Qf6 subtree
  (`C.LtO.Gre` + 11 descendants, whose sub-lines mirror Lichess's
  *Latvian Gambit Accepted* names) was renamed to a "Latvian Main Line"
  stem — which also killed the second duplicate ("Latvian Greco Nc4,
  fxe4" appeared on both Nc4 paths).
- **`B.Sic.OKe.c4`** spelled "Maroczy" against its own
  `attributed_to` ("Géza Maróczy") — diacritic fixed.
- **`A.Ret`** had an empty aliases field; "Zukertort Opening" (the
  standard name for bare 1.Nf3, referenced by Lot 3's own notes) added.

## Result (verified post-apply)

- Exactly **16 rows changed** (32-line diff), fields = `canonical_name` /
  `aliases` only; rows 5,899 → 5,899; slugs frozen (`Mad`, `Gre` tokens
  diverge from their names by design — slug renames are release-boundary
  migrations).
- SHA-256: `3e62cb06…` → `c90f5fed…` (identical to the dry-run prediction).
- Global duplicate canonical_names: **6 → 3**. The remaining three
  ("English Reversed Sicilian g3, d5", "King's Indian Attack", "King's
  Pawn Game") are possible legitimate move-order twins — per-case review
  belongs to the P1 naming wave, not this lot.
- `validate.py --strict-chess` OK 5899/0; `unresolved_groups=0`.

## Notable

The two flagged-as-stale name/slug pairs (`A.War.Mad` "Mad" ← Meadow,
`C.LtO.Gre` "Gre" ← Greco) keep their slugs: OCN slugs are frozen
identifiers, and the spec's recovery mechanism for *wrong slugs* is
`deprecated` + new entry, which these do not warrant (the positions are
right; only the display names were wrong).
