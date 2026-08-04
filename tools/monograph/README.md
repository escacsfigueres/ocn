# Monograph inputs

`tools/build_monograph.py` writes its HTML here, and reads two cached inputs
that are expensive to rebuild.

| file | what it is | how to rebuild |
|---|---|---|
| `game-tags.tsv` | Event, Site, Date and Round for the 12,085 games in the notable-games proposal, fetched from the Lichess bulk export in batches of 300 | `python3 tools/fetch_lichess_tags.py` |
| `heights.json` | the height in pixels of every catalogue entry, measured in Chrome | `python3 tools/measure_monograph_heights.py` |

**Re-measure the heights whenever the anatomy of an entry changes.** The packer
decides which entries share a page before it renders them, so a stale cache
either overflows pages or wastes a quarter of each one. Estimating instead of
measuring has failed twice, once by 12mm per entry.

The generated `ruy-book.html` and `heights-probe.html` are gitignored. To make
the PDF:

```
python3 tools/build_monograph.py
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu --no-pdf-header-footer \
  --print-to-pdf=ruy-lopez.pdf --virtual-time-budget=120000 \
  "file://$PWD/tools/monograph/ruy-book.html"
```

## What it depends on outside this repository

Nothing, by design. The OCN identity is generated in the separate
`ocn-logo-system` workspace, and what the monograph needs from it — two
drawings and the display face — is snapshotted into `web/brand/` and
`web/fonts/`. To refresh the drawings, re-run `lockup_horizontal_svg()` and
`micro_svg("c")` there and overwrite the SVGs. The lockup is rendered with no
family argument on purpose: its band stays ink so it does not compete with the
gold band and the giant C already on the cover.
