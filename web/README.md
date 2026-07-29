# OCN web explorer

The static explorer for the OCN-1 catalogue (roadmap
[H2.3](../docs/traction-roadmap.md)). Four files in, one directory out:
no framework, no bundler, no backend, no request to any third-party host
at runtime.

```
web/
  build.py        generates dist/ (stdlib only)
  index.html      the shell: header, mount point, footer
  app.js          one ES module: data load, search, tree, board, router
  style.css       one stylesheet: light and dark from one token block
  dist/           generated, gitignored, never committed
```

## Build

```bash
python3 web/build.py
```

Writes `web/dist/`: the three static assets copied verbatim plus
`dist/data/ocn.json`, the display payload built from `catalog/ocn-1.csv`
and `catalog/ocn-1.lichess-xref.tsv`. About seven seconds, deterministic
(two builds of the same catalogue are byte-identical).

Useful flags: `--out DIR`, `--pretty` (indent the payload),
`--version ocn-1.2.0` (otherwise the most recent git tag),
`--catalog` / `--xref` to point at other inputs.

## Serve locally

```bash
python3 -m http.server -d web/dist 8000
```

Then open <http://localhost:8000/>. It must be served over HTTP, not
opened as a `file://` path: `app.js` is an ES module and it fetches the
payload, and both are blocked on the file scheme.

## Deploy

**Deployment is gated.** The repository is private and the Vercel project
belongs to the `escacsfigueres` team, so publishing this directory is the
owner's call, made once under an explicit GO (roadmap H0.8 flips the
repository public; H2.3 ships the explorer). Nothing in this directory
runs a deploy, and no CI job publishes it. When the GO comes, the deploy
is `vercel-escacs --prod` with `web/dist` as the output directory and
`python3 web/build.py` as the build command — never plain `vercel`, per
the account rules in the root `CLAUDE.md`.

## The payload

`dist/data/ocn.json`, schema `ocn.web.v1`, about 2.3 MB (330 KB over the
wire once the host applies gzip):

```json
{
  "schema": "ocn.web.v1",
  "catalog_version": "ocn-1.2.0",
  "generated_note": "display projection of catalog/ocn-1.csv: ...",
  "rows": [ { "slug": "B.Sic.Naj.Eng", "...": "..." } ]
}
```

One object per catalogue row, in catalogue order. **Empty fields are
omitted** rather than emitted as `""` or `[]` — 26 rows carry an
attribution and 112 a transposition, so writing the blanks would cost
more than the data.

| Field | Always | Meaning |
|---|---|---|
| `slug` | yes | `ocn1`, the primary key |
| `name` | yes | `canonical_name` |
| `depth` | yes | integer, equals the dot count |
| `fen` | yes | complete FEN of the position, derived at build time |
| `parent` | no | `parent_ocn1`; absent on the five class roots |
| `san` | no | numbered SAN movetext (`1.e4 c5 2.Nf3`); absent on the roots |
| `eco` | no | `eco_legacy` split on `\|` |
| `aliases` | no | real aliases only, see below |
| `flags` | no | `flags` split on `\|` |
| `transposes_to` | no | slug this row canonicalises to |
| `same_as` | no | co-canonical slugs |
| `attributed_to`, `attribution_source`, `historical_notes` | no | the attribution block, together or not at all |
| `lichess` | no | `{name, eco, kind}` from the xref; `kind` is `exact` or `prefix` |

### Three display decisions

The payload is a projection, not a second catalogue. `catalog/ocn-1.csv`
stays canonical and nothing here writes to it.

1. **`notes` is dropped entirely.** The July 2026 audit measured ~49% of
   that column as template boilerplate; `B.Sic.Naj.Eng` has the note
   `6.Be3.` under a movetext that already ends in 6.Be3. Publishing it
   would make every row page look padded for no reader's gain.
2. **Synthetic aliases are dropped**: a bare `Main Line` (398 rows) and
   the `<SAN> Line` shape — `Nf6 Line`, `O-O Line`, `Bxf6 Line` (about
   1,730 rows). These are exactly the strings roadmap H2.6 deletes from
   the catalogue; the explorer must not display them in the meantime.
   The filter matches that lot and no more: `Castled Line` and
   `Fianchetto Line` read synthetic but are not in it, so they survive.
   Real aliases are untouched — `B.Sic.Sve` still shows Lasker-Pelikán
   and Cheliabinsk.
3. **Every row gains `fen`**, replayed from `moves_uci` through
   `tools/export_positions.py`, so the board never replays moves in the
   browser. The five class roots are filters rather than positions and
   get the standard initial position.

`moves_uci` and `eco_legacy` are left out: `san`, `fen` and `eco` cover
every display and link the pages make.

## What the pages do

Three hash routes, so the whole site is one HTML file:

| Route | View |
|---|---|
| `#/` | search box, the A-E tree, the ECO converter |
| `#/B.Sic.Naj.Eng` | one row: breadcrumb, board, moves, ECO, Lichess label, relations, sub-lines |
| `#/eco/B90` | the converter, pre-filled and shareable |

Search is a scored linear scan over pre-folded strings built once at
load. It answers in single-digit milliseconds on all 5,899 rows, so
there is no inverted index and no debounce. The fold matches the Python
package's (`ocn.catalog._fold`: NFKD, casefold, drop combining marks)
and adds the punctuation flattening a search box needs: `king's indian`,
`kings indian` and the curly-quoted `king’s indian` an iPhone produces
all reach the same rows, and a query in the German transliteration
(`gruenfeld`) falls back to the native spelling the catalogue uses.

The board is generated SVG: 64 rects and one `<text>` per piece using
the solid Unicode chess glyphs, painted twice (light fill with a dark
stroke for White, the inverse for Black). No image, no web font, no
board library.

## Constraints this directory keeps

- **No external request.** Every `src` and `href` in the shipped markup
  is local. The only absolute URLs the module builds are the per-row
  Lichess analysis deep link and the repository link in the footer.
  `tools/tests/test_web_build.py` fails if a third one appears.
- **No middle dot.** `U+00B7` as a separator is banned project-wide; the
  build refuses to write an asset containing one.
- **Light and dark.** One token block, flipped by
  `prefers-color-scheme`; the board keeps its own square colours so it
  stays a chessboard in both.
- **Mobile.** The tree collapses, the board scales, the breadcrumb drops
  its subtitles below 520px, and no page scrolls horizontally at 390px.

## Tests

```bash
python3 -m unittest tools.tests.test_web_build
```

Builds the site into a temporary directory and checks the payload
(5,899 rows, a known FEN, notes gone, synthetic aliases gone from the B
rows, real aliases kept, every parent and relation target resolving,
size under the roadmap's cap) and the no-external-request guarantee
across `index.html`, `app.js` and `style.css`.

## Design tokens, and the audit behind them

Everything visual comes from the token block at the top of `style.css`.
The values are not taste; three of them were measured and moved.

**Colour.** Contrast was computed against the page background rather
than eyeballed. Three tokens failed and were corrected:

| token | was | now | on paper |
|---|---|---|---|
| `--ink-3` (labels, counts, captions) | `#838a90` | `#6b7178` | 3.2:1 to 4.6:1, clears AA for small text |
| `--cls-c` (the amber volume) | `#a4791b` | `#8a6512` | 3.6:1 to 4.9:1 |
| control boundaries | `--rule-2` at 1.5:1 | `--edge` at 3.1:1 | WCAG 1.4.11 wants 3:1 for the edge of a control |

`--rule` stays a hairline at 1.2:1 on purpose: a decorative separator is
exempt, and darkening it would turn a quiet page into a grid.

**Type.** Seven steps, `--t-micro` through `--t-display`, and no strays.
The ten ad-hoc sizes that preceded them included four within a pixel of
each other, which is noise rather than hierarchy.

**Space.** A four-pixel grid, `--s0` through `--s8`. Twenty-eight
lengths were snapped onto it; optical values (a chip's inner padding, an
underline offset) stay off-grid deliberately, because they answer to the
glyph rather than to the layout.

**Motion.** Two durations and one curve: `--dur-1` for a control,
`--dur-2` for a panel, and a decelerating cubic rather than `ease`,
which starts too fast to read as deliberate. Anything that moves
together uses the same pair — the tree's arrow and its drawer open on
one gesture, because an arrow that animates beside content that snaps is
what makes a disclosure feel broken.
