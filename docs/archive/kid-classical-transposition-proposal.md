# KID Classical Old/e5 — arbitration proposal

**Status**: **APPLIED** — see `docs/transpositions.md` → "KID
Classical Old/e5 (resolved, mixed multiple + single canonical)" for
the per-row outcomes. Sets the precedent that `multiple_canonical`
requires at least one in-group pointer to be computable today.

**Companion**: builds on the rules in `spec/OCN-1.md` →
"Canonicalisation arbitration" and the precedent set by the Veresov
/ French resolution (`docs/veresov-french-proposal.md`).

## Context

After the Veresov / French resolution, the new top-1 group in the
audit is an intra-E triple inside the King's Indian Defence
Classical family:

```
E.KID.Cls.Old.e5
E.KID.Cls.e5.O-O.Nbd7
E.KID.Cls.e5.O-O.Nbd7.O-O
```

All three reach the same FEN
`r1bq1rk1/pppn1pbp/3p1np1/4p3/2PPP3/2N2N2/PP2BPPP/R1BQ1RK1 w - -`,
the canonical Classical KID tabiya after `…e5`, `…O-O`, `…Nbd7`
and `O-O` in some order. Unlike the Veresov / French case, **all
three sit within the same E.KID.Cls subtree** — they are not three
different opening traditions, they are three move-order paths
within one. But two of them carry distinct, literature-anchored
names (`E91 Old Main Line` and `E95 Castled with Nbd7`) while the
third is a Lichess-imported descriptor (`E94 Positional Defence`
via the OID move order).

This proposal resolves rank 1 plus its two cascading children
(rank 15, rank 16) and explains why the recommendation is
**multiple canonical at rank 1, 15, 16, plus one targeted leaf
deletion**.

## FEN groups in scope (3 groups)

| rank | size | classes | slugs | depths |
|---|---|---|---|---|
| 1   | 3 | E | `E.KID.Cls.Old.e5`, `E.KID.Cls.e5.O-O.Nbd7`, `E.KID.Cls.e5.O-O.Nbd7.O-O` | 4 / 5 / 6 |
| 15  | 2 | E | `E.KID.Cls.Old.e5.c6`, `E.KID.Cls.e5.O-O.Nbd7.c6` | 5 / 6 |
| 16  | 2 | E | `E.KID.Cls.Old.e5.Re1`, `E.KID.Cls.e5.O-O.Nbd7.Re1` | 5 / 6 |

## Subtree shape

```
E.KID.Cls
├── E.KID.Cls.Old            "Old Main Line"  (literary anchor)
│   └── E.KID.Cls.Old.e5     "Old Main Line, e5"  E91
│       ├── d5     unique line, no FEN mirror
│       ├── Re1    same FEN as e5.O-O.Nbd7.Re1
│       └── c6     same FEN as e5.O-O.Nbd7.c6
│
└── E.KID.Cls.e5             "e5 Prefix"  (structural waypoint)
    └── E.KID.Cls.e5.O-O     "Castled"
        ├── E.KID.Cls.e5.O-O.c6      "Donner"  (different position)
        ├── E.KID.Cls.e5.O-O.Na6     "Glek"    (different position)
        └── E.KID.Cls.e5.O-O.Nbd7    "Castled, Nbd7"  E95
            ├── Re1    same FEN as Old.e5.Re1
            ├── c6     same FEN as Old.e5.c6
            └── O-O    "Positional Defence" E94  (OID move-order)
```

`E.KID.Cls.Old.e5` (depth 4, 3 kids, E91) and
`E.KID.Cls.e5.O-O.Nbd7` (depth 5, 3 kids, E95) are **literary
mirror subtrees** — two named descriptions of the same tabiya
reached by different move orders. The third path
(`e5.O-O.Nbd7.O-O`, depth 6, 0 kids, E94, "Positional Defence" via
the Old-Indian move order) is a Lichess-imported descriptor
*re-stating* the same position from a third move order.

## Why this is different from Veresov / French

In Veresov / French, three slugs came from three different opening
traditions (`B.Fre`, `A.Ver`, `D.QPG.Ver`) on three different
move-order trees. Here, both literary slugs are inside the same
`E.KID.Cls` subtree. The case is closer to a single family with
two parallel naming conventions than to a true cross-family
transposition.

Still, the names matter:
- `E.KID.Cls.Old.e5` is on the **literary** `Old Main Line` branch
  (ECO E91). The "Old Main Line" name is a real chess term for the
  historical mainline of KID Classical.
- `E.KID.Cls.e5.O-O.Nbd7` is on the **structural** `e5 Prefix`
  branch (ECO E95). The parent `E.KID.Cls.e5` is explicitly named
  "e5 Prefix" (the spec already treats Prefix as a structural
  waypoint, not a literary identity).

ECO assigns different codes (E91 vs E95 vs E94) to the same
position because of the move order, exactly the kind of distortion
OCN's hierarchy is meant to clarify — by recording both names but
acknowledging they reach the same FEN.

## Options considered

**Option A — single canonical (TT cascade)**
Pick `E.KID.Cls.e5.O-O.Nbd7` as canonical; `E.KID.Cls.Old.e5` →
TT; `E.KID.Cls.e5.O-O.Nbd7.O-O` → DELETE; rank 15 / 16 mirrors
also TT into the e5.O-O.Nbd7 subtree.

- **Pro**: cleanest catalogue; matches the single-canonical pattern
  used for most resolved cases so far.
- **Con**: forcibly demotes "Old Main Line, e5" to a move-order
  alias. Loses the E91 literary identity as a canonical anchor.
  The `Old Main Line` family at depth 3 stays alive but its primary
  branch (`Old.e5`) becomes a redirect.

**Option B — multiple canonical (recursive)**
Preserve both `E.KID.Cls.Old.e5` and `E.KID.Cls.e5.O-O.Nbd7` as
canonicals at rank 1. Same for rank 15 and rank 16 mirror pairs.
DELETE the third-path descriptor `E.KID.Cls.e5.O-O.Nbd7.O-O`.

- **Pro**: preserves both literary anchors. Consistent with the
  Veresov / French precedent for two-real-names cases. Lets a
  reader navigating from `E.KID.Cls.Old` find the canonical Old
  Main Line, AND a reader navigating from `E.KID.Cls.e5` find the
  canonical Castled Nbd7.
- **Con**: adds 3 multiple_canonical groups (rank 1, 15, 16) to
  the audit. Catalogue size unchanged; just more groups
  classified `multiple_canonical` rather than collapsed.

**Option C — delete descriptor only (no TT, no canonical change)**
DELETE `E.KID.Cls.e5.O-O.Nbd7.O-O` and leave everything else
unresolved.

- **Pro**: minimal touch.
- **Con**: leaves rank 1 unresolved as a pair (still in the top
  default report), and ranks 15 / 16 still unresolved. Solves
  nothing structurally.

## Recommendation: Option B — multiple canonical, with descriptor deletion

The `Old Main Line` is a strong enough literary identity that
forcing it into a `transposes_to` arrow toward the more structural
`Castled Nbd7` slug would mis-represent the catalogue's purpose.
The opening literature consistently distinguishes:

- `…e5` followed by `…Nbd7` (the historical Old Main Line, E91).
- `…Nbd7` followed by `…e5` (the modern Castled-then-Nbd7
  arrangement, E95).

OCN's job is to record that both names point at the same FEN
without claiming one is "an alias of" the other. The Veresov /
French precedent applies: two canonicals coexist, only the
documented move-order pointer carries `transposes_to`.

### Per-slug actions

**Rank 1 — 3-way intra-E**

| slug | action | rationale | rule |
|---|---|---|---|
| `E.KID.Cls.Old.e5` | **PRESERVE (canonical)** | E91 Old Main Line, e5 — primary literary identity on the `Old Main Line` branch. Has 3 children (d5, Re1, c6). | Rule 4 (two real names) |
| `E.KID.Cls.e5.O-O.Nbd7` | **PRESERVE (canonical)** | E95 Castled with Nbd7 — primary structural identity on the `e5 Prefix` branch. Has 3 children (Re1, c6, O-O). | Rule 4 |
| `E.KID.Cls.e5.O-O.Nbd7.O-O` | **DELETE** | E94 "Positional Defence" via the OID move order. Leaf (0 kids), 0 inbound refs. Its notes explicitly identify it as an OID-move-order descriptor of the same tabiya. The "Positional Defence" label is a Lichess-imported third-path descriptor; the chess content is preserved by the two canonicals above. | Rule 1 (descriptor) + Rule 3 (leaf, no identity gain) |

**Rank 15 — c6 children**

| slug | action | rationale | rule |
|---|---|---|---|
| `E.KID.Cls.Old.e5.c6` | **PRESERVE (canonical)** | E96 c6 line in Old Main Line. Leaf in literature anchor. | Rule 4 (parent decision cascades) |
| `E.KID.Cls.e5.O-O.Nbd7.c6` | **PRESERVE (canonical)** | E96 c6 line in Castled Nbd7. Leaf in structural anchor. | Rule 4 |

Both leaves; both kept as paired multiple canonicals.

**Rank 16 — Re1 children**

| slug | action | rationale | rule |
|---|---|---|---|
| `E.KID.Cls.Old.e5.Re1` | **PRESERVE (canonical)** | E95 Re1 line in Old Main Line. Leaf. | Rule 4 |
| `E.KID.Cls.e5.O-O.Nbd7.Re1` | **PRESERVE (canonical)** | E95 Re1 line in Castled Nbd7. Leaf. | Rule 4 |

Same shape as rank 15.

### Audit impact

After applying:

- `duplicate_groups`: unchanged (3 groups stay as duplicate FEN
  groups by definition).
- `resolved_groups`: **+3** (all three become resolved).
- `multiple_canonical_groups`: **+3** (1, 15, 16 all become
  multiple_canonical).
- `unresolved_groups`: **−3**.
- `rows_in_unresolved_groups`: **−7** (the 7 rows currently sitting
  in these 3 unresolved groups move to resolved).
- 1 physical row deletion (`E.KID.Cls.e5.O-O.Nbd7.O-O`).

### Cross-references to add

To make the multiple-canonical relationship readable from each
side, add notes:

- `E.KID.Cls.Old.e5.notes`:
  `Also reached as E.KID.Cls.e5.O-O.Nbd7 (Castled with Nbd7, E95).
  Both canonicals preserved per arbitration rule 4.`
- `E.KID.Cls.e5.O-O.Nbd7.notes`:
  `Also reached as E.KID.Cls.Old.e5 (Old Main Line, E91). Both
  canonicals preserved per arbitration rule 4.`
- `E.KID.Cls.Old.e5.c6.notes` and the e5.O-O.Nbd7.c6 mirror: same
  pattern.
- `E.KID.Cls.Old.e5.Re1.notes` and the e5.O-O.Nbd7.Re1 mirror:
  same pattern.

No alias changes proposed (the existing aliases on these slugs
already describe the line; adding a "move-order" alias here would
not aid lookup the way it does for clear A→E or D→A breadcrumb
cases).

## Risks and open questions

1. **Triple multiple-canonical inside a single family**. This will
   be the first case where multiple_canonical applies to slugs in
   the **same parent class**, not across classes. The audit logic
   handles it correctly (no change needed), but the conceptual
   precedent is worth noting in the spec. **Recommendation**: add
   a short example to `spec/OCN-1.md` → arbitration rule 4 once
   applied, showing both Veresov/French (cross-class) and KID
   Old/e5 (intra-class) cases.

2. **Cascading multiple-canonical to children.** If the parent
   pair coexists, do all paired children coexist by default? Not
   automatically — only when the children themselves have
   substantive identity beyond restating the parent's relation.
   In this case ranks 15 and 16 pair real ECO-coded lines (E96
   c6, E95 Re1), so yes. If a future case has only one of the
   pair carrying real identity, single canonical there is
   appropriate.

3. **`E.KID.Cls.Old.e5.d5`** has no mirror in the e5.O-O.Nbd7
   subtree. It stays as-is (unique line). No action needed.

4. **`E.KID.Cls.Old` parent (depth 3)** is not in any audit group.
   It remains canonical for the broader "Old Main Line" family.
   Its children other than `.e5` are unaffected.

5. **Should the OID-move-order "Positional Defence" slug be kept
   alive as a navigation breadcrumb instead of deleted?** Looking
   at the established pattern: similar OID-move-order descriptors
   were deleted in the Modern/OID→KID sprint when they were leaf
   mirrors. Same pattern here. DELETE is consistent. If the
   user prefers to keep a Lichess-named "Positional Defence" label
   alive, change to TT → `E.KID.Cls.e5.O-O.Nbd7`. Either is
   defensible; deletion is the established default.

## Recommended apply order

When you approve:

1. Apply 1 deletion + 4–6 note touches in one
   "Resolve KID Classical Old e5 transpositions" commit. No
   `transposes_to` writes needed because the three groups become
   multiple_canonical via the existing canonical structure
   (`E.KID.Cls.e5.O-O.Nbd7.O-O` is deleted; the remaining 6
   slugs in 3 paired canonical groups carry no `transposes_to`).

   **Caveat**: with no TT writes, the audit will treat ranks 1,
   15, 16 as `unresolved` (no pointers → no declaration). To
   produce the multiple_canonical resolution, **at least one
   non-canonical pointer must exist per group**. Two options:

   a. Add a placeholder `transposes_to` from one mirror to the
      other (e.g. `E.KID.Cls.e5.O-O.Nbd7.O-O` is being deleted, so
      it can't carry one; but
      `E.KID.Cls.e5.O-O.Nbd7 → E.KID.Cls.Old.e5` or vice versa
      would resolve rank 1, contradicting the "both canonical"
      claim).

   b. Extend the `_resolution_kind()` semantics: a group with **no
      pointers but two canonicals that explicitly cross-reference
      each other in notes** counts as `multiple_canonical`. This
      requires either a new column or a notes-keyword convention.

   **Open question for the user**: how should we represent
   "multiple canonicals coexist by design, with NO row marked as
   non-canonical"? The Veresov / French case had a clear
   non-canonical (`D.QPG.Ver.MLn.Be7` → `A.Ver.Cls.MLn.Be7`) that
   declared the equivalence. Here, after deleting the OID
   descriptor, there is no third-party pointer left. Rank 1 would
   stay `unresolved` in the audit despite being conceptually
   resolved.

   **My recommendation**: introduce a lightweight `same_as`
   pseudo-relation via `notes` keyword `Same FEN as <slug>:`
   that the audit's `_resolution_kind()` can scan. This avoids
   schema growth. Or alternatively, in this specific group keep
   the OID descriptor alive with TT to one of the canonicals
   (not delete it), so the group has a declared pointer. The
   second option is simpler and keeps a Lichess-named "Positional
   Defence" entry navigable. **I lean toward keeping it alive with
   TT**, not deleting.

## Revised recommendation (after open question 5)

To avoid the "no pointer → no declaration" problem:

| slug | revised action |
|---|---|
| `E.KID.Cls.Old.e5` | **PRESERVE (canonical)** |
| `E.KID.Cls.e5.O-O.Nbd7` | **PRESERVE (canonical)** |
| `E.KID.Cls.e5.O-O.Nbd7.O-O` | **TT → `E.KID.Cls.e5.O-O.Nbd7`** (keep "Positional Defence" navigable) |
| `E.KID.Cls.Old.e5.c6` | **PRESERVE (canonical)** |
| `E.KID.Cls.e5.O-O.Nbd7.c6` | **PRESERVE (canonical)** |
| `E.KID.Cls.Old.e5.Re1` | **PRESERVE (canonical)** |
| `E.KID.Cls.e5.O-O.Nbd7.Re1` | **PRESERVE (canonical)** |

But this still leaves rank 15 and rank 16 with **zero pointers**
because both children are paired canonicals with no descriptor to
TT. They stay `unresolved` per the current audit logic.

**Decision needed**: do we

- (i) live with rank 15 and 16 staying `unresolved` (cosmetic, but
  visible in the report), OR

- (ii) accept Option A for ranks 15 and 16 (pick one side as
  canonical, TT the other) while keeping Option B at rank 1, OR

- (iii) extend the audit to recognise "intentional multiple
  canonical without pointer" via a notes convention.

**Plain recommendation**: option (ii) — multiple canonical only
where it adds informational value (rank 1, where E91 vs E95
literary distinction matters). For the leaf-level children
(rank 15, rank 16) the pair is structurally redundant and the
spirit of OCN's "classify by position" tips toward TT (single
canonical). This produces a cleaner audit and keeps the
multiple_canonical primitive reserved for cases where literature
genuinely distinguishes the names at the same FEN.

### Final per-slug plan (option ii)

| slug | action | target | rule |
|---|---|---|---|
| `E.KID.Cls.Old.e5` | PRESERVE (canonical) | — | 4 |
| `E.KID.Cls.e5.O-O.Nbd7` | PRESERVE (canonical) | — | 4 |
| `E.KID.Cls.e5.O-O.Nbd7.O-O` | TT | `E.KID.Cls.e5.O-O.Nbd7` | 1 + 5 |
| `E.KID.Cls.Old.e5.c6` | PRESERVE (canonical, leaf) | — | 5 |
| `E.KID.Cls.e5.O-O.Nbd7.c6` | TT | `E.KID.Cls.Old.e5.c6` | 5 |
| `E.KID.Cls.Old.e5.Re1` | PRESERVE (canonical, leaf) | — | 5 |
| `E.KID.Cls.e5.O-O.Nbd7.Re1` | TT | `E.KID.Cls.Old.e5.Re1` | 5 |

At rank 15 and 16 the Old.e5 side wins because it is anchored on
the `Old Main Line` literary family. At rank 1 both sides survive
because their parent identities at depth 3–5 carry independent
literary weight (E91 vs E95). Rank 1 becomes multiple_canonical
with `e5.O-O.Nbd7.O-O` as the in-group pointer. Rank 15 and 16
become single_canonical.

## Summary of recommended apply

**Preserve (no change)**: 4 slugs — `E.KID.Cls.Old.e5`,
`E.KID.Cls.e5.O-O.Nbd7`, `E.KID.Cls.Old.e5.c6`,
`E.KID.Cls.Old.e5.Re1`.

**TT (3 arrows)**:

| from | → | to |
|---|---|---|
| `E.KID.Cls.e5.O-O.Nbd7.O-O` | → | `E.KID.Cls.e5.O-O.Nbd7` |
| `E.KID.Cls.e5.O-O.Nbd7.c6` | → | `E.KID.Cls.Old.e5.c6` |
| `E.KID.Cls.e5.O-O.Nbd7.Re1` | → | `E.KID.Cls.Old.e5.Re1` |

**Deletions**: 0.

**Notes**: extend the rank-1 canonicals' notes to cross-reference
each other (Old.e5 ↔ e5.O-O.Nbd7) so the multiple_canonical
relationship is visible to a human reader.

**Expected audit metric impact**:
- `duplicate_groups`: 192 → 192 (unchanged).
- `resolved_groups`: 66 → 69 (+3).
- `multiple_canonical_groups`: 1 → 2 (+1, rank 1).
- `unresolved_groups`: 126 → 123 (−3).
- `rows_in_unresolved_groups`: 255 → 248 (−7).

No catalogue rows added or removed. 3 `transposes_to` writes and
2–4 cross-reference notes.
