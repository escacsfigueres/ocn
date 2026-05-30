# Player-eponym attribution — batch proposal (post-1.1)

**Status**: **PROPOSED — no catalogue change.** A classification map of
player-eponym attribution candidates into *batch-safe* / *individual-proposal*
/ *deeper-review* / *ignore-keep*. **Dynamic workflow used: yes** (4
parallel read-only sweeps). It applies nothing; every item is gated on
its own proposal + first-hand evidence + explicit GO.

> **Headline: the safe batch is empty — but for a different reason than
> the venue batch.** There venue tokens were the wrong *kind* (F/G labels,
> not type-E anchors). Here the candidates are genuinely the right kind —
> classic single-person eponyms — but **no read-only agent opened a
> first-hand naming source** (a book chapter or a "named-for" attestation;
> the web tools were not loaded this run, and a Lichess label is type-G,
> proof of the label not of who named the line). Per the Cambridge Springs
> precedent (*never assert a source you have not seen*), **0 candidates
> are batch-safe right now.** The fix is small and known: each strong
> eponym needs **one focused first-hand citation**, after which it becomes
> an individual apply. The valuable output of this run is the
> **classification + surname risk map + house-style templates** that make
> those individual checks fast and safe.

## Method

A dynamic workflow ran **4 parallel read-only agents** over the live
5,899-row catalogue, calibrated against the 12 attributed rows (7 of them
player eponyms). Agents returned structured classifications and **edited
nothing**; the orchestrator consolidated and **re-verified all 19 cited
slugs against the CSV** (all exist with the quoted names; all candidate
heads have empty attribution).

| # | Workstream | Result |
|---|---|---|
| 1 | Tier-1 candidate triage (10 backlog eponyms) | all verified empty; 0 batch-safe; split individual-proposal vs deeper-review |
| 2 | House-style sweep (7 attributed eponyms) | extracted Tier-1 (rich) + Tier-2 (book-sourced) field templates; applied rows have no defects |
| 3 | Multi-opening surname risk map (18 surnames) | per-head decomposition; flags DANGEROUS vs MODERATE vs closest-to-safe |
| 4 | Evidence sweep (10 heads) | only type-G Lichess labels seen; **no first-hand naming source** → all deeper-review |

**Sources consulted:** `catalog/ocn-1.csv` (source of truth, all slugs
re-verified), the 7 attributed eponym rows verbatim, `external/lichess-openings`
(confirms labels = type G, not attribution), methodology + backlog. **No
web** (WS4's web tools were not loaded this run — the key limitation; see
below). `nlm` not invoked this run.

**Limitations:**

- **No first-hand naming source was opened for any candidate.** This is
  *the* gate. WS4's web tools were unavailable this run, and no printed
  openings reference is in-repo, so every "named-for-X" claim rests on
  model recall + a type-G label — insufficient to apply.
- Surname counts are over `canonical_name` substrings in *this* catalogue;
  the methodology's larger figures count a broader label space.
- Each agent self-corrected one or two premature mid-run outputs (a
  recurring tool-output-ordering artifact); the final structured results
  are first-hand-verified and are what this proposal uses.

## A. Batch-safe candidates

**None.** No candidate has a first-hand source tying its **name** to the
person. Manufacturing a batch here would mean asserting unseen citations —
exactly the failure mode the track exists to prevent.

## B. Individual-proposal candidates (strong eponym, needs ONE seen citation)

These are clean, low-controversy, single-or-dominant-head eponyms. Each
is apply-ready *after* one focused first-hand citation (a monograph/chapter,
or a dated game for the game-anchor) — the same shape as the Cambridge
Springs cycle.

| slug | current name | type (provisional) | the one check needed | blast |
|---|---|---|---|---|
| `B.Fre.Win` | French, Winawer | A/C (Winawer, 1880s) | a French-defence chapter naming the line for Winawer; siblings `B.Fre.Exc.Uhl`/`B.Fre.Kor` already attributed in-family with book chapters → ideal template match | head only (8 surname rows; do not touch children) |
| `A.Tro` | Trompowsky Attack | A/C (Trompowsky, 1930s–40s) | **closest-to-safe of the whole set** — all 26 rows under the single head `A.Tro`, zero reuse; need one source + check the Pomar/Opocensky co-naming nuance | head only |
| `B.Sic.Ros` | Sicilian Rossolimo | C popularizer (3.Bb5) | source distinguishing *popularizer* from inventor; dominant head (17/18 rows) | head only |
| `C.RyL.Mar` | Ruy López, Marshall Attack | **E game-anchor** (Capablanca–Marshall, NY 1918) | the game (date/players/id) **plus** a source attesting the line is *named-for* it — else downgrade to type-C `historical_notes`. Routed here from the venue batch | head only (multi-opening "Marshall" surname — per-head) |
| `B.Ale` | Alekhine Defence | A introducer-is-namesake (Budapest 1921) | a source that the name derives from his 1921 introduction → unusually clean type-A template | head only (multi-opening; QGA Alekhine is a separate head) |
| `B.Sic.Naj.Pol` | Sicilian Najdorf, Polugaevsky | A/B (his own published 7…b5 analysis) | his *Grandmaster Preparation* is the natural seen source; deep child of the already-attributed Najdorf | head only (deep child) |

## C. Deeper-review candidates (ambiguous type or multi-head risk)

| slug | current name | why deeper-review |
|---|---|---|
| `B.Sic.Tay` | Sicilian Taimanov | type-C but origin of the *name* undocumented; alias "Taimanov-Bastrikov" signals a co-namer to reconcile; multi-head surname |
| `B.Sic.Alp` | Sicilian Alapin | naming mechanism (own publication vs later naming) historically debated; "Alapin" labels ≥6 unrelated openings |
| `D.Tar` | Tarrasch Defence | strong type-B at the QGD head, **but** "Tarrasch" = ~150 rows across ≥3 distinct namesake heads (`D.Tar`, `D.STa` Semi-Tarrasch, `B.Fre.Tar` French Tarrasch) → individual-proposal at best, never batch |
| `D.Chi` | Chigorin Defence | QGD head defensible, **but** keep strictly distinct from the Ruy López Chigorin (`C.RyL.Cha`) — two independent primary heads |

## D. Ignore / keep

**The 7 attributed eponyms — no action** (calibration set, no defects):
`B.Sic.Naj`, `B.Sic.Sve`, `B.Sic.Sve.Bxf6.Nd5.Bg7`, `E.Ben.Bnk`,
`B.Fre.Exc.Uhl`, `A.KIA.Fre.Bar`, `B.Fre.Kor`. WS2 confirmed the
book-sourced trio's empty `historical_notes` is *by design* (methodology
line 111), not a defect — explicitly **not** a change candidate.

**Leaf-reuse surnames with NO eponym head** (every appearance is an
"X Variation" inside someone else's opening → no head to attribute):
**Spassky** (20 rows), **Smyslov** (27), **Pillsbury** (13). Per-leaf
only if ever pursued; not a batch.

## Surname risk map (WS3 — the reusable safety artifact)

Counts = `canonical_name` substring matches in this catalogue. **Never
blanket-attribute a surname; attribute one specific head.**

| surname | rows | risk | the legitimate primary head(s) |
|---|---|---|---|
| Tarrasch | 150 | **DANGEROUS** | `D.Tar` + `D.STa` + `B.Fre.Tar` (3 distinct heads) |
| Alekhine | 127 | **DANGEROUS** | `B.Ale` (defence) primary; dozens of reuse leaves |
| Rubinstein | 117 | **DANGEROUS** | `D.Rub`, `E.Nim.Rub`, `B.Fre.Rub` … (≥9 heads) |
| Steinitz | 107 | **DANGEROUS** | no single head — `B.Fre.Stn` + Ruy/Scotch/Vienna/… |
| Chigorin | 75 | **DANGEROUS** | `D.Chi` (defence) + `C.RyL.Cha` (Ruy) |
| Winawer | 59 | MODERATE | `B.Fre.Win` dominant |
| Najdorf | 58 | settled | `B.Sic.Naj` (already attributed) |
| Alapin | 54 | **DANGEROUS** | `B.Sic.Alp` + ≥5 others |
| Marshall | 50 | **DANGEROUS** | `C.RyL.Mar` (Attack) primary; "Marshall Gambit" ≠ same |
| Taimanov | 35 | **DANGEROUS** | `B.Sic.Tay` primary; Nimzo/KID/Benoni/QID separate |
| Bogoljubow | 33 | **DANGEROUS** | true primary `E.Bog` (canonicalised "Bogo-Indian", outside the surname match-set) |
| Trompowsky | 26 | **closest-to-safe** | `A.Tro` — single head, zero reuse |
| Rossolimo | 18 | MODERATE | `B.Sic.Ros` dominant |
| Pillsbury | 13 | leaf-reuse | no head |
| Polugaevsky | 4 | MODERATE | `B.Sic.Naj.Pol` primary; QID Polugaevsky Gambit separate |
| Spassky / Smyslov | 20 / 27 | leaf-reuse | no head |

## Recommended first batch

**No batch.** Instead, the highest-yield next step is a **single
source-gated individual proposal**, pick-one:

1. **`A.Tro` (Trompowsky)** — structurally the safest (single head, zero
   reuse); needs one source + the co-naming nuance. *Recommended first.*
2. **`B.Fre.Win` (Winawer)** — best template match (attributed siblings
   in-family with book chapters).
3. **`C.RyL.Mar` (Marshall)** — highest-profile, but type-E game-anchor →
   needs the game *and* a "named-for" source; slightly more work.

Run it exactly like Cambridge Springs: find **one first-hand source**
(web allowed at that point) → confirm type → apply 3 strings to the head
row only → validate → GO push. Expected impact: **≤1 row**, strings-only,
0 children, audit counts unchanged.

If you'd rather batch, the only honest way is a **short evidence sprint
first** (give an agent web access to find one citation each for the 6
Group-B heads), *then* a 3–6 row batch — but that is "find sources then
apply", never "apply on recall".

## Risk controls (carried from prior cycles)

- **No blanket surname attribution** — attribute one head; the risk map
  above is the guard.
- **No "played by X" ⇒ "named after X"** — a surname in the name is not a
  source.
- **No unseen source as primary `attribution_source`** — Lichess is type-G
  (label only); model recall is not a citation. (Cambridge Springs precedent.)
- **No child-row churn** — head row only; children inherit.
- **No transposition / slug / FEN / relation changes** — attribution is
  strings-only on the three attribution columns.
- **Honest empty beats invented** — every Group-C/D row stays empty until sourced.

## House-style templates (WS2 — for the eventual single applies)

**Tier 1 — rich eponym (dating needs reconciling):**
```
attributed_to      = <Name> (<role: systematiser | modern systematiser | popularizer | early adopter>)
                     [dual:  <NameA> (<role>); <NameB> (<role>)]
attribution_source = <Author>, '<Monograph>' (<Publisher>, <year>)   — or — <eponym>'s own analyses/practice from <decades>; the variation bears his name in standard literature.
historical_notes   = <corpus first appearance Player–Player Year> … <namesake's later advocacy> … the line is named for the <systematiser>, not the first player. <corpus top scorer>.
```
(Canonical antedating exemplar: Sveshnikov — corpus 1888 vs namesake 1972, ~84y.)

**Tier 2 — book-sourced eponym (no reconciliation needed):**
```
attributed_to      = <Full Name>            (bare, NO role qualifier — sanctioned by methodology line 111)
attribution_source = <Author>, <Book Title>, chapter '<chapter>'.
historical_notes   = (empty — by design)
```
(Models: `B.Fre.Exc.Uhl`, `A.KIA.Fre.Bar`, `B.Fre.Kor`.) En-dash `–`
(U+2013) for player/game pairs.

## Next action

- **Recommended:** GO a single source-gated proposal — **`A.Tro`** first
  (or `B.Fre.Win`).
- **Do NOT** request a batch apply — nothing is batch-safe on current evidence.
- **Optional:** GO an *evidence sprint* (agent with web) to gather one
  citation per Group-B head, converting B into a real 3–6 row batch.

## See also

- [`naming-attribution-audit-methodology.md`](naming-attribution-audit-methodology.md)
  — types A–I, evidence rules, the role-qualifier convention.
- [`qgd-cambridge-springs-attribution-proposal.md`](qgd-cambridge-springs-attribution-proposal.md)
  — the source-gated single-apply template this would follow.
- [`event-venue-attribution-batch-proposal.md`](event-venue-attribution-batch-proposal.md)
  — the prior batch (also "no batch-safe", different reason).
- [`naming-attribution-audit-backlog.md`](naming-attribution-audit-backlog.md)
  — the candidate backlog this refines.
