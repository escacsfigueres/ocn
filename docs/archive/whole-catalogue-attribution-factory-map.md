# Whole-catalogue attribution factory map

**Status: DISCOVERY + PLANNING ONLY. No catalogue change, no manifest apply, no
tags/release.** Produced by a 12-agent read-only dynamic workflow over all 5,899
rows; the orchestrator re-verified every cited slug against `catalog/ocn-1.csv`
(407/409 exist; 2 agent-invented slugs dropped — see risk register). The goal is
to stop working *a cullereta* (one candidate at a time) and turn the catalogue
into a small set of homogeneous, source-gated **lots** plus the **tooling** that
makes future lots cheap.

## 1. Executive summary — how we scale

- **The shape of the problem:** 5,877 of 5,899 rows have an empty `attributed_to`;
  only 22 are attributed so far. One-at-a-time will never finish — and *most rows
  should never be attributed* (they are editorial descriptors, structures, or
  geographic families). The win is isolating the small attributable subset and
  batching it.
- **The factory model:** triage (done) → pick a homogeneous group → evidence
  sprint (source-gated) → manifest → `--dry-run` review → GO `--apply`. This doc
  supplies the *batchable work-packages* and the *tooling backlog* that feed that
  loop at scale.
- **The load-bearing structural rule:** the engine targets **exact slugs**, so a
  "full-family" attribution stamps the head's person onto *every* sub-row. That
  is only safe when the family is structurally homogeneous with **no distinct
  sub-eponyms**. Many families fail this (e.g. the French MacCutcheon family
  contains Janowski / Olland / Morozevich sub-lines). **Default to head-only**;
  treat full-family as the exception that needs a per-sub-row eponym check.
- **Yield this pass:** 10 candidate lots (6 *safe-if-sourced*, 4 *hold*), 5
  automation tools, a 21-family "do-not-touch" map, a source strategy, and a
  concrete 3-sprint plan. Each lot remains gated on a first-hand source and an
  explicit GO — the factory automates *triage and mechanics*, never *truth*.

## 2. Full-catalogue counts (orchestrator-computed, authoritative)

| ECO | rows | attributed | empty |
|---|---:|---:|---:|
| A | 1,311 | 2 | 1,309 |
| B | 1,367 | 11 | 1,356 |
| C | 1,445 | 2 | 1,443 |
| D | 870 | 5 | 865 |
| E | 906 | 2 | 904 |
| **Total** | **5,899** | **22** | **5,877** |

**Candidate classification (whole-CSV normalizers):**

- Person-name clusters: **141** — 66 `empty_likely_eponym`, 50
  `leaf_descriptor_no_head` (no head action), 15 `already_attributed`, **9
  `dangerous_multihead`** (never blanket), 1 false-positive.
- Non-person: **21** permanent-unattributed families, **3** genuine event
  anchors, **7** `historical_notes`-only enrichment candidates.
- Batchability of the 10 designed lots: **6 safe-if-sourced, 4 hold**.

## 3. Top 10 highest-yield lots (ranked)

All `attribution_fields_only`, all engine-automatable as-is. "Scope" = head-only
(attribute the family head) unless noted. QA verdict from the adversarial agent.

| # | Lot | ~rows | Scope | QA | Primary source to pin |
|---|---|---:|---|---|---|
| 1 | King's Gambit Accepted — Kieseritzky (`C.KGm.Acc.Kie`) + Allgaier (`C.KGm.Acc.All`) | 38 | full-family ⚠ | safe-if-sourced | OCC / Sunnucks |
| 2 | KGD Falkbeer (`C.KGm.Dec.Fal`) | 24 | **head-only** (was full-family) | **hold** | OCC 'Falkbeer' |
| 3 | ECO-A heads — Réti `A.Ret`, Bird `A.Bir`, Larsen `A.Lar`, Grob `A.Gro` | 4 | head-only | safe-if-sourced | OCC entries |
| 4 | Ruy López — Breyer `C.RyL.Brk` + Zaitsev `C.RyL.Zai` | 13 | full-family ⚠ | **hold** | MCO / OCC |
| 5 | French — MacCutcheon `B.Fre.Mac` + Burn `B.Fre.Bur` | 21 | **head-only** (sub-eponyms) | safe-if-sourced | OCC entries |
| 6 | QGD heads — Lasker `D.QGD.Lsk`, Ragozin `D.QGD.Rag`, Harrwitz `D.QGD.Har` | 3 | head-only | safe-if-sourced | OCC/Sunnucks (not a repertoire book) |
| 7 | Caro-Kann Karpov (`B.CaK.Kar`) | 17 | full-family ⚠ | **hold** | ECO B / MCO |
| 8 | Sämisch heads — `E.KID.Sml`, `E.Nim.Sml`, `E.Gru.Sml` | 3 | head-only (exact-slug) | safe-if-sourced | ECO E / monograph |
| 9 | Scotch Göring Gambit (`C.Sco.Gor`) | 13 | full-family | safe-if-sourced | OCC 'Göring Gambit' |
| 10 | ECO-E defence heads — `E.Nim`, `E.Gru`, `E.Blf` | 3 | head-only | **hold** (scope ambiguity) | OCC entries |

⚠ = full-family lots stamp the head's person onto every sub-row; before drafting,
confirm no sub-row carries a distinct eponym (else scope to head-only). The 4
**hold** lots each need a specific fix before becoming a manifest (see §8).

## 4. Top 5 tooling gaps to automate next

From the automation-gap agent (all small/medium effort, stdlib only):

1. **`scaffold_manifest`** (S) — generate a skeleton `ocn.attribution_manifest.v1`
   from a reviewed TSV slice of triage output, so an evidence sprint's sourced
   strings become an apply-ready manifest without hand-writing JSON.
2. **`source_status_table`** (S) — machine-readable per-head source-status table
   (which heads have a CLEAR source, which are PARTIAL), so picking the next
   sprint target stops being manual doc-scanning.
3. **`candidate_slice_export`** (S) — export a focused, sprint-ready candidate
   slice (small TSV/brief) from the triage map, so agents get *only* the relevant
   rows instead of the whole 5,899-row CSV.
4. **`docs_slug_verifier`** (S) — verify every backtick-quoted slug in `docs/`
   exists in the live catalogue (the agent reported ~67 stale slug refs across
   ~26 files). Makes `docs/` a reliable agent-context source.
5. **`lumbra_chronology_helper`** (M) — a reusable CLI for the Lumbra Gigabase
   chronology / first-appearance queries the evidence sprints already run ad-hoc.

## 5. "Do not touch" — the negative map

Categories that must stay **unattributed** (attributing them would be wrong, not
merely unsourced):

- **Permanent-unattributed families (21):** `B.Sic`, `B.Fre`, `A.Hol`, `A.Eng`,
  `C.Ita`, `D.Sla`, `D.Sem`, `B.Sca`, `C.LtO`, `A.Pol`, `A.Hng`, `E.KID`,
  `E.QID`, `E.Nim`, `E.Bog`, `E.OldI`, `E.Ind`, `A.EID`, `A.KIA`, `B.Sic.Dra`,
  `A.Hol.Sto` — geographic families, structures, and editorial descriptors.
- **Dangerous multi-head surnames — head-only, never blanket** (verified row
  counts): Nimzowitsch (~126), Rubinstein (~124), Steinitz (~110), Botvinnik
  (~60), Marshall (~53), Paulsen (~43), Keres (~40), Bogoljubow (~37), Lasker
  (~33). Each surname labels *several unrelated openings*; only a specific,
  sourced head may be attributed, one at a time.
- **`leaf_descriptor_no_head` (50 clusters):** descriptive variation labels with
  no introducing head — no attribution action.
- **Transposition layer:** `transposes_to` / `same_as` are CLOSED
  (`unresolved_groups=0`). The factory never touches them.

## 6. Source strategy — which sources unlock which lots

| Source | Kind | Unlocks |
|---|---|---|
| **NotebookLM (`nlm`)** grounded chess library | grounded book (high) | The workhorse: grounded "named after" passages (already unblocked Winawer, Carlsbad, Tarrasch, Chigorin). First stop for any eponym head. |
| **Lumbra Gigabase** `~/Downloads/GIGABASE/` | database (high) | Chronology / first-appearance dating only (introducer-vs-inventor, antedating). Never naming proof. |
| **Oxford Companion to Chess** (Hooper & Whyld) | secondary (med) | Encyclopedic eponym confirmation for most lots — but reached via Wikipedia footnotes, not first-hand (archive.org blocked). Treat as corroboration. |
| **Edward Winter / chesshistory.com** | grounded (med) | Deep single-eponym histories (Alapin, Taimanov, Schliemann). |
| **`external/lichess-openings`** | label-only (high) | Type-G label confirmation and misplacement detection — **never** a naming citation. |
| Panczyk & Ilczuk; Polugaevsky; Lissowski & Bogdanovich; Wikipedia | mixed | Single-item / corroboration sources tied to specific candidates. |

Rule unchanged: a Lichess label is type-G (label only); a repertoire book is not
a primary historical attribution source; only a grounded "named after" passage or
an encyclopedic entry is load-bearing.

## 7. Proposed next sprint (three tracks)

1. **Tooling sprint (do first, S-effort):** build `candidate_slice_export` +
   `scaffold_manifest` + `docs_slug_verifier`. These convert "send agents the
   whole CSV" into "send a verified slice", auto-draft manifests from sourced
   slices, and clean the ~67 stale doc slugs. Highest leverage for everything after.
2. **Evidence sprint (source-gate the safe lots):** a dynamic-workflow `nlm`/OCC
   pass over the **head-only, safe-if-sourced** lots first — Lot 3 (ECO-A heads),
   Lot 6 (QGD heads), Lot 8 (Sämisch heads), Lot 9 (Göring). One grounded passage
   per head; orchestrator re-verifies each.
3. **Manifest batch sprint (apply, GO-gated):** the first post-Lot-A real batch
   should be a head-only, low-risk lot whose sources cleared in track 2 — Lot 3
   (`A.Ret`, `A.Bir`, `A.Lar`, `A.Gro`) is the natural candidate. Dry-run, review
   the row-level diff, then GO `--apply`.

## 8. Risk register

**Systemic (from adversarial QA):**

- **Full-family stamping on dangerous-surname sub-rows** — lots 1, 4, 5, 7, 9
  propose full-family runs; some sub-rows carry *other* eponyms. Mitigation:
  default to head-only; for a full-family lot, verify every sub-row's
  `canonical_name` shares the head's eponym before drafting.
- **Slug-inventory discipline** — agents invented 2 slugs (NON-CATALOGUE:
  `C.KGm.Dec.Fal.MLn.Qd3`, `B.CaK.Kar.Kar.Kas`; a third, NON-CATALOGUE
  `C.RyL.Mor.Brk`, was cited and dropped). Every manifest must be slug-verified
  before apply; the engine already rejects unknown slugs, and `docs_slug_verifier`
  closes the gap in docs.
- **Homonym three-letter codes** — `Sml` = Sämisch in `E.*` but Smyslov in
  `D.Sla.Sml` / `B.CaK.Kar.Sml`. Mitigated by the engine's **exact-slug**
  targeting (never prefix wildcards); manifests must list explicit slugs.
- **`approx_rows` vs scope** — head-only lots (6, 8, 10) list ~3 rows but head a
  much larger family; the count is the *changed* rows, not the family size. State
  scope explicitly in each manifest.
- **Source grade** — do not accept a repertoire book (e.g. Avrukh) as the primary
  citation where an encyclopedic entry is needed (Lot 6 Harrwitz).

**Per-lot holds:** Lot 2 (drop invented slug; scope head-only), Lot 4 (decide
`C.RyL.Brk` sub-row handling), Lot 7 (fix invented note slug; list all family
slugs), Lot 10 (resolve whether `E.Blf.Acc` is in scope).

**Pre-existing catalogue issues surfaced (not for this doc to fix):**
`D.QGD.Har.Har` has a duplicated `canonical_name` ("QGD, Harrwitz Attack,
Harrwitz Attack"); ~67 stale slug references across ~26 docs. Log for a future
cleanup pass.

## See also

- [`naming-attribution-automation.md`](naming-attribution-automation.md) — the loop this map feeds.
- [`attribution-batch-engine.md`](attribution-batch-engine.md) — the apply engine + guardrails.
- [`parked-attribution-reference-source-log.md`](parked-attribution-reference-source-log.md) — verified source grades for the parked items.
- [`lot-a-player-eponyms-dry-run.md`](lot-a-player-eponyms-dry-run.md) — the first applied batch (Tarrasch, Chigorin).
