# Ambiguous aliases: the 29 name collisions

**Status: PENDING DECISIONS — no change applied.** This is a decision
table, not a manifest. Nothing here has been written to
`catalog/ocn-1.csv`, and no manifest exists for it: each row wants a
human yes/no, and only after that does a lot get built.

Roadmap [H2.6](traction-roadmap.md) asks for "name-to-slug lookup unique
or flagged". Twenty-nine alias strings in the catalogue are *exactly*
another row's `canonical_name`, so a name lookup for "Modern Defence"
today returns `B.Mod` plus four unrelated rows and no way to rank them.

**Why the validator does not already catch this.** `validate.py` check
16 bans an alias identical to **its own row's** `canonical_name` — pure
self-identity, retired by the June naming-hygiene lot. An alias equal to
a *different* row's canonical name is not banned by anything today, and
deliberately so: it can be genuine synonymy (see the KEEP rows below).
The follow-up validator check therefore cannot be written until these
decisions exist — it has to know which collisions are legal. It lands
with them, most plausibly as a warning listing every cross-row collision
plus an error for any collision not on an approved list.

## The structural test used for the recommendations

The catalogue is asked, not the literature. A collision is **genuine
synonymy** when OCN itself says the two slugs name the same thing:
`transposes_to` or `same_as` pointing at the row that owns the name,
with byte-identical `moves_uci`. In that case the lookup is not
ambiguous, it is a transposition group, and the name legitimately
applies to every member.

Everything else is a **naming artefact**: the alias is a comma-segment
of the row's own `canonical_name`, or a fragment of the Lichess label
the row was split from, or an ancestor's name repeated on a descendant.
In each of those the unqualified name has an owner elsewhere and the
row's own qualified alias already covers lookup.

That test yields **3 KEEP, 26 DELETE**. Where it feels tight the
reasoning column says so.

## KEEP — 3 rows

`transposes_to` points at the owner and `moves_uci` is byte-identical:
the two slugs are the same position under two move orders, so the shared
name is true synonymy and the lookup resolves to a well-defined
transposition group.

| slug | alias | name owned by | why KEEP |
|---|---|---|---|
| `D.QPG.Ver.Ric` | Richter-Veresov Attack | `A.Ver` | `transposes_to = A.Ver`, identical `moves_uci` (`d2d4 g8f6 b1c3 d7d5 c1g5`); the row exists precisely to re-state the Richter-Veresov identity from the queen-pawn move order. |
| `D.QPG.Zuk.Nf6.Bf4` | London System | `A.Lon` | `transposes_to = A.Lon`, identical `moves_uci`; same London position from the Zukertort move order. |
| `D.QPG.Zuk.Col.Bd3` | Colle System | `A.Col` | `transposes_to = A.Col`, identical `moves_uci`; same Colle position from the Zukertort Colle prefix. |

## DELETE — 26 rows

### Segment of the row's own canonical_name (14)

The alias is one comma-segment lifted out of the row's own name. It
carries no information the canonical name does not, and the unqualified
form belongs to a different opening.

| slug | alias | name owned by | why DELETE |
|---|---|---|---|
| `A.QPO.g6` | Modern Defence | `B.Mod` | Tail segment of "Queen's Pawn Opening, Modern Defence"; `B.Mod` is 1.e4 g6, this row is 1.d4 g6, no link. The American-folded full name stays. |
| `B.Sic.Ama` | Amazon Attack | `D.QPG.Ama` | Tail segment of "Sicilian, Amazon Attack"; the bare name belongs to the 1.d4 d5 2.Qd3 row. Leaves this row alias-less. |
| `A.Eng.AIn.Nf3.g6.b4` | English Orangutan | `A.Eng.Org` | Lead segment of "English Orangutan, Anglo-Indian"; `A.Eng.Org` is the 3-ply owner, this row a 5-ply cousin under `A.Eng`. Leaves this row alias-less. |
| `B.Fre.d3` | King's Indian Attack | `A.KIA` | Tail segment of "French Defence, King's Indian Attack"; the qualified alias "French Defense, King's Indian Attack" already serves the lookup this row deserves. |
| `A.Hng.f5` | Dutch Defence | `A.Hol` | Tail segment of "Hungarian Opening, Dutch Defence"; `A.Hol` is 1.d4 f5, this row 1.g3 f5, no link. |
| `D.QPG.Ver.Nbd7.Nf3.g6` | Grünfeld Defence | `E.Gru` | Tail segment of "Veresov Two Knights, Grünfeld Defence"; no c4 has been played, so it is not `E.Gru`'s position and there is no link. |
| `E.KID.Fou.Na6` | Modern Defence | `B.Mod` | Tail segment of "KID Four Pawns, Modern Defence"; both qualified forms are already aliases. |
| `C.Cen.Dsh.Acc.MLn.Qe7` | Chigorin Defence | `D.Chi` | Tail segment of "Danish Gambit Accepted Main Line, Chigorin Defence"; a King's-Pawn gambit line, unrelated to `D.Chi` (1.d4 d5 2.c4 Nc6). |
| `D.Sem.Mer.Bd3.Bd6` | Chigorin Defence | `D.Chi` | Tail segment of "Semi-Slav Meran Bd3, Chigorin Defence"; the qualified form is already an alias. |
| `D.Sem.AMe.Chi` | Chigorin Defence | `D.Chi` | Tail segment of "Semi-Slav Anti-Meran, Chigorin Defence"; the qualified form is already an alias. |
| `C.Vie.Nc6.d4.f5` | Philidor Countergambit | `C.PhD.d4.f5` | Tail segment of "Vienna Fyfe, Philidor Countergambit"; a Vienna with Nc3/Nc6, not `C.PhD.d4.f5`'s Nf3/...d6 position. Leaves this row alias-less. |
| `D.QGD.Vie.Sxx` | Queen's Gambit Accepted | `D.QGA` | Tail segment of "QGD, Vienna Variation, Queen's Gambit Accepted"; `D.QGA` is the 4-ply root of the whole accepted complex. Leaves this row alias-less. |
| `A.EID.Fch.NGr.dxc4` | Modern Defence | `B.Mod` | Tail segment of "East Indian Neo-Grünfeld, Modern Defence"; both qualified forms are already aliases. |
| `C.KGm.Acc.Nf3.KKn.Bc4.Phi` | Philidor Gambit | `C.PhD.d4.Bd7` | Tail segment of "King Knight Gambit Bc4, Philidor Gambit"; two unrelated things share the Philidor name, and the qualified "King's Gambit Accepted: Philidor Gambit" alias survives. |

### Ancestor or prefix duplication (2)

The alias is a name an ancestor (or the line this row is a ply-prefix
of) already owns, so lookup should resolve upward.

| slug | alias | name owned by | why DELETE |
|---|---|---|---|
| `B.Pir.Pre` | Pirc Defence | `B.Pir` | `B.Pir` is this row's own `parent_ocn1`, and this row's `moves_uci` is a prefix of the parent's; a child cannot also be the unqualified parent. "Pirc Defense, Precursor" stays. |
| `A.Ret.Nf6.g3` | King's Indian Attack | `A.KIA` | This row's `moves_uci` is `A.KIA`'s line one ply short (`A.KIA` adds ...d5); the owner is the complete setup. Leaves this row alias-less. |

### Lichess sub-label fragment (5)

The alias is a sub-variation word from the Lichess label the row was
split from, colliding by accident with a top-level opening name. The
full Lichess label is retained where present.

| slug | alias | name owned by | why DELETE |
|---|---|---|---|
| `E.KID.Avk.Cst.Bg5.Na6` | Modern Defence | `B.Mod` | "Modern" here is Lichess's word for ...Na6 inside the Averbakh; the full label "King's Indian Defense: Averbakh Variation, Modern Defense" survives. |
| `D.Sem.e3.Nbd7.Bd3.Bd6` | Chigorin Defence | `D.Chi` | "Chigorin" is Lichess's word for the ...Bd6 Semi-Slav setup, not the 1.d4 d5 2.c4 Nc6 defence. Leaves this row alias-less. |
| `D.Sem.AMe.Sto.b6` | Chigorin Defence | `D.Chi` | Same Semi-Slav sub-label as above, on the Stoltz b6 line. Leaves this row alias-less. |
| `B.Pir.Pre.f4` | Rat Defence | `B.Rat` | Survives from the Lichess label "Rat Defense: Harmonist"; the row is 1.e4 d6 2.f4, `B.Rat` is the ...d6/...e6 small-centre defence. "Harmonist" stays. |
| `D.Sem.Bg5.Nbd7.e3` | Queen's Gambit Declined | `D.QGD` | A depth-5 Semi-Slav row cannot be the unqualified 4-ply `D.QGD`. This row also loses "e3 Line" to the synthetic-alias lot, leaving only "D52 Prefix". |

### Unqualified system or family name owned elsewhere (5)

The name is real for this row in loose usage, but the catalogue gives it
an owner and asserts no link between the two positions. These are the
judgement calls; each is defensible either way, and the note says what
the alternative to deletion would be.

| slug | alias | name owned by | why DELETE (and the alternative) |
|---|---|---|---|
| `E.Ind.Cat` | Catalan Opening | `D.Cat` | The row's own `notes` say OCN keeps the ...d5 Catalans in class D; `D.Cat` owns the bare name. **Alternative:** keep it and accept that "Catalan Opening" is a 4-way lookup. Leaves this row alias-less. |
| `E.Ind.Cat.d5` | Catalan Opening | `D.Cat` | Same collision one ply deeper; a deeper row repeating its parent's unqualified alias is inherited noise. Leaves this row alias-less. |
| `E.Ind.Cat.d5.Bg2` | Catalan Opening | `D.Cat` | Same collision two plies deeper; the qualified "Catalan Opening: Closed" alias survives. |
| `A.QPO.Nf6.Nf3.e6.Bf4` | London System | `A.Lon` | White's setup is a London, but the position differs from `A.Lon` (...e6 vs ...d5) and no `transposes_to`/`same_as` links them, unlike the three KEEP rows. **Alternative:** keep it, and accept that London-by-Black's-setup is a system name rather than a position name. Leaves this row alias-less. |
| `B.Pir.Pre.d4.Nf6.Nc3.Nbd7` | Lion Defence | `B.Lio` | The tightest call in the table: this row *is* Black's ...d6/...Nf6/...Nbd7 Lion setup, while `B.Lio`'s `moves_uci` encodes White's f3 line against it. **Alternative:** keep the alias and instead cross-link the two rows, which is arguably the more honest fix. "Pirc Defense, Lion Setup" stays either way. |

## If every recommendation is accepted

- 26 alias entries removed, 3 kept.
- 10 of the 26 rows are left with an empty `aliases` cell (marked "leaves
  this row alias-less" above). That is the expected outcome of deleting a
  string that only ever restated another row's name, and matches what
  the synthetic-alias lot does to 1,648 rows.
- "Modern Defence" drops from a 5-way to a 1-way lookup, "Chigorin
  Defence" from 6-way to 1-way, "Catalan Opening" from 4-way to 1-way.
- The three surviving collisions are all inside declared transposition
  groups, so a name index can return the group and be correct.
- The follow-up validator check then has a rule it can enforce: a
  cross-row canonical-name collision is an error unless the aliasing row
  declares `transposes_to`/`same_as` at the row that owns the name.
