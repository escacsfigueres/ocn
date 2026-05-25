# Transposition cleanup — phase closure

**Status**: **CLOSED** (except two dedicated-research holds).
**Final baseline**: `origin/main` at `0200e8e`.
**No catalogue changes accompany this document** — it records the
state, it does not alter it.

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
> DELETE. The two groups that remain unresolved are deliberately
> held: each requires a dedicated investigation sprint, not a
> clean-up edit.

## Remaining holds (2 groups)

| group | ECO | status | why held | next-sprint path |
|---|---|---|---|---|
| `E.Nim.Sml.Bot` ⇄ `E.Nim.Sml.Kmo` | E24/E25 ⇄ E26 | **ON HOLD — naming review** | Catalogue self-conflict: `E.Nim.Fou` (4.f3, depth 2) already carries the `Kmoch Variation\|4.f3 System` alias, so the depth-3 `Sml.Kmo` "Kmoch" attribution is disputed. A `same_as` would freeze a contested name. | External naming review (Lichess opening DB, ECO, Wikipedia, the lichess-org/chess-openings source); then rename / `same_as` / keep-hold. See [`nimzo-saemisch-botvinnik-kmoch-proposal.md`](nimzo-saemisch-botvinnik-kmoch-proposal.md). |
| `E.QID.Mil.MLn` ⇄ `E.QID.Pet.KPe` | E12 ⇄ E12 | **DEFERRED — structural review** | `E.QID.Mil.MLn`'s move list (`…a3 Bb7 Nc3`) does not extend its parent `E.QID.Mil` (4.Bf4) — a **broken parent chain**. The whole a3/Nc3 Kasparov-Petrosian theory subtree (10 descendants) hangs under the mislabelled "Miles" branch, while the correctly-named `E.QID.Pet.KPe` is an empty leaf. | Reparent the `Mil.MLn` subtree under `E.QID.Pet`, or relabel, or collapse against `Pet.KPe`. Larger than a `same_as`. See [`final-same-as-candidates-proposal.md`](final-same-as-candidates-proposal.md). |

Both are visible in `audit_transpositions.py --ranked` as the only
two remaining unresolved groups (ranks 1-2). Neither should be
touched without its own investigation sprint — applying a quick
`same_as` to either would bury a real problem (a contested name, or
a broken parent chain).

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
layer without a dedicated investigation sprint** for QID
Miles/Petrosian (structural) or Nimzo Bot/Kmo (naming). The
mechanical and clear-conceptual work is done; what remains is
judgement requiring either external sources (Nimzo) or a
reparent/relabel decision (QID). Treat `0200e8e` as the closed
baseline for this phase.

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
`nimzo-saemisch-botvinnik-kmoch-proposal.md` (ON HOLD).
