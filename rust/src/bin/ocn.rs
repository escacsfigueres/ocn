//! The `ocn` command line, mirroring the Python reader's shape.
//!
//! ```text
//! ocn lookup B90                  # ECO code, OCN slug or opening name
//! ocn lookup B.Sic.Naj.Eng
//! ocn lookup najdorf
//! ocn fen "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2"
//! ocn version
//! ```
//!
//! Exit codes: 0 on a hit, 1 on no match, 2 on a usage or input error.
//! Argument parsing is by hand, on purpose: the crate has no runtime
//! dependency and three subcommands do not justify acquiring one.

use std::process::ExitCode;

use ocn::{fen_key, Catalog, Row};

const EXIT_NO_MATCH: u8 = 1;
const EXIT_USAGE: u8 = 2;

const USAGE: &str = "\
Open Chess Naming: look up OCN-1 opening slugs, names and positions. The
catalogue is embedded in this binary; no network access and no other
dependency is used.

usage:
  ocn lookup <ECO code | OCN slug | name> [--limit N]
  ocn fen <FEN>
  ocn version
  ocn --help

Code MIT, embedded catalogue CC-BY-4.0.";

fn main() -> ExitCode {
    let args: Vec<String> = std::env::args().skip(1).collect();
    let Some(command) = args.first().map(String::as_str) else {
        println!("{USAGE}");
        return ExitCode::from(EXIT_USAGE);
    };

    match command {
        "-h" | "--help" | "help" => {
            println!("{USAGE}");
            ExitCode::SUCCESS
        }
        "-V" | "--version" | "version" => {
            let catalog = Catalog::load();
            println!(
                "ocn {} (catalogue {}, {} rows)",
                env!("CARGO_PKG_VERSION"),
                catalog.version(),
                catalog.len()
            );
            ExitCode::SUCCESS
        }
        "lookup" => lookup(&args[1..]),
        "fen" => fen(&args[1..]),
        other => fail(&format!("unknown command {other:?}; try `ocn --help`")),
    }
}

fn lookup(args: &[String]) -> ExitCode {
    let mut limit = 10usize;
    let mut words: Vec<&str> = Vec::new();
    let mut rest = args.iter();
    while let Some(arg) = rest.next() {
        if arg == "--limit" {
            match rest.next().and_then(|value| value.parse().ok()) {
                Some(value) => limit = value,
                None => return fail("--limit wants a number"),
            }
        } else {
            words.push(arg);
        }
    }

    let query = words.join(" ");
    let query = query.trim();
    if query.is_empty() {
        return fail("empty query");
    }

    let catalog = Catalog::load();
    // An ECO code is a class letter and two digits; anything else is a
    // slug if the catalogue knows it and free text otherwise.
    let bytes = query.as_bytes();
    let is_eco = bytes.len() == 3
        && matches!(bytes[0].to_ascii_uppercase(), b'A'..=b'E')
        && bytes[1..].iter().all(u8::is_ascii_digit);

    let (kind, rows) = if is_eco {
        ("ECO code", catalog.by_eco(query))
    } else if let Some(row) = catalog.by_slug(query) {
        ("OCN slug", vec![row])
    } else {
        let by_name = catalog.by_name(query);
        (
            "name",
            if by_name.is_empty() {
                catalog.search(query, limit)
            } else {
                by_name
            },
        )
    };

    if rows.is_empty() {
        eprintln!("ERROR: no OCN-1 match for {kind} {query:?}");
        return ExitCode::from(EXIT_NO_MATCH);
    }
    print_rows(catalog, rows.into_iter().take(limit));
    ExitCode::SUCCESS
}

fn fen(args: &[String]) -> ExitCode {
    let query = args.join(" ");
    let catalog = Catalog::load();
    let mut rows = match catalog.by_fen(query.trim()) {
        Ok(rows) => rows,
        Err(error) => return fail(&error.to_string()),
    };
    if rows.is_empty() {
        eprintln!("ERROR: no OCN-1 match for FEN position");
        eprintln!("  key  {}", fen_key(query.trim()).unwrap_or_default());
        return ExitCode::from(EXIT_NO_MATCH);
    }
    // Deepest first: the most specific name for the position on top.
    rows.sort_by(|a, b| b.depth.cmp(&a.depth).then_with(|| a.ocn1.cmp(&b.ocn1)));
    print_rows(catalog, rows.into_iter());
    ExitCode::SUCCESS
}

fn print_rows<'a>(catalog: &Catalog, rows: impl Iterator<Item = &'a Row>) {
    for (index, row) in rows.enumerate() {
        if index > 0 {
            println!();
        }
        println!("{}  {}", row.ocn1, row.canonical_name);
        println!("  eco    {}", or_dash(&row.eco.join("|")));
        println!("  moves  {}", or_dash(&row.moves_uci.join(" ")));
        let path: Vec<&str> = catalog
            .parents(&row.ocn1)
            .iter()
            .map(|parent| parent.ocn1.as_str())
            .collect();
        println!("  path   {}", or_dash(&path.join(" > ")));
        if let Some(canonical) = &row.transposes_to {
            println!("  canon  {canonical}");
        }
        if !row.same_as.is_empty() {
            println!("  same   {}", row.same_as.join("|"));
        }
    }
}

fn or_dash(text: &str) -> &str {
    if text.is_empty() {
        "-"
    } else {
        text
    }
}

fn fail(message: &str) -> ExitCode {
    eprintln!("ERROR: {message}");
    ExitCode::from(EXIT_USAGE)
}
