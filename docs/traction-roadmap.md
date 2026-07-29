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
| H2.8 | **Positions sidecar completed** (`export_positions.py` grows): SAN movetext, EPD, corrected FEN, **Polyglot zobrist computed in Python in-repo** (completes the chess-parquet decoupling), and a `mainline` SAN continuation for leaf rows — the answer to "ECO main lines run 20-24 plies" as data, not as deeper slugs. | M | One regenerable artefact carries every derived per-row field; local tools consume it instead of recomputing. |

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
  [`consuming-ocn.md`](consuming-ocn.md) section 10; 22 tests in
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
