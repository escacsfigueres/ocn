# `named-after-person`: adversarial re-test of all 240 claims

**Status: analysis, nothing applied.** Re-test of
`docs/evidence/provenance/named-after-person.proposed.tsv` (240 claims over
224 slugs), run 2026-08-02 before any conversion. The re-test was asked for
because every evidence file in this project has so far asserted more than
its quotes prove; the question was whether that holds here too.

## Method: population, not sample

A 30-row sample was planned. It turned out to be unnecessary and weaker
than what the data allows. Each claim asserts exactly one thing, stated in
its own `note` column:

> catalogue name 'X' carries this person's name

That is mechanically checkable against the catalogue for **every** row, so
all 240 were tested rather than 30. For each claim the person's surname
(and, where present, forename) was normalised for diacritics and common
transliterations and looked for in the row's `canonical_name`, then in its
`aliases`.

## Result

| outcome | claims | share |
|---|---:|---:|
| name present in `canonical_name` | 172 | 71.7% |
| name present only in `aliases` | 20 | 8.3% |
| present in **neither** | 48 | 20.0% |
| person row missing | 0 | 0% |

**One claim in five does not assert what it says it asserts.** The failure
is not random: the 48 fall into three groups, and only the third is
worthless.

### Group A — the person is the eponym of a *different name for the same opening* (majority of the 48)

These are true and interesting naming facts, wrongly worded. OCN chose one
canonical name; the person is the eponym of another name for the same line:

| slug | OCN calls it | the person |
|---|---|---|
| `B.Pir` | Pirc Defence | Ufimtsev (Ufimtsev Defence in Russian usage) |
| `B.Mod.Std` | Modern Defence | Robatsch (Robatsch Defence) |
| `A.Tro` | Trompowsky Attack | Opočenský |
| `D.QPG.Ver` | Veresov Setup | Richter (Richter-Veresov Attack) |
| `D.QPG.Lev` | Levitsky Attack | Hodgson (Hodgson Attack) |
| `A.Sod` | Sodium Attack | Durkin (Durkin Attack) |
| `A.Van` | Van Geet Opening | Dunst (Dunst Opening) |
| `A.Kan` | Kangaroo Defence | Keres |
| `A.Mik` | Mikėnas Defence | Lundin |

Recording these as `named-after-person` on the current wording would be
false. Recording them as *what they are* — the same opening carrying a
different person's name in another tradition — is the naming divergence
this catalogue exists to document, and it is the same structural question
raised by Golombek on Reynolds/Klaus Junge and Abrahams/Noteboom (see
`winter-batch-03-findings.md`).

### Group B — the test's own blind spots, claims are sound

- `C.KPO.Nap` "Napoleon Opening" ← Bonaparte: the name carries the
  **forename**, not the surname.
- `E.Bog` "Bogo-Indian" ← Bogoljubov: the name is a **contraction**.
- `C.RyL` "Ruy López" ← López de Segura: OCN's name uses the person's
  first two names, the surname is dropped.

These pass on inspection; a substring test cannot see them.

### Group C — genuine defects, do not convert

- `C.Vie.Fal.MLn` "Vienna Falkbeer, Main Line" ← **Frankenstein's monster**
  and **Count Dracula**. Neither is a person, and the Frankenstein-Dracula
  is a specific line rather than this slug.
- `C.KPO.Ke2` "Bongcloud Attack" ← **Chess.com**: an organisation, not a
  person.
- `C.KPO.Kgt.Qe7` "Gunderam Defence" ← **"Master, International"**: not a
  person at all but a corrupted PGN name string, the same failure mode as
  `Marshall Viele, Fabrizio Aaron` and `Kushnir Aleksandr`.
- `B.CaK.Adv.Bot` "Botvinnik-Carls" ← Arkell and Khenkin: the
  Arkell/Khenkin line is a different node of the Caro-Kann Advance;
  attached to the wrong slug.

## Verdict

`survives with changes`, and the changes are not cosmetic.

1. **192 of 240 (80%) are convertible as written** — the 172 whose name is
   in the canonical name, plus the 20 whose name is in the aliases, if the
   `note` wording changes from "catalogue name X carries this person's
   name" to name-or-alias for the alias cases.
2. **Group A must not be converted under this relation** on its current
   wording. It is either a new relation (the opening is known by this
   person's name elsewhere) or an editorial decision about which name OCN
   should treat as canonical. That is a naming decision, not a source
   batch.
3. **Group C must be dropped**, and two of its rows are catalogue defects
   worth fixing independently: `Master, International` is a corrupted
   corpus string masquerading as a person, and Chess.com, Frankenstein's
   monster and Count Dracula do not belong in a table of people.

## What this says about the method

The triage was right about the relation (this *is* the designed slot for
"the opening carries this person's name") and right to refuse to invent
roles. It was wrong in the same direction as every previous evidence file:
the note claims a specific, checkable thing, and for one row in five it is
not true. The population test cost minutes and found what a 30-row sample
would probably have missed — Group C is four rows out of 240, and a sample
of 30 had a fair chance of drawing none of them.
