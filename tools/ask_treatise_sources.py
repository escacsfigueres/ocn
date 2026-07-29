#!/usr/bin/env python3
"""Put the treatise questions to a NotebookLM library, and record what comes back.

`docs/treatise-school-questions.md` says what each of the fifteen heads
has to answer before it can become a claim. This asks those questions
against a library of chess literature and history through the `nlm`
CLI, and writes the answers down verbatim with their citations.

It answers nothing itself. The output is evidence to read, not a
manifest: a head becomes a claim only after a human has looked at what
came back and decided the grade. Every question ends by telling the
assistant to say when a point cannot be established rather than infer
it, and an answer that says so is a useful answer -- it means the
library does not hold the source, which is worth knowing before anyone
spends an afternoon looking.

Usage:
    python3 tools/ask_treatise_sources.py --out docs/evidence/treatise
    python3 tools/ask_treatise_sources.py --head C.RyL --dry-run
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

#: The libraries worth asking, and why each one. Chess literature that
#: merely *uses* an opening name is not evidence about the name, which a
#: first pass established the hard way: the books notebooks answered
#: "the sources do not say who Ruy Lopez was" for every historical
#: question. Historical scholarship is what answers these.
NOTEBOOKS = {
    "winter-1": "f2d48aac-880d-4833-b4c3-e86699c9484b",
    "winter-2": "53612620-95bc-4945-8a14-8109dc39b8db",
    "winter-3": "a19ca649-56fb-4da0-9fce-5ada0495d9e0",
    "historia-es-1": "3f1a2d89-9915-4f12-ba8a-9290daac7c08",
    "historia-es-2": "bd054183-76f0-47ab-bd1b-ee03e6a03a48",
}

#: (head slug, opening, person, the doubt to press on). The doubt is the
#: part that makes each question specific rather than a template.
HEADS = [
    ("C.RyL", "Ruy Lopez (1.e4 e5 2.Nf3 Nc6 3.Bb5)", "Ruy Lopez de Segura",
     "He published a book in 1561. Did he originate 3.Bb5 or record and analyse a line already played?"),
    ("C.PhD", "Philidor Defence (1.e4 e5 2.Nf3 d6)", "Francois-Andre Danican Philidor",
     "L'analyse des echecs (1749) recommends this setup. Is the defence his advocacy or his invention?"),
    ("C.Pon", "Ponziani Opening (1.e4 e5 2.Nf3 Nc6 3.c3)", "Domenico Lorenzo Ponziani",
     "His 1769 book was published anonymously. How is authorship established, and who named the opening for him?"),
    ("C.Dam", "Damiano Defence (1.e4 e5 2.Nf3 f6)", "Pedro Damiano",
     "Damiano condemned 2...f6 rather than recommending it. Is the opening named for its analyst or its critic?"),
    ("C.RyL.Coz", "Ruy Lopez, Cozio Defence (3...Nge7)", "Carlo Cozio",
     "His manuscript circulated well before the 1766 printing. Which is the citable source?"),
    ("C.RyL.Luc", "Ruy Lopez, Lucena Variation", "Luis Ramirez de Lucena",
     "His 1497 book predates Ruy Lopez's by 64 years. What exactly is the line called after him, and on what authority?"),
    ("C.Sco.Nxd4", "Scotch Game, Lolli Variation", "Giambattista Lolli",
     "Which line in the Scotch carries Lolli's name, and who attached it?"),
    ("C.Pon.Jae", "Ponziani, Jaenisch Counterattack", "Carl Friedrich Jaenisch",
     "Jaenisch has several eponyms. Confirm this one is his rather than a namesake line."),
    ("A.Hol.Sta", "Dutch Defence, Staunton Gambit (1.d4 f5 2.e4)", "Howard Staunton",
     "Did Staunton play or publish 2.e4 against the Dutch, and where?"),
    ("C.KGm.Acc.Sta", "King's Gambit Accepted, Stamma Gambit", "Philipp Stamma",
     "Stamma's 1737 Essai is largely endgame studies. Does it contain this gambit?"),
    ("C.LtO.Bil", "Latvian Gambit, Bilguer Variation", "Paul Rudolf von Bilguer",
     "The Handbuch was completed and published after Bilguer's death. Is the line his own work?"),
    ("C.Bsh.Ber.f4", "Bishop's Opening, Greco Gambit line", "Gioachino Greco",
     "Greco left manuscripts rather than a printed book. Which manuscript, and in which modern edition is it reproduced?"),
    ("C.Ita.Two.Ng5.Pol", "Two Knights Defence, Polerio Defence", "Giulio Cesare Polerio",
     "Same manuscript problem as Greco. What is the citable modern source?"),
    ("D.QPG.c4.c5.dxc5.d4", "Queen's Gambit Austrian, Salvio Countergambit", "Alessandro Salvio",
     "Salvio's 1604 Trattato is about open games. Does it contain a queen's-pawn line at all?"),
]

TEMPLATE = """For the chess opening known as {opening}, said to be named after {person}:

1. Which reference work or historical source states that the opening is named after this person? Give the work, edition and page or entry.
2. In which of their own publications does the relevant analysis appear? Give the title, the edition and the year of that edition.
3. Was this person the inventor of the line, the first to publish an analysis of it, or the populariser of a line already played? Quote the passage that decides it.
4. Does any source dispute the attribution or credit someone else?

Specific doubt to address: {doubt}

If a point cannot be established from the sources available to you, say so plainly rather than inferring it. An honest "not in these sources" is more useful to me than a plausible guess."""


def ask(notebook_id: str, question: str, timeout: int) -> dict:
    """One query, returned as the CLI's JSON or an error record."""
    proc = subprocess.run(
        ["nlm", "notebook", "query", notebook_id, question, "--json"],
        capture_output=True, text=True, timeout=timeout,
    )
    if proc.returncode != 0:
        return {"error": (proc.stderr or proc.stdout).strip()[:400]}
    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return {"error": "unparseable response", "raw": proc.stdout[:400]}
    return payload.get("value", payload)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out", type=Path, default=REPO_ROOT / "docs" / "evidence" / "treatise")
    parser.add_argument("--head", action="append",
                        help="only this head; repeatable")
    parser.add_argument("--notebook", action="append",
                        help="only this library key; repeatable")
    parser.add_argument("--timeout", type=int, default=420)
    parser.add_argument("--dry-run", action="store_true",
                        help="print the questions and ask nothing")
    args = parser.parse_args(sys.argv[1:] if argv is None else argv)

    heads = [h for h in HEADS if not args.head or h[0] in args.head]
    books = {k: v for k, v in NOTEBOOKS.items() if not args.notebook or k in args.notebook}
    if not heads:
        print("no such head", file=sys.stderr)
        return 1

    print(f"{len(heads)} head(s) against {len(books)} librar(ies) = "
          f"{len(heads) * len(books)} queries", file=sys.stderr)

    if args.dry_run:
        for slug, opening, person, doubt in heads:
            print(f"\n=== {slug} ===")
            print(TEMPLATE.format(opening=opening, person=person, doubt=doubt))
        return 0

    args.out.mkdir(parents=True, exist_ok=True)
    for index, (slug, opening, person, doubt) in enumerate(heads, 1):
        question = TEMPLATE.format(opening=opening, person=person, doubt=doubt)
        record = {"head": slug, "opening": opening, "person": person,
                  "doubt": doubt, "question": question, "answers": {}}
        for key, notebook_id in books.items():
            print(f"[{index}/{len(heads)}] {slug} <- {key}", file=sys.stderr, flush=True)
            started = time.monotonic()
            try:
                record["answers"][key] = ask(notebook_id, question, args.timeout)
            except subprocess.TimeoutExpired:
                record["answers"][key] = {"error": f"timed out after {args.timeout}s"}
            print(f"    {time.monotonic() - started:.0f}s", file=sys.stderr, flush=True)
        path = args.out / f"{slug.replace('.', '_')}.json"
        path.write_text(json.dumps(record, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"    wrote {path}", file=sys.stderr, flush=True)
    print("done", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
