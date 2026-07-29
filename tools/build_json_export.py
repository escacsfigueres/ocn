#!/usr/bin/env python3
"""Build the whole-catalogue JSON export `ocn-1.json` (roadmap H1.2).

One file that a JS consumer, the web explorer, or a HuggingFace loader can
eat without a CSV parser, a pipe-splitter, or a chess engine. It carries
every `catalog/ocn-1.csv` column verbatim plus four derived conveniences:

- `moves_san` — the UCI line replayed through `tools/chess_uci.py` and
  rendered as numbered SAN (`1.e4 c5 2.Nf3`). Class roots have no moves and
  get `""`. This is the field consumers keep re-deriving badly; deriving it
  once, offline, at build time is the point of the artefact.
- `eco` — `eco_legacy` split on `|` into an array (`[]` when empty).
- `aliases_list`, `same_as_list`, `flags_list` — the same treatment for the
  other three pipe-packed columns.

The export is a **derived artefact and is never committed**: the canonical
source stays `catalog/ocn-1.csv`, and the JSON is built at release time and
attached to the release (`/ocn-1.json` is gitignored so a stray root build
cannot drift into the tree). Nothing here writes to the catalogue.

Output is deterministic: rows follow catalogue order, and every row object
uses the same fixed key order (the CSV columns as declared in the header,
then the derived fields in the order above), so two builds of the same
catalogue are byte-identical and a diff is a real change.

Usage:
    python3 tools/build_json_export.py --out ocn-1.json [--pretty]
        [--catalog catalog/ocn-1.csv] [--version ocn-1.2.0]

`--version` fills `catalog_version`; without it the tool reads the most
recent git tag, and falls back to `unknown` outside a git checkout.
"""
from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
from pathlib import Path

try:
    from chess_uci import validate_uci_sequence
except ImportError:  # pragma: no cover - only for unusual direct imports.
    from tools.chess_uci import validate_uci_sequence

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CATALOG = REPO_ROOT / "catalog" / "ocn-1.csv"

SCHEMA = "ocn.catalog.v1"
GENERATED_NOTE = "derived artefact, canonical source is catalog/ocn-1.csv"
UNKNOWN_VERSION = "unknown"

#: (source CSV column, derived array field) for the pipe-packed columns.
LIST_FIELDS = (
    ("aliases", "aliases_list"),
    ("same_as", "same_as_list"),
    ("flags", "flags_list"),
)


def moves_san(moves_uci: str) -> str:
    """Render a UCI move string as numbered SAN (`1.e4 c5 2.Nf3`).

    Empty in, empty out: the five class roots are filters, not positions,
    and carry no move sequence.
    """
    moves_uci = (moves_uci or "").strip()
    if not moves_uci:
        return ""
    tokens: list[str] = []
    for ply, san in enumerate(validate_uci_sequence(moves_uci)):
        tokens.append(f"{ply // 2 + 1}.{san}" if ply % 2 == 0 else san)
    return " ".join(tokens)


def split_pipe(value: str) -> list[str]:
    """Split a pipe-packed catalogue field into a list, empties dropped."""
    return [part.strip() for part in (value or "").split("|") if part.strip()]


def build_row(row: dict[str, str]) -> dict[str, object]:
    """One catalogue row as a JSON object: CSV columns then derived fields."""
    out: dict[str, object] = dict(row)
    out["moves_san"] = moves_san(row.get("moves_uci", ""))
    out["eco"] = split_pipe(row.get("eco_legacy", ""))
    for source, derived in LIST_FIELDS:
        out[derived] = split_pipe(row.get(source, ""))
    return out


def detect_version(repo_root: Path = REPO_ROOT) -> str:
    """Most recent git tag, or `unknown` outside a usable git checkout."""
    try:
        proc = subprocess.run(
            ["git", "describe", "--tags", "--abbrev=0"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            timeout=30,
        )
    except (OSError, subprocess.SubprocessError):  # pragma: no cover
        return UNKNOWN_VERSION
    tag = proc.stdout.strip()
    if proc.returncode != 0 or not tag:
        return UNKNOWN_VERSION
    return tag


def load_catalog(catalog: Path) -> list[dict[str, str]]:
    with catalog.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def build_document(
    catalog: Path = DEFAULT_CATALOG,
    version: str | None = None,
) -> dict[str, object]:
    return {
        "schema": SCHEMA,
        "catalog_version": version or detect_version(),
        "generated_note": GENERATED_NOTE,
        "rows": [build_row(row) for row in load_catalog(catalog)],
    }


def render_json(document: dict[str, object], pretty: bool = False) -> str:
    if pretty:
        text = json.dumps(document, ensure_ascii=False, indent=2)
    else:
        text = json.dumps(document, ensure_ascii=False, separators=(",", ":"))
    return text + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build the whole-catalogue OCN-1 JSON export."
    )
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    parser.add_argument("--out", type=Path, required=True,
                        help="Destination path for ocn-1.json.")
    parser.add_argument("--pretty", action="store_true",
                        help="Indent the JSON (larger, diff-friendly).")
    parser.add_argument("--version", default=None,
                        help="Value for catalog_version; defaults to the "
                             "most recent git tag.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(
        sys.argv[1:] if argv is None else argv
    )
    if not args.catalog.exists():
        print(f"ERROR: catalogue not found: {args.catalog}", file=sys.stderr)
        return 1

    document = build_document(args.catalog, args.version)
    args.out.write_text(render_json(document, args.pretty), encoding="utf-8")
    rows = document["rows"]
    assert isinstance(rows, list)
    print(
        f"wrote {args.out} ({len(rows)} rows, "
        f"catalog_version {document['catalog_version']})"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
