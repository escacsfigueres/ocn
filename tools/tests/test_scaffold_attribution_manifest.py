"""Tests for tools/scaffold_attribution_manifest.py.

Builds an ocn.attribution_manifest.v1 SKELETON from reviewed slugs. The skeleton
is structurally valid (the apply engine's validate_manifest accepts it) but is
intentionally NOT apply-ready: its field values are empty strings, so the engine
rejects it as a no-op in dry-run until a human fills real values.
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
TOOL = TOOLS / "scaffold_attribution_manifest.py"
FIXTURES = Path(__file__).resolve().parent / "fixtures"
BASE = FIXTURES / "apply_manifest_base.csv"  # 5 rows; A.Tro is attributed

sys.path.insert(0, str(TOOLS))
import apply_attribution_manifest as abm  # noqa: E402


def run_tool(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, str(TOOL), "--catalog", str(BASE), *args],
                          capture_output=True, text=True, check=False)


def scaffold(tmp: Path, *args: str) -> tuple[subprocess.CompletedProcess[str], Path]:
    out = tmp / "manifest.json"
    proc = run_tool("--out", str(out), *args)
    return proc, out


class ScaffoldTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)

    def test_attribution_mode_skeleton_shape(self) -> None:
        proc, out = scaffold(self.tmp, "--title", "T", "--mode", "attribution_fields_only",
                             "--ocn1", "B.Fre.Win")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        m = json.loads(out.read_text(encoding="utf-8"))
        self.assertEqual(m["kind"], "ocn.attribution_manifest.v1")
        self.assertEqual(m["expected_catalog_rows"], 5)
        self.assertEqual(m["expected_changed_rows"], ["B.Fre.Win"])
        self.assertEqual(
            set(m["changes"][0]["fields"]),
            {"attributed_to", "attribution_source", "historical_notes"},
        )
        self.assertTrue(all(v == "" for v in m["changes"][0]["fields"].values()))

    def test_naming_mode_skeleton_has_six_fields(self) -> None:
        proc, out = scaffold(self.tmp, "--title", "T", "--mode", "naming_strings_only",
                             "--ocn1", "B.Fre")
        m = json.loads(out.read_text(encoding="utf-8"))
        self.assertEqual(
            set(m["changes"][0]["fields"]),
            {"canonical_name", "aliases", "notes",
             "attributed_to", "attribution_source", "historical_notes"},
        )

    def test_skeleton_is_structurally_valid_for_the_engine(self) -> None:
        _, out = scaffold(self.tmp, "--title", "T", "--mode", "attribution_fields_only",
                          "--ocn1", "B.Fre.Win")
        # validate_manifest is the engine's structural gate — must NOT raise.
        abm.validate_manifest(json.loads(out.read_text(encoding="utf-8")))

    def test_raw_skeleton_is_rejected_by_dry_run_as_noop(self) -> None:
        _, out = scaffold(self.tmp, "--title", "T", "--mode", "attribution_fields_only",
                          "--ocn1", "B.Fre.Win")
        with self.assertRaises(abm.ApplyError):
            abm.plan(out, BASE)

    def test_filled_skeleton_is_accepted_by_dry_run(self) -> None:
        _, out = scaffold(self.tmp, "--title", "T", "--mode", "attribution_fields_only",
                          "--ocn1", "B.Fre.Win")
        m = json.loads(out.read_text(encoding="utf-8"))
        m["changes"][0]["fields"] = {
            "attributed_to": "Szymon Winawer",
            "attribution_source": "Test source",
            "historical_notes": "Filled.",
        }
        filled = self.tmp / "filled.json"
        filled.write_text(json.dumps(m), encoding="utf-8")
        result = abm.plan(filled, BASE)
        self.assertEqual([c["ocn1"] for c in result.changed], ["B.Fre.Win"])

    def test_expected_changed_rows_in_catalogue_order(self) -> None:
        _, out = scaffold(self.tmp, "--title", "T", "--mode", "attribution_fields_only",
                          "--ocn1", "B.Fre.Win", "--ocn1", "A.Tro", "--ocn1", "B.Fre",
                          "--allow-attributed")
        m = json.loads(out.read_text(encoding="utf-8"))
        self.assertEqual(m["expected_changed_rows"], ["A.Tro", "B.Fre", "B.Fre.Win"])

    def test_source_refs_and_grade_propagate(self) -> None:
        _, out = scaffold(self.tmp, "--title", "T", "--mode", "attribution_fields_only",
                          "--ocn1", "B.Fre.Win", "--evidence-grade", "PARTIAL",
                          "--source-ref", "Ref A", "--source-ref", "Ref B")
        c = json.loads(out.read_text(encoding="utf-8"))["changes"][0]
        self.assertEqual(c["evidence_grade"], "PARTIAL")
        self.assertEqual(c["source_refs"], ["Ref A", "Ref B"])

    def test_duplicate_slug_rejected(self) -> None:
        proc, _ = scaffold(self.tmp, "--title", "T", "--mode", "attribution_fields_only",
                           "--ocn1", "B.Fre", "--ocn1", "B.Fre")
        self.assertEqual(proc.returncode, 1)
        self.assertIn("ERROR", proc.stderr)

    def test_missing_slug_rejected(self) -> None:
        proc, _ = scaffold(self.tmp, "--title", "T", "--mode", "attribution_fields_only",
                           "--ocn1", "Z.Nope")
        self.assertEqual(proc.returncode, 1)
        self.assertIn("ERROR", proc.stderr)

    def test_invalid_mode_is_usage_error(self) -> None:
        proc, _ = scaffold(self.tmp, "--title", "T", "--mode", "bogus_mode",
                           "--ocn1", "B.Fre")
        self.assertEqual(proc.returncode, 2)

    def test_invalid_evidence_grade_is_usage_error(self) -> None:
        proc, _ = scaffold(self.tmp, "--title", "T", "--mode", "attribution_fields_only",
                           "--ocn1", "B.Fre", "--evidence-grade", "UNKNOWN")
        self.assertEqual(proc.returncode, 2)

    def test_already_attributed_slug_warns(self) -> None:
        # A.Tro is attributed; an empty-field skeleton would CLEAR it on apply.
        proc, _ = scaffold(self.tmp, "--title", "T", "--mode", "attribution_fields_only",
                           "--ocn1", "A.Tro", "--allow-attributed")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("WARN", proc.stderr)
        self.assertIn("A.Tro", proc.stderr)

    def test_already_attributed_slug_rejected_without_override(self) -> None:
        proc, _ = scaffold(self.tmp, "--title", "T", "--mode", "attribution_fields_only",
                           "--ocn1", "A.Tro")
        self.assertEqual(proc.returncode, 1)
        self.assertIn("A.Tro", proc.stderr)


if __name__ == "__main__":
    unittest.main()
