/*
 * OCN web explorer (roadmap H2.3).
 *
 * One ES module, no framework, no bundler, no network beyond the payload
 * this page ships with. It reads `data/ocn.json` once, builds four
 * in-memory indexes, and renders three views behind hash routes:
 *
 *   #/                  home: search + the A-E tree + the ECO converter
 *   #/B.Sic.Naj.Eng     one row: breadcrumb, board, moves, ECO, Lichess
 *   #/eco/B90           converter results for an ECO code
 *
 * Everything below builds DOM nodes rather than HTML strings: catalogue
 * names carry quotes, ampersands and commas, and string templating is
 * how those turn into a rendering bug.
 */

const DATA_URL = "data/ocn.json";
const LICHESS_ANALYSIS = "https://lichess.org/analysis/standard/";
const REPO_URL = "https://github.com/escacsfigueres/ocn";
const MAX_RESULTS = 60;

/* ------------------------------------------------------------------ */
/* DOM helpers                                                         */
/* ------------------------------------------------------------------ */

const HTML_NS = "http://www.w3.org/1999/xhtml";
const SVG_NS = "http://www.w3.org/2000/svg";

function make(ns, tag, props, children) {
  const node = document.createElementNS(ns, tag);
  for (const [key, value] of Object.entries(props || {})) {
    if (value === null || value === undefined || value === false) continue;
    if (key === "text") node.textContent = value;
    else if (key === "class") node.setAttribute("class", value);
    else if (key.startsWith("on")) node.addEventListener(key.slice(2), value);
    else node.setAttribute(key, value === true ? "" : String(value));
  }
  for (const child of children || []) {
    if (child === null || child === undefined || child === false) continue;
    node.appendChild(typeof child === "string" ? document.createTextNode(child) : child);
  }
  return node;
}

const h = (tag, props, children) => make(HTML_NS, tag, props, children);
const svg = (tag, props, children) => make(SVG_NS, tag, props, children);

/** Replace a container's contents, dropping the sections that rendered nothing. */
function mount(container, ...nodes) {
  container.replaceChildren(...nodes.filter(Boolean));
}

/* ------------------------------------------------------------------ */
/* Text folding                                                        */
/* ------------------------------------------------------------------ */

/*
 * The Python package's fold (`ocn.catalog._fold`: NFKD, casefold, drop
 * combining marks) plus the punctuation flattening a search box needs and
 * a lookup key must not have.
 *
 * A few letters carry their diacritic inside the code point and never
 * decompose, so they are mapped by hand. Apostrophes and commas are
 * dropped and dashes become spaces on both sides of the comparison, which
 * is what makes "kings indian", "king's indian" and the curly-quoted
 * "king’s indian" an iPhone produces all find the same rows -- and what
 * lets "najdorf english attack" find "Sicilian Najdorf, English Attack".
 * Dots survive: they carry the slug structure and the SAN move numbers.
 */
const FOLD_EXTRA = {
  "ø": "o", "đ": "d", "ð": "d", "ł": "l", "ß": "ss",
  "æ": "ae", "œ": "oe", "þ": "th", "ħ": "h", "ı": "i",
};
const FOLD_DROP = /['‘’´`,]/;
const FOLD_DASH = /[-‐‑‒–—]/;

function fold(text) {
  const lowered = String(text || "").normalize("NFKD").toLowerCase();
  let out = "";
  for (const char of lowered) {
    if (/\p{M}/u.test(char) || FOLD_DROP.test(char)) continue;
    out += FOLD_DASH.test(char) ? " " : (FOLD_EXTRA[char] || char);
  }
  return out.replace(/\s+/g, " ").trim();
}

/* ------------------------------------------------------------------ */
/* Data                                                                */
/* ------------------------------------------------------------------ */

const DB = {
  version: "",
  rows: [],
  bySlug: new Map(),
  children: new Map(),
  byEco: new Map(),
  descendants: new Map(),
};

async function loadData() {
  const response = await fetch(DATA_URL);
  if (!response.ok) throw new Error(`${response.status} ${response.statusText}`);
  const document_ = await response.json();
  DB.version = document_.catalog_version || "";
  DB.rows = document_.rows || [];

  for (const row of DB.rows) {
    DB.bySlug.set(row.slug, row);
    // Folded haystacks are computed once, here, and never recomputed:
    // this is what keeps a keystroke over 5,899 rows inside a frame.
    row._name = fold(row.name);
    row._slug = fold(row.slug);
    row._aliases = row.aliases ? fold(row.aliases.join(" | ")) : "";
    row._eco = new Set(row.eco || []);
    // `pop` is [masters_games, lichess_games] and is absent on every row
    // whose position no game in either pool has reached. Summing the two
    // pools is a ranking signal, never a displayed total: they count
    // different populations and are only ever shown separately.
    row._pop = row.pop ? (row.pop[0] || 0) + (row.pop[1] || 0) : 0;
    if (row.parent) {
      if (!DB.children.has(row.parent)) DB.children.set(row.parent, []);
      DB.children.get(row.parent).push(row);
    }
    for (const code of row.eco || []) {
      if (!DB.byEco.has(code)) DB.byEco.set(code, []);
      DB.byEco.get(code).push(row);
    }
  }

  // Most-played first, wherever the popularity sidecar has something to
  // say. `sort` is stable, so rows without game counts keep the
  // catalogue order they arrived in and a payload built without the
  // sidecar comes out exactly as before.
  if (DB.rows.some((row) => row._pop > 0)) {
    for (const kids of DB.children.values()) kids.sort((a, b) => b._pop - a._pop);
  }

  // Descendant counts, deepest rows first so every child is already
  // counted when its parent is reached.
  const byDepth = [...DB.rows].sort((a, b) => b.depth - a.depth);
  for (const row of byDepth) {
    const own = DB.descendants.get(row.slug) || 0;
    if (row.parent) {
      DB.descendants.set(row.parent, (DB.descendants.get(row.parent) || 0) + own + 1);
    }
  }
}

const childrenOf = (slug) => DB.children.get(slug) || [];
const descendantsOf = (slug) => DB.descendants.get(slug) || 0;

/* ------------------------------------------------------------------ */
/* Search                                                              */
/* ------------------------------------------------------------------ */

/*
 * Scored linear scan. 5,899 rows times a handful of `indexOf` calls on
 * pre-folded strings runs in single-digit milliseconds, so there is no
 * inverted index to keep in sync with the payload and no debounce to
 * make the box feel laggy.
 */
function search(query) {
  const rows = scan(fold(query), query);
  if (rows.length) return rows;
  // Second chance for the German transliteration. Canonical names spell
  // eponyms natively (`Grünfeld`, `Sämisch`) and the catalogue bans the
  // ASCII forms outright, so the NFKD fold answers "grunfeld" but not the
  // equally common "gruenfeld". Only tried when the plain fold found
  // nothing, so it can never reorder a normal result set.
  const transliterated = fold(query).replace(/([aou])e/g, "$1");
  if (transliterated === fold(query)) return rows;
  return scan(transliterated, query);
}

function scan(q, query) {
  if (!q) return [];
  const upper = query.trim().toUpperCase();
  const scored = [];

  for (const row of DB.rows) {
    let score = 0;
    if (row._slug === q) score = 1000;
    else if (row._eco.has(upper)) score = 900;
    else if (row._name === q) score = 800;
    // A word-start hit anywhere in the name ranks with a name-start hit,
    // so depth decides between them: typing "naj" should reach
    // `B.Sic.Naj` (Sicilian, Najdorf) before a depth-4 tabiya whose name
    // happens to begin with the word.
    else if (row._name.startsWith(q) || row._name.includes(` ${q}`)) score = 600;
    else if (row._name.includes(q)) score = 380;
    else if (row._aliases.includes(q)) score = 250;
    else if (row._slug.includes(q)) score = 150;
    if (score) scored.push([score, row]);
  }

  // Relevance first, then games played. Popularity ranks *within* a
  // score band rather than across all of them: an exact slug match must
  // outrank a wildly popular substring hit, but among rows that match
  // equally well, the one people actually play should come first.
  scored.sort((a, b) =>
    b[0] - a[0] ||
    b[1]._pop - a[1]._pop ||
    a[1].depth - b[1].depth ||
    a[1].name.length - b[1].name.length ||
    a[1].slug.localeCompare(b[1].slug));
  return scored.slice(0, MAX_RESULTS).map((entry) => entry[1]);
}

/* ------------------------------------------------------------------ */
/* Board                                                               */
/* ------------------------------------------------------------------ */

/*
 * The board is a printed plate.
 *
 * Squares are 64 rects; pieces are <use> references into a sprite of the
 * Cburnett diagram set, inlined once into the page at build time. That
 * set is what opening books and Wikipedia print, which is the point: the
 * board should look like a figure in a reference work, not like a game
 * client. Coordinates sit inside the border so the plate stays square.
 *
 * The position is held as an 8x8 array and stepped through the line's
 * UCI moves, so a reader can walk the opening rather than stare at its
 * final position.
 */
const PIECE_ID = {
  P: "wP", N: "wN", B: "wB", R: "wR", Q: "wQ", K: "wK",
  p: "bP", n: "bN", b: "bB", r: "bR", q: "bQ", k: "bK",
};
const FILES = "abcdefgh";
const UNIT = 40;
const START_PLACEMENT = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR";

function parsePlacement(fen) {
  const board = [];
  for (const rankText of String(fen).split(" ")[0].split("/")) {
    const rank = [];
    for (const char of rankText) {
      if (char >= "1" && char <= "8") {
        for (let i = 0; i < Number(char); i += 1) rank.push(null);
      } else {
        rank.push(char);
      }
    }
    board.push(rank);
  }
  return board;
}

//: rank index 0 is the eighth rank, so a1 is [7][0].
const squareIndex = (name) => [8 - Number(name[1]), FILES.indexOf(name[0])];

/*
 * Apply one UCI move to a board array. The moves come from the
 * catalogue and are known legal, so this only has to reproduce the three
 * cases where a move touches a square it does not name: castling moves a
 * rook, en passant clears the captured pawn, and promotion changes the
 * piece.
 */
function applyUci(board, uci) {
  const [fr, ff] = squareIndex(uci.slice(0, 2));
  const [tr, tf] = squareIndex(uci.slice(2, 4));
  const promotion = uci.slice(4, 5);
  const piece = board[fr][ff];
  if (!piece) return;
  const white = piece === piece.toUpperCase();
  const kind = piece.toLowerCase();

  board[fr][ff] = null;
  if (kind === "p" && ff !== tf && !board[tr][tf]) board[fr][tf] = null;
  if (kind === "k" && Math.abs(tf - ff) === 2) {
    const rookFrom = tf > ff ? 7 : 0;
    const rookTo = tf > ff ? tf - 1 : tf + 1;
    board[tr][rookTo] = board[tr][rookFrom];
    board[tr][rookFrom] = null;
  }
  board[tr][tf] = promotion
    ? (white ? promotion.toUpperCase() : promotion.toLowerCase())
    : piece;
}

function placementAfter(uciList, plies) {
  const board = parsePlacement(START_PLACEMENT);
  for (let i = 0; i < plies && i < uciList.length; i += 1) applyUci(board, uciList[i]);
  return board;
}

function boardSvg(board) {
  const size = 8 * UNIT;
  const squares = [];
  const pieces = [];
  const coords = [];

  for (let rank = 0; rank < 8; rank += 1) {
    for (let file = 0; file < 8; file += 1) {
      const x = file * UNIT;
      const y = rank * UNIT;
      const dark = (rank + file) % 2 === 1;
      squares.push(svg("rect", {
        class: `sq ${dark ? "dark" : "light"}`, x, y, width: UNIT, height: UNIT,
      }));
      if (file === 0) {
        coords.push(svg("text", {
          class: "coord", x: -6, y: y + UNIT / 2 + 3,
          "text-anchor": "end", text: String(8 - rank),
        }));
      }
      if (rank === 7) {
        coords.push(svg("text", {
          class: "coord", x: x + UNIT / 2, y: size + 12,
          "text-anchor": "middle", text: FILES[file],
        }));
      }
      const piece = (board[rank] || [])[file];
      if (!piece) continue;
      const id = PIECE_ID[piece];
      if (!id) continue;
      pieces.push(svg("use", {
        class: "board-piece", href: `#p-${id}`,
        x, y, width: UNIT, height: UNIT,
      }));
    }
  }

  return svg("svg", {
    class: "board", viewBox: `-18 -4 ${size + 22} ${size + 22}`, role: "img",
    "aria-label": "Board position",
  }, [
    svg("g", {}, squares),
    svg("rect", { class: "board-frame", x: 0, y: 0, width: size, height: size }),
    svg("g", {}, coords),
    svg("g", {}, pieces),
  ]);
}

/*
 * The move list and the board are one instrument: stepping the board
 * moves the highlight, clicking a move steps the board. Move numbers are
 * printed like a book (1. before White, no number before Black unless
 * the line starts there).
 */
function lineViewer(row) {
  const uciList = (row.uci || "").split(" ").filter(Boolean);
  const sanList = (row.san || "").replace(/\d+\./g, " ").trim().split(/\s+/).filter(Boolean);
  const total = uciList.length;
  let ply = total;

  const boardHost = h("div", {});
  const moveNodes = [];
  const plyLabel = h("span", { class: "ply" });
  const back = h("button", { type: "button", "aria-label": "Previous move", text: "\u2039" });
  const forward = h("button", { type: "button", "aria-label": "Next move", text: "\u203a" });
  const start = h("button", { type: "button", "aria-label": "Starting position", text: "\u00ab" });
  const end = h("button", { type: "button", "aria-label": "Final position", text: "\u00bb" });

  function draw() {
    boardHost.replaceChildren(boardSvg(placementAfter(uciList, ply)));
    moveNodes.forEach((node, index) => {
      node.classList.toggle("current", index === ply - 1);
    });
    plyLabel.textContent = total ? `${ply} / ${total}` : "";
    back.disabled = ply === 0;
    start.disabled = ply === 0;
    forward.disabled = ply === total;
    end.disabled = ply === total;
  }

  const goTo = (value) => { ply = Math.max(0, Math.min(total, value)); draw(); };
  back.addEventListener("click", () => goTo(ply - 1));
  forward.addEventListener("click", () => goTo(ply + 1));
  start.addEventListener("click", () => goTo(0));
  end.addEventListener("click", () => goTo(total));

  const moves = [];
  sanList.forEach((san, index) => {
    if (index % 2 === 0) {
      moves.push(h("span", { class: "move-no", text: `${index / 2 + 1}.` }));
    }
    const node = h("a", {
      class: "move", href: "#", role: "button", text: san,
      title: `Position after ${san}`,
    });
    node.addEventListener("click", (event) => { event.preventDefault(); goTo(index + 1); });
    moveNodes.push(node);
    moves.push(node);
  });

  draw();
  return {
    board: boardHost,
    moves: total ? h("div", { class: "moves" }, moves) : null,
    stepper: total
      ? h("div", { class: "stepper" }, [start, back, forward, end, plyLabel])
      : null,
  };
}

const lichessUrl = (fen) => LICHESS_ANALYSIS + String(fen).replace(/ /g, "_");
const sideToMove = (fen) => (String(fen).split(" ")[1] === "b" ? "Black to move" : "White to move");

/* ------------------------------------------------------------------ */
/* Shared fragments                                                    */
/* ------------------------------------------------------------------ */

const slugHref = (slug) => `#/${encodeURIComponent(slug)}`;
const ecoHref = (code) => `#/eco/${encodeURIComponent(code)}`;

const classOf = (slug) => `cls-${String(slug)[0]}`;

//: A result row shows at most this many ECO codes. `B.Sic` carries ten;
//  rendering all of them starves the name column on every list.
const ECO_CHIPS_IN_LIST = 2;

function rowLink(row) {
  const codes = row.eco || [];
  const shown = codes.slice(0, ECO_CHIPS_IN_LIST);
  const hidden = codes.length - shown.length;
  return h("a", { class: `row-link ${classOf(row.slug)}`, href: slugHref(row.slug) }, [
    h("span", { class: "row-name", text: row.name }),
    h("span", { class: "row-meta" }, [
      shown.length
        ? h("span", { class: "row-eco", text: shown.join(" ") + (hidden > 0 ? ` +${hidden}` : "") ,
                      title: codes.join(", ") })
        : null,
      h("span", { class: "row-slug", text: row.slug }),
    ]),
  ]);
}

function slugChip(slug) {
  const row = DB.bySlug.get(slug);
  return h("a", { class: "chip", href: slugHref(slug), title: row ? row.name : slug, text: slug });
}

function ecoChip(code) {
  return h("a", { class: "chip eco", href: ecoHref(code), text: code });
}

function field(label, ...content) {
  return [h("dt", { text: label }), h("dd", {}, content.filter(Boolean))];
}

function resultList(rows, emptyMessage) {
  if (!rows.length) return h("p", { class: "empty", text: emptyMessage });
  return h("ul", { class: "rows" }, rows.map((row) => h("li", {}, [rowLink(row)])));
}

/* ------------------------------------------------------------------ */
/* The ECO converter                                                   */
/* ------------------------------------------------------------------ */

const ECO_RE = /^[A-Ea-e][0-9]{2}$/;
const SLUG_RE = /^[A-Ea-e](\.[A-Za-z0-9_=+-]+)*$/;

function convert(query) {
  const text = String(query || "").trim();
  if (!text) return { kind: "empty" };
  if (ECO_RE.test(text)) {
    const code = text.toUpperCase();
    const rows = [...(DB.byEco.get(code) || [])].sort((a, b) =>
      b.depth - a.depth || a.slug.localeCompare(b.slug));
    return { kind: "eco", code, rows };
  }
  if (SLUG_RE.test(text)) {
    const slug = text.length === 1 ? text.toUpperCase() : text;
    const row = DB.bySlug.get(slug) || DB.rows.find((candidate) => candidate._slug === fold(slug));
    if (row) return { kind: "slug", row };
    return { kind: "unknown", text };
  }
  return { kind: "unknown", text };
}

function converterAnswer(result) {
  if (result.kind === "empty") {
    return h("p", { class: "hint", text: "An ECO code answers with its OCN rows, deepest first. A slug answers with its ECO codes." });
  }
  if (result.kind === "eco") {
    if (!result.rows.length) {
      return h("p", { class: "empty", text: `No catalogue row carries ECO ${result.code}.` });
    }
    return h("div", {}, [
      h("p", { class: "hint" }, [
        h("span", { class: "ident", text: result.code }),
        ` maps to ${result.rows.length} OCN ${result.rows.length === 1 ? "row" : "rows"}, deepest first.`,
      ]),
      resultList(result.rows, ""),
    ]);
  }
  if (result.kind === "slug") {
    const row = result.row;
    const codes = row.eco || [];
    return h("div", {}, [
      h("p", { class: "hint" }, [
        h("a", { class: "ident", href: slugHref(row.slug), text: row.slug }),
        h("span", { class: "name", text: ` \u2014 ${row.name}` }),
      ]),
      codes.length
        ? h("p", { class: "chip-row" }, codes.map(ecoChip))
        : h("p", { class: "empty", text: "No ECO code: this line sits beyond ECO's 500-code resolution, or it is a class root." }),
    ]);
  }
  return h("p", { class: "empty" }, [
    "Neither an ECO code nor a slug: ",
    h("span", { class: "ident", text: result.text }),
    ". Try B90, or B.Sic.Naj.Eng.",
  ]);
}

function converterBox(initial, withHeading = true) {
  const answer = h("div", { id: "converter-answer" });
  const input = h("input", {
    type: "search", id: "converter-input",
    placeholder: "B90, or B.Sic.Naj.Eng",
    autocomplete: "off", spellcheck: "false", value: initial || "",
    "aria-describedby": "converter-answer",
  });

  const run = (pushHash) => {
    const result = convert(input.value);
    answer.replaceChildren(converterAnswer(result));
    if (pushHash && result.kind === "eco") location.hash = ecoHref(result.code).slice(1);
    if (pushHash && result.kind === "slug") location.hash = slugHref(result.row.slug).slice(1);
  };

  input.addEventListener("input", () => run(false));
  input.addEventListener("keydown", (event) => {
    if (event.key === "Enter") { event.preventDefault(); run(true); }
  });
  run(false);

  return h("section", {}, [
    withHeading
      ? h("div", { class: "section-head" }, [
          h("h2", { class: "label", text: "ECO converter" }),
          h("span", { class: "count", text: "both directions" }),
        ])
      : null,
    h("label", { class: "skip", for: "converter-input", text: "ECO code or OCN slug" }),
    h("div", { class: "seek" }, [input]),
    answer,
  ]);
}

/*
 * Children are built on first expand. The A class alone has 1,367
 * descendants; rendering the whole forest up front is roughly 5,899
 * list items nobody asked for.
 */
function treeNode(row) {
  const kids = childrenOf(row.slug);
  const total = descendantsOf(row.slug);
  //: The children live inside a collapsible wrapper rather than being
  //  display:none, so the branch can open rather than appear. `inert`
  //  keeps a closed branch out of the tab order and out of a screen
  //  reader's way, which `hidden` used to do for free.
  const list = h("ul", {});
  const drawer = h("div", { class: "drawer", hidden: true }, [list]);
  let built = false;

  //: The disclosure arrow is drawn, not typed. A glyph carries its own
  //  font metrics -- ascent, baseline, side bearings -- none of which
  //  line up with the text beside it, which is why a character triangle
  //  never sits straight. An SVG path has the geometry we give it.
  const arrow = svg("svg", { viewBox: "0 0 12 12", "aria-hidden": "true" }, [
    svg("path", { d: "M4.2 1.7 L9.6 6 L4.2 10.3 Z" }),
  ]);
  const toggle = h("button", {
    class: "node-toggle", type: "button", "aria-expanded": "false",
    "aria-label": `Expand ${row.name}`,
    disabled: kids.length === 0,
  }, kids.length ? [arrow] : []);

  /*
   * Build on approach, not on click. Pointing at a row is the earliest
   * honest signal that it is about to be opened, and building then puts
   * the layout cost in a frame nobody is watching. By the time the
   * click lands the rows exist and the drawer has nothing to do but
   * move. Keyboard users get the same through focus.
   */
  const prepare = () => {
    if (built || !kids.length) return;
    const rows = kids.map(treeNode);
    //: Each row carries its position so the entrance can stagger. The
    //  stagger is capped: past ten rows it stops reading as a cascade
    //  and starts reading as a wait.
    rows.forEach((node, index) => node.style.setProperty("--i", String(Math.min(index, 10))));
    list.replaceChildren(...rows);
    built = true;
  };
  toggle.addEventListener("pointerenter", prepare);
  toggle.addEventListener("focus", prepare);

  const item = h("li", { class: classOf(row.slug) }, [
    h("div", { class: "node" }, [
      toggle,
      h("a", { class: `node-slug${row.depth === 0 ? " is-root" : ""}`, href: slugHref(row.slug),
               text: row.slug.split(".").pop() }),
      h("a", { class: "node-name", href: slugHref(row.slug), text: row.name }),
      total ? h("span", { class: "node-count", text: String(total), title: `${total} lines below` }) : null,
    ]),
    drawer,
  ]);

  toggle.addEventListener("click", () => {
    const show = toggle.getAttribute("aria-expanded") !== "true";
    if (show) prepare();
    toggle.setAttribute("aria-expanded", String(show));
    toggle.setAttribute("aria-label", `${show ? "Collapse" : "Expand"} ${row.name}`);

    /*
     * The layout change happens once, in a single frame; only the rows
     * animate, and only through opacity and transform, which the
     * compositor handles without touching layout.
     *
     * The previous version animated the drawer's height, which asks the
     * browser to re-lay-out the whole branch on every frame -- twenty
     * rows, each with its own nested grid. It measured clean on an idle
     * machine and stuttered on a real one, which is the signature of
     * animating the wrong property rather than of the wrong curve.
     */
    drawer.hidden = !show;
    if (show) {
      drawer.classList.remove("is-entering");
      void drawer.offsetWidth;
      drawer.classList.add("is-entering");
    }
  });

  return item;
}

function treePanel() {
  const roots = DB.rows.filter((row) => row.depth === 0);
  return h("section", {}, [
    h("div", { class: "section-head" }, [
      h("h2", { class: "label", text: "The tree" }),
      h("span", { class: "count", text: "5 classes" }),
    ]),
    h("ul", { class: "tree" }, roots.map(treeNode)),
  ]);
}

/* ------------------------------------------------------------------ */
/* Views                                                               */
/* ------------------------------------------------------------------ */

function searchPanel() {
  const results = h("div", { id: "search-results", "aria-live": "polite" });
  const meta = h("p", { class: "hint" });
  const input = h("input", {
    type: "search", id: "search-input",
    placeholder: "Najdorf, Berlin Wall, B.Sic, B90",
    autocomplete: "off", spellcheck: "false",
    "aria-describedby": "search-results",
  });

  input.addEventListener("input", () => {
    const query = input.value.trim();
    if (!query) {
      results.replaceChildren();
      meta.textContent = "";
      return;
    }
    const started = performance.now();
    const rows = search(query);
    const elapsed = performance.now() - started;
    results.replaceChildren(resultList(rows, "Nothing matches that name, alias, slug or code."));
    meta.textContent = rows.length
      ? `${rows.length === MAX_RESULTS ? "top " : ""}${rows.length} of 5,899 rows, ${elapsed.toFixed(1)} ms`
      : `no matches, ${elapsed.toFixed(1)} ms`;
  });

  return h("section", {}, [
    h("div", { class: "section-head" }, [
      h("h2", { class: "label", text: "Search" }),
      h("span", { class: "count", text: "names, aliases, slugs, ECO" }),
    ]),
    h("label", { class: "skip", for: "search-input", text: "Search the catalogue" }),
    h("div", { class: "seek" }, [input]),
    meta,
    results,
  ]);
}

function renderHome() {
  const view = document.getElementById("view");
  mount(view,
    h("p", { class: "home-lead" }, [
      "ECO gives you ", h("span", { class: "ident", text: "B90" }),
      ". Lichess gives you a sixty-character string. Neither gives you the tree. ",
      h("strong", { text: "OCN is " }), h("span", { class: "ident", text: "B.Sic.Naj.Eng" }),
      h("strong", { text: "" }),
      " — machine-readable parents, transposition canonicalisation, keyed to both.",
    ]),
    h("div", { class: "panels" }, [searchPanel(), converterBox("")]),
    treePanel(),
  );
  const input = document.getElementById("search-input");
  if (input && window.matchMedia("(min-width: 700px)").matches) input.focus();
}

/*
 * The path is the slug.
 *
 * A breadcrumb of names cannot be laid out: the names are one to five
 * words long, they wrap to different heights, and seven of them will not
 * sit on a line. The identifier will -- it is at most 29 characters, it
 * is monospaced, and every segment of it is already a real row. So the
 * navigation is the slug itself, dot separators and all, with the class
 * letter in its volume colour. The name of whichever segment you point
 * at appears in a fixed slot underneath, so nothing moves.
 */
function slugPath(slug) {
  const parts = slug.split(".");
  const nameSlot = h("div", { class: "path-name" });
  const line = [];
  let prefix = "";

  const currentName = (DB.bySlug.get(slug) || {}).name || "";
  const showName = (text) => { nameSlot.textContent = text || currentName; };

  parts.forEach((token, index) => {
    prefix = index === 0 ? token : `${prefix}.${token}`;
    const row = DB.bySlug.get(prefix);
    const last = index === parts.length - 1;
    if (index > 0) line.push(h("span", { class: "path-dot", "aria-hidden": "true", text: "." }));
    const seg = h("a", {
      class: `path-seg${last ? " here" : ""}${index === 0 ? " root" : ""}`,
      href: slugHref(prefix),
      title: row ? row.name : prefix,
      "aria-current": last ? "page" : null,
      text: token,
    });
    const name = row ? row.name : "";
    seg.addEventListener("mouseenter", () => showName(name));
    seg.addEventListener("focus", () => showName(name));
    seg.addEventListener("mouseleave", () => showName(""));
    seg.addEventListener("blur", () => showName(""));
    line.push(seg);
  });

  showName("");
  return h("nav", { class: `path cls-${parts[0]}`, "aria-label": "Slug hierarchy" }, [
    h("div", { class: "path-line" }, line),
    nameSlot,
  ]);
}

function lichessBlock(lichess) {
  const kind = lichess.kind === "exact"
    ? "exact match"
    : lichess.kind === "prefix"
      ? "prefix match, the nearest named Lichess line"
      : lichess.kind;
  return h("div", {}, [
    h("span", { class: "name", text: lichess.name }),
    h("span", { class: "sub" }, [kind, lichess.eco ? ` (${lichess.eco})` : ""]),
  ]);
}

/*
 * The popularity line (roadmap H2.7).
 *
 * Every figure is scoped to the database it came from, because that is
 * the only honest thing either number can claim: the masters count is
 * games in the Lichess masters database (~3M OTB master games), not
 * games ever played, and the Lichess count is games in the rated
 * blitz/rapid/classical pool from 1800 up, not "games on Lichess". The
 * two are never added together in front of a reader -- they count
 * different populations, and a sum would be a number with no referent.
 */
const NUM = (value) => Number(value).toLocaleString("en");

function popularityLine(row) {
  const [masters, lichess] = row.pop || [0, 0];
  if (!masters && !lichess) return null;
  const parts = [];
  if (masters) parts.push(`${NUM(masters)} games in the Lichess masters database`);
  if (lichess) parts.push(`${masters ? NUM(lichess) : NUM(lichess) + " games"} on Lichess`);
  return h("div", {}, [
    h("span", { text: parts.join(", ") }),
    h("span", { class: "sub", text: "Lichess pool: rated blitz, rapid and classical from 1800 up" }),
  ]);
}

function relationFields(row) {
  const items = [];
  if (row.transposes_to) {
    items.push(...field("Transposes to", slugChip(row.transposes_to),
      h("span", { class: "sub", text: "the same position, canonicalised there" })));
  }
  if (row.same_as && row.same_as.length) {
    items.push(...field("Same position", h("span", { class: "chip-row" }, row.same_as.map(slugChip)),
      h("span", { class: "sub", text: "co-canonical: both names are real" })));
  }
  return items;
}

function attributionSection(row) {
  return h("section", {}, [
    h("div", { class: "section-head" }, [h("h2", { class: "label", text: "Attribution" })]),
    h("dl", { class: "facts" }, [
      ...field("Named after", h("span", { class: "name", text: row.attributed_to })),
      ...(row.attribution_source ? field("Source", h("span", { text: row.attribution_source })) : []),
      ...(row.historical_notes ? field("History", h("span", { text: row.historical_notes })) : []),
    ]),
  ]);
}

function childrenSection(row) {
  const kids = childrenOf(row.slug);
  if (!kids.length) return null;
  return h("section", {}, [
    h("div", { class: "section-head" }, [
      h("h2", { class: "label", text: "Sub-lines" }),
      h("span", { class: "count", text: String(kids.length) }),
    ]),
    resultList(kids, ""),
  ]);
}

function renderRow(slug) {
  const view = document.getElementById("view");
  const row = DB.bySlug.get(slug);
  if (!row) {
    mount(view, h("section", { class: "notice" }, [
      h("h1", { class: "display", text: "No such slug" }),
      h("p", {}, [h("span", { class: "ident", text: slug }), " is not in the catalogue."]),
      h("p", {}, [h("a", { href: "#/", text: "Back to search" })]),
    ]));
    return;
  }

  const line = lineViewer(row);
  const played = popularityLine(row);
  const facts = [
    ...(row.eco ? field("ECO", h("span", { class: "chip-row" }, row.eco.map(ecoChip))) : []),
    ...(row.lichess ? field("Lichess", lichessBlock(row.lichess)) : []),
    ...(played ? field("Played", played) : []),
    ...(row.aliases ? field("Also known as", h("span", { class: "name", text: row.aliases.join(", ") })) : []),
    ...(row.flags ? field("Flags", h("span", { class: "chip-row" },
      row.flags.map((flag) => h("span", { class: "chip flag", text: flag })))) : []),
    ...relationFields(row),
    ...field("Parent", row.parent
      ? slugChip(row.parent)
      : h("span", { class: "sub", text: "class root, the top of its family" })),
  ];

  mount(view,
    h("header", { class: `entry-head ${classOf(row.slug)}` }, [
      slugPath(row.slug),
      h("h1", { class: "display", text: row.name }),
    ]),
    h("div", { class: "entry-body" }, [
      h("div", { class: "plate-col" }, [
        line.board,
        h("div", { class: "plate-caption" }, [
          h("span", { text: sideToMove(row.fen) }),
          h("a", { href: lichessUrl(row.fen), rel: "noopener", target: "_blank",
                   text: "Analyse on Lichess \u2197" }),
        ]),
        line.stepper,
        h("p", { class: "fen", text: row.fen }),
      ]),
      h("div", {}, [
        line.moves,
        h("dl", { class: "facts" }, facts),
        row.attributed_to ? attributionSection(row) : null,
        childrenSection(row),
      ].filter(Boolean)),
    ]),
  );
}

function renderEco(query) {
  const view = document.getElementById("view");
  mount(view,
    h("header", { class: "entry-head" }, [
      h("h1", { class: "display", text: "ECO converter" }),
    ]),
    h("div", { style: "margin-top:1.75rem" }, [converterBox(query, false)]),
  );
}

/* ------------------------------------------------------------------ */
/* Router                                                              */
/* ------------------------------------------------------------------ */

function route() {
  const raw = location.hash.replace(/^#\/?/, "");
  const path = decodeURIComponent(raw);
  if (!path) renderHome();
  else if (path.startsWith("eco/")) renderEco(path.slice(4));
  else renderRow(path);
  window.scrollTo(0, 0);
}

async function boot() {
  const view = document.getElementById("view");
  try {
    await loadData();
  } catch (error) {
    mount(view, h("section", { class: "panel" }, [
      h("h1", { text: "The catalogue did not load" }),
      h("p", { text: String(error && error.message ? error.message : error) }),
      h("p", {}, [
        "Build it with ", h("code", { text: "python3 web/build.py" }),
        " and serve the result, or read the catalogue at ",
        h("a", { href: REPO_URL, text: "the repository" }), ".",
      ]),
    ]));
    return;
  }
  const badge = document.getElementById("catalog-version");
  if (badge) badge.textContent = `${DB.rows.length.toLocaleString("en")} rows, ${DB.version}`;
  window.addEventListener("hashchange", route);
  route();
}

boot();
