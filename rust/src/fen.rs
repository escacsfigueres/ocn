//! Position identity for OCN-1 — spec Annex A, normative.
//!
//! A catalogue row's position is identified by its `fen_key`: the first
//! four FEN fields of the position reached by replaying `moves_uci` from
//! the standard initial position.
//!
//! 1. Board — standard FEN piece placement.
//! 2. Side to move — `w` or `b`.
//! 3. Castling rights — the FEN castling field, `-` when none remain.
//! 4. En passant — the target square **only if at least one enemy pawn
//!    can legally capture en passant** (a capture that would leave the
//!    capturer's own king in check does not count); otherwise `-`.
//!
//! Rule 4 is the trap. Many FEN emitters print the en-passant square
//! after every double pawn push whether or not the capture is legal, so
//! a string that looks right never matches the catalogue and the lookup
//! silently returns nothing instead of failing loudly. [`fen_key`]
//! normalises to the legal-capture form.
//!
//! No move generator is needed for any of this. Rule 4 asks one question
//! about a static position — can an enemy pawn take en passant without
//! exposing its own king — and answering it needs piece-attack detection
//! along rays (for the pin and discovered-check cases), nothing more.

use std::error::Error;
use std::fmt;

/// The FEN file letters, a-file first.
pub const FILES: &[u8; 8] = b"abcdefgh";

/// The castling rights in FEN field order.
pub const CASTLING_ORDER: [char; 4] = ['K', 'Q', 'k', 'q'];

const CASTLING_BITS: [u8; 4] = [1, 2, 4, 8];

/// Everything that can go wrong turning a FEN string into a position.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum FenError {
    /// A FEN must carry 4 fields (a position key) or 6 (with counters).
    FieldCount(usize),
    /// The halfmove clock or fullmove number is not a usable integer.
    Counters(String),
    /// The side-to-move field is neither `w` nor `b`.
    Turn(String),
    /// The piece-placement field is malformed.
    Board(String),
    /// The castling field is malformed.
    Castling(String),
    /// The en-passant field is neither `-` nor a rank-3/rank-6 square.
    EnPassant(String),
    /// The position parses but legality cannot be decided on it (no king
    /// for the side that would have to make the en-passant capture).
    IllegalPosition(String),
}

impl fmt::Display for FenError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            FenError::FieldCount(n) => write!(
                f,
                "expected a FEN with 4 or 6 fields: \
                 <board> <turn> <castling> <en-passant> [halfmove fullmove], got {n}"
            ),
            FenError::Counters(text) => {
                write!(f, "invalid FEN halfmove/fullmove counters: {text:?}")
            }
            FenError::Turn(text) => write!(f, "invalid FEN turn field: {text:?}"),
            FenError::Board(text) => write!(f, "invalid FEN board field: {text:?}"),
            FenError::Castling(text) => write!(f, "invalid FEN castling field: {text:?}"),
            FenError::EnPassant(text) => write!(f, "invalid FEN en-passant field: {text:?}"),
            FenError::IllegalPosition(text) => write!(f, "illegal FEN position: {text}"),
        }
    }
}

impl Error for FenError {}

/// Normalise a FEN string to the OCN-1 position key.
///
/// Accepts a 4-field or a 6-field FEN and returns
/// `"<board> <turn> <castling> <ep>"`: move counters are dropped (they
/// are not part of position identity) and the en-passant square is kept
/// only when an en-passant capture is actually legal.
///
/// ```
/// # use ocn::fen_key;
/// // 1.e4 c5 as most board libraries print it: the c6 square is there,
/// // but no white pawn can take on it.
/// let fen = "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2";
/// assert!(fen_key(fen).unwrap().ends_with(" w KQkq -"));
/// ```
pub fn fen_key(fen: &str) -> Result<String, FenError> {
    Position::parse(fen)?.fen_key()
}

/// A chess position: the four fields of a FEN that carry identity.
///
/// Squares are indexed a1 = 0 through h8 = 63, so `square % 8` is the
/// file and `square / 8` the rank — the same layout the Polyglot book
/// format indexes its piece-square keys by.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Position {
    squares: [u8; 64],
    white_to_move: bool,
    castling: u8,
    ep_square: Option<u8>,
}

impl Position {
    /// Parse a 4-field or 6-field FEN.
    ///
    /// The en-passant field is kept exactly as written; [`Position::fen_key`]
    /// and [`Position::legal_ep_square`] apply Annex A's rule 4 to it.
    pub fn parse(fen: &str) -> Result<Position, FenError> {
        let parts: Vec<&str> = fen.split_whitespace().collect();
        if parts.len() != 4 && parts.len() != 6 {
            return Err(FenError::FieldCount(parts.len()));
        }
        if parts.len() == 6 {
            let halfmove_ok = !parts[4].is_empty() && parts[4].bytes().all(|b| b.is_ascii_digit());
            let fullmove = parts[5].parse::<u64>().ok().filter(|n| *n >= 1);
            if !halfmove_ok || fullmove.is_none() {
                return Err(FenError::Counters(format!("{:?}", &parts[4..6])));
            }
        }

        let white_to_move = match parts[1] {
            "w" => true,
            "b" => false,
            other => return Err(FenError::Turn(other.to_string())),
        };

        Ok(Position {
            squares: parse_board(parts[0])?,
            white_to_move,
            castling: parse_castling(parts[2])?,
            ep_square: parse_ep_square(parts[3])?,
        })
    }

    /// The 64 squares, a1 first, `0` for empty and the FEN letter
    /// otherwise (upper case = White).
    pub fn squares(&self) -> &[u8; 64] {
        &self.squares
    }

    /// True when White is to move.
    pub fn white_to_move(&self) -> bool {
        self.white_to_move
    }

    /// Whether a castling right (`'K'`, `'Q'`, `'k'` or `'q'`) survives.
    pub fn has_castling_right(&self, right: char) -> bool {
        CASTLING_ORDER
            .iter()
            .position(|c| *c == right)
            .is_some_and(|index| self.castling & CASTLING_BITS[index] != 0)
    }

    /// The castling field as FEN writes it, `-` when no right survives.
    pub fn castling_field(&self) -> String {
        let text: String = CASTLING_ORDER
            .iter()
            .copied()
            .filter(|right| self.has_castling_right(*right))
            .collect();
        if text.is_empty() {
            "-".to_string()
        } else {
            text
        }
    }

    /// The en-passant square exactly as the FEN carried it, before rule 4.
    pub fn ep_square(&self) -> Option<u8> {
        self.ep_square
    }

    /// The en-passant square **after** Annex A rule 4: `Some` only when a
    /// pawn of the side to move can legally capture on it.
    ///
    /// The legality test is what makes this more than a lookup: the
    /// capturing pawn may be pinned (a diagonal ray through it to its own
    /// king), and the capture removes *two* pawns from a rank at once, so
    /// it can also open a rank onto its own king. Both cases are decided
    /// here by making the capture on a copy and asking whether the mover's
    /// king is attacked afterwards.
    pub fn legal_ep_square(&self) -> Result<Option<u8>, FenError> {
        let Some(ep) = self.ep_square else {
            return Ok(None);
        };
        let ep = ep as usize;
        let pawn = if self.white_to_move { b'P' } else { b'p' };
        let direction: isize = if self.white_to_move { 1 } else { -1 };
        let src_rank = (ep / 8) as isize - direction;
        if !(0..8).contains(&src_rank) {
            return Ok(None);
        }
        let dst_file = (ep % 8) as isize;

        for delta in [-1isize, 1] {
            let src_file = dst_file + delta;
            if !(0..8).contains(&src_file) {
                continue;
            }
            let src = (src_rank * 8 + src_file) as usize;
            if self.squares[src] != pawn {
                continue;
            }
            if self.capture_leaves_king_safe(src, ep)? {
                return Ok(Some(ep as u8));
            }
        }
        Ok(None)
    }

    /// The OCN-1 position key: board, turn, castling, normalised en passant.
    ///
    /// The placement field is re-serialised, so an unusual but parseable
    /// board field is canonicalised on the way through.
    pub fn fen_key(&self) -> Result<String, FenError> {
        let ep = match self.legal_ep_square()? {
            Some(square) => square_name(square as usize),
            None => "-".to_string(),
        };
        Ok(format!(
            "{} {} {} {}",
            self.placement_field(),
            if self.white_to_move { 'w' } else { 'b' },
            self.castling_field(),
            ep
        ))
    }

    /// The FEN piece-placement field for this position.
    pub fn placement_field(&self) -> String {
        let mut out = String::with_capacity(72);
        for rank in (0..8).rev() {
            if rank != 7 {
                out.push('/');
            }
            let mut empty = 0u8;
            for file in 0..8 {
                let piece = self.squares[rank * 8 + file];
                if piece == 0 {
                    empty += 1;
                    continue;
                }
                if empty > 0 {
                    out.push((b'0' + empty) as char);
                    empty = 0;
                }
                out.push(piece as char);
            }
            if empty > 0 {
                out.push((b'0' + empty) as char);
            }
        }
        out
    }

    /// Is `square` attacked by the given colour?
    ///
    /// Pawns, knights and the king by offset; rooks, bishops and queens by
    /// walking the rays until they hit a piece. This is the whole of the
    /// chess knowledge the crate needs.
    pub fn is_attacked(&self, square: usize, by_white: bool) -> bool {
        let file = (square % 8) as isize;
        let rank = (square / 8) as isize;

        let pawn_rank = if by_white { rank - 1 } else { rank + 1 };
        if (0..8).contains(&pawn_rank) {
            let pawn = if by_white { b'P' } else { b'p' };
            for pawn_file in [file - 1, file + 1] {
                if (0..8).contains(&pawn_file)
                    && self.squares[(pawn_rank * 8 + pawn_file) as usize] == pawn
                {
                    return true;
                }
            }
        }

        let knight = if by_white { b'N' } else { b'n' };
        const KNIGHT_STEPS: [(isize, isize); 8] = [
            (1, 2),
            (2, 1),
            (2, -1),
            (1, -2),
            (-1, -2),
            (-2, -1),
            (-2, 1),
            (-1, 2),
        ];
        for (df, dr) in KNIGHT_STEPS {
            let (nf, nr) = (file + df, rank + dr);
            if (0..8).contains(&nf)
                && (0..8).contains(&nr)
                && self.squares[(nr * 8 + nf) as usize] == knight
            {
                return true;
            }
        }

        let king = if by_white { b'K' } else { b'k' };
        for df in -1..=1isize {
            for dr in -1..=1isize {
                if df == 0 && dr == 0 {
                    continue;
                }
                let (nf, nr) = (file + df, rank + dr);
                if (0..8).contains(&nf)
                    && (0..8).contains(&nr)
                    && self.squares[(nr * 8 + nf) as usize] == king
                {
                    return true;
                }
            }
        }

        const ORTHOGONAL: [(isize, isize); 4] = [(1, 0), (-1, 0), (0, 1), (0, -1)];
        const DIAGONAL: [(isize, isize); 4] = [(1, 1), (1, -1), (-1, 1), (-1, -1)];
        self.ray_attacked(file, rank, by_white, &ORTHOGONAL, b"RQ")
            || self.ray_attacked(file, rank, by_white, &DIAGONAL, b"BQ")
    }

    fn ray_attacked(
        &self,
        file: isize,
        rank: isize,
        by_white: bool,
        directions: &[(isize, isize)],
        attackers: &[u8; 2],
    ) -> bool {
        for (df, dr) in directions {
            let (mut nf, mut nr) = (file + df, rank + dr);
            while (0..8).contains(&nf) && (0..8).contains(&nr) {
                let piece = self.squares[(nr * 8 + nf) as usize];
                if piece != 0 {
                    let matches = attackers.iter().any(|&kind| {
                        piece
                            == if by_white {
                                kind
                            } else {
                                kind.to_ascii_lowercase()
                            }
                    });
                    if matches {
                        return true;
                    }
                    break;
                }
                nf += df;
                nr += dr;
            }
        }
        false
    }

    /// Make the en-passant capture `src` -> `dst` on a copy and report
    /// whether the mover's own king survives it.
    fn capture_leaves_king_safe(&self, src: usize, dst: usize) -> Result<bool, FenError> {
        let mut next = self.clone();
        let piece = next.squares[src];
        // The captured pawn stands beside the capturer, not on the target
        // square: that is the whole point of en passant, and the reason a
        // single capture can clear two men off one rank.
        let captured = if piece.is_ascii_uppercase() {
            dst - 8
        } else {
            dst + 8
        };
        next.squares[captured] = 0;
        next.squares[src] = 0;
        next.squares[dst] = piece;

        let king = if self.white_to_move { b'K' } else { b'k' };
        let king_square = next
            .squares
            .iter()
            .position(|&p| p == king)
            .ok_or_else(|| {
                FenError::IllegalPosition(format!(
                    "no {} king, so en-passant legality is undecidable",
                    if self.white_to_move { "white" } else { "black" }
                ))
            })?;
        Ok(!next.is_attacked(king_square, !self.white_to_move))
    }
}

/// The algebraic name of a square index (`0` -> `"a1"`).
pub fn square_name(square: usize) -> String {
    let mut name = String::with_capacity(2);
    name.push(FILES[square % 8] as char);
    name.push((b'1' + (square / 8) as u8) as char);
    name
}

fn parse_board(field: &str) -> Result<[u8; 64], FenError> {
    let mut squares = [0u8; 64];
    let ranks: Vec<&str> = field.split('/').collect();
    if ranks.len() != 8 {
        return Err(FenError::Board(field.to_string()));
    }
    for (offset, rank_text) in ranks.iter().enumerate() {
        let board_rank = 7 - offset;
        let mut file = 0usize;
        for byte in rank_text.bytes() {
            if byte.is_ascii_digit() {
                if !(b'1'..=b'8').contains(&byte) {
                    return Err(FenError::Board(field.to_string()));
                }
                file += (byte - b'0') as usize;
                continue;
            }
            if !b"PNBRQKpnbrqk".contains(&byte) || file >= 8 {
                return Err(FenError::Board(field.to_string()));
            }
            squares[board_rank * 8 + file] = byte;
            file += 1;
        }
        if file != 8 {
            return Err(FenError::Board(field.to_string()));
        }
    }
    Ok(squares)
}

fn parse_castling(field: &str) -> Result<u8, FenError> {
    if field == "-" {
        return Ok(0);
    }
    let mut mask = 0u8;
    for right in field.chars() {
        let Some(index) = CASTLING_ORDER.iter().position(|c| *c == right) else {
            return Err(FenError::Castling(field.to_string()));
        };
        // A repeated right is a malformed field, not a harmless duplicate.
        if mask & CASTLING_BITS[index] != 0 {
            return Err(FenError::Castling(field.to_string()));
        }
        mask |= CASTLING_BITS[index];
    }
    Ok(mask)
}

fn parse_ep_square(field: &str) -> Result<Option<u8>, FenError> {
    if field == "-" {
        return Ok(None);
    }
    let bytes = field.as_bytes();
    if bytes.len() != 2 || !FILES.contains(&bytes[0]) || !matches!(bytes[1], b'3' | b'6') {
        return Err(FenError::EnPassant(field.to_string()));
    }
    let file = (bytes[0] - b'a') as usize;
    let rank = (bytes[1] - b'1') as usize;
    Ok(Some((rank * 8 + file) as u8))
}
