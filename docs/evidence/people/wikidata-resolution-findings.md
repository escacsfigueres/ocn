# Wikidata identity resolution — results

Output of a 16-agent parallel pass over all 243 OCN person entities: the 61 already
in `catalog/ocn-1.people.tsv` plus the 182 proposed in
`../provenance/people-proposed-additions.tsv`. Full data in `wikidata-resolved.tsv`.
**Nothing is applied.**

Agents were forbidden from guessing a QID — a wrong QID corrupts a reference
catalogue silently, so `null` was the required answer whenever a page could not
actually be loaded and read.

## Numbers

| confidence | count |
|---|---:|
| high | 226 |
| medium | 4 |
| not-found | 13 |

230 QIDs, none malformed.

## The case for dropping surname keys

**98 of 243 people (40%) share a surname with another notable chess figure.**
That is not an edge case to patch with suffixes; it is the majority condition of
the domain. A QID is a globally unique key and ends the problem outright.

| id | resolved | hazard found |
|---|---|---|
| `sveshnikov` | Evgeny, `Q675955` | Vladimir Sveshnikov `Q24027558` is **his son** |
| `kasparov` | Garry, `Q28614` | Sergey Kasparov `Q3918615`, **unrelated** |
| `zaitsev-alexander` | `Q1339147` | Igor Zaitsev `Q1657668` owns the Ruy López line |
| `adams-weaver` | `Q983313` | Michael Adams `Q299636` is "regularly and wrongly credited" |

## Five duplicate identities

One human, two catalogue entities. All five are artefacts of surname slugging:

| QID | ids that collapse | cause |
|---|---|---|
| `Q131374` | `alekhine`, `aljechin` | transliteration |
| `Q57310` | `bogoljubow`, `bogoljubov` | transliteration |
| `Q253772` | `bykova`, `bikova` | transliteration |
| `Q312814` | `marshall`, `marshall-viele` | a false split introduced by disambiguation — **the two agents disagree**: one argues the rows must not converge, the other shows every `marshall-viele` game is the 1907 Lasker match. The event evidence favours the merge, but a human should rule |
| `Q1512937` | `gunderam`, `master` | `master` is a source-text artefact, not a person |

## The three known errors, confirmed and fixed

| id | was | is | QID |
|---|---|---|---|
| `karpov` | Karpov, Aleksandr | Karpov, **Anatoly** | `Q131674` |
| `smyslov` | Smyslov, Vladimir | Smyslov, **Vasily** | `Q104148` |
| `segura` | Segura, Ruy | **López de Segura, Ruy** | `Q297457` |

## Non-persons found in the proposal — five, and the dangerous two are not the obvious ones

| id | actually is | opening | outcome |
|---|---|---|---|
| `monster` | Frankenstein's monster | Vienna Falkbeer | **QID assigned**, `Q2021531`, medium |
| `chesscom` | the website Chess.com | Bongcloud Attack | **QID assigned**, `Q16829376`, medium |
| `dracula` | Count Dracula | Vienna Falkbeer | not-found |
| `master` | "Master, International", a parse artefact | Gunderam Defence | correctly resolved to the real eponym |
| `morrison` | a corrupt PGN header, 10 catalogue rows | none | not-found |

`monster` and `chesscom` are the ones to watch. Both received a QID at medium
confidence, and both matches are *technically correct* — `Q2021531` really is Mary
Shelley's creature, `Q16829376` really is chess.com. A resolved-but-wrong entity
passes review in a way a null never does.

One real naming fact hides in here: the Frankenstein-Dracula Variation genuinely
is named for the two fictional characters, coined by Tim Harding in 1976. That is
a legitimate naming claim — it simply is not `named-after-person` pointing at a
person entity, and would need a different `subject_type`. The Bongcloud is not
named after chess.com at all.

## Unresolved (13)

Genuine gaps, not failures: `hopton`, `zilbermints`, `lamb`, `parham`, `gusev`,
`jerome`, `dory`, `vinogradov`, `worrall`, `adler`, `desprez` and the two
non-persons above. Several are minor 19th-century amateurs with no Wikidata item.
The agents explicitly declined tempting near-matches — `vinogradov` carries a
"DO NOT USE" note against the obvious wrong candidate, and `gusev` was left open
rather than matched to a likely-but-unverified namesake.

## What this unblocks

`wikidata_qid` becomes the identity key and `person_id` degrades to a human-readable
handle. Then `adams` beside `adams-weaver` stops being an inconsistency, because the
slug is no longer carrying identity. The five duplicates merge, the three wrong names
correct, and the three non-persons drop out before they ever reach the catalogue.
