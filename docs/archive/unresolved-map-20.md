# Unresolved transposition map — 20 remaining groups

**Snapshot**: `origin/main` at `f06e242`. Audit summary:
`duplicate_groups=127 resolved_groups=107 unresolved_groups=20
multiple_canonical_groups=15 rows_in_unresolved_groups=40
top_group_size=2`.

**Purpose**: classify every remaining unresolved group before
touching the catalogue again, so the next sprints attack in the
right order and conceptual cases are separated from mechanical
ones. **No catalogue changes in this document.**

All 20 groups are size-2 (one FEN, two slugs). None is mixed-class
beyond the cross-family cases flagged below.

## Category legend

| category | meaning |
|---|---|
| `ON_HOLD_NAMING_REVIEW` | blocked on external naming evidence (catalogue self-conflict) |
| `CROSS_FAMILY_CONCEPTUAL` | two different opening families converge; needs a proposal to pick treatment |
| `SAME_AS_CANDIDATE` | two real player/variation names at one FEN → bilateral `same_as` after a short proposal |
| `SINGLE_CANONICAL_MIRROR` | pure move-order mirror, no naming dispute → `transposes_to` (pick the developed side) |
| `LONG_TAIL_MECHANICAL` | descriptor/move-name duplicate of a sibling/parent → `transposes_to` or `delete` |

## Per-group analysis

### [1] B.Mod.Std.Nf3.C5S ⇄ B.Sic.HAc.d4.Bg7 — rank 1, score 5
- FEN `rnbqk1nr/pp1pppbp/6p1/2p5/3PP3/5N2/PPP2PPP/RNBQKB1R w` — `1.e4 g6 2.d4 Bg7 3.Nf3 c5` (Modern) vs `1.e4 c5 2.Nf3 g6 3.d4 Bg7` (Sicilian Hyper-Accelerated).
- classes B/B, ECO B06 / B27. kids: C5S=2, Bg7=1. TT/SA empty.
- **Category**: `CROSS_FAMILY_CONCEPTUAL`. Modern Defence vs Sicilian — two legitimate family framings of the same position. Both have subtrees.
- **recommended_action**: `proposal_needed` (likely `same_as` — both framings are real, B06 vs B27 distinct). `confidence: medium`. `external: no`.
- **next_step**: "Propose Modern/Sicilian Hyper-Accelerated cross-family arbitration (B06 ⇄ B27)."

### [2] E.Nim.Sml.Bot ⇄ E.Nim.Sml.Kmo — rank 2, score 5
- FEN Sämisch doubled-pawn tabiya. ECO E24|E25 / E26. kids: Bot=3, Kmo=1.
- **Category**: `ON_HOLD_NAMING_REVIEW`. Catalogue self-conflict: `E.Nim.Fou` (4.f3) already carries the "Kmoch Variation" alias at depth 2.
- **recommended_action**: `naming_review`. `confidence: low` (blocked). `external: YES` (Lichess opening DB, ECO, Wikipedia for the Kmoch/Botvinnik depth attribution).
- **next_step**: "Run Nimzo Sämisch naming review against authoritative sources; produce nimzo-naming-review.md."

### [3] A.QPO.Nf6.Nf3.c6 ⇄ A.QPO.c6.Nf3.Nf6 — rank 3, score 5
- FEN `1.d4 Nf6 2.Nf3 c6` vs `1.d4 c6 2.Nf3 Nf6`. ECO A46 / A40. kids: Nf6.Nf3.c6=0, c6.Nf3.Nf6=1.
- **Category**: `SINGLE_CANONICAL_MIRROR`. Pure descriptive path mirror (no player name). The ECO split (A46 vs A40) is purely a move-order artifact.
- **recommended_action**: `transposes_to`. Direction needs a quick subtree check — `c6.Nf3.Nf6` has the child, but `Nf6.Nf3.c6` is the more natural Indian (Nf6-first) move order. Verify at apply time. `confidence: medium`. `external: no`.
- **next_step**: "Resolve Czech-Indian QPO mirror via transposes_to (decide Nf6-first vs c6-first canonical)."

### [4] B.Fre.Win.Adv.MLn.Nf3 ⇄ B.Fre.Win.Adv.MLn.Ne7.Nf3 — rank 4, score 4
- French Winawer Advance. ECO C19 / C19. kids: .Nf3=2, .Ne7.Nf3=0.
- **Category**: `SINGLE_CANONICAL_MIRROR`. Move-order mirror (`...Nf3` direct vs via `...Ne7`). The leaf `.Ne7.Nf3` (0 kids) → developed `.Nf3` (2 kids).
- **recommended_action**: `transposes_to` (`.Ne7.Nf3 → .Nf3`). `confidence: high`. `external: no`.
- **next_step**: "TT B.Fre.Win.Adv.MLn.Ne7.Nf3 → .Nf3 (leaf mirror into developed sibling)."

### [5] B.Sic.Naj.Sch.MLn ⇄ B.Sic.Naj.Sch.O-O — rank 5, score 4
- Najdorf Scheveningen. ECO B92|B93 / B90. kids: .MLn=0, .O-O=3.
- **Category**: `SINGLE_CANONICAL_MIRROR`. `.O-O` (3 kids, describes the castling that reaches the FEN) is the developed side; `.MLn` (0 kids, generic) demotes.
- **recommended_action**: `transposes_to` (`.MLn → .O-O`). `confidence: medium` (the generic "Main Line" name sits on the demoted side; subtree wins). `external: no`.
- **next_step**: "TT B.Sic.Naj.Sch.MLn → .O-O (developed castling node canonical)."

### [6] B.Fre.Nrm.d5.Nc3.a6.Nf3 ⇄ B.Fre.Nrm.d5.Nc3.a6.Nfd7 — rank 6, score 4
- French Steinitz a6. **Identical 10-ply move list** in both slugs (`…g1f3 g8f6 e4e5 f6d7`); the two slugs name different moves of the same line (White's Nf3 vs Black's ...Nfd7). ECO C11|C14 / C11. kids: both 0.
- **Category**: `LONG_TAIL_MECHANICAL`. True naming duplicate (same line, two names).
- **recommended_action**: `delete` or `transposes_to` the redundant one. `.Nfd7` names the defining final move; `.Nf3` is the lesser. `confidence: high`. `external: no`.
- **next_step**: "Collapse French Steinitz a6 Nf3/Nfd7 duplicate (keep .Nfd7, TT/delete .Nf3)."

### [7] A.Ret.Ang.g3.Nf6.Bg2 ⇄ A.Eng.CKa.Nf3.d5.g3.Bg2 — rank 7, score 4
- Cross-family: Reti Anglo-Slav vs English Caro-Kann, same g3/Bg2 FEN. No ECO either side. kids: Ret=3, Eng.CKa=0.
- **Category**: `SINGLE_CANONICAL_MIRROR` (cross-family, but no naming dispute — both are descriptive move-order labels).
- **recommended_action**: `transposes_to` (`A.Eng.CKa.Nf3.d5.g3.Bg2 → A.Ret.Ang.g3.Nf6.Bg2`, the developed side with 3 kids). `confidence: medium-high`. `external: no`.
- **next_step**: "TT English Caro-Kann g3 Bg2 leaf → Reti Anglo-Slav g3 Nf6 Bg2 (developed side)."

### [8] B.Ale.Nrm.Dpn.d6.Nb6 ⇄ B.Ale.Nrm.Dpn.d6.c4.Nb6 — rank 8, score 4
- Alekhine Defence. ECO B03 / B03. kids: .d6.Nb6=2, .d6.c4.Nb6=0.
- **Category**: `SINGLE_CANONICAL_MIRROR` (deeper-path duplicate). `.d6.c4.Nb6` (leaf, explicit c4 in path) → `.d6.Nb6` (2 kids).
- **recommended_action**: `transposes_to` (`.d6.c4.Nb6 → .d6.Nb6`). `confidence: high`. `external: no`.
- **next_step**: "TT B.Ale.Nrm.Dpn.d6.c4.Nb6 → .d6.Nb6 (developed sibling)."

### [9] C.KGm.Acc.Bsh.MLn ⇄ C.KGm.Acc.Bsh.Nf6.Nc3 — rank 9, score 4
- King's Gambit Bishop's Gambit. ECO C33 / C33. kids: .MLn=1, .Nf6.Nc3=2. `.Nf6.Nc3` carries "Bogoljubow Prefix".
- **Category**: `LONG_TAIL_MECHANICAL` (both have small subtrees; needs a direction check). The `.Nf6.Nc3` (2 kids + Bogoljubow name) is the stronger canonical.
- **recommended_action**: `transposes_to` (`.MLn → .Nf6.Nc3`), pending confirmation both subtrees are FEN-distinct. `confidence: medium`. `external: no`.
- **next_step**: "Resolve KGm Bishop's Gambit MLn/Nf6.Nc3 (verify subtrees, TT the generic .MLn)."

### [10] E.QID.Mil.MLn ⇄ E.QID.Pet.KPe — rank 10, score 3
- QID. ECO E12 / E12. kids: Mil.MLn=2, Pet.KPe=0. **Miles** (Tony Miles) and **Petrosian/Kasparov-Petrosian** are both real player-named QID systems converging on the a3/Nc3 tabiya.
- **Category**: `SAME_AS_CANDIDATE`. Two genuine literary names, both E12.
- **recommended_action**: `proposal_needed` → bilateral `same_as`. `confidence: high`. `external: no`.
- **next_step**: "Propose QID Miles ⇄ Kasparov-Petrosian same_as (both E12 player names)."

### [11] E.KID.Fch.Sim ⇄ E.KID.Fch.Uhl — rank 11, score 2
- KID Fianchetto. ECO E62 / E62. kids: 1 each. **Simagin** and **Uhlmann-Szabo** — two player-named systems, symmetric depth.
- **Category**: `SAME_AS_CANDIDATE`. Cleanest same_as shape (symmetric, both 1 kid).
- **recommended_action**: `proposal_needed` → bilateral `same_as`. `confidence: medium-high`. `external: no`.
- **next_step**: "Propose KID Fianchetto Simagin ⇄ Uhlmann-Szabo same_as (both E62)."

### [12] B.Sca.Nf6.Mar.Gip ⇄ B.Sca.Por.Cls.MLn — rank 12, score 2
- Scandinavian. ECO (Gip empty) / B01. kids: Gip=0, Por.Cls.MLn=1. Marshall/**Gipslis** vs **Portuguese** Classical.
- **Category**: `SAME_AS_CANDIDATE` (tentative — verify both names are independent literary identities, not one a descriptor).
- **recommended_action**: `proposal_needed`. `confidence: medium` (lean same_as; confirm Gipslis vs Portuguese both real). `external: no` (structural; Gipslis and Portuguese are both documented Scandinavian names).
- **next_step**: "Inspect Scandinavian Gipslis ⇄ Portuguese Classical; propose same_as if both literary."

### [13] D.Sem.Bg5.Acc ⇄ D.Sem.Bg5.dxc4 — rank 13, score 2
- Semi-Slav Bg5. ECO D44 / (dxc4 empty). kids: Acc=0, dxc4=1. "Accepted" and "dxc4" name the **same move** (...dxc4 accepts).
- **Category**: `LONG_TAIL_MECHANICAL`. Descriptor duplicate.
- **recommended_action**: `transposes_to` (`.Acc → .dxc4`, the side with the subtree) or delete `.Acc`. `confidence: high`. `external: no`.
- **next_step**: "Collapse Semi-Slav Bg5 Acc/dxc4 (TT .Acc → .dxc4)."

### [14] A.Ama.Par ⇄ A.Hng.Par — rank 14, score 2
- Cross-family: Amar Opening (1.Nh3) vs Hungarian Opening (1.g3), both reaching the **Paris Gambit** FEN. ECO A00 / A00. kids: Ama=2, Hng=1.
- **Category**: `CROSS_FAMILY_CONCEPTUAL`. Shared "Paris Gambit" name via two offbeat first moves. Like Van Geet/Van't Kruijs.
- **recommended_action**: `proposal_needed` (same_as or single_canonical). `confidence: medium`. `external: no`.
- **next_step**: "Propose Amar ⇄ Hungarian Paris Gambit cross-family arbitration (both A00)."

### [15] C.KGm.Acc.Muz.Dbl.MLn ⇄ C.KGm.Acc.Muz.MLn.Qxf3 — rank 15, score 2
- King's Gambit Muzio. ECO C37 / C37. kids: Dbl.MLn=1, MLn.Qxf3=4. Paired with [20] (Muzio Dbl vs MLn at two depths).
- **Category**: `LONG_TAIL_MECHANICAL` (with a Double-Muzio naming nuance). `.MLn.Qxf3` (4 kids) is the developed Muzio node.
- **recommended_action**: `transposes_to` (`.Dbl.MLn → .MLn.Qxf3`), resolved together with [20]. `confidence: medium` (confirm Double Muzio isn't a distinct gambit at this exact FEN). `external: no`.
- **next_step**: "Resolve Muzio Double/Main Line pair [15]+[20] together (TT Dbl into the developed Muzio MLn)."

### [16] B.CaK.Adv.Tal.MLn ⇄ B.CaK.Adv.Tal.h5 — rank 16, score 1
- Caro-Kann Advance Tal. ECO B12 / B12. kids: .MLn=0, .h5=1. "Main Line" vs "h5" (the move reaching the FEN).
- **Category**: `LONG_TAIL_MECHANICAL`.
- **recommended_action**: `transposes_to` (`.MLn → .h5`). `confidence: high`. `external: no`.
- **next_step**: "TT B.CaK.Adv.Tal.MLn → .h5."

### [17] B.CaK.Adv.Sht.MLn ⇄ B.CaK.Adv.Sht.O-O — rank 17, score 1
- Caro-Kann Advance Short. ECO B12 / B12. kids: 1 each.
- **Category**: `LONG_TAIL_MECHANICAL` (symmetric; pick canonical by which child is more standard).
- **recommended_action**: `transposes_to` (direction TBD at apply — likely `.MLn → .O-O` since O-O names the move reaching the FEN). `confidence: medium`. `external: no`.
- **next_step**: "Resolve CaK Advance Short MLn/O-O (TT, decide direction)."

### [18] B.Fre.Win.Psn.MLn.Ne2 ⇄ B.Fre.Win.Psn.MLn.Qxg7 — rank 18, score 1
- French Winawer Poisoned Pawn. ECO C18 / C18. kids: both 0. Two move-names in the same forcing sequence reaching one FEN.
- **Category**: `LONG_TAIL_MECHANICAL`.
- **recommended_action**: `transposes_to` or `delete` the redundant move-name. `confidence: medium` (verify which is the conventional node name). `external: no`.
- **next_step**: "Collapse Winawer Poisoned Pawn Ne2/Qxg7 duplicate."

### [19] B.Sic.Sch.Krs.MLn ⇄ B.Sic.Sch.Krs.h6 — rank 19, score 1
- Sicilian Scheveningen Keres Attack. ECO B81 / B81. kids: .MLn=0, .h6=1.
- **Category**: `LONG_TAIL_MECHANICAL`.
- **recommended_action**: `transposes_to` (`.MLn → .h6`). `confidence: high`. `external: no`.
- **next_step**: "TT B.Sic.Sch.Krs.MLn → .h6."

### [20] C.KGm.Acc.Muz.Dbl ⇄ C.KGm.Acc.Muz.MLn — rank 20, score 1
- King's Gambit Muzio. ECO C37 / C37. kids: Dbl=1, MLn=6. Paired with [15].
- **Category**: `LONG_TAIL_MECHANICAL`. `.MLn` (6 kids) is the canonical Muzio.
- **recommended_action**: `transposes_to` (`.Dbl → .MLn`), with [15]. `confidence: medium`. `external: no`.
- **next_step**: "Resolve Muzio Double/Main Line pair [15]+[20] together."

## Classification summary

| category | count | groups |
|---|---:|---|
| `ON_HOLD_NAMING_REVIEW` | 1 | [2] |
| `CROSS_FAMILY_CONCEPTUAL` | 2 | [1], [14] |
| `SAME_AS_CANDIDATE` | 3 | [10], [11], [12] |
| `SINGLE_CANONICAL_MIRROR` | 5 | [3], [4], [5], [7], [8] |
| `LONG_TAIL_MECHANICAL` | 9 | [6], [9], [13], [15], [16], [17], [18], [19], [20] |
| **total** | **20** | |

### By recommended action

| action | count | groups |
|---|---:|---|
| `transposes_to` / `delete` (mechanical) | 14 | [3][4][5][6][7][8][9][13][15][16][17][18][19][20] |
| `proposal_needed` → same_as / arbitration | 5 | [1][10][11][12][14] |
| `naming_review` (external) | 1 | [2] |

### By confidence

- **high**: [4][6][8][13][16][19] (clean mechanical TT/delete) + [10] (same_as).
- **medium / medium-high**: [3][5][7][9][11][12][15][17][18][20] + [1][14] (proposals).
- **low / blocked**: [2].

## Groups requiring external bibliography

**Only [2]** (Nimzo Sämisch Bot/Kmo) needs authoritative sources
(Lichess opening DB, ECO, Wikipedia) because the catalogue
internally disagrees about where "Kmoch" lives. All other 19
groups are resolvable from chess-structural reasoning + the
existing catalogue (no external lookup).

## Top 5 recommended next actions (in order)

1. **Mechanical batch — LONG_TAIL + SINGLE_CANONICAL** (14 groups,
   one sprint): all `transposes_to`/`delete`, high/medium
   confidence, no proposals. Would take unresolved **20 → ~6** in a
   single commit. The biggest, safest reduction. Resolve the Muzio
   pair [15]+[20] together and the Czech-Indian [3] direction with
   a subtree check.
2. **QID Miles ⇄ Kasparov-Petrosian same_as** [10]: cleanest
   `same_as` candidate (two famous player names, both E12,
   high confidence). Short proposal then apply.
3. **KID Fianchetto Simagin ⇄ Uhlmann-Szabo same_as** [11]:
   symmetric same_as, mirrors Budapest/Larsen. Short proposal.
4. **Cross-family proposals** [1] Modern/Sicilian + [14]
   Amar/Hungarian: two conceptual arbitrations (same_as vs
   single_canonical). One proposal each.
5. **Nimzo naming review** [2]: the only externally-blocked case.
   Run when there's appetite for a bibliography pass; produces
   `nimzo-naming-review.md` and then either renames, same_as, or
   keeps ON HOLD.

After steps 1-4, the only remaining unresolved group would be the
ON-HOLD Nimzo [2] — i.e. the catalogue would be fully resolved
modulo one consciously-deferred naming question.

## Notes

- This map is a **snapshot at `f06e242`**; ranks shift as groups
  resolve. Re-run `audit_transpositions.py --ranked` before each
  sprint.
- Direction decisions marked "TBD at apply" ([3], [5], [17], [18])
  need a 1-minute subtree/standard-move-order check at apply time;
  they are not blockers, just not pre-decided here.
- No `same_as` multi-target (N=2) case appears among the 20; all
  are bilateral or single-canonical.
