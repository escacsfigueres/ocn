# ocn — Open Chess Naming, for Rust

[![Crates.io](https://img.shields.io/crates/v/ocn.svg)](https://crates.io/crates/ocn)
[![Docs.rs](https://docs.rs/ocn/badge.svg)](https://docs.rs/ocn)

**OCN** is a hierarchical, human-readable naming scheme for chess
openings: the layer over ECO and the Lichess opening names, not a
replacement for either. `B90` becomes `B.Sic.Naj.Eng`, and you can read
the class, the family, the variation and the tabiya straight off the
slug.

This crate is the Rust reader, with the **whole 5,899-opening catalogue
embedded in the binary**. No download, no database, no runtime
dependency, and the lookups work on a plane.

```bash
cargo add ocn
```

## Quickstart

```rust
use ocn::Catalog;

let cat = Catalog::load();                             // embedded, parsed once
let row = cat.by_slug("B.Sic.Naj.Eng").unwrap();
assert_eq!(row.canonical_name, "Sicilian Najdorf, English Attack");

let path: Vec<&str> = cat.parents("B.Sic.Naj.Eng").iter().map(|r| r.ocn1.as_str()).collect();
assert_eq!(path, ["B", "B.Sic", "B.Sic.Naj"]);         // the breadcrumb
assert!(!cat.by_eco("B90").is_empty());                // deepest first
assert!(!cat.by_name("Grunfeld").is_empty());          // case- and diacritic-folded

// 1.e4 c5, as a board library prints it — trailing en-passant square and all.
let fen = "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2";
assert_eq!(cat.by_fen(fen).unwrap()[0].ocn1, "B.Sic");
```

## The en-passant trap

That last line is the reason this crate exists rather than a
`HashMap<String, String>` you build yourself.

Spec [Annex A](https://github.com/escacsfigueres/ocn/blob/main/spec/OCN-1.md)
makes position identity the first four FEN fields, with the en-passant
square kept **only when an enemy pawn can legally capture on it**. Most
FEN emitters print the square after every double pawn push whether or
not the capture is legal, so a string that looks right never matches the
catalogue: the lookup returns nothing instead of failing loudly.

[`ocn::fen_key`] normalises to the legal-capture form, pins and
discovered checks included, and [`Catalog::by_fen`] applies it for you.
[`ocn::polyglot_hash`] computes the same position's Polyglot book hash
under the same rule, so the 64-bit key joins against `.bin` opening books
and the catalogue's own `zobrist` column.

The crate needs **no move generator** for any of this: positions are
looked up in the embedded index, and rule 4 is a question about a static
board.

## Cross-validated against the reference implementation

The catalogue's position columns are derived in Python
(`src/ocn/fen.py`, `tools/polyglot_zobrist.py`). This crate's test suite
recomputes both of them for **every one of the 5,894 concrete catalogue
rows** and demands equality — then re-feeds each position in the
always-emit form a board library would hand you, which makes rule 4
decide 1,084 more times (1,063 squares dropped, 21 kept). The seven
public Polyglot test vectors are pinned exactly on top of that.

## Command line

```bash
cargo install ocn --features cli

ocn lookup B90
ocn lookup B.Sic.Naj
ocn lookup najdorf
ocn fen "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2"
ocn version
```

Exit codes: 0 on a hit, 1 on no match, 2 on a usage or input error.

## Licensing

- **Code: MIT.**
- **Embedded catalogue: CC-BY-4.0.** The files under `data/` are the
  OCN-1 catalogue. Use, share and adapt them for any purpose, including
  commercial, provided you cite **"OCN, Club d'Escacs Figueres"** and
  link to <https://github.com/escacsfigueres/ocn>.

The full texts are `LICENSE-CODE` and `LICENSE-SPEC` in the repository.

## See also

- The spec, catalogue and issue tracker:
  <https://github.com/escacsfigueres/ocn>
- The Python package, same catalogue, same API shape:
  [`ocn-chess`](https://pypi.org/project/ocn-chess/)

[`ocn::fen_key`]: https://docs.rs/ocn/latest/ocn/fn.fen_key.html
[`ocn::polyglot_hash`]: https://docs.rs/ocn/latest/ocn/fn.polyglot_hash.html
[`Catalog::by_fen`]: https://docs.rs/ocn/latest/ocn/struct.Catalog.html#method.by_fen
