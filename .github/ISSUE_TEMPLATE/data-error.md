---
name: Data error
about: A catalogue field is wrong, or a tool returns the wrong result
title: "[data] <slug>: "
labels: data-error
---

<!--
Read CONTRIBUTING.md first. Report the error here; do not attach a diff
against catalog/ocn-1.csv, which is never hand-edited.
-->

**Slug or slugs**
<!-- The OCN-1 slug(s) affected, e.g. B.Sic.Naj. List them if a group
     shares the same error. -->

**Field**
<!-- eco_legacy / moves_uci / parent_ocn1 / depth / flags /
     transposes_to / same_as / aliases / notes, or the tool at fault. -->

**Expected**
<!-- What the field or the tool output should be. -->

**Actual**
<!-- What it is now, quoted verbatim. -->

**Reproduction**
<!-- The command you ran and its output, if any. For example:

python3 tools/from_eco.py B90
python3 tools/from_uci.py e2e4 c7c5 g1f3 d7d6
python3 tools/validate.py --strict-chess catalog/ocn-1.csv
-->

```
```

**Catalogue version**
<!-- Release tag (e.g. ocn-1.2.0) or commit you checked against. -->

**Why it is wrong**
<!-- A source, a legal-move argument, an ECO reference, a position.
     For a naming or attribution claim, use the naming-dispute template
     instead. -->
