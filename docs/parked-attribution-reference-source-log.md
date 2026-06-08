# Parked attribution — reference-source access log (post-1.1)

**Status**: **SOURCE ACCESS LOG — no catalogue change, no apply.** Records
what reference-grade sources could be reached first-hand for the 6 parked
PARTIAL items, via the **Oxford-Companion-access tactic** (the common
blocker). **Dynamic workflow used: yes** (6 parallel read-only agents) +
**orchestrator re-verification** of every grade by direct `nlm` query.
Short citation snippets only — no long copyrighted text.

> **Headline: the breakthrough was NotebookLM, not the Oxford Companion.**
> The OC entries stayed unreachable. But the user's own `nlm` chess
> library held reference-grade **book passages**. **4 items reach CLEAR —
> `B.Fre.Win` (Winawer), `D.QGD.Exc.Car` (Carlsbad), `D.Tar` (Tarrasch),
> `D.Chi` (Chigorin)** — each backed by a grounded, quoted book passage,
> each re-verified by direct `nlm` query. **2 stay PARTIAL —
> `B.Sic.Alp` (Alapin), `B.Sic.Tay` (Taimanov)** — `nlm` returned an
> explicit *negative* (no source states the naming).

> **Update 2026-06-08 — Lot A manifested + dry-run verified (no apply).**
> The two strongest CLEARs, `D.Tar` (Tarrasch) and `D.Chi` (Chigorin), are now
> drafted into a real engine manifest
> ([`manifests/lot-a-player-eponyms.manifest.json`](manifests/lot-a-player-eponyms.manifest.json))
> and pass `--dry-run --strict --validate` (2 rows, result validates 5899/0,
> catalogue untouched) — see
> [`lot-a-player-eponyms-dry-run.md`](lot-a-player-eponyms-dry-run.md). **Winawer
> (`B.Fre.Win`) is held out** of that manifest pending an author/year pin for
> *The Center Game*; Carlsbad (`D.QGD.Exc.Car`) is a separate Lot B. Apply is a
> separate GO.

## Verification (orchestrator re-queried every item)

I re-ran each item as a direct `nlm` query rather than trusting the
agents' grades — the discipline that caught the earlier "Paris 1878"
fabrication. **Result: the agents' 4-CLEAR / 2-PARTIAL grading was
correct.** (My own first consolidation draft briefly mis-graded Tarrasch
then Chigorin; both are grounded-CLEAR on direct re-query — corrected
here.) The four CLEARs rest on grounded verbatim passages:

- **Tarrasch** (`D.Tar`) — Avrukh, *GM Repertoire – 1.d4 Vol.1*: *"…the
  starting position of the Tarrasch Defence, named after the famous German
  Grandmaster Siegbert Tarrasch."* + *The Power of Pawns*: *"…the opening
  which was named after him…"*
- **Chigorin** (`D.Chi`) — Avrukh, *GM Repertoire – 1.d4* (Vol.1 / *The
  Queen's Gambit*): *"This opening is named after the famous 19th-century
  Russian grandmaster Mikhail Chigorin."*
- **Winawer** (`B.Fre.Win`) — *The Center Game*: *"…the dangerous
  variation in the French Defence (3.Nc3 Bb4) named after him."* (Szymon
  Winawer 1838–1919).
- **Carlsbad** (`D.QGD.Exc.Car`) — Karpov & Matsukevich, *Estrategia en el
  Ajedrez*, p.61: the structure drew interest after **Karlsbad 1923**.

The two PARTIALs got explicit `nlm` negatives:

- **Alapin** (`B.Sic.Alp`) — *"No source… states that the 1.e4 c5 2.c3
  line is named after Semyon Alapin."* The OC confirms the *label* exists,
  not the naming; one agent "grounded" hit was the **Spanish/Ruy López
  Alapin**, a different opening. Held.
- **Taimanov** (`B.Sic.Tay`) — *"None of the provided sources state that
  the Sicilian Taimanov is named after Mark Taimanov."* Secondary only. Held.

**Verified tally: 4 CLEAR · 2 PARTIAL · 0 BLOCKED.** (Methodology lesson:
re-verify *both* directions — a subagent's grounded CLEAR can be an
over-read OR about the wrong line, and an orchestrator "correction" can
itself be wrong; re-query and quote before trusting either.)

## Per-item status (verified)

| item | slug | grade | source reached (first-hand) | action |
|---|---|---|---|---|
| **Winawer** | `B.Fre.Win` | **CLEAR** | *The Center Game* (nlm Q25, src `a433382e`): "(3.Nc3 Bb4) **named after him**" | apply-ready |
| **Carlsbad** | `D.QGD.Exc.Car` | **CLEAR** (non-person → `attributed_to` EMPTY) | Karpov & Matsukevich, *Estrategia en el Ajedrez* p.61 (nlm Q9, src `f463f146`): **Karlsbad 1923** origin | apply-ready (`historical_notes` only) |
| **Tarrasch** | `D.Tar` (QGD head only) | **CLEAR** | Avrukh *GM Repertoire 1.d4 Vol.1* + *The Power of Pawns* (nlm Q25): "**named after … Siegbert Tarrasch**" | apply-ready (head only) |
| **Chigorin** | `D.Chi` (QGD head only) | **CLEAR** | Avrukh *GM Repertoire 1.d4* (nlm Q25): "**named after the famous 19th-century Russian grandmaster Mikhail Chigorin**" | apply-ready (head only; keep distinct from Ruy López Chigorin `C.RyL.Cha`) |
| **Alapin** | `B.Sic.Alp` | PARTIAL | nlm: no source names the 2.c3 Sicilian after Alapin; OC confirms label only | keep-parked |
| **Taimanov** | `B.Sic.Tay` | PARTIAL | nlm: negative; secondary (Wikipedia) only | keep-parked |

## Methods attempted

- **NotebookLM (`nlm`) — the productive channel.** Grounded book passages
  surfaced for Winawer (*The Center Game*), Carlsbad (Karpov &
  Matsukevich), Tarrasch (Avrukh + *Power of Pawns*), Chigorin (Avrukh). It
  correctly returned **negative** for the Sicilian Alapin and Taimanov. A
  larger library remains unexhausted (Q31a–e *All-book-texts*, Q27, Q32) —
  the natural next pass for the 2 held items.
- **Oxford Companion to Chess** — **not reached first-hand**; archive.org
  search-inside returned `No hOCR/Abbyy file present`. The intended OC
  tactic did not pan out; nlm book passages substituted for the 4 CLEARs.
- **Web (Wikipedia, chess.com, ChessBase)** — secondary corroboration for
  all six; never the load-bearing citation.

## Recommended next actions

1. **Apply the 4 CLEAR items.** Per head:
   - `D.Tar` **Tarrasch** — `attributed_to` "Siegbert Tarrasch
     (systematiser/advocate)", source Avrukh + *Power of Pawns*; **QGD head
     only** (surname spans ~150 rows — never blanket).
   - `D.Chi` **Chigorin** — `attributed_to` "Mikhail Chigorin (…)", source
     Avrukh; **QGD head only**, keep distinct from `C.RyL.Cha`.
   - `B.Fre.Win` **Winawer** — closes Group B 6/6; source *The Center
     Game* (pin exact author/year before applying — passage grounded, book
     author not surfaced; note Mario Ziegler is cited for a *different*
     book in the same paragraph — do not conflate).
   - `D.QGD.Exc.Car` **Carlsbad** — `historical_notes` ONLY,
     `attributed_to` stays EMPTY (non-person); source Karpov & Matsukevich
     p.61; head row (descendants inherit).
   Mixed-type set (3 person-eponym + 1 non-person place): apply as one
   commit, or split the person-eponyms from the Carlsbad note.
2. **Hold Alapin, Taimanov (PARTIAL).** Next attempt: a focused nlm pass
   over Q31/Q27/Q32 for a grounded "named after" passage on each.

## Copyright note

Only short citation snippets recorded (one sentence each) for
verification/attribution; no long passages reproduced. `nlm` source_ids
point back to the user's own licensed library.

## See also

- [`parked-naming-audit-source-sweep.md`](parked-naming-audit-source-sweep.md) — the prior grading this updates (now 4 CLEAR / 2 PARTIAL).
- [`french-winawer-attribution-proposal.md`](french-winawer-attribution-proposal.md) — Winawer's standing proposal (now CLEAR → apply-ready).
- [`naming-attribution-audit-methodology.md`](naming-attribution-audit-methodology.md) — the re-verify-grounded-grades lesson belongs here.
