# i18n alias sidecars (Track 2)

**Status**: pilot seeded 2026-06-12 (Catalan + Spanish, class roots +
~55 depth-1 families each). Sidecar-only — the catalogue and its
14-column schema are untouched; the English `canonical_name` stays
definitive.

## Format

One TSV per locale: `catalog/ocn-1.aliases.<locale>.tsv`, columns
`ocn1`, `name`. **Partial coverage is by design**: a consumer renders
the localized name when the slug is present, otherwise falls back to
the English canonical (which is always correct). Integrity is enforced
by `tools/tests/test_i18n_aliases.py`: slugs must exist, no duplicates,
no banned characters or stray whitespace.

## Naming conventions per locale

- **ca**: Catalan capitalisation (first word only: "Defensa siciliana",
  "Obertura espanyola"); Cyrillic names follow Catalan romanisation
  ("Defensa Txigorin").
- **es**: Spanish chess-literature casing ("Defensa Siciliana",
  "Apertura Española"); Cyrillic names follow Spanish convention
  ("Defensa Chigorin").
- Diacritics policy is the catalogue's (person orthography decides);
  C.RyL is "Obertura espanyola" / "Apertura Española" per native usage,
  with the person's name available via the English canonical.

## Growth path

Seeds grow per family, in reviewed lots like everything else (the seed
itself is open to native-speaker correction — flag anything off).
Deeper rows can be derived semi-mechanically later (family name +
translated qualifier vocabulary), but only under review: literal
translation of established line names is exactly the kind of truth a
human gates. New locales = new file + the pilot test set updated.
