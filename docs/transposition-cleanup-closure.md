# Transposition cleanup — phase closure

**Status**: **CLOSED**. Originally one of two research holds; the
Nimzo Bot/Kmo hold was **resolved after closure** (commit
`e036203`), leaving **QID Miles/Petrosian as the sole remaining
unresolved group**.
**Closure snapshot**: `origin/main` at `0200e8e` (the metrics
tables below are this snapshot).
**Current state**: `origin/main` at `e036203` —
`unresolved_groups=1` (QID only), `resolved_groups=124`,
`multiple_canonical_groups=17`, 5,900 rows.
**No catalogue changes accompany this document** — it records
state, it does not alter it.

> **Post-closure update (`e036203`)**: Nimzo Bot/Kmo resolved via
> single_canonical `transposes_to` (`E.Nim.Sml.Kmo → E.Nim.Sml.Bot`,
> spurious "Kmoch" demoted — Lichess E20 places "Kmoch" at 4.f3,
> `E.Nim.Fou`). See
> [`nimzo-botvinnik-kmoch-naming-review.md`](nimzo-botvinnik-kmoch-naming-review.md)
> and
> [`nimzo-botvinnik-kmoch-apply-preflight.md`](nimzo-botvinnik-kmoch-apply-preflight.md).
> The metrics/holds tables below are kept as the `0200e8e` closure
> snapshot for history; see "Remaining holds" for the current
> single hold.

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

## Remaining holds — 1 group (was 2 at closure)

| group | ECO | status | why / outcome | next-sprint path |
|---|---|---|---|---|
| `E.Nim.Sml.Bot` ⇄ `E.Nim.Sml.Kmo` | E24/E25 ⇄ E26 | ✅ **RESOLVED after closure** (`e036203`) | Naming review (Lichess E20 = Kmoch is 4.f3; E24 = the Sämisch f3-tabiya is Botvinnik) showed `E.Nim.Sml.Kmo`'s "Kmoch" was an artifact. Resolved via `E.Nim.Sml.Kmo.transposes_to = E.Nim.Sml.Bot` + relabel ("a3 Move Order"). | done — follow-ups (`E.Nim.Rub.Kmo` artifact, `Kmo.MLn` parent-chain) noted in the apply preflight. |
| `E.QID.Mil.MLn` ⇄ `E.QID.Pet.KPe` | E12 ⇄ E12 | **DEFERRED — structural review** (sole remaining hold) | `E.QID.Mil.MLn`'s move list (`…a3 Bb7 Nc3`) does not extend its parent `E.QID.Mil` (4.Bf4) — a **broken parent chain**. The whole a3/Nc3 Kasparov-Petrosian theory subtree (10 descendants) hangs under the mislabelled "Miles" branch, while the correctly-named `E.QID.Pet.KPe` is an empty leaf. | Re-slug the `Mil.MLn` subtree under `E.QID.Pet.KPe` (OCN's first slug-rename; coordinate `chess-parquet`). Fully preflighted in [`qid-miles-petrosian-migration-preflight.md`](qid-miles-petrosian-migration-preflight.md). |

As of `e036203`, `audit_transpositions.py --ranked` shows **one**
remaining unresolved group: QID Miles/Petrosian. It must not be
touched without its dedicated slug-migration sprint — a quick
`same_as` would bury the broken parent chain.

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
