# Event / venue / game-anchor attribution — batch proposal (post-1.1)

**Status**: **PROPOSED — no catalogue change.** A map of event/venue/game
anchor attribution candidates, classified into *batch-safe* vs
*individual-proposal* vs *ignore*. **Dynamic workflow used: yes** (4
parallel read-only sweeps). It applies nothing and is gated on the usual
proposal + evidence + explicit GO.

> **Headline: the safe batch is empty.** The sweeps converged on a clear
> negative — **no candidate is batch-safe.** Every venue/place name found
> is a positional/structure or ECO-DB label (type F/G), *not* a type-E
> event anchor with a source tying the **name** to an event. This is the
> correct, methodology-consistent result ("an honest empty `attributed_to`
> beats an invented one"), and it is more useful than a forced batch: it
> stops us from inventing attributions. The recommended next action is
> **at most one individual proposal (Carlsbad), source-gated** — not a
> batch.

## Method

A dynamic workflow ran **4 parallel read-only agents** over the live
5,899-row catalogue, calibrated against the 5 attributed venue/event
exemplars (`D.Cat`, `D.Sem.Mer`, `E.KID.Cls.Mar`, `C.RyL.Ber.Wal.End`,
`D.QGD.Cmb`). Agents returned structured classifications and **edited
nothing**; the orchestrator consolidated and re-verified every cited slug
against the CSV (all 6 candidates exist with empty attribution; all 5
exemplars confirmed attributed).

| # | Workstream | Result |
|---|---|---|
| 1 | Venue/tournament anchor sweep (484 venue-token hits) | **0 batch-safe**; tokens are F/G structure/place labels |
| 2 | Famous-game / match anchor sweep | **0 batch-safe**; Marshall is a *player* eponym, not an event anchor |
| 3 | House-style / consistency sweep | extracted reusable field templates; 5 exemplars consistent, no defects |
| 4 | Evidence / source sweep | **no first-hand event source** for any candidate; Lichess = label only (G) |

**Sources consulted:** `catalog/ocn-1.csv` (source of truth, every slug
re-verified), the 5 attributed exemplars verbatim, `external/lichess-openings`
(confirms the *labels* exist but ties no name to an event — it is a type-G
label source, not an attribution source), and the methodology/backlog.
**No web used** (no candidate rose to high-priority-with-thin-local in a
way that justified web before this scoping decision).

**Limitations:**

- Discovery, not arbitration: no agent located a binding first-hand
  source tying any candidate's **name** to an event. Web was deliberately
  not used at this stage; a single individual proposal (Carlsbad) could
  justify it later.
- The sweep covered name/alias/notes tokens; a name whose event-origin
  lives only in an unindexed book would be missed (exactly why the
  recommendation is *source-gated*, not *apply*).
- The strict bar ("source must tie the NAME to the event, not merely that
  moves occurred there") is intentional and is why the batch is empty.

## A. Batch-safe candidates

**None.** No candidate meets the bar (homogeneous type-E, high evidence,
a first-hand source tying the name to an event). This row exists to record
that the batch was genuinely sought and is empty — not skipped.

The reasoning, in one line: the three game/venue exemplars each cite a
specific `Player–Player, Venue Year` (Meran → Rubinstein–Tartakower 1924;
Mar del Plata → Najdorf–Gligorić 1953; Berlin Wall → Kasparov–Kramnik
2000) or a named-at-event source (Catalan → Barcelona 1929). **None of
the six candidates carry any such event link** — their notes are purely
positional/structural.

## B. Individual-proposal candidates (source-gated, not batched)

| slug | current name | why individual, not batch | anchor kind | evidence | next |
|---|---|---|---|---|---|
| `D.QGD.Exc.Car` | QGD Exchange, Carlsbad | The strongest of the six — the "Carlsbad structure" is a genuinely recognised concept tied to Carlsbad 1923. **But** "Carlsbad" names a *pawn structure*, reused across 7 unrelated rows (Caro-Kann Panov, Nimzo Spielmann, Dutch Fianchetto) — the F/G reuse signature. At most a `historical_notes` structure-origin note, **not** a clean type-E `attributed_to`. | structure/event label | medium | **individual proposal, gated on a first-hand QGD monograph / Oxford Companion read directly** (not the unseen-OC mistake we avoided for Cambridge Springs) |
| `C.RyL.Mar` | Ruy López, Marshall Attack | A **player eponym** (Frank Marshall), not an event anchor. The famous Capablanca–Marshall, New York 1918 game is its unveiling → belongs in `historical_notes`, not as the naming basis. | player eponym (B/C) + famous game (A) | medium | **route to the player-eponym track**, not this event batch |

## C. Already-good / ignore

Two groups:

**Already attributed (the calibration exemplars — no action):**
`D.Cat`, `D.Sem.Mer`, `E.KID.Cls.Mar`, `C.RyL.Ber.Wal.End`, `D.QGD.Cmb`.
WS3 confirmed they are structurally consistent; the only structural
variant is the *person-less* `D.QGD.Cmb` template (correct for an event
anchor with no namesake). No applied row needs fixing.

**Confirmed F/G place labels — leave `attributed_to` empty:**

| slug | current name | why ignore |
|---|---|---|
| `E.Nim.Cls.Zur` | Nimzo Classical, Zurich Variation | "Zurich" reused for the unrelated `D.QPG.Zur` Zurich Gambit — generic place/ECO label, no event link |
| `E.Gru.Bg5` | Grünfeld, Stockholm Variation | "Stockholm" reused for the Dragon Stockholm Attack — generic label |
| `C.RyL.Mor.Opn.Rig` | Ruy López Open, Riga | likely Riga-milieu / player association, not a single event; "played-by ≠ named-after" |
| `D.Sem.Bg5.Mos.Hst` | Semi-Slav Moscow, Hastings Variation | Hastings = annual congress over decades, the opposite of a single-event anchor; deep ECO sub-line label |

## Recommended first batch

**No batch.** Per the evidence, the recommendation is:

1. **Apply nothing as a batch.** There is no honest homogeneous type-E set.
2. **Open at most ONE individual proposal: `D.QGD.Exc.Car` (Carlsbad)** —
   and only if a first-hand source (a QGD monograph chapter, or the Oxford
   Companion read directly) ties the *name* to Carlsbad 1923. Likely
   outcome is a `historical_notes` structure-origin note rather than a
   type-E `attributed_to`, because "Carlsbad" is a structure label.
3. **Leave the four F/G place labels empty.** Honest empty beats invented.
4. **Route `C.RyL.Mar` (Marshall) to the player-eponym track**, not here.

Expected impact of the recommended path (if/when Carlsbad is later
applied as a single row): **≤1 catalogue row** touched, strings-only,
**0 children**, audit counts unchanged (`unresolved_groups=0`,
`multiple_canonical_groups=17`, rows 5,899), no transposition semantics
affected. **Nothing is applied by this document.**

## House-style templates (extracted by WS3, for future single applies)

For when a candidate *does* clear the source bar:

**Person anchor (game/venue):**
```
attributed_to      = <Person> (<role: key game | resurrector | systematiser>)
attribution_source = <Player>–<Player>, <Venue> <Year>; <one line on how the name arose>.
historical_notes   = <pre-history / first appearance> … but <why this event/person fixed the name> … <corpus colour>.
```

**Person-less event anchor (the Cambridge Springs template):**
```
attributed_to      = Named at the <Venue> <Year> tournament (no individual eponym)
attribution_source = Named for the <Venue> <Year> international tournament (<place>), where <line> was played in several games (<Player–Player, …>); cf. <first-hand source>.
historical_notes   = <line> takes its name from the <Venue> <Year> tournament … The idea predates the event (<pre-history>) … Sub-lines carry later eponyms (…).
```

Use the en-dash (`–`, U+2013) for player pairs, matching the existing
rows.

## Risk controls (carried from the Cambridge Springs cycle)

- **No child rows** touched unless a child is *explicitly* justified (none
  here).
- **No inferred attribution** from a famous game merely occurring in a
  line — "occurs in" is `historical_notes`, never `attributed_to`.
- **No source asserted as primary `attribution_source` unless read
  first-hand** — the reason the unseen Oxford Companion was dropped for
  Cambridge Springs, and the reason Carlsbad stays gated.
- **No transposition / slug / FEN / relation changes** — attribution is
  strings-only on `attributed_to` / `attribution_source` /
  `historical_notes`.
- **Honest empty beats invented** — the default for every F/G label.

## Next action

- **If you accept the recommendation:** no apply; optionally **GO a single
  Carlsbad proposal** with an explicit instruction to find a first-hand
  source (web allowed at that point).
- **Do NOT** request a batch apply — there is nothing batch-safe to apply.
- The Marshall Attack belongs to the **player-eponym sweep** (backlog Tier
  1: `B.Fre.Win`, `B.Ale`, `B.Sic.Tay/Ros/Alp`, `A.Tro`, `D.Tar`/`D.Chi`,
  `B.Sic.Naj.Pol`, `C.RyL.Mar`), which is the more productive next batch
  than event/venue.

## See also

- [`naming-attribution-audit-methodology.md`](naming-attribution-audit-methodology.md)
  — type-E evidence rules (the bar this batch failed to clear).
- [`qgd-cambridge-springs-attribution-proposal.md`](qgd-cambridge-springs-attribution-proposal.md)
  — the one applied event anchor and its person-less template.
- [`naming-attribution-audit-backlog.md`](naming-attribution-audit-backlog.md)
  — the full candidate backlog (player-eponym track is the better next batch).
