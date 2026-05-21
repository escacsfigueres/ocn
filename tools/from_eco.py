#!/usr/bin/env python3
"""Resolve an ECO code to OCN-1 catalogue rows.

ECO is coarse: a single code often covers multiple named OCN lines. By
default this tool returns the unique deepest row when one exists and
reports ambiguity when several rows tie at the deepest depth.
"""
from __future__ import annotations

import csv
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path


DEFAULT_CATALOG = Path(__file__).resolve().parent.parent / "catalog" / "ocn-1.csv"
ECO_RE = re.compile(r"^[A-E]\d{2}$", re.IGNORECASE)
ECO_TAG_RE = re.compile(r'\[ECO\s+"([A-E]\d{2})"\]', re.IGNORECASE)


@dataclass(frozen=True)
class Match:
    ocn1: str
    canonical_name: str
    eco_legacy: str
    depth: int
    moves_uci: str


def fail(message: str, *, code: int = 1) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(code)


def load_catalog(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        fail(f"catalogue not found: {path}")
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def extract_eco_from_pgn(text: str) -> str | None:
    match = ECO_TAG_RE.search(text)
    if match is None:
        return None
    return match.group(1).upper()


def normalize_eco(parts: list[str]) -> str:
    if not parts:
        fail("missing ECO code or PGN", code=2)

    if len(parts) == 1:
        candidate_path = Path(parts[0])
        if candidate_path.exists():
            eco = extract_eco_from_pgn(candidate_path.read_text(encoding="utf-8"))
            if eco is None:
                fail(f"no ECO tag found in PGN: {candidate_path}")
            return eco

    text = " ".join(parts).strip()
    tagged = extract_eco_from_pgn(text)
    if tagged is not None:
        return tagged

    eco = text.upper()
    if not ECO_RE.match(eco):
        fail(f"not a valid ECO code: {text!r}", code=2)
    return eco


def row_contains_eco(row: dict[str, str], eco: str) -> bool:
    return eco in [
        code.strip().upper()
        for code in (row.get("eco_legacy") or "").split("|")
    ]


def find_matches(rows: list[dict[str, str]], eco: str) -> list[Match]:
    matches = [
        Match(
            ocn1=row["ocn1"],
            canonical_name=row["canonical_name"],
            eco_legacy=row["eco_legacy"],
            depth=int(row["depth"]),
            moves_uci=(row.get("moves_uci") or "").strip(),
        )
        for row in rows
        if row_contains_eco(row, eco)
    ]
    return sorted(matches, key=lambda match: (-match.depth, match.ocn1))


def deepest_matches(matches: list[Match]) -> list[Match]:
    if not matches:
        return []
    depth = matches[0].depth
    return [match for match in matches if match.depth == depth]


def print_matches(matches: list[Match], *, json_output: bool) -> None:
    if json_output:
        print(
            json.dumps(
                [match.__dict__ for match in matches],
                ensure_ascii=False,
                sort_keys=True,
            )
        )
        return

    for match in matches:
        print(
            "\t".join(
                [
                    match.ocn1,
                    match.canonical_name,
                    match.eco_legacy,
                    str(match.depth),
                    match.moves_uci,
                ]
            )
        )


def main() -> int:
    args = sys.argv[1:]
    json_output = False
    if "--json" in args:
        json_output = True
        args.remove("--json")

    all_matches = False
    if "--all" in args:
        all_matches = True
        args.remove("--all")

    catalog = DEFAULT_CATALOG
    if "--catalog" in args:
        index = args.index("--catalog")
        try:
            catalog = Path(args[index + 1])
        except IndexError:
            fail("--catalog requires a path", code=2)
        del args[index:index + 2]

    if not args:
        fail(
            "usage: python3 tools/from_eco.py [--all] [--json] "
            "[--catalog path] <eco-code|pgn-file|pgn-text>",
            code=2,
        )

    eco = normalize_eco(args)
    matches = find_matches(load_catalog(catalog), eco)
    if not matches:
        fail(f"no OCN-1 match for ECO code {eco}")

    if all_matches:
        print_matches(matches, json_output=json_output)
        return 0

    top = deepest_matches(matches)
    if len(top) > 1:
        candidates = ", ".join(match.ocn1 for match in top[:8])
        suffix = "" if len(top) <= 8 else f", ... ({len(top)} total)"
        fail(
            f"ECO code {eco} is ambiguous at depth {top[0].depth}: "
            f"{candidates}{suffix}. Use --all or resolve by moves with tools/from_uci.py."
        )

    print_matches(top, json_output=json_output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
