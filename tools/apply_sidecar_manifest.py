#!/usr/bin/env python3
"""Apply an OCN chronicle-sidecar manifest (dry-run by default).

The attribution engine keys every change to a slug, because a row of
`catalog/ocn-1.csv` is one opening. The chronicle sidecars are not like that:
`catalog/ocn-1.wch.tsv` holds one row per game, and a correction there is
usually "this player is spelled four ways, and one of the spellings is a
different person entirely". The unit of change is a **value**, not a row.

So this manifest declares, for every operation, exactly how many rows it must
touch, and the run aborts if the count is off by one. That is the same
guarantee `expected_changed_rows` gives on the catalogue side, expressed the
only way it can be expressed when the target is a value:

- the file must have the row count the manifest expects;
- every operation must match exactly the number of rows it declares;
- a rename may only alter cells in the fields it names, and only where the
  cell held the exact `from` value;
- a drop may only remove rows matching every field it specifies;
- nothing else in the file may differ, including column order and quoting.

`--apply --out` writes; without them nothing is written and a report is
printed. Evidence belongs in the manifest, not here: this tool moves strings
that somebody else has already proved.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path

KIND = "ocn.sidecar_manifest.v1"
REQUIRED_KEYS = ("kind", "title", "description", "target",
                 "expected_file_rows", "operations")
OPS = ("rename", "drop", "sync_prefix", "insert")


class ApplyError(Exception):
    """Anything that should stop the run before a byte is written."""


# --------------------------------------------------------------- manifest


def validate_manifest(obj: object) -> None:
    if not isinstance(obj, dict):
        raise ApplyError("manifest must be a JSON object")
    if obj.get("kind") != KIND:
        raise ApplyError(f"'kind' must be {KIND!r}, found {obj.get('kind')!r}")
    for k in REQUIRED_KEYS:
        if k not in obj:
            raise ApplyError(f"manifest is missing required key {k!r}")
    if not isinstance(obj["target"], str) or not obj["target"]:
        raise ApplyError("'target' must be a non-empty path")
    n = obj["expected_file_rows"]
    if not isinstance(n, int) or isinstance(n, bool) or n <= 0:
        raise ApplyError("'expected_file_rows' must be a positive integer")
    ops = obj["operations"]
    if not isinstance(ops, list) or not ops:
        raise ApplyError("'operations' must be a non-empty list")
    for i, op in enumerate(ops):
        where = f"operations[{i}]"
        if not isinstance(op, dict):
            raise ApplyError(f"{where} must be an object")
        kind = op.get("op")
        if kind not in OPS:
            raise ApplyError(f"{where}: 'op' must be one of {', '.join(OPS)}")
        rows = op.get("expected_rows")
        if not isinstance(rows, int) or isinstance(rows, bool) or rows <= 0:
            raise ApplyError(f"{where}: 'expected_rows' must be a positive integer")
        if not op.get("evidence"):
            raise ApplyError(f"{where}: 'evidence' is required; a change with no "
                             "stated basis does not belong in a manifest")
        if kind == "rename":
            fields = op.get("fields")
            if not isinstance(fields, list) or not fields or not all(
                    isinstance(f, str) and f for f in fields):
                raise ApplyError(f"{where}: 'fields' must be a non-empty list of names")
            if not isinstance(op.get("from"), str) or not op["from"]:
                raise ApplyError(f"{where}: 'from' must be a non-empty string")
            if not isinstance(op.get("to"), str) or not op["to"]:
                raise ApplyError(f"{where}: 'to' must be a non-empty string")
            if op["from"] == op["to"]:
                raise ApplyError(f"{where}: 'from' and 'to' are identical")
        elif kind == "drop":
            match = op.get("match")
            if not isinstance(match, dict) or not match:
                raise ApplyError(f"{where}: 'match' must be a non-empty object")
            if not all(isinstance(k, str) and isinstance(v, str)
                       for k, v in match.items()):
                raise ApplyError(f"{where}: 'match' must map field names to strings")
        elif kind == "insert":
            row = op.get("row")
            if not isinstance(row, dict) or not row:
                raise ApplyError(f"{where}: 'row' must be a non-empty object")
            if not all(isinstance(k, str) and isinstance(v, str) for k, v in row.items()):
                raise ApplyError(f"{where}: 'row' must map field names to strings")
            key = op.get("unique_by")
            #: One field where the table has an id column, several where it
            #: does not: a claim's opening already appears (a championship
            #: game) and so does its subject (another opening named after
            #: the same person), and only the combination is new.
            fields = [key] if isinstance(key, str) else key
            if not isinstance(fields, list) or not fields or not all(
                    isinstance(f, str) and f for f in fields):
                raise ApplyError(f"{where}: 'unique_by' names the field, or the "
                                 "fields together, that must not already hold "
                                 "this value")
            for field in fields:
                if field not in row:
                    raise ApplyError(
                        f"{where}: 'unique_by' field {field!r} is not in 'row'")
            if op["expected_rows"] != 1:
                raise ApplyError(f"{where}: an insert adds exactly one row")
        else:
            if not isinstance(op.get("field"), str) or not op["field"]:
                raise ApplyError(f"{where}: 'field' must be a non-empty string")
            pair = op.get("pair_fields")
            if not isinstance(pair, list) or len(pair) != 2 or not all(
                    isinstance(f, str) and f for f in pair):
                raise ApplyError(f"{where}: 'pair_fields' must be two field names")
            if not isinstance(op.get("separator"), str) or not op["separator"]:
                raise ApplyError(f"{where}: 'separator' must be a non-empty string")


def load_manifest(path: Path) -> dict:
    try:
        obj = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ApplyError(f"{path}: not valid JSON — {exc}") from exc
    validate_manifest(obj)
    return obj


# ------------------------------------------------------------------ file


@dataclass
class Sidecar:
    path: Path
    fieldnames: list[str]
    rows: list[dict]

    @property
    def sha256(self) -> str:
        return hashlib.sha256(self.path.read_bytes()).hexdigest()


def load_sidecar(path: Path) -> Sidecar:
    if not path.exists():
        raise ApplyError(f"{path}: no such file")
    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh, delimiter="\t")
        if not reader.fieldnames:
            raise ApplyError(f"{path}: no header row")
        return Sidecar(path, list(reader.fieldnames), list(reader))


def serialize(fieldnames: list[str], rows: list[dict]) -> str:
    out = ["\t".join(fieldnames)]
    for r in rows:
        out.append("\t".join((r.get(f) or "") for f in fieldnames))
    return "\n".join(out) + "\n"


# ----------------------------------------------------------------- apply


@dataclass
class OpResult:
    op: dict
    matched: int
    samples: list[str] = field(default_factory=list)


@dataclass
class ApplyResult:
    rows_before: int
    rows_after: int
    ops: list[OpResult]
    text: str
    sha_before: str
    sha_after: str


def apply(manifest: dict, sidecar: Sidecar) -> ApplyResult:
    if len(sidecar.rows) != manifest["expected_file_rows"]:
        raise ApplyError(
            f"expected {manifest['expected_file_rows']} rows but found "
            f"{len(sidecar.rows)}; the manifest was written against a different "
            "version of this file")

    for op in manifest["operations"]:
        if op["op"] == "rename":
            need = op["fields"]
        elif op["op"] == "drop":
            need = list(op["match"])
        elif op["op"] == "insert":
            need = list(op["row"])
        else:
            need = [op["field"], *op["pair_fields"]]
        for f in need:
            if f not in sidecar.fieldnames:
                raise ApplyError(f"field {f!r} is not in {sidecar.path.name}")

    rows = [dict(r) for r in sidecar.rows]
    results: list[OpResult] = []
    dropped: set[int] = set()

    for op in manifest["operations"]:
        matched, samples = 0, []
        if op["op"] == "rename":
            for r in rows:
                for f in op["fields"]:
                    if r.get(f) == op["from"]:
                        r[f] = op["to"]
                        matched += 1
                        if len(samples) < 2:
                            samples.append(f"{f}: {op['from']} -> {op['to']}")
        elif op["op"] == "insert":
            key = op["unique_by"]
            fields = [key] if isinstance(key, str) else key
            taken = {f: op["row"][f] for f in fields}
            if any(all(r.get(f) == v for f, v in taken.items())
                   for i, r in enumerate(rows) if i not in dropped):
                raise ApplyError(
                    "insert: " + ", ".join(f"{f}={v!r}" for f, v in taken.items())
                    + " is already in the file; an insert adds a row that is not "
                    "there, and this one is")
            rows.append({f: op["row"].get(f, "") for f in sidecar.fieldnames})
            matched = 1
            samples = [", ".join(f"{f}={v}" for f, v in taken.items())]
        elif op["op"] == "drop":
            for i, r in enumerate(rows):
                if i in dropped:
                    continue
                if all(r.get(k) == v for k, v in op["match"].items()):
                    dropped.add(i)
                    matched += 1
                    if len(samples) < 2:
                        samples.append(", ".join(f"{k}={v}" for k, v in op["match"].items()))
        else:
            # A citation repeats the pair it cites. Rewriting it by substring is
            # not safe -- "Bogoljubow, Efim" contains "Bogoljubow," -- so the
            # rewrite is anchored instead: the prefix the row used to carry,
            # replaced by the one it carries now, at position zero or not at all.
            a, b = op["pair_fields"]
            sep, fld = op["separator"], op["field"]
            for i, r in enumerate(rows):
                if i in dropped or i >= len(sidecar.rows):
                    continue          # a row inserted by this manifest has no "before"
                was = f'{sidecar.rows[i].get(a, "")}{sep}{sidecar.rows[i].get(b, "")}'
                now = f'{r.get(a, "")}{sep}{r.get(b, "")}'
                cite = r.get(fld) or ""
                if not cite.startswith(was):
                    raise ApplyError(
                        f"row {i + 1}: {fld} does not begin with its own "
                        f"{a}{sep}{b}; sync_prefix assumes it always does, and "
                        "that assumption no longer holds for this file")
                if was != now:
                    r[fld] = now + cite[len(was):]
                    matched += 1
                    if len(samples) < 2:
                        samples.append(f"{was} -> {now}")
        if matched != op["expected_rows"]:
            raise ApplyError(
                f"operation {op['op']} declared {op['expected_rows']} rows but "
                f"matched {matched}; refusing to apply a manifest that does not "
                "describe this file")
        results.append(OpResult(op, matched, samples))

    kept = [r for i, r in enumerate(rows) if i not in dropped]
    text = serialize(sidecar.fieldnames, kept)
    return ApplyResult(
        rows_before=len(sidecar.rows), rows_after=len(kept), ops=results,
        text=text, sha_before=sidecar.sha256,
        sha_after=hashlib.sha256(text.encode("utf-8")).hexdigest())


def check_referential(text: str, catalog_path: Path) -> tuple[int, list[str]]:
    """Every ocn1 in the result must still name a row of the catalogue."""
    with catalog_path.open(newline="", encoding="utf-8") as fh:
        known = {r["ocn1"] for r in csv.DictReader(fh)}
    reader = csv.DictReader(text.splitlines(), delimiter="\t")
    if "ocn1" not in (reader.fieldnames or []):
        return 0, []
    missing = sorted({r["ocn1"] for r in reader if r["ocn1"] not in known})
    return len(known), missing


# ---------------------------------------------------------------- report


def report_markdown(manifest: dict, res: ApplyResult, target: Path) -> str:
    out = [f"# Sidecar manifest — {manifest['title']}", "",
           f"- kind: `{manifest['kind']}`",
           f"- target: `{target}`",
           f"- rows: {res.rows_before} -> {res.rows_after}",
           f"- sha256 before: `{res.sha_before}`",
           f"- sha256 after:  `{res.sha_after}`", "", "## Operations", ""]
    for r in res.ops:
        op = r.op
        if op["op"] == "rename":
            head = f"`{op['from']}` -> `{op['to']}` in {', '.join(op['fields'])}"
        elif op["op"] == "drop":
            head = "drop " + ", ".join(f"{k}={v!r}" for k, v in op["match"].items())
        elif op["op"] == "insert":
            key = op["unique_by"]
            fields = [key] if isinstance(key, str) else key
            head = "insert " + ", ".join(f"{f}=`{op['row'][f]}`" for f in fields)
        else:
            head = (f"re-anchor `{op['field']}` on "
                    f"{op['separator'].join(op['pair_fields'])}")
        qid = f" ({op['wikidata_qid']})" if op.get("wikidata_qid") else ""
        out.append(f"### {head}{qid}")
        out.append(f"- rows: {r.matched}")
        out.append(f"- evidence: {op['evidence']}")
        out.append("")
    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description="Apply an OCN chronicle-sidecar manifest (dry-run by default).")
    p.add_argument("--manifest", required=True, type=Path)
    p.add_argument("--target", type=Path,
                   help="Override the manifest's target path.")
    p.add_argument("--dry-run", action="store_true",
                   help="Default behaviour: compute and report, write nothing.")
    p.add_argument("--apply", action="store_true",
                   help="Write the result to --out (required with --apply).")
    p.add_argument("--out", type=Path)
    p.add_argument("--report", "--format", dest="report",
                   choices=("markdown", "json"), default="markdown")
    p.add_argument("--catalog", type=Path, default=Path("catalog/ocn-1.csv"))
    p.add_argument("--check-referential", action="store_true",
                   help="Confirm every ocn1 in the result exists in the catalogue.")
    args = p.parse_args(argv)

    if args.apply and args.out is None:
        print("--apply requires --out", file=sys.stderr)
        return 2

    try:
        manifest = load_manifest(args.manifest)
        target = args.target or Path(manifest["target"])
        res = apply(manifest, load_sidecar(target))
        if args.check_referential:
            n, missing = check_referential(res.text, args.catalog)
            if missing:
                raise ApplyError(
                    f"{len(missing)} ocn1 value(s) in the result are not in the "
                    f"catalogue: {', '.join(missing[:5])}")
    except ApplyError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.report == "json":
        print(json.dumps({
            "target": str(target), "rows_before": res.rows_before,
            "rows_after": res.rows_after, "sha256_before": res.sha_before,
            "sha256_after": res.sha_after,
            "operations": [{"op": r.op["op"], "rows": r.matched} for r in res.ops],
        }, indent=2))
    else:
        print(report_markdown(manifest, res, target))

    if args.apply:
        args.out.write_text(res.text, encoding="utf-8")
        print(f"\nWROTE {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
