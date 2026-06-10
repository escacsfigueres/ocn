# OCN 360° audit — findings and proposals (2026-06-10)

**Status: READ-ONLY AUDIT + PROPOSALS. No catalogue change, no manifest apply,
no tags/release/push.** A 13-agent read-only dynamic workflow audited every
dimension of the project (data, chess structure, ECO accuracy, coverage vs
Lichess, naming style, attribution quality, spec/README, docs hygiene, validator
gaps, tooling, enrichments, consumer experience, release readiness, plus a free
adversarial hunt). The orchestrator **independently re-verified every headline
claim** by re-running the checks (all confirmed; all 125 cited slugs exist in
the catalogue — zero invented references).

Method stats: 13 agents, ~1.07M tokens, 815 tool uses. Severity totals:
**3 critical, 29 high, 48 medium, 34 low.**

## Health dashboard

| Dimension | Health | One-liner |
|---|---|---|
| docs-hygiene | 4/10 | Stale slugs reached the *public contract* (README, spec); no index; 48 flat files |
| spec-readme | 5/10 | LICENSE still says "OCS"; README row count wrong; spec frozen at "Draft v0.1" |
| consumer-sim | 5/10 | `from_position.py` drops co-canonicals; consuming guide outdated on 5 counts |
| eco-accuracy | 6/10 | ~16 rows with demonstrably wrong ECO; no same-moves-ECO-consistency check |
| naming-style | 6/10 | Diacritic splits at scale (López 307, Grünfeld 151, Réti 103); 6 duplicate names |
| attribution-quality | 6/10 | 14 ad-hoc role labels; 3 rows missing role; 1 source contradicts its own row |
| validator-gaps | 6/10 | Several zero-violation checks ready to adopt; name-uniqueness gap proven real |
| tooling-tests | 6/10 | Seed-list drift; 7 tools outside CI byte-compile; CLI flag inconsistency |
| chess-structural | 7/10 | Sound overall; 6 phantom parent-child pairs + 7 inversions invisible to validate.py |
| coverage-gaps | 7/10 | 97% of Lichess corpus name-covered; the 3% gap is label-only, fixable via aliases |
| enrichment-ideas | 7/10 | Highest-value enrichments already half-specified elsewhere; just need design |
| release-strategy | 7/10 | 28 unreleased commits, 17 catalogue rows changed; parquet regen WILL be needed |
| adversarial-meta | 7/10 | Two genuinely wrong opening names found; `deprecated` flag is dead (0 uses) |

## Critical (3)

1. **LICENSE still licenses the old project.** `LICENSE:1` reads "OCS — Open
   Chess Slug" and grants rights over "the OCS-1 specification and catalogues";
   `LICENSE-SPEC:14` directs attribution to `github.com/escacsfigueres/ocs`
   (wrong repo). For a CC-BY-4.0 dataset whose whole point is attribution, the
   attribution target itself is wrong. *(Verified by grep.)* **Fix: S effort —
   rename OCS→OCN, OCN-1, correct the URL in both files.**
2. **`46f7c93` (Lot 3 apply) is unpushed.** The live catalogue state exists
   only locally; any release/tag work before pushing would tag a state absent
   from `origin/main`. *(Verified: ahead 1.)* **Fix: the standing push GO.**
3. **README states "6,099 entries"** (`README.md:84`); the catalogue has 5,899.
   The single most-read number in the repo is wrong. *(Verified by grep.)*

## High — catalogue data errors (all orchestrator-verified)

- **Two openings carry the wrong name:**
  - `A.War.Mad` "Ware Opening, Meadow Hay Trap" has moves `a2a4 e7e5 a4a5 d7d5`
    — but the Meadow Hay Trap is the rook-lift line, and `A.War.e5.Ra3`
    (`a2a4 e7e5 a1a3`) *also* carries the same name. The trap name belongs to
    the Ra3 row; `A.War.Mad` needs renaming.
  - `C.LtO.Nxe5.Qe7` "Latvian Gambit, Greco Variation" — Greco is
    definitionally the 3...Qf6 line, which `C.LtO.Gre` already is. The Qe7 row
    (Behting/Polerio territory) is misnamed, and the catalogue currently has
    two rows with this exact name.
- **6 globally duplicated canonical_names** (no validator check exists):
  the two above plus "English Reversed Sicilian g3, d5", "King's Indian
  Attack", "King's Pawn Game", "Latvian Greco Nc4, fxe4" — each needs
  per-case review (some may be legitimate move-order twins, but the two
  name-errors prove the check earns its keep).
- **ECO misassignments (~16 rows):** `A.Lon` family (10 rows) carries `A48`
  with `1.d4 d5` moves — that is `D02` (A48 is the ...g6 London); 
  `B.Sic.Dra.Yug.Bd7.O-O-O` is a B78 position tagged `B76`; `E.QID.Nim` parent
  E17 sits above E15 children (inversion); `E.Nim.Kas.b6.Bg5` E13→E44;
  `D.Sla.Sch.MLn.Bd3.O-O.Flo`/`.Smy` carry Grünfeld D94 on Slav positions;
  `B.Lio` B00→B07.
- **Diacritic splits at scale** (same surname, two spellings, often within one
  subtree): López/Lopez across 307 `C.RyL` rows; Grünfeld/Grunfeld 151 rows
  (mixed *inside* `E.Gru.Exc`); Réti/Reti 103 rows; smaller splits for Maróczy,
  Göring, Hübner, Sörensen, Sämisch. Also `B.Sic.OKe.c4` spells "Maroczy" in
  its canonical_name while its own `attributed_to` says "Géza Maróczy".
- **`A.Ret` has an empty aliases field** — "Zukertort Opening" (the standard
  name for bare 1.Nf3, explicitly referenced in Lot 3's own historical_notes)
  is invisible to name search. Related: the **Tennison Gambit** sits under
  Scandinavian in OCN but under Zukertort/Réti in Lichess (cross-family
  conflict worth an explicit decision).
- **6 phantom parent-child pairs** (child `moves_uci` *identical* to parent:
  `D.Sla.Cze.Kra.MLn`, `A.Tro.Bxf6.e3`, `E.Gru.Rus.Hng.e4`, `E.QID.Euw.Bd3`,
  `A.Ret.f5.d3.e4`, `A.PQI.e3.Bb7`) plus **7 structural inversions** (child
  shorter than parent with no ancestral FEN link, e.g. `E.Ben.Old`,
  `D.QGD.Ort.Hne.Sws`). All pass `--strict-chess` silently because the SAN
  check only fires on exact parent+1-move extensions.
- **Attribution defects in the pre-engine rows:** 3 of the 26 attributed rows
  lack a role parenthetical (`B.Fre.Exc.Uhl` Uhlmann, `A.KIA.Fre.Bar` Barcza,
  `B.Fre.Kor` Korchnoi — all from the Moskalenko batch); `B.Fre.Kor`'s source
  spells "Kortchnoi" against the row's own "Korchnoi"; 14 distinct role
  parentheticals exist with no enum.
- **Tooling/CI:** `DANGEROUS_SURNAMES` in `audit_naming_attribution.py` has 6
  surnames vs the factory map's verified 9 (misses Nimzowitsch ~126 rows,
  Botvinnik, Keres, Lasker, Paulsen); CI byte-compiles only the 7 original
  tools — the 7 post-bootstrap tools (engine, triage, factory trio,
  transposition audit, export) are outside it; `from_position.py` silently
  drops the shallower co-canonical partner for 7 of 17 `same_as` pairs.
- **Docs/spec contract breaches:** stale (non-existent) slugs appear in
  README.md and spec/OCN-1.md quick-reference tables (the *public* docs, not
  just working notes); spec header still reads "Draft v0.1", dated 2026-04-28
  — and that very header line uses the banned middle-dot separator (one of 18
  raw hits in tracked files).

## Medium / low — by dimension (compact)

- **naming-style:** 4 duplicated comma-segments (`D.QGA.Cls.Ale.MLn.Ale`,
  `C.Vie.Cls.MLn.Nf3.O-O.O-O` + the 2 above); 77 repeated-token names; 24
  identity aliases (alias == canonical_name); 27 aliases colliding with other
  rows' canonical names; possessive forks (Bird's/Bird); KID vs spelled-out
  King's Indian inconsistency (200 vs 65 rows); B.Sic comma fork at depth 2.
- **coverage:** 110/3,695 Lichess entries (3.0%) have no OCN name match — all
  label gaps, not missing positions; 561 British "Defence" rows lack an
  American "Defense" alias; Döry Defense absent; 294 depth≥2 rows carry no ECO
  anchor at all; exact-label coverage of Lichess subvariants is 20.1%.
- **consumer:** `consuming-ocn-0.2.md` wrong on 5 counts (130 vs 124 groups, 6
  vs 17 co-canonical pairs, release link at 1.0.3, aliases/flags columns and
  the lookup tools undocumented); no SAN/PGN→OCN recipe anywhere.
- **chess-structural:** 15 `transposes_to` point at ancestors; 3 in-family
  "Main Line" rows are the non-canonical member of their pair (consumer
  surprise); 6 sibling pairs express same-position with one-way transposes_to
  while 17 pairs elsewhere use bilateral `same_as` (two idioms, one concept).
- **validator-gaps (adoptable, violations counted):** global canonical_name
  uniqueness (6 today → fix data first); alias==canonical warn (24); leading/
  trailing whitespace (2 notes fields); banned chars (0 today — cheap to lock
  in); child-shorter-than-parent warn (12 known exceptions to allowlist).
- **attribution/process:** Maróczy triple shares verbatim boilerplate source;
  Oxford Companion cited with and without edition; `deprecated` flag is
  spec-mandated but used 0 times (no documented protocol); `theoretical` flag
  (105 rows) has no documented criteria.
- **release:** 28 commits unreleased; catalogue delta vs `ocn-1.1.0` = **17
  rows** (16 attribution + 1 canonical_name relabel `E.Nim.Rub.Kmo`) — the
  relabel means **openings.parquet regeneration is required** at next release;
  no 1.1.x runbook exists for the attribution track.

## Proposals — ranked

### P0 — quick wins (each S effort, do as one hygiene wave)

1. **Fix LICENSE + LICENSE-SPEC** (OCS→OCN, URL). Trivial, legal-grade.
2. **README/spec truth pass:** 5,899 count, spec header out of Draft v0.1,
   stale slugs in both, document the 6 missing columns, list post-1.1 tools,
   kill the middle dots. Add **CITATION.cff** (CC-BY wants a canonical cite).
3. **Push `46f7c93`** (standing GO) — precondition for everything release-y.
4. **Naming-error micro-lot** (engine, `naming_strings_only`, ~4 rows):
   rename `A.War.Mad`, rename `C.LtO.Nxe5.Qe7`, fix `B.Sic.OKe.c4`
   Maroczy→Maróczy, add `A.Ret` alias "Zukertort Opening". Dry-run → GO.
5. **Attribution-polish micro-lot** (engine, `attribution_fields_only`, 3-4
   rows): add role parentheticals to Uhlmann/Barcza/Korchnoi rows, harmonize
   Kortchnoi spelling. Define the **role enum** in the methodology doc first
   (14 → ~6 values).
6. **Tooling patches:** sync `DANGEROUS_SURNAMES` to 9; add the 7 missing
   tools to CI byte-compile; `--format` alias on the engine; guard
   `audit_chess.py` missing-path; fix `from_position.py` co-canonical drop.

### P1 — systematic (M effort, each its own gated sprint)

7. **Diacritic normalization lot** (engine, `naming_strings_only`; the
   biggest data-quality win by row count: ~570 rows across López, Grünfeld,
   Réti + small splits). Needs a spec'd normalization map + a validator check
   so it never regresses. Note: canonical_name changes at this scale make the
   next release a **minor (1.2.0)**, and force parquet regen — bundle
   deliberately.
8. **ECO correction lot (~16 rows).** `eco_legacy` is structurally frozen in
   both engine modes — add a third manifest mode **`eco_legacy_only`** to the
   engine (S) and ship the fixes through it, plus the two new validator rules
   (same-moves-ECO-consistency, parent-ECO-inversion).
9. **Validator wave:** global name uniqueness, identity-alias warn,
   whitespace, banned-chars, child-shorter warn (with allowlist), plus a
   documented decision on the 6 phantom pairs + 3 in-family MLn canonicals
   (merge, extend, or spec-bless).
10. **Docs system:** `docs/INDEX.md` + `docs/archive/` convention; expand
    `verify_doc_slugs` standard invocation to README+spec; stale-ref cleanup
    sprint (90 refs in docs/ + the public-doc ones); refresh
    `consuming-ocn-0.2.md` (5 numbers + recipes section).
11. **Release 1.1.x runbook + notes** (the release agent drafted the
    skeleton: 4 categories, 17-row table, parquet regen step, checksum block,
    downstream join-key gate). Decide semver policy: attribution-only = patch
    (1.1.1) vs naming-wave = minor (1.2.0). Recommendation: hold the tag until
    P0 items land, then cut **1.2.0** once the diacritic lot ships (it is the
    consumer-visible event).

### P2 — strategic / enrichment (pick by appetite)

12. **Lichess cross-reference** (sidecar TSV `ocn1 ↔ lichess name/eco`):
    unlocks coverage CI, alias import, popularity later. M effort, high value.
13. **`name_basis` sidecar** (8-category taxonomy already documented; makes
    the do-not-attribute map machine-readable). M effort.
14. **Machine-readable attribution:** `evidence_grade` + structured role as
    sidecar or columns — the manifest JSONs already carry the data; today it
    is stripped at apply time. Design decision: sidecar (no schema break) vs
    15th/16th column (downstream coordination).
15. **`tools/ocn.py` reader** (~50 lines: by-slug, by-FEN, family-walk,
    transposition-resolve) + recipes — directly addresses consumer-sim
    friction with zero schema impact.
16. **i18n Track 2 unblock:** design `ocn-1.aliases.ca.tsv` sidecar and seed
    Catalan as the pilot locale.
17. **American-spelling alias lot** (561 rows, mechanical) and the broader
    Lichess subvariant alias import (L — only with the cross-reference in
    place first).

## Do not do

- Do **not** reopen `transposes_to`/`same_as` resolution (layer CLOSED;
  `unresolved_groups=0` reconfirmed during this audit).
- Do **not** blanket-attribute: the 21 permanent-unattributed families and the
  (now 9) dangerous surnames stand. The audit found no reason to weaken
  head-only discipline.
- Do **not** hand-edit the CSV for any of the above — every catalogue fix goes
  through a manifest (`naming_strings_only`, `attribution_fields_only`, or the
  proposed `eco_legacy_only`), dry-run, GO.

## Proposed next three sprints

1. **Hygiene wave (P0):** push `46f7c93`; LICENSE/README/spec truth pass +
   CITATION.cff; the two engine micro-lots (naming errors, attribution
   polish); tooling patches. One day of work, kills all 3 criticals and the
   most visible highs.
2. **Diacritic + ECO wave (P1 7-9):** spec the normalization map and role
   enum; add `eco_legacy_only` engine mode; ship both lots gated; land the
   validator wave so none of it regresses.
3. **Release 1.2.0 (P1 11):** runbook, notes (17+ rows table), parquet regen
   coordination with chess-parquet, checksums, tag under GO.

## Verification appendix

Orchestrator re-ran and confirmed: LICENSE/LICENSE-SPEC OCS text and URL;
README 6,099; spec Draft v0.1 header; `A.Ret` empty aliases; both Meadow Hay
rows and both Greco rows (names + moves); `B.Fre.Kor` fields (missing role +
Kortchnoi); `A.Lon` A48 vs `1.d4 d5` moves; the 6 duplicate canonical_names;
the 6 phantom parent-child pairs (exact list); `B.Fre.Exc.Uhl` and
`A.KIA.Fre.Bar` missing parentheticals; deprecated=0 and theoretical=105 flag
counts; 28 commits and 17 changed rows (1 canonical_name) since `ocn-1.1.0`;
`DANGEROUS_SURNAMES` = 6 entries in the tool; CI byte-compile list = 7 tools.

Count reconciliations: "90 stale refs" = `verify_doc_slugs docs/*.md` (the
official scan; excludes README/spec, which add the public-contract hits);
the adversarial agent's broader sweep (267 raw / 80 unique) used no
NON-CATALOGUE exemption and a wider file set — both are real, different
denominators. Middle-dot count: 18 raw grep hits, of which several are the
CLAUDE.md rule text itself quoting the banned character; actionable hits
include `spec/OCN-1.md` (header) and `README.md`.

## See also

- [`whole-catalogue-attribution-factory-map.md`](whole-catalogue-attribution-factory-map.md) — the attribution-specific map this audit generalises.
- [`attribution-batch-engine.md`](attribution-batch-engine.md) + [`attribution-factory-tooling.md`](attribution-factory-tooling.md) — the apply pipeline all fix-lots ride.
- [`post-1.1-roadmap.md`](post-1.1-roadmap.md) — tracks; this audit feeds Tracks 1-3.
