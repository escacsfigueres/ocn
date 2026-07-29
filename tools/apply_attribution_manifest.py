#!/usr/bin/env python3
"""Apply an attribution/naming manifest to the OCN-1 catalogue — safely.

This is the executable form of step 4 of the naming/attribution loop in
`docs/naming-attribution-automation.md`: an evidence sprint produces a small,
homogeneous, CLEAR batch; that batch is written as a JSON manifest; this tool
validates the manifest against the live catalogue, shows exactly what would
change, and only writes when explicitly told to with `--apply --out`.

The whole point is to stop hand-editing a 5,899-row CSV. The guardrails:

- **Dry-run by default.** Nothing is written unless `--apply` AND `--out` are
  both given. A dry-run never touches the catalogue or any other file.
- **Four safety modes** restrict which columns a manifest may change:
    `attribution_fields_only` -> attributed_to, attribution_source, historical_notes
    `naming_strings_only`     -> canonical_name, aliases, notes, + the three above
    `eco_legacy_only`         -> eco_legacy, alone (audit P1 item 8)
    `aliases_only`            -> aliases, alone (roadmap H2.6 editorial pass)
  Every other column (ocn1, moves_uci, parent_ocn1, depth, transposes_to,
  same_as, flags) is structural and cannot be touched here.
- **Exact-change contract.** The set of rows that actually change must equal
  the manifest's `expected_changed_rows` — so a stale, already-applied, or
  no-op manifest is rejected, not silently no-opped.
- **Zero collateral diff.** Untouched rows are emitted byte-for-byte from the
  source; only the rows the manifest changes are re-serialised. The tool
  *cannot* alter a row it did not target.
- **Invariant preservation.** A non-empty `attributed_to` must travel with a
  non-empty `attribution_source` (the hard rule in validate.py); we refuse to
  write a catalogue that validate.py would then reject.

Usage:
    python3 tools/apply_attribution_manifest.py --manifest M.json [--catalog C.csv]
        [--dry-run] [--apply --out OUT.csv] [--report markdown|json] [--strict] [--validate]

Exit codes: 0 success, 1 manifest/catalogue rejection or validation failure,
2 usage error (e.g. --apply without --out).
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

try:
    from validate import REQUIRED_COLUMNS
except ImportError:  # pragma: no cover - only for unusual direct imports.
    from tools.validate import REQUIRED_COLUMNS

TOOLS_DIR = Path(__file__).resolve().parent
VALIDATE_PY = TOOLS_DIR / "validate.py"
DEFAULT_CATALOG = TOOLS_DIR.parent / "catalog" / "ocn-1.csv"

MANIFEST_KIND = "ocn.attribution_manifest.v1"

# Field whitelists per safety mode. Anything not listed here (including every
# structural column and any unknown field name) is rejected.
MODE_ALLOWED_FIELDS = {
    "attribution_fields_only": frozenset(
        {"attributed_to", "attribution_source", "historical_notes"}
    ),
    "naming_strings_only": frozenset(
        {
            "canonical_name",
            "aliases",
            "notes",
            "attributed_to",
            "attribution_source",
            "historical_notes",
        }
    ),
    # ECO corrections travel alone: a wrong eco_legacy is a classification
    # bug, and bundling it with naming/attribution edits would blur the
    # blast radius of both lots.
    "eco_legacy_only": frozenset({"eco_legacy"}),
    # Alias-only editing (roadmap H2.6). The editorial passes over the
    # alias column — deleting synthetic strings, adding spelling variants,
    # resolving name collisions — touch thousands of rows at once. Running
    # them under `naming_strings_only` would leave canonical_name and notes
    # inside the blast radius of a lot that has no business changing a
    # name; this mode makes "aliases and nothing else" a checkable
    # property of the manifest rather than a promise in its description.
    "aliases_only": frozenset({"aliases"}),
}

REQUIRED_TOP_LEVEL = (
    "kind",
    "title",
    "mode",
    "expected_catalog_rows",
    "expected_changed_rows",
    "changes",
)
OPTIONAL_TOP_LEVEL = ("description",)
REQUIRED_CHANGE_KEYS = ("ocn1", "evidence_grade", "source_refs", "fields")
CLEAR_GRADE = "CLEAR"


class ApplyError(Exception):
    """A manifest or catalogue was rejected. main() turns this into exit 1."""


def warn(msg: str) -> None:
    print(f"WARN:  {msg}", file=sys.stderr)


# --------------------------------------------------------------------------- #
# Manifest loading + structural validation (no catalogue needed)
# --------------------------------------------------------------------------- #
def validate_manifest(obj: object) -> None:
    if not isinstance(obj, dict):
        raise ApplyError("manifest must be a JSON object")

    keys = set(obj)
    unknown = keys - set(REQUIRED_TOP_LEVEL) - set(OPTIONAL_TOP_LEVEL)
    if unknown:
        raise ApplyError(
            f"unknown manifest key(s): {', '.join(sorted(unknown))}. "
            f"Allowed: {', '.join(REQUIRED_TOP_LEVEL + OPTIONAL_TOP_LEVEL)}"
        )
    missing = set(REQUIRED_TOP_LEVEL) - keys
    if missing:
        raise ApplyError(f"missing manifest key(s): {', '.join(sorted(missing))}")

    if obj["kind"] != MANIFEST_KIND:
        raise ApplyError(
            f"unknown manifest kind {obj['kind']!r}; expected {MANIFEST_KIND!r}"
        )
    if not isinstance(obj["title"], str) or not obj["title"].strip():
        raise ApplyError("manifest 'title' must be a non-empty string")

    mode = obj["mode"]
    if mode not in MODE_ALLOWED_FIELDS:
        raise ApplyError(
            f"unknown safety mode {mode!r}; must be one of "
            f"{', '.join(sorted(MODE_ALLOWED_FIELDS))}"
        )
    allowed = MODE_ALLOWED_FIELDS[mode]

    rows = obj["expected_catalog_rows"]
    if isinstance(rows, bool) or not isinstance(rows, int) or rows <= 0:
        raise ApplyError("'expected_catalog_rows' must be a positive integer")

    expected_changed = obj["expected_changed_rows"]
    if not isinstance(expected_changed, list) or not all(
        isinstance(s, str) for s in expected_changed
    ):
        raise ApplyError("'expected_changed_rows' must be a list of slug strings")
    if len(expected_changed) != len(set(expected_changed)):
        raise ApplyError("'expected_changed_rows' contains duplicate slugs")

    changes = obj["changes"]
    if not isinstance(changes, list):
        raise ApplyError("'changes' must be a list")

    change_slugs: list[str] = []
    for i, change in enumerate(changes):
        where = f"changes[{i}]"
        if not isinstance(change, dict):
            raise ApplyError(f"{where} must be an object")
        ckeys = set(change)
        c_unknown = ckeys - set(REQUIRED_CHANGE_KEYS)
        if c_unknown:
            raise ApplyError(f"{where} has unknown key(s): {', '.join(sorted(c_unknown))}")
        c_missing = set(REQUIRED_CHANGE_KEYS) - ckeys
        if c_missing:
            raise ApplyError(f"{where} missing key(s): {', '.join(sorted(c_missing))}")

        slug = change["ocn1"]
        if not isinstance(slug, str) or not slug.strip():
            raise ApplyError(f"{where} 'ocn1' must be a non-empty string")
        change_slugs.append(slug)

        if not isinstance(change["evidence_grade"], str) or not change["evidence_grade"].strip():
            raise ApplyError(f"{where} 'evidence_grade' must be a non-empty string")
        refs = change["source_refs"]
        if not isinstance(refs, list) or not all(isinstance(r, str) for r in refs):
            raise ApplyError(f"{where} 'source_refs' must be a list of strings")

        fields = change["fields"]
        if not isinstance(fields, dict) or not fields:
            raise ApplyError(f"{where} 'fields' must be a non-empty object")
        for key, value in fields.items():
            if key not in REQUIRED_COLUMNS:
                raise ApplyError(f"{where} field {key!r} is not a catalogue column")
            if key not in allowed:
                raise ApplyError(
                    f"{where} field {key!r} is not permitted in mode {mode!r}. "
                    f"Allowed: {', '.join(sorted(allowed))}"
                )
            if not isinstance(value, str):
                raise ApplyError(f"{where} field {key!r} value must be a string")

    dupes = sorted({s for s in change_slugs if change_slugs.count(s) > 1})
    if dupes:
        raise ApplyError(f"duplicate slug(s) in changes: {', '.join(dupes)}")

    if set(change_slugs) != set(expected_changed):
        only_changes = sorted(set(change_slugs) - set(expected_changed))
        only_expected = sorted(set(expected_changed) - set(change_slugs))
        detail = []
        if only_changes:
            detail.append(f"in changes but not expected_changed_rows: {', '.join(only_changes)}")
        if only_expected:
            detail.append(f"in expected_changed_rows but not changes: {', '.join(only_expected)}")
        raise ApplyError("manifest slug sets disagree — " + "; ".join(detail))


def load_manifest(path: Path) -> dict:
    if not path.exists():
        raise ApplyError(f"manifest not found: {path}")
    try:
        obj = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ApplyError(f"manifest is not valid JSON: {exc}")
    validate_manifest(obj)
    return obj


# --------------------------------------------------------------------------- #
# Catalogue loading with raw-line preservation
# --------------------------------------------------------------------------- #
@dataclass
class Catalog:
    header: str
    fieldnames: list[str]
    rows: list[dict]
    raw_lines: list[str]  # data lines, no trailing newline, aligned to rows
    trailing_newline: bool
    raw_bytes: bytes


def load_catalog(path: Path) -> Catalog:
    if not path.exists():
        raise ApplyError(f"catalogue not found: {path}")
    raw_bytes = path.read_bytes()
    raw = raw_bytes.decode("utf-8")
    if "\r" in raw:
        raise ApplyError(
            "catalogue uses CR/CRLF line endings; this tool preserves LF-only files"
        )

    with io.StringIO(raw, newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)
    if fieldnames != list(REQUIRED_COLUMNS):
        raise ApplyError(
            "catalogue header does not match the canonical 14-column schema "
            f"(got {fieldnames})"
        )

    trailing_newline = raw.endswith("\n")
    segments = raw.split("\n")
    if trailing_newline:
        segments = segments[:-1]
    if not segments:
        raise ApplyError("catalogue is empty")
    header, data_lines = segments[0], segments[1:]
    if len(data_lines) != len(rows):
        raise ApplyError(
            f"catalogue line count ({len(data_lines)}) does not match parsed row "
            f"count ({len(rows)}); embedded newlines are unsupported"
        )
    return Catalog(
        header=header,
        fieldnames=fieldnames,
        rows=rows,
        raw_lines=data_lines,
        trailing_newline=trailing_newline,
        raw_bytes=raw_bytes,
    )


# --------------------------------------------------------------------------- #
# Apply (planning) — pure: computes the result without writing anything
# --------------------------------------------------------------------------- #
@dataclass
class ApplyResult:
    kind: str
    title: str
    mode: str
    catalog_path: str
    input_rows: int
    output_rows: int
    sha_before: str
    sha_after: str
    changed: list = field(default_factory=list)
    warnings: list = field(default_factory=list)
    output_text: str = ""
    validation: dict | None = None


def serialize_row(row: dict, fieldnames: list[str]) -> str:
    buf = io.StringIO()
    writer = csv.writer(buf, lineterminator="\n")
    writer.writerow([row[name] for name in fieldnames])
    line = buf.getvalue()
    return line[:-1] if line.endswith("\n") else line


def apply(manifest: dict, catalog: Catalog, *, catalog_path: str = "",
          strict: bool = False) -> ApplyResult:
    mode = manifest["mode"]
    expected_rows = manifest["expected_catalog_rows"]
    expected_changed = set(manifest["expected_changed_rows"])
    changes = manifest["changes"]
    warnings: list[str] = []

    if len(catalog.rows) != expected_rows:
        raise ApplyError(
            f"expected {expected_rows} catalogue rows but found {len(catalog.rows)}; "
            f"the manifest may be stale"
        )

    slug_to_index = {row["ocn1"]: i for i, row in enumerate(catalog.rows)}

    for change in changes:
        slug = change["ocn1"]
        if slug not in slug_to_index:
            raise ApplyError(f"slug {slug!r} in changes does not exist in the catalogue")
        if strict:
            if change["evidence_grade"] != CLEAR_GRADE:
                raise ApplyError(
                    f"--strict: change for {slug!r} has evidence_grade "
                    f"{change['evidence_grade']!r}; only {CLEAR_GRADE!r} may be applied"
                )
            if not change["source_refs"]:
                raise ApplyError(f"--strict: change for {slug!r} has no source_refs")

    new_rows = [dict(row) for row in catalog.rows]
    changed_indices: set[int] = set()
    changed_entries: list[dict] = []

    for change in changes:
        idx = slug_to_index[change["ocn1"]]
        target = new_rows[idx]
        for key, value in change["fields"].items():
            target[key] = value

        diffs = {
            col: [catalog.rows[idx][col], new_rows[idx][col]]
            for col in catalog.fieldnames
            if catalog.rows[idx][col] != new_rows[idx][col]
        }
        if diffs:
            changed_indices.add(idx)
            changed_entries.append(
                {
                    "ocn1": change["ocn1"],
                    "evidence_grade": change["evidence_grade"],
                    "source_refs": list(change["source_refs"]),
                    "diffs": diffs,
                }
            )

    actual_changed = {entry["ocn1"] for entry in changed_entries}
    if actual_changed != expected_changed:
        no_change = sorted(expected_changed - actual_changed)
        surprise = sorted(actual_changed - expected_changed)
        detail = []
        if no_change:
            detail.append(
                f"expected to change but did not (no-op / already applied): "
                f"{', '.join(no_change)}"
            )
        if surprise:
            detail.append(f"changed unexpectedly: {', '.join(surprise)}")
        raise ApplyError("changed rows do not match expected_changed_rows — "
                         + "; ".join(detail))

    # Preserve the validate.py invariant: attributed_to needs attribution_source.
    for idx in changed_indices:
        row = new_rows[idx]
        attributed = (row["attributed_to"] or "").strip()
        source = (row["attribution_source"] or "").strip()
        if attributed and not source:
            raise ApplyError(
                f"slug {row['ocn1']!r} would have attributed_to without "
                f"attribution_source; every attribution must cite a source"
            )
        if source and not attributed:
            warnings.append(
                f"slug {row['ocn1']!r} has attribution_source without "
                f"attributed_to (orphan citation)"
            )

    out_segments = [catalog.header]
    for i in range(len(catalog.rows)):
        if i in changed_indices:
            out_segments.append(serialize_row(new_rows[i], catalog.fieldnames))
        else:
            out_segments.append(catalog.raw_lines[i])
    output_text = "\n".join(out_segments)
    if catalog.trailing_newline:
        output_text += "\n"

    output_rows = len(out_segments) - 1
    if output_rows != len(catalog.rows):
        raise ApplyError(
            f"internal error: row count changed ({len(catalog.rows)} -> {output_rows})"
        )

    return ApplyResult(
        kind=manifest["kind"],
        title=manifest["title"],
        mode=mode,
        catalog_path=catalog_path,
        input_rows=len(catalog.rows),
        output_rows=output_rows,
        sha_before=hashlib.sha256(catalog.raw_bytes).hexdigest(),
        sha_after=hashlib.sha256(output_text.encode("utf-8")).hexdigest(),
        changed=changed_entries,
        warnings=warnings,
        output_text=output_text,
    )


def plan(manifest_path: Path, catalog_path: Path, *, strict: bool = False) -> ApplyResult:
    """Load + validate a manifest against a catalogue and compute the result."""
    manifest = load_manifest(Path(manifest_path))
    catalog = load_catalog(Path(catalog_path))
    return apply(manifest, catalog, catalog_path=str(catalog_path), strict=strict)


# --------------------------------------------------------------------------- #
# Optional integration with validate.py (subprocess, never refactors it)
# --------------------------------------------------------------------------- #
def run_external_validation(output_text: str, *, strict_chess: bool) -> tuple[bool, str]:
    with tempfile.TemporaryDirectory() as d:
        candidate = Path(d) / "candidate.csv"
        candidate.write_text(output_text, encoding="utf-8")
        cmd = [sys.executable, str(VALIDATE_PY)]
        if strict_chess:
            cmd.append("--strict-chess")
        cmd.append(str(candidate))
        proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    detail = (proc.stdout + proc.stderr).strip()
    return proc.returncode == 0, detail


# --------------------------------------------------------------------------- #
# Reporting
# --------------------------------------------------------------------------- #
def render_report(result: ApplyResult, *, fmt: str) -> str:
    if fmt == "json":
        payload = {
            "kind": result.kind,
            "title": result.title,
            "mode": result.mode,
            "catalog": result.catalog_path,
            "input_rows": result.input_rows,
            "output_rows": result.output_rows,
            "sha_before": result.sha_before,
            "sha_after": result.sha_after,
            "changed": result.changed,
            "warnings": result.warnings,
            "validation": result.validation,
        }
        return json.dumps(payload, ensure_ascii=False, indent=2)

    lines = [
        f"# Attribution manifest — {result.title}",
        "",
        f"- kind: `{result.kind}`",
        f"- mode: `{result.mode}`",
        f"- catalogue: `{result.catalog_path}`",
        f"- rows: {result.input_rows} -> {result.output_rows}",
        f"- sha256 before: `{result.sha_before}`",
        f"- sha256 after:  `{result.sha_after}`",
        f"- rows changed: {len(result.changed)}",
        "",
        "## Changes",
        "",
    ]
    if not result.changed:
        lines.append("_No changes._")
    for entry in result.changed:
        lines.append(f"### `{entry['ocn1']}` (evidence: {entry['evidence_grade']})")
        if entry["source_refs"]:
            lines.append(f"- sources: {'; '.join(entry['source_refs'])}")
        for col, (old, new) in entry["diffs"].items():
            lines.append(f"- `{col}`: {old!r} -> {new!r}")
        lines.append("")
    if result.warnings:
        lines.append("## Warnings")
        lines.append("")
        lines.extend(f"- {w}" for w in result.warnings)
        lines.append("")
    if result.validation is not None:
        status = "PASS" if result.validation.get("ok") else "FAIL"
        lines.append(f"## Validation: {status}")
        lines.append("")
        lines.append("```")
        lines.append(result.validation.get("detail", "").strip())
        lines.append("```")
    return "\n".join(lines)


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Apply an OCN attribution/naming manifest (dry-run by default)."
    )
    parser.add_argument("--manifest", type=Path, required=True,
                        help="Path to the JSON manifest to apply.")
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG,
                        help="Catalogue CSV (default: catalog/ocn-1.csv).")
    parser.add_argument("--dry-run", action="store_true",
                        help="Default behaviour: compute and report, write nothing.")
    parser.add_argument("--apply", action="store_true",
                        help="Write the result to --out (required with --apply).")
    parser.add_argument("--out", type=Path, default=None,
                        help="Output CSV path; required with --apply.")
    parser.add_argument("--report", "--format", choices=("markdown", "json"),
                        default="markdown",
                        help="Report format written to stdout "
                             "(--format is an alias, matching the other tools).")
    parser.add_argument("--strict", action="store_true",
                        help="Only apply CLEAR, sourced changes.")
    parser.add_argument("--validate", action="store_true",
                        help="Run validate.py on the result; abort apply on failure.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(sys.argv[1:] if argv is None else argv)

    if args.dry_run and args.apply:
        parser.error("--dry-run and --apply are mutually exclusive")
    if args.apply and args.out is None:
        parser.error("--apply requires --out PATH")
    if args.out is not None and not args.apply:
        warn("--out is ignored without --apply (dry-run writes nothing)")

    try:
        result = plan(args.manifest, args.catalog, strict=args.strict)
    except ApplyError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    for message in result.warnings:
        warn(message)

    if args.validate:
        ok, detail = run_external_validation(result.output_text, strict_chess=args.strict)
        result.validation = {"ran": True, "ok": ok, "detail": detail}
        if not ok:
            print(render_report(result, fmt=args.report))
            print("ERROR: validate.py rejected the result; not applying.", file=sys.stderr)
            return 1

    if args.apply:
        if args.out.resolve() == args.catalog.resolve():
            warn("--out targets the input catalogue; overwriting it in place.")
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(result.output_text, encoding="utf-8")

    print(render_report(result, fmt=args.report))
    return 0


if __name__ == "__main__":
    sys.exit(main())
