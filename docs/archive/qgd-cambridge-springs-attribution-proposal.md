# Naming audit proposal — `D.QGD.Cmb` (Cambridge Springs)

**Status**: **APPLIED 2026-05-30** (option A1, strings-only, head row
only). OCN's first post-1.1 attribution edit and first **event-anchor**
attribution. Drawn from
[`naming-attribution-audit-backlog.md`](naming-attribution-audit-backlog.md)
(Top-5 #1, the single high-evidence item), governed by
[`naming-attribution-audit-methodology.md`](naming-attribution-audit-methodology.md),
and verified per the Citation verification section below.

> **APPLIED.** The three attribution fields were set on `D.QGD.Cmb` only;
> no other row changed (verified: `CHANGED_ROWS=['D.QGD.Cmb']`, rows still
> 5,899, `unresolved_groups=0`). **The Oxford Companion was NOT used as
> the primary citation** — it was never read first-hand, so the verified
> tournament + Panczyk & Ilczuk (2002) source was used instead. Exact
> strings applied are recorded in "Applied result" below. Downstream
> artefact regen + any tag remain GO-gated and NOT executed.

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
| 2 | Wikipedia "QGD, Cambridge Springs Defense", citing Schiller (1984) + Panczyk & Ilczuk (2002); corroborated by chess.com & cs1904.com | the defence is **named after the Cambridge Springs 1904 tournament** (played in 3 games there) | **tournament anchor** (type E) | **high** — see Citation verification below (web-confirmed 2026-05-30) |
| 3 | Same sources | the `...Qa5` idea **predates 1904** (Lasker 1892; Pillsbury, Nuremberg 1896) — the tournament popularised/named it | type-A pre-history → `historical_notes`, not `attributed_to` | **high** (sourced) |
| 4 | Lichess sub-labels (Capablanca, Bogoljubow, Rubinstein, Argentine, Yugoslav) | strong players are tied to **sub-lines**, not to the head name | confirms the **head** name is the *event*, not a person | high |
| 5 | — | a single identified model game that fixed the name | **none found** → do NOT assert a game | n/a |

**Honesty note:** evidence #2 was the load-bearing citation. It has since
been **verified by web sources** (see Citation verification below) — the
origin claim is confirmed and now cites sources actually seen (Wikipedia +
Schiller 1984 / Panczyk & Ilczuk 2002), not the unseen Oxford Companion
entry. The `attribution_source` string in the table below is therefore
**superseded** by the revised block in the Citation verification section.

## Citation verification (2026-05-30)

**Status: CONFIRMED (origin fact) · PARTIALLY CONFIRMED (exact Oxford
Companion entry).** The naming claim — that the line is named for the
**Cambridge Springs 1904 tournament** — is corroborated by multiple
independent secondary sources with citable references. The *verbatim
Oxford Companion (1984) entry wording* was **not** read first-hand, so a
direct primary quote from that specific book remains unconfirmed; the
attribution itself no longer depends on it.

**Sources consulted:**

- **Local repo / `external/`** — only the OCN docs themselves cite the
  Oxford Companion (circular: that is the claim under test). The Lichess
  TSVs confirm the *label* (D52) but say nothing about origin.
- **NotebookLM (`nlm`)** — queried the Q25 editorial-chess notebook
  (123 sources). It returned **two grounded opening-book excerpts**
  confirming the line is real and called the "Cambridge Springs
  variation/system" (`5...Nbd7 6.e3 Qa5`), but **neither excerpt
  describes the origin of the name**. `nlm` honestly **disclaimed** its
  Oxford-Companion paragraph as *"from outside the given sources …
  independently verify it"* — ungrounded recall, correctly flagged.
- **Web (Wikipedia + chess history sources)** — *succeeded* and is the
  decisive evidence. Wikipedia "Queen's Gambit Declined, Cambridge
  Springs Defense": **"The name derives from a 1904 tournament in
  Cambridge Springs, Pennsylvania, where it was played several times."**
  It cites real references — **Schiller, *Cambridge Springs Defense*
  (1984)** and **Panczyk & Ilczuk, *The Cambridge Springs* (2002)** —
  and notes the line **predates 1904** (first recorded Lasker 1892;
  introduced by Pillsbury, Nuremberg 1896). Multiple corroborating
  sources (chess.com, the cs1904.com tournament site) agree, and name
  the three anchoring games: **Marshall–Teichmann, Hodges–Barry,
  Schlechter–Teichmann** (Black scored only ½/3).

**What IS confirmed (high):**

1. The canonical name "Cambridge Springs" is a genuine corpus-attested
   label (Lichess D52 + two opening books via `nlm`) — **not** a DB
   artifact. (`canonical_name`/`aliases` unchanged; never in question.)
2. **Origin = the 1904 tournament** — type-E venue/tournament anchor,
   attributed to the **event/location, not a person and not a single
   game** (three games carried it, no one game fixed it). Confirmed by
   multiple independent secondary sources with citations.
3. **Pre-1904 history** — the `...Qa5` idea predates the event (Lasker
   1892; Pillsbury 1896) → a clean type-A `historical_notes` fact, exactly
   as the Berlin Wall row records its 1880 pre-history.

**What is NOT confirmed:** the **verbatim Oxford Companion (1984) entry**
itself (the specific book was not opened in this session). This no longer
blocks the attribution — the origin fact is independently sourced — but
the proposed `attribution_source` string, which cites the Oxford
Companion, should be **revised to cite a source actually seen** (see
below).

**Effect on the A1/A2 decision:** the **direction and strength are now
solid** for a type-E event anchor (upgraded from "unverified" to
**confirmed origin**). The remaining work before apply is purely the
**`attribution_source` wording** — do not ship the Oxford Companion
citation as written (unseen). Two honest options:

1. **Confirm the Oxford Companion entry in-hand** → keep an OC citation.
2. **Cite what was actually verified** (recommended) → the 1904
   tournament as the anchor plus a real secondary reference, e.g.
   Panczyk & Ilczuk, *The Cambridge Springs* (2002), and/or the named
   1904 games — mirroring how `D.Sem.Mer`/`E.KID.Cls.Mar` cite the
   venue/event directly. No unseen book asserted.

**Recommendation after verification:** **A1** (event anchor in
`attributed_to`, no invented person) is now well-supported and is the
recommendation. The single change vs the originally-drafted A1 strings is
the **`attribution_source`** — substitute the verified
tournament+secondary-source citation (option 2 above) for the unseen
Oxford Companion reference. With that one revision the proposal is
**apply-ready pending GO**; the `historical_notes` should add the type-A
pre-history (Lasker 1892 / Pillsbury 1896) now that it is sourced. The
A1-vs-A2 field-design choice and the final `attribution_source` wording
are the two points for the apply-time GO.

### Revised proposed `attribution_source` (supersedes the table below)

```
attribution_source = Named for the Cambridge Springs 1904 international tournament (Pennsylvania), where the ...Qa5 defence was played in several games (Marshall–Teichmann, Hodges–Barry, Schlechter–Teichmann); cf. Panczyk & Ilczuk, 'The Cambridge Springs' (2002).
```

```
historical_notes (revised) = The ...Qa5 defence takes its name from the Cambridge Springs 1904 tournament, where it appeared in several games. The idea predates the event (first recorded Lasker 1892; introduced by Pillsbury, Nuremberg 1896), so the tournament popularised and named the line rather than originating it. Sub-lines carry later eponyms (Capablanca's Bxf6, Bogoljubow's Qc2, Rubinstein's 7...dxc4).
```

The `attribution_source` / `historical_notes` rows in **"Exact proposed
field changes"** below are the *original* draft (Oxford-Companion-based);
the two blocks here **supersede** them and are what a future apply should
use.

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

## Applied result (2026-05-30)

Applied to **`D.QGD.Cmb` only** — 3 previously-empty fields set, nothing
else touched. Verified: `CHANGED_ROWS=['D.QGD.Cmb']`, `ADDED=[]`,
`REMOVED=[]`, rows still **5,899**, `unresolved_groups=0`,
`multiple_canonical_groups=17`, `git diff --numstat` = `1 1
catalog/ocn-1.csv`. **Exact strings as written to the CSV:**

```
attributed_to      = Named at the Cambridge Springs 1904 tournament (no individual eponym)
attribution_source = Named for the Cambridge Springs 1904 international tournament (Pennsylvania), where the ...Qa5 defence was played in several games (Marshall–Teichmann, Hodges–Barry, Schlechter–Teichmann); cf. Panczyk & Ilczuk, 'The Cambridge Springs' (2002).
historical_notes   = The ...Qa5 defence takes its name from the Cambridge Springs 1904 tournament, where it appeared in several games. The idea predates the event (first recorded Lasker 1892; introduced by Pillsbury, Nuremberg 1896), so the tournament popularised and named the line rather than originating it. Sub-lines carry later eponyms (Capablanca's Bxf6, Bogoljubow's Qc2, Rubinstein's 7...dxc4).
```

**Note on the citation:** the Oxford Companion to Chess was **not** used
as the primary `attribution_source` because its entry was never read
first-hand in this cycle. The applied citation uses the web-verified
tournament origin plus Panczyk & Ilczuk (2002) — sources actually
consulted — per the Citation verification decision above. `canonical_name`,
`aliases`, `notes`, `flags`, `eco_legacy`, `moves_uci`, `parent_ocn1`,
`depth`, `transposes_to`, `same_as` all unchanged; **0 child rows touched**.

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
