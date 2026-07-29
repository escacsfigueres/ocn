# OCN-1 — Open Chess Naming, version 1

**Status**: v1.3 — the standards edition: normative ABNF, catalogue
profile, conformance classes and corpus. **Unreleased**: it takes effect
with the next catalogue tag; the released catalogue line is still
`ocn-1.2.x`. (First issued as Draft v0.1 on 2026-04-28; see "Spec
history" under Versioning.)
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

## Requirements language

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT",
"SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and
"OPTIONAL" in this document are to be interpreted as described in
BCP 14 [RFC 2119] [RFC 8174] when, and only when, they appear in all
capitals, as shown here.

Normative parts of OCN-1 are: this document except where a section is
marked *informative*, the ABNF below, the catalogue profile, and the
conformance corpus in [`conformance/`](../conformance/). Everything else
in the repository — tools, guides, audits, release notes — is
informative. Where a tool and this document disagree, the document is
wrong until proven otherwise (`errata.md`, E-003): the spec bends to the
deployed catalogue, and the catalogue is never churned to satisfy a
document.

## Format

### The two layers

OCN-1 separates what a slug *may* look like from what the reference
catalogue actually contains.

- **The grammar** — the ABNF below — is the stable layer, and it is
  **major-versioned**. Changing it (a new character in a token, a
  different separator, a different move notation) is a 2.x change and
  nothing less.
- **The catalogue profile** is the tightening layer, and it is
  **minor-versioned**. It caps depth, constrains token shape, and closes
  the set of ambiguous tokens. A profile constraint MAY be tightened in a
  minor version **only when the catalogue shipped in that release already
  satisfies it** — every profile rule below was computed from the live
  catalogue before it was written down.

A slug is **grammar-valid** when it matches the ABNF. It is
**profile-valid** when it is grammar-valid and satisfies every rule of
the profile in force. The reference catalogue contains profile-valid
slugs only. Class roots (bare `A` through `E`) are grammar-valid and
profile-valid.

Earlier editions of this document published a narrower production (at
most six segments, at most two move segments) that the catalogue
outgrew; see [`errata.md`](errata.md), E-003.

### Grammar (normative ABNF)

The slug grammar in ABNF as defined by RFC 5234. Terminals are given as
numeric values because ABNF quoted strings are case-insensitive and OCN-1
slugs are case-significant.

```abnf
   ocn-slug    = class *( dot named ) *( dot san-move )

   class       = %x41 / %x42 / %x43 / %x44 / %x45
                                     ; "A" / "B" / "C" / "D" / "E"

   dot         = %x2E                ; "."

   named       = 1*token-char
   token-char  = ALPHA / DIGIT / %x5F / %x3D / %x2D
                                     ; letter / digit / "_" / "=" / "-"

   san-move    = castling / piece-move
   castling    = %x4F.2D.4F [ %x2D.4F ]
                                     ; "O-O" / "O-O-O"
   piece-move  = [ piece ] [ file ] [ rank ] [ %x78 ] square [ promotion ]
                                     ; %x78 = "x", the capture marker
   piece       = %x4E / %x42 / %x52 / %x51 / %x4B
                                     ; "N" / "B" / "R" / "Q" / "K"
   promotion   = %x3D promo-piece    ; "=" then the promoted piece
   promo-piece = %x4E / %x42 / %x52 / %x51
                                     ; "N" / "B" / "R" / "Q"
   square      = file rank
   file        = %x61-68             ; "a" - "h"
   rank        = %x31-38             ; "1" - "8"

   ; ALPHA and DIGIT are the RFC 5234 Appendix B.1 core rules:
   ;   ALPHA = %x41-5A / %x61-7A
   ;   DIGIT = %x30-39
```

Four things follow directly from the grammar and are stated here so no
implementer has to infer them:

1. **Class roots are grammar-valid.** Both repetitions may be empty, so
   `A` is a complete slug. It names a filter, not a position (Annex A).
2. **The grammar is ambiguous by construction.** Every `san-move` is
   also a well-formed `named`, so `B.Sic.Sve.Nd5` has more than one
   derivation. This is deliberate: token-shape policy belongs to the
   profile, not to the stable layer. The parse rule below makes the
   partition unique.
3. **Check and mate are not slug characters.** `+` and `#` are outside
   `token-char`: they describe a move event, not a variation. A SAN move
   is written with them stripped.
4. **Slugs are ASCII and case-significant.** `B.Sic` and the
   NON-CATALOGUE `B.sic` are different strings, and only the first is a
   slug (see String canonicalisation, and profile rule CP-4).

### The catalogue profile (1.x)

These constraints apply to the reference catalogue and to anything
claiming to be an OCN-1 1.x catalogue. They are minor-versioned.

| ID | Rule |
|---|---|
| **CP-1** | A slug MUST have at most **7 segments** (at most 6 dots). |
| **CP-2** | Every slug other than a class root MUST have at least **one named segment**. A move tail can never begin immediately after the class letter. |
| **CP-3** | Every named token MUST be exactly **3 characters**, unless it is listed in the named-token registry below. |
| **CP-4** | A named token MUST NOT consist solely of lowercase ASCII letters. Named tokens are TitleCase, an established acronym, or a numeric label (`B.Pir.150`); an all-lowercase token is either a misplaced SAN pawn move or a casing error. |
| **CP-5** | A named token that also parses as `san-move` MUST appear in the grandfathered-token table below. The table is **closed**: no new SAN-shaped named token may be minted (see Conformance, P-2). |

CP-1 is a design boundary, not headroom — see "Maximum depth" below.
There is no cap on the length of the move tail beyond CP-1: 1,393 rows
(23.6%) carry three to five move segments.

The named levels carry conventional role names by depth. This table is
**descriptive of convention**; the normative constraints are the ABNF
and CP-1 to CP-5 above.

| Position | Length | Case | Examples |
|---|---|---|---|
| `class` | 1 char | uppercase A/B/C/D/E | `A`, `B`, `C`, `D`, `E` |
| `family` (named, depth 1) | 3 chars | TitleCase or registered acronym | `Sic`, `Fre`, `RyL`, `KID`, `QGD` |
| `variation` (named, depth 2) | 3 chars | TitleCase | `Naj`, `Sve`, `Mar`, `Tar`, `Sml` |
| `subline` and deeper (named) | 3 chars | TitleCase | `Eng`, `End`, `Ope`, `Cls` |
| `move` (tail) | as `san-move` | SAN-style, check/mate stripped | `Be3`, `e5`, `Bxf6`, `O-O`, `O-O-O` |

### Token ambiguity: the maximal-SAN-suffix rule

A token like `Bg5` or `Nd5` is both a legal SAN move and a plausible
3-character named token. The following rule resolves every such case,
normatively and from the slug string alone.

**Parse rule.** Let a grammar-valid slug be `s0 . s1 . … . sn`, where
`s0` is the class. Let *k* be the **smallest** index in `1 … n+1` such
that every segment in `sk … sn` matches `san-move` (for a slug whose
last segment is not SAN-shaped, *k* = *n*+1 and the run is empty). Then:

- the **move tail** is `sk … sn` — the *maximal* trailing run of
  segments that parse as `san-move`;
- the **named region** is `s1 … s(k-1)`, and **every** segment in it is a
  named token, whatever its shape.

The rule is positional and purely lexical: it depends on the slug string
only, never on the position, the parent chain or the catalogue. Two
consequences the catalogue relies on:

```
B.Sic.Sve.Nd5    named = Sic, Sve        tail = Nd5
D.Sem.Bg5.Mos    named = Sem, Bg5, Mos   tail = (empty)
```

`Nd5` is the 11.Nd5 Sveshnikov tabiya — a move. `Bg5` is the label of
the Bg5 branch of the Semi-Slav — a name. The maximal-suffix rule gets
both right without a lookup table.

**Grandfathered SAN-shaped named tokens.** CP-5 closes this class. The
table below is the complete list of tokens that occupy a named-region
position somewhere in the reference catalogue *and* parse as `san-move`
— **39 tokens across 570 named-region occurrences**, computed from the
catalogue, not curated. New named tokens MUST NOT be SAN-shaped; these
survive because they are already published keys and slugs are stable.

| Token | Example slug |
|---|---|
| `Ba4` | `C.RyL.Mor.Ba4.Nf6.O-O.Cls` |
| `Bb3` | `B.Sic.Dra.Yug.Chn.Bb3.Top` |
| `Bb4` | `D.Cat.Ope.Bb4.Mod` |
| `Bb5` | `C.Ita.Two.Ng5.Pol.Bb5.Two` |
| `Bb7` | `D.QGD.Tar.MLn.Bd3.Bb7.Pil` |
| `Bc4` | `B.Mod.Std.Bc4.Mky` |
| `Bc5` | `C.Ita.Two.O-O.Bc5.Hol` |
| `Bd2` | `E.Ind.Cat.Bb4.Bd2.Be7.D5N` |
| `Bd3` | `D.Sem.Mer.Bd3.Bd6.Chi` |
| `Bd6` | `D.Sem.Mer.Bd3.Bd6.Chi` |
| `Bd7` | `B.Sic.Mor.Bd7.MLn` |
| `Be2` | `B.Sic.Cls.Be2.Drg` |
| `Be3` | `B.Sic.Dra.Be3.Bg7.Be2.Ams` |
| `Be6` | `D.Tar.Cls.Bg5.Be6.Sto` |
| `Be7` | `E.Ind.Cat.Bb4.Bd2.Be7.D5N` |
| `Bf4` | `A.PQI.Bf4.MLn` |
| `Bf5` | `B.CaK.Two.Bf5.MLn` |
| `Bg2` | `C.Vie.Mie.Bc5.Bg2.Nc6.Pol` |
| `Bg5` | `D.Sem.Bg5.Mos` |
| `Bg7` | `B.Pir.Cls.Bg7.MLn` |
| `Na6` | `E.KID.Avk.Cst.Bg5.Na6.Brg` |
| `Nc3` | `C.Sco.Gor.Nc3.MLn` |
| `Nc6` | `A.Lon.Job.Nc6.MLn` |
| `Nd6` | `C.RyL.Ber.Rio.Qe2.Nd6.Cor` |
| `Nd7` | `B.CaK.Cls.Spd.Nd7.Lob` |
| `Ne2` | `E.Nim.Rub.O-O.Ne2.Sim` |
| `Ne4` | `E.Nim.Spl.Rom.Nf3.Ne4.Crl` |
| `Nf3` | `B.Sca.Nf6.Nf3.Gou` |
| `Nf6` | `B.Sca.Nf6.Mar` |
| `Ng5` | `C.Ita.Two.Ng5.Trx` |
| `O-O` | `E.Nim.Rub.Res.MLn.O-O.Brn` |
| `Qa4` | `D.Cat.Ope.Qa4.Ale` |
| `Qc2` | `D.Cat.Cls.Qc2.Btr` |
| `Qd1` | `D.Tar.HSc.MLn.Qd1.Von` |
| `Qe2` | `C.RyL.Ber.Rio.Qe2.Nd6.Cor` |
| `Qe7` | `C.KGm.Acc.Kie.Qe7.Coz` |
| `Qh5` | `C.Vie.Fal.MLn.Qh5.Nd6.Ada` |
| `Rc1` | `D.QGD.Ort.Rc1.Pil` |
| `Re8` | `E.Ben.Mod.Cls.MLn.Re8.Tal` |

A token in this table is grandfathered as a *token*, not as a
subtree-local licence: it may keep appearing in the named region of the
slugs that already carry it, and it may not be introduced anywhere new.
The validator enforces the table as check 22
(`GRANDFATHERED_SAN_NAMED_TOKENS` in `tools/validate.py`, pinned to this
table by test).

### Named-token registry (CP-3 exemptions)

Tokens that may appear in the named region at a length other than three,
plus the established acronyms recorded here for provenance. Adding a
token to this registry is a minor version.

| Token | Meaning |
|---|---|
| `KID` | King's Indian Defence |
| `QGD` | Queen's Gambit Declined |
| `QGA` | Queen's Gambit Accepted |
| `QID` | Queen's Indian Defence |
| `NID` | Nimzo-Indian Defence (registered, unused: the catalogue heads that family `E.Nim`) |
| `OID` | Old Indian move order |
| `RyL` | Ruy López (the `y` is preserved because the pronunciation collapses into "Roo-Ee-Lo-Pez") |
| `OldI` | Old Indian Defence |
| `AntM` | Anti-Marshall systems |
| `Cmb` | Cambridge Springs |
| `NoD5` | Line without an early `...d5` (registered, currently unused) |

Only `OldI` and `AntM` are actually longer than three characters in the
shipped catalogue; the rest satisfy CP-3 on length alone and are listed
because the registry, not the length rule, is what makes an acronym
legitimate.

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

Some openings sit awkwardly between classes, and in those cases OCN's letter
differs from ECO's. Each case is argued here and carries a stable key — the
`rationale_ref` column of the divergence sidecar described at the end of this
section — so a consumer holding a divergent row can look up the argument
instead of guessing at it.

- **French** (`french-b`). `B.Fre` and its entire subtree are class `B`,
  although ECO codes the French `C00`-`C19`. This redefines what ECO's
  letter `C` means, and OCN states it as such rather than presenting the
  result as fidelity. ECO's `C` bundles two different answers to 1.e4 — the
  Open Games (1.e4 e5) and the French (1.e4 e6) — while ECO's `B` holds
  every *other* reply to 1.e4. OCN takes the rule that already generates
  the rest of that class, "1.e4 and Black does not answer 1...e5", and
  applies it without an exception: `C` becomes exactly the symmetric
  king-pawn openings, and the French joins the Sicilian, Caro-Kann, Pirc,
  Modern, Alekhine and Scandinavian in `B`.

  The argument is structural, not stylistic. In the Open Games both sides
  stake a pawn on the fourth rank, and the resulting fight is over d4 and
  f7, with fast piece play and near-symmetrical development. The French
  declines that symmetry: Black leaves e5 alone, strikes the centre with
  ...d5, and accepts less space and a fixed pawn chain in return for the
  ...c5 lever and a long-term target on d4 — the same bargain the Caro-Kann
  makes by a different move-order (1...c6 and 2...d5). The questions a
  French player actually studies (the light-squared bishop, the d4/e5
  chain, when to break with ...c5 or ...f6) are semi-open questions, and
  they are not questions any Open Game asks.

  It is worth being explicit about what this rationale does **not** claim.
  It does not claim the French plays like a Sicilian; the two share a
  boundary rule, not a character. It does not claim ECO was careless: ECO's
  letters were printed-volume boundaries as much as structural claims, and
  keeping twenty codes of self-contained French theory next to the rest of
  1.e4 was a reasonable 1971 decision. The claim is narrower — that for a
  hierarchy meant to be read off a slug, a class defined by a rule with one
  exception is worse than the same class with the exception removed — and
  OCN pays for the change in exactly one place: the letter. Every French row
  keeps its ECO code unchanged — all twenty of `C00`-`C19` are present in
  the catalogue, and the one French row ECO files elsewhere (`A43`, the
  French Benoni by transposition) keeps that code too.

  Two normative consequences follow:

  - A consumer mapping between ECO and OCN **MUST NOT** assume letter
    equality. On this case the relation is exactly stated: OCN's `B` is
    ECO's B *plus* the French, and OCN's `C` is ECO's C *minus* the French.
  - A consumer bucketing rows by OCN class letter and labelling the buckets
    with ECO's letter meanings **MUST** consult the divergence sidecar
    first, or it will misfile every French row. Join by code
    (`catalog/ocn-1.eco.tsv`) or by position (Annex A) — never by letter.

  At 252 rows this is the largest single divergence in the catalogue and the
  one OCN most expects to be argued with. It is also the most expensive to
  undo: the class letter is the first character of a slug, so reversing it
  would rewrite 252 primary keys and could only ever ship in a major (2.x)
  version, never in a minor or a patch.

- **London / Colle and the queen's-pawn systems** (`london-colle-a`).
  `A.Lon`, `A.Col` and their neighbours are class `A`, although ECO codes
  the London and Colle in the `D02`-`D05` range. ECO's placement keys on the
  pawns: d4 against d5 is a closed queen-pawn game, so the letter is `D`.
  OCN keys on the character of the opening instead. These are *systems* —
  White plays Nf3, d4, Bf4 or e3/Bd3/c3 and castles in much the same way
  whatever Black does, and the line is chosen as a repertoire object rather
  than entered as a branch of Queen's Gambit theory. Grouping them with the
  Réti, English and Trompowsky in `A` puts them beside the other openings
  whose defining feature is a scheme rather than a central pawn duel; filing
  them in `D` would place a London player's whole repertoire inside a family
  whose theory that player never studies.

  The same principle extends to queen's-pawn move-order objects whose
  deeper lines run into `D` theory by transposition: `A.Hor` (Horwitz, 29
  rows — the largest head in this group), `A.Ver` (Richter-Veresov, 8),
  `A.QPO` (Queen's Pawn Opening, 8) and `A.EID` (East Indian, 3), alongside
  `A.Lon` (16) and `A.Col` (18). Eighty-two rows in total: the class letter
  follows the family the line belongs to, not the ECO code its tabiya
  happens to transpose into.

- **Catalan** (`catalan-d`): classified `D` only when Black plays ...d5
  within the first five moves. Without ...d5 (e.g. King's Indian setup
  against the Catalan bishop) the position is classified `E`. Spec
  rationale: Catalan is defined by the structural fight for d5; without that
  fight, the position belongs in the Indian family.
- **Grünfeld** (`gruenfeld-e`): classified `E` even though some legacy ECO
  codes place it in the D range. Spec rationale: Grünfeld is structurally an
  Indian defence (1.d4 Nf6 first), and grouping it with the Indian family
  makes the parent-child hierarchy clean.
- **Budapest / Fajarowicz** (`budapest-e`): `E.Bud`. The legacy ECO codes
  are `A51` and `A52`, but `1.d4 Nf6 2.c4 e5` is an Indian countergambit
  against the d4/c4 complex, so it belongs with the Indian defences rather
  than with flank openings.
- **Queen's Gambit Accepted**: `D.QGA`. Black plays ...d5 then ...dxc4.
  Stays in D. (No divergence: ECO agrees.)
- **Benoni / Benko** (`indians-e`): `E.Ben`. Even though the legacy ECO
  range is `A43` and `A56`-`A79`, the main Benoni and Benko families arise
  from `1.d4 Nf6 2.c4 c5` Indian move-orders and should live beside King's
  Indian and Grünfeld structures. Immediate Old Benoni move-orders without
  ...Nf6 stay in the same family to avoid splitting a single named opening
  across classes. The same key covers the other Indian defences ECO files
  outside its E range: `E.Ind`, `E.OldI`, `E.KID` and `E.Blf`.
- **Everything else** (`misc`): 44 rows, almost all of them deep
  transposition tails where an `A`- or `B`-class family's move-order runs
  into another class's theory several moves in — `A.Kan` into the
  Nimzo-Indian, `A.Ret` into the Semi-Slav, `B.Mod` into the `A41`/`A42`
  Modern-against-d4 lines. These are accidents of tabiya depth, not
  family-level class decisions, and OCN documents them as a bucket rather
  than inventing a rationale per row.

The complete, machine-readable list of divergent rows is the derived sidecar
[`catalog/ocn-1.eco-divergence.tsv`](../catalog/ocn-1.eco-divergence.tsv):
one row per divergent slug with its OCN class, its ECO codes, its family head
and its `rationale_ref` from the closed set above. It is regenerated by
`python3 tools/build_eco_divergence.py`, pinned by a drift test, and
independently recomputed by `tools/validate.py`, which refuses a catalogue
whose committed sidecar disagrees with it — so the number cannot quietly
grow. As of this profile it lists **770 rows, 13.8% of the 5,600 ECO-bearing
rows** (252 French, 195 other Indian defences, 117 Grünfeld, 82
London/Colle-family, 49 Catalan, 44 misc, 31 Budapest).

The class letter is a property of **OCN's** taxonomy, not a restatement of
ECO's. Nothing is renumbered to match it: within ECO's coverage every row
keeps its `eco_legacy` codes exactly as ECO assigned them, and the scalar
join table `catalog/ocn-1.eco.tsv` remains the correct way to move between
the two systems.

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
not become OCN-1 slugs. (Honesty note: this bar is editorial and the
validator does not enforce it mechanically — much of the current deep
tail derives from the Lichess long-tail import. It is a SHOULD on
producers, P-8, not a profile rule, because no machine check for
"literature attaches a name to it" exists.)

### Maximum depth

CP-1 restated with its reasoning: the catalogue MUST NOT contain entries
with more than 6 dots (i.e. 7 segments). This cap is a design boundary,
not headroom: 18.4% of current
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
| `flags` | string null | Pipe-separated tags drawn from the flags registry (see Extension mechanism). Open registry: new values arrive in minor versions, and `x-` is reserved for private use. |
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
with `fen_key` (board, turn, castling, legal en-passant), a complete
`fen` (the same position with the halfmove clock and fullmove number
computed during the replay), and
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

## String canonicalisation

OCN-1 carries two kinds of string, and they have opposite rules.

### Slugs

Slugs are **ASCII** (the `token-char` set of the ABNF) and
**case-significant**. `B.Sic` and the NON-CATALOGUE `B.sic` are
different strings; only the first is a slug, and CP-4 rejects the
second. Implementations MUST
compare slugs as byte strings and MUST NOT case-fold, ASCII-fold,
Unicode-normalise, trim, or percent-decode them before comparison — a
slug is already in its only form, and every normalisation is therefore a
way to conflate two keys that OCN considers distinct.

### Name fields

`canonical_name`, `aliases`, `notes`, `attributed_to`,
`attribution_source`, `historical_notes` and the locale sidecars carry
Unicode text.

1. They MUST be stored in **Unicode Normalization Form C** (NFC).
2. They MUST spell eponyms with **true diacritics**, following the
   person's own orthography — `Sämisch`, `López`, `Grünfeld`, `Maróczy`
   — not an ASCII transliteration. The validator enforces the retired
   ASCII forms as a regression guard (check 17).
3. They MUST NOT contain the middle dot, invisible spacing characters,
   or ASCII control characters (check 14), and MUST NOT carry leading,
   trailing or doubled spaces (check 15).

### ASCII folding is a search affordance, never a key

Consumers SHOULD offer ASCII-folded matching for **search and lookup**,
so that a user typing `Samisch` or `Lopez` finds the row. This is a
presentation-layer equivalence only. Implementations MUST NOT store the
folded form, MUST NOT join on it, and MUST NOT emit it in any published
artefact — folding is lossy and two distinct names can fold together.
The `ocn-chess` package implements the affordance as a folded index
beside the true names (`Catalog.by_name`).

The full policy, the surname-by-surname evidence and the three applied
normalisation tiers are Annex B (informative).

## Extension mechanism

OCN-1 is extended by registration, not by ad-hoc convention. Three
registries exist; each of them **is** the spec section that lists it.

### Flags registry

`flags` is a pipe-separated list drawn from this registry. It is an
**open registry**: adding a value is a minor version, and this table is
the authoritative list as of spec 1.3.

| Flag | Meaning |
|---|---|
| `gambit` | The line's defining feature is a deliberate material offer. |
| `sharp` | Concrete, forcing theory where a single move-order error is usually decisive. |
| `closed` | Blocked or semi-blocked pawn structure; manoeuvring rather than contact play. |
| `endgame` | The named tabiya is already an endgame (e.g. the Berlin Wall). |
| `theoretical` | The line is defined by, and only navigable with, published analysis. |
| `deprecated` | The slug has been superseded. It remains published and its successor is recorded in the redirects sidecar — see the deprecation lifecycle. |

A consumer MUST NOT reject a row solely because it carries a flag the
consumer does not recognise: an unknown value means the row was written
against a later minor version, and the correct behaviour is to preserve
and ignore it.

### Private-use flags: the `x-` prefix

Any flag beginning with `x-` is **reserved for private use** and will
never be registered. A validator MUST ignore `x-` flags and MUST
preserve them when rewriting a row; a consumer MUST NOT attach meaning
to one it did not itself define. Private flags MUST NOT appear in the
reference catalogue — they exist so a downstream fork can carry its own
tags without forking the schema. (Honesty note: `tools/validate.py`
does not implement the `x-` exemption yet; it validates the reference
catalogue, which by rule contains none. The obligation above binds any
validator that accepts third-party catalogues.)

### Locale alias sidecars

A localised name set is registered as one TSV per locale, named

```
catalog/ocn-1.aliases.<bcp47>.tsv
```

where `<bcp47>` is a BCP 47 language tag (`ca`, `es`, `pt-BR`). The file
has a header row and exactly two columns, `ocn1` and `name`. Partial
coverage is by design: a consumer renders the localised name when the
slug is present and falls back to the English `canonical_name`, which is
always correct and always definitive. Name fields in a sidecar follow
the same canonicalisation rules as the catalogue's.

Registered locales as of spec 1.3: `ca` (Catalan), `es` (Spanish).
Adding a locale file, or rows to one, is a patch.

## Versioning

OCN-1 versions the **catalogue** semantically, and the version class of
a change is decided **field by field**. The earlier three-line rule
("minor = new entries") could not classify most of the edits the
catalogue actually receives, and version 1.2.0 shipped a change it did
not authorise (`errata.md`, E-002). The table is the rule now.

### Field-level change classes

| Change | Class |
|---|---|
| A published `ocn1` is removed | **major** (2.x) |
| A published `ocn1` is re-pointed to a different position | **major** |
| The slug grammar changes (character set, separator, move notation) | **major** |
| The profile segment cap is raised | **major** |
| An existing row's class letter changes | **major** |
| A new entry is added | minor |
| `canonical_name` changes on an existing row | minor, **changelog entry required** |
| `eco_legacy` is corrected on an existing row | minor, changelog entry required |
| `transposes_to` or `same_as` is added or corrected | minor |
| A flag is added to the registry | minor |
| A row is marked `deprecated` and its successor added | minor |
| A profile rule is tightened, the shipped catalogue already satisfying it | minor |
| `aliases` added or removed | patch |
| `notes` or `historical_notes` edited | patch |
| `attributed_to` / `attribution_source` added, re-sourced or withdrawn | patch |
| A locale sidecar is added, or rows added to one | patch |
| Spec prose clarified without changing a rule | patch |

Two standing rules survive unchanged from earlier editions and are
restated here as MUST-level obligations:

- Once a release is tagged, an entry's `ocn1` MUST NOT be re-pointed to
  a different position.
- Within the 1.x line a slug is **never removed and never reused**.
  Corrections go through the deprecation lifecycle below.

**Retroactive effect.** These classes legalise, explicitly and in
advance of the next release, the class of change that release 1.2.0
already made: 683 `canonical_name` values were normalised to true
diacritics under a minor bump while no slug, move sequence or position
moved. `errata.md` E-002 records it as the motivating precedent, and
under the table above it is a minor with a required changelog entry —
which 1.2.0's release notes in fact carried. Nothing about 1.2.0 is
being re-litigated; the rule is being written to match the practice that
was already correct.

Known deviations from this policy, and clauses this document has had to
correct about itself, remain recorded openly in
[`errata.md`](errata.md).

### Deprecation lifecycle (normative)

The mechanism that lets a wrong slug be corrected without breaking a
published key. It replaces in-place migration entirely: the QID
re-point that predates it is `errata.md` E-001.

1. The superseded row **stays in the catalogue**, keeping its `ocn1`,
   its position, its parent and its history. It MUST NOT be deleted.
2. `deprecated` is added to the superseded row's `flags`.
3. The successor row is added as a normal new entry with its own slug,
   under the normal profile rules.
4. The pair is recorded in the permanent redirects sidecar
   `catalog/ocn-1.redirects.tsv` (format below). The sidecar is
   append-only: a row, once written, is never edited or removed.
5. Both rows and the redirect ship in the **same release**, and the
   release notes name the pair.
6. The whole operation is a **minor** version.
7. The deprecated slug MUST NOT be reused for anything else, ever, and
   MUST NOT be removed within the 1.x line. Removal is a 2.x change.
8. Consumers resolving a slug they do not recognise SHOULD consult the
   redirects sidecar and MAY follow a redirect once. Redirects are not
   chained: a successor MUST NOT itself be deprecated in the same
   release.

**Redirects sidecar format.** Tab-separated, one header row, sorted by
`deprecated_slug`:

| Column | Description |
|---|---|
| `deprecated_slug` | The superseded `ocn1`. Still present in the catalogue, flagged `deprecated`. |
| `successor_slug` | The `ocn1` that replaces it. MUST exist in the catalogue. |
| `since_version` | The catalogue version that shipped the pair, without the tag prefix (e.g. `1.4.0`). |
| `reason` | One of the closed set `spec-violation`, `misclassification`, `duplicate`, `rename`. |

The file ships empty (header only) with spec 1.3: no deprecation has
been executed under this lifecycle yet.

**First scheduled case: `A.Hol`.** The Dutch Defence is filed under the
token `Hol`, derived from "Holland" rather than from its own
`canonical_name`, "Dutch Defence". That contradicts the family
abbreviation rules above, which take the first three pronounceable
characters *of the name* — which would give
<!-- NON-CATALOGUE: scheduled successor slug, not yet minted -->
`A.Dut`. It is the only token in the catalogue that violates the
abbreviation rules outright, and it is therefore designated the
lifecycle's first worked example.

**This is scheduled, not done.** `A.Hol` and its 113 descendants are
live, valid and unchanged; the successor slug does not exist yet; the
redirects sidecar is empty. The migration is its own gated catalogue lot
(114 rows, a manifest, a GO), not part of this spec change — spec 1.3
supplies the procedure, and the lot executes it. Note that the `Dut`
token is already in use subtree-locally (`A.Bir.Dut`, `A.Pol.Dut`) and
that is not a collision: tokens are subtree-local labels, scoped by
their parent, which is exactly why the mnemonic-unification proposals
for `Chi`/`Cha`/`Sch`/`RyL` are **not** scheduled — those tokens do not
violate any rule, and re-cutting them would shred slug stability for
aesthetics.

### Conformance corpus (normative)

The corpus in [`conformance/`](../conformance/) is a normative part of
this specification. It is two files — `valid.tsv` (slugs that MUST be
accepted) and `invalid.tsv` (slug plus reason code, which MUST be
rejected) — plus a README defining the closed reason-code set and the
order in which rules are evaluated, so that every rejection has exactly
one correct reason.

An implementation conforms to the slug layer of OCN-1 when it accepts
every case in `valid.tsv`, rejects every case in `invalid.tsv`, and
accepts every `ocn1` in the reference catalogue. The corpus is versioned
with this document: cases are added when a rule is added, and a case is
never removed or weakened within the 1.x line.

`tools/tests/test_conformance_corpus.py` runs the corpus against a
parser written from this document's ABNF and profile — deliberately a
second implementation, sharing no regex with `tools/validate.py` — and
asserts that the two agree on all ~100 corpus cases and on all 5,899
catalogue slugs. That agreement is the conformance claim.

The older fixtures under `tools/tests/fixtures/` remain the validator's
own regression suite. They are informative; the corpus is the spec.

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
- **v1.3 (2026-07-29, unreleased until the next catalogue tag)** — the
  standards edition. The prose production is replaced by a normative
  RFC 5234 ABNF and the grammar/profile split is stated explicitly: the
  grammar is major-versioned, the profile (CP-1 to CP-5) minor-versioned
  and tightenable only against a catalogue that already satisfies it.
  Token ambiguity is settled normatively by the maximal-SAN-suffix parse
  rule, with the 39 grandfathered SAN-shaped named tokens published in
  full and closed to new entries (validator check 22). New sections:
  Requirements language (BCP 14), Conformance (Producer / Consumer /
  Validator obligations), String canonicalisation (ASCII case-significant
  slugs, NFC name fields, ASCII folding as a search affordance only),
  Extension mechanism (flags registry, `x-` private-use prefix,
  `ocn-1.aliases.<bcp47>.tsv` locale sidecars), Versioning 2.0 with
  field-level change classes (which legalise the 1.2.0 mass rename
  explicitly, `errata.md` E-002), and the deprecation lifecycle with the
  permanent redirects sidecar `catalog/ocn-1.redirects.tsv` — shipped
  empty, with `A.Hol` designated its first scheduled case. The
  conformance corpus becomes normative and moves to
  [`conformance/`](../conformance/). No catalogue change.

## Conformance

This section is the checklist. Every obligation below is stated
elsewhere in this document; nothing new is introduced here, and each
item names the section it draws on so a disagreement can be traced.

An implementation conforms as one or more of three classes. A tool that
both mints rows and reads them MUST satisfy both lists.

### Producer — mints slugs and catalogue rows

- **P-1** MUST emit only profile-valid slugs: grammar-valid, and
  satisfying CP-1 to CP-5 of the profile in force. (Format)
- **P-2** MUST NOT mint a named token that parses as `san-move`. The
  grandfathered table is closed. (CP-5)
- **P-3** MUST NOT re-point or remove a published `ocn1`. A slug found
  to be wrong goes through the deprecation lifecycle, and the pair MUST
  be recorded in `catalog/ocn-1.redirects.tsv`. (Versioning;
  Deprecation lifecycle)
- **P-4** MUST classify every change by the field-level table before
  choosing a version number, and MUST publish a changelog entry for a
  `canonical_name` or `eco_legacy` change. (Field-level change classes)
- **P-5** MUST pair a non-empty `attributed_to` with an
  `attribution_source` citing published, publicly checkable evidence.
  (Catalogue)
- **P-6** MUST store name fields in NFC with true diacritics, and MUST
  NOT emit an ASCII-folded form in a published artefact. (String
  canonicalisation)
- **P-7** MUST resolve every duplicate-FEN group: exactly one canonical
  row, every other row carrying `transposes_to` into the group, or the
  group declared co-canonical with `same_as`. `transposes_to` and
  `same_as` MUST NOT both appear on one row. (Canonicalisation by
  position; Co-canonical preservation)
- **P-8** SHOULD append a move-tail segment only where opening
  literature attaches a name to that tabiya. (`move` segments)
- **P-9** MUST NOT emit a flag outside the registry, and MUST NOT ship
  an `x-` private-use flag in a catalogue presented as the reference
  catalogue. (Extension mechanism)

### Consumer — parses slugs, joins on them, displays them

- **C-1** MUST accept every slug up to the profile cap of the version it
  claims to support — seven segments, five-segment move tails,
  grandfathered SAN-shaped named tokens included. An implementation
  written against a narrower reading of an earlier edition rejects about
  a quarter of the reference catalogue. (`errata.md`, E-003)
- **C-2** MUST partition a slug with the maximal-SAN-suffix parse rule
  when it needs to tell a named token from a move. (Token ambiguity)
- **C-3** MUST treat slugs as case-significant ASCII byte strings, and
  MUST NOT normalise, fold or trim them before comparison. (String
  canonicalisation)
- **C-4** MUST normalise the en-passant field to the legal-capture form
  before comparing any `fen_key`, in both directions. (Annex A)
- **C-5** MUST NOT deduplicate rows on position identity. Rows sharing a
  FEN are distinct published names by editorial decision; collapsing
  them destroys the identities `same_as` exists to preserve.
  (Co-canonical preservation)
- **C-6** SHOULD follow `transposes_to` exactly once when resolving a
  position to a name, and MUST NOT assume the target carries a further
  pointer. (Canonicalisation by position)
- **C-7** SHOULD apply the deepest-match rule for ECO to OCN-1, and
  SHOULD report a tie rather than silently pick one of the tied rows.
  (Looking up a slug from an ECO code)
- **C-8** MUST NOT assume OCN's class letter equals ECO's, and MUST
  consult `catalog/ocn-1.eco-divergence.tsv` before bucketing rows by
  letter. (Borderline rules)
- **C-9** MUST special-case the five class roots: they carry no
  `moves_uci`, no `fen_key` and no zobrist, because they are filters,
  not positions. (Annex A)
- **C-10** MUST NOT reject a row solely for carrying an unrecognised
  flag, and MUST preserve `x-` flags it does not understand. (Extension
  mechanism)
- **C-11** MAY use ASCII-folded matching for search, and MUST NOT use it
  as a storage form or a join key. (String canonicalisation)
- **C-12** SHOULD consult `catalog/ocn-1.redirects.tsv` when a slug is
  not found, and MAY follow a redirect once. (Deprecation lifecycle)

### Validator — decides whether a catalogue is conforming

- **V-1** MUST implement both layers, and MUST distinguish them in its
  diagnostics: a grammar violation and a profile violation are different
  failures with different version consequences. (The two layers)
- **V-2** MUST use the maximal-SAN-suffix parse rule to classify
  segments, not a left-to-right heuristic. (Token ambiguity)
- **V-3** MUST reject a SAN-shaped named token that is absent from the
  grandfathered table. (CP-5; `tools/validate.py` check 22)
- **V-4** MUST accept every case in `conformance/valid.tsv` and reject
  every case in `conformance/invalid.tsv`, agreeing with the declared
  reason code's layer. (Conformance corpus)
- **V-5** MUST accept 100% of the reference catalogue of the release it
  validates. A validator that rejects a shipped row has found a spec
  bug, not a data bug, until the catalogue is proven wrong.
  (Requirements language)
- **V-6** MUST enforce the referential contracts: parent existence and
  depth, prefix consistency, `transposes_to` and `same_as` targets and
  their FEN equality. (Catalogue relations)
- **V-7** MUST recompute a derived sidecar rather than trust it, and
  MUST fail when the committed file disagrees. (`tools/validate.py`
  check 21)
- **V-8** MUST ignore `x-` flags rather than fail on them, and MUST
  preserve them if it rewrites a row. (Extension mechanism; not yet
  implemented in `tools/validate.py`, which validates the reference
  catalogue only)

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

Rule 4 is the trap. Many FEN emitters print the en-passant square after
every double pawn push, whether or not the capture is legal — among
them python-chess when asked for that form (`Board.fen(en_passant=
"fen")`), and the FEN strings that arrive from PGN headers and UCI
engines. Two `fen_key`s for the same position must compare equal, so
OCN normalises to the *legal-capture* form — the same convention the
Polyglot hash uses. Consumers comparing their own FENs against OCN MUST
apply the same normalisation. The `ocn-chess` package ships it as
`ocn.fen_key()`, with `ocn.fen.from_board()` for anybody holding a
board object; `tools/ocn.py` carries the in-repo copy.

The exported `fen` column is `fen_key` plus the true halfmove clock and
fullmove number of the replayed line, so it can be handed to a board
library unchanged. Those counters are **not** part of position
identity: compare on `fen_key`, never on `fen`. (Before the `ocn-chess`
package they were emitted as a placeholder `0 1`, which made the column
misleading rather than merely incomplete.)

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

## Annex B — Diacritic normalisation (informative)

The String canonicalisation section states the rule: name fields are
stored NFC with the eponym's own orthography. The evidence behind it —
the policy argument, the surname-by-surname survey of the pre-1.2.0
catalogue, and the three applied normalisation tiers (755 rows) whose
retired ASCII forms `tools/validate.py` now guards as check 17 — is
[`docs/diacritic-normalization-map.md`](../docs/diacritic-normalization-map.md).

That document is informative and is deliberately not inlined: it is a
dated record of how a specific catalogue was normalised, not a rule an
independent implementer has to satisfy. The rule is in the normative
section; the map is the audit trail.

## Acknowledgements

OCN-1 builds on the work of:

- Šahovski Informator (1971) for the A/B/C/D/E classification.
- Lichess Chess Openings (CC0) for canonical English names.
- Hooper & Whyld, *Oxford Companion to Chess* (1984) for canonical name
  conventions.
- The community of chess players, coaches and database authors who have
  pointed out the limits of ECO for half a century.
