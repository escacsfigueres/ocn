#!/usr/bin/env python3
"""Lumbra Gigabase chronology / first-appearance helper (factory-map tooling
gap #5).

Lumbra Gigabase is an external games database used by evidence sprints to date
a line's *first appearance* (a type-A corpus fact, e.g. "corpus first game
1888") — never to prove who *named* it. This CLI does the two DETERMINISTIC,
OFFLINE halves of that workflow; the actual Lumbra query is run BY HAND,
out-of-band (the sandbox cannot reach Lumbra and this tool makes no network
call):

  1. `spec`      — Build a structured first-appearance query spec from an OCN
                   row (`--ocn1 SLUG`, resolved via tools/ocn.py) or from
                   explicit `--moves` / `--fen` / `--eponym` / `--player`
                   inputs, optionally bounded by `--before YEAR`. A human runs
                   this spec against Lumbra and saves the returned games.

  2. `summarize` — Given that saved results file (a small TSV or JSON of games
                   with at least year / white / black / event), deterministically
                   compute the FIRST APPEARANCE (earliest year; ties broken by
                   input order) and format a one-line evidence string in the
                   house style: "corpus first game <Year>: <White>–<Black>,
                   <Event> <Year>". This is the load-bearing, easily-tested half.

The tool NEVER invents chronology facts: with no results file it only emits a
query spec, and `summarize` only computes over the games the user supplies.
First appearance is a type-A fact for `historical_notes`, not `attributed_to`
(see docs/naming-attribution-audit-methodology.md).

Usage:
    python3 tools/lumbra_chronology_helper.py spec --ocn1 B.Fre.Win [--before YEAR]
        [--eponym TEXT] [--player TEXT] [--catalog catalog/ocn-1.csv]
        [--format text|json] [--out FILE]
    python3 tools/lumbra_chronology_helper.py spec (--moves "e2e4 c7c5" | --fen FEN)
        (--eponym TEXT | --player TEXT) [--before YEAR] [--format text|json]
    python3 tools/lumbra_chronology_helper.py summarize --results games.tsv
        [--before YEAR] [--format text|json] [--out FILE]

Exit codes: 0 success (empty results / empty post-filter is success, with an
explicit "no games" line — never a fabricated date), 1 data error (missing
slug, bad FEN/moves, unreadable/malformed results), 2 usage error.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

try:
    from ocn import Catalog, fen_key
    from chess_uci import validate_uci_sequence, fen_key_after_uci
except ImportError:  # pragma: no cover - only for unusual direct imports.
    from tools.ocn import Catalog, fen_key
    from tools.chess_uci import validate_uci_sequence, fen_key_after_uci

DEFAULT_CATALOG = Path(__file__).resolve().parent.parent / "catalog" / "ocn-1.csv"
QUERY_KIND = "ocn.lumbra_chronology_query.v1"
EN_DASH = "–"
MANUAL_NOTE = (
    "Run this spec against Lumbra Gigabase (~/Downloads/GIGABASE/) BY HAND, "
    "out-of-band — this tool makes no network call. Save the returned games as "
    "a TSV/JSON (columns: year, white, black, event), then feed them to the "
    "`summarize` subcommand. First appearance is a type-A corpus fact for "
    "historical_notes, never proof of who named the line."
)
RESULT_FIELDS = ("year", "white", "black", "event")


def fail(msg: str, *, code: int = 1) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    raise SystemExit(code)


# --------------------------------------------------------------------------- #
# spec — deterministic query-spec generation (offline).
# --------------------------------------------------------------------------- #

def infer_eponym(canonical_name: str) -> str | None:
    """Best-effort eponym candidate from a canonical name.

    The catalogue convention is "<Family>, <Eponym> [<role>]" (e.g.
    "French, Winawer"); the segment after the last comma is the most specific
    label and is the natural Lumbra player/eponym search seed. This is only a
    SEED — the human refines it. Returns None when no comma segment exists.
    """
    if "," not in canonical_name:
        return None
    tail = canonical_name.rsplit(",", 1)[1].strip()
    return tail or None


def derive_san(moves_uci: str) -> str:
    """Render a UCI line as a numbered SAN string (deterministic, offline)."""
    sans = validate_uci_sequence(moves_uci)
    out: list[str] = []
    for ply, san in enumerate(sans):
        if ply % 2 == 0:
            out.append(f"{ply // 2 + 1}.{san}")
        else:
            out.append(san)
    return " ".join(out)


def build_spec(args: argparse.Namespace) -> dict:
    ocn1 = name = moves_uci = moves_san = fen = None
    eponym = args.eponym
    player = args.player

    if args.ocn1:
        catalog = Catalog.load(args.catalog) if args.catalog.exists() else None
        if catalog is None:
            fail(f"catalogue not found: {args.catalog}")
        try:
            row = catalog.by_slug(args.ocn1)
        except KeyError:
            fail(f"slug not in catalogue: {args.ocn1}")
        ocn1 = row["ocn1"]
        name = row.get("canonical_name") or None
        moves_uci = (row.get("moves_uci") or "").strip() or None
        if name and not eponym:
            eponym = infer_eponym(name)

    if args.moves:
        moves_uci = args.moves.strip()

    if moves_uci:
        try:
            moves_san = derive_san(moves_uci)
            fen = fen_key_after_uci(moves_uci)
        except ValueError as exc:
            fail(f"invalid UCI moves: {exc}")

    if args.fen:
        try:
            fen = fen_key(args.fen)
        except (ValueError, IndexError) as exc:
            fail(f"invalid FEN: {exc}")

    # A search needs a position AND something to search for. From a slug the
    # eponym is inferred; explicit inputs must supply --eponym or --player.
    if not (eponym or player):
        fail("a search target is required: --eponym and/or --player "
             "(inferred automatically only from a named --ocn1 slug)", code=2)

    spec = {
        "kind": QUERY_KIND,
        "ocn1": ocn1,
        "name": name,
        "moves_uci": moves_uci,
        "moves_san": moves_san,
        "fen": fen,
        "eponym": eponym,
        "player": player,
        "before_year": args.before,
        "instructions": MANUAL_NOTE,
    }
    return spec


def render_spec_text(spec: dict) -> str:
    lines = [
        "# Lumbra Gigabase chronology / first-appearance query (MANUAL fetch)",
        f"kind:        {spec['kind']}",
    ]
    for label, key in (
        ("ocn1", "ocn1"),
        ("name", "name"),
        ("moves (uci)", "moves_uci"),
        ("moves (san)", "moves_san"),
        ("position fen", "fen"),
        ("eponym", "eponym"),
        ("player", "player"),
    ):
        if spec.get(key):
            lines.append(f"{label}:".ljust(14) + str(spec[key]))
    if spec.get("before_year") is not None:
        lines.append("before year:".ljust(14) + str(spec["before_year"]))
    lines.append("")
    lines.append(spec["instructions"])
    return "\n".join(lines) + "\n"


# --------------------------------------------------------------------------- #
# summarize — deterministic first-appearance over a results file (offline).
# --------------------------------------------------------------------------- #

def load_results(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        fail(f"results file not found: {path}")
    text = path.read_text(encoding="utf-8")
    stripped = text.lstrip()
    if stripped.startswith("[") or stripped.startswith("{"):
        try:
            data = json.loads(text)
        except json.JSONDecodeError as exc:
            fail(f"results file is not valid JSON: {exc}")
        if isinstance(data, dict):
            data = data.get("games", data.get("results", []))
        if not isinstance(data, list):
            fail("JSON results must be a list of game objects "
                 "(or {games|results: [...]})")
        rows = [{k: str(v) for k, v in dict(g).items()} for g in data]
    else:
        reader = csv.DictReader(text.splitlines(), delimiter="\t")
        rows = [dict(r) for r in reader]
    return rows


def parse_games(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    games: list[dict[str, object]] = []
    for idx, raw in enumerate(rows):
        missing = [f for f in RESULT_FIELDS if f not in raw]
        if missing:
            fail(f"results row {idx + 1} missing required column(s): "
                 f"{', '.join(missing)} (need: {', '.join(RESULT_FIELDS)})")
        year_text = str(raw["year"]).strip()
        try:
            year = int(year_text)
        except ValueError:
            fail(f"results row {idx + 1} has a non-integer year: {year_text!r}")
        games.append({
            "order": idx,
            "year": year,
            "white": str(raw["white"]).strip(),
            "black": str(raw["black"]).strip(),
            "event": str(raw["event"]).strip(),
        })
    return games


def first_appearance(games: list[dict[str, object]],
                     before: int | None) -> dict[str, object] | None:
    pool = games if before is None else [g for g in games if g["year"] < before]
    if not pool:
        return None
    # Earliest year; ties broken by original input order (stable, deterministic).
    return min(pool, key=lambda g: (g["year"], g["order"]))


def evidence_line(game: dict[str, object]) -> str:
    players = f"{game['white']}{EN_DASH}{game['black']}"
    event = str(game["event"]).strip()
    tail = f"{players}, {event} {game['year']}".rstrip()
    if not event:
        tail = f"{players} ({game['year']})"
    return f"corpus first game {game['year']}: {tail}"


def summarize(args: argparse.Namespace) -> dict:
    rows = load_results(args.results)
    games = parse_games(rows)
    chosen = first_appearance(games, args.before)
    if chosen is None:
        line = ("no games in results"
                if args.before is None
                else f"no games before {args.before} in results")
        return {
            "first_year": None,
            "white": None,
            "black": None,
            "event": None,
            "count": len(games),
            "before_year": args.before,
            "evidence_line": line,
        }
    return {
        "first_year": chosen["year"],
        "white": chosen["white"],
        "black": chosen["black"],
        "event": chosen["event"],
        "count": len(games),
        "before_year": args.before,
        "evidence_line": evidence_line(chosen),
    }


# --------------------------------------------------------------------------- #
# CLI.
# --------------------------------------------------------------------------- #

def emit(text: str, out: Path | None) -> None:
    if out:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="lumbra_chronology_helper.py",
        description=(
            "Deterministic, OFFLINE helper for Lumbra Gigabase chronology / "
            "first-appearance queries. The actual Lumbra fetch is run BY HAND, "
            "out-of-band (this tool never touches the network). `spec` builds a "
            "query spec; `summarize` turns saved results into a first-appearance "
            "evidence line."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = p.add_subparsers(dest="command")

    sp = sub.add_parser("spec", help="Build a Lumbra first-appearance query "
                                     "spec (manual fetch).")
    sp.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    sp.add_argument("--ocn1", default=None, metavar="SLUG",
                    help="Derive moves/FEN/name/eponym from this catalogue row.")
    sp.add_argument("--moves", default=None, metavar="UCI",
                    help="Explicit UCI line (alternative to --ocn1).")
    sp.add_argument("--fen", default=None,
                    help="Explicit FEN (normalised to the catalogue key).")
    sp.add_argument("--eponym", default=None, metavar="TEXT",
                    help="Eponym/name to search; auto-inferred from --ocn1.")
    sp.add_argument("--player", default=None, metavar="TEXT",
                    help="Player to filter games by.")
    sp.add_argument("--before", type=int, default=None, metavar="YEAR",
                    help="Year ceiling for the chronology search.")
    sp.add_argument("--format", choices=("text", "json"), default="text")
    sp.add_argument("--out", type=Path, default=None)

    su = sub.add_parser("summarize", help="Compute first appearance from a "
                                          "saved Lumbra results file.")
    su.add_argument("--results", type=Path, required=True,
                    help="TSV or JSON of games (columns: year, white, black, "
                         "event).")
    su.add_argument("--before", type=int, default=None, metavar="YEAR",
                    help="Exclude games in/after this year (strict <).")
    su.add_argument("--format", choices=("text", "json"), default="text")
    su.add_argument("--out", type=Path, default=None)
    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(sys.argv[1:] if argv is None else argv)

    if args.command == "spec":
        if not (args.ocn1 or args.moves or args.fen):
            parser.error("spec needs --ocn1, or --moves/--fen (with a "
                         "--eponym/--player target)")
        spec = build_spec(args)
        text = (json.dumps(spec, ensure_ascii=False, indent=2) + "\n"
                if args.format == "json" else render_spec_text(spec))
        emit(text, args.out)
        return 0

    if args.command == "summarize":
        result = summarize(args)
        if args.format == "json":
            text = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
        else:
            text = result["evidence_line"] + "\n"
        emit(text, args.out)
        return 0

    parser.error("a subcommand is required: spec | summarize")
    return 2  # pragma: no cover - parser.error exits.


if __name__ == "__main__":
    sys.exit(main())
