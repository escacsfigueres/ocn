"""PGN annotation: tag every game with the OCN opening it reaches.

The classifier that turns "OCN is a catalogue" into "OCN names the game
in front of me". It reads a multi-game PGN, replays each mainline,
and writes two headers back::

    [ECO "B90"]
    [OCN "B.Sic.Naj.Eng"]
    [OCNName "Sicilian Najdorf, English Attack"]

Matching is **by position, not by prefix**. Every position the mainline
passes through is looked up in the catalogue's ``fen_key`` index and the
*last* hit wins, so a game that reaches the Najdorf English Attack
through 1.Nf3 is named exactly like one that plays 1.e4 — transposition
handling is a property of the method, not a special case bolted on. The
winning row is then canonicalised through ``transposes_to`` once, the
whole rule the catalogue guarantees.

Everything else in the file is passed through untouched: the movetext is
never reflowed, unknown headers keep their order and spelling, and line
endings survive. The two OCN tags are the only bytes this module owns —
existing ones are rewritten in place, so annotating twice is idempotent.

Library use::

    from ocn.annotate import Annotator, annotate_text, iter_games

    text, stats = annotate_text(open("games.pgn").read())
    print(stats.format_text())

Command line: ``ocn annotate games.pgn --stats`` (see :mod:`ocn.cli`).
"""
from __future__ import annotations

import io
import statistics
import re
from collections import Counter
from collections.abc import Iterable, Iterator, Sequence
from dataclasses import dataclass, field
from typing import TextIO

from ._chess import (
    FILES,
    MOVE_NUMBER_RE,
    RESULT_TOKENS,
    Board,
    Move,
    normalize_san_token,
    parse_san_move,
    parse_square,
)
from .catalog import Catalog, Row

__all__ = [
    "Annotator",
    "Game",
    "Match",
    "Stats",
    "DEFAULT_MAX_PLIES",
    "annotate_stream",
    "annotate_text",
    "iter_games",
    "iter_matches",
    "mainline_tokens",
]

# The deepest catalogue line is 36 plies; the slack above it covers a
# transposition that reaches a tabiya later than its own move order does.
# Replay cost is linear in this number, so it is also the knob that keeps
# a million-game run bounded.
DEFAULT_MAX_PLIES = 40

SLUG_TAG = "OCN"
NAME_TAG = "OCNName"
# Where the pair is inserted: right after the classification header a
# reader already looks at, else after the last of the Seven Tag Roster.
ANCHOR_TAGS = ("ECO", "Round")

_HEADER_RE = re.compile(r'^\[\s*([A-Za-z0-9_]+)\s+"(.*)"\s*\]$')
# One normalised SAN move. `x`, check and mate markers carry no
# information a legality test does not already have, so they are parsed
# and dropped rather than verified.
_SAN_RE = re.compile(
    r"^(?:"
    r"(?P<castle>O-O(?:-O)?)"
    r"|(?P<piece>[KQRBN])?(?P<file>[a-h])?(?P<rank>[1-8])?x?"
    r"(?P<dest>[a-h][1-8])(?:=(?P<promotion>[QRBN]))?"
    r")$"
)
_WORD_BREAKS = frozenset("{}();")


# ------------------------------------------------------------------- games


@dataclass(frozen=True)
class Game:
    """One PGN game, kept as the exact lines it was read from.

    ``lead`` holds whatever separated this game from the previous one
    (blank lines, stray text before the first game). Concatenating
    ``lead + header_lines + movetext_lines`` over every game of a file
    reproduces that file byte for byte.
    """

    lead: tuple[str, ...] = ()
    header_lines: tuple[str, ...] = ()
    movetext_lines: tuple[str, ...] = ()

    @property
    def text(self) -> str:
        """The game exactly as it was read."""
        return "".join(self.lead + self.header_lines + self.movetext_lines)

    @property
    def movetext(self) -> str:
        return "".join(self.movetext_lines)

    def header(self, name: str) -> str | None:
        """The value of a PGN tag, or ``None``. Tag names fold in case."""
        wanted = name.lower()
        for line in self.header_lines:
            parsed = _parse_header(line)
            if parsed and parsed[0].lower() == wanted:
                return parsed[1]
        return None


def iter_games(lines: Iterable[str]) -> Iterator[Game]:
    """Split a PGN line stream into games, losing nothing.

    Games are delimited the way the PGN standard describes them: a tag
    pair section, then movetext, then the next tag pair section. A ``[``
    inside a ``{}`` comment does not start a game, which is the one trap
    a naive line split falls into.

    The input is an iterable of lines *with* their endings, so a 1 GB
    file streams through without being read into memory.
    """
    lead: list[str] = []
    header: list[str] = []
    body: list[str] = []
    in_comment = False

    for line in lines:
        if not header:
            (header if _looks_like_header(line) else lead).append(line)
            continue
        if not body:
            if _looks_like_header(line):
                header.append(line)
                continue
            body.append(line)
            in_comment = _comment_state(line, in_comment)
            continue
        if not in_comment and _looks_like_header(line):
            yield Game(tuple(lead), tuple(header), tuple(body))
            lead, header, body = [], [line], []
            in_comment = False
            continue
        body.append(line)
        in_comment = _comment_state(line, in_comment)

    if header:
        yield Game(tuple(lead), tuple(header), tuple(body))


def mainline_tokens(movetext: str) -> list[str]:
    """The mainline SAN tokens of a movetext, variations skipped.

    ``_chess.pgn_tokens`` strips comments and variations with a regular
    expression, which cannot see nesting: ``(1... e5 (2. d4))`` leaves a
    stray ``)`` and a phantom move behind. This scanner tracks depth
    instead, so nested variations, comments inside variations and ``;``
    rest-of-line comments all disappear cleanly — and only the mainline
    comes back, which is the line an annotation is about.

    Move numbers, NAGs (``$1``), suffix annotations (``!?``) and result
    tokens are dropped; the SAN tokens are returned as written.
    """
    tokens: list[str] = []
    index = 0
    length = len(movetext)
    depth = 0

    while index < length:
        char = movetext[index]
        if char == "{":
            end = movetext.find("}", index + 1)
            index = length if end < 0 else end + 1
            continue
        if char == ";":
            end = movetext.find("\n", index + 1)
            index = length if end < 0 else end + 1
            continue
        if char == "<":  # reserved by the standard, never movetext
            end = movetext.find(">", index + 1)
            index = length if end < 0 else end + 1
            continue
        if char == "(":
            depth += 1
            index += 1
            continue
        if char == ")":
            depth = max(0, depth - 1)
            index += 1
            continue
        if char.isspace():
            index += 1
            continue

        start = index
        while index < length and not movetext[index].isspace() and movetext[index] not in _WORD_BREAKS:
            index += 1
        if depth:
            continue
        token = _strip_move_number(movetext[start:index])
        if not token or token in RESULT_TOKENS or token.startswith("$"):
            continue
        tokens.append(token)

    return tokens


# ------------------------------------------------------------------ result


@dataclass(frozen=True)
class Match:
    """What the annotator found in one game.

    ``ply`` is the depth in plies at which the winning position stood —
    the "how deep did OCN get" number the stats summarise. ``plies`` is
    how much of the mainline was replayed at all, and ``error`` carries
    the reason replay stopped early (an unreadable SAN token in a game
    the file otherwise keeps).
    """

    slug: str | None = None
    name: str | None = None
    ply: int = 0
    plies: int = 0
    error: str | None = None

    @property
    def matched(self) -> bool:
        return self.slug is not None


@dataclass
class Stats:
    """Running classification totals over a PGN corpus."""

    games: int = 0
    matched: int = 0
    errors: int = 0
    depths: list[int] = field(default_factory=list)
    openings: Counter = field(default_factory=Counter)

    def add(self, match: Match) -> None:
        self.games += 1
        if match.error:
            self.errors += 1
        if match.matched:
            self.matched += 1
            self.depths.append(match.ply)
            self.openings[(match.slug, match.name)] += 1

    @property
    def match_rate(self) -> float:
        """Matched games as a percentage of games seen."""
        return 100.0 * self.matched / self.games if self.games else 0.0

    @property
    def median_ply(self) -> float:
        """Median depth in plies over the matched games (0.0 when none)."""
        return float(statistics.median(self.depths)) if self.depths else 0.0

    def top(self, limit: int = 10) -> list[tuple[str, str, int]]:
        """The most frequent openings as ``(slug, name, count)``."""
        ordered = sorted(self.openings.items(), key=lambda item: (-item[1], item[0][0]))
        return [(slug, name, count) for (slug, name), count in ordered[:limit]]

    def as_dict(self, limit: int = 10) -> dict[str, object]:
        return {
            "games": self.games,
            "matched": self.matched,
            "match_rate": round(self.match_rate, 2),
            "median_ply": self.median_ply,
            "errors": self.errors,
            "top": [
                {"ocn1": slug, "canonical_name": name, "games": count}
                for slug, name, count in self.top(limit)
            ],
        }

    def format_text(self, limit: int = 10) -> str:
        """A human summary, the shape ``--stats`` prints to stderr."""
        top = self.top(limit)
        counts = [self.games, self.matched, self.errors, *(count for _, _, count in top)]
        median = f"{self.median_ply:,.1f}"
        width = max(len(median), *(len(f"{count:,}") for count in counts))
        lines = [
            f"games         {self.games:>{width},}",
            f"matched       {self.matched:>{width},}  ({self.match_rate:.1f}%)",
            f"median depth  {median:>{width}} plies",
            f"errors        {self.errors:>{width},}",
        ]
        if top:
            slug_width = max(len(slug) for slug, _, _ in top)
            lines.append("")
            lines.append(f"top {len(top)} openings")
            lines.extend(
                f"  {count:>{width},}  {slug:<{slug_width}}  {name}"
                for slug, name, count in top
            )
        return "\n".join(lines)


# --------------------------------------------------------------- annotator


class Annotator:
    """Classifies games against one loaded catalogue.

    The catalogue is loaded once and its position index built once, so
    annotating a file is one setup cost plus a move replay per game.
    """

    def __init__(
        self,
        catalog: Catalog | None = None,
        *,
        max_plies: int = DEFAULT_MAX_PLIES,
    ) -> None:
        self.catalog = Catalog.load() if catalog is None else catalog
        self.max_plies = max_plies

    def match_tokens(self, tokens: Sequence[str]) -> Match:
        """Replay SAN tokens and return the deepest position match."""
        board = Board()
        best: list[Row] | None = None
        best_ply = 0
        played = 0
        error: str | None = None

        limit = self.max_plies if self.max_plies > 0 else len(tokens)
        for token in tokens[:limit]:
            try:
                move = _resolve_san(board, token)
            except ValueError as exc:
                error = str(exc)
                break
            board._push_unchecked(move)
            played += 1
            rows = self.catalog.by_fen_key(board.fen_key())
            if rows:
                best, best_ply = rows, played

        if best is None:
            return Match(plies=played, error=error)
        row = _preferred(best)
        slug = self.catalog.resolve(row.ocn1)
        canonical = self.catalog.get(slug) or row
        return Match(
            slug=slug,
            name=canonical.canonical_name,
            ply=best_ply,
            plies=played,
            error=error,
        )

    def match_game(self, game: Game) -> Match:
        return self.match_tokens(mainline_tokens(game.movetext))

    def annotate_game(self, game: Game) -> tuple[str, Match]:
        """The game's text with the OCN tags applied, and what was found."""
        match = self.match_game(game)
        headers = _apply_tags(game.header_lines, match)
        return "".join(game.lead) + "".join(headers) + game.movetext, match


def iter_matches(
    lines: Iterable[str], annotator: Annotator
) -> Iterator[tuple[Game, Match]]:
    """Classify a PGN stream without building any output.

    The path ``tools/coverage_stat.py`` takes over a corpus too large to
    rewrite.
    """
    for game in iter_games(lines):
        yield game, annotator.match_game(game)


def annotate_stream(lines: Iterable[str], annotator: Annotator, out: TextIO) -> Stats:
    """Annotate a PGN stream game by game, writing as it goes."""
    stats = Stats()
    for game in iter_games(lines):
        text, match = annotator.annotate_game(game)
        out.write(text)
        stats.add(match)
    return stats


def annotate_text(
    text: str,
    *,
    catalog: Catalog | None = None,
    annotator: Annotator | None = None,
    max_plies: int = DEFAULT_MAX_PLIES,
) -> tuple[str, Stats]:
    """Annotate a PGN held in memory; returns the new text and the stats."""
    if annotator is None:
        annotator = Annotator(catalog, max_plies=max_plies)
    buffer = io.StringIO()
    stats = annotate_stream(text.splitlines(keepends=True), annotator, buffer)
    return buffer.getvalue(), stats


# ----------------------------------------------------------------- headers


def _looks_like_header(line: str) -> bool:
    stripped = line.strip()
    return stripped.startswith("[") and stripped.endswith("]")


def _parse_header(line: str) -> tuple[str, str] | None:
    matched = _HEADER_RE.match(line.strip())
    return (matched.group(1), matched.group(2)) if matched else None


def _comment_state(line: str, in_comment: bool) -> bool:
    """Track whether a ``{}`` comment is still open at the end of a line."""
    for char in line:
        if in_comment:
            if char == "}":
                in_comment = False
        elif char == "{":
            in_comment = True
        elif char == ";":
            break  # rest-of-line comment: cannot open or close a brace
    return in_comment


def _escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def _apply_tags(header_lines: Sequence[str], match: Match) -> list[str]:
    """Rewrite the OCN tag pair inside a header block.

    Any tags this module owns are dropped first, so re-annotating a file
    replaces stale names instead of stacking duplicates, and an unmatched
    game is left with no OCN claim at all.
    """
    kept = [
        line
        for line in header_lines
        if (_parse_header(line) or ("", ""))[0] not in (SLUG_TAG, NAME_TAG)
    ]
    if not match.matched:
        return kept

    newline = _newline_of(kept)
    index = _anchor_index(kept)
    if index and not kept[index - 1].endswith("\n"):
        kept[index - 1] += newline
    tags = [
        f'[{SLUG_TAG} "{_escape(match.slug or "")}"]{newline}',
        f'[{NAME_TAG} "{_escape(match.name or "")}"]{newline}',
    ]
    return kept[:index] + tags + kept[index:]


def _anchor_index(header_lines: Sequence[str]) -> int:
    for tag in ANCHOR_TAGS:
        for position in range(len(header_lines) - 1, -1, -1):
            parsed = _parse_header(header_lines[position])
            if parsed and parsed[0].lower() == tag.lower():
                return position + 1
    return len(header_lines)


def _newline_of(lines: Sequence[str]) -> str:
    for line in lines:
        if line.endswith("\r\n"):
            return "\r\n"
        if line.endswith("\n"):
            return "\n"
    return "\n"


# -------------------------------------------------------------- move logic


def _strip_move_number(token: str) -> str:
    while True:
        cleaned = MOVE_NUMBER_RE.sub("", token, count=1)
        if cleaned == token:
            return token.strip()
        token = cleaned


def _resolve_san(board: Board, token: str) -> Move:
    """Turn one SAN token into the legal move it names.

    ``_chess.parse_san_move`` answers the same question by generating
    every legal move and rendering each one as SAN — correct, and far too
    slow for a corpus, because rendering SAN needs its own disambiguation
    pass per candidate. This reads the token instead and tests only the
    pieces that could possibly be meant. Anything the pattern does not
    recognise falls back to ``parse_san_move``, which is authoritative.
    """
    text = normalize_san_token(token)
    parsed = _SAN_RE.match(text)
    if not parsed:
        return parse_san_move(board, token)

    white = board.white_to_move
    castle = parsed.group("castle")
    if castle:
        rank = 0 if white else 7
        move = Move(rank * 8 + 4, rank * 8 + (2 if castle == "O-O-O" else 6))
        if not board.is_legal(move):
            raise ValueError(f"no legal match for SAN move '{token}'")
        return move

    piece = parsed.group("piece") or "P"
    piece = piece if white else piece.lower()
    destination = parse_square(parsed.group("dest"))
    promotion = (parsed.group("promotion") or "").lower()
    from_file = FILES.index(parsed.group("file")) if parsed.group("file") else None
    from_rank = int(parsed.group("rank")) - 1 if parsed.group("rank") else None

    found: Move | None = None
    for square, occupant in enumerate(board.squares):
        if occupant != piece:
            continue
        if from_file is not None and square % 8 != from_file:
            continue
        if from_rank is not None and square // 8 != from_rank:
            continue
        move = Move(square, destination, promotion)
        if not board.is_legal(move):
            continue
        if found is not None:
            raise ValueError(f"ambiguous SAN move '{token}'")
        found = move

    if found is None:
        raise ValueError(f"no legal match for SAN move '{token}'")
    return found


def _preferred(rows: Sequence[Row]) -> Row:
    """Pick one row among the several a position can carry.

    Canonical rows first (a ``transposes_to`` row is by definition a
    pointer to one of its neighbours here), then the deepest, then the
    slug — so the choice is stable across runs and catalogue order.
    """
    return min(
        rows, key=lambda row: (row.transposes_to is not None, -row.depth, row.ocn1)
    )
