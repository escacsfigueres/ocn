# OCN — post-1.1 roadmap

Where the project stands after `ocn-1.1.0`, and what the next tracks
are. **Docs-only planning** — nothing here implies an applied change.

## Where 1.1.0 left us

- **Transposition layer: COMPLETE.** `unresolved_groups=0`; every
  duplicate-FEN group classified (`single_canonical` /
  `multiple_canonical`). 5,899 rows. Released and **downstream-verified**
  end-to-end by a real consumer
  ([`release-ocn-1.1.0-downstream-verification.md`](release-ocn-1.1.0-downstream-verification.md)).
- **Schema stable** — 14-column catalogue; 13-column `openings.parquet`.
- **Do not reopen** duplicate-FEN cleanup. Future work is *data
  quality* and *features*, not resolution.

## Track 1 — post-1.1 data quality (naming / attribution)

The remaining quality frontier is **names and attributions**, not
positions. Are `canonical_name` / `aliases` / `attributed_to` *true*,
and is the *kind* of attribution explicit (invented vs published vs
popularised vs event-anchored)?

- **Methodology**:
  [`naming-attribution-audit-methodology.md`](naming-attribution-audit-methodology.md)
  — attribution types A–I (incl. the explicit **event/game anchor**
  type), evidence rules, decision criteria, 3 worked examples, and a
  candidate backlog.
- **Discipline**: each audit is gated on its own proposal + evidence +
  explicit GO. Naming-only edits never touch `transposes_to` /
  `same_as`; structural (slug/parent) corrections ride a release
  boundary as a governed migration (the QID Miles/Petrosian precedent).
- **Discovery backlog** — **CREATED 2026-05-30** (dynamic-workflow,
  4 parallel read-only sweeps, no catalogue change):
  [`naming-attribution-audit-backlog.md`](naming-attribution-audit-backlog.md).
  38 findings → 32 distinct slugs: 12 proposal candidates, 11
  deeper-source-review, 14 ignore/keep, 1 cosmetic. Each item is
  source-gated on its own proposal + explicit GO.
- **Backlog items** (see the discovery backlog + methodology for detail):
  - `E.Nim.Rub.Kmo` Kmoch question — **APPLIED 2026-05-28** (option C,
    strings-only):
    ([`nimzo-rubinstein-kmoch-naming-proposal.md`](nimzo-rubinstein-kmoch-naming-proposal.md))
    relabelled "Kmoch Variation" → "f3 Move Order" (borrowed label, not
    in Lichess / opening-book corpus). `same_as` left unchanged
    (option D deferred as a separate transposition-layer call).
  - `E.Nim.Sml.Kmo.MLn` parent-chain quirk — **verified closeable**
    (reads sensibly post-relabel; discovery backlog WS4).
  - player-eponym attribution — **batch-5 APPLIED 2026-05-30**: `A.Tro`
    (Trompowsky), `B.Ale` (Alekhine), `B.Sic.Ros` (Rossolimo),
    `C.RyL.Mar` (Marshall), `B.Sic.Naj.Pol` (Polugaevsky) — strings-only,
    head rows only, evidence-sprint + Lumbra chronology backed (all
    popularizer/introducer types). `B.Fre.Win` held PARTIAL pending a
    reference-grade naming source; `B.Sic.Tay/Alp`, `D.Tar`, `D.Chi`
    remain deeper-review (per-head only).
  - non-person name taxonomy — **MAPPED 2026-05-30** (dynamic-workflow, 6 read-only sweeps): why non-person names exist (geography/structure/move/metaphor/gambit/descriptor). Result: **no attribution batch** — the non-person space is already correctly unattributed (~46% of rows are pure editorial descriptors that must stay so). ([`non-person-opening-name-taxonomy.md`](non-person-opening-name-taxonomy.md)). Only Maróczy Bind is mis-filed (a person → eponym track); Carlsbad note is the one source-gated enrichment.
  - parked-items source sweep — **MAPPED 2026-05-31** (dynamic-workflow, 5 read-only agents): graded Winawer, Maróczy Bind, Carlsbad, and the deeper-review eponyms — **one CLEAR 3-row batch (Maróczy Bind) + 6 PARTIAL**. ([`parked-naming-audit-source-sweep.md`](parked-naming-audit-source-sweep.md)).
  - Maróczy Bind attribution — **APPLIED 2026-05-31** (`B.Sic.Acc.Mar`, `B.Sic.Kan.Mar`, `B.Sic.OKe.c4`): `attributed_to` "Géza Maróczy (popularizer)", strings-only, head rows only; first-hand source (Edward Winter, *Géza Maróczy*); `historical_notes` notes he never played the bind as White (named via Swiderski–Maróczy, Monte Carlo 1904). The other six parked items stay PARTIAL pending one first-hand reference each.
  - `D.QGD.Cmb` Cambridge Springs — **APPLIED 2026-05-30** (option A1,
    strings-only, head row only)
    ([`qgd-cambridge-springs-attribution-proposal.md`](qgd-cambridge-springs-attribution-proposal.md)):
    type-E tournament anchor; `attributed_to`/`attribution_source`/
    `historical_notes` set, web-verified source (Panczyk & Ilczuk 2002),
    Oxford Companion not used (unseen first-hand). 0 child rows touched;
    catalogue stays 5,899 rows / `unresolved_groups=0`. **OCN's first
    post-1.1 attribution edit and first event-anchor attribution.**
  - source-specific/Lichess labels → aliases — Kmoch cluster triaged
    (corpus-confirmed, no demotions); next pass is a token-normalised
  - event/venue anchor batch — **MAPPED 2026-05-30** (dynamic-workflow, 4 read-only sweeps): **no batch-safe type-E candidates** — venue tokens are F/G structure/place labels. ([`event-venue-attribution-batch-proposal.md`](event-venue-attribution-batch-proposal.md)). Next event candidate at most Carlsbad (source-gated); Marshall → eponym track.
  - player-eponym anchor batch — **MAPPED 2026-05-30** (dynamic-workflow, 4 read-only sweeps): **no batch-safe candidates** — strong eponyms, but no first-hand naming source opened (Lichess = type-G label). ([`player-eponym-attribution-batch-proposal.md`](player-eponym-attribution-batch-proposal.md)). Next: single source-gated proposal (A.Tro / B.Fre.Win) or an evidence sprint. Includes a reusable per-surname risk map + house-style templates.
    misplacement detector (backlog Top-5 #5).
  - **triage automation** — **CREATED 2026-05-31** (`tools/audit_naming_attribution.py`,
    [`naming-attribution-automation.md`](naming-attribution-automation.md)):
    deterministic triage of all 5,899 rows into category / risk /
    next-action + eponym head-groups, so a human points dynamic workflows
    at the next *homogeneous* batch instead of auditing one row at a time.
    **Automates triage, not truth** — no catalogue change, no source
    invention. The scaling lever for the rest of this track; pipeline is
    triage → select top groups → workflow evidence search → CLEAR-batch apply.
  - **batch apply engine** — **CREATED 2026-06-08**
    (`tools/apply_attribution_manifest.py`,
    [`attribution-batch-engine.md`](attribution-batch-engine.md)): the
    executable form of the loop's final step. Consumes a JSON manifest
    (`ocn.attribution_manifest.v1`: mode, expected rows, per-row field
    changes + evidence grade + sources) and applies a CLEAR, homogeneous
    batch with **zero collateral diff** (untouched rows kept byte-for-byte;
    only named rows re-serialised). **Dry-run by default**; `--apply --out`
    writes only under an explicit GO. Guardrails: 14-column schema, stale-
    manifest row count, slug existence, mode field-whitelist, the
    `attributed_to ⇒ attribution_source` invariant, and an exact
    `expected_changed_rows` contract that rejects no-op / already-applied
    batches. Optional `--validate` runs `validate.py` on the result and
    aborts on failure. The automation foundation that turns
    "triage → workflow → manifest → dry-run → human review → GO apply" into
    repeatable, low-risk tooling instead of hand-editing the CSV.
    **First real batch APPLIED 2026-06-08** via the engine — Lot A player
    eponyms `D.Tar` (Tarrasch) + `D.Chi` (Chigorin), QGD heads only, Avrukh-
    sourced (`docs/manifests/lot-a-player-eponyms.manifest.json`,
    [`lot-a-player-eponyms-dry-run.md`](lot-a-player-eponyms-dry-run.md));
    2 rows, validates 5899/0, `unresolved_groups=0`. Winawer held (citation
    author/year unpinned); Carlsbad (`D.QGD.Exc.Car`) is the parked Lot B.
  - **whole-catalogue factory map** — **CREATED 2026-06-08** (12-agent read-only
    dynamic workflow, no catalogue change):
    [`whole-catalogue-attribution-factory-map.md`](whole-catalogue-attribution-factory-map.md).
    Turns 5,877 empty-attribution rows into 10 ranked source-gated lots (6
    safe-if-sourced, 4 hold), a 21-family do-not-touch map, 9 dangerous
    multi-head surnames, a source strategy, and a 5-item tooling backlog
    (`scaffold_manifest`, `source_status_table`, `candidate_slice_export`,
    `docs_slug_verifier`, `lumbra_chronology_helper`). Next sprint =
    tooling → evidence (head-only safe lots) → one manifest batch.

## Track 2 — 0.3 internationalised aliases

Catalan / Spanish / French / German display names. The English
`canonical_name` stays definitive (per the README roadmap). Independent
of Track 1; can proceed in parallel.

## Track 3 — 1.0 freeze

Frozen format and stable catalogue, public call for feedback. Gated on
Tracks 1–2 reaching a satisfactory state.

## Sequencing note

Track 1 (data quality) and Track 2 (i18n) are independent and may
interleave. Neither blocks on the other; both should be in a good
state before the 1.0 freeze (Track 3).
