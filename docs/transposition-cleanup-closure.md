# Transposition cleanup — phase closure

**Status**: **FULLY RESOLVED — 0 unresolved groups.** Both former
research holds are fixed: Nimzo Bot/Kmo (`e036203`, single_canonical
TT) and QID Miles/Petrosian (slug-migration — OCN's first
slug-rename). Every duplicate FEN group in the catalogue is now
resolved.
**Closure snapshot**: `origin/main` at `0200e8e` (the metrics
tables below are this snapshot, when 2 holds remained).
**Current state**: `unresolved_groups=0`, `resolved_groups=124`,
`multiple_canonical_groups=17`, **5,899 rows**.
**No catalogue changes accompany this document** — it records
state, it does not alter it.

> **Post-closure updates**:
> - Nimzo Bot/Kmo resolved (`e036203`) via single_canonical
>   `transposes_to` (`E.Nim.Sml.Kmo → E.Nim.Sml.Bot`, spurious
>   "Kmoch" demoted — Lichess E20 places "Kmoch" at 4.f3).
> - **QID Miles/Petrosian resolved** (slug-migration): re-slugged
>   the 10-node mislabelled subtree `E.QID.Mil.MLn.* →
>   E.QID.Pet.KPe.*` + deleted the duplicate `E.QID.Mil.MLn` →
>   **unresolved 1 → 0**, rows 5,900 → 5,899. Release-cycle artefact
>   regen + tag still GO-gated
>   ([`qid-release-cycle-checklist.md`](qid-release-cycle-checklist.md)
>   steps 4-9).
>
> The metrics/holds tables below are kept as the `0200e8e` closure
> snapshot for history; the catalogue is now fully resolved.

## What this phase did

Systematically resolved every duplicate-FEN group in the OCN-1
catalogue that could be settled either mechanically (move-order
mirrors, descriptor duplicates, deeper-path duplicates) or by a
clear conceptual arbitration (two genuine literary names → `same_as`;
one home + a move-order route → `transposes_to`). The only groups
left unresolved are two that are **not** clean-up items but genuine
research questions (see "Remaining holds").

## Metrics

### This session (baseline `5037eef` → final `0200e8e`)

| metric | start (`5037eef`) | final (`0200e8e`) | Δ |
|---|---|---|---|
| catalogue rows | 5,905 | 5,900 | −5 (5 DELETEs of mechanical descriptor leaves) |
| duplicate_groups | 130 | 125 | −5 |
| resolved_groups | 99 | **123** | **+24** |
| unresolved_groups | 31 | **2** | **−29** |
| multiple_canonical_groups | 12 | **17** | **+5** |
| rows_in_unresolved_groups | 62 | 4 | −58 |

### Full `same_as` arc (OCN 0.3 schema → now)

Multiple-canonical groups grew **6 → 17 (+11)** across the whole
`same_as` programme (the OCN 0.3 schema commit seeded 6; the +11
spans Larsen, London, Van Geet/Van't Kruijs, QGA Flohr, Budapest,
KID Simagin/Uhlmann, and Modern/Sicilian). The +5 in the table
above is the slice of that arc that landed in this session.

## Closure principle

> **All actionable duplicate FEN groups are resolved** — every
> mechanical mirror, descriptor duplicate, and clear conceptual
> arbitration has been settled via `transposes_to`, `same_as`, or
> DELETE. The groups that remain unresolved are deliberately held:
> each requires a dedicated investigation sprint, not a clean-up
> edit. *(At closure there were 2; Nimzo was resolved after closure
> in `e036203`, leaving 1 — QID.)*

## Former holds — both RESOLVED (0 remaining)

| group | ECO | status | outcome |
|---|---|---|---|
| `E.Nim.Sml.Bot` ⇄ `E.Nim.Sml.Kmo` | E24/E25 ⇄ E26 | ✅ **RESOLVED** (`e036203`) | Naming review (Lichess E20 = Kmoch is 4.f3; E24 = the Sämisch f3-tabiya is Botvinnik) showed `E.Nim.Sml.Kmo`'s "Kmoch" was an artifact. Resolved via `E.Nim.Sml.Kmo.transposes_to = E.Nim.Sml.Bot` + relabel ("a3 Move Order"). Follow-ups (`E.Nim.Rub.Kmo` artifact, `Kmo.MLn` parent-chain) noted in the apply preflight. |
| `E.QID.Mil.MLn` ⇄ `E.QID.Pet.KPe` | E12 ⇄ E12 | ✅ **RESOLVED via slug-migration** (OCN's first slug-rename) | The a3/Nc3 Kasparov-Petrosian subtree (broken parent chain, mislabelled "Miles") was re-slugged `E.QID.Mil.MLn.* → E.QID.Pet.KPe.*` (10 rows, parents fixed, relabelled) and the duplicate `E.QID.Mil.MLn` deleted. rows 5,900 → 5,899, **unresolved 1 → 0**. Release-cycle artefact regen + tag still GO-gated ([`qid-release-cycle-checklist.md`](qid-release-cycle-checklist.md) steps 4-9). |

`audit_transpositions.py --ranked` now shows **no** unresolved
groups. The catalogue is fully resolved.

## Tags untouched

The release tags were **not moved** during this phase:

| tag | commit | role |
|---|---|---|
| `ocn-1.0.2` | `415f1df` | release baseline |
| `ocn-1.0.3` | `dd2abd3` | post-cleanup release with downloadable artefacts |

All cleanup landed on `main` after `dd2abd3`; the tagged releases
remain immutable. The `ocn-1.0.3` artefacts (positions.tsv,
openings.parquet) reflect the `dd2abd3` state — regenerating now
would change the positions.tsv checksum (additional `same_as` and
`transposes_to` rows), but the existing release is not invalidated.

## Recommendation

**Do not apply further catalogue changes to the transposition
layer without a dedicated investigation sprint.** Nimzo Bot/Kmo is
now done (`e036203`); the **only remaining hold is QID
Miles/Petrosian** — a structural slug-migration (re-slug the
mislabelled subtree under `E.QID.Pet.KPe`), fully preflighted, which
needs `chess-parquet` coordination and its own GO. Treat `e036203`
as the current baseline (`0200e8e` was the closure snapshot).

The **go/no-go decision** for that slug-migration is recorded in
[`qid-migration-decision-record.md`](qid-migration-decision-record.md)
— recommendation: **bundle it with the next release/tag cycle**, not
an immediate out-of-band apply (the defect is internal/non-position
and the catalogue is fully functional at `unresolved_groups=1`).

## Provenance

Full per-group resolution log: [`transpositions.md`](transpositions.md).
Roadmap of the cleanup: [`unresolved-map-20.md`](unresolved-map-20.md).
Per-case proposals: `larsen-reti-nimzowitsch-proposal.md`,
`london-classical-mason-proposal.md`,
`van-geet-vant-kruijs-proposal.md`,
`qga-flohr-janowski-proposal.md`,
`budapest-adler-rubinstein-proposal.md`,
`final-same-as-candidates-proposal.md`,
`final-cross-family-arbitration-proposal.md`,
`nimzo-saemisch-botvinnik-kmoch-proposal.md` →
`nimzo-botvinnik-kmoch-naming-review.md` →
`nimzo-botvinnik-kmoch-apply-preflight.md` (RESOLVED `e036203`),
`qid-miles-petrosian-structural-proposal.md` →
`qid-miles-petrosian-migration-preflight.md` (remaining hold).
