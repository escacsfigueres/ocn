#!/usr/bin/env python3
"""Build the static OCN web explorer into `web/dist/` (roadmap H2.3).

The explorer is a directory of files: three static assets copied verbatim
and one generated payload, `data/ocn.json`. There is no server, no build
toolchain, no bundler and no external request at runtime -- `python3
web/build.py` then any static file host is the whole deployment story.

## What the payload is

`data/ocn.json` is the display projection of the catalogue, not a second
copy of it. It reuses the H1.2 export logic (`tools/build_json_export.py`
for `moves_san` and the pipe splitters, `tools/export_positions.py` for
the position replay) and then applies the three display decisions H2.3
asks for:

- **`notes` is dropped entirely.** The July 2026 audit measured ~49% of
  the column as template boilerplate ("(move) in/against the (parent)");
  showing it would make the row pages look padded, and no honest reader
  gains anything from "6.Be3." under a movetext that already says 6.Be3.
- **Synthetic aliases are dropped**: a lone `Main Line` (398 rows) and
  the `<SAN> Line` shape (`Nf6 Line`, `O-O Line`, ~1,730 rows). These are
  the strings roadmap H2.6 deletes from the catalogue itself; the
  explorer must not display them in the meantime. Real aliases survive
  untouched, including near-synthetic ones the H2.6 lot does not name
  (`Castled Line`, `Fianchetto Line`) -- this filter matches H2.6's
  scope exactly rather than inventing a wider one.
- **Every row gains `fen`**, so the board renderer never has to replay
  moves in the browser. The five class roots are filters rather than
  positions and get the standard initial position, which is the honest
  rendering of "no moves played yet".

Fields that no view uses are left out (`moves_uci` -- the SAN movetext
and the FEN cover every display and link need; `eco_legacy` -- the `eco`
array replaces it). Empty fields are omitted rather than emitted as `""`
or `[]`, which is most of the size saving: 26 rows carry attribution,
112 carry `transposes_to`.

Output is deterministic: catalogue row order, fixed key order per row, so
two builds of the same catalogue are byte-identical.

Usage:
    python3 web/build.py [--out web/dist] [--pretty] [--version ocn-1.2.0]

Serve the result with any static file server:
    python3 -m http.server -d web/dist 8000
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
import sys
from pathlib import Path

WEB_DIR = Path(__file__).resolve().parent
REPO_ROOT = WEB_DIR.parent
sys.path.insert(0, str(REPO_ROOT / "tools"))

from build_json_export import (  # noqa: E402
    detect_version,
    load_catalog,
    moves_san,
    split_pipe,
)
from export_positions import replay  # noqa: E402

DEFAULT_CATALOG = REPO_ROOT / "catalog" / "ocn-1.csv"
DEFAULT_XREF = REPO_ROOT / "catalog" / "ocn-1.lichess-xref.tsv"
DEFAULT_OUT = WEB_DIR / "dist"

#: Copied verbatim into the output directory, in this order.
STATIC_ASSETS = ("index.html", "app.js", "style.css")

SCHEMA = "ocn.web.v1"
GENERATED_NOTE = (
    "display projection of catalog/ocn-1.csv: notes dropped, synthetic "
    "aliases dropped, fen added. Canonical source is the CSV."
)

#: The position every game starts from. The five class roots (`A`..`E`)
#: have no `moves_uci`, so this is what their board shows.
START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

#: A single SAN move: castling, or an optionally disambiguated piece or
#: pawn move with optional capture, promotion and check/mate suffix.
SAN_MOVE_RE = re.compile(
    r"^(?:O-O(?:-O)?|(?:[KQRBN][a-h1-8]?|[a-h])?x?[a-h][1-8](?:=[QRBN])?)[+#]?$"
)

#: The bare alias roadmap H2.6 deletes alongside the `<SAN> Line` lot.
MAIN_LINE_ALIAS = "Main Line"

LINE_SUFFIX = " Line"

#: Banned as a separator across the whole project (an AI tell). The build
#: refuses to ship an asset containing one.
MIDDLE_DOT = "·"


def row_fen(moves_uci: str) -> str:
    """The complete FEN of a UCI line, via `export_positions.replay`.

    Tolerant of both shapes that helper has carried: the original
    `(fen_key, fen)` pair and the richer position record H2.8 introduces.
    The explorer only ever wants the complete FEN, so it asks for it by
    name first and falls back to the pair's second slot.
    """
    position = replay(moves_uci)
    fen = getattr(position, "fen", None)
    return fen if fen else position[1]


def is_synthetic_alias(alias: str) -> bool:
    """True for the two alias shapes H2.6 classifies as generated noise.

    A lone ``Main Line`` and the ``<SAN> Line`` family (``Nf6 Line``,
    ``O-O Line``, ``Bxf6 Line``). Anything else is a real alias, including
    ``Castled Line`` and ``Fianchetto Line``: they read synthetic but are
    outside the lot H2.6 names, and the explorer suppresses only what the
    catalogue is committed to deleting.
    """
    alias = alias.strip()
    if alias == MAIN_LINE_ALIAS:
        return True
    if not alias.endswith(LINE_SUFFIX):
        return False
    return bool(SAN_MOVE_RE.match(alias[: -len(LINE_SUFFIX)]))


def display_aliases(raw: str) -> list[str]:
    """Pipe-split an alias cell, with the synthetic shapes removed."""
    return [a for a in split_pipe(raw) if not is_synthetic_alias(a)]


def load_xref(path: Path) -> dict[str, dict[str, str]]:
    """The Lichess cross-reference keyed by slug (`ocn1`)."""
    with path.open(newline="", encoding="utf-8") as f:
        return {
            row["ocn1"]: row
            for row in csv.DictReader(f, delimiter="\t")
        }


def build_row(row: dict[str, str], xref: dict[str, dict[str, str]]) -> dict[str, object]:
    """One catalogue row as the explorer sees it. Empty fields are omitted."""
    slug = (row.get("ocn1") or "").strip()
    moves_uci = (row.get("moves_uci") or "").strip()
    out: dict[str, object] = {
        "slug": slug,
        "name": (row.get("canonical_name") or "").strip(),
        "depth": int(row.get("depth") or 0),
    }
    parent = (row.get("parent_ocn1") or "").strip()
    if parent:
        out["parent"] = parent

    if moves_uci:
        out["san"] = moves_san(moves_uci)
        out["fen"] = row_fen(moves_uci)
    else:
        out["fen"] = START_FEN

    for key, source in (("eco", "eco_legacy"), ("flags", "flags")):
        values = split_pipe(row.get(source, ""))
        if values:
            out[key] = values
    aliases = display_aliases(row.get("aliases", ""))
    if aliases:
        out["aliases"] = aliases

    transposes_to = (row.get("transposes_to") or "").strip()
    if transposes_to:
        out["transposes_to"] = transposes_to
    same_as = split_pipe(row.get("same_as", ""))
    if same_as:
        out["same_as"] = same_as

    # The attribution block renders only when there is an attribution:
    # 26 rows today, and a blank block on the other 5,873 would advertise
    # the gap rather than the work.
    attributed_to = (row.get("attributed_to") or "").strip()
    if attributed_to:
        out["attributed_to"] = attributed_to
        for key in ("attribution_source", "historical_notes"):
            value = (row.get(key) or "").strip()
            if value:
                out[key] = value

    entry = xref.get(slug) or {}
    lichess_name = (entry.get("lichess_name") or "").strip()
    if lichess_name:
        out["lichess"] = {
            "name": lichess_name,
            "eco": (entry.get("lichess_eco") or "").strip(),
            "kind": (entry.get("match_kind") or "").strip(),
        }
    return out


def build_document(
    catalog: Path = DEFAULT_CATALOG,
    xref_path: Path = DEFAULT_XREF,
    version: str | None = None,
) -> dict[str, object]:
    xref = load_xref(xref_path)
    rows = [build_row(row, xref) for row in load_catalog(catalog)]
    return {
        "schema": SCHEMA,
        "catalog_version": version or detect_version(),
        "generated_note": GENERATED_NOTE,
        "rows": rows,
    }


def render_json(document: dict[str, object], pretty: bool = False) -> str:
    if pretty:
        text = json.dumps(document, ensure_ascii=False, indent=2)
    else:
        text = json.dumps(document, ensure_ascii=False, separators=(",", ":"))
    return text + "\n"


def check_no_middle_dot(name: str, text: str) -> None:
    """Fail the build on U+00B7 anywhere in a shipped asset."""
    if MIDDLE_DOT in text:
        raise ValueError(
            f"{name} contains U+00B7 (middle dot), banned as a separator"
        )


def build_dist(
    out_dir: Path = DEFAULT_OUT,
    catalog: Path = DEFAULT_CATALOG,
    xref_path: Path = DEFAULT_XREF,
    version: str | None = None,
    pretty: bool = False,
) -> dict[str, object]:
    """Write the whole site into `out_dir`. Returns the built document."""
    document = build_document(catalog, xref_path, version)
    payload = render_json(document, pretty)
    check_no_middle_dot("data/ocn.json", payload)

    out_dir.mkdir(parents=True, exist_ok=True)
    for asset in STATIC_ASSETS:
        source = WEB_DIR / asset
        text = source.read_text(encoding="utf-8")
        check_no_middle_dot(asset, text)
        shutil.copyfile(source, out_dir / asset)

    data_dir = out_dir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    (data_dir / "ocn.json").write_text(payload, encoding="utf-8")
    return document


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build the static OCN web explorer into web/dist."
    )
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    parser.add_argument("--xref", type=Path, default=DEFAULT_XREF)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT,
                        help="Output directory (default: web/dist).")
    parser.add_argument("--pretty", action="store_true",
                        help="Indent the JSON payload (larger, readable).")
    parser.add_argument("--version", default=None,
                        help="Value for catalog_version; defaults to the "
                             "most recent git tag.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(sys.argv[1:] if argv is None else argv)
    for path, label in ((args.catalog, "catalogue"), (args.xref, "xref")):
        if not path.exists():
            print(f"ERROR: {label} not found: {path}", file=sys.stderr)
            return 1

    try:
        document = build_dist(
            args.out, args.catalog, args.xref, args.version, args.pretty
        )
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    rows = document["rows"]
    assert isinstance(rows, list)
    payload = args.out / "data" / "ocn.json"
    total = sum(
        (args.out / asset).stat().st_size for asset in STATIC_ASSETS
    ) + payload.stat().st_size
    print(
        f"wrote {args.out} ({len(rows)} rows, "
        f"catalog_version {document['catalog_version']}, "
        f"payload {payload.stat().st_size / 1024:.0f} KB, "
        f"site {total / 1024:.0f} KB)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
