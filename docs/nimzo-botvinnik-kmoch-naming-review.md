# Nimzo Botvinnik/Kmoch — naming review

**Status**: REVIEW COMPLETE → **APPLIED** (Option B). The
recommendation was applied: `E.Nim.Sml.Kmo.transposes_to =
E.Nim.Sml.Bot` + the spurious "Kmoch" dropped (relabelled "a3 Move
Order"). The Nimzo Bot/Kmo group is resolved (single_canonical);
the only remaining unresolved group in the whole catalogue is now
QID Miles/Petrosian. See
[`nimzo-botvinnik-kmoch-apply-preflight.md`](nimzo-botvinnik-kmoch-apply-preflight.md).
Resolves the bibliographic question behind the (formerly) ON-HOLD
Nimzo Bot/Kmo group (`E.Nim.Sml.Bot ⇄ E.Nim.Sml.Kmo`). Companion to
[`nimzo-saemisch-botvinnik-kmoch-proposal.md`](nimzo-saemisch-botvinnik-kmoch-proposal.md).

## Sources consulted

| source | availability | role |
|---|---|---|
| **Lichess opening DB** (`external/lichess-openings/*.tsv`, in-repo) | ✅ used | **decisive** — this is the dataset OCN imported its opening names from, so it is authoritative for "what does this slug's name come from" |
| OCN catalogue (`catalog/ocn-1.csv`) | ✅ used | internal cross-check |
| General ECO / opening-theory knowledge | ✅ used | labelled as inference, corroborating only |
| **NotebookLM — `nlm` CLI** (albertpi@gmail.com, 93 notebooks) | ✅ **used** | secondary corroboration. The **MCP** server was unusable (`authenticated:false`, 0 notebooks), but the `nlm` CLI works — queried Q25 (Editorial chess: Quality/Gambit/Everyman/Thinkers, 123 sources) and Q30a (Telegram chess library, 207 sources). Findings below corroborate the Lichess conclusion. |

### NotebookLM evidence (via `nlm` CLI — secondary, corroborating)

Queried the opening-book corpora for the Kmoch/Botvinnik Nimzo
naming. Both notebooks point the same way as Lichess:

- **Q30a (Telegram chess library)** — *"the sources do not attribute
  any specific Nimzo-Indian variation to [Kmoch]"* (he is mentioned
  only as a player); the `4.a3 Bxc3+ 5.bxc3` doubled-pawn line "which
  frequently features f3" is *"explicitly identified as the **Sämisch
  Variation**"*; and *"Botvinnik worked out specific plans … involving
  f2-f3 and e3-e4"* (the *Magnus Method* even calls `19.f3` "the
  Botvinnik plan" in the Rubinstein Nimzo).
- **Q25 (Editorial: Quality/Gambit/Everyman/Thinkers)** — citations
  surface Botvinnik's own Nimzo games (Botvinnik–Chekhover 1938) and
  the doubled-pawn Sämisch context, but **no source names a "Sämisch
  Kmoch"**; "Botvinnik Variation" in this corpus most often refers to
  the *Semi-Slav* Botvinnik or the *English* Botvinnik System
  (different openings — corpus noise, not the Nimzo Sämisch).

**Net**: the book corpus does **not** attest "Kmoch" as a Nimzo
Sämisch variation name, identifies the doubled-pawn line as the
**Sämisch**, and ties **Botvinnik** to the f3/e4 plan — fully
consistent with the Lichess finding (Kmoch = 4.f3 only; the Sämisch
f3-tabiya = Botvinnik; no "Sämisch Kmoch"). NotebookLM does not
overturn anything; it reinforces Option B.

## Evidence table

### External (Lichess opening DB — authoritative for OCN naming)

| eco | Lichess name | line | what it establishes |
|---|---|---|---|
| **E20** | **Nimzo-Indian Defense: Kmoch Variation** | `1.d4 Nf6 2.c4 e6 3.Nc3 Bb4 4.f3` | **"Kmoch" = the direct 4.f3 move.** Decisive. |
| **E24** | **Nimzo-Indian Defense: Sämisch Variation, Botvinnik Variation** | `…4.f3 d5 5.a3 Bxc3+ 6.bxc3 c5 7.e3 O-O 8.cxd5 Nxd5` | The Sämisch doubled-pawn f3-line is **"Botvinnik"**, not "Kmoch". |
| E25 | Nimzo-Indian: Sämisch Variation [+ Keres, Romanovsky] | `…4.f3 d5 5.a3 Bxc3+ 6.bxc3 c5 7.cxd5 …` | The f3-Sämisch region is "Sämisch"/"Botvinnik"/"Keres"/"Romanovsky" — **never "Kmoch"**. |
| E26 | Nimzo-Indian: Sämisch Variation [+ O'Kelly] | `…4.a3 Bxc3+ 5.bxc3 c5 6.e3 [b6]` | The a3-route to the Sämisch is plain **"Sämisch"** (O'Kelly for …b6) — **no "Kmoch" sub-name**. |
| — | (absence) | grep `kmoch` across all Lichess `*.tsv` | The **only** Nimzo "Kmoch" is E20 (4.f3). There is **NO** "Nimzo Sämisch Kmoch" and **NO** "Nimzo Rubinstein Kmoch" anywhere in Lichess. |

(For completeness, "Kmoch Variation" elsewhere in Lichess is a
different opening each time: D41 Semi-Tarrasch, C41 Philidor Hanham,
B02 Alekhine — none is the Nimzo Sämisch.)

### Internal (OCN catalogue)

| slug | name / alias | eco | verdict vs Lichess |
|---|---|---|---|
| `E.Nim.Fou` | "Nimzo, 4.f3" / alias **"Kmoch Variation\|4.f3 System"** | E20 | ✅ **CORRECT** — matches Lichess E20 (Kmoch = 4.f3). |
| `E.Nim.Sml.Bot` | "Nimzo Sämisch, **Botvinnik**" | E24/E25 | ✅ **CORRECT** — matches Lichess E24 (Sämisch Botvinnik, f3-line). |
| `E.Nim.Sml.Kmo` | "Nimzo Saemisch, **Kmoch** Variation" | E26 | ❌ **ARTIFACT** — Lichess has no "Sämisch Kmoch"; this is the a3-route into the Botvinnik FEN, mislabelled "Kmoch". |
| `E.Nim.Rub.Kmo` | "Nimzo Rubinstein, **Kmoch** Variation" | E40 | ❌ **ARTIFACT** (pre-existing, separate group) — Lichess has no "Rubinstein Kmoch"; Kmoch = 4.f3. |

### Inference (general ECO/theory — corroborating only)

ECO E20 is traditionally the Kmoch (4.f3 / "Kmoch System"). The
doubled-c-pawn Sämisch tabiya with an early …c5/…d5 is commonly
attributed to **Botvinnik** in modern references. Both align with
Lichess. (Labelled inference; the Lichess DB is the binding source.)

## Answers to the review questions

1. **Does "Kmoch Variation" designate 4.f3 directly?** **Yes,
   decisively.** Lichess E20 = "Nimzo-Indian: Kmoch Variation" =
   `4.f3`. OCN's `E.Nim.Fou` already encodes this correctly.

2. **Are "Botvinnik" and "Kmoch" independent names for the same
   Sämisch FEN, or is one an artifact?** **One is an artifact.**
   Lichess names the Sämisch f3-tabiya **"Botvinnik"** (E24).
   "Kmoch" is a *different* line (4.f3 itself, E20). The OCN
   `E.Nim.Sml.Kmo` "Kmoch" label on the depth-3 Sämisch position is
   not a genuine second name — it is a misattribution.

3. **Is `E.Nim.Sml.Kmo` a real literary identity or a mislabelled
   slug?** **Mislabelled.** It is the *a3-first move order* into the
   Botvinnik tabiya (`4.a3 … c5 6.f3 d5`). The move order is real;
   the **name "Kmoch" is wrong** (Kmoch belongs to 4.f3). Note its
   only child `E.Nim.Sml.Kmo.MLn` is itself the plain E26 Sämisch
   e3 line (`…c5 e3`) and does **not** even extend its parent's
   moves (`…c5 f3 d5`) — a secondary parent-chain quirk to fix at
   apply time.

4. **Is the precedent `E.Nim.Sml.Bot.MLn ⇄ E.Nim.Rub.Kmo`
   coherent?** **Position-equivalence yes; the "Kmoch" label no.**
   The two slugs share the FEN (the `same_as` is sound), and
   `Bot.MLn` ("Botvinnik Main Line") is correctly named. But
   `E.Nim.Rub.Kmo`'s "Kmoch" is the *same artifact* (no Lichess
   "Rubinstein Kmoch"). The `same_as` links a correct name to a
   mislabelled one — flag for a **follow-up relabel**, but it is
   pre-existing and lower priority than the active hold.

5. **Recommended action.** **Option B — single canonical Botvinnik;
   `E.Nim.Sml.Kmo` transposes_to `E.Nim.Sml.Bot`, and drop the
   spurious "Kmoch" name.** (Details below.)

## Recommendation: Option B (single_canonical) + relabel

`E.Nim.Sml.Bot` is the correct Lichess/ECO name for this Sämisch
f3-tabiya and is the more developed node (3 children vs 1).
`E.Nim.Sml.Kmo` is the a3-move-order transposition into it, wearing
a wrong name. So:

```
E.Nim.Sml.Kmo.transposes_to = E.Nim.Sml.Bot
```
plus **relabel** `E.Nim.Sml.Kmo` to remove "Kmoch" (e.g. canonical
name → "Nimzo Sämisch, a3 move order" or similar neutral
descriptor; the slug segment `.Kmo` should likewise be reconsidered
at preflight, since it encodes the wrong name).

### Options rejected

- **A — `same_as` bilateral (Bot ⇄ Kmo)**: ✗ would enshrine
  "Kmoch" as a co-equal name for this FEN, but Lichess shows it is
  not a name for this position at all (it is 4.f3). `same_as` is
  for two *genuine* names; here there is one (Botvinnik).
- **C — relabel only (keep as its own node)**: ✗ a relabel alone
  leaves the duplicate FEN group unresolved; it must be combined
  with the `transposes_to` of Option B anyway.
- **D — defer further**: ✗ the bibliography is now decisive (Lichess
  E20 vs E24). Nothing more to research.

## Status change

This group moves from **"ON HOLD — naming review pending"** to
**"REVIEWED — bibliography decisive; ready for a preflight + apply
sprint"**. It is **not** applied here. Like QID, the apply needs a
short preflight because it involves:
- a `transposes_to` + a `canonical_name` relabel (and possibly a
  slug rename `.Kmo` → neutral),
- the `E.Nim.Sml.Kmo.MLn` parent-chain quirk (it is really the E26
  Sämisch e3 line),
- a **follow-up** decision on the related `E.Nim.Rub.Kmo` artifact
  (relabel its "Kmoch"; review its `same_as` with `Bot.MLn`).

## Expected impact (if Option B applied in a future sprint)

| metric | now | after B | Δ |
|---|---|---|---|
| catalogue rows | 5,900 | 5,900 | 0 (transposes_to + relabel; no delete) |
| unresolved_groups | 2 | **1** | −1 (then only QID would remain unresolved) |
| multiple_canonical_groups | 17 | 17 | 0 (single_canonical, not multi) |
| `canonical_ocn1` downstream | — | relabel of `E.Nim.Sml.Kmo` (+ maybe a slug rename) | needs the preflight to scope |

After Option B, the only unresolved group left would be QID
Miles/Petrosian (already preflighted). The broader "Kmoch
over-application" (the `E.Nim.Rub.Kmo` artifact) would be a small
follow-up, independent of the duplicate-group count.

## Recommended next step

Treat the bibliographic question as **settled** (Kmoch = 4.f3;
the Sämisch f3-tabiya = Botvinnik). The apply is fully specified in
[`nimzo-botvinnik-kmoch-apply-preflight.md`](nimzo-botvinnik-kmoch-apply-preflight.md)
(the `transposes_to` + relabel, the `Kmo.MLn` relabel, the `Rub.Kmo`
follow-up marked out of scope, and a verification checklist). Apply
in a dedicated, GO'd commit. This review commit changes nothing in
`catalog/ocn-1.csv`.
