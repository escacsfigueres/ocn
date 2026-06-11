#!/usr/bin/env python3
"""Triage the OCN-1 catalogue for naming / attribution audit work.

This tool **automates triage, not truth.** It scans ``catalog/ocn-1.csv``
and classifies every row by the *basis* of its name (person eponym,
place/event, editorial descriptor, metaphor, gambit/tactic) and the state
of its attribution fields, then recommends a next action per row and per
family head. It deliberately does **not** write attribution fields, invent
sources, or touch the catalogue — those decisions stay human, gated on
first-hand evidence (see docs/naming-attribution-audit-methodology.md).

Pipeline this tool is built for:

  1. deterministic triage (this script) → a prioritized map
  2. select the top ``source_sprint`` / ``batch_candidate`` groups
  3. dynamic-workflow evidence search over just those groups
  4. apply only CLEAR, homogeneous batches (head rows only)

The seed token lists below are intentionally small and editable; they are
derived from the existing audit docs (the surname risk map, the non-person
taxonomy) and are **not exhaustive**. The tool's job is to surface and
rank candidates, not to be the final authority on any one name.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable

DEFAULT_CATALOG = Path(__file__).resolve().parent.parent / "catalog" / "ocn-1.csv"

# --- Categories (naming basis) ------------------------------------------
CAT_ALREADY = "already_attributed"
CAT_PERSON = "likely_person_eponym"
CAT_PLACE = "likely_place_or_event"
CAT_DESCRIPTOR = "editorial_descriptor"
CAT_METAPHOR = "metaphor_or_animal"
CAT_GAMBIT = "gambit_or_tactic"
CAT_UNKNOWN = "unknown_or_mixed"

CATEGORIES = (
    CAT_ALREADY,
    CAT_PERSON,
    CAT_PLACE,
    CAT_DESCRIPTOR,
    CAT_METAPHOR,
    CAT_GAMBIT,
    CAT_UNKNOWN,
)

# --- Recommended next actions -------------------------------------------
ACT_ALREADY = "already_done"
ACT_IGNORE = "ignore_descriptor"
ACT_SOURCE = "source_sprint"
ACT_INDIVIDUAL = "individual_proposal"
ACT_BATCH = "batch_candidate"

ACTIONS = (ACT_ALREADY, ACT_IGNORE, ACT_SOURCE, ACT_INDIVIDUAL, ACT_BATCH)

RISK_LOW = "low"
RISK_MEDIUM = "medium"
RISK_HIGH = "high"

# --- Seed knowledge (editable; derived from the audit docs) -------------
# Multi-opening surnames: the same surname names ≥2 distinct heads, so it
# must NEVER be blanket-attributed — only one specific head at a time.
# Source: docs/player-eponym-attribution-batch-proposal.md (surname risk map).
DANGEROUS_SURNAMES = {
    "tarrasch",
    "rubinstein",
    "steinitz",
    "marshall",
    "chigorin",
    "bogoljubow",
    # Added 2026-06-11 from the whole-catalogue factory map's verified
    # row counts (docs/whole-catalogue-attribution-factory-map.md):
    # each labels several unrelated openings — never blanket-attribute.
    "nimzowitsch",
    "botvinnik",
    "keres",
    "lasker",
    "paulsen",
}

# Single-/few-head eponyms with a recognised primary head. These are the
# homogeneous batch targets once a first-hand naming source is read.
MODERATE_SURNAMES = {
    "alekhine",
    "grunfeld",
    "reti",
    "tartakower",
    "bird",
    "larsen",
    "pirc",
    "winawer",
    "trompowsky",
    "rossolimo",
    "najdorf",
    "sveshnikov",
    "polugaevsky",
    "alapin",
    "taimanov",
    "benko",
    "uhlmann",
    "korchnoi",
    "barcza",
    "maroczy",
    "petroff",
    "petrov",
    "caro",
    "kann",
    "veresov",
    "colle",
    "zukertort",
    "schliemann",
    "breyer",
    "smyslov",
    "panov",
    "richter",
    "sozin",
    "velimirovic",
    "kalashnikov",
    "kupreichik",
}

# Geography-family names: the place *is* the line's identity. The name is
# correct as-is and gets no attributed_to (taxonomy category 1).
GEO_FAMILY_TOKENS = {
    "sicilian",
    "french",
    "italian",
    "scandinavian",
    "dutch",
    "english",
    "scotch",
    "vienna",
    "slav",
    "spanish",
    "russian",
    "latvian",
    "polish",
    "indian",
    "catalan",
    "benoni",
    "london",
}

# Event / venue tokens: a place that may anchor a dated event (taxonomy
# category 2/3). Worth a source check, not an automatic attribution.
EVENT_VENUE_TOKENS = {
    "cambridge springs",
    "carlsbad",
    "karlsbad",
    "meran",
    "merano",
    "mar del plata",
    "monte carlo",
    "zurich",
    "stockholm",
    "hastings",
    "nuremberg",
    "noteboom",
    "wade",
    "riga",
    "leningrad",
    "scheveningen",
    "wilkes-barre",
    "marienbad",
}

# Editorial / database descriptors: bookkeeping tokens, permanently
# unattributed (taxonomy category 8). ~46% of the catalogue.
DESCRIPTOR_TOKENS = {
    "main line",
    "variation",
    "system",
    "accepted",
    "declined",
    "exchange",
    "move order",
    "normal",
    "deferred",
    "transposition",
    "advance",
    "open",
    "closed",
    "fianchetto",
    "classical",
    "modern",
    "anti",
    "delayed",
    "early",
    "general",
    "other",
    "miscellaneous",
    "with",
    "without",
    "lines",
}

# Metaphor / animal / evocative coinages (taxonomy category 6). A name,
# not a person; story → historical_notes only if a real coinage is sourced.
METAPHOR_TOKENS = {
    "dragon",
    "hippopotamus",
    "hippo",
    "orangutan",
    "pterodactyl",
    "elephant",
    "snake",
    "hedgehog",
    "stonewall",
    "monkey",
    "octopus",
    "spider",
    "crab",
    "hawk",
    "kangaroo",
    "mosquito",
    "fingerslip",
}

# Gambit / tactic / evaluation tokens (taxonomy category 7). The idea, not
# a person — never attributed_to.
GAMBIT_TACTIC_TOKENS = {
    "gambit",
    "countergambit",
    "counter-gambit",
    "poisoned pawn",
    "attack",
    "sacrifice",
    "trap",
    "wing",
    "sniper",
    "swindle",
}


def fail(message: str, *, code: int = 1) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(code)


def load_catalog(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        fail(f"catalogue not found: {path}")
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _norm(text: str) -> str:
    """Lowercase + strip diacritics for token matching."""
    decomposed = unicodedata.normalize("NFKD", text)
    stripped = "".join(c for c in decomposed if not unicodedata.combining(c))
    return stripped.lower()


def _depth(row: dict[str, str]) -> int:
    raw = (row.get("depth") or "").strip()
    try:
        return int(raw)
    except ValueError:
        return -1


def _attr_state(row: dict[str, str]) -> str:
    """Compact present-fields mask, e.g. 'ASH', 'A-S', '---'."""
    a = "A" if (row.get("attributed_to") or "").strip() else "-"
    s = "S" if (row.get("attribution_source") or "").strip() else "-"
    h = "H" if (row.get("historical_notes") or "").strip() else "-"
    return a + s + h


def _is_attributed(row: dict[str, str]) -> bool:
    return any(
        (row.get(f) or "").strip()
        for f in ("attributed_to", "attribution_source", "historical_notes")
    )


def _match_tokens(haystack: str, tokens: Iterable[str]) -> list[str]:
    return sorted({t for t in tokens if t in haystack})


def _surnames_in(haystack: str) -> list[tuple[str, str]]:
    """Return (surname, risk) pairs detected in the normalised text."""
    out: list[tuple[str, str]] = []
    for surname in DANGEROUS_SURNAMES:
        if surname in haystack:
            out.append((surname, RISK_HIGH))
    for surname in MODERATE_SURNAMES:
        if surname in haystack:
            out.append((surname, RISK_MEDIUM))
    return sorted(out)


def _family_prefix(slug: str) -> str:
    """First two dot-segments of a slug, e.g. 'B.Fre.Win' -> 'B.Fre'."""
    return ".".join(slug.split(".")[:2])


def classify_row(
    row: dict[str, str],
    *,
    parent_row: dict[str, str] | None,
    has_children: bool,
    family_has_template: bool = False,
) -> dict[str, object]:
    """Classify a single catalogue row. Pure function, no I/O."""
    name = row.get("canonical_name") or ""
    aliases = row.get("aliases") or ""
    hay = _norm(f"{name} {aliases}")

    surnames = _surnames_in(hay)
    surname_tokens = [s for s, _ in surnames]
    geo = _match_tokens(hay, GEO_FAMILY_TOKENS)
    events = _match_tokens(hay, EVENT_VENUE_TOKENS)
    descriptors = _match_tokens(hay, DESCRIPTOR_TOKENS)
    metaphors = _match_tokens(hay, METAPHOR_TOKENS)
    gambits = _match_tokens(hay, GAMBIT_TACTIC_TOKENS)

    detected: list[str] = []
    detected += [f"person:{s}" for s in surname_tokens]
    detected += [f"event:{e}" for e in events]
    detected += [f"geo:{g}" for g in geo]
    detected += [f"meta:{m}" for m in metaphors]
    detected += [f"gambit:{g}" for g in gambits]
    detected += [f"descr:{d}" for d in descriptors]

    attr_state = _attr_state(row)
    already = _is_attributed(row)

    # Does the row introduce its surname, or merely inherit it from a
    # parent that already carries the same surname?
    inherits_surname = False
    if parent_row is not None and surname_tokens:
        parent_hay = _norm(
            f"{parent_row.get('canonical_name') or ''} "
            f"{parent_row.get('aliases') or ''}"
        )
        parent_surnames = {s for s, _ in _surnames_in(parent_hay)}
        inherits_surname = bool(parent_surnames & set(surname_tokens))

    # --- decide category (precedence: existing attribution wins, then
    # person eponym, then event, then non-person descriptor families) ---
    if already:
        category = CAT_ALREADY
    elif surname_tokens:
        category = CAT_PERSON
    elif events:
        category = CAT_PLACE
    elif metaphors:
        category = CAT_METAPHOR
    elif gambits:
        category = CAT_GAMBIT
    elif geo:
        category = CAT_PLACE
    elif descriptors:
        category = CAT_DESCRIPTOR
    else:
        category = CAT_UNKNOWN

    # --- decide risk + action -------------------------------------------
    if category == CAT_ALREADY:
        risk, action, reason = RISK_LOW, ACT_ALREADY, "attribution fields already populated"
    elif category == CAT_PERSON:
        worst_risk = RISK_HIGH if any(r == RISK_HIGH for _, r in surnames) else RISK_MEDIUM
        if inherits_surname:
            risk = RISK_LOW
            action = ACT_IGNORE
            reason = "inherits surname from parent head; children need no edit"
        elif worst_risk == RISK_HIGH:
            risk = RISK_HIGH
            action = ACT_INDIVIDUAL
            reason = (
                "multi-opening surname (DANGEROUS) — attribute one specific "
                "head only, never blanket; individual source-gated proposal"
            )
        elif family_has_template:
            risk = RISK_MEDIUM
            action = ACT_BATCH
            reason = (
                "eponym head whose family already has an attributed sibling "
                "(in-family template) — strongest batch target once sourced"
            )
        elif surname_tokens and any(s in MODERATE_SURNAMES for s in surname_tokens):
            risk = RISK_MEDIUM
            action = ACT_SOURCE
            reason = "recognised single-head eponym; needs a first-hand naming source (source sprint)"
        else:
            risk = RISK_MEDIUM
            action = ACT_SOURCE
            reason = "surname detected but not in seed list; confirm it names a person, then source"
    elif category == CAT_PLACE:
        if events:
            risk, action = RISK_MEDIUM, ACT_SOURCE
            reason = "place/event token — check for a dated event anchor before any attribution"
        else:
            risk, action = RISK_LOW, ACT_IGNORE
            reason = "geographic family name — the place is the name; attributed_to stays empty"
    elif category == CAT_METAPHOR:
        risk, action = RISK_LOW, ACT_IGNORE
        reason = "metaphor/animal coinage — name, not person; story → historical_notes only if sourced"
    elif category == CAT_GAMBIT:
        risk, action = RISK_LOW, ACT_IGNORE
        reason = "gambit/tactic descriptor — the idea, not a person; permanently unattributed"
    elif category == CAT_DESCRIPTOR:
        risk, action = RISK_LOW, ACT_IGNORE
        reason = "editorial/database descriptor (Type-H) — permanently unattributed"
    else:  # CAT_UNKNOWN
        depth = _depth(row)
        if depth <= 1 and not inherits_surname:
            risk, action = RISK_MEDIUM, ACT_SOURCE
            reason = "shallow head with no recognised token — manual review / source sprint"
        else:
            risk, action = RISK_LOW, ACT_IGNORE
            reason = "deep row, no recognised naming token — likely descriptor; low priority"

    # A head candidate is a shallow-ish row that introduces its own name
    # (does not inherit a surname) — the unit worth auditing.
    head_candidate = (parent_row is None) or (not inherits_surname)

    return {
        "ocn1": (row.get("ocn1") or "").strip(),
        "canonical_name": name,
        "eco_legacy": (row.get("eco_legacy") or "").strip(),
        "parent_ocn1": (row.get("parent_ocn1") or "").strip(),
        "depth": _depth(row),
        "has_children": has_children,
        "head_candidate": head_candidate,
        "attribution_fields_state": attr_state,
        "detected_tokens": detected,
        "surnames": surname_tokens,
        "category": category,
        "risk_level": risk,
        "recommended_next_action": action,
        "reason": reason,
    }


def audit_catalog(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    by_slug = {(r.get("ocn1") or "").strip(): r for r in rows}
    parents = {(r.get("parent_ocn1") or "").strip() for r in rows}
    parents.discard("")
    # Families (2-segment prefixes) that already contain an attributed row;
    # an unsourced eponym head in such a family is the strongest batch
    # target because the in-family attribution template already exists.
    attributed_prefixes = {
        _family_prefix((r.get("ocn1") or "").strip())
        for r in rows
        if _is_attributed(r)
    }
    attributed_prefixes.discard("")
    results: list[dict[str, object]] = []
    for row in rows:
        slug = (row.get("ocn1") or "").strip()
        parent_slug = (row.get("parent_ocn1") or "").strip()
        parent_row = by_slug.get(parent_slug) if parent_slug else None
        has_children = slug in parents
        family_has_template = _family_prefix(slug) in attributed_prefixes
        results.append(
            classify_row(
                row,
                parent_row=parent_row,
                has_children=has_children,
                family_has_template=family_has_template,
            )
        )
    return results


# --- grouping -----------------------------------------------------------
def group_eponym_heads(results: list[dict[str, object]]) -> list[dict[str, object]]:
    """Group person-eponym head candidates by surname for batch planning."""
    by_surname: dict[str, list[dict[str, object]]] = defaultdict(list)
    for r in results:
        if r["category"] != CAT_PERSON or not r["head_candidate"]:
            continue
        for s in r["surnames"]:  # type: ignore[union-attr]
            by_surname[s].append(r)
    groups: list[dict[str, object]] = []
    for surname, members in by_surname.items():
        risk = RISK_HIGH if surname in DANGEROUS_SURNAMES else RISK_MEDIUM
        groups.append(
            {
                "surname": surname,
                "risk_level": risk,
                "head_count": len(members),
                # Shallowest first: the genuine family head (e.g. B.Fre.Win)
                # leads, deeper substring matches follow — so a human
                # winnowing the group reads the real head at the top.
                "heads": sorted(members, key=lambda m: (int(m["depth"]), str(m["ocn1"]))),
            }
        )
    groups.sort(key=lambda g: (g["risk_level"] != RISK_MEDIUM, -int(g["head_count"]), str(g["surname"])))
    return groups


# --- output -------------------------------------------------------------
ROW_FIELDS = [
    "ocn1",
    "canonical_name",
    "eco_legacy",
    "parent_ocn1",
    "depth",
    "has_children",
    "head_candidate",
    "attribution_fields_state",
    "category",
    "risk_level",
    "recommended_next_action",
    "detected_tokens",
    "reason",
]


def _row_to_flat(r: dict[str, object]) -> dict[str, object]:
    flat = dict(r)
    flat["has_children"] = "1" if r["has_children"] else "0"
    flat["head_candidate"] = "1" if r["head_candidate"] else "0"
    flat["detected_tokens"] = "|".join(r["detected_tokens"])  # type: ignore[arg-type]
    return {k: flat.get(k, "") for k in ROW_FIELDS}


def write_tsv(results: list[dict[str, object]], out) -> None:
    writer = csv.DictWriter(out, fieldnames=ROW_FIELDS, delimiter="\t", lineterminator="\n")
    writer.writeheader()
    for r in results:
        writer.writerow(_row_to_flat(r))


def write_json(results: list[dict[str, object]], groups: list[dict[str, object]], out) -> None:
    payload = {"rows": results, "eponym_head_groups": groups}
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True), file=out)


def write_markdown(results: list[dict[str, object]], groups: list[dict[str, object]], out) -> None:
    cat_counts = Counter(r["category"] for r in results)
    act_counts = Counter(r["recommended_next_action"] for r in results)
    risk_counts = Counter(r["risk_level"] for r in results)

    print("# Naming / attribution audit — triage map\n", file=out)
    print(
        "Deterministic triage of `catalog/ocn-1.csv`. **No catalogue change.** "
        "Recommends a next action per row; sources stay human + first-hand.\n",
        file=out,
    )
    print(f"- Rows scanned: **{len(results)}**", file=out)
    print("\n## By category\n", file=out)
    print("| category | rows |", file=out)
    print("|---|---|", file=out)
    for cat in CATEGORIES:
        print(f"| {cat} | {cat_counts.get(cat, 0)} |", file=out)
    print("\n## By recommended action\n", file=out)
    print("| action | rows |", file=out)
    print("|---|---|", file=out)
    for act in ACTIONS:
        print(f"| {act} | {act_counts.get(act, 0)} |", file=out)
    print("\n## By risk\n", file=out)
    print("| risk | rows |", file=out)
    print("|---|---|", file=out)
    for risk in (RISK_HIGH, RISK_MEDIUM, RISK_LOW):
        print(f"| {risk} | {risk_counts.get(risk, 0)} |", file=out)

    print("\n## Top eponym head-candidate groups (batch / proposal targets)\n", file=out)
    print("| surname | risk | heads | example slugs |", file=out)
    print("|---|---|---|---|", file=out)
    for g in groups[:25]:
        slugs = ", ".join(str(h["ocn1"]) for h in g["heads"][:6])  # type: ignore[index]
        print(
            f"| {g['surname']} | {g['risk_level']} | {g['head_count']} | {slugs} |",
            file=out,
        )

    print("\n## Source-sprint head candidates (non-eponym, need review)\n", file=out)
    print("| slug | name | category | reason |", file=out)
    print("|---|---|---|---|", file=out)
    sprint = [
        r
        for r in results
        if r["recommended_next_action"] == ACT_SOURCE
        and r["head_candidate"]
        and r["category"] != CAT_PERSON
    ]
    sprint.sort(key=lambda r: (int(r["depth"]), str(r["ocn1"])))
    for r in sprint[:40]:
        print(
            f"| `{r['ocn1']}` | {r['canonical_name']} | {r['category']} | {r['reason']} |",
            file=out,
        )


def print_summary(results: list[dict[str, object]], groups: list[dict[str, object]]) -> None:
    cat_counts = Counter(r["category"] for r in results)
    act_counts = Counter(r["recommended_next_action"] for r in results)
    risk_counts = Counter(r["risk_level"] for r in results)
    head_candidates = sum(1 for r in results if r["head_candidate"])
    print(
        "SUMMARY "
        f"rows={len(results)} "
        f"head_candidates={head_candidates} "
        f"already_attributed={cat_counts.get(CAT_ALREADY, 0)} "
        f"person_eponym={cat_counts.get(CAT_PERSON, 0)} "
        f"place_or_event={cat_counts.get(CAT_PLACE, 0)} "
        f"descriptor={cat_counts.get(CAT_DESCRIPTOR, 0)} "
        f"metaphor={cat_counts.get(CAT_METAPHOR, 0)} "
        f"gambit_tactic={cat_counts.get(CAT_GAMBIT, 0)} "
        f"unknown={cat_counts.get(CAT_UNKNOWN, 0)} "
        f"act_source_sprint={act_counts.get(ACT_SOURCE, 0)} "
        f"act_batch_candidate={act_counts.get(ACT_BATCH, 0)} "
        f"act_individual_proposal={act_counts.get(ACT_INDIVIDUAL, 0)} "
        f"act_ignore={act_counts.get(ACT_IGNORE, 0)} "
        f"act_already_done={act_counts.get(ACT_ALREADY, 0)} "
        f"risk_high={risk_counts.get(RISK_HIGH, 0)} "
        f"risk_medium={risk_counts.get(RISK_MEDIUM, 0)} "
        f"risk_low={risk_counts.get(RISK_LOW, 0)} "
        f"eponym_head_groups={len(groups)}",
        file=sys.stderr,
    )


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Triage the OCN-1 catalogue for naming/attribution work. "
            "Classifies every row by naming basis + attribution state and "
            "recommends a next action. Read-only: never edits the catalogue."
        )
    )
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    parser.add_argument("--out", type=Path, help="write the report to a file instead of stdout")
    parser.add_argument(
        "--format",
        choices=("tsv", "markdown", "json"),
        default="tsv",
        help="output format (default tsv)",
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="print a compact summary line to stderr",
    )
    parser.add_argument(
        "--category",
        choices=CATEGORIES,
        help="only emit rows in this category",
    )
    parser.add_argument(
        "--action",
        choices=ACTIONS,
        help="only emit rows with this recommended action",
    )
    parser.add_argument(
        "--head-only",
        action="store_true",
        help="only emit head-candidate rows (skip rows that inherit a name)",
    )
    return parser.parse_args(argv)


def main() -> int:
    args = parse_args(sys.argv[1:])
    rows = load_catalog(args.catalog)
    results = audit_catalog(rows)
    groups = group_eponym_heads(results)

    filtered = results
    if args.category:
        filtered = [r for r in filtered if r["category"] == args.category]
    if args.action:
        filtered = [r for r in filtered if r["recommended_next_action"] == args.action]
    if args.head_only:
        filtered = [r for r in filtered if r["head_candidate"]]

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        with args.out.open("w", newline="", encoding="utf-8") as f:
            if args.format == "json":
                write_json(filtered, groups, f)
            elif args.format == "markdown":
                write_markdown(filtered, groups, f)
            else:
                write_tsv(filtered, f)
    else:
        if args.format == "json":
            write_json(filtered, groups, sys.stdout)
        elif args.format == "markdown":
            write_markdown(filtered, groups, sys.stdout)
        else:
            write_tsv(filtered, sys.stdout)

    if args.summary:
        print_summary(results, groups)
    return 0


if __name__ == "__main__":
    sys.exit(main())
