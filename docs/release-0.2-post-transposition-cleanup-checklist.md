# Release candidate — post-transposition-cleanup (`ad25527`)

**Status**: CANDIDATE NOTE (planning only). **No tag, no release,
no artefacts, no catalogue change** accompany this document. It
records what a release of the current `main` would look like and
the open decision about whether/when to cut it.

## Candidate ref

- **`ad25527`** — current `origin/main`. Transposition cleanup
  complete except the one governed QID hold.

## Relation to existing tags

| ref | commit | role |
|---|---|---|
| `ocn-1.0.2` | `415f1df` | release baseline (immutable) |
| `ocn-1.0.3` | `dd2abd3` | post-cleanup release **with downloadable assets** (positions.tsv, openings.parquet, manifest) |
| **`ad25527`** | (current `main`) | **30 commits ahead of `dd2abd3`** — transposition cleanup complete (1 governed hold left). Not tagged. |

The two tags stay immutable. `ad25527` is current development state;
this note is about whether to cut a new tag on it.

## What changed since `ocn-1.0.3` (`dd2abd3` → `ad25527`, 30 commits)

- **`same_as` programme**: Larsen, London Classical/Mason cascade,
  Van Geet/Van't Kruijs (mixed Option D), QGA Flohr/Janowski,
  Budapest Adler/Rubinstein 3-level cascade, KID Simagin/Uhlmann,
  Modern/Sicilian Western Pterodactyl → multiple_canonical 12 → 17.
- **Mechanical + parent-child cleanup**: English Symmetrical Three
  Knights TT, parent-child batch (4 TT + 3 DELETE), 14-group
  mechanical batch (12 TT + 2 DELETE), Scandinavian/Amar TT.
- **Nimzo Bot/Kmo RESOLVED** (`e036203`) — `E.Nim.Sml.Kmo
  transposes_to E.Nim.Sml.Bot`, spurious "Kmoch" demoted (Lichess
  E20: Kmoch = 4.f3 = `E.Nim.Fou`).
- **QID Miles/Petrosian** — diagnosed, preflighted, and **governed**
  (decision record); **not applied** by release-governance choice.
- Docs: unresolved map, closure record, all per-case proposals,
  QID structural/preflight/decision docs.

Net since `1.0.3`: unresolved groups down to **1**, the catalogue is
fully resolved except one internal, non-position-visible
slug-migration hold.

## Current metrics (`ad25527`)

| metric | value |
|---|---|
| catalogue rows | 5,900 |
| schema columns | 14 (unchanged downstream contract) |
| duplicate_groups | 125 |
| resolved_groups | 124 |
| unresolved_groups | **1** (QID only) |
| multiple_canonical_groups | 17 |
| tests | 60/60 OK |
| lichess parent-map | 3690/3690 |

## Known limitation (single, documented, governed)

**QID Miles/Petrosian slug-migration hold** — `E.QID.Mil.MLn` is the
mislabelled Kasparov-Petrosian subtree under "Miles" with a broken
parent chain; fix = re-slug under `E.QID.Pet.KPe` (OCN's first
slug-rename). Internal naming/hierarchy only — **invisible to
position-lookup consumers** (they join on FEN/zobrist). Fully
documented:
[`qid-miles-petrosian-structural-proposal.md`](qid-miles-petrosian-structural-proposal.md),
[`qid-miles-petrosian-migration-preflight.md`](qid-miles-petrosian-migration-preflight.md),
[`qid-migration-decision-record.md`](qid-migration-decision-record.md)
(decision: Option C — apply with the next release/tag, not in-cold).

## Release options

### A — No release; keep `main` as current development state

Leave `ad25527` as development head; consumers keep using
`ocn-1.0.3`. Zero work. Downside: the 30 commits of cleanup
(esp. the `same_as` additions and Nimzo fix) aren't in a tagged,
asset-backed release.

### B — Tag `ocn-1.0.4` on `ad25527` with regenerated artefacts

Cut a release of the "almost fully resolved" state now: 1 known
governed hold, 17 multiple-canonical groups, Nimzo fixed. Regenerate
positions.tsv + openings.parquet, record sha256s, annotate the tag,
upload assets. Downside: the QID hold ships unresolved (documented),
so it's a "1 unresolved" release.

### C — Wait, apply QID in a release-cycle, then tag

Hold the next tag until QID is applied (per its decision record),
so the next release is a clean **"0 unresolved"**. Downside: the
substantial cleanup since `1.0.3` stays untagged longer; couples
the release to the first-ever slug-migration.

## Recommendation

- **B** if the goal is to make the current, much-improved
  "almost fully resolved" state consumable now (the QID hold is
  internal/non-position and fully documented — a "1 unresolved"
  release is honest and useful).
- **C** if the goal is for the next release to be a clean
  "0 unresolved" milestone — then bundle QID (its decision record
  already recommends riding a release boundary) and tag afterwards.

Either is defensible; **no immediate action is required**. This note
exists so the choice is explicit when a release is wanted.

> **UPDATE (2026-05-26): Option C selected and the catalogue is now
> at 0 unresolved.** The QID slug-migration was applied (`5208e08`);
> the catalogue is fully resolved (5,899 rows). **Candidate
> artefacts exist locally but are NOT uploaded**, in
> `/private/tmp/ocn-1.1.0-candidate/`:
> - `ocn-1.positions.tsv` — sha256 `0e78c315c62b1c37a7267b5df3c82f98e1af4e1ae0dbe8e9d47fc68211d89d7d`, 5,899 data rows
> - `openings.parquet` — sha256 `a9180bfcd4fee272f0a9a76e866ffbe4ca2311ea68f373b435a5aff75209a5c2`, 369,663 B, 13-col schema (unchanged), zobrist polyglot-v1.0
> - `_efcdb_manifest.json` — sha256 `a8aa50e904328e240290c1f17c56578a3c71875629f953b901ff551ca4ede9f6`
>
> Both regenerated against the migrated catalogue and
> downstream-verified (producer absorbed the 10 renamed
> `canonical_ocn1`; no schema/code change; chess-parquet tests
> green). Remaining release steps (final changelog, tag `ocn-1.1.0`,
> upload) are GO-gated — see
> [`qid-release-cycle-checklist.md`](qid-release-cycle-checklist.md)
> steps 7-9.

## Future commands (DO NOT EXECUTE here — release-time only)

When a release (Option B or C) is GO'd:

```bash
# 1. Regenerate the position index from the tagged commit
python3 tools/export_positions.py --include-roots --stats --out /tmp/ocn-1.positions.tsv

# 2. Regenerate openings.parquet via chess-parquet's efcdb-openings producer
#    (coordinate with that repo; confirm canonical_ocn1 materialisation)
#    efcdb-openings ... --out /tmp/openings.parquet

# 3. Checksums for the release notes
shasum -a 256 /tmp/ocn-1.positions.tsv /tmp/openings.parquet /tmp/_efcdb_manifest.json

# 4. Annotated tag (example for Option B)
git tag -a ocn-1.0.4 -m "OCN 0.2 post-transposition-cleanup (1 governed QID hold)"
git push origin ocn-1.0.4

# 5. GitHub release + asset upload
gh release create ocn-1.0.4 --title "..." --notes-file ... \
   /tmp/ocn-1.positions.tsv /tmp/openings.parquet /tmp/_efcdb_manifest.json
```

**Note**: the `ocn-1.0.3` assets are stale relative to `ad25527`
(30 commits of `same_as`/TT/DELETE since), so positions.tsv WILL have
a new sha256 — regenerate fresh; do not reuse the `1.0.3` checksums.
Prior `1.0.3` asset sha256s are recorded in
[`release-0.2-checklist.md`](release-0.2-checklist.md) for reference.

## Gating

No tag/release/artefact work happens without an explicit GO. If the
release also applies QID, follow the QID decision-record GO
checklist first (chess-parquet smoke test, etc.). This candidate
note changes nothing in `catalog/ocn-1.csv`.
