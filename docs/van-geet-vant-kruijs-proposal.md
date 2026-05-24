# Van Geet ↔ Van't Kruijs — arbitration proposal

**Status**: draft proposal — NOT yet applied to `catalog/ocn-1.csv`.
**Companion**: builds on `spec/OCN-1.md` → "Canonicalisation
arbitration", the `same_as` policy section, and the precedents from
the 4 prior `same_as` applications (Rubinstein/Colle-Zukertort,
Italian Giuoco/Two Knights, Larsen/Reti Nimzowitsch-Larsen, London
Classical/Mason).

## Context

The Van triple at rank 1 was the case earmarked for testing
**`same_as` multi-target** (N=2 pipe-separated targets,
e.g. `same_as = "slugA|slugB"`). The schema supports it; no case
to date has needed it. This proposal evaluates whether the Van
triple genuinely requires multi-target — or whether structural
analysis points to a different resolution.

**Spoiler**: the structural analysis points to a **mixed
resolution** (Option D below): two co-canonical slugs via
bilateral `same_as` (N=1) + one structural breadcrumb via
`transposes_to`. The multi-target feature remains untested by
this case. That's not a problem — features wait for genuinely
matching cases, not artificially-fitted ones.

This proposal also addresses **rank 29** (the parents of the
rank-1 slugs), which is a second related FEN group that resolves
with bilateral `same_as`.

## FEN groups in scope (2 groups)

| rank | size | classes | slugs |
|---|---|---|---|
| 1  | 3 | A | `A.Van.ReN.e3.d5`, `A.Van.d5.e3.e5`, `A.VtK.e5.Nc3.d5` |
| 29 | 2 | A | `A.Van.ReN.e3`, `A.VtK.e5.Nc3` (parents of the rank-1 slugs after 3 plies each) |

## Subtree shape

```
A.Van                                    "Dunst Opening" / Van Geet (1.Nc3)
├── A.Van.ReN                            "Reversed Nimzowitsch"   ← literary sub-name
│   └── A.Van.ReN.e3                     "e3 Line"                ← rank 29 twin
│       └── A.Van.ReN.e3.d5              "d5 Line"                ← rank 1 twin
│           ├── A.Van.ReN.e3.d5.Be6      "Hulsemann Gambit"       (named child)
│           └── A.Van.ReN.e3.d5.Nf6      "Liebig Gambit"          (named child)
├── A.Van.d5                             "d5 Line"  ← STRUCTURAL prefix (just "d5 Line" alias)
│   └── A.Van.d5.e3                      "e3 Line"
│       └── A.Van.d5.e3.e5               "e5 Line"                ← rank 1 third member
│           └── A.Van.d5.e3.e5.d4        "d4 Line"
│               └── A.Van.d5.e3.e5.d4.Bb4  "Sleipnir Gambit"     (named leaf)
├── A.Van.ReS                            "Reversed Scandinavian"
├── A.Van.Tub                            "Tubingen Gambit"
├── A.Van.{b5, c5, d5, d6, f5, g6}       Black response sub-tree
└── …

A.VtK                                    Van't Kruijs Opening (1.e3)
├── A.VtK.FrD                            "French Transposition"
├── A.VtK.Sic                            "Sicilian Transposition"
└── A.VtK.e5                             "e5 Line"
    ├── A.VtK.e5.Bc4                     "Bouncing Bishop Prefix"
    └── A.VtK.e5.Nc3                     "Keoni-Hiva Prefix"      ← rank 29 twin
        ├── A.VtK.e5.Nc3.Nc6             "Alua Variation"         ← Hawaiian naming tradition
        ├── A.VtK.e5.Nc3.Nf6             "Akahi Variation"
        └── A.VtK.e5.Nc3.d5              "Ekolu Variation"        ← rank 1 twin
            └── A.VtK.e5.Nc3.d5.f4       "f4 Line"
```

Two completely separate opening families that converge at one FEN
via three different move-order paths (and at a sibling FEN one
move earlier via two paths).

## Conceptual analysis — are all three slugs equivalent?

**No.** Two of the three carry literary identity, one is a
structural breadcrumb.

| slug | parent | parent alias | literary identity? |
|---|---|---|---|
| `A.Van.ReN.e3.d5` | `A.Van.ReN.e3` | "e3 Line" | **YES** — anchored in `A.Van.ReN` ("Reversed Nimzowitsch"), with named gambit children (Hulsemann, Liebig). |
| `A.VtK.e5.Nc3.d5` | `A.VtK.e5.Nc3` | "Keoni-Hiva Prefix" | **YES** — own alias "Ekolu Variation", part of the named Hawaiian-tradition sub-family (Alua / Akahi / Ekolu) under Keoni-Hiva. |
| `A.Van.d5.e3.e5` | `A.Van.d5` | **"d5 Line"** (pure structural prefix) | **NO** — the parent itself is a structural prefix (just "d5 Line"), and the slug's own note is "...e5 after e3 in the Van Geet d5 line" — describes a move-order, not a named opening. |

The third slug exists as a structural waypoint inside the
`A.Van.d5` sub-tree (which exists because Black plays …d5 first
against Van Geet's 1.Nc3 — a different Black move-order than the
Reversed Nimzowitsch where Black plays …e5 first). Its own
children continue into named territory (`.d4.Bb4` is the Sleipnir
Gambit), but the slug itself is a breadcrumb, not a named line.

Compare with the four prior `same_as` cases:

| case | all sides literary? |
|---|---|
| Rubinstein ⇄ Colle-Zukertort | yes, both |
| Italian Giuoco ⇄ Two Knights | yes, both |
| Larsen ⇄ Reti Nimzowitsch-Larsen | yes, both |
| London Classical ⇄ Mason | yes, both |
| **Van triple** | **two yes, one no (structural)** |

This is the first triple in the audit where the structural
analysis splits the slugs into two literary + one descriptor.
Option D (mixed) below reflects this honestly.

## Options considered

### Option A — `same_as` multi-target (all 3 co-canonical)

```
A.Van.ReN.e3.d5.same_as  = A.Van.d5.e3.e5|A.VtK.e5.Nc3.d5
A.Van.d5.e3.e5.same_as   = A.Van.ReN.e3.d5|A.VtK.e5.Nc3.d5
A.VtK.e5.Nc3.d5.same_as  = A.Van.ReN.e3.d5|A.Van.d5.e3.e5
```

- **Pro**: validates the N=2 pipe-separated `same_as` feature.
- **Con**: treats `A.Van.d5.e3.e5` as canonical when its parent
  is a structural prefix and its own notes describe a move-order
  rather than a named line. Inflates the literary claim.
- **Decision**: **discarded**. The schema feature is correct;
  this case is the wrong test bed. Wait for a real 3-literary
  case (none in current top 100).

### Option B — Single canonical `A.Van` (e.g. ReN.e3.d5)

`A.Van.d5.e3.e5.transposes_to = A.Van.ReN.e3.d5`
`A.VtK.e5.Nc3.d5.transposes_to = A.Van.ReN.e3.d5`

- **Pro**: simple single canonical.
- **Con**: erases the Keoni-Hiva / Ekolu Variation literary
  identity. Van't Kruijs is a distinct opening family with its
  own named sub-tradition; making it transpose to Van Geet
  collapses the distinction.

### Option C — Single canonical `A.VtK.e5.Nc3.d5`

- **Pro**: keeps Van't Kruijs naming alive.
- **Con**: symmetric problem. Erases the Reversed Nimzowitsch
  literary anchor.

### Option D — Mixed: 2 co-canonical + 1 breadcrumb (RECOMMENDED)

```
A.Van.ReN.e3.d5.same_as       = A.VtK.e5.Nc3.d5    # bilateral
A.VtK.e5.Nc3.d5.same_as       = A.Van.ReN.e3.d5    # bilateral
A.Van.d5.e3.e5.transposes_to  = A.Van.ReN.e3.d5    # structural TT to closer Van canonical
```

- **Pro**: honest about which slugs have literary identity and
  which is a structural breadcrumb. Preserves both real names.
- **Pro**: matches the structural analysis — same approach as
  Modern Benoni Classical (where 3 slugs converged but only 1
  had literary identity, resulting in single_canonical with 2
  TT pointers).
- **Pro**: TT direction is principled — A.Van.d5.e3.e5 starts
  with 1.Nc3 (same as A.Van.ReN.e3.d5) so the closer cousin in
  move-order tree is the right canonical to point at.
- **Con**: doesn't exercise the `same_as` N=2 multi-target
  feature. Acceptable: features wait for genuinely matching
  cases.

### Option E — Defer

- **Con**: structural analysis is clear; no reason to wait.

## Recommendation: **Option D** plus same_as on rank 29 (parents)

### Per-slug actions

**Rank 1 — Van triple (FEN after 4 plies)**

| slug | action | rationale | rule |
|---|---|---|---|
| `A.Van.ReN.e3.d5` | **PRESERVE (canonical)**, add `same_as = A.VtK.e5.Nc3.d5` | Reversed Nimzowitsch d5, anchored in literary A.Van.ReN family with named gambit children. | Rule 4 |
| `A.VtK.e5.Nc3.d5` | **PRESERVE (canonical)**, add `same_as = A.Van.ReN.e3.d5` | Ekolu Variation of Keoni-Hiva, anchored in literary A.VtK Hawaiian-tradition sub-family. | Rule 4 |
| `A.Van.d5.e3.e5` | **TT → `A.Van.ReN.e3.d5`** | Structural breadcrumb under A.Van.d5 ("d5 Line" prefix); notes self-describe as move-order step. Both rows start with 1.Nc3 so TT to closer Van canonical. Keeps its subtree (`.d4 → .Sleipnir`) alive. | Rule 1 + Rule 5 |

**Rank 29 — Parents (FEN after 3 plies)**

| slug | action | rationale | rule |
|---|---|---|---|
| `A.Van.ReN.e3` | **PRESERVE (canonical)**, add `same_as = A.VtK.e5.Nc3` | Reversed Nimzowitsch e3 prefix, parent of the rank-1 d5 slug. Anchored in literary A.Van.ReN. | Rule 4 |
| `A.VtK.e5.Nc3` | **PRESERVE (canonical)**, add `same_as = A.Van.ReN.e3` | Keoni-Hiva Prefix — explicitly named sub-family (parent of Alua/Akahi/Ekolu Variations). | Rule 4 |

Same cascading bilateral `same_as` pattern as London Classical/Mason
and Italian Giuoco/Two Knights. The third slug at rank 1
(A.Van.d5.e3.e5) doesn't have a parent twin at rank 29 because
its 3-ply parent (A.Van.d5.e3) doesn't share a FEN with anything
— the rank-29 group is a 2-slug Van.ReN.e3 ⇄ VtK.e5.Nc3 only.

### Notes to add (cross-references)

- `A.Van.ReN.e3.d5.notes`: `...d5 against the e3 Reversed
  Nimzowitsch. Co-canonical with A.VtK.e5.Nc3.d5 (Van't Kruijs
  Keoni-Hiva Ekolu Variation, A00) — same FEN via the 1.e3 Van't
  Kruijs move order.`
- `A.VtK.e5.Nc3.d5.notes`: `...d5 in the Keoni-Hiva Gambit
  (Ekolu Variation). Co-canonical with A.Van.ReN.e3.d5 (Van Geet
  Reversed Nimzowitsch d5, A00) — same FEN via the 1.Nc3 Van
  Geet move order.`
- `A.Van.d5.e3.e5.notes`: `Move-order transposition to A.Van.ReN.e3.d5:
  same FEN reached via the Van Geet d5-first move order
  (1.Nc3 d5 2.e3 e5).`
- `A.Van.ReN.e3.notes`: `e3 in the Van Geet Reversed Nimzowitsch.
  Co-canonical with A.VtK.e5.Nc3 (Van't Kruijs Keoni-Hiva Prefix,
  A00) — same FEN via the 1.e3 Van't Kruijs move order.`
- `A.VtK.e5.Nc3.notes`: `Nc3 after ...e5 in Van't Kruijs Opening
  (Keoni-Hiva Prefix). Co-canonical with A.Van.ReN.e3 (Van Geet
  Reversed Nimzowitsch e3 prefix, A00) — same FEN via the 1.Nc3
  Van Geet move order.`

No alias changes.

## Summary

**Preserve (no canonicality change)**: 4 slugs (the 2 co-canonical
pairs at rank 1 and rank 29).

**`same_as` (4 declarations, 2 bilateral pairs)**:

| slug | same_as |
|---|---|
| `A.Van.ReN.e3.d5` | `A.VtK.e5.Nc3.d5` |
| `A.VtK.e5.Nc3.d5` | `A.Van.ReN.e3.d5` |
| `A.Van.ReN.e3` | `A.VtK.e5.Nc3` |
| `A.VtK.e5.Nc3` | `A.Van.ReN.e3` |

**`transposes_to` (1 arrow)**:

| from | → | to |
|---|---|---|
| `A.Van.d5.e3.e5` | → | `A.Van.ReN.e3.d5` |

**Deletions**: 0. **Reparenting**: 0.

## Expected audit metric impact

|                            | before | after | Δ |
|----------------------------|---|---|---|
| rows totals catàleg        | 5,905 | 5,905 | 0 |
| duplicate_groups           | 130 | 130 | 0 |
| resolved_groups            | 96 | **98** | **+2** |
| multiple_canonical_groups  | 9 | **11** | **+2** |
| unresolved_groups          | 34 | **32** | **−2** |
| rows_in_unresolved_groups  | 69 | **64** | **−5** |

Rank 1 (3-row group: 2 canonicals + 1 TT pointer →
`multiple_canonical`). Rank 29 (2-row group: 2 canonicals via
`same_as` → `multiple_canonical`).

## Risks and open questions

1. **`same_as` multi-target (N=2 pipe) remains untested.** The
   schema supports it; no current case genuinely requires it.
   This is the right outcome: features wait for cases, not the
   other way around. If a future audit surfaces a true 3-literary
   convergence (three independent opening names on one FEN),
   that's when multi-target gets exercised.

2. **TT direction for `A.Van.d5.e3.e5`**: chose
   `A.Van.ReN.e3.d5` (closer Van-family cousin) over
   `A.VtK.e5.Nc3.d5`. Both target slugs would work
   (FEN-equivalent), but pointing within the same family root
   (A.Van) preserves a cleaner navigation breadcrumb. If you
   prefer pointing across to the Van't Kruijs side, change the
   one line.

3. **Rank 29 included with rank 1**: scope-creep risk if you
   wanted only the Van triple. Defensible because rank 29 is the
   direct parent of the rank-1 slugs and resolves with the
   identical conceptual argument (Reversed Nimzowitsch vs
   Keoni-Hiva as two real named sub-families). Resolving both in
   one commit avoids leaving the parent pair as documented-noise
   in the audit while the child is resolved. If you'd rather
   ship them separately, the proposal can split into two commits.

4. **Hawaiian naming tradition** (Keoni-Hiva / Alua / Akahi /
   Ekolu) is unusual but real — it's how OCN's source data
   labelled the A.VtK.e5.Nc3 sub-family. Treating these as
   genuine literary names is consistent with how OCN treats
   other player-attribution names (Larsen, Reti, Sleipnir,
   Hulsemann, etc.).

## Recommended apply order

When approved (single commit):

1. Set 4 `same_as` declarations (2 bilateral pairs at ranks 1 + 29).
2. Set 1 `transposes_to` arrow (A.Van.d5.e3.e5 → A.Van.ReN.e3.d5).
3. Add cross-reference notes on all 5 touched rows.
4. Update `docs/transpositions.md`:
   - Move Van triple from "Deferred" to the `same_as`-resolved
     table (with note about Option D structural mixing).
   - Bump multi-canonical count from 9 to 11.
5. Mark this proposal `Status: APPLIED`.

Validation suite: standard. Expected commit shape: 5 catalogue
rows touched (10 / 10 line diff with notes), short doc updates,
no row count change.
