# Agentic development playbook

**Status**: methodology only. **No catalogue, tag, or release change**
accompanies this document. It defines *how* we work with an AI coding
agent (Claude Code) on this repository — the human–agent contract, the
gates, and the verification discipline. It does **not** propose or apply
any catalogue edit.

## Purpose

OCN's quality came from a process, not from luck. The transposition
cleanup and the 1.1.0 release cycle worked because every change went
through the same loop: **propose → review → apply**, with a **decision
record** before anything risky, a **preflight** before delicate
mechanics, an **explicit GO** before every mutating or remote action,
and **verification + cross-session memory** after. This playbook names
that loop so it is repeatable, teachable, and applied the same way every
time — by a human or an agent.

The contract is four artifacts. Define them *before* the agent
implements:

- **Intent** — the human outcome we want, and why. Not implementation.
- **Expectations** — how we will know it is done: BDD scenarios
  (Given/When/Then) and/or an acceptance checklist.
- **Context** — what the agent needs to know: repo, constraints,
  invariants, prior decisions, `CLAUDE.md`, memory.
- **Workflow** — the operational steps: GO gates, verification,
  push/release discipline.

> **Three Amigos, adapted.** Before the agent writes anything, the
> human(s) and the agent agree on Intent + Expectations. The classic
> "three amigos" (business, dev, test) collapse here into: *what
> outcome* (Intent), *how we'll check it* (Expectations), and *what the
> agent must not touch* (Non-goals). If you cannot state the
> Expectations, the agent will guess — make it guess from an explicit
> contract, not a vacuum.

## The four artifacts in detail

### Intent — the human outcome

State the outcome a person cares about, in their language. No file
names, no function signatures, no "add a flag to X".

- Good: *"The catalogue should have zero unresolved duplicate-FEN
  groups, so downstream consumers never hit an ambiguous slug."*
- Bad: *"Edit `audit_transpositions.py` to set `unresolved_groups=0`."*
  (That is a *task*, possibly the wrong one, and it pre-commits to a
  mechanism before we know it is right.)

Intent answers **why now** and **what changes for the user/consumer**.

### Expectations — how we know it's done

Expectations are the acceptance contract. Prefer **BDD scenarios**
(Given/When/Then) that are readable by a non-coder and verifiable by the
agent. Where a scenario does not fit, use an acceptance checklist. See
[BDD as Expectations](#bdd-as-expectations) below.

Every Expectation must be **checkable** — by a command, a metric, or an
observable artifact. "Looks good" is not an Expectation.

### Context — what the agent must know

The agent does not share your memory of the repo. Hand it:

- The relevant files and where the source of truth lives (for OCN: the
  catalogue CSV is the source of truth; artefacts are derived).
- **Invariants** that must hold (schema column count, `moves_uci`
  byte-stability, tags immutable, account/remote rules in `CLAUDE.md`).
- **Prior decisions** that constrain this one — link the decision
  records and proposals (e.g. the QID migration decision record).
- `CLAUDE.md` and any cross-session **memory** that applies.

If Context is thin, the agent will rediscover it (slowly) or assume it
(dangerously). Front-load it.

### Workflow — the operational steps

The default loop is **proposal → apply → verify**, escalated by task
size (see [Task sizing](#task-sizing)) and gated by explicit **GO**s
(see [GO gates](#go-gates)). Mutating and remote actions never happen on
inferred consent.

## BDD as Expectations

For each feature/intent, write **2–5** Given/When/Then scenarios. Each
scenario must be:

- **Readable by the business** — a non-coder understands what it
  asserts.
- **Verifiable by the agent** — it maps to a command, a metric, or an
  observable artifact the agent can check.

If you genuinely cannot write the scenario, the agent should still
*infer* the most likely one, state it back, and proceed under that
stated assumption (a [stop condition](#stop-conditions) if the
assumption is load-bearing and uncertain).

Example — the QID slug-migration intent, as scenarios:

```gherkin
Scenario: The last unresolved duplicate group is collapsed
  Given the catalogue has exactly one unresolved duplicate-FEN group
        (E.QID.Mil.MLn ⇄ E.QID.Pet.KPe)
  When the migration is applied
  Then `audit_transpositions.py --summary` reports unresolved_groups = 0

Scenario: No position changes, only identity
  Given the 10 descendants being re-slugged
  When the migration is applied
  Then `moves_uci` is byte-identical on all 10 rows
  And no FEN/position in the catalogue changes

Scenario: The naming lie is gone
  Given the re-slugged rows previously read "QID Miles, …"
  When the migration is applied
  Then no `canonical_name` on any E.QID.Pet.KPe.* row contains "Miles"

Scenario: Downstream contract is unbroken
  Given the schema is 14 columns
  When the migration is applied
  Then the schema is still 14 columns
  And the only downstream effect is regenerated artefacts (new sha256s)
```

Each `Then` is a command the agent can run — that is the point. BDD here
is not ceremony; it is the verification plan written in advance.

## When to use dynamic workflows

Dynamic workflows (multi-agent fan-out: an agent that plans, splits work
across parallel subagents, and verifies before reporting) are powerful
but **consume substantially more tokens**. Match the tool to the task.

**Use them for:**

- Wide **audits** across many files/entries (e.g. a player-eponym sweep
  over the whole catalogue).
- **Migrations** with many independent sites to transform.
- **Bug hunts** where breadth of search matters.
- **Adversarial verification** — independent agents trying to *refute* a
  finding before it is trusted.
- **Large refactors** that no single context can hold.

**Do not use them for:**

- Small changes, simple docs, edits to one or two files.
- Anything a single proposal→apply loop handles cleanly.

**Always:** start with a **scoped** slice. Prove the shape on a small
work-list first, read the result, then widen. Never fan out blind — the
cost is real and a wrong decomposition multiplies it.

## GO gates

Every mutating or outward-facing action waits for an explicit **GO**.
Approval for one gate does **not** carry to the next. The gates, in the
order OCN uses them:

| Gate | What it authorizes | Precondition |
|---|---|---|
| **GO proposal** | The agent writes a proposal / decision record / preflight (docs only). | Intent + Expectations agreed. |
| **GO apply** | The agent mutates the working tree (catalogue, code, docs). | Proposal reviewed; scope fenced. |
| **GO push** | `git push` to a remote. | Validation green; **account verified** per `CLAUDE.md` (`gh auth status` = `escacsfigueres` + `gh auth setup-git`). |
| **GO tag** | Create/move a version tag. | Release notes ready; tags are otherwise **immutable**. |
| **GO release / upload** | Cut a release, upload assets, regenerate downstream artefacts. | Downstream consumer (chess-parquet) impact confirmed. |
| **GO dynamic workflow** | Launch a multi-agent fan-out. | Scope bounded; token cost acknowledged; start-small slice defined. |

Rules:

- **One gate, one GO.** A GO apply is not a GO push. A GO push is not a
  GO tag.
- **Account safety is a hard gate.** Before any `gh`, `vercel`, or
  `git push`, confirm the active account is correct (`escacsfigueres` /
  `vercel-escacs`). If it is wrong: **STOP and ask** — do not write to
  any remote. (See `CLAUDE.md`.)
- **The catalogue, tags, and releases are never touched casually.** A
  docs-only or methodology task touches none of them.

## Task sizing

Escalate ceremony to risk. Pick the smallest loop that is honest about
the blast radius.

| Size | Shape | Loop |
|---|---|---|
| **tiny** | One/two files, no identity or contract change, reversible. | Direct apply + tests. |
| **normal** | A bounded feature or fix; clear Expectations. | Proposal → apply → verify. |
| **risky** | Changes identity, a contract, or something hard to reverse; downstream impact. | Proposal → **preflight** → **decision record** → apply (explicit GO) → verify. |
| **large / codebase-wide** | Sweeps, migrations, audits no single context holds. | **Dynamic workflow** + independent verification agents, scoped slice first. |

"Risky" is defined by **blast radius**, not line count: a one-line
change that renames a slug (row identity) or moves a tag is *risky*; a
500-line docs addition is *normal* or *tiny*.

## Reusable template

Copy this for any non-trivial intent:

```md
## Intent
What outcome do we want? (human language, not implementation)

## Expectations
Scenario: ...
  Given ...
  When ...
  Then ...   # must map to a command / metric / artifact

## Context
Repo, files, source of truth, constraints, invariants, prior decisions,
relevant CLAUDE.md rules and memory.

## Non-goals
What the agent must NOT touch (catalogue? tags? releases? a subsystem?).

## Workflow
Task size → loop. Proposal / apply / validation / push gates.

## Verification
Commands, checks, expected metrics. (The Then-clauses, executable.)

## Stop conditions
When to stop and ask instead of proceeding.
```

## Worked example — QID slug migration (a *risky* migration)

OCN's first slug-rename (`E.QID.Mil.MLn.* → E.QID.Pet.KPe.*`, 1 row
deleted) is the canonical *risky* case. It is documented across
[`qid-migration-decision-record.md`](qid-migration-decision-record.md)
(the go/no-go) and
[`qid-miles-petrosian-migration-preflight.md`](archive/qid-miles-petrosian-migration-preflight.md)
(the mechanics). Reconstructed against this playbook's contract:

**Intent.** *Collapse the last unresolved duplicate-FEN group so the
catalogue is fully resolved, and stop the Kasparov-Petrosian theory
subtree from living — and reading — as "Miles".* The user-visible
outcome: `unresolved_groups = 0` and honest names; no change for
position-lookup consumers.

**Expectations.** The four scenarios in
[BDD as Expectations](#bdd-as-expectations) above — each `Then` is one of
the preflight's verification commands (`audit_transpositions.py
--summary` → `unresolved_groups=0`, `rows=5,899`; `moves_uci`
byte-identical; no `canonical_name` says "Miles"; schema still 14
columns).

**Context.** Catalogue is the source of truth; `moves_uci`/FEN must not
change; this is the *first* slug-rename so it changes row **identity**
and `canonical_ocn1` downstream; tags `ocn-1.0.2`/`ocn-1.0.3` are
immutable; chess-parquet is the downstream consumer that must regenerate
`openings.parquet`. The decision record fixed the *when* (ride a release
boundary, not an out-of-band apply).

**Non-goals.** No schema change. No `moves_uci`/FEN change. No tag move.
No transposition-relation edits beyond collapsing this one group. Not
folded into any other commit.

**Workflow.** Sized **risky** → proposal (structural) → **preflight**
(exact row table, re-slug + relabel map) → **decision record** (Option C:
bundle with the release) → apply under explicit **GO apply** → verify →
the remaining steps (artefact regen, tag, upload) each behind their own
GO.

**Why this shape mattered.** The preflight caught that re-slugging
*alone* was insufficient — the `canonical_name` fields still read
"Miles", so the migration had to relabel them too. That finding came
from writing the mechanics down *before* applying. The decision record
separated *whether/when* from *how*, so the irreversible identity change
rode a version boundary where downstream churn was expected, not a
surprise. This is the playbook in one example: the discipline is what
caught the bug before it shipped.

## Stop conditions

Stop and ask the human when:

- A load-bearing assumption is uncertain (the Expectation cannot be
  written *and* the guess would change identity, a contract, or a
  remote).
- The active **account** is wrong for `gh`/`vercel`/`git push`
  (hard stop — never write to a remote on the wrong account).
- A change's scope creeps **beyond the agreed Non-goals** (e.g. a naming
  audit surfaces a new duplicate-FEN group → that is a *separate*
  sprint, not an inline edit).
- A `cherry-pick`/merge conflict appears **outside the expected scope**
  of the feature (see `CLAUDE.md` promotion checklist).
- Validation fails and the fix is not obviously within the current
  task's scope.

An honest "I stopped because X is ambiguous" is always better than a
confident wrong mutation.

## Relation to OCN's existing process

This playbook **formalises practice that already exists** in this repo —
it does not invent a new process:

- The proposal → preflight → decision-record → apply ladder is what the
  `docs/*-proposal.md`, `*-preflight.md`, and `*-decision-record.md`
  files already embody.
- The scope-fence + worked-example shape mirrors
  [`naming-attribution-audit-methodology.md`](naming-attribution-audit-methodology.md).
- The GO gates and account-safety rules come straight from
  [`../CLAUDE.md`](../CLAUDE.md) (remote/account verification,
  promotion checklist, worktree-per-stream).

## See also

- [`../CLAUDE.md`](../CLAUDE.md) — the repo's agent workflow conventions
  (accounts, promotion, worktrees, GO discipline).
- [`naming-attribution-audit-methodology.md`](naming-attribution-audit-methodology.md)
  — a methodology-only doc in the same house style.
- [`qid-migration-decision-record.md`](qid-migration-decision-record.md)
  and
  [`qid-miles-petrosian-migration-preflight.md`](archive/qid-miles-petrosian-migration-preflight.md)
  — the worked *risky migration* example.
- [`post-1.1-roadmap.md`](post-1.1-roadmap.md) — where post-1.1 work
  sits.
