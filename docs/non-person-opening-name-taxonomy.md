# Non-person opening-name taxonomy (post-1.1)

**Status**: **DISCOVERY — no catalogue change.** A terrain map of *why
non-person opening names exist* in OCN-1, so future naming work picks a
**class of names with homogeneous treatment** rather than one opening at
a time. **Dynamic workflow used: yes** (6 parallel read-only sweeps). It
applies nothing; everything here is documentation + a gated backlog.

> **The load-bearing finding, six times over: the catalogue is already
> right.** Across all six non-person categories, essentially every row
> has `attributed_to` **empty** with the descriptor living in
> `notes` — which is exactly what the methodology prescribes. Non-person
> names are overwhelmingly **document-only / no change**. The catalogue's
> 17 attributed rows are person eponyms + 5 sourced event anchors; **no
> non-person descriptor should receive `attributed_to`** absent a real
> source, and almost none warrant even `historical_notes` without one.
> The value of this map is therefore mostly **negative space**: it tells
> future audits where *not* to spend effort.

## Method

A dynamic workflow ran **6 parallel read-only agents**, one per naming
category, over the live 5,899-row catalogue (calibrated on the
methodology + the two prior batch proposals). Agents returned structured
taxonomies and **edited nothing**.

**Orchestrator verification (important):** I re-checked every cited slug
against the CSV. **18 agent-cited slugs were guessed abbreviations that
do not exist**; I resolved the **real** slug by name for each and this
document uses only those. The corrections (wrong guess ⟶ verified slug;
the left-hand strings are NON-CATALOGUE pseudo-slugs shown only to record
the fix):

- "C.4Kt" ⟶ `C.Fou` (Four Knights Game)
- "C.BiO" ⟶ `C.Bsh` (Bishop's Opening)
- "C.KGa" ⟶ `C.KGm` (King's Gambit)
- "A.Sok" ⟶ `A.Eng.Org` (English Orangutan)
- "B.Sic.Naj.Psn" ⟶ `B.Sic.Naj.Pst` (Sicilian Najdorf, Poisoned Pawn)
- "D.BDG" ⟶ `D.Bgm` (Blackmar-Diemer Gambit)

Every backtick-quoted slug elsewhere in this document is verified present
in `catalog/ocn-1.csv`. Per-token counts below are verified by direct
`csv` passes (ballpark where noted — a token recurs across depths).

**Sources:** `catalog/ocn-1.csv` (source of truth, all cited slugs
re-verified), methodology, the event-venue + player-eponym batch
proposals, `external/lichess-openings` (type-G labels). No web needed.

**Limitations:** counts are over `canonical_name` substrings (a token can
appear at many depths). The taxonomy classifies *naming basis*, not
position correctness. Folk etymologies (Dragon/Orangutan/Hippo stories)
are recorded as **research questions**, never as facts.

## Taxonomy

| # | Category | Definition | Verified OCN examples | Evidence to change a field | Recommended storage |
|---|---|---|---|---|---|
| 1 | **Geography — opening family** | The place *is* the line's identity | `B.Sic` Sicilian, `B.Fre` French, `C.Ita` Italian, `B.Sca` Scandinavian, `A.Hol` Dutch, `A.Eng` English, `C.Sco` Scotch, `C.Vie` Vienna, `D.Sla` Slav | Oxford-Companion-grade etymology of the family name | `canonical_name` (is the name); `attributed_to` **empty**; family etymology → `historical_notes` *only if sourced* |
| 2 | **Geography — event anchor** | Place+context names a line fixed at a dated event | `D.Cat` (Barcelona 1929), `D.Sem.Mer` (Meran 1924), `E.KID.Cls.Mar` (Mar del Plata 1953), `C.RyL.Ber.Wal.End` (London 2000), `D.QGD.Cmb` (Cambridge Springs 1904) | dated game/event + a source tying the *name* to it | **all 5 already applied** — the reference template, not new work |
| 3 | **Geography — place/structure or DB label** | Place token reused across unrelated lines | `D.QGD.Exc.Car` Carlsbad (7 rows), `E.Nim.Cls.Zur` Zurich, `E.Gru.Bg5` Stockholm, `C.RyL.Mor.Opn.Rig` Riga | a source tying the name to an event (rare) | keep `notes`; `attributed_to` **empty** (F/G) |
| 4 | **Structure / strategic concept** | Names a pawn structure, setup, or plan | `A.Hol.Sto` Stonewall, `A.Eng.Sym.Hdg` Hedgehog, `B.Sic.Kan.Mar`/`B.Sic.OKe.c4` Maróczy Bind, `*.Fch` Fianchetto, `*.Exc` Exchange | coiner + datable print source for the term | `notes` (already there); `historical_notes` only if sourced; `attributed_to` empty — **except Maróczy Bind = a person** |
| 5 | **Move / piece / formation** | Move-shape or piece arrangement | `C.Fou` Four Knights (106), `C.Thr` Three Knights, `C.Ita.Two` Two Knights, `C.Bsh` Bishop's Opening, `C.Pet` Petrov | earliest-use source for the traditional name | `canonical_name`; `attributed_to` empty |
| 6 | **Metaphor / animal / evocative** | Nickname/metaphor label | `B.Sic.Dra` Dragon (~92), `B.Hip` Hippopotamus, `A.Eng.Org` English Orangutan, `B.Mod.Pte` Pterodactyl (~50), `C.Ele` Elephant Gambit, `E.Ben.Mod.Snk` Snake | a **sourced** coinage (not folklore) | `canonical_name`/`aliases`; `attributed_to` empty; story → `historical_notes` only if sourced |
| 7 | **Gambit / tactic / evaluation** | Material offer or tactical motif | `C.KGm` King's Gambit, `D.Bgm` Blackmar-Diemer, `B.Sic.Naj.Pst` Poisoned Pawn, `B.Sic.Win` Wing Gambit, `C.RyL.Cls.d4.Nxd4` Noah's Ark Trap | source for first-use of the motif name | `canonical_name` + `notes`; `attributed_to` empty (the idea, not a person) |
| 8 | **Database / editorial descriptor** | ECO/Lichess/OCN bookkeeping token | `D.QGA` Accepted, `D.QGD` Declined, `B.Fre.Exc` Exchange, `E.Nim.Sml.Kmo` Move Order, `A.Lon` System | **none — never attribute** | `canonical_name` + `notes`; **permanently unattributed** |

## Candidate buckets

### A. Document-only / no catalogue change (the overwhelming majority)

Every geographic-family root (`B.Sic`, `B.Fre`, `C.Ita`, `B.Sca`,
`A.Hol`, `A.Eng`, `C.Sco`, `C.Vie`, `D.Sla`), all structure names, all
move/piece names, all metaphors, and all gambit/tactic labels are
**already correctly unattributed**. No action. A `csv` pass confirmed
**1,370 structure/setup rows** and **all metaphor rows** have empty
`attributed_to`.

### B. Possible `historical_notes` enrichment (sourced, future, optional)

Only if a real source is found — never on folklore. Highest-value:
- `D.QGD.Exc.Car` **Carlsbad** — structure-origin note (Carlsbad 1923), source-gated; the one place token where a note may be justified.
- Family etymologies (`B.Fre`, `B.Sca`, `A.Hol`, `C.Vie`, `C.Sco`) — *why* the geographic name, if an Oxford-Companion-grade source is read.
- `C.Fou` Four Knights / `C.Bsh` Bishop's Opening — earliest-use note.
- Structure coinages: `A.Hol.Sto` Stonewall, `A.Eng.Sym.Hdg` Hedgehog.

### C. Deeper review (genuine ambiguity)

- **`B.Sic.Kan.Mar` / `B.Sic.OKe.c4` Maróczy Bind** — a structure named for a **person** (Géza Maróczy). This is the one structure label that is really a *player eponym* → route to the eponym track, attribute per-head with a source. (Don't treat as a generic structure descriptor.)
- `B.Sic.Sch` **Scheveningen**, `A.Hol.Lng` **Leningrad** — place-named *systems*; confirm whether sourced to city/event or pure F/G label.
- The **Pterodactyl** subtree (`B.Mod.Pte` + dinosaur-genus children) and **Monkey's Bum**, **Orangutan**, **Hippopotamus** — colourful coinages with well-known *folklore* but no source in hand; document the question, do not encode the story.

### D. Ignore / keep — the "never attribute" descriptor map

**46.3% of the catalogue (2,734 / 5,899 rows)** carries a pure
editorial/descriptor token. Verified counts: **Gambit 1008**, **Main
Line 861**, **Variation 852**, Classical 470, Modern 362, Accepted 243,
Exchange 199, Declined 110, System 94, Move Order, Normal, Deferred,
Transposition, Advance, Open, Closed, Fianchetto. **Policy: these are
Type-H descriptors and must remain unattributed permanently.** This is
the single biggest "do not spend effort here" set — future audits should
filter it out first.

## Recommended next batch

**No attribution batch.** The honest output of this map is that the
non-person space is **already correct** — there is no homogeneous set of
rows needing `attributed_to`. Three *optional, source-gated* threads, in
priority order, none an apply:

1. **Maróczy Bind → eponym track** (it's a person; the only mis-filed
   case) — a 1–3 row per-head attribution once sourced.
2. **Carlsbad `historical_notes`** — the one place-structure note worth a
   source check.
3. **Family/structure etymology enrichment** — `historical_notes` only,
   only with Oxford-Companion-grade sources; large effort, low urgency.

Everything else: **document-only, leave as-is.**

## Rules learned (promote to methodology)

1. **Place name ≠ event attribution.** A geographic family name (Sicilian,
   French) names the *line*, not a person/event; it gets no `attributed_to`.
2. **Metaphor needs a source, not folk etymology.** Dragon/Orangutan/
   Hippopotamus stories stay out of the catalogue until a citable coinage
   is read.
3. **Descriptors are legitimate and stay unattributed.** Main Line,
   Exchange, Accepted, Variation, System, Move Order — ~46% of rows —
   are Type-H by design; never attribute them.
4. **`historical_notes` > `attributed_to` for non-person names.** When a
   sourced story exists, it belongs in `historical_notes`; `attributed_to`
   stays empty unless there is a person, or an event/organisation with a
   source (the Cambridge Springs person-less shape).
5. **A structure label can hide a person** (Maróczy Bind) — check before
   filing as a descriptor.
6. **Verify slugs.** Agent-suggested slugs may be guessed abbreviations;
   resolve real slugs by name before citing.

## Top 10 "why named so?" research questions

1. **Maróczy Bind** — confirm Géza Maróczy as eponym + a source (then attribute).
2. **Carlsbad structure** (`D.QGD.Exc.Car`) — does a QGD monograph / Oxford Companion tie the name to Carlsbad 1923?
3. **Stonewall** (`A.Hol.Sto`) — who first coined it for the d/e/f formation; datable print source?
4. **Hedgehog** (`A.Eng.Sym.Hdg`) — when/by whom did the metaphor enter chess literature?
5. **Dragon** (`B.Sic.Dra`) — is the Draco-constellation origin (and a Dus-Chotimirsky coinage) backed by a primary source?
6. **Orangutan** (`A.Eng.Org`) — does any New York 1924 record document Tartakower's zoo anecdote?
7. **Pterodactyl** subtree — who coined it and its dinosaur pseudo-taxonomy?
8. **Bishop's Opening / Four Knights** — earliest recorded use of these traditional descriptive names?
9. **Scheveningen / Leningrad** — city-named systems: sourced to event/city, or pure F/G?
10. **Poisoned Pawn / Noah's Ark Trap** — sourced first-use of the motif names?

## See also

- [`naming-attribution-audit-methodology.md`](naming-attribution-audit-methodology.md) — types A–I; rules 1–6 above are candidates to fold in.
- [`event-venue-attribution-batch-proposal.md`](archive/event-venue-attribution-batch-proposal.md) — the venue "no batch-safe" precedent (consistent with category 3).
- [`player-eponym-attribution-batch-proposal.md`](archive/player-eponym-attribution-batch-proposal.md) — where Maróczy Bind should route.
- [`qgd-cambridge-springs-attribution-proposal.md`](archive/qgd-cambridge-springs-attribution-proposal.md) — the person-less event-anchor template (category 2).
