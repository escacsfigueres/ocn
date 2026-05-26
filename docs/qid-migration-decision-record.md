# QID migration — decision record

**Purpose**: separate the **go / no-go decision** about OCN's first
slug-rename from the technical mechanics (those live in
[`qid-miles-petrosian-migration-preflight.md`](qid-miles-petrosian-migration-preflight.md)).
This record is about *whether and when* to apply, not *how*.

**No catalogue change accompanies this document.**

> **DECISION: Option C SELECTED** (2026-05-26) — apply the QID
> slug-migration inside a release cycle whose end state is
> `unresolved_groups=0`, rather than now or as an "almost-resolved"
> release. The ordered runbook is in
> [`qid-release-cycle-checklist.md`](qid-release-cycle-checklist.md).
> Still **not applied** — the release cycle is itself GO-gated per
> step.

## Current state (`026c5e7`)

- 5,900 rows · **124 resolved** · **1 unresolved** · 17 multiple-canonical · tags `ocn-1.0.2`/`ocn-1.0.3` intact.
- The **sole remaining unresolved group** is QID Miles/Petrosian
  (`E.QID.Mil.MLn ⇄ E.QID.Pet.KPe`). Every other duplicate FEN group
  in the catalogue is resolved.

## What the migration would fix

1. **Broken parent chain** — `E.QID.Mil.MLn`'s moves (`…a3 Bb7 Nc3`)
   do not extend its parent `E.QID.Mil` (4.Bf4). It is the only
   broken parent chain left in the catalogue.
2. **Naming lie** — the entire a3/Nc3 **Kasparov-Petrosian** theory
   subtree (10 descendants, including slugs literally named
   "Kasparov Attack" and "Petrosian Attack") hangs under the
   **"Miles"** branch, and their `canonical_name`s read "QID
   Miles …". The correctly-named `E.QID.Pet.KPe` sits empty.
3. **The last unresolved group** — collapsing the duplicate would
   take `unresolved_groups` 1 → 0 (the catalogue would be fully
   resolved).

## What it costs

- **OCN's first slug-rename.** Every prior cleanup step was an
  add-relation (`transposes_to`/`same_as`) or a delete-leaf — never
  a rename. This changes row *identity*.
- **10 slugs change `ocn1`** (`E.QID.Mil.MLn.* → E.QID.Pet.KPe.*`)
  → `canonical_ocn1` churn for downstream consumers.
- **1 row deleted** (the duplicate `E.QID.Mil.MLn`) → 5,900 → 5,899.
- **`canonical_name` relabel** on the 10 migrated rows
  ("QID Miles …" → "QID Kasparov-Petrosian …").
- **Downstream artefacts must regenerate** — `openings.parquet`
  and `ocn-1.positions.tsv` change (new sha256s); any `chess-parquet`
  consumer that pinned an `E.QID.Mil.MLn*` slug breaks until updated.

## What it does NOT cost

- **No schema change** — still 14 columns, same downstream contract.
- **No `moves_uci`/FEN change** on any row — every migrated row keeps
  its exact line; positions are identical.
- **No new positions**; the only position-level change is the
  deletion of the duplicate `E.QID.Mil.MLn` node (which shares its
  FEN with the surviving `E.QID.Pet.KPe`).
- **No tag move** — `ocn-1.0.2`/`ocn-1.0.3` stay immutable.
- **No impact on position-lookup consumers** that join on
  FEN/zobrist rather than slug — the defect is internal
  (naming + parent hierarchy), invisible to a position query.

## Options

### A — Leave as a documented hold (status quo)

Keep `unresolved_groups=1` as a known, fully-documented item. The
catalogue functions perfectly; the blemish is an internal
naming/structure inconsistency that position-lookup consumers never
see. **Cost: 0.** Risk: the "Miles"-labelled Kasparov-Petrosian
subtree remains mislabelled for human/slug readers.

### B — Apply on `main` now + regenerate artefacts immediately

Fixes it now, but forces an **out-of-band** `chess-parquet` regen
and consumer churn outside any release cycle, for a defect that is
not urgent and not position-visible. **Not recommended.**

### C — Apply bundled with the next release/tag

Ride the slug-rename on the next version bump (e.g. a future
`ocn-1.0.4`, or the 0.3 i18n cycle), where a downstream regen + a
changelog/consumer-note are expected anyway. The first slug-rename
gets a proper version boundary and migration label. **Lowest-friction
correct path.**

## Recommendation

**Do not apply immediately.** Prefer **Option C** — apply the QID
slug-migration as part of the next coordinated release/tag cycle,
where `chess-parquet` regeneration and a consumer changelog are
already on the table. Until then, hold as **Option A**: it is a
documented, preflighted, zero-cost hold, and the catalogue is fully
functional with `unresolved_groups=1`.

Rationale: the cost (first slug-rename, 10 `canonical_ocn1` changes,
downstream regen + possible consumer breakage) is real, while the
benefit (fixing an internal naming/hierarchy inconsistency that no
position-lookup consumer sees) is not urgent. Coupling it to a
release boundary turns the downstream churn from a surprise into an
expected, batched event.

## Future GO checklist (when Option C/B is chosen)

Before applying the slug-migration:

- [ ] Confirm `chess-parquet` `efcdb-openings` producer absorbs the
      renamed `canonical_ocn1` (or accept the regenerated parquet) —
      run its smoke test against the migrated catalogue.
- [ ] Run the full preflight verification checklist
      ([`qid-miles-petrosian-migration-preflight.md`](qid-miles-petrosian-migration-preflight.md))
      — no old `E.QID.Mil.MLn*` left, all new parents resolve,
      moves/FEN unchanged, no `canonical_name` still says "Miles".
- [ ] Regenerate `openings.parquet` + `ocn-1.positions.tsv`; record
      the new sha256s.
- [ ] Write a consumer note / changelog entry: "slug-migration —
      10 `E.QID.Mil.MLn*` → `E.QID.Pet.KPe*`, 1 delete; no FEN/schema
      change."
- [ ] Label the commit/release explicitly as a **slug-migration**
      (the first in OCN), so downstream pinners are warned.
- [ ] Decide version semantics — recommend a **minor** bump (row
      identity changes for 11 rows, though no positions change).
- [ ] Apply with explicit GO; verify `unresolved_groups=0` after.

## Links

- Technical mechanics: [`qid-miles-petrosian-migration-preflight.md`](qid-miles-petrosian-migration-preflight.md)
- Structural diagnosis: [`qid-miles-petrosian-structural-proposal.md`](qid-miles-petrosian-structural-proposal.md)
- Phase closure: [`transposition-cleanup-closure.md`](transposition-cleanup-closure.md)
- Running log: [`transpositions.md`](transpositions.md)
