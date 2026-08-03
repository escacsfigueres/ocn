# Open decisions, 2026-08-03

Everything currently waiting on a human, in one place, with a
recommendation for each. Nothing here is applied. Written after a day in
which five commits landed (CI green throughout) and `attributed_to` went
from 71 to 126 rows.

## A. Two batches at the door — DONE

Applied 2026-08-03 05:15 as `d5501e2`, CI green. `winter-batch-04`
(Dragon, Kalashnikov, Löwenthal) and `winter-batch-05` (Marshall Attack).
A fourth row (Fort Knox) was drafted and dropped when `--strict` refused
it at PARTIAL — the guardrail was right. `historical_notes` now stands at
79 rows, `attributed_to` at 126.

## B. The QID packet — MOSTLY DONE

Applied 2026-08-03 05:25 as `3940c5d`, CI green: 60 of 61 rows carry a
QID with dates, 16 display names corrected, one row left null on purpose,
Gukesh D kept against the proposal. Record:
`docs/evidence/people/identity-fill-record.md`.

**Still open from this block:** the merges (deferred deliberately — see
the record; the duplicates are now annotated and machine-detectable), the
182-row additions file with its non-persons, and the greco/harrwitz date
divergences.

The original decision list follows for reference.

Independently cross-checked: the repo's own `tools/resolve_people.py`
agrees with the external packet on **57 of 61 rows, with zero conflicting
QIDs**. The four differences are all rows whose corpus spelling is
corrupt, which is the repo tool refusing by design.

| # | decision | recommendation |
|---|---|---|
| 1 | Five merges: aljechin→alekhine, bogoljubov→bogoljubow, bikova→bykova, master→gunderam, marshall-viele→marshall | **Merge all five.** The marshall case is no longer a coin flip: the catalogue has no `marshall` row, and `marshall-viele` carries the 1907 Lasker world championship match (15 games), which is Frank Marshall as historical fact. "Marshall Viele, Fabrizio Aaron" is a modern player's name string attached to 1907 games by the source database — the same failure as "Kushnir Aleksandr" |
| 2 | Kushnir | **Non-negotiable: the QID and the display name "Kushnir, Alla" land in the same commit.** Otherwise the champion's challenger stays labelled with a man's forename |
| 3 | 13 name corrections (PGN middle initials, `Hou, Yifan(HLJ)`, `Capablanca, Jose` → `José Raúl`, `Forgacs, Leo` → `Forgács, Leó`) | **Apply.** These are corpus artefacts, and consistent with the repo's own diacritic work |
| 4 | `gukesh-d`: "Gukesh D" → "Dommaraju, Gukesh" | **Keep "Gukesh D".** Wikidata's label ordering is not chess practice; FIDE and every broadcast use Gukesh D. If we want surname-first everywhere, make it a stated rule rather than an import side-effect |
| 5 | The 182-row additions file, containing Chess.com (Q16829376), Frankenstein's monster (Q2021531) and Count Dracula | **Decide separately from the 61-row fill, and drop the non-persons.** A table called `people` should contain people |
| 6 | Dates: greco (1634 vs 1630), harrwitz (1821 vs 1823) | Both historically uncertain. **Leave as they are and note the divergence** rather than picking a side without a source |
| 7 | dunst vs Van Geet; worrall vs wormald | Naming decisions, not identity ones. See D below |

## C. `named-after-person`: 240 claims, re-tested over the whole population

Not a sample. Each claim asserts one checkable thing — "catalogue name X
carries this person's name" — so all 240 were tested against
`canonical_name` and `aliases`.

| outcome | claims |
|---|---:|
| name in the canonical name | 172 |
| name in the aliases only | 20 |
| in neither | 48 |

**Recommendation: convert the 192, drop four, park the rest.**

- **Convert 192** (172 + 20), changing the note wording for the alias
  cases from "catalogue name carries" to name-or-alias.
- **Drop 4 defects**: Count Dracula and Frankenstein's monster on the
  Vienna Falkbeer, Chess.com on the Bongcloud, and "Master, International"
  on the Gunderam — the last being another corrupted PGN string
  masquerading as a person.
- **Park the rest of the 48**: these are people who are the eponym of a
  *different name for the same opening* (Pirc/Ufimtsev, Modern/Robatsch,
  Veresov/Richter, Sodium/Durkin, Van Geet/Dunst). True and interesting,
  but not the claim as written. See D.

## D. Naming decisions the sources raised but cannot settle

These need a position, not more evidence.

1. **Openings that carry different people's names in different
   traditions.** Golombek recorded that the Semi-Slav's Reynolds variation
   is the Klaus Junge line to Germans, and the Abrahams the Noteboom to
   the Dutch. OCN currently carries Noteboom as the head with Abrahams and
   Junge beneath it, which encodes one national tradition as the parent of
   the others. The same question governs the parked group in C.
   *Recommendation: a relation for "known as the N Variation in tradition
   T", so the catalogue can record divergence instead of choosing.*
2. **`B.Sic.Kal` carries "Sicilian Defense: Löwenthal Variation" among its
   aliases** while `B.Sic.Loe` is the Löwenthal proper — the exact
   nineteenth-century confusion Winter documents, now encoded in the alias
   table. *Recommendation: drop the alias, keep the confusion in the
   note where it is explained.*
3. **`notable-games.tsv`** (19,860 games): no relation in the chronicle's
   closed set describes it honestly. *Recommendation: a sidecar,
   `catalog/ocn-1.games.tsv`, not claims.*

## E. Outward-facing

- **The chessgames.com letter** is drafted at
  `~/Downloads/2026-08-02-chessgames-permission-email.md`. It explains
  what OCN is and why, offers deep links per opening, the catalogue itself
  (it is CC-BY), and credit to their kibitzers as provenance; it leaves
  the "how" entirely to them. Three independent models recommended sending
  it. Nothing is sent without a human.
- The harvest cron is paused with a two-week tripwire pending their reply.

## F. A caution about the pre-chewed batch cards

The dossier's batch cards pre-extract naming phrases, years and person
hints per slug. Useful, but they inherit the routing: the first card in
the file, `B.Nim.ScD.exd5.Qxd5.Nc3` (Nimzowitsch Scandinavian), is fed
eleven Marshall Gambit items that belong to the Ruy López. Pre-chewing
speeds up drafting in the wrong direction too, so the drafting step still
has to check the moves rather than the label — which is how batch 5 came
out as one row instead of five.
