# Budapest Adler ↔ Rubinstein — arbitration proposal

**Status**: PROPOSED (not applied).
**Companion**: builds on `spec/OCN-1.md` → "Canonicalisation
arbitration" and the precedents from the prior `same_as`
applications (Rubinstein/Colle-Zukertort, Italian Giuoco/Two
Knights, Larsen, London Classical/Mason, Van Geet/Van't Kruijs,
QGA Flohr/Janowski). Closest precedent: **London Classical/Mason**
(a multi-level same_as cascade between two real player-named
variations).

## Context

After the parent-child cleanup batch (commit `f22115a`), the
highest remaining structured group is a 3-level cascade in the
Budapest Gambit, where the **Adler Variation** (4.Nf3 move order)
and the **Rubinstein Variation** (4.Bf4 move order) converge to the
same FEN once both knight-and-bishop developing moves are played:

```
rank 12:  E.Bud.Adl.MLn          ⇄ E.Bud.Rub.MLn          (depth 3)
rank 11:  E.Bud.Adl.MLn.e3       ⇄ E.Bud.Rub.MLn.e3       (depth 4)
rank 10:  E.Bud.Adl.MLn.e3.Be2   ⇄ E.Bud.Rub.MLn.e3.Be2   (depth 5)
```

The two names attach to White's **4th-move choice** in the
3...Ng4 Budapest:

- **Adler Variation** (`E.Bud.Adl`, A52) — `4.Nf3` (develop the knight first).
- **Rubinstein Variation** (`E.Bud.Rub`, A52) — `4.Bf4` (develop the bishop first, holding the e5 pawn).

At depth 2 these are **genuinely different positions** (one has
Nf3 played, the other Bf4) and are correctly kept separate. They
**only converge** once both Nf3 and Bf4 appear, i.e. at the main
line after `...Nc6` and `...Bb4`:

- **Adler main line**: `1.d4 Nf6 2.c4 e5 3.dxe5 Ng4 4.Nf3 Nc6 5.Bf4 Bb4` (Nf3 before Bf4).
- **Rubinstein main line**: `1.d4 Nf6 2.c4 e5 3.dxe5 Ng4 4.Bf4 Nc6 5.Nf3 Bb4` (Bf4 before Nf3).

Both reach `r1bqk2r/pppp1ppp/2n5/4P3/1bP2Bn1/5N2/PP2PPPP/RN1QKB1R w KQkq -`,
then stay converged through `e3` (Nbd2/O-O) and `Be2`.

## FEN groups in scope (3 groups, exact match confirmed)

FEN-collision sweep across the entire 31-slug `E.Bud` subtree
returns **exactly 3 collision groups**, all on the Adler/Rubinstein
main-line cascade:

| rank | depth | FEN (piece-placement + side + castling + ep) | slugs |
|---|---|---|---|
| 12 | 3 | `r1bqk2r/pppp1ppp/2n5/4P3/1bP2Bn1/5N2/PP2PPPP/RN1QKB1R w KQkq -` | `E.Bud.Adl.MLn`, `E.Bud.Rub.MLn` |
| 11 | 4 | `r1bq1rk1/pppp1ppp/2n5/4P3/1bP2Bn1/4PN2/PP1N1PPP/R2QKB1R b KQ -` | `E.Bud.Adl.MLn.e3`, `E.Bud.Rub.MLn.e3` |
| 10 | 5 | `r1bq1rk1/ppp2ppp/2np4/4P3/1bP2Bn1/4PN2/PP1NBPPP/R2QK2R b KQ -` | `E.Bud.Adl.MLn.e3.Be2`, `E.Bud.Rub.MLn.e3.Be2` |

No other `E.Bud` collisions exist. The depth-2 roots
(`E.Bud.Adl` 4.Nf3 vs `E.Bud.Rub` 4.Bf4) do **not** collide, nor
do the `.Nc6` side branches, nor the Adler-only `.Re8` leaf.

## Subtree shape

```
E.Bud                                "Budapest Defence"        depth 1, A51/A52
├── E.Bud.Adl                        "Adler Variation"         depth 2, A52  (4.Nf3 — NOT in cascade)
│   ├── E.Bud.Adl.MLn                "Adler Main Line"         depth 3   ← cascade L1 twin
│   │   └── E.Bud.Adl.MLn.e3         "e3 Line"                 depth 4   ← cascade L2 twin
│   │       └── E.Bud.Adl.MLn.e3.Be2 "Be2 Line"               depth 5   ← cascade L3 twin
│   │           └── E.Bud.Adl.MLn.e3.Be2.Re8  "Re8 Line"      depth 6   (Adler-only, no twin)
│   └── E.Bud.Adl.Nc6               "Nc6 Line"                 depth 3   (4.Nf3 Nc6, no Bf4 — no twin)
├── E.Bud.Rub                        "Rubinstein Variation"    depth 2, A52  (4.Bf4 — NOT in cascade)
│   ├── E.Bud.Rub.MLn                "Rubinstein Main Line"    depth 3   ← cascade L1 twin
│   │   └── E.Bud.Rub.MLn.e3         "e3 Line"                 depth 4   ← cascade L2 twin
│   │       └── E.Bud.Rub.MLn.e3.Be2 "Be2 Line"               depth 5   ← cascade L3 twin (leaf)
│   ├── E.Bud.Rub.Nc6               "Nc6 Line"                 depth 3   (4.Bf4 Nc6 — no twin)
│   │   └── E.Bud.Rub.Nc6.Nf3       "Nf3 Line"                 depth 4   (Bf4 Nc6 Nf3, no Bb4 — no twin)
├── E.Bud.Alk                        "Alekhine Variation"      depth 2, A52  (4.e4)
├── E.Bud.Faj                        "Fajarowicz Variation"    depth 2, A51  (3...Ne4)
└── E.Bud.Ng4 / E.Bud.Faj.* …        (other branches)
```

Both cascade sides carry **parallel literary subtrees** down to
`.Be2`. The Adler side extends one level further (`.Re8`); the
Rubinstein side stops at `.Be2` (leaf). The non-cascade branches
(`.Nc6`, `.Re8`, the depth-2 roots) are untouched.

## Conceptual analysis — are both real?

**Yes.** Both are established player-named variations in Budapest
Gambit theory, both ECO A52, both with their own catalogue
subtrees:

- **Rubinstein Variation** (`4.Bf4`) — Akiba Rubinstein's
  contribution; the **most prominent** Budapest main line, holding
  the extra e5 pawn. Universally recognised.
- **Adler Variation** (`4.Nf3`) — the knight-first development
  route. A secondary but genuine attribution (not a Lichess
  descriptor); the catalogue gives it a full parallel subtree.

| feature | E.Bud.Adl.MLn | E.Bud.Rub.MLn |
|---|---|---|
| Player-name alias | "Adler" (via parent `E.Bud.Adl`) | "Rubinstein" (via parent `E.Bud.Rub`) |
| Move-order signature | Nf3 before Bf4 | Bf4 before Nf3 |
| Depth from family root | 1 (under `E.Bud.Adl`) | 1 (under `E.Bud.Rub`) |
| ECO | A52 | A52 |
| Parallel subtree | MLn → e3 → Be2 → Re8 | MLn → e3 → Be2 |
| Prominence in literature | secondary | primary |

The **asymmetry of prominence** (Rubinstein is the better-known
name) mirrors the QGA Flohr/Haberditz case (Flohr more prominent
than Haberditz) and the Rubinstein/Colle-Zukertort case — and did
not disqualify `same_as` there. What matters for `same_as` is that
**both names are genuine literary attributions**, which they are.

Compare with the prior `same_as` cases:

| case | both literary? | cascade depth | sub-pattern |
|---|---|---|---|
| Rubinstein ⇄ Colle-Zukertort | yes | 1 | depth 1 vs 2 |
| Italian Giuoco ⇄ Two Knights | yes | 2 | castling convergence cascade |
| Larsen ⇄ Reti Nimzowitsch-Larsen | yes | 1 | single pair |
| London Classical ⇄ Mason | yes | 2 | `.MLn` + `.c4` cascade |
| Van Geet ⇄ Van't Kruijs | yes (2 of 3) | 2 | mixed |
| QGA Flohr ⇄ Haberditz | yes | 1 | single pair, asymmetric depth |
| **Budapest Adler ⇄ Rubinstein** | **yes** | **3** | **deepest cascade so far; symmetric depth, parallel subtrees** |

This is the **deepest same_as cascade to date** (3 levels), but
structurally the cleanest kind: two player-named move-order routes
into the same tabiya, symmetric depth, parallel subtrees, no
mechanical descriptors, **no internal naming conflict** (unlike
Nimzo Bot/Kmo, there is no rival `E.Bud.*` slug claiming either
name).

## Internal consistency check (the Nimzo lesson)

The Nimzo Bot/Kmo sprint was put ON HOLD because the catalogue
**already** carried the "Kmoch" name at a different slug
(`E.Nim.Fou`, 4.f3). For Budapest, a deliberate check was run:

- "Adler" appears **only** at `E.Bud.Adl*` — no rival placement.
- "Rubinstein" appears at `E.Bud.Rub*` within Budapest; the other
  catalogue "Rubinstein" slugs (`E.Nim.Rub`, `A.Eng.Sym.Rub`,
  `C.Fou.Spa.Rub`, …) are **different openings** (the surname is
  reused across many openings, which is normal and not a conflict).

There is **no internal disagreement** about where Adler or
Rubinstein live in the Budapest. This case does **not** have the
problem that blocked Nimzo.

## Options considered

### Option A — `same_as` bilateral cascade (RECOMMENDED)

Three bilateral pairs (6 declarations):

```
E.Bud.Adl.MLn.same_as          = E.Bud.Rub.MLn
E.Bud.Rub.MLn.same_as          = E.Bud.Adl.MLn
E.Bud.Adl.MLn.e3.same_as       = E.Bud.Rub.MLn.e3
E.Bud.Rub.MLn.e3.same_as       = E.Bud.Adl.MLn.e3
E.Bud.Adl.MLn.e3.Be2.same_as   = E.Bud.Rub.MLn.e3.Be2
E.Bud.Rub.MLn.e3.Be2.same_as   = E.Bud.Adl.MLn.e3.Be2
```

Both preserved as canonicals at all 3 levels. Audit reports
+3 multiple_canonical, −3 unresolved. No deletions, no
transposes_to, no reparenting.

- **Pro**: preserves both real player names at every level.
- **Pro**: direct precedent — the London Classical/Mason cascade
  resolved the identical shape (two named variations converging
  across multiple levels) bilaterally.
- **Pro**: no internal naming conflict (Nimzo lesson cleared).
- **Pro**: symmetric depth, parallel subtrees — the cleanest
  cascade structurally.
- **Con**: 3 pairs (6 declarations) — more edits than a single
  pair, but mechanically identical to London.

### Option B — Single canonical Adler (Rubinstein → TT)

- **Con**: erases Rubinstein, the **more prominent** name. Backwards.

### Option C — Single canonical Rubinstein (Adler → TT)

`E.Bud.Adl.MLn.transposes_to = E.Bud.Rub.MLn` (and cascade).

- **Pro**: Rubinstein (4.Bf4) is the dominant Budapest main line;
  the Adler (4.Nf3) route arguably transposes *into* the Rubinstein
  tabiya.
- **Con**: erases "Adler" as a literary identity and would
  **orphan the Adler subtree** (`.Re8` leaf hangs under a TT node).
  Adler is a real attribution with a full parallel subtree, not a
  mechanical descriptor — demoting it loses information.
- **Con**: inconsistent with the project's handling of Larsen,
  London, QGA, where the secondary name was preserved via `same_as`
  rather than demoted.

### Option D — Defer

- **Con**: unlike Nimzo Bot/Kmo, there is no naming ambiguity or
  internal conflict here. Both names are cleanly attributed, the
  FEN cascade is exact, and the precedent (London) is direct.
  Nothing to research.

## Recommendation: **Option A** (bilateral `same_as` cascade, 3 pairs)

### Per-slug actions

| slug | name | has_children | proposed_action | rationale | rule |
|---|---|---|---|---|---|
| `E.Bud.Adl.MLn` | Adler Main Line | yes (`.e3`) | PRESERVE, `same_as = E.Bud.Rub.MLn` | Adler 4.Nf3 route, real name, parallel subtree | Rule 4 |
| `E.Bud.Rub.MLn` | Rubinstein Main Line | yes (`.e3`) | PRESERVE, `same_as = E.Bud.Adl.MLn` | Rubinstein 4.Bf4 route, primary Budapest name | Rule 4 |
| `E.Bud.Adl.MLn.e3` | Adler e3 Line | yes (`.Be2`) | PRESERVE, `same_as = E.Bud.Rub.MLn.e3` | cascade level 2, Adler side | Rule 4 |
| `E.Bud.Rub.MLn.e3` | Rubinstein e3 Line | yes (`.Be2`) | PRESERVE, `same_as = E.Bud.Adl.MLn.e3` | cascade level 2, Rubinstein side | Rule 4 |
| `E.Bud.Adl.MLn.e3.Be2` | Adler Be2 Line | yes (`.Re8`) | PRESERVE, `same_as = E.Bud.Rub.MLn.e3.Be2` | cascade level 3, Adler side | Rule 4 |
| `E.Bud.Rub.MLn.e3.Be2` | Rubinstein Be2 Line | no (leaf) | PRESERVE, `same_as = E.Bud.Adl.MLn.e3.Be2` | cascade level 3, Rubinstein side | Rule 4 |

### Notes to add (cross-references, one pair shown; same pattern at each level)

- `E.Bud.Adl.MLn.notes`: `...Bb4 in the Adler Budapest (4.Nf3 move
  order). Co-canonical with E.Bud.Rub.MLn (Rubinstein Variation,
  4.Bf4 move order) — same FEN, both A52.`
- `E.Bud.Rub.MLn.notes`: `...Bb4 in the Rubinstein Budapest (4.Bf4
  move order). Co-canonical with E.Bud.Adl.MLn (Adler Variation,
  4.Nf3 move order) — same FEN, both A52.`

(Analogous cross-reference notes at the `.e3` and `.e3.Be2` levels.)

No alias changes (each slug's alias accurately reflects its
move-order identity).

## Summary

**Preserve (no canonicality change)**: 6 slugs.

**`same_as` (6 declarations, 3 bilateral pairs)**:

| level | pair |
|---|---|
| L1 (depth 3) | `E.Bud.Adl.MLn` ⇄ `E.Bud.Rub.MLn` |
| L2 (depth 4) | `E.Bud.Adl.MLn.e3` ⇄ `E.Bud.Rub.MLn.e3` |
| L3 (depth 5) | `E.Bud.Adl.MLn.e3.Be2` ⇄ `E.Bud.Rub.MLn.e3.Be2` |

**`transposes_to`**: 0. **Deletions**: 0. **Reparenting**: 0.

## Expected audit metric impact

|                            | before | after | Δ |
|----------------------------|---|---|---|
| rows totals catàleg        | 5,902 | 5,902 | 0 |
| duplicate_groups           | 127 | 127 | 0 |
| resolved_groups            | 104 | **107** | **+3** |
| multiple_canonical_groups  | 12 | **15** | **+3** |
| unresolved_groups          | 23 | **20** | **−3** |
| rows_in_unresolved_groups  | 46 | **40** | **−6** |

The three cascade groups disappear from the default ranked report;
visible only under `--include-resolved` with
`resolution_kind=multiple_canonical`.

## Risks and open questions

1. **Prominence asymmetry** (Rubinstein primary, Adler secondary).
   Not a disqualifier — the project consistently preserves the
   secondary name via `same_as` when it is a genuine attribution
   (Flohr/Haberditz, Rubinstein/Colle-Zukertort). Adler has a full
   parallel subtree, confirming editorial intent to treat it as a
   named line.

2. **Cascade depth (3 levels)** — deepest so far. But mechanically
   identical to the London Classical/Mason 2-level cascade, just
   one level longer. No new schema or policy needed.

3. **Adler-only `.Re8` leaf** — `E.Bud.Adl.MLn.e3.Be2.Re8` extends
   one level beyond the Rubinstein side. It is **not** part of the
   cascade (no Rubinstein twin) and is left untouched. After
   applying same_as at `.Be2`, the `.Re8` child remains a normal
   descendant of the (still canonical) Adler `.Be2` slug.

4. **No multi-target `same_as` needed** — each FEN has exactly 2
   slugs, so all 3 pairs are simple bilateral (N=1). The N=2
   pipe-separated form is still unused.

## Recommended apply order

When approved (single commit):

1. Add the 6 `same_as` declarations (3 bilateral pairs).
2. Add cross-reference notes on all 6 slugs.
3. Update `docs/transpositions.md`:
   - Move Budapest Adler/Rubinstein to the same_as-resolved table
     (3 cascade rows).
   - Bump multi-canonical count to 15.
4. Mark this proposal `Status: APPLIED`.

Validation suite: standard. Expected commit shape: 6 catalogue
rows touched (12-line diff with notes), 1 doc update. No row count
change.
