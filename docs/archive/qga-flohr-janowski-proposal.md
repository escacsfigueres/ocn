# QGA Flohr ↔ Janowski-Larsen Haberditz — arbitration proposal

**Status**: **APPLIED via bilateral `same_as`**. See
`docs/transpositions.md` → "`same_as`-resolved groups" for the
applied outcome. Smallest `same_as` sprint since Larsen — single
pair, no cascade, no deletes.
**Companion**: builds on `spec/OCN-1.md` → "Canonicalisation
arbitration" and the precedents from the 5 prior `same_as`
applications (Rubinstein, Italian Giuoco/Two Knights, Larsen,
London Classical/Mason, Van Geet/Van't Kruijs).

## Context

After applying Van Geet/Van't Kruijs (commit `54fb9b7`), one of
the highest-leverage remaining unresolved groups inside D-class
is a single 2-row pair within Queen's Gambit Accepted:

```
rank 5:  D.QGA.Flo.MLn       ⇄ D.QGA.Jan.e3.b5
```

Both reach the same FEN
`rnbqkbnr/2p1pppp/p7/1p6/2pP4/4PN2/PP3PPP/RNBQKB1R w KQkq -`
(QGA after `1.d4 d5 2.c4 dxc4 3.Nf3 a6 4.e3 b5`) by identical
move sequences — the only thing that differs is the OCN parent
chain.

This is a candidate for bilateral `same_as` following the Larsen
precedent (1-group, 2 real literary names, no cascade).

## FEN group in scope (1 group)

| rank | size | classes | slugs |
|---|---|---|---|
| 5 | 2 | D | `D.QGA.Flo.MLn`, `D.QGA.Jan.e3.b5` |

No related FEN duplicates appear in the top 100 beyond this single
pair. The Flohr and Janowski subtrees explore different
continuations from here (Flohr.MLn extends to `.a4`, Janowski leaf
terminates).

## Subtree shape

```
D.QGA                                    "Queen's Gambit Accepted" (D20-D29 family)
├── D.QGA.Flo                            "Flohr Variation"       depth 2, D20
│   └── D.QGA.Flo.MLn                    "Main Line"             depth 3, D20  ← rank 5 twin
│       └── D.QGA.Flo.MLn.a4             "a4 Line"               depth 4 (leaf)
├── D.QGA.Jan                            "Janowski-Larsen"       depth 2, D25
│   ├── D.QGA.Jan.Fur                    "Furman Variation"      depth 3, D21
│   ├── D.QGA.Jan.MLn                    "Main Line"             depth 3, D25
│   │   └── D.QGA.Jan.MLn.O-O            "O-O Line"              depth 4
│   └── D.QGA.Jan.e3                     "e3 Line / Alatortsev Prefix"   depth 3 (structural prefix)
│       ├── D.QGA.Jan.e3.Bg4             "Bg4 Line / Alatortsev Prefix"  (4-deep Alatortsev branch)
│       │   └── D.QGA.Jan.e3.Bg4.Bxc4
│       │       └── D.QGA.Jan.e3.Bg4.Bxc4.e6  "Alatortsev Variation Prefix"
│       └── D.QGA.Jan.e3.b5              "Haberditz Variation"   depth 4 (leaf)   ← rank 5 twin
└── …
```

Two genuine QGA literary identities converge at this FEN:

- **Flohr Variation** (`D.QGA.Flo`, ECO D20) — named after Salo
  Flohr. Substantive enough to have its own family root in OCN.
- **Haberditz Variation** (`D.QGA.Jan.e3.b5`, alias literary) —
  named after Carl Haberditz. Lives one level deeper under the
  Janowski-Larsen Variation (D25) via the e3 / Alatortsev prefix
  structural path.

## Conceptual analysis — are both real?

**Yes**, both names are documented in chess literature, but with
an asymmetry worth noting:

| feature | D.QGA.Flo.MLn | D.QGA.Jan.e3.b5 |
|---|---|---|
| Slug carries literary alias | "Main Line" (generic) | "Haberditz Variation" (literary) |
| Parent literary identity | "Flohr Variation" (D.QGA.Flo, D20) | "e3 Line / Alatortsev Prefix" (structural at depth 3) |
| Grandparent literary identity | n/a (Flo is depth 2) | "Janowski-Larsen Variation" (D.QGA.Jan, D25) |
| Subtree depth from literary anchor | 1 step from Flo | 2 steps from Jan (via structural Jan.e3) |
| ECO assignment on the slug | D20 | empty (D25 inherited from Jan) |
| Children | 1 (.a4) | 0 (leaf) |

Both names are real. The structural asymmetry — Flohr lives one
level closer to its literary family root than Haberditz does — is
the same pattern as Rubinstein/Colle-Zukertort (Rubinstein at
depth 1, Colle-Zukertort at depth 2) and doesn't disqualify
`same_as`. The literary identity of the leaf-with-alias is the
test that matters: Haberditz has it.

Compare with the 5 prior `same_as` cases:

| case | both literary? | sub-pattern |
|---|---|---|
| Rubinstein ⇄ Colle-Zukertort | yes | depth 1 vs depth 2, both family-root literary |
| Italian Giuoco ⇄ Two Knights | yes | both named family children of C.Ita |
| Larsen ⇄ Reti Nimzowitsch-Larsen | yes | both depth 3 under named family parents |
| London Classical ⇄ Mason | yes | both depth 3-4 under named family parents, cascade |
| Van Geet ⇄ Van't Kruijs | yes (2 of 3) | mixed, third was structural breadcrumb |
| **QGA Flohr ⇄ Haberditz** | **yes** | **Flohr at family-root, Haberditz at leaf-with-literary-alias** |

The pattern is closest to Rubinstein (literary at different depths
from family root), with the additional wrinkle that the
Janowski-Larsen side uses a structural prefix (`Jan.e3`) before
reaching the Haberditz literary leaf. But the Haberditz name is
genuine — it's a recognised QGA line attributable to Haberditz,
not a Lichess-imported descriptor.

## Options considered

### Option A — `same_as` bilateral (RECOMMENDED)

```
D.QGA.Flo.MLn.same_as       = D.QGA.Jan.e3.b5
D.QGA.Jan.e3.b5.same_as     = D.QGA.Flo.MLn
```

Both preserved as canonicals. Audit reports +1 multi_canonical,
−1 unresolved. No deletions, no transposes_to, no reparenting.

- **Pro**: preserves both literary names. Mirrors Rubinstein
  precedent (literary identities at different depths from their
  family roots — no requirement that both anchors be at the same
  tree level).
- **Pro**: no schema work, no policy change, single pair (no
  cascade).
- **Con**: none material.

### Option B — Single canonical `D.QGA.Flo.MLn`

`D.QGA.Jan.e3.b5.transposes_to = D.QGA.Flo.MLn`

- **Con**: erases Haberditz as a literary identity. Haberditz is
  a real attribution, not a Lichess descriptor. Marking it as
  transposition misrepresents its standing in QGA literature.

### Option C — Single canonical `D.QGA.Jan.e3.b5`

- **Con**: symmetric problem. Flohr is more prominent in
  contemporary QGA repertoires (ECO D20 is widely cited as Flohr
  Variation). Marking it as transposes_to would be a step
  backward.

### Option D — Defer

- **Con**: structural analysis is unambiguous. The Haberditz
  leaf has an explicit literary alias and the Flohr family is
  a recognised ECO branch. `same_as` exists for exactly this case.

## Recommendation: **Option A** (bilateral `same_as`)

### Per-slug actions

| slug | action | rationale | rule |
|---|---|---|---|
| `D.QGA.Flo.MLn` | **PRESERVE (canonical)**, add `same_as = D.QGA.Jan.e3.b5` | Flohr Variation main line — anchored in literary D.QGA.Flo family (D20). | Rule 4 |
| `D.QGA.Jan.e3.b5` | **PRESERVE (canonical)**, add `same_as = D.QGA.Flo.MLn` | Haberditz Variation — literary leaf alias within Janowski-Larsen e3 path. | Rule 4 |

### Notes to add (cross-references)

- `D.QGA.Flo.MLn.notes`: `...b5 in the Flohr QGA. Co-canonical
  with D.QGA.Jan.e3.b5 (Janowski-Larsen e3 Haberditz Variation)
  — same FEN via the Janowski-Larsen Alatortsev e3 move order.`
- `D.QGA.Jan.e3.b5.notes`: `...b5 holds the c4 pawn in the
  Janowski-Larsen e3 branch (Haberditz Variation). Co-canonical
  with D.QGA.Flo.MLn (Flohr Variation Main Line, D20) — same FEN
  via the direct Flohr move order.`

No alias changes (each slug's existing alias accurately reflects
its literary identity; adding cross-family aliases would confuse
the Flohr and Janowski-Larsen naming traditions).

## Summary

**Preserve (no canonicality change)**: 2 slugs.

**`same_as` (2 declarations, 1 bilateral pair)**:

| slug | same_as |
|---|---|
| `D.QGA.Flo.MLn` | `D.QGA.Jan.e3.b5` |
| `D.QGA.Jan.e3.b5` | `D.QGA.Flo.MLn` |

**`transposes_to`**: 0. **Deletions**: 0. **Reparenting**: 0.

## Expected audit metric impact

|                            | before | after | Δ |
|----------------------------|---|---|---|
| rows totals catàleg        | 5,905 | 5,905 | 0 |
| duplicate_groups           | 130 | 130 | 0 |
| resolved_groups            | 98 | **99** | **+1** |
| multiple_canonical_groups  | 11 | **12** | **+1** |
| unresolved_groups          | 32 | **31** | **−1** |
| rows_in_unresolved_groups  | 64 | **62** | **−2** |

The rank-5 group disappears from the default ranked report;
visible only under `--include-resolved` with
`resolution_kind=multiple_canonical`.

## Risks and open questions

1. **Asymmetric depth-from-literary-root** (Flohr at depth 1 from
   D.QGA.Flo, Haberditz at depth 2 from D.QGA.Jan via the
   structural Jan.e3 prefix). Not a disqualifier — Rubinstein
   precedent has the same pattern (depth 1 vs depth 2) and worked
   cleanly.

2. **Haberditz parent is structural** (`Jan.e3` with alias
   "Alatortsev Prefix"). The Haberditz literary identity lives
   at the leaf alias, not at the immediate parent. This is
   acceptable per OCN's convention — literary identity at the
   slug-alias level is sufficient for `same_as`. Compare with
   A.VtK.e5.Nc3.d5 where "Ekolu Variation" was the literary
   alias under a structural Keoni-Hiva prefix.

3. **ECO on the Haberditz leaf is empty** (parent D.QGA.Jan
   carries D25, but Jan.e3.b5 itself has no ECO). The Flohr side
   has D20. This is unusual but does not affect `same_as`
   validity — ECO is informational, not a precondition for
   co-canonical status.

4. **Single-pair, no cascade** — easier than London or Italian.
   Lowest-risk `same_as` proposal since Larsen.

## Recommended apply order

When approved (single commit):

1. Set `D.QGA.Flo.MLn.same_as = D.QGA.Jan.e3.b5`.
2. Set `D.QGA.Jan.e3.b5.same_as = D.QGA.Flo.MLn`.
3. Add cross-reference notes on both.
4. Update `docs/transpositions.md`:
   - Move QGA Flohr/Haberditz to the same_as-resolved table.
   - Bump multi-canonical count to 12.
5. Mark this proposal `Status: APPLIED`.

Validation suite: standard. Expected commit shape: 2 catalogue
rows touched (4 / 4 line diff with notes), 1 doc update. No row
count change.
