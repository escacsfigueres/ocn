# i18n alias DRAFT seeds — French (fr) + German (de)

**STATUS: UNREVIEWED DRAFT. NOT A LIVE LOCALE.**

These two files are *seeds* pending native-speaker review:

- `ocn-1.aliases.fr.tsv`
- `ocn-1.aliases.de.tsv`

They are **inert**: they live under `docs/drafts/i18n/`, not under
`catalog/`, so the integrity test (`tools/tests/test_i18n_aliases.py`,
which globs `catalog/ocn-1.aliases.*.tsv`) does **not** discover them and
no consumer reads them. They become live only via the promotion path
below, after a human review. Nothing here overrides the English
`canonical_name`, which stays definitive (English-fallback-by-design,
per `docs/i18n-aliases-design.md`).

## What these are

Same format and the **exact same slug coverage** as the live ca/es
pilots: TSV with columns `ocn1`, `name`; **58 data rows** each = the 5
class roots (A–E) + 53 depth-1 family heads. Coverage mirrors
`catalog/ocn-1.aliases.ca.tsv` / `.es.tsv` row-for-row (verified equal).

## How they were grounded (sources)

Names are **not invented**. Each is the established French / German
chess-literature form, derived from the ca/es seed and cross-checked
against the French and German Wikipedia opening articles. Casing follows
the design doc's per-locale convention:

- **fr**: French chess usage — adjective after the noun is lowercased
  ("Défense sicilienne", "Partie espagnole", "Ouverture anglaise");
  eponyms keep the person's capital ("Défense Caro-Kann", "Attaque
  Trompowsky"). Cyrillic names use French romanisation ("Défense
  Tchigorine").
- **de**: German nouns are capitalised; the conventional compound /
  attributive form is used ("Sizilianische Verteidigung", "Spanische
  Partie", "Damengambit", "Königsindische Verteidigung"). Cyrillic
  names use German romanisation ("Tschigorin", "Aljechin", "Weressow").

Key reference pages consulted (fr.wikipedia / de.wikipedia and the
linked per-opening articles):

- fr: `Liste_des_ouvertures_d'échecs`, `Défense_indienne`,
  `Défense_est-indienne`, `Défense_vieille-indienne`,
  `Défense_nimzo-indienne`, `Défense_semi-Tarrasch`, `Attaque_est-indienne`,
  `Défense_Benoni`.
- de: `Trompowsky-Eröffnung` (body: "heutzutage als Trompowsky-Angriff
  bekannt"), `Torre-Angriff`, `Tarrasch-Verteidigung`,
  `Tschigorin-Verteidigung`, `Albins_Gegengambit`, `Ponziani-Eröffnung`,
  `Vierspringerspiel`, `Mittelgambit`, `Königsindischer_Angriff`,
  `Altindische_Verteidigung`, `Richter-Weressow`.

## Notes on specific choices (for the reviewer)

- **D.QGD / D.QGA** (fr): rendered "Gambit dame refusé / accepté" per
  fr.wikipedia's ECO list. A reviewer may prefer "Gambit de la dame
  refusé/accepté"; both occur in French literature. Not flagged as
  uncertain (the chosen form is attested) but worth a glance.
- **B.Mod** (de): "Moderne Verteidigung" chosen; "Robatsch-Verteidigung"
  is a common synonym in German sources — reviewer to confirm house style.
- **A.Ver** (de): German spells the player "Weressow" →
  "Richter-Weressow-Angriff" (fr keeps "Veressov").
- **E.OldI**: fr conventional title is "Défense vieille-indienne"
  (fr.wikipedia), which intentionally differs from the ca/es
  "antiga/antigua". de is "Altindische Verteidigung".

## FLAGGED / uncertain rows — scrutinise these first

No row is a raw English fallback; every cell carries a real fr/de form.
The rows below are where the *conventional* native name is genuinely
ambiguous or where competing names exist, so a native reviewer should
confirm or replace them:

| slug | fr draft | de draft | why flagged |
|------|----------|----------|-------------|
| `A.Hng` | Ouverture hongroise | Ungarische Eröffnung | Hungarian Opening (1.g3) has no single dominant native title; fr "Ouverture hongroise" and de "Ungarische Eröffnung" are calques. de literature also uses "Benkö-Eröffnung" / "Königsfianchetto". **Confirm the house form.** |
| `A.Van` | Début Van Geet | Van-Geet-Eröffnung | Attested, but competes with "Dunst" / "Sleipner" / "Heinrichsen" in both languages. Confirm preferred eponym. |
| `D.STa` | Défense semi-Tarrasch | Halb-Tarrasch-Verteidigung | fr form confirmed (fr.wikipedia `Défense_semi-Tarrasch`). de "Halb-Tarrasch-Verteidigung" is the natural compound but the exact de.wikipedia title was **not** confirmed (only "Tarrasch-Verteidigung" was). **Verify the de form** (possibly "Semi-Tarrasch-Verteidigung"). |

Lower-confidence-but-attested (not in the table, listed for awareness):
`A.Ver` de spelling (Weressow vs Wereßow), `D.QGD`/`D.QGA` fr wording
variants noted above.

## Manual integrity check (performed)

Reusing the live test's rules (`tools/tests/test_i18n_aliases.py` +
`tools/validate.py::BANNED_CHAR_RE`) via a throwaway script — **NOT** a
wired-in test:

- header is exactly `ocn1`, `name` — OK (both)
- every slug exists in `catalog/ocn-1.csv` — OK (both)
- coverage equals the ca/es set, row-for-row — OK (58 rows each)
- no duplicate slugs — OK
- no empty names, no leading/trailing or double whitespace — OK
- no banned characters (middle dot, NBSP, zero-width, BOM, control) — OK
- no localized name accidentally equals the English canonical — OK

Result: **0 problems** on both drafts. The live ca/es sidecars, the live
test, and `catalog/ocn-1.csv` were not modified.

## Promotion path

1. Native fr and de reviewer corrects/approves each row (especially the
   flagged ones above), per the design doc's "seeds grow in reviewed lots,
   open to native correction" rule.
2. Move the approved file(s) from `docs/drafts/i18n/` to `catalog/`
   (`catalog/ocn-1.aliases.fr.tsv`, `catalog/ocn-1.aliases.de.tsv`).
3. Extend `tools/tests/test_i18n_aliases.py`: add `"fr"` / `"de"` to the
   `test_pilot_locales_exist` expected set so the new locales are
   integrity-gated like ca/es. (`test_sidecars_are_sound` already covers
   any `catalog/ocn-1.aliases.*.tsv` automatically.)
4. Run `python3 -m unittest tools.tests.test_i18n_aliases` — must stay
   green — then commit as a reviewed lot.
