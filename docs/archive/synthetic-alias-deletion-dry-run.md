**Status: APPLIED 2026-07-29 under the loop mandate (roadmap H2.6); apply sha256 matched the dry-run prediction** — roadmap H2.6, the
minimum editorial pass. Nothing has been written: `catalog/ocn-1.csv` is
untouched and this report is the dry-run output only. The apply is gated on a
human GO (`--apply --out`), after which this header becomes APPLIED with the
date, per the archive convention.

## What the lot removes

| measure | audit (2026-07) | measured here |
|---|---|---|
| `<SAN> Line` alias strings | 1,726 | **1,730** |
| standalone `Main Line` alias strings | 398 | **398** |
| total alias occurrences deleted | 2,124 | **2,128** |
| alias occurrences in the catalogue | — | 7,456 -> **5,328** |
| rows touched | — | **2,128** (exactly one synthetic entry each) |
| rows whose `aliases` cell becomes empty | — | **1,648** |

The `<SAN> Line` count is exactly 4 above the audit's 1,726, and the difference
is accounted for: 4 occurrences carry a check suffix (`Qa4+ Line`, `Bb4+ Line`)
which the audit's plainer SAN pattern did not match and `SAN_MOVE_RE` does.
1,726 + 4 = 1,730; drop those 4 and every audit figure reproduces exactly. The
202 distinct strings behind the 1,730 occurrences are the measure of how little
information the family carries. The 7,456 -> 5,328 line is the number the H2.3
explorer build already reports for its display filter, which is the point: the
filter and the deletion lot are the same predicate.

## Rule

`web/build.py`'s `is_synthetic_alias`, unchanged and imported rather than
re-implemented: a pipe entry is deleted when it equals `Main Line`, or when it
ends in ` Line` and the preceding token parses as a single SAN move
(`SAN_MOVE_RE` — castling, or an optionally disambiguated piece or pawn move
with optional capture, promotion and check/mate suffix). Surviving entries keep
their original order; a row left with nothing gets an empty cell.

Deliberately **not** in the lot: `Castled Line`, `Fianchetto Line`,
`Small Centre Line`, `D52 Prefix` and the ` Line`-suffixed strings whose head is
a word rather than a move. They read synthetic but name something; widening the
rule to catch them would be a different editorial decision, taken separately.

## Guardrails exercised

`aliases_only` mode (new in H2.6) — the manifest cannot name any column but
`aliases`, so no canonical name, note or attribution is inside this lot's blast
radius. The 2,128 rows that change are exactly `expected_changed_rows`; the
other 3,771 rows are emitted byte-for-byte from the source; `validate.py` passes
on the result with 0 warnings. Check 16 (no alias identical to its own row's
`canonical_name`) still holds after the deletion.

---

# Attribution manifest — Synthetic alias deletion (Main Line / <SAN> Line)

- kind: `ocn.attribution_manifest.v1`
- mode: `aliases_only`
- catalogue: `/Users/albertpi/Code/ocn/catalog/ocn-1.csv`
- rows: 5899 -> 5899
- sha256 before: `091b9b6269404ff7beebbb9239047854fd5abead07ab7326be633f29bc10bd16`
- sha256 after:  `7269fbc0d2171f4e39c967f26ad76cd59b0e14da737c1a3e161c5abfdc864958`
- rows changed: 2128

## Changes

### `D.Cat.Ope.Qa4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qa4+ Line' -> ''

### `D.Sem.Bg5.Mos.Qxf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qxf6 Line' -> ''

### `D.Cat.Ope.Bb4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bb4+ Line' -> ''

### `D.Chi.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Main Line|Chigorin Defense, Main Line|Queen's Gambit Declined: Chigorin Defense, Main Line" -> "Chigorin Defense, Main Line|Queen's Gambit Declined: Chigorin Defense, Main Line"

### `D.Sla.Che.Bf5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bf5 Line' -> ''

### `B.Sca.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `B.Sic.OKe.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `C.RyL.Mor.Ark.Ctr` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c3 Line' -> ''

### `C.Ita.Pia.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf6 Line' -> ''

### `C.Ita.Pia.Wai` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'a6 Line' -> ''

### `D.Sem.Mar.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.Sem.Bg5.Bot.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.QGD.Rag.Bg5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bg5 Line' -> ''

### `C.RyL.Mor.Ark.Qe2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qe2 Line' -> ''

### `C.RyL.Mor.NeA.Ctr` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c3 Line' -> ''

### `D.QGA.Man.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.QGD.Lsk.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.Sem.AMe.Bd3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bd3 Line' -> ''

### `D.Cat.Cls.Qc2.Btr` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'b3 Line' -> ''

### `E.Nim.Rub.Hub.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line|Nimzo-Indian Defense: Rubinstein System, Hübner Variation' -> 'Nimzo-Indian Defense: Rubinstein System, Hübner Variation'

### `E.Nim.Sml.Bot.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.KID.Cls.Byn.Nd2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nd2 Line' -> ''

### `E.KID.Fou.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.Blf.Acc.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line|Blumenfeld Countergambit Accepted' -> 'Blumenfeld Countergambit Accepted'

### `A.OID.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf6 Line' -> ''

### `A.PQI.Bf4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bf4 Line' -> ''

### `E.Ind.Tgo.Nf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf3 Line' -> ''

### `D.QGD.Mar.e4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e4 Line' -> ''

### `D.QGD.Bal.Nc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc3 Line' -> ''

### `A.Lon.Job.Nc6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc6 Line' -> ''

### `C.RyL.Brk.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line|Ruy López: Closed, Breyer Defense' -> 'Ruy López: Closed, Breyer Defense'

### `C.RyL.Brk.Nh4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nh4 Line|Ruy López: Closed, Breyer Defense' -> 'Ruy López: Closed, Breyer Defense'

### `C.RyL.Zai.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `C.RyL.Cha.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line|Ruy López: Closed, Chigorin Defense' -> 'Ruy López: Closed, Chigorin Defense'

### `B.Sic.Cls.Rch.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `B.Sic.Cls.Rch.Bc4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bc4 Line' -> ''

### `B.Sic.Cls.Bol.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.Ben.Mod.Cls.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.Ben.Mod.Cls.Nd2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nd2 Line' -> ''

### `E.Ben.Mod.Cls.Bg5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bg5 Line' -> ''

### `E.Ben.Mod.Cls.Rb1` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Rb1 Line' -> ''

### `E.Ben.Mod.Cls.h3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'h3 Line' -> ''

### `E.Ben.Mod.Fch.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.Ben.Mod.Fch.Nd2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nd2 Line' -> ''

### `E.Ben.Mod.Fch.Bf4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bf4 Line' -> ''

### `E.Ben.Mod.Fou.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.QGD.Vie.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.QGD.Vie.Qa4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qa4 Line' -> ''

### `D.QGD.Ort.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.Sla.Cls.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.Sem.Mer.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.KID.Sml.Ort.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Main Line|King's Indian Defense: Sämisch Variation" -> "King's Indian Defense: Sämisch Variation"

### `E.KID.Sml.Ort.d5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "d5 Line|King's Indian Defense: Sämisch Variation, Closed Variation" -> "King's Indian Defense: Sämisch Variation, Closed Variation"

### `E.KID.Fch.Yug.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `A.Hol.Lng.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `B.Fre.Tar.Cls.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `B.Fre.Tar.Cls.Be7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be7 Line' -> ''

### `B.Fre.Tar.Cls.c5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c5 Line' -> ''

### `B.Sic.Clo.Fch.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.QGD.Tar.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.Sla.Exc.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.Sla.Che.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.Gru.Fch.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.Nim.Lng.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line|Nimzo-Indian Defense: Leningrad Variation, Benoni Defense' -> 'Nimzo-Indian Defense: Leningrad Variation, Benoni Defense'

### `E.KID.Cls.Mar.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.KID.Cls.Pet.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Main Line|King's Indian Defense: Petrosian Variation, Stein Defense" -> "King's Indian Defense: Petrosian Variation, Stein Defense"

### `E.KID.Fch.Pan.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.KID.Avk.Fle.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `A.Kan.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line|Kangaroo Defense, Main Line|Kangaroo Defense: Keres Defense, Transpositional Variation' -> 'Kangaroo Defense, Main Line|Kangaroo Defense: Keres Defense, Transpositional Variation'

### `A.Kan.Nf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf3 Line|Kangaroo Defense, Nf3 Line' -> 'Kangaroo Defense, Nf3 Line'

### `A.OID.Nf6.e4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e4 Line|Old Indian Defense, Nf6 e4 Line' -> 'Old Indian Defense, Nf6 e4 Line'

### `C.Thr.Stn.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `C.KGm.Dec.Fal.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Main Line|King's Gambit Declined: Falkbeer Countergambit, Staunton Line" -> "King's Gambit Declined: Falkbeer Countergambit, Staunton Line"

### `C.KGm.Acc.All.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `C.LtO.Acc.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `C.Ele.Pau.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.Alb.Las.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.Alb.Nrm.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.Bgm.Acc.Ryd.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.Bgm.Dec.Lam.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.Rub.Col.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.QGD.Jan.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.QGD.Bal.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.Sla.Qui.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.Sla.Sch.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.QGD.Mar.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line|QGD Marshall Defense, Main Line' -> 'QGD Marshall Defense, Main Line'

### `E.Ind.QID.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Main Line|Indian Defense, Queen's Indian Main Line" -> "Indian Defense, Queen's Indian Main Line"

### `E.Ind.Tgo.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line|Indian Defense, Tango Main Line' -> 'Indian Defense, Tango Main Line'

### `E.Gru.Brn.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.Nim.Rom.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.KID.Mak.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `A.Eng.Sym.Hdg.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `A.Eng.Sym.Rub.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `A.Eng.Rev.Fou.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `A.Eng.Rev.Bot.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `A.Eng.Mik.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `A.Ret.KIA.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `A.Ret.Nim.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `A.Lon.Cls.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `A.Col.Kol.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `A.Pol.Cen.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `B.Sic.Naj.Eng.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `B.Sic.Naj.Pol.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `B.Sic.Dra.Yug.Sol.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `B.Sic.Dra.Cls.Nrm.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `B.Sic.Acc.Mar.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `B.Sic.Sch.Eng.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `B.Sic.Kan.Tal.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `B.Sic.Ros.Nim.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `B.Fre.Win.Psn.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `B.CaK.Adv.Sht.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `C.RyL.Mar.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `C.RyL.Ber.Wal.End.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `C.RyL.Mor.Opn.Rig.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `C.RyL.Exc.Alk.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `C.Ita.Giu.Cls.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `C.Ita.Evn.Dec.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `C.Ita.Pia.Nf6.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `C.Pet.Cls.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `C.Pet.Mod.Stn.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `C.Sco.Mie.Pot.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.QGD.Ort.Rub.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.QGD.Ort.Cap.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.QGD.Tar.Mak.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.QGD.Lsk.Te7.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.Sla.Exc.MLn.e3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e3 Line' -> ''

### `D.Sla.Che.MLn.a4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'a4 Line' -> ''

### `D.Sem.Mer.Rab.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.Sem.Bg5.AMo.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.QGA.Cls.Rub.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.Cat.Ope.Yug.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.Bog.Nim.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.Bog.WSm.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.Bud.Adl.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.Bud.Rub.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.OldI.Cls.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.OldI.Fch.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.Blf.Dec.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.Blf.Spl.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.Nim.Rub.Tai.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.QID.Pet.Kas.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `A.War.Mad.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `A.Ama.Par.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `A.Sod.Dur.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `A.Mie.ReR.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `A.Mie.Ven.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `A.Mik.Ker.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `A.Kan.MLn.e3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e3 Line' -> ''

### `B.Brg.Gro.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `B.StG.Bas.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `B.Lio.Han.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `B.Rat.Sma.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line|Rat Small Center, Main Line' -> 'Rat Small Center, Main Line'

### `B.Car.Ham.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `B.Gld.Pck.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `B.Hip.Ama.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `B.War.Mat.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line|Ware Defense Meadow, Main Line' -> 'Ware Defense Meadow, Main Line'

### `B.Mod.Avk.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line|Modern Averbakh Kotov via 1.d4 move-order' -> 'Modern Averbakh Kotov via 1.d4 move-order'

### `B.OwM.Smi.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `C.Dam.Nim.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `C.Dam.Ger.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `C.Pon.Jae.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `C.Pon.Ste.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `C.Thr.Win.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `C.Ele.Nor.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `C.Cen.Dsh.Acc.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `C.Bsh.Urs.Kei.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `C.PhD.Nim.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `C.Vie.Gbt.Fal.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.QGD.Tar.MLn.Bd3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bd3 Line' -> ''

### `D.Sla.Cls.MLn.e4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e4 Line' -> ''

### `D.Sla.Qui.MLn.Bd3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bd3 Line' -> ''

### `D.Sem.Bg5.Bot.Ekf.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.Sem.Mer.Lun.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.QGA.Cen.Mod.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.Cat.Cls.Kor.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.QPG.Zuk.Col.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.Bgm.Acc.Ryd.MLn.Be3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be3 Line' -> ''

### `E.Bog.Nim.MLn.Be2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be2 Line' -> ''

### `E.Bud.Adl.MLn.e3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e3 Line' -> ''

### `E.OldI.Cls.MLn.Re1` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Re1 Line' -> ''

### `E.Blf.Dec.MLn.e3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e3 Line' -> ''

### `E.Nim.Rub.Tai.MLn.Qc2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qc2 Line' -> ''

### `E.QID.Pet.Kas.MLn.e4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e4 Line' -> ''

### `E.KID.Mak.MLn.Be2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be2 Line' -> ''

### `E.Gru.Brn.MLn.Be2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be2 Line' -> ''

### `E.Nim.Rom.MLn.Nf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf3 Line' -> ''

### `E.Ind.Tgo.MLn.Nc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc3 Line' -> ''

### `A.Owe.Fch.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line|Owen Defense Fianchetto, Main Line' -> 'Owen Defense Fianchetto, Main Line'

### `A.VtK.FrD.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `A.VtK.Sic.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `A.Hor.Ker.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line|Horwitz Keres Defense, Main Line' -> 'Horwitz Keres Defense, Main Line'

### `A.Hor.Fch.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `A.And.Pol.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `A.Clm.Spk.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `A.Egl.Har.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `A.OID.Mod.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `A.Ret.KIA.MLn.e4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e4 Line' -> ''

### `B.Nim.Ken.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `B.Nim.ScD.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `B.Nim.Col.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `B.Mod.Tig.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `B.Mod.Pte.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `B.OwM.Mat.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `B.OwM.Eng.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `B.Sca.Mod.Mie.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `B.Ale.Mod.KID.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `B.Pir.150.Arg.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `C.KPO.Kgt.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Main Line|King's Knight Opening: Normal Variation" -> "King's Knight Opening: Normal Variation"

### `C.KPO.Nap.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `C.KPO.Prt.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `C.Fou.Glk.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `C.Fou.Sco.Bel.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `C.Fou.Spa.Rub.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `C.Sco.Gor.Nc3.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `C.Sco.Gbt.Max.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `C.KGm.Dec.Cls.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `C.KGm.Acc.Muz.Dbl.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.Chi.MLn.e3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e3 Line' -> ''

### `D.Chi.Exc.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.Tar.Cls.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.Tar.Prg.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.STa.Exc.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.STa.Pil.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.QGA.Old.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.QGA.Ale.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.Cat.Ope.Qa4.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.Bgm.Dec.Lam.MLn.Qd2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qd2 Line' -> ''

### `E.KID.Cls.Mar.MLn.Nd3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nd3 Line' -> ''

### `E.KID.Cls.Pet.MLn.c5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c5 Line' -> ''

### `E.KID.Fch.Pan.MLn.b3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'b3 Line' -> ''

### `E.Gru.Exc.Cla.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.Gru.Rus.Hng.Be2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be2 Line' -> ''

### `E.QID.Mod.Fch.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Main Line|Queen's Indian Defense: Classical Variation, Traditional Variation" -> "Queen's Indian Defense: Classical Variation, Traditional Variation"

### `E.QID.Nim.Tim.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.Bog.Ret.Fch.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.Ind.QID.MLn.e3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e3 Line' -> ''

### `A.Ama.Par.MLn.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf6 Line' -> ''

### `A.Sod.Dur.MLn.Nc6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc6 Line' -> ''

### `A.Owe.Fch.MLn.Ne2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Ne2 Line' -> ''

### `A.VtK.FrD.MLn.Bd6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bd6 Line' -> ''

### `A.VtK.Sic.MLn.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf6 Line' -> ''

### `A.Hor.Ker.MLn.a3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'a3 Line' -> ''

### `A.Hor.Fch.MLn.Nf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf3 Line' -> ''

### `A.And.Pol.MLn.e5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e5 Line' -> ''

### `A.Clm.Spk.MLn.d5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd5 Line' -> ''

### `A.Ret.KIA.MLn.e4.c5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c5 Line' -> ''

### `B.Nim.Ken.MLn.Nf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf3 Line' -> ''

### `B.Nim.ScD.MLn.Nf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf3 Line' -> ''

### `B.Nim.Col.MLn.d4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd4 Line' -> ''

### `B.Mod.Tig.MLn.e5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e5 Line' -> ''

### `B.Mod.Pte.MLn.Bc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bc3 Line' -> ''

### `B.OwM.Mat.MLn.c3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c3 Line' -> ''

### `B.OwM.Eng.MLn.Bd3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bd3 Line' -> ''

### `B.Sca.Mod.Mie.MLn.Bc4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bc4 Line' -> ''

### `B.Ale.Mod.KID.MLn.cxd6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'cxd6 Line' -> ''

### `C.KPO.Kgt.MLn.a3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'a3 Line' -> ''

### `C.KPO.Nap.MLn.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf6 Line' -> ''

### `C.KPO.Prt.MLn.c6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c6 Line' -> ''

### `C.Fou.Glk.MLn.Bg2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bg2 Line' -> ''

### `C.Fou.Sco.Bel.MLn.Nxd4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nxd4 Line' -> ''

### `C.Fou.Spa.Rub.MLn.b5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'b5 Line' -> ''

### `C.Sco.Gor.Nc3.MLn.Bd3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bd3 Line' -> ''

### `C.Sco.Gbt.Max.MLn.c3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c3 Line' -> ''

### `C.KGm.Dec.Cls.MLn.d4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd4 Line' -> ''

### `C.KGm.Acc.Muz.Dbl.MLn.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf6 Line' -> ''

### `D.Chi.MLn.e3.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf6 Line' -> ''

### `D.Chi.Exc.MLn.e3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e3 Line' -> ''

### `D.Tar.Cls.MLn.Re8` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Re8 Line' -> ''

### `D.Tar.Prg.MLn.Nxd4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nxd4 Line' -> ''

### `D.STa.Exc.MLn.Nxc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nxc3 Line' -> ''

### `D.STa.Pil.MLn.Nxd4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nxd4 Line' -> ''

### `D.QGA.Old.MLn.exd4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'exd4 Line' -> ''

### `D.QGA.Ale.MLn.Bb3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bb3 Line' -> ''

### `D.Cat.Ope.Qa4.MLn.c5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c5 Line' -> ''

### `D.Bgm.Dec.Lam.MLn.Qd2.e6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e6 Line' -> ''

### `E.QID.Nim.Tim.MLn.Nc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc3 Line' -> ''

### `E.Bog.Ret.Fch.MLn.O-O` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'O-O Line' -> ''

### `E.Ind.QID.MLn.e3.Be7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be7 Line' -> ''

### `E.KID.Cls.Mar.MLn.Nd3.f5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'f5 Line' -> ''

### `E.KID.Cls.Pet.MLn.c5.Na6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Na6 Line' -> ''

### `E.KID.Fch.Pan.MLn.b3.Bd7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bd7 Line' -> ''

### `E.KID.Fou.MLn.Cap.fxe6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'fxe6 Line' -> ''

### `E.Gru.Exc.Cla.MLn.O-O` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'O-O Line' -> ''

### `E.Gru.Rus.Hng.Be2.Nc6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc6 Line' -> ''

### `E.QID.Mod.Fch.MLn.d5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "d5 Line|Queen's Indian Defense: Classical Variation, Traditional Variation, Nimzowitsch Line" -> "Queen's Indian Defense: Classical Variation, Traditional Variation, Nimzowitsch Line"

### `A.Ama.Par.MLn.Nf6.d4.Nc6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc6 Line' -> ''

### `A.Sod.Dur.MLn.Nc6.g3.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf6 Line' -> ''

### `A.Owe.Fch.MLn.Ne2.a6.Bd3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bd3 Line' -> ''

### `A.VtK.FrD.MLn.Bd6.Bd3.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf6 Line' -> ''

### `A.VtK.Sic.MLn.Nf6.Bg5.Be7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be7 Line' -> ''

### `A.Hor.Ker.MLn.a3.Bd6.e3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e3 Line' -> ''

### `A.Hor.Fch.MLn.Nf3.Be7.e3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e3 Line' -> ''

### `A.And.Pol.MLn.e5.Bb2.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf6 Line' -> ''

### `A.Clm.Spk.MLn.d5.Bg2.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf6 Line' -> ''

### `A.Ret.KIA.MLn.e4.c5.b6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'b6 Line' -> ''

### `B.Nim.Ken.MLn.Nf3.d6.Nc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc3 Line' -> ''

### `B.Nim.ScD.MLn.Nf3.e6.Be2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be2 Line' -> ''

### `B.Nim.Col.MLn.d4.Bxf5.Bd3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bd3 Line' -> ''

### `B.Mod.Tig.MLn.e5.Nd7.Bd3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bd3 Line' -> ''

### `B.Mod.Pte.MLn.Bc3.cxd4.Nxd4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nxd4 Line' -> ''

### `B.OwM.Mat.MLn.c3.Nf6.Bg5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bg5 Line' -> ''

### `B.OwM.Eng.MLn.Bd3.Nf6.O-O` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'O-O Line' -> ''

### `B.Sca.Mod.Mie.MLn.Bc4.e6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e6 Line' -> ''

### `B.Ale.Mod.KID.MLn.cxd6.Be2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be2 Line' -> ''

### `B.Pir.150.Arg.MLn.Lng.Nbd7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nbd7 Line' -> ''

### `C.KPO.Nap.MLn.Nf6.Nc3.Bc5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bc5 Line' -> ''

### `C.KPO.Prt.MLn.c6.Ba4.d6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd6 Line' -> ''

### `C.Fou.Glk.MLn.Bg2.dxe4.Nxe4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nxe4 Line' -> ''

### `C.Fou.Sco.Bel.MLn.Nxd4.d6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd6 Line' -> ''

### `C.Fou.Spa.Rub.MLn.b5.Nxb5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nxb5 Line' -> ''

### `C.Sco.Gor.Nc3.MLn.Bd3.d6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd6 Line' -> ''

### `C.Sco.Gbt.Max.MLn.c3.dxc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'dxc3 Line' -> ''

### `C.KGm.Dec.Cls.MLn.d4.Bb6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bb6 Line' -> ''

### `C.KGm.Acc.Muz.Coc.exd5.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf6 Line' -> ''

### `D.Chi.MLn.e3.Nf6.Nc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc3 Line' -> ''

### `D.Chi.Exc.MLn.e3.Qd8.Nf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf3 Line' -> ''

### `D.Tar.Cls.MLn.Re8.Re1` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Re1 Line' -> ''

### `D.Tar.Prg.MLn.Nxd4.Qb6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qb6 Line' -> ''

### `D.STa.Exc.MLn.Nxc3.Qb3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qb3 Line' -> ''

### `D.STa.Pil.MLn.Nxd4.a6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'a6 Line' -> ''

### `D.QGA.Old.MLn.exd4.Be7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be7 Line' -> ''

### `D.QGA.Ale.MLn.Bb3.e6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e6 Line' -> ''

### `D.Cat.Ope.Qa4.MLn.c5.dxc5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'dxc5 Line' -> ''

### `D.Bgm.Acc.Ryd.MLn.Be3.Qd6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qd6 Line' -> ''

### `E.QID.Nim.Tim.MLn.Nc3.d5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd5 Line' -> ''

### `E.Bog.Ret.Fch.MLn.O-O.Nc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc3 Line' -> ''

### `E.Ind.QID.MLn.e3.Be7.Be2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be2 Line' -> ''

### `E.KID.Cls.Mar.MLn.Nd3.c5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c5 Line' -> ''

### `E.KID.Fch.Pan.MLn.b3.Re8` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Re8 Line' -> ''

### `E.KID.Fou.MLn.Cap.fxe6.Be3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be3 Line' -> ''

### `E.Gru.Exc.Cla.MLn.O-O.Qc2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qc2 Line' -> ''

### `E.Gru.Rus.Hng.Be2.Nc6.h3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'h3 Line' -> ''

### `E.QID.Mod.Fch.MLn.d5.Ne5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Ne5 Line' -> ''

### `E.Nim.Rub.Tai.MLn.Qc2.c5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c5 Line' -> ''

### `A.Ama.Par.MLn.Nf6.d4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd4 Line' -> ''

### `A.Sod.Dur.MLn.Nc6.g3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'g3 Line' -> ''

### `A.Owe.Fch.MLn.Ne2.a6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'a6 Line' -> ''

### `A.VtK.FrD.MLn.Bd6.Bd3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bd3 Line' -> ''

### `A.VtK.Sic.MLn.Nf6.Bg5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bg5 Line' -> ''

### `A.Hor.Ker.MLn.a3.Bd6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bd6 Line' -> ''

### `A.Hor.Fch.MLn.Nf3.Be7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be7 Line' -> ''

### `A.And.Pol.MLn.e5.Bb2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bb2 Line' -> ''

### `A.Clm.Spk.MLn.d5.Bg2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bg2 Line' -> ''

### `A.Ret.KIA.MLn.e4.c5.Nc6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc6 Line' -> ''

### `B.Nim.Ken.MLn.Nf3.d6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd6 Line' -> ''

### `B.Nim.ScD.MLn.Nf3.e6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e6 Line' -> ''

### `B.Nim.Col.MLn.d4.Bxf5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bxf5 Line' -> ''

### `B.Mod.Tig.MLn.e5.Nd7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nd7 Line' -> ''

### `B.Mod.Pte.MLn.Bc3.cxd4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'cxd4 Line' -> ''

### `B.OwM.Mat.MLn.c3.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf6 Line' -> ''

### `B.OwM.Eng.MLn.Bd3.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf6 Line' -> ''

### `B.Sca.Mod.Mie.MLn.Bc4.Bg4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bg4 Line' -> ''

### `B.Ale.Mod.KID.MLn.cxd6.Bg7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bg7 Line' -> ''

### `B.Pir.150.Arg.MLn.Lng.a5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'a5 Line' -> ''

### `C.KPO.Kgt.MLn.a3.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf6 Line' -> ''

### `C.KPO.Nap.MLn.Nf6.Nc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc3 Line' -> ''

### `C.KPO.Prt.MLn.c6.Ba4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Ba4 Line' -> ''

### `C.Fou.Glk.MLn.Bg2.dxe4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'dxe4 Line' -> ''

### `C.Fou.Sco.Bel.MLn.Nxd4.Bc5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bc5 Line' -> ''

### `C.Fou.Spa.Rub.MLn.b5.Bb3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bb3 Line' -> ''

### `C.Sco.Gor.Nc3.MLn.Bd3.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf6 Line' -> ''

### `C.Sco.Gbt.Max.MLn.c3.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf6 Line' -> ''

### `C.KGm.Dec.Cls.MLn.d4.exd4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'exd4 Line' -> ''

### `C.KGm.Acc.Muz.Coc.exd5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'exd5 Line' -> ''

### `D.Chi.MLn.e3.Nf6.Be2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be2 Line' -> ''

### `D.Chi.Exc.MLn.e3.Qd8` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qd8 Line' -> ''

### `D.Tar.Cls.MLn.Re8.Be3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be3 Line' -> ''

### `D.Tar.Prg.MLn.Nxd4.Be6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be6 Line' -> ''

### `D.STa.Exc.MLn.Nxc3.bxc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'bxc3 Line' -> ''

### `D.STa.Pil.MLn.Nxd4.Be7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be7 Line' -> ''

### `D.QGA.Old.MLn.exd4.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf6 Line' -> ''

### `D.QGA.Ale.MLn.Bb3.Nc6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc6 Line' -> ''

### `D.Cat.Ope.Qa4.MLn.c5.O-O` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'O-O Line' -> ''

### `D.Bgm.Acc.Ryd.MLn.Be3.Nc6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc6 Line' -> ''

### `E.QID.Nim.Tim.MLn.Nc3.O-O` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'O-O Line' -> ''

### `E.Bog.Ret.Fch.MLn.O-O.d5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd5 Line' -> ''

### `E.Ind.QID.MLn.e3.Be7.Bd3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bd3 Line' -> ''

### `E.KID.Cls.Mar.MLn.Nd3.h6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'h6 Line' -> ''

### `E.KID.Cls.Pet.MLn.c5.c6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c6 Line' -> ''

### `E.KID.Fch.Pan.MLn.b3.b5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'b5 Line' -> ''

### `E.KID.Fou.MLn.Cap.fxe6.Be2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be2 Line' -> ''

### `E.Gru.Exc.Cla.MLn.O-O.e5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e5 Line' -> ''

### `E.Gru.Rus.Hng.Be2.Nc6.O-O` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'O-O Line' -> ''

### `E.QID.Mod.Fch.MLn.d5.cxd5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'cxd5 Line' -> ''

### `E.Ben.Mod.Cls.MLn.Re1` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Re1 Line' -> ''

### `E.Ben.Mod.Cls.MLn.h3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'h3 Line' -> ''

### `E.Ben.Mod.Fch.MLn.O-O` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'O-O Line' -> ''

### `E.Ben.Mod.Fch.MLn.h3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'h3 Line' -> ''

### `E.Ben.Mod.Fou.MLn.Be3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be3 Line' -> ''

### `E.Ben.Mod.Fou.MLn.Bd3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bd3 Line' -> ''

### `A.Eng.Sym.Hdg.MLn.b3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'b3 Line' -> ''

### `A.Eng.Sym.Hdg.MLn.Qa4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qa4 Line' -> ''

### `A.Eng.Sym.Rub.MLn.Be2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be2 Line' -> ''

### `A.Eng.Rev.Fou.MLn.Bg2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bg2 Line' -> ''

### `B.Sic.Cls.Rch.MLn.Kb1` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Kb1 Line' -> ''

### `B.Sic.Cls.Bol.MLn.Be3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be3 Line' -> ''

### `B.Fre.Tar.Cls.MLn.Ngf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Ngf3 Line' -> ''

### `B.Sic.Clo.Fch.MLn.Nge2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nge2 Line' -> ''

### `B.Sic.Naj.Eng.MLn.f3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'f3 Line' -> ''

### `B.Sic.Naj.Pol.MLn.Qf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qf3 Line' -> ''

### `B.Sic.Dra.Yug.Sol.MLn.Bb3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bb3 Line' -> ''

### `B.Sic.Dra.Cls.Nrm.MLn.Qd2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qd2 Line' -> ''

### `B.Sic.Acc.Mar.MLn.Be3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be3 Line' -> ''

### `B.Fre.Win.Psn.MLn.Nf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf3 Line' -> ''

### `C.RyL.Mor.Opn.Rig.MLn.Re1` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Re1 Line' -> ''

### `C.RyL.Exc.Alk.MLn.Nc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc3 Line' -> ''

### `C.Ita.Giu.Cls.MLn.Nc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc3 Line' -> ''

### `C.Ita.Evn.Dec.MLn.O-O` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'O-O Line' -> ''

### `C.Ita.Pia.Nf6.MLn.Re1` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Re1 Line' -> ''

### `C.Pet.Mod.Stn.MLn.Re1` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Re1 Line' -> ''

### `C.Sco.Mie.Pot.MLn.Kb1` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Kb1 Line' -> ''

### `C.Cen.Dsh.Acc.MLn.Nxc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nxc3 Line' -> ''

### `C.Bsh.Urs.Kei.MLn.Re1` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Re1 Line' -> ''

### `C.Vie.Gbt.Fal.MLn.Nf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf3 Line' -> ''

### `D.QGD.Ort.Rub.MLn.Re1` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Re1 Line' -> ''

### `D.QGD.Ort.Cap.MLn.O-O` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'O-O Line' -> ''

### `D.QGD.Tar.Mak.MLn.Re1` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Re1 Line' -> ''

### `D.QGD.Lsk.Te7.MLn.O-O` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'O-O Line' -> ''

### `D.Sla.Exc.MLn.e3.Nf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf3 Line' -> ''

### `D.Sem.Mer.Rab.MLn.O-O` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'O-O Line' -> ''

### `D.Sem.Bg5.AMo.MLn.Be2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be2 Line' -> ''

### `D.QGA.Cls.Rub.MLn.Qe2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qe2 Line' -> ''

### `D.Cat.Ope.Yug.MLn.Qxc4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qxc4 Line' -> ''

### `D.QPG.Zuk.Col.MLn.O-O` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'O-O Line' -> ''

### `E.Nim.Rub.Hub.MLn.O-O` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'O-O Line' -> ''

### `E.Nim.Sml.Bot.MLn.Bd3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bd3 Line' -> ''

### `E.KID.Sml.Ort.MLn.Qd2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qd2 Line' -> ''

### `E.KID.Sml.Ort.d5.Nge2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nge2 Line' -> ''

### `E.KID.Fch.Yug.MLn.d5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "d5 Line|King's Indian Defense: Fianchetto Variation, Yugoslav Variation, Advance Line" -> "King's Indian Defense: Fianchetto Variation, Yugoslav Variation, Advance Line"

### `E.KID.Cls.Mar.MLn.f3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'f3 Line' -> ''

### `E.KID.Cls.Pet.MLn.Ne1` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Ne1 Line' -> ''

### `E.KID.Fch.Pan.MLn.e4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e4 Line' -> ''

### `E.QID.Pet.Kas.MLn.Nc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc3 Line' -> ''

### `E.Bud.Adl.MLn.e3.Be2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be2 Line' -> ''

### `E.Ben.Mod.Cls.MLn.Re1.Nbd7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nbd7 Line' -> ''

### `E.Ben.Mod.Cls.MLn.h3.Re8` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Re8 Line' -> ''

### `E.Ben.Mod.Fch.MLn.O-O.Nbd7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nbd7 Line' -> ''

### `E.Ben.Mod.Fch.MLn.h3.Re8` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Re8 Line' -> ''

### `E.Ben.Mod.Fou.MLn.Be3.Re8` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Re8 Line' -> ''

### `E.Ben.Mod.Fou.MLn.Bd3.Na6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Na6 Line' -> ''

### `A.Eng.Sym.Hdg.MLn.b3.O-O` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'O-O Line' -> ''

### `A.Eng.Sym.Hdg.MLn.Qa4.O-O` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'O-O Line' -> ''

### `A.Eng.Sym.Rub.MLn.Be2.O-O` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'O-O Line' -> ''

### `A.Eng.Rev.Fou.MLn.Bg2.Nb6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Nb6 Line|Reversed Dragon|English Opening: King's English Variation, Four Knights Variation, Fianchetto Line, with Nb6" -> "Reversed Dragon|English Opening: King's English Variation, Four Knights Variation, Fianchetto Line, with Nb6"

### `B.Sic.Cls.Rch.MLn.Kb1.Bd7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bd7 Line' -> ''

### `B.Sic.Cls.Bol.MLn.Be3.Be6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be6 Line' -> ''

### `B.Fre.Tar.Cls.MLn.Ngf3.c5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c5 Line' -> ''

### `B.Sic.Clo.Fch.MLn.Nge2.e6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e6 Line' -> ''

### `B.Sic.Naj.Eng.MLn.f3.Nbd7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nbd7 Line' -> ''

### `B.Sic.Naj.Pol.MLn.Qf3.Bb7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bb7 Line' -> ''

### `B.Sic.Dra.Yug.Sol.MLn.h4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'h4 Line' -> ''

### `B.Sic.Dra.Cls.Nrm.MLn.h4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'h4 Line' -> ''

### `B.Sic.Acc.Mar.MLn.Be3.Be6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be6 Line' -> ''

### `B.Fre.Win.Psn.MLn.Nf3.Nbc6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nbc6 Line' -> ''

### `C.RyL.Mor.Opn.Rig.MLn.c3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c3 Line' -> ''

### `C.Ita.Evn.Dec.MLn.O-O.d6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd6 Line' -> ''

### `C.Ita.Pia.Nf6.MLn.Re1.a6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'a6 Line' -> ''

### `C.Pet.Mod.Stn.MLn.Re1.Be7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be7 Line' -> ''

### `C.Sco.Mie.Pot.MLn.Kb1.Re8` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Re8 Line' -> ''

### `C.Cen.Dsh.Acc.MLn.Nxc3.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf6 Line' -> ''

### `C.Bsh.Urs.Kei.MLn.Re1.Be7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be7 Line' -> ''

### `C.Vie.Gbt.Fal.MLn.Nf3.Be7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be7 Line|Vienna Game: Vienna Gambit, Breyer Variation' -> 'Vienna Game: Vienna Gambit, Breyer Variation'

### `D.QGD.Ort.Rub.MLn.Re1.cxd4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'cxd4 Line' -> ''

### `D.QGD.Ort.Cap.MLn.O-O.b5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'b5 Line' -> ''

### `D.QGD.Tar.Mak.MLn.Re1.Nbd7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nbd7 Line' -> ''

### `D.QGD.Lsk.Te7.MLn.O-O.Bg4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bg4 Line' -> ''

### `D.Sla.Exc.MLn.e3.Nf3.e6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e6 Line' -> ''

### `D.Sem.Mer.Rab.MLn.O-O.c5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c5 Line' -> ''

### `D.Sem.Bg5.AMo.MLn.Be2.Nbd7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nbd7 Line' -> ''

### `D.QGA.Cls.Rub.MLn.Qe2.Be7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be7 Line' -> ''

### `D.Cat.Ope.Yug.MLn.Qxc4.b5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'b5 Line' -> ''

### `D.QPG.Zuk.Col.MLn.O-O.Bd6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bd6 Line' -> ''

### `E.Nim.Rub.Hub.MLn.O-O.O-O` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'O-O Line|Nimzo-Indian Defense: Rubinstein System, Hübner Variation' -> 'Nimzo-Indian Defense: Rubinstein System, Hübner Variation'

### `E.Nim.Sml.Bot.MLn.Bd3.Nc6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc6 Line' -> ''

### `E.KID.Sml.Ort.MLn.Qd2.exd4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'exd4 Line' -> ''

### `E.KID.Sml.Ort.d5.Nge2.a5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'a5 Line' -> ''

### `E.KID.Fch.Yug.MLn.d5.Ne5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Ne5 Line' -> ''

### `E.KID.Cls.Mar.MLn.f3.f5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "f5 Line|King's Indian Defense: Orthodox Variation, Classical System, Traditional Line" -> "King's Indian Defense: Orthodox Variation, Classical System, Traditional Line"

### `E.KID.Fch.Pan.MLn.e4.e5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e5 Line' -> ''

### `E.Bud.Adl.MLn.e3.Be2.Re8` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Re8 Line' -> ''

### `B.Sic.Sve.Nd5.Qa5.Bd2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bd2 Line' -> ''

### `C.Ita.Two.Ng5.Trx.Bxf7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bxf7 Line|Italian Game: Two Knights Defense, Traxler Counterattack, Bishop Sacrifice Line' -> 'Italian Game: Two Knights Defense, Traxler Counterattack, Bishop Sacrifice Line'

### `C.Ita.Two.Ng5.Feg.Kxf7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Kxf7 Line' -> ''

### `C.Ita.Two.Ng5.Ulv.Bxb5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bxb5 Line' -> ''

### `C.Ita.Two.Ng5.Pol.Bb5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bb5 Line|Polerio Defense, Bb5|Italian Game: Two Knights Defense, Polerio Defense, Bishop Check Line' -> 'Polerio Defense, Bb5|Italian Game: Two Knights Defense, Polerio Defense, Bishop Check Line'

### `D.Cat.Ope.Qa4.Ale.Be7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be7 Line' -> ''

### `C.RyL.Mor.Opn.Dil.Rxf2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Rxf2 Line' -> ''

### `C.RyL.Mor.Opn.Hwl.Nc5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc5 Line' -> ''

### `C.RyL.Mor.StD.Sie.exf5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'exf5 Line' -> ''

### `C.Ita.Two.Ng5.Frt.c3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c3 Line' -> ''

### `C.Ita.Two.Ng5.Lol.exd4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'exd4 Line' -> ''

### `C.Ita.Evn.Acc.Stn.O-O` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'O-O Line|Italian Game: Evans Gambit, Slow Variation' -> 'Italian Game: Evans Gambit, Slow Variation'

### `C.RyL.Mor.Ark.Ctr.Nxe4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nxe4 Line' -> ''

### `B.Sic.Dra.Yug.Chn.Bb3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bb3 Line' -> ''

### `C.RyL.Mor.Ark.Qe2.d6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd6 Line' -> ''

### `C.RyL.Mor.NeA.Ctr.d6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd6 Line' -> ''

### `C.Ita.Evn.Acc.Mor.d6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd6 Line' -> ''

### `C.Ita.Two.Ng5.Nxd.d3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd3 Line' -> ''

### `D.Cat.Cls.Qc2.Btr.Bb7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bb7 Line' -> ''

### `D.Cat.Ope.Bb4.Mod.O-O` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'O-O Line' -> ''

### `E.Nim.Cls.Zur.Mil.e3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e3 Line' -> ''

### `E.KID.Cls.Byn.Nd2.a5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'a5 Line' -> ''

### `B.Sic.Cls.Rch.Lip.Bd7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bd7 Line' -> ''

### `B.Sic.Cls.Rch.Psn.O-O-O` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'O-O-O Line' -> ''

### `B.Sic.Cls.Rch.Drg.O-O-O` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'O-O-O Line' -> ''

### `B.Sic.Cls.Rch.Bc4.Be7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be7 Line' -> ''

### `B.Sic.Cls.Soz.Vel.O-O` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'O-O Line' -> ''

### `B.Sic.Cls.Soz.Fis.O-O` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'O-O Line' -> ''

### `B.Sic.Dra.Cls.Ams.Be6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be6 Line' -> ''

### `E.Ben.Mod.Cls.Nd2.Re8` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Re8 Line' -> ''

### `E.Ben.Mod.Cls.Bg5.h6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'h6 Line' -> ''

### `E.Ben.Mod.Cls.Rb1.a6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'a6 Line' -> ''

### `E.Ben.Mod.Cls.h3.Na6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Na6 Line' -> ''

### `E.Ben.Mod.Fch.Nd2.Re8` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Re8 Line' -> ''

### `E.Ben.Mod.Fch.Bf4.Re8` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Re8 Line' -> ''

### `E.KID.Sml.Ort.Exc.dxe5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'dxe5 Line' -> ''

### `E.KID.Fch.Yug.Exc.Nc6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc6 Line' -> ''

### `A.Hol.Cls.IZh.Win.Ne4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Ne4 Line' -> ''

### `A.Hol.Cls.IZh.Ala.Ne4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Ne4 Line' -> ''

### `B.Fre.Tar.Cls.Be7.Ngf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Ngf3 Line' -> ''

### `B.Fre.Tar.Cls.c5.c3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c3 Line' -> ''

### `B.Fre.Tar.Cls.Kor.O-O` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'O-O Line' -> ''

### `B.Sic.Clo.Fch.Bot.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf6 Line' -> ''

### `B.Sic.Clo.Fch.Eng.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf6 Line' -> ''

### `C.KGm.Acc.Kie.Lon.Nxg4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nxg4 Line' -> ''

### `C.KGm.Acc.Bsh.Ble.Nf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf3 Line' -> ''

### `E.Nim.Rub.Hub.Rau.O-O` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'O-O Line' -> ''

### `E.KID.Avk.Fle.MLn.Nf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf3 Line' -> ''

### `C.KGm.Dec.Fal.MLn.d3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "d3 Line|King's Gambit Declined: Falkbeer Countergambit, Charousek Gambit" -> "King's Gambit Declined: Falkbeer Countergambit, Charousek Gambit"

### `C.KGm.Acc.All.MLn.Nxf7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Nxf7 Line|King's Gambit Accepted: Kieseritzky Gambit, Cotter Gambit" -> "King's Gambit Accepted: Kieseritzky Gambit, Cotter Gambit"

### `B.Sic.Sve.Nd5.Be7.Bxf6.g3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'g3 Line' -> ''

### `B.Sic.Sve.Bxf6.Nd5.Bg7.c3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c3 Line' -> ''

### `B.Sic.Sve.Bxf6.Nd5.f5.c3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c3 Line' -> ''

### `A.Eng.Rev.Bot.MLn.Nd5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nd5 Line' -> ''

### `B.Sic.Sch.Eng.MLn.Qd2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qd2 Line' -> ''

### `B.Sic.Kan.Tal.MLn.O-O` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'O-O Line' -> ''

### `B.Sic.Ros.Nim.MLn.d4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd4 Line' -> ''

### `B.CaK.Adv.Sht.MLn.c3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c3 Line' -> ''

### `C.RyL.Ber.Wal.End.MLn.Re1` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Re1 Line' -> ''

### `D.Sla.Che.MLn.a4.axb5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'axb5 Line' -> ''

### `D.QGD.Ort.Hne.Cap.O-O` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'O-O Line' -> ''

### `D.QGD.Tar.MLn.Bd3.O-O` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'O-O Line' -> ''

### `D.Sla.Cls.MLn.e4.Qe2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qe2 Line' -> ''

### `D.Sla.Qui.MLn.Bd3.O-O` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'O-O Line' -> ''

### `D.Sem.Bg5.Bot.Ekf.MLn.hxg5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'hxg5 Line' -> ''

### `D.Sem.Mer.Lun.MLn.O-O` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'O-O Line' -> ''

### `D.QGA.Cen.Mod.MLn.Be3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be3 Line' -> ''

### `D.Cat.Cls.Kor.MLn.Bf4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bf4 Line' -> ''

### `E.Bog.Nim.MLn.Be2.O-O` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'O-O Line' -> ''

### `E.OldI.Cls.MLn.Re1.Be3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be3 Line' -> ''

### `E.Blf.Dec.MLn.e3.Be2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be2 Line' -> ''

### `E.QID.Pet.Kas.MLn.e4.O-O` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'O-O Line' -> ''

### `E.KID.Mak.MLn.Be2.Re8` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Re8 Line' -> ''

### `E.Gru.Brn.MLn.Be2.Nc6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc6 Line' -> ''

### `E.Nim.Rom.MLn.Nf3.dxc4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'dxc4 Line' -> ''

### `E.Ind.Tgo.MLn.Nc3.exd4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'exd4 Line' -> ''

### `D.Chi.MLn.e3.Nf6.Nc3.e6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e6 Line' -> ''

### `D.Tar.Cls.MLn.Re8.Re1.Bf8` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bf8 Line' -> ''

### `D.Tar.Prg.MLn.Nxd4.Qb6.Be3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be3 Line' -> ''

### `D.STa.Exc.MLn.Nxc3.Qb3.cxd4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'cxd4 Line' -> ''

### `D.STa.Pil.MLn.Nxd4.a6.e3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e3 Line' -> ''

### `D.QGA.Old.MLn.exd4.Be7.Nf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf3 Line' -> ''

### `D.QGA.Ale.MLn.Bb3.e6.Nf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf3 Line' -> ''

### `D.Chi.MLn.e3.Nf6.Be2.e6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e6 Line' -> ''

### `D.Tar.Cls.MLn.Re8.Be3.Bf8` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bf8 Line' -> ''

### `D.Tar.Prg.MLn.Nxd4.Be6.O-O` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'O-O Line' -> ''

### `D.STa.Exc.MLn.Nxc3.bxc3.Nc6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc6 Line' -> ''

### `D.STa.Pil.MLn.Nxd4.Be7.e3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e3 Line' -> ''

### `D.QGA.Old.MLn.exd4.Nf6.Nf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf3 Line' -> ''

### `D.QGA.Ale.MLn.Bb3.Nc6.Nf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf3 Line' -> ''

### `B.Sic.Sve.Nd5.Qa5.Bd2.Rb8` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Rb8 Line' -> ''

### `C.Ita.Two.Ng5.Trx.Bxf7.Ke7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Ke7 Line' -> ''

### `C.Ita.Two.Ng5.Feg.Kxf7.Qf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qf3 Line' -> ''

### `C.Ita.Two.Ng5.Ulv.Bxb5.Qxd5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qxd5 Line' -> ''

### `C.Ita.Two.Ng5.Pol.Bb5.c6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c6 Line' -> ''

### `D.Cat.Ope.Qa4.Ale.Be7.Bg2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bg2 Line' -> ''

### `C.RyL.Mor.Opn.Hwl.Nc5.Rd1` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Rd1 Line' -> ''

### `C.RyL.Mor.StD.Sie.exf5.Bxf5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bxf5 Line' -> ''

### `C.Ita.Two.Ng5.Frt.c3.b5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'b5 Line' -> ''

### `C.Ita.Two.Ng5.Lol.exd4.O-O` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'O-O Line' -> ''

### `B.Sic.Naj.Sch.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `B.Sic.Naj.Adm.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `B.Sic.Naj.Pst.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `B.Sic.Sch.Krs.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.Sem.Bg5.Mos.Qxf6.g3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'g3 Line' -> ''

### `D.Sem.Bg5.AMo.dxc4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'dxc4 Line' -> ''

### `B.Sic.Clo.GPr.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `C.RyL.Mor.Nor.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line|Ruy López: Morphy Defense, Norwegian Variation, Nightingale Gambit' -> 'Ruy López: Morphy Defense, Norwegian Variation, Nightingale Gambit'

### `C.RyL.Mor.Wor.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `C.Ita.Giu.Mol.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Main Line|Italian Game: Giuoco Piano, Greco's Attack" -> "Italian Game: Giuoco Piano, Greco's Attack"

### `C.Ita.Two.Opn.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line|Scotch Game: Scotch Gambit, Dubois Réti Defense' -> 'Scotch Game: Scotch Gambit, Dubois Réti Defense'

### `C.Ita.Two.Max.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.KID.Sml.Pan.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.KID.Cls.Glg.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.KID.Cls.Exc.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.Gru.Exc.Sev.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `A.Hol.Sto.Bot.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.Sem.AMe.Shr.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.Cat.Cls.Bot.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.Cat.Cls.Rab.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.QID.Mod.Trd.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Main Line|Queen's Indian Defense: Classical Variation" -> "Queen's Indian Defense: Classical Variation"

### `E.Nim.Cls.Ker.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.Gru.Exc.Sps.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.KID.Fch.Uhl.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.KID.Sml.Byr.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.KID.Fou.Dyn.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Main Line|King's Indian Defense: Four Pawns Attack, Normal Attack" -> "King's Indian Defense: Four Pawns Attack, Normal Attack"

### `E.KID.Avk.Ben.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Main Line|King's Indian Defense: Averbakh Variation, Benoni Defense, Advance Variation" -> "King's Indian Defense: Averbakh Variation, Benoni Defense, Advance Variation"

### `B.Sic.Dra.Lev.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `B.Sic.Tay.Eng.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `B.Sic.Kan.Mar.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `B.Fre.Adv.Mil.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `B.Fre.Tar.Ope.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `B.CaK.Adv.Tal.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `C.RyL.Ber.Rio.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line|Ruy López: Berlin Defense, Minckwitz Variation' -> 'Ruy López: Berlin Defense, Minckwitz Variation'

### `C.RyL.Mor.ClD.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `C.RyL.Mor.Fch.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `C.RyL.Mor.Car.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `C.Ita.Giu.Grc.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line|Italian Game: Classical Variation, Greco Gambit, Modern Line' -> 'Italian Game: Classical Variation, Greco Gambit, Modern Line'

### `C.Sco.Gor.Dbl.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `C.Vie.Gbt.Hmp.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `C.Fou.Spa.Dbl.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `C.Fou.Spa.Cls.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.Ben.Bnk.Acc.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line|Benko Gambit Accepted: Fully Accepted Variation' -> 'Benko Gambit Accepted: Fully Accepted Variation'

### `E.Ben.Bnk.Dec.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.Gru.Brn.Nad.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.QGD.Exc.Car.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.QGD.Exc.Min.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.KID.Cls.Bol.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.KID.Cls.Ort.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.Bud.Faj.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.Bud.Faj.MLn.e3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e3 Line' -> ''

### `E.Bud.Faj.MLn.e3.Be2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be2 Line' -> ''

### `E.Bud.Faj.MLn.e3.Be2.O-O` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'O-O Line' -> ''

### `E.Bud.Faj.Bns.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.Bud.Faj.Ste.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.Bud.Rub.MLn.e3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e3 Line' -> ''

### `E.Bud.Rub.MLn.e3.Be2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be2 Line' -> ''

### `E.Bud.Alk.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.Bud.Alk.MLn.Nf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf3 Line' -> ''

### `E.Gru.Thr.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.Gru.Thr.MLn.Qb3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qb3 Line' -> ''

### `E.Gru.Neo.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.Gru.Neo.MLn.cxd5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'cxd5 Line' -> ''

### `E.Gru.Neo.MLn.cxd5.Nxd5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nxd5 Line' -> ''

### `E.Gru.Rus.Prz.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line|Grünfeld Defense: Russian Variation, Byrne Variation' -> 'Grünfeld Defense: Russian Variation, Byrne Variation'

### `E.Gru.Rus.Szs.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.Gru.Fch.Pac.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.Gru.Fch.Euw.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.Gru.Exc.Mod.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.Nim.Spl.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.Nim.Spl.MLn.e3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e3 Line' -> ''

### `E.Nim.Cls.Noa.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.Nim.Cls.Bot.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.Nim.Cls.Mil.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.Nim.Rub.Res.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line|Nimzo-Indian Defense: Normal Variation, Gligoric System' -> 'Nimzo-Indian Defense: Normal Variation, Gligoric System'

### `E.Nim.Rub.Flo.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.Nim.Rub.StP.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.Nim.Sml.Kmo.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line|Nimzo-Indian Defense: Sämisch Variation' -> 'Nimzo-Indian Defense: Sämisch Variation'

### `E.Nim.Kas.Euw.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.QID.Sps.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.QID.Euw.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.QID.Kas.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.QID.Cls.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.KID.Cls.Arb.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.KID.Sml.Bob.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.KID.Sml.Krs.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.KID.Fch.Sim.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Main Line|King's Indian Defense: Fianchetto Variation, Panno Variation" -> "King's Indian Defense: Fianchetto Variation, Panno Variation"

### `E.KID.Fch.Kav.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.Sla.Sml.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.Sla.Ala.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.Sla.Cze.Kra.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.Sla.Not.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.Sla.Stn.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.QGA.Bog.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.QGA.Flo.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Main Line|Queen's Gambit Accepted: Alekhine Defense, Haberditz Variation" -> "Queen's Gambit Accepted: Alekhine Defense, Haberditz Variation"

### `D.QGA.Jan.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.QGD.Har.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.QGD.Alt.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.QGD.Cls.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.QGD.Cls.MLn.Bh4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bh4 Line' -> ''

### `D.QGD.Cls.Bd3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bd3 Line' -> ''

### `D.QGD.Cls.Nf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf3 Line' -> ''

### `D.QGD.Cls.Nf3.c5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c5 Line' -> ''

### `D.QGA.Cls.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Main Line|Queen's Gambit Accepted: Classical Defense, Main Line" -> "Queen's Gambit Accepted: Classical Defense, Main Line"

### `D.QGA.Cls.MLn.a4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'a4 Line' -> ''

### `D.QGA.Cls.Ale.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Main Line|Queen's Gambit Accepted: Classical Defense, Alekhine System" -> "Queen's Gambit Accepted: Classical Defense, Alekhine System"

### `D.Sla.Cls.MLn.Nh4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nh4 Line' -> ''

### `D.Sla.Cls.MLn.Qe2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qe2 Line' -> ''

### `D.Sla.Dim.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.Sla.Win.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.Tar.Rub.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line|Tarrasch Defense: Prague Variation, Main Line' -> 'Tarrasch Defense: Prague Variation, Main Line'

### `D.Tar.Rub.MLn.O-O` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'O-O Line' -> ''

### `D.Tar.HSc.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.Tar.Mar.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.STa.Kmo.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.STa.Sym.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.STa.End.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.Chi.Laz.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.Chi.Tar.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.QPG.Ver.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.QPG.Ama.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.QPG.Mas.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.QPG.Sto.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.QPG.Zur.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.Ben.Czk.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.Ben.Czk.MLn.Be7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be7 Line' -> ''

### `E.Gru.Sml.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.Gru.Sml.MLn.c5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c5 Line' -> ''

### `E.OldI.Ukr.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.OldI.Jan.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.Nim.Fou.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.Nim.Fou.MLn.e4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e4 Line' -> ''

### `E.Nim.Mik.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.Nim.Mik.MLn.Nf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf3 Line' -> ''

### `E.Bog.Exc.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.Bog.Hai.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.Bog.Rom.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.Bog.NEn.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.Bog.Grn.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.KID.Fch.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.KID.Fch.MLn.O-O` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'O-O Line' -> ''

### `E.KID.Fou.Bg5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bg5 Line' -> ''

### `E.KID.Fou.Be2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be2 Line' -> ''

### `E.KID.Cls.Old.e5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e5 Line' -> ''

### `E.Nim.Rub.Cls.cxd5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'cxd5 Line' -> ''

### `B.Fre.Cls.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line|French Defense: Classical Variation, Normal Variation' -> 'French Defense: Classical Variation, Normal Variation'

### `B.Fre.Stn.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `B.Fre.Mac.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `A.KIA.Fre.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `B.Sic.Ros.a6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'a6 Line' -> ''

### `A.Tro.Bxf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bxf6 Line' -> ''

### `B.CaK.Cls.Spd.Nd7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nd7 Line' -> ''

### `B.Fre.Rub.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line|French Defense: Rubinstein Variation, Blackburne Defense' -> 'French Defense: Rubinstein Variation, Blackburne Defense'

### `B.Fre.Mac.exd5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'exd5 Line' -> ''

### `B.Sic.Mor.Bd7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bd7 Line' -> ''

### `B.CaK.Exc.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `B.CaK.Fan.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `B.Pir.Cls.Bg7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bg7 Line' -> ''

### `B.Sic.Kal.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `B.Sic.Loe.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `B.Sic.Nim.e5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e5 Line|Sicilian Defense: Nimzowitsch Variation, Advance Variation' -> 'Sicilian Defense: Nimzowitsch Variation, Advance Variation'

### `B.Sca.Por.Bnk.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `B.Sca.Nf6.Chk.Bd7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bd7 Line' -> ''

### `B.Sca.Nf6.Chk.Nbd` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nbd7 Line' -> ''

### `B.CaK.Two.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf6 Line' -> ''

### `B.CaK.Two.Bf5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bf5 Line' -> ''

### `B.CaK.Tar.Be3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be3 Line' -> ''

### `A.Tro.Cls.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line|Trompowsky Attack: Classical Defense, Big Center Variation' -> 'Trompowsky Attack: Classical Defense, Big Center Variation'

### `A.Tro.Cls.MLn.e3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e3 Line' -> ''

### `A.Tro.Rap.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `A.Tro.Rap.MLn.e6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e6 Line' -> ''

### `A.Tro.Rap.MLn.f6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'f6 Line' -> ''

### `A.Tro.Bxf6.e3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e3 Line' -> ''

### `A.Tor.ClD.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line|Torre Classical Defense, Main Line' -> 'Torre Classical Defense, Main Line'

### `A.Tor.ClD.MLn.c3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c3 Line' -> ''

### `A.Tor.Nim.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `A.Tor.Yus.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `B.Ale.Fou.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `B.Ale.Fou.MLn.Nf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf3 Line' -> ''

### `B.Ale.Fou.MLn.Be3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be3 Line' -> ''

### `B.Ale.Fou.Trd.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `B.Ale.Mod.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `B.Ale.Chs.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `B.Pir.Cls.Bg7.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line|Pirc Defense: Classical Variation, Quiet System' -> 'Pirc Defense: Classical Variation, Quiet System'

### `B.Pir.Cls.Bg7.MLn.O-O` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'O-O Line' -> ''

### `B.Pir.Aus.Drg.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line|Pirc Defense: Austrian Attack, Weiss Variation' -> 'Pirc Defense: Austrian Attack, Weiss Variation'

### `B.Pir.Aus.Unz.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `B.Pir.150.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `B.Pir.150.MLn.O-O-O` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'O-O-O Line' -> ''

### `B.Pir.Byr.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `C.PhD.Han.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `C.PhD.Han.MLn.O-O` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'O-O Line' -> ''

### `C.PhD.Exc.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `C.PhD.Lio.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `C.Pon.CGm.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `C.Pon.CGm.MLn.exf5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'exf5 Line' -> ''

### `C.Pon.Jae.MLn.e5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e5 Line' -> ''

### `C.Pon.Ste.MLn.f6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'f6 Line' -> ''

### `C.Vie.Cls.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Main Line|Bishop's Opening: Vienna Hybrid, Spielmann Attack" -> "Bishop's Opening: Vienna Hybrid, Spielmann Attack"

### `C.Vie.Cls.MLn.Nf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf3 Line' -> ''

### `C.Vie.Mie.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `C.Vie.Fal.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line|Vienna Game: Frankenstein-Dracula Variation' -> 'Vienna Game: Frankenstein-Dracula Variation'

### `C.Vie.Gbt.Pie.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `B.Sic.Alp.Nf6.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `B.Sic.Alp.Cen.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `B.Sic.Alp.Dd6.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `B.Sic.Ros.Cls.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `B.Sic.Ros.Cls.MLn.c3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c3 Line' -> ''

### `B.Sic.Ros.a6.Bxc6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bxc6 Line' -> ''

### `B.Sic.Mor.Bd7.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `B.Sic.Mor.Nd7.O-O` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'O-O Line' -> ''

### `B.Fre.Rub.MLn.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf6 Line' -> ''

### `B.Fre.Rub.MLn.Bd3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bd3 Line' -> ''

### `B.Fre.Mac.MLn.Bd3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bd3 Line' -> ''

### `B.Fre.Mac.MLn.Bh4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bh4 Line|French Defense: McCutcheon Variation, Bernstein Variation' -> 'French Defense: McCutcheon Variation, Bernstein Variation'

### `B.CaK.Two.Nf6.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `B.CaK.Two.Bf5.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.Bgm.Acc.Bog.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.Bgm.Acc.Euw.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.Bgm.Acc.Tei.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.Bgm.Acc.Gun.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.Bgm.Acc.Zie.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.Bgm.Dec.Elb.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.Chi.Jan.Mod.e3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e3 Line' -> ''

### `D.Chi.Laz.MLn.Ne5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Ne5 Line' -> ''

### `D.Chi.Tar.MLn.Nb5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nb5 Line' -> ''

### `D.Sla.Sml.MLn.Bg4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bg4 Line' -> ''

### `D.Sla.Ala.MLn.a4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'a4 Line' -> ''

### `D.Sla.Not.MLn.a4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'a4 Line' -> ''

### `D.Sla.Stn.MLn.e4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e4 Line' -> ''

### `D.QGA.Bog.MLn.O-O` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'O-O Line' -> ''

### `D.QGA.Flo.MLn.a4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'a4 Line' -> ''

### `D.QGA.Jan.MLn.O-O` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'O-O Line' -> ''

### `D.QGA.Man.MLn.e4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e4 Line' -> ''

### `D.Tar.HSc.MLn.Qd1` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qd1 Line' -> ''

### `D.Tar.Mar.MLn.Bd6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bd6 Line' -> ''

### `D.STa.Kmo.MLn.Be7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be7 Line' -> ''

### `D.STa.Sym.MLn.b6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'b6 Line' -> ''

### `D.STa.End.MLn.Bc4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bc4 Line' -> ''

### `D.QPG.Ver.MLn.Be7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be7 Line' -> ''

### `D.QPG.Ama.MLn.c6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c6 Line' -> ''

### `D.QPG.Mas.MLn.e6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e6 Line' -> ''

### `D.QPG.Sto.MLn.c5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c5 Line' -> ''

### `D.QPG.Zur.MLn.h3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'h3 Line' -> ''

### `E.OldI.Ukr.MLn.Be7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be7 Line' -> ''

### `E.OldI.Jan.MLn.e3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e3 Line' -> ''

### `E.Bog.Exc.MLn.Nc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc3 Line' -> ''

### `E.Bog.Hai.MLn.O-O` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'O-O Line' -> ''

### `E.Bog.Rom.MLn.O-O` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'O-O Line' -> ''

### `E.Bog.NEn.MLn.g3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'g3 Line' -> ''

### `E.Bog.Grn.MLn.e3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e3 Line' -> ''

### `E.QID.Sps.MLn.O-O` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'O-O Line' -> ''

### `E.QID.Euw.MLn.Bxd2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bxd2 Line' -> ''

### `E.QID.Kas.MLn.Bd2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bd2 Line' -> ''

### `E.QID.Pet.KPe.Be7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Be7 Line|Queen's Indian Defense: Kasparov-Petrosian Variation, Marco Defense" -> "Queen's Indian Defense: Kasparov-Petrosian Variation, Marco Defense"

### `E.QID.Cls.MLn.exd5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'exd5 Line' -> ''

### `E.Gru.Hng.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.Gru.Sml.MLn.c5.dxc5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'dxc5 Line' -> ''

### `E.Gru.Thr.MLn.Qb3.Nxc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nxc3 Line' -> ''

### `E.Gru.Neo.MLn.cxd5.Nxd5.e4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e4 Line' -> ''

### `E.Gru.Exc.Mod.MLn.Be2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be2 Line' -> ''

### `E.KID.Fou.Bg5.Be2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be2 Line' -> ''

### `E.KID.Fou.Be2.O-O` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'O-O Line' -> ''

### `E.KID.Cls.Old.e5.d5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "d5 Line|King's Indian Defense: Orthodox Variation, Positional Defense, Closed Line" -> "King's Indian Defense: Orthodox Variation, Positional Defense, Closed Line"

### `E.KID.Cls.Arb.MLn.Nxd4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nxd4 Line' -> ''

### `E.KID.Sml.Bob.MLn.b5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'b5 Line' -> ''

### `E.KID.Sml.Krs.MLn.c5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c5 Line' -> ''

### `E.Ben.Czk.MLn.Be7.Nf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf3 Line' -> ''

### `E.Ben.Bnk.Acc.MLn.Bxa6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bxa6 Line' -> ''

### `E.Ben.Bnk.Dec.MLn.Bxe7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bxe7 Line' -> ''

### `A.Eng.Org.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `A.Eng.Org.MLn.Bb2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bb2 Line' -> ''

### `A.Eng.Org.MLn.Bb2.Bxb4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bxb4 Line' -> ''

### `A.Eng.Mik.MLn.Ne4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Ne4 Line' -> ''

### `A.Eng.Mik.MLn.Ne4.Nfd7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nfd7 Line' -> ''

### `A.Eng.Rev.Bot.MLn.Qd7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qd7 Line' -> ''

### `A.Eng.Rev.Bot.MLn.Qd7.f4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'f4 Line' -> ''

### `A.Eng.Sym.Hdg.MLn.Bxg2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bxg2 Line' -> ''

### `A.Eng.Sym.Hdg.MLn.Bxg2.Kxg2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Kxg2 Line' -> ''

### `A.Eng.Sym.Rub.MLn.O-O` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'O-O Line' -> ''

### `A.Eng.Sym.Rub.MLn.O-O.Be2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be2 Line' -> ''

### `A.Eng.Rev.Fou.MLn.e3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e3 Line' -> ''

### `A.Eng.Rev.Fou.MLn.e3.Be7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be7 Line' -> ''

### `A.Ret.Acc.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `A.Ret.Acc.MLn.Be6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be6 Line|Réti Opening: Réti Gambit, Keres Variation' -> 'Réti Opening: Réti Gambit, Keres Variation'

### `A.Ret.Acc.MLn.Be6.Bxc4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bxc4 Line' -> ''

### `A.Ret.Adv.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `A.Ret.Adv.MLn.Nc6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc6 Line' -> ''

### `A.Ret.Adv.MLn.Nc6.Bg2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bg2 Line' -> ''

### `A.Ret.Ang.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `A.Ret.Ang.MLn.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf6 Line' -> ''

### `A.Ret.QGI.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `A.Ret.QGI.MLn.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf6 Line' -> ''

### `A.Ret.Fch.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `A.Ret.Fch.MLn.Bg2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bg2 Line' -> ''

### `A.KIA.Sic.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `A.KIA.Sic.MLn.g3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'g3 Line' -> ''

### `A.KIA.Sic.MLn.g3.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf6 Line' -> ''

### `A.KIA.Car.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `A.KIA.Car.MLn.Ngf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Ngf3 Line' -> ''

### `A.Hol.Fch.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `A.Hol.Fch.MLn.c4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c4 Line' -> ''

### `A.Hol.Sta.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `A.Hol.Sta.MLn.d5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd5 Line' -> ''

### `A.Hol.Hop.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `A.Hol.Kre.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `A.Hol.Alp.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `A.Hol.Lng.MLn.b3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'b3 Line' -> ''

### `A.Hol.Lng.MLn.b3.Nc6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc6 Line' -> ''

### `A.Hol.Sto.Bot.MLn.c5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c5 Line' -> ''

### `A.Lon.Msn.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `A.Lon.Msn.MLn.Nbd2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nbd2 Line' -> ''

### `A.Lon.Job.Nc6.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `A.Lon.Job.Nc6.MLn.Nb5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nb5 Line' -> ''

### `A.Lon.Psn.Qxb2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qxb2 Line' -> ''

### `A.Lon.Psn.Qxb2.Nb5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nb5 Line' -> ''

### `A.Col.Zuk.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `A.Col.Zuk.MLn.Be7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be7 Line' -> ''

### `A.Col.Phn.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `A.Tor.Yus.MLn.c3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c3 Line' -> ''

### `A.Tor.Yus.MLn.c3.Bb7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bb7 Line' -> ''

### `A.Ver.Cls.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Main Line|Queen's Pawn Veresov MLn move-order" -> "Queen's Pawn Veresov MLn move-order"

### `A.Ver.Cls.MLn.Be7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be7 Line' -> ''

### `A.Lar.Cls.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `A.Lar.Cls.MLn.Be2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be2 Line' -> ''

### `A.Pol.Bhm.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `A.Pol.Bhm.MLn.Bb2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bb2 Line' -> ''

### `A.Gro.Gbt.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line|Grob Opening: Grob Gambit, Fritz Gambit' -> 'Grob Opening: Grob Gambit, Fritz Gambit'

### `A.Gro.Gbt.MLn.d4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd4 Line|Grob Opening: Romford Countergambit' -> 'Grob Opening: Romford Countergambit'

### `A.Mod.Avk.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `A.Mod.Avk.MLn.Be2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be2 Line' -> ''

### `A.PQI.Bf4.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `A.PQI.Fch.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `A.EID.Fch.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `A.EID.Col.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `C.KGm.Acc.Nf3.Mod.exd5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'exd5 Line' -> ''

### `E.Ind.Qb3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qb3 Line|Indian Defense, Qb3' -> 'Indian Defense, Qb3'

### `B.Fre.Nrm.d5.Nc3.a6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'a6 Line' -> ''

### `B.CaK.Dpn.Mdn.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line|Caro-Kann Defense: Main Line' -> 'Caro-Kann Defense: Main Line'

### `B.Fre.Win.Fsl.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line|French Defense: Winawer Variation, Fingerslip Variation, Main Line' -> 'French Defense: Winawer Variation, Fingerslip Variation, Main Line'

### `B.Fre.Win.Adv.MWl.Nf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf3 Line|French Defense: Winawer Variation, Advance Variation' -> 'French Defense: Winawer Variation, Advance Variation'

### `B.Fre.Win.Adv.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `B.Fre.Win.Adv.MLn.Ne7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Ne7 Line' -> ''

### `B.Fre.Win.Adv.MLn.Ne7.Bd3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bd3 Line|French Defense: Winawer Variation, Advance Variation, with Bd3' -> 'French Defense: Winawer Variation, Advance Variation, with Bd3'

### `B.Fre.Win.Adv.MLn.Ne7.h4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'h4 Line|French Defense: Winawer Variation, Advance Variation, with h4' -> 'French Defense: Winawer Variation, Advance Variation, with h4'

### `B.Fre.Win.Adv.MLn.Ne7.Nf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf3 Line' -> ''

### `B.Fre.Win.Adv.Pos.Qa5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qa5 Line' -> ''

### `B.Fre.Win.Adv.Pos.Qa5.Bd2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bd2 Line' -> ''

### `B.Fre.Win.Adv.Pos.Qa5.Qd2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qd2 Line' -> ''

### `B.Ale.Nrm.Bc4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bc4 Line|Alekhine Defense, Bc4 Line' -> 'Alekhine Defense, Bc4 Line'

### `B.Sca.b3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'b3 Line|Scandinavian Defense, b3 Line' -> 'Scandinavian Defense, b3 Line'

### `B.Sic.Naj.Be2.e5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e5 Line' -> ''

### `B.Sic.Naj.Be2.e5.Nb3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nb3 Line' -> ''

### `B.Sic.Naj.Be2.e5.Nb3.Be6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be6 Line' -> ''

### `B.Sic.Naj.Bg5.e6.f4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'f4 Line' -> ''

### `B.Sic.Tay.Nb5.d6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd6 Line' -> ''

### `B.Sic.Tay.Nb5.d6.c4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c4 Line' -> ''

### `B.Sic.Tay.Nc3.Nf6.Ndb5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Ndb5 Line' -> ''

### `B.Sic.Tay.Nc3.a6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'a6 Line' -> ''

### `B.Sic.SmM.Acc.Nxc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nxc3 Line' -> ''

### `B.Sic.SmM.Acc.Nxc3.Nc6.Nf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf3 Line' -> ''

### `B.Sic.SmM.Acc.Nxc3.e6.Nf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf3 Line' -> ''

### `B.Sic.Fre.c3.d5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd5 Line|Sicilian Defense: Delayed Alapin Variation' -> 'Sicilian Defense: Delayed Alapin Variation'

### `B.Sic.Fre.d4.cxd4.Nxd4.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf6 Line' -> ''

### `B.Sic.Old.Nc3.Bc4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bc4 Line' -> ''

### `B.Sic.Old.Nc3.Bc4.d6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd6 Line|Sicilian Defense: Closed, Anti-Sveshnikov Variation, with d6' -> 'Sicilian Defense: Closed, Anti-Sveshnikov Variation, with d6'

### `B.Sic.Old.Nc3.Bc4.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf6 Line|Sicilian Defense: Closed, Anti-Sveshnikov Variation, with Nf6' -> 'Sicilian Defense: Closed, Anti-Sveshnikov Variation, with Nf6'

### `B.Sic.Clo.e6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e6 Line' -> ''

### `B.Sic.Clo.e6.g3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'g3 Line' -> ''

### `B.Sic.Clo.D6L` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd6 Line' -> ''

### `B.Sic.Cls.Rch.Bd7.Qd2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qd2 Line|Sicilian Defense: Richter-Rauzer Variation, Modern Variation' -> 'Sicilian Defense: Richter-Rauzer Variation, Modern Variation'

### `B.Sic.Cls.Rch.e6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e6 Line|Sicilian Defense: Richter-Rauzer Variation' -> 'Sicilian Defense: Richter-Rauzer Variation'

### `C.RyL.Fia.c3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c3 Line' -> ''

### `C.RyL.Stn.d4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd4 Line' -> ''

### `C.RyL.Stn.d4.Bd7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bd7 Line' -> ''

### `C.Vie.Nc6.f4.exf4.Nf3.g5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'g5 Line' -> ''

### `C.Vie.Nc6.f4.exf4.d4.Qh4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line|Vienna Gambit, with Max Lange Defense: Steinitz Gambit, Main Line' -> 'Vienna Gambit, with Max Lange Defense: Steinitz Gambit, Main Line'

### `C.PhD.Bc4.Be7.c3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c3 Line' -> ''

### `C.PhD.d4.exd4.Nxd4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nxd4 Line' -> ''

### `C.PhD.d4.Nd7.Bc4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bc4 Line' -> ''

### `C.PhD.d4.Nd7.Bc4.c6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c6 Line' -> ''

### `C.PhD.d4.Nf6.dxe5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'dxe5 Line' -> ''

### `C.PhD.d4.Nf6.dxe5.Nxe4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nxe4 Line' -> ''

### `C.KPO.f3.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Nf6 Line|King's Pawn Game: King's Head Opening" -> "King's Pawn Game: King's Head Opening"

### `C.KPO.b3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'b3 Line' -> ''

### `C.Bsh.b5.Bxb5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bxb5 Line' -> ''

### `C.Bsh.b5.Bxb5.c6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c6 Line' -> ''

### `C.Bsh.Nc6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc6 Line' -> ''

### `C.Sco.exd4.Nxd4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nxd4 Line' -> ''

### `C.Sco.Nxd4.Nxd4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nxd4 Line' -> ''

### `C.Sco.Nxd4.Nxd4.Qxd4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qxd4 Line' -> ''

### `C.KGm.Qh4.g3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "g3 Line|King's Gambit Declined: Keene's Defense" -> "King's Gambit Declined: Keene's Defense"

### `C.KGm.Qf6.Nc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc3 Line' -> ''

### `C.KGm.Qf6.Nc3.Qxf4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qxf4 Line' -> ''

### `C.KGm.Nc6.Nf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf3 Line' -> ''

### `C.KGm.f5.exf5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'exf5 Line' -> ''

### `C.LtO.Bc4.fxe4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'fxe4 Line' -> ''

### `C.LtO.Nxe5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nxe5 Line' -> ''

### `D.Sla.Nc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc3 Line|Slav Defense, Nc3' -> 'Slav Defense, Nc3'

### `D.Sla.Nc3.dxc4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'dxc4 Line|Slav Defense, Nc3 dxc4' -> 'Slav Defense, Nc3 dxc4'

### `D.Sla.Nc3.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf6 Line|Slav Defense, Nc3 Nf6' -> 'Slav Defense, Nc3 Nf6'

### `D.Sla.Nc3.Nf6.e3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e3 Line|Slav Defense, Nc3 Nf6 e3' -> 'Slav Defense, Nc3 Nf6 e3'

### `D.Sla.Nf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf3 Line|Slav Defense, Nf3|Slav Defense: Modern Line' -> 'Slav Defense, Nf3|Slav Defense: Modern Line'

### `D.Sla.Nf3.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf6 Line|Slav Defense, Nf3 Nf6' -> 'Slav Defense, Nf3 Nf6'

### `D.Bgm.Cap.Nc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc3 Line' -> ''

### `D.Bgm.Cap.Nc3.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf6 Line' -> ''

### `D.QGA.e3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "e3 Line|Queen's Gambit Accepted: Old Variation" -> "Queen's Gambit Accepted: Old Variation"

### `D.QGA.Qa4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Qa4+ Line|Queen's Gambit Accepted: Accelerated Mannheim Variation" -> "Queen's Gambit Accepted: Accelerated Mannheim Variation"

### `D.QGA.Nf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Nf3 Line|Queen's Gambit Accepted: Normal Variation" -> "Queen's Gambit Accepted: Normal Variation"

### `D.QGA.Nf3.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf6 Line' -> ''

### `D.QPG.e3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e3 Line' -> ''

### `D.QPG.e3.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf6 Line' -> ''

### `D.QPG.Zuk.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Nf6 Line|Queen's Pawn Game: Symmetrical Variation" -> "Queen's Pawn Game: Symmetrical Variation"

### `D.QPG.Zuk.Nf6.e3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "e3 Line|Queen's Pawn Game: Colle System" -> "Queen's Pawn Game: Colle System"

### `D.QPG.Zuk.Nf6.c4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c4 Line' -> ''

### `D.QPG.Zuk.c6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c6 Line' -> ''

### `D.QPG.Zuk.e6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e6 Line' -> ''

### `D.QPG.Zuk.Bf5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bf5 Line' -> ''

### `D.Tar.Exd.Nf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf3 Line|Tarrasch Defense: Two Knights Variation' -> 'Tarrasch Defense: Two Knights Variation'

### `D.Tar.Exd.Nf3.Nc6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc6 Line' -> ''

### `D.Tar.Cls.Bg5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bg5 Line|Tarrasch Defense: Classical Variation, Carlsbad Variation' -> 'Tarrasch Defense: Classical Variation, Carlsbad Variation'

### `D.Tar.Cls.Bg5.cxd4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'cxd4 Line' -> ''

### `D.Tar.Cls.Bg5.cxd4.Nxd4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nxd4 Line' -> ''

### `D.Tar.Cls.Bg5.cxd4.Nxd4.h6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'h6 Line' -> ''

### `D.QGD.Cls.Nf3.Nbd7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nbd7 Line' -> ''

### `D.QGD.Cls.Nf3.Nbd7.Bd3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bd3 Line' -> ''

### `D.QGD.Cls.Nf3.Nbd7.Qc2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qc2 Line' -> ''

### `D.QGD.Cls.Nf3.Nbd7.Rc1` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Rc1 Line' -> ''

### `D.QGD.Ort.Hne.Bxe7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bxe7 Line' -> ''

### `D.QGD.Ort.Hne.Bxe7.Qxe7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qxe7 Line' -> ''

### `D.QGD.Ort.Hne.Bxe7.Qxe7.O-O` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'O-O Line' -> ''

### `D.QGD.Ort.Hne.Bxe7.Qxe7.Ne4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Ne4 Line' -> ''

### `D.Sem.AMe.b6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'b6 Line' -> ''

### `D.Sem.AMe.b6.b3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'b3 Line' -> ''

### `D.Sem.AMe.b6.b3.Bb7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bb7 Line' -> ''

### `D.Sem.AMe.Bd6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bd6 Line' -> ''

### `D.Sem.AMe.Bd6.b3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'b3 Line' -> ''

### `D.Sem.AMe.Bd6.b3.O-O` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'O-O Line' -> ''

### `D.Sem.Mer.MLn.c5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c5 Line' -> ''

### `D.Sem.Mer.MLn.c5.e5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e5 Line' -> ''

### `D.Sem.Mer.MLn.c5.d5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "d5 Line|Semi-Slav Defense: Meran Variation, Reynolds' Variation" -> "Semi-Slav Defense: Meran Variation, Reynolds' Variation"

### `D.Sem.Mer.MLn.c5.e5.cxd4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'cxd4 Line' -> ''

### `D.Sem.Mer.MLn.b4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'b4 Line|Semi-Slav Defense: Meran Variation, Pirc Variation' -> 'Semi-Slav Defense: Meran Variation, Pirc Variation'

### `E.Gru.Nf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf3 Line|Grünfeld Defense, Nf3|Grünfeld Defense: Three Knights Variation' -> 'Grünfeld Defense, Nf3|Grünfeld Defense: Three Knights Variation'

### `E.Gru.Thr.e3.O-O` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'O-O Line' -> ''

### `E.Gru.Thr.e3.O-O.Bd3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bd3 Line|Grünfeld Defense: Three Knights Variation, Paris Variation' -> 'Grünfeld Defense: Three Knights Variation, Paris Variation'

### `E.Gru.Thr.e3.O-O.Qb3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qb3 Line|Grünfeld Defense: Three Knights Variation, Vienna Variation' -> 'Grünfeld Defense: Three Knights Variation, Vienna Variation'

### `E.Gru.Exc.SeV.Nf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf3 Line|Grünfeld Defense: Exchange Variation, Modern Exchange Variation' -> 'Grünfeld Defense: Exchange Variation, Modern Exchange Variation'

### `E.Gru.Exc.SeV.Bc4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bc4 Line|Grünfeld Defense: Exchange Variation, Classical Variation' -> 'Grünfeld Defense: Exchange Variation, Classical Variation'

### `E.Gru.Exc.SeV.Bc4.O-O` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'O-O Line' -> ''

### `E.Gru.Exc.SeV.Bc4.c5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c5 Line' -> ''

### `E.Gru.Exc.SeV.Bc4.c5.Ne2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Ne2 Line' -> ''

### `E.Gru.Rus.Hng.e4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e4 Line' -> ''

### `E.Gru.Rus.Hng.e4.a6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'a6 Line' -> ''

### `E.Gru.Rus.Hng.e4.b6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'b6 Line|Grünfeld Defense: Russian Variation, Levenfish Variation' -> 'Grünfeld Defense: Russian Variation, Levenfish Variation'

### `E.Gru.Rus.Hng.e4.Bg4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bg4 Line|Grünfeld Defense: Russian Variation, Smyslov Variation' -> 'Grünfeld Defense: Russian Variation, Smyslov Variation'

### `E.KID.e4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "e4 Line|King's Indian Defense, e4|King's Indian Defense: Normal Variation" -> "King's Indian Defense, e4|King's Indian Defense: Normal Variation"

### `E.KID.Nf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Nf3 Line|King's Indian Defense, Nf3" -> "King's Indian Defense, Nf3"

### `E.KID.Nf3.d6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "d6 Line|King's Indian Defense Nf3, d6" -> "King's Indian Defense Nf3, d6"

### `E.KID.Nf3.Cst.e3.d6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd6 Line' -> ''

### `E.KID.Nf3.Cst.e3.d6.Be2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be2 Line' -> ''

### `E.KID.Sml.Cst.Bg5.c5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c5 Line' -> ''

### `E.KID.Sml.Cst.Bg5.c5.d5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "d5 Line|Benoni Defense: King's Pawn Line, with Bg5" -> "Benoni Defense: King's Pawn Line, with Bg5"

### `E.KID.Sml.Cst.Be3.Nc6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Nc6 Line|King's Indian Defense: Sämisch Variation, Yates Defense" -> "King's Indian Defense: Sämisch Variation, Yates Defense"

### `E.KID.Sml.Cst.Nge2.c5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c5 Line' -> ''

### `E.KID.Avk.Cst.Bg5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bg5 Line' -> ''

### `E.Nim.Cls.O-O` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'O-O Line' -> ''

### `E.Nim.Cls.O-O.a3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'a3 Line' -> ''

### `E.Nim.Cls.O-O.e3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e3 Line' -> ''

### `E.Nim.Cls.O-O.e3.d5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd5 Line' -> ''

### `E.Nim.Cls.O-O.e3.d5.Nf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf3 Line' -> ''

### `E.Nim.Cls.d5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd5 Line|Nimzo-Indian Defense: Classical Variation, Noa Variation' -> 'Nimzo-Indian Defense: Classical Variation, Noa Variation'

### `E.Nim.Cls.d5.cxd5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'cxd5 Line' -> ''

### `E.Nim.Cls.d5.cxd5.exd5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'exd5 Line|Nimzo-Indian Defense: Classical Variation, Noa Variation' -> 'Nimzo-Indian Defense: Classical Variation, Noa Variation'

### `E.Nim.Cls.d5.a3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'a3 Line|Nimzo-Indian Defense: Classical Variation, Noa Variation' -> 'Nimzo-Indian Defense: Classical Variation, Noa Variation'

### `E.Nim.Cls.c5.dxc5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'dxc5 Line' -> ''

### `E.Nim.Cls.c5.dxc5.Bxc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bxc3 Line|Nimzo-Indian Defense: Classical Variation, Berlin Variation, Steiner Variation' -> 'Nimzo-Indian Defense: Classical Variation, Berlin Variation, Steiner Variation'

### `E.Nim.Cls.c5.dxc5.O-O` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'O-O Line|Nimzo-Indian Defense: Classical Variation, Berlin Variation, Pirc Variation' -> 'Nimzo-Indian Defense: Classical Variation, Berlin Variation, Pirc Variation'

### `E.Nim.Rub.Res.MLn.O-O` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'O-O Line' -> ''

### `E.Nim.Rub.Res.MLn.O-O.Nbd7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nbd7 Line|Nimzo-Indian Defense: Normal Variation, Gligoric System' -> 'Nimzo-Indian Defense: Normal Variation, Gligoric System'

### `E.Nim.Rub.Res.MLn.O-O.b6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'b6 Line|Nimzo-Indian Defense: Normal Variation, Gligoric System, Keres Variation' -> 'Nimzo-Indian Defense: Normal Variation, Gligoric System, Keres Variation'

### `E.Nim.Rub.Res.MLn.O-O.dxc4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'dxc4 Line' -> ''

### `E.Ind.Cat.Bb4.Bd2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bd2 Line' -> ''

### `E.Ind.Cat.Bb4.Bd2.Be7.Bg2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bg2 Line' -> ''

### `E.Ind.e6.Nf3.c5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c5 Line' -> ''

### `E.Ind.e6.Nf3.c5.d5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd5 Line' -> ''

### `E.Ind.e6.Nf3.c5.d5.exd5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'exd5 Line' -> ''

### `E.Ben.d5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd5 Line|Benoni Defense, d5' -> 'Benoni Defense, d5'

### `E.Ben.d5.e6.Nc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc3 Line|Benoni Defense d5 e6, Nc3' -> 'Benoni Defense d5 e6, Nc3'

### `E.Ben.d5.e6.Nc3.exd5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'exd5 Line|Benoni Defense d5 e6 Nc3, exd5' -> 'Benoni Defense d5 e6 Nc3, exd5'

### `E.Ben.d5.e6.Nc3.exd5.cxd5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'cxd5 Line|Benoni Defense d5 e6 Nc3, cxd5' -> 'Benoni Defense d5 e6 Nc3, cxd5'

### `E.Ben.dxc5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'dxc5 Line|Benoni Defense, dxc5' -> 'Benoni Defense, dxc5'

### `E.Ben.Old.Adv.Nf6.Nf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf3 Line|Benoni Defense: Benoni-Indian Defense, Kingside Move Order' -> 'Benoni Defense: Benoni-Indian Defense, Kingside Move Order'

### `E.Ben.Old.Adv.Nf6.Nc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc3 Line' -> ''

### `E.Ben.Old.Adv.e5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e5 Line' -> ''

### `E.Ben.Bnk.Nf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf3 Line' -> ''

### `E.Ben.Bnk.Acc.Nc3.axb5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'axb5 Line' -> ''

### `A.Eng.Rev.e3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e3 Line' -> ''

### `A.Eng.Rev.e3.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf6 Line' -> ''

### `A.Eng.Rev.g3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'g3 Line' -> ''

### `A.Eng.Rev.g3.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf6 Line' -> ''

### `A.Eng.Rev.g3.Nf6.Bg2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bg2 Line' -> ''

### `A.Eng.Rev.g3.Nf6.Bg2.d5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd5 Line' -> ''

### `A.Eng.Rev.Nc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Nc3 Line|English Opening: King's English Variation, Reversed Sicilian" -> "English Opening: King's English Variation, Reversed Sicilian"

### `A.Eng.Rev.Nc3.d6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd6 Line' -> ''

### `A.Eng.Rev.Nc3.d6.Nf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Nf3 Line|English Opening: King's English Variation" -> "English Opening: King's English Variation"

### `A.Eng.Rev.Nc3.Nf6.Nf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf3 Line' -> ''

### `A.Eng.Rev.Nc3.Nf6.Nf3.e4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e4 Line' -> ''

### `A.Eng.Rev.Nc3.Nf6.g3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'g3 Line|English Opening: Carls-Bremen System' -> 'English Opening: Carls-Bremen System'

### `A.Eng.Rev.Nc3.Nc6.g3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'g3 Line' -> ''

### `A.Eng.Rev.Fou.e3.Bb4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bb4 Line' -> ''

### `A.Eng.Rev.Fou.g3.Bc5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bc5 Line' -> ''

### `A.Eng.Rev.Fou.g3.Bc5.d3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd3 Line' -> ''

### `A.Eng.Sym.Nf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf3 Line' -> ''

### `A.Eng.Sym.Nf3.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf6 Line' -> ''

### `A.Eng.Sym.Nf3.Nf6.Nc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc3 Line|Three Knights Line' -> 'Three Knights Line'

### `A.Eng.Sym.Nc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc3 Line|English Opening: Symmetrical Variation, Normal Variation' -> 'English Opening: Symmetrical Variation, Normal Variation'

### `A.Eng.Sym.Nc3.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf6 Line' -> ''

### `A.Eng.Sym.Nc3.Nf6.Nf3.e5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e5 Line' -> ''

### `A.Eng.Sym.Nc3.Nc6.g3.g6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'g6 Line' -> ''

### `A.Hol.h3.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf6 Line' -> ''

### `A.Hol.Nf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf3 Line|Dutch Defense, Nf3' -> 'Dutch Defense, Nf3'

### `A.Hol.Bf4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bf4 Line|Dutch Defense, Bf4' -> 'Dutch Defense, Bf4'

### `A.Hol.Bf4.e6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e6 Line|Dutch Defense Bf4, e6' -> 'Dutch Defense Bf4, e6'

### `A.Hol.c4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c4 Line|Dutch Defense, c4' -> 'Dutch Defense, c4'

### `A.Hol.c4.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf6 Line|Dutch Defense c4, Nf6|Dutch Defense: Normal Variation' -> 'Dutch Defense c4, Nf6|Dutch Defense: Normal Variation'

### `A.Hol.c4.Nf6.Nc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Nc3 Line|Dutch Defense c4 Nf6, Nc3|Dutch Defense: Queen's Knight Variation" -> "Dutch Defense c4 Nf6, Nc3|Dutch Defense: Queen's Knight Variation"

### `A.Hol.c4.Nf6.g3.g6.Bg2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bg2 Line' -> ''

### `A.Hol.c4.Nf6.g3.e6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e6 Line|Dutch Defense c4 Nf6, e6' -> 'Dutch Defense c4 Nf6, e6'

### `A.Hol.c4.Nf6.g3.e6.Bg2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bg2 Line|Dutch Defense c4 Nf6 e6, Bg2|Dutch Defense: Classical Variation' -> 'Dutch Defense c4 Nf6 e6, Bg2|Dutch Defense: Classical Variation'

### `A.Hol.c4.e6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e6 Line|Dutch Defense c4, e6|Dutch Defense: Classical Variation' -> 'Dutch Defense c4, e6|Dutch Defense: Classical Variation'

### `A.Hol.c4.g6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'g6 Line|Dutch Defense c4, g6' -> 'Dutch Defense c4, g6'

### `A.Hol.Sta.fxe4.Nc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc3 Line' -> ''

### `A.Hol.Sta.fxe4.Nc3.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf6 Line' -> ''

### `A.Pol.e5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e5 Line' -> ''

### `A.Pol.e5.Bb2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bb2 Line' -> ''

### `A.Pol.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf6 Line' -> ''

### `A.Pol.Nf6.Bb2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bb2 Line' -> ''

### `A.Pol.e6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e6 Line' -> ''

### `A.Pol.e6.Bb2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bb2 Line' -> ''

### `A.Pol.e6.Bb2.Nf6.b5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'b5 Line' -> ''

### `A.Van.d5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd5 Line' -> ''

### `A.Van.d5.f4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'f4 Line' -> ''

### `A.Van.d5.f4.d4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd4 Line' -> ''

### `A.Van.d5.f4.e5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e5 Line|Van Geet Opening: Damhaug Gambit' -> 'Van Geet Opening: Damhaug Gambit'

### `A.Van.c5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c5 Line' -> ''

### `A.Van.c5.Nf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf3 Line' -> ''

### `A.Van.c5.Nf3.Nc6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc6 Line' -> ''

### `A.Van.d6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd6 Line' -> ''

### `A.Van.f5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'f5 Line' -> ''

### `A.Van.g6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'g6 Line' -> ''

### `A.Hng.d5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd5 Line' -> ''

### `A.Hng.d5.Bg2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bg2 Line' -> ''

### `A.Hng.e5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e5 Line' -> ''

### `A.Hng.e5.a3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'a3 Line' -> ''

### `A.Hng.e5.a3.d5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd5 Line' -> ''

### `A.Hng.Nc6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc6 Line' -> ''

### `A.Hng.Nc6.Nc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc3 Line' -> ''

### `A.Hng.Nc6.Nc3.d5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd5 Line' -> ''

### `A.Lar.Nf6.Bb2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bb2 Line' -> ''

### `A.Lar.f5.Bb2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bb2 Line' -> ''

### `A.Egl.dxe5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'dxe5 Line' -> ''

### `A.Egl.dxe5.Nc6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc6 Line' -> ''

### `A.Egl.dxe5.Nc6.Nf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf3 Line' -> ''

### `A.QPO.Nf6.Nf3.e6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e6 Line' -> ''

### `A.EID.Bf4.Bg7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bg7 Line' -> ''

### `A.EID.Bf4.Bg7.e3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e3 Line' -> ''

### `A.EID.Bf4.Bg7.e3.d6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd6 Line' -> ''

### `A.EID.Bg5.Bg7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bg7 Line' -> ''

### `A.EID.Bg5.Bg7.Nbd2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nbd2 Line' -> ''

### `A.EID.Bg5.Bg7.Nbd2.d5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd5 Line' -> ''

### `A.EID.Nc3.d5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd5 Line' -> ''

### `A.EID.Nc3.d5.Bf4.Bg7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Bg7 Line|Queen's Pawn Game: Barry Attack" -> "Queen's Pawn Game: Barry Attack"

### `A.EID.Nc3.d5.Bf4.Bg7.e3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e3 Line' -> ''

### `C.RyL.Mor.Ba4.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf6 Line' -> ''

### `C.RyL.Mor.Ba4.Nf6.O-O.Be7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be7 Line|Ruy López: Closed' -> 'Ruy López: Closed'

### `C.RyL.Ber.O-O.Nxe4.d4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd4 Line' -> ''

### `C.RyL.Mor.Opn.d4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd4 Line' -> ''

### `C.RyL.Mor.Opn.d4.b5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'b5 Line' -> ''

### `C.RyL.Mor.Opn.d4.b5.Bb3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bb3 Line' -> ''

### `C.RyL.Mor.Opn.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `C.RyL.Mor.Opn.MLn.dxe5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'dxe5 Line' -> ''

### `C.RyL.Mor.Opn.MLn.dxe5.Be6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be6 Line' -> ''

### `C.Ita.Giu.O-O.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf6 Line' -> ''

### `C.Ita.Giu.O-O.Nf6.c3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c3 Line|Italian Game: Classical Variation, Albin Gambit' -> 'Italian Game: Classical Variation, Albin Gambit'

### `C.Ita.Giu.O-O.Nf6.d4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd4 Line|Italian Game: Deutz Gambit' -> 'Italian Game: Deutz Gambit'

### `C.Ita.Giu.O-O.Nf6.d3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd3 Line' -> ''

### `C.Ita.Giu.c3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c3 Line|Italian Game: Classical Variation' -> 'Italian Game: Classical Variation'

### `C.Ita.Giu.c3.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf6 Line|Italian Game: Classical Variation' -> 'Italian Game: Classical Variation'

### `C.Ita.Giu.c3.Nf6.d4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd4 Line|Italian Game: Classical Variation, Center Attack' -> 'Italian Game: Classical Variation, Center Attack'

### `C.Ita.Giu.c3.Nf6.d4.exd4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'exd4 Line' -> ''

### `C.Ita.Giu.c3.Nf6.d3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd3 Line|Italian Game: Classical Variation, Giuoco Pianissimo' -> 'Italian Game: Classical Variation, Giuoco Pianissimo'

### `C.Ita.Giu.c3.Nf6.d3.d6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd6 Line|Italian Game: Classical Variation, Giuoco Pianissimo' -> 'Italian Game: Classical Variation, Giuoco Pianissimo'

### `C.Ita.Giu.c3.Nf6.d3.d5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd5 Line|Italian Game: Classical Variation, with d5' -> 'Italian Game: Classical Variation, with d5'

### `C.Ita.Giu.c3.Qe7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qe7 Line|Italian Game: Classical Variation, Closed Variation' -> 'Italian Game: Classical Variation, Closed Variation'

### `C.Ita.Giu.c3.Qe7.d4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd4 Line' -> ''

### `C.Ita.Giu.c3.d6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd6 Line' -> ''

### `C.Ita.Giu.c3.d6.d4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd4 Line' -> ''

### `C.Ita.Evn.Acc.c3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c3 Line' -> ''

### `C.Ita.Evn.Acc.c3.Bc5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bc5 Line|Italian Game: Evans Gambit, McDonnell Defense' -> 'Italian Game: Evans Gambit, McDonnell Defense'

### `C.Ita.Evn.Acc.c3.Bc5.d4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd4 Line' -> ''

### `C.Ita.Evn.Acc.c3.Be7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be7 Line|Italian Game: Evans Gambit, Anderssen Variation' -> 'Italian Game: Evans Gambit, Anderssen Variation'

### `C.Ita.Evn.Acc.c3.Bf8` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bf8 Line|Italian Game: Evans Gambit, Mayet Defense' -> 'Italian Game: Evans Gambit, Mayet Defense'

### `C.Ita.Evn.Acc.c3.Bd6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bd6 Line|Italian Game: Evans Gambit, Stone-Ware Variation' -> 'Italian Game: Evans Gambit, Stone-Ware Variation'

### `C.Ita.Evn.Dec.a4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'a4 Line|Italian Game: Evans Gambit Declined' -> 'Italian Game: Evans Gambit Declined'

### `C.Ita.Evn.Dec.Bb2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bb2 Line|Italian Game: Evans Gambit Declined, Cordel Variation' -> 'Italian Game: Evans Gambit Declined, Cordel Variation'

### `C.Ita.Evn.Dec.b5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'b5 Line' -> ''

### `C.Ita.Evn.Dec.b5.Na5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Na5 Line' -> ''

### `C.Ita.Evn.Dec.b5.Na5.Nxe5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nxe5 Line' -> ''

### `C.Ita.Two.Nc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc3 Line|Four Knights Game: Italian Variation' -> 'Four Knights Game: Italian Variation'

### `C.Ita.Two.Nc3.Nxe4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nxe4 Line' -> ''

### `C.Ita.Two.O-O.Bc5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bc5 Line' -> ''

### `C.Ita.Two.O-O.Bc5.d4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd4 Line' -> ''

### `C.Ita.Two.O-O.Bc5.d4.Bxd4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bxd4 Line' -> ''

### `C.Cen.d6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd6 Line' -> ''

### `C.Cen.d6.dxe5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'dxe5 Line' -> ''

### `C.Cen.exd4.Qxd4.Nc6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc6 Line|Center Game: Normal Variation' -> 'Center Game: Normal Variation'

### `C.Cen.exd4.Qxd4.Nc6.Qc4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qc4 Line|Center Game: Hall Variation' -> 'Center Game: Hall Variation'

### `C.Cen.exd4.Nf3.c5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c5 Line|Center Game: Kieseritzky Variation' -> 'Center Game: Kieseritzky Variation'

### `C.Cen.exd4.Nf3.Bc5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bc5 Line' -> ''

### `C.Cen.exd4.Bc4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bc4 Line|Center Game: von der Lasa Gambit' -> 'Center Game: von der Lasa Gambit'

### `C.Cen.exd4.Bd3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bd3 Line|Center Game: Ross Gambit' -> 'Center Game: Ross Gambit'

### `C.KGm.Acc.Bsh.g5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "g5 Line|King's Gambit Accepted: Bishop's Gambit, Anderssen Defense" -> "King's Gambit Accepted: Bishop's Gambit, Anderssen Defense"

### `C.KGm.Acc.Bsh.d5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "d5 Line|King's Gambit Accepted: Bishop's Gambit, Bledow Variation" -> "King's Gambit Accepted: Bishop's Gambit, Bledow Variation"

### `C.KGm.Acc.Bsh.d5.Bxd5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bxd5 Line' -> ''

### `C.KGm.Acc.Bsh.d5.Bxd5.c6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "c6 Line|King's Gambit Accepted: Bishop's Gambit, Anderssen Variation" -> "King's Gambit Accepted: Bishop's Gambit, Anderssen Variation"

### `C.KGm.Acc.Bsh.d5.Bxd5.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Nf6 Line|King's Gambit Accepted: Bishop's Gambit, Bledow Countergambit" -> "King's Gambit Accepted: Bishop's Gambit, Bledow Countergambit"

### `C.KGm.Acc.Bsh.Qh4.Kf1` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Kf1 Line' -> ''

### `C.KGm.Acc.Bsh.Qh4.Kf1.Nc6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Nc6 Line|King's Gambit Accepted: Bishop's Gambit, Boden Variation" -> "King's Gambit Accepted: Bishop's Gambit, Boden Variation"

### `C.KGm.Acc.Bsh.Qh4.Kf1.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Nf6 Line|King's Gambit Accepted: Bishop's Gambit, First Jaenisch Variation" -> "King's Gambit Accepted: Bishop's Gambit, First Jaenisch Variation"

### `C.KGm.Acc.Bsh.Qh4.Kf1.Bc5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Bc5 Line|King's Gambit Accepted: Bishop's Gambit, Greco Variation" -> "King's Gambit Accepted: Bishop's Gambit, Greco Variation"

### `C.KGm.Acc.Bsh.Qh4.Kf1.d6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "d6 Line|King's Gambit Accepted: Bishop's Gambit, Cozio Variation" -> "King's Gambit Accepted: Bishop's Gambit, Cozio Variation"

### `C.KGm.Acc.Bsh.Qh4.Kf1.b5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "b5 Line|King's Gambit Accepted: Bishop's Gambit, Bryan Countergambit" -> "King's Gambit Accepted: Bishop's Gambit, Bryan Countergambit"

### `C.KGm.Acc.Bsh.Qh4.Kf1.Ne7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Ne7 Line' -> ''

### `C.KGm.Acc.Bsh.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Nf6 Line|King's Gambit Accepted: Bishop's Gambit, Cozio Defense" -> "King's Gambit Accepted: Bishop's Gambit, Cozio Defense"

### `C.KGm.Acc.Bsh.f5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "f5 Line|King's Gambit Accepted: Bishop's Gambit, Gianutio Gambit" -> "King's Gambit Accepted: Bishop's Gambit, Gianutio Gambit"

### `C.KGm.Acc.Bsh.b5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "b5 Line|King's Gambit Accepted: Bishop's Gambit, Kieseritzky Gambit" -> "King's Gambit Accepted: Bishop's Gambit, Kieseritzky Gambit"

### `C.KGm.Acc.Bsh.c6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "c6 Line|King's Gambit Accepted: Bishop's Gambit, López Defense" -> "King's Gambit Accepted: Bishop's Gambit, López Defense"

### `C.KGm.Acc.Bsh.Nc6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Nc6 Line|King's Gambit Accepted: Bishop's Gambit, Maurian Defense" -> "King's Gambit Accepted: Bishop's Gambit, Maurian Defense"

### `C.KGm.Acc.Bsh.Ne7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Ne7 Line|King's Gambit Accepted: Bishop's Gambit, Steinitz Defense" -> "King's Gambit Accepted: Bishop's Gambit, Steinitz Defense"

### `C.KGm.Acc.Kie.d5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "d5 Line|King's Gambit Accepted: Kieseritzky Gambit, Brentano Defense" -> "King's Gambit Accepted: Kieseritzky Gambit, Brentano Defense"

### `C.KGm.Acc.Kie.d5.d4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd4 Line' -> ''

### `C.KGm.Acc.Kie.d5.d4.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf6 Line' -> ''

### `C.KGm.Acc.Kie.h5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "h5 Line|King's Gambit Accepted: Kieseritzky Gambit, Long Whip" -> "King's Gambit Accepted: Kieseritzky Gambit, Long Whip"

### `C.KGm.Acc.Kie.Nc6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Nc6 Line|King's Gambit Accepted: Kieseritzky Gambit, Neumann Defense" -> "King's Gambit Accepted: Kieseritzky Gambit, Neumann Defense"

### `C.KGm.Acc.Kie.Bg7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Bg7 Line|King's Gambit Accepted: Kieseritzky Gambit, Paulsen Defense" -> "King's Gambit Accepted: Kieseritzky Gambit, Paulsen Defense"

### `C.KGm.Acc.Kie.Qe7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Qe7 Line|King's Gambit Accepted: Kieseritzky Gambit, Rosenthal Defense" -> "King's Gambit Accepted: Kieseritzky Gambit, Rosenthal Defense"

### `C.KGm.Acc.Kie.Be7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Be7 Line|King's Gambit Accepted: Kieseritzky, Polerio Defense" -> "King's Gambit Accepted: Kieseritzky, Polerio Defense"

### `C.Pet.Cls.Bd3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bd3 Line' -> ''

### `C.Pet.Cls.Bd3.Nc6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Nc6 Line|Petrov's Defense: Classical Attack, Mason-Showalter Variation" -> "Petrov's Defense: Classical Attack, Mason-Showalter Variation"

### `C.Pet.Cls.Bd3.Nc6.O-O.Be7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be7 Line' -> ''

### `C.Pet.Cls.Bd3.Bd6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Bd6 Line|Petrov's Defense: Classical Attack, Marshall Variation" -> "Petrov's Defense: Classical Attack, Marshall Variation"

### `C.KPO.Kgt.MLn.Nxe5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nxe5 Line|Irish Gambit' -> 'Irish Gambit'

### `C.KPO.Kgt.MLn.g3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "g3 Line|King's Knight Opening: Konstantinopolsky" -> "King's Knight Opening: Konstantinopolsky"

### `C.KPO.Kgt.MLn.c4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "c4 Line|King's Pawn Game: Dresden Opening" -> "King's Pawn Game: Dresden Opening"

### `C.KPO.Kgt.MLn.c4.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf6 Line' -> ''

### `C.KPO.Kgt.MLn.b4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "b4 Line|King's Pawn Game: Pachman Wing Gambit" -> "King's Pawn Game: Pachman Wing Gambit"

### `C.KPO.Kgt.MLn.Be2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Be2 Line|King's Pawn Game: Tayler Opening" -> "King's Pawn Game: Tayler Opening"

### `C.KPO.Kgt.MLn.Be2.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf6 Line' -> ''

### `C.KPO.Kgt.MLn.Be2.Nf6.d4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "d4 Line|King's Pawn Game: Tayler Opening" -> "King's Pawn Game: Tayler Opening"

### `C.KPO.Kgt.MLn.d3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd3 Line' -> ''

### `C.KPO.Kgt.MLn.d3.f5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'f5 Line' -> ''

### `B.Nim.ScD.exd5.Qxd5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qxd5 Line' -> ''

### `B.Nim.ScD.Nc3.dxe4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'dxe4 Line' -> ''

### `B.Nim.Ken.d5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd5 Line|Nimzowitsch Defense: Kennedy Variation, Linksspringer Variation' -> 'Nimzowitsch Defense: Kennedy Variation, Linksspringer Variation'

### `B.Nim.Ken.d5.Nce7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `B.Nim.Ken.dxe5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'dxe5 Line' -> ''

### `B.Nim.Ken.dxe5.Nxe5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nxe5 Line' -> ''

### `B.Nim.Ken.dxe5.Nxe5.f4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'f4 Line' -> ''

### `B.Nim.Ken.dxe5.Nxe5.f4.Ng6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `B.Fre.Adv.c5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c5 Line' -> ''

### `B.Fre.Adv.c5.c3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c3 Line' -> ''

### `B.Fre.Adv.c5.c3.Nc6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc6 Line' -> ''

### `B.Fre.Adv.c5.c3.Nc6.Nf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf3 Line|French Defense: Advance Variation, Paulsen Attack' -> 'French Defense: Advance Variation, Paulsen Attack'

### `B.Fre.Adv.c5.c3.Qb6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qb6 Line' -> ''

### `B.Fre.Adv.c5.Nf3.cxd4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'cxd4 Line' -> ''

### `B.CaK.Adv.Bf5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bf5 Line' -> ''

### `B.CaK.Adv.Bf5.Nf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf3 Line|Caro-Kann Defense: Advance Variation, Short Variation' -> 'Caro-Kann Defense: Advance Variation, Short Variation'

### `B.CaK.Adv.Bf5.Nf3.e6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e6 Line' -> ''

### `B.CaK.Adv.Bf5.Nc3.e6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e6 Line' -> ''

### `B.CaK.Adv.Bf5.c3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c3 Line' -> ''

### `B.Sic.OKn.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf6 Line|Open Sicilian Nf6' -> 'Open Sicilian Nf6'

### `B.Sic.OKn.Nf6.Nc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc3 Line' -> ''

### `B.Sic.Kan.Bd3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bd3 Line|Sicilian Defense: Kan Variation, Modern Variation' -> 'Sicilian Defense: Kan Variation, Modern Variation'

### `B.Sic.Kan.Bd3.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf6 Line' -> ''

### `B.Sic.Cls.Be2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be2 Line' -> ''

### `B.Sic.Cls.Soz.e6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e6 Line' -> ''

### `B.Sic.Cls.Soz.e6.Be3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `B.Sic.Acc.Nc3.Bg7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bg7 Line' -> ''

### `B.Sic.Acc.Nc3.Bg7.Be3.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf6 Line' -> ''

### `B.Sic.Acc.Be3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be3 Line' -> ''

### `B.Sic.Acc.Be3.Bg7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bg7 Line' -> ''

### `B.Sic.Sve.Ndb5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Ndb5 Line' -> ''

### `B.Sic.Sve.Ndb5.d6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd6 Line' -> ''

### `B.Sic.Sve.Ndb5.d6.Bg5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bg5 Line' -> ''

### `B.Sic.Sve.Ndb5.d6.Bg5.a6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'a6 Line' -> ''

### `B.Sic.Dra.Be3.Bg7.f3.Nc6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc6 Line|Sicilian Defense: Dragon Variation, Yugoslav Attack, Belezky Line' -> 'Sicilian Defense: Dragon Variation, Yugoslav Attack, Belezky Line'

### `B.Sic.Dra.Yug.Nc6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc6 Line' -> ''

### `B.Sic.Dra.Yug.Nc6.Bc4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bc4 Line' -> ''

### `A.Hor.Fch.MLn.Bg5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bg5 Line' -> ''

### `A.Hor.Fch.MLn.Bg5.c5.cxd5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'cxd5 Line' -> ''

### `A.Hor.Fch.MLn.Bg5.Nbd7.e3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e3 Line' -> ''

### `A.Hor.Fch.MLn.Bg5.Be7.Nf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf3 Line' -> ''

### `A.Kan.MLn.e3.c5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c5 Line' -> ''

### `A.Kan.MLn.e3.c5.Bd3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bd3 Line' -> ''

### `A.Kan.MLn.e3.c5.Bd3.Nc6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc6 Line' -> ''

### `A.Kan.MLn.e3.Ne4.Qc2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qc2 Line' -> ''

### `A.Ret.Eng.Be7.O-O.O-O.b3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'b3 Line' -> ''

### `A.Ret.Eng.Be7.b3.b6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'b6 Line' -> ''

### `A.Ret.Eng.Be7.b3.c5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c5 Line' -> ''

### `A.Ret.Eng.c5.b3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'b3 Line' -> ''

### `A.Ret.Eng.c5.b3.Nc6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc6 Line' -> ''

### `A.Ret.Ang.g3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'g3 Line' -> ''

### `A.Ret.Ang.g3.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf6 Line' -> ''

### `A.Ret.Ang.g3.Nf6.Bg2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bg2 Line' -> ''

### `A.Ret.Ang.g3.Nf6.Bg2.dxc4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'dxc4 Line' -> ''

### `A.Ret.Ang.g3.Nf6.Bg2.Bf5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bf5 Line' -> ''

### `A.Ret.Ang.g3.Nf6.b3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'b3 Line' -> ''

### `A.Ret.Ang.b3.Bg4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bg4 Line|Réti Opening: Anglo-Slav Variation, Bogoljubow Variation' -> 'Réti Opening: Anglo-Slav Variation, Bogoljubow Variation'

### `A.Ret.Ang.b3.Bf5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bf5 Line|Réti Opening: Anglo-Slav Variation, Bogoljubow Variation' -> 'Réti Opening: Anglo-Slav Variation, Bogoljubow Variation'

### `A.Ret.Ang.b3.Bf5.Bb2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bb2 Line|Réti Opening: Anglo-Slav Variation, Bogoljubow Variation' -> 'Réti Opening: Anglo-Slav Variation, Bogoljubow Variation'

### `A.Eng.Rev.Nc3.Nf6.g3.Bc5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bc5 Line' -> ''

### `A.Eng.Rev.Nc3.Nc6.g3.d6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd6 Line' -> ''

### `A.Bir.Fro.fxe5.d6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd6 Line' -> ''

### `A.Bir.Fro.fxe5.d6.exd6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'exd6 Line' -> ''

### `A.Bir.Fro.fxe5.d6.exd6.Bxd6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bxd6 Line' -> ''

### `A.Bir.Fro.d4.exd4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'exd4 Line' -> ''

### `A.QPO.Nf6.Nd2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nd2 Line' -> ''

### `A.QPO.Nf6.e4.Nxe4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nxe4 Line' -> ''

### `C.RyL.Ber.O-O.Bc5.c3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c3 Line|Ruy López: Classical Variation, Zukertort Gambit' -> 'Ruy López: Classical Variation, Zukertort Gambit'

### `C.RyL.Ber.O-O.d6.d4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd4 Line' -> ''

### `C.RyL.Ber.O-O.d6.d4.Bd7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bd7 Line' -> ''

### `C.RyL.Ber.O-O.d6.d4.Nd7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nd7 Line|Ruy López: Closed Berlin Defense, Chigorin Variation' -> 'Ruy López: Closed Berlin Defense, Chigorin Variation'

### `C.RyL.Ber.O-O.d6.Bxc6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bxc6 Line' -> ''

### `C.RyL.Cls.c3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c3 Line' -> ''

### `C.RyL.Cls.c3.O-O.h3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'h3 Line' -> ''

### `C.RyL.Cls.c3.O-O.h3.Bb7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bb7 Line|Ruy López: Closed, Flohr System' -> 'Ruy López: Closed, Flohr System'

### `C.RyL.Cls.c3.O-O.h3.Be6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be6 Line|Ruy López: Closed, Kholmov Variation' -> 'Ruy López: Closed, Kholmov Variation'

### `C.RyL.Cls.c3.O-O.h3.Re8` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Re8 Line|Ruy López: Closed, Zaitsev System' -> 'Ruy López: Closed, Zaitsev System'

### `C.RyL.Cls.c3.Na5.Bc2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bc2 Line' -> ''

### `C.RyL.Cls.c3.Na5.Bc2.c5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c5 Line' -> ''

### `C.RyL.Cls.d4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd4 Line|Ruy López: Closed, Rosen Attack' -> 'Ruy López: Closed, Rosen Attack'

### `C.RyL.Exc.dxc6.Nc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc3 Line|Ruy López: Exchange Variation, Keres Variation' -> 'Ruy López: Exchange Variation, Keres Variation'

### `C.RyL.Exc.dxc6.Nc3.f6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'f6 Line' -> ''

### `C.RyL.Exc.dxc6.Nc3.f6.d3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd3 Line|Ruy López: Exchange Variation, Romanovsky Variation' -> 'Ruy López: Exchange Variation, Romanovsky Variation'

### `C.RyL.Exc.dxc6.O-O.Bg4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bg4 Line' -> ''

### `C.RyL.Exc.dxc6.O-O.Bg4.h3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'h3 Line' -> ''

### `C.RyL.Exc.dxc6.O-O.Qd6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qd6 Line|Ruy López: Exchange Variation, Bronstein Variation' -> 'Ruy López: Exchange Variation, Bronstein Variation'

### `C.RyL.Exc.dxc6.O-O.f6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'f6 Line|Ruy López: Exchange Variation, Gligoric Variation' -> 'Ruy López: Exchange Variation, Gligoric Variation'

### `C.RyL.Exc.dxc6.O-O.Bd6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Bd6 Line|Ruy López: Exchange Variation, King's Bishop Variation" -> "Ruy López: Exchange Variation, King's Bishop Variation"

### `C.RyL.Exc.dxc6.d4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd4 Line' -> ''

### `C.RyL.Exc.dxc6.d4.exd4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'exd4 Line' -> ''

### `C.RyL.Exc.dxc6.d4.exd4.Qxd4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qxd4 Line' -> ''

### `C.RyL.Mor.Ba4.d6.Nc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc3 Line|Ruy López: Morphy Defense, Modern Steinitz Defense' -> 'Ruy López: Morphy Defense, Modern Steinitz Defense'

### `C.RyL.Mor.Ba4.d6.c4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c4 Line|Ruy López: Morphy Defense, Modern Steinitz Defense' -> 'Ruy López: Morphy Defense, Modern Steinitz Defense'

### `C.RyL.Mor.Ba4.d6.O-O.Bd7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bd7 Line' -> ''

### `C.RyL.Mor.Ba4.d6.c3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c3 Line|Ruy López: Morphy Defense, Modern Steinitz Defense' -> 'Ruy López: Morphy Defense, Modern Steinitz Defense'

### `C.RyL.Mor.Ba4.d6.c3.Bd7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bd7 Line|Ruy López: Morphy Defense, Modern Steinitz Defense' -> 'Ruy López: Morphy Defense, Modern Steinitz Defense'

### `C.RyL.Mor.Ba4.d6.Bxc6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bxc6 Line' -> ''

### `C.RyL.Mor.Ba4.Nf6.O-O.d5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd5 Line|Ruy López: Central Countergambit' -> 'Ruy López: Central Countergambit'

### `C.RyL.Mor.Ba4.Nf6.O-O.b5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'b5 Line' -> ''

### `C.RyL.Mor.Ba4.Nf6.O-O.d6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd6 Line|Ruy López: Morphy Defense, Steinitz Deferred' -> 'Ruy López: Morphy Defense, Steinitz Deferred'

### `C.KGm.Dec.Fal.exd5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "exd5 Line|King's Gambit Declined: Falkbeer Countergambit Accepted" -> "King's Gambit Declined: Falkbeer Countergambit Accepted"

### `C.KGm.Dec.Fal.Nf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Nf3 Line|King's Gambit Declined: Falkbeer Countergambit, Blackburne Attack" -> "King's Gambit Declined: Falkbeer Countergambit, Blackburne Attack"

### `C.KGm.Dec.Fal.d4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "d4 Line|King's Gambit Declined: Falkbeer Countergambit, Hinrichsen Gambit" -> "King's Gambit Declined: Falkbeer Countergambit, Hinrichsen Gambit"

### `C.KGm.Dec.Fal.Nc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Nc3 Line|King's Gambit Declined: Falkbeer Countergambit, Milner-Barry Variation" -> "King's Gambit Declined: Falkbeer Countergambit, Milner-Barry Variation"

### `C.KGm.Dec.Fal.exd5.Bc5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Bc5 Line|King's Gambit Declined: Falkbeer Countergambit, Miles Gambit" -> "King's Gambit Declined: Falkbeer Countergambit, Miles Gambit"

### `C.KGm.Dec.Fal.exd5.exf4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "exf4 Line|King's Gambit Declined: Falkbeer Countergambit, Modern Transfer" -> "King's Gambit Declined: Falkbeer Countergambit, Modern Transfer"

### `C.KGm.Dec.Fal.exd5.c6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "c6 Line|King's Gambit Declined: Falkbeer Countergambit, Nimzowitsch-Marshall Countergambit" -> "King's Gambit Declined: Falkbeer Countergambit, Nimzowitsch-Marshall Countergambit"

### `C.KGm.Dec.Fal.exd5.c6.dxc6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'dxc6 Line' -> ''

### `C.KGm.Dec.Fal.Nc3.dxe4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'dxe4 Line' -> ''

### `C.KGm.Dec.Fal.Nc3.dxe4.Nxe4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nxe4 Line|Van Geet Opening: Grünfeld Defense, Steiner Gambit' -> 'Van Geet Opening: Grünfeld Defense, Steiner Gambit'

### `B.Fre.Mac.MLn.exf6.hxg5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'hxg5 Line' -> ''

### `B.Fre.Mac.MLn.Bd2.Bxc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bxc3 Line|French Defense: McCutcheon Variation, Lasker Variation' -> 'French Defense: McCutcheon Variation, Lasker Variation'

### `D.Alb.Nrm.Nbd2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Nbd2 Line|Queen's Gambit Declined: Albin Countergambit, Modern Line" -> "Queen's Gambit Declined: Albin Countergambit, Modern Line"

### `D.Alb.Nrm.Nbd2.Qe7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Qe7 Line|Queen's Gambit Declined: Albin Countergambit, Balogh Variation" -> "Queen's Gambit Declined: Albin Countergambit, Balogh Variation"

### `D.Alb.Nrm.Nbd2.f6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "f6 Line|Queen's Gambit Declined: Albin Countergambit, Janowski Variation" -> "Queen's Gambit Declined: Albin Countergambit, Janowski Variation"

### `D.Alb.Nrm.Nbd2.Bg4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bg4 Line' -> ''

### `D.Alb.Nrm.Nbd2.Bg4.h3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'h3 Line' -> ''

### `D.Alb.Nrm.Nbd2.Bg4.h3.Bxf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bxf3 Line' -> ''

### `D.Alb.Nrm.g3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "g3 Line|Queen's Gambit Declined: Albin Countergambit, Fianchetto Variation" -> "Queen's Gambit Declined: Albin Countergambit, Fianchetto Variation"

### `D.Alb.Nrm.g3.Be6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Be6 Line|Queen's Gambit Declined: Albin Countergambit, Fianchetto Variation, Be6 Line" -> "Queen's Gambit Declined: Albin Countergambit, Fianchetto Variation, Be6 Line"

### `D.Alb.Nrm.g3.Bf5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Bf5 Line|Queen's Gambit Declined: Albin Countergambit, Fianchetto Variation, Bf5 Line" -> "Queen's Gambit Declined: Albin Countergambit, Fianchetto Variation, Bf5 Line"

### `D.Alb.Nrm.g3.Bg4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Bg4 Line|Queen's Gambit Declined: Albin Countergambit, Fianchetto Variation, Bg4 Line" -> "Queen's Gambit Declined: Albin Countergambit, Fianchetto Variation, Bg4 Line"

### `E.QID.Pet.KPe.d5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "d5 Line|Queen's Indian Defense: Kasparov-Petrosian Variation, Main Line" -> "Queen's Indian Defense: Kasparov-Petrosian Variation, Main Line"

### `E.QID.Pet.KPe.d5.cxd5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'cxd5 Line' -> ''

### `D.Sem.e3.Nbd7.Bd3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bd3 Line' -> ''

### `D.Sem.e3.Nbd7.Bd3.Bd6.Qc2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qc2 Line' -> ''

### `D.Sem.e3.Nbd7.b3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'b3 Line' -> ''

### `D.Sem.e3.Nbd7.b3.Bd6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bd6 Line' -> ''

### `D.Sem.e3.Nbd7.b3.Bd6.Bb2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bb2 Line' -> ''

### `D.Sem.e3.Ne4.Bd3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bd3 Line' -> ''

### `D.Sem.e3.Ne4.Bd3.f5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'f5 Line' -> ''

### `D.Sem.e3.Bd6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bd6 Line' -> ''

### `D.Sem.e3.Bd6.Bd3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bd3 Line' -> ''

### `D.Sem.e3.Bd6.Bd3.dxc4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'dxc4 Line' -> ''

### `D.Sem.e3.Bd6.Bd3.dxc4.Bxc4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bxc4 Line' -> ''

### `A.KIA.Bg2.c6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c6 Line' -> ''

### `A.KIA.Bg2.c6.O-O.Bf5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bf5 Line' -> ''

### `A.KIA.Bg2.c6.O-O.Bf5.d3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd3 Line' -> ''

### `A.KIA.Bg2.e6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e6 Line' -> ''

### `C.KPO.Kgt.Qe7.Bc4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bc4 Line' -> ''

### `C.KPO.Kgt.Bc5.Nxe5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nxe5 Line' -> ''

### `C.KPO.Kgt.Qf6.Bc4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bc4 Line' -> ''

### `C.LtO.Gre.d4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `C.LtO.Gre.d4.d6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd6 Line' -> ''

### `C.LtO.Gre.Nc4.fxe4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'fxe4 Line' -> ''

### `C.Sco.Gbt.Bb4.c3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c3 Line' -> ''

### `C.Sco.Gbt.Bb4.c3.dxc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'dxc3 Line' -> ''

### `C.Sco.Gbt.Bc5.Ng5.Nh6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nh6 Line' -> ''

### `D.Sla.Not.a4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'a4 Line' -> ''

### `D.Sla.Not.a4.Bb4.e3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e3 Line' -> ''

### `D.QGD.Cmb.Nd2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nd2 Line' -> ''

### `D.QGD.Cmb.Nd2.Bb4.Qc2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qc2 Line' -> ''

### `D.QGD.Cmb.cxd5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'cxd5 Line' -> ''

### `D.QGD.Cmb.cxd5.exd5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'exd5 Line' -> ''

### `A.Bir.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf6 Line' -> ''

### `A.Bir.Nf6.Nf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf3 Line' -> ''

### `A.Bir.Nf6.Nf3.g6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'g6 Line' -> ''

### `A.Bir.f5.d4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd4 Line' -> ''

### `A.Bir.f5.e4.fxe4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'fxe4 Line' -> ''

### `A.Bir.f5.e4.fxe4.Nc3.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf6 Line' -> ''

### `A.Bir.h6.Nf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf3 Line' -> ''

### `A.Kad.c5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c5 Line' -> ''

### `A.Kad.d5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd5 Line' -> ''

### `A.Kad.d5.d4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd4 Line' -> ''

### `A.Kad.d5.d4.c5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c5 Line' -> ''

### `A.Kad.d5.d4.c5.Nf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf3 Line' -> ''

### `A.Kad.d5.d4.c5.Nf3.cxd4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'cxd4 Line' -> ''

### `A.Kad.e5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e5 Line' -> ''

### `A.Kad.e5.d4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd4 Line' -> ''

### `A.Kad.e5.d4.exd4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'exd4 Line' -> ''

### `A.Kad.f5.e4.fxe4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'fxe4 Line' -> ''

### `A.Kad.f5.e4.fxe4.d3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd3 Line' -> ''

### `A.War.e5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e5 Line' -> ''

### `A.War.b6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'b6 Line' -> ''

### `A.War.b6.d4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd4 Line' -> ''

### `A.War.b6.d4.d5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd5 Line' -> ''

### `A.War.b6.d4.d5.Nc3.Nd7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nd7 Line' -> ''

### `A.War.b5.axb5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'axb5 Line' -> ''

### `A.War.b5.axb5.Bb7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bb7 Line' -> ''

### `A.Hng.ReM.Nf3.Nc6.d4.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf6 Line' -> ''

### `A.Hng.ReM.Nf3.Nc6.d4.e6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e6 Line' -> ''

### `A.Hng.ReM.Nf3.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf6 Line' -> ''

### `A.Hng.ReM.Nf3.Nf6.O-O.e6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e6 Line' -> ''

### `A.QPO.g6.Nf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf3 Line' -> ''

### `A.QPO.g6.Nf3.Bg7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bg7 Line' -> ''

### `A.QPO.g6.Nf3.Bg7.e3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e3 Line' -> ''

### `A.QPO.g6.Nf3.Bg7.Nc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc3 Line' -> ''

### `B.Sca.MLn.Qd6.d4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd4 Line' -> ''

### `B.Sca.MLn.Qd6.d4.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf6 Line' -> ''

### `B.Sca.MLn.Qd8.d4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd4 Line' -> ''

### `B.Sca.MLn.Qd8.d4.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf6 Line' -> ''

### `B.Sca.MLn.Qd8.d4.Nf6.Nf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf3 Line' -> ''

### `B.CaK.Kar.Ng5.Ngf6.Bd3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bd3 Line' -> ''

### `B.CaK.Kar.Ng5.Ngf6.Bd3.e6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e6 Line' -> ''

### `B.CaK.Kar.Bc4.Ngf6.Ng5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Ng5 Line' -> ''

### `B.CaK.Kar.Bc4.Ngf6.Ng5.e6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e6 Line' -> ''

### `B.CaK.Kar.Bc4.Ngf6.Nxf6.Nxf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nxf6 Line' -> ''

### `C.Bsh.Ber.d4.exd4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'exd4 Line' -> ''

### `C.Bsh.Ber.Ne2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Ne2 Line' -> ''

### `C.Bsh.Ber.f3.Bc5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bc5 Line' -> ''

### `C.Bsh.Ber.f3.Bc5.Ne2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Ne2 Line' -> ''

### `C.Bsh.Ber.f3.Bc5.Ne2.Nc6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc6 Line' -> ''

### `C.Pet.Mod.exd4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "exd4 Line|Petrov's Defense: Modern Attack" -> "Petrov's Defense: Modern Attack"

### `C.Pet.Mod.Nxe4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nxe4 Line' -> ''

### `C.Pet.Mod.Nxe4.Bd3.d5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd5 Line' -> ''

### `C.Pon.Jae.d3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd3 Line|Ponziani Opening: Jaenisch Counterattack' -> 'Ponziani Opening: Jaenisch Counterattack'

### `C.Pon.Jae.d3.d5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd5 Line|Ponziani Opening: Jaenisch Counterattack' -> 'Ponziani Opening: Jaenisch Counterattack'

### `C.Pon.Jae.d3.d5.Nbd2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nbd2 Line|Ponziani Opening: Jaenisch Counterattack' -> 'Ponziani Opening: Jaenisch Counterattack'

### `C.Pon.Jae.d4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd4 Line' -> ''

### `C.Pon.Jae.d4.Nxe4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nxe4 Line' -> ''

### `C.Pon.Jae.d4.Nxe4.d5.Bc5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bc5 Line' -> ''

### `C.Fou.Sco.exd4.Nxd4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nxd4 Line' -> ''

### `C.Fou.Sco.Bb4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bb4 Line' -> ''

### `C.Fou.Sco.Bb4.d5.Nd4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nd4 Line' -> ''

### `A.Bar.e5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e5 Line' -> ''

### `A.Bar.d5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd5 Line' -> ''

### `A.Bar.d5.e4.g6.d4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd4 Line' -> ''

### `A.Bar.d5.e4.g6.d4.dxe4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'dxe4 Line' -> ''

### `A.Bar.f5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'f5 Line' -> ''

### `A.Bar.f5.e4.fxe4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'fxe4 Line' -> ''

### `A.Bar.f5.e4.fxe4.Nc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc3 Line' -> ''

### `A.Gro.Gbt.c6.c4.dxc4.b3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'b3 Line' -> ''

### `A.Gro.Gbt.e5.d4.exd4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'exd4 Line' -> ''

### `A.Gro.Gbt.e5.d4.exd4.c3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c3 Line' -> ''

### `A.Pol.Cen.Bb2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bb2 Line' -> ''

### `A.Pol.Cen.Bb2.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf6 Line' -> ''

### `A.Pol.Cen.Bb2.c6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c6 Line' -> ''

### `A.VtK.e5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e5 Line' -> ''

### `A.VtK.e5.Bc4.b5.Bb3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bb3 Line' -> ''

### `A.VtK.e5.Nc3.Nf6.f4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'f4 Line' -> ''

### `A.VtK.e5.Nc3.Nf6.f4.exf4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'exf4 Line' -> ''

### `A.VtK.e5.Nc3.Nc6.f4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'f4 Line' -> ''

### `A.VtK.e5.Nc3.d5.f4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'f4 Line' -> ''

### `A.Mod.Nc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc3 Line|Modern Defense, Nc3' -> 'Modern Defense, Nc3'

### `A.Mod.Nc3.c5.d5.Bxc3.bxc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'bxc3 Line' -> ''

### `E.Ben.Old.c4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c4 Line' -> ''

### `E.Ben.Old.c4.cxd4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'cxd4 Line' -> ''

### `B.Pir.Pre.f4.d5.exd5.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf6 Line|Rat Defense: Fuller Gambit' -> 'Rat Defense: Fuller Gambit'

### `B.Sca.Nf6.d4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd4 Line|Scandinavian Defense: Modern Variation' -> 'Scandinavian Defense: Modern Variation'

### `B.Sca.Nf6.d4.g6.c4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c4 Line' -> ''

### `B.Sca.Nf6.d4.c6.dxc6.e5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e5 Line' -> ''

### `D.QPG.Chi.e6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e6 Line' -> ''

### `D.QGD.Exc.Bg5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bg5 Line' -> ''

### `D.QGD.Exc.Bg5.Be7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be7 Line' -> ''

### `D.QGD.Exc.Bg5.Be7.e3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e3 Line' -> ''

### `D.QGD.Lsk.Bxe7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bxe7 Line' -> ''

### `D.QGD.Lsk.Bxe7.Qxe7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qxe7 Line' -> ''

### `D.QGD.Lsk.Bxe7.Qxe7.cxd5.Nxc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nxc3 Line' -> ''

### `E.Nim.Kas.c5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c5 Line' -> ''

### `E.Nim.Kas.c5.g3.cxd4.Nxd4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nxd4 Line' -> ''

### `E.Nim.Kas.b6.e3.Ne4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Ne4 Line' -> ''

### `E.Nim.Kas.b6.e3.Ne4.Qc2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qc2 Line|Nimzo-Indian Defense: St. Petersburg Variation' -> 'Nimzo-Indian Defense: St. Petersburg Variation'

### `E.Nim.Cls.Noa.Ne4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Ne4 Line|Nimzo-Indian Defense: Classical Variation, Noa Variation, Main Line' -> 'Nimzo-Indian Defense: Classical Variation, Noa Variation, Main Line'

### `E.Nim.Cls.Noa.Ne4.Qc2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qc2 Line|Nimzo-Indian Defense: Classical Variation, Noa Variation' -> 'Nimzo-Indian Defense: Classical Variation, Noa Variation'

### `E.Nim.Rub.Cls.Nf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf3 Line' -> ''

### `E.Nim.Rub.Cls.a3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'a3 Line' -> ''

### `E.Nim.Rub.Cls.a3.Bxc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bxc3 Line' -> ''

### `E.Nim.Rub.Cls.a3.Bxc3.bxc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'bxc3 Line|Nimzo-Indian Defense: Normal Variation, Botvinnik System' -> 'Nimzo-Indian Defense: Normal Variation, Botvinnik System'

### `A.Ret.Adv.b4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'b4 Line' -> ''

### `A.Ret.Adv.e3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e3 Line' -> ''

### `A.Eng.Mik.Nc6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc6 Line' -> ''

### `A.Eng.Mik.d5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd5 Line' -> ''

### `A.Eng.Mik.d5.e5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e5 Line' -> ''

### `A.Eng.Mik.c5.e5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e5 Line' -> ''

### `A.OID.Nf6.Nc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc3 Line' -> ''

### `A.OID.Nf6.Nf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf3 Line' -> ''

### `A.Hol.Alp.e6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e6 Line' -> ''

### `A.Hol.Alp.g6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'g6 Line' -> ''

### `A.Hol.Alp.d6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd6 Line' -> ''

### `A.Hol.Alp.d5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd5 Line' -> ''

### `A.Hol.Sta.MLn.g6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'g6 Line' -> ''

### `B.CaK.Two.dxe4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'dxe4 Line' -> ''

### `B.CaK.Two.Bg4.h3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'h3 Line' -> ''

### `B.CaK.Pmv.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf6 Line' -> ''

### `B.CaK.Pmv.Nf6.Nc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc3 Line' -> ''

### `B.CaK.Pmv.Nf6.Nc3.e6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e6 Line' -> ''

### `B.CaK.Pmv.Nf6.Nc3.e6.Nf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `B.CaK.Cls.Ng3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Ng3 Line' -> ''

### `B.CaK.Cls.Ng3.Bg6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bg6 Line' -> ''

### `B.CaK.Cls.Ng3.Bg6.h4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'h4 Line' -> ''

### `B.CaK.Cls.Ng5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Ng5 Line' -> ''

### `B.CaK.Cls.Ng5.Bg6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bg6 Line' -> ''

### `B.CaK.Cls.Ng5.Bg6.N1f3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf3 Line' -> ''

### `C.Sco.Cls.Nxc6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nxc6 Line' -> ''

### `C.Sco.Cls.Be3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be3 Line' -> ''

### `C.Sco.Cls.Be3.Qf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qf6 Line' -> ''

### `D.Sla.Cze.Kra.MLn.Nbd7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nbd7 Line' -> ''

### `D.Sla.Cze.Kra.MLn.Nbd7.Nxc4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nxc4 Line' -> ''

### `A.Eng.Agi.Nf3.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf6 Line|Agincourt Defense Nf3, Nf6' -> 'Agincourt Defense Nf3, Nf6'

### `A.Eng.Agi.Nf3.Nf6.g3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'g3 Line' -> ''

### `A.Eng.Agi.Nf3.Nf6.Nc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc3 Line' -> ''

### `A.Ret.Ang.MLn.Nf6.Nc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc3 Line' -> ''

### `A.Ret.Ang.MLn.Nf6.Nc3.Nbd7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nbd7 Line' -> ''

### `A.Ret.Ang.MLn.Nf6.Nc3.e6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e6 Line' -> ''

### `B.Sca.Mod.Mie.e5.dxe5.Nc6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc6 Line' -> ''

### `B.Sca.Mod.Mie.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf6 Line' -> ''

### `B.CaK.Pmv.Nc6.Bg5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bg5 Line' -> ''

### `B.CaK.Pmv.Nc6.Bg5.dxc4.d5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd5 Line' -> ''

### `B.Sic.Acc.Mar.Bg7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bg7 Line|Sicilian Defense: Accelerated Dragon, Maróczy Bind' -> 'Sicilian Defense: Accelerated Dragon, Maróczy Bind'

### `B.Sic.Acc.Mar.Bg7.Be3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be3 Line|Sicilian Defense: Accelerated Dragon, Maróczy Bind' -> 'Sicilian Defense: Accelerated Dragon, Maróczy Bind'

### `B.Sic.Acc.Mar.Bg7.Be3.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf6 Line' -> ''

### `B.Sic.Acc.Mar.Bg7.Nc2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc2 Line' -> ''

### `B.Sic.Naj.Eng.e6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e6 Line' -> ''

### `B.Sic.Naj.Eng.e6.Qd2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qd2 Line|Sicilian Defense: Scheveningen Variation, English Attack, with Qd2' -> 'Sicilian Defense: Scheveningen Variation, English Attack, with Qd2'

### `B.Fre.Tar.Cls.MLn.Bd3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bd3 Line' -> ''

### `B.Fre.Tar.Cls.MLn.Bd3.c5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c5 Line' -> ''

### `C.Vie.Fal.MLn.Qh5.Nd6.Bb3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bb3 Line' -> ''

### `C.Sco.Cls.Sch.Qd2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qd2 Line|Scotch Game: Classical Variation, Blackburne Attack' -> 'Scotch Game: Classical Variation, Blackburne Attack'

### `C.RyL.Shl.Jae.fxe4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'fxe4 Line' -> ''

### `C.RyL.Shl.Jae.fxe4.Nxe4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nxe4 Line' -> ''

### `C.RyL.Shl.Jae.fxe4.Nxe4.d5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd5 Line' -> ''

### `D.QPG.Ver.Nbd7.Nf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf3 Line' -> ''

### `D.QPG.Ver.c5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c5 Line' -> ''

### `D.QPG.Ver.c5.Bxf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bxf6 Line' -> ''

### `E.QID.Euw.Bd3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bd3 Line' -> ''

### `E.QID.Euw.Bd3.c5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "c5 Line|Queen's Indian Defense: Spassky System3" -> "Queen's Indian Defense: Spassky System3"

### `E.KID.Fch.Kav.Nc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc3 Line' -> ''

### `E.KID.Fou.O-O.Be2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be2 Line' -> ''

### `E.KID.Fou.O-O.Be2.c5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c5 Line' -> ''

### `E.KID.Fou.O-O.Nf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf3 Line' -> ''

### `E.Ben.Mod.Cls.MLn.a6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'a6 Line' -> ''

### `E.Ben.Mod.Cls.MLn.a6.a4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'a4 Line|Benoni Defense: Classical Variation, Full Line' -> 'Benoni Defense: Classical Variation, Full Line'

### `C.KGm.Dec.Cls.c3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c3 Line' -> ''

### `C.KGm.Acc.All.MLn.Nxf7.Kxf7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Kxf7 Line' -> ''

### `C.KGm.Acc.Kie.MLn.Bc4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bc4 Line' -> ''

### `C.Ita.Giu.Mol.MLn.Nxe4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nxe4 Line' -> ''

### `C.Ita.Evn.Acc.Stn.d4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd4 Line' -> ''

### `C.Ita.Evn.Acc.Stn.O-O.d6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd6 Line|Italian Game: Evans Gambit' -> 'Italian Game: Evans Gambit'

### `C.Ita.Pia.Nf6.MLn.a6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'a6 Line' -> ''

### `C.Ita.Pia.Nf6.MLn.a6.a4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'a4 Line' -> ''

### `C.Ita.Pia.Nf6.MLn.h6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'h6 Line' -> ''

### `C.Ita.Pia.Nf6.MLn.h6.Nbd2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nbd2 Line' -> ''

### `A.Hor.Fch.Nf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf3 Line' -> ''

### `A.Hor.Fch.Nf3.c5.cxd5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'cxd5 Line' -> ''

### `A.Hor.Fch.Nc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc3 Line' -> ''

### `E.Ben.Bnk.Acc.MLn.g6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'g6 Line' -> ''

### `E.Ben.Bnk.Acc.MLn.g6.Nc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc3 Line' -> ''

### `E.Ben.Bnk.Acc.MLn.Bxa6.Nc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc3 Line' -> ''

### `B.Fre.Cls.MLn.ACh.Bxg5.hxg5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'hxg5 Line' -> ''

### `C.KGm.Acc.Bsh.Ble.Nc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc3 Line' -> ''

### `C.KGm.Acc.Bsh.Ble.Nc3.Bg7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bg7 Line' -> ''

### `C.Fou.Spa.Rub.Be2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be2 Line|Four Knights Game: Spanish Variation, Rubinstein Variation' -> 'Four Knights Game: Spanish Variation, Rubinstein Variation'

### `C.Fou.Spa.Rub.Nxe5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nxe5 Line' -> ''

### `C.Fou.Spa.Rub.Nxe5.Qe7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qe7 Line' -> ''

### `C.RyL.Ber.Rio.Qe2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qe2 Line' -> ''

### `C.RyL.Ber.Rio.Qe2.Nd6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nd6 Line' -> ''

### `C.RyL.Ber.Rio.Qe2.Nd6.Bxc6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bxc6 Line' -> ''

### `D.QGD.Har.MLn.c5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c5 Line' -> ''

### `D.QGD.Har.MLn.c5.dxc5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'dxc5 Line' -> ''

### `E.Nim.Rub.StP.MLn.Nf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf3 Line|Nimzo-Indian Defense: St. Petersburg Variation' -> 'Nimzo-Indian Defense: St. Petersburg Variation'

### `E.Nim.Rub.StP.MLn.Nf3.Ne4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Ne4 Line|Nimzo-Indian Defense: St. Petersburg Variation, with Ne4' -> 'Nimzo-Indian Defense: St. Petersburg Variation, with Ne4'

### `C.Ita.Two.Opn.MLn.e5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e5 Line' -> ''

### `C.RyL.Mar.MLn.Rxe5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Rxe5 Line' -> ''

### `C.RyL.Mar.MLn.Rxe5.c6.d4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `C.RyL.Cha.MLn.d4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd4 Line' -> ''

### `C.RyL.Cha.MLn.d4.Nc6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc6 Line|Ruy López: Closed, Borisenko Variation' -> 'Ruy López: Closed, Borisenko Variation'

### `C.RyL.Cha.MLn.d4.Qc7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qc7 Line|Ruy López: Closed, Chigorin Defense' -> 'Ruy López: Closed, Chigorin Defense'

### `C.RyL.Cha.MLn.d4.Qc7.Nbd2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nbd2 Line' -> ''

### `D.Sem.Bg5.Bot.MLn.g5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'g5 Line' -> ''

### `D.Sem.Bg5.Bot.MLn.g5.Nxg5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nxg5 Line' -> ''

### `D.Cat.Cls.Qc2.c6.Nbd2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nbd2 Line' -> ''

### `D.Cat.Cls.Qc2.c6.Bf4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bf4 Line' -> ''

### `D.Cat.Cls.Qc2.c6.Bf4.b6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'b6 Line' -> ''

### `E.QID.Kas.Bb7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bb7 Line' -> ''

### `E.QID.Kas.Bb7.Bg5.h6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'h6 Line' -> ''

### `E.QID.Kas.Bb7.Bg5.h6.Bh4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bh4 Line' -> ''

### `E.QID.Pet.Ba6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Ba6 Line' -> ''

### `E.QID.Pet.Ba6.Qc2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qc2 Line' -> ''

### `E.QID.Sps.Bb7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Bb7 Line|Queen's Indian Defense: Spassky System" -> "Queen's Indian Defense: Spassky System"

### `E.QID.Euw.Bd3.c5.Nc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc3 Line' -> ''

### `E.QID.Euw.Bd3.c5.Nc3.cxd4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'cxd4 Line' -> ''

### `E.QID.Euw.Bd3.c5.O-O.g6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'g6 Line' -> ''

### `E.QID.Mod.Sms.d5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd5 Line' -> ''

### `E.QID.Mod.Sms.d5.exd5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'exd5 Line' -> ''

### `E.Ind.Cat.d5.Bg2.dxc4.Qa4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qa4+ Line' -> ''

### `E.Ind.Cat.d5.Bg2.dxc4.Nf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf3 Line' -> ''

### `A.Eng.AIn.Nc3.d5.cxd5.Nf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf3 Line|English Opening: Anglo-Indian Defense, Anglo-Grünfeld Variation' -> 'English Opening: Anglo-Indian Defense, Anglo-Grünfeld Variation'

### `A.Eng.AIn.Nc3.d5.cxd5.g3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'g3 Line' -> ''

### `A.Ret.Ang.g3.Nf6.b3.g6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'g6 Line' -> ''

### `A.Ret.Ang.g3.Nf6.b3.dxc4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'dxc4 Line' -> ''

### `A.EID.Bf4.Bg7.e3.d6.Bd3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bd3 Line' -> ''

### `A.EID.Bf4.Bg7.e3.d6.Be2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be2 Line' -> ''

### `A.EID.Bf4.Bg7.e3.d6.h3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'h3 Line' -> ''

### `A.Eng.Rev.a3.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf6 Line' -> ''

### `A.Eng.Rev.a3.d6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd6 Line' -> ''

### `A.Eng.Rev.d3.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf6 Line' -> ''

### `A.Eng.Rev.d3.Nf6.a3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'a3 Line|Reversed Najdorf' -> 'Reversed Najdorf'

### `A.Eng.Rev.d3.d6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd6 Line' -> ''

### `A.Eng.Rev.d3.d6.a3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'a3 Line|Reversed Najdorf' -> 'Reversed Najdorf'

### `A.Lar.Mod.e3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e3 Line|Nimzo-Larsen Attack: Modern Variation' -> 'Nimzo-Larsen Attack: Modern Variation'

### `A.Lar.Mod.e3.d5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd5 Line' -> ''

### `A.Lar.Mod.e3.d5.Bb5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bb5 Line' -> ''

### `B.Fre.Stn.MLn.f4.c5.dxc5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'dxc5 Line' -> ''

### `B.Fre.Stn.MLn.f4.c5.Nf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf3 Line|Boleslavsky Prefix' -> 'Boleslavsky Prefix'

### `C.Fou.Spa.Dbl.MLn.d3.Bxc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bxc3 Line|Janowski Prefix|Svenonius Prefix' -> 'Janowski Prefix|Svenonius Prefix'

### `C.Fou.Spa.Dbl.MLn.d3.Qe7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qe7 Line|Alatortsev Prefix' -> 'Alatortsev Prefix'

### `C.Ita.Two.Max.MLn.exf6.dxc4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'dxc4 Line|Accepted Prefix' -> 'Accepted Prefix'

### `C.RyL.Ber.d3.d6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd6 Line|Improved Steinitz Prefix' -> 'Improved Steinitz Prefix'

### `C.RyL.Ber.d3.Bc5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bc5 Line|Kaufmann Prefix' -> 'Kaufmann Prefix'

### `C.RyL.Ber.d3.Ne7.Nxe5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nxe5 Line|Mortimer Trap Prefix' -> 'Mortimer Trap Prefix'

### `A.Van.d5.f4.d4.Ne4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Ne4 Line' -> ''

### `B.Sic.HAc.d4.Bg7.dxc5.Nc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc3 Line|Pteranodon Prefix|Pterodactyl Defense: Sicilian, Rhamphorhynchus' -> 'Pteranodon Prefix|Pterodactyl Defense: Sicilian, Rhamphorhynchus'

### `B.Sic.Old.d4.cxd4.Nxd4.a6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "a6 Line|O'Kelly Maróczy Prefix" -> "O'Kelly Maróczy Prefix"

### `B.Sic.Old.d4.cxd4.Nxd4.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf6 Line' -> ''

### `A.Sod.e5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e5 Line|Celadon Prefix|Durkin Gambit Prefix' -> 'Celadon Prefix|Durkin Gambit Prefix'

### `A.Owe.Eng.e4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e4 Line|English Defense, e4' -> 'English Defense, e4'

### `A.Owe.Eng.e4.Bb7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bb7 Line|English Defense e4, Bb7' -> 'English Defense e4, Bb7'

### `A.OID.e5.dxe5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'dxe5 Line' -> ''

### `A.QPO.Nf6.f3.d5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd5 Line' -> ''

### `A.Tro.Rap.Bh4.c6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c6 Line|Hergert Prefix' -> 'Hergert Prefix'

### `A.Tro.Rap.Bh4.d5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd5 Line|Hergert Prefix' -> 'Hergert Prefix'

### `A.Hol.Fch.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf6 Line|Blackburne Prefix' -> 'Blackburne Prefix'

### `B.Ale.Chs.Nd5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nd5 Line' -> ''

### `B.Ale.Fou.Bf5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bf5 Line|Trifunovic Prefix' -> 'Trifunovic Prefix'

### `B.Pir.Be2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be2 Line|Bayonet Prefix|Chinese Prefix|Pirc Defense, Be2' -> 'Bayonet Prefix|Chinese Prefix|Pirc Defense, Be2'

### `B.CaK.Exc.Bf4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bf4 Line' -> ''

### `B.CaK.Exc.Bd3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bd3 Line|Rubinstein Prefix' -> 'Rubinstein Prefix'

### `B.CaK.Exc.Bd3.Nc6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc6 Line' -> ''

### `B.CaK.Exc.Bd3.Nc6.c3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c3 Line' -> ''

### `B.Sic.Alp.Cen.MLn.cxd4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'cxd4 Line|Barmen Prefix' -> 'Barmen Prefix'

### `B.Sic.Alp.Cen.MLn.Nc6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc6 Line|Milner-Barry Prefix' -> 'Milner-Barry Prefix'

### `B.Sic.Clo.Fch.g6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'g6 Line' -> ''

### `B.Sic.Clo.Fch.g6.Bg2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bg2 Line' -> ''

### `C.Vie.Cls.Bc5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bc5 Line|Spielmann Prefix|Eifel Prefix' -> 'Spielmann Prefix|Eifel Prefix'

### `C.PhD.d4.exd4.Nxd4.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf6 Line' -> ''

### `C.PhD.Lio.Ng5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Ng5 Line|Nimzowitsch Prefix' -> 'Nimzowitsch Prefix'

### `C.PhD.Lio.Ng5.O-O` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'O-O Line' -> ''

### `C.PhD.d4.f5.dxe5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'dxe5 Line' -> ''

### `C.PhD.d4.f5.dxe5.fxe4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'fxe4 Line' -> ''

### `C.Pet.Mod.Stn.Qe2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Qe2 Line|Steinitz Variation|Petrov's Defense: Modern Attack, Steinitz Variation" -> "Steinitz Variation|Petrov's Defense: Modern Attack, Steinitz Variation"

### `C.Pet.Mod.Stn.Qe2.Nc5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc5 Line|Bardeleben Prefix' -> 'Bardeleben Prefix'

### `C.Sco.exd4.Nxd4.Qh4.Nb5.Bb4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bb4 Line|Blackburne Prefix|Rosenthal Prefix' -> 'Blackburne Prefix|Rosenthal Prefix'

### `C.Sco.Mie.Nxc6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nxc6 Line|Mieses Prefix|Tartakower Prefix' -> 'Mieses Prefix|Tartakower Prefix'

### `C.Sco.Mie.Nxc6.bxc6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'bxc6 Line' -> ''

### `C.Ita.Giu.O-O.Nf6.d3.h6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'h6 Line' -> ''

### `C.Ita.Giu.O-O.Nf6.d3.a5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'a5 Line' -> ''

### `C.Ita.Two.Ng5.Nb4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nb4 Line' -> ''

### `D.Bgm.Acc.Bog.MLn.O-O` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'O-O Line' -> ''

### `A.Col.Bd6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bd6 Line|Rubinstein Semi-Slav Prefix' -> 'Rubinstein Semi-Slav Prefix'

### `D.QPG.c4.c5.dxc5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'dxc5 Line|Salvio Prefix' -> 'Salvio Prefix'

### `D.QPG.c4.c5.cxd5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'cxd5 Line|Gusev Prefix' -> 'Gusev Prefix'

### `D.Sla.Qui.cxd5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'cxd5 Line|Schallopp Exchange Prefix' -> 'Schallopp Exchange Prefix'

### `D.Sla.Qui.cxd5.cxd5.Nc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc3 Line|Exchange Schallopp Prefix|Amsterdam Prefix' -> 'Exchange Schallopp Prefix|Amsterdam Prefix'

### `D.QGA.Old.MLn.Qb3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qb3 Line|Billinger Prefix|Christensen Prefix|Korchnoi Prefix|Novikov Prefix' -> 'Billinger Prefix|Christensen Prefix|Korchnoi Prefix|Novikov Prefix'

### `D.QGA.Old.MLn.Qb3.Qe7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qe7 Line' -> ''

### `D.Sem.Mer.Bd3.Bb7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bb7 Line|Wade Prefix' -> 'Wade Prefix'

### `D.QGD.Ort.Te7.a6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'a6 Line' -> ''

### `D.QGD.Ort.Te7.Ne4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Ne4 Line' -> ''

### `D.QGD.Ort.Te7.a6.cxd5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'cxd5 Line' -> ''

### `E.Nim.Spl.Rom.Nf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf3 Line|Carlsbad Prefix|Stahlberg Prefix' -> 'Carlsbad Prefix|Stahlberg Prefix'

### `E.Nim.Spl.Rom.Nf3.Ne4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Ne4 Line' -> ''

### `E.Nim.Spl.Rom.Nf3.Ne4.Bd2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bd2 Line|Carlsbad Prefix|Stahlberg Prefix' -> 'Carlsbad Prefix|Stahlberg Prefix'

### `E.Nim.Rub.StP.Ne2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Ne2 Line|American Prefix|Romanishin-Psakhis Prefix|Nimzo-Indian Defense: St. Petersburg Variation' -> 'American Prefix|Romanishin-Psakhis Prefix|Nimzo-Indian Defense: St. Petersburg Variation'

### `E.Nim.Rub.StP.Ne2.c5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c5 Line|Romanishin-Psakhis Prefix' -> 'Romanishin-Psakhis Prefix'

### `E.KID.Sml.Ort.d5.c6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "c6 Line|Closed Variation|King's Indian Defense: Sämisch Variation, Closed Variation" -> "Closed Variation|King's Indian Defense: Sämisch Variation, Closed Variation"

### `E.KID.Sml.Ort.d5.Nh5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nh5 Line|Bronstein Prefix' -> 'Bronstein Prefix'

### `C.Ita.Two.Ng5.d5.exd5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'exd5 Line' -> ''

### `C.Cen.exd4.f4.Bc5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bc5 Line' -> ''

### `C.Cen.exd4.f4.Bc5.Nf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf3 Line' -> ''

### `C.Sco.Gor.Dbl.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf6 Line' -> ''

### `C.Sco.Gor.Dbl.Nf6.Nxc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nxc3 Line' -> ''

### `C.Vie.Mie.Bc5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bc5 Line' -> ''

### `C.Vie.Mie.Bc5.Bg2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bg2 Line' -> ''

### `C.Vie.Mie.Bc5.Bg2.Nc6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc6 Line' -> ''

### `C.Vie.Nc6.g3.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf6 Line' -> ''

### `C.Vie.Nc6.g3.Nf6.Bg2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bg2 Line' -> ''

### `C.Vie.Cls.Bc5.Nge2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nge2 Line' -> ''

### `C.KGm.Acc.Bsh.b5.Bxb5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bxb5 Line' -> ''

### `C.Ita.Two.d3.Be7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Be7 Line|Italian Game: Two Knights Defense, Modern Bishop's Opening" -> "Italian Game: Two Knights Defense, Modern Bishop's Opening"

### `C.Ita.Two.Ng5.Ulv.Bf1` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bf1 Line' -> ''

### `C.Ita.Two.Ng5.Trx.Nxf7.Bxf2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bxf2 Line' -> ''

### `C.RyL.Mor.Opn.Re1` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Re1 Line' -> ''

### `C.RyL.Mor.Opn.MLn.a4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'a4 Line' -> ''

### `C.RyL.Brk.d4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd4 Line|Ruy López: Closed, Breyer' -> 'Ruy López: Closed, Breyer'

### `C.RyL.Brk.d4.Nbd7.Nbd2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nbd2 Line' -> ''

### `C.RyL.Cha.Bc2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bc2 Line|Ruy López: Closed, Chigorin Defense' -> 'Ruy López: Closed, Chigorin Defense'

### `C.Fou.Sco.Bel.MLn.Qe2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qe2 Line' -> ''

### `E.OldI.Jan.f3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.Ben.Mod.KPL.Be3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be3 Line' -> ''

### `E.Ben.Mod.KPL.Bg5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bg5 Line' -> ''

### `E.Ben.Mod.KPL.Nge2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nge2 Line' -> ''

### `E.Gru.Exc.Cla.Rb1` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Rb1 Line' -> ''

### `E.Gru.Exc.Cla.Rb1.O-O` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'O-O Line' -> ''

### `E.Gru.Exc.Cla.Rb1.O-O.Be2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be2 Line' -> ''

### `E.Ben.e3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e3 Line|Benoni Defense, e3' -> 'Benoni Defense, e3'

### `E.Ben.e3.g6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'g6 Line' -> ''

### `E.Ben.e3.g6.Nc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc3 Line' -> ''

### `E.Ben.e3.g6.Nc3.Bg7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bg7 Line' -> ''

### `E.Bud.Ng4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Ng4 Line|Budapest Defense, Ng4 Line|Indian Defense: Budapest Defense' -> 'Budapest Defense, Ng4 Line|Indian Defense: Budapest Defense'

### `E.Bud.Alk.Nxe5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nxe5 Line' -> ''

### `E.Bud.Alk.Nxe5.f4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'f4 Line' -> ''

### `E.Bud.Rub.Nc6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc6 Line' -> ''

### `E.Bud.Rub.Nc6.Nf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf3 Line' -> ''

### `E.Bud.Adl.Nc6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc6 Line' -> ''

### `E.OldI.Ukr.e3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e3 Line' -> ''

### `E.OldI.Ukr.e3.Nbd7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nbd7 Line' -> ''

### `E.Ind.WIn.f3.c5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c5 Line' -> ''

### `E.Ind.WIn.f3.c5.d5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd5 Line' -> ''

### `E.Ind.WIn.f3.c5.d5.d6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd6 Line' -> ''

### `E.Ind.WIn.g3.Bg7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bg7 Line' -> ''

### `E.Ind.WIn.g3.Bg7.Bg2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bg2 Line' -> ''

### `E.Ind.WIn.Nf3.d5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf3 Line' -> ''

### `E.Gru.Hng.Rc1.c5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c5 Line' -> ''

### `E.Gru.Hng.Rc1.c5.dxc5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'dxc5 Line' -> ''

### `E.Gru.Sml.c5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c5 Line' -> ''

### `E.Gru.Sml.c5.cxd5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'cxd5 Line' -> ''

### `E.Gru.Sml.c5.cxd5.Nxd5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nxd5 Line' -> ''

### `E.Bog.Grn.b6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'b6 Line' -> ''

### `E.Bog.Grn.b6.e3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e3 Line' -> ''

### `E.Bog.Grn.b6.a3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'a3 Line' -> ''

### `E.Bog.Grn.b6.a3.Bxd2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bxd2 Line' -> ''

### `E.Bog.Grn.b6.a3.Bxd2.Qxd2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qxd2 Line' -> ''

### `E.Nim.Sml.Bxc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bxc3 Line' -> ''

### `E.Nim.Sml.Bxc3.bxc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'bxc3 Line' -> ''

### `E.Nim.Sml.Bxc3.bxc3.O-O` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'O-O Line|Nimzo-Indian Defense: Sämisch Variation' -> 'Nimzo-Indian Defense: Sämisch Variation'

### `E.Nim.Sml.Bot.cxd5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'cxd5 Line|Nimzo-Indian Defense: Sämisch Variation' -> 'Nimzo-Indian Defense: Sämisch Variation'

### `E.Nim.Sml.Bot.cxd5.Nxd5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nxd5 Line' -> ''

### `E.Nim.Kas.Bxc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bxc3 Line' -> ''

### `E.Nim.Kas.Bxc3.bxc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'bxc3 Line' -> ''

### `E.Nim.Kas.Bxc3.bxc3.b6.e3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e3 Line' -> ''

### `E.KID.Cls.Pet.Nbd7.Bg5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bg5 Line' -> ''

### `E.KID.Cls.Byn.Nh5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nh5 Line' -> ''

### `E.KID.Mak.O-O` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'O-O Line' -> ''

### `E.KID.Fch.Yug.Nc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc3 Line' -> ''

### `E.Ben.Old.Adv.d6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd6 Line' -> ''

### `E.Ind.Tgo.d5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd5 Line' -> ''

### `E.Ind.Tgo.d5.Ne5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Ne5 Line' -> ''

### `D.Alb.dxe5.d4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd4 Line' -> ''

### `D.QGA.Jan.e3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e3 Line|Alatortsev Prefix' -> 'Alatortsev Prefix'

### `D.QGA.Jan.e3.Bg4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bg4 Line|Alatortsev Prefix' -> 'Alatortsev Prefix'

### `D.QGA.Jan.e3.Bg4.Bxc4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bxc4 Line|Alatortsev Prefix' -> 'Alatortsev Prefix'

### `D.QGA.Cls.Qe2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qe2 Line|Furman Prefix' -> 'Furman Prefix'

### `D.QGA.Cls.Qe2.a6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'a6 Line|Furman Prefix' -> 'Furman Prefix'

### `D.QGA.Cls.Qe2.a6.dxc5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'dxc5 Line|Furman Prefix' -> 'Furman Prefix'

### `D.QGA.Cls.MLn.dxc5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'dxc5 Line|Furman Prefix' -> 'Furman Prefix'

### `D.QGA.Cls.MLn.dxc5.Bxc5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Bxc5 Line|Furman Prefix|Queen's Gambit Accepted: Furman Variation" -> "Furman Prefix|Queen's Gambit Accepted: Furman Variation"

### `D.QGD.Alt.e4.dxe4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'dxe4 Line|Miladinovic Prefix' -> 'Miladinovic Prefix'

### `D.QGD.Exc.Min.h6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'h6 Line|Reshevsky Prefix' -> 'Reshevsky Prefix'

### `D.QGD.Exc.Min.h6.Bh4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bh4 Line' -> ''

### `D.Tar.e3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e3 Line|Symmetrical Prefix|Tarrasch Defense, e3' -> 'Symmetrical Prefix|Tarrasch Defense, e3'

### `D.Tar.e3.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf6 Line|Symmetrical Prefix|Tarrasch Defense e3, Nf6' -> 'Symmetrical Prefix|Tarrasch Defense e3, Nf6'

### `D.Tar.e3.Nf6.Nf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf3 Line|Symmetrical Prefix|Tarrasch Defense e3 Nf6, Nf3' -> 'Symmetrical Prefix|Tarrasch Defense e3 Nf6, Nf3'

### `D.Tar.Exd.dxc5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'dxc5 Line|Tarrasch Gambit Prefix' -> 'Tarrasch Gambit Prefix'

### `D.Tar.Exd.dxc5.d4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd4 Line|Tarrasch Gambit Prefix' -> 'Tarrasch Gambit Prefix'

### `D.Tar.Exd.dxc5.d4.Na4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Na4 Line|Tarrasch Gambit Prefix' -> 'Tarrasch Gambit Prefix'

### `D.Tar.Exd.dxc5.d4.Na4.b5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'b5 Line' -> ''

### `D.Tar.Prg.Bg2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bg2 Line|Wagner Prefix' -> 'Wagner Prefix'

### `D.STa.cxd5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "cxd5 Line|Main Line Prefix|Queen's Gambit Declined: Semi-Tarrasch Defense" -> "Main Line Prefix|Queen's Gambit Declined: Semi-Tarrasch Defense"

### `D.STa.cxd5.Nxd5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nxd5 Line|Main Line Prefix' -> 'Main Line Prefix'

### `D.STa.cxd5.Nxd5.e3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "e3 Line|Main Line Prefix|Queen's Gambit Declined: Semi-Tarrasch Defense, Pillsbury Variation" -> "Main Line Prefix|Queen's Gambit Declined: Semi-Tarrasch Defense, Pillsbury Variation"

### `D.STa.cxd5.Nxd5.e3.Nc6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc6 Line|Main Line Prefix' -> 'Main Line Prefix'

### `D.STa.Sym.Qe2.Qe7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qe7 Line|Levenfish Prefix' -> 'Levenfish Prefix'

### `D.STa.Sym.Qe2.Qe7.dxc5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'dxc5 Line|Levenfish Prefix' -> 'Levenfish Prefix'

### `D.Sem.Bg5.dxc4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'dxc4 Line|Botvinnik Prefix' -> 'Botvinnik Prefix'

### `D.Sem.Bg5.Nbd7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nbd7 Line|D52 Prefix' -> 'D52 Prefix'

### `D.Sem.Bg5.Nbd7.e3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "e3 Line|D52 Prefix|Queen's Gambit Declined" -> "D52 Prefix|Queen's Gambit Declined"

### `D.Sem.Mar.dxe4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'dxe4 Line|Marshall Accepted Prefix' -> 'Marshall Accepted Prefix'

### `D.Sem.Mar.dxe4.Nxe4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nxe4 Line|Marshall Main Prefix' -> 'Marshall Main Prefix'

### `D.Sem.Mar.dxe4.Nxe4.Bb4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bb4 Line|Marshall Main Prefix' -> 'Marshall Main Prefix'

### `D.Sem.Mar.MLn.Qxd4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qxd4 Line|Tolush Prefix' -> 'Tolush Prefix'

### `D.Chi.Exc.e3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e3 Line|Costa Prefix' -> 'Costa Prefix'

### `D.Chi.Exc.e3.e5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e5 Line|Costa Prefix' -> 'Costa Prefix'

### `D.Chi.Exc.e3.e5.Nc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc3 Line|Costa Prefix' -> 'Costa Prefix'

### `D.Chi.Jan.Nf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Nf3 Line|Modern Gambit Prefix|Queen's Gambit Declined: Chigorin Defense, Janowski Variation" -> "Modern Gambit Prefix|Queen's Gambit Declined: Chigorin Defense, Janowski Variation"

### `D.Rub.Nc6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc6 Line|Bogoljubow Prefix|Classical Prefix' -> 'Bogoljubow Prefix|Classical Prefix'

### `D.Rub.Nc6.O-O.Bd6.Bb2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bb2 Line' -> ''

### `D.Rub.Nc6.O-O.Be7.Bb2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bb2 Line' -> ''

### `D.QGD.Bal.cxd5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'cxd5 Line|Argentinian Prefix' -> 'Argentinian Prefix'

### `D.QGD.Bal.cxd5.Bxb1` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bxb1 Line|Argentinian Prefix' -> 'Argentinian Prefix'

### `D.QGD.Bal.cxd5.Bxb1.Qa4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qa4 Line|Argentinian Prefix' -> 'Argentinian Prefix'

### `D.QGD.Bal.Nc3.Nf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf3 Line|Pseudo-Chigorin Prefix' -> 'Pseudo-Chigorin Prefix'

### `D.QGD.Mar.cxd5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'cxd5 Line|Tan Gambit Prefix|QGD Marshall Defense, cxd5' -> 'Tan Gambit Prefix|QGD Marshall Defense, cxd5'

### `D.QPG.Zuk.c5.e3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e3 Line|Krause Prefix' -> 'Krause Prefix'

### `D.QPG.Zuk.c5.e3.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf6 Line|Krause Prefix' -> 'Krause Prefix'

### `D.QPG.Zuk.c5.e3.Nf6.Nbd2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nbd2 Line|Krause Prefix' -> 'Krause Prefix'

### `A.Ret.QGI.MLn.Sic` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c5 Line|English Opening: Agincourt Defense, Catalan Defense' -> 'English Opening: Agincourt Defense, Catalan Defense'

### `A.Ret.Nf6.b4.g6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'g6 Line' -> ''

### `A.Gro.Kee.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line|Grob Keene Defense, Main Line' -> 'Grob Keene Defense, Main Line'

### `A.Van.d6.f4.e5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e5 Line|Hergert Prefix' -> 'Hergert Prefix'

### `A.Bir.Dut.b3.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf6 Line|Thomas Prefix' -> 'Thomas Prefix'

### `A.Bir.Dut.b3.Nf6.Bb2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bb2 Line|Thomas Prefix' -> 'Thomas Prefix'

### `A.War.Mad.MLn.f5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'f5 Line|Ware Gambit Prefix' -> 'Ware Gambit Prefix'

### `A.Pol.c6.Bb2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bb2 Line|Schuehler Prefix' -> 'Schuehler Prefix'

### `A.Pol.c6.Bb2.a5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'a5 Line|Schuehler Prefix' -> 'Schuehler Prefix'

### `A.Tro.Rap.MLn.Nxg5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nxg5 Line|Hergert Prefix' -> 'Hergert Prefix'

### `A.Tro.Rap.MLn.Nxg5.hxg5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'hxg5 Line|Hergert Prefix' -> 'Hergert Prefix'

### `B.Fre.Tar.Gui.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `B.Fre.Bur.Be7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be7 Line|French Defense: Classical Variation' -> 'French Defense: Classical Variation'

### `B.Fre.Bur.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line|French Defense: Classical Variation, Burn Variation, Main Line' -> 'French Defense: Classical Variation, Burn Variation, Main Line'

### `B.Fre.Win.Psn.Qxg7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qxg7 Line' -> ''

### `B.Fre.Win.Psn.Qxg7.Nbc6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nbc6 Line' -> ''

### `B.Pir.150.Arg.Qd2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qd2 Line' -> ''

### `B.Pir.Aus.c5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c5 Line|Pirc Defense: Austrian Attack, Dragon Formation' -> 'Pirc Defense: Austrian Attack, Dragon Formation'

### `B.Ale.Fou.Trd.Be3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be3 Line' -> ''

### `B.Sic.Nim.e5.Nc6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.Ind.Cat.Bb4.Bd2.Be7.Qc2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qc2 Line' -> ''

### `E.Ind.Cat.Bb4.Bd2.Be7.Nbd` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nbd7 Line' -> ''

### `E.Ind.Cat.Bb4.Bd2.Be7.Btr` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'b3 Line' -> ''

### `E.Ind.Cat.Bb4.Bd2.Be7.Rc1` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Rc1 Line' -> ''

### `E.Ind.Cat.Bb4.Bd2.Be7.Rd1` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Rd1 Line' -> ''

### `E.Ind.Cat.Bb4.Bd2.Be7.H6R` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'h6 Line' -> ''

### `E.KID.Sml.Cst.Bg5.c5.Bf4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "h6 Line|King's Indian Defense: Steiner Attack" -> "King's Indian Defense: Steiner Attack"

### `E.KID.Sml.Cst.Bg5.c5.Nxd5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Nxd5 Line|King's Indian Defense: Steiner Attack" -> "King's Indian Defense: Steiner Attack"

### `E.KID.Sml.Cst.Bg5.c5.Bxh6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Bxh6 Line|King's Indian Defense: Steiner Attack" -> "King's Indian Defense: Steiner Attack"

### `E.Nim.Rub.StP.MLn.Nf3.c5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c5 Line|Nimzo-Indian Defense: St. Petersburg Variation' -> 'Nimzo-Indian Defense: St. Petersburg Variation'

### `E.Nim.Rub.StP.MLn.Nf3.Ca4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Na4 Line|Nimzo-Indian Defense: St. Petersburg Variation' -> 'Nimzo-Indian Defense: St. Petersburg Variation'

### `E.Ind.e6.Nf3.d5.Bg5.c6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c6 Line' -> ''

### `E.Ind.e6.Nf3.d5.e3.Bb7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Bb7 Line|Queen's Indian Defense, with e3" -> "Queen's Indian Defense, with e3"

### `E.Ind.e6.Nf3.d5.e3.Bd6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Bd6 Line|Queen's Indian Defense, with e3" -> "Queen's Indian Defense, with e3"

### `E.Nim.Rub.Res.MLn.O-O.ML2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line|Nimzo-Indian Defense: Normal Variation, Bernstein Defense' -> 'Nimzo-Indian Defense: Normal Variation, Bernstein Defense'

### `E.KID.Cls.Old.e5.Re1` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Re1 Line' -> ''

### `E.KID.Cls.Old.e5.c6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c6 Line' -> ''

### `E.Ben.Mod.Cls.MLn.Re8.Na6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Na6 Line' -> ''

### `E.Ben.Mod.Cls.MLn.Re8.f3L` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'f3 Line' -> ''

### `E.Gru.Neo.MLn.cxd5.dxc5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'dxc5 Line' -> ''

### `E.Gru.Neo.MLn.cxd5.Nb6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nb6 Line' -> ''

### `E.KID.Cls.e5.O-O.Nbd7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nbd7 Line' -> ''

### `E.KID.Cls.e5.O-O.Nbd7.Re1` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Re1 Line|King's Indian Defense: Orthodox Variation" -> "King's Indian Defense: Orthodox Variation"

### `E.KID.Cls.e5.O-O.Nbd7.c6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "c6 Line|King's Indian Defense: Orthodox Variation, Positional Defense, Main Line" -> "King's Indian Defense: Orthodox Variation, Positional Defense, Main Line"

### `E.Nim.Rub.c5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c5 Line|Kangaroo Main Line e3 c5|Nimzo-Indian Defense: Rubinstein System' -> 'Kangaroo Main Line e3 c5|Nimzo-Indian Defense: Rubinstein System'

### `E.Nim.Rub.c5.Ne2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Ne2 Line|Nimzo-Indian Defense: Rubinstein System, Rubinstein Variation' -> 'Nimzo-Indian Defense: Rubinstein System, Rubinstein Variation'

### `E.Nim.Rub.c5.Ne2.a3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line|Nimzo-Indian Defense: Rubinstein System, Rubinstein Variation, Main Line' -> 'Nimzo-Indian Defense: Rubinstein System, Rubinstein Variation, Main Line'

### `E.Nim.Rub.O-O.Ne2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Ne2 Line|Nimzo-Indian Defense: Reshevsky Variation' -> 'Nimzo-Indian Defense: Reshevsky Variation'

### `A.Lar.Mod.c4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c4 Line|Nimzo-Larsen Attack: Modern Variation' -> 'Nimzo-Larsen Attack: Modern Variation'

### `A.Eng.Agi.Nf3.d5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd5 Line|Agincourt Defense Nf3, d5|English Opening: Agincourt Defense' -> 'Agincourt Defense Nf3, d5|English Opening: Agincourt Defense'

### `A.Eng.Agi.Nf3.d5.b3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'b3 Line|Agincourt Defense d5, b3 Line|English Opening: Agincourt Defense' -> 'Agincourt Defense d5, b3 Line|English Opening: Agincourt Defense'

### `A.Eng.Agi.Nf3.d5.b3.d4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd4 Line|Agincourt Defense b3 Line, d4|English Opening: Agincourt Defense' -> 'Agincourt Defense b3 Line, d4|English Opening: Agincourt Defense'

### `A.PQI.e3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e3 Line' -> ''

### `A.Hol.Rap.d5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "d5 Line|Queen's Pawn Game: Veresov Attack, Dutch System" -> "Queen's Pawn Game: Veresov Attack, Dutch System"

### `A.Hor.Fch.MLn.Nf3.Nbd` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Nbd7 Line|Queen's Gambit Declined: Barmen Variation" -> "Queen's Gambit Declined: Barmen Variation"

### `A.Gro.Gbt.MLn.d4.Bxb7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bxb7 Line' -> ''

### `A.Sod.e5.d3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd3 Line' -> ''

### `A.Sod.e5.Nc4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc4 Line' -> ''

### `A.Sod.e5.Nc4.Nc6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc6 Line' -> ''

### `A.Sod.e5.Nc4.Nc6.e4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e4 Line' -> ''

### `A.Van.c5.d4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd4 Line' -> ''

### `A.Van.c5.d4.cxd4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'cxd4 Line' -> ''

### `A.Van.c5.d4.cxd4.Qxd4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qxd4 Line' -> ''

### `A.Ret.Nf6.g3.g6.Bg2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bg2 Line|KIA Symmetrical Defense, Bg2' -> 'KIA Symmetrical Defense, Bg2'

### `A.Ret.d5.g3.g6.Bg2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bg2 Line' -> ''

### `A.Ret.d5.g3.Bg4.Bg2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bg2 Line' -> ''

### `A.Ret.d5.g3.Bg4.Bg2.Nd7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Nd7 Line|King's Indian Attack: Keres Variation" -> "King's Indian Attack: Keres Variation"

### `A.Kan.MLn.e3.c5.Ne2.cxd4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'cxd4 Line' -> ''

### `A.Col.Bd6.O-O.O-O` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'O-O Line' -> ''

### `A.Col.Bd6.O-O.O-O.b3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'b3 Line' -> ''

### `A.Col.Bd6.O-O.O-O.b3.Nbd7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nbd7 Line' -> ''

### `A.Lon.Job.e6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e6 Line|Rapport-Jobava System' -> 'Rapport-Jobava System'

### `A.Lon.Job.g6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'g6 Line|Rapport-Jobava System' -> 'Rapport-Jobava System'

### `B.Sic.McD.d5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd5 Line' -> ''

### `B.Fre.Rub.Nxe4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nxe4 Line' -> ''

### `B.Fre.Mac.MLn.Bd2.Bxc3.g6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'g6 Line|French Defense: McCutcheon Variation, Lasker Variation' -> 'French Defense: McCutcheon Variation, Lasker Variation'

### `B.Sic.Cls.Rch.Lip.e5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e5 Line' -> ''

### `B.Sic.Cls.Rch.Lip.Nxd4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nxd4 Line|Sicilian Defense: Richter-Rauzer Variation, Rauzer Attack' -> 'Sicilian Defense: Richter-Rauzer Variation, Rauzer Attack'

### `B.Sic.Cls.Rch.Lip.Nxd4.Qxd4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qxd4 Line|Sicilian Defense: Richter-Rauzer Variation, Classical Variation' -> 'Sicilian Defense: Richter-Rauzer Variation, Classical Variation'

### `B.Sic.Dra.Cls.Nrm.f4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'f4 Line' -> ''

### `B.Sic.Dra.Yug.Bd7.O-O-O.Rb8` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Rb8 Line|Sicilian Defense: Dragon Variation, Yugoslav Attack, Chinese Dragon' -> 'Sicilian Defense: Dragon Variation, Yugoslav Attack, Chinese Dragon'

### `B.Sic.Dra.Yug.Bd7.O-O-O.Qa5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qa5 Line' -> ''

### `B.Sic.Dra.Be3.Bg7.Be2.Nc6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc6 Line|Sicilian Defense: Dragon Variation, Classical Variation' -> 'Sicilian Defense: Dragon Variation, Classical Variation'

### `B.Fre.Tar.Ope.exd5.exd5.Nc6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `B.Sic.Tay.Nc3.Qc7.Be2.O-O` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'O-O Line' -> ''

### `B.Sic.Tay.Nc3.Qc7.Be2.Kh1` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Kh1 Line' -> ''

### `B.Sic.Kan.Nc3.b5.Bd3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bd3 Line' -> ''

### `B.Sic.Kan.Nc3.b5.Bd3.Qb6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qb6 Line' -> ''

### `B.Sic.Naj.Bg5.e6.f4.Qf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qf3 Line' -> ''

### `B.Sic.Naj.Bg5.e6.f4.Nbd7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line|Sicilian Defense: Najdorf Variation, Main Line' -> 'Sicilian Defense: Najdorf Variation, Main Line'

### `B.Sic.Cls.Rch.e6.Qd2.Bd7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bd7 Line|Sicilian Defense: Richter-Rauzer Variation, Neo-Modern Variation' -> 'Sicilian Defense: Richter-Rauzer Variation, Neo-Modern Variation'

### `B.Sic.Cls.Rch.e6.Qd2.f4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'f4 Line' -> ''

### `B.Sic.Cls.Rch.e6.Qd2.O-O-O` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be7 Line|Sicilian Defense: Richter-Rauzer Variation, Neo-Modern Variation' -> 'Sicilian Defense: Richter-Rauzer Variation, Neo-Modern Variation'

### `B.Sic.OKn.Nf6.Nc3.g6.Bg7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bg7 Line' -> ''

### `B.Sic.OKn.Nf6.Nc3.g6.O-O` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'O-O Line' -> ''

### `B.Sic.OKn.Nf6.Nc3.g6.Nc6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc6 Line' -> ''

### `B.Sic.Dra.Be3.Bg7.Be2.Nb3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nb3 Line|Sicilian Defense: Dragon Variation, Classical Variation' -> 'Sicilian Defense: Dragon Variation, Classical Variation'

### `B.Fre.Adv.c5.c3.Nc6.Qb6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `B.Fre.Tar.Cls.MLn.Bd3.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `B.Fre.Stn.MLn.f4.c5.Nc6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc6 Line' -> ''

### `B.Fre.Win.Adv.MLn.Ne7.Qc7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qc7 Line|French Defense: Winawer Variation, Advance Variation, with Bd3' -> 'French Defense: Winawer Variation, Advance Variation, with Bd3'

### `B.Fre.Win.Adv.MLn.Ne7.Nbc6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nbc6 Line|French Defense: Winawer Variation, Positional Variation' -> 'French Defense: Winawer Variation, Positional Variation'

### `B.Fre.Win.Adv.Pos.Qa5.c4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c4 Line' -> ''

### `B.Fre.Win.Psn.MLn.Ne2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Ne2 Line|French Defense: Winawer Variation, Poisoned Pawn Variation, Main Line' -> 'French Defense: Winawer Variation, Poisoned Pawn Variation, Main Line'

### `B.Nim.ScD.Nc3.dxe4.d5.Ne5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Ne5 Line|Nimzowitsch Defense: Scandinavian Variation, Bogoljubow Variation, Nimzowitsch Gambit' -> 'Nimzowitsch Defense: Scandinavian Variation, Bogoljubow Variation, Nimzowitsch Gambit'

### `B.Sic.Win.cxb4.a3.d5.Qxd5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qxd5 Line' -> ''

### `B.Ale.Chs.Nd5.Bc4.e6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e6 Line' -> ''

### `B.Ale.Chs.Nd5.Bc4.e6.Nc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc3 Line|Alekhine Defense: Hunt Variation, Lasker Simul Gambit' -> 'Alekhine Defense: Hunt Variation, Lasker Simul Gambit'

### `B.CaK.Cls.Spd.Nd7.h5.Bd3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bd3 Line' -> ''

### `B.Fre.Adv.Mil.MLn.Bd7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bd7 Line' -> ''

### `B.Fre.Win.Adv.MLn.Nc6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nbc6 Line|French Defense: Winawer Variation, Positional Variation' -> 'French Defense: Winawer Variation, Positional Variation'

### `B.Fre.Win.Adv.MLn.Nc6.Qa5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qa5 Line|French Defense: Winawer Variation, Positional Variation' -> 'French Defense: Winawer Variation, Positional Variation'

### `D.Sem.Qui.Nbd7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nbd7 Line' -> ''

### `D.Sem.Mer.Rab.Ng4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Ng4 Line' -> ''

### `D.Sem.Mer.Soz.O-O` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'O-O Line' -> ''

### `D.QGD.Ort.Cls.Qb1` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Qb1 Line|Queen's Gambit Declined: Orthodox Defense, Classical Variation" -> "Queen's Gambit Declined: Orthodox Defense, Classical Variation"

### `D.QGD.Ort.Cls.Qc2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Qc2 Line|Queen's Gambit Declined: Orthodox Defense, Classical Variation" -> "Queen's Gambit Declined: Orthodox Defense, Classical Variation"

### `D.Cat.Cls.Qc2.Bf4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bf4 Line' -> ''

### `D.Cat.Cls.Qc2.Bf4.Bb7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bb7 Line' -> ''

### `D.Cat.Cls.Qc2.Bf4.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.Cat.Cls.Qc2.Bf4.Ba6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Ba6 Line|Bogo-Indian Defense: Retreat Variation' -> 'Bogo-Indian Defense: Retreat Variation'

### `D.Sla.Not.Abr.a5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "a5 Line|Queen's Gambit Declined: Semi-Slav, Abrahams Variation" -> "Queen's Gambit Declined: Semi-Slav, Abrahams Variation"

### `D.Tar.Cls.Bg5.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `D.QGD.Har.Qc2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qc2 Line' -> ''

### `D.QGD.Har.Qc2.Rd1` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Rd1 Line|Queen's Gambit Declined: Harrwitz Attack" -> "Queen's Gambit Declined: Harrwitz Attack"

### `D.QGD.Har.Qc2.O-O-O` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "O-O-O Line|Queen's Gambit Declined: Harrwitz Attack" -> "Queen's Gambit Declined: Harrwitz Attack"

### `D.Sem.AMe.Sto.Bb2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bb2 Line' -> ''

### `D.Sem.AMe.Chi.Qe7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qe7 Line' -> ''

### `D.QGD.Tar.Exc.Nxd5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Nxd5 Line|Queen's Gambit Declined: Tartakower Defense, Makogonov Exchange Variation" -> "Queen's Gambit Declined: Tartakower Defense, Makogonov Exchange Variation"

### `D.QGD.Ort.Rc1` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Rc1 Line|Queen's Gambit Declined: Orthodox Defense, Main Line" -> "Queen's Gambit Declined: Orthodox Defense, Main Line"

### `D.QGD.Ort.Rc1.c6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "c6 Line|Queen's Gambit Declined: Orthodox Defense, Main Line" -> "Queen's Gambit Declined: Orthodox Defense, Main Line"

### `D.QGD.Ort.Rc1.c6.Bd3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Bd3 Line|Queen's Gambit Declined: Orthodox Defense, Bd3 Line" -> "Queen's Gambit Declined: Orthodox Defense, Bd3 Line"

### `A.Hol.Cls.c4.Nf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf3 Line' -> ''

### `A.Hol.Cls.c4.Nf3.d6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd6 Line' -> ''

### `A.Hol.Cls.c4.Nf3.d6.Nc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc3 Line' -> ''

### `A.Hol.Sto.c4.Nc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc3 Line' -> ''

### `A.Hol.Sto.c4.Nc3.c6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c6 Line' -> ''

### `A.Eng.Sym.Nc3.Nc6.g3.d6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd6 Line' -> ''

### `A.Eng.Sym.Nc3.Nc6.g3.Nge7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nge7 Line' -> ''

### `A.Eng.Sym.Nc3.Nc6.g3.a3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'a3 Line' -> ''

### `A.Eng.Sym.Nc3.Nc6.g3.d3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd3 Line' -> ''

### `A.Eng.Rev.Nc3.Nc6.g3.Nge2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nge2 Line' -> ''

### `A.KIA.Bg2.c6.O-O.Bf5.h6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'h6 Line' -> ''

### `A.KIA.Bg2.c6.O-O.Bf5.c4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c4 Line' -> ''

### `A.KIA.Bg2.c6.O-O.Bf5.e6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e6 Line' -> ''

### `A.KIA.Bg2.c6.O-O.Bf5.Nbd2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nbd2 Line' -> ''

### `A.KIA.Bg2.c6.O-O.Bf5.Nh4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nh4 Line' -> ''

### `A.Ret.Eng.Be7.O-O.O-O.c5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c5 Line' -> ''

### `A.Ret.Eng.Be7.O-O.O-O.e3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e3 Line' -> ''

### `A.Ret.Eng.Be7.O-O.O-O.d4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd4 Line' -> ''

### `A.Ret.Eng.Be7.O-O.O-O.Nc6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc6 Line' -> ''

### `A.Eng.Sym.Nf3.Nf6.Nc3.d4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd4 Line' -> ''

### `A.Eng.AIn.Nc3.d5.cxd5.g6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'g6 Line|English Opening: Anglo-Indian Defense, Anglo-Grünfeld Variation' -> 'English Opening: Anglo-Indian Defense, Anglo-Grünfeld Variation'

### `A.Eng.Rev.Fou.g3.Bc5.d6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "d6 Line|English Opening: King's English Variation, Four Knights Variation, Fianchetto Line, with .. d6" -> "English Opening: King's English Variation, Four Knights Variation, Fianchetto Line, with .. d6"

### `A.Eng.Rev.Fou.g3.Bc5.a6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "a6 Line|English Opening: King's English Variation, Four Knights Variation, Fianchetto Line, with .. d6, a6" -> "English Opening: King's English Variation, Four Knights Variation, Fianchetto Line, with .. d6, a6"

### `A.Eng.Rev.Fou.g3.Bc5.h6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "h6 Line|English Opening: King's English Variation, Four Knights Variation, Fianchetto Line, with .. d6, h6" -> "English Opening: King's English Variation, Four Knights Variation, Fianchetto Line, with .. d6, h6"

### `A.Ret.Ang.MLn.Nf6.Nc3.Qc2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qc2 Line' -> ''

### `E.KID.Avk.Ben.MLn.e6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Main Line|King's Indian Defense: Averbakh Variation, Main Line" -> "King's Indian Defense: Averbakh Variation, Main Line"

### `C.KGm.Acc.Bsh.Ble.Nc3.Gtr` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "g3 Line|King's Gambit Accepted: Bishop's Gambit, McDonnell Attack" -> "King's Gambit Accepted: Bishop's Gambit, McDonnell Attack"

### `C.Ita.Two.O-O.Bc5.Bg5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bg5 Line' -> ''

### `C.Ita.Pia.Nf6.MLn.Ba7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Ba7 Line|Italian Game: Classical Variation, Giuoco Pianissimo' -> 'Italian Game: Classical Variation, Giuoco Pianissimo'

### `E.Ben.Mod.Fou.MLn.Re8` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.Nim.Rub.StP.MLn.Nf3.Qe7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qe7 Line|Nimzo-Indian Defense: St. Petersburg Variation' -> 'Nimzo-Indian Defense: St. Petersburg Variation'

### `E.Nim.Rub.Cls.Nf3.Nc6.dxc4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'dxc4 Line|Nimzo-Indian Defense: Ragozin Variation' -> 'Nimzo-Indian Defense: Ragozin Variation'

### `A.Van.ReN.e3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e3 Line' -> ''

### `A.Van.ReN.e3.d5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd5 Line' -> ''

### `A.Van.d5.e3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e3 Line' -> ''

### `A.Van.d5.e3.e5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e5 Line' -> ''

### `A.Van.d5.e3.e5.d4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd4 Line' -> ''

### `A.Eng.Rev.g3.Nf6.Bg2.d3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "d3 Line|English Opening: King's English Variation, Four Knights Variation, Fianchetto Line" -> "English Opening: King's English Variation, Four Knights Variation, Fianchetto Line"

### `A.PoD.Bb7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bb7 Line|Polish Defense, Bb7' -> 'Polish Defense, Bb7'

### `A.EID.Bf4.Bg7.e3.d6.O-O` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'O-O Line' -> ''

### `A.QPO.c6.Nf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf3 Line' -> ''

### `A.QPO.c6.Nf3.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf6 Line' -> ''

### `B.Fre.Nrm.d5.Nc3.a6.a3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'a3 Line' -> ''

### `B.Fre.Nrm.d5.Nc3.a6.Ne2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Ne2 Line' -> ''

### `B.Fre.Nrm.d5.Nc3.a6.Bg5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bg5 Line|French Defense: Classical Variation' -> 'French Defense: Classical Variation'

### `B.Sic.Clo.Fch.Bot.e5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e5 Line' -> ''

### `B.Sic.Cls.Be2.e5.Nb3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nb3 Line' -> ''

### `B.Sic.Dra.Yug.Nc6.Bc4.Bb3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `B.Sic.Dra.Yug.Nc6.Bc4.h4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'h4 Line' -> ''

### `B.Sca.MLn.Qd8.d4.Nf6.Bg4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `B.Fre.Win.Adv.MLn.Nf3.Qc7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qc7 Line|French Defense: Winawer Variation, Positional Variation' -> 'French Defense: Winawer Variation, Positional Variation'

### `B.Fre.Win.Adv.MLn.Nf3.h4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'h4 Line|French Defense: Winawer Variation, Positional Variation' -> 'French Defense: Winawer Variation, Positional Variation'

### `B.Ale.Nrm.Dpn.d6.Nb6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nb6 Line|Alekhine Defense d6, Nb6' -> 'Alekhine Defense d6, Nb6'

### `B.CaK.Kar.Bc4.Ngf6.Qe2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qe2 Line' -> ''

### `B.CaK.Kar.Bc4.Ngf6.Qe2.Nb6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nb6 Line' -> ''

### `B.CaK.Kar.Bc4.Ngf6.Qe2.Bb3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `B.Sca.Mod.Mie.Bf5.Ne5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Ne5 Line' -> ''

### `B.Mod.Std.Ctr.d6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd6 Line|Modern c4 Center, d6 Line' -> 'Modern c4 Center, d6 Line'

### `B.Mod.Std.Ctr.d6.Be3.f3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'f3 Line' -> ''

### `B.Mod.Pte.Nc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc3 Line' -> ''

### `B.Mod.Pte.Nc3.d6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd6 Line' -> ''

### `B.Sic.StC.Nc6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc6 Line' -> ''

### `B.Sic.StC.Nc6.Nc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc3 Line' -> ''

### `B.Sic.Fre.Nc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc3 Line' -> ''

### `B.Sic.SmM.Acc.Sib.Qe2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qe2 Line' -> ''

### `A.Mod.Nc3.d6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd6 Line|Modern Defense Nc3, d6' -> 'Modern Defense Nc3, d6'

### `A.Tro.Psn.Nc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc3 Line' -> ''

### `A.Ret.Fch.MLn.Bg2.d6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd6 Line|Zukertort Opening: Double Fianchetto Attack' -> 'Zukertort Opening: Double Fianchetto Attack'

### `A.Hol.Sto.Bot.MLn.Ba3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Ba3 Line' -> ''

### `A.Ret.Ang.MLn.Nf6.Nc3.Bd6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bd6 Line' -> ''

### `A.Col.Bd6.O-O.O-O.b3.Bb2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bb2 Line|Rubinstein Opening: Semi-Slav Defense' -> 'Rubinstein Opening: Semi-Slav Defense'

### `A.Col.Bd6.O-O.O-O.b3.c6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c6 Line|Rubinstein Opening: Semi-Slav Defense' -> 'Rubinstein Opening: Semi-Slav Defense'

### `A.Col.Bd6.O-O.O-O.b3.Nbd2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nbd2 Line|Rubinstein Opening: Semi-Slav Defense' -> 'Rubinstein Opening: Semi-Slav Defense'

### `A.Hor.Fch.MLn.Bg5.Nbd7.c6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "c6 Line|Horwitz French Knight Defense, c6|Queen's Gambit Declined: Modern Variation, Knight Defense" -> "Horwitz French Knight Defense, c6|Queen's Gambit Declined: Modern Variation, Knight Defense"

### `A.PQI.e3.Bb7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `C.Cen.exd4.Nf3.c5.Bc4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bc4 Line' -> ''

### `C.Bsh.Lew.Bxd5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Bxd5 Line|Bishop's Opening: Lewis Countergambit" -> "Bishop's Opening: Lewis Countergambit"

### `C.KGm.Acc.Nf3.KKn.Bc4.Qxf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qxf3 Line' -> ''

### `C.Thr.Bb4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bb4 Line' -> ''

### `C.Ita.Giu.c3.Nf6.d3.a6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'a6 Line|Italian Game: Classical Variation, Giuoco Pianissimo, with a6' -> 'Italian Game: Classical Variation, Giuoco Pianissimo, with a6'

### `C.Ita.Pia.Wai.MLn.Re1.Ba7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Ba7 Line|Italian Game: Classical Variation, Giuoco Pianissimo' -> 'Italian Game: Classical Variation, Giuoco Pianissimo'

### `C.Ita.Giu.O-O.Nf6.d3.d5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd5 Line|Italian Game: Classical Variation, Giuoco Pianissimo' -> 'Italian Game: Classical Variation, Giuoco Pianissimo'

### `C.Ita.Two.Opn.MLn.e5.Ne4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Ne4 Line|Italian Game: Scotch Gambit, Max Lange Attack' -> 'Italian Game: Scotch Gambit, Max Lange Attack'

### `C.RyL.Mor.Ba4.d6.Bxc6.d4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd4 Line|Ruy López: Morphy Defense, Modern Steinitz Defense' -> 'Ruy López: Morphy Defense, Modern Steinitz Defense'

### `C.RyL.Mor.Ba4.d6.c3.Nge7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nge7 Line|Ruy López: Morphy Defense, Modern Steinitz Defense' -> 'Ruy López: Morphy Defense, Modern Steinitz Defense'

### `C.RyL.Cha.MLn.d4.Qc7.Nc6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc6 Line|Ruy López: Closed, Chigorin Defense' -> 'Ruy López: Closed, Chigorin Defense'

### `C.Fou.Spa.Dbl.MLn.d3.Ne7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Ne7 Line|Four Knights Game: Spanish Variation, Symmetrical Variation' -> 'Four Knights Game: Spanish Variation, Symmetrical Variation'

### `D.QGD.Exc.Bg5.c6.Qc2.Bd3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Bd3 Line|Queen's Gambit Declined: Exchange Variation, Reshevsky Variation" -> "Queen's Gambit Declined: Exchange Variation, Reshevsky Variation"

### `D.Sem.AMe.Sto.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Main Line' -> ''

### `E.Ind.Cat.d5.Bg2.dxc4.Qxc4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qxc4 Line' -> ''

### `E.Nim.Rub.Res.MLn.O-O.Qc2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qc2 Line|Nimzo-Indian Defense: Normal Variation, Bernstein Defense' -> 'Nimzo-Indian Defense: Normal Variation, Bernstein Defense'

### `E.Ben.Bnk.Acc.Nc3.axb5.a4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'a4 Line' -> ''

### `E.Ben.Bnk.Acc.MLn.Bxa6.Nf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf3 Line' -> ''

### `E.Ben.Mod.Cls.MLn.a6.Nd2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nd2 Line' -> ''

### `E.Ben.Mod.Cls.MLn.a6.Bg5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bg5 Line' -> ''

### `E.Ben.Mod.Fou.MLn.h3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'h3 Line' -> ''

### `E.Ben.Mod.Fou.MLn.e5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e5 Line' -> ''

### `E.Gru.Exc.SeV.Bc4.c5.Nc6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc6 Line' -> ''

### `C.PhD.d4.exd4.Nxd4.d5.exd5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'exd5 Line' -> ''

### `C.Fou.Spa.Rub.Nxe5.Qe7.f4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'f4 Line' -> ''

### `C.Ita.Two.O-O.Bc5.Nc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc3 Line' -> ''

### `C.Ita.Two.O-O.Bc5.Nc3.d6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd6 Line' -> ''

### `C.Ita.Evn.Acc.Mcd.Mor.Bg4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bg4 Line|Italian Game: Evans Gambit' -> 'Italian Game: Evans Gambit'

### `C.Ita.Two.Nc3.Nxe4.Nxe4.d5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd5 Line' -> ''

### `C.RyL.SCG.Nxe5.Nxc6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nxc6 Line|Ruy López: Spanish Countergambit, Harding Gambit' -> 'Ruy López: Spanish Countergambit, Harding Gambit'

### `C.RyL.Stn.d4.Bd7.Nc3.Bxc6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bxc6 Line' -> ''

### `C.RyL.Mor.Ba4.b5.Bb3.d6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd6 Line' -> ''

### `C.RyL.Fia.c3.a6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'a6 Line' -> ''

### `C.RyL.Fia.c3.a6.Ba4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Ba4 Line' -> ''

### `C.RyL.Fia.c3.a6.Ba4.d6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd6 Line' -> ''

### `B.Fre.Adv.Mil.MLn.O-O.Bd7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bd7 Line' -> ''

### `B.Fre.Adv.NwG.cxd4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'cxd4 Line' -> ''

### `B.Fre.Win.Adv.Smy.Qc7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qc7 Line|French Defense: Winawer Variation, Advance Variation, Smyslov Variation' -> 'French Defense: Winawer Variation, Advance Variation, Smyslov Variation'

### `B.Sic.Clo.Nc6.d3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd3 Line' -> ''

### `B.Sic.Clo.Nc6.d3.g6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'g6 Line' -> ''

### `B.Sic.Kan.Tal.MLn.Nc6.Bc2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bc2 Line|Sicilian Defense: Kan Variation, Maróczy Bind, Bronstein Variation' -> 'Sicilian Defense: Kan Variation, Maróczy Bind, Bronstein Variation'

### `B.Sic.Nf3.f5.exf5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'exf5 Line' -> ''

### `B.Sic.Tay.Nc3.d6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd6 Line' -> ''

### `B.Sic.Tay.Nc3.d6.Be2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be2 Line' -> ''

### `B.Sic.Tay.Nc3.Qc7.Be3.a6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'a6 Line' -> ''

### `B.Sic.SmM.Acc.Nxc3.Nc6.Bc4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bc4 Line' -> ''

### `B.Sic.SmM.Acc.Pau.O-O` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'O-O Line' -> ''

### `B.Sic.SmM.Acc.Pau.O-O.b5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'b5 Line' -> ''

### `A.Ret.Ang.MLn.Nf6.Nc3.Be2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be2 Line|Semi-Slav Defense: Normal Variation' -> 'Semi-Slav Defense: Normal Variation'

### `A.Ret.Ang.MLn.Nf6.Nc3.Bd3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bd3 Line|Semi-Slav Defense: Chigorin Defense' -> 'Semi-Slav Defense: Chigorin Defense'

### `A.Eng.Agi.Nf3.d5.Nbd2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Nbd2 Line|Agincourt Defense d5, Queen's Indian Nbd2 Line" -> "Agincourt Defense d5, Queen's Indian Nbd2 Line"

### `A.Eng.AIn.Nc3.d5.cxd5.Nb6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nb6 Line|English Opening: Anglo-Indian Defense, Anglo-Grünfeld Variation' -> 'English Opening: Anglo-Indian Defense, Anglo-Grünfeld Variation'

### `A.Eng.AIn.Nc3.d5.cxd5.Nxc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nxc3 Line|English Opening: Anglo-Indian Defense, Anglo-Grünfeld Variation' -> 'English Opening: Anglo-Indian Defense, Anglo-Grünfeld Variation'

### `A.Eng.Rev.Fou.e3.Bb4.Bxc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Bxc3 Line|English Opening: King's English Variation, Four Knights Variation, Quiet Line" -> "English Opening: King's English Variation, Four Knights Variation, Quiet Line"

### `A.Eng.Rev.Fou.e3.Bb4.Qf5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Qf5 Line|English Opening: King's English Variation, Four Knights Variation, Quiet Line" -> "English Opening: King's English Variation, Four Knights Variation, Quiet Line"

### `A.Eng.Sym.Nc3.Nc6.g3.e5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e5 Line|English Opening: Symmetrical Variation, Botvinnik System Reversed, with Nf3' -> 'English Opening: Symmetrical Variation, Botvinnik System Reversed, with Nf3'

### `A.QPO.g6.Nf3.Bg7.e3.Nxd4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nxd4 Line' -> ''

### `A.Mod.Nc3.c5.d5.Bxc3.f5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'f5 Line|Modern Defense: Beefeater Variation' -> 'Modern Defense: Beefeater Variation'

### `A.Mod.Nc3.c5.d5.Bxc3.Qa5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qa5 Line|Pterodactyl Defense: Fianchetto, Queen Pteranodon' -> 'Pterodactyl Defense: Fianchetto, Queen Pteranodon'

### `A.PQI.e3.Bb7.Bb2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bb2 Line' -> ''

### `C.RyL.Mor.Ba4.d6.Bxc6.f6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'f6 Line|Ruy López: Morphy Defense, Modern Steinitz Defense' -> 'Ruy López: Morphy Defense, Modern Steinitz Defense'

### `C.RyL.Mor.Ba4.Nf6.O-O.d3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd3 Line|Ruy López: Closed, Worrall Attack, Castling Line' -> 'Ruy López: Closed, Worrall Attack, Castling Line'

### `C.RyL.Cha.MLn.d4.Qc7.dxc5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'dxc5 Line|Ruy López: Closed, Chigorin Defense' -> 'Ruy López: Closed, Chigorin Defense'

### `C.PhD.d4.f5.Bc4.exd4.Nxh7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nxh7 Line' -> ''

### `A.Hol.c4.Nf6.g3.e6.d5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd5 Line|Dutch Defense c4 Nf6 e6, d5 Line|Dutch Defense: Classical Variation' -> 'Dutch Defense c4 Nf6 e6, d5 Line|Dutch Defense: Classical Variation'

### `A.Hor.Fch.MLn.Nf3.Be7.b3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'b3 Line' -> ''

### `A.QPO.Nf6.Nf3.e6.e3.c5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "c5 Line|Queen's Pawn Game: Colle System" -> "Queen's Pawn Game: Colle System"

### `A.QPO.Nf6.Nf3.e6.e3.Be7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be7 Line' -> ''

### `B.Sic.Alp.Cen.MLn.cxd4.cxd4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'cxd4 Line|Central Exchange' -> 'Central Exchange'

### `B.Sic.Alp.Dd6.MLn.Nc6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc6 Line' -> ''

### `B.Sic.Alp.Dd6.MLn.Nc6.d4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd4 Line' -> ''

### `B.Sic.Mor.Bd7.MLn.O-O` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'O-O Line' -> ''

### `B.Sic.Mor.Bd7.MLn.O-O.Nc6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc6 Line' -> ''

### `B.Fre.Rub.MLn.Nf6.Nxf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nxf6 Line' -> ''

### `B.Sic.OKn.Nf6.f3.e5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e5 Line' -> ''

### `B.Sic.Naj.Sch.O-O.Nbd7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nbd7 Line' -> ''

### `B.Sic.Naj.Sch.O-O.Qc7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Qc7 Line|Sicilian Defense: Scheveningen Variation, Classical Variation' -> 'Sicilian Defense: Scheveningen Variation, Classical Variation'

### `B.Sic.Cls.Soz.e6.Be3.Be7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Be7 Line' -> ''

### `B.Sic.Sch.Be2.Be7.Bd7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bd7 Line|Sicilian Defense: Scheveningen Variation, Modern Variation' -> 'Sicilian Defense: Scheveningen Variation, Modern Variation'

### `A.Eng.Rev.Fou.MLn.Bg2.Bc5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Bc5 Line|Fianchetto Line|English Opening: King's English Variation, Four Knights Variation, Fianchetto Line, with Bc5" -> "Fianchetto Line|English Opening: King's English Variation, Four Knights Variation, Fianchetto Line, with Bc5"

### `A.Owe.Eng.e4.Bb7.Bd3.Nc6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc6 Line|English Defense Perrin, Nc6' -> 'English Defense Perrin, Nc6'

### `A.Eng.Rev.e3.Nf6.f4.Nf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Nf3 Line|English Opening: King's English Variation, Kahiko-Hula Gambit" -> "English Opening: King's English Variation, Kahiko-Hula Gambit"

### `A.Kan.MLn.e3.O-O.a3.bxc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'bxc3 Line' -> ''

### `A.KIA.Sic.MLn.g3.Nf6.Re1` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Re1 Line' -> ''

### `C.LtO.Bc4.fxe4.Nxh8.Nf6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf6 Line' -> ''

### `B.Sic.Naj.Pst.MLn.Qxb2.Rb1` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Rb1 Line' -> ''

### `A.Van.d5.e4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e4 Line' -> ''

### `A.Van.d5.e4.dxe4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'dxe4 Line' -> ''

### `A.Eng.CKa.Nf3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nf3 Line' -> ''

### `A.Eng.CKa.Nf3.d5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd5 Line' -> ''

### `A.Mod.e4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e4 Line|Modern Defense, e4 Line' -> 'Modern Defense, e4 Line'

### `A.Mod.e4.c5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c5 Line|Modern Defense e4, c5' -> 'Modern Defense e4, c5'

### `A.VtK.e5.Nc3.Nc6.f4.exf4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'exf4 Line' -> ''

### `A.VtK.e5.Nc3.d5.f4.exf4` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'exf4 Line' -> ''

### `A.KIA.Fre.c5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c5 Line' -> ''

### `A.Eng.AIn.g3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'g3 Line|Anglo-Indian Defense, g3 Line' -> 'Anglo-Indian Defense, g3 Line'

### `A.Eng.AIn.g3.c6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'c6 Line' -> ''

### `A.Eng.Sym.Nf3.Nf6.Nc3.d5` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'd5 Line' -> ''

### `A.Eng.AIn.Nf3.g6.g3.Bg7` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bg7 Line' -> ''

### `A.Eng.CKa.Nf3.d5.g3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'g3 Line' -> ''

### `A.Eng.CKa.Nf3.d5.g3.Bg2` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Bg2 Line|Réti Opening: Anglo-Slav Variation, with g3' -> 'Réti Opening: Anglo-Slav Variation, with g3'

### `A.Eng.Agi.Nc3` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'Nc3 Line|Agincourt Defense, Nc3' -> 'Agincourt Defense, Nc3'

### `D.QGD.Har.Har.MLn` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: "Main Line|Queen's Gambit Declined: Harrwitz Attack, Main Line" -> "Queen's Gambit Declined: Harrwitz Attack, Main Line"

### `B.CaK.Adv.Bf5.c3.e6` (evidence: EDITORIAL)
- sources: docs/ocn-audit-2026-07.md section 2, Content weaknesses (synthetic aliases); docs/traction-roadmap.md H2.6 and design decision 6; rule = web/build.py is_synthetic_alias.
- `aliases`: 'e6 Line' -> ''

## Validation: PASS

```
OK: 5899 entries validated, 0 warning(s)
```

