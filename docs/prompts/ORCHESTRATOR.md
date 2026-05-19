# AI Rollout Training OS - Codex-Only Orchestrator

Version: 1.0
Execution model: Codex-only, no nested external AI process.

---

## Operating Rule

This project is operated from the current Codex session. Do not invoke an external Codex process, host-specific slash commands, or an Agent tool as part of the normal loop.

The current Codex session owns the loop end to end:

1. Read state.
2. Select one task.
3. Implement directly in the shared workspace.
4. Run tests and lint directly.
5. Review the diff in a separate review pass.
6. Update state files and commit when requested by the human.

The loop is nonstop. Do not pause between tasks or phases for routine permission to continue. A phase boundary is a verification, review, archive, and state-update checkpoint inside the same loop. After the checkpoint passes with no P0/P1 blockers, immediately select the next task and continue. Stop only for a true blocker, an unresolved P0/P1 finding, missing required human decision, failing baseline that prevents safe work, or an explicit human instruction to pause.

Use built-in Codex tools only. If the human explicitly asks for parallel subagents, split work into bounded, non-overlapping tasks; otherwise keep execution local and sequential.

## Required Inputs

Read these before starting a task:

- `docs/CODEX_PROMPT.md`
- `docs/tasks.md`
- `docs/IMPLEMENTATION_CONTRACT.md`
- task `Context-Refs`
- `docs/DECISION_LOG.md` when changing architecture, runtime, RAG, auth, approval boundaries, or prior decisions
- `docs/EVIDENCE_INDEX.md` when a task is heavy, RAG-tagged, eval-related, or resolves a finding

## Step 0 - Placeholder And State Check

Scan these files for unresolved template placeholders:

- `docs/ARCHITECTURE.md`
- `docs/IMPLEMENTATION_CONTRACT.md`
- `docs/CODEX_PROMPT.md`

If any active placeholder remains, stop and report:

```text
PLACEHOLDER_ERROR
File: {path}
Placeholder: {text}
Action required: replace with a concrete value before orchestration continues.
```

Then read current state from `docs/CODEX_PROMPT.md`:

- current phase
- current baseline
- next task
- open findings
- fix queue
- active profiles and eval state

## Step 1 - Select Work

Default selection order:

1. P0/P1 findings.
2. Fix Queue items blocking the current phase.
3. `docs/CODEX_PROMPT.md` Next Task.
4. The first uncompleted task in `docs/tasks.md`.

Only work on one implementation task at a time unless the human explicitly asks for parallel work.

## Step 2 - Pre-Task Protocol

Before editing files:

1. Read the selected task block in `docs/tasks.md`.
2. Read all Depends-On task blocks.
3. Read task `Context-Refs`.
4. Run `pytest -q` if tests exist; record baseline.
5. Run `ruff check` if ruff and source/test dirs exist; fix pre-existing lint separately if needed.
6. Confirm every acceptance criterion has a test reference.

If baseline tests fail before changes, stop and report `IMPLEMENTATION_RESULT: BLOCKED`.

## Step 3 - Implement Directly

Implement the selected task directly in the current workspace.

Rules:

- Use `apply_patch` for manual file edits.
- Keep edits inside the task `Files` scope unless a dependency requires a small supporting change.
- Do not silently expand solution shape, runtime tier, active profiles, or human approval boundaries.
- RAG tasks must preserve ingestion/query separation and the evaluation lifecycle.
- Heavy tasks must produce the evidence listed in their task block.

## Step 4 - Verify

Run the task's required tests and the general checks available at that point:

- `pytest -q`
- `ruff check ...`
- `ruff format --check ...`
- RAG eval checks for `rag:ingestion` / `rag:query` tasks

If a command cannot run because the skeleton or dependency is not present yet, record the exact reason in the implementation result.

## Step 5 - Review Pass

After implementation, switch to review mode in the same Codex session:

- prioritize bugs, regressions, missing tests, security issues, contract violations, and profile drift
- for RAG changes, check `insufficient_evidence`, corpus filtering, schema versioning, eval artifact updates, and ingestion/query separation
- for approval-boundary changes, check that AI cannot set human-owned states

If review finds blockers, fix them before marking the task done. If the issue is non-blocking, add it to `docs/CODEX_PROMPT.md` Open Findings or Fix Queue with severity and task reference.

## Step 6 - State Update

When a task is done:

1. Update `docs/CODEX_PROMPT.md`:
   - baseline
   - completed task
   - next task
   - open findings
   - eval state when applicable
2. Update `docs/IMPLEMENTATION_JOURNAL.md` for durable handoff context.
3. Update `docs/EVIDENCE_INDEX.md` if the task created or changed proof artifacts.
4. Update `docs/retrieval_eval.md` for RAG tasks.

Commit only when the human asks for a commit or when the current instruction explicitly includes commit/push.

## Phase Boundary

At the end of a phase:

1. Run all available tests and lint.
2. Run the relevant review prompts from `docs/audit/` as review passes in the current Codex session.
3. Write or update the phase review report in `docs/audit/`.
4. Update `docs/audit/AUDIT_INDEX.md`.
5. Update `docs/CODEX_PROMPT.md` Phase History.
6. Do not start the next phase with open P0/P1 findings.
7. If there are no open P0/P1 findings and required checks passed, continue directly to the first task of the next phase without waiting for a separate prompt.

## RAG-Specific Gate

For any task tagged `rag:ingestion` or `rag:query`, the task is not done until:

- `docs/retrieval_eval.md` is current or includes a valid not-yet-measured reason
- Eval Source, Date, and Corpus Version rules are satisfied once eval automation exists
- no-answer queries exercise `insufficient_evidence`
- retrieval changes compare against the current baseline once a baseline exists
- `docs/reference/dream_motif_rag_reuse.md` reuse constraints are respected

## Return Formats

When done:

```text
IMPLEMENTATION_RESULT: DONE
New baseline: {N passing tests or exact reason not run}
Commits: {hashes if committed, otherwise "not committed"}
Notes: {surprises, deviations, follow-ups}
```

When blocked:

```text
IMPLEMENTATION_RESULT: BLOCKED
Blocker: {exact blocker}
Type: dependency | interface_mismatch | environment | ambiguity
Recommended action: {what the human or next Codex turn should do}
Progress made: {what changed before the blocker}
```
