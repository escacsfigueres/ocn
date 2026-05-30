# Naming audit proposal — `D.QGD.Cmb` (Cambridge Springs)

**Status**: **PROPOSED — no catalogue change.** This document proposes a
future attribution edit; it applies nothing. The first post-1.1
event-anchor attribution candidate, drawn from
[`naming-attribution-audit-backlog.md`](naming-attribution-audit-backlog.md)
(Top-5 #1, the single high-evidence item) and governed by
[`naming-attribution-audit-methodology.md`](naming-attribution-audit-methodology.md).

**Scope fence**: a *naming* audit. It touches only
`attributed_to` / `attribution_source` / `historical_notes` on the head
row. It does **not** propose any edit to `transposes_to` / `same_as` /
`moves_uci` / `parent_ocn1` / `depth` / `canonical_name` / `aliases`, and
**no child row** changes.

## The entry under audit

```
D.QGD.Cmb  | "QGD, Cambridge Springs"  (ECO D52)
  parent  = D.QGD   depth=2   flags=sharp
  moves   = 1.d4 d5 2.c4 e6 3.Nc3 Nf6 4.Bg5 Nbd7 5.e3 c6 6.Nf3 Qa5
  aliases = "Cambridge Springs"
  notes   = "...Qa5."
  attributed_to / attribution_source / historical_notes : ALL EMPTY
  children: 4 direct, 10 descendants (none attributed)
```

The defining move is **6...Qa5** (the `...Qa5` pin-breaker that gives the
line its bite). `canonical_name` and `aliases` are correct and
Lichess-confirmed — **this proposal does not touch them**. The gap is the
three empty attribution fields.

### Children (for scope — none touched by this proposal)

| slug | name | note |
|---|---|---|
| `D.QGD.Cmb.Yug` | Cambridge Springs, Yugoslav Variation | sub-eponym/venue, own audit later |
| `D.QGD.Cmb.Nd2` (+ `.Bb4`, `.Bb4.Qc2`, `.Bb4.Qc2.O-O`, `.dxc4`) | Nd2 / Bogoljubow line | Lichess "Bogoljubow Variation" |
| `D.QGD.Cmb.cxd5` (+ `.Nxd5`, `.exd5`) | cxd5 lines | — |
| `D.QGD.Cmb.Bxf6` | Cambridge Springs, Capablanca Bxf6 | Lichess "Capablanca Variation" |

Lichess also labels a "Rubinstein Variation" (`7.Nd2 dxc4`) and
"Argentine Variation" in this subtree. These **sub-eponyms are separate
future audits**, explicitly out of scope here. Children **inherit context
by parent**; no child churn.

## Diagnosis — what kind of name is "Cambridge Springs"?

"Cambridge Springs" is a **place/event name**, not a person eponym. The
name derives from the **Cambridge Springs 1904 international tournament**
(Cambridge Springs, Pennsylvania), where the `...Qa5` defence drew
theoretical attention. This is a **type-E event/tournament anchor** in
the methodology's scheme — the same family as `D.Cat` (Catalan, named at
Barcelona 1929), `D.Sem.Mer` (Meran 1924), and `E.KID.Cls.Mar` (Mar del
Plata 1953).

It is **not**:
- **A famous-game anchor (type-E game sub-case).** Unlike the Berlin Wall
  (fixed by a specific match) or Mar del Plata (a specific Najdorf–Gligorić
  game), I have **no evidence** that a single identified game fixed the
  Cambridge Springs name. Per the methodology's "if the source says
  tournament, do not infer a specific game" rule, this proposal does
  **not** assert a model game.
- **A database/location label (type F/G).** Lichess carries "Cambridge
  Springs Defense" (D52) as a real corpus label, and the name is in every
  standard reference — it is a genuine historical name, not a DB artifact.

### The one structural nuance — a *person-less* venue anchor

All four existing type-E exemplars put a **person** in `attributed_to`
(Tartakower, Rubinstein, Najdorf/Gligorić, Kramnik). Cambridge Springs
has **no single namer** — it is named purely for the event. This is the
first person-less venue anchor in the audit, and it forces a field-design
choice (see Options A1 vs A2 below). The methodology's governing rules:

- *"Set `attributed_to` only with a role qualifier and a matching
  `attribution_source`."*
- *"An honest empty `attributed_to` beats an invented one."*

## Evidence table

| # | source | claim | supports | confidence |
|---|---|---|---|---|
| 1 | `external/lichess-openings` (local corpus) | "QGD: Cambridge Springs Defense", ECO **D52**, `...Qa5` — exact move match to `D.QGD.Cmb` | name is a **real corpus label** (not type F/G) | **high** (verified locally) |
| 2 | Standard reference knowledge (Oxford Companion to Chess, Hooper & Whyld 1984, entry "Cambridge Springs Defence") | the defence is **named after the Cambridge Springs 1904 tournament** | **tournament anchor** (type E) | **high** on the *fact*; **medium** that the exact OC entry wording must be confirmed in-hand before apply |
| 3 | Standard reference knowledge | the `...Qa5` idea **predates 1904** (played earlier; the tournament popularised/named it) | type-A pre-history → `historical_notes`, not `attributed_to` | medium (state as pre-history, not as a dated first game) |
| 4 | Lichess sub-labels (Capablanca, Bogoljubow, Rubinstein, Argentine, Yugoslav) | strong players are tied to **sub-lines**, not to the head name | confirms the **head** name is the *event*, not a person | high |
| 5 | — | a single identified model game that fixed the name | **none found** → do NOT assert a game | n/a |

**Honesty note:** evidence #2 is the load-bearing citation and is given
here from standard reference knowledge. **Before any apply, the Oxford
Companion entry must be physically confirmed** (or replaced with an
equivalent reliable opening-reference citation). No web was consulted for
this proposal; `nlm` is available but was not needed for a
proposal-stage diagnosis. This proposal is explicitly gated on that
source confirmation.

## Options

### A — Tournament-anchor attribution (recommended)

Record the type-E event anchor in the attribution fields, head row only.
Two field-design sub-variants for the person-less case:

**A1 (recommended) — event in all three fields, no invented person.**
```
attributed_to      = Named at the Cambridge Springs 1904 tournament (no individual eponym)
attribution_source = Hooper & Whyld, Oxford Companion to Chess (1984), entry 'Cambridge Springs Defence'; the variation takes its name from the Cambridge Springs 1904 international tournament (Pennsylvania).
historical_notes   = The ...Qa5 defence (1.d4 d5 2.c4 e6 3.Nc3 Nf6 4.Bg5 Nbd7 5.e3 c6 6.Nf3 Qa5) takes its name from the Cambridge Springs 1904 tournament, where it drew theoretical attention; the idea itself predates the event. Sub-lines carry later eponyms (Capablanca's Bxf6, Bogoljubow's Qc2, Rubinstein's 7...dxc4).
```
This mirrors the `D.Cat` Oxford-Companion sourcing style, while being
honest that no single person named it — the parenthetical role qualifier
becomes an *event* qualifier rather than a person role.

**A2 — empty `attributed_to`, event in source + notes only.**
```
attributed_to      = (left empty)
attribution_source = Hooper & Whyld, Oxford Companion to Chess (1984), entry 'Cambridge Springs Defence'; named for the Cambridge Springs 1904 tournament.
historical_notes   = (as A1)
```
Strictly defensible under "no person → empty `attributed_to`", but loses
the at-a-glance event anchor that the other three venue exemplars all
surface in `attributed_to`.

### B — Famous-game anchor attribution

Assert a specific model game (e.g. a Pillsbury or Marshall game from
Cambridge Springs 1904) as the anchor. **Not recommended** — no source
ties the name to a single game; the name is the *tournament*, not a game.
Asserting one would violate the methodology's type-E evidence rules.

### C — Source/database label only

Treat "Cambridge Springs" as a type-G label and leave attribution empty.
**Not recommended** — it is demonstrably more than a DB label (it is the
real historical event name, in every reference), so we would be
*under*-attributing a clean type-E case.

### D — Defer

Hold until the Oxford Companion entry is confirmed in-hand. A valid
fallback **only if** source confirmation fails; otherwise A1 is ready.

## Recommendation

**Option A1**, head row `D.QGD.Cmb` only, **gated on confirming the
Oxford Companion entry (evidence #2) before apply**. Rationale:

- It is the cleanest, highest-evidence type-E case in the backlog and
  makes the catalogue's event-anchor treatment internally consistent with
  the four existing exemplars.
- A1 keeps the event anchor visible in `attributed_to` (like all three
  venue siblings) while being explicit that there is no person — no
  invented eponym, satisfying "honest empty beats invented".
- It strictly respects the evidence: tournament, **not** a specific game
  (Option B rejected); the pre-1904 origin of the idea goes in
  `historical_notes` as type-A context, not as `attributed_to`.

If the reviewer prefers maximal conservatism on the person-less point,
**A2** is the fallback within the same recommendation (same source +
notes, empty `attributed_to`). The choice between A1 and A2 is the single
decision this proposal surfaces for GO.

## Exact proposed field changes (for a future apply — NOT applied here)

**Row:** `D.QGD.Cmb` — **3 fields set, all currently empty.**

| field | current | proposed (A1) |
|---|---|---|
| `attributed_to` | *(empty)* | `Named at the Cambridge Springs 1904 tournament (no individual eponym)` |
| `attribution_source` | *(empty)* | `Hooper & Whyld, Oxford Companion to Chess (1984), entry 'Cambridge Springs Defence'; the variation takes its name from the Cambridge Springs 1904 international tournament (Pennsylvania).` |
| `historical_notes` | *(empty)* | `The ...Qa5 defence takes its name from the Cambridge Springs 1904 tournament, where it drew theoretical attention; the idea itself predates the event. Sub-lines carry later eponyms (Capablanca's Bxf6, Bogoljubow's Qc2, Rubinstein's 7...dxc4).` |

**Unchanged on the row:** `canonical_name` ("QGD, Cambridge Springs"),
`aliases` ("Cambridge Springs"), `notes` ("...Qa5."), `flags`,
`moves_uci`, `parent_ocn1`, `depth`, `transposes_to`, `same_as`.

**No other row changes.** The 10 descendants are untouched.

## Blast radius / impact

| dimension | effect |
|---|---|
| rows touched | **1** (`D.QGD.Cmb`); strings-only, 3 previously-empty fields |
| child rows | **0** (children inherit context by parent) |
| row count | **unchanged** (5,899) |
| schema | **unchanged** (14 columns) |
| `moves_uci` / FEN / positions | **unchanged** (no move or position edit) |
| transposition semantics | **none** — `transposes_to` / `same_as` untouched; `unresolved_groups` stays 0 |
| `canonical_ocn1` downstream | **unchanged** — the parquet carries these attribution columns; no slug/identity change, so no consumer breakage |
| tags / release | **untouched** |
| version semantics | content-only attribution enrichment; rides normal proposal→apply + GO, no version bump implied |

## Validation summary (this proposal, docs-only)

Run against the **unmodified** catalogue to confirm this proposal changed
nothing in it:

- `validate.py --strict-chess` → `OK: 5899 entries, 0 warnings`
- `unittest discover tools/tests` → `60 tests OK`
- `audit_transpositions.py --summary` → `unresolved_groups=0`
- `git diff --check` → clean
- `catalog/ocn-1.csv` blob unchanged (`95c908a8…`)

## Apply gating (when GO is given)

1. **Confirm evidence #2** — the Oxford Companion "Cambridge Springs
   Defence" entry in-hand (or substitute an equivalent reliable
   opening-reference citation). No confirmation → Option D (defer).
2. Decide **A1 vs A2** (the person-less `attributed_to` question).
3. Apply the 3 field strings to `D.QGD.Cmb` only, in a dedicated commit
   with explicit **GO apply**; not folded into other work.
4. Re-run the full validation suite; confirm row count 5,899 and
   `unresolved_groups=0` unchanged.

## See also

- [`naming-attribution-audit-methodology.md`](naming-attribution-audit-methodology.md)
  — type-E evidence rules and the event-anchor exemplars this mirrors.
- [`naming-attribution-audit-backlog.md`](naming-attribution-audit-backlog.md)
  — where this candidate ranked #1.
- [`nimzo-rubinstein-kmoch-naming-proposal.md`](nimzo-rubinstein-kmoch-naming-proposal.md)
  — the prior applied naming proposal (the shape this follows).
