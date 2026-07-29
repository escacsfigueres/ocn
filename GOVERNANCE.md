# OCN governance

This page answers one question: who decides what an opening is called in
OCN, and on what basis.

## The model: a registrar

OCN is run as a **registrar**, not as a committee or a vote. The
registrar is the maintainer of this repository, **Club d'Escacs
Figueres**. One accountable party allocates slugs, sets canonical names,
grades attribution evidence, and resolves conflicts between rows.

A registrar model is deliberate. A naming catalogue needs stable
identifiers and a single consistent editorial hand more than it needs
consensus; what it owes the public in exchange is that every decision is
written down, sourced, and reversible in the open. Full governance
machinery — acknowledgement and decision deadlines, a public decision
log with English summaries, per-release data-quality reports, and
solicited review by an external chess historian and database
practitioner — is roadmap item **H4.5** in
[`docs/traction-roadmap.md`](docs/traction-roadmap.md). What is written
here is the minimum that already holds today.

## Every decision is a record

Nothing changes in the catalogue on a private judgement call. Each
decision leaves one of two artefacts in `docs/`, indexed by
[`docs/INDEX.md`](docs/INDEX.md):

- **Decision records**, for structural or identity questions. Examples:
  [`docs/qid-migration-decision-record.md`](docs/qid-migration-decision-record.md)
  (OCN's first and so far only slug migration),
  [`docs/phantom-and-duplicate-name-decision.md`](docs/phantom-and-duplicate-name-decision.md)
  (path markers blessed in the spec, duplicate names renamed), and
  [`docs/transposition-cleanup-closure.md`](docs/transposition-cleanup-closure.md)
  (closure of the duplicate-FEN layer at `unresolved_groups=0`).
- **Dry-run records**, for every applied batch of catalogue edits: the
  engine report reviewed before the write, kept afterwards and marked
  APPLIED. Examples:
  [`docs/archive/lot-a-player-eponyms-dry-run.md`](docs/archive/lot-a-player-eponyms-dry-run.md)
  and
  [`docs/archive/naming-error-corrections-record.md`](docs/archive/naming-error-corrections-record.md).

The mechanism that produces those records, and the guarantees it
enforces, are described in [`CONTRIBUTING.md`](CONTRIBUTING.md) and
[`docs/attribution-batch-engine.md`](docs/attribution-batch-engine.md).
The rule for contributors and registrar alike is the same: the catalogue
CSV is never hand-edited.

## Slugs are stable keys

An OCN slug is an identifier, not a description that must stay in
fashion.

- **Slugs are never reused.** A retired slug does not come back pointing
  at a different position.
- **A wrong display name does not change the slug.** Names, aliases and
  notes are corrected in place; the slug stays. Two rows in the
  catalogue carry tokens that no longer match their corrected names,
  by design.
- **A wrong slug is retired, not silently repointed.** The recovery
  mechanism in [`spec/OCN-1.md`](spec/OCN-1.md) is the `deprecated` flag
  plus a new entry. Where an identity genuinely has to move, it rides a
  release-boundary migration with a decision record, never an inline
  edit; the QID migration is the worked precedent.
- **Structural columns are release-boundary business.** `ocn1`,
  `moves_uci`, `parent_ocn1`, `depth`, `eco_legacy`, `flags`,
  `transposes_to` and `same_as` are refused by the batch engine in every
  editing mode.

Consumers can therefore treat a slug as a durable join key, and treat
`canonical_name` as the thing that may improve.

## Disputes are resolved on written evidence

A dispute is decided by what a source says, not by how widely a belief
is held. In descending weight: a reference-grade work read first-hand; a
credible secondary attestation; a dated game in a verifiable corpus,
which establishes chronology only. Grades and the retraction policy are
in [`CONTRIBUTING.md`](CONTRIBUTING.md).

For conflicts between rows rather than between sources — two slugs
claiming the same position, or a name pulled between two families — the
normative doctrine is the **Canonicalisation arbitration** section of
[`spec/OCN-1.md`](spec/OCN-1.md). Its rules are ordered and applied in
order; the registrar states which rule decided the case. In particular:

- **Rule 1, established name beats descriptor.** A literary opening name
  outranks a path descriptor or an imported label restating a parent.
- **Rule 2, spec-governed structural classes win.** Where the spec
  already writes a class rule, the slug matching that rule is canonical.
- **Rule 7, ECO is evidence, not authority.** ECO codes inform the
  choice, but ECO is a flat 1971 classification with known coarseness.
  Where ECO and a stronger rule disagree, the stronger rule wins, and
  the ECO observation is recorded in `eco_legacy` and `notes` rather
  than in the canonical slug choice.

The same section lists the groups that must **not** be resolved
automatically — competing literary identities, cases where a name would
disappear entirely, groups whose rows both have substantive children.
Those go to human review before any arrow is written.

Disputes that survive all of this are decided by the registrar, in
writing, with the losing argument recorded alongside the winning one.

## Scope and appeal

The registrar decides the catalogue and the specification. It does not
decide what anyone else calls an opening: OCN is a layer over ECO and
the established literature, never a replacement for either, and the
`aliases` column exists so that a name we did not make canonical is
still findable.

If you believe a decision is wrong, reopen it with a source. That is the
whole appeal procedure, and it is the only one that has ever changed an
OCN row.
