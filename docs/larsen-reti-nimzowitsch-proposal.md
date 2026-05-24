# Larsen ↔ Reti Nimzowitsch-Larsen — arbitration proposal

**Status**: draft proposal — NOT yet applied to `catalog/ocn-1.csv`.
**Companion**: builds on `spec/OCN-1.md` → "Canonicalisation
arbitration" and the precedents from Veresov / KID / Modern Benoni
/ Rubinstein-Colle-Zukertort.

## Context

After OCN 0.2 post-cleanup (tag `ocn-1.0.3` at `dd2abd3`), the
top-3 default unresolved groups are all "two real literary names,
no third pointer" cases that `same_as` was introduced to resolve.
The cleanest of the three by structure is:

```
A.Lar.Cls.MLn         "Larsen Classical Line, Main Line"           A01
A.Ret.Nim.MLn         "Reti Nimzowitsch-Larsen, Main Line"          A06
```

Same FEN, two different ECO codes, two different OCN family roots,
both real chess opening names. Structurally identical to the
Rubinstein ⇄ Colle-Zukertort case resolved in OCN 0.3 with
bilateral `same_as`.

## FEN group in scope (1 group)

| rank (current) | size | classes | slugs |
|---|---|---|---|
| 4 | 2 | A | `A.Lar.Cls.MLn`, `A.Ret.Nim.MLn` |

No other groups in the top 100 involve `A.Lar.*` or `A.Ret.Nim.*`.
Their respective `.Be2` and `.d4` children reach distinct FENs
and do not produce mirror duplicates at deeper levels — a cleaner
shape than KID Classical Old/e5 (which cascaded children).

## Subtree shape

```
A.Lar                              "Nimzo-Larsen Attack"           depth 1, A01
├── A.Lar.Cls                      "Classical Line"
│   └── A.Lar.Cls.MLn              "Larsen Classical, Main Line"   depth 3   ← FEN twin
│       └── A.Lar.Cls.MLn.Be2      "Be2 Line"                      depth 4 (unique FEN)
├── A.Lar.Fch                      "Fianchetto Defence"
├── A.Lar.Mod                      "Modern setup"                  (4 kids, own subtree)
├── A.Lar.Nf6                      "Indian Variation"
├── A.Lar.{b5, b6, c5, d5, e5, f5} other Black responses
└── …

A.Ret                              "Reti Opening"                  (separate root chain)
└── A.Ret.Nim                      "Nimzowitsch-Larsen Setup"      depth 2, A06
    ├── A.Ret.Nim.Ble              "Bled Variation"
    ├── A.Ret.Nim.MLn              "Reti Nimzowitsch-Larsen, Main Line"   depth 3   ← FEN twin
    │   └── A.Ret.Nim.MLn.d4       (depth 4, distinct FEN)
    │       └── A.Ret.Nim.MLn.d4.c5 (depth 5)
    └── A.Ret.Nim.Nor              "Norfolk Gambit Transposition"
```

Two real subtrees, one shared FEN at depth 3 of each. The
divergence happens at the next move: `.Be2` on the Larsen side,
`.d4` on the Reti side — completely different continuations.

## Why this is a clean `same_as` case

Apply the arbitration rules:

- **Rule 1 (descriptor vs literary)**: does NOT fire — neither
  slug is a descriptor. Both have proper literary names rooted
  in their family (Larsen Classical Line, Reti Nimzowitsch-Larsen).
- **Rule 4 (two real names, preserve both)**: **fires cleanly**.
  - `A.Lar.Cls.MLn` is anchored in the "Nimzo-Larsen Attack" family
    (`A.Lar`, ECO A01). Move order `1.b3 d5 2.Bb2 Nf6 3.e3 e6
    4.Nf3 Be7`.
  - `A.Ret.Nim.MLn` is anchored in the "Reti / Nimzowitsch-Larsen
    Setup" family (`A.Ret.Nim`, ECO A06). Move order `1.Nf3 d5
    2.b3 Nf6 3.Bb2 e6 4.e3 Be7`.
  - Both end at the same FEN. ECO codes differ (A01 vs A06)
    because ECO classifies by move order — exactly the kind of
    coarseness OCN exists to clarify.

Diagnostic table (compare against the Rubinstein/Colle-Zukertort
precedent that this proposal mirrors):

| Feature | A.Lar.Cls.MLn | A.Ret.Nim.MLn | Rubinstein precedent |
|---|---|---|---|
| Substantive family subtree | Yes (10-slug `A.Lar` tree) | Yes (Reti Nim subtree with 3 named children) | matches |
| Independent literary name | Yes (Nimzo-Larsen Attack) | Yes (Reti Nimzowitsch-Larsen) | matches |
| Distinct ECO | A01 | A06 | matches (D05 vs D05 in Rub case — actually same ECO there, this is even cleaner) |
| Self-described as descriptor | No | No | matches |
| Notes language | Plain ("Nf3 and ...Be7 in the Larsen Classical line.") | Plain ("e3 and Be7 in the Reti Nimzowitsch-Larsen setup.") | matches |
| Mirror children at deeper levels | No (Be2 vs d4 diverge) | No | matches (Rub also had no deeper mirror) |

This is a **textbook `same_as` case**. Recommended action mirrors
the D.Rub ⇄ A.Col.Zuk resolution exactly.

## Options considered

### Option A — `same_as` bilateral (RECOMMENDED)

```
A.Lar.Cls.MLn.same_as  = A.Ret.Nim.MLn
A.Ret.Nim.MLn.same_as  = A.Lar.Cls.MLn
```

Both preserved as canonicals. The audit reports the rank-4 group
as `multiple_canonical` (canonical_count=2) and hides it from the
default ranked report. Downstream consumers join by zobrist and
get both rows, then render as `Larsen Classical Line, Main Line /
Reti Nimzowitsch-Larsen, Main Line` per the OCN 0.2 consumer guide.

- **Pro**: preserves both literary identities (the Larsen name
  with ECO A01 and the Reti Nimzowitsch-Larsen name with ECO A06,
  both established in chess literature). No data loss, no
  arbitrary canonical choice.
- **Pro**: matches the precedent set by Rubinstein/Colle-Zukertort,
  Italian Giuoco/Two Knights, Nimzo Kmoch/Sämisch-Botvinnik, and
  the French/KID multi-canonical groups. No new patterns
  introduced.
- **Con**: none material. Audit metric impact is +1
  `multiple_canonical_groups`, −1 `unresolved_groups`, 0 schema
  change, 0 row deletions, 0 transposes_to writes.

### Option B — Single canonical `A.Lar.Cls.MLn` (DISCARDED)

Would require `A.Ret.Nim.MLn.transposes_to = A.Lar.Cls.MLn`.

- **Con**: erases the Reti Nimzowitsch-Larsen identity (A06) as
  a canonical OCN entry. The A.Ret.Nim subtree would have its
  named "Main Line" reduced to a transposition pointer, which
  misrepresents the Reti tradition.

### Option C — Single canonical `A.Ret.Nim.MLn` (DISCARDED)

Would require `A.Lar.Cls.MLn.transposes_to = A.Ret.Nim.MLn`.

- **Con**: symmetric problem. Erases the Larsen Classical Line
  (A01) as canonical and pushes the Nimzo-Larsen Attack literary
  identity below its Reti-routed sibling. Counter to how the
  opening is commonly named in 1.b3-side literature.

### Option D — Defer (DISCARDED)

- **Con**: no longer the right call now that `same_as` exists.
  The reason previous similar cases were deferred was the absence
  of a declaration channel. With `same_as` in production since
  OCN 0.3, there is no schema barrier.

## Per-slug actions (Option A)

| slug | action | rationale | rule |
|---|---|---|---|
| `A.Lar.Cls.MLn` | **PRESERVE (canonical)**, add `same_as = A.Ret.Nim.MLn` | "Nimzo-Larsen Attack" literary identity (A01), kept canonical. | Rule 4 |
| `A.Ret.Nim.MLn` | **PRESERVE (canonical)**, add `same_as = A.Lar.Cls.MLn` | "Reti Nimzowitsch-Larsen" literary identity (A06), kept canonical. | Rule 4 |

**Notes to add (informational cross-reference)**:

- `A.Lar.Cls.MLn.notes`: `Nf3 and ...Be7 in the Larsen Classical
  line. Co-canonical with A.Ret.Nim.MLn (Reti Nimzowitsch-Larsen
  Main Line, A06) — same FEN via the 1.Nf3 then 2.b3 Reti move
  order.`
- `A.Ret.Nim.MLn.notes`: `e3 and Be7 in the Reti Nimzowitsch-Larsen
  setup. Co-canonical with A.Lar.Cls.MLn (Larsen Classical Line
  Main Line, A01) — same FEN via the 1.b3 Larsen move order.`

No alias changes (the existing aliases describe the line
correctly; adding cross-family aliases would mix ECO ranges and
confuse ECO-aware consumers).

## Summary

**Preserve (no change to canonicality)**: 2 slugs.

**`same_as` (2 declarations, bilateral)**:

| slug | same_as |
|---|---|
| `A.Lar.Cls.MLn` | `A.Ret.Nim.MLn` |
| `A.Ret.Nim.MLn` | `A.Lar.Cls.MLn` |

**`transposes_to`**: 0.

**Deletions**: 0.

**Reparenting**: 0.

## Expected audit metric impact

|                            | before | after | Δ |
|----------------------------|---|---|---|
| rows totals catàleg        | 5,905 | 5,905 | 0 |
| duplicate_groups           | 130 | 130 | 0 |
| resolved_groups            | 93 | **94** | **+1** |
| multiple_canonical_groups  | 6 | **7** | **+1** |
| unresolved_groups          | 37 | **36** | **−1** |
| rows_in_unresolved_groups  | 75 | **73** | **−2** |

The rank-4 group disappears from the default ranked report;
becomes visible only under `--include-resolved` with
`resolution_kind=multiple_canonical`.

## Risks and open questions

1. **Cleanest `same_as` case to date**. No deletions, no
   cascading children, no schema change, no policy debate. The
   only judgement call is "are both names real?" — and the
   diagnostic table above answers yes on every criterion.

2. **Subtree size asymmetry** (A.Lar has 10-slug subtree; A.Ret.Nim
   has 5-slug subtree). Does this argue against `same_as`?
   No — the Rubinstein/Colle-Zukertort precedent had a worse
   asymmetry (11-slug Rubinstein vs 3-slug Colle-Zukertort) and
   `same_as` worked fine. Subtree size is independent of which
   names are co-canonical at the shared FEN.

3. **What if a user looks up the Larsen Classical line and gets
   a Reti name back?** With the OCN 0.2 consumer guide already
   published, downstream consumers know to expect multi-row
   returns on zobrist joins and to render both names. This case
   is precisely the third worked example in
   [`docs/consuming-ocn-0.2.md`](consuming-ocn-0.2.md) §6.

4. **Should the children get `same_as` too?** No. The children
   `A.Lar.Cls.MLn.Be2` and `A.Ret.Nim.MLn.d4` reach distinct
   FENs (Be2 vs d4 are different White moves). They are not
   co-canonical and the audit does not flag them as duplicates.

## Recommended apply order

When approved (single commit):

1. Set `A.Lar.Cls.MLn.same_as = A.Ret.Nim.MLn`.
2. Set `A.Ret.Nim.MLn.same_as = A.Lar.Cls.MLn`.
3. Update notes on both slugs with cross-references.
4. Update `docs/transpositions.md`:
   - Move Larsen/Reti from "Deferred" to "Resolved via same_as"
     (in the same section that already lists Rubinstein,
     Nimzo Kmoch, Italian Giuoco).
5. Mark this proposal `Status: APPLIED`.

Validations to run: standard suite (`validate.py --strict-chess`,
`audit_chess.py`, `unittest`, `lichess_parent_map --check`,
`audit_transpositions --summary` and `--ranked --limit 30`).
Expected commit shape: 2 catalogue rows touched (10 / 10 line
diff), `docs/transpositions.md` updated, proposal status flipped.
