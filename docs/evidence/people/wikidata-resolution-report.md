# Identity resolution pass, closing report

## 1. Headline numbers

| Confidence | Rows | Share |
|---|---:|---:|
| high | 226 | 93.0% |
| medium | 4 | 1.6% |
| not-found (null QID) | 13 | 5.3% |
| **total** | **243** | |

| Metric | Value |
|---|---:|
| QIDs assigned | 230 |
| Distinct QIDs | 225 |
| Rows in a QID collision | 10 (5 pairs) |
| display_name corrected | 35 |
| Rows carrying a same-surname hazard | 98 (40.3%) |
| Non-human / non-person entities resolved | 3 (`monster`, `chesscom`, `dracula`) |

## 2. Duplicate identities

| QID | Person ids | Verdict | Action |
|---|---|---|---|
| Q312814 | `marshall`, `marshall-viele` | Same human, Frank James Marshall. `marshall-viele` is a corrupt corpus string; all its games are the 1907 Lasker match. | Merge `marshall-viele` into `marshall`, remap event refs, retire the corrupt row. **Note the direct conflict**: the `marshall` note says the two rows must NOT converge on Q312814, the `marshall-viele` note proves they must. Human adjudicates; the event evidence favours the merge. |
| Q131374 | `aljechin`, `alekhine` | Same human, Alexander Alekhine. `Aljechin` is the German/Dutch transliteration; the same 1929 Bogoljubow match is split across both spellings (21 games / 2 games). | Merge into `alekhine`; keep "Aljechin" as an alias string only. |
| Q57310 | `bogoljubov`, `bogoljubow` | Same human, Efim Bogoljubow/-ov. Pure spelling fork (Wikidata label `-ov`, enwiki title `-ow`). | Collapse to one row; pick the enwiki spelling `Bogoljubow` for house consistency, other as alias. |
| Q253772 | `bikova`, `bykova` | Same woman, Elisaveta Bykova. `bikova` was "Bikova, E." from the 1959 wch row. | Merge into `bykova`; `Bikova` becomes an alias. |
| Q1512937 | `master`, `gunderam` | Same human, Gerhart Gunderam. `master` is the parse artefact "Master, International". | Delete `master`, remap its opening row to `gunderam`. |

## 3. Corrected names

| person_id | Input | Corrected | Type |
|---|---|---|---|
| master | Master, International | Gunderam, Gerhart | parse artefact, not a person |
| marshall-viele | Marshall Viele, Fabrizio Aaron | Marshall, Frank | conflated record |
| aljechin | Aljechin, Yuri | Alekhine, Alexander | wrong forename + transliteration |
| morrison → see §5 | Morrison, John | (unchanged, unresolved) | corrupt PGN header |
| karklins | Karklins, Chicago | Karklins, Andrew | city string as forename |
| kushnir-aleksandr | Kushnir Aleksandr | Kushnir, Alla | man's forename on a woman's row |
| karpov | Karpov, Aleksandr | Karpov, Anatoly | wrong forename |
| smyslov | Smyslov, Vladimir | Smyslov, Vasily | wrong forename |
| bikova | Bikova, E. | Bykova, Elisaveta | initial + spelling |
| bykova | Bykova, Elizaveta | Bykova, Elisaveta | spelling normalised to enwiki |
| gunderam | Gunderam, Gerhard | Gunderam, Gerhart | spelling |
| spielmann | Spielmann, Rudolph | Spielmann, Rudolf | spelling |
| winawer | Winawer, Simon | Winawer, Szymon | anglicisation reverted |
| soldatenkov | Soldatenkov, Vasily | Soldatenkov, Vassily | spelling to Wikidata/enwiki |
| bonschosmolovsky | Bonsch-Osmolovsky, Mikhail | Bonch-Osmolovsky, Mikhail | transliteration (opening keeps ECO's "Bonsch-") |
| lopez | López, Juan | Bellón López, Juan Manuel | maternal surname taken as family name |
| galway | Galway, Albéric | O'Kelly de Galway, Albéric | compound surname split |
| kruijs | Kruijs, Maarten | van 't Kruijs, Maarten | nobiliary particle dropped |
| lucena | Lucena, Luis | Ramírez de Lucena, Luis | compound surname truncated |
| segura | Lopez de Segura, Ruy | López de Segura, Ruy | diacritic |
| forgacs | Forgacs, Leo | Forgács, Leó | diacritics restored (house style) |
| gukesh-d\* | Gukesh D | Dommaraju, Gukesh | name order, family name is Dommaraju |
| hou | Hou, Yifan (HLJ) | Hou, Yifan | league team tag stripped |
| spassky | Spassky, Boris Vasily | Spassky, Boris | mangled patronymic |
| petrosian | Petrosian, Tigran V | Petrosian, Tigran | initial dropped |
| bronstein | Bronstein, David I | Bronstein, David | stray initial reads as regnal numeral |
| romanishin | Romanishin, Oleg M | Romanishin, Oleg | initial dropped |
| short | Short, Nigel D | Short, Nigel | truncated middle name |
| timman | Timman, Jan H | Timman, Jan | db-style abbreviation |
| fischer | Fischer, Robert J | Fischer, Robert James | truncation expanded |
| zvorykina | Zvorykina, K. | Zvorykina, Kira | initial expanded |
| capablanca | Capablanca, Jose | Capablanca, José Raúl | expanded + accented |
| from | From, Martin | From, Martin Severin | forename expanded |
| polerio | Polerio, Giulio | Polerio, Giulio Cesare | forename expanded |
| allgaier | Allgaier, Johann | Allgaier, Johann Baptist | forename expanded |
| leonhardt | Leonhardt, Paul | Leonhardt, Paul Saladin | forename expanded |

\* input form inferred from the person_id; confirm against the source row before applying.

## 4. Shared-surname hazards (98 rows)

| person_id | Kept | Colliding entities | Discriminator |
|---|---|---|---|
| petrov | Petrov, Alexander Q550980 | Vladimirs Petrovs Q740571, Marian Petrov Q3657819, Dmitry Petrov Q4360762 | eponym is the 19th-c Russian |
| adams-weaver | Adams, Weaver Q983313 | Michael Adams Q299636 | 1940s dating; Michael b. 1971 is routinely miscredited |
| adams | Adams, Michael Q299636 | Weaver W. Adams Q983313 (`adams-weaver`) | 1994 PCA candidates match; must never merge |
| lundin | Lundin, Erik Q653809 | Jan Lundin Q71304538; non-chess Erik Lundins Q5967031, Q24018410, Q5967023 + 2 researchers | occupation + dates |
| kieseritzky | Kieseritzky, Lionel Q313177 | R.K. Kieseritzky Q7273374 (1870-1923) | King's Gambit line is Lionel's |
| gusev | unresolved | 5 chess Gusevs Q21638545, Q27525608, Q27525609, Q71316177, Q134176649 | none is the Nikolai Nikolaevich the sources name |
| mcdonnell | McDonnell, Alexander Q555043 | George Alcock MacDonnell Q2630805 | La Bourdonnais 1834 match provenance |
| forgacs | Forgács, Leó Q934474 | Gyula Q27525051, József Q71297979, Attila Jr Q113673585 | dates separate cleanly |
| topalov | Topalov, Veselin Q172798 | Aleksandar Topalov Q108488306 | nationality + FIDE ID |
| segura | López de Segura, Ruy Q297457 | Bellón López Q2561974 (same batch) | "López" alone never identifies him |
| larsen | Larsen, Bent Q108807 | badminton Q138633139, rower Q56254483, handball Q4890337, Q38471596, disambig Q12303181 | only chess Bent Larsen |
| marshall | Marshall, Frank Q312814 | repo's own `marshall-viele` row; multiple non-chess Frank Marshalls | see §2 |
| marshall-viele | Marshall, Frank Q312814 | the input string itself conflates the 1907 challenger with a modern double-surname record | treat any "Marshall Viele" as this conflation |
| hromadka | Hromádka, Karel Q934788 | footballer Q12028265, ice-hockey Q12028266, disambig Q12028264 | occupation |
| lopez | Bellón López, Juan Manuel Q2561974 | Ruy López de Segura Q297457 | the surname split is exactly what went wrong |
| kushnir-aleksandr | Kushnir, Alla Q269098 | not a second human, a corrupted corpus spelling | wch 1965/69/72 rows prove identity |
| xie | Xie, Jun Q255142 | swimmer Q8044370, biotechnologist Q110148908, 4 Ming/Yuan figures | 1970 birth + chess occupation |
| petrosian | Petrosian, Tigran Q180636 | Tigran L. Petrosian Q528959 (b. 1984); crime boss Q4361652 | this is Vartanovich, the world champion |
| fleissig | Fleissig, Bernhard Q2902583 | brother Max Fleissig (no QID) | Scotch variation is Bernhard's |
| balogh | Balogh, János Q79081 | Csaba Balogh Q789568; a dozen non-chess János Baloghs | match on chess-player description |
| sveshnikov | Sveshnikov, Evgeny Q675955 | son Vladimir Q24027558 | the Sicilian is the father's |
| smith | Smith, Ken Q16014510 | poet Q6388513, several footballers | enwiki "(chess player)" |
| goring | Göring, Carl Q69142 | Hermann Göring (dominant non-chess homonym) | forename is load-bearing |
| lange | Lange, Max Q62453 | Q1912934, Q1912932, Q27505699, Q94819080, Q18411569 | only Q62453 is the chess master |
| leonard | Leonard, James Q6128173 | Giovanni Leonardo Di Bona Q455398 | "Leonardis" invites the 16th-c Italian |
| ware | Ware, Preston Q7242011 | Preston Ware Orem Q7242013 (composer) | prefix-search trap |
| neumann | Neumann, Gustav Q62176 | 9+ Gustav Neumanns incl. Holocaust records Q105566792, Q105470086 | only Q62176 is chess |
| gelfand | Gelfand, Boris Q486778 | scientist Q60694743; disambig Q56653678 | 2012 Anand match |
| arkell | Arkell, Keith Q1277091 | Susan Lalic Q5157522, competed as Susan Arkell | male GM |
| levitsky | Levitsky, Stepan Q166086 | Andrey Levitskiy Q71318535 (b. 2002); older "Levitzky" spelling | 1876-1924 Russian master |
| albin | Albin, Adolf Q360771 | Albin Planinc Q603418 (Albin as forename) | real risk for a surname-keyed id |
| gurgenidze | Gurgenidze, Bukhuti Q650054 | David Gurgenidze Q338291, study composer | different chess Gurgenidze |
| vinogradov | unresolved | Sir Paul Vinogradoff Q1976412 (legal historian, mislinked by Wikipedia); chess Q27533912, Q27533913, Q71304964 | DO NOT USE Q1976412 |
| popov | Popov, Georgi Alexandrov Q65695255 | Valery Q517854, Ivan Q3429656, Nikolay Q4372576, Petar Popović Q1376916, a dozen more | Bulgarian correspondence player, not any OTB Popov |
| aljechin | Alekhine, Alexander Q131374 | brother Alexei Alekhine Q4062145 | also duplicate of `alekhine` |
| morrison | unresolved | John Morrison Q487308 (Canadian, real, NOT this row); Robert Q27528639, William Q27528642, Graham Q71299980 | row is a corrupt header for Schlechter |
| khenkin | Khenkin, Igor Q70779 | Viktor Khenkin Q4497237 (1923-2010) | eponym is the GM b. 1968 |
| janowski | Janowski, Dawid Q378839 | Chaim Janowski Q5067813 | Polish-French master 1868-1927 |
| anand | Anand, Viswanathan Q45747 | Pranav Anand Q71319679 and others with Anand as final element | former world champion |
| muzychuk | Muzychuk, Mariya Q439881 | sister Anna Muzychuk Q241258 (b. 1990) | birth year 1992 |
| torre | Torre, Carlos Q544520 | Eugenio Torre Q1373353; Vittorio Torre Q1643573 | Mexican GM |
| kasparov | Kasparov, Garry Q28614 | Sergey Kasparov Q3918615 | unrelated |
| dory | unresolved | Jenő Döry Q27579527 (chess, b. 1951) do not use; László Dőry de Jobaháza Q111270511 (theologian) name-alike | neither is the 1897 player |
| macleod | MacLeod, Nicholas Q7025815 | Norman Macleod Q351085; non-chess Nicholas MacLeod Q76065344 | 1870-1965 |
| bikova | Bykova, Elisaveta Q253772 | Evgeniya Bykova Q28480088 (also "E.") | the 1959 wch match rules her out |
| gulko | Gulko, Boris Q893658 | military officer Boris Gulko Q16640689 | do not use Q16640689 |
| alekhine | Alekhine, Alexander Q131374 | brother Alexei Alekhine Q4062145 | Q4062145 is not the eponym |
| keres | Keres, Paul Q207727 | Paul Keres the lawyer Q61110028 (b. 1982) | identical label |
| cochrane | Cochrane, John Q964982 | 10+ John Cochranes incl. US general Q5844272, an economist | only Q964982 has the chess occupation |
| durkin | Durkin, Robert Q63125610 | Q51751963 (USAF officer), Q21453080 | only Q63125610 is the chess player |
| polgar | Polgar, Susan Q12823 | Judit Q183250, Sofia Q155388, father László | Q12823 specifically |
| grunfeld | Grünfeld, Ernst Q93742 | Yehuda Gruenfeld Q1338537; economist Ernst Grünfeld Q1358384 (identical full name) | occupation |
| zaitsev-igor | Zaitsev, Igor Q1657668 | Alexander Zaitsev Q1339147; Aleksandr Zaytsev Q27534513 | Ruy Lopez Zaitsev is Igor's |
| zaitsev-alexander | Zaitsev, Alexander Q1339147 | Igor Zaitsev Q1657668; Q27534513 whose English alias is exactly "Alexander Zaitsev" | Grünfeld gambit is Alexander's |
| furman | Furman, Semyon Q2005726 | actor Semyon Furman Q4493515 | identical name |
| paulsen | Paulsen, Louis Q60377 | brother Wilfried Q75290; Dirk Paulsen Q42380970 | |
| cunningham | Cunningham, Alexander Q283083 | Q1288869 (historian, holds a spurious chess-player claim), Q18611108 (empty duplicate stub) | occupation filter alone picks the wrong item |
| horwitz | Horwitz, Bernhard Q62031 | Holocaust victim Bernhard Horwitz Q104805997 (top search hit); I.A. Horowitz | search rank is misleading |
| karpov | Karpov, Anatoly Q131674 | Q4215781, Q4215780, Q487571, Q28124076 | verify by FIDE ID 4100026, not the name |
| mccutcheon | McCutcheon, John Q55653977 | cartoonist John T. McCutcheon; folk musician John McCutcheon | item has no en label, only ruwiki |
| adler | unresolved | Q504223 Mór Adler, Hungarian painter, exact name match | DECOY, do not use |
| camara | Câmara, Hélder Q10299150 | archbishop Hélder Câmara Q378326 | DECOY, far more famous |
| desprez | unresolved | Q3288890 Marcel Després (politician) carries alias "Marcel Desprez"; Marcel Deprez the engineer | DECOY |
| bronstein | Bronstein, David Q312908 | Trotsky's father David Bronstein Q58419633; Q86932220, Q95759386 | |
| ioseliani | Ioseliani, Nana Q259851 | second Nana Ioseliani Q140356693 (actor); Jaba Ioseliani | |
| hubner | Hübner, Robert Q77389 | Q94893160 actor, Q2157636 presenter, Q50426874, disambig Q17591506 | label-only match fails |
| miles | Miles, Tony Q203644 | Q7822977, Q55530833, Q16732596, Q16228471, disambig Q7822978 | name-only matching unsafe |
| monster | Frankenstein's monster Q2021531 | Victor Frankenstein confusion; Q1131389, Q102440966, Q102442594, Q16259544, Q56433191 | fictional, see §5 |
| parham | unresolved | 50+ humans with family name Parham, none this player; opening Q1671558 has no P138 | any Parham QID is a false match |
| richter | Richter, Kurt Q65956 | Emil Richter Q5371420 (separate eponym); Michael/Christian/Wolfgang/Julia Richter; Kurt Richters Q1522081, Q16569609, Q131442881 | |
| worrall | unresolved | Robert B. Wormald Q16597044, do not substitute | catalogue conflates Worrall (C86) and Wormald (C77) |
| gajewski | Gajewski, Grzegorz Q4131618 | film director Q22115069; actor/director Q122641815 | plwiki "(szachista)" |
| abonyi | Abonyi, István Q732901 | politician Q111607676, engineer Q139576109, forestry engineer Q125590062 | |
| kondratiyev | Kondratiyev, Pavel Q117532 | Vissarion Kondratiev Q104149817; variants Kondratyev/Kondratev/Kondratjew | |
| brentano | Brentano, Franz Q57196 | painter Q94831774, Franz Dominicus Q1446569, Franz Anton Q53157132 | philosopher has no chess occupation, so an occupation filter wrongly rejects him |
| rubtsova | Rubtsova, Olga Q254159 | Tatyana Rubtsova Q529790; Alexander Rubtsov Q122955247 | |
| philidor | Philidor, François-André Q203229 | Danican Philidor musical dynasty; Q124786266 (19th-c official, same full name) | only Q203229 is a chess player |
| hanham | Hanham, James Q6135487 | Dorset baronets Q75279792, Q75743707 | only chess Hanham |
| fischer | Fischer, Robert James Q41314 | 8 chess Fischers Q71318786, Q71304137, Q28481027, Q109381919, Q71321312, Q71291186 | KG Fischer Defence is Bobby's own |
| becker | Becker, Albert Q84930 | 10 chess Beckers (Q1382864, Q10299796, Q30310067...); composer Q566825, painter Q52822161, historian Q2637591, disambig Q2637600 | |
| carrera | Carrera, Pietro Q631673 | architect Pietro Carrera Q132987130 | only Q631673 is chess |
| spassky | Spassky, Boris Q177310 | Georgy Spassky Q71291438; physicist Boris Spassky Q21148694; Boris Spassky Jr Q140077276 | |
| reti | Réti, Richard Q312985 | brother Rudolph Réti, musicologist | |
| grivas | Grivas, Efstratios Q641271 | Georgios Grivas (EOKA leader) | |
| owen | Owen, John Q1386704 | epigrammatist Q1230607, politician Q883201; chess Michael Owen Q109423199 | the Reverend John Owen of Liverpool |
| karklins | Karklins, Andrew Q71293221 | father Erik Karklins (Riga/Chicago master, no QID) | the opening is the son's |
| short | Short, Nigel Q313778 | Philip Short Q2854985 (chess); conductor Nigel Short Q17059055 | |
| tan | Tan, Zhongyi Q7682163 | Tan Lian Ann Q7682088, Tan Chengxuan Q7682032, Hiong Liong Tan Q2227116, Justin Tan Q27533018/Q106232451 | |
| lasker | Lasker, Emanuel Q57095 | Edward Lasker (1885-1981) | the listed openings are Emanuel's |
| martinovsky | Martinovsky, Eugene Q65697695 | Slobodan Martinović (GM, different spelling) | co-eponym Karklins is a separate person |
| ding | Ding, Liren Q1191198 | WGM Ding Yixin | world champion |
| koneru | Koneru, Humpy Q255044 | father and first coach Koneru Ashok, also a player | |
| mikenas | Mikėnas, Vladas Q715582 | Alius Mikėnas Q21789881 (b. 1955) | 1910-1992 |
| evans | Evans, William Q456905 | Larry Evans Q725629, Larry D. Evans Q27524893, Deborah Evans-Quek Q108563023 | gambit is the 19th-c captain |
| anderssen | Anderssen, Adolf Q57155 | Ulf Andersson Q434364 (near-homograph) | a spelling normalisation must not collapse the two |
| urusov | Urusov, Sergey Q1428416 | brother Dmitry Urusov Q4477389; Q3479756, Q4477401, Q124459937 | only Q1428416, b. 1827 |
| englund | Englund, Fritz Q1465925 | Henry Charlick Q5719343 shares the gambit's P138 | the Englund label is Q1465925 |
| knorre | Knorre, Viktor Q62371 | astronomer dynasty: Ernst Friedrich, Karl Friedrich Q85243 | item is described as astronomer, so a naive occupation filter drops him |

## 5. Unresolved

### 5a. not-found (13)

| person_id | Name as held | Why null | What a human must check |
|---|---|---|---|
| gusev | Gusev, Yuri | Sources name Soviet master Nikolai Nikolaevich Gusev; no Wikidata item, and Yury Gusev Q21638545 has no sourced link to the line | Confirm the eponym, then either mint a Wikidata item or keep null. Do not attach Q21638545. |
| zilbermints | Zilbermints, Lev | Only the opening exists (Q3171706, no P138, no linked person) | Decide whether to create a person item; never borrow the opening QID. |
| vinogradov | Vinogradov, Paul | No verifiable chess player; Wikipedia mislinks to legal historian Q1976412 | Whether the eponym claim should survive at all. |
| morrison | Morrison, John | Corrupt PGN header: all 10 games are Lasker vs Schlechter, wch 10th 1910 | Data repair, not identity: remap to the existing `schlechter` row (Q320017). Same corruption class as `forgacs` standing in for Janowski in wch 11th. |
| hopton | Hopton | Zero Hopton rows among Wikidata chess players; trail ends at "R. Hopton", one 1860 game | Accept null or drop the eponym. |
| dory | Döry, Ladislaus | Ladislaus Döry von Jobbaháza has no item; chessgames dates him 1897 Austria | Source the player before creating anything; Q27579527 and Q111270511 are both wrong. |
| jerome | Jerome, Alonzo Wheeler (1834-1902) | Documented on enwiki, no Wikidata item; gambit Q1687720 has no P138 | Keep the dates with a null QID, or create the item. |
| lamb | Lamb, F. | No chess Lamb on Wikidata; BDG sources describe the line but never the person | Whether "F. Lamb" is a person at all. |
| adler | Adler, Mór | Played the first known Budapest Gambit game vs Maróczy, 5 Mar 1896; no item | Hungarian-language sources. Q504223 (painter) is a decoy. |
| desprez | Desprez, Marcel | enwiki red-links "Marcel Després"; nothing on Wikidata | Also decide the eponym: the same opening is the Kádas Opening after Gábor Kádas. Spelling Desprez/Després unresolved. |
| parham | Parham, Bernard | Real and correctly named, but no enwiki article and no Wikidata entity | Create the item or accept null; the opening item Q1671558 carries no P138 to borrow. |
| worrall | Worrall, Thomas Herbert | No item; Q75545278 has wrong dates and no occupation | Bigger issue: row C.RyL.Mor.Wor is canonically the **Wormald** Attack (C77) while the evidence file credits **Worrall** (C86), and separate C86 rows already say "Worrall Attack". Naming decision required. |
| dracula | Dracula, Count | Not a person; the pair-eponym of the Frankenstein-Dracula Variation, coined by Tim Harding 1976 | Recommend dropping the row. Q3266236 exists but is a fictional character. |

### 5b. medium confidence (4)

| person_id | Assigned | Why only medium | Human check |
|---|---|---|---|
| popov | Q65695255 Popov, Georgi Alexandrov | Dates-less ICCF-derived stub, no sitelinks, no cross-check possible; the eponym claim itself is a Wikipedia red link | Confirm the Bulgarian correspondence player and source birth/death. |
| martinovsky | Q65697695 Martinovsky, Eugene | Bare ICCF import, no dates, no sitelinks; the OTB-to-correspondence identity link is inferred from the distinctive name, not asserted on the item | Confirm the Chicago OTB master is the same man; he died shortly before the Feb-Mar 2002 memorial named for him. |
| monster | Q2021531 Frankenstein's monster | Fictional character, not a person; the counterpart eponym (Count Dracula) is missing from the catalogue | Decide whether fictional eponyms belong in a people table at all; pairs with `dracula`. |
| chesscom | Q16829376 Chess.com | Entity match is certain but it is an organisation. The real Bongcloud eponym is the pseudonymous site user Lenny_Bongcloud | Editorial: this is probably a catalogue error, not a company row. |

### 5c. resolved high, still needs a human

| person_id | Issue |
|---|---|
| marshall / marshall-viele | The two notes contradict each other on whether they may share Q312814. See §2. |
| kushnir-aleksandr | Safe to resolve, but the display-name fix must ship in the same change or the challenger stays labelled with a man's forename. |
| dunst | Q596219 (Dunst Opening, P138 to Q63125490) vs Van Geet Opening, whose eponym is Dick van Geet Q2902350. Same 1.Nc3; confirm which eponym this row carries. |
| petrov | Wikidata P569 says 1799-02-02 (unsourced Wikipedia import); item description and enwiki say 1794. 1794 reported. |
| bird | 1829 used (baptismal-record correction, matches existing CSV); Wikidata still records 1830-07-14. |
| torre | 1904 from the preferred-rank claim; a normal-rank 1905 claim also exists. |
| alburt | Wikidata carries 1945-08-21, 1945 and 1946; enwiki gives 1945. |
| lucena | Wikidata carries both 1465 and 1475 for birth; both dates are circa. |
| eisenberg | Death recorded as unknown value; enwiki says "after 1920". Died field left empty. |
| amar | Q63125130 is thin (no dates, no sitelinks, no references); dates left empty deliberately. |
| durkin | Death 2014 comes from Wikipedia only; Wikidata holds birth alone. |
| salvio, polerio, cozio, stamma, greco, segura | Year-precision dates with circa qualifiers; do not present as exact. |
| greco | The listed opening string names McConnell, not Greco; the row's eponym mapping deserves a look. |
| ilyingenevsky | Catalogue spells the variation "Ilyin-Zhenevsky", the person row "Ilyin-Genevsky"; same man, two transliterations. |