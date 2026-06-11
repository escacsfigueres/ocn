"""Self-contained test runner for tools/validate.py.

Iterates fixtures under tools/tests/fixtures/ and asserts that:

- valid_*.csv files validate cleanly (exit 0, "OK: ..." in stdout).
- invalid_*.csv files fail (exit 1) with an expected substring in
  stderr.
- warn_*.csv files validate cleanly (exit 0) but with at least one
  WARN line in stderr matching an expected substring.

The expected substring is encoded in the filename / EXPECTED_* dict so
a reader (and CI) can see at a glance which rule each fixture exercises.

Run it directly:
    python3 tools/tests/test_validate.py

Or via the canonical entry point:
    python3 -m unittest tools.tests.test_validate
"""
from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
VALIDATE = REPO_ROOT / "tools" / "validate.py"
FIXTURES = Path(__file__).resolve().parent / "fixtures"

# Each invalid fixture pairs with the extra CLI args it needs (usually
# none) and a substring expected on stderr. The substring should be
# specific enough to confirm the right rule fired, but not so brittle
# that small wording tweaks break CI.
EXPECTED_INVALID: dict[str, tuple[tuple[str, ...], str]] = {
    "invalid_duplicate_slug.csv": ((), "duplicate slug"),
    "invalid_depth_mismatch.csv": ((), "dots but depth"),
    "invalid_missing_parent.csv": ((), "missing parent"),
    "invalid_uci.csv": ((), "invalid UCI move"),
    "invalid_class_root.csv": ((), "does not match format"),
    "invalid_check_in_slug.csv": ((), "does not match format"),
    "invalid_attribution_no_source.csv": ((), "without 'attribution_source'"),
    "invalid_san_at_class_root.csv": ((), "immediately after the class"),
    "invalid_named_after_tail.csv": ((), "follows a move tail"),
    "invalid_unknown_flag.csv": ((), "unknown flag"),
    "invalid_missing_schema_column.csv": ((), "missing required column"),
    "invalid_transposes_to_missing.csv": ((), "transposes_to='A.Bar'"),
    "invalid_transposes_to_self.csv": ((), "pointing to itself"),
    "invalid_transposes_to_fen_mismatch.csv": ((), "FEN keys differ"),
    "invalid_same_as_missing.csv": ((), "same_as='A.Bar'"),
    "invalid_same_as_self.csv": ((), "same_as pointing to itself"),
    "invalid_same_as_fen_mismatch.csv": ((), "this is not a co-canonical pair"),
    "invalid_same_as_with_transposes_to.csv": ((), "both same_as"),
    "invalid_duplicate_canonical_name.csv": ((), "duplicate canonical_name"),
    "invalid_banned_char_middle_dot.csv": ((), "banned character"),
    "invalid_banned_ascii_form.csv": (
        ("--ban-ascii-form", "Lopez=López"), "banned ASCII form"
    ),
    "invalid_whitespace_in_text.csv": ((), "stray whitespace"),
    "invalid_identity_alias.csv": ((), "identical to canonical_name"),
}

# Fixtures that MUST validate (exit 0) but emit a specific warning.
# The validator prints warnings to stderr with the prefix "WARN:".
# Same (extra_args, substring) shape as EXPECTED_INVALID.
EXPECTED_WARN: dict[str, tuple[tuple[str, ...], str]] = {
    "warn_orphan_attribution_source.csv": ((), "orphan citation"),
    "warn_banned_ascii_form_in_notes.csv": (
        ("--ban-ascii-form", "Lopez=López"), "banned ASCII form"
    ),
    "warn_child_shorter_name.csv": (("--audit-naming",), "shorter than parent"),
}

# Strict chess fixtures run with --strict-chess; the canonical catalogue
# is also expected to pass strict mode now that move-order debt is cleared.
EXPECTED_STRICT_INVALID: dict[str, str] = {
    "strict_invalid_illegal_move.csv": "illegal UCI move",
    "strict_invalid_san_mismatch.csv": "does not match appended move SAN",
}


def run_validator(fixture: Path, *extra_args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VALIDATE), *extra_args, str(fixture)],
        capture_output=True,
        text=True,
        check=False,
    )


class ValidatorTests(unittest.TestCase):
    def test_canonical_catalogue_validates(self) -> None:
        """The shipped catalogue must always validate clean."""
        catalogue = REPO_ROOT / "catalog" / "ocn-1.csv"
        self.assertTrue(catalogue.exists(), f"missing {catalogue}")
        for extra_args in ((), ("--strict-chess",)):
            with self.subTest(args=extra_args):
                result = run_validator(catalogue, *extra_args)
                self.assertEqual(
                    result.returncode,
                    0,
                    f"canonical catalogue failed: stderr={result.stderr!r}",
                )
                self.assertIn("OK:", result.stdout)

    def test_canonical_catalogue_header_matches_downstream_contract(self) -> None:
        """OCN 0.2 ships 14 columns in a fixed order. Downstream tools
        (chess-parquet's efcdb-openings) parse the catalogue against
        this exact contract; any reordering or addition is a breaking
        change and MUST be coordinated with the downstream release.
        """
        import csv

        catalogue = REPO_ROOT / "catalog" / "ocn-1.csv"
        with catalogue.open(newline="") as f:
            header = next(csv.reader(f))
        self.assertEqual(
            header,
            [
                "ocn1",
                "canonical_name",
                "eco_legacy",
                "parent_ocn1",
                "moves_uci",
                "depth",
                "aliases",
                "flags",
                "notes",
                "attributed_to",
                "attribution_source",
                "historical_notes",
                "transposes_to",
                "same_as",
            ],
            "OCN 0.2 catalogue header drift — downstream chess-parquet "
            "consumers depend on this exact 14-column order",
        )

    def test_valid_fixtures_pass(self) -> None:
        for fixture in sorted(FIXTURES.glob("valid_*.csv")):
            with self.subTest(fixture=fixture.name):
                result = run_validator(fixture)
                self.assertEqual(
                    result.returncode,
                    0,
                    f"{fixture.name} should validate. "
                    f"stdout={result.stdout!r}, stderr={result.stderr!r}",
                )
                self.assertIn("OK:", result.stdout)

    def test_invalid_fixtures_fail_with_expected_message(self) -> None:
        for fixture_name, (extra_args, expected) in EXPECTED_INVALID.items():
            fixture = FIXTURES / fixture_name
            with self.subTest(fixture=fixture_name):
                self.assertTrue(
                    fixture.exists(), f"missing fixture {fixture_name}"
                )
                result = run_validator(fixture, *extra_args)
                self.assertNotEqual(
                    result.returncode,
                    0,
                    f"{fixture_name} should NOT validate. "
                    f"stdout={result.stdout!r}, stderr={result.stderr!r}",
                )
                self.assertIn(
                    expected,
                    result.stderr,
                    f"{fixture_name}: expected {expected!r} in stderr, "
                    f"got {result.stderr!r}",
                )

    def test_every_invalid_fixture_has_an_expected_message(self) -> None:
        """Guard: a new invalid_*.csv must come with an EXPECTED_INVALID
        entry — otherwise it would silently pass-by-default if the
        validator doesn't error."""
        on_disk = {p.name for p in FIXTURES.glob("invalid_*.csv")}
        registered = set(EXPECTED_INVALID)
        missing = on_disk - registered
        self.assertFalse(
            missing,
            f"invalid_*.csv fixtures without an EXPECTED_INVALID entry: {missing}",
        )
        spurious = registered - on_disk
        self.assertFalse(
            spurious,
            f"EXPECTED_INVALID entries without a fixture file: {spurious}",
        )

    def test_warn_fixtures_validate_with_expected_warning(self) -> None:
        """warn_*.csv files MUST validate (exit 0) AND emit the expected
        WARN substring on stderr. They guard against the warning being
        accidentally promoted to an error or silently dropped."""
        for fixture_name, (extra_args, expected) in EXPECTED_WARN.items():
            fixture = FIXTURES / fixture_name
            with self.subTest(fixture=fixture_name):
                self.assertTrue(
                    fixture.exists(), f"missing fixture {fixture_name}"
                )
                result = run_validator(fixture, *extra_args)
                self.assertEqual(
                    result.returncode,
                    0,
                    f"{fixture_name} should validate (exit 0). "
                    f"stdout={result.stdout!r}, stderr={result.stderr!r}",
                )
                self.assertIn(
                    "WARN:",
                    result.stderr,
                    f"{fixture_name}: expected a WARN line, got "
                    f"stderr={result.stderr!r}",
                )
                self.assertIn(
                    expected,
                    result.stderr,
                    f"{fixture_name}: expected {expected!r} in stderr, "
                    f"got {result.stderr!r}",
                )

    def test_every_warn_fixture_has_an_expected_message(self) -> None:
        on_disk = {p.name for p in FIXTURES.glob("warn_*.csv")}
        registered = set(EXPECTED_WARN)
        self.assertEqual(on_disk, registered,
                         f"warn fixtures vs EXPECTED_WARN drift: "
                         f"on_disk={on_disk}, registered={registered}")

    def test_banned_ascii_forms_match_the_applied_tier_maps(self) -> None:
        """Both diacritic lots are applied (Tier 1 on 2026-06-11, Tier 2
        the same day), so validate.py's BANNED_ASCII_NAME_FORMS must
        mirror the union of the generator's tier maps — data and guard
        activate atomically and stay in sync."""
        sys.path.insert(0, str(REPO_ROOT / "tools"))
        from generate_diacritic_manifest import TIER1_FORMS, TIER2_FORMS
        from validate import BANNED_ASCII_NAME_FORMS

        expected = {
            variant: target
            for forms in (TIER1_FORMS, TIER2_FORMS)
            for target, variants in forms.items()
            for variant in variants
        }
        self.assertEqual(BANNED_ASCII_NAME_FORMS, expected)

    def test_child_shorter_check_is_opt_in(self) -> None:
        """The child-shorter heuristic fires on ~1,400 legitimate rows of
        the live catalogue (names shorten at depth by design), so it must
        stay silent unless --audit-naming is passed."""
        fixture = FIXTURES / "warn_child_shorter_name.csv"
        result = run_validator(fixture)
        self.assertEqual(result.returncode, 0)
        self.assertNotIn("shorter than parent", result.stderr)

    def test_strict_chess_fixtures_fail_with_expected_message(self) -> None:
        for fixture_name, expected in EXPECTED_STRICT_INVALID.items():
            fixture = FIXTURES / fixture_name
            with self.subTest(fixture=fixture_name):
                self.assertTrue(
                    fixture.exists(), f"missing fixture {fixture_name}"
                )
                result = run_validator(fixture, "--strict-chess")
                self.assertNotEqual(
                    result.returncode,
                    0,
                    f"{fixture_name} should NOT validate in strict chess mode. "
                    f"stdout={result.stdout!r}, stderr={result.stderr!r}",
                )
                self.assertIn(
                    expected,
                    result.stderr,
                    f"{fixture_name}: expected {expected!r} in stderr, "
                    f"got {result.stderr!r}",
                )

    def test_every_strict_fixture_has_an_expected_message(self) -> None:
        on_disk = {p.name for p in FIXTURES.glob("strict_invalid_*.csv")}
        registered = set(EXPECTED_STRICT_INVALID)
        self.assertEqual(on_disk, registered,
                         f"strict fixtures vs EXPECTED_STRICT_INVALID drift: "
                         f"on_disk={on_disk}, registered={registered}")


if __name__ == "__main__":
    unittest.main()
