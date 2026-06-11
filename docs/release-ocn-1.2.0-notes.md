# OCN 1.2.0 — diacritic-true names, audited ECO, unconditional gate

**Release notes (draft — tag not yet created).** Docs-only record; no
tag/release/upload accompanies this document. Tag and parquet regen each
wait for their own GO.

- **Proposed release**: `OCN 1.2.0 — diacritic-true names, audited ECO,
  unconditional gate`
- **Proposed tag**: `ocn-1.2.0` (minor bump: 683 `canonical_name` changes
  are consumer-visible; **no slug changes** — row identity is fully stable
  across this boundary, unlike 1.1.0)
- **Target commit**: current `main` (this notes commit or its successor)
- **Previous release**: `ocn-1.1.0`

## Summary

Everything the 360 audit rated P0/P1 on the catalogue itself is closed:

- **Diacritic normalization, Tiers 1+2** — 10 + 4 eponym surnames respelled
  to the person's orthography across all naming columns (López, Grünfeld,
  Réti, Sämisch, Maróczy, Göring, Hübner, Löwenthal, Hromádka, Møller;
  Mikėnas, Krejčík, Opočenský, Pelikán). Policy + evidence:
  `docs/diacritic-normalization-map.md`. Sørensen and Würzburger stay
  parked pending per-row referent evidence.
- **ECO corrections** — 12 rows double-sourced (audit claim + independent
  longest-SAN-prefix derivation against `lichess-org/chess-openings`):
  London family A48→D02 (10), Dragon Yugoslav B76→B78, QID Nimzowitsch
  E17→E15. Four audit claims were **refuted** by the derivation and left
  unchanged (record in `docs/eco-corrections-dry-run.md`).
- **Naming hygiene** — 24 identity aliases dropped, 2 whitespace typos
  fixed; the two checks promoted to errors.
- **Phantom + duplicate-name decisions executed**
  (`docs/phantom-and-duplicate-name-decision.md`): path-marker children
  spec-blessed and ECO-aligned (2 rows); the four duplicate canonical
  names made unique (5 rows). Both validator allowlists now empty.
- **Validator naming + ECO waves** — checks 13–20 live: global name
  uniqueness, banned characters (middle dot, invisibles, controls),
  whitespace, identity-alias, diacritic regression guard (20 banned ASCII
  variants), same-moves-ECO consistency, plus `--audit-naming` /
  `--audit-eco` sweep heuristics. The default gate runs **unconditional —
  zero allowlists, zero standing warnings**.
- **Engine** — third safety mode `eco_legacy_only`; every change in this
  release went through a manifest (8 in `docs/manifests/`), each with a
  committed dry-run record.
- **Schema unchanged** — 14-column catalogue; `transposes_to`/`same_as`
  layer untouched (`unresolved_groups=0` reconfirmed).

## Catalogue diff vs `ocn-1.1.0`

| metric | value |
|---|---|
| rows | 5,899 → 5,899 (0 added, 0 removed, **0 slug changes**) |
| distinct rows changed | 782 |
| `canonical_name` | 683 |
| `notes` | 416 |
| `aliases` | 113 |
| `historical_notes` / `attributed_to` / `attribution_source` | 20 / 19 / 19 |
| `eco_legacy` | 14 |
| sha256 (release head) | `255ab28006ed6ce5bdf713936298cba1cb067eaa859e5fe167cdea84acf34b9a` |
| validator | 5,899 entries, 0 warnings, `--strict-chess` green |
| tool tests | 165 |

Applied lots, in order (manifest → dry-run record, all in `docs/`):

| lot | mode | rows |
|---|---|---|
| naming-error-corrections (P0) | naming_strings_only | 16 |
| attribution-polish (P0) | attribution_fields_only | 3 |
| diacritic-tier1-normalization | naming_strings_only | 663 |
| diacritic-tier2-normalization | naming_strings_only | 50 |
| naming-hygiene | naming_strings_only | 26 |
| eco-corrections | eco_legacy_only | 12 |
| phantom-eco-align | eco_legacy_only | 2 |
| duplicate-name-renames | naming_strings_only | 5 |

## Downstream impact (chess-parquet)

- **Parquet regen is mandatory**: `canonical_name` feeds the parquet's
  name column; 683 values changed.
- **Join keys are safe**: zero `ocn1` changes — anything keyed by slug,
  FEN or zobrist survives untouched. Only name-string joins break (and
  they were joining misspellings).
- Downstream gate, mirroring the 1.1.0 verification doc: regen
  `openings.parquet`, re-run the efcdb-openings join, confirm row count
  5,899 and zero unmatched slugs, then publish both artefacts together.

## Release runbook (each step its own GO)

1. **Freeze + gate** — clean worktree at the release head; run
   `validate.py --strict-chess` (5,899/0), full test suite (165),
   `audit_transpositions.py --summary` (`unresolved_groups=0`); verify
   account `escacsfigueres` and tags `ocn-1.0.2/1.0.3/1.1.0` intact.
2. **GO tag** — annotated tag `ocn-1.2.0` at the head; tags are
   immutable once pushed.
3. **GO push** — push `main` + the tag.
4. **GO regen** — coordinate `chess-parquet`: regenerate, run the
   downstream gate above, record checksums in a
   `release-ocn-1.2.0-downstream-verification.md`.
5. **Record** — mark this document released (replace the draft header),
   update `post-1.1-roadmap.md`.
