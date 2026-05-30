# Naming / attribution audit — discovery backlog (post-1.1)

**Status**: **post-1.1 data-quality discovery**. **No catalogue change**
accompanies this document — it is a prioritized backlog of *candidates*,
not a change set. Every item is gated on its own proposal + evidence +
explicit GO, exactly as the
[`naming-attribution-audit-methodology.md`](naming-attribution-audit-methodology.md)
requires. **Dynamic workflow used: yes** (4 parallel read-only sweeps).

> **Event/venue batch map (2026-05-30):** a follow-up dynamic-workflow sweep classified event/venue/game anchors — result: **no batch-safe candidates** (venue tokens are F/G structure/place labels, not type-E event anchors). See [`event-venue-attribution-batch-proposal.md`](event-venue-attribution-batch-proposal.md). At most one source-gated individual proposal (Carlsbad); Marshall routes to the player-eponym track.
>
> **Player-eponym batch map (2026-05-30):** a third dynamic-workflow sweep classified the Tier-1 player eponyms — result: **no batch-safe candidates** (right *kind* of eponym, but no first-hand naming source was opened; a Lichess label is type-G only). See [`player-eponym-attribution-batch-proposal.md`](player-eponym-attribution-batch-proposal.md). Next: a single source-gated proposal (A.Tro Trompowsky or B.Fre.Win Winawer), or an evidence sprint to convert Group B into a real batch. **UPDATE (evidence sprint, 2026-05-30):** done — [`player-eponym-group-b-evidence-sprint.md`](player-eponym-group-b-evidence-sprint.md) made 3 heads batch-ready (A.Tro, B.Ale, C.RyL.Mar); 3 remain PARTIAL pending one reference each.

This document sits on top of the methodology (it supplies the *what to
audit next*; the methodology supplies the *how*). It changes nothing in
`catalog/ocn-1.csv`.

## Method

A dynamic workflow ran **4 parallel read-only discovery agents**, each a
distinct sweep over the live 5,899-row catalogue, calibrated against the
11 rows that already carry `attributed_to`. Agents returned structured
findings (slug · issue · type A–I · evidence strength · recommended
action · blast radius · uncertainty) and **edited nothing**; the
orchestrator consolidated, deduplicated, and verified every cited slug
against the CSV before writing this file.

| # | Workstream | Found |
|---|---|---|
| 1 | Player-eponym sweep (surname in name/alias, empty `attributed_to`) | 15 |
| 2 | Source-specific / database-label sweep (type F/G) | 6 |
| 3 | Event / venue / famous-game anchor sweep (type E) | 9 |
| 4 | Known-residual sweep (docs/release-flagged items vs live CSV) | 8 |

**38 findings total**, deduplicated to **32 distinct slugs** (the 6
overlaps are the Kmoch cluster, where WS2 and WS4 independently agree).
Action split: **12 proposal · 11 deeper-source-review · 14 ignore/keep ·
1 cosmetic-relabel**.

**Sources consulted**: `catalog/ocn-1.csv` (source of truth, every cited
slug re-verified against it), the methodology + roadmap + the applied
`nimzo-rubinstein-kmoch-naming-proposal.md`, and the local Lichess corpus
`external/lichess-openings` (decisive for the Kmoch cluster). **No web
was used.** `nlm` was available but not needed for discovery.

**Limitations** (carried up from the agents):

- This is **discovery, not arbitration**: no agent located the binding
  source for any candidate. Every "proposal" still needs one citable
  source (book/chapter > dated game > DB aggregate) before any apply.
- Evidence-strength ratings reflect **how universally the name is tied
  to the person/event in standard reference knowledge**, not a verified
  in-repo citation.
- The sweeps were **selective by design** (family-head nodes, the Kmoch
  cluster, recognized venue anchors) — they are **not** an exhaustive
  type-F/G pass over all ~5,888 unattributed rows. The long tail of
  minor surnames (Cozio, Worrall, Knorre, Stoltz, Glek…) and a more
  sensitive token-normalised Lichess-vs-OCN misplacement detector are
  explicitly deferred (see Top-5 #5).
- Surnames spanning **multiple distinct openings** (Tarrasch 150 rows,
  Chigorin 75, Rubinstein 117, Steinitz 107) must be attributed
  **per-head, never blanket** — each finding below targets one head node.
- One node (`D.STa.Exc.MLn.Nxd5.Bb4.O-O`) could not have its move-order
  confirmed (transient tool-output gap mid-sweep); it is rated low and
  routed to deeper-source-review, not action.

## Candidate table

`blast` = estimated blast radius. All "proposal"/"review" items are
**strings-only on the named head row** unless noted; children inherit
the name and need no edit.

### Tier 1 — proposal candidates (source-gated)

| slug | current name | suspected issue | type | evidence | action | blast |
|---|---|---|---|---|---|---|
| `D.QGD.Cmb` | QGD, Cambridge Springs | ~~Textbook tournament anchor, empty attribution.~~ **✅ APPLIED 2026-05-30** (option A1, strings-only, head row only) — `attributed_to`/`attribution_source`/`historical_notes` set to the 1904-tournament event anchor; web-verified source (Panczyk & Ilczuk 2002), Oxford Companion not used (unseen). See [`qgd-cambridge-springs-attribution-proposal.md`](qgd-cambridge-springs-attribution-proposal.md). **First post-1.1 attribution applied.** | E (tournament anchor) | **high** | **DONE** | 1 row; 0 children touched |
| `B.Fre.Win` | French, Winawer | 3…Bb4 named for Winawer (1880s); empty `attributed_to`. Parallels the already-attributed `B.Fre.Exc.Uhl`/`B.Fre.Kor`. | A + B | medium | proposal | 1 row |
| `B.Ale` | Alekhine Defence | Introducer **is** the namesake (Budapest 1921); the 1921 game is a type-A `historical_notes` anchor. | A + B | medium | proposal | 1 row |
| `B.Sic.Tay` | Sicilian Taimanov | Taimanov's own system; dual alias Taimanov-Bastrikov signals a co-namer to reconcile. | C + B | medium | proposal | 1 row |
| `B.Sic.Ros` | Sicilian Rossolimo | 3.Bb5 = Rossolimo's signature weapon; qualifier should read *popularizer*, not inventor. | C + B | medium | proposal | 1 row |
| `B.Sic.Alp` | Sicilian Alapin | 2.c3 introduced/advocated by Alapin ~1900; `c3 Sicilian` descriptor alias already correctly placed. | C/A + B | medium | proposal | 1 row |
| `A.Tro` | Trompowsky Attack | 2.Bg5 championed by Trompowsky (1930s–40s); codification came decades later → qualifier *popularizer*. | C + B | medium | proposal | 1 row |
| `D.Tar` | Tarrasch Defence | QGD 3…c5 from Tarrasch's published theory. **QGD head only** — do not blanket the 150 "Tarrasch" rows. | B + C | medium | proposal | 1 row (head only) |
| `D.Chi` | Chigorin Defence | QGD …Nc6 from Chigorin's 19th-c practice. Keep distinct from the Ruy López Chigorin (separate head). | A/C + B | medium | proposal | 1 row (head only) |
| `C.RyL.Mar` | Ruy López, Marshall Attack | Classic game-anchor candidate (Capablanca–Marshall, New York 1918) — Berlin-Wall/Meran shape. | E + C | medium | proposal | 1 row |
| `B.Sic.Naj.Pol` | Sicilian Najdorf, Polugaevsky | Child eponym (7…b5) from Polugaevsky's own published analysis; parent Najdorf already attributed. | C/B | medium | proposal | 1 row |
| `D.QGD.Exc.Car` | QGD Exchange, Carlsbad | Carlsbad tournaments (1923/1929) venue/structure anchor; ~9 other "Carlsbad" alias rows must NOT be touched. | E (venue) + structure nuance | medium | proposal | 1 row (+ maybe MLn child) |

### Tier 2 — deeper-source-review (analyst/practitioner or place/DB ambiguity)

| slug | current name | the question | type | evidence | blast |
|---|---|---|---|---|---|
| `B.Sic.Cls.Rch` | Sicilian Classical, Richter-Rauzer | Reconcile dual eponym: Richter introduces (1930s) / Rauzer systematises. Name already canonical; enrich attribution only. | B + A/C | medium | 1 row |
| `C.RyL.Shl` | Ruy López, Schliemann (alias Jaenisch) | Priority vs popularity: Jaenisch (1840s) has priority, Schliemann the common label. Possible alias reorder. | B vs G | low | 1 row + alias order |
| `C.RyL.Zai` | Ruy López, Zaitsev | Separate Zaitsev-the-analyst (possible `attributed_to`) from Karpov-the-practitioner (type D `historical_notes` only). | C vs D | low | 1 row |
| `C.RyL.Brk` | Ruy López, Breyer | Breyer-idea claim itself needs a source; later popularisers (Spassky/Karpov) belong in `historical_notes`. | B/idea vs D | low | 1 row |
| `B.Sic.Kal` | Sicilian Kalashnikov | Is "Kalashnikov" a sourced eponym (B) or a DB/house label (G)? Far less documented than the adjacent Sveshnikov. | G vs B | low | 1 row if confirmed; else leave empty |
| `E.Nim.Cls.Zur` | Nimzo Classical, Zurich Variation | True Zurich event anchor (which event?) or generic geographic label (F/G)? | E vs F/G | low | 1 row (+≤3 children) |
| `E.Gru.Bg5` | Grünfeld, Stockholm Variation | Which Stockholm event, if any, fixed the name? Could be a DB label. | E vs F/G | low | 1 row |
| `D.Sem.Bg5.Mos.Hst` | Semi-Slav Moscow, Hastings Variation | Deep sub-line; "famous game illustrates ≠ anchor" applies. Likely `historical_notes`-only at most. | E vs G | low | 1 deep row |
| `C.RyL.Mor.Opn.Rig` | Ruy López Open, Riga Variation | Place/heritage label (Latvian analysts) vs documented event anchor — probably the former. | E vs B/F | low | 1 row (+≤3 children) |
| `D.QGD.Lsk.Ber.MdP` | QGD Lasker Bernstein, Mar del Plata Gambit | A *second* "Mar del Plata" outside the attributed KID line — do NOT copy the KID anchor across; needs its own source. | E vs F/G | low | 1 row |
| `D.STa.Exc.MLn.Nxd5.Bb4.O-O` | Semi-Tarrasch Kmoch, Castled Line | Name sits on the `.Exc.MLn` branch, not the sibling `.Kmo` branch — label drift, or genuine transposition? Move-order unconfirmed. | I/G | low | 1 row if drift; structural if misplaced (out of naming scope) |

### Tier 3 — ignore / keep (triaged, no defect) and cosmetic

| slug | current name | verdict | action |
|---|---|---|---|
| `C.PhD.d4.Nd7.Bc4.c6.Ng5` | Philidor Hanham Kmoch Variation | Eponym corpus-confirmed; only a comma-style nicety vs siblings. | **cosmetic-relabel** (optional) |
| `E.Nim.Rub.Kmo` | Nimzo Rubinstein, f3 Move Order | **Already remediated** (2026-05-28); no "Kmoch" survives. Methodology backlog still lists it open — this closes it. | ignore |
| `E.Nim.Sml.Kmo` | Nimzo Sämisch, a3 Move Order | The 1.1.0 I→H exemplar; verified still resolved. | ignore |
| `E.Nim.Sml.Kmo.MLn` | Nimzo Sämisch, e3 Main Line | Parent-chain quirk verified to read sensibly now; closeable as cosmetic. | ignore |
| `E.Nim.Fou` | Nimzo, 4.f3 (alias Kmoch Variation) | The legitimate Kmoch home (Lichess E20); correct as alias. | ignore |
| `D.STa.Kmo` | Semi-Tarrasch, Kmoch Variation | Lichess-confirmed real label (D41), correct family. | ignore |
| `B.Ale.Nrm.Bc4.Kmo` | Alekhine Defence, Kmoch Variation | Lichess-confirmed real label (B02), correct node. | ignore |
| `B.Sic.Naj.f4` / `B.Sic.Dra.Cls.Ams` | Najdorf/Dragon "Amsterdam" | One venue token reused across unrelated lines ⇒ DB convention, not a type-E anchor. | ignore |
| `C.RyL.Ber.Wal.End` | Berlin Wall, Endgame | Calibration exemplar re-verified correct (Kramnik / London 2000). | ignore |

## Top 5 recommended next audits

1. **`D.QGD.Cambridge Springs` (`D.QGD.Cmb`) — event anchor.** *Why next:*
   the single highest-confidence candidate, a textbook type-E venue
   anchor (Cambridge Springs 1904) that is strictly parallel to the
   already-attributed Meran / Mar del Plata / Catalan rows, yet has empty
   `historical_notes`/`attributed_to`. Closing it makes the catalogue's
   type-E treatment internally consistent. *Evidence needed:* one citable
   source tying the **name** to the 1904 event (Oxford Companion entry, or
   a specific Pillsbury/Marshall game from the tournament), phrased like
   `D.Cat`'s "named at the tournament". Strings-only on the head row; 12
   children inherit.

2. **`B.Fre.Win` (Winawer) — book-sourced eponym.** *Why next:* a
   marquee, uncontested single-person eponym whose siblings in the *same
   family* (`B.Fre.Exc.Uhl`, `B.Fre.Kor`) are already attributed with
   the exact `attribution_source` style — so this is a low-risk
   pattern-match that closes an obvious gap. *Evidence needed:* a
   French-defence monograph chapter naming the line for Winawer (not just
   "Winawer played it", which is the type-A `historical_notes` fact).

3. **`C.RyL.Mar` (Marshall Attack) — game anchor.** *Why next:* the
   strongest type-E *game*-anchor (vs venue) candidate, directly modelled
   on the Berlin Wall exemplar already in the catalogue. *Evidence
   needed:* the game/date/PGN-id (Capablanca–Marshall, New York 1918)
   **and** a source attesting the line is *named for / fixed by* that
   game — not merely that the moves occurred. If only "Marshall played
   it", downgrade to type-C `historical_notes`. The popular
   "Capablanca refuted it at the board" story must be checked, not
   assumed.

4. **`B.Ale` (Alekhine Defence) — introducer-is-namesake.** *Why next:*
   a clean type-A case where the introducer and the namesake coincide
   (Budapest 1921), making the attribution unusually well-defined — a
   good template for the introducer-is-namesake pattern (contrast
   Sveshnikov, where the namesake postdates the first game by 84y).
   *Evidence needed:* a source that the name derives from his 1921
   introduction; then `attributed_to` + a type-A `historical_notes`
   anchor are both defensible.

5. **Token-normalised Lichess-vs-OCN misplacement detector (tooling
   pass).** *Why next:* WS2 showed that an exact-string Lichess diff is
   too weak (≈3,910 hits dominated by phrasing differences) to surface
   real borrowed-label misplacements — yet the genuine Kmoch cases were
   exactly that kind of defect. *Evidence needed:* none yet — this is a
   **method** task: normalise both sides to family+sub-variation tokens,
   then flag eponyms present in OCN but on a *different node/ECO* than
   Lichess assigns. That detector is the principled way to find the next
   `E.Nim.*.Kmo`-style misplacement instead of guessing, and it would
   also drive the deferred long-tail player-eponym sweep.

## Non-goals

- **No transposition cleanup.** This audit does not touch `transposes_to`
  / `same_as` / `moves_uci` / `parent_ocn1` / `depth`. The transposition
  layer is settled at 1.1.0 (`unresolved_groups=0`).
- **No automatic relabel.** Nothing here is approved for apply; every
  candidate is source-gated and rides its own proposal + explicit GO.
- **No release regen / no tag move.** No downstream artefact regeneration
  is implied; this is a docs-only backlog.
- **No blanket attribution.** Multi-opening surnames are attributed
  per-head only.
- **Structural (slug/parent) misplacements** (e.g. the `D.STa.Exc…`
  question, if it proves real) are **migrations** governed at a release
  boundary, never inline naming edits — the QID Miles/Petrosian precedent.

## Appendix — raw subagent summaries (compressed, deduplicated)

**WS1 — player-eponym (15 findings).** Surfaced family-head nodes with a
sourceable eponym and empty `attributed_to`, calibrated against the 11
attributed rows. Clean single-person heads (Taimanov, Rossolimo, Alapin,
Trompowsky, Winawer, Tarrasch-QGD, Chigorin-QGD, Alekhine) → proposal;
Marshall → type-E game anchor → proposal; analyst/practitioner splits
(Zaitsev, Breyer) and dual eponyms (Richter-Rauzer, Jaenisch/Schliemann)
→ deeper-review; Kalashnikov flagged as possible DB label. Explicitly
*downgraded* "played-by-X" cases to `historical_notes`. Deferred the
long tail of minor surnames and the `D.Rub`/Colle-Zukertort overlap
(already its own proposal). No source strings asserted.

**WS2 — source/DB labels (6 findings).** A direct grep of the local
Lichess corpus for "kmoch" was **decisive and reversed the interim
hypothesis**: Lichess carries a real "Kmoch Variation" label in four
families (Nimzo E20, Alekhine B02, Semi-Tarrasch D41, Philidor C41), so
the OCN nodes carrying Kmoch in those families are **corpus-supported,
not borrowed-label red flags** → all "ignore". The only Kmoch red flags
were the two Nimzo move-order twins, **already remediated**. Net: no
strong new type-F/G demotions in the Kmoch cluster; one optional comma
cosmetic. Recommended a token-normalised detector as the right next pass
(→ Top-5 #5).

**WS3 — event/venue anchors (9 findings).** The catalogue is internally
inconsistent on type-E: four anchors are attributed but their siblings
with equally strong venue names are empty. Strongest: Cambridge Springs
(high) and Carlsbad (medium) → proposal. Weaker venue/place labels
(Zurich, Stockholm, Hastings, Riga, a second Mar del Plata) →
deeper-review, each needing a source distinguishing event-anchor (E)
from geographic/DB label (F/G). "Amsterdam" reused across unrelated
lines → ignore (DB convention). Berlin Wall re-verified as the correct
exemplar.

**WS4 — known residuals (8 findings).** Verified the three required
residuals **against the live CSV**: `E.Nim.Rub.Kmo` fully applied (no
"Kmoch" survives; this **closes** the methodology backlog item that still
lists it open); `E.Nim.Sml.Kmo.MLn` parent-chain reads sensibly →
closeable cosmetic; `E.Nim.Fou` Kmoch alias correctly intact. Remaining
catalogue "Kmoch" rows are genuinely different, corpus-legitimate
openings. One Semi-Tarrasch node (`D.STa.Exc.MLn.Nxd5.Bb4.O-O`) carries
"Kmoch" on a non-`.Kmo` branch — light source check (move-order
unconfirmed this run), not a fix.

## See also

- [`naming-attribution-audit-methodology.md`](naming-attribution-audit-methodology.md)
  — the *how* (types A–I, evidence rules, decision criteria).
- [`nimzo-rubinstein-kmoch-naming-proposal.md`](nimzo-rubinstein-kmoch-naming-proposal.md)
  — the first applied naming audit (the model proposal shape).
- [`agentic-development-playbook.md`](agentic-development-playbook.md)
  — why this ran as a dynamic workflow (wide discovery) and how each
  candidate becomes a GO-gated proposal.
- [`post-1.1-roadmap.md`](post-1.1-roadmap.md) — Track 1, where this
  backlog lives.
