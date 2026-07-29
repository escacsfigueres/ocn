# OCN audit, July 2026 — traction readiness

**Date:** 2026-07-29. **Tree audited:** `main` @ `3137dfb` (catalogue 5,899 rows,
released tag `ocn-1.2.0`). **Method:** three parallel read-only exploration
agents (catalogue data, tooling/engineering, spec/docs/positioning), external
landscape research (GitHub, Lichess, standards precedents), and two roadmap
design passes (traction lens, credibility lens) synthesised into
[`traction-roadmap.md`](traction-roadmap.md). This document is the dated
snapshot of findings; the roadmap is the living plan derived from it.

Companion to [`ocn-360-audit.md`](ocn-360-audit.md) (2026-06-10), which audited
internal correctness. This audit asks a different question: **what stands
between OCN and real-world adoption as a complement to ECO?**

---

## Verdict

> OCN has built an impressively rigorous data-quality factory and almost no
> distribution surface. The catalogue is arguably ready to compete for the role
> of "the hierarchy layer over ECO and the Lichess names" — and the engineering
> around it makes that impossible for anyone to find out.

Structural integrity is reference-grade: 0 orphan parents, 0 duplicate
canonical names, all 500 ECO codes covered, 0 unresolved transposition groups,
194 tests green, a 1:1 Lichess cross-reference, and a manifest-driven change
process with guarantees most open-data projects lack. But the repo is private
with zero public artefacts, nothing is installable, the published spec grammar
is contradicted by a quarter of its own catalogue, the README makes one
verifiably false claim, and the project's unique moat (sourced naming
attributions) covers 0.44% of rows because its own publication policy cannot
scale past double digits.

## Scorecard

| Dimension | Grade | One line |
|---|---|---|
| Structural data integrity | A | 0 orphans, 0 dangling links, 500/500 ECO codes, 0 unresolved FEN groups |
| Maintainer tooling | A- | Manifest engine with zero-collateral-diff and dry-run-by-default is genuinely strong |
| Test discipline | B+ | 194 green in 18s, systematic negative fixtures; depth uneven (`chess_uci.py`: 548 LOC, 5 tests) |
| CI | B- | 3-version matrix, strict data gate; drifted compile list, no release automation |
| Consumer API | C+ | `ocn.py` well designed but unpackaged; no name/ECO lookup, untyped rows |
| Editorial content | C- | Half the notes are boilerplate, a quarter of aliases synthetic, attribution at 0.44% |
| Spec as a standard | C- | No formal grammar; the published one rejects 23.6% of the catalogue; no conformance or governance |
| Performance | C | 0.5s per position lookup per process; the materialised index exists but is unused locally |
| Packaging | F | No pyproject, no package, no entry points, no PyPI, no npm |
| Distribution and reach | F | Private repo, 0 stars, releases 404 to the public, no DOI/HF/Kaggle/web |
| Adoption readiness | D- | Catalogue quality far ahead of anyone's ability to consume it |

---

## 1. External reality: OCN does not publicly exist

- `escacsfigueres/ocn` is **private**: 0 stars, 0 forks, empty homepage URL.
  Release asset URLs 404 to unauthenticated clients (documented in
  [`release-ocn-1.2.0-downstream-verification.md`](release-ocn-1.2.0-downstream-verification.md)).
  Web searches for "OCN Open Chess Naming" return nothing. Every outward-facing
  artefact in the repo — CC-BY licence, CITATION.cff, "corrections welcome via
  issues" — is written for a public standard nobody can read.
- The companion repo `escacsfigueres/chess-parquet` is also private, and stays
  so by owner decision. Consequence for OCN: the release pipeline and the
  spec's normative surface must be decoupled from it (see §11).
- **The real incumbent is not ECO — it is
  [lichess-org/chess-openings](https://github.com/lichess-org/chess-openings)**:
  CC0, ~3,690 lines across five TSVs (eco, name, PGN, UCI, EPD), 544 stars,
  127 forks, powers Lichess itself, mirrored on Kaggle, exported to Parquet,
  governed by one-opening-per-PR review. Any OCN pitch must position relative
  to this dataset, not to the 1971 encyclopaedia in the abstract.
- **The cautionary precedent is NIC-Key** (New in Chess): a mnemonic ECO
  alternative from the NICBase era (`SI` for Sicilian, `KI` for King's Indian).
  It never displaced ECO — proprietary, tied to one vendor's tooling, no open
  distribution. Lesson: mnemonics alone do not win; distribution and
  integrations do.
- OCN's genuine differentiators over the Lichess dataset: explicit
  machine-readable hierarchy with stable slug keys, transposition
  canonicalisation relations, sourced naming attributions (nobody else has
  this), locale sidecars, dual ECO+Lichess mapping, and strict validation.
  None of them is visible anywhere outside this repo.

## 2. Catalogue data

### What is verifiably clean (0 violations each)

5,899 rows, 14 columns. 0 duplicate `canonical_name`; 0 orphan `parent_ocn1`;
0 rows where the parent is not a slug prefix; 0 dangling `transposes_to` or
`same_as`; all 500 atomic ECO codes A00-E99 present after splitting composites;
0 unresolved duplicate-FEN groups (124 groups, all resolved via
`transposes_to`/`same_as`, both FEN-verified); depth equals dot count on all
rows. The Lichess xref sidecar covers 100% of rows (56.6% exact, 43.3% prefix,
5 roots), and 91.7% of upstream Lichess (eco, name) pairs have an exact OCN
row.

### Shape: broad and shallow

- `moves_uci` length: average 9.6 plies, median 9, mode 6. Only 3.1% of rows
  reach 20+ plies — the depth where ECO's actual main lines live (20-24
  plies). OCN names the tree; it does not carry the theory. (The roadmap's
  answer is a `mainline` data field, not deeper slugs — see roadmap D-2/H2.8.)
- Rows per class: A 1,367, B 1,071, C 1,642, D 902, E 618, no-ECO 299.
- ECO coverage is top-heavy: A00 alone maps to 290 rows; 57% of ECO codes map
  to exactly one row.

### Content weaknesses

- **`notes` is 100% filled and ~49% boilerplate.** 2,556 rows match the
  template "(move) in/against the (parent)"; 189 rows are "Lichess split line
  extending X."; 50 note strings repeat verbatim across rows. Mean length 43
  characters; some notes restate a single move ("6.Be3.").
- **Aliases are heavily synthetic.** 1,726 alias strings are "(SAN) Line"
  ("Nf6 Line", "O-O Line"); standalone "Main Line" appears 398 times; 27.9% of
  rows carry only generic aliases; 8.3% have none. One row (`E.Gru.Neo`)
  duplicates an alias inside its own cell.
- **29 aliases are exactly another row's canonical name**, making name-to-slug
  lookup ambiguous (e.g. `B.Sic.Ama` aliases "Amazon Attack", which is
  `D.QPG.Ama`'s canonical name).
- **36.2% of canonical names contain raw SAN tokens** — concatenated
  Lichess label segments ("Sveshnikov 9.Nd5 Be7, 10.Bxf6 Bxf6"); 330 names have
  two or more commas; one near-duplicate pair differs only by a comma.
- **Spelling is asymmetric**: canonical names are 100% British ("Defence" on
  701 rows); the American-alias lot covered 691 rows, so US-spelling lookup
  succeeds inconsistently.
- **`flags` is effectively binary**: `sharp` (2,974) and `closed` (2,556)
  cover 94% of tagged rows; `theoretical` (105) has no documented criteria;
  `deprecated` — the flag the entire stability promise rests on — has 0 uses
  ever; 9 rows are flagged both `sharp` and `closed`.
- **`eco_legacy` is not consumer-safe as stored**: 526 rows carry pipe-joined
  composites (up to 30 codes in one cell) and 299 rows (5.1%) are NULL —
  which quietly falsifies spec Goal 3 ("every slug carries a back-reference to
  its ECO codes"). The NULL rows are Lichess long-tail lines that extend
  beyond ECO's coverage; the honest fix is to say so.
- **41 pairs share byte-identical `moves_uci`** — two names for literally the
  same line (e.g. `A.Lon` and `D.QPG.Zuk.Nf6.Bf4`), all linked, but mostly via
  the asymmetric `transposes_to` rather than `same_as`.

### What a consumer wants and does not get

No SAN/PGN movetext (every consumer must ship a legal-move generator just to
render "1.e4 c5"); no EPD or Polyglot key in this repo; exported FEN hardcodes
"0 1" counters (breaks PGN/GUI round-trips); no popularity or W/D/L data
(Lichess publishes exactly this per position); no year-of-first-play; no
example games; no structured attribution; no shipped name-to-slug reverse
index; no per-row provenance (even though the manifest history contains it).

## 3. Tooling and engineering

- 17 Python tools, ~5,070 LOC, plus ~2,910 LOC of tests. **84% of tool code is
  maintainer-facing, 16% consumer-facing** — inverted relative to what an
  adoption push needs.
- **Packaging: nothing.** No pyproject/setup/requirements; no `__init__.py`;
  the documented integration path is `sys.path.insert(0, "tools")`. Four files
  carry a try/except dual-import dance that exists only because there is no
  package.
- **`tools/ocn.py`** (the consumer reader, 105 LOC) is well designed and well
  tested (pins the en-passant trap in both directions), but: no `by_name`, no
  ECO lookup, no `parents()`/breadcrumb, no `__version__`, rows are raw
  `dict[str, str]`. The CLIs it should subsume are inconsistent: 5 consumer
  tools hand-roll `sys.argv` and have **no `--help`**; flag vocabulary forks
  (`--json` vs `--format`).
- **`chess_uci.py`** is a correct, from-scratch move generator (castling
  rights, underpromotion, and the subtle legal-en-passant FEN rule all
  handled) — guarded by only **5 tests for 548 LOC** of code where a silent
  bug would corrupt every FEN key and every published artefact. Its real
  safety net is `validate.py --strict-chess` replaying all rows in CI, which
  catches illegal moves but not wrong-but-legal SAN.
- **The en-passant trap is a silent adoption killer.** OCN's `fen_key` emits
  the ep square only when a capture is actually legal; python-chess emits it
  unconditionally. A python-chess user passing `board.fen()` to `by_fen()`
  gets `[]` for any position after a double pawn push and concludes the
  catalogue is broken. The fix is a ~30-line adapter; today the trap is
  documented in a guide the public cannot read.
- **Performance:** every tool re-parses the CSV per invocation; a position
  lookup costs ~0.5s per process because the FEN index is rebuilt from moves
  each time. `export_positions.py` materialises exactly this index as a
  release artefact — and the local tools ignore it and recompute.
- **CI** runs a 3.10/3.11/3.12 matrix with strict validation — good — but has
  **zero release automation** (three artefacts are built and attached by hand,
  coordinated cross-repo via a prose runbook), and the hand-maintained
  byte-compile list has drifted: `build_lichess_xref.py`,
  `generate_diacritic_manifest.py` and `ocn.py` (the consumer reader!) are
  outside CI. The fix (glob + guard test) sits on the unmerged branch.
- **PR #1 (`feat/finish-goals`) has been open since 2026-06-18.** It is
  cleanly bimodal: ~60% ship-ready engineering (the CI glob fix, README truth
  to 1.2.0, four new tools each with ~1:1 test ratio; suite grows 194 to 285)
  and ~40% deliberately inert drafts quarantined under `docs/drafts/` (two
  attribution manifests, fr/de i18n seeds) awaiting GOs. The ship-ready half
  has no reason to keep waiting: meanwhile `main`'s README advertises a
  superseded release and CI skips the consumer reader.
- **`CITATION.cff` is stale** (1.1.0 / 2026-05-26 vs released 1.2.0 /
  2026-06-11) and carries no DOI.

## 4. Spec integrity

- **No formal grammar, and the informal one is wrong.** The spec's production
  allows at most 6 segments and at most 2 trailing move segments. The
  catalogue contains 1,084 rows (18.4%) at 7 segments and 1,393 rows (23.6%)
  with 3-5 SAN move tails, up to `C.Vie.Nc6.f4.exf4.Nf3.g5`. The real grammar
  ("class, one or more named tokens, zero or more SAN moves") exists only as a
  comment in `validate.py`. A second implementer working from the spec would
  reject a quarter of the reference catalogue. **The implementation is the
  spec; the document is a stale approximation.**
- **Context-sensitive token ambiguity is unspecified.** `Bg5` is a legal SAN
  move and a plausible named token; `D.Sem.Bg5.Mos` parses it as a name while
  `B.Sic.Sve.Nd5` parses `Nd5` as a move. The validator resolves this
  positionally; the spec never mentions it.
- **The versioning policy is untested and already violated.** The `deprecated`
  mechanism has never been exercised (0 uses); the policy was broken once by
  the QID slug re-point across a release boundary
  ([`qid-migration-decision-record.md`](qid-migration-decision-record.md)) with
  no errata entry; spec history stops at v1.1 while the catalogue is 1.2.0;
  and 1.2.0 renamed 683 canonical names under a "minor" bump that the spec's
  own change rules arguably forbid.
- **String canonicalisation is absent from the spec** — Unicode normal form,
  diacritic policy, ASCII-fold search equivalence all live in tooling and
  working docs, even though 1.2.0 was entirely a diacritics release.
- **No conformance machinery**: no Conformance section, no RFC 2119 boilerplate,
  no producer/consumer split, no normative test corpus (30 usable fixtures
  exist in `tools/tests/fixtures/` but are not declared).
- **No registration or governance**: the question "who mints a new slug?" has
  no answer anywhere in the repo. Spec Rule 4 promises collision choices
  "documented in the catalogue": 0 rows comply.
- **No extension mechanism**: the flags vocabulary is closed; locale sidecars
  are unregistered; a third party cannot add a field without forking.
- **The depth cap is saturated.** 18.4% of rows sit at the absolute 7-segment
  maximum ("legendary tabiyas" is not a category with 1,084 members), and the
  spec's own rules make any raise a 2.x event. Unacknowledged.
- **The spec normatively references an unpublished document** (the EFCDB spec
  in the private chess-parquet repo) for its primary join recommendation. An
  outside implementer cannot follow the spec's own advice.

## 5. Classification honesty

The README asserts, in bold, that OCN keeps ECO's A-E classification
unchanged. Measured: **770 rows (13.8% of ECO-bearing rows) carry an OCN class
letter that is not among their own ECO letters.**

| OCN class | ECO letters | Rows | Documented? |
|---|---|---|---|
| B | C | 252 (the French, `B.Fre`) | **No** |
| E | A | 217 (Benoni, Benko, Budapest) | Yes |
| E | D | 126 (Grünfeld) | Yes |
| A | D | 82 (`A.Hor`, `A.Col`, `A.Lon`, `A.Ver`, others) | **No** |
| D | E | 49 (Catalan) | Yes, framed backwards |
| A and B, misc | E, B, C, A | 44 | **No** |

The French is the elephant: ECO's class C is "1.e4 e5 and the French"; OCN
redefines C as symmetric king-pawn and moves the entire French to B. That is a
redefinition of an ECO class letter's semantics — strictly larger than the
documented Grünfeld case — on one of the five most-played defences in chess.
The rationales for the documented cases are chess-legitimate; the problem is
the false fidelity claim, the two undocumented families, and the absence of
any divergence table or validator visibility that would keep the number
honest. The 1.2.0 ECO-correction lot even *increased* the divergence
(correcting `A.Lon` from A48 to D02) without a spec note.

## 6. Mnemonic quality (the "read once, remember forever" claim)

- 150 of 754 distinct leaf tokens (20%) carry more than one meaning across
  subtrees — formally legal (the spec only forbids same-parent collisions),
  corrosive to the memorability pitch.
- The same person gets different tokens: Chigorin is `D.Chi` but `C.RyL.Cha` —
  and `Cha` reads as Chatard (a real French Defence eponym) to any experienced
  player.
- `A.Hol` (Dutch Defence) derives from "holandesa", not from any English
  name — it violates the spec's own first-three-pronounceable-characters rule
  (which would give <!-- NON-CATALOGUE: proposed successor slug --> `A.Dut`)
  and quietly undermines the "English canonical names are definitive" claim.
- `Sch` corresponds to 14 distinct leading surnames upstream (Scheveningen,
  Schlechter, Schneider, ...) — the worst collision cluster, inherent to
  3-char German surnames.
- The `RyL` justification in the spec is post-hoc; `Ruy` or `Spa` would have
  been at least as defensible, and `RyL` breaks TitleCase, needing special
  handling.

The roadmap's position: tokens are subtree-local labels, not global person
identifiers (person identity belongs in the attribution data); only
spec-violating tokens migrate, under a real deprecation lifecycle.

## 7. Attribution: the moat at 0.44%

- 26 of 5,899 rows carry `attributed_to` + `attribution_source` +
  `historical_notes`, against roughly 2,375 rows bearing a recognisable
  eponym. Ten months of genuinely excellent machinery — the A-I taxonomy, ten
  ranked source-gated lots, the dangerous-surnames list, the batch engine, the
  triage tool, CLEAR/PARTIAL evidence grading, and a documented public
  retraction of a hallucinated citation — has produced 26 rows.
- **The bottleneck is policy, not tooling.** CLEAR (the only publishable
  grade) requires a reference-grade book or encyclopaedia source; exactly one
  row in the world currently clears that bar (`C.KGm.Acc.All`, Allgaier, via
  the Oxford Companion) and it sits un-applied on the stale branch. The
  policy conflates *publishable* with *certain*; reference works publish
  graded, hedged etymologies instead.
- **Some sources are unverifiable by construction**: rows citing "the corpus"
  (e.g. `B.Sic.Sve.Bxf6.Nd5.Bg7`) point at an unpublished game collection. An
  unverifiable citation is worse than none — it converts missing data into
  apparent fabrication.
- Sources are free text (no author/year/work/page/URL/role/grade structure),
  and three rows share a byte-identical copy-pasted source string.

## 8. i18n: a well-designed pilot, not a feature

The sidecar architecture (per-locale TSV, English canonical stays definitive,
partial coverage by design, integrity-tested) is right. The content is 58 rows
per locale (ca, es) = 1.0% of the catalogue, one label per slug, nothing below
depth 1; fr/de drafts sit on the unmerged branch pending native review — and
the live ca/es pilots have had no native sign-off either. At this coverage the
sidecars are a liability if presented as a feature. (Roadmap: rescope to a
declared core tier, off the traction path.)

## 9. Documentation and positioning

- ~83 doc files, ~17,300 lines: **~96% internal process records, one
  consumer-facing guide (~2%)**. The three dry-run diff logs alone are 11,174
  lines — 64% of all documentation — sitting at `docs/` top level where a
  newcomer lands first.
- **There is no PGN-to-OCN recipe anywhere** — the number-one newcomer
  question. The consumer guide's quick start begins "compute the Polyglot
  zobrist hash", presupposing an artefact from a second private repo; the word
  "PGN" does not appear in it.
- The README spends ~75 of 313 lines documenting 16 CLI tools (most of them
  internal audit scripts) and carries **5 broken links** (docs moved to
  `archive/` without updating it), an obsolete 0.x roadmap numbering scheme,
  and the stale 1.1.0 badge/status.
- Audience coverage: database developers partially served (three-relation
  model, DuckDB recipes — but behind a private wall); coaches and content
  creators not served at all (the hierarchy is OCN's best asset for them and
  nothing renders it as a browsable tree); data scientists barely served
  (no DOI, no dataset publication, no data card, no notebook).
- Distribution-channel sweep across the whole repo: zenodo 0, DOI 0,
  huggingface 0, kaggle 0, github.io 0, pypi 0, npm 0. A Vercel project named
  `ocn` already exists in the team account — empty.

## 10. Governance: everything external is missing

No CONTRIBUTING.md, no code of conduct, no issue or PR templates, no
SECURITY.md, no discussions, no naming-dispute process, no
"how to propose an opening name", no maintainer statement. The only
invitation — "corrections welcome via issues" — points at a repo outsiders
cannot see.

What exists instead is a strong *internal* process: the GO-gate playbook, the
manifest discipline ("never hand-edit the CSV"), evidence grading with a
documented public retraction, and real decision records. That is better
change-control than most open chess data projects have — it has simply never
been translated into rules an outsider could follow (parts of it live in
Catalan in `CLAUDE.md`). Converting it into a public contribution and dispute
process is cheap and buys disproportionate credibility.

## 11. chess-parquet coupling (must be resolved for a public OCN)

OCN's headline join key (Polyglot zobrist) is materialised by a Rust crate in
the private chess-parquet repo; the three release assets are built there or by
hand; release gate 4 is cross-repo ("parquet regen is mandatory"); and the
spec normatively references the unpublished EFCDB spec. Since chess-parquet
stays private, a public OCN must: demote the EFCDB reference to informative,
inline the position-identity parameters it actually needs as a spec annex,
grow a Python-side zobrist/positions exporter in-repo, and drop the parquet
from its own releases. The interface discipline between the two repos is
otherwise excellent (drift checks, both-direction join verification) — the
issue is publishability, not quality.

## 12. Status of the June 360 audit

Resolved and verified still-fixed: the OCS licence leftovers, the row-count
claim, duplicate names (0, validator-gated), the wrong-ECO lot (12 applied, 4
refuted), diacritic tiers 1-3, phantom parents spec-blessed,
`from_position.py` co-canonical fix, CITATION.cff added, spec bumped to v1.1
with history, validator checks 13-20 unconditional, Lichess xref shipped,
`tools/ocn.py` built, ca/es pilot seeded, American-spelling lot applied.

Still open (and carried into the new roadmap): no PGN recipe (H2.1-H2.2);
`deprecated` never exercised (D-5/H2.4); `theoretical` criteria undocumented
(H2.4); 299 no-ECO rows vs spec Goal 3 (H1.5); CI byte-compile drift —
regressed after the fix, proper glob fix unmerged on PR #1 (H0.1); the
~1,400-hit naming-heuristic backlog untriaged; stale README links — new
breakage from the archive move (H0.2).

## 13. Assets to leverage (what is already better than the competition)

1. The manifest engine and its guarantees — a stronger change-control story
   than lichess-org's PR review; should be advertised in CONTRIBUTING, not
   hidden in internal docs.
2. The three-relation model (`parent_ocn1`, `transposes_to`, `same_as`) —
   genuinely novel among open opening datasets, position-verified.
3. The evidence-grading discipline including a public retraction of a
   hallucinated source — exemplary scientific hygiene, ready to be a public
   credibility signal.
4. The docs slug gate (`verify_doc_slugs.py`) — a novel docs-integrity idea
   worth a paragraph in any announcement.
5. The 1:1 Lichess cross-reference — the bridge that makes "layer over, not
   replacement of" credible.
6. An empty Vercel project named `ocn`, one deploy away from being the
   explorer.

---

**Next:** the full plan derived from these findings is
[`traction-roadmap.md`](traction-roadmap.md).
