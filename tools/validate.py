#!/usr/bin/env python3
"""Validate the OCN-1 catalogue against the spec.

Checks performed:

1. Every row's `ocn1` matches the format `<A-E>(\\.[A-Za-z0-9-]+)*`.
2. The first segment of every slug is a valid class (A/B/C/D/E) — except
   the class roots themselves, which are exactly that single letter.
3. Each non-root entry has a `parent_ocn1` that exists in the catalogue
   and that has a `depth` exactly one less than this entry's depth.
4. `depth` matches `slug.count('.')`.
5. No two rows share the same `ocn1` (uniqueness).
6. Maximum depth is 6 (i.e. at most 6 dots, 7 segments).
7. `eco_legacy` codes (when present) match the `[A-E]\\d{2}` pattern.
8. Family/variation/subline segments are 3 characters by default; longer
   tokens are allowed only if explicitly listed in `KNOWN_LONG_TOKENS`
   (handful of legacy compounds like `KID`, `QGD`, `RyL`).
9. With `--strict-chess`, every `moves_uci` sequence must be legal chess
   from the initial position, and one-move child extensions with SAN-like
   trailing slugs must match the appended move's SAN.

Exits with code 0 on success, 1 on the first error encountered.

Usage:
    python3 tools/validate.py [--strict-chess] [catalog/ocn-1.csv]
"""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

try:
    from chess_uci import last_move_san, validate_uci_sequence
except ImportError:  # pragma: no cover - only for unusual direct imports.
    from tools.chess_uci import last_move_san, validate_uci_sequence

DEFAULT_CATALOG = Path(__file__).resolve().parent.parent / "catalog" / "ocn-1.csv"

# Slug character set: alphanumerics + `=` for promotion + `-` for O-O / O-O-O.
# `+` (check) and `#` (mate) are NOT part of OCN slugs — they describe a
# move event, not a variation, so they would be redundant here.
SLUG_RE = re.compile(r"^[A-E](?:\.[A-Za-z0-9_=-]+)*$")
ECO_RE = re.compile(r"^[A-E]\d{2}$")
# A SAN-like move-segment: castling, or a piece/file move with optional
# disambiguation, capture, target square and promotion.
SAN_RE = re.compile(
    r"^(O-O(?:-O)?|[NBRQK]?[a-h]?[1-8]?x?[a-h][1-8](?:=[NBRQ])?)$"
)
# A UCI move: from-square + to-square (+ optional promotion piece).
# e.g. e2e4, g1f3, e7e8q. Castling is encoded as the king's two-square move
# (e1g1 / e1c1 / e8g8 / e8c8).
UCI_RE = re.compile(r"^[a-h][1-8][a-h][1-8][nbrq]?$")

# Tokens that intentionally break the "3 characters" rule.
KNOWN_LONG_TOKENS = {
    # Established acronyms in chess literature.
    "KID", "QGD", "QGA", "QID", "NID", "OID", "RyL", "OldI", "AntM",
    "Cmb", "NoD5",
    # Generic openings that are themselves a class root + alias.
    # (single-letter top-level classes are matched separately)
}

ALLOWED_FLAGS = {
    "gambit", "sharp", "closed", "endgame", "theoretical", "deprecated",
}

REQUIRED_COLUMNS = [
    "ocn1",
    "canonical_name",
    "eco_legacy",
    "parent_ocn1",
    "moves_uci",
    "depth",
    "aliases",
    "flags",
    "notes",
    "attributed_to",
    "attribution_source",
    "historical_notes",
]


def fail(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def warn(msg: str) -> None:
    print(f"WARN:  {msg}", file=sys.stderr)


def normalize_san(san: str) -> str:
    return san.rstrip("+#")


def validate(path: Path, *, strict_chess: bool = False) -> None:
    if not path.exists():
        fail(f"catalogue not found: {path}")

    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        missing_columns = [
            column for column in REQUIRED_COLUMNS
            if column not in (reader.fieldnames or [])
        ]
        if missing_columns:
            fail(f"catalogue missing required column(s): {', '.join(missing_columns)}")
        rows = list(reader)

    seen_slugs: dict[str, dict] = {}
    warnings = 0

    for i, row in enumerate(rows, start=2):  # start=2 to align with CSV row numbers (header is row 1)
        slug = (row.get("ocn1") or "").strip()
        if not slug:
            fail(f"row {i}: missing ocn1")

        # 1. Format
        if not SLUG_RE.match(slug):
            fail(f"row {i}: slug '{slug}' does not match format")

        # 5. Uniqueness
        if slug in seen_slugs:
            fail(f"row {i}: duplicate slug '{slug}' (also at row "
                 f"{seen_slugs[slug]['_row']})")
        row["_row"] = i
        seen_slugs[slug] = row

        # 4. Depth matches dots
        try:
            depth = int(row.get("depth", "").strip())
        except ValueError:
            fail(f"row {i}: depth not an integer for slug '{slug}'")
        expected_depth = slug.count(".")
        if depth != expected_depth:
            fail(f"row {i}: slug '{slug}' has {expected_depth} dots but depth={depth}")

        # 6. Maximum depth
        if depth > 6:
            fail(f"row {i}: slug '{slug}' exceeds maximum depth of 6 dots")

        # 2. Class root rule
        segments = slug.split(".")
        if depth == 0:
            if segments[0] not in {"A", "B", "C", "D", "E"}:
                fail(f"row {i}: class root '{slug}' is not A/B/C/D/E")

        # 8. Segment length policy + position-aware SAN tail.
        #
        # The grammar is: class . named+ ( . san_move )*
        # i.e. the slug starts with the class root, must include at
        # least one *named* segment (3-char token or KNOWN_LONG_TOKEN)
        # before any SAN move tail can begin, and once a SAN-only token
        # (e.g. `e4`, `Bxf6`, `O-O`) appears, every subsequent segment
        # must also parse as SAN. This rules out malformed slugs like
        # `A.e4` (move directly after class, no family named) and
        # `B.Sic.e4.Naj` (named segment after a move tail has started).
        #
        # 3-char tokens that happen to also be SAN (`Be3`, `Nd5`) are
        # treated as named when they appear in the named region — the
        # catalogue uses them as variation labels there.
        in_tail = False
        for seg_idx, seg in enumerate(segments):
            if seg_idx == 0:
                if seg not in {"A", "B", "C", "D", "E"}:
                    fail(f"row {i}: first segment '{seg}' must be A/B/C/D/E")
                continue
            if in_tail:
                if not SAN_RE.match(seg):
                    fail(f"row {i}: segment '{seg}' (slug '{slug}') is not SAN "
                         f"but follows a move tail — named tokens cannot reappear "
                         f"after the tail has started")
                if not (1 <= len(seg) <= 6):
                    fail(f"row {i}: move segment '{seg}' length out of range (1-6)")
                continue
            # We're still in the named region.
            if seg in KNOWN_LONG_TOKENS:
                continue
            if len(seg) == 3:
                # Named token (possibly SAN-shaped like `Be3`, `Nd5`).
                continue
            if SAN_RE.match(seg):
                # SAN-only move triggers the tail. Require at least one
                # named segment between the class and this point.
                if seg_idx == 1:
                    fail(f"row {i}: slug '{slug}' opens with SAN move '{seg}' "
                         f"immediately after the class — a named family segment "
                         f"is required first (e.g. `A.Eng.e4`, not `A.e4`)")
                if not (1 <= len(seg) <= 6):
                    fail(f"row {i}: move segment '{seg}' length out of range (1-6)")
                in_tail = True
                continue
            warn(f"row {i}: non-standard segment length: '{seg}' "
                 f"(in slug '{slug}'). Add to KNOWN_LONG_TOKENS if intentional.")
            warnings += 1

        # 7. ECO legacy format
        eco_legacy = (row.get("eco_legacy") or "").strip()
        if eco_legacy:
            for code in eco_legacy.split("|"):
                code = code.strip()
                if code and not ECO_RE.match(code):
                    warn(f"row {i}: ECO code '{code}' not in standard A00-E99 form "
                         f"(slug '{slug}')")
                    warnings += 1

        # 9. moves_uci format (when present): space-separated UCI tokens.
        moves_uci = (row.get("moves_uci") or "").strip()
        if moves_uci:
            if depth == 0:
                warn(f"row {i}: class root '{slug}' should not have moves_uci "
                     f"(it is a filter, not a position)")
                warnings += 1
            for tok in moves_uci.split():
                if not UCI_RE.match(tok):
                    fail(f"row {i}: invalid UCI move '{tok}' in slug '{slug}' "
                         f"(expected format like e2e4, g1f3, e7e8q)")
            if strict_chess:
                try:
                    validate_uci_sequence(moves_uci)
                except ValueError as exc:
                    fail(f"row {i}: {exc} in slug '{slug}'")

        # Flags whitelist (pipe-separated, same as eco_legacy and aliases)
        flags = (row.get("flags") or "").strip()
        if flags:
            for flag in flags.split("|"):
                flag = flag.strip()
                if flag and flag not in ALLOWED_FLAGS:
                    fail(f"row {i}: unknown flag '{flag}' (slug '{slug}'). "
                         f"Allowed: {sorted(ALLOWED_FLAGS)}")

        # 10. Attribution columns (Layer 2 metadata) — optional, but
        #     the contract is: any non-empty `attributed_to` MUST come
        #     paired with a non-empty `attribution_source`. We refuse
        #     unsourced historical claims so the catalogue is auditable
        #     by anyone who reads it later.
        attributed_to = (row.get("attributed_to") or "").strip()
        attribution_source = (row.get("attribution_source") or "").strip()
        if attributed_to and not attribution_source:
            fail(f"row {i}: slug '{slug}' has 'attributed_to' "
                 f"({attributed_to!r}) without 'attribution_source'. "
                 f"Every attribution must cite a source — fill the column "
                 f"or remove the claim.")
        if attribution_source and not attributed_to:
            warn(f"row {i}: slug '{slug}' has 'attribution_source' but "
                 f"empty 'attributed_to' — orphan citation, prefer to "
                 f"name the attributed party.")
            warnings += 1

    # 3. Parent existence and depth-1 rule (second pass)
    for slug, row in seen_slugs.items():
        depth = int(row["depth"])
        parent = (row.get("parent_ocn1") or "").strip()
        if depth == 0:
            if parent:
                fail(f"row {row['_row']}: class root '{slug}' should not have a parent "
                     f"(found '{parent}')")
            continue
        if not parent:
            fail(f"row {row['_row']}: slug '{slug}' has depth {depth} but no parent_ocn1")
        if parent not in seen_slugs:
            fail(f"row {row['_row']}: slug '{slug}' references missing parent '{parent}'")
        parent_depth = int(seen_slugs[parent]["depth"])
        if parent_depth != depth - 1:
            fail(f"row {row['_row']}: slug '{slug}' has depth {depth} but parent "
                 f"'{parent}' has depth {parent_depth} (expected {depth - 1})")

        # Parent prefix sanity: child's slug must start with parent + '.' (when depth >= 1).
        if not slug.startswith(parent + "."):
            fail(f"row {row['_row']}: slug '{slug}' does not start with parent '{parent}.'")

        if strict_chess:
            parent_moves = (seen_slugs[parent].get("moves_uci") or "").strip()
            child_moves = (row.get("moves_uci") or "").strip()
            last_segment = slug.rsplit(".", 1)[-1]
            if child_moves and SAN_RE.match(last_segment):
                try:
                    san = last_move_san(parent_moves, child_moves)
                except ValueError as exc:
                    fail(f"row {row['_row']}: {exc} in slug '{slug}'")
                if san is not None and normalize_san(san) != last_segment:
                    fail(f"row {row['_row']}: last slug segment '{last_segment}' "
                         f"does not match appended move SAN '{normalize_san(san)}' "
                         f"(slug '{slug}')")

    print(f"OK: {len(seen_slugs)} entries validated, {warnings} warning(s)")


def main() -> int:
    args = sys.argv[1:]
    strict_chess = False
    if "--strict-chess" in args:
        strict_chess = True
        args.remove("--strict-chess")
    if len(args) > 1:
        fail("usage: python3 tools/validate.py [--strict-chess] [catalog/ocn-1.csv]")
    path = Path(args[0]) if args else DEFAULT_CATALOG
    validate(path, strict_chess=strict_chess)
    return 0


if __name__ == "__main__":
    sys.exit(main())
