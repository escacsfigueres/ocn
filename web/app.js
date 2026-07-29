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
 * A chessboard as 64 rects plus hand-drawn piece shapes.
 *
 * The pieces are our own SVG paths, drawn in the spirit of the figurines
 * printed in opening books: solid silhouettes, flat fills, no gradients,
 * legible at 40px. They replace the Unicode glyphs (U+265A..), which
 * render at a different weight and baseline in every system font and
 * cannot be aligned reliably. Each piece is drawn in a 45x45 box that is
 * scaled onto the square.
 *
 * Shapes are MIT like the rest of the code: no third-party piece set, no
 * licence patchwork inside a CC-BY catalogue.
 */
const BASE = "M11.6,39.6c0-4.1,3.3-6,6.4-6.6h9c3.1,0.6,6.4,2.5,6.4,6.6z";

const PIECES = {
  p: {
    body: [
      "M22.5,7.2a5.4,5.4 0 1 1 0,10.8a5.4,5.4 0 1 1 0,-10.8z",
      "M17.3,17.8c3.4,1.8,7,1.8,10.4,0c0.5,6.5,2.7,10.7,4.6,13.4h-19.6c1.9,-2.7,4.1,-6.9,4.6,-13.4z",
      "M15.8,31.2h13.4v2.2h-13.4z",
      BASE,
    ],
  },
  r: {
    body: [
      "M11.6,9.4h4.6v3.6h4.2v-3.6h4.2v3.6h4.2v-3.6h4.6v9.4h-22z",
      "M14.6,18.8h15.8l-1.4,12.4h-13z",
      "M13,31.2h19v2.2h-19z",
      BASE,
    ],
    detail: ["M16.2,13h12.6"],
  },
  b: {
    body: [
      "M22.5,6a2.4,2.4 0 1 1 0,4.8a2.4,2.4 0 1 1 0,-4.8z",
      "M22.5,10.4c5.4,2.4,8.8,7.6,8.8,12.8c0,3.2,-1.2,5.6,-2.4,7.2h-12.8c-1.2,-1.6,-2.4,-4,-2.4,-7.2c0,-5.2,3.4,-10.4,8.8,-12.8z",
      "M13.6,30.4h17.8v2.8h-17.8z",
      BASE,
    ],
    detail: ["M19.6,15.4l5.6,6.4"],
  },
  n: {
    body: [
      "M13.5,33.4C13.7,27.5,15.2,23.6,18.2,21.2C16,21.6,13.6,22.6,11.8,24.2C10.2,22.4,10.4,19.6,12.2,17.2C14.6,14,17.8,11.6,20.6,9.8C20.2,7.6,20.6,5.6,22,4.6C23.4,5.8,24,7.8,24.2,9.6C25,8.4,26.2,7.2,27.6,7C28.4,8.4,28.4,10.4,27.8,12.2C30.6,15,32,19.4,32,25C32,28.4,31.8,31,31.6,33.4Z",
      BASE,
    ],
    detail: ["M12.9,20.2a0.95,0.95 0 1 1 0,1.9a0.95,0.95 0 1 1 0,-1.9z", "M19.6,13.2a1.25,1.25 0 1 1 0,2.5a1.25,1.25 0 1 1 0,-2.5z", "M26.4,13.6c2.2,2.6,3.2,6.2,3.2,10.8"],
  },
  q: {
    body: [
      "M10.6,9.2a2.3,2.3 0 1 1 0,4.6a2.3,2.3 0 1 1 0,-4.6z",
      "M16.4,5.6a2.3,2.3 0 1 1 0,4.6a2.3,2.3 0 1 1 0,-4.6z",
      "M22.5,4.4a2.4,2.4 0 1 1 0,4.8a2.4,2.4 0 1 1 0,-4.8z",
      "M28.6,5.6a2.3,2.3 0 1 1 0,4.6a2.3,2.3 0 1 1 0,-4.6z",
      "M34.4,9.2a2.3,2.3 0 1 1 0,4.6a2.3,2.3 0 1 1 0,-4.6z",
      "M11.6,13.4l3.2,16.8h15.4l3.2,-16.8l-5.2,4.6l-3.1,-8.4l-3.1,8.8l-3.1,-8.8l-3.1,8.4z",
      "M13.4,30.2h18.2v3h-18.2z",
      BASE,
    ],
  },
  k: {
    body: [
      "M21.4,4.4h2.2v3.2h3.2v2.2h-3.2v3.6h-2.2v-3.6h-3.2v-2.2h3.2z",
      "M22.5,13.4c-5.8,0,-9.9,3.8,-9.9,8.4c0,2.2,1,4.1,2.2,5.6h15.4c1.2,-1.5,2.2,-3.4,2.2,-5.6c0,-4.6,-4.1,-8.4,-9.9,-8.4z",
      "M14,26.6h17v3.6h-17z",
      "M13.4,30.2h18.2v3h-18.2z",
      BASE,
    ],
    detail: ["M22.5,17.4v6"],
  },
};
const FILES = "abcdefgh";
const UNIT = 40;
const MARGIN = 15;

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

function boardSvg(fen) {
  const board = parsePlacement(fen);
  const width = MARGIN + 8 * UNIT;
  const height = 8 * UNIT + MARGIN;
  const squares = [];
  const pieces = [];

  for (let rank = 0; rank < 8; rank += 1) {
    for (let file = 0; file < 8; file += 1) {
      const x = MARGIN + file * UNIT;
      const y = rank * UNIT;
      squares.push(svg("rect", {
        class: `sq ${(rank + file) % 2 === 0 ? "light" : "dark"}`,
        x, y, width: UNIT, height: UNIT,
      }));
      const piece = (board[rank] || [])[file];
      if (!piece) continue;
      const shape = PIECES[piece.toLowerCase()];
      if (!shape) continue;
      const white = piece === piece.toUpperCase();
      const scale = (UNIT / 45) * 1.08;
      const parts = shape.body.map((d) => svg("path", { class: "piece-body", d }));
      for (const d of shape.detail || []) {
        parts.push(svg("path", { class: "piece-detail", d }));
      }
      pieces.push(svg("g", {
        class: `piece ${white ? "white" : "black"}`,
        transform: `translate(${x + UNIT / 2} ${y + UNIT / 2}) scale(${scale}) translate(-22.5 -22.5)`,
      }, parts));
    }
  }

  const coords = [];
  for (let i = 0; i < 8; i += 1) {
    coords.push(svg("text", {
      class: "coord", x: MARGIN - 5, y: i * UNIT + UNIT / 2,
      "text-anchor": "end", "dominant-baseline": "central", text: String(8 - i),
    }));
    coords.push(svg("text", {
      class: "coord", x: MARGIN + i * UNIT + UNIT / 2, y: 8 * UNIT + MARGIN - 4,
      "text-anchor": "middle", text: FILES[i],
    }));
  }

  return svg("svg", {
    class: "board",
    viewBox: `0 0 ${width} ${height}`,
    role: "img",
    "aria-label": `Board position, FEN ${fen}`,
  }, [
    svg("g", {}, squares),
    svg("g", {}, coords),
    svg("g", {}, pieces),
  ]);
}

const lichessUrl = (fen) => LICHESS_ANALYSIS + String(fen).replace(/ /g, "_");
const sideToMove = (fen) => (String(fen).split(" ")[1] === "b" ? "Black to move" : "White to move");

/* ------------------------------------------------------------------ */
/* Shared fragments                                                    */
/* ------------------------------------------------------------------ */

const slugHref = (slug) => `#/${encodeURIComponent(slug)}`;
const ecoHref = (code) => `#/eco/${encodeURIComponent(code)}`;

function rowLink(row, extraClass) {
  return h("a", {
    class: `row-link${extraClass ? " " + extraClass : ""}`,
    href: slugHref(row.slug),
  }, [
    h("span", { class: "row-link-name", text: row.name }),
    h("code", { class: "row-link-slug", text: row.slug }),
  ]);
}

function slugChip(slug) {
  const row = DB.bySlug.get(slug);
  return h("a", { class: "chip chip-slug", href: slugHref(slug), title: row ? row.name : slug },
    [h("code", { text: slug })]);
}

function ecoChip(code) {
  return h("a", { class: "chip chip-eco", href: ecoHref(code), text: code });
}

function field(label, ...content) {
  return [
    h("dt", { text: label }),
    h("dd", {}, content.filter(Boolean)),
  ];
}

//: A result row shows at most this many ECO codes. `B.Sic` carries ten;
//  rendering all of them starves the name column on every list. The full
//  set is one click away on the row page.
const ECO_CHIPS_IN_LIST = 3;

function resultList(rows, emptyMessage) {
  if (!rows.length) return h("p", { class: "muted", text: emptyMessage });
  return h("ul", { class: "results" }, rows.map((row) => {
    const codes = row.eco || [];
    const shown = codes.slice(0, ECO_CHIPS_IN_LIST);
    const hidden = codes.length - shown.length;
    return h("li", {}, [
      rowLink(row),
      h("span", { class: "result-meta" }, [
        h("span", { class: "depth", text: `depth ${row.depth}` }),
        ...shown.map((code) => h("span", { class: "chip chip-eco flat", text: code })),
        hidden > 0
          ? h("span", { class: "depth", text: `+${hidden}`, title: codes.join(", ") })
          : null,
      ]),
    ]);
  }));
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
    return h("p", { class: "muted", text: "An ECO code answers with its OCN rows, deepest first. A slug answers with its ECO codes." });
  }
  if (result.kind === "eco") {
    if (!result.rows.length) {
      return h("p", { class: "muted", text: `No catalogue row carries ECO ${result.code}.` });
    }
    return h("div", {}, [
      h("p", { class: "answer-head" }, [
        h("strong", { text: result.code }),
        ` maps to ${result.rows.length} OCN ${result.rows.length === 1 ? "row" : "rows"}, deepest first.`,
      ]),
      resultList(result.rows, ""),
    ]);
  }
  if (result.kind === "slug") {
    const row = result.row;
    const codes = row.eco || [];
    return h("div", {}, [
      h("p", { class: "answer-head" }, [
        h("code", { text: row.slug }),
        ` — ${row.name}`,
      ]),
      codes.length
        ? h("p", { class: "chips" }, [
            h("span", { class: "chips-label", text: codes.length === 1 ? "ECO code:" : "ECO codes:" }),
            ...codes.map(ecoChip),
          ])
        : h("p", { class: "muted", text: "No ECO code: this line sits beyond ECO's 500-code resolution, or it is a class root." }),
      h("p", {}, [h("a", { class: "more", href: slugHref(row.slug), text: "Open the row page" })]),
    ]);
  }
  return h("p", { class: "muted" }, [
    `Neither an ECO code nor a slug: `,
    h("code", { text: result.text }),
    ". Try B90, or B.Sic.Naj.Eng.",
  ]);
}

function converterBox(initial) {
  const answer = h("div", { class: "answer", id: "converter-answer" });
  const input = h("input", {
    type: "search",
    id: "converter-input",
    class: "box",
    placeholder: "B90, or B.Sic.Naj.Eng",
    autocomplete: "off",
    spellcheck: "false",
    value: initial || "",
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

  return h("section", { class: "panel converter" }, [
    h("h2", { text: "ECO converter" }),
    h("label", { class: "sr-only", for: "converter-input", text: "ECO code or OCN slug" }),
    input,
    answer,
  ]);
}

/* ------------------------------------------------------------------ */
/* The tree                                                            */
/* ------------------------------------------------------------------ */

/*
 * Children are built on first expand. The A class alone has 1,367
 * descendants; rendering the whole forest up front is roughly 5,899
 * list items nobody asked for.
 */
function treeNode(row) {
  const kids = childrenOf(row.slug);
  const total = descendantsOf(row.slug);
  const list = h("ul", { class: "tree-children", hidden: true });
  let built = false;

  const twisty = h("button", {
    class: "twisty",
    type: "button",
    "aria-expanded": "false",
    "aria-label": `Expand ${row.name}`,
    text: kids.length ? "+" : "",
    disabled: kids.length === 0,
  });

  twisty.addEventListener("click", () => {
    const open = twisty.getAttribute("aria-expanded") === "true";
    if (!open && !built) {
      list.replaceChildren(...kids.map(treeNode));
      built = true;
    }
    twisty.setAttribute("aria-expanded", String(!open));
    twisty.setAttribute("aria-label", `${open ? "Expand" : "Collapse"} ${row.name}`);
    twisty.textContent = open ? "+" : "−";
    list.hidden = open;
  });

  return h("li", { class: "tree-node" }, [
    h("div", { class: "tree-row" }, [
      twisty,
      h("a", { class: "tree-link", href: slugHref(row.slug) }, [
        h("code", { class: "tree-token", text: row.slug.split(".").pop() }),
        h("span", { class: "tree-name", text: row.name }),
      ]),
      total ? h("span", { class: "tree-count", text: String(total), title: `${total} lines below` }) : null,
    ]),
    list,
  ]);
}

function treePanel() {
  const roots = DB.rows.filter((row) => row.depth === 0);
  return h("section", { class: "panel tree-panel" }, [
    h("h2", { text: "The tree" }),
    h("p", { class: "muted", text: "Five structural classes, expanded on demand. The number is how many lines sit below a node." }),
    h("ul", { class: "tree tree-root" }, roots.map(treeNode)),
  ]);
}

/* ------------------------------------------------------------------ */
/* Views                                                               */
/* ------------------------------------------------------------------ */

function searchPanel() {
  const results = h("div", { class: "search-results", id: "search-results", "aria-live": "polite" });
  const meta = h("p", { class: "search-meta" });
  const input = h("input", {
    type: "search",
    id: "search-input",
    class: "box",
    placeholder: "Najdorf, Berlin Wall, B.Sic, B90, Lasker-Pelikán",
    autocomplete: "off",
    spellcheck: "false",
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
      ? `${rows.length === MAX_RESULTS ? "top " : ""}${rows.length} of 5,899 rows in ${elapsed.toFixed(1)} ms`
      : `0 matches in ${elapsed.toFixed(1)} ms`;
  });

  return h("section", { class: "panel search-panel" }, [
    h("h2", { text: "Search" }),
    h("label", { class: "sr-only", for: "search-input", text: "Search names, aliases, slugs and ECO codes" }),
    input,
    meta,
    results,
  ]);
}

function renderHome() {
  const view = document.getElementById("view");
  mount(view, 
    h("section", { class: "hero" }, [
      h("h1", { text: "The hierarchy layer over ECO and the Lichess names" }),
      h("p", { class: "lede" }, [
        "ECO gives you ", h("code", { text: "B90" }), ". Lichess gives you a ",
        "sixty-character string. Neither gives you the tree. OCN is ",
        h("code", { text: "B.Sic.Naj.Eng" }),
        " — machine-readable parents, transposition canonicalisation, keyed to both.",
      ]),
      h("p", { class: "hero-example" }, [
        h("a", { href: slugHref("B.Sic.Naj.Eng"), text: "B.Sic.Naj.Eng" }),
        h("a", { href: slugHref("C.RyL.Ber.Wal.End"), text: "C.RyL.Ber.Wal.End" }),
        h("a", { href: slugHref("E.KID.Cls.Mar"), text: "E.KID.Cls.Mar" }),
        h("a", { href: ecoHref("B90"), text: "B90" }),
      ]),
    ]),
    h("div", { class: "columns" }, [searchPanel(), converterBox("")]),
    treePanel(),
  );
  const input = document.getElementById("search-input");
  if (input && window.matchMedia("(min-width: 700px)").matches) input.focus();
}

function breadcrumb(slug) {
  const parts = slug.split(".");
  const crumbs = [];
  let prefix = "";
  parts.forEach((token, index) => {
    prefix = index === 0 ? token : `${prefix}.${token}`;
    const row = DB.bySlug.get(prefix);
    const last = index === parts.length - 1;
    if (index > 0) crumbs.push(h("span", { class: "crumb-sep", "aria-hidden": "true", text: ">" }));
    crumbs.push(h("a", {
      class: `crumb${last ? " current" : ""}`,
      href: slugHref(prefix),
      title: row ? row.name : prefix,
      "aria-current": last ? "page" : null,
    }, [
      h("code", { class: "crumb-token", text: token }),
      h("span", { class: "crumb-name", text: row ? row.name : "" }),
    ]));
  });
  return h("nav", { class: "breadcrumb", "aria-label": "Slug hierarchy" }, crumbs);
}

function lichessBlock(lichess) {
  const kind = lichess.kind === "exact"
    ? "exact match"
    : lichess.kind === "prefix"
      ? "prefix match, the nearest named Lichess line"
      : lichess.kind;
  return h("div", {}, [
    h("span", { class: "lichess-name", text: lichess.name }),
    h("span", { class: "note" }, [
      kind,
      lichess.eco ? ` (${lichess.eco})` : "",
    ]),
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
    h("span", {
      class: "note",
      text: "Lichess pool: rated blitz, rapid and classical from 1800 up",
    }),
  ]);
}

function attributionBlock(row) {
  return h("section", { class: "panel attribution" }, [
    h("h2", { text: "Attribution" }),
    h("dl", { class: "fields" }, [
      ...field("Named after", h("span", { text: row.attributed_to })),
      ...(row.attribution_source ? field("Source", h("span", { text: row.attribution_source })) : []),
      ...(row.historical_notes ? field("History", h("span", { text: row.historical_notes })) : []),
    ]),
  ]);
}

function relationsBlock(row) {
  const items = [];
  if (row.transposes_to) {
    items.push(...field("Transposes to", slugChip(row.transposes_to),
      h("span", { class: "note", text: "the same position, canonicalised there" })));
  }
  if (row.same_as && row.same_as.length) {
    items.push(...field("Same position as",
      h("span", { class: "chips" }, row.same_as.map(slugChip)),
      h("span", { class: "note", text: "co-canonical: both names are real" })));
  }
  if (!items.length) return null;
  return h("section", { class: "panel" }, [
    h("h2", { text: "Relations" }),
    h("dl", { class: "fields" }, items),
  ]);
}

function childrenBlock(row) {
  const kids = childrenOf(row.slug);
  if (!kids.length) return null;
  return h("section", { class: "panel" }, [
    h("h2", { text: `Sub-lines (${kids.length})` }),
    resultList(kids, ""),
  ]);
}

function renderRow(slug) {
  const view = document.getElementById("view");
  const row = DB.bySlug.get(slug);
  if (!row) {
    mount(view, h("section", { class: "panel" }, [
      h("h1", { text: "No such slug" }),
      h("p", {}, [h("code", { text: slug }), " is not in the catalogue."]),
      h("p", {}, [h("a", { class: "more", href: "#/", text: "Back to search" })]),
    ]));
    return;
  }

  const played = popularityLine(row);
  const facts = [
    ...(row.san ? field("Moves", h("span", { class: "movetext", text: row.san })) : []),
    ...(row.eco ? field("ECO", h("span", { class: "chips" }, row.eco.map(ecoChip))) : []),
    ...(row.lichess ? field("Lichess", lichessBlock(row.lichess)) : []),
    ...(played ? field("Played", played) : []),
    ...(row.aliases ? field("Also known as", h("span", { text: row.aliases.join(", ") })) : []),
    ...(row.flags ? field("Flags", h("span", { class: "chips" },
      row.flags.map((flag) => h("span", { class: "chip flat", text: flag })))) : []),
    ...field("Parent", row.parent
      ? slugChip(row.parent)
      : h("span", { class: "note", text: "class root, the top of its family" })),
  ];

  mount(view, 
    breadcrumb(row.slug),
    h("header", { class: "row-head" }, [
      h("h1", { text: row.name }),
      h("code", { class: "row-slug", text: row.slug }),
    ]),
    h("div", { class: "row-body" }, [
      h("section", { class: "panel board-panel" }, [
        boardSvg(row.fen),
        h("p", { class: "board-caption", text: sideToMove(row.fen) }),
        h("p", {}, [h("a", {
          class: "more",
          href: lichessUrl(row.fen),
          rel: "noopener",
          target: "_blank",
          text: "Analyse this position on Lichess",
        })]),
        h("p", { class: "fen" }, [h("code", { text: row.fen })]),
      ]),
      h("section", { class: "panel facts" }, [h("dl", { class: "fields" }, facts)]),
    ]),
    row.attributed_to ? attributionBlock(row) : null,
    relationsBlock(row),
    childrenBlock(row),
  );
}

function renderEco(query) {
  const view = document.getElementById("view");
  mount(view, 
    h("header", { class: "row-head" }, [
      h("h1", { text: "ECO converter" }),
      h("code", { class: "row-slug", text: query }),
    ]),
    converterBox(query),
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
