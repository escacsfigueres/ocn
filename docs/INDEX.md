# docs/ index

One line per live document. **Convention:** `docs/` holds live
documentation and permanent records; `docs/archive/` holds era-closed
working documents (applied proposals and dry-run records, migration
preflights, superseded roadmaps and checklists) — nothing is deleted,
and relative links inside archived documents are frozen as written in
their era. The slug gate (`tools/verify_doc_slugs.py`, enforced by
`tools/tests/test_verify_doc_slugs.py`) runs over README, the spec and
every top-level doc here; intentional historical slugs in live records
carry a `NON-CATALOGUE` marker within two lines. New working documents
start here and move to `archive/` when their era closes.

## Start here

| doc | what it is |
|---|---|
| [`consuming-ocn.md`](consuming-ocn.md) | **The consumer guide**: joins, transpositions, co-canonicals, recipes (`tools/ocn.py`). Current as of 1.2.0. |
| [`traction-roadmap.md`](traction-roadmap.md) | **The living roadmap** (adopted 2026-07-29): five horizons from private catalogue to public standard. |
| [`ocn-audit-2026-07.md`](ocn-audit-2026-07.md) | The traction-readiness audit (2026-07-29) the roadmap derives from. |
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
| [`ambiguous-alias-decisions.md`](ambiguous-alias-decisions.md) | **Pending**: the 29 aliases equal to another row's canonical name, one recommendation each (H2.6). |

## Attribution system (live)

| doc | what it is |
|---|---|
| [`attribution-batch-engine.md`](attribution-batch-engine.md) | The apply engine: manifest schema, modes, guardrails. |
| [`naming-attribution-automation.md`](naming-attribution-automation.md) | The triage tool — automates triage, not truth. |
| [`naming-attribution-audit-methodology.md`](naming-attribution-audit-methodology.md) | Attribution types A–I, evidence rules. |
| [`attribution-factory-tooling.md`](attribution-factory-tooling.md) | Factory tools built / pending. |
| [`non-person-opening-name-taxonomy.md`](non-person-opening-name-taxonomy.md) | Why non-person names stay unattributed. |
| [`attribution-source-status.tsv`](attribution-source-status.tsv) | The machine-readable evidence registry: grade + citing doc per candidate head. |

## Data directories

| path | what it is |
|---|---|
| [`manifests/`](manifests/) | The applied batch manifests — the change-control record behind every catalogue edit. |
| [`examples/`](examples/) | Worked examples shipped with the consumer guide. |

## Archive

Era-closed working documents live in [`archive/`](archive/). Nothing is
deleted, and the links inside those files stay frozen as they were
written.

- **Applied-lot records.** Every applied batch keeps its dry-run report
  there, marked APPLIED and paired with its manifest in
  [`manifests/`](manifests/): the player-eponym and ECO-A eponym lots,
  the naming-error corrections, the three diacritic tiers, naming
  hygiene, the ECO and phantom-ECO corrections, the duplicate-name
  renames, the American-spelling and Lichess-label alias lots, and
  Allgaier.
- **Superseded planning.** The 0.2-era roadmap and checklists, and
  `post-1.1-roadmap.md`, whose live role passed to
  [`traction-roadmap.md`](traction-roadmap.md).
- **Closed working sets.** The transposition-era trackers, the QID
  migration working set, every applied attribution/naming proposal, and
  the attribution discovery documents (audit backlog, the parked source
  log and sweep, the Group B evidence sprint, the parked French Winawer
  proposal, the whole-catalogue factory map) whose surviving conclusions
  are carried by the catalogue and by
  [`attribution-source-status.tsv`](attribution-source-status.tsv).
