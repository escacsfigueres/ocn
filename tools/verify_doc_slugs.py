#!/usr/bin/env python3
"""Verify backtick-quoted OCN slugs in docs against the live catalogue.

Scans inline-code (single-backtick) tokens that have OCN slug shape and reports
any that do not exist in `catalog/ocn-1.csv`, so `docs/` stays a reliable
agent-context source. It deliberately does NOT false-positive on:

- ECO codes (`A45`), git hashes (`204eb07`), versions (`ocn-1.1.0`), CLI flags
  (`--strict`), filenames (`ocn-1.csv`), commands (`git push`) — none match the
  slug regex;
- field-accessor notation (`A.Tro.notes`) — last component is a catalogue column;
- slugs explicitly marked NON-CATALOGUE / pseudo-slug (looking back 2 lines, so
  the marker may sit on a preceding line).

Usage:
    python3 tools/verify_doc_slugs.py [--catalog catalog/ocn-1.csv]
        [--format text|json] PATH_OR_GLOB ...

Exit codes: 0 all verified, 1 missing slug(s) found OR zero files matched,
2 usage error.
"""
from __future__ import annotations

import argparse
import csv
import glob as globmod
import json
import re
import sys
from pathlib import Path

try:
    from validate import REQUIRED_COLUMNS
except ImportError:  # pragma: no cover
    from tools.validate import REQUIRED_COLUMNS

DEFAULT_CATALOG = Path(__file__).resolve().parent.parent / "catalog" / "ocn-1.csv"
BACKTICK_RE = re.compile(r"`([^`]+)`")           # non-greedy: each inline-code token
SLUG_RE = re.compile(r"^[A-E](?:\.[A-Za-z0-9_=-]+)*$")  # same shape as validate.py
KNOWN_FIELDS = set(REQUIRED_COLUMNS)
EXEMPT_MARKERS = ("NON-CATALOGUE", "pseudo-slug")
LOOKBACK = 2  # lines: current + 2 preceding may carry the exemption marker


def warn(msg: str) -> None:
    print(f"WARN:  {msg}", file=sys.stderr)


def is_field_accessor(token: str) -> bool:
    parts = token.split(".")
    return len(parts) > 1 and parts[-1] in KNOWN_FIELDS


def exempt(lines: list[str], idx: int) -> bool:
    start = max(0, idx - LOOKBACK)
    window = " ".join(lines[start: idx + 1])
    return any(marker in window for marker in EXEMPT_MARKERS)


def scan_file(path: Path, catalog: set[str]) -> list[dict]:
    violations = []
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    for i, line in enumerate(lines):
        for token in BACKTICK_RE.findall(line):
            if not SLUG_RE.match(token) or token in catalog:
                continue
            if is_field_accessor(token):
                continue
            if exempt(lines, i):
                continue
            violations.append({"file": str(path), "line": i + 1, "slug": token})
    return violations


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Verify backticked OCN slugs in docs.")
    p.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    p.add_argument("--format", choices=("text", "json"), default="text")
    p.add_argument("paths", nargs="+", help="files or globs, e.g. docs/*.md")
    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(sys.argv[1:] if argv is None else argv)

    if not args.catalog.exists():
        print(f"ERROR: catalogue not found: {args.catalog}", file=sys.stderr)
        return 1
    with args.catalog.open(newline="", encoding="utf-8") as f:
        catalog = {r["ocn1"] for r in csv.DictReader(f)}

    files: list[Path] = []
    seen = set()
    for pattern in args.paths:
        for match in globmod.glob(pattern):
            if match not in seen:
                seen.add(match)
                files.append(Path(match))
    if not files:
        warn(f"no files matched: {' '.join(args.paths)}")
        return 1

    violations = []
    for path in files:
        violations.extend(scan_file(path, catalog))

    if args.format == "json":
        print(json.dumps(violations, ensure_ascii=False, indent=2))
    else:
        for v in violations:
            print(f"{v['file']}:{v['line']}: stale slug `{v['slug']}`")

    if violations:
        warn(f"{len(violations)} stale slug reference(s) across {len(files)} file(s)")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
