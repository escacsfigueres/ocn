# Naming / attribution audit — methodology (post-1.1)

**Status**: methodology only. **No catalogue change** accompanies this
document. This defines *how* to audit opening **names and
attributions** in OCN-1 after the 1.1.0 transposition cleanup — it
does **not** propose or apply edits.

## Purpose

OCN 1.1.0 closed the *transposition* layer: every duplicate-FEN group
is classified (`unresolved_groups=0`). The remaining quality frontier
is **naming**: is each `canonical_name` / `aliases` / `attributed_to`
value *true*, and is the *kind* of attribution explicit?

This audit answers, for any entry, a single question:

> **Where does this name come from, and is the catalogue saying that
> correctly?**

It is **not** about positions, move orders, or transpositions. Scope
fence:

- **Do NOT** change `transposes_to` or `same_as` in a naming audit.
  Those are FEN-identity relations, settled in 1.1.0. A naming
  finding touches `canonical_name` / `aliases` / `attributed_to` /
  `attribution_source` / `historical_notes` — never the resolution
  relations — **unless** the audit surfaces a genuinely new
  duplicate-FEN discovery, which is then handled as a *separate*
  transposition sprint with its own proposal, not folded into the
  naming edit.
- **Do NOT** change `moves_uci`, `depth`, `parent_ocn1` for naming
  reasons. (A *misplacement* finding — type I below — is a structural
  defect; it rides a release boundary as a slug-migration, exactly as
  the QID Miles/Petrosian case did. It is *flagged* by a naming audit
  but *governed* like a migration, not applied inline.)

## The fields, and what each one means

The convention below is **already in use** in the 11 attributed rows
present at 1.1.0 (e.g. `B.Sic.Sve`, `C.RyL.Ber.Wal.End`, `D.Sem.Mer`).
This methodology *formalises the existing practice*; it does not invent
a new schema.

| field | role in a naming audit |
|---|---|
| `canonical_name` | The **definitive English display name**. Must be the name a well-informed reader expects. If the eponym is wrong/spurious, the fix is usually to **demote it to an alias or a descriptor**, not to keep it canonical. |
| `aliases` | `\|`-separated alternate names: source-specific labels, historical co-names, database conventions. A *true-but-not-primary* name lives here. |
| `attributed_to` | Person(s) **plus a parenthetical role qualifier** that encodes the attribution *type* in prose — e.g. `"…(systematiser)"`, `"…(popularizer; Novosibirsk school)"`, `"…(resurrector at GM level)"`, `"…(key game)"`, `"…(named at the 1929 Barcelona tournament)"`. The qualifier is what distinguishes "invented" from "popularised" from "anchored by a game". |
| `attribution_source` | The **evidence**: a bibliographic citation (book + chapter) and/or the anchoring game/event (`Player–Player, Venue Year`). This is the field a sceptic checks. |
| `historical_notes` | The **reconciling narrative**: first-appearance vs popularisation vs naming-event, and corpus facts — *including explicit disconfirmation* (e.g. "the corpus does **not** support the claim that he played it first"). |
| `notes` | Per-row **positional descriptor** (always present). Describes the move/idea, **not** the attribution. Do not overload it with attribution claims. |

## Attribution types

The role qualifier in `attributed_to` (and the narrative in
`historical_notes`) should make exactly one of these the *primary*
basis for the name — and may note secondary ones.

- **A. First known game / earliest game.** The earliest corpus or
  literary trace of the position. *A first appearance is rarely the
  source of the name* — record it in `historical_notes` as a corpus
  fact, not as `attributed_to`.
- **B. First publication / theoretical codification.** The first
  book/article that names or systematises the line. Strong basis for
  `attribution_source` (e.g. a monograph or a named opening-book
  chapter).
- **C. Popularizer.** A player who used it repeatedly and made it
  visible, *without* necessarily inventing it. Role qualifier
  `(popularizer)`.
- **D. Elite practitioner / strongest association.** A strong player
  associated with the line (often the modern corpus top scorer),
  even if neither inventor nor namesake. Belongs in
  `historical_notes` ("championed by…", "top corpus Black is…").
- **E. Famous game / match / tournament anchor.** A specific game,
  match, or event that *fixed the line in theoretical memory* — the
  name is anchored to the **event**, not strictly to an inventor.
  Distinct from C: a popularizer is a *person over many games*; an
  anchor is *one game/match/event*. (See evidence rules below.)
- **F. Database convention.** A modern label inherited from a games
  database with no clear inventor (ECO codes, generic house names).
  Usually an `alias`, occasionally the only available `canonical_name`.
- **G. Source-specific label.** A name particular to one source
  (Lichess, chess.com, ECO, a single book). Acceptable as an
  `alias` and as `attribution_source` context; **not** automatically
  `attributed_to`. A Lichess label is a *label*, not evidence of who
  named or invented the line.
- **H. Editorial descriptor / move-order descriptor.** An OCN-internal
  functional name when no eponym is warranted — `"a3 Move Order"`,
  `"Main Line"`, `"e4 Line"`. The honest default when attribution is
  thin.
- **I. Suspected misattribution / subtree misplacement.** The name is
  wrong, spurious, or attached to the wrong node/parent-chain. Flag
  it; resolve naming-only cases by demotion, and structural
  (slug/parent) cases via a governed migration.

### How the existing 11 attributed rows map to the types

This is the empirical anchor — the convention is descriptive, not
aspirational:

| entry | primary type(s) | how it's encoded |
|---|---|---|
| `B.Sic.Sve` (Sveshnikov) | B + A + C + G-alias | source cites the 2003 monograph; notes record corpus first game **1888** (antedates the namesake by 84y); alias `Lasker-Pelikan`. |
| `B.Sic.Sve.…Bg7` (Novosibirsk) | C + E(place) | `(popularizer; Novosibirsk school)`; notes explicitly say corpus does **not** support first-play; name from his hometown. |
| `C.RyL.Ber.Wal.End` (Berlin Wall Endgame) | **E (match anchor)** | `(resurrector at GM level)`; source = **Kasparov–Kramnik, London 2000**; notes reconcile 1880 origin vs 2000 anchor. |
| `D.Sem.Mer` (Meran) | E (tournament anchor) | source = **Rubinstein–Tartakower, Meran 1924**; venue name. |
| `D.Cat` (Catalan) | E (named-at-event) + B | `(named at the 1929 Barcelona tournament)`; source = Oxford Companion. |
| `E.KID.Cls.Mar` (Mar del Plata) | E (venue anchor) | source = **Najdorf–Gligorić, Mar del Plata 1953**. |
| `B.Sic.Naj` (Najdorf) | B/C eponym + D | own practice; Fischer/Kasparov cement the name (D). |
| `E.Ben.Bnk` (Benko/Volga) | B + parallel discovery + G | monograph 1974 + Soviet "Volga" tradition; dual name. |
| `B.Fre.Exc.Uhl`, `A.KIA.Fre.Bar`, `B.Fre.Kor` | B (book-sourced eponym) | `attribution_source` = specific opening-book chapter; no `historical_notes` needed. |

## Evidence rules

### Minimum evidence to touch the catalogue

- **`attribution_source` requires a primary source or a reliable
  opening book** — a monograph, a named book chapter, the Oxford
  Companion, or a specific dated game. A games **database is support,
  not sole proof** of *who named* a line (it proves *who played* it,
  and *when* — type A/D facts).
- **A Lichess/DB label is acceptable as an `alias` or source-specific
  context (G)** but is **not** by itself an `attributed_to`.
- **"Played by X" ≠ "named after X".** If a source only attests that X
  played the line, you may record type A/C/D in `historical_notes`;
  you may **not** write `attributed_to = X` as the namesake without a
  source that links the *name* to X.
- **A famous game that merely *illustrates* a line is not an anchor.**
  Put "appears in `<game>`" in `historical_notes`. Only promote to
  `attributed_to` type E when a source attests the line is *named for*
  or *theoretically fixed by* that game/match/event.

### Evidence specific to type E (event/game anchor)

To assert an event/game anchor, record **all** of:

1. The **game/match/event**: `Player–Player` (or match/tournament
   name), with **round/game number where relevant** and **date**.
2. A **PGN game id or bibliographic reference** for the game(s), where
   one exists.
3. A **source** attesting that the line is *associated with / named
   for / fixed by* that event — not merely that the moves occurred
   there.
4. An explicit **distinction from type A**: if the position predates
   the anchor (it usually does), say so in `historical_notes` (as the
   Berlin Wall row does: "dates back to Wemmers–Riemann 1880 … but the
   modern weapon is owed to Kramnik's 2000 match").

A match-series anchor (e.g. "associated with Karpov–Kasparov 1985,
games *N*/*M*") is valid **only** if a source ties the line's identity
to that series; list the specific game numbers and do not generalise
from a single illustrative game.

## Decision criteria

- **Keep as `canonical_name`** when the name is well-attested and is
  what an informed reader expects (types B/C/E with a source).
- **Move from `canonical_name` to `aliases`** when the eponym is
  *true but secondary* (a co-name, a source-specific label) — promote
  the more standard name to canonical.
- **Demote to a descriptor (type H)** when the eponym is *spurious or
  unsupported* and no better eponym exists (what `E.Nim.Sml.Kmo` →
  "a3 Move Order" did).
- **Set `attributed_to`** only with a role qualifier and a matching
  `attribution_source`. No source → no `attributed_to`.
- **Set `attribution_source`** to the strongest available evidence
  (book/chapter > specific dated game > database aggregate).
- **Use `historical_notes`** for the reconciling story and for
  famous-game/event context that does *not* rise to `attributed_to`
  (type A/D facts, "appears in…", corpus disconfirmations).
- **Change nothing** when the current name is fine and adding
  attribution would be unsourced speculation. An honest empty
  `attributed_to` beats an invented one.

## Relation to OCN 1.1

- Transpositions are **resolved**; naming audits **must not** alter
  `transposes_to` / `same_as` except on a genuinely new FEN-identity
  discovery, which becomes its own transposition sprint.
- Structural (slug/parent) corrections (type I) ride a **release
  boundary** as a governed slug-migration — the precedent is the QID
  Miles/Petrosian rename in 1.1.0 — never an inline naming edit.
- Naming edits that only touch `canonical_name` / `aliases` /
  `attributed_to` / `attribution_source` / `historical_notes` are
  catalogue-content changes with **no downstream schema impact**
  (the parquet carries these columns unchanged); they still ride the
  normal proposal-then-apply + explicit-GO discipline.

## Worked examples

### 1. Nimzo / "Kmoch" — eponym placement (types H, I, G)

Three nodes currently carry, or carried, a "Kmoch" name:

- **`E.Nim.Fou` ("Nimzo, 4.f3")** — keeps `Kmoch Variation` as an
  **alias**. This is the *correct home* for the Kmoch name (4.f3,
  ECO E20), per Lichess. **No change** — type B/G alias, well-placed.
- **`E.Nim.Sml.Kmo`** — already **demoted** in 1.1.0 from a spurious
  "Kmoch" canonical to **"a3 Move Order"** (type H descriptor) and
  `transposes_to E.Nim.Sml.Bot`. Its `notes` explicitly state the
  Kmoch name belongs to `E.Nim.Fou`. **Done** — exemplar of an I→H
  resolution (spurious eponym → honest descriptor).
- **`E.Nim.Rub.Kmo` ("Nimzo Rubinstein, Kmoch Variation")** — **open
  question**, a type-I candidate. Its `canonical_name` *and* `aliases`
  still carry "Kmoch", and it is `same_as E.Nim.Sml.Bot.MLn`
  (Sämisch-Botvinnik Main Line). Audit question: is "Kmoch" here a
  *real* Rubinstein-Nimzo line name (B), a **database artifact** (F),
  or a **source-specific label** (G) inherited alongside the
  Sämisch-Botvinnik FEN-twin? Resolution path mirrors `E.Nim.Sml.Kmo`
  *only if* the evidence matches — otherwise keep. **Flagged, not
  applied.**

### 2. QID Miles → Petrosian — naming lie + misplacement (type I)

Resolved in 1.1.0; included as the canonical type-I template. The
Kasparov-Petrosian QID theory (`…a3 …Bb7 …Nc3`, with the Kasparov
Attack `Qc2`) was sitting under a **"Miles" branch slug**
(`E.QID.Mil.MLn.*`) — the *name* on the line ("Kasparov-Petrosian")
contradicted the *slug/parent-chain* ("Miles"). That is a structural
misplacement, not a cosmetic rename: it was governed as OCN's first
**slug-migration** (→ `E.QID.Pet.KPe.*`) riding the 1.1.0 release, with
a decision record, not an inline edit. Lesson for type I: **separate
the naming claim from the slug identity** — if only the *name* is
wrong, demote/relabel; if the *slug/parent* is wrong, migrate at a
release boundary.

### 3. Event/game anchor — the real model: Berlin Wall Endgame (type E)

OCN already contains the canonical event-anchor exemplar, so no
invented case is needed: **`C.RyL.Ber.Wal.End`**.

- `attributed_to = "Vladimir Kramnik (resurrector at GM level)"` —
  the role qualifier says *anchor*, not *inventor*.
- `attribution_source = "Kasparov–Kramnik World Championship match,
  London 2000"` — the specific **match** that fixed the line in modern
  memory.
- `historical_notes` reconciles type A vs E explicitly: the position
  "dates back to Wemmers–Riemann 1880 … but the Berlin Wall as a
  modern weapon at world-championship level is owed to Kramnik's 2000
  match."

This is exactly the shape any future event-anchor audit should
produce — e.g. a line genuinely fixed by a specific Karpov–Kasparov
1985 game would read `attributed_to = "… (match anchor)"`,
`attribution_source = "Karpov–Kasparov, World Championship, Moscow
1985, game N"`, with the pre-history in `historical_notes`. Sibling
venue/event anchors already in the catalogue: **Meran** (`D.Sem.Mer`,
Rubinstein–Tartakower 1924), **Mar del Plata** (`E.KID.Cls.Mar`,
Najdorf–Gligorić 1953), **Catalan** (`D.Cat`, named at Barcelona 1929).

## Candidate future audits (not committing to apply)

A backlog of naming questions worth an audit, *each gated on its own
proposal + evidence + explicit GO*:

- **`E.Nim.Rub.Kmo`** — is the "Kmoch" name real (B), a DB artifact
  (F), or a source-specific label (G)? (See example 1.)
- **`E.Nim.Sml.Kmo.MLn`** — cosmetic parent-chain quirk: it sits under
  `E.Nim.Sml.Kmo` (now "a3 Move Order"). Confirm the child's
  `canonical_name`/parent reads sensibly now that the parent was
  relabelled; descriptor-only, low priority.
- **Player-eponym sweep** — systematically check the entries whose
  `canonical_name` carries a player surname but whose `attributed_to`
  is empty (the vast majority): classify each as B/C/D/E or demote to
  H, adding sources only where they exist. Start from names already
  flagged in `notes` / release notes.
- **Source-specific / Lichess labels** — identify `canonical_name`
  values that are really type-G labels and move them to `aliases`
  with a more standard canonical.

None of the above is approved for apply; this is a methodology +
backlog, not a change set.

## See also

- [`docs/nimzo-botvinnik-kmoch-naming-review.md`](nimzo-botvinnik-kmoch-naming-review.md)
  — the worked naming review behind example 1.
- [`docs/transposition-cleanup-closure.md`](transposition-cleanup-closure.md)
  — the resolved transposition layer this audit sits *on top of*.
- [`docs/post-1.1-roadmap.md`](post-1.1-roadmap.md) — where this work
  sits in the post-1.1 plan.
