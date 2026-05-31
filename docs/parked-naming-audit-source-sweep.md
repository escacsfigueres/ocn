# Parked naming-audit — source sweep (post-1.1)

**Status**: **SOURCE SWEEP — Maróczy Bind 3-row batch APPLIED 2026-05-31;
the rest remain parked.** A source-gated grading of the parked
naming-audit items (Winawer, Maróczy Bind, Carlsbad, deeper-review
eponyms). **Dynamic workflow used: yes** (5 parallel web-enabled
read-only agents; one transient failed launch, then a clean re-run). The
one CLEAR result — the 3 Maróczy Bind heads — was applied; Winawer,
Carlsbad, Taimanov, Alapin, Tarrasch, Chigorin stay PARTIAL/parked.

> **APPLIED 2026-05-31** (strings-only, head rows only): `B.Sic.Acc.Mar`,
> `B.Sic.Kan.Mar`, `B.Sic.OKe.c4` — `attributed_to = "Géza Maróczy
> (popularizer)"`, shared `attribution_source` (Winter / Oxford Companion
> / Swiderski–Maróczy 1904), per-move-order `historical_notes` (each notes
> Maróczy never played the bind as White). Verified:
> `CHANGED_ROWS` = exactly those 3, 0 children, 0 parked items touched,
> rows still 5,899, `unresolved_groups=0`.

> **Headline: one CLEAR batch emerged — the 3 Maróczy Bind heads — while
> everything else stays PARTIAL.** The Maróczy agent reached a
> reference-grade source first-hand (Edward Winter, *Géza Maróczy*,
> chesshistory.com — independently re-verified by the orchestrator), so
> the three Bind heads (`B.Sic.Acc.Mar`, `B.Sic.Kan.Mar`, `B.Sic.OKe.c4`)
> grade **CLEAR** and form a homogeneous **3-row batch-apply candidate**
> (one eponym, one source). The six player/place items (Winawer, Carlsbad,
> Taimanov, Alapin, Tarrasch, Chigorin) remain **PARTIAL** — uncontested
> secondary agreement but no reference-grade read; by the Winawer rule we
> hold those. Grade tally: **3 CLEAR · 9 PARTIAL · 3 INSUFFICIENT** (the
> INSUFFICIENT are chronology-stream and descriptor-child rows, not new
> defects). The sweep's value is a precise **upgrade map**: each parked
> item needs exactly one first-hand reference read to become applyable.

## Method

5 parallel read-only agents (web + Lumbra + `nlm` allowed), each grading
its items CLEAR / PARTIAL / INSUFFICIENT against the rule *"a game
database proves played/when, never named-after; secondary agreement is
PARTIAL, not shippable."* Agents edited nothing; the orchestrator
re-verified every slug against the CSV and consolidated.

**Sources reached first-hand:** the catalogue rows; Wikipedia (French
Defence, Maróczy Bind, Taimanov, Alapin, Tarrasch, Chigorin, Carlsbad
1923); Edward Winter "The French Defence" (read in full); Lumbra Gigabase
chronology. **Reference-grade targets NOT reached:** Oxford Companion
entries (Winawer/Maróczy/Taimanov/Alapin/Tarrasch/Chigorin), *The Wizard
of Warsaw* biography, Kmoch/Pachman pawn-structure monographs.

**A fabrication caught (important):** an earlier WebSearch *summary* in a
prior session paraphrased Edward Winter as saying the Winawer was "named
after Szymon Winawer, who won a game … Paris 1878." A first-hand WebFetch
of Winter's actual page (×3) shows **that sentence is not there** — it was
a summarizer fabrication. It is **not** cited anywhere, and "Paris 1878"
must not be encoded (it also conflicts with the Lumbra-verified
Steinitz–Winawer **Paris 1867**). This is exactly why the standard is
*first-hand reads only*.

**Limitations:** grades reflect *first-hand reference-grade* availability,
not whether the naming is true (it is uncontested for all). Chronology is
TYPE support only. Counts are ballpark.

## Per-item grades

| item | slug(s) | grade | type | action | the one upgrade read |
|---|---|---|---|---|---|
| **Winawer** | `B.Fre.Win` | PARTIAL | C early-practitioner (person) | keep-parked | Oxford Companion 'Winawer' **or** *Wizard of Warsaw* |
| **Maróczy Bind** | `B.Sic.Acc.Mar`, `B.Sic.Kan.Mar`, `B.Sic.OKe.c4` | **CLEAR** | C popularizer (Géza Maróczy) behind a structure label — named via Swiderski–Maróczy, Monte Carlo 1904 + his journalism; *he never played it as White* | **batch-apply candidate** (homogeneous 3-head set, one source) | already sourced (Winter, *Géza Maróczy*, chesshistory.com — verified first-hand) |
| **Carlsbad** | `D.QGD.Exc.Car` | PARTIAL | E/H **non-person** place/structure label → `attributed_to` stays EMPTY | individual-proposal (`historical_notes` only) | Kmoch *Pawn Power* / Pachman structure monograph |
| **Taimanov** | `B.Sic.Tay` | PARTIAL | C eponym (Mark Taimanov; co-namer Bastrikov) | individual-proposal | Oxford Companion 'Taimanov' |
| **Alapin** | `B.Sic.Alp` | PARTIAL | B/C eponym (Semyon Alapin, 2.c3) | individual-proposal | Oxford Companion 'Alapin' |
| **Tarrasch** | `D.Tar` (QGD head only) | PARTIAL | B/C eponym (Siegbert Tarrasch) | individual-proposal | Oxford Companion 'Tarrasch' |
| **Chigorin** | `D.Chi` (QGD head only) | PARTIAL | A/C eponym (Mikhail Chigorin) | individual-proposal | Oxford Companion 'Chigorin' |

All head-row only; all current attribution fields verified **empty**.

**Multi-head risk (per-head, never blanket):** Winawer also labels Slav
Countergambit `D.Sla.Win` + Three Knights `C.Thr.Win` (separate, not the
same person-claim); Tarrasch = 3 distinct heads (`D.Tar`/`D.STa`/`B.Fre.Tar`);
Chigorin = `D.Chi` + Ruy López `C.RyL.Cha`; Taimanov/Alapin span several
families; "Carlsbad" reused across 7 structure-label rows; Maróczy Bind =
3 heads of the *same* eponym (the one coherent set). Spelling split
**Maróczy vs Maroczy** flagged as a cosmetic consistency question only —
**no `canonical_name` change proposed here.**

## Chronology (Lumbra — TYPE support only, not naming proof)

- **Alapin** 2.c3 in corpus 1890s–1900s → early-practitioner/advocate.
- **Tarrasch** 3…c5 from the 1880s; Tarrasch's own use late 19th c → B/C.
- **Chigorin** …Nc6 from 1880s–90s; his own practice → A/C.
- **Taimanov** modern line (~1950s); idea-predates not applicable → C.
- **Maróczy Bind** c4-clamp associated with Maróczy from the early 1900s.

Each supports `historical_notes` + the attribution *type*; none is a
naming source.

## Batch analysis

**No homogeneous batch is apply-ready** (all PARTIAL). The only
*structurally* homogeneous set is **Maróczy Bind** — 3 heads
(`B.Sic.Acc.Mar`, `B.Sic.Kan.Mar`, `B.Sic.OKe.c4`) sharing **one eponym
(Géza Maróczy) and one structure**, so a **single Oxford Companion
'Maróczy' read** could unlock a clean 3-row batch in one step. The six
player/place items are otherwise independent individual proposals, each
gated on its own single reference read.

This is the same shape as the player-eponym batch before its evidence
sprint: the *naming* is settled; the bottleneck is **sourcing**, and the
good unit is "find one reference per item," not "apply one row."

## Top next actions (max 3, ranked)

1. **Maróczy Bind 3-row batch — ✅ APPLIED 2026-05-31.** The only
   apply-ready item; done (strings below, head rows only). Resolved the
   one mis-filed case the taxonomy flagged (structure-that's-really-a-
   person).
2. **Oxford Companion 'Winawer' read → close Group B 6/6.** One first-hand
   read lifts the last Group-B PARTIAL to CLEAR; proposal + fields already
   drafted.
3. **Batch the four deeper-review eponyms via one Oxford Companion sprint**
   (Taimanov, Alapin, Tarrasch-QGD, Chigorin-QGD) — if the OC is reachable
   first-hand, all four upgrade together (per-head strings), the same way
   the Group-B evidence sprint worked.

### Maróczy Bind — drafted apply strings (CLEAR; for a future GO apply)

Head rows only (`B.Sic.Acc.Mar`, `B.Sic.Kan.Mar`, `B.Sic.OKe.c4`), the 3
empty attribution fields each; en-dash `–`:

```
attributed_to      = Géza Maróczy (popularizer)
attribution_source = Edward Winter, 'Géza Maróczy' (chesshistory.com) / 'Kings, Commoners and Knaves' (1999); Hooper & Whyld, 'The Oxford Companion to Chess' (2nd ed., 1992). First recognised master game: Swiderski–Maróczy, Monte Carlo 1904.
historical_notes   = The c4+e4 clamp denying Black the ...d5 and ...b5 breaks, named for Géza Maróczy — who, notably, never played it as White. The name attaches via the first master game in which the bind gained recognition (Swiderski–Maróczy, Monte Carlo 1904, Maróczy as Black) and his subsequent journalism (Wiener Schachzeitung, 1906); by the 1920s permitting the bind was treated as a strategic error. A popularizer, not the inventor.
```

The three rows share the source; each `historical_notes` may note its
own move order (Accelerated Dragon / Kan / O'Kelly). `attributed_to` is a
person here — correct, because the Bind is a person-eponym wearing a
structure label (the taxonomy's flagged exception).

The common dependency is a **first-hand Oxford Companion read** (the
archive.org "W"/entry pages have resisted WebFetch twice). If that source
stays unreachable, these remain honestly parked — which is the correct
outcome, not a failure.

## Source appendix

- Catalogue rows — `catalog/ocn-1.csv` (all slugs verified, fields empty).
- Wikipedia: *French Defence*, *Maróczy Bind*, *Géza Maróczy*, *Taimanov
  Variation*, *Alapin*, *Tarrasch Defense*, *Chigorin Defense*, *Carlsbad
  1923* (all secondary; no inline reference-grade citations).
- Edward Winter, *The French Defence* (chesshistory.com) — read first-hand;
  does **not** treat the Winawer naming (only a Euwe–Gligorić sub-line).
- *The Wizard of Warsaw* (Lissowski & Bogdanovich, Elk and Ruby) — exists;
  body text not obtained.
- Lumbra Gigabase — chronology support (dated games), not naming proof.

## See also

- [`naming-attribution-audit-methodology.md`](naming-attribution-audit-methodology.md) — the CLEAR/PARTIAL evidence rules.
- [`player-eponym-group-b-evidence-sprint.md`](player-eponym-group-b-evidence-sprint.md) — the sourcing-then-apply template these would follow.
- [`french-winawer-attribution-proposal.md`](french-winawer-attribution-proposal.md) — Winawer's standing proposal (PARTIAL).
- [`non-person-opening-name-taxonomy.md`](non-person-opening-name-taxonomy.md) — flagged Maróczy Bind (person) and Carlsbad (structure).
