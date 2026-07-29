# external/ — vendored upstream snapshots

`lichess-openings/` is a snapshot of the five TSVs from
[lichess-org/chess-openings](https://github.com/lichess-org/chess-openings)
(CC0 public domain), vendored 2026-04-28 via `tools/fetch_lichess.sh`.
It is the pinned input for `tools/build_lichess_xref.py` and its drift
test: the committed `catalog/ocn-1.lichess-xref.tsv` must always equal a
rebuild from exactly this snapshot, so CI needs it in-tree. Refreshing
the snapshot is a deliberate act (rerun the fetch script, regenerate the
xref, commit both together).
