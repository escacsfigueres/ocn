# Attribution drafts — per-slug record

**UN-APPLIED. No `--apply` ran. CSV byte-for-byte unchanged.** Companion to
[`README.md`](README.md). One row per drafted head. All head-only, all
`mode = attribution_fields_only`. Drafted 2026-06-19; restructured into a
clean CLEAR/PARTIAL split.

## Manifests

| File | Slugs | Grade | Dry-run | `--strict` |
|---|---|---|---|---|
| [`attribution-clear.manifest.json`](attribution-clear.manifest.json) | `C.KGm.Acc.All` (Allgaier) | **CLEAR** | clean, 1 row, zero collateral | **PASSES** |
| [`attribution-partial.manifest.json`](attribution-partial.manifest.json) | 10 heads (below) | **PARTIAL** | clean, 10 rows, zero collateral | **REJECTED** (errors on first PARTIAL: `B.Fre.Win`) |

## CLEAR — `attribution-clear.manifest.json`

| slug | attributed_to | role / type | source (URL + exact quote) | grade |
|---|---|---|---|---|
| `C.KGm.Acc.All` | Johann Baptist Allgaier | analyst; first to publish the analysis, 1819 (type C) | Hooper & Whyld, *The Oxford Companion to Chess* (1st ed.), entry 'ALLGAIER GAMBIT' (<https://archive.org/stream/TheOxfordCompanionToChessFirstEditionByDavidHooperKennethWhyld>): "…line played around 1780 by the Englishman Cotter, after whom it is sometimes named… Allgaier was the first to publish a detailed analysis, which appeared in the fourth edition of his book, 1819…" | **CLEAR** (reference-grade book/encyclopaedia) |

**Allgaier/Cotter caveat (recorded):** dual attribution. The Oxford Companion
notes the line is "sometimes named" after the Englishman Cotter (who played it
around 1780); Allgaier was the *first to publish* the detailed analysis (1819)
and the name stuck to him. `attributed_to` reflects the analyst/first-publisher
role.

## PARTIAL — `attribution-partial.manifest.json`

All web-sourced → **PARTIAL**. Each needs a reference-grade pin (Oxford
Companion entry / monograph) to lift to CLEAR before any `--strict --apply`.

| slug | attributed_to | role / type | source (URL + exact quote) | grade |
|---|---|---|---|---|
| `B.Fre.Win` | Szymon Winawer | eponym; early practitioner (type B) | Wikipedia *French Defence* (<https://en.wikipedia.org/wiki/French_Defence>): "The Winawer Variation, **named after** Szymon Winawer and pioneered by Aron Nimzowitsch and Mikhail Botvinnik…" | **PARTIAL** |
| `B.Fre.Mac` | John Lindsay McCutcheon | eponym; early practitioner (type B) | Wikipedia *French Defence* (<https://en.wikipedia.org/wiki/French_Defence>): "The McCutcheon Variation is **named for** John Lindsay McCutcheon of Philadelphia (1857–1905), who … defeat[ed] World Champion Steinitz in a simultaneous exhibition in Manhattan in 1885." | **PARTIAL** |
| `B.Fre.Bur` | Amos Burn | eponym (type C) | Wikipedia *Amos Burn* (<https://en.wikipedia.org/wiki/Amos_Burn>): "Burn is the **eponym** of the Burn Variation of the French Defence (1.e4 e6 2.d4 d5 3.Nc3 Nf6 4.Bg5 dxe4)." | **PARTIAL** |
| `C.Sco.Gor` | Carl Theodor Göring | eponym; introduced into master play 1872 (type C) | Wikipedia *Carl Göring* (<https://en.wikipedia.org/wiki/Carl_G%C3%B6ring>): "His **name is attached to** the Göring Gambit in the Scotch Game (1.e4 e5 2.Nf3 Nc6 3.d4 exd4 4.c3)… Carl Theodor Göring introduced it into master play in 1872." | **PARTIAL** |
| `C.KGm.Acc.Kie` | Lionel Kieseritzky | eponym; theorist of 5.Ne5 (type C) | Wikipedia *Kieseritzky Gambit* (<https://en.wikipedia.org/wiki/Kieseritzky_Gambit>): "**Named after** Lionel Kieseritzky (1805-1853)… first described by Polerio in the late 16th century… Kieseritzky had contributed significantly to the theory of 5.Ne5." | **PARTIAL** |
| `D.QGD.Lsk` | Emanuel Lasker | author of the …Ne4 concept (type C) | chess.com *Lasker's Queen's Gambit Declined* (<https://www.chess.com/article/view/lasker-s-queen-s-gambit-declined>): "…Lasker is generally considered the **author** of the …Ne4 concept." | **PARTIAL** |
| `D.QGD.Rag` | Viacheslav Ragozin | eponym (type B) | chessable blog *The Ragozin Defence* (<https://www.chessable.com/blog/chess-opening-basics-the-ragozin-defence/>): "…Viacheslav Ragozin (the man **after whom the defence was named**)…" | **PARTIAL** |
| `D.QGD.Har` | Daniel Harrwitz | eponym (type B) | Wikipedia *List of chess openings named after people* (<https://en.wikipedia.org/wiki/List_of_chess_openings_named_after_people>): "Harrwitz Attack of the Queen's Gambit Declined – 1.d4 d5 2.c4 e6 3.Nc3 Nf6 4.Bf4 – **named after** Daniel Harrwitz." | **PARTIAL** |
| `E.KID.Sml` | Friedrich Sämisch | eponym (type B) | Wikipedia *King's Indian Defence, Sämisch Variation* (<https://en.wikipedia.org/wiki/King%27s_Indian_Defence,_S%C3%A4misch_Variation>): "It is **named after** the German grandmaster Friedrich Sämisch." | **PARTIAL** |
| `E.Nim.Sml` | Friedrich Sämisch | eponym (type C) | Wikipedia *Nimzo-Indian Defence* (<https://en.wikipedia.org/wiki/Nimzo-Indian_Defence>): "4.a3 is known as the Sämisch Variation, **after** Fritz Sämisch." | **PARTIAL** |

## Per-head caveats / review notes

- **`B.Fre.Win` Winawer — CORRECTION (prominent).** The earlier draft graded
  this **CLEAR** on *The Center Game*. That is **debunked**: *The Center Game*
  is Arne Moll's monograph about the **Center Game** opening (1.e4 e5 2.d4 exd4
  3.Qxd4) — a **different** opening — and the NotebookLM "(3.Nc3 Bb4) named after
  him" grounding was **hallucinated**. Do **not** cite *The Center Game*. The
  grade now rests on Wikipedia *French Defence* (web → **PARTIAL**). The same
  eponym also names the **Winawer Countergambit in the Slav** (catalogue
  `D.Sla.Win`) — a distinct line.
- **`B.Fre.Mac` McCutcheon — spelling note.** The person is **"John Lindsay
  McCutcheon"** (Mc); the catalogue variation is spelled **"MacCutcheon"**.
  `attributed_to` uses the person spelling (McCutcheon); the discrepancy is
  flagged in `historical_notes` for review.
- **`C.KGm.Acc.All` Allgaier — Cotter caveat.** Dual attribution; see CLEAR
  table above. Line first played around 1780 by the Englishman Cotter; Allgaier
  first published the analysis (1819).
- **`C.KGm.Acc.Kie` Kieseritzky — Polerio caveat.** The line was **first
  described by Polerio** (late 16th c.); it carries Kieseritzky's name for his
  significant contribution to the theory of 5.Ne5. (This corrects an earlier
  skip — Kieseritzky was previously parked for lacking a clean "named after"
  attestation; Wikipedia's *Kieseritzky Gambit* now supplies one.)
- **`D.QGD.Lsk` Lasker — multi-head surname.** "Lasker" names several lines;
  this attribution is the **QGD …Ne4 defence** specifically.
- **`E.KID.Sml` / `E.Nim.Sml` Sämisch — shared eponym.** Friedrich (Fritz)
  Sämisch names both the King's Indian Sämisch (`E.KID.Sml`, 5.f3) and the
  Nimzo-Indian Sämisch (`E.Nim.Sml`, 4.a3) — distinct lines, both head-only.

## GO path

- **CLEAR (`C.KGm.Acc.All`):** reference-grade and `--strict`-passable.
  Apply-ready **pending only Albert's explicit GO** (`--apply --out` under GO,
  per the agentic-development playbook).
- **PARTIAL (10 heads):** each must be lifted to **CLEAR** with a
  reference-grade pin (Oxford Companion entry / monograph) **before** it can pass
  `--strict --apply`. Until then they stay parked. The engine's `--strict` mode
  physically rejects the PARTIAL manifest (errors on the first PARTIAL grade).

## Verification

- All 11 drafted slugs exist in `catalog/ocn-1.csv`, are heads, and had
  `attributed_to` / `attribution_source` / `historical_notes` all empty before
  drafting (confirmed by direct CSV read).
- Both dry-runs exited 0 with rows `5899 -> 5899` and the engine's exact-change
  contract satisfied (changed rows == `expected_changed_rows`), i.e. zero
  collateral diff. CLEAR `--strict` **passes** (exit 0); PARTIAL `--strict` is
  **rejected** (exit 1, errors on `B.Fre.Win`).
- The registry (`docs/attribution-source-status.tsv`) `B.Fre.Win` row was
  downgraded CLEAR → PARTIAL with the *The Center Game* debunk recorded;
  `tools/tests/test_source_status_table.py` still passes (20/20).
- No `--apply` was run. `git diff --stat catalog/ocn-1.csv` is empty (CSV
  unchanged). No git command that writes was run; no fabrication — every quote
  above is from the verified-findings set fetched first-hand.
