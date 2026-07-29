//! The public API, exercised the way a consumer would reach it.
//!
//! Everything here goes through `ocn::` — no private items, no test-only
//! helpers — so a change that keeps the internals working but breaks the
//! surface still fails.

use ocn::{fen_key, polyglot_hash_from_fen, Catalog};

#[test]
fn by_slug_returns_the_typed_row() {
    let cat = Catalog::load();
    let row = cat
        .by_slug("B.Sic.Naj.Eng")
        .expect("the Najdorf English Attack");
    assert_eq!(row.canonical_name, "Sicilian Najdorf, English Attack");
    assert_eq!(row.parent.as_deref(), Some("B.Sic.Naj"));
    assert_eq!(row.depth, 3, "B, B.Sic, B.Sic.Naj, then this row");
    assert_eq!(row.moves_uci.first().map(String::as_str), Some("e2e4"));
    assert!(row.eco.contains(&"B90".to_string()));
    assert!(!row.is_class_root());
    assert_eq!(cat.by_slug("B.Sic.NotAnOpening"), None);
}

#[test]
fn by_eco_comes_back_deepest_first() {
    let cat = Catalog::load();
    let rows = cat.by_eco("B90");
    assert!(!rows.is_empty(), "B90 must resolve to rows");
    let depths: Vec<u32> = rows.iter().map(|row| row.depth).collect();
    let mut sorted = depths.clone();
    sorted.sort_unstable_by(|a, b| b.cmp(a));
    assert_eq!(depths, sorted, "by_eco must return deepest first");
    assert!(rows.iter().any(|row| row.ocn1 == "B.Sic.Naj.Eng"));
    // The lookup is case- and whitespace-tolerant on the code itself.
    assert_eq!(cat.by_eco(" b90 ").len(), rows.len());
    assert!(cat.by_eco("Z99").is_empty());
}

#[test]
fn by_name_folds_case_and_diacritics() {
    let cat = Catalog::load();
    for query in ["Grunfeld", "grünfeld", "GRÜNFELD"] {
        let rows = cat.by_name(query);
        assert!(
            rows.iter().any(|row| row.ocn1 == "E.Gru"),
            "by_name({query:?}) must find E.Gru"
        );
    }
    assert!(cat.by_name("no such opening anywhere").is_empty());
}

#[test]
fn search_comes_back_broadest_first() {
    let cat = Catalog::load();
    let rows = cat.search("najdorf", 5);
    assert!(!rows.is_empty());
    assert!(rows.len() <= 5);
    let depths: Vec<u32> = rows.iter().map(|row| row.depth).collect();
    let mut sorted = depths.clone();
    sorted.sort_unstable();
    assert_eq!(depths, sorted, "search must return shallowest first");
    assert!(cat.search("   ", 5).is_empty());
}

#[test]
fn by_fen_normalises_the_en_passant_trap() {
    let cat = Catalog::load();
    // 1.e4 c5 as a board library prints it: the c6 square is on the FEN
    // and no white pawn can legally capture on it. Comparing the raw
    // string would find nothing; `by_fen` finds the Sicilian.
    let trap = "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2";
    let rows = cat.by_fen(trap).expect("a well-formed FEN");
    assert_eq!(rows.first().map(|row| row.ocn1.as_str()), Some("B.Sic"));

    // The same position with the square already normalised away, and as a
    // bare four-field key: one position, one answer.
    let normalised = "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq -";
    assert_eq!(cat.by_fen(normalised).unwrap(), rows);
    assert_eq!(cat.by_fen_key(&fen_key(trap).unwrap()), rows);

    // A legal position nobody named is a miss, not an error.
    assert!(cat
        .by_fen("4k3/8/8/8/8/8/8/4K3 w - - 0 1")
        .unwrap()
        .is_empty());
    // A malformed FEN is an error, not a silent miss.
    assert!(cat.by_fen("not a fen").is_err());
}

#[test]
fn parents_walks_the_breadcrumb_root_first() {
    let cat = Catalog::load();
    let path: Vec<&str> = cat
        .parents("B.Sic.Naj.Eng")
        .iter()
        .map(|row| row.ocn1.as_str())
        .collect();
    assert_eq!(path, ["B", "B.Sic", "B.Sic.Naj"]);
    assert!(cat.parents("B").is_empty(), "a class root has no parent");
    assert!(
        cat.parents("Nope").is_empty(),
        "an unknown slug has no path"
    );
}

#[test]
fn children_and_walk_agree_about_the_subtree() {
    let cat = Catalog::load();
    let children = cat.children("B.Sic.Naj");
    assert!(!children.is_empty());
    assert!(children
        .iter()
        .all(|row| row.parent.as_deref() == Some("B.Sic.Naj")));

    let subtree = cat.walk("B.Sic.Naj");
    assert_eq!(
        subtree[0].ocn1, "B.Sic.Naj",
        "walk starts at the row itself"
    );
    assert!(
        subtree.len() > children.len(),
        "the subtree is deeper than one generation"
    );
    for child in &children {
        assert!(subtree.iter().any(|row| row.ocn1 == child.ocn1));
    }
    assert!(cat.walk("Nope").is_empty());
}

#[test]
fn resolve_follows_transposes_to_exactly_once() {
    let cat = Catalog::load();
    // A canonical row resolves to itself.
    assert_eq!(cat.resolve("B.Sic"), Some("B.Sic"));
    assert_eq!(cat.resolve("no such slug"), None);

    // Every link in the catalogue points at a row that is itself
    // canonical: that is the contract that makes one hop the whole rule.
    let mut followed = 0usize;
    for row in cat.iter() {
        let Some(target) = &row.transposes_to else {
            continue;
        };
        followed += 1;
        assert_eq!(cat.resolve(&row.ocn1), Some(target.as_str()));
        let landed = cat.by_slug(target).expect("transposes_to must resolve");
        assert!(
            landed.transposes_to.is_none(),
            "{} -> {} chains, and links must not chain",
            row.ocn1,
            target
        );
    }
    assert!(followed > 0, "the catalogue carries transposition links");
}

#[test]
fn co_canonicals_are_symmetric_and_never_self_referential() {
    let cat = Catalog::load();
    let mut pairs = 0usize;
    for row in cat.iter() {
        for partner in cat.co_canonicals(&row.ocn1) {
            pairs += 1;
            assert_ne!(partner, &row.ocn1, "{}: same_as points at itself", row.ocn1);
            let other = cat.by_slug(partner).expect("same_as must resolve");
            assert!(
                other.same_as.contains(&row.ocn1),
                "{} lists {} but not the other way round",
                row.ocn1,
                partner
            );
        }
    }
    assert!(pairs > 0, "the catalogue carries co-canonical partners");
    assert!(cat.co_canonicals("no such slug").is_empty());
}

#[test]
fn the_catalogue_reports_its_own_size_and_release() {
    let cat = Catalog::load();
    assert_eq!(cat.len(), 5899);
    assert_eq!(cat.len(), cat.rows().len());
    assert_eq!(cat.iter().count(), cat.len());
    assert_eq!(cat.into_iter().count(), cat.len());
    assert_eq!(cat.version(), "1.2.1");
    // Loading twice hands back the same parsed catalogue, not a second one.
    assert!(std::ptr::eq(Catalog::load(), cat));
}

#[test]
fn the_position_helpers_are_reachable_without_a_catalogue() {
    // `fen_key` and the hash stand on their own: a consumer indexing its
    // own games needs the normalisation without loading 5,899 rows.
    let start = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1";
    assert_eq!(
        fen_key(start).unwrap(),
        "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -"
    );
    assert_eq!(polyglot_hash_from_fen(start).unwrap(), 0x463B96181691FC9C);
}
