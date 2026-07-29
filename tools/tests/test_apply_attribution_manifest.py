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


class EcoModeTests(unittest.TestCase):
    """eco_legacy_only — the third safety mode (audit P1 item 8). ECO
    corrections travel alone: no naming or attribution field may ride
    along, and the other two modes keep rejecting eco_legacy."""

    def eco_manifest(self, **over) -> dict:
        manifest = base_manifest(
            mode="eco_legacy_only",
            expected_changed_rows=["A.Tro"],
            changes=[
                {
                    "ocn1": "A.Tro",
                    "evidence_grade": "CLEAR",
                    "source_refs": ["Test ECO source."],
                    "fields": {"eco_legacy": "D00"},
                }
            ],
        )
        manifest.update(over)
        return manifest

    def test_eco_mode_allows_eco_legacy_change(self) -> None:
        result = plan(self.eco_manifest())
        self.assertEqual([c["ocn1"] for c in result.changed], ["A.Tro"])
        self.assertEqual(
            result.changed[0]["diffs"]["eco_legacy"], ["A45", "D00"]
        )

    def test_eco_mode_rejects_naming_fields(self) -> None:
        manifest = self.eco_manifest()
        manifest["changes"][0]["fields"]["canonical_name"] = "Trompowsky"
        with self.assertRaises(abm.ApplyError) as ctx:
            plan(manifest)
        self.assertIn("not permitted", str(ctx.exception))

    def test_attribution_mode_still_rejects_eco_legacy(self) -> None:
        manifest = base_manifest()
        manifest["changes"][0]["fields"] = {"eco_legacy": "C19"}
        with self.assertRaises(abm.ApplyError) as ctx:
            plan(manifest)
        self.assertIn("not permitted", str(ctx.exception))


class AliasesOnlyModeTests(unittest.TestCase):
    """aliases_only — the fourth safety mode (roadmap H2.6). The editorial
    alias passes touch thousands of rows, so "aliases and nothing else"
    has to be a property the engine checks, not a promise in the
    manifest's description. Same guardrails as every other mode:
    field-scope, exact expected_changed_rows, zero collateral diff."""

    def alias_manifest(self, **over) -> dict:
        manifest = base_manifest(
            mode="aliases_only",
            expected_changed_rows=["B.Fre"],
            changes=[
                {
                    "ocn1": "B.Fre",
                    "evidence_grade": "EDITORIAL",
                    "source_refs": ["Test editorial rule."],
                    "fields": {"aliases": "French"},
                }
            ],
        )
        manifest.update(over)
        return manifest

    # --- happy path -------------------------------------------------- #
    def test_alias_mode_allows_alias_change(self) -> None:
        result = plan(self.alias_manifest())
        self.assertEqual([c["ocn1"] for c in result.changed], ["B.Fre"])
        self.assertEqual(set(result.changed[0]["diffs"]), {"aliases"})

    def test_alias_mode_allows_clearing_the_cell(self) -> None:
        """The synthetic-deletion lot empties 1,648 alias cells; an empty
        string is a legitimate new value, not a missing field."""
        m = self.alias_manifest(expected_changed_rows=["A.Tro"])
        m["changes"] = [
            {
                "ocn1": "A.Tro",
                "evidence_grade": "EDITORIAL",
                "source_refs": ["Test editorial rule."],
                "fields": {"aliases": ""},
            }
        ]
        result = plan(m)
        self.assertEqual(result.changed[0]["diffs"]["aliases"][1], "")

    def test_alias_mode_does_not_disturb_other_columns(self) -> None:
        result = plan(self.alias_manifest())
        original = BASE.read_text(encoding="utf-8").splitlines()
        produced = result.output_text.splitlines()
        self.assertEqual(len(produced), len(original))
        # Every line except B.Fre's is byte-identical to the source.
        changed_lines = [
            i for i, (a, b) in enumerate(zip(original, produced)) if a != b
        ]
        self.assertEqual(len(changed_lines), 1)
        self.assertTrue(produced[changed_lines[0]].startswith("B.Fre,"))

    # --- field-scope violations -------------------------------------- #
    def test_alias_mode_rejects_canonical_name(self) -> None:
        m = self.alias_manifest()
        m["changes"][0]["fields"]["canonical_name"] = "French"
        with self.assertRaises(abm.ApplyError) as ctx:
            plan(m)
        self.assertIn("not permitted", str(ctx.exception))

    def test_alias_mode_rejects_notes(self) -> None:
        m = self.alias_manifest()
        m["changes"][0]["fields"]["notes"] = "Rewritten."
        with self.assertRaises(abm.ApplyError) as ctx:
            plan(m)
        self.assertIn("not permitted", str(ctx.exception))

    def test_alias_mode_rejects_attribution_fields(self) -> None:
        m = self.alias_manifest()
        m["changes"][0]["fields"]["attributed_to"] = "Somebody"
        with self.assertRaises(abm.ApplyError) as ctx:
            plan(m)
        self.assertIn("not permitted", str(ctx.exception))

    def test_alias_mode_rejects_structural_columns(self) -> None:
        for column, value in (("moves_uci", "e2e4"), ("same_as", "A.Tro"),
                              ("eco_legacy", "C00")):
            with self.subTest(column=column):
                m = self.alias_manifest()
                m["changes"][0]["fields"] = {column: value}
                with self.assertRaises(abm.ApplyError):
                    plan(m)

    # --- collateral-diff / exact-change refusals --------------------- #
    def test_alias_mode_rejects_unexpected_changed_row(self) -> None:
        """A row that would really change but is absent from
        expected_changed_rows is collateral damage. On a lot this size the
        realistic slip is an extra `changes` entry nobody re-counted, so
        the refusal has to name the slug — it does."""
        m = self.alias_manifest()
        m["changes"].append(
            {
                "ocn1": "A.Tro",
                "evidence_grade": "EDITORIAL",
                "source_refs": ["Test editorial rule."],
                "fields": {"aliases": "Trompowsky"},
            }
        )
        with self.assertRaises(abm.ApplyError) as ctx:
            plan(m)
        message = str(ctx.exception)
        self.assertIn("A.Tro", message)
        self.assertIn("not expected_changed_rows", message)
        # And the mirror slip: a slug promised in expected_changed_rows
        # with no corresponding change entry.
        m2 = self.alias_manifest(expected_changed_rows=["B.Fre", "A.Tro"])
        with self.assertRaises(abm.ApplyError) as ctx2:
            plan(m2)
        self.assertIn("A.Tro", str(ctx2.exception))

    def test_alias_mode_rejects_noop_row(self) -> None:
        """Re-writing a cell with its current value changes nothing, so
        the lot is stale or already applied — refuse rather than no-op."""
        m = self.alias_manifest(expected_changed_rows=["A.Tro"])
        m["changes"] = [
            {
                "ocn1": "A.Tro",
                "evidence_grade": "EDITORIAL",
                "source_refs": ["Test editorial rule."],
                "fields": {"aliases": "Ruth Opening"},
            }
        ]
        with self.assertRaises(abm.ApplyError) as ctx:
            plan(m)
        self.assertIn("no-op", str(ctx.exception))

    def test_alias_mode_rejects_stale_row_count(self) -> None:
        with self.assertRaises(abm.ApplyError):
            plan(self.alias_manifest(expected_catalog_rows=5899))

    # --- interaction with the other modes ---------------------------- #
    def test_eco_mode_still_rejects_aliases(self) -> None:
        m = base_manifest(mode="eco_legacy_only")
        m["changes"][0]["fields"] = {"aliases": "French"}
        with self.assertRaises(abm.ApplyError) as ctx:
            plan(m)
        self.assertIn("not permitted", str(ctx.exception))

    def test_alias_mode_is_registered(self) -> None:
        self.assertEqual(
            abm.MODE_ALLOWED_FIELDS["aliases_only"], frozenset({"aliases"})
        )

    # --- CLI: dry-run default still holds ---------------------------- #
    def test_alias_mode_dry_run_writes_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            mpath = write_json(Path(d), self.alias_manifest())
            out = Path(d) / "should_not_exist.csv"
            before = hashlib.sha256(BASE.read_bytes()).hexdigest()
            result = run_tool("--manifest", str(mpath), "--catalog", str(BASE),
                              "--out", str(out))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(out.exists())
            self.assertEqual(hashlib.sha256(BASE.read_bytes()).hexdigest(), before)
            self.assertIn("aliases_only", result.stdout)


class SyntheticAliasDeletionManifestTests(unittest.TestCase):
    """The H2.6 deletion lot itself: it must stay in aliases_only mode and
    dry-run clean against the live catalogue for as long as it is
    unapplied. Skipped once the lot lands (it then becomes a no-op)."""

    MANIFEST = (REPO_ROOT / "docs" / "manifests"
                / "synthetic-alias-deletion.manifest.json")

    def setUp(self) -> None:
        if not self.MANIFEST.exists():
            self.skipTest("synthetic-alias deletion manifest not present")

    def test_manifest_is_aliases_only(self) -> None:
        payload = json.loads(self.MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(payload["mode"], "aliases_only")
        touched = {k for c in payload["changes"] for k in c["fields"]}
        self.assertEqual(touched, {"aliases"})

    def test_manifest_dry_run_leaves_catalog_untouched(self) -> None:
        before = hashlib.sha256(CATALOG.read_bytes()).hexdigest()
        result = run_tool("--manifest", str(self.MANIFEST),
                          "--catalog", str(CATALOG), "--report", "json")
        if result.returncode != 0 and "already applied" in result.stderr:
            self.skipTest("lot has been applied; manifest is now a no-op")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["input_rows"], payload["output_rows"])
        self.assertEqual(hashlib.sha256(CATALOG.read_bytes()).hexdigest(), before)


if __name__ == "__main__":
    unittest.main()
