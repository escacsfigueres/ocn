# OCN-1 — Open Chess Naming, version 1

**Status**: v1.1 — living spec for the released `ocn-1.1.x` catalogue line
(first issued as Draft v0.1 on 2026-04-28; see "Spec history" under
Versioning)
**Author**: Club d'Escacs Figueres
**License**: CC-BY-4.0 (this document and the catalogue)
**Repository**: https://github.com/escacsfigueres/ocn

## Why OCN

The Encyclopaedia of Chess Openings (ECO), introduced by Šahovski Informator
in 1971, has been the de facto naming standard for chess openings for
50+ years. ECO has aged remarkably well in one respect: the **A/B/C/D/E**
top-level classification captures the fundamental structural divide of
chess openings, and any new opening fits cleanly into one of those five
families.

ECO has aged poorly in another respect: the 100 sub-codes within each
letter (`A00`–`E99`) are arbitrary, frozen in 1971, distributed by what was
fashionable then, and offer no parent-child hierarchy. Knowing that "B33"
is the Sveshnikov, "E97" is the King's Indian Classical, and "C67" is the
Ruy López Berlin Endgame is a feat of memorisation that does not benefit
the player learning openings or the database designer running queries.

OCN-1 is **a hierarchical companion to ECO**, not a replacement. It keeps
the A/B/C/D/E top-level classification — that is the part of ECO that
deserves to live another 50 years — and replaces the arbitrary 00-99
sub-code with a small, human-readable, hierarchical slug.

## Goals

1. **Memorable**. A player should be able to read `B.Sic.Naj.Eng` once
   and never need to look it up.
2. **Hierarchical**. Parent-child relationships are explicit. All Sicilian
   lines start with `B.Sic`.
3. **Compatible**. Every OCN-1 slug within ECO's coverage carries a
   back-reference to its ECO code(s), preserved in the catalogue as
   `eco_legacy` and joinable scalar-wise as `catalog/ocn-1.eco.tsv`.
   299 rows (5.1%) carry none: the five class roots, which are filters
   rather than lines, and 294 Lichess long-tail lines that lie beyond
   ECO's 500-code resolution. That is coverage extension, not a defect.
4. **Open**. The specification and the catalogue are CC-BY-4.0. Anyone may
   adopt OCN-1 in their own database, book or product.
5. **Stable**. Once a slug is published in a tagged release, it MUST NOT
   change meaning. New openings extend the catalogue; existing entries are
   amended only via aliases or deprecation, never by re-pointing.

## Format

```
<class> ( "." <named> )+ ( "." <move> )*
```

A slug is the class letter, then **one or more named segments**, then
**zero or more trailing SAN move segments**, bounded at 7 segments in
total (6 dots). This is the grammar the validator has always enforced
(`tools/validate.py`); earlier editions of this document published a
narrower production (at most six segments, at most two move segments)
that the catalogue outgrew — see [`errata.md`](errata.md), E-003. A
normative ABNF with a conformance corpus is planned for spec 1.3
(roadmap H2.4).

The named levels carry conventional role names by depth:

| Position | Length | Case | Examples |
|---|---|---|---|
| `class` | 1 char | uppercase A/B/C/D/E | `A`, `B`, `C`, `D`, `E` |
| `family` (named, depth 1) | 3 chars | TitleCase or known ALLCAPS abbreviation | `Sic`, `Fre`, `RyL`, `KID`, `QGD` |
| `variation` (named, depth 2) | 3 chars | TitleCase | `Naj`, `Sve`, `Mar`, `Tar`, `Sml` |
| `subline` and deeper (named) | 3 chars | TitleCase | `Eng`, `End`, `Ope`, `Cls` |
| `move` (tail) | 1-6 chars | SAN-style, check/mate stripped | `Be3`, `e5`, `Bxf6`, `O-O`, `O-O-O` |

One known ambiguity: a token like `Bg5` or `Nd5` is both a legal SAN
move and a plausible 3-character named token. The catalogue resolves it
positionally — SAN-shaped tokens inside the named region are named
tokens (`D.Sem.Bg5.Mos`), and the move tail is the trailing run of
SAN-parsing segments (`B.Sic.Sve.Nd5`). The precise normative rule
(maximal SAN suffix, plus a ban on minting new SAN-shaped named tokens)
lands in spec 1.3.

### Class assignment

The class is derived from the position **after the principal opening
moves of the variation**, not from a single rigid rule. The intent is:

- **A** — Flank openings: lines outside 1.e4 and outside the main
  1.d4/2.c4 Indian-defence complex. Includes Réti, English, Bird,
  Larsen, the Dutch family, Trompowsky, and other "non-classical" centre
  treatments.
- **B** — Semi-Open: 1.e4 followed by **any reply other than 1...e5**.
  Includes Sicilian, Caro-Kann, French, Pirc, Modern, Alekhine,
  Scandinavian.
- **C** — Open: 1.e4 e5 (symmetric king-pawn). Includes Ruy López, Italian,
  Petrov, Scotch, Vienna, King's Gambit and the rest of the Open Games.
- **D** — Closed Queen's Pawn: 1.d4 d5 (symmetric queen-pawn) or any line
  in which Black plays an early ...d5. Includes Queen's Gambit (declined,
  accepted), Slav, Semi-Slav, Catalan (Black plays ...d5; otherwise see
  below), Tarrasch, Albin.
- **E** — Indian: 1.d4 Nf6 with Black defining the game by an Indian
  piece setup or hypermodern central strike rather than by the classical
  1...d5 queen-pawn symmetry. Includes King's Indian Defence,
  Nimzo-Indian, Queen's Indian, Bogo-Indian, Old Indian, Grünfeld,
  Benoni/Benko, and Catalan-without-d5.

The class is a property of the **OCN-1 slug**, not of the literal
move-order that produced it. Two transposing move-orders that converge to
the same canonical position therefore share the same OCN-1 slug.

#### Borderline rules

- **Catalan**: classified `D` only when Black plays ...d5 within the first
  five moves. Without ...d5 (e.g. King's Indian setup against the Catalan
  bishop) the position is classified `E`. Spec rationale: Catalan is
  defined by the structural fight for d5; without that fight, the position
  belongs in the Indian family.
- **Grünfeld**: classified `E` even though some legacy ECO codes place it
  in the D range. Spec rationale: Grünfeld is structurally an Indian
  defence (1.d4 Nf6 first), and grouping it with the Indian family makes
  the parent-child hierarchy clean.
- **Budapest / Fajarowicz**: `E.Bud`. The legacy ECO codes are `A51` and
  `A52`, but `1.d4 Nf6 2.c4 e5` is an Indian countergambit against the
  d4/c4 complex, so it belongs with the Indian defences rather than with
  flank openings.
- **Queen's Gambit Accepted**: `D.QGA`. Black plays ...d5 then ...dxc4.
  Stays in D.
- **Benoni / Benko**: `E.Ben`. Even though the legacy ECO range is `A43`
  and `A56`-`A79`, the main Benoni and Benko families arise from
  `1.d4 Nf6 2.c4 c5` Indian move-orders and should live beside King's
  Indian and Grünfeld structures. Immediate Old Benoni move-orders
  without ...Nf6 stay in the same family to avoid splitting a single
  named opening across classes.

### Family abbreviation rules

When abbreviating a family or variation name to 3 characters:

1. **Preserve a vowel** if possible. Prefer `Naj` over `Njd`,
   `Sve` over `Svs`, `Tar` over `Trt`.
2. **Use the first three pronounceable characters** of the name, accents
   dropped (`Sml` for Sämisch, `Gru` for Grünfeld).
3. **Honour established acronyms**: `KID`, `QGD`, `QGA`, `QID`, `NID`,
   `OID`, `RyL` (Ruy López — the y is preserved because the
   pronunciation collapses into "Roo-Ee-Lo-Pez").
4. **Avoid collisions within the same parent**. If two children of the
   same parent both want `Cla`, the second uses a different abbreviation
   (`Clo`, `Csc`, …) and the choice is documented in the catalogue.

Display names (`canonical_name`) keep the original spelling, including
accents, punctuation and full words: `Sicilian Defence: Sämisch
Variation`. The 3-letter slug is purely for compact reference.

### `move` segments — the depth tail

For lines that are routinely identified by a specific tabiya beyond the
named variation, append literal SAN moves separated by dots. Check (`+`)
and mate (`#`) are stripped. File/rank disambiguation is allowed when SAN
requires it. The tail may run to several moves within the 7-segment cap
(about a quarter of catalogue rows carry three to five — e.g.
`C.Vie.Nc6.f4.exf4.Nf3.g5`); short tails read best:

```
B.Sic.Sve.Nd5            11.Nd5 main Sveshnikov tabiya            (one move)
B.Sic.Sve.Bxf6           9.Bxf6 line                              (one move)
B.Sic.Naj.Eng.e5         6.Be3 e5 line of the English Attack      (one move)
B.Sic.Naj.Eng.e6.Qd2     6.Be3 e6 7.Qd2 Scheveningen-style        (two moves)
B.Sic.Naj.Eng.e6.g4      6.Be3 e6 7.g4 Delayed Keres              (two moves)
```

All of the above are real catalogue entries (the `Eng` segment already
encodes 6.Be3, so the move tail starts at Black's reply). The catalogue
does not enumerate every deep tabiya; it grows as the community
contributes lines that meet the "named-tabiya" bar (see below).

Castling is `O-O` (kingside) or `O-O-O` (queenside). Captures use `x`.
Promotions: `=Q`. Check (`+`) and mate (`#`) are not part of the slug —
they describe the move, not the variation.

The depth tail is appended only when the SAN move is **the canonical tabiya
that opening literature attaches a name to**. Random middlegame moves do
not become OCN-1 slugs. (Honesty note: the validator does not yet enforce
this bar mechanically — much of the current deep tail derives from the
Lichess long-tail import. Enforcement criteria are a spec 1.3 work item.)

### Maximum depth

The catalogue MUST NOT contain entries with more than 6 dots (i.e. 7
segments). This cap is a design boundary, not headroom: 18.4% of current
rows sit at the 7-segment maximum, and that is accepted — the cap marks
where naming ends and position identity begins. Deeper theory attaches to
existing slugs as data (a planned `mainline` continuation field in the
positions sidecar, roadmap H2.8) or is identified by position key, never
by a longer slug. Raising the cap would be a format change and therefore
a major (2.x) version.

## Catalogue

The reference catalogue is `catalog/ocn-1.csv`. Each row has the columns:

| Column | Type | Description |
|---|---|---|
| `ocn1` | string | The slug (primary key). |
| `canonical_name` | string | Full human-readable name with accents and punctuation. |
| `eco_legacy` | string | Pipe-separated ECO codes that this slug covers (`B90`, or `B90\|B91`). |
| `parent_ocn1` | string null | Parent slug. NULL for class roots like `A`. |
| `moves_uci` | string null | Canonical UCI move sequence reaching the slug's reference position (space-separated, e.g. `e2e4 c7c5 g1f3 d7d6 d2d4 c5d4 f3d4 g8f6 b1c3 a7a6`). NULL for class roots, which are filters, not positions. |
| `depth` | int | 0 for class roots, increments by 1 per dot. |
| `aliases` | string null | Pipe-separated alternative names (Lasker–Pelikan, etc.). |
| `flags` | string null | Pipe-separated tags from the closed set `{gambit, sharp, closed, endgame, theoretical, deprecated}`. |
| `notes` | string null | Free text explaining edge cases or borderline classification. |
| `attributed_to` | string null | Player(s), school, or event the opening is associated with. Free text. |
| `attribution_source` | string null | Citation supporting `attributed_to`. **Required** when `attributed_to` is non-empty — the validator rejects unsourced claims. Free text but must reference published, publicly checkable evidence: a book, an article, or a dated tournament game. Unverifiable sources (unpublished game collections, private databases) are rejected by the validator. |
| `historical_notes` | string null | Longer-form context (transmission history, popularisation, dated antecedent games). |
| `transposes_to` | string null | Slug of the FEN-canonical OCN-1 entry that owns this position. Set when this row is a move-order transposition of another. NULL when this row is itself canonical. See "Canonicalisation by position" below. |
| `same_as` | string null | Pipe-separated list of OCN-1 slug(s) that share this row's FEN and are preserved alongside it as co-canonical entries. Set when two or more rows are both canonical literary identities of the same position. Mutually exclusive with `transposes_to` on a single row. NULL when this row has no declared co-canonical partner. See "Co-canonical preservation" below. |

The three attribution columns form the catalogue's "Layer 2" — curated,
human-asserted history. Downstream position-indexed datasets MAY
maintain a machine-recomputable "Layer 1" beside it (first/last game,
top players, total games) and join it by `ocn1`; that layering is
informative and lives outside OCN-1.

Position identity — how a row's `moves_uci` becomes a comparable
position key and a 64-bit hash — is defined normatively in
**Annex A** below. Producers MAY emit a derived `zobrist` (INT64)
column when serialising to a position-indexed format; a positions
sidecar carrying SAN movetext, EPD, corrected FEN and the Polyglot
zobrist, generated in-repo, is planned (roadmap H2.8). (Informative:
external toolchains have historically produced such an artefact;
nothing in OCN-1 depends on any of them.)

The OCN repository also provides a lightweight derived export:
`tools/export_positions.py` emits one row per concrete catalogue entry
with `fen_key` (board, turn, castling, legal en-passant), canonical
counter-normalised `fen` (`fen_key 0 1`), and
`transposition_group_size`.

### Canonicalisation by position (`transposes_to`)

OCN-1 has two distinct relations between slugs:

- **`parent_ocn1`** is the **nominal hierarchy**. It groups slugs by
  literature lineage and lets a human reader navigate from a family
  root (`A.Kan`, `E.Nim`) down to a specific tabiya. The parent chain
  is what produces a readable slug.
- **`transposes_to`** is **canonicalisation by position**. It points
  from a slug whose FEN coincides with another slug's FEN to that
  other slug — the FEN-canonical one. It does not change the
  parent-child tree.

Many openings are reached by more than one move order. OCN-1 keeps
each named move order alive (so a reader following the Kangaroo
literature can still find the Kangaroo entries) but records on each
non-canonical entry that the position **is** another OCN-1 slug by
FEN. Consumers building a position index SHOULD treat
`transposes_to` as the canonicalisation arrow: when resolving a FEN
to OCN-1, follow `transposes_to` once and report the target slug.

Contract:

- `transposes_to` is a single `ocn1` value or NULL.
- It MUST differ from `ocn1`.
- The target MUST exist in the catalogue.
- The target MUST NOT be a class root (class roots are filters, not
  positions).
- Class roots themselves MUST NOT carry `transposes_to`.
- When both rows have `moves_uci`, their FEN keys (board + side to
  move + castling + en-passant) MUST match. The validator rejects
  rows whose declared transposition does not hold by FEN.
- `transposes_to` does not replace `aliases` or `notes`. Aliases
  preserve human-readable alternate names; notes capture move-order
  context. `transposes_to` makes the relation computable.

A duplicate FEN group is "resolved" when exactly one entry has empty
`transposes_to` (the canonical) and every other entry points into
the group with `transposes_to`. `tools/audit_transpositions.py`
hides resolved groups by default and surfaces them with
`--include-resolved`.

**Path-marker children.** A child entry MAY carry `moves_uci`
byte-identical to its parent's when it documents that the named line is
reached by another move order. Such a path-marker MUST declare the
move-order relation in its `notes` and MUST carry its parent's
`eco_legacy` — same position, same classification (the validator
enforces the latter). Path-markers deliberately do not use
`transposes_to`: the canonicalisation layer records cross-tree
position identity, not parent-child move-order refinement.

### Co-canonical preservation (`same_as`)

`transposes_to` records the relation **non-canonical → canonical**:
one slug is the FEN-canonical entry, the other is a documented
move-order transposition. There is one canonical per FEN, by design.

`same_as` records a different relation: **canonical ↔ canonical**.
Two (or more) slugs reach the same FEN but each carries an
established literary identity that the catalogue preserves on
purpose. Neither is "the alias" of the other; both are real names
in chess literature, often from different historical traditions
(Rubinstein Opening ⇄ Colle-Zukertort, Italian Giuoco ⇄ Two
Knights after castling, Nimzo Rubinstein Kmoch ⇄ Sämisch Botvinnik).

Contract:

- `same_as` is a pipe-separated list of `ocn1` slugs, or NULL.
- `same_as` and `transposes_to` are **mutually exclusive** on a
  single row. A row is either non-canonical (declares
  `transposes_to`) or co-canonical (declares `same_as`), never
  both.
- Each target slug must exist in the catalogue.
- No self-reference.
- Class roots cannot carry `same_as`.
- When both rows have `moves_uci`, their FEN keys must match. The
  validator rejects rows whose declared co-canonical does not hold
  by FEN.
- The relation is conceptually symmetric. The CSV may declare it
  one-way or bilaterally; bilateral is preferred for human
  readability. `tools/audit_transpositions.py` treats in-group
  `same_as` edges as undirected when classifying a group's
  resolution.

A duplicate FEN group counts as `multiple_canonical` (resolved) iff
all non-canonical entries point into the group via `transposes_to`
AND at least one of these declarations exists:
- a non-canonical pointer (the original mechanism, French / Veresov
  and KID Classical precedents), OR
- an in-group `same_as` edge between two canonical entries (the
  OCN 0.3 mechanism, for cases without a third descriptor slug).

Three slug-level relations now coexist:

- **`parent_ocn1`** — nominal hierarchy. Groups slugs by literature
  lineage. Produces readable slugs (`E.Nim.Rub.O-O.Nf3` is a child
  of `E.Nim.Rub.O-O`).
- **`transposes_to`** — canonicalisation by position, asymmetric.
  Points from a non-canonical row to the canonical that owns its
  FEN.
- **`same_as`** — co-canonical preservation, symmetric. Links two
  canonical rows that share a FEN by editorial decision.

### Canonicalisation arbitration

When two or more rows share the same FEN, exactly one of them must
be canonical and the others must declare a `transposes_to` pointing
into the group (or be deleted as redundant). The following rules
arbitrate that choice. They are **ordered**: apply rule 1 first; if
it does not resolve the case, fall through to rule 2; and so on.

**Rule 1 — Established name beats descriptor.**
If one side carries an established literary opening name (London,
Colle, Trompowsky, Nimzo, Sicilian Najdorf, Queen's Indian, Catalan,
…) and the other side is a path descriptor whose slug or
`canonical_name` essentially restates a parent's name or an imported
Lichess label (e.g. `.Std`, `.Closed`, `.Cls.Nf3.Nbd7.Rc1.c6`), the
established name is canonical and the descriptor either gets
`transposes_to` or is deleted (rule 6 governs which).

**Rule 2 — Spec-governed structural classes win.**
If the position falls under a rule explicitly written elsewhere in
this spec — Catalan with `...d5` is `D`, Indian without `...d5` is
`E`, Grünfeld is `E`, Benoni / Benko is `E`, Old Indian with `...Nf6`
reaching a KID FEN is `E.KID.*`, etc. — the slug whose class matches
that rule is canonical, regardless of which family produced the
shorter slug or appeared first by ECO order.

**Rule 3 — Parent–child same-FEN redundancy.**
If one of the duplicate rows is a direct child of another and they
share the same FEN, the parent is the canonical anchor. The child
may be deleted iff it has zero children of its own AND zero inbound
`transposes_to` references AND its `canonical_name` adds no
literature identity beyond the parent's. Otherwise it stays alive
with `transposes_to` pointing at the parent.

**Rule 4 — Two real names: prefer to preserve both.**
If both rows carry distinct, established literary names from
different opening traditions (e.g. French Classical Main Line ⇄
Veresov Classical Main Line, KID Old Main Line ⇄ KID Classical
e5 castled, Italian Giuoco ⇄ Italian Two Knights when O-O is on the
board), the default is to **preserve both rows**. Use
`transposes_to` only when one side is unambiguously dominant for
canonical position lookup (e.g. the position is universally cited
by one of the two names in literature). When dominance is not
unambiguous, mark the group as deferred and document the conceptual
choice in `docs/transpositions.md` before acting.

**Rule 5 — Family tabiya beats move-order breadcrumb.**
If one row is the canonical named tabiya of a family (`E.Nim.Rub`,
`E.KID.Cls.Nrm`, `B.Sic.Dra`) and the other is a path through a
different family's move-order that happens to arrive at that tabiya
(`A.Kan.MLn.e3`, `A.OID.Mod.MLn.Nf6`, `B.Sic.OKn.Nf6.Nc3.g6`), the
family tabiya is canonical and the breadcrumb gets `transposes_to`.
The breadcrumb stays alive so a reader navigating the move-order
subtree can still reach its FEN counterpart.

**Rule 6 — Prefer `transposes_to` over slug surgery when surgery
cascades.**
If resolving a group would require reparenting many descendants of
the non-canonical row, or would orphan rows referenced by external
consumers, prefer `transposes_to`. Physical deletion is reserved
for leaf rows with zero children, zero inbound references, and a
descriptor-only identity (rule 1 + rule 3 satisfied). Move-order
breadcrumbs with substantive subtrees are kept alive with
`transposes_to`.

**Rule 7 — ECO is evidence, not authority.**
ECO codes inform canonical choice (a position cited by every ECO
publication as `B06` is more likely to be canonically `B.Mod` than
`A.Mod`), but they are not the final arbiter. ECO is a flat 1971
classification with known coarseness and frozen choices. When ECO
and a stronger rule (1, 2, 4 or 5) disagree, the stronger rule
wins. Record the ECO observation in `eco_legacy` and `notes`, not
in the canonical slug choice.

#### Do not resolve automatically

Some FEN duplicates are not safe to auto-resolve and MUST go
through human review before any `transposes_to` arrow is written or
any row deleted:

- The **French / Veresov** complex (`B.Fre.Cls.MLn ⇄ A.Ver.Cls.MLn.Be7
  ⇄ D.QPG.Ver.MLn.Be7` and its `A.Ver` / `D.QPG.Ver` subtree).
  Three established literary identities converge on the same FEN; a
  single canonical choice would erase one of them.
- Groups with **multiple strong literary identities** on different
  sides (rule 4 applies).
- Groups where the **shorter slug carries a name that disappears
  if deleted** — e.g. a Lichess-imported alias is the only place a
  particular opening label survives in the catalogue.
- Groups where **both rows have substantive children**: deletion
  would orphan; `transposes_to` is technically safe but the
  canonical choice still needs human judgement.

When in doubt, deferred is better than wrong. The
`audit_transpositions.py --ranked` report keeps deferred groups
visible until they are resolved.

### Looking up a slug from an ECO code

A single ECO code can map to several OCN-1 slugs (e.g. `B90` covers the
Najdorf family root and several depth-3 lines). Tools resolving "ECO →
OCN-1" SHOULD apply the **deepest-match** rule:

1. Filter rows whose `eco_legacy` contains the queried code.
2. Among those, pick the row with the highest `depth` whose path is
   consistent with the available context (e.g. the move list).
3. If multiple rows tie at the same depth, the consumer SHOULD report
   the ambiguity rather than silently picking one.

When precise matching matters (preparation, novelty hunting,
move-order-aware analysis) consumers SHOULD JOIN by `zobrist` — as
defined in Annex A — against a position-indexed dataset rather than
rely on ECO at all. ECO is a coarse filter; the canonical zobrist is
the unambiguous identifier.

## Versioning

OCN-1 follows semantic versioning at the catalogue level:

- **Patch** (1.0.x): clarifications, typo fixes, alias additions.
- **Minor** (1.x): new entries that do not change the meaning of existing
  slugs. New `flags` values. Breaking format changes in the spec are NOT
  allowed in a minor version.
- **Major** (2.x): changes to the slug format itself.

Once a release is tagged, an entry's `ocn1` MUST NOT be re-pointed to a
different position. If a slug is found to be wrong, mark it `deprecated`
in `flags` and add the correct slug as a new entry.

Known deviations from this policy, and clauses this document has had to
correct about itself, are recorded openly in [`errata.md`](errata.md).
A field-level rewrite of the change classes (versioning 2.0) is planned
for spec 1.3.

### Conformance corpus (provisional)

The fixtures under `tools/tests/fixtures/` — valid and invalid slugs,
warning cases, strict-chess negatives — are the **provisional**
conformance corpus for this spec: an implementation that agrees with
`tools/validate.py` on all of them can consider itself aligned with the
catalogue's rules as enforced today. Spec 1.3 formalises this into a
declared, versioned corpus of ~100 cases with reason codes.

### Spec history

- **Draft v0.1 (2026-04-28)** — initial public draft.
- **v1.0 (2026-05, `ocn-1.0.2`/`ocn-1.0.3`)** — position canonicalisation:
  `transposes_to` (asymmetric) and `same_as` (symmetric) relations added,
  completing the 14-column catalogue.
- **v1.1 (2026-05-26, `ocn-1.1.0`)** — transposition layer fully resolved
  (`unresolved_groups=0`); attribution columns (`attributed_to`,
  `attribution_source`, `historical_notes`) actively populated under the
  sourced-attribution contract (a non-empty `attributed_to` MUST carry an
  `attribution_source`).
- **v1.2 (2026-06-11, `ocn-1.2.0`)** — diacritic-true canonical names
  (683 renames — see `errata.md` E-002 on how that sat with the minor
  version rule as then written), audited ECO legacy codes, the validator
  gate made unconditional (checks 13-20, zero allowlists), the Lichess
  cross-reference sidecar, and the American-spelling alias lot. Zero
  `ocn1` changes.
- **v1.2 triage patch (2026-07-29, unreleased)** — this document
  corrected to state the grammar the validator actually enforces
  (`class . named+ . move*`, 7-segment cap), the depth-cap saturation
  acknowledged as design, the token-ambiguity resolution documented
  descriptively, `errata.md` created, and the test fixtures declared the
  provisional conformance corpus. No catalogue change.

## Examples

The full canonical example set lives in `catalog/ocn-1.csv`. A few
illustrative ones:

| OCN-1 | ECO | Canonical name |
|---|---|---|
| `A.Eng.Sym` | A30–A39 | English Opening, Symmetrical Variation |
| `A.Hol.Lng` | A87–A89 | Dutch Defence, Leningrad Variation |
| `A.Tro` | A45 | Trompowsky Attack |
| `B.Sic` | B20–B99 | Sicilian Defence |
| `B.Sic.Naj` | B90–B99 | Sicilian Defence, Najdorf Variation |
| `B.Sic.Naj.Eng` | B90 | Sicilian Najdorf, English Attack |
| `B.Sic.Naj.Eng.e5` | B90 | Najdorf English Attack, 6.Be3 e5 |
| `B.Sic.Sve` | B33 | Sicilian Sveshnikov (Lasker–Pelikan) |
| `B.CaK.Adv` | B12 | Caro-Kann, Advance Variation |
| `B.Fre.Win` | C15–C19 | French Defence, Winawer Variation |
| `C.RyL.Ber.Wal.End` | C67 | Ruy López, Berlin Wall Endgame |
| `C.Ita.Evn` | C51 | Italian, Evans Gambit |
| `C.Pet` | C42 | Petrov Defence |
| `D.QGD.Tar` | D58–D59 | Queen's Gambit Declined, Tartakower |
| `D.Sem.Mer` | D47 | Semi-Slav, Meran Variation |
| `D.Cat.Ope` | E04–E05 | Catalan, Open Variation |
| `E.KID.Sml` | E80–E89 | King's Indian Defence, Sämisch Variation |
| `E.Nim.Cls` | E32–E33 | Nimzo-Indian, Classical Variation |
| `E.Gru.Exc` | D85 | Grünfeld, Exchange Variation |

## Lichess long-tail integration

OCN-1 is intentionally curated — it names 5,899 opening families,
variations, and tabiyas (as of the `ocn-1.1.x` line) that carry real
literary or practical identity. It does NOT attempt to name every line
that ever appeared in a game.

For the long tail (Bird's Australian Variation, Polish Sokolsky
Defended, Englund Gambit Complex…), consumers SHOULD layer the Lichess
Opening Book (`lichess-org/chess-openings`, CC0) on top of OCN-1:

1. Resolve a position to OCN-1 first via `positions.zobrist =
   openings.zobrist`.
2. If no OCN-1 match, fall back to the Lichess catalogue keyed by the
   same Polyglot Zobrist.
3. Lichess entries carry a `parent_ocn1` field — the deepest OCN-1
   ancestor of that line — so even unnamed-by-OCN positions can be
   shown grouped under a familiar OCN-1 family.

The OCN repository ships this layering directly:
`catalog/ocn-1.lichess-xref.tsv` maps every OCN-1 row to its exact or
nearest-ancestor Lichess label. With the catalogue and the upstream
Lichess TSVs loaded, every position in a real game database can be
resolved to a name: curated OCN-1 names first, and then Lichess's CC0
names with an OCN-1 family as breadcrumb.

The repository includes `tools/lichess_parent_map.py` as a lightweight
CSV/TSV bridge: it converts Lichess SAN PGN lines to UCI and assigns the
deepest OCN-1 parent by move-prefix match.

## Annex A — Position identity (normative)

How a catalogue row's `moves_uci` becomes a comparable position key.
This annex makes OCN-1 self-contained: everything needed to compute
position identity is defined here or in public, freely available
standards.

### The `fen_key`

Replay `moves_uci` from the standard initial position. The `fen_key`
is the first four FEN fields of the resulting position:

1. **Board** — standard FEN piece placement.
2. **Side to move** — `w` or `b`.
3. **Castling rights** — the FEN castling field, `-` when none remain.
4. **En passant** — the target square **only if at least one enemy
   pawn can legally capture en passant** (a capture that would leave
   the capturer's own king in check does not count); otherwise `-`.

Rule 4 is the trap. Most FEN emitters (including python-chess's
`Board.fen()`) print the en-passant square after every double pawn
push, whether or not the capture is legal. Two `fen_key`s for the same
position must compare equal, so OCN normalises to the *legal-capture*
form — the same convention the Polyglot hash uses. Consumers comparing
their own FENs against OCN MUST apply the same normalisation
(`tools/ocn.py` ships it as `fen_key()`).

The exported `fen` column is `fen_key` plus placeholder counters;
halfmove and fullmove counters are not part of position identity.

### The Polyglot Zobrist hash

Where a 64-bit key is wanted (joins, opening books), OCN-1 uses the
**Polyglot book hash**: the XOR of the standard public Polyglot random
keys for piece placement, castling rights, the en-passant file (only
when a legal capture exists — the same rule as `fen_key`), and the
side to move, computed on the position reached by replaying
`moves_uci`. The 781-key array and the hashing rules are the public
Polyglot book format, documented and reproduced identically across
open implementations (among them python-chess's `chess.polyglot`
module and the chessprogramming wiki's "BookFormats" entry). An
implementation that disagrees with those public keys is nonconforming.

Class roots (`A` through `E`) carry no `moves_uci` and therefore no
position identity: they are filters, not positions. Consumers MUST
special-case them (they are the five null-key rows in any derived
export).

## Acknowledgements

OCN-1 builds on the work of:

- Šahovski Informator (1971) for the A/B/C/D/E classification.
- Lichess Chess Openings (CC0) for canonical English names.
- Hooper & Whyld, *Oxford Companion to Chess* (1984) for canonical name
  conventions.
- The community of chess players, coaches and database authors who have
  pointed out the limits of ECO for half a century.
