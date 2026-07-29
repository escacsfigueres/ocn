# OCN-1 spec errata

Deviations from the spec's own rules, and clauses the spec has had to
correct about itself. Recorded openly, before anyone else finds them:
an erratum published by the project is process; one discovered by a
reader is a scandal. Each entry names the corrective policy.

## E-001 — Slug re-pointed across a release boundary (QID migration)

**What the spec said:** "Once a release is tagged, an entry's `ocn1`
MUST NOT be re-pointed to a different position."

**What happened:** during the transposition-resolution era, ten QID
rows were slug-migrated (the Miles head renamed to the
Kasparov-Petrosian head) inside a release cycle, re-pointing tagged
identifiers. The full reasoning and preflight are in
[`docs/qid-migration-decision-record.md`](../docs/qid-migration-decision-record.md);
it was the right structural call, made without an exception path
existing on paper.

**Corrective policy:** this class of change now requires the
deprecation lifecycle (mark `deprecated`, add the successor entry, keep
a permanent redirect) rather than in-place migration. The lifecycle,
including its first worked example, is spec 1.3 work (roadmap H2.4);
until it lands, no further slug re-points are permitted at all.

## E-002 — 683 canonical names renamed under a minor version (1.2.0)

**What the spec said:** minor versions are for "new entries that do not
change the meaning of existing slugs."

**What happened:** release 1.2.0 renamed 683 `canonical_name` values
(diacritic normalisation, tiers 1-3) under a minor bump. No slug, move
sequence, or position changed — the *identity* of every row was stable,
and name-string joins were the only breakage, which the release notes
called out explicitly. Still, the rule as written did not authorise a
mass rename.

**Corrective policy:** versioning 2.0 (spec 1.3, roadmap H2.4) defines
field-level change classes — slug removal/re-point major; entry
addition, canonical-name change with changelog, new flag minor;
notes/aliases/attribution patch — which legalises this class of release
explicitly instead of by silence. 1.2.0 is its motivating precedent.

## E-003 — Published grammar narrower than the enforced grammar

**What the spec said (through v1.2):** the Format production allowed at
most six segments and at most two trailing SAN move segments.

**What was true:** the validator has always enforced
`class . named+ ( . san_move )*` with a 7-segment cap, and the released
catalogue contains 1,084 rows (18.4%) at seven segments and 1,393 rows
(23.6%) with three to five move segments. A second implementer reading
the spec literally would have rejected a quarter of the reference
catalogue.

**Corrective policy:** the Format section now states the enforced
grammar (triage patch, 2026-07-29). The normative ABNF, the
maximal-SAN-suffix token rule, and the conformance corpus land in spec
1.3 (roadmap H2.4). Doctrine going forward: the spec bends to the
deployed catalogue; the catalogue is never churned to satisfy a
document.
