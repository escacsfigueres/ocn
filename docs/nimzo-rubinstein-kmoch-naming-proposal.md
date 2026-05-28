# Naming audit proposal — `E.Nim.Rub.Kmo` ("Kmoch")

**Status**: **APPLIED 2026-05-28** (option C, strings-only). The
naming fix below was applied to `catalog/ocn-1.csv` in the same commit
as this status update. First naming-audit candidate executed under
[`naming-attribution-audit-methodology.md`](naming-attribution-audit-methodology.md);
follow-up to the resolved Nimzo Bot/Kmo case. **The `same_as` relation
was NOT touched** (option D deferred — see below).

**Scope fence**: this is a *naming* audit. It does **not** propose any
edit to `transposes_to` / `same_as` / `moves_uci` / `parent_ocn1` in
this sprint. The one resolution-relation question it surfaces
(`same_as`) is explicitly **flagged and deferred**, not applied.

## The entry under audit

```
E.Nim.Rub.Kmo  | "Nimzo Rubinstein, Kmoch Variation"
  parent  = E.Nim.Rub  depth=3  flags=sharp
  moves   = 1.d4 Nf6 2.c4 e6 3.Nc3 Bb4 4.e3 O-O 5.f3 d5 6.a3 Bxc3 7.bxc3 c5
  aliases = "Kmoch Variation"
  same_as = E.Nim.Sml.Bot.MLn      (no transposes_to)
  attributed_to / attribution_source / historical_notes : all empty
  notes   = "f3/a3 structure in the Rubinstein Nimzo. Co-canonical with
             E.Nim.Sml.Bot.MLn (Sämisch-Botvinnik Main Line, ECO E25) —
             same FEN via Rubinstein and Sämisch move orders."
  children: none
```

Its `same_as` partner:

```
E.Nim.Sml.Bot.MLn | "Nimzo Saemisch Botvinnik, Main Line"
  parent  = E.Nim.Sml.Bot  depth=4
  moves   = 1.d4 Nf6 2.c4 e6 3.Nc3 Bb4 4.f3 d5 5.a3 Bxc3 6.bxc3 c5 7.e3 O-O
  aliases = "Main Line"
  same_as = E.Nim.Rub.Kmo
  notes   = "...Co-canonical with E.Nim.Rub.Kmo (Rubinstein Kmoch, ECO E40)..."
```

**FEN identity confirmed**: the two move orders reach the **same final
position** (verified — both normalise to the same FEN). The `same_as`
pairing is a genuine cross-branch FEN twin (Rubinstein `4.e3` route vs
Sämisch `4.f3/a3` route into the Botvinnik tabiya).

## Neighbourhood (for context)

| node | name | role |
|---|---|---|
| `E.Nim.Fou` | "Nimzo, 4.f3" — alias **"Kmoch Variation"** | **the real Kmoch home** (ECO E20) |
| `E.Nim.Sml.Kmo` | "Nimzo Sämisch, a3 Move Order" → `transposes_to E.Nim.Sml.Bot` | **resolved** ex-"Kmoch" artifact (precedent) |
| `E.Nim.Sml.Bot` | "Nimzo Sämisch, Botvinnik" | the Sämisch Botvinnik node |
| `E.Nim.Rub` | "Nimzo, Rubinstein" (`4.e3`) | parent branch of the entry under audit |

Every other "Kmoch" in the catalogue is a **different opening**
(`D.STa.Kmo` Semi-Tarrasch, `B.Ale.Nrm.Bc4.Kmo` Alekhine,
`C.PhD…Ng5` Philidor) — none relevant here.

## Evidence

### External (authoritative)

- **Lichess opening DB** (`external/lichess-openings/*.tsv`, the
  authoritative naming source for OCN). The **only** Nimzo-Indian
  "Kmoch Variation" is **`E20 … 4.f3`** (`e.tsv:132`). There is **no**
  Lichess entry naming a "Kmoch" line inside the Rubinstein `4.e3`
  system. The other Lichess "Kmoch Variation" rows are the
  Semi-Tarrasch (`D41`), Philidor Hanham (`C41`) and Alekhine (`B02`)
  — unrelated openings.

- **NotebookLM Q25** ("Editorial chess — Quality/Gambit/Everyman/
  Thinkers", notebook `8e7cc92b-…`), asked whether any opening book in
  its corpus names a "Kmoch Variation" in the Nimzo Rubinstein:

  > "**No, no opening book in the provided sources uses the name
  > 'Kmoch Variation' for a line in the Nimzo-Indian Rubinstein system
  > (4.e3).** … The name Kmoch only appears when referring to the
  > author Hans Kmoch and his book *Pawn Power in Chess*, or when
  > citing a 1927 game he played against Aron Nimzowitsch."

  (The corpus is also silent on the 4.f3 Kmoch — i.e. it neither
  confirms nor names "Rubinstein Kmoch"; it simply does **not support**
  it. Hans Kmoch surfaces only as a *pawn-structure theoretician*
  — *Pawn Power in Chess*, 1956; *Die Kunst der Bauernführung*, 1967 —
  and as the loser of **Kmoch–Nimzowitsch, Bad Niendorf 1927**.)

### OCN-internal (inference, not external evidence)

- The position is **already legitimately named** by its FEN twin
  `E.Nim.Sml.Bot.MLn` = "Nimzo Sämisch Botvinnik, Main Line".
- The pattern is the **same artifact** already resolved at
  `E.Nim.Sml.Kmo`: a "Kmoch" label attached to a node that is really a
  *move order* into the Sämisch-Botvinnik structure. That node was
  relabelled to a descriptor ("a3 Move Order") and its `notes`
  explicitly record that the Kmoch name belongs to `E.Nim.Fou` (E20).
- What is *real* at `E.Nim.Rub.Kmo` is the **Rubinstein move order**
  (`4.e3 O-O 5.f3`) reaching the Botvinnik tabiya — a legitimate,
  distinct route, just **not** one called "Kmoch".

## Attribution classification (per methodology A–I)

- The "**Kmoch**" name here is **type I — suspected misattribution /
  borrowed label**. It is *not* type B (no publication names it), not
  C/D/E (no player/event anchor ties Kmoch to this line), and **not a
  defensible type-G source label** (no source — not even Lichess —
  uses it for this line, so keeping it as an alias would propagate an
  unsourced label).
- The honest replacement is **type H — editorial / move-order
  descriptor**, exactly as `E.Nim.Sml.Kmo` → "a3 Move Order".

## The four questions

1. **Is there a real "Kmoch Variation" in the Nimzo Rubinstein /
   Sämisch-Botvinnik tabiya?** — **No.** The only real Nimzo Kmoch is
   `4.f3` (E20, `E.Nim.Fou`). Neither Lichess nor the opening-book
   corpus attaches "Kmoch" to the Rubinstein `4.e3` line.

2. **Is `E.Nim.Rub.Kmo` a real source label or an artifact?** —
   **Artifact / borrowed label.** Same class as the resolved
   `E.Nim.Sml.Kmo`: "Kmoch" was borrowed because the line reaches the
   same f3/a3 big-centre structure as the genuine 4.f3 Kmoch.

3. **Is the `same_as E.Nim.Sml.Bot.MLn ⇄ E.Nim.Rub.Kmo` still
   correct after the Kmoch fix?** — **The FEN identity is correct**
   (verified). Whether the relation should stay `same_as`
   (co-canonical) or become `transposes_to` is a *separate*
   transposition-layer question (see "Deferred", below). The naming
   fix does **not** require touching it.

4. **What should change?** — see recommendation.

## Applied (2026-05-28) — option C, strings-only

Exact catalogue changes (2 rows, verified: only lines 434 + 644
changed, all 5,897 other rows byte-identical; audit counts unchanged
`unresolved=0` / `multiple_canonical=17`):

- **`E.Nim.Rub.Kmo`**
  - `canonical_name`: "Nimzo Rubinstein, Kmoch Variation" →
    **"Nimzo Rubinstein, f3 Move Order"**
  - `aliases`: "Kmoch Variation" → **"f3 Move Order"**
  - `notes`: rewritten to "Rubinstein move order (4.e3 O-O 5.f3 d5 6.a3
    Bxc3 7.bxc3 c5) reaching the Sämisch-Botvinnik Main Line tabiya;
    co-canonical with E.Nim.Sml.Bot.MLn — same FEN via Rubinstein and
    Sämisch move orders. The 'Kmoch Variation' name belongs to the
    4.f3 line (E.Nim.Fou, E20), not this Rubinstein node; no source
    attests a Rubinstein Kmoch label."
  - **unchanged**: `ocn1` (slug stays `.Kmo`), `eco_legacy` (E40),
    `parent_ocn1`, `moves_uci`, `depth`, `flags`, `transposes_to`
    (empty), **`same_as` (still `E.Nim.Sml.Bot.MLn`)**.
- **`E.Nim.Sml.Bot.MLn`** — one cross-reference phrase only:
  `notes` "(Rubinstein Kmoch, ECO E40)" → "(Rubinstein f3 move order,
  ECO E40)". All other fields incl. `same_as` unchanged.
- **`E.Nim.Fou`** untouched — keeps `Kmoch Variation|4.f3 System`
  (the real Kmoch home).

**`same_as` decision = option D, DEFERRED / no change** — the
co-canonical relation persists; any move to `transposes_to` is a
separate transposition-layer call (lean: keep), not bundled here.

## Recommendation (as proposed; primary option C now applied)

**Primary — option C (relabel to a Rubinstein move-order descriptor).
Applied 2026-05-28, strings-only.**

Proposed catalogue-content edit (naming only) when approved:

- `canonical_name`: "Nimzo Rubinstein, Kmoch Variation" →
  **"Nimzo Rubinstein, f3 Move Order"** (alt wording: "Rubinstein–
  Sämisch Transposition"). Mirrors the resolved `E.Nim.Sml.Kmo`
  ("a3 Move Order").
- `aliases`: drop "Kmoch Variation" (unsourced for this line); set to
  the descriptor (e.g. "f3 Move Order"). **Reject option B** — do not
  retain "Kmoch" as an alias; no source supports it, so it would be an
  unsourced label, the very thing the methodology warns against.
- `notes`: rewrite to record the move-order fact **and** the
  borrowed-label finding, paralleling `E.Nim.Sml.Kmo`: e.g. *"Rubinstein
  move order (4.e3 O-O 5.f3 d5 6.a3 Bxc3 7.bxc3 c5) reaching the same
  FEN as the Sämisch-Botvinnik Main Line (E.Nim.Sml.Bot.MLn). The
  'Kmoch Variation' name belongs to the 4.f3 line (E.Nim.Fou, E20),
  not this Rubinstein node."*
- Optionally populate `historical_notes` with the Lichess + Q25
  finding (Kmoch = pawn-structure author + the 4.f3/E20 eponym; no
  source names a Rubinstein Kmoch).
- The cross-reference in `E.Nim.Sml.Bot.MLn.notes` ("Co-canonical with
  E.Nim.Rub.Kmo (Rubinstein Kmoch, ECO E40)") gets its parenthetical
  name updated to the new descriptor (cosmetic, same edit).

**Reject option A** (keep "Kmoch" + just document): the name is not
merely under-documented, it is *wrong* per the authoritative source.

**Slug stays `E.Nim.Rub.Kmo`.** Renaming the `.Kmo` leaf would be a
structural slug-migration (release-boundary governed, QID precedent) —
**not** part of a naming edit. The interim state "descriptor name +
`.Kmo` slug" is **already precedented and accepted**: `E.Nim.Sml.Kmo`
("a3 Move Order") likewise kept its `.Kmo` slug. No migration needed.

### Deferred — option D (the `same_as` relation), NOT in scope

Once the name is a descriptor, one *could* argue it should become
`transposes_to E.Nim.Sml.Bot.MLn` rather than co-canonical `same_as`,
to mirror `E.Nim.Sml.Kmo`'s `transposes_to`. **Lean: keep `same_as`.**
The Sämisch precedent is not a perfect parallel — `E.Nim.Sml.Kmo` and
`E.Nim.Sml.Bot` are siblings in the *same* (Sämisch) branch, so the
descriptor is clearly the non-canonical member; here the twins sit in
*different, both-legitimate* branches (Rubinstein `4.e3` vs Sämisch),
which is the natural shape for a symmetric co-canonical pair. Either
way this is a **transposition-layer decision**, explicitly out of
scope for a naming audit per the methodology. If a future pass wants
to align the two ex-Kmoch artifacts' treatment, it rides a **separate
governed transposition sprint** with its own proposal — it must not be
bundled into the naming edit.

**Option E (defer everything for lack of evidence): rejected** — the
evidence (two independent authoritative sources + an exact internal
precedent) is sufficient to recommend the naming fix C now.

## Expected impact if the naming fix (C) is applied later

- **Rows touched**: 2 (`E.Nim.Rub.Kmo` name/alias/notes; one
  cross-reference word in `E.Nim.Sml.Bot.MLn.notes`).
- **No change** to `transposes_to` / `same_as` / `moves_uci` /
  `parent_ocn1` / slug / `eco_legacy`.
- **Resolution counts unchanged**: `unresolved_groups=0`,
  `multiple_canonical_groups=17` stay (the `same_as` pair persists).
- **Downstream**: `canonical_name` / `aliases` are parquet columns, so
  the strings change there, but `canonical_ocn1` / `zobrist` /
  resolution kind are **unaffected** — no schema change, no consumer
  churn beyond the display string. (Only the deferred option D would
  move counts / `canonical_ocn1`.)

## See also

- [`naming-attribution-audit-methodology.md`](naming-attribution-audit-methodology.md)
- [`nimzo-botvinnik-kmoch-naming-review.md`](nimzo-botvinnik-kmoch-naming-review.md)
  — the sibling case (`E.Nim.Sml.Kmo`) whose resolution this mirrors.
- [`post-1.1-roadmap.md`](post-1.1-roadmap.md) — backlog this clears one item from.
