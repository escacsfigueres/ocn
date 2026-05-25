# Transpositions in OCN-1

## Current state

- Catalogue size: **5,900** rows.
- Duplicate FEN groups: **125** total — **119 resolved** (**15 with
  multiple canonicals**, 104 single canonical), **6 unresolved**.
- Rows in unresolved groups: **12**.
- Top group size in unresolved: **2** (all remaining unresolved
  are pairs; Van triple resolution removed the last conceptual
  triple).
- Resolution channels: `transposes_to` (non-canonical →
  canonical, asymmetric) and `same_as` (canonical ↔ canonical,
  symmetric, OCN 0.3).
- All remaining unresolved groups were classified in
  [`unresolved-map-20.md`](unresolved-map-20.md) (snapshot at
  `f06e242`). The 14 mechanical groups have since been resolved
  (see "Post-map mechanical cleanup batch" below). **The 6 still
  unresolved** are the conceptual / ON-HOLD set: Modern/Sicilian
  cross-family, Nimzo Bot/Kmo (ON HOLD), QID Miles/Petrosian, KID
  Simagin/Uhlmann, Scandinavian Gipslis/Portuguese, Amar/Hungarian
  — all `proposal_needed` except the ON-HOLD Nimzo (the only one
  needing external bibliography).

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

## Arbitration policy

Operational summary of the canonicalisation rules. Full text and
reasoning live in [`spec/OCN-1.md`](../spec/OCN-1.md) under
"Canonicalisation arbitration". Rules are **ordered** — apply rule
1 first, fall through to the next if it does not resolve.

1. **Established name beats descriptor.** Literary opening name vs
   path / Lichess label → literary name canonical.
2. **Spec-governed structural classes win.** Borderline rules in
   the spec (Catalan ...d5 → D, Indian without ...d5 → E, Grünfeld
   → E, Benoni / Benko → E, OID with ...Nf6 reaching a KID FEN →
   E.KID, …) take precedence.
3. **Parent–child same-FEN redundancy.** Parent is canonical; child
   may be deleted only if leaf + no inbound refs + no literature
   identity beyond the parent.
4. **Two real names → preserve both.** Default to preservation. Use
   `transposes_to` only when one side is unambiguously dominant for
   position lookup. Otherwise **defer**.
5. **Family tabiya beats move-order breadcrumb.** Family tabiya
   canonical; breadcrumb gets `transposes_to`.
6. **Prefer `transposes_to` over slug surgery when surgery
   cascades.** Physical deletion is reserved for leaves with no
   children, no inbound refs, and descriptor-only identity.
7. **ECO is evidence, not authority.** Record ECO in `eco_legacy`
   and `notes`; do not let a flat 1971 code override a stronger
   structural or literary rule.

## Deferred conceptual families

Groups in the current top 30 that are flagged "do not auto-resolve"
under rule 4 or 6, pending a human decision:

| Group | Slugs | Why deferred |
|---|---|---|
| ~~French / Veresov~~ | ~~3-way A↔B↔D~~ | **RESOLVED** in commit `c0ffee2` — see "French / Veresov complex" section below for the applied resolution (multiple-canonical group for rank 1; transposes_to + targeted deletions for the rest). |
| ~~Veresov A↔D subtree~~ | ~~A.Ver ⇄ D.QPG.Ver ⇄ D.QPG.Ver.Ric~~ | **RESOLVED** with the same commit. D.QPG.Ver subtree now points into A.Ver canonicals. |
| ~~KID Old / Classical e5~~ | ~~3-way intra-E~~ | **RESOLVED** in commit `<see below>` — multiple_canonical at rank 1 (Old Main Line E91 + Castled Nbd7 E95 coexist), single_canonical at the two child mirror groups (Old.e5.c6/Re1 canonical, e5.O-O.Nbd7.c6/Re1 → TT). See "KID Classical Old/e5" section below. |
| ~~Modern Benoni Classical/Traditional~~ | ~~3-way Benoni + Indian~~ | **RESOLVED** as single_canonical — counter-example to KID Classical where 3 slugs converged on one FEN but only one carried independent literary identity. See "Modern Benoni Classical" section below. |
| ~~D.Rub ↔ A.Col.Zuk~~ | ~~Rubinstein ⇄ Colle-Zukertort~~ | **RESOLVED via `same_as`** in the OCN 0.3 schema extension. See "same_as-resolved groups" section below. |
| **Italian Giuoco / Two Knights post-castling** (ranks 21, 22) | `C.Ita.Giu.O-O.Nf6 ⇄ C.Ita.Two.O-O.Bc5` and `.d4` deeper | Classic transposition: Giuoco Piano with Black's …Nf6 reaches the same castled tabiya as Two Knights with Black's …Bc5. Both real lines, both with children. |
| **Philidor Nimzowitsch / Lion castled** (ranks 16, 17) | `C.PhD.Nim ⇄ C.PhD.Lio.MLn.O-O` and `.Re1` deeper | Nimzowitsch Variation and Lion Defence Main Line converge after castling. Lion is the path (kids); Nimzowitsch is the named ECO-C41 anchor. Candidate for TT under rule 1, but Lion has substantive identity — defer pending rule 4 review. |
| **English Mikenas / Agincourt** (rank 12 + family) | `A.Eng.Mik ⇄ A.Eng.Agi.Nc3.Nf6.e4` | Same English Opening family, both literary (Mikenas-Carls vs Agincourt) reaching the same FEN after `1.c4 Nf6 2.Nc3 e5 3.e4`. Pure rule 4 case. |
| **Reverse-direction Meran** (rank 9) | `D.Sem.Mer.MLn.Old ⇄ D.Sem.Mer.MLn.c5.e5` | Same FEN; `.Old` carries "Old Variation" literary tag with 0 kids while `c5.e5` is structural path with 1 kid. Reverse of the usual direction (descriptor with children). Defer until OCN-0.3 decides whether a kid-bearing path can be transposed to a leaf-named slug. |

### What this list means

These are the **conceptual residue** after the high-confidence
intra-family cleanup. None of them can be safely resolved by the
patterns established so far. Each one needs an explicit choice
written into the catalogue's notes (and possibly into this document)
before any `transposes_to` arrow is added.

Once the French / Veresov complex is decided, several of the
others (KID Old/e5 triple, Modern Benoni Classical/Traditional)
will likely follow the same conceptual pattern and can be resolved
together.

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

### French / Veresov complex (resolved, with multiple canonicals)

First case where two canonical slugs coexist in the same FEN group
**by design**. Proposed in
[`veresov-french-proposal.md`](veresov-french-proposal.md) and
applied here. Supporting tool change: the audit now distinguishes
`single_canonical` from `multiple_canonical` resolution kinds
(`tools/audit_transpositions.py --summary` reports
`multiple_canonical_groups`).

**Rank 1 — three names, one FEN, two canonicals preserved**

| slug | role | action |
|---|---|---|
| `B.Fre.Cls.MLn` | French Classical Main Line (ECO C13/C14) | **PRESERVED canonical**. Note extended to cross-reference Richter-Veresov. |
| `A.Ver.Cls.MLn.Be7` | Richter-Veresov Classical Be7 (ECO D01) | **PRESERVED canonical**. |
| `D.QPG.Ver.MLn.Be7` | Queen's Pawn Veresov Main Line Be7 | TT → `A.Ver.Cls.MLn.Be7`. |

The audit now reports rank 1 as `resolution_kind=multiple_canonical`,
`canonical_count=2`. The group is resolved (hidden from the default
ranked report) because the only non-canonical entry points into the
group; the two canonicals are kept on purpose.

**Veresov A↔D subtree — D.QPG.Ver collapses into A.Ver**

| from (D-side breadcrumb) | → | to (A-side canonical) |
|---|---|---|
| `D.QPG.Ver` | → | `A.Ver` |
| `D.QPG.Ver.Ric` | → | `A.Ver` |
| `D.QPG.Ver.Ric.Bf5` | → | `A.Ver.Ric` |
| `D.QPG.Ver.MLn` | → | `A.Ver.Cls.MLn` |

`A.Ver` canonicals receive a short alias of the form
`Queen's Pawn Veresov [...] move-order`.

**Deleted as redundant mirrors** (leaves, 0 children, 0 inbound refs):

- `D.QPG.Ver.Ric.Nbd7.Nf3` — mirror of `D.QPG.Ver.Nbd7.Nf3` via the
  Nf6 move order.
- `D.QPG.Ver.Ric.Nbd7` — parent of the above; becomes leaf after
  the cascade.
- `D.QPG.Ver.Ric.Ne4` — mirror of `D.QPG.Ver.Ne4` via Nf6 move order.
- `B.Fre.Cls.MLn.e5.Nfd7.Qxe7` — mirror of `B.Fre.Cls.MLn.e5.Qxe7`
  via the explicit Nfd7 path.

Net change: **5 transposes_to arrows + 4 row deletions** + alias
and note touches. No reparenting. The `A.Ver` subtree preserves
its 3 children intact; `D.QPG.Ver` keeps `Nbd7`, `Nbd7.Nf3`, `Ne4`
as still-canonical sibling slugs (no Ric mirror needed any more).

### KID Classical Old/e5 (resolved, mixed multiple + single canonical)

Second case where the `multiple_canonical` resolution kind applies,
and the first where it lives **inside a single class** (E). Three
FEN groups handled together; see
[`kid-classical-transposition-proposal.md`](kid-classical-transposition-proposal.md)
for the full reasoning.

**Rank 1 — Old Main Line (E91) and Castled Nbd7 (E95) coexist**

| slug | role | action |
|---|---|---|
| `E.KID.Cls.Old.e5` | E91 Old Main Line — literary anchor on the `Old Main Line` branch | **PRESERVED canonical** |
| `E.KID.Cls.e5.O-O.Nbd7` | E95 Castled with Nbd7 — structural anchor on the `e5 Prefix` branch | **PRESERVED canonical** |
| `E.KID.Cls.e5.O-O.Nbd7.O-O` | E94 "Positional Defence" via the OID move order | TT → `E.KID.Cls.e5.O-O.Nbd7`. Kept alive so the group has a declared pointer (precedent: `multiple_canonical` requires at least one in-group pointer; without it the group would stay `unresolved`). |

The OID descriptor was kept alive (with TT) rather than deleted —
this is the lever that makes the `multiple_canonical` resolution
computable today, without growing the schema (no `same_as` column
needed yet).

**Ranks 15 and 16 — mirror leaves, single canonical**

Two paired leaves whose pair distinction is structural mirror
only (same ECO code on both sides, no separate literary identity
beyond the parent decision):

| from | → | to (canonical) | parent rationale |
|---|---|---|---|
| `E.KID.Cls.e5.O-O.Nbd7.c6` | → | `E.KID.Cls.Old.e5.c6` | E96 c6 line; the Old.e5 branch carries the literary anchor. |
| `E.KID.Cls.e5.O-O.Nbd7.Re1` | → | `E.KID.Cls.Old.e5.Re1` | E95 Re1 line; same reasoning. |

**Net change**: 3 transposes_to arrows, 5 cross-reference notes,
0 deletions. The 7 rows that were in 3 unresolved groups now sit
in 1 resolved-multiple_canonical group + 2 resolved-single_canonical
groups.

**Precedent set**: `multiple_canonical` is reserved for cases where
literature distinguishes both names at the same FEN AND a
third-party pointer exists to declare the relation. Leaf mirrors
without independent literary identity default to single_canonical.

### `same_as`-resolved groups (OCN 0.3)

Schema extension shipped in commit `84f18fc`. The new `same_as`
column declares co-canonical pairs without forcing one to be
non-canonical. The audit treats in-group `same_as` edges as
undirected and reports such groups as `multiple_canonical`.

**Groups resolved purely via `same_as`** (no in-group
`transposes_to` pointer; both rows canonical by editorial decision):

| pair | classes | both ECO | rationale |
|---|---|---|---|
| `D.Rub` ⇄ `A.Col.Zuk` | A, D | D05 | Rubinstein Opening (historical) and Colle-Zukertort (contemporary) — the textbook case the schema was introduced for. |
| `E.Nim.Rub.Kmo` ⇄ `E.Nim.Sml.Bot.MLn` | E | E40 / E25 | Nimzo Kmoch (Rubinstein move order) and Sämisch Botvinnik Main Line (Sämisch move order); both literary, different ECOs, same FEN. |
| `C.Ita.Giu.O-O.Nf6` ⇄ `C.Ita.Two.O-O.Bc5` | C | C50-C54 / C55-C56 | Giuoco Piano and Two Knights Defence converge after castling — textbook ECO transposition between two named openings. |
| `C.Ita.Giu.O-O.Nf6.d4` ⇄ `C.Ita.Two.O-O.Bc5.d4` | C | C54 / C56 | Same convergence one move deeper (4.d4). |
| `A.Lar.Cls.MLn` ⇄ `A.Ret.Nim.MLn` | A | A01 / A06 | Nimzo-Larsen Attack (1.b3 move order) and Reti Nimzowitsch-Larsen (1.Nf3 then 2.b3 move order) — both real opening names with distinct ECO codes and independent family subtrees. First post-OCN-1.0.3 `same_as` addition. |
| `A.Lon.Cls.MLn` ⇄ `A.Lon.Msn.MLn.Nbd2` | A | A48 / A48 | Classical London System (contemporary literary name) and Mason London (historical, attributed to James Mason 19th–20th century) — both A48, both with their own subtree, cascading `.c4` pair also resolved bilaterally. |
| `A.Lon.Cls.MLn.c4` ⇄ `A.Lon.Msn.MLn.Nbd2.c4` | A | A48 / A48 | Same convergence one move deeper (`...c4`) inside the London System Cls/Msn pair. |
| `A.Van.ReN.e3.d5` ⇄ `A.VtK.e5.Nc3.d5` | A | A00 / A00 | Van Geet Reversed Nimzowitsch d5 (1.Nc3) and Van't Kruijs Keoni-Hiva Ekolu Variation (1.e3) — both real opening-family identities. Same FEN via different first moves. Note: `A.Van.d5.e3.e5` is a third path through the same FEN but stayed as `transposes_to` (structural breadcrumb under "d5 Line" prefix, not literary). |
| `A.Van.ReN.e3` ⇄ `A.VtK.e5.Nc3` | A | A00 / A00 | Parents of the rank-1 pair (after 3 plies). Reversed Nimzowitsch e3 prefix vs Keoni-Hiva Prefix — both anchored in their respective family root literary identities. |
| `D.QGA.Flo.MLn` ⇄ `D.QGA.Jan.e3.b5` | D | D20 / (D25 inherited) | Flohr Variation Main Line vs Haberditz Variation (Janowski-Larsen e3 path). Both real QGA literary attributions; same FEN reached via different move orders inside the Queen's Gambit Accepted family. |
| `E.Bud.Adl.MLn` ⇄ `E.Bud.Rub.MLn` | E | A52 / A52 | Budapest Adler (4.Nf3 order) vs Rubinstein (4.Bf4 order) main line — two real player-named move-order routes into the same A52 tabiya. Cascade level 1. |
| `E.Bud.Adl.MLn.e3` ⇄ `E.Bud.Rub.MLn.e3` | E | A52 / A52 | Same Budapest Adler/Rubinstein convergence one move deeper (e3 + Nbd2 + O-O). Cascade level 2. |
| `E.Bud.Adl.MLn.e3.Be2` ⇄ `E.Bud.Rub.MLn.e3.Be2` | E | A52 / A52 | Same convergence at the Be2 line (+...d6). Cascade level 3 — deepest same_as cascade in the series. The Adler-only `.Re8` leaf extends beyond and stays a normal descendant. |

**Groups previously multi-canonical via in-group pointer, now also
carrying explicit `same_as`** (declaration made more readable; no
behaviour change):

| pair | how |
|---|---|
| `B.Fre.Cls.MLn` ⇄ `A.Ver.Cls.MLn.Be7` | Pre-existing TT from `D.QPG.Ver.MLn.Be7` provided the in-group pointer; `same_as` now makes the bilateral relation explicit between the two canonicals. |
| `E.KID.Cls.Old.e5` ⇄ `E.KID.Cls.e5.O-O.Nbd7` | Same shape — TT from `E.KID.Cls.e5.O-O.Nbd7.O-O` is the in-group pointer; `same_as` makes the canonical relation explicit. |

**Total multiple_canonical groups**: **15** as of the Budapest
Adler/Rubinstein sprint (was 2 before `same_as`, 6 after the
OCN 0.3 schema commit, 7 after Larsen, 9 after London cascade,
11 after Van cascade, 12 with QGA Flohr, +3 with the Budapest
Adler/Rubinstein 3-level cascade). Reported by
`audit_transpositions.py --summary` as
`multiple_canonical_groups=15`.

**`same_as` multi-target (N=2 pipe-separated) usage so far**: 0.
The schema supports it; the Van triple was the first plausible
test case but structural analysis showed only 2 of 3 slugs are
genuine literary canonicals, so Option D (mixed `same_as` + `transposes_to`)
was the honest resolution. Multi-target remains available for a
future case with three genuine literary identities on one FEN.

### Post-map mechanical cleanup batch

Executed against the 14 mechanical groups classified in
[`unresolved-map-20.md`](unresolved-map-20.md) (the 5
`SINGLE_CANONICAL_MIRROR` + 9 `LONG_TAIL_MECHANICAL` groups). One
commit, no proposals, no `same_as`. The 6 conceptual / ON-HOLD
groups were deliberately left untouched.

**12 `transposes_to` + 2 `DELETE`**:

| group | action | non-canonical → canonical | family |
|---|---|---|---|
| Czech-Indian QPO | TT | `A.QPO.c6.Nf3.Nf6 → A.QPO.Nf6.Nf3.c6` | A — "Czech-Indian" name kept canonical |
| French Winawer Advance | TT | `B.Fre.Win.Adv.MLn.Ne7.Nf3 → …MLn.Nf3` | B — leaf → developed |
| Najdorf Scheveningen | TT | `B.Sic.Naj.Sch.MLn → …Sch.O-O` | B — 0 vs 3 children |
| Reti/English Caro-Kann g3 | TT | `A.Eng.CKa.Nf3.d5.g3.Bg2 → A.Ret.Ang.g3.Nf6.Bg2` | A — cross-family, 0 vs 3 children |
| Alekhine d6 | TT | `B.Ale.Nrm.Dpn.d6.c4.Nb6 → …d6.Nb6` | B — deeper-path → shallower |
| KGm Bishop's Gambit | TT | `C.KGm.Acc.Bsh.Nf6.Nc3 → …Bsh.MLn` | C — shallower "Main Line" |
| Semi-Slav Bg5 Accepted | TT | `D.Sem.Bg5.Acc → D.Sem.Bg5.dxc4` | D — Accepted = ...dxc4 |
| Muzio Qxf3 node | TT | `C.KGm.Acc.Muz.Dbl.MLn → …Muz.MLn.Qxf3` | C — Double Muzio premature here |
| Caro-Kann Tal | TT | `B.CaK.Adv.Tal.MLn → …Tal.h5` | B |
| Caro-Kann Short | TT | `B.CaK.Adv.Sht.O-O → …Sht.MLn` | B — equal children, "Main Line" tiebreak |
| Sicilian Scheveningen Keres | TT | `B.Sic.Sch.Krs.MLn → …Krs.h6` | B |
| Muzio gxf3 node | TT | `C.KGm.Acc.Muz.Dbl → C.KGm.Acc.Muz.MLn` | C — Double Muzio premature here |
| French Steinitz a6 | **DELETE** | `B.Fre.Nrm.d5.Nc3.a6.Nf3` (kept `.Nfd7` "Steinitz Variation") | B — identical move list, leaf |
| Winawer Poisoned Pawn | **DELETE** | `B.Fre.Win.Psn.MLn.Qxg7` (kept `.Ne2`) | B — identical move list, leaf |

**Double Muzio micro-check**: the `.Dbl`/`.Dbl.MLn` nodes share
the FEN of the Muzio main line at the gxf3 and Qxf3 positions; the
defining second sacrifice (Bxf7+) diverges *later* and correctly
lives at `C.KGm.Acc.Muz.MLn.Dbl`. So the premature Double-Muzio
slugs transpose into the main line (cascade: `.Dbl → .MLn`,
`.Dbl.MLn → .MLn.Qxf3`).

**Audit impact**:
- duplicate_groups: 127 → 125 (−2: each DELETE collapsed its group)
- resolved_groups: 107 → 119 (+12 TT)
- unresolved_groups: 20 → **6** (−14)
- rows_in_unresolved_groups: 40 → 12 (−28)
- depth_varying_groups: 4 → 0
- catalogue rows: 5,902 → 5,900 (−2)

**The 6 remaining unresolved groups** are exactly the conceptual /
ON-HOLD set from the map: Modern/Sicilian cross-family [1], Nimzo
Bot/Kmo ON HOLD [2], QID Miles/Petrosian [10], KID Simagin/Uhlmann
[11], Scandinavian Gipslis/Portuguese [12], Amar/Hungarian [14].
All five non-ON-HOLD ones are `proposal_needed` (same_as or
cross-family arbitration); none needs external bibliography except
the Nimzo ON-HOLD case.

### Post-0.2 parent-child cleanup batch

Mechanical sweep over the parent-child same-FEN residuals in the top-60 unresolved (a child slug carrying the identical FEN to its direct parent, reached either by an identical move list or a pure move-order variant). Same arbitration rules as the earlier batches: DELETE a leaf descriptor with no inbound refs and no independent literary name; `transposes_to` the parent when the child has its own children or carries a name worth preserving.

**7 groups resolved (4 TT + 3 DELETE)**:

| child | parent | action | reason |
|---|---|---|---|
| `A.PQI.e3.Bb7` | `A.PQI.e3` | TT | child has a `.Bb2` branch; preserve subtree |
| `A.Tro.Bxf6.e3` | `A.Tro.Bxf6` | TT | child has a `.d5` branch; preserve subtree |
| `A.Ret.f5.d3.e4` | `A.Ret.f5.d3` | TT | preserves the Lisitsyn Gambit Deferred name |
| `A.Ret.Eng.Be7.O-O.NCD` | `A.Ret.Eng.Be7.O-O` | TT | preserves the Neo-Catalan Declined name (real opening identity) |
| `A.Ret.Nh6.d4.g6` | — | DELETE | leaf, "Kingside Variation" already on parent, 0 inbound |
| `A.Owe.Eng.e6` | — | DELETE | leaf, pure "e6 Move Order" descriptor, 0 inbound |
| `A.And.Cre.ClD` | — | DELETE | leaf, Lichess exact-move-order descriptor, 0 inbound |

**Audit impact**:
- duplicate_groups: 130 → 127 (−3: each DELETE collapsed its group)
- resolved_groups: 100 → 104 (+4 TT)
- unresolved_groups: 30 → 23 (−7)
- rows_in_unresolved_groups: 60 → 46 (−14)
- catalogue rows: 5,905 → 5,902 (−3)

No same_as, no reparenting, no conceptual decisions. Nimzo Sml Bot/Kmo left ON HOLD; Czech-Indian and Modern/Sicilian cross-family untouched.

### Resolved: English Symmetrical Three Knights mirror

Pure descriptive move-order mirror under `A.Eng.Sym.Nf3.Nf6` / `A.Eng.Sym.Nc3.Nf6`. Both slugs reach the same FEN
`rnbqkb1r/pp1ppppp/5n2/2p5/2P5/2N2N2/PP1PPPPP/R1BQKB1R b KQkq -`
(Symmetrical English Three Knights, after `1.c4 c5` and the {Nc3, Nf3, Nf6} development) via swapped white-knight order.

**Resolution**: `single_canonical` with `transposes_to`.

| slug | role | reason |
|---|---|---|
| `A.Eng.Sym.Nf3.Nf6.Nc3` (A34) | **CANONICAL** | Hosts the developed Four Knights subtree (5 named children: `.Nc6`, `.d4`, `.g3`, `.O-O` Mecking, `.d5`). Editorial choice already encoded by the deeper structure. Promoted to carry both aliases: `Nc3 Line|Three Knights Line`. |
| `A.Eng.Sym.Nc3.Nf6.Nf3` (A34/A35) | `transposes_to = A.Eng.Sym.Nf3.Nf6.Nc3` | Mirror move order. Has 1 child (`.e5` line, A35) which remains a distinct branch under this path. |

No same_as: no two literary identities at this FEN — just two descriptive paths to the same Symmetrical English Three Knights position. No deletions, no reparenting, no cascade.

**Net change**: 1 TT + alias merge + notes cross-reference on both rows.



Third top-1 case in a row, but the **first to resolve as
single_canonical** despite a 3-way group. See
[`modern-benoni-transposition-proposal.md`](modern-benoni-transposition-proposal.md)
for the full analysis.

**Rank 1 — three slugs, one literary anchor**

| slug | role | action |
|---|---|---|
| `E.Ben.Mod.Cls` | "Modern Benoni, Classical" (ECO A70-A79, 7 named children) — only literary anchor | **PRESERVED canonical**. Alias `Traditional Variation` added so the Lichess label remains searchable. |
| `E.Ben.Mod.Cls.Trd` | Self-described move-order descriptor ("Nf3 move order into the Classical Modern Benoni"); 0 kids | TT → `E.Ben.Mod.Cls`. Kept as breadcrumb. |
| `E.Ind.e6.Nf3.c5.d5.Be2` | Same `moves_uci` literally identical to `.Trd`; 0 kids | DELETE. Pure duplicate descriptor parented under the Anti-Nimzo Indian tree. |

**Why not multiple_canonical**: `multiple_canonical` is reserved
for cases where literature distinguishes two names on the same
FEN with independent identity (distinct ECO codes, own subtrees,
literature treating them as separate openings). Here both
non-canonical slugs are self-described move-order descriptors, the
ECO range is identical (A70), and only `E.Ben.Mod.Cls` carries the
substantive subtree (7 children for actual White plans). Number of
slugs in the group does not decide the resolution kind — content
does.

**Cascading cleanups in the same commit**:

- Rank 70: `E.Ben.Mod.Cls.MLn.Re8.Nd2` deleted (sibling mirror of
  `E.Ben.Mod.Cls.MLn.Re8.Tal`, both aliased "Tal Line"; literary
  Tal label survives, move-name redundant removed). The group
  collapses to size 1 and disappears from the audit.
- Rank 111: `E.Ben.Bnk.Acc.MLn.g6.f4` → TT to
  `E.Ben.Bnk.Acc.MLn.Bxa6.f4`. Two Benko Accepted leaves with
  the same `Central Storming Variation` alias and notes; Bxa6 is
  the canonical Benko move order at this depth.

**Net change**: 2 TT + 2 deletions + alias/notes touches. No
reparenting.

**Precedent reinforced**: group size alone does not determine
resolution kind. `multiple_canonical` requires *content evidence*
of two real names, not just a count.

### Post-0.2 Phase 1 cleanup batch 2

Mechanical descriptor cleanup over the top 80 unresolved. Same
arbitration rules as batch 1, applied at scale.

**Pattern dominant**: Lichess-imported descriptor leaves with the
self-explaining `.Std`, `.Mer`, `.Sto`, `.Gel`, `.Bro`, `.Duz`,
`.Lin`, `.Sad`, `.TKn`, `.Lut`, `.Hen`, `.Spi`, `.Lit`, `.Nrm`,
`.Max.Max`, `.Bog.Std`, `.Nf6.Nrm`, `.Q-O.Hen` suffixes
duplicating a literary anchor parent or sibling.

**Counts by family** (60 DELETE + 10 TT, applied):

| Family | DELETE | TT |
|---|---:|---:|
| D.QGA (Queen's Gambit Accepted) | 11 | 0 |
| D.Sla (Slav family) | 11 | 0 |
| D.Sem (Semi-Slav) | 5 | 1 |
| D.STa (Semi-Tarrasch) | 4 | 2 |
| D.Tar (Tarrasch) | 2 | 0 |
| D.Bgm (Blackmar-Diemer) | 3 | 0 |
| D.QGD (Cambridge Springs, Reshevsky, Vienna, Ragozin, etc.) | 7 | 0 |
| D.QPG.Zuk | 1 | 0 |
| E.KID (Yugoslav Fianchetto) | 1 | 0 |
| E.Gru (Saemisch, Nf3) | 2 | 0 |
| E.Nim (4.f3 Kmoch) | 1 | 0 |
| E.Blf (Blumenfeld) | 1 | 0 |
| E.Ind (Normal Variation) | 1 | 0 |
| A.Eng (Symmetrical c5, Agincourt Nf6) | 2 | 0 |
| A.Mik (Lithuanian) | 1 | 0 |
| A.EID (Przepiorka / Fianchetto MLn) | 0 | 2 |
| C.RyL (Exchange, Ba4 path collapses) | 4 | 1 |
| C.Ita (Pianissimo Nor, Giuoco Cls, Two Knights Max/Spi) | 4 | 0 |
| C.Fou (Spanish Rubinstein Henneberger) | 1 | 0 |
| B.Sic (Closed Fianchetto, Naj reorg, CaK Karpov) | 2 | 1 |
| B.CaK (Karpov Modern) | 1 | 0 |
| B.Sca (Mieses Nf3) | 1 | 0 |
| B.Fre (Winawer Poisoned Pawn Kd1) | 1 | 0 |
| B.Nim (Kennedy d5 Nce7) | 1 | 1 |
| D.QGD.Har (parent same-FEN with kids) | 0 | 1 |
| D.Sla.Cze.Kra (Krause Main Line same-FEN) | 0 | 1 |
| B.Sic.Cls (Boleslavsky vs Be2.e5) | 0 | 1 |
| **TOTAL** | **60** | **10** |

(Some families spread across multiple rows; the counts above
group the work conceptually, not by exact subtree.)

**Audit impact**:
- duplicate_groups: 190 → 130 (−60: every DELETE collapsed its group)
- resolved_groups: 83 → 93 (+10 TT)
- unresolved_groups: 107 → **37** (−70)
- rows_in_unresolved_groups: 215 → 75 (−140)
- catalogue rows: 5,965 → 5,905 (−60)

**Target was unresolved_groups < 100; result is 37** — well below
target.

**Deferred (10 groups)**, all conceptual or "two real names" cases:

- ~~Van Geet / Van't Kruijs triple~~: **RESOLVED via mixed Option D** — `A.Van.ReN.e3.d5 ⇄ A.VtK.e5.Nc3.d5` bilateral `same_as` (rank 1) + `A.Van.ReN.e3 ⇄ A.VtK.e5.Nc3` bilateral `same_as` (rank 29 parents) + `A.Van.d5.e3.e5 → A.Van.ReN.e3.d5` `transposes_to`. Multi-target `same_as` (N=2) deliberately NOT used: structural analysis shows only 2 of the 3 are real literary canonicals; the third is a Van Geet d5-prefix breadcrumb. See [`van-geet-vant-kruijs-proposal.md`](van-geet-vant-kruijs-proposal.md).
- rank 7-9 post-batch: `B.Mod.Std.Nf3.C5S ⇄ B.Sic.HAc.d4.Bg7` (cross-family Modern/Sicilian).
- rank 8: `E.Nim.Sml.Bot ⇄ E.Nim.Sml.Kmo` (Botvinnik vs Kmoch — both literary Sämisch siblings). **ON HOLD — naming review pending**. See [`nimzo-saemisch-botvinnik-kmoch-proposal.md`](nimzo-saemisch-botvinnik-kmoch-proposal.md). User challenge raised: 365Chess and Chess.com both attribute "Kmoch Variation" to the depth-2 `4.f3` move (the slug `E.Nim.Fou` already canonically carries the "Kmoch Variation" alias at depth 2, ECO E20), not to the depth-3 Sämisch sub-line. Apply same_as only after naming review confirms both Botvinnik and Kmoch are genuine depth-3 attributions.
- ~~Larsen ↔ Reti Nimzowitsch-Larsen~~: **RESOLVED via bilateral `same_as`** — `A.Lar.Cls.MLn ⇄ A.Ret.Nim.MLn` (Nimzo-Larsen Attack A01 ⇄ Reti Nimzowitsch-Larsen A06). Cleanest `same_as` case to date: no deletes, no cascades, no schema work, ECO-distinct on both sides. Mirrors the Rubinstein/Colle-Zukertort precedent. See [`larsen-reti-nimzowitsch-proposal.md`](larsen-reti-nimzowitsch-proposal.md) for the per-row analysis.
- rank 19: `A.QPO.Nf6.Nf3.c6 ⇄ A.QPO.c6.Nf3.Nf6` (Czech-Indian path mirror).
- ~~ranks 10-12: Budapest `E.Bud.Adl.MLn ⇄ E.Bud.Rub.MLn` 3-level cascade~~ **RESOLVED via bilateral `same_as` cascade** (3 pairs: `.MLn`, `.MLn.e3`, `.MLn.e3.Be2`). Adler (4.Nf3) and Rubinstein (4.Bf4) are two real player-named move-order routes converging to the same A52 tabiya. Deepest same_as cascade in the series; no internal naming conflict (unlike Nimzo). See [`budapest-adler-rubinstein-proposal.md`](budapest-adler-rubinstein-proposal.md).
- ~~rank 20: `A.Eng.Sym.Nc3.Nf6.Nf3 ⇄ A.Eng.Sym.Nf3.Nf6.Nc3` (English Symmetrical Three Knights — both real names).~~ **RESOLVED via single_canonical** — `Nc3.Nf6.Nf3.transposes_to = Nf3.Nf6.Nc3`. Pure descriptive path mirror (no player-name dispute). Canonical chosen by subtree development: Nf3.Nf6.Nc3 hosts 5 named children including the Four Knights subtree; Nc3.Nf6.Nf3 has 1 (.e5). "Three Knights Line" alias promoted to the canonical side. See section below.
- ~~QGA Flohr ↔ Janowski-Haberditz~~: **RESOLVED via bilateral `same_as`** — `D.QGA.Flo.MLn ⇄ D.QGA.Jan.e3.b5` (Flohr Variation D20 vs Haberditz Variation literary leaf under Janowski-Larsen). Smallest possible `same_as` sprint since Larsen — single pair, no cascade, no deletes. See [`qga-flohr-janowski-proposal.md`](qga-flohr-janowski-proposal.md) for the per-row analysis.
- ~~London Classical ↔ Mason~~: **RESOLVED via bilateral `same_as`** on both paired ranks. `A.Lon.Cls.MLn ⇄ A.Lon.Msn.MLn.Nbd2` (Classical London contemporary vs Mason London historical, both A48) plus the cascading `.c4` pair. Mirror of the Italian Giuoco/Two Knights cascade. See [`london-classical-mason-proposal.md`](london-classical-mason-proposal.md) for the per-row analysis.
- rank 76: `A.PQI.e3 ⇄ A.PQI.e3.Bb7` (parent-child same-FEN, structural review needed).

All deferred cases either fit `same_as` (two real names, future
batch) or need conceptual proposals before any change.

### Post-0.2 Phase 1 cleanup batch 1

First post-tag (`ocn-1.0.2`) cleanup pass, scoped to the 9 top-9
unresolved intra-family groups that survived the OCN 0.2 release.
All HIGH-confidence single_canonical or DELETE; no schema changes,
no new `same_as` cases, no proposals required.

| rank pre-sprint | action | canonical | from | rationale |
|---|---|---|---|---|
| 1 | TT | `E.KID.Fch.Kav` | `E.KID.Fch.Kav.Nc3.e5` | "Kavalek System" (E62) literary anchor beats Nc3-path depth-5 |
| 2 | TT | `D.Sem.Mer.MLn.Old` | `D.Sem.Mer.MLn.c5.e5` | "Old Variation" (D48) literary beats generic "e5 Line" |
| 3 | TT | `E.Gru.Rus.Hng` | `E.Gru.Rus.Hng.e4` | identical `moves_uci` — parent-child redundancy, kept for breadcrumbs |
| 4 | DELETE | (none) | `A.Eng.Agi.Nc3.Nf6.e4` | leaf, 0/0 refs, self-described move-order descriptor of Mikenas-Carls; its previous kids were deleted in the prior intra-family batch |
| 5 | TT | `C.RyL.Mor.Car.MLn` | `C.RyL.Mor.Ba4.b5.Bb3` | "Caro Main Line" literary beats "Bb3 Retreat" structural |
| 6 | TT | `C.RyL.Mor.Car` | `C.RyL.Mor.Ba4.b5` | "Caro Variation" literary; .Ba4.b5 self-described as "Caro Prefix" |
| 7 | TT | `E.KID.Avk` | `E.KID.Avk.Cst.Bg5` | "Averbakh Variation" (E73) literary beats generic "Bg5 Line" |
| 8 | TT | `C.PhD.Nim` | `C.PhD.Lio.MLn.O-O` | "Nimzowitsch Variation" (C41) literary; Lion descendant has no alias |
| 9 | TT | `C.PhD.Nim.MLn` | `C.PhD.Lio.MLn.O-O.Re1` | same logic one depth deeper |

**Net change**: 8 transposes_to arrows + 1 row deletion.

**Audit impact**:
- duplicate_groups: 191 → 190 (rank 4 collapsed to size 1 after delete)
- resolved_groups: 75 → 83 (+8)
- unresolved_groups: 116 → 107 (−9)
- rows_in_unresolved_groups: 233 → 215 (−18)
- multiple_canonical_groups: 6 (unchanged)

All 9 listed groups exited the unresolved set. The new top of the
ranked default is the Van Geet / Van't Kruijs triple (deferred
case) followed by score-5 long-tail intra-family residuals — the
target zone for the next Phase 1 batch.

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
