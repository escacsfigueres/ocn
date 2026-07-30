#!/usr/bin/env python3
"""Ask the Companion about one line inside an entry that covers several.

`tools/generate_companion_manifest.py` holds back every row whose entry
describes more than one opening, because the role that comes back may
belong to a sibling line. The Sämisch entry covers the Slav, the Queen's
Gambit Declined, the Nimzo-Indian and the King's Indian; a role read off
it as a whole says nothing reliable about which of the four our row is.

Held is the right default and a poor destination. This asks again,
naming the entry and the exact line, and requiring the answer to quote
only the clause describing *that* line. The Flohr entry then stops being
"several openings, unusable" and becomes "574 in the Caro-Kann, an idea
of Opocensky's played twice by Flohr at Moscow 1935" -- a populariser,
with a rival claimant the whole-entry reading could never have found.

The narrowing is the same one the Companion graph needed: the clause
governs, not the entry.

Usage:
    python3 tools/resolve_multi_entries.py --notebook <id>
    python3 tools/resolve_multi_entries.py --notebook <id> --resume
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
sys.path.insert(0, str(REPO_ROOT / "tools"))

import generate_companion_manifest as gen  # noqa: E402

DEFAULT_IN = REPO_ROOT / "docs" / "evidence" / "eponyms" / "companion-verdicts.tsv"
DEFAULT_OUT = REPO_ROOT / "docs" / "evidence" / "eponyms" / "companion-sublines.tsv"

COLUMNS = ("ocn1", "canonical_name", "asked_as", "moves_san", "person",
           "clause", "role", "rival", "verdict")

BATCH = 6

PROMPT = """Each entry below covers SEVERAL openings. For each, I give the entry name \
and the exact line I care about. Quote ONLY the clause of that entry describing THAT \
line, and say what role it gives the named person FOR THAT LINE ALONE.

Reply one line each, pipe-delimited, nothing else:
LABEL | verbatim clause for that line only | role | rival or none
role from: originated, first-published, recommended, popularised, condemned, unclear.
If the entry says nothing about that specific line, write: LABEL | NOTHING

"""


def held_rows(path: Path) -> list[dict[str, str]]:
    """The rows the manifest generator sets aside as multi-opening."""
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    return [r for r in rows
            if r["verdict"] == "entry"
            and gen.openings_in_quote(r["quote"]) > 1
            and gen.quote_names(r["quote"], r["person"])]


def build_prompt(batch: list[dict[str, str]]) -> str:
    lines = []
    for index, row in enumerate(batch, 1):
        label = re.sub(r"[|\n]", " ", row["asked_as"]).strip()
        family = row["canonical_name"].split(",")[0]
        lines.append(f"{index}) {label} — {family}, {row['moves_san']}")
    return PROMPT + "\n".join(lines)


def parse_answer(answer: str, batch: list[dict[str, str]]) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for line in answer.splitlines():
        line = line.strip().lstrip("*").strip()
        if "|" not in line:
            continue
        parts = [p.strip() for p in line.split("|")]
        row = None
        numbered = re.match(r"^\s*(\d+)\s*[).]", parts[0])
        if numbered:
            position = int(numbered.group(1)) - 1
            if 0 <= position < len(batch):
                row = batch[position]
        if row is None:
            for candidate in batch:
                if candidate["asked_as"].lower()[:16] in parts[0].lower():
                    row = candidate
                    break
        if row is None:
            continue
        if len(parts) >= 2 and parts[1].upper().startswith("NOTHING"):
            out[row["ocn1"]] = {"verdict": "no-clause"}
            continue
        out[row["ocn1"]] = {
            "verdict": "clause",
            "clause": parts[1] if len(parts) > 1 else "",
            "role": parts[2].lower() if len(parts) > 2 else "",
            "rival": parts[3] if len(parts) > 3 else "",
        }
    return out


def ask(notebook: str, prompt: str, timeout: int) -> dict:
    proc = subprocess.run(["nlm", "notebook", "query", notebook, prompt],
                          capture_output=True, text=True, timeout=timeout)
    if proc.returncode != 0:
        return {"error": (proc.stderr or proc.stdout).strip()[:300]}
    try:
        return json.loads(proc.stdout).get("value", {})
    except json.JSONDecodeError:
        return {"error": "unparseable response"}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--notebook", required=True)
    parser.add_argument("--in", dest="source", type=Path, default=DEFAULT_IN)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args(sys.argv[1:] if argv is None else argv)

    done: dict[str, dict[str, str]] = {}
    if args.resume and args.out.is_file():
        with args.out.open(newline="", encoding="utf-8") as handle:
            done = {r["ocn1"]: r for r in csv.DictReader(handle, delimiter="\t")}
        print(f"resuming: {len(done)} already resolved", file=sys.stderr)

    rows = [r for r in held_rows(args.source) if r["ocn1"] not in done]
    print(f"{len(rows)} held row(s) in {-(-len(rows)//BATCH)} batch(es)", file=sys.stderr)

    results = dict(done)
    for start in range(0, len(rows), BATCH):
        batch = rows[start:start + BATCH]
        print(f"[{start//BATCH + 1}] {len(batch)} lines...", file=sys.stderr, flush=True)
        began = time.monotonic()
        try:
            payload = ask(args.notebook, build_prompt(batch), args.timeout)
        except subprocess.TimeoutExpired:
            payload = {"error": f"timed out after {args.timeout}s"}
        if "error" in payload:
            print(f"    ERROR {payload['error']}", file=sys.stderr)
            continue
        answers = parse_answer(payload.get("answer", ""), batch)
        for row in batch:
            found = answers.get(row["ocn1"], {"verdict": "no-answer"})
            results[row["ocn1"]] = {
                "ocn1": row["ocn1"], "canonical_name": row["canonical_name"],
                "asked_as": row["asked_as"], "moves_san": row["moves_san"],
                "person": row["person"],
                "clause": found.get("clause", "")[:600].replace("\t", " "),
                "role": found.get("role", ""), "rival": found.get("rival", ""),
                "verdict": found["verdict"],
            }
        got = sum(1 for r in batch if answers.get(r["ocn1"], {}).get("verdict") == "clause")
        print(f"    {time.monotonic() - began:.0f}s, {got}/{len(batch)} resolved",
              file=sys.stderr, flush=True)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8", newline="") as handle:
        handle.write("\t".join(COLUMNS) + "\n")
        for row in results.values():
            handle.write("\t".join(str(row.get(c, "")) for c in COLUMNS) + "\n")

    kinds: dict[str, int] = {}
    for row in results.values():
        kinds[row["verdict"]] = kinds.get(row["verdict"], 0) + 1
    print("\n" + ", ".join(f"{v} {k}" for k, v in sorted(kinds.items())))
    print(f"wrote {args.out}")
    print("evidence only: no manifest, no catalogue row")
    return 0


if __name__ == "__main__":
    sys.exit(main())
