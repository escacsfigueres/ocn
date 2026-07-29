"""OCN — Open Chess Naming, the OCN-1 catalogue and its reader.

Hierarchical, human-readable slugs for chess openings (``B.Sic.Naj.Eng``
= Sicilian Najdorf, English Attack), a companion to ECO rather than a
replacement. The catalogue ships inside the package, so nothing is
downloaded at import time and lookups work offline::

    from ocn import Catalog

    cat = Catalog.load()
    cat.by_slug("B.Sic.Naj.Eng").canonical_name
    cat.by_eco("B90")
    cat.by_fen("rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2")

The command line covers the same ground: ``ocn lookup B90``,
``ocn fen "<FEN>"``, ``ocn uci "e2e4 c7c5"``, ``ocn version``.

Code is MIT; the bundled catalogue and spec text are CC-BY-4.0.
"""
from __future__ import annotations

from .catalog import Catalog, Row
from .fen import fen_key

__version__ = "1.2.1.dev0"

__all__ = ["Catalog", "Row", "fen_key", "__version__"]
