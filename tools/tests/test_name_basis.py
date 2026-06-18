"""Tests for tools/name_basis.py.

The name_basis sidecar classifies WHY each OCN-1 opening name exists, making
the "do-not-attribute" map (docs/non-person-opening-name-taxonomy.md) machine
readable. The deterministic first pass is *conservative*: it assigns a category
ONLY when an unambiguous rule fires, and marks everything else ``review`` — it
NEVER guesses a category. Two rules are implemented:

  * ``person`` (rule ``attributed_to``) — fires iff ``attributed_to`` is
    non-empty (an already-asserted person attribution; the validator enforces
    ``attributed_to => attribution_source``). The safest deterministic signal.
  * ``descriptor`` (rule ``editorial_leaf_token``) — fires iff the LEAF
    (last comma-segment) of ``canonical_name`` is one of a small curated set of
    pure editorial-bookkeeping tokens the taxonomy doc's category 8 +
    bucket D enumerate as permanently-unattributed descriptors
    (Main Line / Accepted / Declined / Move Order).

Every other row → ``name_basis = review``, ``basis_rule = review``. These tests
build small CSV fixtures so they do not depend on the live catalogue, plus one
drift test pinning the committed sidecar to a fresh deterministic rebuild.
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
TOOL = REPO_ROOT / "tools" / "name_basis.py"
sys.path.insert(0, str(REPO_ROOT / "tools"))

# A tiny catalogue mirroring the 14-column schema. Rows chosen to exercise each
# rule and the review fallback:
#   A               class root, plain descriptor name      -> review
#   A.Ret           ATTRIBUTED person eponym               -> person
#   A.Ret.Acc       leaf "Accepted" (editorial)            -> descriptor
#   B.Sic           geographic family (no rule)            -> review
#   B.Sic.Dra       metaphor "Dragon" (no rule)            -> review
#   D.QGD.Mln       leaf "Main Line" (editorial)           -> descriptor
#   E.Nim.Sml.Kmo   leaf "Move Order" (editorial)          -> descriptor
#   B.Fre.Win.Dec   leaf "Declined" (editorial)            -> descriptor
#   C.Bsh           move/piece name "Bishop's Opening"     -> review
CATALOG_HEADER = (
    "ocn1,canonical_name,eco_legacy,parent_ocn1,moves_uci,depth,aliases,"
    "flags,notes,attributed_to,attribution_source,historical_notes,"
    "transposes_to,same_as"
)
CATALOG_ROWS = [
    "A,Flank Openings,,,,0,,,Top-level class.,,,,,",
    "A.Ret,Réti Opening,A04,A,g1f3,1,Zukertort,,1.Nf3.,Richard Réti (popularizer),"
    '"Wikipedia, Réti Opening",Named for Réti.,,',
    "A.Ret.Acc,\"Réti Opening, Accepted\",A09,A.Ret,g1f3 d7d5 c2c4,2,,,2.c4.,,,,,",
    "B.Sic,Sicilian Defense,B20,B,e2e4 c7c5,1,,,1...c5.,,,,,",
    "B.Sic.Dra,\"Sicilian, Dragon\",B70,B.Sic,e2e4 c7c5 g1f3 d7d6,2,,,Dragon.,,,,,",
    "D.QGD.Mln,\"Queen's Gambit Declined, Main Line\",D30,D.QGD,d2d4 d7d5 c2c4 e7e6,2,,,Main line.,,,,,",
    "E.Nim.Sml.Kmo,\"Nimzo, Main, Move Order\",E40,E.Nim.Sml,d2d4 g8f6 c2c4 e7e6,3,,,Move order.,,,,,",
    "B.Fre.Win.Dec,\"French, Winawer, Declined\",C18,B.Fre.Win,e2e4 e7e6 b1c3 f8b4,3,,,Declined.,,,,,",
    "C.Bsh,Bishop's Opening,C23,C,e2e4 e7e5 f1c4,1,,,2.Bc4.,,,,,",
]


def write_catalog(path: Path, rows=None) -> None:
    body = CATALOG_ROWS if rows is None else rows
    path.write_text("\n".join([CATALOG_HEADER, *body]) + "\n", encoding="utf-8")


def rows_from_tsv(text: str) -> list[dict]:
    return list(csv.DictReader(io.StringIO(text), delimiter="\t"))


class NameBasisTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)
        self.catalog = self.tmp / "cat.csv"
        write_catalog(self.catalog)

    def run_tool(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(TOOL), "--catalog", str(self.catalog), *args],
            capture_output=True, text=True, check=False)

    def index(self, rows: list[dict]) -> dict[str, dict]:
        return {r["ocn1"]: r for r in rows}

    # --- schema ---------------------------------------------------------
    def test_output_schema_columns(self) -> None:
        r = self.run_tool()
        self.assertEqual(r.returncode, 0, r.stderr)
        rows = rows_from_tsv(r.stdout)
        self.assertEqual(
            list(rows[0].keys()),
            ["ocn1", "canonical_name", "name_basis", "basis_rule"])

    def test_one_row_per_catalogue_row_in_order(self) -> None:
        r = self.run_tool()
        slugs = [x["ocn1"] for x in rows_from_tsv(r.stdout)]
        self.assertEqual(slugs, [
            "A", "A.Ret", "A.Ret.Acc", "B.Sic", "B.Sic.Dra",
            "D.QGD.Mln", "E.Nim.Sml.Kmo", "B.Fre.Win.Dec", "C.Bsh"])

    # --- person rule ----------------------------------------------------
    def test_person_rule_fires_on_attributed_row(self) -> None:
        r = self.run_tool()
        by = self.index(rows_from_tsv(r.stdout))
        self.assertEqual(by["A.Ret"]["name_basis"], "person")
        self.assertEqual(by["A.Ret"]["basis_rule"], "attributed_to")

    def test_person_rule_does_not_fire_without_attribution(self) -> None:
        # B.Sic is a geographic family with empty attributed_to: must be review,
        # never auto-classified as geography (no deterministic geography rule).
        r = self.run_tool()
        by = self.index(rows_from_tsv(r.stdout))
        self.assertEqual(by["B.Sic"]["name_basis"], "review")
        self.assertEqual(by["B.Sic"]["basis_rule"], "review")

    def test_person_rule_requires_source_too(self) -> None:
        # The validator enforces attributed_to => attribution_source. A row with
        # attributed_to but no source is malformed; the person rule must NOT
        # fire on it (treat as review, not a confident person classification).
        rows = [
            "A,Flank,,,,0,,,c.,,,,,",
            "A.Half,Half Attributed,A00,A,g1f3,1,,,x.,Some Person,,,,",
        ]
        cat = self.tmp / "half.csv"
        write_catalog(cat, rows)
        r = subprocess.run(
            [sys.executable, str(TOOL), "--catalog", str(cat)],
            capture_output=True, text=True, check=False)
        self.assertEqual(r.returncode, 0, r.stderr)
        by = self.index(rows_from_tsv(r.stdout))
        self.assertEqual(by["A.Half"]["name_basis"], "review")
        self.assertEqual(by["A.Half"]["basis_rule"], "review")

    # --- descriptor (editorial leaf token) rule -------------------------
    def test_descriptor_rule_fires_on_editorial_leaf(self) -> None:
        r = self.run_tool()
        by = self.index(rows_from_tsv(r.stdout))
        for slug in ("A.Ret.Acc", "D.QGD.Mln", "E.Nim.Sml.Kmo", "B.Fre.Win.Dec"):
            self.assertEqual(by[slug]["name_basis"], "descriptor",
                             f"{slug} should be descriptor")
            self.assertEqual(by[slug]["basis_rule"], "editorial_leaf_token",
                             f"{slug} rule")

    def test_descriptor_rule_is_leaf_only_not_substring(self) -> None:
        # A token appearing mid-name (not as the leaf segment) must NOT trigger
        # the descriptor rule — only the distinguishing leaf segment counts.
        rows = [
            "A,Flank,,,,0,,,c.,,,,,",
            "A.X,\"Accepted Variation, Dragon\",A00,A,g1f3,1,,,x.,,,,,",
        ]
        cat = self.tmp / "midname.csv"
        write_catalog(cat, rows)
        r = subprocess.run(
            [sys.executable, str(TOOL), "--catalog", str(cat)],
            capture_output=True, text=True, check=False)
        by = self.index(rows_from_tsv(r.stdout))
        # leaf is "Dragon" (metaphor, no rule) -> review, despite "Accepted" mid
        self.assertEqual(by["A.X"]["name_basis"], "review")

    def test_person_rule_wins_over_descriptor(self) -> None:
        # If a row is both attributed AND has an editorial leaf, person wins
        # (highest-confidence rule is checked first).
        rows = [
            "A,Flank,,,,0,,,c.,,,,,",
            "A.E,\"Englund Gambit, Accepted\",A40,A,d2d4,1,,,x.,"
            'Fritz Englund,"Source X",note.,,',
        ]
        cat = self.tmp / "both.csv"
        write_catalog(cat, rows)
        r = subprocess.run(
            [sys.executable, str(TOOL), "--catalog", str(cat)],
            capture_output=True, text=True, check=False)
        by = self.index(rows_from_tsv(r.stdout))
        self.assertEqual(by["A.E"]["name_basis"], "person")
        self.assertEqual(by["A.E"]["basis_rule"], "attributed_to")

    # --- review fallback ------------------------------------------------
    def test_ambiguous_rows_default_to_review(self) -> None:
        r = self.run_tool()
        by = self.index(rows_from_tsv(r.stdout))
        # geography family, metaphor, move/piece name, class root — all review
        for slug in ("A", "B.Sic", "B.Sic.Dra", "C.Bsh"):
            self.assertEqual(by[slug]["name_basis"], "review", slug)
            self.assertEqual(by[slug]["basis_rule"], "review", slug)

    def test_no_category_without_a_rule(self) -> None:
        # Invariant: every non-review name_basis MUST carry a non-review
        # basis_rule (a category is never assigned without a deterministic
        # rule firing). And review rows carry the review rule.
        r = self.run_tool()
        for row in rows_from_tsv(r.stdout):
            if row["name_basis"] == "review":
                self.assertEqual(row["basis_rule"], "review")
            else:
                self.assertNotEqual(row["basis_rule"], "review")
                self.assertTrue(row["basis_rule"])

    # --- summary counts -------------------------------------------------
    def test_summary_counts_per_category(self) -> None:
        r = self.run_tool("--summary")
        self.assertEqual(r.returncode, 0, r.stderr)
        # summary goes to stderr; parse "category<TAB>count" lines
        text = r.stderr
        self.assertIn("person", text)
        self.assertIn("descriptor", text)
        self.assertIn("review", text)
        # parse counts
        counts = {}
        for line in text.splitlines():
            parts = line.split("\t")
            if len(parts) == 2 and parts[1].strip().isdigit():
                counts[parts[0].strip()] = int(parts[1].strip())
        self.assertEqual(counts.get("person"), 1)
        self.assertEqual(counts.get("descriptor"), 4)
        self.assertEqual(counts.get("review"), 4)

    def test_summary_json_counts(self) -> None:
        r = self.run_tool("--summary", "--format", "json")
        self.assertEqual(r.returncode, 0, r.stderr)
        # data on stdout parses as json list
        payload = json.loads(r.stdout)
        self.assertEqual(len(payload), 9)
        # summary on stderr is also valid (counts present)
        self.assertIn("review", r.stderr)

    # --- output formats -------------------------------------------------
    def test_json_format_parses(self) -> None:
        r = self.run_tool("--format", "json")
        self.assertEqual(r.returncode, 0, r.stderr)
        payload = json.loads(r.stdout)
        by = {row["ocn1"]: row for row in payload}
        self.assertEqual(by["A.Ret"]["name_basis"], "person")
        self.assertEqual(by["A.Ret.Acc"]["name_basis"], "descriptor")

    def test_table_format_human_readable(self) -> None:
        r = self.run_tool("--format", "table")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("A.Ret", r.stdout)
        self.assertIn("person", r.stdout)
        self.assertIn("ocn1", r.stdout)

    def test_out_file_written(self) -> None:
        out = self.tmp / "sidecar.tsv"
        r = self.run_tool("--out", str(out))
        self.assertEqual(r.returncode, 0, r.stderr)
        text = out.read_text(encoding="utf-8")
        by = self.index(rows_from_tsv(text))
        self.assertEqual(by["A.Ret"]["name_basis"], "person")

    # --- filter ---------------------------------------------------------
    def test_basis_filter(self) -> None:
        r = self.run_tool("--name-basis", "descriptor")
        slugs = [x["ocn1"] for x in rows_from_tsv(r.stdout)]
        self.assertEqual(
            slugs, ["A.Ret.Acc", "D.QGD.Mln", "E.Nim.Sml.Kmo", "B.Fre.Win.Dec"])

    def test_review_filter(self) -> None:
        r = self.run_tool("--name-basis", "review")
        slugs = [x["ocn1"] for x in rows_from_tsv(r.stdout)]
        self.assertEqual(slugs, ["A", "B.Sic", "B.Sic.Dra", "C.Bsh"])

    # --- error handling -------------------------------------------------
    def test_missing_catalogue_is_error(self) -> None:
        r = subprocess.run(
            [sys.executable, str(TOOL), "--catalog", str(self.tmp / "nope.csv")],
            capture_output=True, text=True, check=False)
        self.assertEqual(r.returncode, 1)


class SidecarDriftTests(unittest.TestCase):
    SIDECAR = REPO_ROOT / "catalog" / "ocn-1.name_basis.tsv"

    def test_committed_sidecar_is_current(self) -> None:
        """The committed sidecar must equal a fresh deterministic rebuild from
        the live catalogue — a catalogue change without a sidecar regen fails
        here. Stable because only deterministic rules feed it."""
        from name_basis import build_from_repo

        self.assertTrue(self.SIDECAR.exists(), "sidecar not committed")
        fresh = build_from_repo()
        self.assertEqual(
            self.SIDECAR.read_text(encoding="utf-8"), fresh,
            "catalog/ocn-1.name_basis.tsv is stale — regenerate with "
            "tools/name_basis.py --out catalog/ocn-1.name_basis.tsv")

    def test_sidecar_only_uses_known_categories(self) -> None:
        from name_basis import VALID_BASES

        with self.SIDECAR.open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f, delimiter="\t"))
        for row in rows:
            self.assertIn(row["name_basis"], VALID_BASES, row["ocn1"])

    def test_sidecar_no_category_without_rule(self) -> None:
        with self.SIDECAR.open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f, delimiter="\t"))
        for row in rows:
            if row["name_basis"] == "review":
                self.assertEqual(row["basis_rule"], "review", row["ocn1"])
            else:
                self.assertNotEqual(row["basis_rule"], "review", row["ocn1"])


if __name__ == "__main__":
    unittest.main()
