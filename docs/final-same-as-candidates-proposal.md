# Final same_as candidates — arbitration proposal

**Status**: PROPOSED (not applied). Covers the 3 candidates the
unresolved map flagged as `SAME_AS_CANDIDATE`. **Key finding: only
2 of the 3 are clean `same_as`; the QID Miles/Petrosian pair is
actually a structural mis-parenting defect and is recommended for
DEFER, not same_as.**

**Companion**: `spec/OCN-1.md` → "Canonicalisation arbitration",
the 8 prior `same_as` applications, and
[`unresolved-map-20.md`](unresolved-map-20.md).

---

## Candidate 1 — QID Miles ⇄ Kasparov-Petrosian — **DEFER**

### Context

Map classified `E.QID.Mil.MLn ⇄ E.QID.Pet.KPe` (E12, rank 3) as a
`SAME_AS_CANDIDATE` ("Miles vs Kasparov-Petrosian, both real player
names"). Closer inspection shows this is **not** a co-canonical
naming case but a **mis-parenting defect**.

### FEN group

Both reach `rn1qkb1r/pbpp1ppp/1p2pn2/8/2PP4/P1N2N2/1P2PPPP/R1BQKB1R b KQkq -`
(`1.d4 Nf6 2.c4 e6 3.Nf3 b6 4.a3 Bb7 5.Nc3`).

### The defect

```
E.QID.Mil          "QID, Miles Variation"   moves: …Nf3 b6 4.Bf4      (the real Miles = 4.Bf4)
└── E.QID.Mil.MLn  "Miles … Main Line"      moves: …Nf3 b6 4.a3 Bb7 5.Nc3   ← BROKEN: does NOT contain Bf4
    └── (10 descendants: …d5, cxd5, Kasparov Attack, Petrosian Attack,
         Polovodin Gambit, Rashkovsky/Romanishin Attack, …)        ← all the a3/Nc3 theory tree

E.QID.Pet          "QID, Petrosian"         moves: …Nf3 b6 4.a3
└── E.QID.Pet.KPe  "Kasparov-Petrosian"     moves: …Nf3 b6 4.a3 Bb7 5.Nc3   ← correctly parented, but a LEAF (0 descendants)
```

`E.QID.Mil.MLn`'s move list (`…a3 Bb7 Nc3`) does **not** extend its
parent `E.QID.Mil` (`…Bf4`). The entire Kasparov-Petrosian
main-line theory (10 nodes) hangs under the **mislabelled** "Miles"
branch, while the correctly-named `E.QID.Pet.KPe` is an empty leaf.

### Why not same_as

A bilateral `same_as` would declare "Miles Main Line ⇄
Kasparov-Petrosian" as two equal literary names for this FEN. But
`E.QID.Mil.MLn` is not really "Miles" at all — it's the
Kasparov-Petrosian line wearing the wrong label (its parent is the
unrelated 4.Bf4 Miles). Baking a `same_as` here would freeze the
mislabel into the contract (the Nimzo lesson: don't `same_as` over
a naming defect).

### Options

- **A same_as** — ✗ freezes the mislabel.
- **B/C single_canonical** — ✗ premature; doesn't fix the broken parent.
- **D Defer** — ✓ **RECOMMENDED**. Needs its own structural proposal: either reparent the `E.QID.Mil.MLn` subtree under `E.QID.Pet` (it IS the a3 Petrosian line), relabel it, or collapse it against `E.QID.Pet.KPe`. This is a reparenting/relabelling decision, larger than a same_as, and the first to involve a broken parent chain.

### Recommendation: **DEFER** — open a separate "QID Miles/Petrosian structural review" sprint.

| slug | name | has_children | proposed_action | rationale | rule |
|---|---|---|---|---|---|
| `E.QID.Mil.MLn` | Miles Main Line (mislabelled) | yes (10 desc) | **DEFER** | moves are the a3/Nc3 Petrosian line, not Miles 4.Bf4; broken parent chain | structural review |
| `E.QID.Pet.KPe` | Kasparov-Petrosian | no (leaf) | **DEFER** | correctly named/parented but empty; the theory tree is under the wrong branch | structural review |

---

## Candidate 2 — KID Fianchetto Simagin ⇄ Uhlmann-Szabo — **same_as**

### Context

`E.KID.Fch.Sim ⇄ E.KID.Fch.Uhl` (E62, rank 4). Two named move-order
routes into the same Fianchetto KID `...Nc6/...e5` tabiya.

### FEN group

Both reach `r1bq1rk1/ppp2pbp/2np1np1/4p3/2PP4/2N2NP1/PP2PPBP/R1BQ1RK1 w - -`:

- **Simagin**: `…Nc3 Bg7 Nf3 O-O g3 d6 Bg2 Nc6 O-O e5` (Nc3 first).
- **Uhlmann-Szabo**: `…Nf3 Bg7 g3 O-O Bg2 d6 O-O Nc6 Nc3 e5` (Nf3 first, Nc3 last).

Same position, different white development order. (`E.KID.Fch.Uhl`'s
move list does not prefix-extend its parent `E.KID.Fch` only because
the parent's representative line is Nc3-first — a benign move-order
artefact, not a defect like candidate 1.)

### Subtree shape

```
E.KID.Fch  "KID, Fianchetto"
├── E.KID.Fch.Sim  "Simagin System"        ← twin (Nc3-first)
│   └── E.KID.Fch.Sim.MLn  → transposes_to E.KID.Fch.Pan (Panno)   (…a6 continuation)
│       └── (Blockade, Donner)
├── E.KID.Fch.Uhl  "Uhlmann-Szabo System"  ← twin (Nf3-first)
│   └── E.KID.Fch.Uhl.MLn   (d5 continuation, leaf)
└── E.KID.Fch.Pan  "Panno"   (Sim.MLn already transposes here)
```

Both twins are real named systems (Simagin; Uhlmann + Szabó). Their
children diverge (`Sim.MLn` → ...a6/Panno; `Uhl.MLn` → d5), so the
`same_as` is only at the parent twin level — no cascade.

### Options

- **A same_as bilateral** — ✓ **RECOMMENDED**. Two real names, same FEN, symmetric depth (both depth 3, 1 child each).
- **B/C single_canonical** — ✗ would erase one real system name.
- **D defer** — ✗ no ambiguity; both names are genuine.

### Recommendation: **A (same_as bilateral)**

```
E.KID.Fch.Sim.same_as = E.KID.Fch.Uhl
E.KID.Fch.Uhl.same_as = E.KID.Fch.Sim
```

| slug | name | has_children | proposed_action | rationale | rule |
|---|---|---|---|---|---|
| `E.KID.Fch.Sim` | Simagin System | yes (1) | PRESERVE, `same_as = E.KID.Fch.Uhl` | real system, Nc3-first route | Rule 4 |
| `E.KID.Fch.Uhl` | Uhlmann-Szabo System | yes (1) | PRESERVE, `same_as = E.KID.Fch.Sim` | real system, Nf3-first route | Rule 4 |

Notes: cross-reference each other; mention the shared `...Nc6/...e5`
tabiya. No alias changes. **Risk/open question**: the family also has
`E.KID.Fch.Pan` (Panno), and `Sim.MLn` already transposes to it — so
"Simagin", "Uhlmann-Szabo" and "Panno" are three names in this
neighbourhood. The proposed same_as only links the two depth-3 twins
that share *this* FEN; Panno is a deeper/adjacent node and is left as
is. Confidence: medium-high.

---

## Candidate 3 — Scandinavian Gipslis ⇄ Portuguese Classical — **same_as (lean) / single_canonical (alt)**

### Context

`B.Sca.Nf6.Mar.Gip ⇄ B.Sca.Por.Cls.MLn` (B01, rank 5). Two routes
into the same `2...Nf6` Scandinavian with `...Nxd5` and `...Bg4`.

### FEN group

Both reach `rn1qkb1r/ppp1pppp/8/3n4/3P2b1/5N2/PPP2PPP/RNBQKB1R w KQkq -`:

- **Gipslis** (under Marshall): `…exd5 Nf6 d4 Nxd5 Nf3 Bg4` (Nxd5 then Bg4).
- **Portuguese Classical**: `…exd5 Nf6 d4 Bg4 Nf3 Nxd5` (Bg4 then Nxd5).

### Subtree shape

```
B.Sca.Nf6.Mar  "Marshall Variation"
└── B.Sca.Nf6.Mar.Gip  "Gipslis Variation"   ← twin; LEAF, no ECO, note "Lichess maps this line to B01"
B.Sca.Por  "Portuguese Variation"
└── B.Sca.Por.Cls  "The Classical"
    └── B.Sca.Por.Cls.MLn  ← twin; B01, has child .Be2
```

### Options

- **A same_as bilateral** — Gipslis (Aivars Gipslis) is a real attribution; Portuguese Classical is the established ...Bg4 Scandinavian name. Preserves both.
- **C single_canonical** (`B.Sca.Nf6.Mar.Gip.transposes_to = B.Sca.Por.Cls.MLn`) — Gipslis is a **leaf with no ECO** and an explicit "Lichess maps…" note (smells like a Lichess-derived label), while Portuguese Classical carries B01 and the subtree. Arguably Gipslis transposes into the Portuguese home.
- **D defer** — only if we can't decide whether Gipslis is independent.

### Recommendation: **A (same_as bilateral)**, with **C as the honest fallback**

Lean A because Gipslis is a genuine player name and the two reach the
same FEN by symmetric move-order swaps. But this is the **weakest of
the three** — if the editor judges "Gipslis" to be a Lichess
descriptor rather than an independent literary identity, **C
(single_canonical, TT Gip → Por.Cls.MLn)** is the cleaner call and
should be used instead.

| slug | name | has_children | proposed_action | rationale | rule |
|---|---|---|---|---|---|
| `B.Sca.Nf6.Mar.Gip` | Gipslis Variation | no (leaf) | PRESERVE + `same_as` **or** `transposes_to` Por.Cls.MLn | player name, but leaf / no ECO / Lichess-derived note | Rule 4 (A) or canonicalisation (C) |
| `B.Sca.Por.Cls.MLn` | Portuguese Classical Main Line | yes (1) | PRESERVE (canonical either way) | established ...Bg4 name, B01, has subtree | Rule 4 |

**Risk/open question**: is "Gipslis Variation" an independent
literary name or a Lichess import? The "Lichess maps this line to
B01" note leans toward import. Confidence: medium.

---

## Summary

| candidate | recommendation | same_as | TT | delete | defer |
|---|---|---|---|---|---|
| QID Miles/Petrosian | **DEFER** (structural mis-parenting) | 0 | 0 | 0 | yes |
| KID Simagin/Uhlmann | **same_as bilateral** | 2 | 0 | 0 | no |
| Scandinavian Gipslis/Portuguese | **same_as bilateral** (or single_canonical TT) | 2 (or 0) | 0 (or 1) | 0 | no |

**If approved as recommended (KID + Scand same_as, QID deferred)**:
4 `same_as` declarations (2 pairs), 0 TT, 0 deletes. Expected:
unresolved 6 → 4, multiple_canonical 15 → 17.

If the editor prefers single_canonical for Scandinavian: 2 same_as
(KID) + 1 TT (Scand), unresolved 6 → 4, multiple_canonical 15 → 16.

QID stays unresolved pending its own structural review (alongside
the ON-HOLD Nimzo) — leaving 2 conceptual residuals after this
sprint: QID (structural) and the cross-family pairs [1 Modern/Sicilian,
14 Amar/Hungarian] plus Nimzo ON HOLD.

## Recommended apply order (when approved)

1. KID: add 2 `same_as` (Sim ⇄ Uhl) + cross-ref notes.
2. Scandinavian: per editor's call — either 2 `same_as`
   (Gip ⇄ Por.Cls.MLn) or 1 `transposes_to` (Gip → Por.Cls.MLn).
3. QID: **no change** — log the structural defect for a separate sprint.
4. Update `docs/transpositions.md` (same_as-resolved table + counts).
5. Mark this proposal APPLIED (noting QID still deferred).

Validation suite: standard. No catalogue rows added/removed (same_as
+ optional 1 TT only).
