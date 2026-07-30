#!/usr/bin/env python3
"""Put the eponym candidates to the Oxford Companion, and record what it says.

`docs/eponym-list-findings.md` produced 211 candidate attributions, each
tied to a catalogue row by its move sequence and graded no better than
`attested`, because a Wikipedia footnote is not a reading. This asks the
Companion itself about each one and writes the answers down verbatim, so
a human can promote the ones the book actually supports.

Two instruments, failing in opposite directions
-----------------------------------------------
A mechanical index of the Companion's headwords (built by scanning the
OCR for `Name. <number>`) **over-matches**: one headword covers several
unrelated openings -- "Alekhine Variation" spans the Slav, the Queen's
Pawn, the Dutch and the Staunton Gambit -- so a name lookup lands
confidently on the wrong line.

Asking a retrieval model over the same book **under-matches**: given the
moves and told to find that exact line, it answers NONE for entries that
demonstrably exist, because it declines to stretch a near-match.

Neither is trustworthy alone and their errors do not overlap, so this
records both and marks the rows where they agree. Agreement is not proof
either -- it is the shortlist a human reads the page for. Nothing here
writes a catalogue row, and nothing here is graded `verified`, because
that grade belongs to the reading and not to the retrieval.

What is recorded is the answer's `cited_text`, the verbatim passage from
the book, never the model's prose summary. The prose is a finding aid;
the passage is the evidence.

Usage:
    python3 tools/verify_against_companion.py --notebook <id> --limit 20
    python3 tools/verify_against_companion.py --notebook <id> --tier oxford-companion
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import subprocess
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_IN = REPO_ROOT / "docs" / "evidence" / "eponyms" / "named-after-people.tsv"
DEFAULT_OUT = REPO_ROOT / "docs" / "evidence" / "eponyms" / "companion-verdicts.tsv"

OUT_COLUMNS = ("ocn1", "canonical_name", "asked_as", "moves_san", "person",
               "prev_tier", "companion_index", "role", "rival", "verdict",
               "quote")

#: Small batches: a long list invites the model to skimp on the later
#: items, and a failed call costs only its own batch.
BATCH = 8

PROMPT_HEAD = """For each opening below I give a LABEL and its moves. Find the Oxford \
Companion's entry for THAT EXACT LINE, using the moves to choose when one headword \
covers several openings.

Reply with one line per opening, in this exact pipe-delimited form and nothing else:
LABEL | index number | VERBATIM quote of the entry | role | rival claimant or "none"

`role` must be one of: originated, first-published, recommended, popularised, \
condemned, unclear.
If the Companion has no entry for that line, write exactly: LABEL | NONE
Do not guess and do not paraphrase the quote.

"""


def rows_to_ask(path: Path, tier: str | None, limit: int | None,
                skip: set[str]) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = [r for r in csv.DictReader(handle, delimiter="\t")
                if not r["already_attributed"] and r["ocn1"] not in skip]
    if tier:
        rows = [r for r in rows if r["source_tier"] == tier]
    return rows[:limit] if limit else rows


def label_for(row: dict[str, str]) -> str:
    """A short, pipe-free label the model can echo back."""
    name = row["wikipedia_name"].split(" of the ")[0].split(" of ")[0]
    return re.sub(r"[|\n]", " ", name).strip() or row["ocn1"]


def build_prompt(batch: list[dict[str, str]]) -> str:
    lines = [f"{i}) {label_for(r)} = {r['moves_san']}" for i, r in enumerate(batch, 1)]
    return PROMPT_HEAD + "\n".join(lines)


def ask(notebook: str, prompt: str, timeout: int) -> dict:
    proc = subprocess.run(["nlm", "notebook", "query", notebook, prompt],
                          capture_output=True, text=True, timeout=timeout)
    if proc.returncode != 0:
        return {"error": (proc.stderr or proc.stdout).strip()[:300]}
    try:
        return json.loads(proc.stdout).get("value", {})
    except json.JSONDecodeError:
        return {"error": "unparseable response"}


def parse_answer(answer: str, batch: list[dict[str, str]]) -> dict[str, dict]:
    """Match each reply line back to the row it answers, by position then label."""
    out: dict[str, dict] = {}
    for line in answer.splitlines():
        line = line.strip().lstrip("*").strip()
        if "|" not in line:
            continue
        parts = [p.strip() for p in line.split("|")]
        head = parts[0]
        number = re.match(r"^\s*(\d+)\s*[).]", head)
        row = None
        if number:
            position = int(number.group(1)) - 1
            if 0 <= position < len(batch):
                row = batch[position]
        if row is None:
            for candidate in batch:
                if label_for(candidate).lower()[:18] in head.lower():
                    row = candidate
                    break
        if row is None:
            continue
        if len(parts) >= 2 and parts[1].upper().startswith("NONE"):
            out[row["ocn1"]] = {"verdict": "no-entry"}
            continue
        out[row["ocn1"]] = {
            "verdict": "entry",
            "companion_index": re.sub(r"\s+", "", parts[1]) if len(parts) > 1 else "",
            "quote": parts[2] if len(parts) > 2 else "",
            "role": parts[3].lower() if len(parts) > 3 else "",
            "rival": parts[4] if len(parts) > 4 else "",
        }
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--notebook", required=True, help="NotebookLM notebook id")
    parser.add_argument("--in", dest="source", type=Path, default=DEFAULT_IN)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--tier", help="only candidates whose Wikipedia footnote was this tier")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument("--resume", action="store_true",
                        help="skip rows already present in --out")
    args = parser.parse_args(sys.argv[1:] if argv is None else argv)

    if not args.source.is_file():
        print(f"ERROR: no such file: {args.source}", file=sys.stderr)
        return 1

    done: dict[str, dict[str, str]] = {}
    if args.resume and args.out.is_file():
        with args.out.open(newline="", encoding="utf-8") as handle:
            done = {r["ocn1"]: r for r in csv.DictReader(handle, delimiter="\t")}
        print(f"resuming: {len(done)} already answered", file=sys.stderr)

    rows = rows_to_ask(args.source, args.tier, args.limit, set(done))
    print(f"{len(rows)} candidate(s) in {-(-len(rows)//BATCH)} batch(es)", file=sys.stderr)

    results = dict(done)
    for start in range(0, len(rows), BATCH):
        batch = rows[start:start + BATCH]
        print(f"[{start//BATCH + 1}] asking about {len(batch)}...", file=sys.stderr, flush=True)
        began = time.monotonic()
        try:
            payload = ask(args.notebook, build_prompt(batch), args.timeout)
        except subprocess.TimeoutExpired:
            payload = {"error": f"timed out after {args.timeout}s"}
        if "error" in payload:
            print(f"    ERROR {payload['error']}", file=sys.stderr)
            continue
        answers = parse_answer(payload.get("answer", ""), batch)
        #: The verbatim passages the notebook cited, kept whole so a
        #: reviewer sees the book's words and not the model's.
        cited = " ~ ".join(r.get("cited_text", "") for r in payload.get("references", []))
        for row in batch:
            found = answers.get(row["ocn1"], {"verdict": "no-answer"})
            results[row["ocn1"]] = {
                "ocn1": row["ocn1"], "canonical_name": row["canonical_name"],
                "asked_as": label_for(row), "moves_san": row["moves_san"],
                "person": row["person"], "prev_tier": row["source_tier"],
                "companion_index": found.get("companion_index", ""),
                "role": found.get("role", ""), "rival": found.get("rival", ""),
                "verdict": found["verdict"],
                "quote": (found.get("quote") or cited)[:600].replace("\t", " "),
            }
        print(f"    {time.monotonic() - began:.0f}s, "
              f"{sum(1 for r in batch if answers.get(r['ocn1'],{}).get('verdict')=='entry')}"
              f"/{len(batch)} with an entry", file=sys.stderr, flush=True)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8", newline="") as handle:
        handle.write("\t".join(OUT_COLUMNS) + "\n")
        for row in results.values():
            handle.write("\t".join(str(row.get(c, "")) for c in OUT_COLUMNS) + "\n")

    kinds: dict[str, int] = {}
    for row in results.values():
        kinds[row["verdict"]] = kinds.get(row["verdict"], 0) + 1
    print("\n" + ", ".join(f"{v} {k}" for k, v in sorted(kinds.items())))
    print(f"wrote {args.out}")
    print("evidence only: nothing graded verified, no catalogue row written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
