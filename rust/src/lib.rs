//! **OCN — Open Chess Naming**: the hierarchy layer over ECO and the
//! Lichess opening names, with the catalogue embedded in the binary.
//!
//! ```
//! use ocn::Catalog;
//!
//! let cat = Catalog::load();                                  // embedded, offline
//! let najdorf = cat.by_slug("B.Sic.Naj.Eng").unwrap();
//! assert_eq!(najdorf.canonical_name, "Sicilian Najdorf, English Attack");
//!
//! let path: Vec<&str> = cat.parents("B.Sic.Naj.Eng").iter().map(|r| r.ocn1.as_str()).collect();
//! assert_eq!(path, ["B", "B.Sic", "B.Sic.Naj"]);
//!
//! // The FEN most board libraries print after 1.e4 c5 carries an
//! // en-passant square no pawn can legally capture on. `by_fen`
//! // normalises it; comparing the raw string would silently miss.
//! let fen = "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2";
//! assert_eq!(cat.by_fen(fen).unwrap()[0].ocn1, "B.Sic");
//! ```
//!
//! # What is embedded
//!
//! The catalogue CSV and its position index travel inside the compiled
//! artefact: no download, no database, no runtime dependency, and the
//! lookups work on a plane. Position lookup is a hash-map hit against the
//! pre-computed index, never a move replay — the crate carries no move
//! generator at all.
//!
//! # Licensing
//!
//! The code is MIT. The **embedded catalogue is CC-BY-4.0**: cite "OCN,
//! Club d'Escacs Figueres" and link to
//! <https://github.com/escacsfigueres/ocn> when you redistribute the data.

#![forbid(unsafe_code)]
#![warn(missing_docs)]

pub mod fen;
mod fold;
pub mod zobrist;

use std::collections::{BTreeSet, HashMap};
use std::sync::OnceLock;

pub use fen::{fen_key, FenError, Position};
pub use fold::fold;
pub use zobrist::{polyglot_hash, polyglot_hash_from_fen};

/// The embedded catalogue, verbatim from `catalog/ocn-1.csv`.
const CATALOG_CSV: &str = include_str!("../data/ocn-1.csv");

/// The embedded position index, the artefact `tools/export_positions.py`
/// derives. Its `fen_key` column is the join key `by_fen` resolves to.
const POSITIONS_TSV: &str = include_str!("../data/ocn-1.positions.tsv");

/// The catalogue release the embedded data came from. Distinct from the
/// crate version, which tracks the reader.
const CATALOG_VERSION: &str = include_str!("../data/VERSION");

/// One catalogue entry, typed.
///
/// The CSV's pipe-separated multi-value fields (`eco_legacy`, `aliases`,
/// `flags`, `same_as`) arrive split; NULLs arrive as empty containers or
/// `None` rather than empty strings, so callers never re-implement the
/// same five "trim, or None" idioms.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Row {
    /// The OCN-1 slug, this row's stable identity (`B.Sic.Naj.Eng`).
    pub ocn1: String,
    /// The row's canonical English name.
    pub canonical_name: String,
    /// Every legacy ECO code the row covers, in catalogue order.
    pub eco: Vec<String>,
    /// The parent slug, `None` only for the five class roots.
    pub parent: Option<String>,
    /// The line that reaches this position, as UCI moves.
    pub moves_uci: Vec<String>,
    /// Depth in the hierarchy; a class root is 0.
    pub depth: u32,
    /// Alternative names this row answers to.
    pub aliases: Vec<String>,
    /// Catalogue flags, sorted and deduplicated.
    pub flags: BTreeSet<String>,
    /// Editorial notes.
    pub notes: String,
    /// Who the opening is attributed to, when the attribution is carried.
    pub attributed_to: String,
    /// The source backing `attributed_to`.
    pub attribution_source: String,
    /// Longer historical commentary.
    pub historical_notes: String,
    /// The FEN-canonical slug for this position, when this row is not it.
    pub transposes_to: Option<String>,
    /// Co-canonical partners: other legitimate names for this position.
    pub same_as: Vec<String>,
}

impl Row {
    /// True for the five family filters `A`-`E`, which hold no position.
    pub fn is_class_root(&self) -> bool {
        self.moves_uci.is_empty()
    }
}

/// An in-memory OCN-1 catalogue with the lookups consumers need.
#[derive(Debug)]
pub struct Catalog {
    rows: Vec<Row>,
    by_slug: HashMap<String, usize>,
    by_fen_key: HashMap<String, Vec<usize>>,
    by_eco: HashMap<String, Vec<usize>>,
    by_folded_name: HashMap<String, Vec<usize>>,
    children: HashMap<String, Vec<usize>>,
}

impl Catalog {
    /// The embedded catalogue, parsed once for the life of the process.
    ///
    /// Subsequent calls hand back the same instance, so a program that
    /// looks openings up in a loop pays the parse cost exactly once.
    pub fn load() -> &'static Catalog {
        static CATALOG: OnceLock<Catalog> = OnceLock::new();
        CATALOG.get_or_init(|| Catalog::parse(CATALOG_CSV, Some(POSITIONS_TSV)))
    }

    /// Parse a catalogue CSV, optionally with a positions sidecar.
    ///
    /// For consumers holding their own copy of the artefacts — a release
    /// download, a pinned older catalogue. Without a sidecar the position
    /// index is empty and [`Catalog::by_fen`] finds nothing: this crate
    /// carries no move generator, so it cannot derive positions itself.
    pub fn parse(catalog_csv: &str, positions_tsv: Option<&str>) -> Catalog {
        let table = Table::parse(catalog_csv, ',');
        let rows: Vec<Row> = table
            .records
            .iter()
            .map(|record| {
                let field = |name: &str| table.field(record, name);
                Row {
                    ocn1: field("ocn1").trim().to_string(),
                    canonical_name: field("canonical_name").trim().to_string(),
                    eco: split_pipes(field("eco_legacy")),
                    parent: optional(field("parent_ocn1")),
                    moves_uci: field("moves_uci")
                        .split_whitespace()
                        .map(str::to_string)
                        .collect(),
                    depth: field("depth").trim().parse().unwrap_or(0),
                    aliases: split_pipes(field("aliases")),
                    flags: split_pipes(field("flags")).into_iter().collect(),
                    notes: field("notes").trim().to_string(),
                    attributed_to: field("attributed_to").trim().to_string(),
                    attribution_source: field("attribution_source").trim().to_string(),
                    historical_notes: field("historical_notes").trim().to_string(),
                    transposes_to: optional(field("transposes_to")),
                    same_as: split_pipes(field("same_as")),
                }
            })
            .collect();

        let by_slug: HashMap<String, usize> = rows
            .iter()
            .enumerate()
            .map(|(index, row)| (row.ocn1.clone(), index))
            .collect();

        let mut by_eco: HashMap<String, Vec<usize>> = HashMap::new();
        let mut by_folded_name: HashMap<String, Vec<usize>> = HashMap::new();
        let mut children: HashMap<String, Vec<usize>> = HashMap::new();
        for (index, row) in rows.iter().enumerate() {
            for code in &row.eco {
                by_eco.entry(code.clone()).or_default().push(index);
            }
            for name in std::iter::once(&row.canonical_name).chain(row.aliases.iter()) {
                let key = fold(name);
                if key.is_empty() {
                    continue;
                }
                let bucket = by_folded_name.entry(key).or_default();
                // One row may reach the same key twice (a name repeated as
                // its own alias); it should still appear once.
                if bucket.last() != Some(&index) {
                    bucket.push(index);
                }
            }
            if let Some(parent) = &row.parent {
                children.entry(parent.clone()).or_default().push(index);
            }
        }
        // ECO is coarse — `B90` alone covers twenty OCN rows — so the
        // deepest-first order puts the most specific names on top.
        for bucket in by_eco.values_mut() {
            bucket.sort_by(|a, b| {
                rows[*b]
                    .depth
                    .cmp(&rows[*a].depth)
                    .then_with(|| rows[*a].ocn1.cmp(&rows[*b].ocn1))
            });
        }

        let mut by_fen_key: HashMap<String, Vec<usize>> = HashMap::new();
        if let Some(tsv) = positions_tsv {
            let positions = Table::parse(tsv, '\t');
            for record in &positions.records {
                let key = positions.field(record, "fen_key").trim();
                let slug = positions.field(record, "ocn1").trim();
                if key.is_empty() {
                    continue;
                }
                if let Some(index) = by_slug.get(slug) {
                    by_fen_key.entry(key.to_string()).or_default().push(*index);
                }
            }
        }

        Catalog {
            rows,
            by_slug,
            by_fen_key,
            by_eco,
            by_folded_name,
            children,
        }
    }

    /// The catalogue release the embedded data came from.
    ///
    /// Distinct from the crate version, which tracks the reader.
    pub fn version(&self) -> &'static str {
        CATALOG_VERSION.trim()
    }

    /// How many rows the catalogue holds.
    pub fn len(&self) -> usize {
        self.rows.len()
    }

    /// True when the catalogue holds no rows at all.
    pub fn is_empty(&self) -> bool {
        self.rows.is_empty()
    }

    /// Every row, in catalogue order.
    pub fn rows(&self) -> &[Row] {
        &self.rows
    }

    /// Iterate every row, in catalogue order.
    pub fn iter(&self) -> std::slice::Iter<'_, Row> {
        self.rows.iter()
    }

    /// The row for `slug`, or `None` when the slug is not in the catalogue.
    pub fn by_slug(&self, slug: &str) -> Option<&Row> {
        self.by_slug.get(slug).map(|index| &self.rows[*index])
    }

    /// Every row standing at this position, in catalogue order.
    ///
    /// The input is normalised with [`fen_key`] first, so a raw
    /// board-library FEN (en-passant square printed after every double
    /// push, arbitrary move counters) matches. Multiple rows are normal
    /// and not an error: co-canonical names and documented transpositions
    /// share positions by design.
    pub fn by_fen(&self, fen: &str) -> Result<Vec<&Row>, FenError> {
        Ok(self.by_fen_key(&fen_key(fen)?))
    }

    /// Every row at an already-normalised position key.
    ///
    /// The same lookup as [`Catalog::by_fen`] with the normalisation step
    /// skipped, for callers that hold a key rather than a FEN. A key that
    /// is not in `fen_key` form simply misses.
    pub fn by_fen_key(&self, key: &str) -> Vec<&Row> {
        self.resolve_all(self.by_fen_key.get(key))
    }

    /// Every row carrying this ECO code in `eco_legacy`, deepest first.
    pub fn by_eco(&self, code: &str) -> Vec<&Row> {
        self.resolve_all(self.by_eco.get(code.trim().to_uppercase().as_str()))
    }

    /// Rows whose canonical name or one alias equals `text`.
    ///
    /// Case- and diacritic-insensitive: `"grunfeld"` finds the Grünfeld
    /// rows, `"SICILIAN DEFENCE"` finds the Sicilian.
    pub fn by_name(&self, text: &str) -> Vec<&Row> {
        self.resolve_all(self.by_folded_name.get(&fold(text)))
    }

    /// Rows whose canonical name or an alias *contains* `text`.
    ///
    /// Same folding as [`Catalog::by_name`]. Results come back broadest
    /// first (shallowest depth), so a truncated list keeps the family
    /// heads rather than an arbitrary corner of one subtree.
    pub fn search(&self, text: &str, limit: usize) -> Vec<&Row> {
        let needle = fold(text);
        if needle.is_empty() {
            return Vec::new();
        }
        let mut hits: Vec<usize> = Vec::new();
        for (folded, bucket) in &self.by_folded_name {
            if folded.contains(&needle) {
                hits.extend(bucket);
            }
        }
        hits.sort_by(|a, b| {
            (self.rows[*a].depth, &self.rows[*a].ocn1)
                .cmp(&(self.rows[*b].depth, &self.rows[*b].ocn1))
        });
        hits.dedup();
        hits.truncate(limit);
        hits.into_iter().map(|index| &self.rows[index]).collect()
    }

    /// The breadcrumb for `slug`: root first, immediate parent last.
    ///
    /// `parents("B.Sic.Naj.Eng")` is `[B, B.Sic, B.Sic.Naj]`. The row
    /// itself is not included, and an unknown slug yields an empty path.
    pub fn parents(&self, slug: &str) -> Vec<&Row> {
        let mut chain: Vec<&Row> = Vec::new();
        let mut seen: BTreeSet<&str> = BTreeSet::new();
        seen.insert(slug);
        let mut current = self.by_slug(slug).and_then(|row| row.parent.as_deref());
        while let Some(next) = current {
            if !seen.insert(next) {
                break;
            }
            let Some(row) = self.by_slug(next) else { break };
            chain.push(row);
            current = row.parent.as_deref();
        }
        chain.reverse();
        chain
    }

    /// The direct children of `slug`, in catalogue order.
    pub fn children(&self, slug: &str) -> Vec<&Row> {
        self.resolve_all(self.children.get(slug))
    }

    /// `slug`'s own row, then its whole subtree in catalogue order.
    pub fn walk(&self, slug: &str) -> Vec<&Row> {
        let Some(row) = self.by_slug(slug) else {
            return Vec::new();
        };
        let prefix = format!("{slug}.");
        std::iter::once(row)
            .chain(self.rows.iter().filter(|r| r.ocn1.starts_with(&prefix)))
            .collect()
    }

    /// The FEN-canonical slug: follow `transposes_to` once.
    ///
    /// The catalogue contract guarantees the links never chain, so one hop
    /// is the whole rule. Canonical rows resolve to themselves; an unknown
    /// slug resolves to `None`.
    pub fn resolve<'a>(&'a self, slug: &'a str) -> Option<&'a str> {
        let row = self.by_slug(slug)?;
        Some(row.transposes_to.as_deref().unwrap_or(&row.ocn1))
    }

    /// The row's `same_as` partners as slugs.
    ///
    /// A `same_as` partner is *not* an alias to collapse: both slugs are
    /// canonical literary names for the same position.
    pub fn co_canonicals(&self, slug: &str) -> &[String] {
        self.by_slug(slug).map_or(&[], |row| row.same_as.as_slice())
    }

    fn resolve_all(&self, bucket: Option<&Vec<usize>>) -> Vec<&Row> {
        bucket.map_or_else(Vec::new, |indexes| {
            indexes.iter().map(|index| &self.rows[*index]).collect()
        })
    }
}

impl<'a> IntoIterator for &'a Catalog {
    type Item = &'a Row;
    type IntoIter = std::slice::Iter<'a, Row>;

    fn into_iter(self) -> Self::IntoIter {
        self.rows.iter()
    }
}

fn split_pipes(value: &str) -> Vec<String> {
    value
        .split('|')
        .map(str::trim)
        .filter(|part| !part.is_empty())
        .map(str::to_string)
        .collect()
}

fn optional(value: &str) -> Option<String> {
    let trimmed = value.trim();
    if trimmed.is_empty() {
        None
    } else {
        Some(trimmed.to_string())
    }
}

// ------------------------------------------------------------ delimited text

/// A header-keyed reader for the delimited text the catalogue ships as.
///
/// RFC 4180 quoting: a field may be wrapped in `"`, inside which the
/// delimiter, a doubled `"`, and line breaks are all literal. That is the
/// dialect Python's `csv` module writes by default, which is what produced
/// these files, and it is the whole reason a plain `split(',')` will not
/// do — 1,300 catalogue names carry a comma.
struct Table {
    header: Vec<String>,
    records: Vec<Vec<String>>,
}

impl Table {
    fn parse(text: &str, delimiter: char) -> Table {
        let mut rest = text;
        let header = read_record(&mut rest, delimiter).unwrap_or_default();
        let mut records = Vec::new();
        while let Some(fields) = read_record(&mut rest, delimiter) {
            // The trailing newline of the last line yields one empty
            // field, which is a file terminator and not a row.
            if fields.len() == 1 && fields[0].is_empty() {
                continue;
            }
            records.push(fields);
        }
        Table { header, records }
    }

    /// The named column of a record, or `""` when either is absent.
    fn field<'a>(&self, record: &'a [String], name: &str) -> &'a str {
        self.header
            .iter()
            .position(|column| column == name)
            .and_then(|index| record.get(index))
            .map_or("", String::as_str)
    }
}

/// Consume one record from `text`, leaving the remainder behind.
fn read_record(text: &mut &str, delimiter: char) -> Option<Vec<String>> {
    let source: &str = text;
    if source.is_empty() {
        return None;
    }
    let mut fields: Vec<String> = Vec::new();
    let mut field = String::new();
    let mut quoted = false;
    let mut chars = source.char_indices();

    while let Some((offset, ch)) = chars.next() {
        if quoted {
            if ch == '"' {
                // A doubled quote inside a quoted field is one literal `"`.
                if matches!(chars.clone().next(), Some((_, '"'))) {
                    field.push('"');
                    chars.next();
                } else {
                    quoted = false;
                }
            } else {
                field.push(ch);
            }
            continue;
        }
        match ch {
            '"' if field.is_empty() => quoted = true,
            c if c == delimiter => fields.push(std::mem::take(&mut field)),
            '\r' => {}
            '\n' => {
                fields.push(field);
                *text = &source[offset + 1..];
                return Some(fields);
            }
            other => field.push(other),
        }
    }

    fields.push(field);
    *text = "";
    Some(fields)
}

#[cfg(test)]
mod tests;
