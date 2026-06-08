# Attribution Batch Engine

**Status: TOOLING + DOCS.** Introduces `tools/apply_attribution_manifest.py`,
a deterministic engine that applies an evidence-backed attribution/naming
**batch** from a JSON manifest. **It changes nothing unless `--apply --out`
is passed explicitly**, and it never invents sources or grades evidence.

> **Why it exists.** With 5,899 rows, hand-editing the CSV one attribution at
> a time does not scale and is fragile (a stray quote, a wrong column, an
> already-applied row re-touched). The engine is the **seatbelt** for the last
> step of the naming loop: a workflow finds evidence, a human writes a small
> manifest, and this tool proves — before anything is written — that the batch
> touches only the rows and only the fields it claims to.

## Where it fits — step 4 of the scaled loop

This is the executable form of **step 4** of
[`naming-attribution-automation.md`](naming-attribution-automation.md):

1. **Deterministic triage** — `tools/audit_naming_attribution.py` ranks all
   5,899 rows into category / risk / next-action + eponym head-groups.
2. **Select top groups** — a human picks one homogeneous, high-value group.
3. **Dynamic-workflow evidence search** — parallel read-only agents hunt
   first-hand naming sources for *only* that group; the orchestrator
   re-verifies every slug and every grounded quote.
4. **Apply only CLEAR, homogeneous batches** — the group becomes a manifest;
   `apply_attribution_manifest.py` dry-runs it, a human reviews the row-level
   diff, and **only under an explicit GO** is it applied.

```
evidence sprint  ->  manifest.json  ->  --dry-run (review diff)  ->  GO  ->  --apply --out
```

## Manifest schema (`ocn.attribution_manifest.v1`)

JSON only (no YAML, no comments — use the `description` field for prose):

```json
{
  "kind": "ocn.attribution_manifest.v1",
  "title": "Short human-readable batch title",
  "description": "Optional prose: provenance, scope, GO context.",
  "mode": "attribution_fields_only",
  "expected_catalog_rows": 5899,
  "expected_changed_rows": ["A.Ret", "A.Bir", "A.Lar"],
  "changes": [
    {
      "ocn1": "A.Ret",
      "evidence_grade": "CLEAR",
      "source_refs": ["Hooper & Whyld, Oxford Companion to Chess (1984), entry 'Réti Opening'."],
      "fields": {
        "attributed_to": "Richard Réti",
        "attribution_source": "Hooper & Whyld, Oxford Companion to Chess (1984), entry 'Réti Opening'.",
        "historical_notes": "Named for Richard Réti (1889–1929), who championed 1.Nf3."
      }
    }
  ]
}
```

| Top-level key | Required | Meaning |
|---|---|---|
| `kind` | yes | Must be exactly `ocn.attribution_manifest.v1`. |
| `title` | yes | Non-empty; appears in the report header. |
| `description` | no | Free prose for humans; ignored by the engine. |
| `mode` | yes | Safety mode (see below). |
| `expected_catalog_rows` | yes | Must equal the catalogue's data-row count (stale-manifest guard). |
| `expected_changed_rows` | yes | The exact set of slugs the batch will change. |
| `changes` | yes | One object per row; keys exactly `ocn1`, `evidence_grade`, `source_refs`, `fields`. |

`evidence_grade` and `source_refs` document the provenance of each change.
They are recorded in the report; `--strict` additionally enforces them (below).

A working manifest ships at
[`examples/attribution-manifest.example.json`](examples/attribution-manifest.example.json)
— **example only, not an active proposal.**

## Safety modes

A manifest declares one `mode`. The engine **whitelists** the columns that
mode may change; every other column — including any unknown field name — is
rejected.

| Mode | May change |
|---|---|
| `attribution_fields_only` | `attributed_to`, `attribution_source`, `historical_notes` |
| `naming_strings_only` | `canonical_name`, `aliases`, `notes` + the three attribution fields |

**Always forbidden** (structural / positional identity): `ocn1`,
`moves_uci`, `parent_ocn1`, `depth`, `eco_legacy`, `flags`, `transposes_to`,
`same_as`. These ride a release-boundary migration, never an inline naming
edit (the QID Miles/Petrosian precedent).

## Guardrails (all checked before anything is written)

- **Schema** — catalogue header must be the canonical 14 columns, in order.
- **Stale manifest** — `expected_catalog_rows` must equal the real row count.
- **Slug existence** — every `changes[].ocn1` must exist (case-sensitive).
- **No duplicates** — a slug may appear once in `changes`.
- **Field scope** — every changed field must be allowed by the mode.
- **Exact-change contract** — the set of rows that *actually* differ after
  applying must equal `expected_changed_rows`. A no-op or already-applied
  change is therefore **rejected**, not silently dropped.
- **Attribution pairing** — a non-empty `attributed_to` must travel with a
  non-empty `attribution_source` (the hard rule in `validate.py`); a lone
  `attribution_source` is a warning. We refuse to write a catalogue that
  `validate.py` would then reject.
- **Row count** — output row count must equal input (no adds/deletes in v1).
- **Zero collateral diff** — untouched rows are emitted **byte-for-byte** from
  the source; only changed rows are re-serialised. `git diff` after an apply
  shows exactly the rows the manifest named, and nothing else.

Any failure prints `ERROR: <reason>` to stderr and exits 1 (usage errors exit 2).

## Dry-run workflow (default)

Dry-run is the **default**: with no `--apply`, the engine validates, computes
the result in memory, prints a report, and **writes nothing**.

```bash
python3 tools/apply_attribution_manifest.py \
  --catalog catalog/ocn-1.csv \
  --manifest docs/examples/attribution-manifest.example.json \
  --dry-run --report markdown
```

The report shows the before/after SHA-256, the rows changed, and a field-level
`old -> new` diff for each. Review it before proceeding.

## Apply workflow (explicit GO only)

```bash
# 1. Dry-run and review (above). Then, under an explicit GO:
python3 tools/apply_attribution_manifest.py \
  --catalog catalog/ocn-1.csv \
  --manifest path/to/batch.json \
  --apply --out catalog/ocn-1.csv \
  --strict --validate --report markdown

# 2. Confirm the diff is exactly the intended rows, then validate + audit:
git diff --stat catalog/ocn-1.csv
python3 tools/validate.py --strict-chess catalog/ocn-1.csv
python3 tools/audit_transpositions.py --summary
```

- `--apply` **requires** `--out`. Writing to a fresh path first (e.g.
  `/tmp/ocn-1.next.csv`) and diffing is the safest habit; `--out` may equal
  `--catalog` to write in place, but the engine prints a loud warning when it does.
- `--strict` applies only `CLEAR`, sourced changes (rejects any other
  `evidence_grade` or an empty `source_refs`).
- `--validate` runs `validate.py` (with `--strict-chess` when `--strict` is
  set) on the result and **aborts the apply** if it fails. It runs in a
  temporary directory during dry-run, so dry-run still writes nothing.

## Example commands

```bash
# Dry-run, JSON report (machine-readable diff)
python3 tools/apply_attribution_manifest.py --manifest batch.json --report json

# Strict dry-run with full validation, nothing written
python3 tools/apply_attribution_manifest.py --manifest batch.json --strict --validate

# Apply to a review copy, validate, then diff before promoting
python3 tools/apply_attribution_manifest.py --manifest batch.json \
  --apply --out /tmp/ocn-1.next.csv --strict --validate
diff catalog/ocn-1.csv /tmp/ocn-1.next.csv
```

## Non-goals (v1)

- It does **not** invent, fetch, or grade sources. `evidence_grade` is the
  human's claim; the engine records and (under `--strict`) gates on it.
- It does **not** add or delete rows, and never touches structural columns.
- It does **not** refactor `validate.py`; integration is via subprocess so a
  bug in one cannot corrupt the other.
- It is **not** a substitute for human review under an explicit GO — it makes
  that review fast and trustworthy, it does not replace it.
- No rollback/inversion, no multi-manifest stacking, no apply-history log,
  no non-stdlib dependencies. These are deliberately deferred.

## See also

- [`naming-attribution-automation.md`](naming-attribution-automation.md) — the full loop; this tool is step 4.
- [`naming-attribution-audit-methodology.md`](naming-attribution-audit-methodology.md) — attribution types A–I; the *how* of a single attribution.
- [`agentic-development-playbook.md`](agentic-development-playbook.md) — the GO-gate / verification contract every apply runs under.
