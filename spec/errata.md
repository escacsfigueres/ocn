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
a permanent redirect) rather than in-place migration. **The lifecycle
landed in v1.3**: it is a numbered normative procedure, the permanent
redirect sidecar `catalog/ocn-1.redirects.tsv` exists (shipped empty),
and `A.Hol` is designated its first scheduled case. In-place re-pointing
of a published slug is now a major (2.x) change under the field-level
table, so the QID migration could not recur inside a minor version.

## E-002 — 683 canonical names renamed under a minor version (1.2.0)

**What the spec said:** minor versions are for "new entries that do not
change the meaning of existing slugs."

**What happened:** release 1.2.0 renamed 683 `canonical_name` values
(diacritic normalisation, tiers 1-3) under a minor bump. No slug, move
sequence, or position changed — the *identity* of every row was stable,
and name-string joins were the only breakage, which the release notes
called out explicitly. Still, the rule as written did not authorise a
mass rename.

**Corrective policy:** versioning 2.0 **landed in v1.3**. It defines
field-level change classes — slug removal/re-point major; entry
addition, canonical-name change with changelog, new flag minor;
notes/aliases/attribution/i18n patch — which legalises this class of
release explicitly instead of by silence. 1.2.0 is its motivating
precedent, and under the table it is a minor with a required changelog
entry, which 1.2.0's release notes carried. The rule was written to
match a practice that was already correct; nothing about 1.2.0 is
re-litigated.

## E-003 — Published grammar narrower than the enforced grammar

**What the spec said (through v1.2):** the Format production allowed at
most six segments and at most two trailing SAN move segments.

**What was true:** the validator has always enforced
`class . named+ ( . san_move )*` with a 7-segment cap, and the released
catalogue contains 1,084 rows (18.4%) at seven segments and 1,393 rows
(23.6%) with three to five move segments. A second implementer reading
the spec literally would have rejected a quarter of the reference
catalogue.

**Corrective policy:** the Format section stated the enforced grammar in
the triage patch (2026-07-29), and **v1.3 replaced it with a normative
RFC 5234 ABNF**, the maximal-SAN-suffix token rule, and the normative
conformance corpus in `conformance/`. The grammar/profile split exists
so this cannot recur: the profile may only be tightened against a
catalogue that already satisfies the tighter rule, and a validator that
rejects a shipped row has found a spec bug (Conformance, V-5). Doctrine
going forward: the spec bends to the deployed catalogue; the catalogue
is never churned to satisfy a document.
