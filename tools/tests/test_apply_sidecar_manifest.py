"""The sidecar engine's job is to refuse. These test the refusals."""

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from apply_sidecar_manifest import (  # noqa: E402
    ApplyError, apply, check_referential, load_manifest, load_sidecar,
    serialize, validate_manifest,
)

HEADER = "ocn1\tevent\tyear\twhite\tblack\tcitation\n"
def _row(slug, ev, yr, w, b):
    return f"{slug}\t{ev}\t{yr}\t{w}\t{b}\t{w}-{b}, {ev}, {yr}"


ROWS = [
    _row("C.RyL", "World Championship 1st", "1886", "Steinitz, Wilhelm", "Zukertort, Johannes"),
    _row("C.RyL", "World Championship 1st", "1886", "Zukertort, Johannes", "Steinitz, Wilhelm"),
    _row("C.RyL", "World Championship 1st", "1886", "Loureda Garcia, Jose", "Garcia Camina, Bel"),
    _row("A.Bir", "World Championship 14th", "1929", "Aljechin, Yuri", "Bogoljubow"),
    _row("A.Bir", "World Championship 14th", "1929", "Bogoljubow", "Aljechin, Yuri"),
]


def sidecar_text():
    return HEADER + "\n".join(ROWS) + "\n"


def base_manifest(**over):
    m = {
        "kind": "ocn.sidecar_manifest.v1",
        "title": "test",
        "description": "test",
        "target": "x.tsv",
        "expected_file_rows": 5,
        "operations": [{
            "op": "rename", "fields": ["white", "black"],
            "from": "Aljechin, Yuri", "to": "Alekhine, Alexander",
            "expected_rows": 2, "evidence": "wikidata Q131374",
        }],
    }
    m.update(over)
    return m


class TempSidecar:
    def __enter__(self):
        self.dir = tempfile.TemporaryDirectory()
        self.path = Path(self.dir.name) / "x.tsv"
        self.path.write_text(sidecar_text(), encoding="utf-8")
        return self.path

    def __exit__(self, *a):
        self.dir.cleanup()


class ValidateManifest(unittest.TestCase):
    def test_accepts_a_well_formed_manifest(self):
        validate_manifest(base_manifest())

    def test_rejects_a_foreign_kind(self):
        with self.assertRaisesRegex(ApplyError, "kind"):
            validate_manifest(base_manifest(kind="ocn.attribution_manifest.v1"))

    def test_rejects_a_missing_key(self):
        m = base_manifest()
        del m["expected_file_rows"]
        with self.assertRaisesRegex(ApplyError, "expected_file_rows"):
            validate_manifest(m)

    def test_rejects_an_operation_with_no_evidence(self):
        m = base_manifest()
        del m["operations"][0]["evidence"]
        with self.assertRaisesRegex(ApplyError, "evidence"):
            validate_manifest(m)

    def test_rejects_a_rename_that_changes_nothing(self):
        m = base_manifest()
        m["operations"][0]["to"] = m["operations"][0]["from"]
        with self.assertRaisesRegex(ApplyError, "identical"):
            validate_manifest(m)

    def test_rejects_a_drop_with_no_match(self):
        with self.assertRaisesRegex(ApplyError, "match"):
            validate_manifest(base_manifest(operations=[
                {"op": "drop", "expected_rows": 1, "evidence": "e"}]))

    def test_rejects_expected_rows_of_zero(self):
        m = base_manifest()
        m["operations"][0]["expected_rows"] = 0
        with self.assertRaisesRegex(ApplyError, "expected_rows"):
            validate_manifest(m)


class Apply(unittest.TestCase):
    def test_renames_exactly_the_declared_fields_and_nothing_else(self):
        """A rename reaches the fields it names and stops there. The citation
        still carries the old spelling afterwards, which is the coupling that
        sync_prefix exists to close, and leaving it visible here is the point."""
        with TempSidecar() as p:
            res = apply(base_manifest(), load_sidecar(p))
        self.assertEqual(res.rows_before, 5)
        self.assertEqual(res.rows_after, 5)
        self.assertEqual(res.text.count("Alekhine, Alexander"), 2)
        self.assertEqual(res.text.count("Aljechin, Yuri"), 2)  # both in citations

    def test_refuses_when_the_file_is_a_different_size(self):
        with TempSidecar() as p:
            with self.assertRaisesRegex(ApplyError, "different version"):
                apply(base_manifest(expected_file_rows=99), load_sidecar(p))

    def test_refuses_when_an_operation_matches_the_wrong_count(self):
        m = base_manifest()
        m["operations"][0]["expected_rows"] = 3
        with TempSidecar() as p:
            with self.assertRaisesRegex(ApplyError, "matched 2"):
                apply(m, load_sidecar(p))

    def test_refuses_a_rename_that_matches_nothing(self):
        m = base_manifest()
        m["operations"][0]["from"] = "Nobody, At All"
        with TempSidecar() as p:
            with self.assertRaisesRegex(ApplyError, "matched 0"):
                apply(m, load_sidecar(p))

    def test_refuses_an_unknown_field(self):
        m = base_manifest()
        m["operations"][0]["fields"] = ["winner"]
        with TempSidecar() as p:
            with self.assertRaisesRegex(ApplyError, "winner"):
                apply(m, load_sidecar(p))

    def test_drops_only_rows_matching_every_field(self):
        m = base_manifest(operations=[{
            "op": "drop",
            "match": {"year": "1886", "white": "Loureda Garcia, Jose",
                      "black": "Garcia Camina, Bel"},
            "expected_rows": 1, "evidence": "not a participant"}])
        with TempSidecar() as p:
            res = apply(m, load_sidecar(p))
        self.assertEqual(res.rows_after, 4)
        self.assertNotIn("Loureda Garcia", res.text)
        self.assertIn("Steinitz, Wilhelm", res.text)

    def test_a_drop_never_removes_the_same_row_twice(self):
        op = {"op": "drop", "match": {"year": "1886"}, "expected_rows": 3,
              "evidence": "e"}
        m = base_manifest(operations=[op, dict(op, expected_rows=1)])
        with TempSidecar() as p:
            with self.assertRaisesRegex(ApplyError, "matched 0"):
                apply(m, load_sidecar(p))

    def test_leaves_every_other_cell_untouched(self):
        with TempSidecar() as p:
            before = load_sidecar(p)
            res = apply(base_manifest(), before)
        after = list(__import__("csv").DictReader(
            res.text.splitlines(), delimiter="\t"))
        for old, new in zip(before.rows, after):
            for k in old:
                if old[k] == "Aljechin, Yuri":
                    self.assertEqual(new[k], "Alekhine, Alexander")
                else:
                    self.assertEqual(old[k], new[k])

    def test_round_trips_a_file_it_does_not_change(self):
        with TempSidecar() as p:
            s = load_sidecar(p)
            self.assertEqual(serialize(s.fieldnames, s.rows), sidecar_text())


SYNC = {"op": "sync_prefix", "field": "citation",
        "pair_fields": ["white", "black"], "separator": "-",
        "expected_rows": 2, "evidence": "the citation repeats the pair it cites"}


class SyncPrefix(unittest.TestCase):
    def test_reanchors_the_citation_on_the_corrected_pair(self):
        m = base_manifest()
        m["operations"] = m["operations"] + [SYNC]
        with TempSidecar() as p:
            res = apply(m, load_sidecar(p))
        self.assertNotIn("Aljechin, Yuri", res.text)
        self.assertEqual(res.text.count("Alekhine, Alexander-Bogoljubow,"), 1)
        self.assertEqual(res.text.count("Bogoljubow-Alekhine, Alexander,"), 1)

    def test_never_touches_a_correct_row_that_the_wrong_one_is_a_prefix_of(self):
        """Bogoljubow, Efim contains Bogoljubow, which is why this is anchored
        rather than substituted."""
        m = base_manifest(operations=[
            {"op": "rename", "fields": ["white", "black"], "from": "Bogoljubow",
             "to": "Bogoljubow, Efim", "expected_rows": 2,
             "evidence": "wikidata Q57310"},
            dict(SYNC, expected_rows=2)])
        with TempSidecar() as p:
            res = apply(m, load_sidecar(p))
        self.assertNotIn("Efim, Efim", res.text)
        self.assertEqual(res.text.count("Bogoljubow, Efim"), 4)

    def test_leaves_rows_whose_pair_did_not_change(self):
        m = base_manifest(operations=[dict(SYNC, expected_rows=1)])
        with TempSidecar() as p:
            with self.assertRaisesRegex(ApplyError, "matched 0"):
                apply(m, load_sidecar(p))

    def test_refuses_a_file_whose_citation_is_not_its_own_pair(self):
        m = base_manifest()
        m["operations"] = m["operations"] + [SYNC]
        with TempSidecar() as p:
            text = p.read_text().replace("Steinitz, Wilhelm-Zukertort", "Nobody-Nobody", 1)
            p.write_text(text, encoding="utf-8")
            with self.assertRaisesRegex(ApplyError, "does not begin with its own"):
                apply(m, load_sidecar(p))

    def test_rejects_pair_fields_that_are_not_a_pair(self):
        with self.assertRaisesRegex(ApplyError, "pair_fields"):
            validate_manifest(base_manifest(operations=[dict(SYNC, pair_fields=["white"])]))


class Referential(unittest.TestCase):
    def test_reports_slugs_the_catalogue_does_not_know(self):
        with tempfile.TemporaryDirectory() as d:
            cat = Path(d) / "cat.csv"
            cat.write_text("ocn1,canonical_name\nC.RyL,Ruy López\n", encoding="utf-8")
            n, missing = check_referential(sidecar_text(), cat)
        self.assertEqual(n, 1)
        self.assertEqual(missing, ["A.Bir"])


class Loading(unittest.TestCase):
    def test_rejects_a_file_that_is_not_json(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "m.json"
            p.write_text("{ not json", encoding="utf-8")
            with self.assertRaisesRegex(ApplyError, "not valid JSON"):
                load_manifest(p)

    def test_rejects_a_missing_target(self):
        with self.assertRaisesRegex(ApplyError, "no such file"):
            load_sidecar(Path("/nonexistent/nope.tsv"))

    def test_loads_a_manifest_from_disk(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "m.json"
            p.write_text(json.dumps(base_manifest()), encoding="utf-8")
            self.assertEqual(load_manifest(p)["title"], "test")


if __name__ == "__main__":
    unittest.main()
