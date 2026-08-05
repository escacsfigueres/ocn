# The names Lichess already gave us

**Status: 155 applied 2026-08-05; 30 parked on a policy question.** Companion
to `docs/manifests/lichess-exact-aliases.manifest.json`.

## Why

2,144 of 5,899 rows carried no alternative name at all. The monograph argues
this is the catalogue's most consequential weakness, worse than being wrong: a
reader searching the name their own source uses does not find us, and a missing
name is invisible where a wrong one gets argued with.

Most of that gap needs research. Part of it did not, because the answer was
already in the repository. Every row cross-references
`lichess-org/chess-openings` in `catalog/ocn-1.lichess-xref.tsv`, and Lichess's
name is the one millions of players actually see.

## Five filters, and what each one is for

| filter | rows left | why |
|---|---:|---|
| rows with no alias at all | 2,144 | the gap being closed |
| a Lichess name exists and differs from ours | 2,105 | 39 already agree |
| **exact position match only** | 367 | a prefix match names a *shallower* line; importing it would give dozens of rows one alias and identify nothing |
| the name identifies exactly one row in the cross-reference | 186 | Lichess reuses names across positions |
| no ASCII-folded eponym | 156 | see below |
| not already another row's canonical name or alias | **155** | the registrar guard rejects cross-row collisions |

Two of those filters exist because the repository's own guards refused the
batch and were right to. The diacritic validator rejected `Ruy Lopez: …`, and
the alias registrar rejected giving `C.KPO.b3` the string *King's Pawn
Opening*, which is the canonical name of `B.KPG`.

Applied with `--validate --strict`: 5,899 rows before and after, 155 changed,
validator clean. Rows with no alias: **2,144 to 1,989**.

## The 30 that are parked, and why it is a policy question

They are held back by `BANNED_ASCII_NAME_FORMS`: 28 contain `Lopez` and two
contain `Moeller`, where the catalogue requires `López` and `Møller`.

The diacritic policy is right and this is the one place it works against
itself. `docs/diacritic-normalization-map.md` states the intent as *"OCN-1
**canonical names** must spell eponym surnames the way the person spelled
them"*, and cites the spec's definition of `canonical_name`. The validator
applies the same rule to `aliases`.

But the two fields have opposite jobs. A canonical name says how a thing
**should** be written. An alias says how it **might be searched for** — which
is why the column already holds `Modern Defense`, an American spelling that is
not how anyone would argue the name should be set. Forbidding `Ruy Lopez` in
aliases guarantees that the catalogue cannot be found by the spelling almost
every database, book index and search box in the world actually uses, including
Lichess's own.

**The question for a human:** should the diacritic rule bind `canonical_name`
only, with `aliases` free to carry the ASCII form precisely so it can be
matched? Three ways to go:

1. **Narrow the rule to `canonical_name`.** The alias column becomes a lookup
   surface, and 28 Ruy López rows plus two Møller rows gain the string people
   type. Costs nothing in how the catalogue presents itself.
2. **Keep the rule and normalise on import.** The aliases become `Ruy López:
   Open, Main Line`, which no Lichess user will ever type. This is the current
   behaviour and it is why the 30 are parked.
3. **Add a separate `search_forms` column.** Correct, and it is a schema change
   affecting every consumer and the published packages.

The recommendation is (1), on the grounds that an alias nobody searches for is
not an alias. It is recorded here rather than acted on because the diacritic
policy was applied deliberately, in three tiers, under explicit GO, and
narrowing it is not a decision to take inside an import.

## What this does not solve

1,989 rows still carry no alternative name, and the 1,738 prefix matches are
not a source for them: a name that describes a shallower line is not a name for
this one. Those need the thing the README now asks readers for — the name they
use and where they got it. See [[ocn-open-decisions-sheet]] and the `known-as`
relation, which is where a sourced second name belongs when it comes with an
argument rather than a cross-reference.
