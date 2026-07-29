"""Tests for tools/attribution_metadata.py.

The attribution-metadata sidecar recovers the *richer* attribution data that
the apply engine strips at write time. The applied CSV keeps only
``attributed_to`` + ``attribution_source``; the committed
``ocn.attribution_manifest.v1`` manifests (mode ``attribution_fields_only``)
additionally carry a structured ``evidence_grade`` and a parenthetical ROLE
inside ``attributed_to`` (the methodology's type-A..I qualifier). This tool
joins the catalogue's ATTRIBUTED rows back to the manifest that set them and
lifts role / evidence_grade / type, recording WHICH manifest.

Honesty contract exercised here:

  * the join key is the catalogue's attributed rows (both fields non-empty);
    the sidecar covers EXACTLY those rows — no more, no fewer.
  * ``attributed_to`` / ``attribution_source`` in the sidecar EQUAL the live
    catalogue values; if a manifest disagrees with the applied CSV, the CSV
    wins and the row is flagged (the manifest is never silently trusted).
  * a manifest contributes role/grade ONLY when its ``attributed_to`` matches
    the catalogue's; a row with no matching manifest is ``unknown`` (the tool
    never guesses a role, grade, or type).

These tests build small CSV + manifest fixtures so they do not depend on the
live data, plus a drift test pinning the committed sidecar to a fresh rebuild.
"""
from __future__ import annotations

import csv
import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TOOL = REPO_ROOT / "tools" / "attribution_metadata.py"
sys.path.insert(0, str(REPO_ROOT / "tools"))

CATALOG_HEADER = (
    "ocn1,canonical_name,eco_legacy,parent_ocn1,moves_uci,depth,aliases,"
    "flags,notes,attributed_to,attribution_source,historical_notes,"
    "transposes_to,same_as"
)

# Catalogue fixture. Rows chosen to exercise every branch:
#   A                       class root, not attributed              -> excluded
#   A.Ret                   attributed + matching manifest (CLEAR)  -> role/grade lifted
#   A.Gro                   attributed + matching manifest (CLEAR)  -> role/grade lifted
#   B.Old                   attributed, NO manifest (pre-engine)    -> unknown
#   B.Half                  half-filled (source missing)            -> NOT attributed -> excluded
#   B.Conf                  attributed + manifest DISAGREES on attr -> CSV wins, flagged, unknown
CATALOG_ROWS = [
    "A,Flank Openings,,,,0,,,Top-level class.,,,,,",
    "A.Ret,Réti Opening,A04,A,g1f3,1,Zukertort,,1.Nf3.,Richard Réti (popularizer),"
    '"Wikipedia, Réti Opening",Named for Réti.,,',
    "A.Gro,Grob's Attack,A00,A,g2g4,1,,,1.g4.,Henri Grob (analyst and popularizer),"
    '"Wikipedia, Grob",Named for Grob.,,',
    "B.Old,Old Defense,B00,B,e2e4,1,,,pre-engine.,Some Master (popularizer),"
    '"A book, ch.3",Older attribution.,,',
    "B.Half,Half Filled,B01,B,e2e4 d7d5,2,,,half.,Only A Name,,,,",
    "B.Conf,Conflict Line,B02,B,e2e4 e7e5,2,,,conflict.,CSV Authority (advocate),"
    '"CSV source wins",csv note.,,',
]


def attribution_manifest(title, changes):
    return {
        "kind": "ocn.attribution_manifest.v1",
        "title": title,
        "mode": "attribution_fields_only",
        "expected_catalog_rows": 6,
        "expected_changed_rows": [c["ocn1"] for c in changes],
        "changes": changes,
    }


def change(ocn1, attributed_to, grade="CLEAR", source="manifest source"):
    return {
        "ocn1": ocn1,
        "evidence_grade": grade,
        "source_refs": ["ref-1"],
        "fields": {
            "attributed_to": attributed_to,
            "attribution_source": source,
            "historical_notes": "notes",
        },
    }


# A non-attribution manifest (diacritic mode) that must be IGNORED even though
# it touches one of the attributed slugs.
NON_ATTR_MANIFEST = {
    "kind": "ocn.naming_manifest.v1",
    "title": "diacritics — not attribution data",
    "mode": "diacritic_normalization",
    "changes": [{"ocn1": "A.Ret", "fields": {"canonical_name": "Réti Opening"}}],
}


def write_catalog(path, rows=None):
    body = CATALOG_ROWS if rows is None else rows
    path.write_text("\n".join([CATALOG_HEADER, *body]) + "\n", encoding="utf-8")


def rows_from_tsv(text):
    return list(csv.DictReader(io.StringIO(text), delimiter="\t"))


class AttributionMetadataTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)
        self.catalog = self.tmp / "cat.csv"
        write_catalog(self.catalog)
        self.manifests = self.tmp / "manifests"
        self.manifests.mkdir()
        # lot manifest: covers A.Ret and A.Gro with matching attributed_to.
        self._write_manifest("lot-eponyms.manifest.json", attribution_manifest(
            "Lot eponyms",
            [
                change("A.Ret", "Richard Réti (popularizer)"),
                change("A.Gro", "Henri Grob (analyst and popularizer)"),
            ],
        ))
        # conflict manifest: B.Conf attributed_to disagrees with the CSV.
        self._write_manifest("conflict.manifest.json", attribution_manifest(
            "Conflict",
            [change("B.Conf", "Manifest Disagrees (inventor)", grade="PARTIAL")],
        ))
        # non-attribution manifest that touches A.Ret — must be ignored.
        self._write_manifest("diacritics.manifest.json", NON_ATTR_MANIFEST)

    def _write_manifest(self, name, payload):
        (self.manifests / name).write_text(
            json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    def run_tool(self, *args, catalog=None):
        cat = str(catalog or self.catalog)
        return subprocess.run(
            [sys.executable, str(TOOL), "--catalog", cat,
             "--manifests", str(self.manifests), *args],
            capture_output=True, text=True, check=False)

    def index(self, rows):
        return {r["ocn1"]: r for r in rows}

    # --- schema / coverage ---------------------------------------------
    def test_output_schema_columns(self):
        r = self.run_tool()
        self.assertEqual(r.returncode, 0, r.stderr)
        rows = rows_from_tsv(r.stdout)
        self.assertEqual(list(rows[0].keys()), [
            "ocn1", "attributed_to", "attribution_source", "role",
            "evidence_grade", "attribution_type", "source_manifest",
            "manifest_conflict",
        ])

    def test_covers_exactly_the_attributed_rows(self):
        # Exactly the 3 rows with BOTH fields non-empty: A.Ret, A.Gro, B.Old,
        # B.Conf. (4 of them.) The class root A (no attr) and B.Half (source
        # missing) are excluded.
        r = self.run_tool()
        slugs = [x["ocn1"] for x in rows_from_tsv(r.stdout)]
        self.assertEqual(slugs, ["A.Ret", "A.Gro", "B.Old", "B.Conf"])

    def test_excludes_half_filled_rows(self):
        r = self.run_tool()
        slugs = {x["ocn1"] for x in rows_from_tsv(r.stdout)}
        self.assertNotIn("B.Half", slugs)
        self.assertNotIn("A", slugs)

    # --- lift from manifest --------------------------------------------
    def test_lifts_role_and_grade_from_matching_manifest(self):
        r = self.run_tool()
        by = self.index(rows_from_tsv(r.stdout))
        self.assertEqual(by["A.Ret"]["role"], "popularizer")
        self.assertEqual(by["A.Ret"]["evidence_grade"], "CLEAR")
        self.assertEqual(by["A.Ret"]["source_manifest"], "lot-eponyms.manifest.json")
        self.assertEqual(by["A.Ret"]["manifest_conflict"], "")

    def test_attribution_type_maps_popularizer_to_C(self):
        # docs/naming-attribution-audit-methodology.md ties role qualifier
        # "(popularizer)" verbatim to type C.
        r = self.run_tool()
        by = self.index(rows_from_tsv(r.stdout))
        self.assertEqual(by["A.Ret"]["attribution_type"], "C")
        # "analyst and popularizer" still contains the popularizer keyword -> C.
        self.assertEqual(by["A.Gro"]["attribution_type"], "C")

    def test_sidecar_attribution_fields_equal_catalogue(self):
        # The sidecar's attributed_to/source come from the CSV, verbatim.
        r = self.run_tool()
        by = self.index(rows_from_tsv(r.stdout))
        self.assertEqual(by["A.Ret"]["attributed_to"], "Richard Réti (popularizer)")
        self.assertEqual(by["A.Ret"]["attribution_source"], "Wikipedia, Réti Opening")

    # --- unknown (no manifest) -----------------------------------------
    def test_no_manifest_row_is_unknown(self):
        r = self.run_tool()
        by = self.index(rows_from_tsv(r.stdout))
        self.assertEqual(by["B.Old"]["role"], "unknown")
        self.assertEqual(by["B.Old"]["evidence_grade"], "unknown")
        self.assertEqual(by["B.Old"]["attribution_type"], "unknown")
        self.assertEqual(by["B.Old"]["source_manifest"], "")
        # still carries the catalogue attribution verbatim
        self.assertEqual(by["B.Old"]["attributed_to"], "Some Master (popularizer)")

    # --- conflict: CSV wins, flagged -----------------------------------
    def test_conflict_csv_wins_and_is_flagged(self):
        # B.Conf: a manifest exists for this slug, but its attributed_to does
        # not match the CSV. The CSV value wins; role/grade are NOT lifted from
        # the disagreeing manifest (treated as unknown); the conflict is flagged
        # naming the manifest.
        r = self.run_tool()
        by = self.index(rows_from_tsv(r.stdout))
        self.assertEqual(by["B.Conf"]["attributed_to"], "CSV Authority (advocate)")
        self.assertEqual(by["B.Conf"]["role"], "unknown")
        self.assertEqual(by["B.Conf"]["evidence_grade"], "unknown")
        self.assertEqual(by["B.Conf"]["source_manifest"], "")
        self.assertIn("conflict.manifest.json", by["B.Conf"]["manifest_conflict"])

    def test_non_attribution_manifest_is_ignored(self):
        # The diacritic manifest touches A.Ret but carries no attribution data;
        # A.Ret's role/grade come from the real attribution manifest, and the
        # diacritic file is never named as a source.
        r = self.run_tool()
        by = self.index(rows_from_tsv(r.stdout))
        self.assertEqual(by["A.Ret"]["source_manifest"], "lot-eponyms.manifest.json")
        self.assertNotIn("diacritics", by["A.Ret"]["source_manifest"])

    # --- never fabricate -----------------------------------------------
    def test_every_value_traces_to_manifest_or_is_unknown(self):
        r = self.run_tool()
        for row in rows_from_tsv(r.stdout):
            has_manifest = bool(row["source_manifest"])
            for col in ("role", "evidence_grade", "attribution_type"):
                if not has_manifest:
                    self.assertEqual(row[col], "unknown",
                                     f"{row['ocn1']}.{col} must be unknown without a manifest")
                else:
                    self.assertNotEqual(row[col], "", f"{row['ocn1']}.{col}")

    # --- summary -------------------------------------------------------
    def test_summary_reports_resolved_vs_unknown(self):
        r = self.run_tool("--summary")
        self.assertEqual(r.returncode, 0, r.stderr)
        text = r.stderr
        counts = {}
        for line in text.splitlines():
            parts = line.split("\t")
            if len(parts) == 2 and parts[1].strip().isdigit():
                counts[parts[0].strip()] = int(parts[1].strip())
        self.assertEqual(counts.get("attributed"), 4)
        self.assertEqual(counts.get("resolved"), 2)   # A.Ret, A.Gro
        self.assertEqual(counts.get("unknown"), 2)    # B.Old, B.Conf
        self.assertEqual(counts.get("conflict"), 1)   # B.Conf

    # --- output formats ------------------------------------------------
    def test_json_format_parses(self):
        r = self.run_tool("--format", "json")
        self.assertEqual(r.returncode, 0, r.stderr)
        by = {row["ocn1"]: row for row in json.loads(r.stdout)}
        self.assertEqual(by["A.Ret"]["role"], "popularizer")
        self.assertEqual(by["B.Old"]["role"], "unknown")

    def test_table_format_human_readable(self):
        r = self.run_tool("--format", "table")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("A.Ret", r.stdout)
        self.assertIn("popularizer", r.stdout)
        self.assertIn("ocn1", r.stdout)

    def test_out_file_written(self):
        out = self.tmp / "sidecar.tsv"
        r = self.run_tool("--out", str(out))
        self.assertEqual(r.returncode, 0, r.stderr)
        by = self.index(rows_from_tsv(out.read_text(encoding="utf-8")))
        self.assertEqual(by["A.Ret"]["evidence_grade"], "CLEAR")

    # --- filters -------------------------------------------------------
    def test_grade_filter(self):
        r = self.run_tool("--evidence-grade", "unknown")
        slugs = [x["ocn1"] for x in rows_from_tsv(r.stdout)]
        self.assertEqual(slugs, ["B.Old", "B.Conf"])

    def test_conflicts_only_filter(self):
        r = self.run_tool("--conflicts-only")
        slugs = [x["ocn1"] for x in rows_from_tsv(r.stdout)]
        self.assertEqual(slugs, ["B.Conf"])

    # --- error handling ------------------------------------------------
    def test_missing_catalogue_is_error(self):
        r = self.run_tool(catalog=self.tmp / "nope.csv")
        self.assertEqual(r.returncode, 1)

    def test_missing_manifests_dir_is_error(self):
        r = subprocess.run(
            [sys.executable, str(TOOL), "--catalog", str(self.catalog),
             "--manifests", str(self.tmp / "no_such_dir")],
            capture_output=True, text=True, check=False)
        self.assertEqual(r.returncode, 1)


class SidecarDriftTests(unittest.TestCase):
    SIDECAR = REPO_ROOT / "catalog" / "ocn-1.attribution.tsv"

    def test_committed_sidecar_is_current(self):
        """The committed sidecar must equal a fresh rebuild from the live
        catalogue + committed manifests. A catalogue/manifest change without a
        regen fails here. Stable because the join is deterministic."""
        from attribution_metadata import build_from_repo

        self.assertTrue(self.SIDECAR.exists(), "sidecar not committed")
        fresh = build_from_repo()
        self.assertEqual(
            self.SIDECAR.read_text(encoding="utf-8"), fresh,
            "catalog/ocn-1.attribution.tsv is stale — regenerate with "
            "tools/attribution_metadata.py --out catalog/ocn-1.attribution.tsv")

    def test_sidecar_covers_exactly_live_attributed_rows(self):
        import attribution_metadata as am

        catalog = am.load_catalog(am.DEFAULT_CATALOG)
        live_attr = {r["ocn1"] for r in catalog if am.is_attributed(r)}
        with self.SIDECAR.open(newline="", encoding="utf-8") as f:
            sidecar = {r["ocn1"] for r in csv.DictReader(f, delimiter="\t")}
        self.assertEqual(sidecar, live_attr)

    def test_sidecar_values_trace_to_manifest_or_unknown(self):
        with self.SIDECAR.open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f, delimiter="\t"))
        for row in rows:
            has_manifest = bool(row["source_manifest"])
            for col in ("role", "evidence_grade", "attribution_type"):
                if not has_manifest:
                    self.assertEqual(row[col], "unknown", f"{row['ocn1']}.{col}")
                else:
                    self.assertTrue(row[col], f"{row['ocn1']}.{col}")

    def test_sidecar_attribution_matches_live_catalogue(self):
        import attribution_metadata as am

        catalog = {r["ocn1"]: r for r in am.load_catalog(am.DEFAULT_CATALOG)}
        with self.SIDECAR.open(newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f, delimiter="\t"):
                cat = catalog[row["ocn1"]]
                self.assertEqual(row["attributed_to"], cat["attributed_to"].strip())
                self.assertEqual(
                    row["attribution_source"], cat["attribution_source"].strip())


if __name__ == "__main__":
    unittest.main()
