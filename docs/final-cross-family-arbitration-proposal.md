# Final cross-family arbitrations — proposal

**Status**: PROPOSED (not applied). The last two
`CROSS_FAMILY_CONCEPTUAL` groups from
[`unresolved-map-20.md`](unresolved-map-20.md). After these, the
only unresolved groups left are the two that need dedicated
investigation: QID Miles/Petrosian (structural defect) and Nimzo
Bot/Kmo (naming review, ON HOLD).

**Headline**: the two groups want **different** treatments —
Modern/Sicilian is a genuine two-home transposition (`same_as`);
Amar/Hungarian is a one-home gambit with a move-order route
(`transposes_to`). Both verified: same FEN, no broken parent
chains.

---

## Group 1 — Modern ⇄ Sicilian (the Pterodactyl) — **same_as**

### Context

`B.Mod.Std.Nf3.C5S ⇄ B.Sic.HAc.d4.Bg7` (rank 1, score 5). The same
`...g6/...c5/...Bg7` vs `Nf3/d4` position reached from two opening
families — the Modern Defence (1.e4 g6) and the Sicilian
Hyper-Accelerated Dragon (1.e4 c5). This is the **Western
Pterodactyl** tabiya.

### FEN group

Both reach `rnbqk1nr/pp1pppbp/6p1/2p5/3PP3/5N2/PPP2PPP/RNBQKB1R w KQkq -`:

- **Modern** (`B.Mod.Std.Nf3.C5S`, B06): `1.e4 g6 2.d4 Bg7 3.Nf3 c5` (g6 first).
- **Sicilian** (`B.Sic.HAc.d4.Bg7`, B27): `1.e4 c5 2.Nf3 g6 3.d4 Bg7` (c5 first).

### Subtree shape

```
B.Mod.Std.Nf3.C5S   "Modern Defence Nf3, c5 System"  B06  ← twin
├── B.Mod.Std.Nf3.C5S.Be3   "Modern Pterodactyl Western, Anhanguera"   B06
└── B.Mod.Std.Nf3.C5S.Bc4   "Modern Pterodactyl Western, Siroccopteryx" B06

B.Sic.HAc.d4.Bg7    "Hyper-Accelerated Pterodactyl"  B27  ← twin
└── B.Sic.HAc.d4.Bg7.dxc5   "… Rhamphorhynchus"  B27
    ├── …Nc3 (Pteranodon Prefix)
    ├── …Bxc3 (Pteranodon)
    └── …Qxc3 (Exchange Variation)
```

Both sides carry **independent, developed Pterodactyl subtrees**
(Modern: Western Pterodactyl Anhanguera/Siroccopteryx; Sicilian:
Rhamphorhynchus/Pteranodon), distinct ECO (B06 vs B27), and real
opening-family identities. Neither is a breadcrumb.

### Options

- **A same_as bilateral** — ✓ **RECOMMENDED**. Two genuine family framings of the same Pterodactyl tabiya, each with its own ECO and subtree. Mirrors the cross-family precedent (Van Geet/Van't Kruijs) and the "two named routes" logic (Budapest), here across B06/B27.
- **B single_canonical** — ✗ would erase one family's claim; both are legitimately "their" opening (a Modern player and a Sicilian player both reach this by their own move order).
- **C delete** — ✗ both have subtrees.
- **D defer** — ✗ no ambiguity; the cross-family transposition is clean and both names are real.

### Recommendation: **A (same_as bilateral)**

```
B.Mod.Std.Nf3.C5S.same_as = B.Sic.HAc.d4.Bg7
B.Sic.HAc.d4.Bg7.same_as  = B.Mod.Std.Nf3.C5S
```

| slug | name | class | has_children | proposed_action | rationale | rule |
|---|---|---|---|---|---|---|
| `B.Mod.Std.Nf3.C5S` | Modern Nf3 c5 System (Western Pterodactyl) | B (Modern) | yes (2) | PRESERVE, `same_as` | B06 family framing, own subtree | Rule 4 |
| `B.Sic.HAc.d4.Bg7` | Hyper-Accelerated Pterodactyl | B (Sicilian) | yes (1) | PRESERVE, `same_as` | B27 family framing, own subtree | Rule 4 |

Notes: cross-reference, naming the Pterodactyl tabiya and the two
move orders. **Risk/open question**: the Central Pterodactyl
(`B.Mod.Std.Ctr.PtC`) is a *different* FEN and already resolved
(single_canonical with `A.Mod.e4.c5`); this proposal is only the
**Western** Pterodactyl (Nf3 line). Confidence: medium-high.

---

## Group 2 — Amar ⇄ Hungarian (the Paris Gambit) — **transposes_to**

### Context

`A.Ama.Par ⇄ A.Hng.Par` (rank 4, score 2). The Paris Gambit
(`...f4` thrust) reached from the Amar Opening (1.Nh3) and the
Hungarian Opening (1.g3). Both A00.

### FEN group

Both reach `rnbqkbnr/ppp2ppp/8/3pp3/5P2/6PN/PPPPP2P/RNBQKB1R b KQkq -`:

- **Amar** (`A.Ama.Par`, A00): `1.Nh3 d5 2.g3 e5 3.f4` (Nh3 first).
- **Hungarian** (`A.Hng.Par`, A00): `1.g3 e5 2.Nh3 d5 3.f4` (g3 first).

### Subtree shape

```
A.Ama  "Amar Opening" (1.Nh3)
└── A.Ama.Par  "Amar Opening, Paris Gambit"  ← twin; DEVELOPED
    ├── A.Ama.Par.MLn  → .Nf6 → .d4 → .Nc6   (main-line theory)
    └── A.Ama.Par.Gen  "Gent Gambit"

A.Hng  "Hungarian Opening" (1.g3)
└── A.Hng.Par  "Hungarian Opening, Paris Gambit"  ← twin; note: "Hungarian move order into the Paris Gambit"
    └── A.Hng.Par.Gen  "Gent Line"  (single child)
```

### Why this differs from Group 1

Unlike the Pterodactyl (two genuine family homes), the **Paris
Gambit has one home — the Amar (1.Nh3)**. Evidence:

- `A.Ama.Par` has the developed main-line theory subtree (MLn →
  Nf6 → d4 → Nc6) plus the Gent Gambit.
- `A.Hng.Par`'s own note says **"Hungarian move order into the
  Paris Gambit"** — it self-describes as a move-order route, not an
  independent variation. Single child.
- The gambit is defined in the 1.Nh3 (Amar) context; the 1.g3
  Hungarian simply transposes in.

So this is a single_canonical case: the Hungarian route transposes
into the Amar home.

### Options

- **A same_as** — ✗ would over-promote a self-described move-order route to co-canonical. No evidence the Hungarian framing is an independent literary identity.
- **B single_canonical via transposes_to** — ✓ **RECOMMENDED**. `A.Hng.Par → A.Ama.Par`. Preserves the Hungarian route as a breadcrumb without falsely co-canonicalising it.
- **C delete** — ✗ `A.Hng.Par` has a child (`.Gen`); deleting would orphan it, and the move-order route is worth keeping as a breadcrumb.
- **D defer** — ✗ the evidence (self-describing note + one-home gambit) is clear enough.

### Recommendation: **B (single_canonical, transposes_to)**

```
A.Hng.Par.transposes_to = A.Ama.Par
```

| slug | name | class | has_children | proposed_action | rationale | rule |
|---|---|---|---|---|---|---|
| `A.Ama.Par` | Amar Opening, Paris Gambit | A (Amar) | yes (2) | PRESERVE (canonical) | the Paris Gambit's home; developed theory subtree | canonicalisation |
| `A.Hng.Par` | Hungarian Opening, Paris Gambit | A (Hungarian) | yes (1) | `transposes_to = A.Ama.Par` | self-described "Hungarian move order into the Paris Gambit" | canonicalisation |

Notes: update `A.Hng.Par` note to point at the Amar home.
**Risk/open question**: the `.Gen` children (`A.Ama.Par.Gen` Gent
Gambit vs `A.Hng.Par.Gen` Gent Line) are at different depths/FENs
(the Amar Gent line is longer), so they are **not** a paired
duplicate and need no action here — `A.Hng.Par.Gen` simply stays a
descendant of the (now TT) `A.Hng.Par`. Confidence: medium-high.

---

## Summary

| group | recommendation | same_as | TT | delete | defer |
|---|---|---|---|---|---|
| Modern/Sicilian (Pterodactyl) | **same_as bilateral** | 2 | 0 | 0 | no |
| Amar/Hungarian (Paris Gambit) | **single_canonical TT** | 0 | 1 | 0 | no |

**If approved as recommended**: 2 `same_as` declarations (1 pair) +
1 `transposes_to`, 0 deletes, 0 row-count change. Expected:
unresolved 4 → 2, multiple_canonical 16 → 17, resolved 121 → 123.

The 2 remaining unresolved after this would be the two that need
dedicated investigation, **not** quick arbitrations:
- **QID Miles/Petrosian** — structural mis-parenting defect (broken parent chain); needs reparent/relabel sprint.
- **Nimzo Bot/Kmo** — ON HOLD pending external naming review (E.Nim.Fou conflict).

## Recommended apply order (when approved)

1. Modern/Sicilian: add 2 `same_as` (C5S ⇄ Bg7) + cross-ref notes.
2. Amar/Hungarian: add 1 `transposes_to` (Hng.Par → Ama.Par) + note.
3. Update `docs/transpositions.md` (same_as table + counts + the
   remaining-unresolved block down to 2).
4. Mark this proposal APPLIED.

Validation suite: standard. No catalogue rows added/removed.
