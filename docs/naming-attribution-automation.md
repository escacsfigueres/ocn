# Naming / attribution audit — automation (post-1.1)

**Status**: **TOOLING + DOCS.** Introduces `tools/audit_naming_attribution.py`,
a deterministic triage tool. **It changes nothing in `catalog/ocn-1.csv`**
and never writes attribution fields or invents sources.

> **The scaling principle: automate triage, not truth.** With 5,899 rows,
> "one name → one proposal → one apply" does not scale. So a script decides
> *which rows are candidates*, *what kind of name each has*, *whether the
> attribution fields are already populated*, *whether a row is a family
> head*, and *whether a surname carries multi-opening risk*. Humans still
> decide the **truth** — and only on `CLEAR`, source-backed batches. The
> tool moves the cullereta (one-spoonful-at-a-time) bottleneck off the
> human and onto deterministic code.

## What the tool does

`tools/audit_naming_attribution.py` reads the catalogue and, for every row,
emits:

- `ocn1`, `canonical_name`, `eco_legacy`, `parent_ocn1`, `depth`
- `has_children` — is this slug a parent of any row
- `head_candidate` — does the row *introduce* its name (vs inherit a
  surname from its parent head)
- `attribution_fields_state` — compact mask of which of
  `attributed_to` / `attribution_source` / `historical_notes` are populated
  (e.g. `ASH`, `A-S`, `---`)
- `detected_tokens` — which seed tokens fired (e.g. `person:winawer`,
  `geo:french`, `descr:main line`)
- `category` — the naming **basis**:
  - `already_attributed`
  - `likely_person_eponym`
  - `likely_place_or_event`
  - `editorial_descriptor`
  - `metaphor_or_animal`
  - `gambit_or_tactic`
  - `unknown_or_mixed`
- `risk_level` — `low` / `medium` / `high`
- `recommended_next_action`:
  - `already_done` — fields already populated
  - `ignore_descriptor` — Type-H descriptor / metaphor / gambit / geo
    family / inheriting child; permanently or trivially unattributed
  - `source_sprint` — a recognised eponym head or event token needing one
    first-hand naming source before anything is written
  - `individual_proposal` — a **multi-opening (DANGEROUS) surname**; must
    be attributed one specific head at a time, never as a batch
  - `batch_candidate` — an eponym head whose family already contains an
    attributed sibling (the in-family template exists) — the strongest,
    most homogeneous batch target once sourced
- `reason` — one-line justification

It also groups person-eponym **head candidates** by surname
(`eponym_head_groups` in JSON / the markdown report), so a source sprint
can target a whole homogeneous group at once.

### Classification precedence

Existing attribution wins first (`already_attributed`). Then person eponym
> event/venue > metaphor > gambit/tactic > geographic family > editorial
descriptor > unknown. A surname therefore beats the geographic family
token in its name (`French, Winawer` → person, not place).

### Seed knowledge

The token lists are **small, curated, and editable**, derived from the
existing audit docs:

- **DANGEROUS surnames** (multi-opening, never blanket): Tarrasch,
  Rubinstein, Steinitz, Marshall, Chigorin, Bogoljubow — from the surname
  risk map in
  [`player-eponym-attribution-batch-proposal.md`](archive/player-eponym-attribution-batch-proposal.md).
- **Moderate surnames** (recognised single-/few-head eponyms): Alekhine,
  Nimzowitsch, Grünfeld, Réti, Winawer, Trompowsky, Rossolimo, Maróczy,
  Alapin, Taimanov, … (diacritics normalised).
- **Geo-family / event-venue / descriptor / metaphor / gambit** tokens —
  from [`non-person-opening-name-taxonomy.md`](non-person-opening-name-taxonomy.md).

These lists are **not exhaustive**. The long tail of minor surnames
(Cozio, Worrall, Knorre, Stoltz, Glek …) is deliberately out of scope;
extend the seed lists as sprints surface new heads.

## What the tool does NOT do

- It does **not** edit `catalog/ocn-1.csv` (a test asserts the file's
  hash is unchanged after a run).
- It does **not** write `attributed_to` / `attribution_source` /
  `historical_notes`.
- It does **not** invent, fetch, or grade sources. A `source_sprint` /
  `batch_candidate` label means *"a human + a first-hand source decides
  this"*, never *"this is true."*
- It does **not** rank reliability of names — only the *basis* of the
  name and the *state* of the fields.

## How to run it

```bash
# Compact summary (counts by category / action / risk) to stderr
python3 tools/audit_naming_attribution.py --summary

# Full per-row TSV to stdout (or --out path)
python3 tools/audit_naming_attribution.py
python3 tools/audit_naming_attribution.py --out /tmp/naming-triage.tsv

# Human-readable map (summary tables + top eponym groups + sprint list)
python3 tools/audit_naming_attribution.py --format markdown | less

# Machine-readable (rows + eponym_head_groups)
python3 tools/audit_naming_attribution.py --format json

# Slice the map
python3 tools/audit_naming_attribution.py --action source_sprint --head-only
python3 tools/audit_naming_attribution.py --category likely_person_eponym
```

## How it fits with dynamic workflows

The tool is step 1 of the scaled loop; dynamic workflows are step 3:

1. **Deterministic triage** — `audit_naming_attribution.py` produces the
   prioritized map (this script; no GO needed, read-only).
2. **Select top groups** — a human picks the highest-value
   `source_sprint` / `batch_candidate` eponym groups (e.g. one surname
   group, or one event token) — the *homogeneous evidence-backed batch*,
   not a cullereta.
3. **Dynamic-workflow evidence search** — parallel read-only agents hunt
   first-hand naming sources for **only those groups**; the orchestrator
   re-verifies every slug and every grounded quote (the discipline that
   caught the "Paris 1878" fabrication).
4. **Apply only CLEAR, homogeneous batches** — head rows only, strings in
   `attributed_to` / `attribution_source` (+ `historical_notes`), with a
   row-level diff vs `origin/main` and full validation, under an explicit
   GO. PARTIAL items stay parked; a "no batch" negative result is itself
   valuable knowledge.

The tool makes step 2 cheap and repeatable: instead of eyeballing 5,899
rows, a human reads a ranked map and points the workflow at the next
homogeneous group.

## See also

- [`naming-attribution-audit-methodology.md`](naming-attribution-audit-methodology.md) — types A–I; the *how* of a single attribution.
- [`naming-attribution-audit-backlog.md`](naming-attribution-audit-backlog.md) — the discovery backlog this tool generalises.
- [`player-eponym-attribution-batch-proposal.md`](archive/player-eponym-attribution-batch-proposal.md) — the surname risk map the DANGEROUS seed list comes from.
- [`non-person-opening-name-taxonomy.md`](non-person-opening-name-taxonomy.md) — the descriptor/metaphor/gambit token taxonomy.
- [`parked-attribution-reference-source-log.md`](parked-attribution-reference-source-log.md) — the 4 CLEAR / 2 PARTIAL source-access result the next sprint builds on.
- [`agentic-development-playbook.md`](agentic-development-playbook.md) — the GO-gate / verification contract every apply runs under.
