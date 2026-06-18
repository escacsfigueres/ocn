# Attribution drafts — per-slug record

**UN-APPLIED. No `--apply` ran. CSV byte-for-byte unchanged.** Companion to
[`README.md`](README.md). One row per drafted head. All head-only, all
`mode = attribution_fields_only`. Drafted 2026-06-19.

## Drafted

| slug | attributed_to | role / type | source (URL + exact quote) | grade | dry-run | needed before apply |
|---|---|---|---|---|---|---|
| `B.Fre.Win` | Szymon Winawer | early practitioner (type C) | *The Center Game* (nlm Q25, src `a433382e`): "(3.Nc3 Bb4) **named after him**"; corroborated Wikipedia *French Defence* / *Szymon Winawer* | **CLEAR** | clean, 1 row, zero collateral; `--strict` passes | Albert GO + pin *The Center Game* author/year |
| `B.Fre.Mac` | John Lindsay McCutcheon | early practitioner / popularizer (type C) | Wikipedia *French Defence* (<https://en.wikipedia.org/wiki/French_Defence>, 2026-06-19): "The McCutcheon Variation is **named for** John Lindsay McCutcheon of Philadelphia (1857–1905), who … defeat[ed] World Champion Steinitz in a simultaneous exhibition in Manhattan in 1885." | **PARTIAL** | clean (in 4-row batch), zero collateral; `--strict` rejects | reference-grade pin (OC 'McCutcheon') + GO |
| `B.Fre.Bur` | Amos Burn | eponym / practitioner (type C) | Wikipedia *Amos Burn* (<https://en.wikipedia.org/wiki/Amos_Burn>, 2026-06-19): "Burn is the **eponym** of the Burn Variation of the French Defence (1.e4 e6 2.d4 d5 3.Nc3 Nf6 4.Bg5 dxe4)." (1848–1925); corroborated Wikipedia *French Defence*: "**Named after** Amos Burn…" | **PARTIAL** | clean (in 4-row batch), zero collateral; `--strict` rejects | reference-grade pin (OC 'Burn') + GO |
| `C.KGm.Acc.All` | Johann Baptist Allgaier | eponym (type B/C) | Wikipedia *Johann Baptist Allgaier* (<https://en.wikipedia.org/wiki/Johann_Baptist_Allgaier>, 2026-06-19): "…the variant of the King's Gambit **named after him** (1.e4 e5 2.f4 exf4 3.Nf3 g5 4.h4 g4 5.Ng5, the so-called Allgaier's Gambit)…" (1763–1823) | **PARTIAL** | clean (in 4-row batch), zero collateral; `--strict` rejects | reference-grade pin (OC 'Allgaier Gambit') + GO |
| `C.Sco.Gor` | Carl Theodor Göring | introduced into master play / eponym (type B/C) | Wikipedia *Carl Göring* (<https://en.wikipedia.org/wiki/Carl_G%C3%B6ring>, 2026-06-19): "His **name is attached to** the Göring Gambit in the Scotch Game (1.e4 e5 2.Nf3 Nc6 3.d4 exd4 4.c3)…" (1841–1879); corroborated Wikipedia *Scotch Game* (introduced into master play 1872; Staunton played it in the 1840s) | **PARTIAL** | clean (in 4-row batch), zero collateral; `--strict` rejects | reference-grade pin (OC 'Göring Gambit') + GO |

**Manifests:** `B.Fre.Win` is in `french-winawer.manifest.json`; the four PARTIAL
heads are in `web-sourced-safe-heads.manifest.json`.

## Skipped — needs source

| slug | reason |
|---|---|
| `C.KGm.Acc.Kie` (Kieseritzky) | Wikipedia gives only "popularized by" / "name became associated with the Kieseritzky Gambit" — associative, not a direct "named after" attestation. Over-reading risk; skipped. Needs a source that states the naming directly. |
| `D.QGD.Lsk` (Lasker), `D.QGD.Rag` (Ragozin), `D.QGD.Har` (Harrwitz) | Not source-fetched this run; no first-hand naming passage obtained. Left for a future evidence pass. (`D.QGD.Har.Har` has a known pre-existing duplicated-`canonical_name`, out of scope.) |
| `E.KID.Sml`, `E.Nim.Sml`, `E.Gru.Sml` (Sämisch heads) | Not source-fetched this run; left for a future pass. |

## Verification

- All 5 drafted slugs exist in `catalog/ocn-1.csv`, are heads, and had
  `attributed_to` / `attribution_source` / `historical_notes` all empty before
  drafting (confirmed by direct CSV read).
- Both dry-runs exited 0 with rows `5899 -> 5899` and the engine's exact-change
  contract satisfied (changed rows == `expected_changed_rows`), i.e. zero
  collateral diff.
- No `--apply` was run. `git diff --stat catalog/ocn-1.csv` is empty (CSV
  unchanged). No git command that writes was run; no fabrication — every quote
  above was fetched first-hand this run or carried verbatim from the verified
  source log.
