# QID Miles/Petrosian — structural review proposal

**Status**: PROPOSED (investigation only — **no catalogue change
in this commit**). One of the two deliberate research holds left
after the transposition cleanup phase closed (`fe66649`); see
[`transposition-cleanup-closure.md`](transposition-cleanup-closure.md).

**Headline**: this is **not** a co-canonical (`same_as`) case. It
is a **mislabelled-slug + broken-parent-chain defect**:
`E.QID.Mil.MLn` is the Kasparov-Petrosian main line wearing the
"Miles" name, carrying an 11-node theory subtree under the wrong
family root, while the correctly-named `E.QID.Pet.KPe` sits empty.
The fix is a **slug migration** (re-home the subtree under
`E.QID.Pet.KPe`), the first slug-rename in OCN — so it needs
downstream coordination and its own GO, not a quick relation edit.

## The two openings (they are different)

- **Miles Variation** = `4.Bf4` — `E.QID.Mil`, moves end `c1f4`,
  FEN has the bishop on f4 (`…2PP1B2…`). A real but minor QID
  sideline.
- **Petrosian / Kasparov-Petrosian** = `4.a3` (then `…Bb7 5.Nc3`)
  — `E.QID.Pet` → `E.QID.Pet.KPe`. The mainstream a3 system.

These are distinct 4th moves reaching distinct positions. They do
**not** transpose at move 4.

## The defect (verified)

```
E.QID.Mil          "Miles Variation"   4.Bf4   moves: …g1f3 b7b6 c1f4         depth 2, 1 child
└── E.QID.Mil.MLn  "Miles … Main Line"         moves: …g1f3 b7b6 a2a3 c8b7 b1c3   ← BROKEN parent
                                                 (no c1f4 — does NOT extend its parent E.QID.Mil)
    FEN rn1qkb1r/pbpp1ppp/1p2pn2/8/2PP4/P1N2N2/1P2PPPP/R1BQKB1R b KQkq -

E.QID.Pet          "Petrosian"         4.a3    moves: …g1f3 b7b6 a2a3          depth 2, 5 children
└── E.QID.Pet.KPe  "Kasparov-Petrosian"        moves: …g1f3 b7b6 a2a3 c8b7 b1c3   ← parent OK, but LEAF (0 children)
    FEN rn1qkb1r/pbpp1ppp/1p2pn2/8/2PP4/P1N2N2/1P2PPPP/R1BQKB1R b KQkq -   ← IDENTICAL to E.QID.Mil.MLn
```

`E.QID.Mil.MLn` and `E.QID.Pet.KPe` have the **identical move list**
(`d2d4 g8f6 c2c4 e7e6 g1f3 b7b6 a2a3 c8b7 b1c3`) and the **identical
FEN**. They are the same line. But:

- `E.QID.Mil.MLn` (broken parent — claims descent from Miles 4.Bf4,
  but its moves are the a3/Nc3 line) **carries the whole theory subtree**.
- `E.QID.Pet.KPe` (correctly named and parented) is an **empty leaf**.

## The mislabelled subtree (11 nodes under the wrong root)

`E.QID.Mil.MLn` + 10 descendants — every one with the a3/Nc3
Kasparov-Petrosian move order, all rooted (wrongly) under "Miles":

```
E.QID.Mil.MLn                       (= E.QID.Pet.KPe position)
├── E.QID.Mil.MLn.Be7               "Be7 Line"
└── E.QID.Mil.MLn.d5                "d5 Line"
    └── E.QID.Mil.MLn.d5.cxd5       "cxd5 Line"           (7 children)
        ├── …Nxd5                   "Nxd5 Recapture"
        ├── …exd5                   "exd5 Recapture"
        ├── …Qc2                    "Kasparov Attack"     ← named after Kasparov, under "Miles"
        ├── …e3                     "Petrosian Attack"    ← named after Petrosian, under "Miles"
        ├── …Qa4                    "Rashkovsky Attack"
        ├── …e4                     "Polovodin Gambit"
        └── …Bd2                    "Romanishin Attack"
```

The smoking gun: the catalogue has the **"Kasparov Attack"** and
**"Petrosian Attack"** (and the Polovodin/Rashkovsky/Romanishin
attacks) sitting under the **Miles** branch. These are
Kasparov-Petrosian theory, not Miles theory. The naming is internally
self-contradictory.

## Migration safety (verified)

- The 12-slug Miles subtree (`E.QID.Mil` + `Mil.MLn` + 10
  descendants) has **zero inbound references from outside** (no
  external `parent_ocn1`, `transposes_to`, or `same_as` points
  into it).
- `E.QID.Pet.KPe` is an **empty leaf with 0 inbound references**.
- No other QID FEN collisions exist (the audit flags only the one
  `Mil.MLn ⇄ KPe` group). The 10 descendants do not collide with
  any existing `E.QID.Pet.*` slug.

So a migration that re-homes the `Mil.MLn` subtree under
`E.QID.Pet.KPe` is **self-contained** — nothing outside the subtree
needs touching, and the target slug is free.

## Options

### Option A — Re-slug the subtree under `E.QID.Pet.KPe` (RECOMMENDED)

Move the 11-node `Mil.MLn` subtree to live under the correctly-named
`E.QID.Pet.KPe`:

- **Delete** `E.QID.Mil.MLn` (it is a duplicate of `E.QID.Pet.KPe`;
  the correctly-named KPe survives).
- **Re-slug** its 10 descendants `E.QID.Mil.MLn.* → E.QID.Pet.KPe.*`
  (moves unchanged; only slug + `parent_ocn1` change), fixing every
  parent chain.
- `E.QID.Mil` (real 4.Bf4 Miles) keeps its identity and becomes a
  childless depth-2 leaf (it has no catalogued 4.Bf4 sub-theory —
  which is accurate; the Miles is a minor sideline).

- **Pro**: removes BOTH defects at once — the naming lie ("Kasparov
  Attack" no longer under "Miles") and the broken parent chain.
- **Pro**: the Kasparov-Petrosian theory ends up under the
  correctly-named, correctly-parented `E.QID.Pet.KPe`.
- **Pro**: self-contained (no external refs), target slug free.
- **Con**: this is the **first slug-rename in OCN**. All prior
  cleanup was add-relation or delete-leaf; never a rename. Slug
  renames change `canonical_ocn1` downstream — needs coordination
  with `chess-parquet` and a deliberate apply (not folded into a
  routine batch).

### Option B — Repair `parent_ocn1` only (keep slug)

Set `E.QID.Mil.MLn.parent_ocn1 = E.QID.Pet` (its moves DO extend
`E.QID.Pet`'s `4.a3`, so the chain would no longer be broken).

- **Con**: leaves the slug literally `E.QID.Mil.MLn` with parent
  `E.QID.Pet` — a slug-path/parent **mismatch** (OCN slugs mirror
  the parent chain). And it keeps the "Miles" naming lie on the
  whole subtree. A half-fix that trades one inconsistency for
  another.

### Option C — `same_as` bilateral (`Mil.MLn ⇄ KPe`)

- **Con**: freezes the broken parent chain and the naming lie,
  declaring a mislabelled slug co-canonical. Explicitly the wrong
  tool here (the closure doc flagged this — don't `same_as` over a
  structural defect).

### Option D — Relabel `canonical_name` only

Rename `E.QID.Mil.MLn`'s `canonical_name` to "Kasparov-Petrosian …"
and delete/redirect the empty KPe.

- **Con**: the **slug** still says `.Mil.MLn` and the parent chain
  is still broken. Fixes the display name but not the structure.
  Half-fix.

## Recommendation: **Option A** (slug migration), as a separate GO'd apply

Option A is the only fully-correct fix. But because it is OCN's first
slug-rename and changes `canonical_ocn1` for 11 slugs downstream,
**do not fold it into a routine apply**. The recommended path:

1. Confirm `chess-parquet` can absorb a slug rename (its
   `canonical_ocn1` materialisation) — or accept that the
   `openings.parquet` regenerates with the new slugs.
2. Apply the migration in a dedicated commit (see plan below) with
   explicit GO.
3. Since slugs are renamed (not just relations added), consider
   whether this warrants an OCN minor-version note (it changes the
   identity of 11 catalogue rows, though no FEN/position changes).

## Migration plan (when approved — NOT in this commit)

| step | action |
|---|---|
| 1 | Delete `E.QID.Mil.MLn` (duplicate of `E.QID.Pet.KPe`). |
| 2 | Re-slug `E.QID.Mil.MLn.Be7 → E.QID.Pet.KPe.Be7` (parent → `E.QID.Pet.KPe`). |
| 3 | Re-slug `E.QID.Mil.MLn.d5 → E.QID.Pet.KPe.d5` (parent → `E.QID.Pet.KPe`). |
| 4 | Re-slug `E.QID.Mil.MLn.d5.cxd5 → E.QID.Pet.KPe.d5.cxd5` (parent → `E.QID.Pet.KPe.d5`). |
| 5 | Re-slug the 7 `…d5.cxd5.{Nxd5,exd5,Qc2,e3,Qa4,e4,Bd2} → E.QID.Pet.KPe.d5.cxd5.*` (parent → `E.QID.Pet.KPe.d5.cxd5`). |
| 6 | Leave `E.QID.Pet.KPe`'s own name/alias as-is (already correct: "Kasparov-Petrosian Variation"); it now has children. |
| 7 | `E.QID.Mil` keeps its 4.Bf4 identity, now a childless leaf. |

Moves are unchanged on every re-slugged row — only `ocn1` and
`parent_ocn1` change. No FEN/position changes anywhere.

## Expected impact (of applying Option A)

| metric | now | after A | Δ |
|---|---|---|---|
| catalogue rows | 5,900 | 5,899 | −1 (`Mil.MLn` deleted; KPe absorbs the subtree) |
| unresolved_groups | 2 | **1** | −1 (only Nimzo Bot/Kmo would remain) |
| resolved_groups | 123 | 123 | 0 (the group collapses, not "resolves") |
| duplicate_groups | 125 | 124 | −1 |
| slugs renamed (downstream `canonical_ocn1` churn) | — | 10 | first slug-rename in OCN |

After Option A, the **only** unresolved group in the whole catalogue
would be the ON-HOLD Nimzo Bot/Kmo naming review.

## Risks and open questions

1. **First slug-rename in OCN** — every prior change added relations
   or deleted leaves. Renames change row identity for downstream
   consumers (`chess-parquet` `canonical_ocn1`). Must be coordinated,
   not routine.
2. **Does the real Miles (4.Bf4) deserve sub-theory?** After
   migration `E.QID.Mil` is a leaf. That is accurate today (no
   catalogued 4.Bf4 lines), but a future editor may add genuine
   4.Bf4 continuations — that is independent of this fix.
3. **Version semantics** — 11 rows change `ocn1`; no positions
   change. Decide whether this is a patch or a minor bump in the
   downstream contract.

## Recommended next step

Treat this as **reviewed and ready**, but apply only in a dedicated,
GO'd, downstream-coordinated commit — not folded into other work.
This proposal commit changes nothing in `catalog/ocn-1.csv`.
