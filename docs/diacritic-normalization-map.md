# Diacritic normalization map

**Status**: **Tier 1 APPLIED 2026-06-11** under explicit GO (663 rows, sha256
`e6853ef7…` → `a89001c9…`). **Tier 2 APPLIED 2026-06-11** under the wave GO
(50 rows, sha256 `a89001c9…` → `0d3318d4…`). **Tier 3 APPLIED 2026-06-11**
under the fase 2b GO (42 rows, sha256 `8b398ce1…` → `ec91e0d6…`, all 11
xref-discovered forms including the two Lichess-only-evidence entries).
`BANNED_ASCII_NAME_FORMS` carries all 31 variants, populated in the same
commits as their lots and pinned to the generator maps by test. Still
parked (per-row referent evidence needed): Sørensen, Würzburger. The
survey below describes the pre-Tier-1 catalogue (run 2026-06-11, post-P0,
5,899 rows) and is kept as the lots' evidence record.

## Intent

OCN-1 canonical names must spell eponym surnames the way the person spelled
them. This is not a new policy: `spec/OCN-1.md` already defines
`canonical_name` as *"full human-readable name with accents and punctuation"*
and uses `Sämisch` as its worked example. The catalogue violates this at
scale, and inconsistently — the same surname appears in both forms, sometimes
inside one subtree (`E.Gru.Exc` mixes `Grunfeld` and `Grünfeld`). One
evidence-backed, engine-applied lot closes the gap and a validator guard
keeps it closed.

## Policy

1. **Person orthography decides.** Natively Latin-script names take their
   native spelling; the operative source is the person's Wikipedia article
   (with the catalogue's own `attributed_to` strings as internal
   corroboration — e.g. rows already carrying "Géza Maróczy").
2. **Transliterated names stay plain.** Names romanized from Cyrillic or
   other non-Latin scripts use the standard English transliteration with no
   invented diacritics: `Sokolsky`, `Najdorf`, `Alekhine` are correct as-is.
3. **Reference corpora corroborate, they do not decide.** Lichess
   (`lichess-org/chess-openings`) is inconsistent: it spells `Grünfeld`,
   `Réti`, `Sämisch`, `Maróczy`, `Göring`, `Hübner`, `Löwenthal`,
   `Hromádka`, `Møller` with diacritics, but `Ruy Lopez` and the whole
   Czech/Lithuanian class without. Where Lichess agrees it is cited as
   corroboration; where it disagrees the person's orthography wins (rule 1).

## Survey

Word-boundary matches per column, post-P0 catalogue. "rows" = distinct rows
matching in any naming column.

| target | canonical | aliases | notes | attr. fields | rows | families (canonical) |
|---|---:|---:|---:|---:|---:|---|
| López | 273 | 6 | 60 | 1 | 275 | C.RyL, C.Bsh, C.PhD |
| Grünfeld | 149 | 19 | 137 | 0 | 159 | E.Gru, A.EID, A.Eng, A.Hng, B.Sca, D.QPG, D.Tar, E.Bog |
| Réti | 86 | 6 | 79 | 0 | 90 | A.Ret, B.Fre, B.Sic, D.Tar |
| Sämisch | 72 | 16 | 66 | 0 | 79 | E.KID, E.Nim, E.Gru, E.Ben, A.Kan, B.Ale, B.Mod, D.Sla |
| Maróczy | 25 | 14 | 17 | 0 | 32 | B.Sic, B.Ale, B.CaK, B.Fre, C.Fou, C.Ita |
| Göring | 10 | 2 | 10 | 0 | 12 | C.Sco |
| Møller | 7 | 1 | 13 | 0 | 14 | C.Ita |
| Hübner | 5 | 1 | 5 | 0 | 6 | E.Nim |
| Löwenthal | 1 | 1 | 1 | 0 | 2 | B.Sic |
| Hromádka | 0 | 1 | 0 | 0 | 1 | E.Ben |
| Mikėnas? | 27 | 8 | 20 | 0 | 28 | A.Eng, A.Mik, B.Ale, B.Nim, E.Ben, E.Nim |
| Krejčík? | 9 | 4 | 6 | 0 | 10 | A.Hol, B.Ale, C.Bsh |
| Opočenský? | 7 | 4 | 6 | 0 | 9 | B.Sic.Naj, E.Gru |
| Sørensen? | 4 | 4 | 1 | 0 | 4 | B.Fre, C.Cen, C.KGm |
| Pelikán? | 1 | 2 | 0 | 4 | 3 | B.Fre |
| Würzburger? | 0 | 1 | 0 | 0 | 1 | C.Vie |

The audit's estimate was ~570 rows; the real Tier 1 scope is **663 distinct
rows (621 canonical_name changes)** because `Sämisch` (79) and the
`ae`/`oe` transliteration variants (`Gruenfeld`, `Saemisch`, `Huebner`,
`Goering`, `Moeller`, `Loewenthal`) were not in the estimate.

## Tier 1 — the map (GO-ready)

All persons natively Latin-script, orthography unambiguous, Lichess
corroborating except where noted.

| ASCII forms found | normalized | person | evidence |
|---|---|---|---|
| `Lopez` | `López` | Ruy López de Segura | WP person article. Lichess diverges ("Ruy Lopez") — rule 1 wins; spec example + 34 existing `López` rows in-catalogue. |
| `Grunfeld`, `Gruenfeld` | `Grünfeld` | Ernst Grünfeld | WP; Lichess ✓ |
| `Reti` | `Réti` | Richard Réti | WP; Lichess ✓ ("Réti Opening") |
| `Saemisch`, `Samisch` | `Sämisch` | Friedrich Sämisch | WP; Lichess ✓; spec's own example |
| `Maroczy` | `Maróczy` | Géza Maróczy | WP; Lichess ✓; in-catalogue `attributed_to` already "Géza Maróczy" |
| `Goring`, `Goering` | `Göring` | Carl Theodor Göring | WP; Lichess ✓ ("Göring Gambit") |
| `Hubner`, `Huebner` | `Hübner` | Robert Hübner | WP; Lichess ✓ |
| `Lowenthal`, `Loewenthal` | `Löwenthal` | Johann Löwenthal | WP; Lichess ✓ ("Sicilian: Löwenthal Variation") |
| `Hromadka` | `Hromádka` | Karel Hromádka | WP; Lichess ✓; in-catalogue precedent `C.Vie.Nc6.Bc4.Nf6.Hro` |
| `Moller`, `Moeller` | `Møller` | Jørgen Møller (Danish) | WP (Giuoco "Møller Attack"); Lichess ✓ (ø in "Ruy Lopez: Morphy Defense, Møller Variation") |

## Tier 2 — parked, one batched decision

**The Czech/Lithuanian class** — `Mikėnas` (Vladas Mikėnas), `Krejčík`
(Josef Krejčík), `Opočenský` (Karel Opočenský), `Pelikán` (Jiří/Jorge
Pelikán): rule 1 says normalize (all natively Latin-script), but here
Lichess *and* mainstream English literature uniformly use ASCII, unlike the
Tier 1 names where usage is split. Normalizing is policy-coherent but makes
OCN diverge from every reference corpus at once (~50 rows). This is one
decision, taken once for the whole class: **normalize / keep ASCII /
spec-bless ASCII as the documented exception**. Recommendation: normalize,
for coherence with rule 1 — but it needs its own GO, separate from Tier 1.
Note `Pelikán` also touches an applied `attributed_to` string ("Jorge
Pelikan (early adopter)" on `B.Sic.Sve`).

> **Decision 2026-06-11: GO normalize.** Lot prepared as
> `docs/manifests/diacritic-tier2-normalization.manifest.json` (50 rows, 44
> canonical_name; per-surname: Mikėnas 28, Krejčík 10, Opočenský 9,
> Pelikán 3) with dry-run record `docs/archive/diacritic-tier2-dry-run.md`
> (Validation PASS, zero new collisions, structural columns byte-identical,
> candidate green under strict-chess + the four Tier 2 banned forms).
> Review flag: `B.Sic.Sve` updates the applied attribution strings
> (aliases, attributed_to, attribution_source) to "Pelikán". **Apply waits
> for its own GO.** On apply, add the four pairs to
> `BANNED_ASCII_NAME_FORMS` in the same commit.

**Per-row referent cases** — `Sorensen` (4 rows): Lichess itself splits the
spelling by line (ö in "Danish Gambit Declined: Sörensen Defense" and the
two KGA gambits, ø in "French Advance Milner-Barry, Sørensen Variation"),
and the existing in-catalogue `Sörensen` (`C.Vie.Nc6.Srn`) may itself be
ö-for-ø if the referent is the Dane S. A. Sørensen. Needs per-row referent
evidence before any change. `Wurzburger` (1 alias): Lichess uses ASCII
("Wurzburger Trap"); if the eponym is the American Otto Wurzburger, ASCII
is correct and this becomes a documented non-change.

## Tier 3 — Lichess xref discoveries (2026-06-11)

The position-keyed cross-reference (`tools/build_lichess_xref.py`,
consumer sprint fase 1) surfaced 12 further diacritic divergences the
audit-era surveys missed: rows whose Lichess label restores a diacritic
the OCN text dropped. Eleven enter Tier 3 (~42 rows whole-catalogue,
Kádas alone 23):

| ASCII form | normalized | referent | evidence |
|---|---|---|---|
| `Kadas` | `Kádas` | Gábor Kádas | Lichess ✓; Hungarian orthography |
| `Bucker` | `Bücker` | Stefan Bücker | Lichess ✓; WP |
| `Kostic` | `Kostić` | Borislav Kostić | Lichess ✓; WP |
| `Szen` | `Szén` | József Szén | Lichess ✓; WP |
| `Suchting` | `Süchting` | Hugo Süchting | Lichess ✓; WP |
| `Hubsch` | `Hübsch` | Hübsch Gambit | Lichess ✓; German orthography |
| `Dory` | `Döry` | Ladislaus Döry | Lichess ✓; WP |
| `Lohn` | `Löhn` | (no encyclopedia entry found) | Lichess + German orthography only — flagged for review |
| `Schonemann` | `Schönemann` | (no encyclopedia entry found) | Lichess + German orthography only — flagged for review |
| `Dusseldorf` | `Düsseldorf` | place name | unambiguous |
| `Tubingen` | `Tübingen` | place name | unambiguous |

The twelfth divergence is `Sorensen`/`Sörensen` — the xref re-confirms
the split but the **parking stands** (per-row referents; Lichess itself
writes ö and ø on different lines).

## Deliberate non-changes

- `Sokolsky` (8 rows) — Alexey Sokolsky, romanized from Cyrillic; rule 2.
  Lichess ✓ ASCII.
- `Dubois` (3 rows) — Serafino Dubois, Italian; carries no diacritic.
- General: transliterated Russian/Soviet names (`Najdorf` is
  Polish-Argentine and likewise plain) are out of scope by rule 2.

## Mechanics

- One manifest, `ocn.attribution_manifest.v1`, mode `naming_strings_only`,
  generated from this map — never hand-edited. Fields touched:
  `canonical_name`, `aliases`, `notes` (plus one `historical_notes` hit on
  a López row). The engine's field-scope, exact-changed-rows and
  zero-collateral guardrails apply.
- Replacement is per ASCII variant, **word-boundary** (`\bLopez\b`), per
  field. No naming column contains URLs (verified), so no link breakage is
  possible.
- The manifest generator emits, for review, each changed row's slug, family
  and old/new strings — the per-row referent check (every `Grunfeld` in
  `B.Sca` etc. must plausibly refer to the mapped person) happens at that
  review, before GO apply.
- **No alias additions.** Preserving ASCII search forms as aliases is a
  separate decision (it belongs with audit P2 item 17, the
  American-spelling alias lot).
- No `ocn1`, `parent_ocn1`, `moves_uci`, `eco_legacy`, `depth`, `flags`,
  `transposes_to`, `same_as` changes. Slugs are diacritic-free by
  construction (spec §3) and do not move.

## Regression guard

`tools/validate.py` gains a banned-ASCII-forms check (validator wave): the
Tier 1 ASCII variants above, word-boundary, **error** in `canonical_name`
and `aliases`, **warning** in `notes` (notes may legitimately quote titles).
The list ships **empty** in the validator-wave commit (the catalogue still
carries the ASCII forms) and is populated in the same commit that applies
the lot, so guard and data activate atomically. The check mechanism itself
is tested with an injected list from day one.

### Amendment, 2026-08-14: the guard binds `canonical_name` only

`aliases` is exempt. The rule's stated intent, at the top of this document,
is that **canonical names** spell an eponym's surname the way the person
spelled it — an assertion about how a name *should* be written. An alias
asserts nothing; it records how a name *might be searched for*, which is why
the column already holds `Modern Defense`. Applying the rule to both fields
made the catalogue unfindable by the spelling nearly every database, book
index and search box uses, including Lichess's own.

The Non-goals below already deferred this ("**No alias additions.**
Preserving ASCII search forms as aliases is a separate decision"). This is
that decision, and it goes the other way from the guard's first draft.
Nothing in the applied lots changes: 621 canonical names keep their
diacritics and rule 17 still fails on any regression there. Fixture
`tools/tests/fixtures/valid_ascii_alias.csv` pins the exemption;
`invalid_banned_ascii_form.csv` pins that `canonical_name` still errors.

Immediate consequence: the 30 Lichess aliases parked in
[`evidence/provenance/lichess-alias-import.md`](evidence/provenance/lichess-alias-import.md)
(28 `Lopez`, two `Moeller`) become importable.

## Dry-run finding (2026-06-11)

Normalizing `A.Ret` ("Reti Opening" → "Réti Opening") collides with
`A.Ret.d5.c4`, which already carried "Réti Opening": the spelling split was
masking a genuine duplicate name. The whole-catalogue sweep found **no other
new collision**. The pair joins `DUPLICATE_NAME_ALLOWLIST` (with `A.KIA` /
`A.Ret.d5.g3`, the same subtree) pending the duplicate-names decision — the
lot stays purely mechanical and does not invent a differentiating name.

## Release impact

621 `canonical_name` changes force the next release to be a **minor
(1.2.0)** and force `chess-parquet` regeneration, per the audit's release
policy. Bundle with the ECO lot (P1 item 8); hold the tag until both land.

## Expectations (BDD)

1. Given the Tier 1 lot applied, when `validate.py --strict-chess` runs,
   then it reports 5,899 entries, 0 errors, and 0 banned ASCII forms in
   `canonical_name`/`aliases`.
2. Given the manifest dry-run, then the changed-row set is exactly the
   Tier 1 survey set (663 rows; 621 canonical_name) and no field outside
   `{canonical_name, aliases, notes, historical_notes}` differs anywhere.
3. Given the applied CSV, then `ocn1`, `parent_ocn1`, `moves_uci`,
   `eco_legacy`, `depth`, `flags`, `transposes_to`, `same_as` are
   byte-identical to pre-apply for all 5,899 rows.
4. Given a future edit reintroducing `Lopez` in any `canonical_name`, then
   the validator fails.

## Non-goals

No slug changes; no alias additions; no Tier 2 surnames (separate GO); no
ECO or attribution edits (separate lots); no spec text changes.
