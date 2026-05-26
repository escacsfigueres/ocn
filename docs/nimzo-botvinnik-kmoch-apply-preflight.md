# Nimzo Botvinnik/Kmoch — apply preflight checklist

**Status**: **APPLIED** (commit pending push). `E.Nim.Sml.Kmo`
now `transposes_to = E.Nim.Sml.Bot` with the spurious "Kmoch"
relabelled to "a3 Move Order"; `E.Nim.Sml.Kmo.MLn` relabelled to
"e3 Main Line". Result: unresolved 2 → 1 (only QID remains),
resolved 123 → 124. The `Rub.Kmo` artifact + `Kmo.MLn` parent-chain
quirk remain out-of-scope follow-ups (below). Specifies the apply of
**Option B** from
[`nimzo-botvinnik-kmoch-naming-review.md`](nimzo-botvinnik-kmoch-naming-review.md):
demote the spurious "Kmoch" on the depth-3 Sämisch node and point it
at the correctly-named Botvinnik canonical.

**Do not apply from this document.** Apply in a dedicated, GO'd
commit. This is a small relation + relabel apply (no delete, no
slug rename, no schema change) — much lighter than the QID slug
migration, but still its own commit.

## Affected rows (current state at `4e96984`)

| slug | name | alias | eco | TT | SA | children | role in apply |
|---|---|---|---|---|---|---|---|
| `E.Nim.Sml.Kmo` | "Nimzo Saemisch, **Kmoch** Variation" | "Kmoch Variation" | E26 | — | — | `Kmo.MLn` | **MODIFY**: add TT → Bot, drop "Kmoch" |
| `E.Nim.Sml.Bot` | "Nimzo Sämisch, Botvinnik" | "Botvinnik Variation" | E24/E25 | — | — | MLn, cxd5, Rom | **CANONICAL** (unchanged) |
| `E.Nim.Sml.Kmo.MLn` | "Nimzo Saemisch **Kmoch**, Main Line" | "Main Line" | E26 | — | — | (leaf) | **MODIFY** (relabel): drop "Kmoch" |
| `E.Nim.Fou` | "Nimzo, 4.f3" | "**Kmoch Variation**\|4.f3 System" | E20 | — | — | `Fou.MLn` | **UNCHANGED** — this is the *correct* home of "Kmoch" (must NOT lose the alias) |
| `E.Nim.Sml.Bot.MLn` | "Nimzo Saemisch Botvinnik, Main Line" | "Main Line" | E25 | — | **SA=`E.Nim.Rub.Kmo`** | Bd3, Nxd5 | **OUT OF SCOPE** (see follow-up) |
| `E.Nim.Rub.Kmo` | "Nimzo Rubinstein, **Kmoch** Variation" | "Kmoch Variation" | E40 | — | **SA=`E.Nim.Sml.Bot.MLn`** | (leaf) | **OUT OF SCOPE** (separate "Kmoch" artifact — see follow-up) |

`E.Nim.Sml.Kmo` has no inbound `transposes_to`/`same_as`, so adding
its own TT is self-contained.

## Apply plan (Option B — minimal)

### 1. `E.Nim.Sml.Kmo` — add transposes_to + relabel

- `transposes_to` (field 13) → **`E.Nim.Sml.Bot`**
- `same_as` (field 14) → **stays empty**
- `canonical_name`: "Nimzo Saemisch, Kmoch Variation" → **"Nimzo Sämisch, a3 move order"** *(proposed; drops the spurious "Kmoch")*
- `aliases`: "Kmoch Variation" → **"a3 move order"** *(proposed; or empty)*
- `notes`: → e.g. *"a3-first move order (4.a3 Bxc3+ 5.bxc3 c5 6.f3 d5) reaching the same FEN as E.Nim.Sml.Bot (Sämisch Botvinnik); transposes there. The 'Kmoch Variation' name belongs to the 4.f3 line (E.Nim.Fou, E20), not here."*
- **slug unchanged** (`E.Nim.Sml.Kmo`) — no rename.

### 2. `E.Nim.Sml.Kmo.MLn` — relabel only (drop "Kmoch")

- `canonical_name`: "Nimzo Saemisch Kmoch, Main Line" → **"Nimzo Sämisch, e3 Main Line"** *(proposed; this node is the plain E26 Sämisch `4.a3 Bxc3+ 5.bxc3 c5 6.e3` line)*
- `aliases`: "Main Line" → unchanged
- No TT/SA change; slug unchanged; stays a child of (now-TT) `E.Nim.Sml.Kmo`.

### 3. Everything else — UNCHANGED

- `E.Nim.Sml.Bot` stays canonical (no edit).
- `E.Nim.Fou` keeps its `Kmoch Variation|4.f3 System` alias (the correct Kmoch home).
- `E.Nim.Sml.Bot.MLn ⇄ E.Nim.Rub.Kmo` same_as is **not touched** in this apply.

**No same_as. No delete. No slug rename. No reparent. No schema change.**

## CSV field mechanics (avoid the comma-count trap)

`E.Nim.Sml.Kmo` currently ends `…,<notes>,,,,,` (5 empty trailing
fields: attributed_to, attribution_source, historical_notes,
transposes_to, same_as). To set `transposes_to` (field 13) with
`same_as` (field 14) empty:

```
…,"<new notes>",,,,E.Nim.Sml.Bot,
```
(4 commas, value, 1 trailing comma). Verify with a `csv.DictReader`
field-dump: `transposes_to=='E.Nim.Sml.Bot'`, `same_as==''`,
`historical_notes==''`.

## Expected audit metrics (after apply)

| metric | now | after | Δ |
|---|---|---|---|
| catalogue rows | 5,900 | 5,900 | 0 (TT + relabel; no delete) |
| unresolved_groups | 2 | **1** | −1 (only QID Miles/Petrosian remains) |
| resolved_groups | 123 | **124** | +1 (Bot ⇄ Kmo now single_canonical) |
| multiple_canonical_groups | 17 | 17 | 0 (single_canonical, not multi) |
| duplicate_groups | 125 | 125 | 0 (group still exists, now resolved) |

## Verification checklist (for the future apply)

- [ ] `E.Nim.Sml.Kmo.transposes_to == "E.Nim.Sml.Bot"` (field 13).
- [ ] `E.Nim.Sml.Kmo.same_as == ""` (field 14) and
      `historical_notes == ""` (no comma-count drift).
- [ ] `E.Nim.Sml.Kmo` canonical_name/alias no longer contain "Kmoch".
- [ ] `E.Nim.Sml.Kmo.MLn` canonical_name no longer contains "Kmoch".
- [ ] `E.Nim.Sml.Bot` unchanged (still canonical, correct name).
- [ ] `E.Nim.Fou` STILL has alias `Kmoch Variation|4.f3 System`
      (the legitimate Kmoch home — must not be touched).
- [ ] No new FEN collision introduced; `E.Nim.Sml.Kmo` FEN still
      equals `E.Nim.Sml.Bot` FEN (the TT target shares the FEN).
- [ ] `E.Nim.Sml.Bot.MLn ⇄ E.Nim.Rub.Kmo` same_as **unchanged**
      (explicitly out of scope; not accidentally altered).
- [ ] `validate.py --strict-chess` → 0 warnings (TT target exists,
      shares FEN, not self, not class root).
- [ ] `audit_chess.py` → 0 illegal / 0 san_mismatch.
- [ ] `unittest discover tools/tests` → green (grep tests for
      `E.Nim.Sml.Kmo` first; update any assertion that pins its
      name/alias).
- [ ] `audit_transpositions.py --summary` → `unresolved_groups=1`,
      `resolved_groups=124`, `multiple_canonical_groups=17`,
      rows=5,900.
- [ ] `lichess_parent_map.py --check` → still 3690/3690.
- [ ] `git diff --check` clean.

## Out of scope / follow-ups (NOT in this apply)

1. **`E.Nim.Rub.Kmo` "Kmoch" artifact** — the review found this is
   the *same* misattribution (no Lichess "Rubinstein Kmoch";
   Kmoch = 4.f3). Its `same_as` with `E.Nim.Sml.Bot.MLn` is
   position-sound, but the "Kmoch" label should be relabelled in a
   **separate** follow-up. Left untouched here to keep this apply
   minimal and the same_as intact.
2. **`E.Nim.Sml.Kmo.MLn` parent-chain quirk** — its moves
   (`…c5 e3`) do not extend its parent `E.Nim.Sml.Kmo` (`…c5 f3 d5`);
   it is really the E26 Sämisch e3 line. This apply only relabels
   it (drops "Kmoch"); a structural reparent is a separate, deeper
   decision (not required to resolve the duplicate group).
3. **Slug segment `.Kmo`** — after relabel, the slug still reads
   `E.Nim.Sml.Kmo` while its name no longer says "Kmoch". This is a
   cosmetic slug/name residue on a non-canonical (TT) node;
   acceptable. A slug rename is explicitly **not** done here (the
   user scoped this apply as "cap slug rename").

## Apply gating

Apply in a dedicated commit with explicit GO. This apply changes
nothing downstream beyond the `E.Nim.Sml.Kmo` relabel (the slug is
unchanged, so `canonical_ocn1` is stable; `chess-parquet` need only
pick up the new display name on regenerate). This preflight commit
changes nothing in `catalog/ocn-1.csv`.
