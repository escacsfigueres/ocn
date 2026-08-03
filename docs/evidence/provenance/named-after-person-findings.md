# `named-after-person` — proposal and findings

Draft output of the evidence-conversion pass over
`docs/evidence/eponyms/named-after-people.tsv` (228 rows). **Nothing here is
applied.** Two proposal files sit beside this one:

- `named-after-person.proposed.tsv` — 240 claims over 224 slugs
- `people-proposed-additions.tsv` — 182 new person entities

## Why these are claims, not attributions

The file has **no `role` column**, and 202 of its 228 citations are Wikipedia
`<ref>` blobs pointing at chessgames.com, chess.com and 365chess.com. It
establishes *the opening carries this person's name*. It does **not** establish
*this person originated / popularised / published it*.

Feeding it into `attributed_to` would require inventing a role the evidence
does not state — the same failure found in the Companion pass, but systematic
rather than occasional. `named-after-person` is already in the chronicle
layer's closed relation set (`docs/chronicle-layer-design.md`, "the opening
carries this person's name") and has **zero rows**, so this is filling a
designed slot, not extending the schema.

## Three findings from the released catalogue

### 1. Two wrong forenames in `catalog/ocn-1.people.tsv`

Both shipped in 1.3.0, both verified against `catalog/ocn-1.wch.tsv`:

| person_id | catalogue says | should be | evidence |
|---|---|---|---|
| `karpov` | Karpov, Aleksandr | Karpov, **Anatoly** | 183 WCh games, 1978–1996 |
| `smyslov` | Smyslov, Vladimir | Smyslov, **Vasily** | 69 WCh games, 1954–1958 vs Botvinnik |

Both rows carry `note: identity unverified` and an empty `wikidata_qid`, so the
file is honest that it was never checked — but the display name is still what a
consumer reads.

### 2. All 61 person entities are orphans

No claim in `catalog/ocn-1.claims.tsv` has `subject_type=person`. The existing
relations point at `place` (119), `name` (259) and `event` (733). The README
describes `ocn-1.people.tsv` / `ocn-1.events.tsv` as "the entities those claims
point at"; for people that is currently false. This proposal would make 13 of
the 61 load-bearing.

### 3. Surname slugs are not a safe person key

Four collisions, each needing a ruling a heuristic cannot make:

| name in evidence | ruling | id |
|---|---|---|
| Weaver W. Adams | **distinct** from Michael Adams | `adams-weaver` |
| Alexander Zaitsev / Igor Zaitsev | **distinct** from each other | `zaitsev-alexander` / `zaitsev-igor` |
| Bobby Fischer | **same** as Fischer, Robert J | reuse `fischer` |
| Anatoly Karpov / Vasily Smyslov | **same** as the catalogue rows, which are misnamed | reuse `karpov` / `smyslov` |

A forename-mismatch heuristic gets the first two right and the last two exactly
backwards, because a diminutive and a data error both look like a mismatch.

## Open decisions

- Adopting `-forename` suffixes only on collision leaves the key scheme
  inconsistent (`fischer` beside `adams-weaver`). The alternative is suffixing
  everyone, which churns the 13 existing referenced ids.
- 182 new entities would all carry `identity unverified` and no QID. Whether to
  land them unverified or gate on a Wikidata resolution pass first is editorial;
  `docs/evidence/people/wikidata-resolution.tsv` exists but was not consulted here.
