# OCN-1 conformance corpus

**Normative.** This directory is part of the OCN-1 specification, not a
test fixture directory. [`spec/OCN-1.md`](../spec/OCN-1.md) defines the
slug grammar and the catalogue profile; this corpus is the executable
statement of what that definition accepts and rejects.

An implementation conforms to the slug layer of OCN-1 when it

1. accepts every case in [`valid.tsv`](valid.tsv),
2. rejects every case in [`invalid.tsv`](invalid.tsv), and
3. accepts every `ocn1` in `catalog/ocn-1.csv` (5,899 rows).

The third condition is not decoration. The spec bends to the deployed
catalogue (`spec/errata.md`, E-003): a rule that rejects a shipped row is
a spec bug until the catalogue is proven wrong.

## Files

| File | Shape |
|---|---|
| `valid.tsv` | One slug per line. 60 cases. |
| `invalid.tsv` | `slug` TAB `reason_code`. 41 cases. |

In both files, lines beginning with `#` are comments and blank lines are
ignored. Comments carry the section structure, which is how a reader can
tell which structural shape a case is there to exercise.

`invalid.tsv` slugs may contain `\uXXXX` escapes (exactly four hex
digits, lowercase), and an implementation MUST decode them before
parsing. They exist because a TSV cannot carry a literal tab, cannot
carry a trailing space unambiguously, and this project does not put the
U+00B7 separator glyph in its own files even as a negative example. `\\`
is a literal backslash. No other escape is defined.

## Reason codes

A closed set. Adding a code means adding a rule to the spec.

Codes split into two layers, matching the spec's two-layer model, and
the layer is a hard property of the code: a **G-** case is rejected by
the ABNF alone, so `tools/validate.py`'s `SLUG_RE` must not match it; a
**CP-** case is grammar-valid and rejected by a catalogue-profile rule,
so `SLUG_RE` must match it. `tools/tests/test_conformance_corpus.py`
asserts exactly that, case by case.

| Code | Layer | Rejected because |
|---|---|---|
| `G-EMPTY-SEGMENT` | grammar | A dot-delimited segment is empty (leading dot, trailing dot, or a doubled dot). `named` is `1*token-char`. |
| `G-CLASS` | grammar | The first segment is not exactly one of `A` `B` `C` `D` `E`. |
| `G-CHAR` | grammar | A character outside `token-char` (`ALPHA / DIGIT / "_" / "=" / "-"`). Covers check `+` and mate `#` suffixes, whitespace, separator glyphs, non-ASCII letters and move annotations. |
| `CP-1` | profile | More than seven segments. |
| `CP-2` | profile | A non-root slug with no named segment: the move tail cannot start immediately after the class letter. |
| `CP-3` | profile | A named token that is neither exactly 3 characters nor listed in the spec's named-token registry. |
| `CP-4` | profile | A named token consisting solely of lowercase ASCII letters. |
| `CP-5` | profile | A named token that parses as `san-move` and is absent from the spec's grandfathered-token table. |

### Evaluation order

A slug can break more than one rule; the corpus declares exactly one
reason per case, so the order is normative:

```
G-EMPTY-SEGMENT, G-CLASS, G-CHAR, CP-1, CP-2, CP-3, CP-4, CP-5
```

The first rule that fires is the reported reason, and a rule is applied
across all tokens before the next rule is tried. One case in the corpus
depends on the order: `.Sic` is `G-EMPTY-SEGMENT` rather than `G-CLASS`,
because its first segment is empty *and* not a class letter. The other
place it bites is length: an over-long token is `CP-3` even when it
would also fail `CP-4` or `CP-5` — NON-CATALOGUE illustrations,
`B.sicilian.Naj` and `B.Sic.Naj.Bxc6x`.

`CP-4` and `CP-5` cannot both fire on one token, as it happens: every
`san-move` either ends in a rank digit or is uppercase castling, so no
SAN-shaped token is made of lowercase letters alone.

An implementation MAY report additional violations. It MUST report at
least the declared one, and it MUST NOT accept the slug.

## What the valid cases cover

- The five class roots, which are grammar-valid and carry no position.
- Depth 1 through 6, and both boundaries of the 7-segment profile cap.
- Move tails of every length the catalogue uses, 0 through 5.
- Grandfathered SAN-shaped named tokens — the `D.Sem.Bg5.Mos` /
  `D.Sem.Bg5` contrast is the maximal-SAN-suffix rule in one pair: the
  same token is a name in the first slug and a move in the second.
- Registry tokens (`RyL`, `KID`, `QGD`, `QGA`, `QID`, `OID`, `OldI`,
  `AntM`, `Cmb`).
- Named tokens that are not TitleCase letters: the numeric `B.Pir.150`
  and the mixed `E.Ben.Mod.Cls.MLn.Re8.f3L`.
- Castling (`O-O`, `O-O-O`), captures, and both file and rank SAN
  disambiguation in the tail.
- Four **synthetic** grammar corners the catalogue does not currently
  occupy — promotion (`=Q`, `=N`, capture-promotion) and the `_`
  token character. They are conforming strings and are not catalogue
  rows; the file marks them as such.

Every other case in `valid.tsv` is a live catalogue slug.

## Versioning

The corpus is versioned with the spec, and the spec version it belongs
to is stated at the top of `valid.tsv`. Current: **spec 1.3**.

Within the 1.x line, a case is never removed and never weakened: cases
are added when a rule is added. A `valid` case that had to become
`invalid` would be a major (2.x) change by definition, because it means
the grammar or the profile cap moved.

## Running it

```bash
python3 -m unittest tools.tests.test_conformance_corpus -v
```

The test implements the spec's ABNF and profile as an **independent
parser** — recursive descent plus regexes written from the document,
sharing no code with `tools/validate.py` — and then asserts that the two
implementations agree on all 101 corpus cases and all 5,899 catalogue
slugs. That agreement is the conformance claim; a corpus that only ever
ran against the implementation it was derived from would prove nothing.
