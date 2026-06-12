# Rubinstein Opening ↔ Colle-Zukertort — arbitration proposal

**Status**: **APPLIED via `same_as` schema extension (OCN 0.3)**. See
`docs/transpositions.md` → "`same_as`-resolved groups" for the
applied outcome. The proposal also triggered the schema extension
itself (commit `84f18fc`: `same_as` column added with full
validator + audit support) and the bulk apply (this commit:
populated 6 co-canonical pairs).

**Companion**: builds on `spec/OCN-1.md` → "Canonicalisation
arbitration" and "Co-canonical preservation".

## Context

After Modern Benoni, the new top-1 in the audit is a single 2-row
group:

```
D.Rub     "Rubinstein Opening"            depth 1, ECO D05, 2 kids
A.Col.Zuk "Colle System, Zukertort"       depth 2, ECO D05, 1 kid
```

Both reach the same FEN
`rnbqkb1r/pp3ppp/4pn2/2pp4/3P4/1P1BPN2/P1P2PPP/RNBQK2R b KQkq -` —
the `d4 + Nf3 + e3 + Bd3 + b3` queen-pawn setup after Black has
played `…Nf6, …e6, …c5, …d5`.

This is the **first case in OCN where two pure literary identities
share a FEN with no third slug available to act as in-group
pointer**. The existing `multiple_canonical` resolution kind
requires at least one pointer into the group to be computable; this
group does not have one and cannot get one without contortions.

## FEN group in scope (1 group)

| rank | size | classes | slugs |
|---|---|---|---|
| 1 | 2 | A,D | `D.Rub`, `A.Col.Zuk` |

No deeper cross-tree FEN duplicates exist. Verified: the 11-slug
`D.Rub.*` subtree and the 3-slug `A.Col.Zuk.*` subtree explore
**different** sub-positions (Rubinstein side develops via `…Bd6`,
Colle-Zukertort side via `…Nc6`), so there is no mirror cascade
like KID Old/e5 or the Veresov D.QPG subtree.

## Subtree shape

```
D                                                        depth 0
└── D.Rub                          "Rubinstein Opening"  depth 1, D05
    ├── D.Rub.Col                  "Rubinstein, Colle-Zukertort Setup"   ← explicit cross-name
    │   └── D.Rub.Col.MLn          "Rubinstein Colle-Zukertort, Main Line"
    └── D.Rub.Nc6                  "Rubinstein Opening, Nc6"
        ├── D.Rub.Nc6.O-O
        │   ├── .Bd6
        │   │   └── .Bd6.Bb2
        │   │       └── .Bd6.Bb2.O-O
        │   └── .Be7
        │       └── .Be7.Bb2
        │           └── .Be7.Bb2.O-O

A                                                        depth 0
└── A.Col                          "Colle System"        depth 1, D04|D05
    ├── A.Col.Kol                  "Koltanowski"
    ├── A.Col.Zuk                  "Colle System, Zukertort"  depth 2, D05  ← FEN twin of D.Rub
    │   └── A.Col.Zuk.MLn          "Colle Zukertort, Main Line"
    │       └── A.Col.Zuk.MLn.Be7
    ├── A.Col.Phn                  "Phoenix Attack"
    └── A.Col.Bd6                  "Bd6"
```

Notable observations:

- **`D.Rub.Col` is literally named "Rubinstein Opening,
  Colle-Zukertort Setup"** — the catalogue already records the
  cross-naming relationship one level down, using `Col` as a
  sub-label inside the Rubinstein tree.
- **`A.Col` (the Colle System root)** already carries the alias
  `Zukertort Colle move-order` (added in the Veresov sprint when
  `D.QPG.Zuk.Col.Bd3 → A.Col` was wired).
- **D.Rub has 11 descendants** (substantive subtree exploring `.Col`
  and `.Nc6` branches); A.Col.Zuk has 3 descendants (one Main Line
  chain). Both are real chess opening systems, not stubs.
- **Same ECO D05** for both root slugs.

## Why this case is hard

The two slugs match every diagnostic for "two real literary
identities":

| Diagnostic | D.Rub | A.Col.Zuk |
|---|---|---|
| Substantive subtree | Yes (11 slugs) | Yes (3 slugs) |
| Distinct subtree topology | Yes (.Col + .Nc6 branches) | Yes (only MLn → Be7) |
| Independent literary name | Yes (Rubinstein Opening, historical) | Yes (Colle-Zukertort, contemporary) |
| ECO assignment | D05 | D05 |
| Self-described as descriptor | No | No |
| Notes language | Plain ("d4/Nf3/e3/Bd3/b3 queen-pawn setup") | Plain ("b3/Bb2 queenside fianchetto in the Colle family") |

This is structurally **stronger** than the KID Old/e5 case where
the multiple_canonical resolution applied — both slugs here have
their own family-level identity, not just a parent-child
relationship within one family.

But unlike KID:

- The group has **only 2 entries**. KID had 3 (the OID descriptor
  was the third slug acting as in-group pointer).
- No third path slug exists in the catalogue. No D.QPG-style
  breadcrumb, no Indian-route descriptor, nothing.

Without a third slug, the current `_resolution_kind()` cannot
classify the group as `multiple_canonical`: that kind requires
`pointers_into_group > 0`. The group would stay `unresolved` in
the audit even if both slugs were preserved as canonicals by
design.

## Options considered

### Option A — Multiple canonical via invented pointer

Preserve both as canonicals; pick one to artificially carry a
"placeholder" TT pointing at the other.

- **Pro**: closes the audit, no schema growth.
- **Con**: forces one of the two slugs to formally declare itself
  non-canonical (`transposes_to = ...`) while we are also calling
  it canonical in the doc. **This is the relaxation the user
  explicitly rejected** when approving the `multiple_canonical`
  design: "`transposes_to` continua volent dir 'aquest és no-
  canònic'". Discarded.

### Option B — Single canonical: A.Col.Zuk

`D.Rub → TT to A.Col.Zuk`. The 11-slug D.Rub subtree stays alive
under a TT'd root.

- **Pro**: matches contemporary literature (Colle-Zukertort is the
  modern label). Computable today, no schema growth.
- **Con**: erases "Rubinstein Opening" as a canonical D-tree
  identity. The whole 11-slug Rubinstein subtree becomes
  navigable but non-canonical, even though the Rubinstein
  identity has historical primacy and its own theoretical
  framework. Also asymmetric: a 2-slug subtree (A.Col.Zuk + MLn +
  MLn.Be7) becomes the canonical anchor for an 11-slug Rubinstein
  subtree.

### Option C — Single canonical: D.Rub

`A.Col.Zuk → TT to D.Rub`. The 3-slug Colle-Zukertort subtree
stays alive under a TT'd node.

- **Pro**: respects OCN's hierarchy logic (depth-1 family root
  beats depth-2 sub-variation). Larger and historically primary
  subtree wins. Computable today.
- **Con**: marks the contemporarily-dominant name
  ("Colle-Zukertort") as a transposition of the
  historically-original name ("Rubinstein"). Counter to how the
  opening is taught and named in modern training resources
  (Chessable, ChessBase, recent books). Less defensible by
  current literature; more defensible by chronology.

### Option D — Defer with dignity

Leave both as canonicals with no `transposes_to`. Group stays
`unresolved` in the audit. Add explicit cross-reference notes on
both slugs. Document the case as the first that justifies a
future `same_as` schema if more accumulate.

- **Pro**: preserves both literary identities without forcing a
  choice. No schema growth. The audit's report correctly reflects
  that OCN has not catalogued this transposition computationally
  yet.
- **Con**: rank 1 stays in the default ranked report (one
  permanently-visible unresolved group). Cosmetic, not functional.

## Recommendation: Option D (Defer), and propose `same_as` as
followup if more cases accumulate

The case has the structure of `multiple_canonical` (two real
names, both with substantive subtrees, no descriptor sides) but
lacks the **declaration mechanism** (no third slug to act as
in-group pointer). Forcing one of the four other options would
either:

- **Option A**: corrupt the meaning of `transposes_to`.
- **Option B or C**: erase a real literary identity to satisfy a
  catalogue convenience.

Defer is the honest choice. The group is **conceptually resolved**
(both slugs preserved as canonicals by editorial decision) but
**not computationally resolved** (no TT pointer exists). The audit
will reflect the gap correctly.

### Schema followup: `same_as` is worth considering now

This is **not** an isolated case. Two other top-30 unresolved
groups have the same shape (two real literary identities, no
third slug, no descriptor side):

| rank | slugs | trad. names |
|---|---|---|
| 1 (this) | `D.Rub` ⇄ `A.Col.Zuk` | Rubinstein Opening ⇄ Colle-Zukertort |
| 5 | `E.Nim.Rub.Kmo` ⇄ `E.Nim.Sml.Bot.MLn` | Nimzo Rubinstein Kmoch ⇄ Nimzo Sämisch Botvinnik MLn |
| 13, 14 | `C.Ita.Giu.O-O.Nf6` ⇄ `C.Ita.Two.O-O.Bc5` (+ deeper `.d4` pair) | Giuoco Piano ⇄ Two Knights |

Three families, four groups. None has a third slug available to
act as in-group pointer. All three would benefit from a
declaration-only mechanism that lets the audit recognise
"intentionally co-canonical" without requiring a fake TT.

**Recommended next infrastructure work** (after this proposal is
applied or accepted as defer):

- Introduce a `same_as` column or a notes-keyword convention (e.g.
  `Same FEN as <slug>:` parsed by the audit) that allows
  declaring multiple_canonical without requiring an in-group
  pointer.
- Apply same_as to D.Rub ⇄ A.Col.Zuk, Nimzo Kmo ⇄ Sml.Bot, and
  Italian Giuoco ⇄ Two Knights in one cleanup commit.
- Extend `_resolution_kind()` to recognise the new declaration
  channel.

The user's intuition was right: this is the first case that
justifies `same_as` if anything does. **Two more cases of the same
shape exist in the top 30**, which crosses the threshold from
"one-off" to "structural need".

## Per-slug action (Option D, defer)

| slug | action | rationale |
|---|---|---|
| `D.Rub` | **PRESERVE (canonical, deferred)** | Real literary identity, historical primacy, 11-slug subtree. Add cross-reference note pointing at A.Col.Zuk. |
| `A.Col.Zuk` | **PRESERVE (canonical, deferred)** | Real literary identity, contemporary dominance, substantive subtree under Colle System. Add cross-reference note pointing at D.Rub. |

**Notes to add** (informational only, no behavioural impact):

- `D.Rub.notes`: `d4/Nf3/e3/Bd3/b3 queen-pawn setup. Same FEN also
  catalogued as A.Col.Zuk (Colle System, Zukertort, ECO D05); both
  canonicals preserved per arbitration rule 4. Group remains
  unresolved in the audit pending a 'same_as' declaration channel.`
- `A.Col.Zuk.notes`: `b3/Bb2 queenside fianchetto in the Colle
  family. Same FEN also catalogued as D.Rub (Rubinstein Opening,
  ECO D05); both canonicals preserved per arbitration rule 4.
  Group remains unresolved in the audit pending a 'same_as'
  declaration channel.`

No `transposes_to` writes. No deletions. No reparenting.

## Expected audit metric impact (Option D)

|                            | before | after | Δ |
|----------------------------|---|---|---|
| rows totals catàleg        | 5,966 | 5,966 | 0 |
| duplicate_groups           | 191 | 191 | 0 |
| resolved_groups            | 71 | 71 | 0 |
| unresolved_groups          | 120 | 120 | 0 |
| multiple_canonical_groups  | 2 | 2 | 0 |
| rows_in_unresolved_groups  | 241 | 241 | 0 |

Defer means **no metric changes**. The group stays at rank 1 in
the default ranked report as a known-and-documented unresolved
case until the `same_as` followup lands.

## TT proposed: 0
## Deletes proposed: 0
## Multiple canonical: conceptually yes, computationally not yet (deferred)
## `same_as` needed: yes, when 1-2 more similar cases land or when the
  user prefers to ship `same_as` now given that 3 candidate cases
  already exist.

## Risks and open questions

1. **Cosmetic visibility**: rank 1 stays visible in default
   `--ranked` output. Will the user (or downstream consumers) find
   this noisy? Mitigation: cross-reference notes signal "intentional"
   to a human reader; the `--include-resolved` flag is unchanged.

2. **Schema growth timing**: introducing `same_as` is a real
   schema change with non-trivial cascade (validator, audit,
   export_positions, spec, all fixtures, doc). The Veresov sprint
   already used a similar amount of work to add `transposes_to`.
   Worth doing only if 3 cases is enough of a pattern.

3. **Alternative**: instead of `same_as` column, use a
   notes-keyword convention. Pro: no schema change, no fixture
   churn. Con: less rigorous; notes are free-text and parsing them
   is brittle. The trade-off depends on how strictly we want to
   enforce declaration syntax.

4. **What if the user disagrees with defer?** Then Option B
   (A.Col.Zuk canonical) is the next-best choice: it respects
   contemporary literature and computes the resolution today. Option
   C (D.Rub canonical) is third-best: respects OCN's hierarchy
   logic but conflicts with how the opening is actually named
   today.

5. **Two cross-references in notes is the minimum**: with `same_as`
   the canonical-cross-reference moves out of notes into a
   structured field. Until then, notes carry the burden.

## Summary

**Action this sprint**: defer with two informational notes added to
the canonicals (`D.Rub` and `A.Col.Zuk`) cross-referencing each
other.

**Action next sprint (recommended)**: introduce `same_as` schema or
notes-keyword convention to declare intentional multiple-canonical
groups without requiring in-group pointer. Apply to D.Rub ⇄
A.Col.Zuk, Nimzo Kmo ⇄ Sml.Bot, Italian Giuoco ⇄ Two Knights in
one cleanup commit.

This proposal contains no `catalog/ocn-1.csv` edits. The two
informational notes can be added now as part of the defer
documentation, or held until the same_as followup so all
cross-references are written in one consistent style.
