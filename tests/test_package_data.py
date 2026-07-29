"""Drift guard for the catalogue bundled inside the published packages.

`src/ocn/data/` and `rust/data/` hold committed copies of catalogue
artefacts so the wheel and the crate answer lookups with no checkout and
no network. Copies drift: a catalogue edit that is not followed by
`tools/sync_package_data.py --apply` would ship stale openings under a
fresh version number. These tests fail the moment the committed bytes
stop matching a fresh sync — the same pattern as
`tools/tests/test_attribution_metadata.py`'s `SidecarDriftTests` guards
`catalog/ocn-1.attribution.tsv`.

Both targets are guarded, and one extra test pins them to *each other*:
two packages shipping different catalogues under the same version number
is the failure mode the whole arrangement exists to prevent.
"""
from __future__ import annotations

import csv
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "tools"))
sys.path.insert(0, str(REPO_ROOT / "src"))  # src last so `ocn` wins over tools/ocn.py

from ocn import Catalog  # noqa: E402
from sync_package_data import (  # noqa: E402
    CATALOG_VERSION,
    DATA_DIR,
    RUST_DATA_DIR,
    RUST_FILES,
    build_payload,
    drifted,
    rust_payload,
)


class BundledDataDriftTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.payload = build_payload()

    def test_every_bundled_file_is_committed(self) -> None:
        for name in self.payload:
            with self.subTest(name=name):
                self.assertTrue((DATA_DIR / name).exists(), f"{name} not committed")

    def test_bundled_data_is_byte_identical_to_a_fresh_sync(self) -> None:
        self.assertEqual(
            drifted(self.payload),
            [],
            "src/ocn/data/ is stale — regenerate with "
            "python3 tools/sync_package_data.py --apply",
        )

    def test_version_file_matches_the_declared_catalogue_release(self) -> None:
        self.assertEqual(
            (DATA_DIR / "VERSION").read_text(encoding="utf-8").strip(),
            CATALOG_VERSION,
        )
        self.assertEqual(Catalog.load().version(), CATALOG_VERSION)


class RustBundledDataDriftTests(unittest.TestCase):
    """The same guard for `rust/data/`, which the crate embeds at compile
    time via `include_str!`. A stale copy here ships a wrong catalogue
    inside every binary built from the crate."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.payload = rust_payload()

    def test_every_embedded_file_is_committed(self) -> None:
        for name in self.payload:
            with self.subTest(name=name):
                self.assertTrue(
                    (RUST_DATA_DIR / name).exists(), f"rust/data/{name} not committed"
                )

    def test_embedded_data_is_byte_identical_to_a_fresh_sync(self) -> None:
        self.assertEqual(
            drifted(self.payload, RUST_DATA_DIR),
            [],
            "rust/data/ is stale — regenerate with "
            "python3 tools/sync_package_data.py --apply",
        )

    def test_the_crate_embeds_exactly_what_it_has_a_reader_for(self) -> None:
        # The Lichess cross-reference is deliberately absent: the crate
        # has no reader for it, and embedding it would grow every binary
        # built from the crate by 436 KB for nothing.
        self.assertEqual(set(self.payload), set(RUST_FILES))
        self.assertNotIn("ocn-1.lichess-xref.tsv", self.payload)

    def test_both_packages_bundle_the_same_catalogue_bytes(self) -> None:
        """The point of one payload, two targets."""
        for name in RUST_FILES:
            with self.subTest(name=name):
                self.assertEqual(
                    (RUST_DATA_DIR / name).read_bytes(),
                    (DATA_DIR / name).read_bytes(),
                    f"{name} differs between the wheel and the crate",
                )

    def test_the_crate_manifest_declares_the_bundled_release(self) -> None:
        """`rust/Cargo.toml` moves with the catalogue it embeds."""
        manifest = (RUST_DATA_DIR.parent / "Cargo.toml").read_text(encoding="utf-8")
        self.assertIn(f'version = "{CATALOG_VERSION}"', manifest)
        self.assertIn('name = "ocn"', manifest)


class PositionsIndexTests(unittest.TestCase):
    """The index must cover every concrete row, with true FEN counters."""

    @classmethod
    def setUpClass(cls) -> None:
        with (DATA_DIR / "ocn-1.positions.tsv").open(
            newline="", encoding="utf-8"
        ) as handle:
            cls.rows = list(csv.DictReader(handle, delimiter="\t"))
        cls.catalog = Catalog.load()

    def test_index_covers_every_row_that_has_moves(self) -> None:
        concrete = {row.ocn1 for row in self.catalog if row.moves_uci}
        self.assertEqual({row["ocn1"] for row in self.rows}, concrete)

    def test_fen_column_carries_real_counters(self) -> None:
        """Not the old `fen_key 0 1` placeholder: the counters are replayed."""
        by_slug = {row["ocn1"]: row for row in self.rows}
        # 1.e4 c5 2.Nf3 d6 3.d4 cxd4 4.Nxd4 Nf6 5.Nc3 a6 6.Be3 is eleven
        # plies; the last capture was ply 7, so the clock reads 1 and the
        # fullmove number is 11 // 2 + 1.
        najdorf = by_slug["B.Sic.Naj.Eng"]
        self.assertEqual(najdorf["fen"], f"{najdorf['fen_key']} 1 6")
        placeholders = sum(1 for row in self.rows if row["fen"].endswith(" 0 1"))
        self.assertLess(placeholders, len(self.rows) // 10, "counters look placeheld")

    def test_every_fen_extends_its_own_fen_key(self) -> None:
        for row in self.rows:
            self.assertTrue(row["fen"].startswith(row["fen_key"] + " "), row["ocn1"])
            halfmove, fullmove = row["fen"].rsplit(" ", 2)[1:]
            self.assertTrue(halfmove.isdigit(), row["ocn1"])
            self.assertGreaterEqual(int(fullmove), 1, row["ocn1"])

    def test_fullmove_number_follows_the_move_count(self) -> None:
        for row in self.rows:
            plies = len(row["moves_uci"].split())
            self.assertEqual(int(row["fen"].rsplit(" ", 1)[1]), plies // 2 + 1, row["ocn1"])


if __name__ == "__main__":
    unittest.main()
