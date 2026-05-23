# Modern Benoni triple — arbitration proposal

**Status**: draft proposal — NOT yet applied to `catalog/ocn-1.csv`.
**Companion**: builds on the rules in `spec/OCN-1.md` →
"Canonicalisation arbitration" and the precedents from
`veresov-french-proposal.md` and
`kid-classical-transposition-proposal.md`.

## Context

After resolving Veresov / French (multiple canonical, cross-class)
and KID Classical Old/e5 (multiple canonical at parent, single at
leaves, both intra-E), the new top-1 in the audit is the **Modern
Benoni Classical** triple:

```
E.Ben.Mod.Cls
E.Ben.Mod.Cls.Trd
E.Ind.e6.Nf3.c5.d5.Be2
```

The shape is superficially similar to KID Old/e5 — three slugs, one
FEN, cross-family flavour — but the *content* is different. The
KID case had two genuine literary anchors (E91 Old Main Line vs
E95 Castled Nbd7). The Modern Benoni case has **one literary
anchor and two move-order descriptors**:

- `E.Ben.Mod.Cls` is the canonical "Modern Benoni, Classical" with
  ECO A70-A79 (the full Classical Benoni range) and **7 children**
  covering distinct White plans (MLn, Nd2, Bg5, Rb1, h3, Trd, O-O).
- `E.Ben.Mod.Cls.Trd` is depth 4, **0 kids**, alias `Traditional
  Variation`, notes literally say *"Nf3 move order into the
  Classical Modern Benoni"*. It is **a move-order re-statement of
  its own parent**, not a peer literary identity.
- `E.Ind.e6.Nf3.c5.d5.Be2` is depth 6, **0 kids**, alias
  `Traditional Variation` (same alias!), notes *"Be2 in the
  Anti-Nimzo Benoni move order"*. Its `moves_uci` is **identical**
  to `.Trd`'s — they are literally the same move sequence, just
  parented under different families.

This is **not a multiple_canonical case**. It is a single canonical
(`E.Ben.Mod.Cls`) with two descriptor mirrors that converge on the
same Benoni position via two move orders.

## FEN groups in scope (3 groups in top 80)

| rank | size | classes | slugs | summary |
|---|---|---|---|---|
| 1   | 3 | E | `E.Ben.Mod.Cls`, `E.Ben.Mod.Cls.Trd`, `E.Ind.e6.Nf3.c5.d5.Be2` | Canonical + 2 move-order descriptors |
| 70  | 2 | E | `E.Ben.Mod.Cls.MLn.Re8.Nd2`, `E.Ben.Mod.Cls.MLn.Re8.Tal` | Two leaf siblings, same FEN, both aliased `Tal Line` |
| 111 | 2 | E | `E.Ben.Bnk.Acc.MLn.Bxa6.f4`, `E.Ben.Bnk.Acc.MLn.g6.f4` | Two Benko Accepted leaves, same `Central Storming` alias |

Ranks 70 and 111 are **not** part of the rank 1 triple's complex —
they sit in different Benoni subtrees (Classical MLn Re8 and Benko
Accepted respectively). I include them here because they fit the
same intra-Benoni cleanup pass.

## Subtree shape (rank 1 context)

```
E.Ben.Mod                            "Modern Benoni"      depth 2
├── E.Ben.Mod.Fch                    "Fianchetto"         3 kids
├── E.Ben.Mod.Fou                    "Four Pawns Attack"  2 kids
├── E.Ben.Mod.Cls                    "Classical"          7 kids   ← literary anchor
│   ├── E.Ben.Mod.Cls.MLn            "Main Line"          4 kids
│   ├── E.Ben.Mod.Cls.Nd2            "Nd2 Line"           1 kid
│   ├── E.Ben.Mod.Cls.Bg5            "Bg5 Line"           1 kid
│   ├── E.Ben.Mod.Cls.Rb1            "Rb1 Line"           1 kid
│   ├── E.Ben.Mod.Cls.h3             "h3 Line"            1 kid
│   ├── E.Ben.Mod.Cls.Trd            "Traditional Var."   0 kids   ← move-order descriptor (Nf3 order)
│   └── E.Ben.Mod.Cls.O-O            "Castled Defence"    0 kids
└── …

E.Ind.e6.Nf3.c5.d5                   "Anti-Nimzo c5, d5"  8 kids
└── E.Ind.e6.Nf3.c5.d5.Be2           "Anti-Nimzo Benoni"  0 kids   ← same FEN as .Trd
```

Observations:

- The .Trd slug is the **only child of E.Ben.Mod.Cls without a
  chess-move-based name**. Its siblings (MLn, Nd2, Bg5, Rb1, h3,
  O-O) each describe a specific White move or Black response; .Trd
  just describes a move order.
- The Indian leaf is the deepest of 8 Anti-Nimzo Benoni continuations
  under `E.Ind.e6.Nf3.c5.d5.*`. The other 7 (`exd5`, `g6`, `g3`,
  `Nd2`, `Bg5`, `e4`, `h3`) describe White's next move at that
  depth; `.Be2` is the only one named "Traditional" with explicit
  move-order notes.
- Move sequences for `.Trd` and `.Be2`:
  ```
  E.Ben.Mod.Cls.Trd        : d2d4 g8f6 c2c4 e7e6 g1f3 c7c5 d4d5 e6d5 c4d5 d7d6 b1c3 g7g6 e2e4 f8g7 f1e2
  E.Ind.e6.Nf3.c5.d5.Be2   : d2d4 g8f6 c2c4 e7e6 g1f3 c7c5 d4d5 e6d5 c4d5 d7d6 b1c3 g7g6 e2e4 f8g7 f1e2
  ```
  **Literally identical**. They are duplicate descriptors of the
  same Nf3-move-order path.

## Why not multiple_canonical here

Apply the arbitration rules in order:

- **Rule 1 (established name beats descriptor)** fires immediately.
  `E.Ben.Mod.Cls` is the literary anchor (Modern Benoni Classical,
  ECO A70-A79, 7-child subtree). `.Trd` and `.Be2` are
  Lichess-imported "Traditional Variation" labels that re-state
  the same position via the Nf3 move order. Single canonical.

- **Rule 4 (preserve both real names)** does NOT fire. For Rule 4
  to apply, both sides need substantive literary identity — typically
  shown by having distinct ECO ranges, their own subtrees, and
  literature treating them as separate openings. .Trd has 0 kids
  and notes explicitly identifying it as a move-order descriptor.
  This is the disqualifying signal.

- **Rule 5 (family tabiya beats move-order breadcrumb)** confirms:
  the Indian leaf is a breadcrumb from the Anti-Nimzo move-order
  tree; the Benoni Classical is the family tabiya.

Compare to the KID Classical case:

| Feature | KID Old/e5 | Modern Benoni |
|---|---|---|
| Both sides have children | Yes (3 + 3) | No (7 + 0 + 0) |
| Distinct ECO codes per side | Yes (E91 vs E95) | Same range (A70 on all three) |
| Subtree of literary continuations | Yes on both sides | Only on E.Ben.Mod.Cls |
| Notes explicitly call out "move order" | No | **Yes on both descriptors** |
| Self-described as descriptor | No | Yes |

Different structurally, different conceptually. KID was a real
two-name case; Modern Benoni is a single-name + two move-order
mirrors.

## Per-slug actions

### Rank 1 — Modern Benoni Classical triple

| slug | action | rationale | rule |
|---|---|---|---|
| `E.Ben.Mod.Cls` | **PRESERVE (canonical)** | Modern Benoni Classical with 7 chess-named children. ECO A70-A79. Literary anchor of the whole subtree. | Rule 1 |
| `E.Ben.Mod.Cls.Trd` | **TT → `E.Ben.Mod.Cls`** | Move-order re-statement of parent. Notes literally say "Nf3 move order into the Classical Modern Benoni". 0 kids, 0 inbound refs. Kept alive (with TT) so the Lichess "Traditional Variation" label remains navigable from inside the Benoni subtree. | Rule 5 |
| `E.Ind.e6.Nf3.c5.d5.Be2` | **DELETE** | Leaf, 0 kids, 0 inbound refs. `moves_uci` is **literally identical** to `.Trd` — it is the same move-order descriptor parented under the Anti-Nimzo tree. Once `.Trd` declares the equivalence with TT, this row adds nothing the catalogue does not already record. | Rule 1 + Rule 3 (leaf descriptor) + Rule 6 (no cascade risk) |

### Rank 70 — Tal Line intra-Benoni pair

| slug | action | rationale | rule |
|---|---|---|---|
| `E.Ben.Mod.Cls.MLn.Re8.Tal` | **PRESERVE (canonical)** | Named "Tal Line" — literary anchor on the Czerniak Defence side. Same FEN as sibling. | Rule 1 |
| `E.Ben.Mod.Cls.MLn.Re8.Nd2` | **DELETE** | Same FEN, 0 kids, 0 inbound. Alias is *also* "Tal Line" — the slug is a move-name duplicate of its literary sibling. Identical notes ("Nd2 in the Classical Modern Benoni Czerniak Defence"). | Rule 1 + Rule 3 |

Rank 70 collapses to size 1 after this delete (only `Tal` survives
under `Re8`); the group disappears from the audit's duplicate
report.

### Rank 111 — Benko Accepted Central Storming pair

| slug | action | rationale | rule |
|---|---|---|---|
| `E.Ben.Bnk.Acc.MLn.Bxa6.f4` | **PRESERVE (canonical)** | Bxa6 is the canonical Benko Accepted main move-order at this depth; the f4 push (Central Storming) anchors the literary identity. | Rule 1 |
| `E.Ben.Bnk.Acc.MLn.g6.f4` | **TT → `E.Ben.Bnk.Acc.MLn.Bxa6.f4`** | Same FEN, 0 kids, 0 inbound. Distinct move-order (...g6 before Bxa6) so deletion would lose the breadcrumb. TT preserves the move-order label. | Rule 5 |

`E.Ben.Bnk.Acc.MLn.g6.f4` carries the same alias "Central Storming
Variation" and notes — it is a move-order mirror, not a separate
literary line.

## Summary

**Preserve (no change)**: 3 slugs — `E.Ben.Mod.Cls`,
`E.Ben.Mod.Cls.MLn.Re8.Tal`, `E.Ben.Bnk.Acc.MLn.Bxa6.f4`.

**TT (2 arrows)**:

| from | → | to |
|---|---|---|
| `E.Ben.Mod.Cls.Trd` | → | `E.Ben.Mod.Cls` |
| `E.Ben.Bnk.Acc.MLn.g6.f4` | → | `E.Ben.Bnk.Acc.MLn.Bxa6.f4` |

**DELETE (2 leaves)**:

| slug | reason |
|---|---|
| `E.Ind.e6.Nf3.c5.d5.Be2` | Identical move sequence to `E.Ben.Mod.Cls.Trd`. Pure duplicate descriptor. Lose nothing. |
| `E.Ben.Mod.Cls.MLn.Re8.Nd2` | Move-name slug duplicating its sibling `E.Ben.Mod.Cls.MLn.Re8.Tal` which carries the literary "Tal Line" identity. |

**Notes / alias touches**:

- `E.Ben.Mod.Cls`: existing alias `Classical Variation` is fine. Add
  `Traditional Variation` to aliases so the Lichess label remains
  searchable after `.Trd` is converted to TT (the slug stays but
  becomes a pointer; the alias on the parent ensures lookup still
  finds the canonical).
- `E.Ben.Mod.Cls.Trd`: notes reworded as `Move-order transposition
  to E.Ben.Mod.Cls: same FEN reached via the Nf3 (Anti-Nimzo)
  move order.`
- `E.Ben.Bnk.Acc.MLn.g6.f4`: notes reworded as `Move-order
  transposition to E.Ben.Bnk.Acc.MLn.Bxa6.f4: ...g6-before-Bxa6
  move-order mirror.`

## Expected audit metric impact

|                            | before | after | Δ |
|----------------------------|---|---|---|
| rows totals catàleg        | 5,968 | **5,966** | −2 (2 deletes) |
| duplicate_groups           | 192 | **191** | −1 (rank 70 collapses to size 1) |
| resolved_groups            | 69  | **71** | +2 (rank 1 + rank 111 resolved single_canonical) |
| multiple_canonical_groups  | 2   | **2** | unchanged |
| unresolved_groups          | 123 | **120** | −3 (ranks 1, 70, 111 all leave unresolved) |
| rows_in_groups             | 390 | **387** | −3 |
| rows_in_unresolved_groups  | 248 | **241** | −7 |

Modern Benoni triple disappears from default ranked top. New rank 1
will be the next deferred conceptual group (likely `D.Rub /
A.Col.Zuk` outlier, or the `E.KID.Fch.Kav` intra-E with both kids).

## Risks and open questions

1. **Is "Traditional Variation" a name we want to preserve?** Yes
   — by adding it as an alias on `E.Ben.Mod.Cls`. The label is
   useful for Lichess interop; we just stop treating it as a
   separate slug. The TT on `.Trd` keeps the slug navigable from
   inside the catalog without claiming separate canonical status.

2. **Is `E.Ind.e6.Nf3.c5.d5.Be2` deletion safe?** Verified: leaf,
   0 kids, 0 inbound refs, move sequence identical to `.Trd`. No
   downstream consumer is referencing this slug today. The Anti-Nimzo
   Benoni route is still navigable from `E.Ind.e6.Nf3.c5.d5` via its
   7 other children that cover the depth-6 split points.

3. **Rank 70 deletion**: `.Nd2` and `.Tal` aliases are both "Tal
   Line". The slug name `.Nd2` (describing White's move) is the
   move-name; `.Tal` is the literary attribution. Keeping the
   literary attribution as canonical is consistent with Rule 1.
   Alternative: keep `.Nd2` (move-name structural), delete `.Tal`.
   I recommend `.Tal` survives — the Tal label is the actual
   theoretical name in Benoni literature.

4. **Rank 111 TT direction**: Bxa6.f4 canonical chosen because in
   the Benko Accepted main line, ...Bxa6 is the canonical move
   order (Black recaptures with the bishop). g6 first then Bxa6
   is a "flexible" move order. Either choice is defensible; the
   Bxa6 side has marginally stronger conventional support.

5. **No multiple_canonical here**: the Modern Benoni case
   reinforces that `multiple_canonical` should be reserved for
   genuine two-name positions, not used for any 3-way group. The
   precedent is that the slug content (subtree depth, ECO range,
   note language) decides — not the group size.

## Recommended apply order

When approved:

1. Apply 2 TT + 2 deletions + alias/note touches in one
   `Resolve Modern Benoni transpositions` commit.
2. Update `docs/transpositions.md`:
   - Move Modern Benoni from "Deferred conceptual families" to a
     new "Resolved" section.
   - Note that this case is the **counter-example** to KID
     Classical — three slugs converging on one FEN, but
     single_canonical because two of the three are move-order
     descriptors, not literary identities.
3. Update this proposal doc with `Status: APPLIED`.

No `spec/OCN-1.md` changes needed (the existing arbitration rules
cover this case cleanly).
