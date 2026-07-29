# Allgaier CLEAR attribution — dry-run record (APPLIED)

**Status: APPLIED 2026-07-29** under Albert's GO (traction-roadmap H0.1),
after the ship-ready half of `feat/finish-goals` was merged. Manifest:
[`manifests/allgaier-clear.manifest.json`](manifests/allgaier-clear.manifest.json)
(extracted byte-identical from the branch drafts at `9b2304c`; its DRAFT
wording is historical). This was the single CLEAR, reference-grade,
`--strict`-passable head from the verified-findings sweep.

- Mode: `attribution_fields_only`; head row only: `C.KGm.Acc.All`.
- Rows changed: 1 (exactly the expected set).
- Catalogue sha256 before: `163a0aac8fe2692578da1cffbdd3cc20577578960b6db054b4ac2736cb8070e8`
- Catalogue sha256 after:  `41eb3374aeff4e5122974ce6de4ff0349736f12a061565eeeba9051b77cff1b3`
  (apply output matched the dry-run prediction byte-for-byte).
- `--strict`: PASS (CLEAR only). Validator: `OK: 5899 entries validated,
  0 warning(s)`. Test suite: 285 green after regenerating the two derived
  sidecars (`ocn-1.attribution.tsv`, `ocn-1.name_basis.tsv`) whose drift
  guards correctly fired on the catalogue change.
- Source: Hooper & Whyld, *The Oxford Companion to Chess* (first edition),
  entry "ALLGAIER GAMBIT". Dual-attribution caveat (Cotter, ~1780) recorded
  in `historical_notes`.

The ten PARTIAL heads from the same sweep remain un-applied on the branch,
tracked as an issue until the graded-evidence policy (roadmap H4.4) lands.
