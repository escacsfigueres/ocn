# Editorial curation of games: what is available and what is closed

**Status: assessment.** Which routes can give OCN "the notable games for
this opening" — the editorial judgement, not just the rating list.

## chessgames.com is closed, explicitly

Their `robots.txt` disallows precisely the endpoints that would serve
this purpose:

    Disallow: /pgn/                Disallow: /perl/explorer
    Disallow: /perl/pgndownload    Disallow: /perl/lookupfen
    Disallow: /fen/                Disallow: /perl/lookupmoves
    Disallow: /perl/nph-chesspgn   Disallow: /perl/chess.pl

PGN download, the opening explorer, and position lookup — all barred.
The file also lists `/spidertrap.html`, which is an active defence
rather than a passive preference.

This is not a grey area and it is not about copyright: it is the site
stating, in the standard machine-readable place, that automated access
to exactly this data is not wanted. **OCN does not scrape it.** Reading
a page as a human to check a fact remains ordinary research; harvesting
does not.

## Three routes that are open

### 1. World championship games, already derived

Joining `docs/evidence/provenance/notable-games.tsv` against
`catalog/ocn-1.wch.tsv` by player pair and year identifies **359 games
across 271 openings** that were played in a world championship match,
each with a permanent `lichess.org` URL.

"Played in a world championship" is editorial significance of the
highest order and it costs nothing: both datasets are ours, the join is
reproducible, and no third party is involved. The Sveshnikov rows come
back as Caruana–Carlsen 2018; the Trompowsky as Carlsen–Karjakin 2016.

This is the strongest of the three and it is already sitting there.

### 2. Wikipedia's illustrative games

Opening articles frequently name the game that made a line famous, and
Wikipedia is CC BY-SA — reusable with attribution, unlike a proprietary
collection. The parser in `tools/parse_eponym_lists.py` already reads
these articles for eponyms; extracting their named games is the same
shape of work.

### 3. The Oxford Companion's printed games

The Companion prints illustrative games inside entries — the Staunton
Gambit entry carries Tartakower–Mieses, Baden-Baden 1925 in full. These
are reference-grade selections by named editors, citable by entry and
page, and the book is already loaded as a NotebookLM source.

## What none of them give

A ranking of *quality*. All three answer "which games are historically
significant here", and none answers "which games are best". OCN should
not pretend otherwise: significance is recordable, merit is an opinion.
