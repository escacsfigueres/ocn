# London Classical ↔ Mason — arbitration proposal

**Status**: **APPLIED via bilateral `same_as` on both paired ranks**.
See `docs/transpositions.md` → "`same_as`-resolved groups" for the
applied outcome. Mirror of the Italian Giuoco/Two Knights cascade
precedent. Brings `multiple_canonical_groups` to 9.
**Companion**: builds on `spec/OCN-1.md` → "Canonicalisation
arbitration" and the precedents from
[Rubinstein/Colle-Zukertort](rubinstein-colle-zukertort-proposal.md),
[Italian Giuoco/Two Knights](transpositions.md#same_as-resolved-groups),
and [Larsen/Reti Nimzowitsch-Larsen](larsen-reti-nimzowitsch-proposal.md).

## Context

After applying the Larsen `same_as` resolution (commit `cc3152c`),
the top two unresolved groups at score 4 are a **cascading pair**
of London System tabiyas:

```
rank 7:  A.Lon.Cls.MLn          ⇄ A.Lon.Msn.MLn.Nbd2
rank 8:  A.Lon.Cls.MLn.c4       ⇄ A.Lon.Msn.MLn.Nbd2.c4
```

Both pairs share their FEN. The shape is **structurally identical
to the Italian Giuoco / Two Knights pair** resolved in OCN 0.3:
two named subtrees with real literary identities converging at the
same tabiya, then converging again one move deeper. The Italian
case applied bilateral `same_as` at both ranks; the same pattern
applies here.

## FEN groups in scope (2 groups)

| rank | size | classes | slugs |
|---|---|---|---|
| 7 | 2 | A | `A.Lon.Cls.MLn`, `A.Lon.Msn.MLn.Nbd2` |
| 8 | 2 | A | `A.Lon.Cls.MLn.c4`, `A.Lon.Msn.MLn.Nbd2.c4` |

These are the only two groups in the top 100 involving the
A.Lon.Cls.* or A.Lon.Msn.* subtrees. Beyond rank 8, the Classical
side has unique continuations (`.c4.g3`, `.c4.g3.g6`) and the
Mason side terminates at the depth-5 leaf — no further mirroring.

## Subtree shape

```
A.Lon                          "London System"      depth 1, A48
  alias "Zukertort London move-order" (added by D.QPG.Zuk.Col.Bd3 → A.Lon)
├── A.Lon.Cls                  "Classical Line"     depth 2
│   └── A.Lon.Cls.MLn          "Main Line"          depth 3   ← rank 7 twin
│       └── A.Lon.Cls.MLn.c4   (no alias)           depth 4   ← rank 8 twin
│           └── A.Lon.Cls.MLn.c4.g3                 depth 5  (unique)
│               └── A.Lon.Cls.MLn.c4.g3.g6          depth 6  (unique leaf)
├── A.Lon.Job                  "Jobava London"      (separate Jobava-Prié subtree)
├── A.Lon.Msn                  "Mason Line"         depth 2
│   └── A.Lon.Msn.MLn          "Main Line"          depth 3
│       └── A.Lon.Msn.MLn.Nbd2 "Nbd2 Line"          depth 4   ← rank 7 twin
│           └── A.Lon.Msn.MLn.Nbd2.c4               depth 5  (leaf) ← rank 8 twin
└── A.Lon.Psn                  "Poisoned Pawn"      (separate subtree)
```

Two real, parallel subtrees inside `A.Lon`:

- **Classical** (contemporary literary name; modern repertoire
  books and ECO call this the "Classical London System"; depth
  goes to 6 with `.c4.g3.g6`).
- **Mason** (historical literary name attributed to James Mason
  19th–early 20th century; depth stops at 5 — the historical
  treatment doesn't extend as deeply in OCN today).

`A.Lon.Job` (Jobava London) and `A.Lon.Psn` (Poisoned Pawn) are
separate London variations and are not part of this complex.

## Why this is a clean `same_as` cascade

Apply the arbitration rules:

- **Rule 1 (descriptor vs literary)**: does NOT fire — both
  branches carry literary names rooted in their family parent
  (Classical Line / Mason Line). Neither side has "self-described
  as descriptor" notes.
- **Rule 4 (two real names, preserve both)**: **fires cleanly at
  both ranks**.
  - `A.Lon.Cls.MLn` is anchored in the "Classical London"
    family (`A.Lon.Cls`, contemporary literary name). Move order
    `d4 d5 Nf3 Nf6 Bf4 e6 e3 c5 c3 Nc6 Nbd2`.
  - `A.Lon.Msn.MLn.Nbd2` is anchored in the "Mason London"
    family (`A.Lon.Msn`, historical literary name). Move order
    `d4 d5 Nf3 Nf6 Bf4 c5 e3 e6 c3 Nc6 Nbd2`.
  - Identical FEN at move 11 (and again at move 12 after `...c4`).
  - The only difference between the move sequences is the order
    of Black's `...e6` and `...c5` — exactly the kind of move-order
    overlap that `same_as` is for.

Diagnostic table (compare against Italian Giuoco/Two Knights):

| Feature | Cls.MLn / Msn.MLn.Nbd2 | Italian Giu.O-O.Nf6 / Two.O-O.Bc5 (precedent) |
|---|---|---|
| Both have substantive subtree | Yes (Classical goes to depth 6) / Yes (Mason terminates at depth 5) | Yes / Yes (both with children) |
| Independent literary name | Yes (Classical London) | Yes (Giuoco Piano) |
| Independent literary name | Yes (Mason London) | Yes (Two Knights Defence) |
| ECO | A48 (same) | C50-C54 / C55-C56 (different) |
| Notes self-describe as descriptor | No | No |
| Cascading child pair | Yes (`.c4` deeper pair) | Yes (`.d4` deeper pair) |

Same shape, same recommendation. The ECO being identical for
Cls/Msn is the one notable difference from the Italian precedent
(which had distinct C50-54 vs C55-56), but ECO sameness does NOT
disqualify `same_as` — the Rubinstein/Colle-Zukertort precedent
had identical D05 codes on both sides and still resolved as
multi-canonical because the literary identities are real and
independent.

## Options considered

### Option A — `same_as` bilateral on BOTH ranks (RECOMMENDED)

4 `same_as` declarations total:

```
A.Lon.Cls.MLn.same_as           = A.Lon.Msn.MLn.Nbd2
A.Lon.Msn.MLn.Nbd2.same_as      = A.Lon.Cls.MLn
A.Lon.Cls.MLn.c4.same_as        = A.Lon.Msn.MLn.Nbd2.c4
A.Lon.Msn.MLn.Nbd2.c4.same_as   = A.Lon.Cls.MLn.c4
```

- **Pro**: preserves both literary identities at every depth. Same
  pattern as the Italian Giuoco/Two Knights cascade (4 `same_as`
  on 2 paired groups). Audit reports +2 multi_canonical, −2
  unresolved.
- **Pro**: respects that Mason is a complete historical naming
  tradition, not just a label for the top-of-tree position.
- **Con**: none material.

### Option B — `same_as` at rank 7, single canonical at rank 8

Bilateral `same_as` at rank 7, then `A.Lon.Msn.MLn.Nbd2.c4
.transposes_to = A.Lon.Cls.MLn.c4` at rank 8.

- **Pro**: follows the KID Classical Old/e5 precedent where leaf
  pairs got single canonical (because at KID the leaf naming was
  structural mirror).
- **Con**: at London, the Mason name IS literary at this depth
  (not just structural). Marking it as transposes_to misrepresents
  the historical Mason naming tradition. KID's leaves were
  generic "c6 Line" / "Re1 Line" descriptors; London's Mason leaf
  carries a genuine family identity.

### Option C — Single canonical `A.Lon.Cls` for both ranks (DISCARDED)

Erases Mason as literary identity. Counter to "two real names"
diagnostic. Bad.

### Option D — Single canonical `A.Lon.Msn` for both ranks (DISCARDED)

Symmetric problem. Erases the contemporary Classical naming.
Bad.

### Option E — Defer (DISCARDED)

The case is mechanically identical to Italian Giuoco/Two Knights
and Larsen/Reti Nimzowitsch-Larsen. `same_as` is in production
and exactly the tool for this. No reason to defer.

## Per-slug actions (Option A)

| slug | action | rationale | rule |
|---|---|---|---|
| `A.Lon.Cls.MLn` | **PRESERVE (canonical)**, add `same_as = A.Lon.Msn.MLn.Nbd2` | Classical London Main Line — contemporary literary anchor (A48). | Rule 4 |
| `A.Lon.Msn.MLn.Nbd2` | **PRESERVE (canonical)**, add `same_as = A.Lon.Cls.MLn` | Mason London Main Line Nbd2 — historical literary anchor (A48). | Rule 4 |
| `A.Lon.Cls.MLn.c4` | **PRESERVE (canonical)**, add `same_as = A.Lon.Msn.MLn.Nbd2.c4` | Classical London with ...c4 — has deeper exploration via `.g3.g6`. | Rule 4 |
| `A.Lon.Msn.MLn.Nbd2.c4` | **PRESERVE (canonical)**, add `same_as = A.Lon.Cls.MLn.c4` | Mason London Nbd2 with ...c4 — leaf but co-canonical literary identity. | Rule 4 |

**Notes to add** (cross-reference, informational only):

- `A.Lon.Cls.MLn.notes`: `Nbd2 in the Classical London System.
  Co-canonical with A.Lon.Msn.MLn.Nbd2 (Mason London Main Line
  Nbd2, A48) — same FEN via the historical Mason move order.`
- `A.Lon.Msn.MLn.Nbd2.notes`: `Nbd2 in the London Mason main
  line. Co-canonical with A.Lon.Cls.MLn (Classical London Main
  Line, A48) — same FEN via the contemporary Classical move
  order.`
- `A.Lon.Cls.MLn.c4.notes`: `c4 in the London Classical Main
  Line. Co-canonical with A.Lon.Msn.MLn.Nbd2.c4 (Mason London
  Nbd2 c4, A48) — same FEN.`
- `A.Lon.Msn.MLn.Nbd2.c4.notes`: `c4 in the London Mason Main
  Line, Nbd2. Co-canonical with A.Lon.Cls.MLn.c4 (Classical
  London Main Line c4, A48) — same FEN.`

No alias changes (existing "Main Line" / "Nbd2 Line" descriptions
are accurate; adding cross-family aliases would mix Mason and
Classical naming traditions in an unhelpful way).

## Summary

**Preserve (no change to canonicality)**: 4 slugs.

**`same_as` (4 declarations, 2 bilateral pairs)**:

| slug | same_as |
|---|---|
| `A.Lon.Cls.MLn` | `A.Lon.Msn.MLn.Nbd2` |
| `A.Lon.Msn.MLn.Nbd2` | `A.Lon.Cls.MLn` |
| `A.Lon.Cls.MLn.c4` | `A.Lon.Msn.MLn.Nbd2.c4` |
| `A.Lon.Msn.MLn.Nbd2.c4` | `A.Lon.Cls.MLn.c4` |

**`transposes_to`**: 0.

**Deletions**: 0.

**Reparenting**: 0.

## Expected audit metric impact

|                            | before | after | Δ |
|----------------------------|---|---|---|
| rows totals catàleg        | 5,905 | 5,905 | 0 |
| duplicate_groups           | 130 | 130 | 0 |
| resolved_groups            | 94 | **96** | **+2** |
| multiple_canonical_groups  | 7 | **9** | **+2** |
| unresolved_groups          | 36 | **34** | **−2** |
| rows_in_unresolved_groups  | 73 | **69** | **−4** |

Both rank-7 and rank-8 groups disappear from the default ranked
report; visible only under `--include-resolved` with
`resolution_kind=multiple_canonical`.

## Risks and open questions

1. **Same ECO on both sides (A48)** — unlike Rubinstein (D05/D05),
   Italian (C50-54/C55-56), or Larsen (A01/A06), here both Cls and
   Msn carry ECO A48. Does this argue against `same_as`? No — the
   precedent is set by Rubinstein (also same ECO on both sides)
   that `same_as` requires literary independence, not ECO
   independence. ECO sameness just reflects that ECO 1971 didn't
   distinguish the Mason naming subtree, which is itself a reason
   OCN preserves the distinction.

2. **Cascading depth-5 leaf** — `A.Lon.Msn.MLn.Nbd2.c4` is a leaf
   (0 kids) while its co-canonical `A.Lon.Cls.MLn.c4` has a child
   (`.g3`). Does the leaf status change anything? No. `same_as`
   pairs two canonicals regardless of subtree shape. The Mason
   leaf preserves the Mason naming for the position; the
   Classical side keeps its deeper exploration intact.

3. **Should Mason be considered a "weaker" name** because
   contemporary literature prefers Classical? No. OCN's job is to
   preserve real literary identities, not to apply a popularity
   filter. Mason London is documented in chess history; consumers
   who want to render only contemporary names can pick the
   Classical row in their UI layer.

## Recommended apply order

When approved (single commit):

1. Set 4 `same_as` declarations (2 bilateral pairs).
2. Add cross-reference notes on all 4 slugs.
3. Update `docs/transpositions.md`:
   - Move London Cls/Msn from "Deferred" to the same_as-resolved
     table.
   - Bump multi-canonical count to 9.
4. Mark this proposal `Status: APPLIED`.

Validations to run: standard suite. Expected commit shape: 4
catalogue rows touched (8 / 8 line diff with notes), one short
doc update. No catalogue row count change.
