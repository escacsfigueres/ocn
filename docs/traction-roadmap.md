# OCN traction roadmap — from private catalogue to public standard

**Status: live.** Adopted 2026-07-29 from the findings in
[`ocn-audit-2026-07.md`](ocn-audit-2026-07.md). Supersedes the traction-facing
ambitions of [`archive/post-1.1-roadmap.md`](archive/post-1.1-roadmap.md) (whose Track 1
attribution work continues here as D-1, and whose Track 2 i18n work is
rescoped as G-1). Every mutating step below runs under the usual GO gates
([`agentic-development-playbook.md`](agentic-development-playbook.md));
catalogue changes ride the manifest engine, never hand edits.

## Positioning (governs everything)

**OCN is the missing hierarchy layer over ECO and the Lichess names — never a
replacement for either.**

> ECO gives you `B90`. Lichess gives you a 60-character string. Neither gives
> you the tree. OCN is `B.Sic.Naj.Eng` — machine-readable parents,
> transposition canonicalisation, keyed 1:1 to both.

The historical precedent (NIC-Key, the 1990s mnemonic ECO alternative) failed
on proprietariness and distribution, not on mnemonics. Therefore this roadmap
is distribution-first: the catalogue's quality already exists; nobody can see
it.

Scope constraints: `chess-parquet` stays private — OCN decouples from it
(H0.5, H2.8) and drops the parquet from its own releases. Solo maintainer plus
agentic workflows; phases are sized as agent-executable batches, one GO per
landing.

## North stars per horizon

| Horizon | The bar |
|---|---|
| H0 | Survives 5 minutes of hostile public scrutiny |
| H1 | `pip install ocn-chess` works on a clean machine |
| H2 | A stranger annotates their own PGN in under 5 minutes; the spec accepts 100% of its own catalogue |
| H3 | Announcement clicks do not bounce |
| H4 | At least one external integration exists; top-100 eponyms attributed and graded |

---

## Horizon 0 — Public-ready gate (~1-2 weeks; everything here blocks the flip)

The repo will be judged in its first 5 minutes: README, one link click, a
glance at `docs/`, a spec claim checked against the data. Each step currently
has a landmine.

| ID | Item | Effort | Done when |
|---|---|---|---|
| H0.1 | **Resolve PR #1.** Merge the ship-ready ~60% (CI byte-compile glob + guard test, README truth to 1.2.0, four tested tools). Convert the inert drafts (attribution manifests, fr/de seeds) into labelled issues; close the branch. Apply the Allgaier manifest (`C.KGm.Acc.All`) — launching with the flagship rigour policy having zero applied results is self-refuting. | M | 0 open PRs; drafts tracked as issues; CI green; Allgaier row live. |
| H0.2 | **README truth pass.** Fix the 5 broken links and the 1.1.0 badge/status; **delete the false "OCN keeps ECO classes unchanged" claim** and replace it with an honest class-divergence paragraph (13.8%, link to the H2.5 table); remove all references to the private chess-parquet repo and its parquet artefact; collapse the 16-tool CLI catalogue into two short sections (consumer / maintainer). | S | Every README link resolves; every quantitative claim verifiable against the catalogue; no private-repo references. |
| H0.3 | **Spec triage patch (not the full ABNF).** Promote the real grammar (class, named tokens, SAN tail) from the `validate.py` comment into the spec prose; acknowledge the depth-cap saturation; create `spec/errata.md` with E-001 (the QID slug re-point, referencing [`qid-migration-decision-record.md`](qid-migration-decision-record.md)) and the corrective policy; extend spec history to 1.2.0; declare the test fixtures the provisional conformance corpus. | S | A parser written from spec prose accepts all 5,899 rows; a reader who diffs spec vs catalogue finds every discrepancy already acknowledged. |
| H0.4 | **Attribution hygiene.** Re-source or withdraw every "the corpus" citation (unverifiable is worse than absent); fix the 3 byte-identical source strings; add a validator check banning unverifiable source patterns. | S | Zero rows cite unpublished sources; validator enforces it. |
| H0.5 | **EFCDB decoupling (spec side).** Demote the EFCDB reference to informative; add a normative "Position identity" annex to `spec/OCN-1.md` inlining the zobrist scheme parameters OCN needs. | M | No normative dependency on unpublished documents; position keys computable from OCN-1 alone. |
| H0.6 | **Minimum governance surface.** `CONTRIBUTING.md` + one-page `GOVERNANCE.md` in English (registrar = maintainer; manifest engine described as the change-control asset it is; decisions logged); two issue templates (naming dispute, data error); `CITATION.cff` bumped. | M | An outsider can answer "who decides names and how do I dispute one" in one click. |
| H0.7 | **Docs triage.** `git mv` the ~34 process files (11k lines of dry-run logs, applied-lot records) under `docs/archive/`; drop the release suffix from the consumer guide's filename (now `consuming-ocn.md`); INDEX updated. | S | `docs/` top level is short enough to scan and the first thing a newcomer opens is the consumer guide. |
| H0.8 | **Flip public** (major GO) + tag `ocn-1.2.1` with all of the above; enable the Zenodo webhook *before* tagging; set topics, About, social preview. | S | Repo public; release visible; webhook armed. |

Explicitly *not* blocking the flip: the full ABNF, attribution scale-up,
editorial cleanup, new columns, i18n. Labelled imperfection is what
standards-grade looks like; silent contradiction is what gets punished.

## Horizon 1 — Exist and install (~2-3 weeks)

| ID | Item | Effort | Done when |
|---|---|---|---|
| H1.1 | **pip package `ocn-chess`** (register the name the day of the GO; assume `ocn` is taken/squattable). Data ships inside the wheel (CSV + xref + prebuilt positions index) like tzdata. The reader grows `by_name`, `by_eco`, `by_position`, `parents()`, `children()`, `version()`, typed rows; O(1) position lookup via the bundled index; **the python-chess en-passant adapter built in** (silent-zero-matches is a traction bug); a single `ocn` CLI with `--help` subsuming the five help-less tools; FEN counter fix. | L | `pip install ocn-chess` then `ocn lookup B90` works on a clean machine; a python-chess `Board` round-trips to a match. |
| H1.2 | **Whole-catalogue `ocn-1.json`** with `moves_san` derived at build time (the canonical CSV is not touched). Feeds the explorer, HF, and any JS consumer. | S | Attached to releases; schema in the consumer guide. |
| H1.3 | **Release automation.** Tag push runs validator + tests, builds CSV/JSON/positions/checksums, attaches to the release. Parquet is dropped. | M | A tag produces a complete release with zero manual steps. |
| H1.4 | **Zenodo DOI + HuggingFace dataset card.** First automated release mints the DOI; DOI lands in CITATION.cff and README; HF card built from the JSON. | S | DOI resolves; `datasets.load_dataset` works. |
| H1.5 | **Scalar ECO join table** `catalog/ocn-1.eco.tsv` (slug, eco, seq), keeping `eco_legacy` as legacy; spec Goal 3 restated honestly (299 no-ECO rows are Lichess long-tail beyond ECO's coverage). | M | Consumers join ECO without splitting pipes; no false universal claim remains. |

## Horizon 2 — Prove it (~3-4 weeks; H2.4-H2.6 must land before the announcement)

| ID | Item | Effort | Done when |
|---|---|---|---|
| H2.1 | **PGN annotator**: `ocn annotate games.pgn` adds `[OCN]`/`[OCNName]` tags, deepest-match, transposition-aware; prints classification stats. Then the headline number: run it over ~1M Lichess games and publish "OCN classifies X% of real games" with a reproducible script. | M | A 1,000-game file annotates in seconds; the coverage stat is in the README. |
| H2.2 | **Five-minute quickstart** at the top of the README and the consumer guide, doctest-run in CI so copy-paste always works. | S | CI executes the quickstart verbatim. |
| H2.3 | **Web explorer MVP** on the existing Vercel project (static, no backend, eats `ocn-1.json`): searchable A-E tree (name, alias, slug, ECO); row pages with the breadcrumb (the money shot), SAN line, static SVG board, ECO and Lichess names, link to Lichess analysis; an ECO-to-OCN converter box (the most shareable widget); boilerplate notes and synthetic aliases suppressed from display; deep links per slug. | L | A slug URL deep-links to a row page with breadcrumb and board; search answers in under 100ms. |
| H2.4 | **Spec 1.3 — the standards release.** Normative ABNF (RFC 5234), *spec bends to data*, two-layer model: stable grammar (major-versioned) vs catalogue profile (minor-versioned; 1.x profile cap stays 7 segments). Token-ambiguity rule: the move tail is the maximal SAN-parsing suffix; newly minted named tokens must not be SAN-shaped (grandfather table for existing ones). Conformance section + RFC 2119 (Producer / Consumer / Validator classes). String canonicalisation section (NFC, diacritics, ASCII-fold search) promoting the diacritic map to an annex. Open flags registry + `x-` private prefix + locale sidecar registration. Versioning 2.0 with field-level change classes (retroactively legalising the 1.2.0 mass rename, cited as precedent). Deprecation lifecycle with a real worked example: `A.Hol` migrates to <!-- NON-CATALOGUE: proposed successor slug --> `A.Dut` (the one token violating the spec's own rule); Chi/Cha/Sch/RyL do **not** migrate — tokens are redefined as subtree-local labels, person identity lives in attribution data. Conformance corpus grows to ~100 normative cases. | L | ABNF validates 100% of rows (new CI test); a from-spec reimplementation agrees with `validate.py` on every fixture. |
| H2.5 | **Classification honesty.** Derived sidecar `catalog/ocn-1.eco-divergence.tsv` (CI-regenerated, validator-checked); normative exception list in the spec with written rationales for the French (the stress test: if it cannot be written convincingly it is the *only* reversion candidate, and only ever in a 2.0), London/Colle, and the misc rows; a "consuming OCN from ECO-keyed systems" migration section. Position: revert nothing. | M | All 770 divergent rows listed with resolving rationale refs; README paragraph links here. |
| H2.6 | **Minimum editorial pass before the announcement.** Delete the 1,726 "(SAN) Line" aliases and 398 bare "Main Line" aliases (patch-level under the new versioning; a skeptic smells padded data in two minutes); resolve all 29 canonical-name/alias collisions; finish the American-spelling lot. Notes are *not* mass-rewritten: they get a generated/curated provenance label (D-3) and improve gradually with D-1. | M | Name search returns no synthetic noise; name-to-slug lookup unique or flagged; validator prevents recurrence. |
| H2.7 | **Popularity sidecar** `catalog/ocn-1.popularity.tsv` (games, W/D/L from the Lichess explorer API; masters + lichess pools), independently refreshable. Turns the taxonomy into a map — explorer sorts by it. Soft gate: ships as explorer v1.1 if it slips; does not delay H3. | M | Tree default-sorted by games played. |
| H2.8 | **Positions sidecar completed** (`export_positions.py` grows): SAN movetext, EPD, corrected FEN, **Polyglot zobrist computed in Python in-repo** (completes the chess-parquet decoupling), and a `mainline` SAN continuation for leaf rows — the answer to "ECO main lines run 20-24 plies" as data, not as deeper slugs. **Landed except `mainline`, which needs H2.7's popularity ranking to be a fact rather than an opinion and ships with it.** | M | One regenerable artefact carries every derived per-row field; local tools consume it instead of recomputing. |

## Horizon 3 — Announce (~1-2 weeks, deliberate order)

Gate: pip installs, quickstart doctest green, explorer deep-links resolve, the
spec parses its own catalogue, DOI minted.

1. **r/chessprogramming + TalkChess** — the technical story (hierarchy,
   canonicalisation, ABNF, the annotator). They will find bugs; that is the
   point. Fix for a week.
2. **Lichess forum** — tribute framing, never replacement: built on
   lichess-org/chess-openings (CC0), 1:1 xref, 91.7% exact coverage, every
   explorer line links back to Lichess analysis.
3. **r/chess** — lead with the explorer and the ECO converter, not the spec.
4. **Show HN** — "OCN: a hierarchical naming layer over chess opening codes".
   The HN story is dataset engineering + honest governance + the NIC-Key
   lesson (tried commercially in the 90s, died of proprietariness; this is the
   open version).
5. **chessprogramming wiki** — an encyclopedia entry after the dust settles,
   citing the DOI and the stable spec.

One story everywhere, different depth: *the missing hierarchy layer over ECO
and the Lichess names.*

## Horizon 4 — Grow (continuous, post-announcement)

| ID | Item | Effort | Notes |
|---|---|---|---|
| H4.1 | **Permission-free wedges first**: `ocn export --format pgn-extract` and `--format scid` eco-files. Two decades-old tools consume these without a single upstream change. Can be pulled forward into H2. | S-M | The sleeper wedge. |
| H4.2 | **En Croissant**: file the issue with the mapping file and JSON attached — arrive with the work done. | M | Small active team, feature-hungry. |
| H4.3 | **lichess-org/chess-openings upstream PR** (an `ocn` column) — only after stars/DOI/HN exist, framed as "1:1 mapping, we maintain it, CI-verified against your releases". The standalone xref already serves the need; the PR is upside, not dependency. | M | Highest leverage, last in line. |
| H4.4 | **Attribution top-100 sprint** (the moat). Unblock the policy: publish PARTIAL with an explicit `evidence_grade` (verified / attested / traditional / disputed); `--strict` becomes a grade-integrity gate, not a suppression gate. Structured source sidecar `catalog/ocn-1.sources.tsv` (claim type, person, role enum, source type, author, year, work, page, ISBN/URL, grade, retrieved date); per-row provenance published from the manifest history that already exists (D-3). Six-month target: the ~100 most-played eponyms (ranked by H2.7) attributed and graded, at least 40 at verified grade — "every opening you have actually heard of has a sourced, graded attribution". Opens as the community-contribution surface (good-first-issue farm). | L | Longest-running stream; starts as soon as the grading policy lands. |
| H4.5 | **Full governance**: registrar-with-public-log model (acknowledge within 14 days, decide within 60); public decision-record index with English summaries; a per-release public data-quality report (publishing your own worst numbers is the strongest credibility signal available — the 360-audit machinery already exists); solicited expert review by one chess historian and one database practitioner, published with responses. | M | This is how "reference dataset" status is actually conferred. |
| H4.6 | **i18n rescoped** (off the traction path, not deleted): declared core tier = 100% of depth 0-2 rows per shipped language; vocabulary-table derivation (~80-120 structural terms per language) for template-shaped names; ca/es completed to tier before adding languages; fr/de merge only with native-reviewer sign-off. Claim nothing beyond declared coverage. | M | Locale data doubles as a QA instrument (the `A.Hol` finding came from locale leakage). |

## Explicit cuts

| Cut | Why |
|---|---|
| npm/TS package | The explorer eats static JSON; ship npm only when a real JS consumer asks. |
| Web API / backend | The static JSON on releases and Vercel *is* the API. |
| Parquet in OCN releases | chess-parquet is private; the positions sidecar (H2.8) carries the zobrist instead. |
| Deep-theory slug expansion | The `mainline` field answers depth as data; the 7-segment profile cap stands. |
| Mass rewrite of boilerplate notes | Label generated vs curated (provenance), replace gradually on top-played rows; honest labelling beats fake curation. |
| Mnemonic token unification (Chi/Cha, Sch, RyL) | Would shred slug stability for aesthetics; tokens are subtree-local labels by doctrine (H2.4). |

## The ten design decisions

1. Layer over ECO and Lichess, never a substitute.
2. The spec bends to the data: two-layer ABNF (stable grammar / minor-versioned catalogue profile).
3. No class reclassification is reverted; radical honesty instead (divergence sidecar + normative rationales; the French rationale is the stress test).
4. Attribution publishes graded PARTIAL evidence; "the corpus" citations die; effort concentrates on the popularity-ranked top 100.
5. Slugs are stable keys: only spec violations migrate (`A.Hol` — sole case), under a real deprecation lifecycle that doubles as the spec's worked example.
6. Synthetic aliases are deleted; boilerplate notes are labelled, not faked.
7. i18n is rescoped to a declared core tier, off the critical path.
8. Zobrist moves in-repo (Python); parquet leaves the releases.
9. Distribution is pip-first (`ocn-chess`, data in the wheel); npm and any backend wait for demand.
10. Announcements run technical-first, Lichess-as-tribute, HN last; permission-free integrations before upstream PRs.

## Dependency spine

```
H0.1-H0.7 ──> H0.8 flip public ──> H1.1 pip + H1.2 JSON ──> H1.3 automation ──> H1.4 DOI/HF
                                          |
                    H2.1 annotator  H2.3 explorer (needs H1.2)
                    H2.2 quickstart H2.4 spec 1.3 ──> H2.5 divergence ──> H2.6 editorial
                    H2.7 popularity (soft)            H2.8 positions (needs H0.5)
                                          |
                                   H3 announcement wave
                                          |
                    H4.1 eco-file exports (can start in H2) ──> H4.2 ──> H4.3
                    H4.4 attribution sprint (starts when grading lands)
                    H4.5 governance, H4.6 i18n (parallel, continuous)
```

## Progress metrics (reported per release from H1 on)

- Installability: pip installs on clean machine (CI-checked), time-to-first-lookup.
- Reach: stars, explorer visits, dataset downloads (HF/Zenodo), DOI citations.
- Coverage: % of a 1M-game Lichess sample classified, and at what depth.
- Credibility: % of catalogue accepted by the published ABNF (must stay 100%),
  attribution coverage by grade, divergence rows with rationales (must stay
  100%), open disputes and median resolution time.

## Execution log

*(append entries as horizons land: date, IDs completed, release, evidence)*

- 2026-07-29 — Roadmap adopted. Audit snapshot:
  [`ocn-audit-2026-07.md`](ocn-audit-2026-07.md).
- 2026-07-29 — **H0.1 done.** Ship-ready half of PR #1 merged (`c88517d`:
  CI glob + guard, README 1.2.0 truth, four tested tools; suite 194 to
  285). Allgaier CLEAR applied under GO (`389929e`,
  [`archive/allgaier-clear-dry-run.md`](archive/allgaier-clear-dry-run.md)) — first live
  attribution with a reference-grade source. Inert drafts tracked as
  issues #2 (PARTIAL heads) and #3 (fr/de seeds); PR #1 closed, branch
  kept for the draft files. 0 open PRs.
- 2026-07-29 — **H0.2 done** (`352206a`). False ECO-fidelity claim
  replaced with the measured 13.8% divergence statement; French and
  London/Colle documented under Borderline classifications; 5 archived
  links fixed; private-repo references neutralised; tools section split
  consumer/maintainer; README 316 to 281 lines.
- 2026-07-29 — **H0.6 done** (`3a03694`). CONTRIBUTING.md, GOVERNANCE.md
  (registrar model), naming-dispute and data-error issue templates with
  labels created on the repo, CITATION.cff bumped to 1.2.0.
- 2026-07-29 — **H0.7 done** (`32e6002`). Twenty era-closed docs
  (13,573 lines) archived as pure renames; consumer guide renamed to
  [`consuming-ocn.md`](consuming-ocn.md); INDEX rewritten (20 live docs,
  was 40); live links repointed, archived links frozen.
- 2026-07-29 — **H0.4 done.** Corpus-citation hygiene lot applied
  (manifest `corpus-citation-hygiene.manifest.json`, 10 rows: 9 rewords
  to public dated games, 1 withdrawal — the Novosibirsk line returns to
  the backlog; attributed rows 27 to 26). Validator now fails on
  unverifiable-source patterns (corpus, Gigabase, private database);
  fixture + test added (suite at 286). Record:
  [`archive/corpus-citation-hygiene-dry-run.md`](archive/corpus-citation-hygiene-dry-run.md).
  Maroczy trio deliberately kept: identical sources are legitimate for
  identical claims; per-row context lives in historical_notes.
- 2026-07-29 — **H2.1 + H2.2 done.** `ocn annotate` names games by
  position at every ply (a Najdorf reached through 1.Nf3 is named a
  Najdorf), resolves `transposes_to` once, rewrites only its own
  headers, and annotates 1,000 games in 0.33s; `tools/coverage_stat.py`
  is the reproducible headline script. Honesty correction to the H2.1
  wording: every first move is a catalogue row, so "X% classified" is
  ~100% by construction — the meaningful stat is the depth table (share
  still named at 8/12/16/20 plies), and the script prints exactly that.
  The README quickstart is now executed verbatim by
  `tests/test_quickstart.py` (each `# ->` comment asserted against
  reality); consumer-guide sections 0 and 4 rewritten package-first
  (the stale parquet-join advice is gone). Suites: tests/ 100,
  tools/tests 375.
- 2026-07-29 — **H1.1 done.** The `ocn-chess` package: src layout, zero
  runtime deps, data bundled in the wheel (CSV + xref + positions index
  + VERSION with sync-script drift guard), typed `Row`, `Catalog` with
  by_slug/by_eco/by_name (diacritic-folded)/by_fen (O(1) via the
  index)/search/parents/children/resolve/co_canonicals/version, the
  python-chess en-passant adapter, and an `ocn` CLI (lookup/fen/uci/
  version, all with --help and --json). export_positions.py counters
  fixed (true halfmove/fullmove, cross-validated against python-chess).
  Verified: wheel installs in a clean venv on Python 3.10 and answers
  `ocn lookup B90` outside the repo. 59 package tests; tools suite 368.
  PyPI registration deferred to the GO (H1.1 note); README says
  `pip install .` until then. Annex A's python-chess claim tightened
  (modern python-chess defaults to the legal-ep form; the trap survives
  via en_passant="fen", PGN headers, engines, older versions).
- 2026-07-29 — **H2.5 done.** `catalog/ocn-1.eco-divergence.tsv`: 770
  rows (13.8% of ECO-bearing rows, the audit number reproduced exactly)
  across 7 rationale keys (french-b 252, indians-e 195, gruenfeld-e
  117, london-colle-a 82, catalan-d 49, misc 44, budapest-e 31), each
  resolving to prose in the spec's Borderline rules — the French
  rationale states plainly that OCN redefines ECO's letter C and what
  that does and does not claim. Validator check 21 recomputes the set
  independently of the builder (a builder bug cannot certify itself).
  Consumer guide gains "Consuming OCN from an ECO-keyed system" with
  the C00 worked example (43 slugs, all class B). 42 new tests.
- 2026-07-29 — **H0.5 done.** EFCDB references removed from the spec
  entirely (grep-clean): the Layer 1 pairing and the Lichess long-tail
  layering are restated over in-repo artefacts (the xref sidecar), and
  the new normative **Annex A — Position identity** defines `fen_key`
  (with the legal-en-passant rule stated as the trap it is) and the
  Polyglot Zobrist by reference to the public book format. Position
  keys are now computable from OCN-1 alone. Two leftover "corpus"
  mentions in the column table also removed (H0.4 alignment).
  **Horizon 0 is complete except H0.8, the flip itself.**
- 2026-07-29 — **H0.3 done.** Spec Format section now states the
  enforced grammar (`class . named+ . move*`, 7-segment cap);
  depth-cap saturation acknowledged as design; token ambiguity
  documented descriptively; `spec/errata.md` created (E-001 QID
  re-point, E-002 1.2.0 mass rename, E-003 grammar gap); fixtures
  declared the provisional conformance corpus; spec history extended
  through 1.2 plus the triage patch.
- 2026-07-29 — **H0.7 done.** Docs triage: 20 era-closed working
  documents `git mv`-ed into [`archive/`](archive/) — the 12
  `*-dry-run.md` reports plus `naming-error-corrections-record.md` (the
  13 applied-lot records the INDEX used to list one by one), the six
  process-not-reference attribution documents (audit backlog, both
  parked source logs, the Group B evidence sprint, the parked French
  Winawer proposal, the factory map) and the superseded
  `post-1.1-roadmap.md`, whose live role this roadmap took over. The
  consumer guide lost its release suffix and is now
  [`consuming-ocn.md`](consuming-ocn.md); every reference in a live file
  (README, CONTRIBUTING, GOVERNANCE, live docs, two tool comments) was
  repointed, while links inside archived documents stay frozen as
  written. INDEX rewritten: consumer guide first, applied-lot records
  collapsed to a single archive line. `docs/*.md` goes 40 to 20 live
  files (13,573 lines of process logs moved out of the top level);
  `attribution-source-status.tsv`, `examples/` and `manifests/` stay.
  Slug gate and the 285-test suite green.
- 2026-07-29 — **H1.2 done.** `tools/build_json_export.py` builds the
  whole-catalogue export `ocn-1.json` (`schema: ocn.catalog.v1`,
  `catalog_version` from the git tag or `--version`, `generated_note`
  naming the CSV as canonical): all 5,899 rows, every CSV column
  verbatim in header order plus five derived fields — `moves_san` (the
  UCI line replayed through `tools/chess_uci.py` to numbered SAN, `""`
  for the five class roots) and the arrays `eco`, `aliases_list`,
  `same_as_list`, `flags_list`. Stdlib only, deterministic (catalogue
  row order, fixed key order, two builds byte-identical), 3.3 MB
  compact / 4.5 MB `--pretty`. Not committed: it is a release artefact,
  so `/ocn-1.json` is gitignored. Schema documented in
  [`consuming-ocn.md`](consuming-ocn.md) section 11; 22 tests in
  `tools/tests/test_build_json_export.py`.
- 2026-07-29 — **H1.5 done.** `tools/build_eco_table.py` emits the
  committed sidecar `catalog/ocn-1.eco.tsv`
  (`ocn1`/`eco`/`seq`, one row per slug and atomic ECO code, `seq` the
  0-based position in the original pipe list): **7,234 rows, 500
  distinct ECO codes, 5,600 slugs**, longer than the catalogue because
  526 slugs carry a composite cell. `eco_legacy` is untouched — the
  table is additive, not a migration. Drift-guarded like the
  attribution sidecar (committed file must equal a fresh rebuild); 17
  tests in `tools/tests/test_build_eco_table.py`, including a
  round-trip that rebuilds every `eco_legacy` cell from the table.
  Consumer guide gained section 9 (join by ECO without `LIKE`), and
  spec Goal 3 now states the truth instead of a universal claim: rows
  within ECO's coverage carry their code(s), and the 299 rows (5.1%)
  that carry none are the five class roots plus 294 Lichess long-tail
  lines beyond ECO's 500-code resolution — coverage extension, not a
  defect.
- 2026-07-29 — **H2.5 done.** Classification honesty shipped as data plus
  argument. `tools/build_eco_divergence.py` emits the committed sidecar
  `catalog/ocn-1.eco-divergence.tsv`
  (`ocn1`/`ocn_class`/`eco_codes`/`family_head`/`rationale_ref`): every row
  whose OCN class letter is absent from its own ECO letters — **770 rows,
  13.8% of the 5,600 ECO-bearing rows**, matching the audit's measurement
  exactly. `rationale_ref` is a closed 7-key set assigned by `family_head`,
  so no row can carry an unexplained divergence: french-b 252, indians-e
  195, gruenfeld-e 117, london-colle-a 82, catalan-d 49, misc 44,
  budapest-e 31. The buckets reconcile with the audit table row for row (its
  E-from-A 217 and E-from-D 126 split here into indians-e / budapest-e /
  gruenfeld-e). Enforced twice: a drift test (committed file equals a fresh
  rebuild) and validator check 21, which recomputes the divergent set inline
  — deliberately a second implementation, `tools/validate.py` does not
  import the builder — and fails listing unlisted/stale slugs, capped at 10
  examples, scoped to the canonical catalogue so the fixtures stay clean.
  Spec "Borderline rules" gained the two undocumented cases with real
  reasoning: **French to B** (the stress test — OCN's `C` is the symmetric
  king-pawn openings, so `C` loses its one exception; stated plainly as a
  redefinition of ECO's letter `C`, with the normative "MUST NOT assume
  letter equality" consequence and the note that reversal would rewrite 252
  primary keys and could only ship in a 2.x) and **London/Colle to A**
  (queen's-pawn systems are repertoire objects, not Queen's Gambit theory;
  ECO keys on the d4/d5 pawn pair, OCN on the system character). Existing
  bullets gained their rationale keys so every key resolves to prose, plus a
  closing paragraph with the totals and the standing position: the letter is
  a property of OCN's taxonomy, ECO codes stay untouched on every row within
  ECO's coverage. Consumer guide gained section 10, "Consuming OCN from an
  ECO-keyed system" — the two safe join paths (by code, by position), the
  `C00` worked example (43 slugs, all class `B`: bucket by OCN's letter with
  ECO's meaning and the whole French is misfiled), and the exception-table
  recipe for consumers stuck with a letter-keyed schema. 42 tests in
  `tools/tests/test_build_eco_divergence.py`. Position held: nothing
  reverted.
- 2026-07-29 — **H1.3 done** (`59ed17e`). `.github/workflows/release.yml`
  replaces the five-step manual runbook of the 1.2.0 notes. An `ocn-*` tag
  push (or a `workflow_dispatch` with a `tag` input, for re-runs) reruns the
  whole ci.yml gate — byte-compile, `validate.py`, `--strict-chess`, the
  tools suite, the Lichess fixture check, the package suite — then adds a
  release-only guard the branch gate does not need: `sync_package_data.py`
  in its default dry-run mode, so a wheel can never ship a catalogue that
  has drifted from `catalog/`. It then builds **eight assets** into
  `dist-release/`: four committed sidecars copied verbatim (`ocn-1.csv`,
  `ocn-1.lichess-xref.tsv`, `ocn-1.eco.tsv`, `ocn-1.eco-divergence.tsv`),
  `ocn-1.positions.tsv` rebuilt with the same options the package sync uses
  and `cmp`-ed against the bundled copy, `ocn-1.json` built with
  `--version "$TAG"` so `catalog_version` is the release tag rather than
  whatever `git describe` finds, the sdist + wheel from a pinned
  `build==1.2.2.post1`, and `SHA256SUMS` over the lot. The wheel is
  smoke-tested in a clean venv (`ocn version`, `ocn lookup B90` — the H1.1
  criterion, now automated against the exact file being published) before
  anything is uploaded. Publication is plain `gh` with `GITHUB_TOKEN`:
  `gh release create --verify-tag` for a new tag, `upload --clobber` plus
  `edit` for a re-run, **never** `--generate-notes` — the title and body are
  taken from `docs/release-<tag>-notes.md` (its H1 becomes the release
  title), and a missing notes file yields a body that says so instead of
  GitHub's commit-list filler. `permissions: contents: write`, one
  concurrency group per tag, `cancel-in-progress: false` so a half-uploaded
  release cannot be interrupted. **Parquet is dropped** (decision 8), stated
  as such in a workflow comment: `openings.parquet` and
  `_efcdb_manifest.json` came from the private `chess-parquet` repo, so a
  public workflow cannot regenerate them and every asset OCN now publishes
  is buildable from `catalog/` alone. Consumer guide gained section 13 with
  the exact eight-asset list. Every build command was run locally against a
  `git archive` checkout before landing: 5,894 position rows, 5,899 JSON
  rows, 3.3 MB JSON, 619 KB wheel, `SHA256SUMS` verified with
  `sha256sum -c`.
- 2026-07-29 — **H2.8 done, minus the deferred `mainline` column.** The
  Polyglot zobrist is computed in this repository:
  `tools/polyglot_zobrist.py` carries the public 781-key Polyglot random
  array as vendored data with a provenance header (the array is part of
  the book format, not an OCN choice; it was dumped programmatically from
  python-chess inside a throwaway virtualenv that was then deleted, so the
  values are transcription-free) and implements Annex A's XOR scheme —
  piece-square keys, castling rights, the en-passant file **only when a
  capture is legal**, side to move. Stdlib only; python-chess is never a
  dependency. The gate is the book format's **published test vectors, all
  seven matched exactly**, including the two pathological cases (`1.e4 d5
  2.e5 f5` → `0x22a48b5a8e47ff78`, the en-passant file key; `1.a4 b5 2.h4
  b4 3.c4 bxc3 4.Ra3` → `0x5c3f9b829b279560`, en passant plus a lost
  castling right). Two independent confirmations beyond the vectors: a
  one-off cross-check against `chess.polyglot` over all 5,894 concrete
  rows agreed 5,894/5,894, and the tabiya the consumer guide has
  documented since 1.1.0 (`D.Rub` / `A.Col.Zuk`,
  `7092856595585369542` — a number the private `chess-parquet` Rust
  implementation produced) reproduces exactly, so the decoupling changes
  no published hash and a 1.2.0-era join keeps working.
  `export_positions.py` now derives everything in one pass over the board
  and appends three columns after the existing eleven — `san` (numbered
  movetext, byte-identical to `build_json_export`'s `moves_san` on all
  5,894 rows), `epd` (four fields, no operations) and `zobrist` (unsigned
  decimal) — appended rather than interleaved so index-reading consumers
  survive; class roots stay excluded and blank under `--include-roots`.
  The 5,765 distinct `zobrist` values map one-to-one onto the 5,765
  distinct `fen_key` values, no collisions. Sidecar 1.48 to 2.12 MB;
  bundled copy regenerated, `cmp` against a fresh release build passes.
  `epd` is by construction the same string as `fen_key` (Annex A already
  normalises en passant the way EPD wants) — kept as a named column for
  EPD-driven tooling, and it is the obvious thing to drop if the ~350 KB
  it costs the wheel ever matters. Consumer guide: section 4 gained the
  full column table, a worked `B.Sic.Naj.Eng` sample and the
  unsigned-vs-signed INT64 warning, and section 7's SQL stopped telling
  people to `read_parquet('openings.parquet')` — a file no release has
  shipped since H1.3 — in favour of `read_csv` over the sidecar.
  27 new tests: 15 in `tools/tests/test_polyglot_zobrist.py`, and
  `test_export_positions.py` goes 5 to 17 (the column order is now pinned
  as a contract, so a future insertion breaks the suite rather than a
  consumer's `awk`).
  **Deferred: the `mainline` SAN continuation.** It is only meaningful if
  the continuation is the *popular* one, and that ranking is the Lichess
  explorer data H2.7 brings in. Shipping a `mainline` picked by any rule
  available today (first child by slug order, deepest descendant) would
  publish an editorial claim dressed as data, which is exactly the failure
  mode the roadmap's positioning section forbids. It lands with H2.7.
- 2026-07-29 — **H2.4 done** (this commit). Spec 1.3, the standards
  release. The prose production is gone: `spec/OCN-1.md` now carries a
  **normative RFC 5234 ABNF** (numeric terminals throughout, because
  ABNF quoted strings are case-insensitive and slugs are not) whose
  language is exactly `validate.py`'s `SLUG_RE`, and the **two-layer
  model** is stated as a versioning rule — the grammar is
  major-versioned, the **catalogue profile** (CP-1 seven segments, CP-2
  at least one named segment, CP-3 3-char tokens outside the registry,
  CP-4 no all-lowercase named token, CP-5 no new SAN-shaped named token)
  is minor-versioned and may only be tightened against a catalogue that
  already satisfies it. Every profile rule was computed from the live
  catalogue before it was written down; class roots are grammar-valid.
  **Token ambiguity is settled normatively**: the move tail is the
  maximal trailing run of segments parsing as `san-move`, everything
  before it is a named token. That rule reads `B.Sic.Sve.Nd5` as a move
  and `D.Sem.Bg5.Mos` as a name — the left-to-right "any 3-char token is
  named" heuristic in check 8 gets the first one wrong, which is exactly
  why the spec now says which walk is correct. The **grandfather table**
  is computed, not curated: the 39 SAN-shaped tokens that occupy a
  named-region position in the catalogue, across 570 occurrences, listed
  exhaustively in the spec and closed. New sections: Requirements
  language (BCP 14), **Conformance** (Producer P-1..P-9, Consumer
  C-1..C-12, Validator V-1..V-8, each obligation citing the section it
  draws on), **String canonicalisation** (ASCII case-significant slugs
  that MUST NOT be normalised before comparison; NFC name fields with
  true diacritics; ASCII folding a search affordance and never a key),
  **Extension mechanism** (the flags registry *is* the spec section,
  `x-` reserved for private use, `ocn-1.aliases.<bcp47>.tsv` registered
  with `ca`/`es` listed), **Versioning 2.0** (17-row field-level change
  table; slug removal/re-point and any grammar change major, entry
  addition and canonical_name/eco_legacy change minor with a changelog,
  aliases/notes/attribution/i18n patch) and the **deprecation
  lifecycle** (8 numbered steps, `catalog/ocn-1.redirects.tsv` shipped
  empty with its four-column format specified). Versioning 2.0
  retroactively legalises the 1.2.0 mass rename and `errata.md` E-002 now
  says "landed in v1.3"; E-001 and E-003 likewise. `A.Hol` is
  **designated, not migrated** — the one token violating the spec's own
  abbreviation rules ("Dutch Defence" gives Dut, not Hol), scheduled as
  its own gated 114-row lot, with the note that `Dut` already exists
  subtree-locally without collision because tokens are subtree-local
  labels (which is also why Chi/Cha/Sch/RyL stay put). **`conformance/`
  is declared normative**: `valid.tsv` (60 cases — roots, depth 1-6,
  tails 0-5, grandfathered tokens, registry tokens, castling, captures,
  file and rank disambiguation, plus four flagged synthetic grammar
  corners for `=Q`/`=N`/capture-promotion/`_`), `invalid.tsv` (41 cases,
  `slug` TAB reason code) and a README defining the closed 8-code set
  (`G-EMPTY-SEGMENT`, `G-CLASS`, `G-CHAR`, `CP-1`..`CP-5`) with a
  normative evaluation order, so every rejection has exactly one correct
  reason. Invalid slugs carry `\uXXXX` escapes — a TSV cannot hold a
  literal tab, and the project does not put U+00B7 in its own files even
  as a negative example. `tools/tests/test_conformance_corpus.py` is the
  gate: it implements the ABNF **independently** (backtracking recursive
  descent over the optional elements of `piece-move`, because `b8=Q`
  parses only when [file] and [rank] are both skipped) and reads both
  registries out of the spec markdown, then asserts the two
  implementations agree on all 101 corpus cases and all **5,899**
  catalogue slugs, that the grandfather table is exactly what the
  catalogue contains, and that the spec tables pin `validate.py`'s
  constants. Two of its tests go further and prove the *languages* are
  identical rather than merely agreeing on the corpus: exhaustive
  enumeration of every token of length 1-3 over SAN's alphabet against
  `SAN_RE`, and every string of length 0-3 over a hostile alphabet
  against `SLUG_RE`, zero mismatches (a wider one-off fuzz — 1.4M cases
  including random tokens to length 12 — also found none). Validator
  **check 22** enforces CP-5 with its own maximal-suffix walk plus a
  fixture. Suites: tools/tests 447, tests/ 100; validator clean in both
  modes (0 warnings); slug gate green.
