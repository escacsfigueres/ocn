"""Self-contained test runner for tools/validate.py.

Iterates fixtures under tools/tests/fixtures/ and asserts that:

- valid_*.csv files validate cleanly (exit 0, "OK: ..." in stdout).
- invalid_*.csv files fail (exit 1) with an expected substring in
  stderr. The expected substring is encoded in the filename so a
  reader (and CI) can see at a glance which rule each fixture
  exercises.

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

# Each invalid fixture pairs with a substring expected on stderr.
# The substring should be specific enough to confirm the right rule
# fired, but not so brittle that small wording tweaks break CI.
EXPECTED_INVALID: dict[str, str] = {
    "invalid_duplicate_slug.csv": "duplicate slug",
    "invalid_depth_mismatch.csv": "dots but depth",
    "invalid_missing_parent.csv": "missing parent",
    "invalid_uci.csv": "invalid UCI move",
    "invalid_class_root.csv": "does not match format",
    "invalid_check_in_slug.csv": "does not match format",
    "invalid_attribution_no_source.csv": "without 'attribution_source'",
}


def run_validator(fixture: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VALIDATE), str(fixture)],
        capture_output=True,
        text=True,
        check=False,
    )


class ValidatorTests(unittest.TestCase):
    def test_canonical_catalogue_validates(self) -> None:
        """The shipped catalogue must always validate clean."""
        catalogue = REPO_ROOT / "catalog" / "ocn-1.csv"
        self.assertTrue(catalogue.exists(), f"missing {catalogue}")
        result = run_validator(catalogue)
        self.assertEqual(
            result.returncode,
            0,
            f"canonical catalogue failed: stderr={result.stderr!r}",
        )
        self.assertIn("OK:", result.stdout)

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
        for fixture_name, expected in EXPECTED_INVALID.items():
            fixture = FIXTURES / fixture_name
            with self.subTest(fixture=fixture_name):
                self.assertTrue(
                    fixture.exists(), f"missing fixture {fixture_name}"
                )
                result = run_validator(fixture)
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


if __name__ == "__main__":
    unittest.main()
