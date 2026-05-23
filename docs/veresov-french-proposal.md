# Veresov / French complex — arbitration proposal

**Status**: draft proposal — NOT yet applied to `catalog/ocn-1.csv`.
**Companion**: builds on the rules in `spec/OCN-1.md` →
"Canonicalisation arbitration" and the list in
`docs/transpositions.md` → "Deferred conceptual families".

## Why this complex is different

Every previous resolved family had a clear winner: a literary name on
one side, a path descriptor on the other. The Veresov / French
complex breaks that pattern in two distinct ways:

1. **Three real names converge on one FEN** (rank 1):
   `B.Fre.Cls.MLn` (French Classical Main Line, ECO C13/C14),
   `A.Ver.Cls.MLn.Be7` (Richter-Veresov Classical Be7, ECO D01),
   and `D.QPG.Ver.MLn.Be7` (Queen's Pawn Veresov Setup Be7,
   ECO D01). French Classical is not a breadcrumb of Veresov;
   Veresov is not a breadcrumb of French; both are taught and
   played under their own name. Any single canonical choice
   erases real literature.
2. **The D-side Veresov subtree mirrors itself**. `A.Ver`
   (Richter-Veresov Attack, the literary anchor) and `D.QPG.Ver`
   (Queen's Pawn Game / Veresov Setup) share the FEN reached
   after the diagonal move order. Inside `D.QPG.Ver`, a sibling
   `D.QPG.Ver.Ric` ("Queen's Pawn Veresov, Richter-Veresov
   Attack") **re-states** the same Richter-Veresov identity via
   the `1...Nf6` move order, and each of its three children
   mirrors a sibling of `D.QPG.Ver`.

This proposal applies the Canonicalisation arbitration rules (1–7)
slug-by-slug, **preserves French Classical without a
transposes_to**, collapses the Veresov D-side breadcrumbs into the
A-side canonical, and prunes the redundant Ric-mirror subtree
inside D where it is safe.

## FEN groups in scope (8 total)

Audit ranks at the moment of this proposal:

| rank | size | classes | slugs |
|---|---|---|---|
| 1   | 3 | A,B,D | `B.Fre.Cls.MLn`, `A.Ver.Cls.MLn.Be7`, `D.QPG.Ver.MLn.Be7` |
| 2   | 3 | A,D   | `A.Ver`, `D.QPG.Ver`, `D.QPG.Ver.Ric` |
| 5   | 2 | A,D   | `A.Ver.Ric`, `D.QPG.Ver.Ric.Bf5` |
| 8   | 2 | A,D   | `A.Ver.Cls.MLn`, `D.QPG.Ver.MLn` |
| 24  | 2 | D     | `D.QPG.Ver.Nbd7.Nf3`, `D.QPG.Ver.Ric.Nbd7.Nf3` |
| 25  | 2 | D     | `D.QPG.Ver.Nbd7`, `D.QPG.Ver.Ric.Nbd7` |
| 60  | 2 | D     | `D.QPG.Ver.Ne4`, `D.QPG.Ver.Ric.Ne4` |
| 103 | 2 | B     | `B.Fre.Cls.MLn.e5.Qxe7`, `B.Fre.Cls.MLn.e5.Nfd7.Qxe7` |

Ranks 1 and 2 are the conceptual anchors; the rest cascade once
those two are decided.

## Slug inventory

| slug | name | class | depth | kids | aliases / notes summary |
|---|---|---|---|---|---|
| `B.Fre.Cls.MLn` | French Classical, Main Line | B | 3 | 3 | alias `Main Line`; notes `4.Bg5 Be7 in the Classical French` |
| `A.Ver` | Richter-Veresov Attack | A | 1 | 3 | alias `Veresov Attack`; notes `Queen-pawn system with Nc3 and Bg5` |
| `A.Ver.Cls.MLn` | Richter-Veresov Classical, Main Line | A | 3 | 1 | alias `Main Line`; notes `e4 in the Classical Veresov` |
| `A.Ver.Cls.MLn.Be7` | Richter-Veresov Classical MLn, Be7 | A | 4 | 0 | alias `Be7 Line` |
| `A.Ver.Ric` | Richter-Veresov, Richter Attack | A | 2 | 1 | alias `Richter Attack` |
| `D.QPG.Ver` | Queen's Pawn Game, Veresov Setup | D | 2 | 5 | alias `Veresov Setup` |
| `D.QPG.Ver.Ric` | Queen's Pawn Veresov, Richter-Veresov Attack | D | 3 | 3 | alias `Richter-Veresov Attack`; notes `Nf6 move order into the Veresov attack` |
| `D.QPG.Ver.MLn` | Queen's Pawn Veresov Setup, Main Line | D | 3 | 1 | alias `Main Line` |
| `D.QPG.Ver.MLn.Be7` | Queen's Pawn Veresov MLn, Be7 | D | 4 | 1 | alias `Be7 Line` |
| `D.QPG.Ver.Nbd7` | Veresov, Two Knights System | D | 3 | 1 | alias `Two Knights System` |
| `D.QPG.Ver.Nbd7.Nf3` | Veresov Two Knights, Nf3 | D | 4 | 1 | alias `Nf3 Line` |
| `D.QPG.Ver.Ne4` | Veresov, Boyce Defence | D | 3 | 0 | alias `Boyce Defence` |
| `D.QPG.Ver.Ric.Bf5` | Veresov Richter, Bf5 Line | D | 4 | 1 | alias `Richter Variation` |
| `D.QPG.Ver.Ric.Nbd7` | Veresov Richter, Two Knights System | D | 4 | 1 | alias `Two Knights System` |
| `D.QPG.Ver.Ric.Nbd7.Nf3` | Veresov Richter Two Knights, Nf3 | D | 5 | 0 | alias `Nf3 Line` |
| `D.QPG.Ver.Ric.Ne4` | Veresov Richter, Boyce Defence | D | 4 | 0 | alias `Boyce Defense` |
| `B.Fre.Cls.MLn.e5.Qxe7` | French Classical e5, Bxe7 Qxe7 | B | 5 | 4 | alias `Classical Exchange Line` |
| `B.Fre.Cls.MLn.e5.Nfd7.Qxe7` | French Classical Nfd7, Qxe7 | B | 6 | 0 | alias `Qxe7 Line` |

## Proposal — per-slug action

Actions are PRESERVE (no change), TT → target (set `transposes_to`),
or DELETE (physically remove the row). Each action cites the
arbitration rule that justifies it.

### Group rank 1 — the 3-way A/B/D Be7 tabiya

| slug | action | rationale | rule |
|---|---|---|---|
| `B.Fre.Cls.MLn` | **PRESERVE** | French Classical Main Line is a primary literary identity (ECO C13/C14) on its own move-order tree (`1.e4 e6`). It is not a breadcrumb of any Veresov line. The position is reached by French and known by French. | Rule 4 (two real names) |
| `A.Ver.Cls.MLn.Be7` | **PRESERVE** | Canonical Richter-Veresov Classical Be7 on the A.Ver subtree (literary anchor). | Rule 4 (two real names) |
| `D.QPG.Ver.MLn.Be7` | **TT → A.Ver.Cls.MLn.Be7** | D-side breadcrumb of the same Veresov line; `D.QPG.Ver.*` is the Queen's Pawn Game move-order tree that converges on Veresov by transposition. Has 1 child — kept alive with TT. | Rule 5 (family tabiya beats breadcrumb) + Rule 6 (cascade) |

**Outcome at rank 1**: the FEN group remains "duplicate" by audit
(B.Fre.Cls.MLn and A.Ver.Cls.MLn.Be7 are both canonical) but is
"resolved" by `transposes_to` because D.QPG.Ver.MLn.Be7 points into
the group. Result in audit: 1 canonical (counting either of the
two preserved as the "canonical" entry — see open question below)
+ 1 TT pointer. **Audit may need adjustment** (see "Open questions").

### Group rank 2 — A.Ver tree root

| slug | action | rationale | rule |
|---|---|---|---|
| `A.Ver` | **PRESERVE (canonical)** | Established literary name "Richter-Veresov Attack", root of the A.Ver subtree with 3 named children. | Rule 1 (established name) |
| `D.QPG.Ver` | **TT → A.Ver** | "Queen's Pawn Game, Veresov Setup" — move-order breadcrumb from the D-class root. Has 5 kids — TT (rule 6). | Rule 5 |
| `D.QPG.Ver.Ric` | **TT → A.Ver** | Self-re-stating "Queen's Pawn Veresov, Richter-Veresov Attack" — same FEN, same identity as A.Ver, reached via `1.d4 Nf6` move order. Has 3 kids (Bf5, Ne4, Nbd7) all of which mirror siblings of D.QPG.Ver. TT (rule 6). | Rule 5 + Rule 3 (parent-child redundancy on D.QPG.Ver side) |

### Group rank 5 — Richter Attack

| slug | action | rationale | rule |
|---|---|---|---|
| `A.Ver.Ric` | **PRESERVE (canonical)** | Literary "Richter Attack" inside Richter-Veresov. | Rule 1 |
| `D.QPG.Ver.Ric.Bf5` | **TT → A.Ver.Ric** | D-side breadcrumb of the same Bf5 line; has 1 child — TT. | Rule 5 + Rule 6 |

### Group rank 8 — Classical MLn

| slug | action | rationale | rule |
|---|---|---|---|
| `A.Ver.Cls.MLn` | **PRESERVE (canonical)** | Canonical Richter-Veresov Classical Main Line. | Rule 1 |
| `D.QPG.Ver.MLn` | **TT → A.Ver.Cls.MLn** | D-side breadcrumb. Has 1 child — TT. | Rule 5 + Rule 6 |

### Group rank 24 — Veresov Two Knights Nf3

| slug | action | rationale | rule |
|---|---|---|---|
| `D.QPG.Ver.Nbd7.Nf3` | **PRESERVE (canonical)** | Canonical "Veresov Two Knights, Nf3" on the non-Ric subtree. | Rule 3 (sibling-mirror anchor) |
| `D.QPG.Ver.Ric.Nbd7.Nf3` | **DELETE** | Mirror of the non-Ric Nf3 line via the `1...Nf6` move order. 0 children, 0 inbound refs, descriptor identity only. | Rule 3 + Rule 6 |

### Group rank 25 — Veresov Two Knights System

| slug | action | rationale | rule |
|---|---|---|---|
| `D.QPG.Ver.Nbd7` | **PRESERVE (canonical)** | Canonical "Veresov, Two Knights System". | Rule 3 |
| `D.QPG.Ver.Ric.Nbd7` | **DELETE** | After rank 24 delete fires, this row becomes leaf (0 kids). Identical FEN to its non-Ric sibling, descriptor identity. | Rule 3 + Rule 6 |

### Group rank 60 — Veresov Boyce Defence

| slug | action | rationale | rule |
|---|---|---|---|
| `D.QPG.Ver.Ne4` | **PRESERVE (canonical)** | Canonical "Veresov, Boyce Defence". | Rule 3 |
| `D.QPG.Ver.Ric.Ne4` | **DELETE** | Mirror leaf, 0 kids/0 refs, descriptor identity. | Rule 3 + Rule 6 |

### Group rank 103 — French Classical Qxe7 mirror

| slug | action | rationale | rule |
|---|---|---|---|
| `B.Fre.Cls.MLn.e5.Qxe7` | **PRESERVE (canonical)** | Established "French Classical e5, Bxe7 Qxe7" with 4 substantive children. | Rule 3 |
| `B.Fre.Cls.MLn.e5.Nfd7.Qxe7` | **DELETE** | Same-FEN leaf via the explicit-Nfd7 move-order path; 0 kids, 0 refs, descriptor only. | Rule 3 |

## Summary

**Preserved (no change)**: 9 slugs — `B.Fre.Cls.MLn`, `A.Ver`,
`A.Ver.Cls.MLn`, `A.Ver.Cls.MLn.Be7`, `A.Ver.Ric`,
`D.QPG.Ver.Nbd7`, `D.QPG.Ver.Nbd7.Nf3`, `D.QPG.Ver.Ne4`,
`B.Fre.Cls.MLn.e5.Qxe7`.

**TT (transposes_to)**: 5 arrows.

| from | → | to |
|---|---|---|
| `D.QPG.Ver.MLn.Be7` | → | `A.Ver.Cls.MLn.Be7` |
| `D.QPG.Ver` | → | `A.Ver` |
| `D.QPG.Ver.Ric` | → | `A.Ver` |
| `D.QPG.Ver.Ric.Bf5` | → | `A.Ver.Ric` |
| `D.QPG.Ver.MLn` | → | `A.Ver.Cls.MLn` |

**DELETE**: 4 rows.

| slug | reason | safety |
|---|---|---|
| `D.QPG.Ver.Ric.Nbd7.Nf3` | mirror of `D.QPG.Ver.Nbd7.Nf3` via Nf6 move order | leaf, 0 kids/0 refs, depth 5 |
| `D.QPG.Ver.Ric.Nbd7` | parent of the above; after rank-24 delete becomes leaf | depth 4, becomes leaf post-cascade |
| `D.QPG.Ver.Ric.Ne4` | mirror of `D.QPG.Ver.Ne4` via Nf6 move order | leaf, 0 kids/0 refs, depth 4 |
| `B.Fre.Cls.MLn.e5.Nfd7.Qxe7` | mirror of `B.Fre.Cls.MLn.e5.Qxe7` via explicit Nfd7 path | leaf, 0 kids/0 refs, depth 6 |

## Concrete policy summary

The Veresov / French complex resolves into three distinct decisions:

1. **A.Ver is the literary canonical for Richter-Veresov**.
   The whole `D.QPG.Ver.*` subtree becomes a move-order
   breadcrumb pointing into `A.Ver.*` via `transposes_to` at each
   matching depth where a same-FEN pair exists. Rows are kept
   alive (rule 6) because most have children, but the canonical
   relation is now explicit.

2. **The D.QPG.Ver.Ric sub-subtree is structurally redundant**.
   It re-states the same Richter-Veresov identity via the
   `1...Nf6` move order. Its top row gets TT into `A.Ver`; its
   leaf descendants whose siblings live under `D.QPG.Ver.*` get
   physically deleted as descriptor mirrors. The `Bf5` child is
   preserved with TT (because A.Ver.Ric is its real canonical).

3. **French Classical is preserved without `transposes_to`**.
   The 3-way rank-1 group keeps both `B.Fre.Cls.MLn` and
   `A.Ver.Cls.MLn.Be7` as canonical entries on their respective
   trees. Only the D-side breadcrumb `D.QPG.Ver.MLn.Be7` points
   into the A side. This is the first OCN case where **two
   canonical slugs coexist in the same FEN group by design**.

## Risks and open questions

1. **The audit's resolved-detection logic assumes exactly one
   canonical per group.** In rank 1, after applying this
   proposal, the group has TWO canonicals (`B.Fre.Cls.MLn` +
   `A.Ver.Cls.MLn.Be7`) and ONE pointer (`D.QPG.Ver.MLn.Be7` →
   `A.Ver.Cls.MLn.Be7`). The current `_is_resolved()` returns
   False when `len(canonicals) != 1`. This proposal will leave
   rank 1 **unresolved by the audit even after applying**, even
   though it is conceptually correct. Options:

   - **Accept**: rank 1 stays in the unresolved report as a
     known "two canonicals by design" group. Cheap. Loses
     audit precision.
   - **Extend the resolved-detection rule**: a group with N
     canonicals + (group_size − N) pointers into the group
     counts as resolved if every pointer's target is one of
     the N canonicals. Cleaner but requires a small change to
     `tools/audit_transpositions.py` and a test.
   - **Introduce a `same_as` / `also_known_as_position`
     column** (your suggestion at the end of your prompt).
     Most principled but expands the schema. Defer to OCN 0.3.

   **Recommendation**: extend `_is_resolved()` to accept multiple
   canonicals (option 2). Small, testable, no schema change. Can
   be a separate commit that lands before applying the catalogue
   changes.

2. **Should `B.Fre.Cls.MLn` carry an alias or note** indicating
   the Veresov transposition? E.g. `aliases += "Richter-Veresov
   Classical move-order"` or a note `Reached as Richter-Veresov
   Classical via 1.d4 Nf6 2.Nc3 d5 3.Bg5 e6 4.e4 Be7`. This is
   informational only, no behavioural impact. **Recommendation**:
   yes, add the note (not the alias — the alias would be
   misleading for ECO consumers reading C13/C14).

3. **The 4 deletions in the D.QPG.Ver.Ric subtree** leave that
   subtree with only the Bf5 child (which has its own TT to
   A.Ver.Ric). Once that lands, `D.QPG.Ver.Ric` is a depth-3 slug
   with 1 child and a TT pointer to A.Ver. **Acceptable?** Yes —
   it preserves a literary identity ("Queen's Pawn Veresov,
   Richter-Veresov Attack" is a known label for the `1...Nf6`
   move order) without re-stating the whole subtree.

4. **No reparenting**. All preserved slugs keep their existing
   `parent_ocn1`. The proposal is strictly additive
   (`transposes_to` writes) + selective deletion of mirror leaves.
   This is consistent with Rule 6 ("prefer TT over slug surgery
   when surgery cascades").

5. **External consumers**: any tool that resolves OCN by FEN and
   follows `transposes_to` will now resolve all `D.QPG.Ver.*`
   FEN to `A.Ver.*`. Tools that resolve by ECO (`D01` → first
   matching slug) continue to work; the deepest-match rule still
   selects from preserved rows. No breaking change.

6. **What about `A.Ver.Hub`** (the third child of A.Ver under
   "Hübner Variation")? It is preserved as-is (not in this
   complex's audit groups, so no FEN duplicate). The proposal
   does not touch it. Same for the deeper `D.QPG.Ver.c5`
   (another sibling not in any audit group at this rank
   range).

## Recommended apply order

When you approve the proposal:

1. Extend `tools/audit_transpositions.py` `_is_resolved()` to
   accept multiple canonicals (separate commit).
2. Apply the 5 `transposes_to` arrows + 4 deletions in one
   "Resolve Veresov French complex" commit.
3. Add the cross-reference note on `B.Fre.Cls.MLn`.
4. Update `docs/transpositions.md` `Deferred conceptual families`
   table to move French/Veresov from "Deferred" to "Resolved".
