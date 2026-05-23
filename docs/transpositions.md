# Transpositions in OCN-1

## Current state

- Catalogue size: **6,099** rows.
- Duplicate FEN groups: **316**.
- Rows participating in duplicate groups: **645**.
- Top group size observed: **3**.

Numbers are produced by:

```
python3 tools/audit_transpositions.py --summary
python3 tools/audit_transpositions.py --ranked --limit 20
```

`audit_transpositions.py` groups concrete rows by FEN position key
(board + side to move + castling + en-passant, ignoring move counters).

## Principle

One FEN can be reached by multiple move orders. OCN-1 still needs a
single canonical slug per opening. Duplicates in the catalogue are
**expected**: they record real chess move orders. They are not bugs by
themselves. They become a problem only when the catalogue fails to mark
which slug is canonical and which slugs are aliases or named children.

The audit surfaces every duplicate. Resolution is a manual, per-family
decision made on the catalogue itself.

## Categories of relationship

When two or more rows share a FEN, exactly one of these labels applies:

| Label                          | Meaning                                                                                            | Catalogue treatment                                                                |
|--------------------------------|----------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------|
| **canonical slug**             | The slug that owns the position in OCN-1.                                                          | One per FEN. Carries `canonical_name`, `eco_legacy`, and the preferred move order. |
| **move-order alias**           | Same opening, alternate move order. No independent literature identity.                            | Folded into the canonical row's `aliases` (no separate slug).                      |
| **legitimate named transposition** | Two distinct named openings that converge on this FEN through different conceptual paths.       | Two slugs kept. Cross-reference recorded; consumers may see either.                |
| **redundant duplicate**        | Two rows refer to the same opening at the same depth and are bookkeeping mistakes.                 | One row removed.                                                                   |

The default outcome should be **move-order alias** unless there is a
clear literature reason for two slugs.

## Top families to decide

Detected by `audit_transpositions.py --ranked` over the current
catalogue. Each family covers multiple groups and should be resolved
with a single family-level decision rather than group by group.

| Family                                      | Pattern                                                                                  | Suggested canonical                                       |
|---------------------------------------------|------------------------------------------------------------------------------------------|-----------------------------------------------------------|
| **A.Kan ↔ E.Nim**                           | `1.d4 e6 2.c4 Bb4+` (Kangaroo) transposes into `1.d4 Nf6 2.c4 e6 3.Nc3 Bb4` (Nimzo).     | `E.Nim.*` canonical; `A.Kan.*` becomes move-order alias.  |
| **A.Ver ↔ D.QPG.Ver ↔ B.Fre**               | Richter-Veresov reached via `1.d4 Nf6 2.Nc3 d5 3.Bg5` (A) or `1.d4 d5 2.Nc3` (D); when …e6 follows, the French Classical lines (B.Fre) also converge. | `A.Ver.*` canonical; `D.QPG.Ver.*` alias; `B.Fre.Cls.MLn` kept as named transposition. |
| **A.Mod.Avk / A.OID.Mod ↔ E.KID**           | Modern-Averbakh and Old Indian move orders converge on KID-Classical with …e5.            | `E.KID.*` canonical; flank slugs become aliases.          |
| **D.Cat ↔ E.Ind.Cat**                       | Catalan with …d5 (D) vs Indian Catalan with …d5 inserted later (E).                      | `D.Cat.Cls.Qc2.Clo` canonical once …d5 is on the board.   |
| **A.Lon ↔ D.QPG.Zuk**                       | London System reached from the A-side or the D-side.                                     | `A.Lon` canonical; `D.QPG.Zuk.Nf6.Bf4` alias.             |
| **A.Hor / A.Col ↔ D.QGD / D.QPG**           | Horwitz French and Colle move orders transposing into QGD / Zukertort.                   | D-side canonical; A-side becomes alias.                   |
| **E.Ben.Mod ↔ E.Ind.e6**                    | Intra-E: Modern Benoni and Indian-via-…e6 reaching the same FEN.                         | `E.Ben.Mod.*` canonical; `E.Ind.e6.*` collapsed.          |

## Workflow

1. Generate a ranked report:
   ```
   python3 tools/audit_transpositions.py --ranked --limit 20 > /tmp/ranked.tsv
   ```
2. Pick one family. Decide canonical, aliases, named transpositions, and
   redundant rows. Record the reasoning in this document under a new
   `## Decisions` section as families are resolved.
3. Apply changes to `catalog/ocn-1.csv` in a single dedicated commit per
   family. Do not mix families in one commit.
4. Re-run `audit_transpositions.py --summary` and confirm the affected
   groups drop or shrink as expected.

## Out of scope (for now)

- Changing the CSV schema. Aliases continue to use the existing
  `aliases` column. A separate `transposes_to` column is a candidate for
  OCN-0.2 but is not introduced by this audit.
- Polyglot Zobrist or any other position-indexed artefact. Handled by
  the `chess-parquet` producer downstream.
