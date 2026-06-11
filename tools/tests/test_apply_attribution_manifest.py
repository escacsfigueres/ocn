"""Tests for tools/apply_attribution_manifest.py.

The Attribution Batch Engine turns evidence-backed batches into validatable,
safely-applicable manifests. These tests pin down its safety contract:

- only mode-allowed fields may change (whitelist per mode);
- the set of rows that actually change must equal expected_changed_rows;
- untouched rows are byte-identical (raw-line preservation);
- attributed_to always travels with attribution_source;
- dry-run (the default) never writes the catalogue or --out.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TOOLS = REPO_ROOT / "tools"
TOOL = TOOLS / "apply_attribution_manifest.py"
CATALOG = REPO_ROOT / "catalog" / "ocn-1.csv"
FIXTURES = Path(__file__).resolve().parent / "fixtures"
BASE = FIXTURES / "apply_manifest_base.csv"
EXAMPLE_MANIFEST = REPO_ROOT / "docs" / "examples" / "attribution-manifest.example.json"

sys.path.insert(0, str(TOOLS))
import apply_attribution_manifest as abm  # noqa: E402


def base_manifest(**over) -> dict:
    """A valid attribution_fields_only manifest against the 5-row fixture."""
    manifest = {
        "kind": "ocn.attribution_manifest.v1",
        "title": "Test batch",
        "mode": "attribution_fields_only",
        "expected_catalog_rows": 5,
        "expected_changed_rows": ["B.Fre.Win"],
        "changes": [
            {
                "ocn1": "B.Fre.Win",
                "evidence_grade": "CLEAR",
                "source_refs": ["Test source, p.1"],
                "fields": {
                    "attributed_to": "Szymon Winawer",
                    "attribution_source": "Oxford Companion to Chess",
                    "historical_notes": "Introduced 5...a6 lines.",
                },
            }
        ],
    }
    manifest.update(over)
    return manifest


def write_json(directory: Path, obj: dict, name: str = "manifest.json") -> Path:
    path = Path(directory) / name
    path.write_text(json.dumps(obj, ensure_ascii=False), encoding="utf-8")
    return path


def plan(manifest: dict, *, catalog: Path = BASE, strict: bool = False):
    """Write `manifest` to a temp file and run the engine's planning path."""
    with tempfile.TemporaryDirectory() as d:
        mpath = write_json(Path(d), manifest)
        return abm.plan(mpath, catalog, strict=strict)


def run_tool(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(TOOL), *args],
        capture_output=True,
        text=True,
        check=False,
    )


class ManifestStructureTests(unittest.TestCase):
    def test_valid_manifest_changes_only_attribution_fields(self) -> None:
        result = plan(base_manifest())
        self.assertEqual([c["ocn1"] for c in result.changed], ["B.Fre.Win"])
        diffs = result.changed[0]["diffs"]
        self.assertEqual(
            set(diffs),
            {"attributed_to", "attribution_source", "historical_notes"},
        )

    def test_unknown_kind_rejected(self) -> None:
        with self.assertRaises(abm.ApplyError):
            plan(base_manifest(kind="ocn.attribution_manifest.v2"))

    def test_unknown_top_level_key_rejected(self) -> None:
        with self.assertRaises(abm.ApplyError):
            plan(base_manifest(unexpected_key="boom"))

    def test_unknown_mode_rejected(self) -> None:
        with self.assertRaises(abm.ApplyError):
            plan(base_manifest(mode="attribution_fields_only_typo"))

    def test_forbidden_field_rejected(self) -> None:
        m = base_manifest()
        m["changes"][0]["fields"] = {"moves_uci": "e2e4"}
        with self.assertRaises(abm.ApplyError):
            plan(m)

    def test_empty_fields_dict_rejected(self) -> None:
        m = base_manifest()
        m["changes"][0]["fields"] = {}
        with self.assertRaises(abm.ApplyError):
            plan(m)

    def test_duplicate_slug_rejected(self) -> None:
        m = base_manifest()
        m["changes"].append(dict(m["changes"][0]))
        with self.assertRaises(abm.ApplyError):
            plan(m)


class CatalogConsistencyTests(unittest.TestCase):
    def test_unknown_slug_rejected(self) -> None:
        m = base_manifest(expected_changed_rows=["Z.Nope"])
        m["changes"][0]["ocn1"] = "Z.Nope"
        with self.assertRaises(abm.ApplyError):
            plan(m)

    def test_expected_catalog_rows_mismatch_rejected(self) -> None:
        with self.assertRaises(abm.ApplyError):
            plan(base_manifest(expected_catalog_rows=999))

    def test_expected_changed_rows_mismatch_rejected(self) -> None:
        # Manifest changes B.Fre.Win but claims it will change A.Tro.
        with self.assertRaises(abm.ApplyError):
            plan(base_manifest(expected_changed_rows=["A.Tro"]))

    def test_noop_change_rejected(self) -> None:
        # Re-applying A.Tro's existing values changes nothing -> mismatch.
        m = base_manifest(expected_changed_rows=["A.Tro"])
        m["changes"][0] = {
            "ocn1": "A.Tro",
            "evidence_grade": "CLEAR",
            "source_refs": ["Oxford Companion to Chess"],
            "fields": {
                "attributed_to": "Octávio Trompowsky",
                "attribution_source": "Oxford Companion to Chess",
                "historical_notes": "Named for the Brazilian player.",
            },
        }
        with self.assertRaises(abm.ApplyError):
            plan(m)


class FieldInvariantTests(unittest.TestCase):
    def test_attributed_to_without_source_rejected(self) -> None:
        m = base_manifest(expected_changed_rows=["B.Fre"])
        m["changes"][0] = {
            "ocn1": "B.Fre",
            "evidence_grade": "CLEAR",
            "source_refs": ["Test"],
            "fields": {"attributed_to": "Somebody"},
        }
        with self.assertRaises(abm.ApplyError):
            plan(m)

    def test_strict_rejects_non_clear_grade(self) -> None:
        m = base_manifest()
        m["changes"][0]["evidence_grade"] = "PARTIAL"
        with self.assertRaises(abm.ApplyError):
            plan(m, strict=True)
        # Same manifest with CLEAR passes under --strict.
        self.assertEqual(len(plan(base_manifest(), strict=True).changed), 1)


class NamingModeTests(unittest.TestCase):
    def test_naming_mode_allows_name_alias_notes(self) -> None:
        m = base_manifest(mode="naming_strings_only", expected_changed_rows=["B.Fre"])
        m["changes"][0] = {
            "ocn1": "B.Fre",
            "evidence_grade": "CLEAR",
            "source_refs": ["Test"],
            "fields": {
                "canonical_name": "French Defence (revised)",
                "aliases": "French",
                "notes": "Updated note.",
            },
        }
        result = plan(m)
        self.assertEqual(
            set(result.changed[0]["diffs"]),
            {"canonical_name", "aliases", "notes"},
        )

    def test_naming_mode_rejects_moves_uci(self) -> None:
        m = base_manifest(mode="naming_strings_only")
        m["changes"][0]["fields"] = {"moves_uci": "e2e4"}
        with self.assertRaises(abm.ApplyError):
            plan(m)

    def test_naming_mode_rejects_same_as(self) -> None:
        m = base_manifest(mode="naming_strings_only")
        m["changes"][0]["fields"] = {"same_as": "A.Tro"}
        with self.assertRaises(abm.ApplyError):
            plan(m)


class PreservationTests(unittest.TestCase):
    def test_untouched_rows_are_byte_identical(self) -> None:
        result = plan(base_manifest())
        original = BASE.read_text(encoding="utf-8").splitlines()
        produced = result.output_text.splitlines()
        # Header + rows A, A.Tro, B, B.Fre are untouched; only B.Fre.Win changes.
        self.assertEqual(produced[:5], original[:5])
        # The deliberately over-quoted A.Tro notes survives verbatim.
        self.assertIn('"Quiet system."', produced[2])

    def test_row_count_preserved(self) -> None:
        result = plan(base_manifest())
        self.assertEqual(result.input_rows, 5)
        self.assertEqual(result.output_rows, 5)

    def test_sha_changes_only_when_content_changes(self) -> None:
        result = plan(base_manifest())
        self.assertNotEqual(result.sha_before, result.sha_after)


class ReportTests(unittest.TestCase):
    def test_json_report_shape(self) -> None:
        result = plan(base_manifest())
        payload = json.loads(abm.render_report(result, fmt="json"))
        for key in ("kind", "title", "mode", "input_rows", "output_rows",
                    "sha_before", "sha_after", "changed"):
            self.assertIn(key, payload)
        self.assertEqual(payload["changed"][0]["ocn1"], "B.Fre.Win")

    def test_markdown_report_mentions_slug_and_mode(self) -> None:
        result = plan(base_manifest())
        md = abm.render_report(result, fmt="markdown")
        self.assertIn("B.Fre.Win", md)
        self.assertIn("attribution_fields_only", md)


class CLITests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)

    def test_dry_run_is_default_and_writes_nothing(self) -> None:
        mpath = write_json(self.tmp, base_manifest())
        out = self.tmp / "should_not_exist.csv"
        before = hashlib.sha256(BASE.read_bytes()).hexdigest()
        result = run_tool("--manifest", str(mpath), "--catalog", str(BASE),
                          "--out", str(out))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(out.exists(), "dry-run must not write --out")
        self.assertEqual(hashlib.sha256(BASE.read_bytes()).hexdigest(), before)

    def test_apply_requires_out(self) -> None:
        mpath = write_json(self.tmp, base_manifest())
        result = run_tool("--manifest", str(mpath), "--catalog", str(BASE),
                          "--apply")
        self.assertEqual(result.returncode, 2, result.stderr)

    def test_apply_writes_out_and_leaves_catalog_untouched(self) -> None:
        mpath = write_json(self.tmp, base_manifest())
        out = self.tmp / "out.csv"
        before = hashlib.sha256(BASE.read_bytes()).hexdigest()
        result = run_tool("--manifest", str(mpath), "--catalog", str(BASE),
                          "--apply", "--out", str(out))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(out.exists())
        self.assertIn("Szymon Winawer", out.read_text(encoding="utf-8"))
        self.assertEqual(hashlib.sha256(BASE.read_bytes()).hexdigest(), before)

    def test_forbidden_field_exits_one_with_error(self) -> None:
        m = base_manifest()
        m["changes"][0]["fields"] = {"moves_uci": "e2e4"}
        mpath = write_json(self.tmp, m)
        result = run_tool("--manifest", str(mpath), "--catalog", str(BASE))
        self.assertEqual(result.returncode, 1)
        self.assertIn("ERROR", result.stderr)


class ExampleManifestTests(unittest.TestCase):
    """The shipped example must work against the real catalogue (spec command)."""

    def setUp(self) -> None:
        if not EXAMPLE_MANIFEST.exists():
            self.skipTest("example manifest not present yet")

    def test_example_dry_run_against_real_catalog_succeeds(self) -> None:
        result = run_tool("--manifest", str(EXAMPLE_MANIFEST),
                          "--catalog", str(CATALOG), "--report", "markdown")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_example_apply_leaves_real_catalog_untouched(self) -> None:
        before = hashlib.sha256(CATALOG.read_bytes()).hexdigest()
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "out.csv"
            result = run_tool("--manifest", str(EXAMPLE_MANIFEST),
                              "--catalog", str(CATALOG), "--apply",
                              "--out", str(out))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(out.exists())
        self.assertEqual(hashlib.sha256(CATALOG.read_bytes()).hexdigest(), before)


class FormatAliasTests(unittest.TestCase):
    """--format is an alias of --report (CLI harmonization with other tools)."""

    def test_format_flag_works_as_report_alias(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            mpath = write_json(Path(d), base_manifest())
            result = run_tool("--manifest", str(mpath), "--catalog", str(BASE),
                              "--format", "json")
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["mode"], "attribution_fields_only")


if __name__ == "__main__":
    unittest.main()
