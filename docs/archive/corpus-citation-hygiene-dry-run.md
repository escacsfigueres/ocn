# Corpus-citation hygiene — dry-run record (APPLIED)

**Status: APPLIED 2026-07-29** (traction-roadmap H0.4). Manifest:
[`../manifests/corpus-citation-hygiene.manifest.json`](../manifests/corpus-citation-hygiene.manifest.json),
mode `attribution_fields_only`, 10 rows changed.

- Catalogue sha256 before: `41eb3374aeff4e5122974ce6de4ff0349736f12a061565eeeba9051b77cff1b3`
- Catalogue sha256 after:  `091b9b6269404ff7beebbb9239047854fd5abead07ab7326be633f29bc10bd16`
  (apply matched the dry-run prediction byte for byte).

What changed:

- **Nine rewords** (A.Tro, B.Ale, B.Sic.Naj.Pol, B.Sic.Ros, B.Sic.Sve,
  C.RyL.Ber.Wal.End, C.RyL.Mar, D.Cat, D.Sem.Mer): every reference to
  "the corpus" (an unpublished game collection) removed. Claims are
  unchanged; the evidence now cites only public, dated master games and
  published works, all checkable in public databases. Two rows also lost
  corpus-derived player statistics that carried no attribution value.
- **One withdrawal** (B.Sic.Sve.Bxf6.Nd5.Bg7, the Novosibirsk 10...Bg7
  line): the corpus was the load-bearing source, and the row's own notes
  conceded it did not support first-play. All three attribution fields
  cleared; the head returns to the re-sourcing backlog under the H4.4
  graded-evidence policy. Attributed rows: 27 -> 26.
- **Maroczy trio kept as-is** (deliberate): their byte-identical source
  string is the same reference legitimately supporting the same claim on
  three move orders; per-row context already lives in historical_notes.
- **Validator check added**: attribution fields now fail validation on
  unverifiable-source patterns (corpus, Gigabase, private database) —
  `UNVERIFIABLE_SOURCE_RE` in `tools/validate.py`, with fixture
  `invalid_unverifiable_source.csv`. Suite: 286 tests green.

Both derived sidecars regenerated after the apply.
