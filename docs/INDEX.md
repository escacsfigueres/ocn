# docs/ index

One line per live document. **Convention:** `docs/` holds live
documentation and permanent records; `docs/archive/` holds era-closed
working documents (applied proposals, migration preflights, superseded
roadmaps and checklists) — nothing is deleted, and relative links inside
archived documents are frozen as written in their era. The slug gate
(`tools/verify_doc_slugs.py`, enforced by
`tools/tests/test_verify_doc_slugs.py`) runs over README, the spec and
every top-level doc here; intentional historical slugs in live records
carry a `NON-CATALOGUE` marker within two lines. New working documents
start here and move to `archive/` when their era closes.

## Start here

| doc | what it is |
|---|---|
| [`consuming-ocn-0.2.md`](consuming-ocn-0.2.md) | The consumer guide: joins, transpositions, co-canonicals, recipes (`tools/ocn.py`). Current as of 1.2.0. |
| [`post-1.1-roadmap.md`](post-1.1-roadmap.md) | The living roadmap and work log since `ocn-1.1.0`. |
| [`agentic-development-playbook.md`](agentic-development-playbook.md) | The human–agent contract: Intent/Expectations/Context/Workflow, GO gates, task sizing. |
| [`ocn-360-audit.md`](ocn-360-audit.md) | The 13-agent 360° audit (2026-06-10) that drove the P0/P1/P2 plan. |
| [`i18n-aliases-design.md`](i18n-aliases-design.md) | Locale alias sidecars (Track 2): format, conventions, ca+es pilot. |

## Releases (permanent records)

| doc | what it is |
|---|---|
| [`release-ocn-1.2.0-notes.md`](release-ocn-1.2.0-notes.md) | 1.2.0 notes and gated runbook (released 2026-06-11). |
| [`release-ocn-1.2.0-downstream-verification.md`](release-ocn-1.2.0-downstream-verification.md) | Published-asset verification for 1.2.0. |
| [`release-ocn-1.1.0-notes.md`](release-ocn-1.1.0-notes.md) | 1.1.0 notes (fully resolved transposition catalogue). |
| [`release-ocn-1.1.0-downstream-verification.md`](release-ocn-1.1.0-downstream-verification.md) | Published-asset verification for 1.1.0. |

## Decision records

| doc | what it is |
|---|---|
| [`qid-migration-decision-record.md`](qid-migration-decision-record.md) | OCN's first slug migration (QID Miles → Kasparov-Petrosian). |
| [`transposition-cleanup-closure.md`](transposition-cleanup-closure.md) | Closure of the duplicate-FEN resolution layer (`unresolved_groups=0`). |
| [`phantom-and-duplicate-name-decision.md`](phantom-and-duplicate-name-decision.md) | Path-marker spec-bless + duplicate-name renames (executed 2026-06-11). |
| [`diacritic-normalization-map.md`](diacritic-normalization-map.md) | The diacritic policy and all three applied tier maps (755 rows). |

## Applied-lot records (manifest + dry-run pairs)

Manifests live in [`manifests/`](manifests/); each applied lot keeps its
dry-run report here, marked APPLIED:
[`lot-a-player-eponyms-dry-run.md`](lot-a-player-eponyms-dry-run.md),
[`lot-3-eco-a-eponyms-dry-run.md`](lot-3-eco-a-eponyms-dry-run.md),
[`naming-error-corrections-record.md`](naming-error-corrections-record.md),
[`diacritic-tier1-dry-run.md`](diacritic-tier1-dry-run.md),
[`diacritic-tier2-dry-run.md`](diacritic-tier2-dry-run.md),
[`diacritic-tier3-dry-run.md`](diacritic-tier3-dry-run.md),
[`naming-hygiene-dry-run.md`](naming-hygiene-dry-run.md),
[`eco-corrections-dry-run.md`](eco-corrections-dry-run.md),
[`phantom-eco-align-dry-run.md`](phantom-eco-align-dry-run.md),
[`duplicate-name-renames-dry-run.md`](duplicate-name-renames-dry-run.md),
[`american-spelling-aliases-dry-run.md`](american-spelling-aliases-dry-run.md),
[`lichess-label-aliases-dry-run.md`](lichess-label-aliases-dry-run.md).

## Attribution system (live)

| doc | what it is |
|---|---|
| [`attribution-batch-engine.md`](attribution-batch-engine.md) | The apply engine: manifest schema, modes, guardrails. |
| [`naming-attribution-automation.md`](naming-attribution-automation.md) | The triage tool — automates triage, not truth. |
| [`naming-attribution-audit-methodology.md`](naming-attribution-audit-methodology.md) | Attribution types A–I, evidence rules. |
| [`naming-attribution-audit-backlog.md`](naming-attribution-audit-backlog.md) | Discovery backlog (32 slugs, source-gated). |
| [`whole-catalogue-attribution-factory-map.md`](whole-catalogue-attribution-factory-map.md) | The 10 ranked source-gated lots + do-not-touch map. |
| [`attribution-factory-tooling.md`](attribution-factory-tooling.md) | Factory tools built / pending. |
| [`non-person-opening-name-taxonomy.md`](non-person-opening-name-taxonomy.md) | Why non-person names stay unattributed. |
| [`parked-attribution-reference-source-log.md`](parked-attribution-reference-source-log.md) | Source log for parked items (CLEAR/PARTIAL grades). |
| [`parked-naming-audit-source-sweep.md`](parked-naming-audit-source-sweep.md) | Source sweep over the parked naming items. |
| [`player-eponym-group-b-evidence-sprint.md`](player-eponym-group-b-evidence-sprint.md) | Evidence state for the parked Group B eponyms (Alapin, Taimanov…). |
| [`french-winawer-attribution-proposal.md`](french-winawer-attribution-proposal.md) | PARKED proposal — held until the citation author/year is pinned. |

## Archive

Era-closed working documents: [`archive/`](archive/) — 0.2-era roadmap
and checklists, the transposition-era trackers and proposals, the QID
migration working set, and every applied attribution/naming proposal
whose outcome is recorded above.
