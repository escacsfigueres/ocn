"""The ``ocn`` command line.

One entry point with ``--help`` everywhere, subsuming the help-less
one-off scripts the repository grew during catalogue development
(``from_uci.py``, ``from_eco.py``, ``from_position.py``)::

    ocn lookup B90                  # ECO code, OCN slug or opening name
    ocn lookup B.Sic.Naj.Eng
    ocn lookup "najdorf"
    ocn fen "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2"
    ocn uci "e2e4 c7c5 g1f3 d7d6"
    ocn version

Every subcommand takes ``--json`` for machine-readable output. Exit
codes: 0 on a hit, 1 on no match, 2 on a usage or input error.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections.abc import Sequence

from . import __version__
from .catalog import Catalog, Row

__all__ = ["main"]

ECO_RE = re.compile(r"^[A-E]\d{2}$")
# Same shape the validator enforces: the `-` matters, 382 slugs end in a
# castling token (`E.Gru.Exc.Cla.MLn.O-O`).
SLUG_RE = re.compile(r"^[A-E](\.[A-Za-z0-9_=-]+)*$")

EXIT_OK = 0
EXIT_NO_MATCH = 1
EXIT_USAGE = 2


# ------------------------------------------------------------------ output


def _breadcrumb(catalog: Catalog, row: Row) -> str:
    return " > ".join(parent.ocn1 for parent in catalog.parents(row.ocn1))


def _print_rows(catalog: Catalog, rows: Sequence[Row], *, as_json: bool) -> None:
    if as_json:
        payload = []
        for row in rows:
            record = row.as_dict()
            record["parents"] = [p.ocn1 for p in catalog.parents(row.ocn1)]
            record["canonical_ocn1"] = catalog.resolve(row.ocn1)
            payload.append(record)
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return

    for index, row in enumerate(rows):
        if index:
            print()
        print(f"{row.ocn1}  {row.canonical_name}")
        print(f"  eco    {'|'.join(row.eco) or '-'}")
        print(f"  moves  {' '.join(row.moves_uci) or '-'}")
        print(f"  path   {_breadcrumb(catalog, row) or '-'}")
        if row.transposes_to:
            print(f"  canon  {row.transposes_to}")
        if row.same_as:
            print(f"  same   {'|'.join(row.same_as)}")


def _fail(message: str, *, code: int = EXIT_USAGE) -> int:
    print(f"ERROR: {message}", file=sys.stderr)
    return code


# ---------------------------------------------------------------- commands


def _cmd_lookup(args: argparse.Namespace) -> int:
    """Auto-detect what the query is and answer accordingly."""
    catalog = Catalog.load(args.catalog)
    query = " ".join(args.query).strip()
    if not query:
        return _fail("empty query")

    if ECO_RE.match(query.upper()):
        kind = "ECO code"
        rows = catalog.by_eco(query)
    else:
        kind = "OCN slug" if SLUG_RE.match(query) else "name"
        row = catalog.get(query)
        # A slug-shaped query that misses is still worth trying as text;
        # exact names beat substrings, substrings beat nothing.
        rows = (
            [row]
            if row
            else catalog.by_name(query) or catalog.search(query, limit=args.limit)
        )

    if not rows:
        return _fail(f"no OCN-1 match for {kind} {query!r}", code=EXIT_NO_MATCH)
    _print_rows(catalog, rows[: args.limit], as_json=args.json)
    return EXIT_OK


def _cmd_fen(args: argparse.Namespace) -> int:
    """Resolve a FEN to catalogue rows, normalising the en-passant field."""
    catalog = Catalog.load(args.catalog)
    fen = " ".join(args.fen).strip()
    try:
        rows = catalog.by_fen(fen)
    except ValueError as exc:
        return _fail(str(exc))

    if not rows:
        return _fail("no OCN-1 match for FEN position", code=EXIT_NO_MATCH)
    rows = sorted(rows, key=lambda row: (-row.depth, row.ocn1))
    _print_rows(catalog, rows, as_json=args.json)
    return EXIT_OK


def _cmd_uci(args: argparse.Namespace) -> int:
    """Deepest prefix match for a UCI move sequence.

    If the input runs past a catalogue tabiya, the deepest row whose
    ``moves_uci`` is still a prefix of it wins.
    """
    catalog = Catalog.load(args.catalog)
    query = " ".join(args.moves).split()
    if not query:
        return _fail("missing UCI moves")

    best: Row | None = None
    best_key: tuple[int, int, str] | None = None
    for row in catalog:
        moves = row.moves_uci
        if not moves or len(moves) > len(query):
            continue
        if tuple(query[: len(moves)]) != moves:
            continue
        key = (len(moves), row.depth, row.ocn1)
        if best_key is None or key > best_key:
            best, best_key = row, key

    if best is None or best_key is None:
        return _fail("no OCN-1 match for UCI sequence", code=EXIT_NO_MATCH)

    if args.json:
        record = best.as_dict()
        record["matched_ply"] = best_key[0]
        record["parents"] = [p.ocn1 for p in catalog.parents(best.ocn1)]
        record["canonical_ocn1"] = catalog.resolve(best.ocn1)
        print(json.dumps(record, ensure_ascii=False, indent=2))
    else:
        _print_rows(catalog, [best], as_json=False)
        print(f"  ply    {best_key[0]} of {len(query)}")
    return EXIT_OK


def _cmd_version(args: argparse.Namespace) -> int:
    """Report the reader version and the catalogue release it carries."""
    catalog_version = Catalog.load(args.catalog).version()
    if args.json:
        print(
            json.dumps(
                {"package": __version__, "catalogue": catalog_version},
                ensure_ascii=False,
            )
        )
    else:
        print(f"ocn-chess {__version__} (catalogue {catalog_version})")
    return EXIT_OK


# ------------------------------------------------------------------ parser


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ocn",
        description=(
            "Open Chess Naming: look up OCN-1 opening slugs, names and "
            "positions. The catalogue ships with the package; no network "
            "access and no other dependency is used."
        ),
        epilog="Code MIT, bundled catalogue CC-BY-4.0.",
    )
    parser.add_argument("--version", action="version", version=f"ocn-chess {__version__}")
    subcommands = parser.add_subparsers(dest="command", metavar="<command>")

    def add(name: str, help_text: str, **kwargs) -> argparse.ArgumentParser:
        sub = subcommands.add_parser(name, help=help_text, description=help_text, **kwargs)
        sub.add_argument("--json", action="store_true", help="emit JSON instead of text")
        sub.add_argument(
            "--catalog",
            metavar="PATH",
            default=None,
            help="read this catalogue CSV instead of the bundled one",
        )
        return sub

    lookup = add(
        "lookup",
        "Look up rows by ECO code (B90), OCN slug (B.Sic.Naj) or opening name.",
    )
    lookup.add_argument("query", nargs="+", help="ECO code, OCN-1 slug, or name text")
    lookup.add_argument(
        "--limit", type=int, default=10, help="maximum rows to print (default: 10)"
    )
    lookup.set_defaults(func=_cmd_lookup)

    fen = add(
        "fen",
        "Look up rows by FEN. The en-passant field is normalised to OCN's "
        "legal-capture rule and move counters are ignored.",
    )
    fen.add_argument("fen", nargs="+", help="a 4-field or 6-field FEN")
    fen.set_defaults(func=_cmd_fen)

    uci = add(
        "uci",
        "Resolve a UCI move sequence to the deepest matching OCN-1 row.",
    )
    uci.add_argument("moves", nargs="+", help="UCI moves, e.g. \"e2e4 c7c5 g1f3\"")
    uci.set_defaults(func=_cmd_uci)

    version = add("version", "Print the reader version and the catalogue release.")
    version.set_defaults(func=_cmd_version)

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)
    if not getattr(args, "func", None):
        parser.print_help()
        return EXIT_USAGE
    try:
        return args.func(args)
    except (KeyError, FileNotFoundError) as exc:
        return _fail(str(exc))
    except BrokenPipeError:  # pragma: no cover - `ocn lookup B90 | head -5`
        # Point stdout at devnull so the interpreter's final flush does
        # not report the closed pipe as an error.
        os.dup2(os.open(os.devnull, os.O_WRONLY), sys.stdout.fileno())
        return EXIT_OK


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
