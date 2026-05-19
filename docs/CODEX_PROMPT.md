# CODEX_PROMPT.md

Version: 1.0
Date: 2026-05-19
Phase: 1

This file is the single source of truth for session state. Update it at task and phase boundaries.

---

## Current State

- Phase: 1
- Baseline: 0 passing tests (pre-implementation)
- Ruff: not yet configured
- Last CI run: not yet configured
- Last updated: 2026-05-19
- Session tokens: not yet tracked
- Cumulative phase tokens: not yet tracked
- Execution model: Codex-only current session; no external AI worker process

## Continuity Pointers

- Decision log: `docs/DECISION_LOG.md`
- Implementation journal: `docs/IMPLEMENTATION_JOURNAL.md`
- Evidence index: `docs/EVIDENCE_INDEX.md`
- Retrieval evaluation: `docs/retrieval_eval.md`
- Codex-only workflow: `reference/CODEX_ONLY_WORKFLOW.md`
- Task-scoped context: read `Context-Refs` in `docs/tasks.md` before broad searching

## Next Task

T01: Project Skeleton

## Fix Queue

empty

## Open Findings

none

## Profile State: RAG

- RAG Status: ON
- Active corpora: company policy, SOPs, role-pack content, rubrics, allowed/forbidden use cases, approved examples
- Retrieval mode: text-only
- Retrieval baseline: not yet measured
- Open retrieval findings: none
- Index schema version: v1 planned, not yet implemented
- Max index age: 7 days after ingestion exists
- Pending reindex actions: none
- Retrieval-related next tasks: T13, T14, T22
- Retrieval-driven tasks: none
- Reuse reference: `docs/reference/dream_motif_rag_reuse.md`

## Tool-Use State

- Tool-Use Profile: OFF
- Registered tool schemas: n/a
- Unsafe-action guardrails: n/a
- Open tool findings: none

## Agentic State

- Agentic Profile: OFF
- Active agent roles: n/a
- Loop termination contract version: n/a
- Cross-iteration state mechanism: n/a
- Open agent findings: none

## Planning State

- Planning Profile: OFF
- Plan schema version: n/a
- Plan validation method: n/a
- Open plan findings: none

## Compliance State

- Compliance Status: OFF
- Active frameworks: n/a
- Controls implemented: n/a
- Controls partial: n/a
- Controls not started: n/a
- Evidence artifact: n/a
- Open compliance findings: none

## NFR Baseline

- API p99 latency: not yet measured
- Feedback p95 latency: target under 60 seconds, not yet measured
- Retrieval p95 latency: not yet measured
- Error rate: not yet measured
- Throughput: not yet measured
- Last measured: none
- NFR regression open: No

## Evaluation State

### Last Evaluation

- Profile: RAG
- Task: n/a
- Date: n/a
- Eval Source: n/a
- Metric(s): n/a
- Score: n/a
- Baseline: n/a
- Delta: n/a
- Regression: n/a

### Open Evaluation Issues

none

### Evaluation History

| Date | Task | Profile | Key metric | Score | Baseline | Delta | Regression? |
|------|------|---------|------------|-------|----------|-------|-------------|

## Completed Tasks

none

## Phase History

none

## Compaction Protocol

Compact this file when either condition is true:

- `## Completed Tasks` contains more than 20 entries.
- `## Phase History` contains more than 5 phase summaries.

When compacting, create or update `## Summary State` immediately after `## Current State`, retain the 5 most recent completed tasks, retain the 2 most recent phase summaries, and move older entries to archive sections. Do not delete history.

## Instructions for Codex

1. Read the orchestrator's inline task digest first.
2. Read `docs/tasks.md` for the current task entry.
3. Read `docs/IMPLEMENTATION_CONTRACT.md` when the digest does not inline applicable rules or when the task touches a risky boundary.
4. Read Depends-On tasks, `Context-Refs`, and continuity artifacts when the task depends on prior decisions, proof, or findings.
5. Execute tasks directly in the current Codex session; do not launch an external AI worker process.
6. Run `pytest -q` before changing code and record the baseline. If tests fail, stop and report the blocker.
7. Run `ruff check`. It must exit 0 before implementation work proceeds. Fix lint in a separate commit if needed.
8. Write tests before or alongside implementation. Every acceptance criterion has at least one test.
9. For RAG tasks, update `docs/retrieval_eval.md` and this file's evaluation state before returning done.
10. Update this file at task completion: new baseline, completed task, next task, and any open findings.
11. Commit with format `type(scope): description`; one logical change per commit.

## Return Format

When done, return exactly:

```text
IMPLEMENTATION_RESULT: DONE
New baseline: {N} passing tests
Commits: {list of commit hashes and messages}
Notes: {anything the orchestrator should know}
```

When blocked, return exactly:

```text
IMPLEMENTATION_RESULT: BLOCKED
Blocker: {exact blocker}
Type: dependency | interface_mismatch | environment | ambiguity
Recommended action: {what the orchestrator or human should do}
Progress made: {what was completed before the blocker}
```
