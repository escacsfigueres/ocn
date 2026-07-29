//! Where the crate earns trust.
//!
//! Three gates, in order of how much they would hurt to get wrong:
//!
//! 1. **The public Polyglot vectors.** Annex A makes the book hash
//!    normative, which means OCN does not get to have an opinion about
//!    its value: a hash that disagrees with the public book format is
//!    simply wrong, and every `.bin` opening book and every consumer
//!    joining on the number would silently miss.
//! 2. **The whole catalogue, cross-validated against Python.** Every row
//!    of the embedded positions sidecar was produced by
//!    `src/ocn/fen.py` and `tools/polyglot_zobrist.py`. Recomputing both
//!    columns here and demanding equality proves the two implementations
//!    agree on 5,894 real positions, with no fixtures to maintain.
//! 3. **The en-passant trap, isolated.** Rule 4 of Annex A is the one
//!    place a plausible-looking implementation silently returns nothing,
//!    so it gets pins of its own in both directions, pins included.

use super::*;
use crate::fen::{square_name, Position, FILES};
use crate::zobrist::{
    piece_kind, polyglot_hash, CASTLING_BASE, EN_PASSANT_BASE, RANDOM_KEYS, TURN_INDEX,
};

// ------------------------------------------------------- the public vectors

/// The published Polyglot test vectors: `(description, FEN as a board
/// library emits it, the OCN `fen_key`, the key)`.
///
/// The FENs are the always-emit form — the en-passant square printed
/// after every double push — which is exactly what makes them a test of
/// rule 4 and not merely of the XOR. Three of them carry an en-passant
/// square that must be **dropped** before hashing (`e3`, `d6`), and two
/// carry one that must be **kept** (`f6`, `c3`). Every value below was
/// emitted by the Python implementation in this repository, not
/// transcribed.
const PUBLIC_VECTORS: &[(&str, &str, &str, u64)] = &[
    (
        "initial position",
        "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
        "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -",
        0x463B96181691FC9C,
    ),
    (
        "1.e4 — the e3 square nobody can capture on",
        "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1",
        "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq -",
        0x823C9B50FD114196,
    ),
    (
        "1.e4 d5 — likewise d6",
        "rnbqkbnr/ppp1pppp/8/3p4/4P3/8/PPPP1PPP/RNBQKBNR w KQkq d6 0 2",
        "rnbqkbnr/ppp1pppp/8/3p4/4P3/8/PPPP1PPP/RNBQKBNR w KQkq -",
        0x0756B94461C50FB0,
    ),
    (
        "1.e4 d5 2.e5",
        "rnbqkbnr/ppp1pppp/8/3pP3/8/8/PPPP1PPP/RNBQKBNR b KQkq - 0 2",
        "rnbqkbnr/ppp1pppp/8/3pP3/8/8/PPPP1PPP/RNBQKBNR b KQkq -",
        0x662FAFB965DB29D4,
    ),
    (
        "1.e4 d5 2.e5 f5 — the famous one: exf6 is legal, so f6 stays",
        "rnbqkbnr/ppp1p1pp/8/3pPp2/8/8/PPPP1PPP/RNBQKBNR w KQkq f6 0 3",
        "rnbqkbnr/ppp1p1pp/8/3pPp2/8/8/PPPP1PPP/RNBQKBNR w KQkq f6",
        0x22A48B5A8E47FF78,
    ),
    (
        "1.e4 d5 2.e5 f5 3.Ke2 — the king move drops both white rights",
        "rnbqkbnr/ppp1p1pp/8/3pPp2/8/8/PPPPKPPP/RNBQ1BNR b kq - 1 3",
        "rnbqkbnr/ppp1p1pp/8/3pPp2/8/8/PPPPKPPP/RNBQ1BNR b kq -",
        0x652A607CA3F242C1,
    ),
    (
        "1.e4 d5 2.e5 f5 3.Ke2 Kf7 — and the black ones",
        "rnbq1bnr/ppp1pkpp/8/3pPp2/8/8/PPPPKPPP/RNBQ1BNR w - - 2 4",
        "rnbq1bnr/ppp1pkpp/8/3pPp2/8/8/PPPPKPPP/RNBQ1BNR w - -",
        0x00FDD303C946BDD9,
    ),
    (
        "1.a4 b5 2.h4 b4 3.c4 — bxc3 is legal, so c3 stays",
        "rnbqkbnr/p1pppppp/8/8/PpP4P/8/1P1PPPP1/RNBQKBNR b KQkq c3 0 3",
        "rnbqkbnr/p1pppppp/8/8/PpP4P/8/1P1PPPP1/RNBQKBNR b KQkq c3",
        0x3C8123EA7B067637,
    ),
    (
        "1.a4 b5 2.h4 b4 3.c4 bxc3 4.Ra3 — the rook move costs White Q-side",
        "rnbqkbnr/p1pppppp/8/8/P6P/R1p5/1P1PPPP1/1NBQKBNR b Kkq - 1 4",
        "rnbqkbnr/p1pppppp/8/8/P6P/R1p5/1P1PPPP1/1NBQKBNR b Kkq -",
        0x5C3F9B829B279560,
    ),
];

#[test]
fn every_published_polyglot_vector_matches_exactly() {
    for (description, fen, _, expected) in PUBLIC_VECTORS {
        let actual = polyglot_hash_from_fen(fen).expect(description);
        assert_eq!(
            actual, *expected,
            "{description}: Polyglot key mismatch, got {actual:#018X}"
        );
    }
}

#[test]
fn every_published_vector_normalises_to_its_documented_key() {
    for (description, fen, key, _) in PUBLIC_VECTORS {
        assert_eq!(&fen_key(fen).expect(description), key, "{description}");
    }
}

#[test]
fn the_initial_position_matches_the_documented_unsigned_decimal() {
    // The sidecar ships the column as unsigned decimal, so the one
    // position everybody can check is pinned in that form too.
    let start = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1";
    assert_eq!(polyglot_hash_from_fen(start).unwrap(), 5060803636482931868);
}

#[test]
fn the_key_table_has_781_distinct_entries() {
    // A truncated or duplicated paste fails here rather than corrupting a
    // release.
    assert_eq!(RANDOM_KEYS.len(), 781);
    let distinct: BTreeSet<u64> = RANDOM_KEYS.iter().copied().collect();
    assert_eq!(distinct.len(), 781);
}

#[test]
fn the_offsets_partition_the_key_table() {
    assert_eq!(CASTLING_BASE, 768); // 12 kinds * 64 squares
    assert_eq!(EN_PASSANT_BASE, 772); // + 4 castling rights
    assert_eq!(TURN_INDEX, 780); // + 8 en-passant files
    assert_eq!(TURN_INDEX + 1, RANDOM_KEYS.len());
}

#[test]
fn piece_kinds_cover_both_colours_and_nothing_else() {
    let kinds: BTreeSet<usize> = b"pPnNbBrRqQkK"
        .iter()
        .filter_map(|b| piece_kind(*b))
        .collect();
    assert_eq!(kinds, (0..12).collect::<BTreeSet<usize>>());
    assert_eq!(piece_kind(0), None);
    assert_eq!(piece_kind(b'x'), None);
}

// ------------------------------------------------------- the en-passant trap

#[test]
fn an_en_passant_square_nobody_can_capture_on_is_dropped() {
    // 1.d4 Nf6 2.c4 is a double push with no black pawn beside it.
    let fen = "rnbqkb1r/pppppppp/5n2/8/2PP4/8/PP2PPPP/RNBQKBNR b KQkq c3 0 2";
    let position = Position::parse(fen).unwrap();
    assert_eq!(position.ep_square(), Some(18)); // c3, as written
    assert_eq!(position.legal_ep_square().unwrap(), None); // ... and as meant
    assert!(fen_key(fen).unwrap().ends_with(" b KQkq -"));
}

#[test]
fn an_en_passant_square_a_pawn_can_capture_on_is_kept() {
    // 1.a4 b5 2.h4 b4 3.c4: bxc3 is available, so the square is identity.
    let fen = "rnbqkbnr/p1pppppp/8/8/PpP4P/8/1P1PPPP1/RNBQKBNR b KQkq c3 0 3";
    assert!(fen_key(fen).unwrap().ends_with(" b KQkq c3"));
}

#[test]
fn a_pinned_pawn_cannot_capture_so_the_square_is_dropped() {
    // Black king a3, white bishop c5: the b4 pawn is pinned along the
    // a3-b4-c5 diagonal, and bxc3 would step off it into check.
    let pinned = "8/8/8/2B5/1pP5/k7/8/4K3 b - c3 0 1";
    assert!(fen_key(pinned).unwrap().ends_with(" b - -"));

    // The same position with the bishop one square off the pin ray: now
    // the capture is legal and the square survives. One piece moved, the
    // position identity changes in the en-passant field.
    let free = "8/8/8/3B4/1pP5/k7/8/4K3 b - c3 0 1";
    assert!(fen_key(free).unwrap().ends_with(" b - c3"));
}

#[test]
fn a_capture_that_opens_a_rank_onto_its_own_king_is_illegal() {
    // The case that needs the capture to be *made* before it can be
    // judged: gxf6 removes the f5 pawn and vacates g5, clearing two men
    // off rank 5 at once and exposing the white king on h5 to the a5 rook.
    let exposed = "k7/8/8/r4pPK/8/8/8/8 w - f6 0 1";
    assert!(fen_key(exposed).unwrap().ends_with(" w - -"));

    // Block the rook's path and the same capture becomes legal.
    let blocked = "k7/8/8/rb3pPK/8/8/8/8 w - f6 0 1";
    assert!(fen_key(blocked).unwrap().ends_with(" w - f6"));
}

#[test]
fn the_hash_follows_the_fen_key_en_passant_rule() {
    // The two encodings of Annex A must never disagree about en passant:
    // same rule, same position, one identity. The pair below differs only
    // in whether the capture is legal, so the hashes must differ by
    // exactly the c-file en-passant key.
    let pinned = "8/8/8/2B5/1pP5/k7/8/4K3 b - c3 0 1";
    let same_without_ep = "8/8/8/2B5/1pP5/k7/8/4K3 b - - 0 1";
    assert_eq!(
        polyglot_hash_from_fen(pinned).unwrap(),
        polyglot_hash_from_fen(same_without_ep).unwrap()
    );

    let free = "8/8/8/3B4/1pP5/k7/8/4K3 b - c3 0 1";
    let free_without_ep = "8/8/8/3B4/1pP5/k7/8/4K3 b - - 0 1";
    assert_eq!(
        polyglot_hash_from_fen(free).unwrap() ^ polyglot_hash_from_fen(free_without_ep).unwrap(),
        RANDOM_KEYS[EN_PASSANT_BASE + 2], // the c-file
    );
}

#[test]
fn move_counters_are_not_part_of_position_identity() {
    let four = "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq -";
    let six = "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 99 250";
    assert_eq!(fen_key(four).unwrap(), fen_key(six).unwrap());
}

#[test]
fn malformed_fens_are_rejected_with_the_offending_field() {
    use crate::fen::FenError;
    type Expectation = fn(&FenError) -> bool;
    let cases: &[(&str, Expectation)] = &[
        ("8/8/8/8/8/8/8/8 w", |e| {
            matches!(e, FenError::FieldCount(2))
        }),
        ("8/8/8/8/8/8/8/8 w - - 0 1 extra", |e| {
            matches!(e, FenError::FieldCount(7))
        }),
        ("8/8/8/8/8/8/8 w - -", |e| matches!(e, FenError::Board(_))),
        ("8/8/8/8/8/8/8/9 w - -", |e| matches!(e, FenError::Board(_))),
        ("8/8/8/8/8/8/8/pppppppppp w - -", |e| {
            matches!(e, FenError::Board(_))
        }),
        ("8/8/8/8/8/8/8/8 x - -", |e| matches!(e, FenError::Turn(_))),
        ("8/8/8/8/8/8/8/8 w KKq -", |e| {
            matches!(e, FenError::Castling(_))
        }),
        ("8/8/8/8/8/8/8/8 w - e4", |e| {
            matches!(e, FenError::EnPassant(_))
        }),
        ("8/8/8/8/8/8/8/8 w - - x 1", |e| {
            matches!(e, FenError::Counters(_))
        }),
        ("8/8/8/8/8/8/8/8 w - - 0 0", |e| {
            matches!(e, FenError::Counters(_))
        }),
    ];
    for (fen, is_expected) in cases {
        let error = fen_key(fen).expect_err(fen);
        assert!(is_expected(&error), "{fen}: unexpected {error:?}");
        // Every variant renders a message a human can act on.
        assert!(!error.to_string().is_empty());
    }
}

#[test]
fn legality_is_undecidable_without_the_capturing_side_s_king() {
    // No white king, and a white pawn that would have to capture en
    // passant: Python raises here rather than guessing, and so do we.
    let fen = "4k3/8/8/3pP3/8/8/8/8 w - d6 0 1";
    assert!(matches!(
        fen_key(fen),
        Err(crate::fen::FenError::IllegalPosition(_))
    ));

    // Without the en-passant question there is nothing to decide, so the
    // same kingless board keys fine.
    let quiet = "4k3/8/8/3pP3/8/8/8/8 w - - 0 1";
    assert!(fen_key(quiet).is_ok());
}

// ------------------------------------------- the whole catalogue, vs Python

/// The last move of `moves_uci` as an always-emit en-passant square.
///
/// `Some(square)` when the line ends in a pawn double push, which is
/// exactly when a board library would print an en-passant square whether
/// or not the capture is legal. Reconstructing that string lets the
/// cross-check feed the *unnormalised* FEN — the one real consumers hold
/// — through `fen_key` and demand the catalogue's answer back.
fn always_emit_ep_square(placement: &str, moves_uci: &str) -> Option<String> {
    let last = moves_uci.split_whitespace().next_back()?;
    let bytes = last.as_bytes();
    if bytes.len() < 4 {
        return None;
    }
    let src_file = FILES.iter().position(|f| *f == bytes[0])?;
    let src_rank = (bytes[1] as char).to_digit(10)? as i32;
    let dst_file = FILES.iter().position(|f| *f == bytes[2])?;
    let dst_rank = (bytes[3] as char).to_digit(10)? as i32;
    if src_file != dst_file || (dst_rank - src_rank).abs() != 2 {
        return None;
    }
    // A rook or queen can also travel two ranks up a file; only a pawn
    // leaves an en-passant square behind it.
    let position = Position::parse(&format!("{placement} w - - 0 1")).ok()?;
    let landed = position.squares()[((dst_rank - 1) * 8) as usize + dst_file];
    if !landed.eq_ignore_ascii_case(&b'p') {
        return None;
    }
    Some(square_name(
        (((src_rank + dst_rank) / 2 - 1) * 8) as usize + src_file,
    ))
}

struct CrossCheck {
    rows: usize,
    double_pushes: usize,
    ep_kept: usize,
}

/// Recompute both derived position columns for every catalogue row.
fn cross_check_the_whole_catalogue() -> CrossCheck {
    let table = Table::parse(POSITIONS_TSV, '\t');
    let mut seen = CrossCheck {
        rows: 0,
        double_pushes: 0,
        ep_kept: 0,
    };

    for record in &table.records {
        let slug = table.field(record, "ocn1");
        let fen = table.field(record, "fen");
        let expected_key = table.field(record, "fen_key");
        let expected_epd = table.field(record, "epd");
        let expected_hash: u64 = table
            .field(record, "zobrist")
            .parse()
            .unwrap_or_else(|_| panic!("{slug}: unparseable zobrist column"));

        let position = Position::parse(fen).unwrap_or_else(|e| panic!("{slug}: {e}"));
        assert_eq!(
            position.fen_key().unwrap_or_else(|e| panic!("{slug}: {e}")),
            expected_key,
            "{slug}: fen_key disagrees with the Python-derived column"
        );
        assert_eq!(
            polyglot_hash(&position).unwrap_or_else(|e| panic!("{slug}: {e}")),
            expected_hash,
            "{slug}: Polyglot hash disagrees with the Python-derived column"
        );
        // Annex A: EPD's four fields are `fen_key`'s four fields.
        assert_eq!(expected_epd, expected_key, "{slug}: epd/fen_key divergence");
        seen.rows += 1;
        if !expected_key.ends_with(" -") {
            seen.ep_kept += 1;
        }

        // Now the harder direction: hand the same position back in the
        // form a board library would print it, en-passant square and all.
        let placement = expected_key.split(' ').next().unwrap();
        if let Some(ep) = always_emit_ep_square(placement, table.field(record, "moves_uci")) {
            seen.double_pushes += 1;
            let fields: Vec<&str> = fen.split(' ').collect();
            let always_emit = format!(
                "{} {} {} {} {} {}",
                fields[0], fields[1], fields[2], ep, fields[4], fields[5]
            );
            assert_eq!(
                fen_key(&always_emit).unwrap_or_else(|e| panic!("{slug}: {e}")),
                expected_key,
                "{slug}: rule 4 mis-decided on the always-emit form {always_emit}"
            );
            assert_eq!(
                polyglot_hash_from_fen(&always_emit).unwrap(),
                expected_hash,
                "{slug}: hash changed with the always-emit en-passant square"
            );
        }
    }
    seen
}

#[test]
fn the_whole_catalogue_agrees_with_the_python_implementation() {
    let seen = cross_check_the_whole_catalogue();
    // Every concrete row of the 5,899-row catalogue; the five class roots
    // hold no position and are not in the sidecar.
    assert_eq!(seen.rows, 5894, "the positions sidecar changed size");
    assert_eq!(seen.rows, Catalog::load().len() - 5);
}

#[test]
fn rule_4_is_exercised_in_both_directions_by_the_catalogue() {
    // The cross-check is only worth its runtime if the catalogue actually
    // makes rule 4 decide something. It does, 1,084 times: an en-passant
    // square is on the board, and 1,063 times it must come off again.
    let seen = cross_check_the_whole_catalogue();
    assert_eq!(seen.double_pushes, 1084);
    assert_eq!(seen.ep_kept, 21);
    assert_eq!(seen.double_pushes - seen.ep_kept, 1063);
}

// --------------------------------------------------------------- the fold

#[test]
fn the_fold_is_case_and_diacritic_insensitive() {
    assert_eq!(fold("Grünfeld"), "grunfeld");
    assert_eq!(fold("GRÜNFELD"), "grunfeld");
    assert_eq!(fold("  grunfeld  "), "grunfeld");
    assert_eq!(fold("Réti"), "reti");
    assert_eq!(fold("Bogoljubov"), "bogoljubov");
    assert_eq!(fold("Sicilian Defence"), "sicilian defence");
}

#[test]
fn the_fold_keeps_the_characters_nfkd_does_not_decompose() {
    // `ø` has no NFKD decomposition, so Python's fold leaves it alone and
    // so must this one: folding it to `o` would make the two
    // implementations index different keys.
    assert_eq!(fold("Ø"), "ø");
    assert_eq!(fold("Løwenthal"), "løwenthal");
    // `ß` casefolds to `ss`, which is not a diacritic question at all.
    assert_eq!(fold("STRAßE"), "strasse");
    assert_eq!(fold("Straße"), "strasse");
}

#[test]
fn every_catalogue_name_folds_to_something_findable() {
    // The property that matters: whatever a row is called, looking that
    // name up finds the row back.
    let catalog = Catalog::load();
    for row in catalog.iter().take(400) {
        let hits = catalog.by_name(&row.canonical_name);
        assert!(
            hits.iter().any(|hit| hit.ocn1 == row.ocn1),
            "{}: by_name({:?}) lost its own row",
            row.ocn1,
            row.canonical_name
        );
    }
}

// ------------------------------------------------------- the delimited text

#[test]
fn the_reader_honours_rfc_4180_quoting() {
    let text = "a,b,c\n1,\"two, with a comma\",3\n4,\"a \"\"quoted\"\" word\",6\n";
    let table = Table::parse(text, ',');
    assert_eq!(table.records.len(), 2);
    assert_eq!(table.field(&table.records[0], "b"), "two, with a comma");
    assert_eq!(table.field(&table.records[1], "b"), "a \"quoted\" word");
    assert_eq!(table.field(&table.records[1], "missing"), "");
}

#[test]
fn the_reader_survives_a_missing_trailing_newline_and_crlf() {
    assert_eq!(Table::parse("a,b\r\n1,2\r\n", ',').records.len(), 1);
    assert_eq!(Table::parse("a,b\n1,2", ',').records.len(), 1);
    assert_eq!(Table::parse("", ',').records.len(), 0);
}

#[test]
fn a_caller_can_bring_its_own_catalogue() {
    // The release-download path: someone pins an older catalogue, or a
    // slice of one, and reads it with this crate.
    let csv = "ocn1,canonical_name,eco_legacy,parent_ocn1,moves_uci,depth,aliases,flags,\
               notes,attributed_to,attribution_source,historical_notes,transposes_to,same_as\n\
               B,Semi-Open Games,,,,0,,,,,,,,\n\
               B.Sic,\"Sicilian Defence, a comma\",B20|B21,B,e2e4 c7c5,1,Sicilian,popular|tabiya,\
               a note,,,,,B.Other\n";
    let tsv = "ocn1\tfen_key\n\
               B.Sic\trnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq -\n";
    let catalog = Catalog::parse(csv, Some(tsv));

    assert_eq!(catalog.len(), 2);
    let sicilian = catalog.by_slug("B.Sic").unwrap();
    assert_eq!(sicilian.canonical_name, "Sicilian Defence, a comma");
    assert_eq!(sicilian.eco, ["B20", "B21"]);
    assert_eq!(sicilian.moves_uci, ["e2e4", "c7c5"]);
    assert_eq!(sicilian.aliases, ["Sicilian"]);
    assert_eq!(
        sicilian
            .flags
            .iter()
            .map(String::as_str)
            .collect::<Vec<_>>(),
        ["popular", "tabiya"]
    );
    assert_eq!(sicilian.same_as, ["B.Other"]);
    assert_eq!(sicilian.transposes_to, None);
    assert!(catalog.by_slug("B").unwrap().is_class_root());
    assert_eq!(catalog.by_name("sicilian")[0].ocn1, "B.Sic");
    assert_eq!(
        catalog
            .by_fen("rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2")
            .unwrap()[0]
            .ocn1,
        "B.Sic"
    );

    // Without a sidecar there is no position index at all: this crate
    // carries no move generator, so it cannot derive one.
    let no_index = Catalog::parse(csv, None);
    assert_eq!(no_index.len(), 2);
    assert!(no_index
        .by_fen("rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq -")
        .unwrap()
        .is_empty());
}

#[test]
fn the_catalogue_csv_parses_into_the_expected_shape() {
    let catalog = Catalog::load();
    assert_eq!(catalog.len(), 5899);
    assert!(!catalog.is_empty());
    // The five class roots carry no moves and no parent.
    let roots: Vec<&Row> = catalog.iter().filter(|row| row.is_class_root()).collect();
    assert_eq!(roots.len(), 5);
    assert!(roots.iter().all(|row| row.parent.is_none()));
    assert_eq!(
        roots
            .iter()
            .map(|row| row.ocn1.as_str())
            .collect::<Vec<_>>(),
        ["A", "B", "C", "D", "E"]
    );
    // A name with a comma proves the quoted field survived the reader.
    assert_eq!(
        catalog.by_slug("B.Sic.Naj.Eng").unwrap().canonical_name,
        "Sicilian Najdorf, English Attack"
    );
}
