# Handoff, 2026-08-03 evening to 2026-08-05

**Everything below is pushed and CI is green.** Working tree clean apart from
an untracked `tree-expanded.png` that predates this run. Twenty commits,
`149cdf3` to `996c27c`.

Read this before starting anything new. The open decisions are at the bottom
and four of them are one-line answers that unblock real work.

## What this was

It began as a showcase monograph on the Ruy López for chessgames.com. It
turned into an audit. **Rendering the catalogue is what found the defects** —
none of them came from reading the data, and most had been sitting there
through several passes that looked directly at the same rows.

## What was wrong, and is now fixed

**A wrong attribution, and the two proposals it had spawned.** `C.RyL.Mor.Wor`
is the Wormald Attack (5.Qe2) and carried an attribution to Thomas Herbert
Worrall, sourced to an Oxford Companion entry that describes 6.Qe2, a
different line. Matched on the three letters the two identifiers share.
Retracted rather than moved, because the Companion establishes an eponym and
not a role. The same substring error had also produced a `named-after-person`
proposal and a person record, both corrected. Robert B. Wormald now has a
record (Q16597044); the identity was already in the repository, filed as a
*warning* while resolving Worrall.

**Seven games that were not world-championship games.** Two Spanish amateurs
filed into Steinitz–Zukertort 1886, three into Alekhine–Capablanca 1927, a
`Botvinnik, Alexander v Al Tal, Ammar` into Botvinnik–Tal 1961, and a
different Koneru into Hou Yifan's 2011 defence. Every one pulled in because a
surname matched.

**Thirteen misspelled participants over 334 rows**, including a women's world
championship challenger recorded under a man's forename. Found by a test that
needs no outside knowledge: a title match is two players, so inside one event
the participant pair must be constant. **Three of the ten rows that test
flagged turned out to be the correct ones** — flagged because the majority
spelling in their event was wrong. A modal vote is a consistency check, not a
truth procedure.

**221 player-name defects in `popularity.tsv`**, 998 distinct names down to
889. Deliberately left alone: 31 surnames that genuinely carry two given
names, and every form ending in a database disambiguator (`Fedoseev,
Vladimir2`), because that digit marks a specific person.

**A citation field leaking player names into the place column.** Events read
"Steinitz - Zukertort World Championship Match, **Johannes**". The citation
begins `{white}-{black}` and both names carry a comma.

**Four artefacts contradicting each other about Modern/Robatsch.** `B.Mod`
(1.e4 g6, 96 lines beneath it) never said "Robatsch"; the alias sat on
`A.Mod`; the person record said Robatsch is the eponym of the Modern Defence;
and the one sourced sentence about him was filed in a dry-run report.

**The volume printed raw UCI.** Every move list in 222 pages read
`1.e2e4 e7e5 2.g1f3` — the storage format. `web/build.py` had the converter
all along. Now algebraic, and then figurine, because algebraic is not
language-independent either.

**The PDF embedded fonts from this laptop.** Georgia and Helvetica, because
`u_DIN` has 266 glyphs and Spectral shipped as the Google Fonts *latin*
subset. The catalogue needs exactly four characters beyond Latin-1: `ć č ė ř`.

## What was built

| | |
|---|---|
| `tools/build_monograph.py` | the generator, moved out of a scratch directory. No dependency outside this repository; the identity system's two drawings are snapshotted into `web/brand/` |
| `tools/measure_monograph_heights.py` | entry heights measured in Chrome. **Re-run whenever an entry's anatomy changes** — estimating has failed twice |
| `tools/apply_sidecar_manifest.py` | the batch engine the chronicle sidecars never had. 30 tests, all about refusing |
| `tools/set_pdf_boxes.py` | writes TrimBox and BleedBox so a press knows where to cut |
| `tools/subset_fonts.py` | rebuilds `web/fonts` from upstream with Latin Extended-A |
| `known-as`, `attested-in-print` | two relations added to the closed set, with their justification |

## The volume

221 A4 pages, zero overflow, ten embedded faces and none from the machine that
built it. `--bleed` produces a 226 × 313 mm print edition with crop marks.

**Colour has one rule now:** gold marks a line that carries documentary
evidence, and nothing else. It had been doing eight jobs — family identity,
board squares, bar length, treemap share, the draw segment, "still played",
and three kinds of rule — which is the same as doing none. Anything added
follows that rule or argues with it in writing.

## Open decisions — the four that are cheap

1. **Should the diacritic rule bind `canonical_name` only?** 28 `Lopez` and
   two `Moeller` aliases are parked because the validator applies it to
   `aliases` too. But an alias exists to be *searched for*, which is why the
   column already holds `Modern Defense`. Forbidding `Ruy Lopez` there means
   the catalogue cannot be found by the spelling nearly every database and
   search box uses. Recommendation: narrow it.
   `docs/evidence/provenance/lichess-alias-import.md`.
2. **`build_chronicle.py` should merge, not overwrite.** It regenerates
   `events.tsv` wholesale and keeps only the two match kinds, so a publication
   event cannot survive. This blocks the two `analysed-in` claims for the
   Göttingen manuscript and Segura's book, and it is why `claims.tsv` is
   spliced by hand.
3. **192 `named-after-person` conversions** have been verified and waiting for
   days.
4. **The chessgames.com letter** is drafted at
   `~/Downloads/2026-08-02-chessgames-permission-email.md` and unsent. The
   README now says what we want and the explorer serves the evidence, so it is
   no longer a promise.

## The project, as against the tasks

**1,989 of 5,899 rows carry no alternative name.** Down from 2,144 — the 155
that Lichess had already given us by exact position are in. The rest has no
rule: the 1,738 prefix matches name a *shallower* line and importing them
would give dozens of rows one alias that identifies nothing.

The README now asks for it directly, and a translated name turns out to be the
same shape as a tradition name — `known-as` with a source — which folds i18n
into naming rather than running it alongside. The `ca`/`es` sidecars hold 58
rows of 5,899 and are a dead end in their current form.

## Two habits worth keeping

**The repository's guards were right every time they refused something.** The
diacritic validator, the alias registrar, the manifest engine's row counts,
CI's Python 3.10 floor. Four separate refusals in two days, no false alarms.

**Verify by rendering, not by reading.** Every defect above was invisible in
the data and obvious on the page.

## One thing I got wrong and had to fix

`7a598dc` described 155 alias changes and contained none of them: the staging
command named a `python/` directory that does not exist, git refused the whole
invocation, and `2>/dev/null` swallowed it. For a while the deployed explorer
served aliases the repository did not have. Fixed in `2c5070f`, not amended,
because a commit that lied is worth leaving visible next to the one that says
so.
