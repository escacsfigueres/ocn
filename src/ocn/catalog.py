"""The OCN-1 catalogue reader.

Every consumer the 2026 audit simulated rewrote the same handful of
loops; this module is those loops, once, over typed rows, with the
catalogue bundled so nothing has to be downloaded or checked out::

    from ocn import Catalog

    cat = Catalog.load()                        # bundled ocn-1.csv
    cat.by_slug("B.Sic.Naj.Eng")                # KeyError if absent
    cat.get("B.Sic.Naj.Eng")                    # None if absent
    cat.by_fen(fen)                             # O(1), ep trap handled
    cat.by_fen_key(key)                         # the same, key already normalised
    cat.by_eco("B90")                           # deepest first
    cat.by_name("najdorf")                      # fold-insensitive exact
    cat.search("najdorf", limit=5)              # substring, broadest first
    cat.parents("B.Sic.Naj.Eng")                # breadcrumb, root to parent
    cat.children("B.Sic"); cat.walk("B.Sic")    # direct kids / whole subtree
    cat.resolve("E.Nim.Sml.Kmo")                # canonical slug
    cat.co_canonicals("D.Rub")                  # same_as partners

Position lookup goes through the bundled ``ocn-1.positions.tsv`` index:
a dict hit, never a move replay at query time. When the catalogue is
loaded from a path with no positions sidecar next to it the index is
derived by replaying ``moves_uci`` once, on first use.
"""
from __future__ import annotations

import csv
import unicodedata
from collections.abc import Iterator
from dataclasses import dataclass
from importlib import resources
from pathlib import Path

from ._chess import fen_key_after_uci
from .fen import fen_key

__all__ = ["Catalog", "Row"]

CATALOG_FILE = "ocn-1.csv"
POSITIONS_FILE = "ocn-1.positions.tsv"
XREF_FILE = "ocn-1.lichess-xref.tsv"
VERSION_FILE = "VERSION"

# Running from a checkout with no synced package data: fall back to the
# canonical catalogue the repository already carries.
_REPO_CATALOG_DIR = Path(__file__).resolve().parents[2] / "catalog"


@dataclass(frozen=True)
class Row:
    """One catalogue entry, typed.

    The CSV's pipe-separated multi-value fields (``eco_legacy``,
    ``aliases``, ``flags``, ``same_as``) arrive split; NULLs arrive as
    empty containers or ``None`` rather than empty strings, so callers
    never re-implement the same five ``.strip() or None`` idioms.
    """

    ocn1: str
    canonical_name: str
    eco: tuple[str, ...]
    parent: str | None
    moves_uci: tuple[str, ...]
    depth: int
    aliases: tuple[str, ...]
    flags: frozenset[str]
    notes: str
    attributed_to: str
    attribution_source: str
    historical_notes: str
    transposes_to: str | None
    same_as: tuple[str, ...]

    @property
    def is_class_root(self) -> bool:
        """True for the five family filters ``A``-``E``, which hold no position."""
        return not self.moves_uci

    @classmethod
    def from_csv(cls, record: dict[str, str]) -> "Row":
        """Build a row from one ``csv.DictReader`` record."""
        return cls(
            ocn1=(record.get("ocn1") or "").strip(),
            canonical_name=(record.get("canonical_name") or "").strip(),
            eco=_split_pipes(record.get("eco_legacy")),
            parent=(record.get("parent_ocn1") or "").strip() or None,
            moves_uci=tuple((record.get("moves_uci") or "").split()),
            depth=int((record.get("depth") or "0").strip() or 0),
            aliases=_split_pipes(record.get("aliases")),
            flags=frozenset(_split_pipes(record.get("flags"))),
            notes=(record.get("notes") or "").strip(),
            attributed_to=(record.get("attributed_to") or "").strip(),
            attribution_source=(record.get("attribution_source") or "").strip(),
            historical_notes=(record.get("historical_notes") or "").strip(),
            transposes_to=(record.get("transposes_to") or "").strip() or None,
            same_as=_split_pipes(record.get("same_as")),
        )

    def as_dict(self) -> dict[str, object]:
        """A JSON-serialisable view (tuples become lists, flags sort)."""
        return {
            "ocn1": self.ocn1,
            "canonical_name": self.canonical_name,
            "eco": list(self.eco),
            "parent": self.parent,
            "moves_uci": list(self.moves_uci),
            "depth": self.depth,
            "aliases": list(self.aliases),
            "flags": sorted(self.flags),
            "notes": self.notes,
            "attributed_to": self.attributed_to,
            "attribution_source": self.attribution_source,
            "historical_notes": self.historical_notes,
            "transposes_to": self.transposes_to,
            "same_as": list(self.same_as),
        }


class Catalog:
    """An in-memory OCN-1 catalogue with the lookups consumers need.

    Indexes are built lazily and cached for the object's lifetime, so a
    program that only calls :meth:`by_slug` never pays for the name-fold
    or position tables.
    """

    def __init__(self, rows: list[Row], *, positions_tsv: str | None = None) -> None:
        self._rows: list[Row] = list(rows)
        self._by_slug: dict[str, Row] = {row.ocn1: row for row in self._rows}
        self._positions_tsv = positions_tsv
        self._positions: dict[str, list[Row]] | None = None
        self._eco: dict[str, list[Row]] | None = None
        self._folded: dict[str, list[Row]] | None = None
        self._children: dict[str, list[Row]] | None = None

    # ---------------------------------------------------------------- load

    @classmethod
    def load(cls, path: Path | str | None = None) -> "Catalog":
        """Load the catalogue.

        With no argument the data bundled in the wheel is used
        (``ocn/data/ocn-1.csv`` plus its positions index), resolved
        through :mod:`importlib.resources` so it works from a wheel, a
        zipapp or an editable install alike. When that data is absent —
        a checkout that has never run ``tools/sync_package_data.py`` —
        the repository's own ``catalog/`` is used instead.

        Pass ``path`` to read a specific catalogue CSV; a sibling
        ``ocn-1.positions.tsv`` is picked up automatically if present.
        """
        if path is None:
            catalog_text = _bundled_text(CATALOG_FILE)
            positions_text = _bundled_text(POSITIONS_FILE)
            if catalog_text is None:
                catalog_text = (_REPO_CATALOG_DIR / CATALOG_FILE).read_text(
                    encoding="utf-8"
                )
                positions_text = _optional_text(_REPO_CATALOG_DIR / POSITIONS_FILE)
        else:
            catalog_path = Path(path)
            catalog_text = catalog_path.read_text(encoding="utf-8")
            positions_text = _optional_text(catalog_path.parent / POSITIONS_FILE)

        reader = csv.DictReader(catalog_text.splitlines(True))
        return cls(
            [Row.from_csv(record) for record in reader],
            positions_tsv=positions_text,
        )

    def version(self) -> str:
        """The catalogue release this data came from (``ocn/data/VERSION``).

        Distinct from ``ocn.__version__``, which versions the reader.
        Returns ``"unknown"`` when the bundled data is not present (a
        checkout falling back to ``catalog/``).
        """
        text = _bundled_text(VERSION_FILE)
        return text.strip() if text else "unknown"

    # -------------------------------------------------------------- by key

    def by_slug(self, slug: str) -> Row:
        """The row for ``slug``. Raises ``KeyError`` when absent."""
        return self._by_slug[slug]

    def get(self, slug: str) -> Row | None:
        """The row for ``slug``, or ``None`` when absent."""
        return self._by_slug.get(slug)

    def by_fen(self, fen: str) -> list[Row]:
        """Every row standing at this position, in catalogue order.

        The input is normalised with :func:`ocn.fen_key` first, so a raw
        board-library FEN (en-passant square printed after every double
        push, arbitrary move counters) matches. Multiple rows are normal
        and not an error: co-canonical names and documented
        transpositions share positions by design.
        """
        return self.by_fen_key(fen_key(fen))

    def by_fen_key(self, key: str) -> list[Row]:
        """Every row at an already-normalised position key.

        The same lookup as :meth:`by_fen` with the normalisation step
        skipped, for callers that hold a key rather than a FEN — a move
        replay asking the catalogue after every ply (``ocn annotate``)
        would otherwise re-parse and re-validate a FEN it has just built.
        A key that is not in ``fen_key`` form simply misses.
        """
        return list(self._position_index().get(key, ()))

    def by_eco(self, code: str) -> list[Row]:
        """Every row carrying this ECO code in ``eco_legacy``, deepest first.

        ECO is coarse — ``B90`` alone covers twenty OCN rows — so the
        deepest-first order puts the most specific names on top.
        """
        return list(self._eco_index().get(code.strip().upper(), ()))

    def by_name(self, text: str) -> list[Row]:
        """Rows whose canonical name or one alias equals ``text``.

        Case- and diacritic-insensitive: ``"grunfeld"`` finds the
        Grünfeld rows, ``"SICILIAN DEFENCE"`` finds the Sicilian.
        """
        return list(self._fold_index().get(_fold(text), ()))

    def search(self, text: str, limit: int = 10) -> list[Row]:
        """Rows whose canonical name or an alias contains ``text``.

        Same folding as :meth:`by_name`. Results come back broadest
        first (shallowest depth), so a truncated list keeps the family
        heads rather than an arbitrary corner of one subtree.
        """
        needle = _fold(text)
        if not needle:
            return []
        hits: dict[str, Row] = {}
        for folded, rows in self._fold_index().items():
            if needle in folded:
                for row in rows:
                    hits.setdefault(row.ocn1, row)
        ordered = sorted(hits.values(), key=lambda row: (row.depth, row.ocn1))
        return ordered if limit is None else ordered[:limit]

    # ------------------------------------------------------------ hierarchy

    def children(self, slug: str) -> list[Row]:
        """The direct children of ``slug``, in catalogue order."""
        return list(self._children_index().get(slug, ()))

    def parents(self, slug: str) -> list[Row]:
        """The breadcrumb for ``slug``: root first, immediate parent last.

        ``parents("B.Sic.Naj.Eng")`` is ``[B, B.Sic, B.Sic.Naj]``. The
        row itself is not included. Raises ``KeyError`` when ``slug`` is
        absent.
        """
        chain: list[Row] = []
        seen = {slug}
        current = self.by_slug(slug).parent
        while current and current not in seen:
            seen.add(current)
            row = self._by_slug.get(current)
            if row is None:
                break
            chain.append(row)
            current = row.parent
        chain.reverse()
        return chain

    def walk(self, slug: str) -> Iterator[Row]:
        """Yield ``slug``'s row, then its whole subtree in catalogue order."""
        yield self.by_slug(slug)
        prefix = slug + "."
        for row in self._rows:
            if row.ocn1.startswith(prefix):
                yield row

    # ------------------------------------------------------ canonicalisation

    def resolve(self, slug: str) -> str:
        """The FEN-canonical slug: follow ``transposes_to`` once.

        The catalogue contract guarantees the links never chain, so one
        hop is the whole rule. Canonical rows resolve to themselves.
        """
        return self.by_slug(slug).transposes_to or slug

    def co_canonicals(self, slug: str) -> list[str]:
        """The row's ``same_as`` partners as slugs.

        A ``same_as`` partner is *not* an alias to collapse: both slugs
        are canonical literary names for the same position.
        """
        return list(self.by_slug(slug).same_as)

    # ------------------------------------------------------------- protocol

    def __len__(self) -> int:
        return len(self._rows)

    def __iter__(self) -> Iterator[Row]:
        return iter(self._rows)

    def __repr__(self) -> str:  # pragma: no cover - debugging aid
        return f"<Catalog {self.version()}, {len(self._rows)} rows>"

    # --------------------------------------------------------------- indexes

    def _position_index(self) -> dict[str, list[Row]]:
        if self._positions is None:
            self._positions = (
                self._positions_from_sidecar()
                if self._positions_tsv
                else self._positions_from_replay()
            )
        return self._positions

    def _positions_from_sidecar(self) -> dict[str, list[Row]]:
        index: dict[str, list[Row]] = {}
        assert self._positions_tsv is not None
        reader = csv.DictReader(self._positions_tsv.splitlines(True), delimiter="\t")
        for record in reader:
            key = (record.get("fen_key") or "").strip()
            row = self._by_slug.get((record.get("ocn1") or "").strip())
            if key and row is not None:
                index.setdefault(key, []).append(row)
        return index

    def _positions_from_replay(self) -> dict[str, list[Row]]:
        """Derive the index by replaying ``moves_uci``.

        Only reached when no positions sidecar is available. It costs a
        few seconds once; every subsequent lookup is a dict hit.
        """
        index: dict[str, list[Row]] = {}
        for row in self._rows:
            if not row.moves_uci:
                continue
            index.setdefault(fen_key_after_uci(" ".join(row.moves_uci)), []).append(row)
        return index

    def _eco_index(self) -> dict[str, list[Row]]:
        if self._eco is None:
            index: dict[str, list[Row]] = {}
            for row in self._rows:
                for code in row.eco:
                    index.setdefault(code, []).append(row)
            for rows in index.values():
                rows.sort(key=lambda row: (-row.depth, row.ocn1))
            self._eco = index
        return self._eco

    def _fold_index(self) -> dict[str, list[Row]]:
        if self._folded is None:
            index: dict[str, list[Row]] = {}
            for row in self._rows:
                for name in (row.canonical_name, *row.aliases):
                    key = _fold(name)
                    if not key:
                        continue
                    bucket = index.setdefault(key, [])
                    if not bucket or bucket[-1] is not row:
                        bucket.append(row)
            self._folded = index
        return self._folded

    def _children_index(self) -> dict[str, list[Row]]:
        if self._children is None:
            index: dict[str, list[Row]] = {}
            for row in self._rows:
                if row.parent:
                    index.setdefault(row.parent, []).append(row)
            self._children = index
        return self._children


def _split_pipes(value: str | None) -> tuple[str, ...]:
    return tuple(part.strip() for part in (value or "").split("|") if part.strip())


def _fold(text: str) -> str:
    """Case- and diacritic-insensitive search key.

    NFKD decomposition then combining-mark removal, on top of
    ``casefold()``: ``"Grünfeld"`` and ``"GRUNFELD"`` fold together, per
    the spec's string-canonicalisation guidance.
    """
    decomposed = unicodedata.normalize("NFKD", text.strip().casefold())
    return "".join(char for char in decomposed if not unicodedata.combining(char))


def _bundled_text(name: str) -> str | None:
    """Read a file from the package's bundled data, or ``None`` if absent."""
    try:
        # Single-child joinpath: multi-argument joinpath on a Traversable
        # only landed in 3.11, and this package supports 3.10.
        resource = resources.files(__package__) / "data" / name
    except (ModuleNotFoundError, TypeError):  # pragma: no cover - odd loaders
        return None
    try:
        if not resource.is_file():
            return None
        return resource.read_text(encoding="utf-8")
    except (FileNotFoundError, OSError):  # pragma: no cover - odd loaders
        return None


def _optional_text(path: Path) -> str | None:
    return path.read_text(encoding="utf-8") if path.exists() else None
