# Attribution draft proposals — UN-APPLIED, GO-pending

**Status: DRAFTS ONLY. Nothing here is applied. No catalogue change, no
`--apply`, no commit.** These are reviewable `ocn.attribution_manifest.v1`
proposals produced by a read-only drafting pass. They are deliberately **not**
wired into any test and **not** placed in `docs/manifests/` (the live dir). Each
must clear human review under an explicit GO before any apply.

The CSV (`catalog/ocn-1.csv`) was verified byte-for-byte unchanged after every
dry-run (`git diff --stat catalog/ocn-1.csv` empty).

## What's here

| File | Lot | Slugs | Grade | Dry-run |
|---|---|---|---|---|
| `french-winawer.manifest.json` | Winawer (existing proposal) | `B.Fre.Win` | **CLEAR** | clean, 1 row changed |
| `web-sourced-safe-heads.manifest.json` | factory-map Lots 1/5/9 (head-only) | `B.Fre.Mac`, `B.Fre.Bur`, `C.KGm.Acc.All`, `C.Sco.Gor` | **PARTIAL** | clean, 4 rows changed |

All `mode = attribution_fields_only` (only `attributed_to` /
`attribution_source` / `historical_notes` may change). All **head rows only** —
no child rows. Each target head was confirmed to exist and to have all three
attribution fields empty before drafting.

## Evidence grades — honest

- **CLEAR** is used **only** for Winawer, and only because a **reference-grade**
  source already exists and was nlm-verified: *The Center Game* ("(3.Nc3 Bb4)
  named after him"), recorded in
  [`../parked-attribution-reference-source-log.md`](../parked-attribution-reference-source-log.md).
  Even so it is **not** unconditionally apply-ready: the exact **author/year of
  *The Center Game* must be pinned** first (do not conflate with Mario Ziegler,
  cited for a different book in the same source paragraph), plus an explicit GO.
- **PARTIAL** is used for every web-only head. A Wikipedia/web source is **not**
  reference-grade. Each PARTIAL row is marked **"needs reference-grade pin
  before apply"** (Oxford Companion entry / monograph). The engine's `--strict`
  mode **rejects** these (verified: it errors on the first PARTIAL), so they
  physically cannot ride a strict apply until upgraded to CLEAR.

## Sources (first-hand, fetched this run — URL + exact quote)

### CLEAR

- **`B.Fre.Win` Winawer** — *The Center Game* (NotebookLM Q25, src `a433382e`),
  verified in `../parked-attribution-reference-source-log.md`:
  > "(3.Nc3 Bb4) **named after him**" (Szymon Winawer, 1838–1919).

  Corroborating: Wikipedia *French Defence* / *Szymon Winawer*; Lumbra chronology
  (3...Bb4 from Paulsen 1861; Winawer's Paris 1867; Nimzowitsch 1921; Botvinnik
  1927).

### PARTIAL (web-only — needs reference-grade pin)

- **`B.Fre.Mac` McCutcheon** — Wikipedia, *French Defence*
  (<https://en.wikipedia.org/wiki/French_Defence>, fetched 2026-06-19):
  > "The McCutcheon Variation is **named for** John Lindsay McCutcheon of
  > Philadelphia (1857–1905), who brought the variation to public attention when
  > he used it to defeat World Champion Steinitz in a simultaneous exhibition in
  > Manhattan in 1885."

- **`B.Fre.Bur` Burn** — Wikipedia, *Amos Burn*
  (<https://en.wikipedia.org/wiki/Amos_Burn>, fetched 2026-06-19):
  > "Burn is the **eponym** of the Burn Variation of the French Defence (1.e4 e6
  > 2.d4 d5 3.Nc3 Nf6 4.Bg5 dxe4)." (Amos Burn, 1848–1925.)

  Corroborating: Wikipedia *French Defence*: "**Named after** Amos Burn, the Burn
  Variation is the most common reply at the top level."

- **`C.KGm.Acc.All` Allgaier** — Wikipedia, *Johann Baptist Allgaier*
  (<https://en.wikipedia.org/wiki/Johann_Baptist_Allgaier>, fetched 2026-06-19):
  > "…the variant of the King's Gambit **named after him** (1.e4 e5 2.f4 exf4
  > 3.Nf3 g5 4.h4 g4 5.Ng5, the so-called Allgaier's Gambit) is a particularly
  > sharp opening." (Johann Baptist Allgaier, 1763–1823.)

- **`C.Sco.Gor` Göring** — Wikipedia, *Carl Göring*
  (<https://en.wikipedia.org/wiki/Carl_G%C3%B6ring>, fetched 2026-06-19):
  > "His **name is attached to** the Göring Gambit in the Scotch Game (1.e4 e5
  > 2.Nf3 Nc6 3.d4 exd4 4.c3)…" (Carl Theodor Göring, 1841–1879.)

  Corroborating: Wikipedia *Scotch Game*: "Carl Theodor Göring introduced it into
  master play in 1872" (first played at high level by Howard Staunton in the
  1840s).

## Dry-run results (captured)

Run from the worktree root; default `--dry-run`, **no `--apply`**, nothing written.

```
python3 tools/apply_attribution_manifest.py --manifest docs/drafts/french-winawer.manifest.json --dry-run
  -> rows 5899 -> 5899 ; rows changed: 1 (B.Fre.Win) ; exit 0 ; zero collateral
  -> --strict: PASSES (CLEAR)

python3 tools/apply_attribution_manifest.py --manifest docs/drafts/web-sourced-safe-heads.manifest.json --dry-run
  -> rows 5899 -> 5899 ; rows changed: 4 (B.Fre.Mac, B.Fre.Bur, C.KGm.Acc.All, C.Sco.Gor) ; exit 0 ; zero collateral
  -> --strict: REJECTED ("evidence_grade 'PARTIAL'; only 'CLEAR' may be applied") — expected, the grade gate working
```

The engine's exact-change contract passed for both (the actually-differing rows
equalled `expected_changed_rows`), so each manifest changes exactly its named
head row(s) and nothing else.

## Candidates SKIPPED this run (needs source)

- **`C.KGm.Acc.Kie` Kieseritzky** — Wikipedia gives only "popularized by Lionel
  Kieseritzky" and "Kieseritzky's name became associated with … the Kieseritzky
  Gambit" — a type-C (popularizer) / associative phrasing, **not** a clean
  "named after" attestation. Skipped to avoid over-reading. Needs a source that
  states the naming directly (OC entry / monograph) before drafting.
- **QGD heads `D.QGD.Lsk` (Lasker), `D.QGD.Rag` (Ragozin), `D.QGD.Har`
  (Harrwitz)** — not source-fetched this run. Heads exist and are empty, but no
  first-hand "named after" passage was obtained, so they are left for a future
  evidence pass. (`D.QGD.Har.Har` also has a known duplicated-`canonical_name`
  pre-existing issue, logged in the factory map — out of scope here.)
- **Sämisch heads `E.KID.Sml`, `E.Nim.Sml`, `E.Gru.Sml`** — not source-fetched
  this run; left for a future pass.

## What's needed before any apply

1. **Albert's explicit GO** (per the agentic-development playbook).
2. **Winawer:** pin the exact author/year of *The Center Game*.
3. **PARTIAL heads:** lift each to **CLEAR** with a reference-grade source
   (Oxford Companion entry or a monograph chapter) before they may pass
   `--strict --apply`. Until then they stay parked.

## See also

- [`attribution-drafts-record.md`](attribution-drafts-record.md) — per-slug summary table.
- [`../attribution-batch-engine.md`](../attribution-batch-engine.md) — the engine + guardrails.
- [`../whole-catalogue-attribution-factory-map.md`](../whole-catalogue-attribution-factory-map.md) — the lot map these drafts draw from.
- [`../french-winawer-attribution-proposal.md`](../french-winawer-attribution-proposal.md) — the standing Winawer proposal.
