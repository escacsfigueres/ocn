# Nimzo Sämisch Botvinnik ↔ Kmoch — arbitration proposal

**Status**: **ON HOLD — naming review pending**.

The original conclusion (bilateral `same_as`, Option A) was a clean
move-order resolution at the FEN level. A user challenge raised
during review showed that the *attribution* of the slug names to
chess history may not be consistent with how modern opening
databases (365Chess, Chess.com, and OCN's own `E.Nim.Fou` alias)
label the "Kmoch" name. Before applying any `same_as`, the slug
attributions need to be verified against authoritative sources.

**Companion**: builds on `spec/OCN-1.md` → "Canonicalisation
arbitration" and the precedents from the 6 prior `same_as`
applications. Differs from those precedents: this is the first
proposal where the **terminology** of the slug labels is itself
in question.

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
`...d5` both played, before either side plays `e3`) via different
move orders:

- **Bot** move order: `1.d4 Nf6 2.c4 e6 3.Nc3 Bb4 4.f3 d5 5.a3 Bxc3+ 6.bxc3 c5` — `f3` *before* `a3`.
- **Kmo** move order: `1.d4 Nf6 2.c4 e6 3.Nc3 Bb4 4.a3 Bxc3+ 5.bxc3 c5 6.f3 d5` — `a3` first, `f3` deferred.

This *position* is a pure move-order transposition. The question
the user has raised is not about the position but about the
**names attached to the two move-order paths**.

## Naming correction / user challenge

### The user's observation

The user noted that in standard chess opening references the
**Kmoch Variation** of the Nimzo-Indian refers specifically to the
early `4.f3` move (independent of the Sämisch `4.a3` structure):

- **365Chess**: "Nimzo-Indian, Kmoch variation" = `1.d4 Nf6 2.c4 e6 3.Nc3 Bb4 4.f3`
- **Chess.com**: "Nimzo-Indian Defense: Kmoch Variation, 4.f3 d5 5.a3 Bxc3+ 6.bxc3"

If that is the canonical literary attribution, then OCN's
`E.Nim.Sml.Bot` (whose move order starts with `4.f3`) would more
naturally carry the *Kmoch* label, and `E.Nim.Sml.Kmo` (whose move
order starts with `4.a3` and reaches the same FEN via `6.f3` later)
would not be Kmoch in the modern sense at all.

### Catalogue finding — `E.Nim.Fou` already carries "Kmoch Variation"

Verification against the existing catalogue **confirms the user's
intuition is well-grounded**. The catalogue already has a dedicated
4.f3 slug at depth 2 with the Kmoch alias:

```
E.Nim.Fou  "Nimzo, 4.f3"  E20  aliases=Kmoch Variation|4.f3 System
              moves = d2d4 g8f6 c2c4 e7e6 b1c3 f8b4 f2f3
```

with children:

```
E.Nim.Fou.MLn       "Nimzo 4.f3, Main Line"   E20  (after 4.f3 d5)
E.Nim.Fou.MLn.e4    "Nimzo 4.f3 Main Line, e4" E20 (after 4.f3 d5 e4)
```

OCN therefore **already canonically locates the Kmoch name at the
4.f3 depth-2 slug**, consistent with 365Chess and Chess.com. The
depth-3 `E.Nim.Sml.Kmo` slug is a *second*, possibly Lichess-derived,
use of the "Kmoch" label at a different position.

### Two competing literary frames

After deeper review, the chess-historical truth is genuinely
double-attributed at the depth-3 FEN in question:

| Frame | What it says |
|---|---|
| **Move-naming convention** (365Chess, Chess.com, OCN's `E.Nim.Fou`) | "Kmoch" = the 4.f3 move (depth 2). The depth-3 doubled-pawn FEN reached by `4.a3 + later f3` is just "Sämisch Main Line" or "Sämisch with f3/c5/d5". |
| **Structural-analysis convention** (some opening databases, possibly Lichess) | "Kmoch Variation" = the resulting pawn structure (f3 + c5 + d5 with doubled c-pawns), regardless of move order. Under this frame, the depth-3 FEN itself IS "Kmoch" because Kmoch's pawn-structure analysis applies. |
| **Botvinnik attribution** | Botvinnik analysed the SAME depth-3 structure deeply (especially in the post-WWII Soviet school). Some sources call it the "Botvinnik Variation" of the Sämisch. |

Under the first frame, the catalogue's `E.Nim.Sml.Kmo` is a
**naming mistake** — the slug name should not borrow "Kmoch" if
that label canonically lives at `E.Nim.Fou`. Under the second/third
frame, both names co-exist legitimately, and `same_as` is the
correct treatment.

### Why this matters for the same_as decision

The proposed bilateral `same_as` would *bake the current naming
into the catalogue contract*. Consumers reading
`E.Nim.Sml.Bot.same_as = E.Nim.Sml.Kmo` would interpret this as:
"Sämisch-Botvinnik and Sämisch-Kmoch are co-canonical at this FEN."
If the catalogue has the names backwards or mis-attributed, the
`same_as` declaration propagates that error and makes it harder to
fix later (downstream consumers like `chess-parquet` would already
have pinned the relationship).

**Therefore: resolve naming first, then decide on `same_as`.**

## FEN group in scope (1 group)

| rank | size | classes | slugs |
|---|---|---|---|
| 2 | 2 | E | `E.Nim.Sml.Bot`, `E.Nim.Sml.Kmo` |

Confirmed by FEN-exact match: only these two catalogue rows hit
this FEN. `E.Nim.Fou.*` subtree never reaches it (4.f3 family
stays at shallower positions before `...c5` is played).

## Subtree shape (unchanged from original analysis)

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
└── E.Nim.Sml.Bxc3                  "Bxc3 Line"                depth 3 (structural prefix)
    └── E.Nim.Sml.Bxc3.bxc3
        └── E.Nim.Sml.Bxc3.bxc3.O-O
```

And the now-relevant separate Kmoch home in the catalogue:

```
E.Nim.Fou                           "Nimzo, 4.f3"              depth 2, E20, aliases=Kmoch Variation|4.f3 System
├── E.Nim.Fou.MLn                   "Nimzo 4.f3, Main Line"    depth 3, E20
└── E.Nim.Fou.MLn.e4                "Nimzo 4.f3 Main Line, e4" depth 4, E20
```

## Internal consistency observation

The catalogue **already encodes** the structural-analysis frame at
depth 4 via the existing same_as link:

```
E.Nim.Sml.Bot.MLn  ←→  E.Nim.Rub.Kmo
   (E25, depth 4)        (E40, depth 3 under Rubinstein, with f3 added at move 5)
```

Both have f3/a3/Bxc3/bxc3/c5/d5/e3 played. The OCN catalogue treats
`E.Nim.Sml.Bot.MLn` (Sämisch-Botvinnik label) and `E.Nim.Rub.Kmo`
(Rubinstein-Kmoch label) as co-canonical for the same FEN. This
internal precedent **supports the bilateral-same_as approach** —
provided the underlying slug names are accurate. If `E.Nim.Sml.Kmo`
is mis-attributed, however, then the existing `Bot.MLn ↔ Rub.Kmo`
link is also worth re-examining (different FEN, but same naming
question).

## Options considered (re-ranked under the naming challenge)

### Option D — Defer (RECOMMENDED, NEW)

Do not apply any `same_as`. First conduct a **naming review sprint**:

1. Verify against authoritative sources:
   - Lichess opening database export (which name does it use for the depth-3 FEN?)
   - ECO official codes E24/E25/E26 attribution (Encyclopaedia of Chess Openings)
   - NCO (Nunn's Chess Openings) attribution
   - Wikipedia "Nimzo-Indian Defence" article
2. Determine whether the depth-3 FEN has:
   - One canonical name → rename one slug, delete or transposes_to the other.
   - Two genuine names (Botvinnik AND Kmoch both real attributions) → keep both, apply `same_as`.
   - One real name + one Lichess-import descriptor → demote the descriptor (alias-only) and apply transposes_to.
3. Re-examine the existing `E.Nim.Sml.Bot.MLn ↔ E.Nim.Rub.Kmo`
   same_as link for the same naming consistency.

- **Pro**: avoids baking a possibly-wrong attribution into the
  catalogue contract.
- **Pro**: the user's discovery of `E.Nim.Fou` carrying the
  "Kmoch Variation" alias at depth 2 is concrete evidence that the
  catalogue already disagrees with itself on where "Kmoch" lives.
- **Pro**: future-proofs against downstream consumer breakage.
- **Con**: delays closing the rank-2 group; metrics stay at 31
  unresolved.

### Option A — `same_as` bilateral (now DEMOTED)

```
E.Nim.Sml.Bot.same_as       = E.Nim.Sml.Kmo
E.Nim.Sml.Kmo.same_as       = E.Nim.Sml.Bot
```

Still the right *position-level* answer **if** both names are
confirmed real literary attributions at this FEN.

- **Pro**: clean move-order resolution, mirrors prior precedent,
  no schema work.
- **Con (new, decisive)**: applies on top of possibly mis-attributed
  slug names. If the catalogue has Kmoch in the wrong place
  (depth 3 instead of depth 2 where `E.Nim.Fou` already canonically
  has it), this entrenches the error.

### Option E — Rename + transposes_to (NEW, contingent)

If the naming review concludes that the depth-3 FEN should
canonically be named only "Botvinnik" (and "Kmoch" belongs only to
the depth-2 4.f3 line, where `E.Nim.Fou` already places it):

```
1. Rename E.Nim.Sml.Kmo → E.Nim.Sml.Sml.MLn (or similar generic name)
   - Update canonical_name, aliases, notes
2. E.Nim.Sml.<renamed>.transposes_to = E.Nim.Sml.Bot
3. Update E.Nim.Fou aliases to reinforce the Kmoch=4.f3 canonical placement
4. Re-examine E.Nim.Sml.Bot.MLn ↔ E.Nim.Rub.Kmo accordingly
```

- **Pro**: corrects the catalogue's naming inconsistency.
- **Con**: bigger commit, naming changes affect downstream consumers
  that may have already pinned the name. Slug renames are
  particularly invasive (vs alias-only changes).

### Option F — Reinforce both names + apply same_as (NEW, contingent)

If the naming review concludes that both Botvinnik and Kmoch are
*genuine* literary attributions for the depth-3 FEN (from
different historical traditions), apply Option A but with:

```
- Updated aliases on both slugs disambiguating the attribution source
- Notes explaining the dual-attribution history
- Cross-reference to E.Nim.Fou explaining that "Kmoch" at depth 2 is
  the move-order attribution, while "Kmoch" at depth 3 is the
  pawn-structure attribution
```

- **Pro**: preserves both names with proper provenance.
- **Con**: assumes the dual-attribution thesis is correct.

## Recommendation: **Option D (Defer)** until naming review is complete

### Reasons

1. The user's challenge is well-grounded (365Chess + Chess.com +
   OCN's own `E.Nim.Fou` alias all canonically place "Kmoch" at
   depth 2, not depth 3).
2. The catalogue is **internally inconsistent**: "Kmoch Variation"
   appears as an alias at `E.Nim.Fou` (depth 2) AND as the
   canonical name at `E.Nim.Sml.Kmo` (depth 3). If both uses are
   legitimate, the duality needs to be documented; if only one is
   legitimate, the other should be removed.
3. The existing `E.Nim.Sml.Bot.MLn ↔ E.Nim.Rub.Kmo` link
   (depth 4) is also affected by whichever frame applies.
4. Applying same_as on top of unverified naming **propagates any
   error** to downstream consumers (chess-parquet etc.) where it
   becomes much costlier to fix.

### Proposed naming review sprint (separate work)

Out of scope for this proposal, but the follow-up should:

1. **Cross-reference** the depth-3 FEN against:
   - Lichess opening database (PGN export with names)
   - Encyclopaedia of Chess Openings (ECO) E24-E26 official names
   - Chess.com Opening Explorer
   - chessable / lichess-org/chess-openings repo (the source of
     Lichess's classifications)
   - Wikipedia "Nimzo-Indian Defence" article
2. **Document the dual-attribution history**:
   - When did "Botvinnik Variation" enter the Sämisch lexicon?
   - When did "Kmoch Variation" get attached to the same position?
   - Are they really co-naming, or did one supplant the other?
3. **Decide** which of Options E, F, or A applies based on
   evidence.
4. **Audit similar Sämisch/Rubinstein co-canonical pairs** for
   consistency:
   - `E.Nim.Sml.Bot.MLn ↔ E.Nim.Rub.Kmo` (depth 4)
   - Other Nimzo cases where player-name attributions diverge from
     Lichess imports.

## Summary

**NO catalogue change in this proposal.** Status: ON HOLD pending
naming review.

| metric | value |
|---|---|
| `same_as` declarations proposed | **0 (deferred)** |
| `transposes_to` declarations proposed | **0 (deferred)** |
| deletions proposed | **0** |
| catalogue rows touched | **0** |
| naming corrections recommended | **TBD pending review** |

## Risks and open questions

1. **The depth-3 FEN attribution split** — neither I nor the user
   has yet checked Lichess opening DB exports for what name it
   uses for this FEN. That's the most-likely-to-be-authoritative
   single source for OCN's purposes (since OCN historically
   imported Lichess names into many slugs).

2. **Cascading naming review** — if `E.Nim.Sml.Kmo` is renamed,
   `E.Nim.Sml.Kmo.MLn` (its child, "Kmoch Main Line") also needs
   review.

3. **Cross-tree consistency** — `E.Nim.Rub.Kmo` (depth 3 under
   Rubinstein) uses "Kmoch" *legitimately* in the move-order
   frame (it has 5.f3 played as a Rubinstein follow-up). The
   same_as link `E.Nim.Sml.Bot.MLn ↔ E.Nim.Rub.Kmo` may need
   re-examination depending on how the depth-3 Sml.Kmo question
   resolves.

4. **chess-parquet impact** — the downstream `openings.parquet`
   has `canonical_ocn1` materialized. If we rename slugs, the
   producer needs to handle the slug-history transition. None of
   the current resolutions involve slug renames; this would be a
   first.

## Recommended next step

1. Treat this proposal as **on hold** (status updated).
2. Open a separate naming review sprint that produces a
   `docs/nimzo-naming-review.md` with:
   - Authoritative-source citations for each slug attribution.
   - Recommendation: keep / rename / merge.
3. Only after the naming review concludes, return to this proposal
   and either:
   - Promote Option A (if dual-attribution confirmed),
   - Apply Option E (rename + transposes_to, if attribution
     mis-placed),
   - Apply Option F (reinforce both, if explicit historical
     duality).

---

## Appendix — Original analysis (preserved for reference)

The remainder of the proposal as originally drafted is preserved
below. It assumes both Botvinnik and Kmoch are genuine literary
attributions at the depth-3 FEN. The naming review will determine
whether this assumption holds.

### Conceptual analysis — are both real? (original)

The original argument was: yes, both are real, with Botvinnik's
subtree more developed but Kmoch's depth-3 attribution genuine.
Compare with 6 prior `same_as` cases — this looked like the most
symmetric pattern in the series. **That argument depends on
"Kmoch" being a genuine depth-3 attribution**, which the user's
challenge has now put in doubt.

### Per-slug actions (original, deferred)

| slug | proposed action |
|---|---|
| `E.Nim.Sml.Bot` | PRESERVE (canonical), `same_as = E.Nim.Sml.Kmo` |
| `E.Nim.Sml.Kmo` | PRESERVE (canonical), `same_as = E.Nim.Sml.Bot` |

### Expected audit metric impact (original, deferred)

|                            | before | after | Δ |
|----------------------------|---|---|---|
| rows totals catàleg        | 5,905 | 5,905 | 0 |
| duplicate_groups           | 130 | 130 | 0 |
| resolved_groups            | 99 | **100** | **+1** |
| multiple_canonical_groups  | 12 | **13** | **+1** |
| unresolved_groups          | 31 | **30** | **−1** |
| rows_in_unresolved_groups  | 62 | **60** | **−2** |
