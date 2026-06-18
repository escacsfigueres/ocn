# Attribution draft proposals — UN-APPLIED, GO-pending

**Status: DRAFTS ONLY. Nothing here is applied. No catalogue change, no
`--apply`, no commit.** These are reviewable `ocn.attribution_manifest.v1`
proposals produced by a read-only drafting pass. They are deliberately **not**
wired into any test and **not** placed in `docs/manifests/` (the live dir). Each
must clear human review under an explicit GO before any apply.

The CSV (`catalog/ocn-1.csv`) was verified byte-for-byte unchanged after every
dry-run (`git diff --stat catalog/ocn-1.csv` empty).

## What's here — clean CLEAR/PARTIAL split

| File | Slugs | Grade | Dry-run | `--strict` |
|---|---|---|---|---|
| `attribution-clear.manifest.json` | `C.KGm.Acc.All` (Allgaier) | **CLEAR** | clean, 1 row changed | **PASSES** |
| `attribution-partial.manifest.json` | `B.Fre.Win`, `B.Fre.Mac`, `B.Fre.Bur`, `C.Sco.Gor`, `C.KGm.Acc.Kie`, `D.QGD.Lsk`, `D.QGD.Rag`, `D.QGD.Har`, `E.KID.Sml`, `E.Nim.Sml` (10 heads) | **PARTIAL** | clean, 10 rows changed | **REJECTED** |

All `mode = attribution_fields_only` (only `attributed_to` /
`attribution_source` / `historical_notes` may change). All **head rows only** —
no child rows. Each target head was confirmed to exist and to have all three
attribution fields empty before drafting.

> **History:** this dir previously held `web-sourced-safe-heads.manifest.json`
> (4 PARTIAL heads) and `french-winawer.manifest.json` (Winawer, then graded
> CLEAR). Both were **deleted** and replaced by the CLEAR/PARTIAL split above,
> after the Winawer source was debunked (see correction below) and six more
> verified findings were added.

## Evidence grades — honest

OCN reserves **CLEAR** for a **reference-grade** BOOK / ENCYCLOPAEDIA source.
Web / Wikipedia / chess.com / chessable = **PARTIAL**.

- **CLEAR** is used for **only** `C.KGm.Acc.All` (Allgaier), and only because
  the source is reference-grade: **Hooper & Whyld, *The Oxford Companion to
  Chess*** (1st ed.), entry 'ALLGAIER GAMBIT'. It is `--strict`-passable and
  apply-ready **pending only an explicit GO**.
- **PARTIAL** is used for every web-only head (the other ten). A
  Wikipedia/web/chess.com source is **not** reference-grade. Each PARTIAL row is
  marked **"needs reference-grade pin before apply"** (Oxford Companion entry /
  monograph). The engine's `--strict` mode **rejects** the PARTIAL manifest (it
  errors on the first PARTIAL, `B.Fre.Win`), so these physically cannot ride a
  strict apply until upgraded to CLEAR.

## ⚠️ Winawer correction (prominent)

`B.Fre.Win` was previously graded **CLEAR** on a source titled *The Center
Game*. **That is debunked.** *The Center Game* is **Arne Moll's monograph about
the Center Game opening** (1.e4 e5 2.d4 exd4 3.Qxd4) — a **different** opening
— and the NotebookLM "(3.Nc3 Bb4) named after him" grounding was
**hallucinated**. **Do not cite *The Center Game*.** Winawer is now graded
**PARTIAL** on Wikipedia *French Defence* ("named after Szymon Winawer"). The
registry row in [`../attribution-source-status.tsv`](../attribution-source-status.tsv)
was downgraded CLEAR → PARTIAL to match. (Note: the same eponym also names the
Winawer Countergambit in the Slav, catalogue `D.Sla.Win` — a distinct line.)

## Sources (first-hand — URL + exact quote)

### CLEAR (reference-grade)

- **`C.KGm.Acc.All` Allgaier** — Hooper & Whyld, *The Oxford Companion to Chess*
  (1st ed.), entry 'ALLGAIER GAMBIT'
  (<https://archive.org/stream/TheOxfordCompanionToChessFirstEditionByDavidHooperKennethWhyld>):
  > "…line played around 1780 by the Englishman Cotter, after whom it is
  > sometimes named… Allgaier was the first to publish a detailed analysis, which
  > appeared in the fourth edition of his book, 1819…"

  **Allgaier/Cotter caveat:** dual attribution. Cotter played the line c.1780;
  Allgaier first published the analysis (1819) and the name stuck to him.

### PARTIAL (web-only — needs reference-grade pin)

- **`B.Fre.Win` Winawer** — Wikipedia, *French Defence*
  (<https://en.wikipedia.org/wiki/French_Defence>):
  > "The Winawer Variation, **named after** Szymon Winawer and pioneered by Aron
  > Nimzowitsch and Mikhail Botvinnik, is one of the main systems in the French."

  (See the Winawer correction above. Distinct from the Slav `D.Sla.Win`.)

- **`B.Fre.Mac` McCutcheon** — Wikipedia, *French Defence*
  (<https://en.wikipedia.org/wiki/French_Defence>):
  > "The McCutcheon Variation is **named for** John Lindsay McCutcheon of
  > Philadelphia (1857–1905), who brought the variation to public attention when
  > he used it to defeat World Champion Steinitz in a simultaneous exhibition in
  > Manhattan in 1885."

  **Spelling note:** the person is **"John Lindsay McCutcheon"** (Mc); the
  catalogue variation is spelled **"MacCutcheon"**. `attributed_to` uses the
  person spelling; the discrepancy is flagged for review.

- **`B.Fre.Bur` Burn** — Wikipedia, *Amos Burn*
  (<https://en.wikipedia.org/wiki/Amos_Burn>):
  > "Burn is the **eponym** of the Burn Variation of the French Defence (1.e4 e6
  > 2.d4 d5 3.Nc3 Nf6 4.Bg5 dxe4)."

- **`C.Sco.Gor` Göring** — Wikipedia, *Carl Göring*
  (<https://en.wikipedia.org/wiki/Carl_G%C3%B6ring>):
  > "His **name is attached to** the Göring Gambit in the Scotch Game (1.e4 e5
  > 2.Nf3 Nc6 3.d4 exd4 4.c3)… Carl Theodor Göring introduced it into master play
  > in 1872."

- **`C.KGm.Acc.Kie` Kieseritzky** — Wikipedia, *Kieseritzky Gambit*
  (<https://en.wikipedia.org/wiki/Kieseritzky_Gambit>):
  > "**Named after** Lionel Kieseritzky (1805-1853)… first described by Polerio
  > in the late 16th century… Kieseritzky had contributed significantly to the
  > theory of 5.Ne5."

  **Polerio caveat:** first described by Polerio (16th c.); named after
  Kieseritzky for his 5.Ne5 theory. (Corrects an earlier skip — Kieseritzky was
  previously parked for lacking a clean "named after" attestation.)

- **`D.QGD.Lsk` Lasker** — chess.com, *Lasker's Queen's Gambit Declined*
  (<https://www.chess.com/article/view/lasker-s-queen-s-gambit-declined>):
  > "…His contribution was the idea of …Ne4… Lasker is generally considered the
  > **author** of the …Ne4 concept."

  **Caveat:** "Lasker" is a multi-head surname; this is the QGD …Ne4 defence
  specifically.

- **`D.QGD.Rag` Ragozin** — chessable blog, *The Ragozin Defence*
  (<https://www.chessable.com/blog/chess-opening-basics-the-ragozin-defence/>):
  > "…Viacheslav Ragozin (the man **after whom the defence was named**)…"

- **`D.QGD.Har` Harrwitz** — Wikipedia, *List of chess openings named after
  people*
  (<https://en.wikipedia.org/wiki/List_of_chess_openings_named_after_people>):
  > "Harrwitz Attack of the Queen's Gambit Declined – 1.d4 d5 2.c4 e6 3.Nc3 Nf6
  > 4.Bf4 – **named after** Daniel Harrwitz."

- **`E.KID.Sml` Sämisch (KID)** — Wikipedia, *King's Indian Defence, Sämisch
  Variation*
  (<https://en.wikipedia.org/wiki/King%27s_Indian_Defence,_S%C3%A4misch_Variation>):
  > "It is **named after** the German grandmaster Friedrich Sämisch."

- **`E.Nim.Sml` Sämisch (Nimzo)** — Wikipedia, *Nimzo-Indian Defence*
  (<https://en.wikipedia.org/wiki/Nimzo-Indian_Defence>):
  > "4.a3 is known as the Sämisch Variation, **after** Fritz Sämisch."

  (Shared eponym with `E.KID.Sml`; distinct lines.)

## Dry-run results (captured)

Run from the worktree root; default `--dry-run`, **no `--apply`**, nothing written.

```
python3 tools/apply_attribution_manifest.py --manifest docs/drafts/attribution-clear.manifest.json --dry-run
  -> rows 5899 -> 5899 ; rows changed: 1 (C.KGm.Acc.All) ; exit 0 ; zero collateral
python3 tools/apply_attribution_manifest.py --manifest docs/drafts/attribution-clear.manifest.json --dry-run --strict
  -> PASSES (CLEAR) ; exit 0

python3 tools/apply_attribution_manifest.py --manifest docs/drafts/attribution-partial.manifest.json --dry-run
  -> rows 5899 -> 5899 ; rows changed: 10 (B.Fre.Win, B.Fre.Mac, B.Fre.Bur, C.Sco.Gor,
     C.KGm.Acc.Kie, D.QGD.Lsk, D.QGD.Rag, D.QGD.Har, E.KID.Sml, E.Nim.Sml) ; exit 0 ; zero collateral
python3 tools/apply_attribution_manifest.py --manifest docs/drafts/attribution-partial.manifest.json --dry-run --strict
  -> REJECTED: "--strict: change for 'B.Fre.Win' has evidence_grade 'PARTIAL'; only 'CLEAR' may be applied" ; exit 1
```

The engine's exact-change contract passed for both (the actually-differing rows
equalled `expected_changed_rows`), so each manifest changes exactly its named
head row(s) and nothing else.

## What's needed before any apply

1. **Albert's explicit GO** (per the agentic-development playbook).
2. **CLEAR (`C.KGm.Acc.All`):** reference-grade and `--strict`-passable —
   apply-ready under GO (`--apply --out --strict --validate`).
3. **PARTIAL heads:** lift each to **CLEAR** with a reference-grade source
   (Oxford Companion entry or a monograph chapter) before they may pass
   `--strict --apply`. Until then they stay parked.

## See also

- [`attribution-drafts-record.md`](attribution-drafts-record.md) — per-slug summary table + caveats.
- [`../attribution-batch-engine.md`](../attribution-batch-engine.md) — the engine + guardrails.
- [`../attribution-source-status.tsv`](../attribution-source-status.tsv) — the source-status registry (Winawer row downgraded to PARTIAL).
