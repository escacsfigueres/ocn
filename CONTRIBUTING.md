# Contributing to OCN

OCN is a naming catalogue before it is a piece of software, so the most
valuable contributions are usually reports and evidence rather than
patches: a canonical name that is wrong, an attribution that no source
supports, an ECO mapping that does not match the position, a lookup that
returns nothing when it should.

Two rules cover almost everything:

1. **Do not open a pull request against `catalog/ocn-1.csv`.** Catalogue
   rows are never hand-edited, not even by the maintainer. Open an issue
   instead.
2. **A naming claim travels with its source.** "Everyone knows this" is
   not an argument here. A book, an encyclopaedia entry, an article, or
   a dated game is.

## Reporting an error or proposing a change

Open an issue with one of the two templates:

- **Naming dispute** — a canonical name, an alias, or an attribution is
  wrong or unsupported. Give the slug, the name you believe is correct,
  the written source (author, work, year, page or URL), and which field
  is wrong.
- **Data error** — a field is wrong or a tool misbehaves: ECO codes,
  moves, parent, flags, `transposes_to` / `same_as`, a failing lookup.
  Give the slug or slugs, the field, expected versus actual, and the
  command that reproduces it.

Anything else (a question, a spec ambiguity, a tooling idea) is a plain
issue.

## How a catalogue change actually lands

Every catalogue change rides a JSON manifest
(`ocn.attribution_manifest.v1`) through the batch engine,
[`tools/apply_attribution_manifest.py`](tools/apply_attribution_manifest.py),
documented in
[`docs/attribution-batch-engine.md`](docs/attribution-batch-engine.md).
The manifest declares, before anything is written, which rows change,
which fields may change, the evidence grade, and the source behind each
change.

```
issue + evidence  ->  manifest.json  ->  dry-run (reviewed, recorded)  ->  GO  ->  apply
```

The engine refuses the batch unless all of these hold:

- **Field scope** — the manifest's mode whitelists the columns it may
  touch (the three attribution fields, or naming strings plus those).
  Structural columns — `ocn1`, `moves_uci`, `parent_ocn1`, `depth`,
  `eco_legacy`, `flags`, `transposes_to`, `same_as` — are never writable
  by an inline edit; they ride a release-boundary migration with its own
  decision record.
- **Exact changed rows** — the set of rows that actually differ after
  applying must equal the set the manifest declared. A no-op, an
  already-applied row, or one row too many aborts the run.
- **Zero collateral diff** — untouched rows are re-emitted byte for
  byte, so `git diff` shows exactly the declared rows and nothing else.
- **Stale-manifest guard** — the declared catalogue row count must match
  the live one.
- **Attribution pairing** — a non-empty `attributed_to` must travel with
  a non-empty `attribution_source`, the same rule `tools/validate.py`
  enforces.

Dry-run is the default. With no `--apply`, the engine validates,
computes the result in memory, prints the before and after SHA-256 plus
a field-level `old -> new` diff for every changed row, and writes
nothing. Applying is a separate, explicit step, and it can be told to
run the validator on the result and abort if it fails.

Every applied lot leaves its dry-run report in `docs/`, marked APPLIED,
beside the manifest that produced it (the applied-lot list is in
[`docs/INDEX.md`](docs/INDEX.md)). Those records are permanent: what was
proposed, what the engine predicted, and what the catalogue looked like
before and after.

**Why this instead of ordinary pull-request review.** A reviewer reading
a CSV diff can confirm that the visible lines look plausible. They
cannot confirm that nothing else moved, that the batch was not applied
twice, that only the intended columns were touched, or that the result
still validates. The engine proves all of that mechanically before the
write happens, and the resulting report is reviewable by someone who has
never opened the CSV. A hand-made CSV diff bypasses the whole mechanism,
which is why it is not accepted, however correct its content.

## Evidence and grades

Attribution claims carry an evidence grade:

| Grade | Bar | Effect |
|---|---|---|
| `CLEAR` | A reference-grade source, read first-hand: a book, monograph, or encyclopaedia entry that states the naming. | Publishable; may be applied. |
| `PARTIAL` | Credible secondary or web attestation, corroborating but not reference-grade. | Recorded and parked; rejected by the engine's `--strict` mode. |

Two working rules stand behind the grades:

- **A game database proves that a line was played and when. It never
  proves what the line is named after.** Chronology supports a claim; it
  does not establish one.
- **First-hand reads only.** A summary of a source is not the source.

**Retraction is part of the process, not an embarrassment.** It has
already happened once in public: a search summary paraphrased Edward
Winter as saying the Winawer was named after a game at "Paris 1878", a
first-hand read of Winter's actual page showed the sentence is not
there, the claim was never encoded in the catalogue, and the finding is
written up in
[`docs/archive/parked-naming-audit-source-sweep.md`](docs/archive/parked-naming-audit-source-sweep.md).
If you find a row whose `attribution_source` does not say what the row
claims it says, that is a first-class bug report. File it as a naming
dispute; the row will be downgraded or withdrawn, in public, with a
record.

## Code contributions

Pull requests against `tools/` are welcome, with tests.

- Tests live in `tools/tests/`. Run
  `python3 -m unittest discover -s tools/tests`.
- The catalogue must stay green:
  `python3 tools/validate.py --strict-chess`.
- If you touch documentation, run the slug gate:
  `python3 tools/verify_doc_slugs.py README.md docs/*.md`. Every
  backtick-quoted OCN slug in the docs must exist in the live catalogue;
  intentional historical slugs carry a `NON-CATALOGUE` marker.
- Standard library only. The tools have no third-party runtime
  dependencies and should keep none.
- CI runs the same checks on Python 3.10, 3.11 and 3.12.

Code you contribute is accepted under the MIT licence
([`LICENSE-CODE`](LICENSE-CODE)); catalogue and specification material
under CC-BY-4.0 ([`LICENSE-SPEC`](LICENSE-SPEC)).

## What cannot be accepted

- Hand edits to `catalog/ocn-1.csv`, for the reasons above.
- An attribution with no checkable source, or a citation pointing at
  unpublished or private material. An uncheckable citation is worse than
  an empty field: it turns missing data into apparent fabrication.
- Bulk text copied from a copyrighted work. Short quoted snippets that
  carry a specific claim are fine and expected.
- A slug rename offered as a fix. Slugs are stable keys and are not
  corrected when a name changes; see [`GOVERNANCE.md`](GOVERNANCE.md).

## What to expect

OCN is maintained by one club, with agent-assisted workflows. Issues are
read and answered on a best-effort basis; there is no response-time
commitment yet. Formal turnaround targets, a public decision log, and
solicited expert review are roadmap item H4.5 in
[`docs/traction-roadmap.md`](docs/traction-roadmap.md).
