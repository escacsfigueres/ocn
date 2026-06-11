# Decision record — phantom pairs and duplicate canonical names

**Status: APPROVED AND EXECUTED 2026-06-11.** Albert approved all
recommendations the same day; both micro-lots applied via the engine
(`phantom-eco-align`, 2 rows; `duplicate-name-renames`, 5 rows), the spec
gained the path-marker blessing, and both allowlists
(`PHANTOM_PAIR_ECO_ALLOWLIST`, `DUPLICATE_NAME_ALLOWLIST`) are now empty —
validator checks 13 and 19 run unconditionally. The analysis below is the
decision's evidence record.

## The 6 phantom pairs — recommendation: spec-bless + ECO-align

Every "phantom" child (moves_uci byte-identical to its parent) turns out to
be a **deliberate path-marker from the transposition cleanup**: each one's
notes already say "Move-order transposition / Same FEN as parent …
transposes there". They document that a named line is reached by another
move order without reopening the `transposes_to` layer (which the audit
marks CLOSED — "do not reopen").

| child | parent | eco child vs parent |
|---|---|---|
| `D.Sla.Cze.Kra.MLn` | `D.Sla.Cze.Kra` | D17 = D17 |
| `A.Tro.Bxf6.e3` | `A.Tro.Bxf6` | A45 = A45 |
| `E.Gru.Rus.Hng.e4` | `E.Gru.Rus.Hng` | **D97\|D98\|D99 ≠ D97** |
| `E.QID.Euw.Bd3` | `E.QID.Euw` | **E14\|E17 ≠ E17** |
| `A.Ret.f5.d3.e4` | `A.Ret.f5.d3` | A04 = A04 |
| `A.PQI.e3.Bb7` | `A.PQI.e3` | A47 = A47 |

Options considered:

- **Merge** (delete the children): row-identity loss — *risky* class,
  breaks downstream slugs, forces consumer coordination. Overkill for six
  documented markers.
- **Link** (`transposes_to=parent`): structurally cleanest but reopens the
  closed transposition layer and touches structural columns no engine mode
  may write. Defer to a future major if ever.
- **Spec-bless** *(recommended)*: one spec sentence blessing path-marker
  children (same-FEN child allowed iff its notes declare the move-order
  relation), plus an **ECO-align micro-lot** (`eco_legacy_only`, 2 rows:
  `E.Gru.Rus.Hng.e4` → `D97`, `E.QID.Euw.Bd3` → `E17`) so a path-marker
  always carries its parent's classification. Afterwards
  `PHANTOM_PAIR_ECO_ALLOWLIST` empties and validator check 19 becomes
  unconditional.

## The 4 duplicate-name pairs — recommendation: surgical renames

All four pairs are **different positions (different FEN)** sharing one
string — never co-canonicals. One `naming_strings_only` micro-lot:

1. **"English Reversed Sicilian g3, d5"** — `A.Eng.Rev.g3.Nf6.Bg2.d5`
   (A29, via Bg2) vs `A.Eng.Rev.Nc3.Nf6.g3.d5` (A22, via Nc3; alias
   "Reversed Dragon"). Rename the second to **"English Reversed Sicilian
   Nc3 g3, d5"** (path-compositional, matches its slug); the first keeps
   the name.
2. **"King's Indian Attack"** — `A.KIA` (family head, A05|A07|A08) vs
   `A.Ret.d5.g3` (A07, the 1.Nf3 d5 2.g3 path). Rename the child to
   **"Réti, King's Indian Attack Setup"**; the family head keeps the
   plain name.
3. **"King's Pawn Game"** — `C.KPO` (1.e4 e5, C20) vs `B.KPG` (bare 1.e4,
   B00). Different concepts: rename `B.KPG` to **"King's Pawn Opening"**
   (its own existing alias, which then drops as identity; `C.KPO` also
   carries that alias — drop there too). `C.KPO` keeps "King's Pawn Game"
   (standard usage for 1.e4 e5).
4. **"Réti Opening"** — `A.Ret` (family head, bare 1.Nf3, alias "Zukertort
   Opening") vs `A.Ret.d5.c4` (A09, the Réti proper). Rename the child to
   **"Réti Opening, 2.c4"** — the family head stays stable for consumers.
   (Alternative considered: rename the head to "Zukertort Opening" to
   match Lichess A04 exactly; rejected as a consumer-visible family-head
   rename with no data gain.)

Afterwards `DUPLICATE_NAME_ALLOWLIST` empties and the uniqueness check
becomes unconditional.

## Sequencing

Both micro-lots are engine-mode work (one `eco_legacy_only` 2 rows, one
`naming_strings_only` ~5 rows + 1 spec sentence + allowlist removals) and
bundle naturally **into release 1.2.0** with the diacritic and ECO lots
already applied. Each needs its own dry-run + GO.
