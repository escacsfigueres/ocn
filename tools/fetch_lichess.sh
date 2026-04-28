#!/usr/bin/env bash
# Fetch the Lichess opening book TSVs (lichess-org/chess-openings, CC0)
# into external/lichess-openings/. Used by EFCDB's `efcdb lichess`
# subcommand to build lichess_openings.parquet.
#
# We do NOT vendor the TSVs in this repo — they are upstream and refresh
# at Lichess's pace. Re-run this script to update.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DEST="$REPO_ROOT/external/lichess-openings"
mkdir -p "$DEST"

for letter in a b c d e; do
  url="https://raw.githubusercontent.com/lichess-org/chess-openings/master/${letter}.tsv"
  echo "Fetching $letter.tsv..."
  curl -fsSL "$url" -o "$DEST/$letter.tsv"
done

echo
wc -l "$DEST"/*.tsv
echo
echo "Done. Built: $DEST"
