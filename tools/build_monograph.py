"""OCN Monograph C — The Ruy López. The complete volume.

Every named line with its own diagram and figures, plus the structural
graphics: a radial dendrogram of the whole naming tree, a flow diagram of
master practice through the first levels, and the rankings.

Pieces are declared once as SVG symbols and referenced, so 328 boards cost
roughly one board's worth of geometry.
"""

import base64
import csv
import math
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

OCN = Path(__file__).resolve().parents[1]      # the repository root


def _git(*args):
    import subprocess
    try:
        return subprocess.run(["git", "-C", str(OCN), *args], capture_output=True,
                              text=True, timeout=20).stdout.strip() or "unknown"
    except Exception:                                        # noqa: BLE001
        return "unknown"


_COMMIT = _git("rev-parse", "--short", "HEAD")
_BUILT = _git("log", "-1", "--format=%cs")
for p in (OCN / "tools", OCN / "web"):
    sys.path.insert(0, str(p))

from build import row_fen  # noqa: E402

HERE = Path(__file__).resolve().parent / "monograph"   # cached inputs and output
FAMILY, ROOT = "c", "C.RyL"
# The OCN identity lives in the separate ocn-logo-system workspace, which this
# repository does not depend on. What the monograph needs from it is four
# colours and two drawings, so the colours are stated here and the drawings are
# snapshotted into web/brand. To refresh either, re-run
# `build_ocn_assets.lockup_horizontal_svg("c")` and `micro_svg("c")` there.
BAND, NAMING = "#F0C053", "#654F1E"     # family C band, and its text tone
INK, PAPER = "#15171a", "#f6f6f3"
BRAND = OCN / "web" / "brand"
H_TOTAL_WIDTH = 745.242                 # width of the horizontal lockup's viewBox

# ------------------------------------------------------------------ data

def tsv(n):
    return list(csv.DictReader((OCN / "catalog" / n).open(), delimiter="\t"))

CATALOG = {r["ocn1"]: r for r in csv.DictReader((OCN / "catalog" / "ocn-1.csv").open())}
RYL = {k: v for k, v in CATALOG.items() if k == ROOT or k.startswith(ROOT + ".")}
POP = {r["ocn1"]: r for r in tsv("ocn-1.popularity.tsv") if r["ocn1"] in RYL}
_RETRIEVED = next((r.get("retrieved", "") for r in POP.values() if r.get("retrieved")),
                  "unknown")
WCH = [r for r in tsv("ocn-1.wch.tsv") if r["ocn1"] in RYL]
CLAIMS = [r for r in tsv("ocn-1.claims.tsv") if r["ocn1"] in RYL]
XREF = {r["ocn1"]: r for r in tsv("ocn-1.lichess-xref.tsv") if r["ocn1"] in RYL}
PROPOSED = [r for r in csv.DictReader(
    (OCN / "docs/evidence/provenance/named-after-person.proposed.tsv").open(),
    delimiter="\t") if r["ocn1"] in RYL]
PROP_PEOPLE = {r["person_id"]: r for r in csv.DictReader(
    (OCN / "docs/evidence/provenance/people-proposed-additions.tsv").open(),
    delimiter="\t")}
PEOPLE = {r["person_id"]: r for r in tsv("ocn-1.people.tsv")}
BASIS = {r["ocn1"]: r for r in tsv("ocn-1.name_basis.tsv") if r["ocn1"] in RYL}
ATTRSIDE = {r["ocn1"]: r for r in tsv("ocn-1.attribution.tsv") if r["ocn1"] in RYL}
GAME_TAGS = {}
try:
    for _r in csv.DictReader((HERE / "game-tags.tsv").open(), delimiter="\t"):
        GAME_TAGS[_r["lichess_id"]] = _r
except FileNotFoundError:
    pass

MONTHS = ("January February March April May June July August September "
          "October November December").split()

def pretty_date(d):
    """1846.03.07 -> 7 March 1846; partial dates degrade to what is known."""
    if not d:
        return ""
    parts = [x for x in d.split(".") if x and x[0].isdigit()]
    if len(parts) == 3 and parts[1] != "??" and parts[2] != "??":
        try:
            return f"{int(parts[2])} {MONTHS[int(parts[1]) - 1]} {parts[0]}"
        except (ValueError, IndexError):
            return parts[0]
    return parts[0] if parts else ""

def where(gid):
    """Event and place for a proposal game, as one phrase."""
    t = GAME_TAGS.get(gid or "", {})
    ev, si = t.get("event", "").strip(), t.get("site", "").strip()
    if si.endswith(" INT"):
        si = si[:-4] + ", online"
    bits = [b for b in (ev, si) if b]
    return ", ".join(bits)

def _fix_name(n):
    """The game proposal spells one player three ways and doubles the stop on
    79 rows. Normalising is display-only: the proposal file keeps its defect
    until it is fixed at the source, and this makes the book readable now."""
    n = re.sub(r"\.\.+$", ".", (n or "").strip())
    m = re.match(r"^([^,]+),\s*([A-Z])\.$", n)
    if m and (m.group(1), m.group(2)) in _FULL_NAME:
        return f"{m.group(1)}, {_FULL_NAME[(m.group(1), m.group(2))]}"
    m = re.match(r"^([^,]+),\s*(.+)$", n)
    if m and (m.group(1), m.group(2).lower()) in _CANON:
        return f"{m.group(1)}, {_CANON[(m.group(1), m.group(2).lower())]}"
    return n


# The proposal spells given names three ways: full, initialled, and truncated
# mid-word ("Nakamura, Hi", "Karpov, Ana"). Variants are collapsed onto the
# longest only when every shorter one is a prefix of it, so two genuinely
# different players who share a surname and an initial stay two people.
_seen = defaultdict(set)
for _r in list(csv.DictReader(
        (OCN / "docs/evidence/provenance/notable-games.tsv").open(),
        delimiter="\t")) + WCH:
    for _k in ("white", "black"):
        _m = re.match(r"^([^,]+),\s*([A-Za-z][A-Za-z]+(?: [A-Z][a-z]+)*)$",
                      (_r.get(_k) or "").strip())
        if _m:
            _seen[(_m.group(1), _m.group(2)[0].upper())].add(_m.group(2))

_FULL_NAME, _CANON = {}, {}
for (_sur, _ini), _vars in _seen.items():
    _long = max(_vars, key=len)
    if all(_long.lower().startswith(v.lower()) for v in _vars):
        _FULL_NAME[(_sur, _ini)] = _long
        for _v in _vars:
            _CANON[(_sur, _v.lower())] = _long

for _r in WCH:
    _r["white"], _r["black"] = _fix_name(_r["white"]), _fix_name(_r["black"])

# top_player comes from catalog/ocn-1.popularity.tsv, which carries the same
# defect. Normalised here for reading; the catalogue itself is unchanged.
for _r in POP.values():
    if _r.get("top_player"):
        _r["top_player"] = _fix_name(_r["top_player"])


def short_player(n, limit=18):
    """Full name where it fits, otherwise back to the initialled form, so the
    rankings column never cuts a person off mid-name."""
    if len(n) <= limit:
        return n
    m = re.match(r"^([^,]+),\s*(\S)", n)
    return f"{m.group(1)}, {m.group(2)}." if m else n[:limit]

NOTABLE = defaultdict(list)
for r in csv.DictReader((OCN / "docs/evidence/provenance/notable-games.tsv").open(), delimiter="\t"):
    if r["ocn1"] in RYL:
        r["white"], r["black"] = _fix_name(r["white"]), _fix_name(r["black"])
        NOTABLE[r["ocn1"]].append(r)
for v in NOTABLE.values():
    v.sort(key=lambda g: -(int(g["white_elo"] or 0) + int(g["black_elo"] or 0)))
WCH_GAMES = defaultdict(list)
for r in WCH:
    # the citation carries the place: "...World Championship 6th, Moscow RUS, 1896"
    # The citation begins with exactly "{white}-{black}", and both names carry a
    # comma, so splitting the whole string on commas hands back fragments of the
    # players as though they were places. Strip the pair first; it is verified to
    # be there on every row.
    _cit = r.get("citation", "")
    _pair = f'{r["white"]}-{r["black"]}'
    if _cit.startswith(_pair):
        _cit = _cit[len(_pair):].lstrip(", ")
    bits = [b.strip() for b in _cit.split(",")]
    place = ""
    for b in bits:
        if b and b != r["event"] and not b[0].isdigit() and " wch-m" not in b \
                and r["white"].split(",")[0] not in b and r["black"].split(",")[0] not in b:
            place = re.sub(r"\s+(wch-m|RUS|USA|GER|NED|ESP|FRA|ARG|SUI|SWE|YUG|URS|ENG)$",
                           "", b).strip()
            if place:
                break
    r = dict(r, place=place)
    WCH_GAMES[r["ocn1"]].append(r)
# Earliest game on record for a line, computed over its whole subtree: a game
# played in a sub-line is a game of the line it refines. Computing it per exact
# slug gave the Morphy Defence a first game of 2019, because the game sample is
# selected by rating and every top-rated game filed on the bare parent is modern.
_EXACT = defaultdict(list)
for _src in (NOTABLE, WCH_GAMES):
    for _k, _v in _src.items():
        for _g in _v:
            if _g.get("year", "").isdigit():
                _EXACT[_k].append((int(_g["year"]), _g))

FIRST_GAME = {}

def subtree(s0):
    out = [s0]
    for k in CHILDREN.get(s0, []):
        out += subtree(k)
    return out


def _earliest(slug):
    best = None
    for x in subtree(slug):
        for cand in _EXACT.get(x, []):
            if best is None or cand[0] < best[0]:
                best = cand
    return best



def dendrogram(root_slug, width=470, per_leaf=9.0, max_h=452):
    nodes = subtree(root_slug)
    leaves = [n for n in nodes if not CHILDREN.get(n)]
    if len(nodes) < 2:
        return ""
    li = {n: i for i, n in enumerate(leaves)}
    ypos = {}
    def ycoord(n):
        if n in ypos:
            return ypos[n]
        kids = CHILDREN.get(n, [])
        v = li[n] if not kids else sum(ycoord(k) for k in kids) / len(kids)
        ypos[n] = v
        return v
    ycoord(root_slug)
    d0 = int(CATALOG[root_slug]["depth"])
    maxd = max(int(CATALOG[n]["depth"]) for n in nodes)
    span = max(maxd - d0, 1)
    h = min(max(len(leaves) * per_leaf + 14, 46), max_h)
    scale = (h - 14) / max(len(leaves) - 1, 1)
    xs = lambda n: 8 + (int(CATALOG[n]["depth"]) - d0) / span * (width - 150)
    ys = lambda n: 7 + ycoord(n) * scale
    parts = []
    for n in nodes:
        if n == root_slug:
            continue
        pnt = CATALOG[n]["parent_ocn1"]
        x1, y1, x2, y2 = xs(pnt), ys(pnt), xs(n), ys(n)
        dd = int(CATALOG[n]["depth"]) - d0
        parts.append(f'<path d="M{x1:.1f} {y1:.1f}H{(x1+x2)/2:.1f}V{y2:.1f}H{x2:.1f}" '
                     f'stroke="{NAMING if dd<=1 else "#b9b2a2"}" stroke-width="{1.1 if dd<=1 else .6}" '
                     f'fill="none" opacity="{.9 if dd<=1 else .6}"/>')
    for n in nodes:
        g = games(n)
        r = 1.1 + (2.4 * (math.log10(g + 1) / 6) if g else 0)
        parts.append(f'<circle cx="{xs(n):.1f}" cy="{ys(n):.1f}" r="{r:.2f}" '
                     f'fill="{INK}" opacity="{1 if n == root_slug or int(CATALOG[n]["depth"])-d0<=1 else 0.55}" '
                     f'opacity="{1 if int(CATALOG[n]["depth"])-d0<=1 else .5}"/>')
    last_y = -99.0
    for n in CHILDREN.get(root_slug, []):
        y_ = ys(n)
        if y_ - last_y < 6.4:
            continue
        last_y = y_
        g = games(n)
        lbl = f'{short(n)[:26]}' + (f'  {g:,}' if g else '')
        parts.append(f'<text x="{xs(n)+3.6:.1f}" y="{y_+1.9:.1f}" font-size="5.4" fill="{INK}" '
                     f'font-family="Plex Mono, monospace">{lbl}</text>')
    return (f'<svg class="chart" viewBox="0 0 {width} {h:.0f}" xmlns="http://www.w3.org/2000/svg" '
            f'role="img"><title>Subtree of {short(root_slug)}</title>{"".join(parts)}</svg>')

TRANSPOSE_IN = [r for r in CATALOG.values()
                if not r["ocn1"].startswith(ROOT)
                and any(t.strip().startswith(ROOT) for t in r["transposes_to"].split("|") if t.strip())]

def games(s):
    r = POP.get(s); return int(r["masters_games"]) if r and r["masters_games"] else 0

def lich(s):
    r = POP.get(s); return int(r["lichess_games"]) if r and r["lichess_games"] else 0

def eco_of(s):
    e = [x for x in CATALOG[s]["eco_legacy"].split("|") if x.strip()]
    return "" if not e else (e[0] if len(e) == 1 else f"{e[0]}–{e[-1]}")

def short(s):
    return re.sub(r"^Ruy L[oó]pez[ ,]*", "", CATALOG[s]["canonical_name"]) or CATALOG[s]["canonical_name"]

def moves_text(s):
    u = CATALOG[s]["moves_uci"].split()
    return " ".join(f"{i//2+1}.{u[i]}{(' ' + u[i+1]) if i+1 < len(u) else ''}"
                    for i in range(0, len(u), 2))

CHILDREN = defaultdict(list)
for k, v in RYL.items():
    if k != ROOT:
        CHILDREN[v["parent_ocn1"]].append(k)
for kk in CHILDREN.values():
    kk.sort(key=lambda s: (-games(s), s))

for _slug in RYL:
    _b = _earliest(_slug)
    if _b:
        FIRST_GAME[_slug] = _b

WCH_BY_SLUG = Counter(r["ocn1"] for r in WCH)
CLAIM_BY_SLUG = defaultdict(list)
for c in CLAIMS:
    CLAIM_BY_SLUG[c["ocn1"]].append(c)
PROP_BY_SLUG = {p["ocn1"]: p for p in PROPOSED}

# ------------------------------------------------------------------ assets

def data_uri(p, m):
    return f"data:{m};base64,{base64.b64encode(p.read_bytes()).decode()}"

FONTS = "".join(f"@font-face {{ font-family:'{fam}'; font-weight:{w}; font-style:{st};"
                f" src:url('{data_uri(p, m)}') format('{f}'); }}\n"
                for fam, w, st, p, m, f in [
    ("OCN DIN", 400, "normal", OCN / "web/fonts/uDIN1451Mittelschrift.ttf", "font/ttf", "truetype"),
    ("Spectral", 400, "normal", OCN / "web/fonts/spectral-400.woff2", "font/woff2", "woff2"),
    ("Spectral", 400, "italic", OCN / "web/fonts/spectral-400i.woff2", "font/woff2", "woff2"),
    ("Spectral", 600, "normal", OCN / "web/fonts/spectral-600.woff2", "font/woff2", "woff2"),
    ("Plex Mono", 400, "normal", OCN / "web/fonts/plexmono-400.woff2", "font/woff2", "woff2"),
    ("Plex Mono", 600, "normal", OCN / "web/fonts/plexmono-600.woff2", "font/woff2", "woff2")])

SYMBOLS = []
for f in sorted((OCN / "web" / "pieces").glob("*.svg")):
    b = f.read_text()
    inner = b[b.index(">", b.index("<svg")) + 1: b.rindex("</svg>")]
    SYMBOLS.append(f'<symbol id="p{f.stem}" viewBox="0 0 45 45">{inner}</symbol>')
DEFS = ('<svg width="0" height="0" style="position:absolute" aria-hidden="true">'
        f'<defs>{"".join(SYMBOLS)}</defs></svg>')

INNER = re.compile(r"</title>\n(.*)</svg>", re.DOTALL)
li = lambda s: INNER.search(s).group(1).replace("\n", "")

# ------------------------------------------------------------------ board

LIGHT_SQ, DARK_SQ = "#efece2", "#c9c2ad"
_BOARD_BG = "".join(
    f'<rect x="{c*45}" y="{r*45}" width="45" height="45" '
    f'fill="{DARK_SQ if (r+c)%2 else LIGHT_SQ}"/>' for r in range(8) for c in range(8))

def board(fen, cls="board"):
    out = [_BOARD_BG]
    for r, row in enumerate(fen.split()[0].split("/")):
        fi = 0
        for ch in row:
            if ch.isdigit():
                fi += int(ch); continue
            k = ("w" if ch.isupper() else "b") + ch.upper()
            out.append(f'<use href="#p{k}" x="{fi*45}" y="{r*45}" width="45" height="45"/>')
            fi += 1
    return (f'<svg class="{cls}" viewBox="0 0 360 360" xmlns="http://www.w3.org/2000/svg" '
            f'role="img"><title>Position</title>{"".join(out)}'
            f'<rect width="360" height="360" fill="none" stroke="{INK}" stroke-width="2"/></svg>')

def board_of(slug, cls="board"):
    return board(row_fen(CATALOG[slug]["moves_uci"]), cls)

def figure(slug, caption, cls="board"):
    g = games(slug)
    return (f'<figure class="diagram">{board_of(slug, cls)}'
            f'<figcaption><span class="slug">{slug}</span> <span class="eco">{eco_of(slug)}</span>'
            f'<br><b>{CATALOG[slug]["canonical_name"]}</b><br><span class="cap">{caption}</span>'
            f'<br><span class="eco">{f"{g:,} master games" if g else "no master games"}</span>'
            f'</figcaption></figure>')

# ------------------------------------------------------------------ stats

ATTRIBUTED = sorted(k for k, v in RYL.items() if v["attributed_to"])
DEPTHS = Counter(int(v["depth"]) for v in RYL.values())
ECOS = sorted({e.strip() for v in RYL.values() for e in v["eco_legacy"].split("|") if e.strip()})
PLACES = [c for c in CLAIMS if c["relation"] == "named-after-place"]
RENAMED = [c for c in CLAIMS if c["relation"] == "renamed"]
WCH_DECADE = Counter(f"{int(r['year'])//10*10}s" for r in WCH if r["year"].isdigit())
WCH_EVENT = Counter(f"{r['event']}, {r['year']}" for r in WCH)
BY_GAMES = sorted((s for s in RYL if games(s)), key=lambda s: -games(s))
NO_ALIAS = [s for s, v in RYL.items() if not v["aliases"].strip()]
BRANCH25 = sorted((s for s in RYL if int(CATALOG[s]["depth"]) == 2), key=lambda s: -games(s))
DEEP = sorted((s for s in RYL if int(CATALOG[s]["depth"]) > 2), key=lambda s: (-games(s), s))

def bars(pairs, width_mm=112):
    top = max(v for _, v in pairs) or 1
    return '<div class="bars">' + "".join(
        f'<div class="bar"><span class="bl">{k}</span>'
        f'<span class="btrack"><span class="bb" style="width:{v/top*100:.1f}%"></span></span>'
        f'<span class="bn">{v}</span></div>' for k, v in pairs) + "</div>"

# ------------------------------------------------------------------ radial tree

# ------------------------------------------------------------------ chapter cover

# One rule for colour in this volume: gold marks a line that carries
# documentary evidence, and nothing else. It was previously doing eight jobs at
# once — family identity, board squares, bar length, treemap share, the draw
# segment of a result split, "still played", and rules — which is the same as
# doing none. Everything that is a quantity is ink at varying weight; the cover
# keeps the band and the letter, because that is identity and not data.
SQ_LIGHT, SQ_DARK = PAPER, "#dedbd2"   # a warm grey, not the family colour
GOLD_LIGHT, GOLD_DARK = SQ_LIGHT, SQ_DARK


def board_gold(fen, mark=()):
    """The cover plate: gold dark squares, and the squares that changed outlined."""
    out = []
    for r in range(8):
        for c in range(8):
            out.append(f'<rect x="{c*45}" y="{r*45}" width="45" height="45" '
                       f'fill="{GOLD_DARK if (r+c)%2 else GOLD_LIGHT}"/>')
    for r, row in enumerate(fen.split()[0].split("/")):
        fi = 0
        for ch in row:
            if ch.isdigit():
                fi += int(ch)
                continue
            k = ("w" if ch.isupper() else "b") + ch.upper()
            out.append(f'<use href="#p{k}" x="{fi*45}" y="{r*45}" width="45" height="45"/>')
            fi += 1
    for sq in mark:
        f_, r_ = "abcdefgh".index(sq[0]), 8 - int(sq[1])
        out.append(f'<rect x="{f_*45+3}" y="{r_*45+3}" width="39" height="39" fill="none" '
                   f'stroke="{INK}" stroke-width="2.4"/>')
    return (f'<svg class="plate" viewBox="0 0 360 360" xmlns="http://www.w3.org/2000/svg" '
            f'role="img"><title>Position</title>{"".join(out)}'
            f'<rect width="360" height="360" fill="none" stroke="{INK}" stroke-width="2"/></svg>')


def occupancy(fen):
    occ = {}
    for r, row in enumerate(fen.split()[0].split("/")):
        fi = 0
        for ch in row:
            if ch.isdigit():
                fi += int(ch)
                continue
            occ["abcdefgh"[fi] + str(8 - r)] = ch
            fi += 1
    return occ


def changed_squares(slug):
    """The squares of the last move only.

    This used to diff against the parent line, which is the same thing when the
    parent is one move away and nonsense when it is eleven: the Marshall sits
    eleven plies below its parent and the mark covered half the board. The last
    move is always the move that makes this line what it is, it is always two
    squares (four when castling, which the occupancy diff still gets right), and
    it is legible on every diagram in the book."""
    mv = CATALOG[slug]["moves_uci"].split()
    if not mv:
        return ()
    a = occupancy(row_fen(" ".join(mv[:-1])))
    b = occupancy(row_fen(" ".join(mv)))
    return tuple(sorted({k for k in set(a) | set(b) if a.get(k) != b.get(k)}))


def census(ch):
    """The chapter's figures. A zero is printed at full size, never omitted."""
    nodes = subtree(ch)
    att = sum(1 for x in nodes if CATALOG[x]["attributed_to"])
    wq = sum(WCH_BY_SLUG.get(x, 0) for x in nodes)
    big = lambda v: f'<div class="cv big">{v}</div>'
    med = lambda v: f'<div class="cv">{v}</div>'
    lab = lambda t: f'<div class="cl">{t}</div>'
    rule = '<div class="crule"></div>'
    colA = (lab("Named lines") + big(f"{len(nodes)}") + '<div class="crule gold"></div>'
            + lab("Master games") + med(f"{games(ch):,}") + rule
            + lab("Lichess games") + med(f"{lich(ch):,}") + rule)
    colB = (lab("World championship games") + med(f"{wq}") + rule
            + lab("Sourced names") + med(f"{att} of {len(nodes)}") + rule
            + lab("ECO") + med(eco_of(ch)) + rule)
    return f'<div class="census"><div>{colA}</div><div>{colB}</div></div>'


def signature(ch):
    """The same measurement for every chapter, chosen before the numbers were
    looked at: how many of its lines carry no alternative name at all.

    This used to be a cascade that printed whichever quantity was most extreme.
    Selecting the largest deviation from each of twenty-four groups guarantees
    that every group looks abnormal, which makes the figure an artefact of the
    selection rather than a fact about the chapter. One measurement stated for
    all of them is comparable, and this is the one the volume argues matters
    most: a line with no second name is a line nobody can find by the name
    their own source uses. The census above already counts sourced names, so
    this counts the other gap rather than repeating that one.
    """
    nodes = subtree(ch)
    n = len(nodes)
    bare = [x for x in nodes if not (CATALOG[x]["aliases"] or "").strip()]
    b = len(bare)
    if b == 0:
        return ("0", f"of the {n} named line{'s' if n != 1 else ''} here lacks an "
                     "alternative name. Every one of them can be found by more than one "
                     "string, which is rarer in this catalogue than it should be.")
    return (f"{b}", f"of the {n} named line{'s' if n != 1 else ''} in this chapter "
            f"carr{'y' if b != 1 else 'ies'} no alternative name at all — "
            f"{b / n * 100:.0f} per cent that a reader can only reach by knowing the name "
            "this catalogue happens to have chosen. The same count is on every chapter "
            "cover, so the chapters can be compared.")

def fingerprint(ch, width=470, height=190):
    """A chapter of this size has a shape, not a directory. Square size is master
    practice; a filled square carries a sourced attribution."""
    nodes = subtree(ch)
    leaves = [n for n in nodes if not CHILDREN.get(n)]
    li = {n: i for i, n in enumerate(leaves)}
    yy = {}

    def yc(n):
        if n in yy:
            return yy[n]
        k = CHILDREN.get(n, [])
        v = li[n] if not k else sum(yc(x) for x in k) / len(k)
        yy[n] = v
        return v

    yc(ch)
    d0 = int(CATALOG[ch]["depth"])
    maxd = max(int(CATALOG[n]["depth"]) for n in nodes)
    xs = lambda n: 6 + (yc(n) + 0.5) * (width - 12) / max(len(leaves), 1)
    ys = lambda n: 8 + (int(CATALOG[n]["depth"]) - d0) / max(maxd - d0, 1) * (height - 20)
    mx = max(games(n) for n in nodes) or 1
    parts = []
    for n in nodes:
        if n == ch:
            continue
        pnt = CATALOG[n]["parent_ocn1"]
        x1, y1, x2, y2 = xs(pnt), ys(pnt), xs(n), ys(n)
        parts.append(f'<path d="M{x1:.1f} {y1:.1f}V{(y1+y2)/2:.1f}H{x2:.1f}V{y2:.1f}" '
                     f'stroke="{INK}" stroke-width="0.35" fill="none" opacity=".5"/>')
    for n in nodes:
        sz = 1.3 + 3.2 * (math.log10(1 + games(n)) / math.log10(1 + mx))
        filled = bool(CATALOG[n]["attributed_to"])
        parts.append(f'<rect x="{xs(n)-sz/2:.2f}" y="{ys(n)-sz/2:.2f}" width="{sz:.2f}" '
                     f'height="{sz:.2f}" fill="{BAND if filled else PAPER}" '
                     f'stroke="{INK}" stroke-width="{0.5 if filled else 0.3}"/>')
    return (f'<svg class="chart" viewBox="0 0 {width} {height}" '
            f'xmlns="http://www.w3.org/2000/svg" role="img">'
            f'<title>Subtree fingerprint</title>{"".join(parts)}</svg>')


def labelled_tree(ch):
    nodes = [n for n in subtree(ch) if n != ch]
    mx = max((games(n) for n in nodes), default=1) or 1
    d0 = int(CATALOG[ch]["depth"])
    rows_ = []
    for n in nodes:
        ind = (int(CATALOG[n]["depth"]) - d0 - 1) * 3.4
        g = games(n)
        w = (math.log10(1 + g) / math.log10(1 + mx) * 100) if g else 0
        att = ('<span class="tick"></span>' if CATALOG[n]["attributed_to"]
               else '<span class="tickx"></span>')
        rows_.append(f'<div class="ltrow">{att}'
                     f'<span class="ltn" style="padding-left:{ind:.1f}mm">{short(n)}</span>'
                     f'<span class="ltb"><span style="width:{w:.1f}%"></span></span>'
                     f'<span class="ltg">{g:,}</span></div>')
    cls = "lt two-col" if len(rows_) > 13 else "lt"
    return f'<div class="{cls}">{"".join(rows_)}</div>'


def dossier(ch):
    """For the small chapters: the densest, most human page in the book."""
    nodes = subtree(ch)
    p = POP.get(ch, {})
    g = games(ch)
    w_ = int(p.get("masters_white") or 0)
    d_ = int(p.get("masters_draws") or 0)
    b_ = int(p.get("masters_black") or 0)
    if g:
        split = (f'<div class="split"><span style="width:{w_/g*100:.1f}%" class="sw"></span>'
                 f'<span style="width:{d_/g*100:.1f}%" class="sd"></span>'
                 f'<span style="width:{b_/g*100:.1f}%" class="sb"></span></div>'
                 f'<div class="eco">White {w_/g*100:.0f}%, drawn {d_/g*100:.0f}%, '
                 f'Black {b_/g*100:.0f}%</div>')
        hero, herol = f"{lich(ch)/g:,.0f} to 1", "amateur games per master game"
    else:
        split = ('<div class="split empty"></div>'
                 '<div class="eco">An empty box, drawn deliberately: no master game on record</div>')
        hero, herol = f"{lich(ch):,}", "amateur games, and no master game on record"
    src = CATALOG[ch]["attribution_source"]
    if CATALOG[ch]["attributed_to"]:
        name_block = (f'<div class="cl">The name</div>'
                      f'<div class="dname">{CATALOG[ch]["attributed_to"]}</div>'
                      f'<p class="dq">{src[:560]}</p>')
    else:
        also = (" Also called " + CATALOG[ch]["aliases"].replace("|", "; ") + "."
                if CATALOG[ch]["aliases"] else "")
        name_block = (f'<div class="cl">The name</div>'
                      f'<p class="dq"><i>No attribution on record.</i>{also}</p>')
    kidlist = ""
    if len(nodes) > 1:
        kidlist = ('<div class="cl" style="margin-top:3mm">Beneath it</div><div class="eco">'
                   + "<br>".join(f"{short(x)} &nbsp;{games(x):,}" for x in nodes[1:]) + "</div>")
    return (f'<div class="dossier"><div>{name_block}</div>'
            f'<div><div class="cl">Where it is played</div><div class="dhero">{hero}</div>'
            f'<div class="eco">{herol}</div>{split}{kidlist}</div></div>')


def chapter_cover(ci, ch, band_html):
    nodes = subtree(ch)
    n = len(nodes)
    if n >= 26:
        fig, fig_label = fingerprint(ch), ("Subtree. Square size is master practice; "
                                           "a filled square carries a sourced attribution.")
    elif n >= 9:
        fig, fig_label = labelled_tree(ch), ("Subtree. Bar length is master games, "
                                             "logarithmic; a gold tick marks a sourced name.")
    else:
        fig, fig_label = dossier(ch), "The complete record"
    sig_n, sig_t = signature(ch)
    fg = FIRST_GAME.get(ch)
    if fg:
        y, g = fg
        if g.get("lichess_id"):
            t = GAME_TAGS.get(g["lichess_id"], {})
            when, wh = pretty_date(t.get("date", "")) or str(y), where(g["lichess_id"])
        else:
            when = str(y)
            wh = ", ".join(x for x in (g.get("event", ""), g.get("place", "")) if x)
        first = ('<div class="cl">Earliest game in the sample</div>'
                 f'<div class="fgame">{g.get("white","")} v {g.get("black","")}<br>'
                 f'<span class="eco">{when}{", " + wh if wh else ""}</span></div>')
    else:
        first = ('<div class="cl">Earliest game in the sample</div>'
                 '<div class="fgame"><span class="eco">No dated game on record</span></div>')
    return f"""
{band_html}
<div class="chead"><span>Chapter {ci} of {len(CHAPTERS)}</span><span>{eco_of(ch)}</span></div>
<div class="csup">Ruy López</div>
<div class="ctitle">{short(ch)}</div>
<div class="cmoves mono">{moves_text(ch)}</div>
<div class="cmid">
 <div class="cleft">{census(ch)}{first}</div>
 <div class="cright">{board_gold(row_fen(CATALOG[ch]["moves_uci"]), changed_squares(ch))}
  <div class="pcap">{CATALOG[ch]["notes"].strip()}</div></div>
</div>
<div class="cfield"><div class="cflabel">{fig_label}</div>{fig}</div>
<div class="csig"><div class="csn">{sig_n}</div><div class="cst">{sig_t}</div></div>
"""


def _gcell_attr(c):
    """The attribution line of a gathered cell, or nothing.

    Written out rather than inlined because the inline form nested a
    single-quoted subscript inside a single-quoted f-string, which is PEP 701
    and therefore 3.12 and later. This repository builds on 3.10.
    """
    a = CATALOG[c]["attributed_to"]
    return f'<br><span class="attr">{a}</span>' if a else ""


# ------------------------------------------------------------------ pages

micro = li((BRAND / "micro-c.svg").read_text(encoding="utf-8"))
lock = li((BRAND / "lockup-horizontal.svg").read_text(encoding="utf-8"))
HW = f"{H_TOTAL_WIDTH:.3f}".rstrip("0").rstrip(".")
PAGES = []

SECTIONS = []

def add(title, body, folio, cls=""):
    SECTIONS.append((title, folio, len(PAGES)))
    head = "" if "chcover" in cls else f"<h2>{title}</h2>"
    PAGES.append(f'<section class="page {cls}">{head}{body}'
                 f'<div class="folio"><span>{folio}</span><span class="pn"></span></div></section>')

COVER = f"""<section class="page cover"><div class="band"></div><div class="inner">
 <div class="eyebrow din">OCN MONOGRAPHS</div>
 <div class="micro"><svg viewBox="0 0 72 72" xmlns="http://www.w3.org/2000/svg">{micro}</svg></div>
 <div class="letter din">C</div><h1>THE RUY LÓPEZ</h1>
 <div class="sub">SPANISH OPENING, C.RyL<br>{len(RYL)} NAMED LINES, ECO C60 TO C99<br>THE COMPLETE VOLUME</div>
 <div class="foot"><span class="din">CLUB D'ESCACS FIGUERES</span>
  <span class="lockup"><svg viewBox="0 0 {HW} 72" xmlns="http://www.w3.org/2000/svg">{lock}</svg></span></div>
</div></section>"""

stat_block = "".join(f'<div class="stat"><div class="n">{n}</div><div class="l">{l}</div></div>'
    for n, l in [(f"{len(RYL)}", "named lines"), (f"{len(ECOS)}", "ECO codes"),
                 (f"{max(DEPTHS)}", "levels deep"), (f"{len(WCH)}", "championship games"),
                 (f"{len(ATTRIBUTED)}", "sourced attributions"), (f"{len(PLACES)}", "named after places"),
                 (f"{len(RENAMED)}", "renamings"), (f"{len(PROPOSED)}", "open proposals")])

add("What this volume found", f"""
<p class="lead">If you read one page, this is the one. Everything below is a claim you
can check against the catalogue, and the identifiers are how you would argue with it.</p>

<h3>The scale, and what is actually proved</h3>
<table class="kv">
 <tr><td class="mono">{len(RYL)}</td><td>named Ruy López lines, of {len(CATALOG):,} openings in the catalogue</td></tr>
 <tr><td class="mono">{len(ATTRIBUTED)}</td><td>carry an attribution with a source and a stated role</td></tr>
 <tr><td class="mono">{len(PROPOSED)}</td><td>more have a proposed eponym <b>deliberately held back</b>, because the evidence establishes a name and not what the person did</td></tr>
 <tr><td class="mono">{len(NO_ALIAS)}</td><td>carry no alternative name at all, which is this catalogue's largest and most consequential gap</td></tr>
 <tr><td class="mono">{len(WCH)}</td><td>world-championship games, mapped to the exact line rather than to the opening</td></tr>
</table>

<h3>What this edition corrects</h3>
<p class="small"><b>An attribution of our own, retracted.</b> The line we call the Wormald
Attack carried an attribution to Thomas Herbert Worrall, sourced to an Oxford Companion
entry that describes a different line. It had been matched on the three letters the two
identifiers share. Retracted rather than moved, and the reasoning is at the back.</p>
<p class="small"><b>Seven games that were not world-championship games.</b> Two Spanish
amateurs had been filed into Steinitz–Zukertort 1886, three games into
Alekhine–Capablanca 1927, and a different Koneru into Hou Yifan's 2011 defence — every
one of them pulled in because a surname matched.</p>
<p class="small"><b>Thirteen misspelled participants over 334 rows</b>, including a
women's world championship challenger recorded under a man's forename for
{2025 - 1965} years of catalogue history.</p>

<h3>What we cannot do without you</h3>
<p class="small">A 2026 course teaches one of these lines as the <b>Modern Archangel</b>
and a recent book teaches another as the <b>Neo-Møller</b>. Neither string appears
anywhere in this catalogue. We are not asking whether our names are right. We are asking
what you call these lines, and since when — because that is the one thing a catalogue
cannot generate for itself, and it is the difference between being correct and being
findable.</p>
""", "Findings")

add("Everything we hold, through one opening", f"""
<p class="lead">This is the Ruy López as Open Chess Naming records it, in full: every
named line with its own diagram and figures, the shape of the naming tree, what is
actually played, the world-championship record, the people, the places, the
renamings, the pending proposals, and the questions we cannot answer.</p>
<p>OCN is a catalogue of {len(CATALOG):,} named chess openings maintained by Club
d'Escacs Figueres, a Catalan chess club approaching its hundredth year. Its subject is
not how to play the openings but what they are called and why: each name traced, where
the evidence allows, to the people and published sources behind it, each claim graded,
and every gap left visible rather than filled with a plausible guess. CC BY 4.0, no
paywall, no advertising.</p>
<p>The Ruy López is the right specimen. It is the oldest opening still in the highest
practice, it has been played continuously through the entire recorded history of the
world championship, and it carries more named sub-variations than any other opening in
the catalogue. Whatever the data can do, it can do here.</p>
<div class="stats">{stat_block}</div>
<p class="small">Every line has a stable identifier, a move list, a legacy ECO range, a
Lichess cross-reference and a position key. {len(POP)} of {len(RYL)} carry popularity
figures. The naming and the hierarchy are OCN's own work; the corpus of lines worth
naming came from lichess-org/chess-openings, released CC0, and every line here but the
root cross-references it.</p>
<h3>How to read the catalogue section</h3>
<p class="small">The catalogue section that follows holds every one of the {len(RYL)}
lines with its position, its identifier, its ECO range and its recorded practice. The
{len(BRANCH25)} principal branches are given at full size first; the {len(DEEP)}
deeper lines follow in compact form, in tree order, so that a line always appears
after the line it refines.</p>
""", "Overview")

add("The name", f"""
<p>The opening is named after <b>Ruy López de Segura</b> (c. 1530 – c. 1580), a Spanish
priest from Zafra in Extremadura who served at the court of Philip II and who
recommended 3.Bb5 in <i>Libro de la invención liberal y arte del juego del axedrez</i>
(Alcalá, 1561). Wikidata records the opening (Q1290671) as named after him (Q297457).</p>
<p>The name is unusual in a way the catalogue records explicitly: it carries his
<i>given names</i>, not his surname. "Ruy López" is Ruy the son of López; the family
name is de Segura. Every other person-named line here is called after a surname. A
catalogue that matched names to people by surname alone would fail on its own root,
which is why OCN treats a Wikidata identity, and not a name string, as who a person
is.</p>
<div class="two">
 <div>{figure(ROOT, "The position after 3.Bb5. Everything in this volume descends from it.", "board big")}</div>
 <div>
  <h3>Also called</h3>
  <p class="small">The Spanish Opening across most of Europe: <i>Spanische Partie</i>,
  <i>Partie espagnole</i>, <i>apertura española</i>. English-language sources kept the
  man's name, others kept his nationality. The catalogue records both and privileges
  neither.</p>
  <h3>Moves</h3><p class="mono">{moves_text(ROOT)}</p>
  <h3>Practice</h3>
  <p class="small mono">{games(ROOT):,} master games<br>{lich(ROOT):,} Lichess games<br>
  strongest recorded: {POP[ROOT]['top_player']} ({POP[ROOT]['top_player_elo']})</p>
 </div>
</div>
<h3>"A bad opening", 1846</h3>
<p>When Staunton played 3.Bb5 against Horwitz he felt obliged to explain himself, and
Saint-Amant was unimpressed:</p>
<blockquote>Ceci est un mauvais début, généralement condamné … le début qu'il a adopté
n'est rien moins que du nouveau: c'est du vieux, et ce n'est pas du meilleur, voilà
tout.<span class="src">Le Palamède, March 1846, pp. 125-126, located by Edward Winter, C.N. 9822</span></blockquote>
<p class="small">The catalogue records the assessment and its date, not a verdict on it.
"The Ruy López is sound" is not a naming fact; "Le Palamède called it a bad opening in
March 1846" is one, and it is checkable.</p>
""", "The name")

add("The shape of it", f"""
<p>Names in OCN form a tree, not a list: each name is a child of the name it refines,
so a line inherits everything its parent asserts and adds one distinction. The Ruy
López runs {max(DEPTHS)} levels deep and holds {len(RYL)} names.</p>
{bars([(f"level {d}", DEPTHS[d]) for d in sorted(DEPTHS)])}
<p class="small">Depth is not decoration. It is what lets the catalogue say that the
Zaitsev is a kind of Closed Spanish which is a kind of Morphy Defence, and why a query
for the Morphy Defence returns {games('C.RyL.Mor'):,} master games where its parent
returns {games(ROOT):,}.</p>
<h3>Legacy ECO coverage</h3>
<p class="small">The opening spans {len(ECOS)} ECO codes, the whole of C60 to C99. ECO
was designed in 1966 for a five-volume printed encyclopaedia and has no room below its
three-character code, which is precisely the gap this catalogue fills. The mapping is
many-to-many and OCN records it rather than pretending otherwise.</p>
<p class="mono small">{" ".join(ECOS)}</p>
<h3>What a single row holds</h3>
<table class="kv">
 <tr><td class="mono">ocn1</td><td>C.RyL.Zai.MLn</td></tr>
 <tr><td class="mono">canonical_name</td><td>{CATALOG['C.RyL.Zai.MLn']['canonical_name']}</td></tr>
 <tr><td class="mono">eco_legacy</td><td>{eco_of('C.RyL.Zai.MLn')}</td></tr>
 <tr><td class="mono">parent_ocn1</td><td>{CATALOG['C.RyL.Zai.MLn']['parent_ocn1']}</td></tr>
 <tr><td class="mono">moves_uci</td><td class="mono">{CATALOG['C.RyL.Zai.MLn']['moves_uci']}</td></tr>
 <tr><td class="mono">masters_games</td><td>{games('C.RyL.Zai.MLn'):,}</td></tr>
 <tr><td class="mono">lichess_xref</td><td>{XREF['C.RyL.Zai.MLn']['lichess_name'][:52]}</td></tr>
</table>
""", "Structure")

def _squarify(areas, x, y, w, h):
    """Squarified treemap layout. `areas` must be sorted descending and already
    scaled so they sum to w*h. Returns one rect per area, in the same order."""
    def worst(row, side):
        s = sum(row)
        if s <= 0 or side <= 0:
            return float("inf")
        return max(side * side * max(row) / (s * s), (s * s) / (side * side * min(row)))

    rects, rest = [], list(areas)
    while rest:
        side = min(w, h)
        row = [rest.pop(0)]
        while rest and worst(row + [rest[0]], side) <= worst(row, side):
            row.append(rest.pop(0))
        s = sum(row)
        if w >= h:
            rw = s / h if h else 0
            oy = y
            for a in row:
                rh = (a / s * h) if s else 0
                rects.append((x, oy, rw, rh))
                oy += rh
            x, w = x + rw, w - rw
        else:
            rh = s / w if w else 0
            ox = x
            for a in row:
                rw2 = (a / s * w) if s else 0
                rects.append((ox, y, rw2, rh))
                ox += rw2
            y, h = y + rh, h - rh
    return rects


def treemap(width=470, height=430):
    """The whole opening by weight of practice, nested two levels.

    The radial tree this replaces drew every name the same size, which put a
    line played twice beside one played half a million times and made the
    figure a picture of the catalogue's shape rather than of the opening's.
    Area here is master games, so what a reader sees is where the game
    actually is."""
    tops = [c for c in CHILDREN.get(ROOT, []) if games(c) > 0]
    tops.sort(key=lambda c: -games(c))
    vals = [float(games(c)) for c in tops]
    total = sum(vals) or 1
    cells = _squarify([v / total * width * height for v in vals], 0, 0, width, height)

    p = [f'<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" '
         f'style="width:100%;height:auto">']
    for c, (x, y, w, h) in zip(tops, cells):
        kids = [k for k in CHILDREN.get(c, []) if games(k) > 0]
        kids.sort(key=lambda k: -games(k))
        own = games(c) - sum(games(k) for k in kids)
        p.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" '
                 f'fill="#f6f6f3" stroke="#15171a" stroke-width="0.9"/>')
        if kids and w > 14 and h > 14:
            kv = [float(games(k)) for k in kids] + ([float(own)] if own > 0 else [])
            kt = sum(kv) or 1
            inner = _squarify([v / kt * (w - 2) * (h - 2) for v in kv],
                              x + 1, y + 1, w - 2, h - 2)
            for i, (kx, ky, kw, kh) in enumerate(inner):
                share = kv[i] / kt
                p.append(f'<rect x="{kx:.2f}" y="{ky:.2f}" width="{max(kw,0):.2f}" '
                         f'height="{max(kh,0):.2f}" fill="{INK}" '
                         f'opacity="{0.10 + 0.40 * share:.2f}" '
                         f'stroke="#f6f6f3" stroke-width="0.5"/>')
        if w > 46 and h > 15:
            nm = short(c).split(",")[-1].strip() if "," in short(c) else short(c)
            p.append(f'<text x="{x + 3.5:.1f}" y="{y + 10.5:.1f}" font-size="7.4" '
                     f'fill="#15171a" font-family="u_DIN 1451">{nm[:int(w / 5.4)]}</text>')
        if w > 46 and h > 27:
            p.append(f'<text x="{x + 3.5:.1f}" y="{y + 19.5:.1f}" font-size="6.2" '
                     f'fill="#15171a" opacity="0.6" font-family="IBM Plex Mono">'
                     f'{games(c):,}</text>')
    p.append("</svg>")
    return "".join(p)


def _hum(d):
    v = 10 ** d
    return (f"{v:,}" if v < 1000
            else f"{v // 1000}k" if v < 1_000_000 else f"{v // 1_000_000}M")


def scatter(width=470, height=352):
    """Club play against master play, both on a log scale.

    Every other figure in this volume measures one population. This one puts
    two beside each other, and the distance between them is the only thing in
    the book that says which of these names belong to the game as it is
    actually played."""
    pts = [(s, lich(s), games(s)) for s in RYL if lich(s) > 0 and games(s) > 0]
    lx = [math.log10(a) for _, a, _ in pts]
    ly = [math.log10(b) for _, _, b in pts]
    x0, x1, y0, y1 = 34, width - 8, height - 30, 16
    lo_x, hi_x, lo_y, hi_y = 0, math.ceil(max(lx)), 0, math.ceil(max(ly))

    def X(v):
        return x0 + (v - lo_x) / (hi_x - lo_x) * (x1 - x0)

    def Y(v):
        return y0 + (v - lo_y) / (hi_y - lo_y) * (y1 - y0)

    p = [f'<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" '
         f'style="width:100%;height:auto">']
    for d in range(lo_x, hi_x + 1):
        p.append(f'<line x1="{X(d):.1f}" y1="{y0}" x2="{X(d):.1f}" y2="{y1}" '
                 f'stroke="#15171a" stroke-width="0.3" opacity="0.1"/>')
        p.append(f'<text x="{X(d):.1f}" y="{y0 + 10}" font-size="6" fill="#15171a" '
                 f'opacity="0.55" text-anchor="middle" font-family="IBM Plex Mono">'
                 f'{_hum(d)}</text>')
    for d in range(lo_y, hi_y + 1):
        p.append(f'<line x1="{x0}" y1="{Y(d):.1f}" x2="{x1}" y2="{Y(d):.1f}" '
                 f'stroke="#15171a" stroke-width="0.3" opacity="0.1"/>')
        p.append(f'<text x="{x0 - 4}" y="{Y(d) + 2:.1f}" font-size="6" fill="#15171a" '
                 f'opacity="0.55" text-anchor="end" font-family="IBM Plex Mono">'
                 f'{_hum(d)}</text>')
    # the reference is not parity, which nobody expects, but the opening's own
    # ratio: a line on this diagonal is played in club chess exactly as often,
    # relative to master practice, as the Ruy López is as a whole.
    lb = math.log10(BASE)
    xa, xb = lb, hi_x
    p.append(f'<line x1="{X(xa):.1f}" y1="{Y(0):.1f}" x2="{X(xb):.1f}" '
             f'y2="{Y(xb - lb):.1f}" stroke="#15171a" stroke-width="0.7" '
             f'stroke-dasharray="3 2" opacity="0.5"/>')
    p.append(f'<text x="{X(hi_x) - 4:.1f}" y="{Y(hi_x - lb) - 4:.1f}" font-size="6" '
             f'fill="#15171a" opacity="0.65" text-anchor="end" font-family="Spectral">'
             f'as club-heavy as the opening as a whole</text>')
    for (s, a, b) in pts:
        p.append(f'<circle cx="{X(math.log10(a)):.1f}" cy="{Y(math.log10(b)):.1f}" '
                 f'r="1.9" fill="#654F1E" opacity="0.4"/>')
    # the extremes of the ratio, plus the three most played, named
    solid = [t for t in pts if t[2] >= MIN_SAMPLE]
    by_ratio = sorted(solid, key=lambda t: -(t[1] / t[2]))
    marked = by_ratio[:3] + by_ratio[-3:] + sorted(pts, key=lambda t: -t[2])[:2]
    seen, k = set(), 0
    for s, a, b in marked:
        if s in seen:
            continue
        seen.add(s)
        cx, cy = X(math.log10(a)), Y(math.log10(b))
        p.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="3" fill="none" '
                 f'stroke="#15171a" stroke-width="0.9"/>')
        nm = short(s).split(",")[-1].strip()
        anc, tx = "middle", cx
        if cx < x0 + 46:
            anc, tx = "start", cx - 2
        elif cx > x1 - 46:
            anc, tx = "end", cx + 2
        ty = cy - 6.5 if k % 2 == 0 else cy + 10.5
        k += 1
        p.append(f'<text x="{tx:.1f}" y="{ty:.1f}" font-size="6.4" '
                 f'fill="#15171a" font-family="Spectral" text-anchor="{anc}">'
                 f'{nm[:30]}</text>')
    p.append(f'<text x="{(x0 + x1) / 2:.0f}" y="{height - 4}" font-size="6.6" '
             f'fill="#15171a" opacity="0.7" text-anchor="middle" font-family="Spectral">'
             f'Lichess games</text>')
    p.append(f'<text x="10" y="{(y0 + y1) / 2:.0f}" font-size="6.6" fill="#15171a" '
             f'opacity="0.7" text-anchor="middle" font-family="Spectral" '
             f'transform="rotate(-90 10 {(y0 + y1) / 2:.0f})">master games</text>')
    p.append("</svg>")
    return "".join(p)


MIN_SAMPLE = 25   # below this a ratio is one game's worth of accident
# Lichess holds far more games than the master sample, so a raw club-to-master
# ratio measures the two corpora before it measures anything about a line. The
# opening's own ratio is the denominator that removes it.
BASE = lich(ROOT) / games(ROOT)
_ratio = sorted(((lich(s) / games(s), s) for s in RYL if games(s) and lich(s)),
                reverse=True)
_solid = [t for t in _ratio if games(t[1]) >= MIN_SAMPLE]
_sens = ", ".join(
    f"{short(max((t for t in _ratio if games(t[1]) >= k), key=lambda t: t[0])[1])} at {k}"
    for k in (10, 25, 50, 100))
_top_ratio, _low_ratio = _solid[0], _solid[-1]
_raw_top = _ratio[0]

add("Club play against master play", f"""
<p class="lead">The catalogue records both populations for {len(_ratio)} of these lines:
what strong players do, and what everybody else does. Nobody has put them on the same
axes before, and they do not agree.</p>
{scatter()}
<p class="small">One dot per line, both axes logarithmic, each decade a tenfold increase.
The dashed diagonal is the opening's own club-to-master ratio, so a line sitting
on it is played below master level exactly as often as the Ruy López is as a whole.
Above the line is over-represented in club chess, below it under-represented, and the
spread runs over four orders of magnitude within one opening.</p>
<h3>What the spread says</h3>

<p>Among the {len(_solid)} lines with at least {MIN_SAMPLE} master games, the extreme is
<b>{short(_top_ratio[1])}</b>: {lich(_top_ratio[1]):,} club games against
{games(_top_ratio[1]):,} master games, which is <b>{_top_ratio[0] / BASE:,.0f} times</b>
as club-heavy as the opening it belongs to. At the other end,
<b>{short(_low_ratio[1])}</b> is {BASE / _low_ratio[0]:,.0f} times <i>less</i> club-heavy
than the opening as a whole: a name that lives almost entirely inside strong practice.</p>
<p class="small">The threshold is deliberate: a ratio needs a denominator before it means
anything, and without a minimum the top of this list is arithmetic on a single master
game. The {len(_ratio) - len(_solid)} lines below it are drawn in the figure and not
quoted from. How much the choice carries: at minimums of 10, 25, 50 and 100 master games
the most club-heavy line is {_sens}. It moves once, between ten and twenty-five, and then
holds — which is the honest way to say that the threshold matters at the bottom and the
finding is stable above it.</p>
<p>The catalogue treats both as one kind of thing, and this figure argues it should not: a
name above the diagonal is one club players need whatever the grandmasters think, and one
below it only makes sense to somebody reading theory. Which a naming catalogue owes its
precision to is a real editorial question, and OCN has never answered it.</p>
""", "Two populations")

SPANS = sorted(((int(POP[s]["top_game_year_earliest"]), int(POP[s]["top_game_year_latest"]), s)
                 for s in RYL
                 if POP.get(s, {}).get("top_game_year_earliest", "").isdigit()
                 and POP[s].get("top_game_year_latest", "").isdigit()),
                key=lambda t: (t[0], t[1]))
SPAN_LO = min(a for a, _, _ in SPANS)
SPAN_HI = max(b for _, b, _ in SPANS)
_lens = sorted(b - a for a, b, _ in SPANS)
SPAN_MED = _lens[len(_lens) // 2]
SPAN_CURRENT = [t for t in SPANS if t[1] >= 2023]
SPAN_ONEYEAR = [t for t in SPANS if t[0] == t[1]]
SPAN_LONGEST = max(SPANS, key=lambda t: t[1] - t[0])

# Every date here is one the catalogue already cites somewhere else in this
# volume. Nothing on this axis is supplied for the sake of the drawing.
ANCHORS = [
    (1490, 0, "c. 1490 — the Göttingen manuscript already contains the opening"),
    (1561, 1, "1561 — Ruy López de Segura, Libro de la invención liberal, Alcalá"),
    (1846, 2, "1846 — Le Palamède calls it a bad opening"),
    (1886, 3, "1886 — first world-championship game in the chronicle"),
    (1963, 4, "1963 — first book found naming one of these lines"),
]


def span_chart(width=470, height=486):
    """Two registers: the documented sweep, and the sliver the sample can see.

    Drawing the spans alone on their own axis would say the opening began in
    1971. It is 550 years old in this catalogue's own citations, and the point
    of the figure is the distance between those two statements."""
    a_lo, a_hi = 1475, 2025
    ax0, ax1, ay = 8, width - 8, 104
    bx0, bx1 = 26, width - 6
    b_top, b_bot = 172, height - 22

    def A(y):
        return ax0 + (y - a_lo) / (a_hi - a_lo) * (ax1 - ax0)

    def B(y):
        return bx0 + (y - SPAN_LO) / (SPAN_HI - SPAN_LO) * (bx1 - bx0)

    p = [f'<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" '
         f'style="width:100%;height:auto">']

    # ---- register A: the whole documented sweep
    p.append(f'<line x1="{ax0}" y1="{ay}" x2="{ax1}" y2="{ay}" stroke="#15171a" '
             f'stroke-width="0.8"/>')
    for c in range(1500, 2001, 100):
        p.append(f'<line x1="{A(c):.1f}" y1="{ay}" x2="{A(c):.1f}" y2="{ay + 4}" '
                 f'stroke="#15171a" stroke-width="0.5" opacity="0.6"/>')
        p.append(f'<text x="{A(c):.1f}" y="{ay + 13}" font-size="6.2" fill="#15171a" '
                 f'opacity="0.6" text-anchor="middle" font-family="IBM Plex Mono">{c}'
                 f'</text>')
    for yr, lvl, label in ANCHORS:
        x, ly = A(yr), 20 + lvl * 16
        p.append(f'<line x1="{x:.1f}" y1="{ay}" x2="{x:.1f}" y2="{ly + 3:.0f}" '
                 f'stroke="#15171a" stroke-width="0.45" opacity="0.45"/>')
        p.append(f'<circle cx="{x:.1f}" cy="{ay}" r="2.2" fill="#15171a"/>')
        anc = "end" if x > width * 0.62 else "start"
        p.append(f'<text x="{x + (-4 if anc == "end" else 4):.1f}" y="{ly:.0f}" '
                 f'font-size="6.6" fill="#15171a" text-anchor="{anc}" '
                 f'font-family="Spectral">{label}</text>')
    # the sample's window, marked on the long axis and opened out below
    wx0, wx1 = A(SPAN_LO), A(SPAN_HI)
    p.append(f'<rect x="{wx0:.1f}" y="{ay - 7:.0f}" width="{max(wx1 - wx0, 1.4):.1f}" '
             f'height="14" fill="#F0C053" stroke="#654F1E" stroke-width="0.6"/>')
    p.append(f'<path d="M{wx0:.1f} {ay + 7:.0f} L{bx0} {b_top - 6} '
             f'M{wx1:.1f} {ay + 7:.0f} L{bx1} {b_top - 6}" fill="none" '
             f'stroke="#654F1E" stroke-width="0.5" stroke-dasharray="2.5 2" opacity="0.75"/>')
    p.append(f'<text x="{ax0}" y="{b_top - 13:.0f}" font-size="6.6" fill="#654F1E" '
             f'opacity="0.9" font-family="Spectral">{SPAN_LO} to {SPAN_HI}, opened out'
             f'</text>')

    # ---- register B: one hairline per line, sorted by first appearance
    body = b_bot - b_top
    for d in range(1970, SPAN_HI + 1, 10):
        if d < SPAN_LO:
            continue
        p.append(f'<line x1="{B(d):.1f}" y1="{b_top:.0f}" x2="{B(d):.1f}" '
                 f'y2="{b_bot:.0f}" stroke="#15171a" stroke-width="0.3" opacity="0.12"/>')
        p.append(f'<text x="{B(d):.1f}" y="{b_bot + 11:.0f}" font-size="6.4" '
                 f'fill="#15171a" opacity="0.55" text-anchor="middle" '
                 f'font-family="IBM Plex Mono">{d}</text>')
    rh = body / len(SPANS)
    for i, (a, b, s) in enumerate(SPANS):
        y = b_top + i * rh + rh / 2
        live = b >= 2023
        col = INK
        if a == b:
            p.append(f'<circle cx="{B(a):.2f}" cy="{y:.2f}" r="0.9" fill="{col}" '
                     f'opacity="0.85"/>')
        else:
            p.append(f'<line x1="{B(a):.2f}" y1="{y:.2f}" x2="{B(b):.2f}" y2="{y:.2f}" '
                     f'stroke="{col}" stroke-width="{1.15 if live else 0.7}" '
                     f'opacity="{0.95 if live else 0.4}"/>')
    p.append(f'<text x="{bx0}" y="{height - 3:.0f}" font-size="6.4" fill="#654F1E" '
             f'font-family="Spectral">heavier line: still played in the sample in 2023 or later'
             f'</text>')
    p.append("</svg>")
    return "".join(p)


add("How long a name stays in play", f"""
<p class="lead">The upper axis is the opening's documented life as this catalogue can cite
it, from the incunabula to now. The gold band on it is everything the game sample can
see, opened out below as one hairline for each of the {len(SPANS)} lines that can be dated
at both ends.</p>
{span_chart()}
<p class="small">In the lower register each line runs from its first strong game to its
last, ordered by first appearance, so the left edge of the block is itself the curve of
how fast the sample met these names. Gold hairlines are lines still played in 2023 or
later; a line seen in one year only is a dot. Every date on the upper axis is cited
elsewhere in this volume.</p>
""", "Spans")

add("Five centuries, and the years we can measure", f"""
<p class="lead">The figure opposite is two statements about the same opening, and the gap
between them is what this catalogue spends most of its time apologising for.</p>
<p>Drawn on its own the lower register would say this opening began in {SPAN_LO}. It did
not. The position is in the Göttingen manuscript by about 1490; the opening takes its
name from a book printed at Alcalá in 1561, seventy years later; a French magazine was
dismissing it by 1846; and the world-championship record runs from 1886. What the game sample reaches is the marked sliver: a
{SPAN_HI - SPAN_LO}-year window at the end of a five-century record, which is
{round(100 * (SPAN_HI - SPAN_LO) / (SPAN_HI - 1490))} per cent of the documented life of
the thing it is measuring.</p>
<p>Inside that window the shape is real. The median line runs <b>{SPAN_MED} years</b> from
first appearance to last, {len(SPAN_ONEYEAR)} appear in a single year of the sample and not again in it, and
the longest-lived is <b>{short(SPAN_LONGEST[2])}</b> at
{SPAN_LONGEST[1] - SPAN_LONGEST[0]} years ({SPAN_LONGEST[0]} to {SPAN_LONGEST[1]}).
{len(SPAN_CURRENT)} of the {len(SPANS)} are still being played, which is to say that
roughly {100 - round(100 * len(SPAN_CURRENT) / len(SPANS))} per cent of these names
describe positions strong players have stopped reaching.</p>
<p class="small">Two cautions about the left of the axis. The 1490 mark is the position
and not the name: the Göttingen manuscript contains the opening about seventy years
before anyone called it after Ruy López de Segura, so the 1561 mark is the only date on
this figure that is about the <i>name</i>. And this catalogue holds a <i>Lucena
Variation</i> and cites Lucena's book of about 1497 for three other openings, but not for
this one. That book analyses eleven openings and the sources naming which eleven are not
good enough to cite here, so it is left off the axis. If you know the page, that is one
of the questions at the back.</p>
<h3>The two ends of the window</h3>
<div class="two">
 <div>
  <p class="small"><b>Longest in play.</b> The lines the sample has watched for longest,
  first game to last.</p>
  <table class="kv tight">{"".join(
    f'<tr><td>{short(sl)}</td><td class="mono">{a}&ndash;{b}</td>'
    f'<td class="mono">{b - a}y</td></tr>'
    for a, b, sl in sorted(SPANS, key=lambda t: -(t[1] - t[0]))[:11])}</table>
 </div>
 <div>
  <p class="small"><b>Newest to the record.</b> The names the sample met last, which is
  not the same as the newest ideas.</p>
  <table class="kv tight">{"".join(
    f'<tr><td>{short(sl)}</td><td class="mono">{a}&ndash;{b}</td>'
    f'<td class="mono">{games(sl):,}</td></tr>'
    for a, b, sl in sorted(SPANS, key=lambda t: (-t[0], t[1]))[:11])}</table>
 </div>
</div>
<p class="small">The right-hand column of the second table is master games. A name the
sample met only recently and on a handful of games is a name whose entry in this volume
rests on very little, and there are more of those than the tables elsewhere make
obvious.</p>
""", "Spans")

add("The naming tree, entire", f"""
<p>All {len(RYL)} names as one figure, and the only one in this volume drawn to the
weight of the game rather than to the shape of the catalogue. Every branch of the tree is
a rectangle whose <b>area is its master practice</b>; inside each, its own branches divide
it again. A name that has been played half a million times and a name played twice are
the same entry in every table in this book, and here they are not.</p>
<div class="figwrap">{treemap()}</div>
<p class="small">Outer cells are the branches from 3.Bb5, labelled where they are large
enough to carry it; the inner divisions are their own children, shaded by share, with the
practice that stops at the parent shown as a cell of its own. Two thirds of everything is
inside one rectangle. The {len([s for s in RYL if int(CATALOG[s]['depth'])==2 and not games(s)])} depth-two names with no master
games at all have no area and so do not appear here, which is the honest consequence of
drawing practice instead of names, and the reason the catalogue is not this figure.</p>
""", "The tree")



top_rows = "".join(
    f'<tr><td class="mono">{s}</td><td>{short(s)}</td><td class="num">{games(s):,}</td>'
    f'<td class="num">{lich(s):,}</td><td class="mono">{short_player(POP[s]["top_player"])}</td></tr>'
    for s in BY_GAMES[1:14])
wch_rows = "".join(f'<tr><td class="mono">{s}</td><td>{short(s)}</td><td class="num">{n}</td></tr>'
                   for s, n in WCH_BY_SLUG.most_common(8))
zero = len(RYL) - len(BY_GAMES)
add("Which lines are most played", f"""
<p>Popularity is recorded, not assumed. Each line carries counts from a master database
and from Lichess, the strongest player recorded on it, and the year range of those
games.</p>
<h3>Most played, master practice</h3>
<table><tr><th>Line</th><th>Name</th><th class="num">Master games</th>
 <th class="num">Lichess</th><th>Strongest recorded</th></tr>{top_rows}</table>
<p class="small">The ordering is the hierarchy showing through: a parent always holds at
least as many games as any child, so the head of a long arm outranks the specific line
people actually choose. Read it as a map of where practice concentrates rather than as a
popularity chart of variations.</p>
""", "Rankings")

add("Which lines are most contested", f"""
<div>
 <div><h3>Most contested at world-championship level</h3>
  <table class="tight"><tr><th>Line</th><th>Name</th><th class="num">Games</th></tr>{wch_rows}</table>
  <h3>The long tail</h3>
  <p class="small">{zero} of the {len(RYL)} lines have no master games recorded at all.
  They exist because someone named them, which is exactly the kind of thing a naming
  catalogue must keep and a practice database has no reason to. The catalogue's job is
  to hold the name that was given, not only the name that was used.</p>
  <h3>Deepest naming</h3>
  <p class="small">{DEPTHS[6]} lines sit six levels down, each step a distinction
  someone thought worth a name.</p>
 </div>
</div>
""", "Rankings")

add("The world championship record", f"""
<p>The catalogue maps every world-championship game to the line it opened. {len(WCH)} of
them are Ruy Lópezes, across {len(WCH_EVENT)} matches and
{max(int(r['year']) for r in WCH if r['year'].isdigit()) - min(int(r['year']) for r in WCH if r['year'].isdigit())}
years, from {min(int(r['year']) for r in WCH if r['year'].isdigit())} to
{max(int(r['year']) for r in WCH if r['year'].isdigit())}. No other opening in the
catalogue has an unbroken presence like it.</p>
{bars([(d, WCH_DECADE[d]) for d in sorted(WCH_DECADE)])}
<p class="small">The gap in the 1940s is the war. The thinness of the 2000s is the
Berlin: when Kramnik took the Berlin endgame to London in 2000, the answer at the top
was to stop playing 1.e4 rather than to argue with it.</p>
<div class="two">
 <div><h3>Matches with the most</h3>
  <table class="tight"><tr><th>Match</th><th class="num">Games</th></tr>
  {"".join(f'<tr><td>{e}</td><td class="num">{n}</td></tr>' for e, n in WCH_EVENT.most_common(11))}</table></div>
 <div><h3>The first on record</h3>
  <p class="small">Steinitz v Zukertort, World Championship Match, 1886, opening
  <b>{CATALOG[[r for r in WCH if r['year']=='1886'][0]['ocn1']]['canonical_name']}</b>.
  <b>This is where the world championship starts, and nowhere near where the opening
  starts.</b> The position is in the incunabula: it is already in the Göttingen
  manuscript of about 1490, and it takes its name from Ruy López de Segura's <i>Libro de
  la invención liberal y arte del juego del axedrez</i>, printed at Alcalá in 1561, which
  analyses it — seventy years after the moves were first written down. Every date in this section is the date of a title match and
  should be read as one.
  Every one of these {len(WCH)} games is a graded claim in the chronicle, with the
  event, the players, the result and the citation that supports it, attached to the
  exact line rather than to the opening in general.</p>
  <h3>What that buys</h3>
  <p class="small">A question like "which Ruy López line has been contested most often
  for the world title" is a query here, not an afternoon of reading. The answer is
  {WCH_BY_SLUG.most_common(1)[0][0]}, with {WCH_BY_SLUG.most_common(1)[0][1]} games.</p>
 </div>
</div>
""", "Championship")

att_rows = "".join(f'<tr><td class="mono">{s}</td><td>{short(s)}</td>'
                   f'<td>{CATALOG[s]["attributed_to"]}</td></tr>' for s in ATTRIBUTED)
add("The people, and what is proved about them", f"""
<p>{len(ATTRIBUTED)} lines here carry an attribution backed by a published source. Each
records a <i>role</i> as well as a name, because "named after" and "invented by" are
different claims and the evidence usually supports only one.</p>
<table><tr><th>Line</th><th>Name</th><th>Attribution and role</th></tr>{att_rows}</table>
<p class="small">Roles come from a closed vocabulary: originator, populariser, first to
publish, advocate, key game, resurrector at GM level. Morphy is recorded as the
<i>populariser</i> of 3...a6 because the sources establish that he made it standard and
do not establish that he found it.</p>
<div class="two">
 <div><h3>Identity is the item, not the name</h3>
  <p class="small">Every person in the chronicle carries a Wikidata identity with dates
  where one could be verified, and a visible null where it could not. Roughly two in
  five chess surnames collide with another notable figure, so a catalogue keyed by
  surname would merge strangers. Three names here turned out to be corpus artefacts
  rather than people: a world-championship challenger filed under a man's forename, and
  Frank Marshall under a modern player's name string.</p></div>
 <div><h3>Sources cited for this opening</h3>
  <p class="small">Hooper &amp; Whyld, <i>The Oxford Companion to Chess</i>, 2nd ed.
  1992, carries nine of the eleven; the Kasparov–Kramnik match of 2000 stands behind
  the Berlin endgame; the Marshall rests on the primary record overleaf.</p>
  <p class="small">One printed reference book therefore does most of the work, which is
  worth saying plainly. The Companion is excellent and it is also a single point of
  failure: where it is silent this catalogue is silent, and where an entry of it is
  attached to the wrong row this catalogue inherits the mistake. That happened with the
  Wormald and Worrall attributions, it was found while this volume was being assembled,
  and the attribution was retracted for this edition rather than left standing with an
  apology. The open question it leaves is put to readers at the back.</p></div>
</div>
""", "People")

prop_rows = "".join(
    f'<tr><td class="mono">{p["ocn1"]}</td>'
    f'<td>{(PROP_PEOPLE.get(p["subject_id"]) or PEOPLE.get(p["subject_id"]) or {}).get("display_name", p["subject_id"])}</td></tr>'
    for p in sorted(PROPOSED, key=lambda x: x["ocn1"]))
add("Proposed, and deliberately not applied", f"""
<p>{len(PROPOSED)} further lines have a person proposed but not recorded. They are held
back for one reason: the evidence establishes an <i>eponym</i> and not a <i>role</i>. It
shows that a line carries someone's name; it does not show that they originated it,
popularised it or published it first.</p>
<p>Putting them into <span class="mono">attributed_to</span> would mean inventing the
missing half. So they sit here instead, published as proposals, so anyone can check the
reasoning and, if they hold the source that closes one, say so.</p>
<div class="two">
 <div><table class="tight"><tr><th>Line</th><th>Proposed person</th></tr>{prop_rows}</table></div>
 <div><h3>Why this is the hard part</h3>
  <p class="small">An entire pass of evidence was tested against this rule and one claim
  in five failed it. Some failed interestingly: the person really is the eponym, but of a
  <i>different name for the same opening</i> in another tradition. A few failed
  embarrassingly, including two fictional characters and a company that had been
  resolved, confidently and correctly, as entities that were never people.</p>
  <p class="small">A resolver that returns a confident, technically correct match for
  something that should not be an entity at all is more dangerous than one that returns
  nothing. That is why this table exists and has not been applied.</p>
  <h3>What would move a row out of it</h3>
  <p class="small">A published source that states what the person did, not merely that
  the line bears their name. One sentence in a period magazine is usually enough.</p></div>
</div>
""", "Proposals")

add("A legend, and its sources", f"""
<p>The best-known story in this opening is that Frank Marshall invented 8...d5, kept it
secret for years, and unleashed it on Capablanca at New York 1918. The catalogue records
the gambit under Marshall's name, because the 1918 game is what fixed it there. It does
not record the secrecy, because the sources do not support it.</p>
<div class="two">
 <div>{figure("C.RyL.Mar", "Capablanca accepted, defended, and won.", "board big")}</div>
 <div><h3>What the record shows</h3>
  <p class="small">The gambit was <b>in print eight months earlier</b>: Jaffe and Cleland
  v Marshall and Padelford, New York, c. 15 February 1918, published in the <i>Brooklyn
  Daily Eagle</i> of 7 March 1918, p. 6, including the 16...h5 later debated in analysis.
  The Capablanca game was played on 23 October 1918.</p>
  <p class="small">The citation usually offered for the secrecy story, a Frere v Marshall
  game of 1917, traces to a 1983 <i>Chess Life</i> article whose account is, in Edward
  Winter's words, "devoid of any sources". Winter reports finding that game nowhere
  before Marshall's own <i>Comparative Chess</i> (1932), which printed it undated.</p>
  <p class="small">Older still: the 8.c3 d5 position appears in a Walbrodt consultation
  game, Havana 1893, published in <i>The Chess World</i> (February 1893) and
  <i>Deutsches Wochenschach</i> (2 April 1893).</p></div>
</div>
<p class="small">The note in the catalogue therefore says what the documents show and
stops there. Whether Marshall <i>regarded</i> it as a surprise is not something these
documents settle. Whether it was unpublished is.</p>
""", "Marshall")

place_rows = "".join(f'<tr><td class="mono">{c["ocn1"]}</td><td>{short(c["ocn1"])}</td>'
                     f'<td>{c["subject_id"].replace("-", " ").title()}</td></tr>' for c in PLACES)
ren_rows = "".join(f'<tr><td class="mono">{c["ocn1"]}</td><td class="small">{c["subject_id"][:54]}</td>'
                   f'<td class="mono">{c["date"]}</td></tr>'
                   for c in sorted(RENAMED, key=lambda x: x["ocn1"])[:14])
add("Places, and the names that move", f"""
<p>Not every name is a person. {len(PLACES)} lines here are named after places, and the
catalogue records that as a distinct relation rather than filing a city as though it
were a player.</p>
<table><tr><th>Line</th><th>Name</th><th>Place</th></tr>{place_rows}</table>
<p class="small">Berlin, Rio de Janeiro, Arkhangelsk, Riga, St Petersburg, Breslau,
Bayreuth, Graz, and a Basque, a Norwegian and a Bulgarian variation: a map of where
nineteenth and twentieth century chess was argued about.</p>
<h3>Names are not stable, and the catalogue says when they changed</h3>
<p class="small">{len(RENAMED)} lines here carry a recorded renaming: the name a line
used to have, the date it changed, and the pull request that changed it. Naming is an
editorial act with a history, and hiding that history would make the catalogue look more
authoritative than it is.</p>
<table class="tight"><tr><th>Line</th><th>Previously</th><th>Changed</th></tr>{ren_rows}</table>
""", "Places")

add("The living edge", f"""
<p>Two lines are being explored at the very top right now and both are thinly covered
here. Both are also cases where the working name in the current literature is not the
name in the catalogue, which is the same problem seen from the other side.</p>
<div class="two">
 <div>{figure("C.RyL.Mor.ClD", "4...Bc5, taught in a 2026 course as the Modern Archangel. The catalogue calls it Classical Deferred and holds two sub-lines.", "board big")}</div>
 <div>{figure("C.RyL.Mor.NeA", "5...Bc5, the Møller Defence, taught in a recent book on Carlsen as the Neo-Møller. The catalogue calls it Neo-Arkhangelsk and holds three sub-lines.", "board big")}</div>
</div>
<h3>The gap this exposes</h3>
<p>Of the {len(RYL)} lines here, <b>{len(NO_ALIAS)} carry no alternative name at all</b>.
The string "Archangel" appears nowhere in the catalogue; we hold only "Arkhangelsk".
"Møller" appears only on an Italian Game line, never here. "Delayed Schliemann", the
common English name for 4...f5, appears nowhere: we call it Schliemann Deferred.</p>
<p>The explanation is structural rather than careless. OCN inherited its name vocabulary
from an open corpus with its own conventions, and no layer of <i>working names</i> was
ever added on top: the names books, courses and players actually use. The machinery
exists, the column is there, and the content is not. A reader who searches the name their
own source uses does not find us. This is the least glamorous finding in the volume and
probably the most consequential, because it is the difference between a catalogue that is
correct and one that is findable.</p>
""", "The living edge")

# ---------------- printed attestation
LIT = list(csv.DictReader(
    (OCN / "docs/evidence/provenance/printed-name-attestations.proposed.tsv").open(),
    delimiter="\t"))
for _r in LIT:                      # the evidence file names the columns its own way
    _r["slug"], _r["year"] = _r["ocn1"], _r["date"]
    _m = re.match(r"^(.*?), '(.*?)' \((\d{4})\)", _r["source_ref"])
    _r["author"], _r["title"] = (_m.group(1), _m.group(2)) if _m else ("", _r["source_ref"][:60])
    _r["olid"] = (re.search(r"(OL\d+W)", _r["source_ref"]) or [""])[0] if "OL" in _r["source_ref"] else ""
_APPLIED = sum(1 for _c in CLAIMS if _c["relation"] == "attested-in-print")


def attestation_span(width=470):
    """Each line twice on one axis: when it was played, when it was printed.

    The gap is the point. Everything else in this volume dates a move; a
    title page dates a name, which is the thing the catalogue is actually
    about, and the two are not the same measurement.
    """
    rows = []
    for r in LIT:
        e = _earliest(r["slug"])
        rows.append((r["slug"], CATALOG[r["slug"]]["canonical_name"],
                     e[0] if e else None, int(r["year"])))
    rows.sort(key=lambda x: x[3])
    lo, hi = 1880, 2010
    x0, x1 = 172, width - 26
    def X(y):
        return x0 + (y - lo) / (hi - lo) * (x1 - x0)
    rh, top = 19, 26
    h = top + rh * len(rows) + 8
    p = [f'<svg viewBox="0 0 {width} {h}" xmlns="http://www.w3.org/2000/svg" '
         f'style="width:100%;height:auto">']
    for d in range(1880, 2011, 20):
        p.append(f'<line x1="{X(d):.1f}" y1="{top - 10:.0f}" x2="{X(d):.1f}" '
                 f'y2="{h - 8:.0f}" stroke="#15171a" stroke-width="0.3" opacity="0.13"/>')
        p.append(f'<text x="{X(d):.1f}" y="{top - 14:.0f}" font-size="6" '
                 f'fill="#15171a" opacity="0.5" text-anchor="middle" '
                 f'font-family="IBM Plex Mono">{d}</text>')
    for i, (slug, name, played, printed) in enumerate(rows):
        y = top + rh * i + rh / 2
        label = name.replace("Ruy López", "").strip(" ,") or "Ruy López, the opening itself"
        p.append(f'<text x="0" y="{y + 2.4:.1f}" font-size="7.6" fill="#15171a" '
                 f'font-family="Spectral">{label[:34]}</text>')
        a = min(X(played), X(printed)) if played else X(printed)
        if played:
            b = max(X(played), X(printed))
            p.append(f'<line x1="{a:.1f}" y1="{y:.1f}" x2="{b:.1f}" y2="{y:.1f}" '
                     f'stroke="#15171a" stroke-width="0.5" opacity="0.35"/>')
            p.append(f'<circle cx="{X(played):.1f}" cy="{y:.1f}" r="2.4" fill="#15171a"/>')
            lx, anc = ((X(played) - 5, "end") if X(played) <= X(printed)
                       else (X(played) + 6, "start"))
            p.append(f'<text x="{lx:.1f}" y="{y + 2.2:.1f}" font-size="6" '
                     f'fill="#15171a" opacity="0.6" text-anchor="{anc}" '
                     f'font-family="IBM Plex Mono">{played}</text>')
        p.append(f'<circle cx="{X(printed):.1f}" cy="{y:.1f}" r="3.1" fill="#F0C053" '
                 f'stroke="#654F1E" stroke-width="0.6"/>')
        gx, ganc = ((X(printed) - 6, "end") if played and X(printed) < X(played)
                    else (X(printed) + 6, "start"))
        p.append(f'<text x="{gx:.1f}" y="{y + 2.2:.1f}" font-size="6" text-anchor="{ganc}" '
                 f'fill="#654F1E" font-family="IBM Plex Mono">{printed}</text>')
    p.append("</svg>")
    return "".join(p)


_lit_rows = "".join(
    f'<tr><td class="mono">{r["slug"]}</td>'
    f'<td>{r["title"]}<br><span class="small">{r["author"]}, {r["year"]}</span></td>'
    f'<td class="mono">{r["olid"]}</td></tr>'
    for r in sorted(LIT, key=lambda x: int(x["year"])))

_played = [(_earliest(r["slug"]) or (None,))[0] for r in LIT]
_gaps = [int(r["year"]) - p for r, p in zip(LIT, _played) if p]

add("Dated in print", f"""
<p class="lead">Every other date in this volume is the date of a game. This page holds the
only dates of a different kind: the year a name was on a title page.</p>
<p>The distinction is the whole subject. A game proves when a move was played. It says
nothing about when anybody called the move anything, and a catalogue of names that can
only date moves is dating the wrong thing. A book called <i>Ruy Lopez, Breyer system</i>
and printed in 1976 is direct evidence that the name was in circulation by 1976 — weaker
than a first attestation, because an earlier one almost certainly exists, but it is
evidence of the right kind, and the catalogue held none of it before this volume.</p>
<p class="small">These seven are now <b>claims in the catalogue</b>, under a relation
added for them, <span class="mono">attested-in-print</span>. It is kept distinct from
<span class="mono">analysed-in</span> on purpose: a title page proves the name and says
nothing about the contents of the book, and asserting the stronger relation from the
weaker evidence is the mistake this whole volume is arguing against.</p>
{attestation_span()}
<p class="small">Ink marks the earliest strong game the sample holds for the line; gold
marks the year of the earliest book found that names the line in its title. The bar
between them is not a claim about who was first — it is the distance between the two
things the catalogue can currently measure. Where a line has no ink mark, the sample
holds no game for it at all.</p>
<h3>The seven</h3>
<table class="kv">
 <tr><td class="mono">line</td><td>earliest book <i>found</i> naming it</td><td class="mono">Open Library</td></tr>
 {_lit_rows}
</table>
""", "Dated in print")

def filter_funnel(width=470):
    """How 234 records became seven. The severity is the point: a bibliography
    this catalogue would stand behind has to survive every one of these."""
    steps = [(234, "records returned by Open Library for the distinctive part of each name"),
             (52, "that are a book about a line, rather than about a person or an event"),
             (32, "after removing books whose subject is a rival opening"),
             (16, "after requiring this opening be named wherever a name is shared")]
    rh, bw = 44, width - 40
    p = [f'<svg viewBox="0 0 {width} {rh * len(steps) + 6}" '
         f'xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto">']
    for i, (n, label) in enumerate(steps):
        y = i * rh + 4
        last = i == len(steps) - 1
        p.append(f'<text x="0" y="{y + 9:.0f}" font-size="7.6" fill="#15171a" '
                 f'font-family="Spectral">{label}</text>')
        p.append(f'<rect x="0" y="{y + 16:.0f}" width="{bw * n / 234:.1f}" height="8" '
                 f'fill="{"#F0C053" if last else "#15171a"}" '
                 f'opacity="{1 if last else 0.82}"/>')
        p.append(f'<text x="{bw * n / 234 + 7:.1f}" y="{y + 23:.0f}" font-size="9" '
                 f'fill="{"#654F1E" if last else "#15171a"}" '
                 f'font-family="IBM Plex Mono">{n}</text>')
    p.append("</svg>")
    return "".join(p)


add("What the shelf does not index", f"""
<p class="lead">Seven of {len(RYL)}. The number is worth explaining, because the reason
for it is a finding in its own right.</p>
<p>All {len(RYL)} lines were searched against Open Library's public catalogue, by the
distinctive part of each name. That returned 234 candidate records; filtering left
<b>seven</b>. Two per cent, and the shortfall is not a failure of the method but a fact
about how the literature is indexed. Most opening books are titled for the opening, not
the line — the shelf is full of volumes called <i>The Ruy Lopez</i> that treat forty of
these names inside and announce none of them on the cover.</p>
<p>The rest of the loss is the eponym problem this catalogue keeps running into. A book
titled <i>Panov Attack</i> is about the Caro-Kann, and one titled <i>Rossolimo's
Opening</i> is about the Sicilian, yet this opening holds a Panov System and a Rossolimo
Defence of its own, both hanging off the Chigorin. A title cannot say which is meant, so
a name shared with any line outside this opening was accepted only when the title also
named the Ruy López. That rule is conservative on purpose and it certainly discarded true
books along with false ones. Seven is a floor.</p>
<p>What would actually populate this is not a better search. It is the survey literature —
where every <i>Informant</i> and <i>Yearbook</i> article names its line explicitly — and
the publishers' and course catalogues, none of which is open data. It is also the kind of
thing a reading community knows offhand and no index holds. If you are reading this and
you know the book that first put one of these names in print, that is precisely the
contribution this catalogue cannot generate for itself.</p>
<h3>The filtering, in full</h3>
{filter_funnel()}
<p class="small">Those sixteen books name nine catalogue slugs between them, which is one
more problem: two titles name a line this opening holds twice under different parents.
<i>The Schliemann variation of the Ruy Lopez</i> is the immediate 3…f5 and not the
deferred 4…f5; the Cordel book is the Classical 3…Bc5 and not the Berlin Rio line of the
same name. Reading what each title actually says leaves <b>seven lines</b>. Every step
above is code and reproducible; this last one is a judgement, and it is recorded as a
judgement rather than folded into the filter.</p>
""", "Printed evidence")


# ---------------- the catalogue itself
add("The catalogue", f"""
<p class="lead">Every named line follows, each with the position it denotes, its
identifier, its legacy ECO range and its recorded practice.</p>
<p>All {len(RYL)} of them, in tree order, so a line always appears after the line it
refines. Each entry carries its position, identifier, legacy ECO range, full move list,
recorded practice with the white/draw/black split, the strongest player recorded on it,
when it was first seen at the top, its attribution or the proposal waiting on evidence,
its world-championship games, its renamings, its Lichess cross-reference, and a flow bar
showing how its own sub-lines divide the practice beneath it.</p>
<p class="small">Dates are floors, not firsts. A line's earliest game is the earliest in
the catalogue's game sample anywhere beneath it, and that sample is selected by rating,
so it marks the earliest strong game the catalogue happens to hold rather than the first
time the move was played. The Marshall Attack is the clearest warning: its sample begins
in 1983, while the chapter itself documents the gambit in print in 1918 and the position
in 1893. Where the catalogue knows an earlier game from documents rather than from the
sample, it is in the line's own note, and the note is the better evidence.</p>
<p class="small">Where a line carries an attribution it is printed with it. Where it
carries world-championship games, the count is given. Positions are rendered from the
catalogue's own move lists, so a diagram here is the data and not an illustration of
it.</p>
<h3>Reading an entry</h3>
<table class="kv">
 <tr><td class="mono">identifier, ECO</td><td>stable across releases; the legacy range the line falls in</td></tr>
 <tr><td>canonical name</td><td>what OCN calls it, followed by the full move list</td></tr>
 <tr><td class="mono">practice</td><td>master and Lichess counts, then the white/draw/black split</td></tr>
 <tr><td class="mono">strongest</td><td>the highest-rated player recorded on the line</td></tr>
 <tr><td>attribution</td><td>person and role where a source proves both, or the proposal waiting on one</td></tr>
 <tr><td>claims</td><td>world-championship games, place names, recorded renamings</td></tr>
 <tr><td>sub-lines</td><td>a flow bar dividing this line's practice among its children</td></tr>
</table>
<p class="small">A line with no sub-lines is a leaf: nobody has yet thought a further
distinction worth naming. A line with sub-lines but no practice is a name kept for the
record. Both are deliberate.</p>
<h3>The sub-line bar</h3>
<p class="small">Where an entry ends in a horizontal bar, that bar is the line's own
practice divided among its children, widest first, so a glance shows whether a line
splits evenly or is dominated by one continuation. The named segments are the three
largest; the pale grey tail at the right, where present, is everything beyond the ninth
child. A line whose bar is one long block has children in name only, as far as practice
is concerned.</p>
<h3>Games</h3>
<p class="small">Where an entry lists games, those in dark type are world-championship
games already recorded as claims in the catalogue. Those in grey with a Lichess
identifier come from a proposal of 1,172 games over 307 of these lines, selected by
rating, which has <b>not been applied</b> — the catalogue has no relation that describes
"a notable game" honestly, and inventing one to fit the data would be the wrong order of
operations. They are printed here because they are useful and marked because they are
not yet ours to assert.</p>
""", "Catalogue")


def pct(a, b):
    return f"{a/b*100:.0f}%" if b else "—"

def child_flow(slug, width=470, height=15):
    kids = CHILDREN.get(slug, [])
    if not kids:
        return ""
    tot = sum(games(k) for k in kids)
    shown = kids[:9]
    if tot == 0:
        names = ", ".join(short(k) for k in shown[:5])
        more = f" and {len(kids)-5} more" if len(kids) > 5 else ""
        return (f'<div class="kids"><span class="kh">{len(kids)} sub-lines, none with '
                f'recorded practice:</span> <span class="kn">{names}{more}</span></div>')
    x, parts, labels = 0.0, [], []
    for i, k in enumerate(shown):
        g = games(k)
        w = max(g / tot * width, 1.2)
        op = 1 - (i * 0.075)
        parts.append(f'<rect x="{x:.1f}" y="0" width="{w:.1f}" height="{height}" '
                     f'fill="{INK}" opacity="{max(op * 0.62, 0.16):.2f}"/>')
        if w > 34:
            labels.append(f'<text x="{x+3:.1f}" y="{height-4}" font-size="5.4" fill="{PAPER}" '
                          f'font-family="Plex Mono, monospace">{short(k)[:16]}</text>')
        x += w
    rest = sum(games(k) for k in kids[9:])
    if rest:
        w = max(rest / tot * width, 1.2)
        parts.append(f'<rect x="{x:.1f}" y="0" width="{w:.1f}" height="{height}" '
                     f'fill="#b8b1a1" opacity="0.5"/>')
    top3 = ", ".join(f"{short(k)} {games(k):,}" for k in shown[:3] if games(k))
    return (f'<div class="kids2"><div class="kh">{len(kids)} sub-lines, by share of this '
            f'line\'s practice</div>'
            f'<svg viewBox="0 0 {width} {height}" class="kflow2" '
            f'xmlns="http://www.w3.org/2000/svg" role="img"><title>Sub-lines by practice</title>'
            f'{"".join(parts)}{"".join(labels)}</svg>'
            f'<div class="kn2">{top3}</div></div>')

def first_seen(slug):
    ws = [int(r["year"]) for r in WCH if r["ocn1"] == slug and r["year"].isdigit()]
    if ws:
        return f"first at world-championship level {min(ws)}"
    r = POP.get(slug)
    if r and r.get("top_game_year_earliest"):
        return f"strongest games {r['top_game_year_earliest']}–{r['top_game_year_latest']}"
    return ""

def entry_full(slug):
    r = CATALOG[slug]
    g, l = games(slug), lich(slug)
    p = POP.get(slug, {})
    w = int(p.get("masters_white") or 0); d = int(p.get("masters_draws") or 0)
    b = int(p.get("masters_black") or 0)
    meta = [f'<span class="slug">{slug}</span>', f'<span class="eco">{eco_of(slug)}</span>']
    for fl in [x.strip() for x in r["flags"].split("|") if x.strip()]:
        meta.append(f'<span class="flag">{fl}</span>')
    nb = (BASIS.get(slug) or {}).get("name_basis", "")
    if nb and nb != "review":
        meta.append(f'<span class="flag basis">{nb} name</span>')
    lines = []
    if r["notes"].strip():
        lines.append(f'<span class="note">{r["notes"].strip()}</span>')
    al = [a.strip() for a in r["aliases"].split("|") if a.strip()]
    if al:
        lines.append(f'<span class="alias">also: {"; ".join(al[:3])}'
                     f'{f" and {len(al)-3} more" if len(al) > 3 else ""}</span>')
    if g:
        lines.append(f'<span class="mono">{g:,} master, {l:,} Lichess</span> '
                     f'<span class="eco">W {pct(w,g)} / D {pct(d,g)} / B {pct(b,g)}</span>')
        if p.get("top_player"):
            lines.append(f'<span class="eco">strongest: {p["top_player"]} '
                         f'({p.get("top_player_elo","")})</span>')
    else:
        lines.append('<span class="eco">no master practice recorded</span>')
    fg = FIRST_GAME.get(slug)
    if fg:
        y, g = fg
        w_, b_ = g.get("white", ""), g.get("black", "")
        if g.get("lichess_id"):
            t = GAME_TAGS.get(g["lichess_id"], {})
            when = pretty_date(t.get("date", "")) or str(y)
            wh = where(g["lichess_id"])
        else:
            when = str(y)
            wh = ", ".join(x for x in (g.get("event", ""), g.get("place", "")) if x)
        lines.append(f'<span class="first">earliest in the sample {when}: {w_} v {b_}'
                     f'{", " + wh if wh else ""}</span>')
    fs = first_seen(slug)
    if fs and not fg:
        lines.append(f'<span class="eco">{fs}</span>')
    a = r["attributed_to"]
    if a:
        gr = (ATTRSIDE.get(slug) or {}).get("evidence_grade", "")
        lines.append(f'<span class="attr">{a}</span>'
                     + (f' <span class="eco">[{gr}]</span>' if gr and gr != "unknown" else ""))
    elif slug in PROP_BY_SLUG:
        pid = PROP_BY_SLUG[slug]["subject_id"]
        nm = (PROP_PEOPLE.get(pid) or PEOPLE.get(pid) or {}).get("display_name", pid)
        lines.append(f'<span class="prop">eponym proposed, role unproved: {nm}</span>')
    if r.get("historical_notes", "").strip():
        lines.append(f'<span class="hist">{r["historical_notes"].strip()}</span>')
    elif not a and slug not in PROP_BY_SLUG:
        # Nothing documentary on this line. Naming is inherited, so the reader is
        # pointed at the nearest line above it that does carry something, rather
        # than being left to conclude that nobody has ever written about any of it.
        anc, up = CATALOG[slug]["parent_ocn1"], 1
        while anc and anc in RYL:
            ar = CATALOG[anc]
            if ar["attributed_to"].strip() or ar.get("historical_notes", "").strip():
                # Only worth printing while the ancestor is close enough to be
                # about this line. Five levels up is the chapter, which the
                # reader is already inside.
                if up <= 3:
                    lines.append(f'<span class="inh">nothing documentary here; '
                                 f'nearest is <b>{short(anc)}</b></span>')
                break
            anc, up = ar["parent_ocn1"], up + 1
    cl = CLAIM_BY_SLUG.get(slug, [])
    wq = sum(1 for c in cl if c["relation"] == "wch-game")
    pl = [c for c in cl if c["relation"] == "named-after-place"]
    rn = [c for c in cl if c["relation"] == "renamed"]
    if wq:
        lines.append(f'<span class="eco">{wq} world-championship game{"s" if wq>1 else ""}</span>')
    if pl:
        lines.append(f'<span class="attr">named after {pl[0]["subject_id"].replace("-", " ").title()}</span>')
    if rn:
        _src = rn[0].get("source_ref", "")
        _pr = re.search(r"pull/(\d+)", _src)
        _sha = re.search(r"commit ([0-9a-f]{7})", _src)
        _where = (f' &nbsp;lichess-org/chess-openings&#8202;#{_pr.group(1)}' if _pr
                  else f' &nbsp;commit {_sha.group(1)}' if _sha else "")
        lines.append(f'<span class="prop">renamed {rn[0]["date"]}, was: '
                     f'{rn[0]["subject_id"][:44]}{_where}</span>')
    tr = [t.strip() for t in r["transposes_to"].split("|") if t.strip()]
    if tr:
        lines.append(f'<span class="prop">transposes to {", ".join(tr)}</span>')
    xr = XREF.get(slug)
    if xr and xr.get("lichess_name"):
        lines.append(f'<span class="xref">Lichess: {xr["lichess_name"][:54]}</span>')
    gl = []
    for g in WCH_GAMES.get(slug, [])[:2]:
        pl = f', {g["place"]}' if g.get("place") else ""
        gl.append(f'<span class="wg">{g["white"]} v {g["black"]}, {g["event"]}'
                  f'{pl}, {g["year"]} &nbsp;{g["result"]}</span>')
    for g in NOTABLE.get(slug, [])[:3]:
        wh = where(g["lichess_id"])
        gl.append(f'<span class="ng">{g["white"]} {g["white_elo"]} v {g["black"]} '
                  f'{g["black_elo"]} &nbsp;{g["result"]}'
                  f'{", " + wh if wh else ""}, {g["year"]}</span>')
    if gl:
        n_more = max(len(NOTABLE.get(slug, [])) - 3, 0)
        games_html = (f'<div class="gm"><span class="gh">games</span>'
                      f'<span class="gg">{"<br>".join(gl)}'
                      f'{f"<br><span class=gmore>and {n_more} more in the proposal</span>" if n_more else ""}'
                      f'</span></div>')
    else:
        games_html = ""
    kf = child_flow(slug)
    # height model in mm: count wrapped rows from actual text length.
    # the detail column is ~136mm wide; at 7.6pt that is roughly 88 characters.
    strip = lambda t: re.sub(r"<[^>]+>", "", t)
    rows_ = sum(max(1, math.ceil(len(strip(x)) / 88)) for x in lines)
    mv_rows = max(1, math.ceil(len(moves_text(slug)) / 104))
    nm_rows = max(1, math.ceil(len(r["canonical_name"]) / 46))
    text_mm = (nm_rows * 5.0 + mv_rows * 3.1 + rows_ * 3.25 + (4.6 if kf else 0)
               + len(gl) * 2.9 + (1.6 if gl else 0) + 3.4)
    mm = max(34.0, text_mm) + 5.4
    html = (f'<div class="fentry"><div class="fb">{board_of(slug)}</div>'
            f'<div class="fd"><div class="fh">{" ".join(meta)}</div>'
            f'<div class="fn">{r["canonical_name"]}</div>'
            f'<div class="fm mono">{moves_text(slug)}</div>'
            f'<div class="fs">{"<br>".join(lines)}</div>'
            f'{games_html}{kf}</div></div>')
    return html, mm

def entry_big(s):
    a = CATALOG[s]["attributed_to"]
    w = WCH_BY_SLUG.get(s, 0)
    extra = []
    if a:
        extra.append(f'<span class="attr">{a}</span>')
    if w:
        extra.append(f'<span class="eco">{w} championship game{"s" if w > 1 else ""}</span>')
    if s in PROP_BY_SLUG:
        pid = PROP_BY_SLUG[s]["subject_id"]
        nm = (PROP_PEOPLE.get(pid) or PEOPLE.get(pid) or {}).get("display_name", pid)
        extra.append(f'<span class="prop">proposed: {nm}</span>')
    g = games(s)
    return (f'<figure class="entry big">{board_of(s)}'
            f'<figcaption><span class="slug">{s}</span> <span class="eco">{eco_of(s)}</span>'
            f'<br><b>{short(s)}</b>'
            f'<br><span class="mono mv">{moves_text(s)}</span>'
            f'<br><span class="eco">{f"{g:,} master, {lich(s):,} Lichess" if g else "no master games"}</span>'
            f'{"<br>" + "<br>".join(extra) if extra else ""}</figcaption></figure>')

def entry_small(s):
    g = games(s)
    a = CATALOG[s]["attributed_to"]
    return (f'<figure class="entry sm">{board_of(s)}'
            f'<figcaption><span class="slug">{s}</span><br><b>{short(s)}</b>'
            f'<br><span class="eco">{eco_of(s)} · {f"{g:,}" if g else "—"}</span>'
            f'{f"<br><span class=chip>{a.split(chr(40))[0].strip()}</span>" if a else ""}'
            f'</figcaption></figure>')

def full_order():
    out = []
    def walk(x):
        out.append(x)
        for k in CHILDREN.get(x, []):
            walk(k)
    walk(ROOT)
    return out

FULL = full_order()
BUDGET_MM = 236.0
try:
    import json
    MEASURED = {k: v / 3.7795 for k, v in json.load(open(HERE / "heights.json")).items()}
except Exception:
    MEASURED = {}

ALL_BRANCHES = sorted((s0 for s0 in RYL if int(CATALOG[s0]["depth"]) == 2),
                      key=lambda s0: -len(subtree(s0)))

def earns_cover(s0):
    """A chapter of its own for size, for practice, or for having been played
    for the world title. Everything else is gathered."""
    return (len(subtree(s0)) >= 6
            or games(s0) >= 2000
            or sum(WCH_BY_SLUG.get(x, 0) for x in subtree(s0)) >= 1)

GATEWAY = "C.RyL.Mor"        # 3...a6, through which two thirds of practice passes
_promoted = sorted(CHILDREN.get(GATEWAY, []), key=lambda x: -len(subtree(x)))
CHAPTERS = ([s0 for s0 in ALL_BRANCHES if earns_cover(s0) and s0 != GATEWAY]
            + _promoted)
CHAPTERS.sort(key=lambda x: -len(subtree(x)))
GATHERED = [s0 for s0 in ALL_BRANCHES if not earns_cover(s0)]
CHAPTER_AT = {}   # chapter slug -> index in PAGES
SLUG_PAGE = {}    # line slug -> index in PAGES of the page its entry is on

# ---- chronology ----
chron_raw = sorted(((y, sl, g) for sl, (y, g) in FIRST_GAME.items()),
                   key=lambda t: (t[0], t[1]))
# A line inherits the games beneath it, so one game can be the earliest for a
# parent and every child in the chain. Group by game and name the lines it dates.
_by_game = {}
for y, sl, g in chron_raw:
    key = (y, g.get("white", ""), g.get("black", ""),
           g.get("lichess_id") or g.get("event", ""))
    _by_game.setdefault(key, [y, g, []])[2].append(sl)
chron = sorted(_by_game.values(), key=lambda t: (t[0], t[2][0]))

def _chron_cells(y, g, slugs):
    """The three cells of a chronology row, so height and markup agree."""
    if g.get("lichess_id"):
        t = GAME_TAGS.get(g["lichess_id"], {})
        when, wh = pretty_date(t.get("date", "")) or str(y), where(g["lichess_id"])
    else:
        when = str(y)
        wh = ", ".join(x for x in (g.get("event", ""), g.get("place", "")) if x)
    names = "; ".join(short(x) for x in slugs[:4])
    if len(slugs) > 4:
        names += f" and {len(slugs) - 4} more"
    return (f'{g.get("white","")} v {g.get("black","")}',
            f'{when}{", " + wh if wh else ""}', names,
            f'{len(slugs)} line{"s" if len(slugs) != 1 else ""}')


def _chron_height(y, g, slugs):
    """Rows are not one height: a game that dates a chain of five lines is
    three lines tall and one that dates a leaf is two. Packing by a fixed
    count is what pushed rows under the folio."""
    game, sub, names, count = _chron_cells(y, g, slugs)
    gm = -(-len(game) // 49) + -(-len(sub) // 49)
    ln = -(-len(names) // 59) + 1
    return 2.94 + 4.0 * max(gm, ln, 2)


def balance(items):
    """Split entries across pages in tree order, evening out the fill.

    Greedy first-fit never looks ahead, so with entries averaging 89mm against
    a 236mm page it leaves two on a page and starts a third — a quarter of the
    book set at two thirds density. This finds the fewest pages that fit, then
    the smallest maximum page height achievable with that many, which spreads
    the slack instead of dumping it all on the last page. Order is preserved,
    because a line must still follow the line it refines.
    """
    hs = [m for _s, _h, m in items]

    def pages_needed(cap):
        n, used = 1, 0.0
        for m in hs:
            if used and used + m > cap:
                n, used = n + 1, 0.0
            used += m
        return n

    if not hs:
        return []
    k = pages_needed(BUDGET_MM)
    lo, hi = max(hs), BUDGET_MM
    while hi - lo > 0.5:                     # smallest cap that still fits in k
        mid = (lo + hi) / 2
        if pages_needed(mid) <= k:
            hi = mid
        else:
            lo = mid
    out, cur, used = [], [], 0.0
    for it, m in zip(items, hs):
        if cur and used + m > hi:
            out.append(cur); cur, used = [], 0.0
        cur.append(it); used += m
    if cur:
        out.append(cur)
    return out


# greedy-pack by measured content, first page shorter for the two intro paragraphs
CHRON_PAGES, _cur, _h, _budget = [], [], 0.0, 174.0
for _row in chron:
    _rh = _chron_height(*_row)
    if _cur and _h + _rh > _budget:
        CHRON_PAGES.append(_cur)
        _cur, _h, _budget = [], 0.0, 222.0
    _cur.append(_row)
    _h += _rh
if _cur:
    CHRON_PAGES.append(_cur)

for i, chunk in enumerate(CHRON_PAGES):
    rows_ = ""
    for y, g, slugs in chunk:
        game, sub, names, count = _chron_cells(y, g, slugs)
        rows_ += (f'<tr><td class="num yr">{y}</td>'
                  f'<td class="gm2">{game}<br><span class="eco">{sub}</span></td>'
                  f'<td class="ln2">{names}<br>'
                  f'<span class="eco">{count}</span></td></tr>')
    intro = ("<p>The catalogue in order of the earliest game it can show. A line "
             "inherits the games of the lines beneath it, because a game played in a "
             "sub-line is a game of the line it refines, so one game often dates a "
             "whole chain at once; the lines it dates are named beside it. "
             f"{len(FIRST_GAME)} of {len(RYL)} lines can be dated at all, by "
             f"{len(chron)} distinct games, from {chron[0][0]} to {chron[-1][0]}.</p>"
             "<p class=\"small\">This is a floor, not a first. The sample is selected "
             "by rating, so it shows the earliest strong game the catalogue holds, not "
             "the first time anybody played the move. The Marshall Attack enters this "
             "table in 1983, while its own chapter documents the gambit in print in "
             "1918. Where a date looks late for a line you know to be old, that is the "
             "sample speaking, and the catalogue would rather say so than imply a "
             "discovery.</p>") if i == 0 else ""
    add(f"Chronology, by earliest game in the sample ({i+1} of "
        f"{len(CHRON_PAGES)})",
        f'{intro}<table class="chron"><tr><th class="num">Year</th><th>Game</th>'
        f'<th>Lines it dates</th></tr>{rows_}</table>', "Chronology")

# ---- chapters ----
add("The chapters", f"""
<p class="lead">The catalogue proper follows, divided into {len(CHAPTERS)} chapters, one
for each line that branches directly from 3.Bb5.</p>
<p>Each chapter opens with its position, its figures and a dendrogram of everything named
beneath it, then gives every line in that branch in tree order. Chapters are ordered by
size, from the Morphy Defence with {len(subtree("C.RyL.Mor"))} names down to the several
that are a single line with no descendants at all.</p>
<p class="small">A chapter of one line is not an oversight. It means somebody named a
reply to 3.Bb5 and nobody has since thought any continuation of it worth a name of its
own. The catalogue keeps both kinds of fact.</p>
<table class="tight"><tr><th>Chapter</th><th>Name</th><th class="num">Lines</th>
 <th class="num">Master games</th><th class="num">WCh</th></tr>
{"".join(f'<tr><td class="mono">{c}</td><td>{short(c)}</td>'
         f'<td class="num">{len(subtree(c))}</td><td class="num">{games(c):,}</td>'
         f'<td class="num">{sum(WCH_BY_SLUG.get(x,0) for x in subtree(c)) or "—"}</td></tr>'
         for c in CHAPTERS)}
</table>
""", "Chapters")

# first pass: how many pages does each chapter occupy
CH_PAGES = {}
for ch in CHAPTERS:
    nodes = subtree(ch)
    used, pages_ = 0.0, 1
    for x in nodes:
        mm = MEASURED.get(x, entry_full(x)[1])
        if used + mm > BUDGET_MM:
            pages_ += 1; used = 0.0
        used += mm
    CH_PAGES[ch] = pages_ + 1          # + the cover

def band(current):
    total = sum(CH_PAGES.values())
    x, segs = 0.0, []
    for c in CHAPTERS:
        w = max(CH_PAGES[c] / total * 100, 1.0)
        segs.append(f'<span class="bandseg{" on" if c == current else ""}" '
                    f'style="width:{w:.2f}%"></span>')
    return f'<div class="pband">{"".join(segs)}</div>'

_gw_kids = set(_promoted)
_gw_done = False
for ci, ch in enumerate(CHAPTERS, 1):
    if ch in _gw_kids and not _gw_done:
        _gw_done = True
        add("The gateway: 3...a6", f"""
<p class="lead">Two thirds of all Ruy López master practice passes through
3...a6, the Morphy Defence. It is not a variation of the opening so much as the
door most of the opening goes through.</p>
<div class="two">
 <div>{figure(GATEWAY, "The position after 3...a6. Named for Morphy as populariser, not inventor.", "board big")}</div>
 <div>
  <h3>Why it has no chapter of its own</h3>
  <p class="small">{len(subtree(GATEWAY))} of the {len(RYL)} named lines in this
  catalogue hang from this move, which is more than a chapter can hold and more
  than a reader can navigate. Its {len(_promoted)} branches are therefore given
  chapters of their own, in the order of the catalogue's usual ranking, and this
  page stands in for the parent.</p>
  <p class="small mono">{games(GATEWAY):,} master, {lich(GATEWAY):,} Lichess<br>
  earliest in the sample {FIRST_GAME[GATEWAY][0]}</p>
  <h3>Its branches</h3>
  <div class="eco">{"<br>".join(f"{short(k)} &nbsp;{len(subtree(k))} lines, {games(k):,} master" for k in _promoted)}</div>
 </div>
</div>
""", "The gateway")
    CHAPTER_AT[ch] = len(PAGES)
    add(f"Chapter {ci}. {short(ch)}", chapter_cover(ci, ch, ""),
        f"Chapter {ci}", cls="chcover")
    nodes = subtree(ch)
    rendered = [(x, entry_full(x)[0], MEASURED.get(x, entry_full(x)[1])) for x in nodes]
    pgs = [[(s_, h_) for s_, h_, _m in grp]
           for grp in balance([(s_, h_, m_) for s_, h_, m_ in rendered])]
    for n, chunk in enumerate(pgs, 1):
        for slug_, _h in chunk:
            SLUG_PAGE[slug_] = len(PAGES)
        add(f"Chapter {ci}. {short(ch)}" + (f" ({n} of {len(pgs)})" if len(pgs) > 1 else ""),
            "".join(h for _s, h in chunk), f"Chapter {ci}")

GATH_NODES = [x for c in GATHERED for x in subtree(c)]
add("The single names", f"""
<p class="lead">{len(GATHERED)} replies to 3.Bb5 carry a name and almost nothing else:
{len(GATH_NODES)} lines between them, and in most cases nobody has ever thought a
continuation of them worth naming.</p>
<p>They are gathered here rather than given a chapter each, because they are more
interesting as a set than as {len(GATHERED)} near-empty openings. The set makes a point
the rest of the book cannot: a catalogue of names must keep the name that was given, not
only the name that was used. Several of these have a sourced attribution from the Oxford
Companion and no master game at all — somebody was named, and the line was then never
played strongly again.</p>
<div class="gathered">
{"".join(f'<figure class="gcell">{board_of(c)}<figcaption>'
         f'<span class="slug">{c}</span> <span class="eco">{eco_of(c)}</span><br>'
         f'<b>{short(c)}</b><br><span class="cap">{CATALOG[c]["notes"].strip()}</span><br>'
         f'<span class="eco">{games(c):,} master, {lich(c):,} Lichess</span>'
         f'{_gcell_attr(c)}'
         f'</figcaption></figure>' for c in GATHERED)}
</div>
""", "Single names")
_rend = [(entry_full(x)[0], MEASURED.get(x, entry_full(x)[1])) for x in GATH_NODES]
_cur, _used, _pgs = [], 0.0, []
for _h, _mm in _rend:
    if _cur and _used + _mm > BUDGET_MM:
        _pgs.append(_cur); _cur, _used = [], 0.0
    _cur.append(_h); _used += _mm
if _cur:
    _pgs.append(_cur)
for _n, _chunk in enumerate(_pgs, 1):
    add("The single names, in full" + (f" ({_n} of {len(_pgs)})" if len(_pgs) > 1 else ""),
        "".join(_chunk), "Single names")

add("What we cannot answer", f"""
<p>Three questions where a community with long memories and deep databases is better
placed than a small club with a spreadsheet. None needs research funding; all three need
someone who happens to know.</p>
<div class="ask"><h4>1. Wormald or Worrall? We found our own catalogue wrong and can only half fix it.</h4>
 <div class="two" style="margin:2.5mm 0">
  <div>{figure("C.RyL.Mor.Wor", "5.Qe2, which we call the Wormald Attack.")}</div>
  <div>{figure("C.RyL.Mor.Ba4.Nf6.O-O.Wor", "6.Qe2, the Worrall Attack, with no attribution at all.")}</div></div>
 <p class="small">Until this edition the first row carried an attribution to Thomas
 Herbert Worrall (1807-78), sourced to the <i>Oxford Companion</i> entry "Worrall
 Attack". That entry is about 6.Qe2, the second position, while the row it sat on is the
 5.Qe2 line named for Robert Wormald: it had been matched on the fragment
 <span class="mono">Wor</span> the two identifiers share. It is <b>retracted</b> here
 rather than moved, because the Companion gives an eponym and not a role. The error is
 gone and the question is not, since neither row now says who named it.
 <b>What would help:</b> the earliest printed use of each name, and for which move
 order.</p></div>
<div class="ask"><h4>2. A 1938 column we can see but cannot read.</h4>
 <p class="small">Walter Penn Shipley's "Chess and Checkers" column in the
 <i>Philadelphia Inquirer</i> of 6 March 1938, page 8A, carries a remark about the
 Marshall Gambit before 1918 that Edward Winter singles out as noteworthy (C.N. 11754).
 It survives as a facsimile image and we have not been able to transcribe it.
 <b>What would help:</b> the text of that remark, and anything else Shipley, who knew
 Marshall, wrote about when the gambit was first seen.</p></div>
<div class="ask"><h4>3. Which names do your readers actually use?</h4>
 <p class="small">The one we most need, and the one only a community can answer. Of the
 {len(RYL)} lines here, {len(NO_ALIAS)} carry no alternative name at all. A course
 published this year teaches 4...Bc5 as the <b>Modern Archangel</b>; we call it Classical
 Deferred and "Archangel" appears nowhere in our data. A recent book on Carlsen teaches
 5...Bc5 as the <b>Neo-Møller</b>; we call it Neo-Arkhangelsk, and "Møller" appears in
 our data only for an Italian Game line. Anyone searching the name their own source uses
 would not find us. <b>What would help:</b> the working names your readers actually type,
 so we can record them alongside ours instead of choosing for them.</p></div>
""", "Open questions")

add("The data, and how to take it", f"""
<p>Everything in this volume is generated from the public catalogue. Nothing was
transcribed by hand, which is deliberate: if a fact here is wrong it is wrong in the data
too, and fixing the data fixes the document.</p>
<table><tr><th>What</th><th>Where</th></tr>
 <tr><td>Catalogue, spec and tools</td><td class="mono">github.com/escacsfigueres/ocn</td></tr>
 <tr><td>Live explorer</td><td class="mono">ocn.vercel.app</td></tr>
 <tr><td>Citable release</td><td class="mono">doi:10.5281/zenodo.21670207</td></tr>
 <tr><td>Catalogue and spec</td><td class="mono">CC BY 4.0</td></tr>
 <tr><td>Tools</td><td class="mono">MIT</td></tr></table>
<h3>And one standing question</h3>
<p class="small">This opening is the Ruy López to English speakers and the Spanish Opening
to much of Europe; the same Semi-Slav line is the Reynolds Variation to the English and
the Klaus Junge line to the Germans. A catalogue must choose a canonical name, and every
choice buries a tradition. We would rather record the divergence than pick a winner, and
we are designing a way to do it.</p>
<h3>What we would offer in return</h3>
<p class="small">Deep links per opening from our explorer and dataset back to your pages,
so every OCN entry can send a reader to the games and the discussion. The catalogue
itself, CC BY and yours to use: the naming hierarchy, the sourced attributions, the
position-keyed cross-references. And credit as provenance, recorded in the catalogue for
the leads contributed.</p>
<h3>Sources used in this volume</h3>
<h3>How to reproduce this</h3>
<p class="small">This volume is generated, so it should be checkable. Catalogue
<b>ocn-1</b> at commit <span class="mono">{_COMMIT}</span>, {len(CATALOG):,} rows,
{len(RYL)} of them Ruy López. Master and club counts from the Lichess opening explorer as
recorded in <span class="mono">ocn-1.popularity.tsv</span>, retrieved
{_RETRIEVED}. Game headers from the Lichess bulk export. The bibliographic search of
Open Library was run on 2026-08-03. Built {_BUILT}. A claim you want to correct should be
quoted with its identifier and that commit, because both will change.</p>
<h3>What is and is not CC-BY here</h3>
<p class="small">The catalogue and this volume's own text are CC-BY-4.0. The quotations
are not, and appearing inside a CC-BY document does not relicense them: the passages from
Hooper &amp; Whyld's <i>Oxford Companion to Chess</i>, from <i>Le Palamède</i> and from
the newspaper columns cited in the Marshall chapter remain the property of their rights
holders and are reproduced here as short quotations for commentary. Reuse the data
freely; clear the quotations yourself. The Cburnett piece set is CC-BY-SA 3.0, u_DIN and
Spectral are under the SIL Open Font License, and IBM Plex Mono under the same.</p>
<p class="small">Ruy López de Segura, <i>Libro de la invención liberal y arte del juego
del axedrez</i>, 1561; Staunton, <i>Chess Player's Chronicle</i>, 1846; <i>Le
Palamède</i>, March 1846; <i>The Chess World</i>, February 1893; <i>Deutsches
Wochenschach</i>, 2 April 1893; <i>Brooklyn Daily Eagle</i>, 7 March 1918; F.J. Marshall,
<i>Comparative Chess</i>, 1932; W.P. Shipley, <i>Philadelphia Inquirer</i>, 6 March 1938;
A. Soltis, <i>Chess Life</i>, January 1983; Hooper &amp; Whyld, <i>The Oxford Companion to
Chess</i>, 2nd ed. 1992; Edward Winter, <i>Chess Notes</i>, items 3980, 5664, 6777, 6980,
9822, 11754; and, for the living edge, the 2026 course on the Modern Archangel and the
recent New in Chess volume on Carlsen's Neo-Møller. Every historical item was read at
source before it was recorded.</p>
<h3>Typography and pieces</h3>
<p class="small">Set in u_DIN 1451 Mittelschrift (OFL), Spectral and IBM Plex Mono.
Diagrams use the Cburnett piece set by Colin M.L. Burnett (CC BY-SA 3.0), the same pieces
Wikipedia and Lichess use, rendered from the catalogue's own move lists.</p>
<div class="endfoot"><span class="din">CLUB D'ESCACS FIGUERES</span>
 <span class="lockup"><svg viewBox="0 0 {HW} 72" xmlns="http://www.w3.org/2000/svg">{lock}</svg></span></div>
""", "Colophon")

# ------------------------------------------------------------------ css

CSS = f"""
{FONTS}
@page {{ size: A4; margin: 0; }}
* {{ margin: 0; box-sizing: border-box; }}
html {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
body {{ font-family: Spectral, serif; color: {INK}; background: {PAPER};
  font-size: 10.2pt; line-height: 1.6; counter-reset: page; }}
.page {{ width: 210mm; height: 297mm; padding: 20mm 18mm 16mm; position: relative;
  page-break-after: always; overflow: hidden; counter-increment: page; }}
.page:last-child {{ page-break-after: auto; }}
h1,h2,h3,h4,.din {{ font-family:'OCN DIN',Spectral,serif; font-weight:400; letter-spacing:.05em; }}
h2 {{ font-size: 18pt; margin-bottom: 3mm; }}
h3 {{ font-size: 10.5pt; letter-spacing: .14em; text-transform: uppercase; color: {INK}; opacity:.62; margin: 5.5mm 0 1.6mm; }}
p {{ margin-bottom: 2.8mm; max-width: 64em; hyphens: auto; }}
.lead {{ font-size: 11.6pt; }}
.small {{ font-size: 8.9pt; line-height: 1.5; }}
.mono {{ font-family: 'Plex Mono', monospace; font-size: 8.2pt; }}
blockquote {{ margin: 3mm 0 3mm 5mm; padding-left: 4.5mm; border-left: 2.5pt solid {INK};
  font-style: italic; font-size: 9.6pt; }}
blockquote .src {{ display:block; font-style:normal; font-family:'Plex Mono',monospace;
  font-size: 7.4pt; color:#5c5f64; margin-top:1.4mm; }}
.cover {{ padding: 0; }}
.cover .band {{ position:absolute; inset:0 0 auto 0; height:12mm; background:{BAND}; }}
.cover .inner {{ position:absolute; inset:22mm 20mm 16mm; }}
.cover .eyebrow {{ font-size:9.5pt; letter-spacing:.34em; }}
.cover .micro {{ position:absolute; right:0; top:8mm; width:16mm; }}
.cover .letter {{ position:absolute; left:50%; top:34mm; transform:translateX(-50%);
  font-size:124mm; line-height:.78; color:{BAND}; }}
.cover h1 {{ position:absolute; left:0; right:0; top:182mm; text-align:center; font-size:26pt; letter-spacing:.1em; }}
.cover .sub {{ position:absolute; left:0; right:0; top:196mm; text-align:center; color:{NAMING};
  font-family:'Plex Mono',monospace; font-size:8.2pt; letter-spacing:.18em; line-height:2; }}
.cover .foot {{ position:absolute; left:0; right:0; bottom:0; display:flex; justify-content:space-between; align-items:flex-end; }}
.foot .din, .endfoot .din {{ font-size:8.2pt; letter-spacing:.2em; }}
.endfoot {{ position:absolute; left:18mm; right:18mm; bottom:16mm; display:flex; justify-content:space-between; align-items:flex-end; }}
.lockup {{ width:44mm; }} .lockup svg, .micro svg {{ display:block; width:100%; height:auto; }}
.folio {{ position:absolute; bottom:7mm; left:18mm; right:18mm; display:flex; justify-content:space-between;
  font-family:'Plex Mono',monospace; font-size:7.2pt; color:#6b6e73; border-top:.5pt solid #cfcabb; padding-top:2mm; }}
.pn::before {{ content: counter(page); }}
.two {{ display:grid; grid-template-columns:1fr 1fr; gap:7mm; }}
figure {{ margin:0; }}
.board {{ display:block; width:100%; height:auto; }}
.diagram figcaption {{ margin-top:1.6mm; font-size:8pt; line-height:1.34; }}
.diagram .slug, .entry .slug {{ font-family:'Plex Mono',monospace; font-size:7.4pt; color:{INK}; opacity:.55; }}
.diagram .eco, .entry .eco {{ font-family:'Plex Mono',monospace; font-size:7.4pt; color:#6b6e73; }}
.diagram .cap {{ color:#3c3f44; }}
table {{ border-collapse:collapse; width:100%; margin-top:2.5mm; font-size:8.9pt; }}
th, td {{ text-align:left; padding:1.1mm 1.8mm; border-bottom:.4pt solid #d8d3c6; vertical-align:top; }}
th {{ font-family:'OCN DIN',Spectral,serif; letter-spacing:.1em; font-size:8.2pt; text-transform:uppercase;
  color:{INK}; opacity:.62; border-bottom:1pt solid {INK}; }}
td.num, th.num {{ text-align:right; font-family:'Plex Mono',monospace; font-size:8.2pt; }}
table.tight td, table.tight th {{ padding:.65mm 1.3mm; font-size:8pt; }}
table.kv td:first-child {{ width:34mm; color:{INK}; opacity:.62; }}
.stats {{ display:flex; flex-wrap:wrap; gap:6.5mm; margin:4mm 0 2mm; }}
.stat .n {{ font-family:'OCN DIN',Spectral,serif; font-size:21pt; line-height:1; }}
.stat .l {{ font-family:'Plex Mono',monospace; font-size:7pt; color:#6b6e73; letter-spacing:.05em; text-transform:uppercase; }}
.bars {{ margin:3mm 0 4mm; }}
.bar {{ display:grid; grid-template-columns:24mm 1fr 10mm; align-items:center; gap:2.5mm; margin-bottom:1.3mm; }}
.bl {{ font-family:'Plex Mono',monospace; font-size:7.4pt; color:#6b6e73; overflow:hidden;
  text-overflow:ellipsis; white-space:nowrap; }}
.btrack {{ position:relative; height:3.2mm; }}
.bb {{ position:absolute; left:0; top:0; height:100%; background:{INK}; opacity:.72; }}
.bn {{ font-family:'Plex Mono',monospace; font-size:7.4pt; text-align:right; }}
.ask {{ border:1pt solid {INK}; padding:3mm 3.6mm; margin-top:2.4mm; }}
.ask h4 {{ font-size:10.5pt; color:{INK}; margin-bottom:1.8mm; }}
.figwrap {{ text-align:center; margin:3mm 0; }}
.chart {{ display:block; margin:0 auto; max-width:100%; height:auto; }}
.grid3 {{ display:grid; grid-template-columns:repeat(3,1fr); gap:6mm 6mm; }}
.grid5 {{ display:grid; grid-template-columns:repeat(5,1fr); gap:4mm 4mm; }}
.entry figcaption {{ margin-top:1.2mm; line-height:1.3; }}
.entry.big figcaption {{ font-size:7.8pt; }}
.entry.sm figcaption {{ font-size:6.6pt; }}
.entry.sm .slug {{ font-size:6.2pt; }} .entry.sm .eco {{ font-size:6.2pt; }}
.entry .mv {{ font-size:6.6pt; color:#5c5f64; }}
.entry .attr {{ color:{NAMING}; font-size:7.2pt; }}
.entry .prop {{ color:#8a8d92; font-size:7pt; font-style:italic; }}
.chip {{ font-family:'Plex Mono',monospace; font-size:5.8pt; color:{INK}; opacity:.55; }}
.ixcols {{ display:grid; grid-template-columns:1fr 1fr 1fr; gap:0 5mm; }}
.ixline {{ display:flex; justify-content:space-between; align-items:baseline; gap:1.5mm;
  font-size:6.9pt; line-height:1.55; border-bottom:.2pt dotted #ddd8ca; }}
.ixn {{ overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }}
.ixp {{ font-family:'Plex Mono',monospace; font-size:6.2pt; color:{INK}; opacity:.55; flex:none; }}
.entry .inh {{ display:block; font-size:6.8pt; color:#8b8e93; margin-top:.8mm; }}
.entry.sm .inh {{ font-size:6.1pt; }}
.entry .hist {{ display:block; font-size:7.2pt; line-height:1.42; color:#3c3f44;
  border-left:1.6pt solid {INK}; padding-left:2.2mm; margin-top:1.1mm; }}
.entry.sm .hist {{ font-size:6.4pt; }}
.chron td {{ padding:1.4mm 2mm; vertical-align:top; }}
.chron .yr {{ width:12mm; font-size:9pt; }}
.chron .gm2 {{ width:74mm; font-size:8.4pt; line-height:1.35; }}
.chron .ln2 {{ font-size:8.4pt; line-height:1.35; }}
.gathered {{ display:grid; grid-template-columns:repeat(5,1fr); gap:5mm 5mm; margin-top:4mm; }}
.gcell figcaption {{ margin-top:1.4mm; font-size:6.8pt; line-height:1.34; }}
.gcell .attr {{ color:{NAMING}; }}
.chcover {{ padding:0 18mm 16mm; }}
.pband {{ display:flex; height:6mm; margin:0 -18mm 6mm; border-top:.3pt solid {INK};
  border-bottom:.3pt solid {INK}; }}
.bandseg {{ border-right:.25pt solid {INK}; }}
.bandseg:last-child {{ border-right:none; }}
.bandseg.on {{ background:{BAND}; }}
.chead {{ display:flex; justify-content:space-between; font-family:'Plex Mono',monospace;
  font-size:6.5pt; text-transform:uppercase; letter-spacing:.14em; padding-bottom:1mm;
  border-bottom:.25pt solid {INK}; }}
.chead span:last-child {{ color:{INK}; opacity:.5; }}
.csup {{ font-family:'Plex Mono',monospace; font-size:6.5pt; text-transform:uppercase;
  letter-spacing:.14em; color:{INK}; opacity:.5; margin-top:2.4mm; }}
.ctitle {{ font-family:'OCN DIN',Spectral,serif; font-size:40pt; line-height:1.02;
  letter-spacing:.005em; margin:.8mm 0 1.4mm; }}
.cmoves {{ font-size:8.4pt; }}
.cmid {{ display:grid; grid-template-columns:1fr 84mm; gap:6mm; margin-top:5mm; }}
.plate {{ display:block; width:84mm; height:auto; }}
.pcap {{ font-family:'Plex Mono',monospace; font-size:6pt; color:#5c5f64; margin-top:1.4mm; }}
.census {{ display:grid; grid-template-columns:1fr 1fr; gap:5mm; }}
.cl {{ font-family:'Plex Mono',monospace; font-size:6.2pt; text-transform:uppercase;
  letter-spacing:.12em; color:{INK}; }}
.cv {{ font-family:'OCN DIN',Spectral,serif; font-size:17pt; line-height:1.1; }}
.cv.big {{ font-size:44pt; line-height:1; }}
.crule {{ border-bottom:.25pt solid #cfcabb; margin:1.2mm 0 2.2mm; }}
.crule.gold {{ border-bottom:.5pt solid {INK}; opacity:.35; }}
.fgame {{ font-size:8.4pt; line-height:1.4; margin-top:1mm; }}
.cfield {{ margin-top:5mm; border-top:.25pt solid {INK}; padding-top:1.6mm; }}
.cflabel {{ font-family:'Plex Mono',monospace; font-size:6.2pt; text-transform:uppercase;
  letter-spacing:.1em; color:{INK}; opacity:.5; margin-bottom:2mm; }}
.csig {{ position:absolute; left:18mm; right:18mm; bottom:26mm; border-top:.6pt solid {INK};
  padding-top:2.4mm; display:grid; grid-template-columns:54mm 1fr; gap:6mm; align-items:start; }}
.csn {{ font-family:'OCN DIN',Spectral,serif; font-size:28pt; line-height:1; color:{INK}; }}
.cst {{ font-size:10.5pt; line-height:1.45; }}
.lt {{ font-size:7.2pt; }}
.lt.two-col {{ column-count:2; column-gap:7mm; }}
.ltrow {{ display:flex; align-items:center; gap:1.6mm; break-inside:avoid; padding:.15mm 0; }}
.tick {{ width:1.8mm; height:1.8mm; background:{BAND}; flex:none; }}
.tickx {{ width:1.8mm; height:1.8mm; flex:none; }}
.ltn {{ flex:1; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }}
.ltb {{ width:22mm; height:1.1mm; background:#e6e1d4; flex:none; }}
.ltb span {{ display:block; height:100%; background:{INK}; opacity:.72; }}
.ltg {{ font-family:'Plex Mono',monospace; font-size:6.4pt; width:12mm; text-align:right; color:#6b6e73; }}
.dossier {{ display:grid; grid-template-columns:1fr 1fr; gap:7mm; }}
.dname {{ font-family:'OCN DIN',Spectral,serif; font-size:14pt; margin:.6mm 0 1.4mm; }}
.dq {{ font-size:9.2pt; line-height:1.45; }}
.dhero {{ font-family:'OCN DIN',Spectral,serif; font-size:26pt; line-height:1; margin:.6mm 0 .6mm; }}
.split {{ display:flex; height:4mm; margin:1.8mm 0 1mm; border:.3pt solid {INK}; }}
.split.empty {{ background:{PAPER}; }}
.sw {{ background:{INK}; }} .sd {{ background:{INK}; opacity:.34; }} .sb {{ background:{PAPER}; }}
.tocline {{ display:flex; align-items:baseline; gap:2mm; font-size:9pt; padding:.5mm 0; }}
.tt {{ white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }}
.td {{ flex:1; border-bottom:.4pt dotted #b9b2a2; transform:translateY(-1mm); }}
.tp {{ font-family:'Plex Mono',monospace; font-size:8pt; color:{INK}; opacity:.55; }}
.chopen {{ display:grid; grid-template-columns:46mm 1fr; gap:6mm; margin-bottom:4mm;
  padding-bottom:4mm; border-bottom:1pt solid {INK}; }}
.chb .board {{ width:46mm; }}
.chn {{ font-family:'OCN DIN',Spectral,serif; font-size:17pt; letter-spacing:.03em; margin-bottom:1mm; }}
.fentry {{ display:grid; grid-template-columns:34mm 1fr; gap:4mm; margin-bottom:4.5mm;
  padding-bottom:3.5mm; border-bottom:.4pt solid #ddd8ca; break-inside:avoid; }}
.fentry:last-child {{ border-bottom:none; }}
.fb .board {{ width:34mm; }}
.fh {{ display:flex; gap:3mm; align-items:baseline; }}
.fn {{ font-family:'OCN DIN',Spectral,serif; font-size:12pt; letter-spacing:.03em; margin:.6mm 0 1mm; }}
.fm {{ font-size:7.2pt; color:#5c5f64; margin-bottom:1.2mm; }}
.fs {{ font-size:7.6pt; line-height:1.5; }}
.fs .attr {{ color:{NAMING}; }}
.fs .note {{ color:#3c3f44; }}
.fs .first {{ color:{INK}; }}
.fs .alias {{ color:#6b6e73; font-style:italic; }}
.flag {{ font-family:'Plex Mono',monospace; font-size:6pt; letter-spacing:.06em;
  text-transform:uppercase; color:{INK}; opacity:.6; border:.4pt solid #ccc8bd; padding:0 1mm; border-radius:1mm; }}
.flag.basis {{ color:#5c5f64; border-color:#ddd8ca; }}
.fs .prop {{ color:#7c7f84; font-style:italic; }}
.fs .xref {{ color:#8a8d92; font-family:'Plex Mono',monospace; font-size:6.8pt; }}
.kids {{ margin-top:1.6mm; display:flex; align-items:center; gap:2mm; }}
.kh {{ font-family:'Plex Mono',monospace; font-size:6.4pt; color:{INK}; opacity:.55; white-space:nowrap; }}
.kflow {{ width:52mm; height:3.4mm; }}
.gm {{ margin-top:1.4mm; display:grid; grid-template-columns:11mm 1fr; gap:2mm; }}
.gh {{ font-family:'Plex Mono',monospace; font-size:6.4pt; color:{INK}; opacity:.55; text-transform:uppercase; }}
.gg {{ font-size:6.9pt; line-height:1.42; }}
.wg {{ color:{INK}; display:block; }}
.wg::before {{ content:"WCh"; font-family:'Plex Mono',monospace; font-size:5.6pt;
  color:{NAMING}; letter-spacing:.04em; border:.4pt solid {NAMING}; padding:0 .7mm;
  margin-right:1.4mm; vertical-align:.7pt; }}
.ng {{ color:#5c5f64; display:block; }}
.ng::before {{ content:"top"; font-family:'Plex Mono',monospace; font-size:5.6pt;
  color:#8b8e93; letter-spacing:.04em; border:.4pt solid #c9ccd1; padding:0 .7mm;
  margin-right:1.4mm; vertical-align:.7pt; }}
.gid {{ font-family:'Plex Mono',monospace; font-size:6pt; color:#a8a294; }}
.gmore {{ color:#a8a294; font-style:italic; }}
.kn {{ font-family:'Plex Mono',monospace; font-size:6.2pt; color:#8a8d92;
  overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }}
"""

# ---------------- contents, two-pass ----------------
FRONT_TITLES = {
    "What this volume found", "Everything we hold, through one opening", "The name", "The shape of it",
    "The naming tree, entire", "Which lines are most played",
    "Which lines are most contested", "The world championship record",
    "The people, and what is proved about them", "Proposed, and deliberately not applied",
    "A legend, and its sources", "Places, and the names that move",
    "What the catalogue knows about a name", "Club play against master play",
    "How long a name stays in play",
    "The living edge",
    "Dated in print", "What the shelf does not index", "The chapters",
    "What we cannot answer", "The data, and how to take it",
}

def build_contents(offset):
    front, chron_first, chaps = [], None, []
    for title, folio, idx in SECTIONS:
        n = idx + 2 + offset
        if title in FRONT_TITLES:
            front.append((title, n))
        elif folio == "Chronology" and chron_first is None:
            chron_first = n
        elif folio.startswith("Chapter") and title.startswith("Chapter") and " (" not in title:
            if not chaps or chaps[-1][0] != title:
                chaps.append((title, n))
    rows_f = "".join(f'<div class="tocline"><span class="tt">{t}</span>'
                     f'<span class="td"></span><span class="tp">{n}</span></div>'
                     for t, n in front)
    rows_c = "".join(f'<div class="tocline"><span class="tt">{t}</span>'
                     f'<span class="td"></span><span class="tp">{n}</span></div>'
                     for t, n in chaps)
    p1 = (f'<section class="page"><h2>Contents</h2>'
          f'<h3>The opening, and what is recorded about it</h3>{rows_f}'
          f'<h3>Chronology</h3><div class="tocline"><span class="tt">By first recorded '
          f'game, {chron[0][0]} to {chron[-1][0]}</span><span class="td"></span>'
          f'<span class="tp">{chron_first}</span></div>'
          f'<div class="folio"><span>Contents</span><span class="pn"></span></div></section>')
    half = (len(chaps) + 1) // 2
    rows_c1 = "".join(f'<div class="tocline"><span class="tt">{t}</span>'
                      f'<span class="td"></span><span class="tp">{n}</span></div>'
                      for t, n in chaps[:half])
    rows_c2 = "".join(f'<div class="tocline"><span class="tt">{t}</span>'
                      f'<span class="td"></span><span class="tp">{n}</span></div>'
                      for t, n in chaps[half:])
    p2 = (f'<section class="page"><h2>Contents, the chapters</h2>'
          f'<p class="small">One chapter for each line that branches directly from 3.Bb5, '
          f'ordered by how many names hang beneath it.</p>'
          f'<div class="two"><div>{rows_c1}</div><div>{rows_c2}</div></div>'
          f'<div class="folio"><span>Contents</span><span class="pn"></span></div></section>')
    return [p1, p2]

# ---------------- the indexes
# A page number is the section's index in PAGES plus the cover plus the two
# contents pages, which is the same arithmetic build_contents does.
def _pageno(idx):
    return idx + 4


def _pg(slug):
    i = SLUG_PAGE.get(slug)
    return _pageno(i) if i is not None else None


def _sortkey(slug):
    n = CATALOG[slug]["canonical_name"]
    n = re.sub(r"^Ruy L[oó]pez[ ,]*", "", n).strip()
    return (n or "Ruy López").lower()


_named = sorted((s for s in RYL if _pg(s)), key=_sortkey)
_PER_IDX = 165
_idx_pages = [_named[i:i + _PER_IDX] for i in range(0, len(_named), _PER_IDX)]

for _n, _chunk in enumerate(_idx_pages, 1):
    _third = -(-len(_chunk) // 3)
    _cols = [_chunk[i:i + _third] for i in range(0, len(_chunk), _third)]
    _colhtml = "".join(
        "<div>" + "".join(
            f'<div class="ixline"><span class="ixn">'
            f'{re.sub(r"^Ruy L[oó]pez[ ,]*", "", CATALOG[s]["canonical_name"]) or "Ruy López"}'
            f'</span><span class="ixp">{_pg(s)}</span></div>' for s in col) + "</div>"
        for col in _cols)
    _intro = ('<p class="small">Every named line, alphabetically by the part of its name '
              'that is its own, with the page its entry is on. A name that begins with '
              'the opening\'s own name is filed under what follows it, because filing 328 '
              'lines under R would be filing nothing. One name appears twice: <b>Open, '
              'Classical Defence</b> is carried by two different positions, which is a '
              'collision in the catalogue rather than in this index, and both are '
              'listed.</p>') if _n == 1 else ""
    add(f"Index of names" + (f" ({_n} of {len(_idx_pages)})" if len(_idx_pages) > 1 else ""),
        f'{_intro}<div class="ixcols">{_colhtml}</div>', "Index")

# --- people
_by_person = {}
for _s in ATTRIBUTED:
    _who = RYL[_s]["attributed_to"]
    _by_person.setdefault(re.sub(r"\s*\([^)]*\)\s*$", "", _who).strip(),
                          ["sourced", []])[1].append(_s)
for _c in PROPOSED:
    _pid = _c["subject_id"]
    _nm = (PROP_PEOPLE.get(_pid) or PEOPLE.get(_pid) or {}).get("display_name",
                                                               _pid.replace("-", " ").title())
    _by_person.setdefault(_nm, ["proposed", []])[1].append(_c["ocn1"])

_prows = "".join(
    f'<tr><td>{nm}</td><td class="mono small">{state}</td><td class="small">'
    + "; ".join(f'{short(s)}&nbsp;<span class="ixp">{_pg(s) or "—"}</span>'
                for s in sorted(set(ls), key=_sortkey)) + '</td></tr>'
    for nm, (state, ls) in sorted(_by_person.items()))

add("Index of people", f"""
<p class="small">Everybody the catalogue names in connection with one of these lines,
with the lines and their pages. <b>Sourced</b> means a source establishes the person and
what they did. <b>Proposed</b> means the evidence establishes an eponym and not a role,
so the claim is held back; those {len(PROPOSED)} are printed in the volume as proposals
and are not part of the catalogue.</p>
<table class="kv"><tr><td>person</td><td class="mono">status</td><td>lines</td></tr>
{_prows}</table>
""", "Index")

# --- places
_by_place = {}
for _c in PLACES:
    _by_place.setdefault(_c["subject_id"].replace("-", " ").title(), []).append(_c["ocn1"])
_qrows = "".join(
    f'<tr><td>{pl}</td><td class="small">'
    + "; ".join(f'{short(s)}&nbsp;<span class="ixp">{_pg(s) or "—"}</span>'
                for s in sorted(set(ls), key=_sortkey)) + '</td></tr>'
    for pl, ls in sorted(_by_place.items()))

add("Index of places", f"""
<p class="small">The {len(_by_place)} places whose names ended up on a line of this
opening, each with the lines that carry them. Every one of these is a graded claim in the
catalogue's chronicle, not an inference from the name.</p>
<table class="kv"><tr><td>place</td><td>lines</td></tr>{_qrows}</table>
<p class="small">A place on this list is not a claim that the line was invented there.
It is a claim that the name refers to the place, which is a smaller and more defensible
thing, and it is the distinction the chronicle exists to keep.</p>
""", "Index")

TOC = build_contents(0)
TOC = build_contents(len(TOC))
PAGES = TOC + PAGES

HTML = (f'<!doctype html><html lang="en"><head><meta charset="utf-8">'
        f'<title>OCN Monograph C — The Ruy López, complete volume</title>'
        f'<style>{CSS}</style></head><body>{DEFS}{COVER}{"".join(PAGES)}</body></html>')

out = HERE / "ruy-book.html"
out.write_text(HTML)
print(f"html: {out} ({len(HTML)/1024/1024:.1f} MB), pages: {len(PAGES)+1}")
print(f"{len(CHAPTERS)} chapters, {len(FULL)} entries, {len(chron)} dated lines")
