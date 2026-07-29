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
10. Any non-empty `attributed_to` must cite an `attribution_source`
    (an orphan source without a party warns). Attribution fields must
    not cite unverifiable sources ("the corpus", "Gigabase", private
    databases) — published, publicly checkable evidence only
    (traction-roadmap H0.4).
11. `transposes_to` link contract: target exists, is not self or a class
    root, and FEN keys match when both rows carry moves.
12. `same_as` co-canonical contract: mutually exclusive with
    `transposes_to`; targets exist; FEN keys match.
13. Global `canonical_name` uniqueness; the three audit-pending duplicate
    pairs live in `DUPLICATE_NAME_ALLOWLIST` with pinned slug sets.
14. No banned characters in text columns: middle dot, invisible spacing
    characters, ASCII control characters.
15. Whitespace hygiene in text columns: no leading/trailing or doubled
    spaces.
16. No alias identical to the row's own canonical_name.
17. Diacritic regression guard: ASCII surname forms retired by the
    normalization lot (`BANNED_ASCII_NAME_FORMS`, extendable per run via
    `--ban-ascii-form ASCII=Normalized`) fail in canonical_name/aliases
    and warn in notes.
18. With `--audit-naming`, children whose canonical_name is shorter than
    their parent's warn — an audit-sweep heuristic (~1,400 legitimate
    hits on the live catalogue), never part of the default gate.
19. A child whose moves_uci is byte-identical to its parent's must carry
    the parent's eco_legacy (`PHANTOM_PAIR_ECO_ALLOWLIST` pins the two
    contradictions pending the phantom-pair decision).
20. With `--audit-eco`, children with a single same-class ECO code
    numerically below their parent's warn — audit-sweep heuristic (~55
    legitimate hits), never part of the default gate.
21. The committed ECO class-divergence sidecar
    (`catalog/ocn-1.eco-divergence.tsv`) must exist and must list exactly
    the rows whose OCN class letter is absent from their own ECO letters,
    recomputed here from the catalogue. Canonical catalogue only — the
    fixtures carry no sidecar (traction-roadmap H2.5).

Exits with code 0 on success, 1 on the first error encountered.

Usage:
    python3 tools/validate.py [--strict-chess] [--audit-naming]
        [--audit-eco] [--ban-ascii-form ASCII=Normalized ...]
        [catalog/ocn-1.csv]
"""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

try:
    from chess_uci import fen_key_after_uci, last_move_san, validate_uci_sequence
except ImportError:  # pragma: no cover - only for unusual direct imports.
    from tools.chess_uci import (
        fen_key_after_uci,
        last_move_san,
        validate_uci_sequence,
    )

DEFAULT_CATALOG = Path(__file__).resolve().parent.parent / "catalog" / "ocn-1.csv"
DIVERGENCE_SIDECAR = (
    Path(__file__).resolve().parent.parent / "catalog" / "ocn-1.eco-divergence.tsv"
)
# How many example slugs a divergence mismatch prints before eliding.
DIVERGENCE_EXAMPLE_CAP = 10

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

# Free-text columns, in schema order. Slug / moves / depth / link columns
# have their own format checks; these six are where prose lives.
TEXT_COLUMNS = [
    "canonical_name", "aliases", "notes",
    "attributed_to", "attribution_source", "historical_notes",
]

# Unverifiable-source patterns banned from attribution fields (roadmap
# H0.4): evidence must be published and publicly checkable. An unpublished
# game collection ("the corpus", "Gigabase") is not a citable source.
UNVERIFIABLE_SOURCE_RE = re.compile(
    r"\bcorpus\b|\bgigabase\b|\bprivate database\b", re.IGNORECASE)

# Characters that never belong in catalogue text: the middle dot
# (banned project-wide as a separator), invisible spacing characters,
# and ASCII control characters (tabs and newlines included — a field
# that needs one is a field that needs rewriting).
BANNED_CHAR_RE = re.compile(r"[· ​‌‍﻿\x00-\x1f\x7f]")
BANNED_CHAR_LABELS = {
    "·": "middle dot",
    " ": "no-break space",
    "​": "zero-width space",
    "‌": "zero-width non-joiner",
    "‍": "zero-width joiner",
    "﻿": "byte-order mark",
}

# Diacritic regression guard (see docs/diacritic-normalization-map.md).
# Maps a banned ASCII surname form -> its normalized spelling. Word-boundary
# match: error in canonical_name/aliases, warning in notes (notes may
# legitimately quote titles). Populated by the same commit that applied the
# Tier 1 normalization lot, so data and guard activated atomically; the
# entries mirror tools/generate_diacritic_manifest.py's Tier 1 map (a test
# pins them together). `--ban-ascii-form ASCII=Normalized` (repeatable)
# extends it ad hoc, e.g. to pre-check a candidate CSV for a future tier.
BANNED_ASCII_NAME_FORMS: dict[str, str] = {
    "Lopez": "López",
    "Grunfeld": "Grünfeld",
    "Gruenfeld": "Grünfeld",
    "Reti": "Réti",
    "Saemisch": "Sämisch",
    "Samisch": "Sämisch",
    "Maroczy": "Maróczy",
    "Goring": "Göring",
    "Goering": "Göring",
    "Hubner": "Hübner",
    "Huebner": "Hübner",
    "Lowenthal": "Löwenthal",
    "Loewenthal": "Löwenthal",
    "Hromadka": "Hromádka",
    "Moller": "Møller",
    "Moeller": "Møller",
    # Tier 2 (Czech/Lithuanian class), applied 2026-06-11.
    "Mikenas": "Mikėnas",
    "Krejcik": "Krejčík",
    "Opocensky": "Opočenský",
    "Pelikan": "Pelikán",
    # Tier 3 (Lichess xref discoveries), applied 2026-06-11.
    "Kadas": "Kádas",
    "Bucker": "Bücker",
    "Kostic": "Kostić",
    "Szen": "Szén",
    "Suchting": "Süchting",
    "Hubsch": "Hübsch",
    "Dory": "Döry",
    "Lohn": "Löhn",
    "Schonemann": "Schönemann",
    "Dusseldorf": "Düsseldorf",
    "Tubingen": "Tübingen",
}

# Canonical names temporarily allowed on more than one row, pending an
# explicit decision (each entry pins the exact slug set, so a NEW
# duplication of the same name still fails). EMPTY since 2026-06-11: the
# four audit pairs were resolved by the duplicate-name renames lot
# (docs/phantom-and-duplicate-name-decision.md).
DUPLICATE_NAME_ALLOWLIST: dict[str, frozenset[str]] = {}

# Phantom path-marker children whose eco_legacy disagrees with their
# parent, pinned pending a decision. EMPTY since 2026-06-11: the two
# contradictions were ECO-aligned under the approved decision record, and
# the spec now blesses path-markers that carry their parent's code.
PHANTOM_PAIR_ECO_ALLOWLIST: frozenset[str] = frozenset()

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
    "transposes_to",
    "same_as",
]


def fail(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def warn(msg: str) -> None:
    print(f"WARN:  {msg}", file=sys.stderr)


def normalize_san(san: str) -> str:
    return san.rstrip("+#")


def recompute_divergent_slugs(rows: list[dict]) -> set[str]:
    """Slugs whose OCN class letter is absent from their own ECO letters.

    A deliberate second implementation of the rule in
    `tools/build_eco_divergence.py`: the validator does not import the
    builder, so a bug in the builder cannot certify itself. Rows with no
    ECO code are not divergent — outside ECO's coverage there is no
    assignment to disagree with.
    """
    divergent: set[str] = set()
    for row in rows:
        slug = (row.get("ocn1") or "").strip()
        codes = [c.strip() for c in (row.get("eco_legacy") or "").split("|")
                 if c.strip()]
        if slug and codes and slug[:1] not in {code[:1] for code in codes}:
            divergent.add(slug)
    return divergent


def divergence_sidecar_problem(
    rows: list[dict],
    sidecar: Path = DIVERGENCE_SIDECAR,
) -> str | None:
    """Compare the committed divergence sidecar with the live catalogue.

    Returns an error message, or `None` when they agree exactly. Both
    directions matter: an *unlisted* slug means the published divergence
    count understates reality (the failure this sidecar exists to prevent),
    a *stale* slug means it overstates it.
    """
    if not sidecar.exists():
        return (f"ECO divergence sidecar not found: {sidecar} — build it with "
                f"python3 tools/build_eco_divergence.py")
    with sidecar.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        if "ocn1" not in (reader.fieldnames or []):
            return (f"ECO divergence sidecar {sidecar.name} has no 'ocn1' "
                    f"column (found: {reader.fieldnames})")
        listed = {(r.get("ocn1") or "").strip() for r in reader}
    listed.discard("")

    computed = recompute_divergent_slugs(rows)
    unlisted = sorted(computed - listed)
    stale = sorted(listed - computed)
    if not unlisted and not stale:
        return None

    def sample(slugs: list[str]) -> str:
        shown = ", ".join(slugs[:DIVERGENCE_EXAMPLE_CAP])
        return shown + (", ..." if len(slugs) > DIVERGENCE_EXAMPLE_CAP else "")

    parts = []
    if unlisted:
        parts.append(f"{len(unlisted)} unlisted (divergent in the catalogue, "
                     f"absent from the sidecar): {sample(unlisted)}")
    if stale:
        parts.append(f"{len(stale)} stale (listed in the sidecar, no longer "
                     f"divergent): {sample(stale)}")
    return (f"{sidecar.name} disagrees with the catalogue — "
            + "; ".join(parts)
            + ". Regenerate with python3 tools/build_eco_divergence.py")


def validate(
    path: Path,
    *,
    strict_chess: bool = False,
    extra_banned_forms: dict[str, str] | None = None,
    audit_naming: bool = False,
    audit_eco: bool = False,
) -> None:
    if not path.exists():
        fail(f"catalogue not found: {path}")

    banned_forms = {**BANNED_ASCII_NAME_FORMS, **(extra_banned_forms or {})}
    banned_form_re = re.compile(
        r"\b(" + "|".join(re.escape(f) for f in sorted(banned_forms)) + r")\b"
    ) if banned_forms else None

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

        # 14. Banned characters in text columns.
        # 15. Whitespace hygiene: leading/trailing whitespace or doubled
        #     spaces. Error since the naming-hygiene lot (2026-06-11)
        #     cleared the two historical offenders.
        for col in TEXT_COLUMNS:
            value = row.get(col) or ""
            hit = BANNED_CHAR_RE.search(value)
            if hit:
                ch = hit.group(0)
                label = BANNED_CHAR_LABELS.get(
                    ch, f"control character U+{ord(ch):04X}"
                )
                fail(f"row {i}: banned character ({label}) in {col} "
                     f"(slug '{slug}')")
            if value != value.strip() or "  " in value:
                fail(f"row {i}: stray whitespace in {col} (slug '{slug}')")

        # 17. Diacritic regression guard: ASCII surname forms retired by
        #     the normalization lot must not reappear.
        if banned_form_re:
            for col in ("canonical_name", "aliases"):
                hit = banned_form_re.search(row.get(col) or "")
                if hit:
                    fail(f"row {i}: banned ASCII form '{hit.group(0)}' in "
                         f"{col} (slug '{slug}') — normalized spelling is "
                         f"'{banned_forms[hit.group(0)]}' "
                         f"(docs/diacritic-normalization-map.md)")
            hit = banned_form_re.search(row.get("notes") or "")
            if hit:
                warn(f"row {i}: banned ASCII form '{hit.group(0)}' in notes "
                     f"(slug '{slug}') — normalized spelling is "
                     f"'{banned_forms[hit.group(0)]}'")
                warnings += 1

        # 16. Identity alias: an alias equal to the row's own
        #     canonical_name carries no information — it pads search
        #     indexes and suggests a copy-paste during authoring. Error
        #     since the naming-hygiene lot (2026-06-11) dropped the 24
        #     historical ones.
        canonical_name = (row.get("canonical_name") or "").strip()
        aliases_raw = (row.get("aliases") or "").strip()
        if aliases_raw:
            for alias in aliases_raw.split("|"):
                if alias.strip() == canonical_name:
                    fail(f"row {i}: alias identical to canonical_name "
                         f"({canonical_name!r}) on slug '{slug}'")

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

        #     Unverifiable-source ban (traction-roadmap H0.4): attribution
        #     evidence must be published and publicly checkable. Citing an
        #     unpublished game collection converts missing data into
        #     apparent fabrication, so it fails outright.
        historical_notes_val = (row.get("historical_notes") or "").strip()
        for attr_field, attr_value in (
                ("attributed_to", attributed_to),
                ("attribution_source", attribution_source),
                ("historical_notes", historical_notes_val)):
            hit = UNVERIFIABLE_SOURCE_RE.search(attr_value)
            if hit:
                fail(f"row {i}: slug '{slug}' cites an unverifiable source "
                     f"({hit.group(0)!r} in '{attr_field}'). Attribution "
                     f"evidence must be published and publicly checkable "
                     f"(roadmap H0.4).")

    # 13. Global canonical_name uniqueness. Consumers join and search by
    #     name; two rows with the same name are an ambiguity bug unless
    #     the pair is explicitly allowlisted pending the audit decision.
    names_to_slugs: dict[str, list[str]] = {}
    for slug, row in seen_slugs.items():
        name = (row.get("canonical_name") or "").strip()
        names_to_slugs.setdefault(name, []).append(slug)
    for name, name_slugs in names_to_slugs.items():
        if len(name_slugs) < 2:
            continue
        if set(name_slugs) == DUPLICATE_NAME_ALLOWLIST.get(name):
            continue
        where = ", ".join(
            f"'{s}' (row {seen_slugs[s]['_row']})" for s in sorted(name_slugs)
        )
        fail(f"duplicate canonical_name {name!r} on {where} — canonical "
             f"names must be globally unique; known-pending pairs live in "
             f"DUPLICATE_NAME_ALLOWLIST")

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

        # 18. Child-shorter heuristic (opt-in via --audit-naming): a child
        #     whose canonical_name is shorter than its parent's MAY signal
        #     naming drift, but the catalogue legitimately shortens names
        #     at depth (~1,400 such rows), so this is an audit-sweep tool,
        #     never part of the default gate.
        if audit_naming:
            parent_name = (seen_slugs[parent].get("canonical_name") or "").strip()
            child_name = (row.get("canonical_name") or "").strip()
            if len(child_name) < len(parent_name):
                warn(f"row {row['_row']}: canonical_name {child_name!r} is "
                     f"shorter than parent's {parent_name!r} (slug '{slug}')")
                warnings += 1

        # 19. Same-moves ECO consistency: a child whose moves_uci is
        #     byte-identical to its parent's names the same position, so a
        #     different eco_legacy is a classification contradiction. The
        #     two known offenders sit in PHANTOM_PAIR_ECO_ALLOWLIST pending
        #     the phantom-pair decision.
        same_moves = (row.get("moves_uci") or "").strip()
        parent_same_moves = (seen_slugs[parent].get("moves_uci") or "").strip()
        if (same_moves and same_moves == parent_same_moves
                and slug not in PHANTOM_PAIR_ECO_ALLOWLIST):
            child_eco = (row.get("eco_legacy") or "").strip()
            parent_eco = (seen_slugs[parent].get("eco_legacy") or "").strip()
            if child_eco != parent_eco:
                fail(f"row {row['_row']}: slug '{slug}' has identical moves "
                     f"to parent '{parent}' but a different eco_legacy "
                     f"('{child_eco}' vs '{parent_eco}') — same position, "
                     f"same classification")

        # 20. Parent-ECO inversion (opt-in via --audit-eco): a child with a
        #     single same-class ECO code numerically below its parent's MAY
        #     signal a misclassified parent (the E.QID.Nim case), but ECO
        #     numbering is legitimately non-monotonic with depth (~55 such
        #     rows live in the catalogue) — audit-sweep tool only.
        if audit_eco:
            child_eco = (row.get("eco_legacy") or "").strip()
            parent_eco = (seen_slugs[parent].get("eco_legacy") or "").strip()
            if (ECO_RE.match(child_eco) and ECO_RE.match(parent_eco)
                    and child_eco[0] == parent_eco[0]
                    and int(child_eco[1:]) < int(parent_eco[1:])):
                warn(f"row {row['_row']}: ECO inversion — '{slug}' carries "
                     f"{child_eco}, below parent '{parent}' {parent_eco}")
                warnings += 1

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

    # 11. transposes_to (Layer: canonical link, OCN 0.2).
    #
    # A row may declare `transposes_to=<another slug>` to say "this row
    # is a move-order transposition; the FEN-canonical entry is over
    # there". The contract:
    #   - Target slug must exist.
    #   - Target must differ from the row's own slug.
    #   - Target must NOT be a class root (A/B/C/D/E).
    #   - Class roots themselves must NOT carry transposes_to.
    #   - When both rows have moves_uci, their FEN keys must match —
    #     otherwise the "transposition" claim is false by FEN and the
    #     catalogue would be lying to its consumers.
    for slug, row in seen_slugs.items():
        target = (row.get("transposes_to") or "").strip()
        depth = int(row["depth"])
        if not target:
            continue
        if depth == 0:
            fail(f"row {row['_row']}: class root '{slug}' must not have "
                 f"transposes_to (found '{target}')")
        if target == slug:
            fail(f"row {row['_row']}: slug '{slug}' has transposes_to pointing "
                 f"to itself")
        if target not in seen_slugs:
            fail(f"row {row['_row']}: slug '{slug}' has transposes_to='{target}' "
                 f"but that slug is missing from the catalogue")
        target_row = seen_slugs[target]
        target_depth = int(target_row["depth"])
        if target_depth == 0:
            fail(f"row {row['_row']}: slug '{slug}' has transposes_to='{target}' "
                 f"but target is a class root (class roots are filters, not "
                 f"positions)")
        row_moves = (row.get("moves_uci") or "").strip()
        target_moves = (target_row.get("moves_uci") or "").strip()
        if row_moves and target_moves:
            try:
                row_fen = fen_key_after_uci(row_moves)
                target_fen = fen_key_after_uci(target_moves)
            except ValueError as exc:
                fail(f"row {row['_row']}: {exc} in slug '{slug}'")
            if row_fen != target_fen:
                fail(f"row {row['_row']}: slug '{slug}' has "
                     f"transposes_to='{target}' but their FEN keys differ "
                     f"(this is not a transposition by position)")

    # 12. same_as (Layer: co-canonical link, OCN 0.3).
    #
    # A row may declare `same_as=<other slug>[|<other slug>...]` to say
    # "this row shares its FEN with the listed slug(s), and all of us
    # are preserved as canonicals by editorial decision". Where
    # `transposes_to` records non-canonical → canonical, `same_as`
    # records canonical ↔ canonical. The contract:
    #   - same_as and transposes_to are mutually exclusive on a row.
    #   - Each pipe-separated target slug must exist.
    #   - No self-reference.
    #   - Class roots cannot carry same_as.
    #   - When both rows have moves_uci, their FEN keys must match.
    #   - The relation is conceptually symmetric; the audit treats
    #     in-group same_as edges as undirected when deciding whether
    #     a duplicate group is resolved as multiple_canonical. The
    #     CSV may declare it one-way or bilaterally; bilateral is
    #     preferred for human readability.
    for slug, row in seen_slugs.items():
        same_as_raw = (row.get("same_as") or "").strip()
        transposes_to_raw = (row.get("transposes_to") or "").strip()
        depth = int(row["depth"])
        if not same_as_raw:
            continue
        if transposes_to_raw:
            fail(f"row {row['_row']}: slug '{slug}' has both same_as "
                 f"({same_as_raw!r}) and transposes_to ({transposes_to_raw!r}); "
                 f"a row is either non-canonical (transposes_to) or "
                 f"co-canonical (same_as), never both")
        if depth == 0:
            fail(f"row {row['_row']}: class root '{slug}' must not have "
                 f"same_as (found '{same_as_raw}')")
        targets = [t.strip() for t in same_as_raw.split("|") if t.strip()]
        for target in targets:
            if target == slug:
                fail(f"row {row['_row']}: slug '{slug}' has same_as pointing "
                     f"to itself")
            if target not in seen_slugs:
                fail(f"row {row['_row']}: slug '{slug}' has same_as='{target}' "
                     f"but that slug is missing from the catalogue")
            target_row = seen_slugs[target]
            if int(target_row["depth"]) == 0:
                fail(f"row {row['_row']}: slug '{slug}' has same_as='{target}' "
                     f"but target is a class root")
            row_moves = (row.get("moves_uci") or "").strip()
            target_moves = (target_row.get("moves_uci") or "").strip()
            if row_moves and target_moves:
                try:
                    row_fen = fen_key_after_uci(row_moves)
                    target_fen = fen_key_after_uci(target_moves)
                except ValueError as exc:
                    fail(f"row {row['_row']}: {exc} in slug '{slug}'")
                if row_fen != target_fen:
                    fail(f"row {row['_row']}: slug '{slug}' has "
                         f"same_as='{target}' but their FEN keys differ "
                         f"(this is not a co-canonical pair by position)")

    # 21. ECO class-divergence sidecar consistency (roadmap H2.5).
    #
    # OCN keeps ECO's five families but not every one of ECO's letter
    # assignments; `catalog/ocn-1.eco-divergence.tsv` is the complete,
    # committed list of the rows where they differ, and the spec attaches a
    # written rationale to each. That honesty only holds while the list is
    # current, so the validator recomputes the divergent set from the rows it
    # just read and demands an exact match — reclassify a row or edit an
    # `eco_legacy` cell without regenerating and this fires.
    #
    # Scoped to the canonical catalogue: the sidecar is a property of
    # `catalog/ocn-1.csv`, and the small fixtures used by the test suite
    # (and any catalogue slice a maintainer validates ad hoc) have none.
    if path.resolve() == DEFAULT_CATALOG.resolve():
        problem = divergence_sidecar_problem(rows)
        if problem:
            fail(problem)

    print(f"OK: {len(seen_slugs)} entries validated, {warnings} warning(s)")


def main() -> int:
    args = sys.argv[1:]
    strict_chess = False
    audit_naming = False
    audit_eco = False
    extra_banned: dict[str, str] = {}
    positional: list[str] = []
    i = 0
    while i < len(args):
        arg = args[i]
        if arg == "--strict-chess":
            strict_chess = True
        elif arg == "--audit-naming":
            audit_naming = True
        elif arg == "--audit-eco":
            audit_eco = True
        elif arg == "--ban-ascii-form":
            i += 1
            if i >= len(args) or "=" not in args[i]:
                fail("--ban-ascii-form expects ASCII=Normalized "
                     "(e.g. --ban-ascii-form Lopez=López)")
            ascii_form, _, normalized = args[i].partition("=")
            extra_banned[ascii_form] = normalized
        else:
            positional.append(arg)
        i += 1
    if len(positional) > 1:
        fail("usage: python3 tools/validate.py [--strict-chess] "
             "[--audit-naming] [--audit-eco] "
             "[--ban-ascii-form ASCII=Normalized ...] [catalog/ocn-1.csv]")
    path = Path(positional[0]) if positional else DEFAULT_CATALOG
    validate(
        path,
        strict_chess=strict_chess,
        extra_banned_forms=extra_banned,
        audit_naming=audit_naming,
        audit_eco=audit_eco,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
