"""Tests for web/build.py — the static explorer build (roadmap H2.3).

The explorer is a deployment artefact with two properties that are easy
to break silently and expensive to discover in production, so both are
pinned here:

  * **The payload is the display projection, not a second catalogue.**
    All 5,899 rows survive, every row carries a `fen` the board renderer
    can use, `notes` is gone entirely (~49% boilerplate per the July 2026
    audit) and the two synthetic alias shapes H2.6 deletes (`Main Line`,
    `<SAN> Line`) never reach a page. Real aliases are untouched.
  * **Nothing on the page reaches a third-party host.** The site is
    served from a static directory with no backend and no CDN: every
    `src`/`href` in the markup is local, and the only absolute URLs the
    module builds are the Lichess analysis deep link and the repository
    link. A stray font or analytics tag would break that guarantee
    without breaking any page.

Run:
    python3 -m unittest tools.tests.test_web_build
"""
from __future__ import annotations

import importlib.util
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
WEB_DIR = REPO_ROOT / "web"

# Loaded by path under a unique name: `build` is too generic to import by
# module name from a repo that also has a gitignored `build/` directory.
_SPEC = importlib.util.spec_from_file_location("ocn_web_build", WEB_DIR / "build.py")
assert _SPEC and _SPEC.loader
web_build = importlib.util.module_from_spec(_SPEC)
sys.modules["ocn_web_build"] = web_build
_SPEC.loader.exec_module(web_build)

EXPECTED_ROWS = 5899
TEST_VERSION = "ocn-1.2.0-test"

#: `B.Sic.Naj.Eng` after 6.Be3 — the roadmap's own headline row.
NAJDORF_ENGLISH_FEN = "rnbqkb1r/1p2pppp/p2p1n2/8/3NP3/2N1B3/PPP2PPP/R2QKB1R b KQkq - 1 6"

#: The one absolute URL allowed to appear in the shipped markup.
REPO_URL = "https://github.com/escacsfigueres/ocn"

#: Roadmap H2.3 caps the payload; H2.6 will shrink it further by deleting
#: the synthetic aliases from the catalogue itself.
MAX_PAYLOAD_BYTES = 4 * 1024 * 1024

_BUILT: dict[str, object] = {}


def built_site() -> tuple[Path, dict]:
    """Build the site once into a temp dir, shared by every test below."""
    if not _BUILT:
        tmp = tempfile.TemporaryDirectory()
        out = Path(tmp.name) / "dist"
        web_build.build_dist(out, version=TEST_VERSION)
        _BUILT["tmp"] = tmp  # keep alive for the process lifetime
        _BUILT["out"] = out
        _BUILT["data"] = json.loads((out / "data" / "ocn.json").read_text(encoding="utf-8"))
    return _BUILT["out"], _BUILT["data"]  # type: ignore[return-value]


class SyntheticAliasTests(unittest.TestCase):
    def test_bare_main_line_is_synthetic(self) -> None:
        self.assertTrue(web_build.is_synthetic_alias("Main Line"))

    def test_san_line_shapes_are_synthetic(self) -> None:
        for alias in ("Nf6 Line", "O-O Line", "O-O-O Line", "Bxf6 Line",
                      "cxd5 Line", "e4 Line", "Qa4+ Line", "Nge2 Line"):
            with self.subTest(alias=alias):
                self.assertTrue(web_build.is_synthetic_alias(alias))

    def test_real_aliases_survive(self) -> None:
        # Including the near-synthetic ones outside H2.6's named lot: the
        # explorer suppresses what the catalogue is committed to deleting,
        # not everything that reads generated.
        for alias in ("Lasker-Pelikán", "Berlin Endgame", "Castled Line",
                      "Fianchetto Line", "Modern Main Line", "Korchnoi Line",
                      "Dragon", "Main Line Dragon"):
            with self.subTest(alias=alias):
                self.assertFalse(web_build.is_synthetic_alias(alias))

    def test_display_aliases_filters_a_mixed_cell(self) -> None:
        self.assertEqual(
            web_build.display_aliases("Dragon|Nf6 Line|Main Line|Yugoslav"),
            ["Dragon", "Yugoslav"],
        )


class PayloadTests(unittest.TestCase):
    def test_dist_contains_every_asset(self) -> None:
        out, _ = built_site()
        self.assertTrue(out.is_dir())
        for asset in web_build.STATIC_ASSETS:
            with self.subTest(asset=asset):
                self.assertTrue((out / asset).is_file())
        self.assertTrue((out / "data" / "ocn.json").is_file())

    def test_static_assets_are_copied_verbatim(self) -> None:
        out, _ = built_site()
        for asset in web_build.STATIC_ASSETS:
            with self.subTest(asset=asset):
                self.assertEqual(
                    (out / asset).read_bytes(), (WEB_DIR / asset).read_bytes())

    def test_envelope(self) -> None:
        _, data = built_site()
        self.assertEqual(data["schema"], web_build.SCHEMA)
        self.assertEqual(data["catalog_version"], TEST_VERSION)
        self.assertIn("catalog/ocn-1.csv", data["generated_note"])

    def test_whole_catalogue_is_present(self) -> None:
        _, data = built_site()
        self.assertEqual(len(data["rows"]), EXPECTED_ROWS)

    def test_payload_stays_under_the_roadmap_cap(self) -> None:
        out, _ = built_site()
        size = (out / "data" / "ocn.json").stat().st_size
        self.assertLess(size, MAX_PAYLOAD_BYTES, f"payload grew to {size} bytes")

    def test_every_row_carries_a_fen(self) -> None:
        _, data = built_site()
        missing = [row["slug"] for row in data["rows"] if not row.get("fen")]
        self.assertEqual(missing, [])

    def test_known_row_fen(self) -> None:
        _, data = built_site()
        row = next(r for r in data["rows"] if r["slug"] == "B.Sic.Naj.Eng")
        self.assertEqual(row["fen"], NAJDORF_ENGLISH_FEN)
        self.assertEqual(row["san"], "1.e4 c5 2.Nf3 d6 3.d4 cxd4 4.Nxd4 Nf6 5.Nc3 a6 6.Be3")
        self.assertEqual(row["eco"], ["B90"])
        self.assertEqual(row["parent"], "B.Sic.Naj")

    def test_class_roots_get_the_initial_position(self) -> None:
        _, data = built_site()
        roots = [row for row in data["rows"] if row["depth"] == 0]
        self.assertEqual(len(roots), 5)
        for row in roots:
            with self.subTest(slug=row["slug"]):
                self.assertEqual(row["fen"], web_build.START_FEN)
                self.assertNotIn("san", row)
                self.assertNotIn("parent", row)

    def test_notes_are_dropped_entirely(self) -> None:
        _, data = built_site()
        keys = {key for row in data["rows"] for key in row}
        self.assertNotIn("notes", keys)
        self.assertNotIn("moves_uci", keys)
        self.assertNotIn("eco_legacy", keys)

    def test_synthetic_aliases_are_stripped_from_the_b_rows(self) -> None:
        _, data = built_site()
        b_rows = [row for row in data["rows"] if row["slug"].startswith("B")]
        self.assertGreater(len(b_rows), 1000)
        offenders = [
            (row["slug"], alias)
            for row in b_rows
            for alias in row.get("aliases", [])
            if web_build.is_synthetic_alias(alias)
        ]
        self.assertEqual(offenders, [])

    def test_real_aliases_survive_the_filter(self) -> None:
        _, data = built_site()
        row = next(r for r in data["rows"] if r["slug"] == "B.Sic.Sve")
        self.assertEqual(row["aliases"], ["Lasker-Pelikán", "Cheliabinsk"])

    def test_lichess_label_carries_its_match_kind(self) -> None:
        _, data = built_site()
        row = next(r for r in data["rows"] if r["slug"] == "B.Sic.Naj.Eng")
        self.assertEqual(row["lichess"]["kind"], "exact")
        self.assertEqual(
            row["lichess"]["name"],
            "Sicilian Defense: Najdorf Variation, English Attack")
        prefix = next(r for r in data["rows"] if r["slug"] == "A.Hol.Sto")
        self.assertEqual(prefix["lichess"]["kind"], "prefix")

    def test_attribution_only_where_attributed(self) -> None:
        _, data = built_site()
        attributed = [row for row in data["rows"] if row.get("attributed_to")]
        self.assertEqual(len(attributed), 26)
        for row in data["rows"]:
            if not row.get("attributed_to"):
                with self.subTest(slug=row["slug"]):
                    self.assertNotIn("attribution_source", row)
                    self.assertNotIn("historical_notes", row)

    def test_every_parent_resolves(self) -> None:
        _, data = built_site()
        slugs = {row["slug"] for row in data["rows"]}
        dangling = [
            row["slug"] for row in data["rows"]
            if row.get("parent") and row["parent"] not in slugs
        ]
        self.assertEqual(dangling, [])

    def test_relation_targets_resolve(self) -> None:
        _, data = built_site()
        slugs = {row["slug"] for row in data["rows"]}
        targets = [
            target
            for row in data["rows"]
            for target in ([row["transposes_to"]] if row.get("transposes_to") else [])
            + row.get("same_as", [])
        ]
        self.assertGreater(len(targets), 100)
        self.assertEqual([t for t in targets if t not in slugs], [])

    def test_two_builds_are_byte_identical(self) -> None:
        first = web_build.render_json(
            web_build.build_document(version=TEST_VERSION))
        second = web_build.render_json(
            web_build.build_document(version=TEST_VERSION))
        self.assertEqual(first, second)

    def test_no_middle_dot_anywhere(self) -> None:
        out, _ = built_site()
        for path in (out / "data" / "ocn.json", *(out / a for a in web_build.STATIC_ASSETS)):
            with self.subTest(path=path.name):
                self.assertNotIn("·", path.read_text(encoding="utf-8"))

    def test_middle_dot_fails_the_build(self) -> None:
        with self.assertRaises(ValueError):
            web_build.check_no_middle_dot("fake.js", "a · b")


class NoExternalRequestTests(unittest.TestCase):
    """The site must be servable from a static directory with no network."""

    ATTR_URL_RE = re.compile(r"""\b(?:src|href)\s*=\s*["']([^"']+)["']""")
    ABSOLUTE_RE = re.compile(r"""https?://[^\s"'`)]+""")

    def test_index_html_references_only_local_assets(self) -> None:
        out, _ = built_site()
        html = (out / "index.html").read_text(encoding="utf-8")
        external = [
            url for url in self.ATTR_URL_RE.findall(html)
            if url.startswith(("http://", "https://", "//"))
        ]
        self.assertEqual(external, [REPO_URL])

    def test_index_html_has_no_stray_absolute_url(self) -> None:
        # Catches an absolute URL smuggled through an attribute this test
        # does not scan (srcset, @import in a style block, a preload).
        out, _ = built_site()
        html = (out / "index.html").read_text(encoding="utf-8")
        urls = set(self.ABSOLUTE_RE.findall(html))
        # The SVG favicon data URI names the SVG namespace, which is a URL
        # but never fetched.
        urls.discard("http://www.w3.org/2000/svg")
        self.assertEqual(urls, {REPO_URL})

    def test_app_js_fetches_only_its_own_payload(self) -> None:
        source = (WEB_DIR / "app.js").read_text(encoding="utf-8")
        calls = re.findall(r"fetch\(([^)]*)\)", source)
        self.assertEqual(calls, ["DATA_URL"])
        self.assertIn('const DATA_URL = "data/ocn.json";', source)

    def test_app_js_absolute_urls_are_the_two_documented_links(self) -> None:
        source = (WEB_DIR / "app.js").read_text(encoding="utf-8")
        urls = set(self.ABSOLUTE_RE.findall(source))
        urls.discard("http://www.w3.org/1999/xhtml")   # DOM namespaces, not requests
        urls.discard("http://www.w3.org/2000/svg")
        self.assertEqual(
            urls,
            {"https://lichess.org/analysis/standard/", REPO_URL},
        )

    def test_css_has_no_import_or_remote_url(self) -> None:
        source = (WEB_DIR / "style.css").read_text(encoding="utf-8")
        self.assertNotIn("@import", source)
        self.assertEqual(self.ABSOLUTE_RE.findall(source), [])


if __name__ == "__main__":
    unittest.main()
