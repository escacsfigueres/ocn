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

## Resolved

### Kangaroo ↔ Nimzo (partial, by FEN)

OCN classifies by **position**, not by intended move order. A.Kan
slugs whose FEN coincides with an E.Nim slug are recorded as
move-order transpositions; the E.Nim slug owns the position.

A.Kan slugs whose FEN does **not** coincide with any E.Nim slug
(notably the root `A.Kan = 1.d4 e6 2.c4 Bb4+` before ...Nf6 and the
intermediate `A.Kan.MLn`) remain canonical Kangaroo entries.

**Pairings recorded** (E.Nim canonical, A.Kan move-order):

| FEN pattern                              | Canonical          | Transposition           |
|------------------------------------------|--------------------|-------------------------|
| Nimzo, 4.Nf3                             | `E.Nim.Kas`        | `A.Kan.Nf3`             |
| Nimzo, 4.e3 (Rubinstein)                 | `E.Nim.Rub`        | `A.Kan.MLn.e3`          |
| Rubinstein with ...O-O                   | `E.Nim.Rub.O-O`    | `A.Kan.MLn.e3.O-O`      |
| Rubinstein ...O-O Nf3                    | `E.Nim.Rub.O-O.Nf3`| `A.Kan.MLn.e3.O-O.Nf3`  |
| Rubinstein with ...c5                    | `E.Nim.Rub.c5`     | `A.Kan.MLn.e3.c5`       |

**Changes applied to the catalogue:**

- Each E.Nim row above gains pipe-separated aliases pointing at the
  Kangaroo move-order label.
- Each A.Kan row above gets a `notes` field of the form
  `Move-order transposition to E.Nim.*: same FEN ...`.
- Two redundant E.Nim siblings deleted (no children, identical FEN to
  their parent): `E.Nim.Kas.TKn`, `E.Nim.Rub.Sys`.

**Still open in this family:** none of the 5 transposition pairs above
are physically merged. Their FEN duplicates remain visible in
`audit_transpositions.py --summary` because OCN keeps both slugs alive
for navigation from the Kangaroo subtree. The pairs are now
**catalogued**, not removed. Physical merge of A.Kan.* into E.Nim.* is
out of scope for this sprint; it requires either a `transposes_to`
column or careful reassignment of A.Kan children.

### Modern Averbakh / Old Indian ↔ KID (partial, by FEN)

Same principle as Kangaroo ↔ Nimzo: classify by FEN, not by intent.
A.Mod / A.OID slugs that have reached a Classical KID FEN (i.e. after
...Nf6 and the d4/c4/e4 + Bg7/d6 KID tabiya is on the board) are
recorded as move-order transpositions; the matching E.KID slug owns
the position. A.Mod and A.OID slugs that have **not** yet transposed
to a KID FEN (no ...Nf6) remain canonical Modern / Old Indian
entries.

**Pairings recorded** (E side canonical, A side move-order):

| FEN pattern                              | Canonical                  | Transposition                       |
|------------------------------------------|----------------------------|-------------------------------------|
| 1.d4 Nf6 2.c4 d6 (Old Indian)            | `E.OldI`                   | `A.OID.Nf6`                         |
| Classical KID Normal                     | `E.KID.Cls.Nrm`            | `A.OID.Mod.MLn.Nf6`                 |
| Normal, 5.Be2                            | `E.KID.Cls.Nrm.Be2`        | `A.OID.Mod.MLn.Nf6.Be2`             |
| Normal, 5.Bg5 (Accelerated Averbakh)     | `E.KID.Cls.Nrm.Bg5`        | `A.OID.Mod.MLn.Nf6.Bg5`             |
| Normal, 5.Nge2 (Kramer)                  | `E.KID.Cls.Nrm.Nge2`       | `A.OID.Mod.MLn.Nf6.Nge2`            |
| Normal, 5.g3 (Deferred Fianchetto)       | `E.KID.Cls.Nrm.g3`         | `A.OID.Mod.MLn.Nf6.g3`              |
| Orthodox Classical (5.Nf3 O-O 6.Be2)     | `E.KID.Cls.Oth`            | `A.Mod.Avk.MLn.Be2`                 |
| Orthodox + ...Na6 (Kazakh)               | `E.KID.Cls.Oth.Na6`        | `A.Mod.Avk.MLn.Be2.Na6`             |
| Classical Mar del Plata prefix (...e5)   | `E.KID.Cls.e5`             | `A.Mod.Avk.MLn.Be2.e5`              |
| Classical Mar del Plata + ...O-O         | `E.KID.Cls.e5.O-O`         | `A.Mod.Avk.MLn.Be2.e5.O-O`          |

**Changes applied to the catalogue:**

- Each E.KID row above gains an alias of the form
  `Old Indian Modern ... move-order` or `Modern Averbakh ... move-order`.
- Each A-side row above gets a `notes` field of the form
  `Move-order transposition to E.KID.*: same FEN ...`.
- No rows deleted. No intra-E redundants in this family.

**Preserved as canonical** (no FEN coincidence with E.KID):

- `A.Mod` root and its non-...Nf6 children (Robatsch / Modern Defence
  against 1.d4, e.g. `A.Mod.e4`, `A.Mod.Avk` itself).
- `A.OID` root and its non-...Nf6 children (e.g. `A.OID.Mod`,
  `A.OID.Mod.MLn` before the Nf6 move).
- `A.Mod.Avk.MLn` (after castling but on a unique FEN, no E.KID
  equivalent).

**Deferred to OCN 0.2 (requires `transposes_to`):** five intra-Modern
groups where the A-side and B-side reach the same pre-KID Averbakh /
extended-centre Modern FEN through 1.d4 vs 1.e4 move orders:

- `A.Mod.Avk` ⇄ `B.Mod.Avk` ⇄ `A.OID.Mod.MLn`
- `A.Mod.Avk.Nc6` ⇄ `B.Mod.Avk.MLn`
- `A.Mod.e4` ⇄ `B.Mod.Std.Ctr`
- `A.Mod.e4.c5` ⇄ `B.Mod.Std.Ctr.PtC`
- `A.Mod.e4.e5` ⇄ `B.Mod.Std.Ctr.e5`

These are pre-KID Modern Defence positions (no ...Nf6). OCN has no
rule that selects a canonical between the 1.d4 (A) and 1.e4 (B)
move-order trees for the same Modern FEN — both are literature-valid
labels (B06 is the ECO-canonical Modern Defence; A40-A42 are the
Modern against 1.d4). Resolving them by mutual cross-reference would
require either a tie-breaker rule (which OCN has not adopted) or the
`transposes_to` column proposed for 0.2.

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
