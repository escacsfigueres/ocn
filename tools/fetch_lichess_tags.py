"""Fetch Event, Site, Date and Round for the proposal games from Lichess.

Lichess publishes its data under CC0 and documents this endpoint for public
use. Bulk export takes up to 300 ids per request, so 1,172 games is four
requests. The result is cached to game-tags.tsv and never fetched twice.
"""

import csv
import re
import sys
import time
import urllib.request
from pathlib import Path

OCN = Path.home() / "Code" / "ocn"
HERE = Path(__file__).resolve().parent
OUT = HERE / "game-tags.tsv"
ENDPOINT = ("https://lichess.org/api/games/export/_ids"
            "?moves=false&clocks=false&evals=false&tags=true")
BATCH = 300

ids = []
seen = set()
for r in csv.DictReader((OCN / "docs/evidence/provenance/notable-games.tsv").open(),
                        delimiter="\t"):
    gid = r["lichess_id"].strip()
    if gid and gid not in seen:
        seen.add(gid)
        ids.append(gid)
print(f"{len(ids)} distinct game ids")

TAG = re.compile(r'\[(\w+)\s+"([^"]*)"\]')


def fetch(chunk):
    req = urllib.request.Request(
        ENDPOINT, data=",".join(chunk).encode(),
        headers={"Content-Type": "text/plain", "Accept": "application/x-chess-pgn",
                 "User-Agent": "OCN monograph builder (escacsfigueres/ocn)"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        return resp.read().decode("utf-8", "replace")


rows = {}
for i in range(0, len(ids), BATCH):
    chunk = ids[i:i + BATCH]
    for attempt in range(4):
        try:
            body = fetch(chunk)
            break
        except Exception as exc:            # noqa: BLE001
            wait = 5 * (attempt + 1)
            print(f"  retry in {wait}s ({exc})", file=sys.stderr)
            time.sleep(wait)
    else:
        print("  giving up on this batch", file=sys.stderr)
        continue
    for block in body.split("\n\n\n"):
        tags = dict(TAG.findall(block))
        gid = tags.get("GameId")
        if gid:
            rows[gid] = tags
    print(f"  {min(i + BATCH, len(ids))}/{len(ids)}")
    time.sleep(1.5)

with OUT.open("w", newline="") as fh:
    w = csv.writer(fh, delimiter="\t", lineterminator="\n")
    w.writerow(["lichess_id", "event", "site", "date", "round"])
    for gid in ids:
        t = rows.get(gid, {})
        w.writerow([gid, t.get("Event", ""), t.get("Site", ""),
                    t.get("Date", ""), t.get("Round", "")])

got = sum(1 for gid in ids if gid in rows)
print(f"wrote {OUT}: {got} of {len(ids)} enriched")
