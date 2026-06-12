"""Tests for tools/verify_doc_slugs.py.

Verifies backtick-quoted OCN slugs in docs against the catalogue, without
false-positiving on hashes, ECO codes, versions, flags, filenames, or
field-accessor notation, and honouring a NON-CATALOGUE / pseudo-slug exemption
(with a 2-line lookback).
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TOOLS = REPO_ROOT / "tools"
TOOL = TOOLS / "verify_doc_slugs.py"
FIXTURES = Path(__file__).resolve().parent / "fixtures"
BASE = FIXTURES / "apply_manifest_base.csv"  # slugs: A, A.Tro, B, B.Fre, B.Fre.Win


class VerifyDocSlugsTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)

    def doc(self, text: str, name: str = "d.md") -> Path:
        p = self.tmp / name
        p.write_text(text, encoding="utf-8")
        return p

    def run_tool(self, *paths_and_args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(TOOL), "--catalog", str(BASE), *paths_and_args],
            capture_output=True, text=True, check=False)

    def test_existing_slug_passes(self) -> None:
        d = self.doc("The `A.Tro` head is attributed.\n")
        r = self.run_tool(str(d))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_missing_slug_fails_with_file_line(self) -> None:
        d = self.doc("line one\nsee `A.Zzz` here\n")
        r = self.run_tool(str(d))
        self.assertEqual(r.returncode, 1)
        out = r.stdout + r.stderr
        self.assertIn("A.Zzz", out)
        self.assertIn(":2", out)  # reported on line 2

    def test_noncatalogue_same_line_exempt(self) -> None:
        d = self.doc("NON-CATALOGUE pseudo-slug `A.Zzz` for illustration.\n")
        self.assertEqual(self.run_tool(str(d)).returncode, 0)

    def test_noncatalogue_preceding_line_exempt(self) -> None:
        d = self.doc("The following is NON-CATALOGUE:\n`A.Zzz`\n")
        self.assertEqual(self.run_tool(str(d)).returncode, 0)

    def test_code_tokens_not_flagged(self) -> None:
        d = self.doc("ECO `A45`, hash `204eb07`, version `ocn-1.1.0`, flag "
                     "`--strict`, file `ocn-1.csv`, cmd `git push`.\n")
        self.assertEqual(self.run_tool(str(d)).returncode, 0)

    def test_field_accessor_not_flagged(self) -> None:
        d = self.doc("Set `A.Tro.notes` and `A.Tro.attributed_to` in review.\n")
        self.assertEqual(self.run_tool(str(d)).returncode, 0)

    def test_two_slugs_one_line_each_checked(self) -> None:
        d = self.doc("compare `A.Tro` and `A.Zzz` directly\n")
        r = self.run_tool(str(d))
        self.assertEqual(r.returncode, 1)
        self.assertIn("A.Zzz", r.stdout + r.stderr)

    def test_zero_files_is_error_not_silent_pass(self) -> None:
        r = self.run_tool(str(self.tmp / "does_not_exist_*.md"))
        self.assertEqual(r.returncode, 1)

    def test_json_format(self) -> None:
        d = self.doc("bad `A.Zzz`\n")
        r = self.run_tool("--format", "json", str(d))
        self.assertEqual(r.returncode, 1)
        payload = json.loads(r.stdout)
        self.assertEqual(payload[0]["slug"], "A.Zzz")
        self.assertEqual(payload[0]["line"], 1)
        self.assertIn("d.md", payload[0]["file"])

    def test_clean_doc_with_no_backticks(self) -> None:
        d = self.doc("Just prose, no code spans here.\n")
        self.assertEqual(self.run_tool(str(d)).returncode, 0)


class LiveDocsGateTests(unittest.TestCase):
    def test_live_docs_have_no_stale_slugs(self) -> None:
        """Every backticked slug in live documentation (README, spec,
        docs/*.md top level) must exist in the live catalogue.
        Era-closed working documents live in docs/archive/, exempt by
        location; intentional historical slugs in live records carry
        the NON-CATALOGUE marker within two lines."""
        paths = [
            str(REPO_ROOT / "README.md"),
            str(REPO_ROOT / "spec" / "OCN-1.md"),
        ]
        paths += sorted(str(p) for p in (REPO_ROOT / "docs").glob("*.md"))
        result = subprocess.run(
            [sys.executable, str(TOOL), *paths],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(
            result.returncode,
            0,
            "stale slugs in live docs:\n" + result.stdout + result.stderr,
        )


if __name__ == "__main__":
    unittest.main()
