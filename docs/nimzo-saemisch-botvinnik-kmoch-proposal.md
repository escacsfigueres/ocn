# Nimzo Sämisch Botvinnik ↔ Kmoch — arbitration proposal

**Status**: PROPOSED (not applied).
**Companion**: builds on `spec/OCN-1.md` → "Canonicalisation
arbitration" and the precedents from the 6 prior `same_as`
applications (Rubinstein, Italian Giuoco/Two Knights, Larsen,
London Classical/Mason, Van Geet/Van't Kruijs, QGA Flohr/Janowski).

## Context

After applying QGA Flohr/Janowski-Haberditz (commit `5037eef`),
the highest-leverage unresolved group at score 5 inside E-class is
a single 2-row pair under the Nimzo-Indian Sämisch root:

```
rank 2:  E.Nim.Sml.Bot       ⇄ E.Nim.Sml.Kmo
```

Both reach the same FEN
`rnbqk2r/pp3ppp/4pn2/2pp4/2PP4/P1P2P2/4P1PP/R1BQKBNR w KQkq -`
(Sämisch Nimzo after the doubled c-pawns structure with `...c5` and
`...d5` both played, before either side plays `e3`):

- **Bot** move order: `1.d4 Nf6 2.c4 e6 3.Nc3 Bb4 4.f3 d5 5.a3 Bxc3+ 6.bxc3 c5` — `f3` *before* `a3`.
- **Kmo** move order: `1.d4 Nf6 2.c4 e6 3.Nc3 Bb4 4.a3 Bxc3+ 6.bxc3 c5 6.f3 d5` — `a3` first, `f3` deferred.

This is a pure move-order transposition. The only thing that differs
in OCN is which player-name appears at the depth-3 alias.

This is a candidate for bilateral `same_as` and represents the
**cleanest precedent so far**: both slugs are direct depth-3 children
of the same family parent (`E.Nim.Sml`), both have player-name
literary aliases, both have subtrees of their own, and the existing
catalogue already has a co-canonical pair one level deeper
(`E.Nim.Sml.Bot.MLn ↔ E.Nim.Rub.Kmo`) that demonstrates the
Sämisch/Rubinstein-Kmoch ↔ Sämisch-Botvinnik correspondence is
already recognised in OCN at depth 4.

## FEN group in scope (1 group)

| rank | size | classes | slugs |
|---|---|---|---|
| 2 | 2 | E | `E.Nim.Sml.Bot`, `E.Nim.Sml.Kmo` |

No related FEN duplicates appear in the top 100 beyond this single
pair. The Bot and Kmo subtrees diverge from this point — Bot has 3
children (`MLn`, `cxd5`, `Rom`), Kmo has 1 child (`MLn`). All
child FENs are distinct (Bot.MLn has `e3 O-O` played; Kmo.MLn has
only `e3`; Bot.cxd5 has the cxd5 capture; Bot.Rom has the
Romanovsky `...f5`).

## Subtree shape

```
E.Nim.Sml                           "Nimzo, Sämisch"           depth 2, E25-E29, parent E.Nim
├── E.Nim.Sml.Bot                   "Nimzo Sämisch, Botvinnik" depth 3, E24/E25  ← rank 2 twin
│   ├── E.Nim.Sml.Bot.MLn           "Botvinnik Main Line"      depth 4, E25
│   │   │  same_as = E.Nim.Rub.Kmo  (already co-canonical with Rubinstein-Kmoch, depth 4)
│   │   ├── E.Nim.Sml.Bot.MLn.Bd3
│   │   │   └── E.Nim.Sml.Bot.MLn.Bd3.Nc6
│   │   └── E.Nim.Sml.Bot.MLn.Nxd5
│   ├── E.Nim.Sml.Bot.cxd5
│   │   └── E.Nim.Sml.Bot.cxd5.Nxd5
│   │       └── E.Nim.Sml.Bot.cxd5.Nxd5.dxc5  "Keres Variation"
│   └── E.Nim.Sml.Bot.Rom           "Romanovsky Variation"
├── E.Nim.Sml.Kmo                   "Nimzo Saemisch, Kmoch"    depth 3, E26    ← rank 2 twin
│   └── E.Nim.Sml.Kmo.MLn           "Kmoch Main Line"          depth 4, E26 (leaf, +e3)
├── E.Nim.Sml.OKe                   "Nimzo Saemisch, O'Kelly"  depth 3, E26    (different FEN: ...b6)
└── E.Nim.Sml.Bxc3                  "Bxc3 Line"                depth 3 (structural prefix without Bot/Kmo divergence)
    └── E.Nim.Sml.Bxc3.bxc3
        └── E.Nim.Sml.Bxc3.bxc3.O-O
```

Two genuine player-named identities converge at the depth-3 FEN
under the Sämisch root:

- **Botvinnik Variation** (`E.Nim.Sml.Bot`, ECO E24/E25) — named
  after Mikhail Botvinnik (World Champion 1948-63), who explored
  this structure extensively in the Soviet tradition.
- **Kmoch Variation** (`E.Nim.Sml.Kmo`, ECO E26) — named after
  Hans Kmoch (Austrian-American IM, author of *Pawn Power in
  Chess*, who codified analysis of this f3/d5 structure).

## Conceptual analysis — are both real?

**Yes**, and this is the most symmetric `same_as` candidate
processed so far. Both are direct depth-3 children of the same
family parent (`E.Nim.Sml`), both have player-name literary
aliases, both have catalogued subtrees.

| feature | E.Nim.Sml.Bot | E.Nim.Sml.Kmo |
|---|---|---|
| Slug carries player-name alias | "Botvinnik Variation" | "Kmoch Variation" |
| Parent literary identity | `E.Nim.Sml` (Sämisch, depth 2) | `E.Nim.Sml` (Sämisch, depth 2) |
| Depth from literary family root | **1** | **1** |
| ECO assignment on the slug | E24/E25 | E26 |
| Direct children | 3 (MLn, cxd5, Rom) | 1 (MLn) |
| Indirect descendants | 6 (.MLn.Bd3, .MLn.Bd3.Nc6, .MLn.Nxd5, .cxd5.Nxd5, .cxd5.Nxd5.dxc5, .Bot.MLn.same_as cross-link) | 1 |
| Pre-existing same_as on subtree | yes (`.MLn` ↔ `E.Nim.Rub.Kmo`) | no |

Botvinnik's subtree is more developed (4× the descendants of
Kmoch), but this is a quantitative difference, not a qualitative
one. Kmoch's name is firmly attached in ECO and literature
(E26 is the Kmoch Variation, full stop — not a Lichess descriptor,
not a structural breadcrumb). Pawn structure analysis in the f3/d5
Sämisch traces directly to Kmoch's *Pawn Power*.

Compare with the 6 prior `same_as` cases:

| case | both literary? | sub-pattern |
|---|---|---|
| Rubinstein ⇄ Colle-Zukertort | yes | depth 1 vs depth 2, both family-root literary |
| Italian Giuoco ⇄ Two Knights | yes | both named family children of C.Ita |
| Larsen ⇄ Reti Nimzowitsch-Larsen | yes | both depth 3 under named family parents |
| London Classical ⇄ Mason | yes | both depth 3-4 under named family parents, cascade |
| Van Geet ⇄ Van't Kruijs | yes (2 of 3) | mixed, third was structural breadcrumb |
| QGA Flohr ⇄ Haberditz | yes | Flohr at family-root, Haberditz at leaf-with-literary-alias |
| **Nimzo Sml Bot ⇄ Kmo** | **yes** | **two player-name siblings under same family root, symmetric depth** |

**This is the cleanest pattern of all seven**: not only are both
names literary (as in Larsen and QGA), but both occupy the
*structurally identical position* under the same parent — they
are true siblings, only differing in subtree elaboration.

The strongest piece of supporting evidence is internal: OCN
**already** treats Sämisch-Botvinnik and Rubinstein-Kmoch as
co-canonical at depth 4 (the `.MLn ↔ E.Nim.Rub.Kmo` link). It
would be inconsistent to acknowledge the Bot/Kmoch convergence
under Rubinstein at depth 4 but leave the *same* convergence
unmarked one move earlier within the Sämisch tree itself.

## Options considered

### Option A — `same_as` bilateral (RECOMMENDED)

```
E.Nim.Sml.Bot.same_as       = E.Nim.Sml.Kmo
E.Nim.Sml.Kmo.same_as       = E.Nim.Sml.Bot
```

Both preserved as canonicals. Audit reports +1 multi_canonical,
−1 unresolved. No deletions, no transposes_to, no reparenting,
no cascade into children.

- **Pro**: preserves both player-name literary identities.
- **Pro**: mirrors the existing internal precedent at depth 4
  (`E.Nim.Sml.Bot.MLn ↔ E.Nim.Rub.Kmo`) and externalises that
  recognition one level earlier where it belongs.
- **Pro**: most symmetric `same_as` to date — both at the same
  depth from the same family parent. No structural asymmetry to
  document.
- **Pro**: zero cascade. Children of Bot and Kmo do not share
  FENs (different prefixes / different added moves).
- **Pro**: no schema work, no policy change, single pair.
- **Con**: none material.

### Option B — Single canonical `E.Nim.Sml.Bot`

`E.Nim.Sml.Kmo.transposes_to = E.Nim.Sml.Bot`

- **Pro**: Botvinnik is the more famous player (World Champion).
  Bot subtree is more developed (3 children vs 1).
- **Con**: **erases Kmoch as a literary identity**. ECO E26 is
  specifically "Kmoch Variation" — not "Botvinnik via Kmoch order".
  Marking it as a transposition misrepresents its standing.
- **Con**: would force the existing `.MLn ↔ E.Nim.Rub.Kmo`
  precedent to look inconsistent (Bot.MLn is co-canonical with a
  Kmoch-named slug at depth 4, yet Kmo at depth 3 was deleted).

### Option C — Single canonical `E.Nim.Sml.Kmo`

`E.Nim.Sml.Bot.transposes_to = E.Nim.Sml.Kmo`

- **Con**: would erase Botvinnik and orphan three named child
  subtrees (Bot.MLn — which itself carries a same_as cross-link —
  plus Bot.cxd5 and Bot.Rom). Symmetrically bad.

### Option D — Defer

- **Con**: structural analysis is unambiguous. Both slugs are
  player-named, both have children, and OCN already accepts the
  same correspondence at depth 4. `same_as` exists for exactly
  this case.

## Recommendation: **Option A** (bilateral `same_as`)

### Per-slug actions

| slug | action | rationale | rule |
|---|---|---|---|
| `E.Nim.Sml.Bot` | **PRESERVE (canonical)**, add `same_as = E.Nim.Sml.Kmo` | Botvinnik Variation — depth-3 player-name sibling under the Sämisch family root. | Rule 4 |
| `E.Nim.Sml.Kmo` | **PRESERVE (canonical)**, add `same_as = E.Nim.Sml.Bot` | Kmoch Variation — depth-3 player-name sibling under the Sämisch family root (ECO E26). | Rule 4 |

### Notes to add (cross-references)

- `E.Nim.Sml.Bot.notes`:
  `Saemisch Nimzo structure with f3/a3 and ...c5. Co-canonical
  with E.Nim.Sml.Kmo (Kmoch Variation, ECO E26) — same FEN via
  the Kmoch move order (a3 before f3).`

- `E.Nim.Sml.Kmo.notes`:
  `f3 and ...d5 against the Saemisch structure. Co-canonical
  with E.Nim.Sml.Bot (Botvinnik Variation, ECO E24/E25) — same
  FEN via the Botvinnik move order (f3 before a3).`

No alias changes (each slug's existing alias accurately reflects
its player-name identity).

## Summary

**Preserve (no canonicality change)**: 2 slugs.

**`same_as` (2 declarations, 1 bilateral pair)**:

| slug | same_as |
|---|---|
| `E.Nim.Sml.Bot` | `E.Nim.Sml.Kmo` |
| `E.Nim.Sml.Kmo` | `E.Nim.Sml.Bot` |

**`transposes_to`**: 0. **Deletions**: 0. **Reparenting**: 0.

## Expected audit metric impact

|                            | before | after | Δ |
|----------------------------|---|---|---|
| rows totals catàleg        | 5,905 | 5,905 | 0 |
| duplicate_groups           | 130 | 130 | 0 |
| resolved_groups            | 99 | **100** | **+1** |
| multiple_canonical_groups  | 12 | **13** | **+1** |
| unresolved_groups          | 31 | **30** | **−1** |
| rows_in_unresolved_groups  | 62 | **60** | **−2** |

The rank-2 group disappears from the default ranked report;
visible only under `--include-resolved` with
`resolution_kind=multiple_canonical`.

## Risks and open questions

1. **Cross-subtree implications** with the existing
   `E.Nim.Sml.Bot.MLn ↔ E.Nim.Rub.Kmo` same_as link. After
   applying this proposal:
   - `E.Nim.Sml.Bot.same_as = E.Nim.Sml.Kmo` (at depth 3)
   - `E.Nim.Sml.Bot.MLn.same_as = E.Nim.Rub.Kmo` (at depth 4)
   These do **not** form a chain, transitive relationship, or
   conflict — they live at different FENs (different positions)
   and OCN does not auto-propagate `same_as` through parent-child
   links. Each is a position-local declaration. The validator
   does not require closure or transitivity, only that targets
   exist and share the FEN at the same position. ✓ safe.

2. **Asymmetric subtree depth/size**. Bot has 3 children, Kmo has
   1. Not a disqualifier — Rubinstein/Colle-Zukertort had similar
   structural asymmetry (Rubinstein has multiple children; the
   Colle-Zukertort branch is much smaller) and worked cleanly.
   `same_as` is a position-level statement, not a subtree merge.

3. **ECO asymmetry** (E24/E25 for Bot vs E26 for Kmo). Both ECO
   codes are real and well-attested. The split exists in published
   ECO because the move order distinguishes them; OCN's `same_as`
   acknowledges position equivalence without erasing the ECO split.

4. **Single-pair, no cascade** — easier than London or Italian.
   Easier than Larsen (which required noting the Réti-Nimzowitsch
   asymmetric naming). Easier than Van Geet (mixed Option D with
   structural breadcrumb). Easier than QGA Flohr (asymmetric depth).
   **This is the simplest `same_as` proposal in the series.**

## Recommended apply order

When approved (single commit):

1. Set `E.Nim.Sml.Bot.same_as = E.Nim.Sml.Kmo`.
2. Set `E.Nim.Sml.Kmo.same_as = E.Nim.Sml.Bot`.
3. Update both notes with the cross-references shown above.
4. Update `docs/transpositions.md`:
   - Move Nimzo Sml Bot/Kmo to the same_as-resolved table.
   - Bump multi-canonical count to 13.
5. Mark this proposal `Status: APPLIED`.

Validation suite: standard. Expected commit shape: 2 catalogue
rows touched (4 / 4 line diff with notes), 1 doc update. No row
count change.
