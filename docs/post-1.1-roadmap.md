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
- **Backlog** (see methodology for detail):
  - `E.Nim.Rub.Kmo` Kmoch question — **APPLIED 2026-05-28** (option C,
    strings-only):
    ([`nimzo-rubinstein-kmoch-naming-proposal.md`](nimzo-rubinstein-kmoch-naming-proposal.md))
    relabelled "Kmoch Variation" → "f3 Move Order" (borrowed label, not
    in Lichess / opening-book corpus). `same_as` left unchanged
    (option D deferred as a separate transposition-layer call).
  - `E.Nim.Sml.Kmo.MLn` parent-chain quirk;
  - a player-eponym classification sweep;
  - source-specific/Lichess labels → aliases.

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
