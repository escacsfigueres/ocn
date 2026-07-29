# Player-eponym Group B — evidence sprint (post-1.1)

**Status**: **APPLIED 2026-05-30** (5-row batch, strings-only, head rows
only). Web-enabled sourcing for the 6 Group-B player-eponym heads + a
Lumbra chronology addendum. **Dynamic workflow used: yes** (6 parallel
web-enabled agents). The 5 batch-ready rows (`A.Tro`, `B.Ale`,
`B.Sic.Ros`, `C.RyL.Mar`, `B.Sic.Naj.Pol`) were applied with the refined
strings below; **`B.Fre.Win` remains PARTIAL / held** (no reference-grade
naming source yet). Verified: `CHANGED_ROWS` = exactly those 5, 0 child
rows, rows still 5,899, `unresolved_groups=0`.

> **Result: the sprint worked — a 5-row sourced batch is now possible.**
> Unlike the prior discovery run (which returned "no batch" because web
> tools were off), this sprint found real naming citations, and the
> follow-up **Lumbra Gigabase chronology addendum** (see bottom) firmed up
> the attribution *types*. **Five heads clear our bar** — `A.Tro`
> (Trompowsky), `B.Ale` (Alekhine), `B.Sic.Ros` (Rossolimo), `C.RyL.Mar`
> (Marshall), `B.Sic.Naj.Pol` (Polugaevsky) — each with a naming source
> *and* a dated corpus chronology confirming popularizer/introducer (not
> inventor). Only **`B.Fre.Win` (Winawer)** stays PARTIAL, pending one
> reference-grade naming citation.
>
> **Note (supersedes the "3-row" framing below):** the body of this doc
> was drafted before the chronology addendum; its "3-row batch"
> recommendation **undercounts**. The authoritative recommendation is the
> **5-row batch in the Chronology addendum**, with the refined field
> strings there.

## Method

A dynamic workflow ran **6 parallel read-only, web-enabled agents**, one
per Group-B head. Each: read the live CSV row first-hand, searched the
web, and returned only sources it **actually fetched** (URL + quoted
sentence), classifying CLEAR / PARTIAL / INSUFFICIENT and drafting
house-style strings. The orchestrator (me) **re-verified all 6 slugs
exist with empty attribution**, and **re-graded each against our evidence
standard** rather than accepting the agents' labels verbatim.

**Source-quality rules applied (from the GO):**
- ACCEPTABLE for CLEAR: a reference work / book / encyclopedia saying
  "named after / introduced by X", **or** a dated game/event + a source
  tying the *name* to it.
- NOT sufficient alone: a Lichess/DB label; **Wikipedia with no cited
  reference**; "played by X"; a bare game list.
- Only a source *actually fetched and quoted* counts. (Cambridge Springs
  precedent: no unseen source as primary citation.)

**Sources searched:** Wikipedia (article + raw wikitext for footnotes),
`365chess`/ECO, `chessgames.com` (dated games), `external/lichess-openings`
(type-G label only), and — where Wikipedia footnoted it — the *Oxford
Companion to Chess* citation. `nlm` not needed.

**Orchestrator re-grade vs agent labels (the key judgment):** agents
returned 4 CLEAR + 2 PARTIAL. Against our own "Wikipedia-alone ≠ CLEAR"
rule, I down-grade `B.Sic.Ros` (Wikipedia-only, no reference, no dated
anchor) to effectively PARTIAL, and treat `B.Ale`/`C.RyL.Mar` as CLEAR
**on dated-anchor grounds** (not book grounds). This is recorded
per-candidate below so nothing is hidden.

## Per-candidate evidence

### `A.Tro` — Trompowsky Attack — **CLEAR ✅ (batch-ready)**

- **Type:** A+C (eponym practitioner + popularizer). **Agent:** CLEAR.
  **Orchestrator:** CLEAR — the strongest of the six.
- **Source:** Wikipedia *Trompowsky Attack* (raw wikitext fetched),
  naming sentence footnoted to **Hooper & Whyld, *The Oxford Companion to
  Chess* (2nd ed., OUP 1996), p. 430, entry 'Trompowsky Opening'**.
  Quote: *"The opening is named after the one-time Brazilian champion
  Octávio Trompowsky (1897–1984) who played it in the 1930s and 1940s."*
- **Claim supported:** named for Octávio Trompowsky; clean single eponym
  (the co-credited Opočenský / Ruth attach to *alternate names* of the
  same line, not to "Trompowsky").
- **Caveat (honest):** the Oxford Companion page was confirmed via
  Wikipedia's footnote, not read directly — the same standard used for
  Cambridge Springs (`cf. Panczyk & Ilczuk`), and here stronger (exact
  page + entry).

### `B.Ale` — Alekhine Defence — **CLEAR ✅ (batch-ready, dated anchor)**

- **Type:** A (introducer-is-namesake). **Agent:** CLEAR / batch-ready.
  **Orchestrator:** CLEAR on the dated-event anchor.
- **Source:** Wikipedia *Alekhine's Defence* — *"named after Alexander
  Alekhine, who introduced it at the Budapest 1921 tournament"*; +
  chessgames.com Budapest 1921 (Sämisch–Alekhine, Steiner–Alekhine,
  first-hand verifiable).
- **Claim supported:** named for Alekhine; introducer and namesake
  coincide (clean type-A). No reference *book* quoted — rests on WP +
  verifiable dated event (same basis as Mar del Plata / Berlin Wall).

### `C.RyL.Mar` — Ruy López, Marshall Attack — **CLEAR ✅ (individual-proposal, dated anchor)**

- **Type:** A+E (player eponym **and** game anchor). **Agent:** CLEAR /
  individual-proposal. **Orchestrator:** CLEAR, but **individual** (the
  eponym-vs-anchor wording deserves a human glance).
- **Source:** Wikipedia *Marshall Attack* — *"named after Frank Marshall,
  who introduced it against Capablanca in 1918"*; + chessgames.com
  **Capablanca–Marshall, New York 1918** (1–0; the famous unveiling).
- **Resolution of the open question:** it is *both* — named for the
  player **and** anchored to the 1918 game. Model as type A+E "key game"
  (Meran shape). Marshall is a multi-opening surname → head row only.

### `B.Sic.Ros` — Sicilian Rossolimo — **PARTIAL ⚠ (agent said CLEAR)**

- **Type:** C (popularizer of 3.Bb5). **Agent:** CLEAR / batch-ready.
  **Orchestrator: down-graded to PARTIAL** — the naming claim is
  corroborated across Wikipedia *Bb5 Sicilian* + Wikipedia *Nicolas
  Rossolimo* (*"His name is given to the Rossolimo Variation… 3.Bb5"*),
  but **no reference work and no dated anchor** were quoted. By our own
  "Wikipedia-alone ≠ CLEAR" rule it is not batch-ready.
- **Upgrade path:** one reference-work entry (Oxford Companion 'Rossolimo')
  or a dated Rossolimo game tied to the name → promotes to CLEAR.

### `B.Fre.Win` — French, Winawer — **PARTIAL ⚠ → PROPOSAL WRITTEN 2026-05-30**

> **Update:** a focused source sprint produced a proposal —
> [`french-winawer-attribution-proposal.md`](french-winawer-attribution-proposal.md).
> The naming is uncontested (multi-source secondary attestation + the
> verified dated game Steinitz–Winawer, Paris 1867); still no
> reference-grade source quoted first-hand, so it stays formally PARTIAL,
> but the proposal recommends **apply on the Marshall precedent**
> (secondary attestation + dated game), Oxford Companion noted as an
> optional upgrade. Type C early-practitioner; idea predates him
> (Paulsen 1861). Head row only.

- **Type:** A+C (eponym Winawer; popularised by Nimzowitsch/Botvinnik).
  **Agent + orchestrator:** PARTIAL.
- **Source:** Wikipedia *French Defence* (*"the Winawer Variation, named
  after Szymon Winawer…"*) + Wikipedia *Szymon Winawer* + pawnbreak.com;
  **but** the Oxford Companion 'Winawer Variation' entry was **not
  readable** this run (archive truncated before 'W'). No reference quoted.
- **Upgrade path:** read the OC 'Winawer' entry (or any reference-grade
  source) → CLEAR. Note: in-family siblings `B.Fre.Exc.Uhl`/`B.Fre.Kor`
  are book-sourced, so a French monograph chapter would match house style.

### `B.Sic.Naj.Pol` — Sicilian Najdorf, Polugaevsky — **PARTIAL ⚠**

- **Type:** A+B (his own published 7…b5 analysis). **Agent + orchestrator:**
  PARTIAL.
- **Source:** Wikipedia *Lev Polugaevsky* (*"The Polugaevsky Variation…
  is named after him and reflects years of his home analysis"*) +
  Wikipedia *Najdorf Variation*. His book *Grandmaster Preparation*
  (Pergamon, 1981) is the natural primary source but was **not read** this
  run (recall only).
- **Upgrade path:** quote *Grandmaster Preparation* (or an OC-grade
  entry). Deep child of the attributed Najdorf head → head-of-subline only.

## Batch recommendation

| candidate | orchestrator grade | basis | recommendation |
|---|---|---|---|
| `A.Tro` | **CLEAR** | WP + Oxford Companion (named, paged) | **batch-ready** |
| `B.Ale` | **CLEAR** | WP + dated event (Budapest 1921) | **batch-ready** |
| `C.RyL.Mar` | **CLEAR** | WP + dated game (NY 1918), A+E | batch-ready, prefer individual review of wording |
| `B.Sic.Ros` | PARTIAL | Wikipedia-only | one source upgrade → then apply |
| `B.Fre.Win` | PARTIAL | WP; OC entry unread | one source upgrade → then apply |
| `B.Sic.Naj.Pol` | PARTIAL | WP; book unread | one source upgrade → then apply |

**Two honest options for the apply:**

1. **Conservative batch — `A.Tro` only** (1 row). The single head that
   clears the strict "named reference work" bar. Lowest-risk.
2. **Dated-anchor batch — `A.Tro` + `B.Ale` + `C.RyL.Mar`** (3 rows).
   Adds the two whose naming rests on a *verifiable dated event* — the
   exact basis already accepted for Meran, Mar del Plata, Berlin Wall and
   Cambridge Springs. Defensible and consistent with applied precedent.

**Recommended:** **Option 2 (3-row batch)** — it applies the same
evidence standard the catalogue already uses for its event/game anchors,
and all three naming claims are corroborated across multiple fetched
sources. `B.Sic.Ros` / `B.Fre.Win` / `B.Sic.Naj.Pol` stay out until one
reference-grade citation each is read (a short follow-up sprint or
individual checks).

### Exact proposed field strings (the 3-row batch — NOT applied here)

**`A.Tro`** (Tier-1, popularizer):
```
attributed_to      = Octávio Trompowsky (popularizer)
attribution_source = Hooper & Whyld, 'The Oxford Companion to Chess' (2nd ed., OUP 1996), entry 'Trompowsky Opening' (p. 430), via Wikipedia footnote.
historical_notes   = Named for the Brazilian champion Octávio Trompowsky (1897–1984), who employed 2.Bg5 in the 1930s–40s; he popularised rather than invented it (pre-Trompowsky cases exist, e.g. Levitzky–Burn 1912). The same line also carries the alternate eponyms Opočenský Opening and Ruth Opening. Resurrected at GM level from the 1980s by Julian Hodgson.
```

**`B.Ale`** (type-A, introducer-is-namesake, dated anchor):
```
attributed_to      = Alexander Alekhine (introduced the defence)
attribution_source = Alekhine's introduction at the Budapest 1921 tournament (e.g. Sämisch–Alekhine, Steiner–Alekhine; chessgames.com); naming per Wikipedia 'Alekhine's Defence'.
historical_notes   = 1.e4 Nf6. Named for Alexander Alekhine, who introduced the hypermodern defence at Budapest 1921 — here the introducer and the namesake coincide, a clean type-A eponym.
```

**`C.RyL.Mar`** (type A+E, key game):
```
attributed_to      = Frank Marshall (key game)
attribution_source = Capablanca–Marshall, New York 1918 (the game in which Marshall unveiled the gambit; chessgames.com, 1–0); naming per Wikipedia 'Marshall Attack'.
historical_notes   = 8...d5 gambit in the Ruy López. Named for Frank Marshall, who reportedly prepared it for years and unveiled it against Capablanca at New York 1918 (he lost the game, but the gambit bears his name) — a type-E game anchor.
```

All three: head row only, strings in 3 previously-empty fields, 0 child
rows, en-dash `–` for player/game pairs. Expected impact if applied:
**3 rows, strings-only, audit counts unchanged** (rows 5,899,
`unresolved_groups=0`, `multiple_canonical_groups=17`), no transposition
semantics.

## Risk controls

- **Orchestrator re-graded, did not rubber-stamp** — the agents' 4 CLEAR
  became 3 batch-ready (A.Tro book-grade; B.Ale/C.RyL.Mar dated-anchor),
  with `B.Sic.Ros` honestly held back as Wikipedia-only.
- **No blanket surname attribution** — head row only; Marshall/Alekhine
  are multi-opening surnames (per the risk map in the batch proposal).
- **No unseen source as a bare assertion** — A.Tro cites the OC *via
  Wikipedia's footnote* (stated as such); the dated-anchor rows lead with
  the verifiable game/event, naming per the WP article.
- **No child churn; no transposition/slug/FEN/relation changes.**
- **Honest empty beats invented** — the 3 PARTIAL rows stay empty.

## Next action

- **Recommended (updated by the chronology addendum):** **GO apply the
  5-row batch** — `A.Tro`, `B.Ale`, `B.Sic.Ros`, `C.RyL.Mar`,
  `B.Sic.Naj.Pol` — refined strings in the Chronology addendum, head rows
  only.
- **Or, conservative:** GO apply the 3 with the strongest *naming*
  sources — `A.Tro` (Oxford Companion), `B.Ale` and `B.Sic.Ros`
  (Winter) — and hold the other two.
- **`B.Fre.Win`** stays out until one reference-grade naming citation is
  read (chronology confirms the type but is not a naming source).
- Nothing applied until your explicit GO.

## Chronology addendum: Lumbra / Mega (2026-05-30)

**DB availability:** **Lumbra Gigabase — AVAILABLE and used** (local OTB
PGN, `~/Downloads/GIGABASE/`, periods `0001-1899` → `1950-1969` queried;
standard `[Date]`/`[ECO]` tags). **Mega / ChessBase Database — NOT
available** (no CLI, no `.cbh`; the nlm "MEGA CHESS VAULT" is a text
notebook, not a game DB).

**Query method:** streamed `grep`/Python over the PGN (never whole-file
loads), matching on the **movetext signature** (e.g. `2.Bg5`, `8.c3 d5`,
`3...Bb4`) because Lumbra's ECO sub-codes (`C89a..C89x`, etc.) make a
plain ECO grep unreliable; eponym passes filtered `[White]`/`[Black]` by
surname. Obvious bad-date rows (years `0002`, `1792`, `1811`, apocryphal
Napoleon games) were discarded.

**Cardinal rule (unchanged):** a game database proves *played / appeared
/ when*, **never *named after***. So chronology here **only firms the
attribution TYPE** (inventor vs popularizer vs elite-association) and
feeds `historical_notes` — it is **never** an `attribution_source` for
the name. The naming sources remain the textual ones from the sprint body.

**The decisive cross-cutting finding:** *none of the six is an inventor.*
Every one shows the idea **predating the eponym**, who is a
**popularizer / introducer / elite-associator**. This does not weaken any
naming claim — it matches the catalogue's own Sveshnikov precedent (corpus
first game 1888 antedates the namesake by 84y) and tells us the
`historical_notes` should state the antedating, exactly as the applied
rows do.

| slug | status | earliest in corpus (idea) | earliest by eponym | type |
|---|---|---|---|---|
| `B.Sic.Ros` | **CONFIRMS** | 3.Bb5: Von der Lasa, Berlin **1836–37** | Rossolimo, Bad Gastein **1948** | popularizer (idea predates by ~110y) |
| `A.Tro` | SUPPORTS | 2.Bg5: Levitzky–Burn **1912** (+ earlier) | Trompowsky–Endzelins, Munich ol **1936** | popularizer/namesake |
| `B.Ale` | SUPPORTS | 1.e4 Nf6: Blackburne games **~1889** | Sämisch–Alekhine & Steiner–Alekhine, Budapest **1921** | introducer at master level |
| `B.Sic.Naj.Pol` | SUPPORTS | 7…b5: Reicher–Krogius, Ploesti **1957** | Polugaevsky from **1959** (Zagorovsky–Polugaevsky) | self-eponym / popularizer |
| `B.Fre.Win` | SUPPORTS | 3…Bb4: Paulsen games **1861** | Winawer from **1867** (Black) / **1870** (White) | early practitioner (Botvinnik later popularizer) |
| `C.RyL.Mar` | **COMPLICATES** | 8.c3 d5: Walbrodt, Havana **1893** | Capablanca–Marshall, New York **1918** | popularizer/champion; name anchored to the 1918 game |

**Effect on readiness:** **batch-ready stays at 5** (`A.Tro`, `B.Ale`,
`B.Sic.Ros`, `C.RyL.Mar`, `B.Sic.Naj.Pol`). Chronology *strengthened* the
type wording for all five and confirmed Marshall is a **player eponym +
1918 key game**, not an event anchor. `B.Fre.Win` stays PARTIAL (chronology
fine, naming source still not reference-grade). The 1893 Walbrodt precursor
for Marshall independently corroborates Winter's note read in the sprint.

### Refined 5-row field strings (chronology-backed — **APPLIED 2026-05-30**)

Tier-1 house style; en-dash `–` (U+2013); head row only; `historical_notes`
now carries the dated antedating fact. `attribution_source` cites only
**sources actually seen** (the Gigabase is *not* cited as a naming source).

**`A.Tro`:**
```
attributed_to      = Octávio Trompowsky (popularizer)
attribution_source = Hooper & Whyld, 'The Oxford Companion to Chess' (2nd ed., OUP 1996), entry 'Trompowsky Opening' (p. 430), via Wikipedia footnote.
historical_notes   = Named for the Brazilian champion Octávio Trompowsky (1897–1984), who took up 2.Bg5 in the 1930s–40s; he popularised rather than invented it — the corpus shows 2.Bg5 from Levitzky–Burn 1912 and earlier, well before his own earliest example (Trompowsky–Endzelins, Munich Olympiad 1936). The line also carries the alternate eponyms Opočenský and Ruth; resurrected at GM level from the 1980s by Julian Hodgson.
```

**`B.Ale`:**
```
attributed_to      = Alexander Alekhine (introducer at master level)
attribution_source = Named for Alekhine, who introduced the defence at Budapest 1921 (Sämisch–Alekhine and Steiner–Alekhine, both 1 Sep 1921, confirmed in the corpus); naming per Wikipedia 'Alekhine's Defence' citing Hooper & Whyld and the 1922 Fahrni monograph 'Die Aljechin-Verteidigung'.
historical_notes   = 1.e4 Nf6. Named for Alexander Alekhine, who introduced it at master level at Budapest 1921; the move itself predates him (corpus antecedents from the late 1880s, e.g. Blackburne 1889), so the eponym marks the introducer, not the inventor.
```

**`B.Sic.Ros`:**
```
attributed_to      = Nicolas Rossolimo (popularizer)
attribution_source = Pal Benko's annotation, Chess Life & Review, October 1975 ('Rossolimo … made this system an effective and fully respectable weapon'), as reproduced in Edward Winter, 'Nicolas Rossolimo' (chesshistory.com).
historical_notes   = 1.e4 c5 2.Nf3 Nc6 3.Bb5. The move long predates its namesake — the corpus has it from Von der Lasa, Berlin 1836–37 — but Nicolas Rossolimo made it a respected weapon through frequent use from 1948 (Bad Gastein), and the line took his name (Benko, 1975). A popularizer, not the inventor.
```

**`C.RyL.Mar`:**
```
attributed_to      = Frank Marshall (key game)
attribution_source = Named for Frank Marshall, who unveiled 8...d5 against Capablanca (Capablanca–Marshall, New York 1918, confirmed in the corpus); pre-history per Edward Winter, 'The Marshall Gambit' (chesshistory.com).
historical_notes   = 8...d5 gambit in the Ruy López. Named for Frank Marshall after he sprang it on Capablanca at New York 1918 (Capablanca defended and won). The idea predates that game — the corpus has the 8.c3 d5 position from Walbrodt, Havana 1893 — so the 1918 game is the famous reveal that fixed the name to Marshall, not the line's first occurrence.
```

**`B.Sic.Naj.Pol`:**
```
attributed_to      = Lev Polugaevsky (systematiser)
attribution_source = Lev Polugaevsky, 'Grandmaster Preparation' (Pergamon, 1981; Russian orig. 'Rozhdenie varianta', 1977) — his multi-decade analysis of the 7...b5 system; per the ChessBase feature on the book ('the line that bears his name').
historical_notes   = 6.Bg5 e6 7.f4 b5. A self-eponym via own practice and published analysis: the corpus has 7...b5 from Reicher–Krogius, Ploesti 1957, and Polugaevsky's own games run from 1959 (e.g. Zagorovsky–Polugaevsky); his sustained play and analysis gave the line his name. Attribution on this child node only; the parent Najdorf head is named for Miguel Najdorf.
```

All five: head row only, 3 previously-empty fields, **0 child rows**.
Expected apply impact: 5 rows, strings-only, audit counts unchanged
(rows 5,899, `unresolved_groups=0`, `multiple_canonical_groups=17`), no
transposition semantics.

## See also

- [`player-eponym-attribution-batch-proposal.md`](archive/player-eponym-attribution-batch-proposal.md)
  — the parent map (this sprint sources its Group B).
- [`qgd-cambridge-springs-attribution-proposal.md`](archive/qgd-cambridge-springs-attribution-proposal.md)
  — the source-gated apply template these would follow.
- [`naming-attribution-audit-methodology.md`](naming-attribution-audit-methodology.md)
  — types A–I and the evidence rules used to re-grade.
