# OCN 1.2.1 — the launch release: public repo, installable package, honest spec

**Tag:** `ocn-1.2.1`. **Date:** 2026-07-30. **Catalogue:** 5,899 rows,
zero slug changes since 1.2.0 — anything keyed by `ocn1`, `fen_key` or
zobrist survives untouched. This is the release that takes OCN public.

## Headlines

- **Installable.** `pip install ocn-chess` (or the wheel attached here):
  the catalogue travels inside the package — typed rows, ECO and
  diacritic-folded name lookup, O(1) position lookup with the en-passant
  normalisation built in, and an `ocn` CLI (`lookup`, `fen`, `uci`,
  `annotate`, `version`).
- **`ocn annotate games.pgn`** names your games by position at every ply
  — a Najdorf reached through 1.Nf3 is named a Najdorf. About a thousand
  games per third of a second.
- **Spec 1.3.** Normative RFC 5234 ABNF with a public conformance corpus
  (101 cases); a from-spec second implementation agrees with the
  validator on every one of the 5,899 slugs. Position identity (FEN key
  and Polyglot zobrist) is defined in-spec (Annex A) and computed
  in-repo — all seven public Polyglot test vectors match exactly.
- **Honest classification.** 770 rows (13.8%) carry an OCN class letter
  that differs from their ECO letters — deliberately, and now
  machine-readably: `ocn-1.eco-divergence.tsv`, validator-enforced, with
  written rationales (the French above all).
- **Editorial floor raised.** 2,128 synthetic aliases deleted; the 29
  cross-row alias collisions decided (5 approved shared names, validator
  check 23 guards the rest); every attribution source is published and
  publicly checkable (unverifiable-source patterns fail validation).
- **Governance for outsiders.** CONTRIBUTING, GOVERNANCE (registrar
  model), issue templates, an errata register that names the spec's own
  past mistakes, and a deprecation lifecycle with a permanent redirects
  sidecar.

## Assets on this release

| file | what it is |
|---|---|
| `ocn-1.csv` | the catalogue, 14 columns, CC-BY-4.0 |
| `ocn-1.json` | whole catalogue with derived SAN movetext |
| `ocn-1.positions.tsv` | per-row `fen_key`, FEN, SAN, EPD, Polyglot zobrist |
| `ocn-1.lichess-xref.tsv` | 1:1 mapping to the Lichess opening names |
| `ocn-1.eco.tsv` | scalar (slug, eco, seq) join table, 7,234 rows |
| `ocn-1.eco-divergence.tsv` | the 770 documented class divergences |
| `ocn_chess-1.2.1-*.whl` + `.tar.gz` | the Python package |
| `SHA256SUMS` | checksums for everything above |

## Compatibility

No `ocn1` changes. Name-string joins: 2,152 alias strings were removed
(synthetic "(SAN) Line" and "Main Line" entries, plus 24 decided
collisions) — joins on those strings were matching noise. The `fen`
column in the positions sidecar now carries true halfmove/fullmove
counters (was hardcoded "0 1"); `fen_key` is unchanged and remains the
join key. The parquet artefact is retired; the positions sidecar carries
the zobrist.

## Provenance

Everything above landed through the manifest engine or reviewed lots,
each with a dry-run record in `docs/archive/`, under the process
described in `GOVERNANCE.md`. The full audit that drove this release:
`docs/ocn-audit-2026-07.md`; the plan: `docs/traction-roadmap.md`.
