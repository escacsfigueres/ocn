# Naming audit proposal — `B.Fre.Win` (French, Winawer)

**Status**: **PROPOSED — no catalogue change.** Closes the one PARTIAL
candidate left from the Group-B evidence sprint. Source-gated like every
prior apply. It applies nothing.

**Scope fence**: a *naming* audit. It touches only `attributed_to` /
`attribution_source` / `historical_notes` on the **head row `B.Fre.Win`**.
No child rows, no `transposes_to`/`same_as`/`moves_uci`/`parent_ocn1`/etc.

## The entry under audit

```
B.Fre.Win | "French, Winawer"  (ECO C15|C16|C17|C18|C19)
  parent  = B.Fre   depth=2   flags=sharp
  moves   = 1.e4 e6 2.d4 d5 3.Nc3 Bb4
  aliases = (empty)   notes = "3.Nc3 Bb4."
  attributed_to / attribution_source / historical_notes : ALL EMPTY (verified)
```

Multi-opening surname risk: "Winawer" appears in 59 rows, but `B.Fre.Win`
is the **dominant primary head** (the others are reuses, e.g. a Three
Knights line). Head row only.

## Evidence

| # | source | exact claim | quality | supports |
|---|---|---|---|---|
| 1 | Wikipedia *French Defence* (fetched) | *"The Winawer Variation, named after Szymon Winawer and pioneered by Aron Nimzowitsch and Mikhail Botvinnik, is one of the main systems in the French."* | secondary, **no inline ref** | naming + popularizers |
| 2 | Wikipedia *Szymon Winawer* (fetched) | *"Several chess openings are named after him, most notably the Winawer Variation of the French Defence (1.e4 e6 2.d4 d5 3.Nc3 Bb4)."* Winawer 1838–1919, 19th-c master | secondary, no inline ref | naming; dates |
| 3 | Multiple instructional sites (frenchdefense.org, ppqty, chesspathways, chess.com, 365chess) | all state the line is named after Szymon Winawer; popularised by Nimzowitsch/Botvinnik | secondary, corroborating | breadth of attestation |
| 4 | **Lumbra Gigabase** (prior chronology sprint, verified) | 3…Bb4 in the corpus from **Paulsen 1861**; Winawer's own earliest **Steinitz–Winawer, Paris 1867** (as Black); Nimzowitsch from 1921, Botvinnik from 1927 | first-hand corpus | chronology (idea predates eponym; Winawer = early practitioner) |
| 5 | Oxford Companion to Chess (Hooper & Whyld), 'Winawer' entry | would be the reference-grade naming source | **NOT read this run** | — (the gap) |

**Honesty note:** the naming claim is **universally attested and
uncontested**, but — exactly as in the original Group-B grade — **no
reference-grade source (Oxford Companion entry / monograph chapter /
Winter article) was quoted first-hand this run.** What is first-hand: the
multiple secondary attestations (#1–3) and the dated corpus game #4. This
is the same evidence *shape* already accepted for the applied **Marshall
Attack** row (secondary naming attestation + a verified dated game), and
weaker only in that Marshall's anchoring game is famous while Winawer's
1867 game is merely his earliest corpus use.

## Source-read attempt 2 (2026-05-30)

A second, focused attempt to lift this from PARTIAL to CLEAR with a
reference-grade naming citation. **Outcome: still PARTIAL** — no
reference-grade source was readable first-hand. What was tried and found:

- **Oxford Companion to Chess full text** (archive.org djvu) — WebFetch
  reached only the "A" section / archive nav interface; the **"W"
  (Winawer) entry remained unreadable**. Not quoted.
- **Edward Winter, "The French Defence"** (chesshistory.com) — does
  **not** discuss the Winawer naming (only a Euwe–Gligorić sub-line
  query). No help.
- **A genuine reference-grade source exists but unread:** *The Wizard of
  Warsaw — A Chess Biography of Szymon Winawer* (Lissowski & Bogdanovich).
  The natural primary source for a future upgrade.
- **Secondary corroboration** (chess.com "The French Winawer: A History",
  pawnbreak, 365chess, modern-chess) — all agree the line is named for
  Winawer, popularised by Nimzowitsch (1920s) / Botvinnik (1940s), and
  that Winawer himself played it only a few times. None cites a reference
  work.
- A secondary claim of a **dated game "Paris 1878"** surfaced, but it is
  instructional-site grade and **conflicts** with the Lumbra corpus
  (Steinitz–Winawer, Paris **1867**). Treat with caution; **do not encode
  1878** in the field strings.

**Net:** the naming is uncontested and broadly attested, but the
reference-grade citation gap is unchanged. The recommendation is
unaffected — **Option A** (apply on the Marshall precedent) or **Option B**
(hold for one read of the *Wizard of Warsaw* biography or the OC "W"
entry). The choice remains yours.

## Diagnosis

- **Attribution type: C (early practitioner / namesake), not inventor.**
  The 3…Bb4 idea predates Winawer in the corpus (Paulsen 1861); Winawer
  is the 19th-c master the line is named for; Nimzowitsch and especially
  Botvinnik are the 20th-c popularizers. This mirrors the
  idea-predates-eponym pattern of the applied batch-5 rows.
- **Idea predates the eponym: yes** — state it plainly in
  `historical_notes` (the Sveshnikov/Cambridge-Springs antedating shape).

## Options

### A — Apply attribution to `B.Fre.Win` (recommended)

Apply on the **Marshall precedent**: secondary naming attestation
(uncontested, multi-source) + the verified dated corpus game, with
`attribution_source` citing **only what was seen** (not the unread Oxford
Companion). Closes the Group-B PARTIAL. Strings below.

### B — Keep PARTIAL / deeper review

Hold until the Oxford Companion 'Winawer' entry (or a monograph chapter)
is read first-hand, to make the citation fully reference-grade. Defensible
if the project wants every player eponym to carry a reference-grade
source; costs little since the fact is not in doubt.

### C — `historical_notes` only

Record the story/chronology without `attributed_to`. **Not recommended** —
under-attributes a marquee, uncontested single-person eponym whose
in-family siblings (`B.Fre.Exc.Uhl`, `B.Fre.Kor`) are already attributed.

## Recommendation

**Option A**, head row only — apply, citing the verified secondary
attestation + dated game, with the Oxford Companion noted as an optional
future upgrade (not a blocker). Rationale: the eponym is uncontested, the
evidence shape equals the already-applied Marshall row, and holding a
marquee eponym that its own family-siblings already carry would be
inconsistent. If you prefer strict reference-grade-only, take **B** and
I'll do one Oxford Companion read first.

## Exact proposed field changes (for a future apply — NOT applied here)

**Row `B.Fre.Win`** — 3 currently-empty fields. En-dash `–` (U+2013).

```
attributed_to      = Szymon Winawer (early practitioner; popularised at top level by Aron Nimzowitsch and Mikhail Botvinnik)
attribution_source = Named after Szymon Winawer (1838–1919) per standard references (Wikipedia 'French Defence' and 'Szymon Winawer'; corroborated across opening references); the corpus confirms his early use, e.g. Steinitz–Winawer, Paris 1867 (3...Bb4). [Oxford Companion 'Winawer' entry would upgrade this to reference-grade.]
historical_notes   = 1.e4 e6 2.d4 d5 3.Nc3 Bb4. Named for the Polish master Szymon Winawer (1838–1919), an early adopter of the ...Bb4 pin against 3.Nc3. The idea predates him — the corpus has 3...Bb4 from Paulsen's games (1861) — and the line was developed into a main French weapon in the 20th century by Aron Nimzowitsch (from 1921) and especially Mikhail Botvinnik (from 1927). A namesake early-practitioner, not the inventor.
```

`canonical_name` ("French, Winawer"), `aliases`, `notes`, `flags`,
`moves_uci`, `parent_ocn1`, `transposes_to`, `same_as` all unchanged.

## Expected impact

| dimension | effect |
|---|---|
| rows touched | **1** (`B.Fre.Win`), strings-only |
| child rows | **0** |
| row count | unchanged (5,899) |
| audit counts | unchanged (`unresolved_groups=0`, `multiple_canonical_groups=17`) |
| relations / FEN / schema | unchanged |
| Group-B status | **closes the last PARTIAL** → Group B fully resolved (6/6 sourced) |

## See also

- [`player-eponym-group-b-evidence-sprint.md`](player-eponym-group-b-evidence-sprint.md) — where `B.Fre.Win` was held PARTIAL.
- [`player-eponym-attribution-batch-proposal.md`](player-eponym-attribution-batch-proposal.md) — the parent batch (5 applied).
- [`qgd-cambridge-springs-attribution-proposal.md`](qgd-cambridge-springs-attribution-proposal.md) — the source-gated apply template.
