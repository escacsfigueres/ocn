# Attribution factory tooling

**Status: TOOLING + DOCS.** The first automation layer from
[`whole-catalogue-attribution-factory-map.md`](whole-catalogue-attribution-factory-map.md).
Three small stdlib-only tools that make attribution lots faster and safer to
build. **None of them edits `catalog/ocn-1.csv` or applies anything** — they
prepare and verify the inputs that the
[Attribution Batch Engine](attribution-batch-engine.md) then dry-runs and applies
under an explicit GO.

```
slice  ->  human fills sources  ->  scaffold  ->  human fills field values  ->  engine --dry-run  ->  GO --apply
```

## The three tools

### 1. `tools/candidate_slice_export.py` — pull a review slice

Export the review-relevant columns for a set of rows, in deterministic
catalogue order. Base set = explicit slugs (or ALL rows if none); `--eco-prefix`
and `--empty-attribution` then narrow it (logical AND).

```bash
# all unattributed ECO-A rows (1,309 of them), review columns:
python3 tools/candidate_slice_export.py --eco-prefix A --empty-attribution

# a specific reviewed set, custom columns, JSON:
python3 tools/candidate_slice_export.py --ocn1 A.Ret --ocn1 A.Bir \
    --columns ocn1,canonical_name,attributed_to --format json
```

Flags: `--catalog`, `--ocn1` (repeatable), `--ocn1-file` (one slug/line, `#`
comments and blanks skipped), `--eco-prefix A|B|C|D|E`, `--empty-attribution`,
`--columns` (default: the 9 attribution-review columns), `--format csv|json`,
`--out`, `--allow-missing`. Missing slug → exit 1 (or a `WARN:` + skip under
`--allow-missing`); unknown column → exit 2; an empty slice is success (exit 0).

### 2. `tools/scaffold_attribution_manifest.py` — build a manifest skeleton

Turn a reviewed slug list into an `ocn.attribution_manifest.v1` skeleton. The
field values are **empty strings**: the skeleton is *structurally* valid (the
engine's `validate_manifest` accepts it) but the engine **rejects it in dry-run
as a no-op** until a human fills real values. So "fill before apply" is enforced
by the engine, not left to discipline.

```bash
python3 tools/scaffold_attribution_manifest.py \
    --title "Lot 3 — ECO-A eponym heads" --mode attribution_fields_only \
    --ocn1 A.Ret --ocn1 A.Bir --ocn1 A.Lar --ocn1 A.Gro \
    --evidence-grade PARTIAL --out docs/manifests/lot-3.manifest.json
```

It computes `expected_catalog_rows` live, sets `expected_changed_rows` to the
slugs in catalogue order, and writes an empty `fields` skeleton for the mode's
columns. It **never guesses field values**, and **refuses by default to scaffold
an already-attributed slug** (an empty-field skeleton would *clear* it on apply)
— `--allow-attributed` overrides with a loud `WARN:`. Missing/duplicate slug →
exit 1; bad `--mode`/`--evidence-grade` → exit 2.

### 3. `tools/verify_doc_slugs.py` — keep docs honest

Verify every backtick-quoted OCN slug in docs against the live catalogue, so
`docs/` stays a reliable agent-context source.

```bash
python3 tools/verify_doc_slugs.py docs/*.md          # exit 1 if any stale slug
python3 tools/verify_doc_slugs.py --format json docs/my-new-doc.md
```

It only considers tokens that match the slug shape `^[A-E](\.[A-Za-z0-9_=-]+)*$`
(so git hashes, ECO codes like `A45`, versions, `--flags`, filenames, and
commands are ignored), skips field-accessor notation (`A.Tro.notes`), and
honours a `NON-CATALOGUE` / `pseudo-slug` exemption with a 2-line lookback (the
marker may sit on a preceding line). Reports `file:line: stale slug` and exits 1;
zero files matched → exit 1 (never a silent green).

## Worked workflow

```bash
# 1. Export the candidate slice for review.
python3 tools/candidate_slice_export.py --ocn1 A.Ret --ocn1 A.Bir \
    --ocn1 A.Lar --ocn1 A.Gro --out /tmp/lot3.review.csv
#    -> a human fills attributed_to / source / notes from a first-hand source.

# 2. Scaffold the manifest skeleton.
python3 tools/scaffold_attribution_manifest.py --title "Lot 3 — ECO-A heads" \
    --mode attribution_fields_only --ocn1 A.Ret --ocn1 A.Bir --ocn1 A.Lar \
    --ocn1 A.Gro --out docs/manifests/lot-3.manifest.json
#    -> a human pastes the reviewed values into each change's empty fields,
#       and sets evidence_grade=CLEAR once sourced.

# 3. Dry-run with the engine (rejects the unfilled skeleton; passes once filled).
python3 tools/apply_attribution_manifest.py --manifest docs/manifests/lot-3.manifest.json \
    --dry-run --strict --report markdown

# 4. Review the row-level diff, then under an explicit GO:
python3 tools/apply_attribution_manifest.py --manifest docs/manifests/lot-3.manifest.json \
    --apply --out catalog/ocn-1.csv --strict --validate
```

A freshly-scaffolded skeleton run through step 3 reports
`ERROR: changed rows do not match expected_changed_rows — expected to change but
did not (no-op)` — the intended "you have not filled the values yet" gate.

## Current docs health

Running `verify_doc_slugs.py docs/*.md` today reports **90 stale slug references
across 14 files** — pre-existing residue from past slug migrations (QID, the
transposition cleanup), not introduced here. They are logged for a dedicated
cleanup pass (see the factory map's risk register); this sprint's new docs are
clean.

## Non-goals

- No tool edits `catalog/ocn-1.csv` or applies a manifest — that is the engine's
  job, under a GO.
- Scaffold never invents attribution text; it produces an empty, un-appliable
  skeleton on purpose.
- The slug verifier does not fix stale references, only reports them.
- Stdlib only; no new dependencies.

## See also

- [`whole-catalogue-attribution-factory-map.md`](whole-catalogue-attribution-factory-map.md) — the lots and tooling backlog these tools begin.
- [`attribution-batch-engine.md`](attribution-batch-engine.md) — the engine these tools feed.
