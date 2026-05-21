#!/usr/bin/env python3
"""Map Lichess opening TSV rows to their deepest OCN-1 parent."""
from __future__ import annotations

import csv
import json
import sys
from dataclasses import dataclass
from pathlib import Path

try:
    from chess_uci import uci_sequence_from_pgn
    from from_uci import find_match, load_catalog
except ImportError:  # pragma: no cover - only for unusual direct imports.
    from tools.chess_uci import uci_sequence_from_pgn
    from tools.from_uci import find_match, load_catalog


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CATALOG = REPO_ROOT / "catalog" / "ocn-1.csv"
DEFAULT_LICHESS = REPO_ROOT / "external" / "lichess-openings"


@dataclass(frozen=True)
class MappedOpening:
    source: str
    eco: str
    name: str
    pgn: str
    moves_uci: str
    parent_ocn1: str
    parent_name: str
    parent_depth: int | None
    parent_matched_ply: int | None


def fail(message: str, *, code: int = 1) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(code)


def input_files(path: Path) -> list[Path]:
    if path.is_file():
        return [path]
    if path.is_dir():
        return sorted(path.glob("*.tsv"))
    fail(f"Lichess input not found: {path}")


def lichess_rows(path: Path) -> list[tuple[Path, dict[str, str]]]:
    rows: list[tuple[Path, dict[str, str]]] = []
    for file in input_files(path):
        with file.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter="\t")
            missing = {"eco", "name", "pgn"} - set(reader.fieldnames or [])
            if missing:
                fail(f"{file}: missing column(s): {', '.join(sorted(missing))}")
            rows.extend((file, row) for row in reader)
    return rows


def map_rows(
    rows: list[tuple[Path, dict[str, str]]],
    catalog: list[dict[str, str]],
    *,
    limit: int | None = None,
) -> tuple[list[MappedOpening], list[str]]:
    mapped: list[MappedOpening] = []
    errors: list[str] = []
    for file, row in rows[:limit]:
        pgn = row["pgn"].strip()
        try:
            moves_uci = uci_sequence_from_pgn(pgn)
        except ValueError as exc:
            errors.append(f"{file.name}: {row['name']}: {exc}")
            continue

        match = find_match(catalog, moves_uci)
        mapped.append(
            MappedOpening(
                source=file.name,
                eco=row["eco"],
                name=row["name"],
                pgn=pgn,
                moves_uci=moves_uci,
                parent_ocn1="" if match is None else match.ocn1,
                parent_name="" if match is None else match.canonical_name,
                parent_depth=None if match is None else match.depth,
                parent_matched_ply=None if match is None else match.matched_ply,
            )
        )
    return mapped, errors


def print_tsv(rows: list[MappedOpening]) -> None:
    fields = list(MappedOpening.__dataclass_fields__)
    writer = csv.DictWriter(sys.stdout, fieldnames=fields, delimiter="\t")
    writer.writeheader()
    for row in rows:
        writer.writerow(row.__dict__)


def print_summary(rows: list[MappedOpening], errors: list[str]) -> None:
    matched = sum(1 for row in rows if row.parent_ocn1)
    print(
        f"rows={len(rows)} matched={matched} "
        f"unmatched={len(rows) - matched} parse_errors={len(errors)}"
    )
    by_class: dict[str, int] = {}
    for row in rows:
        key = row.parent_ocn1[:1] if row.parent_ocn1 else "-"
        by_class[key] = by_class.get(key, 0) + 1
    print("by_parent_class=" + ",".join(f"{key}:{by_class[key]}" for key in sorted(by_class)))
    for error in errors[:10]:
        print(f"ERROR_SAMPLE: {error}", file=sys.stderr)


def coverage_status(rows: list[MappedOpening], errors: list[str]) -> tuple[int, int]:
    unmatched = sum(1 for row in rows if not row.parent_ocn1)
    return unmatched, len(errors)


def main() -> int:
    args = sys.argv[1:]
    json_output = False
    if "--json" in args:
        json_output = True
        args.remove("--json")

    summary = False
    if "--summary" in args:
        summary = True
        args.remove("--summary")

    check = False
    if "--check" in args:
        check = True
        args.remove("--check")

    limit: int | None = None
    if "--limit" in args:
        index = args.index("--limit")
        try:
            limit = int(args[index + 1])
        except (IndexError, ValueError):
            fail("--limit requires an integer", code=2)
        del args[index:index + 2]

    catalog_path = DEFAULT_CATALOG
    if "--catalog" in args:
        index = args.index("--catalog")
        try:
            catalog_path = Path(args[index + 1])
        except IndexError:
            fail("--catalog requires a path", code=2)
        del args[index:index + 2]

    input_path = Path(args[0]) if args else DEFAULT_LICHESS
    rows, errors = map_rows(
        lichess_rows(input_path),
        load_catalog(catalog_path),
        limit=limit,
    )

    if summary or check:
        print_summary(rows, errors)
    elif json_output:
        print(
            json.dumps(
                [row.__dict__ for row in rows],
                ensure_ascii=False,
                sort_keys=True,
            )
        )
    else:
        print_tsv(rows)

    unmatched, parse_errors = coverage_status(rows, errors)
    if check and (unmatched or parse_errors):
        print(
            f"ERROR: Lichess parent coverage check failed: "
            f"unmatched={unmatched} parse_errors={parse_errors}",
            file=sys.stderr,
        )
        return 1
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
