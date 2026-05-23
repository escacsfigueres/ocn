# Transpositions in OCN-1

## Current state

- Catalogue size: **5,972** rows.
- Duplicate FEN groups: **196** total — **62 resolved** by
  `transposes_to`, **134 unresolved**.
- Rows in unresolved groups: **273**.
- Top group size observed: **3**.

Numbers are produced by:

```
python3 tools/audit_transpositions.py --summary
python3 tools/audit_transpositions.py --ranked --limit 20
python3 tools/audit_transpositions.py --ranked --include-resolved --limit 20
```

`audit_transpositions.py` groups concrete rows by FEN position key
(board + side to move + castling + en-passant, ignoring move counters).
By default it hides groups already resolved by `transposes_to` so the
report focuses on duplicates that still need a decision. Use
`--include-resolved` to see everything.

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
- Each A.Kan row above carries `transposes_to=<E.Nim slug>` so the
  audit can treat the pair as resolved and consumers can canonicalise
  by FEN computationally.
- Two redundant E.Nim siblings deleted (no children, identical FEN to
  their parent): `E.Nim.Kas.TKn`, `E.Nim.Rub.Sys`.

All five Kangaroo ↔ Nimzo groups now report as **resolved** in
`audit_transpositions.py --summary` and are hidden from the default
ranked report. Physical merge of `A.Kan.*` into `E.Nim.*` (slug
removal and child reparenting) remains out of scope; `transposes_to`
makes that future merge unnecessary for canonical lookup.

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
- Each A-side row above carries `transposes_to=<E side slug>` so the
  audit reports the pair as resolved.
- No rows deleted. No intra-E redundants in this family.

All ten Modern/OID ↔ KID groups now report as **resolved** in
`audit_transpositions.py --summary` and are hidden from the default
ranked report.

**Preserved as canonical** (no FEN coincidence with E.KID):

- `A.Mod` root and its non-...Nf6 children (Robatsch / Modern Defence
  against 1.d4, e.g. `A.Mod.e4`, `A.Mod.Avk` itself).
- `A.OID` root and its non-...Nf6 children (e.g. `A.OID.Mod`,
  `A.OID.Mod.MLn` before the Nf6 move).
- `A.Mod.Avk.MLn` (after castling but on a unique FEN, no E.KID
  equivalent).

### Modern intra-family A↔B (resolved, by FEN)

Five pre-KID Modern Defence groups where the A-side (1.d4 move order)
and B-side (1.e4 move order) reach the same FEN. The
canonicalisation rule applied: **B.Mod is canonical** when the
position is reached with both `1.e4` and `1.d4` on the board.

Rationale: ECO/textbook Modern Defence is `B06`/`B07`; the A-side
slugs (`A.Mod.*`, `A.OID.Mod.MLn`) are 1.d4-side or Old-Indian-side
move-order breadcrumbs into the same Modern tabiya. Choosing B
matches the literature default and aligns with consumers that key
Modern Defence by its ECO range.

**Pairings recorded** (B side canonical, A / OID side move-order):

| Position                                  | Canonical              | Transposition         |
|-------------------------------------------|------------------------|-----------------------|
| Modern Averbakh tabiya (4.e4 vs Bg7+d6)   | `B.Mod.Avk`            | `A.Mod.Avk`           |
| Same tabiya via 1...d6 Old Indian         | `B.Mod.Avk`            | `A.OID.Mod.MLn`       |
| Modern Averbakh Main Line (4...Nc6)       | `B.Mod.Avk.MLn`        | `A.Mod.Avk.Nc6`       |
| Modern extended centre (3...d6 4.c4)      | `B.Mod.Std.Ctr`        | `A.Mod.e4`            |
| Central Pterodactyl (...c5)               | `B.Mod.Std.Ctr.PtC`    | `A.Mod.e4.c5`         |
| Neo-Modern Defence (...e5)                | `B.Mod.Std.Ctr.e5`     | `A.Mod.e4.e5`         |

**Changes applied to the catalogue:**

- Each B-side row gains a short alias of the form
  `Modern [Averbakh|e4 ...] move-order` so a reader can find it by
  the move-order label too.
- Each A / OID-side row gets a `notes` field of the form
  `Move-order transposition to B.Mod...`.
- Each A / OID-side row carries `transposes_to=<B-side slug>`.
- No rows deleted. The triple `A.Mod.Avk ⇄ B.Mod.Avk ⇄ A.OID.Mod.MLn`
  is resolved with TWO non-canonical pointers into the same B
  canonical, which the audit's resolved-detection logic accepts.

All five groups now report as **resolved** in
`audit_transpositions.py --summary` and are hidden from the default
ranked report.

### London ↔ Zukertort London (resolved, by FEN)

Single pair where the same London System FEN (`1.d4 d5 2.Nf3 Nf6
3.Bf4`) is reached via two named routes:

| FEN pattern                | Canonical | Transposition         |
|----------------------------|-----------|-----------------------|
| London System (Bf4 setup)  | `A.Lon`   | `D.QPG.Zuk.Nf6.Bf4`   |

This is the **first canonical decision where the A side wins**.
Reason: "London System" is the strong literature name (ECO A48
assigns the position to the A range when reached this way); the
D-side slug is a Zukertort move-order descriptor with the literal
alias `London System` already on it. The choice acknowledges that
canonicalisation by FEN should also respect which slug carries the
stronger literary identity — the parent chain and the slug name
matter when the FEN alone is ambiguous between two equally valid
routes.

**Changes applied:**

- `D.QPG.Zuk.Nf6.Bf4.transposes_to = A.Lon`.
- `A.Lon` gains alias `Zukertort London move-order` (it had no
  aliases before; this is the first one).
- `D.QPG.Zuk.Nf6.Bf4.notes` reworded as a move-order transposition
  pointer.
- No rows deleted. `A.Lon` keeps its 4 children intact.

### Colle ↔ Zukertort Colle (resolved, by FEN)

Single pair following the London precedent: A-side canonical because
the literary name is stronger than the D-side move-order descriptor.

| FEN pattern                              | Canonical | Transposition          |
|------------------------------------------|-----------|------------------------|
| Colle System (1.d4 d5 Nf3 Nf6 e3 e6 Bd3) | `A.Col`   | `D.QPG.Zuk.Col.Bd3`    |

The D-side row already carried the alias `Colle System` and was
explicitly tagged as a Zukertort prefix into the Colle structure.
The transposition arrow makes that relation computable; `A.Col`
keeps its 4 children (`A.Col.Kol`, `A.Col.Zuk`, `A.Col.Phn`,
`A.Col.Bd6`) intact.

**Changes applied:**

- `D.QPG.Zuk.Col.Bd3.transposes_to = A.Col`.
- `A.Col` gains alias `Zukertort Colle move-order` (it had no
  aliases before; this is the first one — same pattern as London).
- `D.QPG.Zuk.Col.Bd3.notes` reworded as a move-order transposition
  pointer.

### Catalan Qc2 (resolved, by FEN — first deletion since Kangaroo)

Triple group resolved by combining a `transposes_to` arrow with a
physical row deletion of an intra-D redundant sibling.

| Position                                  | Outcome                                              |
|-------------------------------------------|------------------------------------------------------|
| `D.Cat.Cls.Qc2`                           | **Canonical**. Keeps 5 children (the deleted .Clo was the 6th, leaf). |
| `D.Cat.Cls.Qc2.Clo`                       | **Deleted**. Same FEN as its parent, 0 children, 0 inbound references — a Lichess-imported "Closed" label that added no information. |
| `E.Ind.Cat.d5.Bg2.Be7.Qc2`                | **Transposition**: `transposes_to = D.Cat.Cls.Qc2`. |

Rationale: the spec rule on Catalan classification says Catalan is
`D` when `...d5` structures the position; this FEN has `...d5` on
the board, so D-canonical is the principled choice. The E-side
slug describes the Indian Catalan move order with `...d5` inserted
late — same FEN, different route, marked as transposition.

**Changes applied:**

- `E.Ind.Cat.d5.Bg2.Be7.Qc2.transposes_to = D.Cat.Cls.Qc2`.
- `D.Cat.Cls.Qc2` gains alias `Indian Catalan Qc2 move-order`.
- `E.Ind.Cat.d5.Bg2.Be7.Qc2.notes` reworded as transposition pointer.
- `D.Cat.Cls.Qc2.Clo` row deleted (0 children, 0 inbound refs).

After this sprint the audit still reports **316 duplicate groups**:
the deleted row collapsed the triple into a pair, but the remaining
pair is still a duplicate by FEN — it is now **resolved** through
`transposes_to`, so it disappears from the default ranked report.

### Queen's Indian ↔ English Defence (resolved, by FEN)

Single pair. When the FEN reaches a true Queen's Indian structure
(`1.d4 Nf6 2.c4 e6 3.Nf3 b6`), the canonical slug is the E-side
Indian name regardless of which move order produced it.

| Position           | Canonical | Transposition           |
|--------------------|-----------|--------------------------|
| Queen's Indian, 3...b6 | `E.QID` | `A.Owe.Eng.Nf3.Nf6`     |

Rationale: this reinforces the rule **Indian-structure-by-FEN → E
canonical**, already applied for Kangaroo↔Nimzo, Modern/OID↔KID,
and Catalan Qc2 (where the rule pointed the other way because of
the explicit `...d5` Catalan exception). The English Defence
(`1.d4 b6`) is a legitimate move-order route but the destination
position is universally named Queen's Indian.

**Changes applied:**

- `A.Owe.Eng.Nf3.Nf6.transposes_to = E.QID`.
- `E.QID` gains alias `English Defence Nf3 move-order`.
- `A.Owe.Eng.Nf3.Nf6.notes` reworded as transposition pointer.
- No rows deleted. `E.QID` keeps its 9 children intact.

### Resolved batch — high-confidence transpositions (multi-family)

Big multi-family pass over the top 80 ranked unresolved groups,
driven by parallel agent classification with same-FEN verification
on every proposal. Two patterns applied:

1. **`transposes_to` arrow** when both rows have substantive
   children or are family-level anchors that should stay alive as
   navigation breadcrumbs.
2. **Physical deletion** when a row is a Lichess-imported descriptor
   sibling that has identical FEN to its direct parent, 0 children,
   and 0 inbound `transposes_to` refs — adding no information.

**Families covered**

| Family pattern | Canonical side | Transposing side | Pairs | Deletions |
|---|---|---|---|---|
| Horwitz French ↔ QGD | `D.QGD.*` (Queen's Gambit Declined named tree) | `A.Hor.Fch.*` (1.d4 e6 c4 d5 move-order) | 13 | 0 |
| Kangaroo ↔ Nimzo (deep continuation) | `E.Nim.Rub.*` | `A.Kan.MLn.e3.*` | 4 | 0 |
| Horwitz Keres ↔ Bogo-Indian | `E.Bog` | `A.Hor.Ker` | 1 | 0 |
| Vampire-Mengarini ↔ Scandinavian | `B.Sca.Nc3*` (ECO B01) | `A.Van.d5.e4.*` (A00 curiosity) | 4 | 0 |
| Reti Anglo ↔ English Caro-Kann path | `A.Ret.Ang*` | `A.Eng.CKa.Nf3.d5*` | 2 | 1 leaf |
| Reti QGI ↔ English Agincourt path | `A.Ret.QGI` | `A.Eng.Agi.Nf3.d5` | 1 | 1 leaf |
| Yugoslav Dragon path collapse | `B.Sic.Dra.Yug` | `B.Sic.Dra.Yug.Nc6.Bc4` (kept w/ children) | 1 TT | 2 leaves |
| Four Knights ↔ Petrov 3-Knights | `C.Fou` | `C.Pet.Thr.Fou` | 1 | 0 |
| Anti-Berlin ↔ Portuguese path | `C.RyL.Ber.d3` | `C.KPO.Prt.MLn.Nc6.Nf3*` | 1 | 0 |
| Centre Game vs Pirc prefix (mixed) | `C.Cen.d6` (literary, 1 child) | `B.Pir.Pre.d4.e5` (0 kids) | — | 1 |
| Intra-D Lichess-descriptor cleanup | various D parents | various deep `.Std` / `.Mer` / `.Cze` / `.Sch` etc. leaves | — | 20 |
| Intra-E Lichess-descriptor cleanup | various E parents | `.Trd` / `.TrP` / `.Pan` / `.Rub` / `.Bob.Rub` / `.Flo.Fis` etc. | — | 6 |
| Intra-A / intra-B / intra-C / mixed | various canonical anchors | Lichess deep-path descriptors | 1 TT | 10 |

**Totals applied**: 28 new `transposes_to` arrows + 40 row deletions.
All deletions verified to have 0 children and 0 inbound references at
apply time. The validator's same-FEN check confirmed every new
`transposes_to` link.

**Deferred from this batch** (do not touch yet):

- French Classical / Veresov 3-way (`B.Fre.Cls.MLn ⇄ A.Ver.Cls.MLn.Be7 ⇄ D.QPG.Ver.MLn.Be7`).
- Veresov A↔D triple (`A.Ver ⇄ D.QPG.Ver ⇄ D.QPG.Ver.Ric`) and its
  subtree (`A.Ver.Ric`, `A.Ver.Cls.MLn`, `D.QPG.Ver.MLn`).
- Intra-E triple `E.KID.Cls.Old.e5 ⇄ E.KID.Cls.e5.O-O.Nbd7 ⇄ ...O-O`
  (3-way intra-E, needs careful subtree review).
- Intra-E triple `E.Ben.Mod.Cls ⇄ Trd ⇄ E.Ind.e6...` (parent/child
  same FEN + cross-family E, needs structural review).
- `D.Rub ↔ A.Col.Zuk` (Rubinstein Opening vs Colle-Zukertort —
  different conceptual families, no clear precedent yet).
- A handful of MEDIUM-confidence groups where both sides have
  substantive children (logged by the agents).

### Resolved batch — intra-family duplicate cleanup

Big intra-family pass over the top 120 ranked unresolved groups,
classified by 3 parallel agents (intra-E, intra-D, intra-A/B/C).
Each agent verified `kids=0 ∧ inbound_refs=0` for every DELETE
candidate against the live catalogue before recommending.

**Pattern**: deep slugs imported from Lichess with `.Std`, `.Closed`,
`.Mer.Mer`, `.Trd`, `.Pan`, `.Cls.Nf3.Nbd7.Rc1.c6`-style move-order
descriptors duplicating a shorter named anchor. Where the descriptor
had children, a `transposes_to` arrow was added instead of deletion.

**Counts by family**

| Family | DELETE | TT |
|---|---:|---:|
| E.KID (King's Indian) | 12 | 1 |
| E.QID (Queen's Indian) | 4 | 1 |
| E.Ben (Benoni / Benko) | 3 | 0 |
| E.Gru (Grünfeld) | 3 | 0 |
| E.Nim (Nimzo-Indian) | 2 | 0 |
| E.Ind / E.OldI (Indian root / Old Indian) | 3 | 0 |
| D.QGD (Queen's Gambit Declined family) | 25 | 1 |
| D.Sem (Semi-Slav) | 9 | 0 |
| D.Sla (Slav) | 2 | 0 |
| D.Cat (Catalan) | 4 | 1 |
| D.Tar (Tarrasch) | 3 | 1 |
| D.STa (Symmetrical Tarrasch) | 3 | 0 |
| D.QGA (Queen's Gambit Accepted) | 2 | 0 |
| D.QPG.Zuk (Zukertort, not Veresov) | 1 | 0 |
| A.Eng / A.KIA / A.Ret | 4 | 0 |
| B.Sic (Sicilian Dragon/Open Knight, Najdorf) | 5 | 2 |
| B.CaK / B.Fre.Tar | 2 | 1 |
| C.RyL / C.Vie / C.Ita / C.PhD | 4 | 1 |
| **TOTAL** | **91** | **10** |

(Actual applied totals: 84 DELETE + 10 TT; the family table above
counts the canonical-side aliases that fired across families;
deletions may belong to several family rollups when grandparents
differ. See git for the exact slug list.)

**Test impact**: one test in `test_from_eco.py` was updated to
reference `B.Sic.Naj.Eng.MLn` instead of `B.Sic.Naj.Eng.e5.Nb3.Be6`
(the latter was collapsed into the former during this batch as they
shared identical FEN and moves_uci).

**Still deferred for the next pass**:

- French / Veresov complex (ranks 1, 2, 5, 8) — needs conceptual
  decision on the 3-way A/B/D French Classical Main Line.
- KID Classical Old/e5 intra-E triple (rank 3) and Modern Benoni
  cross-E triple (rank 4) — structural review.
- D.Rub ↔ A.Col.Zuk outlier (rank 6).
- A handful of MEDIUM-confidence intra-class groups where both sides
  have substantive children (`E.KID.Fch.Kav`, `E.KID.Avk`,
  `D.Sem.Mer.MLn.Old`, `D.Sem.AMe.Sto`, `D.Sla.Cze.Kra.MLn`,
  Italian Giuoco/Two Knights pair, English Mikenas-Agincourt deep
  three-way, Caro-Kann Ruy López Caro/b5/Bb3 line).

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
