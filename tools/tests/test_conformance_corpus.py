"""The OCN-1 conformance corpus, run against a from-spec reimplementation.

`conformance/` is a normative part of spec 1.3. This module is what makes
that claim checkable: it implements the spec's ABNF and catalogue profile
**independently** — recursive descent and explicit character classes
written from `spec/OCN-1.md`, sharing no regex and no parsing code with
`tools/validate.py` — and then asserts that the two implementations agree

  * on all 101 corpus cases (60 valid, 41 invalid), and
  * on all 5,899 slugs of the reference catalogue.

That agreement is the conformance claim. A corpus that only ever ran
against the implementation it was derived from would prove nothing, so
nothing below may import `validate.SLUG_RE` or `validate.SAN_RE` for
parsing. The two constants that *are* imported —
`GRANDFATHERED_SAN_NAMED_TOKENS` and `KNOWN_LONG_TOKENS` — are imported
only to be compared against the tables published in the spec, which is
the direction of the pin: the document is the source of truth, the
validator mirrors it.

Run it directly:
    python3 tools/tests/test_conformance_corpus.py

Or via the canonical entry point:
    python3 -m unittest tools.tests.test_conformance_corpus
"""
from __future__ import annotations

import csv
import itertools
import re
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT / "tools") not in sys.path:
    # Only so the agreement tests can import validate.py's constants for
    # comparison. Nothing in the from-spec parser below touches it.
    sys.path.insert(0, str(REPO_ROOT / "tools"))
CONFORMANCE = REPO_ROOT / "conformance"
VALID_TSV = CONFORMANCE / "valid.tsv"
INVALID_TSV = CONFORMANCE / "invalid.tsv"
CORPUS_README = CONFORMANCE / "README.md"
SPEC = REPO_ROOT / "spec" / "OCN-1.md"
CATALOG = REPO_ROOT / "catalog" / "ocn-1.csv"

# ---------------------------------------------------------------------
# The from-spec implementation.
#
# spec/OCN-1.md, "Grammar (normative ABNF)":
#
#   ocn-slug    = class *( dot named ) *( dot san-move )
#   class       = %x41 / %x42 / %x43 / %x44 / %x45
#   dot         = %x2E
#   named       = 1*token-char
#   token-char  = ALPHA / DIGIT / %x5F / %x3D / %x2D
#   san-move    = castling / piece-move
#   castling    = %x4F.2D.4F [ %x2D.4F ]
#   piece-move  = [ piece ] [ file ] [ rank ] [ %x78 ] square [ promotion ]
#   piece       = %x4E / %x42 / %x52 / %x51 / %x4B
#   promotion   = %x3D promo-piece
#   promo-piece = %x4E / %x42 / %x52 / %x51
#   square      = file rank
#   file        = %x61-68
#   rank        = %x31-38
# ---------------------------------------------------------------------

DOT = "."
CLASS_LETTERS = frozenset("ABCDE")
ALPHA = frozenset(
    "".join(chr(c) for c in range(0x41, 0x5B))
    + "".join(chr(c) for c in range(0x61, 0x7B))
)
DIGIT = frozenset(chr(c) for c in range(0x30, 0x3A))
TOKEN_CHARS = ALPHA | DIGIT | {"_", "=", "-"}
PIECE = frozenset("NBRQK")
PROMO_PIECE = frozenset("NBRQ")
FILE_CHARS = frozenset(chr(c) for c in range(0x61, 0x69))   # a-h
RANK_CHARS = frozenset(chr(c) for c in range(0x31, 0x39))   # 1-8
CAPTURE = "x"                                          # "x"
PROMOTION_MARK = "="                                   # "="

PROFILE_SEGMENT_CAP = 7

REASON_CODES = (
    "G-EMPTY-SEGMENT",
    "G-CLASS",
    "G-CHAR",
    "CP-1",
    "CP-2",
    "CP-3",
    "CP-4",
    "CP-5",
)


def matches_castling(token: str) -> bool:
    """castling = %x4F.2D.4F [ %x2D.4F ]  ->  "O-O" or "O-O-O"."""
    return token in ("O-O", "O-O-O")


def matches_piece_move(token: str) -> bool:
    """piece-move = [ piece ] [ file ] [ rank ] [ "x" ] square [ promotion ]

    Four of the six elements are optional, which makes the production
    non-deterministic: `b8=Q` parses only if BOTH [file] and [rank] are
    skipped, so that `b8` can be the mandatory `square`. A greedy
    left-to-right walk gets that wrong. ABNF alternation is not greedy,
    so we enumerate the 16 subsets of the optional prefix elements and
    accept if any of them consumes the token exactly — which is what the
    production means.
    """
    n = len(token)
    for use_piece in (True, False):
        for use_file in (True, False):
            for use_rank in (True, False):
                for use_capture in (True, False):
                    i = 0
                    if use_piece:
                        if i >= n or token[i] not in PIECE:
                            continue
                        i += 1
                    if use_file:
                        if i >= n or token[i] not in FILE_CHARS:
                            continue
                        i += 1
                    if use_rank:
                        if i >= n or token[i] not in RANK_CHARS:
                            continue
                        i += 1
                    if use_capture:
                        if i >= n or token[i] != CAPTURE:
                            continue
                        i += 1
                    # square = file rank  (mandatory)
                    if i + 1 >= n:
                        continue
                    if token[i] not in FILE_CHARS:
                        continue
                    if token[i + 1] not in RANK_CHARS:
                        continue
                    i += 2
                    # [ promotion ] = [ "=" promo-piece ]
                    if i < n:
                        if token[i] != PROMOTION_MARK:
                            continue
                        i += 1
                        if i >= n or token[i] not in PROMO_PIECE:
                            continue
                        i += 1
                    if i == n:
                        return True
    return False


def matches_san_move(token: str) -> bool:
    """san-move = castling / piece-move."""
    return matches_castling(token) or matches_piece_move(token)


def grammar_reason(slug: str) -> str | None:
    """Reject reason from the ABNF alone, or None if grammar-valid."""
    segments = slug.split(DOT)
    if any(segment == "" for segment in segments):
        return "G-EMPTY-SEGMENT"
    if segments[0] not in CLASS_LETTERS:
        return "G-CLASS"
    for segment in segments[1:]:
        for char in segment:
            if char not in TOKEN_CHARS:
                return "G-CHAR"
    return None


def split_slug(slug: str) -> tuple[list[str], list[str]]:
    """(named region, move tail) under the maximal-SAN-suffix parse rule.

    spec/OCN-1.md, "Token ambiguity": the move tail is the *maximal*
    trailing run of segments that parse as san-move; every segment before
    it is a named token, whatever its shape.
    """
    rest = slug.split(DOT)[1:]
    cut = len(rest)
    while cut and matches_san_move(rest[cut - 1]):
        cut -= 1
    return rest[:cut], rest[cut:]


def profile_reason(
    slug: str,
    *,
    registry: frozenset[str],
    grandfathered: frozenset[str],
) -> str | None:
    """Reject reason from the catalogue profile, or None if profile-valid.

    Assumes the slug is already grammar-valid. Rules are evaluated in the
    order the corpus README declares, rule by rule (not token by token),
    so that every case has exactly one correct reason.
    """
    segments = slug.split(DOT)
    if len(segments) > PROFILE_SEGMENT_CAP:
        return "CP-1"
    named, _tail = split_slug(slug)
    if len(segments) > 1 and not named:
        return "CP-2"
    for token in named:
        if len(token) != 3 and token not in registry:
            return "CP-3"
    for token in named:
        if all("a" <= char <= "z" for char in token):
            return "CP-4"
    for token in named:
        if matches_san_move(token) and token not in grandfathered:
            return "CP-5"
    return None


def reject_reason(
    slug: str,
    *,
    registry: frozenset[str],
    grandfathered: frozenset[str],
) -> str | None:
    """The single declared reason this slug is not an OCN-1 1.x slug."""
    reason = grammar_reason(slug)
    if reason is not None:
        return reason
    return profile_reason(slug, registry=registry, grandfathered=grandfathered)


# ---------------------------------------------------------------------
# Corpus and spec-table loading.
# ---------------------------------------------------------------------

ESCAPE_RE = re.compile(r"\\(\\|u[0-9a-fA-F]{4})")


def decode_escapes(text: str) -> str:
    r"""Decode the corpus escape convention: `\uXXXX` and `\\`."""
    def sub(match: re.Match[str]) -> str:
        body = match.group(1)
        return "\\" if body == "\\" else chr(int(body[1:], 16))
    return ESCAPE_RE.sub(sub, text)


def load_valid_cases() -> list[str]:
    cases = []
    for line in VALID_TSV.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        cases.append(decode_escapes(line))
    return cases


def load_invalid_cases() -> list[tuple[str, str]]:
    cases = []
    for line in INVALID_TSV.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        slug, _tab, code = line.partition("\t")
        cases.append((decode_escapes(slug), code.strip()))
    return cases


def load_catalogue_slugs() -> list[str]:
    with CATALOG.open(newline="", encoding="utf-8") as handle:
        return [(row["ocn1"] or "").strip() for row in csv.DictReader(handle)]


def spec_table_first_column(header: str) -> frozenset[str]:
    """First column of the spec's markdown table with the given header row.

    The spec is the source of truth for both registries, so the parser
    below reads them out of the document rather than duplicating them.
    """
    lines = SPEC.read_text(encoding="utf-8").splitlines()
    try:
        start = lines.index(header)
    except ValueError as exc:  # pragma: no cover - guarded by test
        raise AssertionError(f"spec table header not found: {header!r}") from exc
    tokens = set()
    for line in lines[start + 2:]:            # skip header + separator row
        if not line.startswith("|"):
            break
        cell = line.split("|")[1].strip()
        tokens.add(cell.strip("`"))
    return frozenset(tokens)


SPEC_GRANDFATHER_HEADER = "| Token | Example slug |"
SPEC_REGISTRY_HEADER = "| Token | Meaning |"


class ConformanceCorpusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.grandfathered = spec_table_first_column(SPEC_GRANDFATHER_HEADER)
        cls.registry = spec_table_first_column(SPEC_REGISTRY_HEADER)
        cls.valid = load_valid_cases()
        cls.invalid = load_invalid_cases()
        cls.catalogue = load_catalogue_slugs()

    def reason(self, slug: str) -> str | None:
        return reject_reason(
            slug, registry=self.registry, grandfathered=self.grandfathered
        )

    # -- the corpus itself ------------------------------------------------

    def test_corpus_shape(self) -> None:
        self.assertEqual(len(self.valid), 60)
        self.assertEqual(len(self.invalid), 41)
        self.assertEqual(len(self.valid) + len(self.invalid), 101)
        self.assertEqual(len(set(self.valid)), len(self.valid),
                         "duplicate case in valid.tsv")
        slugs = [slug for slug, _ in self.invalid]
        self.assertEqual(len(set(slugs)), len(slugs),
                         "duplicate case in invalid.tsv")
        self.assertFalse(set(self.valid) & set(slugs),
                         "a slug appears in both valid.tsv and invalid.tsv")

    def test_reason_codes_are_the_closed_set(self) -> None:
        used = {code for _, code in self.invalid}
        self.assertEqual(used - set(REASON_CODES), set(),
                         "invalid.tsv uses a reason code outside the closed set")
        self.assertEqual(set(REASON_CODES) - used, set(),
                         "a declared reason code has no case exercising it")

    def test_reason_codes_documented_in_readme(self) -> None:
        readme = CORPUS_README.read_text(encoding="utf-8")
        for code in REASON_CODES:
            self.assertIn(f"`{code}`", readme,
                          f"reason code {code} is not documented in the README")

    # -- the from-spec parser vs the corpus -------------------------------

    def test_valid_cases_are_accepted(self) -> None:
        for slug in self.valid:
            with self.subTest(slug=slug):
                self.assertIsNone(
                    self.reason(slug),
                    f"valid.tsv case rejected by the from-spec parser: {slug!r}",
                )

    def test_invalid_cases_are_rejected_with_the_declared_reason(self) -> None:
        for slug, expected in self.invalid:
            with self.subTest(slug=slug, reason=expected):
                self.assertEqual(
                    self.reason(slug), expected,
                    f"invalid.tsv case {slug!r} should be rejected as "
                    f"{expected}",
                )

    # -- the from-spec parser vs the catalogue ----------------------------

    def test_catalogue_is_fully_accepted(self) -> None:
        """Spec 1.3 must accept 100% of the catalogue it ships with."""
        rejected = [
            (slug, self.reason(slug))
            for slug in self.catalogue
            if self.reason(slug) is not None
        ]
        self.assertEqual(rejected, [],
                         "the published grammar+profile rejects live rows")
        self.assertEqual(len(self.catalogue), 5899)

    # -- the two implementations must agree -------------------------------

    def test_slug_re_agrees_with_the_abnf_on_the_catalogue(self) -> None:
        """validate.py's SLUG_RE is the grammar layer; it must match all rows."""
        slug_re = self._validate_slug_re()
        for slug in self.catalogue:
            with self.subTest(slug=slug):
                self.assertIsNone(grammar_reason(slug))
                self.assertTrue(slug_re.match(slug))

    def test_slug_re_agrees_with_the_abnf_on_the_corpus(self) -> None:
        """Layer agreement, case by case.

        A `G-` case is rejected by the grammar, so SLUG_RE must NOT match
        it. A `CP-` case is grammar-valid and rejected by the profile, so
        SLUG_RE MUST match it — the profile is not SLUG_RE's job. Every
        valid case must match.
        """
        slug_re = self._validate_slug_re()
        for slug in self.valid:
            with self.subTest(case=slug, expect="match"):
                self.assertTrue(bool(slug_re.match(slug)))
        for slug, code in self.invalid:
            grammar_layer = code.startswith("G-")
            with self.subTest(case=slug, reason=code):
                self.assertEqual(grammar_reason(slug) is not None, grammar_layer)
                self.assertEqual(bool(slug_re.match(slug)), not grammar_layer)

    def test_parse_rule_agrees_with_the_validator_on_the_catalogue(self) -> None:
        """The maximal-SAN-suffix split, computed twice, must agree."""
        from validate import named_region  # noqa: PLC0415 - comparison only

        for slug in self.catalogue:
            with self.subTest(slug=slug):
                self.assertEqual(split_slug(slug)[0],
                                 named_region(slug.split(DOT)))

    # -- the spec tables are the source of truth --------------------------

    def test_spec_grandfather_table_pins_the_validator_constant(self) -> None:
        from validate import GRANDFATHERED_SAN_NAMED_TOKENS  # noqa: PLC0415

        self.assertEqual(self.grandfathered, GRANDFATHERED_SAN_NAMED_TOKENS)
        self.assertEqual(len(self.grandfathered), 39)

    def test_spec_named_token_registry_pins_the_validator_constant(self) -> None:
        from validate import KNOWN_LONG_TOKENS  # noqa: PLC0415

        self.assertEqual(self.registry, frozenset(KNOWN_LONG_TOKENS))

    def test_grandfather_table_is_computed_from_the_catalogue(self) -> None:
        """Not curated: the table is exactly the SAN-shaped named tokens
        the live catalogue contains. A padded table would let a new
        SAN-shaped token in through the back door; a short one would
        reject a shipped row."""
        observed = set()
        occurrences = 0
        for slug in self.catalogue:
            for token in split_slug(slug)[0]:
                if matches_san_move(token):
                    observed.add(token)
                    occurrences += 1
        self.assertEqual(observed, set(self.grandfathered))
        self.assertEqual(occurrences, 570)

    def test_every_grandfathered_token_is_san_shaped(self) -> None:
        for token in self.grandfathered:
            with self.subTest(token=token):
                self.assertTrue(matches_san_move(token))

    # -- the ABNF's own corners -------------------------------------------

    def test_promotion_needs_backtracking(self) -> None:
        """`b8=Q` parses only when [file] and [rank] are both skipped."""
        for token in ("b8=Q", "f8=N", "cxb8=R", "e1=Q"):
            with self.subTest(token=token):
                self.assertTrue(matches_piece_move(token))
        for token in ("b9=Q", "b8=K", "b8=", "=Q"):
            with self.subTest(token=token):
                self.assertFalse(matches_piece_move(token))

    def test_castling_and_non_moves(self) -> None:
        self.assertTrue(matches_san_move("O-O"))
        self.assertTrue(matches_san_move("O-O-O"))
        for token in ("Sic", "Naj", "150", "f3L", "O-O-O-O", "Nd5+", ""):
            with self.subTest(token=token):
                self.assertFalse(matches_san_move(token))

    def test_class_roots_are_valid(self) -> None:
        for root in "ABCDE":
            with self.subTest(root=root):
                self.assertIsNone(self.reason(root))

    # -- the ABNF and the shipped regexes describe the same language ------

    def test_abnf_san_move_equals_validator_san_re(self) -> None:
        """Exhaustive over every token of length 1-3 that SAN could use.

        The spec claims its `san-move` production matches `SAN_RE`
        exactly. Claiming it is cheap; 16,275 tokens is the proof.
        """
        from validate import SAN_RE  # noqa: PLC0415 - comparison only

        alphabet = "NBRQKOabcdefgh12345678x=-"
        mismatches = []
        for length in (1, 2, 3):
            for combo in itertools.product(alphabet, repeat=length):
                token = "".join(combo)
                if bool(SAN_RE.match(token)) != matches_san_move(token):
                    mismatches.append(token)
        self.assertEqual(mismatches, [])

    def test_abnf_slug_grammar_equals_validator_slug_re(self) -> None:
        """Exhaustive over every string of length 0-3 from a hostile
        alphabet: class letters, a non-class letter, the separator, every
        token character, and characters that must be rejected."""
        from validate import SLUG_RE  # noqa: PLC0415 - comparison only

        alphabet = "ABEFa.-_=+#/ 1x\t"
        mismatches = []
        for length in (0, 1, 2, 3):
            for combo in itertools.product(alphabet, repeat=length):
                text = "".join(combo)
                if (grammar_reason(text) is None) != bool(SLUG_RE.match(text)):
                    mismatches.append(text)
        self.assertEqual(mismatches, [])

    @staticmethod
    def _validate_slug_re() -> re.Pattern[str]:
        from validate import SLUG_RE  # noqa: PLC0415 - comparison only

        return SLUG_RE


if __name__ == "__main__":
    unittest.main()
